"""
Solveur EPANET pour l'architecture Strategy Pattern.

Ce module implémente le solveur hydraulique EPANET qui peut être utilisé
de manière interchangeable avec le solveur LCPI Hardy-Cross.
"""

import os
import tempfile
from typing import Dict, Any, Optional
from pathlib import Path

from .base import HydraulicSolver

try:
    from ..epanet_wrapper import EpanetSimulator, create_epanet_inp_file
    from ..core.epanet_integration import EpanetWithDiagnostics
    EPANET_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ EPANET non disponible: {e}")
    EPANET_AVAILABLE = False


class EpanetSolver(HydraulicSolver):
    """
    Solveur hydraulique utilisant le moteur EPANET.
    
    Implémente l'interface HydraulicSolver pour permettre l'utilisation
    d'EPANET de manière interchangeable avec le solveur LCPI Hardy-Cross.
    """
    
    def __init__(self, epanet_path: Optional[str] = None):
        """
        Initialise le solveur EPANET.
        
        Args:
            epanet_path: Chemin vers la DLL EPANET (optionnel)
        """
        if not EPANET_AVAILABLE:
            raise RuntimeError("EPANET n'est pas disponible. Vérifiez l'installation.")
        
        self.epanet_path = epanet_path
        self.epanet_simulator = None
        self._initialize_epanet()
    
    def _initialize_epanet(self):
        """Initialise le simulateur EPANET."""
        try:
            self.epanet_simulator = EpanetWithDiagnostics(self.epanet_path)
        except Exception as e:
            raise RuntimeError(f"Impossible d'initialiser EPANET: {e}")
    
    def run_simulation(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une simulation hydraulique avec EPANET.
        
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
        try:
            # Exécuter la simulation avec diagnostics
            results = self.epanet_simulator.run_with_diagnostics(
                network_data, 
                skip_diagnostics=False
            )
            
            if not results["success"]:
                return {
                    "pressions": {},
                    "flows": {},
                    "velocities": {},
                    "status": "failure",
                    "solver": "epanet",
                    "convergence": {"converge": False},
                    "diagnostics": results.get("diagnostics", {}),
                    "errors": results.get("errors", [])
                }
            
            # Extraire les résultats EPANET
            epanet_results = results.get("epanet_results", {})
            
            return {
                "pressions": epanet_results.get("pressions", {}),
                "flows": epanet_results.get("flows", {}),
                "velocities": epanet_results.get("velocities", {}),
                "status": "success",
                "solver": "epanet",
                "convergence": {"converge": True},
                "diagnostics": results.get("diagnostics", {}),
                "simulation_time": epanet_results.get("simulation_time", 0.0)
            }
            
        except Exception as e:
            return {
                "pressions": {},
                "flows": {},
                "velocities": {},
                "status": "failure",
                "solver": "epanet",
                "convergence": {"converge": False},
                "diagnostics": {},
                "errors": [str(e)]
            }
    
    def get_solver_info(self) -> Dict[str, str]:
        """
        Retourne les informations sur le solveur EPANET.
        
        Returns:
            Dictionnaire contenant :
            - name: Nom du solveur
            - version: Version du solveur
            - description: Description du solveur
            - capabilities: Capacités du solveur
        """
        return {
            "name": "EPANET",
            "version": "2.2",
            "description": "Moteur de simulation hydraulique EPA (Environmental Protection Agency)",
            "capabilities": "Simulation hydraulique complète, analyse de qualité d'eau, gestion des pompes et vannes"
        }
    
    def validate_network(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valide la structure du réseau pour EPANET.
        
        Args:
            network_data: Données du réseau à valider
            
        Returns:
            Dictionnaire contenant :
            - valid: bool - Si le réseau est valide
            - errors: List[str] - Liste des erreurs
            - warnings: List[str] - Liste des avertissements
        """
        errors = []
        warnings = []
        
        # Vérifications de base
        if "noeuds" not in network_data:
            errors.append("Section 'noeuds' manquante")
        if "conduites" not in network_data:
            errors.append("Section 'conduites' manquante")
        
        if errors:
            return {
                "valid": False,
                "errors": errors,
                "warnings": warnings
            }
        
        # Vérifications spécifiques EPANET
        noeuds = network_data.get("noeuds", {})
        conduites = network_data.get("conduites", {})
        
        # Vérifier qu'il y a au moins un réservoir
        reservoirs = [n for n in noeuds.values() if n.get("role") == "reservoir"]
        if not reservoirs:
            errors.append("Au moins un nœud de type 'reservoir' est requis")
        
        # Vérifier la connectivité des conduites
        for conduit_id, conduit in conduites.items():
            noeud_amont = conduit.get("noeud_amont")
            noeud_aval = conduit.get("noeud_aval")
            
            if not noeud_amont or not noeud_aval:
                errors.append(f"Conduite {conduit_id}: noeud_amont et noeud_aval requis")
            elif noeud_amont not in noeuds:
                errors.append(f"Conduite {conduit_id}: noeud_amont '{noeud_amont}' non trouvé")
            elif noeud_aval not in noeuds:
                errors.append(f"Conduite {conduit_id}: noeud_aval '{noeud_aval}' non trouvé")
        
        # Vérifications des paramètres
        for noeud_id, noeud in noeuds.items():
            if noeud.get("role") == "consommation":
                if "demande_m3_s" not in noeud:
                    warnings.append(f"Nœud {noeud_id}: demande_m3_s recommandée pour les nœuds de consommation")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def get_supported_formulas(self) -> Dict[str, str]:
        """
        Retourne les formules de perte de charge supportées par EPANET.
        
        Returns:
            Dictionnaire des formules supportées avec leurs descriptions
        """
        return {
            "hazen_williams": "Formule de Hazen-Williams (C)",
            "darcy_weisbach": "Formule de Darcy-Weisbach (f)",
            "chezy_manning": "Formule de Chezy-Manning (n)"
        }
    
    def get_solver_parameters(self) -> Dict[str, Any]:
        """
        Retourne les paramètres par défaut du solveur EPANET.
        
        Returns:
            Dictionnaire des paramètres par défaut
        """
        return {
            "tolerance": 1e-6,
            "max_iterations": 200,
            "formula": "hazen_williams",
            "duration_hours": 24,
            "timestep_minutes": 60,
            "quality_type": "none"
        }
    
    def generate_inp_file(self, network_data: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """
        Génère un fichier .inp EPANET à partir des données réseau.
        
        Args:
            network_data: Données du réseau
            output_path: Chemin de sortie (optionnel)
            
        Returns:
            Chemin du fichier .inp généré
        """
        try:
            if output_path is None:
                # Créer un fichier temporaire
                temp_dir = tempfile.gettempdir()
                output_path = os.path.join(temp_dir, f"lcpi_epanet_{os.getpid()}.inp")
            
            # Utiliser la fonction existante de création de fichier .inp
            create_epanet_inp_file(network_data, output_path)
            
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la génération du fichier .inp: {e}")
    
    def run_epanet_simulation(self, inp_file_path: str) -> Dict[str, Any]:
        """
        Exécute une simulation EPANET directement depuis un fichier .inp.
        
        Args:
            inp_file_path: Chemin vers le fichier .inp
            
        Returns:
            Résultats de la simulation EPANET
        """
        try:
            # Utiliser le simulateur EPANET existant
            results = self.epanet_simulator.run_with_diagnostics(
                {},  # Données vides car on utilise le fichier .inp
                inp_file_path=inp_file_path,
                skip_diagnostics=True  # Pas besoin de diagnostics pour un fichier .inp
            )
            
            return results
            
        except Exception as e:
            return {
                "success": False,
                "errors": [str(e)],
                "epanet_results": {}
            }
