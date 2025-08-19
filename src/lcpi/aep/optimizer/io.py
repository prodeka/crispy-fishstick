from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import hashlib

import yaml
from pydantic import BaseModel


class NetworkModel(BaseModel):
    """Modèle réseau minimal utilisé par l'optimiseur (MVP)."""
    nodes: Dict[str, Dict[str, Any]] = {}
    links: Dict[str, Dict[str, Any]] = {}
    tanks: Dict[str, Dict[str, Any]] = {}


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_yaml_or_inp(path: Path) -> Tuple[NetworkModel, Dict[str, Any]]:
    """Charge un fichier YAML (schéma interne) ou INP (EPANET).

    Pour INP (MVP), on ne parse pas: on retourne un modèle vide avec un meta checksum.
    """
    if path.suffix.lower() in (".yml", ".yaml"):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        nm = NetworkModel(**(raw or {}))
        return nm, {"format": "yaml"}
    if path.suffix.lower() == ".inp":
        checksum = sha256_of_file(path)
        # Parse minimal [PIPES] section: ID Node1 Node2 Length Diameter Roughness MinorLoss Status
        text = path.read_text(errors="ignore")
        links: Dict[str, Dict[str, Any]] = {}
        in_pipes = False
        for line in text.splitlines():
            s = line.strip()
            if not s or s.startswith(";"):
                continue
            if s.startswith("["):
                in_pipes = s.upper().startswith("[PIPES]")
                continue
            if in_pipes:
                parts = s.split()
                if len(parts) >= 4:
                    lid = parts[0]
                    n1 = parts[1]
                    n2 = parts[2]
                    try:
                        length = float(parts[3])
                    except Exception:
                        length = 0.0
                    # Diamètre s'il est présent
                    diameter_mm = None
                    if len(parts) >= 5:
                        try:
                            diameter_mm = int(float(parts[4]))
                        except Exception:
                            diameter_mm = None
                    links[lid] = {
                        "from": n1,
                        "to": n2,
                        "length_m": length,
                        "diameter_mm": diameter_mm,
                    }
        nm = NetworkModel(nodes={}, links=links, tanks={})
        return nm, {"format": "inp", "checksum": checksum, "links_parsed": len(links), "file_path": str(path)}
    raise ValueError("Format réseau non supporté. Utiliser .yml/.yaml ou .inp")


def convert_to_solver_network_data(
    network_model: NetworkModel,
    H_tank: float,
    diameters_mm_override: Optional[Dict[str, int]] = None,
) -> Dict[str, Any]:
    """Convertit NetworkModel -> format attendu par les solveurs (noeuds/conduites).

    Remplit les champs minimaux: noeuds, conduites, parametres.
    """
    noeuds: Dict[str, Any] = {}
    # Copier nœuds existants comme consommateurs par défaut
    for nid, n in (network_model.nodes or {}).items():
        noeuds[nid] = {
            "role": n.get("role", "consommation"),
            "elevation_m": float(n.get("elevation_m", 0.0)),
            "demande_m3_s": float(n.get("base_demand_m3_s", 0.0)),
        }
    # Ajouter un réservoir à partir du premier tank
    if network_model.tanks:
        tid, t = next(iter(network_model.tanks.items()))
        noeuds[tid] = {
            "role": "reservoir",
            "elevation_m": float(t.get("radier_elevation_m", 0.0)),
            "H_tank_m": float(H_tank),
        }

    conduites: Dict[str, Any] = {}
    for lid, link in (network_model.links or {}).items():
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


