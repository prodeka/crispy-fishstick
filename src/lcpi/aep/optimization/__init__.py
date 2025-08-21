"""
Module d'optimisation des réseaux AEP.

Ce module implémente les algorithmes d'optimisation des diamètres
et de la configuration des réseaux d'alimentation en eau potable.
"""

from .individual import Individu
from .genetic_algorithm import GeneticOptimizerV2 as GeneticOptimizer
from .constraints import ConstraintManager

__all__ = [
    'Individu',
    'GeneticOptimizer',
    'ConstraintManager'
]
