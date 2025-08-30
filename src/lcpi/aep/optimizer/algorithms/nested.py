from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, List
from pathlib import Path
from dataclasses import dataclass

import yaml

from .binary import BinarySearchOptimizer, MockSolver
from ..io import NetworkModel, convert_to_solver_network_data
from ..solvers import EPANETOptimizer
from ..solvers.lcpi_optimizer import LCPIOptimizer
from ..scoring import CostScorer
from ..db import PriceDB
from ..models import OptimizationResult, Proposal, TankDecision
from ...utils.warnings_filter import suppress_warnings_decorator


@dataclass
class NestedResult:
	feasible: bool
	H_tank_m: Optional[float]
	diameters_mm: Dict[str, int]
	meta: Dict[str, Any]


class NestedGreedyOptimizer:
	"""Optimisation en deux étapes (Jalon 2 - version améliorée)."""

	def __init__(self, network_model: NetworkModel | str | Path, solver: str = "auto"):
		self.network = network_model
		self.solver_choice = solver

	@suppress_warnings_decorator
	def optimize_nested(
		self,
		H_bounds: Tuple[float, float],
		pressure_min_m: float,
		velocity_constraints: Optional[Dict[str, float]] = None,
		diameter_db_path: Optional[str] = None,
	) -> OptimizationResult:
		# Étape 1: H_tank (binaire)
		binary = BinarySearchOptimizer(self._get_network_model(), pressure_min_m)
		bres = binary.optimize_tank_height(H_bounds[0], H_bounds[1])
		if not bres.get("feasible"):
			return OptimizationResult(
				proposals=[],
				pareto_front=None,
				metadata={
					"method": "nested_greedy",
					"error": "binary infeasible",
					"binary_result": bres,
					"feasible": False
				}
			)

		H_opt = float(bres["H_tank_m"])

		vmin = (velocity_constraints or {}).get("min_m_s", 0.0)
		vmax = (velocity_constraints or {}).get("max_m_s", float("inf"))

		# Charger diamètres depuis le gestionnaire centralisé
		try:
			from ..diameter_manager import get_standard_diameters_with_prices
			db_rows = get_standard_diameters_with_prices()
			candidates: List[int] = sorted(int(row["d_mm"]) for row in (db_rows or []))
			logger.info(f"✅ {len(candidates)} diamètres chargés depuis le gestionnaire centralisé")
		except Exception as e:
			logger.warning(f"Erreur lors du chargement des diamètres centralisés: {e}")
			# Fallback avec diamètres standards et prix réalistes
			candidates = [50, 63, 75, 90, 110, 125, 140, 160, 180, 200, 225, 250, 280, 315, 355, 400, 450, 500]
			logger.info(f"⚠️ Utilisation de {len(candidates)} diamètres standards (fallback)")

		nm = self._get_network_model()
		current = {lid: int(link.get("diameter_mm")) for lid, link in (nm.links or {}).items() if link.get("diameter_mm") is not None}

		# Sélection du solveur
		simulate_with = self._build_simulator(self.solver_choice)

		# Tri par criticité (longueur / diametre^2) pour prioriser les conduites influentes
		def get_criticality(link_tuple):
			link_data = link_tuple[1]
			length = float(link_data.get("length_m", 0.0))
			diameter = float(link_data.get("diameter_mm", 1.0)) # Evite division par zéro
			return length / (diameter**2)

		links_sorted = sorted(
			(list(nm.links.items()) if isinstance(nm.links, dict) else []),
			key=get_criticality,
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

		# Mesurer les métriques hydrauliques finales avec la solution trouvée
		p_min_final, v_max_final, _pressures, _velocities = simulate_with(H_opt, current)

		# Scoring CAPEX relié à la DB de prix, avec détail tuyaux + accessoires
		scorer = CostScorer(diameter_cost_db=None)
		breakdown = scorer.compute_capex_with_breakdown(nm, current)
		capex = breakdown.get("total_capex", 0.0)
		# total = CAPEX (pas d'OPEX ici)
		costs = {
			"CAPEX": capex,
			"OPEX": 0.0,
			"total": capex,
			"CAPEX_breakdown": breakdown,
		}

		# Créer la proposition au format V11
		tank_decision = TankDecision(
			id="TANK1",  # À adapter selon le réseau
			H_m=H_opt
		)

		proposal = Proposal(
			name="nested_greedy_solution",
			is_feasible=True,
			tanks=[tank_decision],
			diameters_mm=current,
			costs=costs,
			metrics={
				"min_pressure_m": float(p_min_final),
				"max_velocity_m_s": float(v_max_final),
				"binary_iterations": bres.get("iterations")
			}
		)

		# Retourner le résultat au format V11
		return OptimizationResult(
			proposals=[proposal],
			pareto_front=None,  # Pas de front Pareto pour cet optimiseur
			metadata={
				"method": "nested_greedy",
				"network_file": self._get_network_file_path(),
				"binary_iterations": bres.get("iterations"),
				"pressure_min_m": pressure_min_m,
				"velocity_constraints": velocity_constraints,
				"diameter_db_path": diameter_db_path
			}
		)

	def _build_simulator(self, solver: str):
		# Prefer EPANET if requested, else LCPI, else Mock
		if solver == "epanet":
			try:
				epo = EPANETOptimizer()
				def simulate_with(H: float, diams: Dict[str, int]):
					data = epo.simulate_with_tank_height(self._get_network_input_for_epanet(), H, diams)
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
				data = convert_to_solver_network_data(self._get_network_model(), H, diams)
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
				sim = mock.simulate(self._get_network_model(), H, diams)
				return sim.min_pressure_m, sim.max_velocity_m_s, sim.pressures_m, sim.velocities_m_s
			return simulate_with

	def _get_network_model(self) -> NetworkModel:
		# Si self.network est un chemin, charger via load_yaml_or_inp
		from ..io import load_yaml_or_inp
		if isinstance(self.network, (str, Path)):
			nm, _ = load_yaml_or_inp(Path(self.network))
			return nm
		return self.network

	def _get_network_file_path(self) -> str:
		if isinstance(self.network, (str, Path)):
			return str(self.network)
		try:
			return str(getattr(self.network, 'file_path'))
		except Exception:
			return "unknown"

	def _get_network_input_for_epanet(self):
		# EPANETOptimizer accepte un chemin vers un .inp pour une simulation réelle
		if isinstance(self.network, (str, Path)):
			return str(self.network)
		return self._get_network_model()


def _vmin_ok(vmin: float, velocities: Dict[str, float]) -> bool:
	if vmin <= 0:
		return True
	return all((v >= vmin) for v in velocities.values())


