"""
Module de calculs pompage amélioré intégrant les formules de AMELIORATION.
Inclut la transparence mathématique et les explications pédagogiques.
"""

import math
import json
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

from ..core.mathematical_transparency import math_transparency
from ..core.constants import *
from ..core.formulas import *

class PumpingCalculationsEnhanced:
    """
    Classe pour les calculs pompage améliorés avec transparence mathématique.
    Intègre les formules de AMELIORATION/calcul_adduction.py
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialise le calculateur pompage.
        
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
            Dict: Puissance du groupe électrogène
        """
        puissance_groupe_kw = puissance_electrique_kw * facteur_securite
        
        # Arrondir à la puissance standard supérieure
        puissances_standard = [5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100, 125, 150, 200, 250, 300]
        puissance_standard_kw = next((p for p in puissances_standard if p >= puissance_groupe_kw), 300)
        
        return {
            "puissance_calculee_kw": puissance_groupe_kw,
            "puissance_standard_kw": puissance_standard_kw,
            "facteur_securite": facteur_securite,
            "puissance_electrique_kw": puissance_electrique_kw
        }
    
    def calculer_hauteur_manometrique_totale(self, hauteur_geometrique_m: float,
                                            perte_charge_m: float,
                                            pression_requise_mce: float = 0) -> Dict[str, Any]:
        """
        Calcule la hauteur manométrique totale.
        
        Args:
            hauteur_geometrique_m: Hauteur géométrique en mètres
            perte_charge_m: Perte de charge en mètres
            pression_requise_mce: Pression requise en mCE
            
        Returns:
            Dict: Hauteur manométrique totale
        """
        hauteur_manometrique_totale = hauteur_geometrique_m + perte_charge_m + pression_requise_mce
        
        return {
            "hauteur_manometrique_totale_m": hauteur_manometrique_totale,
            "hauteur_geometrique_m": hauteur_geometrique_m,
            "perte_charge_m": perte_charge_m,
            "pression_requise_mce": pression_requise_mce
        }
    
    def dimensionner_pompe(self, debit_m3s: float, hauteur_manometrique_m: float,
                          type_pompe: str = 'centrifuge') -> Dict[str, Any]:
        """
        Dimensionne une pompe.
        
        Args:
            debit_m3s: Débit en m³/s
            hauteur_manometrique_m: Hauteur manométrique en mètres
            type_pompe: Type de pompe ('centrifuge', 'volumetrique')
            
        Returns:
            Dict: Dimensionnement de la pompe
        """
        # Calcul de la puissance hydraulique
        resultats_hydraulique = self.calculer_puissance_hydraulique(debit_m3s, hauteur_manometrique_m)
        
        # Rendement selon le type de pompe
        rendements = {
            'centrifuge': 0.75,
            'volumetrique': 0.85
        }
        rendement = rendements.get(type_pompe, 0.75)
        
        # Calcul de la puissance électrique
        resultats_electrique = self.calculer_puissance_electrique(
            resultats_hydraulique['puissance_hydraulique_w'], 
            rendement
        )
        
        # Dimensionnement du groupe électrogène
        resultats_groupe = self.calculer_puissance_groupe_electrogene(
            resultats_electrique['puissance_electrique_kw']
        )
        
        return {
            **resultats_hydraulique,
            **resultats_electrique,
            **resultats_groupe,
            "type_pompe": type_pompe,
            "rendement_pompe": rendement
        }
    
    def calculer_courbe_rendement(self, debit_m3s: float, hauteur_manometrique_m: float,
                                 rendement_max: float = 0.85) -> Dict[str, Any]:
        """
        Calcule la courbe de rendement d'une pompe.
        
        Args:
            debit_m3s: Débit nominal en m³/s
            hauteur_manometrique_m: Hauteur manométrique nominale en mètres
            rendement_max: Rendement maximum
            
        Returns:
            Dict: Courbe de rendement
        """
        # Points de la courbe de rendement (débit relatif, rendement relatif)
        points_courbe = [
            (0.0, 0.0),
            (0.5, 0.6),
            (0.75, 0.85),
            (1.0, 1.0),
            (1.25, 0.95),
            (1.5, 0.8),
            (2.0, 0.5)
        ]
        
        courbe_rendement = []
        for debit_rel, rendement_rel in points_courbe:
            debit_abs = debit_rel * debit_m3s
            rendement_abs = rendement_rel * rendement_max
            puissance_hydraulique = self.calculer_puissance_hydraulique(debit_abs, hauteur_manometrique_m)
            puissance_electrique = self.calculer_puissance_electrique(
                puissance_hydraulique['puissance_hydraulique_w'], 
                rendement_abs
            )
            
            courbe_rendement.append({
                "debit_relatif": debit_rel,
                "debit_absolu_m3s": debit_abs,
                "rendement_relatif": rendement_rel,
                "rendement_absolu": rendement_abs,
                "puissance_hydraulique_kw": puissance_hydraulique['puissance_hydraulique_kw'],
                "puissance_electrique_kw": puissance_electrique['puissance_electrique_kw']
            })
        
        return {
            "courbe_rendement": courbe_rendement,
            "debit_nominal_m3s": debit_m3s,
            "hauteur_nominale_m": hauteur_manometrique_m,
            "rendement_maximum": rendement_max
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
        # Recherche du point d'intersection
        point_fonctionnement = None
        
        for point_pompe in courbe_pompe:
            debit_pompe = point_pompe['debit_m3s']
            hauteur_pompe = point_pompe['hauteur_m']
            
            # Recherche du point correspondant sur la courbe réseau
            for point_reseau in courbe_reseau:
                if abs(point_reseau['debit_m3s'] - debit_pompe) < 0.001:
                    hauteur_reseau = point_reseau['hauteur_m']
                    
                    # Si les hauteurs sont proches, c'est le point de fonctionnement
                    if abs(hauteur_pompe - hauteur_reseau) < 0.1:
                        point_fonctionnement = {
                            "debit_m3s": debit_pompe,
                            "hauteur_m": hauteur_pompe,
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
            Dict: Énergie consommée
        """
        energie_kwh = puissance_electrique_kw * temps_fonctionnement_h
        energie_mwh = energie_kwh / 1000
        
        return {
            "energie_kwh": energie_kwh,
            "energie_mwh": energie_mwh,
            "puissance_electrique_kw": puissance_electrique_kw,
            "temps_fonctionnement_h": temps_fonctionnement_h
        }
    
    def calculer_cout_energie(self, energie_kwh: float, prix_kwh: float = 0.15) -> Dict[str, Any]:
        """
        Calcule le coût de l'énergie.
        
        Args:
            energie_kwh: Énergie en kWh
            prix_kwh: Prix du kWh en euros
            
        Returns:
            Dict: Coût de l'énergie
        """
        cout_euros = energie_kwh * prix_kwh
        
        return {
            "cout_euros": cout_euros,
            "energie_kwh": energie_kwh,
            "prix_kwh": prix_kwh
        }

# Fonctions d'interface pour compatibilité avec l'API existante
def dimension_pumping_enhanced(data: Dict) -> Dict:
    """
    Dimensionne un système de pompage avec transparence mathématique.
    
    Args:
        data: Données du système de pompage
        
    Returns:
        Dict: Résultats du dimensionnement
    """
    calc = PumpingCalculationsEnhanced()
    
    debit = data.get('debit_m3s', 0.1)
    hauteur_geometrique = data.get('hauteur_geometrique_m', 50)
    perte_charge = data.get('perte_charge_m', 5)
    pression_requise = data.get('pression_requise_mce', 10)
    type_pompe = data.get('type_pompe', 'centrifuge')
    
    # Calcul de la hauteur manométrique totale
    hauteur_totale = calc.calculer_hauteur_manometrique_totale(
        hauteur_geometrique, perte_charge, pression_requise
    )
    
    # Dimensionnement de la pompe
    resultats = calc.dimensionner_pompe(debit, hauteur_totale['hauteur_manometrique_totale_m'], type_pompe)
    
    # Calcul de la courbe de rendement
    courbe_rendement = calc.calculer_courbe_rendement(debit, hauteur_totale['hauteur_manometrique_totale_m'])
    
    return {
        **resultats,
        **hauteur_totale,
        **courbe_rendement
    }

def comparer_types_pompes(data: Dict) -> Dict:
    """
    Compare différents types de pompes.
    
    Args:
        data: Données du système de pompage
        
    Returns:
        Dict: Comparaison des types de pompes
    """
    calc = PumpingCalculationsEnhanced()
    
    debit = data.get('debit_m3s', 0.1)
    hauteur_geometrique = data.get('hauteur_geometrique_m', 50)
    perte_charge = data.get('perte_charge_m', 5)
    pression_requise = data.get('pression_requise_mce', 10)
    
    hauteur_totale = calc.calculer_hauteur_manometrique_totale(
        hauteur_geometrique, perte_charge, pression_requise
    )
    
    resultats = {}
    
    # Comparaison des types de pompes
    types_pompes = ['centrifuge', 'volumetrique']
    for type_pompe in types_pompes:
        resultats[type_pompe] = calc.dimensionner_pompe(
            debit, hauteur_totale['hauteur_manometrique_totale_m'], type_pompe
        )
    
    # Analyse comparative
    puissances = [resultats[t]['puissance_electrique_kw'] for t in types_pompes]
    resultats['analyse'] = {
        'type_min': types_pompes[puissances.index(min(puissances))],
        'type_max': types_pompes[puissances.index(max(puissances))],
        'ecart_relatif': (max(puissances) - min(puissances)) / min(puissances) * 100
    }
    
    return resultats

def calculer_cout_energie_pompage(data: Dict) -> Dict:
    """
    Calcule le coût énergétique du pompage.
    
    Args:
        data: Données du système de pompage
        
    Returns:
        Dict: Coût énergétique
    """
    calc = PumpingCalculationsEnhanced()
    
    debit = data.get('debit_m3s', 0.1)
    hauteur_manometrique = data.get('hauteur_manometrique_m', 50)
    temps_fonctionnement = data.get('temps_fonctionnement_h', 24)
    prix_kwh = data.get('prix_kwh', 0.15)
    
    # Calcul de la puissance électrique
    puissance_hydraulique = calc.calculer_puissance_hydraulique(debit, hauteur_manometrique)
    puissance_electrique = calc.calculer_puissance_electrique(puissance_hydraulique['puissance_hydraulique_w'])
    
    # Calcul de l'énergie consommée
    energie = calc.calculer_energie_consommee(puissance_electrique['puissance_electrique_kw'], temps_fonctionnement)
    
    # Calcul du coût
    cout = calc.calculer_cout_energie(energie['energie_kwh'], prix_kwh)
    
    return {
        **puissance_hydraulique,
        **puissance_electrique,
        **energie,
        **cout
    } 