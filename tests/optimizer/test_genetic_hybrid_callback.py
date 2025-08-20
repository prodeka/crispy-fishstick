from __future__ import annotations

from pathlib import Path

from src.lcpi.aep.optimizer.controllers import OptimizationController


def test_ga_hybrid_callback_counts_with_bismark():
	inp = Path("src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp")
	assert inp.exists(), "INP de test manquant"

	controller = OptimizationController()
	res = controller.run_optimization(
		input_path=inp,
		method="genetic",
		solver="lcpi",
		constraints={"pressure_min_m": 10.0, "velocity_max_m_s": 2.0},
		hybrid_refiner="nested",
		hybrid_params={"period": 1, "elite_k": 1},
		algo_params={"dry_run": True},
		price_db=None,
		verbose=False,
	)
	metrics = res.get("metrics", {})
	assert metrics.get("ga_hook_calls", 0) >= 1
	assert metrics.get("hybrid_improved_count", 0) >= 0
