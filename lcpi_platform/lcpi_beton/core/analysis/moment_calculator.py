# PROJET_DIMENTIONEMENT/BA/core/analysis/moment_calculator.py
# Moteur de calcul pour les moments, avec affichage pédagogique intégré.

from lcpi_platform.lcpi_core.utils.ui_helpers import v_print


def get_isostatic_moment(charge_q_kNm, span_L_m):
    """
    Calcule le moment isostatique maximal de référence M0 = qL²/8
    et affiche le détail du calcul.
    """
    M0 = (charge_q_kNm * span_L_m**2) / 8
    v_print(
        label="Moment isostatique de référence (M0)",
        formula="M0 = q * L² / 8",
        numeric_app=f"{charge_q_kNm:.2f} * {span_L_m:.2f}² / 8",
        result=M0,
        unit="kNm",
    )
    return M0


def calculate_beam_end_moment(charge_q_kNm, span_L_m, is_end_span=True):
    """
    Estime le moment d'appui d'une poutre continue par la méthode forfaitaire
    et affiche le détail du calcul.
    """
    # Cette fonction appelle d'abord get_isostatic_moment qui affichera son propre détail.
    M0 = get_isostatic_moment(charge_q_kNm, span_L_m)

    # Choix du coefficient et de la formule en fonction de la position de la travée
    if is_end_span:
        coeff = 0.4
        formula = "Mu,appui = 0.4 * M0 (appui de rive)"
    else:
        coeff = 0.5
        formula = "Mu,appui = 0.5 * M0 (appui intermédiaire)"

    moment_kNm = coeff * M0

    v_print(
        label="Moment d'appui forfaitaire",
        formula=formula,
        numeric_app=f"{coeff:.1f} * {M0:.2f}",
        result=moment_kNm,
        unit="kNm",
    )

    # On retourne la valeur en MN.m pour qu'elle soit directement utilisable
    return moment_kNm / 1000
