import math

def dimensionner_troncon_assainissement(donnees: dict) -> dict:
    q_projet = donnees.get("debit_projet_m3s")
    pente_j = donnees.get("pente_m_m")
    k_strickler = donnees.get("k_strickler")
    diametre_initial_m = donnees.get("diametre_initial_m")

    # Logique itérative simplifiée pour trouver le bon diamètre
    d = diametre_initial_m
    while True:
        aire_ps = math.pi * d**2 / 4
        rh_ps = d / 4
        q_ps = k_strickler * aire_ps * (rh_ps**(2/3)) * (pente_j**0.5)
        v_ps = q_ps / aire_ps

        if v_ps < 0.6: return {"statut": "Erreur", "message": f"Vitesse trop faible ({v_ps:.2f} m/s) pour D={d*1000}mm. Augmenter la pente."}
        if v_ps > 4.0: return {"statut": "Erreur", "message": f"Vitesse trop forte ({v_ps:.2f} m/s) pour D={d*1000}mm. Réduire la pente."}
        if q_projet > q_ps:
            # Placeholder: passer au diamètre commercial supérieur
            d += 0.100 
            if d > 2.0: return {"statut": "Erreur", "message": "Diamètre requis trop grand."}
            continue

        # Calcul du taux de remplissage (simplifié, un abaque serait plus précis)
        ratio_q = q_projet / q_ps
        h_sur_d = 0.5 * (1 - math.cos(math.acos(1 - 2 * ratio_q**(1/0.75)))) if ratio_q < 1 else 1
        
        if h_sur_d > 0.8:
            d += 0.100
            continue
        
        return {
            "statut": "OK", "diametre_requis_mm": d * 1000,
            "vitesse_pleine_section_ms": round(v_ps, 2), "debit_pleine_section_m3s": round(q_ps, 3),
            "taux_remplissage_h_d": round(h_sur_d, 2)
        }
