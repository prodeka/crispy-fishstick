from __future__ import annotations

from typing import Any, Dict, List, Tuple, Optional
import random

try:
	import numpy as np
	from sklearn.ensemble import RandomForestRegressor
	SKLEARN_OK = True
except Exception:
	SKLEARN_OK = False

from ..io import convert_to_solver_network_data
from ..cache import OptimizationCache
from .nested import NestedGreedyOptimizer


def lhs_samples(n: int, bounds: Tuple[float, float]) -> List[float]:
	low, high = float(bounds[0]), float(bounds[1])
	return [low + (i + random.random()) * (high - low) / n for i in range(n)]


class SurrogateOptimizer:
	def __init__(self, network_model, solver: str = "lcpi", cache_dir: Optional[str] = None):
		self.network = network_model
		self.solver = solver
		self.model = None
		self.dataset: List[Tuple[float, float]] = []  # (H, min_pressure)
		self.cache = OptimizationCache(cache_dir)

	def _simulate_min_pressure(self, H: float, pressure_min_m: float = 0.0) -> float:
		# Utilise NestedGreedyOptimizer pour obtenir une évaluation rapide
		# et tente d’utiliser le cache si possible
		trial_diams: Dict[str, int] = {lid: int(link.get("diameter_mm")) for lid, link in (self.network.links or {}).items() if link.get("diameter_mm") is not None}
		cached = self.cache.get(
			self.network.dict() if hasattr(self.network, "dict") else self.network,
			H,
			trial_diams,
			context={"solver": self.solver, "method": "surrogate"},
		)
		if cached is not None:
			return float(cached.get("min_pressure_m", 0.0))
		opt = NestedGreedyOptimizer(self.network, solver=self.solver)
		res = opt.optimize_nested((H, H), pressure_min_m=pressure_min_m)
		p_min = 0.0
		if isinstance(res, dict):
			# Re-simuler proprement pour obtenir p_min en une passe
			p_min = float(res.get("binary", {}).get("min_pressure_m", 0.0)) if isinstance(res.get("binary"), dict) else 0.0
		# Enregistrer au cache (structure minimale)
		self.cache.set(
			self.network.dict() if hasattr(self.network, "dict") else self.network,
			H,
			trial_diams,
			{"min_pressure_m": p_min},
			context={"solver": self.solver, "method": "surrogate"},
		)
		return p_min

	def build_and_optimize(self, H_bounds: Tuple[float, float], n_initial: int = 50, top_k: int = 5, rounds: int = 2, pressure_min_m: float = 0.0, grid_points: int = 200) -> Dict[str, Any]:
		# Étape 1: générer un dataset initial
		Hs = lhs_samples(n_initial, H_bounds)
		for H in Hs:
			p_min = self._simulate_min_pressure(H, pressure_min_m=pressure_min_m)
			self.dataset.append((H, p_min))

		validated: List[Tuple[float, float]] = []
		H_sel = float(H_bounds[1])

		# Étape 2-3: surrogate + active learning
		for _ in range(max(1, rounds)):
			if SKLEARN_OK and len(self.dataset) >= 10:
				X = np.array([[h] for h, _ in self.dataset])
				y = np.array([p for _, p in self.dataset])
				self.model = RandomForestRegressor(n_estimators=200, random_state=42)
				self.model.fit(X, y)
				grid = np.linspace(H_bounds[0], H_bounds[1], grid_points).reshape(-1, 1)
				pred = self.model.predict(grid)
				order = np.argsort(-pred)
				candidates = [float(grid[i][0]) for i in order[:max(1, top_k)]]
			else:
				candidates = [h for h, _ in sorted(self.dataset, key=lambda t: -t[1])[:max(1, top_k)]]

			for hc in candidates:
				p_min_c = self._simulate_min_pressure(hc, pressure_min_m=pressure_min_m)
				validated.append((hc, p_min_c))
				self.dataset.append((hc, p_min_c))

			if validated:
				if SKLEARN_OK:
					import numpy as _np
					cible = max(pressure_min_m, float(_np.median([p for _, p in validated])))
				else:
					vals = [p for _, p in validated]
					cible = max(pressure_min_m, sum(vals) / len(vals))
				feas = [h for h, p in validated if p >= cible]
				H_sel = float(min(feas)) if feas else float(min(validated, key=lambda t: -t[1])[0])

		# Étape 4: valider via nested
		final = NestedGreedyOptimizer(self.network, solver=self.solver).optimize_nested(H_bounds=(H_sel, H_sel), pressure_min_m=pressure_min_m)
		return {"meta": {"method": "surrogate"}, "H_selected": H_sel, "validated": validated, "dataset_size": len(self.dataset), "result": final}
