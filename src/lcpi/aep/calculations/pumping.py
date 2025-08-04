"""
Module de calculs pour le dimensionnement des équipements de pompage AEP

Ce module implémente les calculs de dimensionnement des équipements de pompage
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

def dimension_pumping(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Dimensionnement des équipements de pompage d'eau potable.
    
    Args:
        data: Dictionnaire contenant les données de pompage
        verbose: Afficher les détails des calculs
    
    Returns:
        Dictionnaire avec les résultats du dimensionnement
    """
    if not data:
        return {
            "statut": "ERREUR",
            "message": "Aucune donnée fournie pour le dimensionnement du pompage"
        }
    
    try:
        # Extraction des paramètres
        debit_m3h = data.get("debit_m3h", 0.0)
        hmt_m = data.get("hmt_m", 0.0)
        rendement_pompe = data.get("rendement_pompe", RENDEMENT_POMPE)
        rendement_moteur = data.get("rendement_moteur", RENDEMENT_MOTEUR)
        facteur_puissance = data.get("facteur_puissance", FACTEUR_PUISSANCE)
        
        # Conversion débit m³/h vers m³/s
        debit_m3s = debit_m3h / 3600
        
        # Calculs de puissance
        puissance_hydraulique = calculer_puissance_hydraulique(debit_m3s, hmt_m)
        puissance_electrique = calculer_puissance_electrique(
            puissance_hydraulique, rendement_pompe, rendement_moteur
        )
        puissance_groupe = calculer_puissance_groupe_electrogene(
            debit_m3h, hmt_m, rendement_pompe, rendement_moteur, facteur_puissance
        )
        
        # Vérification des contraintes
        contraintes = {
            "debit_ok": debit_m3h > 0,
            "hmt_ok": 0 < hmt_m <= 200,  # HMT max typique
            "puissance_ok": puissance_electrique > 0,
            "rendement_ok": 0 < rendement_pompe <= 1 and 0 < rendement_moteur <= 1
        }
        
        # Résultats
        resultat = {
            "statut": "SUCCES",
            "pompage": {
                "debit_m3h": debit_m3h,
                "debit_m3s": debit_m3s,
                "hmt_m": hmt_m,
                "puissance_hydraulique_w": puissance_hydraulique,
                "puissance_hydraulique_kw": puissance_hydraulique / 1000,
                "puissance_electrique_w": puissance_electrique,
                "puissance_electrique_kw": puissance_electrique / 1000,
                "puissance_groupe_kva": puissance_groupe,
                "rendement_pompe": rendement_pompe,
                "rendement_moteur": rendement_moteur,
                "facteur_puissance": facteur_puissance
            },
            "contraintes": contraintes,
            "recommandations": []
        }
        
        # Recommandations
        if puissance_electrique > 100000:  # 100 kW
            resultat["recommandations"].append(
                "Puissance élevée, considérer plusieurs pompes en parallèle"
            )
        
        if hmt_m > 100:
            resultat["recommandations"].append(
                "HMT élevée, vérifier la nécessité d'étages multiples"
            )
        
        if verbose:
            print(f"Dimensionnement pompage: P_élec = {puissance_electrique/1000:.1f} kW")
        
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

def dimension_pumping_advanced(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Dimensionnement avancé du pompage avec optimisation des rendements.
    
    Args:
        data: Dictionnaire contenant les données de pompage
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
        resultat = dimension_pumping(data, verbose)
        
        if resultat["statut"] == "SUCCES":
            # Optimisation des rendements
            debit_m3h = data.get("debit_m3h", 0.0)
            hmt_m = data.get("hmt_m", 0.0)
            
            # Essayer différents rendements
            rendements_pompe = [0.70, 0.75, 0.80, 0.85, 0.90]
            rendements_moteur = [0.80, 0.85, 0.90, 0.95]
            
            meilleure_combinaison = None
            puissance_min = float('inf')
            
            for rp in rendements_pompe:
                for rm in rendements_moteur:
                    data_test = data.copy()
                    data_test["rendement_pompe"] = rp
                    data_test["rendement_moteur"] = rm
                    
                    resultat_test = dimension_pumping(data_test, False)
                    if resultat_test["statut"] == "SUCCES":
                        puissance = resultat_test["pompage"]["puissance_electrique_w"]
                        if puissance < puissance_min:
                            puissance_min = puissance
                            meilleure_combinaison = (rp, rm)
            
            if meilleure_combinaison:
                resultat["optimisation"] = {
                    "rendement_pompe_optimal": meilleure_combinaison[0],
                    "rendement_moteur_optimal": meilleure_combinaison[1],
                    "puissance_minimale_w": puissance_min,
                    "economie_w": resultat["pompage"]["puissance_electrique_w"] - puissance_min
                }
        
        return resultat
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors de l'optimisation: {str(e)}"
        }

def compare_pumping_scenarios(scenarios: List[Dict[str, Any]], verbose: bool = False) -> Dict[str, Any]:
    """
    Comparaison de différents scénarios de dimensionnement pompage.
    
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
            resultat = dimension_pumping(scenario, verbose)
            resultats.append({
                "nom": scenario["nom"],
                "resultat": resultat
            })
        
        # Analyse comparative
        puissances = [
            r["resultat"]["pompage"]["puissance_electrique_kw"] 
            for r in resultats 
            if r["resultat"]["statut"] == "SUCCES"
        ]
        
        analyse = {
            "nb_scenarios": len(scenarios),
            "scenarios_reussis": sum(1 for r in resultats if r["resultat"]["statut"] == "SUCCES"),
            "puissance_min": min(puissances) if puissances else 0,
            "puissance_max": max(puissances) if puissances else 0,
            "puissance_moyenne": sum(puissances) / len(puissances) if puissances else 0
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

def get_pumping_help() -> str:
    """
    Retourne l'aide pour les fonctions de dimensionnement pompage.
    
    Returns:
        Message d'aide formaté
    """
    return """
    DIMENSIONNEMENT ÉQUIPEMENTS DE POMPAGE AEP
    
    Fonctions disponibles:
    
    1. dimension_pumping(data, verbose=False)
       Dimensionnement de base des équipements de pompage
       
       Paramètres:
       - debit_m3h: Débit en m³/h
       - hmt_m: Hauteur manométrique totale en m
       - rendement_pompe: Rendement de la pompe (défaut: 0.75)
       - rendement_moteur: Rendement du moteur (défaut: 0.85)
       - facteur_puissance: Facteur de puissance (défaut: 0.85)
    
    2. dimension_pumping_advanced(data, verbose=False)
       Dimensionnement avec optimisation des rendements
       
    3. compare_pumping_scenarios(scenarios, verbose=False)
       Comparaison de plusieurs scénarios de dimensionnement
       
    Exemple d'utilisation:
    data = {
        "debit_m3h": 100,
        "hmt_m": 50,
        "rendement_pompe": 0.80,
        "rendement_moteur": 0.90
    }
    resultat = dimension_pumping(data, verbose=True)
    """ 