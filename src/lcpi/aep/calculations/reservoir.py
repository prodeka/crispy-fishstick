"""
Module de calculs pour le dimensionnement des réservoirs de stockage AEP

Ce module implémente les calculs de dimensionnement des réservoirs de stockage
d'eau potable selon les standards techniques.
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

# Ajouter le chemin pour importer hydrodrain
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from lcpi.aep.core.constants import *
from lcpi.aep.core.formulas import *
from lcpi.aep.core.validators import AEPValidationError

def dimension_reservoir(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Dimensionnement d'un réservoir de stockage d'eau potable.
    
    Args:
        data: Dictionnaire contenant les données du réservoir
        verbose: Afficher les détails des calculs
    
    Returns:
        Dictionnaire avec les résultats du dimensionnement
    """
    if not data:
        return {
            "statut": "ERREUR",
            "message": "Aucune donnée fournie pour le dimensionnement du réservoir"
        }
    
    try:
        # Extraction des paramètres
        besoin_brut_jour = data.get("besoin_brut_jour", 0.0)
        type_adduction = data.get("type_adduction", "continue")
        volume_incendie = data.get("volume_incendie", VOLUME_INCENDIE)
        duree_couverture = data.get("duree_couverture", DUREE_COUVERTURE_SECURITE)
        
        # Calculs des volumes
        volume_utile = calculer_volume_utile(besoin_brut_jour, type_adduction)
        volume_mort = calculer_volume_mort(volume_utile)
        volume_securite = calculer_volume_securite(besoin_brut_jour, duree_couverture)
        volume_total = calculer_volume_total(volume_utile, volume_incendie, volume_mort, volume_securite)
        
        # Calcul des dimensions (réservoir cylindrique)
        dimensions = calculer_dimensions_reservoir_cylindrique(volume_total)
        
        # Vérification des contraintes
        contraintes = {
            "volume_ok": volume_total > 0,
            "dimensions_ok": dimensions["diametre_m"] <= 20 and dimensions["hauteur_m"] <= 12,
            "ratio_ok": dimensions["hauteur_m"] / dimensions["diametre_m"] <= 1.5
        }
        
        # Résultats
        resultat = {
            "statut": "SUCCES",
            "reservoir": {
                "volume_utile_m3": volume_utile,
                "volume_incendie_m3": volume_incendie,
                "volume_mort_m3": volume_mort,
                "volume_securite_m3": volume_securite,
                "volume_total_m3": volume_total,
                "diametre_m": dimensions["diametre_m"],
                "hauteur_m": dimensions["hauteur_m"],
                "type_adduction": type_adduction
            },
            "contraintes": contraintes,
            "recommandations": []
        }
        
        # Recommandations
        if not contraintes["dimensions_ok"]:
            resultat["recommandations"].append(
                "Dimensions du réservoir hors limites recommandées"
            )
        
        if not contraintes["ratio_ok"]:
            resultat["recommandations"].append(
                "Ratio hauteur/diamètre élevé, considérer un réservoir plus large"
            )
        
        if verbose:
            print(f"Dimensionnement réservoir: Volume total = {volume_total:.1f} m³")
        
        return resultat
        
    except AEPValidationError as e:
        return {
            "statut": "ERREUR_VALIDATION",
            "message": str(e)
        }
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors du dimensionnement: {str(e)}"
        }

