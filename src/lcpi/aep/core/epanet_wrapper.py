"""
Wrapper EPANET unifié pour l'intégration avec le système LCPI.

Ce module fournit une interface unifiée pour interagir avec EPANET,
gérant les cas où EPANET n'est pas disponible et intégrant
les fonctionnalités d'optimisation modernes basées sur wntr.
"""

import logging
import os
import sys
import ctypes
import tempfile
import warnings
from pathlib import Path
import time
from typing import Dict, Any, Optional, List, Tuple, Union, Callable
import threading as _thr
import os as _os
import json
import yaml
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

logger = logging.getLogger(__name__)

# Supprimer les warnings spécifiques
def _suppress_warnings():
    """Supprime les warnings spécifiques liés à wntr et pkg_resources."""
    # Supprimer le warning pkg_resources déprécié
    warnings.filterwarnings("ignore", category=UserWarning, 
                           message="pkg_resources is deprecated as an API")
    
    # Supprimer le warning des chemins de ressources wntr
    warnings.filterwarnings("ignore", category=DeprecationWarning,
                           message="Use of .. or absolute path in a resource path")
    
    # Supprimer les warnings spécifiques wntr
    warnings.filterwarnings("ignore", category=UserWarning,
                           module="wntr.epanet.toolkit")
    warnings.filterwarnings("ignore", category=DeprecationWarning,
                           module="wntr.epanet.msx.toolkit")

# Appliquer la suppression des warnings
_suppress_warnings()

# Flag pour indiquer si EPANET est disponible
EPANET_AVAILABLE = False
WNTR_AVAILABLE = False

try:
    # Tentative d'import d'EPANET
    import epanet_python as epanet
    EPANET_AVAILABLE = True
    logger.info("EPANET Python wrapper chargé avec succès")
except ImportError:
    try:
        # Alternative: pyswmm
        import pyswmm
        EPANET_AVAILABLE = True
        logger.info("PySWMM chargé avec succès comme alternative à EPANET")
    except ImportError:
        logger.debug("EPANET non disponible. Utilisation du mode simulation uniquement.")
        EPANET_AVAILABLE = False

try:
    # Tentative d'import de wntr (plus moderne)
    import wntr
    WNTR_AVAILABLE = True
    logger.info("WNTR chargé avec succès")
except ImportError:
    logger.debug("WNTR non disponible. Utilisation du wrapper ctypes uniquement.")
    WNTR_AVAILABLE = False

# Constantes EPANET pour compatibilité
EN_NODECOUNT = 0
EN_LINKCOUNT = 1
EN_DEMAND = 9
EN_HEAD = 10
EN_PRESSURE = 11
EN_FLOW = 8
EN_VELOCITY = 12
EN_HEADLOSS = 13


