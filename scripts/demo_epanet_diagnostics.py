#!/usr/bin/env python3
"""
Démonstration de l'intégration EPANET avec diagnostics de connectivité

Ce script démontre comment utiliser la nouvelle fonctionnalité de diagnostic
automatique de connectivité réseau avant l'exécution d'EPANET pour prévenir
l'erreur 110 "cannot solve network hydraulic equations".
"""

import sys
import os
import yaml
import json
from pathlib import Path

# Ajouter le répertoire src au path pour importer les modules LCPI
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.core.epanet_integration import (
    run_epanet_with_diagnostics,
    quick_diagnostic,
    EpanetWithDiagnostics
)


def create_test_networks():
    """Crée des réseaux de test avec différents scénarios"""
    
    # Réseau 1: Réseau valide (devrait fonctionner avec EPANET)
    valid_network = {
        "network": {
            "nodes": {
                "R1": {"type": "reservoir", "cote": 120, "demande": 0},
                "N1": {"type": "junction", "cote": 100, "demande": 10},
                "N2": {"type": "junction", "cote": 95, "demande": 15},
                "N3": {"type": "junction", "cote": 90, "demande": 8}
            },
            "pipes": {
                "P1": {"noeud_amont": "R1", "noeud_aval": "N1", "longueur": 1000, "diametre": 0.3, "coefficient_rugosite": 120},
                "P2": {"noeud_amont": "N1", "noeud_aval": "N2", "longueur": 800, "diametre": 0.25, "coefficient_rugosite": 120},
                "P3": {"noeud_amont": "N2", "noeud_aval": "N3", "longueur": 600, "diametre": 0.2, "coefficient_rugosite": 120}
            }
        }
    }
    
    # Réseau 2: Réseau avec composante orpheline (devrait échouer)
    orphaned_network = {
        "network": {
            "nodes": {
                "R1": {"type": "reservoir", "cote": 120, "demande": 0},
                "N1": {"type": "junction", "cote": 100, "demande": 10},
                "N2": {"type": "junction", "cote": 95, "demande": 15},
                "N3": {"type": "junction", "cote": 90, "demande": 8},
                "N4": {"type": "junction", "cote": 85, "demande": 12},
                "N5": {"type": "junction", "cote": 80, "demande": 6}
            },
            "pipes": {
                "P1": {"noeud_amont": "R1", "noeud_aval": "N1", "longueur": 1000, "diametre": 0.3, "coefficient_rugosite": 120},
                "P2": {"noeud_amont": "N1", "noeud_aval": "N2", "longueur": 800, "diametre": 0.25, "coefficient_rugosite": 120},
                "P3": {"noeud_amont": "N2", "noeud_aval": "N3", "longueur": 600, "diametre": 0.2, "coefficient_rugosite": 120},
                "P4": {"noeud_amont": "N4", "noeud_aval": "N5", "longueur": 500, "diametre": 0.15, "coefficient_rugosite": 120}
            }
        }
    }
    
    # Réseau 3: Réseau sans source d'eau (devrait échouer)
    no_source_network = {
        "network": {
            "nodes": {
                "N1": {"type": "junction", "cote": 100, "demande": 10},
                "N2": {"type": "junction", "cote": 95, "demande": 15},
                "N3": {"type": "junction", "cote": 90, "demande": 8}
            },
            "pipes": {
                "P1": {"noeud_amont": "N1", "noeud_aval": "N2", "longueur": 800, "diametre": 0.25, "coefficient_rugosite": 120},
                "P2": {"noeud_amont": "N2", "noeud_aval": "N3", "longueur": 600, "diametre": 0.2, "coefficient_rugosite": 120}
            }
        }
    }
    
    return {
        "valid": valid_network,
        "orphaned": orphaned_network,
        "no_source": no_source_network
    }


def demo_quick_diagnostic():
    """Démonstration du diagnostic rapide"""
    
    print("🔍 DÉMONSTRATION: DIAGNOSTIC RAPIDE")
    print("=" * 50)
    
    networks = create_test_networks()
    
    for network_name, network_data in networks.items():
        print(f"\n📋 Test du réseau '{network_name.upper()}':")
        print("-" * 40)
        
        try:
            # Diagnostic rapide
            results = quick_diagnostic(network_data)
            
            print(f"   • Connectivité: {'✅' if results['connectivity'] else '❌'}")
            print(f"   • Compatible EPANET: {'✅' if results['epanet_compatible'] else '❌'}")
            
            if results['errors']:
                print(f"   • Erreurs: {len(results['errors'])}")
                for error in results['errors']:
                    print(f"     - {error}")
            
            if results['warnings']:
                print(f"   • Avertissements: {len(results['warnings'])}")
                for warning in results['warnings']:
                    print(f"     - {warning}")
            
            if results['topology']:
                print(f"   • Densité réseau: {results['topology'].get('densite', 'N/A'):.4f}")
                print(f"   • Composantes connexes: {results['topology'].get('composantes_connexes', 'N/A')}")
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")


