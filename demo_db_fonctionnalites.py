#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration des fonctionnalités de base de données métier
"""

import sys
import os
from pathlib import Path

# Configuration du path
sys.path.insert(0, 'src')

from lcpi.db_manager import db_manager, search_bois_cli, compare_materials_cli, export_data_cli, sql_query_cli

def demo_recherche():
    """Démonstration des fonctionnalités de recherche"""
    print("🔍 DÉMONSTRATION DES FONCTIONNALITÉS DE RECHERCHE")
    print("=" * 60)
    
    # Recherche par classe
    print("\n1. Recherche par classe de résistance:")
    search_bois_cli(classe="C24")
    
    # Recherche par propriété
    print("\n2. Recherche par propriété mécanique:")
    search_bois_cli(propriete="fm_k_MPa", min_val=20)
    
    # Recherche par module d'Young
    print("\n3. Recherche par module d'Young:")
    search_bois_cli(propriete="E0_mean_KN_mm2", min_val=10, max_val=15)

def demo_comparaison():
    """Démonstration des fonctionnalités de comparaison"""
    print("\n🔍 DÉMONSTRATION DES FONCTIONNALITÉS DE COMPARAISON")
    print("=" * 60)
    
    # Comparaison de matériaux
    print("\n1. Comparaison C24 vs C30:")
    compare_materials_cli(["C24", "C30"])
    
    print("\n2. Comparaison bois massif vs lamellé-collé:")
    compare_materials_cli(["C24", "GL24h"])

def demo_informations():
    """Démonstration des fonctionnalités d'information"""
    print("\n📋 DÉMONSTRATION DES FONCTIONNALITÉS D'INFORMATION")
    print("=" * 60)
    
    # Informations détaillées
    print("\n1. Informations détaillées C24:")
    info = db_manager.get_material_info("C24")
    if info:
        print(f"Type: {info['type']}")
        print(f"Classe: {info['classe']}")
        print("Propriétés principales:")
        for key, value in info['proprietes'].items():
            if key not in ["Classe", "Désignation", "Unité"]:
                print(f"  {key}: {value}")

def demo_export():
    """Démonstration des fonctionnalités d'export"""
    print("\n📤 DÉMONSTRATION DES FONCTIONNALITÉS D'EXPORT")
    print("=" * 60)
    
    # Export des données
    print("\n1. Export des données bois:")
    export_data_cli("bois_classes", "export_bois_demo.csv")
    
    # Vérifier que le fichier a été créé
    if Path("export_bois_demo.csv").exists():
        print("✅ Fichier export_bois_demo.csv créé avec succès")
    else:
        print("❌ Erreur lors de la création du fichier")

def demo_sql():
    """Démonstration des fonctionnalités SQL"""
    print("\n🗄️ DÉMONSTRATION DES FONCTIONNALITÉS SQL")
    print("=" * 60)
    
    # Conversion en SQLite
    print("\n1. Conversion en SQLite:")
    success = db_manager.create_sqlite_db("bois_test", "bois_test_sqlite")
    
    if success:
        print("✅ Base SQLite créée avec succès")
        
        # Requêtes SQL
        print("\n2. Requête SQL - Tous les bois avec fm_k > 20:")
        sql_query_cli("bois_test_sqlite", "SELECT Classe, fm_k_MPa FROM Valeurs_caractristiques_des_bois_massifs_rsineux WHERE CAST(fm_k_MPa AS FLOAT) > 20")
        
        print("\n3. Requête SQL - Comparaison des modules d'Young:")
        sql_query_cli("bois_test_sqlite", "SELECT Classe, E0_mean_KN_mm2 FROM Valeurs_caractristiques_des_bois_massifs_rsineux ORDER BY CAST(E0_mean_KN_mm2 AS FLOAT) DESC")
    else:
        print("❌ Erreur lors de la conversion SQLite")

def demo_repl_usage():
    """Démonstration de l'utilisation en REPL"""
    print("\n🐍 DÉMONSTRATION DE L'UTILISATION EN REPL")
    print("=" * 60)
    
    print("""
Pour utiliser les fonctionnalités en REPL:

1. Lancer le REPL:
   python -i repl_db_test.py

2. Exemples d'utilisation:
   
   # Recherche
   result = db_manager.search_bois_by_class('C24')
   result = db_manager.search_bois_by_property('fm_k_MPa', min_value=20)
   
   # Comparaison
   table = db_manager.compare_materials(['C24', 'C30', 'GL24h'])
   
   # Informations
   info = db_manager.get_material_info('C24')
   
   # Export
   db_manager.export_to_csv(data, 'mon_export.csv')
   
   # SQL
   db_manager.create_sqlite_db('bois_test', 'ma_base')
   results = db_manager.query_sql('ma_base', 'SELECT * FROM table')
""")

def main():
    """Fonction principale de démonstration"""
    print("🚀 DÉMONSTRATION COMPLÈTE DES FONCTIONNALITÉS DE BASE DE DONNÉES")
    print("=" * 80)
    
    try:
        demo_recherche()
        demo_comparaison()
        demo_informations()
        demo_export()
        demo_sql()
        demo_repl_usage()
        
        print("\n" + "=" * 80)
        print("🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS!")
        print("\n📝 RÉSUMÉ DES FONCTIONNALITÉS:")
        print("✅ Recherche par classe de résistance")
        print("✅ Recherche par propriété mécanique")
        print("✅ Comparaison de matériaux")
        print("✅ Informations détaillées")
        print("✅ Export en CSV")
        print("✅ Conversion SQLite et requêtes SQL")
        print("✅ Interface REPL interactive")
        
        print("\n💡 PROCHAINES ÉTAPES:")
        print("1. Utiliser: python -i repl_db_test.py")
        print("2. Tester les commandes CLI: lcpi db search --classe C24")
        print("3. Intégrer dans vos calculs métier")
        print("4. Ajouter de nouvelles bases de données")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 