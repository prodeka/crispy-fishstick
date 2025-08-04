"""
Module de calculs réservoir amélioré intégrant les formules de AMELIORATION.
Inclut la transparence mathématique et les explications pédagogiques.
"""

import math
import json
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

from ..core.mathematical_transparency import math_transparency
from ..core.constants import *
from ..core.formulas import *

class ReservoirCalculationsEnhanced:
    """
    Classe pour les calculs réservoir améliorés avec transparence mathématique.
    Intègre les formules de AMELIORATION/reservoir.py
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialise le calculateur réservoir.
        
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
        explanation = math_transparency.display_formula("volume_utile", {
            "V_max": max(bilan),
            "V_min": min(bilan)
        })
        
        return {
            "volume_utile_m3": volume_utile,
            "volume_max_m3": max(bilan),
            "volume_min_m3": min(bilan),
            "bilan_horaire": bilan,
            "debit_moyen_m3h": debit_moyen_a,
            "mode_adduction": mode_adduction,
            "explication": explanation
        }
    
    def calculer_capacite_pratique(self, volume_utile_m3: float, volume_journalier_m3: float,
                                  surface_radier_m2: float, params_calcul: Dict) -> Dict[str, Any]:
        """
        Calcule la capacité pratique (totale) du réservoir.
        
        Args:
            volume_utile_m3: Volume utile calculé
            volume_journalier_m3: Consommation totale sur 24h
            surface_radier_m2: Surface au sol du réservoir
            params_calcul: Dictionnaire des paramètres de calcul
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        # Calcul du volume de réserve incendie
        debit_moyen_a = self.calculer_debit_moyen(volume_journalier_m3)
        facteur_incendie = params_calcul.get('facteur_reserve_incendie_par_debit_moyen', 2.0)
        volume_incendie = facteur_incendie * debit_moyen_a
        
        # Calcul du volume mort
        hauteur_mort = params_calcul.get('hauteur_volume_mort_m', 0.5)
        volume_mort = hauteur_mort * surface_radier_m2
        
        # Capacité totale
        capacite_totale = volume_utile_m3 + volume_incendie + volume_mort
        
        # Transparence mathématique pour le volume d'incendie
        explanation_incendie = math_transparency.display_formula("volume_incendie", {
            "D": debit_moyen_a * 3600 / 1000,  # Conversion en L/min
            "T": 30  # 30 minutes par défaut
        })
        
        return {
            "volume_utile_m3": volume_utile_m3,
            "volume_incendie_m3": volume_incendie,
            "volume_mort_m3": volume_mort,
            "capacite_totale_m3": capacite_totale,
            "hauteur_mort_m": hauteur_mort,
            "facteur_incendie": facteur_incendie,
            "explication_incendie": explanation_incendie
        }
    
    def dimensionner_reservoir_cylindrique(self, volume_total_m3: float, 
                                         rapport_h_d: float = 1.0) -> Dict[str, Any]:
        """
        Dimensionne un réservoir cylindrique.
        
        Args:
            volume_total_m3: Volume total du réservoir
            rapport_h_d: Rapport hauteur/diamètre
            
        Returns:
            Dict: Dimensions du réservoir
        """
        # Volume d'un cylindre : V = π × (D/2)² × H
        # Avec H = rapport_h_d × D
        # V = π × (D/2)² × rapport_h_d × D
        # V = π × rapport_h_d × D³ / 4
        # D³ = 4 × V / (π × rapport_h_d)
        
        diametre = (4 * volume_total_m3 / (math.pi * rapport_h_d))**(1/3)
        hauteur = rapport_h_d * diametre
        
        return {
            "diametre_m": diametre,
            "hauteur_m": hauteur,
            "volume_total_m3": volume_total_m3,
            "rapport_h_d": rapport_h_d,
            "surface_radier_m2": math.pi * (diametre/2)**2
        }
    
    def dimensionner_reservoir_rectangulaire(self, volume_total_m3: float, 
                                           rapport_l_l: float = 2.0, 
                                           rapport_h_l: float = 1.0) -> Dict[str, Any]:
        """
        Dimensionne un réservoir rectangulaire.
        
        Args:
            volume_total_m3: Volume total du réservoir
            rapport_l_l: Rapport longueur/largeur
            rapport_h_l: Rapport hauteur/largeur
            
        Returns:
            Dict: Dimensions du réservoir
        """
        # Volume d'un parallélépipède : V = L × l × H
        # Avec L = rapport_l_l × l et H = rapport_h_l × l
        # V = rapport_l_l × l × l × rapport_h_l × l
        # V = rapport_l_l × rapport_h_l × l³
        # l³ = V / (rapport_l_l × rapport_h_l)
        
        largeur = (volume_total_m3 / (rapport_l_l * rapport_h_l))**(1/3)
        longueur = rapport_l_l * largeur
        hauteur = rapport_h_l * largeur
        
        return {
            "largeur_m": largeur,
            "longueur_m": longueur,
            "hauteur_m": hauteur,
            "volume_total_m3": volume_total_m3,
            "rapport_l_l": rapport_l_l,
            "rapport_h_l": rapport_h_l,
            "surface_radier_m2": longueur * largeur
        }
    
    def calculer_temps_sejour(self, volume_reservoir_m3: float, 
                             debit_entree_m3h: float) -> Dict[str, Any]:
        """
        Calcule le temps de séjour de l'eau dans le réservoir.
        
        Args:
            volume_reservoir_m3: Volume du réservoir
            debit_entree_m3h: Débit d'entrée
            
        Returns:
            Dict: Temps de séjour
        """
        temps_sejour_h = volume_reservoir_m3 / debit_entree_m3h
        temps_sejour_min = temps_sejour_h * 60
        
        return {
            "temps_sejour_h": temps_sejour_h,
            "temps_sejour_min": temps_sejour_min,
            "volume_reservoir_m3": volume_reservoir_m3,
            "debit_entree_m3h": debit_entree_m3h
        }
    
    def verifier_temps_contact_desinfection(self, temps_sejour_h: float, 
                                          temps_contact_min_h: float = 0.5) -> Dict[str, Any]:
        """
        Vérifie si le temps de contact est suffisant pour la désinfection.
        
        Args:
            temps_sejour_h: Temps de séjour dans le réservoir
            temps_contact_min_h: Temps de contact minimum requis
            
        Returns:
            Dict: Résultats de la vérification
        """
        if temps_sejour_h >= temps_contact_min_h:
            statut = "OK"
            message = f"Temps de contact {temps_sejour_h:.2f} h ≥ {temps_contact_min_h} h requis"
        else:
            statut = "INSUFFISANT"
            message = f"Temps de contact {temps_sejour_h:.2f} h < {temps_contact_min_h} h requis"
        
        return {
            "statut": statut,
            "message": message,
            "temps_sejour_h": temps_sejour_h,
            "temps_contact_min_h": temps_contact_min_h
        }
    
    def calculer_profil_consommation_standard(self, type_zone: str = 'ville_francaise_peu_importante') -> Dict[str, Any]:
        """
        Retourne un profil de consommation standard.
        
        Args:
            type_zone: Type de zone urbaine
            
        Returns:
            Dict: Profil de consommation
        """
        profils_standard = {
            'ville_francaise_peu_importante': {
                'description': 'Ville française de moins de 10 000 habitants',
                'repartition': [
                    {'debut': 0, 'fin': 6, 'coefficient': 0.02},
                    {'debut': 6, 'fin': 8, 'coefficient': 0.08},
                    {'debut': 8, 'fin': 12, 'coefficient': 0.06},
                    {'debut': 12, 'fin': 14, 'coefficient': 0.10},
                    {'debut': 14, 'fin': 18, 'coefficient': 0.06},
                    {'debut': 18, 'fin': 22, 'coefficient': 0.12},
                    {'debut': 22, 'fin': 24, 'coefficient': 0.04}
                ]
            },
            'ville_francaise_importante': {
                'description': 'Ville française de plus de 10 000 habitants',
                'repartition': [
                    {'debut': 0, 'fin': 6, 'coefficient': 0.03},
                    {'debut': 6, 'fin': 8, 'coefficient': 0.10},
                    {'debut': 8, 'fin': 12, 'coefficient': 0.08},
                    {'debut': 12, 'fin': 14, 'coefficient': 0.12},
                    {'debut': 14, 'fin': 18, 'coefficient': 0.08},
                    {'debut': 18, 'fin': 22, 'coefficient': 0.15},
                    {'debut': 22, 'fin': 24, 'coefficient': 0.06}
                ]
            }
        }
        
        return profils_standard.get(type_zone, profils_standard['ville_francaise_peu_importante'])

