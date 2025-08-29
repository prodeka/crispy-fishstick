"""
Module d'optimisation LCPI utilisant le solveur Hardy-Cross.

Ce module fournit une interface d'optimisation compatible avec le système
d'optimisation génétique existant, en utilisant notre solveur LCPI Hardy-Cross.
"""

import time
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

from ...core.solvers.lcpi_solver import LcpiHardyCrossSolver
from ...core.solvers.factory import SolverFactory

logger = logging.getLogger(__name__)


class LCPIOptimizer:
    """
    Optimiseur LCPI utilisant le solveur Hardy-Cross.
    
    Cette classe fournit une interface compatible avec le système d'optimisation
    existant, en utilisant notre solveur LCPI Hardy-Cross pour les simulations hydrauliques.
    """
    
    def __init__(self, tolerance: float = 1e-6, max_iterations: int = 200):
        """
        Initialise l'optimiseur LCPI.
        
        Args:
            tolerance: Tolérance de convergence pour Hardy-Cross
            max_iterations: Nombre maximum d'itérations pour Hardy-Cross
        """
        self.solver = LcpiHardyCrossSolver(tolerance=tolerance, max_iterations=max_iterations)
        self.network_model = None
        
    def _get_network_model_from_path(self, network_path: str) -> Dict[str, Any]:
        """
        Charge le modèle de réseau depuis un fichier INP ou YAML.
        
        Args:
            network_path: Chemin vers le fichier réseau
            
        Returns:
            Modèle de réseau au format attendu par le solveur
        """
        from ..controllers import convert_inp_to_unified_model
        
        path = Path(network_path)
        if path.suffix.lower() == '.inp':
            # Conversion INP vers modèle unifié
            network_data = convert_inp_to_unified_model(path)
            return network_data
        else:
            # Fichier YAML/JSON existant
            import yaml
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
    
    def simulate_network(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simule le réseau avec le solveur LCPI Hardy-Cross.
        
        Args:
            network_data: Données du réseau au format unifié
            
        Returns:
            Résultats de la simulation au format standardisé
        """
        try:
            # Adapter le format des données pour notre solveur
            adapted_data = self._adapt_network_data(network_data)
            
            # Exécuter la simulation
            start_time = time.time()
            results = self.solver.run_simulation(adapted_data)
            sim_time = time.time() - start_time
            
            # Adapter le format de sortie pour compatibilité
            return self._adapt_simulation_results(results, sim_time)
            
        except Exception as e:
            logger.error(f"Erreur lors de la simulation LCPI: {e}")
            return {
                "success": False,
                "error": str(e),
                "pressures": {},
                "velocities": {},
                "flows": {},
                "sim_time_seconds": 0.0
            }
    
    def _adapt_network_data(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapte le format des données réseau pour notre solveur.
        
        Args:
            network_data: Données réseau au format unifié
            
        Returns:
            Données adaptées pour le solveur LCPI
        """
        adapted = {
            "noeuds": {},
            "conduites": {},
            "parametres": {
                "tolerance": 1e-6,
                "max_iterations": 200,
                "methode": "hazen_williams"
            }
        }
        
        # Adapter les nœuds
        if "nodes" in network_data:
            for node_id, node_data in network_data["nodes"].items():
                adapted["noeuds"][node_id] = {
                    "role": node_data.get("type", "consommation"),
                    "cote_m": node_data.get("elevation_m", 0.0),
                    "demande_m3_s": node_data.get("base_demand_m3_s", 0.0),
                    "pression_min_mce": 20.0,
                    "pression_max_mce": 80.0
                }
        
        # Adapter les réservoirs
        if "tanks" in network_data:
            for tank_id, tank_data in network_data["tanks"].items():
                adapted["noeuds"][tank_id] = {
                    "role": "reservoir",
                    "cote_m": tank_data.get("radier_elevation_m", 0.0),
                    "demande_m3_s": 0.0,
                    "pression_min_mce": 20.0,
                    "pression_max_mce": 80.0
                }
        
        # Adapter les conduites
        if "links" in network_data:
            for link_id, link_data in network_data["links"].items():
                adapted["conduites"][link_id] = {
                    "noeud_amont": link_data.get("from", ""),
                    "noeud_aval": link_data.get("to", ""),
                    "longueur_m": link_data.get("length_m", 100.0),
                    "diametre_m": (link_data.get("diameter_mm", 100) / 1000.0),  # Conversion mm -> m
                    "rugosite": link_data.get("roughness", 100.0),
                    "materiau": "acier",  # Par défaut
                    "statut": "existant",
                    "coefficient_frottement": "hazen_williams"
                }
        
        return adapted
    
    def _adapt_simulation_results(self, results: Dict[str, Any], sim_time: float) -> Dict[str, Any]:
        """
        Adapte les résultats de simulation pour compatibilité.
        
        Args:
            results: Résultats bruts du solveur LCPI
            sim_time: Temps de simulation
            
        Returns:
            Résultats adaptés au format standard
        """
        if results.get("status") != "success":
            return {
                "success": False,
                "error": "Simulation LCPI échouée",
                "pressures": {},
                "velocities": {},
                "flows": {},
                "sim_time_seconds": sim_time
            }
        
        # Extraire les données des résultats
        pressures = results.get("pressures", {})
        velocities = results.get("velocities", {})
        flows = results.get("flows", {})
        
        # Calculer les statistiques
        min_pressure = min(pressures.values()) if pressures else 0.0
        max_pressure = max(pressures.values()) if pressures else 0.0
        min_velocity = min(velocities.values()) if velocities else 0.0
        max_velocity = max(velocities.values()) if velocities else 0.0
        
        return {
            "success": True,
            "pressures": pressures,
            "velocities": velocities,
            "flows": flows,
            "min_pressure_m": min_pressure,
            "max_pressure_m": max_pressure,
            "min_velocity_m_s": min_velocity,
            "max_velocity_m_s": max_velocity,
            "sim_time_seconds": sim_time,
            "solver_trace": results.get("solver_trace", []),
            "convergence": results.get("convergence", {}),
            "diagnostics": results.get("diagnostics", {})
        }
    
    def optimize_diameters(self, network_data: Dict[str, Any], 
                          constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimise les diamètres des conduites selon les contraintes.
        
        Args:
            network_data: Données du réseau
            constraints: Contraintes d'optimisation
            
        Returns:
            Résultats de l'optimisation
        """
        # Pour l'instant, retourner une solution de base
        # Dans une implémentation future, on pourrait ajouter une logique d'optimisation
        return {
            "success": True,
            "message": "Optimisation des diamètres non encore implémentée",
            "diameters": {},
            "cost": 0.0
        }


