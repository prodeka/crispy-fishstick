"""
Gestion des versions d'API des plugins LCPI.
Assure la compatibilité entre les plugins et le core LCPI.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from packaging import version

# Version d'API LCPI actuelle
CURRENT_API_VERSION = "2.1.0"

# Versions d'API supportées (rétrocompatibilité)
SUPPORTED_API_VERSIONS = [
    "2.0.0",
    "2.1.0"
]

class PluginVersionManager:
    """Gère la compatibilité des versions d'API des plugins."""
    
    def __init__(self):
        self.plugin_versions = {}
        self._load_plugin_versions()
    
    def _load_plugin_versions(self):
        """Charge les informations de version des plugins depuis leurs métadonnées."""
        plugin_dirs = [
            "aep", "cm", "bois", "beton", "hydrodrain", 
            "shell", "reporting", "validation"
        ]
        
        for plugin_name in plugin_dirs:
            plugin_path = Path(__file__).parent.parent / plugin_name
            if plugin_path.exists():
                version_info = self._extract_plugin_version(plugin_path, plugin_name)
                if version_info:
                    self.plugin_versions[plugin_name] = version_info
    
    def _extract_plugin_version(self, plugin_path: Path, plugin_name: str) -> Optional[Dict]:
        """Extrait les informations de version d'un plugin."""
        # Chercher dans __init__.py
        init_file = plugin_path / "__init__.py"
        if init_file.exists():
            content = init_file.read_text(encoding='utf-8')
            
            # Extraire la version
            version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                plugin_version = version_match.group(1)
                
                # Déterminer la version d'API supportée
                api_version = self._determine_api_version(plugin_name, plugin_version)
                
                return {
                    "plugin_version": plugin_version,
                    "api_version": api_version,
                    "compatible": self._is_compatible(api_version),
                    "status": self._get_compatibility_status(api_version)
                }
        
        return None
    
    def _determine_api_version(self, plugin_name: str, plugin_version: str) -> str:
        """Détermine la version d'API supportée par un plugin."""
        # Logique de mapping plugin → API version
        # Peut être étendue avec des métadonnées spécifiques
        if plugin_name in ["aep", "cm", "bois", "beton"]:
            # Plugins métier principaux
            if version.parse(plugin_version) >= version.parse("2.0.0"):
                return "2.1.0"
            else:
                return "2.0.0"
        elif plugin_name in ["shell", "validation"]:
            # Plugins de base
            return "2.1.0"
        else:
            # Par défaut
            return "2.0.0"
    
    def _is_compatible(self, api_version: str) -> bool:
        """Vérifie si une version d'API est compatible."""
        return api_version in SUPPORTED_API_VERSIONS
    
    def _get_compatibility_status(self, api_version: str) -> str:
        """Retourne le statut de compatibilité."""
        if self._is_compatible(api_version):
            if api_version == CURRENT_API_VERSION:
                return "✅ Compatible (version actuelle)"
            else:
                return "⚠️ Compatible (version antérieure)"
        else:
            return "❌ Incompatible"
    
    def get_plugin_api_version(self, plugin_name: str) -> Optional[Dict]:
        """Récupère les informations de version d'API d'un plugin."""
        return self.plugin_versions.get(plugin_name)
    
    def check_plugin_compatibility(self, plugin_name: str) -> Tuple[bool, str]:
        """Vérifie la compatibilité d'un plugin."""
        plugin_info = self.get_plugin_api_version(plugin_name)
        if not plugin_info:
            return False, f"Plugin '{plugin_name}' non trouvé"
        
        if not plugin_info["compatible"]:
            return False, f"Plugin '{plugin_name}' incompatible (API {plugin_info['api_version']})"
        
        return True, f"Plugin '{plugin_name}' compatible (API {plugin_info['api_version']})"
    
    def list_plugin_versions(self) -> Dict[str, Dict]:
        """Liste tous les plugins avec leurs versions d'API."""
        return self.plugin_versions
    
    def get_api_compatibility_matrix(self) -> Dict[str, List[str]]:
        """Retourne la matrice de compatibilité des versions d'API."""
        matrix = {}
        for api_ver in SUPPORTED_API_VERSIONS:
            matrix[api_ver] = []
            for plugin_name, info in self.plugin_versions.items():
                if info["api_version"] == api_ver:
                    matrix[api_ver].append(plugin_name)
        return matrix

# Instance globale
plugin_version_manager = PluginVersionManager()
