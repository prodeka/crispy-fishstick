"""
Gestionnaire de contraintes et pénalités pour l'optimisation des réseaux d'eau.
Phase 2: Système de pénalités non-linéaires et liées au coût.
"""

from typing import Dict, Any, Optional, Tuple
import math
import logging

logger = logging.getLogger(__name__)

# PHASE 2: Fonctions de niveau module pour compatibilité
def normalize_violations(sim_metrics: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, float]:
    """
    Calcule un score de violation normalisé pour la pression et la vitesse.
    Un ratio > 0 indique une violation.
    
    Retourne un dictionnaire détaillé avec les ratios de violation et un total pondéré.
    """
    calculator = ConstraintPenaltyCalculator()
    return calculator.normalize_violations(sim_metrics, constraints)

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
    calculator = ConstraintPenaltyCalculator()
    return calculator.adaptive_penalty(violation_total, generation, total_generations, alpha_start, alpha_max, beta)

class ConstraintViolation:
    """Représente une violation de contrainte avec sa sévérité."""
    
    def __init__(self, constraint_type: str, current_value: float, required_value: float, 
                 violation_ratio: float, severity: str):
        self.constraint_type = constraint_type
        self.current_value = current_value
        self.required_value = required_value
        self.violation_ratio = violation_ratio
        self.severity = severity  # "minor", "moderate", "severe", "critical"

