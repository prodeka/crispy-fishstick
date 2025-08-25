from __future__ import annotations

import pickle
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

import numpy as np
# Les dépendances `pymoo` ne sont pas toujours disponibles (en environnement CI minimal).
# On tente l'import, sinon on fournit des stubs qui déclencheront une erreur uniquement à l'exécution.
try:  # pragma: no cover
    from pymoo.algorithms.moo.nsga2 import NSGA2  # type: ignore
    from pymoo.core.problem import Problem  # type: ignore
    from pymoo.optimize import minimize  # type: ignore
    from pymoo.termination import get_termination  # type: ignore
    _PYMOO_AVAILABLE = True
except Exception:  # pragma: no cover
    _PYMOO_AVAILABLE = False

    class Problem:  # minimal stub
        def __init__(self, *args, **kwargs):
            pass

    class NSGA2:  # minimal stub
        def __init__(self, *args, **kwargs):
            pass

    def minimize(*args, **kwargs):
        raise ImportError("pymoo n'est pas installé. Installez-le pour utiliser GlobalOptimizer.")

    def get_termination(*args, **kwargs):
        return None

from ..models import OptimizationConfig, OptimizationResult, Proposal, TankDecision
from ..solvers import EPANETOptimizer
from ..scoring import CostScorer
from ..db_dao import get_candidate_diameters
from ..inp_utils import count_pipes

# Structure pour passer les données à l'évaluation parallèle
EVAL_TUPLE = Tuple[np.ndarray, OptimizationConfig, Path]


def evaluate_candidate(eval_tuple: EVAL_TUPLE) -> Dict[str, Any]:
    """Fonction exécutée dans un processus parallèle pour évaluer un individu."""
    chromosome, config, network_path = eval_tuple

    # Write debugging information to a log file
    try:
        with open("debug_diameters.log", "a") as f:
            f.write(f"Evaluating chromosome: {chromosome}\n")
    except Exception: # Ignore file writing errors
        pass # Continue execution even if logging fails

    try:
        # Décoder le chromosome
        # Le premier gène est la hauteur du tank, les autres sont des index de diamètres
        h_tanks = {list(config.h_bounds_m.keys())[0]: float(chromosome[0])}

        candidate_diams = get_candidate_diameters()
        # Créer un mapping des diamètres basé sur les indices du chromosome
        diam_map = {}
        for i, idx in enumerate(chromosome[1:], 1):
            if 0 <= int(idx) < len(candidate_diams):
                try:
                    with open("debug_diameters.log", "a") as f:
                        f.write(f" Pipe {i}: index {int(idx)} -> diameter {candidate_diams[int(idx)]['d_mm']} mm\n")
                except Exception: # Ignore file writing errors
                    pass
                diam_map[f"pipe_{i}"] = candidate_diams[int(idx)]["d_mm"]
            else:
                # Index invalide, utiliser le diamètre par défaut
                try:
                    with open("debug_diameters.log", "a") as f:
                        f.write(f" Pipe {i}: Invalid index {int(idx)}. Using default diameter {candidate_diams[0]['d_mm']} mm.\n")
                except Exception: # Ignore file writing errors
                    pass
                diam_map[f"pipe_{i}"] = candidate_diams[0]["d_mm"]

        # Simulation
        solver = EPANETOptimizer()
        sim_result = solver.simulate(
            network_path,
            H_tank_map=h_tanks, 
            diameters_map=diam_map,
            duration_h=24,
            timestep_min=5,
            timeout_s=30
        )

        if not sim_result.get("success") or sim_result.get("min_pressure_m", 0) < config.pressure_min_m or sim_result.get("max_velocity_m_s", 0) > config.velocity_max_m_s:
            return {"feasible": False, "capex": 1e12, "opex_npv": 1e12}  # Pénalité forte

        # Scoring (le CostScorer interrogera la DB si aucun mapping fourni)
        scorer = CostScorer(diameter_cost_db={})
        costs = scorer.evaluate_solution(network=None, diameters=diam_map, sim_results=sim_result) # type: ignore
        
        return {"feasible": True, **costs}
        
    except Exception as e:
        # En cas d'erreur, retourner une solution invalide
        return {"feasible": False, "capex": 1e12, "opex_npv": 1e12, "error": str(e)}


