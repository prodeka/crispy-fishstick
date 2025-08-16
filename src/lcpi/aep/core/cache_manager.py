"""
Gestionnaire de cache intelligent pour optimiser les performances des calculs AEP.

Ce module implémente un système de cache avec :
- Mémorisation des résultats de calculs hydrauliques
- Gestion automatique de la mémoire
- Cache LRU (Least Recently Used) avec taille configurable
- Nettoyage automatique et gestion des dépendances
"""

import hashlib
import json
import pickle
import time
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


class CacheEntry:
    """Représente une entrée dans le cache."""
    
    def __init__(self, key: str, data: Any, dependencies: Optional[List[str]] = None):
        self.key = key
        self.data = data
        self.dependencies = dependencies or []
        self.timestamp = time.time()
        self.access_count = 0
        self.size_bytes = self._estimate_size()
    
    def _estimate_size(self) -> int:
        """Estime la taille en bytes de l'entrée."""
        try:
            # Essayer de sérialiser pour estimer la taille
            serialized = pickle.dumps(self.data)
            return len(serialized)
        except Exception:
            # Fallback : estimation basée sur le type
            return len(str(self.data)) * 2  # Approximation
    
    def access(self):
        """Marque l'entrée comme accédée."""
        self.timestamp = time.time()
        self.access_count += 1
    
    def is_expired(self, max_age_seconds: int) -> bool:
        """Vérifie si l'entrée a expiré."""
        return time.time() - self.timestamp > max_age_seconds


