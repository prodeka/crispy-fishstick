"""
Gestionnaire de base de données global pour LCPI

Ce module fournit une interface unifiée pour interroger et manipuler
toutes les bases de données LCPI (AEP, CM, Bois, Béton, Hydrodrain).
"""

import json
import sqlite3
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import re

class GlobalDatabaseManager:
    """
    Gestionnaire de base de données global pour LCPI.
    
    Fonctionnalités :
    - Requêtes unifiées sur toutes les bases de données
    - Recherche textuelle globale
    - Filtres avancés par plugin
    - Export des résultats
    - Auto-complétion globale
    """
    
    def __init__(self):
        """Initialise le gestionnaire de base de données global."""
        self.databases = {}
        self.load_all_databases()
        
    def load_all_databases(self):
        """Charge toutes les bases de données disponibles."""
        db_path = Path("src/lcpi/db")
        
        # Base de données AEP
        aep_db_path = db_path / "aep_database.json"
        if aep_db_path.exists():
            try:
                with open(aep_db_path, 'r', encoding='utf-8') as f:
                    self.databases['aep'] = json.load(f)
                print("✅ Base de données AEP chargée")
            except Exception as e:
                print(f"⚠️ Erreur chargement AEP: {e}")
                self.databases['aep'] = {}
        
        # Base de données CM-Bois
        cm_bois_db_path = db_path / "cm_bois.json"
        if cm_bois_db_path.exists():
            try:
                with open(cm_bois_db_path, 'r', encoding='utf-8') as f:
                    self.databases['cm_bois'] = json.load(f)
                print("✅ Base de données CM-Bois chargée")
            except Exception as e:
                print(f"⚠️ Erreur chargement CM-Bois: {e}")
                self.databases['cm_bois'] = {}
        
        # Base de données Bois
        bois_db_path = db_path / "bois_test.json"
        if bois_db_path.exists():
            try:
                with open(bois_db_path, 'r', encoding='utf-8') as f:
                    self.databases['bois'] = json.load(f)
                print("✅ Base de données Bois chargée")
            except Exception as e:
                print(f"⚠️ Erreur chargement Bois: {e}")
                self.databases['bois'] = {}
        
        print(f"📊 {len(self.databases)} bases de données chargées")
    
    def global_search(self, search_term: str, plugins: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Recherche globale dans toutes les bases de données.
        
        Args:
            search_term: Terme de recherche
            plugins: Liste des plugins à rechercher (optionnel)
            
        Returns:
            List: Résultats de la recherche avec indication du plugin
        """
        results = []
        search_term_lower = search_term.lower()
        
        # Déterminer les plugins à rechercher
        if plugins is None:
            plugins = list(self.databases.keys())
        
        for plugin in plugins:
            if plugin not in self.databases:
                continue
                
            plugin_results = self._search_in_database(
                self.databases[plugin], 
                search_term_lower, 
                plugin
            )
            results.extend(plugin_results)
        
        return results
    
    def _search_in_database(self, data: Any, search_term: str, plugin: str, path: str = "") -> List[Dict[str, Any]]:
        """
        Recherche récursive dans une base de données.
        
        Args:
            data: Données à rechercher
            search_term: Terme de recherche
            plugin: Nom du plugin
            path: Chemin actuel dans la structure
            
        Returns:
            List: Résultats de la recherche
        """
        results = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                
                # Recherche dans les clés
                if search_term in key.lower():
                    results.append({
                        "plugin": plugin,
                        "path": current_path,
                        "key": key,
                        "value": value,
                        "match_type": "key"
                    })
                
                # Recherche dans les valeurs
                if isinstance(value, str) and search_term in value.lower():
                    results.append({
                        "plugin": plugin,
                        "path": current_path,
                        "key": key,
                        "value": value,
                        "match_type": "value"
                    })
                
                # Recherche récursive
                results.extend(self._search_in_database(value, search_term, plugin, current_path))
                
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]"
                results.extend(self._search_in_database(item, search_term, plugin, current_path))
        
        return results
    
    def query_by_plugin(self, plugin: str, query_type: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Requête spécifique par plugin.
        
        Args:
            plugin: Nom du plugin (aep, cm_bois, bois, etc.)
            query_type: Type de requête
            **kwargs: Paramètres supplémentaires
            
        Returns:
            List: Résultats de la requête
        """
        if plugin not in self.databases:
            return []
        
        if plugin == "aep":
            return self._query_aep(query_type, **kwargs)
        elif plugin == "cm_bois":
            return self._query_cm_bois(query_type, **kwargs)
        elif plugin == "bois":
            return self._query_bois(query_type, **kwargs)
        else:
            return self._query_generic(plugin, query_type, **kwargs)
    
    def _query_aep(self, query_type: str, **kwargs) -> List[Dict[str, Any]]:
        """Requêtes spécifiques AEP."""
        results = []
        data = self.databases.get('aep', {})
        
        if query_type == "coefficients":
            # Recherche des coefficients de rugosité
            for key, value in data.items():
                if "coefficient" in key.lower() or "rugosite" in key.lower():
                    results.append({
                        "plugin": "aep",
                        "type": key,
                        "data": value
                    })
        
        elif query_type == "materials":
            # Recherche des matériaux
            for key, value in data.items():
                if "materiau" in key.lower() or "material" in key.lower():
                    results.append({
                        "plugin": "aep",
                        "type": key,
                        "data": value
                    })
        
        elif query_type == "formulas":
            # Recherche des formules
            for key, value in data.items():
                if "formule" in key.lower() or "formula" in key.lower():
                    results.append({
                        "plugin": "aep",
                        "type": key,
                        "data": value
                    })
        
        return results
    
    def _query_cm_bois(self, query_type: str, **kwargs) -> List[Dict[str, Any]]:
        """Requêtes spécifiques CM-Bois."""
        results = []
        data = self.databases.get('cm_bois', {})
        
        if query_type == "sections":
            # Recherche des sections
            for key, value in data.items():
                if "section" in key.lower():
                    results.append({
                        "plugin": "cm_bois",
                        "type": key,
                        "data": value
                    })
        
        elif query_type == "materials":
            # Recherche des matériaux
            for key, value in data.items():
                if "materiau" in key.lower() or "material" in key.lower():
                    results.append({
                        "plugin": "cm_bois",
                        "type": key,
                        "data": value
                    })
        
        return results
    
    def _query_bois(self, query_type: str, **kwargs) -> List[Dict[str, Any]]:
        """Requêtes spécifiques Bois."""
        results = []
        data = self.databases.get('bois', {})
        
        if query_type == "species":
            # Recherche des essences de bois
            for key, value in data.items():
                if "espece" in key.lower() or "species" in key.lower():
                    results.append({
                        "plugin": "bois",
                        "type": key,
                        "data": value
                    })
        
        elif query_type == "properties":
            # Recherche des propriétés
            for key, value in data.items():
                if "propriete" in key.lower() or "property" in key.lower():
                    results.append({
                        "plugin": "bois",
                        "type": key,
                        "data": value
                    })
        
        return results
    
    def _query_generic(self, plugin: str, query_type: str, **kwargs) -> List[Dict[str, Any]]:
        """Requêtes génériques pour les autres plugins."""
        results = []
        data = self.databases.get(plugin, {})
        
        # Recherche générique par type
        for key, value in data.items():
            if query_type.lower() in key.lower():
                results.append({
                    "plugin": plugin,
                    "type": key,
                    "data": value
                })
        
        return results
    
    def get_autocomplete_options(self, query: str, plugins: Optional[List[str]] = None) -> List[str]:
        """
        Génère des options d'auto-complétion globales.
        
        Args:
            query: Requête de recherche
            plugins: Liste des plugins à considérer (optionnel)
            
        Returns:
            List: Options d'auto-complétion
        """
        options = set()
        
        # Déterminer les plugins à considérer
        if plugins is None:
            plugins = list(self.databases.keys())
        
        for plugin in plugins:
            if plugin not in self.databases:
                continue
            
            plugin_options = self._get_autocomplete_for_plugin(
                self.databases[plugin], 
                query, 
                plugin
            )
            options.update(plugin_options)
        
        return sorted(list(options))
    
    def _get_autocomplete_for_plugin(self, data: Any, query: str, plugin: str) -> List[str]:
        """
        Génère des options d'auto-complétion pour un plugin.
        
        Args:
            data: Données du plugin
            query: Requête de recherche
            plugin: Nom du plugin
            
        Returns:
            List: Options d'auto-complétion
        """
        options = []
        query_lower = query.lower()
        
        def search_keys(data):
            if isinstance(data, dict):
                for key in data.keys():
                    if query_lower in key.lower():
                        options.append(f"{plugin}:{key}")
                for value in data.values():
                    search_keys(value)
            elif isinstance(data, list):
                for item in data:
                    search_keys(item)
        
        search_keys(data)
        return options
    
    def export_results(self, results: List[Dict[str, Any]], format: str = "json") -> str:
        """
        Exporte les résultats dans différents formats.
        
        Args:
            results: Résultats à exporter
            format: Format d'export (json, csv, markdown)
            
        Returns:
            str: Contenu exporté
        """
        if format == "json":
            return json.dumps(results, indent=2, ensure_ascii=False)
        
        elif format == "csv":
            if not results:
                return ""
            
            # Déterminer les colonnes
            columns = set()
            for result in results:
                if isinstance(result, dict):
                    columns.update(result.keys())
            
            columns = sorted(list(columns))
            
            # Générer le CSV
            lines = [",".join(columns)]
            for result in results:
                if isinstance(result, dict):
                    row = []
                    for col in columns:
                        value = result.get(col, "")
                        if isinstance(value, (dict, list)):
                            value = str(value)
                        row.append(str(value))
                    lines.append(",".join(row))
            
            return "\n".join(lines)
        
        elif format == "markdown":
            if not results:
                return ""
            
            lines = ["# Résultats de la recherche globale", ""]
            
            # Grouper par plugin
            by_plugin = {}
            for result in results:
                plugin = result.get("plugin", "unknown")
                if plugin not in by_plugin:
                    by_plugin[plugin] = []
                by_plugin[plugin].append(result)
            
            for plugin, plugin_results in by_plugin.items():
                lines.append(f"## Plugin {plugin.upper()}")
                lines.append("")
                
                for i, result in enumerate(plugin_results, 1):
                    lines.append(f"### Résultat {i}")
                    lines.append("")
                    
                    if isinstance(result, dict):
                        for key, value in result.items():
                            if isinstance(value, dict):
                                lines.append(f"#### {key}")
                                lines.append("")
                                for sub_key, sub_value in value.items():
                                    lines.append(f"- **{sub_key}:** {sub_value}")
                                lines.append("")
                            else:
                                lines.append(f"- **{key}:** {value}")
                    else:
                        lines.append(f"- {result}")
                    
                    lines.append("")
            
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Format non supporté: {format}")

# Fonctions d'interface pour CLI/REPL
def create_global_database_manager() -> GlobalDatabaseManager:
    """
    Crée et retourne une instance du gestionnaire de base de données global.
    
    Returns:
        GlobalDatabaseManager: Instance du gestionnaire
    """
    return GlobalDatabaseManager()

def global_search(search_term: str, plugins: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Interface de recherche globale.
    
    Args:
        search_term: Terme de recherche
        plugins: Liste des plugins à rechercher (optionnel)
        
    Returns:
        List: Résultats de la recherche
    """
    manager = create_global_database_manager()
    return manager.global_search(search_term, plugins)

def query_database(plugin: str, query_type: str, **kwargs) -> List[Dict[str, Any]]:
    """
    Interface de requête par plugin.
    
    Args:
        plugin: Nom du plugin
        query_type: Type de requête
        **kwargs: Paramètres supplémentaires
        
    Returns:
        List: Résultats de la requête
    """
    manager = create_global_database_manager()
    return manager.query_by_plugin(plugin, query_type, **kwargs)

def get_global_autocomplete_options(query: str, plugins: Optional[List[str]] = None) -> List[str]:
    """
    Interface d'auto-complétion globale.
    
    Args:
        query: Requête de recherche
        plugins: Liste des plugins à considérer (optionnel)
        
    Returns:
        List: Options d'auto-complétion
    """
    manager = create_global_database_manager()
    return manager.get_autocomplete_options(query, plugins) 