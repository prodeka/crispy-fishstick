"""
CLI `lcpi aep tank` (MVP Binary): verify, simulate, optimize, auto-optimize.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime

import typer
import yaml

from ..optimizer.io import load_yaml_or_inp
from ..optimizer.validators import NetworkValidator
from ..optimizer.algorithms.binary import MockSolver, BinarySearchOptimizer
from ..optimizer.scoring import CostScorer


app = typer.Typer(help="🏗️ Optimisation des réservoirs surélevés (MVP Binary)")
pareto_app = typer.Typer(help="Export du front de Pareto")


@pareto_app.command("export")
def cmd_pareto_export(input_points: Path = typer.Argument(..., help="JSON avec points [{'CAPEX':...,'OPEX':...}]"), out: Path = typer.Option(Path("results/pareto.json"), help="Fichier de sortie"), knee: bool = typer.Option(True, "--knee/--no-knee", help="Inclure knee point")):
	from ..optimizer.pareto import compute_pareto, knee_point
	data = json.loads(input_points.read_text(encoding="utf-8"))
	pareto = compute_pareto(data)
	payload = {"pareto": pareto}
	if knee:
		payload["knee"] = knee_point(pareto)
	out.parent.mkdir(parents=True, exist_ok=True)
	out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
	typer.secho(f"Pareto exporté: {out}", fg=typer.colors.GREEN)

app.add_typer(pareto_app, name="pareto")


@app.command("verify")
def cmd_verify(network: Path = typer.Argument(..., help="Chemin du réseau (.yml/.yaml/.inp)")):
	v = NetworkValidator()
	r = v.check_integrity(network)
	if not r.get("ok"):
		typer.secho("ERREUR: fichier introuvable ou illisible", fg=typer.colors.RED)
		raise typer.Exit(code=1)
	if network.suffix.lower() in (".yml", ".yaml"):
		nm, _ = load_yaml_or_inp(network)
		vm = v.validate_model(nm)
		if not vm["ok"]:
			typer.secho(f"Validation modèle échouée: {vm['errors']}", fg=typer.colors.RED)
			raise typer.Exit(code=1)
	typer.secho(f"Intégrité OK. checksum: {r['checksum']}", fg=typer.colors.GREEN)
	typer.echo(json.dumps(r, indent=2, ensure_ascii=False))


@app.command("simulate")
def cmd_simulate(
	network: Path = typer.Argument(...),
	H: float = typer.Option(..., help="Hauteur du réservoir H_tank (m)"),
):
	nm, _ = load_yaml_or_inp(network)
	solver = MockSolver()
	sim = solver.simulate(nm, float(H))
	out = {
		"H_tank_m": float(H),
		"min_pressure_m": sim.min_pressure_m,
		"max_velocity_m_s": sim.max_velocity_m_s,
		"pressures_m": sim.pressures_m,
		"velocities_m_s": sim.velocities_m_s,
		"meta": {"solver": "MockSolver", "timestamp": datetime.utcnow().isoformat()},
	}
	typer.echo(json.dumps(out, indent=2, ensure_ascii=False))


@app.command("optimize")
def cmd_optimize(
	network: Path = typer.Argument(...),
	config: Path = typer.Option(..., help="config.yml avec paramètres d'optimisation"),
	out: Path = typer.Option(Path("results/tank_opt.json"), help="Fichier de sortie JSON"),
	method: Optional[str] = typer.Option(None, "--method", help="Override de la méthode: binary|nested|global|surrogate"),
	solver: Optional[str] = typer.Option(None, "--solver", help="Solveur à utiliser: lcpi|epanet|mock"),
	debug: bool = typer.Option(False, "--debug", help="Affichage d'informations de debug"),
):
	cfg_raw = yaml.safe_load(config.read_text(encoding="utf-8"))
	optimization = cfg_raw.get("optimization", {})
	pressure_constraints = cfg_raw.get("pressure_constraints", {"min_pressure_m": 12.0})
	solver_cfg = cfg_raw.get("solver", {"type": "mock"})
	if solver:
		solver_cfg["type"] = solver

	method = method or optimization.get("method", "binary")
	H_bounds = optimization.get("H_bounds_m")
	H_fixed = optimization.get("H_fixed_m")
	tolerance = float(optimization.get("tolerance_m", 0.1))
	max_iter = int(optimization.get("max_iterations", 60))

	nm, _ = load_yaml_or_inp(network)
	v = NetworkValidator()
	vm = v.validate_model(nm)
	if not vm["ok"]:
		typer.secho(f"Erreurs de validation: {vm['errors']}", fg=typer.colors.RED)
		raise typer.Exit(code=1)

	if method not in ("binary", "nested", "global", "surrogate"):
		typer.secho("Méthode non supportée (binary|nested|global|surrogate).", fg=typer.colors.RED)
		raise typer.Exit(code=2)

	if H_fixed is not None:
		H_min = H_max = float(H_fixed)
	elif H_bounds is not None:
		H_min, H_max = float(H_bounds[0]), float(H_bounds[1])
	else:
		typer.secho("Veuillez fournir 'H_bounds_m' ou 'H_fixed_m' dans la config.", fg=typer.colors.RED)
		raise typer.Exit(code=1)

	if debug:
		typer.secho(f"[debug] Méthode: {method} | H_bounds: {(H_min, H_max)} | tol: {tolerance} | iters: {max_iter}", fg=typer.colors.BLUE)

	method_used = method
	if method == "binary":
		optimizer = BinarySearchOptimizer(nm, float(pressure_constraints.get("min_pressure_m", 12.0)))
		res = optimizer.optimize_tank_height(H_min, H_max, tolerance=tolerance, max_iter=max_iter)
	elif method == "nested":
		from ..optimizer.algorithms.nested import NestedGreedyOptimizer
		vel = cfg_raw.get("velocity_constraints", {})
		res = NestedGreedyOptimizer(nm, solver=solver_cfg.get("type", "lcpi")).optimize_nested(
			(H_min, H_max),
			float(pressure_constraints.get("min_pressure_m", 12.0)),
			velocity_constraints=vel,
			diameter_db_path=optimization.get("diameter_db"),
		)
	elif method == "global":
		cfg_obj = optimization if isinstance(optimization, dict) else {}
		from ..optimizer.algorithms.global_opt import GlobalOptimizer
		res = GlobalOptimizer(cfg_obj).optimize_global(nm.dict())
	else:  # surrogate
		from ..optimizer.algorithms.surrogate import SurrogateOptimizer
		res = SurrogateOptimizer(nm, solver=solver_cfg.get("type", "lcpi")).build_and_optimize((H_min, H_max), n_initial=30)

	# Ajout CAPEX minimal (à partir des diamètres existants)
	try:
		diam_db_path = optimization.get("diameter_db") or "project/data/diameters.yml"
		diameter_db = yaml.safe_load(Path(diam_db_path).read_text(encoding="utf-8"))
		d_costs = {int(row["d_mm"]): float(row.get("cost_per_m", 0.0)) for row in (diameter_db or [])}
	except Exception:
		d_costs = {}
	diameters_current = {lid: int(link.get("diameter_mm")) for lid, link in (nm.links or {}).items() if link.get("diameter_mm") is not None}
	scorer = CostScorer(d_costs)
	costs = scorer.compute_total_cost(nm, diameters_current, res.get("H_tank_m", H_max)) if isinstance(res, dict) else {}

	report_payload = {
		"template": "optimisation_tank.jinja2",
		"placeholders": {
			"methode_utilisee": method_used,
			"contrainte_pression_min": f"{pressure_constraints.get('min_pressure_m', 12.0)} m",
			"cout_total": f"{costs.get('total_cost')} FCFA" if costs.get("total_cost") is not None else "N/A",
		},
	}

	if isinstance(res, dict):
		res.setdefault("meta", {})
		res["meta"].update({"solver": solver_cfg.get("type", "mock")})
		res["costs"] = res.get("costs") or costs
		res["report_payload"] = res.get("report_payload") or report_payload
		final = res
	else:
		final = {"meta": {"method": method_used, "solver": solver_cfg.get("type", "mock")}, "result": res, "costs": costs, "report_payload": report_payload}

	out.parent.mkdir(parents=True, exist_ok=True)
	out.write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
	typer.secho(f"Optimisation terminée. Résultat: {out}", fg=typer.colors.GREEN)


@app.command("auto-optimize")
def cmd_auto_optimize(
	network: Path = typer.Argument(...),
	config: Path = typer.Option(...),
	out: Path = typer.Option(Path("results/tank_auto.json")),
):
	# Vérification
	v = NetworkValidator()
	r = v.check_integrity(network)
	if not r.get("ok"):
		typer.secho("Échec de l'intégrité", fg=typer.colors.RED)
		raise typer.Exit(code=1)
	# Optimisation
	cmd_optimize.callback(network=network, config=config, out=out)
	typer.secho("Auto-optimize terminé.", fg=typer.colors.CYAN)


if __name__ == "__main__":
	app()


