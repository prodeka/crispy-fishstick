#!/usr/bin/env python3
"""
Script pour harmoniser précisément les contraintes hydrauliques entre EPANET et LCPI.
Objectif : Éliminer les différences de contraintes qui pourraient expliquer les écarts.
"""

import sys
import json
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Any

def analyze_constraint_definitions():
    """Analyse les définitions de contraintes dans les deux solveurs."""
    
    print("🔍 ANALYSE DES DÉFINITIONS DE CONTRAINTES")
    print("=" * 60)
    
    # Fichiers à analyser pour les contraintes
    constraint_files = [
        "src/lcpi/aep/optimizer/constraints_handler.py",
        "src/lcpi/aep/optimization/genetic_algorithm.py",
        "src/lcpi/aep/optimizer/controllers.py"
    ]
    
    print("\n📊 CONTRAINTES IDENTIFIÉES:")
    
    for file_path in constraint_files:
        if Path(file_path).exists():
            print(f"\n📁 {file_path}:")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Chercher les contraintes de pression
            if "pression_min" in content or "pressure_min" in content:
                print("   📏 Contraintes de pression: Détectées")
                
            if "vitesse_max" in content or "velocity_max" in content:
                print("   🏃 Contraintes de vitesse: Détectées")
                
            if "vitesse_min" in content or "velocity_min" in content:
                print("   🐌 Contraintes de vitesse min: Détectées")
                
            # Chercher les valeurs par défaut
            if "pressure_default_min" in content:
                print("   💡 Valeur par défaut pression: Définie")
                
            if "velocity_max_default" in content:
                print("   💡 Valeur par défaut vitesse max: Définie")

def _resolve_input_file() -> Path:
    """Résout un fichier INP existant à utiliser pour les tests."""
    candidates = [
        Path("bismark_inp.inp"),
        Path("examples") / "bismark-Administrator.inp",
        Path("examples") / "bismark-Administrator.inp.backup",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return Path("bismark_inp.inp")


def _find_result_json(basename: str) -> Path | None:
    """Trouve le fichier JSON de résultat attendu.

    Essaye à la racine puis dans le dossier `results/` avec variantes.
    """
    direct = Path(f"{basename}.json")
    if direct.exists():
        return direct
    # Cherche dans results/ exact
    results_dir = Path("results")
    if results_dir.exists():
        candidate = results_dir / f"{basename}.json"
        if candidate.exists():
            return candidate
        # Cherche fichiers qui commencent par basename (ex: basename_timestamp.json)
        matches = list(results_dir.glob(f"{basename}*.json"))
        if matches:
            # Prend le plus récent
            matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            return matches[0]
    return None


def _run_cmd(cmd: list[str], label: str) -> tuple[bool, str, str]:
    """Exécute une commande avec timeout et retourne (ok, stdout, stderr)."""
    try:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        completed = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env,
            timeout=300,
        )
        ok = completed.returncode == 0
        if not ok:
            print(f"   ❌ {label} a retourné le code {completed.returncode}")
        return ok, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as e:
        print(f"   ⏱️ Timeout pendant {label} (>{e.timeout}s)")
        return False, e.stdout or "", e.stderr or ""


