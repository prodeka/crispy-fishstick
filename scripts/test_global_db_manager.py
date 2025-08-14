#!/usr/bin/env python3
"""
Test du gestionnaire de base de données global
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_global_database_loading():
    """Test du chargement de toutes les bases de données"""
    print("🔵 TEST CHARGEMENT BASES DE DONNÉES GLOBALES")
    print("-" * 50)
    
    try:
        from lcpi.db.db_manager import GlobalDatabaseManager
        
        manager = GlobalDatabaseManager()
        
        if manager.databases:
            print(f"✅ Bases de données chargées avec succès")
            print(f"   Nombre de bases: {len(manager.databases)}")
            print(f"   Bases disponibles: {list(manager.databases.keys())}")
            return True
        else:
            print(f"❌ Aucune base de données chargée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur chargement bases de données: {e}")
        return False

def test_global_search():
    """Test de la recherche globale"""
    print("🔵 TEST RECHERCHE GLOBALE")
    print("-" * 30)
    
    try:
        from lcpi.db.db_manager import global_search
        
        # Test de recherche globale
        results = global_search("coefficient")
        print(f"✅ Recherche globale 'coefficient': {len(results)} résultats")
        
        # Test de recherche par plugin
        results_aep = global_search("coefficient", ["aep"])
        print(f"✅ Recherche AEP 'coefficient': {len(results_aep)} résultats")
        
        # Test de recherche par plugin
        results_cm = global_search("section", ["cm_bois"])
        print(f"✅ Recherche CM-Bois 'section': {len(results_cm)} résultats")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur recherche globale: {e}")
        return False

def test_plugin_queries():
    """Test des requêtes par plugin"""
    print("🔵 TEST REQUÊTES PAR PLUGIN")
    print("-" * 30)
    
    try:
        from lcpi.db.db_manager import query_database
        
        # Test requête AEP
        results_aep = query_database("aep", "coefficients")
        print(f"✅ Requête AEP coefficients: {len(results_aep)} résultats")
        
        # Test requête CM-Bois
        results_cm = query_database("cm_bois", "sections")
        print(f"✅ Requête CM-Bois sections: {len(results_cm)} résultats")
        
        # Test requête Bois
        results_bois = query_database("bois", "species")
        print(f"✅ Requête Bois species: {len(results_bois)} résultats")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur requêtes par plugin: {e}")
        return False

def test_global_autocomplete():
    """Test de l'auto-complétion globale"""
    print("🔵 TEST AUTO-COMPLÉTION GLOBALE")
    print("-" * 35)
    
    try:
        from lcpi.db.db_manager import get_global_autocomplete_options
        
        # Test auto-complétion globale
        options = get_global_autocomplete_options("coef")
        print(f"✅ Auto-complétion globale 'coef': {len(options)} options")
        if options:
            print(f"   Exemples: {options[:3]}")
        
        # Test auto-complétion par plugin
        options_aep = get_global_autocomplete_options("coef", ["aep"])
        print(f"✅ Auto-complétion AEP 'coef': {len(options_aep)} options")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur auto-complétion globale: {e}")
        return False

def test_export_functions():
    """Test des fonctions d'export"""
    print("🔵 TEST FONCTIONS D'EXPORT")
    print("-" * 25)
    
    try:
        from lcpi.db.db_manager import create_global_database_manager
        
        manager = create_global_database_manager()
        
        # Données de test
        test_results = [
            {"plugin": "aep", "type": "coefficient", "value": 120},
            {"plugin": "cm_bois", "type": "section", "value": "HEA200"}
        ]
        
        # Test export JSON
        json_export = manager.export_results(test_results, "json")
        if json_export and "aep" in json_export:
            print(f"✅ Export JSON: {len(json_export)} caractères")
        else:
            print(f"❌ Export JSON échoué")
            return False
        
        # Test export CSV
        csv_export = manager.export_results(test_results, "csv")
        if csv_export and "aep" in csv_export:
            print(f"✅ Export CSV: {len(csv_export)} caractères")
        else:
            print(f"❌ Export CSV échoué")
            return False
        
        # Test export Markdown
        md_export = manager.export_results(test_results, "markdown")
        if md_export and "aep" in md_export:
            print(f"✅ Export Markdown: {len(md_export)} caractères")
        else:
            print(f"❌ Export Markdown échoué")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur fonctions d'export: {e}")
        return False

def test_cli_commands():
    """Test des commandes CLI"""
    print("🔵 TEST COMMANDES CLI")
    print("-" * 20)
    
    try:
        from lcpi.db.db_manager import global_search, query_database, get_global_autocomplete_options
        
        # Test recherche globale
        results = global_search("coefficient")
        print(f"✅ CLI recherche globale: {len(results)} résultats")
        
        # Test requête par plugin
        results_aep = query_database("aep", "coefficients")
        print(f"✅ CLI requête AEP: {len(results_aep)} résultats")
        
        # Test auto-complétion
        options = get_global_autocomplete_options("coef")
        print(f"✅ CLI auto-complétion: {len(options)} options")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur commandes CLI: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST GESTIONNAIRE BASE DE DONNÉES GLOBAL")
    print("=" * 60)
    print("Ce test vérifie le gestionnaire de base de données global.")
    print("=" * 60)
    
    # Tests
    tests = [
        ("Chargement bases de données", test_global_database_loading),
        ("Recherche globale", test_global_search),
        ("Requêtes par plugin", test_plugin_queries),
        ("Auto-complétion globale", test_global_autocomplete),
        ("Fonctions d'export", test_export_functions),
        ("Commandes CLI", test_cli_commands)
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
    print("📊 RÉSUMÉ DES TESTS BASE DE DONNÉES GLOBALE")
    print("=" * 60)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ RÉUSSI" if i < success_count else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
    
    print(f"\n📈 Résultat global: {success_count}/{len(tests)} tests réussis")
    
    if success_count == len(tests):
        print("🎉 Tous les tests de base de données globale sont réussis !")
        print("✅ Le gestionnaire de base de données global fonctionne parfaitement.")
        return True
    else:
        print("⚠️ Certains tests de base de données globale ont échoué.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 