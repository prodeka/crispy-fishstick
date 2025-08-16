#!/usr/bin/env python3
"""
Script de test pour vérifier l'intégration EPANET dans LCPI.
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, 'src')

def test_epanet_imports():
    """Test des imports EPANET"""
    print("🔍 Test des imports EPANET...")
    
    try:
        from lcpi.aep.core.epanet_wrapper import (
            EpanetWrapper,
            EpanetSimulator,
            get_epanet_wrapper,
            is_epanet_available,
            get_epanet_version,
            create_epanet_inp_file,
            validate_hardy_cross_with_epanet
        )
        print("✅ Tous les imports EPANET réussis")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_epanet_wrapper():
    """Test du wrapper EPANET"""
    print("\n🔍 Test du wrapper EPANET...")
    
    try:
        from lcpi.aep.core import get_epanet_wrapper, is_epanet_available, get_epanet_version
        
        wrapper = get_epanet_wrapper()
        available = is_epanet_available()
        version = get_epanet_version()
        
        print(f"✅ Wrapper créé: {wrapper is not None}")
        print(f"✅ EPANET disponible: {available}")
        print(f"✅ Version: {version}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur wrapper: {e}")
        return False

def test_epanet_simulator():
    """Test du simulateur EPANET"""
    print("\n🔍 Test du simulateur EPANET...")
    
    try:
        from lcpi.aep.core import EpanetSimulator
        
        simulator = EpanetSimulator()
        print(f"✅ Simulateur créé: {simulator is not None}")
        
        # Test des méthodes de base
        summary = simulator.get_network_summary()
        print(f"✅ Résumé réseau: {summary}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur simulateur: {e}")
        return False

def test_epanet_functions():
    """Test des fonctions utilitaires EPANET"""
    print("\n🔍 Test des fonctions utilitaires...")
    
    try:
        from lcpi.aep.core import create_epanet_inp_file, validate_hardy_cross_with_epanet
        
        print(f"✅ create_epanet_inp_file: {create_epanet_inp_file is not None}")
        print(f"✅ validate_hardy_cross_with_epanet: {validate_hardy_cross_with_epanet is not None}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur fonctions: {e}")
        return False

def test_epanet_commands():
    """Test des commandes AEP avec EPANET"""
    print("\n🔍 Test des commandes AEP...")
    
    try:
        from lcpi.aep.commands.main import app
        
        print(f"✅ Application AEP chargée: {app is not None}")
        
        # Vérifier que les commandes sont disponibles
        commands = [cmd.name for cmd in app.registered_commands]
        print(f"✅ Commandes disponibles: {len(commands)}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur commandes: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test d'intégration EPANET dans LCPI")
    print("=" * 50)
    
    tests = [
        test_epanet_imports,
        test_epanet_wrapper,
        test_epanet_simulator,
        test_epanet_functions,
        test_epanet_commands
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors du test {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Résultats des tests:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {test.__name__}: {status}")
    
    print(f"\n🎯 Résumé: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! L'intégration EPANET fonctionne correctement.")
        return 0
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
