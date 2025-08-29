"""
Module des solveurs hydrauliques pour LCPI-AEP (alias vers core.solvers).

Ce module fournit un alias vers les solveurs implémentés dans core.solvers
pour maintenir la compatibilité avec les imports existants.
"""

# Import des solveurs depuis core.solvers
from ..core.solvers import (
    HydraulicSolver,
    LcpiHardyCrossSolver,
    EpanetSolver,
    SolverFactory
)

# Import du module d'optimisation LCPI
from .lcpi_optimizer import LCPIOptimizer

__all__ = [
    'HydraulicSolver',
    'LcpiHardyCrossSolver', 
    'EpanetSolver',
    'SolverFactory',
    'LCPIOptimizer'
]
