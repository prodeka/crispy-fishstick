# PROJET_DIMENTIONEMENT/BA/core/design/raft_foundation_design.py

import pandas as pd
from utils.ui_helpers import v_print

def design_raft_by_strip_method(poteaux_df, A, B, h, sigma_sol_adm, beton, acier):
    """
    Dimensionne un radier par la méthode des bandes.
    poteaux_df: DataFrame pandas avec les données des poteaux.
    A, B, h: Dimensions du radier en mètres.
    """
    
    # --- Étape 1: Vérification géométrique et contrainte au sol ---
    
    # Calcul des charges de service et ultimes
    poteaux_df['P_ser'] = poteaux_df['Charge_G_MN'] + poteaux_df['Charge_Q_MN']
    poteaux_df['P_ui'] = 1.35 * poteaux_df['Charge_G_MN'] + 1.5 * poteaux_df['Charge_Q_MN']
    
    # Centre de gravité des charges
    sum_P_ser = poteaux_df['P_ser'].sum()
    Gx = (poteaux_df['coord_x_m'] * poteaux_df['P_ser']).sum() / sum_P_ser
    Gy = (poteaux_df['coord_y_m'] * poteaux_df['P_ser']).sum() / sum_P_ser
    v_print("Centre de gravité charges", "(Gx, Gy)", f"({Gx:.2f}m, {Gy:.2f}m)", "OK")
    v_print("Centre de gravité radier", "(A/2, B/2)", f"({A/2:.2f}m, {B/2:.2f}m)", "À comparer")
    
    # Contrainte de service sous le radier
    q_sol_ser = sum_P_ser / (A * B) # en MPa (car MN/m²)
    v_print("Contrainte sur le sol", "q_sol = ΣP_ser / S", f"{sum_P_ser:.2f} / {A*B:.2f}", q_sol_ser, "MPa")
    
    if q_sol_ser > sigma_sol_adm:
        return {"status": "ERREUR", "message": f"Contrainte au sol ({q_sol_ser:.3f} MPa) dépasse l'admissible ({sigma_sol_adm:.3f} MPa)."}

    # --- Étape 2: Calcul par la méthode des bandes ---
    # Pour cet exemple, nous allons analyser une bande principale dans le sens X.
    # On imagine une bande de 1m de large.
    
    # Réaction du sol (charge inversée) ultime par mètre de bande
    q_radier_ultime_par_m = (poteaux_df['P_ui'].sum() / (A * B)) * 1.0 # Pression * 1m de large
    
    # Simplification : on considère la bande la plus chargée (autour de x=7m)
    poteaux_bande_centrale = poteaux_df[poteaux_df['coord_x_m'] == 7.0]
    
    # C'est un problème de poutre continue sur 3 appuis (P4, P5, P6) avec une charge q inversée.
    # Les moments sur appuis sont plus élevés. Un calcul simplifié donne : M_appui ≈ q*L²/10
    L_moyenne = 6.0 # (11-1)/2, portée moyenne entre poteaux
    M_appui_ultime_MNm = (q_radier_ultime_par_m * L_moyenne**2) / 10
    
    # Moment en travée : M_travee ≈ q*L²/14
    M_travee_ultime_MNm = (q_radier_ultime_par_m * L_moyenne**2) / 14

    v_print("Moment sur appui (bande X)", "M_appui ≈ qL²/10", "...", M_appui_ultime_MNm, "MN.m/m")
    v_print("Moment en travée (bande X)", "M_travée ≈ qL²/14", "...", M_travee_ultime_MNm, "MN.m/m")

    # --- Étape 3: Calcul du ferraillage ---
    d = h - 0.07 # Hauteur utile
    f_su = acier.fe / acier.gamma_s
    
    # Aciers supérieurs (sur appuis)
    As_sup_m2_par_m = M_appui_ultime_MNm / (0.9 * d * f_su)
    # Aciers inférieurs (en travée)
    As_inf_m2_par_m = M_travee_ultime_MNm / (0.9 * d * f_su)
    
    As_sup_cm2_par_m = As_sup_m2_par_m * 10000
    As_inf_cm2_par_m = As_inf_cm2_par_m * 10000

    return {
        "status": "OK",
        "As_sup_X_cm2_per_m": As_sup_cm2_par_m,
        "As_inf_X_cm2_per_m": As_inf_cm2_par_m,
        "message": "Calcul pour la bande principale en X. Le calcul en Y est à faire séparément."
    }