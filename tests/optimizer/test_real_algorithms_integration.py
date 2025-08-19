from pathlib import Path


def test_surrogate_on_bismark_inp(tmp_path: Path):
    from lcpi.aep.optimizer.controllers import OptimizationController
    # Utilise le chemin réel fourni
    project_root = Path(__file__).resolve().parents[2]
    inp = project_root / "src" / "lcpi" / "aep" / "PROTOTYPE" / "INP" / "bismark-Administrator.inp"
    assert inp.exists(), f"INP introuvable: {inp}"

    c = OptimizationController()
    res = c.run_optimization(
        input_path=inp,
        method="surrogate",
        solver="lcpi",
        constraints={"pressure_min_m": 10.0, "velocity_min_m_s": 0.3, "velocity_max_m_s": 2.5},
        algo_params={"surrogate_config": {"initial_samples": 5, "active_learning_rounds": 1, "grid_points": 20}, "dry_run": True}
    )
    assert isinstance(res, dict)
    assert res.get("meta", {}).get("method") == "surrogate"


def test_global_adapter_dry_run(tmp_path: Path):
    from lcpi.aep.optimizer.controllers import OptimizationController
    project_root = Path(__file__).resolve().parents[2]
    inp = project_root / "src" / "lcpi" / "aep" / "PROTOTYPE" / "INP" / "bismark-Administrator.inp"
    c = OptimizationController()
    res = c.run_optimization(
        input_path=inp,
        method="global",
        solver="epanet",
        constraints={"pressure_min_m": 10.0},
        algo_params={"H_bounds": {"R1": (5.0, 20.0)}, "dry_run": True}
    )
    assert isinstance(res, dict)
    assert res.get("meta", {}).get("method") == "global"


def test_multi_tank_adapter(tmp_path: Path):
    from lcpi.aep.optimizer.controllers import OptimizationController
    project_root = Path(__file__).resolve().parents[2]
    inp = project_root / "src" / "lcpi" / "aep" / "PROTOTYPE" / "INP" / "bismark-Administrator.inp"
    c = OptimizationController()
    res = c.run_optimization(
        input_path=inp,
        method="multi-tank",
        solver="epanet",
        constraints={"pressure_min_m": 10.0},
        algo_params={"h_bounds_m": {"R1": (5.0, 20.0), "R2": (5.0, 25.0)}, "max_iterations": 1, "dry_run": True}
    )
    assert isinstance(res, dict)
    assert res.get("meta", {}).get("method") == "multi-tank"


