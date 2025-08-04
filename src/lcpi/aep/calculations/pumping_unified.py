"""
Module de calculs pompage unifié pour AEP - Version Fusionnée et Enrichie

Ce module fusionne les fonctionnalités de pumping.py et pumping_enhanced.py
pour offrir une version complète avec :
- Transparence mathématique
- Support de base de données
- Multiples méthodes de dimensionnement
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
from lcpi.aep.core.validators import AEPValidationError, validate_pumping_data

try:
    from ..core.mathematical_transparency import math_transparency
    MATH_TRANSPARENCY_AVAILABLE = True
except ImportError:
    MATH_TRANSPARENCY_AVAILABLE = False
    print("⚠️ Module de transparence mathématique non disponible")

class PumpingCalculationsUnified:
    """
    Classe unifiée pour les calculs pompage AEP.
    Fusionne les fonctionnalités de pumping.py et pumping_enhanced.py
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialise le calculateur pompage unifié.
        
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
    
    def calculer_puissance_hydraulique(self, debit_m3s: float, hauteur_manometrique_m: float,
                                      masse_volumique_kg_m3: float = 1000) -> Dict[str, Any]:
        """
        Calcule la puissance hydraulique.
        
        Args:
            debit_m3s: Débit en m³/s
            hauteur_manometrique_m: Hauteur manométrique en mètres
            masse_volumique_kg_m3: Masse volumique du fluide
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        g = 9.81  # Accélération de la pesanteur en m/s²
        puissance_hydraulique_w = masse_volumique_kg_m3 * g * debit_m3s * hauteur_manometrique_m
        puissance_hydraulique_kw = puissance_hydraulique_w / 1000
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("puissance_hydraulique", {
                "ρ": masse_volumique_kg_m3,
                "g": g,
                "Q": debit_m3s,
                "H": hauteur_manometrique_m
            })
        
        return {
            "puissance_hydraulique_w": puissance_hydraulique_w,
            "puissance_hydraulique_kw": puissance_hydraulique_kw,
            "debit_m3s": debit_m3s,
            "hauteur_manometrique_m": hauteur_manometrique_m,
            "masse_volumique_kg_m3": masse_volumique_kg_m3,
            "explication": explanation
        }
    
    def calculer_puissance_electrique(self, puissance_hydraulique_w: float, 
                                     rendement_pompe: float = 0.75) -> Dict[str, Any]:
        """
        Calcule la puissance électrique nécessaire.
        
        Args:
            puissance_hydraulique_w: Puissance hydraulique en W
            rendement_pompe: Rendement de la pompe (0-1)
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        puissance_electrique_w = puissance_hydraulique_w / rendement_pompe
        puissance_electrique_kw = puissance_electrique_w / 1000
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("puissance_electrique", {
                "P_h": puissance_hydraulique_w,
                "η": rendement_pompe
            })
        
        return {
            "puissance_electrique_w": puissance_electrique_w,
            "puissance_electrique_kw": puissance_electrique_kw,
            "puissance_hydraulique_w": puissance_hydraulique_w,
            "rendement_pompe": rendement_pompe,
            "explication": explanation
        }
    
    def calculer_puissance_groupe_electrogene(self, puissance_electrique_kw: float,
                                             facteur_securite: float = 1.2) -> Dict[str, Any]:
        """
        Calcule la puissance du groupe électrogène.
        
        Args:
            puissance_electrique_kw: Puissance électrique en kW
            facteur_securite: Facteur de sécurité
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        puissance_groupe_kva = puissance_electrique_kw * facteur_securite
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("puissance_groupe", {
                "P_elec": puissance_electrique_kw,
                "fs": facteur_securite
            })
        
        return {
            "puissance_groupe_kva": puissance_groupe_kva,
            "puissance_electrique_kw": puissance_electrique_kw,
            "facteur_securite": facteur_securite,
            "explication": explanation
        }
    
    def calculer_hauteur_manometrique_totale(self, hauteur_geometrique_m: float,
                                            perte_charge_m: float,
                                            pression_requise_mce: float = 0) -> Dict[str, Any]:
        """
        Calcule la hauteur manométrique totale.
        
        Args:
            hauteur_geometrique_m: Hauteur géométrique en mètres
            perte_charge_m: Pertes de charge en mètres
            pression_requise_mce: Pression requise en mètres de colonne d'eau
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        hmt = hauteur_geometrique_m + perte_charge_m + pression_requise_mce
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("hauteur_manometrique_totale", {
                "H_g": hauteur_geometrique_m,
                "ΔH": perte_charge_m,
                "P": pression_requise_mce
            })
        
        return {
            "hauteur_manometrique_totale_m": hmt,
            "hauteur_geometrique_m": hauteur_geometrique_m,
            "perte_charge_m": perte_charge_m,
            "pression_requise_mce": pression_requise_mce,
            "explication": explanation
        }
    
    def dimensionner_pompe(self, debit_m3s: float, hauteur_manometrique_m: float,
                          type_pompe: str = 'centrifuge') -> Dict[str, Any]:
        """
        Dimensionne une pompe selon le type.
        
        Args:
            debit_m3s: Débit en m³/s
            hauteur_manometrique_m: Hauteur manométrique en mètres
            type_pompe: Type de pompe ('centrifuge', 'helice', 'volumetrique')
            
        Returns:
            Dict: Résultats du dimensionnement
        """
        # Calcul de la puissance hydraulique
        resultat_puissance = self.calculer_puissance_hydraulique(debit_m3s, hauteur_manometrique_m)
        
        # Rendements selon le type de pompe
        rendements = {
            'centrifuge': 0.75,
            'helice': 0.80,
            'volumetrique': 0.70
        }
        
        rendement_pompe = rendements.get(type_pompe, 0.75)
        
        # Calcul de la puissance électrique
        resultat_electrique = self.calculer_puissance_electrique(
            resultat_puissance['puissance_hydraulique_w'], rendement_pompe
        )
        
        # Calcul de la puissance du groupe
        resultat_groupe = self.calculer_puissance_groupe_electrogene(
            resultat_electrique['puissance_electrique_kw']
        )
        
        return {
            "type_pompe": type_pompe,
            "debit_m3s": debit_m3s,
            "hauteur_manometrique_m": hauteur_manometrique_m,
            "rendement_pompe": rendement_pompe,
            **resultat_puissance,
            **resultat_electrique,
            **resultat_groupe
        }
    
    def calculer_courbe_rendement(self, debit_m3s: float, hauteur_manometrique_m: float,
                                 rendement_max: float = 0.85) -> Dict[str, Any]:
        """
        Calcule une courbe de rendement simplifiée.
        
        Args:
            debit_m3s: Débit nominal en m³/s
            hauteur_manometrique_m: Hauteur manométrique nominale en mètres
            rendement_max: Rendement maximum
            
        Returns:
            Dict: Courbe de rendement
        """
        # Points de la courbe de rendement (simplifiée)
        points = []
        debits_test = [0.5, 0.75, 1.0, 1.25, 1.5]  # Multiplicateurs du débit nominal
        
        for facteur in debits_test:
            debit_test = debit_m3s * facteur
            
            # Rendement simplifié (courbe parabolique)
            if facteur == 1.0:
                rendement = rendement_max
            else:
                # Rendement décroît quand on s'éloigne du point nominal
                ecart = abs(facteur - 1.0)
                rendement = rendement_max * (1 - 0.3 * ecart**2)
                rendement = max(rendement, 0.1)  # Rendement minimum
            
            points.append({
                "debit_m3s": debit_test,
                "rendement": rendement,
                "facteur": facteur
            })
        
        return {
            "points_courbe": points,
            "debit_nominal_m3s": debit_m3s,
            "rendement_max": rendement_max,
            "hauteur_nominale_m": hauteur_manometrique_m
        }
    
    def calculer_point_fonctionnement(self, courbe_pompe: List[Dict], 
                                    courbe_reseau: List[Dict]) -> Dict[str, Any]:
        """
        Calcule le point de fonctionnement pompe-réseau.
        
        Args:
            courbe_pompe: Courbe caractéristique de la pompe
            courbe_reseau: Courbe caractéristique du réseau
            
        Returns:
            Dict: Point de fonctionnement
        """
        # Recherche de l'intersection (simplifiée)
        point_fonctionnement = None
        
        for point_pompe in courbe_pompe:
            debit_pompe = point_pompe['debit_m3s']
            
            # Recherche du point réseau correspondant
            for point_reseau in courbe_reseau:
                if abs(point_reseau['debit_m3s'] - debit_pompe) < 0.01:  # Tolérance
                    if abs(point_reseau['hauteur_m'] - point_pompe['hauteur_m']) < 1.0:
                        point_fonctionnement = {
                            "debit_m3s": debit_pompe,
                            "hauteur_m": point_pompe['hauteur_m'],
                            "rendement": point_pompe.get('rendement', 0.75)
                        }
                        break
            
            if point_fonctionnement:
                break
        
        return {
            "point_fonctionnement": point_fonctionnement,
            "courbe_pompe": courbe_pompe,
            "courbe_reseau": courbe_reseau
        }
    
    def calculer_energie_consommee(self, puissance_electrique_kw: float,
                                  temps_fonctionnement_h: float) -> Dict[str, Any]:
        """
        Calcule l'énergie consommée.
        
        Args:
            puissance_electrique_kw: Puissance électrique en kW
            temps_fonctionnement_h: Temps de fonctionnement en heures
            
        Returns:
            Dict: Résultats du calcul
        """
        energie_kwh = puissance_electrique_kw * temps_fonctionnement_h
        
        return {
            "energie_kwh": energie_kwh,
            "puissance_electrique_kw": puissance_electrique_kw,
            "temps_fonctionnement_h": temps_fonctionnement_h
        }
    
    def calculer_cout_energie(self, energie_kwh: float, prix_kwh: float = 0.15) -> Dict[str, Any]:
        """
        Calcule le coût de l'énergie.
        
        Args:
            energie_kwh: Énergie consommée en kWh
            prix_kwh: Prix du kWh en euros
            
        Returns:
            Dict: Résultats du calcul
        """
        cout_euros = energie_kwh * prix_kwh
        
        return {
            "cout_euros": cout_euros,
            "energie_kwh": energie_kwh,
            "prix_kwh": prix_kwh
        }