def dimension_reservoir_advanced(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Dimensionnement avancé du réservoir avec optimisation des dimensions.
    
    Args:
        data: Dictionnaire contenant les données du réservoir
        verbose: Afficher les détails des calculs
    
    Returns:
        Dictionnaire avec les résultats optimisés
    """
    if not data:
        return {
            "statut": "ERREUR",
            "message": "Aucune donnée fournie"
        }
    
    try:
        # Dimensionnement de base
        resultat = dimension_reservoir(data, verbose)
        
        if resultat["statut"] == "SUCCES":
            # Optimisation des dimensions
            volume_total = resultat["reservoir"]["volume_total_m3"]
            
            # Essayer différentes hauteurs pour optimiser
            hauteurs_test = [8.0, 10.0, 12.0, 15.0]
            meilleures_dimensions = None
            meilleur_score = float('inf')
            
            for hauteur in hauteurs_test:
                dimensions = calculer_dimensions_reservoir_cylindrique(volume_total, hauteur)
                score = abs(dimensions["hauteur_m"] / dimensions["diametre_m"] - 1.0)  # Ratio proche de 1
                
                if score < meilleur_score and dimensions["diametre_m"] <= 20:
                    meilleur_score = score
                    meilleures_dimensions = dimensions
            
            if meilleures_dimensions:
                resultat["reservoir"].update(meilleures_dimensions)
                resultat["optimisation"] = {
                    "score_optimisation": meilleur_score,
                    "hauteurs_testees": hauteurs_test
                }
        
        return resultat
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors de l'optimisation: {str(e)}"
        }

def compare_reservoir_scenarios(scenarios: List[Dict[str, Any]], verbose: bool = False) -> Dict[str, Any]:
    """
    Comparaison de différents scénarios de dimensionnement réservoir.
    
    Args:
        scenarios: Liste des scénarios à comparer
        verbose: Afficher les détails
    
    Returns:
        Dictionnaire avec la comparaison
    """
    if not scenarios:
        return {
            "statut": "ERREUR",
            "message": "Aucun scénario fourni"
        }
    
    try:
        resultats = []
        
        for i, scenario in enumerate(scenarios):
            scenario["nom"] = scenario.get("nom", f"Scénario {i+1}")
            resultat = dimension_reservoir(scenario, verbose)
            resultats.append({
                "nom": scenario["nom"],
                "resultat": resultat
            })
        
        # Analyse comparative
        volumes_utiles = [
            r["resultat"]["reservoir"]["volume_utile_m3"] 
            for r in resultats 
            if r["resultat"]["statut"] == "SUCCES"
        ]
        
        analyse = {
            "nb_scenarios": len(scenarios),
            "scenarios_reussis": sum(1 for r in resultats if r["resultat"]["statut"] == "SUCCES"),
            "volume_min": min(volumes_utiles) if volumes_utiles else 0,
            "volume_max": max(volumes_utiles) if volumes_utiles else 0,
            "volume_moyen": sum(volumes_utiles) / len(volumes_utiles) if volumes_utiles else 0
        }
        
        return {
            "statut": "SUCCES",
            "resultats": resultats,
            "analyse": analyse
        }
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors de la comparaison: {str(e)}"
        }

def get_reservoir_help() -> str:
    """
    Retourne l'aide pour les fonctions de dimensionnement réservoir.
    
    Returns:
        Message d'aide formaté
    """
    return """
    DIMENSIONNEMENT RÉSERVOIR DE STOCKAGE AEP
    
    Fonctions disponibles:
    
    1. dimension_reservoir(data, verbose=False)
       Dimensionnement de base d'un réservoir de stockage
       
       Paramètres:
       - besoin_brut_jour: Besoin brut journalier en m³/jour
       - type_adduction: Type d'adduction ("continue" ou "discontinue")
       - volume_incendie: Volume incendie en m³ (défaut: 7.2)
       - duree_couverture: Durée de couverture en heures (défaut: 6.0)
    
    2. dimension_reservoir_advanced(data, verbose=False)
       Dimensionnement avec optimisation des dimensions
       
    3. compare_reservoir_scenarios(scenarios, verbose=False)
       Comparaison de plusieurs scénarios de dimensionnement
       
    Exemple d'utilisation:
    data = {
        "besoin_brut_jour": 2000,
        "type_adduction": "continue",
        "volume_incendie": 10.0
    }
    resultat = dimension_reservoir(data, verbose=True)
    """ 