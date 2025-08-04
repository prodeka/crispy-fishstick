#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de recherche globale dans toutes les bases de données
Permet de rechercher avec des mots-clés flexibles dans toutes les DB
"""

import json
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Set
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import re
from collections import defaultdict

console = Console()

class GlobalDatabaseSearch:
    """Système de recherche globale dans toutes les bases de données"""
    
    def __init__(self, db_path: str = "src/lcpi/db"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        self.cache = {}
    
    def get_all_databases(self) -> Dict[str, Path]:
        """Récupère toutes les bases de données disponibles"""
        databases = {}
        
        # Bases JSON
        for json_file in self.db_path.glob("*.json"):
            databases[json_file.stem] = json_file
        
        # Bases SQLite
        for sqlite_file in self.db_path.glob("*.db"):
            databases[sqlite_file.stem] = sqlite_file
        
        return databases
    
    def load_json_db(self, db_file: Path) -> Dict:
        """Charge une base de données JSON (supporte les fichiers multi-JSON)"""
        with open(db_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Essayer de charger comme JSON simple d'abord
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Si ça échoue, essayer de traiter comme multi-JSON
            try:
                # Diviser le contenu en objets JSON séparés
                json_objects = []
                brace_count = 0
                start_pos = 0
                
                for i, char in enumerate(content):
                    if char == '{':
                        if brace_count == 0:
                            start_pos = i
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            # Extraire l'objet JSON complet
                            json_str = content[start_pos:i+1]
                            try:
                                obj = json.loads(json_str)
                                json_objects.append(obj)
                            except json.JSONDecodeError:
                                continue
                
                # Fusionner tous les objets en un seul
                merged_data = {}
                for obj in json_objects:
                    merged_data.update(obj)
                
                return merged_data
                
            except Exception as e:
                raise Exception(f"Impossible de parser le fichier JSON {db_file}: {e}")
    
    def search_in_json_data(self, data: Dict, keywords: List[str], db_name: str) -> List[Dict]:
        """Recherche dans les données JSON avec des mots-clés"""
        results = []
        
        def search_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    search_recursive(value, current_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{path}[{i}]"
                    search_recursive(item, current_path)
            else:
                # Vérifier si la valeur contient les mots-clés
                value_str = str(obj).lower()
                matched_keywords = []
                
                for keyword in keywords:
                    if keyword.lower() in value_str:
                        matched_keywords.append(keyword)
                
                if matched_keywords:
                    results.append({
                        "database": db_name,
                        "type": "JSON",
                        "path": path,
                        "value": str(obj),
                        "matched_keywords": matched_keywords,
                        "context": self.get_context(data, path)
                    })
        
        search_recursive(data)
        return results
    
    def get_context(self, data: Dict, path: str) -> Dict:
        """Obtient le contexte autour d'une valeur trouvée"""
        try:
            # Essayer de naviguer dans le chemin
            parts = path.split('.')
            current = data
            
            for part in parts:
                if '[' in part:
                    # Gérer les indices de liste
                    key_part = part.split('[')[0]
                    index_part = part.split('[')[1].split(']')[0]
                    current = current[key_part][int(index_part)]
                else:
                    current = current[part]
            
            # Retourner le contexte (l'objet parent)
            return current
        except:
            return {}
    
    def search_in_sqlite_db(self, db_file: Path, keywords: List[str], db_name: str) -> List[Dict]:
        """Recherche dans une base SQLite avec des mots-clés"""
        results = []
        
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Obtenir toutes les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                
                # Obtenir la structure de la table
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                
                # Rechercher dans toutes les colonnes
                for column in column_names:
                    # Construire la requête de recherche
                    conditions = []
                    for keyword in keywords:
                        conditions.append(f"CAST({column} AS TEXT) LIKE '%{keyword}%'")
                    
                    if conditions:
                        query = f"SELECT * FROM {table_name} WHERE {' OR '.join(conditions)}"
                        
                        try:
                            cursor.execute(query)
                            rows = cursor.fetchall()
                            
                            for row in rows:
                                # Trouver les mots-clés correspondants
                                matched_keywords = []
                                for i, value in enumerate(row):
                                    if value:
                                        value_str = str(value).lower()
                                        for keyword in keywords:
                                            if keyword.lower() in value_str:
                                                matched_keywords.append(keyword)
                                
                                if matched_keywords:
                                    # Créer un dictionnaire avec les colonnes
                                    row_dict = dict(zip(column_names, row))
                                    
                                    results.append({
                                        "database": db_name,
                                        "type": "SQLite",
                                        "table": table_name,
                                        "matched_keywords": matched_keywords,
                                        "data": row_dict,
                                        "context": f"Table: {table_name}"
                                    })
                        except Exception as e:
                            continue
            
            conn.close()
            
        except Exception as e:
            console.print(f"[red]Erreur lors de la recherche dans {db_name}: {e}[/red]")
        
        return results
    
    def global_search(self, keywords: Union[str, List[str]], 
                     search_type: str = "AND") -> List[Dict]:
        """
        Recherche globale dans toutes les bases de données
        
        Args:
            keywords: Mots-clés à rechercher (string ou liste)
            search_type: "AND" (tous les mots) ou "OR" (au moins un mot)
        """
        # Normaliser les mots-clés
        if isinstance(keywords, str):
            keywords = [keywords]
        
        # Nettoyer les mots-clés
        keywords = [kw.strip() for kw in keywords if kw.strip()]
        
        if not keywords:
            return []
        
        console.print(f"[blue]🔍 Recherche globale: {', '.join(keywords)} ({search_type})[/blue]")
        
        all_results = []
        databases = self.get_all_databases()
        
        if not databases:
            console.print("[yellow]Aucune base de données trouvée[/yellow]")
            return []
        
        console.print(f"[green]📁 Bases de données trouvées: {len(databases)}[/green]")
        
        for db_name, db_file in databases.items():
            console.print(f"[cyan]Recherche dans {db_name}...[/cyan]")
            
            if db_file.suffix == '.json':
                try:
                    data = self.load_json_db(db_file)
                    results = self.search_in_json_data(data, keywords, db_name)
                    all_results.extend(results)
                except Exception as e:
                    console.print(f"[red]Erreur avec {db_name}: {e}[/red]")
            
            elif db_file.suffix == '.db':
                results = self.search_in_sqlite_db(db_file, keywords, db_name)
                all_results.extend(results)
        
        # Filtrer selon le type de recherche
        if search_type.upper() == "AND":
            # Garder seulement les résultats qui contiennent TOUS les mots-clés
            filtered_results = []
            for result in all_results:
                if search_type.upper() == "AND":
                    if len(result["matched_keywords"]) == len(keywords):
                        filtered_results.append(result)
                else:
                    filtered_results.append(result)
            all_results = filtered_results
        
        console.print(f"[green]✅ {len(all_results)} résultats trouvés[/green]")
        return all_results
    
    def display_results(self, results: List[Dict], max_results: int = 50):
        """Affiche les résultats de recherche de manière formatée"""
        if not results:
            console.print("[yellow]Aucun résultat trouvé[/yellow]")
            return
        
        # Limiter le nombre de résultats
        if len(results) > max_results:
            console.print(f"[yellow]Affichage des {max_results} premiers résultats sur {len(results)}[/yellow]")
            results = results[:max_results]
        
        # Grouper par base de données
        grouped_results = defaultdict(list)
        for result in results:
            grouped_results[result["database"]].append(result)
        
        for db_name, db_results in grouped_results.items():
            console.print(f"\n[bold blue]📊 Base: {db_name}[/bold blue]")
            
            table = Table(title=f"Résultats dans {db_name}")
            table.add_column("Type", style="cyan")
            table.add_column("Mots-clés", style="green")
            table.add_column("Valeur/Données", style="yellow")
            table.add_column("Contexte", style="magenta")
            
            for result in db_results:
                # Formater les données selon le type
                if result["type"] == "JSON":
                    value = result.get("value", "N/A")
                    context = result.get("path", "N/A")
                else:  # SQLite
                    data = result.get("data", {})
                    value = str(data)[:100] + "..." if len(str(data)) > 100 else str(data)
                    context = result.get("context", "N/A")
                
                keywords_str = ", ".join(result["matched_keywords"])
                
                table.add_row(
                    result["type"],
                    keywords_str,
                    value,
                    context
                )
            
            console.print(table)
    
    def search_and_display(self, keywords: Union[str, List[str]], 
                          search_type: str = "AND", max_results: int = 50):
        """Recherche et affiche les résultats"""
        results = self.global_search(keywords, search_type)
        self.display_results(results, max_results)
        return results
    
    def interactive_search(self):
        """Mode de recherche interactif"""
        console.print(Panel(
            "[bold blue]🔍 RECHERCHE GLOBALE INTERACTIVE[/bold blue]\n\n"
            "Entrez vos mots-clés séparés par des espaces.\n"
            "Utilisez 'AND' ou 'OR' pour spécifier le type de recherche.\n"
            "Exemples:\n"
            "  - C24 fm_k (recherche AND par défaut)\n"
            "  - C24 OR fm_k (recherche OR)\n"
            "  - valeur A AND valeur B (recherche AND explicite)\n"
            "  - quit (pour quitter)",
            title="Mode Interactif",
            border_style="blue"
        ))
        
        while True:
            try:
                query = input("\n🔍 Recherche: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    console.print("[green]Au revoir ![/green]")
                    break
                
                if not query:
                    continue
                
                # Parser la requête
                if ' AND ' in query.upper():
                    search_type = "AND"
                    keywords = [kw.strip() for kw in query.upper().split(' AND ')]
                elif ' OR ' in query.upper():
                    search_type = "OR"
                    keywords = [kw.strip() for kw in query.upper().split(' OR ')]
                else:
                    search_type = "AND"
                    keywords = [kw.strip() for kw in query.split()]
                
                # Effectuer la recherche
                self.search_and_display(keywords, search_type)
                
            except KeyboardInterrupt:
                console.print("\n[green]Au revoir ![/green]")
                break
            except Exception as e:
                console.print(f"[red]Erreur: {e}[/red]")

# Instance globale
global_search = GlobalDatabaseSearch()

# Fonctions CLI
def search_global_cli(keywords: str, search_type: str = "AND", max_results: int = 50):
    """Interface CLI pour la recherche globale"""
    if not keywords:
        console.print("[red]Veuillez spécifier des mots-clés[/red]")
        return
    
    keyword_list = [kw.strip() for kw in keywords.split()]
    global_search.search_and_display(keyword_list, search_type, max_results)

def interactive_search_cli():
    """Interface CLI pour la recherche interactive"""
    global_search.interactive_search()

if __name__ == "__main__":
    # Test
    console.print("[bold blue]Test du système de recherche globale[/bold blue]")
    
    # Test 1: Recherche simple
    console.print("\n[bold]Test 1: Recherche 'C24'[/bold]")
    search_global_cli("C24")
    
    # Test 2: Recherche multiple AND
    console.print("\n[bold]Test 2: Recherche 'fm_k AND 24'[/bold]")
    search_global_cli("fm_k 24", "AND")
    
    # Test 3: Recherche multiple OR
    console.print("\n[bold]Test 3: Recherche 'C24 OR GL24h'[/bold]")
    search_global_cli("C24 GL24h", "OR") 