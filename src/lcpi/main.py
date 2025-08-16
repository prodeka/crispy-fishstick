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
print("⚠️  Vérification de licence temporairement désactivée pour les tests")

# Import du gestionnaire de session
from .core.session_manager import session_manager

# Flag global pour l'initialisation des plugins
_plugins_initialized = False

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
    global _json_output_enabled, _plugins_initialized
    _json_output_enabled = json_output
    
    # Initialiser les plugins si ce n'est pas déjà fait
    if not _plugins_initialized:
        print_plugin_status()
        _plugins_initialized = True
    
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
@app.command()
def init(
    nom_projet: str = typer.Argument(None, help="Nom du projet à créer"),
    template: str = typer.Option(None, "--template", "-t", help="Template spécifique (cm, bois, beton, hydro, complet)"),
    plugins: str = typer.Option(None, "--plugins", "-p", help="Plugins à inclure (séparés par des virgules)"),
    force: bool = typer.Option(False, "--force", "-f", help="Forcer la création même si le dossier existe"),
    interactive: bool = typer.Option(True, "--no-interactive", help="Désactiver le mode interactif"),
    git_init: bool = typer.Option(False, "--git", "-g", help="Initialiser un dépôt Git"),
    remote_url: str = typer.Option(None, "--remote", "-r", help="URL du remote Git (ex: https://github.com/user/repo.git)")
):
    """Initialise un nouveau projet LCPI avec une arborescence complète et gestion avancée."""
    
    # Mode interactif pour collecter les informations
    if interactive:
        console.print(Panel(
            "[bold blue]🚀 INITIALISATION D'UN NOUVEAU PROJET LCPI[/bold blue]\n\n"
            "Je vais vous guider pour créer votre projet. Répondez aux questions ci-dessous.",
            title="Assistant d'Initialisation",
            border_style="blue"
        ))
        
        # Collecter les informations du projet
        if not nom_projet:
            while True:
                nom_projet = input("\n📝 Nom du projet: ").strip()
                if nom_projet:
                    # Valider le nom du projet
                    if not nom_projet.replace("_", "").replace("-", "").isalnum():
                        console.print("[red]❌ Le nom du projet ne peut contenir que des lettres, chiffres, tirets et underscores[/red]")
                        continue
                    if len(nom_projet) < 3:
                        console.print("[red]❌ Le nom du projet doit contenir au moins 3 caractères[/red]")
                        continue
                    break
                else:
                    console.print("[red]❌ Le nom du projet est obligatoire[/red]")
        
        # Demander le nom de l'utilisateur
        nom_utilisateur = input("👤 Nom de l'utilisateur/ingénieur: ").strip()
        if not nom_utilisateur:
            nom_utilisateur = "Ingénieur LCPI"
        
        # Demander la description
        description = input("📋 Description du projet (optionnel): ").strip()
        if not description:
            description = f"Projet {nom_projet} créé avec LCPI"
        
        # Demander le template si pas spécifié
        if not template:
            console.print("\n🎯 Choisissez un template de projet:")
            console.print("1. [cyan]cm[/cyan] - Construction métallique")
            console.print("2. [cyan]bois[/cyan] - Construction bois")
            console.print("3. [cyan]beton[/cyan] - Béton armé")
            console.print("4. [cyan]hydro[/cyan] - Hydrologie/Assainissement")
            console.print("5. [cyan]complet[/cyan] - Tous les modules")
            console.print("6. [cyan]personnalise[/cyan] - Sélection manuelle des plugins")
            
            while True:
                choix = input("\nVotre choix (1-6): ").strip()
                template_map = {
                    "1": "cm", "2": "bois", "3": "beton", 
                    "4": "hydro", "5": "complet", "6": "personnalise"
                }
                if choix in template_map:
                    template = template_map[choix]
                    break
                else:
                    console.print("[red]❌ Choix invalide. Entrez un nombre entre 1 et 6.[/red]")
        
        # Si personnalisé, demander les plugins
        if template == "personnalise" and not plugins:
            available_plugins = get_available_plugins()
            console.print(f"\n🔌 Plugins disponibles: {', '.join(available_plugins)}")
            console.print("Entrez les plugins séparés par des virgules (ex: cm,bois,hydrodrain)")
            
            while True:
                plugins_input = input("Plugins à inclure: ").strip()
                if plugins_input:
                    selected_plugins = [p.strip() for p in plugins_input.split(",")]
                    invalid_plugins = [p for p in selected_plugins if p not in available_plugins]
                    if invalid_plugins:
                        console.print(f"[red]❌ Plugins invalides: {', '.join(invalid_plugins)}[/red]")
                        console.print(f"Plugins valides: {', '.join(available_plugins)}")
                        continue
                    plugins = plugins_input
                    break
                else:
                    console.print("[red]❌ Vous devez sélectionner au moins un plugin[/red]")
    
    else:
        # Mode non-interactif
        if not nom_projet:
            nom_projet = "nouveau_projet_lcpi"
        nom_utilisateur = "Ingénieur LCPI"
        description = f"Projet {nom_projet} créé avec LCPI"
    
    project_path = pathlib.Path(nom_projet)
    
    # Vérifier si le dossier existe
    if project_path.exists() and not force:
        if interactive:
            console.print(f"\n⚠️  Le dossier '{nom_projet}' existe déjà.")
            overwrite = input("Voulez-vous l'écraser ? (o/N): ").strip().lower()
            if overwrite not in ['o', 'oui', 'y', 'yes']:
                console.print("[yellow]Initialisation annulée.[/yellow]")
                return
        else:
            console.print(Panel(
                f"[bold red]ERREUR[/bold red]: Le dossier '{nom_projet}' existe déjà.\n"
                f"Utilisez --force pour écraser le contenu existant.",
                title="Erreur d'Initialisation",
                border_style="red"
            ))
            return
    
    # Créer le dossier principal
    try:
        project_path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        console.print(Panel(
            "[bold red]ERREUR[/bold red]: Permissions insuffisantes pour créer le dossier.\n"
            "Vérifiez vos droits d'écriture dans le répertoire.",
            title="Erreur de Permissions",
            border_style="red"
        ))
        return
    except Exception as e:
        console.print(Panel(
            f"[bold red]ERREUR[/bold red]: Impossible de créer le dossier: {str(e)}",
            title="Erreur de Création",
            border_style="red"
        ))
        return
    
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
        
        # Créer les fichiers de configuration avec les informations utilisateur
        create_config_files(project_path, selected_plugins, nom_utilisateur, description)
        
        # Créer les exemples selon les plugins
        create_examples(project_path, selected_plugins)
        
        # Créer la documentation du projet
        create_project_docs(project_path, selected_plugins, nom_utilisateur, description)
        
        console.print(Panel(
            f"[bold green]SUCCÈS[/bold green]: Projet '{nom_projet}' initialisé avec succès !\n\n"
            f"📁 Structure créée: {project_path}\n"
            f"👤 Utilisateur: {nom_utilisateur}\n"
            f"📋 Description: {description}\n"
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
            try:
                shutil.rmtree(project_path)
            except:
                console.print("[yellow]⚠️  Impossible de nettoyer le dossier créé.[/yellow]")

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

def create_config_files(project_path: pathlib.Path, plugins: list, nom_utilisateur: str, description: str):
    """Crée les fichiers de configuration du projet."""
    
    # Fichier de configuration principal
    config_content = f"""# Configuration du projet LCPI
projet:
  nom: "{project_path.name}"
  version: "1.0.0"
  date_creation: "{time.strftime('%Y-%m-%d')}"
  description: "{description}"
  utilisateur: "{nom_utilisateur}"

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

def create_project_docs(project_path: pathlib.Path, plugins: list, nom_utilisateur: str, description: str):
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

@app.command()
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

@app.command()
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

    # Charger le plugin de reporting
    try:
        from .reporting.cli import app as reporting_app
        app.add_typer(reporting_app, name="rapport")
        plugins_info['reporting'] = {'status': 'loaded', 'path': 'rapport.cli'}
        console.print("[green]✓[/green] Plugin 'reporting' chargé.")
    except ImportError as e:
        plugins_info['reporting'] = {'status': 'error', 'error': str(e)}
        console.print(Panel(f"[bold red]✗[/bold red] Plugin 'reporting' non chargé. Erreur : {e}", title="Erreur de Chargement Plugin", border_style="red"))

    # Charger le plugin de gestion des projets
    try:
        from .project_cli import app as project_app
        app.add_typer(project_app, name="project")
        plugins_info['project'] = {'status': 'loaded', 'path': 'project_cli'}
        console.print("[green]✓[/green] Plugin 'project' chargé.")
    except ImportError as e:
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
        
        # Mettre à jour la session si elle existe
        if session_manager.is_session_valid():
            session_manager.update_session_usage()
        return
    
    # Vérifier si une session valide existe
    if session_manager.is_session_valid():
        session_data = session_manager.get_session_data()
        plugins_count = len(session_data.get('plugins', {}))
        console.print(f"🚀 [green]Session restaurée[/green] - {plugins_count} plugins chargés")
        console.print("[bold]----------------------------------[/bold]")
        
        # Marquer les plugins comme initialisés (ils sont déjà chargés dans l'app)
        _plugins_initialized = True
        
        # Mettre à jour l'utilisation de la session
        session_manager.update_session_usage()
        return
    
    # Pas de session valide, initialiser les plugins
    plugins_info = initialize_plugins()
    console.print("[bold]----------------------------------[/bold]")
    
    # Créer une nouvelle session
    session_manager.create_session(plugins_info)
    console.print(f"💾 [blue]Nouvelle session créée[/blue] - {len(plugins_info)} plugins initialisés")

# Appel de la fonction pour enregistrer les plugins au démarrage
# On vérifie la variable d'environnement pour un lancement "core only"
# Note: print_plugin_status() sera appelé lors de la première commande

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

# Import des modules de logging et validation
from .logging_cli import app as logs_app

# Ajouter la sous-commande de logging
app.add_typer(logs_app, name="logs", help="Gestion des logs avec signature et intégrité")

@app.command()
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