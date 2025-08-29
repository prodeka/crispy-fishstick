#!/usr/bin/env python3
"""
Run Optimization Tests v2 (EPANET only) - Sequential, concise output like compare_solvers.

- Reads param combinations from a config JSON (default: optimization_test_config.json)
- Runs lcpi.aep.cli network-optimize-unified with --solver epanet and --no-log
- Sequential execution; prints a short summary per run from the resulting JSON
- Saves outputs to test_runs/<run_name>_<timestamp>.json

Usage:
  python tools/run_optimization_test_v2.py --config optimization_test_config.json
"""

import argparse
import json
import os
import sys
import subprocess
import datetime
from pathlib import Path
from typing import Dict, Any, List

# Forcer UTF-8 sur Windows pour ce processus et les sous-processus
if sys.platform == "win32":
	try:
		import codecs
		# Rediriger stdout/stderr en UTF-8 si possible
		if hasattr(sys.stdout, "detach"):
			sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
		if hasattr(sys.stderr, "detach"):
			sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
	except Exception:
		pass
	# Variables d'environnement pour UTF-8
	os.environ["PYTHONIOENCODING"] = "utf-8"
	os.environ["PYTHONLEGACYWINDOWSSTDIO"] = "utf-8"
	os.environ["PYTHONUTF8"] = "1"
	# Basculer la console en CP65001 (UTF-8)
	try:
		os.system("chcp 65001 >NUL")
	except Exception:
		pass

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified"]
DEFAULT_CONFIG = "optimization_test_config.json"


def load_config(path: str) -> Dict[str, Any]:
	cfg_path = Path(path)
	if not cfg_path.exists():
		# minimal default
		return {
			"output_dir": "test_runs",
			"cli_script": [sys.executable, "-m", "lcpi.aep.cli"],
			"input_network_file": "bismark_inp.inp",
			"max_workers": 1,
			"param_combinations": [
				{"generations": 10, "population": 20, "hmax": 100, "run_name": "gen10_pop20_hmax100"}
			]
		}
	with open(cfg_path, "r", encoding="utf-8") as f:
		return json.load(f)


def ensure_output_dir(path: str) -> Path:
	out = ROOT / path
	out.mkdir(parents=True, exist_ok=True)
	return out


def build_command(args_cfg: Dict[str, Any], params: Dict[str, Any], output_file: Path) -> List[str]:
	cmd = CLI + [
		str((ROOT / args_cfg["input_network_file"]).resolve()),
		"--method", "genetic",
		"--generations", str(params["generations"]),
		"--population", str(params["population"]),
		"--solver", "epanet",
		"--hmax", str(params["hmax"]),
		"--output", str(output_file),
		"--no-log",
		"--show-stats",
		"--verbose",
	]
	# optionals
	if "demand" in params:
		cmd += ["--demand", str(params["demand"])]
	if "mutation_rate" in params:
		cmd += ["--mutation-rate", str(params["mutation_rate"])]
	if "crossover_rate" in params:
		cmd += ["--crossover-rate", str(params["crossover_rate"])]
	if "elite_size" in params:
		cmd += ["--elite-size", str(params["elite_size"])]
	return cmd


def run_once(args_cfg: Dict[str, Any], params: Dict[str, Any], out_dir: Path) -> Path:
	stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
	out_path = out_dir / f"{params['run_name']}_{stamp}.json"
	cmd = build_command(args_cfg, params, out_path)
	print(f"\n➡️ Run: {params['run_name']}\n   Cmd: {' '.join(cmd)}")
	# Préparer environnement UTF-8 pour le sous-processus
	env = os.environ.copy()
	env["PYTHONIOENCODING"] = "utf-8"
	env["PYTHONLEGACYWINDOWSSTDIO"] = "utf-8"
	env["PYTHONUTF8"] = "1"
	# capture output to avoid spinners; show nothing unless error
	completed = subprocess.run(cmd, env=env, check=True)
	# si check=True ne lève pas d'exception, on considère réussi
	print(f"✅ Terminé: {params['run_name']} -> {out_path}")
	return out_path


def summarize(result_path: Path) -> None:
	if not result_path.exists():
		print(f"⚠️ Fichier manquant: {result_path}")
		return
	try:
		with open(result_path, "r", encoding="utf-8") as f:
			data = json.load(f)
		meta = data.get("meta", {})
		props = data.get("proposals", [])
		best = props[0] if props else {}
		best_cost = meta.get("best_cost", best.get("CAPEX"))
		constraints_ok = best.get("constraints_ok")
		solver = meta.get("solver")
		gens = meta.get("generations")
		pop = meta.get("population")
		print(f"   Solver: {solver} | Generations: {gens} | Population: {pop}")
		print(f"   Best CAPEX: {best_cost:,} FCFA | Feasible: {constraints_ok}")
	except Exception as e:
		print(f"⚠️ Erreur lecture JSON: {result_path} -> {e}")


def main():
	parser = argparse.ArgumentParser(description="Run multiple EPANET optimizations sequentially")
	parser.add_argument("--config", "-c", default=DEFAULT_CONFIG)
	args = parser.parse_args()

	cfg = load_config(args.config)
	inp = cfg["input_network_file"]
	if not (ROOT / inp).exists():
		print(f"❌ Fichier réseau introuvable: {inp}")
		sys.exit(1)

	out_dir = ensure_output_dir(cfg.get("output_dir", "test_runs"))
	param_combos = cfg.get("param_combinations", [])
	if not param_combos:
		print("❌ Aucune combinaison de paramètres trouvée dans la config")
		sys.exit(1)

	print("🚀 Exécutions séquentielles EPANET")
	print(f"📁 Sortie: {out_dir}")
	print(f"🗂️ Réseau: {inp}")
	print(f"🔢 Runs: {len(param_combos)}")

	results: List[Path] = []
	for params in param_combos:
		p = run_once(cfg, params, out_dir)
		results.append(p)
		# summary
		summarize(p)

	print("\n🎯 Tous les runs sont terminés.")
	print("📄 Fichiers JSON:")
	for p in results:
		print(f" - {p}")


if __name__ == "__main__":
	main()
