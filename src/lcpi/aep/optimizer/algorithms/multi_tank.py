from __future__ import annotations

from typing import Dict, Any, Tuple, List

from .binary import BinarySearchOptimizer
from ..algorithms.nested import NestedGreedyOptimizer


class MultiTankOptimizer:
    """Coordinate descent simple pour plusieurs réservoirs, puis greedy DN.

    H_bounds_by_tank: dict[tank_id, (Hmin, Hmax)]
    """

    def __init__(self, network_model, solver: str = "lcpi"):
        self.network = network_model
        self.solver = solver

    def optimize(self, H_bounds_by_tank: Dict[str, Tuple[float, float]], pressure_min_m: float) -> Dict[str, Any]:
        # Simplification: on optimise séquentiellement chaque tank (2 passes)
        H_sel: Dict[str, float] = {}
        for _ in range(2):
            for tid, bounds in H_bounds_by_tank.items():
                # Ajuster temporairement le réseau pour fixer ce tank
                # Ici on suppose un seul tank utilisé dans BinarySearchOptimizer (approx)
                b = BinarySearchOptimizer(self.network, pressure_min_m)
                res = b.optimize_tank_height(bounds[0], bounds[1])
                if not res.get("feasible"):
                    return {"feasible": False, "reason": f"infeasible tank {tid}", "partial": H_sel}
                H_sel[tid] = float(res["H_tank_m"])

        # DN greedy pour H fixés (approx avec nested en traitant H moyen)
        H_avg = sum(H_sel.values()) / max(1, len(H_sel))
        nested = NestedGreedyOptimizer(self.network, solver=self.solver)
        gres = nested.optimize_nested((H_avg, H_avg), pressure_min_m)
        return {"feasible": True, "H_tanks": H_sel, "nested": gres}


