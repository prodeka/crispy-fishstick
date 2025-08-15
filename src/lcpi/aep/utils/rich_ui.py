"""
Module centralisé pour les composants Rich UI.
Fournit une interface cohérente et moderne pour toutes les commandes CLI.
"""

from rich.console import Console
from rich.table import Table
from rich.status import Status
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from typing import List, Dict, Any, Optional
import typer

# Console globale pour tout le projet
console = Console()

class RichUI:
    """Classe utilitaire pour les composants Rich UI."""
    
    @staticmethod
    def print_success(message: str):
        """Affiche un message de succès."""
        console.print(f"✅ {message}", style="green")
    
    @staticmethod
    def print_error(message: str):
        """Affiche un message d'erreur."""
        console.print(f"❌ {message}", style="red")
    
    @staticmethod
    def print_warning(message: str):
        """Affiche un message d'avertissement."""
        console.print(f"⚠️ {message}", style="yellow")
    
    @staticmethod
    def print_info(message: str):
        """Affiche un message d'information."""
        console.print(f"ℹ️ {message}", style="blue")
    
    @staticmethod
    def print_header(title: str):
        """Affiche un en-tête de section."""
        console.print(f"\n[bold cyan]{title}[/bold cyan]")
        console.print("=" * len(title))
    
    @staticmethod
    def create_results_table(title: str, data: List[Dict[str, Any]]) -> Table:
        """Crée un tableau de résultats avec Rich."""
        if not data:
            return Table(title=title, show_header=False)
        
        table = Table(title=title)
        
        # Ajouter les colonnes basées sur les clés du premier élément
        for key in data[0].keys():
            table.add_column(key, style="cyan")
        
        # Ajouter les données
        for row in data:
            table.add_row(*[str(value) for value in row.values()])
        
        return table
    
    @staticmethod
    def create_parameters_table(title: str, parameters: Dict[str, Any]) -> Table:
        """Crée un tableau de paramètres avec Rich."""
        table = Table(title=title)
        table.add_column("Paramètre", style="cyan")
        table.add_column("Valeur", style="magenta")
        table.add_column("Unité", style="yellow", no_wrap=True)
        
        for param, value in parameters.items():
            if isinstance(value, tuple) and len(value) == 2:
                val, unit = value
                table.add_row(param, str(val), unit)
            else:
                table.add_row(param, str(value), "")
        
        return table
    
    @staticmethod
    def show_status_with_spinner(message: str):
        """Affiche un spinner avec un message."""
        return console.status(f"[bold green]{message}")
    
    @staticmethod
    def show_progress_bar(total: int, description: str = "Traitement en cours..."):
        """Affiche une barre de progression."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        )
    
    @staticmethod
    def show_code_snippet(code: str, language: str = "python"):
        """Affiche un snippet de code avec coloration syntaxique."""
        syntax = Syntax(code, language, theme="monokai")
        console.print(syntax)
    
    @staticmethod
    def show_panel(content: str, title: str = "", border_style: str = "blue"):
        """Affiche un contenu dans un panel."""
        panel = Panel(content, title=title, border_style=border_style)
        console.print(panel)
    
    @staticmethod
    def prompt_choice(message: str, choices: List[str]) -> str:
        """Demande à l'utilisateur de choisir parmi une liste d'options."""
        console.print(f"\n{message}")
        for i, choice in enumerate(choices, 1):
            console.print(f"{i}. {choice}")
        
        while True:
            try:
                choice = Prompt.ask("Votre choix", choices=[str(i) for i in range(1, len(choices) + 1)])
                return choices[int(choice) - 1]
            except ValueError:
                console.print("Choix invalide. Veuillez réessayer.", style="red")
    
    @staticmethod
    def confirm_action(message: str) -> bool:
        """Demande confirmation à l'utilisateur."""
        return Confirm.ask(message)

# Fonctions utilitaires pour migration progressive
def migrate_echo_to_rich(message: str, style: str = "default"):
    """Remplace typer.echo() par console.print() avec style."""
    if style == "success":
        RichUI.print_success(message)
    elif style == "error":
        RichUI.print_error(message)
    elif style == "warning":
        RichUI.print_warning(message)
    elif style == "info":
        RichUI.print_info(message)
    else:
        console.print(message)

def show_calculation_results(results: Dict[str, Any], title: str = "Résultats du Calcul"):
    """Affiche les résultats d'un calcul de manière structurée."""
    RichUI.print_header(title)
    
    # Afficher les valeurs principales
    if "valeurs" in results:
        console.print("\n[bold]Valeurs principales :[/bold]")
        for key, value in results["valeurs"].items():
            console.print(f"  • {key}: {value}")
    
    # Afficher les diagnostics
    if "diagnostics" in results:
        console.print("\n[bold]Diagnostics :[/bold]")
        for key, value in results["diagnostics"].items():
            status_style = "green" if value else "red"
            status_icon = "✅" if value else "❌"
            console.print(f"  {status_icon} {key}: {value}", style=status_style)
    
    # Afficher les itérations si disponibles
    if "iterations" in results:
        console.print("\n[bold]Détails des itérations :[/bold]")
        for key, value in results["iterations"].items():
            console.print(f"  • {key}: {value}")

def show_network_diagnostics(diagnostics: Dict[str, Any]):
    """Affiche les diagnostics d'un réseau de manière visuelle."""
    RichUI.print_header("Diagnostics du Réseau")
    
    # Tableau des diagnostics
    table = Table(title="État du Réseau")
    table.add_column("Composant", style="cyan")
    table.add_column("Statut", style="magenta")
    table.add_column("Détails", style="yellow")
    
    for component, status in diagnostics.items():
        if isinstance(status, dict):
            status_text = status.get("status", "N/A")
            details = status.get("details", "")
        else:
            status_text = "OK" if status else "ERREUR"
            details = ""
        
        status_style = "green" if status_text == "OK" else "red"
        table.add_row(component, f"[{status_style}]{status_text}[/{status_style}]", details)
    
    console.print(table)
