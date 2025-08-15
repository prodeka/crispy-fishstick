"""
Phasage et planification pour les projets AEP

Ce module implémente les fonctionnalités de phasage et planification
selon les besoins métier des ingénieurs AEP.
"""

import math
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
from enum import Enum

class TypePlanning(Enum):
    """Types de planning supportés"""
    PHASES = "phases"
    HORIZONS = "horizons"

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
    type_planning: TypePlanning
    phase: str
    annee_debut: int
    annee_fin: int
    population_phase: int
    population_cumulee: int
    besoins_phase: float
    besoins_cumules: float
    infrastructure_requise: float
    cout_estime: float
    unite_besoins: str = "m³/j"
    unite_infrastructure: str = "m³/an"
    unite_cout: str = "€"

@dataclass
class HorizonResult:
    """Résultat d'un calcul d'horizon"""
    type_planning: TypePlanning
    annee: int
    population: int
    besoins: float
    cout_estime: float
    unite_besoins: str = "m³/j"
    unite_cout: str = "€"

class AEPPhasingPlanner:
    """Planificateur de phasage pour les projets AEP"""
    
    def __init__(self, annee_courante: int = 2025, duree_phase_defaut: int = 5):
        """
        Initialise le planificateur
        
        Args:
            annee_courante: Année de référence pour les calculs
            duree_phase_defaut: Durée par défaut d'une phase en années
        """
        self.annee_courante = annee_courante
        self.duree_phase_defaut = duree_phase_defaut
        self.horizons_standard = [2025, 2030, 2035, 2040, 2045, 2050]
        self.phases_standard = {
            "court_terme": Phase(
                nom="Court terme",
                annee_debut=annee_courante,
                annee_fin=annee_courante + duree_phase_defaut,
                pourcentage_population=0.30,
                pourcentage_infrastructure=0.40,
                description="Phase initiale avec infrastructure de base",
                priorite=1
            ),
            "moyen_terme": Phase(
                nom="Moyen terme",
                annee_debut=annee_courante + duree_phase_defaut,
                annee_fin=annee_courante + 2 * duree_phase_defaut,
                pourcentage_population=0.50,
                pourcentage_infrastructure=0.40,
                description="Phase d'extension et d'optimisation",
                priorite=2
            ),
            "long_terme": Phase(
                nom="Long terme",
                annee_debut=annee_courante + 2 * duree_phase_defaut,
                annee_fin=annee_courante + 3 * duree_phase_defaut,
                pourcentage_population=0.20,
                pourcentage_infrastructure=0.20,
                description="Phase finale et maintenance",
                priorite=3
            )
        }
    
    def _valider_phases(self, phases: List[Phase]) -> None:
        """
        Valide la cohérence des phases
        
        Args:
            phases: Liste des phases à valider
            
        Raises:
            ValueError: Si les phases ne sont pas cohérentes
        """
        if not phases:
            raise ValueError("La liste des phases ne peut pas être vide")
        
        # Vérifier que les pourcentages cumulés ≤ 100%
        total_population = sum(phase.pourcentage_population for phase in phases)
        if total_population > 1.0:
            raise ValueError(f"Les pourcentages de population cumulés ({total_population*100:.1f}%) dépassent 100%")
        
        total_infrastructure = sum(phase.pourcentage_infrastructure for phase in phases)
        if total_infrastructure > 1.0:
            raise ValueError(f"Les pourcentages d'infrastructure cumulés ({total_infrastructure*100:.1f}%) dépassent 100%")
        
        # Vérifier que les priorités sont uniques
        priorities = [phase.priorite for phase in phases]
        if len(priorities) != len(set(priorities)):
            raise ValueError("Les priorités des phases doivent être uniques")
        
        # Vérifier que les années sont cohérentes
        for i, phase in enumerate(phases):
            if phase.annee_debut >= phase.annee_fin:
                raise ValueError(f"Phase '{phase.nom}': année de début ({phase.annee_debut}) doit être < année de fin ({phase.annee_fin})")
            
            if i > 0 and phase.annee_debut != phases[i-1].annee_fin:
                raise ValueError(f"Phase '{phase.nom}': année de début ({phase.annee_debut}) doit être égale à l'année de fin de la phase précédente ({phases[i-1].annee_fin})")
    
    def _calculer_phase(
        self,
        phase: Phase,
        population_base: int,
        taux_croissance: float,
        dotation: float,
        cout_infrastructure_m3: float,
        population_cumulee_precedente: int = 0
    ) -> PlanningResult:
        """
        Calcule les résultats pour une phase donnée
        
        Args:
            phase: Phase à calculer
            population_base: Population de référence
            taux_croissance: Taux de croissance démographique
            dotation: Dotation en eau (L/j/hab)
            cout_infrastructure_m3: Coût par m³ d'infrastructure
            population_cumulee_precedente: Population cumulée des phases précédentes
            
        Returns:
            Résultat de calcul pour la phase
        """
        # Calculer la population pour cette phase
        population_fin_phase = population_base * (1 + taux_croissance) ** (phase.annee_fin - self.annee_courante)
        population_phase = int(population_fin_phase * phase.pourcentage_population)
        
        # Calculer la population cumulée
        population_cumulee = population_cumulee_precedente + population_phase
        
        # Calculer les besoins en eau
        besoins_phase = population_phase * dotation / 1000  # m³/jour
        besoins_cumules = population_cumulee * dotation / 1000  # m³/jour
        
        # Calculer l'infrastructure requise
        infrastructure_requise = besoins_phase * 365 * phase.pourcentage_infrastructure  # m³/an
        
        # Calculer le coût estimé
        cout_estime = infrastructure_requise * cout_infrastructure_m3
        
        return PlanningResult(
            type_planning=TypePlanning.PHASES,
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
    
    def calculer_planning_generique(
        self,
        population_base: int,
        taux_croissance: float,
        phases: List[Phase],
        dotation: float = 60.0,
        cout_infrastructure_m3: float = 1000.0
    ) -> Dict[str, PlanningResult]:
        """
        Méthode générique pour calculer un planning avec des phases personnalisées
        
        Args:
            population_base: Population de référence
            taux_croissance: Taux de croissance démographique
            phases: Liste des phases personnalisées
            dotation: Dotation en eau (L/j/hab)
            cout_infrastructure_m3: Coût par m³ d'infrastructure
            
        Returns:
            Dictionnaire avec les résultats par phase
        """
        # Valider les phases
        self._valider_phases(phases)
        
        # Trier les phases par priorité
        phases_triees = sorted(phases, key=lambda x: x.priorite)
        
        resultats = {}
        population_cumulee_precedente = 0
        
        for phase in phases_triees:
            resultat = self._calculer_phase(
                phase, population_base, taux_croissance, dotation, 
                cout_infrastructure_m3, population_cumulee_precedente
            )
            resultats[phase.nom] = resultat
            population_cumulee_precedente = resultat.population_cumulee
        
        return resultats
    
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
        phases = list(self.phases_standard.values())
        return self.calculer_planning_generique(
            population_base, taux_croissance, phases, dotation, cout_infrastructure_m3
        )
    
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
        return self.calculer_planning_generique(
            population_base, taux_croissance, phases, dotation, cout_infrastructure_m3
        )
    
    def calculer_planning_horizons(
        self,
        population_base: int,
        taux_croissance: float,
        horizons: Optional[List[int]] = None,
        dotation: float = 60.0,
        cout_infrastructure_m3: float = 1000.0
    ) -> Dict[int, HorizonResult]:
        """
        Calcule les besoins par horizon temporel
        
        Args:
            population_base: Population de référence
            taux_croissance: Taux de croissance démographique
            horizons: Liste des années d'horizon (utilise les horizons standard si None)
            dotation: Dotation en eau (L/j/hab)
            cout_infrastructure_m3: Coût par m³ d'infrastructure
            
        Returns:
            Dictionnaire avec les résultats par horizon
        """
        if horizons is None:
            horizons = self.horizons_standard
        
        resultats = {}
        
        for annee in horizons:
            # Calculer la population pour cet horizon
            population = int(population_base * (1 + taux_croissance) ** (annee - self.annee_courante))
            
            # Calculer les besoins en eau
            besoins = population * dotation / 1000  # m³/jour
            
            # Calculer le coût estimé (simplifié pour les horizons)
            cout_estime = besoins * 365 * cout_infrastructure_m3
            
            resultats[annee] = HorizonResult(
                type_planning=TypePlanning.HORIZONS,
                annee=annee,
                population=population,
                besoins=round(besoins, 2),
                cout_estime=round(cout_estime, 2)
            )
        
        return resultats
    
    def calculer_planning_phases_pourcentages(
        self,
        population_base: int,
        taux_croissance: float,
        pourcentages_population: List[float],
        pourcentages_infrastructure: List[float],
        noms_phases: Optional[List[str]] = None,
        dotation: float = 60.0,
        cout_infrastructure_m3: float = 1000.0
    ) -> Dict[str, PlanningResult]:
        """
        Calcule un planning basé sur des pourcentages
        
        Args:
            population_base: Population de référence
            taux_croissance: Taux de croissance démographique
            pourcentages_population: Liste des pourcentages de population par phase
            pourcentages_infrastructure: Liste des pourcentages d'infrastructure par phase
            noms_phases: Noms des phases (générés automatiquement si None)
            dotation: Dotation en eau (L/j/hab)
            cout_infrastructure_m3: Coût par m³ d'infrastructure
            
        Returns:
            Dictionnaire avec les résultats par phase
        """
        if len(pourcentages_population) != len(pourcentages_infrastructure):
            raise ValueError("Les listes de pourcentages doivent avoir la même longueur")
        
        if noms_phases is None:
            noms_phases = [f"Phase {i+1}" for i in range(len(pourcentages_population))]
        
        if len(noms_phases) != len(pourcentages_population):
            raise ValueError("Le nombre de noms de phases doit correspondre au nombre de pourcentages")
        
        phases = []
        annee_debut = self.annee_courante
        
        for i, (nom, pct_pop, pct_infra) in enumerate(zip(noms_phases, pourcentages_population, pourcentages_infrastructure)):
            annee_fin = annee_debut + self.duree_phase_defaut
            
            phase = Phase(
                nom=nom,
                annee_debut=annee_debut,
                annee_fin=annee_fin,
                pourcentage_population=pct_pop,
                pourcentage_infrastructure=pct_infra,
                description=f"Phase {i+1} basée sur les pourcentages",
                priorite=i+1
            )
            phases.append(phase)
            annee_debut = annee_fin
        
        return self.calculer_planning_generique(
            population_base, taux_croissance, phases, dotation, cout_infrastructure_m3
        )
    
    def generer_rapport_planning(
        self, 
        resultats: Union[Dict[str, PlanningResult], Dict[int, HorizonResult]], 
        format_sortie: str = "json"
    ) -> str:
        """
        Génère un rapport de planning dans le format spécifié
        
        Args:
            resultats: Résultats de planning (phases ou horizons)
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
    
    def generer_rapport_json(self, resultats: Union[Dict[str, PlanningResult], Dict[int, HorizonResult]]) -> str:
        """Génère un rapport JSON des résultats de planning"""
        rapport = {
            "planning_aep": {
                "date_analyse": datetime.now().isoformat(),
                "type_planning": "phases" if isinstance(next(iter(resultats.values())), PlanningResult) else "horizons",
                "resultats": {}
            }
        }
        
        for cle, resultat in resultats.items():
            if isinstance(resultat, PlanningResult):
                rapport["planning_aep"]["resultats"][cle] = {
                    "phase": resultat.phase,
                    "annee_debut": resultat.annee_debut,
                    "annee_fin": resultat.annee_fin,
                    "population_phase": resultat.population_phase,
                    "population_cumulee": resultat.population_cumulee,
                    "besoins_phase": f"{resultat.besoins_phase} {resultat.unite_besoins}",
                    "besoins_cumules": f"{resultat.besoins_cumules} {resultat.unite_besoins}",
                    "infrastructure_requise": f"{resultat.infrastructure_requise} {resultat.unite_infrastructure}",
                    "cout_estime": f"{resultat.cout_estime:,.0f} {resultat.unite_cout}"
                }
            else:  # HorizonResult
                rapport["planning_aep"]["resultats"][str(cle)] = {
                    "annee": resultat.annee,
                    "population": resultat.population,
                    "besoins": f"{resultat.besoins} {resultat.unite_besoins}",
                    "cout_estime": f"{resultat.cout_estime:,.0f} {resultat.unite_cout}"
                }
        
        return json.dumps(rapport, indent=2, ensure_ascii=False)
    
    def generer_rapport_markdown(self, resultats: Union[Dict[str, PlanningResult], Dict[int, HorizonResult]]) -> str:
        """Génère un rapport Markdown des résultats de planning"""
        is_phases = isinstance(next(iter(resultats.values())), PlanningResult)
        
        rapport = f"# 📅 Rapport de Planning AEP\n\n"
        rapport += f"**Date d'analyse:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        rapport += f"**Type de planning:** {'Phases' if is_phases else 'Horizons'}\n\n"
        
        if is_phases:
            rapport += "## 🎯 Résumé des Phases\n\n"
            rapport += "| Phase | Population | Besoins | Infrastructure | Coût |\n"
            rapport += "|------|------------|---------|----------------|------|\n"
            
            for nom_phase, resultat in resultats.items():
                rapport += f"| {resultat.phase} | {resultat.population_phase:,} hab | {resultat.besoins_phase} {resultat.unite_besoins} | {resultat.infrastructure_requise} {resultat.unite_infrastructure} | {resultat.cout_estime:,.0f} {resultat.unite_cout} |\n"
            
            rapport += "\n## 📊 Détails par Phase\n\n"
            
            for nom_phase, resultat in resultats.items():
                rapport += f"### {resultat.phase}\n\n"
                rapport += f"- **Période:** {resultat.annee_debut} - {resultat.annee_fin}\n"
                rapport += f"- **Population de la phase:** {resultat.population_phase:,} habitants\n"
                rapport += f"- **Population cumulée:** {resultat.population_cumulee:,} habitants\n"
                rapport += f"- **Besoins de la phase:** {resultat.besoins_phase} {resultat.unite_besoins}\n"
                rapport += f"- **Besoins cumulés:** {resultat.besoins_cumules} {resultat.unite_besoins}\n"
                rapport += f"- **Infrastructure requise:** {resultat.infrastructure_requise} {resultat.unite_infrastructure}\n"
                rapport += f"- **Coût estimé:** {resultat.cout_estime:,.0f} {resultat.unite_cout}\n\n"
        else:
            rapport += "## 🎯 Résumé des Horizons\n\n"
            rapport += "| Année | Population | Besoins | Coût |\n"
            rapport += "|-------|------------|---------|------|\n"
            
            for annee, resultat in resultats.items():
                rapport += f"| {resultat.annee} | {resultat.population:,} hab | {resultat.besoins} {resultat.unite_besoins} | {resultat.cout_estime:,.0f} {resultat.unite_cout} |\n"
            
            rapport += "\n## 📊 Détails par Horizon\n\n"
            
            for annee, resultat in resultats.items():
                rapport += f"### {resultat.annee}\n\n"
                rapport += f"- **Population:** {resultat.population:,} habitants\n"
                rapport += f"- **Besoins:** {resultat.besoins} {resultat.unite_besoins}\n"
                rapport += f"- **Coût estimé:** {resultat.cout_estime:,.0f} {resultat.unite_cout}\n\n"
        
        return rapport
    
    def generer_rapport_html(self, resultats: Union[Dict[str, PlanningResult], Dict[int, HorizonResult]]) -> str:
        """Génère un rapport HTML des résultats de planning"""
        is_phases = isinstance(next(iter(resultats.values())), PlanningResult)
        
        rapport = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rapport de Planning AEP</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .cout {{ color: #d32f2f; font-weight: bold; }}
                .population {{ color: #1976d2; }}
                .besoins {{ color: #388e3c; }}
            </style>
        </head>
        <body>
            <h1>📅 Rapport de Planning AEP</h1>
            <p><strong>Date d'analyse:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Type de planning:</strong> {'Phases' if is_phases else 'Horizons'}</p>
        """
        
        if is_phases:
            rapport += """
            <h2>🎯 Résumé des Phases</h2>
            <table>
                <tr>
                    <th>Phase</th>
                    <th>Population</th>
                    <th>Besoins</th>
                    <th>Infrastructure</th>
                    <th>Coût</th>
                </tr>
            """
            
            for nom_phase, resultat in resultats.items():
                rapport += f"""
                <tr>
                    <td>{resultat.phase}</td>
                    <td class="population">{resultat.population_phase:,} hab</td>
                    <td class="besoins">{resultat.besoins_phase} {resultat.unite_besoins}</td>
                    <td>{resultat.infrastructure_requise} {resultat.unite_infrastructure}</td>
                    <td class="cout">{resultat.cout_estime:,.0f} {resultat.unite_cout}</td>
                </tr>
                """
            
            rapport += """
            </table>
            
            <h2>📊 Détails par Phase</h2>
            """
            
            for nom_phase, resultat in resultats.items():
                rapport += f"""
                <h3>{resultat.phase}</h3>
                <ul>
                    <li><strong>Période:</strong> {resultat.annee_debut} - {resultat.annee_fin}</li>
                    <li><strong>Population de la phase:</strong> {resultat.population_phase:,} habitants</li>
                    <li><strong>Population cumulée:</strong> {resultat.population_cumulee:,} habitants</li>
                    <li><strong>Besoins de la phase:</strong> {resultat.besoins_phase} {resultat.unite_besoins}</li>
                    <li><strong>Besoins cumulés:</strong> {resultat.besoins_cumules} {resultat.unite_besoins}</li>
                    <li><strong>Infrastructure requise:</strong> {resultat.infrastructure_requise} {resultat.unite_infrastructure}</li>
                    <li><strong>Coût estimé:</strong> {resultat.cout_estime:,.0f} {resultat.unite_cout}</li>
                </ul>
                """
        else:
            rapport += """
            <h2>🎯 Résumé des Horizons</h2>
            <table>
                <tr>
                    <th>Année</th>
                    <th>Population</th>
                    <th>Besoins</th>
                    <th>Coût</th>
                </tr>
            """
            
            for annee, resultat in resultats.items():
                rapport += f"""
                <tr>
                    <td>{resultat.annee}</td>
                    <td class="population">{resultat.population:,} hab</td>
                    <td class="besoins">{resultat.besoins} {resultat.unite_besoins}</td>
                    <td class="cout">{resultat.cout_estime:,.0f} {resultat.unite_cout}</td>
                </tr>
                """
            
            rapport += """
            </table>
            
            <h2>📊 Détails par Horizon</h2>
            """
            
            for annee, resultat in resultats.items():
                rapport += f"""
                <h3>{resultat.annee}</h3>
                <ul>
                    <li><strong>Population:</strong> {resultat.population:,} habitants</li>
                    <li><strong>Besoins:</strong> {resultat.besoins} {resultat.unite_besoins}</li>
                    <li><strong>Coût estimé:</strong> {resultat.cout_estime:,.0f} {resultat.unite_cout}</li>
                </ul>
                """
        
        rapport += """
        </body>
        </html>
        """
        
        return rapport
