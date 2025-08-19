"""
Fichier de compatibilité pour l'ancien code utilisant lcpi.aep.epanet_wrapper.

Ce fichier redirige maintenant vers le wrapper unifié dans core.epanet_wrapper
pour maintenir la compatibilité avec l'ancien code.
"""

# Redirection vers le wrapper unifié
from .core.epanet_wrapper import (
    EpanetSimulator,           # Ancien wrapper ctypes
    EPANETOptimizer,           # Nouveau wrapper wntr pour optimisation
    EpanetWrapper,             # Interface moderne
    create_epanet_inp_file,    # Fonction utilitaire
    validate_hardy_cross_with_epanet,  # Validation
    is_epanet_available,       # Vérification disponibilité
    get_epanet_version         # Version EPANET
)

# Alias pour compatibilité
__all__ = [
    'EpanetSimulator',
    'EPANETOptimizer', 
    'EpanetWrapper',
    'create_epanet_inp_file',
    'validate_hardy_cross_with_epanet',
    'is_epanet_available',
    'get_epanet_version'
]

 