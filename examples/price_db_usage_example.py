#!/usr/bin/env python3
"""
Exemple d'utilisation pratique de la classe PriceDB.

Ce script démontre comment utiliser la classe PriceDB dans différents scénarios :
- Initialisation avec différents chemins
- Récupération des informations de base
- Recherche de diamètres et prix
- Gestion des erreurs et fallback
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path Python
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def example_basic_usage():
    """Exemple d'utilisation basique de PriceDB"""
    print("🔍 Exemple d'utilisation basique")
    print("=" * 50)
    
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        # Création d'une instance avec le chemin par défaut
        db = PriceDB()
        
        # Informations sur la base
        info = db.get_database_info()
        print(f"✅ Base de données initialisée:")
        print(f"   Chemin: {info['path']}")
        print(f"   Type: {info['type']}")
        print(f"   Diamètres disponibles: {info['diameter_count']}")
        print(f"   Accessoires disponibles: {info['accessory_count']}")
        print(f"   Checksum: {info['checksum']}")
        
        # Récupération de tous les diamètres
        all_diameters = db.get_candidate_diameters()
        print(f"\n📏 Diamètres disponibles: {len(all_diameters)}")
        
        # Affichage des premiers diamètres
        print("   Premiers diamètres:")
        for i, diameter in enumerate(all_diameters[:5]):
            print(f"     {i+1}. DN {diameter['dn_mm']}mm - {diameter['total_fcfa_per_m']} FCFA/m ({diameter['material']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def example_material_filtering():
    """Exemple de filtrage par matériau"""
    print("\n🔍 Exemple de filtrage par matériau")
    print("=" * 50)
    
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        db = PriceDB()
        
        # Matériaux disponibles
        materials = ["PVC-U", "PEHD", "Fonte_dutile"]
        
        for material in materials:
            diameters = db.get_candidate_diameters(material)
            print(f"📏 {material}: {len(diameters)} diamètres")
            
            if diameters:
                # Afficher la gamme de diamètres
                min_dn = min(d['dn_mm'] for d in diameters)
                max_dn = max(d['dn_mm'] for d in diameters)
                avg_cost = sum(d['total_fcfa_per_m'] for d in diameters) / len(diameters)
                
                print(f"   Gamme: DN {min_dn}mm - DN {max_dn}mm")
                print(f"   Prix moyen: {avg_cost:.0f} FCFA/m")
                
                # Afficher quelques exemples
                examples = [d for d in diameters if d['dn_mm'] in [50, 110, 200]]
                for example in examples:
                    print(f"     DN {example['dn_mm']}mm: {example['total_fcfa_per_m']} FCFA/m")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def example_price_lookup():
    """Exemple de recherche de prix"""
    print("\n🔍 Exemple de recherche de prix")
    print("=" * 50)
    
    try:
        from lcpi.aep.optimizer.db import PriceDB
        
        db = PriceDB()
        
        # Diamètres à rechercher
        target_diameters = [50, 110, 200, 315, 400]
        
        print("💰 Recherche de prix par diamètre:")
        for target_dn in target_diameters:
            price = db.get_diameter_price(target_dn)
            if price is not None:
                print(f"   DN {target_dn}mm: {price} FCFA/m")
            else:
                print(f"   DN {target_dn}mm: Prix non trouvé")
        
        # Recherche du diamètre le plus proche
        print("\n🎯 Recherche du diamètre le plus proche:")
        test_values = [115, 225, 350]
        
        for test_value in test_values:
            closest = db.get_closest_diameter(test_value)
            if closest:
                diff = abs(closest['dn_mm'] - test_value)
                print(f"   {test_value}mm → DN {closest['dn_mm']}mm (différence: {diff}mm)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def example_fallback_scenario():
    """Exemple de scénario de fallback"""
    print("\n🔍 Exemple de scénario de fallback")
    print("=" * 50)
    
    try:
        from lcpi.aep.optimizer.db import PriceDB
        import tempfile
        
        # Créer un chemin temporaire inexistant
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_db_path = Path(temp_dir) / "nonexistent_aep_prices.db"
            
            print(f"📁 Test avec base inexistante: {fake_db_path}")
            
            # Créer PriceDB avec un chemin inexistant
            db = PriceDB(fake_db_path)
            
            # Vérifier que le fallback est utilisé
            info = db.get_database_info()
            print(f"   Fallback utilisé: {info['fallback_used']}")
            print(f"   Base existe: {info['exists']}")
            
            # Récupérer les diamètres de fallback
            fallback_diameters = db.get_candidate_diameters()
            print(f"   Diamètres de fallback: {len(fallback_diameters)}")
            
            # Afficher les diamètres de fallback
            print("   Diamètres disponibles:")
            for diameter in fallback_diameters:
                print(f"     DN {diameter['dn_mm']}mm - {diameter['total_fcfa_per_m']} FCFA/m ({diameter['material']})")
            
            # Test de recherche de prix avec fallback
            test_price = db.get_diameter_price(110)
            if test_price:
                print(f"   Prix DN 110mm (fallback): {test_price} FCFA/m")
            
            # Test de diamètre le plus proche avec fallback
            closest = db.get_closest_diameter(115)
            if closest:
                diff = abs(closest['dn_mm'] - 115)
                print(f"   Diamètre le plus proche de 115mm: DN {closest['dn_mm']}mm (différence: {diff}mm)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def example_error_handling():
    """Exemple de gestion des erreurs"""
    print("\n🔍 Exemple de gestion des erreurs")
    print("=" * 50)
    
    try:
        from lcpi.aep.optimizer.db import PriceDB
        import tempfile
        
        # Test avec différents types de chemins
        test_paths = [
            None,  # Chemin par défaut
            "/invalid/path/aep_prices.db",  # Chemin invalide
            "src/lcpi/db/aep_prices.db",  # Chemin relatif valide
        ]
        
        for i, test_path in enumerate(test_paths, 1):
            print(f"\n📁 Test {i}: {test_path or 'Chemin par défaut'}")
            
            try:
                db = PriceDB(test_path)
                info = db.get_database_info()
                
                print(f"   ✅ Succès:")
                print(f"      Existe: {info['exists']}")
                print(f"      Fallback: {info['fallback_used']}")
                print(f"      Diamètres: {info.get('diameter_count', 'N/A')}")
                
            except Exception as e:
                print(f"   ❌ Erreur: {type(e).__name__}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def example_performance_analysis():
    """Exemple d'analyse de performance"""
    print("\n🔍 Exemple d'analyse de performance")
    print("=" * 50)
    
    try:
        from lcpi.aep.optimizer.db import PriceDB
        import time
        
        db = PriceDB()
        
        # Test de performance pour la récupération des diamètres
        print("⏱️  Test de performance:")
        
        # Test 1: Récupération de tous les diamètres
        start_time = time.time()
        all_diameters = db.get_candidate_diameters()
        end_time = time.time()
        
        print(f"   Récupération de {len(all_diameters)} diamètres: {(end_time - start_time)*1000:.2f}ms")
        
        # Test 2: Recherche de prix multiples
        test_diameters = [50, 110, 200, 315, 400, 500, 630, 800]
        
        start_time = time.time()
        prices = []
        for dn in test_diameters:
            price = db.get_diameter_price(dn)
            prices.append(price)
        end_time = time.time()
        
        print(f"   Recherche de {len(test_diameters)} prix: {(end_time - start_time)*1000:.2f}ms")
        
        # Test 3: Recherche de diamètres proches
        start_time = time.time()
        closest_diameters = []
        for target in range(100, 1000, 50):
            closest = db.get_closest_diameter(target)
            if closest:
                closest_diameters.append(closest)
        end_time = time.time()
        
        print(f"   Recherche de {len(closest_diameters)} diamètres proches: {(end_time - start_time)*1000:.2f}ms")
        
        # Statistiques
        valid_prices = [p for p in prices if p is not None]
        if valid_prices:
            avg_price = sum(valid_prices) / len(valid_prices)
            print(f"\n📊 Statistiques:")
            print(f"   Prix trouvés: {len(valid_prices)}/{len(test_diameters)}")
            print(f"   Prix moyen: {avg_price:.0f} FCFA/m")
            print(f"   Prix min: {min(valid_prices):.0f} FCFA/m")
            print(f"   Prix max: {max(valid_prices):.0f} FCFA/m")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Exemples d'utilisation de PriceDB")
    print("=" * 60)
    
    examples = [
        ("Utilisation basique", example_basic_usage),
        ("Filtrage par matériau", example_material_filtering),
        ("Recherche de prix", example_price_lookup),
        ("Scénario de fallback", example_fallback_scenario),
        ("Gestion des erreurs", example_error_handling),
        ("Analyse de performance", example_performance_analysis),
    ]
    
    results = []
    for example_name, example_func in examples:
        print(f"\n{'='*60}")
        try:
            result = example_func()
            results.append((example_name, result))
        except Exception as e:
            print(f"❌ Erreur inattendue dans {example_name}: {e}")
            results.append((example_name, False))
    
    # Résumé
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ DES EXEMPLES")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for example_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{status} {example_name}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} exemples réussis")
    
    if passed == total:
        print("🎉 Tous les exemples sont passés avec succès!")
    else:
        print("⚠️  Certains exemples ont échoué. Vérifiez les détails ci-dessus.")

if __name__ == "__main__":
    main()