class CacheManager:
    """Gestionnaire de cache intelligent pour les calculs AEP."""
    
    def __init__(self, 
                 max_size_mb: int = 100,
                 max_entries: int = 1000,
                 cache_dir: Optional[Path] = None,
                 enable_persistence: bool = True):
        """
        Initialise le gestionnaire de cache.
        
        Args:
            max_size_mb: Taille maximale du cache en MB
            max_entries: Nombre maximum d'entrées
            cache_dir: Répertoire pour la persistance (optionnel)
            enable_persistence: Activer la persistance sur disque
        """
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.max_entries = max_entries
        self.enable_persistence = enable_persistence
        
        # Cache en mémoire (LRU)
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.current_size_bytes = 0
        
        # Répertoire de cache
        if cache_dir and enable_persistence:
            self.cache_dir = Path(cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.cache_dir = None
        
        # Statistiques
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "size_evictions": 0
        }
        
        # Charger le cache persistant si activé
        if self.enable_persistence and self.cache_dir:
            self._load_persistent_cache()
    
    def _generate_key(self, data: Any, prefix: str = "") -> str:
        """
        Génère une clé de cache basée sur les données.
        
        Args:
            data: Données à hasher
            prefix: Préfixe pour la clé
            
        Returns:
            Clé de cache unique
        """
        try:
            # Essayer de sérialiser en JSON pour un hash stable
            data_str = json.dumps(data, sort_keys=True, default=str)
        except Exception:
            # Fallback : conversion en string
            data_str = str(data)
        
        # Ajouter le préfixe
        if prefix:
            data_str = f"{prefix}:{data_str}"
        
        # Générer le hash SHA-256
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Récupère une valeur du cache.
        
        Args:
            key: Clé de cache
            default: Valeur par défaut si la clé n'existe pas
            
        Returns:
            Valeur en cache ou valeur par défaut
        """
        if key in self.cache:
            entry = self.cache[key]
            entry.access()
            
            # Vérifier l'expiration (24h par défaut)
            if entry.is_expired(24 * 3600):
                del self.cache[key]
                self.current_size_bytes -= entry.size_bytes
                self.stats["misses"] += 1
                return default
            
            # Déplacer en fin (LRU)
            self.cache.move_to_end(key)
            self.stats["hits"] += 1
            return entry.data
        
        self.stats["misses"] += 1
        return default
    
    def set(self, key: str, data: Any, dependencies: Optional[List[str]] = None) -> bool:
        """
        Stocke une valeur dans le cache.
        
        Args:
            key: Clé de cache
            data: Données à stocker
            dependencies: Liste des dépendances
            
        Returns:
            True si l'opération a réussi
        """
        try:
            # Créer l'entrée
            entry = CacheEntry(key, data, dependencies)
            
            # Vérifier si on doit faire de la place
            while (len(self.cache) >= self.max_entries or 
                   self.current_size_bytes + entry.size_bytes > self.max_size_bytes):
                self._evict_oldest()
            
            # Ajouter l'entrée
            self.cache[key] = entry
            self.current_size_bytes += entry.size_bytes
            
            # Persister si activé
            if self.enable_persistence and self.cache_dir:
                self._persist_entry(key, entry)
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout au cache: {e}")
            return False
    
    def _evict_oldest(self):
        """Évince l'entrée la plus ancienne du cache."""
        if not self.cache:
            return
        
        # Supprimer la première entrée (la plus ancienne)
        oldest_key = next(iter(self.cache))
        oldest_entry = self.cache[oldest_key]
        
        del self.cache[oldest_key]
        self.current_size_bytes -= oldest_entry.size_bytes
        self.stats["evictions"] += 1
        
        # Supprimer du disque si persistant
        if self.enable_persistence and self.cache_dir:
            self._remove_persistent_entry(oldest_key)
    
    def invalidate_by_dependency(self, dependency: str) -> int:
        """
        Invalide toutes les entrées dépendant d'une dépendance donnée.
        
        Args:
            dependency: Dépendance à invalider
            
        Returns:
            Nombre d'entrées invalidées
        """
        invalidated = 0
        keys_to_remove = []
        
        for key, entry in self.cache.items():
            if dependency in entry.dependencies:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            entry = self.cache[key]
            del self.cache[key]
            self.current_size_bytes -= entry.size_bytes
            invalidated += 1
            
            # Supprimer du disque si persistant
            if self.enable_persistence and self.cache_dir:
                self._remove_persistent_entry(key)
        
        return invalidated
    
    def clear(self):
        """Vide complètement le cache."""
        self.cache.clear()
        self.current_size_bytes = 0
        
        # Nettoyer le disque si persistant
        if self.enable_persistence and self.cache_dir:
            self._clear_persistent_cache()
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache."""
        hit_rate = 0
        if self.stats["hits"] + self.stats["misses"] > 0:
            hit_rate = self.stats["hits"] / (self.stats["hits"] + self.stats["misses"])
        
        return {
            **self.stats,
            "hit_rate": hit_rate,
            "current_entries": len(self.cache),
            "current_size_mb": self.current_size_bytes / (1024 * 1024),
            "max_size_mb": self.max_size_bytes / (1024 * 1024),
            "max_entries": self.max_entries
        }
    
    def _persist_entry(self, key: str, entry: CacheEntry):
        """Persiste une entrée sur disque."""
        if not self.cache_dir:
            return
        
        try:
            cache_file = self.cache_dir / f"{key}.cache"
            
            # Préparer les données pour la persistance
            persist_data = {
                "data": entry.data,
                "dependencies": entry.dependencies,
                "timestamp": entry.timestamp,
                "access_count": entry.access_count
            }
            
            with open(cache_file, 'wb') as f:
                pickle.dump(persist_data, f)
                
        except Exception as e:
            logger.error(f"Erreur lors de la persistance: {e}")
    
    def _remove_persistent_entry(self, key: str):
        """Supprime une entrée persistante du disque."""
        if not self.cache_dir:
            return
        
        try:
            cache_file = self.cache_dir / f"{key}.cache"
            if cache_file.exists():
                cache_file.unlink()
        except Exception as e:
            logger.error(f"Erreur lors de la suppression: {e}")
    
    def _load_persistent_cache(self):
        """Charge le cache depuis le disque."""
        if not self.cache_dir:
            return
        
        try:
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    with open(cache_file, 'rb') as f:
                        persist_data = pickle.load(f)
                    
                    key = cache_file.stem
                    entry = CacheEntry(
                        key=key,
                        data=persist_data["data"],
                        dependencies=persist_data.get("dependencies", [])
                    )
                    entry.timestamp = persist_data.get("timestamp", time.time())
                    entry.access_count = persist_data.get("access_count", 0)
                    
                    # Vérifier l'expiration avant de charger
                    if not entry.is_expired(24 * 3600):
                        self.cache[key] = entry
                        self.current_size_bytes += entry.size_bytes
                    else:
                        # Supprimer le fichier expiré
                        cache_file.unlink()
                        
                except Exception as e:
                    logger.error(f"Erreur lors du chargement de {cache_file}: {e}")
                    # Supprimer le fichier corrompu
                    try:
                        cache_file.unlink()
                    except Exception:
                        pass
                        
        except Exception as e:
            logger.error(f"Erreur lors du chargement du cache: {e}")
    
    def _clear_persistent_cache(self):
        """Nettoie le cache persistant sur disque."""
        if not self.cache_dir:
            return
        
        try:
            for cache_file in self.cache_dir.glob("*.cache"):
                cache_file.unlink()
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage du cache: {e}")


class HydraulicCacheManager(CacheManager):
    """Gestionnaire de cache spécialisé pour les calculs hydrauliques."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hydraulic_cache_prefix = "hydraulic"
    
    def cache_hydraulic_result(self, network_data: Dict[str, Any], 
                              solver_name: str, 
                              result: Dict[str, Any]) -> str:
        """
        Met en cache un résultat de calcul hydraulique.
        
        Args:
            network_data: Données du réseau
            solver_name: Nom du solveur utilisé
            result: Résultat du calcul
            
        Returns:
            Clé de cache générée
        """
        # Créer une clé basée sur les données du réseau et le solveur
        cache_data = {
            "network": network_data,
            "solver": solver_name,
            "timestamp": time.time()
        }
        
        key = self._generate_key(cache_data, self.hydraulic_cache_prefix)
        
        # Dépendances : hash des données du réseau
        network_hash = self._generate_key(network_data, "network")
        dependencies = [network_hash, solver_name]
        
        # Mettre en cache
        self.set(key, result, dependencies)
        
        return key
    
    def get_hydraulic_result(self, network_data: Dict[str, Any], 
                           solver_name: str) -> Optional[Dict[str, Any]]:
        """
        Récupère un résultat hydraulique du cache.
        
        Args:
            network_data: Données du réseau
            solver_name: Nom du solveur
            
        Returns:
            Résultat en cache ou None
        """
        # Créer la même clé que pour la mise en cache
        cache_data = {
            "network": network_data,
            "solver": solver_name,
            "timestamp": time.time()
        }
        
        key = self._generate_key(cache_data, self.hydraulic_cache_prefix)
        return self.get(key)
    
    def invalidate_network_cache(self, network_data: Dict[str, Any]) -> int:
        """
        Invalide le cache pour un réseau donné.
        
        Args:
            network_data: Données du réseau
            
        Returns:
            Nombre d'entrées invalidées
        """
        network_hash = self._generate_key(network_data, "network")
        return self.invalidate_by_dependency(network_hash)


# Instance globale du gestionnaire de cache
_default_cache_manager = None

def get_cache_manager(**kwargs) -> CacheManager:
    """Retourne l'instance globale du gestionnaire de cache."""
    global _default_cache_manager
    
    if _default_cache_manager is None:
        _default_cache_manager = HydraulicCacheManager(**kwargs)
    
    return _default_cache_manager


def clear_cache():
    """Vide le cache global."""
    global _default_cache_manager
    
    if _default_cache_manager:
        _default_cache_manager.clear()


def get_cache_stats() -> Dict[str, Any]:
    """Retourne les statistiques du cache global."""
    global _default_cache_manager
    
    if _default_cache_manager:
        return _default_cache_manager.get_stats()
    
    return {"error": "Cache non initialisé"}
