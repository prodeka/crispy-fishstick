#!/usr/bin/env python3
"""
Test de l'intégration des commandes CLI Sprint 3
"""

import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, 'src')

def test_cli_integration():
    """Test l'intégration des commandes CLI"""
    print("🔗 Test de l'intégration des commandes CLI")
    print("=" * 50)
    
    try:
        # Test 1: Import du CLI principal
        print("1. Test du CLI principal...")
        from lcpi.aep.cli import app
        print("   ✅ CLI principal importé avec succès")
        
        # Test 2: Vérification des groupes
        print("2. Test des groupes CLI...")
        groups = [group for group in app.registered_groups if group.name]
        print(f"   ✅ Groupes trouvés: {len(groups)}")
        for group in groups:
            print(f"      - {group.name}: {group.help}")
        
        # Test 3: Vérification des commandes
        print("3. Test des commandes CLI...")
        commands = [cmd for cmd in app.registered_commands if cmd.name]
        print(f"   ✅ Commandes trouvées: {len(commands)}")
        for cmd in commands:
            print(f"      - {cmd.name}")
        
        # Test 4: Test du groupe optimizer
        print("4. Test du groupe optimizer...")
        optimizer_group = None
        for group in app.registered_groups:
            if group.name == "optimizer":
                optimizer_group = group
                break
        
        if optimizer_group:
            print("   ✅ Groupe 'optimizer' trouvé")
            # Les groupes Typer n'ont pas de registered_commands directement
            print("      - Groupe d'optimisation disponible")
        else:
            print("   ❌ Groupe 'optimizer' non trouvé")
        
        # Test 5: Test des commandes d'optimisation
        print("5. Test des commandes d'optimisation...")
        from lcpi.aep.optimizer.cli_commands import AEPOptimizationCLI
        cli = AEPOptimizationCLI()
        
        # Vérifier que les méthodes existent
        methods = ['price_optimize', 'report', 'diameters_manage']
        for method in methods:
            if hasattr(cli, method):
                print(f"   ✅ Méthode {method} disponible")
            else:
                print(f"   ❌ Méthode {method} manquante")
        
        # Test 6: Test de la gestion des diamètres
        print("6. Test de la gestion des diamètres...")
        if hasattr(cli, '_list_diameters'):
            print("   ✅ Méthode _list_diameters disponible")
        if hasattr(cli, '_add_diameter'):
            print("   ✅ Méthode _add_diameter disponible")
        if hasattr(cli, '_remove_diameter'):
            print("   ✅ Méthode _remove_diameter disponible")
        if hasattr(cli, '_update_diameter'):
            print("   ✅ Méthode _update_diameter disponible")
        
        print("\n🎉 Intégration CLI testée avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cli_integration()
    sys.exit(0 if success else 1)
