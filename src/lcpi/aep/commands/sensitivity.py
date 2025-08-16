"""
Commandes CLI pour l'analyse de sensibilité parallélisée AEP.

Ce module implémente :
- Analyse Monte Carlo parallélisée
- Distribution des tâches entre workers
- Intégration avec le cache intelligent
- Monitoring des performances
"""

import typer
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from ..optimization.parallel_monte_carlo import run_parallel_monte_carlo
from ..core.cache_manager import get_cache_manager
from ..utils.performance_monitor import get_performance_monitor, profile_algorithm

app = typer.Typer(help="📊 Analyse de sensibilité parallélisée AEP")
console = Console()


@app.command("parallel")
def parallel_sensitivity_cli(
    config_file: Path = typer.Argument(..., help="Fichier de configuration du réseau"),
    workers: int = typer.Option(4, "--workers", "-w", help="Nombre de workers pour la parallélisation"),
    simulations: int = typer.Option(1000, "--simulations", "-s", help="Nombre de simulations Monte Carlo"),
    solver: str = typer.Option("lcpi", "--solver", "-S", help="Solveur hydraulique à utiliser"),
    use_cache: bool = typer.Option(True, "--use-cache", help="Utiliser le cache intelligent"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour les résultats")
):
    """🚀 Analyse Monte Carlo parallélisée pour l'analyse de sensibilité."""
    
    console.print(Panel.fit("🚀 [bold blue]Analyse Monte Carlo Parallélisée[/bold blue]"))
    
    try:
        # Charger la configuration du réseau
        with console.status("[bold green]Chargement de la configuration..."):
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                network_config = yaml.safe_load(f)
        
        # Configuration des distributions de paramètres
        console.print("📋 Configuration des distributions de paramètres...")
        
        # Distributions par défaut (à personnaliser selon les besoins)
        parameter_distributions = {
            "node_demand": {
                "type": "normal",
                "mean": 0.001,
                "std": 0.0002,
                "min": 0.0001,
                "max": 0.002
            },
            "pipe_roughness": {
                "type": "uniform",
                "min": 100,
                "max": 150
            },
            "pipe_diameter": {
                "type": "normal",
                "mean": 150,
                "std": 20,
                "min": 100,
                "max": 200
            }
        }
        
        # Afficher la configuration
        config_table = Table(title="⚙️ Configuration de l'Analyse")
        config_table.add_column("Paramètre", style="cyan")
        config_table.add_column("Valeur", style="white")
        
        config_table.add_row("Workers", str(workers))
        config_table.add_row("Simulations", str(simulations))
        config_table.add_row("Solveur", solver)
        config_table.add_row("Cache", "✅ Activé" if use_cache else "❌ Désactivé")
        config_table.add_row("Distributions", str(len(parameter_distributions)))
        
        console.print(config_table)
        
        # Afficher les distributions
        dist_table = Table(title="📊 Distributions des Paramètres")
        dist_table.add_column("Paramètre", style="cyan")
        dist_table.add_column("Type", style="green")
        dist_table.add_column("Paramètres", style="white")
        
        for param_name, dist_config in parameter_distributions.items():
            dist_type = dist_config["type"]
            if dist_type == "normal":
                params = f"μ={dist_config['mean']}, σ={dist_config['std']}"
            elif dist_type == "uniform":
                params = f"min={dist_config['min']}, max={dist_config['max']}"
            else:
                params = str(dist_config)
            
            dist_table.add_row(param_name, dist_type, params)
        
        console.print(dist_table)
        
        # Lancer l'analyse Monte Carlo parallélisée
        console.print(f"\n🚀 Lancement de l'analyse avec {workers} workers...")
        
        with console.status("[bold blue]Analyse Monte Carlo en cours..."):
            with profile_algorithm("monte_carlo_parallel") as profiler:
                results = run_parallel_monte_carlo(
                    base_network=network_config,
                    parameter_distributions=parameter_distributions,
                    num_simulations=simulations,
                    solver_name=solver,
                    max_workers=workers,
                    use_cache=use_cache
                )
        
        # Affichage des résultats
        console.print(f"\n✅ Analyse terminée en {results['execution_time']:.2f} secondes")
        
        # Statistiques de l'analyse
        analysis = results['analysis']
        stats_table = Table(title="📊 Résultats de l'Analyse Monte Carlo")
        stats_table.add_column("Métrique", style="cyan")
        stats_table.add_column("Valeur", style="white")
        
        stats_table.add_row("Total de simulations", str(analysis['total_simulations']))
        stats_table.add_row("Simulations réussies", str(analysis['successful_simulations']))
        stats_table.add_row("Simulations échouées", str(analysis['failed_simulations']))
        stats_table.add_row("Taux de succès", f"{analysis['success_rate']*100:.1f}%")
        stats_table.add_row("Taux de cache", f"{analysis['cache_hit_rate']*100:.1f}%")
        stats_table.add_row("Temps moyen par simulation", f"{analysis['average_execution_time']:.3f}s")
        
        console.print(stats_table)
        
        # Statistiques des workers
        stats = results['stats']
        workers_table = Table(title="⚡ Statistiques des Workers")
        workers_table.add_column("Métrique", style="cyan")
        workers_table.add_column("Valeur", style="white")
        
        workers_table.add_row("Workers utilisés", str(workers))
        workers_table.add_row("Tâches totales", str(stats['total_tasks']))
        workers_table.add_row("Tâches complétées", str(stats['completed_tasks']))
        workers_table.add_row("Cache hits", str(stats['cache_hits']))
        workers_table.add_row("Cache misses", str(stats['cache_misses']))
        workers_table.add_row("Erreurs", str(stats['errors']))
        
        console.print(workers_table)
        
        # Export des résultats si demandé
        if output:
            import json
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            console.print(f"💾 Résultats exportés vers: {output}")
        
        # Recommandations
        console.print("\n💡 Recommandations:")
        if analysis['success_rate'] < 0.9:
            console.print("  ⚠️  Taux de succès faible - vérifiez les paramètres des distributions")
        
        if analysis['cache_hit_rate'] < 0.1:
            console.print("  💡 Taux de cache faible - augmentez la taille du cache ou réutilisez les réseaux")
        
        if results['execution_time'] > 60:
            console.print("  ⚡ Temps d'exécution élevé - augmentez le nombre de workers")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'analyse: {e}", style="red")
        raise typer.Exit(code=1)


@app.command("distributions")
def configure_distributions_cli(
    config_file: Path = typer.Option(..., "--config", "-c", help="Fichier de configuration du réseau"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour les distributions")
):
    """📋 Configurer les distributions de paramètres pour l'analyse de sensibilité."""
    
    console.print(Panel.fit("📋 [bold blue]Configuration des Distributions de Paramètres[/bold blue]"))
    
    try:
        # Charger la configuration du réseau
        with console.status("[bold green]Chargement de la configuration..."):
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                network_config = yaml.safe_load(f)
        
        # Analyser la structure du réseau pour suggérer des distributions
        console.print("🔍 Analyse de la structure du réseau...")
        
        nodes = network_config.get("nodes", {})
        pipes = network_config.get("pipes", {})
        
        # Distributions suggérées basées sur la structure du réseau
        suggested_distributions = {}
        
        if nodes:
            # Analyser les demandes des nœuds
            demands = [node.get("demand", 0) for node in nodes.values() if "demand" in node]
            if demands:
                avg_demand = sum(demands) / len(demands)
                suggested_distributions["node_demand"] = {
                    "type": "normal",
                    "mean": avg_demand,
                    "std": avg_demand * 0.2,  # 20% de variation
                    "min": avg_demand * 0.5,
                    "max": avg_demand * 1.5,
                    "description": "Demande des nœuds de distribution"
                }
        
        if pipes:
            # Analyser les diamètres des conduites
            diameters = [pipe.get("diameter", 150) for pipe in pipes.values() if "diameter" in pipe]
            if diameters:
                avg_diameter = sum(diameters) / len(diameters)
                suggested_distributions["pipe_diameter"] = {
                    "type": "normal",
                    "mean": avg_diameter,
                    "std": avg_diameter * 0.1,  # 10% de variation
                    "min": avg_diameter * 0.8,
                    "max": avg_diameter * 1.2,
                    "description": "Diamètres des conduites"
                }
            
            # Analyser les rugosités
            roughnesses = [pipe.get("roughness", 120) for pipe in pipes.values() if "roughness" in pipe]
            if roughnesses:
                avg_roughness = sum(roughnesses) / len(roughnesses)
                suggested_distributions["pipe_roughness"] = {
                    "type": "uniform",
                    "min": avg_roughness * 0.8,
                    "max": avg_roughness * 1.2,
                    "description": "Rugosité des conduites"
                }
        
        # Affichage des distributions suggérées
        if suggested_distributions:
            console.print("💡 Distributions suggérées basées sur votre réseau:")
            
            for param_name, dist_config in suggested_distributions.items():
                console.print(f"\n📊 {param_name}:")
                console.print(f"  Description: {dist_config.get('description', 'N/A')}")
                console.print(f"  Type: {dist_config['type']}")
                
                if dist_config['type'] == "normal":
                    console.print(f"  Moyenne: {dist_config['mean']}")
                    console.print(f"  Écart-type: {dist_config['std']}")
                    console.print(f"  Min: {dist_config['min']}")
                    console.print(f"  Max: {dist_config['max']}")
                elif dist_config['type'] == "uniform":
                    console.print(f"  Min: {dist_config['min']}")
                    console.print(f"  Max: {dist_config['max']}")
        else:
            console.print("⚠️  Aucune distribution suggérée - structure du réseau non reconnue")
        
        # Export des distributions si demandé
        if output:
            distributions_data = {
                "network_config": config_file.name,
                "distributions": suggested_distributions,
                "generated_at": str(datetime.now()),
                "description": "Distributions de paramètres suggérées pour l'analyse de sensibilité"
            }
            
            import json
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(distributions_data, f, indent=2, ensure_ascii=False)
            
            console.print(f"💾 Distributions exportées vers: {output}")
        
        # Instructions d'utilisation
        console.print("\n📋 Instructions d'utilisation:")
        console.print("1. Modifiez les distributions selon vos besoins")
        console.print("2. Utilisez la commande 'sensitivity parallel' avec votre fichier de distributions")
        console.print("3. Ajustez le nombre de workers selon votre machine")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de la configuration: {e}", style="red")
        raise typer.Exit(code=1)


@app.command("validate")
def validate_distributions_cli(
    distributions_file: Path = typer.Argument(..., help="Fichier de distributions à valider")
):
    """✅ Valider un fichier de distributions de paramètres."""
    
    console.print(Panel.fit("✅ [bold blue]Validation des Distributions de Paramètres[/bold blue]"))
    
    try:
        # Charger le fichier de distributions
        with console.status("[bold green]Chargement des distributions..."):
            import yaml
            with open(distributions_file, 'r', encoding='utf-8') as f:
                distributions = yaml.safe_load(f)
        
        # Validation des distributions
        validation_results = []
        errors = []
        warnings = []
        
        for param_name, dist_config in distributions.items():
            param_validation = {"param_name": param_name, "valid": True, "issues": []}
            
            # Vérifier la présence des champs requis
            required_fields = {
                "normal": ["type", "mean", "std"],
                "uniform": ["type", "min", "max"],
                "lognormal": ["type", "mean", "std"],
                "discrete": ["type", "values"]
            }
            
            dist_type = dist_config.get("type")
            if not dist_type:
                param_validation["valid"] = False
                param_validation["issues"].append("Type de distribution manquant")
                errors.append(f"{param_name}: Type manquant")
                continue
            
            if dist_type not in required_fields:
                param_validation["valid"] = False
                param_validation["issues"].append(f"Type de distribution non supporté: {dist_type}")
                errors.append(f"{param_name}: Type non supporté")
                continue
            
            # Vérifier les champs requis
            for field in required_fields[dist_type]:
                if field not in dist_config:
                    param_validation["valid"] = False
                    param_validation["issues"].append(f"Champ requis manquant: {field}")
                    errors.append(f"{param_name}: Champ {field} manquant")
            
            # Vérifications spécifiques par type
            if dist_type == "normal":
                if "mean" in dist_config and "std" in dist_config:
                    if dist_config["std"] <= 0:
                        param_validation["valid"] = False
                        param_validation["issues"].append("Écart-type doit être positif")
                        errors.append(f"{param_name}: Écart-type non positif")
            
            elif dist_type == "uniform":
                if "min" in dist_config and "max" in dist_config:
                    if dist_config["min"] >= dist_config["max"]:
                        param_validation["valid"] = False
                        param_validation["issues"].append("Min doit être < Max")
                        errors.append(f"{param_name}: Min >= Max")
            
            elif dist_type == "discrete":
                if "values" in dist_config:
                    if not isinstance(dist_config["values"], list) or len(dist_config["values"]) == 0:
                        param_validation["valid"] = False
                        param_validation["issues"].append("Values doit être une liste non vide")
                        errors.append(f"{param_name}: Values invalide")
            
            validation_results.append(param_validation)
        
        # Affichage des résultats de validation
        console.print(f"📊 Validation terminée pour {len(distributions)} paramètres")
        
        # Résumé
        valid_count = sum(1 for r in validation_results if r["valid"])
        invalid_count = len(validation_results) - valid_count
        
        summary_table = Table(title="📋 Résumé de la Validation")
        summary_table.add_column("Statut", style="bold")
        summary_table.add_column("Nombre", style="white")
        
        summary_table.add_row("✅ Valides", str(valid_count))
        summary_table.add_row("❌ Invalides", str(invalid_count))
        summary_table.add_row("Total", str(len(distributions)))
        
        console.print(summary_table)
        
        # Détails des erreurs
        if errors:
            console.print("\n❌ Erreurs détectées:")
            for error in errors:
                console.print(f"  - {error}")
        
        # Détails des avertissements
        if warnings:
            console.print("\n⚠️  Avertissements:")
            for warning in warnings:
                console.print(f"  - {warning}")
        
        # Statut global
        if invalid_count == 0:
            console.print("\n🎉 Toutes les distributions sont valides !")
        else:
            console.print(f"\n⚠️  {invalid_count} distribution(s) à corriger")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de la validation: {e}", style="red")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
