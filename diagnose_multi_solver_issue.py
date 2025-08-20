#!/usr/bin/env python3
"""
Script de diagnostic pour analyser le problème des résultats multi-solveurs identiques
"""

import json
import hashlib
from pathlib import Path

def analyze_multi_solver_files():
    """Analyse les fichiers multi-solveurs pour détecter les problèmes"""
    
    print("🔍 Diagnostic des fichiers multi-solveurs")
    print("=" * 60)
    
    # Fichiers à analyser
    files = {
        "multi": "results/out_multi_multi.json",
        "epanet": "results/out_multi_epanet.json", 
        "lcpi": "results/out_multi_lcpi.json"
    }
    
    # Vérifier l'existence des fichiers
    for name, path in files.items():
        file_path = Path(path)
        if file_path.exists():
            print(f"✅ {name}: {path} (existe)")
        else:
            print(f"❌ {name}: {path} (manquant)")
            return False
    
    # Analyser le fichier multi-solveurs
    print("\n📋 Analyse du fichier multi-solveurs:")
    with open(files["multi"], 'r', encoding='utf-8') as f:
        multi_data = json.load(f)
    
    print(f"  Solveurs déclarés: {multi_data.get('meta', {}).get('solvers', [])}")
    print(f"  Fichiers référencés: {list(multi_data.get('results', {}).keys())}")
    
    # Analyser les fichiers individuels
    print("\n📊 Analyse des fichiers individuels:")
    
    epanet_data = None
    lcpi_data = None
    
    try:
        with open(files["epanet"], 'r', encoding='utf-8') as f:
            epanet_data = json.load(f)
        print(f"✅ EPANET: {len(epanet_data.get('proposals', []))} propositions")
    except Exception as e:
        print(f"❌ Erreur lecture EPANET: {e}")
    
    try:
        with open(files["lcpi"], 'r', encoding='utf-8') as f:
            lcpi_data = json.load(f)
        print(f"✅ LCPI: {len(lcpi_data.get('proposals', []))} propositions")
    except Exception as e:
        print(f"❌ Erreur lecture LCPI: {e}")
    
    if epanet_data and lcpi_data:
        # Comparer les métadonnées
        print("\n🔍 Comparaison des métadonnées:")
        epanet_meta = epanet_data.get('meta', {})
        lcpi_meta = lcpi_data.get('meta', {})
        
        print(f"  EPANET solver: {epanet_meta.get('solver')}")
        print(f"  LCPI solver: {lcpi_meta.get('solver')}")
        print(f"  EPANET method: {epanet_meta.get('method')}")
        print(f"  LCPI method: {lcpi_meta.get('method')}")
        
        # Comparer les meilleures propositions
        print("\n🔍 Comparaison des meilleures propositions:")
        epanet_best = epanet_data.get('proposals', [{}])[0] if epanet_data.get('proposals') else {}
        lcpi_best = lcpi_data.get('proposals', [{}])[0] if lcpi_data.get('proposals') else {}
        
        print(f"  EPANET CAPEX: {epanet_best.get('CAPEX')}")
        print(f"  LCPI CAPEX: {lcpi_best.get('CAPEX')}")
        print(f"  EPANET min_pressure: {epanet_best.get('min_pressure_m')}")
        print(f"  LCPI min_pressure: {lcpi_best.get('min_pressure_m')}")
        
        # Calculer les hashes pour vérifier l'identité
        epanet_hash = hashlib.md5(json.dumps(epanet_data, sort_keys=True).encode()).hexdigest()
        lcpi_hash = hashlib.md5(json.dumps(lcpi_data, sort_keys=True).encode()).hexdigest()
        
        print(f"\n🔐 Hashes des fichiers:")
        print(f"  EPANET: {epanet_hash}")
        print(f"  LCPI: {lcpi_hash}")
        
        if epanet_hash == lcpi_hash:
            print("\n🚨 PROBLÈME DÉTECTÉ: Les fichiers sont identiques!")
            print("   Cela signifie que le même solveur a été utilisé pour les deux.")
        else:
            print("\n✅ Les fichiers sont différents")
    
    return True

