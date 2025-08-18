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

	def _simulate_min_pressure(self, H: float) -> float:
		# Utilise NestedGreedyOptimizer pour obtenir une évaluation rapide
		# et tente d’utiliser le cache si possible
		trial_diams: Dict[str, int] = {lid: int(link.get("diameter_mm")) for lid, link in (self.network.links or {}).items() if link.get("diameter_mm") is not None}
		cached = self.cache.get(self.network.dict() if hasattr(self.network, "dict") else self.network, H, trial_diams)
		if cached is not None:
			return float(cached.get("min_pressure_m", 0.0))
		opt = NestedGreedyOptimizer(self.network, solver=self.solver)
		res = opt.optimize_nested((H, H), pressure_min_m=0.0)
		p_min = 0.0
		if isinstance(res, dict):
			# Re-simuler proprement pour obtenir p_min en une passe
			p_min = float(res.get("binary", {}).get("min_pressure_m", 0.0)) if isinstance(res.get("binary"), dict) else 0.0
		# Enregistrer au cache (structure minimale)
		self.cache.set(self.network.dict() if hasattr(self.network, "dict") else self.network, H, trial_diams, {"min_pressure_m": p_min})
		return p_min

	def build_and_optimize(self, H_bounds: Tuple[float, float], n_initial: int = 50) -> Dict[str, Any]:
		# Étape 1: générer un dataset initial
		Hs = lhs_samples(n_initial, H_bounds)
		for H in Hs:
			p_min = self._simulate_min_pressure(H)
			self.dataset.append((H, p_min))

		# Étape 2: entraîner un surrogate simple
		if SKLEARN_OK and len(self.dataset) >= 10:
			X = np.array([[h] for h, _ in self.dataset])
			y = np.array([p for _, p in self.dataset])
			self.model = RandomForestRegressor(n_estimators=100, random_state=42)
			self.model.fit(X, y)
			# Étape 3: optimiser sur le surrogate
			grid = np.linspace(H_bounds[0], H_bounds[1], 200).reshape(-1, 1)
			pred = self.model.predict(grid)
			cible = max(1.0, float(np.percentile(pred, 50)))
			feasible = [grid[i][0] for i in range(len(grid)) if pred[i] >= cible]
			H_sel = float(min(feasible)) if feasible else float(H_bounds[1])
		else:
			best = max(self.dataset, key=lambda t: t[1]) if self.dataset else (H_bounds[1], 0.0)
			H_sel = float(best[0])

		# Étape 4: valider via nested
		final = NestedGreedyOptimizer(self.network, solver=self.solver).optimize_nested(H_bounds=(H_sel, H_sel), pressure_min_m=0.0)
		return {"meta": {"method": "surrogate"}, "H_selected": H_sel, "result": final}
