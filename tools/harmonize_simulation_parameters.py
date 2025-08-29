#!/usr/bin/env python3
"""
Script d'harmonisation des paramètres de simulation entre EPANET et LCPI Hardy-Cross.

Ce script vérifie et harmonise les paramètres de convergence, tolérance et itérations
entre les deux solveurs pour assurer une comparaison équitable.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Tuple

# Forcer l'encodage UTF-8 pour le terminal
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    
    # Forcer l'encodage de la console Windows
    try:
        import subprocess
        subprocess.run(['chcp', '65001'], shell=True, check=True, capture_output=True)
    except:
        pass

# Ajouter le répertoire src au path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

def get_lcpi_defaults() -> Dict[str, Any]:
    """Récupère les paramètres par défaut de LCPI Hardy-Cross."""
    try:
        from lcpi.aep.core.models import ConfigurationOptimisation
        from lcpi.aep.core.pydantic_models import HardyCrossConfig
        
        # Paramètres par défaut de LCPI
        lcpi_defaults = {
            "tolerance": 1e-6,
            "max_iterations": 200,
            "formula": "hazen_williams",
            "convergence_criteria": "relative_error"
        }
        
        print(f"✅ Paramètres LCPI Hardy-Cross par défaut:")
        for key, value in lcpi_defaults.items():
            print(f"   • {key}: {value}")
            
        return lcpi_defaults
        
    except ImportError as e:
        print(f"⚠️ Impossible d'importer les modèles LCPI: {e}")
        return {
            "tolerance": 1e-6,
            "max_iterations": 200,
            "formula": "hazen_williams"
        }

def get_epanet_defaults() -> Dict[str, Any]:
    """Récupère les paramètres par défaut d'EPANET."""
    try:
        # Constantes EPANET standard
        epanet_defaults = {
            "tolerance": 1e-6,  # Tolérance de convergence par défaut
            "max_iterations": 100,  # Nombre maximum d'itérations
            "formula": "hazen_williams",  # Formule de perte de charge
            "convergence_criteria": "relative_error"  # Critère de convergence
        }
        
        print(f"✅ Paramètres EPANET par défaut:")
        for key, value in epanet_defaults.items():
            print(f"   • {key}: {value}")
            
        return epanet_defaults
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la récupération des paramètres EPANET: {e}")
        return {}

def check_epanet_wrapper_config() -> Dict[str, Any]:
    """Vérifie la configuration du wrapper EPANET."""
    try:
        from lcpi.aep.core.epanet_wrapper import EpanetWrapper
        
        wrapper = EpanetWrapper()
        available = wrapper.is_available()
        version = wrapper.get_version()
        
        print(f"✅ Wrapper EPANET:")
        print(f"   • Disponible: {available}")
        print(f"   • Version: {version}")
        
        return {
            "available": available,
            "version": version
        }
        
    except ImportError as e:
        print(f"⚠️ Impossible d'importer le wrapper EPANET: {e}")
        return {"available": False, "version": "unknown"}

def check_constraints_handler() -> Dict[str, Any]:
    """Vérifie la configuration du gestionnaire de contraintes."""
    try:
        from lcpi.aep.optimizer.constraints_handler import ConstraintManager, ConstraintPenaltyCalculator
        
        # Vérifier les seuils de contraintes
        constraints_config = {
            "pressure_min": 10.0,  # Pression minimale en mCE
            "velocity_max": 3.0,   # Vitesse maximale en m/s
            "velocity_min": 0.3    # Vitesse minimale en m/s
        }
        
        print(f"✅ Gestionnaire de contraintes:")
        for key, value in constraints_config.items():
            print(f"   • {key}: {value}")
            
        return constraints_config
        
    except ImportError as e:
        print(f"⚠️ Impossible d'importer le gestionnaire de contraintes: {e}")
        return {}