def check_command_execution():
    """Vérifie comment la commande a été exécutée"""
    
    print("\n🔧 Analyse de l'exécution de la commande:")
    print("=" * 60)
    
    # Commande originale
    original_cmd = """lcpi aep network-optimize-unified src\\lcpi\\aep\\PROTOTYPE\\INP\\bismark-Administrator.inp --method genetic --solvers epanet,lcpi --pression-min 12 --vitesse-max 2.0 --output results\\out_multi.json --report html --no-log"""
    
    print("Commande originale:")
    print(f"  {original_cmd}")
    
    print("\n🔍 Problèmes potentiels identifiés:")
    print("  1. Le paramètre --solvers epanet,lcpi n'est peut-être pas supporté")
    print("  2. La commande n'a peut-être exécuté qu'un seul solveur")
    print("  3. Les résultats ont peut-être été copiés d'un solveur à l'autre")
    print("  4. Le système multi-solveurs n'est peut-être pas implémenté")
    
    # Vérifier les logs
    log_files = list(Path("logs").glob("*.json"))
    if log_files:
        print(f"\n📋 Logs disponibles: {len(log_files)} fichiers")
        for log_file in log_files[-3:]:  # 3 derniers logs
            print(f"  - {log_file.name}")
    else:
        print("\n📋 Aucun log trouvé")

def suggest_solutions():
    """Suggère des solutions pour corriger le problème"""
    
    print("\n💡 Solutions suggérées:")
    print("=" * 60)
    
    print("1. 🔧 Exécuter les solveurs séparément:")
    print("   lcpi aep network-optimize-unified src\\lcpi\\aep\\PROTOTYPE\\INP\\bismark-Administrator.inp --method genetic --solver epanet --pression-min 12 --vitesse-max 2.0 --output results\\out_epanet.json")
    print("   lcpi aep network-optimize-unified src\\lcpi\\aep\\PROTOTYPE\\INP\\bismark-Administrator.inp --method genetic --solver lcpi --pression-min 12 --vitesse-max 2.0 --output results\\out_lcpi.json")
    
    print("\n2. 🔧 Créer manuellement le fichier multi-solveurs:")
    print("   - Générer les résultats séparément")
    print("   - Créer le fichier multi-solveurs avec les bonnes références")
    
    print("\n3. 🔧 Vérifier la documentation:")
    print("   - Consulter la documentation de la commande network-optimize-unified")
    print("   - Vérifier si le paramètre --solvers est supporté")
    
    print("\n4. 🔧 Tester avec des paramètres différents:")
    print("   - Essayer avec --solver au lieu de --solvers")
    print("   - Vérifier les options disponibles avec --help")

def create_test_script():
    """Crée un script de test pour exécuter les solveurs séparément"""
    
    script_content = '''#!/usr/bin/env python3
"""
Script de test pour exécuter les solveurs séparément
"""

import subprocess
import json
from pathlib import Path

def run_solver_test():
    """Exécute les solveurs séparément pour tester"""
    
    base_cmd = [
        "lcpi", "aep", "network-optimize-unified",
        "src\\lcpi\\aep\\PROTOTYPE\\INP\\bismark-Administrator.inp",
        "--method", "genetic",
        "--pression-min", "12",
        "--vitesse-max", "2.0",
        "--output"
    ]
    
    solvers = ["epanet", "lcpi"]
    
    for solver in solvers:
        output_file = f"results/test_{solver}_separate.json"
        cmd = base_cmd + [output_file, "--solver", solver]
        
        print(f"🔄 Exécution de {solver}...")
        print(f"   Commande: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print(f"✅ {solver} terminé avec succès")
                
                # Vérifier le contenu
                if Path(output_file).exists():
                    with open(output_file, 'r') as f:
                        data = json.load(f)
                    solver_used = data.get('meta', {}).get('solver', 'unknown')
                    print(f"   Solveur utilisé: {solver_used}")
                    print(f"   CAPEX: {data.get('proposals', [{}])[0].get('CAPEX', 'N/A')}")
            else:
                print(f"❌ {solver} échoué")
                print(f"   Erreur: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"⏰ {solver} timeout")
        except Exception as e:
            print(f"❌ Erreur {solver}: {e}")

if __name__ == "__main__":
    run_solver_test()
'''
    
    script_file = Path("test_solvers_separately.py")
    script_file.write_text(script_content, encoding='utf-8')
    print(f"\n📝 Script de test créé: {script_file}")

def main():
    """Fonction principale"""
    print("🚨 Diagnostic du problème multi-solveurs")
    print("=" * 80)
    
    # Analyser les fichiers
    analyze_multi_solver_files()
    
    # Vérifier l'exécution
    check_command_execution()
    
    # Suggérer des solutions
    suggest_solutions()
    
    # Créer un script de test
    create_test_script()
    
    print("\n" + "=" * 80)
    print("🎯 Prochaines étapes:")
    print("1. Exécuter: python test_solvers_separately.py")
    print("2. Vérifier que les solveurs produisent des résultats différents")
    print("3. Créer manuellement le fichier multi-solveurs si nécessaire")
    print("4. Tester le rapport avec les vrais résultats multi-solveurs")

if __name__ == "__main__":
    main()