def demo_epanet_integration():
    """Démonstration de l'intégration EPANET avec diagnostics"""
    
    print("\n⚡ DÉMONSTRATION: INTÉGRATION EPANET AVEC DIAGNOSTICS")
    print("=" * 60)
    
    networks = create_test_networks()
    
    for network_name, network_data in networks.items():
        print(f"\n{'='*80}")
        print(f"🌐 SIMULATION: Réseau '{network_name.upper()}'")
        print(f"{'='*80}")
        
        try:
            # Simulation EPANET avec diagnostics
            results = run_epanet_with_diagnostics(network_data)
            
            # Affichage des résultats
            print(f"\n📊 RÉSULTATS DE LA SIMULATION:")
            print(f"   • Succès: {'✅' if results['success'] else '❌'}")
            
            if results['success']:
                print(f"   • Statistiques EPANET:")
                stats = results['epanet_results'].get('statistics', {})
                print(f"     - Itérations: {stats.get('iterations', 'N/A')}")
                print(f"     - Erreur relative: {stats.get('relative_error', 'N/A'):.2e}")
                print(f"     - Erreur max tête: {stats.get('max_head_error', 'N/A'):.2e}")
                print(f"     - Changement max débit: {stats.get('max_flow_change', 'N/A'):.2e}")
                print(f"     - Bilan de masse: {stats.get('mass_balance', 'N/A'):.2e}")
                
                print(f"   • Résultats nœuds: {len(results['epanet_results'].get('nodes', {}))}")
                print(f"   • Résultats conduites: {len(results['epanet_results'].get('pipes', {}))}")
            
            if results['errors']:
                print(f"   • Erreurs: {len(results['errors'])}")
                for error in results['errors']:
                    print(f"     - {error}")
            
            if results['warnings']:
                print(f"   • Avertissements: {len(results['warnings'])}")
                for warning in results['warnings']:
                    print(f"     - {warning}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la simulation: {e}")
        
        print(f"\n{'-'*80}")


def demo_with_real_file():
    """Démonstration avec un fichier réseau réel"""
    
    print("\n🌐 DÉMONSTRATION: FICHIER RÉSEAU RÉEL")
    print("=" * 50)
    
    # Chercher un fichier réseau valide
    test_file = "examples/reseau_test_avec_source.yml"
    
    if os.path.exists(test_file):
        print(f"📁 Test avec le fichier: {test_file}")
        
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                network_data = yaml.safe_load(f)
            
            print("✅ Fichier chargé avec succès")
            
            # Diagnostic rapide
            print("\n🔍 Diagnostic rapide:")
            results = quick_diagnostic(network_data)
            
            print(f"   • Connectivité: {'✅' if results['connectivity'] else '❌'}")
            print(f"   • Compatible EPANET: {'✅' if results['epanet_compatible'] else '❌'}")
            
            if results['connectivity'] and results['epanet_compatible']:
                print("\n⚡ Simulation EPANET (optionnelle):")
                print("   • Pour lancer la simulation complète, décommentez la ligne suivante:")
                print("   • run_epanet_with_diagnostics(network_data)")
                
                # Décommentez la ligne suivante pour tester la simulation complète
                # epanet_results = run_epanet_with_diagnostics(network_data)
                # print(f"   • Résultat: {'✅ Succès' if epanet_results['success'] else '❌ Échec'}")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
    else:
        print(f"⚠️  Fichier de test non trouvé: {test_file}")


def main():
    """Fonction principale de démonstration"""
    
    print("🚀 DÉMONSTRATION: DIAGNOSTIC DE CONNECTIVITÉ RÉSEAU")
    print("=" * 60)
    print("Ce script démontre l'utilisation des nouvelles fonctionnalités de")
    print("diagnostic de connectivité réseau pour prévenir l'erreur EPANET 110.")
    print("=" * 60)
    
    # Démonstration 1: Diagnostic rapide
    demo_quick_diagnostic()
    
    # Démonstration 2: Intégration EPANET
    demo_epanet_integration()
    
    # Démonstration 3: Fichier réel
    demo_with_real_file()
    
    print(f"\n{'='*60}")
    print("✅ DÉMONSTRATION TERMINÉE")
    print("=" * 60)
    
    print("\n💡 UTILISATION DANS VOTRE CODE:")
    print("   • Importez: from lcpi.aep.core.epanet_integration import run_epanet_with_diagnostics")
    print("   • Utilisez: results = run_epanet_with_diagnostics(network_data)")
    print("   • Vérifiez: if results['success']: ...")
    
    print("\n🔧 AVANTAGES:")
    print("   • Diagnostic automatique avant EPANET")
    print("   • Prévention de l'erreur 110")
    print("   • Messages d'erreur clairs et actionables")
    print("   • Analyse topologique complète")
    print("   • Validation de compatibilité EPANET")
    
    print("\n📋 PROCHAINES ÉTAPES:")
    print("   • Intégrez cette fonction dans votre workflow EPANET existant")
    print("   • Remplacez les appels directs à EPANET par run_epanet_with_diagnostics")
    print("   • Utilisez les diagnostics pour corriger vos réseaux problématiques")


if __name__ == "__main__":
    main() 