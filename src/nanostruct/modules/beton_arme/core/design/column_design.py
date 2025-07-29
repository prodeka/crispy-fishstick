# PROJET_DIMENTIONEMENT/BA/core/design/column_design.py
# Contient les moteurs de calcul pour le dimensionnement des poteaux.

import math
from nanostruct.utils.ui_helpers import v_print
from nanostruct.modules.beton_arme.core.rebar_selector import get_rebar_proposals


# ==============================================================================
# MÉTHODE 1 : FLEXION COMPOSÉE (GÉNÉRALE)
# ==============================================================================
def design_rectangular_column(Nu, Mu, height, k_factor, section, beton, acier):
    """
    Calcule la section d'acier requise par la méthode de la Flexion Composée.
    Retourne un dictionnaire de résultats standardisé.
    """
    b, h = section.b, section.h
    d, d_prime = 0.9 * h, h - (0.9 * h)

    v_print(
        label="Données d'entrée",
        formula="[Nu, Mu, b, h, L, k]",
        numeric_app=f"[{Nu} MN, {Mu:.4f} MN.m, {b}m, {h}m, k={k_factor}]",
        result="OK",
    )

    # --- Calcul de l'élancement et des effets du second ordre ---
    Lf = k_factor * height
    A = b * h
    I_min = min(b * h**3, h * b**3) / 12
    i = math.sqrt(I_min / A)
    elancement_lambda = Lf / i if i > 0 else 0
    v_print(
        "Élancement mécanique", "λ = lf / i", f"{Lf:.2f} / {i:.4f}", elancement_lambda
    )

    alpha = 1.0
    if elancement_lambda > 50:
        alpha = 1 / (1 - (elancement_lambda / 35) ** 2 / 5)
        v_print("Statut poteau", "λ > 50", f"{elancement_lambda:.2f} > 50", "Élancé")
    else:
        v_print(
            "Statut poteau", "λ <= 50", f"{elancement_lambda:.2f} <= 50", "Non-élancé"
        )

    Mu_calcul_Nm = alpha * (Mu * 1e6)
    v_print(
        "Moment de calcul",
        "Mu,cal = α * Mu",
        f"{alpha:.3f} * {Mu:.4f}",
        Mu_calcul_Nm / 1e6,
        "MN.m",
    )

    # --- Calcul de la section d'acier théorique ---
    if Nu == 0:
        return {"status": "ERREUR", "message": "Effort normal nul."}
    e_calcul = Mu_calcul_Nm / (Nu * 1e6)
    Ma_Nm = (Nu * 1e6) * (e_calcul + d - h / 2)
    f_su = acier.fe / acier.gamma_s
    z = d - d_prime
    A_requise_m2 = Ma_Nm / (z * f_su * 1e6)
    A_requise_cm2 = A_requise_m2 * 10000
    v_print(
        "Section d'acier théorique",
        "As = Ma / (z*fsu)",
        f"{Ma_Nm / 1e6:.4f} / ({z:.3f} * {f_su:.2f})",
        A_requise_cm2,
        "cm²",
    )

    # --- Vérifications réglementaires ---
    A_min_cm2 = max(4.0, 0.002 * (A * 10000))
    B_m2 = b * h
    A_max_cm2 = 0.05 * (B_m2 * 10000)
    A_finale_cm2 = max(A_requise_cm2, A_min_cm2)
    v_print(
        "Section d'acier finale",
        "max(As, Amin)",
        f"max({A_requise_cm2:.2f}, {A_min_cm2:.2f})",
        A_finale_cm2,
        "cm²",
    )

    status = "OK"
    message = ""
    if A_finale_cm2 > A_max_cm2:
        status = "ERREUR"
        message = f"Section d'acier ({A_finale_cm2:.2f} cm²) dépasse le maximum ({A_max_cm2:.2f} cm²)."

    # On génère les propositions
    proposals = get_rebar_proposals(A_finale_cm2)

    return {
        "status": status,
        "message": message,
        "section": section,
        "height_L_m": height,
        "enrobage_cm": 3,
        "required_longitudinal_steel_cm2": A_finale_cm2,
        "proposals": proposals,
    }


