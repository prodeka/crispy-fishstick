import typer
import sys
import os
import importlib
import subprocess
import json
from .reporter import generate_pdf_report
import shutil
import pathlib
import importlib.util

app = typer.Typer(
    name="lcpi",
    help="LCPI-CLI: Plateforme de Calcul Polyvalent pour l'Ingénierie.",
    rich_markup_mode="markdown"
)

# -----------------------------------------------------------------------------
# Configuration des chemins pour le développement
# -----------------------------------------------------------------------------
# On s'assure que le dossier `lcpi_platform` est dans le path
# pour que `from lcpi.cm ...` fonctionne.
platform_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if platform_path not in sys.path:
    sys.path.insert(0, platform_path)

# --- Commandes du noyau (placeholders) ---
@app.command()
def init(nom_projet: str = typer.Argument("nouveau_projet_lcpi"), template: str = typer.Option(None, "--template", help="Nom du template à utiliser.")):
    """Initialise un nouveau projet LCPI (optionnellement à partir d'un template)."""
    project_path = pathlib.Path(nom_projet)
    if project_path.exists():
        print(f"[ERREUR] Le dossier '{nom_projet}' existe déjà.")
        return
    project_path.mkdir(parents=True)
    if template:
        print(f"[INFO] (Simulation) Clonage du template '{template}' dans '{nom_projet}'.")
        # Ici, on pourrait copier un dossier template réel si disponible
    else:
        print(f"[SUCCES] Projet '{nom_projet}' initialisé.")

@app.command()
def plugins(action: str = typer.Argument(..., help="Action à effectuer : list, install, uninstall, search, update."), nom_plugin: str = typer.Argument(None)):
    """Gère le cycle de vie des plugins."""
    plugins_dir = pathlib.Path(__file__).parent / "lcpi"
    if action == "list":
        print("Plugins installés :")
        for d in plugins_dir.iterdir():
            if d.is_dir() and not d.name.startswith("__"):
                print(f"- {d.name}")
    elif action == "install" and nom_plugin:
        print(f"[SIMULATION] Installation du plugin '{nom_plugin}' (utiliser pip ou un registre réel ici).")
    elif action == "uninstall" and nom_plugin:
        print(f"[SIMULATION] Désinstallation du plugin '{nom_plugin}'.")
    elif action == "search" and nom_plugin:
        print(f"[SIMULATION] Recherche du plugin '{nom_plugin}' sur le registre.")
    elif action == "update" and nom_plugin:
        print(f"[SIMULATION] Mise à jour du plugin '{nom_plugin}'.")
    else:
        print("Usage : lcpi plugins <list|install|uninstall|search|update> [nom-plugin]")

@app.command()
def config(action: str, cle: str = typer.Argument(None), valeur: str = typer.Argument(None), global_: bool = typer.Option(False, "--global", help="Config globale utilisateur.")):
    """Gère la configuration de LCPI (get|set|list)."""
    import json
    config_path = pathlib.Path.home() / ".lcpi_config.json" if global_ else pathlib.Path(".lcpi_config.json")
    if not config_path.exists():
        config = {}
    else:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    if action == "set" and cle and valeur is not None:
        config[cle] = valeur
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        print(f"[SUCCES] Clé '{cle}' définie à '{valeur}'.")
    elif action == "get" and cle:
        print(config.get(cle, f"[ERREUR] Clé '{cle}' non trouvée."))
    elif action == "list":
        print(json.dumps(config, indent=2, ensure_ascii=False))
    else:
        print("Usage : lcpi config [get|set|list] <clé> [valeur] [--global]")

@app.command()
def doctor():
    """Vérifie l'installation, les dépendances et la compatibilité des plugins."""
    print("Vérification des dépendances Python...")
    required = ["typer", "yaml", "pandas", "matplotlib", "reportlab", "scipy"]
    for pkg in required:
        if importlib.util.find_spec(pkg) is not None:
            print(f"[OK] {pkg}")
        else:
            print(f"[ERREUR] {pkg} non installé.")
    print("\nVérification de Pandoc et LaTeX (optionnel)...")
    for tool in ["pandoc", "pdflatex"]:
        if shutil.which(tool):
            print(f"[OK] {tool}")
        else:
            print(f"[WARN] {tool} non trouvé dans le PATH.")
    print("\nPlugins disponibles :")
    plugins_dir = pathlib.Path(__file__).parent / "lcpi"
    for d in plugins_dir.iterdir():
        if d.is_dir() and not d.name.startswith("__"):
            print(f"- {d.name}")

@app.command()
def report(project_dir: str = typer.Argument("."), output: str = typer.Option("pdf", "--output", help="Format de sortie (pdf, md, html)")):
    """Analyse tous les éléments d'un projet et génère un rapport."""
    print(f"--- Lancement de l'analyse du projet dans : {project_dir} ---")
    # Ici, on pourrait parcourir les résultats YAML/JSON et les fusionner
    # Pour l'instant, on appelle generate_pdf_report si dispo
    try:
        generate_pdf_report([], f"rapport_lcpi.{output}")
        print(f"[SUCCES] Rapport généré : rapport_lcpi.{output}")
    except Exception as e:
        print(f"[ERREUR] Impossible de générer le rapport : {e}")


# --- Logique de découverte et de chargement des plugins (VERSION CORRIGÉE) ---
def print_plugin_status():
    print("--- Initialisation de LCPI-CLI ---")
    try:
        from .cm.main import register as register_cm
        app.add_typer(register_cm(), name="cm")
        print("[SUCCES] Plugin 'cm' chargé.")
    except ImportError as e:
        print(f"[ECHEC] Plugin 'cm' non chargé. Erreur : {e}")
    try:
        from .bois.main import register as register_bois
        app.add_typer(register_bois(), name="bois")
        print("[SUCCES] Plugin 'bois' chargé.")
    except ImportError as e:
        print(f"[ECHEC] Plugin 'bois' non chargé. Erreur : {e}")
    try:
        from .beton.main import register as register_beton
        app.add_typer(register_beton(), name="beton")
        print("[SUCCES] Plugin 'beton' chargé.")
    except ImportError as e:
        print(f"[ECHEC] Plugin 'beton' non chargé. Erreur : {e}")
    try:
        from .hydrodrain.main import register as register_hydrodrain
        app.add_typer(register_hydrodrain(), name="hydro")
        print("[SUCCES] Plugin 'hydro' chargé.")
    except ImportError as e:
        print(f"[ECHEC] Plugin 'hydro' non chargé. Erreur : {e}")
    print("----------------------------------")

@app.command("shell")
def shell():
    """Lance le shell interactif LCPI-CLI (invite >)."""
    print_plugin_status()
    print("Bienvenue dans le shell interactif LCPI-CLI ! Tapez 'exit' ou 'quit' pour sortir.")
    print("\nAide CLI :")
    app(["--help"])
    while True:
        try:
            cmd = input('> ').strip()
            if cmd in ('exit', 'quit'):
                print('Sortie du shell interactif.')
                break
            if not cmd:
                continue
            args = cmd.split()
            app(args)
        except (EOFError, KeyboardInterrupt):
            print('\nSortie du shell interactif.')
            break
