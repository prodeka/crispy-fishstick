#!/usr/bin/env python3
"""
Script de comparaison entre l'ancien et le nouveau script d'extraction Excel
"""

import os
import sys
from extract_excel_formulas import extract_formulas
from extract_excel_formulas_improved import extract_formulas_improved

def compare_methods():
    """Compare les méthodes d'extraction"""
    
    excel_file = "Reseaux_2.xlsx"
    if not os.path.exists(excel_file):
        print(f"❌ Fichier Excel '{excel_file}' non trouvé")
        return False
    
    print("🔍 Comparaison des méthodes d'extraction Excel")
    print("=" * 70)
    
    # Test avec l'ancien script
    print("\n📋 Méthode ANCIENNE (extract_excel_formulas.py):")
    print("-" * 50)
    try:
        extract_formulas(
            excel_path=excel_file,
            output_dir="output_old_method",
            unique=True,
            split=True,
            max_rows=50  # Limiter pour la comparaison
        )
        
        # Analyser les résultats
        old_files = []
        if os.path.exists("output_old_method"):
            for file in os.listdir("output_old_method"):
                if file.startswith("valeurs_"):
                    file_path = os.path.join("output_old_method", file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        # Compter les lignes avec "None"
                        none_count = sum(1 for line in lines if 'None' in line and '|' in line)
                        total_lines = len([line for line in lines if '|' in line and line.strip()])
                        old_files.append({
                            'file': file,
                            'total_lines': total_lines,
                            'none_count': none_count,
                            'empty_percentage': (none_count / total_lines * 100) if total_lines > 0 else 0
                        })
        
        print("📊 Résultats de l'ancienne méthode:")
        for file_info in old_files:
            print(f"   📄 {file_info['file']}:")
            print(f"      - Total lignes: {file_info['total_lines']}")
            print(f"      - Lignes avec 'None': {file_info['none_count']}")
            print(f"      - Pourcentage de cellules vides: {file_info['empty_percentage']:.1f}%")
            
    except Exception as e:
        print(f"❌ Erreur avec l'ancienne méthode: {e}")
    
    # Test avec le nouveau script
    print("\n🚀 Méthode AMÉLIORÉE (extract_excel_formulas_improved.py):")
    print("-" * 50)
    try:
        extract_formulas_improved(
            excel_path=excel_file,
            output_dir="output_new_method",
            values_only=True,
            formulas_only=False,
            non_empty_only=True,
            split=True,
            max_rows=50  # Limiter pour la comparaison
        )
        
        # Analyser les résultats
        new_files = []
        if os.path.exists("output_new_method"):
            for file in os.listdir("output_new_method"):
                if file.startswith("valeurs_"):
                    file_path = os.path.join("output_new_method", file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        # Compter les lignes avec "None"
                        none_count = sum(1 for line in lines if 'None' in line and '|' in line)
                        total_lines = len([line for line in lines if '|' in line and line.strip()])
                        new_files.append({
                            'file': file,
                            'total_lines': total_lines,
                            'none_count': none_count,
                            'empty_percentage': (none_count / total_lines * 100) if total_lines > 0 else 0
                        })
        
        print("📊 Résultats de la nouvelle méthode:")
        for file_info in new_files:
            print(f"   📄 {file_info['file']}:")
            print(f"      - Total lignes: {file_info['total_lines']}")
            print(f"      - Lignes avec 'None': {file_info['none_count']}")
            print(f"      - Pourcentage de cellules vides: {file_info['empty_percentage']:.1f}%")
            
    except Exception as e:
        print(f"❌ Erreur avec la nouvelle méthode: {e}")
    
    # Comparaison
    print("\n📈 COMPARAISON:")
    print("-" * 50)
    
    if old_files and new_files:
        for old_file, new_file in zip(old_files, new_files):
            if old_file['file'] == new_file['file']:
                print(f"📄 {old_file['file']}:")
                print(f"   Ancienne méthode: {old_file['total_lines']} lignes, {old_file['empty_percentage']:.1f}% vides")
                print(f"   Nouvelle méthode: {new_file['total_lines']} lignes, {new_file['empty_percentage']:.1f}% vides")
                
                improvement = old_file['total_lines'] - new_file['total_lines']
                if improvement > 0:
                    print(f"   ✅ Amélioration: {improvement} lignes vides supprimées")
                else:
                    print(f"   ℹ️  Même nombre de lignes")
    
    print("\n🎯 AVANTAGES DE LA NOUVELLE MÉTHODE:")
    print("   ✅ Filtrage automatique des cellules vides")
    print("   ✅ Distinction visuelle entre formules et valeurs")
    print("   ✅ Options de filtrage avancées")
    print("   ✅ Extraction sélective (formules ou valeurs)")
    print("   ✅ Filtre de valeur minimale configurable")
    print("   ✅ Messages informatifs si aucune donnée trouvée")
    print("   ✅ Code plus maintenable et extensible")
    
    print("\n💡 RECOMMANDATIONS D'UTILISATION:")
    print("   🔧 Pour extraire uniquement les valeurs non vides:")
    print("      python extract_excel_formulas_improved.py --excel fichier.xlsx --output output --values-only")
    print("   🔧 Pour extraire uniquement les formules:")
    print("      python extract_excel_formulas_improved.py --excel fichier.xlsx --output output --formulas-only")
    print("   🔧 Pour filtrer les valeurs numériques > 0:")
    print("      python extract_excel_formulas_improved.py --excel fichier.xlsx --output output --values-only --min-value 0.1")
    
    return True

if __name__ == "__main__":
    compare_methods() 