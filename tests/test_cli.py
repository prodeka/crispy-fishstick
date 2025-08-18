#!/usr/bin/env python3
"""
Script de test pour l'application CLI LCPI
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from lcpi.main import app
    print("✅ Application CLI importée avec succès")
    print(f"📊 Nombre de commandes: {len(app.registered_commands)}")
    print("🔍 Commandes disponibles:")
    for cmd in app.registered_commands:
        print(f"  - {cmd.name}: {cmd.help or 'Aucune description'}")
    
    print("\n🧪 Test de la commande tips...")
    from lcpi.main import tips
    tips()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
