import math

def dimensionner_canal(donnees: dict) -> dict:
    # Implémentation de la Phase 2 du guide
    q_projet = donnees.get("debit_projet_m3s")
    pente_j = donnees.get("pente_m_m")
    k_strickler = donnees.get("k_strickler")
    fruit_m = donnees.get("fruit_talus_m_m")
    vitesse_imposee = donnees.get("vitesse_imposee_ms")

    # Approche A : Vitesse Imposée
    if not vitesse_imposee:
        return {"statut": "Erreur", "message": "L'approche par vitesse imposée est la seule implémentée."}
    
    aire_s = q_projet / vitesse_imposee
    rayon_h = (vitesse_imposee / (k_strickler * (pente_j**0.5)))**1.5
    perimetre_p = aire_s / rayon_h
    
    # Résolution du système pour h et b (simplifié, non-itératif pour ce placeholder)
    # S = h*(b+mh) => b = S/h - mh
    # P = b + 2h*sqrt(1+m²) => P = S/h - mh + 2h*sqrt(1+m²)
    # Pour ce placeholder, nous donnons une solution directe approximative
    h = math.sqrt(aire_s / (2 * math.sqrt(1 + fruit_m**2) - fruit_m))
    b = aire_s / h - fruit_m * h
    
    # Phase 3 : Vérifications
    largeur_miroir = b + 2 * fruit_m * h
    froude = vitesse_imposee / (math.sqrt(9.81 * (aire_s / largeur_miroir)))
    
    return {
        "statut": "OK",
        "hauteur_eau_h_m": round(h, 3),
        "largeur_fond_b_m": round(b, 3),
        "vitesse_ecoulement_ms": round(vitesse_imposee, 2),
        "nombre_froude": round(froude, 2),
        "regime": "Fluvial" if froude < 1 else "Torrentiel"
    }
