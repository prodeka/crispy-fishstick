#!/usr/bin/env python3
"""
Démonstration des statistiques hydrauliques dans les résultats d'optimisation.
Usage: python tools/demo_hydraulic_statistics.py
"""

import json
import sys
from pathlib import Path

def display_hydraulic_statistics(json_file_path: str):
    """Affiche les statistiques hydrauliques d'un fichier de résultats JSON."""
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier {json_file_path}: {e}")
        return
    
    # Extraire les statistiques hydrauliques
    hydraulics = data.get("hydraulics", {})
    statistics = hydraulics.get("statistics", {})
    
    if not statistics:
        print(f"❌ Aucune statistique hydraulique trouvée dans {json_file_path}")
        return
    
    print(f"\n📊 STATISTIQUES HYDRAULIQUES - {Path(json_file_path).name}")
    print("=" * 80)
    
    # Résumé global
    if "summary" in statistics:
        print("\n🎯 RÉSUMÉ GLOBAL:")
        summary = statistics["summary"]
        for key, value in summary.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Statistiques des pressions
    if "pressures" in statistics:
        print("\n💧 PRESSIONS (m):")
        p = statistics["pressures"]
        print(f"  Nombre de nœuds: {p['count']}")
        print(f"  Min: {p['min']} | Max: {p['max']} | Moyenne: {p['mean']} | Médiane: {p['median']}")
        print(f"  Écart-type: {p['std']} | Q25: {p['q25']} | Q75: {p['q75']}")
        print(f"  % sous 10m: {p['percent_under_10m']}% | % sous 15m: {p['percent_under_15m']}% | % sous 20m: {p['percent_under_20m']}%")
    
    # Statistiques des vitesses
    if "velocities" in statistics:
        print("\n⚡ VITESSES (m/s):")
        v = statistics["velocities"]
        print(f"  Nombre de conduites: {v['count']}")
        print(f"  Min: {v['min']} | Max: {v['max']} | Moyenne: {v['mean']} | Médiane: {v['median']}")
        print(f"  Écart-type: {v['std']} | Q25: {v['q25']} | Q75: {v['q75']}")
        print(f"  % au-dessus 1m/s: {v['percent_over_1ms']}% | % au-dessus 2m/s: {v['percent_over_2ms']}% | % au-dessus 3m/s: {v['percent_over_3ms']}%")
    
    # Statistiques des charges hydrauliques
    if "heads" in statistics:
        print("\n🌊 CHARGES HYDRAULIQUES (m):")
        h = statistics["heads"]
        print(f"  Nombre de nœuds: {h['count']}")
        print(f"  Min: {h['min']} | Max: {h['max']} | Moyenne: {h['mean']} | Médiane: {h['median']}")
        print(f"  Écart-type: {h['std']}")
    
    # Statistiques des pertes de charge
    if "headlosses" in statistics:
        print("\n📉 PERTES DE CHARGE (m):")
        hl = statistics["headlosses"]
        print(f"  Nombre de conduites: {hl['count']}")
        print(f"  Min: {hl['min']} | Max: {hl['max']} | Moyenne: {hl['mean']} | Médiane: {hl['median']}")
        print(f"  Écart-type: {hl['std']} | Total: {hl['total']}")
    
    # Statistiques des débits
    if "flows" in statistics:
        print("\n🌊 DÉBITS (m³/s):")
        f = statistics["flows"]
        print(f"  Nombre de conduites: {f['count']}")
        print(f"  Min: {f['min']} | Max: {f['max']} | Moyenne: {f['mean']} | Médiane: {f['median']}")
        print(f"  Écart-type: {f['std']} | Total: {f['total']}")
    
    # Statistiques des diamètres
    if "diameters" in statistics:
        print("\n🔧 DIAMÈTRES (mm):")
        d = statistics["diameters"]
        print(f"  Nombre de conduites: {d['count']}")
        print(f"  Min: {d['min']} | Max: {d['max']} | Moyenne: {d['mean']} | Médiane: {d['median']}")
        print(f"  Écart-type: {d['std']}")
        
        if "distribution" in d:
            print("  Distribution par gammes DN:")
            for range_name, count in d["distribution"].items():
                if count > 0:
                    print(f"    {range_name}: {count} conduites ({count/d['count']*100:.1f}%)")
    
    # Indice de performance
    if "performance_index" in statistics:
        print(f"\n📈 INDICE DE PERFORMANCE HYDRAULIQUE: {statistics['performance_index']}")
    
    # Informations sur l'optimisation
    if "meta" in data:
        meta = data["meta"]
        print(f"\n⚙️ INFORMATIONS D'OPTIMISATION:")
        print(f"  Méthode: {meta.get('method', 'N/A')}")
        print(f"  Solveur: {meta.get('solver', 'N/A')}")
        print(f"  Générations: {meta.get('generations', 'N/A')}")
        print(f"  Population: {meta.get('population', 'N/A')}")
        print(f"  Durée: {meta.get('duration_seconds', 'N/A'):.2f} secondes")
    
    # Propositions d'optimisation
    proposals = data.get("proposals", [])
    if proposals:
        print(f"\n🏆 PROPOSITIONS D'OPTIMISATION ({len(proposals)} trouvées):")
        for i, prop in enumerate(proposals[:3], 1):  # Afficher les 3 premières
            print(f"  {i}. ID: {prop.get('id', 'N/A')}")
            print(f"     CAPEX: {prop.get('CAPEX', 'N/A'):,.0f} FCFA")
            print(f"     Pression min: {prop.get('min_pressure_m', 'N/A')} m")
            print(f"     Vitesse max: {prop.get('max_velocity_m_s', 'N/A')} m/s")
            print(f"     Contraintes respectées: {'✅' if prop.get('constraints_ok', False) else '❌'}")


def main():
    """Fonction principale."""
    
    # Fichiers de résultats à analyser
    result_files = [
        "results/out_with_hydraulic_stats.json",
        "results/out_with_hydraulic_stats_v2.json"
    ]
    
    print("🔍 ANALYSE DES STATISTIQUES HYDRAULIQUES")
    print("=" * 80)
    
    for file_path in result_files:
        if Path(file_path).exists():
            display_hydraulic_statistics(file_path)
            print("\n" + "="*80 + "\n")
        else:
            print(f"⚠️  Fichier non trouvé: {file_path}")
    
    print("✅ Analyse terminée!")


if __name__ == "__main__":
    main()
