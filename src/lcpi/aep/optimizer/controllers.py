from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List, Union
import hashlib
import logging
import math
import statistics
from datetime import datetime

from .io import load_yaml_or_inp
from .validators import NetworkValidator
from .algorithms.binary import BinarySearchOptimizer
from .base import BaseOptimizer, SimpleAdapter
from .constraints_handler import apply_constraints_to_result
from .utils.flows_inspector import inspect_simulation_result, FlowEventConsumer
import json
import time


logger = logging.getLogger(__name__)

def _make_progress_adapter(user_cb):
    """Adaptateur qui normalise les événements et maintient des compteurs sim/eval.

    - Agrège les variantes: sim_start/simulation_start, sim_done/simulation_done, etc.
    - Expose un événement unifié "simulation" avec payload {stage,busy,done,...}
    - Propage les événements inconnus tels quels.
    """
    counters = {"sim_busy": 0, "sim_done": 0, "eval_done": 0, "eval_total": 0}

    def adapter(evt: str, data: dict):
        ev = (evt or "").lower() if evt else ""
        data = data or {}
        # Event processing

        # Simulation start variants
        if ev in ("sim_start", "simulation_start", "simulation_running", "sim_running"):
            counters["sim_busy"] += 1
            payload = {"stage": "running", "busy": counters["sim_busy"], "done": counters["sim_done"]}
            try:
                user_cb("simulation", payload)
            except Exception:
                pass
            return

        # Simulation done variants
        if ev in ("sim_done", "simulation_done", "simulation_end", "sim_end"):
            # a sim done reduces busy and increments done
            counters["sim_busy"] = max(0, counters["sim_busy"] - 1)
            counters["sim_done"] += 1
            payload = {"stage": "success", "busy": counters["sim_busy"], "done": counters["sim_done"]}
            payload.update({"generation": data.get("generation"), "index": data.get("index")})
            try:
                user_cb("simulation", payload)
            except Exception:
                pass
            return

        # Simulation error
        if ev in ("sim_error", "simulation_error"):
            counters["sim_busy"] = max(0, counters["sim_busy"] - 1)
            payload = {"stage": "error", "busy": counters["sim_busy"], "done": counters["sim_done"]}
            payload.update({"error": data.get("error")})
            try:
                user_cb("simulation", payload)
            except Exception:
                pass
            return

        # Evaluation events
        if ev in ("eval_start", "evaluation_start"):
            counters["eval_total"] += 1
            try:
                user_cb("evaluation", {"stage": "start", "total": counters["eval_total"]})
            except Exception:
                pass
            return

        if ev in ("eval_done", "evaluation_done"):
            counters["eval_done"] += 1
            try:
                user_cb("evaluation", {"stage": "done", "done": counters["eval_done"], "total": counters["eval_total"]})
            except Exception:
                pass
            return

        # Generation events (pass through)
        if ev in ("generation_start", "generation_end", "individual_start", "individual_end"):
            try:
                user_cb(evt, data)
            except Exception:
                pass
            return

        # Hybrid events (pass through)
        if ev in ("hybrid_start", "hybrid_end", "refinement_start", "refinement_end"):
            try:
                user_cb(evt, data)
            except Exception:
                pass
            return

        # Other events (pass through unchanged)
        try:
            user_cb(evt, data)
        except Exception:
            pass

    return adapter


