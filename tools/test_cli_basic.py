#!/usr/bin/env python3
"""
Script de test simple pour vérifier que le CLI LCPI fonctionne et génère des résultats.
Objectif : Diagnostiquer pourquoi aucun fichier de résultats n'est créé.
"""

import sys
import subprocess
import os
import json
from pathlib import Path
from typing import Dict, Any

def test_cli_basic_functionality():
    """Teste la fonctionnalité de base du CLI LCPI."""
    
    print("🧪 TEST DE FONCTIONNALITÉ DE BASE DU CLI LCPI")
    print("=" * 60)
    
    # Vérifier que le fichier INP existe
    input_file = "bismark_inp.inp"
    if not Path(input_file).exists():
        print(f"❌ Fichier d'entrée non trouvé: {input_file}")
        return False
    
    print(f"✅ Fichier d'entrée trouvé: {input_file}")
    
    # Test 1: Vérifier que le module CLI est accessible
    print("\n🔍 Test 1: Accessibilité du module CLI")
    try:
        import lcpi.aep.cli
        print("✅ Module lcpi.aep.cli importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    
    # Test 2: Vérifier que la commande network-optimize-unified existe
    print("\n🔍 Test 2: Vérification de la commande network-optimize-unified")
    try:
        result = subprocess.run([
            sys.executable, "-m", "lcpi.aep.cli", "--help"
        ], capture_output=True, text=True, timeout=30)
        
        if "network-optimize-unified" in result.stdout:
            print("✅ Commande network-optimize-unified détectée")
        else:
            print("❌ Commande network-optimize-unified non trouvée")
            print("Commandes disponibles:")
            print(result.stdout)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️ Timeout lors de la vérification des commandes")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False
    
    # Test 3: Test simple avec LCPI (sans EPANET)
    print("\n🔍 Test 3: Test simple avec LCPI (générations réduites)")
    
    output_name = "test_cli_basic_lcpi"
    cmd = [
        sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
        input_file,
        "--method", "genetic",
        "--generations", "5",  # Très peu de générations pour test rapide
        "--population", "10",  # Petite population pour test rapide
        "--solver", "lcpi",
        "--pression-min", "15.0",
        "--vitesse-max", "2.0",
        "--vitesse-min", "0.5",
        "--output", output_name,
        "--no-log"
    ]
    
    print(f"   🔄 Exécution: {' '.join(cmd)}")
    
    try:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env,
            timeout=120  # 2 minutes max
        )
        
        print(f"   📊 Code de retour: {result.returncode}")
        
        if result.stdout:
            print("   📤 stdout (dernières lignes):")
            lines = result.stdout.strip().split('\n')
            for line in lines[-10:]:  # Dernières 10 lignes
                print(f"      {line}")
        
        if result.stderr:
            print("   📤 stderr (dernières lignes):")
            lines = result.stderr.strip().split('\n')
            for line in lines[-10:]:  # Dernières 10 lignes
                print(f"      {line}")
        
        # Vérifier si des fichiers ont été créés
        print("\n🔍 Vérification des fichiers créés:")
        
        # Chercher dans différents emplacements
        search_paths = [
            Path(f"{output_name}.json"),
            Path("results") / f"{output_name}.json",
            Path("results") / f"{output_name}_*.json",
            Path("output") / f"{output_name}.json",
            Path("output") / f"{output_name}_*.json"
        ]
        
        files_found = []
        for search_path in search_paths:
            if search_path.exists():
                if search_path.is_file():
                    files_found.append(search_path)
                elif search_path.is_dir() or "*" in str(search_path):
                    # Chercher des fichiers correspondants
                    if "*" in str(search_path):
                        pattern = str(search_path).replace("*", "*")
                        matches = list(Path(search_path.parent).glob(search_path.name))
                        files_found.extend(matches)
                    else:
                        matches = list(search_path.glob("*.json"))
                        files_found.extend(matches)
        
        if files_found:
            print("✅ Fichiers trouvés:")
            for file_path in files_found:
                print(f"   📄 {file_path}")
                
                # Essayer de lire le contenu
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    print(f"      📊 Type: {type(data)}")
                    if isinstance(data, dict):
                        print(f"      🔑 Clés: {list(data.keys())}")
                        if "proposals" in data:
                            proposals = data["proposals"]
                            print(f"      📋 Propositions: {len(proposals)}")
                            if proposals:
                                best = proposals[0]
                                print(f"      🏆 Meilleure: {best.get('CAPEX', 'N/A')} FCFA")
                                print(f"      ✅ Faisable: {best.get('constraints_ok', 'N/A')}")
                except Exception as e:
                    print(f"      ❌ Erreur lecture: {e}")
        else:
            print("❌ Aucun fichier de résultats trouvé")
            print("   📁 Dossiers vérifiés:")
            for search_path in search_paths:
                parent = search_path.parent if search_path.parent != Path(".") else Path(".")
                if parent.exists():
                    print(f"      {parent}/")
                    if parent.is_dir():
                        files = list(parent.glob("*.json"))
                        if files:
                            print(f"         Fichiers JSON: {[f.name for f in files[:5]]}")
                        else:
                            print("         Aucun fichier JSON")
        
        return result.returncode == 0 and len(files_found) > 0
        
    except subprocess.TimeoutExpired:
        print("   ⏱️ Timeout après 2 minutes")
        return False
    except Exception as e:
        print(f"   ❌ Erreur d'exécution: {e}")
        return False

def main():
    """Fonction principale."""
    
    print("🔧 TEST DE FONCTIONNALITÉ DE BASE DU CLI LCPI")
    print("=" * 80)
    print("Objectif: Diagnostiquer pourquoi aucun fichier de résultats n'est créé")
    
    success = test_cli_basic_functionality()
    
    print("\n" + "=" * 80)
    if success:
        print("✅ TEST RÉUSSI: Le CLI LCPI fonctionne et génère des résultats")
        print("🎯 Prochaine étape: Analyser la qualité des résultats générés")
    else:
        print("❌ TEST ÉCHOUÉ: Problème avec le CLI LCPI ou génération de résultats")
        print("🔧 Actions recommandées:")
        print("   1. Vérifier l'installation du module LCPI")
        print("   2. Vérifier les permissions d'écriture")
        print("   3. Analyser les logs d'erreur")
        print("   4. Tester avec des paramètres plus simples")

if __name__ == "__main__":
    main()
