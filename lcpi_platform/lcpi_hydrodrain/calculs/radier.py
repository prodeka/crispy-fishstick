import math

def dimensionner_radier_submersible(donnees: dict) -> dict:
    q_projet = donnees.get("debit_crue_m3s")
    largeur_radier = donnees.get("largeur_radier_m")
    cote_crete_radier = donnees.get("cote_crete_radier_m")
    coeff_debit = 0.40 # Coeff pour seuil épais

    # Phase 2.3 : Calcul de la hauteur de lame d'eau en crue
    h_lame_crue = (q_projet / (coeff_debit * largeur_radier * math.sqrt(2 * 9.81)))**(2/3)
    niveau_amont_crue = cote_crete_radier + h_lame_crue

    # Phase 3.1 : Calcul de la vitesse en sortie (simplifié)
    vitesse_sortie = math.sqrt(2 * 9.81 * h_lame_crue)

    return {
        "statut": "OK",
        "cote_crete_radier_m_ngf": cote_crete_radier,
        "hauteur_eau_amont_crue_m": round(h_lame_crue, 2),
        "niveau_eau_amont_m_ngf": round(niveau_amont_crue, 2),
        "vitesse_sortie_estimee_ms": round(vitesse_sortie, 2)
    }

def verifier_radier_ancrage(donnees: dict) -> dict:
    # Phase 2 : Calcul des forces
    h_sous_pression = donnees.get("niveau_nappe_ngf") - donnees.get("niveau_fond_radier_ngf")
    if h_sous_pression < 0: h_sous_pression = 0
    
    force_soulevement_kn = h_sous_pression * 9.81 * donnees.get("surface_radier_m2")
    
    force_stabilisante_kn = donnees.get("poids_radier_kn") + donnees.get("poids_remblai_kn")
    
    # Phase 3 : Vérification
    coeff_secu_calcule = force_stabilisante_kn / force_soulevement_kn if force_soulevement_kn > 0 else 999
    
    return {
        "statut": "OK",
        "force_soulevement_kn": round(force_soulevement_kn, 2),
        "force_stabilisante_kn": round(force_stabilisante_kn, 2),
        "coefficient_securite_calcule": round(coeff_secu_calcule, 2),
        "conforme": coeff_secu_calcule >= donnees.get("coeff_securite_requis")
    }
