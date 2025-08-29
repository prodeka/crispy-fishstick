"""
Module d'entrée/sortie pour LCPI-AEP.

Ce module fournit des fonctions pour la conversion et la manipulation
des fichiers de réseau (INP, YAML, JSON).
"""

import time
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, Union
import yaml

try:
    import wntr  # type: ignore
    WNTR_AVAILABLE = True
except ImportError:
    WNTR_AVAILABLE = False


def convert_inp_to_unified_model(inp_path: Path) -> Dict[str, Any]:
    """
    Convertit un fichier .inp EPANET en modèle unifié.
    
    Args:
        inp_path: Chemin vers le fichier .inp
        
    Returns:
        Modèle unifié au format standard LCPI
    """
    try:
        if WNTR_AVAILABLE:
            # Utiliser WNTR pour une conversion riche
            wn = wntr.network.WaterNetworkModel(str(inp_path))
            nodes: Dict[str, Dict[str, Any]] = {}
            links: Dict[str, Dict[str, Any]] = {}
            tanks: Dict[str, Dict[str, Any]] = {}

            for name, j in wn.junctions():
                nodes[name] = {
                    "type": "junction",
                    "elevation_m": float(getattr(j, "elevation", 0.0)),
                    "base_demand_m3_s": float(getattr(j, "base_demand", 0.0)),
                }
            for name, t in wn.tanks():
                tanks[name] = {
                    "type": "tank",
                    "radier_elevation_m": float(getattr(t, "elevation", 0.0)),
                    "init_level_m": float(getattr(t, "init_level", 0.0)),
                    "min_level_m": float(getattr(t, "min_level", 0.0)),
                    "max_level_m": float(getattr(t, "max_level", 0.0)),
                }
            for name, l in wn.pipes():
                links[name] = {
                    "from": getattr(l, "start_node_name", None),
                    "to": getattr(l, "end_node_name", None),
                    "length_m": float(getattr(l, "length", 0.0)),
                    "diameter_mm": int(float(getattr(l, "diameter", 0.0)) * 1000.0) if getattr(l, "diameter", None) else None,
                    "roughness": float(getattr(l, "roughness", 130.0)),
                }

            return {
                "meta": {"source": "inp", "file": str(inp_path), "converted_at": time.time()},
                "nodes": nodes,
                "links": links,
                "tanks": tanks,
            }
        else:
            # Fallback: parse minimal de la section [PIPES]
            return _parse_inp_minimal(inp_path)
            
    except Exception as e:
        # Fallback: parse minimal
        return _parse_inp_minimal(inp_path)


def _parse_inp_minimal(inp_path: Path) -> Dict[str, Any]:
    """
    Parse minimal d'un fichier INP sans WNTR.
    
    Args:
        inp_path: Chemin vers le fichier .inp
        
    Returns:
        Modèle minimal extrait du fichier INP
    """
    try:
        text = inp_path.read_text(errors="ignore")
        links: Dict[str, Dict[str, Any]] = {}
        nodes: Dict[str, Dict[str, Any]] = {}
        tanks: Dict[str, Dict[str, Any]] = {}
        
        in_pipes = False
        in_junctions = False
        in_tanks = False
        
        for line in text.splitlines():
            s = line.strip()
            if not s or s.startswith(";"):
                continue
            if s.startswith("[PIPES]"):
                in_pipes = True
                in_junctions = False
                in_tanks = False
                continue
            elif s.startswith("[JUNCTIONS]"):
                in_pipes = False
                in_junctions = True
                in_tanks = False
                continue
            elif s.startswith("[TANKS]"):
                in_pipes = False
                in_junctions = False
                in_tanks = True
                continue
            elif s.startswith("["):
                in_pipes = False
                in_junctions = False
                in_tanks = False
                continue
            
            if in_pipes:
                parts = s.split()
                if len(parts) >= 4:
                    pipe_id = parts[0]
                    node1 = parts[1]
                    node2 = parts[2]
                    # CONVERSION AUTOMATIQUE : km -> m
                    length_km = float(parts[3])
                    length_m = length_km * 1000.0  # Convertir km en m
                    diameter = float(parts[4]) if len(parts) > 4 else 100.0
                    roughness = float(parts[5]) if len(parts) > 5 else 0.009
                    
                    links[pipe_id] = {
                        "from_node": node1,
                        "to_node": node2,
                        "length_m": length_m,  # Maintenant en mètres
                        "diameter_mm": diameter,
                        "roughness": roughness,
                        "type": "pipe"
                    }
                    
                    # Ajouter les nœuds s'ils n'existent pas
                    if node1 not in nodes:
                        nodes[node1] = {"type": "junction", "elevation": 0.0}
                    if node2 not in nodes:
                        nodes[node2] = {"type": "junction", "elevation": 0.0}
                        
            elif in_junctions:
                parts = s.split()
                if len(parts) >= 3:
                    node_id = parts[0]
                    elevation = float(parts[1])
                    demand = float(parts[2]) if len(parts) > 2 else 0.0
                    
                    nodes[node_id] = {
                        "type": "junction",
                        "elevation": elevation,
                        "demand": demand
                    }
                    
            elif in_tanks:
                parts = s.split()
                if len(parts) >= 3:
                    tank_id = parts[0]
                    elevation = float(parts[1])
                    H_tank = float(parts[2])
                    
                    tanks[tank_id] = {
                        "type": "tank",
                        "elevation": elevation,
                        "parametres": {"H_tank": H_tank},
                    }
        
        return {
            "meta": {"format": "inp"},
            "nodes": nodes,
            "links": links,
            "tanks": tanks
        }
        
    except Exception as e:
        print(f"Erreur lors du parsing INP minimal: {e}")
        return {
            "meta": {"format": "inp", "error": str(e)},
            "nodes": {},
            "links": {},
            "tanks": {}
        }


