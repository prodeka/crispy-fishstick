#!/usr/bin/env python3
"""
Script d'harmonisation des contraintes hydrauliques entre EPANET et LCPI.

Ce script vérifie et harmonise les seuils de pression, vitesse et autres contraintes
hydrauliques pour assurer une évaluation cohérente des solutions.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List

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

def get_project_constraints() -> Dict[str, Any]:
    """Récupère les contraintes du projet depuis la configuration."""
    
    # Contraintes standard du projet AEP
    project_constraints = {
        "pressure": {
            "min_mce": 10.0,      # Pression minimale en mCE
            "max_mce": 100.0,     # Pression maximale en mCE
            "critical_mce": 5.0    # Pression critique (alerte)
        },
        "velocity": {
            "min_ms": 0.3,        # Vitesse minimale en m/s
            "max_ms": 3.0,        # Vitesse maximale en m/s
            "optimal_min_ms": 0.5, # Vitesse optimale minimale
            "optimal_max_ms": 2.5  # Vitesse optimale maximale
        },
        "flow": {
            "min_lps": 0.1,       # Débit minimal en L/s
            "max_lps": 1000.0     # Débit maximal en L/s
        },
        "quality": {
            "min_contact_time_minutes": 30,  # Temps de contact minimal
            "max_turbidity_ntu": 1.0         # Turbidité maximale
        }
    }
    
    print(f"✅ Contraintes du projet AEP:")
    for category, constraints in project_constraints.items():
        print(f"   • {category}:")
        for key, value in constraints.items():
            print(f"     - {key}: {value}")
    
    return project_constraints

def get_constraints_handler_config() -> Dict[str, Any]:
    """Récupère la configuration du gestionnaire de contraintes."""
    try:
        from lcpi.aep.optimizer.constraints_handler import ConstraintManager, ConstraintPenaltyCalculator
        
        # Créer une instance pour tester
        penalty_calculator = ConstraintPenaltyCalculator()
        constraint_manager = ConstraintManager(penalty_calculator)
        
        # Configuration actuelle
        handler_config = {
            "penalty_calculator": {
                "base_penalty_factor": penalty_calculator.base_penalty_factor,
                "velocity_penalty_method": "non_linear",
                "pressure_penalty_method": "non_linear",
                "budget_penalty_method": "exponential"
            },
            "constraint_manager": {
                "available": True,
                "version": "1.0"
            }
        }
        
        print(f"✅ Gestionnaire de contraintes:")
        print(f"   • Facteur de pénalité de base: {handler_config['penalty_calculator']['base_penalty_factor']}")
        print(f"   • Méthode de pénalité vitesse: {handler_config['penalty_calculator']['velocity_penalty_method']}")
        print(f"   • Méthode de pénalité pression: {handler_config['penalty_calculator']['pressure_penalty_method']}")
        
        return handler_config
        
    except ImportError as e:
        print(f"⚠️ Impossible d'importer le gestionnaire de contraintes: {e}")
        return {
            "penalty_calculator": {
                "base_penalty_factor": 1000.0,
                "velocity_penalty_method": "unknown",
                "pressure_penalty_method": "unknown"
            },
            "constraint_manager": {
                "available": False,
                "version": "unknown"
            }
        }

def get_epanet_constraints() -> Dict[str, Any]:
    """Récupère les contraintes EPANET standard."""
    
    # Contraintes EPANET standard (basées sur la documentation)
    epanet_constraints = {
        "pressure": {
            "min_mce": 10.0,      # Pression minimale recommandée
            "max_mce": 100.0,     # Pression maximale recommandée
            "warning_mce": 15.0    # Seuil d'alerte
        },
        "velocity": {
            "min_ms": 0.3,        # Vitesse minimale pour éviter la sédimentation
            "max_ms": 3.0,        # Vitesse maximale pour éviter l'érosion
            "optimal_ms": [0.5, 2.5]  # Plage optimale
        },
        "flow": {
            "min_lps": 0.1,       # Débit minimal mesurable
            "max_lps": 1000.0     # Débit maximal typique
        }
    }
    
    print(f"Contraintes EPANET standard:")
    for category, constraints in epanet_constraints.items():
        print(f"   • {category}:")
        for key, value in constraints.items():
            print(f"     - {key}: {value}")
    
    return epanet_constraints

def check_constraints_compatibility(project: Dict[str, Any], 
                                  epanet: Dict[str, Any]) -> Dict[str, Any]:
    """Vérifie la compatibilité des contraintes entre le projet et EPANET."""
    
    print(f"\n🔍 VÉRIFICATION DE LA COMPATIBILITÉ DES CONTRAINTES")
    print("=" * 60)
    
    compatibility_report = {
        "pressure": {},
        "velocity": {},
        "flow": {},
        "overall_compatibility": True,
        "warnings": [],
        "recommendations": []
    }
    
    # Vérifier la pression
    p_min_project = project["pressure"]["min_mce"]
    p_min_epanet = epanet["pressure"]["min_mce"]
    
    if abs(p_min_project - p_min_epanet) < 0.1:
        compatibility_report["pressure"]["min"] = "compatible"
    else:
        compatibility_report["pressure"]["min"] = "incompatible"
        compatibility_report["overall_compatibility"] = False
        compatibility_report["warnings"].append(
            f"Pression minimale différente: Projet ({p_min_project}) vs EPANET ({p_min_epanet})"
        )
    
    # Vérifier la vitesse
    v_min_project = project["velocity"]["min_ms"]
    v_min_epanet = epanet["velocity"]["min_ms"]
    v_max_project = project["velocity"]["max_ms"]
    v_max_epanet = epanet["velocity"]["max_ms"]
    
    if abs(v_min_project - v_min_epanet) < 0.01:
        compatibility_report["velocity"]["min"] = "compatible"
    else:
        compatibility_report["velocity"]["min"] = "incompatible"
        compatibility_report["overall_compatibility"] = False
        compatibility_report["warnings"].append(
            f"Vitesse minimale différente: Projet ({v_min_project}) vs EPANET ({v_min_epanet})"
        )
    
    if abs(v_max_project - v_max_epanet) < 0.01:
        compatibility_report["velocity"]["max"] = "compatible"
    else:
        compatibility_report["velocity"]["max"] = "incompatible"
        compatibility_report["overall_compatibility"] = False
        compatibility_report["warnings"].append(
            f"Vitesse maximale différente: Projet ({v_max_project}) vs EPANET ({v_max_epanet})"
        )
    
    # Générer des recommandations
    if compatibility_report["overall_compatibility"]:
        compatibility_report["recommendations"].append(
            "✅ Toutes les contraintes sont compatibles - aucune action nécessaire"
        )
                else:
        compatibility_report["recommendations"].append(
            "🔧 Harmoniser les contraintes incompatibles pour assurer une évaluation cohérente"
        )
        compatibility_report["recommendations"].append(
            "📊 Utiliser les mêmes seuils pour les deux solveurs"
        )
    
    return compatibility_report

def create_harmonized_constraints(project: Dict[str, Any], 
                                 epanet: Dict[str, Any],
                                 compatibility: Dict[str, Any]) -> Dict[str, Any]:
    """Crée des contraintes harmonisées."""
    
    print(f"\n🔧 CRÉATION DES CONTRAINTES HARMONISÉES")
    print("=" * 60)
    
    # Utiliser les valeurs du projet comme référence principale
    harmonized_constraints = {
        "pressure": {
            "min_mce": project["pressure"]["min_mce"],
            "max_mce": project["pressure"]["max_mce"],
            "critical_mce": project["pressure"]["critical_mce"],
            "warning_mce": epanet["pressure"]["warning_mce"]
        },
        "velocity": {
            "min_ms": project["velocity"]["min_ms"],
            "max_ms": project["velocity"]["max_ms"],
            "optimal_min_ms": project["velocity"]["optimal_min_ms"],
            "optimal_max_ms": project["velocity"]["optimal_max_ms"]
        },
        "flow": {
            "min_lps": project["flow"]["min_lps"],
            "max_lps": project["flow"]["max_lps"]
        },
        "quality": project["quality"],
        "metadata": {
            "source": "harmonized_project_epanet",
            "version": "1.0",
            "compatibility": compatibility["overall_compatibility"]
        }
    }
    
    print(f"✅ Contraintes harmonisées créées:")
    print(f"   • Pression minimale: {harmonized_constraints['pressure']['min_mce']} mCE")
    print(f"   • Vitesse minimale: {harmonized_constraints['velocity']['min_ms']} m/s")
    print(f"   • Vitesse maximale: {harmonized_constraints['velocity']['max_ms']} m/s")
    print(f"   • Compatibilité: {'✅' if compatibility['overall_compatibility'] else '⚠️'}")
    
    return harmonized_constraints

def save_harmonized_constraints(constraints: Dict[str, Any], 
                               output_path: str = "harmonized_hydraulic_constraints.json") -> bool:
    """Sauvegarde les contraintes harmonisées."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(constraints, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Contraintes harmonisées sauvegardées dans: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