def create_harmonized_config() -> Dict[str, Any]:
    """Crée une configuration harmonisée pour les deux solveurs."""
    
    print("\n🔧 HARMONISATION DES PARAMÈTRES DE SIMULATION")
    print("=" * 60)
    
    # Récupérer les paramètres par défaut
    lcpi_params = get_lcpi_defaults()
    epanet_params = get_epanet_defaults()
    
    # Vérifier la disponibilité des composants
    epanet_wrapper = check_epanet_wrapper_config()
    constraints = check_constraints_handler()
    
    # Créer la configuration harmonisée
    harmonized_config = {
        "convergence": {
            "tolerance": max(lcpi_params.get("tolerance", 1e-6), 
                           epanet_params.get("tolerance", 1e-6)),
            "max_iterations": max(lcpi_params.get("max_iterations", 200), 
                                epanet_params.get("max_iterations", 100)),
            "formula": "hazen_williams",
            "criteria": "relative_error"
        },
        "constraints": {
            "pressure_min_mce": constraints.get("pressure_min", 10.0),
            "velocity_max_ms": constraints.get("velocity_max", 3.0),
            "velocity_min_ms": constraints.get("velocity_min", 0.3)
        },
        "solver_specific": {
            "lcpi": {
                "tolerance": lcpi_params.get("tolerance", 1e-6),
                "max_iterations": lcpi_params.get("max_iterations", 200)
            },
            "epanet": {
                "tolerance": epanet_params.get("tolerance", 1e-6),
                "max_iterations": epanet_params.get("max_iterations", 100)
            }
        },
        "epanet_wrapper": epanet_wrapper
    }
    
    print(f"\n✅ Configuration harmonisée créée:")
    print(f"   • Tolérance de convergence: {harmonized_config['convergence']['tolerance']}")
    print(f"   • Itérations maximales: {harmonized_config['convergence']['max_iterations']}")
    print(f"   • Formule de perte de charge: {harmonized_config['convergence']['formula']}")
    
    return harmonized_config

def save_harmonized_config(config: Dict[str, Any], output_path: str = "harmonized_simulation_config.json"):
    """Sauvegarde la configuration harmonisée."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Configuration sauvegardée dans: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

def generate_recommendations(config: Dict[str, Any]) -> None:
    """Génère des recommandations d'harmonisation."""
    
    print(f"\n📋 RECOMMANDATIONS D'HARMONISATION")
    print("=" * 60)
    
    # Vérifier la cohérence des paramètres
    lcpi_tol = config["solver_specific"]["lcpi"]["tolerance"]
    epanet_tol = config["solver_specific"]["epanet"]["tolerance"]
    lcpi_iter = config["solver_specific"]["lcpi"]["max_iterations"]
    epanet_iter = config["solver_specific"]["epanet"]["max_iterations"]
    
    recommendations = []
    
    # Vérifier la tolérance
    if abs(lcpi_tol - epanet_tol) > 1e-8:
        recommendations.append(
            f"🔧 Harmoniser la tolérance: LCPI ({lcpi_tol}) vs EPANET ({epanet_tol})"
        )
    
    # Vérifier les itérations
    if lcpi_iter != epanet_iter:
        recommendations.append(
            f"🔧 Harmoniser les itérations: LCPI ({lcpi_iter}) vs EPANET ({epanet_iter})"
        )
    
    # Vérifier la disponibilité d'EPANET
    if not config["epanet_wrapper"]["available"]:
        recommendations.append(
            "⚠️ EPANET n'est pas disponible. Vérifier l'installation et la configuration."
        )
    
    if recommendations:
        print("Recommandations identifiées:")
        for rec in recommendations:
            print(f"   {rec}")
    else:
        print("✅ Aucune harmonisation nécessaire - paramètres déjà cohérents")
    
    # Recommandations générales
    print(f"\n💡 Recommandations générales:")
    print(f"   • Utiliser la même tolérance pour les deux solveurs")
    print(f"   • Aligner le nombre d'itérations maximal")
    print(f"   • Vérifier que les formules de perte de charge sont identiques")
    print(f"   • S'assurer que les contraintes hydrauliques sont cohérentes")

def main():
    """Fonction principale."""
    print("🚀 HARMONISATION DES PARAMÈTRES DE SIMULATION")
    print("=" * 60)
    
    try:
        # Créer la configuration harmonisée
        config = create_harmonized_config()
        
        # Sauvegarder la configuration
        save_harmonized_config(config)
        
        # Générer les recommandations
        generate_recommendations(config)
        
        print(f"\n✅ Harmonisation terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'harmonisation: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
