import pytest
from unittest.mock import MagicMock
from src.lcpi.aep.optimizer.algorithms.multi_tank import MultiTankOptimizer

# Création d'un mock pour le solveur EPANET
class MockEPANETOptimizer:
    def simulate(self, network_path, H_tank_map, **kwargs):
        """
        Ce faux solveur retourne une pression minimale qui est simplement
        la moyenne des hauteurs des réservoirs. L'optimum est donc que toutes
        les hauteurs soient à leur maximum.
        """
        avg_height = sum(H_tank_map.values()) / len(H_tank_map)
        return {
            "success": True,
            "min_pressure_m": avg_height,
            "pressures": {f"node_{i}": avg_height for i in range(len(H_tank_map))},
            "velocities": {f"link_{i}": 1.0 for i in range(len(H_tank_map))}
        }


def test_multi_tank_optimizer_logic():
    """Teste que l'optimiseur ajuste les hauteurs dans la bonne direction."""
    config = {
        "h_bounds_m": {
            "T1": [50.0, 60.0],
            "T2": [70.0, 80.0]
        },
        "pressure_min_m": 65.0, # Cible plus réaliste (moyenne des hauteurs min)
        "max_iterations": 5,
        "tolerance_m": 0.1
    }

    # Instancier l'optimiseur avec le faux solveur
    optimizer = MultiTankOptimizer(network_path="dummy_path.inp", config=config)
    optimizer.solver = MockEPANETOptimizer()

    result = optimizer.optimize_heights()

    assert result["feasible"]
    
    # L'algorithme doit avoir augmenté les hauteurs par rapport à leur point de départ
    # (qui est le milieu des bornes: 55 et 75)
    final_h_t1 = result["H_tanks_m"]["T1"]
    final_h_t2 = result["H_tanks_m"]["T2"]

    assert final_h_t1 > 55.0
    assert final_h_t2 > 75.0

    # Idéalement, il devrait s'approcher des bornes max (60, 80)
    assert final_h_t1 == pytest.approx(60.0, abs=1)
    assert final_h_t2 == pytest.approx(80.0, abs=1)
