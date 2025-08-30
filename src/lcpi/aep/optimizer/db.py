from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import hashlib
import logging

import yaml


# --- Modèle de tarification réaliste (loi de puissance) ---

# Coefficients à stocker dans un fichier de config à terme, mais OK ici pour commencer.
# Le 'scaling_factor' est à ajuster pour que les prix correspondent à votre monnaie (FCFA).
PRICE_MODELS = {
    "PVC": {"scaling_factor": 25, "exponent_b": 1.30},
    "PEHD": {"scaling_factor": 30, "exponent_b": 1.35},
    "Fonte": {"scaling_factor": 150, "exponent_b": 1.20}
}

def _get_realistic_pipe_price(diameter_mm: int, material: str) -> float:
    """Estime le coût unitaire d'une conduite en utilisant un modèle de loi de puissance."""
    model = PRICE_MODELS.get(material, PRICE_MODELS["PEHD"]) # Fallback sur PEHD si matériau inconnu
    
    # Formule : Coût = a * D^b
    # On arrondit au 100 FCFA le plus proche pour un résultat plus propre.
    cost = model["scaling_factor"] * (diameter_mm ** model["exponent_b"])
    return round(cost / 100) * 100


# --- Liste de base des diamètres de fallback ---

# NOUVELLE LISTE DE BASE - Structure harmonisée avec dn_mm
FALLBACK_DIAMETERS_BASE = [
    # --- PVC-U Pression (généralement pour les petits à moyens diamètres) ---
    {"dn_mm": 25, "material": "PVC"},
    {"dn_mm": 32, "material": "PVC"},
    {"dn_mm": 40, "material": "PVC"},
    {"dn_mm": 50, "material": "PVC"},
    {"dn_mm": 63, "material": "PVC"},
    {"dn_mm": 75, "material": "PVC"},
    {"dn_mm": 90, "material": "PVC"},
    {"dn_mm": 110, "material": "PVC"},
    {"dn_mm": 125, "material": "PVC"},
    {"dn_mm": 140, "material": "PVC"},
    {"dn_mm": 160, "material": "PVC"},
    {"dn_mm": 200, "material": "PVC"},
    {"dn_mm": 225, "material": "PVC"},
    {"dn_mm": 250, "material": "PVC"},

    # --- PEHD (Polyéthylène Haute Densité) - Flexible et très courant ---
    # Note : les diamètres PEHD sont souvent "externes", mais on les utilise comme nominaux ici
    {"dn_mm": 63, "material": "PEHD"},
    {"dn_mm": 75, "material": "PEHD"},
    {"dn_mm": 90, "material": "PEHD"},
    {"dn_mm": 110, "material": "PEHD"},
    {"dn_mm": 125, "material": "PEHD"},
    {"dn_mm": 160, "material": "PEHD"},
    {"dn_mm": 180, "material": "PEHD"},
    {"dn_mm": 200, "material": "PEHD"},
    {"dn_mm": 225, "material": "PEHD"},
    {"dn_mm": 250, "material": "PEHD"},
    {"dn_mm": 315, "material": "PEHD"},

    # --- Fonte Ductile (pour les conduites structurantes et grands diamètres) ---
    {"dn_mm": 100, "material": "Fonte"},
    {"dn_mm": 125, "material": "Fonte"},
    {"dn_mm": 150, "material": "Fonte"},
    {"dn_mm": 200, "material": "Fonte"},
    {"dn_mm": 250, "material": "Fonte"},
    {"dn_mm": 300, "material": "Fonte"},
    {"dn_mm": 350, "material": "Fonte"},
    {"dn_mm": 400, "material": "Fonte"},
    {"dn_mm": 450, "material": "Fonte"},
    {"dn_mm": 500, "material": "Fonte"},
    {"dn_mm": 600, "material": "Fonte"},
]


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
            if not all("dn_mm" in item for item in data):
                raise ValueError("Champ 'dn_mm' manquant dans certains éléments")
            
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
            Liste des diamètres avec leurs coûts (structure canonique)
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
        """Récupère les diamètres depuis SQLite avec structure canonique."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if material:
                cursor.execute(
                    "SELECT dn_mm, supply_fcfa_per_m, pose_fcfa_per_m, total_fcfa_per_m, material, source_method FROM diameters WHERE material=? ORDER BY dn_mm",
                    (material,)
                )
            else:
                cursor.execute(
                    "SELECT dn_mm, supply_fcfa_per_m, pose_fcfa_per_m, total_fcfa_per_m, material, source_method FROM diameters ORDER BY dn_mm"
                )
            
            results = cursor.fetchall()
            return [
                {
                    "dn_mm": row[0],
                    "supply_fcfa_per_m": row[1],
                    "pose_fcfa_per_m": row[2],
                    "total_fcfa_per_m": row[3],
                    "material": row[4],
                    "source_method": row[5] if len(row) > 5 else "sqlite"
                }
                for row in results
            ]
    
    def _get_diameters_from_yaml(self, material: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupère les diamètres depuis YAML avec structure canonique."""
        data = yaml.safe_load(self.db_path.read_text(encoding="utf-8"))
        
        if not isinstance(data, list):
            return []
        
        diameters = []
        for item in data:
            if not isinstance(item, dict) or "dn_mm" not in item:
                continue
            
            if material and item.get("material") != material:
                continue
            
            # Structure canonique avec valeurs par défaut si manquantes
            diameters.append({
                "dn_mm": item["dn_mm"],
                "supply_fcfa_per_m": item.get("supply_fcfa_per_m", 0.0),
                "pose_fcfa_per_m": item.get("pose_fcfa_per_m", 0.0),
                "total_fcfa_per_m": item.get("total_fcfa_per_m", item.get("cost_per_m", 0.0)),
                "material": item.get("material", "Unknown"),
                "source_method": item.get("source_method", "yaml")
            })
        
        return sorted(diameters, key=lambda x: x["dn_mm"])
    
    def _get_fallback_diameters(self, material: Optional[str] = None) -> List[Dict[str, Any]]:
        """Génère la liste de fallback avec des prix calculés de manière réaliste et structure canonique."""
        self._logger.warning("Utilisation des diamètres de fallback internes avec modèle de tarification réaliste.")
        
        fallback_data = []
        for item in FALLBACK_DIAMETERS_BASE:
            dn_mm = item["dn_mm"]
            item_material = item["material"]
            
            # Filtrer par matériau si spécifié
            if material and item_material != material:
                continue
            
            # Calculer le prix dynamiquement avec le modèle réaliste
            price = _get_realistic_pipe_price(dn_mm, item_material)
            
            # Structure canonique complète
            fallback_data.append({
                "dn_mm": dn_mm,
                "supply_fcfa_per_m": price,
                "pose_fcfa_per_m": 0,  # Coût de pose non inclus dans le modèle de base
                "total_fcfa_per_m": price,
                "material": item_material,
                "source_method": "fallback_realistic_model"
            })
        
        return sorted(fallback_data, key=lambda x: x["dn_mm"])
    
    def get_diameter_price(self, dn_mm: int, material: Optional[str] = None) -> Optional[float]:
        """
        Obtient le prix d'un diamètre spécifique.
        
        Args:
            dn_mm: Diamètre nominal en mm
            material: Matériau (optionnel)
            
        Returns:
            Prix total en FCFA/m ou None si non trouvé
        """
        diameters = self.get_candidate_diameters(material)
        
        for diameter in diameters:
            if diameter["dn_mm"] == dn_mm:
                return diameter["total_fcfa_per_m"]
        
        return None
    
    def get_closest_diameter(self, target_dn_mm: int, material: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Trouve le diamètre le plus proche d'une valeur cible.
        
        Args:
            target_dn_mm: Diamètre cible en mm
            material: Matériau (optionnel)
            
        Returns:
            Diamètre le plus proche avec structure canonique ou None
        """
        diameters = self.get_candidate_diameters(material)
        
        if not diameters:
            return None
        
        # Trouver le diamètre le plus proche
        closest = min(diameters, key=lambda x: abs(x["dn_mm"] - target_dn_mm))
        
        # Log si on utilise un diamètre différent
        if closest["dn_mm"] != target_dn_mm:
            self._logger.info(
                f"Diamètre {target_dn_mm}mm non trouvé, utilisation de {closest['dn_mm']}mm "
                f"(différence: {abs(closest['dn_mm'] - target_dn_mm)}mm)"
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
        Retourne une liste de dictionnaires avec structure canonique.
        """
        if self.db_path and not self._is_yaml:
            # Logique pour lire depuis une base de données SQLite
            try:
                con = sqlite3.connect(self.db_path)
                cur = con.cursor()
                res = cur.execute("SELECT dn_mm, total_fcfa_per_m, material FROM diameters ORDER BY dn_mm ASC")
                candidates = [{"dn_mm": row[0], "total_fcfa_per_m": row[1], "material": row[2]} for row in res.fetchall()]
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
                if isinstance(db, list) and all("dn_mm" in row for row in db):
                    return sorted(db, key=lambda x: x["dn_mm"])
            except (IOError, yaml.YAMLError):
                # Si le YAML échoue, on utilise le fallback
                pass
        
        # Fallback si aucune source de données n'est fournie ou ne fonctionne
        # Utiliser la nouvelle structure harmonisée
        fallback_data = []
        for item in FALLBACK_DIAMETERS_BASE:
            dn_mm = item["dn_mm"]
            material = item["material"]
            price = _get_realistic_pipe_price(dn_mm, material)
            
            fallback_data.append({
                "dn_mm": dn_mm,
                "total_fcfa_per_m": price,
                "material": material
            })
        
        return sorted(fallback_data, key=lambda x: x["dn_mm"])

def get_candidate_diameters(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fonction utilitaire pour un accès simple."""
    dao = DiameterDAO(db_path)
    return dao.get_candidate_diameters()