class ConstraintPenaltyCalculator:
    """Calcule les pénalités pour les violations de contraintes avec stratégie non-linéaire."""
    
    def __init__(self, base_penalty_factor: float = 1000.0):
        self.base_penalty_factor = base_penalty_factor
        
    # PHASE 2: Nouvelles méthodes de normalisation et pénalité adaptative
    def normalize_violations(self, sim_metrics: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, float]:
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
        self,
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
        
    def calculate_velocity_penalty(self, current_velocity: float, max_velocity: float, 
                                  solution_cost: float, budget_max: float) -> float:
        """
        Calcule la pénalité pour violation de vitesse avec stratégie non-linéaire.
        
        Args:
            current_velocity: Vitesse actuelle en m/s
            max_velocity: Vitesse maximale autorisée en m/s
            solution_cost: Coût de la solution en FCFA
            budget_max: Budget maximum en FCFA
            
        Returns:
            Pénalité en FCFA
        """
        if current_velocity <= max_velocity:
            return 0.0
            
        violation_ratio = current_velocity / max_velocity
        
        # PHASE 2: Pénalité non-linéaire basée sur la sévérité
        if violation_ratio > 2.0:
            # Violation critique: pénalité exponentielle
            penalty_multiplier = math.exp(violation_ratio - 2.0)
            severity_factor = 5.0
        elif violation_ratio > 1.5:
            # Violation sévère: pénalité cubique
            penalty_multiplier = (violation_ratio - 1.0) ** 3
            severity_factor = 3.0
        elif violation_ratio > 1.2:
            # Violation modérée: pénalité quadratique
            penalty_multiplier = (violation_ratio - 1.0) ** 2
            severity_factor = 2.0
        else:
            # Violation légère: pénalité linéaire
            penalty_multiplier = violation_ratio - 1.0
            severity_factor = 1.0
        
        # PHASE 2: Pénalité liée au coût de la solution
        base_penalty = self.base_penalty_factor * penalty_multiplier * severity_factor
        
        # Ajuster la pénalité en fonction du coût relatif
        if budget_max > 0:
            cost_ratio = solution_cost / budget_max
            if cost_ratio > 0.8:
                # Solution déjà coûteuse: pénalité plus forte
                cost_factor = 1.0 + (cost_ratio - 0.8) * 5.0
            elif cost_ratio < 0.5:
                # Solution bon marché: pénalité plus douce
                cost_factor = 0.5 + cost_ratio
            else:
                cost_factor = 1.0
        else:
            cost_factor = 1.0
            
        final_penalty = base_penalty * cost_factor
        
        logger.debug(f"Velocity penalty: {current_velocity:.2f}m/s vs {max_velocity:.2f}m/s "
                    f"(ratio: {violation_ratio:.2f}, penalty: {final_penalty:.0f} FCFA)")
        
        return final_penalty
    
    def calculate_pressure_penalty(self, current_pressure: float, min_pressure: float,
                                 solution_cost: float, budget_max: float) -> float:
        """
        Calcule la pénalité pour violation de pression avec stratégie non-linéaire.
        
        Args:
            current_pressure: Pression actuelle en mCE
            min_pressure: Pression minimale requise en mCE
            solution_cost: Coût de la solution en FCFA
            budget_max: Budget maximum en FCFA
            
        Returns:
            Pénalité en FCFA
        """
        if current_pressure >= min_pressure:
            return 0.0
            
        # Pression insuffisante: calculer la déficience
        pressure_deficit = min_pressure - current_pressure
        deficit_ratio = pressure_deficit / min_pressure if min_pressure > 0 else 1.0
        
        # PHASE 2: Pénalité non-linéaire pour la pression
        if deficit_ratio > 0.5:
            # Déficit critique: pénalité exponentielle
            penalty_multiplier = math.exp(deficit_ratio * 2.0)
            severity_factor = 8.0  # Plus sévère que la vitesse
        elif deficit_ratio > 0.3:
            # Déficit sévère: pénalité cubique
            penalty_multiplier = (deficit_ratio * 2.0) ** 3
            severity_factor = 5.0
        elif deficit_ratio > 0.1:
            # Déficit modéré: pénalité quadratique
            penalty_multiplier = (deficit_ratio * 3.0) ** 2
            severity_factor = 3.0
        else:
            # Déficit léger: pénalité linéaire
            penalty_multiplier = deficit_ratio * 5.0
            severity_factor = 1.5
        
        # PHASE 2: Pénalité liée au coût de la solution
        base_penalty = self.base_penalty_factor * penalty_multiplier * severity_factor
        
        # Ajuster la pénalité en fonction du coût relatif
        if budget_max > 0:
            cost_ratio = solution_cost / budget_max
            if cost_ratio > 0.8:
                # Solution déjà coûteuse: pénalité plus forte
                cost_factor = 1.0 + (cost_ratio - 0.8) * 8.0
            elif cost_ratio < 0.5:
                # Solution bon marché: pénalité plus douce
                cost_factor = 0.3 + cost_ratio * 0.4
            else:
                cost_factor = 1.0
        else:
            cost_factor = 1.0
            
        final_penalty = base_penalty * cost_factor
        
        logger.debug(f"Pressure penalty: {current_pressure:.2f}mCE vs {min_pressure:.2f}mCE "
                    f"(deficit: {pressure_deficit:.2f}mCE, penalty: {final_penalty:.0f} FCFA)")
        
        return final_penalty
    
    def calculate_budget_penalty(self, solution_cost: float, budget_max: float) -> float:
        """
        Calcule la pénalité pour dépassement du budget.
        
        Args:
            solution_cost: Coût de la solution en FCFA
            budget_max: Budget maximum en FCFA
            
        Returns:
            Pénalité en FCFA
        """
        if budget_max <= 0 or solution_cost <= budget_max:
            return 0.0
            
        # PHASE 2: Pénalité exponentielle pour dépassement de budget
        overshoot_ratio = solution_cost / budget_max
        overshoot_excess = overshoot_ratio - 1.0
        
        if overshoot_excess > 0.5:
            # Dépassement critique: pénalité très forte
            penalty_multiplier = math.exp(overshoot_excess * 3.0)
            severity_factor = 10.0
        elif overshoot_excess > 0.2:
            # Dépassement sévère: pénalité forte
            penalty_multiplier = math.exp(overshoot_excess * 2.0)
            severity_factor = 6.0
        else:
            # Dépassement modéré: pénalité modérée
            penalty_multiplier = overshoot_excess * 3.0
            severity_factor = 3.0
        
        # Pénalité basée sur le coût excédentaire
        base_penalty = (solution_cost - budget_max) * penalty_multiplier * severity_factor
        
        logger.debug(f"Budget penalty: {solution_cost:.0f} FCFA vs {budget_max:.0f} FCFA "
                    f"(overshoot: {overshoot_excess:.1%}, penalty: {base_penalty:.0f} FCFA)")
        
        return base_penalty
    
    def calculate_total_penalty(self, violations: Dict[str, Any], solution_cost: float, 
                               budget_max: float) -> Tuple[float, Dict[str, float]]:
        """
        Calcule la pénalité totale pour toutes les violations.
        
        Args:
            violations: Dictionnaire des violations détectées
            solution_cost: Coût de la solution en FCFA
            budget_max: Budget maximum en FCFA
            
        Returns:
            Tuple (pénalité totale, détail par type de violation)
        """
        total_penalty = 0.0
        penalty_details = {}
        
        # Pénalité pour violation de vitesse
        if "max_velocity_m_s" in violations:
            current_v = violations.get("current_velocity_m_s", 0.0)
            max_v = violations.get("max_velocity_m_s", 0.0)
            if max_v > 0:
                vel_penalty = self.calculate_velocity_penalty(current_v, max_v, solution_cost, budget_max)
                total_penalty += vel_penalty
                penalty_details["velocity"] = vel_penalty
        
        # Pénalité pour violation de pression
        if "min_pressure_mce" in violations:
            current_p = violations.get("current_pressure_mce", 0.0)
            min_p = violations.get("min_pressure_mce", 0.0)
            if min_p > 0:
                press_penalty = self.calculate_pressure_penalty(current_p, min_p, solution_cost, budget_max)
                total_penalty += press_penalty
                penalty_details["pressure"] = press_penalty
        
        # Pénalité pour dépassement de budget
        budget_penalty = self.calculate_budget_penalty(solution_cost, budget_max)
        if budget_penalty > 0:
            total_penalty += budget_penalty
            penalty_details["budget"] = budget_penalty
        
        # PHASE 2: Pénalité supplémentaire pour solutions avec violations multiples
        violation_count = len([v for v in penalty_details.values() if v > 0])
        if violation_count > 1:
            # Multiplicateur pour violations multiples
            multiple_violation_factor = 1.0 + (violation_count - 1) * 0.3
            total_penalty *= multiple_violation_factor
            penalty_details["multiple_violations"] = multiple_violation_factor
        
        logger.info(f"Total penalty: {total_penalty:.0f} FCFA for {violation_count} violations")
        
        return total_penalty, penalty_details

