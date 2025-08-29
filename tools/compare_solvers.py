#!/usr/bin/env python3
"""
Tool: Compare EPANET vs LCPI solver outputs on the same network and params.

- Runs lcpi.aep.cli network-optimize-unified twice (solver=epanet, solver=lcpi)
- Uses identical GA parameters provided via CLI or sensible defaults
- Loads both result JSONs and prints a concise comparison summary

Usage examples:
  python tools/compare_solvers.py bismark_inp.inp --generations 10 --population 20 --output_prefix cmp_bismark
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified"]


def _load_model(input_path: str) -> Dict[str, Any]:
	"""Load unified model (YAML or INP) to access real pipe lengths."""
	try:
		from lcpi.aep.io import load_yaml_or_inp  # type: ignore
		model, _meta = load_yaml_or_inp(Path(input_path))
		
		# Debug: afficher le type et la structure
		print(f"🔍 Debug: Type du modèle: {type(model)}")
		print(f"🔍 Debug: Méta: {_meta}")
		
		# Normalize to dict - handle both dict and object cases
		if hasattr(model, "dict"):
			model_dict = model.dict()
			print(f"🔍 Debug: Modèle converti via .dict(): {len(model_dict.get('links', {}))} liens")
			return model_dict
		elif isinstance(model, dict):
			print(f"🔍 Debug: Modèle déjà dict: {len(model.get('links', {}))} liens")
			return model
		else:
			# Fallback: try to access attributes directly
			links = getattr(model, "links", {})
			nodes = getattr(model, "nodes", {})
			tanks = getattr(model, "tanks", {})
			
			# Debug: afficher les liens trouvés
			if links:
				sample_links = list(links.items())[:3]
				print(f"🔍 Debug: Liens trouvés (échantillon): {sample_links}")
				for lid, ldata in sample_links:
					length = getattr(ldata, "length_m", None) or getattr(ldata, "length", None)
					print(f"🔍 Debug: Conduite {lid} - longueur: {length}")
			
			result = {"links": links, "nodes": nodes, "tanks": tanks}
			print(f"🔍 Debug: Modèle fallback créé avec {len(links)} liens")
			return result
	except Exception as e:
		print(f"❌ Erreur lors du chargement du modèle: {e}")
		return {}


def run_solver(input_path: str, solver: str, generations: int, population: int, output_prefix: str) -> Path:
	"""Run optimization with specified solver and return result file path."""
	output_file = f"{output_prefix}_{solver}"
	cmd = CLI + [
		input_path,
		"--method", "genetic",
		"--generations", str(generations),
		"--population", str(population),
		"--solver", solver,
		"--show-stats",
		"--output", output_file,
		"--verbose",
		"--no-log"
	]
	print(f"\n➡️ Running: {' '.join(cmd)}")
	subprocess.run(cmd, check=True)
	return ROOT / output_file


def load_json(path: Path) -> Dict[str, Any]:
	with open(path, "r", encoding="utf-8") as f:
		return json.load(f)


def extract_summary(result: Dict[str, Any], model: Dict[str, Any]) -> Dict[str, Any]:
    meta = result.get("meta", {})
    props = result.get("proposals", [])
    best = props[0] if props else {}
    
    # Debug: afficher la structure du modèle
    print(f"🔍 Debug: Structure du modèle: {list(model.keys())}")
    
    # total length from model - improved extraction
    total_len = 0.0
    links = model.get("links", {})
    print(f"🔍 Debug: Nombre de liens dans le modèle: {len(links)}")
    
    try:
        for lid, link_data in links.items():
            # Try multiple ways to get length
            length = None
            if isinstance(link_data, dict):
                length = link_data.get("length_m") or link_data.get("length")
            else:
                # Try to access as object
                length = getattr(link_data, "length_m", None) or getattr(link_data, "length", None)
            
            if length is not None:
                total_len += float(length)
                if total_len < 1.0:  # Debug first few lengths
                    print(f"🔍 Debug: Conduite {lid} - longueur: {length} m")
            else:
                print(f"⚠️ Warning: Impossible de récupérer la longueur pour {lid}")
    except Exception as e:
        print(f"⚠️ Erreur lors du calcul de la longueur totale: {e}")
				
    print(f"🔍 Debug: Longueur totale calculée: {total_len:.2f} m")
    
    # Extract cost and feasibility
    cost = None
    feasible = None
    
    # Try multiple ways to get cost
    if "best_cost" in meta:
        cost = meta["best_cost"]
    elif "CAPEX" in best:
        cost = best["CAPEX"]
    elif "cost" in best:
        cost = best["cost"]
    
    # Try multiple ways to get feasibility
    if "best_constraints_ok" in meta:
        feasible = meta["best_constraints_ok"]
    elif "constraints_ok" in best:
        feasible = best["constraints_ok"]
    elif "feasible" in best:
        feasible = best["feasible"]
    
    print(f"🔍 Debug: Coût EPANET: {cost}")
    print(f"🔍 Debug: Longueur totale: {total_len}")
    
    # Calculate implied unit cost if we have both cost and length
    implied_unit = None
    if cost is not None and total_len > 0:
        implied_unit = cost / total_len
        print(f"🔍 Debug: Prix unitaire implicite: {implied_unit}")
    
    return {
        "cost": cost,
        "feasible": feasible,
        "total_length": total_len,
        "implied_unit_cost": implied_unit,
        "num_pipes": len(links),
        "diameters": best.get("diameters_mm", {}),
        "diameters_mm": best.get("diameters_mm", {}),
    }


def compare_solvers(epanet_result: Dict[str, Any], lcpi_result: Dict[str, Any], model: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
    """Compare les résultats des deux solveurs et génère un rapport détaillé."""
    
    epanet_summary = extract_summary(epanet_result, model)
    lcpi_summary = extract_summary(lcpi_result, model)
    
    # Get price database info
    price_db_path = "C:\\PROJET_DIMENTIONEMENT_2\\src\\lcpi\\db\\aep_prices.db"
    
    # Analyze diameters and prices
    epanet_diameters = epanet_summary.get("diameters", {})
    lcpi_diameters = lcpi_summary.get("diameters", {})
    
    # Calculate cost per meter for each solver
    epanet_cost_per_m = epanet_summary.get("implied_unit_cost")
    lcpi_cost_per_m = lcpi_summary.get("implied_unit_cost")
    
    # Calculate delta
    epanet_cost = epanet_summary.get("cost", 0)
    lcpi_cost = lcpi_summary.get("cost", 0)
    delta = lcpi_cost - epanet_cost
    delta_percent = (delta / epanet_cost * 100) if epanet_cost != 0 else 0
    
    report = f"""===== COMPARISON: EPANET vs LCPI =====
