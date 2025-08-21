#!/usr/bin/env python3
"""
Script pour afficher les statistiques hydrauliques d'un fichier de résultats d'optimisation.
Usage: python tools/show_hydraulic_stats.py <fichier_resultats.json>
"""

import json
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

def format_value(value, unit=""):
    """Formate une valeur avec son unité."""
    if isinstance(value, (int, float)):
        if isinstance(value, int):
            return f"{value:,}{unit}"
        else:
            return f"{value:.3f}{unit}"
    return str(value)

def display_hydraulic_statistics(stats_data):
    """Affiche les statistiques hydrauliques de manière structurée."""
    
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
    if len(sys.argv) != 2:
        console.print("[red]Usage: python tools/show_hydraulic_stats.py <fichier_resultats.json>[/red]")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        console.print(f"[red]Fichier non trouvé: {file_path}[/red]")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
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
        
        if not stats:
            console.print("[yellow]Aucune statistique hydraulique trouvée dans le fichier.[/yellow]")
            console.print("Vérifiez que le fichier contient des résultats d'optimisation avec des statistiques hydrauliques.")
            sys.exit(1)
        
        console.print(f"[bold green]📊 Statistiques Hydrauliques - {file_path.name}[/bold green]")
        console.print("=" * 60)
        
        display_hydraulic_statistics(stats)
        
    except json.JSONDecodeError as e:
        console.print(f"[red]Erreur de lecture JSON: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Erreur inattendue: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
