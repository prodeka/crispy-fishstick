from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseOptimizer(ABC):
    """Interface de base pour les optimiseurs AEP.

    Tous les optimiseurs appelés par la CLI unifiée doivent exposer cette API.
    """

    def __init__(
        self,
        network_model: Dict[str, Any] | Any,
        solver: str = "epanet",
        price_db: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.network_model = network_model
        self.solver = solver
        self.price_db = price_db
        self.config = config or {}

    @abstractmethod
    def optimize(
        self, constraints: Dict[str, Any], objective: str = "price", seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """Lance l'optimisation et retourne un dictionnaire standardisé.

        Retour attendu:
            {
                'meta': {...},
                'proposals': [ { 'id': 'p1', 'H_tank_m': .., 'diameters_mm': {...}, 'CAPEX': .., 'constraints_ok': bool }, ...],
                'pareto': [...],  # optionnel
                'metrics': {...}
            }
        """
        raise NotImplementedError

    def refine_solution(self, solution: Dict[str, Any], steps: int = 1) -> Dict[str, Any]:
        """Optionnel: améliore localement une solution donnée si possible."""
        return solution


class SimpleAdapter(BaseOptimizer):
    """Adaptateur générique pour encapsuler un optimiseur existant.

    Tente d'appeler `optimize`, `run` ou un callable simple.
    """

    def __init__(
        self,
        impl: Any,
        network_model: Dict[str, Any] | Any,
        solver: str = "epanet",
        price_db: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(network_model, solver, price_db, config)
        self.impl = impl

    def optimize(
        self, constraints: Dict[str, Any], objective: str = "price", seed: Optional[int] = None
    ) -> Dict[str, Any]:
        if hasattr(self.impl, "optimize"):
            return self.impl.optimize(constraints=constraints, objective=objective, seed=seed)
        if hasattr(self.impl, "run"):
            return self.impl.run(constraints=constraints, objective=objective, seed=seed)
        # Fallback: callable sans args
        res = self.impl()
        if isinstance(res, dict):
            return res
        raise RuntimeError("Underlying optimizer does not expose a known entry point (optimize/run)")

    def refine_solution(self, solution: Dict[str, Any], steps: int = 1) -> Dict[str, Any]:
        if hasattr(self.impl, "refine_solution"):
            return self.impl.refine_solution(solution, steps=steps)
        if hasattr(self.impl, "refine"):
            return self.impl.refine(solution, steps=steps)
        return solution


