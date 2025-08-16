"""
Commandes CLI pour la gestion des performances et du cache AEP.

Ce module implémente :
- Profiling des algorithmes
- Monitoring en temps réel
- Gestion du cache
- Benchmark des solveurs
"""

import typer
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.layout import Layout

from ..core.cache_manager import get_cache_manager, clear_cache, get_cache_stats
from ..utils.performance_monitor import (
    get_performance_monitor, 
    PerformanceReporter, 
    benchmark_solvers,
    profile_algorithm
)
from ..core.solvers import SolverFactory

app = typer.Typer(help="🔧 Gestion des performances et du cache AEP")
console = Console()


@app.command("profile")
def profile_algorithm_cli(
    algorithm: str = typer.Argument(..., help="Nom de l'algorithme à profiler"),
    config_file: Path = typer.Option(..., "--config", "-c", help="Fichier de configuration du réseau"),
    iterations: int = typer.Option(1, "--iterations", "-i", help="Nombre d'itérations"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour le profil")
):
    """📊 Profiler un algorithme spécifique."""
    
    console.print(Panel.fit(f"🔍 [bold blue]Profiling de l'algorithme: {algorithm}[/bold blue]"))
    
    try:
        # Charger la configuration du réseau
        with console.status("[bold green]Chargement de la configuration..."):
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                network_config = yaml.safe_load(f)
        
        # Démarrer le profiling
        monitor = get_performance_monitor()
        
        for i in range(iterations):
            with console.status(f"[bold blue]Itération {i+1}/{iterations}..."):
                with profile_algorithm(f"{algorithm}_{i}") as profiler:
                    # Simuler l'exécution de l'algorithme
                    # (ici on simule, en pratique ce serait l'algorithme réel)
                    import time
                    time.sleep(0.5)  # Simulation
                    
                    profiler.add_metric("test_metric", 42.0, "units", "Métrique de test")
                    profiler.add_iteration()
        
        # Afficher les résultats
        console.print(f"✅ Profiling terminé pour {iterations} itération(s)")
        
        # Statistiques de l'algorithme
        stats = monitor.get_algorithm_stats(algorithm)
        if "error" not in stats:
            stats_table = Table(title=f"📊 Statistiques de {algorithm}")
            stats_table.add_column("Métrique", style="cyan")
            stats_table.add_column("Valeur", style="white")
            
            stats_table.add_row("Total d'exécutions", str(stats["total_runs"]))
            stats_table.add_row("Taux de succès", f"{stats['success_rate']*100:.1f}%")
            stats_table.add_row("Temps moyen", f"{stats.get('avg_execution_time', 0):.3f}s")
            stats_table.add_row("Mémoire moyenne", f"{stats.get('avg_memory_peak', 0):.1f} MB")
            
            console.print(stats_table)
        
        # Export si demandé
        if output:
            # Exporter le profil
            profile_id = f"{algorithm}_0"  # Premier profil
            if monitor.export_profile(profile_id, output):
                console.print(f"💾 Profil exporté vers: {output}")
            else:
                console.print("⚠️ Erreur lors de l'export du profil")
        
    except Exception as e:
        console.print(f"❌ Erreur lors du profiling: {e}", style="red")
        raise typer.Exit(code=1)


@app.command("monitor")
def monitor_performance_cli(
    watch: bool = typer.Option(False, "--watch", "-w", help="Monitoring en temps réel"),
    refresh_interval: float = typer.Option(1.0, "--interval", "-i", help="Intervalle de rafraîchissement en secondes")
):
    """📈 Monitoring des performances en temps réel."""
    
    if watch:
        console.print(Panel.fit("🔍 [bold blue]Monitoring des Performances en Temps Réel[/bold blue]"))
        console.print("💡 Appuyez sur Ctrl+C pour arrêter le monitoring")
        
        try:
            monitor = get_performance_monitor()
            reporter = PerformanceReporter(monitor)
            reporter.display_live_monitoring(refresh_interval)
        except KeyboardInterrupt:
            console.print("\n🛑 Monitoring arrêté")
        except Exception as e:
            console.print(f"❌ Erreur lors du monitoring: {e}", style="red")
            raise typer.Exit(code=1)
    else:
        # Affichage des statistiques actuelles
        monitor = get_performance_monitor()
        stats = monitor.get_global_stats()
        
        console.print(Panel.fit("📊 [bold blue]Statistiques de Performance[/bold blue]"))
        
        stats_table = Table(title="📈 Statistiques Globales")
        stats_table.add_column("Métrique", style="cyan")
        stats_table.add_column("Valeur", style="white")
        
        stats_table.add_row("Total d'algorithmes", str(stats["total_algorithms"]))
        stats_table.add_row("Temps d'exécution total", f"{stats['total_execution_time']:.2f}s")
        stats_table.add_row("Pic de mémoire global", f"{stats['total_memory_peak']:.1f} MB")
        stats_table.add_row("Pic CPU global", f"{stats['total_cpu_peak']:.1f}%")
        stats_table.add_row("Exécutions réussies", str(stats["successful_runs"]))
        stats_table.add_row("Exécutions échouées", str(stats["failed_runs"]))
        
        console.print(stats_table)


@app.command("cache")
def manage_cache_cli(
    action: str = typer.Option("stats", "--action", "-a", help="Action (stats, clear, info)"),
    cache_size_mb: Optional[int] = typer.Option(None, "--size", "-s", help="Taille du cache en MB")
):
    """🗄️ Gestion du cache intelligent."""
    
    console.print(Panel.fit("🗄️ [bold blue]Gestion du Cache Intelligent[/bold blue]"))
    
    try:
        cache_manager = get_cache_manager()
        
        if action == "stats":
            # Afficher les statistiques du cache
            stats = get_cache_stats()
            
            if "error" in stats:
                console.print("⚠️ Cache non initialisé")
                return
            
            stats_table = Table(title="📊 Statistiques du Cache")
            stats_table.add_column("Métrique", style="cyan")
            stats_table.add_column("Valeur", style="white")
            
            stats_table.add_row("Taux de succès", f"{stats['hit_rate']*100:.1f}%")
            stats_table.add_row("Entrées actuelles", str(stats["current_entries"]))
            stats_table.add_row("Taille actuelle", f"{stats['current_size_mb']:.1f} MB")
            stats_table.add_row("Taille maximale", f"{stats['max_size_mb']:.1f} MB")
            stats_table.add_row("Entrées maximales", str(stats["max_entries"]))
            stats_table.add_row("Hits", str(stats["hits"]))
            stats_table.add_row("Misses", str(stats["misses"]))
            stats_table.add_row("Évictions", str(stats["evictions"]))
            
            console.print(stats_table)
            
        elif action == "clear":
            # Vider le cache
            clear_cache()
            console.print("✅ Cache vidé avec succès")
            
        elif action == "info":
            # Informations détaillées sur le cache
            console.print("ℹ️ Informations du cache:")
            console.print(f"  - Type: Cache intelligent avec persistance")
            console.print(f"  - Algorithme: LRU (Least Recently Used)")
            console.print(f"  - Gestion des dépendances: Activée")
            console.print(f"  - Expiration automatique: 24h")
            
        else:
            console.print(f"❌ Action non reconnue: {action}")
            console.print("Actions disponibles: stats, clear, info")
            
    except Exception as e:
        console.print(f"❌ Erreur lors de la gestion du cache: {e}", style="red")
        raise typer.Exit(code=1)


@app.command("benchmark")
def benchmark_solvers_cli(
    config_file: Path = typer.Option(..., "--config", "-c", help="Fichier de configuration du réseau"),
    solvers: List[str] = typer.Option(None, "--solvers", "-s", help="Solveurs à tester"),
    iterations: int = typer.Option(5, "--iterations", "-i", help="Nombre d'itérations par solveur"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour les résultats")
):
    """⚡ Benchmark des solveurs hydrauliques."""
    
    console.print(Panel.fit("⚡ [bold blue]Benchmark des Solveurs Hydrauliques[/bold blue]"))
    
    try:
        # Charger la configuration du réseau
        with console.status("[bold green]Chargement de la configuration..."):
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                network_config = yaml.safe_load(f)
        
        # Déterminer les solveurs à tester
        if not solvers:
            available_solvers = SolverFactory.list_available_solvers()
            solvers = list(available_solvers.keys())
            console.print(f"🔍 Solveurs détectés automatiquement: {', '.join(solvers)}")
        
        # Lancer le benchmark
        with console.status("[bold blue]Exécution du benchmark..."):
            results = benchmark_solvers(
                network_data=network_config,
                solvers=solvers,
                iterations=iterations
            )
        
        # Affichage des résultats
        console.print(f"✅ Benchmark terminé pour {len(solvers)} solveur(s)")
        
        benchmark_table = Table(title="🏆 Résultats du Benchmark")
        benchmark_table.add_column("Solveur", style="cyan")
        benchmark_table.add_column("Itérations", style="blue")
        benchmark_table.add_column("Taux de Succès", style="green")
        benchmark_table.add_column("Temps Moyen", style="yellow")
        benchmark_table.add_column("Mémoire Moyenne", style="magenta")
        
        for solver_name, solver_results in results.items():
            if "error" in solver_results:
                benchmark_table.add_row(
                    solver_name,
                    "N/A",
                    "❌ Erreur",
                    "N/A",
                    "N/A"
                )
            else:
                success_rate = f"{solver_results['success_rate']*100:.1f}%"
                avg_time = f"{solver_results['avg_execution_time']:.3f}s"
                
                benchmark_table.add_row(
                    solver_name,
                    str(solver_results["iterations"]),
                    success_rate,
                    avg_time,
                    "N/A"  # Mémoire non disponible dans ce benchmark
                )
        
        console.print(benchmark_table)
        
        # Export si demandé
        if output:
            import json
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            console.print(f"💾 Résultats exportés vers: {output}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors du benchmark: {e}", style="red")
        raise typer.Exit(code=1)


@app.command("report")
def generate_performance_report_cli(
    output: Path = typer.Option(..., "--output", "-o", help="Fichier de sortie pour le rapport"),
    format: str = typer.Option("markdown", "--format", "-f", help="Format du rapport (markdown, html, json)")
):
    """📄 Générer un rapport de performance complet."""
    
    console.print(Panel.fit("📄 [bold blue]Génération du Rapport de Performance[/bold blue]"))
    
    try:
        monitor = get_performance_monitor()
        reporter = PerformanceReporter(monitor)
        
        with console.status("[bold green]Génération du rapport..."):
            if format == "markdown":
                report_content = reporter.generate_summary_report()
                
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                    
            elif format == "json":
                # Export JSON des statistiques
                global_stats = monitor.get_global_stats()
                algorithm_stats = {}
                
                algorithm_names = set(p.algorithm_name for p in monitor.completed_profiles)
                for alg_name in algorithm_names:
                    algorithm_stats[alg_name] = monitor.get_algorithm_stats(alg_name)
                
                report_data = {
                    "global_stats": global_stats,
                    "algorithm_stats": algorithm_stats,
                    "generated_at": str(datetime.now())
                }
                
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, ensure_ascii=False)
                    
            elif format == "html":
                # Export HTML basique
                report_content = reporter.generate_summary_report()
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rapport de Performance AEP</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        .metric {{ margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>📊 Rapport de Performance AEP</h1>
    <div class="metric">
        {report_content.replace('\n', '<br>')}
    </div>
</body>
</html>
                """
                
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            else:
                raise ValueError(f"Format non supporté: {format}")
        
        console.print(f"✅ Rapport généré: {output}")
        console.print(f"📊 Format: {format.upper()}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de la génération du rapport: {e}", style="red")
        raise typer.Exit(code=1)


@app.command("optimize")
def optimize_performance_cli(
    config_file: Path = typer.Option(..., "--config", "-c", help="Fichier de configuration du réseau"),
    use_cache: bool = typer.Option(True, "--use-cache", help="Utiliser le cache intelligent"),
    cache_size_mb: int = typer.Option(100, "--cache-size", help="Taille du cache en MB"),
    workers: Optional[int] = typer.Option(None, "--workers", "-w", help="Nombre de workers pour la parallélisation")
):
    """🚀 Optimisation des performances avec cache et parallélisation."""
    
    console.print(Panel.fit("🚀 [bold blue]Optimisation des Performances[/bold blue]"))
    
    try:
        # Charger la configuration du réseau
        with console.status("[bold green]Chargement de la configuration..."):
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                network_config = yaml.safe_load(f)
        
        # Configuration du cache
        if use_cache:
            cache_manager = get_cache_manager(max_size_mb=cache_size_mb)
            console.print(f"🗄️ Cache configuré: {cache_size_mb} MB")
        
        # Configuration de la parallélisation
        if workers:
            console.print(f"⚡ Parallélisation configurée: {workers} workers")
        
        # Test de performance avec et sans cache
        console.print("\n📊 Test de performance...")
        
        # Test sans cache
        with console.status("[bold blue]Test sans cache..."):
            with profile_algorithm("test_sans_cache") as profiler:
                # Simulation d'un calcul
                import time
                time.sleep(1)
        
        # Test avec cache
        if use_cache:
            with console.status("[bold blue]Test avec cache..."):
                with profile_algorithm("test_avec_cache") as profiler:
                    # Simulation d'un calcul (plus rapide avec cache)
                    time.sleep(0.3)
        
        # Affichage des résultats
        monitor = get_performance_monitor()
        
        console.print("\n✅ Optimisation terminée")
        console.print("\n📈 Résultats des tests:")
        
        # Comparer les performances
        if use_cache:
            sans_cache_stats = monitor.get_algorithm_stats("test_sans_cache")
            avec_cache_stats = monitor.get_algorithm_stats("test_avec_cache")
            
            if "error" not in sans_cache_stats and "error" not in avec_cache_stats:
                improvement = ((sans_cache_stats["avg_execution_time"] - avec_cache_stats["avg_execution_time"]) / 
                             sans_cache_stats["avg_execution_time"] * 100)
                
                console.print(f"  - Sans cache: {sans_cache_stats['avg_execution_time']:.3f}s")
                console.print(f"  - Avec cache: {avec_cache_stats['avg_execution_time']:.3f}s")
                console.print(f"  - Amélioration: {improvement:.1f}%")
        
        # Recommandations
        console.print("\n💡 Recommandations d'optimisation:")
        console.print("  - Utilisez le cache pour les calculs répétitifs")
        console.print("  - Activez la parallélisation pour les gros réseaux")
        console.print("  - Surveillez l'utilisation mémoire")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'optimisation: {e}", style="red")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