class TankAEPProblem(Problem):
    """Définit le problème d'optimisation pour pymoo avec parallélisation."""
    
    def __init__(self, config: OptimizationConfig, network_path: Path, executor: ProcessPoolExecutor):
        self.config = config
        self.network_path = network_path
        self.executor = executor
        
        # Déterminer le nombre de conduites à partir du réseau
        num_pipes = count_pipes(self.network_path)
        n_var = 1 + num_pipes
        
        # Bornes des variables
        h_bounds = list(config.h_bounds_m.values())[0]
        num_diams = len(get_candidate_diameters())
        xl = np.array([h_bounds[0]] + [0] * num_pipes)
        xu = np.array([h_bounds[1]] + [num_diams - 1] * num_pipes)

        super().__init__(n_var=n_var, n_obj=2, n_constr=1, xl=xl, xu=xu)

    def _evaluate(self, x, out, *args, **kwargs):
        """Évalue une population en parallèle."""
        # Préparer les tâches pour l'évaluation parallèle
        tasks = [(ind, self.config, self.network_path) for ind in x]
        
        # Utiliser l'exécuteur parallèle
        results = list(self.executor.map(evaluate_candidate, tasks))
        
        # Extraire les objectifs (CAPEX, OPEX) et les contraintes
        objectives = np.array([[r["capex"], r["opex_npv"]] for r in results])
        constraints = np.array([[0 if r["feasible"] else 1] for r in results])  # 0 = contrainte respectée

        out["F"] = objectives
        out["G"] = constraints


