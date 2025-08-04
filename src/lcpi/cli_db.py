#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Commandes CLI pour l'interrogation des bases de données métier
"""

import typer
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from .db_manager import db_manager, search_bois_cli, compare_materials_cli, export_data_cli, sql_query_cli

console = Console()
app = typer.Typer(name="db", help="Gestion des bases de données métier")

@app.command()
def search(
    classe: Optional[str] = typer.Option(None, "--classe", "-c", help="Classe de résistance à rechercher"),
    propriete: Optional[str] = typer.Option(None, "--propriete", "-p", help="Propriété mécanique à rechercher"),
    min_val: Optional[float] = typer.Option(None, "--min", help="Valeur minimale pour la propriété"),
    max_val: Optional[float] = typer.Option(None, "--max", help="Valeur maximale pour la propriété")
):
    """Recherche dans les bases de données de matériaux"""
    if not classe and not propriete:
        console.print(Panel(
            "[red]Erreur: Spécifiez soit --classe soit --propriete[/red]\n"
            "Exemples:\n"
            "  lcpi db search --classe C24\n"
            "  lcpi db search --propriete fm_k_MPa --min 20\n"
            "  lcpi db search --propriete E0_mean_KN_mm2 --min 10 --max 15",
            title="Aide - Recherche",
            border_style="red"
        ))
        return
    
    search_bois_cli(classe=classe, propriete=propriete, min_val=min_val, max_val=max_val)

@app.command()
def compare(
    materials: List[str] = typer.Argument(..., help="Liste des matériaux à comparer")
):
    """Compare plusieurs matériaux"""
    if len(materials) < 2:
        console.print(Panel(
            "[red]Erreur: Il faut au moins 2 matériaux pour la comparaison[/red]\n"
            "Exemple: lcpi db compare C24 C30 GL24h",
            title="Aide - Comparaison",
            border_style="red"
        ))
        return
    
    compare_materials_cli(materials)

@app.command()
def info(
    classe: str = typer.Argument(..., help="Classe de matériau à consulter")
):
    """Affiche les informations détaillées d'un matériau"""
    info = db_manager.get_material_info(classe)
    if info:
        console.print(Panel(
            f"[bold green]Informations pour {classe}[/bold green]\n"
            f"Type: {info['type']}\n"
            f"Classe: {info['classe']}\n"
            f"Nombre de propriétés: {len(info['proprietes'])}",
            title="Informations Matériau",
            border_style="green"
        ))
        
        # Afficher les propriétés dans un tableau
        from rich.table import Table
        table = Table(title=f"Propriétés de {classe}")
        table.add_column("Propriété", style="cyan")
        table.add_column("Valeur", style="green")
        table.add_column("Unité", style="yellow")
        
        for key, value in info['proprietes'].items():
            if key not in ["Classe", "Désignation"]:
                table.add_row(key, str(value), info['proprietes'].get("Unité", "N/A"))
        
        console.print(table)
    else:
        console.print(f"[red]Matériau {classe} non trouvé[/red]")

@app.command()
def export(
    data_type: str = typer.Argument(..., help="Type de données à exporter (bois_classes, ...)"),
    filename: str = typer.Option("export.csv", "--output", "-o", help="Nom du fichier de sortie")
):
    """Exporte les données en CSV"""
    export_data_cli(data_type, filename)

@app.command()
def convert(
    json_db: str = typer.Argument(..., help="Nom de la base JSON (sans extension)"),
    sqlite_name: Optional[str] = typer.Option(None, "--name", "-n", help="Nom de la base SQLite (défaut: json_db_sqlite)")
):
    """Convertit une base JSON en SQLite pour requêtes SQL"""
    if not sqlite_name:
        sqlite_name = f"{json_db}_sqlite"
    
    success = db_manager.create_sqlite_db(json_db, sqlite_name)
    if success:
        console.print(f"[green]Base SQLite créée: {sqlite_name}.db[/green]")
        console.print("Vous pouvez maintenant utiliser: lcpi db sql --db " + sqlite_name + " --query 'SELECT * FROM table'")
    else:
        console.print("[red]Erreur lors de la conversion[/red]")

@app.command()
def sql(
    db_name: str = typer.Option(..., "--db", "-d", help="Nom de la base SQLite"),
    query: str = typer.Option(..., "--query", "-q", help="Requête SQL à exécuter")
):
    """Exécute une requête SQL sur une base SQLite"""
    sql_query_cli(db_name, query)

@app.command()
def list():
    """Liste les bases de données disponibles"""
    db_path = db_manager.db_path
    
    console.print(Panel(
        "[bold blue]Bases de données disponibles:[/bold blue]",
        title="Bases de Données",
        border_style="blue"
    ))
    
    json_files = list(db_path.glob("*.json"))
    sqlite_files = list(db_path.glob("*.db"))
    
    if json_files:
        console.print("\n[bold green]Bases JSON:[/bold green]")
        for file in json_files:
            console.print(f"  📄 {file.stem}")
    
    if sqlite_files:
        console.print("\n[bold green]Bases SQLite:[/bold green]")
        for file in sqlite_files:
            console.print(f"  🗄️  {file.stem}")
    
    if not json_files and not sqlite_files:
        console.print("[yellow]Aucune base de données trouvée[/yellow]")

@app.command()
def examples():
    """Affiche des exemples d'utilisation"""
    console.print(Panel(
        "[bold blue]Exemples d'utilisation:[/bold blue]\n\n"
        "[green]Recherche par classe:[/green]\n"
        "  lcpi db search --classe C24\n"
        "  lcpi db search --classe GL24h\n\n"
        "[green]Recherche par propriété:[/green]\n"
        "  lcpi db search --propriete fm_k_MPa --min 20\n"
        "  lcpi db search --propriete E0_mean_KN_mm2 --min 10 --max 15\n\n"
        "[green]Comparaison de matériaux:[/green]\n"
        "  lcpi db compare C24 C30 GL24h\n\n"
        "[green]Informations détaillées:[/green]\n"
        "  lcpi db info C24\n\n"
        "[green]Export de données:[/green]\n"
        "  lcpi db export bois_classes --output bois_data.csv\n\n"
        "[green]Conversion et requêtes SQL:[/green]\n"
        "  lcpi db convert cm_bois\n"
        "  lcpi db sql --db cm_bois_sqlite --query \"SELECT Classe, fm_k_MPa FROM Valeurs_caractéristiques_des_bois_massifs_résineux WHERE fm_k_MPa > 20\"",
        title="Exemples d'Utilisation",
        border_style="blue"
    ))

if __name__ == "__main__":
    app() 