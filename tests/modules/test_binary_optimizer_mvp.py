from pathlib import Path

from lcpi.aep.optimizer.algorithms.binary import BinarySearchOptimizer
from lcpi.aep.optimizer.io import NetworkModel


def test_binary_converges_simple_case():
    nm = NetworkModel(
        nodes={"n1": {"elevation_m": 0.0}, "n2": {"elevation_m": 5.0}},
        links={"p1": {"length_m": 100.0, "diameter_mm": 110}},
        tanks={"t1": {"radier_elevation_m": 70.0}},
    )
    opt = BinarySearchOptimizer(nm, pressure_min_m=10.0)
    res = opt.optimize_tank_height(50.0, 80.0, tolerance=0.1, max_iter=50)
    assert res["feasible"] is True
    assert 50.0 <= res["H_tank_m"] <= 80.0


