"""
Wrapper EPANET pour l'intégration avec le système LCPI.

Ce module fournit une interface unifiée pour interagir avec EPANET,
gérant les cas où EPANET n'est pas disponible.
"""

import logging
import os
import sys
import ctypes
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import json
import yaml

logger = logging.getLogger(__name__)

# Flag pour indiquer si EPANET est disponible
EPANET_AVAILABLE = False

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
            num_nodes = en.ENgetcount(epanet.EN_NODECOUNT)
            for i in range(1, num_nodes + 1):
                node_id = en.ENgetnodeid(i)
                pressure = en.ENgetnodevalue(i, epanet.EN_PRESSURE)
                head = en.ENgetnodevalue(i, epanet.EN_HEAD)
                demand = en.ENgetnodevalue(i, epanet.EN_DEMAND)
                
                results["nodes"][node_id] = {
                    "pressure": pressure,
                    "head": head,
                    "demand": demand
                }
            
            # Informations sur les conduites
            num_pipes = en.ENgetcount(epanet.EN_LINKCOUNT)
            for i in range(1, num_pipes + 1):
                link_id = en.ENgetlinkid(i)
                link_type = en.ENgetlinktype(i)
                
                if link_type == epanet.EN_PIPE:
                    flow = en.ENgetlinkvalue(i, epanet.EN_FLOW)
                    velocity = en.ENgetlinkvalue(i, epanet.EN_VELOCITY)
                    headloss = en.ENgetlinkvalue(i, epanet.EN_HEADLOSS)
                    
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
