"""
DAO (Data Access Object) pour la base de données des prix AEP.

Ce module gère l'accès aux données de prix des diamètres et accessoires
stockées dans la base SQLite.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from .models import OptimizationConfig


class AEPPricesDAO:
    """DAO pour l'accès aux prix AEP."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialise le DAO.
        
        Args:
            db_path: Chemin vers la base de données. Si None, utilise le chemin par défaut.
        """
        if db_path is None:
            # Chemin par défaut relatif au module
            db_path = Path(__file__).parent.parent.parent / "db" / "aep_prices.db"
        
        self.db_path = db_path
        
        if not self.db_path.exists():
            raise FileNotFoundError(f"Base de données introuvable: {self.db_path}")
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtient une connexion à la base de données."""
        return sqlite3.connect(self.db_path)
    
    def _default_material(self) -> str:
        """Retourne le matériau par défaut (env AEP_MATERIAL ou PVC-U)."""
        return os.getenv("AEP_MATERIAL", "PVC-U")

    def get_diameter_price(self, dn_mm: int, material: Optional[str] = None) -> Optional[float]:
        """
        Obtient le prix total (fourniture + pose) d'un diamètre.
        
        Args:
            dn_mm: Diamètre nominal en mm
            material: Matériau (PVC-U, PEHD, Fonte_dutile, etc.)
            
        Returns:
            Prix total en FCFA/m ou None si non trouvé
        """
        try:
            material = material or self._default_material()
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT total_fcfa_per_m FROM diameters WHERE dn_mm=? AND material=? LIMIT 1",
                    (dn_mm, material)
                )
                result = cur.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture du prix: {e}")
            return None
    
    def get_diameter_supply_price(self, dn_mm: int, material: Optional[str] = None) -> Optional[float]:
        """Obtient le prix de fourniture d'un diamètre."""
        try:
            material = material or self._default_material()
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT supply_fcfa_per_m FROM diameters WHERE dn_mm=? AND material=? LIMIT 1",
                    (dn_mm, material)
                )
                result = cur.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture du prix de fourniture: {e}")
            return None
    
    def get_diameter_pose_price(self, dn_mm: int, material: Optional[str] = None) -> Optional[float]:
        """Obtient le prix de pose d'un diamètre."""
        try:
            material = material or self._default_material()
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT pose_fcfa_per_m FROM diameters WHERE dn_mm=? AND material=? LIMIT 1",
                    (dn_mm, material)
                )
                result = cur.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture du prix de pose: {e}")
            return None
    
    def get_accessory_price(self, accessory_code: str, dn_mm: int, material: Optional[str] = None) -> Optional[float]:
        """
        Obtient le prix d'un accessoire.
        
        Args:
            accessory_code: Code de l'accessoire (elbow_90, tee, valve, etc.)
            dn_mm: Diamètre nominal en mm
            material: Matériau
            
        Returns:
            Prix unitaire en FCFA ou None si non trouvé
        """
        try:
            material = material or self._default_material()
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT unit_fcfa FROM accessories WHERE accessory_code=? AND dn_mm=? AND material=? LIMIT 1",
                    (accessory_code, dn_mm, material)
                )
                result = cur.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture du prix d'accessoire: {e}")
            return None
    
    def get_available_diameters(self, material: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtient la liste des diamètres disponibles pour un matériau.
        
        Args:
            material: Matériau
            
        Returns:
            Liste des diamètres avec leurs prix
        """
        try:
            material = material or self._default_material()
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT dn_mm, supply_fcfa_per_m, pose_fcfa_per_m, total_fcfa_per_m FROM diameters WHERE material=? ORDER BY dn_mm",
                    (material,)
                )
                results = cur.fetchall()
                
                return [
                    {
                        "d_mm": row[0],
                        "supply_fcfa_per_m": row[1],
                        "pose_fcfa_per_m": row[2],
                        "cost_per_m": row[3]
                    }
                    for row in results
                ]
        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture des diamètres: {e}")
            return []
    
    def get_available_materials(self) -> List[str]:
        """Obtient la liste des matériaux disponibles."""
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT material FROM diameters ORDER BY material")
                results = cur.fetchall()
                return [row[0] for row in results]
        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture des matériaux: {e}")
            return []
    
    def get_accessory_types(self) -> List[str]:
        """Obtient la liste des types d'accessoires disponibles."""
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT accessory_code FROM accessories ORDER BY accessory_code")
                results = cur.fetchall()
                return [row[0] for row in results]
        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture des types d'accessoires: {e}")
            return []
    
    def add_diameter(self, dn_mm: int, material: str, supply_price: float, pose_price: float) -> bool:
        """
        Ajoute un nouveau diamètre à la base de données.
        
        Args:
            dn_mm: Diamètre nominal en mm
            material: Matériau
            supply_price: Prix de fourniture en FCFA/m
            pose_price: Prix de pose en FCFA/m
            
        Returns:
            True si l'ajout a réussi, False sinon
        """
        try:
            total_price = supply_price + pose_price
            source_method = "manual_entry"
            
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO diameters (dn_mm, material, supply_fcfa_per_m, pose_fcfa_per_m, total_fcfa_per_m, source_method) VALUES (?, ?, ?, ?, ?, ?)",
                    (dn_mm, material, supply_price, pose_price, total_price, source_method)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout du diamètre: {e}")
            return False
    
    def update_diameter(self, dn_mm: int, material: str, supply_price: float, pose_price: float) -> bool:
        """
        Met à jour le prix d'un diamètre existant.
        
        Args:
            dn_mm: Diamètre nominal en mm
            material: Matériau
            supply_price: Nouveau prix de fourniture en FCFA/m
            pose_price: Nouveau prix de pose en FCFA/m
            
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        try:
            total_price = supply_price + pose_price
            
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE diameters SET supply_fcfa_per_m=?, pose_fcfa_per_m=?, total_fcfa_per_m=? WHERE dn_mm=? AND material=?",
                    (supply_price, pose_price, total_price, dn_mm, material)
                )
                
                if cur.rowcount == 0:
                    print(f"⚠️  Aucun diamètre trouvé: DN {dn_mm} {material}")
                    return False
                
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour du diamètre: {e}")
            return False
    
    def remove_diameter(self, dn_mm: int, material: str) -> bool:
        """
        Supprime un diamètre de la base de données.
        
        Args:
            dn_mm: Diamètre nominal en mm
            material: Matériau
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "DELETE FROM diameters WHERE dn_mm=? AND material=?",
                    (dn_mm, material)
                )
                
                if cur.rowcount == 0:
                    print(f"⚠️  Aucun diamètre trouvé: DN {dn_mm} {material}")
                    return False
                
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ Erreur lors de la suppression du diamètre: {e}")
            return False
    
    def get_diameter_info(self, dn_mm: int, material: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Obtient toutes les informations d'un diamètre.
        
        Args:
            dn_mm: Diamètre nominal en mm
            material: Matériau
            
        Returns:
            Dictionnaire avec les informations du diamètre ou None
        """
        try:
            material = material or self._default_material()
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT * FROM diameters WHERE dn_mm=? AND material=? LIMIT 1",
                    (dn_mm, material)
                )
                result = cur.fetchone()
                
                if result:
                    return {
                        "id": result[0],
                        "dn_mm": result[1],
                        "material": result[2],
                        "supply_fcfa_per_m": result[3],
                        "pose_fcfa_per_m": result[4],
                        "total_fcfa_per_m": result[5],
                        "source_method": result[6]
                    }
                return None
        except Exception as e:
            print(f"⚠️  Erreur lors de la lecture des informations du diamètre: {e}")
            return None


# Instance globale pour utilisation
prices_dao = AEPPricesDAO()


def get_candidate_diameters(material: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fonction de compatibilité avec l'ancien code.
    
    Args:
        material: Matériau
        
    Returns:
        Liste des diamètres disponibles
    """
    return prices_dao.get_available_diameters(material)


def get_diameter_price(dn_mm: int, material: Optional[str] = None) -> Optional[float]:
    """
    Fonction de compatibilité avec l'ancien code.
    
    Args:
        dn_mm: Diamètre nominal en mm
        material: Matériau
        
    Returns:
        Prix total en FCFA/m ou None
    """
    return prices_dao.get_diameter_price(dn_mm, material)
