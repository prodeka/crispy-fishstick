#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des bases de données métier
Permet d'interroger les bases de données comme cm_bois.json et autres
"""

import json
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import yaml

console = Console()

class DatabaseManager:
    """Gestionnaire de bases de données métier"""
    
    def __init__(self, db_path: str = "src/lcpi/db"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        self.connections = {}
    
    def load_json_db(self, db_name: str) -> Dict:
        """Charge une base de données JSON (supporte les fichiers multi-JSON)"""
        db_file = self.db_path / f"{db_name}.json"
        if not db_file.exists():
            raise FileNotFoundError(f"Base de données {db_name}.json non trouvée")
        
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
                raise Exception(f"Impossible de parser le fichier JSON {db_name}: {e}")
    
    def search_bois_by_class(self, classe_resistance: str) -> List[Dict]:
        """Recherche des bois par classe de résistance"""
        try:
            # Essayer d'abord le fichier de test, puis le fichier principal
            try:
                db = self.load_json_db("bois_test")
            except FileNotFoundError:
                db = self.load_json_db("cm_bois")
            
            results = []
            # Chercher dans les bois massifs résineux
            if "Valeurs caractéristiques des bois massifs résineux" in db:
                for propriete in db["Valeurs caractéristiques des bois massifs résineux"]:
                    if classe_resistance in propriete.get("Classe", ""):
                        results.append({
                            "type": "Bois massif résineux",
                            "classe": propriete.get("Classe"),
                            "proprietes": propriete
                        })
            
            # Chercher dans les bois lamellés-collés
            if "Valeurs caractéristiques des bois lamellés-collés homogènes" in db:
                for propriete in db["Valeurs caractéristiques des bois lamellés-collés homogènes"]:
                    if classe_resistance in propriete.get("Classe", ""):
                        results.append({
                            "type": "Bois lamellé-collé",
                            "classe": propriete.get("Classe"),
                            "proprietes": propriete
                        })
            
            return results
        except Exception as e:
            console.print(f"[red]Erreur lors de la recherche: {e}[/red]")
            return []
    
    def search_bois_by_property(self, property_name: str, min_value: Optional[float] = None, max_value: Optional[float] = None) -> List[Dict]:
        """Recherche des bois par propriété mécanique"""
        try:
            # Essayer d'abord le fichier de test, puis le fichier principal
            try:
                db = self.load_json_db("bois_test")
            except FileNotFoundError:
                db = self.load_json_db("cm_bois")
            results = []
            
            # Recherche dans tous les types de bois
            for section_name, section_data in db.items():
                if isinstance(section_data, list):
                    for propriete in section_data:
                        if property_name in propriete:
                            try:
                                value = float(propriete[property_name])
                                if min_value is None or value >= min_value:
                                    if max_value is None or value <= max_value:
                                        results.append({
                                            "type": section_name,
                                            "classe": propriete.get("Classe", "N/A"),
                                            "propriete": property_name,
                                            "valeur": value,
                                            "unite": propriete.get("Unité", "N/A")
                                        })
                            except (ValueError, TypeError):
                                continue
            
            return results
        except Exception as e:
            console.print(f"[red]Erreur lors de la recherche: {e}[/red]")
            return []
    
    def compare_materials(self, material_list: List[str]) -> Table:
        """Compare plusieurs matériaux"""
        table = Table(title="Comparaison de Matériaux")
        table.add_column("Propriété", style="cyan")
        
        # Ajouter les colonnes pour chaque matériau
        for material in material_list:
            table.add_column(material, style="green")
        
        # Récupérer les propriétés communes
        try:
            db = self.load_json_db("bois_test")
        except FileNotFoundError:
            db = self.load_json_db("cm_bois")
        common_properties = set()
        
        for section_data in db.values():
            if isinstance(section_data, list):
                for propriete in section_data:
                    if isinstance(propriete, dict):
                        common_properties.update(propriete.keys())
        
        # Filtrer les propriétés numériques
        numeric_properties = []
        for prop in common_properties:
            if prop not in ["Classe", "Désignation", "Unité", "Symbole"]:
                numeric_properties.append(prop)
        
        # Ajouter les lignes de comparaison
        for prop in sorted(numeric_properties):
            row = [prop]
            for material in material_list:
                # Chercher la valeur pour ce matériau
                value = "N/A"
                for section_data in db.values():
                    if isinstance(section_data, list):
                        for propriete in section_data:
                            if propriete.get("Classe") == material and prop in propriete:
                                try:
                                    value = f"{float(propriete[prop]):.2f}"
                                except (ValueError, TypeError):
                                    value = str(propriete[prop])
                                break
                row.append(value)
            table.add_row(*row)
        
        return table
    
    def get_material_info(self, classe: str) -> Dict:
        """Obtient les informations complètes d'un matériau"""
        try:
            try:
                db = self.load_json_db("bois_test")
            except FileNotFoundError:
                db = self.load_json_db("cm_bois")
            
            for section_name, section_data in db.items():
                if isinstance(section_data, list):
                    for propriete in section_data:
                        if propriete.get("Classe") == classe:
                            return {
                                "type": section_name,
                                "classe": classe,
                                "proprietes": propriete
                            }
            
            return {}
        except Exception as e:
            console.print(f"[red]Erreur lors de la récupération: {e}[/red]")
            return {}
    
    def export_to_csv(self, data: List[Dict], filename: str) -> bool:
        """Exporte les données en CSV"""
        try:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8')
            console.print(f"[green]Données exportées vers {filename}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Erreur lors de l'export: {e}[/red]")
            return False
    
    def create_sqlite_db(self, json_db_name: str, sqlite_db_name: str) -> bool:
        """Convertit une base JSON en SQLite pour des requêtes SQL"""
        try:
            json_data = self.load_json_db(json_db_name)
            sqlite_file = self.db_path / f"{sqlite_db_name}.db"
            
            conn = sqlite3.connect(sqlite_file)
            
            # Créer les tables pour chaque section
            for section_name, section_data in json_data.items():
                if isinstance(section_data, list) and section_data:
                    # Créer la table
                    columns = list(section_data[0].keys())
                    table_name = section_name.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_').replace(',', '').replace('%', 'pct').replace('²', '2').replace('³', '3')
                    create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
                    create_sql += ", ".join([f"{col.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_').replace(',', '').replace('%', 'pct').replace('²', '2').replace('³', '3')} TEXT" for col in columns])
                    create_sql += ")"
                    
                    conn.execute(create_sql)
                    
                    # Insérer les données
                    for item in section_data:
                        placeholders = ", ".join(["?" for _ in columns])
                        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
                        values = [str(item.get(col, "")).replace('%', 'pct').replace('²', '2').replace('³', '3') for col in columns]
                        conn.execute(insert_sql, values)
            
            conn.commit()
            conn.close()
            
            console.print(f"[green]Base SQLite créée: {sqlite_file}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Erreur lors de la conversion: {e}[/red]")
            return False
    
    def query_sql(self, sqlite_db_name: str, query: str) -> List[Dict]:
        """Exécute une requête SQL sur une base SQLite"""
        try:
            sqlite_file = self.db_path / f"{sqlite_db_name}.db"
            if not sqlite_file.exists():
                raise FileNotFoundError(f"Base SQLite {sqlite_db_name}.db non trouvée")
            
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Obtenir les noms des colonnes
            columns = [description[0] for description in cursor.description]
            
            # Convertir en liste de dictionnaires
            data = []
            for row in results:
                data.append(dict(zip(columns, row)))
            
            conn.close()
            return data
            
        except Exception as e:
            console.print(f"[red]Erreur lors de la requête SQL: {e}[/red]")
            return []