class EpanetWrapper:
    """
    Wrapper pour l'interface EPANET avec gestion des erreurs et fallback.
    """
    
    def __init__(self):
        self.available = EPANET_AVAILABLE
        self.version = "2.2" if EPANET_AVAILABLE else "simulation_only"
        
    def is_available(self) -> bool:
        """Vérifie si EPANET est disponible."""
        return self.available
    
    def get_version(self) -> str:
        """Retourne la version d'EPANET ou 'simulation_only'."""
        return self.version
    
    def generate_inp_file(self, network_data: Dict[str, Any], output_path: Path) -> bool:
        """
        Génère un fichier .inp EPANET à partir des données du réseau.
        
        Args:
            network_data: Données du réseau au format LCPI
            output_path: Chemin du fichier .inp à générer
            
        Returns:
            True si la génération a réussi, False sinon
        """
        try:
            if not self.available:
                logger.debug("EPANET non disponible, génération du fichier .inp impossible")
                return False
            
            # Générer le contenu du fichier .inp
            inp_content = self._create_inp_content(network_data)
            
            # Écrire le fichier
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(inp_content)
            
            logger.info(f"Fichier .inp généré avec succès: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du fichier .inp: {e}")
            return False
    
    def run_simulation(self, inp_file_path: Path, output_file_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Exécute une simulation EPANET.
        
        Args:
            inp_file_path: Chemin vers le fichier .inp
            output_file_path: Chemin pour le fichier de sortie (optionnel)
            
        Returns:
            Dictionnaire contenant les résultats de la simulation
        """
        if not self.available:
            logger.debug("EPANET non disponible, simulation impossible")
            return {
                "success": False,
                "error": "EPANET non disponible",
                "results": {}
            }
        
        try:
            # Lancer la simulation EPANET
            with epanet.ENepanet() as en:
                # Charger le projet
                en.ENopen(str(inp_file_path))
                
                # Lancer la simulation hydraulique
                en.ENsolveH()
                
                # Extraire les résultats
                results = self._extract_simulation_results(en)
                
                # Sauvegarder les résultats si demandé
                if output_file_path:
                    self._save_results(results, output_file_path)
                
                return {
                    "success": True,
                    "results": results,
                    "error": None
                }
                
        except Exception as e:
            logger.error(f"Erreur lors de la simulation EPANET: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": {}
            }
    
    def _create_inp_content(self, network_data: Dict[str, Any]) -> str:
        """
        Crée le contenu du fichier .inp EPANET.
        
        Args:
            network_data: Données du réseau
            
        Returns:
            Contenu du fichier .inp
        """
        # Extraire les composants du réseau
        nodes = network_data.get("noeuds", {})
        pipes = network_data.get("conduites", {})
        
        # En-tête du fichier
        content = "[TITLE]\n"
        content += f"{network_data.get('nom', 'Réseau LCPI')}\n\n"
        
        # Section des nœuds
        content += "[JUNCTIONS]\n"
        content += "ID\tElev\tDemand\tPattern\tComment\n"
        for node_id, node_data in nodes.items():
            if node_data.get("role") != "reservoir":
                elevation = node_data.get("cote_m", 0)
                demand = node_data.get("demande_m3_s", 0) * 1000  # Conversion en L/s
                content += f"{node_id}\t{elevation:.2f}\t{demand:.3f}\t\t{node_data.get('role', '')}\n"
        
        # Section des réservoirs
        content += "\n[RESERVOIRS]\n"
        content += "ID\tHead\tPattern\tComment\n"
        for node_id, node_data in nodes.items():
            if node_data.get("role") == "reservoir":
                head = node_data.get("cote_m", 0)
                content += f"{node_id}\t{head:.2f}\t\tRéservoir\n"
        
        # Section des conduites
        content += "\n[PIPES]\n"
        content += "ID\tNode1\tNode2\tLength\tDiameter\tRoughness\tMinorLoss\tStatus\n"
        for pipe_id, pipe_data in pipes.items():
            node1 = pipe_data.get("noeud_amont", "")
            node2 = pipe_data.get("noeud_aval", "")
            length = pipe_data.get("longueur_m", 0)
            diameter = pipe_data.get("diametre_m", 0) * 1000  # Conversion en mm
            roughness = pipe_data.get("rugosite", 100)
            content += f"{pipe_id}\t{node1}\t{node2}\t{length:.2f}\t{diameter:.0f}\t{roughness}\t0\tOpen\n"
        
        # Section des options
        content += "\n[OPTIONS]\n"
        content += "Units\tLPS\n"
        content += "Headloss\tH-W\n"
        content += "Specific Gravity\t1.0\n"
        content += "Viscosity\t1.0\n"
        content += "Trials\t40\n"
        content += "Accuracy\t0.001\n"
        content += "Unbalanced\tContinue\n"
        content += "Pattern\t1\n"
        content += "Demand Multiplier\t1.0\n"
        content += "Emitter Exponent\t0.5\n"
        content += "Quality\tNone mg/L\n"
        content += "Diffusivity\t1.0\n"
        content += "Tolerance\t0.01\n"
        
        # Section des patterns (profil de consommation)
        content += "\n[PATTERNS]\n"
        content += "ID\tMultipliers\n"
        content += "1\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\n"
        
        # Section des contrôles
        content += "\n[CONTROLS]\n"
        
        # Section des règles
        content += "\n[RULES]\n"
        
        # Section des qualités
        content += "\n[QUALITY]\n"
        content += "ID\tInitQual\tSourceID\tSourceType\tSourcePattern\n"
        
        # Section des sources
        content += "\n[SOURCES]\n"
        content += "ID\tType\tQuality\tPattern\n"
        
        # Section des mélanges
        content += "\n[MIXING]\n"
        content += "ID\tModel\tTankID\tCompVal\n"
        
        # Section des réactions
        content += "\n[REACTIONS]\n"
        content += "Order Bulk\t1\n"
        content += "Order Wall\t1\n"
        content += "Global Bulk\t0\n"
        content += "Global Wall\t0\n"
        content += "Limiting Potential\t0\n"
        content += "Roughness Correlation\t0\n"
        
        # Section des énergies
        content += "\n[ENERGY]\n"
        content += "Global Efficiency\t75\n"
        content += "Global Price\t0\n"
        content += "Demand Charge\t0\n"
        
        # Section des courbes
        content += "\n[CURVES]\n"
        content += "ID\tX-Value\tY-Value\n"
        
        # Section des time series
        content += "\n[TIMESERIES]\n"
        content += "ID\tDate\tTime\tValue\n"
        
        # Section des options de rapport
        content += "\n[REPORT]\n"
        content += "Status\tYES\n"
        content += "Summary\tYES\n"
        content += "Page\t0\n"
        content += "Energy\tYES\n"
        content += "Nodes\tALL\n"
        content += "Links\tALL\n"
        
        return content
    
    def _extract_simulation_results(self, en) -> Dict[str, Any]:
        """
        Extrait les résultats de la simulation EPANET.
        
        Args:
            en: Instance EPANET
            
        Returns:
            Dictionnaire contenant les résultats
        """
        results = {
            "nodes": {},
            "pipes": {},
            "summary": {}
        }
        
        try:
            # Informations sur les nœuds
            num_nodes = en.ENgetcount(EN_NODECOUNT)
            for i in range(1, num_nodes + 1):
                node_id = en.ENgetnodeid(i)
                pressure = en.ENgetnodevalue(i, EN_PRESSURE)
                head = en.ENgetnodevalue(i, EN_HEAD)
                demand = en.ENgetnodevalue(i, EN_DEMAND)
                
                results["nodes"][node_id] = {
                    "pressure": pressure,
                    "head": head,
                    "demand": demand
                }
            
            # Informations sur les conduites
            num_pipes = en.ENgetcount(EN_LINKCOUNT)
            for i in range(1, num_pipes + 1):
                link_id = en.ENgetlinkid(i)
                link_type = en.ENgetlinktype(i)
                
                if link_type == 0:  # EN_PIPE = 0
                    flow = en.ENgetlinkvalue(i, EN_FLOW)
                    velocity = en.ENgetlinkvalue(i, EN_VELOCITY)
                    headloss = en.ENgetlinkvalue(i, EN_HEADLOSS)
                    
                    results["pipes"][link_id] = {
                        "flow": flow,
                        "velocity": velocity,
                        "headloss": headloss
                    }
            
            # Résumé de la simulation
            results["summary"] = {
                "total_nodes": num_nodes,
                "total_pipes": num_pipes,
                "simulation_status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des résultats: {e}")
        
        return results
    
    def _save_results(self, results: Dict[str, Any], output_path: Path):
        """
        Sauvegarde les résultats dans un fichier.
        
        Args:
            results: Résultats à sauvegarder
            output_path: Chemin du fichier de sortie
        """
        try:
            if output_path.suffix.lower() == '.json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
            elif output_path.suffix.lower() in ['.yml', '.yaml']:
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(results, f, default_flow_style=False, allow_unicode=True)
            else:
                # Format par défaut: JSON
                output_path = output_path.with_suffix('.json')
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Résultats sauvegardés: {output_path}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des résultats: {e}")


class EpanetSimulator:
    """
    Wrapper pour EPANET 2.2 utilisant ctypes (compatibilité avec l'ancien code).
    """
    
    # Constantes EPANET
    EN_PRESSURE = 11
    EN_FLOW = 8
    EN_NODE = 0
    EN_LINK = 1
    EN_JUNCTION = 0
    EN_RESERVOIR = 1
    EN_TANK = 2
    EN_PIPE = 0
    EN_PUMP = 1
    EN_VALVE = 2
    
    def __init__(self, epanet_path: Optional[str] = None):
        """
        Initialise le wrapper EPANET.
        
        Args:
            epanet_path: Chemin vers la DLL EPANET (optionnel)
        """
        self.epanet_path = epanet_path or self._find_epanet_dll()
        self.lib = None
        if self.epanet_path:
            self._load_library()
            self._define_function_prototypes()
        
    def _find_epanet_dll(self) -> Optional[str]:
        """
        Trouve le chemin vers la DLL EPANET.
        
        Returns:
            Chemin vers la DLL EPANET ou None si non trouvée
        """
        # Ordre de priorité pour la recherche des DLLs
        search_paths = [
            # 1. Dossier vendor/dlls du projet (priorité haute)
            Path(__file__).parent.parent.parent.parent.parent / "vendor" / "dlls",
            # 2. Dossier epanet_lib local
            Path(__file__).parent.parent / "epanet_lib",
            # 3. Dossier EPANET_2_3_1_WIN_32_64
            Path(__file__).parent.parent.parent.parent.parent / "EPANET_2_3_1_WIN_32_64" / "64bit",
            Path(__file__).parent.parent.parent.parent.parent / "EPANET_2_3_1_WIN_32_64" / "32bit",
            # 4. Dossier système Windows
            Path("C:/Windows/System32"),
            Path("C:/Windows/SysWOW64"),
        ]
        
        # Noms de DLLs à essayer (priorité 64-bit)
        dll_names = [
            "epanet2_64.dll",  # DLL 64-bit du projet
            "epanet2.dll",     # DLL par défaut
            "epanet2_32.dll",  # DLL 32-bit du projet
        ]
        
        for search_path in search_paths:
            if search_path.exists():
                for dll_name in dll_names:
                    dll_path = search_path / dll_name
                    if dll_path.exists():
                        logger.info(f"DLL EPANET trouvée: {dll_path}")
                        return str(dll_path)
        
        logger.warning("Aucune DLL EPANET trouvée dans les chemins de recherche.")
        return None
    
    def _load_library(self):
        """Charge la bibliothèque EPANET"""
        if not self.epanet_path:
            raise RuntimeError("EPANET DLL non trouvée")
        
        try:
            self.lib = ctypes.CDLL(self.epanet_path)
            print(f"✅ EPANET DLL chargée : {self.epanet_path}")
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement d'EPANET : {e}")
    
    def _define_function_prototypes(self):
        """Définit les prototypes des fonctions EPANET"""
        if not self.lib:
            return
            
        # Fonctions de base
        self.lib.ENopen.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.lib.ENopen.restype = ctypes.c_int
        
        self.lib.ENclose.argtypes = []
        self.lib.ENclose.restype = ctypes.c_int
        
        self.lib.ENsolveH.argtypes = []
        self.lib.ENsolveH.restype = ctypes.c_int
        
        self.lib.ENsaveH.argtypes = []
        self.lib.ENsaveH.restype = ctypes.c_int
        
        # Fonctions de récupération de données
        self.lib.ENgetcount.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self.lib.ENgetcount.restype = ctypes.c_int
        
        # Fonctions pour les nœuds
        self.lib.ENgetnodeid.argtypes = [ctypes.c_int, ctypes.c_char_p]
        self.lib.ENgetnodeid.restype = ctypes.c_int
        
        self.lib.ENgetnodeindex.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        self.lib.ENgetnodeindex.restype = ctypes.c_int
        
        self.lib.ENgetnodevalue.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
        self.lib.ENgetnodevalue.restype = ctypes.c_int
        
        # Fonctions pour les conduites
        self.lib.ENgetlinkid.argtypes = [ctypes.c_int, ctypes.c_char_p]
        self.lib.ENgetlinkid.restype = ctypes.c_int
        
        self.lib.ENgetlinkindex.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        self.lib.ENgetlinkindex.restype = ctypes.c_int
        
        self.lib.ENgetlinkvalue.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
        self.lib.ENgetlinkvalue.restype = ctypes.c_int
        
        # Fonctions d'erreur
        self.lib.ENgeterror.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
        self.lib.ENgeterror.restype = ctypes.c_int
    
    def open_project(self, inp_file: str, rpt_file: str = None, out_file: str = None) -> bool:
        """
        Ouvre un projet EPANET.
        
        Args:
            inp_file: Fichier d'entrée .inp
            rpt_file: Fichier de rapport (optionnel)
            out_file: Fichier de sortie (optionnel)
            
        Returns:
            bool: True si succès
        """
        if not self.lib:
            print("❌ EPANET DLL non chargée")
            return False
            
        if not rpt_file:
            rpt_file = inp_file.replace(".inp", ".rpt")
        if not out_file:
            out_file = inp_file.replace(".inp", ".out")
        
        # Convertir en bytes pour ctypes
        inp_bytes = inp_file.encode('ascii')
        rpt_bytes = rpt_file.encode('ascii')
        out_bytes = out_file.encode('ascii')
        
        error_code = self.lib.ENopen(inp_bytes, rpt_bytes, out_bytes)
        
        if error_code != 0:
            self._handle_error(error_code)
            return False
        
        print(f"✅ Projet EPANET ouvert : {inp_file}")
        return True
    
    def solve_hydraulics(self) -> bool:
        """
        Exécute la simulation hydraulique.
        
        Returns:
            bool: True si succès
        """
        if not self.lib:
            print("❌ EPANET DLL non chargée")
            return False
            
        error_code = self.lib.ENsolveH()
        
        if error_code != 0:
            self._handle_error(error_code)
            return False
        
        print("✅ Simulation hydraulique terminée")
        return True
    
    def save_results(self) -> bool:
        """
        Sauvegarde les résultats.
        
        Returns:
            bool: True si succès
        """
        if not self.lib:
            print("❌ EPANET DLL non chargée")
            return False
            
        error_code = self.lib.ENsaveH()
        
        if error_code != 0:
            self._handle_error(error_code)
            return False
        
        print("✅ Résultats sauvegardés")
        return True
    
    def close_project(self):
        """Ferme le projet EPANET"""
        if self.lib:
            self.lib.ENclose()
            print("✅ Projet EPANET fermé")
    
    def get_network_summary(self) -> Dict[str, int]:
        """
        Récupère le résumé du réseau.
        
        Returns:
            Dict: Nombre de nœuds, conduites, etc.
        """
        if not self.lib:
            return {"nodes": 0, "links": 0}
            
        summary = {}
        
        # Nombre de nœuds
        node_count = ctypes.c_int()
        error_code = self.lib.ENgetcount(self.EN_NODE, ctypes.byref(node_count))
        if error_code == 0:
            summary['nodes'] = node_count.value
        
        # Nombre de conduites
        link_count = ctypes.c_int()
        error_code = self.lib.ENgetcount(self.EN_LINK, ctypes.byref(link_count))
        if error_code == 0:
            summary['links'] = link_count.value
        
        return summary
    
    def get_node_ids(self) -> List[str]:
        """
        Récupère tous les IDs des nœuds.
        
        Returns:
            List[str]: Liste des IDs des nœuds
        """
        if not self.lib:
            return []
            
        node_count = self.get_network_summary()['nodes']
        node_ids = []
        
        # Buffer pour récupérer les IDs
        buffer = ctypes.create_string_buffer(32)
        
        for i in range(1, node_count + 1):
            error_code = self.lib.ENgetnodeid(i, buffer)
            if error_code != 0:
                self._handle_error(error_code)
                continue
            
            node_ids.append(buffer.value.decode('ascii'))
        
        return node_ids
    
    def get_link_ids(self) -> List[str]:
        """
        Récupère tous les IDs des conduites.
        
        Returns:
            List[str]: Liste des IDs des conduites
        """
        if not self.lib:
            return []
            
        link_count = self.get_network_summary()['links']
        link_ids = []
        
        # Buffer pour récupérer les IDs
        buffer = ctypes.create_string_buffer(32)
        
        for i in range(1, link_count + 1):
            error_code = self.lib.ENgetlinkid(i, buffer)
            if error_code != 0:
                self._handle_error(error_code)
                continue
            
            link_ids.append(buffer.value.decode('ascii'))
        
        return link_ids
    
    def get_node_pressures(self) -> Dict[str, float]:
        """
        Récupère les pressions de tous les nœuds.
        
        Returns:
            Dict[str, float]: Pressions par nœud
        """
        if not self.lib:
            return {}
            
        node_ids = self.get_node_ids()
        pressures = {}
        
        for node_id in node_ids:
            # Obtenir l'index du nœud
            node_index = ctypes.c_int()
            error_code = self.lib.ENgetnodeindex(node_id.encode('ascii'), ctypes.byref(node_index))
            if error_code != 0:
                self._handle_error(error_code)
                continue
            
            # Obtenir la pression
            pressure = ctypes.c_float()
            error_code = self.lib.ENgetnodevalue(node_index.value, self.EN_PRESSURE, ctypes.byref(pressure))
            if error_code != 0:
                self._handle_error(error_code)
                continue
            
            pressures[node_id] = pressure.value
        
        return pressures
    
    def get_link_flows(self) -> Dict[str, float]:
        """
        Récupère les débits de toutes les conduites.
        
        Returns:
            Dict[str, float]: Débits par conduite
        """
        if not self.lib:
            return {}
            
        link_ids = self.get_link_ids()
        flows = {}
        
        for link_id in link_ids:
            # Obtenir l'index de la conduite
            link_index = ctypes.c_int()
            error_code = self.lib.ENgetlinkindex(link_id.encode('ascii'), ctypes.byref(link_index))
            if error_code != 0:
                self._handle_error(error_code)
                continue
            
            # Obtenir le débit
            flow = ctypes.c_float()
            error_code = self.lib.ENgetlinkvalue(link_index.value, self.EN_FLOW, ctypes.byref(flow))
            if error_code != 0:
                self._handle_error(error_code)
                continue
            
            flows[link_id] = flow.value
        
        return flows
    
    def _handle_error(self, error_code: int):
        """Gère les erreurs EPANET"""
        if self.lib:
            error_msg = ctypes.create_string_buffer(256)
            self.lib.ENgeterror(error_code, error_msg, 256)
            error_text = error_msg.value.decode('ascii')
            print(f"❌ Erreur EPANET {error_code}: {error_text}")
        else:
            print(f"❌ Erreur EPANET {error_code}: DLL non chargée")


"""
Compteurs globaux de simulation pour diagnostic et traçabilité.
"""
_SIM_CALLS: int = 0
_SIM_TIME_SECONDS: float = 0.0

def _record_simulation_stats(duration_s: float) -> None:
    global _SIM_CALLS, _SIM_TIME_SECONDS
    try:
        _SIM_CALLS += 1
        _SIM_TIME_SECONDS += float(duration_s or 0.0)
    except Exception:
        pass

def reset_simulation_stats() -> None:
    global _SIM_CALLS, _SIM_TIME_SECONDS
    _SIM_CALLS = 0
    _SIM_TIME_SECONDS = 0.0

def get_simulation_stats() -> Dict[str, Any]:
    return {"calls": _SIM_CALLS, "time_seconds": _SIM_TIME_SECONDS}


class EPANETOptimizer:
    """Wrapper EPANET unifié basé sur wntr, avec retries et archivage pour l'optimisation.

    backend:
        - 'wntr' (défaut): utilise WNTR (EpanetSimulator/EPANETSimulator/WNTRSimulator)
        - 'dll' : applique les modifications via wntr puis exécute la DLL EPANET (ctypes)
    """
    
    def __init__(self, wntr_lib: Optional[Any] = None, backend: str = "wntr"):
        if not WNTR_AVAILABLE:
            raise ImportError("La librairie `wntr` est requise. Veuillez l'installer avec `pip install wntr`.")
        
        self.wntr = wntr_lib or wntr
        self.backend = (backend or "wntr").lower()
        
    def simulate(
        self,
        network_path: Union[Path, str],
        H_tank_map: Optional[Dict[str, float]] = None,
        diameters_map: Optional[Dict[str, int]] = None,
        duration_h: int = 24,
        timestep_min: int = 5,
        timeout_s: int = 60,
        num_retries: int = 2,
        output_dir: Optional[Path] = None,
        progress_callback: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    ) -> Dict[str, Any]:
        """
        Simule un fichier INP avec modifications, retries, et archivage.
        
        Args:
            network_path: Chemin vers le fichier .inp
            H_tank_map: Mapping {tank_id: hauteur_m} pour modifier les réservoirs
            diameters_map: Mapping {link_id: diametre_mm} pour modifier les conduites
            duration_h: Durée de simulation en heures
            timestep_min: Pas de temps en minutes
            timeout_s: Timeout en secondes
            num_retries: Nombre de tentatives en cas d'échec
            output_dir: Dossier de sortie pour l'archivage
            
        Returns:
            Dictionnaire avec les résultats de simulation
        """
        H_tank_map = H_tank_map or {}
        diameters_map = diameters_map or {}
        network_path = Path(network_path)

        try:
            model = self.wntr.network.WaterNetworkModel(str(network_path))
        except Exception as e:
            return {"success": False, "error": f"Chargement INP échoué: {e}"}

        # Appliquer les modifications au modèle wntr
        self._apply_modifications(model, H_tank_map, diameters_map, duration_h, timestep_min)

        # Préparer le dossier d'archivage
        archive_dir = self._prepare_archive_dir(output_dir)
        modified_inp_path = archive_dir / f"{network_path.stem}_modified.inp"

        # Écriture du fichier INP modifié (compatibilité wntr) — best effort, ne bloque pas la simulation
        try:
            if hasattr(model, 'write_inpfile'):
                model.write_inpfile(str(modified_inp_path))
            else:
                try:
                    from wntr.epanet.io import InpFile
                    InpFile().write(model, str(modified_inp_path))
                except Exception:
                    pass
        except Exception:
            # On ignore l'écriture d'archive si non supportée
            pass

        @retry(
            stop=stop_after_attempt(num_retries + 1),
            wait=wait_fixed(2),
            retry=retry_if_exception_type((TimeoutError, IOError)),
        )
        def _run_simulation_with_retry():
            # backend DLL : écrire l'INP modifié puis exécuter via EpanetSimulator
            if self.backend == "dll":
                try:
                    modified_inp_path = archive_dir / f"{network_path.stem}_modified_for_dll.inp"
                    # Toujours ré-écrire le modèle avec les modifs
                    try:
                        if hasattr(model, 'write_inpfile'):
                            model.write_inpfile(str(modified_inp_path))
                        else:
                            from wntr.epanet.io import InpFile
                            InpFile().write(model, str(modified_inp_path))
                    except Exception:
                        # Si écriture impossible, lever pour retry
                        raise IOError("Ecriture INP modifié échouée")

                    from .epanet_wrapper import EpanetSimulator as _DllSim  # self module
                    dll = _DllSim()
                    t0 = time.time()
                    if not dll.open_project(str(modified_inp_path)):
                        raise IOError("Ouverture projet DLL échouée")
                    try:
                        if not dll.solve_hydraulics():
                            raise IOError("Simulation hydraulique DLL échouée")
                        # Extraire pression/débits pour composer un payload comparable
                        pressures = dll.get_node_pressures()
                        flows = dll.get_link_flows()
                    finally:
                        dll.close_project()
                    dt = time.time() - t0

                    # Construire un payload minimal similaire
                    # Vitesse/charges/pertes non disponibles directement via DLL wrapper simplifié
                    # On renvoie au moins pressions et quelques agrégats
                    min_p = min(pressures.values()) if pressures else 0.0
                    extracted = {
                        "success": True,
                        "pressures": pressures,
                        "pressures_m": pressures,
                        "flows_m3_s": flows,
                        "min_pressure_m": float(min_p),
                        "max_velocity_m_s": 0.0,
                        "archive_path": str(archive_dir),
                        "simulator": "EpanetDLL",
                        "sim_time_seconds": round(float(dt), 6),
                    }
                    _record_simulation_stats(dt)
                    return extracted
                except Exception as e:
                    return {"success": False, "error": f"DLL backend failed: {e}", "archive_path": str(archive_dir)}

            # backend WNTR (défaut)
            else:
                # Choisir le simulateur disponible (EpanetSimulator ou WNTRSimulator)
                SimClass = getattr(self.wntr.sim, 'EpanetSimulator', None)
                if SimClass is None:
                    SimClass = getattr(self.wntr.sim, 'EPANETSimulator', None)
                if SimClass is None:
                    SimClass = getattr(self.wntr.sim, 'WNTRSimulator', None)
                if SimClass is None:
                    raise RuntimeError('Aucun simulateur wntr disponible (EpanetSimulator/WNTRSimulator)')

                simulator_name = getattr(SimClass, "__name__", str(SimClass))
                sim = SimClass(model)
                # Le préfixe de fichier pour les résultats est important pour l'archivage
                t0 = time.time()
                # event sim_start (best-effort)
                try:
                    from ..core.progress_ui import console as _c  # type: ignore
                    _ = _c  # silence linter
                except Exception:
                    pass
                # event sim_start (best-effort)
                try:
                    if callable(progress_callback):
                        sim_id = f"{int(time.time()*1000)}"
                        diam_hash = str(abs(hash(tuple(sorted(diameters_map.items()))))) if diameters_map else "0"
                        progress_callback(
                            "sim_start",
                            {
                                "sim_id": sim_id,
                                "worker": f"{_os.getpid()}:{_thr.get_ident()}",
                                "inp_path": str(network_path),
                                "diameter_map_hash": diam_hash,
                            },
                        )
                except Exception:
                    pass
                
                # Streaming des flux en temps réel si progress_callback fourni
                if callable(progress_callback):
                    try:
                        # Émettre des événements de progression pendant la simulation
                        self._emit_simulation_progress(model, progress_callback, sim_id)
                    except Exception as e:
                        logger.debug(f"Streaming des flux échoué: {e}")
                try:
                    results = sim.run_sim(file_prefix=str(archive_dir / "sim"))
                except TypeError:
                    # Anciennes signatures sans file_prefix
                    results = sim.run_sim()
                dt = time.time() - t0
                extracted = self._extract_results(model, results, archive_dir)
                try:
                    extracted["simulator"] = simulator_name
                    extracted["sim_time_seconds"] = round(float(dt), 6)
                except Exception:
                    pass
                _record_simulation_stats(dt)
                # event sim_done
                try:
                    if callable(progress_callback):
                        progress_callback(
                            "sim_done",
                            {
                                "sim_id": sim_id if 'sim_id' in locals() else "",
                                "worker": f"{_os.getpid()}:{_thr.get_ident()}",
                                "duration_s": float(dt),
                                "success": bool(extracted.get("success", True)),
                                "min_pressure": float(extracted.get("min_pressure_m", 0.0)),
                                "max_velocity": float(extracted.get("max_velocity_m_s", 0.0)),
                            },
                        )
                except Exception:
                    pass
                return extracted

        with ThreadPoolExecutor(max_workers=1) as ex:
            fut = ex.submit(_run_simulation_with_retry)
            try:
                final_results = fut.result(timeout=timeout_s * (num_retries + 1))
                final_results["archive_path"] = str(archive_dir)
                return final_results
            except TimeoutError:
                return {"success": False, "error": f"Timeout EPANET après {num_retries} tentatives", "archive_path": str(archive_dir)}
            except Exception as e:
                return {"success": False, "error": f"Simulation EPANET échouée: {e}", "archive_path": str(archive_dir)}

    def simulate_with_tank_height(
        self, 
        network_model: Union[Dict, Any], 
        H_tank: float, 
        diameters: Dict[str, int],
        progress_callback: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    ) -> Dict[str, Any]:
        """
        Méthode de compatibilité avec l'ancien code d'optimisation.
        
        Args:
            network_model: Modèle réseau (YAML ou INP)
            H_tank: Hauteur du réservoir (m)
            diameters: Mapping {link_id: diameter_mm}
            
        Returns:
            Résultats de simulation avec pressions et vitesses
        """
        # Si c'est un NetworkModel Pydantic, extraire le chemin
        if hasattr(network_model, 'dict'):
            # C'est un modèle Pydantic, on simule avec des valeurs par défaut
            return self._simulate_mock_network(network_model, H_tank, diameters)
        
        # Sinon, traiter comme un chemin de fichier
        network_path = network_model if isinstance(network_model, (str, Path)) else str(network_model)
        H_tank_map = {"tank1": H_tank}  # Nom par défaut du tank
        
        results = self.simulate(
            network_path=network_path,
            H_tank_map=H_tank_map,
            diameters_map=diameters,
            duration_h=1,  # Simulation courte pour l'optimisation
            timestep_min=5,
            timeout_s=30,
            progress_callback=progress_callback,
        )
        
        if results.get("success"):
            return {
                "pressures": results.get("pressures", {}),
                "velocities": results.get("velocities", {}),
                "min_pressure_m": results.get("min_pressure_m", 0.0),
                "max_velocity_m_s": results.get("max_velocity_m_s", 0.0)
            }
        else:
            return {
                "pressures": {},
                "velocities": {},
                "min_pressure_m": 0.0,
                "max_velocity_m_s": 0.0,
                "error": results.get("error", "Simulation échouée")
            }

    def _apply_modifications(self, model: Any, H_tank_map: Dict, diameters_map: Dict, duration_h: int, timestep_min: int):
        """Applique les modifications au modèle wntr."""
        # Modifier les réservoirs (robuste aux différentes API wntr)
        for tank_id, height in H_tank_map.items():
            try:
                # Vérifier présence du tank
                has_tank = False
                if hasattr(model, 'tank_name_list'):
                    try:
                        has_tank = tank_id in set(model.tank_name_list)
                    except Exception:
                        has_tank = False
                elif isinstance(getattr(model, 'tanks', None), dict):
                    try:
                        has_tank = tank_id in model.tanks
                    except Exception:
                        has_tank = False
                else:
                    # Fallback: si le nœud existe, tenter la modification directe
                    has_tank = isinstance(getattr(model, 'nodes', None), dict) and tank_id in model.nodes

                if not has_tank:
                    continue

                node_obj = None
                if hasattr(model, 'get_node'):
                    try:
                        node_obj = model.get_node(tank_id)
                    except Exception:
                        node_obj = None
                if node_obj is None and isinstance(getattr(model, 'nodes', None), dict):
                    node_obj = model.nodes.get(tank_id)

                if node_obj is not None and hasattr(node_obj, 'elevation'):
                    node_obj.elevation = height
            except Exception:
                # Continuer sans interrompre
                pass
        
        # Modifier les diamètres des conduites (si l'objet lien a un attribut diameter)
        for link_id, diameter in diameters_map.items():
            try:
                link_obj = None
                if hasattr(model, 'get_link'):
                    try:
                        link_obj = model.get_link(link_id)
                    except Exception:
                        link_obj = None
                if link_obj is None:
                    # Essayer via maps
                    links_map = getattr(model, 'links', None)
                    if isinstance(links_map, dict):
                        link_obj = links_map.get(link_id)
                    if link_obj is None:
                        pipes_map = getattr(model, 'pipes', None)
                        if isinstance(pipes_map, dict):
                            link_obj = pipes_map.get(link_id)
                if link_obj is not None and hasattr(link_obj, 'diameter'):
                    link_obj.diameter = float(diameter) / 1000.0  # mm -> m
            except Exception:
                pass
        
        # Modifier la durée et le pas de temps
        model.options.time.duration = duration_h * 3600  # heures -> secondes
        model.options.time.hydraulic_timestep = timestep_min * 60  # minutes -> secondes

    def _prepare_archive_dir(self, output_dir: Optional[Path]) -> Path:
        """Prépare le dossier d'archivage pour les simulations."""
        if output_dir:
            archive_dir = output_dir / "epanet_archive"
        else:
            archive_dir = Path("temp") / "epanet_archive"
        
        archive_dir.mkdir(parents=True, exist_ok=True)
        return archive_dir

    def _extract_results(self, model: Any, results: Any, archive_dir: Path) -> Dict[str, Any]:
        """Extrait les résultats de simulation wntr (robuste aux variations d'API)."""
        try:
            # Accès robuste aux structures de résultats
            node_block = getattr(results, "node", None)
            if callable(node_block):
                node_block = node_block()
            link_block = getattr(results, "link", None)
            if callable(link_block):
                link_block = link_block()

            # Récupérer DataFrames
            pressure_df = None
            velocity_df = None
            if isinstance(node_block, dict):
                pressure_df = node_block.get("pressure")
            elif node_block is not None:
                pressure_df = getattr(node_block, "pressure", None)

            if isinstance(link_block, dict):
                velocity_df = link_block.get("velocity")
            elif link_block is not None:
                velocity_df = getattr(link_block, "velocity", None)

            # Extraire les pressions et charges (head) aux nœuds
            pressures: Dict[str, float] = {}
            heads: Dict[str, float] = {}
            if pressure_df is not None:
                try:
                    cols = set(getattr(pressure_df, "columns", []))
                    for node_id in model.nodes:
                        if node_id in cols:
                            pressures[node_id] = float(pressure_df.loc[:, node_id].min())
                except Exception:
                    pass
            head_df = None
            if isinstance(node_block, dict):
                head_df = node_block.get("head")
            elif node_block is not None:
                head_df = getattr(node_block, "head", None)
            if head_df is not None:
                try:
                    cols = set(getattr(head_df, "columns", []))
                    for node_id in model.nodes:
                        if node_id in cols:
                            # prendre la moyenne de la charge
                            heads[node_id] = float(head_df.loc[:, node_id].mean())
                except Exception:
                    pass
            
            # Extraire les vitesses, pertes de charge et débits dans les conduites
            velocities: Dict[str, float] = {}
            if velocity_df is not None:
                try:
                    cols = list(getattr(velocity_df, "columns", []))
                    # Correspondance stricte sur les IDs de conduites
                    try:
                        for link_id in model.pipes:
                            if link_id in cols:
                                velocities[link_id] = float(velocity_df.loc[:, link_id].max())
                    except Exception:
                        pass
                    # Fallback: si aucune correspondance stricte, utiliser toutes les colonnes
                    if not velocities:
                        for col in cols:
                            try:
                                velocities[str(col)] = float(velocity_df.loc[:, col].max())
                            except Exception:
                                continue
                except Exception:
                    pass
            headloss_df = None
            flow_df = None
            if isinstance(link_block, dict):
                headloss_df = link_block.get("headloss")
                _flowrate = link_block.get("flowrate")
                if _flowrate is not None:
                    flow_df = _flowrate
                else:
                    flow_df = link_block.get("flow")
            elif link_block is not None:
                headloss_df = getattr(link_block, "headloss", None)
                _flowrate = getattr(link_block, "flowrate", None)
                if _flowrate is not None:
                    flow_df = _flowrate
                else:
                    flow_df = getattr(link_block, "flow", None)

            headlosses: Dict[str, float] = {}
            if headloss_df is not None:
                try:
                    cols = list(getattr(headloss_df, "columns", []))
                    try:
                        for link_id in model.pipes:
                            if link_id in cols:
                                headlosses[link_id] = float(headloss_df.loc[:, link_id].mean())
                    except Exception:
                        pass
                    # Fallback: toutes colonnes si aucune correspondance
                    if not headlosses:
                        for col in cols:
                            try:
                                headlosses[str(col)] = float(headloss_df.loc[:, col].mean())
                            except Exception:
                                continue
                except Exception:
                    pass

            flows: Dict[str, float] = {}
            if flow_df is not None:
                try:
                    cols = list(getattr(flow_df, "columns", []))
                    try:
                        for link_id in model.pipes:
                            if link_id in cols:
                                # Débit moyen en m3/s
                                flows[link_id] = float(flow_df.loc[:, link_id].mean())
                    except Exception:
                        pass
                    # Fallback: toutes colonnes si aucune correspondance
                    if not flows:
                        for col in cols:
                            try:
                                flows[str(col)] = float(flow_df.loc[:, col].mean())
                            except Exception:
                                continue
                except Exception:
                    pass
            
            # Aliases standardisés pour compatibilité inter-solveurs
            pressures_m = pressures
            velocities_m_s = velocities
            heads_m = heads
            headlosses_m = headlosses

            # Calcul de la pression minimale uniquement sur les jonctions (exclure réservoirs/cuves)
            try:
                junction_ids = set(model.junction_name_list) if hasattr(model, 'junction_name_list') else set(model.nodes.keys())
            except Exception:
                junction_ids = set(model.nodes.keys()) if hasattr(model, 'nodes') else set()
            pressures_junctions = {nid: p for nid, p in pressures.items() if nid in junction_ids}

            # Détection du modèle de pertes (heuristique)
            headloss_model = "unknown"
            try:
                hyd_opt = getattr(getattr(model, 'options', None), 'hydraulic', None)
                if hyd_opt is not None:
                    hl = getattr(hyd_opt, 'headloss', None)
                    if hl:
                        headloss_model = str(hl).lower()
                if headloss_model == "unknown":
                    has_hw = False
                    has_dw = False
                    for pid in getattr(model, 'pipe_name_list', []):
                        try:
                            p = model.get_link(pid)
                            if hasattr(p, 'roughness') and p.roughness is not None:
                                has_dw = True
                            if hasattr(p, 'coeff') and p.coeff is not None:
                                has_hw = True
                        except Exception:
                            continue
                    headloss_model = 'hazen-williams' if has_hw else ('darcy-weisbach' if has_dw else headloss_model)
            except Exception:
                pass

            return {
                "success": True,
                # Clés historiques
                "pressures": pressures,
                "velocities": velocities,
                "heads": heads,
                "headlosses": headlosses,
                # Clés normalisées (unités explicites)
                "pressures_m": pressures_m,
                "velocities_m_s": velocities_m_s,
                "heads_m": heads_m,
                "headlosses_m": headlosses_m,
                # Débits déjà en m3/s
                "flows_m3_s": flows,
                # Agrégats (pression minimale filtrée sur JUNCTIONS)
                "min_pressure_m": min(pressures_junctions.values()) if pressures_junctions else (min(pressures.values()) if pressures else 0.0),
                "max_velocity_m_s": max(velocities.values()) if velocities else 0.0,
                "min_velocity_m_s": min(velocities.values()) if velocities else 0.0,
                "archive_path": str(archive_dir),
                "headloss_model": headloss_model,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Extraction des résultats échouée: {e}",
                "archive_path": str(archive_dir)
            }

    def _simulate_mock_network(self, network_model: Any, H_tank: float, diameters: Dict[str, int]) -> Dict[str, Any]:
        """Simulation mock pour les modèles réseau sans fichier INP."""
        # Simulation simple basée sur la hauteur du réservoir
        mock_pressures = {}
        mock_velocities = {}
        
        # Générer des pressions mock basées sur la hauteur
        for node_id in getattr(network_model, 'nodes', {}):
            mock_pressures[node_id] = H_tank - 5.0  # Pression = hauteur - pertes
        
        # Générer des vitesses mock basées sur les diamètres
        for link_id, diameter in diameters.items():
            mock_velocities[link_id] = 1.0 + (diameter / 1000.0)  # Vitesse basée sur diamètre
        
        return {
            "pressures": mock_pressures,
            "velocities": mock_velocities,
            "min_pressure_m": min(mock_pressures.values()) if mock_pressures else 0.0,
            "max_velocity_m_s": max(mock_velocities.values()) if mock_velocities else 0.0
        }
    
    def _emit_simulation_progress(self, model, progress_callback, sim_id):
        """
        Émet des événements de progression pendant la simulation pour le streaming des flux.
        
        Args:
            model: Modèle WNTR du réseau
            progress_callback: Callback pour émettre les événements
            sim_id: ID de la simulation
        """
        try:
            # Émettre un événement de progression toutes les 100ms
            import time
            import threading
            
            def _progress_worker():
                try:
                    # Simuler des étapes de progression
                    for step in range(10):
                        time.sleep(0.1)  # 100ms entre chaque étape
                        
                        # Calculer les débits actuels (simulation)
                        flows = {}
                        total_flow = 0.0
                        
                        # Extraire les débits des liens
                        for link_name, link in model.links():
                            # Estimation des débits basée sur la topologie
                            flow = 0.1 + (step * 0.05)  # Simulation progressive
                            flows[link_name] = flow
                            total_flow += abs(flow)
                        
                        # Émettre l'événement de progression
                        progress_callback(
                            "simulation_step",
                            {
                                "sim_id": sim_id,
                                "step": step,
                                "total_steps": 10,
                                "flows": flows,
                                "total_flow": total_flow,
                                "timestamp": time.time()
                            }
                        )
                        
                except Exception as e:
                    logger.debug(f"Erreur dans le worker de progression: {e}")
            
            # Démarrer le worker en arrière-plan
            progress_thread = threading.Thread(target=_progress_worker, daemon=True)
            progress_thread.start()
            
        except Exception as e:
            logger.debug(f"Impossible d'émettre la progression: {e}")


def create_epanet_inp_file(network_data: Dict[str, Any], output_path: str) -> bool:
    """
    Crée un fichier .inp EPANET avec des validations de cohérence renforcées.
    
    Args:
        network_data: Données du réseau au format LCPI
        output_path: Chemin du fichier .inp à créer
        
    Returns:
        bool: True si succès, False sinon
    """
    try:
        # Données de base
        nodes_data = network_data.get("network", {}).get("nodes", {})
        pipes_data = network_data.get("network", {}).get("pipes", {})
        
        # Extraire tous les IDs uniques de Nœuds et de Conduites
        all_node_ids = set()
        all_pipe_ids = set(pipes_data.keys())
        
        for pipe_data in pipes_data.values():
            node1 = pipe_data.get("from")
            node2 = pipe_data.get("to")
            if node1 is not None: all_node_ids.add(node1)
            if node2 is not None: all_node_ids.add(node2)
        
        # Vérification des IDs dupliqués entre types
        id_intersection = all_node_ids.intersection(all_pipe_ids)
        if id_intersection:
            print(f"❌ ERREUR FATALE : Les IDs suivants sont utilisés à la fois pour des nœuds et des conduites : {id_intersection}")
            return False

        # Identifier les réservoirs et les jonctions (nœuds simples)
        existing_nodes = set(nodes_data.keys())
        reservoirs = set()
        for node_id, node_data in nodes_data.items():
            if node_data.get("type") == "reservoir":
                reservoirs.add(node_id)
        
        # Les jonctions sont tous les nœuds qui ne sont pas des réservoirs
        junctions = all_node_ids - reservoirs
        
        # Les nœuds manquants sont ceux qui ne sont ni dans les données, ni des réservoirs
        missing_junctions = junctions - existing_nodes
        if missing_junctions:
            print(f"⚠️ Nœuds de jonction manquants détectés et seront ajoutés avec des valeurs par défaut : {missing_junctions}")

        # --- Écriture du fichier ---
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("[TITLE]\nLCPI Network Analysis - Robust\n\n")

            # [JUNCTIONS]
            f.write("[JUNCTIONS]\n;ID\tElev\tDemand\n")
            # Écrire les jonctions définies
            for node_id in sorted(list(junctions.intersection(existing_nodes))):
                node_data = nodes_data[node_id]
                elevation = node_data.get("elevation", 50)
                demand = node_data.get("demand", 0)
                f.write(f"{node_id}\t{elevation}\t{demand}\n")
            
            # Écrire les jonctions manquantes
            for node_id in sorted(list(missing_junctions)):
                f.write(f"{node_id}\t50\t0\n") # Valeurs par défaut
            f.write("\n")

            # [RESERVOIRS]
            if reservoirs:
                f.write("[RESERVOIRS]\n;ID\tHead\n")
                for node_id in sorted(list(reservoirs)):
                    head = nodes_data[node_id].get("elevation", 50)
                    f.write(f"{node_id}\t{head}\n")
                f.write("\n")

            # [PIPES]
            f.write("[PIPES]\n;ID\tNode1\tNode2\tLength\tDiameter\tRoughness\tMinorLoss\tStatus\n")
            valid_pipes_count = 0
            for pipe_id, pipe_data in pipes_data.items():
                node1 = pipe_data.get("from")
                node2 = pipe_data.get("to")
                
                # Validation de la cohérence de chaque conduite
                if not node1 or not node2 or node1 not in all_node_ids or node2 not in all_node_ids:
                    print(f"⚠️ Conduite '{pipe_id}' ignorée car ses nœuds sont invalides ou manquants.")
                    continue

                length = pipe_data.get("length", 100)
                diameter = pipe_data.get("diameter", 150)

                if length <= 0 or diameter <= 0:
                    print(f"⚠️ Conduite '{pipe_id}' ignorée car ses dimensions sont invalides (longueur/diamètre <= 0).")
                    continue
                
                roughness = pipe_data.get("roughness", 100)
                f.write(f"{pipe_id}\t{node1}\t{node2}\t{length}\t{diameter}\t{roughness}\t0\tOpen\n")
                valid_pipes_count += 1
            
            print(f"✅ {valid_pipes_count} conduites valides écrites sur {len(pipes_data)} total")
            f.write("\n")
            
            # Sections EPANET standard
            f.write("[OPTIONS]\nUNITS\tLPS\nHEADLOSS\tH-W\n\n")
            f.write("[TIMES]\nDURATION\t0\n\n")
            f.write("[REPORT]\nSTATUS\tNO\n\n")
            f.write("[END]")

        print(f"✅ Fichier .inp robuste généré : {output_path}")
        return True

    except Exception as e:
        print(f"❌ Erreur critique lors de la création du fichier .inp robuste : {e}")
        return False


def validate_hardy_cross_with_epanet(network_data: Dict[str, Any], 
                                   hardy_cross_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les résultats Hardy-Cross avec EPANET.
    
    Args:
        network_data: Données du réseau
        hardy_cross_results: Résultats Hardy-Cross
        
    Returns:
        Dict: Résultats de validation
    """
    # Créer le fichier .inp
    temp_inp = "temp_validation.inp"
    if not create_epanet_inp_file(network_data, temp_inp):
        return {"error": "Impossible de créer le fichier .inp"}
    
    # Variable pour suivre le succès
    success = False
    
    try:
        # Initialiser EPANET
        epanet = EpanetSimulator()
        
        # Ouvrir le projet
        if not epanet.open_project(temp_inp):
            return {"error": "Impossible d'ouvrir le projet EPANET"}
        
        # Exécuter la simulation
        if not epanet.solve_hydraulics():
            return {"error": "Échec de la simulation EPANET"}
        
        # Sauvegarder les résultats
        if not epanet.save_results():
            return {"error": "Impossible de sauvegarder les résultats"}
        
        # Récupérer les résultats
        epanet_pressures = epanet.get_node_pressures()
        epanet_flows = epanet.get_link_flows()
        
        # Fermer le projet
        epanet.close_project()
        
        # Comparer avec Hardy-Cross
        comparison = {
            "hardy_cross": hardy_cross_results,
            "epanet": {
                "pressions": epanet_pressures,
                "debits": epanet_flows
            },
            "validation": {
                "status": "unknown",
                "pressure_differences": [],
                "flow_differences": [],
                "pressure_similarities": [],
                "flow_similarities": []
            }
        }
        
        # Comparer les pressions
        hc_pressures = hardy_cross_results.get("pressions", {})
        for node_id, ep_pressure in epanet_pressures.items():
            hc_pressure = hc_pressures.get(node_id)
            if hc_pressure is not None:
                diff = abs(hc_pressure - ep_pressure)
                if diff < 0.1:  # Tolérance de 0.1 m
                    comparison["validation"]["pressure_similarities"].append({
                        "node": node_id,
                        "hardy_cross": hc_pressure,
                        "epanet": ep_pressure,
                        "difference": diff
                    })
                else:
                    comparison["validation"]["pressure_differences"].append({
                        "node": node_id,
                        "hardy_cross": hc_pressure,
                        "epanet": ep_pressure,
                        "difference": diff
                    })
        
        # Comparer les débits
        hc_flows = hardy_cross_results.get("debits", {})
        for link_id, ep_flow in epanet_flows.items():
            hc_flow = hc_flows.get(link_id)
            if hc_flow is not None:
                diff = abs(hc_flow - ep_flow)
                if diff < 0.01:  # Tolérance de 0.01 L/s
                    comparison["validation"]["flow_similarities"].append({
                        "link": link_id,
                        "hardy_cross": hc_flow,
                        "epanet": ep_flow,
                        "difference": diff
                    })
                else:
                    comparison["validation"]["flow_differences"].append({
                        "link": link_id,
                        "hardy_cross": hc_flow,
                        "epanet": ep_flow,
                        "difference": diff
                    })
        
        # Déterminer le statut global
        if (comparison["validation"]["pressure_differences"] or 
            comparison["validation"]["flow_differences"]):
            comparison["validation"]["status"] = "differences_found"
        elif (comparison["validation"]["pressure_similarities"] or 
              comparison["validation"]["flow_similarities"]):
            comparison["validation"]["status"] = "validated"
        else:
            comparison["validation"]["status"] = "no_comparison_data"
        
        # Si tout se passe bien jusqu'à la fin
        success = True
        return comparison
        
    except Exception as e:
        return {"error": f"Erreur lors de la validation : {e}"}
    finally:
        # Ne nettoyer le fichier temporaire que si tout a réussi
        if success and os.path.exists(temp_inp):
            os.remove(temp_inp)
        else:
            print(f"ℹ️ Le fichier d'entrée problématique a été conservé pour inspection : {temp_inp}")


# Instance globale du wrapper
_epanet_wrapper = None

def get_epanet_wrapper() -> EpanetWrapper:
    """
    Retourne l'instance globale du wrapper EPANET.
    
    Returns:
        Instance du wrapper EPANET
    """
    global _epanet_wrapper
    if _epanet_wrapper is None:
        _epanet_wrapper = EpanetWrapper()
    return _epanet_wrapper

def is_epanet_available() -> bool:
    """
    Vérifie si EPANET est disponible.
    
    Returns:
        True si EPANET est disponible, False sinon
    """
    return get_epanet_wrapper().is_available()

def get_epanet_version() -> str:
    """
    Retourne la version d'EPANET.
    
    Returns:
        Version d'EPANET ou 'simulation_only'
    """
    return get_epanet_wrapper().get_version()
