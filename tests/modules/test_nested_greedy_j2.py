import pytest
from pathlib import Path

try:
	from lcpi.aep.optimizer.algorithms.nested import NestedGreedyOptimizer
	from lcpi.aep.optimizer.io import NetworkModel
	PKG_OK = True
except Exception:
	PKG_OK = False


@pytest.mark.skipif(not PKG_OK, reason="lcpi package not importable in current environment")
def test_nested_greedy_basic_capex():
	nm = NetworkModel(
		nodes={"n1": {"elevation_m": 0.0}, "n2": {"elevation_m": 5.0}},
		links={"p1": {"from": "n1", "to": "n2", "length_m": 150.0, "diameter_mm": 110}},
		tanks={"t0": {"radier_elevation_m": 70.0, "init_level_m": 2.0}},
	)

	res = NestedGreedyOptimizer(nm).optimize_nested(
		H_bounds=(50.0, 80.0),
		pressure_min_m=12.0,
		velocity_constraints={"min_m_s": 0.3, "max_m_s": 2.5},
		diameter_db_path=str(Path("project/data/diameters.yml")),
	)

	assert res["feasible"] is True
	assert "H_tank_m" in res and 50.0 <= res["H_tank_m"] <= 80.0
	assert "diameters_mm" in res and isinstance(res["diameters_mm"], dict)
	assert "costs" in res and res["costs"]["CAPEX"] >= 0.0

