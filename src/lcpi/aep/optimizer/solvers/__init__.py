"""
Module des solveurs d'optimisation pour LCPI-AEP.
"""

from .lcpi_optimizer import LCPIOptimizer

# Import d'EPANETOptimizer depuis core pour maintenir la compatibilité
try:
    from ...core.epanet_wrapper import EPANETOptimizer
except ImportError:
    # Fallback si EPANETOptimizer n'est pas disponible
    EPANETOptimizer = None

__all__ = [
    'LCPIOptimizer',
    'EPANETOptimizer'
]


