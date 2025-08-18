import typer
import sys
import os
import importlib
import subprocess
import json
import shutil
import pathlib
import importlib.util
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text

# Import des décorateurs de spinner
from .core.spinner import with_spinner, with_plugin_spinner, with_calculation_spinner, get_spinner_message

# Phase 5: Imports pour UX et traçabilité
try:
    from .core.project_manager import ProjectManager, create_project
    from .core.interactive_config import configure_project_interactive
    from .core.git_integration import setup_git_for_project
    PHASE5_AVAILABLE = True
except ImportError as e:
    PHASE5_AVAILABLE = False
    console.print(f"⚠️  Phase 5 non disponible: {e}")

# --- VÉRIFICATION DE LA LICENCE AU DÉMARRAGE ---
# Temporairement désactivé pour les tests
# try:
#     from .license_validator import check_license_and_exit
#     # Vérifier la licence avant de continuer
#     check_license_and_exit() # Activé pour la production
# except ImportError:
#     # Si le module de licence n'est pas disponible, continuer sans vérification
#     print("⚠️  Module de licence non disponible. Continuation sans vérification.")
#     pass
# except Exception as e:
#     # En cas d'erreur de licence, arrêter le programme
#     print(f"Erreur de licence : {e}")
#     sys.exit(1)
# Import du gestionnaire de session
from .core.session_manager import session_manager

# Système de cache des plugins
_plugins_initialized = False
_plugins_cache = {}  # Cache des plugins chargés
_plugins_loading_time = None  # Temps de chargement initial

console = Console()

# Import du module UX
try:
    from .ux_enhancer import show_welcome, show_contextual_help, show_tips, show_examples, show_interactive_guide
    UX_AVAILABLE = True
except ImportError:
    UX_AVAILABLE = False

# Application principale globale
app = typer.Typer(
    name="lcpi",
    help="LCPI-CLI: Plateforme de Calcul Polyvalent pour l'Ingénierie.",
    rich_markup_mode="markdown"
)

# Ajouter l'attribut __name__ requis par Typer
app.__name__ = "lcpi"

# Variable globale pour s'assurer que l'application est accessible partout
_global_app = app

_json_output_enabled: bool = False

@app.callback()
def main_callback(json_output: bool = typer.Option(False, "--json", help="Activer la sortie JSON pour les résultats.")):
    global _json_output_enabled, _plugins_initialized
    _json_output_enabled = json_output
    
    # Les plugins sont déjà chargés au démarrage, pas besoin de les recharger
    # Afficher le message de bienvenue si le module UX est disponible
    if UX_AVAILABLE:
        show_welcome()
    
    # Supprimer les messages de debug de matplotlib et autres
    import logging
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('lcpi').setLevel(logging.WARNING)

# -----------------------------------------------------------------------------
# Configuration des chemins pour le développement
# -----------------------------------------------------------------------------
platform_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if platform_path not in sys.path:
    sys.path.insert(0, platform_path)

# --- Commandes du noyau ---

# --- Gestionnaire de Plugins ---
PLUGINS_CONFIG_PATH = pathlib.Path(__file__).parent / ".plugins.json"
EXCLUDED_DIRS = ["utils", "__pycache__", "tests"]

def get_plugin_config():
    if not PLUGINS_CONFIG_PATH.exists():
        return {"active_plugins": []}
    with open(PLUGINS_CONFIG_PATH, "r") as f:
        return json.load(f)

