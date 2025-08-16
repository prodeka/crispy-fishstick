"""
Commande principale CLI pour LCPI-AEP.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Import des commandes
from . import network_optimize

# Import conditionnel des nouvelles commandes
try:
    from . import solvers
    from . import data_management
    from . import project_management
    SOLVERS_AVAILABLE = True
    DATA_MANAGEMENT_AVAILABLE = True
    PROJECT_MANAGEMENT_AVAILABLE = True
except ImportError:
    SOLVERS_AVAILABLE = False
    DATA_MANAGEMENT_AVAILABLE = False
    PROJECT_MANAGEMENT_AVAILABLE = False

app = typer.Typer(
    name="lcpi",
    help="LCPI-AEP: Outils d'analyse et d'optimisation des réseaux d'eau potable",
    add_completion=False
)

console = Console()

@app.callback()
def main():
    """LCPI-AEP - Outils d'analyse et d'optimisation des réseaux d'eau potable"""
    pass

# Ajout des commandes existantes
app.add_typer(network_optimize.app, name="network", help="Commandes d'analyse et d'optimisation de réseaux")

# Ajout des nouvelles commandes si disponibles
if SOLVERS_AVAILABLE:
    app.add_typer(solvers.app, name="solveurs", help="Gestion des solveurs hydrauliques")

if DATA_MANAGEMENT_AVAILABLE:
    app.add_typer(data_management.app, name="data", help="Gestion des données (import/export/validation)")

if PROJECT_MANAGEMENT_AVAILABLE:
    app.add_typer(project_management.app, name="project", help="Gestion des projets AEP")

@app.command("version")
def show_version():
    """Afficher la version de LCPI-AEP."""
    console.print(Panel.fit("📊 [bold blue]LCPI-AEP - Version[/bold blue]"))
    
    version_table = Table(title="Informations de Version")
    version_table.add_column("Composant", style="cyan")
    version_table.add_column("Version", style="white")
    version_table.add_column("Statut", style="bold")
    
    version_table.add_row("LCPI-AEP Core", "1.5.0", "✅ Disponible")
    version_table.add_row("Module Optimisation", "1.0.0", "✅ Disponible")
    version_table.add_row("Module Sensibilité", "1.0.0", "✅ Disponible")
    version_table.add_row("Module Comparaison", "1.0.0", "✅ Disponible")
    
    if SOLVERS_AVAILABLE:
        version_table.add_row("Gestion Solveurs", "1.0.0", "✅ Disponible")
    else:
        version_table.add_row("Gestion Solveurs", "N/A", "❌ Indisponible")
    
    if DATA_MANAGEMENT_AVAILABLE:
        version_table.add_row("Gestion Données", "1.0.0", "✅ Disponible")
    else:
        version_table.add_row("Gestion Données", "N/A", "❌ Indisponible")
    
    if PROJECT_MANAGEMENT_AVAILABLE:
        version_table.add_row("Gestion Projets", "1.0.0", "✅ Disponible")
    else:
        version_table.add_row("Gestion Projets", "N/A", "❌ Indisponible")
    
    console.print(version_table)

