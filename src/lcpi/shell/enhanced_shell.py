"""
Shell interactif amélioré pour LCPI-CLI
"""

import sys
import os
import pathlib
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
import json

console = Console()

class EnhancedShell:
    """Shell interactif amélioré pour LCPI-CLI."""
    
    def __init__(self):
        self.history = []
        self.variables = {}
        self.current_project = None
        
    def run(self):
        """Lance le shell interactif."""
        # Message de bienvenue
        welcome_panel = Panel(
            "[bold cyan]LCPI-CLI Enhanced Shell[/bold cyan]\n\n"
            "[green]Commandes disponibles:[/green]\n"
            "• [yellow]help[/yellow] - Afficher l'aide\n"
            "• [yellow]csv[/yellow] - Commandes CSV\n"
            "• [yellow]calc[/yellow] - Calculs\n"
            "• [yellow]report[/yellow] - Rapports\n"
            "• [yellow]vars[/yellow] - Variables\n"
            "• [yellow]exit[/yellow] - Quitter\n\n"
            "[blue]Tapez 'help' pour plus d'informations[/blue]",
            title="🚀 Bienvenue dans LCPI-CLI Enhanced Shell",
            border_style="cyan"
        )
        console.print(welcome_panel)
        
        # Boucle principale
        while True:
            try:
                # Afficher le prompt
                prompt_text = f"[bold green]lcpi[/bold green]"
                if self.current_project:
                    prompt_text += f"[bold yellow]@{self.current_project}[/bold yellow]"
                prompt_text += "[bold white]>[/bold white] "
                
                # Lire la commande
                command = Prompt.ask(prompt_text)
                
                if not command.strip():
                    continue
                
                # Ajouter à l'historique
                self.history.append(command)
                
                # Traiter la commande
                self._process_command(command)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Utilisez 'exit' pour quitter[/yellow]")
            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Erreur: {e}[/red]")
        
        console.print("[green]Au revoir ![/green]")
    
    def _process_command(self, command: str):
        """Traite une commande."""
        parts = command.split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        # Commandes de base
        if cmd in ['exit', 'quit']:
            raise EOFError()
        elif cmd == 'help':
            self._cmd_help(args)
        elif cmd == 'clear':
            console.clear()
        elif cmd == 'pwd':
            console.print(f"[green]{os.getcwd()}[/green]")
        elif cmd == 'ls':
            self._cmd_ls(args)
        elif cmd == 'cd':
            self._cmd_cd(args)
        
        # Variables
        elif cmd == 'set':
            self._cmd_set(args)
        elif cmd == 'get':
            self._cmd_get(args)
        elif cmd == 'vars':
            self._cmd_vars()
        elif cmd == 'unset':
            self._cmd_unset(args)
        
        # CSV
        elif cmd == 'csv':
            self._cmd_csv(args)
        
        # Calculs
        elif cmd == 'calc':
            self._cmd_calc(args)
        
        # Rapports
        elif cmd == 'report':
            self._cmd_report(args)
        
        # Commande inconnue
        else:
            console.print(f"[red]Commande inconnue: {cmd}[/red]")
            console.print("[yellow]Tapez 'help' pour voir les commandes disponibles[/yellow]")
    
    def _cmd_help(self, args):
        """Affiche l'aide."""
        help_text = """
[bold cyan]LCPI-CLI Enhanced Shell - Commandes disponibles[/bold cyan]

[bold green]Navigation:[/bold green]
  pwd                    - Afficher le répertoire courant
  ls [dir]              - Lister les fichiers
  cd <dir>              - Changer de répertoire
  clear                 - Effacer l'écran

[bold green]Variables:[/bold green]
  set <var> = <value>   - Définir une variable
  get <var>             - Afficher une variable
  vars                  - Lister toutes les variables
  unset <var>           - Supprimer une variable

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
  help                  - Afficher l'aide
  exit/quit             - Quitter le shell
        """
        console.print(Panel(help_text, title="📚 Aide", border_style="green"))
    
    def _cmd_ls(self, args):
        """Liste les fichiers."""
        path = args[0] if args else "."
        try:
            files = os.listdir(path)
            table = Table(title=f"Contenu de {path}")
            table.add_column("Nom", style="cyan")
            table.add_column("Type", style="green")
            
            for file in files:
                file_path = os.path.join(path, file)
                file_type = "📁" if os.path.isdir(file_path) else "📄"
                table.add_row(file, file_type)
            
            console.print(table)
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
    
    def _cmd_cd(self, args):
        """Change de répertoire."""
        if not args:
            console.print("[red]Usage: cd <directory>[/red]")
            return
        
        try:
            os.chdir(args[0])
            console.print(f"[green]Répertoire changé: {os.getcwd()}[/green]")
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
    
    def _cmd_set(self, args):
        """Définit une variable."""
        if len(args) < 2 or '=' not in ' '.join(args):
            console.print("[red]Usage: set <var> = <value>[/red]")
            return
        
        full_cmd = ' '.join(args)
        var_part, value_part = full_cmd.split('=', 1)
        var = var_part.strip()
        value = value_part.strip()
        
        self.variables[var] = value
        console.print(f"[green]Variable '{var}' définie: {value}[/green]")
    
    def _cmd_get(self, args):
        """Affiche une variable."""
        if not args:
            console.print("[red]Usage: get <var>[/red]")
            return
        
        var = args[0]
        if var in self.variables:
            console.print(f"[green]{var} = {self.variables[var]}[/green]")
        else:
            console.print(f"[red]Variable '{var}' non définie[/red]")
    
    def _cmd_vars(self):
        """Liste toutes les variables."""
        if not self.variables:
            console.print("[yellow]Aucune variable définie[/yellow]")
            return
        
        table = Table(title="Variables définies")
        table.add_column("Variable", style="cyan")
        table.add_column("Valeur", style="green")
        
        for var, value in self.variables.items():
            table.add_row(var, str(value))
        
        console.print(table)
    
    def _cmd_unset(self, args):
        """Supprime une variable."""
        if not args:
            console.print("[red]Usage: unset <var>[/red]")
            return
        
        var = args[0]
        if var in self.variables:
            del self.variables[var]
            console.print(f"[green]Variable '{var}' supprimée[/green]")
        else:
            console.print(f"[red]Variable '{var}' non définie[/red]")
    
    def _cmd_csv(self, args):
        """Commandes CSV."""
        if not args:
            console.print("[red]Usage: csv <import|export|validate|template>[/red]")
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
            console.print("[red]Usage: report <generate|compare>[/red]")
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

def main():
    """Point d'entrée principal."""
    shell = EnhancedShell()
    shell.run()

if __name__ == '__main__':
    main() 