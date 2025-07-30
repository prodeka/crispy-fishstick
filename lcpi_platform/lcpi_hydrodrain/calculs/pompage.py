import math

def predimensionner_pompe(donnees: dict) -> dict:
    # Phase 2 : Calcul HMT
    q_pompage = donnees.get("debit_pompage_m3s")
    z_ref = donnees.get("cote_refoulement_m")
    z_asp_min = donnees.get("cote_aspiration_min_m")
    longueur_conduite = donnees.get("longueur_conduite_m")
    diametre_conduite = donnees.get("diametre_conduite_m")
    somme_k_singuliers = sum(donnees.get("pertes_singulieres_k", []))
    
    h_geo = z_ref - z_asp_min
    aire_conduite = math.pi * (diametre_conduite**2) / 4
    vitesse = q_pompage / aire_conduite
    
    # Pertes de charge linéaires (Darcy-Weisbach avec lambda simplifié)
    lambda_colebrook = 0.02 # Placeholder
    pertes_lineaires = lambda_colebrook * (longueur_conduite / diametre_conduite) * (vitesse**2 / (2 * 9.81))
    pertes_singulieres = somme_k_singuliers * (vitesse**2 / (2 * 9.81))
    h_pertes = pertes_lineaires + pertes_singulieres
    hmt = h_geo + h_pertes
    
    # Phase 3 : Puissance
    p_hydraulique_watt = q_pompage * 1000 * 9.81 * hmt
    p_elec_watt = p_hydraulique_watt / (0.75 * 0.90) # rendements pompe/moteur
    
    return {
        "statut": "OK",
        "point_fonctionnement": {
            "debit_m3s": q_pompage,
            "hmt_m": round(hmt, 2)
        },
        "puissance_electrique_requise_kW": round(p_elec_watt / 1000, 2)
    }
