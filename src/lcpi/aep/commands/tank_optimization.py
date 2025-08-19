"""
CLI `lcpi aep tank` (V11+): verify, simulate, optimize.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

import typer
import yaml
from rich.table import Table
from rich.console import Console

# Import des nouveaux algorithmes et modèles
from ..optimizer.algorithms.global_opt import GlobalOptimizer
from ..optimizer.algorithms.multi_tank import MultiTankOptimizer
from ..optimizer.models import OptimizationConfig, OptimizationResult, Proposal
from ..optimizer.pareto import compute_pareto, knee_point
from ..optimizer.validators import NetworkValidator
from ..optimizer.db import get_candidate_diameters
from lcpi.reporting.report_generator import ReportGenerator

app = typer.Typer(help="🏗️ Optimisation des réservoirs surélevés (V11+)")
pareto_app = typer.Typer(help="Analyse du front de Pareto")
diameters_app = typer.Typer(help="Gestion de la base de données des diamètres")
app.add_typer(pareto_app, name="pareto")
app.add_typer(diameters_app, name="diameters-manage")

# ... (Les commandes `verify` et `simulate` peuvent rester si elles sont jugées utiles)

class TankOptimizationOrchestrator:
    """Orchestre le processus d'optimisation de bout en bout."""

    def __init__(self, network_path: Path, config_path: Path, output_path: Path, objectives: Optional[Dict] = None):
        self.network_path = network_path
        self.output_path = output_path
        self.config = self._load_config(config_path, objectives)
        self.validator = NetworkValidator()

    def _load_config(self, path: Path, objectives_override: Optional[Dict]) -> OptimizationConfig:
        try:
            raw_config = yaml.safe_load(path.read_text(encoding="utf-8"))
            if objectives_override:
                raw_config["objectives"] = objectives_override
            return OptimizationConfig(**raw_config)
        except Exception as e:
            typer.secho(f"Erreur de validation de la configuration: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    def run(self):
        """Point d'entrée principal pour lancer l'orchestration."""
        validation = self.validator.check_integrity(self.network_path)
        if not validation.get("ok"):
            typer.secho(f"Validation du fichier réseau échouée: {validation['errors']}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        optimizer = self._get_optimizer()
        raw_result = optimizer.optimize()
        v11_result = self._format_result(raw_result)
        self.save_and_report(v11_result)

    def _get_optimizer(self) -> Any:
        method = self.config.method
        if method == "global":
            return GlobalOptimizer(self.config, self.network_path)
        elif method == "multi-tank":
            return MultiTankOptimizer(self.network_path, self.config.dict())
        else:
            raise NotImplementedError(f"La méthode '{method}' n'est pas encore intégrée.")

    def _format_result(self, raw_result: Dict[str, Any]) -> OptimizationResult:
        proposals: list[Proposal] = []
        if not proposals:
            proposals.append(
                Proposal(
                    name="placeholder_solution",
                    is_feasible=raw_result.get("feasible", False),
                    tanks=[],
                    diameters_mm={},
                    costs=raw_result.get("costs", {}),
                    metrics={}
                )
            )
        return OptimizationResult(
            proposals=proposals,
            pareto_front=None,
            metadata={"method": self.config.method, "network_file": str(self.network_path)}
        )

    from lcpi.core.integrity import sign_data

# ... (le reste des imports)

# ... (le reste du fichier jusqu'à la méthode save_and_report)

    def save_and_report(self, result: OptimizationResult):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        result_data = result.dict()
        
        # Signer les données avant de les sauvegarder
        try:
            signed_data = sign_data(result_data)
            json_output = json.dumps(signed_data, indent=2)
            typer.secho("Résultat signé avec succès.", fg=typer.colors.CYAN)
        except FileNotFoundError:
            typer.secho("AVERTISSEMENT: Clé de signature non trouvée. Le résultat ne sera pas signé.", fg=typer.colors.YELLOW)
            typer.secho("Exécutez `lcpi-admin generate-keys` pour créer une clé.", fg=typer.colors.YELLOW)
            json_output = json.dumps(result_data, indent=2)

        self.output_path.write_text(json_output, encoding="utf-8")
        typer.secho(f"Optimisation terminée. Résultat V11 sauvegardé: {self.output_path}", fg=typer.colors.GREEN)
        self.generate_report(result.dict(), self.output_path) # Le rapport n'a pas besoin des données de signature

    @staticmethod
    def generate_report(result_data: Dict, output_path: Path):
        try:
            rg = ReportGenerator()
            report_path = output_path.with_suffix(".html")
            rg.generate_from_template(result_data, template_name="optimisation_tank.jinja2", output_path=report_path)
            typer.secho(f"Rapport généré: {report_path}", fg=typer.colors.GREEN)
        except Exception as e:
            typer.secho(f"Génération du rapport échouée: {e}", fg=typer.colors.YELLOW)

@app.command("optimize")
def cmd_optimize(
    network: Path = typer.Argument(..., help="Chemin du réseau (.yml/.yaml/.inp)"),
    config: Path = typer.Option(..., help="Fichier de configuration YAML (multi-objectif par défaut)"),
    out: Path = typer.Option(Path("results/tank_opt.json"), help="Fichier de sortie JSON"),
):
    """Lance une optimisation multi-objectifs (CAPEX vs OPEX)."""
    orchestrator = TankOptimizationOrchestrator(network_path=network, config_path=config, output_path=out)
    orchestrator.run()

@app.command("price-optimize")
def cmd_price_optimize(
    network: Path = typer.Argument(..., help="Chemin du réseau (.yml/.yaml/.inp)"),
    config: Path = typer.Option(..., help="Fichier de configuration YAML"),
    lambda_opex: float = typer.Option(10.0, help="Facteur de pondération pour l'OPEX"),
    out: Path = typer.Option(Path("results/tank_price_opt.json"), help="Fichier de sortie JSON"),
):
    """Optimise pour un coût pondéré unique (CAPEX + λ * OPEX)."""
    objectives = {"capex": True, "opex": False, "lambda_opex": lambda_opex}
    orchestrator = TankOptimizationOrchestrator(network_path=network, config_path=config, output_path=out, objectives=objectives)
    orchestrator.run()

@app.command("report")
def cmd_report(
    result_file: Path = typer.Argument(..., help="Fichier de résultat JSON V11 existant", exists=True),
):
    """Régénère le rapport HTML à partir d'un fichier de résultats."""
    result_data = json.loads(result_file.read_text(encoding="utf-8"))
    TankOptimizationOrchestrator.generate_report(result_data, result_file)

@diameters_app.command("list")
def cmd_diameters_list(db_path: Optional[str] = typer.Option(None, help="Chemin vers la DB YAML/SQLite")):
    """Liste les diamètres candidats disponibles."""
    candidates = get_candidate_diameters(db_path)
    table = Table(title="Diamètres Candidats")
    table.add_column("Diamètre (mm)", justify="right")
    table.add_column("Coût/m", justify="right")
    table.add_column("Matériau")
    for d in candidates:
        table.add_row(str(d["d_mm"]), f"{d.get('cost_per_m', 'N/A'):.2f}", d.get("material", "N/A"))
    console = Console()
    console.print(table)