def test_constraint_harmonization():
    """Teste l'harmonisation des contraintes."""
    
    print("\n🧪 TEST D'HARMONISATION DES CONTRAINTES")
    print("=" * 60)
    
    input_path = _resolve_input_file()
    if not input_path.exists():
        print(f"❌ Aucun fichier INP trouvé parmi les candidats. Essayé: bismark_inp.inp, examples/bismark-Administrator.inp(.backup)")
        return
    else:
        print(f"   📄 Fichier INP utilisé: {input_path}")
    
    # Configurations de contraintes à tester
    constraint_configs = [
        {
            "name": "Contraintes Standard",
            "pressure_min": 15.0,
            "velocity_max": 2.0,
            "velocity_min": 0.5
        },
        {
            "name": "Contraintes Strictes",
            "pressure_min": 20.0,
            "velocity_max": 1.5,
            "velocity_min": 0.8
        },
        {
            "name": "Contraintes Souples",
            "pressure_min": 10.0,
            "velocity_max": 3.0,
            "velocity_min": 0.3
        },
        {
            "name": "Contraintes EPANET-like",
            "pressure_min": 18.0,
            "velocity_max": 2.5,
            "velocity_min": 0.6
        }
    ]
    
    results = []
    
    for config in constraint_configs:
        print(f"\n🎯 Test: {config['name']}")
        print(f"   Pression min: {config['pressure_min']} m")
        print(f"   Vitesse max: {config['velocity_max']} m/s")
        print(f"   Vitesse min: {config['velocity_min']} m/s")
        
        # Test avec EPANET
        epanet_output = f"epanet_constraints_{config['pressure_min']}_{config['velocity_max']}"
        epanet_cmd = [
            sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
            str(input_path),
            "--method", "genetic",
            "--generations", "15",
            "--population", "25",
            "--solver", "epanet",
            "--pression-min", str(config['pressure_min']),
            "--vitesse-max", str(config['velocity_max']),
            "--vitesse-min", str(config['velocity_min']),
            "--show-stats",
            "--output", epanet_output,
            "--no-log"
        ]
        
        # Test avec LCPI
        lcpi_output = f"lcpi_constraints_{config['pressure_min']}_{config['velocity_max']}"
        lcpi_cmd = [
            sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
            str(input_path),
            "--method", "genetic",
            "--generations", "15",
            "--population", "25",
            "--solver", "lcpi",
            "--pression-min", str(config['pressure_min']),
            "--vitesse-max", str(config['velocity_max']),
            "--vitesse-min", str(config['velocity_min']),
            "--show-stats",
            "--output", lcpi_output,
            "--no-log"
        ]
        
        try:
            print("   🔄 Exécution EPANET...")
            ok1, out1, err1 = _run_cmd(epanet_cmd, "EPANET")
            if not ok1:
                print("   ├─ stdout (EPANET):\n" + (out1[-2000:] if out1 else ""))
                print("   └─ stderr (EPANET):\n" + (err1[-2000:] if err1 else ""))
            
            print("   🔄 Exécution LCPI...")
            ok2, out2, err2 = _run_cmd(lcpi_cmd, "LCPI")
            if not ok2:
                print("   ├─ stdout (LCPI):\n" + (out2[-2000:] if out2 else ""))
                print("   └─ stderr (LCPI):\n" + (err2[-2000:] if err2 else ""))
            
            # Analyser les résultats
            epanet_file = _find_result_json(epanet_output)
            lcpi_file = _find_result_json(lcpi_output)
            
            if epanet_file and lcpi_file and epanet_file.exists() and lcpi_file.exists():
                # Charger les résultats EPANET
                with open(epanet_file, 'r', encoding='utf-8') as f:
                    epanet_data = json.load(f)
                
                # Charger les résultats LCPI
                with open(lcpi_file, 'r', encoding='utf-8') as f:
                    lcpi_data = json.load(f)
                
                epanet_props = epanet_data.get("proposals", [])
                lcpi_props = lcpi_data.get("proposals", [])
                
                if epanet_props and lcpi_props:
                    epanet_best = epanet_props[0]
                    lcpi_best = lcpi_props[0]
                    
                    epanet_cost = epanet_best.get("CAPEX", 0)
                    lcpi_cost = lcpi_best.get("CAPEX", 0)
                    epanet_feasible = epanet_best.get("constraints_ok", False)
                    lcpi_feasible = lcpi_best.get("constraints_ok", False)
                    
                    print(f"   💰 EPANET: {epanet_cost:,.0f} FCFA ({'✅' if epanet_feasible else '❌'})")
                    print(f"   💰 LCPI  : {lcpi_cost:,.0f} FCFA ({'✅' if lcpi_feasible else '❌'})")
                    
                    if epanet_cost > 0:
                        delta = lcpi_cost - epanet_cost
                        delta_percent = (delta / epanet_cost) * 100
                        print(f"   📊 Différence: {delta:+,.0f} FCFA ({delta_percent:+.1f}%)")
                    
                    results.append({
                        "config": config,
                        "epanet": {"cost": epanet_cost, "feasible": epanet_feasible},
                        "lcpi": {"cost": lcpi_cost, "feasible": lcpi_feasible}
                    })
                else:
                    print("   ❌ Aucune proposition trouvée dans les JSON")
            else:
                print("   ❌ Fichiers de résultats manquants")
                print(f"      - Cherché: {epanet_output}.json et {lcpi_output}.json")
                print(f"      - Essai dossiers: ./ et ./results/")
                
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erreur d'exécution: {e}")
        except Exception as e:  # Sécurité pour voir les erreurs inattendues
            print(f"   ❌ Exception inattendue: {e}")
    
    return results

