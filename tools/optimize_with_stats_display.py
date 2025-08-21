#!/usr/bin/env python3
"""
Script pour lancer l'optimisation et afficher automatiquement les statistiques hydrauliques.
Usage: python tools/optimize_with_stats_display.py <fichier_inp> [options]
"""

import sys
import subprocess
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def run_optimization(input_file, output_file, **kwargs):
    """Lance l'optimisation avec les paramètres donnés."""
    
    # Construction de la commande
    cmd = [
        "python", "-m", "lcpi.aep.cli", "network-optimize-unified",
        str(input_file),
        "--output", str(output_file)
    ]
    
    # Ajout des paramètres optionnels
    if kwargs.get("method"):
        cmd.extend(["--method", kwargs["method"]])
    if kwargs.get("solver"):
        cmd.extend(["--solver", kwargs["solver"]])
    if kwargs.get("generations"):
        cmd.extend(["--generations", str(kwargs["generations"])])
    if kwargs.get("population"):
        cmd.extend(["--population", str(kwargs["population"])])
    if kwargs.get("pression_min") is not None:
        cmd.extend(["--pression-min", str(kwargs["pression_min"])])
    if kwargs.get("vitesse_max") is not None:
        cmd.extend(["--vitesse-max", str(kwargs["vitesse_max"])])
    if kwargs.get("verbose"):
        cmd.append("--verbose")
    if kwargs.get("no_cache"):
        cmd.append("--no-cache")
    if kwargs.get("no_surrogate"):
        cmd.append("--no-surrogate")
    
    console.print(f"[blue]🚀 Lancement de l'optimisation...[/blue]")
    console.print(f"[dim]Commande: {' '.join(cmd)}[/dim]")
    
    # Exécution de la commande
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        console.print("[green]✅ Optimisation terminée avec succès[/green]")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Erreur lors de l'optimisation:[/red] {e}")
        console.print(f"[red]Sortie d'erreur:[/red] {e.stderr}")
        return False, e.stderr

