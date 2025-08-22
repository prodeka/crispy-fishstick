from __future__ import annotations

from typing import Any, Dict, Optional

from ..io import NetworkModel
from ...core.solvers.factory import SolverFactory


class LCPIOptimizer:
    """Wrapper LCPI (Hardy-Cross) pour optimisation (Jalon 2 - version minimale)."""

    def __init__(self):
        self.solver = SolverFactory.get_solver("lcpi")

    def simulate_with_tank_height(
        self,
        network_model: NetworkModel,
        H_tank: float,
        diameters: Optional[Dict[str, int]] = None,
    ) -> Dict[str, Any]:
        network_dict = network_model.dict()
        params = {"H_tank": float(H_tank), "diameters": diameters or {}}
        result = self.solver.simulate_network(network_dict, **params)
        return result
    
    def _get_network_model_from_path(self, network_path: str | Path) -> NetworkModel:
        """Charge un modèle réseau depuis un chemin de fichier (.inp ou .yml)."""
        from ..io import load_yaml_or_inp
        nm, _ = load_yaml_or_inp(Path(network_path))
        return nm


