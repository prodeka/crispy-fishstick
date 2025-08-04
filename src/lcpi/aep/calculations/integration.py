"""
Module d'intégration pour le dimensionnement complet AEP
"""

import sys
import os
from typing import Dict, List, Optional, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from lcpi.aep.core.constants import *
from lcpi.aep.core.formulas import *
from lcpi.aep.core.validators import AEPValidationError

def integrated_aep_design(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """Dimensionnement intégré complet d'un système AEP."""
    if not data:
        return {"statut": "ERREUR", "message": "Aucune donnée fournie"}
    
    try:
        resultats = {}
        
        # Projection démographique
        if "population" in data:
            if verbose:
                print("📊 Calcul de projection démographique...")
            from .population import calculate_population_projection
            resultat_pop = calculate_population_projection(
                population_base=data["population"].get("population_base", 0),
                taux_croissance=data["population"].get("taux_croissance", 0.0),
                annees=data["population"].get("annees", 20),
                verbose=verbose
            )
            resultats["population"] = resultat_pop
        
        # Calcul des besoins en eau
        if "demande" in data:
            if verbose:
                print("💧 Calcul des besoins en eau...")
            from .demand import calculate_water_demand
            population_projetee = resultats.get("population", {}).get("population_projetee", 
                                                                     data["demande"].get("population", 0))
            resultat_demande = calculate_water_demand(
                population=population_projetee,
                dotation_l_j_hab=data["demande"].get("dotation_l_j_hab", 60),
                coefficient_pointe=data["demande"].get("coefficient_pointe", 1.5),
                verbose=verbose
            )
            resultats["demande"] = resultat_demande
        
        # Analyse globale
        statuts = [r.get("statut", "ERREUR") for r in resultats.values()]
        nb_succes = statuts.count("SUCCES")
        nb_total = len(statuts)
        
        resume = {
            "nb_modules": nb_total,
            "nb_succes": nb_succes,
            "nb_echecs": nb_total - nb_succes,
            "taux_reussite": (nb_succes / nb_total * 100) if nb_total > 0 else 0
        }
        
        return {
            "statut": "SUCCES" if resume["taux_reussite"] == 100 else "PARTIEL",
            "resultats": resultats,
            "resume": resume
        }
        
    except Exception as e:
        return {"statut": "ERREUR", "message": f"Erreur: {str(e)}"}

def compare_aep_scenarios(scenarios: List[Dict[str, Any]], verbose: bool = False) -> Dict[str, Any]:
    """Comparaison de différents scénarios de dimensionnement AEP."""
    if not scenarios:
        return {"statut": "ERREUR", "message": "Aucun scénario fourni"}
    
    try:
        resultats = []
        for i, scenario in enumerate(scenarios):
            scenario["nom"] = scenario.get("nom", f"Scénario {i+1}")
            resultat = integrated_aep_design(scenario, verbose)
            resultats.append({"nom": scenario["nom"], "resultat": resultat})
        
        return {"statut": "SUCCES", "resultats": resultats}
        
    except Exception as e:
        return {"statut": "ERREUR", "message": f"Erreur: {str(e)}"}

def get_integration_help() -> str:
    """Retourne l'aide pour les fonctions d'intégration AEP."""
    return """
    INTÉGRATION AEP - DIMENSIONNEMENT COMPLET
    
    Fonctions disponibles:
    
    1. integrated_aep_design(data, verbose=False)
       Dimensionnement intégré complet d'un système AEP
    
    2. compare_aep_scenarios(scenarios, verbose=False)
       Comparaison de plusieurs scénarios AEP complets
       
    Exemple d'utilisation:
    data = {
        "population": {"population_base": 10000, "taux_croissance": 0.03, "annees": 20},
        "demande": {"dotation_l_j_hab": 60, "coefficient_pointe": 1.5}
    }
    resultat = integrated_aep_design(data, verbose=True)
    """ 