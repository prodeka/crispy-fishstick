#!/usr/bin/env python3
"""
Script pour analyser les résultats de la commande nested multi-solveurs
"""

import json
import hashlib
from pathlib import Path

def analyze_nested_results():
    """Analyse les résultats de la commande nested"""
    
    print("🔍 Analyse des résultats nested multi-solveurs")
    print("=" * 60)
    
    # Fichiers à analyser
    files = {
        "multi": "results/out_multi_nested_multi.json",
        "epanet": "results/out_multi_nested_epanet.json", 
        "lcpi": "results/out_multi_nested_lcpi.json"
    }
    
    # Vérifier l'existence des fichiers
    for name, path in files.items():
        file_path = Path(path)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {name}: {path} (existe, {size:,} octets)")
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
        
        # Comparer les contraintes
        epanet_constraints = epanet_meta.get('constraints', {})
        lcpi_constraints = lcpi_meta.get('constraints', {})
        
        print(f"\n🔍 Comparaison des contraintes:")
        print(f"  EPANET pressure_min: {epanet_constraints.get('pressure_min_m')} m")
        print(f"  LCPI pressure_min: {lcpi_constraints.get('pressure_min_m')} m")
        print(f"  EPANET velocity_min: {epanet_constraints.get('velocity_min_m_s')} m/s")
        print(f"  LCPI velocity_min: {lcpi_constraints.get('velocity_min_m_s')} m/s")
        print(f"  EPANET velocity_max: {epanet_constraints.get('velocity_max_m_s')} m/s")
        print(f"  LCPI velocity_max: {lcpi_constraints.get('velocity_max_m_s')} m/s")
        
        # Comparer les meilleures propositions
        print("\n🔍 Comparaison des meilleures propositions:")
        epanet_proposals = epanet_data.get('proposals', [])
        lcpi_proposals = lcpi_data.get('proposals', [])
        
        if epanet_proposals and lcpi_proposals:
            epanet_best = epanet_proposals[0]
            lcpi_best = lcpi_proposals[0]
            
            print(f"  EPANET ID: {epanet_best.get('id')}")
            print(f"  LCPI ID: {lcpi_best.get('id')}")
            
            # Comparer les diamètres
            epanet_diameters = epanet_best.get('diameters_mm', {})
            lcpi_diameters = lcpi_best.get('diameters_mm', {})
            
            print(f"  EPANET diamètres: {len(epanet_diameters)} conduites")
            print(f"  LCPI diamètres: {len(lcpi_diameters)} conduites")
            
            # Vérifier si les diamètres sont identiques
            if epanet_diameters == lcpi_diameters:
                print("  ⚠️  ATTENTION: Les diamètres sont identiques!")
            else:
                print("  ✅ Les diamètres sont différents")
            
            # Comparer les métriques de performance
            epanet_metrics = epanet_best.get('metrics', {})
            lcpi_metrics = lcpi_best.get('metrics', {})
            
            print(f"\n📊 Métriques de performance:")
            print(f"  EPANET coût: {epanet_metrics.get('cost_fcfa', 'N/A')} FCFA")
            print(f"  LCPI coût: {lcpi_metrics.get('cost_fcfa', 'N/A')} FCFA")
            print(f"  EPANET performance: {epanet_metrics.get('performance', 'N/A')}")
            print(f"  LCPI performance: {lcpi_metrics.get('performance', 'N/A')}")
            
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
            
            # Analyser les différences spécifiques
            analyze_differences(epanet_data, lcpi_data)
    
    return True

