#!/usr/bin/env python3
"""
Module d'Amélioration UX pour LCPI-CLI
Améliore l'expérience utilisateur avec des messages contextuels et des guides interactifs
"""

import os
import sys
import json
import pathlib
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.columns import Columns
from rich.markdown import Markdown
from rich.syntax import Syntax

console = Console()

class UXEnhancer:
    def __init__(self):
        self.project_root = pathlib.Path(__file__).parent.parent.parent
        self.config_file = pathlib.Path.home() / ".lcpi" / "ux_config.json"
        self.load_user_preferences()
    
    def load_user_preferences(self):
        """Charge les préférences utilisateur"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.preferences = json.load(f)
            except:
                self.preferences = self.get_default_preferences()
        else:
            self.preferences = self.get_default_preferences()
            self.save_user_preferences()
    
    def get_default_preferences(self):
        """Retourne les préférences par défaut"""
        return {
            "show_welcome": True,
            "show_tips": True,
            "show_examples": True,
            "interactive_mode": False,
            "expert_mode": False,
            "last_used": datetime.now().isoformat()
        }
    
    def save_user_preferences(self):
        """Sauvegarde les préférences utilisateur"""
        self.config_file.parent.mkdir(exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.preferences, f, indent=4, ensure_ascii=False)
    
    def show_welcome_message(self):
        """Affiche un message de bienvenue personnalisé"""
        if not self.preferences.get("show_welcome", True):
            return
        
        welcome_text = f"""
[bold blue]🎉 Bienvenue dans LCPI-CLI ![/bold blue]

[bold]Plateforme de Calcul Polyvalent pour l'Ingénierie[/bold]

[dim]Version 2.1.0 - Dernière utilisation: {self.preferences.get('last_used', 'Première utilisation')}[/dim]

[bold]Commandes rapides:[/bold]
• [cyan]lcpi --help[/cyan] - Afficher l'aide générale
• [cyan]lcpi doctor[/cyan] - Vérifier l'installation
• [cyan]lcpi shell[/cyan] - Mode interactif
• [cyan]lcpi plugins list[/cyan] - Voir les plugins disponibles