def analyze_constraint_impact(results: List[Dict[str, Any]]):
    """Analyse l'impact des contraintes sur les résultats."""
    
    print("\n📊 ANALYSE DE L'IMPACT DES CONTRAINTES")
    print("=" * 60)
    
    if not results:
        print("❌ Aucun résultat à analyser")
        return
    
    print("\n📈 COMPARAISON PAR CONFIGURATION:")
    
    for i, result in enumerate(results):
        config = result["config"]
        epanet = result["epanet"]
        lcpi = result["lcpi"]
        
        print(f"\n{i+1}. {config['name']}:")
        print(f"   📏 Pression min: {config['pressure_min']} m")
        print(f"   🏃 Vitesse max: {config['velocity_max']} m/s")
        print(f"   💰 EPANET: {epanet['cost']:,.0f} FCFA ({'✅' if epanet['feasible'] else '❌'})")
        print(f"   💰 LCPI  : {lcpi['cost']:,.0f} FCFA ({'✅' if lcpi['feasible'] else '❌'})")
        
        if epanet['cost'] > 0:
            delta = lcpi['cost'] - epanet['cost']
            delta_percent = (delta / epanet['cost']) * 100
            print(f"   📊 Écart: {delta:+,.0f} FCFA ({delta_percent:+.1f}%)")
    
    # Analyser les tendances
    print(f"\n📊 TENDANCES GLOBALES:")
    
    feasible_pairs = [r for r in results if r["epanet"]["feasible"] and r["lcpi"]["feasible"]]
    infeasible_pairs = [r for r in results if not r["epanet"]["feasible"] or not r["lcpi"]["feasible"]]
    
    print(f"   Paires faisables: {len(feasible_pairs)}/{len(results)}")
    print(f"   Paires avec infaisabilité: {len(infeasible_pairs)}/{len(results)}")
    
    if feasible_pairs:
        avg_delta_feasible = sum(
            (r["lcpi"]["cost"] - r["epanet"]["cost"]) / r["epanet"]["cost"] * 100 
            for r in feasible_pairs if r["epanet"]["cost"] > 0
        ) / len(feasible_pairs)
        print(f"   📊 Écart moyen (faisable): {avg_delta_feasible:+.1f}%")

def generate_harmonization_recommendations():
    """Génère des recommandations d'harmonisation."""
    
    print("\n💡 RECOMMANDATIONS D'HARMONISATION")
    print("=" * 60)
    
    recommendations = [
        {
            "category": "Contraintes de Pression",
            "items": [
                "Utiliser la même valeur de pression minimale pour les deux solveurs",
                "Vérifier que les unités sont cohérentes (m vs mCE)",
                "Implémenter des contraintes de pression par nœud si nécessaire"
            ]
        },
        {
            "category": "Contraintes de Vitesse",
            "items": [
                "Harmoniser les seuils de vitesse maximale et minimale",
                "Vérifier la cohérence des unités (m/s)",
                "Implémenter des contraintes de vitesse par conduite"
            ]
        },
        {
            "category": "Application des Contraintes",
            "items": [
                "Utiliser le même mode d'application (soft vs hard)",
                "Harmoniser les poids de pénalité",
                "Implémenter la même logique de tolérance"
            ]
        },
        {
            "category": "Validation des Résultats",
            "items": [
                "Vérifier que les contraintes sont bien respectées",
                "Comparer les métriques hydrauliques détaillées",
                "Analyser les violations de contraintes"
            ]
        }
    ]
    
    for rec in recommendations:
        print(f"\n📋 {rec['category']}:")
        for item in rec['items']:
            print(f"   • {item}")

def main():
    """Fonction principale."""
    
    print("🔧 HARMONISATION DES CONTRAINTES HYDRAULIQUES")
    print("=" * 80)
    print("Objectif: Éliminer les différences de contraintes entre EPANET et LCPI")
    
    # 1. Analyser les définitions actuelles
    analyze_constraint_definitions()
    
    # 2. Tester l'harmonisation
    results = test_constraint_harmonization()
    
    # 3. Analyser l'impact
    analyze_constraint_impact(results)
    
    # 4. Générer les recommandations
    generate_harmonization_recommendations()
    
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("1. Implémenter les recommandations d'harmonisation")
    print("2. Tester avec des contraintes parfaitement alignées")
    print("3. Valider la cohérence des résultats")
    print("4. Documenter les contraintes harmonisées")

if __name__ == "__main__":
    main()
