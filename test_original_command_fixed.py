#!/usr/bin/env python3
"""
Script pour tester la commande originale avec les données corrigées
"""

import subprocess
import json
import time
from pathlib import Path

def test_original_command():
    """Teste la commande originale avec les données corrigées"""
    
    print("🔧 Test de la commande originale avec données corrigées")
    print("=" * 70)
    
    # Commande originale
    original_cmd = [
        "lcpi", "aep", "network-optimize-unified",
        "src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp",
        "--method", "genetic",
        "--solvers", "epanet,lcpi",
        "--pression-min", "12",
        "--vitesse-max", "2.0",
        "--output", "results/out_multi_fixed.json",
        "--report", "html",
        "--no-log"
    ]
    
    print("🚀 Exécution de la commande originale:")
    print(f"   {' '.join(original_cmd)}")
    print()
    
    try:
        # Exécuter la commande
        start_time = time.time()
        result = subprocess.run(original_cmd, capture_output=True, text=True, timeout=600)
        execution_time = time.time() - start_time
        
        print(f"⏱️  Temps d'exécution: {execution_time:.1f} secondes")
        print(f"📊 Code de retour: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Commande exécutée avec succès")
            
            # Vérifier les fichiers générés
            output_files = [
                "results/out_multi_fixed.json",
                "results/out_multi_fixed.html"
            ]
            
            print("\n📁 Fichiers générés:")
            for file_path in output_files:
                if Path(file_path).exists():
                    size = Path(file_path).stat().st_size
                    print(f"  ✅ {file_path} ({size:,} octets)")
                else:
                    print(f"  ❌ {file_path} (manquant)")
            
            # Analyser le fichier JSON généré
            if Path("results/out_multi_fixed.json").exists():
                analyze_generated_file()
            
        else:
            print("❌ Commande échouée")
            print(f"   Erreur: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Commande interrompue (timeout)")
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")

def analyze_generated_file():
    """Analyse le fichier généré par la commande"""
    
    print("\n🔍 Analyse du fichier généré")
    print("=" * 50)
    
    try:
        with open("results/out_multi_fixed.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Type de données: {type(data)}")
        
        if isinstance(data, dict):
            if "meta" in data and "results" in data:
                print("✅ Structure multi-solveurs détectée")
                
                solvers = data.get("meta", {}).get("solvers", [])
                results = data.get("results", {})
                
                print(f"📋 Solveurs déclarés: {solvers}")
                print(f"📁 Fichiers référencés: {list(results.keys())}")
                
                # Vérifier les fichiers référencés
                for solver, file_path in results.items():
                    if Path(file_path).exists():
                        print(f"  ✅ {solver}: {file_path} (existe)")
                        
                        # Analyser le contenu
                        try:
                            with open(file_path, 'r') as f:
                                solver_data = json.load(f)
                            solver_used = solver_data.get("meta", {}).get("solver", "unknown")
                            print(f"     Solveur utilisé: {solver_used}")
                            
                            if "proposals" in solver_data:
                                best_proposal = solver_data["proposals"][0] if solver_data["proposals"] else {}
                                capex = best_proposal.get("CAPEX", "N/A")
                                print(f"     CAPEX: {capex}")
                        except Exception as e:
                            print(f"     ❌ Erreur lecture: {e}")
                    else:
                        print(f"  ❌ {solver}: {file_path} (manquant)")
            else:
                print("⚠️  Structure non reconnue")
                print(f"   Clés disponibles: {list(data.keys())}")
        else:
            print("⚠️  Format de données non attendu")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")

def create_comparison_with_realistic():
    """Compare les résultats générés avec nos données réalistes"""
    
    print("\n📊 Comparaison avec les données réalistes")
    print("=" * 50)
    
    # Vérifier si les fichiers existent
    realistic_files = [
        "results/out_multi_epanet_realistic.json",
        "results/out_multi_lcpi_realistic.json"
    ]
    
    generated_files = [
        "results/out_multi_fixed.json"
    ]
    
    print("📁 Fichiers réalistes:")
    for file_path in realistic_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"  ✅ {file_path} ({size:,} octets)")
        else:
            print(f"  ❌ {file_path} (manquant)")
    
    print("\n📁 Fichiers générés:")
    for file_path in generated_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"  ✅ {file_path} ({size:,} octets)")
        else:
            print(f"  ❌ {file_path} (manquant)")
    
    # Si les deux types de fichiers existent, faire une comparaison
    if all(Path(f).exists() for f in realistic_files) and Path("results/out_multi_fixed.json").exists():
        print("\n🔍 Comparaison des structures:")
        
        try:
            # Charger les données réalistes
            with open("results/out_multi_epanet_realistic.json", 'r') as f:
                epanet_realistic = json.load(f)
            with open("results/out_multi_lcpi_realistic.json", 'r') as f:
                lcpi_realistic = json.load(f)
            
            # Charger les données générées
            with open("results/out_multi_fixed.json", 'r') as f:
                generated_data = json.load(f)
            
            print(f"  Structure réaliste EPANET: {list(epanet_realistic.keys())}")
            print(f"  Structure réaliste LCPI: {list(lcpi_realistic.keys())}")
            print(f"  Structure générée: {list(generated_data.keys())}")
            
            # Comparer les CAPEX
            epanet_capex = epanet_realistic.get("best_proposal", {}).get("CAPEX", 0)
            lcpi_capex = lcpi_realistic.get("best_proposal", {}).get("CAPEX", 0)
            
            print(f"\n💰 Comparaison CAPEX:")
            print(f"  EPANET réaliste: {epanet_capex:,.0f} €")
            print(f"  LCPI réaliste: {lcpi_capex:,.0f} €")
            print(f"  Différence: {lcpi_capex - epanet_capex:+,.0f} € ({(lcpi_capex - epanet_capex) / epanet_capex * 100:+.1f}%)")
            
        except Exception as e:
            print(f"  ❌ Erreur lors de la comparaison: {e}")

def suggest_next_steps():
    """Suggère les prochaines étapes"""
    
    print("\n🎯 Prochaines étapes recommandées")
    print("=" * 50)
    
    print("1. 🔧 Si la commande fonctionne:")
    print("   - Vérifier que les solveurs produisent des résultats différents")
    print("   - Analyser les différences de performance")
    print("   - Documenter les avantages de chaque solveur")
    
    print("\n2. 🔧 Si la commande échoue:")
    print("   - Vérifier la documentation de la commande")
    print("   - Tester avec --solver au lieu de --solvers")
    print("   - Exécuter les solveurs séparément")
    
    print("\n3. 📊 Analyse des résultats:")
    print("   - Comparer les performances hydrauliques")
    print("   - Analyser les coûts d'investissement")
    print("   - Évaluer la robustesse des solutions")
    
    print("\n4. 📈 Améliorations futures:")
    print("   - Ajouter plus de métriques de comparaison")
    print("   - Intégrer des analyses de sensibilité")
    print("   - Développer des visualisations avancées")

def main():
    """Fonction principale"""
    print("🚀 Test de la commande originale avec correction")
    print("=" * 80)
    
    # Test de la commande originale
    test_original_command()
    
    # Analyse du fichier généré
    if Path("results/out_multi_fixed.json").exists():
        analyze_generated_file()
    
    # Comparaison avec les données réalistes
    create_comparison_with_realistic()
    
    # Suggestions
    suggest_next_steps()
    
    print("\n" + "=" * 80)
    print("✅ Test terminé!")
    print("📁 Vérifiez les fichiers dans le dossier results/")
    print("🌐 Ouvrez le rapport HTML pour voir les résultats")

if __name__ == "__main__":
    main()
