"""
GeneticOptimizer V2 - Améliorations:
- Initialisation mixte (heuristique + aléatoire)
- Uniform crossover + mutation adaptative (selon stagnation)
- Réparation (adjust h_tank si pression insuffisante)
- Parallélisation des évaluations (multiprocessing)
- Mémoïsation / cache des simulations
- Evénements riches (_emit) pour UI / ProgressManager
"""

import time
import random
import math
import hashlib
import json
from typing import List, Dict, Tuple, Optional, Callable, Any
from dataclasses import dataclass, field
from multiprocessing import Pool, cpu_count
import numpy as np

# IMPORTS PROJET (adapter aux chemins réels)
from .models import ConfigurationOptimisation, DiametreCommercial  # type: ignore
from .constraints import ConstraintManager  # type: ignore
from .individual import Individu  # type: ignore
from ..core.epanet_wrapper import EPANETOptimizer  # type: ignore

# ---- Helpers -----------------
def _hash_candidate(diams: List[int], h_tank: Optional[float]) -> str:
    payload = {"d": diams, "h": h_tank}
    return hashlib.sha1(json.dumps(payload, sort_keys=True).encode()).hexdigest()

# ---- GeneticOptimizerV2 -----
class GeneticOptimizerV2:
    """
    Version améliorée de l'optimiseur génétique.
    """

    def __init__(
        self,
        config: ConfigurationOptimisation,
        constraint_manager: ConstraintManager,
        network_path: Optional[str] = None,
        solver: Optional[EPANETOptimizer] = None,
        pipe_ids: Optional[List[str]] = None,
        workers: Optional[int] = None,
        seed: Optional[int] = None,
    ):
        self.config = config
        self.constraint_manager = constraint_manager
        self.network_path = network_path
        self.solver = solver
        self.pipe_ids = pipe_ids
        self.population: List[Individu] = []
        self.best_solution: Optional[Individu] = None
        self.history: List[Dict[str, Any]] = []
        self.on_generation_callback: Optional[Callable[[List[Individu], int], None]] = None
        self._progress_cb: Optional[Callable[[str, dict], None]] = None

        # Parameters
        self.generations = int(getattr(self.config.algorithme, "generations", 120))
        self.population_size = int(getattr(self.config.algorithme, "population_size", 120))
        self.crossover_rate = float(getattr(self.config.algorithme, "crossover_rate", 0.9))
        self.mutation_rate_base = float(getattr(self.config.algorithme, "mutation_rate", 0.02))
        self.elitism_ratio = float(getattr(self.config.algorithme, "elitism_ratio", 0.10))
        self.h_bounds = getattr(self.config, "h_bounds_m", {"min": 0.0, "max": 50.0})
        self.pressure_default_min = float(getattr(self.config, "pressure_min_default", 10.0))
        self.velocity_min_default = float(getattr(self.config, "velocity_min_default", 0.3))
        self.velocity_max_default = float(getattr(self.config, "velocity_max_default", 1.5))

        self.workers = workers or max(1, min(cpu_count(), 8))
        self.cache: Dict[str, Dict[str, Any]] = {}  # key -> simulation payload
        self.stagnation_counter = 0
        self.best_cost_history: List[float] = []
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # quick lookup of candidate diameters (list of DiametreCommercial)
        self.diam_candidats: List[DiametreCommercial] = list(getattr(self.config, "diametres_candidats", []))

    # ---------------- callbacks ----------------
    def set_on_generation_callback(self, callback: Optional[Callable[[List[Individu], int], None]]) -> None:
        """Accept either (population, generation) or (evt, data) signature."""
        self.on_generation_callback = callback
        try:
            if callback and callback.__code__.co_argcount == 2:
                self._progress_cb = callback  # type: ignore
        except Exception:
            pass

    def set_progress_callback(self, cb: Optional[Callable[[str, dict], None]]) -> None:
        """Standard setter used by controller."""
        self._progress_cb = cb

    def _emit(self, evt: str, data: dict) -> None:
        cb = getattr(self, "_progress_cb", None)
        if not cb:
            return
        try:
            cb(evt, data)
        except Exception:
            pass

    # -------------- initialization ----------------
    def initialiser_population(self, nb_conduites: int, reseau_data: Optional[Dict] = None) -> None:
        """
        Initialise la population: mélange d'individus heuristiques et aléatoires.
        Heuristique: dimensionne diamètres selon débit nominal ou vitesse cible.
        """
        self.population = []
        heuristics_ratio = 0.2  # 20% heuristique
        n_heur = max(1, int(self.population_size * heuristics_ratio))
        n_random = self.population_size - n_heur

        # precompute candidate diam list in mm
        candidate_diams = [int(d.diametre_mm) for d in self.diam_candidats]
        if not candidate_diams:
            raise ValueError("Aucun diamètre candidat défini dans la config")

        # Heuristic individuals
        for _ in range(n_heur):
            diams = []
            for i in range(nb_conduites):
                # try to use reseau_data if available to estimate flow
                debit = None
                if reseau_data and "conduites" in reseau_data and i < len(reseau_data["conduites"]):
                    debit = reseau_data["conduites"][i].get("debit_m3_s") or reseau_data["conduites"][i].get("q_m3_s")
                # target velocity (m/s) moderate to avoid extremes
                target_v = 0.8
                chosen = candidate_diams[len(candidate_diams)//2]  # default mid
                if debit and debit > 0:
                    # pick smallest candidate with section >= needed to get target_v
                    for d in candidate_diams:
                        section = math.pi * (d / 1000) ** 2 / 4
                        v = debit / section
                        if v <= target_v:
                            chosen = d
                            break
                diams.append(int(chosen))
            # choose h_tank near mid-range
            h_min = float(self.h_bounds.get("min", 0.0))
            h_max = float(self.h_bounds.get("max", 50.0))
            h_val = (h_min + h_max) / 2.0
            ind = Individu(diametres=diams, h_tank_m=float(h_val))
            self.population.append(ind)

        # Random individuals
        for _ in range(n_random):
            diams = [int(random.choice(candidate_diams)) for _ in range(nb_conduites)]
            # h_tank random within bounds but biased toward mid
            h_min = float(self.h_bounds.get("min", 0.0))
            h_max = float(self.h_bounds.get("max", 50.0))
            h_val = random.uniform(h_min + (h_max - h_min) * 0.25, h_max - (h_max - h_min) * 0.25)
            ind = Individu(diametres=diams, h_tank_m=float(h_val))
            self.population.append(ind)

    # -------------- evaluation ----------------
    def _simulate_or_approx(self, individu: Individu, reseau_data: Optional[Dict]) -> Dict[str, Any]:
        """
        Exécute une simulation via le solver (si présent) ou renvoie une approximation.
        Utilise cache pour éviter simulations répétées exactes.
        Retourne: { success: bool, min_pressure_m, max_velocity_m_s, sim_time_s }
        """
        key = _hash_candidate(individu.diametres, getattr(individu, "h_tank_m", None))
        if key in self.cache:
            return self.cache[key]

        result: Dict[str, Any] = {"success": False}

        if self.solver and self.network_path:
            # build diams map
            diam_map = {}
            if self.pipe_ids and len(self.pipe_ids) == len(individu.diametres):
                diam_map = {self.pipe_ids[i]: d for i, d in enumerate(individu.diametres)}
            # H_tank map heuristic
                h_map = {}
            if getattr(individu, "h_tank_m", None) is not None:
                # if tank IDs unknown, the wrapper will interpret/assign as appropriate
                    h_map = {"tank1": float(individu.h_tank_m)}
            t0 = time.time()
            try:
                sim = self.solver.simulate(
                    self.network_path,
                    H_tank_map=h_map,
                    diameters_map=diam_map,
                    duration_h=1,
                    timestep_min=5,
                    progress_callback=self._progress_cb,
                )
                t1 = time.time()
                sim_time = max(0.0, t1 - t0)
                # normalize some keys
                result = {
                    "success": bool(sim.get("success", False)),
                    "min_pressure_m": float(sim.get("min_pressure_m", 0.0) or 0.0),
                    "max_velocity_m_s": float(sim.get("max_velocity_m_s", 0.0) or 0.0),
                    "min_velocity_m_s": float(sim.get("min_velocity_m_s", 0.0) or 0.0),
                    "sim_time_s": sim_time,
                    "raw": sim
                }
            except Exception as e:
                result = {"success": False, "error": str(e)}
            else:
                # approximation simple (Hazen-Williams based losses -> pressure proxy)
                # This is a cheap check: compute approximate velocities and a pressure proxy
                min_p = float("inf")
                max_v = 0.0
                for i, d in enumerate(individu.diametres):
                    diam_m = d / 1000.0
                    debit = 0.1  # default if unknown
                    if reseau_data and "conduites" in reseau_data and i < len(reseau_data["conduites"]):
                        debit = float(reseau_data["conduites"][i].get("debit_m3_s", debit))
                    section = math.pi * diam_m * diam_m / 4.0
                    v = debit / section if section > 0 else 0.0
                    max_v = max(max_v, v)
                    # crude proxy: pressure loss ~ v^2 -> so min pressure approx inverse
                    p_proxy = max(0.0, 50.0 - (v * 5.0))  # puppet proxy
                    min_p = min(min_p, p_proxy)
                result = {"success": True, "min_pressure_m": min_p, "max_velocity_m_s": max_v, "min_velocity_m_s": 0.0, "sim_time_s": 0.0}
        # cache
        self.cache[key] = result
        return result

    def _calculate_cost(self, individu: Individu, reseau_data: Optional[Dict]) -> float:
        """Calculate CAPEX using candidate costs and link lengths if available."""
        total = 0.0
        for i, d in enumerate(individu.diametres):
            unit_cost = None
            for c in self.diam_candidats:
                if int(c.diametre_mm) == int(d):
                    unit_cost = getattr(c, "cout_fcfa_m", None)
                    break
            if unit_cost is None:
                # fallback estimate (proportional to diameter^2)
                unit_cost = (d ** 2) * 0.01
            length = 1.0
            if reseau_data and "conduites" in reseau_data and i < len(reseau_data["conduites"]):
                length = float(reseau_data["conduites"][i].get("longueur_m", 1.0))
            total += unit_cost * length
        return float(total)

    def _repair_if_needed(self, individu: Individu, sim_result: Dict[str, Any]) -> Tuple[Individu, Dict[str, Any]]:
        """
        Tentative de réparation simple: si pression min insuffisante, augmenter h_tank progressivement
        jusqu'à h_max. Retourne (individu_potentiellement_modifie, sim_result_final).
        """
        p_min = float(sim_result.get("min_pressure_m", 0.0) or 0.0)
        p_req = float(getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "pression_min_mce", self.pressure_default_min))
        if p_min >= p_req or getattr(individu, "h_tank_m", None) is None:
            return individu, sim_result

        # try to increase tank height by steps until feasible or max reached
        h_current = float(individu.h_tank_m)
        h_max = float(self.h_bounds.get("max", 50.0))
        step = max(0.5, (h_max - h_current) * 0.1)
        attempts = 0
        last_sim = sim_result
        while p_min < p_req and h_current < h_max and attempts < 6:
            h_current = min(h_max, h_current + step)
            individu.h_tank_m = float(h_current)
            last_sim = self._simulate_or_approx(individu, None)
            p_min = float(last_sim.get("min_pressure_m", 0.0) or 0.0)
            attempts += 1
        return individu, last_sim

    def _evaluate_individual(self, args: Tuple[int, int, Individu, Optional[Dict], int]) -> Tuple[int, Individu, float, Dict[str, Any]]:
        """Worker-friendly evaluation: args=(generation, idx1, individu, reseau_data, pop_size) -> (idx1, individu, fitness, sim_result)"""
        generation, idx1, individu, reseau_data, pop_size = args
        try:
            self._emit("sim_start", {"generation": generation, "index": idx1, "population_size": pop_size})
        except Exception:
            pass
        sim = self._simulate_or_approx(individu, reseau_data)
        try:
            self._emit("sim_done", {"generation": generation, "index": idx1, "population_size": pop_size, "success": bool(sim.get("success", False))})
        except Exception:
            pass
        # attempt repair only if simulation failed or pressure not met
        if sim.get("success") and sim.get("min_pressure_m", 0.0) < getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "pression_min_mce", self.pressure_default_min):
            individu, sim = self._repair_if_needed(individu, sim)

        # cost
        cost = self._calculate_cost(individu, reseau_data)
        penal = 0.0
        if not sim.get("success"):
            penal += 1e6  # keep but it's softened by repair attempt
        else:
            # pressure penalty (soft)
            p_req = float(getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "pression_min_mce", self.pressure_default_min))
            p_min = float(sim.get("min_pressure_m", 0.0) or 0.0)
            if p_min < p_req:
                penal += 1e5 * (p_req - p_min) ** 2
            # velocity penalties
            v_max_req = float(getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "vitesse_max_m_s", self.velocity_max_default))
            v_min_req = float(getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "vitesse_min_m_s", self.velocity_min_default))
            vmax_obs = float(sim.get("max_velocity_m_s", 0.0) or 0.0)
            vmin_obs = float(sim.get("min_velocity_m_s", 0.0) or 0.0)
            if vmax_obs > v_max_req:
                penal += 1e5 * (vmax_obs - v_max_req) ** 2
            if vmin_obs < v_min_req:
                penal += 1e4 * (v_min_req - vmin_obs) ** 2

        # energy approx: use sim raw if exists (wrapper may provide energy_W)
        energy = float(sim.get("raw", {}).get("energy_W", 0.0) or 0.0)
        # composite objective (normalized)
        # normalize cost by a scaling factor (configurable)
        cost_scale = max(1.0, getattr(self.config, "cost_scale", 1e5))
        norm_cost = cost / cost_scale
        perf = self._approx_performance(individu, sim)
        # weights
        alpha = float(getattr(self.config.criteres, "alpha", 0.7)) if hasattr(self.config, "criteres") else 0.7
        beta = float(getattr(self.config.criteres, "beta", 0.2)) if hasattr(self.config, "criteres") else 0.2
        gamma = float(getattr(self.config.criteres, "gamma", 0.1)) if hasattr(self.config, "criteres") else 0.1

        objective = alpha * norm_cost + beta * (1.0 - perf) + gamma * (energy / (1.0 + energy))
        total_score = cost + penal  # used for reporting
        # fitness = inverse of objective (higher better)
        fitness = 1.0 / (1.0 + objective)
        # store fields on individu for reporting
        individu.cout_total = float(cost)
        individu.energie_totale = float(energy)
        individu.performance_hydraulique = float(perf)
        individu.constraints_ok = (penal == 0.0)
        # Agrégation de statistiques hydrauliques globales
        try:
            _hs = getattr(self, "_hydro_stats", None) or {
                "sim_count": 0,
                "success_count": 0,
                "min_pressure_min": float("inf"),
                "max_velocity_max": 0.0,
                "min_velocity_min": float("inf"),
                "sum_min_pressure": 0.0,
                "sum_max_velocity": 0.0,
            }
            _hs["sim_count"] += 1
            _hs["success_count"] += 1 if sim.get("success") else 0
            pmin = float(sim.get("min_pressure_m", float("inf")) or float("inf"))
            vmax = float(sim.get("max_velocity_m_s", 0.0) or 0.0)
            vmin = float(sim.get("min_velocity_m_s", float("inf")) or float("inf"))
            _hs["min_pressure_min"] = min(_hs["min_pressure_min"], pmin)
            _hs["max_velocity_max"] = max(_hs["max_velocity_max"], vmax)
            _hs["min_velocity_min"] = min(_hs["min_velocity_min"], vmin)
            if pmin != float("inf"):
                _hs["sum_min_pressure"] += pmin
            _hs["sum_max_velocity"] += vmax
            setattr(self, "_hydro_stats", _hs)
        except Exception:
            pass
        return idx1, individu, float(fitness), sim

    def _approx_performance(self, individu: Individu, sim_res: Dict[str, Any]) -> float:
        """Estimate an hydrau performance between 0 and 1 from sim result or proxy."""
        if sim_res.get("success"):
            v_max = float(sim_res.get("max_velocity_m_s", 0.0) or 0.0)
            v_min = float(sim_res.get("min_velocity_m_s", 0.0) or 0.0)
            # target interval
            vmin = getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "vitesse_min_m_s", self.velocity_min_default)
            vmax = getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "vitesse_max_m_s", self.velocity_max_default)
            # penalize extremes
            if v_min < vmin or v_max > vmax:
                return max(0.0, 1.0 - ((vmin - v_min) if v_min < vmin else 0.0) - ((v_max - vmax) if v_max > vmax else 0.0))
            return 1.0
        return 0.0

    # ---------------- genetic operators ----------------
    def _uniform_crossover(self, p1: Individu, p2: Individu) -> Tuple[Individu, Individu]:
        """Uniform crossover per gene (diamètre and h_tank)."""
        n = len(p1.diametres)
        child1 = Individu(diametres=p1.diametres.copy(), h_tank_m=getattr(p1, "h_tank_m", None))
        child2 = Individu(diametres=p2.diametres.copy(), h_tank_m=getattr(p2, "h_tank_m", None))
        for i in range(n):
            if random.random() < 0.5:
                child1.diametres[i], child2.diametres[i] = child2.diametres[i], child1.diametres[i]
        # crossover h_tank with 50% pick
        if hasattr(p1, "h_tank_m") and hasattr(p2, "h_tank_m") and random.random() < 0.5:
            child1.h_tank_m, child2.h_tank_m = p2.h_tank_m, p1.h_tank_m
        return child1, child2

    def _adaptive_mutation(self, individu: Individu, mutation_rate: float) -> None:
        """Mutation that can also nudge h_tank and offers higher exploration when stagnating."""
        # diameters mutation: with mutation_rate change a gene
        for i in range(len(individu.diametres)):
            if random.random() < mutation_rate:
                individu.diametres[i] = int(random.choice([int(d.diametre_mm) for d in self.diam_candidats]))
        # mutate tank height slightly
        if hasattr(individu, "h_tank_m") and random.random() < (mutation_rate * 0.5):
            h_min = float(self.h_bounds.get("min", 0.0))
            h_max = float(self.h_bounds.get("max", 50.0))
            perturb = (h_max - h_min) * (random.uniform(-0.05, 0.05))
            individu.h_tank_m = float(max(h_min, min(h_max, individu.h_tank_m + perturb)))

    # ---------------- main loop ----------------
    def optimiser(self, reseau_data: Optional[Dict] = None, nb_conduites: Optional[int] = None) -> Dict[str, Any]:
        """Main entry: run GA and return canonical JSON-like result."""
        t_start = time.time()
        # compute nb_conduites
        if nb_conduites is None:
            if self.pipe_ids:
                nb_conduites = len(self.pipe_ids)
            else:
                # try from reseau_data
                if reseau_data and "conduites" in reseau_data:
                    nb_conduites = len(reseau_data["conduites"])
                else:
                    raise ValueError("nb_conduites non spécifié et pipe_ids/reseau_data absents")
        
        # init population
        self.initialiser_population(int(nb_conduites), reseau_data)
        
        total_gen = int(self.generations)
        pop_size = int(self.population_size)

        # warm-up: emit run_start
        try:
            self._emit("run_start", {"generations": total_gen, "population": pop_size, "num_solvers": 1})
        except Exception:
            pass

        # create multiprocessing pool if needed
        use_mp = False  # DÉSACTIVÉ TEMPORAIREMENT: (self.workers > 1 and self.solver is not None)
        pool = Pool(processes=self.workers) if use_mp else None

        for generation in range(total_gen):
            gen_t0 = time.time()
            # adaptive mutation rate based on stagnation
            mutation_rate = self.mutation_rate_base * (1.0 + min(5.0, self.stagnation_counter * 0.5))

            # emit generation_start
            try:
                self._emit("generation_start", {"generation": generation, "total_generations": total_gen, "population_size": pop_size})
            except Exception:
                pass

            # Evaluate population (parallel if possible)
            args = [(generation, i + 1, ind, reseau_data, pop_size) for i, ind in enumerate(self.population)]
            results = []
            if pool:
                results = pool.map(self._evaluate_individual, args)
            else:
                results = [self._evaluate_individual(a) for a in args]

            # unpack results; update individuals
            for idx, ind, fitness, sim in results:
                ind.fitness = float(fitness)
                # emit individual_start event
                try:
                    self._emit("individual_start", {"generation": generation, "index": idx, "candidate_id": getattr(ind, "id", None)})
                except Exception:
                    pass
                # emit individual_end event
                try:
                    self._emit("individual_end", {"generation": generation, "index": idx, "candidate_id": getattr(ind, "id", None), "cost": getattr(ind, "cout_total", None), "fitness": ind.fitness, "feasible": bool(getattr(ind, "constraints_ok", False))})
                except Exception:
                    pass

            # sort population by fitness descending
            self.population.sort(key=lambda x: getattr(x, "fitness", 0.0), reverse=True)

            # track best
            current_best = self.population[0]
            current_best_cost = float(getattr(current_best, "cout_total", float("inf")) or float("inf"))
            if self.best_solution is None or self.population[0].fitness > getattr(self.best_solution, "fitness", -1):
                self.best_solution = Individu(
                    diametres=self.population[0].diametres.copy(),
                    h_tank_m=getattr(self.population[0], "h_tank_m", None),
                    fitness=self.population[0].fitness,
                    cout_total=self.population[0].cout_total,
                    energie_totale=self.population[0].energie_totale,
                    performance_hydraulique=self.population[0].performance_hydraulique,
                )
                self.stagnation_counter = 0
                try:
                    self._emit("best_improved", {"generation": generation, "new_cost": current_best_cost})
                except Exception:
                    pass
            else:
                self.stagnation_counter += 1

            self.best_cost_history.append(current_best_cost)
            
            # history record
            fitness_vals = [getattr(ind, "fitness", 0.0) for ind in self.population]
            mean_fitness = float(np.mean(fitness_vals)) if fitness_vals else 0.0
            self.history.append({
                "generation": generation,
                "best_fitness": float(self.population[0].fitness),
                "mean_fitness": mean_fitness,
                "best_cost": current_best_cost,
                "stagnation": int(self.stagnation_counter),
            })

            # emit generation_end
            try:
                self._emit("generation_end", {"generation": generation, "best_cost": current_best_cost, "best_id": getattr(self.population[0], "id", None)})
            except Exception:
                pass

            # optionally call external on_generation_callback (UI)
            try:
                if self.on_generation_callback:
                    # provide limited frequency to avoid spam
                    if generation % max(1, total_gen // 40) == 0 or generation in (0, total_gen - 1):
                        self.on_generation_callback(self.population, generation)
            except Exception:
                pass

            # create new generation
            nouvelle_population: List[Individu] = []
            nb_elites = max(1, int(self.elitism_ratio * pop_size))
            nouvelle_population.extend(self.population[:nb_elites])
            
            # fill rest
            while len(nouvelle_population) < pop_size:
                # selection: binary tournament
                parent1 = self._tournament_select(3)
                parent2 = self._tournament_select(3)
                # crossover (with probability)
                if random.random() < self.crossover_rate:
                    child1, child2 = self._uniform_crossover(parent1, parent2)
                else:
                    child1, child2 = Individu(diametres=parent1.diametres.copy(), h_tank_m=getattr(parent1, "h_tank_m", None)), Individu(diametres=parent2.diametres.copy(), h_tank_m=getattr(parent2, "h_tank_m", None))
                # mutation
                self._adaptive_mutation(child1, mutation_rate)
                self._adaptive_mutation(child2, mutation_rate)
                nouvelle_population.append(child1)
                if len(nouvelle_population) < pop_size:
                    nouvelle_population.append(child2)

            # replace population (truncate if oversize)
            self.population = nouvelle_population[:pop_size]

        # clean up pool
        if pool:
            pool.close()
            pool.join()

        duration = time.time() - t_start
        # final report
        result = self._generer_resultats(duration_seconds=duration)
        return result

    # ---------------- selection ----------------
    def _tournament_select(self, k: int = 3) -> Individu:
        participants = random.sample(self.population, min(k, len(self.population)))
        return max(participants, key=lambda x: getattr(x, "fitness", 0.0))

    # ---------------- results ----------------
    def _generer_resultats(self, duration_seconds: float = 0.0) -> Dict[str, Any]:
        """Sortie standardisée pour intégration rapports."""
        algo_type = getattr(getattr(self.config, "algorithme", None), "type", "genetic_v2")
        best = self.best_solution
        diam_map = {}
        if best:
            if self.pipe_ids and len(best.diametres) == len(self.pipe_ids):
                diam_map = {self.pipe_ids[i]: int(best.diametres[i]) for i in range(len(best.diametres))}
            else:
                diam_map = {f"C{i+1}": int(best.diametres[i]) for i in range(len(best.diametres))}
        # Calcul des statistiques hydrauliques agrégées
        hs = getattr(self, "_hydro_stats", {}) or {}
        avg_min_pressure = 0.0
        avg_max_velocity = 0.0
        if hs.get("sim_count", 0) > 0:
            avg_min_pressure = float(hs.get("sum_min_pressure", 0.0)) / float(hs.get("sim_count", 1))
            avg_max_velocity = float(hs.get("sum_max_velocity", 0.0)) / float(hs.get("sim_count", 1))
        
        # Statistiques hydrauliques détaillées si disponibles
        detailed_stats = {}
        if hasattr(self, "last_hydraulics") and self.last_hydraulics:
            try:
                from ..optimizer.controllers import _calculate_hydraulic_statistics
                detailed_stats = _calculate_hydraulic_statistics(self.last_hydraulics)
            except Exception as e:
                detailed_stats = {"error": str(e)}
        return {
            "optimisation": {
                "algorithme": algo_type,
                "meta": {
                    "generations": self.generations,
                    "population": self.population_size,
                    "duration_seconds": float(duration_seconds),
                    "best_cost_history": self.best_cost_history,
                    "stagnation": self.stagnation_counter,
                    "evaluations": len(self.cache),
                    "hydraulics_stats": {
                        "sim_count": int(hs.get("sim_count", 0)),
                        "success_count": int(hs.get("success_count", 0)),
                        "min_pressure_min": float(hs.get("min_pressure_min", 0.0) if hs.get("min_pressure_min", float("inf")) != float("inf") else 0.0),
                        "max_velocity_max": float(hs.get("max_velocity_max", 0.0)),
                        "min_velocity_min": float(hs.get("min_velocity_min", 0.0) if hs.get("min_velocity_min", float("inf")) != float("inf") else 0.0),
                        "avg_min_pressure": float(avg_min_pressure),
                        "avg_max_velocity": float(avg_max_velocity),
                        "detailed_statistics": detailed_stats,
                    },
                },
                "meilleure_solution": {
                    "diameters_mm": diam_map,
                    "cout_total_fcfa": float(getattr(best, "cout_total", 0.0) if best else 0.0),
                    "energie_total_wh": float(getattr(best, "energie_totale", 0.0) if best else 0.0),
                    "performance_hydraulique": float(getattr(best, "performance_hydraulique", 0.0) if best else 0.0),
                },
                "historique": self.history,
            }
        }
