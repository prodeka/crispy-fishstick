"""
Gestionnaire de templates pour LCPI.
Gère la création de projets à partir de templates prédéfinis.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import yaml

# Configuration des templates disponibles
TEMPLATES_CONFIG = {
    "aep-village": {
        "description": "Projet AEP pour village/rural",
        "type": "AEP",
        "files": ["lcpi.yml", "data/", "output/", "docs/"],
        "source": "examples/templates/aep-village/"
    },
    "aep-urbain": {
        "description": "Projet AEP pour zone urbaine",
        "type": "AEP",
        "files": ["lcpi.yml", "data/", "output/", "docs/"],
        "source": "examples/templates/aep-urbain/"
    },
    "canal-simple": {
        "description": "Dimensionnement de canal simple",
        "type": "Hydro",
        "files": ["canal.yml", "data/", "output/"],
        "source": "examples/"
    },
    "dalot": {
        "description": "Dimensionnement de dalot",
        "type": "Hydro",
        "files": ["dalot.yml", "data/", "output/"],
        "source": "examples/"
    },
    "deversoir": {
        "description": "Dimensionnement de déversoir",
        "type": "Hydro",
        "files": ["deversoir.yml", "data/", "output/"],
        "source": "examples/"
    },
    "beton-arme": {
        "description": "Projet béton armé complet",
        "type": "Béton",
        "files": ["lcpi.yml", "data/beton/", "output/", "docs/"],
        "source": "projet_templates_final/"
    },
    "bois": {
        "description": "Projet construction bois",
        "type": "Bois",
        "files": ["lcpi.yml", "data/bois/", "output/", "docs/"],
        "source": "projet_templates_final/"
    },
    "mixte": {
        "description": "Projet mixte (béton + bois + hydro)",
        "type": "Mixte",
        "files": ["lcpi.yml", "data/", "output/", "docs/"],
        "source": "projet_templates_final/"
    }
}

def get_available_templates() -> List[str]:
    """Retourne la liste des templates disponibles."""
    return list(TEMPLATES_CONFIG.keys())

def get_template_description(template_name: str) -> str:
    """Retourne la description d'un template."""
    return TEMPLATES_CONFIG.get(template_name, {}).get("description", "Description non disponible")

def get_template_type(template_name: str) -> str:
    """Retourne le type d'un template."""
    return TEMPLATES_CONFIG.get(template_name, {}).get("type", "Inconnu")

def get_template_files(template_name: str) -> List[str]:
    """Retourne la liste des fichiers d'un template."""
    return TEMPLATES_CONFIG.get(template_name, {}).get("files", [])

def get_template_source(template_name: str) -> str:
    """Retourne le chemin source d'un template."""
    return TEMPLATES_CONFIG.get(template_name, {}).get("source", "")

def validate_template(template_name: str) -> bool:
    """Valide qu'un template existe et est accessible."""
    if template_name not in TEMPLATES_CONFIG:
        return False
    
    source_path = Path(get_template_source(template_name))
    return source_path.exists()

def create_project_from_template(
    nom_projet: str,
    template: str,
    output_dir: str = ".",
    force: bool = False,
    git_init: bool = False,
    remote_url: Optional[str] = None
) -> Path:
    """Crée un projet à partir d'un template."""
    if not validate_template(template):
        raise ValueError(f"Template '{template}' non valide ou inaccessible")
    
    # Chemin de sortie
    output_path = Path(output_dir) / nom_projet
    
    if output_path.exists() and not force:
        raise FileExistsError(f"Le répertoire '{output_path}' existe déjà. Utilisez --force pour écraser.")
    
    # Chemin source du template
    source_path = Path(get_template_source(template))
    
    # Créer le répertoire de sortie
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Copier les fichiers du template
    if source_path.is_dir():
        shutil.copytree(source_path, output_path, dirs_exist_ok=True)
    else:
        shutil.copy2(source_path, output_path)
    
    # Personnaliser le projet
    customize_project(output_path, nom_projet, template)
    
    # Initialiser Git si demandé
    if git_init:
        _init_git_repo(output_path, remote_url)
    
    return output_path

