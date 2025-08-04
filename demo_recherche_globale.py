#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration de la recherche globale dans toutes les bases de données
"""

import sys
import os
from pathlib import Path

# Configuration du path
sys.path.insert(0, 'src')

from lcpi.db_global_search import global_search

def demo_recherche_simple():
    """Démonstration des recherches simples"""
    print("🔍 DÉMONSTRATION DES RECHERCHES SIMPLES")
    print("=" * 60)
    
    # Recherche simple
    print("\n1. Recherche 'C24':")
    global_search.search_and_display("C24")
    
    # Recherche par propriété
    print("\n2. Recherche 'fm_k':")
    global_search.search_and_display("fm_k")
    
    # Recherche par valeur
    print("\n3. Recherche '24.0':")
    global_search.search_and_display("24.0")

def demo_recherche_multiple():
    """Démonstration des recherches multiples"""
    print("\n🔍 DÉMONSTRATION DES RECHERCHES MULTIPLES")
    print("=" * 60)
    
    # Recherche AND
    print("\n1. Recherche AND 'C24 fm_k' (tous les mots):")
    global_search.search_and_display(["C24", "fm_k"], "AND")
    
    # Recherche OR
    print("\n2. Recherche OR 'C24 GL24h' (au moins un mot):")
    global_search.search_and_display(["C24", "GL24h"], "OR")
    
    # Recherche avec valeurs
    print("\n3. Recherche AND '24.0 MPa' (tous les mots):")
    global_search.search_and_display(["24.0", "MPa"], "AND")

def demo_recherche_avancee():
    """Démonstration des recherches avancées"""
    print("\n🔍 DÉMONSTRATION DES RECHERCHES AVANCÉES")
    print("=" * 60)
    
    # Recherche par type de matériau
    print("\n1. Recherche 'massif':")
    global_search.search_and_display("massif")
    
    # Recherche par propriété mécanique
    print("\n2. Recherche 'E0_mean':")
    global_search.search_and_display("E0_mean")
    
    # Recherche combinée
    print("\n3. Recherche 'bois lamellé' (AND):")
    global_search.search_and_display(["bois", "lamellé"], "AND")

def demo_bases_disponibles():
    """Démonstration de la liste des bases"""
    print("\n📁 DÉMONSTRATION DES BASES DISPONIBLES")
    print("=" * 60)
    
    databases = global_search.get_all_databases()
    
    if not databases:
        print("Aucune base de données trouvée")
        return
    
    print(f"Bases de données trouvées: {len(databases)}")
    
    json_dbs = []
    sqlite_dbs = []
    
    for db_name, db_file in databases.items():
        if db_file.suffix == '.json':
            json_dbs.append(db_name)
        elif db_file.suffix == '.db':
            sqlite_dbs.append(db_name)
    
    if json_dbs:
        print(f"\n📄 Bases JSON ({len(json_dbs)}):")
        for db_name in json_dbs:
            print(f"  - {db_name}")
    
    if sqlite_dbs:
        print(f"\n🗄️ Bases SQLite ({len(sqlite_dbs)}):")
        for db_name in sqlite_dbs:
            print(f"  - {db_name}")

def demo_utilisation_repl():
    """Démonstration de l'utilisation en REPL"""
    print("\n🐍 DÉMONSTRATION DE L'UTILISATION EN REPL")
    print("=" * 60)
    
    print("""
Pour utiliser la recherche globale en REPL:

1. Lancer le REPL:
   python -i repl_db_test.py

2. Exemples d'utilisation:
   
   # Recherche simple
   results = global_search.global_search('C24')
   global_search.display_results(results)
   
   # Recherche multiple AND
   results = global_search.global_search(['C24', 'fm_k'], 'AND')
   global_search.display_results(results)
   
   # Recherche multiple OR
   results = global_search.global_search(['C24', 'GL24h'], 'OR')
   global_search.display_results(results)
   
   # Recherche et affichage en une fois
   global_search.search_and_display('C24')
   global_search.search_and_display(['valeur A', 'valeur B'], 'AND')
   
   # Mode interactif
   global_search.interactive_search()
""")

def main():
    """Fonction principale de démonstration"""
    print("🚀 DÉMONSTRATION DE LA RECHERCHE GLOBALE")
    print("=" * 80)
    
    try:
        demo_bases_disponibles()
        demo_recherche_simple()
        demo_recherche_multiple()
        demo_recherche_avancee()
        demo_utilisation_repl()
        
        print("\n" + "=" * 80)
        print("🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS!")
        print("\n📝 RÉSUMÉ DES FONCTIONNALITÉS:")
        print("✅ Recherche dans toutes les bases de données")
        print("✅ Support JSON et SQLite")
        print("✅ Recherche AND/OR flexible")
        print("✅ Mots-clés illimités")
        print("✅ Mode interactif")
        print("✅ Interface CLI complète")
        print("✅ Affichage formaté des résultats")
        
        print("\n💡 PROCHAINES ÉTAPES:")
        print("1. Utiliser: python -i repl_db_test.py")
        print("2. Tester: lcpi search global 'C24'")
        print("3. Mode interactif: lcpi search interactive")
        print("4. Ajouter de nouvelles bases de données")
        print("5. Intégrer dans vos workflows")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 