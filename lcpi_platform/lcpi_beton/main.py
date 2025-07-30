

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

@app.command(name="calc")
def run_calc_from_file(filepath: str):
    # ... (code existant, pas besoin de le copier)
    pass # Déjà fonctionnel

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
