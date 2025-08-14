#!/usr/bin/env python3
"""Test complet Hardy-Cross avec rapport détaillé - Multiples configurations"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.calculations.hardy_cross_enhanced import hardy_cross_network_enhanced
import sys
sys.path.append('scripts')
from generate_paris_network import ParisNetworkGenerator

def test_hardy_cross_configuration(hardy_cross_data: dict, max_iterations: int, tolerance: float, config_name: str):
    """Test Hardy-Cross avec une configuration spécifique"""
    
    print(f"\n🔧 Configuration '{config_name}' - max_iterations={max_iterations}, tolerance={tolerance}")
    print("-" * 60)
    
    hc_start_time = time.time()
    
    hardy_cross_results = hardy_cross_network_enhanced(
        hardy_cross_data, 
        max_iterations=max_iterations, 
        tolerance=tolerance
    )
    
    hc_time = time.time() - hc_start_time
    
    # Analyser les résultats
    iterations = hardy_cross_results.get('iterations', [])
    final_results = hardy_cross_results.get('final_results', {})
    flows = final_results.get('flows', {})
    convergence = hardy_cross_results.get('convergence', False)
    tolerance_finale = hardy_cross_results.get('tolerance_finale', 'N/A')
    
    print(f"   ⏱️  Temps : {hc_time:.3f}s")
    print(f"   🔄 Itérations : {len(iterations)}")
    print(f"   ✅ Convergence : {convergence}")
    print(f"   📊 Débits calculés : {len(flows)}")
    print(f"   🎯 Tolérance finale : {tolerance_finale}")
    
    if flows:
        flow_values = list(flows.values())
        print(f"   📈 Débit moyen : {sum(flow_values)/len(flow_values):.2f} L/s")
        print(f"   📉 Débit min : {min(flow_values):.2f} L/s")
        print(f"   📈 Débit max : {max(flow_values):.2f} L/s")
    
    return {
        'config_name': config_name,
        'max_iterations': max_iterations,
        'tolerance': tolerance,
        'time': hc_time,
        'iterations': len(iterations),
        'convergence': convergence,
        'tolerance_finale': tolerance_finale,
        'flows_count': len(flows),
        'results': hardy_cross_results
    }

def test_hardy_cross_complete():
    """Test complet Hardy-Cross avec multiples configurations"""
    
    print("🌊 Test complet Hardy-Cross - Réseau Paris Type - Multiples Configurations")
    print("=" * 80)
    
    # 1. Générer réseau
    print("\n📊 Génération du réseau...")
    start_time = time.time()
    
    generator = ParisNetworkGenerator()
    network_data = generator.generate_network_data()
    
    generation_time = time.time() - start_time
    print(f"✅ Réseau généré en {generation_time:.3f}s")
    print(f"   - Nœuds : {len(network_data['network']['nodes'])}")
    print(f"   - Conduites : {len(network_data['network']['pipes'])}")
    
    # 2. Convertir structure pour le calculateur Hardy-Cross
    print("\n🔄 Préparation des données pour le calculateur...")
    hardy_cross_troncons = []
    # On parcourt le dictionnaire de conduites pour préserver l'ID
    for pipe_id, pipe_data in network_data["network"]["pipes"].items():
        troncon = {
            # On s'assure que les clés attendues par le calculateur sont présentes
            "id": pipe_id,
            "noeud_amont": pipe_data.get("noeud_amont"), # ou from_node
            "noeud_aval": pipe_data.get("noeud_aval"),   # ou to_node
            "noeud_debut": pipe_data.get("noeud_amont"), # Assurer la compatibilité
            "noeud_fin": pipe_data.get("noeud_aval"),   # Assurer la compatibilité
            "longueur": pipe_data.get("longueur"),
            "diametre": pipe_data.get("diametre"),
            "coefficient_rugosite": pipe_data.get("coefficient_rugosite"),
            "debit_initial": pipe_data.get("debit_initial", 0.1) # IMPORTANT: Mettre un petit débit initial non-nul
        }
        hardy_cross_troncons.append(troncon)

    hardy_cross_data = {
        "metadata": network_data["metadata"],
        "troncons": hardy_cross_troncons, # Utiliser la liste correctement formatée
        "noeuds": list(network_data["network"]["nodes"].values())
    }
    print("✅ Données préparées.")
    
    # 3. Définir les configurations à tester
    configurations = [
        # Configuration rapide (baseline)
        {"name": "Rapide", "max_iterations": 200, "tolerance": 1e-3},
        
        # Configurations progressives
        {"name": "Standard", "max_iterations": 500, "tolerance": 1e-4},
        {"name": "Précision", "max_iterations": 1000, "tolerance": 1e-5},
        {"name": "Haute Précision", "max_iterations": 2000, "tolerance": 1e-6},
        
        # Configurations avec tolérance relâchée
        {"name": "Tolérance Large", "max_iterations": 1000, "tolerance": 1e-3},
        {"name": "Tolérance Moyenne", "max_iterations": 1500, "tolerance": 1e-4},
        
        # Configurations avec beaucoup d'itérations
        {"name": "Max Itérations", "max_iterations": 3000, "tolerance": 1e-5},
        {"name": "Ultra Précision", "max_iterations": 5000, "tolerance": 1e-6},
        
        # Configuration finale recommandée
        {"name": "Recommandée", "max_iterations": 2000, "tolerance": 1e-4},
    ]
    
    # 4. Tester toutes les configurations
    print(f"\n🧪 Test de {len(configurations)} configurations...")
    results_summary = []
    
    for i, config in enumerate(configurations, 1):
        print(f"\n📋 Configuration {i}/{len(configurations)}")
        
        try:
            result = test_hardy_cross_configuration(
                hardy_cross_data,
                config["max_iterations"],
                config["tolerance"],
                config["name"]
            )
            results_summary.append(result)
            
            # Si convergence atteinte, on peut arrêter ou continuer selon la précision
            if result['convergence']:
                print(f"   🎉 CONVERGENCE ATTEINTE avec {config['name']}!")
                if result['tolerance_finale'] < 1e-5:
                    print(f"   🏆 Précision excellente atteinte!")
                    break
            else:
                print(f"   ⚠️  Convergence non atteinte, tolérance finale: {result['tolerance_finale']}")
                
        except Exception as e:
            print(f"   ❌ Erreur avec {config['name']}: {e}")
            results_summary.append({
                'config_name': config['name'],
                'error': str(e),
                'convergence': False
            })
    
    # 5. Résumé des résultats
    print("\n" + "="*80)
    print("📊 RÉSUMÉ DES CONFIGURATIONS TESTÉES")
    print("="*80)
    
    converged_configs = [r for r in results_summary if r.get('convergence', False)]
    failed_configs = [r for r in results_summary if not r.get('convergence', False)]
    
    print(f"✅ Configurations convergentes : {len(converged_configs)}")
    print(f"❌ Configurations non convergentes : {len(failed_configs)}")
    
    if converged_configs:
        print("\n🏆 MEILLEURES CONFIGURATIONS :")
        # Trier par temps puis par précision
        converged_configs.sort(key=lambda x: (x.get('time', float('inf')), x.get('tolerance_finale', float('inf'))))
        
        for i, config in enumerate(converged_configs[:3], 1):
            print(f"   {i}. {config['config_name']}")
            print(f"      ⏱️  Temps: {config.get('time', 'N/A'):.3f}s")
            print(f"      🔄 Itérations: {config.get('iterations', 'N/A')}")
            print(f"      🎯 Tolérance finale: {config.get('tolerance_finale', 'N/A')}")
            print(f"      📊 Débits: {config.get('flows_count', 'N/A')}")
    
    # 6. Générer rapport avec la meilleure configuration
    if converged_configs:
        best_config = converged_configs[0]
        print(f"\n📝 Génération du rapport avec la configuration '{best_config['config_name']}'...")
        
        report_path = create_hardy_cross_report(
            network_data, 
            best_config['results'], 
            generation_time, 
            best_config['time']
        )
        print(f"✅ Rapport sauvegardé : {report_path}")
    
    # 7. Recommandations
    print("\n💡 RECOMMANDATIONS :")
    if converged_configs:
        best = converged_configs[0]
        print(f"   🎯 Configuration recommandée : {best['config_name']}")
        print(f"   📋 Paramètres : max_iterations={best['max_iterations']}, tolerance={best['tolerance']}")
        print(f"   ⏱️  Temps de calcul : {best['time']:.3f}s")
        print(f"   🎯 Précision : {best['tolerance_finale']}")
    else:
        print("   ⚠️  Aucune convergence atteinte")
        print("   💡 Suggestions :")
        print("      - Augmenter max_iterations à 5000+")
        print("      - Relâcher la tolérance à 1e-3")
        print("      - Vérifier la cohérence du réseau")
    
    total_time = time.time() - start_time
    print(f"\n🎉 Test terminé en {total_time:.3f}s")
    
    return results_summary

def create_hardy_cross_report(network_data: dict, hardy_cross_results: dict, 
                            generation_time: float, hc_time: float) -> str:
    """Crée un rapport détaillé Hardy-Cross et le sauvegarde"""
    
    iterations = hardy_cross_results.get('iterations', [])
    final_results = hardy_cross_results.get('final_results', {})
    flows = final_results.get('flows', {})
    pressures = final_results.get('pressures', {})
    convergence = hardy_cross_results.get('convergence', False)
    
    # Déterminer le statut de convergence
    if convergence:
        convergence_status = "Convergé"
        convergence_icon = "✅"
    else:
        convergence_status = "Non convergé"
        convergence_icon = "⚠️"
    
    # Déterminer le message de conclusion
    if convergence:
        conclusion_status = "convergé avec succès"
    else:
        conclusion_status = "pas convergé (avertissement)"
    
    report = f"""# 📊 Rapport Hardy-Cross - Réseau Paris Type

