"""
Commandes CLI pour l'optimisation AEP (V11).

Ce module s'intègre avec l'architecture CLI existante de LCPI
et ajoute les commandes manquantes pour l'optimisation.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
import yaml
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .models import OptimizationConfig, OptimizationObjectives
from .output import formatter, save_optimization_result_v11
from .report_adapter import v11_adapter
from .algorithms.global_opt import GlobalOptimizer
from .algorithms.nested import NestedGreedyOptimizer
from .algorithms.multi_tank import MultiTankOptimizer
from .algorithms.surrogate import SurrogateOptimizer
from .db_dao import prices_dao, get_candidate_diameters
from .pareto import compute_pareto, knee_point
from .io import load_yaml_or_inp

console = Console()

# Typer app to expose commands under `lcpi aep optimizer`
app = typer.Typer(name="optimizer", help="Commandes d'optimisation AEP (V11)")


class AEPOptimizationCLI:
    """Interface CLI pour l'optimisation AEP (V11)."""
    
    def __init__(self):
        """Initialise l'interface CLI."""
        pass
    
    def price_optimize(self, network: Path, lambda_opex: float = 10.0, 
                      method: str = "nested", output: Optional[Path] = None,
                      config_file: Optional[Path] = None) -> None:
        """
        Optimise avec score pondéré J = CAPEX + lambda·OPEX_NPV.
        
        Args:
            network: Fichier réseau (.inp)
            lambda_opex: Facteur de pondération pour l'OPEX
            method: Méthode d'optimisation
            output: Fichier de sortie
            config_file: Fichier de configuration YAML
        """
        try:
            # Charger la configuration
            config = self._load_optimization_config(config_file, lambda_opex, method)
            
            # Valider le réseau
            if not self._validate_network(network):
                raise typer.BadParameter("Fichier réseau invalide")
            
            # Lancer l'optimisation
            console.print(f"🚀 [bold blue]Démarrage de l'optimisation avec lambda = {lambda_opex}[/bold blue]")
            console.print(f"📁 Réseau: {network}")
            console.print(f"⚙️  Méthode: {method}")
            
            # Convertir l'entrée en NetworkModel si nécessaire (INP)
            network_model, _meta = load_yaml_or_inp(Path(network))
            result = self._run_optimization((network, network_model), config)
            
            # Formater et sauvegarder le résultat
            if output:
                self._save_and_display_result(result, output, config)
            else:
                # Générer un nom de fichier par défaut
                default_output = Path(f"optimization_result_{method}_{lambda_opex}.json")
                self._save_and_display_result(result, default_output, config)
                
        except Exception as e:
            console.print(f"❌ [bold red]Erreur lors de l'optimisation: {e}[/bold red]")
            raise typer.Exit(code=1)
    
    def report(self, results_file: Path, template: str = "default", 
              output: Optional[Path] = None) -> None:
        """
        Régénère un rapport d'optimisation.
        
        Args:
            results_file: Fichier de résultats JSON V11
            template: Template de rapport à utiliser
            output: Fichier de sortie HTML
        """
        try:
            # Charger les résultats
            if not results_file.exists():
                raise typer.BadParameter(f"Fichier de résultats introuvable: {results_file}")
            
            results_data = formatter.load_v11_json(results_file)
            
            # Valider le format V11
            if not formatter.validate_v11_format(results_data):
                raise typer.BadParameter("Format de résultats V11 invalide")
            
            # Générer le rapport
            console.print(f"📊 [bold blue]Génération du rapport depuis {results_file}[/bold blue]")
            
            from ...reporting.report_generator import ReportGenerator
            report_gen = ReportGenerator(Path("src/lcpi/reporting/templates"))
            
            # Générer le rapport HTML
            html_content = self._generate_html_report(results_data, template)
            
            # Sauvegarder le rapport
            if output:
                output_path = output
            else:
                output_path = results_file.with_suffix('.html')
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            console.print(f"✅ [bold green]Rapport généré: {output_path}[/bold green]")
            
        except Exception as e:
            console.print(f"❌ [bold red]Erreur lors de la génération du rapport: {e}[/bold red]")
            raise typer.Exit(code=1)
    
    def diameters_manage(self, action: str, diameter_mm: Optional[int] = None, 
                        price_fcfa: Optional[float] = None) -> None:
        """
        Gère la base de données des diamètres disponibles.
        
        Args:
            action: Action à effectuer (list, add, remove, update)
            diameter_mm: Diamètre en mm (pour add/remove/update)
            price_fcfa: Prix en FCFA (pour add/update)
        """
        try:
            if action == "list":
                self._list_diameters()
            elif action == "add":
                if diameter_mm is None or price_fcfa is None:
                    raise typer.BadParameter("Les paramètres diameter_mm et price_fcfa sont requis pour l'ajout")
                self._add_diameter(diameter_mm, price_fcfa)
            elif action == "remove":
                if diameter_mm is None:
                    raise typer.BadParameter("Le paramètre diameter_mm est requis pour la suppression")
                self._remove_diameter(diameter_mm)
            elif action == "update":
                if diameter_mm is None or price_fcfa is None:
                    raise typer.BadParameter("Les paramètres diameter_mm et price_fcfa sont requis pour la mise à jour")
                self._update_diameter(diameter_mm, price_fcfa)
            else:
                raise typer.BadParameter(f"Action non reconnue: {action}")
                
        except Exception as e:
            console.print(f"❌ [bold red]Erreur lors de la gestion des diamètres: {e}[/bold red]")
            raise typer.Exit(code=1)
    
    def _load_optimization_config(self, config_file: Optional[Path], 
                                lambda_opex: float, method: str) -> OptimizationConfig:
        """Charge ou crée la configuration d'optimisation."""
        if config_file and config_file.exists():
            # Charger depuis le fichier
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
        else:
            # Configuration par défaut
            config_data = {
                "method": method,
                "objectives": {
                    "capex": True,
                    "opex": True,
                    "lambda_opex": lambda_opex
                },
                "h_bounds_m": {"TANK1": (50.0, 100.0)},
                "pressure_min_m": 10.0
            }
        
        return OptimizationConfig(**config_data)
    
    def _validate_network(self, network_path: str | Path) -> bool:
        """Valide le fichier réseau."""
        # Convertir en Path si nécessaire
        if isinstance(network_path, str):
            network_path = Path(network_path)
        
        if not network_path.exists():
            return False
        
        # Vérifier l'extension
        if network_path.suffix.lower() != '.inp':
            return False
        
        # Vérifier le contenu de base
        try:
            content = network_path.read_text(encoding='utf-8')
            required_sections = ['[JUNCTIONS]', '[PIPES]', '[RESERVOIRS]']
            return all(section in content for section in required_sections)
        except Exception:
            return False
    
    def _run_optimization(self, network_input: Any, config: OptimizationConfig) -> Any:
        """Lance l'optimisation selon la méthode configurée."""
        method = config.method
        # network_input = (path, network_model)
        if isinstance(network_input, tuple):
            network_path, network_model = network_input
        else:
            network_path, network_model = network_input, None

        if method == "global":
            optimizer = GlobalOptimizer(config, network_path)
            return optimizer.optimize()
        elif method == "nested":
            # Utiliser le chemin du réseau pour permettre la simulation EPANET réelle
            optimizer = NestedGreedyOptimizer(network_path, solver="epanet")
            # Extraire bornes et contraintes depuis la config
            try:
                h_bounds = list(config.h_bounds_m.values())[0]
            except Exception:
                h_bounds = (50.0, 100.0)
            return optimizer.optimize_nested(
                H_bounds=h_bounds,
                pressure_min_m=config.pressure_min_m,
                velocity_constraints=None,
                diameter_db_path=None
            )
        elif method == "multi-tank":
            optimizer = MultiTankOptimizer(network_path, config.model_dump())
            return optimizer.optimize()
        elif method == "surrogate":
            optimizer = SurrogateOptimizer(network_path, config.model_dump())
            return optimizer.build_and_optimize()
        else:
            raise ValueError(f"Méthode d'optimisation non supportée: {method}")
    
    def _save_and_display_result(self, result: Any, output_path: Path, config: OptimizationConfig) -> None:
        """Sauvegarde et affiche le résultat."""
        # Convertir le résultat brut en format V11
        v11_result = self._convert_to_v11_format(result, config)
        
        # Sauvegarder au format V11
        save_optimization_result_v11(v11_result, output_path)
        
        # Sauvegarder aussi au format compatible avec 'lcpi rapport'
        log_output_path = output_path.with_suffix('.log.json')
        execution_metadata = {
            "execution_time": "N/A",  # À calculer dans une version future
            "lambda_opex": config.objectives.lambda_opex,
            "command": "price-optimize"
        }
        log_id = v11_adapter.save_v11_result_as_log(v11_result, log_output_path, execution_metadata)
        
        # Afficher un résumé
        self._display_optimization_summary(v11_result)
        
        console.print(f"✅ [bold green]Résultats sauvegardés: {output_path}[/bold green]")
        console.print(f"📋 [bold blue]Log compatible 'lcpi rapport': {log_output_path}[/bold blue]")
        console.print(f"🆔 [dim]Log ID: {log_id}[/dim]")
    
    def _convert_to_v11_format(self, raw_result: Any, config: OptimizationConfig) -> Any:
        """Convertit le résultat brut au format V11."""
        # Cette méthode doit être adaptée selon le format de sortie de chaque optimiseur
        # Pour l'instant, on retourne le résultat tel quel
        return raw_result
    
    def _display_optimization_summary(self, result: Any) -> None:
        """Affiche un résumé de l'optimisation."""
        console.print("\n📊 [bold blue]Résumé de l'optimisation[/bold blue]")
        
        # Afficher les informations de base
        if hasattr(result, 'proposals') and result.proposals:
            table = Table(title="Propositions d'optimisation")
            table.add_column("Nom", style="cyan")
            table.add_column("Faisable", style="green")
            table.add_column("CAPEX (FCFA)", style="yellow")
            table.add_column("OPEX NPV (FCFA)", style="magenta")
            
            for proposal in result.proposals:
                capex = proposal.costs.get("CAPEX", 0) if hasattr(proposal, 'costs') else 0
                opex = proposal.costs.get("OPEX_npv", 0) if hasattr(proposal, 'costs') else 0
                
                table.add_row(
                    proposal.name,
                    "✅" if proposal.is_feasible else "❌",
                    f"{capex:,.0f}",
                    f"{opex:,.0f}"
                )
            
            console.print(table)
    
    def _generate_html_report(self, results_data: Dict[str, Any], template: str) -> str:
        """Génère le rapport HTML."""
        # Utiliser le template V11 de LCPI AEP
        template_path = Path("src/lcpi/aep/templates/optimisation_tank_v11.jinja2")
        
        if template_path.exists():
            from jinja2 import Environment, FileSystemLoader
            env = Environment(loader=FileSystemLoader(template_path.parent))
            template_obj = env.get_template(template_path.name)
            
            # Préparer le contexte
            context = {
                "proposals": results_data.get("proposals", []),
                "pareto_front": results_data.get("pareto_front", []),
                "metadata": results_data.get("metadata", {}),
                "now": datetime.now()
            }
            
            return template_obj.render(**context)
        else:
            # Template de fallback
            return self._generate_fallback_html_report(results_data)
    
    def _generate_fallback_html_report(self, results_data: Dict[str, Any]) -> str:
        """Génère un rapport HTML de fallback."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rapport d'Optimisation AEP V11</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Rapport d'Optimisation AEP V11</h1>
            <h2>Propositions</h2>
            <table>
                <tr><th>Nom</th><th>Faisable</th><th>CAPEX</th><th>OPEX NPV</th></tr>
        """
        
        for proposal in results_data.get("proposals", []):
            html += f"""
                <tr>
                    <td>{proposal.get('name', 'N/A')}</td>
                    <td>{'Oui' if proposal.get('is_feasible') else 'Non'}</td>
                    <td>{proposal.get('costs', {}).get('CAPEX', 'N/A')}</td>
                    <td>{proposal.get('costs', {}).get('OPEX_npv', 'N/A')}</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        return html
    
    def _list_diameters(self) -> None:
        """Liste tous les diamètres disponibles."""
        diameters = get_candidate_diameters()
        
        if not diameters:
            console.print("⚠️  [yellow]Aucun diamètre trouvé dans la base de données[/yellow]")
            return
        
        table = Table(title="Diamètres disponibles (PVC-U)")
        table.add_column("DN (mm)", style="cyan")
        table.add_column("Fourniture (FCFA/m)", style="green")
        table.add_column("Pose (FCFA/m)", style="blue")
        table.add_column("Total (FCFA/m)", style="yellow")
        
        for diam in diameters:
            total = float(diam.get('cost_per_m', 0) or 0)
            supply = diam.get('supply_fcfa_per_m')
            pose = diam.get('pose_fcfa_per_m')
            # Si la DB renvoie seulement un total, estimer une répartition affichage 70/30
            if supply is None and pose is None and total:
                supply = total * 0.7
                pose = total * 0.3
            supply = float(supply or 0)
            pose = float(pose or 0)
            
            table.add_row(
                str(diam.get("d_mm", "?")),
                f"{supply:,.0f}",
                f"{pose:,.0f}",
                f"{total:,.0f}"
            )
        
        console.print(table)
        
        # Afficher des statistiques
        total_diameters = len(diameters)
        try:
            min_price = min(float(d.get('cost_per_m', 0) or 0) for d in diameters)
            max_price = max(float(d.get('cost_per_m', 0) or 0) for d in diameters)
            console.print(f"\n📊 [dim]Statistiques: {total_diameters} diamètres, prix de {min_price:,.0f} à {max_price:,.0f} FCFA/m[/dim]")
        except Exception:
            console.print(f"\n📊 [dim]{total_diameters} diamètres listés[/dim]")
    
    def _add_diameter(self, diameter_mm: int, price_fcfa: float) -> None:
        """Ajoute un nouveau diamètre."""
        # Demander les prix séparés
        console.print(f"➕ [bold green]Ajout du diamètre {diameter_mm}mm[/bold green]")
        
        # Pour l'instant, on divise le prix total en fourniture (70%) et pose (30%)
        supply_price = price_fcfa * 0.7
        pose_price = price_fcfa * 0.3
        
        success = prices_dao.add_diameter(diameter_mm, "PVC-U", supply_price, pose_price)
        if success:
            console.print(f"✅ Diamètre {diameter_mm}mm ajouté avec succès")
            console.print(f"   - Fourniture: {supply_price:,.0f} FCFA/m")
            console.print(f"   - Pose: {pose_price:,.0f} FCFA/m")
            console.print(f"   - Total: {price_fcfa:,.0f} FCFA/m")
        else:
            console.print(f"❌ Erreur lors de l'ajout du diamètre {diameter_mm}mm")
    
    def _remove_diameter(self, diameter_mm: int) -> None:
        """Supprime un diamètre."""
        console.print(f"➖ [bold red]Suppression du diamètre {diameter_mm}mm[/bold red]")
        
        success = prices_dao.remove_diameter(diameter_mm, "PVC-U")
        if success:
            console.print(f"✅ Diamètre {diameter_mm}mm supprimé avec succès")
        else:
            console.print(f"❌ Erreur lors de la suppression du diamètre {diameter_mm}mm")
    
    def _update_diameter(self, diameter_mm: int, price_fcfa: float) -> None:
        """Met à jour le prix d'un diamètre."""
        console.print(f"🔄 [bold blue]Mise à jour du diamètre {diameter_mm}mm[/bold blue]")
        
        # Pour l'instant, on divise le prix total en fourniture (70%) et pose (30%)
        supply_price = price_fcfa * 0.7
        pose_price = price_fcfa * 0.3
        
        success = prices_dao.update_diameter(diameter_mm, "PVC-U", supply_price, pose_price)
        if success:
            console.print(f"✅ Diamètre {diameter_mm}mm mis à jour avec succès")
            console.print(f"   - Nouveau prix total: {price_fcfa:,.0f} FCFA/m")
            console.print(f"   - Fourniture: {supply_price:,.0f} FCFA/m")
            console.print(f"   - Pose: {pose_price:,.0f} FCFA/m")
        else:
            console.print(f"❌ Erreur lors de la mise à jour du diamètre {diameter_mm}mm")


