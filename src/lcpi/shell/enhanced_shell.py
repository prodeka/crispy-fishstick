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
            "• [yellow]aep[/yellow] - Commandes AEP unifiées\n"
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
        
        # Commandes spécialisées
        elif cmd == 'csv':
            self._cmd_csv(args)
        elif cmd == 'calc':
            self._cmd_calc(args)
        elif cmd == 'report':
            self._cmd_report(args)
        
        # Commandes AEP unifiées
        elif cmd == 'aep':
            self._cmd_aep(args)
        
        else:
            console.print(f"[red]Commande inconnue: {cmd}[/red]")
            console.print("[yellow]Tapez 'help' pour voir les commandes disponibles[/yellow]")
    
    def _cmd_help(self, args):
        """Affiche l'aide."""
        if not args:
            help_text = """
[bold cyan]LCPI-CLI Enhanced Shell - Aide[/bold cyan]

[bold green]Commandes de base:[/bold green]
  help [commande]     - Afficher l'aide générale ou spécifique
  clear              - Effacer l'écran
  pwd                - Afficher le répertoire courant
  ls [chemin]        - Lister les fichiers
  cd [chemin]        - Changer de répertoire
  exit/quit          - Quitter le shell

[bold green]Variables:[/bold green]
  set <nom> <valeur> - Définir une variable
  get <nom>          - Afficher une variable
  vars               - Lister toutes les variables
  unset <nom>        - Supprimer une variable

[bold green]Commandes spécialisées:[/bold green]
  csv <commande>     - Commandes CSV (read, write, analyze)
  calc <expression>  - Calculs mathématiques
  report <type>      - Génération de rapports

[bold green]Commandes AEP unifiées:[/bold green]
  aep population-unified <pop> [options] - Projection démographique
  aep demand-unified <pop> [options]     - Calcul demande en eau
  aep network-unified <debit> [options]  - Dimensionnement réseau
  aep reservoir-unified <volume> [options] - Dimensionnement réservoir
  aep pumping-unified <debit> [options]  - Dimensionnement pompage
  aep help-<module>  - Aide spécifique AEP

[bold green]Exemples:[/bold green]
  aep population-unified 1000 --taux 0.037 --annees 20
  aep demand-unified 1000 --dotation 150 --coeff-pointe 1.5
  aep network-unified 0.1 --longueur 1000 --materiau fonte
  set population 1000
  get population
"""
            console.print(Panel(help_text, title="📚 Aide", border_style="blue"))
        else:
            subcmd = args[0].lower()
            if subcmd == 'aep':
                self._cmd_aep_help()
            else:
                console.print(f"[yellow]Aide spécifique pour '{subcmd}' non disponible[/yellow]")
    
    def _cmd_aep(self, args):
        """Traite les commandes AEP unifiées."""
        if not args:
            self._cmd_aep_help()
            return
        
        subcmd = args[0].lower()
        
        try:
            # Import des modules AEP unifiés
            if subcmd == 'population-unified':
                from lcpi.aep.calculations.population_unified import calculate_population_projection_unified
                
                if len(args) < 2:
                    console.print("[red]Erreur: Population requise[/red]")
                    return
                
                population = int(args[1])
                options = self._parse_aep_options(args[2:])
                
                resultat = calculate_population_projection_unified(
                    population_base=population,
                    taux_croissance=options.get('taux', 0.037),
                    annees=options.get('annees', 20),
                    methode=options.get('methode', 'malthus'),
                    verbose=options.get('verbose', False)
                )
                
                if resultat['statut'] == 'SUCCES':
                    console.print(f"📈 Projection {options.get('methode', 'malthus')}: {resultat['population_finale']:.0f} habitants")
                else:
                    console.print(f"❌ Erreur: {resultat['message']}")
            
            elif subcmd == 'demand-unified':
                from lcpi.aep.calculations.demand_unified import calculate_water_demand_unified
                
                if len(args) < 2:
                    console.print("[red]Erreur: Population requise[/red]")
                    return
                
                population = int(args[1])
                options = self._parse_aep_options(args[2:])
                
                resultat = calculate_water_demand_unified(
                    population=population,
                    dotation_l_j_hab=options.get('dotation', 150),
                    coefficient_pointe=options.get('coeff-pointe', 1.5),
                    verbose=options.get('verbose', False)
                )
                
                if resultat['statut'] == 'SUCCES':
                    console.print(f"💧 Demande en eau:")
                    if 'besoin_brut_m3j' in resultat:
                        console.print(f"   Besoin brut: {resultat['besoin_brut_m3j']:.1f} m³/j")
                    if 'debit_pointe_m3s' in resultat:
                        console.print(f"   Débit pointe: {resultat['debit_pointe_m3s']:.3f} m³/s")
                else:
                    console.print(f"❌ Erreur: {resultat['message']}")
            
            elif subcmd == 'network-unified':
                from lcpi.aep.calculations.network_unified import dimension_network_unified
                
                if len(args) < 2:
                    console.print("[red]Erreur: Débit requis[/red]")
                    return
                
                debit = float(args[1])
                options = self._parse_aep_options(args[2:])
                
                data = {
                    "debit_m3s": debit,
                    "longueur_m": options.get('longueur', 1000),
                    "materiau": options.get('materiau', 'fonte'),
                    "perte_charge_max_m": options.get('perte-max', 10.0),
                    "methode": options.get('methode', 'darcy')
                }
                
                resultat = dimension_network_unified(data, options.get('verbose', False))
                
                if resultat['statut'] == 'SUCCES':
                    console.print(f"🔧 Dimensionnement réseau ({options.get('methode', 'darcy')}):")
                    console.print(f"   Diamètre: {resultat['reseau']['diametre_optimal_mm']} mm")
                    console.print(f"   Vitesse: {resultat['reseau']['vitesse_ms']:.2f} m/s")
                else:
                    console.print(f"❌ Erreur: {resultat['message']}")
            
            elif subcmd == 'reservoir-unified':
                from lcpi.aep.calculations.reservoir_unified import dimension_reservoir_unified
                
                if len(args) < 2:
                    console.print("[red]Erreur: Volume journalier requis[/red]")
                    return
                
                volume = float(args[1])
                options = self._parse_aep_options(args[2:])
                
                data = {
                    "volume_journalier_m3": volume,
                    "type_adduction": options.get('adduction', 'continue'),
                    "forme_reservoir": options.get('forme', 'cylindrique'),
                    "type_zone": options.get('zone', 'ville_francaise_peu_importante')
                }
                
                resultat = dimension_reservoir_unified(data, options.get('verbose', False))
                
                if resultat['statut'] == 'SUCCES':
                    console.print(f"🏗️ Dimensionnement réservoir ({options.get('forme', 'cylindrique')}):")
                    console.print(f"   Volume utile: {resultat['reservoir']['volume_utile_m3']:.1f} m³")
                    console.print(f"   Capacité pratique: {resultat['reservoir']['capacite_pratique_m3']:.1f} m³")
                else:
                    console.print(f"❌ Erreur: {resultat['message']}")
            
            elif subcmd == 'pumping-unified':
                from lcpi.aep.calculations.pumping_unified import dimension_pumping_unified
                
                if len(args) < 2:
                    console.print("[red]Erreur: Débit requis[/red]")
                    return
                
                debit = float(args[1])
                options = self._parse_aep_options(args[2:])
                
                data = {
                    "debit_m3h": debit,
                    "hmt_m": options.get('hmt', 50),
                    "type_pompe": options.get('type', 'centrifuge'),
                    "rendement_pompe": options.get('rendement', 0.75)
                }
                
                resultat = dimension_pumping_unified(data, options.get('verbose', False))
                
                if resultat['statut'] == 'SUCCES':
                    console.print(f"⚡ Dimensionnement pompage ({options.get('type', 'centrifuge')}):")
                    console.print(f"   Puissance électrique: {resultat['pompage']['puissance_electrique_kw']:.1f} kW")
                    console.print(f"   Puissance groupe: {resultat['pompage']['puissance_groupe_kva']:.1f} kVA")
                else:
                    console.print(f"❌ Erreur: {resultat['message']}")
            
            elif subcmd.startswith('help-'):
                self._cmd_aep_help_specific(subcmd[5:])
            
            else:
                console.print(f"[red]Commande AEP inconnue: {subcmd}[/red]")
                self._cmd_aep_help()
        
        except ImportError as e:
            console.print(f"[red]Erreur d'import: {e}[/red]")
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
    
    def _parse_aep_options(self, args):
        """Parse les options AEP."""
        options = {}
        i = 0
        while i < len(args):
            if args[i].startswith('--'):
                key = args[i][2:]
                if i + 1 < len(args) and not args[i + 1].startswith('--'):
                    value = args[i + 1]
                    # Conversion automatique des types
                    if value.lower() in ['true', 'false']:
                        options[key] = value.lower() == 'true'
                    elif '.' in value:
                        try:
                            options[key] = float(value)
                        except ValueError:
                            options[key] = value
                    else:
                        try:
                            options[key] = int(value)
                        except ValueError:
                            options[key] = value
                    i += 2
                else:
                    options[key] = True
                    i += 1
            else:
                i += 1
        return options
    
    def _cmd_aep_help(self):
        """Affiche l'aide AEP."""
        help_text = """
[bold cyan]Commandes AEP Unifiées[/bold cyan]

[bold green]Calculs disponibles:[/bold green]
  population-unified <pop> [options] - Projection démographique
  demand-unified <pop> [options]     - Calcul demande en eau
  network-unified <debit> [options]  - Dimensionnement réseau
  reservoir-unified <volume> [options] - Dimensionnement réservoir
  pumping-unified <debit> [options]  - Dimensionnement pompage

[bold green]Options communes:[/bold green]
  --verbose          - Afficher les détails
  --help            - Afficher l'aide spécifique

[bold green]Exemples:[/bold green]
  aep population-unified 1000 --taux 0.037 --annees 20
  aep demand-unified 1000 --dotation 150 --coeff-pointe 1.5
  aep network-unified 0.1 --longueur 1000 --materiau fonte
  aep reservoir-unified 1000 --adduction continue --forme cylindrique
  aep pumping-unified 100 --hmt 50 --type centrifuge

[bold green]Aide spécifique:[/bold green]
  aep help-population-unified
  aep help-demand-unified
  aep help-network-unified
  aep help-reservoir-unified
  aep help-pumping-unified
"""
        console.print(Panel(help_text, title="🔵 AEP Unifié", border_style="blue"))
    
    def _cmd_aep_help_specific(self, module):
        """Affiche l'aide spécifique pour un module AEP."""
        try:
            if module == 'population-unified':
                from lcpi.aep.calculations.population_unified import get_population_unified_help
                console.print(Panel(get_population_unified_help(), title="🔢 Population Unifié", border_style="blue"))
            elif module == 'demand-unified':
                from lcpi.aep.calculations.demand_unified import get_demand_unified_help
                console.print(Panel(get_demand_unified_help(), title="💧 Demande Unifié", border_style="blue"))
            elif module == 'network-unified':
                from lcpi.aep.calculations.network_unified import get_network_unified_help
                console.print(Panel(get_network_unified_help(), title="🔧 Réseau Unifié", border_style="blue"))
            elif module == 'reservoir-unified':
                from lcpi.aep.calculations.reservoir_unified import get_reservoir_unified_help
                console.print(Panel(get_reservoir_unified_help(), title="🏗️ Réservoir Unifié", border_style="blue"))
            elif module == 'pumping-unified':
                from lcpi.aep.calculations.pumping_unified import get_pumping_unified_help
                console.print(Panel(get_pumping_unified_help(), title="⚡ Pompage Unifié", border_style="blue"))
            else:
                console.print(f"[yellow]Aide non disponible pour: {module}[/yellow]")
        except ImportError:
            console.print(f"[red]Module {module} non disponible[/red]")
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")

    def _cmd_ls(self, args):
        """Liste les fichiers."""
        path = args[0] if args else "."
        try:
            files = os.listdir(path)
            for file in files:
                console.print(f"[green]{file}[/green]")
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
    
    def _cmd_cd(self, args):
        """Change de répertoire."""
        if not args:
            console.print("[yellow]Usage: cd <chemin>[/yellow]")
            return
        
        try:
            os.chdir(args[0])
            console.print(f"[green]Répertoire changé vers: {os.getcwd()}[/green]")
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
    
    def _cmd_set(self, args):
        """Définit une variable."""
        if len(args) < 2:
            console.print("[yellow]Usage: set <nom> <valeur>[/yellow]")
            return
        
        name = args[0]
        value = " ".join(args[1:])
        
        # Conversion automatique des types
        if value.lower() in ['true', 'false']:
            self.variables[name] = value.lower() == 'true'
        elif '.' in value:
            try:
                self.variables[name] = float(value)
            except ValueError:
                self.variables[name] = value
        else:
            try:
                self.variables[name] = int(value)
            except ValueError:
                self.variables[name] = value
        
        console.print(f"[green]Variable '{name}' définie[/green]")
    
    def _cmd_get(self, args):
        """Affiche une variable."""
        if not args:
            console.print("[yellow]Usage: get <nom>[/yellow]")
            return
        
        name = args[0]
        if name in self.variables:
            console.print(f"[green]{name}[/green] = [yellow]{self.variables[name]}[/yellow]")
        else:
            console.print(f"[red]Variable '{name}' non définie[/red]")
    
    def _cmd_vars(self):
        """Liste toutes les variables."""
        if not self.variables:
            console.print("[yellow]Aucune variable définie[/yellow]")
            return
        
        table = Table(title="Variables")
        table.add_column("Nom", style="green")
        table.add_column("Valeur", style="yellow")
        table.add_column("Type", style="blue")
        
        for name, value in self.variables.items():
            table.add_row(name, str(value), type(value).__name__)
        
        console.print(table)
    
    def _cmd_unset(self, args):
        """Supprime une variable."""
        if not args:
            console.print("[yellow]Usage: unset <nom>[/yellow]")
            return
        
        name = args[0]
        if name in self.variables:
            del self.variables[name]
            console.print(f"[green]Variable '{name}' supprimée[/green]")
        else:
            console.print(f"[red]Variable '{name}' non définie[/red]")
    
    def _cmd_csv(self, args):
        """Commandes CSV."""
        if not args:
            console.print("[yellow]Usage: csv <commande> [options][/yellow]")
            return
        
        cmd = args[0].lower()
        if cmd == 'read':
            if len(args) < 2:
                console.print("[yellow]Usage: csv read <fichier>[/yellow]")
                return
            
            try:
                import pandas as pd
                df = pd.read_csv(args[1])
                console.print(f"[green]CSV lu: {len(df)} lignes, {len(df.columns)} colonnes[/green]")
                console.print(df.head())
            except Exception as e:
                console.print(f"[red]Erreur: {e}[/red]")
        
        elif cmd == 'write':
            console.print("[yellow]Commande csv write non implémentée[/yellow]")
        
        else:
            console.print(f"[red]Commande CSV inconnue: {cmd}[/red]")
    
    def _cmd_calc(self, args):
        """Calculs mathématiques."""
        if not args:
            console.print("[yellow]Usage: calc <expression>[/yellow]")
            return
        
        try:
            expression = " ".join(args)
            result = eval(expression, {"__builtins__": {}}, self.variables)
            console.print(f"[green]Résultat: {result}[/green]")
        except Exception as e:
            console.print(f"[red]Erreur de calcul: {e}[/red]")
    
    def _cmd_report(self, args):
        """Génération de rapports."""
        if not args:
            console.print("[yellow]Usage: report <type> [options][/yellow]")
            return
        
        report_type = args[0].lower()
        console.print(f"[yellow]Génération de rapport '{report_type}' non implémentée[/yellow]")

def main():
    """Fonction principale."""
    shell = EnhancedShell()
    shell.run()

if __name__ == "__main__":
    main() 