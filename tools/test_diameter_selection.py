#!/usr/bin/env python3
"""
Test de sélection des diamètres - Investigation du problème 200mm uniforme
"""
import json
import sqlite3
from pathlib import Path
import sys

def check_diameter_constraints():
    """Vérifier les contraintes qui pourraient forcer 200mm"""
    print("🔍 VÉRIFICATION DES CONTRAINTES DE DIAMÈTRE")
    print("=" * 50)
    
    # Vérifier la base de prix
    db_path = Path("src/lcpi/db/aep_prices.db")
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les diamètres autour de 200mm
        cursor.execute("""
            SELECT dn_mm, total_fcfa_per_m, material 
            FROM diameters 
            WHERE material = 'PVC-U' AND dn_mm BETWEEN 160 AND 250
            ORDER BY dn_mm
        """)
        nearby_diams = cursor.fetchall()
        
        print(f"📏 Diamètres PVC-U autour de 200mm:")
        for diam, cost, material in nearby_diams:
            print(f"  - {diam}mm: {cost:,.0f} FCFA/m")
        
        conn.close()
    else:
        print("❌ Base de prix non trouvée")

def analyze_network_constraints():
    """Analyser les contraintes du réseau qui pourraient forcer 200mm"""
    print("\n🔍 ANALYSE DES CONTRAINTES DU RÉSEAU")
    print("=" * 50)
    
    # Lire le fichier .inp pour analyser les contraintes
    inp_file = Path("bismark_inp.inp")
    if not inp_file.exists():
        print("❌ Fichier bismark_inp.inp non trouvé")
        return
    
    with open(inp_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chercher les sections importantes
    sections = ['[PIPES]', '[JUNCTIONS]', '[DEMANDS]', '[TANKS]']
    for section in sections:
        if section in content:
            print(f"✅ Section {section} trouvée")
        else:
            print(f"❌ Section {section} manquante")
    
    # Analyser les conduites
    if '[PIPES]' in content:
        pipes_start = content.find('[PIPES]')
        pipes_end = content.find('[', pipes_start + 1)
        if pipes_end == -1:
            pipes_end = len(content)
        
        pipes_section = content[pipes_start:pipes_end]
        pipe_lines = [line.strip() for line in pipes_section.split('\n') if line.strip() and not line.startswith(';') and not line.startswith('[PIPES]')]
        
        print(f"📊 Nombre de conduites: {len(pipe_lines)}")
        
        # Analyser les longueurs et débits
        lengths = []
        for line in pipe_lines:
            parts = line.split()
            if len(parts) >= 4:
                try:
                    length = float(parts[3])
                    lengths.append(length)
                except:
                    pass
        
        if lengths:
            print(f"📏 Longueurs des conduites:")
            print(f"  - Min: {min(lengths):.1f}m")
            print(f"  - Max: {max(lengths):.1f}m")
            print(f"  - Moyenne: {sum(lengths)/len(lengths):.1f}m")

def test_diameter_selection_algorithm():
    """Tester l'algorithme de sélection des diamètres"""
    print("\n🔍 TEST DE L'ALGORITHME DE SÉLECTION")
    print("=" * 50)
    
    # Importer les modules nécessaires
    try:
        from src.lcpi.aep.optimization.genetic_algorithm import GeneticOptimizer
        from src.lcpi.aep.utils.price_manager import PriceManager
        print("✅ Modules importés avec succès")
        
        # Vérifier la base de prix
        price_manager = PriceManager()
        print(f"✅ PriceManager initialisé")
        
        # Vérifier les diamètres disponibles
        available_diameters = price_manager.get_available_diameters('PVC-U')
        print(f"📏 Diamètres PVC-U disponibles: {len(available_diameters)}")
        print(f"  - Min: {min(available_diameters)}mm")
        print(f"  - Max: {max(available_diameters)}mm")
        
        # Vérifier pourquoi 200mm est toujours choisi
        if 200 in available_diameters:
            cost_200 = price_manager.get_pipe_cost(200, 'PVC-U')
            print(f"💰 Coût 200mm PVC-U: {cost_200:,.0f} FCFA/m")
            
            # Comparer avec d'autres diamètres
            for diam in [160, 180, 225, 250]:
                if diam in available_diameters:
                    cost = price_manager.get_pipe_cost(diam, 'PVC-U')
                    print(f"💰 Coût {diam}mm PVC-U: {cost:,.0f} FCFA/m")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def check_optimization_constraints():
    """Vérifier les contraintes d'optimisation"""
    print("\n🔍 VÉRIFICATION DES CONTRAINTES D'OPTIMISATION")
    print("=" * 50)
    
    # Lire un fichier de résultat pour analyser les contraintes
    result_file = Path("temp/out_bismark_inp_demand_600.json")
    if result_file.exists():
        with open(result_file, 'r') as f:
            data = json.load(f)
        
        constraints = data.get('meta', {}).get('constraints', {})
        print(f"📋 Contraintes appliquées:")
        for key, value in constraints.items():
            print(f"  - {key}: {value}")
        
        # Analyser les performances
        proposals = data.get('proposals', [])
        if proposals:
            prop = proposals[0]
            performance = prop.get('performance', {})
            print(f"\n📊 Performances obtenues:")
            for key, value in performance.items():
                print(f"  - {key}: {value}")

def check_database_integration():
    """Vérifier l'intégration complète de la base de données"""
    print("\n🔍 VÉRIFICATION DE L'INTÉGRATION BASE DE DONNÉES")
    print("=" * 50)
    
    db_path = Path("src/lcpi/db/aep_prices.db")
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tables dans la base: {[t[0] for t in tables]}")
        
        # Analyser la table diameters
        cursor.execute("SELECT COUNT(*) FROM diameters")
        total_diams = cursor.fetchone()[0]
        print(f"📊 Total diamètres: {total_diams}")
        
        # Analyser par matériau
        cursor.execute("""
            SELECT material, COUNT(*) as count, 
                   MIN(dn_mm) as min_diam, MAX(dn_mm) as max_diam,
                   AVG(total_fcfa_per_m) as avg_cost
            FROM diameters 
            GROUP BY material
            ORDER BY material
        """)
        materials = cursor.fetchall()
        
        print(f"\n📋 Analyse par matériau:")
        for material, count, min_diam, max_diam, avg_cost in materials:
            print(f"  - {material}: {count} diamètres ({min_diam}-{max_diam}mm), coût moyen: {avg_cost:,.0f} FCFA/m")
        
        # Vérifier la cohérence des prix
        cursor.execute("""
            SELECT dn_mm, material, total_fcfa_per_m,
                   supply_fcfa_per_m, pose_fcfa_per_m
            FROM diameters 
            WHERE material = 'PVC-U' AND dn_mm IN (160, 180, 200, 225, 250)
            ORDER BY dn_mm
        """)
        pvc_prices = cursor.fetchall()
        
        print(f"\n💰 Prix PVC-U détaillés:")
        for diam, material, total, supply, pose in pvc_prices:
            print(f"  - {diam}mm: Total={total:,.0f}, Supply={supply:,.0f}, Pose={pose:,.0f}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")

def main():
    print("🔍 TEST COMPLET DE SÉLECTION DES DIAMÈTRES")
    print("=" * 60)
    
    # 1. Vérifier les contraintes de diamètre
    check_diameter_constraints()
    
    # 2. Analyser les contraintes du réseau
    analyze_network_constraints()
    
    # 3. Tester l'algorithme de sélection
    test_diameter_selection_algorithm()
    
    # 4. Vérifier les contraintes d'optimisation
    check_optimization_constraints()
    
    # 5. Vérifier l'intégration base de données
    check_database_integration()
    
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 60)
    print("🔍 Vérifiez les résultats ci-dessus pour identifier pourquoi 200mm est toujours choisi")

if __name__ == "__main__":
    main()