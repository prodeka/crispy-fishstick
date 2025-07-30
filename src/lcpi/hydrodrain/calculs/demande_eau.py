def estimer_demande_eau(donnees: dict) -> dict:
    """
    Estime la demande en eau potable sur la base de la population, de la dotation
    et du rendement du réseau.
    """
    population = donnees.get("population")
    dotation_domestique = donnees.get("dotation_domestique_l_j_hab")
    besoins_publics_m3_j = donnees.get("besoins_publics_m3_j", 0)
    
    # Le rendement est l'inverse des pertes. Rendement de 0.8 = 20% de pertes.
    rendement = donnees.get("rendement_reseau", 0.8)

    if not all([population, dotation_domestique]):
        return {"statut": "Erreur", "message": "Données d'entrée manquantes (population ou dotation)."}

    q_dom_m3_j = (population * dotation_domestique) / 1000
    q_total_jour_m3 = q_dom_m3_j + besoins_publics_m3_j
    
    # La production doit compenser les pertes du réseau
    q_production_m3_j = q_total_jour_m3 / rendement if rendement > 0 else 0
    
    # Coefficient de pointe horaire (valeur commune)
    cp_h = 1.7 
    q_ph_m3_h = (q_production_m3_j * cp_h) / 24
    
    return {
        "statut": "OK",
        "besoin_journalier_total_m3_jour": round(q_total_jour_m3, 2),
        "production_requise_m3_jour": round(q_production_m3_j, 2),
        "debit_pointe_horaire_m3_h": round(q_ph_m3_h, 2),
        "parametres_entree": {
            "population": population,
            "dotation_domestique_l_j_hab": dotation_domestique,
            "rendement_reseau": rendement
        }
    }
