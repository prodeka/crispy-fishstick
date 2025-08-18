import pytest

try:
	from lcpi.aep.optimizer.algorithms.surrogate import SurrogateOptimizer
	from lcpi.aep.optimizer.io import NetworkModel
	PKG_OK = True
except Exception:
	PKG_OK = False


@pytest.mark.skipif(not PKG_OK, reason="lcpi package not importable in current environment")
def test_surrogate_build_and_optimize_runs():
	nm = NetworkModel(
		nodes={"n1": {"elevation_m": 0.0}, "n2": {"elevation_m": 5.0}},
		links={"p1": {"from": "n1", "to": "n2", "length_m": 150.0, "diameter_mm": 110}},
		tanks={"t0": {"radier_elevation_m": 70.0, "init_level_m": 2.0}},
	)
	op = SurrogateOptimizer(nm, solver="lcpi")
	res = op.build_and_optimize((50.0, 80.0), n_initial=10, top_k=3, rounds=1, pressure_min_m=0.0, grid_points=50)
	assert isinstance(res, dict)
	assert "H_selected" in res
	assert 50.0 <= float(res["H_selected"]) <= 80.0

