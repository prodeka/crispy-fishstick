"""
Factory pour les solveurs hydrauliques.

Ce module implémente le pattern Factory pour créer et gérer
les différentes instances de solveurs hydrauliques.
"""

from typing import Dict, Type, Any
from .base import HydraulicSolver
from .lcpi_solver import LcpiHardyCrossSolver
from .epanet_solver import EpanetSolver


class SolverFactory:
    """
    Factory pour créer les instances de solveurs hydrauliques.
    
    Permet de sélectionner dynamiquement le solveur approprié
    selon les besoins de l'utilisateur et les capacités requises.
    """
    
    _solvers: Dict[str, Type[HydraulicSolver]] = {
        "lcpi": LcpiHardyCrossSolver,
        "hardy_cross": LcpiHardyCrossSolver,  # Alias pour compatibilité
        "epanet": EpanetSolver,
    }
    
    @classmethod
    def get_solver(cls, solver_name: str, **kwargs) -> HydraulicSolver:
        """
        Retourne une instance du solveur demandé.
        
        Args:
            solver_name: Nom du solveur ("lcpi", "epanet", etc.)
            **kwargs: Paramètres d'initialisation du solveur
            
        Returns:
            Instance du solveur hydraulique
            
        Raises:
            ValueError: Si le solveur n'est pas reconnu
        """
        if solver_name not in cls._solvers:
            available = ", ".join(cls._solvers.keys())
            raise ValueError(f"Solveur '{solver_name}' inconnu. Disponibles: {available}")
        
        solver_class = cls._solvers[solver_name]
        return solver_class(**kwargs)
    
    @classmethod
    def list_available_solvers(cls) -> Dict[str, Dict[str, str]]:
        """
        Liste tous les solveurs disponibles avec leurs informations.
        
        Returns:
            Dictionnaire des solveurs disponibles avec leurs informations
        """
        solvers_info = {}
        for name, solver_class in cls._solvers.items():
            try:
                solver_instance = solver_class()
                solvers_info[name] = solver_instance.get_solver_info()
            except RuntimeError as e:
                # Si le solveur n'est pas disponible (ex: EPANET), on l'ignore
                if "EPANET n'est pas disponible" in str(e):
                    continue
                else:
                    raise
        
        return solvers_info
    
    @classmethod
    def register_solver(cls, name: str, solver_class: Type[HydraulicSolver]):
        """
        Enregistre un nouveau solveur dans la factory.
        
        Args:
            name: Nom du solveur
            solver_class: Classe du solveur (doit hériter de HydraulicSolver)
        """
        if not issubclass(solver_class, HydraulicSolver):
            raise ValueError(f"La classe {solver_class} doit hériter de HydraulicSolver")
        
        cls._solvers[name] = solver_class
    
    @classmethod
    def get_solver_capabilities(cls, solver_name: str) -> Dict[str, Any]:
        """
        Retourne les capacités d'un solveur spécifique.
        
        Args:
            solver_name: Nom du solveur
            
        Returns:
            Dictionnaire des capacités du solveur
        """
        solver = cls.get_solver(solver_name)
        return {
            "info": solver.get_solver_info(),
            "supported_formulas": solver.get_supported_formulas(),
            "default_parameters": solver.get_solver_parameters()
        }
    
    @classmethod
    def validate_solver_choice(cls, solver_name: str, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valide si un solveur est approprié pour un réseau donné.
        
        Args:
            solver_name: Nom du solveur à tester
            network_data: Données du réseau
            
        Returns:
            Dictionnaire de validation
        """
        try:
            solver = cls.get_solver(solver_name)
            validation = solver.validate_network(network_data)
            
            return {
                "solver_name": solver_name,
                "compatible": validation["valid"],
                "validation": validation,
                "capabilities": solver.get_solver_info()
            }
            
        except RuntimeError as e:
            # Gestion spécifique pour EPANET non disponible
            if "EPANET n'est pas disponible" in str(e):
                return {
                    "solver_name": solver_name,
                    "compatible": False,
                    "validation": {
                        "valid": False,
                        "errors": [str(e)],
                        "warnings": []
                    },
                    "capabilities": {}
                }
            else:
                raise
        except Exception as e:
            return {
                "solver_name": solver_name,
                "compatible": False,
                "validation": {
                    "valid": False,
                    "errors": [str(e)],
                    "warnings": []
                },
                "capabilities": {}
            }
