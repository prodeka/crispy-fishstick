"""
Adaptateur de prix pour utiliser la base de données existante avec le solveur LCPI.

Ce module permet au solveur LCPI d'utiliser directement la base de données
existante sans modification, en adaptant les requêtes aux tables 'diameters'
et 'accessories'.
"""

import sqlite3
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ExistingPriceAdapter:
    """
    Adaptateur pour utiliser la base de données des prix existante.
    
    Utilise les tables 'diameters' et 'accessories' existantes
    pour fournir les prix au solveur LCPI.
    """
    
    def __init__(self, db_path: str = "src/lcpi/db/aep_prices.db"):
        """
        Initialise l'adaptateur de prix.
        
        Args:
            db_path: Chemin vers la base de données existante
        """
        self.db_path = Path(db_path)
        self._validate_database()
    
    def _validate_database(self):
        """Valide que la base de données contient les tables attendues."""
        if not self.db_path.exists():
            raise FileNotFoundError(f"Base de données non trouvée: {self.db_path}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier la présence des tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['diameters', 'accessories']
            missing_tables = [t for t in required_tables if t not in tables]
            
            if missing_tables:
                raise ValueError(f"Tables manquantes: {missing_tables}")
            
            # Vérifier la structure de la table diameters
            cursor.execute("PRAGMA table_info(diameters)")
            columns = [col[1] for col in cursor.fetchall()]
            required_columns = ['dn_mm', 'material', 'total_fcfa_per_m']
            missing_columns = [c for c in required_columns if c not in columns]
            
            if missing_columns:
                raise ValueError(f"Colonnes manquantes dans 'diameters': {missing_columns}")
            
            conn.close()
            logger.info(f"Base de données validée: {self.db_path}")
            
        except Exception as e:
            raise RuntimeError(f"Erreur de validation de la base de données: {e}")
    
    def get_pipe_price(self, diameter_mm: int, material: str = "Acier_galv") -> Optional[float]:
        """
        Récupère le prix d'une conduite depuis la base existante.
        
        Args:
            diameter_mm: Diamètre en millimètres
            material: Matériau de la conduite
            
        Returns:
            Prix en FCFA/m ou None si non trouvé
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Chercher le prix dans la table diameters
            cursor.execute("""
                SELECT total_fcfa_per_m 
                FROM diameters 
                WHERE dn_mm = ? AND material = ?
                LIMIT 1
            """, (diameter_mm, material))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                price = result[0]
                logger.debug(f"Prix trouvé pour {diameter_mm}mm {material}: {price} FCFA/m")
                return price
            else:
                logger.warning(f"Prix non trouvé pour {diameter_mm}mm {material}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du prix: {e}")
            return None
    
    def get_available_diameters(self, material: str = "Acier_galv") -> List[int]:
        """
        Récupère la liste des diamètres disponibles pour un matériau.
        
        Args:
            material: Matériau de la conduite
            
        Returns:
            Liste des diamètres disponibles en mm
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT dn_mm 
                FROM diameters 
                WHERE material = ?
                ORDER BY dn_mm
            """, (material,))
            
            diameters = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            logger.debug(f"Diamètres disponibles pour {material}: {diameters}")
            return diameters
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des diamètres: {e}")
            return []
    
    def get_available_materials(self) -> List[str]:
        """
        Récupère la liste des matériaux disponibles.
        
        Returns:
            Liste des matériaux disponibles
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT DISTINCT material FROM diameters ORDER BY material")
            materials = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            logger.debug(f"Matériaux disponibles: {materials}")
            return materials
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des matériaux: {e}")
            return []
    
    def get_accessory_price(self, accessory_code: str, diameter_mm: int, material: str = "Acier_galv") -> Optional[float]:
        """
        Récupère le prix d'un accessoire depuis la base existante.
        
        Args:
            accessory_code: Code de l'accessoire (ex: 'elbow_90')
            diameter_mm: Diamètre en millimètres
            material: Matériau de l'accessoire
            
        Returns:
            Prix en FCFA ou None si non trouvé
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT unit_fcfa 
                FROM accessories 
                WHERE accessory_code = ? AND dn_mm = ? AND material = ?
                LIMIT 1
            """, (accessory_code, diameter_mm, material))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                price = result[0]
                logger.debug(f"Prix accessoire {accessory_code} {diameter_mm}mm {material}: {price} FCFA")
                return price
            else:
                logger.warning(f"Prix accessoire non trouvé: {accessory_code} {diameter_mm}mm {material}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du prix accessoire: {e}")
            return None
    
    def calculate_network_cost(self, diameters_mm: Dict[str, int], material: str = "Acier_galv", 
                             conduit_length_m: float = 100.0) -> Dict[str, Any]:
        """
        Calcule le coût total d'un réseau en utilisant la base existante.
        
        Args:
            diameters_mm: Dictionnaire {conduit_id: diameter_mm}
            material: Matériau des conduites
            conduit_length_m: Longueur estimée par conduite (m)
            
        Returns:
            Dictionnaire avec le coût total et le détail
        """
        total_cost = 0.0
        conduit_costs = {}
        missing_prices = []
        
        for conduit_id, diameter in diameters_mm.items():
            price_per_m = self.get_pipe_price(diameter, material)
            
            if price_per_m is not None:
                conduit_cost = price_per_m * conduit_length_m
                total_cost += conduit_cost
                conduit_costs[conduit_id] = {
                    'diameter_mm': diameter,
                    'material': material,
                    'price_per_m': price_per_m,
                    'length_m': conduit_length_m,
                    'total_cost': conduit_cost
                }
            else:
                missing_prices.append(f"{conduit_id}: {diameter}mm {material}")
        
        result = {
            'total_cost_fcfa': total_cost,
            'conduit_costs': conduit_costs,
            'missing_prices': missing_prices,
            'material_used': material,
            'estimated_length_per_conduit_m': conduit_length_m
        }
        
        if missing_prices:
            logger.warning(f"Prix manquants pour {len(missing_prices)} conduites")
        
        logger.info(f"Coût total calculé: {total_cost:,.0f} FCFA")
        return result
    
    def get_price_summary(self) -> Dict[str, Any]:
        """
        Récupère un résumé des prix disponibles.
        
        Returns:
            Résumé des prix par matériau et diamètre
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT material, dn_mm, total_fcfa_per_m
                FROM diameters
                ORDER BY material, dn_mm
            """)
            
            prices = cursor.fetchall()
            conn.close()
            
            summary = {}
            for material, diameter, price in prices:
                if material not in summary:
                    summary[material] = {}
                summary[material][diameter] = price
            
            return summary
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du résumé: {e}")
            return {}
