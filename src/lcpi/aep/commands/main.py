"""
Commandes CLI principales pour le module AEP.

Ce module regroupe toutes les commandes disponibles pour :
- Calculs hydrauliques
- Gestion des données et projets
- Optimisation et analyse
- Performance et cache (Phase 4)
"""

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel

# Import des commandes existantes
from .solvers import app as solvers_app
from .data_management import app as data_app
from .project_management import app as project_app
from .network_optimize import app as network_optimize_app
from .tank_optimization import app as tank_optimization_app

# Import des nouvelles commandes de la Phase 4
from .performance import app as performance_app
from .sensitivity import app as sensitivity_app

app = typer.Typer(help="🌊 Commandes AEP (Adduction Eau Potable)")
console = Console()

# Ajout des sous-commandes existantes
app.add_typer(solvers_app, name="solveurs", help="🔧 Gestion des solveurs hydrauliques")
app.add_typer(data_app, name="data", help="📊 Gestion des données (import/export/validation)")
app.add_typer(project_app, name="project", help="📁 Gestion des projets AEP")
app.add_typer(network_optimize_app, name="network", help="🌐 Optimisation des réseaux")
app.add_typer(tank_optimization_app, name="tank", help="🏗️ Optimisation des réservoirs surélevés")

# Ajout des nouvelles commandes de la Phase 4
app.add_typer(performance_app, name="performance", help="🚀 Gestion des performances et du cache")
app.add_typer(sensitivity_app, name="sensitivity", help="📊 Analyse de sensibilité parallélisée")


@app.command("version")
def show_version():
    """📋 Affiche la version du module AEP."""
    console.print(Panel.fit("🌊 [bold blue]Module AEP - Version 2.1.0[/bold blue]"))
    console.print("📅 Phase 4 : Améliorations de Performance et Parallélisation")
    console.print("🔧 Cache intelligent, Monte Carlo parallélisé, monitoring des performances")


@app.command("status")
def show_status():
    """📊 Affiche le statut des modules AEP."""
    console.print(Panel.fit("📊 [bold blue]Statut des Modules AEP[/bold blue]"))
    
    # Statut des modules principaux
    status_table = [
        ("🌊 Commandes principales", "✅ Actif"),
        ("🔧 Solveurs hydrauliques", "✅ Actif"),
        ("📊 Gestion des données", "✅ Actif"),
        ("📁 Gestion des projets", "✅ Actif"),
        ("🌐 Optimisation des réseaux", "✅ Actif"),
        ("🚀 Performance et cache", "✅ Actif (Phase 4)"),
        ("📊 Analyse de sensibilité", "✅ Actif (Phase 4)")
    ]
    
    for module, status in status_table:
        console.print(f"  {module}: {status}")


@app.command("help")
def show_help():
    """❓ Affiche l'aide complète des commandes AEP."""
    console.print(Panel.fit("❓ [bold blue]Aide des Commandes AEP[/bold blue]"))
    
    console.print("\n🌊 **Commandes Principales:**")
    console.print("  lcpi aep version          - Affiche la version")
    console.print("  lcpi aep status           - Statut des modules")
    console.print("  lcpi aep help             - Cette aide")
    
    console.print("\n🔧 **Solveurs Hydrauliques:**")
    console.print("  lcpi aep solveurs list    - Liste des solveurs disponibles")
    console.print("  lcpi aep solveurs test    - Test d'un solveur")
    console.print("  lcpi aep solveurs compare - Comparaison des solveurs")
    
    console.print("\n📊 **Gestion des Données:**")
    console.print("  lcpi aep data import      - Import de données")
    console.print("  lcpi aep data export      - Export de données")
    console.print("  lcpi aep data validate    - Validation de données")
    console.print("  lcpi aep data convert     - Conversion de formats")
    
    console.print("\n📁 **Gestion des Projets:**")
    console.print("  lcpi aep project init     - Initialiser un projet")
    console.print("  lcpi aep project validate - Valider un projet")
    console.print("  lcpi aep project info     - Informations du projet")
    
    console.print("\n🌐 **Optimisation des Réseaux:**")
    console.print("  lcpi aep network optimize - Optimisation de réseau")
    console.print("  lcpi aep network compare  - Comparaison de variantes")
    
    console.print("\n🚀 **Performance et Cache (Phase 4):**")
    console.print("  lcpi aep performance profile    - Profiler un algorithme")
    console.print("  lcpi aep performance monitor    - Monitoring des performances")
    console.print("  lcpi aep performance cache      - Gestion du cache")
    console.print("  lcpi aep performance benchmark  - Benchmark des solveurs")
    console.print("  lcpi aep performance report     - Rapport de performance")
    console.print("  lcpi aep performance optimize   - Optimisation des performances")
    
    console.print("\n📊 **Analyse de Sensibilité (Phase 4):**")
    console.print("  lcpi aep sensitivity parallel      - Monte Carlo parallélisé")
    console.print("  lcpi aep sensitivity distributions - Configuration des distributions")
    console.print("  lcpi aep sensitivity validate      - Validation des distributions")
    
    console.print("\n💡 **Exemples d'utilisation:**")
    console.print("  # Profiler un algorithme Hardy-Cross")
    console.print("  lcpi aep performance profile hardy_cross --config network.yml --iterations 5")
    console.print("")
    console.print("  # Analyse Monte Carlo parallélisée")
    console.print("  lcpi aep sensitivity parallel network.yml --workers 8 --simulations 5000")
    console.print("")
    console.print("  # Benchmark des solveurs")
    console.print("  lcpi aep performance benchmark --config network.yml --iterations 10")
    console.print("")
    console.print("  # Monitoring en temps réel")
    console.print("  lcpi aep performance monitor --watch")


@app.command("demo")
def run_demo():
    """🎮 Démonstration des fonctionnalités AEP."""
    console.print(Panel.fit("🎮 [bold blue]Démonstration des Fonctionnalités AEP[/bold blue]"))
    
    console.print("🚀 **Phase 4 - Améliorations de Performance:**")
    console.print("  ✅ Cache intelligent avec persistance")
    console.print("  ✅ Parallélisation Monte Carlo")
    console.print("  ✅ Monitoring des performances en temps réel")
    console.print("  ✅ Profiling des algorithmes")
    console.print("  ✅ Benchmark des solveurs")
    
    console.print("\n📊 **Fonctionnalités Disponibles:**")
    console.print("  🌊 Calculs hydrauliques (Hardy-Cross, EPANET)")
    console.print("  🔧 Solveurs multiples avec Strategy Pattern")
    console.print("  📊 Gestion des données et projets")
    console.print("  🌐 Optimisation des réseaux")
    console.print("  🚀 Performance et cache intelligent")
    console.print("  📊 Analyse de sensibilité parallélisée")
    
    console.print("\n💡 **Pour commencer:**")
    console.print("  lcpi aep help              - Aide complète")
    console.print("  lcpi aep performance cache - Gestion du cache")
    console.print("  lcpi aep sensitivity distributions - Configuration des distributions")


if __name__ == "__main__":
    app()
