from __future__ import annotations

from pathlib import Path

from src.lcpi.aep.optimizer.controllers import OptimizationController


def test_price_db_provenance_and_capex():
	inp = Path("src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp")
	assert inp.exists(), "INP de test manquant"

	controller = OptimizationController()
	# Utilise un fichier DB factice uniquement pour la provenance/checksum
	fake_db = inp.parent / "_fake_prices.db"
	fake_db.write_bytes(b"\x01") if not fake_db.exists() else None
	res = controller.run_optimization(
		input_path=inp,
		method="nested",
		solver="lcpi",
		constraints={"pressure_min_m": 10.0, "velocity_max_m_s": 2.0},
		hybrid_refiner=None,
		hybrid_params=None,
		algo_params={"H_bounds": (5.0, 10.0)},
		price_db=str(fake_db),
		verbose=False,
	)
	meta = res.get("meta", {})
	assert "price_db_info" in meta and "checksum" in meta["price_db_info"]
	props = res.get("proposals") or []
	if props:
		capex = props[0].get("CAPEX")
		assert isinstance(capex, (int, float))


def test_metrics_presence_in_proposals():
	inp = Path("src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp")
	assert inp.exists(), "INP de test manquant"
	controller = OptimizationController()
	res = controller.run_optimization(
		input_path=inp,
		method="nested",
		solver="lcpi",
		constraints={"pressure_min_m": 10.0, "velocity_max_m_s": 2.0},
		hybrid_refiner=None,
		hybrid_params=None,
		algo_params={"H_bounds": (5.0, 10.0)},
		price_db=None,
		verbose=False,
	)
	props = res.get("proposals") or []
	if props:
		metrics = props[0].get("metrics", {})
		assert "min_pressure_m" in metrics and "max_velocity_m_s" in metrics


