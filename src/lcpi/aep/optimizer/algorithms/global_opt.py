from __future__ import annotations

import pickle
import json
import sys
import os
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
    from pymoo.operators.sampling.rnd import FloatRandomSampling  # type: ignore
    from pymoo.operators.mutation.real_mut import PolynomialMutation  # type: ignore
    from pymoo.operators.crossover.real_cro import SimulatedBinaryCrossover  # type: ignore
    from pymoo.core.mutation import Mutation  # type: ignore
    from pymoo.core.crossover import Crossover  # type: ignore
    _PYMOO_AVAILABLE = True
except Exception:  # pragma: no cover
    _PYMOO_AVAILABLE = False

    class Problem:  # minimal stub
        def __init__(self, *args, **kwargs):
            pass

    class NSGA2:  # minimal stub
        def __init__(self, *args, **kwargs):
            pass

    class Crossover:  # minimal stub
        def __init__(self, *args, **kwargs):
            pass

    class Mutation:  # minimal stub
        def __init__(self, *args, **kwargs):
            pass

    class FloatRandomSampling:  # minimal stub
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
    # Resolve an absolute logs directory near the project root to avoid worker CWD issues
    try:
        potential_roots = [p for p in Path(__file__).resolve().parents]
        project_root: Optional[Path] = None
        for p in potential_roots:
            if (p / "test_validation").exists():
                project_root = p
                break
        if project_root is None:
            project_root = Path.cwd()

        logs_dir = project_root / "test_validation" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        debug_log_path = str(logs_dir / "debug_diameters.log")
        # Per-process log to avoid Windows file locking issues
        debug_log_path_pid = str(logs_dir / f"debug_diameters_{os.getpid()}.log")
        debug_trace_path = str(logs_dir / "debug_path_trace.log")
    except Exception:
        # Fallback to relative paths if anything above fails
        debug_log_path = "test_validation/logs/debug_diameters.log"
        debug_log_path_pid = f"test_validation/logs/debug_diameters_{os.getpid()}.log"
        debug_trace_path = "test_validation/logs/debug_path_trace.log"
    try:
        # Tenter d'écrire le chemin absolu du fichier pour débogage
        try:
            abs_path = Path(debug_log_path).resolve()
            with open(debug_trace_path, "a") as f_trace:
                 f_trace.write(f"Attempting to write debug log to: {abs_path}\n")
        except Exception as e_trace:
            print(f"Error writing debug path trace: {e_trace}", file=sys.stderr)

        # Tenter d'écrire dans le fichier de débogage principal et par-processus
        line = f"[{datetime.now().isoformat()}] pid={os.getpid()} Evaluating chromosome: {chromosome}\n"
        try:
            with open(debug_log_path, "a", buffering=1) as f:
                f.write(line)
        except Exception as e_main:
            print(f"Error writing to shared debug_diameters.log: {e_main}", file=sys.stderr)
        with open(debug_log_path_pid, "a", buffering=1) as fpid:
            fpid.write(line)
    except Exception as e:
        # Imprimer l'erreur si l'écriture échoue
        print(f"Error writing to debug_diameters.log: {e}", file=sys.stderr)
        pass # Continue execution even if logging fails

    try:
        # Décoder le chromosome
        # Le premier gène est la hauteur du tank, les autres sont des index de diamètres
        h_tanks = {list(config.h_bounds_m.keys())[0]: float(chromosome[0])}

        candidate_diams = get_candidate_diameters()
        # Créer un mapping des diamètres basé sur les indices du chromosome
        diam_map = {}
        for i, idx in enumerate(chromosome[1:], 1):
            idx_int = int(idx)
            if 0 <= idx_int < len(candidate_diams):
                try:
                    msg = f"[{datetime.now().isoformat()}] pid={os.getpid()} Pipe {i}: index {idx_int} -> diameter {candidate_diams[idx_int]['d_mm']} mm\n"
                    try:
                        with open(debug_log_path, "a", buffering=1) as f:
                            f.write(msg)
                    except Exception as e_main:
                        print(f"Error writing diameter info to shared log: {e_main}", file=sys.stderr)
                    with open(debug_log_path_pid, "a", buffering=1) as fpid:
                        fpid.write(msg)
                except Exception as e:
                    print(f"Error writing diameter info to debug logs: {e}", file=sys.stderr)
                    pass
                diam_map[f"pipe_{i}"] = candidate_diams[idx_int]["d_mm"]
            else:
                # Index invalide, utiliser une logique de réparation intelligente
                # Essayer de trouver un index valide proche
                valid_idx = np.clip(idx_int, 0, len(candidate_diams) - 1)
                try:
                    msg = f"[{datetime.now().isoformat()}] pid={os.getpid()} Pipe {i}: Invalid index {idx_int}. Repaired to {valid_idx} -> diameter {candidate_diams[valid_idx]['d_mm']} mm.\n"
                    try:
                        with open(debug_log_path, "a", buffering=1) as f:
                            f.write(msg)
                    except Exception as e_main:
                        print(f"Error writing invalid index info to shared log: {e_main}", file=sys.stderr)
                    with open(debug_log_path_pid, "a", buffering=1) as fpid:
                        fpid.write(msg)
                except Exception as e:
                    print(f"Error writing invalid index info to debug logs: {e}", file=sys.stderr)
                    pass
                diam_map[f"pipe_{i}"] = candidate_diams[valid_idx]["d_mm"]

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


