#!/usr/bin/env python3
"""
Assistant d'Installation LCPI-CLI - Interface Utilisateur Améliorée
Guide interactif pour l'installation et la configuration initiale
"""

import os
import sys
import subprocess
import json
import pathlib
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.layout import Layout
from rich.text import Text
from rich.align import Align

console = Console()

class LCPIInstallWizard:
    def __init__(self):
        self.project_root = pathlib.Path(__file__).parent.parent
        self.installation_log = []
        
    def print_welcome(self):
        """Affiche l'écran de bienvenue"""
        welcome_text = """
[bold blue]LCPI-CLI - Assistant d'Installation[/bold blue]

[bold]Plateforme de Calcul Polyvalent pour l'Ingénierie[/bold]

Ce guide vous accompagnera dans l'installation et la configuration 
de LCPI-CLI sur votre système.

[dim]Version 2.0.0 - Support: Windows, macOS, Linux[/dim]
        """
        
        console.print(Panel(welcome_text, title="🎉 Bienvenue", border_style="blue"))
        
    def check_system_requirements(self):
        """Vérifie les prérequis système"""
        console.print("\n[bold]🔍 Vérification des Prérequis Système[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Vérifier Python
            task = progress.add_task("Vérification de Python...", total=None)
            try:
                python_version = subprocess.check_output([sys.executable, "--version"], 
                                                      text=True, stderr=subprocess.STDOUT)
                progress.update(task, description=f"✅ Python détecté: {python_version.strip()}")
            except:
                progress.update(task, description="❌ Python non trouvé")
                console.print("[red]ERREUR: Python 3.8+ est requis[/red]")
                return False
            
            # Vérifier pip
            task = progress.add_task("Vérification de pip...", total=None)
            try:
                pip_version = subprocess.check_output([sys.executable, "-m", "pip", "--version"], 
                                                   text=True, stderr=subprocess.STDOUT)
                progress.update(task, description=f"✅ pip détecté: {pip_version.strip()}")
            except:
                progress.update(task, description="❌ pip non trouvé")
                console.print("[red]ERREUR: pip est requis[/red]")
                return False
            
            # Vérifier l'espace disque
            task = progress.add_task("Vérification de l'espace disque...", total=None)
            try:
                import shutil
                total, used, free = shutil.disk_usage(self.project_root)
                free_gb = free // (1024**3)
                if free_gb > 1:
                    progress.update(task, description=f"✅ Espace disponible: {free_gb} GB")
                else:
                    progress.update(task, description="❌ Espace insuffisant")
                    console.print("[red]ERREUR: Au moins 1 GB d'espace libre requis[/red]")
                    return False
            except:
                progress.update(task, description="⚠️ Impossible de vérifier l'espace")
        
        return True
    
    def check_network_connection(self):
        """Vérifie la connexion réseau"""
        console.print("\n[bold]🌐 Vérification de la Connexion Réseau[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Test de connexion...", total=None)
            try:
                import urllib.request
                urllib.request.urlopen('http://www.google.com', timeout=5)
                progress.update(task, description="✅ Connexion Internet disponible")
                return True
            except:
                progress.update(task, description="⚠️ Pas de connexion Internet")
                return False
    
    def select_installation_mode(self):
        """Permet à l'utilisateur de choisir le mode d'installation"""
        console.print("\n[bold]⚙️ Mode d'Installation[/bold]")
        
        online_available = self.check_network_connection()
        
        if online_available:
            console.print("""
[green]✅ Connexion Internet détectée[/green]

Options disponibles:
1. [bold]Installation complète[/bold] - Télécharge toutes les dépendances
2. [bold]Installation minimale[/bold] - Installe seulement les composants essentiels
3. [bold]Installation hors ligne[/bold] - Utilise les paquets locaux
            """)
            
            choice = Prompt.ask(
                "Choisissez le mode d'installation",
                choices=["1", "2", "3"],
                default="1"
            )
            
            return {
                "1": "online_full",
                "2": "online_minimal", 
                "3": "offline"
            }[choice]
        else:
            console.print("""
[yellow]⚠️ Pas de connexion Internet détectée[/yellow]

Installation en mode hors ligne avec les paquets locaux.
            """)
            return "offline"
    
    def configure_plugins(self):
        """Configure les plugins selon les besoins de l'utilisateur"""
        console.print("\n[bold]🔌 Configuration des Plugins[/bold]")
        
        console.print("""
LCPI-CLI propose plusieurs plugins spécialisés:

[bold]Plugins de Base (Recommandés):[/bold]
• [cyan]shell[/cyan] - Interface interactive
• [cyan]utils[/cyan] - Utilitaires généraux

[bold]Plugins Métier:[/bold]
• [cyan]beton[/cyan] - Béton armé (BAEL 91 / Eurocode 2)
• [cyan]bois[/cyan] - Structures en bois (Eurocode 5)
• [cyan]cm[/cyan] - Construction métallique
• [cyan]hydro[/cyan] - Hydrologie et hydraulique
        """)
        
        # Plugins de base (toujours activés)
        base_plugins = ["shell", "utils"]
        
        # Sélection des plugins métier
        available_business_plugins = ["beton", "bois", "cm", "hydro"]
        selected_business_plugins = []
        
        for plugin in available_business_plugins:
            if Confirm.ask(f"Installer le plugin [cyan]{plugin}[/cyan] ?"):
                selected_business_plugins.append(plugin)
        
        all_plugins = base_plugins + selected_business_plugins
        
        console.print(f"\n[green]✅ Plugins sélectionnés: {', '.join(all_plugins)}[/green]")
        
        return all_plugins
    
    def install_dependencies(self, mode):
        """Installe les dépendances selon le mode choisi"""
        console.print(f"\n[bold]📦 Installation des Dépendances ({mode})[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Installation en cours...", total=None)
            
            try:
                if mode == "offline":
                    # Installation hors ligne
                    command = [
                        sys.executable, "-m", "pip", "install", 
                        "--no-index", "--find-links=offline_packages", 
                        "-r", "requirements.txt"
                    ]
                else:
                    # Installation en ligne
                    command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
                
                result = subprocess.run(command, cwd=self.project_root, 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    progress.update(task, description="✅ Dépendances installées")
                    return True
                else:
                    progress.update(task, description="❌ Erreur d'installation")
                    console.print(f"[red]Erreur: {result.stderr}[/red]")
                    return False
                    
            except Exception as e:
                progress.update(task, description="❌ Erreur d'installation")
                console.print(f"[red]Erreur: {e}[/red]")
                return False
    
    def install_lcpi_core(self):
        """Installe le noyau LCPI-CLI"""
        console.print("\n[bold]🔧 Installation du Noyau LCPI-CLI[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Installation du noyau...", total=None)
            
            try:
                command = [sys.executable, "-m", "pip", "install", "-e", "."]
                result = subprocess.run(command, cwd=self.project_root, 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    progress.update(task, description="✅ Noyau installé")
                    return True
                else:
                    progress.update(task, description="❌ Erreur d'installation")
                    console.print(f"[red]Erreur: {result.stderr}[/red]")
                    return False
                    
            except Exception as e:
                progress.update(task, description="❌ Erreur d'installation")
                console.print(f"[red]Erreur: {e}[/red]")
                return False
    
    def setup_license_system(self):
        """Configure le système de licence"""
        console.print("\n[bold]🔐 Configuration du Système de Licence[/bold]")
        
        # Créer le dossier de licence
        license_dir = pathlib.Path.home() / ".lcpi"
        license_dir.mkdir(exist_ok=True)
        
        license_file = license_dir / "license.key"
        
        if license_file.exists():
            console.print("[green]✅ Fichier de licence existant détecté[/green]")
        else:
            # Créer un fichier avec des instructions
            with open(license_file, 'w', encoding='utf-8') as f:
                f.write("# LCPI-CLI License Key\n")
                f.write("# Remplacez ce contenu par votre clé de licence\n")
                f.write("# Contactez le support pour obtenir votre licence\n")
                f.write("# Email: support@lcpi-cli.com\n")
            
            console.print(f"[green]✅ Fichier de licence créé: {license_file}[/green]")
        
        return True
    
    def configure_plugins_file(self, selected_plugins):
        """Configure le fichier de plugins"""
        plugins_config_path = self.project_root / "src" / "lcpi" / ".plugins.json"
        
        config = {
            "active_plugins": selected_plugins,
            "available_plugins": ["shell", "utils", "beton", "bois", "cm", "hydro"],
            "installation_date": datetime.now().isoformat(),
            "version": "2.0.0"
        }
        
        # Créer le dossier si nécessaire
        plugins_config_path.parent.mkdir(exist_ok=True)
        
        # Écrire la configuration
        with open(plugins_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        console.print(f"[green]✅ Configuration des plugins sauvegardée[/green]")
        return True
    
    def verify_installation(self):
        """Vérifie que l'installation s'est bien passée"""
        console.print("\n[bold]🔍 Vérification de l'Installation[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Test de l'import
            task = progress.add_task("Test d'import...", total=None)
            try:
                import sys
                src_path = str(self.project_root / "src")
                sys.path.insert(0, src_path)
                
                from lcpi.main import app
                progress.update(task, description="✅ Import réussi")
            except Exception as e:
                progress.update(task, description="❌ Erreur d'import")
                console.print(f"[red]Erreur: {e}[/red]")
                return False
            
            # Test de la commande
            task = progress.add_task("Test de la commande...", total=None)
            try:
                result = subprocess.run([
                    sys.executable, "-c", 
                    "import sys; sys.path.insert(0, 'src'); from lcpi.main import app; print('OK')"
                ], cwd=self.project_root, capture_output=True, text=True)
                
                if result.returncode == 0:
                    progress.update(task, description="✅ Commande fonctionnelle")
                else:
                    progress.update(task, description="❌ Erreur de commande")
                    return False
            except Exception as e:
                progress.update(task, description="❌ Erreur de commande")
                console.print(f"[red]Erreur: {e}[/red]")
                return False
        
        return True
    
    def show_next_steps(self):
        """Affiche les prochaines étapes"""
        console.print("\n" + "="*60)
        console.print("[bold green]🎉 Installation Terminée avec Succès ![/bold green]")
        console.print("="*60)
        
        next_steps = """
[bold]📋 Prochaines Étapes :[/bold]

1. [bold]🚀 Tester LCPI :[/bold]
   lcpi --help

2. [bold]🔌 Vérifier les plugins :[/bold]
   lcpi plugins list

3. [bold]🛠️ Utiliser le shell interactif :[/bold]
   lcpi shell

4. [bold]📚 Consulter la documentation :[/bold]
   - docs/GUIDE_UTILISATION.md
   - docs/NOUVELLES_FONCTIONNALITES.md

5. [bold]🔐 Gestion de la licence :[/bold]
   - Vérifiez votre licence : ~/.lcpi/license.key
   - Contactez le support pour obtenir une licence

[dim]💡 Conseil : Utilisez 'lcpi doctor' pour vérifier l'installation[/dim]
        """
        
        console.print(Panel(next_steps, title="📖 Guide de Démarrage", border_style="green"))
    
    def run(self):
        """Lance l'assistant d'installation"""
        try:
            # Écran de bienvenue
            self.print_welcome()
            
            # Vérifications préliminaires
            if not self.check_system_requirements():
                console.print("[red]❌ Prérequis non satisfaits. Installation annulée.[/red]")
                return False
            
            # Sélection du mode d'installation
            mode = self.select_installation_mode()
            
            # Configuration des plugins
            selected_plugins = self.configure_plugins()
            
            # Installation des dépendances
            if not self.install_dependencies(mode):
                console.print("[red]❌ Échec de l'installation des dépendances.[/red]")
                return False
            
            # Installation du noyau
            if not self.install_lcpi_core():
                console.print("[red]❌ Échec de l'installation du noyau.[/red]")
                return False
            
            # Configuration du système de licence
            if not self.setup_license_system():
                console.print("[red]❌ Échec de la configuration de la licence.[/red]")
                return False
            
            # Configuration des plugins
            if not self.configure_plugins_file(selected_plugins):
                console.print("[red]❌ Échec de la configuration des plugins.[/red]")
                return False
            
            # Vérification finale
            if not self.verify_installation():
                console.print("[red]❌ Échec de la vérification.[/red]")
                return False
            
            # Affichage des prochaines étapes
            self.show_next_steps()
            
            return True
            
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️ Installation interrompue par l'utilisateur.[/yellow]")
            return False
        except Exception as e:
            console.print(f"\n[red]❌ Erreur inattendue: {e}[/red]")
            return False

def main():
    """Point d'entrée principal"""
    wizard = LCPIInstallWizard()
    success = wizard.run()
    
    if success:
        console.print("\n[green]✅ Installation terminée avec succès ![/green]")
    else:
        console.print("\n[red]❌ Installation échouée.[/red]")
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main() 