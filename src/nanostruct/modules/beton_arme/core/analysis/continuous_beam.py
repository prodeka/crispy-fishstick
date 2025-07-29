# PROJET_DIMENTIONEMENT/BA/core/analysis/continuous_beam.py
# Moteur de calcul pour l'analyse d'une poutre continue par la méthode forfaitaire.

from nanostruct.utils.ui_helpers import v_print


def analyze_by_forfaitaire(spans, load_wu):
    """
    Calcule les moments sur appuis et en travée pour une poutre continue,
    en utilisant une version améliorée et plus juste de la méthode forfaitaire.

    Args:
        spans (list): Une liste des longueurs des travées [L1, L2, L3, ...].
        load_wu (float): La charge linéique ultime (w_u) en kN/m.

    Returns:
        dict: Dictionnaire avec la liste des moments sur appuis et en travées (en kNm).
    """
    num_spans = len(spans)
    if num_spans == 0:
        return {"appuis": [], "travees": []}

    # 1. Calcul des moments isostatiques de référence (M0) pour chaque travée
    moments_M0 = [load_wu * L**2 / 8 for L in spans]

    # 2. Calcul des moments sur appuis (valeurs négatives)
    moments_appui = [0] * (num_spans + 1)  # Les appuis de rive ont un moment nul

    # Cas d'une poutre à 2 travées
    if num_spans == 2:
        # L'appui central unique est le plus chargé
        moments_appui[1] = -0.6 * (moments_M0[0] + moments_M0[1]) / 2

    # Cas d'une poutre à plus de 2 travées
    elif num_spans > 2:
        # Premiers appuis intermédiaires adjacents aux rives
        moments_appui[1] = -0.5 * (moments_M0[0] + moments_M0[1])
        moments_appui[-2] = -0.5 * (moments_M0[-2] + moments_M0[-1])

        # Autres appuis intermédiaires
        for i in range(2, num_spans - 1):
            moments_appui[i] = -0.4 * (moments_M0[i - 1] + moments_M0[i])

    # 3. Calcul des moments en travée (valeurs positives)
    moments_travee = [0] * num_spans
    for i in range(num_spans):
        M0 = moments_M0[i]
        # Moments aux appuis de la travée i
        Ma = moments_appui[i]
        Mb = moments_appui[i + 1]

        # Coefficient majorateur pour les travées de rive (Q > 1.2G, charges variables, etc.)
        # C'est une simplification, une analyse plus fine serait nécessaire pour Q et G.
        coeff_trav = 1.15 if num_spans > 1 and (i == 0 or i == num_spans - 1) else 1.05

        # Le moment en travée est réduit par une fraction des moments aux appuis
        # Formule approchée BAEL
        Mt = coeff_trav * M0 + 0.3 * (Ma + Mb)

        # Le moment en travée ne peut être inférieur à celui d'une travée isostatique simple
        moments_travee[i] = max(Mt, 1.05 * M0)

    # Affichage détaillé si verbose
    v_print(
        "Moments sur appuis (kNm)",
        "[M_A, M_B, ...]",
        ", ".join([f"{m:.2f}" for m in moments_appui]),
        f"Min: {min(moments_appui):.2f}",
    )
    v_print(
        "Moments en travée (kNm)",
        "[M_AB, M_BC, ...]",
        ", ".join([f"{m:.2f}" for m in moments_travee]),
        f"Max: {max(moments_travee):.2f}",
    )

    return {"appuis": moments_appui, "travees": moments_travee}
