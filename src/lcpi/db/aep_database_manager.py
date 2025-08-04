"""
Gestionnaire de base de données AEP avec interface de requête

Ce module fournit une interface pour interroger et manipuler
la base de données AEP avec des requêtes avancées.
"""

import json
import sqlite3
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import re

class AEPDatabaseManager:
    """
    Gestionnaire de base de données AEP avec requêtes avancées.
    
    Fonctionnalités :
    - Requêtes par type de données
    - Recherche textuelle
    - Filtres avancés
    - Export des résultats
    - Auto-complétion des options
    """
    
    def __init__(self, db_path: str = "src/lcpi/db/aep_database.json"):
        """
        Initialise le gestionnaire de base de données.
        
        Args:
            db_path: Chemin vers la base de données AEP
        """
        self.db_path = Path(db_path)
        self.data = {}
        self.load_database()
        
    def load_database(self):
        """Charge la base de données AEP."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print("✅ Base de données AEP chargée avec succès.")
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement de la base de données: {e}")
            self.data = {}
    
    def query_by_type(self, data_type: str) -> List[Dict[str, Any]]:
        """
        Requête par type de données.
        
        Args:
            data_type: Type de données (coefficients, materiaux, formules, etc.)
            
        Returns:
            List: Résultats de la requête
        """
        results = []
        
        if isinstance(self.data, dict):
            # Recherche dans les clés principales
            for key, value in self.data.items():
                if data_type.lower() in key.lower():
                    if isinstance(value, dict):
                        results.append({"type": key, "data": value})
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                results.append({"type": key, "data": item})
                            else:
                                results.append({"type": key, "value": item})
                    else:
                        results.append({"type": key, "value": value})
        
        return results
    
    def search_text(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Recherche textuelle dans la base de données.
        
        Args:
            search_term: Terme de recherche
            
        Returns:
            List: Résultats de la recherche
        """
        results = []
        search_term_lower = search_term.lower()
        
        def search_recursive(data, path=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Recherche dans les clés
                    if search_term_lower in key.lower():
                        results.append({
                            "path": current_path,
                            "key": key,
                            "value": value,
                            "match_type": "key"
                        })
                    
                    # Recherche dans les valeurs
                    if isinstance(value, str) and search_term_lower in value.lower():
                        results.append({
                            "path": current_path,
                            "key": key,
                            "value": value,
                            "match_type": "value"
                        })
                    
                    # Recherche récursive
                    search_recursive(value, current_path)
                    
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    current_path = f"{path}[{i}]"
                    search_recursive(item, current_path)
        
        search_recursive(self.data)
        return results
    
    def get_coefficients(self, material: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Récupère les coefficients de rugosité.
        
        Args:
            material: Matériau spécifique (optionnel)
            
        Returns:
            List: Coefficients de rugosité
        """
        results = []
        
        # Recherche des coefficients dans la base
        coefficient_data = self.data.get("coefficients", {})
        
        if material:
            # Filtrage par matériau
            material_lower = material.lower()
            for key, value in coefficient_data.items():
                if material_lower in key.lower():
                    results.append({
                        "material": key,
                        "coefficient": value,
                        "type": "rugosite"
                    })
        else:
            # Tous les coefficients
            for key, value in coefficient_data.items():
                results.append({
                    "material": key,
                    "coefficient": value,
                    "type": "rugosite"
                })
        
        return results
    
    def get_materials(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Récupère les matériaux.
        
        Args:
            category: Catégorie de matériau (optionnel)
            
        Returns:
            List: Matériaux
        """
        results = []
        
        # Recherche des matériaux dans la base
        materials_data = self.data.get("materials", {})
        
        if category:
            # Filtrage par catégorie
            category_lower = category.lower()
            for key, value in materials_data.items():
                if isinstance(value, dict) and category_lower in value.get("category", "").lower():
                    results.append({
                        "name": key,
                        "properties": value,
                        "category": value.get("category", "unknown")
                    })
        else:
            # Tous les matériaux
            for key, value in materials_data.items():
                if isinstance(value, dict):
                    results.append({
                        "name": key,
                        "properties": value,
                        "category": value.get("category", "unknown")
                    })
        
        return results
    
    def get_formulas(self, formula_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Récupère les formules mathématiques.
        
        Args:
            formula_type: Type de formule (optionnel)
            
        Returns:
            List: Formules
        """
        results = []
        
        # Recherche des formules dans la base
        formulas_data = self.data.get("formulas", {})
        
        if formula_type:
            # Filtrage par type
            type_lower = formula_type.lower()
            for key, value in formulas_data.items():
                if isinstance(value, dict) and type_lower in value.get("type", "").lower():
                    results.append({
                        "name": key,
                        "formula": value,
                        "type": value.get("type", "unknown")
                    })
        else:
            # Toutes les formules
            for key, value in formulas_data.items():
                if isinstance(value, dict):
                    results.append({
                        "name": key,
                        "formula": value,
                        "type": value.get("type", "unknown")
                    })
        
        return results
    
    def get_constants(self, constant_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Récupère les constantes physiques.
        
        Args:
            constant_type: Type de constante (optionnel)
            
        Returns:
            List: Constantes
        """
        results = []
        
        # Recherche des constantes dans la base
        constants_data = self.data.get("constants", {})
        
        if constant_type:
            # Filtrage par type
            type_lower = constant_type.lower()
            for key, value in constants_data.items():
                if isinstance(value, dict) and type_lower in value.get("type", "").lower():
                    results.append({
                        "name": key,
                        "value": value.get("value"),
                        "unit": value.get("unit", ""),
                        "type": value.get("type", "unknown")
                    })
        else:
            # Toutes les constantes
            for key, value in constants_data.items():
                if isinstance(value, dict):
                    results.append({
                        "name": key,
                        "value": value.get("value"),
                        "unit": value.get("unit", ""),
                        "type": value.get("type", "unknown")
                    })
        
        return results
    
    def get_autocomplete_options(self, query: str) -> List[str]:
        """
        Génère des options d'auto-complétion basées sur la requête.
        
        Args:
            query: Requête de recherche
            
        Returns:
            List: Options d'auto-complétion
        """
        options = set()
        query_lower = query.lower()
        
        # Recherche dans les clés principales
        for key in self.data.keys():
            if query_lower in key.lower():
                options.add(key)
        
        # Recherche dans les valeurs imbriquées
        def search_keys(data):
            if isinstance(data, dict):
                for key in data.keys():
                    if query_lower in key.lower():
                        options.add(key)
                for value in data.values():
                    search_keys(value)
            elif isinstance(data, list):
                for item in data:
                    search_keys(item)
        
        search_keys(self.data)
        
        return sorted(list(options))
    
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
            
            lines = ["# Résultats de la requête AEP", ""]
            
            for i, result in enumerate(results, 1):
                lines.append(f"## Résultat {i}")
                lines.append("")
                
                if isinstance(result, dict):
                    for key, value in result.items():
                        if isinstance(value, dict):
                            lines.append(f"### {key}")
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

def create_aep_database_manager() -> AEPDatabaseManager:
    """
    Crée et retourne une instance du gestionnaire de base de données AEP.
    
    Returns:
        AEPDatabaseManager: Instance du gestionnaire
    """
    return AEPDatabaseManager()

# Fonctions d'interface pour CLI/REPL
def query_aep_database(query_type: str, **kwargs) -> List[Dict[str, Any]]:
    """
    Interface de requête pour la base de données AEP.
    
    Args:
        query_type: Type de requête (coefficients, materials, formulas, constants, search)
        **kwargs: Paramètres supplémentaires
        
    Returns:
        List: Résultats de la requête
    """
    manager = create_aep_database_manager()
    
    if query_type == "coefficients":
        return manager.get_coefficients(kwargs.get("material"))
    elif query_type == "materials":
        return manager.get_materials(kwargs.get("category"))
    elif query_type == "formulas":
        return manager.get_formulas(kwargs.get("formula_type"))
    elif query_type == "constants":
        return manager.get_constants(kwargs.get("constant_type"))
    elif query_type == "search":
        return manager.search_text(kwargs.get("search_term", ""))
    else:
        return manager.query_by_type(query_type)

def get_aep_autocomplete_options(query: str) -> List[str]:
    """
    Interface d'auto-complétion pour la base de données AEP.
    
    Args:
        query: Requête de recherche
        
    Returns:
        List: Options d'auto-complétion
    """
    manager = create_aep_database_manager()
    return manager.get_autocomplete_options(query) 