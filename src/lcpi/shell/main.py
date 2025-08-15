# src/lcpi/shell/main.py
import os
import pathlib
import subprocess
import tempfile
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
import json
import typer
import csv
import yaml

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
                "• [yellow]aep[/yellow] - Alimentation en Eau Potable\n"
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
        elif cmd == 'aep':
            self._cmd_aep(args)
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

[bold green]AEP (Alimentation en Eau Potable):[/bold green]
  aep population <file> - Projection démographique
  aep demand <file>     - Calcul de demande en eau
  aep network <file>    - Dimensionnement réseau
  aep reservoir <file>  - Dimensionnement réservoir
  aep pumping <file>    - Dimensionnement pompage
  aep hardy-cross <file> - Méthode Hardy-Cross
  aep workflow <file>   - Workflow AEP complet

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
            self._list_module_commands(module_name)
    
    def _list_module_commands(self, module_name: str):
        """Liste les commandes disponibles pour un module."""
        try:
            # Construire la commande LCPI help
            lcpi_cmd = ["lcpi", module_name, "--help"]
            
            # Exécuter la commande
            result = subprocess.run(lcpi_cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                console.print(f"[cyan]Commandes pour le module '{module_name}':[/cyan]")
                
                # Parser la sortie pour extraire les commandes
                lines = result.stdout.split('\n')
                commands = []
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('Usage:') and not line.startswith('Options:') and not line.startswith('--'):
                        # Chercher les commandes (lignes qui commencent par des lettres)
                        if line and line[0].isalpha() and ' ' in line:
                            cmd_part = line.split()[0]
                            if cmd_part not in ['Try', 'For', 'See']:
                                commands.append(cmd_part)
                
                if commands:
                    for cmd in commands:
                        console.print(f"  - [green]{cmd}[/green]")
                else:
                    console.print(f"  [yellow]Aucune commande trouvée pour {module_name}[/yellow]")
                    
            else:
                console.print(f"[red]Module '{module_name}' non trouvé ou erreur[/red]")
                
        except Exception as e:
            console.print(f"[red]Erreur lors de la liste des commandes: {e}[/red]")
            # Fallback vers la simulation
            console.print(f"[cyan]Commandes pour le module '{module_name}':[/cyan]")
            console.print(f"  - [green]check-poteau[/green]")
            console.print(f"  - [green]check-poutre[/green]")
            console.print(f"  - [green]optimize[/green]")
    
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
            self._csv_import(args[1:])
        elif subcmd == 'export':
            self._csv_export(args[1:])
        elif subcmd == 'validate':
            self._csv_validate(args[1:])
        elif subcmd == 'template':
            self._csv_template(args[1:])
        else:
            console.print(f"[red]Sous-commande CSV inconnue: {subcmd}[/red]")
    
    def _csv_import(self, args):
        """Importe un fichier CSV."""
        if not args:
            console.print("[red]Usage: csv import <fichier.csv> [module][/red]")
            return
        
        csv_file = args[0]
        module = args[1] if len(args) > 1 else None
        
        try:
            if not os.path.exists(csv_file):
                console.print(f"[red]Fichier non trouvé: {csv_file}[/red]")
                return
            
            # Lire le CSV
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            # Détecter le module si non spécifié
            if not module:
                module = self._detect_module_from_csv(data)
            
            # Convertir en YAML
            yaml_data = self._csv_to_yaml_data(data, module)
            
            # Sauvegarder en YAML
            yaml_file = csv_file.replace('.csv', '.yml')
            with open(yaml_file, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True)
            
            console.print(f"[green]✓[/green] Import CSV réussi: {csv_file} → {yaml_file}")
            console.print(f"[cyan]Module détecté: {module}[/cyan]")
            console.print(f"[cyan]Lignes traitées: {len(data)}[/cyan]")
            
        except Exception as e:
            console.print(f"[red]Erreur lors de l'import: {e}[/red]")
    
    def _csv_export(self, args):
        """Exporte vers CSV."""
        if not args:
            console.print("[red]Usage: csv export <fichier.yml> [module][/red]")
            return
        
        yaml_file = args[0]
        module = args[1] if len(args) > 1 else None
        
        try:
            if not os.path.exists(yaml_file):
                console.print(f"[red]Fichier non trouvé: {yaml_file}[/red]")
                return
            
            # Lire le YAML
            with open(yaml_file, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
            
            # Détecter le module si non spécifié
            if not module:
                module = self._detect_module_from_yaml(yaml_data)
            
            # Convertir en CSV
            csv_data = self._yaml_to_csv_data(yaml_data, module)
            
            # Sauvegarder en CSV
            csv_file = yaml_file.replace('.yml', '.csv')
            if csv_data:
                with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                    writer.writeheader()
                    writer.writerows(csv_data)
            
            console.print(f"[green]✓[/green] Export CSV réussi: {yaml_file} → {csv_file}")
            console.print(f"[cyan]Module détecté: {module}[/cyan]")
            console.print(f"[cyan]Lignes exportées: {len(csv_data)}[/cyan]")
            
        except Exception as e:
            console.print(f"[red]Erreur lors de l'export: {e}[/red]")
    
    def _csv_validate(self, args):
        """Valide un fichier CSV."""
        if not args:
            console.print("[red]Usage: csv validate <fichier.csv> [module][/red]")
            return
        
        csv_file = args[0]
        module = args[1] if len(args) > 1 else None
        
        try:
            if not os.path.exists(csv_file):
                console.print(f"[red]Fichier non trouvé: {csv_file}[/red]")
                return
            
            # Lire le CSV
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            # Détecter le module si non spécifié
            if not module:
                module = self._detect_module_from_csv(data)
            
            # Valider
            validation = self._validate_csv_data(data, module)
            
            # Afficher les résultats
            table = Table(title=f"Validation CSV: {csv_file}")
            table.add_column("Type", style="cyan")
            table.add_column("Message", style="white")
            
            if validation['errors']:
                for error in validation['errors']:
                    table.add_row("❌ Erreur", error)
            
            if validation['warnings']:
                for warning in validation['warnings']:
                    table.add_row("⚠️ Avertissement", warning)
            
            if not validation['errors'] and not validation['warnings']:
                table.add_row("✅ Valide", f"Fichier valide ({validation['row_count']} lignes)")
            
            console.print(table)
            console.print(f"[cyan]Module détecté: {module}[/cyan]")
            
        except Exception as e:
            console.print(f"[red]Erreur lors de la validation: {e}[/red]")
    
    def _csv_template(self, args):
        """Génère un template CSV."""
        if not args:
            console.print("[red]Usage: csv template <module> <commande>[/red]")
            return
        
        if len(args) < 2:
            console.print("[red]Usage: csv template <module> <commande>[/red]")
            return
        
        module = args[0]
        command = args[1]
        
        template = self._get_csv_template(module, command)
        
        if template.startswith("Template non disponible"):
            console.print(f"[red]{template}[/red]")
        else:
            console.print(Panel(template, title=f"Template CSV pour {module} {command}", border_style="cyan"))
    
    def _detect_module_from_yaml(self, yaml_data: Any) -> str:
        """Détecte le module à partir des données YAML."""
        if isinstance(yaml_data, dict):
            if 'beton' in yaml_data:
                return 'beton'
            elif 'essence' in yaml_data or 'classe' in yaml_data:
                return 'bois'
            elif 'acier' in yaml_data or 'section' in yaml_data:
                return 'cm'
            elif 'debit' in yaml_data or 'volume' in yaml_data:
                return 'hydrodrain'
        return 'unknown'
    
    def _detect_module_from_csv(self, csv_data: List[Dict[str, Any]]) -> str:
        """Détecte le module à partir des données CSV."""
        if not csv_data:
            return 'unknown'
        
        headers = csv_data[0].keys()
        if 'beton' in headers:
            return 'beton'
        elif 'essence' in headers:
            return 'bois'
        elif 'acier' in headers:
            return 'cm'
        elif 'debit' in headers or 'volume' in headers:
            return 'hydrodrain'
        return 'unknown'
    
    def _yaml_to_csv_data(self, yaml_data: Any, module: str) -> List[Dict[str, Any]]:
        """Convertit les données YAML en format CSV."""
        if module == 'cm':
            return self._yaml_to_csv_cm(yaml_data)
        elif module == 'bois':
            return self._yaml_to_csv_bois(yaml_data)
        elif module == 'beton':
            return self._yaml_to_csv_beton(yaml_data)
        elif module == 'hydrodrain':
            return self._yaml_to_csv_hydro(yaml_data)
        else:
            return []
    
    def _csv_to_yaml_data(self, csv_data: List[Dict[str, Any]], module: str) -> Any:
        """Convertit les données CSV en format YAML."""
        if module == 'cm':
            return self._csv_to_yaml_cm(csv_data)
        elif module == 'bois':
            return self._csv_to_yaml_bois(csv_data)
        elif module == 'beton':
            return self._csv_to_yaml_beton(csv_data)
        elif module == 'hydrodrain':
            return self._csv_to_yaml_hydro(csv_data)
        else:
            return {}
    
    def _validate_csv_data(self, csv_data: List[Dict[str, Any]], module: str) -> Dict[str, Any]:
        """Valide les données CSV selon le module."""
        errors = []
        warnings = []
        
        for i, row in enumerate(csv_data):
            if not row.get('element_id'):
                errors.append(f"Ligne {i+1}: element_id manquant")
            
            if module == 'cm':
                errors.extend(self._validate_csv_cm(row, i+1))
            elif module == 'bois':
                errors.extend(self._validate_csv_bois(row, i+1))
            elif module == 'beton':
                errors.extend(self._validate_csv_beton(row, i+1))
            elif module == 'hydrodrain':
                errors.extend(self._validate_csv_hydro(row, i+1))
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'row_count': len(csv_data)
        }
    
    def _get_csv_template(self, module: str, command: str) -> str:
        """Génère un template CSV pour un module et une commande."""
        templates = {
            'cm': {
                'check-poteau': 'element_id,type,section,longueur,charge_permanente,charge_exploitation,acier,statut\nP1,poteau,HEA200,3.5,15.2,25.8,S235,conforme',
                'check-deversement': 'element_id,type,section,longueur,charge_permanente,charge_exploitation,acier,statut\nP1,poutre,IPE300,6.0,18.5,30.2,S235,conforme',
                'check-tendu': 'element_id,type,section,longueur,effort_traction,acier,statut\nT1,tirant,HEA100,4.0,150.5,S235,conforme',
                'check-compose': 'element_id,type,section,longueur,effort_normal,moment_flexion,acier,statut\nC1,poteau,HEA240,4.2,200.0,45.8,S235,conforme',
                'check-fleche': 'element_id,type,section,longueur,charge_totale,flèche_max,acier,statut\nF1,poutre,IPE400,8.0,35.2,25.0,S235,conforme',
                'check-assemblage-boulon': 'element_id,type,nombre_boulons,diametre_boulon,effort_cisaillement,acier,statut\nA1,assemblage,8,M20,85.5,S235,conforme',
                'check-assemblage-soude': 'element_id,type,longueur_soudure,epaisseur_soudure,effort_traction,acier,statut\nA1,assemblage,200.0,8.0,120.5,S235,conforme',
                'optimize-section': 'element_id,type,charge_totale,longueur,acier,section_optimale,statut\nO1,poutre,45.2,6.0,S235,IPE360,conforme'
            },
            'bois': {
                'check-poteau': 'element_id,type,section,longueur,essence,classe,charge_permanente,charge_exploitation,statut\nP1,poteau,100x100,3.0,epicea,C24,8.5,12.3,conforme',
                'check-deversement': 'element_id,type,section,longueur,essence,classe,charge_totale,statut\nP1,poutre,200x400,6.0,chene,D30,25.2,conforme',
                'check-cisaillement': 'element_id,type,section,longueur,essence,classe,effort_cisaillement,statut\nC1,poutre,150x300,4.5,epicea,C24,18.5,conforme',
                'check-compression-perp': 'element_id,type,section,longueur,essence,classe,effort_compression,statut\nCP1,appui,200x200,0.1,chene,D30,45.2,conforme',
                'check-compose': 'element_id,type,section,longueur,essence,classe,effort_normal,moment_flexion,statut\nC1,poteau,150x150,3.5,epicea,C24,85.5,12.8,conforme',
                'check-fleche': 'element_id,type,section,longueur,essence,classe,charge_totale,flèche_max,statut\nF1,poutre,200x400,6.0,chene,D30,35.2,25.0,conforme',
                'check-assemblage-pointe': 'element_id,type,nombre_pointes,diametre_pointe,effort_cisaillement,essence,statut\nA1,assemblage,12,4.0,25.5,epicea,conforme',
                'check-assemblage-embrevement': 'element_id,type,longueur_embrevement,largeur_embrevement,effort_traction,essence,statut\nA1,assemblage,80.0,40.0,45.2,chene,conforme'
            },
            'beton': {
                'calc-poteau': 'element_id,type,section,hauteur,beton,acier,charge_permanente,charge_exploitation,statut\nP1,poteau,30x30,3.0,C25,HA500,45.2,68.5,conforme',
                'calc-radier': 'element_id,type,epaisseur,largeur,longueur,beton,acier,charge_totale,statut\nR1,radier,0.25,10.0,15.0,C25,HA500,120.5,conforme'
            },
            'hydrodrain': {
                'ouvrage-canal': 'element_id,type,largeur,hauteur,debit,matiere,statut\nC1,canal,2.5,1.8,5.0,beton,conforme',
                'reservoir-equilibrage': 'element_id,type,volume,hauteur,diametre,matiere,statut\nR1,reservoir,1000,8.0,12.0,beton,conforme',
                'collector-dimensionner-troncons': 'element_id,type,diametre,longueur,debit,pente,matiere,statut\nT1,troncon,300,150,25.5,0.02,PVC,conforme',
                'plomberie-dimensionner': 'element_id,type,diametre,longueur,debit,type_fluide,matiere,statut\nP1,tuyau,50,25,2.5,eau,PVC,conforme'
            }
        }
        
        if module in templates and command in templates[module]:
            return templates[module][command]
        else:
            return f"Template non disponible pour {module}/{command}"
    
    # Méthodes de conversion spécifiques par module
    def _yaml_to_csv_cm(self, yaml_data: Any) -> List[Dict[str, Any]]:
        """Conversion YAML → CSV pour Construction Métallique."""
        if isinstance(yaml_data, list):
            return [self._yaml_to_csv_cm_single(item) for item in yaml_data]
        else:
            return [self._yaml_to_csv_cm_single(yaml_data)]
    
    def _yaml_to_csv_cm_single(self, yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conversion YAML → CSV pour un élément CM."""
        return {
            'element_id': yaml_data.get('element_id', ''),
            'type': yaml_data.get('type', ''),
            'section': yaml_data.get('section', ''),
            'longueur': str(yaml_data.get('longueur', '')),
            'charge_permanente': str(yaml_data.get('charge_permanente', '')),
            'charge_exploitation': str(yaml_data.get('charge_exploitation', '')),
            'acier': yaml_data.get('acier', ''),
            'statut': yaml_data.get('statut', '')
        }
    
    def _csv_to_yaml_cm(self, csv_data: List[Dict[str, Any]]) -> Any:
        """Conversion CSV → YAML pour Construction Métallique."""
        if len(csv_data) == 1:
            return self._csv_to_yaml_cm_single(csv_data[0])
        else:
            return [self._csv_to_yaml_cm_single(row) for row in csv_data]
    
    def _csv_to_yaml_cm_single(self, csv_row: Dict[str, Any]) -> Dict[str, Any]:
        """Conversion CSV → YAML pour un élément CM."""
        return {
            'element_id': csv_row.get('element_id', ''),
            'type': csv_row.get('type', ''),
            'section': csv_row.get('section', ''),
            'longueur': float(csv_row.get('longueur', 0)),
            'charge_permanente': float(csv_row.get('charge_permanente', 0)),
            'charge_exploitation': float(csv_row.get('charge_exploitation', 0)),
            'acier': csv_row.get('acier', ''),
            'statut': csv_row.get('statut', '')
        }
    
    def _validate_csv_cm(self, row: Dict[str, Any], line_num: int) -> List[str]:
        """Validation CSV pour Construction Métallique."""
        errors = []
        if not row.get('section'):
            errors.append(f"Ligne {line_num}: section manquante")
        if not row.get('acier'):
            errors.append(f"Ligne {line_num}: acier manquant")
        return errors
    
    # Méthodes similaires pour bois, beton, hydrodrain
    def _yaml_to_csv_bois(self, yaml_data: Any) -> List[Dict[str, Any]]:
        if isinstance(yaml_data, list):
            return [self._yaml_to_csv_bois_single(item) for item in yaml_data]
        else:
            return [self._yaml_to_csv_bois_single(yaml_data)]
    
    def _yaml_to_csv_bois_single(self, yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'element_id': yaml_data.get('element_id', ''),
            'type': yaml_data.get('type', ''),
            'section': yaml_data.get('section', ''),
            'longueur': str(yaml_data.get('longueur', '')),
            'essence': yaml_data.get('essence', ''),
            'classe': yaml_data.get('classe', ''),
            'charge_permanente': str(yaml_data.get('charge_permanente', '')),
            'charge_exploitation': str(yaml_data.get('charge_exploitation', '')),
            'statut': yaml_data.get('statut', '')
        }
    
    def _csv_to_yaml_bois(self, csv_data: List[Dict[str, Any]]) -> Any:
        if len(csv_data) == 1:
            return self._csv_to_yaml_bois_single(csv_data[0])
        else:
            return [self._csv_to_yaml_bois_single(row) for row in csv_data]
    
    def _csv_to_yaml_bois_single(self, csv_row: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'element_id': csv_row.get('element_id', ''),
            'type': csv_row.get('type', ''),
            'section': csv_row.get('section', ''),
            'longueur': float(csv_row.get('longueur', 0)),
            'essence': csv_row.get('essence', ''),
            'classe': csv_row.get('classe', ''),
            'charge_permanente': float(csv_row.get('charge_permanente', 0)),
            'charge_exploitation': float(csv_row.get('charge_exploitation', 0)),
            'statut': csv_row.get('statut', '')
        }
    
    def _validate_csv_bois(self, row: Dict[str, Any], line_num: int) -> List[str]:
        errors = []
        if not row.get('essence'):
            errors.append(f"Ligne {line_num}: essence manquante")
        if not row.get('classe'):
            errors.append(f"Ligne {line_num}: classe manquante")
        return errors
    
    def _yaml_to_csv_beton(self, yaml_data: Any) -> List[Dict[str, Any]]:
        if isinstance(yaml_data, list):
            return [self._yaml_to_csv_beton_single(item) for item in yaml_data]
        else:
            return [self._yaml_to_csv_beton_single(yaml_data)]
    
    def _yaml_to_csv_beton_single(self, yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'element_id': yaml_data.get('element_id', ''),
            'type': yaml_data.get('type', ''),
            'section': yaml_data.get('section', ''),
            'hauteur': str(yaml_data.get('hauteur', '')),
            'beton': yaml_data.get('beton', ''),
            'acier': yaml_data.get('acier', ''),
            'charge_permanente': str(yaml_data.get('charge_permanente', '')),
            'charge_exploitation': str(yaml_data.get('charge_exploitation', '')),
            'statut': yaml_data.get('statut', '')
        }
    
    def _csv_to_yaml_beton(self, csv_data: List[Dict[str, Any]]) -> Any:
        if len(csv_data) == 1:
            return self._csv_to_yaml_beton_single(csv_data[0])
        else:
            return [self._csv_to_yaml_beton_single(row) for row in csv_data]
    
    def _csv_to_yaml_beton_single(self, csv_row: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'element_id': csv_row.get('element_id', ''),
            'type': csv_row.get('type', ''),
            'section': csv_row.get('section', ''),
            'hauteur': float(csv_row.get('hauteur', 0)),
            'beton': csv_row.get('beton', ''),
            'acier': csv_row.get('acier', ''),
            'charge_permanente': float(csv_row.get('charge_permanente', 0)),
            'charge_exploitation': float(csv_row.get('charge_exploitation', 0)),
            'statut': csv_row.get('statut', '')
        }
    
    def _validate_csv_beton(self, row: Dict[str, Any], line_num: int) -> List[str]:
        errors = []
        if not row.get('beton'):
            errors.append(f"Ligne {line_num}: beton manquant")
        if not row.get('acier'):
            errors.append(f"Ligne {line_num}: acier manquant")
        return errors
    
    def _yaml_to_csv_hydro(self, yaml_data: Any) -> List[Dict[str, Any]]:
        if isinstance(yaml_data, list):
            return [self._yaml_to_csv_hydro_single(item) for item in yaml_data]
        else:
            return [self._yaml_to_csv_hydro_single(yaml_data)]
    
    def _yaml_to_csv_hydro_single(self, yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'element_id': yaml_data.get('element_id', ''),
            'type': yaml_data.get('type', ''),
            'largeur': str(yaml_data.get('largeur', '')),
            'hauteur': str(yaml_data.get('hauteur', '')),
            'debit': str(yaml_data.get('debit', '')),
            'matiere': yaml_data.get('matiere', ''),
            'statut': yaml_data.get('statut', '')
        }
    
    def _csv_to_yaml_hydro(self, csv_data: List[Dict[str, Any]]) -> Any:
        if len(csv_data) == 1:
            return self._csv_to_yaml_hydro_single(csv_data[0])
        else:
            return [self._csv_to_yaml_hydro_single(row) for row in csv_data]
    
    def _csv_to_yaml_hydro_single(self, csv_row: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'element_id': csv_row.get('element_id', ''),
            'type': csv_row.get('type', ''),
            'largeur': float(csv_row.get('largeur', 0)),
            'hauteur': float(csv_row.get('hauteur', 0)),
            'debit': float(csv_row.get('debit', 0)),
            'matiere': csv_row.get('matiere', ''),
            'statut': csv_row.get('statut', '')
        }
    
    def _validate_csv_hydro(self, row: Dict[str, Any], line_num: int) -> List[str]:
        errors = []
        if not row.get('debit'):
            errors.append(f"Ligne {line_num}: debit manquant")
        if not row.get('matiere'):
            errors.append(f"Ligne {line_num}: matiere manquante")
        return errors
    
    def _cmd_aep(self, args):
        """Commandes AEP (Alimentation en Eau Potable)."""
        if not args:
            console.print("[red]Usage: aep <command> [args...][/red]")
            console.print("[yellow]Commandes disponibles:[/yellow]")
            console.print("  population <file> - Projection démographique")
            console.print("  demand <file>     - Calcul de demande en eau")
            console.print("  network <file>    - Dimensionnement réseau")
            console.print("  reservoir <file>  - Dimensionnement réservoir")
            console.print("  pumping <file>    - Dimensionnement pompage")
            console.print("  hardy-cross <file> - Méthode Hardy-Cross")
            console.print("  workflow <file>   - Workflow AEP complet")
            return
        
        command = args[0]
        cmd_args = args[1:]
        
        try:
            # Construire la commande LCPI AEP
            lcpi_cmd = ["python", "-m", "src.lcpi.aep.cli", command] + cmd_args
            
            # Exécuter la commande
            result = subprocess.run(lcpi_cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                console.print(f"[green]✓[/green] Commande AEP {command} réussie")
                if result.stdout:
                    console.print(Panel(result.stdout, title="Résultat AEP", border_style="green"))
            else:
                console.print(f"[red]✗[/red] Erreur dans la commande AEP {command}")
                if result.stderr:
                    console.print(Panel(result.stderr, title="Erreur AEP", border_style="red"))
                    
        except Exception as e:
            console.print(f"[red]Erreur lors de l'exécution AEP: {e}[/red]")
    
    def _cmd_calc(self, args):
        """Exécute un calcul."""
        if len(args) < 2:
            console.print("[red]Usage: calc <module> <command> [args...][/red]")
            return
        
        module = args[0]
        command = args[1]
        cmd_args = args[2:]
        
        try:
            # Construire la commande LCPI
            lcpi_cmd = ["lcpi", module, command] + cmd_args
            
            # Exécuter la commande
            result = subprocess.run(lcpi_cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                console.print(f"[green]✓[/green] Calcul {module} {command} réussi")
                if result.stdout:
                    console.print(Panel(result.stdout, title="Résultat", border_style="green"))
            else:
                console.print(f"[red]✗[/red] Erreur dans le calcul {module} {command}")
                if result.stderr:
                    console.print(Panel(result.stderr, title="Erreur", border_style="red"))
                    
        except Exception as e:
            console.print(f"[red]Erreur lors de l'exécution: {e}[/red]")
    
    def _cmd_report(self, args):
        """Commandes de rapport."""
        if not args:
            console.print("[red]Usage: report <generate|compare> [args...][/red]")
            return
        
        subcmd = args[0]
        if subcmd == 'generate':
            self._report_generate(args[1:])
        elif subcmd == 'compare':
            self._report_compare(args[1:])
        else:
            console.print(f"[red]Sous-commande rapport inconnue: {subcmd}[/red]")
    
    def _report_generate(self, args):
        """Génère un rapport."""
        try:
            # Construire la commande LCPI report
            lcpi_cmd = ["lcpi", "report", "generate"] + args
            
            # Exécuter la commande
            result = subprocess.run(lcpi_cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                console.print(f"[green]✓[/green] Rapport généré avec succès")
                if result.stdout:
                    console.print(Panel(result.stdout, title="Rapport", border_style="green"))
            else:
                console.print(f"[red]✗[/red] Erreur lors de la génération du rapport")
                if result.stderr:
                    console.print(Panel(result.stderr, title="Erreur", border_style="red"))
                    
        except Exception as e:
            console.print(f"[red]Erreur lors de la génération: {e}[/red]")
    
    def _report_compare(self, args):
        """Compare des versions."""
        if len(args) < 2:
            console.print("[red]Usage: report compare <version1> <version2>[/red]")
            return
        
        v1, v2 = args[0], args[1]
        
        try:
            # Construire la commande LCPI report compare
            lcpi_cmd = ["lcpi", "report", "compare", v1, v2]
            
            # Exécuter la commande
            result = subprocess.run(lcpi_cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                console.print(f"[green]✓[/green] Comparaison {v1} vs {v2} réussie")
                if result.stdout:
                    console.print(Panel(result.stdout, title="Comparaison", border_style="green"))
            else:
                console.print(f"[red]✗[/red] Erreur lors de la comparaison")
                if result.stderr:
                    console.print(Panel(result.stderr, title="Erreur", border_style="red"))
                    
        except Exception as e:
            console.print(f"[red]Erreur lors de la comparaison: {e}[/red]")

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
