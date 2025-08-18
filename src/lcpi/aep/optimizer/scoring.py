from __future__ import annotations

from typing import Dict, Any


class CostScorer:
    """Stub de calcul des coûts (MVP)."""

    def __init__(self, diameter_cost_db: Dict[int, float] | None = None, energy_cost_kwh: float = 0.15):
        self.diameter_costs = diameter_cost_db or {}
        self.energy_cost = energy_cost_kwh

    def compute_capex(self, network: Any, diameters: Dict[str, int]) -> float:
        # somme length_m * cost(d_mm) si disponibles
        links = getattr(network, "links", None)
        if links is None and isinstance(network, dict):
            links = network.get("links", {})
        total = 0.0
        for lid, link in links.items():
            length = float(link.get("length_m", 0.0))
            d = diameters.get(lid, link.get("diameter_mm"))
            if d is None:
                continue
            cost_per_m = float(self.diameter_costs.get(int(d), 0.0))
            total += length * cost_per_m
        return float(total)

    def compute_opex_annual(self, network: Dict[str, Any], H_tank_m: float) -> float:
        # MVP: placeholder simple
        return 0.0

    def compute_total_cost(self, network: Any, diameters: Dict[str, int], H_tank_m: float) -> Dict[str, float]:
        capex = self.compute_capex(network, diameters)
        opex = self.compute_opex_annual(network, H_tank_m)
        return {"CAPEX": capex, "OPEX_annual": opex, "total_cost": capex + opex}


