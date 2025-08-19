from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


class DiameterDAO:
    """Data Access Object pour les diamètres et leurs coûts."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self._is_yaml = db_path and Path(db_path).suffix.lower() in (".yml", ".yaml")

    def get_candidate_diameters(self) -> List[Dict[str, Any]]:
        """
        Récupère les diamètres candidats depuis la source de données (SQLite ou YAML).
        Retourne une liste de dictionnaires, ex: [{"d_mm": 110, "cost_per_m": 15.5}, ...].
        """
        if self.db_path and not self._is_yaml:
            # Logique pour lire depuis une base de données SQLite
            try:
                con = sqlite3.connect(self.db_path)
                cur = con.cursor()
                res = cur.execute("SELECT d_mm, cost_per_m, material FROM diameters ORDER BY d_mm ASC")
                candidates = [{"d_mm": row[0], "cost_per_m": row[1], "material": row[2]} for row in res.fetchall()]
                con.close()
                if candidates:
                    return candidates
            except sqlite3.Error:
                # Si la DB échoue, on utilise le fallback
                pass

        if self.db_path and self._is_yaml:
            # Logique pour lire depuis un fichier YAML
            try:
                db = yaml.safe_load(Path(self.db_path).read_text(encoding="utf-8")) or []
                # Valider la structure minimale
                if isinstance(db, list) and all("d_mm" in row for row in db):
                    return sorted(db, key=lambda x: x["d_mm"])
            except (IOError, yaml.YAMLError):
                # Si le YAML échoue, on utilise le fallback
                pass
        
        # Fallback si aucune source de données n'est fournie ou ne fonctionne
        return [
            {"d_mm": 50, "cost_per_m": 5.0, "material": "PVC"},
            {"d_mm": 63, "cost_per_m": 7.5, "material": "PVC"},
            {"d_mm": 75, "cost_per_m": 10.0, "material": "PVC"},
            {"d_mm": 90, "cost_per_m": 15.0, "material": "PEHD"},
            {"d_mm": 110, "cost_per_m": 20.0, "material": "PEHD"},
            {"d_mm": 125, "cost_per_m": 25.0, "material": "PEHD"},
            {"d_mm": 140, "cost_per_m": 30.0, "material": "Fonte"},
            {"d_mm": 160, "cost_per_m": 35.0, "material": "Fonte"},
            {"d_mm": 200, "cost_per_m": 50.0, "material": "Fonte"},
        ]

def get_candidate_diameters(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fonction utilitaire pour un accès simple."""
    dao = DiameterDAO(db_path)
    return dao.get_candidate_diameters()

