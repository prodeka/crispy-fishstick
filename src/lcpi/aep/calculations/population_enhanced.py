"""
Module de calculs population amélioré intégrant les formules de AMELIORATION.
Inclut la transparence mathématique et les explications pédagogiques.
"""

import math
import json
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

from ..core.mathematical_transparency import math_transparency
from ..core.constants import *
from ..core.formulas import *

class PopulationCalculationsEnhanced:
    """
    Classe pour les calculs population améliorés avec transparence mathématique.
    Intègre les formules de AMELIORATION/production_pop.py
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialise le calculateur population.
        
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
        explanation = math_transparency.display_formula("population_geometrique", {
            "P₂": y2,
            "P₁": y1,
            "t": t_futur,
            "t₂": t2,
            "t₁": t1
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
        Prévision de population par méthode logistique (courbe en S).
        
        Args:
            y0: Population au 1er point (temps 0)
            y1: Population au 2ème point (temps n)
            y2: Population au 3ème point (temps 2n)
            n: Intervalle de temps entre les points
            x: Intervalle de temps entre le point y0 et l'année cible
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        # Calcul des constantes K, a, b
        denom_k = y0 * y2 - y1**2
        if denom_k == 0:
            raise ValueError("Division par zéro dans le calcul de K. Les points sont probablement colinéaires.")
        
        K = (2 * y0 * y1 * y2 - y1**2 * (y0 + y2)) / denom_k
        
        if K <= y0 or K <= y1 or K <= y2:
            raise ValueError("La population de saturation K est inférieure aux données. La méthode logistique n'est pas applicable.")
        
        a = math.log10((K - y0) / y0)
        
        denom_b = y1 * (K - y0)
        if denom_b == 0:
            raise ValueError("Division par zéro dans le calcul de b.")
        
        b = (1 / n) * math.log10((y0 * (K - y1)) / denom_b)
        
        # Calcul de la population future Yc
        Yc = K / (1 + 10**(a + b * x))
        
        # Transparence mathématique
        explanation = math_transparency.display_formula("population_logistique", {
            "K": K,
            "a": a,
            "b": b,
            "x": x
        })
        
        return {
            "population_future": Yc,
            "population_saturation": K,
            "parametre_a": a,
            "parametre_b": b,
            "methode": "logistique",
            "explication": explanation
        }
    
    def comparer_methodes_prevision(self, y0: int, t0: int, y1: int, t1: int, 
                                   y2: int, t2: int, t_futur: int) -> Dict[str, Any]:
        """
        Compare les différentes méthodes de prévision démographique.
        
        Args:
            y0, t0: Premier point de données
            y1, t1: Deuxième point de données
            y2, t2: Troisième point de données
            t_futur: Année cible
            
        Returns:
            Dict: Comparaison des méthodes
        """
        resultats = {}
        
        # Méthode arithmétique (utilise les 2 derniers points)
        resultats['arithmetique'] = self.prevision_population_arithmetique(y1, t1, y2, t2, t_futur)
        
        # Méthode géométrique (utilise les 2 derniers points)
        try:
            resultats['geometrique'] = self.prevision_population_geometrique(y1, t1, y2, t2, t_futur)
        except ValueError as e:
            resultats['geometrique'] = {'erreur': str(e)}
        
        # Méthode logistique (utilise les 3 points)
        try:
            n = t1 - t0  # Intervalle entre les points
            x = t_futur - t0  # Intervalle jusqu'à l'année cible
            resultats['logistique'] = self.prevision_population_logistique(y0, y1, y2, n, x)
        except ValueError as e:
            resultats['logistique'] = {'erreur': str(e)}
        
        # Analyse comparative
        populations = []
        methodes_valides = []
        
        for methode, resultat in resultats.items():
            if 'erreur' not in resultat:
                populations.append(resultat['population_future'])
                methodes_valides.append(methode)
        
        if len(populations) > 1:
            resultats['analyse'] = {
                'methode_min': methodes_valides[populations.index(min(populations))],
                'methode_max': methodes_valides[populations.index(max(populations))],
                'ecart_relatif': (max(populations) - min(populations)) / min(populations) * 100,
                'moyenne': sum(populations) / len(populations)
            }
        
        return resultats
    
    def calculer_debit_puits_nappe_libre(self, K: float, H: float, h: float, 
                                        R: float, r: float) -> Dict[str, Any]:
        """
        Calcule le débit d'un puits en nappe libre (Formule de Thiem).
        
        Args:
            K: Coeff. de perméabilité (m/s)
            H: Hauteur initiale de la nappe (m)
            h: Hauteur de l'eau dans le puits en pompage (m)
            R: Rayon d'influence du pompage (m)
            r: Rayon du puits (m)
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        if R <= r or r <= 0:
            raise ValueError("Le rayon d'influence R doit être supérieur au rayon du puits r.")
        
        Q = (K * math.pi * (H**2 - h**2)) / math.log(R / r)
        
        return {
            "debit_m3s": Q,
            "debit_m3h": Q * 3600,
            "coefficient_permeabilite": K,
            "hauteur_initial": H,
            "hauteur_pompage": h,
            "rayon_influence": R,
            "rayon_puits": r,
            "type_nappe": "libre"
        }
    
    def calculer_debit_puits_nappe_captive(self, K: float, e: float, H: float, 
                                          h: float, R: float, r: float) -> Dict[str, Any]:
        """
        Calcule le débit d'un puits en nappe captive (Formule de Thiem-Dupuit).
        
        Args:
            K: Coeff. de perméabilité (m/s)
            e: Épaisseur de la nappe captive (m)
            H: Charge piézométrique initiale (m)
            h: Charge dans le puits en pompage (m)
            R: Rayon d'influence (m)
            r: Rayon du puits (m)
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        if R <= r or r <= 0:
            raise ValueError("Le rayon d'influence R doit être supérieur au rayon du puits r.")
        
        Q = (2 * K * math.pi * e * (H - h)) / math.log(R / r)
        
        return {
            "debit_m3s": Q,
            "debit_m3h": Q * 3600,
            "coefficient_permeabilite": K,
            "epaisseur_nappe": e,
            "charge_initial": H,
            "charge_pompage": h,
            "rayon_influence": R,
            "rayon_puits": r,
            "type_nappe": "captive"
        }
    
    def calculer_besoin_eau_population(self, population: int, dotation_l_hab_j: float = 150,
                                      coefficient_pointe: float = 1.5) -> Dict[str, Any]:
        """
        Calcule le besoin en eau pour une population donnée.
        
        Args:
            population: Nombre d'habitants
            dotation_l_hab_j: Dotation par habitant en L/jour
            coefficient_pointe: Coefficient de pointe
            
        Returns:
            Dict: Besoins en eau
        """
        # Conversion L → m³
        dotation_m3_hab_j = dotation_l_hab_j / 1000
        
        # Besoin moyen journalier
        besoin_moyen_m3_j = population * dotation_m3_hab_j
        
        # Besoin de pointe
        besoin_pointe_m3_j = besoin_moyen_m3_j * coefficient_pointe
        
        # Besoin de pointe horaire
        besoin_pointe_m3_h = besoin_pointe_m3_j / 24
        
        # Transparence mathématique
        explanation = math_transparency.display_formula("besoin_domestique", {
            "P": population,
            "d_dom": dotation_l_hab_j,
            "C_pointe": coefficient_pointe
        })
        
        return {
            "population": population,
            "dotation_l_hab_j": dotation_l_hab_j,
            "coefficient_pointe": coefficient_pointe,
            "besoin_moyen_m3_j": besoin_moyen_m3_j,
            "besoin_pointe_m3_j": besoin_pointe_m3_j,
            "besoin_pointe_m3_h": besoin_pointe_m3_h,
            "explication": explanation
        }
    
    def calculer_evolution_population(self, population_initial: int, taux_croissance: float,
                                    nombre_annees: int) -> Dict[str, Any]:
        """
        Calcule l'évolution de la population sur plusieurs années.
        
        Args:
            population_initial: Population initiale
            taux_croissance: Taux de croissance annuel (en %)
            nombre_annees: Nombre d'années
            
        Returns:
            Dict: Évolution de la population
        """
        evolution = []
        population_courante = population_initial
        
        for annee in range(nombre_annees + 1):
            evolution.append({
                "annee": annee,
                "population": population_courante,
                "accroissement": population_courante - population_initial if annee > 0 else 0
            })
            
            if annee < nombre_annees:
                population_courante = population_courante * (1 + taux_croissance / 100)
        
        return {
            "population_initial": population_initial,
            "taux_croissance_pourcent": taux_croissance,
            "nombre_annees": nombre_annees,
            "evolution": evolution,
            "population_finale": population_courante
        }

# Fonctions d'interface pour compatibilité avec l'API existante
def calculate_population_projection_enhanced(data: Dict) -> Dict:
    """
    Calcule la projection de population avec transparence mathématique.
    
    Args:
        data: Données de population
        
    Returns:
        Dict: Résultats de la projection
    """
    calc = PopulationCalculationsEnhanced()
    
    y0 = data.get('population_0', 90000)
    t0 = data.get('annee_0', 1990)
    y1 = data.get('population_1', 100000)
    t1 = data.get('annee_1', 2000)
    y2 = data.get('population_2', 108000)
    t2 = data.get('annee_2', 2010)
    t_futur = data.get('annee_future', 2025)
    
    return calc.comparer_methodes_prevision(y0, t0, y1, t1, y2, t2, t_futur)

def calculate_water_demand_enhanced(data: Dict) -> Dict:
    """
    Calcule la demande en eau avec transparence mathématique.
    
    Args:
        data: Données de population et demande
        
    Returns:
        Dict: Résultats de la demande en eau
    """
    calc = PopulationCalculationsEnhanced()
    
    population = data.get('population', 10000)
    dotation = data.get('dotation_l_hab_j', 150)
    coefficient_pointe = data.get('coefficient_pointe', 1.5)
    
    return calc.calculer_besoin_eau_population(population, dotation, coefficient_pointe)

def calculate_well_discharge_enhanced(data: Dict) -> Dict:
    """
    Calcule le débit d'un puits avec transparence mathématique.
    
    Args:
        data: Données du puits
        
    Returns:
        Dict: Résultats du débit du puits
    """
    calc = PopulationCalculationsEnhanced()
    
    K = data.get('coefficient_permeabilite', 0.0005)
    H = data.get('hauteur_initial', 50)
    h = data.get('hauteur_pompage', 45)
    R = data.get('rayon_influence', 300)
    r = data.get('rayon_puits', 0.25)
    type_nappe = data.get('type_nappe', 'libre')
    
    if type_nappe == 'libre':
        return calc.calculer_debit_puits_nappe_libre(K, H, h, R, r)
    else:
        e = data.get('epaisseur_nappe', 15)
        return calc.calculer_debit_puits_nappe_captive(K, e, H, h, R, r)

def calculate_population_evolution_enhanced(data: Dict) -> Dict:
    """
    Calcule l'évolution de la population avec transparence mathématique.
    
    Args:
        data: Données d'évolution
        
    Returns:
        Dict: Résultats de l'évolution
    """
    calc = PopulationCalculationsEnhanced()
    
    population_initial = data.get('population_initial', 10000)
    taux_croissance = data.get('taux_croissance_pourcent', 2.0)
    nombre_annees = data.get('nombre_annees', 20)
    
    return calc.calculer_evolution_population(population_initial, taux_croissance, nombre_annees) 