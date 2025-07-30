import math

def _solve_colebrook(re, epsilon_d):
    # Résolution itérative de l'équation de Colebrook-White
    lambda_val = 0.02
    for _ in range(10): # 10 itérations suffisent généralement
        lambda_val = 1 / (-2 * math.log10( (epsilon_d / 3.7) + (2.51 / (re * math.sqrt(lambda_val))) ))**2
    return lambda_val

def predimensionner_pompe(donnees: dict):
    q_pompage = donnees.get("debit_pompage_m3s")
    z_ref = donnees.get("cote_refoulement_m"); z_arret = donnees.get("cote_arret_pompe_m")
    longueur = donnees.get("longueur_conduite_m"); diametre = donnees.get("diametre_conduite_m")
    somme_k = sum(donnees.get("pertes_singulieres_k", [])); rugosite_eps = donnees.get("rugosite_mm", 0.1)
    
    h_geo = z_ref - z_arret
    aire = math.pi * (diametre**2) / 4
    vitesse = q_pompage / aire
    
    # Calcul de Lambda de Colebrook
    viscosite_nu = 1.004e-6 # m²/s pour l'eau à 20°C
    reynolds = (vitesse * diametre) / viscosite_nu
    epsilon_d = (rugosite_eps / 1000) / diametre
    lambda_colebrook = _solve_colebrook(reynolds, epsilon_d)
    
    pertes_lineaires = lambda_colebrook * (longueur / diametre) * (vitesse**2 / (2 * 9.81))
    pertes_singulieres = somme_k * (vitesse**2 / (2 * 9.81))
    h_pertes = pertes_lineaires + pertes_singulieres
    hmt = h_geo + h_pertes
    
    p_hydraulique = q_pompage * 1000 * 9.81 * hmt
    p_elec = p_hydraulique / (0.75 * 0.90)
    
    return {
        "statut": "OK",
        "point_fonctionnement": {"debit_m3s": q_pompage, "hmt_m": round(hmt, 2)},
        "puissance_electrique_requise_kW": round(p_elec / 1000, 2),
        "lambda_colebrook_calcule": round(lambda_colebrook, 4)
    }

def verifier_npsh(donnees: dict) -> dict:
    # Phase 2 : Calcul NPSH disponible
    p_atm_pa = 101325
    rho_eau = 1000
    g = 9.81
    
    # Tension de vapeur de l'eau (formule simplifiée)
    temp_c = donnees.get("temperature_eau_c", 20)
    pv_pa = 610.78 * math.exp((temp_c * 17.27) / (temp_c + 237.3))
    
    h_v = pv_pa / (rho_eau * g)
    h_atm = p_atm_pa / (rho_eau * g)
    
    z_asp = donnees.get("cote_aspiration_min_m")
    
    # Pertes de charge à l'aspiration
    q_pompage = donnees.get("debit_pompage_m3s")
    d_asp = donnees.get("diametre_conduite_aspiration_m")
    l_asp = donnees.get("longueur_conduite_aspiration_m")
    k_asp = 10.5 # K total simplifié pour aspiration
    
    v_asp = q_pompage / (math.pi * (d_asp**2) / 4)
    pertes_asp = (0.02 * (l_asp / d_asp) + k_asp) * (v_asp**2 / (2*g))
    
    npsh_disponible = h_atm - h_v - z_asp - pertes_asp
    
    # Phase 3 : Vérification
    npsh_requis = donnees.get("npsh_requis_m")
    marge = npsh_disponible - npsh_requis
    
    return {
        "statut": "OK",
        "npsh_disponible_m": round(npsh_disponible, 2),
        "npsh_requis_m": npsh_requis,
        "marge_securite_m": round(marge, 2),
        "conforme": marge > 0.5 # Marge de sécurité de 0.5m
    }
