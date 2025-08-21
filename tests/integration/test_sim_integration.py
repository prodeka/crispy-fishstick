import json
import os
import subprocess
import sys
import tempfile
import pytest


def run_cmd(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


@pytest.mark.integration
def test_no_cache_runs_use_solver(tmp_path):
    # Trouver un .inp minimal pour le test. On utilise un exemple si présent, sinon on skip.
    candidates = [
        os.path.join("examples", "canal.inp"),
        os.path.join("examples", "simple.inp"),
    ]
    inp = None
    for c in candidates:
        if os.path.exists(c):
            inp = c
            break
    if inp is None:
        pytest.skip("Aucun .inp d'exemple disponible pour le test d'intégration")

    out_path = tmp_path / "res.json"
    cmd = (
        f"lcpi aep network-optimize-unified {inp} "
        f"--method genetic --solver epanet --no-cache --no-surrogate "
        f"--generations 3 --population 6 --output {out_path}"
    )
    proc = run_cmd(cmd)
    assert proc.returncode == 0, proc.stderr
    assert out_path.exists(), proc.stderr

    data = json.load(open(out_path, "r", encoding="utf-8"))
    meta = data.get("meta", {})
    assert meta.get("solver_calls", 0) > 0
    assert meta.get("sim_time_seconds_total", 0) > 0.0


