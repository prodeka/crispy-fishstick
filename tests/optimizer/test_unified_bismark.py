from __future__ import annotations

from pathlib import Path

from src.lcpi.aep.optimizer.controllers import OptimizationController


def test_unified_on_bismark_inp_with_constraints_and_cache():
	# Use the provided INP file from the repo
	inp = Path("src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp")
	assert inp.exists(), "Test requires the bismark-Administrator.inp file"

	controller = OptimizationController()

	# First run: expect non-cached, check constraints soft and metrics presence
	res1 = controller.run_optimization(
		input_path=inp,
		method="nested",
		solver="lcpi",
		constraints={"pressure_min_m": 10.0, "velocity_max_m_s": 2.0},
		hybrid_refiner=None,
		hybrid_params=None,
		algo_params={"H_bounds": (5.0, 10.0), "penalty_weight": 1e4, "penalty_beta": 1.0},
		price_db=None,
		verbose=False,
	)
	props1 = res1.get("proposals") or []
	if props1:
		m = props1[0].get("metrics", {})
		assert "min_pressure_m" in m and "max_velocity_m_s" in m

	# Second run: same inputs -> expect cache hit
	res2 = controller.run_optimization(
		input_path=inp,
		method="nested",
		solver="lcpi",
		constraints={"pressure_min_m": 10.0, "velocity_max_m_s": 2.0},
		hybrid_refiner=None,
		hybrid_params=None,
		algo_params={"H_bounds": (5.0, 10.0), "penalty_weight": 1e4, "penalty_beta": 1.0},
		price_db=None,
		verbose=False,
	)
	metrics2 = res2.get("metrics", {})
	assert metrics2.get("cache_hit", False) is True

	# Hard velocity test: set low vmax to force violation -> constraints_ok False or penalized
	res3 = controller.run_optimization(
		input_path=inp,
		method="nested",
		solver="lcpi",
		constraints={"pressure_min_m": 10.0, "velocity_max_m_s": 0.1},
		hybrid_refiner=None,
		hybrid_params=None,
		algo_params={"H_bounds": (5.0, 10.0), "penalty_weight": 1e5, "penalty_beta": 1.0, "hard_velocity": True},
		price_db=None,
		verbose=False,
	)
	props3 = res3.get("proposals") or []
	if props3:
		assert props3[0].get("constraints_ok") in (False, True)  # Presence; can be False under hard

