#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from lcpi.db_manager import sql_query_cli

print("🔍 TEST DES REQUÊTES SQL")
print("=" * 50)

# Test 1: Bois avec fm_k > 20
print("\n1. Bois avec fm_k > 20:")
sql_query_cli("bois_test_sqlite", "SELECT Classe, fm_k_MPa FROM Valeurs_caractéristiques_des_bois_massifs_résineux WHERE CAST(fm_k_MPa AS FLOAT) > 20")

# Test 2: Comparaison des modules d'Young
print("\n2. Comparaison des modules d'Young:")
sql_query_cli("bois_test_sqlite", "SELECT Classe, E0_mean_KN_mm2 FROM Valeurs_caractéristiques_des_bois_massifs_résineux ORDER BY CAST(E0_mean_KN_mm2 AS FLOAT) DESC")

# Test 3: Tous les bois lamellés-collés
print("\n3. Tous les bois lamellés-collés:")
sql_query_cli("bois_test_sqlite", "SELECT Classe, fm_k_MPa, E0_mean_KN_mm2 FROM Valeurs_caractéristiques_des_bois_lamellés_collés_homogènes")

# Test 4: Union des deux types de bois
print("\n4. Union des deux types de bois:")
sql_query_cli("bois_test_sqlite", """
SELECT Classe, fm_k_MPa, 'Massif' as Type 
FROM Valeurs_caractéristiques_des_bois_massifs_résineux
UNION ALL
SELECT Classe, fm_k_MPa, 'Lamellé-collé' as Type 
FROM Valeurs_caractéristiques_des_bois_lamellés_collés_homogènes
ORDER BY CAST(fm_k_MPa AS FLOAT) DESC
""") 