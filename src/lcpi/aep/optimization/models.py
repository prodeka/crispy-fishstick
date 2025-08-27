"""
Modèles Pydantic pour la validation des paramètres d'optimisation.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Literal
from enum import Enum

class CriteresOptimisation(BaseModel):
    """Critères d'optimisation multi-objectifs."""
    principal: Literal["cout", "energie", "performance"] = "cout"
    secondaires: List[Literal["cout", "energie", "performance"]] = []
    poids: List[float] = Field(default=[1.0])
    
    def model_post_init(self, __context):
        if len(self.poids) != len(self.secondaires) + 1:
            raise ValueError("Le nombre de poids doit être égal au nombre de critères")

class ContraintesBudget(BaseModel):
    """Contraintes budgétaires."""
    cout_max_fcfa: float = Field(..., gt=0, description="Coût maximum total en FCFA")
    cout_par_metre_max: Optional[float] = Field(None, gt=0, description="Coût maximum par mètre en FCFA")

class ContraintesTechniques(BaseModel):
    """Contraintes techniques du réseau."""
    pression_min_mce: float = Field(default=10.0, gt=0)
    pression_max_mce: float = Field(default=100.0, gt=0)
    vitesse_min_m_s: float = Field(default=0.5, gt=0)
    vitesse_max_m_s: float = Field(default=1.5, gt=0)
    
    def model_post_init(self, __context):
        if self.pression_min_mce >= self.pression_max_mce:
            raise ValueError("pression_min doit être inférieure à pression_max")
        if self.vitesse_min_m_s >= self.vitesse_max_m_s:
            raise ValueError("vitesse_min doit être inférieure à vitesse_max")

class ParametresAlgorithme(BaseModel):
    """Paramètres de l'algorithme d'optimisation."""
    type: Literal["genetique", "particle_swarm", "simulated_annealing"] = "genetique"
    population_size: int = Field(default=100, ge=20, le=1000)
    generations: int = Field(default=50, ge=10, le=500)
    mutation_rate: float = Field(default=0.1, ge=0.01, le=0.5)
    crossover_rate: float = Field(default=0.8, ge=0.5, le=0.95)
    tolerance: float = Field(default=1e-6, ge=1e-8, le=1e-3)

class DiametreCommercial(BaseModel):
    """Diamètre commercial avec son coût."""
    diametre_mm: int = Field(..., gt=0)
    cout_fcfa_m: float = Field(..., gt=0, description="Coût par mètre en FCFA")
    materiau: str = "pvc"
    pression_nominale: int = Field(default=6, gt=0)

class ConfigurationOptimisation(BaseModel):
    """Configuration complète pour l'optimisation."""
    criteres: CriteresOptimisation
    contraintes_budget: ContraintesBudget
    contraintes_techniques: ContraintesTechniques
    algorithme: ParametresAlgorithme
    diametres_candidats: List[DiametreCommercial]
    
    model_config = {"extra": "forbid"}
