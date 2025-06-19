# Fichier: calculs/bois.py (Version Finale Pédagogique)

# -*- coding: utf-8 -*-
import pandas as pd
import os

# --- FONCTION 1 : CHARGEMENT DES DONNÉES ---
def charger_classes_bois():
    """Lit le fichier classes_bois.csv et retourne les données."""
    chemin_script = os.path.dirname(__file__)
    chemin_db = os.path.join(chemin_script, '..', 'db', 'classes_bois.csv')
    try: return pd.read_csv(chemin_db)
    except FileNotFoundError: return None

# --- CONSTANTES EUROCODE 5 ---
K_MOD_TABLE = {
    'permanente': {'classe_1': 0.6, 'classe_2': 0.6, 'classe_3': 0.5},
    'long_terme': {'classe_1': 0.7, 'classe_2': 0.7, 'classe_3': 0.55},
    'moyen_terme': {'classe_1': 0.8, 'classe_2': 0.8, 'classe_3': 0.65},
    'court_terme': {'classe_1': 0.9, 'classe_2': 0.9, 'classe_3': 0.7},
}
K_DEF_TABLE = {'classe_1': 0.6, 'classe_2': 0.8, 'classe_3': 2.0}

# --- FONCTION 2 : VÉRIFICATION D'UNE SECTION BOIS ---
def verifier_section_bois(b, h, longueur, sollicitations, classe_bois, classe_service, duree_charge, verbose=True):
    """Vérifie si une section de bois (b x h) est adéquate."""
    if verbose:
        print(f"\n--- Vérification de la section bois {b}x{h} mm pour L={longueur}m ---")

    df_classes = charger_classes_bois()
    if df_classes is None: return "Erreur de chargement des données bois.", False
    
    props_bois = df_classes[df_classes['Classe'] == classe_bois]
    if props_bois.empty: return f"Erreur: Classe de bois '{classe_bois}' non trouvée.", False
    
    props_bois_dict = props_bois.iloc[0]
    fm_k = props_bois_dict['fm_k_MPa']
    E0_mean_kN_mm2 = props_bois_dict['E0_mean_KN_mm2']
    E0_mean_MPa = E0_mean_kN_mm2 * 1000
    type_bois = props_bois_dict['Type_Bois']
    gamma_M = 1.25 if type_bois == 'Lamellé-collé' else 1.3
    
    try:
        k_mod = K_MOD_TABLE[duree_charge][classe_service]
        k_def = K_DEF_TABLE[classe_service]
    except KeyError: return "Erreur: 'classe_service' ou 'duree_charge' invalide.", False
    
    if verbose:
        print(f"Propriétés: {classe_bois} ({type_bois}), fm,k={fm_k} MPa, E0,mean={E0_mean_MPa} MPa")
        print(f"Coefficients: k_mod={k_mod}, k_def={k_def}, gamma_M={gamma_M}")

    # --- Calculs de résistance et de déformation ---
    f_md = (k_mod * fm_k) / gamma_M
    M_Ed_Nmm = sollicitations['M_Ed'] * 1e6
    W_mm3 = (b * h**2) / 6
    sigma_m_d = M_Ed_Nmm / W_mm3 if W_mm3 > 0 else float('inf')
    resistance_ok = sigma_m_d <= f_md

    charge_ser_N_mm = sollicitations['p_ser'] / 1000
    I_mm4 = (b * h**3) / 12
    fleche_inst_mm = (5 * charge_ser_N_mm * (longueur * 1000)**4) / (384 * E0_mean_MPa * I_mm4) if I_mm4 > 0 else float('inf')
    fleche_fin_mm = fleche_inst_mm * (1 + k_def)
    fleche_admissible_mm = (longueur * 1000) / 300
    fleche_ok = fleche_fin_mm <= fleche_admissible_mm

    if verbose:
        print("\n1. Vérification de la résistance en flexion (ELU):")
        print("   Formule (Résistance): f_md = (k_mod * fm_k) / gamma_M")
        print(f"   Remplacement: f_md = ({k_mod} * {fm_k}) / {gamma_M} = {f_md:.2f} MPa")
        print("\n   Formule (Contrainte): sigma_m_d = M_Ed / W")
        print(f"   Remplacement: sigma_m_d = {M_Ed_Nmm:.0f} / {W_mm3:.0f} = {sigma_m_d:.2f} MPa")
        print(f"   Condition: {sigma_m_d:.2f} MPa <= {f_md:.2f} MPa ? -> {'OK' if resistance_ok else 'INSUFFISANTE'}")

        print("\n2. Vérification de la flèche (ELS):")
        print("   Formule (Flèche finale): f_fin = f_inst * (1 + k_def)")
        print(f"   Calcul: f_fin = {fleche_inst_mm:.2f} * (1 + {k_def}) = {fleche_fin_mm:.2f} mm")
        print("\n   Formule (Flèche admissible): f_adm = L / 300")
        print(f"   Calcul: f_adm = {longueur*1000:.0f} / 300 = {fleche_admissible_mm:.2f} mm")
        print(f"   Condition: {fleche_fin_mm:.2f} mm <= {fleche_admissible_mm:.2f} mm ? -> {'OK' if fleche_ok else 'INACCEPTABLE'}")
    
    est_valide = resistance_ok and fleche_ok
    message = "La section est conforme." if est_valide else "La section n'est pas conforme."
    
    return message, est_valide

