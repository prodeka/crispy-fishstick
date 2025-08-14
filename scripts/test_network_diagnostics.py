#!/usr/bin/env python3
"""
Script de test pour le diagnostic de connectivité réseau

Ce script démontre l'utilisation des fonctions de diagnostic
pour identifier les problèmes de connectivité dans les réseaux hydrauliques.
"""

import sys
import os
import yaml
from pathlib import Path

# Ajouter le répertoire src au path pour importer les modules LCPI
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.core.network_diagnostics import (
    diagnose_network_connectivity,
    analyze_network_topology,
    validate_epanet_compatibility
)


def create_test_networks():
    """Crée des réseaux de test avec différents problèmes de connectivité"""
    
    # Réseau 1: Réseau valide avec une source d'eau
    valid_network = {
        "network": {
            "nodes": {
                "R1": {"type": "reservoir", "cote": 100, "demande": 0},
                "N1": {"type": "junction", "cote": 90, "demande": 10},
                "N2": {"type": "junction", "cote": 85, "demande": 15},
                "N3": {"type": "junction", "cote": 80, "demande": 8}
            },
            "pipes": {
                "P1": {"noeud_amont": "R1", "noeud_aval": "N1", "longueur": 1000, "diametre": 0.3},
                "P2": {"noeud_amont": "N1", "noeud_aval": "N2", "longueur": 800, "diametre": 0.25},
                "P3": {"noeud_amont": "N2", "noeud_aval": "N3", "longueur": 600, "diametre": 0.2}
            }
        }
    }
    
    # Réseau 2: Réseau avec composante orpheline (pas de source d'eau)
    orphaned_network = {
        "network": {
            "nodes": {
                "R1": {"type": "reservoir", "cote": 100, "demande": 0},
                "N1": {"type": "junction", "cote": 90, "demande": 10},
                "N2": {"type": "junction", "cote": 85, "demande": 15},
                "N3": {"type": "junction", "cote": 80, "demande": 8},
                "N4": {"type": "junction", "cote": 75, "demande": 12},
                "N5": {"type": "junction", "cote": 70, "demande": 6}
            },
            "pipes": {
                "P1": {"noeud_amont": "R1", "noeud_aval": "N1", "longueur": 1000, "diametre": 0.3},
                "P2": {"noeud_amont": "N1", "noeud_aval": "N2", "longueur": 800, "diametre": 0.25},
                "P3": {"noeud_amont": "N2", "noeud_aval": "N3", "longueur": 600, "diametre": 0.2},
                "P4": {"noeud_amont": "N4", "noeud_aval": "N5", "longueur": 500, "diametre": 0.15}
            }
        }
    }
    
    # Réseau 3: Réseau sans source d'eau
    no_source_network = {
        "network": {
            "nodes": {
                "N1": {"type": "junction", "cote": 90, "demande": 10},
                "N2": {"type": "junction", "cote": 85, "demande": 15},
                "N3": {"type": "junction", "cote": 80, "demande": 8}
            },
            "pipes": {
                "P1": {"noeud_amont": "N1", "noeud_aval": "N2", "longueur": 800, "diametre": 0.25},
                "P2": {"noeud_amont": "N2", "noeud_aval": "N3", "longueur": 600, "diametre": 0.2}
            }
        }
    }
    
    return {
        "valid": valid_network,
        "orphaned": orphaned_network,
        "no_source": no_source_network
    }


