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
def init(
    nom_projet: str = typer.Argument("nouveau_projet_lcpi", help="Nom du projet à créer"),
    template: str = typer.Option(None, "--template", "-t", help="Template spécifique (cm, bois, beton, hydro, complet)"),
    plugins: str = typer.Option(None, "--plugins", "-p", help="Plugins à inclure (séparés par des virgules)"),
    force: bool = typer.Option(False, "--force", "-f", help="Forcer la création même si le dossier existe")
):
    """Initialise un nouveau projet LCPI avec une arborescence complète."""
    
    project_path = pathlib.Path(nom_projet)
    
    # Vérifier si le dossier existe
    if project_path.exists() and not force:
        console.print(Panel(
            f"[bold red]ERREUR[/bold red]: Le dossier '{nom_projet}' existe déjà.\n"
            f"Utilisez --force pour écraser le contenu existant.",
            title="Erreur d'Initialisation",
            border_style="red"
        ))
        return
    
    # Créer le dossier principal
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Déterminer les plugins à inclure
    available_plugins = get_available_plugins()
    if plugins:
        selected_plugins = [p.strip() for p in plugins.split(",")]
        # Vérifier que tous les plugins demandés existent
        invalid_plugins = [p for p in selected_plugins if p not in available_plugins]
        if invalid_plugins:
            console.print(Panel(
                f"[bold red]ERREUR[/bold red]: Plugins invalides: {', '.join(invalid_plugins)}\n"
                f"Plugins disponibles: {', '.join(available_plugins)}",
                title="Erreur d'Initialisation",
                border_style="red"
            ))
            return
    elif template:
        # Mapping des templates vers plugins
        template_plugins = {
            "cm": ["cm"],
            "bois": ["bois"],
            "beton": ["beton"],
            "hydro": ["hydrodrain"],
            "complet": available_plugins
        }
        selected_plugins = template_plugins.get(template, available_plugins)
    else:
        # Par défaut, inclure tous les plugins
        selected_plugins = available_plugins
    
    try:
        # Créer l'arborescence du projet
        create_project_structure(project_path, selected_plugins)
        
        # Créer les fichiers de configuration
        create_config_files(project_path, selected_plugins)
        
        # Créer les exemples selon les plugins
        create_examples(project_path, selected_plugins)
        
        # Créer la documentation du projet
        create_project_docs(project_path, selected_plugins)
        
        console.print(Panel(
            f"[bold green]SUCCÈS[/bold green]: Projet '{nom_projet}' initialisé avec succès !\n\n"
            f"📁 Structure créée: {project_path}\n"
            f"🔌 Plugins inclus: {', '.join(selected_plugins)}\n"
            f"📚 Exemples et templates copiés\n"
            f"📖 Documentation générée\n\n"
            f"Prochaines étapes:\n"
            f"1. cd {nom_projet}\n"
            f"2. lcpi doctor\n"
            f"3. lcpi examples\n"
            f"4. lcpi guide first_project",
            title="🎉 Initialisation Réussie",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(Panel(
            f"[bold red]ERREUR[/bold red]: Échec de l'initialisation: {str(e)}",
            title="Erreur d'Initialisation",
            border_style="red"
        ))
        # Nettoyer en cas d'erreur
        if project_path.exists() and not force:
            shutil.rmtree(project_path)

def create_project_structure(project_path: pathlib.Path, plugins: list):
    """Crée l'arborescence de base du projet."""
    
    # Structure de base
    directories = [
        "data",
        "output",
        "reports",
        "docs",
        "scripts",
        "templates"
    ]
    
    # Ajouter les répertoires spécifiques aux plugins
    for plugin in plugins:
        if plugin == "cm":
            directories.extend([
                "data/cm",
                "data/cm/poteaux",
                "data/cm/poutres",
                "data/cm/assemblages"
            ])
        elif plugin == "bois":
            directories.extend([
                "data/bois",
                "data/bois/poteaux",
                "data/bois/poutres",
                "data/bois/assemblages"
            ])
        elif plugin == "beton":
            directories.extend([
                "data/beton",
                "data/beton/poteaux",
                "data/beton/radiers"
            ])
        elif plugin == "hydrodrain":
            directories.extend([
                "data/hydro",
                "data/hydro/canaux",
                "data/hydro/reservoirs",
                "data/hydro/pluviometrie"
            ])
    
    # Créer tous les répertoires
    for directory in directories:
        (project_path / directory).mkdir(parents=True, exist_ok=True)

def create_config_files(project_path: pathlib.Path, plugins: list):
    """Crée les fichiers de configuration du projet."""
    
    # Fichier de configuration principal
    config_content = f"""# Configuration du projet LCPI
projet:
  nom: "{project_path.name}"
  version: "1.0.0"
  date_creation: "{time.strftime('%Y-%m-%d')}"
  description: "Projet d'ingénierie utilisant LCPI-CLI"

plugins_actifs:
{chr(10).join(f"  - {plugin}" for plugin in plugins)}

parametres_globaux:
  unite_longueur: "m"
  unite_force: "kN"
  unite_contrainte: "MPa"
  langue: "fr"

chemins:
  data: "./data"
  output: "./output"
  reports: "./reports"
  templates: "./templates"
"""
    
    with open(project_path / "config.yml", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    # Fichier .gitignore
    gitignore_content = """# Fichiers de sortie LCPI
output/
reports/
*.pdf
*.html
*.json

# Fichiers temporaires
temp/
*.tmp
*.log

# Fichiers système
.DS_Store
Thumbs.db

# Environnements virtuels
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
"""
    
    with open(project_path / ".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    # Fichier README du projet
    readme_content = f"""# {project_path.name}

Projet d'ingénierie utilisant LCPI-CLI (Plateforme de Calcul Polyvalent pour l'Ingénierie).

## Structure du Projet

```
{project_path.name}/
├── data/           # Données d'entrée
├── output/         # Résultats de calculs
├── reports/        # Rapports générés
├── docs/           # Documentation
├── scripts/        # Scripts personnalisés
├── templates/      # Templates de rapports
└── config.yml      # Configuration du projet
```

## Plugins Actifs

{chr(10).join(f"- **{plugin}**: {get_plugin_description(plugin)}" for plugin in plugins)}

## Utilisation

1. **Vérifier l'installation**:
   ```bash
   lcpi doctor
   ```

2. **Voir les exemples**:
   ```bash
   lcpi examples
   ```

3. **Lancer des calculs**:
   ```bash
   # Exemple pour {plugins[0] if plugins else 'un plugin'}
   lcpi {plugins[0] if plugins else 'plugin'} --help
   ```

4. **Générer un rapport**:
   ```bash
   lcpi report .
   ```

## Documentation

- [Guide de démarrage rapide](docs/quick_start.md)
- [Exemples d'utilisation](docs/examples.md)
- [Configuration avancée](docs/configuration.md)
"""
    
    with open(project_path / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

def get_plugin_description(plugin: str) -> str:
    """Retourne la description d'un plugin."""
    descriptions = {
        "cm": "Construction Métallique - Calculs selon Eurocode 3",
        "bois": "Construction Bois - Calculs selon Eurocode 5",
        "beton": "Béton Armé - Calculs selon Eurocode 2",
        "hydrodrain": "Hydrologie et Assainissement - Dimensionnement d'ouvrages"
    }
    return descriptions.get(plugin, "Plugin de calcul")

def create_examples(project_path: pathlib.Path, plugins: list):
    """Crée les exemples selon les plugins activés."""
    
    # Copier les exemples globaux
    examples_src = pathlib.Path(__file__).parent.parent.parent / "examples"
    if examples_src.exists():
        for example_file in examples_src.glob("*.yml"):
            shutil.copy2(example_file, project_path / "data")
    
    # Copier les templates de projet complets
    templates_src = pathlib.Path(__file__).parent / "templates_project"
    if templates_src.exists():
        for plugin in plugins:
            # Mapping des plugins vers les templates
            plugin_mapping = {
                "hydrodrain": "hydro",
                "cm": "cm",
                "bois": "bois",
                "beton": "beton"
            }
            
            template_plugin = plugin_mapping.get(plugin, plugin)
            plugin_templates_dir = templates_src / template_plugin
            if plugin_templates_dir.exists():
                plugin_data_dir = project_path / "data" / plugin
                plugin_data_dir.mkdir(exist_ok=True)
                
                # Copier tous les templates du plugin
                for template_file in plugin_templates_dir.glob("*.yml"):
                    shutil.copy2(template_file, plugin_data_dir)
    
    # Exemples spécifiques aux plugins (anciens exemples)
    for plugin in plugins:
        plugin_examples_dir = pathlib.Path(__file__).parent / plugin / "elements"
        if plugin_examples_dir.exists():
            plugin_data_dir = project_path / "data" / plugin
            plugin_data_dir.mkdir(exist_ok=True)
            
            for example_file in plugin_examples_dir.glob("*.yml"):
                shutil.copy2(example_file, plugin_data_dir)
        
        # Exemples spéciaux pour certains plugins
        if plugin == "beton":
            radiers_dir = pathlib.Path(__file__).parent / plugin / "radiers"
            if radiers_dir.exists():
                beton_data_dir = project_path / "data" / plugin
                for radier_file in radiers_dir.glob("*.yml"):
                    shutil.copy2(radier_file, beton_data_dir)
        
        elif plugin == "hydrodrain":
            hydro_data_dir = pathlib.Path(__file__).parent / plugin / "data"
            if hydro_data_dir.exists():
                project_hydro_dir = project_path / "data" / "hydro"
                for data_file in hydro_data_dir.glob("*.yml"):
                    shutil.copy2(data_file, project_hydro_dir)

def create_project_docs(project_path: pathlib.Path, plugins: list):
    """Crée la documentation du projet."""
    
    docs_dir = project_path / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Guide de démarrage rapide
    quick_start_content = f"""# Guide de Démarrage Rapide - {project_path.name}

## Premiers Pas

### 1. Vérifier l'Installation
```bash
lcpi doctor
```

### 2. Explorer les Exemples
```bash
# Voir tous les exemples
lcpi examples

# Exemples spécifiques
lcpi examples {plugins[0] if plugins else 'plugin'}
```

### 3. Premier Calcul

{get_first_calculation_example(plugins[0] if plugins else None)}

## Structure des Données

### Format YAML
Tous les fichiers de données utilisent le format YAML. Exemple:

```yaml
# Exemple de fichier de données
description: "Description de l'élément"
parametres:
  valeur1: 10.0
  valeur2: "texte"
```

### Organisation des Fichiers
- `data/` : Données d'entrée
- `output/` : Résultats de calculs
- `reports/` : Rapports générés

## Commandes Utiles

```bash
# Aide générale
lcpi --help

# Aide d'un plugin
lcpi {plugins[0] if plugins else 'plugin'} --help

# Mode interactif
lcpi shell

# Générer un rapport
lcpi report .
```
"""
    
    with open(docs_dir / "quick_start.md", "w", encoding="utf-8") as f:
        f.write(quick_start_content)
    
    # Fichier d'exemples
    examples_content = f"""# Exemples d'Utilisation - {project_path.name}

## Plugins Disponibles

{chr(10).join(f"### {plugin.upper()}\n{get_plugin_examples(plugin)}" for plugin in plugins)}

## Exemples de Fichiers de Données

### Construction Métallique (CM)
```yaml
# data/cm/poutre_exemple.yml
element_id: P1
description: "Poutre principale"
materiau:
  nuance: S235
  fy_MPa: 235.0
geometrie:
  type_profil: IPE
  longueur_m: 8.0
charges:
  permanentes_G:
    - type: repartie
      valeur: 5.0
```

### Construction Bois
```yaml
# data/bois/poteau_exemple.yml
description: "Poteau en bois C24"
profil:
  type: "rectangulaire"
  dimensions_mm:
    b: 150
    h: 150
materiau:
  classe_resistance: "C24"
  classe_service: 2
longueur_flambement_m: 4.5
efforts_elu:
  N_c_ed_kN: 80
```

### Béton Armé
```yaml
# data/beton/poteau_exemple.yml
element_id: P1
description: "Poteau béton armé"
materiaux:
  fc28_MPa: 25.0
  fe_MPa: 500.0
geometrie:
  section_mm:
    b: 300
    h: 300
  longueur_m: 3.0
efforts:
  N_ed_kN: 500
  M_ed_kNm: 50
```

### Hydrologie
```yaml
# data/hydro/canal_exemple.yml
debit_projet_m3s: 10.0
k_strickler: 30.0
vitesse_max_admissible_ms: 1.5
pente_m_m: 0.001
fruit_talus_z: 1.5
```
"""
    
    with open(docs_dir / "examples.md", "w", encoding="utf-8") as f:
        f.write(examples_content)

def get_first_calculation_example(plugin: str) -> str:
    """Retourne un exemple de premier calcul selon le plugin."""
    examples = {
        "cm": """```bash
# Vérifier un poteau
lcpi cm check-poteau data/cm/poteau_exemple.yml

# Vérifier une poutre
lcpi cm check-deversement data/cm/poutre_exemple.yml
```""",
        "bois": """```bash
# Vérifier un poteau en bois
lcpi bois check-poteau data/bois/poteau_exemple.yml

# Vérifier une poutre
lcpi bois check-deversement data/bois/poutre_exemple.yml
```""",
        "beton": """```bash
# Calculer un poteau
lcpi beton calc-poteau data/beton/poteau_exemple.yml

# Calculer un radier
lcpi beton calc-radier data/beton/radier_exemple.yml
```""",
        "hydrodrain": """```bash
# Dimensionner un canal
lcpi hydro ouvrage canal data/hydro/canal_exemple.yml

# Dimensionner un réservoir
lcpi hydro reservoir equilibrage --demande-journaliere 1000
```"""
    }
    return examples.get(plugin, "```bash\nlcpi plugin --help\n```")

def get_plugin_examples(plugin: str) -> str:
    """Retourne les exemples pour un plugin spécifique."""
    examples = {
        "cm": """- Vérification de poteaux en compression/flambement
- Vérification de poutres en flexion
- Vérification d'assemblages boulonnés/soudés
- Optimisation de sections""",
        "bois": """- Vérification de poteaux en bois
- Vérification de poutres en flexion
- Vérification d'assemblages à pointes/embrevement
- Vérification de cisaillement""",
        "beton": """- Calcul de poteaux en béton armé
- Calcul de radiers
- Vérification des états limites""",
        "hydrodrain": """- Dimensionnement de canaux
- Dimensionnement de réservoirs
- Analyse pluviométrique
- Calculs d'assainissement"""
    }
    return examples.get(plugin, "Exemples disponibles pour ce plugin")

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
        app.add_typer(register_shell(), name="shell")
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