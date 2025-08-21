#!/usr/bin/env python3
"""
Test du calcul des statistiques hydrauliques détaillées.
Usage: python tools/test_hydraulic_statistics.py
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.lcpi.aep.optimizer.controllers import _calculate_hydraulic_statistics
    print("✅ Import réussi de _calculate_hydraulic_statistics")
except Exception as e:
    print(f"❌ Impossible d'importer _calculate_hydraulic_statistics: {e}")
    sys.exit(1)


def test_hydraulic_statistics():
    """Test avec des données hydrauliques simulées."""
    
    # Données de test réalistes
    test_data = {
        "pressures_m": {
            "N1": 64.73, "N2": 60.73, "N3": 63.73, "N4": 60.73, "N5": 57.73,
            "N6": 58.73, "N7": 60.73, "N8": 59.73, "N9": 61.73, "N10": 60.73,
            "N11": 59.73, "N12": 62.73, "N13": 63.73, "N14": 61.73, "N15": 67.73,
            "N16": 68.73, "N17": 59.73, "N18": 64.73, "N19": 62.73, "N20": 54.73,
        },
        "velocities_m_s": {
            "C1": 1.25, "C2": 0.89, "C3": 1.45, "C4": 0.67, "C5": 1.12,
            "C6": 0.93, "C7": 1.34, "C8": 0.78, "C9": 1.56, "C10": 0.45,
            "C11": 1.23, "C12": 0.91, "C13": 1.38, "C14": 0.72, "C15": 1.19,
        },
        "heads_m": {
            "N1": 165.23, "N2": 161.23, "N3": 164.23, "N4": 161.23, "N5": 158.23,
            "N6": 159.23, "N7": 161.23, "N8": 160.23, "N9": 162.23, "N10": 161.23,
        },
        "headlosses_m": {
            "C1": 2.45, "C2": 1.78, "C3": 3.12, "C4": 0.89, "C5": 2.34,
            "C6": 1.56, "C7": 2.89, "C8": 1.23, "C9": 3.45, "C10": 0.67,
        },
        "flows_m3_s": {
            "C1": 0.025, "C2": 0.018, "C3": 0.032, "C4": 0.012, "C5": 0.028,
            "C6": 0.015, "C7": 0.035, "C8": 0.022, "C9": 0.042, "C10": 0.008,
        },
        "diameters_mm": {
            "C1": 160, "C2": 200, "C3": 125, "C4": 250, "C5": 180,
            "C6": 220, "C7": 140, "C8": 200, "C9": 110, "C10": 315,
        }
    }
    
    print("\n=== TEST DES STATISTIQUES HYDRAULIQUES ===")
    print(f"Données de test: {len(test_data['pressures_m'])} nœuds, {len(test_data['velocities_m_s'])} conduites")
    
    # Calcul des statistiques
    stats = _calculate_hydraulic_statistics(test_data)
    
    # Affichage des résultats
    print("\n📊 RÉSULTATS DES STATISTIQUES HYDRAULIQUES:")
    print("=" * 60)
    
    # Résumé global
    if "summary" in stats:
        print("\n🎯 RÉSUMÉ GLOBAL:")
        for key, value in stats["summary"].items():
            print(f"  {key}: {value}")
    
    # Statistiques des pressions
    if "pressures" in stats:
        print("\n💧 PRESSIONS (m):")
        p = stats["pressures"]
        print(f"  Nombre de nœuds: {p['count']}")
        print(f"  Min: {p['min']} | Max: {p['max']} | Moyenne: {p['mean']} | Médiane: {p['median']}")
        print(f"  Écart-type: {p['std']} | Q25: {p['q25']} | Q75: {p['q75']}")
        print(f"  % sous 10m: {p['percent_under_10m']}% | % sous 15m: {p['percent_under_15m']}% | % sous 20m: {p['percent_under_20m']}%")
    
    # Statistiques des vitesses
    if "velocities" in stats:
        print("\n⚡ VITESSES (m/s):")
        v = stats["velocities"]
        print(f"  Nombre de conduites: {v['count']}")
        print(f"  Min: {v['min']} | Max: {v['max']} | Moyenne: {v['mean']} | Médiane: {v['median']}")
        print(f"  Écart-type: {v['std']} | Q25: {v['q25']} | Q75: {v['q75']}")
        print(f"  % au-dessus 1m/s: {v['percent_over_1ms']}% | % au-dessus 2m/s: {v['percent_over_2ms']}% | % au-dessus 3m/s: {v['percent_over_3ms']}%")
    
    # Statistiques des charges hydrauliques
    if "heads" in stats:
        print("\n🌊 CHARGES HYDRAULIQUES (m):")
        h = stats["heads"]
        print(f"  Nombre de nœuds: {h['count']}")
        print(f"  Min: {h['min']} | Max: {h['max']} | Moyenne: {h['mean']} | Médiane: {h['median']}")
        print(f"  Écart-type: {h['std']}")
    
    # Statistiques des pertes de charge
    if "headlosses" in stats:
        print("\n📉 PERTES DE CHARGE (m):")
        hl = stats["headlosses"]
        print(f"  Nombre de conduites: {hl['count']}")
        print(f"  Min: {hl['min']} | Max: {hl['max']} | Moyenne: {hl['mean']} | Médiane: {hl['median']}")
        print(f"  Écart-type: {hl['std']} | Total: {hl['total']}")
    
    # Statistiques des débits
    if "flows" in stats:
        print("\n🌊 DÉBITS (m³/s):")
        f = stats["flows"]
        print(f"  Nombre de conduites: {f['count']}")
        print(f"  Min: {f['min']} | Max: {f['max']} | Moyenne: {f['mean']} | Médiane: {f['median']}")
        print(f"  Écart-type: {f['std']} | Total: {f['total']}")
    
    # Statistiques des diamètres
    if "diameters" in stats:
        print("\n🔧 DIAMÈTRES (mm):")
        d = stats["diameters"]
        print(f"  Nombre de conduites: {d['count']}")
        print(f"  Min: {d['min']} | Max: {d['max']} | Moyenne: {d['mean']} | Médiane: {d['median']}")
        print(f"  Écart-type: {d['std']}")
        
        if "distribution" in d:
            print("  Distribution par gammes DN:")
            for range_name, count in d["distribution"].items():
                print(f"    {range_name}: {count} conduites")
    
    # Indice de performance
    if "performance_index" in stats:
        print(f"\n📈 INDICE DE PERFORMANCE HYDRAULIQUE: {stats['performance_index']}")
    
    print("\n✅ Test des statistiques hydrauliques terminé avec succès!")


def test_edge_cases():
    """Test avec des cas limites."""
    print("\n=== TEST DES CAS LIMITES ===")
    
    # Test avec données vides
    empty_data = {}
    stats_empty = _calculate_hydraulic_statistics(empty_data)
    print(f"Données vides: {len(stats_empty)} statistiques calculées")
    
    # Test avec données partielles
    partial_data = {
        "pressures_m": {"N1": 15.0, "N2": 20.0},
        "velocities_m_s": {"C1": 1.5}
    }
    stats_partial = _calculate_hydraulic_statistics(partial_data)
    print(f"Données partielles: {len(stats_partial)} statistiques calculées")
    
    # Test avec valeurs NaN
    nan_data = {
        "pressures_m": {"N1": 15.0, "N2": float('nan'), "N3": 20.0},
        "velocities_m_s": {"C1": 1.5, "C2": float('nan')}
    }
    stats_nan = _calculate_hydraulic_statistics(nan_data)
    print(f"Données avec NaN: {len(stats_nan)} statistiques calculées")
    
    print("✅ Tests des cas limites terminés!")


if __name__ == "__main__":
    test_hydraulic_statistics()
    test_edge_cases()
