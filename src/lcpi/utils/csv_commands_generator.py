"""
Générateur de commandes CSV pour tous les modules LCPI-CLI
"""

import typer
from typing import Dict, List, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .csv_handler import CSVHandler

console = Console()

# Définition des commandes par module
MODULE_COMMANDS = {
    'cm': ['check-poteau', 'check-deversement', 'check-tendu', 'check-compose', 'check-fleche', 'check-assemblage-boulon', 'check-assemblage-soude', 'optimize-section'],
    'bois': ['check-poteau', 'check-deversement', 'check-cisaillement', 'check-compression-perp', 'check-compose', 'check-fleche', 'check-assemblage-pointe', 'check-assemblage-embrevement', 'check'],
    'beton': ['calc-poteau', 'calc-radier'],
    'hydrodrain': ['ouvrage-canal', 'reservoir-equilibrage', 'collector-dimensionner-troncons', 'plomberie-dimensionner']
}

def create_csv_app_for_module(module_name: str) -> typer.Typer:
    """Crée l'app Typer avec les commandes CSV pour un module."""
    app = typer.Typer(name="csv", help=f"Commandes CSV pour {module_name}")
    
    @app.command()
    def template_csv(
        command: str = typer.Argument(..., help="Commande pour laquelle générer le template"),
        output: str = typer.Option(None, help="Fichier de sortie (optionnel)")
    ):
        """Génère un template CSV pour une commande spécifique."""
        try:
            handler = CSVHandler()
            template = handler.get_csv_template(module_name, command)
            
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(template)
                console.print(f"[green]✓[/green] Template sauvegardé: {output}")
            else:
                console.print(Panel(template, title=f"Template CSV pour {module_name} {command}", border_style="cyan"))
                
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
    
    @app.command()
    def validate_csv(
        csv_file: str = typer.Argument(..., help="Fichier CSV à valider")
    ):
        """Valide un fichier CSV pour le module."""
        try:
            handler = CSVHandler()
            validation = handler.validate_csv(csv_file, module_name)
            
            if validation['valid']:
                console.print(f"[green]✓[/green] Fichier CSV valide ({validation['row_count']} lignes)")
            else:
                console.print(f"[red]✗[/red] Fichier CSV invalide")
                
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
    
    @app.command()
    def convert_yaml_to_csv(
        yaml_file: str = typer.Argument(..., help="Fichier YAML d'entrée"),
        csv_file: str = typer.Argument(..., help="Fichier CSV de sortie")
    ):
        """Convertit un fichier YAML en CSV."""
        try:
            handler = CSVHandler()
            success = handler.yaml_to_csv(yaml_file, csv_file, module_name)
            
            if success:
                console.print(f"[green]✓[/green] Conversion YAML → CSV réussie")
            else:
                console.print(f"[red]✗[/red] Échec de la conversion")
                
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
    
    @app.command()
    def convert_csv_to_yaml(
        csv_file: str = typer.Argument(..., help="Fichier CSV d'entrée"),
        yaml_file: str = typer.Argument(..., help="Fichier YAML de sortie")
    ):
        """Convertit un fichier CSV en YAML."""
        try:
            handler = CSVHandler()
            success = handler.csv_to_yaml(csv_file, yaml_file, module_name)
            
            if success:
                console.print(f"[green]✓[/green] Conversion CSV → YAML réussie")
            else:
                console.print(f"[red]✗[/red] Échec de la conversion")
                
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
    
    @app.command()
    def batch_process(
        csv_file: str = typer.Argument(..., help="Fichier CSV d'entrée"),
        command: str = typer.Argument(..., help="Commande à exécuter"),
        output: str = typer.Option("results.csv", help="Fichier de sortie")
    ):
        """Traite un fichier CSV en lot."""
        try:
            handler = CSVHandler()
            results = handler.batch_process_csv(csv_file, module_name, command, output)
            
            # Afficher les résultats
            table = Table(title="Résultats du traitement par lot")
            table.add_column("Ligne", style="cyan")
            table.add_column("Élément", style="green")
            table.add_column("Statut", style="yellow")
            table.add_column("Résultat", style="white")
            
            for result in results:
                status_style = "green" if result.get('status') == 'success' else "red"
                table.add_row(
                    str(result.get('row_index', '')),
                    result.get('element_id', ''),
                    result.get('status', ''),
                    str(result.get('result', ''))[:50] + "..." if len(str(result.get('result', ''))) > 50 else str(result.get('result', ''))
                )
            
            console.print(table)
            console.print(f"[green]✓[/green] Traitement par lot terminé: {output}")
            
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
    
    return app 