#!/usr/bin/env python3
"""
Test d'intégration pour la base de données aep_prices.db
et vérification des mécanismes de fallback.
"""

import sys
import sqlite3
from pathlib import Path

# Ajouter le répertoire src au path Python
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_database_exists():
    """Teste l'existence de la base de données aep_prices.db"""
    db_path = Path("src/lcpi/db/aep_prices.db")
    print(f"🔍 Vérification de l'existence de {db_path}")
    
    if db_path.exists():
        print(f"✅ Base de données trouvée: {db_path}")
        print(f"   Taille: {db_path.stat().st_size / 1024:.1f} KB")
        return True
    else:
        print(f"❌ Base de données introuvable: {db_path}")
        return False

def test_database_structure():
    """Teste la structure de la base de données"""
    db_path = Path("src/lcpi/db/aep_prices.db")
    
    if not db_path.exists():
        print("❌ Impossible de tester la structure - base introuvable")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tables trouvées: {', '.join(tables)}")
        
        # Vérifier le contenu des tables
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count} enregistrements")
        
        # Vérifier la structure de la table diameters
        if 'diameters' in tables:
            cursor.execute("PRAGMA table_info(diameters)")
            columns = cursor.fetchall()
            print(f"   Structure de 'diameters':")
            for col in columns:
                print(f"     - {col[1]} ({col[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse de la structure: {e}")
        return False

def test_dao_integration():
    """Teste l'intégration avec le DAO"""
    try:
        from lcpi.aep.optimizer.db_dao import AEPPricesDAO
        
        print("🔍 Test d'intégration avec AEPPricesDAO")
        
        # Test avec le chemin par défaut
        dao = AEPPricesDAO()
        print(f"✅ DAO initialisé avec succès")
        print(f"   Chemin de la base: {dao.db_path}")
        
        # Test de récupération des diamètres
        diameters = dao.get_available_diameters()
        print(f"   Diamètres disponibles: {len(diameters)}")
        
        if diameters:
            print(f"   Premier diamètre: DN {diameters[0]['d_mm']} - {diameters[0]['cost_per_m']} FCFA/m")
        
        # Test de récupération des matériaux
        materials = dao.get_available_materials()
        print(f"   Matériaux disponibles: {', '.join(materials)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'intégration DAO: {e}")
        return False

def test_fallback_scenarios():
    """Teste les scénarios de fallback"""
    print("🔍 Test des scénarios de fallback")
    
    # Test avec un chemin inexistant
    try:
        from lcpi.aep.optimizer.db_dao import AEPPricesDAO
        
        fake_path = Path("fake_path/aep_prices.db")
        dao = AEPPricesDAO(fake_path)
        print("❌ Le DAO aurait dû lever une exception pour un chemin inexistant")
        return False
        
    except FileNotFoundError:
        print("✅ Exception FileNotFoundError correctement levée pour un chemin inexistant")
    
    # Test avec le fallback DiameterDAO
    try:
        from lcpi.aep.optimizer.db import get_candidate_diameters
        
        fallback_diameters = get_candidate_diameters()
        print(f"✅ Fallback DiameterDAO fonctionne: {len(fallback_diameters)} diamètres")
        
        if fallback_diameters:
            print(f"   Premier diamètre de fallback: DN {fallback_diameters[0]['d_mm']} - {fallback_diameters[0]['cost_per_m']} FCFA/m")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du fallback: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test d'intégration de la base de données aep_prices.db")
    print("=" * 60)
    
    tests = [
        ("Existence de la base", test_database_exists),
        ("Structure de la base", test_database_structure),
        ("Intégration DAO", test_dao_integration),
        ("Scénarios de fallback", test_fallback_scenarios),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            results.append((test_name, False))
    
    # Résumé des résultats
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés avec succès!")
        return 0
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les détails ci-dessus.")
        return 1

if __name__ == "__main__":
    exit(main())