# =============================================================================
# FONCTIONS D'INTERFACE POUR CLI/REPL
# =============================================================================

def dimension_pumping_unified(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Dimensionnement unifié des équipements de pompage.
    
    Cette fonction fusionne les fonctionnalités de pumping.py et pumping_enhanced.py.
    
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
        # Validation des données avec le validateur unifié
        from ..core.validators import validate_pumping_unified_data
        data = validate_pumping_unified_data(data)
        
        # Extraction des paramètres
        debit_m3h = data.get("debit_m3h", 0.0)
        hmt_m = data.get("hmt_m", 50.0)
        type_pompe = data.get("type_pompe", "centrifuge")
        rendement_pompe = data.get("rendement_pompe", 0.75)
        
        # Conversion débit m³/h vers m³/s
        debit_m3s = debit_m3h / 3600
        
        # Initialiser le calculateur
        calc = PumpingCalculationsUnified()
        
        # Dimensionnement de la pompe
        resultat_dimensionnement = calc.dimensionner_pompe(debit_m3s, hmt_m, type_pompe)
        
        if 'erreur' in resultat_dimensionnement:
            return {
                "statut": "ERREUR",
                "message": resultat_dimensionnement['erreur']
            }
        
        # Calculs de puissance détaillés
        puissance_hydraulique = calc.calculer_puissance_hydraulique(debit_m3s, hmt_m)
        puissance_electrique = calc.calculer_puissance_electrique(
            puissance_hydraulique['puissance_hydraulique_w'], rendement_pompe
        )
        puissance_groupe = calc.calculer_puissance_groupe_electrogene(
            puissance_electrique['puissance_electrique_kw']
        )
        
        # Calcul de l'énergie consommée (pour 24h de fonctionnement)
        energie_consommee = calc.calculer_energie_consommee(
            puissance_electrique['puissance_electrique_kw'], 24.0
        )
        
        # Calcul du coût énergétique
        cout_energie = calc.calculer_cout_energie(
            energie_consommee['energie_kwh'], 0.15  # Prix par défaut
        )
        
        # Vérification des contraintes
        contraintes = {
            "debit_ok": debit_m3h > 0,
            "hmt_ok": 0 < hmt_m <= 200,  # HMT max typique
            "puissance_ok": puissance_electrique['puissance_electrique_w'] > 0,
            "rendement_ok": 0 < rendement_pompe <= 1
        }
        
        # Résultats enrichis
        resultat_final = {
            "statut": "SUCCES",
            "pompage": {
                "debit_m3h": debit_m3h,
                "debit_m3s": debit_m3s,
                "hmt_m": hmt_m,
                "type_pompe": type_pompe,
                "rendement_pompe": rendement_pompe,
                **puissance_hydraulique,
                **puissance_electrique,
                **puissance_groupe,
                **energie_consommee,
                **cout_energie
            },
            "contraintes": contraintes,
            "recommandations": []
        }
        
        # Recommandations
        if puissance_electrique['puissance_electrique_w'] > 100000:  # 100 kW
            resultat_final["recommandations"].append(
                "Puissance élevée, considérer plusieurs pompes en parallèle"
            )
        
        if hmt_m > 100:
            resultat_final["recommandations"].append(
                "HMT élevée, vérifier la nécessité d'étages multiples"
            )
        
        if rendement_pompe < 0.6:
            resultat_final["recommandations"].append(
                "Rendement faible, vérifier le type de pompe choisi"
            )
        
        if verbose:
            print(f"Dimensionnement pompage ({type_pompe}):")
            print(f"   Puissance hydraulique: {puissance_hydraulique['puissance_hydraulique_kw']:.1f} kW")
            print(f"   Puissance électrique: {puissance_electrique['puissance_electrique_kw']:.1f} kW")
            print(f"   Puissance groupe: {puissance_groupe['puissance_groupe_kva']:.1f} kVA")
            print(f"   Énergie journalière: {energie_consommee['energie_kwh']:.1f} kWh")
            print(f"   Coût journalier: {cout_energie['cout_euros']:.2f} €")
        
        return resultat_final
        
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

def comparer_types_pompes_unified(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare différents types de pompes.
    
    Args:
        data: Dictionnaire contenant les données
        
    Returns:
        Dict: Comparaison des types de pompes
    """
    try:
        debit_m3s = data.get("debit_m3s", 0.1)
        hmt_m = data.get("hmt_m", 50.0)
        
        calc = PumpingCalculationsUnified()
        
        # Comparaison des types de pompes
        types_pompes = ['centrifuge', 'helice', 'volumetrique']
        resultats = {}
        
        for type_pompe in types_pompes:
            resultats[type_pompe] = calc.dimensionner_pompe(debit_m3s, hmt_m, type_pompe)
        
        # Analyse comparative
        puissances = [resultats[tp]['puissance_electrique_kw'] for tp in types_pompes]
        rendements = [resultats[tp]['rendement_pompe'] for tp in types_pompes]
        
        resultats['analyse'] = {
            'type_min_puissance': types_pompes[puissances.index(min(puissances))],
            'type_max_rendement': types_pompes[rendements.index(max(rendements))],
            'puissance_min': min(puissances),
            'puissance_max': max(puissances),
            'rendement_max': max(rendements)
        }
        
        return resultats
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors de la comparaison: {str(e)}"
        }

def calculer_cout_energie_pompage_unified(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule le coût de l'énergie pour le pompage.
    
    Args:
        data: Dictionnaire contenant les données
        
    Returns:
        Dict: Résultats du calcul
    """
    try:
        puissance_electrique_kw = data.get("puissance_electrique_kw", 10.0)
        temps_fonctionnement_h = data.get("temps_fonctionnement_h", 24.0)
        prix_kwh = data.get("prix_kwh", 0.15)
        
        calc = PumpingCalculationsUnified()
        
        # Calcul de l'énergie consommée
        resultat_energie = calc.calculer_energie_consommee(puissance_electrique_kw, temps_fonctionnement_h)
        
        # Calcul du coût
        resultat_cout = calc.calculer_cout_energie(resultat_energie['energie_kwh'], prix_kwh)
        
        return {
            **resultat_energie,
            **resultat_cout
        }
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors du calcul: {str(e)}"
        }

def get_pumping_unified_help() -> str:
    """
    Retourne l'aide pour le module pompage unifié.
    
    Returns:
        str: Texte d'aide
    """
    return """
⚡ MODULE POMPAGE UNIFIÉ AEP

Ce module fusionne les fonctionnalités de pumping.py et pumping_enhanced.py
pour offrir une version complète avec transparence mathématique.

📋 FONCTIONS DISPONIBLES:

🔢 DIMENSIONNEMENT
  dimension_pumping_unified(data) - Dimensionnement complet avec validation
  - Support des types: centrifuge, hélice, volumétrique
  - Calculs de puissance hydraulique et électrique
  - Validation automatique des données
  - Recommandations intégrées

🔍 COMPARAISON
  comparer_types_pompes_unified(data) - Compare les types de pompes
  - Analyse comparative des puissances
  - Identification du type optimal
  - Recommandations de sélection

💰 COÛT ÉNERGIE
  calculer_cout_energie_pompage_unified(data) - Calcule le coût de l'énergie
  - Calcul de l'énergie consommée
  - Estimation des coûts d'exploitation
  - Optimisation économique

📝 EXEMPLES:
  data = {"debit_m3h": 100, "hmt_m": 50, "type_pompe": "centrifuge"}
  result = dimension_pumping_unified(data)
  
  data = {"puissance_electrique_kw": 10, "temps_fonctionnement_h": 24}
  result = calculer_cout_energie_pompage_unified(data)
"""

# =============================================================================
# EXPORTS PRINCIPAUX
# =============================================================================

__all__ = [
    'PumpingCalculationsUnified',
    'dimension_pumping_unified',
    'comparer_types_pompes_unified',
    'calculer_cout_energie_pompage_unified',
    'get_pumping_unified_help'
] 