# Fonctions d'interface pour compatibilité avec l'API existante
def dimension_reservoir_enhanced(data: Dict) -> Dict:
    """
    Dimensionne un réservoir avec transparence mathématique.
    
    Args:
        data: Données du réservoir
        
    Returns:
        Dict: Résultats du dimensionnement
    """
    calc = ReservoirCalculationsEnhanced()
    
    volume_journalier = data.get('volume_journalier_m3', 5000)
    surface_radier = data.get('surface_radier_m2', 250)
    type_zone = data.get('type_zone', 'ville_francaise_peu_importante')
    mode_adduction = data.get('mode_adduction', '24h')
    
    # Paramètres de calcul
    params_calcul = {
        'facteur_reserve_incendie_par_debit_moyen': 2.0,
        'hauteur_volume_mort_m': 0.5
    }
    
    # Profil de consommation
    profil = calc.calculer_profil_consommation_standard(type_zone)
    
    # Calcul du volume utile
    resultats_volume = calc.calculer_volume_utile(volume_journalier, profil, mode_adduction)
    
    # Calcul de la capacité pratique
    resultats_capacite = calc.calculer_capacite_pratique(
        resultats_volume['volume_utile_m3'],
        volume_journalier,
        surface_radier,
        params_calcul
    )
    
    # Dimensionnement du réservoir
    if data.get('forme', 'cylindrique') == 'cylindrique':
        dimensions = calc.dimensionner_reservoir_cylindrique(
            resultats_capacite['capacite_totale_m3'],
            data.get('rapport_h_d', 1.0)
        )
    else:
        dimensions = calc.dimensionner_reservoir_rectangulaire(
            resultats_capacite['capacite_totale_m3'],
            data.get('rapport_l_l', 2.0),
            data.get('rapport_h_l', 1.0)
        )
    
    # Calcul du temps de séjour
    debit_moyen = calc.calculer_debit_moyen(volume_journalier)
    temps_sejour = calc.calculer_temps_sejour(
        resultats_capacite['capacite_totale_m3'],
        debit_moyen
    )
    
    # Vérification du temps de contact
    verification_contact = calc.verifier_temps_contact_desinfection(
        temps_sejour['temps_sejour_h']
    )
    
    return {
        **resultats_volume,
        **resultats_capacite,
        **dimensions,
        **temps_sejour,
        'verification_contact': verification_contact,
        'profil_consommation': profil
    }

def comparer_scenarios_reservoir(data: Dict) -> Dict:
    """
    Compare différents scénarios de dimensionnement de réservoir.
    
    Args:
        data: Données du réservoir
        
    Returns:
        Dict: Comparaison des scénarios
    """
    calc = ReservoirCalculationsEnhanced()
    
    volume_journalier = data.get('volume_journalier_m3', 5000)
    surface_radier = data.get('surface_radier_m2', 250)
    
    # Scénario 1: Adduction continue 24h
    profil = calc.calculer_profil_consommation_standard()
    scenario_24h = calc.calculer_volume_utile(volume_journalier, profil, '24h')
    
    # Scénario 2: Adduction intermittente 10h
    scenario_10h = calc.calculer_volume_utile(volume_journalier, profil, '10h_nuit')
    
    return {
        'scenario_24h': scenario_24h,
        'scenario_10h': scenario_10h,
        'comparaison': {
            'difference_volume_m3': scenario_10h['volume_utile_m3'] - scenario_24h['volume_utile_m3'],
            'rapport_volumes': scenario_10h['volume_utile_m3'] / scenario_24h['volume_utile_m3']
        }
    } 