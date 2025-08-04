"""
Module de calculs demande unifié pour AEP - Version Fusionnée et Enrichie

Ce module fusionne les fonctionnalités de demand.py et population_unified.py
pour offrir une version complète avec :
- Transparence mathématique
- Support de base de données
- Multiples méthodes de calcul
- Validation robuste
- Interface CLI/REPL optimisée
"""

import math
import json
import sys
import os
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

# Ajouter le chemin pour importer hydrodrain
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from lcpi.aep.core.constants import *
from lcpi.aep.core.formulas import *
from lcpi.aep.core.validators import AEPValidationError, validate_demand_data

try:
    from ..core.mathematical_transparency import math_transparency
    MATH_TRANSPARENCY_AVAILABLE = True
except ImportError:
    MATH_TRANSPARENCY_AVAILABLE = False
    print("⚠️ Module de transparence mathématique non disponible")

try:
    from lcpi.hydrodrain.calculs.demande_eau import estimer_demande_eau
    HYDRODRAIN_AVAILABLE = True
except ImportError:
    HYDRODRAIN_AVAILABLE = False
    print("⚠️ Module hydrodrain non disponible")

class DemandCalculationsUnified:
    """
    Classe unifiée pour les calculs demande AEP.
    Fusionne les fonctionnalités de demand.py et population_unified.py
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialise le calculateur demande unifié.
        
        Args:
            db_path: Chemin vers la base de données AEP
        """
        self.db_path = db_path or "src/lcpi/db/aep_database.json"
        self.load_database()
        
    def load_database(self):
        """Charge la base de données AEP."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
            print("✅ Base de données AEP chargée avec succès.")
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement de la base de données: {e}")
            self.db = {}
    
    def calculer_besoin_domestique(self, population: int, dotation_l_hab_j: float) -> Dict[str, Any]:
        """
        Calcule le besoin domestique en eau.
        
        Args:
            population: Nombre d'habitants
            dotation_l_hab_j: Dotation en litres par habitant et par jour
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        besoin_domestique_m3j = population * dotation_l_hab_j / 1000
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("besoin_domestique", {
                "P": population,
                "D": dotation_l_hab_j
            })
        
        return {
            "besoin_domestique_m3j": besoin_domestique_m3j,
            "population": population,
            "dotation_l_hab_j": dotation_l_hab_j,
            "explication": explanation
        }
    
    def calculer_besoin_annexe(self, besoin_domestique_m3j: float, pourcentage_annexe: float = 0.1) -> Dict[str, Any]:
        """
        Calcule le besoin annexe en eau.
        
        Args:
            besoin_domestique_m3j: Besoin domestique en m³/j
            pourcentage_annexe: Pourcentage du besoin domestique (défaut: 10%)
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        besoin_annexe_m3j = besoin_domestique_m3j * pourcentage_annexe
        
        return {
            "besoin_annexe_m3j": besoin_annexe_m3j,
            "besoin_domestique_m3j": besoin_domestique_m3j,
            "pourcentage_annexe": pourcentage_annexe
        }
    
    def calculer_besoin_global(self, besoin_domestique_m3j: float, besoin_annexe_m3j: float) -> Dict[str, Any]:
        """
        Calcule le besoin global en eau.
        
        Args:
            besoin_domestique_m3j: Besoin domestique en m³/j
            besoin_annexe_m3j: Besoin annexe en m³/j
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        besoin_global_m3j = besoin_domestique_m3j + besoin_annexe_m3j
        
        return {
            "besoin_global_m3j": besoin_global_m3j,
            "besoin_domestique_m3j": besoin_domestique_m3j,
            "besoin_annexe_m3j": besoin_annexe_m3j
        }
    
    def calculer_besoin_pointe(self, besoin_global_m3j: float, coefficient_pointe: float = 1.5) -> Dict[str, Any]:
        """
        Calcule le besoin de pointe en eau.
        
        Args:
            besoin_global_m3j: Besoin global en m³/j
            coefficient_pointe: Coefficient de pointe journalière
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        besoin_pointe_m3j = besoin_global_m3j * coefficient_pointe
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("besoin_pointe", {
                "B_global": besoin_global_m3j,
                "C_p": coefficient_pointe
            })
        
        return {
            "besoin_pointe_m3j": besoin_pointe_m3j,
            "besoin_global_m3j": besoin_global_m3j,
            "coefficient_pointe": coefficient_pointe,
            "explication": explanation
        }
    
    def calculer_besoin_brut(self, besoin_pointe_m3j: float, rendement_technique: float = 0.85) -> Dict[str, Any]:
        """
        Calcule le besoin brut en eau (avec pertes techniques).
        
        Args:
            besoin_pointe_m3j: Besoin de pointe en m³/j
            rendement_technique: Rendement technique du réseau (0-1)
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        besoin_brut_m3j = besoin_pointe_m3j / rendement_technique
        
        return {
            "besoin_brut_m3j": besoin_brut_m3j,
            "besoin_pointe_m3j": besoin_pointe_m3j,
            "rendement_technique": rendement_technique
        }
    
    def calculer_debit_pointe_horaire(self, besoin_brut_m3j: float, coefficient_pointe_horaire: float = 2.0) -> Dict[str, Any]:
        """
        Calcule le débit de pointe horaire.
        
        Args:
            besoin_brut_m3j: Besoin brut en m³/j
            coefficient_pointe_horaire: Coefficient de pointe horaire
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        debit_moyen_m3h = besoin_brut_m3j / 24.0
        debit_pointe_m3h = debit_moyen_m3h * coefficient_pointe_horaire
        debit_pointe_m3s = debit_pointe_m3h / 3600
        
        return {
            "debit_pointe_m3h": debit_pointe_m3h,
            "debit_pointe_m3s": debit_pointe_m3s,
            "debit_moyen_m3h": debit_moyen_m3h,
            "coefficient_pointe_horaire": coefficient_pointe_horaire
        }
    
    def calculer_dotation_par_type(self, type_consommation: str) -> float:
        """
        Récupère la dotation selon le type de consommation.
        
        Args:
            type_consommation: Type de consommation
            
        Returns:
            float: Dotation en litres par habitant et par jour
        """
        dotations = {
            "branchement_prive": 150,
            "borne_fontaine": 50,
            "zone_industrielle": 200,
            "zone_commerciale": 100,
            "etablissement_scolaire": 30,
            "hopital": 500,
            "zone_agricole": 100
        }
        
        return dotations.get(type_consommation, 150)
    
    def calculer_besoin_complet(self, population: int, dotation_l_hab_j: float = None,
                               coefficient_pointe_journaliere: float = 1.5,
                               coefficient_pointe_horaire: float = 2.0,
                               rendement_technique: float = 0.85) -> Dict[str, Any]:
        """
        Calcule le besoin complet en eau.
        
        Args:
            population: Nombre d'habitants
            dotation_l_hab_j: Dotation en litres par habitant et par jour
            coefficient_pointe_journaliere: Coefficient de pointe journalière
            coefficient_pointe_horaire: Coefficient de pointe horaire
            rendement_technique: Rendement technique du réseau
            
        Returns:
            Dict: Résultats complets
        """
        if dotation_l_hab_j is None:
            dotation_l_hab_j = self.calculer_dotation_par_type("branchement_prive")
        
        # Calculs en cascade
        resultat_domestique = self.calculer_besoin_domestique(population, dotation_l_hab_j)
        resultat_annexe = self.calculer_besoin_annexe(resultat_domestique['besoin_domestique_m3j'])
        resultat_global = self.calculer_besoin_global(
            resultat_domestique['besoin_domestique_m3j'],
            resultat_annexe['besoin_annexe_m3j']
        )
        resultat_pointe = self.calculer_besoin_pointe(
            resultat_global['besoin_global_m3j'],
            coefficient_pointe_journaliere
        )
        resultat_brut = self.calculer_besoin_brut(
            resultat_pointe['besoin_pointe_m3j'],
            rendement_technique
        )
        resultat_debit = self.calculer_debit_pointe_horaire(
            resultat_brut['besoin_brut_m3j'],
            coefficient_pointe_horaire
        )
        
        return {
            "population": population,
            "dotation_l_hab_j": dotation_l_hab_j,
            "coefficient_pointe_journaliere": coefficient_pointe_journaliere,
            "coefficient_pointe_horaire": coefficient_pointe_horaire,
            "rendement_technique": rendement_technique,
            **resultat_domestique,
            **resultat_annexe,
            **resultat_global,
            **resultat_pointe,
            **resultat_brut,
            **resultat_debit
        }

# =============================================================================
# FONCTIONS D'INTERFACE POUR CLI/REPL
# =============================================================================

def calculate_water_demand_unified(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule les besoins en eau pour une population.
    
    Cette fonction fusionne les fonctionnalités de demand.py et population_unified.py.
    
    Args:
        data: Dictionnaire contenant les données de demande
            - population: Nombre d'habitants
            - dotation_l_j_hab: Dotation en L/hab/j
            - coefficient_pointe: Coefficient de pointe
            - verbose: Afficher les détails
    
    Returns:
        Dictionnaire avec les résultats du calcul
    """
    try:
        # Validation des données avec le validateur unifié
        from ..core.validators import validate_demand_unified_data
        data = validate_demand_unified_data(data)
        
        # Extraction des paramètres validés
        population = data["population"]
        dotation_l_j_hab = data["dotation_l_j_hab"]
        coefficient_pointe = data["coefficient_pointe"]
        verbose = data.get("verbose", False)
        
        # Initialiser le calculateur
        calc = DemandCalculationsUnified()
        
        # Calcul complet des besoins
        resultat = calc.calculer_besoin_complet(
            population=population,
            dotation_l_hab_j=dotation_l_j_hab,
            coefficient_pointe_journaliere=coefficient_pointe
        )
        
        # Ajouter le statut et la méthode
        resultat_final = {
            "statut": "SUCCES",
            "methode": "branchement_prive",
            **resultat
        }
        
        if verbose:
            print(f"💧 Demande en eau:")
            if 'besoin_brut_m3j' in resultat:
                print(f"   Besoin brut: {resultat['besoin_brut_m3j']:.1f} m³/j")
            if 'debit_pointe_m3s' in resultat:
                print(f"   Débit pointe: {resultat['debit_pointe_m3s']:.3f} m³/s")
        
        return resultat_final
        
    except AEPValidationError as e:
        return {
            "statut": "ERREUR_VALIDATION",
            "message": str(e)
        }
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors du calcul de demande: {str(e)}"
        }

