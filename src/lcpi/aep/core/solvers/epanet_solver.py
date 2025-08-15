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
            self.epanet_simulator = EpanetSimulator(self.epanet_path)
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
            # Créer un fichier .inp temporaire
            temp_inp = tempfile.NamedTemporaryFile(suffix='.inp', delete=False)
            temp_inp.close()
            
            # Générer le fichier .inp
            if not create_epanet_inp_file(network_data, temp_inp.name):
                return {
                    "pressions": {},
                    "flows": {},
                    "velocities": {},
                    "status": "failure",
                    "solver": "epanet",
                    "convergence": {"converge": False},
                    "diagnostics": {},
                    "errors": ["Impossible de créer le fichier .inp"]
                }
            
            # Exécuter la simulation EPANET
            results = self._run_epanet_simulation(temp_inp.name)
            
            # Nettoyer le fichier temporaire
            try:
                os.unlink(temp_inp.name)
            except:
                pass
            
            return results
            
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
    
    def _run_epanet_simulation(self, inp_file_path: str) -> Dict[str, Any]:
        """
        Exécute une simulation EPANET complète.
        
        Args:
            inp_file_path: Chemin vers le fichier .inp
            
        Returns:
            Résultats de la simulation
        """
        try:
            # Ouvrir le projet EPANET
            if not self.epanet_simulator.open_project(inp_file_path):
                return {
                    "pressions": {},
                    "flows": {},
                    "velocities": {},
                    "status": "failure",
                    "solver": "epanet",
                    "convergence": {"converge": False},
                    "diagnostics": {},
                    "errors": ["Impossible d'ouvrir le projet EPANET"]
                }
            
            # Exécuter la simulation hydraulique
            if not self.epanet_simulator.solve_hydraulics():
                return {
                    "pressions": {},
                    "flows": {},
                    "velocities": {},
                    "status": "failure",
                    "solver": "epanet",
                    "convergence": {"converge": False},
                    "diagnostics": {},
                    "errors": ["Échec de la simulation hydraulique"]
                }
            
            # Sauvegarder les résultats
            if not self.epanet_simulator.save_results():
                return {
                    "pressions": {},
                    "flows": {},
                    "velocities": {},
                    "status": "failure",
                    "solver": "epanet",
                    "convergence": {"converge": False},
                    "diagnostics": {},
                    "errors": ["Impossible de sauvegarder les résultats"]
                }
            
            # Récupérer les résultats
            pressures = self.epanet_simulator.get_node_pressures()
            flows = self.epanet_simulator.get_link_flows()
            
            # Calculer les vitesses (approximatif)
            velocities = self._calculate_velocities(flows, network_data)
            
            # Générer les diagnostics
            diagnostics = self._generate_diagnostics(pressures, flows, velocities)
            
            # Fermer le projet
            self.epanet_simulator.close_project()
            
            return {
                "pressions": pressures,
                "flows": flows,
                "velocities": velocities,
                "status": "success",
                "solver": "epanet",
                "convergence": {"converge": True},
                "diagnostics": diagnostics
            }
            
        except Exception as e:
            # Fermer proprement en cas d'erreur
            try:
                self.epanet_simulator.close_project()
            except:
                pass
            raise e
    
    def _calculate_velocities(self, flows: Dict[str, float], 
                            network_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcule les vitesses à partir des débits et des diamètres.
        
        Args:
            flows: Débits par conduite
            network_data: Données du réseau
            
        Returns:
            Vitesses par conduite
        """
        velocities = {}
        conduites = network_data.get("conduites", {})
        
        for conduit_id, flow in flows.items():
            if conduit_id in conduites:
                conduit = conduites[conduit_id]
                diametre = conduit.get("diametre_m", 0)
                if diametre > 0:
                    # Convertir le débit de L/s en m³/s et calculer la vitesse
                    flow_m3s = flow / 1000  # L/s vers m³/s
                    area = 3.14159 * (diametre / 2) ** 2  # m²
                    velocity = abs(flow_m3s) / area  # m/s
                    velocities[conduit_id] = velocity
        
        return velocities
    
    def _generate_diagnostics(self, pressures: Dict[str, float], 
                            flows: Dict[str, float], 
                            velocities: Dict[str, float]) -> Dict[str, Any]:
        """
        Génère des diagnostics sur les résultats de simulation.
        
        Args:
            pressures: Pressions par nœud
            flows: Débits par conduite
            velocities: Vitesses par conduite
            
        Returns:
            Dictionnaire des diagnostics
        """
        diagnostics = {
            "boucles_detectees": 0,
            "nœuds_isoles": [],
            "conduites_critiques": [],
            "pression_min": float('inf'),
            "pression_max": float('-inf'),
            "vitesse_min": float('inf'),
            "vitesse_max": float('-inf'),
            "debit_total": 0.0,
            "nombre_noeuds": len(pressures),
            "nombre_conduites": len(flows)
        }
        
        # Analyser les pressions
        if pressures:
            diagnostics["pression_min"] = min(pressures.values())
            diagnostics["pression_max"] = max(pressures.values())
        
        # Analyser les vitesses
        if velocities:
            diagnostics["vitesse_min"] = min(velocities.values())
            diagnostics["vitesse_max"] = max(velocities.values())
        
        # Calculer le débit total
        if flows:
            diagnostics["debit_total"] = sum(abs(flow) for flow in flows.values())
        
        # Détecter les conduites critiques (vitesse trop élevée ou trop faible)
        for conduit_id, velocity in velocities.items():
            if velocity < 0.5:  # Vitesse minimale recommandée
                diagnostics["conduites_critiques"].append({
                    "conduit": conduit_id,
                    "type": "vitesse_trop_faible",
                    "valeur": velocity,
                    "seuil": 0.5
                })
            elif velocity > 2.5:  # Vitesse maximale recommandée
                diagnostics["conduites_critiques"].append({
                    "conduit": conduit_id,
                    "type": "vitesse_trop_elevee",
                    "valeur": velocity,
                    "seuil": 2.5
                })
        
        return diagnostics
    
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
        
        # Vérifications des conduites
        for conduit_id, conduit in conduites.items():
            diametre = conduit.get("diametre_m", 0)
            longueur = conduit.get("longueur_m", 0)
            
            if diametre <= 0:
                errors.append(f"Conduite {conduit_id}: diamètre doit être positif")
            if longueur <= 0:
                errors.append(f"Conduite {conduit_id}: longueur doit être positive")
        
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
            Chemin du fichier .inp
        """
        try:
            if output_path is None:
                # Créer un fichier temporaire
                temp_dir = tempfile.gettempdir()
                output_path = os.path.join(temp_dir, f"lcpi_epanet_{os.getpid()}.inp")
            
            # Utiliser la fonction existante de création de fichier .inp
            if create_epanet_inp_file(network_data, output_path):
                return output_path
            else:
                raise RuntimeError("Échec de la création du fichier .inp")
            
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
        return self._run_epanet_simulation(inp_file_path)