def display_hydraulic_statistics(stats_data):
    """Affiche les statistiques hydrauliques de manière structurée."""
    
    from rich.table import Table
    
    def format_value(value, unit=""):
        """Formate une valeur avec son unité."""
        if isinstance(value, (int, float)):
            if isinstance(value, int):
                return f"{value:,}{unit}"
            else:
                return f"{value:.3f}{unit}"
        return str(value)
    
    # Tableau des pressions
    pressure_table = Table(title="📊 Statistiques des Pressions", show_header=True, header_style="bold magenta")
    pressure_table.add_column("Métrique", style="cyan")
    pressure_table.add_column("Valeur", style="green")
    
    pressures = stats_data.get("pressures", {})
    if pressures:
        pressure_table.add_row("Nombre de nœuds", format_value(pressures.get("count", 0)))
        pressure_table.add_row("Pression minimale", format_value(pressures.get("min", 0), " m"))
        pressure_table.add_row("Pression maximale", format_value(pressures.get("max", 0), " m"))
        pressure_table.add_row("Pression moyenne", format_value(pressures.get("mean", 0), " m"))
        pressure_table.add_row("Pression médiane", format_value(pressures.get("median", 0), " m"))
        pressure_table.add_row("Écart-type", format_value(pressures.get("std", 0), " m"))
        pressure_table.add_row("Q25", format_value(pressures.get("q25", 0), " m"))
        pressure_table.add_row("Q75", format_value(pressures.get("q75", 0), " m"))
        pressure_table.add_row("% < 10m", format_value(pressures.get("percent_under_10m", 0), "%"))
        pressure_table.add_row("% < 15m", format_value(pressures.get("percent_under_15m", 0), "%"))
        pressure_table.add_row("% < 20m", format_value(pressures.get("percent_under_20m", 0), "%"))
    
    # Tableau des vitesses
    velocity_table = Table(title="⚡ Statistiques des Vitesses", show_header=True, header_style="bold blue")
    velocity_table.add_column("Métrique", style="cyan")
    velocity_table.add_column("Valeur", style="green")
    
    velocities = stats_data.get("velocities", {})
    if velocities:
        velocity_table.add_row("Nombre de conduites", format_value(velocities.get("count", 0)))
        velocity_table.add_row("Vitesse minimale", format_value(velocities.get("min", 0), " m/s"))
        velocity_table.add_row("Vitesse maximale", format_value(velocities.get("max", 0), " m/s"))
        velocity_table.add_row("Vitesse moyenne", format_value(velocities.get("mean", 0), " m/s"))
        velocity_table.add_row("Vitesse médiane", format_value(velocities.get("median", 0), " m/s"))
        velocity_table.add_row("Écart-type", format_value(velocities.get("std", 0), " m/s"))
        velocity_table.add_row("Q25", format_value(velocities.get("q25", 0), " m/s"))
        velocity_table.add_row("Q75", format_value(velocities.get("q75", 0), " m/s"))
        velocity_table.add_row("% > 1 m/s", format_value(velocities.get("percent_over_1ms", 0), "%"))
        velocity_table.add_row("% > 2 m/s", format_value(velocities.get("percent_over_2ms", 0), "%"))
        velocity_table.add_row("% > 3 m/s", format_value(velocities.get("percent_over_3ms", 0), "%"))
    
    # Tableau des diamètres
    diameter_table = Table(title="🔧 Statistiques des Diamètres", show_header=True, header_style="bold yellow")
    diameter_table.add_column("Métrique", style="cyan")
    diameter_table.add_column("Valeur", style="green")
    
    diameters = stats_data.get("diameters", {})
    if diameters:
        diameter_table.add_row("Nombre de conduites", format_value(diameters.get("count", 0)))
        diameter_table.add_row("Diamètre minimal", format_value(diameters.get("min", 0), " mm"))
        diameter_table.add_row("Diamètre maximal", format_value(diameters.get("max", 0), " mm"))
        diameter_table.add_row("Diamètre moyen", format_value(diameters.get("mean", 0), " mm"))
        diameter_table.add_row("Diamètre médian", format_value(diameters.get("median", 0), " mm"))
        diameter_table.add_row("Écart-type", format_value(diameters.get("std", 0), " mm"))
        
        # Distribution des diamètres
        distribution = diameters.get("distribution", {})
        if distribution:
            console.print("\n[bold]Distribution des diamètres:[/bold]")
            for range_name, count in distribution.items():
                if count > 0:
                    percentage = (count / diameters.get("count", 1)) * 100
                    console.print(f"  {range_name}: {count} conduites ({percentage:.1f}%)")
    
    # Tableau des pertes de charge
    headloss_table = Table(title="💧 Statistiques des Pertes de Charge", show_header=True, header_style="bold red")
    headloss_table.add_column("Métrique", style="cyan")
    headloss_table.add_column("Valeur", style="green")
    
    headlosses = stats_data.get("headlosses", {})
    if headlosses:
        headloss_table.add_row("Nombre de conduites", format_value(headlosses.get("count", 0)))
        headloss_table.add_row("Perte minimale", format_value(headlosses.get("min", 0), " m"))
        headloss_table.add_row("Perte maximale", format_value(headlosses.get("max", 0), " m"))
        headloss_table.add_row("Perte moyenne", format_value(headlosses.get("mean", 0), " m"))
        headloss_table.add_row("Perte médiane", format_value(headlosses.get("median", 0), " m"))
        headloss_table.add_row("Écart-type", format_value(headlosses.get("std", 0), " m"))
        headloss_table.add_row("Perte totale", format_value(headlosses.get("total", 0), " m"))
    
    # Tableau des débits
    flow_table = Table(title="🌊 Statistiques des Débits", show_header=True, header_style="bold green")
    flow_table.add_column("Métrique", style="cyan")
    flow_table.add_column("Valeur", style="green")
    
    # Explication du sens des débits
    console.print("\n[bold yellow]💡 Note sur les débits:[/bold yellow]")
    console.print("  • Débit positif = écoulement dans le sens défini dans le fichier INP/YML")
    console.print("  • Débit négatif = écoulement dans le sens inverse (ex: N21_N22 avec -0.23 m³/s = écoulement N22→N21)")
    console.print("  • Les valeurs absolues représentent la magnitude réelle de l'écoulement")
    
    flows = stats_data.get("flows", {})
    if flows:
        flow_table.add_row("Nombre de conduites", format_value(flows.get("count", 0)))
        flow_table.add_row("Débit minimal (absolu)", format_value(flows.get("min_abs", 0), " m³/s"))
        flow_table.add_row("Débit maximal (absolu)", format_value(flows.get("max_abs", 0), " m³/s"))
        flow_table.add_row("Débit moyen (absolu)", format_value(flows.get("mean_abs", 0), " m³/s"))
        flow_table.add_row("Débit médian (absolu)", format_value(flows.get("median_abs", 0), " m³/s"))
        flow_table.add_row("Écart-type", format_value(flows.get("std", 0), " m³/s"))
        
        # Statistiques sur le sens d'écoulement
        negative_flows = flows.get("negative_flows", 0)
        positive_flows = flows.get("positive_flows", 0)
        total_flows = flows.get("count", 0)
        
        if total_flows > 0:
            percent_negative = (negative_flows / total_flows) * 100
            percent_positive = (positive_flows / total_flows) * 100
            flow_table.add_row("Conduites sens normal", f"{positive_flows} ({percent_positive:.1f}%)")
            flow_table.add_row("Conduites sens inverse", f"{negative_flows} ({percent_negative:.1f}%)")
        
        # Débit total (conservation de masse)
        flow_table.add_row("Débit total (conservation)", format_value(flows.get("total", 0), " m³/s"))
    
    # Affichage des tableaux
    console.print(pressure_table)
    console.print("\n")
    console.print(velocity_table)
    console.print("\n")
    console.print(diameter_table)
    console.print("\n")
    console.print(headloss_table)
    console.print("\n")
    console.print(flow_table)
    
    # Indice de performance
    performance_index = stats_data.get("performance_index")
    if performance_index is not None:
        console.print(f"\n[bold]Indice de Performance Hydraulique:[/bold] {performance_index:.3f}")
    
    # Résumé
    summary = stats_data.get("summary", {})
    if summary:
        console.print("\n[bold]📋 Résumé Général:[/bold]")
        console.print(f"  • Nœuds: {summary.get('total_nodes', 0)}")
        console.print(f"  • Conduites: {summary.get('total_pipes', 0)}")
        console.print(f"  • Plage de pression: {summary.get('pressure_range', 'N/A')}")
        console.print(f"  • Plage de vitesse: {summary.get('velocity_range', 'N/A')}")
        console.print(f"  • Plage de diamètre: {summary.get('diameter_range', 'N/A')}")
        console.print(f"  • Perte de charge totale: {summary.get('total_headloss', 'N/A')}")
        console.print(f"  • Débit total: {summary.get('total_flow', 'N/A')}")

