"""
Wrapper EPANET pour LCPI

Ce module fournit une interface Python pour EPANET 2.2,
permettant d'intégrer la simulation hydraulique dans LCPI.
"""

import os
import sys
import ctypes
import tempfile
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import yaml

# Import NetworkUtils avec fallback
try:
    from .core.network_utils import NetworkUtils
except ImportError:
    # Fallback pour les imports dynamiques
    import importlib.util
    current_dir = os.path.dirname(os.path.abspath(__file__))
    network_utils_path = os.path.join(current_dir, "core", "network_utils.py")
    
    spec = importlib.util.spec_from_file_location("network_utils", network_utils_path)
    if spec and spec.loader:
        network_utils_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(network_utils_module)
        NetworkUtils = network_utils_module.NetworkUtils
    else:
        raise ImportError("Impossible de charger network_utils")

class EpanetSimulator:
    """Wrapper pour EPANET 2.2 utilisant ctypes"""
    
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
        self._load_library()
        self._define_function_prototypes()
        
    def _find_epanet_dll(self) -> Optional[str]:
        """
        Recherche la DLL EPANET à utiliser (forcée sur la version 64 bits fournie).
        """
        # --- FORCE LE CHEMIN DE LA DLL 64 BITS ---
        forced_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../EPANET_2_3_1_WIN_32_64/64bit/epanet2.dll'))
        if os.path.exists(forced_path):
            print(f"[INFO] Utilisation forcée de la DLL EPANET 64 bits : {forced_path}")
            return forced_path
        # fallback: ancienne logique si besoin
        
        # Obtenir le répertoire du script actuel
        base_dir = Path(__file__).parent

        # --- MODIFIEZ CETTE LISTE ---
        # Liste des emplacements à vérifier, en ordre de priorité
        search_paths = [
            # 1. Priorité au dossier dédié dans notre projet
            base_dir / "epanet_lib",
            
            # 2. Anciens chemins pour la rétrocompatibilité
            "EPANET2.2-master",
            "epanet",
            "EPANET"
        ]
        
        for dir_path in search_paths:
            if Path(dir_path).exists():
                # Chercher les noms de DLL possibles
                for dll_name in ["epanet2.dll", "libepanet2.dll", "epanet22.dll"]:
                    dll_path = Path(dir_path) / dll_name
                    if dll_path.exists():
                        print(f"✅ DLL EPANET trouvée : {dll_path.resolve()}")
                        return str(dll_path.resolve())
        
        # Si rien n'est trouvé
        print("❌ DLL EPANET introuvable dans les chemins de recherche.")
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
        error_code = self.lib.ENsaveH()
        
        if error_code != 0:
            self._handle_error(error_code)
            return False
        
        print("✅ Résultats sauvegardés")
        return True
    
    def close_project(self):
        """Ferme le projet EPANET"""
        self.lib.ENclose()
        print("✅ Projet EPANET fermé")
    
    def get_network_summary(self) -> Dict[str, int]:
        """
        Récupère le résumé du réseau.
        
        Returns:
            Dict: Nombre de nœuds, conduites, etc.
        """
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
        error_msg = ctypes.create_string_buffer(256)
        self.lib.ENgeterror(error_code, error_msg, 256)
        error_text = error_msg.value.decode('ascii')
        print(f"❌ Erreur EPANET {error_code}: {error_text}")

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
        # --- AMÉLIORATION 1 : Collecte et Validation des Données en Amont ---
        
        # Données de base
        nodes_data = network_data.get("network", {}).get("nodes", {})
        pipes_data = network_data.get("network", {}).get("pipes", {})
        
        # Extraire tous les IDs uniques de Nœuds et de Conduites
        all_node_ids = set()
        all_pipe_ids = set(pipes_data.keys())
        
        for pipe_data in pipes_data.values():
            node1, node2 = NetworkUtils.get_pipe_nodes(pipe_data)
            if node1 is not None: all_node_ids.add(node1)
            if node2 is not None: all_node_ids.add(node2)
        
        # Vérification des IDs dupliqués entre types
        id_intersection = all_node_ids.intersection(all_pipe_ids)
        if id_intersection:
            print(f"❌ ERREUR FATALE : Les IDs suivants sont utilisés à la fois pour des nœuds et des conduites : {id_intersection}")
            return False

        # Identifier les réservoirs et les jonctions (nœuds simples)
        existing_nodes = set(nodes_data.keys())
        reservoirs = NetworkUtils.identify_water_sources(network_data)
        
        # Les jonctions sont tous les nœuds qui ne sont pas des réservoirs
        junctions = all_node_ids - reservoirs
        
        # Les nœuds manquants sont ceux qui ne sont ni dans les données, ni des réservoirs
        missing_junctions = junctions - existing_nodes
        if missing_junctions:
            print(f"⚠️ Nœuds de jonction manquants détectés et seront ajoutés avec des valeurs par défaut : {missing_junctions}")

        # --- Écriture du fichier ---
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("[TITLE]\nLCPI Network Analysis - Robust\n\n")

            # --- AMÉLIORATION 2 : Écriture Structurée des Sections ---
            
            # [JUNCTIONS]
            f.write("[JUNCTIONS]\n;ID\tElev\tDemand\n")
            # Écrire les jonctions définies
            for node_id in sorted(list(junctions.intersection(existing_nodes))):
                node_data = nodes_data[node_id]
                elevation = NetworkUtils.get_node_elevation(node_data)
                demand = NetworkUtils.get_node_demand(node_data)
                f.write(f"{node_id}\t{elevation}\t{demand}\n")
            
            # Écrire les jonctions manquantes
            for node_id in sorted(list(missing_junctions)):
                f.write(f"{node_id}\t50\t0\n") # Valeurs par défaut
            f.write("\n")

            # [RESERVOIRS]
            if reservoirs:
                f.write("[RESERVOIRS]\n;ID\tHead\n")
                for node_id in sorted(list(reservoirs)):
                    head = NetworkUtils.get_node_elevation(nodes_data[node_id])
                    f.write(f"{node_id}\t{head}\n")
                f.write("\n")

            # [PIPES]
            f.write("[PIPES]\n;ID\tNode1\tNode2\tLength\tDiameter\tRoughness\tMinorLoss\tStatus\n")
            valid_pipes_count = 0
            for pipe_id, pipe_data in pipes_data.items():
                node1, node2 = NetworkUtils.get_pipe_nodes(pipe_data)
                
                # --- AMÉLIORATION 3 : Validation de la cohérence de chaque conduite ---
                if not node1 or not node2 or node1 not in all_node_ids or node2 not in all_node_ids:
                    print(f"⚠️ Conduite '{pipe_id}' ignorée car ses nœuds sont invalides ou manquants.")
                    continue

                length = NetworkUtils.get_pipe_length(pipe_data)
                diameter = NetworkUtils.get_pipe_diameter(pipe_data)

                if length <= 0 or diameter <= 0:
                    print(f"⚠️ Conduite '{pipe_id}' ignorée car ses dimensions sont invalides (longueur/diamètre <= 0).")
                    continue
                
                roughness = NetworkUtils.get_pipe_roughness(pipe_data)
                f.write(f"{pipe_id}\t{node1}\t{node2}\t{length}\t{diameter}\t{roughness}\t0\tOpen\n")
                valid_pipes_count += 1
            
            print(f"✅ {valid_pipes_count} conduites valides écrites sur {len(pipes_data)} total")
            f.write("\n")
            
            # --- AMÉLIORATION 4 : Utilisation de sections EPANET standard ---
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
                "pressures": epanet_pressures,
                "flows": epanet_flows
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
        hc_pressures = hardy_cross_results.get("pressures", {})
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
        hc_flows = hardy_cross_results.get("flows", {})
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
        # --- MODIFICATION ---
        # Ne nettoyer le fichier temporaire que si tout a réussi
        if success and os.path.exists(temp_inp):
            os.remove(temp_inp)
        else:
            print(f"ℹ️ Le fichier d'entrée problématique a été conservé pour inspection : {temp_inp}") 