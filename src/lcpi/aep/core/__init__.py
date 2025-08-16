"""
Module core pour les fonctionnalités de base AEP.
"""

# Import des composants de base
from .cache_manager import (
    CacheEntry,
    CacheManager,
    HydraulicCacheManager,
    get_cache_manager,
    clear_cache,
    get_cache_stats
)

from .epanet_wrapper import (
    EpanetWrapper,
    EpanetSimulator,
    get_epanet_wrapper,
    is_epanet_available,
    get_epanet_version,
    create_epanet_inp_file,
    validate_hardy_cross_with_epanet
)

# Liste des exports publics
__all__ = [
    # Cache Manager
    'CacheEntry',
    'CacheManager', 
    'HydraulicCacheManager',
    'get_cache_manager',
    'clear_cache',
    'get_cache_stats',
    
    # EPANET Wrapper
    'EpanetWrapper',
    'EpanetSimulator',
    'get_epanet_wrapper',
    'is_epanet_available',
    'get_epanet_version',
    'create_epanet_inp_file',
    'validate_hardy_cross_with_epanet'
] 