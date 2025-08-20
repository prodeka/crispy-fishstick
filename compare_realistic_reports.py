#!/usr/bin/env python3
"""
Script pour comparer les rapports avec les données réalistes
"""

import json
from pathlib import Path

def compare_realistic_data():
    """Compare les données réalistes entre EPANET et LCPI"""
    
    print("🔍 Comparaison des données réalistes")
    print("=" * 60)
    
    # Charger les données
    epanet_file = "results/out_multi_epanet_realistic.json"
    lcpi_file = "results/out_multi_lcpi_realistic.json"
    
    with open(epanet_file, 'r') as f:
        epanet_data = json.load(f)
    with open(lcpi_file, 'r') as f:
        lcpi_data = json.load(f)
    
    epanet_best = epanet_data["best_proposal"]
    lcpi_best = lcpi_data["best_proposal"]
    
    print("📊 Comparaison des meilleures propositions:")
    print(f"{'Métrique':<25} {'EPANET':<15} {'LCPI':<15} {'Différence':<15}")
    print("-" * 70)
    
    metrics = [
        ("CAPEX (€)", "CAPEX", "{:,.0f}"),
        ("Pression min (m)", "min_pressure_m", "{:.3f}"),
        ("Pression max (m)", "max_pressure_m", "{:.3f}"),
        ("Vitesse max (m/s)", "max_velocity_ms", "{:.2f}"),
        ("Score efficacité", "efficiency_score", "{:.3f}"),
        ("Optimisation diamètre", "diameter_optimization", "{:.3f}"),
        ("Distribution pression", "pressure_distribution", "{:.3f}"),
        ("Distribution vitesse", "velocity_distribution", "{:.3f}")
    ]
    
    for label, key, fmt in metrics:
        epanet_val = epanet_best.get(key, 0)
        lcpi_val = lcpi_best.get(key, 0)
        diff = lcpi_val - epanet_val
        
        if key == "CAPEX":
            diff_pct = (diff / epanet_val) * 100 if epanet_val != 0 else 0
            diff_str = f"{diff:+,.0f} ({diff_pct:+.1f}%)"
        else:
            diff_str = f"{diff:+.3f}"
        
        print(f"{label:<25} {fmt.format(epanet_val):<15} {fmt.format(lcpi_val):<15} {diff_str:<15}")
    
    print("\n🎯 Analyse des différences:")
    
    # CAPEX
    capex_diff = lcpi_best['CAPEX'] - epanet_best['CAPEX']
    capex_diff_pct = (capex_diff / epanet_best['CAPEX']) * 100
    print(f"💰 CAPEX: LCPI est {abs(capex_diff_pct):.1f}% {'moins cher' if capex_diff < 0 else 'plus cher'} que EPANET")
    
    # Pression
    pressure_diff = lcpi_best['min_pressure_m'] - epanet_best['min_pressure_m']
    print(f"💧 Pression: LCPI a {pressure_diff:+.3f} m de pression supplémentaire")
    
    # Efficacité
    efficiency_diff = lcpi_best['efficiency_score'] - epanet_best['efficiency_score']
    print(f"⚡ Efficacité: LCPI a un score {efficiency_diff:+.3f} plus élevé")
    
    return True

def analyze_report_content():
    """Analyse le contenu du rapport généré"""
    
    print("\n📄 Analyse du rapport généré")
    print("=" * 60)
    
    report_file = "results/test_multi_solver_report_realistic.html"
    
    if not Path(report_file).exists():
        print(f"❌ Rapport non trouvé: {report_file}")
        return False
    
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📊 Taille du rapport: {len(content):,} caractères")
    
    # Vérifier les éléments clés
    key_elements = [
        ("Comparaison Multi-Solveurs", "Titre principal"),
        ("Vue d'ensemble", "Section vue d'ensemble"),
        ("Comparaison détaillée", "Section comparaison"),
        ("EPANET", "Référence EPANET"),
        ("LCPI", "Référence LCPI"),
        ("1,264,763.94", "CAPEX EPANET"),
        ("1,107,017.5", "CAPEX LCPI"),
        ("-157,746", "Différence CAPEX"),
        ("-12.5%", "Différence pourcentage")
    ]
    
    print("\n🔍 Vérification des éléments clés:")
    for element, description in key_elements:
        if element in content:
            print(f"  ✅ {description}: trouvé")
        else:
            print(f"  ❌ {description}: manquant")
    
    # Compter les occurrences
    epanet_count = content.count("EPANET")
    lcpi_count = content.count("LCPI")
    
    print(f"\n📈 Occurrences:")
    print(f"  EPANET: {epanet_count} fois")
    print(f"  LCPI: {lcpi_count} fois")
    
    return True

