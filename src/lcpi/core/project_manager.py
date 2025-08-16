"""
Gestionnaire de projets pour LCPI.
Gère la création, la configuration et la gestion des projets.
"""

import os
import shutil
import git
from pathlib import Path
from typing import Dict, List, Optional, Union
import yaml
from datetime import datetime

from .template_manager import create_project_from_template as create_from_template
from .global_config import global_config

class ProjectManager:
    """Gestionnaire de projets LCPI."""
    
    def __init__(self):
        self.projects_dir = Path.cwd()
    
    def create_project(
        self,
        nom_projet: str,
        template: Optional[str] = None,
        plugins: Optional[str] = None,
        force: bool = False,
        git_init: bool = False,
        remote_url: Optional[str] = None
    ) -> Path:
        """Crée un nouveau projet LCPI."""
        project_path = self.projects_dir / nom_projet
        
        if project_path.exists() and not force:
            raise FileExistsError(f"Le projet '{nom_projet}' existe déjà. Utilisez --force pour écraser.")
        
        # Créer la structure de base
        if template:
            project_path = create_from_template(nom_projet, template, str(self.projects_dir), force)
        else:
            project_path = self._create_basic_project(nom_projet, force)
        
        # Configurer les plugins
        if plugins:
            self._configure_plugins(project_path, plugins)
        
        # Initialiser Git si demandé
        if git_init:
            self._init_git_repo(project_path, remote_url)
        
        # Ajouter à la configuration globale
        global_config.add_project(nom_projet, str(project_path.resolve()))
        
        return project_path
    
    def _create_basic_project(self, nom_projet: str, force: bool = False) -> Path:
        """Crée un projet de base sans template."""
        project_path = self.projects_dir / nom_projet
        
        if project_path.exists() and not force:
            raise FileExistsError(f"Le projet '{nom_projet}' existe déjà.")
        
        # Créer la structure de base
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Créer les répertoires
        (project_path / "data").mkdir(exist_ok=True)
        (project_path / "output").mkdir(exist_ok=True)
        (project_path / "docs").mkdir(exist_ok=True)
        (project_path / "temp").mkdir(exist_ok=True)
        (project_path / "scripts").mkdir(exist_ok=True)
        
        # Créer la configuration de base
        self._create_basic_config(project_path, nom_projet)
        
        # Créer le README
        self._create_basic_readme(project_path, nom_projet)
        
        # Créer le .gitignore
        self._create_gitignore(project_path)
        
        return project_path
    
    def _create_basic_config(self, project_path: Path, nom_projet: str):
        """Crée la configuration de base du projet."""
        config = {
            "project": {
                "name": nom_projet,
                "version": "1.0.0",
                "description": f"Projet LCPI {nom_projet}",
                "created": datetime.now().isoformat(),
                "author": "LCPI CLI"
            },
            "plugins": ["core"],
            "output": {
                "formats": ["html", "json"],
                "directory": "output/"
            },
            "logging": {
                "level": "INFO",
                "file": "logs/project.log"
            }
        }
        
        with open(project_path / "lcpi.yml", "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    def _create_basic_readme(self, project_path: Path, nom_projet: str):
        """Crée le README de base du projet."""
        readme_content = f"""# {nom_projet}

Projet LCPI créé le {datetime.now().strftime('%d/%m/%Y')}.

## Structure

```
{nom_projet}/
├── lcpi.yml          # Configuration du projet
├── data/             # Données d'entrée
├── output/           # Résultats et rapports
├── docs/             # Documentation
├── scripts/          # Scripts personnalisés
└── temp/             # Fichiers temporaires
```

## Utilisation

1. **Activer le projet :**
   ```bash
   lcpi project switch {nom_projet}
   ```

2. **Exécuter des calculs :**
   ```bash
   lcpi aep run data/network.yml
   ```

3. **Générer des rapports :**
   ```bash
   lcpi report generate
   ```

## Configuration

Modifiez le fichier `lcpi.yml` pour personnaliser votre projet.
"""
        
        with open(project_path / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
    
    def _create_gitignore(self, project_path: Path):
        """Crée le fichier .gitignore du projet."""
        gitignore_content = """# LCPI
output/
temp/
*.log
*.tmp
logs/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Données sensibles
*.key
*.pem
secrets/
"""
        
        with open(project_path / ".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
    
    def _configure_plugins(self, project_path: Path, plugins: str):
        """Configure les plugins du projet."""
        plugin_list = [p.strip() for p in plugins.split(",")]
        
        # Lire la configuration existante
        config_file = project_path / "lcpi.yml"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        else:
            config = {}
        
        # Mettre à jour les plugins
        if "project" not in config:
            config["project"] = {}
        
        config["project"]["plugins"] = plugin_list
        
        # Sauvegarder la configuration
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    def _init_git_repo(self, project_path: Path, remote_url: Optional[str] = None):
        """Initialise un dépôt Git pour le projet."""
        try:
            # Initialiser le dépôt
            repo = git.Repo.init(project_path)
            
            # Ajouter tous les fichiers
            repo.index.add("*")
            
            # Premier commit
            repo.index.commit("Initial commit - Projet LCPI créé")
            
            # Configurer le remote si fourni
            if remote_url:
                origin = repo.create_remote("origin", remote_url)
                repo.index.commit("Configure remote origin")
                
        except git.GitCommandError as e:
            print(f"⚠️  Erreur lors de l'initialisation Git: {e}")
        except Exception as e:
            print(f"⚠️  Erreur inattendue lors de l'initialisation Git: {e}")
    
    def list_projects(self) -> Dict[str, Path]:
        """Liste tous les projets connus."""
        return global_config.list_projects()
    
    def get_project_info(self, nom_projet: str) -> Optional[Dict]:
        """Récupère les informations d'un projet."""
        projects = self.list_projects()
        if nom_projet not in projects:
            return None
        
        project_path = Path(projects[nom_projet])
        
        # Lire la configuration
        config_file = project_path / "lcpi.yml"
        config = {}
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        
        # Informations du projet
        info = {
            "name": nom_projet,
            "path": str(project_path.resolve()),
            "exists": project_path.exists(),
            "config": config,
            "created": project_path.stat().st_ctime if project_path.exists() else None,
            "size": self._get_project_size(project_path) if project_path.exists() else 0
        }
        
        return info
    
    def _get_project_size(self, project_path: Path) -> int:
        """Calcule la taille d'un projet en octets."""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(project_path):
                for filename in filenames:
                    file_path = Path(dirpath) / filename
                    if file_path.is_file():
                        total_size += file_path.stat().st_size
        except (OSError, PermissionError):
            pass
        
        return total_size
    
    def delete_project(self, nom_projet: str, force: bool = False) -> bool:
        """Supprime un projet."""
        projects = self.list_projects()
        if nom_projet not in projects:
            return False
        
        project_path = Path(projects[nom_projet])
        
        if not force:
            confirm = input(f"Êtes-vous sûr de vouloir supprimer le projet '{nom_projet}' ? (oui/non): ")
            if confirm.lower() not in ["oui", "o", "yes", "y"]:
                return False
        
        try:
            # Supprimer le répertoire
            if project_path.exists():
                shutil.rmtree(project_path)
            
            # Retirer de la configuration globale
            global_config.remove_project(nom_projet)
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la suppression: {e}")
            return False
    
    def archive_project(self, nom_projet: str, output_path: Optional[str] = None) -> Optional[Path]:
        """Archive un projet."""
        projects = self.list_projects()
        if nom_projet not in projects:
            return None
        
        project_path = Path(projects[nom_projet])
        
        if not project_path.exists():
            return None
        
        # Chemin de sortie par défaut
        if not output_path:
            output_path = f"{nom_projet}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        output_path = Path(output_path)
        
        try:
            # Créer l'archive
            shutil.make_archive(
                str(output_path.with_suffix("")),
                "zip",
                project_path.parent,
                project_path.name
            )
            
            return output_path.with_suffix(".zip")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'archivage: {e}")
            return None

# Instance globale
project_manager = ProjectManager()

# Fonctions d'interface
def create_project(*args, **kwargs):
    """Interface pour créer un projet."""
    return project_manager.create_project(*args, **kwargs)

def create_project_from_template(*args, **kwargs):
    """Interface pour créer un projet à partir d'un template."""
    return create_from_template(*args, **kwargs)

def list_projects():
    """Interface pour lister les projets."""
    return project_manager.list_projects()

def get_project_info(nom_projet: str):
    """Interface pour récupérer les informations d'un projet."""
    return project_manager.get_project_info(nom_projet)

def delete_project(nom_projet: str, force: bool = False):
    """Interface pour supprimer un projet."""
    return project_manager.delete_project(nom_projet, force)

def archive_project(nom_projet: str, output_path: Optional[str] = None):
    """Interface pour archiver un projet."""
    return project_manager.archive_project(nom_projet, output_path)
