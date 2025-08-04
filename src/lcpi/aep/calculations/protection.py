"""
Module de calculs pour la protection anti-bélier AEP

Ce module implémente les calculs de protection contre le coup de bélier
dans les réseaux d'eau potable selon les standards techniques.
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

def calculate_water_hammer_protection(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Calcul de la protection anti-bélier pour un réseau d'eau potable.
    
    Args:
        data: Dictionnaire contenant les données de protection
        verbose: Afficher les détails des calculs
    
    Returns:
        Dictionnaire avec les résultats de la protection
    """
    if not data:
        return {
            "statut": "ERREUR",
            "message": "Aucune donnée fournie pour le calcul de protection anti-bélier"
        }
    
    try:
        # Extraction des paramètres
        diametre_mm = data.get("diametre_mm", 0.0)
        epaisseur_mm = data.get("epaisseur_mm", 0.0)
        vitesse_initial_ms = data.get("vitesse_initial_ms", 0.0)
        hmt_m = data.get("hmt_m", 0.0)
        niveau_dynamique_max_m = data.get("niveau_dynamique_max_m", 0.0)
        k_materiau = data.get("k_materiau", K_PVC)
        
        # Calculs de protection
        diametre_m = diametre_mm / 1000
        epaisseur_m = epaisseur_mm / 1000
        
        # Célérité des ondes
        celerite = calculer_celerite_ondes(diametre_mm, epaisseur_mm, k_materiau)
        
        # Variation de pression
        variation_pression = calculer_variation_pression(vitesse_initial_ms, celerite)
        
        # Surpression maximale
        surpression_max = calculer_surpression_maximale(hmt_m, variation_pression, niveau_dynamique_max_m)
        
        # Dépression minimale
        depression_min = calculer_depression_minimale(hmt_m, variation_pression, niveau_dynamique_max_m)
        
        # Vérification des contraintes
        contraintes = {
            "celerite_ok": celerite > 0,
            "variation_ok": variation_pression > 0,
            "surpression_ok": surpression_max <= 100,  # 100 m de surpression max
            "depression_ok": depression_min >= -10,  # -10 m de dépression min
            "vitesse_ok": vitesse_initial_ms <= 2.0  # Vitesse max recommandée
        }
        
        # Recommandations de protection
        recommandations = []
        
        if not contraintes["surpression_ok"]:
            recommandations.append(
                f"Surpression élevée ({surpression_max:.1f} m), installer un réservoir anti-bélier"
            )
        
        if not contraintes["depression_ok"]:
            recommandations.append(
                f"Dépression importante ({depression_min:.1f} m), installer un clapet anti-retour"
            )
        
        if not contraintes["vitesse_ok"]:
            recommandations.append(
                f"Vitesse élevée ({vitesse_initial_ms:.2f} m/s), réduire le diamètre ou installer un réducteur"
            )
        
        # Résultats
        resultat = {
            "statut": "SUCCES",
            "protection": {
                "diametre_mm": diametre_mm,
                "epaisseur_mm": epaisseur_mm,
                "vitesse_initial_ms": vitesse_initial_ms,
                "hmt_m": hmt_m,
                "celerite_ms": celerite,
                "variation_pression_m": variation_pression,
                "surpression_maximale_m": surpression_max,
                "depression_minimale_m": depression_min,
                "k_materiau": k_materiau
            },
            "contraintes": contraintes,
            "recommandations": recommandations
        }
        
        if verbose:
            print(f"Protection anti-bélier: Célérité = {celerite:.0f} m/s, Surpression = {surpression_max:.1f} m")
        
        return resultat
        
    except AEPValidationError as e:
        return {
            "statut": "ERREUR_VALIDATION",
            "message": str(e)
        }
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors du calcul: {str(e)}"
        }

