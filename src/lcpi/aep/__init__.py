"""
Module AEP (Alimentation en Eau Potable) pour LCPI-CLI.

Ce module implémente les calculs et analyses pour les systèmes d'alimentation en eau potable,
incluant l'optimisation, l'analyse de sensibilité et la comparaison de variantes.
"""

# Import des modules existants
try:
    from . import calculations
    from . import network
    from . import reservoir
    from . import pumping
    MODULES_BASE_AVAILABLE = True
except ImportError:
    MODULES_BASE_AVAILABLE = False

# Import des nouveaux modules de la PHASE 3
try:
    from . import optimization
    from . import sensitivity
    from . import comparison
    PHASE3_AVAILABLE = True
except ImportError:
    PHASE3_AVAILABLE = False

# Import des commandes
try:
    from .commands import network_optimize
    from .commands import network_optimize_unified
    COMMANDS_AVAILABLE = True
except ImportError:
    COMMANDS_AVAILABLE = False

__version__ = "1.5.0"
__author__ = "LCPI Team"

# Informations sur les modules disponibles
__all__ = [
    'PHASE3_AVAILABLE',
    'COMMANDS_AVAILABLE',
    'MODULES_BASE_AVAILABLE'
]

if MODULES_BASE_AVAILABLE:
    __all__.extend(['calculations', 'network', 'reservoir', 'pumping'])

if PHASE3_AVAILABLE:
    __all__.extend(['optimization', 'sensitivity', 'comparison'])

if COMMANDS_AVAILABLE:
    __all__.append('network_optimize')

def get_phase3_status():
    """Retourne le statut de disponibilité de la PHASE 3."""
    return {
        'optimization': PHASE3_AVAILABLE,
        'sensitivity': PHASE3_AVAILABLE,
        'comparison': PHASE3_AVAILABLE,
        'commands': COMMANDS_AVAILABLE
    } 