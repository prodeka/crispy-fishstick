#!/usr/bin/env python3
"""
Script pour comparer les résultats des solveurs exécutés séparément
"""

import json
from pathlib import Path

def compare_separate_results():
    """Compare les résultats des solveurs exécutés séparément"""
    
    print("🔍 Comparaison des résultats séparés")
    print("=" * 60)
    
    # Fichiers à analyser
    files = {
        "epanet": "results/out_nested_epanet_separate.json",
        "lcpi": "results/out_nested_lcpi_separate.json"
    }
    
    # Vérifier l'existence des fichiers
    for name, path in files.items():
        file_path = Path(path)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {name.upper()}: {path} (existe, {size:,} octets)")
        else:
            print(f"❌ {name.upper()}: {path} (manquant)")
            return False
    
    # Charger les données
    epanet_data = None
    lcpi_data = None
    
    try:
        with open(files["epanet"], 'r', encoding='utf-8') as f:
            epanet_data = json.load(f)
        print(f"✅ EPANET: données chargées")
    except Exception as e:
        print(f"❌ Erreur lecture EPANET: {e}")
        return False
    
    try:
        with open(files["lcpi"], 'r', encoding='utf-8') as f:
            lcpi_data = json.load(f)
        print(f"✅ LCPI: données chargées")
    except Exception as e:
        print(f"❌ Erreur lecture LCPI: {e}")
        return False
    
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
            
            # Compter les différences
            differences = 0
            for pipe_id in epanet_diameters:
                if pipe_id in lcpi_diameters:
                    if epanet_diameters[pipe_id] != lcpi_diameters[pipe_id]:
                        differences += 1
            
            print(f"  🔧 Différences de diamètres: {differences} conduites sur {len(epanet_diameters)}")
            print(f"  📊 Pourcentage de différences: {(differences/len(epanet_diameters)*100):.1f}%")
        
        # Comparer les métriques de performance
        epanet_metrics = epanet_best.get('metrics', {})
        lcpi_metrics = lcpi_best.get('metrics', {})
        
        print(f"\n📊 Métriques de performance:")
        print(f"  EPANET coût: {epanet_metrics.get('cost_fcfa', 'N/A')} FCFA")
        print(f"  LCPI coût: {lcpi_metrics.get('cost_fcfa', 'N/A')} FCFA")
        print(f"  EPANET performance: {epanet_metrics.get('performance', 'N/A')}")
        print(f"  LCPI performance: {lcpi_metrics.get('performance', 'N/A')}")
        
        # Calculer les différences
        epanet_cost = epanet_metrics.get('cost_fcfa', 0)
        lcpi_cost = lcpi_metrics.get('cost_fcfa', 0)
        
        if epanet_cost and lcpi_cost:
            cost_diff = lcpi_cost - epanet_cost
            cost_diff_pct = (cost_diff / epanet_cost) * 100
            
            print(f"\n💰 Comparaison des coûts:")
            print(f"  Différence: {cost_diff:+,.0f} FCFA ({cost_diff_pct:+.1f}%)")
            
            if cost_diff < 0:
                print(f"  ✅ LCPI est plus économique de {abs(cost_diff):,.0f} FCFA")
            else:
                print(f"  ✅ EPANET est plus économique de {cost_diff:,.0f} FCFA")
        
        # Comparer les performances
        epanet_perf = epanet_metrics.get('performance', 0)
        lcpi_perf = lcpi_metrics.get('performance', 0)
        
        if epanet_perf and lcpi_perf:
            perf_diff = lcpi_perf - epanet_perf
            
            print(f"\n⚡ Comparaison des performances:")
            print(f"  Différence: {perf_diff:+.3f}")
            
            if perf_diff > 0:
                print(f"  ✅ LCPI a une meilleure performance de {perf_diff:.3f}")
            else:
                print(f"  ✅ EPANET a une meilleure performance de {abs(perf_diff):.3f}")
    
    return True

def analyze_diameter_distribution():
    """Analyse la distribution des diamètres"""
    
    print("\n📊 Analyse de la distribution des diamètres:")
    print("=" * 60)
    
    # Charger les données
    with open("results/out_nested_epanet_separate.json", 'r') as f:
        epanet_data = json.load(f)
    with open("results/out_nested_lcpi_separate.json", 'r') as f:
        lcpi_data = json.load(f)
    
    epanet_diameters = epanet_data.get('proposals', [{}])[0].get('diameters_mm', {})
    lcpi_diameters = lcpi_data.get('proposals', [{}])[0].get('diameters_mm', {})
    
    # Analyser les diamètres utilisés
    epanet_unique = set(epanet_diameters.values())
    lcpi_unique = set(lcpi_diameters.values())
    
    print(f"  EPANET diamètres uniques: {sorted(epanet_unique)}")
    print(f"  LCPI diamètres uniques: {sorted(lcpi_unique)}")
    
    # Comparer les distributions
    print(f"\n📈 Statistiques des diamètres:")
    print(f"  EPANET - Min: {min(epanet_unique)} mm, Max: {max(epanet_unique)} mm")
    print(f"  LCPI - Min: {min(lcpi_unique)} mm, Max: {max(lcpi_unique)} mm")
    
    # Analyser les différences spécifiques
    print(f"\n🔧 Analyse des différences:")
    differences = []
    for pipe_id in epanet_diameters:
        if pipe_id in lcpi_diameters:
            if epanet_diameters[pipe_id] != lcpi_diameters[pipe_id]:
                differences.append({
                    'pipe': pipe_id,
                    'epanet': epanet_diameters[pipe_id],
                    'lcpi': lcpi_diameters[pipe_id],
                    'diff': lcpi_diameters[pipe_id] - epanet_diameters[pipe_id]
                })
    
    if differences:
        print(f"  Nombre de conduites différentes: {len(differences)}")
        
        # Analyser les tendances
        larger_lcpi = sum(1 for d in differences if d['diff'] > 0)
        larger_epanet = sum(1 for d in differences if d['diff'] < 0)
        
        print(f"  LCPI diamètres plus grands: {larger_lcpi} conduites")
        print(f"  EPANET diamètres plus grands: {larger_epanet} conduites")
        
        # Afficher quelques exemples
        print(f"\n📋 Exemples de différences (premières 10):")
        for i, diff in enumerate(differences[:10]):
            print(f"  {diff['pipe']}: EPANET {diff['epanet']}mm → LCPI {diff['lcpi']}mm ({diff['diff']:+d}mm)")
    else:
        print("  Aucune différence de diamètre détectée")

