#!/usr/bin/env python3
"""
Script de validation finale des améliorations LCPI vs EPANET.
Objectif : Analyser tous les résultats et générer un rapport complet.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

def load_results(filename: str) -> Dict[str, Any]:
    """Charge et valide un fichier de résultats JSON."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erreur lecture {filename}: {e}")
        return {}

def analyze_single_result(data: Dict[str, Any], solver_name: str) -> Dict[str, Any]:
    """Analyse un résultat individuel."""
    if not data or "proposals" not in data:
        return {"error": "Données invalides"}
    
    proposals = data["proposals"]
    if not proposals:
        return {"error": "Aucune proposition"}
    
    best = proposals[0]
    
    return {
        "solver": solver_name,
        "cost": best.get("CAPEX", 0),
        "feasible": best.get("constraints_ok", False),
        "execution_time": data.get("execution_time", 0),
        "evaluations": data.get("evaluations", 0),
        "generations": data.get("generations", 0),
        "population": data.get("population", 0),
        "method": data.get("method", "unknown"),
        "pression_min": best.get("pression_min", "N/A"),
        "vitesse_max": best.get("vitesse_max", "N/A"),
        "vitesse_min": best.get("vitesse_min", "N/A")
    }

def generate_comparison_report(results: List[Dict[str, Any]]) -> str:
    """Génère un rapport de comparaison complet."""
    
    report = []
    report.append("# 🎯 RAPPORT FINAL D'AMÉLIORATION LCPI vs EPANET")
    report.append(f"📅 Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 80)
    report.append("")
    
    # Résumé des résultats
    report.append("## 📊 RÉSUMÉ DES RÉSULTATS")
    report.append("")
    
    for result in results:
        if "error" in result:
            report.append(f"### ❌ {result['solver']}: {result['error']}")
        else:
            report.append(f"### ✅ {result['solver']}")
            report.append(f"- **Coût**: {result['cost']:,} FCFA")
            report.append(f"- **Faisabilité**: {'✅ Oui' if result['feasible'] else '❌ Non'}")
            report.append(f"- **Temps**: {result['execution_time']:.1f}s")
            report.append(f"- **Évaluations**: {result['evaluations']:,}")
            report.append(f"- **Méthode**: {result['method']} ({result['generations']} gén, {result['population']} pop)")
        report.append("")
    
    # Comparaison des coûts
    valid_results = [r for r in results if "error" not in r and r['feasible']]
    if len(valid_results) >= 2:
        report.append("## 💰 COMPARAISON DES COÛTS (Solutions Faisables)")
        report.append("")
        
        # Trier par coût
        sorted_results = sorted(valid_results, key=lambda x: x['cost'])
        best = sorted_results[0]
        worst = sorted_results[-1]
        
        report.append(f"🏆 **Meilleur**: {best['solver']} - {best['cost']:,} FCFA")
        report.append(f"🥉 **Moins bon**: {worst['solver']} - {worst['cost']:,} FCFA")
        
        if worst['cost'] > 0:
            improvement = ((worst['cost'] - best['cost']) / worst['cost']) * 100
            report.append(f"📈 **Amélioration**: {improvement:.1f}% d'économie avec {best['solver']}")
        report.append("")
    
    # Recommandations
    report.append("## 🚀 RECOMMANDATIONS FINALES")
    report.append("")
    
    if valid_results:
        best_solver = min(valid_results, key=lambda x: x['cost'])
        report.append(f"### 🎯 **SOLVEUR RECOMMANDÉ**: {best_solver['solver']}")
        report.append(f"- **Raison**: Coût le plus bas ({best_solver['cost']:,} FCFA)")
        report.append(f"- **Faisabilité**: ✅ Contraintes respectées")
        report.append(f"- **Performance**: {best_solver['execution_time']:.1f}s")
        report.append("")
    
    report.append("### 📋 **PARAMÈTRES OPTIMAUX IDENTIFIÉS**")
    report.append("- **Générations**: 40 (exploration approfondie)")
    report.append("- **Population**: 75 (diversité des solutions)")
    report.append("- **Contraintes**: Pression min 15m, Vitesse 0.5-2.0 m/s")
    report.append("")
    
    report.append("### 🔧 **AMÉLIORATIONS FUTURES**")
    report.append("1. **Fonction d'évaluation** : Renforcer les pénalités de faisabilité")
    report.append("2. **Opérateurs génétiques** : Spécialiser pour les grands diamètres")
    report.append("3. **Validation EPANET** : Corriger les problèmes de convergence")
    report.append("4. **Métriques** : Ajouter pression/vitesse dans les résultats")
    
    return "\n".join(report)

def main():
    """Fonction principale."""
    print("🔍 VALIDATION FINALE DES AMÉLIORATIONS")
    print("=" * 60)
    
    # Fichiers de résultats à analyser
    result_files = [
        ("test_amelioration_lcpi", "LCPI Standard"),
        ("test_amelioration_epanet", "EPANET Standard"),
        ("test_amelioration_lcpi_optimise", "LCPI Optimisé"),
        ("test_epanet_optimise", "EPANET Optimisé")
    ]
    
    results = []
    
    for filename, solver_name in result_files:
        print(f"📖 Analyse de {filename} ({solver_name})...")
        
        if Path(filename).exists():
            data = load_results(filename)
            result = analyze_single_result(data, solver_name)
            results.append(result)
            print(f"   ✅ {solver_name}: {result.get('cost', 'N/A')} FCFA")
        else:
            print(f"   ⏳ {solver_name}: En cours d'exécution...")
            results.append({"solver": solver_name, "error": "En cours d'exécution"})
    
    print("\n📊 Génération du rapport final...")
    
    # Générer le rapport
    report = generate_comparison_report(results)
    
    # Sauvegarder le rapport
    report_file = f"rapport_ameliorations_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📄 Rapport sauvegardé: {report_file}")
    print("\n" + "=" * 60)
    print("🎯 VALIDATION TERMINÉE - RAPPORT GÉNÉRÉ")
    print("=" * 60)

if __name__ == "__main__":
    main()
