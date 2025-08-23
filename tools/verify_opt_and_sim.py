#!/usr/bin/env python3
"""
tools/verify_opt_and_sim.py
Script de vérification automatisée pour les runs d'optimisation + simulation.
Usage: python tools/verify_opt_and_sim.py
Sorties:
 - temp/verification/out_opt_500.json
 - temp/verification/out_opt_600.json
 - temp/verification/sim_500.json
 - temp/verification/sim_600.json
 - temp/verification/plots/* (png)
 - temp/verification/verification_report.md
"""
import os
import subprocess
import json
import sys
from pathlib import Path
import shutil
import math

ROOT = Path.cwd()
TMP = ROOT / "temp" / "verification"
PLOTS = TMP / "plots"
TMP.mkdir(parents=True, exist_ok=True)
PLOTS.mkdir(parents=True, exist_ok=True)

# Commands (Windows-friendly single-line)
OPT_CMD_TEMPLATE = (
    'python -m lcpi.aep.cli network-optimize-unified "{inp}" '
    '--method genetic --solver epanet --epanet-backend dll '
    '--generations 10 --population 20 --demand {demand} --no-confirm --no-cache --no-surrogate '
    '--output "{out_json}"'
)

SIM_CMD_TEMPLATE = (
    'python -m lcpi.aep.cli simulate-inp "{inp_or_out}" --format json'
)

def run_cmd(cmd, check=True):
    print(f">>> RUN: {cmd}")
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(proc.stdout)
    if proc.stderr:
        print("STDERR:", proc.stderr, file=sys.stderr)
    if check and proc.returncode != 0:
        raise RuntimeError(f"Command failed (rc={proc.returncode}): {cmd}\nStderr: {proc.stderr}")
    return proc

def load_json(path):
    p = Path(path)
    if not p.exists():
        return None
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)

def sum_demands_in_inp(inp_path):
    """Somme des demandes lues dans [DEMANDS] et si absent ou vide, retourne None."""
    lines = Path(inp_path).read_text(encoding='utf-8').splitlines()
    in_dem = False
    total = 0.0
    found = False
    for ln in lines:
        s = ln.strip()
        if s.upper().startswith("[DEMANDS]"):
            in_dem = True
            continue
        if in_dem:
            if s.startswith('['):
                break
            if not s or s.startswith(';'):
                continue
            parts = s.split()
            # On lit la première valeur numérique après l'ID si présente
            if len(parts) >= 2:
                try:
                    val = float(parts[1])
                    total += val
                    found = True
                except Exception:
                    continue
    return total if found else None

def extract_pipe_diameters_from_out(json_obj):
    """Tentative d'extraction des diamètres: chercher proposals ou links"""
    diams = []
    if not json_obj:
        return diams
    # proposals -> candidate design: inspect if present
    for k in ("proposals", "design", "links"):
        if k in json_obj:
            try:
                items = json_obj[k]
                if isinstance(items, list):
                    for it in items:
                        # try common keys
                        for key in ("diameter","diam","D","pipe_diameter","nominal_diameter"):
                            if key in it:
                                diams.append(float(it[key]))
                                break
                break
            except Exception:
                continue
    # fallback check nodes/links arrays
    if not diams:
        if "links" in json_obj and isinstance(json_obj["links"], list):
            for l in json_obj["links"]:
                v = l.get("diameter") or l.get("diam")
                if v is not None:
                    try:
                        diams.append(float(v))
                    except Exception:
                        pass
    return diams

def summarize_sim_json(sim):
    if not sim: return {}
    summary = {}
    summary['cost'] = sim.get('cost') or sim.get('meta',{}).get('best_cost') or sim.get('total_cost')
    summary['simulation_time'] = sim.get('simulation_time') or sim.get('meta',{}).get('sim_time_seconds')
    # nodes/links
    summary['n_nodes'] = len(sim.get('nodes',[]))
    summary['n_links'] = len(sim.get('links',[]))
    # pressure stats
    pressures = [n.get('pressure') for n in sim.get('nodes',[]) if isinstance(n.get('pressure'), (int,float))]
    summary['pressure_min'] = min(pressures) if pressures else None
    summary['pressure_max'] = max(pressures) if pressures else None
    # flows
    flows = [l.get('flow') for l in sim.get('links',[]) if isinstance(l.get('flow'), (int,float))]
    summary['flow_sum'] = sum(flows) if flows else None
    # demand sum
    summary['demand_sum'] = sum([n.get('demand',0) for n in sim.get('nodes',[])]) if sim.get('nodes') else None
    return summary

