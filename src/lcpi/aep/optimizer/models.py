from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel, Field


class VelocityConstraints(BaseModel):
    min_m_s: Optional[float] = Field(0.3, description="Vitesse minimale autorisée en m/s")
    max_m_s: Optional[float] = Field(2.5, description="Vitesse maximale autorisée en m/s")


class CostConstraints(BaseModel):
    max_capex_fcfa: Optional[float] = Field(None, description="Budget d'investissement maximal")


class TankDecision(BaseModel):
    id: str = Field(..., description="ID du réservoir")
    H_m: float = Field(..., description="Hauteur piézométrique du réservoir en mètres")


class OptimizationObjectives(BaseModel):
    capex: bool = Field(True, description="Minimiser le CAPEX")
    opex: bool = Field(True, description="Minimiser l'OPEX")
    lambda_opex: float = Field(10.0, description="Facteur de pondération pour l'OPEX dans un score unifié")


class OptimizationConfig(BaseModel):
    method: Literal["binary", "nested", "global", "surrogate", "multi-tank"] = Field("nested", description="Algorithme à utiliser")
    objectives: OptimizationObjectives = Field(default_factory=OptimizationObjectives)
    
    h_bounds_m: Dict[str, Tuple[float, float]] = Field(..., description="Bornes de hauteur [min, max] pour chaque réservoir")
    pressure_min_m: float = Field(10.0, description="Contrainte de pression minimale au niveau des noeuds")
    velocity_constraints: VelocityConstraints = Field(default_factory=VelocityConstraints)
    cost_constraints: CostConstraints = Field(default_factory=CostConstraints)
    
    multi_tank: bool = Field(False, description="Active le mode d'optimisation multi-réservoirs")

    class GlobalMethodConfig(BaseModel):
        population_size: int = 80
        generations: int = 100
        parallel_workers: Optional[int] = None
        resume_from_checkpoint: Optional[str] = None

    class SurrogateMethodConfig(BaseModel):
        initial_samples: int = 50
        active_learning_rounds: int = 3
        persist_model: bool = True

    global_config: GlobalMethodConfig = Field(default_factory=GlobalMethodConfig)
    surrogate_config: SurrogateMethodConfig = Field(default_factory=SurrogateMethodConfig)


# Définition de Proposal comme classe de premier niveau
class Proposal(BaseModel):
    name: str
    is_feasible: bool
    tanks: List[TankDecision]
    diameters_mm: Dict[str, int]
    costs: Dict[str, float]  # CAPEX, OPEX_annual, OPEX_npv
    metrics: Dict[str, float]  # min_pressure_m, max_velocity_m_s


class OptimizationResult(BaseModel):
    proposals: List[Proposal] = Field(..., description="Liste des solutions proposées (ex: min_capex, knee_point)")
    pareto_front: Optional[List[Proposal]] = Field(None, description="Ensemble des points du front de Pareto")
    metadata: Dict[str, Any]