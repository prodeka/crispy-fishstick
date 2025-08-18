import pytest

try:
	from lcpi.aep.optimizer.pareto import compute_pareto, knee_point
	PKG_OK = True
except Exception:
	PKG_OK = False


@pytest.mark.skipif(not PKG_OK, reason="lcpi package not importable in current environment")
def test_compute_pareto_and_knee():
    points = [
        {"CAPEX": 100, "OPEX": 1000},
        {"CAPEX": 120, "OPEX": 800},
        {"CAPEX": 90, "OPEX": 1200},
        {"CAPEX": 150, "OPEX": 700},
    ]
    p = compute_pareto(points)
    assert isinstance(p, list) and len(p) >= 2
    k = knee_point(p)
    assert k is None or ("CAPEX" in k and "OPEX" in k)