def test_network_diagnostics():
    """Teste les fonctions de diagnostic sur différents réseaux"""
    
    print("🧪 TEST DES FONCTIONS DE DIAGNOSTIC RÉSEAU")
    print("=" * 50)
    
    networks = create_test_networks()
    
    for network_name, network_data in networks.items():
        print(f"\n{'='*60}")
        print(f"📋 TEST: Réseau '{network_name.upper()}'")
        print(f"{'='*60}")
        
        try:
            # Test 1: Diagnostic de connectivité
            print(f"\n🔍 1. DIAGNOSTIC DE CONNECTIVITÉ")
            is_connected = diagnose_network_connectivity(network_data)
            print(f"Résultat: {'✅ CONNECTÉ' if is_connected else '❌ NON CONNECTÉ'}")
            
            # Test 2: Analyse topologique
            print(f"\n🔬 2. ANALYSE TOPOLOGIQUE")
            topology = analyze_network_topology(network_data)
            
            # Test 3: Validation EPANET
            print(f"\n🔧 3. VALIDATION EPANET")
            validation = validate_epanet_compatibility(network_data)
            
            # Résumé
            print(f"\n📊 RÉSUMÉ DU TEST '{network_name.upper()}':")
            print(f"   • Connectivité: {'✅' if is_connected else '❌'}")
            print(f"   • Compatibilité EPANET: {'✅' if validation['compatible'] else '❌'}")
            print(f"   • Erreurs détectées: {len(validation['erreurs'])}")
            print(f"   • Avertissements: {len(validation['avertissements'])}")
            
        except Exception as e:
            print(f"❌ Erreur lors du test du réseau '{network_name}': {e}")
        
        print(f"\n{'-'*60}")


def test_with_real_network():
    """Test avec un réseau réel (si disponible)"""
    
    print(f"\n{'='*60}")
    print(f"🌐 TEST AVEC RÉSEAU RÉEL")
    print(f"{'='*60}")
    
    # Chercher un fichier réseau dans les exemples
    example_files = [
        "examples/hardy_cross_test.yml",
        "examples/canal_exemple.yml",
        "data/canaux_a_dimensionner.csv"
    ]
    
    for file_path in example_files:
        if os.path.exists(file_path):
            print(f"\n📁 Test avec le fichier: {file_path}")
            
            try:
                if file_path.endswith('.yml'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        network_data = yaml.safe_load(f)
                    
                    # Adapter la structure si nécessaire
                    if "network" not in network_data:
                        print("   ⚠️  Structure de données non standard, adaptation...")
                        # Créer une structure compatible
                        if "canal" in network_data:
                            # C'est un fichier canal, pas un réseau
                            print("   ℹ️  Fichier canal détecté, ignoré")
                            continue
                    
                    print("   ✅ Fichier chargé avec succès")
                    
                    # Test rapide de connectivité
                    try:
                        is_connected = diagnose_network_connectivity(network_data)
                        print(f"   • Connectivité: {'✅' if is_connected else '❌'}")
                    except Exception as e:
                        print(f"   • Erreur diagnostic: {e}")
                
                elif file_path.endswith('.csv'):
                    print("   ℹ️  Fichier CSV détecté, conversion nécessaire")
                    # Ici on pourrait ajouter la conversion CSV vers le format réseau
                    continue
                    
            except Exception as e:
                print(f"   ❌ Erreur lors du chargement: {e}")
            
            break
    else:
        print("   ℹ️  Aucun fichier réseau de test trouvé")


def main():
    """Fonction principale"""
    
    print("🚀 DÉMARRAGE DES TESTS DE DIAGNOSTIC RÉSEAU")
    print("=" * 60)
    
    # Test 1: Réseaux de test
    test_network_diagnostics()
    
    # Test 2: Réseau réel
    test_with_real_network()
    
    print(f"\n{'='*60}")
    print("✅ TESTS TERMINÉS")
    print("=" * 60)
    print("\n💡 UTILISATION:")
    print("   • Importez le module: from lcpi.aep.core.network_diagnostics import diagnose_network_connectivity")
    print("   • Appelez la fonction: diagnose_network_connectivity(network_data)")
    print("   • La fonction retourne True si le réseau est entièrement alimenté")
    print("\n🔧 INTÉGRATION:")
    print("   • Ajoutez cette fonction avant l'appel à EPANET")
    print("   • Utilisez-la pour diagnostiquer l'erreur 110")
    print("   • Corrigez les problèmes de connectivité identifiés")


if __name__ == "__main__":
    main() 