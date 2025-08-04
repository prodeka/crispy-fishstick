"""
Module de calculs pour le dimensionnement des réseaux de distribution AEP

Ce module implémente les calculs de dimensionnement des réseaux de distribution
d'eau potable, en réutilisant les fonctions existantes d'hydrodrain et en
ajoutant les nouvelles fonctionnalités spécifiques à l'AEP.
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

def dimension_network(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Dimensionnement du réseau de distribution d'eau potable.
    
    Cette fonction réutilise les calculs d'hydrodrain et ajoute les
    spécificités AEP pour le dimensionnement des réseaux.
    
    Args:
        data: Dictionnaire contenant les données du réseau
        verbose: Afficher les détails des calculs
    
    Returns:
        Dictionnaire avec les résultats du dimensionnement
    """
    if not data:
        return {
            "statut": "ERREUR",
            "message": "Aucune donnée fournie pour le dimensionnement du réseau"
        }
    
    try:
        # Validation des données
        validate_network_data(data)
        
        # Extraction des paramètres
        debit_m3s = data.get("debit_m3s", 0.0)
        longueur_m = data.get("longueur_m", 0.0)
        diametre_mm = data.get("diametre_mm", 0.0)
        ks = data.get("ks", KS_PVC)
        hauteur_geometrique_m = data.get("hauteur_geometrique_m", 0.0)
        
        # Calculs de base
        diametre_m = diametre_mm / 1000
        
        # Pertes de charge (Manning-Strickler)
        pertes_charge = calculer_pertes_charge_manning_strickler(
            debit_m3s, longueur_m, diametre_m, ks
        )
        
        # Hauteur manométrique totale
        hmt = calculer_hauteur_manometrique_totale(hauteur_geometrique_m, pertes_charge)
        
        # Vitesse d'écoulement
        section = calculer_section_circulaire(diametre_m)
        vitesse = calculer_vitesse_ecoulement(debit_m3s, section)
        
        # Vérification des contraintes
        contraintes = {
            "vitesse_ok": VITESSE_MIN <= vitesse <= VITESSE_MAX,
            "hmt_ok": hmt <= 100,  # HMT max typique
            "diametre_ok": diametre_mm in DIAMETRES_COMMERCIAUX_MM
        }
        
        # Résultats
        resultat = {
            "statut": "SUCCES",
            "reseau": {
                "debit_m3s": debit_m3s,
                "longueur_m": longueur_m,
                "diametre_mm": diametre_mm,
                "diametre_m": diametre_m,
                "ks": ks,
                "pertes_charge_m": pertes_charge,
                "hauteur_geometrique_m": hauteur_geometrique_m,
                "hmt_m": hmt,
                "vitesse_ms": vitesse,
                "section_m2": section
            },
            "contraintes": contraintes,
            "recommandations": []
        }
        
        # Recommandations
        if not contraintes["vitesse_ok"]:
            resultat["recommandations"].append(
                f"Vitesse {vitesse:.2f} m/s hors limites [{VITESSE_MIN}-{VITESSE_MAX}] m/s"
            )
        
        if not contraintes["diametre_ok"]:
            resultat["recommandations"].append(
                f"Diamètre {diametre_mm} mm non commercial"
            )
        
        if verbose:
            print(f"Dimensionnement réseau: HMT = {hmt:.1f} m, Vitesse = {vitesse:.2f} m/s")
        
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

def dimension_network_advanced(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Dimensionnement avancé du réseau avec optimisation du diamètre.
    
    Args:
        data: Dictionnaire contenant les données du réseau
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
        debit_m3s = data.get("debit_m3s", 0.0)
        longueur_m = data.get("longueur_m", 0.0)
        hauteur_geometrique_m = data.get("hauteur_geometrique_m", 0.0)
        ks = data.get("ks", KS_PVC)
        
        # Calcul du diamètre théorique
        diametre_theorique_m = calculer_diametre_theorique(debit_m3s, 1.0)  # Vitesse cible 1 m/s
        diametre_theorique_mm = diametre_theorique_m * 1000
        
        # Sélection du diamètre commercial le plus proche
        diametre_commercial_mm = min(
            DIAMETRES_COMMERCIAUX_MM,
            key=lambda x: abs(x - diametre_theorique_mm)
        )
        
        # Dimensionnement avec le diamètre commercial
        data_optimise = data.copy()
        data_optimise["diametre_mm"] = diametre_commercial_mm
        
        resultat = dimension_network(data_optimise, verbose)
        
        if resultat["statut"] == "SUCCES":
            resultat["optimisation"] = {
                "diametre_theorique_mm": diametre_theorique_mm,
                "diametre_commercial_mm": diametre_commercial_mm,
                "ecart_mm": abs(diametre_commercial_mm - diametre_theorique_mm)
            }
        
        return resultat
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors de l'optimisation: {str(e)}"
        }

def compare_network_scenarios(scenarios: List[Dict[str, Any]], verbose: bool = False) -> Dict[str, Any]:
    """
    Comparaison de différents scénarios de dimensionnement réseau.
    
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
            resultat = dimension_network(scenario, verbose)
            resultats.append({
                "nom": scenario["nom"],
                "resultat": resultat
            })
        
        # Analyse comparative
        analyse = {
            "nb_scenarios": len(scenarios),
            "scenarios_reussis": sum(1 for r in resultats if r["resultat"]["statut"] == "SUCCES"),
            "meilleur_hmt": min(
                (r for r in resultats if r["resultat"]["statut"] == "SUCCES"),
                key=lambda x: x["resultat"]["reseau"]["hmt_m"],
                default=None
            )
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

def get_network_help() -> str:
    """
    Retourne l'aide pour les fonctions de dimensionnement réseau.
    
    Returns:
        Message d'aide formaté
    """
    return """
    DIMENSIONNEMENT RÉSEAU DE DISTRIBUTION AEP
    
    Fonctions disponibles:
    
    1. dimension_network(data, verbose=False)
       Dimensionnement de base d'un tronçon de réseau
       
       Paramètres:
       - debit_m3s: Débit en m³/s
       - longueur_m: Longueur du tronçon en m
       - diametre_mm: Diamètre en mm
       - ks: Coefficient de rugosité (défaut: KS_PVC)
       - hauteur_geometrique_m: Hauteur géométrique en m
    
    2. dimension_network_advanced(data, verbose=False)
       Dimensionnement avec optimisation automatique du diamètre
       
    3. compare_network_scenarios(scenarios, verbose=False)
       Comparaison de plusieurs scénarios de dimensionnement
       
    Exemple d'utilisation:
    data = {
        "debit_m3s": 0.05,
        "longueur_m": 1000,
        "diametre_mm": 200,
        "hauteur_geometrique_m": 10
    }
    resultat = dimension_network(data, verbose=True)
    """ 