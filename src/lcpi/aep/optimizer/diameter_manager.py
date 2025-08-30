"""
Gestionnaire centralisé des diamètres candidats pour l'optimisation AEP.

Ce module assure une gestion cohérente des diamètres et de leurs prix
dans tous les algorithmes d'optimisation.
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class DiameterCandidate:
    """Représente un diamètre candidat avec ses informations complètes."""
    diameter_mm: int
    cost_per_m: float
    material: str = "PVC-U"
    supply_cost: Optional[float] = None
    installation_cost: Optional[float] = None
    
    def __post_init__(self):
        """Valide et complète les données après initialisation."""
        if self.diameter_mm <= 0:
            raise ValueError(f"Le diamètre doit être positif, reçu: {self.diameter_mm}")
        if self.cost_per_m <= 0:
            raise ValueError(f"Le coût par mètre doit être positif, reçu: {self.cost_per_m}")

class DiameterManager:
    """Gestionnaire centralisé des diamètres candidats."""
    
    def __init__(self, price_db_path: Optional[Path] = None):
        """
        Initialise le gestionnaire de diamètres.
        
        Args:
            price_db_path: Chemin vers la base de données des prix
        """
        self.price_db_path = price_db_path or self._get_default_price_db_path()
        self._cached_diameters: Optional[List[DiameterCandidate]] = None
        
    def _get_default_price_db_path(self) -> Path:
        """Retourne le chemin par défaut de la base de données des prix."""
        return Path(__file__).parent.parent.parent / "db" / "aep_prices.db"
    
    def get_candidate_diameters(self, material: str = "PVC-U") -> List[DiameterCandidate]:
        """
        Récupère la liste des diamètres candidats avec leurs prix.
        
        Stratégie:
        1. Essayer de charger depuis la base de données
        2. Fallback avec des diamètres standards et prix réalistes
        3. Cache pour éviter les rechargements multiples
        
        Args:
            material: Matériau des conduites
            
        Returns:
            Liste des diamètres candidats avec leurs prix
        """
        # Utiliser le cache si disponible
        if self._cached_diameters is not None:
            return self._cached_diameters
        
        # Essayer de charger depuis la base de données
        db_diameters = self._load_from_database(material)
        if db_diameters:
            self._cached_diameters = db_diameters
            logger.info(f"✅ {len(db_diameters)} diamètres chargés depuis la base de données")
            return db_diameters
        
        # Fallback avec des diamètres standards et prix réalistes
        fallback_diameters = self._create_fallback_diameters()
        self._cached_diameters = fallback_diameters
        logger.warning(f"⚠️ Utilisation de {len(fallback_diameters)} diamètres standards (fallback)")
        return fallback_diameters
    
    def _load_from_database(self, material: str) -> Optional[List[DiameterCandidate]]:
        """
        Charge les diamètres depuis la base de données.
        
        Args:
            material: Matériau des conduites
            
        Returns:
            Liste des diamètres ou None si échec
        """
        try:
            if not self.price_db_path.exists():
                logger.debug(f"Base de données introuvable: {self.price_db_path}")
                return None
            
            # Import dynamique pour éviter les dépendances circulaires
            from .db import PriceDB
            
            price_db = PriceDB()
            db_rows = price_db.get_candidate_diameters(material)
            if not db_rows:
                logger.debug(f"Aucun diamètre trouvé pour le matériau: {material}")
                return None
            
            # Convertir en objets DiameterCandidate
            candidates = []
            for row in db_rows:
                try:
                    diameter_mm = int(row.get("d_mm", 0))
                    cost_per_m = float(row.get("cost_per_m", row.get("total_fcfa_per_m", 0)))
                    supply_cost = float(row.get("supply_fcfa_per_m", 0))
                    installation_cost = float(row.get("pose_fcfa_per_m", 0))
                    
                    if diameter_mm > 0 and cost_per_m > 0:
                        candidate = DiameterCandidate(
                            diameter_mm=diameter_mm,
                            cost_per_m=cost_per_m,
                            material=material,
                            supply_cost=supply_cost if supply_cost > 0 else None,
                            installation_cost=installation_cost if installation_cost > 0 else None
                        )
                        candidates.append(candidate)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Erreur lors du parsing du diamètre: {e}, ligne: {row}")
                    continue
            
            # Trier par diamètre croissant
            candidates.sort(key=lambda x: x.diameter_mm)
            return candidates
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement depuis la base de données: {e}")
            return None
    
    def _create_fallback_diameters(self) -> List[DiameterCandidate]:
        """
        Crée une liste de diamètres standards avec des prix réalistes.
        
        Stratégie de prix:
        - Prix de base pour les petits diamètres
        - Facteur de taille pour les gros diamètres
        - Prix cohérents avec le marché local
        
        Returns:
            Liste des diamètres standards avec prix réalistes
        """
        # Diamètres standards selon les normes
        STANDARD_DIAMETERS = [
            50, 63, 75, 90, 110, 125, 140, 160, 180, 200, 
            225, 250, 280, 315, 355, 400, 450, 500
        ]
        
        candidates = []
        for diameter_mm in STANDARD_DIAMETERS:
            # Calcul de prix réaliste basé sur la taille
            cost_per_m = self._calculate_realistic_price(diameter_mm)
            
            candidate = DiameterCandidate(
                diameter_mm=diameter_mm,
                cost_per_m=cost_per_m,
                material="PVC-U"
            )
            candidates.append(candidate)
        
        return candidates
    
    def _calculate_realistic_price(self, diameter_mm: int) -> float:
        """
        Calcule un prix réaliste pour un diamètre donné.
        
        Formule basée sur:
        - Coût de base pour les petits diamètres
        - Facteur de taille (surface de la conduite)
        - Coûts de transport et manutention
        - Prix du marché local (FCFA)
        
        Args:
            diameter_mm: Diamètre en millimètres
            
        Returns:
            Prix par mètre en FCFA
        """
        # Prix de base pour les petits diamètres (50-110mm)
        base_price = 50.0  # FCFA/m
        
        # Facteur de taille basé sur la surface de la conduite
        # Surface ~ (π * D²) / 4, donc facteur ~ D²
        size_factor = (diameter_mm / 100.0) ** 1.8
        
        # Facteur de complexité pour les gros diamètres
        complexity_factor = 1.0
        if diameter_mm > 200:
            complexity_factor = 1.2  # +20% pour les gros diamètres
        elif diameter_mm > 400:
            complexity_factor = 1.5  # +50% pour les très gros diamètres
        
        # Prix final
        price = base_price * size_factor * complexity_factor
        
        # Arrondir à 10 FCFA près
        return round(price / 10) * 10
    
    def get_diameter_price(self, diameter_mm: int) -> Optional[float]:
        """
        Récupère le prix d'un diamètre spécifique.
        
        Args:
            diameter_mm: Diamètre en millimètres
            
        Returns:
            Prix par mètre ou None si non trouvé
        """
        candidates = self.get_candidate_diameters()
        for candidate in candidates:
            if candidate.diameter_mm == diameter_mm:
                return candidate.cost_per_m
        return None
    
    def get_diameter_range(self) -> Tuple[int, int]:
        """
        Retourne la plage de diamètres disponibles.
        
        Returns:
            Tuple (diamètre_min, diamètre_max) en millimètres
        """
        candidates = self.get_candidate_diameters()
        if not candidates:
            return (50, 500)  # Valeurs par défaut
        
        diameters = [c.diameter_mm for c in candidates]
        return (min(diameters), max(diameters))
    
    def get_diameter_step(self, current_diameter: int, direction: int = 1) -> Optional[int]:
        """
        Retourne le diamètre suivant/précédent dans la liste.
        
        Args:
            current_diameter: Diamètre actuel en millimètres
            direction: 1 pour suivant, -1 pour précédent
            
        Returns:
            Diamètre suivant/précédent ou None si non disponible
        """
        candidates = self.get_candidate_diameters()
        if not candidates:
            return None
        
        diameters = [c.diameter_mm for c in candidates]
        try:
            current_index = diameters.index(current_diameter)
            new_index = current_index + direction
            
            if 0 <= new_index < len(diameters):
                return diameters[new_index]
        except ValueError:
            pass
        
        return None
    
    def clear_cache(self):
        """Efface le cache des diamètres."""
        self._cached_diameters = None
        logger.debug("Cache des diamètres effacé")

# Instance globale pour utilisation dans tout le projet
_diameter_manager: Optional[DiameterManager] = None

def get_diameter_manager() -> DiameterManager:
    """Retourne l'instance globale du gestionnaire de diamètres."""
    global _diameter_manager
    if _diameter_manager is None:
        _diameter_manager = DiameterManager()
    return _diameter_manager

def get_standard_diameters_with_prices(material: str = "PVC-U") -> List[Dict[str, any]]:
    """
    Fonction de compatibilité pour l'ancien code.
    
    Args:
        material: Matériau des conduites
        
    Returns:
        Liste des diamètres au format dict compatible
    """
    manager = get_diameter_manager()
    candidates = manager.get_candidate_diameters(material)
    
    # Convertir au format attendu par l'ancien code
    return [
        {
            "d_mm": c.diameter_mm,
            "cost_per_m": c.cost_per_m,
            "total_fcfa_per_m": c.cost_per_m,
            "supply_fcfa_per_m": c.supply_cost or c.cost_per_m * 0.6,
            "pose_fcfa_per_m": c.installation_cost or c.cost_per_m * 0.4,
            "material": c.material
        }
        for c in candidates
    ]