def calculate_water_demand_by_type_unified(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule les besoins en eau selon le type de consommation.
    
    Args:
        data: Dictionnaire contenant les données
        
    Returns:
        Dict: Résultats du calcul
    """
    try:
        population = data.get("population", 1000)
        type_consommation = data.get("type_consommation", "branchement_prive")
        coefficient_pointe = data.get("coefficient_pointe", 1.5)
        
        calc = DemandCalculationsUnified()
        dotation = calc.calculer_dotation_par_type(type_consommation)
        
        resultat = calc.calculer_besoin_complet(
            population, dotation, coefficient_pointe
        )
        
        return {
            **resultat,
            "type_consommation": type_consommation
        }
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors du calcul: {str(e)}"
        }

def compare_water_demand_scenarios_unified(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare différents scénarios de demande en eau.
    
    Args:
        data: Dictionnaire contenant les données
        
    Returns:
        Dict: Comparaison des scénarios
    """
    try:
        population = data.get("population", 1000)
        scenarios = data.get("scenarios", [
            {"type": "branchement_prive", "coefficient_pointe": 1.5},
            {"type": "borne_fontaine", "coefficient_pointe": 1.8},
            {"type": "zone_industrielle", "coefficient_pointe": 1.3}
        ])
        
        calc = DemandCalculationsUnified()
        resultats = {}
        
        for i, scenario in enumerate(scenarios):
            dotation = calc.calculer_dotation_par_type(scenario["type"])
            resultat = calc.calculer_besoin_complet(
                population, dotation, scenario["coefficient_pointe"]
            )
            resultats[f"scenario_{i+1}"] = {
                **resultat,
                "type_consommation": scenario["type"]
            }
        
        # Analyse comparative
        besoins_bruts = [r['besoin_brut_m3j'] for r in resultats.values()]
        
        resultats['analyse'] = {
            'besoin_min': min(besoins_bruts),
            'besoin_max': max(besoins_bruts),
            'ecart_relatif': (max(besoins_bruts) - min(besoins_bruts)) / min(besoins_bruts) * 100
        }
        
        return resultats
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors de la comparaison: {str(e)}"
        }