## 🎯 Objectif
Test complet de l'algorithme Hardy-Cross sur un réseau complexe de distribution d'eau.

## 📋 Données du Réseau
- **Nœuds** : {len(network_data['network']['nodes'])}
- **Conduites** : {len(network_data['network']['pipes'])}
- **Réservoirs** : {len([n for n in network_data['network']['nodes'].values() if n.get('type') == 'reservoir'])}
- **Date de création** : {network_data['metadata']['date_creation']}

## 🔧 Résultats Hardy-Cross
- **Statut** : {convergence_icon} {convergence_status}
- **Itérations** : {len(iterations)}
- **Tolérance finale** : {iterations[-1].get('tolerance', 'N/A') if iterations else 'N/A'}
- **Temps de calcul** : {hc_time:.3f}s

## 📈 Performance
- **Temps de génération** : {generation_time:.3f}s
- **Temps de calcul** : {hc_time:.3f}s
- **Temps total** : {generation_time + hc_time:.3f}s
- **Performance** : {len(flows) / (generation_time + hc_time):.1f} débits/s

## 📊 Résultats Détaillés

### Statistiques des Débits
"""
    
    if flows:
        flow_values = list(flows.values())
        mean_flow = sum(flow_values) / len(flow_values)
        min_flow = min(flow_values)
        max_flow = max(flow_values)
        variance = sum((x - mean_flow) ** 2 for x in flow_values) / len(flow_values)
        std_flow = variance ** 0.5
        
        report += f"""- **Nombre de débits calculés** : {len(flows)}
