#!/usr/bin/env python3
"""
Script d'investigation des diamètres candidats
"""
import json
from pathlib import Path
import sqlite3

def check_price_db():
    """Vérifier la base de prix pour les diamètres disponibles"""
    db_path = Path("src/lcpi/db/aep_prices.db")
    print(f"🔍 Vérification de la base de prix: {db_path}")
    
    if not db_path.exists():
        print("❌ Base de prix non trouvée")
        return []
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les tables disponibles
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Tables disponibles: {[t[0] for t in tables]}")
        
        # Chercher les diamètres PVC-U
        cursor.execute("""
            SELECT DISTINCT dn_mm, total_fcfa_per_m, material 
            FROM diameters 
            WHERE material LIKE '%PVC%' 
            ORDER BY dn_mm
        """)
        pvc_diams = cursor.fetchall()
        
        print(f"🔧 Diamètres PVC-U disponibles: {len(pvc_diams)}")
        for diam, cost, material in pvc_diams:
            print(f"  - {diam}mm: {cost} FCFA/m ({material})")
        
        conn.close()
        return pvc_diams
        
    except Exception as e:
        print(f"❌ Erreur lecture base de prix: {e}")
        return []

def check_standard_diameters():
    """Vérifier les diamètres standards utilisés en fallback"""
    STANDARD_DIAMETERS = [50, 63, 75, 90, 110, 125, 140, 160, 180, 200, 225, 250, 280, 315, 355, 400, 450, 500]
    print(f"📏 Diamètres standards (fallback): {len(STANDARD_DIAMETERS)}")
    for i, diam in enumerate(STANDARD_DIAMETERS):
        print(f"  {i+1:2d}. {diam}mm")
    return STANDARD_DIAMETERS

def analyze_optimization_result(file_path):
    """Analyser un fichier de résultat d'optimisation"""
    print(f"\n🔍 Analyse du fichier: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Extraire les métadonnées
        meta = data.get('meta', {})
        print(f"📊 Métadonnées:")
        print(f"  - Méthode: {meta.get('method')}")
        print(f"  - Solveur: {meta.get('solver')}")
        print(f"  - Contraintes: {meta.get('constraints')}")
        
        # Analyser les propositions
        proposals = data.get('proposals', [])
        print(f"📋 Propositions: {len(proposals)}")
        
        for i, prop in enumerate(proposals):
            print(f"\n  Proposition {i+1}:")
            print(f"    - ID: {prop.get('id')}")
            print(f"    - H_tank: {prop.get('H_tank_m')}m")
            print(f"    - CAPEX: {prop.get('CAPEX'):,} FCFA")
            
            # Analyser les diamètres
            diameters = prop.get('diameters_mm', {})
            print(f"    - Nombre de conduites: {len(diameters)}")
            
            # Statistiques des diamètres
            diam_values = list(diameters.values())
            unique_diams = set(diam_values)
            print(f"    - Diamètres uniques: {sorted(unique_diams)}")
            print(f"    - Diamètre le plus fréquent: {max(set(diam_values), key=diam_values.count)}mm")
            
            # Vérifier si tous les diamètres sont identiques
            if len(unique_diams) == 1:
                print(f"    ⚠️  TOUS LES DIAMÈTRES IDENTIQUES: {list(unique_diams)[0]}mm")
            else:
                print(f"    ✅ Diamètres variés: {len(unique_diams)} valeurs différentes")
        
        return data
        
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return None

def check_demand_parameter():
    """Vérifier l'implémentation du paramètre --demand"""
    print(f"\n🔍 Vérification du paramètre --demand")
    
    # Chercher dans le code source
    cli_file = Path("src/lcpi/aep/cli.py")
    if cli_file.exists():
        content = cli_file.read_text(encoding='utf-8')
        
        # Chercher les références au paramètre demand
        demand_refs = []
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'demand' in line.lower():
                demand_refs.append((i, line.strip()))
        
        print(f"📝 Références à 'demand' dans cli.py: {len(demand_refs)}")
        for line_num, line in demand_refs[:10]:  # Afficher les 10 premières
            print(f"  Ligne {line_num}: {line}")
    
    # Chercher le gestionnaire de demandes
    demand_manager = Path("src/lcpi/aep/utils/inp_demand_manager_fixed.py")
    if demand_manager.exists():
        print(f"✅ Gestionnaire de demandes trouvé: {demand_manager}")
        content = demand_manager.read_text(encoding='utf-8')
        
        # Chercher la fonction handle_demand_logic
        if 'handle_demand_logic' in content:
            print("✅ Fonction handle_demand_logic trouvée")
        else:
            print("❌ Fonction handle_demand_logic non trouvée")
    else:
        print(f"❌ Gestionnaire de demandes non trouvé")

def main():
    print("🔍 INVESTIGATION DES DIAMÈTRES IDENTIQUES")
    print("=" * 60)
    
    # 1. Vérifier la base de prix
    pvc_diams = check_price_db()
    
    # 2. Vérifier les diamètres standards
    standard_diams = check_standard_diameters()
    
    # 3. Analyser les fichiers de résultats existants
    result_files = [
        "temp/out_bismark_inp_demand_600.json",
        "temp/out_bismark_inp_demand_improved.json",
        "temp/sim_500.json",
        "temp/sim_600.json"
    ]
    
    for file_path in result_files:
        if Path(file_path).exists():
            analyze_optimization_result(file_path)
        else:
            print(f"⚠️  Fichier non trouvé: {file_path}")
    
    # 4. Vérifier le paramètre --demand
    check_demand_parameter()
    
    # 5. Résumé des investigations
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DES INVESTIGATIONS")
    print("=" * 60)
    
    if pvc_diams:
        print(f"✅ Base de prix disponible avec {len(pvc_diams)} diamètres PVC-U")
    else:
        print("❌ Base de prix non disponible - utilisation des diamètres standards")
    
    print(f"📏 {len(standard_diams)} diamètres standards disponibles en fallback")
    print("🔍 Vérifiez les fichiers de résultats ci-dessus pour les anomalies")

if __name__ == "__main__":
    main()