import typer
import json
import yaml
from .core.design.column_design import design_rectangular_column, design_column_compression_bael
from .core.materials import Beton, Acier
from .core.sections import SectionRectangulaire
from .core.analysis.continuous_beam import analyze_by_forfaitaire
# Variable globale pour la sortie JSON (sera définie par le noyau)
_json_output_enabled = False
from rich.console import Console
from rich.panel import Panel

console = Console()

# --- Logique pure pour le Poteau ---
def _calculer_poteau_beton_logic(data: dict) -> dict:
    try:
        beton = Beton(fc28=data.get("fc28_MPa", 25.0))
        acier = Acier(fe=data.get("fe_MPa", 500.0))
        section = SectionRectangulaire(b=data.get("largeur_b_m"), h=data.get("hauteur_h_m"))
        type_calcul = data.get("type_calcul")
        if type_calcul == "flexion_composee":
            resultats = design_rectangular_column(Nu=data.get("Nu_MN"), Mu=data.get("Mu_MNm"), section=section, beton=beton, acier=acier, height=data.get("longueur_L_m"), k_factor=data.get("k_flambement"))
        elif type_calcul == "compression_centree":
            resultats = design_column_compression_bael(Nu=data.get("Nu_MN"), section=section, beton=beton, acier=acier, height=data.get("longueur_L_m"), k_factor=data.get("k_flambement"))
        else: return {"statut": "Erreur", "message": f"Type de calcul inconnu : {type_calcul}"}
        resultats["statut"] = "OK"
        return resultats
    except Exception as e: return {"statut": "Erreur", "message": str(e)}

# --- Logique pure pour le Radier ---
def _calculer_radier_beton_logic(data: dict) -> dict:
    try:
        geo = data.get("geometrie", {}); dim_A = geo.get("dimension_A_m"); dim_B = geo.get("dimension_B_m"); h_radier = geo.get("epaisseur_h_m"); poteaux = data.get("poteaux", [])
        if not all([dim_A, dim_B, h_radier, poteaux]): return {"statut": "Erreur", "message": "Données géométriques ou poteaux manquants."}
        total_p_u_kN = sum([(p.get('charge_G_kN', 0) * 1.35 + p.get('charge_Q_kN', 0) * 1.5) for p in poteaux])
        surface_radier = dim_A * dim_B; q_u_kPa = total_p_u_kN / surface_radier if surface_radier > 0 else 0
        moments = {}
        w_u_X = q_u_kPa * dim_B; positions_x = sorted(list(set(p['position_x_m'] for p in poteaux))); travées_x = [positions_x[i+1] - positions_x[i] for i in range(len(positions_x)-1)]
        if travées_x:
            moments_x = analyze_by_forfaitaire(travées_x, w_u_X)
            moments['bande_X'] = {"charge_lineique_kN_m": round(w_u_X, 2), "moments_travées_kNm": [round(m, 2) for m in moments_x["travees"]], "moments_appuis_kNm": [round(m, 2) for m in moments_x["appuis"]]}
        w_u_Y = q_u_kPa * dim_A; positions_y = sorted(list(set(p['position_y_m'] for p in poteaux))); travées_y = [positions_y[i+1] - positions_y[i] for i in range(len(positions_y)-1)]
        if travées_y:
            moments_y = analyze_by_forfaitaire(travées_y, w_u_Y)
            moments['bande_Y'] = {"charge_lineique_kN_m": round(w_u_Y, 2), "moments_travées_kNm": [round(m, 2) for m in moments_y["travees"]], "moments_appuis_kNm": [round(m, 2) for m in moments_y["appuis"]]}
        return {"statut": "OK", "pression_sol_elu_kPa": round(q_u_kPa, 2), "moments_calcules": moments}
    except Exception as e: return {"statut": "Erreur", "message": str(e)}

# --- Commandes du Plugin ---
app = typer.Typer(name="beton", help="Plugin pour le Béton Armé (BAEL 91 / Eurocode 2)")

