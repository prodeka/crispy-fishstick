"""
Courbes de charge horaire et méthodes de pointe pour l'AEP

Ce module implémente les courbes de charge horaire et les différentes
méthodes de calcul des coefficients de pointe selon les standards AEP.
"""

import math
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass
import json
from enum import Enum
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

class TypeCourbe(Enum):
    """Types de courbes supportés"""
    JOURNALIERE = "journaliere"
    HORAIRE = "horaire"
    SAISONNIERE = "saisonniere"
    PERSONNALISEE = "personnalisee"

class MethodeCalcul(Enum):
    """Méthodes de calcul supportées"""
    GENIE_RURAL = "formule_genie_rural"
    OMS = "formule_oms"
    EMPIRIQUE = "formule_empirique"
    STANDARD = "formule_standard"
    POPULATION = "formule_population"
    ZONE = "formule_zone"
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

class TypeCourbe(Enum):
    """Types de courbes supportés"""
    JOURNALIERE = "journaliere"
    HORAIRE = "horaire"
    SAISONNIERE = "saisonniere"
    PERSONNALISEE = "personnalisee"

class MethodeCalcul(Enum):
    """Méthodes de calcul supportées"""
    GENIE_RURAL = "formule_genie_rural"
    OMS = "formule_oms"
    EMPIRIQUE = "formule_empirique"
    STANDARD = "formule_standard"
    POPULATION = "formule_population"
    ZONE = "formule_zone"

@dataclass
class LoadCurvePoint:
    """Point d'une courbe de charge"""
    heure: int
    coefficient: float
    description: str
    unite: str = ""

@dataclass
class LoadCurve:
    """Courbe de charge complète"""
    nom: str
    type: TypeCourbe
    points: List[LoadCurvePoint]
    coefficient_moyen: float
    coefficient_max: float
    description: str
    unite: str = ""
    zone: str = "standard"

@dataclass
class CalculResult:
    """Résultat d'un calcul de coefficient"""
    valeur: float
    methode: str
    unite: str = ""
    description: str = ""

