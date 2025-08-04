"""
Module AEP (Alimentation en Eau Potable) pour LCPI

Ce module implémente les calculs de dimensionnement des systèmes d'alimentation 
en eau potable selon les formules du document AEP et les standards techniques.

Fonctionnalités principales:
- Projections démographiques (Malthus, arithmétique, géométrique, logistique)
- Calculs de demande en eau (domestique, annexe, pointe)
- Dimensionnement réseau de distribution
- Dimensionnement réservoirs de stockage
- Dimensionnement équipements de pompage
- Protection anti-bélier
- Intégration avec les modules existants (hydrodrain, béton, etc.)

Auteur: LCPI Team
Version: 1.1.0 - Modules Unifiés
"""

from .core.constants import *
from .core.formulas import *

# Modules de base
from .calculations.population import *
from .calculations.demand import *
from .calculations.network import *
from .calculations.reservoir import *
from .calculations.pumping import *
from .calculations.protection import *
from .calculations.hardy_cross import *
from .calculations.integration import *

# Modules unifiés (nouvelles fonctionnalités)
from .calculations.population_unified import *
from .calculations.demand_unified import *
from .calculations.network_unified import *
from .calculations.reservoir_unified import *
from .calculations.pumping_unified import *

__version__ = "1.1.0"
__author__ = "LCPI Team"

# Export des fonctions principales pour faciliter l'import
__all__ = [
    # Fonctions de calcul de base
    "calculate_population_projection",
    "calculate_water_demand", 
    "dimension_network",
    "dimension_reservoir",
    "dimension_pumping",
    "calculate_water_hammer_protection",
    
    # Fonctions Hardy-Cross
    "hardy_cross_iteration",
    "hardy_cross_network",
    "calculate_resistance_coefficient",
    "validate_hardy_cross_data",
    
    # Fonctions d'intégration
    "integrated_aep_design",
    "compare_aep_scenarios",
    
    # Fonctions unifiées (nouvelles)
    "calculate_population_projection_unified",
    "calculate_water_demand_unified",
    "dimension_network_unified",
    "dimension_reservoir_unified",
    "dimension_pumping_unified",
    "calculate_water_demand_by_type_unified",
    "compare_water_demand_scenarios_unified",
    "comparer_methodes_network_unified",
    "comparer_scenarios_reservoir_unified",
    "comparer_types_pompes_unified",
    "calculer_temps_sejour_reservoir_unified",
    "calculer_cout_energie_pompage_unified",
    "calculate_well_discharge_unified",
    "calculate_population_evolution_unified",
    "verifier_vitesse_network_unified",
    "calculer_pression_requise_network_unified",
    
    # Utilitaires
    "validate_aep_data",
    "generate_aep_report",
    
    # Fonctions d'aide de base
    "get_population_help",
    "get_demand_help",
    "get_network_help",
    "get_reservoir_help",
    "get_pumping_help",
    "get_protection_help",
    "get_hardy_cross_help",
    "get_integration_help",
    
    # Fonctions d'aide unifiées
    "get_population_unified_help",
    "get_demand_unified_help",
    "get_network_unified_help",
    "get_reservoir_unified_help",
    "get_pumping_unified_help"
] 