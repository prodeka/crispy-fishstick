#!/usr/bin/env python3
"""
lcpi_diagnostics.py
Script d'audit rapide pour vérifier si `lcpi aep network-optimize-unified`
lance réellement le solveur EPANET / effectue des évaluations, ou si le run est
court-circuité (cache / surrogate / mock).

Usage:
    python tools/lcpi_diagnostics.py --input examples/test_network.inp --verbose
"""

import argparse
import json
import shutil
import subprocess
import time
import sys
from pathlib import Path
import os


def run_cmd(cmd, env=None, timeout=None):
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=timeout)
    dt = time.time() - t0
    return proc.returncode, proc.stdout + proc.stderr, dt


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None


def print_section(title):
    print("\n" + "=" * len(title))
    print(title)
    print("=" * len(title))


def find_lcpi_command() -> list[str]:
    # Forcer l'utilisation du wrapper local pour éviter les soucis de PATH
    repo_root = Path(__file__).resolve().parents[1]
    candidate = repo_root / "scripts" / "lcpi.py"
    if candidate.exists():
        return [sys.executable, str(candidate)]
    # Fallback: binaire lcpi si présent, sinon module
    if shutil.which("lcpi"):
        return ["lcpi"]
    return [sys.executable, "-m", "lcpi.main"]


def main():
    parser = argparse.ArgumentParser(description="Diagnostic LCPI: vérifie solver calls, cache, surrogate, timings")
    parser.add_argument("--input", "-i", required=True, help="Fichier .inp ou .yml")
    parser.add_argument("--out", "-o", default=str((Path("temp") / "lcpi_diag_out.json").resolve()), help="Fichier de sortie JSON produit par LCPI")
    parser.add_argument("--runs", type=int, default=1, help="Nombre d'itérations rapide")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_json = Path(args.out)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    lcpi_cmd = find_lcpi_command()

    # Ajouter scripts/ au PATH pour PowerShell si nécessaire
    env = os.environ.copy()
    repo_root = Path(__file__).resolve().parents[1]
    scripts_dir = repo_root / "scripts"
    env["PATH"] = str(scripts_dir) + os.pathsep + env.get("PATH", "")

    # Construire trois variantes de commande: wrapper, module direct, binaire
    cmd_base_common = [
        "network-optimize-unified",
        str(input_path),
        "--solver", "epanet",
        "--method", "genetic",
        "--verbose",
        "--no-log",
        "--output", str(out_json)
    ]
    # 1) Wrapper: scripts/lcpi.py aep ...
    cmd_variant_1 = lcpi_cmd + ["aep"] + cmd_base_common
    # 2) Module direct: python -m lcpi.aep.cli ...
    cmd_variant_2 = [sys.executable, "-m", "lcpi.aep.cli"] + cmd_base_common
    # 3) Binaire lcpi si dispo
    cmd_variant_3 = ["lcpi", "aep"] + cmd_base_common if shutil.which("lcpi") else None

    print_section("RUN 1 - baseline (genetic, solver=epanet)")
    # Nettoyer l'ancien JSON
    try:
        if out_json.exists():
            out_json.unlink()
    except Exception:
        pass
    # Essayer les variantes jusqu'à succès
    rc = 1
    out = ""
    dt = 0.0
    for cmd in (cmd_variant_1, cmd_variant_2, cmd_variant_3):
        if not cmd:
            continue
        rc, out, dt = run_cmd(cmd, env=env, timeout=600)
        if rc == 0 and out_json.exists():
            break
    print(f"Return code: {rc}  | Duration: {dt:.2f}s")
    if args.verbose:
        print(out[:2000])

    data1 = load_json(out_json)
    if not data1:
        print("⚠️  Aucun JSON produit par LCPI (vérifier logs).")
    else:
        print("Meta fields:", list(data1.get("meta", {}).keys()))
        meta = data1.get("meta", {})
        print("meta.duration_seconds:", meta.get("duration_seconds"))
        print("meta.solver_calls:", meta.get("solver_calls"))
        print("meta.eval_count:", meta.get("eval_count"))
        print("meta.cache_hit:", meta.get("cache_hit"))
        print("meta.surrogate_used:", meta.get("surrogate_used"))

    # Run 2
    print_section("RUN 2 - no-cache / no-surrogate (if supported)")
    try:
        if out_json.exists():
            out_json.unlink()
    except Exception:
        pass
    cmd_nc_suffix = ["--no-cache", "--no-surrogate", "--generations", "80", "--population", "60"]
    rc = 1
    out = ""
    dt = 0.0
    for base in (cmd_variant_1, cmd_variant_2, cmd_variant_3):
        if not base:
            continue
        cmd_nc = base + cmd_nc_suffix
        rc, out, dt = run_cmd(cmd_nc, env=env, timeout=1800)
        if rc == 0 and out_json.exists():
            break
    print(f"Return code: {rc}  | Duration: {dt:.2f}s")
    data2 = load_json(out_json)
    if data2:
        meta = data2.get("meta", {})
        print("meta.duration_seconds:", meta.get("duration_seconds"))
        print("meta.solver_calls:", meta.get("solver_calls"))
        print("meta.eval_count:", meta.get("eval_count"))
        print("meta.cache_hit:", meta.get("cache_hit"))
        print("meta.surrogate_used:", meta.get("surrogate_used"))

    # Run 3
    print_section("RUN 3 - stress GA (generations=150, population=100)")
    try:
        if out_json.exists():
            out_json.unlink()
    except Exception:
        pass
    cmd_big_suffix = ["--no-cache", "--no-surrogate", "--generations", "150", "--population", "100"]
    rc = 1
    out = ""
    dt = 0.0
    for base in (cmd_variant_1, cmd_variant_2, cmd_variant_3):
        if not base:
            continue
        cmd_big = base + cmd_big_suffix
        rc, out, dt = run_cmd(cmd_big, env=env, timeout=7200)
        if rc == 0 and out_json.exists():
            break
    print(f"Return code: {rc}  | Duration: {dt:.2f}s")
    data3 = load_json(out_json)
    if data3:
        meta = data3.get("meta", {})
        print("meta.duration_seconds:", meta.get("duration_seconds"))
        print("meta.solver_calls:", meta.get("solver_calls"))
        print("meta.eval_count:", meta.get("eval_count"))
        print("meta.cache_hit:", meta.get("cache_hit"))
        print("meta.surrogate_used:", meta.get("surrogate_used"))

    # Heuristique
    print_section("RAPPORT SYNTHÉTIQUE")
    suspect = False
    for idx, d in enumerate((data1, data2, data3), start=1):
        if not d:
            print(f"Run{idx}: PAS DE JSON")
            suspect = True
            continue
        m = d.get("meta", {})
        dur = m.get("duration_seconds") or 0
        sc = m.get("solver_calls") or 0
        ec = m.get("eval_count") or 0
        su = m.get("surrogate_used")
        ch = m.get("cache_hit")
        print(f"Run{idx}: duration={dur}s, solver_calls={sc}, eval_count={ec}, surrogate={su}, cache_hit={ch}")
        if dur < 2 and sc == 0 and not su:
            print(" --> SUSPICION: run très court sans appel solver ni surrogate.")
            suspect = True

    if suspect:
        print("\nWARNING: Il y a des indices qu'un court-circuit (cache/mock/surrogate non validé) est en place. Voir logs et instrumentation.")
    else:
        print("\nOK: Les runs semblent effectuer des évaluations / appels solver.")


if __name__ == "__main__":
    main()


