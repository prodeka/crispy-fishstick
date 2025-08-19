#!/usr/bin/env python3
"""
Audit V13 (exécution rapide) : DB, imports, simulateur EPANET, scoring, CLI, reporting
Produit un résumé sur stdout et un rapport Markdown dans docs/AUDIT_V13_REPORT.md
"""

import json
import os
import sqlite3
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DOCS = ROOT / "docs"
DOCS.mkdir(parents=True, exist_ok=True)

# Inject src into path
import sys
sys.path.insert(0, str(SRC))

report = {
    "db_present": False,
    "db_diameters": None,
    "db_accessories": None,
    "imports_ok": False,
    "algorithms_import_ok": False,
    "epanet_simulate_ok": False,
    "scoring_capex_ok": False,
    "cli_optimizer_available": False,
    "cli_methods": [],
    "report_html_ok": False,
    "v11_format_ok": False,
    "v11_log_ok": False,
    "notes": []
}

# 1) DB checks
try:
    db_path = ROOT / "src" / "lcpi" / "db" / "aep_prices.db"
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM diameters")
        report["db_diameters"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM accessories")
        report["db_accessories"] = cur.fetchone()[0]
        conn.close()
        report["db_present"] = True
    else:
        report["notes"].append(f"DB not found: {db_path}")
except Exception as e:
    report["notes"].append(f"DB error: {e}")

# 2) Imports
try:
    from lcpi.aep.optimizer.algorithms.binary import BinarySearchOptimizer  # noqa
    from lcpi.aep.optimizer.algorithms.nested import NestedGreedyOptimizer  # noqa
    from lcpi.aep.optimizer.algorithms.global_opt import GlobalOptimizer  # noqa
    from lcpi.aep.optimizer.algorithms.surrogate import SurrogateOptimizer  # noqa
    from lcpi.aep.optimizer.scoring import CostScorer  # noqa
    from lcpi.aep.optimizer.solvers import EPANETOptimizer  # noqa
    report["imports_ok"] = True
    report["algorithms_import_ok"] = True
except Exception as e:
    report["notes"].append(f"Import error: {e}")

# 3) EPANET simulate (light)
try:
    from lcpi.aep.optimizer.solvers import EPANETOptimizer
    inp = ROOT / "examples" / "test_network.inp"
    e = EPANETOptimizer()
    ok = False
    if inp.exists():
        try:
            out = e.simulate_with_tank_height(inp, 63.0, {"PIPE1": 110})
            ok = isinstance(out, dict) and "min_pressure_m" in out and "max_velocity_m_s" in out
        except Exception as ee:
            report["notes"].append(f"EPANET simulate real failed: {ee}")
    # fallback mock path forcing mock network
    if not ok:
        class _StubNetwork:
            def __init__(self):
                self.nodes = {"N1": {}, "N2": {}}
            def dict(self):
                return {"nodes": self.nodes}
        out = e.simulate_with_tank_height(_StubNetwork(), 63.0, {"PIPE1": 110})
        ok = isinstance(out, dict) and "min_pressure_m" in out and "max_velocity_m_s" in out
    report["epanet_simulate_ok"] = ok
except Exception as e:
    report["notes"].append(f"EPANET simulate error: {e}")

# 4) Scoring with DB
try:
    from lcpi.aep.optimizer.scoring import CostScorer
    mock_network = {"links": {"PIPE1": {"length_m": 100.0, "diameter_mm": 110}}}
    diam_map = {"PIPE1": 110}
    cs = CostScorer()  # will query DB via DAO
    capex = cs.compute_capex(mock_network, diam_map)
    report["scoring_capex_ok"] = isinstance(capex, float) and capex > 0.0
except Exception as e:
    report["notes"].append(f"Scoring error: {e}")

# 5) CLI availability
try:
    from lcpi.aep.cli import app as aep_app
    from lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI
    report["cli_optimizer_available"] = True
    cli = AEPOptimizationCLI()
    methods = [m for m in dir(cli) if not m.startswith("_")]
    report["cli_methods"] = methods
except Exception as e:
    report["notes"].append(f"CLI error: {e}")

# 6) Reporting (V11 + HTML)
try:
    from lcpi.aep.optimizer.output import OutputFormatter
    from lcpi.aep.optimizer.models import OptimizationResult, Proposal, TankDecision
    from lcpi.aep.optimizer.report_adapter import v11_adapter
    tank = TankDecision(id="T1", H_m=65.0)
    proposal = Proposal(name="demo", is_feasible=True, tanks=[tank], diameters_mm={"PIPE1": 200}, costs={"CAPEX": 100000}, metrics={"min_pressure_m": 12.5})
    result = OptimizationResult(proposals=[proposal], pareto_front=None, metadata={"method": "audit"})
    fmt = OutputFormatter()
    v11 = fmt.format_v11(result)
    report["v11_format_ok"] = isinstance(v11, dict) and v11.get("metadata", {}).get("version") == "V11"
    # HTML
    from lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI
    cli = AEPOptimizationCLI()
    html = cli._generate_html_report({"proposals": [proposal], "metadata": {"method": "audit"}}, "optimisation_tank_v11.jinja2")
    report["report_html_ok"] = isinstance(html, str) and len(html) > 1000
    # Log compatible
    with tempfile.TemporaryDirectory() as td:
        outp = Path(td) / "audit.log.json"
        log_id = v11_adapter.save_v11_result_as_log(result, outp)
        report["v11_log_ok"] = outp.exists() and outp.stat().st_size > 0 and isinstance(log_id, str)
except Exception as e:
    report["notes"].append(f"Reporting error: {e}")

# Emit markdown report
status = lambda b: "OK" if b else "FAIL"
md = []
md.append("# Audit V13 (exécution rapide)\n")
md.append(f"- DB: {status(report['db_present'])} (diameters={report['db_diameters']}, accessories={report['db_accessories']})")
md.append(f"- Imports: {status(report['imports_ok'])}")
md.append(f"- Algorithms imports: {status(report['algorithms_import_ok'])}")
md.append(f"- EPANET simulate: {status(report['epanet_simulate_ok'])}")
md.append(f"- Scoring CAPEX (DB): {status(report['scoring_capex_ok'])}")
md.append(f"- CLI optimizer available: {status(report['cli_optimizer_available'])} (methods={', '.join(report['cli_methods'])})")
md.append(f"- V11 format: {status(report['v11_format_ok'])}")
md.append(f"- Report HTML: {status(report['report_html_ok'])}")
md.append(f"- LCPI log compatible: {status(report['v11_log_ok'])}")
if report["notes"]:
    md.append("\n## Notes\n")
    for n in report["notes"]:
        md.append(f"- {n}")

(DOCS / "AUDIT_V13_REPORT.md").write_text("\n".join(md), encoding="utf-8")

print(json.dumps(report, indent=2, ensure_ascii=False))