def compare_lists(a,b):
    if not a or not b:
        return False
    # simple compare: mean difference relative
    import statistics
    ma = statistics.mean(a)
    mb = statistics.mean(b)
    if ma == 0 and mb == 0:
        return True
    rel = abs(ma-mb)/max(abs(ma),abs(mb))
    return rel < 1e-6  # essentially equal

# 1) Use existing optimization results
inp = "bismark_inp.inp"
out_opt_500 = Path("temp/out_bismark_inp_demand_500.json")  # Use existing file
out_opt_600 = Path("temp/out_bismark_inp_demand_600.json")  # Use existing file
sim_500 = TMP / "sim_500.json"
sim_600 = TMP / "sim_600.json"

# Use existing files - check for any optimization files with demand in name
existing_opt_files = list(Path("temp").glob("*demand*.json"))
if existing_opt_files:
    print("Found existing optimization files:", existing_opt_files)
    # Use the first two files found
    out_opt_500 = existing_opt_files[0]
    out_opt_600 = existing_opt_files[1] if len(existing_opt_files) > 1 else existing_opt_files[0]
    print("Using:", out_opt_500, out_opt_600)
else:
    print("No existing optimization files found, would need to run optimizations")
    sys.exit(1)

# 2) Locate .inp used by optimizer (if optimizer wrote temporary inp file, try to find it near temp or artifacts)
# Heuristique: check TMP for recent .inp files
used_inps = list((Path.cwd()/ "artifacts").glob("**/*.inp")) if (Path.cwd()/"artifacts").exists() else []
used_inps += list(Path.cwd().glob("**/out_*.inp"))
used_inps = sorted(used_inps, key=lambda p: p.stat().st_mtime, reverse=True)
print("Detected candidate INP files (most recent):", used_inps[:5])

# 3) Run simulate-inp on the generated optimized outputs if they are .inp, otherwise try to feed the optimizer output (if it contains an 'inp' field)
def locate_inp_for_out(out_json_path):
    j = load_json(out_json_path)
    if not j:
        return None
    # Check explicit field
    for key in ("inp_file","inp","input_file","generated_inp"):
        if key in j:
            p = Path(j[key])
            if p.exists():
                return p
    # fallback: check artifacts in meta
    meta = j.get('meta',{})
    artifacts = meta.get('artifacts',{}) if isinstance(meta.get('artifacts',{}), dict) else {}
    flows = artifacts.get('flows') if isinstance(artifacts.get('flows'), dict) else {}
    # search common artifact directories near temp
    candidates = []
    for d in (Path.cwd()/ "artifacts", Path.cwd()/ "temp", Path.cwd()/"results"):
        if d.exists():
            candidates += list(d.glob("**/*.inp"))
    candidates = sorted(set(candidates), key=lambda p: p.stat().st_mtime, reverse=True)
    # return first candidate
    return candidates[0] if candidates else None

inp_for_500 = locate_inp_for_out(out_opt_500) or inp
inp_for_600 = locate_inp_for_out(out_opt_600) or inp

# 4) Sum demands in the INPs that will be simulated (check BEFORE simulation)
sum500_pre = sum_demands_in_inp(inp_for_500)
sum600_pre = sum_demands_in_inp(inp_for_600)

print("Sum demands detected in INP for 500-run:", sum500_pre)
print("Sum demands detected in INP for 600-run:", sum600_pre)

# 5) Use existing simulation results or run simulations
sim_500_existing = Path("temp/sim_500.json")
sim_600_existing = Path("temp/sim_600.json")

if sim_500_existing.exists() and sim_600_existing.exists():
    print("Using existing simulation files:", sim_500_existing, sim_600_existing)
    sim_500 = sim_500_existing
    sim_600 = sim_600_existing
else:
    print("Running simulations...")
    try:
        run_cmd(SIM_CMD_TEMPLATE.format(inp_or_out=inp_for_500, out_json=sim_500))
        run_cmd(SIM_CMD_TEMPLATE.format(inp_or_out=inp_for_600, out_json=sim_600))
    except Exception as e:
        print("ERROR running simulation:", e)
        sys.exit(3)

# 6) Load outputs
opt500 = load_json(out_opt_500)
opt600 = load_json(out_opt_600)
sim500 = load_json(sim_500)
sim600 = load_json(sim_600)