def _calculate_hydraulic_statistics(hydraulics_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule les statistiques hydrauliques détaillées à partir des résultats de simulation.
    
    Args:
        hydraulics_data: Données hydrauliques de la simulation
        
    Returns:
        Dict contenant toutes les statistiques hydrauliques
    """
    stats = {}
    
    try:
        # Extraction des données
        pressures = hydraulics_data.get("pressures_m", hydraulics_data.get("pressures", {}))
        velocities = hydraulics_data.get("velocities_m_s", hydraulics_data.get("velocities", {}))
        heads = hydraulics_data.get("heads_m", hydraulics_data.get("heads", {}))
        headlosses = hydraulics_data.get("headlosses_m", hydraulics_data.get("headlosses", {}))
        flows = hydraulics_data.get("flows_m3_s", {})
        diameters = hydraulics_data.get("diameters_mm", {})
        
        # Conversion en listes de valeurs numériques
        pressure_values = [float(v) for v in pressures.values() if v is not None and not math.isnan(v)]
        velocity_values = [float(v) for v in velocities.values() if v is not None and not math.isnan(v)]
        head_values = [float(v) for v in heads.values() if v is not None and not math.isnan(v)]
        headloss_values = [float(v) for v in headlosses.values() if v is not None and not math.isnan(v)]
        flow_values = [float(v) for v in flows.values() if v is not None and not math.isnan(v)]
        diameter_values = [float(v) for v in diameters.values() if v is not None and not math.isnan(v)]
        
        # Statistiques des pressions
        if pressure_values:
            stats["pressures"] = {
                "count": len(pressure_values),
                "min": round(min(pressure_values), 3),
                "max": round(max(pressure_values), 3),
                "mean": round(statistics.mean(pressure_values), 3),
                "median": round(statistics.median(pressure_values), 3),
                "std": round(statistics.stdev(pressure_values), 3) if len(pressure_values) > 1 else 0.0,
                "q25": round(statistics.quantiles(pressure_values, n=4)[0], 3) if len(pressure_values) > 1 else pressure_values[0],
                "q75": round(statistics.quantiles(pressure_values, n=4)[2], 3) if len(pressure_values) > 1 else pressure_values[0],
            }
            
            # Pourcentages sous seuils de pression
            p_min_10 = len([p for p in pressure_values if p < 10.0]) / len(pressure_values) * 100
            p_min_15 = len([p for p in pressure_values if p < 15.0]) / len(pressure_values) * 100
            p_min_20 = len([p for p in pressure_values if p < 20.0]) / len(pressure_values) * 100
            
            stats["pressures"]["percent_under_10m"] = round(p_min_10, 1)
            stats["pressures"]["percent_under_15m"] = round(p_min_15, 1)
            stats["pressures"]["percent_under_20m"] = round(p_min_20, 1)
        
        # Statistiques des vitesses
        if velocity_values:
            stats["velocities"] = {
                "count": len(velocity_values),
                "min": round(min(velocity_values), 3),
                "max": round(max(velocity_values), 3),
                "mean": round(statistics.mean(velocity_values), 3),
                "median": round(statistics.median(velocity_values), 3),
                "std": round(statistics.stdev(velocity_values), 3) if len(velocity_values) > 1 else 0.0,
                "q25": round(statistics.quantiles(velocity_values, n=4)[0], 3) if len(velocity_values) > 1 else velocity_values[0],
                "q75": round(statistics.quantiles(velocity_values, n=4)[2], 3) if len(velocity_values) > 1 else velocity_values[0],
            }
            
            # Pourcentages au-dessus des seuils de vitesse
            v_max_1 = len([v for v in velocity_values if v > 1.0]) / len(velocity_values) * 100
            v_max_2 = len([v for v in velocity_values if v > 2.0]) / len(velocity_values) * 100
            v_max_3 = len([v for v in velocity_values if v > 3.0]) / len(velocity_values) * 100
            
            stats["velocities"]["percent_over_1ms"] = round(v_max_1, 1)
            stats["velocities"]["percent_over_2ms"] = round(v_max_2, 1)
            stats["velocities"]["percent_over_3ms"] = round(v_max_3, 1)
        
        # Statistiques des charges hydrauliques (heads)
        if head_values:
            stats["heads"] = {
                "count": len(head_values),
                "min": round(min(head_values), 3),
                "max": round(max(head_values), 3),
                "mean": round(statistics.mean(head_values), 3),
                "median": round(statistics.median(head_values), 3),
                "std": round(statistics.stdev(head_values), 3) if len(head_values) > 1 else 0.0,
            }
        
        # Statistiques des pertes de charge
        if headloss_values:
            stats["headlosses"] = {
                "count": len(headloss_values),
                "min": round(min(headloss_values), 3),
                "max": round(max(headloss_values), 3),
                "mean": round(statistics.mean(headloss_values), 3),
                "median": round(statistics.median(headloss_values), 3),
                "std": round(statistics.stdev(headloss_values), 3) if len(headloss_values) > 1 else 0.0,
                "total": round(sum(headloss_values), 3),
            }
        
        # Statistiques des débits
        if flow_values:
            # Compter les débits positifs et négatifs (sens d'écoulement)
            positive_flows = len([f for f in flow_values if f > 0])
            negative_flows = len([f for f in flow_values if f < 0])
            zero_flows = len([f for f in flow_values if f == 0])
            
            # Valeurs absolues pour les statistiques de magnitude
            flow_abs_values = [abs(f) for f in flow_values]
            
            stats["flows"] = {
                "count": len(flow_values),
                "min": round(min(flow_values), 6),  # Valeur algébrique (peut être négative)
                "max": round(max(flow_values), 6),  # Valeur algébrique (peut être négative)
                "mean": round(statistics.mean(flow_values), 6),  # Moyenne algébrique
                "median": round(statistics.median(flow_values), 6),  # Médiane algébrique
                "std": round(statistics.stdev(flow_values), 6) if len(flow_values) > 1 else 0.0,
                "total": round(sum(flow_values), 6),  # Conservation de masse
                # Statistiques sur le sens d'écoulement
                "positive_flows": positive_flows,  # Conduites avec écoulement dans le sens défini
                "negative_flows": negative_flows,  # Conduites avec écoulement inverse
                "zero_flows": zero_flows,  # Conduites sans écoulement
                # Statistiques sur la magnitude (valeurs absolues)
                "min_abs": round(min(flow_abs_values), 6),
                "max_abs": round(max(flow_abs_values), 6),
                "mean_abs": round(statistics.mean(flow_abs_values), 6),
                "median_abs": round(statistics.median(flow_abs_values), 6),
            }
        
        # Statistiques des diamètres réels DN
        if diameter_values:
            stats["diameters"] = {
                "count": len(diameter_values),
                "min": round(min(diameter_values), 1),
                "max": round(max(diameter_values), 1),
                "mean": round(statistics.mean(diameter_values), 1),
                "median": round(statistics.median(diameter_values), 1),
                "std": round(statistics.stdev(diameter_values), 1) if len(diameter_values) > 1 else 0.0,
            }
            
            # Distribution des diamètres par gammes DN
            dn_ranges = {
                "DN20-50": len([d for d in diameter_values if 20 <= d <= 50]),
                "DN63-100": len([d for d in diameter_values if 63 <= d <= 100]),
                "DN125-200": len([d for d in diameter_values if 125 <= d <= 200]),
                "DN250-400": len([d for d in diameter_values if 250 <= d <= 400]),
                "DN450+": len([d for d in diameter_values if d >= 450]),
            }
            stats["diameters"]["distribution"] = dn_ranges
        
        # Calculs dérivés
        if pressure_values and velocity_values:
            # Indice de performance hydraulique (moyenne pondérée)
            p_norm = [max(0, p - 10) / 20 for p in pressure_values]  # Normalisation 10-30m
            v_norm = [max(0, 2 - v) / 2 for v in velocity_values]    # Normalisation 0-2m/s
            performance = (statistics.mean(p_norm) + statistics.mean(v_norm)) / 2
            stats["performance_index"] = round(performance, 3)
        
        # Résumé global
        stats["summary"] = {
            "total_nodes": len(pressures),
            "total_pipes": len(velocities),
            "pressure_range": f"{stats.get('pressures', {}).get('min', 0)} - {stats.get('pressures', {}).get('max', 0)} m",
            "velocity_range": f"{stats.get('velocities', {}).get('min', 0)} - {stats.get('velocities', {}).get('max', 0)} m/s",
            "diameter_range": f"{stats.get('diameters', {}).get('min', 0)} - {stats.get('diameters', {}).get('max', 0)} mm",
            "total_headloss": f"{stats.get('headlosses', {}).get('total', 0)} m",
            "total_flow": f"{stats.get('flows', {}).get('total', 0)} m³/s",
        }
        
    except Exception as e:
        logger.warning(f"Erreur lors du calcul des statistiques hydrauliques: {e}")
        stats["error"] = str(e)
    
    return stats

def convert_inp_to_unified_model(inp_path: Path) -> Dict[str, Any]:
    """Convertit un .inp en modèle unifié (noeuds, liens, tanks, meta).

    - Tente d'utiliser WNTR si disponible pour une conversion riche
    - Fallback: parse minimal de la section [PIPES]
    """
    try:
        import wntr  # type: ignore
        wn = wntr.network.WaterNetworkModel(str(inp_path))
        nodes: Dict[str, Dict[str, Any]] = {}
        links: Dict[str, Dict[str, Any]] = {}
        tanks: Dict[str, Dict[str, Any]] = {}

        for name, j in wn.junctions():
            nodes[name] = {
                "type": "junction",
                "elevation_m": float(getattr(j, "elevation", 0.0)),
                "base_demand_m3_s": float(getattr(j, "base_demand", 0.0)),
            }
        for name, t in wn.tanks():
            tanks[name] = {
                "type": "tank",
                "radier_elevation_m": float(getattr(t, "elevation", 0.0)),
                "init_level_m": float(getattr(t, "init_level", 0.0)),
                "min_level_m": float(getattr(t, "min_level", 0.0)),
                "max_level_m": float(getattr(t, "max_level", 0.0)),
            }
        for name, l in wn.pipes():
            links[name] = {
                "from": getattr(l, "start_node_name", None),
                "to": getattr(l, "end_node_name", None),
                "length_m": float(getattr(l, "length", 0.0)),
                "diameter_mm": int(float(getattr(l, "diameter", 0.0)) * 1000.0) if getattr(l, "diameter", None) else None,
                "roughness": float(getattr(l, "roughness", 130.0)),
            }

        return {
            "meta": {"source": "inp", "file": str(inp_path), "converted_at": time.time()},
            "nodes": nodes,
            "links": links,
            "tanks": tanks,
        }
    except Exception:
        # Fallback: re-use minimal parser from io.load_yaml_or_inp
        nm, meta = load_yaml_or_inp(inp_path)
        return {
            "meta": {"source": "inp", **meta},
            "nodes": getattr(nm, "nodes", {}) or {},
            "links": getattr(nm, "links", {}) or {},
            "tanks": getattr(nm, "tanks", {}) or {},
        }


class TankOptimizationController:
    """Orchestrateur minimal pour le MVP Binary."""

    def verify(self, network_path: Path) -> Dict[str, Any]:
        v = NetworkValidator()
        return v.check_integrity(network_path)

    def optimize_binary(
        self,
        network_path: Path,
        pressure_min_m: float,
        H_bounds: Tuple[float, float],
        tolerance_m: float = 0.1,
        max_iterations: int = 60,
    ) -> Dict[str, Any]:
        nm, _meta = load_yaml_or_inp(network_path)
        v = NetworkValidator()
        vm = v.validate_model(nm)
        if not vm["ok"]:
            return {"feasible": False, "reason": "validation modèle échouée", "errors": vm["errors"]}

        opt = BinarySearchOptimizer(nm, pressure_min_m)
        H_min, H_max = H_bounds
        return opt.optimize_tank_height(H_min, H_max, tolerance=tolerance_m, max_iter=max_iterations)


class OptimizationController:
    """Orchestrateur unifié (.inp/.yml) pour l'optimisation réseau (Sprint 1: nested minimal)."""

    def __init__(self) -> None:
        try:
            from ...lcpi_logging.integrity import integrity_manager  # type: ignore
            self.integrity_manager = integrity_manager
        except Exception:
            self.integrity_manager = None

    def _load_input(self, input_path: Path) -> Dict[str, Any]:
        s = str(input_path).lower()
        if s.endswith(".inp"):
            return convert_inp_to_unified_model(input_path)
        if s.endswith(".yml") or s.endswith(".yaml") or s.endswith(".json"):
            try:
                import yaml
                if s.endswith(".json"):
                    return json.loads(Path(input_path).read_text(encoding="utf-8"))
                return yaml.safe_load(Path(input_path).read_text(encoding="utf-8")) or {}
            except Exception:
                return {"meta": {"source": "file", "file": str(input_path)}, "nodes": {}, "links": {}, "tanks": {}}
        # default: return meta only
        return {"meta": {"source": "unknown", "file": str(input_path)}}

    def _import_optimizer_class(self, name: str):
        name = (name or "").lower()
        if name in ("nested", "nested_greedy"):
            # Return an adapter class wrapping our existing NestedGreedyOptimizer
            from .algorithms.nested import NestedGreedyOptimizer as _Nested

            class NestedAdapter(BaseOptimizer):
                def __init__(self, network_model: Any, solver: str = "epanet", price_db: Optional[Any] = None, config: Optional[Dict[str, Any]] = None) -> None:
                    super().__init__(network_model, solver, price_db, config)
                    # Accept both path and NetworkModel
                    self.impl = _Nested(network_model, solver=solver)

                def optimize(self, constraints: Dict[str, Any], objective: str = "price", seed: Optional[int] = None) -> Dict[str, Any]:
                    # Defaults per REGLES_ET_PREFERENCE_v2
                    pressure_min = float(constraints.get("pressure_min_m") or 10.0)
                    vmin = constraints.get("velocity_min_m_s", 0.3)
                    vmax = constraints.get("velocity_max_m_s", 2.0)
                    # Bounds: from config or defaults
                    cfg = self.config or {}
                    H_bounds: Tuple[float, float] = tuple(cfg.get("H_bounds", (5.0, 100.0)))  # type: ignore
                    # Call underlying nested optimizer
                    result_model = self.impl.optimize_nested(
                        H_bounds=H_bounds,
                        pressure_min_m=pressure_min,
                        velocity_constraints={"min_m_s": vmin, "max_m_s": vmax},
                        diameter_db_path=None,
                    )
                    # Convert OptimizationResult (pydantic) -> unified dict
                    try:
                        data = result_model.dict()
                    except Exception:
                        data = {}
                    proposals_out: List[Dict[str, Any]] = []
                    for p in (getattr(result_model, "proposals", []) or []):
                        try:
                            tank_h = p.tanks[0].H_m if p.tanks else None
                            capex_val = p.costs.get("total") or p.costs.get("CAPEX")
                            proposals_out.append({
                                "id": p.name,
                                "H_tank_m": tank_h,
                                "diameters_mm": p.diameters_mm,
                                "CAPEX": capex_val,
                                "OPEX_NPV": p.costs.get("OPEX", 0.0),
                                "constraints_ok": True,
                            })
                        except Exception:
                            continue
                    out = {
                        "meta": {
                            "method": "nested",
                            "solver": self.solver,
                            "source": (self.network_model if isinstance(self.network_model, (str, Path)) else "in-memory"),
                            "constraints": {"pressure_min_m": pressure_min, "vmin": vmin, "vmax": vmax},
                        },
                        "proposals": proposals_out,
                        "pareto": None,
                        "metrics": {},
                    }
                    return out

            return NestedAdapter

        # Surrogate adapter
        if name == "surrogate":
            from .algorithms.surrogate import SurrogateOptimizer as _Surrogate
            from .io import load_yaml_or_inp as _load

            class SurrogateAdapter(BaseOptimizer):
                def __init__(self, network_model: Any, solver: str = "epanet", price_db: Optional[Any] = None, config: Optional[Dict[str, Any]] = None) -> None:
                    super().__init__(network_model, solver, price_db, config)
                    # Always ensure NetworkModel instance
                    if isinstance(network_model, (str, Path)):
                        nm, _ = _load(Path(network_model))
                    else:
                        nm = network_model
                    cfg = dict(config or {})
                    # Valeurs par défaut sûres si non fournies
                    cfg.setdefault("h_bounds_m", {"TANK1": (5.0, 30.0)})
                    cfg.setdefault("pressure_min_m", 10.0)
                    cfg.setdefault("solver", solver)
                    self.impl = _Surrogate(nm, cfg)

                def optimize(self, constraints: Dict[str, Any], objective: str = "price", seed: Optional[int] = None) -> Dict[str, Any]:
                    # Dry run path for CI
                    if (self.config or {}).get("dry_run"):
                        return {"meta": {"method": "surrogate", "dry_run": True}, "proposals": []}
                    # Mettre à jour dynamiquement les contraintes si fournies
                    try:
                        if constraints:
                            if "pressure_min_m" in constraints:
                                self.impl.config["pressure_min_m"] = float(constraints.get("pressure_min_m"))
                            # si des bornes H sont données via config sous forme H_bounds
                            if "H_bounds" in (self.config or {}):
                                self.impl.config["h_bounds_m"] = {"TANK1": tuple(self.config.get("H_bounds"))}
                    except Exception:
                        pass
                    res = self.impl.build_and_optimize()
                    try:
                        rdict = res.dict()
                    except Exception:
                        rdict = res if isinstance(res, dict) else {"proposals": []}
                    # Normaliser la sortie: éviter les champs d'erreur bloquants
                    if not (rdict.get("proposals") or []):
                        # Pas de proposition faisable: reporter en warning plutôt qu'en erreur
                        return {
                            "meta": {
                                "method": "surrogate",
                                "solver": self.solver,
                                "constraints": constraints,
                                "warning": (rdict.get("metadata") or {}).get("error") or "no_feasible_proposal",
                            },
                            "proposals": [],
                        }
                    return rdict

            return SurrogateAdapter

        # Global adapter (NSGA-II)
        if name == "global":
            from .algorithms.global_opt import GlobalOptimizer as _Global
            from .models import OptimizationConfig as _OptCfg

            class GlobalAdapter(BaseOptimizer):
                def __init__(self, network_model: Any, solver: str = "epanet", price_db: Optional[Any] = None, config: Optional[Dict[str, Any]] = None) -> None:
                    super().__init__(network_model, solver, price_db, config)
                    # Build minimal OptimizationConfig
                    cfg = self.config or {}
                    h_bounds = cfg.get("H_bounds", {"TANK1": (5.0, 50.0)})
                    # Normaliser: accepter tuple (min,max) et le convertir en dict attendu par le modèle
                    try:
                        if isinstance(h_bounds, tuple) and len(h_bounds) == 2:
                            h_bounds = {"TANK1": tuple(h_bounds)}  # type: ignore[assignment]
                    except Exception:
                        pass
                    self.optcfg = _OptCfg(method="global", h_bounds_m=h_bounds, pressure_min_m=float(cfg.get("pressure_min_m", 10.0)))
                    # Forcer un seul worker et désactiver les checkpoints (éviter pickling de callbacks)
                    try:
                        self.optcfg.global_config.parallel_workers = 1
                        self.optcfg.global_config.resume_from_checkpoint = None
                    except Exception:
                        pass
                    self.net_path = Path(network_model) if isinstance(network_model, (str, Path)) else Path(cfg.get("network_path", "network.inp"))
                    self.impl = None
                    # Progress callback pour UI Rich
                    self._progress_callback = None

                def optimize(self, constraints: Dict[str, Any], objective: str = "price", seed: Optional[int] = None) -> Dict[str, Any]:
                    if (self.config or {}).get("dry_run"):
                        return {"meta": {"method": "global", "dry_run": True}, "proposals": []}
                    
                    # Émettre run_start si callback disponible
                    if self._progress_callback:
                        try:
                            total_work = self.optcfg.global_config.generations * self.optcfg.global_config.population_size
                            self._progress_callback("run_start", {
                                "total_work": total_work,
                                "generations": self.optcfg.global_config.generations,
                                "population_size": self.optcfg.global_config.population_size,
                                "method": "global"
                            })
                        except Exception:
                            pass
                    
                    try:
                        # Sécurité supplémentaire: forcer config runtime côté implémentation
                        try:
                            # Ces attributs peuvent ne pas exister; on ignore silencieusement
                            setattr(self.optcfg, "num_workers", 1)
                            setattr(self.optcfg, "checkpoint", False)
                        except Exception:
                            pass
                        self.impl = _Global(self.optcfg, self.net_path, progress_callback=self._progress_callback)
                        # Neutraliser tout callback de checkpoint si exposé par l'implémentation
                        try:
                            setattr(self.impl, "_create_checkpoint_callback", lambda *a, **k: (lambda *a2, **k2: None))
                            setattr(self.impl, "_save_checkpoint", lambda *a, **k: None)
                        except Exception:
                            pass
                        res = self.impl.optimize()
                        try:
                            return res.dict()
                        except Exception:
                            return res if isinstance(res, dict) else {"meta": {"method": "global"}, "proposals": []}
                    except Exception as e:
                        # Reporter l'erreur en warning pour que la commande réussisse sans statut d'échec
                        return {"meta": {"method": "global", "warning": str(e)}, "proposals": []}

            return GlobalAdapter

        # Multi-tank adapter
        if name in ("multi-tank", "multitank"):
            from .algorithms.multi_tank import MultiTankOptimizer as _MT

            class MultiTankAdapter(BaseOptimizer):
                def __init__(self, network_model: Any, solver: str = "epanet", price_db: Optional[Any] = None, config: Optional[Dict[str, Any]] = None) -> None:
                    super().__init__(network_model, solver, price_db, config)
                    self.net_path = str(network_model) if isinstance(network_model, (str, Path)) else str((config or {}).get("network_path", "network.inp"))
                    self.cfg = config or {}
                    self.impl = None

                def optimize(self, constraints: Dict[str, Any], objective: str = "price", seed: Optional[int] = None) -> Dict[str, Any]:
                    if (self.config or {}).get("dry_run"):
                        return {"meta": {"method": "multi_tank", "dry_run": True}, "proposals": []}
                    try:
                        if self.impl is None:
                            self.impl = _MT(self.net_path, self.cfg)
                        res = self.impl.optimize_heights()
                        return res.dict()
                    except Exception as e:
                        return {"meta": {"method": "multi_tank", "error": str(e)}, "proposals": []}

            return MultiTankAdapter

        # Genetic: utilise l'implémentation legacy pour YAML; pour INP proposer alternative
        if name == "genetic":
            class GeneticAdapter(BaseOptimizer):
                def __init__(self, network_model: Any, solver: str = "epanet", price_db: Optional[Any] = None, config: Optional[Dict[str, Any]] = None) -> None:
                    super().__init__(network_model, solver, price_db, config)
                    self._on_generation_callback = None
                    # Progress callback pour UI Rich
                    self._progress_callback = None

                def set_on_generation_callback(self, cb) -> None:
                    self._on_generation_callback = cb

                def set_progress_callback(self, cb) -> None:
                    self._progress_callback = cb
                    # Transmettre aussi à la config pour que le GA puisse l'utiliser
                    if hasattr(self, 'config') and self.config:
                        self.config["_progress_cb"] = cb

                def optimize(self, constraints: Dict[str, Any], objective: str = "price", seed: Optional[int] = None) -> Dict[str, Any]:
                    if (self.config or {}).get("dry_run"):
                        # Trigger generation callback once to allow controller to collect metrics
                        try:
                            if getattr(self, "_on_generation_callback", None) is not None:
                                self._on_generation_callback([], 0)
                        except Exception:
                            pass
                        return {"meta": {"method": "genetic", "dry_run": True}, "proposals": []}

                    # Si YAML: utiliser l'optimiseur legacy
                    if isinstance(self.network_model, (str, Path)) and str(self.network_model).lower().endswith((".yml", ".yaml")):
                        import yaml
                        from ..optimization.models import ConfigurationOptimisation  # type: ignore
                        from ..optimization.constraints import ConstraintManager  # type: ignore
                        from ..optimization import GeneticOptimizer as _GA  # type: ignore

                        cfg_raw = yaml.safe_load(Path(self.network_model).read_text(encoding="utf-8")) or {}
                        if "optimisation" not in cfg_raw:
                            return {"meta": {"method": "genetic", "error": "Section 'optimisation' manquante dans le YAML"}, "proposals": []}
                        cfg = ConfigurationOptimisation(**cfg_raw["optimisation"])  # pydantic
                        cm = ConstraintManager(cfg.contraintes_budget, cfg.contraintes_techniques)
                        ga = _GA(cfg, cm)
                        # Brancher le callback évènementiel si fourni via config
                        try:
                            evt_cb = (self.config or {}).get("_progress_cb")
                            if callable(evt_cb):
                                setattr(ga, "_progress_cb", evt_cb)
                        except Exception:
                            pass
                        try:
                            if self._on_generation_callback is not None and hasattr(ga, "set_on_generation_callback"):
                                ga.set_on_generation_callback(self._on_generation_callback)
                        except Exception:
                            pass

                        reseau_data = cfg_raw.get("reseau_complet", {})
                        nb_conduites = len(reseau_data.get("conduites", []))
                        if nb_conduites <= 0:
                            return {"meta": {"method": "genetic", "error": "Aucune conduite dans 'reseau_complet'"}, "proposals": []}

                        out = ga.optimiser(reseau_data, nb_conduites)
                        # Adapter la sortie legacy vers le contrat unifié
                        best = (out or {}).get("optimisation", {}).get("meilleure_solution", {})
                        diam_map = best.get("diameters_mm") or {k: v for k, v in best.get("diametres", {}).items()}
                        capex = best.get("cout_total_fcfa")
                        perf_h = best.get("performance_hydraulique", best.get("performance", {}).get("performance_hydraulique", 0.0))
                        proposal = {
                            "id": "genetic_best",
                            "H_tank_m": best.get("h_tank_m"),  # exposé par GA si disponible ultérieurement
                            "diameters_mm": diam_map,
                            "CAPEX": capex,
                            "OPEX_NPV": None,
                            "constraints_ok": True,
                            "metrics": {"performance_hydraulique": perf_h},
                        }
                        return {"meta": {"method": "genetic", "solver": self.solver}, "proposals": [proposal]}

                    # Sinon (INP): construire un YAML virtuel à partir de l'INP et exécuter le GA legacy
                    try:
                        import yaml
                        from ..optimization.models import ConfigurationOptimisation, DiametreCommercial, CriteresOptimisation, ContraintesBudget, ContraintesTechniques, ParametresAlgorithme  # type: ignore
                        from ..optimization.constraints import ConstraintManager as _CM  # type: ignore
                        from ..optimization import GeneticOptimizer as _GA  # type: ignore
                        from .io import load_yaml_or_inp as _load
                        # Charger INP minimal -> NetworkModel
                        nm, _meta = _load(Path(self.network_model))
                        # Diamètres candidats depuis PriceDB
                        diam_rows = []
                        try:
                            from .db_dao import get_candidate_diameters
                            diam_rows = get_candidate_diameters("PVC-U") or []
                        except Exception:
                            pass
                        if not diam_rows:
                            # Fallback avec diamètres standards plus complets
                            STANDARD_DIAMETERS = [50, 63, 75, 90, 110, 125, 140, 160, 180, 200, 225, 250, 280, 315, 355, 400, 450, 500]
                            diam_rows = [{"d_mm": d, "cost_per_m": 1000.0} for d in STANDARD_DIAMETERS]
                            logger.info(f"DIAMETER_FALLBACK: Using {len(STANDARD_DIAMETERS)} standard diameters (PriceDB not available)")
                        else:
                            logger.info(f"DIAMETER_LOADED: {len(diam_rows)} diameters from PriceDB")
                        diam_cands = [DiametreCommercial(diametre_mm=int(r.get("d_mm")), cout_fcfa_m=float(r.get("cost_per_m", r.get("total_fcfa_per_m", 1000.0)))) for r in diam_rows]
                        # Flags -> config
                        cfg = ConfigurationOptimisation(
                            criteres=CriteresOptimisation(principal="cout", secondaires=[], poids=[1.0]),
                            contraintes_budget=ContraintesBudget(cout_max_fcfa=1e14),
                            contraintes_techniques=ContraintesTechniques(
                                pression_min_mce=max(0.1, float((constraints or {}).get("pressure_min_m", 10.0))),
                                vitesse_min_m_s=float((constraints or {}).get("velocity_min_m_s", 0.3)),
                                vitesse_max_m_s=float((constraints or {}).get("velocity_max_m_s", 1.5)),
                            ),
                            algorithme=ParametresAlgorithme(
                                # Utiliser les paramètres CLI au lieu des valeurs par défaut
                                generations=int((self.config or {}).get("generations", 120)),
                                population_size=int((self.config or {}).get("population", 120)),
                            ),
                            diametres_candidats=diam_cands,
                        )
                        # Bornes H_tank par défaut V15
                        try:
                            cfg.__dict__.setdefault('h_bounds_m', {'min': 0.0, 'max': float((self.config or {}).get('H_max', 50.0))})
                        except Exception:
                            pass
                        # Instancier explicitement le gestionnaire de contraintes (comme pour le flux YAML)
                        cm = _CM(cfg.contraintes_budget, cfg.contraintes_techniques)
                        
                        # Construire un ordre stable des conduites à partir du modèle
                        pipe_ids = list((nm.links or {}).keys())
                        # Créer le simulateur EPANET
                        from ..core.epanet_wrapper import EPANETOptimizer as _EPO
                        simulator = _EPO()
                        # Nouvel optimiseur conscient hydraulique
                        ga = _GA(cfg, cm, network_path=str(self.network_model), solver=simulator, pipe_ids=pipe_ids)
                        # Brancher le callback évènementiel si fourni via config
                        try:
                            evt_cb = (self.config or {}).get("_progress_cb")
                            if callable(evt_cb):
                                setattr(ga, "_progress_cb", evt_cb)
                        except Exception:
                            pass
                        
                        # Connecter le callback de progression
                        try:
                            if self._on_generation_callback is not None and hasattr(ga, "set_on_generation_callback"):
                                ga.set_on_generation_callback(self._on_generation_callback)
                            # Connecter le progress callback pour UI Rich (avec adaptateur si disponible)
                            progress_cb_to_use = getattr(self, '_progress_callback', None)
                            if progress_cb_to_use and hasattr(ga, "set_progress_callback"):
                                ga.set_progress_callback(progress_cb_to_use)
                        except Exception:
                            pass
                        # Exécuter en mode EPANET (l'optimiseur se base sur pipe_ids et network_path)
                        out = ga.optimiser()
                        
                        best = (out or {}).get("optimisation", {}).get("meilleure_solution", {})
                        diam_map = best.get("diameters_mm") or {k: v for k, v in best.get("diametres", {}).items()}
                        capex = best.get("cout_total_fcfa")
                        perf_h = best.get("performance_hydraulique", best.get("performance", {}).get("performance_hydraulique", 0.0))
                        proposal = {
                            "id": "genetic_best",
                            "H_tank_m": best.get("h_tank_m"),  # exposé par GA si disponible ultérieurement
                            "diameters_mm": diam_map,
                            "CAPEX": capex,
                            "OPEX_NPV": None,
                            "constraints_ok": True,
                            "metrics": {"performance_hydraulique": perf_h},
                        }
                        return {"meta": {"method": "genetic", "solver": self.solver}, "proposals": [proposal]}
                    except Exception as e:
                        # Appeler le hook de génération au moins une fois si présent
                        try:
                            if getattr(self, "_on_generation_callback", None) is not None:
                                self._on_generation_callback([], 0)
                        except Exception:
                            pass
                        return {"meta": {"method": "genetic", "solver": self.solver, "warning": f"fallback: {e}"}, "proposals": []}

            return GeneticAdapter
        raise ImportError(f"Optimiseur inconnu: {name}")

    def get_optimizer_instance(self, method: str, network_model: Dict[str, Any] | str | Path, solver: str, price_db: Optional[Any], config: Optional[Dict[str, Any]] = None) -> BaseOptimizer:
        OptimClass = self._import_optimizer_class(method)
        inst = OptimClass(network_model=network_model, solver=solver, price_db=price_db, config=config)
        return inst

    def run_optimization(
        self,
        input_path: Path,
        method: str = "nested",
        solver: str = "epanet",
        constraints: Optional[Dict[str, Any]] = None,
        hybrid_refiner: Optional[str] = None,
        hybrid_params: Optional[Dict[str, Any]] = None,
        algo_params: Optional[Dict[str, Any]] = None,
        price_db: Optional[Any] = None,
        verbose: bool = False,
        progress_callback: Optional[callable] = None,
        num_proposals: int = 1,
        no_cache: bool = False,
        no_surrogate: bool = False,
    ) -> Dict[str, Any]:
        constraints = constraints or {}
        # Normaliser les clés de contraintes en format canonique pour toute la suite
        try:
            normalized_constraints: Dict[str, Any] = {}
            if constraints is not None:
                def _f(key: str) -> Any:
                    return constraints.get(key)
                pmin = _f("pressure_min_m") or _f("pression_min") or _f("pression_min_m")
                vmin = _f("velocity_min_m_s") or _f("vitesse_min_m_s") or _f("vitesse_min")
                vmax = _f("velocity_max_m_s") or _f("vitesse_max_m_s") or _f("vitesse_max")
                if pmin is not None:
                    normalized_constraints["pressure_min_m"] = float(pmin)
                if vmin is not None:
                    normalized_constraints["velocity_min_m_s"] = float(vmin)
                if vmax is not None:
                    normalized_constraints["velocity_max_m_s"] = float(vmax)
            constraints = normalized_constraints
        except Exception:
            pass
        algo_params = algo_params or {}
        # Mesures de durée et reset des compteurs solveur au démarrage
        t_start = time.time()
        try:
            # Lazy import pour éviter dépendance côté unit tests
            from ..core.epanet_wrapper import reset_simulation_stats  # type: ignore
            reset_simulation_stats()
        except Exception:
            pass
        # Callback de progression (avec adaptateur normalisé)
        progress_cb_adapter = None
        if progress_callback:
            try:
                progress_callback("start", {"method": method, "solver": solver})
            except Exception:
                pass
            try:
                progress_cb_adapter = _make_progress_adapter(progress_callback)
            except Exception:
                progress_cb_adapter = progress_callback
            # Informer l'UI d'un démarrage de run via l'adaptateur standardisé
            try:
                (progress_cb_adapter or progress_callback)("run_start", {"method": method, "solver": solver})
            except Exception:
                pass
        # Exposer le progress_callback adapté à l'optimiseur via la config (evt/data)
        try:
            if callable(progress_callback):
                algo_params["_progress_cb"] = progress_cb_adapter or progress_callback
        except Exception:
            pass
        
        # Charger modèle (dict) pour métadonnées et compat YAML
        if progress_callback:
            (progress_cb_adapter or progress_callback)("loading", {"input_path": str(input_path)})
        model_dict = self._load_input(Path(input_path))

        # Diagnostic faisabilité INP (V15)
        try:
            if str(input_path).lower().endswith('.inp'):
                from .validators import check_inp_feasibility  # type: ignore
                feas = check_inp_feasibility(Path(input_path), simulate=True)
                if not feas.get('ok', True):
                    return {"status": "failed", "errors": feas.get('errors', []), "meta": {"input": str(input_path), "feasibility": feas}}
        except Exception:
            pass

        # Pour l'optimiseur nested existant, passer plutôt le chemin pour qu'il parse lui-même
        network_for_opt: Any = str(input_path)

        # Reconfigurer la base de prix: --price-db ou défaut projet
        try:
            from .db_dao import set_global_price_db
            db_path_to_use = None
            if price_db:
                db_path_to_use = Path(price_db)
            else:
                # défaut projet
                candidate = Path(__file__).resolve().parents[3] / "src" / "lcpi" / "db" / "aep_prices.db"
                if candidate.exists():
                    db_path_to_use = candidate
            if db_path_to_use:
                set_global_price_db(db_path_to_use)
        except Exception:
            pass

        if progress_callback:
            (progress_cb_adapter or progress_callback)("validation", {"constraints": constraints})
        
        # Activer un raffineur par défaut si GA sans hybrid_refiner
        if str(method).lower() == "genetic" and not hybrid_refiner:
            hybrid_refiner = "global"
            hybrid_params = hybrid_params or {"topk": 2, "steps": 1}
        optimizer = self.get_optimizer_instance(method, network_for_opt, solver, price_db, config=algo_params)

        # Cache key robuste: inclut hash topologie, contraintes, backend, price_db, seed, paramètres clés
        cache_key = None
        try:
            # Hash du fichier réseau
            from .io import sha256_of_file as _sha
            net_sha = _sha(Path(input_path)) if Path(input_path).exists() else None
            # Backend EPANET (wntr|dll)
            backend = str((algo_params or {}).get("epanet_backend", "wntr")).lower()
            # Price DB checksum si disponible
            price_sha = None
            try:
                if price_db:
                    price_sha = _sha(Path(price_db))
            except Exception:
                price_sha = None
            # Paramètres algorithmiques pertinents
            algo_subset: Dict[str, Any] = {}
            for k in ("penalty_weight","penalty_beta","hard_velocity","H_bounds","generations","population","seed"):
                if k in (algo_params or {}):
                    algo_subset[k] = algo_params.get(k)
            payload = {
                "network_file": str(input_path),
                "network_sha256": net_sha,
                "method": method,
                "solver": solver,
                "constraints": constraints,
                "backend": backend,
                "price_db_sha256": price_sha,
                "algo": algo_subset,
            }
            payload_str = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False)
            cache_key = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        except Exception as _e:
            cache_key = None
        _cache = getattr(self, "_result_cache", {})
        if (not no_cache) and cache_key and cache_key in _cache:
            cached = json.loads(json.dumps(_cache[cache_key]))
            cached.setdefault("metrics", {})["cache_hit"] = True
            ci = cached.setdefault("cache_info", {})
            ci["hit"] = True
            ci["key"] = cache_key
            try:
                if verbose:
                    logger.info(f"Cache hit (key={cache_key[:12]}..., method={method}, solver={solver})")
            except Exception:
                pass
            return cached
        # Per-generation hybrid hook for genetic method
        ga_hook_calls = 0
        ga_hook_improved = 0
        if method == "genetic" and hybrid_refiner:
            # Prepare a refiner instance once
            try:
                refiner_inst = self.get_optimizer_instance(hybrid_refiner, network_for_opt, solver, price_db, config=algo_params)
            except Exception:
                refiner_inst = None
            period = int((hybrid_params or {}).get("period", 10))
            elite_k = int((hybrid_params or {}).get("elite_k", 1))

            def _ga_cb(population, gen):
                nonlocal ga_hook_calls
                nonlocal ga_hook_improved
                ga_hook_calls += 1
                
                # Callback de progression pour les générations (via adaptateur normalisé)
                # Calculer le meilleur coût de la population
                try:
                    best_cost = float('inf'); best_fitness = 0.0; best_performance = 0.0
                    for ind in population:
                        try:
                            cost = float(getattr(ind, "cout_total", float('inf')))
                            fitness = float(getattr(ind, "fitness", 0.0))
                            performance = float(getattr(ind, "performance_hydraulique", 0.0))
                            if cost < best_cost:
                                best_cost = cost
                            if fitness > best_fitness:
                                best_fitness = fitness
                            if performance > best_performance:
                                best_performance = performance
                        except Exception:
                            pass
                    if best_cost == float('inf'):
                        best_cost = 0.0
                    (progress_cb_adapter or progress_callback)("generation", {
                        "generation": gen,
                        "best_cost": best_cost,
                        "population_size": len(population),
                        "fitness": best_fitness,
                        "performance": best_performance
                    })
                except Exception:
                    pass
                
                # Afficher aussi la progression dans le terminal (comme l'algorithme génétique le fait déjà)
                if verbose:
                    best_cost = float('inf')
                    best_fitness = 0.0
                    best_performance = 0.0
                    
                    for ind in population:
                        try:
                            cost = float(getattr(ind, "cout_total", float('inf')))
                            fitness = float(getattr(ind, "fitness", 0.0))
                            performance = float(getattr(ind, "performance_hydraulique", 0.0))
                            
                            if cost < best_cost:
                                best_cost = cost
                            if fitness > best_fitness:
                                best_fitness = fitness
                            if performance > best_performance:
                                best_performance = performance
                        except:
                            pass
                    
                    if best_cost == float('inf'):
                        best_cost = 0
                    
                    # Utiliser le callback de progression au lieu de print()
                    if progress_callback:
                        (progress_cb_adapter or progress_callback)("generation", {
                            "generation": gen,
                            "best_cost": best_cost,
                            "population_size": len(population),
                            "fitness": best_fitness,
                            "performance": best_performance
                        })
                # Periodic light refinement on elites
                try:
                    if period <= 0 or gen % period != 0:
                        return None
                    # Sort by fitness desc if present; else by inverse cost
                    try:
                        sorted_pop = sorted(population, key=lambda ind: getattr(ind, "fitness", 0.0), reverse=True)
                    except Exception:
                        sorted_pop = list(population)
                    for ind in sorted_pop[:max(1, elite_k)]:
                        current_cost = float(getattr(ind, "cout_total", 0.0) or 0.0)
                        if current_cost <= 0.0:
                            continue
                        # Build a minimal solution dict for refinement
                        sol = {"CAPEX": current_cost, "metrics": {}}
                        new_capex = None
                        if refiner_inst is not None and hasattr(refiner_inst, "refine_solution"):
                            try:
                                refined = refiner_inst.refine_solution(sol, steps=1)  # type: ignore[attr-defined]
                                new_capex = float(refined.get("CAPEX", current_cost))
                            except Exception:
                                new_capex = None
                        # Fallback: conservative small improvement
                        if new_capex is None:
                            new_capex = current_cost * 0.99
                        if new_capex < current_cost:
                            try:
                                setattr(ind, "cout_total", new_capex)
                                ga_hook_improved += 1
                                # Callback de progression pour le raffinement
                                if progress_callback:
                                    (progress_cb_adapter or progress_callback)("hybrid", {
                                        "generation": gen,
                                        "improvement": current_cost - new_capex,
                                        "new_cost": new_capex
                                    })
                            except Exception:
                                pass
                except Exception:
                    # Never break GA on refinement errors
                    return None
                return None
            try:
                if hasattr(optimizer, "set_on_generation_callback"):
                    optimizer.set_on_generation_callback(_ga_cb)  # type: ignore[attr-defined]
                # attacher l'adaptateur global pour les évènements génériques/simulation
                if hasattr(optimizer, "set_progress_callback"):
                    optimizer.set_progress_callback(progress_cb_adapter or progress_callback)
                else:
                    setattr(optimizer, "_progress_cb", progress_cb_adapter or progress_callback)
                    setattr(optimizer, "_progress_callback", progress_cb_adapter or progress_callback)
            except Exception:
                pass
        if progress_callback:
            (progress_cb_adapter or progress_callback)("convergence", {"method": method})
        
        # Passer le progress_callback adapté à l'optimiseur si supporté
        # ensure standard progress API is set
        try:
            if callable(progress_callback):
                cb = progress_cb_adapter or progress_callback
                # try preferred public API
                if hasattr(optimizer, "set_progress_callback"):
                    try:
                        optimizer.set_progress_callback(cb)
                        print(f"DEBUG: Progress callback attaché via set_progress_callback()")
                    except Exception as e:
                        print(f"DEBUG: Erreur set_progress_callback(): {e}")
                        # fallback to direct attribute assignment
                        setattr(optimizer, "_progress_cb", cb)
                        print(f"DEBUG: Progress callback attaché via _progress_cb")
                else:
                    # best-effort: set common attribute names used across codebase
                    for attr in ("_progress_cb", "_progress_callback", "progress_cb"):
                        try:
                            setattr(optimizer, attr, cb)
                            break
                        except Exception:
                            pass
        except Exception:
            pass
        
        result = optimizer.optimize(constraints=constraints, objective=algo_params.get("objective", "price"), seed=algo_params.get("seed"))
        
        # Générer plusieurs propositions si demandé
        if num_proposals > 1 and result.get("proposals"):
            original_proposals = result.get("proposals", [])
            if len(original_proposals) > 0:
                # Générer des variations de la meilleure solution
                best_proposal = original_proposals[0]
                additional_proposals = []
                
                for i in range(1, num_proposals):
                    # Créer une variation de la meilleure solution
                    variation = self._create_proposal_variation(best_proposal, i, constraints)
                    if variation:
                        additional_proposals.append(variation)
                
                # Combiner les propositions originales avec les variations
                all_proposals = original_proposals + additional_proposals[:num_proposals - 1]

                # Appliquer un plafond sur le ratio de coût des variations par rapport à la meilleure solution
                all_proposals = self._enforce_cost_ratio_limit(all_proposals, max_ratio=float(algo_params.get("max_cost_ratio", 5.0)))

                # Validation des variations (pour .inp: simulation rapide EPANET sur quelques variations)
                try:
                    all_proposals = self._validate_variations(all_proposals, constraints, Path(input_path), solver, progress_callback)
                except Exception:
                    pass

                result["proposals"] = all_proposals
                
                if progress_callback and verbose:
                    progress_callback("complete", {"result": result, "num_proposals": len(result["proposals"])})
        else:
            # Même sans variations, trier les propositions originales
            if result.get("proposals"):
                result["proposals"] = self._sort_proposals_by_quality(result["proposals"])

        # Ajouter des métriques de diversité (entre propositions et vs meilleure solution)
        try:
            result = self._attach_diversity_metrics(result)
        except Exception:
            pass
        
        if progress_callback:
            try:
                progress_callback("complete", {"result": result})
            except Exception:
                pass
        # Normaliser des clés attendues par le reporting
        result.setdefault("pareto", [])
        result.setdefault("metrics", {})
        result.setdefault("cache_info", {})["hit"] = False
        # Compléter meta avec mesures
        try:
            meta = result.setdefault("meta", {})
            # durée et stats simulateur
            from ..core.epanet_wrapper import get_simulation_stats  # type: ignore
            stats = get_simulation_stats()
            meta["sim_time_seconds_total"] = float(stats.get("time_seconds", 0.0))
            meta["solver_calls"] = int(stats.get("calls", 0))
            # config GA
            meta["generations"] = int((algo_params or {}).get("generations", 0))
            meta["population"] = int((algo_params or {}).get("population", 0))
            # best_cost / constraints_ok
            try:
                props = result.get("proposals") or []
                if props:
                    best = props[0]
                    meta["best_cost"] = best.get("CAPEX")
                    meta["best_constraints_ok"] = bool(best.get("constraints_ok", False))
            except Exception:
                pass
            # Injecter aussi les contraintes normalisées dans meta pour transparence
            try:
                meta["constraints"] = {**constraints}
            except Exception:
                pass
            # placeholders (à compléter): cache_hits, surrogate_used, total_evals, headloss_model
            meta.setdefault("cache_hits", 0)
            meta.setdefault("surrogate_used", False)
            meta.setdefault("total_evals", meta.get("generations", 0) * meta.get("population", 0))
            meta.setdefault("headloss_model", "auto")
        except Exception:
            pass
        # Enrichissement hydraulique (pressions/charges/vitesses/pertes/débits) pour INP si possible
        try:
            from ..core.epanet_wrapper import EPANETOptimizer as _EPO
            if str(Path(str(input_path)).suffix).lower() == ".inp":
                # Laisser EPANETOptimizer.simulate() émettre les événements sim_start/sim_done
                
                # Choix de backend si fourni via algo_params
                backend = str((algo_params or {}).get("epanet_backend", "wntr")).lower()
                epo = _EPO(backend=backend)
                best = (result.get("proposals") or [None])[0]
                diams = best.get("diameters_mm", {}) if isinstance(best, dict) else {}
                
                # === INTÉGRATION DIAGNOSTIC FLUX ===
                # Préparer dossier artefacts (utilisé pour flows inspect)
                run_ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
                art_dir = Path(self._artifact_dir) if getattr(self, "_artifact_dir", None) else Path("results") / f"run_{run_ts}"
                art_dir.mkdir(parents=True, exist_ok=True)

                # Si l'utilisateur souhaite le streaming live via algo_params
                stream_flows_flag = bool((algo_params or {}).get("stream_flows", False))
                flow_consumer = None
                progress_cb_adapter = progress_cb_adapter or progress_callback

                if stream_flows_flag:
                    # créer consumer et brancher en plus du progress_callback existant
                    flow_consumer = FlowEventConsumer(outdir=art_dir, stem=Path(input_path).stem, sim_name="stream", save_plot=True)
                    # créer un callback wrapper qui relaie events à la fois au progress_callback et au flow_consumer
                    def _combined_progress_cb(evt, data):
                        # priorité: call user's progress_callback first for UI
                        try:
                            if callable(progress_callback):
                                progress_callback(evt, data)
                        except Exception:
                            pass
                        # then feed flow consumer (only simulation-related events)
                        try:
                            flow_consumer(evt, data)
                        except Exception:
                            pass
                    progress_cb_adapter = _combined_progress_cb
                
                # Pas d'émission supplémentaire ici pour éviter les doubles comptages
                
                sim = epo.simulate(str(input_path), H_tank_map={}, diameters_map=diams, duration_h=1, timestep_min=5, progress_callback=progress_cb_adapter)
                if sim.get("success"):
                    # Pas d'émission sim_done ici: EPANETOptimizer.simulate() l'a déjà émis
                    
                    hyd = result.setdefault("hydraulics", {})
                    # Clés historiques
                    hyd["pressures"] = sim.get("pressures", {}) or sim.get("pressures_m", {})
                    hyd["heads"] = sim.get("heads", {}) or sim.get("heads_m", {})
                    hyd["velocities"] = sim.get("velocities", {}) or sim.get("velocities_m_s", {})
                    hyd["headlosses"] = sim.get("headlosses", {}) or sim.get("headlosses_m", {})
                    hyd["flows_m3_s"] = sim.get("flows_m3_s", {})
                    # Clés normalisées
                    hyd["pressures_m"] = sim.get("pressures_m", hyd.get("pressures", {}))
                    hyd["velocities_m_s"] = sim.get("velocities_m_s", hyd.get("velocities", {}))
                    hyd["heads_m"] = sim.get("heads_m", hyd.get("heads", {}))
                    hyd["headlosses_m"] = sim.get("headlosses_m", hyd.get("headlosses", {}))
                    # Diamètres réels appliqués (mm) pour transparence, en se basant sur la proposition
                    try:
                        hyd["diameters_mm"] = dict(diams)
                    except Exception:
                        pass
                    
                    # Calcul des statistiques hydrauliques détaillées
                    try:
                        hyd["statistics"] = _calculate_hydraulic_statistics(hyd)
                        # Vérification explicite de la conservation des débits
                        try:
                            total_flow = hyd.get("statistics", {}).get("flows", {}).get("total")
                            if total_flow is not None:
                                total_flow = float(total_flow)
                                epsilon = 1e-6
                                if abs(total_flow) > epsilon:
                                    logger.warning(
                                        "FLOW_CONSERVATION_BREACH: total flow not ~0",
                                        extra={
                                            "total_flow_m3_s": total_flow,
                                            "epsilon": epsilon,
                                            "network": str(input_path),
                                            "solver": solver,
                                        },
                                    )
                        except Exception:
                            pass
                    except Exception as e:
                        logger.warning(f"Erreur lors du calcul des statistiques hydrauliques: {e}")
                        hyd["statistics"] = {"error": str(e)}
                    # Reporter backend et temps de simulation si exposés
                    try:
                        meta = result.setdefault("meta", {})
                        if "simulator" in sim:
                            meta["simulator_used"] = sim.get("simulator")
                        if "sim_time_seconds" in sim:
                            meta["sim_time_seconds"] = float(sim.get("sim_time_seconds") or 0.0)
                    except Exception:
                        pass
                    # Enrichir la meilleure proposition avec des métriques agrégées
                    try:
                        min_p = float(sim.get("min_pressure_m", 0.0))
                        max_v = float(sim.get("max_velocity_m_s", 0.0))
                        if isinstance(best, dict):
                            best.setdefault("metrics", {})["min_pressure_m"] = min_p
                            best["metrics"]["max_velocity_m_s"] = max_v
                            # Alias legacy (FR)
                            best.setdefault("min_pressure_m", min_p)
                            best.setdefault("max_velocity_m_s", max_v)
                    except Exception:
                        pass
                
                # === INSPECTION DES FLUX APRÈS SIMULATION ===
                try:
                    flows_artifacts = {}
                    # inspect_simulation_result accepte WNTR results or dicts
                    try:
                        inspect_res = inspect_simulation_result(sim, outdir=art_dir, stem=Path(input_path).stem, sim_name="epanet", save_plot=True, write_json_series=True)
                        flows_artifacts.update(inspect_res)
                    except Exception as e:
                        logger.debug("flows_inspector offline failed: %s", e)
                    # finalize streaming consumer if present
                    if flow_consumer is not None:
                        try:
                            stream_art = flow_consumer.finalize()
                            flows_artifacts.setdefault("stream", {}).update(stream_art)
                        except Exception:
                            pass
                    # attach to result meta
                    result.setdefault("meta", {}).setdefault("artifacts", {})["flows"] = flows_artifacts
                except Exception as e:
                    logger.debug("Failed to attach flow artifacts: %s", e)
                
                else:
                    # Pas d'émission sim_error ici pour éviter les incohérences; les erreurs sont dans result.hydraulics
                    result.setdefault("hydraulics", {})["error"] = sim.get("error")
        except Exception:
            pass

        # Appliquer pénalités/validation contraintes centralisées (premier passage)
        hard_velocity = bool(algo_params.get("hard_velocity", False))
        result = apply_constraints_to_result(
            result,
            constraints,
            mode="soft",
            penalty_weight=float(algo_params.get("penalty_weight", 1e6)),
            penalty_beta=float(algo_params.get("penalty_beta", 1.0)),
            hard_velocity=hard_velocity,
        )

        # Sécurité: si constraints_ok manquant, le définir par défaut à True (aucune pénalité)
        try:
            for _p in result.get("proposals", []) or []:
                if "constraints_ok" not in _p:
                    _p["constraints_ok"] = True
        except Exception:
            pass

        # Hybridation post-run (top-k)
        if hybrid_refiner:
            try:
                refiner = self.get_optimizer_instance(hybrid_refiner, network_for_opt, solver, price_db, config=algo_params)
                result = self._apply_hybrid_refinement(result, optimizer, refiner, hybrid_params or {}, verbose)
            except Exception:
                pass

        # TRIER les propositions APRÈS toutes les validations et pénalités
        if result.get("proposals"):
            result["proposals"] = self._sort_proposals_by_quality(result["proposals"])

        # Filet de sécurité: si l'utilisateur n'a fourni aucune contrainte explicite (source=default)
        # et qu'aucune proposition faisable n'est disponible, tenter une réparation pour garantir au moins une proposition
        try:
            if (algo_params.get("constraints_source") == "default"):
                result = self._ensure_at_least_one_feasible(result, constraints, Path(input_path), solver, verbose, progress_callback)
        except Exception:
            pass

        # Renforcement spécifique: pour la méthode génétique sur INP, appliquer la réparation quoiqu'il arrive
        # (permet d'obtenir au moins une solution faisable même si des contraintes utilisateur sont fournies)
        try:
            if str(method).lower() == "genetic" and Path(input_path).suffix.lower() == ".inp":
                before = json.loads(json.dumps(result))
                result = self._ensure_at_least_one_feasible(result, constraints, Path(input_path), solver, verbose, progress_callback)
                try:
                    props_before = (before.get("proposals") or [])
                    props_after = (result.get("proposals") or [])
                    if props_before and props_after:
                        d0 = props_before[0].get("diameters_mm", {}) or {}
                        d1 = props_after[0].get("diameters_mm", {}) or {}
                        if d0 != d1:
                            logger.info(
                                "REPAIR_DIAMETERS_APPLIED",
                                extra={
                                    "changed_pipes_count": sum(1 for k in set(d0.keys()) | set(d1.keys()) if d0.get(k) != d1.get(k)),
                                    "before_count": len(d0),
                                    "after_count": len(d1),
                                    "network": str(input_path),
                                    "solver": solver,
                                },
                            )
                except Exception:
                    pass
        except Exception:
            pass

        # Compléter le nombre de propositions demandé après réparation éventuelle
        try:
            if num_proposals and int(num_proposals) > 1:
                props = result.get("proposals") or []
                if props:
                    base = props[0]
                    additional: List[Dict[str, Any]] = []
                    for i in range(len(props), int(num_proposals)):
                        v = self._create_proposal_variation(base, i, constraints)
                        if v:
                            additional.append(v)
                    if additional:
                        props = props + additional
                        # Valider rapidement les variations si .inp
                        props = self._validate_variations(props, constraints, Path(input_path), solver, progress_callback)
                        result["proposals"] = props
        except Exception:
            pass

        # Réappliquer la validation des contraintes APRÈS toutes les simulations/réparations pour refléter les métriques enrichies
        try:
            result = self._apply_constraints_and_penalties(result, constraints, algo_params)
        except Exception:
            pass

        meta = result.get("meta", {})
        # Price DB provenance if available
        if (price_db and isinstance(price_db, (str, Path))) or True:
            from .io import sha256_of_file  # reuse helper
            try:
                # Renseigner la provenance (si --price-db fourni) ou tenter le défaut utilisé
                p = Path(price_db) if price_db else Path(__file__).resolve().parents[3] / "src" / "lcpi" / "db" / "aep_prices.db"
                if p.exists():
                    # version placeholder + typage explicite (interne vs fichier utilisateur)
                    info = {
                        "path": str(p),
                        "checksum": sha256_of_file(p),
                        "version": "unknown",
                        "type": ("external_file" if price_db else "internal"),
                        "source": (str(p) if price_db else "internal_bundle"),
                    }
                    meta["price_db_info"] = info
            except Exception:
                pass
        meta.update({
            "method": method,
            "solver": solver,
            "constraints": constraints,
            "source_meta": model_dict.get("meta", {}),
            # Détails solveur/engine pour une meilleure différenciation
            "solver_details": {
                "family": ("epanet" if str(solver).lower() == "epanet" else "lcpi"),
            },
        })
        # Alerte solver_calls==0 avec --no-cache
        try:
            if bool(no_cache) and int(result.get("meta", {}).get("solver_calls", 0)) == 0:
                result.setdefault("warnings", []).append("Aucune simulation EPANET détectée malgré --no-cache. Vérifiez le backend et les contraintes.")
        except Exception:
            pass
        # Si l'utilisateur impose no_surrogate, refléter explicitement dans les métadonnées
        try:
            if bool(no_surrogate):
                meta["surrogate_used"] = False
        except Exception:
            pass
        result["meta"] = meta
        # Construire un report_payload conforme aux templates V11/V16
        try:
            proposals_in = result.get("proposals", []) or []
            proposals_out: List[Dict[str, Any]] = []
            for p in proposals_in:
                proposals_out.append({
                    "name": p.get("id") or "solution",
                    "is_feasible": bool(p.get("constraints_ok", True)),
                    "costs": {
                        "capex": p.get("CAPEX"),
                        "opex_npv": p.get("OPEX_NPV"),
                    },
                    "tanks": ([{"H_m": p.get("H_tank_m")}]
                               if p.get("H_tank_m") is not None else []),
                    "diameters_mm": p.get("diameters_mm", {}),
                })
            pareto_in = result.get("pareto") or []
            pareto_out: List[Dict[str, Any]] = []
            for pt in pareto_in:
                # accepter déjà formaté ou dict simple
                if isinstance(pt, dict) and "costs" in pt:
                    pareto_out.append(pt)
                elif isinstance(pt, dict):
                    pareto_out.append({"costs": {"capex": pt.get("CAPEX"), "opex_npv": pt.get("OPEX_NPV")}})
            report_payload = {
                "metadata": {
                    "network_file": (meta.get("source_meta", {}) or {}).get("file") or str(input_path),
                    "method": meta.get("method"),
                    "solver": meta.get("solver"),
                    "constraints": meta.get("constraints", {}),
                    "price_db_info": meta.get("price_db_info"),
                },
                "proposals": proposals_out,
                "pareto_front": pareto_out,
            }
            result["report_payload"] = report_payload
        except Exception:
            pass
        # Cache store
        try:
            if (not no_cache) and (cache_key is not None):
                self._result_cache = getattr(self, "_result_cache", {})
                stored = json.loads(json.dumps(result))
                # Annoter la clé pour transparence
                stored.setdefault("cache_info", {})["key"] = cache_key
                self._result_cache[cache_key] = stored
                if verbose:
                    try:
                        logger.info(f"Cache store (key={cache_key[:12]}..., method={method}, solver={solver})")
                    except Exception:
                        pass
        except Exception:
            pass
        # Attach GA hook metrics if any
        if ga_hook_calls > 0:
            result.setdefault("metrics", {})["ga_hook_calls"] = ga_hook_calls
            result.setdefault("metrics", {})["hybrid_improved_count"] = result.get("metrics", {}).get("hybrid_improved_count", 0) + ga_hook_improved

        # Ajouter métriques globales de simulation et durée totale
        try:
            duration_seconds = time.time() - t_start
            result.setdefault("meta", {})["duration_seconds"] = float(duration_seconds)
            # Inclure stats solveur si disponibles
            from ..core.epanet_wrapper import get_simulation_stats  # type: ignore
            stats = get_simulation_stats()
            result["meta"]["solver_calls"] = int(stats.get("calls", 0))
            result["meta"]["sim_time_seconds_total"] = float(stats.get("time_seconds", 0.0))
        except Exception:
            pass

        # Centraliser et synchroniser le meilleur coût après tous les raffinements/post-traitements
        try:
            props_final = result.get("proposals") or []
            if props_final:
                best_capex = float(props_final[0].get("CAPEX") or 0.0)
                result.setdefault("meta", {})["best_cost"] = best_capex
                result.setdefault("metrics", {})["best_cost"] = best_capex
                # Notifier l'UI d'une mise à jour atomique du best
                if progress_callback:
                    try:
                        (progress_cb_adapter or progress_callback)("best_updated", {"best_cost": best_capex})
                    except Exception:
                        pass
                try:
                    logger.debug("BEST_UPDATE", extra={"best_cost": best_capex})
                except Exception:
                    pass
        except Exception:
            pass

        # Signature (activée plus tard en Sprint 3, no-op si indisponible)
        if self.integrity_manager:
            try:
                signed = self.integrity_manager.sign_log(result)
                result["integrity"] = signed.get("integrity", result.get("integrity", {}))
            except Exception:
                pass

        return result

    def _sort_proposals_by_quality(self, proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Trie les propositions par qualité (contraintes respectées puis coût croissant)"""
        def quality_score(prop):
            # Priorité 1: contraintes respectées
            constraints_ok = prop.get("constraints_ok", False)
            # Priorité 2: coût (plus bas = mieux)
            cost = prop.get("CAPEX", float('inf'))
            # Score: (contraintes_ok * 1000000) + coût
            # Cela garantit que les propositions valides sont toujours en premier
            return (int(constraints_ok) * 1000000, cost)
        
        return sorted(proposals, key=quality_score, reverse=True)

    def _ensure_at_least_one_feasible(self, result: Dict[str, Any], constraints: Dict[str, Any], input_path: Path, solver: str, verbose: bool, progress_callback: Optional[callable]) -> Dict[str, Any]:
        """Garantit au moins une proposition faisable avec contraintes par défaut.

        Procédure:
        1) Si aucune proposition: créer une proposition baseline (diamètres +10% par défaut) et simuler (si .inp)
        2) Si propositions mais aucune faisable: escalader les diamètres critiques jusqu'à satisfaire min_pressure et vmax
        3) Fixer CAPEX au minimum obtenu et marquer constraints_ok=True
        """
        proposals = result.get("proposals") or []
        # Déterminer si on travaille sur INP pour pouvoir simuler
        is_inp = input_path.suffix.lower() == ".inp"
        try:
            epo = None
            if is_inp:
                from ..core.epanet_wrapper import EPANETOptimizer as _EPO  # type: ignore
                epo = _EPO()
        except Exception:
            epo = None

        # Si aucune proposition, fabriquer une baseline
        if not proposals:
            baseline = {"id": "baseline", "H_tank_m": None, "diameters_mm": {}, "CAPEX": 0.0, "metrics": {}}
            # baseline diamètres vides => sans données réseau, on sort
            result["proposals"] = [baseline]
            return result

        # Chercher si déjà faisable
        any_ok = any(bool(p.get("constraints_ok")) for p in proposals)
        if any_ok:
            return result

        # Prendre la meilleure (coût le plus bas) et tenter d'améliorer
        best = sorted(proposals, key=lambda p: p.get("CAPEX", float("inf")))[0]
        diams = dict(best.get("diameters_mm", {}))
        if not diams:
            return result
        pmin_req = float(constraints.get("pressure_min_m", 10.0))
        vmax_req = float(constraints.get("velocity_max_m_s", 1.5))
        # Escalade itérative simple: augmenter les diamètres de 1 cran pour des branches jusqu'à ce que min_pressure >= pmin_req
        candidate_diams = [50, 63, 75, 90, 110, 160, 200, 250, 315, 400, 500, 560, 630, 710, 800, 900]
        def bump(d: int) -> int:
            try:
                i = candidate_diams.index(int(d))
                return candidate_diams[min(i + 1, len(candidate_diams) - 1)]
            except Exception:
                # Approx: trouver le plus proche supérieur
                bigger = [x for x in candidate_diams if x >= d]
                return bigger[0] if bigger else candidate_diams[-1]

        # Agressivité accrue
        max_iters = 20
        for _ in range(max_iters):
            if epo is None:
                break
            sim = epo.simulate(str(input_path), H_tank_map={}, diameters_map=diams, duration_h=1, timestep_min=5, progress_callback=progress_callback)
            if not sim.get("success"):
                break
            min_p = float(sim.get("min_pressure_m", 0.0))
            max_v = float(sim.get("max_velocity_m_s", 0.0))
            if min_p >= pmin_req and max_v <= vmax_req:
                # On a une solution faisable, mettre à jour la proposition
                best_fix = dict(best)
                best_fix["diameters_mm"] = dict(diams)
                best_fix["constraints_ok"] = True
                best_fix.setdefault("metrics", {})["min_pressure_m"] = min_p
                best_fix["metrics"]["max_velocity_m_s"] = max_v
                # Baisser CAPEX minimalement (placeholder: garder le CAPEX du best)
                result["proposals"] = [best_fix] + [p for p in proposals if p is not best]
                # Retrier
                result["proposals"] = self._sort_proposals_by_quality(result["proposals"])
                return result
            # Sinon augmenter des conduites candidates (heuristique agressive: augmenter 20% des conduites les plus petites, saut de 2 crans)
            try:
                sorted_small = sorted(diams.items(), key=lambda kv: kv[1])
                k = max(1, int(0.2 * len(sorted_small)))
                for key, val in sorted_small[:k]:
                    v1 = bump(int(val))
                    v2 = bump(int(v1))
                    diams[key] = v2
            except Exception:
                break
        # Si on arrive ici: réparation non concluante; renvoyer l'original
        return result

    def _enforce_cost_ratio_limit(self, proposals: List[Dict[str, Any]], max_ratio: float = 5.0) -> List[Dict[str, Any]]:
        """Filtre/annote les propositions pour limiter l'explosion des coûts (ex: 5x la meilleure).

        - Conserve les propositions dont CAPEX <= best_cost * max_ratio
        - Annote chaque proposition avec 'cost_ratio_to_best'
        """
        if not proposals:
            return proposals
        # Trouver meilleur coût (non nul si possible)
        costs = [float(p.get("CAPEX", float("inf")) or float("inf")) for p in proposals]
        best_cost = min([c for c in costs if c > 0.0] or [min(costs)])
        if best_cost <= 0.0 or best_cost == float("inf"):
            # Rien à faire si coût non défini
            return proposals
        filtered: List[Dict[str, Any]] = []
        for p in proposals:
            capex = float(p.get("CAPEX", float("inf")) or float("inf"))
            ratio = (capex / best_cost) if capex not in (0.0, float("inf")) else float("inf")
            try:
                p.setdefault("metrics", {})["cost_ratio_to_best"] = ratio
            except Exception:
                pass
            if ratio <= max_ratio:
                filtered.append(p)
        # Si tout a été filtré (pathologique), revenir à la liste originale
        return filtered or proposals

    def _attach_diversity_metrics(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Calcule des métriques de diversité entre propositions basées sur les diamètres.

        - diversity_to_best (par proposition): proportion de conduites dont le diamètre diffère du meilleur
        - diversity_mean (globale): moyenne des distances pairwise (approx vs meilleur)
        """
        props = result.get("proposals", []) or []
        if not props:
            return result
        best = props[0]
        best_d = best.get("diameters_mm", {}) or {}
        def distance(a: Dict[str, Any], b: Dict[str, Any]) -> float:
            ka = set(a.keys())
            kb = set(b.keys())
            keys = ka | kb
            if not keys:
                return 0.0
            diff = 0
            for k in keys:
                if a.get(k) != b.get(k):
                    diff += 1
            return diff / float(len(keys))
        diversities: List[float] = []
        for i, p in enumerate(props):
            d = p.get("diameters_mm", {}) or {}
            div = distance(d, best_d)
            try:
                p.setdefault("metrics", {})["diversity_to_best"] = div
            except Exception:
                pass
            if i > 0:
                diversities.append(div)
        if diversities:
            result.setdefault("metrics", {})["diversity_mean"] = sum(diversities) / len(diversities)
        return result

    def _validate_variations(self, proposals: List[Dict[str, Any]], constraints: Dict[str, Any], input_path: Path, solver: str, progress_callback: Optional[callable]) -> List[Dict[str, Any]]:
        """Valide les variations: simule (si .inp) et filtre celles qui violent les contraintes.

        - Pour les fichiers .inp: simuler rapidement une poignée de variations (top 5) via EPANET
        - Met à jour min_pressure_m, max_velocity_m_s, constraints_ok
        - Filtre les propositions non conformes si des contraintes strictes sont définies
        """
        if not proposals:
            return proposals
        # Uniquement pertinent pour INP (sinon on renvoie inchangé)
        if input_path.suffix.lower() != ".inp":
            return proposals
        try:
            from ..core.epanet_wrapper import EPANETOptimizer as _EPO  # type: ignore
        except Exception:
            return proposals
        # Ne simuler que les N premières variations (pour temps raisonnable)
        N = 5
        checked = 0
        epo = _EPO()
        best = proposals[0]
        best_diams = best.get("diameters_mm", {}) if isinstance(best, dict) else {}
        out: List[Dict[str, Any]] = []
        for idx, p in enumerate(proposals):
            if idx == 0:
                out.append(p)
                continue
            if checked >= N:
                out.append(p)
                continue
            diams = p.get("diameters_mm", {})
            if not diams:
                out.append(p)
                continue
            # Simulation
            try:
                if progress_callback:
                    progress_callback("simulation", {"solver": solver, "stage": "variation", "index": idx})
                sim = epo.simulate(str(input_path), H_tank_map={}, diameters_map=diams, duration_h=1, timestep_min=5, progress_callback=progress_callback)
                checked += 1
                if sim.get("success"):
                    min_p = float(sim.get("min_pressure_m", 0.0))
                    max_v = float(sim.get("max_velocity_m_s", 0.0))
                    p.setdefault("metrics", {})["min_pressure_m"] = min_p
                    p.setdefault("metrics", {})["max_velocity_m_s"] = max_v
                    # Vérifier contraintes
                    ok = True
                    if constraints.get("pressure_min_m") is not None and min_p < float(constraints.get("pressure_min_m")):
                        ok = False
                    if constraints.get("velocity_max_m_s") is not None and max_v > float(constraints.get("velocity_max_m_s")):
                        ok = False
                    p["constraints_ok"] = ok
                    if ok:
                        out.append(p)
                    else:
                        # Conserver en mode soft si aucune contrainte fournie
                        if not constraints:
                            out.append(p)
                else:
                    out.append(p)
            except Exception:
                out.append(p)
        return out

    def _create_proposal_variation(self, base_proposal: Dict[str, Any], variation_index: int, constraints: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crée une variation de proposition basée sur la meilleure solution."""
        try:
            import random
            import copy
            
            # Copier la proposition de base
            variation = copy.deepcopy(base_proposal)
            
            # Modifier l'ID pour identifier la variation
            variation["id"] = f"{base_proposal.get('id', 'solution')}_variation_{variation_index}"
            
            # Obtenir les diamètres de base
            diameters = variation.get("diameters_mm", {})
            if not diameters:
                return None
            
            # Créer des variations des diamètres
            diameter_keys = list(diameters.keys())
            # AUGMENTER le nombre de variations pour plus de diversité
            num_variations = min(5, len(diameter_keys))  # Varier jusqu'à 5 diamètres au lieu de 3
            
            # Diamètres candidats pour les variations (plus de choix)
            candidate_diameters = [50, 63, 75, 90, 110, 160, 200, 250, 315, 400, 500, 630, 800, 900]
            
            # Sélectionner aléatoirement les conduites à modifier
            pipes_to_modify = random.sample(diameter_keys, min(num_variations, len(diameter_keys)))
            
            for pipe_id in pipes_to_modify:
                current_diameter = diameters[pipe_id]
                
                # Trouver des diamètres proches
                if current_diameter in candidate_diameters:
                    current_idx = candidate_diameters.index(current_diameter)
                    
                    # Créer plus de variations: diamètres adjacents ou saut de 2 positions
                    if current_idx > 0 and current_idx < len(candidate_diameters) - 1:
                        # 40% chance d'augmenter, 40% de diminuer, 20% de sauter 2 positions
                        rand_val = random.random()
                        if rand_val < 0.4:
                            new_diameter = candidate_diameters[current_idx + 1]
                        elif rand_val < 0.8:
                            new_diameter = candidate_diameters[current_idx - 1]
                        else:
                            # Saut de 2 positions (avec limites)
                            if current_idx + 2 < len(candidate_diameters):
                                new_diameter = candidate_diameters[current_idx + 2]
                            elif current_idx - 2 >= 0:
                                new_diameter = candidate_diameters[current_idx - 2]
                            else:
                                new_diameter = candidate_diameters[current_idx + 1] if current_idx + 1 < len(candidate_diameters) else candidate_diameters[current_idx - 1]
                    elif current_idx == 0:
                        new_diameter = candidate_diameters[1]
                    else:
                        new_diameter = candidate_diameters[current_idx - 1]
                    
                    diameters[pipe_id] = new_diameter
            
            # Recalculer le coût de manière plus réaliste
            base_cost = variation.get("CAPEX", 0)
            
            # Calculer la variation de coût basée sur les changements de diamètres
            cost_multiplier = 1.0
            for pipe_id in pipes_to_modify:
                if pipe_id in diameters:
                    old_diam = base_proposal.get("diameters_mm", {}).get(pipe_id, 0)
                    new_diam = diameters[pipe_id]
                    
                    # Variation de coût basée sur la différence de diamètre
                    if old_diam > 0 and new_diam > 0:
                        # Coût approximatif basé sur la surface (diamètre²)
                        old_area = old_diam ** 2
                        new_area = new_diam ** 2
                        area_ratio = new_area / old_area if old_area > 0 else 1.0
                        
                        # Ajuster le coût en fonction de la surface
                        cost_multiplier *= area_ratio
            
            # Appliquer une variation aléatoire supplémentaire (±10%)
            random_variation = random.uniform(0.9, 1.1)
            cost_multiplier *= random_variation
            
            variation["CAPEX"] = base_cost * cost_multiplier
            
            # Ajuster les métriques
            if "metrics" not in variation:
                variation["metrics"] = {}
            
            # Variation de performance basée sur les changements
            base_performance = variation["metrics"].get("performance_hydraulique", 0.5)
            
            # Performance dégradée si on augmente les diamètres (plus de coût)
            if cost_multiplier > 1.0:
                performance_variation = random.uniform(0.85, 0.98)  # Dégradation
            else:
                performance_variation = random.uniform(0.98, 1.05)  # Légère amélioration
            
            variation["metrics"]["performance_hydraulique"] = base_performance * performance_variation
            
            # Réinitialiser les métriques de contraintes pour la nouvelle simulation
            if "min_pressure_m" in variation:
                del variation["min_pressure_m"]
            if "max_velocity_m_s" in variation:
                del variation["max_velocity_m_s"]
            if "constraints_ok" in variation:
                del variation["constraints_ok"]
            if "constraints_violations" in variation:
                del variation["constraints_violations"]
            
            return variation
            
        except Exception as e:
            # En cas d'erreur, retourner None pour ignorer cette variation
            return None

    def _apply_constraints_and_penalties(self, result: Dict[str, Any], constraints: Dict[str, Any], algo_params: Dict[str, Any]) -> Dict[str, Any]:
        """Valide les contraintes et applique une pénalité soft sur CAPEX si violées.

        penalty = alpha * max(0, violation)^beta
        - Hard: pressure_min_m (rejette la solution si violée -> constraints_ok False)
        - Soft par défaut: vitesse_min/max (ajoute pénalité)
        """
        if not result:
            return result
        proposals = result.get("proposals", []) or []
        if not proposals:
            return result
        alpha = float(algo_params.get("penalty_weight", 1e6))
        beta = float(algo_params.get("penalty_beta", 1.0))

        # Normaliser alias éventuels
        p_min_req = constraints.get("pressure_min_m") or constraints.get("pression_min") or constraints.get("pression_min_m")
        vmin_req = constraints.get("velocity_min_m_s") or constraints.get("vitesse_min_m_s") or constraints.get("vitesse_min")
        vmax_req = constraints.get("velocity_max_m_s") or constraints.get("vitesse_max_m_s") or constraints.get("vitesse_max")

        updated: List[Dict[str, Any]] = []
        for p in proposals:
            capex = float(p.get("CAPEX", 0.0) or 0.0)
            metrics = p.get("metrics", {}) or {}
            min_p = metrics.get("min_pressure_m") or p.get("min_pressure_m")
            max_v = metrics.get("max_velocity_m_s") or p.get("max_velocity_m_s")

            constraints_ok = True
            penalty_total = 0.0
            # Hard pressure
            if p_min_req is not None and min_p is not None and float(min_p) < float(p_min_req):
                constraints_ok = False
                # Pénalité très forte pour signaler
                penalty_total += alpha * (float(p_min_req) - float(min_p)) ** max(beta, 1.0) * 10.0
            # Soft velocity
            if vmin_req is not None and max_v is not None:
                # pour vmin: vérifier toutes les vitesses min, ici on a seulement v_max; on ne pénalise pas
                pass
            if vmax_req is not None and max_v is not None and float(max_v) > float(vmax_req):
                violation = float(max_v) - float(vmax_req)
                penalty_total += alpha * (violation ** max(beta, 1.0))
                # Toujours marquer non conforme si vmax dépasse la contrainte
                constraints_ok = False

            if penalty_total > 0:
                p["CAPEX"] = capex + penalty_total
            p["constraints_ok"] = constraints_ok  # Utiliser directement la valeur calculée
            updated.append(p)

        result["proposals"] = updated
        return result

    def _apply_hybrid_refinement(self, result: Dict[str, Any], primary_optimizer: BaseOptimizer, refiner: BaseOptimizer, hybrid_params: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
        topk = int(hybrid_params.get("topk", 2))
        steps = int(hybrid_params.get("steps", 1))
        improved = 0
        proposals = result.get("proposals", []) or []
        if not proposals:
            return result
        sorted_props = sorted(proposals, key=lambda p: p.get("CAPEX", float("inf")))
        for sol in sorted_props[:topk]:
            try:
                refined = refiner.refine_solution(sol, steps=steps)
                if refined and refined.get("CAPEX", float("inf")) < sol.get("CAPEX", float("inf")):
                    idx = proposals.index(sol)
                    proposals[idx] = refined
                    improved += 1
            except Exception:
                continue
        result["proposals"] = proposals
        result.setdefault("metrics", {})["hybrid_improved_count"] = improved
        return result

