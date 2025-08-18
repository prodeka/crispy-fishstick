#!/usr/bin/env python3
"""
Test du système de session LCPI.
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_session_manager():
    """Test du gestionnaire de session."""
    print("🧪 Test du gestionnaire de session LCPI")
    print("=" * 50)
    
    try:
        from lcpi.core.session_manager import session_manager
        
        print("✅ SessionManager importé avec succès")
        
        # Afficher le registre de plugins
        print(f"\n📋 Registre de plugins: {session_manager.list_registered_plugins()}")
        
        # Test de création de session
        print("\n📝 Test de création de session...")
        plugins_info = {
            'cm': {'status': 'loaded', 'path': 'cm.main'},
            'aep': {'status': 'loaded', 'path': 'aep.cli'}
        }
        
        session_manager.create_session(plugins_info, 1234567890.0)
        print("✅ Session créée")
        
        # Test de validation de session
        print("\n🔍 Test de validation de session...")
        is_valid = session_manager.is_session_valid()
        print(f"Session valide: {is_valid}")
        
        # Test d'info de session
        print("\n📊 Test d'info de session...")
        session_info = session_manager.get_session_info()
        print(f"Info session: {session_info}")
        
        # Test de restauration (sans app Typer)
        print("\n🔄 Test de restauration de plugins...")
        # Créer un mock app pour le test
        class MockApp:
            def add_typer(self, typer_app, name):
                print(f"  Mock: Plugin {name} ajouté")
        
        mock_app = MockApp()
        restored = session_manager.restore_plugins_from_session(mock_app)
        print(f"Plugins restaurés: {restored}")
        
        # Nettoyer
        session_manager.clear_session()
        print("\n🧹 Session nettoyée")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_session_manager()
