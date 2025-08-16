"""
Module principal de logging pour LCPI.
Intègre la signature, l'intégrité et l'indexation des logs.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import hashlib

from .signature import LogSigner, LogVerifier
from .integrity import IntegrityChecker
from .indexer import LogIndexer

class LCPILogger:
    """Logger principal LCPI avec signature et intégrité."""
    
    def __init__(self, logs_directory: Optional[Path] = None, 
                 enable_signing: bool = True, enable_indexing: bool = True):
        """
        Initialise le logger LCPI.
        
        Args:
            logs_directory: Répertoire des logs
            enable_signing: Activer la signature des logs
            enable_indexing: Activer l'indexation des logs
        """
        self.logs_directory = logs_directory or Path("logs")
        self.logs_directory.mkdir(exist_ok=True)
        
        self.enable_signing = enable_signing
        self.enable_indexing = enable_indexing
        
        # Initialiser les composants
        if self.enable_signing:
            self.signer = LogSigner()
            self.verifier = LogVerifier(self.signer.secret_key)
        
        if self.enable_indexing:
            self.indexer = LogIndexer(self.logs_directory)
        
        self.integrity_checker = IntegrityChecker(self.logs_directory)
    
    def log_calculation(self, calculation_type: str, input_data: Dict[str, Any],
                        output_data: Dict[str, Any], solver: str = None,
                        duration: float = None, status: str = "completed",
                        tags: List[str] = None, metadata: Dict[str, Any] = None,
                        sign_log: bool = True) -> Dict[str, Any]:
        """
        Enregistre un calcul dans les logs.
        
        Args:
            calculation_type: Type de calcul (AEP, Hydro, Béton, etc.)
            input_data: Données d'entrée
            output_data: Données de sortie
            solver: Nom du solveur utilisé
            duration: Durée du calcul en secondes
            status: Statut du calcul
            tags: Tags pour catégoriser le log
            metadata: Métadonnées supplémentaires
            sign_log: Signer le log
            
        Returns:
            Informations sur le log créé
        """
        # Créer l'entrée de log
        log_entry = {
            "id": self._generate_log_id(),
            "timestamp": datetime.utcnow().isoformat(),
            "calculation_type": calculation_type,
            "solver": solver,
            "input_data": input_data,
            "output_data": output_data,
            "duration": duration,
            "status": status,
            "tags": tags or [],
            "metadata": metadata or {}
        }
        
        # Calculer le hash des données d'entrée
        log_entry["input_hash"] = self._calculate_data_hash(input_data)
        log_entry["output_hash"] = self._calculate_data_hash(output_data)
        
        # Signer le log si activé
        if self.enable_signing and sign_log:
            log_entry = self.signer.sign_log(log_entry)
        
        # Sauvegarder le log
        log_file = self._save_log(log_entry)
        
        # Indexer le log si activé
        if self.enable_indexing:
            try:
                self.indexer.index_log_file(log_file)
            except Exception as e:
                print(f"⚠️  Erreur lors de l'indexation: {e}")
        
        # Vérifier l'intégrité
        integrity_result = self.integrity_checker.verify_log_integrity(log_file)
        
        return {
            "log_id": log_entry["id"],
            "log_file": str(log_file),
            "timestamp": log_entry["timestamp"],
            "signed": self.enable_signing and sign_log,
            "indexed": self.enable_indexing,
            "integrity_valid": integrity_result.get("valid", False),
            "file_size": log_file.stat().st_size if log_file.exists() else 0
        }
    
    def _generate_log_id(self) -> str:
        """Génère un ID unique pour le log."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        random_part = os.urandom(4).hex()
        return f"log_{timestamp}_{random_part}"
    
    def _calculate_data_hash(self, data: Any) -> str:
        """Calcule le hash SHA-256 des données."""
        serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()
    
    def _save_log(self, log_entry: Dict[str, Any]) -> Path:
        """Sauvegarde le log dans un fichier JSON."""
        timestamp = datetime.fromisoformat(log_entry["timestamp"])
        filename = f"log_{timestamp.strftime('%Y%m%d_%H%M%S')}_{log_entry['id']}.json"
        log_file = self.logs_directory / filename
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, indent=2, ensure_ascii=False)
        
        return log_file
    
    def verify_log_signature(self, log_file_path: Path) -> Dict[str, Any]:
        """
        Vérifie la signature d'un log.
        
        Args:
            log_file_path: Chemin vers le fichier de log
            
        Returns:
            Résultat de la vérification
        """
        if not self.enable_signing:
            return {
                "valid": False,
                "error": "Signature non activée"
            }
        
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            is_valid, error_message = self.verifier.verify_log(log_data)
            signature_info = self.verifier.get_signature_info(log_data)
            
            return {
                "valid": is_valid,
                "error": error_message,
                "signature_info": signature_info,
                "file_path": str(log_file_path)
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "file_path": str(log_file_path)
            }
    
    def verify_log_integrity(self, log_file_path: Path) -> Dict[str, Any]:
        """
        Vérifie l'intégrité d'un log.
        
        Args:
            log_file_path: Chemin vers le fichier de log
            
        Returns:
            Résultat de la vérification
        """
        return self.integrity_checker.verify_log_integrity(log_file_path)
    
    def verify_all_logs(self) -> Dict[str, Any]:
        """Vérifie l'intégrité de tous les logs."""
        return self.integrity_checker.verify_all_logs()
    
    def search_logs(self, query: str = None, filters: Dict[str, Any] = None,
                    limit: int = 100) -> List[Dict[str, Any]]:
        """
        Recherche dans les logs indexés.
        
        Args:
            query: Requête de recherche
            filters: Filtres spécifiques
            limit: Nombre maximum de résultats
            
        Returns:
            Liste des logs correspondants
        """
        if not self.enable_indexing:
            return []
        
        return self.indexer.search_logs(query, filters, limit)
    
    def get_log_statistics(self) -> Dict[str, Any]:
        """Récupère des statistiques sur les logs."""
        if not self.enable_indexing:
            return {"error": "Indexation non activée"}
        
        return self.indexer.get_statistics()
    
    def export_integrity_report(self, output_path: Optional[Path] = None) -> str:
        """Exporte un rapport d'intégrité complet."""
        return self.integrity_checker.export_integrity_report(output_path)
    
    def get_public_key_info(self) -> Dict[str, str]:
        """Récupère les informations publiques de la clé de signature."""
        if not self.enable_signing:
            return {"error": "Signature non activée"}
        
        return self.signer.get_public_key_info()
    
    def export_signing_key(self, output_path: Optional[Path] = None) -> str:
        """Exporte la clé de signature (à utiliser avec précaution)."""
        if not self.enable_signing:
            raise RuntimeError("Signature non activée")
        
        return self.signer.export_key(output_path)
    
    def list_available_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Liste les logs disponibles.
        
        Args:
            limit: Nombre maximum de logs à retourner
            
        Returns:
            Liste des logs avec informations de base
        """
        if not self.logs_directory.exists():
            return []
        
        log_files = sorted(
            self.logs_directory.glob("*.json"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )[:limit]
        
        logs_info = []
        for log_file in log_files:
            try:
                stat = log_file.stat()
                logs_info.append({
                    "filename": log_file.name,
                    "file_path": str(log_file),
                    "size_bytes": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "age_hours": (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).total_seconds() / 3600
                })
            except Exception as e:
                logs_info.append({
                    "filename": log_file.name,
                    "file_path": str(log_file),
                    "error": str(e)
                })
        
        return logs_info
    
    def load_log_by_id(self, log_id: str) -> Optional[Dict[str, Any]]:
        """
        Charge un log par son ID.
        
        Args:
            log_id: ID du log à charger
            
        Returns:
            Contenu du log ou None
        """
        if not self.enable_indexing:
            return None
        
        # Rechercher dans l'index
        logs = self.indexer.search_logs(filters={"log_id": log_id}, limit=1)
        if not logs:
            return None
        
        log_file = Path(logs[0]["log_file"])
        if not log_file.exists():
            return None
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    def cleanup_old_logs(self, max_age: int = 30, dry_run: bool = True) -> Dict[str, Any]:
        """
        Nettoie les anciens logs.
        
        Args:
            max_age: Âge maximum des logs à conserver (en jours)
            dry_run: Mode simulation (ne supprime rien)
            
        Returns:
            Résumé du nettoyage
        """
        if not self.logs_directory.exists():
            return {"error": "Répertoire des logs non trouvé"}
        
        cutoff_time = datetime.now().timestamp() - (max_age * 24 * 3600)
        old_logs = []
        
        for log_file in self.logs_directory.glob("*.json"):
            if log_file.stat().st_mtime < cutoff_time:
                old_logs.append(log_file)
        
        if dry_run:
            return {
                "dry_run": True,
                "logs_to_remove": len(old_logs),
                "logs": [str(f) for f in old_logs],
                "max_age": max_age
            }
        else:
            removed_count = 0
            for log_file in old_logs:
                try:
                    log_file.unlink()
                    removed_count += 1
                except Exception:
                    pass
            
            return {
                "dry_run": False,
                "logs_removed": removed_count,
                "total_old_logs": len(old_logs),
                "max_age": max_age
            }

# Instance globale
logger = LCPILogger()

# Fonctions d'interface pour la compatibilité
def log_calculation_result(calculation_type: str, input_data: Dict[str, Any],
                          output_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """Interface de compatibilité pour l'enregistrement des calculs."""
    return logger.log_calculation(calculation_type, input_data, output_data, **kwargs)

def list_available_logs(limit: int = 50) -> List[Dict[str, Any]]:
    """Interface de compatibilité pour lister les logs."""
    return logger.list_available_logs(limit)

def load_log_by_id(log_id: str) -> Optional[Dict[str, Any]]:
    """Interface de compatibilité pour charger un log par ID."""
    return logger.load_log_by_id(log_id)
