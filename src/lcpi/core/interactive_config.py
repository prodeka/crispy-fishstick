"""
Configuration interactive pour les projets LCPI.
"""

import typer
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import json
import yaml

from .project_manager import ProjectManager

console = Console()

class InteractiveConfigurator:
    """Configurateur interactif pour les projets LCPI."""
    
    def __init__(self, project_dir: Path):
        """
        Initialise le configurateur interactif.
        
        Args:
            project_dir: Chemin vers le dossier du projet
        """
        self.project_dir = Path(project_dir)
        self.project_manager = ProjectManager(project_dir)
    
    def configure_project(self) -> None:
        """Configure le projet de manière interactive."""
        console.print(Panel("🎨 Configuration Interactive du Projet LCPI", style="blue"))
        
        # Informations de base du projet
        self._configure_basic_info()
        
        # Configuration des plugins
        self._configure_plugins()
        
        # Configuration des dossiers
        self._configure_folders()
        
        # Configuration EPANET
        self._configure_epanet()
        
        # Configuration du reporting
        self._configure_reporting()
        
        # Sauvegarde finale
        self._save_configuration()
        
        console.print("✅ Configuration terminée avec succès !", style="green")
    
    def _configure_basic_info(self) -> None:
        """Configure les informations de base du projet."""
        console.print("\n📋 [bold]Informations de Base du Projet[/bold]")
        
        current_info = self.project_manager.get_project_info()
        
        # Nom du projet
        nom_projet = Prompt.ask(
            "Nom du projet",
            default=current_info.get("nom_projet", self.project_dir.name)
        )
        
        # Description
        description = Prompt.ask(
            "Description du projet",
            default=current_info.get("description", "")
        )
        
        # Auteur
        auteur = Prompt.ask(
            "Auteur du projet",
            default=current_info.get("auteur", "")
        )
        
        # Client
        client = Prompt.ask(
            "Client",
            default=current_info.get("client", "")
        )
        
        # Version
        version = Prompt.ask(
            "Version",
            default=current_info.get("version", "1.0.0")
        )
        
        # Tags
        tags_input = Prompt.ask(
            "Tags (séparés par des virgules)",
            default=",".join(current_info.get("tags", []))
        )
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        
        # Mettre à jour les informations
        updates = {
            "nom_projet": nom_projet,
            "description": description,
            "auteur": auteur,
            "client": client,
            "version": version,
            "tags": tags
        }
        
        self.project_manager.update_project_info(updates)
        console.print("✅ Informations de base configurées", style="green")
    
    def _configure_plugins(self) -> None:
        """Configure les plugins actifs."""
        console.print("\n🔌 [bold]Configuration des Plugins[/bold]")
        
        available_plugins = ["aep", "cm", "bois", "beton", "hydro", "shell"]
        current_plugins = self.project_manager.config.get("plugins_actifs", [])
        
        table = Table(title="Plugins Disponibles")
        table.add_column("Plugin", style="cyan")
        table.add_column("Statut", style="green")
        table.add_column("Description")
        
        plugin_descriptions = {
            "aep": "Alimentation en Eau Potable",
            "cm": "Construction Métallique",
            "bois": "Structures en Bois",
            "beton": "Béton Armé",
            "hydro": "Hydrologie et Hydraulique",
            "shell": "Interpréteur de commandes"
        }
        
        for plugin in available_plugins:
            status = "✅ Actif" if plugin in current_plugins else "❌ Inactif"
            description = plugin_descriptions.get(plugin, "")
            table.add_row(plugin, status, description)
        
        console.print(table)
        
        # Sélection des plugins
        console.print("\nSélectionnez les plugins à activer :")
        selected_plugins = []
        
        for plugin in available_plugins:
            if Confirm.ask(f"Activer le plugin {plugin} ?", default=plugin in current_plugins):
                selected_plugins.append(plugin)
        
        self.project_manager.config["plugins_actifs"] = selected_plugins
        console.print(f"✅ Plugins configurés : {', '.join(selected_plugins)}", style="green")
    
    def _configure_folders(self) -> None:
        """Configure la structure des dossiers."""
        console.print("\n📁 [bold]Configuration des Dossiers[/bold]")
        
        current_folders = self.project_manager.config.get("dossiers", {})
        
        folders_config = {
            "logs": "Dossier des logs de calcul",
            "outputs": "Dossier des résultats",
            "reports": "Dossier des rapports",
            "data": "Dossier des données d'entrée",
            "temp": "Dossier temporaire"
        }
        
        for folder_name, description in folders_config.items():
            current_path = current_folders.get(folder_name, f"{folder_name}/")
            new_path = Prompt.ask(
                f"{description} ({folder_name})",
                default=current_path
            )
            current_folders[folder_name] = new_path
        
        self.project_manager.config["dossiers"] = current_folders
        console.print("✅ Structure des dossiers configurée", style="green")
    
    def _configure_epanet(self) -> None:
        """Configure EPANET."""
        console.print("\n🌊 [bold]Configuration EPANET[/bold]")
        
        epanet_config = self.project_manager.get_plugin_config("epanet")
        
        # Chemin de la DLL
        dll_path = Prompt.ask(
            "Chemin vers la DLL EPANET",
            default=epanet_config.get("dll_path", "vendor/dlls/epanet2_64.dll")
        )
        
        # Version
        version = Prompt.ask(
            "Version d'EPANET",
            default=epanet_config.get("version", "2.3.1")
        )
        
        # Vérifier si la DLL existe
        dll_full_path = self.project_dir / dll_path
        if dll_full_path.exists():
            console.print(f"✅ DLL trouvée : {dll_full_path}", style="green")
        else:
            console.print(f"⚠️ DLL non trouvée : {dll_full_path}", style="yellow")
        
        new_config = {
            "dll_path": dll_path,
            "version": version
        }
        
        self.project_manager.set_plugin_config("epanet", new_config)
        console.print("✅ Configuration EPANET mise à jour", style="green")
    
    def _configure_reporting(self) -> None:
        """Configure le système de reporting."""
        console.print("\n📄 [bold]Configuration du Reporting[/bold]")
        
        reporting_config = self.project_manager.get_plugin_config("reporting")
        
        # Template par défaut
        template_default = Prompt.ask(
            "Template de rapport par défaut",
            choices=["default", "technical", "executive"],
            default=reporting_config.get("template_default", "default")
        )
        
        # Formats supportés
        formats_input = Prompt.ask(
            "Formats supportés (séparés par des virgules)",
            default=",".join(reporting_config.get("formats_supportes", ["html", "pdf", "docx"]))
        )
        formats_supportes = [fmt.strip() for fmt in formats_input.split(",") if fmt.strip()]
        
        new_config = {
            "template_default": template_default,
            "formats_supportes": formats_supportes
        }
        
        self.project_manager.set_plugin_config("reporting", new_config)
        console.print("✅ Configuration du reporting mise à jour", style="green")
    
    def _save_configuration(self) -> None:
        """Sauvegarde la configuration finale."""
        self.project_manager._save_config(self.project_manager.config)
        
        # Créer la structure de dossiers
        self.project_manager.create_project_structure()
        
        # Afficher un résumé
        self._show_configuration_summary()
    
    def _show_configuration_summary(self) -> None:
        """Affiche un résumé de la configuration."""
        console.print("\n📊 [bold]Résumé de la Configuration[/bold]")
        
        project_info = self.project_manager.get_project_info()
        
        summary_table = Table(title="Configuration du Projet")
        summary_table.add_column("Paramètre", style="cyan")
        summary_table.add_column("Valeur", style="green")
        
        summary_table.add_row("Nom du projet", project_info.get("nom_projet", ""))
        summary_table.add_row("Auteur", project_info.get("auteur", ""))
        summary_table.add_row("Client", project_info.get("client", ""))
        summary_table.add_row("Version", project_info.get("version", ""))
        summary_table.add_row("Plugins actifs", ", ".join(self.project_manager.config.get("plugins_actifs", [])))
        summary_table.add_row("Hash du projet", self.project_manager.get_project_hash())
        
        console.print(summary_table)
        
        # Afficher la structure des dossiers
        folders = self.project_manager.config.get("dossiers", {})
        console.print("\n📁 [bold]Structure des Dossiers[/bold]")
        for folder_name, folder_path in folders.items():
            full_path = self.project_dir / folder_path
            status = "✅" if full_path.exists() else "❌"
            console.print(f"{status} {folder_name}: {full_path}")

def configure_project_interactive(project_dir: Path) -> None:
    """
    Configure un projet de manière interactive.
    
    Args:
        project_dir: Chemin vers le dossier du projet
    """
    configurator = InteractiveConfigurator(project_dir)
    configurator.configure_project()
