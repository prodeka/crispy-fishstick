#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Commandes CLI pour la recherche globale dans toutes les bases de données
"""

import typer
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from .db_global_search import global_search, search_global_cli, interactive_search_cli

console = Console()
app = typer.Typer(name="search", help="Recherche globale dans toutes les bases de données")

@app.command()
def global(
    keywords: str = typer.Argument(..., help="Mots-clés à rechercher (séparés par des espaces)"),
    search_type: str = typer.Option("AND", "--type", "-t", help="Type de recherche: AND ou OR"),
    max_results: int = typer.Option(50, "--max", "-m", help="Nombre maximum de résultats à afficher")
):
    """Recherche globale dans toutes les bases de données"""
    search_global_cli(keywords, search_type, max_results)

@app.command()
def interactive():
    """Mode de recherche interactif"""
    interactive_search_cli()

@app.command()
def databases():
    """Liste toutes les bases de données disponibles"""
    databases = global_search.get_all_databases()
    
    if not databases:
        console.print("[yellow]Aucune base de données trouvée[/yellow]")
        return
    
    console.print(Panel(
        f"[bold blue]Bases de données disponibles: {len(databases)}[/bold blue]",
        title="Bases de Données",
        border_style="blue"
    ))
    
    json_dbs = []
    sqlite_dbs = []
    
    for db_name, db_file in databases.items():
        if db_file.suffix == '.json':
            json_dbs.append(db_name)
        elif db_file.suffix == '.db':
            sqlite_dbs.append(db_name)
    
    if json_dbs:
        console.print("\n[bold green]📄 Bases JSON:[/bold green]")
        for db_name in json_dbs:
            console.print(f"  📄 {db_name}")
    
    if sqlite_dbs:
        console.print("\n[bold green]🗄️ Bases SQLite:[/bold green]")
        for db_name in sqlite_dbs:
            console.print(f"  🗄️ {db_name}")

@app.command()
def examples():
    """Affiche des exemples d'utilisation"""
    console.print(Panel(
        "[bold blue]Exemples d'utilisation de la recherche globale:[/bold blue]\n\n"
        "[green]Recherche simple:[/green]\n"
        "  lcpi search global C24\n"
        "  lcpi search global \"fm_k_MPa\"\n\n"
        "[green]Recherche multiple AND (tous les mots):[/green]\n"
        "  lcpi search global \"C24 fm_k\" --type AND\n"
        "  lcpi search global \"valeur A valeur B\"\n\n"
        "[green]Recherche multiple OR (au moins un mot):[/green]\n"
        "  lcpi search global \"C24 GL24h\" --type OR\n"
        "  lcpi search global \"bois massif OR lamellé\"\n\n"
        "[green]Mode interactif:[/green]\n"
        "  lcpi search interactive\n\n"
        "[green]Lister les bases:[/green]\n"
        "  lcpi search databases\n\n"
        "[yellow]Syntaxe dans le mode interactif:[/yellow]\n"
        "  - C24 fm_k (recherche AND par défaut)\n"
        "  - C24 OR fm_k (recherche OR)\n"
        "  - valeur A AND valeur B (recherche AND explicite)\n"
        "  - quit (pour quitter)",
        title="Exemples d'Utilisation",
        border_style="blue"
    ))

@app.command()
def quick(
    query: str = typer.Argument(..., help="Requête rapide (mots-clés séparés par des espaces)")
):
    """Recherche rapide avec paramètres par défaut"""
    search_global_cli(query, "AND", 20)

if __name__ == "__main__":
    app() 