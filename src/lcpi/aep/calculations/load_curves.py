"""
Courbes de charge horaire et méthodes de pointe pour l'AEP

Ce module implémente les courbes de charge horaire et les différentes
méthodes de calcul des coefficients de pointe selon les standards AEP.
"""

import math
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class LoadCurvePoint:
    """Point d'une courbe de charge"""
    heure: int
    coefficient: float
    description: str

@dataclass
class LoadCurve:
    """Courbe de charge complète"""
    nom: str
    type: str  # "journaliere", "horaire", "saisonniere"
    points: List[LoadCurvePoint]
    coefficient_moyen: float
    coefficient_max: float
    description: str

class AEPLoadCurveManager:
    """Gestionnaire des courbes de charge AEP"""
    
    def __init__(self):
        self.courbes_standard = self._initialiser_courbes_standard()
    
    def _initialiser_courbes_standard(self) -> Dict[str, LoadCurve]:
        """Initialise les courbes de charge standard"""
        courbes = {}
        
        # Courbe de charge journalière standard
        courbes["journaliere_standard"] = LoadCurve(
            nom="Courbe journalière standard",
            type="journaliere",
            points=[
                LoadCurvePoint(0, 0.3, "Nuit (minimal)"),
                LoadCurvePoint(6, 0.8, "Réveil"),
                LoadCurvePoint(8, 1.2, "Départ travail"),
                LoadCurvePoint(12, 1.5, "Déjeuner"),
                LoadCurvePoint(14, 1.0, "Après-midi"),
                LoadCurvePoint(18, 1.8, "Retour travail"),
                LoadCurvePoint(20, 1.3, "Soirée"),
                LoadCurvePoint(22, 0.6, "Coucher"),
                LoadCurvePoint(24, 0.3, "Nuit (minimal)")
            ],
            coefficient_moyen=1.0,
            coefficient_max=1.8,
            description="Courbe de charge journalière standard pour zones résidentielles"
        )
        
        # Courbe de charge horaire détaillée
        courbes["horaire_detaille"] = LoadCurve(
            nom="Courbe horaire détaillée",
            type="horaire",
            points=[
                LoadCurvePoint(0, 0.25, "00h - Nuit profonde"),
                LoadCurvePoint(1, 0.20, "01h - Nuit profonde"),
                LoadCurvePoint(2, 0.18, "02h - Nuit profonde"),
                LoadCurvePoint(3, 0.15, "03h - Nuit profonde"),
                LoadCurvePoint(4, 0.20, "04h - Nuit profonde"),
                LoadCurvePoint(5, 0.30, "05h - Réveil agricole"),
                LoadCurvePoint(6, 0.60, "06h - Réveil urbain"),
                LoadCurvePoint(7, 1.10, "07h - Activité matinale"),
                LoadCurvePoint(8, 1.40, "08h - Départ travail"),
                LoadCurvePoint(9, 1.20, "09h - Activité professionnelle"),
                LoadCurvePoint(10, 1.15, "10h - Activité professionnelle"),
                LoadCurvePoint(11, 1.25, "11h - Préparation déjeuner"),
                LoadCurvePoint(12, 1.60, "12h - Déjeuner"),
                LoadCurvePoint(13, 1.30, "13h - Après déjeuner"),
                LoadCurvePoint(14, 1.10, "14h - Activité professionnelle"),
                LoadCurvePoint(15, 1.05, "15h - Activité professionnelle"),
                LoadCurvePoint(16, 1.15, "16h - Fin de journée"),
                LoadCurvePoint(17, 1.35, "17h - Retour travail"),
                LoadCurvePoint(18, 1.70, "18h - Activités domestiques"),
                LoadCurvePoint(19, 1.50, "19h - Dîner"),
                LoadCurvePoint(20, 1.40, "20h - Soirée"),
                LoadCurvePoint(21, 1.25, "21h - Soirée"),
                LoadCurvePoint(22, 0.90, "22h - Préparation coucher"),
                LoadCurvePoint(23, 0.50, "23h - Coucher"),
                LoadCurvePoint(24, 0.25, "24h - Nuit profonde")
            ],
            coefficient_moyen=1.0,
            coefficient_max=1.70,
            description="Courbe de charge horaire détaillée sur 24h"
        )
        
        # Courbe de charge saisonnière
        courbes["saisonniere"] = LoadCurve(
            nom="Courbe saisonnière",
            type="saisonniere",
            points=[
                LoadCurvePoint(1, 0.85, "Janvier - Hiver"),
                LoadCurvePoint(2, 0.80, "Février - Hiver"),
                LoadCurvePoint(3, 0.90, "Mars - Printemps"),
                LoadCurvePoint(4, 1.05, "Avril - Printemps"),
                LoadCurvePoint(5, 1.15, "Mai - Printemps"),
                LoadCurvePoint(6, 1.25, "Juin - Été"),
                LoadCurvePoint(7, 1.35, "Juillet - Été"),
                LoadCurvePoint(8, 1.30, "Août - Été"),
                LoadCurvePoint(9, 1.20, "Septembre - Automne"),
                LoadCurvePoint(10, 1.10, "Octobre - Automne"),
                LoadCurvePoint(11, 0.95, "Novembre - Automne"),
                LoadCurvePoint(12, 0.90, "Décembre - Hiver")
            ],
            coefficient_moyen=1.0,
            coefficient_max=1.35,
            description="Courbe de charge saisonnière mensuelle"
        )
        
        return courbes
    
    def obtenir_courbe(self, nom_courbe: str) -> Optional[LoadCurve]:
        """Obtient une courbe de charge par son nom"""
        return self.courbes_standard.get(nom_courbe)
    
    def lister_courbes_disponibles(self) -> List[str]:
        """Liste toutes les courbes de charge disponibles"""
        return list(self.courbes_standard.keys())
    
    def calculer_coefficient_pointe_horaire(
        self,
        debit_moyen_horaire_m3h: float,
        methode: str = "formule_genie_rural"
    ) -> float:
        """
        Calcule le coefficient de pointe horaire selon différentes méthodes
        
        Args:
            debit_moyen_horaire_m3h: Débit moyen horaire en m³/h
            methode: Méthode de calcul ("formule_genie_rural", "formule_oms", "formule_empirique")
            
        Returns:
            Coefficient de pointe horaire
        """
        if methode == "formule_genie_rural":
            # Formule du génie rural : Cph = 1.5 + 2.5/√Qmh
            return 1.5 + 2.5 / math.sqrt(debit_moyen_horaire_m3h)
        
        elif methode == "formule_oms":
            # Formule OMS : Cph = 1.8 pour Q < 100 m³/h, sinon 1.5
            if debit_moyen_horaire_m3h < 100:
                return 1.8
            else:
                return 1.5
        
        elif methode == "formule_empirique":
            # Formule empirique : Cph = 2.0 - 0.5 * log10(Qmh)
            return 2.0 - 0.5 * math.log10(max(debit_moyen_horaire_m3h, 1))
        
        else:
            raise ValueError(f"Méthode non supportée: {methode}")
    
    def calculer_coefficient_pointe_journalier(
        self,
        population: int,
        methode: str = "formule_standard"
    ) -> float:
        """
        Calcule le coefficient de pointe journalier
        
        Args:
            population: Population desservie
            methode: Méthode de calcul ("formule_standard", "formule_population", "formule_zone")
            
        Returns:
            Coefficient de pointe journalier
        """
        if methode == "formule_standard":
            # Formule standard AEP : Cpj = 1.5
            return 1.5
        
        elif methode == "formule_population":
            # Formule basée sur la population : Cpj = 1.3 + 0.2 * log10(P)
            return 1.3 + 0.2 * math.log10(max(population, 100))
        
        elif methode == "formule_zone":
            # Formule basée sur le type de zone
            if population < 1000:
                return 1.8  # Zone rurale
            elif population < 10000:
                return 1.5  # Zone semi-urbaine
            else:
                return 1.3  # Zone urbaine
        
        else:
            raise ValueError(f"Méthode non supportée: {methode}")
    
    def calculer_coefficient_pointe_global(
        self,
        population: int,
        debit_moyen_horaire_m3h: float,
        methode_journaliere: str = "formule_standard",
        methode_horaire: str = "formule_genie_rural"
    ) -> Dict[str, float]:
        """
        Calcule tous les coefficients de pointe
        
        Args:
            population: Population desservie
            debit_moyen_horaire_m3h: Débit moyen horaire en m³/h
            methode_journaliere: Méthode pour le coefficient journalier
            methode_horaire: Méthode pour le coefficient horaire
            
        Returns:
            Dictionnaire avec tous les coefficients
        """
        cpj = self.calculer_coefficient_pointe_journalier(population, methode_journaliere)
        cph = self.calculer_coefficient_pointe_horaire(debit_moyen_horaire_m3h, methode_horaire)
        
        # Coefficient global = journalier × horaire
        cp_global = cpj * cph
        
        return {
            "coefficient_pointe_journalier": round(cpj, 3),
            "coefficient_pointe_horaire": round(cph, 3),
            "coefficient_pointe_global": round(cp_global, 3)
        }
    
    def generer_courbe_personnalisee(
        self,
        nom: str,
        type_courbe: str,
        points: List[Tuple[int, float, str]]
    ) -> LoadCurve:
        """
        Génère une courbe de charge personnalisée
        
        Args:
            nom: Nom de la courbe
            type_courbe: Type de courbe
            points: Liste de tuples (heure, coefficient, description)
            
        Returns:
            Courbe de charge personnalisée
        """
        load_points = []
        coefficients = []
        
        for heure, coefficient, description in points:
            load_points.append(LoadCurvePoint(heure, coefficient, description))
            coefficients.append(coefficient)
        
        return LoadCurve(
            nom=nom,
            type=type_courbe,
            points=load_points,
            coefficient_moyen=sum(coefficients) / len(coefficients),
            coefficient_max=max(coefficients),
            description=f"Courbe personnalisée: {nom}"
        )
    
    def exporter_courbe_json(self, courbe: LoadCurve) -> str:
        """Exporte une courbe de charge en JSON"""
        data = {
            "nom": courbe.nom,
            "type": courbe.type,
            "coefficient_moyen": courbe.coefficient_moyen,
            "coefficient_max": courbe.coefficient_max,
            "description": courbe.description,
            "points": [
                {
                    "heure": point.heure,
                    "coefficient": point.coefficient,
                    "description": point.description
                }
                for point in courbe.points
            ]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def importer_courbe_json(self, json_data: str) -> LoadCurve:
        """Importe une courbe de charge depuis JSON"""
        data = json.loads(json_data)
        
        points = []
        for point_data in data["points"]:
            points.append(LoadCurvePoint(
                heure=point_data["heure"],
                coefficient=point_data["coefficient"],
                description=point_data["description"]
            ))
        
        return LoadCurve(
            nom=data["nom"],
            type=data["type"],
            points=points,
            coefficient_moyen=data["coefficient_moyen"],
            coefficient_max=data["coefficient_max"],
            description=data["description"]
        )
    
    def calculer_besoin_pointe(
        self,
        besoin_moyen_journalier: float,
        coefficient_pointe_journalier: float,
        coefficient_pointe_horaire: float
    ) -> Dict[str, float]:
        """
        Calcule les besoins de pointe
        
        Args:
            besoin_moyen_journalier: Besoin moyen journalier en m³/jour
            coefficient_pointe_journalier: Coefficient de pointe journalier
            coefficient_pointe_horaire: Coefficient de pointe horaire
            
        Returns:
            Dictionnaire avec les besoins de pointe
        """
        # Besoin de pointe journalier
        besoin_pointe_journalier = besoin_moyen_journalier * coefficient_pointe_journalier
        
        # Besoin de pointe horaire
        besoin_pointe_horaire = besoin_pointe_journalier / 24 * coefficient_pointe_horaire
        
        # Besoin de pointe global
        besoin_pointe_global = besoin_moyen_journalier * coefficient_pointe_journalier * coefficient_pointe_horaire
        
        return {
            "besoin_moyen_journalier_m3_j": round(besoin_moyen_journalier, 2),
            "besoin_pointe_journalier_m3_j": round(besoin_pointe_journalier, 2),
            "besoin_pointe_horaire_m3_h": round(besoin_pointe_horaire, 2),
            "besoin_pointe_global_m3_h": round(besoin_pointe_global, 2),
            "coefficient_pointe_journalier": coefficient_pointe_journalier,
            "coefficient_pointe_horaire": coefficient_pointe_horaire,
            "coefficient_pointe_global": round(coefficient_pointe_journalier * coefficient_pointe_horaire, 3)
        }
