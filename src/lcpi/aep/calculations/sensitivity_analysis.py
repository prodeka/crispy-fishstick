"""
Analyse de sensibilité AEP - version améliorée

Ce module implémente l'analyse de sensibilité des paramètres clés
selon les besoins métier des ingénieurs AEP avec des améliorations
pour la robustesse, la maintenabilité et les fonctionnalités.
"""

import math
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional, Callable
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np

@dataclass
class SensitivityParameter:
    """Paramètre pour l'analyse de sensibilité"""
    nom: str
    valeur_base: float
    variation_pct: float
    pas: float
    unite: str
    description: str

@dataclass
class SensitivityResult:
    """Résultat d'une analyse de sensibilité"""
    parametre: str
    variations: List[float]
    impacts: List[float]
    impact_max: float
    impact_min: float
    impact_moyen: float
    classe_impact: str
    poids_relatif: float  # Nouveau : importance relative du paramètre

class AEPSensitivityAnalyzer:
    """Analyseur de sensibilité pour les calculs AEP - Version améliorée"""
    
    def __init__(self):
        # Définition centralisée des paramètres
        self.parametres_standard = {
            "dotation": SensitivityParameter(
                nom="dotation",
                valeur_base=60.0,
                variation_pct=10.0,
                pas=2.0,
                unite="L/j/hab",
                description="Dotation en eau par habitant"
            ),
            "croissance_demographique": SensitivityParameter(
                nom="croissance_demographique",
                valeur_base=0.025,
                variation_pct=30.0,
                pas=0.005,
                unite="%/an",
                description="Taux de croissance démographique"
            ),
            "fuites": SensitivityParameter(
                nom="fuites",
                valeur_base=0.05,
                variation_pct=20.0,
                pas=0.01,
                unite="%",
                description="Taux de fuites du réseau"
            ),
            "coefficient_pointe": SensitivityParameter(
                nom="coefficient_pointe",
                valeur_base=1.5,
                variation_pct=15.0,
                pas=0.1,
                unite="",
                description="Coefficient de pointe journalière"
            )
        }
    
    def _valider_parametres(self, population: int, dotation: float, rendement: float) -> None:
        """Valide les paramètres d'entrée"""
        if population <= 0:
            raise ValueError("La population doit être strictement positive")
        if dotation <= 0:
            raise ValueError("La dotation doit être strictement positive")
        if not 0 < rendement <= 1:
            raise ValueError("Le rendement doit être entre 0 et 1")
    
    def _classifier_impact(self, impact_max: float) -> str:
        """Classifie l'impact selon des seuils standardisés"""
        if abs(impact_max) > 25:
            return "élevé"
        elif abs(impact_max) > 10:
            return "moyen"
        else:
            return "faible"
    
    def _calculer_poids_relatif(self, impact_max: float, impacts_totaux: List[float]) -> float:
        """Calcule le poids relatif du paramètre par rapport aux autres"""
        if not impacts_totaux:
            return 0.0
        max_global = max(abs(imp) for imp in impacts_totaux)
        return abs(impact_max) / max_global if max_global > 0 else 0.0
    
    def analyser_parametre(
        self,
        param: SensitivityParameter,
        calc_impact: Callable[[float], float],
        impacts_totaux: Optional[List[float]] = None
    ) -> SensitivityResult:
        """
        Méthode générique pour analyser la sensibilité d'un paramètre
        
        Args:
            param: Paramètre à analyser
            calc_impact: Fonction qui calcule l'impact d'une variation
            impacts_totaux: Liste des impacts max de tous les paramètres (pour poids relatif)
            
        Returns:
            Résultat de l'analyse de sensibilité
        """
        variations = []
        impacts = []
        pas = param.pas
        nb_points = int(param.variation_pct / pas)
        
        # Calcul vectorisé des variations
        for i in range(-nb_points, nb_points + 1):
            valeur_variee = param.valeur_base * (1 + i * pas / 100)
            variations.append(valeur_variee)
            impacts.append(calc_impact(valeur_variee))
        
        # Analyse des résultats
        impact_max = max(impacts)
        impact_min = min(impacts)
        impact_moyen = sum(impacts) / len(impacts)
        
        # Classification et poids relatif
        classe = self._classifier_impact(impact_max)
        poids_relatif = self._calculer_poids_relatif(impact_max, impacts_totaux or [impact_max])
        
        return SensitivityResult(
            parametre=param.nom,
            variations=variations,
            impacts=impacts,
            impact_max=impact_max,
            impact_min=impact_min,
            impact_moyen=impact_moyen,
            classe_impact=classe,
            poids_relatif=poids_relatif
        )
    
    def analyser_sensibilite_dotation(
        self, 
        population: int, 
        dotation_base: float = 60.0,
        variation_pct: float = 10.0,
        pas: float = 2.0
    ) -> SensitivityResult:
        """
        Analyse la sensibilité des besoins en eau aux variations de dotation
        
        Args:
            population: Population de référence
            dotation_base: Dotation de base (L/j/hab)
            variation_pct: Variation en pourcentage (±%)
            pas: Pas de variation
            
        Returns:
            Résultat de l'analyse de sensibilité
        """
        self._valider_parametres(population, dotation_base, 0.95)
        
        def calc_impact_dotation(valeur):
            besoin_base = population * dotation_base / 1000  # m³/jour
            besoin_variation = population * valeur / 1000  # m³/jour
            return ((besoin_variation - besoin_base) / besoin_base) * 100
        
        param = SensitivityParameter(
            nom="dotation",
            valeur_base=dotation_base,
            variation_pct=variation_pct,
            pas=pas,
            unite="L/j/hab",
            description="Dotation en eau par habitant"
        )
        
        return self.analyser_parametre(param, calc_impact_dotation)
    
    def analyser_sensibilite_croissance_demographique(
        self,
        population_base: int,
        taux_base: float = 0.025,
        annees: int = 10,
        variation_pct: float = 30.0,
        pas: float = 5.0
    ) -> SensitivityResult:
        """
        Analyse la sensibilité aux variations de croissance démographique
        
        Args:
            population_base: Population de référence
            taux_base: Taux de croissance de base
            annees: Horizon de projection
            variation_pct: Variation en pourcentage (±%)
            pas: Pas de variation
            
        Returns:
            Résultat de l'analyse de sensibilité
        """
        if population_base <= 0:
            raise ValueError("La population de base doit être strictement positive")
        if annees <= 0:
            raise ValueError("L'horizon de projection doit être strictement positif")
        
        def calc_impact_croissance(valeur):
            pop_base = population_base * (1 + taux_base) ** annees
            pop_variation = population_base * (1 + valeur) ** annees
            return ((pop_variation - pop_base) / pop_base) * 100
        
        param = SensitivityParameter(
            nom="croissance_demographique",
            valeur_base=taux_base,
            variation_pct=variation_pct,
            pas=pas,
            unite="%/an",
            description="Taux de croissance démographique"
        )
        
        return self.analyser_parametre(param, calc_impact_croissance)
    
    def analyser_sensibilite_fuites(
        self,
        demande_nette: float,
        rendement_base: float = 0.95,
        variation_pct: float = 20.0,
        pas: float = 2.0
    ) -> SensitivityResult:
        """
        Analyse la sensibilité aux variations de fuites (rendement réseau)
        
        Args:
            demande_nette: Demande nette en eau (m³/jour)
            rendement_base: Rendement de base du réseau
            variation_pct: Variation en pourcentage (±%)
            pas: Pas de variation
            
        Returns:
            Résultat de l'analyse de sensibilité
        """
        if demande_nette <= 0:
            raise ValueError("La demande nette doit être strictement positive")
        if not 0 < rendement_base <= 1:
            raise ValueError("Le rendement de base doit être entre 0 et 1")
        
        def calc_impact_fuites(valeur):
            production_base = demande_nette / rendement_base
            production_variation = demande_nette / valeur
            return ((production_variation - production_base) / production_base) * 100
        
        param = SensitivityParameter(
            nom="fuites",
            valeur_base=rendement_base,
            variation_pct=variation_pct,
            pas=pas,
            unite="%",
            description="Taux de fuites du réseau"
        )
        
        return self.analyser_parametre(param, calc_impact_fuites)
    
    def analyser_sensibilite_globale(
        self,
        population: int,
        dotation: float = 60.0,
        taux_croissance: float = 0.025,
        rendement: float = 0.95,
        annees: int = 10
    ) -> Dict[str, SensitivityResult]:
        """
        Analyse de sensibilité globale sur tous les paramètres
        
        Args:
            population: Population de référence
            dotation: Dotation en eau (L/j/hab)
            taux_croissance: Taux de croissance démographique
            rendement: Rendement du réseau
            annees: Nombre d'années de projection
            
        Returns:
            Dictionnaire avec résultats pour chaque paramètre
        """
        resultats = {}
        
        # Fonction de calcul d'impact pour la dotation
        def calc_impact_dotation(valeur):
            demande_base = population * dotation * (1 + taux_croissance) ** annees / rendement
            demande_variee = population * valeur * (1 + taux_croissance) ** annees / rendement
            return ((demande_variee - demande_base) / demande_base) * 100
        
        # Fonction de calcul d'impact pour le taux de croissance
        def calc_impact_croissance(valeur):
            demande_base = population * dotation * (1 + taux_croissance) ** annees / rendement
            demande_variee = population * dotation * (1 + valeur) ** annees / rendement
            return ((demande_variee - demande_base) / demande_base) * 100
        
        # Fonction de calcul d'impact pour le rendement
        def calc_impact_rendement(valeur):
            demande_base = population * dotation * (1 + taux_croissance) ** annees / rendement
            demande_variee = population * dotation * (1 + taux_croissance) ** annees / valeur
            return ((demande_variee - demande_base) / demande_base) * 100
        
        # Analyse de sensibilité sur la dotation
        param_dotation = SensitivityParameter(
            nom="dotation",
            valeur_base=dotation,
            variation_pct=20.0,
            pas=2.0,
            unite="L/j/hab",
            description="Dotation en eau par habitant"
        )
        resultats['dotation'] = self.analyser_parametre(param_dotation, calc_impact_dotation)
        
        # Analyse de sensibilité sur le taux de croissance
        param_croissance = SensitivityParameter(
            nom="croissance_demographique",
            valeur_base=taux_croissance,
            variation_pct=30.0,
            pas=0.005,
            unite="%/an",
            description="Taux de croissance démographique"
        )
        resultats['croissance_demographique'] = self.analyser_parametre(param_croissance, calc_impact_croissance)
        
        # Analyse de sensibilité sur les fuites (rendement)
        param_fuites = SensitivityParameter(
            nom="fuites",
            valeur_base=rendement,
            variation_pct=10.0,
            pas=0.01,
            unite="%",
            description="Taux de fuites du réseau"
        )
        resultats['fuites'] = self.analyser_parametre(param_fuites, calc_impact_rendement)
        
        return resultats
    
    def generer_rapport_sensibilite(self, resultats: Dict[str, SensitivityResult], format_sortie: str = "json") -> str:
        """
        Génère un rapport d'analyse de sensibilité dans le format spécifié
        
        Args:
            resultats: Résultats d'analyse de sensibilité
            format_sortie: Format de sortie ("json", "markdown", "html")
            
        Returns:
            Rapport formaté
        """
        if format_sortie == "json":
            return self.generer_rapport_json(resultats)
        elif format_sortie == "markdown":
            return self.generer_rapport_markdown(resultats)
        elif format_sortie == "html":
            return self.generer_rapport_html(resultats)
        else:
            raise ValueError(f"Format de sortie non supporté: {format_sortie}")
    
    def generer_rapport_json(self, resultats: Dict[str, SensitivityResult]) -> str:
        """Génère un rapport JSON des résultats d'analyse de sensibilité"""
        rapport = {
            "analyse_sensibilite": {
                "date_analyse": datetime.now().isoformat(),
                "parametres_analyses": list(resultats.keys()),
                "resultats": {}
            }
        }
        
        for nom_param, resultat in resultats.items():
            rapport["analyse_sensibilite"]["resultats"][nom_param] = {
                "parametre": resultat.parametre,
                "variations": resultat.variations,
                "impacts": resultat.impacts,
                "impact_max": resultat.impact_max,
                "impact_min": resultat.impact_min,
                "impact_moyen": resultat.impact_moyen,
                "classe_impact": resultat.classe_impact,
                "poids_relatif": resultat.poids_relatif
            }
        
        return json.dumps(rapport, indent=2, ensure_ascii=False)
    
    def generer_rapport_markdown(self, resultats: Dict[str, SensitivityResult]) -> str:
        """Génère un rapport Markdown des résultats d'analyse de sensibilité"""
        rapport = f"# 📊 Rapport d'Analyse de Sensibilité AEP\n\n"
        rapport += f"**Date d'analyse:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        rapport += "## 🎯 Résumé des Analyses\n\n"
        rapport += "| Paramètre | Impact Max | Impact Min | Classe |\n"
        rapport += "|-----------|------------|------------|--------|\n"
        
        for nom_param, resultat in resultats.items():
            rapport += f"| {nom_param} | {resultat.impact_max:.2f}% | {resultat.impact_min:.2f}% | {resultat.classe_impact} |\n"
        
        rapport += "\n## Détails par paramètre\n\n"
        
        for nom_param, resultat in resultats.items():
            rapport += f"### {nom_param}\n\n"
            rapport += f"- **Classe d'impact:** {resultat.classe_impact}\n"
            rapport += f"- **Impact maximum:** {resultat.impact_max:.2f}%\n"
            rapport += f"- **Impact minimum:** {resultat.impact_min:.2f}%\n"
            rapport += f"- **Impact moyen:** {resultat.impact_moyen:.2f}%\n"
            rapport += f"- **Poids relatif:** {resultat.poids_relatif:.2f}\n\n"
        
        return rapport
    
    def generer_rapport_html(self, resultats: Dict[str, SensitivityResult]) -> str:
        """Génère un rapport HTML des résultats d'analyse de sensibilité"""
        rapport = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rapport d'Analyse de Sensibilité AEP</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .impact-eleve {{ color: red; }}
                .impact-moyen {{ color: orange; }}
                .impact-faible {{ color: green; }}
            </style>
        </head>
        <body>
            <h1>Rapport d'Analyse de Sensibilité AEP</h1>
            <p><strong>Date d'analyse:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>Résumé</h2>
            <table>
                <tr>
                    <th>Paramètre</th>
                    <th>Impact Max</th>
                    <th>Impact Min</th>
                    <th>Classe</th>
                </tr>
        """
        
        for nom_param, resultat in resultats.items():
            classe_css = f"impact-{resultat.classe_impact}"
            rapport += f"""
                <tr>
                    <td>{nom_param}</td>
                    <td class="{classe_css}">{resultat.impact_max:.2f}%</td>
                    <td class="{classe_css}">{resultat.impact_min:.2f}%</td>
                    <td>{resultat.classe_impact}</td>
                </tr>
            """
        
        rapport += """
            </table>
            
            <h2>Détails par paramètre</h2>
        """
        
        for nom_param, resultat in resultats.items():
            rapport += f"""
            <h3>{nom_param}</h3>
            <ul>
                <li><strong>Classe d'impact:</strong> {resultat.classe_impact}</li>
                <li><strong>Impact maximum:</strong> {resultat.impact_max:.2f}%</li>
                <li><strong>Impact minimum:</strong> {resultat.impact_min:.2f}%</li>
                <li><strong>Impact moyen:</strong> {resultat.impact_moyen:.2f}%</li>
                <li><strong>Poids relatif:</strong> {resultat.poids_relatif:.2f}</li>
            </ul>
            """
        
        rapport += """
        </body>
        </html>
        """
        
        return rapport