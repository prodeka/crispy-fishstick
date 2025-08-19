import pytest
from src.lcpi.aep.optimizer.models import OptimizationConfig, OptimizationObjectives, VelocityConstraints

def test_optimization_config_loading():
    """Teste le chargement d'une configuration minimale et la validation par Pydantic."""
    raw_config = {
        "method": "global",
        "h_bounds_m": {
            "TANK1": [50.0, 80.0]
        },
        "pressure_min_m": 15.0
    }
    
    config = OptimizationConfig(**raw_config)
    
    assert config.method == "global"
    assert config.pressure_min_m == 15.0
    # Vérifier que les valeurs par défaut sont bien appliquées
    assert isinstance(config.objectives, OptimizationObjectives)
    assert config.objectives.capex is True
    assert config.objectives.lambda_opex == 10.0
    assert isinstance(config.velocity_constraints, VelocityConstraints)
    assert config.velocity_constraints.max_m_s == 2.5

def test_config_invalid_method():
    """Vérifie qu'une méthode invalide lève une erreur de validation."""
    raw_config = {
        "method": "invalid_method",
        "h_bounds_m": {"TANK1": [50.0, 80.0]}
    }
    with pytest.raises(ValueError):
        OptimizationConfig(**raw_config)

