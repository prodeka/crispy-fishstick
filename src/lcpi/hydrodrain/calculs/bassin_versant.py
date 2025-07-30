import math

def caracteriser_bassin(donnees_bassin: dict):
    s_km2 = donnees_bassin.get("superficie_km2")
    p_km = donnees_bassin.get("perimetre_km")
    ig_m_km = donnees_bassin.get("pente_globale_m_km")
    
    kc = 0.282 * p_km * (s_km2**-0.5)
    
    ratio_l = (kc / 1.128) * (1 + math.sqrt(1 - (1.128 / kc)**2))
    longueur_l = math.sqrt(s_km2) * ratio_l
    
    ds = ig_m_km * math.sqrt(s_km2)

    return {
        "statut": "OK",
        "superficie_km2": s_km2, "perimetre_km": p_km,
        "indice_gravelius_kc": round(kc, 2),
        "longueur_rectangle_equivalent_km": round(longueur_l, 2),
        "denivelee_specifique_m": round(ds, 2)
    }
