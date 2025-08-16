"""
Module des commandes CLI pour LCPI-AEP.
"""

# Import des commandes existantes
from . import network_optimize

# Import des nouvelles commandes créées
try:
    from . import solvers
    from . import data_management
    from . import project_management
    SOLVERS_AVAILABLE = True
    DATA_MANAGEMENT_AVAILABLE = True
    PROJECT_MANAGEMENT_AVAILABLE = True
except ImportError:
    SOLVERS_AVAILABLE = False
    DATA_MANAGEMENT_AVAILABLE = False
    PROJECT_MANAGEMENT_AVAILABLE = False

__all__ = [
    'network_optimize',
    'SOLVERS_AVAILABLE',
    'DATA_MANAGEMENT_AVAILABLE', 
    'PROJECT_MANAGEMENT_AVAILABLE'
]

if SOLVERS_AVAILABLE:
    __all__.append('solvers')

if DATA_MANAGEMENT_AVAILABLE:
    __all__.append('data_management')

if PROJECT_MANAGEMENT_AVAILABLE:
    __all__.append('project_management')
