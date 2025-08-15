"""
Phasage et planification pour les projets AEP

Ce module implémente les fonctionnalités de phasage et planification
selon les besoins métier des ingénieurs AEP.
"""

import math
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

@dataclass
class Phase:
    """Définition d'une phase de projet"""
    nom: str
    annee_debut: int
    annee_fin: int
    pourcentage_population: float
    pourcentage_infrastructure: float
    description: str
    priorite: int

@dataclass
class PlanningResult:
    """Résultat d'un calcul de planning"""
    phase: str
    annee_debut: int
    annee_fin: int
    population_phase: int
    population_cumulee: int
    besoins_phase: float
    besoins_cumules: float
    infrastructure_requise: float
    cout_estime: float

class AEPPhasingPlanner:
    """Planificateur de phasage pour les projets AEP"""
    
    def __init__(self):
        self.horizons_standard = [2025, 2030, 2035, 2040, 2045, 2050]
        self.phases_standard = {
            "court_terme": Phase(
                nom="Court terme",
                annee_debut=2025,
                annee_fin=2030,
                pourcentage_population=0.30,
                pourcentage_infrastructure=0.40,
                description="Phase initiale avec infrastructure de base",
                priorite=1
            ),
            "moyen_terme": Phase(
                nom="Moyen terme",
                annee_debut=2030,
                annee_fin=2040,
                pourcentage_population=0.50,
                pourcentage_infrastructure=0.40,
                description="Phase d'extension et d'optimisation",
                priorite=2
            ),
            "long_terme": Phase(
                nom="Long terme",
                annee_debut=2040,
                annee_fin=2050,
                pourcentage_population=0.20,
                pourcentage_infrastructure=0.20,
                description="Phase finale et maintenance",
                priorite=3
            )
        }
    
    def calculer_planning_standard(
        self,
        population_base: int,
        taux_croissance: float,
        dotation: float = 60.0,
        cout_infrastructure_m3: float = 1000.0
    ) -> Dict[str, PlanningResult]:
        """
        Calcule un planning standard avec 3 phases
        
        Args:
            population_base: Population de référence
            taux_croissance: Taux de croissance démographique
            dotation: Dotation en eau (L/j/hab)
            cout_infrastructure_m3: Coût par m³ d'infrastructure
            
        Returns:
            Dictionnaire avec les résultats par phase
        """
        resultats = {}
        
        for nom_phase, phase in self.phases_standard.items():
            # Calculer la population pour cette phase
            population_fin_phase = population_base * (1 + taux_croissance) ** (phase.annee_fin - 2025)
            population_phase = int(population_fin_phase * phase.pourcentage_population)
            
            # Calculer la population cumulée
            population_cumulee = int(population_fin_phase * (phase.pourcentage_population + 
                                                           sum(p.pourcentage_population for p in self.phases_standard.values() 
                                                               if p.priorite < phase.priorite)))
            
            # Calculer les besoins en eau
            besoins_phase = population_phase * dotation / 1000  # m³/jour
            besoins_cumules = population_cumulee * dotation / 1000  # m³/jour
            
            # Calculer l'infrastructure requise
            infrastructure_requise = besoins_phase * 365 * phase.pourcentage_infrastructure  # m³/an
            
            # Calculer le coût estimé
            cout_estime = infrastructure_requise * cout_infrastructure_m3
            
            resultats[nom_phase] = PlanningResult(
                phase=phase.nom,
                annee_debut=phase.annee_debut,
                annee_fin=phase.annee_fin,
                population_phase=population_phase,
                population_cumulee=population_cumulee,
                besoins_phase=round(besoins_phase, 2),
                besoins_cumules=round(besoins_cumules, 2),
                infrastructure_requise=round(infrastructure_requise, 2),
                cout_estime=round(cout_estime, 2)
            )
        
        return resultats
    
    def calculer_planning_personnalise(
        self,
        population_base: int,
        taux_croissance: float,
        phases: List[Phase],
        dotation: float = 60.0,
        cout_infrastructure_m3: float = 1000.0
    ) -> Dict[str, PlanningResult]:
        """
        Calcule un planning personnalisé avec des phases définies
        
        Args:
            population_base: Population de référence
            taux_croissance: Taux de croissance démographique
            phases: Liste des phases personnalisées
            dotation: Dotation en eau (L/j/hab)
            cout_infrastructure_m3: Coût par m³ d'infrastructure
            
        Returns:
            Dictionnaire avec les résultats par phase
        """
        resultats = {}
        
        # Trier les phases par priorité
        phases_triees = sorted(phases, key=lambda x: x.priorite)
        
        population_cumulee_precedente = 0
        
        for phase in phases_triees:
            # Calculer la population pour cette phase
            population_fin_phase = population_base * (1 + taux_croissance) ** (phase.annee_fin - 2025)
            population_phase = int(population_fin_phase * phase.pourcentage_population)
            
            # Calculer la population cumulée
            population_cumulee = population_cumulee_precedente + population_phase
            population_cumulee_precedente = population_cumulee
            
            # Calculer les besoins en eau
            besoins_phase = population_phase * dotation / 1000  # m³/jour
            besoins_cumules = population_cumulee * dotation / 1000  # m³/jour
            
            # Calculer l'infrastructure requise
            infrastructure_requise = besoins_phase * 365 * phase.pourcentage_infrastructure  # m³/an
            
            # Calculer le coût estimé
            cout_estime = infrastructure_requise * cout_infrastructure_m3
            
            resultats[phase.nom] = PlanningResult(
                phase=phase.nom,
                annee_debut=phase.annee_debut,
                annee_fin=phase.annee_fin,
                population_phase=population_phase,
                population_cumulee=population_cumulee,
                besoins_phase=round(besoins_phase, 2),
                besoins_cumules=round(besoins_cumules, 2),
                infrastructure_requise=round(infrastructure_requise, 2),
                cout_estime=round(cout_estime, 2)
            )
        
        return resultats
    
    def calculer_planning_horizons(
        self,
        population_base: int,
        taux_croissance: float,
        horizons: List[int],
        dotation: float = 60.0
    ) -> Dict[int, Dict[str, Any]]:
        """
        Calcule les besoins par horizon temporel
        
        Args:
            population_base: Population de référence
            taux_croissance: Taux de croissance démographique
            horizons: Liste des années d'horizon
            dotation: Dotation en eau (L/j/hab)
            
        Returns:
            Dictionnaire avec les résultats par horizon
        """
        resultats = {}
        
        for horizon in horizons:
            # Calculer la population à cet horizon
            annees = horizon - 2025
            population_horizon = population_base * (1 + taux_croissance) ** annees
            
            # Calculer les besoins en eau
            besoins_journaliers = population_horizon * dotation / 1000  # m³/jour
            besoins_annuels = besoins_journaliers * 365  # m³/an
            
            # Calculer les besoins cumulés depuis le début
            besoins_cumules = 0
            for annee in range(2025, horizon + 1):
                pop_annee = population_base * (1 + taux_croissance) ** (annee - 2025)
                besoins_cumules += pop_annee * dotation / 1000 * 365
            
            resultats[horizon] = {
                "annee": horizon,
                "population": int(population_horizon),
                "besoins_journaliers_m3_j": round(besoins_journaliers, 2),
                "besoins_annuels_m3_an": round(besoins_annuels, 2),
                "besoins_cumules_m3": round(besoins_cumules, 2),
                "croissance_depuis_2025": round(((population_horizon - population_base) / population_base) * 100, 2)
            }
        
        return resultats
    
    def calculer_planning_phases_pourcentages(
        self,
        population_base: int,
        taux_croissance: float,
        phases_pourcentages: List[Tuple[str, float, float]],
        dotation: float = 60.0,
        cout_infrastructure_m3: float = 1000.0
    ) -> Dict[str, PlanningResult]:
        """
        Calcule un planning avec des phases définies par pourcentages
        
        Args:
            population_base: Population de référence
            taux_croissance: Taux de croissance démographique
            phases_pourcentages: Liste de tuples (nom, %population, %infrastructure)
            dotation: Dotation en eau (L/j/hab)
            cout_infrastructure_m3: Coût par m³ d'infrastructure
            
        Returns:
            Dictionnaire avec les résultats par phase
        """
        resultats = {}
        
        population_cumulee_precedente = 0
        annee_courante = 2025
        
        for i, (nom_phase, pct_pop, pct_infra) in enumerate(phases_pourcentages):
            # Définir la durée de la phase (5 ans par défaut)
            duree_phase = 5
            annee_debut = annee_courante
            annee_fin = annee_courante + duree_phase
            
            # Calculer la population pour cette phase
            population_fin_phase = population_base * (1 + taux_croissance) ** (annee_fin - 2025)
            population_phase = int(population_fin_phase * pct_pop)
            
            # Calculer la population cumulée
            population_cumulee = population_cumulee_precedente + population_phase
            population_cumulee_precedente = population_cumulee
            
            # Calculer les besoins en eau
            besoins_phase = population_phase * dotation / 1000  # m³/jour
            besoins_cumules = population_cumulee * dotation / 1000  # m³/jour
            
            # Calculer l'infrastructure requise
            infrastructure_requise = besoins_phase * 365 * pct_infra  # m³/an
            
            # Calculer le coût estimé
            cout_estime = infrastructure_requise * cout_infrastructure_m3
            
            resultats[nom_phase] = PlanningResult(
                phase=nom_phase,
                annee_debut=annee_debut,
                annee_fin=annee_fin,
                population_phase=population_phase,
                population_cumulee=population_cumulee,
                besoins_phase=round(besoins_phase, 2),
                besoins_cumules=round(besoins_cumules, 2),
                infrastructure_requise=round(infrastructure_requise, 2),
                cout_estime=round(cout_estime, 2)
            )
            
            annee_courante = annee_fin
        
        return resultats
    
    def generer_rapport_planning(
        self,
        resultats: Dict[str, Any],
        format_sortie: str = "json"
    ) -> str:
        """
        Génère un rapport de planning
        
        Args:
            resultats: Résultats du planning
            format_sortie: Format de sortie (json, markdown, html)
            
        Returns:
            Rapport formaté
        """
        if format_sortie == "json":
            return self._generer_rapport_json(resultats)
        elif format_sortie == "markdown":
            return self._generer_rapport_markdown(resultats)
        elif format_sortie == "html":
            return self._generer_rapport_html(resultats)
        else:
            raise ValueError(f"Format de sortie non supporté: {format_sortie}")
    
    def _generer_rapport_json(self, resultats: Dict[str, Any]) -> str:
        """Génère un rapport JSON"""
        # Convertir les objets PlanningResult en dictionnaires
        resultats_serialisables = {}
        for nom, resultat in resultats.items():
            if hasattr(resultat, '__dict__'):
                resultats_serialisables[nom] = resultat.__dict__
            else:
                resultats_serialisables[nom] = resultat
        
        return json.dumps(resultats_serialisables, indent=2, ensure_ascii=False)
    
    def _generer_rapport_markdown(self, resultats: Dict[str, Any]) -> str:
        """Génère un rapport Markdown"""
        rapport = "# 📅 Rapport de Planning AEP\n\n"
        
        # Détecter le type de planning en vérifiant la structure des résultats
        if any(hasattr(resultat, 'phase') for resultat in resultats.values()):
            # Planning par phases
            rapport += "## 🎯 Planning par Phases\n\n"
            rapport += "| Phase | Années | Population | Besoins (m³/j) | Infrastructure | Coût (€) |\n"
            rapport += "|-------|--------|------------|----------------|----------------|----------|\n"
            
            for nom_phase, resultat in resultats.items():
                rapport += f"| {resultat.phase} | {resultat.annee_debut}-{resultat.annee_fin} | "
                rapport += f"{resultat.population_phase:,} | {resultat.besoins_phase} | "
                rapport += f"{resultat.infrastructure_requise} | {resultat.cout_estime:,} |\n"
        else:
            # Planning par horizons
            rapport += "## 🎯 Planning par Horizons\n\n"
            rapport += "| Année | Population | Besoins (m³/j) | Besoins (m³/an) | Besoins Cumulés | Croissance |\n"
            rapport += "|-------|------------|----------------|-----------------|-----------------|------------|\n"
            
            for horizon, resultat in resultats.items():
                rapport += f"| {resultat['annee']} | {resultat['population']:,} | "
                rapport += f"{resultat['besoins_journaliers_m3_j']} | {resultat['besoins_annuels_m3_an']} | "
                rapport += f"{resultat['besoins_cumules_m3']} | {resultat['croissance_depuis_2025']}% |\n"
        
        return rapport
    
    def _generer_rapport_html(self, resultats: Dict[str, Any]) -> str:
        """Génère un rapport HTML basique"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rapport de Planning AEP</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .header { background-color: #0066cc; color: white; padding: 20px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📅 Rapport de Planning AEP</h1>
            </div>
        """
        
        # Détecter le type de planning en vérifiant la structure des résultats
        if any(hasattr(resultat, 'phase') for resultat in resultats.values()):
            # Planning par phases
            html += "<h2>🎯 Planning par Phases</h2>"
            html += "<table><tr><th>Phase</th><th>Années</th><th>Population</th><th>Besoins (m³/j)</th><th>Infrastructure</th><th>Coût (€)</th></tr>"
            
            for nom_phase, resultat in resultats.items():
                html += f"<tr><td>{resultat.phase}</td><td>{resultat.annee_debut}-{resultat.annee_fin}</td>"
                html += f"<td>{resultat.population_phase:,}</td><td>{resultat.besoins_phase}</td>"
                html += f"<td>{resultat.infrastructure_requise}</td><td>{resultat.cout_estime:,}</td></tr>"
            
            html += "</table>"
        else:
            # Planning par horizons
            html += "<h2>🎯 Planning par Horizons</h2>"
            html += "<table><tr><th>Année</th><th>Population</th><th>Besoins (m³/j)</th><th>Besoins (m³/an)</th><th>Besoins Cumulés</th><th>Croissance</th></tr>"
            
            for horizon, resultat in resultats.items():
                html += f"<tr><td>{resultat['annee']}</td><td>{resultat['population']:,}</td>"
                html += f"<td>{resultat['besoins_journaliers_m3_j']}</td><td>{resultat['besoins_annuels_m3_an']}</td>"
                html += f"<td>{resultat['besoins_cumules_m3']}</td><td>{resultat['croissance_depuis_2025']}%</td></tr>"
            
            html += "</table>"
        
        html += "</body></html>"
        return html
