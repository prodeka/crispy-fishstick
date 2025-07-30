# modules/hydrologie/rationnelle.py
import math


from ...core.shared_formulas import dimensionner_section
from ...utils.ui import print_colored
from .idf_formulas import (
    calculer_intensite_pluie,
)

# --- Constantes du module ---
MAX_ITERATIONS = 15
TOLERANCE_TC_min = 0.1
TC_MINIMUM_MIN = 5.0


# --- Fonctions de calcul ---
def calculer_q_max_rationnelle(c, i_mmh, a_ha, verbose=False):
    """Calcule le débit de pointe avec la formule Rationnelle : Q = C*i*A / 360."""
    if verbose:
        print_colored("\n   -> Calcul du débit (Méthode Rationnelle) :", "yellow")
        print("      Formule : Qmax = (C*i*A)/360")
        print(f"      AN : Qmax = ({c:.2f} * {i_mmh:.2f} * {a_ha:.2f}) / 360")
    q_max = (c * i_mmh * a_ha) / 360
    if verbose:
        print(f"      Résultat : Qmax = {q_max:.3f} m³/s")
    return q_max


# --- Fonction principale du workflow Rationnel (VERSION FINALE STABILISÉE) ---
def run_calcul_rationnelle(
    troncon, params_pluie: dict, tc_formule_name: str, verbose=False
):
    """Exécute le calcul itératif complet de la méthode Rationnelle pour un tronçon."""

    # 1. Initialisation du temps de concentration
    tc_surface = troncon.calculer_tc_surface(tc_formule_name)
    tc_amont = troncon.tc_amont_max
    tc_iteration = max(tc_surface, tc_amont, TC_MINIMUM_MIN)

    # 2. Boucle itérative pour la convergence
    for it_num in range(MAX_ITERATIONS):
        if verbose:
            print_colored(
                f"\n--- Itération n°{it_num + 1} (tc = {tc_iteration:.2f} min) ---",
                "bold",
            )

        # Calcul de l'intensité et du débit
        intensite = calculer_intensite_pluie(tc_iteration, params_pluie, verbose)
        troncon.q_max_m3s = calculer_q_max_rationnelle(
            troncon.c_moyen_cumule, intensite, troncon.surface_cumulee, verbose
        )

        # Tentative de dimensionnement
        try:
            resultat_dim_iter = dimensionner_section(
                troncon, troncon.q_max_m3s, verbose
            )
            troncon.resultat_dimensionnement = resultat_dim_iter
            troncon.statut = "OK"
        except ValueError as e:
            # ***** CORRECTION CLÉ : Gestion d'échec robuste *****
            # Si le dimensionnement échoue, on enregistre l'erreur et le dernier Tc utilisé
            troncon.statut = str(e)
            troncon.tc_final_min = tc_iteration  # On transmet une valeur réaliste
            if verbose:
                print_colored(f"\n   -> {troncon.statut}", "red", bold=True)
            return  # Arrêt du calcul pour ce tronçon

        # 3. Calcul du nouveau temps de concentration
        vitesse = resultat_dim_iter.get("vitesse_ms", 0)
        temps_parcours = (
            (troncon.long_troncon_m / vitesse) / 60 if vitesse > 0 else float("inf")
        )
        tc_calcule_nouveau = tc_amont + temps_parcours

        # 4. Vérification de la convergence
        if (
            not math.isinf(tc_calcule_nouveau)
            and abs(tc_calcule_nouveau - tc_iteration) < TOLERANCE_TC_min
        ):
            troncon.tc_final_min = max(tc_calcule_nouveau, TC_MINIMUM_MIN)
            if verbose:
                print_colored("\n>>> CONVERGENCE ATTEINTE !", "green")
            return

        # 5. Préparation de la prochaine itération
        tc_iteration_precedent = tc_iteration
        tc_iteration = max(tc_calcule_nouveau, TC_MINIMUM_MIN)

        if abs(tc_iteration - tc_iteration_precedent) < 1e-6:
            troncon.tc_final_min = tc_iteration
            if verbose:
                print_colored(
                    "\n>>> CONVERGENCE ATTEINTE (valeur plancher stable) !", "green"
                )
            return

    # Si on sort de la boucle, la convergence n'est pas atteinte
    troncon.tc_final_min = tc_iteration
    troncon.statut = "Non-convergence"
    if verbose:
        print_colored(
            "\n>>> ATTENTION: Convergence non atteinte après le nombre maximal d'itérations.",
            "red",
        )
