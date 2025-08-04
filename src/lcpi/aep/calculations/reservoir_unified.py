"""
Module de calculs réservoir unifié pour AEP - Version Fusionnée et Enrichie

Ce module fusionne les fonctionnalités de reservoir.py et reservoir_enhanced.py
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
from lcpi.aep.core.validators import AEPValidationError, validate_reservoir_data

try:
    from ..core.mathematical_transparency import math_transparency
    MATH_TRANSPARENCY_AVAILABLE = True
except ImportError:
    MATH_TRANSPARENCY_AVAILABLE = False
    print("⚠️ Module de transparence mathématique non disponible")

class ReservoirCalculationsUnified:
    """
    Classe unifiée pour les calculs réservoir AEP.
    Fusionne les fonctionnalités de reservoir.py et reservoir_enhanced.py
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialise le calculateur réservoir unifié.
        
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
    
    def calculer_debit_moyen(self, volume_journalier_m3: float) -> float:
        """
        Calcule le débit moyen horaire.
        
        Args:
            volume_journalier_m3: Volume journalier en m³
            
        Returns:
            float: Débit moyen en m³/h
        """
        return volume_journalier_m3 / 24.0
    
    def calculer_volume_utile(self, volume_journalier_m3: float, profil: Dict, 
                            mode_adduction: str = '24h') -> Dict[str, Any]:
        """
        Calcule le volume utile du réservoir par la méthode du bilan hydraulique.
        
        Args:
            volume_journalier_m3: Consommation totale sur 24h
            profil: Dictionnaire du profil de consommation
            mode_adduction: '24h' pour adduction continue, '10h_nuit' pour adduction de 20h à 6h
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        debit_moyen_a = self.calculer_debit_moyen(volume_journalier_m3)
        repartition = profil.get('repartition', [])
        
        bilan = [0.0] * 25  # Pour stocker le volume accumulé à chaque heure (de h=0 à h=24)
        
        # Créer une liste de coefficients pour chaque heure
        coeffs_horaires = [0.0] * 24
        for tranche in repartition:
            for heure in range(tranche['debut'], tranche['fin']):
                coeffs_horaires[heure] = tranche['coefficient']

        for heure in range(24):
            # Calcul du volume entrant pour l'heure en cours
            if mode_adduction == '24h':
                volume_entrant_heure = debit_moyen_a
            elif mode_adduction == '10h_nuit':
                # Adduction pendant 10h (de 20h à 6h du matin)
                debit_adduction_nuit = volume_journalier_m3 / 10.0
                if heure >= 20 or heure < 6:
                    volume_entrant_heure = debit_adduction_nuit
                else:
                    volume_entrant_heure = 0.0
            else:
                raise ValueError("Mode d'adduction non supporté. Choisissez '24h' ou '10h_nuit'.")

            # Calcul du volume sortant
            volume_sortant_heure = coeffs_horaires[heure] * debit_moyen_a
            
            # Variation du volume dans le réservoir
            variation = volume_entrant_heure - volume_sortant_heure
            
            # Bilan à la fin de l'heure
            bilan[heure + 1] = bilan[heure] + variation

        volume_utile = max(bilan) - min(bilan)
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("volume_utile_bilan", {
                "V_utile": volume_utile,
                "V_max": max(bilan),
                "V_min": min(bilan)
            })
        
        return {
            "volume_utile_m3": volume_utile,
            "bilan_horaire": bilan,
            "debit_moyen_m3h": debit_moyen_a,
            "mode_adduction": mode_adduction,
            "explication": explanation
        }
    
    def calculer_capacite_pratique(self, volume_utile_m3: float, volume_journalier_m3: float,
                                  surface_radier_m2: float, params_calcul: Dict) -> Dict[str, Any]:
        """
        Calcule la capacité pratique du réservoir.
        
        Args:
            volume_utile_m3: Volume utile calculé
            volume_journalier_m3: Volume journalier
            surface_radier_m2: Surface du radier
            params_calcul: Paramètres de calcul
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        # Volume mort (10% du volume utile)
        volume_mort = volume_utile_m3 * 0.1
        
        # Volume d'incendie
        volume_incendie = params_calcul.get('volume_incendie', VOLUME_INCENDIE)
        
        # Volume de sécurité (2h de consommation moyenne)
        volume_securite = (volume_journalier_m3 / 24.0) * 2.0
        
        # Capacité pratique
        capacite_pratique = volume_utile_m3 + volume_mort + volume_incendie + volume_securite
        
        return {
            "volume_utile_m3": volume_utile_m3,
            "volume_mort_m3": volume_mort,
            "volume_incendie_m3": volume_incendie,
            "volume_securite_m3": volume_securite,
            "capacite_pratique_m3": capacite_pratique
        }
    
    def dimensionner_reservoir_cylindrique(self, volume_total_m3: float, 
                                         rapport_h_d: float = 1.0) -> Dict[str, Any]:
        """
        Dimensionne un réservoir cylindrique.
        
        Args:
            volume_total_m3: Volume total en m³
            rapport_h_d: Rapport hauteur/diamètre
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        # Calcul du diamètre
        diametre = (4 * volume_total_m3 / (math.pi * rapport_h_d))**(1/3)
        hauteur = diametre * rapport_h_d
        
        # Vérifications
        surface_radier = math.pi * (diametre / 2)**2
        volume_calcule = surface_radier * hauteur
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("reservoir_cylindrique", {
                "V": volume_total_m3,
                "D": diametre,
                "H": hauteur,
                "h/d": rapport_h_d
            })
        
        return {
            "diametre_m": diametre,
            "hauteur_m": hauteur,
            "surface_radier_m2": surface_radier,
            "volume_calcule_m3": volume_calcule,
            "rapport_h_d": rapport_h_d,
            "explication": explanation
        }
    
    def dimensionner_reservoir_rectangulaire(self, volume_total_m3: float, 
                                           rapport_l_l: float = 2.0, 
                                           rapport_h_l: float = 1.0) -> Dict[str, Any]:
        """
        Dimensionne un réservoir rectangulaire.
        
        Args:
            volume_total_m3: Volume total en m³
            rapport_l_l: Rapport longueur/largeur
            rapport_h_l: Rapport hauteur/largeur
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        # Calcul des dimensions
        largeur = (volume_total_m3 / (rapport_l_l * rapport_h_l))**(1/3)
        longueur = largeur * rapport_l_l
        hauteur = largeur * rapport_h_l
        
        # Vérifications
        surface_radier = longueur * largeur
        volume_calcule = surface_radier * hauteur
        
        # Transparence mathématique
        explanation = ""
        if MATH_TRANSPARENCY_AVAILABLE:
            explanation = math_transparency.display_formula("reservoir_rectangulaire", {
                "V": volume_total_m3,
                "L": longueur,
                "l": largeur,
                "H": hauteur,
                "L/l": rapport_l_l,
                "H/l": rapport_h_l
            })
        
        return {
            "longueur_m": longueur,
            "largeur_m": largeur,
            "hauteur_m": hauteur,
            "surface_radier_m2": surface_radier,
            "volume_calcule_m3": volume_calcule,
            "rapport_l_l": rapport_l_l,
            "rapport_h_l": rapport_h_l,
            "explication": explanation
        }
    
    def calculer_temps_sejour(self, volume_reservoir_m3: float, 
                             debit_entree_m3h: float) -> Dict[str, Any]:
        """
        Calcule le temps de séjour dans le réservoir.
        
        Args:
            volume_reservoir_m3: Volume du réservoir en m³
            debit_entree_m3h: Débit d'entrée en m³/h
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        if debit_entree_m3h <= 0:
            raise ValueError("Le débit d'entrée doit être positif")
        
        temps_sejour_h = volume_reservoir_m3 / debit_entree_m3h
        temps_sejour_j = temps_sejour_h / 24.0
        
        return {
            "temps_sejour_h": temps_sejour_h,
            "temps_sejour_j": temps_sejour_j,
            "volume_reservoir_m3": volume_reservoir_m3,
            "debit_entree_m3h": debit_entree_m3h
        }
    
    def verifier_temps_contact_desinfection(self, temps_sejour_h: float, 
                                          temps_contact_min_h: float = 0.5) -> Dict[str, Any]:
        """
        Vérifie si le temps de séjour est suffisant pour la désinfection.
        
        Args:
            temps_sejour_h: Temps de séjour en heures
            temps_contact_min_h: Temps de contact minimum en heures
            
        Returns:
            Dict: Résultats de la vérification
        """
        temps_suffisant = temps_sejour_h >= temps_contact_min_h
        marge = temps_sejour_h - temps_contact_min_h
        
        return {
            "temps_sejour_h": temps_sejour_h,
            "temps_contact_min_h": temps_contact_min_h,
            "temps_suffisant": temps_suffisant,
            "marge_h": marge,
            "recommandation": "Temps de contact suffisant" if temps_suffisant else "Temps de contact insuffisant"
        }
    
    def calculer_profil_consommation_standard(self, type_zone: str = 'ville_francaise_peu_importante') -> Dict[str, Any]:
        """
        Calcule un profil de consommation standard.
        
        Args:
            type_zone: Type de zone ('ville_francaise_peu_importante', 'ville_francaise_importante', 'zone_industrielle')
            
        Returns:
            Dict: Profil de consommation
        """
        profils_standards = {
            'ville_francaise_peu_importante': {
                'repartition': [
                    {'debut': 0, 'fin': 6, 'coefficient': 0.02},   # Nuit
                    {'debut': 6, 'fin': 8, 'coefficient': 0.08},   # Lever
                    {'debut': 8, 'fin': 12, 'coefficient': 0.06},  # Matin
                    {'debut': 12, 'fin': 14, 'coefficient': 0.12}, # Déjeuner
                    {'debut': 14, 'fin': 18, 'coefficient': 0.06}, # Après-midi
                    {'debut': 18, 'fin': 20, 'coefficient': 0.15}, # Dîner
                    {'debut': 20, 'fin': 24, 'coefficient': 0.04}  # Soirée
                ]
            },
            'ville_francaise_importante': {
                'repartition': [
                    {'debut': 0, 'fin': 6, 'coefficient': 0.03},
                    {'debut': 6, 'fin': 9, 'coefficient': 0.12},
                    {'debut': 9, 'fin': 12, 'coefficient': 0.08},
                    {'debut': 12, 'fin': 14, 'coefficient': 0.15},
                    {'debut': 14, 'fin': 18, 'coefficient': 0.08},
                    {'debut': 18, 'fin': 21, 'coefficient': 0.18},
                    {'debut': 21, 'fin': 24, 'coefficient': 0.05}
                ]
            },
            'zone_industrielle': {
                'repartition': [
                    {'debut': 0, 'fin': 8, 'coefficient': 0.05},
                    {'debut': 8, 'fin': 18, 'coefficient': 0.12},
                    {'debut': 18, 'fin': 24, 'coefficient': 0.03}
                ]
            }
        }
        
        if type_zone not in profils_standards:
            raise ValueError(f"Type de zone '{type_zone}' non reconnu")
        
        return profils_standards[type_zone]

    def dimensionner_reservoir(self, volume_journalier_m3: float, mode_adduction: str = '24h',
                             forme: str = 'cylindrique', profil_consommation: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Dimensionne un réservoir selon les paramètres donnés.
        
        Args:
            volume_journalier_m3: Volume journalier en m³
            mode_adduction: Mode d'adduction ('24h' ou '10h_nuit')
            forme: Forme du réservoir ('cylindrique' ou 'rectangulaire')
            profil_consommation: Profil de consommation personnalisé
            
        Returns:
            Dict: Résultats du dimensionnement
        """
        try:
            # Utiliser le profil standard si aucun n'est fourni
            if profil_consommation is None:
                profil_consommation = self.calculer_profil_consommation_standard()
            
            # Calculer le volume utile
            resultat_volume_utile = self.calculer_volume_utile(
                volume_journalier_m3, profil_consommation, mode_adduction
            )
            
            volume_utile_m3 = resultat_volume_utile['volume_utile_m3']
            
            # Calculer la capacité pratique
            params_calcul = {
                'volume_incendie_m3': 7.2,  # Volume d'incendie standard
                'marge_securite': 0.1,  # 10% de marge
                'hauteur_minimale': 2.0  # Hauteur minimale en m
            }
            
            resultat_capacite = self.calculer_capacite_pratique(
                volume_utile_m3, volume_journalier_m3, 0.0, params_calcul
            )
            
            volume_total_m3 = resultat_capacite['capacite_pratique_m3']
            
            # Dimensionner selon la forme
            if forme == 'cylindrique':
                resultat_dimensionnement = self.dimensionner_reservoir_cylindrique(volume_total_m3)
            elif forme == 'rectangulaire':
                resultat_dimensionnement = self.dimensionner_reservoir_rectangulaire(volume_total_m3)
            else:
                raise ValueError(f"Forme '{forme}' non supportée")
            
            # Calculer le temps de séjour
            debit_moyen = self.calculer_debit_moyen(volume_journalier_m3)
            resultat_temps = self.calculer_temps_sejour(volume_total_m3, debit_moyen)
            
            # Vérifier le temps de contact pour la désinfection
            resultat_contact = self.verifier_temps_contact_desinfection(
                resultat_temps['temps_sejour_h']
            )
            
            return {
                "statut": "SUCCES",
                "volume_journalier_m3": volume_journalier_m3,
                "mode_adduction": mode_adduction,
                "forme": forme,
                **resultat_volume_utile,
                **resultat_capacite,
                **resultat_dimensionnement,
                **resultat_temps,
                **resultat_contact,
                "methode": "bilan_hydraulique"
            }
            
        except Exception as e:
            return {
                "statut": "ERREUR",
                "message": f"Erreur lors du dimensionnement: {str(e)}"
            }