def customize_project(project_path: Path, nom_projet: str, template: str):
    """Personnalise le projet créé."""
    # Créer le fichier lcpi.yml s'il n'existe pas
    lcpi_file = project_path / "lcpi.yml"
    if not lcpi_file.exists():
        create_lcpi_config(project_path, nom_projet, template)
    
    # Créer le README
    readme_file = project_path / "README.md"
    if not readme_file.exists():
        create_readme(project_path, nom_projet, template)
    
    # Créer la structure de base
    create_project_structure(project_path, template)

def create_lcpi_config(project_path: Path, nom_projet: str, template: str):
    """Crée la configuration LCPI du projet."""
    config = {
        "project": {
            "name": nom_projet,
            "version": "1.0.0",
            "description": f"Projet {nom_projet} créé avec le template {template}",
            "template": template,
            "created": str(Path.cwd()),
            "author": "LCPI CLI"
        },
        "plugins": get_default_plugins(template),
        "output": {
            "formats": ["html", "pdf", "json"],
            "directory": "output/"
        }
    }
    
    with open(project_path / "lcpi.yml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

def get_default_plugins(template: str) -> List[str]:
    """Retourne les plugins par défaut selon le template."""
    plugin_mapping = {
        "aep-village": ["aep", "hydro"],
        "aep-urbain": ["aep", "hydro"],
        "canal-simple": ["hydro"],
        "dalot": ["hydro"],
        "deversoir": ["hydro"],
        "beton-arme": ["beton"],
        "bois": ["bois"],
        "mixte": ["beton", "bois", "hydro"]
    }
    return plugin_mapping.get(template, [])

def create_readme(project_path: Path, nom_projet: str, template: str):
    """Crée le README du projet."""
    readme_content = f"""# {nom_projet}

Projet créé avec le template LCPI **{template}**.

## Description

{get_template_description(template)}

## Structure du Projet

```
{nom_projet}/
├── lcpi.yml          # Configuration du projet
├── data/             # Données d'entrée
├── output/           # Résultats et rapports
└── docs/             # Documentation
```

## Utilisation

1. **Activer le projet :**
   ```bash
   lcpi project switch {nom_projet}
   ```

2. **Exécuter les calculs :**
   ```bash
   lcpi aep run data/network.yml
   ```

3. **Générer les rapports :**
   ```bash
   lcpi report generate
   ```

## Support

Pour plus d'informations, consultez la documentation LCPI.
"""
    
    with open(project_path / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

def create_project_structure(project_path: Path, template: str):
    """Crée la structure de base du projet."""
    # Créer les répertoires de base
    (project_path / "data").mkdir(exist_ok=True)
    (project_path / "output").mkdir(exist_ok=True)
    (project_path / "docs").mkdir(exist_ok=True)
    (project_path / "temp").mkdir(exist_ok=True)
    
    # Créer le fichier .gitignore
    gitignore_content = """# LCPI
output/
temp/
*.log
*.tmp

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open(project_path / ".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)

def _init_git_repo(project_path: Path, remote_url: Optional[str] = None):
    """Initialise un dépôt Git pour le projet."""
    try:
        import git
        
        # Initialiser le dépôt
        repo = git.Repo.init(project_path)
        
        # Ajouter tous les fichiers
        repo.index.add("*")
        
        # Premier commit
        repo.index.commit("Initial commit - Projet LCPI créé")
        
        # Configurer le remote si fourni
        if remote_url:
            origin = repo.create_remote("origin", remote_url)
            repo.index.commit("Configure remote origin")
            
    except ImportError:
        print("⚠️  GitPython non installé - initialisation Git ignorée")
    except git.GitCommandError as e:
        print(f"⚠️  Erreur lors de l'initialisation Git: {e}")
    except Exception as e:
        print(f"⚠️  Erreur inattendue lors de l'initialisation Git: {e}")
