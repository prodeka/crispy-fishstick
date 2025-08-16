"""
Gestionnaire d'exemples pour LCPI.
Gère la liste et la description des exemples disponibles.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

# Configuration des exemples disponibles
EXAMPLES_CONFIG = {
    "canal_exemple": {
        "description": "Dimensionnement d'un canal simple avec formules de Manning",
        "files": ["canal_exemple.yml", "canal.yml"],
        "category": "Hydro",
        "difficulty": "Débutant"
    },
    "dalot": {
        "description": "Dimensionnement d'un dalot pour passage d'eau",
        "files": ["dalot.yml"],
        "category": "Hydro",
        "difficulty": "Intermédiaire"
    },
    "deversoir": {
        "description": "Dimensionnement d'un déversoir de sécurité",
        "files": ["deversoir.yml"],
        "category": "Hydro",
        "difficulty": "Intermédiaire"
    },
    "hardy_cross": {
        "description": "Résolution d'un réseau par la méthode Hardy-Cross",
        "files": ["hardy_cross_test.yml", "hardy_cross_test.csv"],
        "category": "AEP",
        "difficulty": "Avancé"
    },
    "reseau_optimisation": {
        "description": "Optimisation d'un réseau d'eau potable",
        "files": ["reseau_optimisation.yml"],
        "category": "AEP",
        "difficulty": "Avancé"
    },
    "scenarios_test": {
        "description": "Test de différents scénarios de fonctionnement",
        "files": ["scenarios_test.yml"],
        "category": "AEP",
        "difficulty": "Intermédiaire"
    },
    "reseau_source": {
        "description": "Réseau avec source d'alimentation",
        "files": ["reseau_test_avec_source.yml"],
        "category": "AEP",
        "difficulty": "Intermédiaire"
    },
    "eaux_usees": {
        "description": "Exemple de réseau d'eaux usées",
        "files": ["exemple_reseau_eaux_usees.json"],
        "category": "Assainissement",
        "difficulty": "Intermédiaire"
    },
    "eaux_pluviales": {
        "description": "Exemple de réseau d'eaux pluviales",
        "files": ["exemple_reseau_eaux_pluviales.json"],
        "category": "Assainissement",
        "difficulty": "Intermédiaire"
    }
}

def get_available_examples() -> List[str]:
    """Retourne la liste des exemples disponibles."""
    return list(EXAMPLES_CONFIG.keys())

def get_example_description(example_name: str) -> str:
    """Retourne la description d'un exemple."""
    return EXAMPLES_CONFIG.get(example_name, {}).get("description", "Description non disponible")

def get_example_files(example_name: str) -> List[str]:
    """Retourne la liste des fichiers d'un exemple."""
    return EXAMPLES_CONFIG.get(example_name, {}).get("files", [])

def get_example_category(example_name: str) -> str:
    """Retourne la catégorie d'un exemple."""
    return EXAMPLES_CONFIG.get(example_name, {}).get("category", "Inconnue")

def get_example_difficulty(example_name: str) -> str:
    """Retourne le niveau de difficulté d'un exemple."""
    return EXAMPLES_CONFIG.get(example_name, {}).get("difficulty", "Inconnu")

def get_examples_by_category(category: str) -> List[str]:
    """Retourne les exemples d'une catégorie donnée."""
    return [
        name for name, config in EXAMPLES_CONFIG.items()
        if config.get("category") == category
    ]

def get_examples_by_difficulty(difficulty: str) -> List[str]:
    """Retourne les exemples d'un niveau de difficulté donné."""
    return [
        name for name, config in EXAMPLES_CONFIG.items()
        if config.get("difficulty") == difficulty
    ]

def get_example_path(example_name: str) -> Optional[Path]:
    """Retourne le chemin vers un exemple."""
    if example_name not in EXAMPLES_CONFIG:
        return None
    
    # Chercher dans le répertoire examples
    examples_dir = Path("examples")
    if not examples_dir.exists():
        return None
    
    # Vérifier si les fichiers existent
    files = get_example_files(example_name)
    for file in files:
        file_path = examples_dir / file
        if file_path.exists():
            return file_path
    
    return None

def list_example_files(example_name: str) -> List[Path]:
    """Liste les fichiers d'un exemple avec leurs chemins complets."""
    if example_name not in EXAMPLES_CONFIG:
        return []
    
    examples_dir = Path("examples")
    if not examples_dir.exists():
        return []
    
    files = []
    for file in get_example_files(example_name):
        file_path = examples_dir / file
        if file_path.exists():
            files.append(file_path)
    
    return files

def validate_example(example_name: str) -> bool:
    """Valide qu'un exemple existe et est accessible."""
    if example_name not in EXAMPLES_CONFIG:
        return False
    
    files = list_example_files(example_name)
    return len(files) > 0

def get_example_summary(example_name: str) -> Dict:
    """Retourne un résumé complet d'un exemple."""
    if example_name not in EXAMPLES_CONFIG:
        return {}
    
    config = EXAMPLES_CONFIG[example_name]
    files = list_example_files(example_name)
    
    return {
        "name": example_name,
        "description": config.get("description", ""),
        "category": config.get("category", ""),
        "difficulty": config.get("difficulty", ""),
        "files": [str(f) for f in files],
        "accessible": len(files) > 0,
        "file_count": len(files)
    }

def search_examples(query: str) -> List[str]:
    """Recherche des exemples par mot-clé."""
    query = query.lower()
    results = []
    
    for name, config in EXAMPLES_CONFIG.items():
        # Recherche dans le nom
        if query in name.lower():
            results.append(name)
            continue
        
        # Recherche dans la description
        if query in config.get("description", "").lower():
            results.append(name)
            continue
        
        # Recherche dans la catégorie
        if query in config.get("category", "").lower():
            results.append(name)
            continue
    
    return results

def get_examples_statistics() -> Dict:
    """Retourne des statistiques sur les exemples disponibles."""
    total = len(EXAMPLES_CONFIG)
    categories = {}
    difficulties = {}
    accessible = 0
    
    for name, config in EXAMPLES_CONFIG.items():
        # Compter par catégorie
        category = config.get("category", "Inconnue")
        categories[category] = categories.get(category, 0) + 1
        
        # Compter par difficulté
        difficulty = config.get("difficulty", "Inconnu")
        difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
        
        # Compter les exemples accessibles
        if validate_example(name):
            accessible += 1
    
    return {
        "total": total,
        "accessible": accessible,
        "categories": categories,
        "difficulties": difficulties
    }