# Instance globale
db_manager = DatabaseManager()

# Fonctions CLI
def search_bois_cli(classe: Optional[str] = None, propriete: Optional[str] = None, min_val: Optional[float] = None, max_val: Optional[float] = None):
    """Interface CLI pour la recherche de bois"""
    if classe:
        results = db_manager.search_bois_by_class(classe)
        if results:
            table = Table(title=f"Résultats pour la classe {classe}")
            table.add_column("Type", style="cyan")
            table.add_column("Classe", style="green")
            table.add_column("Propriétés", style="yellow")
            
            for result in results:
                table.add_row(
                    result["type"],
                    result["classe"],
                    str(len(result["proprietes"])) + " propriétés"
                )
            
            console.print(table)
        else:
            console.print(f"[yellow]Aucun résultat trouvé pour la classe {classe}[/yellow]")
    
    elif propriete:
        results = db_manager.search_bois_by_property(propriete, min_val, max_val)
        if results:
            table = Table(title=f"Résultats pour {propriete}")
            table.add_column("Type", style="cyan")
            table.add_column("Classe", style="green")
            table.add_column("Valeur", style="yellow")
            table.add_column("Unité", style="magenta")
            
            for result in results:
                table.add_row(
                    result["type"],
                    result["classe"],
                    str(result["valeur"]),
                    result["unite"]
                )
            
            console.print(table)
        else:
            console.print(f"[yellow]Aucun résultat trouvé pour {propriete}[/yellow]")