# Instance globale pour utilisation
cli = AEPOptimizationCLI()


# Typer command wrappers
@app.command("price-optimize")
def cmd_price_optimize(
    network: Path,
    method: str = typer.Option("nested", "--method"),
    lambda_opex: float = typer.Option(10.0, "--lambda-opex"),
    output: Optional[Path] = typer.Option(None, "--output"),
    config_file: Optional[Path] = typer.Option(None, "--config")
):
    """Optimise J = CAPEX + λ·OPEX_NPV et produit un JSON V11 + log LCPI."""
    cli.price_optimize(network=network, lambda_opex=lambda_opex, method=method, output=output, config_file=config_file)


@app.command("report")
def cmd_report(
    results_file: Path,
    template: str = typer.Option("optimisation_tank_v11.jinja2", "--template"),
    output: Optional[Path] = typer.Option(None, "--output")
):
    """Génère un rapport HTML à partir d'un JSON V11."""
    cli.report(results_file=results_file, template=template, output=output)


@app.command("diameters-manage")
def cmd_diameters_manage(
    action: str = typer.Argument(..., help="list|add|remove|update"),
    diameter_mm: Optional[int] = typer.Option(None, "--dn"),
    price_fcfa: Optional[float] = typer.Option(None, "--price")
):
    """Gère la base des diamètres (lecture et mises à jour)."""
    cli.diameters_manage(action=action, diameter_mm=diameter_mm, price_fcfa=price_fcfa)