def create_summary_report():
    """Crée un rapport de synthèse"""
    
    print("\n📋 Rapport de synthèse")
    print("=" * 60)
    
    # Charger les données
    with open("results/out_multi_epanet_realistic.json", 'r') as f:
        epanet_data = json.load(f)
    with open("results/out_multi_lcpi_realistic.json", 'r') as f:
        lcpi_data = json.load(f)
    
    epanet_best = epanet_data["best_proposal"]
    lcpi_best = lcpi_data["best_proposal"]
    
    summary = f"""
# Rapport de Synthèse - Comparaison Multi-Solveurs

## Résumé Exécutif

**Projet**: Bismark Administrator Network
**Fichier d'entrée**: src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp
**Méthode d'optimisation**: Algorithme génétique
**Date d'analyse**: {epanet_data['meta']['generation_date'][:10]}

## Résultats Principaux

### 🏆 Meilleure Solution: LCPI

| Critère | EPANET | LCPI | Différence |
|---------|--------|------|------------|
| **CAPEX** | {epanet_best['CAPEX']:,.0f} € | {lcpi_best['CAPEX']:,.0f} € | {lcpi_best['CAPEX'] - epanet_best['CAPEX']:+,.0f} € ({(lcpi_best['CAPEX'] - epanet_best['CAPEX']) / epanet_best['CAPEX'] * 100:+.1f}%) |
| **Pression min** | {epanet_best['min_pressure_m']:.3f} m | {lcpi_best['min_pressure_m']:.3f} m | {lcpi_best['min_pressure_m'] - epanet_best['min_pressure_m']:+.3f} m |
| **Vitesse max** | {epanet_best['max_velocity_ms']:.2f} m/s | {lcpi_best['max_velocity_ms']:.2f} m/s | {lcpi_best['max_velocity_ms'] - epanet_best['max_velocity_ms']:+.2f} m/s |
| **Score efficacité** | {epanet_best['efficiency_score']:.3f} | {lcpi_best['efficiency_score']:.3f} | {lcpi_best['efficiency_score'] - epanet_best['efficiency_score']:+.3f} |

## Recommandations

✅ **LCPI est recommandé** pour ce projet car il offre:
- Une économie de {abs(lcpi_best['CAPEX'] - epanet_best['CAPEX']):,.0f} € ({(lcpi_best['CAPEX'] - epanet_best['CAPEX']) / epanet_best['CAPEX'] * 100:.1f}% d'économie)
- Une meilleure pression minimale (+{lcpi_best['min_pressure_m'] - epanet_best['min_pressure_m']:.3f} m)
- Un score d'efficacité supérieur (+{lcpi_best['efficiency_score'] - epanet_best['efficiency_score']:.3f})

## Métriques Techniques

### EPANET
- Modèle de perte de charge: {epanet_best.get('epanet_specific', {}).get('headloss_model', 'N/A')}
- Itérations de convergence: {epanet_best.get('epanet_specific', {}).get('convergence_iterations', 'N/A')}
- Précision hydraulique: {epanet_best.get('epanet_specific', {}).get('hydraulic_accuracy', 'N/A')}

### LCPI
- Algorithme d'optimisation: {lcpi_best.get('lcpi_specific', {}).get('optimization_algorithm', 'N/A')}
- Générations: {lcpi_best.get('lcpi_specific', {}).get('generations', 'N/A')}
- Taille de population: {lcpi_best.get('lcpi_specific', {}).get('population_size', 'N/A')}
- Taux de mutation: {lcpi_best.get('lcpi_specific', {}).get('mutation_rate', 'N/A')}
- Taux de croisement: {lcpi_best.get('lcpi_specific', {}).get('crossover_rate', 'N/A')}

## Conclusion

L'analyse multi-solveurs démontre clairement l'avantage de LCPI pour ce projet spécifique. 
L'économie significative de {abs(lcpi_best['CAPEX'] - epanet_best['CAPEX']):,.0f} € 
justifie l'utilisation de LCPI malgré les différences algorithmiques.
"""
    
    # Sauvegarder le rapport
    summary_file = "results/summary_report_realistic.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✅ Rapport de synthèse créé: {summary_file}")
    print(f"📄 Taille: {len(summary)} caractères")
    
    return True

def main():
    """Fonction principale"""
    print("🔍 Analyse complète des données réalistes")
    print("=" * 80)
    
    # 1. Comparer les données
    compare_realistic_data()
    
    # 2. Analyser le rapport
    analyze_report_content()
    
    # 3. Créer un rapport de synthèse
    create_summary_report()
    
    print("\n" + "=" * 80)
    print("🎉 Analyse terminée avec succès!")
    print("📁 Fichiers générés:")
    print("  - results/test_multi_solver_report_realistic.html")
    print("  - results/summary_report_realistic.md")
    print("\n🌐 Ouvrir le rapport HTML pour voir la comparaison visuelle")

if __name__ == "__main__":
    main()
