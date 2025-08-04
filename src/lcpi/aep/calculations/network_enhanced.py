"""
Module de calculs réseau amélioré intégrant les formules de AMELIORATION.
Inclut la transparence mathématique et les explications pédagogiques.
"""

import math
import json
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

from ..core.mathematical_transparency import math_transparency
from ..core.constants import *
from ..core.formulas import *

class NetworkCalculationsEnhanced:
    """
    Classe pour les calculs réseau améliorés avec transparence mathématique.
    Intègre les formules de AMELIORATION/calcul_adduction.py et calcul_distribution.py
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialise le calculateur réseau.
        
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
    
    def get_rugosite_absolue(self, materiau: str) -> float:
        """
        Récupère la rugosité absolue d'un matériau.
        
        Args:
            materiau: Nom du matériau
            
        Returns:
            float: Rugosité absolue en mètres
        """
        try:
            for item in self.db.get('coefficients_rugosite', {}).get('rugosite_absolue_e_mm', []):
                if item['materiau'].lower() == materiau.lower():
                    return item['valeur_mm'] / 1000.0  # Conversion mm → m
        except:
            pass
        
        # Valeurs par défaut si pas trouvé dans la DB
        rugosites_defaut = {
            'fonte': 0.25,
            'acier': 0.045,
            'pvc': 0.0015,
            'pe': 0.001
        }
        return rugosites_defaut.get(materiau.lower(), 0.1)
    
    def get_manning_coefficient(self, materiau: str, etat: str = 'bon') -> float:
        """
        Récupère le coefficient de Manning.
        
        Args:
            materiau: Matériau de la conduite
            etat: État de la conduite ('bon', 'moyen', 'mauvais')
            
        Returns:
            float: Coefficient de Manning
        """
        try:
            for item in self.db.get('coefficients_rugosite', {}).get('manning_n', []):
                if materiau.lower() in item['nature_parois'].lower():
                    return item.get(etat.lower(), item.get('bon', 0.013))
        except:
            pass
        
        # Valeurs par défaut
        coefficients_defaut = {
            'fonte': {'bon': 0.013, 'moyen': 0.015, 'mauvais': 0.017},
            'acier': {'bon': 0.012, 'moyen': 0.014, 'mauvais': 0.016},
            'pvc': {'bon': 0.009, 'moyen': 0.010, 'mauvais': 0.011}
        }
        return coefficients_defaut.get(materiau.lower(), {}).get(etat.lower(), 0.013)
    
    def get_hazen_williams_coefficient(self, materiau: str, etat: str = 'neuve') -> float:
        """
        Récupère le coefficient de Hazen-Williams.
        
        Args:
            materiau: Matériau de la conduite
            etat: État de la conduite ('neuve', 'bon', 'moyen', 'mauvais')
            
        Returns:
            float: Coefficient de Hazen-Williams
        """
        try:
            for item in self.db.get('coefficients_rugosite', {}).get('hazen_williams_C', []):
                if (item['materiau'].lower() == materiau.lower() and 
                    item['etat'].lower() == etat.lower()):
                    return item['valeur']
        except:
            pass
        
        # Valeurs par défaut
        coefficients_defaut = {
            'fonte': {'neuve': 130, 'bon': 110, 'moyen': 90, 'mauvais': 70},
            'acier': {'neuve': 140, 'bon': 120, 'moyen': 100, 'mauvais': 80},
            'pvc': {'neuve': 150, 'bon': 140, 'moyen': 130, 'mauvais': 120}
        }
        return coefficients_defaut.get(materiau.lower(), {}).get(etat.lower(), 100)
    
    def calculer_vitesse(self, debit_m3s: float, diametre_m: float) -> float:
        """
        Calcule la vitesse d'écoulement.
        
        Args:
            debit_m3s: Débit en m³/s
            diametre_m: Diamètre en mètres
            
        Returns:
            float: Vitesse en m/s
        """
        aire = math.pi * (diametre_m / 2)**2
        return debit_m3s / aire
    
    def calculer_reynolds(self, debit_m3s: float, diametre_m: float) -> float:
        """
        Calcule le nombre de Reynolds.
        
        Args:
            debit_m3s: Débit en m³/s
            diametre_m: Diamètre en mètres
            
        Returns:
            float: Nombre de Reynolds
        """
        vitesse = self.calculer_vitesse(debit_m3s, diametre_m)
        return (vitesse * diametre_m) / VISCOSITE_CINEMATIQUE_EAU
    
    def calculer_colebrook_lambda(self, reynolds: float, diametre_m: float, materiau: str) -> float:
        """
        Calcule le coefficient de friction λ par la méthode de Colebrook-White.
        
        Args:
            reynolds: Nombre de Reynolds
            diametre_m: Diamètre en mètres
            materiau: Matériau de la conduite
            
        Returns:
            float: Coefficient de friction λ
        """
        if reynolds < 2300:  # Régime laminaire
            return 64 / reynolds
            
        e = self.get_rugosite_absolue(materiau)
        eD = e / diametre_m
        
        # Estimation initiale avec la formule de Haaland
        lambda_i = (1 / (-1.8 * math.log10((eD / 3.7)**1.11 + 6.9 / reynolds)))**2
        
        # Itérations pour affiner la valeur
        for _ in range(10):
            terme1 = eD / 3.7
            terme2 = 2.51 / (reynolds * math.sqrt(lambda_i))
            lambda_new = (1 / (-2 * math.log10(terme1 + terme2)))**2
            if abs(lambda_new - lambda_i) < 1e-6:
                return lambda_new
            lambda_i = lambda_new
        return lambda_i
    
    def perte_de_charge_darcy_weisbach(self, debit_m3s: float, diametre_m: float, 
                                      longueur_m: float, materiau: str) -> Dict[str, float]:
        """
        Calcule la perte de charge par la formule de Darcy-Weisbach.
        
        Args:
            debit_m3s: Débit en m³/s
            diametre_m: Diamètre en mètres
            longueur_m: Longueur en mètres
            materiau: Matériau de la conduite
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        # Calculs
        re = self.calculer_reynolds(debit_m3s, diametre_m)
        lambda_f = self.calculer_colebrook_lambda(re, diametre_m, materiau)
        vitesse = self.calculer_vitesse(debit_m3s, diametre_m)
        delta_h = lambda_f * (longueur_m / diametre_m) * (vitesse**2 / (2 * G_ACCELERATION_GRAVITE))
        
        # Transparence mathématique
        explanation = math_transparency.display_formula("darcy_weisbach", {
            "λ": lambda_f,
            "L": longueur_m,
            "D": diametre_m,
            "V": vitesse,
            "g": G_ACCELERATION_GRAVITE
        })
        
        return {
            "perte_charge": delta_h,
            "vitesse": vitesse,
            "reynolds": re,
            "lambda": lambda_f,
            "explication": explanation
        }
    
    def perte_de_charge_manning_strickler(self, debit_m3s: float, diametre_m: float,
                                         longueur_m: float, materiau: str, etat: str = 'bon') -> Dict[str, float]:
        """
        Calcule la perte de charge par la formule de Manning-Strickler.
        
        Args:
            debit_m3s: Débit en m³/s
            diametre_m: Diamètre en mètres
            longueur_m: Longueur en mètres
            materiau: Matériau de la conduite
            etat: État de la conduite
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        n = self.get_manning_coefficient(materiau, etat)
        ks = 1 / n  # Coefficient de Strickler
        vitesse = self.calculer_vitesse(debit_m3s, diametre_m)
        rh = diametre_m / 4  # Rayon hydraulique pour conduite circulaire
        
        # Formule réarrangée pour trouver la perte de charge
        j = (vitesse / (ks * rh**(2/3)))**2
        delta_h = j * longueur_m
        
        return {
            "perte_charge": delta_h,
            "vitesse": vitesse,
            "coefficient_manning": n,
            "coefficient_strickler": ks,
            "rayon_hydraulique": rh,
            "pente_hydraulique": j
        }
    
    def perte_de_charge_hazen_williams(self, debit_m3s: float, diametre_m: float,
                                      longueur_m: float, materiau: str, etat: str = 'neuve') -> Dict[str, float]:
        """
        Calcule la perte de charge par la formule de Hazen-Williams.
        
        Args:
            debit_m3s: Débit en m³/s
            diametre_m: Diamètre en mètres
            longueur_m: Longueur en mètres
            materiau: Matériau de la conduite
            etat: État de la conduite
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        C = self.get_hazen_williams_coefficient(materiau, etat)
        
        # Formule de débit réarrangée pour ΔH/L
        j = (debit_m3s / (0.2785 * C * diametre_m**2.63))**(1/0.54)
        delta_h = j * longueur_m
        
        return {
            "perte_charge": delta_h,
            "coefficient_hazen_williams": C,
            "pente_hydraulique": j
        }
    
    def perte_de_charge_flamant(self, debit_m3s: float, diametre_m: float, longueur_m: float) -> Dict[str, float]:
        """
        Calcule la perte de charge par la formule de Flamant.
        
        Args:
            debit_m3s: Débit en m³/s
            diametre_m: Diamètre en mètres
            longueur_m: Longueur en mètres
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        # Formule de Flamant : j = 0.001404043 × Q^1.75 / D^4.75
        j = 0.001404043 * (debit_m3s**1.75) / (diametre_m**4.75)
        delta_h = j * longueur_m
        
        explanation = math_transparency.display_formula("flamant_perte_charge", {
            "Q": debit_m3s,
            "D": diametre_m
        })
        
        return {
            "perte_charge": delta_h,
            "pente_hydraulique": j,
            "explication": explanation
        }
    
    def dimensionner_conduite(self, debit_m3s: float, longueur_m: float, materiau: str,
                            perte_charge_max_m: float, methode: str = 'darcy') -> Dict[str, Any]:
        """
        Dimensionne une conduite selon différentes méthodes.
        
        Args:
            debit_m3s: Débit en m³/s
            longueur_m: Longueur en mètres
            materiau: Matériau de la conduite
            perte_charge_max_m: Perte de charge maximale autorisée
            methode: Méthode de calcul ('darcy', 'manning', 'hazen', 'flamant')
            
        Returns:
            Dict: Résultats du dimensionnement
        """
        # Diamètres standards à tester (en mm)
        diametres_test = [50, 63, 75, 90, 110, 125, 140, 160, 180, 200, 225, 250, 280, 315, 355, 400, 450, 500]
        
        resultats = {}
        
        for diametre_mm in diametres_test:
            diametre_m = diametre_mm / 1000.0
            
            if methode == 'darcy':
                resultat = self.perte_de_charge_darcy_weisbach(debit_m3s, diametre_m, longueur_m, materiau)
            elif methode == 'manning':
                resultat = self.perte_de_charge_manning_strickler(debit_m3s, diametre_m, longueur_m, materiau)
            elif methode == 'hazen':
                resultat = self.perte_de_charge_hazen_williams(debit_m3s, diametre_m, longueur_m, materiau)
            elif methode == 'flamant':
                resultat = self.perte_de_charge_flamant(debit_m3s, diametre_m, longueur_m)
            else:
                raise ValueError(f"Méthode '{methode}' non reconnue")
            
            if resultat['perte_charge'] <= perte_charge_max_m:
                resultats['diametre_optimal_mm'] = diametre_mm
                resultats['diametre_optimal_m'] = diametre_m
                resultats['perte_charge_m'] = resultat['perte_charge']
                resultats['vitesse_ms'] = resultat.get('vitesse', 0)
                resultats['methode'] = methode
                resultats['materiau'] = materiau
                resultats['explication'] = resultat.get('explication', '')
                break
        
        if not resultats:
            resultats['erreur'] = f"Aucun diamètre trouvé pour respecter la perte de charge maximale de {perte_charge_max_m} m"
        
        return resultats
    
    def comparer_methodes(self, debit_m3s: float, diametre_m: float, longueur_m: float, 
                         materiau: str) -> Dict[str, Any]:
        """
        Compare les différentes méthodes de calcul de perte de charge.
        
        Args:
            debit_m3s: Débit en m³/s
            diametre_m: Diamètre en mètres
            longueur_m: Longueur en mètres
            materiau: Matériau de la conduite
            
        Returns:
            Dict: Comparaison des méthodes
        """
        resultats = {}
        
        # Darcy-Weisbach
        resultats['darcy'] = self.perte_de_charge_darcy_weisbach(debit_m3s, diametre_m, longueur_m, materiau)
        
        # Manning-Strickler
        resultats['manning'] = self.perte_de_charge_manning_strickler(debit_m3s, diametre_m, longueur_m, materiau)
        
        # Hazen-Williams
        resultats['hazen'] = self.perte_de_charge_hazen_williams(debit_m3s, diametre_m, longueur_m, materiau)
        
        # Flamant
        resultats['flamant'] = self.perte_de_charge_flamant(debit_m3s, diametre_m, longueur_m)
        
        # Analyse comparative
        pertes = [resultats['darcy']['perte_charge'], 
                 resultats['manning']['perte_charge'], 
                 resultats['hazen']['perte_charge'],
                 resultats['flamant']['perte_charge']]
        
        resultats['analyse'] = {
            'methode_min': ['darcy', 'manning', 'hazen', 'flamant'][pertes.index(min(pertes))],
            'methode_max': ['darcy', 'manning', 'hazen', 'flamant'][pertes.index(max(pertes))],
            'ecart_relatif': (max(pertes) - min(pertes)) / min(pertes) * 100
        }
        
        return resultats
    
    def verifier_vitesse(self, vitesse_ms: float) -> Dict[str, Any]:
        """
        Vérifie si la vitesse est dans la plage admissible.
        
        Args:
            vitesse_ms: Vitesse en m/s
            
        Returns:
            Dict: Résultats de la vérification
        """
        vmin = 0.5  # m/s
        vmax = 3.0  # m/s
        
        if vmin <= vitesse_ms <= vmax:
            statut = "OK"
            message = f"Vitesse {vitesse_ms:.2f} m/s dans la plage [{vmin}-{vmax}] m/s"
        else:
            statut = "HORS PLAGE"
            message = f"Vitesse {vitesse_ms:.2f} m/s hors de la plage [{vmin}-{vmax}] m/s"
        
        return {
            "statut": statut,
            "message": message,
            "vitesse": vitesse_ms,
            "vmin": vmin,
            "vmax": vmax
        }
    
    def calculer_pression_requise(self, nombre_etages: int) -> Dict[str, Any]:
        """
        Calcule la pression requise pour un nombre d'étages.
        
        Args:
            nombre_etages: Nombre d'étages
            
        Returns:
            Dict: Pression requise
        """
        # Pression de base par étage (en mCE)
        pression_base = 3.0  # mCE par étage
        pression_min = pression_base * nombre_etages
        pression_max = pression_min + 2.0  # Marge de sécurité
        
        return {
            "nombre_etages": nombre_etages,
            "pression_min_mce": pression_min,
            "pression_max_mce": pression_max,
            "pression_recommandee_mce": (pression_min + pression_max) / 2
        }

# Fonctions d'interface pour compatibilité avec l'API existante
def dimension_network_enhanced(data: Dict) -> Dict:
    """
    Dimensionne un réseau avec transparence mathématique.
    
    Args:
        data: Données du réseau
        
    Returns:
        Dict: Résultats du dimensionnement
    """
    calc = NetworkCalculationsEnhanced()
    
    debit = data.get('debit_m3s', 0.1)
    longueur = data.get('longueur_m', 1000)
    materiau = data.get('materiau', 'fonte')
    perte_max = data.get('perte_charge_max_m', 10.0)
    methode = data.get('methode', 'darcy')
    
    resultats = calc.dimensionner_conduite(debit, longueur, materiau, perte_max, methode)
    
    if 'erreur' not in resultats:
        # Vérification de la vitesse
        vitesse = resultats.get('vitesse_ms', 0)
        verification_vitesse = calc.verifier_vitesse(vitesse)
        resultats['verification_vitesse'] = verification_vitesse
        
        # Ajouter la transparence mathématique
        resultats['transparence'] = math_transparency.display_formula("darcy_weisbach", {
            "L": longueur,
            "D": resultats['diametre_optimal_m'],
            "V": resultats['vitesse_ms'],
            "g": G_ACCELERATION_GRAVITE
        })
    
    return resultats

def comparer_methodes_network(data: Dict) -> Dict:
    """
    Compare les méthodes de calcul de perte de charge.
    
    Args:
        data: Données du réseau
        
    Returns:
        Dict: Comparaison des méthodes
    """
    calc = NetworkCalculationsEnhanced()
    
    debit = data.get('debit_m3s', 0.1)
    diametre = data.get('diametre_m', 0.5)
    longueur = data.get('longueur_m', 1000)
    materiau = data.get('materiau', 'fonte')
    
    return calc.comparer_methodes(debit, diametre, longueur, materiau)

def verifier_vitesse_network(data: Dict) -> Dict:
    """
    Vérifie la vitesse d'écoulement.
    
    Args:
        data: Données du réseau
        
    Returns:
        Dict: Résultats de la vérification
    """
    calc = NetworkCalculationsEnhanced()
    
    debit = data.get('debit_m3s', 0.1)
    diametre = data.get('diametre_m', 0.5)
    
    vitesse = calc.calculer_vitesse(debit, diametre)
    return calc.verifier_vitesse(vitesse)

def calculer_pression_requise_network(data: Dict) -> Dict:
    """
    Calcule la pression requise.
    
    Args:
        data: Données du réseau
        
    Returns:
        Dict: Pression requise
    """
    calc = NetworkCalculationsEnhanced()
    
    nombre_etages = data.get('nombre_etages', 4)
    return calc.calculer_pression_requise(nombre_etages) 