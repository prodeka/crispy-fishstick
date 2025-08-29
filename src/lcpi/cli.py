import sys
import os

# Ajouter le répertoire parent au path pour les imports relatifs
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Ajouter le répertoire src au path pour permettre l'exécution depuis la racine
project_root = os.path.dirname(parent_dir)
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    from lcpi.main import app
except ImportError:
    # Fallback pour l'installation pip
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    try:
        from lcpi.main import app
    except ImportError:
        # Dernier fallback : essayer d'importer directement depuis le répertoire courant
        sys.path.insert(0, current_dir)
        from main import app

import typer
from typing import Optional, List

def main():
    """Point d'entrée principal pour l'application CLI"""
    try:
        app()
    except Exception as e:
        print(f"❌ Erreur lors du lancement de LCPI-CLI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

@app.command()
def db_global_search(
    search_term: str = typer.Argument(..., help="Terme de recherche"),
    plugins: Optional[str] = typer.Option(None, "--plugins", "-p", help="Plugins à rechercher (séparés par des virgules)"),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, csv, markdown)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """Recherche globale dans toutes les bases de données"""
    try:
        from .db.db_manager import global_search
        
        # Parser les plugins
        plugin_list = None
        if plugins:
            plugin_list = [p.strip() for p in plugins.split(",")]
        
        # Exécuter la recherche
        results = global_search(search_term, plugin_list)
        
        if verbose:
            typer.echo(f"🔍 Recherche globale: {search_term}")
            typer.echo(f"📊 Résultats: {len(results)} trouvés")
            if plugin_list:
                typer.echo(f"🎯 Plugins: {', '.join(plugin_list)}")
        
        if results:
            # Exporter les résultats
            from .db.db_manager import create_global_database_manager
            manager = create_global_database_manager()
            
            if output_format == "json":
                import json
                typer.echo(json.dumps(results, indent=2, ensure_ascii=False))
            elif output_format == "csv":
                csv_content = manager.export_results(results, "csv")
                typer.echo(csv_content)
            elif output_format == "markdown":
                md_content = manager.export_results(results, "markdown")
                typer.echo(md_content)
            else:
                typer.echo(f"❌ Format non supporté: {output_format}")
        else:
            typer.echo(f"❌ Aucun résultat trouvé pour: {search_term}")
            
    except Exception as e:
        typer.echo(f"❌ Erreur lors de la recherche globale: {e}", err=True)

@app.command()
def db_query(
    plugin: str = typer.Argument(..., help="Plugin (aep, cm_bois, bois, etc.)"),
    query_type: str = typer.Argument(..., help="Type de requête"),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, csv, markdown)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """Requête spécifique par plugin"""
    try:
        from .db.db_manager import query_database
        
        # Exécuter la requête
        results = query_database(plugin, query_type)
        
        if verbose:
            typer.echo(f"🔍 Requête: {plugin}.{query_type}")
            typer.echo(f"📊 Résultats: {len(results)} trouvés")
        
        if results:
            # Exporter les résultats
            from .db.db_manager import create_global_database_manager
            manager = create_global_database_manager()
            
            if output_format == "json":
                import json
                typer.echo(json.dumps(results, indent=2, ensure_ascii=False))
            elif output_format == "csv":
                csv_content = manager.export_results(results, "csv")
                typer.echo(csv_content)
            elif output_format == "markdown":
                md_content = manager.export_results(results, "markdown")
                typer.echo(md_content)
            else:
                typer.echo(f"❌ Format non supporté: {output_format}")
        else:
            typer.echo(f"❌ Aucun résultat trouvé pour: {plugin}.{query_type}")
            
    except Exception as e:
        typer.echo(f"❌ Erreur lors de la requête: {e}", err=True)

@app.command()
def db_autocomplete(
    query: str = typer.Argument(..., help="Requête pour l'auto-complétion"),
    plugins: Optional[str] = typer.Option(None, "--plugins", "-p", help="Plugins à considérer (séparés par des virgules)"),
    limit: int = typer.Option(10, "--limit", "-l", help="Nombre maximum de suggestions")
):
    """Génère des suggestions d'auto-complétion globales"""
    try:
        from .db.db_manager import get_global_autocomplete_options
        
        # Parser les plugins
        plugin_list = None
        if plugins:
            plugin_list = [p.strip() for p in plugins.split(",")]
        
        options = get_global_autocomplete_options(query, plugin_list)
        
        if options:
            typer.echo(f"💡 Suggestions pour '{query}':")
            for i, option in enumerate(options[:limit], 1):
                typer.echo(f"   {i}. {option}")
        else:
            typer.echo(f"❌ Aucune suggestion trouvée pour '{query}'")
            
    except Exception as e:
        typer.echo(f"❌ Erreur lors de l'auto-complétion: {e}", err=True)

# Auto-complétion globale
def get_global_autocomplete(ctx: typer.Context, incomplete: str) -> List[str]:
    """Auto-complétion globale pour toutes les commandes"""
    suggestions = []
    
    # Commandes principales
    main_commands = [
        "help", "version", "doctor", "plugins", "shell", "tips",
        "aep", "cm", "bois", "beton", "hydro", "db"
    ]
    
    # Commandes AEP
    aep_commands = [
        "population", "demande", "reseau", "reservoir", "pompage",
        "hardy-cross-csv", "hardy-cross-yaml", "hardy-cross-help"
    ]
    
    # Commandes CM
    cm_commands = [
        "section", "resistance", "assemblage", "calcul"
    ]
    
    # Commandes Bois
    bois_commands = [
        "poteau", "poutre", "assemblage", "verification"
    ]
    
    # Commandes Béton
    beton_commands = [
        "poteau", "poutre", "fondation", "ferraillage"
    ]
    
    # Commandes Hydro
    hydro_commands = [
        "pluvio", "bassin", "ouvrage", "util", "plomberie", "stockage", "collector", "reservoir"
    ]
    
    # Commandes DB
    db_commands = [
        "global-search", "query", "autocomplete", "export"
    ]
    
    # Filtrer selon le contexte
    if ctx.command.name == "aep":
        suggestions.extend([cmd for cmd in aep_commands if incomplete.lower() in cmd.lower()])
    elif ctx.command.name == "cm":
        suggestions.extend([cmd for cmd in cm_commands if incomplete.lower() in cmd.lower()])
    elif ctx.command.name == "bois":
        suggestions.extend([cmd for cmd in bois_commands if incomplete.lower() in cmd.lower()])
    elif ctx.command.name == "beton":
        suggestions.extend([cmd for cmd in beton_commands if incomplete.lower() in cmd.lower()])
    elif ctx.command.name == "hydro":
        suggestions.extend([cmd for cmd in hydro_commands if incomplete.lower() in cmd.lower()])
    elif ctx.command.name == "db":
        suggestions.extend([cmd for cmd in db_commands if incomplete.lower() in cmd.lower()])
    else:
        suggestions.extend([cmd for cmd in main_commands if incomplete.lower() in cmd.lower()])
    
    return suggestions

if __name__ == "__main__":
    main()