def compare_materials_cli(materials: List[str]):
    """Interface CLI pour la comparaison de matériaux"""
    if len(materials) < 2:
        console.print("[red]Il faut au moins 2 matériaux pour la comparaison[/red]")
        return
    
    table = db_manager.compare_materials(materials)
    console.print(table)

def export_data_cli(data_type: str, filename: str):
    """Interface CLI pour l'export de données"""
    if data_type == "bois_classes":
        db = db_manager.load_json_db("cm_bois")
        data = []
        for section_name, section_data in db.items():
            if isinstance(section_data, list):
                for item in section_data:
                    if isinstance(item, dict):
                        item["section"] = section_name
                        data.append(item)
        
        db_manager.export_to_csv(data, filename)
    else:
        console.print(f"[red]Type de données {data_type} non supporté[/red]")

def sql_query_cli(db_name: str, query: str):
    """Interface CLI pour les requêtes SQL"""
    results = db_manager.query_sql(db_name, query)
    if results:
        table = Table(title=f"Résultats de la requête SQL")
        
        # Ajouter les colonnes
        if results:
            for col in results[0].keys():
                table.add_column(col, style="cyan")
            
            # Ajouter les lignes
            for row in results:
                table.add_row(*[str(val) for val in row.values()])
        
        console.print(table)
    else:
        console.print("[yellow]Aucun résultat trouvé[/yellow]")

if __name__ == "__main__":
    # Tests
    console.print("[bold blue]Test du gestionnaire de bases de données[/bold blue]")
    
    # Test recherche par classe
    console.print("\n[bold]Recherche bois classe C24:[/bold]")
    search_bois_cli(classe="C24")
    
    # Test recherche par propriété
    console.print("\n[bold]Recherche bois avec fm_k > 20:[/bold]")
    search_bois_cli(propriete="fm_k_MPa", min_val=20)
    
    # Test comparaison
    console.print("\n[bold]Comparaison de matériaux:[/bold]")
    compare_materials_cli(["C24", "C30"])
    
    # Test conversion SQLite
    console.print("\n[bold]Conversion en SQLite:[/bold]")
    db_manager.create_sqlite_db("cm_bois", "cm_bois_sqlite")
    
    # Test requête SQL
    console.print("\n[bold]Requête SQL:[/bold]")
    sql_query_cli("cm_bois_sqlite", "SELECT Classe, fm_k_MPa FROM Valeurs_caractéristiques_des_bois_massifs_résineux WHERE fm_k_MPa > 20") 