class GlobalOptimizer:
    """Optimiseur global basé sur NSGA-II (pymoo) avec parallélisation et checkpoints."""

    def __init__(self, config: OptimizationConfig, network_path: Path, progress_callback=None):
        if not _PYMOO_AVAILABLE:
            raise ImportError("pymoo n'est pas installé. Installez-le pour utiliser GlobalOptimizer.")
        
        self.config = config
        self.network_path = network_path
        self.progress_callback = progress_callback
        
        # Configuration des checkpoints
        checkpoint_dir = Path("data/checkpoints")
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        if config.global_config.resume_from_checkpoint:
            self.checkpoint_path = Path(config.global_config.resume_from_checkpoint)
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.checkpoint_path = checkpoint_dir / f"global_opt_{timestamp}.pkl"
        
        # Configuration de la parallélisation
        self.parallel_workers = config.global_config.parallel_workers or min(multiprocessing.cpu_count(), 4)
        
        # Historique des meilleures solutions
        self.best_fitness_history = []
        self.generation_history = []

    def optimize(self) -> OptimizationResult:
        """Exécute l'optimisation NSGA-II avec parallélisation et checkpoints."""
        print(f"🚀 Démarrage de l'optimisation globale avec {self.parallel_workers} workers")
        
        with ProcessPoolExecutor(max_workers=self.parallel_workers) as executor:
            problem = TankAEPProblem(self.config, self.network_path, executor)
            
            algorithm = NSGA2(
                pop_size=self.config.global_config.population_size,
                eliminate_duplicates=True
            )

            termination = get_termination("n_gen", self.config.global_config.generations)

            # Gestion des checkpoints
            if self.config.global_config.resume_from_checkpoint and self.checkpoint_path.exists():
                try:
                    with open(self.checkpoint_path, "rb") as f:
                        checkpoint_data = pickle.load(f)
                    
                    # Vérifier la compatibilité du checkpoint
                    if self._validate_checkpoint(checkpoint_data):
                        algorithm = checkpoint_data["algorithm"]
                        self.best_fitness_history = checkpoint_data.get("best_fitness", [])
                        self.generation_history = checkpoint_data.get("generations", [])
                        print(f"✅ Reprise de l'optimisation depuis {self.checkpoint_path}")
                        print(f"   Génération actuelle: {len(self.generation_history)}")
                    else:
                        print("⚠️ Checkpoint incompatible, démarrage d'une nouvelle optimisation")
                except Exception as e:
                    print(f"⚠️ Erreur lors du chargement du checkpoint: {e}")
                    print("   Démarrage d'une nouvelle optimisation")

            # Callback pour les checkpoints et progress UI
            checkpoint_callback = self._create_checkpoint_callback(algorithm)
            progress_callback = self._create_progress_callback() if self.progress_callback else None
            
            # Combiner les callbacks
            if progress_callback:
                callback = lambda algo: (checkpoint_callback(algo), progress_callback(algo))
            else:
                callback = checkpoint_callback
            
            print(f"🎯 Optimisation: {self.config.global_config.population_size} individus, "
                  f"{self.config.global_config.generations} générations")
            
            # Émettre generation_start si callback disponible
            if self.progress_callback:
                try:
                    self.progress_callback("generation_start", {
                        "generation": 0,
                        "total_generations": self.config.global_config.generations,
                        "population_size": self.config.global_config.population_size
                    })
                except Exception:
                    pass
            
            res = minimize(
                problem,
                algorithm,
                termination,
                seed=1,
                save_history=True,
                verbose=True,
                callback=callback
            )
            
            # Sauvegarder le checkpoint final
            self._save_checkpoint(algorithm, res)
            
            # Convertir le résultat en format V11
            return self._convert_to_v11_result(res)
    
    def _convert_to_v11_result(self, pymoo_result) -> OptimizationResult:
        """Convertit le résultat pymoo en OptimizationResult V11."""
        proposals = []
        
        # Créer des propositions à partir des solutions Pareto
        for i, (capex, opex) in enumerate(pymoo_result.F):
            # Créer une décision de tank basée sur la première solution
            tank_id = list(self.config.h_bounds_m.keys())[0]
            tank_decision = TankDecision(
                id=tank_id,
                H_m=float(pymoo_result.X[i][0])  # Première variable = hauteur du tank
            )
            
            # Créer une proposition
            proposal = Proposal(
                name=f"global_solution_{i+1}",
                is_feasible=True,  # Les solutions Pareto sont toutes faisables
                tanks=[tank_decision],
                diameters_mm={},  # À implémenter si nécessaire
                costs={"CAPEX": float(capex), "OPEX_npv": float(opex)},
                metrics={"min_pressure_m": self.config.pressure_min_m}
            )
            proposals.append(proposal)
        
        # Créer le front de Pareto
        pareto_front = []
        for i, (capex, opex) in enumerate(pymoo_result.F):
            pareto_front.append({
                "name": f"global_solution_{i+1}",
                "CAPEX": float(capex),
                "OPEX": float(opex)
            })
        
        # Métadonnées
        metadata = {
            "method": "global_optimization",
            "algorithm": "NSGA-II",
            "network_file": str(self.network_path),
            "population_size": self.config.global_config.population_size,
            "generations": self.config.global_config.generations,
            "parallel_workers": self.parallel_workers,
            "execution_time": None,  # À calculer si nécessaire
            "iterations": len(self.generation_history)
        }
        
        return OptimizationResult(
            proposals=proposals,
            pareto_front=pareto_front,
            metadata=metadata
        )

    def _create_checkpoint_callback(self, algorithm):
        """Crée un callback pour sauvegarder l'état de l'algorithme."""
        def checkpoint_callback(algorithm):
            self._save_checkpoint(algorithm)
        return checkpoint_callback

    def _create_progress_callback(self):
        """Crée un callback pour émettre les événements de progression."""
        def callback(algorithm):
            try:
                if self.progress_callback:
                    # Émettre generation_end avec les meilleures solutions
                    current_gen = len(algorithm.callback.data["n_gen"])
                    if current_gen > 0:
                        # Trouver la meilleure solution (fitness le plus bas)
                        best_idx = np.argmin(algorithm.callback.data["F"][-1])
                        best_fitness = float(algorithm.callback.data["F"][-1][best_idx])
                        
                        self.progress_callback("generation_end", {
                            "generation": current_gen,
                            "best_cost": best_fitness,
                            "population_size": self.config.global_config.population_size
                        })
                        
                        # Émettre generation_start pour la prochaine génération
                        if current_gen < self.config.global_config.generations:
                            self.progress_callback("generation_start", {
                                "generation": current_gen,
                                "total_generations": self.config.global_config.generations,
                                "population_size": self.config.global_config.population_size
                            })
            except Exception as e:
                # Ignorer silencieusement les erreurs de callback
                pass
        
        return callback

    def _save_checkpoint(self, algorithm, result=None):
        """Sauvegarde l'état de l'algorithme et des métadonnées."""
        try:
            checkpoint_data = {
                "algorithm": algorithm,
                "best_fitness": self.best_fitness_history,
                "generations": self.generation_history,
                "timestamp": datetime.now().isoformat(),
                "config": self.config.dict(),
                "network_path": str(self.network_path)
            }
            
            if result:
                checkpoint_data["result"] = result
            
            with open(self.checkpoint_path, "wb") as f:
                pickle.dump(checkpoint_data, f)
            
            print(f"💾 Checkpoint sauvegardé: {self.checkpoint_path}")
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la sauvegarde du checkpoint: {e}")

    def _validate_checkpoint(self, checkpoint_data: Dict) -> bool:
        """Valide la compatibilité d'un checkpoint."""
        try:
            required_keys = ["algorithm", "config", "network_path"]
            if not all(key in checkpoint_data for key in required_keys):
                return False
            
            # Vérifier que le réseau est le même
            if checkpoint_data["network_path"] != str(self.network_path):
                return False
            
            # Vérifier que la configuration est compatible
            checkpoint_config = checkpoint_data["config"]
            if (checkpoint_config.get("method") != self.config.method or
                checkpoint_config.get("pressure_min_m") != self.config.pressure_min_m):
                return False
            
            return True
            
        except Exception:
            return False

    def resume_from_checkpoint(self, checkpoint_file: str) -> Dict[str, Any]:
        """Reprend l'optimisation depuis un checkpoint spécifique."""
        self.config.global_config.resume_from_checkpoint = checkpoint_file
        return self.optimize()

    def get_optimization_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel de l'optimisation."""
        return {
            "checkpoint_path": str(self.checkpoint_path),
            "parallel_workers": self.parallel_workers,
            "generations_completed": len(self.generation_history),
            "best_fitness_history": self.best_fitness_history,
            "last_checkpoint": self.checkpoint_path.stat().st_mtime if self.checkpoint_path.exists() else None
        }


