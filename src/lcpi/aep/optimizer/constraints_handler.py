"""
Centralized hydrodynamic constraint handling for optimization results.

Supports both aggregated metrics and detailed hydraulic results. Keys are
standardized to English across the codebase:
- pressure_min_m
- velocity_min_m_s
- velocity_max_m_s
"""

from typing import Dict, Any, List


def _get_aggregated_metrics(solution: Dict[str, Any]) -> Dict[str, float]:
    metrics = solution.get("metrics", {}) or {}
    agg: Dict[str, float] = {}
    # Common aggregated values set by optimizers/controllers
    if "min_pressure_m" in metrics or "min_pressure_m" in solution:
        agg["min_pressure_m"] = float(metrics.get("min_pressure_m", solution.get("min_pressure_m", 0.0)))
    if "max_velocity_m_s" in metrics or "max_velocity_m_s" in solution:
        agg["max_velocity_m_s"] = float(metrics.get("max_velocity_m_s", solution.get("max_velocity_m_s", 0.0)))
    return agg


def apply_constraints(
    solution: Dict[str, Any],
    constraints: Dict[str, float],
    *,
    mode: str = "soft",
    penalty_weight: float = 1e6,
    penalty_beta: float = 1.0,
    hard_velocity: bool = False,
) -> Dict[str, Any]:
    """
    Apply hydrodynamic constraints to a single solution proposal.

    The function supports both detailed hydraulic results under
    solution['hydraulics'] and aggregated metrics under solution['metrics'].
    """
    violations: List[str] = []
    total_penalty = 0.0

    # Detailed hydraulics (optional)
    hydraulic_results = solution.get("hydraulics", {}) or {}
    pressures = hydraulic_results.get("pressures_m", {}) or {}
    velocities = hydraulic_results.get("velocities_m_s", {}) or hydraulic_results.get("velocities_ms", {}) or {}

    # Aggregated metrics (common case)
    agg = _get_aggregated_metrics(solution)

    # Accept both EN and legacy FR keys from tests
    pmin_req = constraints.get("pressure_min_m")
    if pmin_req is None:
        pmin_req = constraints.get("pression_min_m")
    vmax_req = constraints.get("velocity_max_m_s")
    if vmax_req is None:
        vmax_req = constraints.get("vitesse_max_ms")
    vmin_req = constraints.get("velocity_min_m_s")
    if vmin_req is None:
        vmin_req = constraints.get("vitesse_min_ms")

    # Check pressure: prefer detailed pressures, else aggregated min
    if pmin_req is not None:
        if pressures:
            for node, pressure in pressures.items():
                if pressure < pmin_req:
                    violations.append(
                        f"Pressure at node {node} = {pressure:.3f}m < min {pmin_req:.3f}m"
                    )
                    if mode == "soft":
                        total_penalty += (pmin_req - pressure) ** max(1.0, penalty_beta) * penalty_weight * 10.0
        else:
            min_p = agg.get("min_pressure_m")
            if min_p is not None and min_p < pmin_req:
                violations.append(
                    f"Min pressure = {min_p:.3f}m < min {pmin_req:.3f}m"
                )
                if mode == "soft":
                    total_penalty += (pmin_req - min_p) ** max(1.0, penalty_beta) * penalty_weight * 10.0

    # Check velocity max: prefer detailed, else aggregated max
    if vmax_req is not None:
        if velocities:
            for pipe, vel in velocities.items():
                if vel > vmax_req:
                    violations.append(
                        f"Velocity in {pipe} = {vel:.3f}m/s > max {vmax_req:.3f}m/s"
                    )
                    if mode == "soft":
                        total_penalty += (vel - vmax_req) ** max(1.0, penalty_beta) * penalty_weight
        else:
            max_v = agg.get("max_velocity_m_s")
            if max_v is not None and max_v > vmax_req:
                violations.append(
                    f"Max velocity = {max_v:.3f}m/s > max {vmax_req:.3f}m/s"
                )
                if mode == "soft":
                    total_penalty += (max_v - vmax_req) ** max(1.0, penalty_beta) * penalty_weight

    # Check velocity min (soft only here; usually lower bound is guidance)
    if vmin_req is not None:
        if velocities:
            for pipe, vel in velocities.items():
                if vel < vmin_req:
                    violations.append(
                        f"Velocity in {pipe} = {vel:.3f}m/s < min {vmin_req:.3f}m/s"
                    )
                    if mode == "soft":
                        total_penalty += (vmin_req - vel) ** max(1.0, penalty_beta) * penalty_weight
        else:
            # Without detailed per-pipe data, we cannot reliably check vmin
            pass

    # Determine pass/fail
    constraints_ok = len(violations) == 0

    # Apply penalty to CAPEX in-place; also support simple 'cost' field used in some tests
    if mode == "soft" and total_penalty > 0.0:
        # Common fields used by controllers/optimizers
        if "CAPEX" in solution:
            try:
                solution["CAPEX"] = float(solution.get("CAPEX", 0.0)) + total_penalty
            except Exception:
                pass
        elif "costs" in solution and isinstance(solution["costs"], dict):
            solution["costs"]["CAPEX"] = float(solution["costs"].get("CAPEX", 0.0)) + total_penalty
        elif "cost" in solution and isinstance(solution.get("cost"), (int, float)):
            solution["cost"] = float(solution.get("cost", 0.0)) + total_penalty
        
        # En mode soft, si il y a des violations, marquer comme non conforme
        if violations:
            constraints_ok = False

    # If hard mode is requested, any violation forces constraints_ok=False
    if mode == "hard" or (hard_velocity and vmax_req is not None):
        if violations:
            constraints_ok = False

    solution["constraints_ok"] = constraints_ok
    solution["constraints_violations"] = violations
    return solution


def apply_constraints_to_result(
    result: Dict[str, Any],
    constraints: Dict[str, float],
    *,
    mode: str = "soft",
    penalty_weight: float = 1e6,
    penalty_beta: float = 1.0,
    hard_velocity: bool = False,
) -> Dict[str, Any]:
    """
    Apply constraints to all proposals in a result dict. Mutates and returns the result.
    """
    if not result:
        return result
    proposals = result.get("proposals", []) or []
    updated: List[Dict[str, Any]] = []
    for sol in proposals:
        updated.append(
            apply_constraints(
                sol,
                constraints,
                mode=mode,
                penalty_weight=penalty_weight,
                penalty_beta=penalty_beta,
                hard_velocity=hard_velocity,
            )
        )
    result["proposals"] = updated
    return result
