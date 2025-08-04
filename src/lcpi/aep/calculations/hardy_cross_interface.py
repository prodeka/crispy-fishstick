"""
Interface pour les fonctions Hardy-Cross
"""

def hardy_cross_from_csv(csv_path: str, max_iterations: int = 100, tolerance: float = 1e-6):
    """Exécute Hardy-Cross depuis un fichier CSV."""
    try:
        from .hardy_cross_enhanced import load_hardy_cross_csv, hardy_cross_network_enhanced
        network_data = load_hardy_cross_csv(csv_path)
        results = hardy_cross_network_enhanced(network_data, max_iterations, tolerance)
        return {"status": "success", "input_file": csv_path, "results": results}
    except Exception as e:
        return {"status": "error", "error": str(e), "input_file": csv_path}

def hardy_cross_from_yaml(yaml_path: str, max_iterations: int = 100, tolerance: float = 1e-6):
    """Exécute Hardy-Cross depuis un fichier YAML."""
    try:
        from .hardy_cross_enhanced import load_hardy_cross_yaml, hardy_cross_network_enhanced
        network_data = load_hardy_cross_yaml(yaml_path)
        results = hardy_cross_network_enhanced(network_data, max_iterations, tolerance)
        return {"status": "success", "input_file": yaml_path, "results": results}
    except Exception as e:
        return {"status": "error", "error": str(e), "input_file": yaml_path}

def get_hardy_cross_help():
    """Retourne l'aide pour la méthode Hardy-Cross."""
    return """
# Méthode Hardy-Cross

## Description
Méthode itérative pour résoudre les réseaux de distribution d'eau en boucle fermée.

## Formules
- Coefficient de résistance : K = 8fL/(π²gD⁵)
- Perte de charge : hf = KQ²
- Correction de débit : ΔQ = -Σhf/(2ΣK|Q|)

## Formats d'entrée
- CSV : pipe_id, from_node, to_node, length, diameter, roughness
- YAML : Structure hiérarchique avec nœuds et conduites

## Exemples
```bash
lcpi aep hardy-cross-csv network.csv
lcpi aep hardy-cross-yaml network.yml
```
""" 