def load_yaml_or_inp(file_path: Union[str, Path]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Charge un fichier YAML ou INP et retourne le modèle et les métadonnées.
    
    Args:
        file_path: Chemin vers le fichier
        
    Returns:
        Tuple (modèle, métadonnées)
    """
    file_path = Path(file_path)
    
    if file_path.suffix.lower() == '.yml' or file_path.suffix.lower() == '.yaml':
        # Charger YAML
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data, {"format": "yaml", "source": str(file_path)}
        
    elif file_path.suffix.lower() == '.inp':
        # FORCER l'utilisation de notre parser personnalisé
        # wntr lit les longueurs en km comme des mètres, causant des coûts 1000x trop faibles
        print("🔧 Utilisation du parser INP personnalisé (conversion km -> m automatique)")
        model = _parse_inp_minimal(file_path)
        return model, {"format": "inp", "source": str(file_path), "parser": "custom"}
        
    else:
        raise ValueError(f"Format de fichier non supporté: {file_path.suffix}")


def convert_to_solver_network_data(
    network_model: Dict[str, Any],
    H_tank: float,
    diameters_mm_override: Optional[Dict[str, int]] = None,
) -> Dict[str, Any]:
    """
    Convertit le modèle réseau unifié vers le format attendu par les solveurs.
    
    Args:
        network_model: Modèle réseau au format unifié
        H_tank: Hauteur du réservoir en mètres
        diameters_mm_override: Surcharge des diamètres en mm
        
    Returns:
        Données au format attendu par les solveurs
    """
    noeuds: Dict[str, Any] = {}
    
    # Copier nœuds existants comme consommateurs par défaut
    for nid, n in (network_model.get("nodes") or {}).items():
        noeuds[nid] = {
            "role": n.get("role", "consommation"),
            "elevation_m": float(n.get("elevation_m", 0.0)),
            "demande_m3_s": float(n.get("base_demand_m3_s", 0.0)),
        }
    
    # Ajouter un réservoir à partir du premier tank
    if network_model.get("tanks"):
        tid, t = next(iter(network_model["tanks"].items()))
        noeuds[tid] = {
            "role": "reservoir",
            "elevation_m": float(t.get("radier_elevation_m", 0.0)),
            "H_tank_m": float(H_tank),
        }

    conduites: Dict[str, Any] = {}
    for lid, link in (network_model.get("links") or {}).items():
        d_mm = diameters_mm_override.get(lid) if diameters_mm_override else link.get("diameter_mm")
        conduites[lid] = {
            "noeud_amont": link.get("from") or link.get("node1") or link.get("noeud_amont"),
            "noeud_aval": link.get("to") or link.get("node2") or link.get("noeud_aval"),
            "longueur_m": float(link.get("length_m", 0.0)),
            "diametre_m": float(d_mm) / 1000.0 if d_mm else 0.0,
            "rugosite": float(link.get("roughness", 130)),
        }

    return {
        "noeuds": noeuds,
        "conduites": conduites,
        "parametres": {"H_tank": float(H_tank)},
    }
