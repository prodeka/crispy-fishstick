#!/usr/bin/env python3
"""
Test spécifique pour la classe PriceDB nouvellement implémentée.
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Ajouter le répertoire src au path Python
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_price_db_creation():
    """Teste la création de l'instance PriceDB"""
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        print("🔍 Test de création de PriceDB")
        
        # Test avec le chemin par défaut
        db = PriceDB()
        print(f"✅ PriceDB créé avec succès")
        print(f"   Chemin: {db.db_path}")
        print(f"   Existe: {db.db_path.exists()}")
        print(f"   Type: {'YAML' if db._is_yaml else 'SQLite'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False

def test_database_info():
    """Teste la méthode get_database_info"""
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        print("🔍 Test de get_database_info")
        
        db = PriceDB()
        info = db.get_database_info()
        
        print(f"✅ Informations de base récupérées:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        # Vérifications spécifiques
        assert "path" in info, "Clé 'path' manquante"
        assert "exists" in info, "Clé 'exists' manquante"
        assert "type" in info, "Clé 'type' manquante"
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des infos: {e}")
        return False

def test_candidate_diameters():
    """Teste la récupération des diamètres candidats"""
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        print("🔍 Test de get_candidate_diameters")
        
        db = PriceDB()
        diameters = db.get_candidate_diameters()
        
        print(f"✅ Diamètres candidats récupérés: {len(diameters)}")
        
        if diameters:
            print(f"   Premier diamètre: DN {diameters[0]['dn_mm']} - {diameters[0]['total_fcfa_per_m']} FCFA/m")
            print(f"   Dernier diamètre: DN {diameters[-1]['dn_mm']} - {diameters[-1]['total_fcfa_per_m']} FCFA/m")
        
        # Vérifications spécifiques
        assert len(diameters) > 0, "Aucun diamètre récupéré"
        assert all("dn_mm" in d for d in diameters), "Champ 'dn_mm' manquant"
        assert all("total_fcfa_per_m" in d for d in diameters), "Champ 'total_fcfa_per_m' manquant"
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des diamètres: {e}")
        return False

def test_material_filtering():
    """Teste le filtrage par matériau"""
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        print("🔍 Test de filtrage par matériau")
        
        db = PriceDB()
        
        # Test avec PVC-U
        pvc_diameters = db.get_candidate_diameters("PVC-U")
        print(f"✅ Diamètres PVC-U: {len(pvc_diameters)}")
        
        if pvc_diameters:
            print(f"   Premier PVC-U: DN {pvc_diameters[0]['dn_mm']} - {pvc_diameters[0]['material']}")
        
        # Test avec PEHD
        pehd_diameters = db.get_candidate_diameters("PEHD")
        print(f"   Diamètres PEHD: {len(pehd_diameters)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du filtrage par matériau: {e}")
        return False

def test_diameter_price_lookup():
    """Teste la recherche de prix par diamètre"""
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        print("🔍 Test de recherche de prix par diamètre")
        
        db = PriceDB()
        
        # Test avec un diamètre existant
        price_110 = db.get_diameter_price(110)
        if price_110 is not None:
            print(f"✅ Prix DN 110mm: {price_110} FCFA/m")
        else:
            print(f"⚠️  Prix DN 110mm: non trouvé")
        
        # Test avec un diamètre inexistant
        price_999 = db.get_diameter_price(999)
        if price_999 is None:
            print(f"✅ Prix DN 999mm: non trouvé (comportement attendu)")
        else:
            print(f"⚠️  Prix DN 999mm: {price_999} FCFA/m (inattendu)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche de prix: {e}")
        return False

def test_closest_diameter():
    """Teste la recherche du diamètre le plus proche"""
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        print("🔍 Test de recherche du diamètre le plus proche")
        
        db = PriceDB()
        
        # Test avec un diamètre proche d'un existant
        closest_115 = db.get_closest_diameter(115)
        if closest_115:
            print(f"✅ Diamètre le plus proche de 115mm: DN {closest_115['dn_mm']}mm")
            print(f"   Différence: {abs(closest_115['dn_mm'] - 115)}mm")
        else:
            print(f"⚠️  Aucun diamètre trouvé pour 115mm")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche du diamètre le plus proche: {e}")
        return False

def test_fallback_scenario():
    """Teste le scénario de fallback avec une base inexistante"""
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        print("🔍 Test du scénario de fallback")
        
        # Créer un chemin temporaire inexistant
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_db_path = Path(temp_dir) / "fake_aep_prices.db"
            
            # Créer PriceDB avec un chemin inexistant
            db = PriceDB(fake_db_path)
            
            # Vérifier que le fallback est utilisé
            info = db.get_database_info()
            assert info["fallback_used"] == True, "Fallback non utilisé"
            
            # Vérifier que les diamètres de fallback sont retournés
            diameters = db.get_candidate_diameters()
            assert len(diameters) > 0, "Aucun diamètre de fallback retourné"
            
            print(f"✅ Fallback fonctionne: {len(diameters)} diamètres de fallback")
            
            # Vérifier la structure canonique
            if diameters:
                first_diameter = diameters[0]
                required_keys = ["dn_mm", "supply_fcfa_per_m", "pose_fcfa_per_m", "total_fcfa_per_m", "material", "source_method"]
                missing_keys = [key for key in required_keys if key not in first_diameter]
                if missing_keys:
                    print(f"⚠️  Clés manquantes dans la structure canonique: {missing_keys}")
                else:
                    print(f"✅ Structure canonique respectée")
                    print(f"   Exemple: DN {first_diameter['dn_mm']}mm - {first_diameter['total_fcfa_per_m']} FCFA/m ({first_diameter['material']})")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de fallback: {e}")
        return False

def test_realistic_pricing():
    """Teste le modèle de tarification réaliste"""
    try:
        from lcpi.aep.optimizer.db import PriceDB, _get_realistic_pipe_price
        
        print("🔍 Test du modèle de tarification réaliste")
        
        # Test de la fonction de calcul
        test_cases = [
            (50, "PVC"),
            (110, "PEHD"),
            (200, "Fonte"),
            (315, "PEHD")
        ]
        
        print("💰 Test des calculs de prix:")
        for dn_mm, material in test_cases:
            price = _get_realistic_pipe_price(dn_mm, material)
            print(f"   DN {dn_mm}mm {material}: {price} FCFA/m")
        
        # Test avec fallback pour vérifier les prix calculés
        db = PriceDB("fake_path")  # Force le fallback
        fallback_diameters = db.get_candidate_diameters()
        
        if fallback_diameters:
            # Vérifier que les prix sont réalistes (pas 0 ou négatifs)
            realistic_prices = [d for d in fallback_diameters if d['total_fcfa_per_m'] > 0]
            print(f"✅ {len(realistic_prices)}/{len(fallback_diameters)} diamètres avec prix réalistes")
            
            # Afficher quelques exemples
            examples = fallback_diameters[:3]
            for example in examples:
                print(f"   DN {example['dn_mm']}mm {example['material']}: {example['total_fcfa_per_m']} FCFA/m")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de tarification réaliste: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test de la classe PriceDB (Version améliorée)")
    print("=" * 60)
    
    tests = [
        ("Création de PriceDB", test_price_db_creation),
        ("Informations de base", test_database_info),
        ("Diamètres candidats", test_candidate_diameters),
        ("Filtrage par matériau", test_material_filtering),
        ("Recherche de prix", test_diameter_price_lookup),
        ("Diamètre le plus proche", test_closest_diameter),
        ("Scénario de fallback", test_fallback_scenario),
        ("Tarification réaliste", test_realistic_pricing),
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