Price DB (EPANET): {price_db_path}
Price DB (LCPI)  : {price_db_path}

Best cost EPANET : {epanet_cost:,.2f} FCFA
Best cost LCPI   : {lcpi_cost:,.2f} FCFA
Delta LCPI-EPANET: {delta:,.2f} FCFA ({delta_percent:.2f}%)

Total pipe length: {epanet_summary.get("total_length", 0):.2f} m
Implied unit (EPANET): {epanet_cost_per_m:,.2f} FCFA/m
Implied unit (LCPI)  : {lcpi_cost_per_m:,.2f} FCFA/m

Pipes (EPANET): {epanet_summary.get("num_pipes", 0)}
Pipes (LCPI)  : {lcpi_summary.get("num_pipes", 0)}
Feasible (EPANET): {epanet_summary.get("feasible")}
Feasible (LCPI)  : {lcpi_summary.get("feasible")}

=== DIAMETER ANALYSIS ===
EPANET Diameters: {len(epanet_diameters)} pipes
LCPI Diameters: {len(lcpi_diameters)} pipes

=== PRICE ANALYSIS ===
EPANET Cost per meter: {epanet_cost_per_m:,.2f} FCFA/m
LCPI Cost per meter: {lcpi_cost_per_m:,.2f} FCFA/m
Price ratio (LCPI/EPANET): {(lcpi_cost_per_m/epanet_cost_per_m*100):.2f}% if epanet_cost_per_m else "N/A"

=== DIAGNOSTIC NOTES ===
- If EPANET cost per meter > 100,000 FCFA/m: Check for very large diameters (800-900mm)
- If LCPI cost per meter < 1,000 FCFA/m: Check if LCPI uses correct price database
- If price ratio < 10%: LCPI may not be using real network lengths or prices
"""
    
    # Créer le dictionnaire JSON avec toutes les données détaillées
    json_data = {
        "epanet": epanet_summary,
        "lcpi": lcpi_summary,
        "comparison": {
            "epanet_cost": epanet_cost,
            "lcpi_cost": lcpi_cost,
            "delta": delta,
            "delta_percent": delta_percent,
            "total_length": epanet_summary.get("total_length", 0),
            "epanet_cost_per_m": epanet_cost_per_m,
            "lcpi_cost_per_m": lcpi_cost_per_m,
            "price_ratio": (lcpi_cost_per_m/epanet_cost_per_m*100) if epanet_cost_per_m else None,
            "price_db_path": price_db_path
        }
    }
    
    return report, json_data


def main():
	parser = argparse.ArgumentParser(description="Compare EPANET vs LCPI solvers")
	parser.add_argument("input", help="Path to INP/YAML network file (e.g., bismark_inp.inp)")
	parser.add_argument("--generations", type=int, default=10)
	parser.add_argument("--population", type=int, default=20)
	parser.add_argument("--output_prefix", type=str, default="cmp_run")
	args = parser.parse_args()

	inp_path = str(Path(args.input).resolve())

	# Load model once for reporting metrics
	model = _load_model(inp_path)

	# Run EPANET
	ep_out = run_solver(inp_path, "epanet", args.generations, args.population, args.output_prefix)
	# Run LCPI
	lc_out = run_solver(inp_path, "lcpi", args.generations, args.population, args.output_prefix)

	# Load results
	epanet_json = load_json(ep_out)
	lcpi_json = load_json(lc_out)

	# Compare
	report, json_data = compare_solvers(epanet_json, lcpi_json, model)
	print(report)

	# Save report alongside outputs
	report_path = ROOT / f"{args.output_prefix}_compare_report.txt"
	report_path.write_text(report, encoding="utf-8")
	print(f"\n📄 Report saved to: {report_path}")
	
	# Save JSON data for detailed analysis
	json_path = ROOT / f"{args.output_prefix}_compare_report.json"
	with open(json_path, 'w', encoding='utf-8') as f:
		json.dump(json_data, f, indent=2, ensure_ascii=False)
	print(f"📊 JSON data saved to: {json_path}")


if __name__ == "__main__":
	main()