def analyze_differences(epanet_data, lcpi_data):
    """Analyse les différences entre les deux solveurs"""
    
    print("\n🔍 Analyse détaillée des différences:")
    
    # Comparer les métadonnées
    epanet_meta = epanet_data.get('meta', {})
    lcpi_meta = lcpi_data.get('meta', {})
    
    if epanet_meta.get('solver') == lcpi_meta.get('solver'):
        print("  ⚠️  Problème: Les deux fichiers indiquent le même solveur")
        print(f"     Solveur déclaré: {epanet_meta.get('solver')}")
    
    # Comparer les propositions
    epanet_proposals = epanet_data.get('proposals', [])
    lcpi_proposals = lcpi_data.get('proposals', [])
    
    if len(epanet_proposals) != len(lcpi_proposals):
        print(f"  📊 Nombre de propositions différent:")
        print(f"     EPANET: {len(epanet_proposals)}")
        print(f"     LCPI: {len(lcpi_proposals)}")
    
    # Comparer les diamètres de la meilleure solution
    if epanet_proposals and lcpi_proposals:
        epanet_diameters = epanet_proposals[0].get('diameters_mm', {})
        lcpi_diameters = lcpi_proposals[0].get('diameters_mm', {})
        
        # Compter les différences
        differences = 0
        for pipe_id in epanet_diameters:
            if pipe_id in lcpi_diameters:
                if epanet_diameters[pipe_id] != lcpi_diameters[pipe_id]:
                    differences += 1
        
        print(f"  🔧 Différences de diamètres: {differences} conduites sur {len(epanet_diameters)}")
        
        if differences == 0:
            print("     ⚠️  Aucune différence de diamètre détectée")
        else:
            print("     ✅ Différences de diamètre détectées")

def check_command_execution():
    """Vérifie comment la commande a été exécutée"""
    
    print("\n🔧 Analyse de l'exécution de la commande:")
    print("=" * 60)
    
    # Commande exécutée
    executed_cmd = """lcpi aep network-optimize-unified src\\lcpi\\aep\\PROTOTYPE\\INP\\bismark-Administrator.inp --method genetic --solvers epanet,lcpi --vitesse-min 0.3 --vitesse-max 1.5 --hmax 30 --output results\\out_multi_nested.json --report html --no-log"""
    
    print("Commande exécutée:")
    print(f"  {executed_cmd}")
    
    print("\n📋 Paramètres utilisés:")
    print("  - Méthode: genetic")
    print("  - Solveurs: epanet,lcpi")
    print("  - Vitesse min: 0.3 m/s")
    print("  - Vitesse max: 1.5 m/s")
    print("  - Hauteur max: 30 m")
    print("  - Rapport: HTML")
    
    print("\n🔍 Problèmes potentiels identifiés:")
    print("  1. Le paramètre --solvers n'a peut-être pas fonctionné correctement")
    print("  2. Les deux solveurs ont peut-être utilisé le même algorithme")
    print("  3. Les résultats ont été copiés d'un solveur à l'autre")
    print("  4. Le système multi-solveurs n'est pas encore implémenté")

def suggest_solutions():
    """Suggère des solutions pour corriger le problème"""
    
    print("\n💡 Solutions suggérées:")
    print("=" * 60)
    
    print("1. 🔧 Exécuter les solveurs séparément:")
    print("   lcpi aep network-optimize-unified src\\lcpi\\aep\\PROTOTYPE\\INP\\bismark-Administrator.inp --method genetic --solver epanet --vitesse-min 0.3 --vitesse-max 1.5 --hmax 30 --output results\\out_nested_epanet.json")
    print("   lcpi aep network-optimize-unified src\\lcpi\\aep\\PROTOTYPE\\INP\\bismark-Administrator.inp --method genetic --solver lcpi --vitesse-min 0.3 --vitesse-max 1.5 --hmax 30 --output results\\out_nested_lcpi.json")
    
    print("\n2. 🔧 Vérifier la documentation:")
    print("   - Consulter la documentation de la commande network-optimize-unified")
    print("   - Vérifier si le paramètre --solvers est supporté")
    
    print("\n3. 🔧 Tester avec des paramètres différents:")
    print("   - Essayer avec --solver au lieu de --solvers")
    print("   - Vérifier les options disponibles avec --help")
    
    print("\n4. 🔧 Analyser les logs:")
    print("   - Vérifier les logs de la commande")
    print("   - Identifier pourquoi les solveurs produisent les mêmes résultats")

def main():
    """Fonction principale"""
    print("🚨 Analyse des résultats nested multi-solveurs")
    print("=" * 80)
    
    # Analyser les fichiers
    analyze_nested_results()
    
    # Vérifier l'exécution
    check_command_execution()
    
    # Suggérer des solutions
    suggest_solutions()
    
    print("\n" + "=" * 80)
    print("🎯 Prochaines étapes:")
    print("1. Exécuter les solveurs séparément pour vérifier")
    print("2. Vérifier la documentation de la commande")
    print("3. Tester avec des paramètres différents")
    print("4. Analyser les logs pour identifier le problème")

if __name__ == "__main__":
    main()
