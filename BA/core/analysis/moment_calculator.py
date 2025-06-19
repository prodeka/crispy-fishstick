from utils.ui_helpers import v_print

# Fichier pour les calculs de RDM simplifiés

def get_isostatic_moment(charge_q_kNm, span_L_m):
    """Calcule le moment isostatique maximal M0 = qL²/8."""
    return (charge_q_kNm * span_L_m**2) / 8


def calculate_beam_end_moment(charge_q_kNm, span_L_m, is_end_span=True):
    """
    Estime le moment d'appui d'une poutre continue (méthode forfaitaire simplifiée).
    """
    M0 = (charge_q_kNm * span_L_m**2) / 8
    v_print("Moment isostatique (M0)", "M0 = q*L²/8", f"{charge_q_kNm:.2f}*{span_L_m:.2f}²/8", M0, "kNm")

    coeff = 0.4 if is_end_span else 0.5
    formula = "Mu = 0.4 * M0" if is_end_span else "Mu = 0.5 * M0"
    
    moment_kNm = coeff * M0
    v_print("Moment d'appui (Mu)", formula, f"{coeff:.1f} * {M0:.2f}", moment_kNm, "kNm")
    
    return moment_kNm / 1000 # Conversion en MN.m