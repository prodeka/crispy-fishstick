"""
Module des solveurs hydrauliques pour LCPI-AEP.

Ce module implémente le Strategy Pattern pour permettre l'utilisation
de différents solveurs hydrauliques (LCPI Hardy-Cross, EPANET, etc.)
de manière interchangeable.
"""

from .base import HydraulicSolver
from .lcpi_solver import LcpiHardyCrossSolver
from .epanet_solver import EpanetSolver
from .factory import SolverFactory

__all__ = [
    'HydraulicSolver',
    'LcpiHardyCrossSolver',
    'EpanetSolver',
    'SolverFactory'
]