def calculate_water_hammer_protection_advanced(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Calcul avancé de protection anti-bélier avec optimisation des paramètres.
    
    Args:
        data: Dictionnaire contenant les données de protection
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
        # Calcul de base
        resultat = calculate_water_hammer_protection(data, verbose)
        
        if resultat["statut"] == "SUCCES":
            # Optimisation des paramètres
            diametre_mm = data.get("diametre_mm", 0.0)
            vitesse_initial_ms = data.get("vitesse_initial_ms", 0.0)
            
            # Essayer différents diamètres pour optimiser
            diametres_test = [d for d in DIAMETRES_COMMERCIAUX_MM if d >= diametre_mm * 0.8 and d <= diametre_mm * 1.2]
            
            meilleur_diametre = None
            meilleur_score = float('inf')
            
            for diametre_test in diametres_test:
                # Recalculer la vitesse pour le nouveau diamètre
                debit_m3s = vitesse_initial_ms * (diametre_mm/1000)**2 * 3.14159 / 4
                vitesse_test = debit_m3s / ((diametre_test/1000)**2 * 3.14159 / 4)
                
                data_test = data.copy()
                data_test["diametre_mm"] = diametre_test
                data_test["vitesse_initial_ms"] = vitesse_test
                
                resultat_test = calculate_water_hammer_protection(data_test, False)
                if resultat_test["statut"] == "SUCCES":
                    score = (resultat_test["protection"]["surpression_maximale_m"]**2 + 
                            abs(resultat_test["protection"]["depression_minimale_m"])**2)
                    
                    if score < meilleur_score:
                        meilleur_score = score
                        meilleur_diametre = diametre_test
            
            if meilleur_diametre:
                resultat["optimisation"] = {
                    "diametre_optimal_mm": meilleur_diametre,
                    "score_optimisation": meilleur_score,
                    "diametres_testes": diametres_test
                }
        
        return resultat
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors de l'optimisation: {str(e)}"
        }

def compare_protection_scenarios(scenarios: List[Dict[str, Any]], verbose: bool = False) -> Dict[str, Any]:
    """
    Comparaison de différents scénarios de protection anti-bélier.
    
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
            resultat = calculate_water_hammer_protection(scenario, verbose)
            resultats.append({
                "nom": scenario["nom"],
                "resultat": resultat
            })
        
        # Analyse comparative
        surpressions = [
            r["resultat"]["protection"]["surpression_maximale_m"] 
            for r in resultats 
            if r["resultat"]["statut"] == "SUCCES"
        ]
        
        depressions = [
            r["resultat"]["protection"]["depression_minimale_m"] 
            for r in resultats 
            if r["resultat"]["statut"] == "SUCCES"
        ]
        
        analyse = {
            "nb_scenarios": len(scenarios),
            "scenarios_reussis": sum(1 for r in resultats if r["resultat"]["statut"] == "SUCCES"),
            "surpression_min": min(surpressions) if surpressions else 0,
            "surpression_max": max(surpressions) if surpressions else 0,
            "depression_min": min(depressions) if depressions else 0,
            "depression_max": max(depressions) if depressions else 0
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

def get_protection_help() -> str:
    """
    Retourne l'aide pour les fonctions de protection anti-bélier.
    
    Returns:
        Message d'aide formaté
    """
    return """
    PROTECTION ANTI-BÉLIER AEP
    
    Fonctions disponibles:
    
    1. calculate_water_hammer_protection(data, verbose=False)
       Calcul de base de la protection anti-bélier
       
       Paramètres:
       - diametre_mm: Diamètre de la conduite en mm
       - epaisseur_mm: Épaisseur de la conduite en mm
       - vitesse_initial_ms: Vitesse initiale en m/s
       - hmt_m: Hauteur manométrique totale en m
       - niveau_dynamique_max_m: Niveau dynamique maximum en m
       - k_materiau: Coefficient k du matériau (défaut: K_PVC)
    
    2. calculate_water_hammer_protection_advanced(data, verbose=False)
       Calcul avec optimisation des paramètres
       
    3. compare_protection_scenarios(scenarios, verbose=False)
       Comparaison de plusieurs scénarios de protection
       
    Exemple d'utilisation:
    data = {
        "diametre_mm": 200,
        "epaisseur_mm": 5.9,
        "vitesse_initial_ms": 1.5,
        "hmt_m": 50,
        "niveau_dynamique_max_m": 30
    }
    resultat = calculate_water_hammer_protection(data, verbose=True)
    """ 