@app.command(name="calc-poteau")
def run_calc_from_file(
    filepath: str = typer.Option(None, "--filepath", "-f", help="Chemin vers le fichier de définition YAML unique."),
    batch_file: str = typer.Option(None, "--batch-file", "-b", help="Chemin vers le fichier CSV pour le traitement par lot de POTEAUX."),
    output_file: str = typer.Option("resultats_batch_beton.csv", "--output-file", "-o", help="Chemin pour le fichier de résultats CSV.")
):
    """Calcule un ou plusieurs poteaux en béton à partir d'un fichier."""
    # Si aucun paramètre obligatoire n'est fourni, afficher les paramètres d'entrée
    if filepath is None and batch_file is None:
        from ..utils.command_helpers import show_input_parameters, create_parameter_dict
        
        required_params = [
            create_parameter_dict("filepath", "Chemin vers le fichier de définition YAML unique", "f"),
            create_parameter_dict("batch-file", "Chemin vers le fichier CSV pour le traitement par lot", "b")
        ]
        
        optional_params = [
            create_parameter_dict("output-file", "Chemin pour le fichier de résultats CSV", default="resultats_batch_beton.csv")
        ]
        
        examples = [
            "lcpi beton calc-poteau --filepath poteau_beton.yml",
            "lcpi beton calc-poteau --batch-file lot_poteaux.csv --output-file resultats.csv",
            "lcpi beton calc-poteau -f poteau_beton.yml",
            "lcpi beton calc-poteau -b lot_poteaux.csv -o resultats.csv"
        ]
        
        show_input_parameters(
            "Calcul Poteau (Béton)",
            required_params,
            optional_params,
            examples,
            "Calcule un ou plusieurs poteaux en béton selon BAEL 91 / Eurocode 2."
        )
        return

    if batch_file:
        try:
            import pandas as pd
        except ImportError:
            if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": "La bibliothèque 'pandas' est requise. Installez-la avec 'pip install pandas'."}))
            else: console.print(Panel("Erreur : La bibliothèque 'pandas' est requise. Installez-la avec 'pip install pandas'.", title="Erreur de Dépendance", border_style="red"))
            raise typer.Exit(code=1)

        if not _json_output_enabled:
            console.print(f"--- Lancement du Traitement par Lot (Poteaux Béton) depuis : {batch_file} ---")
        try:
            df = pd.read_csv(batch_file)
            results_list = []
            for index, row in df.iterrows():
                mu = row.get('Mu_MNm', 0.0)
                donnees_calcul = {
                    "Nu_MN": row['Nu_MN'], "Mu_MNm": mu,
                    "largeur_b_m": row['largeur_b_m'], "hauteur_h_m": row['hauteur_h_m'],
                    "longueur_L_m": row['longueur_L_m'], "k_flambement": row.get('k_flambement', 1.0),
                    "fc28_MPa": row.get('fc28_MPa', 25.0), "fe_MPa": row.get('fe_MPa', 500.0),
                    "type_calcul": "flexion_composee" if mu > 0 else "compression_centree"
                }
                resultats_calcul = _calculer_poteau_beton_logic(donnees_calcul)
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
            with open(filepath, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": f"Fichier non trouvé: {filepath}"}))
            else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Le fichier '{filepath}' n'a pas été trouvé.", title="Erreur de Fichier", border_style="red"))
            raise typer.Exit(code=1)
        except yaml.YAMLError as e:
            if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": f"Erreur de parsing YAML: {e}"}))
            else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Erreur lors du parsing du fichier YAML : {e}", title="Erreur de Parsing", border_style="red"))
            raise typer.Exit(code=1)

        mu = config.get("sollicitations", {}).get("Mu_MNm", 0.0)
        donnees_calcul = {
            "Nu_MN": config.get("sollicitations", {}).get("Nu_MN"), "Mu_MNm": mu,
            "largeur_b_m": config.get("geometrie", {}).get("largeur_b_m"), "hauteur_h_m": config.get("geometrie", {}).get("hauteur_h_m"),
            "longueur_L_m": config.get("geometrie", {}).get("longueur_L_m"), "k_flambement": config.get("geometrie", {}).get("k_flambement", 1.0),
            "fc28_MPa": config.get("materiau", {}).get("fc28_MPa", 25.0), "fe_MPa": config.get("materiau", {}).get("fe_MPa", 500.0),
            "type_calcul": "flexion_composee" if mu > 0 else "compression_centree"
        }
        resultats = _calculer_poteau_beton_logic(donnees_calcul)
        
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2))
        else:
            console.print(f"Calcul de l'élément BÉTON défini dans : {filepath}")
            console.print(f"Résultats : {resultats}")
    else:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": "Vous devez spécifier soit --filepath, soit --batch-file."}))
        else: console.print(Panel("[bold red]ERREUR[/bold red]: Vous devez spécifier soit --filepath, soit --batch-file.", title="Erreur d'Argument", border_style="red"))
        raise typer.Exit(code=1)

@app.command(name="calc-radier")
def run_calc_radier_from_file(filepath: str = typer.Option(None, "--filepath", "-f", help="Chemin vers le fichier de définition YAML du radier.")):
    """Calcule un radier en béton à partir d'un fichier YAML."""
    # Si aucun paramètre obligatoire n'est fourni, afficher les paramètres d'entrée
    if filepath is None:
        from ..utils.command_helpers import show_input_parameters, create_parameter_dict
        
        required_params = [
            create_parameter_dict("filepath", "Chemin vers le fichier de définition YAML du radier", "f")
        ]
        
        examples = [
            "lcpi beton calc-radier --filepath radier_beton.yml",
            "lcpi beton calc-radier -f radier_beton.yml"
        ]
        
        show_input_parameters(
            "Calcul Radier (Béton)",
            required_params,
            examples=examples,
            description="Calcule un radier en béton selon BAEL 91 / Eurocode 2."
        )
        return

    try:
        with open(filepath, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": f"Fichier non trouvé: {filepath}"}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Le fichier '{filepath}' n'a pas été trouvé.", title="Erreur de Fichier", border_style="red"))
        raise typer.Exit(code=1)
    except yaml.YAMLError as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": f"Erreur de parsing YAML: {e}"}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Erreur lors du parsing du fichier YAML : {e}", title="Erreur de Parsing", border_style="red"))
        raise typer.Exit(code=1)

    donnees_calcul = config
    resultats = _calculer_radier_beton_logic(donnees_calcul)

    if _json_output_enabled:
        console.print(json.dumps(resultats, indent=2))
    else:
        console.print(f"Calcul du radier défini dans : {filepath}")
        console.print(f"Résultats : {resultats}")

@app.command(name="interactive")
def run_interactive_mode():
    """Lance le mode interactif pour le calcul des éléments en béton."""
    if _json_output_enabled:
        console.print(json.dumps({"statut": "Erreur", "message": "Le mode interactif n'est pas compatible avec la sortie JSON."}))
        raise typer.Exit(code=1)

    console.print(Panel(
        "[bold blue]Mode Interactif - Calcul Béton Armé[/bold blue]\n\n"
        "Ce mode interactif vous guide dans le calcul d'éléments en béton armé.\n"
        "Fonctionnalité en cours de développement...",
        title="[bold green]Mode Interactif Béton[/bold green]",
        border_style="blue"
    ))

def register():
    return app