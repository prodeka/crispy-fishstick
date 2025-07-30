import typer
import json
import yaml
from .calculs import trouver_profil_acier # Assure-toi que cet import est correct
from lcpi_core.calculs import calculer_sollicitations_completes # Assure-toi que cet import est correct

def _calculer_poutre_acier_logic(data: dict) -> dict:
    # ... (La logique de calcul existante reste ici)
    # ... (Pas besoin de la copier dans le prompt)
    longueur = data.get("longueur")
    charges_entrees = data.get("charges")
    nuance = data.get("nuance")
    fy = data.get("fy_MPa")
    E_module = data.get("E_MPa")
    famille_profil = data.get("famille_profil", "IPE")
    if not all([longueur, nuance, fy, E_module]) or charges_entrees is None:
        return {"statut": "Erreur", "message": "Données d'entrée incomplètes."}
    try:
        sollicitations = calculer_sollicitations_completes(longueur, charges_entrees, "acier", "A", verbose=False)
        profil_recommande = trouver_profil_acier(sollicitations["M_Ed"], sollicitations["V_Ed"], longueur, sollicitations["p_ser"], famille_profil=famille_profil, nuance=nuance, fy_MPa=fy, E_MPa=E_module, verbose=False)
        return {"profil_recommande": profil_recommande, "M_Ed": sollicitations["M_Ed"], "V_Ed": sollicitations["V_Ed"], "p_ser": sollicitations["p_ser"], "statut": "OK"}
    except Exception as e:
        return {"statut": "Erreur", "message": str(e)}
        
app = typer.Typer(name="cm", help="Plugin pour la Construction Métallique")

@app.command(name="calc")
def run_calc_from_file(
    filepath: str = typer.Option(None, "--filepath", help="Chemin vers le fichier de définition YAML unique."),
    batch_file: str = typer.Option(None, "--batch-file", help="Chemin vers le fichier CSV pour le traitement par lot."),
    output_file: str = typer.Option("resultats_batch.csv", "--output-file", help="Chemin pour le fichier de résultats CSV."),
    as_json: bool = typer.Option(False, "--json", help="Afficher la sortie au format JSON (pour un seul fichier).")
):
    """Calcule une ou plusieurs poutres en acier à partir d'un fichier."""
    if batch_file:
        try:
            import pandas as pd
        except ImportError:
            print("Erreur : La bibliothèque 'pandas' est requise pour le mode batch. Installez-la avec 'pip install pandas'.")
            raise typer.Exit(code=1)
            
        print(f"--- Lancement du Traitement par Lot depuis : {batch_file} ---")
        try:
            df = pd.read_csv(batch_file)
            results_list = []
            
            for index, row in df.iterrows():
                # Construire les données de charges à partir des colonnes G et Q
                charges_list = [
                    {'categorie': 'G', 'valeur': row['charge_G_kn_m'], 'type': 'repartie'},
                    {'categorie': 'Q', 'valeur': row['charge_Q_kn_m'], 'type': 'repartie'}
                ]
                
                donnees_calcul = {
                    "longueur": row['longueur_m'],
                    "charges": charges_list,
                    "nuance": row.get('nuance', 'S235'),
                    "fy_MPa": row.get('fy_MPa', 235.0),
                    "E_MPa": row.get('E_MPa', 210000.0),
                    "famille_profil": row.get('famille_profil', 'IPE'),
                }
                
                resultats_calcul = _calculer_poutre_acier_logic(donnees_calcul)
                
                # Fusionner les résultats avec la ligne d'entrée
                output_row = row.to_dict()
                output_row.update(resultats_calcul)
                results_list.append(output_row)

            results_df = pd.DataFrame(results_list)
            results_df.to_csv(output_file, index=False)
            print(f"[SUCCES] Traitement par lot terminé. Résultats sauvegardés dans : {output_file}")

        except FileNotFoundError:
            print(f"Erreur : Le fichier batch '{batch_file}' n'a pas été trouvé.")
            raise typer.Exit(code=1)
        except Exception as e:
            print(f"Une erreur est survenue lors du traitement par lot : {e}")
            raise typer.Exit(code=1)

    elif filepath:
        try:
            with open(filepath, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            if as_json: print(json.dumps({"statut": "Erreur", "message": f"Fichier non trouvé: {filepath}"}))
            else: print(f"Erreur : Le fichier '{filepath}' n'a pas été trouvé.")
            raise typer.Exit(code=1)
        except yaml.YAMLError as e:
            if as_json: print(json.dumps({"statut": "Erreur", "message": f"Erreur de parsing YAML: {e}"}))
            else: print(f"Erreur lors du parsing du fichier YAML : {e}")
            raise typer.Exit(code=1)

        charges_list = []
        if config.get("charges"):
            for charge in config["charges"].get("permanentes_G", []):
                charge['categorie'] = 'G'
                charges_list.append(charge)
            for charge in config["charges"].get("exploitation_Q", []):
                charge['categorie'] = 'Q'
                charges_list.append(charge)

        donnees_calcul = {
            "longueur": config.get("geometrie", {}).get("longueur_m"),
            "charges": charges_list,
            "nuance": config.get("materiau", {}).get("nuance"),
            "fy_MPa": config.get("materiau", {}).get("fy_MPa"),
            "E_MPa": config.get("materiau", {}).get("E_MPa"),
            "famille_profil": config.get("geometrie", {}).get("famille_profil", "IPE"),
        }
        resultats = _calculer_poutre_acier_logic(donnees_calcul)
        
        if as_json:
            print(json.dumps(resultats, indent=2))
        else:
            print(f"Calcul de l'élément ACIER défini dans : {filepath}")
            print(f"Résultats : {resultats}")
    else:
        print("Erreur : Vous devez spécifier soit --filepath, soit --batch-file.")
        raise typer.Exit(code=1)

@app.command(name="interactive")
def run_interactive_mode():
    """Lance le mode interactif pour le calcul d'une poutre en acier."""
    print("--- Mode Interactif : Poutre en Acier ---")
    try:
        longueur = typer.prompt("Longueur de la poutre (m)", type=float)
        charge_g = typer.prompt("Charge permanente G (kN/m)", type=float)
        charge_q = typer.prompt("Charge d'exploitation Q (kN/m)", type=float)
        famille = typer.prompt("Famille de profilé (IPE ou HEA)", default="IPE")

        donnees_calcul = {
            "longueur": longueur,
            "charges": [
                {'categorie': 'G', 'valeur': charge_g, 'type': 'repartie'},
                {'categorie': 'Q', 'valeur': charge_q, 'type': 'repartie'}
            ],
            "nuance": "S235",
            "fy_MPa": 235.0,
            "E_MPa": 210000.0,
            "famille_profil": famille.upper()
        }
        
        resultats = _calculer_poutre_acier_logic(donnees_calcul)
        print("\n--- Résultats du Calcul ---")
        print(json.dumps(resultats, indent=2))

    except Exception as e:
        print(f"\nErreur : {e}")

def register():
    return app