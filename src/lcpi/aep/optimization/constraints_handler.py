# --- Contenu du nouveau fichier src/lcpi/aep/optimization/constraints_handler.py ---

from typing import Dict, Any

def normalize_violations(sim_metrics: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, float]:
    """
    Calcule un score de violation normalisé pour la pression et la vitesse.
    Un ratio > 0 indique une violation.
    
    Retourne un dictionnaire détaillé avec les ratios de violation et un total pondéré.
    """
    # Pression
    pressure_req_m = float(constraints.get("pressure_min_m", 10.0))
    min_pressure_obs_m = float(sim_metrics.get("min_pressure_m", 0.0) or 0.0)
    
    # Ratio = (Requis - Observé) / Requis. Uniquement si violation.
    pressure_violation_ratio = max(0.0, (pressure_req_m - min_pressure_obs_m) / max(1.0, pressure_req_m))

    # Vitesse
    velocity_max_ms = float(constraints.get("velocity_max_m_s", 2.0))
    max_velocity_obs_ms = float(sim_metrics.get("max_velocity_m_s", 0.0) or 0.0)
    
    # Ratio = (Observé - Max) / Max. Uniquement si violation.
    velocity_violation_ratio = max(0.0, (max_velocity_obs_ms - velocity_max_ms) / max(1.0, velocity_max_ms))
    
    # Score total pondéré (plus de poids sur la pression, qui est souvent plus critique)
    total_violation = (pressure_violation_ratio * 0.6) + (velocity_violation_ratio * 0.4)
    
    return {
        "pressure_ratio": pressure_violation_ratio,
        "velocity_ratio": velocity_violation_ratio,
        "total": total_violation
    }

def adaptive_penalty(
    violation_total: float,
    generation: int,
    total_generations: int,
    alpha_start: float = 1e5,
    alpha_max: float = 1e8,
    beta: float = 1.8
) -> Dict[str, float]:
    """
    Calcule une pénalité non linéaire et adaptative.
    
    - 'alpha' est le poids de la pénalité, il augmente avec les générations.
    - 'beta' (>1) est l'exposant non linéaire, qui punit sévèrement les grosses violations.
    """
    if violation_total <= 1e-6:  # Tolérance pour les erreurs de virgule flottante
        return {"value": 0.0, "alpha": 0.0, "beta": beta}
    
    # Progression de l'optimisation (de 0.0 à 1.0)
    progress_t = float(generation) / max(1, total_generations - 1)
    
    # Alpha augmente de manière linéaire au cours des générations
    alpha = min(alpha_start * (1 + 9 * progress_t), alpha_max)
    
    penalty = alpha * (violation_total ** beta)
    
    return {"value": penalty, "alpha": alpha, "beta": beta}
