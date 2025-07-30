import typer
import json
import yaml
# Assure-toi que les imports suivants sont corrects par rapport à la structure
from .calculs import verifier_section_bois
from lcpi.calculs import calculer_sollicitations_completes

def _verifier_poutre_bois_logic(data: dict) -> dict:
    # ... (La logique de calcul existante, déjà migrée, reste ici)
    # ... (Pas besoin de la copier dans le prompt, mais on sait qu'elle est là)
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
    output_file: str = typer.Option("resultats_batch_bois.csv", "--output-file", help="Chemin pour le fichier de résultats CSV."),
    as_json: bool = typer.Option(False, "--json", help="Afficher la sortie au format JSON (pour un seul fichier).")
):
    """Vérifie une ou plusieurs poutres en bois à partir d'un fichier."""
    if batch_file:
        try:
            import pandas as pd
        except ImportError:
            print("Erreur : La bibliothèque 'pandas' est requise. Installez-la avec 'pip install pandas'.")
            raise typer.Exit(code=1)
        
        print(f"--- Lancement du Traitement par Lot (Bois) depuis : {batch_file} ---")
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
            print(f"[SUCCES] Traitement par lot terminé. Résultats sauvegardés dans : {output_file}")

        except Exception as e:
            print(f"Une erreur est survenue lors du traitement par lot : {e}")
            raise typer.Exit(code=1)

    elif filepath:
        # Logique existante pour le fichier YAML unique...
        # (le code reste le même ici)
        try:
            with open(filepath, 'r') as f: config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{filepath}' n'a pas été trouvé.")
            raise typer.Exit(code=1)
        # ... reste de la logique YAML
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
        if as_json: print(json.dumps(resultats, indent=2))
        else: print(f"Résultats : {resultats}")
    else:
        print("Erreur : Vous devez spécifier soit --filepath, soit --batch-file.")
        raise typer.Exit(code=1)

@app.command(name="interactive")
def run_interactive_mode():
    """Lance le mode interactif pour la vérification d'une poutre en bois."""
    print("--- Mode Interactif : Poutre en Bois ---")
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
        print("\n--- Résultats de la Vérification ---")
        print(json.dumps(resultats, indent=2))

    except Exception as e:
        print(f"\nErreur : {e}")

def register():
    return app