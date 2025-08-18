from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, List
from dataclasses import dataclass

import yaml

from .binary import BinarySearchOptimizer, MockSolver
from ..io import NetworkModel, convert_to_solver_network_data
from ..solvers.lcpi_optimizer import LCPIOptimizer
from ..solvers.epanet_optimizer import EPANETOptimizer
from ..scoring import CostScorer


@dataclass
class NestedResult:
	feasible: bool
	H_tank_m: Optional[float]
	diameters_mm: Dict[str, int]
	meta: Dict[str, Any]


class NestedGreedyOptimizer:
	"""Optimisation en deux étapes (Jalon 2 - version améliorée)."""

	def __init__(self, network_model: NetworkModel, solver: str = "auto"):
		self.network = network_model
		self.solver_choice = solver

	def optimize_nested(
		self,
		H_bounds: Tuple[float, float],
		pressure_min_m: float,
		velocity_constraints: Optional[Dict[str, float]] = None,
		diameter_db_path: Optional[str] = None,
	) -> Dict[str, Any]:
		# Étape 1: H_tank (binaire)
		binary = BinarySearchOptimizer(self.network, pressure_min_m)
		bres = binary.optimize_tank_height(H_bounds[0], H_bounds[1])
		if not bres.get("feasible"):
			return {"feasible": False, "reason": "binary infeasible", "binary": bres}

		H_opt = float(bres["H_tank_m"])

		vmin = (velocity_constraints or {}).get("min_m_s", 0.0)
		vmax = (velocity_constraints or {}).get("max_m_s", float("inf"))

		# Charger DB diamètres
		candidates: List[int] = []
		db = []
		if diameter_db_path:
			try:
				db = yaml.safe_load(open(diameter_db_path, "r", encoding="utf-8").read()) or []
				candidates = sorted({int(row["d_mm"]) for row in db})
			except Exception:
				candidates = []
		if not candidates:
			candidates = [50, 63, 75, 90, 110, 125, 140, 160, 200]

		current = {lid: int(link.get("diameter_mm")) for lid, link in (self.network.links or {}).items() if link.get("diameter_mm") is not None}

		# Sélection du solveur
		simulate_with = self._build_simulator(self.solver_choice)

		# Tri par longueur décroissante
		links_sorted = sorted(
			(list(self.network.links.items()) if isinstance(self.network.links, dict) else []),
			key=lambda kv: float(kv[1].get("length_m", 0.0)),
			reverse=True,
		)

		for lid, link in links_sorted:
			existing = int(link.get("diameter_mm", current.get(lid, candidates[-1])))
			feasible_choice = existing
			for d in candidates:
				if d > existing:
					break
				trial = dict(current)
				trial[lid] = d
				p_min, v_max, pressures, velocities = simulate_with(H_opt, trial)
				if p_min >= pressure_min_m and _vmin_ok(vmin, velocities) and v_max <= vmax:
					feasible_choice = d
				else:
					break
			current[lid] = feasible_choice

		# Scoring CAPEX
		try:
			d_costs = {int(row["d_mm"]): float(row.get("cost_per_m", 0.0)) for row in (db or [])}
		except Exception:
			d_costs = {}
		scorer = CostScorer(d_costs)
		costs = scorer.compute_total_cost(self.network, current, H_opt)

		return {
			"feasible": True,
			"H_tank_m": H_opt,
			"diameters_mm": current,
			"costs": costs,
			"meta": {"method": "nested", "binary_iterations": bres.get("iterations")},
		}

	def _build_simulator(self, solver: str):
		# Prefer EPANET if requested, else LCPI, else Mock
		if solver == "epanet":
			try:
				epo = EPANETOptimizer()
				def simulate_with(H: float, diams: Dict[str, int]):
					data = epo.simulate_with_tank_height(self.network, H, diams)
					pressures = data.get("pressures") or data.get("pressions") or {}
					velocities = data.get("velocities", {})
					p_min = min(pressures.values()) if pressures else 0.0
					v_max = max(velocities.values()) if velocities else 0.0
					return p_min, v_max, pressures, velocities
				return simulate_with
			except Exception:
				pass
		try:
			lcpi = LCPIOptimizer()
			def simulate_with(H: float, diams: Dict[str, int]):
				data = convert_to_solver_network_data(self.network, H, diams)
				r = lcpi.solver.run_simulation(data)
				pressures = r.get("pressures", {}) or r.get("pressions", {}) or {}
				velocities = r.get("velocities", {})
				p_min = min(pressures.values()) if pressures else 0.0
				v_max = max(velocities.values()) if velocities else 0.0
				return p_min, v_max, pressures, velocities
			return simulate_with
		except Exception:
			mock = MockSolver()
			def simulate_with(H: float, diams: Dict[str, int]):
				sim = mock.simulate(self.network, H, diams)
				return sim.min_pressure_m, sim.max_velocity_m_s, sim.pressures_m, sim.velocities_m_s
			return simulate_with


def _vmin_ok(vmin: float, velocities: Dict[str, float]) -> bool:
	if vmin <= 0:
		return True
	return all((v >= vmin) for v in velocities.values())