@app.command("status")
def show_status():
    """Afficher le statut de tous les modules LCPI-AEP."""
    console.print(Panel.fit("📊 [bold blue]Statut des Modules LCPI-AEP[/bold blue]"))
    
    status_table = Table(title="Statut des Modules")
    status_table.add_column("Module", style="cyan")
    status_table.add_column("Statut", style="bold")
    status_table.add_column("Version", style="white")
    status_table.add_column("Description", style="white")
    
    # Modules de base
    status_table.add_row(
        "LCPI-AEP Core",
        "✅ Actif",
        "1.5.0",
        "Fonctionnalités de base et calculs hydrauliques"
    )
    
    status_table.add_row(
        "Optimisation",
        "✅ Actif",
        "1.0.0",
        "Algorithme génétique et gestion des contraintes"
    )
    
    status_table.add_row(
        "Sensibilité",
        "✅ Actif",
        "1.0.0",
        "Analyse Monte Carlo et indices de Sobol"
    )
    
    status_table.add_row(
        "Comparaison",
        "✅ Actif",
        "1.0.0",
        "Métriques et visualisation des variantes"
    )
    
    # Nouvelles commandes
    if SOLVERS_AVAILABLE:
        status_table.add_row(
            "Gestion Solveurs",
            "✅ Actif",
            "1.0.0",
            "Gestion des solveurs hydrauliques (LCPI, EPANET)"
        )
    else:
        status_table.add_row(
            "Gestion Solveurs",
            "❌ Inactif",
            "N/A",
            "Module non disponible"
        )
    
    if DATA_MANAGEMENT_AVAILABLE:
        status_table.add_row(
            "Gestion Données",
            "✅ Actif",
            "1.0.0",
            "Import/export, validation et recalcul automatique"
        )
    else:
        status_table.add_row(
            "Gestion Données",
            "❌ Inactif",
            "N/A",
            "Module non disponible"
        )
    
    if PROJECT_MANAGEMENT_AVAILABLE:
        status_table.add_row(
            "Gestion Projets",
            "✅ Actif",
            "1.0.0",
            "Gestion des projets, base de données et constantes"
        )
    else:
        status_table.add_row(
            "Gestion Projets",
            "❌ Inactif",
            "N/A",
            "Module non disponible"
        )
    
    console.print(status_table)

@app.command("help")
def show_help():
    """Afficher l'aide complète de LCPI-AEP."""
    console.print(Panel.fit("📚 [bold blue]Aide LCPI-AEP[/bold blue]"))
    
    help_text = """
[bold]LCPI-AEP[/bold] est un outil complet d'analyse et d'optimisation des réseaux d'eau potable.

[bold cyan]Commandes Principales:[/bold cyan]

[bold]lcpi network[/bold] - Analyse et optimisation de réseaux
  • optimize    - Optimiser un réseau avec algorithme génétique
  • sensitivity - Analyser la sensibilité avec Monte Carlo
  • compare    - Comparer différentes variantes de réseaux

[bold]lcpi solveurs[/bold] - Gestion des solveurs hydrauliques
  • list       - Lister les solveurs disponibles
  • test       - Tester un solveur spécifique
  • compare    - Comparer les performances des solveurs
  • status     - Vérifier le statut des solveurs
  • install    - Installer/configurer un solveur

[bold]lcpi data[/bold] - Gestion des données
  • import     - Importer des données depuis différents formats
  • export     - Exporter des données vers différents formats
  • validate   - Valider des données selon des règles
  • convert    - Convertir entre formats
  • recalculate - Recalculer automatiquement les données
  • batch      - Traiter un lot de fichiers

[bold]lcpi project[/bold] - Gestion des projets
  • init       - Initialiser un nouveau projet
  • validate   - Valider un projet complet
  • info       - Afficher les informations d'un projet
  • query      - Exécuter des requêtes SQL
  • constants  - Gérer les constantes dynamiques

[bold]lcpi version[/bold] - Afficher la version
[bold]lcpi status[/bold] - Afficher le statut des modules
[bold]lcpi help[/bold] - Afficher cette aide

[bold]Exemples d'utilisation:[/bold]

# Optimiser un réseau
lcpi network optimize --config config.yml --output results.json

# Analyser la sensibilité
lcpi network sensitivity --config config.yml --simulations 1000

# Lister les solveurs disponibles
lcpi solveurs list

# Initialiser un nouveau projet
lcpi project init "MonProjet" --dir ./mon_projet

# Valider un projet
lcpi project validate ./mon_projet

# Importer des données
lcpi data import source.yml --format yaml --validate

[bold]Pour plus d'aide sur une commande spécifique:[/bold]
lcpi [commande] --help
"""
    
    console.print(help_text)

if __name__ == "__main__":
    app()
