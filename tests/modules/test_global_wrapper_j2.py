import pytest

try:
	from lcpi.aep.optimizer.algorithms.global_opt import GlobalOptimizer
	PKG_OK = True
except Exception:
	PKG_OK = False


@pytest.mark.skipif(not PKG_OK, reason="lcpi package not importable in current environment")
def test_global_wrapper_initialization():
	cfg = {"criteres": {"principal": "cout", "secondaires": [], "poids": [1.0]}, "algorithme": {"generations": 1, "population_size": 20}}
	opt = GlobalOptimizer(cfg)
	assert opt is not None
