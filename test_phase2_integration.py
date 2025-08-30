#!/usr/bin/env python3
"""
Test d'intégration pour la Phase 2 : Pénalité adaptative non linéaire et normalisation des violations
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lcpi.aep.optimizer.constraints_handler import ConstraintPenaltyCalculator, normalize_violations, adaptive_penalty

def test_phase2_integration():
    """Test d'intégration des nouvelles fonctions de gestion des contraintes"""
    
    print("🧪 Test d'intégration Phase 2")
    print("=" * 50)
    
    # Test 1: Normalisation des violations
    print("\n1. Test de normalisation des violations:")
    
    # Cas sans violation
    metrics_no_violation = {
        "min_pressure_m": 15.0,
        "max_velocity_m_s": 1.5
    }
    constraints = {
        "pressure_min_m": 10.0,
        "velocity_max_m_s": 2.0
    }
    
    violations = normalize_violations(metrics_no_violation, constraints)
    print(f"   ✅ Sans violation: {violations}")
    assert violations["total"] == 0.0
    
    # Cas avec violation de pression
    metrics_pressure_violation = {
        "min_pressure_m": 8.0,
        "max_velocity_m_s": 1.5
    }
    
    violations = normalize_violations(metrics_pressure_violation, constraints)
    print(f"   ✅ Violation pression: {violations}")
    assert violations["pressure_ratio"] > 0.0
    assert violations["total"] > 0.0
    
    # Test 2: Pénalité adaptative
    print("\n2. Test de pénalité adaptative:")
    
    violation_total = violations["total"]
    penalty_info = adaptive_penalty(
        violation_total=violation_total,
        generation=10,
        total_generations=100,
        alpha_start=1e5,
        alpha_max=1e8,
        beta=1.8
    )
    
    print(f"   ✅ Pénalité calculée: {penalty_info}")
    assert penalty_info["value"] > 0.0
    assert penalty_info["alpha"] > 0.0
    assert penalty_info["beta"] == 1.8
    
    # Test 3: Progression de la pénalité
    print("\n3. Test de progression de la pénalité:")
    
    penalties = []
    for gen in [0, 25, 50, 75, 99]:
        penalty = adaptive_penalty(violation_total, gen, 100)
        penalties.append(penalty["value"])
        print(f"   Génération {gen}: pénalité = {penalty['value']:.0f}")
    
    # Vérifier que la pénalité augmente avec les générations
    for i in range(1, len(penalties)):
        assert penalties[i] >= penalties[i-1], f"La pénalité devrait augmenter: {penalties[i-1]} -> {penalties[i]}"
    
    print("\n✅ Tous les tests d'intégration Phase 2 passent !")
    return True

if __name__ == "__main__":
    try:
        test_phase2_integration()
        print("\n🎉 Phase 2 implémentée avec succès !")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        sys.exit(1)
