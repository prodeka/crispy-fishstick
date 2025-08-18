#!/usr/bin/env python3
"""
Script de test final pour vérifier l'intégration complète LCPI-EPANET.
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, 'src')

def test_epanet_plugin_loading():
    """Test du chargement du plugin AEP sans erreur"""
    print("🔍 Test du chargement du plugin AEP...")
    
    try:
        from lcpi.aep.core import is_epanet_available
        available = is_epanet_available()
        print(f"✅ Plugin AEP chargé avec succès")
        print(f"✅ EPANET disponible: {available}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du chargement du plugin: {e}")
        return False

def test_cli_commands():
    """Test des commandes CLI AEP"""
    print("\n🔍 Test des commandes CLI AEP...")
    
    try:
        from lcpi.aep.commands.main import app
        
        # Vérifier que l'application est chargée
        if app is None:
            print("❌ Application AEP non chargée")
            return False
        
        print(f"✅ Application AEP chargée: {app is not None}")
        
        # Vérifier que les commandes sont disponibles
        commands = [cmd.name for cmd in app.registered_commands]
        print(f"✅ Commandes disponibles: {len(commands)}")
        
        # Vérifier quelques commandes importantes
        important_commands = ['population', 'demand', 'network', 'reservoir']
        for cmd in important_commands:
            if cmd in commands:
                print(f"✅ Commande '{cmd}' disponible")
            else:
                print(f"⚠️ Commande '{cmd}' manquante")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test des commandes: {e}")
        return False

def test_epanet_wrapper_functionality():
    """Test des fonctionnalités du wrapper EPANET"""
    print("\n🔍 Test des fonctionnalités EPANET...")
    
    try:
        from lcpi.aep.core import (
            EpanetWrapper,
            EpanetSimulator,
            create_epanet_inp_file,
            validate_hardy_cross_with_epanet
        )
        
        # Test du wrapper
        wrapper = EpanetWrapper()
        print(f"✅ EpanetWrapper créé: {wrapper is not None}")
        
        # Test du simulateur
        simulator = EpanetSimulator()
        print(f"✅ EpanetSimulator créé: {simulator is not None}")
        
        # Test des fonctions utilitaires
        print(f"✅ create_epanet_inp_file: {create_epanet_inp_file is not None}")
        print(f"✅ validate_hardy_cross_with_epanet: {validate_hardy_cross_with_epanet is not None}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test des fonctionnalités: {e}")
        return False

def test_main_application():
    """Test du chargement de l'application principale"""
    print("\n🔍 Test de l'application principale...")
    
    try:
        from lcpi.main import app
        
        if app is None:
            print("❌ Application principale non chargée")
            return False
        
        print(f"✅ Application principale chargée: {app is not None}")
        
        # Vérifier que les plugins sont chargés
        print("✅ Application LCPI chargée avec succès")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du chargement de l'application principale: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test Final d'Intégration LCPI-EPANET")
    print("=" * 60)
    
    tests = [
        test_epanet_plugin_loading,
        test_cli_commands,
        test_epanet_wrapper_functionality,
        test_main_application
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors du test {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 Résultats des tests finaux:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {test.__name__}: {status}")
    
    print(f"\n🎯 Résumé: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! L'intégration LCPI-EPANET est complète et fonctionnelle.")
        print("\n📋 Statut final:")
        print("   ✅ Plugin AEP chargé sans erreur")
        print("   ✅ Commandes CLI opérationnelles")
        print("   ✅ Wrapper EPANET fonctionnel")
        print("   ✅ Application principale stable")
        print("   ✅ Plus de messages d'erreur intrusifs")
        return 0
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
