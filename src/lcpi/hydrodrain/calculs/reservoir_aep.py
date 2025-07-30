import math
import numpy as np
from typing import Dict, List, Optional

def dimensionner_reservoir_equilibrage(demande_journaliere_m3: float, coefficient_pointe_jour: float = 1.3, 
                                     coefficient_pointe_horaire: float = 1.7, nombre_jours_stockage: int = 1) -> Dict:
    """
    Dimensionne un réservoir d'équilibrage pour l'eau potable.
    
    Args:
        demande_journaliere_m3: Demande journalière moyenne en m³
        coefficient_pointe_jour: Coefficient de pointe journalière
        coefficient_pointe_horaire: Coefficient de pointe horaire
        nombre_jours_stockage: Nombre de jours de stockage de sécurité
    
    Returns:
        dict: Résultats du dimensionnement
    """
    # Calcul des débits caractéristiques
    debit_moyen_m3_h = demande_journaliere_m3 / 24
    debit_pointe_jour_m3_h = debit_moyen_m3_h * coefficient_pointe_jour
    debit_pointe_horaire_m3_h = debit_moyen_m3_h * coefficient_pointe_horaire
    
    # Volume d'équilibrage (différence entre production et consommation)
    # Approche simplifiée: 15% du volume journalier
    volume_equilibrage_m3 = demande_journaliere_m3 * 0.15
    
    # Volume de stockage de sécurité
    volume_securite_m3 = demande_journaliere_m3 * nombre_jours_stockage
    
    # Volume total du réservoir
    volume_total_m3 = volume_equilibrage_m3 + volume_securite_m3
    
    # Hauteur d'eau recommandée (entre 3 et 6 m)
    hauteur_eau_m = min(max(volume_total_m3 / 100, 3), 6)  # Surface approximative de 100 m²
    
    return {
        "statut": "OK",
        "debit_moyen_m3_h": round(debit_moyen_m3_h, 2),
        "debit_pointe_jour_m3_h": round(debit_pointe_jour_m3_h, 2),
        "debit_pointe_horaire_m3_h": round(debit_pointe_horaire_m3_h, 2),
        "volume_equilibrage_m3": round(volume_equilibrage_m3, 1),
        "volume_securite_m3": round(volume_securite_m3, 1),
        "volume_total_m3": round(volume_total_m3, 1),
        "hauteur_eau_recommandee_m": round(hauteur_eau_m, 1),
        "surface_approximative_m2": round(volume_total_m3 / hauteur_eau_m, 1)
    }

def dimensionner_reservoir_incendie(population: int, surface_zone_ha: float, type_zone: str = "urbain") -> Dict:
    """
    Dimensionne un réservoir d'incendie selon les normes.
    
    Args:
        population: Population desservie
        surface_zone_ha: Surface de la zone en hectares
        type_zone: Type de zone ("urbain", "rural", "industriel")
    
    Returns:
        dict: Résultats du dimensionnement
    """
    # Débit d'incendie selon le type de zone
    if type_zone == "urbain":
        debit_incendie_l_min = 120
        duree_incendie_min = 60
    elif type_zone == "rural":
        debit_incendie_l_min = 60
        duree_incendie_min = 45
    elif type_zone == "industriel":
        debit_incendie_l_min = 200
        duree_incendie_min = 90
    else:
        return {"statut": "Erreur", "message": f"Type de zone '{type_zone}' non reconnu"}
    
    # Volume d'incendie
    volume_incendie_m3 = (debit_incendie_l_min * duree_incendie_min) / 1000
    
    # Volume supplémentaire pour les besoins domestiques pendant l'incendie
    # (2 heures de consommation normale)
    consommation_domestique_l_jour_hab = 150
    volume_domestique_m3 = (population * consommation_domestique_l_jour_hab * 2) / (1000 * 24)
    
    # Volume total
    volume_total_m3 = volume_incendie_m3 + volume_domestique_m3
    
    return {
        "statut": "OK",
        "type_zone": type_zone,
        "debit_incendie_l_min": debit_incendie_l_min,
        "duree_incendie_min": duree_incendie_min,
        "volume_incendie_m3": round(volume_incendie_m3, 1),
        "volume_domestique_m3": round(volume_domestique_m3, 1),
        "volume_total_m3": round(volume_total_m3, 1)
    }

def calculer_volume_reservoir_optimal(demandes_horaires_m3: List[float], production_horaire_m3: float) -> Dict:
    """
    Calcule le volume optimal d'un réservoir par la méthode des courbes cumulées.
    
    Args:
        demandes_horaires_m3: Liste des demandes horaires sur 24h
        production_horaire_m3: Production horaire constante
    
    Returns:
        dict: Résultats du calcul
    """
    if len(demandes_horaires_m3) != 24:
        return {"statut": "Erreur", "message": "La liste doit contenir 24 valeurs (une par heure)"}
    
    # Production cumulée (constante)
    production_cumulee = [production_horaire_m3 * (i + 1) for i in range(24)]
    
    # Demande cumulée
    demande_cumulee = []
    cumul = 0
    for demande in demandes_horaires_m3:
        cumul += demande
        demande_cumulee.append(cumul)
    
    # Différences entre production et demande
    differences = [prod - dem for prod, dem in zip(production_cumulee, demande_cumulee)]
    
    # Volume de stockage nécessaire
    volume_stockage_m3 = max(differences) - min(differences)
    
    # Heures de pointe et de creux
    heure_pointe = differences.index(max(differences)) + 1
    heure_creux = differences.index(min(differences)) + 1
    
    return {
        "statut": "OK",
        "volume_stockage_m3": round(volume_stockage_m3, 1),
        "heure_pointe": heure_pointe,
        "heure_creux": heure_creux,
        "surplus_max_m3": round(max(differences), 1),
        "deficit_max_m3": round(abs(min(differences)), 1),
        "courbes_cumulees": {
            "production": production_cumulee,
            "demande": demande_cumulee,
            "differences": [round(d, 1) for d in differences]
        }
    }