# =============================================================================
# FONCTIONS D'INTERFACE POUR CLI/REPL
# =============================================================================

def dimension_reservoir_unified(data: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Dimensionnement unifié du réservoir de stockage d'eau potable.
    
    Cette fonction fusionne les fonctionnalités de reservoir.py et reservoir_enhanced.py.
    
    Args:
        data: Dictionnaire contenant les données du réservoir
        verbose: Afficher les détails des calculs
    
    Returns:
        Dictionnaire avec les résultats du dimensionnement
    """
    if not data:
        return {
            "statut": "ERREUR",
            "message": "Aucune donnée fournie pour le dimensionnement du réservoir"
        }
    
    try:
        # Validation des données avec le validateur unifié
        from ..core.validators import validate_reservoir_unified_data
        data = validate_reservoir_unified_data(data)
        
        # Extraction des paramètres
        volume_journalier_m3 = data.get("volume_journalier_m3", 0.0)
        type_adduction = data.get("type_adduction", "continue")
        forme_reservoir = data.get("forme_reservoir", "cylindrique")
        type_zone = data.get("type_zone", "ville_francaise_peu_importante")
        
        # Mapping des paramètres
        mode_adduction = "24h" if type_adduction == "continue" else "10h_nuit"
        
        # Initialiser le calculateur
        calc = ReservoirCalculationsUnified()
        
        # Dimensionnement
        resultats = calc.dimensionner_reservoir(volume_journalier_m3, mode_adduction, forme_reservoir)
        
        if resultats.get('statut') == 'ERREUR':
            return {
                "statut": "ERREUR",
                "message": resultats.get('message', 'Erreur inconnue')
            }
        
        # Résultats enrichis
        resultat_final = {
            "statut": "SUCCES",
            "reservoir": {
                "volume_journalier_m3": volume_journalier_m3,
                "type_adduction": type_adduction,
                "forme_reservoir": forme_reservoir,
                "type_zone": type_zone,
                **resultats
            },
            "recommandations": []
        }
        
        if verbose:
            volume_utile = resultats.get('volume_utile_m3', 0.0)
            print(f"🏗️ Dimensionnement réservoir ({forme_reservoir}): V={volume_utile:.1f}m³")
        
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

def comparer_scenarios_reservoir_unified(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare différents scénarios de dimensionnement de réservoir.
    
    Args:
        data: Dictionnaire contenant les données
        
    Returns:
        Dict: Comparaison des scénarios
    """
    try:
        volume_journalier = data.get("volume_journalier_m3", 1000)
        
        calc = ReservoirCalculationsUnified()
        
        # Scénario 1: Adduction continue
        scenario_1 = dimension_reservoir_unified({
            "volume_journalier_m3": volume_journalier,
            "type_adduction": "continue",
            "forme_reservoir": "cylindrique"
        })
        
        # Scénario 2: Adduction nocturne
        scenario_2 = dimension_reservoir_unified({
            "volume_journalier_m3": volume_journalier,
            "type_adduction": "intermittente",
            "forme_reservoir": "cylindrique"
        })
        
        # Scénario 3: Réservoir rectangulaire
        scenario_3 = dimension_reservoir_unified({
            "volume_journalier_m3": volume_journalier,
            "type_adduction": "continue",
            "forme_reservoir": "rectangulaire"
        })
        
        return {
            "scenario_continue": scenario_1,
            "scenario_intermittent": scenario_2,
            "scenario_rectangulaire": scenario_3,
            "analyse": {
                "volume_min": min(
                    scenario_1['reservoir']['capacite_pratique_m3'],
                    scenario_2['reservoir']['capacite_pratique_m3'],
                    scenario_3['reservoir']['capacite_pratique_m3']
                ),
                "volume_max": max(
                    scenario_1['reservoir']['capacite_pratique_m3'],
                    scenario_2['reservoir']['capacite_pratique_m3'],
                    scenario_3['reservoir']['capacite_pratique_m3']
                )
            }
        }
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors de la comparaison: {str(e)}"
        }

