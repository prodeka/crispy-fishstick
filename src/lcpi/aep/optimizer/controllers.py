from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List

from .io import load_yaml_or_inp
from .validators import NetworkValidator
from .algorithms.binary import BinarySearchOptimizer
from .base import BaseOptimizer, SimpleAdapter
import json
import time


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
        raise ImportError(f"Optimiseur inconnu (Sprint 1 supporte uniquement 'nested'): {name}")

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
    ) -> Dict[str, Any]:
        constraints = constraints or {}
        algo_params = algo_params or {}

        # Charger modèle (dict) pour métadonnées et compat YAML
        model_dict = self._load_input(Path(input_path))

        # Pour l'optimiseur nested existant, passer plutôt le chemin pour qu'il parse lui-même
        network_for_opt: Any = str(input_path)

        optimizer = self.get_optimizer_instance(method, network_for_opt, solver, price_db, config=algo_params)
        result = optimizer.optimize(constraints=constraints, objective=algo_params.get("objective", "price"), seed=algo_params.get("seed"))

        meta = result.get("meta", {})
        meta.update({"method": method, "solver": solver, "constraints": constraints, "source_meta": model_dict.get("meta", {})})
        result["meta"] = meta

        # Signature (activée plus tard en Sprint 3, no-op si indisponible)
        if self.integrity_manager:
            try:
                signed = self.integrity_manager.sign_log(result)
                result["integrity"] = signed.get("integrity", result.get("integrity", {}))
            except Exception:
                pass

        return result

