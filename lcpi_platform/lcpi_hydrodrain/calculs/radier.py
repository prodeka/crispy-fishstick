import math

def dimensionner_radier_submersible(donnees: dict) -> dict:
    q_projet = donnees.get("debit_crue_m3s")
    largeur_radier = donnees.get("largeur_radier_m")
    cote_crete_radier = donnees.get("cote_crete_radier_m")
    coeff_debit = 0.40

    h_lame_crue = (q_projet / (coeff_debit * largeur_radier * math.sqrt(2 * 9.81)))**(2/3)
    niveau_amont_crue = cote_crete_radier + h_lame_crue
    vitesse_sortie = math.sqrt(2 * 9.81 * h_lame_crue)

    return {
        "statut": "OK", "cote_crete_radier_m_ngf": cote_crete_radier,
        "hauteur_eau_amont_crue_m": round(h_lame_crue, 2),
        "niveau_eau_amont_m_ngf": round(niveau_amont_crue, 2),
        "vitesse_sortie_estimee_ms": round(vitesse_sortie, 2)
    }