#---------------------------------------------------------------------------


# --- FONCTION 3 : VÉRIFICATION D'UNE BARRE EN TRACTION AXIALE ---
def verifier_traction_bois(b, h, effort_N_daN, classe_bois, classe_service, duree_charge, verbose=True):
    """
    Vérifie si une section de bois (b x h) est adéquate pour un effort de traction axiale.
    
    Args:
        effort_N_daN (float): L'effort de traction normal en daN.
    """
    if verbose:
        print(f"\n--- Vérification en TRACTION de la section bois {b}x{h} mm ---")
        print(f"Effort de traction appliqué N_Ed = {effort_N_daN} daN")

    # --- Étape 1: Récupérer les propriétés du matériau ---
    df_classes = charger_classes_bois()
    if df_classes is None: return "Erreur de chargement des données bois.", False
    
    props_bois = df_classes[df_classes['Classe'] == classe_bois]
    if props_bois.empty: return f"Erreur: Classe de bois '{classe_bois}' non trouvée.", False
    
    props_bois_dict = props_bois.iloc[0]
    # On récupère la résistance à la TRACTION (ft_0_k_MPa) depuis notre nouveau CSV
    ft_0_k = props_bois_dict['ft_0_k_MPa']
    type_bois = props_bois_dict['Type_Bois']
    gamma_M = 1.25 if type_bois == 'Lamellé-collé' else 1.3
    
    # --- Étape 2: Récupérer les coefficients Eurocode ---
    try:
        k_mod = K_MOD_TABLE[duree_charge][classe_service]
    except KeyError: return "Erreur: 'classe_service' ou 'duree_charge' invalide.", False
    
    if verbose:
        print(f"Propriétés: {classe_bois} ({type_bois}), ft,0,k={ft_0_k} MPa")
        print(f"Coefficients: k_mod={k_mod}, gamma_M={gamma_M}")

    # --- Étape 3: Vérification de la résistance en traction (ELU) ---
    # Résistance de calcul en traction
    f_t0_d = (k_mod * ft_0_k) / gamma_M

    # Contrainte de traction appliquée
    effort_N_Newton = effort_N_daN * 10 # Conversion daN -> N
    aire_section_mm2 = b * h
    sigma_t0_d = effort_N_Newton / aire_section_mm2 if aire_section_mm2 > 0 else float('inf')
    
    resistance_ok = sigma_t0_d <= f_t0_d

    if verbose:
        print("\n1. Vérification de la résistance en traction (ELU):")
        print("   Formule (Résistance): f_t,0,d = (k_mod * ft_0_k) / gamma_M")
        print(f"   Remplacement: f_t,0,d = ({k_mod} * {ft_0_k}) / {gamma_M} = {f_t0_d:.2f} MPa")
        print("\n   Formule (Contrainte): sigma_t,0,d = N_Ed / A")
        print(f"   Remplacement: sigma_t,0,d = {effort_N_Newton:.0f} / {aire_section_mm2:.0f} = {sigma_t0_d:.2f} MPa")
        print(f"   Condition: {sigma_t0_d:.2f} MPa <= {f_t0_d:.2f} MPa ? -> {'OK' if resistance_ok else 'INSUFFISANTE'}")

    message = "La section est conforme en traction." if resistance_ok else "La section n'est pas conforme en traction."
    
    return message, resistance_ok