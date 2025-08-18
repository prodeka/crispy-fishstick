import pytest

try:
	from lcpi.aep.optimizer.algorithms.multi_tank import MultiTankOptimizer
	from lcpi.aep.optimizer.io import NetworkModel
	PKG_OK = True
except Exception:
	PKG_OK = False


@pytest.mark.skipif(not PKG_OK, reason="lcpi package not importable")
def test_multi_tank_coordinate_descent_runs():
	nm = NetworkModel(
		nodes={"n1": {"elevation_m": 0.0}, "n2": {"elevation_m": 5.0}},
		links={"p1": {"from": "n1", "to": "n2", "length_m": 150.0, "diameter_mm": 110}},
		tanks={"tA": {"radier_elevation_m": 70.0, "init_level_m": 2.0}, "tB": {"radier_elevation_m": 60.0, "init_level_m": 2.0}},
	)
	op = MultiTankOptimizer(nm, solver="lcpi")
	res = op.optimize({"tA": (50.0, 80.0), "tB": (45.0, 70.0)}, pressure_min_m=10.0)
	assert isinstance(res, dict) and res.get("feasible") in (True, False)