class AEPLoadCurveManager:
    """Gestionnaire des courbes de charge AEP"""
    
    def __init__(self):
        self.courbes_standard = self._initialiser_courbes_standard()
        self.courbes_zones = {}  # Courbes par zone/village
        self.methodes_supportees = {
            MethodeCalcul.GENIE_RURAL: "Formule génie rural",
            MethodeCalcul.OMS: "Formule OMS",
            MethodeCalcul.EMPIRIQUE: "Formule empirique",
            MethodeCalcul.STANDARD: "Formule standard",
            MethodeCalcul.POPULATION: "Formule basée sur la population",
            MethodeCalcul.ZONE: "Formule basée sur le type de zone"
        }
    
    def _valider_entrees_positives(self, **kwargs) -> None:
        """
        Valide que les entrées sont positives
        
        Args:
            **kwargs: Paramètres à valider
            
        Raises:
            ValueError: Si un paramètre n'est pas positif
        """
        for nom, valeur in kwargs.items():
            if not isinstance(valeur, (int, float)) or valeur <= 0:
                raise ValueError(f"Le paramètre '{nom}' doit être un nombre positif strictement supérieur à 0 (valeur reçue: {valeur})")
    
    def _initialiser_courbes_standard(self) -> Dict[str, LoadCurve]:
        """Initialise les courbes de charge standard"""
        courbes = {}
        
        # Courbe de charge journalière standard
        courbes["journaliere_standard"] = LoadCurve(
            nom="Courbe journalière standard",
            type=TypeCourbe.JOURNALIERE,
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
            description="Courbe de charge journalière standard pour zones résidentielles",
            unite="",
            zone="standard"
        )
        
        # Courbe de charge horaire détaillée
        courbes["horaire_detaille"] = LoadCurve(
            nom="Courbe horaire détaillée",
            type=TypeCourbe.HORAIRE,
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
            description="Courbe de charge horaire détaillée sur 24h",
            unite="",
            zone="standard"
        )
        
        # Courbe de charge saisonnière
        courbes["saisonniere"] = LoadCurve(
            nom="Courbe saisonnière",
            type=TypeCourbe.SAISONNIERE,
            points=[
                LoadCurvePoint(1, 0.8, "Janvier - Hiver"),
                LoadCurvePoint(2, 0.7, "Février - Hiver"),
                LoadCurvePoint(3, 0.9, "Mars - Printemps"),
                LoadCurvePoint(4, 1.0, "Avril - Printemps"),
                LoadCurvePoint(5, 1.1, "Mai - Printemps"),
                LoadCurvePoint(6, 1.2, "Juin - Été"),
                LoadCurvePoint(7, 1.4, "Juillet - Été"),
                LoadCurvePoint(8, 1.3, "Août - Été"),
                LoadCurvePoint(9, 1.1, "Septembre - Automne"),
                LoadCurvePoint(10, 1.0, "Octobre - Automne"),
                LoadCurvePoint(11, 0.9, "Novembre - Automne"),
                LoadCurvePoint(12, 0.8, "Décembre - Hiver")
            ],
            coefficient_moyen=1.0,
            coefficient_max=1.4,
            description="Courbe de charge saisonnière sur 12 mois",
            unite="",
            zone="standard"
        )
        
        return courbes
    
    def lister_courbes_disponibles(self) -> List[str]:
        """Liste toutes les courbes disponibles"""
        return list(self.courbes_standard.keys()) + list(self.courbes_zones.keys())
    
    def obtenir_courbe(self, nom_courbe: str) -> Optional[LoadCurve]:
        """Obtient une courbe par son nom"""
        return self.courbes_standard.get(nom_courbe) or self.courbes_zones.get(nom_courbe)
    
    def calculer_coefficient_pointe_unifie(
        self,
        parametres: Dict[str, Any],
        methodes: List[MethodeCalcul],
        type_calcul: str = "horaire"
    ) -> Dict[str, CalculResult]:
        """
        Méthode unifiée pour calculer les coefficients de pointe
        
        Args:
            parametres: Dictionnaire des paramètres selon le type de calcul
            methodes: Liste des méthodes à utiliser
            type_calcul: Type de calcul ("horaire" ou "journalier")
            
        Returns:
            Dictionnaire des résultats par méthode
        """
        resultats = {}
        
        for methode in methodes:
            try:
                if type_calcul == "horaire":
                    valeur = self._calculer_coefficient_pointe_horaire_par_methode(
                        methode, **parametres
                    )
                else:  # journalier
                    valeur = self._calculer_coefficient_pointe_journalier_par_methode(
                        methode, **parametres
                    )
                
                resultats[methode.value] = CalculResult(
                    valeur=valeur,
                    methode=self.methodes_supportees[methode],
                    unite="",
                    description=f"Coefficient de pointe {type_calcul} - {self.methodes_supportees[methode]}"
                )
            except Exception as e:
                resultats[methode.value] = CalculResult(
                    valeur=0.0,
                    methode=self.methodes_supportees[methode],
                    unite="",
                    description=f"Erreur: {str(e)}"
                )
        
        return resultats
    
    def _calculer_coefficient_pointe_horaire_par_methode(
        self, methode: MethodeCalcul, **kwargs
    ) -> float:
        """Calcule le coefficient de pointe horaire selon la méthode spécifiée"""
        if methode == MethodeCalcul.GENIE_RURAL:
            debit_moyen = kwargs.get('debit_moyen_horaire_m3h')
            self._valider_entrees_positives(debit_moyen_horaire_m3h=debit_moyen)
            return 1.5 + 2.5 / math.sqrt(debit_moyen)
        
        elif methode == MethodeCalcul.OMS:
            return 1.8
        
        elif methode == MethodeCalcul.EMPIRIQUE:
            debit_moyen = kwargs.get('debit_moyen_horaire_m3h')
            self._valider_entrees_positives(debit_moyen_horaire_m3h=debit_moyen)
            return 1.5 + 1.0 / math.log10(debit_moyen + 1)
        
        else:
            raise ValueError(f"Méthode non supportée pour le calcul horaire: {methode.value}")
    
    def _calculer_coefficient_pointe_journalier_par_methode(
        self, methode: MethodeCalcul, **kwargs
    ) -> float:
        """Calcule le coefficient de pointe journalier selon la méthode spécifiée"""
        if methode == MethodeCalcul.STANDARD:
            return 1.5
        
        elif methode == MethodeCalcul.POPULATION:
            population = kwargs.get('population')
            self._valider_entrees_positives(population=population)
            return 1.5 + 0.5 / math.sqrt(population / 1000)
        
        elif methode == MethodeCalcul.ZONE:
            population = kwargs.get('population')
            self._valider_entrees_positives(population=population)
            if population < 1000:
                return 1.8  # Zone rurale
            elif population < 10000:
                return 1.6  # Zone semi-urbaine
            else:
                return 1.4  # Zone urbaine
        
        else:
            raise ValueError(f"Méthode non supportée pour le calcul journalier: {methode.value}")
    
    def calculer_coefficient_pointe_horaire(
        self,
        debit_moyen_horaire_m3h: float,
        methode: str = "formule_genie_rural"
    ) -> float:
        """
        Calcule le coefficient de pointe horaire
        
        Args:
            debit_moyen_horaire_m3h: Débit moyen horaire en m³/h
            methode: Méthode de calcul
            
        Returns:
            Coefficient de pointe horaire
        """
        self._valider_entrees_positives(debit_moyen_horaire_m3h=debit_moyen_horaire_m3h)
        
        try:
            methode_enum = MethodeCalcul(methode)
            return self._calculer_coefficient_pointe_horaire_par_methode(
                methode_enum, debit_moyen_horaire_m3h=debit_moyen_horaire_m3h
            )
        except ValueError:
            raise ValueError(f"Méthode non supportée: {methode}")
    
    def calculer_coefficient_pointe_journalier(
        self,
        population: int,
        methode: str = "formule_standard"
    ) -> float:
        """
        Calcule le coefficient de pointe journalier
        
        Args:
            population: Population en habitants
            methode: Méthode de calcul
            
        Returns:
            Coefficient de pointe journalier
        """
        self._valider_entrees_positives(population=population)
        
        try:
            methode_enum = MethodeCalcul(methode)
            return self._calculer_coefficient_pointe_journalier_par_methode(
                methode_enum, population=population
            )
        except ValueError:
            raise ValueError(f"Méthode non supportée: {methode}")
    
    def calculer_coefficient_pointe_global(
        self,
        population: int,
        debit_moyen_horaire_m3h: float,
        methode_journaliere: str = "formule_standard",
        methode_horaire: str = "formule_genie_rural"
    ) -> Dict[str, float]:
        """
        Calcule le coefficient de pointe global
        
        Args:
            population: Population en habitants
            debit_moyen_horaire_m3h: Débit moyen horaire en m³/h
            methode_journaliere: Méthode pour le coefficient journalier
            methode_horaire: Méthode pour le coefficient horaire
            
        Returns:
            Dictionnaire avec tous les coefficients
        """
        self._valider_entrees_positives(
            population=population, 
            debit_moyen_horaire_m3h=debit_moyen_horaire_m3h
        )
        
        coefficient_journalier = self.calculer_coefficient_pointe_journalier(
            population, methode_journaliere
        )
        coefficient_horaire = self.calculer_coefficient_pointe_horaire(
            debit_moyen_horaire_m3h, methode_horaire
        )
        coefficient_global = coefficient_journalier * coefficient_horaire
        
        return {
            "coefficient_pointe_journalier": round(coefficient_journalier, 3),
            "coefficient_pointe_horaire": round(coefficient_horaire, 3),
            "coefficient_pointe_global": round(coefficient_global, 3)
        }
    
    def generer_courbe_personnalisee(
        self,
        nom: str,
        type_courbe: str,
        points: List[Tuple[int, float, str]],
        zone: str = "personnalisee"
    ) -> LoadCurve:
        """
        Génère une courbe personnalisée
        
        Args:
            nom: Nom de la courbe
            type_courbe: Type de courbe
            points: Liste des points (heure, coefficient, description)
            zone: Zone associée à la courbe
            
        Returns:
            Courbe personnalisée
        """
        if not points:
            raise ValueError("La liste des points ne peut pas être vide")
        
        # Valider les coefficients
        coefficients = [point[1] for point in points]
        if any(c <= 0 for c in coefficients):
            raise ValueError("Tous les coefficients doivent être positifs")
        
        # Créer les points de courbe
        points_courbe = [
            LoadCurvePoint(heure, coefficient, description)
            for heure, coefficient, description in points
        ]
        
        # Calculer les statistiques
        coefficient_moyen = sum(coefficients) / len(coefficients)
        coefficient_max = max(coefficients)
        
        # Créer la courbe
        courbe = LoadCurve(
            nom=nom,
            type=TypeCourbe.PERSONNALISEE,
            points=points_courbe,
            coefficient_moyen=round(coefficient_moyen, 3),
            coefficient_max=round(coefficient_max, 3),
            description=f"Courbe personnalisée: {nom}",
            zone=zone
        )
        
        # Stocker la courbe
        self.courbes_zones[nom] = courbe
        
        return courbe
    
    def calculer_besoin_pointe(
        self,
        besoin_moyen_journalier: float,
        coefficient_pointe_journalier: float,
        coefficient_pointe_horaire: float
    ) -> Dict[str, float]:
        """
        Calcule les besoins de pointe
        
        Args:
            besoin_moyen_journalier: Besoin moyen journalier en m³/j
            coefficient_pointe_journalier: Coefficient de pointe journalier
            coefficient_pointe_horaire: Coefficient de pointe horaire
            
        Returns:
            Dictionnaire avec tous les besoins
        """
        self._valider_entrees_positives(
            besoin_moyen_journalier=besoin_moyen_journalier,
            coefficient_pointe_journalier=coefficient_pointe_journalier,
            coefficient_pointe_horaire=coefficient_pointe_horaire
        )
        
        besoin_pointe_journalier = besoin_moyen_journalier * coefficient_pointe_journalier
        coefficient_pointe_global = coefficient_pointe_journalier * coefficient_pointe_horaire
        besoin_pointe_horaire = besoin_moyen_journalier * coefficient_pointe_global / 24
        
        return {
            "besoin_moyen_journalier_m3_j": round(besoin_moyen_journalier, 2),
            "besoin_pointe_journalier_m3_j": round(besoin_pointe_journalier, 2),
            "besoin_pointe_horaire_m3_h": round(besoin_pointe_horaire, 2),
            "coefficient_pointe_global": round(coefficient_pointe_global, 3)
        }
    
    def ajouter_courbe_zone(
        self,
        nom_zone: str,
        courbe: LoadCurve
    ) -> bool:
        """
        Ajoute une courbe pour une zone spécifique
        
        Args:
            nom_zone: Nom de la zone/village
            courbe: Courbe à ajouter
            
        Returns:
            True si ajouté avec succès
        """
        if nom_zone in self.courbes_zones:
            return False  # Zone déjà existante
        
        courbe.zone = nom_zone
        self.courbes_zones[nom_zone] = courbe
        return True
    
    def obtenir_courbes_zone(self, nom_zone: str) -> Optional[LoadCurve]:
        """Obtient la courbe d'une zone spécifique"""
        return self.courbes_zones.get(nom_zone)
    
    def lister_zones(self) -> List[str]:
        """Liste toutes les zones avec courbes personnalisées"""
        return list(self.courbes_zones.keys())
    
    def generer_graphique_courbe(
        self,
        nom_courbe: str,
        format_sortie: str = "png",
        chemin_fichier: Optional[str] = None
    ) -> str:
        """
        Génère un graphique de courbe de charge
        
        Args:
            nom_courbe: Nom de la courbe à visualiser
            format_sortie: Format de sortie ("png", "jpg", "pdf")
            chemin_fichier: Chemin du fichier de sortie (optionnel)
            
        Returns:
            Chemin du fichier généré
        """
        courbe = self.obtenir_courbe(nom_courbe)
        if not courbe:
            raise ValueError(f"Courbe non trouvée: {nom_courbe}")
        
        # Extraire les données
        heures = [point.heure for point in courbe.points]
        coefficients = [point.coefficient for point in courbe.points]
        
        # Créer le graphique
        plt.figure(figsize=(12, 8))
        
        if courbe.type == TypeCourbe.SAISONNIERE:
            # Graphique saisonnier
            mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", 
                   "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"]
            plt.plot(mois, coefficients, 'o-', linewidth=2, markersize=8)
            plt.xlabel('Mois')
            plt.ylabel('Coefficient')
            plt.title(f'Courbe de charge saisonnière: {courbe.nom}')
            plt.grid(True, alpha=0.3)
            
        else:
            # Graphique journalier/horaire
            plt.plot(heures, coefficients, 'o-', linewidth=2, markersize=6)
            plt.xlabel('Heure')
            plt.ylabel('Coefficient')
            plt.title(f'Courbe de charge: {courbe.nom}')
            plt.grid(True, alpha=0.3)
            
            # Ajouter des annotations pour les points importants
            for point in courbe.points:
                if point.coefficient > 1.5:  # Points de pointe
                    plt.annotate(
                        point.description,
                        xy=(point.heure, point.coefficient),
                        xytext=(10, 10),
                        textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                    )
        
        # Ajouter des informations statistiques
        plt.figtext(0.02, 0.02, 
                   f'Coefficient moyen: {courbe.coefficient_moyen:.3f}\n'
                   f'Coefficient max: {courbe.coefficient_max:.3f}\n'
                   f'Zone: {courbe.zone}',
                   fontsize=10, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        
        # Sauvegarder ou retourner
        if chemin_fichier:
            plt.savefig(chemin_fichier, format=format_sortie, dpi=300, bbox_inches='tight')
            plt.close()
            return chemin_fichier
        else:
            # Générer un nom de fichier automatique
            nom_fichier = f"courbe_{nom_courbe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_sortie}"
            plt.savefig(nom_fichier, format=format_sortie, dpi=300, bbox_inches='tight')
            plt.close()
            return nom_fichier
    
    def exporter_courbe_json(self, nom_courbe: str) -> str:
        """Exporte une courbe au format JSON"""
        courbe = self.obtenir_courbe(nom_courbe)
        if not courbe:
            raise ValueError(f"Courbe non trouvée: {nom_courbe}")
        
        data = {
            "nom": courbe.nom,
            "type": courbe.type.value,
            "zone": courbe.zone,
            "description": courbe.description,
            "coefficient_moyen": courbe.coefficient_moyen,
            "coefficient_max": courbe.coefficient_max,
            "unite": courbe.unite,
            "points": [
                {
                    "heure": point.heure,
                    "coefficient": point.coefficient,
                    "description": point.description,
                    "unite": point.unite
                }
                for point in courbe.points
            ]
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def importer_courbe_json(self, json_data: str) -> LoadCurve:
        """Importe une courbe depuis un JSON"""
        data = json.loads(json_data)
        
        # Créer les points
        points = [
            LoadCurvePoint(
                heure=point["heure"],
                coefficient=point["coefficient"],
                description=point["description"],
                unite=point.get("unite", "")
            )
            for point in data["points"]
        ]
        
        # Créer la courbe
        courbe = LoadCurve(
            nom=data["nom"],
            type=TypeCourbe(data["type"]),
            points=points,
            coefficient_moyen=data["coefficient_moyen"],
            coefficient_max=data["coefficient_max"],
            description=data["description"],
            unite=data.get("unite", ""),
            zone=data.get("zone", "importee")
        )
        
        # Stocker la courbe
        self.courbes_zones[data["nom"]] = courbe
        
        return courbe
    
    def generer_rapport_dimensionnement(
        self,
        population: int,
        dotation: float,
        nom_courbe: str = "horaire_detaille"
    ) -> Dict[str, Any]:
        """
        Génère un rapport de dimensionnement basé sur une courbe
        
        Args:
            population: Population en habitants
            dotation: Dotation en L/j/hab
            nom_courbe: Nom de la courbe à utiliser
            
        Returns:
            Rapport de dimensionnement
        """
        self._valider_entrees_positives(population=population, dotation=dotation)
        
        courbe = self.obtenir_courbe(nom_courbe)
        if not courbe:
            raise ValueError(f"Courbe non trouvée: {nom_courbe}")
        
        # Calculs de base
        besoin_moyen_journalier = population * dotation / 1000  # m³/j
        
        # Coefficients de pointe
        coefficients = self.calculer_coefficient_pointe_global(
            population=population,
            debit_moyen_horaire_m3h=besoin_moyen_journalier / 24
        )
        
        # Besoins de pointe
        besoins = self.calculer_besoin_pointe(
            besoin_moyen_journalier=besoin_moyen_journalier,
            coefficient_pointe_journalier=coefficients["coefficient_pointe_journalier"],
            coefficient_pointe_horaire=coefficients["coefficient_pointe_horaire"]
        )
        
        # Dimensionnement des équipements
        volume_reservoir = besoins["besoin_pointe_journalier_m3_j"] * 0.3  # 30% du besoin journalier
        puissance_pompe = besoins["besoin_pointe_horaire_m3_h"] * 2.5  # kW (approximatif)
        
        return {
            "parametres_entree": {
                "population": population,
                "dotation_l_j_hab": dotation,
                "courbe_utilisee": nom_courbe
            },
            "besoins": {
                "besoin_moyen_journalier_m3_j": round(besoin_moyen_journalier, 2),
                "besoin_pointe_journalier_m3_j": round(besoins["besoin_pointe_journalier_m3_j"], 2),
                "besoin_pointe_horaire_m3_h": round(besoins["besoin_pointe_horaire_m3_h"], 2)
            },
            "coefficients_pointe": coefficients,
            "dimensionnement_equipements": {
                "volume_reservoir_m3": round(volume_reservoir, 1),
                "puissance_pompe_kw": round(puissance_pompe, 1),
                "diametre_conduite_mm": self._estimer_diametre_conduite(besoins["besoin_pointe_horaire_m3_h"])
            },
            "courbe_utilisee": {
                "nom": courbe.nom,
                "type": courbe.type.value,
                "coefficient_max": courbe.coefficient_max,
                "zone": courbe.zone
            }
        }
    
    def _estimer_diametre_conduite(self, debit_horaire_m3h: float) -> int:
        """Estime le diamètre de conduite basé sur le débit"""
        # Formule simplifiée: D = sqrt(4 * Q / (π * v))
        # v = 1.5 m/s (vitesse recommandée)
        vitesse = 1.5  # m/s
        debit_ms = debit_horaire_m3h / 3600  # m³/s
        
        diametre_m = (4 * debit_ms / (math.pi * vitesse)) ** 0.5
        diametre_mm = diametre_m * 1000
        
        # Arrondir aux diamètres commerciaux standards
        diametres_standards = [50, 63, 75, 90, 110, 125, 140, 160, 180, 200, 225, 250, 280, 315, 355, 400]
        
        for diametre_std in diametres_standards:
            if diametre_mm <= diametre_std:
                return diametre_std
        
        return 400  # Diamètre maximum dans la liste
    
    def generer_rapport_complet(
        self,
        population: int,
        dotation: float,
        nom_courbe: str = "horaire_detaille",
        format_sortie: str = "json"
    ) -> str:
        """
        Génère un rapport complet de dimensionnement
        
        Args:
            population: Population en habitants
            dotation: Dotation en L/j/hab
            nom_courbe: Nom de la courbe à utiliser
            format_sortie: Format de sortie ("json", "markdown", "html")
            
        Returns:
            Rapport formaté
        """
        rapport_data = self.generer_rapport_dimensionnement(population, dotation, nom_courbe)
        
        if format_sortie == "json":
            return json.dumps(rapport_data, indent=2, ensure_ascii=False)
        elif format_sortie == "markdown":
            return self._generer_rapport_markdown(rapport_data)
        elif format_sortie == "html":
            return self._generer_rapport_html(rapport_data)
        else:
            raise ValueError(f"Format de sortie non supporté: {format_sortie}")
    
    def _generer_rapport_markdown(self, rapport_data: Dict[str, Any]) -> str:
        """Génère un rapport Markdown"""
        rapport = f"# 📊 Rapport de Dimensionnement AEP\n\n"
        rapport += f"**Date d'analyse:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Paramètres d'entrée
        rapport += "## 🎯 Paramètres d'Entrée\n\n"
        params = rapport_data["parametres_entree"]
        rapport += f"- **Population:** {params['population']:,} habitants\n"
        rapport += f"- **Dotation:** {params['dotation_l_j_hab']} L/j/hab\n"
        rapport += f"- **Courbe utilisée:** {params['courbe_utilisee']}\n\n"
        
        # Besoins
        rapport += "## 💧 Besoins en Eau\n\n"
        besoins = rapport_data["besoins"]
        rapport += f"- **Besoin moyen journalier:** {besoins['besoin_moyen_journalier_m3_j']} m³/j\n"
        rapport += f"- **Besoin de pointe journalier:** {besoins['besoin_pointe_journalier_m3_j']} m³/j\n"
        rapport += f"- **Besoin de pointe horaire:** {besoins['besoin_pointe_horaire_m3_h']} m³/h\n\n"
        
        # Coefficients de pointe
        rapport += "## 📈 Coefficients de Pointe\n\n"
        coeffs = rapport_data["coefficients_pointe"]
        rapport += f"- **Coefficient journalier:** {coeffs['coefficient_pointe_journalier']}\n"
        rapport += f"- **Coefficient horaire:** {coeffs['coefficient_pointe_horaire']}\n"
        rapport += f"- **Coefficient global:** {coeffs['coefficient_pointe_global']}\n\n"
        
        # Dimensionnement
        rapport += "## 🔧 Dimensionnement des Équipements\n\n"
        equip = rapport_data["dimensionnement_equipements"]
        rapport += f"- **Volume réservoir:** {equip['volume_reservoir_m3']} m³\n"
        rapport += f"- **Puissance pompe:** {equip['puissance_pompe_kw']} kW\n"
        rapport += f"- **Diamètre conduite:** {equip['diametre_conduite_mm']} mm\n\n"
        
        # Courbe utilisée
        rapport += "## 📋 Courbe de Charge Utilisée\n\n"
        courbe = rapport_data["courbe_utilisee"]
        rapport += f"- **Nom:** {courbe['nom']}\n"
        rapport += f"- **Type:** {courbe['type']}\n"
        rapport += f"- **Coefficient max:** {courbe['coefficient_max']}\n"
        rapport += f"- **Zone:** {courbe['zone']}\n\n"
        
        return rapport
    
    def _generer_rapport_html(self, rapport_data: Dict[str, Any]) -> str:
        """Génère un rapport HTML"""
        rapport = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rapport de Dimensionnement AEP</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .parametre {{ margin: 10px 0; }}
                .valeur {{ font-weight: bold; color: #1976d2; }}
                .equipement {{ background-color: #f5f5f5; padding: 10px; margin: 5px 0; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <h1>📊 Rapport de Dimensionnement AEP</h1>
            <p><strong>Date d'analyse:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """
        
        # Paramètres d'entrée
        params = rapport_data["parametres_entree"]
        rapport += f"""
            <div class="section">
                <h2>🎯 Paramètres d'Entrée</h2>
                <div class="parametre">Population: <span class="valeur">{params['population']:,} habitants</span></div>
                <div class="parametre">Dotation: <span class="valeur">{params['dotation_l_j_hab']} L/j/hab</span></div>
                <div class="parametre">Courbe utilisée: <span class="valeur">{params['courbe_utilisee']}</span></div>
            </div>
        """
        
        # Besoins
        besoins = rapport_data["besoins"]
        rapport += f"""
            <div class="section">
                <h2>💧 Besoins en Eau</h2>
                <div class="parametre">Besoin moyen journalier: <span class="valeur">{besoins['besoin_moyen_journalier_m3_j']} m³/j</span></div>
                <div class="parametre">Besoin de pointe journalier: <span class="valeur">{besoins['besoin_pointe_journalier_m3_j']} m³/j</span></div>
                <div class="parametre">Besoin de pointe horaire: <span class="valeur">{besoins['besoin_pointe_horaire_m3_h']} m³/h</span></div>
            </div>
        """
        
        # Coefficients
        coeffs = rapport_data["coefficients_pointe"]
        rapport += f"""
            <div class="section">
                <h2>📈 Coefficients de Pointe</h2>
                <div class="parametre">Coefficient journalier: <span class="valeur">{coeffs['coefficient_pointe_journalier']}</span></div>
                <div class="parametre">Coefficient horaire: <span class="valeur">{coeffs['coefficient_pointe_horaire']}</span></div>
                <div class="parametre">Coefficient global: <span class="valeur">{coeffs['coefficient_pointe_global']}</span></div>
            </div>
        """
        
        # Dimensionnement
        equip = rapport_data["dimensionnement_equipements"]
        rapport += f"""
            <div class="section">
                <h2>🔧 Dimensionnement des Équipements</h2>
                <div class="equipement">Volume réservoir: <span class="valeur">{equip['volume_reservoir_m3']} m³</span></div>
                <div class="equipement">Puissance pompe: <span class="valeur">{equip['puissance_pompe_kw']} kW</span></div>
                <div class="equipement">Diamètre conduite: <span class="valeur">{equip['diametre_conduite_mm']} mm</span></div>
            </div>
        """
        
        # Courbe
        courbe = rapport_data["courbe_utilisee"]
        rapport += f"""
            <div class="section">
                <h2>📋 Courbe de Charge Utilisée</h2>
                <div class="parametre">Nom: <span class="valeur">{courbe['nom']}</span></div>
                <div class="parametre">Type: <span class="valeur">{courbe['type']}</span></div>
                <div class="parametre">Coefficient max: <span class="valeur">{courbe['coefficient_max']}</span></div>
                <div class="parametre">Zone: <span class="valeur">{courbe['zone']}</span></div>
            </div>
        </body>
        </html>
        """
        
        return rapport
    
    def comparer_methodes_calcul(
        self,
        population: int,
        debit_moyen_horaire_m3h: float
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare différentes méthodes de calcul de coefficients
        
        Args:
            population: Population en habitants
            debit_moyen_horaire_m3h: Débit moyen horaire en m³/h
            
        Returns:
            Comparaison des méthodes
        """
        self._valider_entrees_positives(
            population=population, 
            debit_moyen_horaire_m3h=debit_moyen_horaire_m3h
        )
        
        resultats = {
            "coefficients_journaliers": {},
            "coefficients_horaires": {},
            "coefficients_globaux": {}
        }
        
        # Méthodes journalières
        methodes_journalieres = [
            MethodeCalcul.STANDARD,
            MethodeCalcul.POPULATION,
            MethodeCalcul.ZONE
        ]
        
        for methode in methodes_journalieres:
            try:
                coeff_j = self._calculer_coefficient_pointe_journalier_par_methode(
                    methode, population=population
                )
                resultats["coefficients_journaliers"][methode.value] = round(coeff_j, 3)
            except Exception as e:
                resultats["coefficients_journaliers"][methode.value] = f"Erreur: {str(e)}"
        
        # Méthodes horaires
        methodes_horaires = [
            MethodeCalcul.GENIE_RURAL,
            MethodeCalcul.OMS,
            MethodeCalcul.EMPIRIQUE
        ]
        
        for methode in methodes_horaires:
            try:
                coeff_h = self._calculer_coefficient_pointe_horaire_par_methode(
                    methode, debit_moyen_horaire_m3h=debit_moyen_horaire_m3h
                )
                resultats["coefficients_horaires"][methode.value] = round(coeff_h, 3)
            except Exception as e:
                resultats["coefficients_horaires"][methode.value] = f"Erreur: {str(e)}"
        
        # Coefficients globaux
        for methode_j in resultats["coefficients_journaliers"]:
            if isinstance(resultats["coefficients_journaliers"][methode_j], (int, float)):
                for methode_h in resultats["coefficients_horaires"]:
                    if isinstance(resultats["coefficients_horaires"][methode_h], (int, float)):
                        coeff_global = (resultats["coefficients_journaliers"][methode_j] * 
                                      resultats["coefficients_horaires"][methode_h])
                        nom_global = f"{methode_j} + {methode_h}"
                        resultats["coefficients_globaux"][nom_global] = round(coeff_global, 3)
        
        return resultats
    
    def analyser_sensibilite_courbe(
        self,
        population: int,
        dotation: float,
        nom_courbe: str = "horaire_detaille",
        variation_population: float = 10.0,
        variation_dotation: float = 10.0
    ) -> Dict[str, Any]:
        """
        Analyse la sensibilité des résultats aux variations des paramètres
        
        Args:
            population: Population de référence
            dotation: Dotation de référence
            nom_courbe: Nom de la courbe
            variation_population: Variation de population en %
            variation_dotation: Variation de dotation en %
            
        Returns:
            Analyse de sensibilité
        """
        self._valider_entrees_positives(
            population=population, 
            dotation=dotation
        )
        
        # Calcul de référence
        rapport_ref = self.generer_rapport_dimensionnement(population, dotation, nom_courbe)
        
        # Variations de population
        pop_min = population * (1 - variation_population / 100)
        pop_max = population * (1 + variation_population / 100)
        
        rapport_pop_min = self.generer_rapport_dimensionnement(int(pop_min), dotation, nom_courbe)
        rapport_pop_max = self.generer_rapport_dimensionnement(int(pop_max), dotation, nom_courbe)
        
        # Variations de dotation
        dot_min = dotation * (1 - variation_dotation / 100)
        dot_max = dotation * (1 + variation_dotation / 100)
        
        rapport_dot_min = self.generer_rapport_dimensionnement(population, dot_min, nom_courbe)
        rapport_dot_max = self.generer_rapport_dimensionnement(population, dot_max, nom_courbe)
        
        return {
            "parametres_reference": {
                "population": population,
                "dotation": dotation,
                "variation_population_pct": variation_population,
                "variation_dotation_pct": variation_dotation
            },
            "resultats_reference": rapport_ref,
            "sensibilite_population": {
                "population_min": int(pop_min),
                "population_max": int(pop_max),
                "impact_besoin_min": rapport_pop_min["besoins"]["besoin_moyen_journalier_m3_j"],
                "impact_besoin_max": rapport_pop_max["besoins"]["besoin_moyen_journalier_m3_j"],
                "variation_besoin_pct": ((rapport_pop_max["besoins"]["besoin_moyen_journalier_m3_j"] - 
                                        rapport_pop_min["besoins"]["besoin_moyen_journalier_m3_j"]) / 
                                       rapport_ref["besoins"]["besoin_moyen_journalier_m3_j"] * 100)
            },
            "sensibilite_dotation": {
                "dotation_min": dot_min,
                "dotation_max": dot_max,
                "impact_besoin_min": rapport_dot_min["besoins"]["besoin_moyen_journalier_m3_j"],
                "impact_besoin_max": rapport_dot_max["besoins"]["besoin_moyen_journalier_m3_j"],
                "variation_besoin_pct": ((rapport_dot_max["besoins"]["besoin_moyen_journalier_m3_j"] - 
                                        rapport_dot_min["besoins"]["besoin_moyen_journalier_m3_j"]) / 
                                       rapport_ref["besoins"]["besoin_moyen_journalier_m3_j"] * 100)
            }
        }
