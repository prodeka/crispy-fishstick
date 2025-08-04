#!/usr/bin/env python3
"""
Test du gestionnaire de base de données AEP
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_database_loading():
    """Test du chargement de la base de données"""
    print("🔵 TEST CHARGEMENT BASE DE DONNÉES")
    print("-" * 40)
    
    try:
        from lcpi.db.aep_database_manager import AEPDatabaseManager
        
        manager = AEPDatabaseManager()
        
        if manager.data:
            print(f"✅ Base de données chargée avec succès")
            print(f"   Nombre d'entrées: {len(manager.data)}")
            return True
        else:
            print(f"❌ Base de données vide")
            return False
            
    except Exception as e:
        print(f"❌ Erreur chargement base de données: {e}")
        return False

def test_query_functions():
    """Test des fonctions de requête"""
    print("🔵 TEST FONCTIONS DE REQUÊTE")
    print("-" * 40)
    
    try:
        from lcpi.db.aep_database_manager import AEPDatabaseManager
        
        manager = AEPDatabaseManager()
        
        # Test des coefficients
        coefficients = manager.get_coefficients()
        print(f"✅ Coefficients: {len(coefficients)} résultats")
        
        # Test des matériaux
        materials = manager.get_materials()
        print(f"✅ Matériaux: {len(materials)} résultats")
        
        # Test des formules
        formulas = manager.get_formulas()
        print(f"✅ Formules: {len(formulas)} résultats")
        
        # Test des constantes
        constants = manager.get_constants()
        print(f"✅ Constantes: {len(constants)} résultats")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur fonctions de requête: {e}")
        return False

def test_search_function():
    """Test de la fonction de recherche"""
    print("🔵 TEST FONCTION DE RECHERCHE")
    print("-" * 40)
    
    try:
        from lcpi.db.aep_database_manager import AEPDatabaseManager
        
        manager = AEPDatabaseManager()
        
        # Test de recherche
        search_results = manager.search_text("coefficient")
        print(f"✅ Recherche 'coefficient': {len(search_results)} résultats")
        
        search_results = manager.search_text("pvc")
        print(f"✅ Recherche 'pvc': {len(search_results)} résultats")
        
        search_results = manager.search_text("formule")
        print(f"✅ Recherche 'formule': {len(search_results)} résultats")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur fonction de recherche: {e}")
        return False

def test_autocomplete():
    """Test de l'auto-complétion"""
    print("🔵 TEST AUTO-COMPLÉTION")
    print("-" * 40)
    
    try:
        from lcpi.db.aep_database_manager import AEPDatabaseManager
        
        manager = AEPDatabaseManager()
        
        # Test d'auto-complétion
        options = manager.get_autocomplete_options("coef")
        print(f"✅ Auto-complétion 'coef': {len(options)} options")
        if options:
            print(f"   Exemples: {options[:3]}")
        
        options = manager.get_autocomplete_options("pvc")
        print(f"✅ Auto-complétion 'pvc': {len(options)} options")
        if options:
            print(f"   Exemples: {options[:3]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur auto-complétion: {e}")
        return False

def test_export_functions():
    """Test des fonctions d'export"""
    print("🔵 TEST FONCTIONS D'EXPORT")
    print("-" * 40)
    
    try:
        from lcpi.db.aep_database_manager import AEPDatabaseManager
        
        manager = AEPDatabaseManager()
        
        # Données de test
        test_results = [
            {"name": "PVC", "coefficient": 120, "type": "rugosite"},
            {"name": "Fonte", "coefficient": 90, "type": "rugosite"}
        ]
        
        # Test export JSON
        json_export = manager.export_results(test_results, "json")
        if json_export and "PVC" in json_export:
            print(f"✅ Export JSON: {len(json_export)} caractères")
        else:
            print(f"❌ Export JSON échoué")
            return False
        
        # Test export CSV
        csv_export = manager.export_results(test_results, "csv")
        if csv_export and "PVC" in csv_export:
            print(f"✅ Export CSV: {len(csv_export)} caractères")
        else:
            print(f"❌ Export CSV échoué")
            return False
        
        # Test export Markdown
        md_export = manager.export_results(test_results, "markdown")
        if md_export and "PVC" in md_export:
            print(f"✅ Export Markdown: {len(md_export)} caractères")
        else:
            print(f"❌ Export Markdown échoué")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur fonctions d'export: {e}")
        return False

def test_interface_functions():
    """Test des fonctions d'interface"""
    print("🔵 TEST FONCTIONS D'INTERFACE")
    print("-" * 40)
    
    try:
        from lcpi.db.aep_database_manager import query_aep_database, get_aep_autocomplete_options
        
        # Test requête coefficients
        coefficients = query_aep_database("coefficients")
        print(f"✅ Interface coefficients: {len(coefficients)} résultats")
        
        # Test requête matériaux
        materials = query_aep_database("materials")
        print(f"✅ Interface matériaux: {len(materials)} résultats")
        
        # Test auto-complétion
        options = get_aep_autocomplete_options("coef")
        print(f"✅ Interface auto-complétion: {len(options)} options")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur fonctions d'interface: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST GESTIONNAIRE BASE DE DONNÉES AEP")
    print("=" * 60)
    print("Ce test vérifie le gestionnaire de base de données AEP.")
    print("=" * 60)
    
    # Tests
    tests = [
        ("Chargement base de données", test_database_loading),
        ("Fonctions de requête", test_query_functions),
        ("Fonction de recherche", test_search_function),
        ("Auto-complétion", test_autocomplete),
        ("Fonctions d'export", test_export_functions),
        ("Fonctions d'interface", test_interface_functions)
    ]
    
    success_count = 0
    for test_name, test_func in tests:
        print(f"\n📊 Test: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                success_count += 1
                print(f"✅ {test_name}: RÉUSSI")
            else:
                print(f"❌ {test_name}: ÉCHEC")
        except Exception as e:
            print(f"❌ {test_name}: ERREUR - {e}")
    
    # Résumé
    print(f"\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS BASE DE DONNÉES")
    print("=" * 60)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ RÉUSSI" if i < success_count else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
    
    print(f"\n📈 Résultat global: {success_count}/{len(tests)} tests réussis")
    
    if success_count == len(tests):
        print("🎉 Tous les tests de base de données sont réussis !")
        print("✅ Le gestionnaire de base de données AEP fonctionne parfaitement.")
        return True
    else:
        print("⚠️ Certains tests de base de données ont échoué.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 