- **Débit moyen** : {mean_flow:.2f} L/s
- **Débit minimum** : {min_flow:.2f} L/s
- **Débit maximum** : {max_flow:.2f} L/s
- **Écart type** : {std_flow:.2f} L/s

### Top 10 des Débits les Plus Élevés
"""
        sorted_flows = sorted(flows.items(), key=lambda x: x[1], reverse=True)
        for i, (pipe_id, flow) in enumerate(sorted_flows[:10]):
            report += f"{i+1}. **{pipe_id}** : {flow:.2f} L/s\n"
    
    report += "\n### Statistiques des Pressions\n"
    
    if pressures:
        pressure_values = list(pressures.values())
        mean_pressure = sum(pressure_values) / len(pressure_values)
        min_pressure = min(pressure_values)
        max_pressure = max(pressure_values)
        variance = sum((x - mean_pressure) ** 2 for x in pressure_values) / len(pressure_values)
        std_pressure = variance ** 0.5
        
        report += f"""- **Nombre de pressions calculées** : {len(pressures)}
- **Pression moyenne** : {mean_pressure:.2f} m
- **Pression minimum** : {min_pressure:.2f} m
- **Pression maximum** : {max_pressure:.2f} m
- **Écart type** : {std_pressure:.2f} m

### Top 10 des Pressions les Plus Élevées
"""
        sorted_pressures = sorted(pressures.items(), key=lambda x: x[1], reverse=True)
        for i, (node_id, pressure) in enumerate(sorted_pressures[:10]):
            report += f"{i+1}. **{node_id}** : {pressure:.2f} m\n"
    
    report += f"""
