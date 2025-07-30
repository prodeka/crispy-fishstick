import typer
import json
import yaml
from .calculs import verifier_section_bois
from lcpi.calculs import calculer_sollicitations_completes
from lcpi.main import _json_output_enabled
from rich.console import Console
from rich.panel import Panel

console = Console()

def _verifier_poutre_bois_logic(data: dict) -> dict:
    b = data.get("b_mm")
    h = data.get("h_mm")
    longueur = data.get("longueur_m")
    charges_entrees = data.get("charges")
    classe_bois = data.get("classe_bois")
    classe_service = data.get("classe_service")
    duree_charge = data.get("duree_charge")
    if not all([b, h, longueur, charges_entrees, classe_bois, classe_service, duree_charge]):
        return {"statut": "Erreur", "message": "Données d'entrée incomplètes."}
    try:
        sollicitations = calculer_sollicitations_completes(longueur, charges_entrees, "bois", "A", verbose=False)
        message, est_valide = verifier_section_bois(b, h, longueur, sollicitations, classe_bois, classe_service, duree_charge, verbose=False)
        return {"section": f"{b}x{h} mm", "statut": "OK" if est_valide else "Non Adéquat", "message": message, "est_valide": bool(est_valide)}
    except Exception as e:
        return {"statut": "Erreur", "message": str(e)}

app = typer.Typer(name="bois", help="Plugin pour les Structures en Bois (Eurocode 5)")

@app.command(name="check")
def run_check_from_file(
    filepath: str = typer.Option(None, "--filepath", help="Chemin vers le fichier de définition YAML unique."),
    batch_file: str = typer.Option(None, "--batch-file", help="Chemin vers le fichier CSV pour le traitement par lot."),
    output_file: str = typer.Option("resultats_batch_bois.csv", "--output-file", help="Chemin pour le fichier de résultats CSV.")
):
    """Vérifie une ou plusieurs poutres en bois à partir d'un fichier."""
    if batch_file:
        try:
            import pandas as pd
        except ImportError:
            if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": "La bibliothèque 'pandas' est requise pour le mode batch. Installez-la avec 'pip install pandas'."}))
            else: console.print(Panel("Erreur : La bibliothèque 'pandas' est requise pour le mode batch. Installez-la avec 'pip install pandas'.", title="Erreur de Dépendance", border_style="red"))
            raise typer.Exit(code=1)
        
        if not _json_output_enabled:
            console.print(f"--- Lancement du Traitement par Lot (Bois) depuis : {batch_file} ---")
        try:
            df = pd.read_csv(batch_file)
            results_list = []
            for index, row in df.iterrows():
                charges_list = [
                    {'categorie': 'G', 'valeur': row['charge_G_kn_m'], 'type': 'repartie'},
                    {'categorie': 'Q', 'valeur': row['charge_Q_kn_m'], 'type': 'repartie'}
                ]
                donnees_calcul = {
                    "b_mm": row['largeur_b_mm'], "h_mm": row['hauteur_h_mm'], "longueur_m": row['longueur_m'],
                    "charges": charges_list, "classe_bois": row['classe_bois'],
                    "classe_service": row['classe_service'], "duree_charge": row['duree_charge']
                }
                resultats_calcul = _verifier_poutre_bois_logic(donnees_calcul)
                output_row = row.to_dict()
                output_row.update(resultats_calcul)
                results_list.append(output_row)
            
            results_df = pd.DataFrame(results_list)
            results_df.to_csv(output_file, index=False)
            if not _json_output_enabled:
                console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Traitement par lot terminé. Résultats sauvegardés dans : {output_file}", title="Traitement par Lot", border_style="green"))

        except Exception as e:
            if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": f"Une erreur est survenue lors du traitement par lot : {e}"}))
            else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Une erreur est survenue lors du traitement par lot : {e}", title="Erreur de Traitement", border_style="red"))
            raise typer.Exit(code=1)

    elif filepath:
        try:
            with open(filepath, 'r') as f: config = yaml.safe_load(f)
        except FileNotFoundError:
            if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": f"Fichier non trouvé: {filepath}"}))
            else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Le fichier '{filepath}' n'a pas été trouvé.", title="Erreur de Fichier", border_style="red"))
            raise typer.Exit(code=1)
        except yaml.YAMLError as e:
            if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": f"Erreur de parsing YAML: {e}"}))
            else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Erreur lors du parsing du fichier YAML : {e}", title="Erreur de Parsing", border_style="red"))
            raise typer.Exit(code=1)

        charges_list = []
        if config.get("charges"):
            for charge in config["charges"].get("permanentes_G", []): charge['categorie'] = 'G'; charges_list.append(charge)
            for charge in config["charges"].get("exploitation_Q", []): charge['categorie'] = 'Q'; charges_list.append(charge)
        donnees_calcul = {
            "b_mm": config.get("geometrie", {}).get("b_mm"), "h_mm": config.get("geometrie", {}).get("h_mm"),
            "longueur_m": config.get("geometrie", {}).get("longueur_m"), "charges": charges_list,
            "classe_bois": config.get("materiau", {}).get("classe_bois"), "classe_service": config.get("materiau", {}).get("classe_service"),
            "duree_charge": config.get("materiau", {}).get("duree_charge"),
        }
        resultats = _verifier_poutre_bois_logic(donnees_calcul)
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2))
        else:
            console.print(f"Résultats : {resultats}")
    else:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": "Vous devez spécifier soit --filepath, soit --batch-file."}))
        else: console.print(Panel("[bold red]ERREUR[/bold red]: Vous devez spécifier soit --filepath, soit --batch-file.", title="Erreur d'Argument", border_style="red"))
        raise typer.Exit(code=1)

@app.command(name="interactive")
def run_interactive_mode():
    """Lance le mode interactif pour la vérification d'une poutre en bois."""
    if _json_output_enabled:
        console.print(json.dumps({"statut": "Erreur", "message": "Le mode interactif n'est pas compatible avec la sortie JSON."}))
        raise typer.Exit(code=1)

    console.print("--- Mode Interactif : Poutre en Bois ---")
    try:
        b = typer.prompt("Largeur de la section (mm)", type=int)
        h = typer.prompt("Hauteur de la section (mm)", type=int)
        longueur = typer.prompt("Longueur de la poutre (m)", type=float)
        charge_g = typer.prompt("Charge permanente G (kN/m)", type=float)
        charge_q = typer.prompt("Charge d'exploitation Q (kN/m)", type=float)
        classe_bois = typer.prompt("Classe du bois (ex: C24)", default="C24")
        classe_service = typer.prompt("Classe de service (classe_1, classe_2, classe_3)", default="classe_1")
        duree = typer.prompt("Durée de la charge (permanente, long_terme, ...)", default="permanente")
        
        donnees_calcul = {
            "b_mm": b, "h_mm": h, "longueur_m": longueur,
            "charges": [
                {'categorie': 'G', 'valeur': charge_g, 'type': 'repartie'},
                {'categorie': 'Q', 'valeur': charge_q, 'type': 'repartie'}
            ],
            "classe_bois": classe_bois,
            "classe_service": classe_service,
            "duree_charge": duree
        }

        resultats = _verifier_poutre_bois_logic(donnees_calcul)
        console.print("\n--- Résultats de la Vérification ---")
        console.print(json.dumps(resultats, indent=2))

    except Exception as e:
        console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur", border_style="red"))

def register():
    return app