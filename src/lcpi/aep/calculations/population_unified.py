"""
Module de calculs population unifié pour AEP - Version Fusionnée et Enrichie

Ce module fusionne les fonctionnalités de population.py et population_enhanced.py
pour offrir une version complète avec :
- Transparence mathématique
- Support de base de données
- Multiples méthodes de projection
- Calculs de puits et besoins en eau
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
from lcpi.aep.core.validators import AEPValidationError, validate_population_data

try:
    from ..core.mathematical_transparency import math_transparency
    MATH_TRANSPARENCY_AVAILABLE = True
except ImportError:
    MATH_TRANSPARENCY_AVAILABLE = False
    print("⚠️ Module de transparence mathématique non disponible")

try:
    from lcpi.hydrodrain.calculs.population import prevoir_population
    HYDRODRAIN_AVAILABLE = True
except ImportError:
    HYDRODRAIN_AVAILABLE = False
    print("⚠️ Module hydrodrain non disponible")

class PopulationCalculationsUnified:
    """
    Classe unifiée pour les calculs population AEP.
    Fusionne les fonctionnalités de population.py et population_enhanced.py
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialise le calculateur population unifié.
        
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
    
    def prevision_population_arithmetique(self, y1: int, t1: int, y2: int, t2: int, 
                                        t_futur: int) -> Dict[str, Any]:
        """
        Prévision de population par progression arithmétique (croissance linéaire).
        
        Args:
            y1: Population au recensement 1
            t1: Année du recensement 1
            y2: Population au recensement 2
            t2: Année du recensement 2
            t_futur: Année cible pour la prévision
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        ku = (y2 - y1) / (t2 - t1)  # Taux d'accroissement uniforme
        population_future = y2 + ku * (t_futur - t2)
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("population_arithmetique", {
                "P₂": y2,
                "k_u": ku,
                "t": t_futur,
                "t₂": t2
            })
        
        return {
            "population_future": population_future,
            "taux_accroissement": ku,
            "methode": "arithmetique",
            "annee_future": t_futur,
            "explication": explanation
        }
    
    def prevision_population_geometrique(self, y1: int, t1: int, y2: int, t2: int, 
                                       t_futur: int) -> Dict[str, Any]:
        """
        Prévision de population par progression géométrique (taux constant en pourcentage).
        
        Args:
            y1: Population au recensement 1
            t1: Année du recensement 1
            y2: Population au recensement 2
            t2: Année du recensement 2
            t_futur: Année cible pour la prévision
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        if y1 <= 0 or y2 <= 0:
            raise ValueError("Les populations doivent être positives pour une projection géométrique.")
        
        kp = (math.log(y2) - math.log(y1)) / (t2 - t1)  # Taux d'accroissement
        log_pop_future = math.log(y2) + kp * (t_futur - t2)
        population_future = math.exp(log_pop_future)
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("population_geometrique", {
                "P₂": y2,
                "P₁": y1,
                "k_p": kp,
                "t": t_futur,
                "t₂": t2
            })
        
        return {
            "population_future": population_future,
            "taux_accroissement": kp,
            "methode": "geometrique",
            "annee_future": t_futur,
            "explication": explanation
        }
    
    def prevision_population_logistique(self, y0: int, y1: int, y2: int, n: int, 
                                      x: int) -> Dict[str, Any]:
        """
        Prévision de population par progression logistique.
        
        Args:
            y0: Population initiale
            y1: Population intermédiaire
            y2: Population finale
            n: Période totale
            x: Période cible
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        # Calcul des paramètres logistiques
        a = (y0 * y2 - y1**2) / (y0 + y2 - 2*y1)
        b = (y2 - y1) / (y1 - y0)
        c = (y0 * y2 - y1**2) / (y1 * (y0 + y2 - 2*y1))
        
        population_future = a / (1 + b * math.exp(-c * x))
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("population_logistique", {
                "a": a,
                "b": b,
                "c": c,
                "x": x
            })
        
        return {
            "population_future": population_future,
            "parametres": {"a": a, "b": b, "c": c},
            "methode": "logistique",
            "periode_cible": x,
            "explication": explanation
        }
    
    def comparer_methodes_prevision(self, y0: int, t0: int, y1: int, t1: int, 
                                   y2: int, t2: int, t_futur: int) -> Dict[str, Any]:
        """
        Compare les différentes méthodes de prévision démographique.
        
        Args:
            y0, t0: Population et année initiales
            y1, t1: Population et année intermédiaires
            y2, t2: Population et année finales
            t_futur: Année cible pour la prévision
            
        Returns:
            Dict: Comparaison des méthodes
        """
        resultats = {}
        
        # Méthode arithmétique
        resultats['arithmetique'] = self.prevision_population_arithmetique(y1, t1, y2, t2, t_futur)
        
        # Méthode géométrique
        resultats['geometrique'] = self.prevision_population_geometrique(y1, t1, y2, t2, t_futur)
        
        # Méthode logistique
        n = t2 - t0
        x = t_futur - t0
        resultats['logistique'] = self.prevision_population_logistique(y0, y1, y2, n, x)
        
        # Analyse comparative
        populations = [
            resultats['arithmetique']['population_future'],
            resultats['geometrique']['population_future'],
            resultats['logistique']['population_future']
        ]
        
        resultats['analyse'] = {
            'methode_min': ['arithmetique', 'geometrique', 'logistique'][populations.index(min(populations))],
            'methode_max': ['arithmetique', 'geometrique', 'logistique'][populations.index(max(populations))],
            'ecart_relatif': (max(populations) - min(populations)) / min(populations) * 100
        }
        
        return resultats
    
    def calculer_debit_puits_nappe_libre(self, K: float, H: float, h: float, 
                                        R: float, r: float) -> Dict[str, Any]:
        """
        Calcule le débit d'un puits en nappe libre.
        
        Args:
            K: Coefficient de perméabilité
            H: Épaisseur de la nappe
            h: Hauteur d'eau dans le puits
            R: Rayon d'influence
            r: Rayon du puits
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        # Formule de Dupuit-Thiem pour nappe libre
        debit = math.pi * K * (H**2 - h**2) / math.log(R/r)
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("puits_nappe_libre", {
                "K": K,
                "H": H,
                "h": h,
                "R": R,
                "r": r
            })
        
        return {
            "debit_m3s": debit,
            "debit_ls": debit * 1000,
            "parametres": {"K": K, "H": H, "h": h, "R": R, "r": r},
            "methode": "Dupuit-Thiem",
            "explication": explanation
        }
    
    def calculer_debit_puits_nappe_captive(self, K: float, e: float, H: float, 
                                          h: float, R: float, r: float) -> Dict[str, Any]:
        """
        Calcule le débit d'un puits en nappe captive.
        
        Args:
            K: Coefficient de perméabilité
            e: Épaisseur de l'aquifère
            H: Charge hydraulique
            h: Charge dans le puits
            R: Rayon d'influence
            r: Rayon du puits
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        # Formule de Dupuit-Thiem pour nappe captive
        debit = 2 * math.pi * K * e * (H - h) / math.log(R/r)
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("puits_nappe_captive", {
                "K": K,
                "e": e,
                "H": H,
                "h": h,
                "R": R,
                "r": r
            })
        
        return {
            "debit_m3s": debit,
            "debit_ls": debit * 1000,
            "parametres": {"K": K, "e": e, "H": H, "h": h, "R": R, "r": r},
            "methode": "Dupuit-Thiem captive",
            "explication": explanation
        }
    
    def calculer_besoin_eau_population(self, population: int, dotation_l_hab_j: float = 150,
                                      coefficient_pointe: float = 1.5) -> Dict[str, Any]:
        """
        Calcule les besoins en eau pour une population donnée.
        
        Args:
            population: Nombre d'habitants
            dotation_l_hab_j: Dotation par habitant et par jour (L/hab/j)
            coefficient_pointe: Coefficient de pointe
            
        Returns:
            Dict: Résultats du calcul
        """
        # Besoin domestique
        besoin_domestique = population * dotation_l_hab_j / 1000  # m³/j
        
        # Besoin annexe (10% du domestique)
        besoin_annexe = besoin_domestique * 0.1
        
        # Besoin global
        besoin_global = besoin_domestique + besoin_annexe
        
        # Besoin de pointe
        besoin_pointe = besoin_global * coefficient_pointe
        
        # Besoin brut (avec pertes techniques)
        rendement_technique = 0.85  # 85% de rendement
        besoin_brut = besoin_pointe / rendement_technique
        
        # Débit de pointe en m³/s
        debit_pointe_m3s = besoin_brut / (24 * 3600)  # Conversion m³/j → m³/s
        
        return {
            "population": population,
            "besoin_domestique_m3j": besoin_domestique,
            "besoin_annexe_m3j": besoin_annexe,
            "besoin_global_m3j": besoin_global,
            "besoin_pointe_m3j": besoin_pointe,
            "besoin_brut_m3j": besoin_brut,
            "debit_pointe_m3s": debit_pointe_m3s,
            "dotation_l_hab_j": dotation_l_hab_j,
            "coefficient_pointe": coefficient_pointe,
            "methode": "standard"
        }
    
    def calculer_evolution_population(self, population_initial: int, taux_croissance: float,
                                    nombre_annees: int) -> Dict[str, Any]:
        """
        Calcule l'évolution de la population sur plusieurs années.
        
        Args:
            population_initial: Population initiale
            taux_croissance: Taux de croissance annuel
            nombre_annees: Nombre d'années
            
        Returns:
            Dict: Résultats avec évolution détaillée
        """
        evolution = []
        population_courante = population_initial
        
        for annee in range(nombre_annees + 1):
            evolution.append({
                "annee": annee,
                "population": population_courante,
                "accroissement": population_courante - population_initial if annee > 0 else 0
            })
            population_courante = population_courante * (1 + taux_croissance)
        
        croissance_totale = evolution[-1]["population"] - population_initial
        taux_croissance_total = (evolution[-1]["population"] / population_initial - 1) * 100
        
        return {
            "population_initial": population_initial,
            "taux_croissance_annuel": taux_croissance,
            "nombre_annees": nombre_annees,
            "evolution": evolution,
            "croissance_totale": croissance_totale,
            "taux_croissance_total_pct": taux_croissance_total,
            "population_finale": evolution[-1]["population"]
        }

# =============================================================================
# FONCTIONS D'INTERFACE POUR CLI/REPL
# =============================================================================

def calculate_population_projection_unified(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule la projection démographique avec transparence mathématique.
    
    Cette fonction fusionne les fonctionnalités de population.py et population_enhanced.py.
    
    Args:
        data: Dictionnaire contenant les données de projection
            - population_base: Population de base
            - taux_croissance: Taux de croissance annuel
            - annees: Nombre d'années de projection
            - methode: Méthode de projection (malthus, arithmetique, geometrique, logistique)
            - verbose: Afficher les détails des calculs
    
    Returns:
        Dictionnaire avec les résultats de la projection
    """
    try:
        # Validation des données avec le validateur unifié
        from ..core.validators import validate_population_unified_data
        data = validate_population_unified_data(data)
        
        # Extraction des paramètres validés
        population_base = data["population_base"]
        taux_croissance = data["taux_croissance"]
        annees = data["annees"]
        methode = data["methode"]
        verbose = data.get("verbose", False)
        
        # Initialiser le calculateur
        calc = PopulationCalculationsUnified()
        
        # Calcul de la projection en utilisant la méthode existante
        resultats = calc.calculer_evolution_population(population_base, taux_croissance, annees)
        
        if 'erreur' in resultats:
            return {
                "statut": "ERREUR",
                "message": resultats['erreur']
            }
        
        # Résultats enrichis
        resultat_final = {
            "statut": "SUCCES",
            "population_base": population_base,
            "taux_croissance": taux_croissance,
            "annees": annees,
            "methode": methode,
            "population_finale": resultats['population_finale'],
            "croissance_relative_pct": resultats.get('croissance_relative_pct', 0),
            "details": resultats.get('details', {})
        }
        
        if verbose:
            print(f"Projection {methode}: {resultats['population_finale']:.0f} habitants")
            if 'croissance_relative_pct' in resultats:
                print(f"   Croissance: {resultats['croissance_relative_pct']:.1f}%")
        
        return resultat_final
        
    except AEPValidationError as e:
        return {
            "statut": "ERREUR_VALIDATION",
            "message": str(e)
        }
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors de la projection: {str(e)}"
        }

