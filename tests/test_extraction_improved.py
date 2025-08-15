#!/usr/bin/env python3
"""
Script de test pour démontrer les améliorations du script d'extraction Excel
"""

import os
import sys
from extract_excel_formulas_improved import extract_formulas_improved

def test_extraction():
    """Test des différentes options d'extraction"""
    
    excel_file = "Reseaux_2.xlsx"
    if not os.path.exists(excel_file):
        print(f"❌ Fichier Excel '{excel_file}' non trouvé")
        return False
    
    print("🧪 Test des améliorations du script d'extraction Excel")
    print("=" * 60)
    
    # Test 1: Extraction des valeurs non vides uniquement
    print("\n1️⃣ Test: Extraction des valeurs non vides uniquement")
    try:
        extract_formulas_improved(
            excel_path=excel_file,
            output_dir="output_test_values_only",
            values_only=True,
            formulas_only=False,
            non_empty_only=True,
            split=True,
            max_rows=100  # Limiter pour le test
        )
        print("✅ Extraction des valeurs réussie")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 2: Extraction des formules uniquement
    print("\n2️⃣ Test: Extraction des formules uniquement")
    try:
        extract_formulas_improved(
            excel_path=excel_file,
            output_dir="output_test_formulas_only",
            values_only=False,
            formulas_only=True,
            split=True,
            max_rows=100
        )
        print("✅ Extraction des formules réussie")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 3: Extraction complète (formules + valeurs non vides)
    print("\n3️⃣ Test: Extraction complète (formules + valeurs non vides)")
    try:
        extract_formulas_improved(
            excel_path=excel_file,
            output_dir="output_test_complete",
            values_only=False,
            formulas_only=False,
            non_empty_only=True,
            split=True,
            max_rows=100
        )
        print("✅ Extraction complète réussie")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 4: Extraction avec filtre de valeur minimale
    print("\n4️⃣ Test: Extraction avec filtre de valeur minimale (>0)")
    try:
        extract_formulas_improved(
            excel_path=excel_file,
            output_dir="output_test_min_value",
            values_only=True,
            formulas_only=False,
            non_empty_only=True,
            min_value=0.1,  # Seulement les valeurs > 0.1
            split=True,
            max_rows=100
        )
        print("✅ Extraction avec filtre de valeur réussie")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("📊 Résumé des tests:")
    
    # Vérification des fichiers générés
    test_dirs = [
        "output_test_values_only",
        "output_test_formulas_only", 
        "output_test_complete",
        "output_test_min_value"
    ]
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            files = os.listdir(test_dir)
            print(f"📁 {test_dir}: {len(files)} fichiers générés")
            for file in files[:3]:  # Afficher les 3 premiers fichiers
                print(f"   - {file}")
            if len(files) > 3:
                print(f"   ... et {len(files) - 3} autres fichiers")
        else:
            print(f"❌ {test_dir}: Dossier non créé")
    
    print("\n🎯 Améliorations apportées:")
    print("   ✅ Filtrage des cellules vides (None, '', espaces)")
    print("   ✅ Distinction visuelle entre formules et valeurs")
    print("   ✅ Options de filtrage avancées")
    print("   ✅ Extraction sélective (formules ou valeurs)")
    print("   ✅ Filtre de valeur minimale")
    print("   ✅ Messages d'information si aucune donnée trouvée")
    
    return True

if __name__ == "__main__":
    test_extraction() 