def verifier_pression_reservoir(cote_reservoir_m: float, cote_terrain_m: float, 
                               pertes_charge_m: float, pression_minimale_m: float = 15.0) -> Dict:
    """
    Vérifie la pression disponible dans le réseau depuis un réservoir.
    
    Args:
        cote_reservoir_m: Cote du réservoir en m NGF
        cote_terrain_m: Cote du terrain en m NGF
        pertes_charge_m: Pertes de charge dans le réseau en m
        pression_minimale_m: Pression minimale requise en m
    
    Returns:
        dict: Résultats de la vérification
    """
    # Pression disponible
    pression_disponible_m = cote_reservoir_m - cote_terrain_m - pertes_charge_m
    
    # Vérification
    conforme = pression_disponible_m >= pression_minimale_m
    marge_securite_m = pression_disponible_m - pression_minimale_m
    
    return {
        "statut": "OK",
        "pression_disponible_m": round(pression_disponible_m, 1),
        "pression_minimale_m": pression_minimale_m,
        "marge_securite_m": round(marge_securite_m, 1),
        "conforme": conforme,
        "niveau_securite": "Excellent" if marge_securite_m > 10 else "Bon" if marge_securite_m > 5 else "Limite" if conforme else "Insuffisant"
    }

def calculer_renouvellement_eau_reservoir(volume_reservoir_m3: float, debit_circulation_m3_h: float) -> Dict:
    """
    Calcule le temps de renouvellement de l'eau dans un réservoir.
    
    Args:
        volume_reservoir_m3: Volume du réservoir en m³
        debit_circulation_m3_h: Débit de circulation en m³/h
    
    Returns:
        dict: Résultats du calcul
    """
    if debit_circulation_m3_h <= 0:
        return {"statut": "Erreur", "message": "Le débit de circulation doit être positif"}
    
    # Temps de renouvellement
    temps_renouvellement_h = volume_reservoir_m3 / debit_circulation_m3_h
    temps_renouvellement_jours = temps_renouvellement_h / 24
    
    # Évaluation de la qualité
    if temps_renouvellement_h < 24:
        qualite = "Excellent"
    elif temps_renouvellement_h < 48:
        qualite = "Bon"
    elif temps_renouvellement_h < 72:
        qualite = "Acceptable"
    else:
        qualite = "Problématique"
    
    return {
        "statut": "OK",
        "temps_renouvellement_h": round(temps_renouvellement_h, 1),
        "temps_renouvellement_jours": round(temps_renouvellement_jours, 1),
        "qualite_renouvellement": qualite,
        "recommandation": "Augmenter la circulation" if temps_renouvellement_h > 72 else "Renouvellement satisfaisant"
    }

def dimensionner_reservoir_complet(population: int, dotation_l_jour_hab: float = 150.0, 
                                 coefficient_pointe_jour: float = 1.3, coefficient_pointe_horaire: float = 1.7,
                                 nombre_jours_securite: int = 1, type_zone_incendie: str = "urbain") -> Dict:
    """
    Dimensionne un réservoir complet (équilibrage + incendie + sécurité).
    
    Args:
        population: Population desservie
        dotation_l_jour_hab: Dotation en L/jour/habitant
        coefficient_pointe_jour: Coefficient de pointe journalière
        coefficient_pointe_horaire: Coefficient de pointe horaire
        nombre_jours_securite: Nombre de jours de stockage de sécurité
        type_zone_incendie: Type de zone pour l'incendie
    
    Returns:
        dict: Résultats du dimensionnement complet
    """
    # Demande journalière
    demande_journaliere_m3 = (population * dotation_l_jour_hab) / 1000
    
    # Dimensionnement équilibrage
    resultat_equilibrage = dimensionner_reservoir_equilibrage(
        demande_journaliere_m3, coefficient_pointe_jour, coefficient_pointe_horaire, nombre_jours_securite
    )
    
    # Dimensionnement incendie
    resultat_incendie = dimensionner_reservoir_incendie(population, 0, type_zone_incendie)
    
    # Volume total
    volume_total_m3 = resultat_equilibrage["volume_total_m3"] + resultat_incendie["volume_total_m3"]
    
    # Dimensions recommandées
    hauteur_eau_m = 4.0  # Hauteur standard
    surface_m2 = volume_total_m3 / hauteur_eau_m
    diametre_m = math.sqrt((4 * surface_m2) / math.pi) if surface_m2 > 0 else 0
    
    return {
        "statut": "OK",
        "population": population,
        "demande_journaliere_m3": round(demande_journaliere_m3, 1),
        "volume_equilibrage_m3": resultat_equilibrage["volume_total_m3"],
        "volume_incendie_m3": resultat_incendie["volume_total_m3"],
        "volume_total_m3": round(volume_total_m3, 1),
        "hauteur_eau_m": hauteur_eau_m,
        "surface_m2": round(surface_m2, 1),
        "diametre_m": round(diametre_m, 1),
        "details_equilibrage": resultat_equilibrage,
        "details_incendie": resultat_incendie
    }