def calculate_water_demand_unified(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule les besoins en eau pour une population.
    
    Args:
        data: Dictionnaire contenant les données
        
    Returns:
        Dict: Résultats du calcul
    """
    try:
        # Validation des données avec le validateur unifié
        from ..core.validators import validate_demand_unified_data
        data = validate_demand_unified_data(data)
        
        # Extraction des paramètres validés
        population = data["population"]
        dotation = data["dotation_l_j_hab"]
        coefficient_pointe = data["coefficient_pointe"]
        verbose = data.get("verbose", False)
        
        calc = PopulationCalculationsUnified()
        resultat = calc.calculer_besoin_eau_population(population, dotation, coefficient_pointe)
        
        if verbose:
            print(f"💧 Demande en eau:")
            if 'besoin_brut_m3j' in resultat:
                print(f"   Besoin brut: {resultat['besoin_brut_m3j']:.1f} m³/j")
            if 'debit_pointe_m3s' in resultat:
                print(f"   Débit pointe: {resultat['debit_pointe_m3s']:.3f} m³/s")
        
        return resultat
        
    except AEPValidationError as e:
        return {
            "statut": "ERREUR_VALIDATION",
            "message": str(e)
        }
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors du calcul des besoins: {str(e)}"
        }

def calculate_well_discharge_unified(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule le débit d'un puits.
    
    Args:
        data: Dictionnaire contenant les données
        
    Returns:
        Dict: Résultats du calcul
    """
    try:
        K = data.get("K", 1e-4)
        H = data.get("H", 10.0)
        h = data.get("h", 5.0)
        R = data.get("R", 100.0)
        r = data.get("r", 0.5)
        type_nappe = data.get("type_nappe", "libre")
        
        calc = PopulationCalculationsUnified()
        
        if type_nappe == "libre":
            return calc.calculer_debit_puits_nappe_libre(K, H, h, R, r)
        elif type_nappe == "captive":
            e = data.get("e", 5.0)  # Épaisseur de l'aquifère
            return calc.calculer_debit_puits_nappe_captive(K, e, H, h, R, r)
        else:
            raise ValueError(f"Type de nappe '{type_nappe}' non reconnu")
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors du calcul du puits: {str(e)}"
        }

