#!/usr/bin/env python3
"""
Script de test pour valider les nouvelles fonctionnalités de la classe PriceDB.
Teste les trois nouvelles méthodes utilitaires ajoutées dans la Section B.
"""

import sys
import os
import tempfile

# Ajoute la racine du projet au path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.lcpi.aep.optimizer.db import PriceDB

def test_new_features():
    """Teste les nouvelles fonctionnalités de PriceDB."""
    print("=== Test des nouvelles fonctionnalités PriceDB ===\n")
    
    # 1. Initialisation de PriceDB
    print("1. Initialisation de PriceDB...")
    db = PriceDB()
    print(f"   ✓ PriceDB initialisée avec {len(db._candidate_diameters)} diamètres")
    print(f"   ✓ Source de données : {db.db_info['type']}")
    print()
    
    # 2. Test de get_price_for_length
    print("2. Test de get_price_for_length...")
    test_cases = [
        (110, 100, "PVC"),  # 100m de PVC DN110
        (200, 50, "PEHD"),  # 50m de PEHD DN200
        (150, 25, "Fonte"), # 25m de Fonte DN150
        (110, 0, "PVC"),    # Longueur nulle
        (999, 100, "PVC"),  # Diamètre inexistant
    ]
    
    for dn_mm, length_m, material in test_cases:
        price = db.get_price_for_length(dn_mm, length_m, material)
        if price is not None:
            print(f"   ✓ DN{dn_mm} {material} x {length_m}m = {price:,.0f} FCFA")
        else:
            print(f"   ⚠ DN{dn_mm} {material} x {length_m}m = Non trouvé")
    print()
    
    # 3. Test de dump_candidates_to_csv
    print("3. Test de dump_candidates_to_csv...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        csv_path = tmp_file.name
    
    try:
        db.dump_candidates_to_csv(csv_path)
        print(f"   ✓ Export CSV réussi vers {csv_path}")
        
        # Vérification rapide du fichier
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"   ✓ Fichier contient {len(lines)} lignes (dont l'en-tête)")
            
    except Exception as e:
        print(f"   ✗ Erreur lors de l'export CSV : {e}")
    finally:
        # Nettoyage
        if os.path.exists(csv_path):
            os.unlink(csv_path)
    print()
    
    # 4. Test de run_sanity_checks
    print("4. Test de run_sanity_checks...")
    is_sane = db.run_sanity_checks()
    if is_sane:
        print("   ✓ Sanity checks passés avec succès")
    else:
        print("   ⚠ Sanity checks ont détecté des anomalies")
    print()
    
    # 5. Test avec des paramètres personnalisés
    print("5. Test de run_sanity_checks avec paramètres personnalisés...")
    is_sane_custom = db.run_sanity_checks(min_expected_price=50.0, max_expected_price=500000.0)
    if is_sane_custom:
        print("   ✓ Sanity checks personnalisés passés")
    else:
        print("   ⚠ Sanity checks personnalisés ont détecté des anomalies")
    print()
    
    print("=== Tests terminés ===")

if __name__ == "__main__":
    test_new_features()
