from __future__ import annotations

import pytest
from src.lcpi.aep.optimizer.constraints_handler import ConstraintPenaltyCalculator, normalize_violations, adaptive_penalty

def test_normalize_violations_no_violation():
    metrics = {"min_pressure_m": 15.0, "max_velocity_m_s": 1.5}
    constraints = {"pressure_min_m": 10.0, "velocity_max_m_s": 2.0}
    violations = normalize_violations(metrics, constraints)
    assert violations["total"] == 0.0
    assert violations["pressure_ratio"] == 0.0
    assert violations["velocity_ratio"] == 0.0

def test_normalize_violations_pressure_violation():
    metrics = {"min_pressure_m": 8.0, "max_velocity_m_s": 1.5}
    constraints = {"pressure_min_m": 10.0, "velocity_max_m_s": 2.0}
    violations = normalize_violations(metrics, constraints)
    # (10 - 8) / 10 = 0.2. Pondéré par 0.6 -> 0.12
    assert violations["pressure_ratio"] == pytest.approx(0.2)
    assert violations["velocity_ratio"] == 0.0
    assert violations["total"] == pytest.approx(0.12)

def test_normalize_violations_velocity_violation():
    metrics = {"min_pressure_m": 15.0, "max_velocity_m_s": 2.5}
    constraints = {"pressure_min_m": 10.0, "velocity_max_m_s": 2.0}
    violations = normalize_violations(metrics, constraints)
    # (2.5 - 2.0) / 2.0 = 0.25. Pondéré par 0.4 -> 0.1
    assert violations["pressure_ratio"] == 0.0
    assert violations["velocity_ratio"] == pytest.approx(0.25)
    assert violations["total"] == pytest.approx(0.1)

def test_normalize_violations_both_violations():
    metrics = {"min_pressure_m": 8.0, "max_velocity_m_s": 2.5}
    constraints = {"pressure_min_m": 10.0, "velocity_max_m_s": 2.0}
    violations = normalize_violations(metrics, constraints)
    # Pression: (10 - 8) / 10 = 0.2 * 0.6 = 0.12
    # Vitesse: (2.5 - 2.0) / 2.0 = 0.25 * 0.4 = 0.1
    # Total: 0.12 + 0.1 = 0.22
    assert violations["pressure_ratio"] == pytest.approx(0.2)
    assert violations["velocity_ratio"] == pytest.approx(0.25)
    assert violations["total"] == pytest.approx(0.22)

def test_normalize_violations_edge_cases():
    # Test avec des valeurs nulles
    metrics = {"min_pressure_m": 0.0, "max_velocity_m_s": 0.0}
    constraints = {"pressure_min_m": 10.0, "velocity_max_m_s": 2.0}
    violations = normalize_violations(metrics, constraints)
    assert violations["pressure_ratio"] == 1.0  # (10 - 0) / 10 = 1.0
    assert violations["velocity_ratio"] == 0.0  # (0 - 2) / 2 = -1, max(0, -1) = 0
    assert violations["total"] == pytest.approx(0.6)  # 1.0 * 0.6 + 0.0 * 0.4

def test_adaptive_penalty_no_violation():
    penalty_info = adaptive_penalty(0.0, 10, 100)
    assert penalty_info["value"] == 0.0
    assert penalty_info["alpha"] == 0.0
    assert penalty_info["beta"] == 1.8

def test_adaptive_penalty_increases_with_generation():
    violation = 0.1
    total_gen = 100
    penalty_start = adaptive_penalty(violation, 0, total_gen)
    penalty_mid = adaptive_penalty(violation, 50, total_gen)
    penalty_end = adaptive_penalty(violation, 99, total_gen)
    
    assert penalty_start["value"] < penalty_mid["value"] < penalty_end["value"]
    assert penalty_start["alpha"] < penalty_mid["alpha"] < penalty_end["alpha"]

def test_adaptive_penalty_is_nonlinear():
    violation_small = 0.1
    violation_large = 0.2  # 2x plus grande
    penalty_small = adaptive_penalty(violation_small, 10, 100)
    penalty_large = adaptive_penalty(violation_large, 10, 100)
    
    # La pénalité doit être plus que 2x plus grande car beta > 1
    assert penalty_large["value"] > penalty_small["value"] * 2

def test_adaptive_penalty_custom_parameters():
    violation = 0.15
    penalty_info = adaptive_penalty(
        violation, 5, 20,
        alpha_start=1e4,
        alpha_max=1e6,
        beta=2.0
    )
    
    assert penalty_info["beta"] == 2.0
    assert penalty_info["alpha"] >= 1e4
    assert penalty_info["alpha"] <= 1e6
    assert penalty_info["value"] > 0.0

def test_adaptive_penalty_progression():
    violation = 0.1
    total_gen = 50
    
    # Test que alpha progresse linéairement
    alphas = []
    for gen in range(0, total_gen, 10):
        penalty_info = adaptive_penalty(violation, gen, total_gen)
        alphas.append(penalty_info["alpha"])
    
    # Alpha doit augmenter de manière monotone
    for i in range(1, len(alphas)):
        assert alphas[i] >= alphas[i-1]

def test_adaptive_penalty_tolerance():
    # Test avec une violation très petite (proche de la tolérance)
    violation_tiny = 1e-7  # Plus petit que 1e-6
    penalty_info = adaptive_penalty(violation_tiny, 10, 100)
    assert penalty_info["value"] == 0.0
    
    # Test avec une violation juste au-dessus de la tolérance
    violation_small = 1e-5  # Plus grand que 1e-6
    penalty_info = adaptive_penalty(violation_small, 10, 100)
    assert penalty_info["value"] > 0.0
