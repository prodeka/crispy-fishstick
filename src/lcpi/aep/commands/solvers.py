"""
Commandes CLI pour la gestion des solveurs hydrauliques.
"""

import typer
import time
import shutil
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..core.solvers import SolverFactory
from ..core.validators import validate_network_config

app = typer.Typer(help="Gestion des solveurs hydrauliques")
console = Console()


def _try_import_wntr() -> bool:
    try:
        import wntr  # type: ignore
        return True
    except Exception:
        return False


def _install_wntr_offline() -> bool:
    """Tente d'installer wntr depuis des wheels locaux pour faciliter la distribution offline.

    Cherche dans `vendor/packages/` puis `offline_packages/` et utilise pip en mode no-index.
    """
    import subprocess, sys
    candidate_dirs = [
        Path(__file__).resolve().parents[3] / "vendor" / "packages",
        Path(__file__).resolve().parents[3] / "offline_packages",
    ]
    for wheel_dir in candidate_dirs:
        if wheel_dir.exists():
            try:
                console.print(f"📦 Tentative d'installation offline de wntr depuis: {wheel_dir}")
                subprocess.check_call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "--no-index",
                        "--find-links",
                        str(wheel_dir),
                        "wntr",
                    ],
                )
                return _try_import_wntr()
            except Exception as e:
                console.print(f"⚠️  Offline install échouée depuis {wheel_dir}: {e}")
                continue
    return False

@app.command("list")
def list_solvers(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Affichage détaillé")
):
    """Lister tous les solveurs hydrauliques disponibles."""
    
    console.print(Panel.fit("🔧 [bold blue]Solveurs Hydrauliques Disponibles[/bold blue]"))
    
    try:
        factory = SolverFactory()
        available_solvers = factory.get_available_solvers()
        
        if not available_solvers:
            console.print("❌ Aucun solveur disponible", style="red")
            return
        
        # Tableau des solveurs
        table = Table(title="Solveurs Disponibles")
        table.add_column("Nom", style="cyan", no_wrap=True)
        table.add_column("Version", style="green")
        table.add_column("Description", style="white")
        table.add_column("Statut", style="bold")
        
        for solver_name in available_solvers:
            try:
                solver = factory.get_solver(solver_name)
                info = solver.get_solver_info()
                
                # Vérifier si le solveur fonctionne
                status = "✅ Disponible" if solver.is_available() else "❌ Indisponible"
                status_style = "green" if solver.is_available() else "red"
                
                table.add_row(
                    solver_name.upper(),
                    info.get("version", "N/A"),
                    info.get("description", "Aucune description"),
                    f"[{status_style}]{status}[/{status_style}]"
                )
                
                if verbose:
                    console.print(f"\n[bold]{solver_name.upper()}[/bold]")
                    console.print(f"  Version: {info.get('version', 'N/A')}")
                    console.print(f"  Description: {info.get('description', 'Aucune description')}")
                    console.print(f"  Statut: {status}")
                    
            except Exception as e:
                table.add_row(
                    solver_name.upper(),
                    "N/A",
                    f"Erreur: {str(e)}",
                    "❌ Erreur"
                )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ Erreur lors de la récupération des solveurs: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("test")