def main():
    if len(sys.argv) < 2:
        console.print("[red]Usage: python tools/optimize_with_stats_display.py <fichier_inp> [options][/red]")
        console.print("\n[bold]Options disponibles:[/bold]")
        console.print("  --method <method>        Méthode d'optimisation (genetic, nested, etc.)")
        console.print("  --solver <solver>        Solveur (epanet, lcpi, etc.)")
        console.print("  --generations <n>        Nombre de générations")
        console.print("  --population <n>         Taille de la population")
        console.print("  --pression-min <m>       Pression minimale (m)")
        console.print("  --vitesse-max <m/s>      Vitesse maximale (m/s)")
        console.print("  --output <file>          Fichier de sortie")
        console.print("  --verbose                Mode verbeux")
        console.print("  --no-cache               Désactiver le cache")
        console.print("  --no-surrogate           Désactiver le surrogate")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    if not input_file.exists():
        console.print(f"[red]Fichier introuvable: {input_file}[/red]")
        sys.exit(1)
    
    # Parsing des arguments
    args = sys.argv[2:]
    kwargs = {}
    output_file = Path("results/optimization_result.json")
    
    i = 0
    while i < len(args):
        if args[i] == "--method" and i + 1 < len(args):
            kwargs["method"] = args[i + 1]
            i += 2
        elif args[i] == "--solver" and i + 1 < len(args):
            kwargs["solver"] = args[i + 1]
            i += 2
        elif args[i] == "--generations" and i + 1 < len(args):
            kwargs["generations"] = int(args[i + 1])
            i += 2
        elif args[i] == "--population" and i + 1 < len(args):
            kwargs["population"] = int(args[i + 1])
            i += 2
        elif args[i] == "--pression-min" and i + 1 < len(args):
            kwargs["pression_min"] = float(args[i + 1])
            i += 2
        elif args[i] == "--vitesse-max" and i + 1 < len(args):
            kwargs["vitesse_max"] = float(args[i + 1])
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_file = Path(args[i + 1])
            i += 2
        elif args[i] == "--verbose":
            kwargs["verbose"] = True
            i += 1
        elif args[i] == "--no-cache":
            kwargs["no_cache"] = True
            i += 1
        elif args[i] == "--no-surrogate":
            kwargs["no_surrogate"] = True
            i += 1
        else:
            i += 1
    
    # Créer le dossier de sortie si nécessaire
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Lancement de l'optimisation
    success, output = run_optimization(input_file, output_file, **kwargs)
    
    if not success:
        console.print("[red]❌ L'optimisation a échoué[/red]")
        sys.exit(1)
    
    # Affichage des statistiques hydrauliques
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Chercher les statistiques hydrauliques
        stats = None
        
        # Chercher dans la section hydraulics
        if "hydraulics" in data:
            hydraulics = data["hydraulics"]
            if "statistics" in hydraulics:
                stats = hydraulics["statistics"]
        
        # Si pas trouvé, chercher dans les propositions
        if not stats:
            proposals = data.get("proposals", [])
            for proposal in proposals:
                if "statistics" in proposal:
                    stats = proposal["statistics"]
                    break
        
        # Si pas trouvé, chercher à la racine
        if not stats and "statistics" in data:
            stats = data["statistics"]
        
        if stats:
            console.print("\n" + "="*80)
            console.print(f"[bold green]📊 Statistiques Hydrauliques - {output_file.name}[/bold green]")
            console.print("="*80)
            display_hydraulic_statistics(stats)
        else:
            console.print("[yellow]⚠️ Aucune statistique hydraulique trouvée dans les résultats[/yellow]")
        
        # Affichage du résumé de l'optimisation
        meta = data.get("meta", {})
        best = data.get("proposals", [{}])[0] if data.get("proposals") else {}
        
        console.print("\n" + "="*80)
        console.print("[bold green]🎯 Résumé de l'Optimisation[/bold green]")
        console.print("="*80)
        console.print(f"  • Méthode: {meta.get('method', 'N/A')}")
        console.print(f"  • Solveur: {meta.get('solver', 'N/A')}")
        console.print(f"  • Coût optimal: {best.get('CAPEX', 'N/A')} FCFA")
        console.print(f"  • Contraintes respectées: {best.get('constraints_ok', 'N/A')}")
        console.print(f"  • Durée totale: {meta.get('duration_seconds', 'N/A')} secondes")
        console.print(f"  • Appels simulateur: {meta.get('solver_calls', 'N/A')}")
        
    except Exception as e:
        console.print(f"[red]❌ Erreur lors de la lecture des résultats: {e}[/red]")

if __name__ == "__main__":
    main()