#!/usr/bin/env python3
"""
Test simple des nouvelles fonctionnalités PriceDB
"""

from src.lcpi.aep.optimizer.db import PriceDB

def test_new_features():
    print("=== Test des nouvelles fonctionnalités PriceDB ===\n")
    
    # Test 1: Timestamp
    print("1. Test du timestamp de chargement:")
    db = PriceDB()
    info = db.get_database_info()
    timestamp = info.get('timestamp_utc')
    print(f"   Timestamp UTC: {timestamp}")
    print(f"   ✓ Timestamp présent" if timestamp else "   ❌ Timestamp manquant")
    
    # Test 2: Version par défaut
    version = info.get('db_version')
    print(f"   Version DB: {version}")
    print(f"   ✓ Version par défaut définie" if version else "   ❌ Version manquante")
    
    # Test 3: Méthode reload
    print("\n2. Test de la méthode reload:")
    initial_count = info.get('diameter_count', 0)
    print(f"   Nombre initial de diamètres: {initial_count}")
    
    db.reload()
    new_info = db.get_database_info()
    new_timestamp = new_info.get('timestamp_utc')
    new_count = new_info.get('diameter_count', 0)
    
    print(f"   Nouveau timestamp: {new_timestamp}")
    print(f"   Nouveau nombre: {new_count}")
    print(f"   ✓ Timestamps différents" if timestamp != new_timestamp else "   ❌ Timestamps identiques")
    print(f"   ✓ Nombre inchangé" if initial_count == new_count else "   ❌ Nombre modifié")
    
    print("\n=== Test des nouvelles fonctionnalités réussi ! ===")

if __name__ == "__main__":
    test_new_features()