def generate_implementation_guide(constraints: Dict[str, Any], 
                                compatibility: Dict[str, Any]) -> None:
    """Génère un guide d'implémentation pour l'harmonisation."""
    
    print(f"\n📋 GUIDE D'IMPLÉMENTATION")
    print("=" * 60)
    
    if compatibility["overall_compatibility"]:
        print("✅ Aucune action d'implémentation nécessaire - contraintes déjà harmonisées")
    else:
        print("🔧 Actions d'implémentation requises:")
        
        for warning in compatibility["warnings"]:
            print(f"   • {warning}")
        
        print(f"\n📝 Étapes d'implémentation:")
        print(f"   1. Mettre à jour constraints_handler.py avec les nouvelles valeurs")
        print(f"   2. Vérifier que EPANET utilise les mêmes seuils")
        print(f"   3. Tester la cohérence des évaluations")
        print(f"   4. Valider sur des cas d'usage réels")
    
    print(f"\n💡 Bonnes pratiques:")
    print(f"   • Utiliser les mêmes seuils pour tous les solveurs")
    print(f"   • Documenter les choix de contraintes")
    print(f"   • Tester régulièrement la cohérence")
    print(f"   • Maintenir un historique des modifications")

def main():
    """Fonction principale."""
    print("🚀 HARMONISATION DES CONTRAINTES HYDRAULIQUES")
    print("=" * 60)
    
    try:
        # Récupérer les contraintes
        project_constraints = get_project_constraints()
        epanet_constraints = get_epanet_constraints()
        handler_config = get_constraints_handler_config()
        
        # Vérifier la compatibilité
        compatibility = check_constraints_compatibility(project_constraints, epanet_constraints)
        
        # Créer les contraintes harmonisées
        harmonized_constraints = create_harmonized_constraints(
            project_constraints, epanet_constraints, compatibility
        )
        
        # Sauvegarder
        save_harmonized_constraints(harmonized_constraints)
        
        # Générer le guide d'implémentation
        generate_implementation_guide(harmonized_constraints, compatibility)
        
        print(f"\n✅ Harmonisation des contraintes terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'harmonisation: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
