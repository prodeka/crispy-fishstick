from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from .io import load_yaml_or_inp
from .validators import NetworkValidator
from .algorithms.binary import BinarySearchOptimizer


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


