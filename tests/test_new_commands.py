#!/usr/bin/env python3
"""
Test simple des nouvelles commandes CLI créées.
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test que tous les modules peuvent être importés."""
    print("🧪 Test des imports des nouvelles commandes...")
    
    try:
        # Test des commandes de base
        from lcpi.aep.commands import network_optimize
        print("✅ network_optimize importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import network_optimize: {e}")
    
    try:
        # Test des nouvelles commandes
        from lcpi.aep.commands import solvers
        print("✅ solvers importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import solvers: {e}")
    
    try:
        from lcpi.aep.commands import data_management
        print("✅ data_management importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import data_management: {e}")
    
    try:
        from lcpi.aep.commands import project_management
        print("✅ project_management importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import project_management: {e}")
    
    try:
        from lcpi.aep.commands import main
        print("✅ main importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import main: {e}")

def test_command_structure():
    """Test la structure des commandes."""
    print("\n🔧 Test de la structure des commandes...")
    
    try:
        from lcpi.aep.commands.main import app
        
        # Vérifier que l'app principal existe
        if hasattr(app, 'commands'):
            print("✅ Commande principale lcpi créée avec succès")
            print(f"   Nombre de commandes: {len(app.commands)}")
            
            # Lister les commandes disponibles
            for cmd_name, cmd_info in app.commands.items():
                print(f"   - {cmd_name}: {cmd_info.help or 'Aucune description'}")
        else:
            print("❌ Commande principale n'a pas de sous-commandes")
            
    except Exception as e:
        print(f"❌ Erreur lors du test de la structure: {e}")

def test_solvers_commands():
    """Test des commandes de gestion des solveurs."""
    print("\n🔧 Test des commandes solveurs...")
    
    try:
        from lcpi.aep.commands.solvers import app as solvers_app
        
        if hasattr(solvers_app, 'commands'):
            print("✅ Commandes solveurs créées avec succès")
            print(f"   Nombre de commandes: {len(solvers_app.commands)}")
            
            for cmd_name, cmd_info in solvers_app.commands.items():
                print(f"   - {cmd_name}: {cmd_info.help or 'Aucune description'}")
        else:
            print("❌ Commandes solveurs n'ont pas de sous-commandes")
            
    except Exception as e:
        print(f"❌ Erreur lors du test des commandes solveurs: {e}")

def test_data_commands():
    """Test des commandes de gestion des données."""
    print("\n📊 Test des commandes data...")
    
    try:
        from lcpi.aep.commands.data_management import app as data_app
        
        if hasattr(data_app, 'commands'):
            print("✅ Commandes data créées avec succès")
            print(f"   Nombre de commandes: {len(data_app.commands)}")
            
            for cmd_name, cmd_info in data_app.commands.items():
                print(f"   - {cmd_name}: {cmd_info.help or 'Aucune description'}")
        else:
            print("❌ Commandes data n'ont pas de sous-commandes")
            
    except Exception as e:
        print(f"❌ Erreur lors du test des commandes data: {e}")

def test_project_commands():
    """Test des commandes de gestion des projets."""
    print("\n📁 Test des commandes project...")
    
    try:
        from lcpi.aep.commands.project_management import app as project_app
        
        if hasattr(project_app, 'commands'):
            print("✅ Commandes project créées avec succès")
            print(f"   Nombre de commandes: {len(project_app.commands)}")
            
            for cmd_name, cmd_info in project_app.commands.items():
                print(f"   - {cmd_name}: {cmd_info.help or 'Aucune description'}")
        else:
            print("❌ Commandes project n'ont pas de sous-commandes")
            
    except Exception as e:
        print(f"❌ Erreur lors du test des commandes project: {e}")

def main():
    """Fonction principale de test."""
    print("🚀 Test des Nouvelles Commandes CLI LCPI-AEP")
    print("=" * 50)
    
    # Tests des imports
    test_imports()
    
    # Tests de la structure
    test_command_structure()
    
    # Tests des commandes spécifiques
    test_solvers_commands()
    test_data_commands()
    test_project_commands()
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés !")
    print("\n📋 Résumé des commandes disponibles:")
    print("   lcpi --help                    # Aide principale")
    print("   lcpi version                   # Version des modules")
    print("   lcpi status                    # Statut des modules")
    print("   lcpi solveurs --help           # Aide des solveurs")
    print("   lcpi data --help               # Aide de la gestion des données")
    print("   lcpi project --help            # Aide de la gestion des projets")
    print("   lcpi network --help            # Aide de l'optimisation")

if __name__ == "__main__":
    main()
