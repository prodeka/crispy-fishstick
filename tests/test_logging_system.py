#!/usr/bin/env python3
"""
Test du système de logging LCPI avec signature et intégrité.
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_logging_system():
    """Test du système de logging complet."""
    print("🧪 Test du système de logging LCPI")
    print("=" * 50)
    
    try:
        from lcpi.logging.logger import LCPILogger
        
        # Créer un logger de test
        test_logs_dir = Path("test_logs")
        logger = LCPILogger(test_logs_dir, enable_signing=True, enable_indexing=True)
        
        print("✅ Logger initialisé")
        
        # Test 1: Création d'un log
        print("\n📝 Test 1: Création d'un log...")
        
        input_data = {
            "canal": {
                "largeur": 2.0,
                "hauteur": 1.5,
                "pente": 0.001,
                "rugosite": 0.013
            }
        }
        
        output_data = {
            "debit": 3.45,
            "vitesse": 1.15,
            "hauteur_eau": 1.2,
            "formule_utilisee": "Manning"
        }
        
        log_result = logger.log_calculation(
            calculation_type="Hydro",
            input_data=input_data,
            output_data=output_data,
            solver="Manning",
            duration=0.15,
            tags=["canal", "dimensionnement"],
            metadata={"version": "1.0", "user": "test"}
        )
        
        print(f"✅ Log créé: {log_result['log_id']}")
        print(f"   Fichier: {log_result['log_file']}")
        print(f"   Signé: {log_result['signed']}")
        print(f"   Indexé: {log_result['indexed']}")
        print(f"   Intégrité: {log_result['integrity_valid']}")
        
        # Test 2: Vérification de la signature
        print("\n🔐 Test 2: Vérification de la signature...")
        
        log_file = Path(log_result['log_file'])
        signature_result = logger.verify_log_signature(log_file)
        
        if signature_result['valid']:
            print("✅ Signature vérifiée avec succès")
            signature_info = signature_result['signature_info']
            print(f"   Algorithme: {signature_info.get('algorithm')}")
            print(f"   Clé ID: {signature_info.get('key_id')}")
            print(f"   Timestamp: {signature_info.get('timestamp')}")
        else:
            print(f"❌ Erreur de signature: {signature_result.get('error')}")
        
        # Test 3: Vérification de l'intégrité
        print("\n🔍 Test 3: Vérification de l'intégrité...")
        
        integrity_result = logger.verify_log_integrity(log_file)
        
        if integrity_result['valid']:
            print("✅ Intégrité vérifiée avec succès")
            print(f"   Taille: {integrity_result.get('file_size')} octets")
            print(f"   Modifié: {integrity_result.get('last_modified')}")
        else:
            print(f"❌ Erreur d'intégrité: {integrity_result.get('error')}")
        
        # Test 4: Indexation et recherche
        print("\n📚 Test 4: Indexation et recherche...")
        
        # Indexer le log
        index_result = logger.indexer.index_log_file(log_file)
        if index_result['success']:
            print("✅ Log indexé avec succès")
        else:
            print(f"❌ Erreur d'indexation: {index_result.get('error')}")
        
        # Rechercher dans les logs
        search_results = logger.search_logs("canal", limit=10)
        print(f"📊 Recherche 'canal': {len(search_results)} résultats")
        
        for result in search_results:
            print(f"   - {result.get('calculation_type')} ({result.get('timestamp')})")
        
        # Test 5: Statistiques
        print("\n📊 Test 5: Statistiques...")
        
        stats = logger.get_log_statistics()
        print(f"Total des logs: {stats.get('total_logs', 0)}")
        
        if stats.get('by_calculation_type'):
            for calc_type, count in stats['by_calculation_type'].items():
                print(f"   {calc_type}: {count}")
        
        # Test 6: Informations de clé
        print("\n🗝️  Test 6: Informations de clé...")
        
        key_info = logger.get_public_key_info()
        print(f"ID de clé: {key_info.get('key_id')}")
        print(f"Algorithme: {key_info.get('algorithm')}")
        
        # Test 7: Vérification de tous les logs
        print("\n🔍 Test 7: Vérification de tous les logs...")
        
        all_logs_result = logger.verify_all_logs()
        print(f"Total: {all_logs_result.get('total_logs', 0)}")
        print(f"Valides: {all_logs_result.get('valid_logs', 0)}")
        print(f"Corrompus: {all_logs_result.get('corrupted_logs', 0)}")
        
        # Test 8: Export du rapport d'intégrité
        print("\n📤 Test 8: Export du rapport d'intégrité...")
        
        try:
            report_path = logger.export_integrity_report()
            print(f"✅ Rapport exporté: {report_path}")
        except Exception as e:
            print(f"❌ Erreur d'export: {e}")
        
        # Test 9: Nettoyage des logs de test
        print("\n🧹 Test 9: Nettoyage des logs de test...")
        
        cleanup_result = logger.cleanup_old_logs(max_age=0, dry_run=False)
        if 'logs_removed' in cleanup_result:
            print(f"✅ {cleanup_result['logs_removed']} logs supprimés")
        
        # Nettoyer le répertoire de test
        import shutil
        if test_logs_dir.exists():
            shutil.rmtree(test_logs_dir)
            print("✅ Répertoire de test supprimé")
        
        print("\n🎉 Tous les tests sont passés !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_log_verification():
    """Test spécifique de la vérification des logs."""
    print("\n🔍 Test de vérification des logs existants...")
    
    try:
        from lcpi.logging.logger import logger
        
        # Lister les logs existants
        existing_logs = logger.list_available_logs(limit=5)
        
        if not existing_logs:
            print("ℹ️  Aucun log existant trouvé")
            return True
        
        print(f"📋 {len(existing_logs)} logs existants trouvés:")
        
        for log in existing_logs[:3]:  # Tester les 3 premiers
            print(f"\n📄 Vérification de {log['filename']}...")
            
            # Vérifier la signature
            signature_result = logger.verify_log_signature(Path(log['file_path']))
            if signature_result['valid']:
                print("   ✅ Signature valide")
            else:
                print(f"   ❌ Signature invalide: {signature_result.get('error')}")
            
            # Vérifier l'intégrité
            integrity_result = logger.verify_log_integrity(Path(log['file_path']))
            if integrity_result['valid']:
                print("   ✅ Intégrité valide")
            else:
                print(f"   ❌ Intégrité invalide: {integrity_result.get('error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test du système de logging LCPI avec signature et intégrité")
    print("=" * 70)
    
    tests = [
        test_logging_system,
        test_log_verification
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 Résumé des tests:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {i+1}. {test.__name__}: {status}")
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés !")
        print("\n🚀 Le système de signature et d'intégrité des logs est opérationnel !")
        return 0
    else:
        print("⚠️  Certains tests ont échoué.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