def calculer_temps_sejour_reservoir_unified(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule le temps de séjour dans un réservoir.
    
    Args:
        data: Dictionnaire contenant les données
        
    Returns:
        Dict: Résultats du calcul
    """
    try:
        volume_reservoir = data.get("volume_reservoir_m3", 1000)
        debit_entree = data.get("debit_entree_m3h", 100)
        
        calc = ReservoirCalculationsUnified()
        resultat = calc.calculer_temps_sejour(volume_reservoir, debit_entree)
        
        # Vérification du temps de contact
        verification = calc.verifier_temps_contact_desinfection(resultat['temps_sejour_h'])
        
        return {
            **resultat,
            "verification": verification
        }
        
    except Exception as e:
        return {
            "statut": "ERREUR",
            "message": f"Erreur lors du calcul: {str(e)}"
        }

def get_reservoir_unified_help() -> str:
    """
    Retourne l'aide pour le module réservoir unifié.
    
    Returns:
        str: Texte d'aide
    """
    return """
🏗️ MODULE RÉSERVOIR UNIFIÉ AEP

Ce module fusionne les fonctionnalités de reservoir.py et reservoir_enhanced.py
pour offrir une version complète avec transparence mathématique.

📋 FONCTIONS DISPONIBLES:

🔢 DIMENSIONNEMENT
  dimension_reservoir_unified(data) - Dimensionnement complet avec validation
  - Support des formes: cylindrique, rectangulaire
  - Modes d'adduction: continue, intermittente
  - Profils de consommation standards
  - Validation automatique des données

🔍 COMPARAISON
  comparer_scenarios_reservoir_unified(data) - Compare les scénarios
  - Analyse comparative des volumes
  - Identification du scénario optimal
  - Recommandations intégrées

⏱️ TEMPS DE SÉJOUR
  calculer_temps_sejour_reservoir_unified(data) - Calcule le temps de séjour
  - Vérification du temps de contact
  - Validation pour la désinfection
  - Recommandations de sécurité

📝 EXEMPLES:
  data = {"volume_journalier_m3": 1000, "type_adduction": "continue"}
  result = dimension_reservoir_unified(data)
  
  data = {"volume_reservoir_m3": 1000, "debit_entree_m3h": 100}
  result = calculer_temps_sejour_reservoir_unified(data)
"""

# =============================================================================
# EXPORTS PRINCIPAUX
# =============================================================================

__all__ = [
    'ReservoirCalculationsUnified',
    'dimension_reservoir_unified',
    'comparer_scenarios_reservoir_unified',
    'calculer_temps_sejour_reservoir_unified',
    'get_reservoir_unified_help'
] 