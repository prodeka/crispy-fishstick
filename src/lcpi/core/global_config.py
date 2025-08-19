"""
Configuration globale pour LCPI.
Gère la configuration des projets et des paramètres globaux.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import yaml

class GlobalConfig:
    """Configuration globale de LCPI."""
    
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "lcpi_global.json"
        self.projects_file = self.config_dir / "projects.json"
        self.config = self._load_config()
        self.projects = self._load_projects()
    
    def _get_config_dir(self) -> Path:
        """Retourne le répertoire de configuration."""
        # Sur Windows, utiliser %APPDATA%
        if os.name == 'nt':
            config_dir = Path(os.environ.get('APPDATA', '')) / "LCPI"
        else:
            # Sur Unix/Linux/macOS
            config_dir = Path.home() / ".config" / "lcpi"
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration globale."""
        if not self.config_file.exists():
            return self._create_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config
        except Exception:
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Crée une configuration par défaut."""
        default_config = {
            "version": "2.1.0",
            "active_project": None,
            "sandbox_path": str(self.config_dir / "sandbox"),
            "default_plugins": ["core"],
            "logging": {
                "level": "INFO",
                "file": str(self.config_dir / "logs" / "lcpi.log"),
                "max_size": "10MB",
                "backup_count": 5
            },
            "output": {
                "default_format": "html",
                "templates_dir": str(self.config_dir / "templates"),
                "reports_dir": str(self.config_dir / "reports")
            },
            "epanet": {
                "dll_path": None,
                "version": "2.3.1"
            },
            "ui": {
                "theme": "default",
                "language": "fr",
                "auto_save": True
            }
        }
        
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config: Dict[str, Any]):
        """Sauvegarde la configuration globale."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Erreur lors de la sauvegarde de la configuration: {e}")
    
    def _load_projects(self) -> Dict[str, str]:
        """Charge la liste des projets."""
        if not self.projects_file.exists():
            return {}
        
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as f:
                projects = json.load(f)
                return projects
        except Exception:
            return {}
    
    def _save_projects(self):
        """Sauvegarde la liste des projets."""
        try:
            with open(self.projects_file, 'w', encoding='utf-8') as f:
                json.dump(self.projects, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Erreur lors de la sauvegarde des projets: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Définit une valeur de configuration."""
        keys = key.split('.')
        config = self.config
        
        # Naviguer vers le bon niveau
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Définir la valeur
        config[keys[-1]] = value
        
        # Sauvegarder
        self._save_config(self.config)
    
    def add_project(self, name: str, path: str):
        """Ajoute un projet à la liste."""
        self.projects[name] = path
        self._save_projects()
    
    def remove_project(self, name: str):
        """Retire un projet de la liste."""
        if name in self.projects:
            del self.projects[name]
            self._save_projects()
        
        # Si c'était le projet actif, le désactiver
        if self.get("active_project") == name:
            self.set("active_project", None)
    
    def list_projects(self) -> Dict[str, str]:
        """Retourne la liste des projets."""
        return self.projects.copy()
    
    def get_project_path(self, name: str) -> Optional[str]:
        """Retourne le chemin d'un projet."""
        return self.projects.get(name)
    
    def set_active_project(self, name: str):
        """Définit le projet actif."""
        if name not in self.projects:
            raise ValueError(f"Projet '{name}' non trouvé")
        
        self.set("active_project", name)
    
    def get_active_project(self) -> Optional[Dict[str, str]]:
        """Retourne le projet actif."""
        active_name = self.get("active_project")
        if not active_name or active_name not in self.projects:
            return None
        
        return {
            "name": active_name,
            "path": self.projects[active_name]
        }
    
    def is_sandbox_active(self) -> bool:
        """Vérifie si le sandbox est actif."""
        return self.get("active_project") is None
    
    def get_sandbox_path(self) -> Path:
        """Retourne le chemin du sandbox."""
        sandbox_path = Path(self.get("sandbox_path"))
        sandbox_path.mkdir(parents=True, exist_ok=True)
        return sandbox_path
    
    def clean_sandbox(self):
        """Nettoie le contenu du sandbox."""
        sandbox_path = self.get_sandbox_path()
        
        for item in sandbox_path.iterdir():
            try:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    import shutil
                    shutil.rmtree(item)
            except Exception as e:
                print(f"⚠️  Erreur lors de la suppression de {item}: {e}")
    
    def get_plugin_config(self, plugin_name: str) -> Dict[str, Any]:
        """Retourne la configuration d'un plugin."""
        return self.get(f"plugins.{plugin_name}", {})
    
    def set_plugin_config(self, plugin_name: str, config: Dict[str, Any]):
        """Définit la configuration d'un plugin."""
        self.set(f"plugins.{plugin_name}", config)
    
    def get_output_config(self) -> Dict[str, Any]:
        """Retourne la configuration de sortie."""
        return self.get("output", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Retourne la configuration de logging."""
        return self.get("logging", {})
    
    def get_epanet_config(self) -> Dict[str, Any]:
        """Retourne la configuration EPANET."""
        return self.get("epanet", {})
    
    def set_epanet_dll(self, dll_path: str):
        """Définit le chemin de la DLL EPANET."""
        self.set("epanet.dll_path", dll_path)
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Retourne la configuration de l'interface."""
        return self.get("ui", {})
    
    def export_config(self, format: str = "json") -> str:
        """Exporte la configuration dans différents formats."""
        if format.lower() == "json":
            import json
            return json.dumps(self.config, indent=2, ensure_ascii=False)
        elif format.lower() == "yaml":
            return yaml.dump(self.config, default_flow_style=False, allow_unicode=True)
        else:
            raise ValueError(f"Format non supporté: {format}")
    
    def import_config(self, config_data: str, format: str = "json"):
        """Importe une configuration."""
        if format.lower() == "json":
            import json
            new_config = json.loads(config_data)
        elif format.lower() == "yaml":
            new_config = yaml.safe_load(config_data)
        else:
            raise ValueError(f"Format non supporté: {format}")
        
        # Fusionner avec la configuration existante
        self.config.update(new_config)
        self._save_config(self.config)
    
    def reset_config(self):
        """Réinitialise la configuration aux valeurs par défaut."""
        self.config = self._create_default_config()
    
    def get_config_info(self) -> Dict[str, Any]:
        """Retourne des informations sur la configuration."""
        return {
            "config_file": str(self.config_file),
            "projects_file": str(self.projects_file),
            "active_project": self.get("active_project"),
            "total_projects": len(self.projects),
            "version": self.get("version"),
            "sandbox_active": self.is_sandbox_active()
        }

# Instance globale
global_config = GlobalConfig()

# Compatibilité avec anciens imports
# Certains tests attendent `GlobalConfigManager` dans ce module.
# On crée un alias vers la classe actuelle.
GlobalConfigManager = GlobalConfig