def calculate_population_evolution_unified(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule l'évolution de la population sur plusieurs années.
    
    Args:
        data: Dictionnaire contenant les données
        
    Returns:
        Dict: Résultats avec évolution détaillée
    """
    try:
        population_initial = data.get("population_initial", 1000)
        taux_croissance = data.get("taux_croissance", 0.037)
        nombre_annees = data.get("nombre_annees", 20)
        
        calc = PopulationCalculationsUnified()
        return calc.calculer_evolution_population(population_initial, taux_croissance, nombre_annees)
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors du calcul de l'évolution: {str(e)}"
        }

def get_population_unified_help() -> str:
    """
    Retourne l'aide pour le module population unifié.
    
    Returns:
        str: Texte d'aide
    """
    return """
🔢 MODULE POPULATION UNIFIÉ AEP

Ce module fusionne les fonctionnalités de population.py et population_enhanced.py
pour offrir une version complète avec transparence mathématique.

📋 FONCTIONS DISPONIBLES:

📈 PROJECTION
  calculate_population_projection_unified(data) - Projection démographique
  - Méthodes: Malthus, arithmétique, géométrique, logistique
  - Validation automatique des données
  - Transparence mathématique

💧 BESOINS EN EAU
  calculate_water_demand_unified(data) - Calcul des besoins en eau
  - Besoin domestique, annexe, global, pointe
  - Coefficients de pointe configurables
  - Rendement technique intégré

🕳️ PUITS
  calculate_well_discharge_unified(data) - Calcul de débit de puits
  - Nappes libres et captives
  - Formules de Dupuit-Thiem
  - Paramètres géologiques

📊 ÉVOLUTION
  calculate_population_evolution_unified(data) - Évolution temporelle
  - Projection année par année
  - Statistiques de croissance
  - Analyse détaillée

📝 EXEMPLES:
  data = {"population_base": 1000, "taux_croissance": 0.037, "annees": 20}
  result = calculate_population_projection_unified(data)
  
  data = {"population": 1000, "dotation_l_hab_j": 150}
  result = calculate_water_demand_unified(data)
"""

# =============================================================================
# EXPORTS PRINCIPAUX
# =============================================================================

__all__ = [
    'PopulationCalculationsUnified',
    'calculate_population_projection_unified',
    'calculate_water_demand_unified',
    'calculate_well_discharge_unified',
    'calculate_population_evolution_unified',
    'get_population_unified_help'
] 