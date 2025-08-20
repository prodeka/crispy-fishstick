from __future__ import annotations

from src.lcpi.aep.optimizer.constraints_handler import apply_constraints, apply_constraints_to_result


def test_apply_constraints_soft_penalty_with_aggregates():
    solution = {
        "CAPEX": 1_000_000.0,
        "metrics": {
            "min_pressure_m": 9.0,
            "max_velocity_m_s": 2.5,
        },
    }
    constraints = {"pressure_min_m": 10.0, "velocity_max_m_s": 2.0}
    out = apply_constraints(solution, constraints, mode="soft", penalty_weight=10.0)
    assert out["CAPEX"] > 1_000_000.0
    assert out["constraints_ok"] is False
    assert any(
        "Min pressure" in msg or "Velocity" in msg for msg in out.get("constraints_violations", [])
    )


def test_apply_constraints_hard_velocity():
    solution = {
        "CAPEX": 1_000_000.0,
        "metrics": {
            "min_pressure_m": 12.0,
            "max_velocity_m_s": 2.1,
        },
    }
    constraints = {"velocity_max_m_s": 2.0}
    out = apply_constraints(solution, constraints, mode="soft", penalty_weight=10.0, hard_velocity=True)
    assert out["constraints_ok"] is False


def test_apply_constraints_to_result():
    result = {
        "proposals": [
            {"CAPEX": 10.0, "metrics": {"min_pressure_m": 8.0}},
            {"CAPEX": 10.0, "metrics": {"min_pressure_m": 12.0}},
        ]
    }
    constraints = {"pressure_min_m": 10.0}
    out = apply_constraints_to_result(result, constraints, mode="soft", penalty_weight=100.0)
    assert len(out["proposals"]) == 2
    assert out["proposals"][0]["CAPEX"] > 10.0
"""
Unit tests for the constraints_handler module.
"""

import pytest
from lcpi.aep.optimizer.constraints_handler import apply_constraints


@pytest.fixture
def base_solution():
    """Provides a base solution with mock hydraulic results."""
    return {
        'cost': 100000,
        'hydraulics': {
            'pressures_m': {'node1': 20, 'node2': 18, 'node3': 25},
            'velocities_ms': {'pipe1': 1.5, 'pipe2': 1.8, 'pipe3': 1.2}
        },
        'constraints_ok': True,
        'constraints_violations': []
    }


@pytest.fixture
def constraints_config():
    """Provides a standard constraints configuration."""
    return {
        'pression_min_m': 15.0,
        'vitesse_max_ms': 2.0,
        'vitesse_min_ms': 0.1
    }


def test_apply_constraints_valid_solution(base_solution, constraints_config):
    """Tests that a valid solution passes the constraints check."""
    solution = apply_constraints(base_solution, constraints_config)
    assert solution['constraints_ok'] is True
    assert not solution['constraints_violations']
    assert solution['cost'] == 100000


def test_apply_constraints_pressure_violation_soft(base_solution, constraints_config):
    """Tests soft penalty for a minimum pressure violation."""
    base_solution['hydraulics']['pressures_m']['node2'] = 10  # Violates 15m
    penalty_weight = 1e5
    expected_penalty = (15.0 - 10.0) * penalty_weight
    
    solution = apply_constraints(base_solution, constraints_config, mode='soft', penalty_weight=penalty_weight)
    
    assert solution['constraints_ok'] is False
    assert len(solution['constraints_violations']) == 1
    assert "Pressure at node node2" in solution['constraints_violations'][0]
    assert solution['cost'] == 100000 + expected_penalty


def test_apply_constraints_velocity_violation_hard(base_solution, constraints_config):
    """Tests hard constraint for a maximum velocity violation."""
    base_solution['hydraulics']['velocities_ms']['pipe2'] = 2.5  # Violates 2.0m/s
    
    solution = apply_constraints(base_solution, constraints_config, mode='hard')
    
    assert solution['constraints_ok'] is False
    assert len(solution['constraints_violations']) == 1
    assert "Velocity in pipe pipe2" in solution['constraints_violations'][0]
    assert solution['cost'] == 100000  # No penalty in hard mode


def test_apply_constraints_multiple_violations_soft(base_solution, constraints_config):
    """Tests multiple soft penalties (pressure and velocity)."""
    base_solution['hydraulics']['pressures_m']['node1'] = 5  # Violates 15m
    base_solution['hydraulics']['velocities_ms']['pipe1'] = 3.0  # Violates 2.0m/s
    penalty_weight = 1e5
    
    pressure_penalty = (15.0 - 5.0) * penalty_weight
    velocity_penalty = (3.0 - 2.0) * penalty_weight
    expected_total_penalty = pressure_penalty + velocity_penalty

    solution = apply_constraints(base_solution, constraints_config, mode='soft', penalty_weight=penalty_weight)
    
    assert not solution['constraints_ok']
    assert len(solution['constraints_violations']) == 2
    assert solution['cost'] == 100000 + expected_total_penalty


def test_apply_constraints_no_hydraulic_data(base_solution, constraints_config):
    """Tests that no errors occur if hydraulic data is missing."""
    del base_solution['hydraulics']
    solution = apply_constraints(base_solution, constraints_config)
    assert solution['constraints_ok'] is True
    assert not solution['constraints_violations']


def test_apply_constraints_empty_hydraulic_data(base_solution, constraints_config):
    """Tests that no errors occur if hydraulic data is empty."""
    base_solution['hydraulics'] = {}
    solution = apply_constraints(base_solution, constraints_config)
    assert solution['constraints_ok'] is True
    assert not solution['constraints_violations']