def test_solver(
    solver: str = typer.Argument(..., help="Nom du solveur à tester"),
    config: Path = typer.Option(..., "--config", "-c", help="Fichier de configuration du réseau"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour les résultats")
):
    """Tester un solveur hydraulique spécifique."""
    
    console.print(Panel.fit(f"🧪 [bold blue]Test du Solveur: {solver.upper()}[/bold blue]"))
    
    try:
        # 1. Validation de la configuration
        with console.status("[bold green]Validation de la configuration..."):
            network_config = validate_network_config(config)
        
        # 2. Récupération du solveur
        with console.status("[bold blue]Récupération du solveur..."):
            factory = SolverFactory()
            solver_instance = factory.get_solver(solver)
        
        # 3. Test du solveur
        with console.status("[bold yellow]Exécution du test..."):
            results = solver_instance.run_simulation(network_config)
        
        # 4. Affichage des résultats
        console.print(f"\n✅ [bold green]Test réussi pour {solver.upper()}[/bold green]")
        
        # Résumé des résultats
        summary_table = Table(title="Résumé du Test")
        summary_table.add_column("Métrique", style="cyan")
        summary_table.add_column("Valeur", style="white")
        
        summary_table.add_row("Statut", results.get("status", "N/A"))
        summary_table.add_row("Solveur", results.get("solver", "N/A"))
        summary_table.add_row("Nœuds traités", str(len(results.get("pressures", {}))))
        summary_table.add_row("Conduites traitées", str(len(results.get("flows", {}))))
        
        console.print(summary_table)
        
        # 5. Sauvegarde des résultats si demandé
        if output:
            import json
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            console.print(f"\n💾 Résultats sauvegardés dans: {output}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors du test du solveur {solver}: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("compare")
def compare_solvers(
    config: Path = typer.Option(..., "--config", "-c", help="Fichier de configuration du réseau"),
    solvers: List[str] = typer.Option(..., "--solvers", "-s", help="Liste des solveurs à comparer (séparés par des virgules)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour la comparaison")
):
    """Comparer les performances de plusieurs solveurs."""
    
    console.print(Panel.fit("⚖️ [bold blue]Comparaison des Solveurs[/bold blue]"))
    
    try:
        # 1. Validation de la configuration
        with console.status("[bold green]Validation de la configuration..."):
            network_config = validate_network_config(config)
        
        # 2. Récupération des solveurs
        factory = SolverFactory()
        solver_instances = {}
        
        for solver_name in solvers:
            try:
                solver_instances[solver_name] = factory.get_solver(solver_name)
            except Exception as e:
                console.print(f"⚠️  Impossible de récupérer le solveur {solver_name}: {e}", style="yellow")
        
        if not solver_instances:
            console.print("❌ Aucun solveur valide à comparer", style="red")
            return
        
        # 3. Exécution des tests
        results = {}
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            for solver_name, solver_instance in solver_instances.items():
                task = progress.add_task(f"Test de {solver_name}...", total=None)
                
                try:
                    start_time = time.time()
                    solver_results = solver_instance.run_simulation(network_config)
                    execution_time = time.time() - start_time
                    
                    results[solver_name] = {
                        **solver_results,
                        "execution_time": execution_time
                    }
                    
                    progress.update(task, description=f"✅ {solver_name} terminé")
                    
                except Exception as e:
                    results[solver_name] = {
                        "status": "error",
                        "error": str(e),
                        "execution_time": 0
                    }
                    progress.update(task, description=f"❌ {solver_name} échoué")
        
        # 4. Affichage de la comparaison
        comparison_table = Table(title="Comparaison des Solveurs")
        comparison_table.add_column("Métrique", style="cyan")
        for solver_name in solver_instances.keys():
            comparison_table.add_column(solver_name.upper(), style="white")
        
        # Statut
        status_row = ["Statut"]
        for solver_name in solver_instances.keys():
            status = results[solver_name].get("status", "N/A")
            status_emoji = "✅" if status == "success" else "❌"
            status_row.append(f"{status_emoji} {status}")
        comparison_table.add_row(*status_row)
        
        # Temps d'exécution
        time_row = ["Temps (s)"]
        for solver_name in solver_instances.keys():
            time_val = results[solver_name].get("execution_time", 0)
            time_row.append(f"{time_val:.3f}")
        comparison_table.add_row(*time_row)
        
        # Nœuds traités
        nodes_row = ["Nœuds traités"]
        for solver_name in solver_instances.keys():
            nodes_count = len(results[solver_name].get("pressures", {}))
            nodes_row.append(str(nodes_count))
        comparison_table.add_row(*nodes_row)
        
        console.print(comparison_table)
        
        # 5. Sauvegarde des résultats si demandé
        if output:
            import json
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            console.print(f"\n💾 Comparaison sauvegardée dans: {output}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de la comparaison: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("status")
def solver_status():
    """Vérifier le statut de tous les solveurs."""
    
    console.print(Panel.fit("📊 [bold blue]Statut des Solveurs[/bold blue]"))
    
    try:
        factory = SolverFactory()
        available_solvers = factory.get_available_solvers()
        
        if not available_solvers:
            console.print("❌ Aucun solveur disponible", style="red")
            return
        
        # Vérification du statut de chaque solveur
        status_table = Table(title="Statut des Solveurs")
        status_table.add_column("Solveur", style="cyan")
        status_table.add_column("Disponibilité", style="bold")
        status_table.add_column("Version", style="green")
        status_table.add_column("Détails", style="white")
        
        for solver_name in available_solvers:
            try:
                solver = factory.get_solver(solver_name)
                info = solver.get_solver_info()
                
                if solver.is_available():
                    availability = "✅ Disponible"
                    details = "Prêt à l'utilisation"
                else:
                    availability = "❌ Indisponible"
                    details = solver.get_unavailable_reason() or "Raison inconnue"
                
                status_table.add_row(
                    solver_name.upper(),
                    availability,
                    info.get("version", "N/A"),
                    details
                )
                
            except Exception as e:
                status_table.add_row(
                    solver_name.upper(),
                    "❌ Erreur",
                    "N/A",
                    f"Erreur: {str(e)}"
                )
        
        console.print(status_table)
        
    except Exception as e:
        console.print(f"❌ Erreur lors de la vérification du statut: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("install")
def install_solver(
    solver: str = typer.Argument(..., help="Nom du solveur à installer/configurer")
):
    """Installer ou configurer un solveur spécifique."""
    
    console.print(Panel.fit(f"🔧 [bold blue]Installation/Configuration: {solver.upper()}[/bold blue]"))
    
    try:
        factory = SolverFactory()
        
        if solver == "epanet":
            console.print("📋 Configuration d'EPANET...")
            
            # Vérifier si EPANET est disponible
            try:
                import epanet_python
                console.print("✅ EPANET Python est déjà installé")
            except ImportError:
                console.print("⚠️  EPANET Python n'est pas installé")
                console.print("📥 Installation recommandée: pip install epanet-python")
            
            # Installer wntr via pip si manquant
            if _try_import_wntr():
                console.print("✅ wntr est déjà installé")
            else:
                # Offline first
                if _install_wntr_offline():
                    console.print("✅ wntr installé (offline)")
                else:
                    console.print("⚠️  wntr introuvable offline — tentative d'installation via pip (online)")
                    try:
                        import subprocess, sys
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "wntr"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        console.print("✅ wntr installé (pip)")
                    except Exception as e:
                        console.print(f"❌ Échec installation wntr: {e}")

            # Vérifier si le binaire EPANET est disponible
            epanet_binary = shutil.which("epanet")
            if epanet_binary:
                console.print(f"✅ Binaire EPANET trouvé: {epanet_binary}")
            else:
                console.print("⚠️  Binaire EPANET non trouvé")
                console.print("📥 Téléchargement: https://www.epa.gov/water-research/epanet")
                
        elif solver == "lcpi":
            console.print("✅ LCPI est toujours disponible (solveur interne)")
            
        else:
            console.print(f"⚠️  Installation automatique non supportée pour {solver}")
            console.print("📖 Consultez la documentation du solveur pour l'installation")
        
        # Test du solveur après installation
        console.print(f"\n🧪 Test du solveur {solver}...")
        try:
            solver_instance = factory.get_solver(solver)
            if solver_instance.is_available():
                console.print(f"✅ {solver.upper()} est maintenant disponible et fonctionnel")
            else:
                console.print(f"❌ {solver.upper()} n'est toujours pas disponible")
        except Exception as e:
            console.print(f"❌ Erreur lors du test de {solver}: {e}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'installation: {e}", style="red")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
