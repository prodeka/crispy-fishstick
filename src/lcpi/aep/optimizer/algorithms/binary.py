from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class SimulationResult:
    pressures_m: Dict[str, float]
    velocities_m_s: Dict[str, float]
    min_pressure_m: float
    max_velocity_m_s: float
    metadata: Dict[str, Any]


class BaseSolver:
    def simulate(self, network, H_tank_m: float, diameters: Optional[Dict[str, int]] = None) -> SimulationResult:
        raise NotImplementedError


class MockSolver(BaseSolver):
    """Solveur heuristique ultra simple pour le MVP."""

    def simulate(self, network, H_tank_m: float, diameters: Optional[Dict[str, int]] = None) -> SimulationResult:
        nodes = getattr(network, "nodes", None) or {"n1": {"elevation_m": 0.0}, "n2": {"elevation_m": 5.0}}
        links = getattr(network, "links", None) or {"p1": {"length_m": 100.0, "diameter_mm": 110}}

        ds = []
        total_length = 0.0
        for lid, link in links.items():
            total_length += float(link.get("length_m", 100.0))
            ds.append(int(link.get("diameter_mm", 110)))
        mean_d = (sum(ds) / len(ds)) if ds else 110.0
        k = 0.01
        loss = k * total_length / (mean_d / 1000.0)

        pressures = {}
        p_min = float("inf")
        for nid, n in nodes.items():
            elev = float(n.get("elevation_m", 0.0))
            p = H_tank_m - loss - elev
            pressures[nid] = round(p, 3)
            if p < p_min:
                p_min = p

        velocities = {}
        v_max = 0.0
        for lid, link in links.items():
            d = float(link.get("diameter_mm", 110)) / 1000.0
            Q = 0.01
            v = Q / (3.14159 * (d ** 2) / 4)
            v = round(v, 3)
            velocities[lid] = v
            if v > v_max:
                v_max = v

        return SimulationResult(
            pressures_m=pressures,
            velocities_m_s=velocities,
            min_pressure_m=float(round(p_min, 3)),
            max_velocity_m_s=float(round(v_max, 3)),
            metadata={"H_tank_m": H_tank_m, "loss": loss},
        )


class BinarySearchOptimizer:
    def __init__(self, network_model, pressure_min_m: float, solver: Optional[BaseSolver] = None):
        self.network = network_model
        self.pressure_min = float(pressure_min_m)
        self.solver = solver or MockSolver()
        
        # Vérifier la disponibilité du gestionnaire centralisé des diamètres
        try:
            from ..diameter_manager import get_standard_diameters_with_prices
            diam_rows = get_standard_diameters_with_prices()
            print(f"✅ BinarySearch: {len(diam_rows)} diamètres disponibles depuis le gestionnaire centralisé")
        except Exception as e:
            print(f"⚠️ BinarySearch: Erreur lors du chargement des diamètres centralisés: {e}")

    def optimize_tank_height(self, H_min: float, H_max: float, tolerance: float = 0.1, max_iter: int = 60) -> Dict[str, Any]:
        low, high = float(H_min), float(H_max)
        best: Optional[Dict[str, Any]] = None
        iterations = 0

        sim_low = self.solver.simulate(self.network, low)
        sim_high = self.solver.simulate(self.network, high)
        monotonic = sim_high.min_pressure_m >= sim_low.min_pressure_m

        while (high - low) > tolerance and iterations < max_iter:
            mid = (low + high) / 2.0
            sim = self.solver.simulate(self.network, mid)
            if sim.min_pressure_m >= self.pressure_min:
                best = {"H_tank_m": mid, "sim": sim}
                high = mid
            else:
                low = mid
            iterations += 1

        if best is None:
            return {
                "feasible": False,
                "reason": "aucune hauteur dans l'intervalle ne satisfait la pression minimale",
                "checked": {"H_min": H_min, "H_max": H_max},
                "iterations": iterations,
            }

        sim = best["sim"]
        return {
            "feasible": True,
            "H_tank_m": round(float(best["H_tank_m"]), 3),
            "min_pressure_m": sim.min_pressure_m,
            "max_velocity_m_s": sim.max_velocity_m_s,
            "pressures_m": sim.pressures_m,
            "velocities_m_s": sim.velocities_m_s,
            "iterations": iterations,
            "meta": {
                "method": "binary",
                "solver": type(self.solver).__name__,
                "timestamp": datetime.utcnow().isoformat(),
                "monotonic": monotonic,
            },
        }


