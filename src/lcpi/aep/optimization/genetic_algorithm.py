"""
GeneticOptimizer V2 - Améliorations AGAMO:
- Initialisation physique adaptative (estimation diamètres par vitesse cible)
- Réparation guidée par contraintes (augmentation diamètres si vitesse excessive)
- Pénalités adaptatives (feasibility-first avec pondérations dynamiques)
- Mutation biaisée vers diamètres supérieurs en cas de violations
- Optimisation multi-phase (coarse-to-fine)
- Diversité et robustesse améliorées
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
from pathlib import Path
import os
from datetime import datetime
from collections import Counter, defaultdict

# IMPORTS PROJET (adapter aux chemins réels)
from .models import ConfigurationOptimisation, DiametreCommercial  # type: ignore
from .constraints import ConstraintManager  # type: ignore
from .individual import Individu  # type: ignore
from ..core.epanet_wrapper import EPANETOptimizer  # type: ignore
from .repairs import soft_repair_solution  # type: ignore

# ---- Helpers -----------------
def _hash_candidate(diams: List[int], h_tank: Optional[float]) -> str:
    payload = {"d": diams, "h": h_tank}
    return hashlib.sha1(json.dumps(payload, sort_keys=True).encode()).hexdigest()

def _estimate_initial_diameter(debit_m3_s: float, target_velocity_m_s: float = 1.0) -> float:
    """Estime un diamètre initial basé sur le débit et une vitesse cible."""
    if debit_m3_s <= 0:
        return 200.0  # diamètre par défaut
    section_m2 = debit_m3_s / target_velocity_m_s
    diam_m = math.sqrt(4 * section_m2 / math.pi)
    return diam_m * 1000.0  # conversion en mm

def _find_nearest_candidate(diam_mm: float, candidates: List[int]) -> int:
    """Trouve le candidat le plus proche d'un diamètre donné."""
    if not candidates:
        return 200
    return min(candidates, key=lambda x: abs(x - diam_mm))

def _get_next_candidate(diam_mm: float, candidates: List[int], direction: int = 1) -> int:
    """Trouve le candidat suivant/précédent dans la liste triée."""
    if not candidates:
        return diam_mm
    sorted_cands = sorted(candidates)
    try:
        current_idx = sorted_cands.index(diam_mm)
        new_idx = max(0, min(len(sorted_cands) - 1, current_idx + direction))
        return sorted_cands[new_idx]
    except ValueError:
        return _find_nearest_candidate(diam_mm, candidates)

