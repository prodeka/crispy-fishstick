from pathlib import Path


def _make_dummy_inp(tmp_path: Path) -> Path:
    content = """
[JUNCTIONS]
;ID               Elevation  Demand    Pattern
 N1               0          0
 N2               0          0

[PIPES]
;ID               Node1      Node2      Length     Diameter   Roughness  MinorLoss  Status
 P1               N1         N2         100        110        100        0          Open
""".strip()
    p = tmp_path / "net.inp"
    p.write_text(content)
    return p


def test_method_routing_genetic(tmp_path: Path):
    from lcpi.aep.optimizer.controllers import OptimizationController
    net = _make_dummy_inp(tmp_path)

    c = OptimizationController()
    res = c.run_optimization(
        input_path=net,
        method="genetic",  # doit router vers nested en fallback mais conserver meta.method demandé
        solver="mock",
        constraints={"pressure_min_m": 10.0, "velocity_min_m_s": 0.3, "velocity_max_m_s": 2.0},
        algo_params={}
    )

    assert isinstance(res, dict)
    assert res.get("meta", {}).get("method") == "genetic"


def test_penalty_applied_on_vmax(tmp_path: Path):
    from lcpi.aep.optimizer.controllers import OptimizationController
    net = _make_dummy_inp(tmp_path)
    c = OptimizationController()

    base = c.run_optimization(
        input_path=net,
        method="nested",
        solver="mock",
        constraints={"pressure_min_m": 10.0, "velocity_min_m_s": 0.0, "velocity_max_m_s": 10.0},
        algo_params={"penalty_weight": 1e3, "penalty_beta": 1.0},
    )
    pen = c.run_optimization(
        input_path=net,
        method="nested",
        solver="mock",
        constraints={"pressure_min_m": 10.0, "velocity_min_m_s": 0.0, "velocity_max_m_s": 0.0001},
        algo_params={"penalty_weight": 1e3, "penalty_beta": 1.0},
    )

    # Récupérer premier CAPEX si disponible
    def get_capex(res):
        props = res.get("proposals") or []
        return (props[0] or {}).get("CAPEX") if props else None

    cap_base = get_capex(base)
    cap_pen = get_capex(pen)

    # Si CAPEX disponibles, vérifier qu'il augmente avec la pénalité
    if cap_base is not None and cap_pen is not None:
        assert float(cap_pen) >= float(cap_base)


def test_hybridation_topk_metrics_present(tmp_path: Path):
    from lcpi.aep.optimizer.controllers import OptimizationController
    net = _make_dummy_inp(tmp_path)
    c = OptimizationController()

    res = c.run_optimization(
        input_path=net,
        method="nested",
        solver="mock",
        constraints={"pressure_min_m": 10.0, "velocity_min_m_s": 0.3, "velocity_max_m_s": 2.0},
        hybrid_refiner="nested",
        hybrid_params={"topk": 1, "steps": 1},
        algo_params={}
    )

    metrics = res.get("metrics", {})
    # La métrique doit exister même si aucune amélioration n'est faite
    assert "hybrid_improved_count" in metrics