# 7) Basic checks: simulator used and sim time
checks = []
for label, j in (("opt500", opt500), ("opt600", opt600), ("sim500", sim500), ("sim600", sim600)):
    if not j:
        checks.append((label, "MISSING_JSON"))
    else:
        meta = j.get("meta",{})
        sim_used = meta.get("simulator_used") or j.get("simulator") or meta.get("solver")
        sim_time = meta.get("sim_time_seconds") or meta.get("simulation_time") or j.get("simulation_time")
        checks.append((label, {"simulator_used": sim_used, "sim_time_seconds": sim_time}))

# 8) Extract diameters from proposals / links
diams_opt500 = extract_pipe_diameters_from_out(opt500)
diams_opt600 = extract_pipe_diameters_from_out(opt600)

# 9) Summaries of simulation JSONs
summary500 = summarize_sim_json(sim500)
summary600 = summarize_sim_json(sim600)

# 10) Build report
report = []
report.append("# Vérification automatisée — network-optimize-unified\n")
report.append("## Résumé des fichiers générés\n")
report.append(f"- out_opt_500: {out_opt_500}\n- out_opt_600: {out_opt_600}\n- sim_500: {sim_500}\n- sim_600: {sim_600}\n")
report.append("## Checks basiques (existence / simulateur)\n")
for c in checks:
    report.append(f"- {c[0]}: {c[1]}\n")

report.append("## Demandes détectées dans INP avant simulation\n")
report.append(f"- INP utilisé pour 500-run: {inp_for_500} -> sum_demands = {sum500_pre}\n")
report.append(f"- INP utilisé pour 600-run: {inp_for_600} -> sum_demands = {sum600_pre}\n")

report.append("## Diamètres extraits\n")
report.append(f"- diametres (opt500) sample count {len(diams_opt500)} -> mean: { (sum(diams_opt500)/len(diams_opt500)) if diams_opt500 else 'N/A'}\n")
report.append(f"- diametres (opt600) sample count {len(diams_opt600)} -> mean: { (sum(diams_opt600)/len(diams_opt600)) if diams_opt600 else 'N/A'}\n")

report.append("## Summary simulations\n")
report.append(f"- sim500 summary: {summary500}\n")
report.append(f"- sim600 summary: {summary600}\n")

# 11) Sanity checks
anomalies = []
# demand sums must differ (500 vs 600) if distribution applied
if sum500_pre is None or sum600_pre is None:
    anomalies.append("Impossible de lire les demandes dans au moins un INP avant simulation.")
else:
    if abs(sum600_pre - sum500_pre) < 1e-3:
        anomalies.append("La somme des demandes dans les INP avant simulation est IDENTIQUE pour 500 et 600 -> incohérence (le flag --demand semble non appliqué ou écrasé).")

# simulator metric presence
for label, info in checks:
    if isinstance(info, dict):
        if not info.get("simulator_used"):
            anomalies.append(f"{label} semble ne pas contenir l'indication du simulateur utilisé (meta.simulator_used manquant).")
        if not info.get("sim_time_seconds"):
            anomalies.append(f"{label} semble ne pas contenir de durée de simulation (meta.sim_time_seconds manquant).")

# diameters should differ or at least mean differ
if diams_opt500 and diams_opt600:
    mean500 = sum(diams_opt500)/len(diams_opt500)
    mean600 = sum(diams_opt600)/len(diams_opt600)
    if abs(mean600-mean500) < 1e-6:
        anomalies.append("Les diamètres moyens extraits des outputs d'optimisation sont identiques (possible problème).")

# cost difference
cost500 = summary500.get('cost')
cost600 = summary600.get('cost')
if cost500 is not None and cost600 is not None:
    if abs(float(cost600)-float(cost500)) < 1e-3:
        anomalies.append("Coût total identique pour les deux scénarios -> vérifier la logique d'évaluation du coût.")

report.append("## Anomalies détectées\n")
if anomalies:
    for a in anomalies:
        report.append(f"- {a}\n")
else:
    report.append("- Aucun anomalie détectée.\n")

# 12) Save report and summaries
(Path(TMP)/"verification_report.md").write_text("\n".join(report), encoding='utf-8')
with open(Path(TMP)/"summary_500.json","w",encoding="utf-8") as f:
    json.dump(summary500,f,indent=2)
with open(Path(TMP)/"summary_600.json","w",encoding="utf-8") as f:
    json.dump(summary600,f,indent=2)

print("Report written to", Path(TMP)/"verification_report.md")
print("If anomalies found, please inspect the files and logs. No pushes performed.")