[dim]💡 Conseil: Utilisez 'lcpi tips' pour des astuces quotidiennes[/dim]
        """
        
        console.print(Panel(welcome_text, title="🚀 LCPI-CLI", border_style="blue"))
    
    def show_contextual_help(self, command=None, subcommand=None):
        """Affiche une aide contextuelle selon la commande"""
        help_content = self.get_contextual_help(command, subcommand)
        if help_content:
            console.print(Panel(help_content, title="📖 Aide Contextuelle", border_style="green"))
    
    def get_contextual_help(self, command, subcommand):
        """Retourne l'aide contextuelle selon la commande"""
        help_content = {
            "init": """
[bold]Initialisation de Projet[/bold]

Cette commande crée un nouveau projet LCPI avec la structure recommandée.

[bold]Exemples:[/bold]
• [cyan]lcpi init mon_projet[/cyan] - Projet basique
• [cyan]lcpi init hangar --template hangar-mixte[/cyan] - Avec template

[bold]Structure créée:[/bold]
```
mon_projet/
├── data/          # Données d'entrée
├── elements/      # Fichiers YAML
├── output/        # Résultats
└── docs/          # Documentation
```
            """,
            
            "plugins": """
[bold]Gestion des Plugins[/bold]

Les plugins étendent les fonctionnalités de LCPI-CLI.

[bold]Commandes:[/bold]
• [cyan]lcpi plugins list[/cyan] - Voir tous les plugins
• [cyan]lcpi plugins install beton[/cyan] - Activer un plugin
• [cyan]lcpi plugins uninstall hydro[/cyan] - Désactiver un plugin

[bold]Plugins disponibles:[/bold]
• [cyan]beton[/cyan] - Béton armé (BAEL 91 / Eurocode 2)
• [cyan]bois[/cyan] - Structures en bois (Eurocode 5)
• [cyan]cm[/cyan] - Construction métallique
• [cyan]hydro[/cyan] - Hydrologie et hydraulique
            """,
            
            "doctor": """
[bold]Diagnostic Système[/bold]

Cette commande vérifie l'installation et la configuration.

[bold]Vérifications:[/bold]
• ✅ Dépendances Python
• ✅ Outils externes (pandoc, pdflatex)
• ✅ Plugins et compatibilité
• ✅ Configuration système

[bold]En cas de problème:[/bold]
1. Vérifiez les messages d'erreur
2. Consultez la documentation
3. Contactez le support
            """,
            
            "shell": """
[bold]Shell Interactif[/bold]

Mode interactif pour une utilisation plus fluide.

[bold]Avantages:[/bold]
• Pas besoin de retaper 'lcpi' à chaque fois
• Historique des commandes
• Auto-complétion
• Variables persistantes

[bold]Commandes internes:[/bold]
• [cyan]help[/cyan] - Afficher l'aide
• [cyan]clear[/cyan] - Effacer l'écran
• [cyan]history[/cyan] - Voir l'historique
• [cyan]exit[/cyan] - Quitter le shell
            """
        }
        
        if command in help_content:
            return help_content[command]
        elif command and subcommand:
            return help_content.get(f"{command}_{subcommand}", "")
        else:
            return None
    
    def show_tips(self):
        """Affiche des astuces utiles"""
        if not self.preferences.get("show_tips", True):
            return
        
        tips = [
            "💡 Utilisez 'lcpi shell' pour une expérience plus fluide",
            "💡 Consultez 'lcpi doctor' si vous rencontrez des problèmes",
            "💡 Activez les plugins selon vos besoins avec 'lcpi plugins install'",
            "💡 Utilisez '--json' pour obtenir des résultats structurés",
            "💡 Consultez la documentation dans docs/ pour des exemples détaillés",
            "💡 Sauvegardez vos projets dans des dossiers organisés",
            "💡 Utilisez des templates pour démarrer rapidement",
            "💡 Vérifiez votre licence avec 'lcpi doctor'"
        ]
        
        import random
        tip = random.choice(tips)
        console.print(Panel(tip, title="💡 Astuce du Jour", border_style="yellow"))
    
    def show_examples(self, command=None):
        """Affiche des exemples d'utilisation"""
        if not self.preferences.get("show_examples", True):
            return
        
        examples = {
            "beton": """
[bold]Exemples Béton Armé:[/bold]

[cyan]Calcul de poteau:[/cyan]
lcpi beton calc-poteau poteaux.yml

[cyan]Calcul de radier:[/cyan]
lcpi beton calc-radier radier.yml

[cyan]Mode interactif:[/cyan]
lcpi beton interactive
            """,
            
            "hydro": """
[bold]Exemples Hydrologie:[/bold]

[cyan]Dimensionnement de canal:[/cyan]
lcpi hydro ouvrage canal canal.yml

[cyan]Analyse pluviométrique:[/cyan]
lcpi hydro pluvio analyser pluies.csv

[cyan]Réseau d'assainissement:[/cyan]
lcpi hydro collector eaux-usees reseau.json
            """,
            
            "general": """
[bold]Exemples Généraux:[/bold]

[cyan]Initialiser un projet:[/cyan]
lcpi init mon_projet_ingenierie

[cyan]Générer un rapport:[/cyan]
lcpi report --format pdf

[cyan]Vérifier l'installation:[/cyan]
lcpi doctor

[cyan]Shell interactif:[/cyan]
lcpi shell
            """
        }
        
        if command and command in examples:
            console.print(Panel(examples[command], title="📚 Exemples d'Utilisation", border_style="cyan"))
        else:
            console.print(Panel(examples["general"], title="📚 Exemples d'Utilisation", border_style="cyan"))
    
    def show_error_help(self, error_type, error_message):
        """Affiche une aide contextuelle pour les erreurs"""
        error_help = {
            "ModuleNotFoundError": """
[bold red]Erreur: Module non trouvé[/bold red]

[bold]Solutions possibles:[/bold]
1. [cyan]Vérifiez l'installation:[/cyan] lcpi doctor
2. [cyan]Installez les dépendances:[/cyan] pip install -r requirements.txt
3. [cyan]Activez le plugin:[/cyan] lcpi plugins install <nom_plugin>
4. [cyan]Vérifiez le PYTHONPATH[/cyan]

[bold]Commande de diagnostic:[/bold]
lcpi doctor
            """,
            
            "FileNotFoundError": """
[bold red]Erreur: Fichier non trouvé[/bold red]

[bold]Solutions possibles:[/bold]
1. [cyan]Vérifiez le chemin du fichier[/cyan]
2. [cyan]Utilisez un chemin absolu[/cyan]
3. [cyan]Créez le fichier manquant[/cyan]
4. [cyan]Utilisez un template:[/cyan] lcpi init --template

[bold]Exemple de structure:[/bold]
```
projet/
├── data/          # Données CSV, JSON
├── elements/      # Fichiers YAML
└── output/        # Résultats
```
            """,
            
            "PermissionError": """
[bold red]Erreur: Permission refusée[/bold red]

[bold]Solutions possibles:[/bold]
1. [cyan]Vérifiez les permissions du dossier[/cyan]
2. [cyan]Exécutez en tant qu'administrateur[/cyan]
3. [cyan]Changez le dossier de sortie[/cyan]
4. [cyan]Vérifiez l'espace disque[/cyan]

[bold]Commande de diagnostic:[/bold]
lcpi doctor
            """,
            
            "LicenseError": """
[bold red]Erreur: Problème de licence[/bold red]

[bold]Solutions possibles:[/bold]
1. [cyan]Vérifiez votre licence:[/cyan] ~/.lcpi/license.key
2. [cyan]Contactez le support[/cyan]
3. [cyan]Utilisez le mode démonstration[/cyan]
4. [cyan]Renouvelez votre licence[/cyan]

[bold]Support:[/bold]
Email: support@lcpi-cli.com
Téléphone: +33 1 23 45 67 89
            """
        }
        
        # Détecter le type d'erreur
        error_key = "general"
        for key in error_help.keys():
            if key in str(error_message):
                error_key = key
                break
        
        if error_key in error_help:
            console.print(Panel(error_help[error_key], title="🛠️ Aide pour l'Erreur", border_style="red"))
    
    def show_interactive_guide(self, topic=None):
        """Affiche un guide interactif"""
        guides = {
            "installation": self.guide_installation,
            "plugins": self.guide_plugins,
            "first_project": self.guide_first_project,
            "troubleshooting": self.guide_troubleshooting
        }
        
        if topic and topic in guides:
            guides[topic]()
        else:
            self.show_guide_menu()
    
    def show_guide_menu(self):
        """Affiche le menu des guides"""
        console.print("\n[bold]📖 Guides Interactifs[/bold]")
        
        guides = [
            ("1", "installation", "Guide d'installation"),
            ("2", "plugins", "Gestion des plugins"),
            ("3", "first_project", "Premier projet"),
            ("4", "troubleshooting", "Dépannage")
        ]
        
        for num, key, title in guides:
            console.print(f"{num}. {title}")
        
        choice = Prompt.ask("Choisissez un guide", choices=["1", "2", "3", "4"])
        topic = guides[int(choice) - 1][1]
        self.show_interactive_guide(topic)
    
    def guide_installation(self):
        """Guide d'installation interactif"""
        console.print(Panel("""
[bold]🔧 Guide d'Installation[/bold]

Ce guide vous accompagne dans l'installation de LCPI-CLI.

[bold]Étapes:[/bold]
1. ✅ Vérification des prérequis
2. 📦 Installation des dépendances
3. 🔧 Configuration du système
4. 🔌 Activation des plugins
5. ✅ Test de l'installation

[bold]Voulez-vous continuer ?[/bold]
        """, title="📖 Guide d'Installation", border_style="blue"))
        
        if Confirm.ask("Lancer l'assistant d'installation ?"):
            # Importer et lancer l'assistant
            try:
                from scripts.install_wizard import LCPIInstallWizard
                wizard = LCPIInstallWizard()
                wizard.run()
            except ImportError:
                console.print("[red]Assistant d'installation non disponible[/red]")
    
    def guide_plugins(self):
        """Guide de gestion des plugins"""
        console.print(Panel("""
[bold]🔌 Guide des Plugins[/bold]

Les plugins étendent les fonctionnalités de LCPI-CLI.

[bold]Plugins disponibles:[/bold]
• [cyan]beton[/cyan] - Béton armé (BAEL 91 / Eurocode 2)
• [cyan]bois[/cyan] - Structures en bois (Eurocode 5)
• [cyan]cm[/cyan] - Construction métallique
• [cyan]hydro[/cyan] - Hydrologie et hydraulique

[bold]Commandes utiles:[/bold]
• [cyan]lcpi plugins list[/cyan] - Voir les plugins
• [cyan]lcpi plugins install <nom>[/cyan] - Activer un plugin
• [cyan]lcpi plugins uninstall <nom>[/cyan] - Désactiver un plugin
        """, title="📖 Guide des Plugins", border_style="cyan"))
    
    def guide_first_project(self):
        """Guide du premier projet"""
        console.print(Panel("""
[bold]🚀 Guide du Premier Projet[/bold]

Créons ensemble votre premier projet LCPI-CLI.

[bold]Étapes:[/bold]
1. [cyan]Initialiser le projet:[/cyan] lcpi init mon_projet
2. [cyan]Activer les plugins:[/cyan] lcpi plugins install beton
3. [cyan]Créer les données:[/cyan] Éditer les fichiers YAML
4. [cyan]Lancer les calculs:[/cyan] lcpi beton calc-poteau
5. [cyan]Générer un rapport:[/cyan] lcpi report

[bold]Structure recommandée:[/bold]
```
mon_projet/
├── data/          # Données d'entrée
├── elements/      # Fichiers YAML
├── output/        # Résultats
└── docs/          # Documentation
```
        """, title="📖 Guide du Premier Projet", border_style="green"))
    
    def guide_troubleshooting(self):
        """Guide de dépannage"""
        console.print(Panel("""
[bold]🛠️ Guide de Dépannage[/bold]

Solutions aux problèmes courants.

[bold]Problèmes courants:[/bold]

[bold]1. Commande 'lcpi' non reconnue[/bold]
• Vérifiez l'installation: lcpi doctor
• Réinstallez: pip install -e .

[bold]2. Plugin non trouvé[/bold]
• Activez le plugin: lcpi plugins install <nom>
• Vérifiez la liste: lcpi plugins list

[bold]3. Erreur de licence[/bold]
• Vérifiez le fichier: ~/.lcpi/license.key
• Contactez le support

[bold]4. Erreur de dépendance[/bold]
• Installez: pip install -r requirements.txt
• Vérifiez: lcpi doctor

[bold]Commande de diagnostic:[/bold]
lcpi doctor
        """, title="📖 Guide de Dépannage", border_style="red"))
    
    def update_last_used(self):
        """Met à jour la date de dernière utilisation"""
        self.preferences["last_used"] = datetime.now().isoformat()
        self.save_user_preferences()

# Instance globale
ux_enhancer = UXEnhancer()

def show_welcome():
    """Affiche le message de bienvenue"""
    ux_enhancer.show_welcome_message()
    ux_enhancer.update_last_used()

def show_contextual_help(command=None, subcommand=None):
    """Affiche l'aide contextuelle"""
    ux_enhancer.show_contextual_help(command, subcommand)

def show_tips():
    """Affiche des astuces"""
    ux_enhancer.show_tips()

def show_examples(command=None):
    """Affiche des exemples"""
    ux_enhancer.show_examples(command)

def show_error_help(error_type, error_message):
    """Affiche l'aide pour les erreurs"""
    ux_enhancer.show_error_help(error_type, error_message)

def show_interactive_guide(topic=None):
    """Affiche un guide interactif"""
    ux_enhancer.show_interactive_guide(topic) 