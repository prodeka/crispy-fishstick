from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import hashlib
import logging

import yaml


class PriceDB:
    """
    Interface unifiée pour l'accès aux prix des diamètres et accessoires.
    
    Cette classe fournit une API cohérente pour accéder aux données de prix
    avec des mécanismes de fallback robustes.
    """
    
    def __init__(self, db_path: Optional[str | Path] = None):
        """
        Initialise la base de données des prix.
        
        Args:
            db_path: Chemin vers la base de données SQLite ou fichier YAML.
                    Si None, utilise le chemin par défaut.
        """
        if db_path is None:
            # Chemin par défaut relatif au module
            db_path = Path(__file__).parent.parent.parent / "db" / "aep_prices.db"
        
        self.db_path = Path(db_path)
        self._is_yaml = self.db_path.suffix.lower() in (".yml", ".yaml")
        self._logger = logging.getLogger(__name__)
        
        # Vérifier l'existence et la validité de la base
        self._validate_database()
    
    def _validate_database(self) -> None:
        """Valide la base de données et configure les fallbacks si nécessaire."""
        if not self.db_path.exists():
            self._logger.warning(f"Base de données introuvable: {self.db_path}")
            self._logger.info("Utilisation des valeurs de fallback par défaut")
            return
        
        try:
            if self._is_yaml:
                self._validate_yaml_db()
            else:
                self._validate_sqlite_db()
        except Exception as e:
            self._logger.error(f"Erreur lors de la validation de la base: {e}")
            self._logger.info("Utilisation des valeurs de fallback par défaut")
    
    def _validate_sqlite_db(self) -> None:
        """Valide une base de données SQLite."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Vérifier les tables essentielles
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = {row[0] for row in cursor.fetchall()}
                
                required_tables = {'diameters', 'accessories'}
                if not required_tables.issubset(tables):
                    missing = required_tables - tables
                    raise ValueError(f"Tables manquantes: {missing}")
                
                # Vérifier le contenu minimal
                cursor.execute("SELECT COUNT(*) FROM diameters")
                diameter_count = cursor.fetchone()[0]
                if diameter_count == 0:
                    raise ValueError("Table diameters vide")
                
                self._logger.info(f"Base SQLite validée: {diameter_count} diamètres disponibles")
                
        except Exception as e:
            raise ValueError(f"Base SQLite invalide: {e}")
    
    def _validate_yaml_db(self) -> None:
        """Valide un fichier YAML de base de données."""
        try:
            data = yaml.safe_load(self.db_path.read_text(encoding="utf-8"))
            if not isinstance(data, list) or not data:
                raise ValueError("Structure YAML invalide")
            
            # Vérifier la structure minimale
            if not all("d_mm" in item for item in data):
                raise ValueError("Champ 'd_mm' manquant dans certains éléments")
            
            self._logger.info(f"Base YAML validée: {len(data)} diamètres disponibles")
            
        except Exception as e:
            raise ValueError(f"Base YAML invalide: {e}")
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Retourne les informations sur la base de données.
        
        Returns:
            Dictionnaire avec les métadonnées de la base
        """
        info = {
            "path": str(self.db_path),
            "exists": self.db_path.exists(),
            "type": "yaml" if self._is_yaml else "sqlite",
            "fallback_used": not self.db_path.exists()
        }
        
        if self.db_path.exists():
            try:
                # Calculer le checksum pour la traçabilité
                checksum = self._calculate_checksum()
                info["checksum"] = checksum
                info["size_bytes"] = self.db_path.stat().st_size
                
                # Informations sur le contenu
                if self._is_yaml:
                    data = yaml.safe_load(self.db_path.read_text(encoding="utf-8"))
                    info["diameter_count"] = len(data) if isinstance(data, list) else 0
                else:
                    with sqlite3.connect(self.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT COUNT(*) FROM diameters")
                        info["diameter_count"] = cursor.fetchone()[0]
                        
                        cursor.execute("SELECT COUNT(*) FROM accessories")
                        info["accessory_count"] = cursor.fetchone()[0]
                        
            except Exception as e:
                info["error"] = str(e)
        
        return info
    
    def _calculate_checksum(self) -> str:
        """Calcule le checksum SHA-256 de la base de données."""
        try:
            with open(self.db_path, 'rb') as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()[:16]
        except Exception:
            return "unknown"
    
    def get_candidate_diameters(self, material: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Récupère les diamètres candidats depuis la source de données.
        
        Args:
            material: Matériau spécifique (optionnel)
            
        Returns:
            Liste des diamètres avec leurs coûts
        """
        if not self.db_path.exists():
            return self._get_fallback_diameters(material)
        
        try:
            if self._is_yaml:
                return self._get_diameters_from_yaml(material)
            else:
                return self._get_diameters_from_sqlite(material)
        except Exception as e:
            self._logger.warning(f"Erreur lors de la lecture des diamètres: {e}")
            return self._get_fallback_diameters(material)
    
    def _get_diameters_from_sqlite(self, material: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupère les diamètres depuis SQLite."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if material:
                cursor.execute(
                    "SELECT dn_mm, total_fcfa_per_m, material FROM diameters WHERE material=? ORDER BY dn_mm",
                    (material,)
                )
            else:
                cursor.execute(
                    "SELECT dn_mm, total_fcfa_per_m, material FROM diameters ORDER BY dn_mm"
                )
            
            results = cursor.fetchall()
            return [
                {
                    "d_mm": row[0],
                    "cost_per_m": row[1],
                    "material": row[2]
                }
                for row in results
            ]
    
    def _get_diameters_from_yaml(self, material: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupère les diamètres depuis YAML."""
        data = yaml.safe_load(self.db_path.read_text(encoding="utf-8"))
        
        if not isinstance(data, list):
            return []
        
        diameters = []
        for item in data:
            if not isinstance(item, dict) or "d_mm" not in item:
                continue
            
            if material and item.get("material") != material:
                continue
            
            diameters.append({
                "d_mm": item["d_mm"],
                "cost_per_m": item.get("cost_per_m", 0.0),
                "material": item.get("material", "Unknown")
            })
        
        return sorted(diameters, key=lambda x: x["d_mm"])
    
    def _get_fallback_diameters(self, material: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retourne les diamètres de fallback par défaut."""
        fallback_diameters = [
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
        
        if material:
            return [d for d in fallback_diameters if d["material"] == material]
        
        return fallback_diameters
    
    def get_diameter_price(self, dn_mm: int, material: Optional[str] = None) -> Optional[float]:
        """
        Obtient le prix d'un diamètre spécifique.
        
        Args:
            dn_mm: Diamètre nominal en mm
            material: Matériau (optionnel)
            
        Returns:
            Prix en FCFA/m ou None si non trouvé
        """
        diameters = self.get_candidate_diameters(material)
        
        for diameter in diameters:
            if diameter["d_mm"] == dn_mm:
                return diameter["cost_per_m"]
        
        return None
    
    def get_closest_diameter(self, target_dn_mm: int, material: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Trouve le diamètre le plus proche d'une valeur cible.
        
        Args:
            target_dn_mm: Diamètre cible en mm
            material: Matériau (optionnel)
            
        Returns:
            Diamètre le plus proche ou None
        """
        diameters = self.get_candidate_diameters(material)
        
        if not diameters:
            return None
        
        # Trouver le diamètre le plus proche
        closest = min(diameters, key=lambda x: abs(x["d_mm"] - target_dn_mm))
        
        # Log si on utilise un diamètre différent
        if closest["d_mm"] != target_dn_mm:
            self._logger.info(
                f"Diamètre {target_dn_mm}mm non trouvé, utilisation de {closest['d_mm']}mm "
                f"(différence: {abs(closest['d_mm'] - target_dn_mm)}mm)"
            )
        
        return closest


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

