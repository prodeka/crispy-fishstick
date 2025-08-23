# tools/simulate_wntr_sumflows.py
from pathlib import Path
import json
import csv
import argparse

def _safe_float(x):
	try:
		return float(x)
	except Exception:
		return 0.0


def run_wntr_sumflows_and_save(inp_path, artifacts_dir, diameters_map=None, backend='wntr', progress_callback=None, duration_h=None, timestep_min=None, conservation_eps=1e-6):
	"""
	Exécute une simulation WNTR/EPANET, calcule la série temporelle de la somme des débits,
	sauvegarde JSON/CSV/PNG et retourne les chemins des artefacts et un check conservation.
	"""
	artifacts_dir = Path(artifacts_dir)
	artifacts_dir.mkdir(parents=True, exist_ok=True)
	inp_path = Path(inp_path)

	out_json = artifacts_dir / "flows_timeseries.json"
	out_csv = artifacts_dir / "flows_timeseries.csv"
	out_png = artifacts_dir / "flows_timeseries.png"

	try:
		import wntr
	except Exception as e:
		raise RuntimeError("wntr requis pour run_wntr_sumflows_and_save") from e

	wn = wntr.network.WaterNetworkModel(str(inp_path))
	if diameters_map:
		for pid, d in (diameters_map or {}).items():
			try:
				p = wn.get_link(pid)
				if p is not None:
					p.diameter = float(d) / 1000.0
			except Exception:
				continue

	# paramètres par défaut si non fournis
	if duration_h is None:
		try:
			dur_s = getattr(wn.options.time, "duration", 3600)
			duration_h = max(1.0, float(dur_s) / 3600.0)
		except Exception:
			duration_h = 1.0
	if timestep_min is None:
		try:
			step_s = getattr(wn.options.time, "hydraulic_timestep", 300)
			timestep_min = max(1, int(step_s // 60))
		except Exception:
			timestep_min = 5

	SimClass = getattr(wntr.sim, 'EpanetSimulator', None) or getattr(wntr.sim, 'EPANETSimulator', None) or getattr(wntr.sim, 'WNTRSimulator', None)
	if SimClass is None:
		raise RuntimeError("Aucun simulateur WNTR trouvé")

	sim = SimClass(wn)
	try:
		results = sim.run_sim()
	except Exception:
		results = wntr.sim.run_sim(wn, sim)

	# Extraire time series
	times = []
	total_flows = []
	try:
		link_flow_df = results.link['flowrate']
		# index en secondes -> heures
		for idx, row in link_flow_df.iterrows():
			times.append(float(idx) / 3600.0)
			vals = [ _safe_float(v) for v in row.values ]
			total_flows.append(float(sum(vals)))
	except Exception:
		pass

	# Simple conservation check: max |sum(flows)| across timesteps
	max_abs_sum = 0.0
	for v in total_flows:
		if abs(v) > max_abs_sum:
			max_abs_sum = abs(v)
	conservation_ok = (max_abs_sum <= float(conservation_eps))

	payload = {
		"inp_file": str(inp_path),
		"backend": backend,
		"timestep_min": int(timestep_min),
		"duration_h": float(duration_h),
		"times_h": times,
		"sum_flows_m3_s": total_flows,
		"flow_conservation_max_abs_sum": max_abs_sum,
		"flow_conservation_eps": float(conservation_eps),
		"flow_conservation_ok": bool(conservation_ok),
	}

	# JSON
	try:
		with out_json.open("w", encoding="utf-8") as f:
			json.dump(payload, f, indent=2, ensure_ascii=False)
	except Exception:
		pass

	# CSV
	try:
		with out_csv.open("w", newline="", encoding="utf-8") as f:
			w = csv.writer(f)
			w.writerow(["time_h", "sum_flows_m3_s"])
			for t, v in zip(times, total_flows):
				w.writerow([t, v])
	except Exception:
		pass

	# PNG
	try:
		import matplotlib
		matplotlib.use("Agg")
		import matplotlib.pyplot as plt
		plt.figure(figsize=(8,3.5))
		if times and total_flows:
			plt.plot(times, total_flows, marker="o", linewidth=1)
			plt.xlabel("Temps (h)")
			plt.ylabel("Somme des débits (m3/s)")
			plt.title("Somme des débits dans le réseau")
			plt.grid(True, linestyle='--', alpha=0.6)
			plt.tight_layout()
			plt.savefig(str(out_png), dpi=150)
			plt.close()
	except Exception:
		pass

	return {"json": out_json, "csv": out_csv, "png": out_png, "flow_conservation_ok": conservation_ok, "flow_conservation_max_abs_sum": max_abs_sum}


def _derive_png_path(json_path: Path = None, csv_path: Path = None) -> Path:
	try:
		if json_path:
			stem = json_path.stem
			base = json_path.with_name(f"{stem}_flow.png")
			return base
	except Exception:
		pass
	try:
		if csv_path:
			stem = csv_path.stem
			if stem.endswith("_flows"):
				stem = stem[:-1]
			base = csv_path.with_name(f"{stem}.png")
			return base
	except Exception:
		pass
	return Path("flows_timeseries.png")


def main_cli():
	parser = argparse.ArgumentParser(description="Simuler un INP avec WNTR/EPANET et exporter la somme des débits (JSON/CSV/PNG)")
	parser.add_argument("--inp", required=True, help="Chemin du fichier .inp")
	parser.add_argument("--out", required=False, help="Chemin du JSON de sortie (ex: artifacts/sim_one.json)")
	parser.add_argument("--csv", dest="csv_out", required=False, help="Chemin du CSV de sortie (ex: artifacts/sim_one_flows.csv)")
	parser.add_argument("--png", dest="png_out", required=False, help="Chemin du PNG de sortie (ex: artifacts/sim_one_flow.png)")
	parser.add_argument("--artifacts", required=False, help="Dossier d'artefacts si --out/--csv non fournis", default=None)
	parser.add_argument("--backend", required=False, default="wntr")
	args = parser.parse_args()

	inp_path = Path(args.inp)
	if args.out:
		art_dir = Path(args.out).parent
	elif args.csv_out:
		art_dir = Path(args.csv_out).parent
	elif args.artifacts:
		art_dir = Path(args.artifacts)
	else:
		art_dir = Path("artifacts")
	art_dir.mkdir(parents=True, exist_ok=True)

	res = run_wntr_sumflows_and_save(inp_path, art_dir, backend=args.backend)

	try:
		if args.out:
			target_json = Path(args.out)
			target_json.parent.mkdir(parents=True, exist_ok=True)
			if Path(res["json"]) != target_json:
				target_json.write_text(Path(res["json"]).read_text(encoding="utf-8"), encoding="utf-8")
			res["json"] = target_json
	except Exception:
		pass

	try:
		if args.csv_out:
			target_csv = Path(args.csv_out)
			target_csv.parent.mkdir(parents=True, exist_ok=True)
			if Path(res["csv"]) != target_csv:
				target_csv.write_text(Path(res["csv"]).read_text(encoding="utf-8"), encoding="utf-8")
			res["csv"] = target_csv
	except Exception:
		pass

	try:
		target_png = None
		if args.png_out:
			target_png = Path(args.png_out)
		elif args.out:
			target_png = _derive_png_path(json_path=Path(args.out))
		elif args.csv_out:
			target_png = _derive_png_path(csv_path=Path(args.csv_out))
		if target_png is not None:
			target_png.parent.mkdir(parents=True, exist_ok=True)
			src_png = Path(res["png"]) if res.get("png") else None
			if src_png and src_png.exists() and src_png != target_png:
				target_png.write_bytes(src_png.read_bytes())
			res["png"] = target_png
	except Exception:
		pass

	try:
		print(json.dumps({"json": str(res.get("json")), "csv": str(res.get("csv")), "png": str(res.get("png")), "flow_conservation_ok": bool(res.get("flow_conservation_ok"))}, indent=2))
	except Exception:
		pass


if __name__ == "__main__":
	main_cli()