class MixedVariableCrossover(Crossover):
    """Opérateur de croisement adapté aux variables mixtes (continue + discrètes)."""
    
    def __init__(self, prob=0.9, eta=15):
        super().__init__(2, 2)  # 2 parents, 2 enfants
        self.prob = prob
        self.eta = eta
    
    def _do(self, problem, X, **kwargs):
        n_parents, n_matings, n_var = X.shape
        
        # Créer les enfants
        Y = np.full_like(X, -1.0, dtype=float)
        
        for i in range(n_matings):
            p1, p2 = X[0, i], X[1, i]
            
            # Pour la première variable (hauteur du tank) : croisement continu
            if np.random.random() < self.prob:
                # Croisement polynomial pour la variable continue
                u = np.random.random()
                if u <= 0.5:
                    beta = (2 * u) ** (1.0 / (self.eta + 1))
                else:
                    beta = (1.0 / (2 * (1 - u))) ** (1.0 / (self.eta + 1))
                
                Y[0, i, 0] = 0.5 * ((1 + beta) * p1[0] + (1 - beta) * p2[0])
                Y[1, i, 0] = 0.5 * ((1 - beta) * p1[0] + (1 + beta) * p2[0])
            else:
                Y[0, i, 0] = p1[0]
                Y[1, i, 0] = p2[0]
            
            # Pour les variables discrètes (index de diamètres) : croisement uniforme
            for j in range(1, n_var):
                if np.random.random() < self.prob:
                    # Croisement uniforme pour les index
                    if np.random.random() < 0.5:
                        Y[0, i, j] = p1[j]
                        Y[1, i, j] = p2[j]
                    else:
                        Y[0, i, j] = p2[j]
                        Y[1, i, j] = p1[j]
                else:
                    Y[0, i, j] = p1[j]
                    Y[1, i, j] = p2[j]
        
        return Y


class DiverseMixedVariableSampling(FloatRandomSampling):
    """Opérateur de sampling pour assurer la diversité de la population initiale."""
    
    def __init__(self, num_diams=None):
        super().__init__()
        self.num_diams = num_diams
    
    def _do(self, problem, n_samples, **kwargs):
        # Générer des échantillons pour les variables continues (hauteur du tank)
        X = super()._do(problem, n_samples, **kwargs)
        
        # Pour les variables discrètes (index de diamètres), assurer une distribution uniforme
        if self.num_diams is not None:
            for i in range(n_samples):
                for j in range(1, problem.n_var):  # Skip first variable (tank height)
                    # Générer un index aléatoire uniformément distribué
                    X[i, j] = np.random.randint(0, self.num_diams)
        
        return X


class MixedVariableMutation(Mutation):
    """Opérateur de mutation adapté aux variables mixtes."""
    
    def __init__(self, prob=None, eta=20, num_diams=None):
        super().__init__()
        self.prob = prob
        self.eta = eta
        self.num_diams = num_diams
    
    def _do(self, problem, X, **kwargs):
        Xp = X.copy()
        
        for i in range(len(X)):
            for j in range(problem.n_var):
                if np.random.random() < self.prob:
                    if j == 0:  # Variable continue (hauteur du tank)
                        # Mutation polynomiale pour la variable continue
                        xl, xu = problem.xl[j], problem.xu[j]
                        delta1 = (X[i, j] - xl) / (xu - xl)
                        delta2 = (xu - X[i, j]) / (xu - xl)
                        
                        mut_pow = 1.0 / (self.eta + 1.0)
                        
                        if np.random.random() <= 0.5:
                            xy = 1.0 - delta1
                            val = 2.0 * np.random.random() + (1.0 - 2.0 * np.random.random()) * (xy ** (self.eta + 1.0))
                            deltaq = val ** mut_pow - 1.0
                        else:
                            xy = 1.0 - delta2
                            val = 2.0 * (1.0 - np.random.random()) + 2.0 * (np.random.random() - 0.5) * (xy ** (self.eta + 1.0))
                            deltaq = 1.0 - val ** mut_pow
                        
                        Xp[i, j] = X[i, j] + deltaq * (xu - xl)
                        Xp[i, j] = np.clip(Xp[i, j], xl, xu)
                    
                    else:  # Variables discrètes (index de diamètres)
                        # Mutation par inversion pour les index
                        if self.num_diams is not None:
                            # Mutation par déplacement aléatoire dans la plage valide
                            current_idx = int(X[i, j])
                            # Déplacement de ±1 ou ±2 avec probabilité décroissante
                            shift = np.random.choice([-2, -1, 1, 2], p=[0.1, 0.3, 0.3, 0.1])
                            new_idx = current_idx + shift
                            # Maintenir dans la plage valide
                            new_idx = np.clip(new_idx, 0, self.num_diams - 1)
                            Xp[i, j] = new_idx
                        else:
                            # Fallback : mutation simple
                            Xp[i, j] = np.random.randint(0, int(problem.xu[j]) + 1)
        
        return Xp


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
        self.num_diams = len(get_candidate_diameters())
        xl = np.array([h_bounds[0]] + [0] * num_pipes)
        xu = np.array([h_bounds[1]] + [self.num_diams - 1] * num_pipes)

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
        print(f"🔧 Utilisation d'opérateurs génétiques adaptés aux variables mixtes")
        
        with ProcessPoolExecutor(max_workers=self.parallel_workers) as executor:
            problem = TankAEPProblem(self.config, self.network_path, executor)
            
            # Configuration des opérateurs génétiques adaptés aux variables mixtes
            sampling = DiverseMixedVariableSampling(num_diams=problem.num_diams)
            crossover = MixedVariableCrossover(prob=0.9, eta=15)
            mutation = MixedVariableMutation(
                prob=1.0 / problem.n_var,  # Probabilité de mutation par variable
                eta=20,
                num_diams=problem.num_diams
            )
            
            algorithm = NSGA2(
                pop_size=self.config.global_config.population_size,
                sampling=sampling,
                crossover=crossover,
                mutation=mutation,
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