## 🔄 Détails des Itérations
"""
    
    if iterations:
        report += "| Itération | Corrections Max (ΔQ) | Statut |\n"
        report += "|-----------|----------------------|--------|\n"
        
        # --- DÉBUT DE LA CORRECTION ---
        
        def get_max_correction_from_iter(iteration):
            """Fonction utilitaire pour extraire la correction max d'une itération."""
            corrections = iteration.get('corrections', {})
            if not corrections or not isinstance(corrections, dict):
                return 'N/A'
            
            # Extraire toutes les valeurs de delta_Q
            delta_values = [
                abs(data['delta_Q']) for data in corrections.values() 
                if isinstance(data, dict) and 'delta_Q' in data
            ]
            
            if not delta_values:
                return 'N/A'
            
            return f"{max(delta_values):.6f}" # On formate directement en texte

        # Afficher les 10 premières itérations
        for i, iteration in enumerate(iterations[:10]):
            max_correction_str = get_max_correction_from_iter(iteration)
            status = "✅ Terminé" if hardy_cross_results.get('convergence') else "🔄 En cours"
            report += f"| {i+1} | {max_correction_str} | {status} |\n"
        
        if len(iterations) > 10:
            report += f"| ... | ... | ... |\n"
            last_iteration = iterations[-1]
            max_correction_str = get_max_correction_from_iter(last_iteration)
            status = "✅ Terminé" if hardy_cross_results.get('convergence') else "⚠️ Limite Atteinte"
            report += f"| {len(iterations)} | {max_correction_str} | {status} |\n"
            
        # --- FIN DE LA CORRECTION ---
    
    report += f"""
## 🎉 Conclusion
L'algorithme Hardy-Cross a {conclusion_status}
sur un réseau complexe de {len(network_data['network']['nodes'])} nœuds et {len(network_data['network']['pipes'])} conduites.

**Performance** : {len(flows) / (generation_time + hc_time):.1f} débits calculés par seconde

"""
    
    if not convergence:
        report += f"""
## ⚠️ Avertissement de Convergence
L'algorithme n'a pas convergé dans le nombre d'itérations maximum autorisé.
**Recommandations :**
- Augmenter le nombre maximum d'itérations
- Ajuster la tolérance de convergence
- Vérifier la cohérence des données d'entrée
- Considérer l'utilisation d'un algorithme de relaxation

"""
    
    report += f"""
---
*Test effectué le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Version LCPI : 2.1.0*
*Algorithme : Hardy-Cross Enhanced*
"""

    # Sauvegarder le rapport
    os.makedirs("output", exist_ok=True)
    report_path = f"output/hardy_cross_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_path

if __name__ == "__main__":
    results = test_hardy_cross_complete()
    converged_configs = [r for r in results if r.get('convergence', False)]
    
    if converged_configs:
        print("\n✅ Test Hardy-Cross complet réussi avec convergence !")
    else:
        print("\n⚠️ Test Hardy-Cross : aucune convergence atteinte (avertissement)")
        sys.exit(1) 