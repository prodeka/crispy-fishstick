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
        nm = NetworkModel(nodes={}, links={}, tanks={})
        return nm, {"format": "inp", "checksum": checksum}
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


