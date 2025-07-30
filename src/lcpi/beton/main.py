

import typer
import json
import yaml
# Imports depuis les fichiers du plugin
from .core.design.column_design import design_rectangular_column, design_column_compression_bael
from .core.materials import Beton, Acier
from .core.sections import SectionRectangulaire
from .core.analysis.continuous_beam import analyze_by_forfaitaire

# --- Logique pure pour le Poteau ---
def _calculer_poteau_beton_logic(data: dict) -> dict:
    # ... (code existant, pas besoin de le copier)
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
    # ... (code existant, pas besoin de le copier)
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
    filepath: str = typer.Option(None, "--filepath", help="Chemin vers le fichier de définition YAML unique."),
    batch_file: str = typer.Option(None, "--batch-file", help="Chemin vers le fichier CSV pour le traitement par lot de POTEAUX."),
    output_file: str = typer.Option("resultats_batch_beton.csv", "--output-file", help="Chemin pour le fichier de résultats CSV."),
    as_json: bool = typer.Option(False, "--json", help="Afficher la sortie au format JSON (pour un seul fichier).")
):
    """Calcule un ou plusieurs poteaux en béton à partir d'un fichier."""
    if batch_file:
        try:
            import pandas as pd
        except ImportError:
            print("Erreur : La bibliothèque 'pandas' est requise. Installez-la avec 'pip install pandas'.")
            raise typer.Exit(code=1)

        print(f"--- Lancement du Traitement par Lot (Poteaux Béton) depuis : {batch_file} ---")
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
            print(f"[SUCCES] Traitement par lot terminé. Résultats sauvegardés dans : {output_file}")

        except Exception as e:
            print(f"Une erreur est survenue lors du traitement par lot : {e}")
            raise typer.Exit(code=1)

    elif filepath:
        # Logique existante pour le fichier YAML unique...
        # (le code reste le même ici)
        print("Logique YAML pour un seul poteau à implémenter si nécessaire.")
    else:
        print("Erreur : Vous devez spécifier soit --filepath, soit --batch-file.")
        raise typer.Exit(code=1)

@app.command(name="calc-radier")
def run_calc_radier_from_file(filepath: str):
    # ... (code existant, pas besoin de le copier)
    pass # Déjà fonctionnel

@app.command(name="interactive")
def run_interactive_mode():
    """Lance le mode interactif pour le calcul des éléments en béton."""
    print("--- Mode Interactif : Béton Armé ---")
    choix = typer.prompt("Quel élément voulez-vous calculer ? (1: Poteau, 2: Radier)", type=int)

    if choix == 1:
        print("\n-- Calcul d'un Poteau --")
        try:
            nu = typer.prompt("Effort normal ultime Nu (MN)", type=float)
            mu = typer.prompt("Moment ultime Mu (MN.m)", type=float, default=0.0)
            b = typer.prompt("Largeur b (m)", type=float)
            h = typer.prompt("Hauteur h (m)", type=float)
            longueur = typer.prompt("Longueur de flambement (m)", type=float)
            
            donnees_calcul = {
                "Nu_MN": nu, "Mu_MNm": mu,
                "largeur_b_m": b, "hauteur_h_m": h,
                "longueur_L_m": longueur, "k_flambement": 1.0, # Simplification
                "fc28_MPa": 25.0, "fe_MPa": 500.0,
                "type_calcul": "flexion_composee" if mu > 0 else "compression_centree"
            }

            resultats = _calculer_poteau_beton_logic(donnees_calcul)
            print("\n--- Résultats du Calcul Poteau ---")
            print(json.dumps(resultats, indent=2, ensure_ascii=False))

        except Exception as e:
            print(f"\nErreur : {e}")

    elif choix == 2:
        print("\n-- Calcul d'un Radier --")
        print("Le mode interactif pour le calcul des radiers est en cours de développement.")
        # TODO: Ajouter les prompts pour collecter les données du radier
        # et appeler _calculer_radier_beton_logic
    else:
        print("Choix invalide.")

def register():
    return app