# ==============================================================================
# MÉTHODE 2 : COMPRESSION "CENTRÉE" (BAEL 91)
# ==============================================================================
def design_column_compression_bael(Nu, height, k_factor, section, beton, acier):
    """
    Calcule la section d'acier requise par la méthode simplifiée du BAEL 91.
    Retourne un dictionnaire de résultats standardisé.
    """
    b, h = section.b, section.h
    a = min(b, h)
    v_print(
        "Données initiales",
        "[Nu, L, k]",
        f"[{Nu} MN, {height:.2f}m, k={k_factor:.2f}]",
        "OK",
    )

    # --- Calcul de l'élancement et du coefficient alpha ---
    lf = k_factor * height
    i = a / math.sqrt(12)
    elancement_lambda = lf / i if i > 0 else 0
    v_print(
        "Élancement mécanique", "λ = lf / i", f"{lf:.2f} / {i:.3f}", elancement_lambda
    )

    alpha = 0.0
    if elancement_lambda <= 50:
        alpha = 0.85 / (1 + 0.2 * (elancement_lambda / 35) ** 2)
        v_print(
            "Coefficient alpha (λ<=50)",
            "α = 0.85/(1+0.2(λ/35)²)",
            f"f(λ={elancement_lambda:.2f})",
            alpha,
        )
    elif 50 < elancement_lambda <= 70:
        alpha = 0.60 * (50 / elancement_lambda) ** 2
        v_print(
            "Coefficient alpha (λ>50)",
            "α = 0.60 * (50/λ)²",
            f"f(λ={elancement_lambda:.2f})",
            alpha,
        )
    else:
        return {
            "status": "ERREUR",
            "message": f"Élancement λ={elancement_lambda:.1f} > 70. Méthode non applicable.",
        }

    # --- Calcul de la section d'acier théorique ---
    Br_m2 = (a - 0.02) * (max(b, h) - 0.02)
    fc28, fe = beton.fc28, acier.fe
    gamma_b, gamma_s = beton.gamma_b, acier.gamma_s
    beton_res_MN = (Br_m2 * fc28) / (0.9 * gamma_b)

    A_requise_cm2 = 0.0
    if (Nu / alpha) > beton_res_MN:
        term1 = (Nu / alpha) - beton_res_MN
        A_requise_m2 = term1 * (gamma_s / fe)
        A_requise_cm2 = A_requise_m2 * 10000
    v_print(
        "Section d'acier (calcul)",
        "As = [(Nu/α)-Res_beton]*γs/fe",
        "...",
        A_requise_cm2,
        "cm²",
    )

    # --- Vérifications réglementaires ---
    B_m2 = b * h
    A_min_cm2 = max(4 * (2 * (b + h)), (0.2 / 100) * (B_m2 * 10000))
    v_print(
        "Acier minimal (Amin)",
        "max(4*P, 0.2%*B)",
        f"max({4 * (2 * (b + h)):.2f}, {(0.2 / 100) * (B_m2 * 10000):.2f})",
        A_min_cm2,
        "cm²",
    )

    A_finale_cm2 = max(A_requise_cm2, A_min_cm2)
    B_m2 = b * h
    A_max_cm2 = (5 / 100) * (B_m2 * 10000)
    status = "OK"
    message = ""
    if A_finale_cm2 > A_max_cm2:
        status = "ERREUR"
        message = f"Section d'acier ({A_finale_cm2:.2f} cm²) dépasse le maximum ({A_max_cm2:.2f} cm²)."

    proposals = get_rebar_proposals(A_finale_cm2)

    return {
        "status": status,
        "message": message,
        "section": section,
        "height_L_m": height,
        "enrobage_cm": 3,
        "required_longitudinal_steel_cm2": A_finale_cm2,
        "proposals": proposals,
    }
