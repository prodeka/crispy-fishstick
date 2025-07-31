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
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# --- VÉRIFICATION DE LA LICENCE AU DÉMARRAGE ---
try:
    from .license_validator import check_license_and_exit
    # Vérifier la licence avant de continuer
    check_license_and_exit() # Activé pour la production
except ImportError:
    # Si le module de licence n'est pas disponible, continuer sans vérification
    print("⚠️  Module de licence non disponible. Continuation sans vérification.")
    pass
except Exception as e:
    # En cas d'erreur de licence, arrêter le programme
    print(f"Erreur de licence : {e}")
    sys.exit(1)

# Force UTF-8 encoding for stdout and stderr
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

console = Console()

# Import du module UX
try:
    from .ux_enhancer import show_welcome, show_contextual_help, show_tips, show_examples, show_interactive_guide
    UX_AVAILABLE = True
except ImportError:
    UX_AVAILABLE = False

app = typer.Typer(
    name="lcpi",
    help="LCPI-CLI: Plateforme de Calcul Polyvalent pour l'Ingénierie.",
    rich_markup_mode="markdown"
)

_json_output_enabled: bool = False

@app.callback()
def main_callback(json_output: bool = typer.Option(False, "--json", help="Activer la sortie JSON pour les résultats.")):
    global _json_output_enabled
    _json_output_enabled = json_output
    
    # Afficher le message de bienvenue si le module UX est disponible
    if UX_AVAILABLE:
        show_welcome()

# -----------------------------------------------------------------------------
# Configuration des chemins pour le développement
# -----------------------------------------------------------------------------
platform_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if platform_path not in sys.path:
    sys.path.insert(0, platform_path)

# --- Commandes du noyau ---
@app.command()
def init(nom_projet: str = typer.Argument("nouveau_projet_lcpi"), template: str = typer.Option(None, "--template", help="Nom du template à utiliser.")):
    """Initialise un nouveau projet LCPI."""
    project_path = pathlib.Path(nom_projet)
    if project_path.exists():
        console.print(Panel(f"[bold red]ERREUR[/bold red]: Le dossier '{nom_projet}' existe déjà.", title="Erreur d'Initialisation", border_style="red"))
        return
    project_path.mkdir(parents=True)
    if template:
        console.print(Panel(f"[INFO] Clonage du template '{template}' dans '{nom_projet}'.", title="Initialisation", border_style="yellow"))
    else:
        console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Projet '{nom_projet}' initialisé.", title="Initialisation", border_style="green"))

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

@app.command()
def plugins(action: str = typer.Argument(..., help="Action: list, install, uninstall"), 
            nom_plugin: str = typer.Argument(None, help="Le nom du plugin à gérer." )):
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
        console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Plugin '{nom_plugin}' activé.", title="Installation", border_style="green"))

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
            console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Plugin '{nom_plugin}' désactivé.", title="Désinstallation", border_style="green"))
        else:
            console.print("Opération annulée.")
    
    else:
        console.print(Panel(f"[bold red]ERREUR[/bold red]: Action '{action}' non reconnue.", title="Erreur", border_style="red"))

@app.command()
def config(action: str, cle: str = typer.Argument(None), valeur: str = typer.Argument(None), global_: bool = typer.Option(False, "--global", help="Config globale utilisateur." )):
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

@app.command()
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

from .reporter import run_analysis_and_generate_report

@app.command()
def report(
    project_dir: str = typer.Argument(".", help="Chemin vers le dossier du projet à analyser."),
    output_format: str = typer.Option("pdf", "--format", "-f", help="Format du rapport de sortie (pdf, json).")
):
    """
    Analyse un projet LCPI, collecte les résultats et génère un rapport de synthèse.
    """
    run_analysis_and_generate_report(project_dir, output_format)


# --- Logique de découverte et de chargement des plugins (VERSION CORRIGÉE) ---
def print_plugin_status():
    console.print("[bold]--- Initialisation de LCPI-CLI ---[/bold]")
    # Charger les plugins de base
    try:
        from .cm.main import register as register_cm
        app.add_typer(register_cm(), name="cm")
        console.print("[green]✓[/green] Plugin 'cm' chargé.")
    except ImportError as e:
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'cm' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
    try:
        from .bois.main import register as register_bois
        app.add_typer(register_bois(), name="bois")
        console.print("[green]✓[/green] Plugin 'bois' chargé.")
    except ImportError as e:
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'bois' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
    try:
        from .beton.main import register as register_beton
        app.add_typer(register_beton(), name="beton")
        console.print("[green]✓[/green] Plugin 'beton' chargé.")
    except ImportError as e:
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'beton' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))
    try:
        from .hydrodrain.main import register as register_hydrodrain
        app.add_typer(register_hydrodrain(), name="hydro")
        console.print("[green]✓[/green] Plugin 'hydro' chargé.")
    except ImportError as e:
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'hydro' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))

    # Charger le plugin shell
    try:
        from .shell.main import register as register_shell
        register_shell(app)
        console.print("[green]✓[/green] Plugin 'shell' chargé.")
    except ImportError as e:
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'shell' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))

    console.print("[bold]----------------------------------[/bold]")

# Appel de la fonction pour enregistrer les plugins au démarrage
# On vérifie la variable d'environnement pour un lancement "core only"
if os.getenv('LCPI_CORE_ONLY_LAUNCH') != '1':
    print_plugin_status()

@app.command()
def tips():
    """Affiche des astuces utiles pour LCPI-CLI."""
    if UX_AVAILABLE:
        show_tips()
    else:
        console.print(Panel("💡 Utilisez 'lcpi doctor' pour vérifier votre installation", 
                           title="💡 Astuce", border_style="yellow"))

@app.command()
def guide(topic: str = typer.Argument(None, help="Topic du guide (installation, plugins, first_project, troubleshooting)")):
    """Affiche un guide interactif pour LCPI-CLI."""
    if UX_AVAILABLE:
        show_interactive_guide(topic)
    else:
        console.print(Panel("📖 Guides disponibles dans la documentation: docs/GUIDE_UTILISATION.md", 
                           title="📖 Guide", border_style="blue"))

@app.command()
def examples(plugin: str = typer.Argument(None, help="Nom du plugin pour des exemples spécifiques")):
    """Affiche des exemples d'utilisation de LCPI-CLI."""
    if UX_AVAILABLE:
        show_examples(plugin)
    else:
        console.print(Panel("📚 Exemples disponibles dans docs/NOUVELLES_FONCTIONNALITES.md", 
                           title="📚 Exemples", border_style="cyan"))

@app.command()
def welcome():
    """Affiche le message de bienvenue et les informations de démarrage."""
    if UX_AVAILABLE:
        show_welcome()
    else:
        console.print(Panel("🚀 Bienvenue dans LCPI-CLI ! Utilisez 'lcpi --help' pour commencer.", 
                           title="🚀 LCPI-CLI", border_style="blue"))