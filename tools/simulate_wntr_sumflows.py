# tools/simulate_wntr_sumflows.py
from pathlib import Path
import json
import csv

def _safe_float(x):
	try:
		return float(x)
	except Exception:
		return 0.0


def run_wntr_sumflows_and_save(inp_path, artifacts_dir, diameters_map=None, backend='wntr', progress_callback=None, duration_h=None, timestep_min=None):
	"""
	Exécute une simulation WNTR/EPANET, calcule la série temporelle de la somme des débits,
	sauvegarde JSON/CSV/PNG et retourne les chemins des artefacts.
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

	payload = {
		"inp_file": str(inp_path),
		"backend": backend,
		"timestep_min": int(timestep_min),
		"duration_h": float(duration_h),
		"times_h": times,
		"sum_flows_m3_s": total_flows,
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

	return {"json": out_json, "csv": out_csv, "png": out_png}