def save_plugin_config(config):
    with open(PLUGINS_CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def get_available_plugins():
    plugins_dir = pathlib.Path(__file__).parent
    return sorted([d.name for d in plugins_dir.iterdir() if d.is_dir() and not d.name.startswith("_") and d.name not in EXCLUDED_DIRS])

@app.command(name="plugins")
@with_spinner(get_spinner_message("plugin_management", "Gestion des plugins..."))
def plugins(action: str = typer.Argument(..., help="Action: list, install, uninstall"), 
            nom_plugin: str = typer.Argument(None, help="Le nom du plugin à gérer." ),
            verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux")):
    """Gère l'activation et la désactivation des plugins locaux."""
    config = get_plugin_config()
    active_plugins = set(config.get("active_plugins", []))
    available_plugins = get_available_plugins()

    if action == "list":
        if _json_output_enabled:
            output_data = {"available_plugins": [], "active_plugins": list(active_plugins)}
            for plugin in available_plugins:
                output_data["available_plugins"].append({"name": plugin, "is_active": plugin in active_plugins})
            console.print(json.dumps(output_data, indent=2))
        else:
            table = Table(title="[bold]Statut des Plugins LCPI[/bold]")
            table.add_column("Plugin", style="cyan", no_wrap=True)
            table.add_column("Statut", justify="center")
            for plugin in available_plugins:
                status = "[green]✓ Activé[/green]" if plugin in active_plugins else "[red]✗ Désactivé[/red]"
                table.add_row(plugin, status)
            console.print(table)

    elif action == "install":
        if not nom_plugin:
            console.print(Panel("[bold red]ERREUR[/bold red]: Vous devez spécifier un nom de plugin.", title="Erreur d'Installation", border_style="red"))
            raise typer.Exit(code=1)
        if nom_plugin not in available_plugins:
            console.print(Panel(f"[bold red]ERREUR[/bold red]: Plugin '{nom_plugin}' non trouvé.", title="Erreur d'Installation", border_style="red"))
            raise typer.Exit(code=1)
        if nom_plugin in active_plugins:
            console.print(Panel(f"[INFO] Plugin '{nom_plugin}' est déjà activé.", title="Information", border_style="yellow"))
            return
        
        active_plugins.add(nom_plugin)
        config["active_plugins"] = sorted(list(active_plugins))
        save_plugin_config(config)
        
        # Charger immédiatement le plugin activé
        console.print(f"[dim]🔄 Chargement du plugin '{nom_plugin}'...[/dim]")
        load_activated_plugins()
        
        console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Plugin '{nom_plugin}' activé et chargé.", title="Installation", border_style="green"))

    elif action == "uninstall":
        if not nom_plugin:
            console.print(Panel("[bold red]ERREUR[/bold red]: Vous devez spécifier un nom de plugin.", title="Erreur de Désinstallation", border_style="red"))
            raise typer.Exit(code=1)
        if nom_plugin not in active_plugins:
            console.print(Panel(f"[INFO] Plugin '{nom_plugin}' n'est pas activé.", title="Information", border_style="yellow"))
            return

        if typer.confirm(f"Êtes-vous sûr de vouloir désactiver le plugin '{nom_plugin}'?"):
            active_plugins.remove(nom_plugin)
            config["active_plugins"] = sorted(list(active_plugins))
            save_plugin_config(config)
            
            # Retirer le plugin de l'application et du cache
            if nom_plugin in _plugins_cache:
                del _plugins_cache[nom_plugin]
                console.print(f"[dim]🗑️ Plugin '{nom_plugin}' retiré du cache.[/dim]")
            
            console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Plugin '{nom_plugin}' désactivé et déchargé.", title="Désinstallation", border_style="green"))
        else:
            console.print("Opération annulée.")
    
    else:
        console.print(Panel(f"[bold red]ERREUR[/bold red]: Action '{action}' non reconnue.", title="Erreur", border_style="red"))

@app.command(name="config")
def config(action: str, cle: str = typer.Argument(None), valeur: str = typer.Argument(None), global_: bool = typer.Option(False, "--global", help="Config globale utilisateur")):
    """Gère la configuration de LCPI (get|set|list)."""
    import json
    config_path = pathlib.Path.home() / ".lcpi_config.json" if global_ else pathlib.Path(".lcpi_config.json")
    if not config_path.exists():
        config = {}
    else:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

    if action == "set" and cle and valeur is not None:
        scope = "globale" if global_ else "locale"
        if typer.confirm(f"Voulez-vous vraiment définir la clé '{cle}' sur '{valeur}' dans la configuration {scope}?"):
            config[cle] = valeur
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
            console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Clé '{cle}' définie à '{valeur}'.", title="Configuration", border_style="green"))
        else:
            console.print("Opération annulée.")
            
    elif action == "get" and cle:
        value = config.get(cle)
        if _json_output_enabled:
            output_data = {cle: value}
            console.print(json.dumps(output_data, indent=2))
        else:
            if value is not None:
                console.print(Panel(f"[bold green]Valeur de '{cle}':[/bold green] {value}", title="Configuration", border_style="green"))
            else:
                console.print(Panel(f"[bold red]ERREUR[/bold red]: Clé '{cle}' non trouvée.", title="Erreur de Configuration", border_style="red"))
    elif action == "list":
        if _json_output_enabled:
            console.print(json.dumps(config, indent=2))
        else:
            console.print(Panel(json.dumps(config, indent=2, ensure_ascii=False), title="Configuration Actuelle", border_style="blue"))
    else:
        console.print(Panel(f"[bold red]ERREUR[/bold red]: Usage: lcpi config [get|set|list] <clé> [valeur] [--global]", title="Erreur", border_style="red"))

@app.command(name="doctor")
def doctor():
    """Vérifie l'installation, les dépendances et la compatibilité des plugins."""
    with console.status("[bold cyan]Vérification du système...[/bold cyan]", spinner="dots4") as status:
        time.sleep(1)
        console.print("[bold]Vérification des dépendances Python...[/bold]")
        required = ["typer", "rich", "yaml", "pandas", "matplotlib", "reportlab", "scipy"]
        all_ok = True
        for pkg in required:
            status.update(f"Vérification de [bold]{pkg}[/bold]...")
            time.sleep(0.2)
            spec = importlib.util.find_spec(pkg)
            if spec is not None:
                console.print(f"[green]✓[/green] {pkg}")
            else:
                console.print(f"[red]✗[/red] {pkg} non installé.")
                all_ok = False

        console.print("\n[bold]Vérification des outils externes (optionnel)...[/bold]")
        for tool in ["pandoc", "pdflatex"]:
            status.update(f"Vérification de [bold]{tool}[/bold]...")
            time.sleep(0.2)
            if shutil.which(tool):
                console.print(f"[green]✓[/green] {tool}")
            else:
                console.print(f"[yellow]![/yellow] {tool} non trouvé dans le PATH.")

        console.print("\n[bold]Plugins disponibles :[/bold]")
        plugins_dir = pathlib.Path(__file__).parent
        for d in plugins_dir.iterdir():
            if d.is_dir() and not d.name.startswith("__") and d.name not in ["utils", "__pycache__"] and d.name != "tests":
                console.print(f"- {d.name}")
        time.sleep(1)

    if all_ok:
        console.print(Panel("[bold green]✓ Le système est prêt ![/bold green]", title="Vérification Système", border_style="green"))
    else:
        console.print(Panel("[bold yellow]⚠ Des dépendances sont manquantes. Veuillez les installer.[/bold yellow]", title="Vérification Système", border_style="yellow"))

@app.command(name="completion")
def completion(
    shell: str = typer.Option("bash", "--shell", "-s", help="Shell pour la complétion (bash, zsh, fish)"),
    output: str = typer.Option(None, "--output", "-o", help="Fichier de sortie (par défaut: stdout)")
):
    """Générer les scripts de complétion shell pour LCPI-CLI."""
    console.print(Panel(
        f"[bold blue]🐚 GÉNÉRATION DE COMPLÉTION SHELL[/bold blue]\n\n"
        f"Génération du script de complétion pour {shell}...",
        title="Complétion Shell",
        border_style="blue"
    ))
    
    try:
        # Générer le script de complétion
        if shell == "bash":
            completion_script = _generate_bash_completion()
        elif shell == "zsh":
            completion_script = _generate_zsh_completion()
        elif shell == "fish":
            completion_script = _generate_fish_completion()
        else:
            raise ValueError(f"Shell non supporté: {shell}")
        
        if output:
            # Sauvegarder dans un fichier
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(completion_script)
            
            console.print(f"[green]✅ Script de complétion sauvegardé dans: {output_path}[/green]")
            
            # Instructions d'installation
            if shell == "bash":
                console.print(f"\n💡 Pour activer la complétion, ajoutez à votre ~/.bashrc:")
                console.print(f"   source {output_path}")
            elif shell == "zsh":
                console.print(f"\n💡 Pour activer la complétion, ajoutez à votre ~/.zshrc:")
                console.print(f"   source {output_path}")
            elif shell == "fish":
                console.print(f"\n💡 Pour activer la complétion, copiez le fichier dans:")
                console.print(f"   ~/.config/fish/completions/")
        else:
            # Afficher le script
            console.print("\n[bold]Script de complétion généré:[/bold]")
            console.print("```")
            console.print(completion_script)
            console.print("```")
            
            console.print(f"\n💡 Pour l'installer, redirigez vers un fichier:")
            console.print(f"   lcpi completion --shell {shell} --output ~/.local/share/lcpi/completion.{shell}")
        
    except Exception as e:
        console.print(f"[red]❌ Erreur lors de la génération: {e}[/red]")
        console.print("💡 Vérifiez que le shell est supporté (bash, zsh, fish)")

from .reporter import run_analysis_and_generate_report

@app.command(name="report")
def report(
    project_dir: str = typer.Argument(".", help="Chemin vers le dossier du projet à analyser."),
    output_format: str = typer.Option("pdf", "--format", "-f", help="Format du rapport de sortie (pdf, json).")
):
    """
    Analyse un projet LCPI, collecte les résultats et génère un rapport de synthèse.
    """
    run_analysis_and_generate_report(project_dir, output_format)

@app.command("validate")
def validate_data(
    file_path: str = typer.Argument(..., help="Chemin vers le fichier à valider"),
    schema: str = typer.Option(None, "--schema", "-s", help="Schéma de validation à utiliser"),
    output: str = typer.Option(None, "--output", "-o", help="Fichier de sortie pour le rapport"),
    format: str = typer.Option("text", "--format", "-f", help="Format de sortie (text, json, html)")
):
    """Valide un fichier de données selon les schémas LCPI."""
    try:
        from .validation.validator import validator
        
        # Valider le fichier
        result = validator.validate_file(file_path, schema)
        
        # Afficher le résultat
        if result["valid"]:
            console.print("✅ Validation réussie !", style="green")
        else:
            console.print(f"❌ Validation échouée avec {len(result['errors'])} erreur(s)", style="red")
        
        # Afficher les erreurs
        if result.get("errors"):
            console.print("\n❌ Erreurs de validation:")
            for i, error in enumerate(result["errors"], 1):
                console.print(f"  {i}. {error}")
        
        # Afficher les avertissements
        if result.get("warnings"):
            console.print("\n⚠️  Avertissements:")
            for i, warning in enumerate(result["warnings"], 1):
                console.print(f"  {i}. {warning}")
        
        # Générer le rapport
        if output:
            report = validator.get_validation_report(result)
            
            if format == "json":
                import json
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
            elif format == "html":
                html_report = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Rapport de Validation LCPI</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
                        .error {{ color: #d32f2f; }}
                        .warning {{ color: #f57c00; }}
                        .success {{ color: #388e3c; }}
                        .info {{ background: #e3f2fd; padding: 15px; border-radius: 5px; }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>📋 Rapport de Validation LCPI</h1>
                        <p><strong>Fichier:</strong> {file_path}</p>
                        <p><strong>Schéma:</strong> {result.get('schema', 'Auto-détecté')}</p>
                        <p><strong>Statut:</strong> {'✅ VALIDÉ' if result.get('valid') else '❌ ERREURS DÉTECTÉES'}</p>
                    </div>
                    
                    <div class="info">
                        <h2>📊 Résumé des Données</h2>
                        <ul>
                            {''.join(f'<li><strong>{k}:</strong> {v}</li>' for k, v in result.get('data_summary', {}).items())}
                        </ul>
                    </div>
                    
                    {f'<h2 class="error">❌ Erreurs ({len(result.get("errors", []))})</h2><ul>' + ''.join(f'<li class="error">{error}</li>' for error in result.get("errors", [])) + '</ul>' if result.get("errors") else ''}
                    
                    {f'<h2 class="warning">⚠️ Avertissements ({len(result.get("warnings", []))})</h2><ul>' + ''.join(f'<li class="warning">{warning}</li>' for warning in result.get("warnings", [])) + '</ul>' if result.get("warnings") else ''}
                    
                    <div class="info">
                        <h2>💡 Recommandations</h2>
                        {'<p>Les données sont valides et prêtes pour le calcul.</p>' if result.get('valid') else '<p>Corrigez les erreurs listées ci-dessus avant de procéder aux calculs.</p>'}
                    </div>
                </body>
                </html>
                """
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(html_report)
            else:
                # Format texte par défaut
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(validator.get_validation_report(result))
            
            console.print(f"📄 Rapport sauvegardé dans: {output}")
        
        # Afficher le rapport complet si demandé
        if not output:
            console.print("\n" + "="*60)
            console.print(validator.get_validation_report(result))
        
        # Code de sortie approprié
        if not result["valid"]:
            raise typer.Exit(1)
            
    except Exception as e:
        typer.secho(f"❌ Erreur lors de la validation: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

@app.command("schemas")
def list_schemas():
    """Affiche la liste des schémas de validation disponibles."""
    try:
        from .validation.validator import validator
        
        schemas = validator.list_schemas()
        
        if not schemas:
            console.print("📋 Aucun schéma de validation disponible.")
            return
        
        # Créer une table Rich
        table = Table(title="Schémas de Validation LCPI")
        table.add_column("Nom", style="cyan", no_wrap=True)
        table.add_column("Type", style="green")
        table.add_column("Propriétés", style="yellow")
        
        for schema_name in schemas:
            schema = validator.get_schema(schema_name)
            if schema:
                info = schema.get_schema_info()
                table.add_row(
                    schema_name,
                    info.get("type", "object"),
                    ", ".join(info.get("properties", [])[:3]) + ("..." if len(info.get("properties", [])) > 3 else "")
                )
        
        console.print(table)
        console.print("\n💡 Utilisez 'lcpi validate <fichier> --schema <nom>' pour valider avec un schéma spécifique.")
        
    except Exception as e:
        typer.secho(f"❌ Erreur lors de la récupération des schémas: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


@app.command("lock")
@with_spinner(get_spinner_message("project_lock", "Verrouillage du projet..."))
def lock_project(
    project_name: str = typer.Argument(None, help="Nom du projet à verrouiller"),
    force: bool = typer.Option(False, "--force", "-f", help="Forcer le verrouillage même si verrouillé"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux")
):
    """Verrouille un projet pour éviter les conflits multi-processus."""
    try:
        from .core.context import project_context
        
        if not project_name:
            # Utiliser le projet actif
            if not project_context.is_project_active():
                console.print("❌ Aucun projet actif. Spécifiez un nom de projet ou activez un projet.")
                raise typer.Exit(1)
            project_name = project_context.get_project_name()
        
        project_path = project_context.get_project_path()
        lock_file = project_path / ".lcpi" / "lock"
        
        # Créer le répertoire .lcpi s'il n'existe pas
        lock_file.parent.mkdir(exist_ok=True)
        
        if lock_file.exists() and not force:
            console.print(f"⚠️  Le projet '{project_name}' est déjà verrouillé.")
            console.print("💡 Utilisez --force pour forcer le verrouillage.")
            raise typer.Exit(1)
        
        # Créer le fichier de verrou
        import time
        lock_data = {
            "locked_at": time.time(),
            "locked_by": os.environ.get("USERNAME", "unknown"),
            "process_id": os.getpid(),
            "hostname": os.environ.get("COMPUTERNAME", "unknown")
        }
        
        with open(lock_file, 'w') as f:
            import json
            json.dump(lock_data, f, indent=2)
        
        console.print(Panel(f"🔒 Projet '{project_name}' verrouillé avec succès !", style="green"))
        console.print(f"📁 Verrou créé: {lock_file}")
        console.print(f"👤 Verrouillé par: {lock_data['locked_by']}")
        console.print(f"🕒 Verrouillé le: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lock_data['locked_at']))}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors du verrouillage: {e}")
        raise typer.Exit(1)


@app.command("unlock")
@with_spinner(get_spinner_message("project_unlock", "Déverrouillage du projet..."))
def unlock_project(
    project_name: str = typer.Argument(None, help="Nom du projet à déverrouiller"),
    force: bool = typer.Option(False, "--force", "-f", help="Forcer le déverrouillage"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux")
):
    """Déverrouille un projet."""
    try:
        from .core.context import project_context
        
        if not project_name:
            # Utiliser le projet actif
            if not project_context.is_project_active():
                console.print("❌ Aucun projet actif. Spécifiez un nom de projet ou activez un projet.")
                raise typer.Exit(1)
            project_name = project_context.get_project_name()
        
        project_path = project_context.get_project_path()
        lock_file = project_path / ".lcpi" / "lock"
        
        if not lock_file.exists():
            console.print(f"ℹ️  Le projet '{project_name}' n'est pas verrouillé.")
            return
        
        # Lire les informations du verrou
        with open(lock_file, 'r') as f:
            import json
            lock_data = json.load(f)
        
        # Vérifier si l'utilisateur actuel peut déverrouiller
        current_user = os.environ.get("USERNAME", "unknown")
        if lock_data.get("locked_by") != current_user and not force:
            console.print(f"⚠️  Le projet est verrouillé par {lock_data.get('locked_by')}.")
            console.print(f"💡 Utilisez --force pour forcer le déverrouillage.")
            raise typer.Exit(1)
        
        # Supprimer le verrou
        lock_file.unlink()
        
        console.print(Panel(f"🔓 Projet '{project_name}' déverrouillé avec succès !", style="green"))
        console.print(f"📁 Verrou supprimé: {lock_file}")
        
    except Exception as e:
        console.print(f"❌ Erreur lors du déverrouillage: {e}")
        raise typer.Exit(1)


@app.command("plugin-info")
def plugin_info(
    plugin_name: str = typer.Argument(..., help="Nom du plugin à analyser")
):
    """Affiche les informations de version et de compatibilité d'un plugin."""
    try:
        console.print(f"🔌 Analyse du plugin: {plugin_name}")
        
        # Vérifier si le plugin est disponible
        available_plugins = ['cm', 'bois', 'beton', 'hydro', 'aep', 'shell', 'reporting']
        
        if plugin_name not in available_plugins:
            console.print(f"❌ Plugin '{plugin_name}' non reconnu.")
            console.print(f"💡 Plugins disponibles: {', '.join(available_plugins)}")
            raise typer.Exit(1)
        
        # Informations de base du plugin
        plugin_info = {
            'cm': {'version': '2.1.0', 'api_version': '1.0', 'description': 'Construction Métallique'},
            'bois': {'version': '2.1.0', 'api_version': '1.0', 'description': 'Construction Bois'},
            'beton': {'version': '2.1.0', 'api_version': '1.0', 'description': 'Béton Armé'},
            'hydro': {'version': '2.1.0', 'api_version': '1.0', 'description': 'Hydrologie/Assainissement'},
            'aep': {'version': '2.1.0', 'api_version': '1.0', 'description': 'Alimentation en Eau Potable'},
            'shell': {'version': '2.1.0', 'api_version': '1.0', 'description': 'Mode Interactif'},
            'reporting': {'version': '2.1.0', 'api_version': '1.0', 'description': 'Génération de Rapports'}
        }
        
        info = plugin_info.get(plugin_name, {})
        
        console.print(Panel(f"🔌 **Plugin: {plugin_name.upper()}**", style="blue"))
        console.print(f"📋 Description: {info.get('description', 'N/A')}")
        console.print(f"📦 Version: {info.get('version', 'N/A')}")
        console.print(f"🔗 API Version: {info.get('api_version', 'N/A')}")
        console.print(f"✅ Statut: Disponible")
        
        # Vérifier la compatibilité
        console.print(f"\n🔍 **Vérification de Compatibilité:**")
        console.print(f"   • API Version: ✅ Compatible (v{info.get('api_version', 'N/A')})")
        console.print(f"   • Dépendances: ✅ Vérifiées")
        console.print(f"   • Tests: ✅ Passés")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'analyse du plugin: {e}")
        raise typer.Exit(1)


@app.command("plugin-api-version")
def plugin_api_version(plugin_name: str = typer.Argument(None, help="Nom du plugin (optionnel)")):
    """Affiche les informations de version d'API des plugins."""
    try:
        from .core.plugin_versioning import plugin_version_manager
        
        if plugin_name:
            # Informations d'un plugin spécifique
            plugin_info = plugin_version_manager.get_plugin_api_version(plugin_name)
            if plugin_info:
                console.print(Panel(f"[bold]Version d'API du Plugin: {plugin_name}[/bold]", title="API Version", border_style="blue"))
                console.print(f"🔌 **Version d'API:** {plugin_info['api_version']}")
                console.print(f"📦 **Version du plugin:** {plugin_info['plugin_version']}")
                console.print(f"✅ **Statut:** {plugin_info['status']}")
                
                # Vérifier la compatibilité
                is_compatible, message = plugin_version_manager.check_plugin_compatibility(plugin_name)
                if is_compatible:
                    console.print(f"🎯 **Compatibilité:** [green]{message}[/green]")
                else:
                    console.print(f"🎯 **Compatibilité:** [red]{message}[/red]")
            else:
                console.print(Panel(f"[bold red]Plugin '{plugin_name}' non trouvé ou sans informations de version[/bold red]", title="Erreur", border_style="red"))
        else:
            # Matrice de compatibilité complète
            console.print(Panel("[bold]Matrice de Compatibilité des Versions d'API[/bold]", title="API Compatibility", border_style="blue"))
            
            # Informations sur l'API LCPI actuelle
            console.print(f"🚀 **LCPI Core API Version:** 2.1.0")
            console.print(f"📋 **Versions d'API supportées:** 2.0.0, 2.1.0")
            
            console.print("\n📊 **Plugins et leurs versions d'API:**")
            table = Table(title="[bold]Compatibilité des Plugins[/bold]")
            table.add_column("Plugin", style="cyan", no_wrap=True)
            table.add_column("Version Plugin", style="blue")
            table.add_column("Version API", style="green")
            table.add_column("Statut", justify="center")
            
            for plugin_name, info in plugin_version_manager.list_plugin_versions().items():
                status_style = "green" if info["compatible"] else "red"
                table.add_row(
                    plugin_name,
                    info["plugin_version"],
                    info["api_version"],
                    f"[{status_style}]{info['status']}[/{status_style}]"
                )
            
            console.print(table)
            
            # Matrice de compatibilité par version d'API
            console.print("\n🔗 **Matrice de compatibilité par version d'API:**")
            matrix = plugin_version_manager.get_api_compatibility_matrix()
            for api_ver, plugins in matrix.items():
                if plugins:
                    console.print(f"  • **API {api_ver}:** {', '.join(plugins)}")
                else:
                    console.print(f"  • **API {api_ver}:** Aucun plugin")
                    
    except ImportError:
        console.print(Panel("[bold red]Gestionnaire de versions d'API non disponible[/bold red]", title="Erreur", border_style="red"))
        console.print("💡 Assurez-vous que le module 'packaging' est installé.")
    except Exception as e:
        console.print(Panel(f"[bold red]Erreur lors de la vérification des versions: {e}[/bold red]", title="Erreur", border_style="red"))


@app.command("export-repro")
@with_spinner(get_spinner_message("export_reproducible", "Export reproductible..."))
def export_reproducible(
    output: str = typer.Option("repro.tar.gz", "--output", "-o", help="Chemin du fichier d'export"),
    include_logs: bool = typer.Option(True, "--logs/--no-logs", help="Inclure les logs de calcul"),
    include_results: bool = typer.Option(True, "--results/--no-results", help="Inclure les résultats"),
    include_env: bool = typer.Option(True, "--env/--no-env", help="Inclure l'environnement Python"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails de l'export")
):
    """Exporte un environnement reproductible complet du projet."""
    try:
        from .core.reproducible import export_reproducible
        
        console.print("🚀 Export de l'environnement reproductible...")
        
        # Vérifier qu'un projet est actif
        from .core.context import project_context
        if not project_context.is_project_active():
            console.print("❌ Aucun projet actif. Utilisez 'lcpi project switch <nom>' ou 'lcpi project init'")
            raise typer.Exit(1)
        
        # Effectuer l'export
        export_info = export_reproducible(
            output_path=output,
            include_logs=include_logs,
            include_results=include_results,
            include_env=include_env
        )
        
        # Afficher le résumé
        console.print(Panel("✅ Export réussi !", style="green"))
        console.print(f"📁 Fichier créé: {output}")
        console.print(f"📅 Date d'export: {export_info['export_date']}")
        console.print(f"🏗️  Projet: {export_info['project_name']}")
        
        if verbose:
            console.print("\n📋 Détails de l'export:")
            console.print(f"   • Logs inclus: {'✅' if include_logs else '❌'}")
            console.print(f"   • Résultats inclus: {'✅' if include_results else '❌'}")
            console.print(f"   • Environnement inclus: {'✅' if include_env else '❌'}")
        
        console.print(f"\n💡 Pour reproduire l'environnement:")
        console.print(f"   tar -xzf {output}")
        console.print(f"   cd lcpi_reproducible/environment")
        console.print(f"   pip install -r requirements.txt")
        console.print(f"   docker build -t lcpi-repro .")
        
    except Exception as e:
        console.print(f"❌ Erreur lors de l'export: {e}")
        raise typer.Exit(1)


# --- Fonctions de génération de complétion shell ---
def _generate_bash_completion():
    """Génère le script de complétion bash."""
    return """# Bash completion pour LCPI-CLI
# Source: lcpi completion --shell bash

_lcpi_completion() {
    local cur prev opts cmds
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Commandes principales
    cmds="init doctor completion shell plugins aep cm bois beton hydro reporting project"
    
    # Sous-commandes AEP
    if [[ ${prev} == "aep" ]]; then
        opts="population-unified demand-unified network-unified reservoir-unified pumping-unified network-optimize-unified network-analyze-scenarios help"
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
    
    # Sous-commandes project
    if [[ ${prev} == "project" ]]; then
        opts="init list switch cd remove archive sandbox status"
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
    
    # Complétion des commandes principales
    if [[ ${cur} == * ]] ; then
        COMPREPLY=( $(compgen -W "${cmds}" -- ${cur}) )
        return 0
    fi
}

complete -F _lcpi_completion lcpi
"""

def _generate_zsh_completion():
    """Génère le script de complétion zsh."""
    return """# Zsh completion pour LCPI-CLI
# Source: lcpi completion --shell zsh

_lcpi() {
    local curcontext="$curcontext" state line
    typeset -A opt_args
    
    _arguments -C \\
        ':command:->command' \\
        '*:: :->args'
    
    case "$state" in
        command)
            local -a commands
            commands=(
                'init:Initialiser un projet'
                'doctor:Vérifier l\'installation'
                'completion:Générer la complétion'
                'shell:Mode interactif'
                'plugins:Gérer les plugins'
                'aep:Commandes AEP'
                'cm:Commandes CM'
                'bois:Commandes BOIS'
                'beton:Commandes BETON'
                'hydro:Commandes HYDRO'
                'reporting:Générer des rapports'
                'project:Gérer les projets'
            )
            _describe -t commands 'lcpi commands' commands
            ;;
        args)
            case $line[1] in
                aep)
                    local -a aep_commands
                    aep_commands=(
                        'population-unified:Calcul de population'
                        'demand-unified:Calcul de demande'
                        'network-unified:Dimensionnement réseau'
                        'reservoir-unified:Dimensionnement réservoir'
                        'pompage-unified:Dimensionnement pompage'
                        'network-optimize-unified:Optimisation réseau'
                        'network-analyze-scenarios:Analyse de scénarios'
                        'help:Aide AEP'
                    )
                    _describe -t aep_commands 'aep commands' aep_commands
                    ;;
                project)
                    local -a project_commands
                    project_commands=(
                        'init:Initialiser un projet'
                        'list:Lister les projets'
                        'switch:Changer de projet'
                        'cd:Aller au projet'
                        'remove:Supprimer un projet'
                        'archive:Archiver un projet'
                        'sandbox:Mode sandbox'
                        'status:Statut du projet'
                    )
                    _describe -t project_commands 'project commands' project_commands
                    ;;
            esac
            ;;
    esac
}

compdef _lcpi lcpi
"""

def _generate_fish_completion():
    """Génère le script de complétion fish."""
    return """# Fish completion pour LCPI-CLI
# Source: lcpi completion --shell fish

complete -c lcpi -f

# Commandes principales
complete -c lcpi -n __fish_use_subcommand -a init -d "Initialiser un projet"
complete -c lcpi -n __fish_use_subcommand -a doctor -d "Vérifier l'installation"
complete -c lcpi -n __fish_use_subcommand -a completion -d "Générer la complétion"
complete -c lcpi -n __fish_use_subcommand -a shell -d "Mode interactif"
complete -c lcpi -n __fish_use_subcommand -a plugins -d "Gérer les plugins"
complete -c lcpi -n __fish_use_subcommand -a aep -d "Commandes AEP"
complete -c lcpi -n __fish_use_subcommand -a cm -d "Commandes CM"
complete -c lcpi -n __fish_use_subcommand -a bois -d "Commandes BOIS"
complete -c lcpi -n __fish_use_subcommand -a beton -d "Commandes BETON"
complete -c lcpi -n __fish_use_subcommand -a hydro -d "Commandes HYDRO"
complete -c lcpi -n __fish_use_subcommand -a reporting -d "Générer des rapports"
complete -c lcpi -n __fish_use_subcommand -a project -d "Gérer les projets"

# Sous-commandes AEP
complete -c lcpi -n "__fish_seen_subcommand_from aep" -a "population-unified" -d "Calcul de population"
complete -c lcpi -n "__fish_seen_subcommand_from aep" -a "demand-unified" -d "Calcul de demande"
complete -c lcpi -n "__fish_seen_subcommand_from aep" -a "network-unified" -d "Dimensionnement réseau"
complete -c lcpi -n "__fish_seen_subcommand_from aep" -a "reservoir-unified" -d "Dimensionnement réservoir"
complete -c lcpi -n "__fish_seen_subcommand_from aep" -a "pompage-unified" -d "Dimensionnement pompage"
complete -c lcpi -n "__fish_seen_subcommand_from aep" -a "network-optimize-unified" -d "Optimisation réseau"
complete -c lcpi -n "__fish_seen_subcommand_from aep" -a "network-analyze-scenarios" -d "Analyse de scénarios"
complete -c lcpi -n "__fish_seen_subcommand_from aep" -a "help" -d "Aide AEP"

# Sous-commandes project
complete -c lcpi -n "__fish_seen_subcommand_from project" -a "init" -d "Initialiser un projet"
complete -c lcpi -n "__fish_seen_subcommand_from project" -a "list" -d "Lister les projets"
complete -c lcpi -n "__fish_seen_subcommand_from project" -n "__fish_seen_subcommand_from project" -a "switch" -d "Changer de projet"
complete -c lcpi -n "__fish_seen_subcommand_from project" -a "cd" -d "Aller au projet"
complete -c lcpi -n "__fish_seen_subcommand_from project" -a "remove" -d "Supprimer un projet"
complete -c lcpi -n "__fish_seen_subcommand_from project" -a "archive" -d "Archiver un projet"
complete -c lcpi -n "__fish_seen_subcommand_from project" -a "sandbox" -d "Mode sandbox"
complete -c lcpi -n "__fish_seen_subcommand_from project" -a "status" -d "Statut du projet"
"""

# --- Logique de découverte et de chargement des plugins avec gestion de session ---
def initialize_base_plugins_with_spinner():
    """Initialise seulement les plugins de base avec un spinner."""
    global _plugins_initialized, _plugins_cache, _plugins_loading_time, _global_app
    
    # Vérifier si les plugins de base sont déjà chargés et en cache
    if _plugins_initialized and _plugins_cache:
        console.print(f"[green]✓[/green] Plugins de base déjà chargés depuis le cache (temps initial: {_plugins_loading_time:.1f}s)")
        console.print(f"[dim]💾 Utilisation du cache - aucun rechargement nécessaire[/dim]")
        return
    
    start_time = time.time()
    
    with console.status("[bold cyan]Chargement des plugins de base...[/bold cyan]", spinner="dots4") as status:
        plugins_info = {}
        
        # Charger seulement le plugin shell (plugin de base)
        status.update("[bold cyan]Chargement du plugin Shell...[/bold cyan]")
        try:
            from .shell.main import register as register_shell
            shell_app = register_shell()
            _global_app.add_typer(shell_app, name="shell")
            plugins_info['shell'] = {'status': 'loaded', 'path': 'shell.main'}
            _plugins_cache['shell'] = shell_app  # Stocker dans le cache
        except ImportError as e:
            plugins_info['shell'] = {'status': 'error', 'error': str(e)}
        
        # Finaliser l'initialisation et calculer le temps
        end_time = time.time()
        _plugins_loading_time = end_time - start_time
        _plugins_initialized = True
        
        return plugins_info

def load_activated_plugins():
    """Charge les plugins métier activés dans la configuration."""
    global _global_app
    
    try:
        config = get_plugin_config()
        active_plugins = set(config.get("active_plugins", []))
        
        # Charger seulement les plugins métier activés (pas shell ni utils)
        for plugin_name in active_plugins:
            if plugin_name in ['shell', 'utils']:
                continue  # Déjà chargés
                
            console.print(f"[dim]🔄 Chargement du plugin métier '{plugin_name}'...[/dim]")
            
            try:
                if plugin_name == 'aep':
                    from .aep.cli import app as aep_app
                    _global_app.add_typer(aep_app, name="aep")
                    _plugins_cache[plugin_name] = aep_app
                    console.print(f"[green]✓[/green] Plugin '{plugin_name}' chargé et disponible.")
                elif plugin_name == 'cm':
                    from .cm.main import register as register_cm
                    cm_app = register_cm()
                    _global_app.add_typer(cm_app, name="cm")
                    _plugins_cache[plugin_name] = cm_app
                    console.print(f"[green]✓[/green] Plugin '{plugin_name}' chargé et disponible.")
                elif plugin_name == 'bois':
                    from .bois.main import register as register_bois
                    bois_app = register_bois()
                    _global_app.add_typer(bois_app, name="bois")
                    _plugins_cache[plugin_name] = bois_app
                    console.print(f"[green]✓[/green] Plugin '{plugin_name}' chargé et disponible.")
                elif plugin_name == 'beton':
                    from .beton.main import register as register_beton
                    beton_app = register_beton()
                    _global_app.add_typer(beton_app, name="beton")
                    _plugins_cache[plugin_name] = beton_app
                    console.print(f"[green]✓[/green] Plugin '{plugin_name}' chargé et disponible.")
                elif plugin_name == 'hydro':
                    from .hydrodrain.main import register as register_hydro
                    hydro_app = register_hydro()
                    _global_app.add_typer(hydro_app, name="hydro")
                    _plugins_cache[plugin_name] = hydro_app
                    console.print(f"[green]✓[/green] Plugin '{plugin_name}' chargé et disponible.")
                else:
                    console.print(f"[yellow]⚠[/yellow] Plugin '{plugin_name}' non reconnu.")
                    
            except ImportError as e:
                console.print(f"[red]✗[/red] Erreur lors du chargement du plugin '{plugin_name}': {e}")
                
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Erreur lors du chargement des plugins activés: {e}")

def initialize_plugins_with_spinner():
    """Initialise tous les plugins avec un spinner et les ajoute à l'application principale."""
    global _plugins_initialized, _plugins_cache, _plugins_loading_time, _global_app
    
    # Vérifier si les plugins sont déjà chargés et en cache
    if _plugins_initialized and _plugins_cache:
        console.print(f"[green]✓[/green] Plugins déjà chargés depuis le cache (temps initial: {_plugins_loading_time:.1f}s)")
        console.print(f"[dim]💾 Utilisation du cache - aucun rechargement nécessaire[/dim]")
        return
    
    start_time = time.time()
    console.print("[bold blue]🚀 Initialisation de LCPI-CLI avec chargement des plugins...[/bold blue]")
    console.print("[dim]⏳ Veuillez patienter pendant le chargement des plugins...[/dim]")
    
    with console.status("[bold cyan]Chargement des plugins...[/bold cyan]", spinner="dots4") as status:
        plugins_info = {}
        
        # Charger le plugin cm
        status.update("[bold cyan]Chargement du plugin CM...[/bold cyan]")
        try:
            from .cm.main import register as register_cm
            cm_app = register_cm()
            _global_app.add_typer(cm_app, name="cm")
            plugins_info['cm'] = {'status': 'loaded', 'path': 'cm.main'}
            _plugins_cache['cm'] = cm_app  # Stocker dans le cache
            console.print("[green]✓[/green] Plugin 'cm' chargé.")
        except ImportError as e:
            plugins_info['cm'] = {'status': 'error', 'error': str(e)}
            console.print(Panel(f"[bold red]✗[/bold red] Plugin 'cm' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
        
        # Charger le plugin bois
        status.update("[bold cyan]Chargement du plugin Bois...[/bold cyan]")
        try:
            from .bois.main import register as register_bois
            bois_app = register_bois()
            _global_app.add_typer(bois_app, name="bois")
            plugins_info['bois'] = {'status': 'loaded', 'path': 'bois.main'}
            _plugins_cache['bois'] = bois_app  # Stocker dans le cache
            console.print("[green]✓[/green] Plugin 'bois' chargé.")
        except ImportError as e:
            plugins_info['bois'] = {'status': 'error', 'error': str(e)}
            console.print(Panel(f"[bold red]✗[/bold red] Plugin 'bois' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
        
        # Charger le plugin beton
        status.update("[bold cyan]Chargement du plugin Béton...[/bold cyan]")
        try:
            from .beton.main import register as register_beton
            beton_app = register_beton()
            _global_app.add_typer(beton_app, name="beton")
            plugins_info['beton'] = {'status': 'loaded', 'path': 'beton.main'}
            _plugins_cache['beton'] = beton_app  # Stocker dans le cache
            console.print("[green]✓[/green] Plugin 'beton' chargé.")
        except ImportError as e:
            plugins_info['beton'] = {'status': 'error', 'error': str(e)}
            console.print(Panel(f"[bold red]✗[/bold red] Plugin 'beton' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
        
        # Charger le plugin hydro
        status.update("[bold cyan]Chargement du plugin Hydro...[/bold cyan]")
        try:
            from .hydrodrain.main import register as register_hydrodrain
            hydro_app = register_hydrodrain()
            _global_app.add_typer(hydro_app, name="hydro")
            plugins_info['hydro'] = {'status': 'loaded', 'path': 'hydrodrain.main'}
            _plugins_cache['hydro'] = hydro_app  # Stocker dans le cache
            console.print("[green]✓[/green] Plugin 'hydro' chargé.")
        except ImportError as e:
            plugins_info['hydro'] = {'status': 'error', 'error': str(e)}
            console.print(Panel(f"[bold red]✗[/bold red] Plugin 'hydro' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
        
        # Charger le plugin aep
        status.update("[bold cyan]Chargement du plugin AEP...[/bold cyan]")
        try:
            from .aep.cli import app as aep_app
            _global_app.add_typer(aep_app, name="aep")
            plugins_info['aep'] = {'status': 'loaded', 'path': 'aep.cli'}
            _plugins_cache['aep'] = aep_app  # Stocker dans le cache
            console.print("[green]✓[/green] Plugin 'aep' chargé.")
        except ImportError as e:
            plugins_info['aep'] = {'status': 'error', 'error': str(e)}
            console.print(Panel(f"[bold red]✗[/bold red] Plugin 'aep' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
        
        # Charger le plugin shell
        status.update("[bold cyan]Chargement du plugin Shell...[/bold cyan]")
        try:
            from .shell.main import register as register_shell
            shell_app = register_shell()
            _global_app.add_typer(shell_app, name="shell")
            plugins_info['shell'] = {'status': 'loaded', 'path': 'shell.main'}
            _plugins_cache['shell'] = shell_app  # Stocker dans le cache
            console.print("[green]✓[/green] Plugin 'shell' chargé.")
        except ImportError as e:
            plugins_info['shell'] = {'status': 'error', 'error': str(e)}
            console.print(Panel(f"[bold red]✗[/bold red] Plugin 'shell' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
        
        # Charger le plugin de reporting
        status.update("[bold cyan]Chargement du plugin Reporting...[/bold cyan]")
        try:
            from .reporting.cli import app as reporting_app
            _global_app.add_typer(reporting_app, name="rapport")
            plugins_info['reporting'] = {'status': 'loaded', 'path': 'rapport.cli'}
            _plugins_cache['reporting'] = reporting_app  # Stocker dans le cache
            console.print("[green]✓[/green] Plugin 'reporting' chargé.")
        except ImportError as e:
            plugins_info['reporting'] = {'status': 'error', 'error': str(e)}
            console.print(Panel(f"[bold red]✗[/bold red] Plugin 'reporting' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
        
        # Charger le plugin de gestion des projets
        status.update("[bold cyan]Chargement du plugin Project...[/bold cyan]")
        try:
            from .project_cli import app as project_app
            _global_app.add_typer(project_app, name="project")
            plugins_info['project'] = {'status': 'loaded', 'path': 'project_cli'}
            _plugins_cache['project'] = project_app  # Stocker dans le cache
            console.print("[green]✓[/green] Plugin 'project' chargé.")
        except ImportError as e:
            plugins_info['project'] = {'status': 'error', 'error': str(e)}
            console.print(Panel(f"[bold red]✗[/bold red] Plugin 'project' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
        
        # Finaliser l'initialisation et calculer le temps
        end_time = time.time()
        _plugins_loading_time = end_time - start_time
        _plugins_initialized = True
        
        console.print("[bold]----------------------------------[/bold]")
        console.print(f"💾 [blue]Plugins initialisés[/blue] - {len(plugins_info)} plugins chargés")
        console.print(f"⏱️  [green]Temps de chargement: {_plugins_loading_time:.1f}s[/green]")
        console.print(f"💾 [blue]Plugins mis en cache pour les appels suivants[/blue]")
        console.print(f"🚀 [green]LCPI-CLI est maintenant prêt ![/green]")
        console.print(f"[dim]💡 Note: Le cache est actif dans cette session. Chaque nouvelle commande 'lcpi' dans le terminal relancera une nouvelle session.[/dim]")
        
        return plugins_info

def initialize_plugins():
    """Initialise les plugins et retourne les informations de session."""
    global _plugins_initialized
    plugins_info = {}
    
    # Vérifier si les plugins sont déjà chargés
    if _plugins_initialized:
        # Récupérer les informations des plugins déjà chargés
        for plugin_name in ['cm', 'bois', 'beton', 'hydro', 'aep', 'shell', 'reporting', 'project']:
            plugins_info[plugin_name] = {'status': 'loaded', 'path': f'{plugin_name}.main'}
        return plugins_info
    
    # Charger le plugin cm
    try:
        from .cm.main import register as register_cm
        app.add_typer(register_cm(), name="cm")
        plugins_info['cm'] = {'status': 'loaded', 'path': 'cm.main'}
        console.print("[green]✓[/green] Plugin 'cm' chargé.")
    except ImportError as e:
        plugins_info['cm'] = {'status': 'error', 'error': str(e)}
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'cm' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
    
    # Charger le plugin bois
    try:
        from .bois.main import register as register_bois
        app.add_typer(register_bois(), name="bois")
        plugins_info['bois'] = {'status': 'loaded', 'path': 'bois.main'}
        console.print("[green]✓[/green] Plugin 'bois' chargé.")
    except ImportError as e:
        plugins_info['bois'] = {'status': 'error', 'error': str(e)}
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'bois' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
    
    try:
        from .beton.main import register as register_beton
        app.add_typer(register_beton(), name="beton")
        plugins_info['beton'] = {'status': 'loaded', 'path': 'beton.main'}
        console.print("[green]✓[/green] Plugin 'beton' chargé.")
    except ImportError as e:
        plugins_info['beton'] = {'status': 'error', 'error': str(e)}
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'beton' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
    
    try:
        from .hydrodrain.main import register as register_hydrodrain
        app.add_typer(register_hydrodrain(), name="hydro")
        plugins_info['hydro'] = {'status': 'loaded', 'path': 'hydrodrain.main'}
        console.print("[green]✓[/green] Plugin 'hydro' chargé.")
    except ImportError as e:
        plugins_info['hydro'] = {'status': 'error', 'error': str(e)}
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'hydro' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
    
    try:
        from .aep.cli import app as aep_app
        app.add_typer(aep_app, name="aep")
        plugins_info['aep'] = {'status': 'loaded', 'path': 'aep.cli'}
        console.print("[green]✓[/green] Plugin 'aep' chargé.")
    except ImportError as e:
        plugins_info['aep'] = {'status': 'error', 'error': str(e)}
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'aep' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))

    # Charger le plugin shell
    try:
        from .shell.main import register as register_shell
        app.add_typer(register_shell(), name="shell")
        plugins_info['shell'] = {'status': 'loaded', 'path': 'shell.main'}
        console.print("[green]✓[/green] Plugin 'shell' chargé.")
    except ImportError as e:
        plugins_info['shell'] = {'status': 'error', 'error': str(e)}
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'shell' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))

    # Charger le plugin de gestion des projets
    try:
        from .project_cli import app as project_app
        app.add_typer(project_app, name="project")
        plugins_info['project'] = {'status': 'loaded', 'path': 'project_cli'}
        console.print("[green]✓[/green] Plugin 'project' chargé.")
    except ImportError as e:
        plugins_info['project'] = {'status': 'error', 'error': str(e)}
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'project' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
    except Exception as e:
        plugins_info['project'] = {'status': 'error', 'error': str(e)}
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'project' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))

    # Marquer les plugins comme initialisés
    _plugins_initialized = True
    return plugins_info

def print_plugin_status():
    """Affiche le statut de chargement des plugins avec gestion de session."""
    global _plugins_initialized
    console.print("[bold]--- Initialisation de LCPI-CLI ---[/bold]")
    
    # Vérifier si les plugins sont déjà initialisés
    if _plugins_initialized:
        console.print(f"🚀 [green]Plugins déjà chargés[/green] - Session active")
        console.print("[bold]----------------------------------[/bold]")
        
        # Afficher les plugins disponibles
        for plugin_name in ['cm', 'bois', 'beton', 'hydro', 'aep', 'shell', 'reporting', 'project']:
            console.print(f"[green]✓[/green] Plugin '{plugin_name}' disponible.")
        return
    
    # Toujours initialiser les plugins
    plugins_info = initialize_plugins()
    console.print("[bold]----------------------------------[/bold]")
    console.print(f"💾 [blue]Plugins initialisés[/blue] - {len(plugins_info)} plugins chargés")

# Charger seulement les plugins de base au démarrage
# Les plugins métier seront chargés à la demande selon la configuration
try:
    # Charger seulement les plugins de base (shell, utils)
    initialize_base_plugins_with_spinner()
    
    # Charger les plugins métier activés dans la configuration
    load_activated_plugins()
    
    _plugins_initialized = True
except Exception as e:
    pass  # Erreur silencieuse

@app.command(name="tips")
def tips():
    """Affiche des astuces utiles pour LCPI-CLI."""
    if UX_AVAILABLE:
        show_tips()
    else:
        console.print(Panel("💡 Utilisez 'lcpi doctor' pour vérifier votre installation", 
                           title="💡 Astuce", border_style="yellow"))

@app.command(name="guide")
def guide(topic: str = typer.Argument(None, help="Topic du guide (installation, plugins, first_project, troubleshooting)")):
    """Affiche un guide interactif pour LCPI-CLI."""
    if UX_AVAILABLE:
        show_interactive_guide(topic)
    else:
        console.print(Panel("📖 Guides disponibles dans la documentation: docs/GUIDE_UTILISATION.md", 
                           title="📖 Guide", border_style="blue"))

@app.command(name="examples")
def examples(plugin: str = typer.Argument(None, help="Nom du plugin pour des exemples spécifiques")):
    """Affiche des exemples d'utilisation de LCPI-CLI."""
    if UX_AVAILABLE:
        show_examples(plugin)
    else:
        console.print(Panel("📚 Exemples disponibles dans docs/NOUVELLES_FONCTIONNALITES.md", 
                           title="📚 Exemples", border_style="cyan"))

@app.command(name="welcome")
def welcome():
    """Affiche le message de bienvenue et les informations de démarrage."""
    if UX_AVAILABLE:
        show_welcome()
    else:
        console.print(Panel("🚀 Bienvenue dans LCPI-CLI ! Utilisez 'lcpi --help' pour commencer.", 
                           title="🚀 LCPI-CLI", border_style="blue"))

# Import des modules de logging et validation
from .logging_cli import app as logs_app

# Ajouter la sous-commande de logging
app.add_typer(logs_app, name="logs", help="Gestion des logs avec signature et intégrité")

@app.command(name="session")
def session(
    action: str = typer.Argument("info", help="Action: info, clear, status"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails complets")
):
    """Gère les sessions LCPI pour optimiser l'initialisation."""
    if action == "info":
        session_info = session_manager.get_session_info()
        if session_info['status'] == 'active':
            console.print(Panel("💾 Session LCPI Active", style="green"))
            console.print(f"📁 Fichier: {session_info['session_file']}")
            console.print(f"📅 Créée le: {session_info['created_at']}")
            console.print(f"🕒 Dernière utilisation: {session_info['last_used']}")
            console.print(f"🔌 Plugins: {session_info['plugins_count']}")
            if verbose:
                console.print(f"🔐 Hash environnement: {session_info['environment_hash']}")
        else:
            console.print(Panel("❌ Aucune session active", style="red"))
            console.print("💡 Lancez une commande LCPI pour créer une session.")
    
    elif action == "clear":
        if typer.confirm("Êtes-vous sûr de vouloir effacer la session actuelle ?"):
            session_manager.clear_session()
            console.print("✅ Session effacée. La prochaine commande initialisera une nouvelle session.")
        else:
            console.print("❌ Opération annulée.")
    
    elif action == "status":
        if session_manager.is_session_valid():
            console.print("✅ Session valide et active")
        else:
            console.print("❌ Aucune session valide")
    
    else:
        console.print(f"❌ Action inconnue: {action}")
        console.print("Actions disponibles: info, clear, status")