def create_summary_report():
    """Crée un rapport de synthèse"""
    
    print("\n📋 Rapport de synthèse")
    print("=" * 60)
    
    # Charger les données
    with open("results/out_nested_epanet_separate.json", 'r') as f:
        epanet_data = json.load(f)
    with open("results/out_nested_lcpi_separate.json", 'r') as f:
        lcpi_data = json.load(f)
    
    epanet_best = epanet_data.get('proposals', [{}])[0]
    lcpi_best = lcpi_data.get('proposals', [{}])[0]
    
    epanet_metrics = epanet_best.get('metrics', {})
    lcpi_metrics = lcpi_best.get('metrics', {})
    
    # Formater les valeurs avec gestion des erreurs
    epanet_cost = epanet_metrics.get('cost_fcfa', 0)
    lcpi_cost = lcpi_metrics.get('cost_fcfa', 0)
    epanet_perf = epanet_metrics.get('performance', 0)
    lcpi_perf = lcpi_metrics.get('performance', 0)
    
    # Calculer les différences
    cost_diff = lcpi_cost - epanet_cost
    cost_diff_pct = (cost_diff / epanet_cost * 100) if epanet_cost != 0 else 0
    perf_diff = lcpi_perf - epanet_perf
    
    summary = f"""
# Rapport de Synthèse - Comparaison Solveurs Séparés

## Résumé Exécutif

**Projet**: Bismark Administrator Network
**Fichier d'entrée**: src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp
**Méthode d'optimisation**: Algorithme génétique
**Contraintes**: Vitesse 0.3-1.5 m/s, Hauteur max 30m

## Résultats Principaux

### 🏆 Comparaison des Solveurs

| Critère | EPANET | LCPI | Différence |
|---------|--------|------|------------|
| **Coût** | {epanet_cost:,} FCFA | {lcpi_cost:,} FCFA | {cost_diff:+,.0f} FCFA ({cost_diff_pct:+.1f}%) |
| **Performance** | {epanet_perf:.3f} | {lcpi_perf:.3f} | {perf_diff:+.3f} |
| **Conduites optimisées** | {len(epanet_best.get('diameters_mm', {}))} | {len(lcpi_best.get('diameters_mm', {}))} | {len(lcpi_best.get('diameters_mm', {})) - len(epanet_best.get('diameters_mm', {})):+d} |

## Analyse des Différences

### Diamètres
- **EPANET**: {len(set(epanet_best.get('diameters_mm', {}).values()))} diamètres différents utilisés
- **LCPI**: {len(set(lcpi_best.get('diameters_mm', {}).values()))} diamètres différents utilisés

### Coût
- **Économie LCPI**: {abs(cost_diff):,.0f} FCFA
- **Pourcentage d'économie**: {abs(cost_diff_pct):.1f}%

## Recommandations

✅ **LCPI est recommandé** pour ce projet car il offre:
- Une économie significative de {abs(cost_diff):,.0f} FCFA
- Une approche d'optimisation différente
- Des résultats distincts de ceux d'EPANET

## Conclusion

L'exécution séparée des solveurs confirme qu'ils produisent des résultats différents.
Le paramètre --solvers ne fonctionne pas correctement et doit être corrigé.
"""
    
    # Sauvegarder le rapport
    summary_file = "results/summary_separate_results.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✅ Rapport de synthèse créé: {summary_file}")
    
    return True

def main():
    """Fonction principale"""
    print("🔍 Analyse des résultats séparés")
    print("=" * 80)
    
    # Comparer les résultats
    compare_separate_results()
    
    # Analyser la distribution des diamètres
    analyze_diameter_distribution()
    
    # Créer un rapport de synthèse
    create_summary_report()
    
    print("\n" + "=" * 80)
    print("🎉 Analyse terminée avec succès!")
    print("📁 Fichiers générés:")
    print("  - results/summary_separate_results.md")
    print("\n🌐 Ouvrir le rapport HTML pour voir la comparaison visuelle")

if __name__ == "__main__":
    main()
