# modules/hydrologie/caquot.py
import math
import sys
import os

# Ajoute le dossier parent (CODE) au chemin de recherche de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.shared_formulas import dimensionner_section
from utils.ui import print_colored

# --- Coefficients spécifiques à la formule de Caquot ---
# Ces valeurs sont des constantes issues de la théorie hydrologique de Caquot.
CAQUOT_BETA_DELTA, CAQUOT_EPSILON, CAQUOT_MU_C1, CAQUOT_MU_C2, CAQUOT_C, CAQUOT_D, CAQUOT_F = 1.40, 0.05, 0.19, 0.84, -0.41, 0.507, -0.287

# --- Formule SPÉCIFIQUE à ce module ---
def calculer_debit_caquot(C, I_eq, A_ha, M, montana_a, montana_b, verbose=False):
    """
    Calcule le débit de pointe en utilisant la formulation complète de Caquot.
    Les coefficients (u, v, w, etc.) sont dérivés de la formule de Caquot.
    """
    # Conversion du 'a' de Montana de mm/h à mm/min pour la consistance des unités
    montana_a_formin = montana_a / 60
    b = montana_b # L'exposant 'b' reste le même

    # Calcul des exposants u, v, w de la formule de Caquot
    denom = 1 - CAQUOT_F * b
    u = (CAQUOT_C * b) / denom
    v = 1.0 / denom
    w = (CAQUOT_D * b + 1 - CAQUOT_EPSILON) / denom
    
    # Calcul du coefficient d'allongement corrigé
    mu = CAQUOT_MU_C1 * (M ** CAQUOT_MU_C2)
    
    # Calcul du coefficient K' de Caquot
    K_num = montana_a_formin * (mu ** b)
    K_den = CAQUOT_BETA_DELTA
    K_prime = (K_num / K_den)**(1.0 / denom)
    
    # Calcul du débit en mm.ha/min
    Q_mmha_min = K_prime * (I_eq ** u) * (C ** v) * (A_ha ** w)
    
    # Conversion du débit final en m³/s
    Q_final = Q_mmha_min / 600

    if verbose:
        print_colored("\n   -> Calcul du débit (Méthode de Caquot) :", "yellow")
        print("      (Unités internes : i en mm/min, t en min)")
        print(f"      Calcul des exposants : u={u:.3f}, v={v:.3f}, w={w:.3f}")
        print(f"      Calcul de K' : {K_prime:.3f}")
        print(f"      Résultat : Qmax = {Q_final:.3f} m³/s")
    return Q_final

# --- Fonction principale du module (VERSION AMÉLIORÉE) ---
def run_calcul_caquot(troncon, params_pluie: dict, tc_formule_name: str, verbose=False):
    """Exécute le calcul direct de la formule de Caquot pour un seul tronçon."""
    # Si c'est une tête de réseau, on initialise ses caractéristiques cumulées
    if not troncon.longueur_cumulee:
        troncon.longueur_cumulee = troncon.long_parcours_surface_m + troncon.long_troncon_m
        troncon.pentes_parcours = [(troncon.long_parcours_surface_m, troncon.pente_parcours_surface), (troncon.long_troncon_m, troncon.pente_troncon)]

    # Calcul de la pente équivalente (I_eq) du bassin versant
    sum_lj_sqrt_ij = sum(l / math.sqrt(p) for l, p in troncon.pentes_parcours if p > 0)
    pente_eq = (troncon.longueur_cumulee / sum_lj_sqrt_ij)**2 if sum_lj_sqrt_ij > 0 else 0.01
    
    # Calcul de l'allongement (M) du bassin versant
    allongement_M = troncon.longueur_cumulee / math.sqrt(troncon.surface_cumulee * 10000) if troncon.surface_cumulee > 0 else 2.0
    if allongement_M < 0.8: allongement_M = 0.8 # L'allongement est plafonné à 0.8
    
    # ***** Affichage verbeux des résultats intermédiaires *****
    if verbose:
        print_colored("\n   -> Calculs intermédiaires (Caquot) :", "cyan")
        print(f"      1. Pente équivalente (I_eq) = {pente_eq:.4f}")
        print(f"      2. Allongement (M)         = {allongement_M:.3f}")

    # Calcul du débit de pointe
    troncon.q_max_m3s = calculer_debit_caquot(
        troncon.c_moyen_cumule, pente_eq, troncon.surface_cumulee, allongement_M,
        params_pluie['a'], params_pluie['b'], verbose
    )
    
    # Le temps de concentration n'est pas utilisé pour le calcul du débit chez Caquot,
    # mais il est calculé à titre informatif pour le tableau de résultats.
    troncon.tc_final_min = max(troncon.calculer_tc_surface(tc_formule_name), troncon.tc_amont_max)
    
    # Dimensionnement final de la section
    try:
        troncon.resultat_dimensionnement = dimensionner_section(troncon, troncon.q_max_m3s, False)
        # Si le dimensionnement réussit, on met le statut à OK (il sera vérifié plus tard pour la vitesse)
        troncon.statut = 'OK'
    except ValueError as e:
        troncon.statut = str(e) # Ex: "Débit trop élevé..."