# ---- GeneticOptimizerV2 -----
class GeneticOptimizerV2:
    """
    Version AGAMO de l'optimiseur génétique avec adaptabilité complète.
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

        # Parameters AGAMO
        self.generations = int(getattr(self.config.algorithme, "generations", 120))
        self.population_size = int(getattr(self.config.algorithme, "population_size", 120))
        self.crossover_rate = float(getattr(self.config.algorithme, "crossover_rate", 0.9))
        self.mutation_rate_base = float(getattr(self.config.algorithme, "mutation_rate", 0.02))
        self.elitism_ratio = float(getattr(self.config.algorithme, "elitism_ratio", 0.10))
        self.h_bounds = getattr(self.config, "h_bounds_m", {"min": 0.0, "max": 50.0})
        self.pressure_default_min = float(getattr(self.config, "pressure_min_default", 10.0))
        self.velocity_min_default = float(getattr(self.config, "velocity_min_default", 0.3))
        self.velocity_max_default = float(getattr(self.config, "velocity_max_default", 1.5))

        # AGAMO: Paramètres adaptatifs
        self.current_phase = 1  # 1: exploration, 2: exploitation, 3: raffinement
        self.stagnation_counter = 0
        self.repair_history: Dict[int, int] = defaultdict(int)  # pipe_idx -> count
        self.constraint_violation_history: Dict[str, int] = defaultdict(int)
        self.adaptive_penalty_weights = {
            "pressure": 1.0,
            "velocity_max": 1.0,
            "velocity_min": 1.0,
            "uniformity": 1.0
        }
        self.feasibility_found = False
        self.generations_without_improvement = 0
        self.best_cost_history: List[float] = []

        self.workers = 1  # Forcer séquentiel pour éviter les problèmes de pickle
        self.cache: Dict[str, Dict[str, Any]] = {}  # key -> simulation payload
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # Charger les diamètres candidats depuis le gestionnaire centralisé
        try:
            from ..optimizer.diameter_manager import get_standard_diameters_with_prices
            diam_rows = get_standard_diameters_with_prices("PVC-U")
            self.diam_candidats = []
            for row in diam_rows:
                candidate = DiametreCommercial(
                    diametre_mm=int(row.get("d_mm")),
                    cout_fcfa_m=float(row.get("cost_per_m", row.get("total_fcfa_per_m", 1000.0)))
                )
                self.diam_candidats.append(candidate)
            logger.info(f"✅ {len(self.diam_candidats)} diamètres chargés depuis le gestionnaire centralisé")
        except Exception as e:
            logger.warning(f"Erreur lors du chargement des diamètres centralisés: {e}")
            # Utiliser les diamètres de la config si disponibles
            self.diam_candidats: List[DiametreCommercial] = list(getattr(self.config, "diametres_candidats", []))
            if not self.diam_candidats:
                logger.warning("⚠️ Aucun diamètre candidat disponible, utilisation des diamètres par défaut")
                # Créer des diamètres par défaut avec prix réalistes
                STANDARD_DIAMETERS = [50, 63, 75, 90, 110, 125, 140, 160, 180, 200, 225, 250, 280, 315, 355, 400, 450, 500]
                for d in STANDARD_DIAMETERS:
                    base_price = 50.0
                    size_factor = (d / 100.0) ** 1.8
                    cost = base_price * size_factor
                    candidate = DiametreCommercial(diametre_mm=d, cout_fcfa_m=cost)
                    self.diam_candidats.append(candidate)
                logger.info(f"✅ {len(self.diam_candidats)} diamètres par défaut créés avec prix réalistes")
        
        # AGAMO: Plages adaptatives par conduite
        self.pipe_diameter_ranges: Dict[int, List[int]] = {}
        self.pipe_repair_bias: Dict[int, float] = defaultdict(float)
        
        # Préparer le dossier de logs (partagé et par-processus)
        try:
            proj = None
            for p in Path(__file__).resolve().parents:
                if (p / "test_validation").exists():
                    proj = p
                    break
            if proj is None:
                proj = Path.cwd()
            self._logs_dir = proj / "test_validation" / "logs"
            self._logs_dir.mkdir(parents=True, exist_ok=True)
            self._ga_log_shared = self._logs_dir / "ga_chromosomes.log"
            self._ga_log_pid = self._logs_dir / f"ga_chromosomes_{os.getpid()}.log"
        except Exception:
            self._logs_dir = None
            self._ga_log_shared = None
            self._ga_log_pid = None
            
        # Journaliser un résumé des candidats (taille, min/max, diversité)
        try:
            if self.diam_candidats:
                vals = [int(d.diametre_mm) for d in self.diam_candidats]
                uniq = sorted(set(vals))
                self._log_ga(
                    f"candidates={len(vals)} unique={len(uniq)} range=[{min(vals)}, {max(vals)}] sample={uniq[:10]}"
                )
            else:
                self._log_ga("candidates=0 (AUCUN DIAMETRE CANDIDAT)")
        except Exception:
            pass
        # Journaliser la réception de pipe_ids
        try:
            n_pid = len(self.pipe_ids) if self.pipe_ids else 0
            self._log_ga(f"pipe_ids_received_len={n_pid}")
            if n_pid > 0:
                sample_n = min(10, n_pid)
                details = [f"pipe_ids[{i}]={self.pipe_ids[i]}" for i in range(sample_n)]
                self._log_ga("pipe_ids_sample:", details)
        except Exception:
            pass

    def _log_ga(self, line: str, details: Optional[List[str]] = None) -> None:
        """Ecrit une ligne de log GA (chromosomes) dans les fichiers partagé et par-processus."""
        try:
            ts = datetime.now().isoformat()
            msg = f"[{ts}] pid={os.getpid()} {line}\n"
            if self._ga_log_shared:
                try:
                    with open(self._ga_log_shared, "a", buffering=1, encoding="utf-8") as f:
                        f.write(msg)
                        if details:
                            for d in details[:50]:
                                f.write(f"  {d}\n")
                except Exception:
                    pass
            if self._ga_log_pid:
                with open(self._ga_log_pid, "a", buffering=1, encoding="utf-8") as f2:
                    f2.write(msg)
                    if details:
                        for d in details[:200]:
                            f2.write(f"  {d}\n")
        except Exception:
            pass

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

    # -------------- AGAMO: Initialisation Physique Adaptative ----------------
    def _estimate_pipe_initial_diameters(self, reseau_data: Optional[Dict]) -> Dict[int, int]:
        """Estime les diamètres initiaux par conduite basés sur la physique du réseau."""
        candidate_diams = [int(d.diametre_mm) for d in self.diam_candidats]
        if not candidate_diams:
            return {}
            
        pipe_diams = {}
        
        # Méthode 1: Estimation par débit nominal
        if reseau_data and "conduites" in reseau_data:
            for i, conduite in enumerate(reseau_data["conduites"]):
                debit = conduite.get("debit_m3_s") or conduite.get("q_m3_s", 0.1)
                # Vitesse cible adaptative selon la taille du réseau
                target_v = 0.8  # vitesse modérée pour éviter les extrêmes
                est_diam = _estimate_initial_diameter(debit, target_v)
                chosen_diam = _find_nearest_candidate(est_diam, candidate_diams)
                pipe_diams[i] = chosen_diam
                
        # Méthode 2: Estimation par longueur (proxy pour l'importance)
        elif reseau_data and "conduites" in reseau_data:
            lengths = [c.get("longueur_m", 100.0) for c in reseau_data["conduites"]]
            if lengths:
                max_len = max(lengths)
                for i, length in enumerate(lengths):
                    # Conduites plus longues = diamètres plus grands
                    ratio = length / max_len
                    diam_idx = int(ratio * (len(candidate_diams) - 1))
                    diam_idx = max(0, min(len(candidate_diams) - 1, diam_idx))
                    pipe_diams[i] = candidate_diams[diam_idx]
                    
        # Méthode 3: Distribution équilibrée
        else:
            for i in range(len(self.pipe_ids) if self.pipe_ids else 100):
                # Distribution centrée sur le milieu de la gamme
                diam_idx = len(candidate_diams) // 2
                pipe_diams[i] = candidate_diams[diam_idx]
                
        return pipe_diams

    def _build_adaptive_diameter_ranges(self, reseau_data: Optional[Dict]) -> None:
        """Construit des plages adaptatives de diamètres par conduite."""
        candidate_diams = [int(d.diametre_mm) for d in self.diam_candidats]
        if not candidate_diams:
            return
            
        initial_diams = self._estimate_pipe_initial_diameters(reseau_data)
        
        for pipe_idx in range(len(self.pipe_ids) if self.pipe_ids else 100):
            initial_diam = initial_diams.get(pipe_idx, candidate_diams[len(candidate_diams)//2])
            
            # Phase 1: Plage large (±5 paliers)
            range_size = min(5, len(candidate_diams) // 3)
            initial_idx = candidate_diams.index(initial_diam) if initial_diam in candidate_diams else len(candidate_diams)//2
            
            start_idx = max(0, initial_idx - range_size)
            end_idx = min(len(candidate_diams), initial_idx + range_size + 1)
            
            self.pipe_diameter_ranges[pipe_idx] = candidate_diams[start_idx:end_idx]
            
        self._log_ga(f"AGAMO: Built adaptive ranges for {len(self.pipe_diameter_ranges)} pipes")

    def initialiser_population(self, nb_conduites: int, reseau_data: Optional[Dict] = None) -> None:
        """
        AGAMO: Initialisation physique adaptative avec plages locales.
        """
        self.population = []

        # Construire les plages adaptatives
        self._build_adaptive_diameter_ranges(reseau_data)
        
        candidate_diams = [int(d.diametre_mm) for d in self.diam_candidats]
        if not candidate_diams:
            raise ValueError("Aucun diamètre candidat défini dans la config")

        # AGAMO: Distribution adaptative avec h_tank_m optimisé
        heuristics_ratio = 0.4  # 40% heuristique (augmenté)
        n_heur = max(1, int(self.population_size * heuristics_ratio))
        n_random = self.population_size - n_heur

        # Individus heuristiques (physique adaptative avec h_tank_m)
        for _ in range(n_heur):
            diams = []
            for i in range(nb_conduites):
                # Initialiser debit par défaut
                debit = 0.1
                
                # Utiliser la plage adaptative si disponible
                if i in self.pipe_diameter_ranges:
                    local_candidates = self.pipe_diameter_ranges[i]
                    chosen = random.choice(local_candidates)
                else:
                    # Fallback: estimation par débit
                    if reseau_data and "conduites" in reseau_data and i < len(reseau_data["conduites"]):
                        debit = reseau_data["conduites"][i].get("debit_m3_s") or reseau_data["conduites"][i].get("q_m3_s", 0.1)
                    else:
                        debit = 0.1
                    target_v = 0.8
                    est_diam = _estimate_initial_diameter(debit, target_v)
                    chosen = _find_nearest_candidate(est_diam, candidate_diams)
                
                diams.append(int(chosen))
                
            # h_tank adaptatif - Utiliser h_max comme guide principal
            h_min = float(self.h_bounds.get("min", 0.0))
            h_max = float(self.h_bounds.get("max", 50.0))
            
            # Stratégie intelligente : favoriser les hauteurs qui permettent la satisfaction des contraintes
            # 70% de chance d'utiliser une hauteur élevée (plus de pression disponible)
            if random.random() < 0.7:
                h_val = random.uniform(h_min + (h_max - h_min) * 0.6, h_max - (h_max - h_min) * 0.1)
            else:
                # 30% de chance d'explorer les hauteurs moyennes
                h_val = random.uniform(h_min + (h_max - h_min) * 0.3, h_min + (h_max - h_min) * 0.7)
            
            ind = Individu(diametres=diams, h_tank_m=float(h_val))
            self.population.append(ind)

        # Individus aléatoires avec biais vers les plages adaptatives et h_tank_m optimisé
        for _ in range(n_random):
            diams = []
            for i in range(nb_conduites):
                if i in self.pipe_diameter_ranges and random.random() < 0.7:
                    # 70% du temps, utiliser la plage adaptative
                    local_candidates = self.pipe_diameter_ranges[i]
                    chosen = random.choice(local_candidates)
                else:
                    # 30% du temps, exploration complète
                    chosen = random.choice(candidate_diams)
                diams.append(int(chosen))
                
            h_min = float(self.h_bounds.get("min", 0.0))
            h_max = float(self.h_bounds.get("max", 50.0))
            
            # Stratégie mixte pour h_tank_m : exploration équilibrée
            if random.random() < 0.5:
                # 50% de chance d'utiliser des hauteurs élevées
                h_val = random.uniform(h_min + (h_max - h_min) * 0.5, h_max - (h_max - h_min) * 0.1)
            else:
                # 50% de chance d'explorer toute la gamme
                h_val = random.uniform(h_min + (h_max - h_min) * 0.1, h_max - (h_max - h_min) * 0.1)
            
            ind = Individu(diametres=diams, h_tank_m=float(h_val))
            self.population.append(ind)
            
        self._log_ga(f"AGAMO: Initialized population with {n_heur} heuristic + {n_random} random individuals")

    # -------------- AGAMO: Réparation Guidée par Contraintes ----------------
    def _repair_velocity_violations(self, individu: Individu, sim_result: Dict[str, Any]) -> Tuple[Individu, Dict[str, Any]]:
        """
        AGAMO: Réparation intelligente des violations de vitesse avec stratégie adaptative et contrôle des coûts.
        """
        v_max_req = float(getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "vitesse_max_m_s", self.velocity_max_default))
        vmax_obs = float(sim_result.get("max_velocity_m_s", 0.0) or 0.0)
        
        if vmax_obs <= v_max_req:
            return individu, sim_result
            
        # Calculer la sévérité de la violation
        violation_ratio = vmax_obs / v_max_req if v_max_req > 0 else 1.0
        candidate_diams = [int(d.diametre_mm) for d in self.diam_candidats]
        repaired = False
        
        # PHASE 2: Stratégie adaptative améliorée avec contrôle des coûts
        if violation_ratio > 1.8:  # Réduit de 2.0 à 1.8
            # Violation sévère (>1.8x) : augmentation modérée
            repair_strategy = "moderate_severe"
            diam_threshold = len(candidate_diams) // 3  # Tiers inférieur
            step_size = 1  # Réduit de 2 à 1 palier max
        elif violation_ratio > 1.3:  # Réduit de 1.5 à 1.3
            # Violation modérée (1.3-1.8x) : augmentation fine
            repair_strategy = "fine_moderate"
            diam_threshold = len(candidate_diams) // 4  # Quart inférieur
            step_size = 1  # 1 palier max
        else:
            # Violation légère (<1.3x) : augmentation très fine
            repair_strategy = "very_fine"
            diam_threshold = len(candidate_diams) // 6  # Sixième inférieur
            step_size = 1  # 1 palier max
        
        current_diams = individu.diametres.copy()
        repairs_made = 0
        
        # PHASE 2: Vérification du coût avant réparation
        try:
            from ..optimizer.scoring import CostScorer
            scorer = CostScorer()
            current_cost = scorer.compute_capex(self.network, {f"link_{i}": d for i, d in enumerate(current_diams)})
            
            # Vérifier la contrainte budgétaire
            budget_max = getattr(getattr(self.constraint_manager, "contraintes_budget", {}), "cout_max_fcfa", float("inf"))
            if current_cost >= budget_max * 0.8:  # Si déjà à 80% du budget
                self._log_ga(f"AGAMO: Skipping repair - cost already at {current_cost:.0f} FCFA (80% of budget)")
                return individu, sim_result
        except Exception as e:
            self._log_ga(f"AGAMO: Warning - could not check cost constraint: {e}")
        
        # Réparation intelligente : cibler les conduites les plus problématiques
        for i, current_diam in enumerate(current_diams):
            diam_idx = candidate_diams.index(current_diam) if current_diam in candidate_diams else -1
            if diam_idx >= 0 and diam_idx < diam_threshold:
                # Augmenter le diamètre selon la stratégie (max 1 palier)
                new_diam = current_diam
                next_diam = _get_next_candidate(new_diam, candidate_diams, direction=1)
                if next_diam != new_diam:
                    new_diam = next_diam
                    
                    # PHASE 2: Vérification du coût après augmentation
                    if hasattr(self, 'network'):
                        try:
                            test_diams = current_diams.copy()
                            test_diams[i] = new_diam
                            test_cost = scorer.compute_capex(self.network, {f"link_{j}": d for j, d in enumerate(test_diams)})
                            
                            # Si l'augmentation dépasse le budget, ne pas réparer
                            if test_cost > budget_max:
                                self._log_ga(f"AGAMO: Skipping repair for link {i} - would exceed budget")
                                continue
                        except Exception:
                            pass  # Continuer si la vérification échoue
                    
                    current_diams[i] = new_diam
                    self.repair_history[i] += 1
                    repairs_made += 1
                    repaired = True
                    
                    # PHASE 2: Limitation plus stricte des réparations
                    if repairs_made >= max(2, len(current_diams) // 15):  # Réduit de 3 à 2 et de 10 à 15
                        self._log_ga(f"AGAMO: Repair limit reached ({repairs_made}) to control costs")
                        break
        
        if repaired:
            individu.diametres = current_diams
            # Re-simuler avec les diamètres réparés
            new_sim = self._simulate_or_approx(individu, None)
            
            # Vérifier si la réparation a amélioré la situation
            new_vmax = float(new_sim.get("max_velocity_m_s", 0.0) or 0.0)
            if new_vmax < vmax_obs:
                self._log_ga(f"AGAMO: Velocity repair successful - {vmax_obs:.2f}m/s → {new_vmax:.2f}m/s (strategy: {repair_strategy})")
            else:
                self._log_ga(f"AGAMO: Velocity repair limited effect - {vmax_obs:.2f}m/s → {new_vmax:.2f}m/s")
            
            return individu, new_sim
            
        return individu, sim_result

    def _repair_if_needed(self, individu: Individu, sim_result: Dict[str, Any]) -> Tuple[Individu, Dict[str, Any]]:
        """
        AGAMO: Réparation complète guidée par contraintes avec optimisation de h_tank_m.
        """
        # Réparation vitesse
        individu, sim_result = self._repair_velocity_violations(individu, sim_result)
        
        # Réparation pression avec optimisation intelligente de h_tank_m
        p_min = float(sim_result.get("min_pressure_m", 0.0) or 0.0)
        p_req = float(getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "pression_min_mce", self.pressure_default_min))
        
        if p_min >= p_req or getattr(individu, "h_tank_m", None) is None:
            return individu, sim_result

        # Stratégie de réparation intelligente : optimisation binaire de h_tank_m
        h_min = float(self.h_bounds.get("min", 0.0))
        h_max = float(self.h_bounds.get("max", 50.0))
        h_current = float(individu.h_tank_m)
        
        # Recherche binaire pour trouver la hauteur optimale
        left = h_current
        right = h_max
        best_h = h_current
        best_p = p_min
        attempts = 0
        max_attempts = 8
        
        while left <= right and attempts < max_attempts:
            mid = (left + right) / 2.0
            individu.h_tank_m = float(mid)
            
            # Simuler avec la nouvelle hauteur
            test_sim = self._simulate_or_approx(individu, None)
            test_p = float(test_sim.get("min_pressure_m", 0.0) or 0.0)
            
            if test_p >= p_req:
                # Cette hauteur satisfait la contrainte de pression
                best_h = mid
                best_p = test_p
                right = mid - 0.5  # Chercher une hauteur plus basse
            else:
                # Cette hauteur ne satisfait pas la contrainte
                left = mid + 0.5  # Chercher une hauteur plus haute
            
            attempts += 1
        
        # Appliquer la meilleure hauteur trouvée
        individu.h_tank_m = float(best_h)
        
        # Re-simuler avec la hauteur optimisée
        final_sim = self._simulate_or_approx(individu, None)
        
        self._log_ga(f"AGAMO: h_tank repair - {h_current:.2f}m → {best_h:.2f}m, pressure: {p_min:.2f}m → {best_p:.2f}m")
        
        return individu, final_sim

    # -------------- AGAMO: Pénalités Adaptatives ----------------
    def _update_adaptive_penalties(self, generation: int) -> None:
        """Met à jour les poids des pénalités selon la phase et l'historique."""
        if not self.feasibility_found and generation > 10:
            # Augmenter les pénalités si aucune solution faisable trouvée
            for key in self.adaptive_penalty_weights:
                self.adaptive_penalty_weights[key] *= 1.1
                
        elif self.feasibility_found and generation > 20:
            # Réduire les pénalités si faisabilité atteinte
            for key in self.adaptive_penalty_weights:
                self.adaptive_penalty_weights[key] *= 0.95
                
        # Limiter les poids
        for key in self.adaptive_penalty_weights:
            self.adaptive_penalty_weights[key] = max(0.1, min(10.0, self.adaptive_penalty_weights[key]))

    def _calculate_adaptive_penalties(self, individu: Individu, sim_result: Dict[str, Any]) -> float:
        """Calcule les pénalités avec poids adaptatifs - Version corrigée avec pénalités linéaires intelligentes."""
        penal = 0.0
        
        if not sim_result.get("success"):
            penal += 1e6  # Pénalité forte pour échec de simulation
            return penal
            
        # Pénalités de pression - LINÉAIRES et PROPORTIONNELLES au coût
        p_req = float(getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "pression_min_mce", self.pressure_default_min))
        p_min = float(sim_result.get("min_pressure_m", 0.0) or 0.0)
        if p_min < p_req:
            weight = self.adaptive_penalty_weights["pressure"]
            # Pénalité linéaire : 10% du coût par mètre de déficit de pression
            deficit = p_req - p_min
            penal += weight * 0.1 * deficit * 1000  # 1000 FCFA par mètre de déficit
            self.constraint_violation_history["pressure"] += 1
            
        # Pénalités de vitesse - LINÉAIRES et PROPORTIONNELLES
        v_max_req = float(getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "vitesse_max_m_s", self.velocity_max_default))
        v_min_req = float(getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "vitesse_min_m_s", self.velocity_min_default))
        vmax_obs = float(sim_result.get("max_velocity_m_s", 0.0) or 0.0)
        vmin_obs = float(sim_result.get("min_velocity_m_s", 0.0) or 0.0)
        
        if vmax_obs > v_max_req:
            weight = self.adaptive_penalty_weights["velocity_max"]
            # Pénalité linéaire : 5% du coût par m/s d'excès
            excess = vmax_obs - v_max_req
            penal += weight * 0.05 * excess * 1000  # 1000 FCFA par m/s d'excès
            self.constraint_violation_history["velocity_max"] += 1
            
        if vmin_obs < v_min_req:
            weight = self.adaptive_penalty_weights["velocity_min"]
            # Pénalité linéaire : 3% du coût par m/s de déficit
            deficit = v_min_req - vmin_obs
            penal += weight * 0.03 * deficit * 1000  # 1000 FCFA par m/s de déficit
            self.constraint_violation_history["velocity_min"] += 1

        # Pénalité d'uniformité - RÉDUITE et linéaire
        try:
            counts = Counter(int(d) for d in individu.diametres)
            total_pipes = max(1, len(individu.diametres))
            max_ratio = max(counts.values()) / float(total_pipes)
            
            # Seuil adaptatif selon la phase
            uniformity_threshold = 0.5 if self.current_phase == 1 else 0.4
            
            if max_ratio > uniformity_threshold:
                weight = self.adaptive_penalty_weights["uniformity"]
                # Pénalité linéaire : 2% du coût par excès d'uniformité
                excess = max_ratio - uniformity_threshold
                penal += weight * 0.02 * excess * 1000  # 1000 FCFA par excès d'uniformité
        except Exception:
            pass

        return penal

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
            else:
                # DEBUG: Log pourquoi le mapping échoue
                try:
                    self._log_ga(f"DEBUG: Mapping failed - pipe_ids_len={len(self.pipe_ids) if self.pipe_ids else 0}, diams_len={len(individu.diametres)}")
                except Exception:
                    pass
            # H_tank map heuristic
                h_map = {}
            if getattr(individu, "h_tank_m", None) is not None:
                # if tank IDs unknown, the wrapper will interpret/assign as appropriate
                    h_map = {"tank1": float(individu.h_tank_m)}
            # Log: ce que le GA envoie réellement au simulateur (échantillon)
            try:
                from pathlib import Path as _P
                from datetime import datetime as _dt
                import os as _os
                _proj = None
                for _p in _P(__file__).resolve().parents:
                    if (_p / "test_validation").exists():
                        _proj = _p
                        break
                if _proj is None:
                    _proj = _P.cwd()
                _ld = _proj / "test_validation" / "logs"
                _ld.mkdir(parents=True, exist_ok=True)
                _out = _ld / "ga_to_solver_debug.log"
                sample = list(diam_map.items())[:10]
                with open(_out, "a", encoding="utf-8", buffering=1) as gf:
                    gf.write(f"[{_dt.now().isoformat()}] pid={_os.getpid()} send {len(diam_map)} diams | sample="
                             f"{[(k, v) for k, v in sample]}\n")
            except Exception:
                pass
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
        """Calculate CAPEX using real pipe lengths and DB prices when available.

        Strategy:
        - If a network file is available, load the unified model and compute CAPEX
          via CostScorer using a map of link_id -> diameter_mm.
        - Else, fall back to reseau_data["conduites"] lengths if provided.
        - As last resort, use a crude estimate.
        """
        # Try to use the robust scorer on the unified network model
        try:
            if self.network_path:
                from ..io import load_yaml_or_inp  # type: ignore
                from ..optimizer.scoring import CostScorer  # type: ignore

                model, _meta = load_yaml_or_inp(Path(self.network_path))
                # Build diameter map per link id
                diam_map: Dict[str, int] = {}
                if self.pipe_ids and len(self.pipe_ids) == len(individu.diametres):
                    diam_map = {self.pipe_ids[i]: int(individu.diametres[i]) for i in range(len(individu.diametres))}
                else:
                    # Fallback: iterate links in deterministic order and zip
                    links_items = list((getattr(model, "links", None) or {}).items())
                    for idx, (lid, _ldata) in enumerate(links_items[: len(individu.diametres)]):
                        diam_map[lid] = int(individu.diametres[idx])

                scorer = CostScorer()
                capex = scorer.compute_capex(model, diam_map)
                # If CAPEX looks valid, return it
                if capex and capex > 0:
                    return float(capex)
        except Exception:
            # Fall back to lightweight computation below
            pass

        # Lightweight fallback using available lengths (reseau_data)
        total_cost = 0.0
        if reseau_data and "conduites" in reseau_data:
            for i, d in enumerate(individu.diametres):
                # Prefer unit cost from candidates when provided
                unit_cost = None
                for c in self.diam_candidats:
                    if int(c.diametre_mm) == int(d):
                        unit_cost = getattr(c, "cout_fcfa_m", None)
                        break
                if unit_cost is None:
                    # very rough fallback
                    unit_cost = (d ** 2) * 0.01
                length = float(reseau_data["conduites"][i].get("longueur_m", 1.0)) if i < len(reseau_data["conduites"]) else 1.0
                total_cost += float(unit_cost) * float(length)
            return float(total_cost)

        # Final crude estimate if nothing else available
        total = 0.0
        for d in individu.diametres:
            total += (d ** 2) * 0.01 * 1.0
        return float(total)

    def _evaluate_individual(self, args: Tuple[int, int, Individu, Optional[Dict], int]) -> Tuple[int, Individu, float, Dict[str, Any]]:
        """Worker-friendly evaluation: args=(generation, idx1, individu, reseau_data, pop_size) -> (idx1, individu, fitness, sim_result)"""
        generation, idx1, individu, reseau_data, pop_size = args
        
        # AGAMO: Mise à jour des pénalités adaptatives
        self._update_adaptive_penalties(generation)
        
        # Journaliser le chromosome: conversion diamètres -> indices par rapport aux candidats
        try:
            cand_list = [int(d.diametre_mm) for d in self.diam_candidats]
            indices = []
            invalid_positions: List[int] = []
            for pos, d in enumerate(individu.diametres):
                try:
                    idx = cand_list.index(int(d))
                except ValueError:
                    idx = -1
                    invalid_positions.append(pos)
                indices.append(idx)
            invalid_count = len(invalid_positions)
            sample_details = []
            # échantillon de paires conduite→(idx->diam)
            n_show = min(10, len(indices))
            for k in range(n_show):
                pipe_id = self.pipe_ids[k] if self.pipe_ids and k < len(self.pipe_ids) else f"C{k+1}"
                idx = indices[k]
                dmm = individu.diametres[k]
                sample_details.append(f"pipe[{pipe_id}]: idx={idx} diam={dmm}mm")
            self._log_ga(
                line=(
                    f"generation={generation} ind={idx1} genes={len(indices)} invalid_indices={invalid_count} "
                    f"h_tank={getattr(individu, 'h_tank_m', None)}"
                ),
                details=sample_details + ([f"invalid_positions={invalid_positions[:50]}"] if invalid_count else [])
            )
        except Exception:
            pass
        try:
            self._emit("sim_start", {"generation": generation, "index": idx1, "population_size": pop_size})
        except Exception:
            pass
        sim = self._simulate_or_approx(individu, reseau_data)
        try:
            self._emit("sim_done", {"generation": generation, "index": idx1, "population_size": pop_size, "success": bool(sim.get("success", False))})
        except Exception:
            pass
        
        # AGAMO: Réparation guidée par contraintes
        if sim.get("success"):
            individu, sim = self._repair_if_needed(individu, sim)

        # cost
        cost = self._calculate_cost(individu, reseau_data)
        
        # PHASE 2: Nouvelle logique de pénalités adaptatives non linéaires
        if sim.get("success"):
            # Utiliser la classe ConstraintPenaltyCalculator existante
            from ..optimizer.constraints_handler import ConstraintPenaltyCalculator
            
            # Créer une instance du calculateur de pénalités
            penalty_calculator = ConstraintPenaltyCalculator()
            
            # 1. Normaliser les violations
            constraints = {
                "pressure_min_m": getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "pression_min_mce", self.pressure_default_min),
                "velocity_max_m_s": getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "vitesse_max_m_s", self.velocity_max_default)
            }
            violation_info = penalty_calculator.normalize_violations(sim, constraints)
            
            # 2. Calculer la pénalité adaptative
            penalty_info = penalty_calculator.adaptive_penalty(
                violation_total=violation_info["total"],
                generation=generation,
                total_generations=self.generations,
                alpha_start=getattr(self.config, "penalty_alpha_start", 1e5),
                alpha_max=getattr(self.config, "penalty_alpha_max", 1e8),
                beta=getattr(self.config, "penalty_beta", 1.8)
            )
            
            penal = penalty_info["value"]
            
            # 3. Stocker les métriques détaillées pour l'analyse
            individu.metrics = getattr(individu, "metrics", {})
            individu.metrics["violations"] = violation_info
            individu.metrics["penalty"] = penalty_info
            individu.is_feasible = violation_info["total"] <= 1e-6
            
            # Marquer si faisabilité trouvée
            if penal == 0.0:
                self.feasibility_found = True
        else:
            # Échec de simulation: pénalité forte
            penal = 1e6
            individu.is_feasible = False

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
        
        # Logique intelligente pour constraints_ok : tolérance technique
        # Une solution est "OK" si les violations sont minimes (< 5% des contraintes)
        if penal == 0.0:
            individu.constraints_ok = True
        else:
            # Calculer le pourcentage de violation par rapport au coût total
            violation_ratio = penal / (cost + penal) if (cost + penal) > 0 else 1.0
            # Tolérance de 5% : si les violations représentent moins de 5% du coût total
            individu.constraints_ok = (violation_ratio < 0.05)
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

    # ---------------- AGAMO: Opérateurs Génétiques Biaisés ----------------
    def _biased_mutation(self, individu: Individu, generation: int) -> Individu:
        """Mutation biaisée équilibrée avec contrôle des coûts et de la faisabilité."""
        candidate_diams = [int(d.diametre_mm) for d in self.diam_candidats]
        if not candidate_diams:
            return individu
            
        mutated = Individu(diametres=individu.diametres.copy(), h_tank_m=getattr(individu, "h_tank_m", None))
        
        # PHASE 2: Taux de mutation adaptatif amélioré
        mutation_rate = self.mutation_rate_base
        if not self.feasibility_found and generation > 10:
            mutation_rate *= 1.3  # Réduit de 1.5 à 1.3
        elif self.feasibility_found:
            mutation_rate *= 0.7  # Réduit de 0.8 à 0.7 pour plus de stabilité
            
        # PHASE 2: Vérification du coût avant mutation
        try:
            from ..optimizer.scoring import CostScorer
            scorer = CostScorer()
            current_cost = scorer.compute_capex(self.network, {f"link_{i}": d for i, d in enumerate(mutated.diametres)})
            budget_max = getattr(getattr(self.constraint_manager, "contraintes_budget", {}), "cout_max_fcfa", float("inf"))
            cost_ratio = current_cost / budget_max if budget_max > 0 else 0.0
        except Exception:
            cost_ratio = 0.0
            
        for i in range(len(mutated.diametres)):
            if random.random() < mutation_rate:
                current_diam = mutated.diametres[i]
                
                # PHASE 2: Biais équilibré basé sur la faisabilité et le coût
                bias = self.pipe_repair_bias.get(i, 0.0)
                
                if bias > 0.6:  # Si réparée plus de 60% du temps (augmenté de 0.5 à 0.6)
                    # PHASE 2: Stratégie équilibrée au lieu de 70% vers le haut
                    if cost_ratio > 0.7:  # Si déjà coûteux
                        # 40% d'augmentation, 30% de diminution, 30% de remplacement aléatoire
                        rand_val = random.random()
                        if rand_val < 0.4:
                            new_diam = _get_next_candidate(current_diam, candidate_diams, direction=1)
                        elif rand_val < 0.7:
                            new_diam = _get_next_candidate(current_diam, candidate_diams, direction=-1)
                        else:
                            new_diam = random.choice(candidate_diams)
                    else:
                        # 50% d'augmentation, 25% de diminution, 25% de remplacement aléatoire
                        rand_val = random.random()
                        if rand_val < 0.5:
                            new_diam = _get_next_candidate(current_diam, candidate_diams, direction=1)
                        elif rand_val < 0.75:
                            new_diam = _get_next_candidate(current_diam, candidate_diams, direction=-1)
                        else:
                            new_diam = random.choice(candidate_diams)
                elif bias > 0.3:  # Si réparée modérément (30-60%)
                    # 40% d'augmentation, 30% de diminution, 30% de remplacement aléatoire
                    rand_val = random.random()
                    if rand_val < 0.4:
                        new_diam = _get_next_candidate(current_diam, candidate_diams, direction=1)
                    elif rand_val < 0.7:
                        new_diam = _get_next_candidate(current_diam, candidate_diams, direction=-1)
                    else:
                        new_diam = random.choice(candidate_diams)
                else:
                    # Mutation normale pour les conduites peu réparées
                    new_diam = random.choice(candidate_diams)
                    
                mutated.diametres[i] = new_diam
                
        # Mutation h_tank avec stratégie intelligente
        if random.random() < mutation_rate and getattr(mutated, "h_tank_m", None) is not None:
            h_min = float(self.h_bounds.get("min", 0.0))
            h_max = float(self.h_bounds.get("max", 50.0))
            h_current = float(mutated.h_tank_m)
            
            # Stratégie de mutation adaptative pour h_tank_m
            h_range = h_max - h_min
            if not self.feasibility_found:
                # Si pas de faisabilité trouvée, favoriser les hauteurs élevées
                if random.random() < 0.7:
                    # 70% de chance d'augmenter la hauteur
                    h_delta = random.uniform(0.5, h_range * 0.2)
                    mutated.h_tank_m = max(h_min, min(h_max, h_current + h_delta))
                else:
                    # 30% de chance de mutation normale
                    h_delta = random.uniform(-h_range * 0.15, h_range * 0.15)
                    mutated.h_tank_m = max(h_min, min(h_max, h_current + h_delta))
            else:
                # Si faisabilité trouvée, mutation fine pour optimisation
                h_delta = random.uniform(-h_range * 0.05, h_range * 0.05)
                mutated.h_tank_m = max(h_min, min(h_max, h_current + h_delta))
            
        return mutated

    def _uniform_crossover(self, p1: Individu, p2: Individu) -> Tuple[Individu, Individu]:
        """Uniform crossover per gene (diamètre and h_tank) avec stratégie intelligente."""
        n = len(p1.diametres)
        child1 = Individu(diametres=p1.diametres.copy(), h_tank_m=getattr(p1, "h_tank_m", None))
        child2 = Individu(diametres=p2.diametres.copy(), h_tank_m=getattr(p2, "h_tank_m", None))
        
        # Crossover des diamètres
        for i in range(n):
            if random.random() < 0.5:
                child1.diametres[i], child2.diametres[i] = child2.diametres[i], child1.diametres[i]
        
        # Crossover h_tank_m avec stratégie intelligente
        if hasattr(p1, "h_tank_m") and hasattr(p2, "h_tank_m") and random.random() < 0.5:
            h1 = float(p1.h_tank_m)
            h2 = float(p2.h_tank_m)
            
            # Stratégie : favoriser la hauteur la plus élevée (plus de pression disponible)
            if h1 > h2:
                # Parent 1 a une hauteur plus élevée
                child1.h_tank_m = float(h1)  # Garder la meilleure
                child2.h_tank_m = float((h1 + h2) / 2.0)  # Moyenne
            else:
                # Parent 2 a une hauteur plus élevée
                child1.h_tank_m = float((h1 + h2) / 2.0)  # Moyenne
                child2.h_tank_m = float(h2)  # Garder la meilleure
            
            # Ajouter une petite variation pour maintenir la diversité
            h_min = float(self.h_bounds.get("min", 0.0))
            h_max = float(self.h_bounds.get("max", 50.0))
            variation = random.uniform(-1.0, 1.0)
            
            child1.h_tank_m = max(h_min, min(h_max, child1.h_tank_m + variation))
            child2.h_tank_m = max(h_min, min(h_max, child2.h_tank_m + variation))
        
        return child1, child2

    # ---------------- AGAMO: Sélection et Gestion des Phases ----------------
    def _tournament_selection(self, population: List[Individu], tournament_size: int = 3) -> Individu:
        """Sélection par tournoi avec biais vers les meilleurs."""
        if not population:
            raise ValueError("Population vide pour la sélection")
        
        # Sélection aléatoire de candidats
        candidates = random.sample(population, min(tournament_size, len(population)))
        
        # Tri par fitness (plus élevé = meilleur)
        candidates.sort(key=lambda x: getattr(x, 'fitness', 0.0), reverse=True)
        
        # Biais vers les meilleurs (70% de chance pour le meilleur)
        if random.random() < 0.7:
            return candidates[0]
        else:
            return random.choice(candidates)

    def _update_phase(self, generation: int) -> None:
        """Met à jour la phase d'optimisation selon la progression."""
        if generation < self.generations // 3:
            self.current_phase = 1  # Exploration
        elif generation < 2 * self.generations // 3:
            self.current_phase = 2  # Exploitation
        else:
            self.current_phase = 3  # Raffinement
            
        # Transition de phase avec ajustements
        if self.current_phase == 2 and not self.feasibility_found:
            # Si pas de faisabilité en phase 2, augmenter les pénalités
            for key in self.adaptive_penalty_weights:
                self.adaptive_penalty_weights[key] *= 1.5
                
        self._log_ga(f"AGAMO: Phase {self.current_phase} at generation {generation}")

    def _apply_soft_repair(self, population: List[Individu], candidate_diameters: List[int]):
        """
        Applique la réparation douce aux meilleurs individus infaisables de la population.
        """
        # Paramètres de la réparation (à rendre configurables)
        repair_top_k = getattr(self.config.algorithme, "repair_top_k", 3)
        repair_max_cost_increase_ratio = getattr(self.config.algorithme, "repair_max_cost_increase_ratio", 1.10) # 10% de surcoût max

        # 1. Identifier les candidats à la réparation
        infeasible_individuals = [ind for ind in population if not getattr(ind, 'is_feasible', True)]
        if not infeasible_individuals:
            return # Rien à faire

        # Trier les infaisables par leur score (le moins mauvais d'abord)
        infeasible_individuals.sort(key=lambda ind: getattr(ind, 'fitness', 0.0), reverse=True)
        
        # Ne garder que les K meilleurs
        candidates_for_repair = infeasible_individuals[:repair_top_k]

        for individual in candidates_for_repair:
            self._log_ga(f"Tentative de réparation douce sur l'individu avec score={getattr(individual, 'fitness', 0.0):.2f}...")
            
            # 2. Tenter la réparation
            # Convertir les diamètres en dictionnaire pour la fonction de réparation
            diameters_map = {}
            if self.pipe_ids and len(self.pipe_ids) == len(individual.diametres):
                diameters_map = {self.pipe_ids[i]: d for i, d in enumerate(individual.diametres)}
            else:
                # Fallback: utiliser des clés numériques
                diameters_map = {f"pipe_{i}": d for i, d in enumerate(individual.diametres)}
            
            repaired_diam_map, changes = soft_repair_solution(
                diameters_map,
                getattr(individual, 'sim_result', {}),
                candidate_diameters
            )

            if changes["total_changes"] == 0:
                continue # La réparation n'a rien pu faire

            # 3. Évaluer la solution réparée
            # Convertir le dictionnaire réparé en liste de diamètres
            repaired_diameters = []
            if self.pipe_ids and len(self.pipe_ids) == len(individual.diametres):
                for pipe_id in self.pipe_ids:
                    repaired_diameters.append(repaired_diam_map.get(pipe_id, individual.diametres[0]))
            else:
                # Fallback: utiliser l'ordre original
                for i in range(len(individual.diametres)):
                    pipe_key = f"pipe_{i}"
                    repaired_diameters.append(repaired_diam_map.get(pipe_key, individual.diametres[i]))
            
            # Créer un nouvel individu avec les diamètres réparés
            repaired_individual = Individu(
                diametres=repaired_diameters,
                h_tank_m=getattr(individual, 'h_tank_m', None)
            )
            
            # Calculer le coût de la solution réparée
            try:
                from ..optimizer.scoring import CostScorer
                scorer = CostScorer()
                repaired_capex = scorer.compute_capex(self.network, repaired_diam_map)
                current_capex = getattr(individual, 'cout_total', 0.0)
                
                # Condition d'acceptation de coût
                if repaired_capex > current_capex * repair_max_cost_increase_ratio:
                    self._log_ga(f"Réparation rejetée: le coût a trop augmenté ({current_capex:.0f} -> {repaired_capex:.0f}).")
                    continue
            except Exception as e:
                self._log_ga(f"Impossible de vérifier le coût de réparation: {e}")
                continue
                
            # Resimuler la solution réparée pour voir si elle est meilleure
            repaired_sim = self._simulate_or_approx(repaired_individual, None)
            
            if not repaired_sim.get("success"):
                self._log_ga("Réparation rejetée: la simulation a échoué.")
                continue
            
            # Normaliser les violations pour comparer
            try:
                from ..optimizer.constraints_handler import ConstraintPenaltyCalculator
                penalty_calculator = ConstraintPenaltyCalculator()
                
                constraints = {
                    "pressure_min_m": getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "pression_min_mce", self.pressure_default_min),
                    "velocity_max_m_s": getattr(getattr(self.constraint_manager, "contraintes_techniques", {}), "vitesse_max_m_s", self.velocity_max_default)
                }
                
                original_violations = penalty_calculator.normalize_violations(
                    getattr(individual, 'sim_result', {}), constraints
                )
                repaired_violations = penalty_calculator.normalize_violations(repaired_sim, constraints)
                
                # Condition d'acceptation de performance
                if repaired_violations["total"] < original_violations["total"]:
                    self._log_ga(
                        f"Réparation ACCEPTÉE sur individu. Violation réduite: "
                        f"{original_violations['total']:.4f} -> {repaired_violations['total']:.4f}. "
                        f"Coût: {repaired_capex:,.0f} FCFA."
                    )
                    # Remplacer l'individu original par sa version réparée
                    individual.diametres = repaired_diameters
                    individual.sim_result = repaired_sim
                    individual.cout_total = repaired_capex
                    # Ré-évaluer complètement l'individu réparé
                    self._evaluate_individual((0, 0, individual, None, len(population)))
                else:
                    self._log_ga("Réparation rejetée: la violation n'a pas diminué.")
            except Exception as e:
                self._log_ga(f"Erreur lors de la comparaison des violations: {e}")

    def _check_stagnation(self, generation: int) -> bool:
        """Vérifie si l'optimisation stagne et déclenche des actions correctives."""
        if len(self.best_cost_history) < 10:
            return False
            
        recent_costs = self.best_cost_history[-10:]
        improvement = recent_costs[0] - recent_costs[-1]
        
        if improvement < 1e-6:  # Pas d'amélioration significative
            self.stagnation_counter += 1
            if self.stagnation_counter > 5:
                self._log_ga(f"AGAMO: Stagnation detected at generation {generation}")
                return True
        else:
            self.stagnation_counter = 0
            
        return False

    def _restart_population_partially(self, reseau_data: Optional[Dict]) -> None:
        """Redémarre partiellement la population pour échapper à la stagnation."""
        if not self.population:
            return
            
        # Garder les 20% meilleurs
        n_keep = max(1, int(self.population_size * 0.2))
        self.population.sort(key=lambda x: getattr(x, 'fitness', 0.0), reverse=True)
        kept = self.population[:n_keep]
        
        # Régénérer le reste avec plus de diversité
        n_new = self.population_size - n_keep
        new_individuals = []
        
        for _ in range(n_new):
            # 50% heuristique, 50% aléatoire avec exploration étendue
            if random.random() < 0.5:
                # Heuristique avec plages élargies
                diams = []
                for i in range(len(self.pipe_ids) if self.pipe_ids else 100):
                    if i in self.pipe_diameter_ranges:
                        # Élargir la plage
                        local_cands = self.pipe_diameter_ranges[i]
                        candidate_diams = [int(d.diametre_mm) for d in self.diam_candidats]
                        if local_cands:
                            # Ajouter des candidats voisins
                            min_local = min(local_cands)
                            max_local = max(local_cands)
                            min_idx = candidate_diams.index(min_local) if min_local in candidate_diams else 0
                            max_idx = candidate_diams.index(max_local) if max_local in candidate_diams else len(candidate_diams)-1
                            extended_min = max(0, min_idx - 2)
                            extended_max = min(len(candidate_diams), max_idx + 3)
                            extended_cands = candidate_diams[extended_min:extended_max]
                            chosen = random.choice(extended_cands)
                        else:
                            chosen = random.choice(candidate_diams)
                    else:
                        chosen = random.choice([int(d.diametre_mm) for d in self.diam_candidats])
                    diams.append(chosen)
            else:
                # Aléatoire complet
                diams = [random.choice([int(d.diametre_mm) for d in self.diam_candidats]) 
                        for _ in range(len(self.pipe_ids) if self.pipe_ids else 100)]
                
            h_min = float(self.h_bounds.get("min", 0.0))
            h_max = float(self.h_bounds.get("max", 50.0))
            h_val = random.uniform(h_min, h_max)
            new_ind = Individu(diametres=diams, h_tank_m=float(h_val))
            new_individuals.append(new_ind)
            
        self.population = kept + new_individuals
        self.stagnation_counter = 0
        self._log_ga(f"AGAMO: Partial restart - kept {n_keep}, generated {n_new} new individuals")

    # ---------------- Boucle Principale d'Optimisation ----------------
    def optimiser(self, reseau_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        AGAMO: Boucle principale d'optimisation avec phases adaptatives.
        """
        if not self.population:
            raise ValueError("Population non initialisée. Appelez initialiser_population() d'abord.")
            
        nb_conduites = len(self.pipe_ids) if self.pipe_ids else len(self.population[0].diametres)
        
        self._log_ga(f"AGAMO: Starting optimization with {self.population_size} individuals, {self.generations} generations")
        
        # Statistiques de suivi
        best_fitness_history = []
        feasibility_rate_history = []
        
        for generation in range(self.generations):
            # Émission de début de génération
            self._emit("generation_start", {
                "generation": generation + 1,
                "total_generations": self.generations,
                "population_size": self.population_size,
                "phase": self.current_phase
            })
            
            # AGAMO: Mise à jour de phase
            self._update_phase(generation)
            
            # AGAMO: Vérification de stagnation
            if self._check_stagnation(generation):
                self._restart_population_partially(reseau_data)
            
            # Évaluation parallèle de la population
            args_list = [(generation, i, ind, reseau_data, self.population_size) 
                         for i, ind in enumerate(self.population)]
            
            # Émission de début d'évaluation
            self._emit("evaluation_start", {
                "generation": generation + 1,
                "population_size": self.population_size,
                "workers": self.workers
            })
            
            if self.workers > 1:
                with Pool(processes=self.workers) as pool:
                    results = pool.map(self._evaluate_individual, args_list)
            else:
                results = [self._evaluate_individual(args) for args in args_list]
            
            # Émission de fin d'évaluation
            self._emit("evaluation_complete", {
                "generation": generation + 1,
                "evaluated_count": len(results),
                "success_count": sum(1 for r in results if r[3].get("success", False))
            })
            
            # Mise à jour de la population avec les résultats
            for idx, individu, fitness, sim_result in results:
                self.population[idx] = individu
                individu.fitness = fitness
                individu.sim_result = sim_result
                
                # Mise à jour du biais de réparation
                if hasattr(individu, 'diametres'):
                    for i, diam in enumerate(individu.diametres):
                        if i in self.repair_history and self.repair_history[i] > 0:
                            self.pipe_repair_bias[i] = self.repair_history[i] / max(1, generation + 1)
            
            # Tri par fitness
            self.population.sort(key=lambda x: getattr(x, 'fitness', 0.0), reverse=True)
            
            # --- HOOK DE RÉPARATION DOUCE ---
            candidate_diams = [int(d.diametre_mm) for d in self.diam_candidats]
            self._apply_soft_repair(self.population, candidate_diams)
            
            # Mise à jour de la meilleure solution
            if not self.best_solution or getattr(self.population[0], 'fitness', 0.0) > getattr(self.best_solution, 'fitness', 0.0):
                self.best_solution = self.population[0]
                self.generations_without_improvement = 0
            else:
                self.generations_without_improvement += 1
            
            # Historique des coûts
            if self.best_solution:
                cost = self._calculate_cost(self.best_solution, reseau_data)
                self.best_cost_history.append(cost)
                
                # Émission de mise à jour du meilleur coût
                self._emit("best_cost_updated", {
                    "generation": generation + 1,
                    "best_cost": cost,
                    "improvement": self.best_cost_history[-2] - cost if len(self.best_cost_history) > 1 else 0.0
                })
            
            # Statistiques de la génération
            best_fitness = getattr(self.population[0], 'fitness', 0.0)
            best_fitness_history.append(best_fitness)
            
            feasibility_count = sum(1 for ind in self.population if getattr(ind, 'constraints_ok', False))
            feasibility_rate = feasibility_count / len(self.population)
            feasibility_rate_history.append(feasibility_rate)
            
            # Émission de progression globale
            total_progress = (generation + 1) / self.generations
            self._emit("progress_update", {
                "generation": generation + 1,
                "total_generations": self.generations,
                "total_progress": total_progress,
                "best_cost": cost if self.best_solution else None,
                "feasibility_rate": feasibility_rate,
                "phase": self.current_phase
            })
            
            # Log de progression
            if generation % 10 == 0 or generation == self.generations - 1:
                self._log_ga(
                    f"AGAMO: Gen {generation}/{self.generations} - "
                    f"Best fitness: {best_fitness:.6f} - "
                    f"Feasibility rate: {feasibility_rate:.2%} - "
                    f"Phase: {self.current_phase}"
                )
            
            # Callback de progression
            if self.on_generation_callback:
                try:
                    self.on_generation_callback(self.population, generation)
                except Exception as e:
                    self._log_ga(f"Error in generation callback: {e}")
            
            # Émission d'événements
            self._emit("generation_complete", {
                "generation": generation,
                "best_fitness": best_fitness,
                "feasibility_rate": feasibility_rate,
                "phase": self.current_phase
            })
            
            # Génération de la nouvelle population
            new_population = []
            
            # Élitisme (garder les meilleurs)
            n_elite = max(1, int(self.population_size * self.elitism_ratio))
            new_population.extend(self.population[:n_elite])
            
            # Génération des enfants
            while len(new_population) < self.population_size:
                # Sélection des parents
                parent1 = self._tournament_selection(self.population)
                parent2 = self._tournament_selection(self.population)
                
                # Croisement
                if random.random() < self.crossover_rate:
                    child1, child2 = self._uniform_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2
                
                # AGAMO: Mutation biaisée
                child1 = self._biased_mutation(child1, generation)
                child2 = self._biased_mutation(child2, generation)
                
                new_population.extend([child1, child2])
            
            # Ajuster la taille si nécessaire
            self.population = new_population[:self.population_size]
            
            # Historique
            self.history.append({
                "generation": generation,
                "best_fitness": best_fitness,
                "feasibility_rate": feasibility_rate,
                "phase": self.current_phase,
                "stagnation_counter": self.stagnation_counter
            })
        
        # Émission de fin d'optimisation
        self._emit("optimization_complete", {
            "total_generations": self.generations,
            "final_phase": self.current_phase,
            "feasibility_found": self.feasibility_found,
            "total_evaluations": self.generations * self.population_size
        })
        
        # Résultats finaux
        if not self.best_solution:
            self.best_solution = self.population[0]
            
        final_cost = self._calculate_cost(self.best_solution, reseau_data)
        
        # Statistiques finales
        final_stats = {
            "best_fitness_history": best_fitness_history,
            "feasibility_rate_history": feasibility_rate_history,
            "repair_history": dict(self.repair_history),
            "constraint_violation_history": dict(self.constraint_violation_history),
            "adaptive_penalty_weights": self.adaptive_penalty_weights.copy(),
            "final_phase": self.current_phase,
            "feasibility_found": self.feasibility_found
        }
        
        self._log_ga(
            f"AGAMO: Optimization completed - "
            f"Final cost: {final_cost:.2f} - "
            f"Feasibility: {self.feasibility_found} - "
            f"Final phase: {self.current_phase}"
        )
        
        return {
            "success": True,
            "best_solution": self.best_solution,
            "final_cost": final_cost,
                    "generations": self.generations,
            "population_size": self.population_size,
            "history": self.history,
            "stats": final_stats
        }

    # ---------------- Méthodes Utilitaires ----------------
    def get_best_solution(self) -> Optional[Individu]:
        """Retourne la meilleure solution trouvée."""
        return self.best_solution
    
    def get_optimization_history(self) -> List[Dict[str, Any]]:
        """Retourne l'historique complet de l'optimisation."""
        return self.history
    
    def get_population_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques actuelles de la population."""
        if not self.population:
            return {}
            
        fitnesses = [getattr(ind, 'fitness', 0.0) for ind in self.population]
        costs = [getattr(ind, 'cout_total', 0.0) for ind in self.population]
        feasibility_count = sum(1 for ind in self.population if getattr(ind, 'constraints_ok', False))
        
        return {
            "population_size": len(self.population),
            "best_fitness": max(fitnesses) if fitnesses else 0.0,
            "avg_fitness": sum(fitnesses) / len(fitnesses) if fitnesses else 0.0,
            "best_cost": min(costs) if costs else 0.0,
            "avg_cost": sum(costs) / len(costs) if costs else 0.0,
            "feasibility_rate": feasibility_count / len(self.population),
            "current_phase": self.current_phase,
            "feasibility_found": self.feasibility_found
        }