def get_demand_unified_help() -> str:
    """
    Retourne l'aide pour le module demande unifié.
    
    Returns:
        str: Texte d'aide
    """
    return """
💧 MODULE DEMANDE UNIFIÉ AEP

Ce module fusionne les fonctionnalités de demand.py et population_unified.py
pour offrir une version complète avec transparence mathématique.

📋 FONCTIONS DISPONIBLES:

🔢 CALCUL BESOINS
  calculate_water_demand_unified(data) - Calcul complet des besoins en eau
  - Besoin domestique, annexe, global, pointe, brut
  - Coefficients de pointe configurables
  - Validation automatique des données
  - Transparence mathématique

🏢 TYPES DE CONSOMMATION
  calculate_water_demand_by_type_unified(data) - Calcul par type
  - Branchement privé, borne fontaine, zone industrielle
  - Dotations spécifiques par type
  - Recommandations intégrées

🔍 COMPARAISON
  compare_water_demand_scenarios_unified(data) - Compare les scénarios
  - Analyse comparative des besoins
  - Identification du scénario optimal
  - Recommandations de dimensionnement

📝 EXEMPLES:
  data = {"population": 1000, "dotation_l_j_hab": 150}
  result = calculate_water_demand_unified(data)
  
  data = {"population": 1000, "type_consommation": "zone_industrielle"}
  result = calculate_water_demand_by_type_unified(data)
"""

# =============================================================================
# EXPORTS PRINCIPAUX
# =============================================================================

__all__ = [
    'DemandCalculationsUnified',
    'calculate_water_demand_unified',
    'calculate_water_demand_by_type_unified',
    'compare_water_demand_scenarios_unified',
    'get_demand_unified_help'
] 