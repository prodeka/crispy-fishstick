"""
Module de parallélisation pour l'analyse Monte Carlo des réseaux AEP.

Ce module implémente :
- Parallélisation des simulations Monte Carlo avec multiprocessing
- Distribution intelligente des tâches entre workers
- Gestion de la mémoire et des ressources
- Intégration avec le système de cache
"""

import multiprocessing as mp
import time
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Callable, Optional, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging
from dataclasses import dataclass
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from ..core.cache_manager import get_cache_manager, HydraulicCacheManager
from ..core.solvers import SolverFactory

logger = logging.getLogger(__name__)


@dataclass
class MonteCarloTask:
    """Représente une tâche Monte Carlo."""
    task_id: int
    network_data: Dict[str, Any]
    parameters: Dict[str, Any]
    solver_name: str
    cache_key: Optional[str] = None


@dataclass
class MonteCarloResult:
    """Représente le résultat d'une simulation Monte Carlo."""
    task_id: int
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    cache_hit: bool = False


class ParallelMonteCarloAnalyzer:
    """Analyseur Monte Carlo parallélisé pour les réseaux AEP."""
    
    def __init__(self, 
                 max_workers: Optional[int] = None,
                 use_cache: bool = True,
                 cache_manager: Optional[HydraulicCacheManager] = None):
        """
        Initialise l'analyseur Monte Carlo parallélisé.
        
        Args:
            max_workers: Nombre maximum de workers (None = auto-détection)
            use_cache: Activer l'utilisation du cache
            cache_manager: Gestionnaire de cache personnalisé
        """
        self.max_workers = max_workers or min(mp.cpu_count(), 8)
        self.use_cache = use_cache
        self.cache_manager = cache_manager or get_cache_manager()
        
        # Statistiques
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
            "total_execution_time": 0.0
        }
        
        logger.info(f"Analyseur Monte Carlo initialisé avec {self.max_workers} workers")
    
    def run_parallel_analysis(self,
                             base_network: Dict[str, Any],
                             parameter_distributions: Dict[str, Any],
                             num_simulations: int,
                             solver_name: str = "lcpi",
                             progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Lance l'analyse Monte Carlo parallélisée.
        
        Args:
            base_network: Réseau de base
            parameter_distributions: Distributions des paramètres
            num_simulations: Nombre de simulations
            solver_name: Nom du solveur à utiliser
            progress_callback: Callback pour le suivi de progression
            
        Returns:
            Résultats de l'analyse Monte Carlo
        """
        start_time = time.time()
        
        # 1. Préparer les tâches
        tasks = self._prepare_tasks(base_network, parameter_distributions, 
                                  num_simulations, solver_name)
        
        # 2. Exécuter les tâches en parallèle
        results = self._execute_tasks_parallel(tasks, progress_callback)
        
        # 3. Analyser les résultats
        analysis_results = self._analyze_results(results)
        
        # 4. Mettre à jour les statistiques
        self.stats["total_tasks"] = len(tasks)
        self.stats["completed_tasks"] = len(results)
        self.stats["total_execution_time"] = time.time() - start_time
        
        return {
            "results": results,
            "analysis": analysis_results,
            "stats": self.stats,
            "execution_time": self.stats["total_execution_time"]
        }
    
    def _prepare_tasks(self,
                       base_network: Dict[str, Any],
                       parameter_distributions: Dict[str, Any],
                       num_simulations: int,
                       solver_name: str) -> List[MonteCarloTask]:
        """
        Prépare la liste des tâches Monte Carlo.
        
        Args:
            base_network: Réseau de base
            parameter_distributions: Distributions des paramètres
            num_simulations: Nombre de simulations
            solver_name: Nom du solveur
            
        Returns:
            Liste des tâches à exécuter
        """
        tasks = []
        
        for i in range(num_simulations):
            # Générer des paramètres aléatoires selon les distributions
            random_parameters = self._generate_random_parameters(parameter_distributions)
            
            # Créer une copie du réseau avec les nouveaux paramètres
            network_variant = self._create_network_variant(base_network, random_parameters)
            
            # Créer la tâche
            task = MonteCarloTask(
                task_id=i,
                network_data=network_variant,
                parameters=random_parameters,
                solver_name=solver_name
            )
            
            tasks.append(task)
        
        return tasks
    
    def _generate_random_parameters(self, distributions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère des paramètres aléatoires selon les distributions spécifiées.
        
        Args:
            distributions: Définitions des distributions
            
        Returns:
            Paramètres aléatoires générés
        """
        random_params = {}
        
        for param_name, dist_config in distributions.items():
            dist_type = dist_config.get("type", "normal")
            
            if dist_type == "normal":
                mean = dist_config["mean"]
                std = dist_config["std"]
                random_params[param_name] = np.random.normal(mean, std)
                
            elif dist_type == "uniform":
                min_val = dist_config["min"]
                max_val = dist_config["max"]
                random_params[param_name] = np.random.uniform(min_val, max_val)
                
            elif dist_type == "lognormal":
                mean = dist_config["mean"]
                std = dist_config["std"]
                random_params[param_name] = np.random.lognormal(mean, std)
                
            elif dist_type == "discrete":
                values = dist_config["values"]
                probabilities = dist_config.get("probabilities", None)
                random_params[param_name] = np.random.choice(values, p=probabilities)
            
            # Appliquer les contraintes si spécifiées
            if "min" in dist_config:
                random_params[param_name] = max(random_params[param_name], dist_config["min"])
            if "max" in dist_config:
                random_params[param_name] = min(random_params[param_name], dist_config["max"])
        
        return random_params
    
    def _create_network_variant(self, 
                               base_network: Dict[str, Any], 
                               parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée une variante du réseau avec de nouveaux paramètres.
        
        Args:
            base_network: Réseau de base
            parameters: Nouveaux paramètres
            
        Returns:
            Variante du réseau
        """
        # Copie profonde du réseau de base
        import copy
        network_variant = copy.deepcopy(base_network)
        
        # Appliquer les paramètres aux éléments appropriés
        for param_name, value in parameters.items():
            if param_name.startswith("node_"):
                # Paramètre de nœud
                node_id = param_name.split("_", 1)[1]
                if node_id in network_variant.get("nodes", {}):
                    network_variant["nodes"][node_id]["demand"] = value
                    
            elif param_name.startswith("pipe_"):
                # Paramètre de conduite
                pipe_id = param_name.split("_", 1)[1]
                if pipe_id in network_variant.get("pipes", {}):
                    if "roughness" in param_name:
                        network_variant["pipes"][pipe_id]["roughness"] = value
                    elif "diameter" in param_name:
                        network_variant["pipes"][pipe_id]["diameter"] = value
        
        return network_variant
    
    def _execute_tasks_parallel(self, 
                               tasks: List[MonteCarloTask],
                               progress_callback: Optional[Callable] = None) -> List[MonteCarloResult]:
        """
        Exécute les tâches en parallèle.
        
        Args:
            tasks: Liste des tâches à exécuter
            progress_callback: Callback pour le suivi de progression
            
        Returns:
            Liste des résultats
        """
        results = []
        
        # Vérifier le cache pour les tâches existantes
        if self.use_cache:
            tasks = self._check_cache_for_tasks(tasks)
        
        # Exécuter les tâches restantes en parallèle
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Soumettre toutes les tâches
            future_to_task = {
                executor.submit(self._execute_single_task, task): task 
                for task in tasks if not task.cache_key
            }
            
            # Traiter les résultats au fur et à mesure
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Mettre à jour le cache si nécessaire
                    if self.use_cache and result.success and result.result:
                        self._cache_task_result(task, result.result)
                    
                    # Callback de progression
                    if progress_callback:
                        progress_callback(len(results), len(tasks))
                        
                except Exception as e:
                    error_result = MonteCarloResult(
                        task_id=task.task_id,
                        success=False,
                        error=str(e),
                        execution_time=0.0
                    )
                    results.append(error_result)
                    self.stats["errors"] += 1
        
        # Ajouter les résultats du cache
        if self.use_cache:
            cache_results = self._get_cached_results(tasks)
            results.extend(cache_results)
        
        return results
    
    def _execute_single_task(self, task: MonteCarloTask) -> MonteCarloResult:
        """
        Exécute une seule tâche Monte Carlo.
        
        Args:
            task: Tâche à exécuter
            
        Returns:
            Résultat de la tâche
        """
        start_time = time.time()
        
        try:
            # Obtenir le solveur
            solver = SolverFactory.get_solver(task.solver_name)
            
            # Exécuter la simulation
            result = solver.run_simulation(task.network_data)
            
            execution_time = time.time() - start_time
            
            return MonteCarloResult(
                task_id=task.task_id,
                success=True,
                result=result,
                execution_time=execution_time,
                cache_hit=False
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            return MonteCarloResult(
                task_id=task.task_id,
                success=False,
                error=str(e),
                execution_time=execution_time,
                cache_hit=False
            )
    
    def _check_cache_for_tasks(self, tasks: List[MonteCarloTask]) -> List[MonteCarloTask]:
        """
        Vérifie le cache pour les tâches existantes.
        
        Args:
            tasks: Liste des tâches
            
        Returns:
            Tâches mises à jour avec les clés de cache
        """
        for task in tasks:
            if self.use_cache and self.cache_manager:
                cached_result = self.cache_manager.get_hydraulic_result(
                    task.network_data, task.solver_name
                )
                if cached_result:
                    task.cache_key = "cached"
                    self.stats["cache_hits"] += 1
                else:
                    self.stats["cache_misses"] += 1
        
        return tasks
    
    def _cache_task_result(self, task: MonteCarloTask, result: Dict[str, Any]):
        """Met en cache le résultat d'une tâche."""
        if self.use_cache and self.cache_manager:
            self.cache_manager.cache_hydraulic_result(
                task.network_data, task.solver_name, result
            )
    
    def _get_cached_results(self, tasks: List[MonteCarloTask]) -> List[MonteCarloResult]:
        """Récupère les résultats du cache."""
        cached_results = []
        
        for task in tasks:
            if task.cache_key == "cached":
                cached_result = MonteCarloResult(
                    task_id=task.task_id,
                    success=True,
                    result={"cached": True},  # Placeholder
                    execution_time=0.0,
                    cache_hit=True
                )
                cached_results.append(cached_result)
        
        return cached_results
    
    def _analyze_results(self, results: List[MonteCarloResult]) -> Dict[str, Any]:
        """
        Analyse les résultats Monte Carlo.
        
        Args:
            results: Liste des résultats
            
        Returns:
            Analyse des résultats
        """
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]
        
        analysis = {
            "total_simulations": len(results),
            "successful_simulations": len(successful_results),
            "failed_simulations": len(failed_results),
            "success_rate": len(successful_results) / len(results) if results else 0,
            "cache_hit_rate": self.stats["cache_hits"] / len(results) if results else 0,
            "average_execution_time": np.mean([r.execution_time for r in successful_results]) if successful_results else 0,
            "execution_time_std": np.std([r.execution_time for r in successful_results]) if successful_results else 0
        }
        
        # Analyser les paramètres des simulations réussies
        if successful_results:
            # Extraire les paramètres et résultats pour l'analyse statistique
            # (à implémenter selon les besoins spécifiques)
            pass
        
        return analysis


def run_parallel_monte_carlo(base_network: Dict[str, Any],
                           parameter_distributions: Dict[str, Any],
                           num_simulations: int,
                           solver_name: str = "lcpi",
                           max_workers: Optional[int] = None,
                           use_cache: bool = True,
                           progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
    """
    Fonction utilitaire pour lancer une analyse Monte Carlo parallélisée.
    
    Args:
        base_network: Réseau de base
        parameter_distributions: Distributions des paramètres
        num_simulations: Nombre de simulations
        solver_name: Nom du solveur
        max_workers: Nombre maximum de workers
        use_cache: Activer le cache
        progress_callback: Callback de progression
        
    Returns:
        Résultats de l'analyse
    """
    analyzer = ParallelMonteCarloAnalyzer(
        max_workers=max_workers,
        use_cache=use_cache
    )
    
    return analyzer.run_parallel_analysis(
        base_network=base_network,
        parameter_distributions=parameter_distributions,
        num_simulations=num_simulations,
        solver_name=solver_name,
        progress_callback=progress_callback
    )


# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple de distributions de paramètres
    parameter_distributions = {
        "node_demand": {
            "type": "normal",
            "mean": 0.001,
            "std": 0.0002,
            "min": 0.0001,
            "max": 0.002
        },
        "pipe_roughness": {
            "type": "uniform",
            "min": 100,
            "max": 150
        }
    }
    
    # Exemple de réseau de base
    base_network = {
        "nodes": {
            "N1": {"demand": 0.001, "elevation": 100},
            "N2": {"demand": 0.0008, "elevation": 95}
        },
        "pipes": {
            "P1": {"from": "N1", "to": "N2", "length": 100, "diameter": 150}
        }
    }
    
    # Lancer l'analyse
    results = run_parallel_monte_carlo(
        base_network=base_network,
        parameter_distributions=parameter_distributions,
        num_simulations=100,
        solver_name="lcpi",
        max_workers=4,
        use_cache=True
    )
    
    print(f"Analyse terminée en {results['execution_time']:.2f} secondes")
    print(f"Taux de succès: {results['analysis']['success_rate']:.2%}")
    print(f"Taux de cache: {results['analysis']['cache_hit_rate']:.2%}")
