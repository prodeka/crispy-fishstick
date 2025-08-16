"""
Contexte de projet pour LCPI.
Gère le contexte de travail actuel (projet ou sandbox).
"""

import os
from pathlib import Path
from typing import Dict, Optional, Union
from .global_config import global_config

class ProjectContext:
    """Contexte de projet LCPI."""
    
    def __init__(self):
        self._current_context = None
        self._refresh_context()
    
    def _refresh_context(self):
        """Actualise le contexte actuel."""
        active_project = global_config.get_active_project()
        
        if active_project:
            self._current_context = {
                "type": "project",
                "name": active_project["name"],
                "path": Path(active_project["path"]),
                "config_file": Path(active_project["path"]) / "lcpi.yml"
            }
        else:
            # Mode sandbox
            sandbox_path = global_config.get_sandbox_path()
            self._current_context = {
                "type": "sandbox",
                "name": "sandbox",
                "path": sandbox_path,
                "config_file": None
            }
    
    def get_context(self) -> Dict:
        """Retourne le contexte actuel."""
        self._refresh_context()
        return self._current_context.copy()
    
    def get_project_path(self) -> Optional[Path]:
        """Retourne le chemin du projet actuel ou None si en sandbox."""
        context = self.get_context()
        if context["type"] == "project":
            return context["path"]
        return None
    
    def get_sandbox_path(self) -> Path:
        """Retourne le chemin du sandbox."""
        return global_config.get_sandbox_path()
    
    def is_project_active(self) -> bool:
        """Vérifie si un projet est actif."""
        context = self.get_context()
        return context["type"] == "project"
    
    def is_sandbox_active(self) -> bool:
        """Vérifie si le sandbox est actif."""
        context = self.get_context()
        return context["type"] == "sandbox"
    
    def get_config_file(self) -> Optional[Path]:
        """Retourne le fichier de configuration du projet ou None."""
        context = self.get_context()
        return context.get("config_file")
    
    def get_project_name(self) -> Optional[str]:
        """Retourne le nom du projet actuel ou None si en sandbox."""
        context = self.get_context()
        if context["type"] == "project":
            return context["name"]
        return None
    
    def get_working_directory(self) -> Path:
        """Retourne le répertoire de travail actuel."""
        context = self.get_context()
        return context["path"]
    
    def get_data_directory(self) -> Path:
        """Retourne le répertoire de données."""
        working_dir = self.get_working_directory()
        data_dir = working_dir / "data"
        data_dir.mkdir(exist_ok=True)
        return data_dir
    
    def get_output_directory(self) -> Path:
        """Retourne le répertoire de sortie."""
        working_dir = self.get_working_directory()
        output_dir = working_dir / "output"
        output_dir.mkdir(exist_ok=True)
        return output_dir
    
    def get_temp_directory(self) -> Path:
        """Retourne le répertoire temporaire."""
        working_dir = self.get_working_directory()
        temp_dir = working_dir / "temp"
        temp_dir.mkdir(exist_ok=True)
        return temp_dir
    
    def get_docs_directory(self) -> Path:
        """Retourne le répertoire de documentation."""
        working_dir = self.get_working_directory()
        docs_dir = working_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        return docs_dir
    
    def get_scripts_directory(self) -> Path:
        """Retourne le répertoire de scripts."""
        working_dir = self.get_working_directory()
        scripts_dir = working_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        return scripts_dir
    
    def get_logs_directory(self) -> Path:
        """Retourne le répertoire de logs."""
        working_dir = self.get_working_directory()
        logs_dir = working_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        return logs_dir
    
    def get_project_config(self) -> Dict:
        """Retourne la configuration du projet."""
        config_file = self.get_config_file()
        if not config_file or not config_file.exists():
            return {}
        
        try:
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}
    
    def get_project_plugins(self) -> list:
        """Retourne la liste des plugins du projet."""
        config = self.get_project_config()
        return config.get("project", {}).get("plugins", [])
    
    def get_output_formats(self) -> list:
        """Retourne les formats de sortie configurés."""
        config = self.get_project_config()
        return config.get("output", {}).get("formats", ["html"])
    
    def get_default_output_format(self) -> str:
        """Retourne le format de sortie par défaut."""
        formats = self.get_output_formats()
        return formats[0] if formats else "html"
    
    def get_project_info(self) -> Dict:
        """Retourne les informations du projet."""
        config = self.get_project_config()
        project_info = config.get("project", {})
        
        return {
            "name": project_info.get("name", "Projet sans nom"),
            "version": project_info.get("version", "1.0.0"),
            "description": project_info.get("description", ""),
            "author": project_info.get("author", ""),
            "created": project_info.get("created", ""),
            "plugins": self.get_project_plugins(),
            "output_formats": self.get_output_formats()
        }
    
    def create_project_structure(self):
        """Crée la structure de dossiers du projet."""
        dirs = [
            self.get_data_directory(),
            self.get_output_directory(),
            self.get_temp_directory(),
            self.get_docs_directory(),
            self.get_scripts_directory(),
            self.get_logs_directory()
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def get_relative_path(self, file_path: Union[str, Path]) -> Path:
        """Retourne le chemin relatif par rapport au projet."""
        working_dir = self.get_working_directory()
        file_path = Path(file_path)
        
        try:
            return file_path.relative_to(working_dir)
        except ValueError:
            return file_path
    
    def get_absolute_path(self, relative_path: Union[str, Path]) -> Path:
        """Retourne le chemin absolu depuis le projet."""
        working_dir = self.get_working_directory()
        return working_dir / relative_path
    
    def file_exists_in_project(self, file_path: Union[str, Path]) -> bool:
        """Vérifie si un fichier existe dans le projet."""
        absolute_path = self.get_absolute_path(file_path)
        return absolute_path.exists()
    
    def list_project_files(self, pattern: str = "*") -> list:
        """Liste les fichiers du projet selon un pattern."""
        working_dir = self.get_working_directory()
        files = []
        
        try:
            for file_path in working_dir.rglob(pattern):
                if file_path.is_file():
                    files.append(file_path.relative_to(working_dir))
        except Exception:
            pass
        
        return files
    
    def get_project_size(self) -> int:
        """Calcule la taille du projet en octets."""
        working_dir = self.get_working_directory()
        total_size = 0
        
        try:
            for file_path in working_dir.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception:
            pass
        
        return total_size
    
    def get_context_summary(self) -> Dict:
        """Retourne un résumé du contexte actuel."""
        context = self.get_context()
        
        summary = {
            "type": context["type"],
            "name": context["name"],
            "path": str(context["path"]),
            "working_directory": str(self.get_working_directory()),
            "project_active": self.is_project_active(),
            "sandbox_active": self.is_sandbox_active()
        }
        
        if self.is_project_active():
            summary.update({
                "project_info": self.get_project_info(),
                "data_directory": str(self.get_data_directory()),
                "output_directory": str(self.get_output_directory()),
                "temp_directory": str(self.get_temp_directory()),
                "docs_directory": str(self.get_docs_directory()),
                "scripts_directory": str(self.get_scripts_directory()),
                "logs_directory": str(self.get_logs_directory()),
                "project_size": self.get_project_size()
            })
        
        return summary

# Instance globale
project_context = ProjectContext()

# Fonctions d'interface pour compatibilité
def get_project_context() -> Dict:
    """Retourne le contexte du projet actuel."""
    return project_context.get_context()

def get_project_path() -> Optional[Path]:
    """Retourne le chemin du projet actuel."""
    return project_context.get_project_path()

def is_project_active() -> bool:
    """Vérifie si un projet est actif."""
    return project_context.is_project_active()

def is_sandbox_active() -> bool:
    """Vérifie si le sandbox est actif."""
    return project_context.is_sandbox_active()

def get_working_directory() -> Path:
    """Retourne le répertoire de travail actuel."""
    return project_context.get_working_directory()

def get_data_directory() -> Path:
    """Retourne le répertoire de données."""
    return project_context.get_data_directory()

def get_output_directory() -> Path:
    """Retourne le répertoire de sortie."""
    return project_context.get_output_directory()

def get_project_config() -> Dict:
    """Retourne la configuration du projet."""
    return project_context.get_project_config()

def get_project_plugins() -> list:
    """Retourne la liste des plugins du projet."""
    return project_context.get_project_plugins()

# =============================================================================
# FONCTIONS DE COMPATIBILITÉ
# =============================================================================

def require_project_context(func):
    """
    Décorateur pour s'assurer qu'une commande s'exécute dans le contexte d'un projet.
    
    Usage:
        @require_project_context
        def ma_commande():
            pass
    """
    def wrapper(*args, **kwargs):
        if not project_context.is_project_active():
            raise RuntimeError("Cette commande nécessite un projet actif. Utilisez 'lcpi project switch <nom>' ou 'lcpi project init'.")
        return func(*args, **kwargs)
    return wrapper

def ensure_project_structure(project_path: Optional[Path] = None) -> Path:
    """
    S'assure que la structure de projet existe et la crée si nécessaire.
    
    Args:
        project_path: Chemin du projet (optionnel, utilise le projet actif si non spécifié)
    
    Returns:
        Chemin du projet validé
    """
    if project_path is None:
        if not project_context.is_project_active():
            raise RuntimeError("Aucun projet actif. Utilisez 'lcpi project switch <nom>' ou 'lcpi project init'.")
        project_path = project_context.get_project_path()
    
    # Créer la structure de base si elle n'existe pas
    for subdir in ["data", "output", "temp", "docs", "scripts", "logs"]:
        (project_path / subdir).mkdir(exist_ok=True)
    
    return project_path
