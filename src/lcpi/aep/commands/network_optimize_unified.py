from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint

from ..optimizer.controllers import OptimizationController  # type: ignore


app = typer.Typer(name="network-optimize-unified", help="Optimisation réseau unifiée (INP/YML)")
_controller = OptimizationController()


@app.command("run")
def network_optimize_unified(
    input_file: Path = typer.Argument(..., help="Fichier réseau (.inp ou .yml)"),
    method: str = typer.Option("nested", "--method", "-m", help="genetic|nested|surrogate|global|multi-tank"),
    solver: str = typer.Option("epanet", "--solver", help="epanet|lcpi|mock"),
    pression_min: Optional[float] = typer.Option(None, "--pression-min", help="Pression minimale (m)"),
    vitesse_min: Optional[float] = typer.Option(None, "--vitesse-min", help="Vitesse minimale (m/s)"),
    vitesse_max: Optional[float] = typer.Option(None, "--vitesse-max", help="Vitesse maximale (m/s)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier JSON de sortie"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose"),
):
    """Commande d'optimisation unifiée acceptant .inp et .yml (Sprint 1: support minimal nested)."""
    if not input_file.exists():
        rprint(f"[red]Fichier introuvable:[/red] {input_file}")
        raise typer.Exit(code=2)

    constraints = {
        "pressure_min_m": pression_min,
        "velocity_min_m_s": vitesse_min,
        "velocity_max_m_s": vitesse_max,
    }

    try:
        result = _controller.run_optimization(
            input_path=input_file,
            method=method,
            solver=solver,
            constraints=constraints,
            hybrid_refiner=None,
            hybrid_params=None,
            algo_params=None,
            price_db=None,
            verbose=verbose,
        )
    except Exception as exc:
        rprint(f"[red]Erreur lors de l'optimisation:[/red] {exc}")
        raise typer.Exit(code=3)

    if output:
        import json
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        rprint(f"[green]Résultat écrit dans[/green] {output}")
    else:
        meta = result.get("meta", {})
        best = result.get("proposals", [{}])[0] if result.get("proposals") else {}
        rprint("[green]Optimisation terminée — résumé :[/green]")
        rprint(f" method: {meta.get('method')} solver: {meta.get('solver')}")
        rprint(f" best CAPEX: {best.get('CAPEX')} constraints_ok: {best.get('constraints_ok')}")


