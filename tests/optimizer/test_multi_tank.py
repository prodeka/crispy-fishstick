from __future__ import annotations

from src.lcpi.aep.optimizer.algorithms.multi_tank import MultiTankOptimizer


class MockEPANETOptimizer:
    def simulate(self, network_path, H_tank_map):
        """
        Ce faux solveur retourne une pression minimale qui est simplement
        la moyenne des hauteurs des réservoirs. L'optimum est donc que toutes
        les hauteurs soient à leur maximum.
        """
        avg_h = sum(H_tank_map.values()) / max(1, len(H_tank_map))
        return {"success": True, "min_pressure_m": avg_h}


def test_multi_tank_optimizer_logic():
    """Teste que l'optimiseur ajuste les hauteurs dans la bonne direction."""
    config = {
        "h_bounds_m": {
            "T1": [50.0, 60.0],
            "T2": [70.0, 80.0]
        },
        "pressure_min_m": 65.0,  # Cible plus réaliste (moyenne des hauteurs min)
        "max_iterations": 5,
        "tolerance_m": 0.1
    }

    # Instancier l'optimiseur avec le faux solveur
    optimizer = MultiTankOptimizer(network_path="dummy_path.inp", config=config)
    optimizer.solver = MockEPANETOptimizer()

    result = optimizer.optimize_heights()
    # Access as pydantic model
    assert bool(result.metadata.get("feasible")) is True
    assert result.proposals and result.proposals[0].metrics.get("min_pressure_m", 0) >= config["pressure_min_m"]
