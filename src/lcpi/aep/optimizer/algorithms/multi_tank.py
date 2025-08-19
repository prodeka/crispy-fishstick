"""Optimiseur multi-réservoirs pour les réseaux d'eau."""

from __future__ import annotations

import copy
from typing import Any, Dict, Tuple
from pathlib import Path

import numpy as np

from ..solvers import EPANETOptimizer
from ..models import OptimizationResult, Proposal, TankDecision
from .binary import BinarySearchOptimizer, MockSolver


class MultiTankOptimizer:
    """Optimise un vecteur de hauteurs de réservoirs via la descente de coordonnées."""

    def __init__(self, network_path: str, config: Dict[str, Any]):
        self.network_path = network_path
        self.config = config
        self.solver = EPANETOptimizer()

    def optimize_heights(self) -> OptimizationResult:
        """Exécute l'algorithme de descente de coordonnées pour les hauteurs de réservoirs."""
        h_bounds = self.config.get("h_bounds_m", {})
        if not h_bounds:
            # Retourner un résultat d'erreur
            return OptimizationResult(
                proposals=[],
                pareto_front=None,
                metadata={
                    "method": "multi_tank",
                    "error": "h_bounds_m non défini pour les réservoirs",
                    "feasible": False
                }
            )

        tank_ids = list(h_bounds.keys())
        # Initialise les hauteurs au milieu de leurs bornes
        current_H = {tid: (bounds[0] + bounds[1]) / 2 for tid, bounds in h_bounds.items()}
        
        max_iter = self.config.get("max_iterations", 10)
        tolerance = self.config.get("tolerance_m", 0.5)

        for i in range(max_iter):
            previous_H = copy.deepcopy(current_H)

            for tank_to_optimize in tank_ids:
                # Crée une version "partielle" du problème pour l'optimiseur binaire
                # où les autres réservoirs sont fixés à leur hauteur actuelle.
                def objective_function(h: float) -> float:
                    temp_H = copy.deepcopy(current_H)
                    temp_H[tank_to_optimize] = h
                    
                    sim_result = self.solver.simulate(
                        self.network_path,
                        H_tank_map=temp_H,
                    )
                    if not sim_result.get("success"):
                        return -1e9 # Pénalité forte
                    
                    # La fonction objectif est la pression minimale (à maximiser)
                    return sim_result.get("min_pressure_m", -1e9)

                # Utilisation d'un simple scan de grille au lieu de l'optimiseur binaire
                # pour mieux gérer les interdépendances.
                bounds = h_bounds[tank_to_optimize]
                best_h = current_H[tank_to_optimize]
                max_pressure = -1e9

                for h_candidate in np.linspace(bounds[0], bounds[1], 10): # 10 étapes par dimension
                    pressure = objective_function(h_candidate)
                    if pressure > max_pressure:
                        max_pressure = pressure
                        best_h = h_candidate
                
                current_H[tank_to_optimize] = best_h

            # Condition de convergence
            h_diff = np.linalg.norm(np.array(list(current_H.values())) - np.array(list(previous_H.values())))
            if h_diff < tolerance:
                print(f"Convergence atteinte à l'itération {i+1}")
                break

        # Vérification finale de la solution
        final_sim = self.solver.simulate(self.network_path, H_tank_map=current_H)
        is_feasible = final_sim.get("success") and final_sim.get("min_pressure_m", 0) >= self.config.get("pressure_min_m", 10.0)

        # Créer les décisions de tanks
        tank_decisions = []
        for tank_id, h_m in current_H.items():
            tank_decisions.append(TankDecision(
                id=tank_id,
                H_m=h_m
            ))

        # Créer la proposition
        proposal = Proposal(
            name="multi_tank_solution",
            is_feasible=is_feasible,
            tanks=tank_decisions,
            diameters_mm={},  # Pas de diamètres dans cet optimiseur
            costs={},  # À calculer si nécessaire
            metrics={
                "min_pressure_m": final_sim.get("min_pressure_m", 0),
                "iterations": i + 1
            }
        )

        # Créer le résultat au format V11
        return OptimizationResult(
            proposals=[proposal],
            pareto_front=None,  # Pas de front Pareto pour cet optimiseur
            metadata={
                "method": "multi_tank",
                "network_file": str(self.network_path),
                "iterations": i + 1,
                "convergence_tolerance": tolerance,
                "max_iterations": max_iter,
                "feasible": is_feasible,
                "final_simulation": final_sim
            }
        )



