"""
Analyseur de scénarios multiples pour AEP.
Exécute plusieurs scénarios et génère des comparaisons.
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import yaml

from ..core.models import (
    ScenarioAnalysis, ScenarioResult, ScenarioComparison,
    PopulationData, DemandeData, NetworkData, ReservoirData, PumpingData
)
from ..core.solvers import SolverFactory
from ..optimization import GeneticOptimizer, ConstraintManager
from ..optimization.models import ConfigurationOptimisation


class ScenarioAnalyzer:
    """
    Analyseur de scénarios multiples pour projets AEP.
    """
    
    def __init__(self, solver_name: str, project_path: Path, output_dir: Path, verbose: bool = False):
        self.solver_name = solver_name
        self.project_path = project_path
        self.output_dir = output_dir
        self.verbose = verbose
        self.solver_factory = SolverFactory()
        
    def analyze_scenarios(self, config: Dict[str, Any]) -> ScenarioComparison:
        """
        Analyse tous les scénarios définis dans la configuration.
        
        Args:
            config: Configuration complète du projet avec scénarios
            
        Returns:
            Résultats comparatifs de tous les scénarios
        """
        if self.verbose:
            print(f"🔍 Analyse de {len(config.get('scenarios', {}).get('scenarios', []))} scénarios...")
        
        # Extraire la configuration des scénarios
        scenario_config = config.get('scenarios', {})
        if not scenario_config or 'scenarios' not in scenario_config:
            raise ValueError("Configuration des scénarios manquante ou invalide")
        
        # Valider la configuration
        scenario_analysis = ScenarioAnalysis(**scenario_config)
        
        # Exécuter chaque scénario
        results = []
        for scenario in scenario_analysis.scenarios:
            if self.verbose:
                print(f"  📊 Exécution du scénario: {scenario.nom}")
            
            try:
                result = self._execute_scenario(config, scenario)
                results.append(result)
            except Exception as e:
                if self.verbose:
                    print(f"    ❌ Erreur: {e}")
                
                # Créer un résultat d'erreur
                error_result = ScenarioResult(
                    nom_scenario=scenario.nom,
                    description=scenario.description,
                    parametres_appliques=scenario.parametres,
                    resultats={},
                    metriques={},
                    statut="erreur",
                    temps_calcul=0.0,
                    erreurs=[str(e)]
                )
                results.append(error_result)
        
        # Générer la comparaison
        comparison = self._generate_comparison(results, scenario_analysis)
        
        # Générer les recommandations
        comparison.recommandations = self._generate_recommendations(results)
        
        return comparison
    
    def _execute_scenario(self, base_config: Dict[str, Any], scenario: Any) -> ScenarioResult:
        """
        Exécute un scénario individuel.
        
        Args:
            base_config: Configuration de base du projet
            scenario: Configuration du scénario
            
        Returns:
            Résultat du scénario
        """
        start_time = time.time()
        
        # Fusionner la configuration de base avec les paramètres du scénario
        merged_config = self._merge_configurations(base_config, scenario.parametres)
        
        # Exécuter les calculs selon le type de projet
        results = self._execute_project_calculations(merged_config)
        
        # Calculer les métriques
        metrics = self._calculate_metrics(results)
        
        execution_time = time.time() - start_time
        
        return ScenarioResult(
            nom_scenario=scenario.nom,
            description=scenario.description,
            parametres_appliques=scenario.parametres,
            resultats=results,
            metriques=metrics,
            statut="succes",
            temps_calcul=execution_time,
            erreurs=[]
        )
    
    def _merge_configurations(self, base_config: Dict[str, Any], scenario_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fusionne la configuration de base avec les paramètres du scénario.
        
        Args:
            base_config: Configuration de base
            scenario_params: Paramètres du scénario
            
        Returns:
            Configuration fusionnée
        """
        merged = base_config.copy()
        
        # Appliquer les overrides du scénario
        for key, value in scenario_params.items():
            if key in merged:
                if isinstance(merged[key], dict) and isinstance(value, dict):
                    merged[key].update(value)
                else:
                    merged[key] = value
            else:
                merged[key] = value
        
        return merged
    
    def _execute_project_calculations(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute les calculs du projet selon la configuration.
        
        Args:
            config: Configuration du projet
            
        Returns:
            Résultats des calculs
        """
        results = {}
        
        # 1. Calculs démographiques
        if 'population' in config:
            pop_data = PopulationData(**config['population'])
            results['population'] = self._calculate_population(pop_data)
        
        # 2. Calculs de demande
        if 'demande' in config:
            demand_data = DemandeData(**config['demande'])
            results['demande'] = self._calculate_demand(demand_data)
        
        # 3. Dimensionnement réseau
        if 'reseau' in config:
            network_data = NetworkData(**config['reseau'])
            results['reseau'] = self._calculate_network(network_data)
        
        # 4. Dimensionnement réservoir
        if 'reservoir' in config:
            reservoir_data = ReservoirData(**config['reservoir'])
            results['reservoir'] = self._calculate_reservoir(reservoir_data)
        
        # 5. Dimensionnement pompage
        if 'pompage' in config:
            pumping_data = PumpingData(**config['pompage'])
            results['pompage'] = self._calculate_pumping(pumping_data)
        
        # 6. Optimisation si demandée
        if 'optimisation' in config:
            results['optimisation'] = self._execute_optimization(config)
        
        return results
    
    def _calculate_population(self, data: PopulationData) -> Dict[str, Any]:
        """Calcule la projection démographique."""
        from ..calculations.population_unified import calculate_population_projection_unified
        
        result = calculate_population_projection_unified({
            "population_base": data.population_base,
            "taux_croissance": data.taux_croissance,
            "annees": data.annees_projection,
            "methode": data.methode.value,
            "verbose": False
        })
        
        return {
            'population_initiale': data.population_base,
            'population_finale': result['population_finale'],
            'taux_croissance': data.taux_croissance,
            'methode': data.methode.value,
            'projections': result.get('projections_annuelles', [])
        }
    
    def _calculate_demand(self, data: DemandeData) -> Dict[str, Any]:
        """Calcule la demande en eau."""
        from ..calculations.demand_unified import calculate_water_demand_unified
        
        result = calculate_water_demand_unified({
            "population": data.population,
            "dotation_l_j_hab": data.dotation_l_hab_j,
            "coefficient_pointe": data.coefficient_pointe,
            "type_consommation": data.type_consommation.value,
            "verbose": False
        })
        
        return {
            'population': data.population,
            'demande_moyenne_m3j': result.get('besoin_brut_m3j', 0),
            'demande_pointe_m3j': result.get('besoin_brut_m3j', 0) * data.coefficient_pointe,
            'demande_pointe_m3s': result.get('debit_pointe_m3s', 0),
            'dotation': data.dotation_l_hab_j,
            'coefficient_pointe': data.coefficient_pointe
        }
    
    def _calculate_network(self, data: NetworkData) -> Dict[str, Any]:
        """Calcule le dimensionnement du réseau."""
        from ..calculations.network_unified import dimension_network_unified
        
        result = dimension_network_unified({
            "debit_m3s": data.debit_m3s,
            "longueur_m": data.longueur_m,
            "materiau": data.materiau,
            "perte_charge_max_m": data.perte_charge_max_m,
            "methode": data.methode.value
        }, verbose=False)
        
        if result.get('statut') == 'SUCCES':
            reseau_data = result.get('reseau', {})
            return {
                'diametre_m': reseau_data.get('diametre_optimal_mm', 0) / 1000,  # Conversion mm → m
                'vitesse_ms': reseau_data.get('vitesse_ms', 0),
                'perte_charge_m': reseau_data.get('perte_charge_m', 0),
                'materiau': data.materiau,
                'methode': data.methode.value
            }
        else:
            return {'erreur': result.get('message', 'Erreur inconnue')}
    
    def _calculate_reservoir(self, data: ReservoirData) -> Dict[str, Any]:
        """Calcule le dimensionnement du réservoir."""
        from ..calculations.reservoir_unified import dimension_reservoir_unified
        
        result = dimension_reservoir_unified({
            "volume_journalier_m3": data.volume_journalier_m3,
            "mode_adduction": data.type_adduction.value,
            "forme_reservoir": data.forme_reservoir.value,
            "type_zone": data.type_zone
        }, verbose=False)
        
        if result.get('statut') == 'SUCCES':
            reservoir_data = result.get('reservoir', {})
            return {
                'volume_utile_m3': reservoir_data.get('volume_utile_m3', 0),
                'volume_total_m3': reservoir_data.get('volume_total_m3', 0),
                'hauteur_m': reservoir_data.get('hauteur_m', 0),
                'diametre_m': reservoir_data.get('diametre_m', 0),
                'surface_m2': reservoir_data.get('surface_m2', 0)
            }
        else:
            return {'erreur': result.get('message', 'Erreur inconnue')}
    
    def _calculate_pumping(self, data: PumpingData) -> Dict[str, Any]:
        """Calcule le dimensionnement du pompage."""
        from ..calculations.pumping_unified import dimension_pumping_unified
        
        result = dimension_pumping_unified({
            'debit_m3h': data.debit_m3h,
            'hmt_m': data.hmt_m,
            'type_pompe': data.type_pompe,
            'rendement_pompe': data.rendement_pompe
        }, verbose=False)
        
        if result['statut'] == 'SUCCES':
            pompage = result['pompage']
            return {
                'puissance_hydraulique_kw': pompage['puissance_hydraulique_kw'],
                'puissance_electrique_kw': pompage['puissance_electrique_kw'],
                'puissance_groupe_kva': pompage['puissance_groupe_kva'],
                'energie_journaliere_kwh': pompage['energie_kwh'],
                'cout_journalier_fcfa': pompage['cout_euros']  # Note: conversion nécessaire
            }
        else:
            return {'erreur': result.get('message', 'Erreur inconnue')}
    
    def _execute_optimization(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute l'optimisation si configurée."""
        if 'optimisation' not in config:
            return {}
        
        try:
            # Créer le solveur
            solver = self.solver_factory.select_solver(self.solver_name)
            
            # Créer le gestionnaire de contraintes
            constraint_manager = ConstraintManager()
            
            # Créer l'optimiseur
            optimizer = GeneticOptimizer(
                ConfigurationOptimisation(**config['optimisation']),
                constraint_manager
            )
            
            # Exécuter l'optimisation
            reseau_data = config.get('reseau_complet', {})
            nb_conduites = len(reseau_data.get('conduites', []))
            
            if nb_conduites == 0:
                return {'erreur': 'Aucune conduite définie pour l\'optimisation'}
            
            result = optimizer.optimiser(reseau_data, nb_conduites)
            return result
            
        except Exception as e:
            return {'erreur': str(e)}
    
    def _calculate_metrics(self, results: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcule les métriques de performance du scénario.
        
        Args:
            results: Résultats des calculs
            
        Returns:
            Métriques calculées
        """
        metrics = {}
        
        # Coût total
        cout_total = 0.0
        if 'reseau' in results:
            # Estimation du coût réseau (simplifiée)
            cout_total += 100000  # Coût de base
        
        if 'reservoir' in results:
            # Estimation du coût réservoir
            volume = results['reservoir'].get('volume_total_m3', 0)
            cout_total += volume * 50  # 50 FCFA/m³
        
        if 'pompage' in results:
            # Coût énergétique annuel
            energie_annuelle = results['pompage'].get('energie_journaliere_kwh', 0) * 365
            cout_total += energie_annuelle * 15  # 15 FCFA/kWh
        
        metrics['cout_total'] = cout_total
        
        # Performance hydraulique
        performance = 0.8  # Valeur par défaut
        if 'reseau' in results:
            vitesse = results['reseau'].get('vitesse_ms', 0)
            if 0.5 <= vitesse <= 2.5:
                performance = 1.0
            elif 0.3 <= vitesse <= 3.0:
                performance = 0.7
            else:
                performance = 0.4
        
        metrics['performance_hydraulique'] = performance
        
        # Énergie consommée
        energie = 0.0
        if 'pompage' in results:
            energie = results['pompage'].get('energie_journaliere_kwh', 0) * 365
        
        metrics['energie_consommee'] = energie
        
        return metrics
    
    def _generate_comparison(self, results: List[ScenarioResult], config: ScenarioAnalysis) -> ScenarioComparison:
        """
        Génère la comparaison entre tous les scénarios.
        
        Args:
            results: Résultats de tous les scénarios
            config: Configuration de l'analyse
            
        Returns:
            Comparaison des scénarios
        """
        # Préparer le tableau comparatif
        tableau = {
            'scenarios': [],
            'cout_total': [],
            'performance_hydraulique': [],
            'energie_consommee': [],
            'temps_calcul': []
        }
        
        for result in results:
            if result.statut == "succes":
                tableau['scenarios'].append(result.nom_scenario)
                tableau['cout_total'].append(result.metriques.get('cout_total', 0))
                tableau['performance_hydraulique'].append(result.metriques.get('performance_hydraulique', 0))
                tableau['energie_consommee'].append(result.metriques.get('energie_consommee', 0))
                tableau['temps_calcul'].append(result.temps_calcul)
        
        return ScenarioComparison(
            nom_analyse=f"Analyse_scenarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            date_analyse=datetime.now(),
            scenarios_analyses=results,
            tableau_comparatif=tableau,
            graphiques={},
            recommandations=[]
        )
    
    def _generate_recommendations(self, results: List[ScenarioResult]) -> List[str]:
        """
        Génère des recommandations basées sur l'analyse des scénarios.
        
        Args:
            results: Résultats de tous les scénarios
            
        Returns:
            Liste des recommandations
        """
        recommendations = []
        
        # Filtrer les scénarios réussis
        successful_scenarios = [r for r in results if r.statut == "succes"]
        
        if not successful_scenarios:
            recommendations.append("Aucun scénario n'a pu être exécuté avec succès. Vérifiez la configuration.")
            return recommendations
        
        # Analyser les coûts
        couts = [s.metriques.get('cout_total', 0) for s in successful_scenarios]
        if couts:
            cout_min = min(couts)
            cout_max = max(couts)
            cout_moyen = sum(couts) / len(couts)
            
            scenarios_min = [s.nom_scenario for s in successful_scenarios if s.metriques.get('cout_total', 0) == cout_min]
            scenarios_max = [s.nom_scenario for s in successful_scenarios if s.metriques.get('cout_total', 0) == cout_max]
            
            recommendations.append(f"Le scénario le plus économique est '{scenarios_min[0]}' avec un coût de {cout_min:,.0f} FCFA")
            recommendations.append(f"Le scénario le plus coûteux est '{scenarios_max[0]}' avec un coût de {cout_max:,.0f} FCFA")
            recommendations.append(f"Coût moyen des scénarios: {cout_moyen:,.0f} FCFA")
        
        # Analyser les performances
        performances = [s.metriques.get('performance_hydraulique', 0) for s in successful_scenarios]
        if performances:
            perf_max = max(performances)
            scenarios_perf = [s.nom_scenario for s in successful_scenarios if s.metriques.get('performance_hydraulique', 0) == perf_max]
            
            recommendations.append(f"Le scénario avec la meilleure performance hydraulique est '{scenarios_perf[0]}' (score: {perf_max:.2f})")
        
        # Recommandations générales
        if len(successful_scenarios) > 1:
            recommendations.append("Considérer une approche hybride combinant les meilleurs aspects de plusieurs scénarios")
        
        return recommendations
    
    def generate_comparison_table(self, comparison: ScenarioComparison, output_dir: Path):
        """Génère un tableau comparatif HTML."""
        # Créer le répertoire pour les tableaux
        tables_dir = output_dir / "tables"
        tables_dir.mkdir(exist_ok=True)
        
        # Générer le HTML
        html_content = self._generate_html_table(comparison)
        
        # Sauvegarder
        output_file = output_dir / "comparaison_scenarios.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def generate_comparison_charts(self, comparison: ScenarioComparison, output_dir: Path):
        """Génère des graphiques de comparaison."""
        # Créer le répertoire pour les graphiques
        graphs_dir = output_dir / "graphs"
        graphs_dir.mkdir(exist_ok=True)
        
        # Générer les graphiques (pour l'instant, on crée des fichiers de données)
        # TODO: Implémenter la génération de vrais graphiques avec matplotlib ou plotly
        
        # Sauvegarder les données pour les graphiques
        data_file = graphs_dir / "donnees_graphiques.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(comparison.tableau_comparatif, f, indent=2, ensure_ascii=False)
        
        # Créer un fichier de métadonnées pour les graphiques
        metadata = {
            "scenarios_count": len(comparison.scenarios_analyses),
            "criteres": list(comparison.tableau_comparatif.keys()),
            "date_generation": datetime.now().isoformat()
        }
        
        metadata_file = graphs_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)
    
    def _generate_html_table(self, comparison: ScenarioComparison) -> str:
        """Génère le contenu HTML du tableau comparatif."""
        html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparaison des Scénarios - {comparison.nom_analyse}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .table-container {{ overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .metric {{ font-weight: bold; color: #2196F3; }}
        .recommendations {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin-top: 20px; }}
        .recommendations h3 {{ color: #2e7d32; margin-top: 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Comparaison des Scénarios AEP</h1>
        <p><strong>Analyse:</strong> {comparison.nom_analyse}</p>
        <p><strong>Date:</strong> {comparison.date_analyse.strftime('%d/%m/%Y à %H:%M')}</p>
        <p><strong>Scénarios analysés:</strong> {len(comparison.scenarios_analyses)}</p>
    </div>
    
    <div class="table-container">
        <h2>📋 Tableau Comparatif</h2>
        <table>
            <thead>
                <tr>
                    <th>Scénario</th>
                    <th>Coût Total (FCFA)</th>
                    <th>Performance Hydraulique</th>
                    <th>Énergie Consommée (kWh/an)</th>
                    <th>Temps Calcul (s)</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Ajouter les lignes du tableau
        for i, scenario in enumerate(comparison.scenarios_analyses):
            if scenario.statut == "succes":
                html += f"""
                <tr>
                    <td><strong>{scenario.nom_scenario}</strong></td>
                    <td class="metric">{scenario.metriques.get('cout_total', 0):,.0f}</td>
                    <td class="metric">{scenario.metriques.get('performance_hydraulique', 0):.2f}</td>
                    <td class="metric">{scenario.metriques.get('energie_consommee', 0):,.0f}</td>
                    <td>{scenario.temps_calcul:.2f}</td>
                </tr>
"""
            else:
                html += f"""
                <tr style="background-color: #ffebee;">
                    <td><strong>{scenario.nom_scenario}</strong></td>
                    <td colspan="4" style="color: #c62828;">❌ Erreur: {', '.join(scenario.erreurs)}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
    </div>
    
    <div class="recommendations">
        <h3>💡 Recommandations</h3>
        <ul>
"""
        
        # Ajouter les recommandations
        for rec in comparison.recommandations:
            html += f"            <li>{rec}</li>\n"
        
        html += """
        </ul>
    </div>
    
    <div style="margin-top: 30px; text-align: center; color: #666;">
        <p>Généré automatiquement par LCPI-CLI v3.0.0</p>
    </div>
</body>
</html>
"""
        
        return html
