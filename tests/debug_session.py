#!/usr/bin/env python3
"""
Debug du système de session LCPI.
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def debug_session():
    """Debug du système de session."""
    print("🔍 Debug du système de session LCPI")
    print("=" * 50)
    
    try:
        from lcpi.core.session_manager import session_manager
        
        print("✅ SessionManager importé avec succès")
        
        # Vérifier s'il y a des sessions existantes
        print(f"\n📁 Répertoire de sessions: {session_manager._session_dir}")
        session_files = list(session_manager._session_dir.glob("session_*.json"))
        print(f"📄 Fichiers de session trouvés: {len(session_files)}")
        for f in session_files:
            print(f"   - {f.name}")
        
        # Vérifier la validation de session
        print(f"\n🔍 Validation de session:")
        is_valid = session_manager.is_session_valid()
        print(f"   Session valide: {is_valid}")
        
        if is_valid:
            session_data = session_manager.get_session_data()
            print(f"   Données de session: {session_data}")
        else:
            print("   Aucune session valide trouvée")
        
        # Vérifier l'environnement
        print(f"\n🌍 Hash environnement actuel:")
        env_hash = session_manager._get_current_environment_hash()
        print(f"   Hash: {env_hash}")
        
        # Examiner le contenu d'une session
        if session_files:
            print(f"\n📖 Contenu de la première session:")
            first_session = session_files[0]
            try:
                import json
                with open(first_session, 'r', encoding='utf-8') as f:
                    session_content = json.load(f)
                print(f"   Fichier: {first_session.name}")
                print(f"   Hash dans la session: {session_content.get('environment_hash', 'N/A')}")
                print(f"   Hash actuel: {env_hash}")
                print(f"   Hashs identiques: {session_content.get('environment_hash') == env_hash}")
                print(f"   Plugins: {list(session_content.get('plugins', {}).keys())}")
            except Exception as e:
                print(f"   Erreur lecture session: {e}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_session()
