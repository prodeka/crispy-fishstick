# src/lcpi/shell/main.py
import os
import pathlib
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
import json
import typer

console = Console()

class EnhancedShell:
    def __init__(self):
        self.variables = {}
        self.current_project = None
        
    def run(self):
        """Lance le shell interactif."""
        console.print(
            Panel(
                "[bold green]Bienvenue dans LCPI-CLI Enhanced Shell![/bold green]\n\n"
                "Ce shell interactif vous permet d'exécuter des commandes LCPI-CLI.\n\n"
                "[bold yellow]Commandes disponibles:[/bold yellow]\n"
                "• [yellow]help[/yellow] - Afficher l'aide\n"
                "• [yellow]clear[/yellow] - Effacer l'écran\n"
                "• [yellow]pwd[/yellow] - Afficher le répertoire courant\n"
                "• [yellow]ls[/yellow] - Lister les fichiers/modules\n"
                "• [yellow]set[/yellow] - Définir une variable\n"
                "• [yellow]get[/yellow] - Afficher la valeur d'une variable\n"
                "• [yellow]vars[/yellow] - Afficher toutes les variables\n"
                "• [yellow]csv[/yellow] - Commandes CSV\n"
                "• [yellow]calc[/yellow] - Calculs\n"
                "• [yellow]report[/yellow] - Rapports\n"
                "• [yellow]exit[/yellow] - Quitter\n\n"
                "[blue]Tapez 'help' pour plus d'informations[/blue]",
                title="🚀 Bienvenue dans LCPI-CLI Enhanced Shell",
                border_style="blue"
            )
        )
        
        while True:
            try:
                command_line = Prompt.ask("[bold green]LCPI[/bold green] > ").strip()
                if not command_line:
                    continue
                
                if command_line.lower() in ['exit', 'quit']:
                    break
                
                self._execute_command(command_line)
            except KeyboardInterrupt:
                console.print("\n[yellow]Interruption par l'utilisateur.[/yellow]")
                break
            except EOFError:
                console.print("\n[yellow]Fin de l'entrée.[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Erreur: {e}[/red]")
        
        console.print("[green]Au revoir ![/green]")
    
    def _execute_command(self, command_line: str):
        """Exécute une commande."""
        parts = command_line.split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == 'help':
            self._cmd_help(args)
        elif cmd == 'clear':
            console.clear()
        elif cmd == 'pwd':
            console.print(f"[green]{os.getcwd()}[/green]")
        elif cmd == 'ls':
            self._cmd_ls(args)
        elif cmd == 'set':
            self._cmd_set(args)
        elif cmd == 'get':
            self._cmd_get(args)
        elif cmd == 'vars':
            self._cmd_vars()
        elif cmd == 'csv':
            self._cmd_csv(args)
        elif cmd == 'calc':
            self._cmd_calc(args)
        elif cmd == 'report':
            self._cmd_report(args)
        
        # Commande inconnue
        else:
            console.print(f"[red]Commande inconnue: '{cmd}'[/red]")
            console.print("[yellow]Tapez 'help' pour voir les commandes disponibles[/yellow]")
    
    def _cmd_help(self, args):
        """Affiche l'aide."""
        help_text = """
[bold cyan]LCPI-CLI Enhanced Shell - Commandes disponibles[/bold cyan]

[bold green]Général:[/bold green]
  help                  - Afficher l'aide
  clear                 - Effacer l'écran
  pwd                   - Afficher le répertoire courant
  ls [module]           - Lister les fichiers ou les commandes d'un module

[bold green]Variables:[/bold green]
  set <nom>=<valeur>    - Définir une variable
  get <nom>             - Afficher la valeur d'une variable
  vars                  - Afficher toutes les variables définies

[bold green]CSV:[/bold green]
  csv import <file>     - Importer un fichier CSV
  csv export <file>     - Exporter vers CSV
  csv validate <file>   - Valider un fichier CSV
  csv template <cmd>    - Générer un template CSV

[bold green]Calculs:[/bold green]
  calc <module> <cmd>   - Exécuter un calcul

[bold green]Rapports:[/bold green]
  report generate       - Générer un rapport
  report compare <v1> <v2> - Comparer des versions

[bold green]Autres:[/bold green]
  exit/quit             - Quitter le shell
        """
        console.print(Panel(help_text, title="📚 Aide", border_style="green"))
    
    def _cmd_ls(self, args):
        """Liste les fichiers ou les commandes d'un module."""
        if not args:
            # Lister les fichiers du répertoire courant
            try:
                items = os.listdir('.')
                for item in items:
                    if os.path.isdir(item):
                        console.print(f"[blue]{item}/[/blue]")
                    else:
                        console.print(f"[white]{item}[/white]")
            except Exception as e:
                console.print(f"[red]Erreur: {e}[/red]")
        else:
            module_name = args[0]
            console.print(f"[cyan]Commandes pour le module '{module_name}':[/cyan]")
            # Ici, on pourrait intégrer la logique pour lister les commandes d'un module LCPI
            # Pour l'instant, c'est une simulation
            console.print(f"  - Commande 1 de {module_name}")
            console.print(f"  - Commande 2 de {module_name}")
    
    def _cmd_set(self, args):
        """Définit une variable."""
        if not args or '=' not in ' '.join(args):
            console.print("[red]Usage: set <nom>=<valeur>[/red]")
            return
        
        full_cmd = ' '.join(args)
        var_part, value_part = full_cmd.split('=', 1)
        var_name = var_part.strip()
        var_value = value_part.strip()
        
        self.variables[var_name] = var_value
        console.print(f"[green]Variable '{var_name}' définie à '{var_value}'[/green]")
    
    def _cmd_get(self, args):
        """Affiche la valeur d'une variable."""
        if not args:
            console.print("[red]Usage: get <nom>[/red]")
            return
        
        var_name = args[0]
        if var_name in self.variables:
            console.print(f"[green]{var_name} = {self.variables[var_name]}[/green]")
        else:
            console.print(f"[red]Variable '{var_name}' non définie[/red]")
    
    def _cmd_vars(self):
        """Affiche toutes les variables."""
        if not self.variables:
            console.print("[yellow]Aucune variable définie.[/yellow]")
            return
        
        table = Table(title="Variables définies")
        table.add_column("Nom", style="cyan")
        table.add_column("Valeur", style="magenta")
        
        for name, value in self.variables.items():
            table.add_row(name, value)
        
        console.print(table)
    
    def _cmd_csv(self, args):
        """Commandes CSV."""
        if not args:
            console.print("[red]Usage: csv <import|export|validate|template> [args...][/red]")
            return
        
        subcmd = args[0]
        if subcmd == 'import':
            console.print(f"[cyan]Import CSV: {' '.join(args[1:])}[/cyan]")
        elif subcmd == 'export':
            console.print(f"[cyan]Export CSV: {' '.join(args[1:])}[/cyan]")
        elif subcmd == 'validate':
            console.print(f"[cyan]Validation CSV: {' '.join(args[1:])}[/cyan]")
        elif subcmd == 'template':
            console.print(f"[cyan]Template CSV: {' '.join(args[1:])}[/cyan]")
        else:
            console.print(f"[red]Sous-commande CSV inconnue: {subcmd}[/red]")
    
    def _cmd_calc(self, args):
        """Exécute un calcul."""
        if len(args) < 2:
            console.print("[red]Usage: calc <module> <command> [args...][/red]")
            return
        
        module = args[0]
        command = args[1]
        cmd_args = args[2:]
        
        console.print(f"[cyan]Calcul {module} {command} {' '.join(cmd_args)}[/cyan]")
    
    def _cmd_report(self, args):
        """Commandes de rapport."""
        if not args:
            console.print("[red]Usage: report <generate|compare> [args...][/red]")
            return
        
        subcmd = args[0]
        if subcmd == 'generate':
            console.print("[cyan]Génération de rapport...[/cyan]")
        elif subcmd == 'compare':
            if len(args) < 3:
                console.print("[red]Usage: report compare <version1> <version2>[/red]")
                return
            v1, v2 = args[1], args[2]
            console.print(f"[cyan]Comparaison: {v1} vs {v2}[/cyan]")
        else:
            console.print(f"[red]Sous-commande rapport inconnue: {subcmd}[/red]")

app = typer.Typer(name="shell", help="Interpréteur de commandes interactif")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Lance le shell interactif."""
    if ctx.invoked_subcommand is None:
        shell = EnhancedShell()
        shell.run()

def register():
    """Enregistre le plugin avec le noyau."""
    return app

if __name__ == '__main__':
    app()