class ConstraintManager:
    """Gestionnaire principal des contraintes avec système de pénalités avancé."""
    
    def __init__(self, penalty_calculator: Optional[ConstraintPenaltyCalculator] = None):
        self.penalty_calculator = penalty_calculator or ConstraintPenaltyCalculator()
        
    def evaluate_solution_feasibility(self, sim_results: Dict[str, Any], 
                                    constraints: Dict[str, Any], 
                                    solution_cost: float) -> Tuple[bool, float, Dict[str, Any]]:
        """
        Évalue la faisabilité d'une solution et calcule les pénalités.
        
        Args:
            sim_results: Résultats de simulation
            constraints: Contraintes à respecter
            solution_cost: Coût de la solution
            
        Returns:
            Tuple (faisable, score total, détails des pénalités)
        """
        violations = {}
        
        # Vérifier les contraintes de vitesse
        if "vitesse_max_m_s" in constraints:
            max_vel = constraints["vitesse_max_m_s"]
            current_vel = sim_results.get("max_velocity_m_s", 0.0)
            if current_vel > max_vel:
                violations["max_velocity_m_s"] = max_vel
                violations["current_velocity_m_s"] = current_vel
        
        # Vérifier les contraintes de pression
        if "pression_min_mce" in constraints:
            min_press = constraints["pression_min_mce"]
            current_press = sim_results.get("min_pressure_m", 0.0)
            if current_press < min_press:
                violations["min_pressure_mce"] = min_press
                violations["current_pressure_mce"] = current_press
        
        # Vérifier les contraintes budgétaires
        budget_max = constraints.get("cout_max_fcfa", float("inf"))
        if solution_cost > budget_max:
            violations["budget_exceeded"] = True
        
        # Calculer les pénalités
        total_penalty, penalty_details = self.penalty_calculator.calculate_total_penalty(
            violations, solution_cost, budget_max
        )
        
        # Déterminer la faisabilité
        is_feasible = total_penalty == 0.0
        
        # Score total (coût + pénalités)
        total_score = solution_cost + total_penalty
        
        return is_feasible, total_score, {
            "violations": violations,
            "penalties": penalty_details,
            "total_penalty": total_penalty,
            "feasible": is_feasible,
            "total_score": total_score
        }
