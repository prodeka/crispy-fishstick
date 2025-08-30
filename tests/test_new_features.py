#!/usr/bin/env python3
"""
Script de test pour les nouvelles fonctionnalités de la classe PriceDB :
- Timestamp de chargement
- Méthode reload
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour pouvoir importer src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.lcpi.aep.optimizer.db import PriceDB
import time

def test_new_features():
    """Teste les nouvelles fonctionnalités de PriceDB."""
    print("=== Test des nouvelles fonctionnalités PriceDB ===\n")
    
    try:
        # Créer une instance
        print("1. Création d'une instance PriceDB...")
        db = PriceDB()
        print("   ✓ Instance créée avec succès !")
        
        # Vérifier le timestamp
        print("\n2. Vérification du timestamp de chargement :")
        info = db.get_database_info()
        timestamp = info.get('timestamp_utc')
        print(f"   Timestamp UTC: {timestamp}")
        print(f"   Timestamp présent: {'✓' if timestamp else '❌'}")
        
        # Vérifier le nombre initial de diamètres
        initial_count = info.get('diameter_count', 0)
        print(f"   Nombre initial de diamètres: {initial_count}")
        
        # Test de la méthode reload
        print("\n3. Test de la méthode reload :")
        print("   Attente de 2 secondes pour simuler un délai...")
        time.sleep(2)
        
        # Recharger les données
        db.reload()
        
        # Vérifier le nouveau timestamp
        new_info = db.get_database_info()
        new_timestamp = new_info.get('timestamp_utc')
        new_count = new_info.get('diameter_count', 0)
        
        print(f"   Nouveau timestamp UTC: {new_timestamp}")
        print(f"   Nouveau nombre de diamètres: {new_count}")
        print(f"   Timestamps différents: {'✓' if timestamp != new_timestamp else '❌'}")
        print(f"   Nombre de diamètres inchangé: {'✓' if initial_count == new_count else '❌'}")
        
        # Test avec fallback
        print("\n4. Test reload avec fallback :")
        db_fallback = PriceDB("chemin/inexistant/vers/db.db")
        initial_fallback_count = db_fallback.get_database_info().get('diameter_count', 0)
        print(f"   Nombre initial (fallback): {initial_fallback_count}")
        
        db_fallback.reload()
        new_fallback_count = db_fallback.get_database_info().get('diameter_count', 0)
        print(f"   Nombre après reload (fallback): {new_fallback_count}")
        print(f"   Fallback reload fonctionne: {'✓' if initial_fallback_count == new_fallback_count else '❌'}")
        
        print("\n=== Tous les tests des nouvelles fonctionnalités ont réussi ! ===")
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test des nouvelles fonctionnalités: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_new_features()
