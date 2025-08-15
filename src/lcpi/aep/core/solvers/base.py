"""
Interface abstraite pour les solveurs hydrauliques.

Ce module définit l'interface commune que tous les solveurs hydrauliques
(LCPI Hardy-Cross, EPANET, etc.) doivent implémenter.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class HydraulicSolver(ABC):
    """
    Interface abstraite pour un solveur hydraulique.
    
    Définit le contrat que tous les moteurs de calcul (LCPI, EPANET)
    doivent respecter pour être utilisables dans l'architecture
    Strategy Pattern.
    """
    
    @abstractmethod
    def run_simulation(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une simulation hydraulique pour un réseau donné.
        
        Args:
            network_data: Dictionnaire représentant le réseau avec les
                         diamètres à tester et les paramètres de calcul
                         
        Returns:
            Dictionnaire contenant les résultats de la simulation :
            - pressions: Dict[str, float] - Pressions par nœud (mCE)
            - flows: Dict[str, float] - Débits par conduite (m³/s)
            - velocities: Dict[str, float] - Vitesses par conduite (m/s)
            - status: str - Statut de la simulation ("success"/"failure")
            - solver: str - Nom du solveur utilisé
            - convergence: Dict[str, Any] - Informations de convergence
            - diagnostics: Dict[str, Any] - Diagnostics du réseau
        """
        pass
    
    @abstractmethod
    def get_solver_info(self) -> Dict[str, str]:
        """
        Retourne les informations sur le solveur.
        
        Returns:
            Dictionnaire contenant :
            - name: Nom du solveur
            - version: Version du solveur
            - description: Description du solveur
            - capabilities: Capacités du solveur
        """
        pass
    
    @abstractmethod
    def validate_network(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valide la structure du réseau pour ce solveur.
        
        Args:
            network_data: Données du réseau à valider
            
        Returns:
            Dictionnaire contenant :
            - valid: bool - Si le réseau est valide
            - errors: List[str] - Liste des erreurs
            - warnings: List[str] - Liste des avertissements
        """
        pass
    
    def get_supported_formulas(self) -> Dict[str, str]:
        """
        Retourne les formules de perte de charge supportées.
        
        Returns:
            Dictionnaire des formules supportées avec leurs descriptions
        """
        return {
            "hazen_williams": "Formule de Hazen-Williams",
            "darcy_weisbach": "Formule de Darcy-Weisbach"
        }
    
    def get_solver_parameters(self) -> Dict[str, Any]:
        """
        Retourne les paramètres par défaut du solveur.
        
        Returns:
            Dictionnaire des paramètres par défaut
        """
        return {
            "tolerance": 1e-6,
            "max_iterations": 200,
            "formula": "hazen_williams"
        }