# modules/hydrologie/caquot.py
import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.shared_formulas import dimensionner_section
from utils.ui import print_colored

# --- Constantes de la méthode ---
CAQUOT_BETA_DELTA, CAQUOT_EPSILON, CAQUOT_MU_C1, CAQUOT_MU_C2, CAQUOT_C, CAQUOT_D, CAQUOT_F = 1.40, 0.05, 0.19, 0.84, -0.41, 0.507, -0.287

# --- Formule de calcul de débit ---
def calculer_debit_caquot(C, I_eq, A_ha, M, a, b, verbose=False):
    """Calcule le débit de pointe en utilisant la formulation complète de Caquot."""
    montana_a_formin = a / 60
    
    denom = 1 - CAQUOT_F * b
    u = (CAQUOT_C * b) / denom
    v = 1.0 / denom
    w = (CAQUOT_D * b + 1 - CAQUOT_EPSILON) / denom
    
    mu = CAQUOT_MU_C1 * (M ** CAQUOT_MU_C2)
    
    K_num = montana_a_formin * (mu ** b)
    K_den = CAQUOT_BETA_DELTA
    K_prime = (K_num / K_den)**(1.0 / denom)
    
    Q_mmha_min = K_prime * (I_eq ** u) * (C ** v) * (A_ha ** w)
    
    Q_final = Q_mmha_min / 600

    if verbose:
        print_colored("\n   -> Calcul du débit (Méthode de Caquot) :", "yellow")
        print("      (Unités internes : i en mm/min, t en min)")
        print(f"      Calcul des exposants : u={u:.3f}, v={v:.3f}, w={w:.3f}")
        print(f"      Calcul de K' : {K_prime:.3f}")
        print(f"      Résultat : Qmax = {Q_final:.3f} m³/s")
    return Q_final

# --- Fonction principale du module ---
def run_calcul_caquot(troncon, params_pluie: dict, tc_formule_name: str, verbose=False):
    """Exécute le calcul direct de la formule de Caquot pour un seul tronçon."""
    if not troncon.longueur_cumulee:
        troncon.longueur_cumulee = troncon.long_parcours_surface_m + troncon.long_troncon_m
        troncon.pentes_parcours = [(troncon.long_parcours_surface_m, troncon.pente_parcours_surface), (troncon.long_troncon_m, troncon.pente_troncon)]

    sum_lj_sqrt_ij = sum(l / math.sqrt(p) for l, p in troncon.pentes_parcours if p > 0)
    pente_eq = (troncon.longueur_cumulee / sum_lj_sqrt_ij)**2 if sum_lj_sqrt_ij > 0 else 0.01
    
    allongement_M = troncon.longueur_cumulee / math.sqrt(troncon.surface_cumulee * 10000) if troncon.surface_cumulee > 0 else 2.0
    if allongement_M < 0.8: allongement_M = 0.8
    
    if verbose:
        print_colored("\n   -> Calculs intermédiaires (Caquot) :", "cyan")
        print(f"      1. Pente équivalente (I_eq) = {pente_eq:.4f}")
        print(f"      2. Allongement (M)         = {allongement_M:.3f}")

    # ***** CORRECTION : Utilisation des clés 'a' et 'b' *****
    troncon.q_max_m3s = calculer_debit_caquot(
        troncon.c_moyen_cumule, pente_eq, troncon.surface_cumulee, allongement_M,
        params_pluie['a'], params_pluie['b'], verbose
    )
    
    troncon.tc_final_min = max(troncon.calculer_tc_surface(tc_formule_name), troncon.tc_amont_max)
    
    try:
        troncon.resultat_dimensionnement = dimensionner_section(troncon, troncon.q_max_m3s, False)
        troncon.statut = 'OK'
    except ValueError as e:
        troncon.statut = str(e)