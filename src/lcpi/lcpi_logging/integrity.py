"""
Module d'intégrité des logs LCPI - Jalon 2.
Gère la signature et la vérification d'intégrité des logs de calcul.
"""

import json
import hashlib
import hmac
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import base64

class LogIntegrityManager:
    """Gère l'intégrité et la signature des logs LCPI."""
    
    def __init__(self, signing_key: Optional[str] = None):
        """
        Initialise le gestionnaire d'intégrité.
        
        Args:
            signing_key: Clé de signature (générée automatiquement si None)
        """
        self._signing_algorithm = "HMAC-SHA256"
        self._signing_key = signing_key or self._generate_signing_key()
        self._key_file = Path.home() / ".lcpi" / "signing_key"
        self._key_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder la clé si elle n'existe pas
        if not self._key_file.exists():
            self._save_signing_key()
    
    def _generate_signing_key(self) -> str:
        """Génère une nouvelle clé de signature sécurisée."""
        return base64.b64encode(os.urandom(32)).decode('utf-8')
    
    def _save_signing_key(self):
        """Sauvegarde la clé de signature de manière sécurisée."""
        try:
            # Sauvegarder avec permissions restrictives
            self._key_file.write_text(self._signing_key, encoding='utf-8')
            self._key_file.chmod(0o600)  # Lecture/écriture pour le propriétaire uniquement
        except Exception as e:
            # En cas d'erreur, utiliser la clé en mémoire
            pass
    
    def _load_signing_key(self) -> str:
        """Charge la clé de signature depuis le fichier."""
        try:
            if self._key_file.exists():
                return self._key_file.read_text(encoding='utf-8').strip()
        except Exception:
            pass
        return self._signing_key
    
    def sign_log(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Signe un log de calcul avec HMAC.
        
        Args:
            log_data: Données du log à signer
            
        Returns:
            Log avec métadonnées d'intégrité
        """
        # Créer une copie des données pour la signature
        data_to_sign = log_data.copy()
        
        # Ajouter un timestamp de signature
        signature_timestamp = time.time()
        data_to_sign["_signature_timestamp"] = signature_timestamp
        
        # Convertir en JSON pour la signature
        json_data = json.dumps(data_to_sign, sort_keys=True, ensure_ascii=False)
        
        # Calculer le checksum SHA-256
        checksum = hashlib.sha256(json_data.encode('utf-8')).hexdigest()
        
        # Calculer la signature HMAC
        signature = hmac.new(
            self._signing_key.encode('utf-8'),
            json_data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Ajouter les métadonnées d'intégrité
        log_data["integrity"] = {
            "checksum": checksum,
            "signature": signature,
            "signature_valid": True,
            "algorithm": self._signing_algorithm,
            "timestamp": signature_timestamp,
            "signed_at": datetime.fromtimestamp(signature_timestamp).isoformat()
        }
        
        return log_data
    
    def verify_log_integrity(self, log_file_path: Path) -> Dict[str, Any]:
        """
        Vérifie l'intégrité d'un log de calcul.
        
        Args:
            log_file_path: Chemin vers le fichier de log
            
        Returns:
            Résultat de la vérification
        """
        try:
            # Lire le fichier de log
            with open(log_file_path, 'r', encoding='utf-8') as f:
                log_content = json.load(f)
            
            # Extraire les métadonnées d'intégrité
            integrity_data = log_content.get("integrity", {})
            if not integrity_data:
                return {
                    "checksum_valid": False,
                    "signature_valid": False,
                    "overall_valid": False,
                    "error": "Aucune métadonnée d'intégrité trouvée"
                }
            
            # Vérifier le checksum
            checksum_valid = self._verify_checksum(log_content, integrity_data)
            
            # Vérifier la signature
            signature_valid = self._verify_signature(log_content, integrity_data)
            
            # Résultat global
            overall_valid = checksum_valid and signature_valid
            
            return {
                "checksum_valid": checksum_valid,
                "signature_valid": signature_valid,
                "overall_valid": overall_valid,
                "algorithm": integrity_data.get("algorithm", "Inconnu"),
                "signed_at": integrity_data.get("signed_at", "Inconnu"),
                "file_path": str(log_file_path)
            }
            
        except Exception as e:
            return {
                "checksum_valid": False,
                "signature_valid": False,
                "overall_valid": False,
                "error": f"Erreur lors de la vérification: {str(e)}"
            }
    
    def _verify_checksum(self, log_content: Dict[str, Any], integrity_data: Dict[str, Any]) -> bool:
        """Vérifie le checksum du log."""
        try:
            # Créer une copie sans les métadonnées d'intégrité
            data_for_checksum = log_content.copy()
            if "integrity" in data_for_checksum:
                del data_for_checksum["integrity"]
            
            # Ajouter le timestamp de signature
            signature_timestamp = integrity_data.get("_signature_timestamp")
            if signature_timestamp:
                data_for_checksum["_signature_timestamp"] = signature_timestamp
            
            # Calculer le checksum
            json_data = json.dumps(data_for_checksum, sort_keys=True, ensure_ascii=False)
            calculated_checksum = hashlib.sha256(json_data.encode('utf-8')).hexdigest()
            
            # Comparer avec le checksum stocké
            stored_checksum = integrity_data.get("checksum", "")
            return calculated_checksum == stored_checksum
            
        except Exception:
            return False
    
    def _verify_signature(self, log_content: Dict[str, Any], integrity_data: Dict[str, Any]) -> bool:
        """Vérifie la signature HMAC du log."""
        try:
            # Créer une copie sans les métadonnées d'intégrité
            data_for_signature = log_content.copy()
            if "integrity" in data_for_signature:
                del data_for_signature["integrity"]
            
            # Ajouter le timestamp de signature
            signature_timestamp = integrity_data.get("_signature_timestamp")
            if signature_timestamp:
                data_for_signature["_signature_timestamp"] = signature_timestamp
            
            # Convertir en JSON
            json_data = json.dumps(data_for_signature, sort_keys=True, ensure_ascii=False)
            
            # Calculer la signature
            calculated_signature = hmac.new(
                self._signing_key.encode('utf-8'),
                json_data.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Comparer avec la signature stockée
            stored_signature = integrity_data.get("signature", "")
            return calculated_signature == stored_signature
            
        except Exception:
            return False
    
    def verify_log_signature(self, log_file_path: Path) -> Dict[str, Any]:
        """
        Vérifie spécifiquement la signature d'un log.
        
        Args:
            log_file_path: Chemin vers le fichier de log
            
        Returns:
            Résultat de la vérification de signature
        """
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                log_content = json.load(f)
            
            integrity_data = log_content.get("integrity", {})
            if not integrity_data:
                return {
                    "valid": False,
                    "error": "Aucune métadonnée d'intégrité trouvée"
                }
            
            # Vérifier la signature
            signature_valid = self._verify_signature(log_content, integrity_data)
            
            return {
                "valid": signature_valid,
                "signature_info": {
                    "algorithm": integrity_data.get("algorithm", "Inconnu"),
                    "timestamp": integrity_data.get("signed_at", "Inconnu"),
                    "signature": integrity_data.get("signature", "")[:16] + "..."  # Afficher seulement le début
                }
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"Erreur lors de la vérification de signature: {str(e)}"
            }
    
    def verify_all_logs(self, logs_directory: Path) -> Dict[str, Any]:
        """
        Vérifie l'intégrité de tous les logs dans un répertoire.
        
        Args:
            logs_directory: Répertoire contenant les logs
            
        Returns:
            Résumé de la vérification
        """
        if not logs_directory.exists():
            return {
                "total_logs": 0,
                "valid_logs": 0,
                "invalid_logs": 0,
                "errors": ["Répertoire de logs non trouvé"]
            }
        
        log_files = list(logs_directory.glob("*.json"))
        results = {
            "total_logs": len(log_files),
            "valid_logs": 0,
            "invalid_logs": 0,
            "details": {}
        }
        
        for log_file in log_files:
            verification_result = self.verify_log_integrity(log_file)
            results["details"][log_file.name] = verification_result
            
            if verification_result.get("overall_valid", False):
                results["valid_logs"] += 1
            else:
                results["invalid_logs"] += 1
        
        return results
    
    def export_signing_key(self, output_path: Path) -> bool:
        """
        Exporte la clé de signature pour sauvegarde.
        
        Args:
            output_path: Chemin de sortie pour la clé
            
        Returns:
            True si l'export a réussi
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Créer un fichier de sauvegarde sécurisé
            backup_data = {
                "signing_key": self._signing_key,
                "algorithm": self._signing_algorithm,
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            # Définir des permissions restrictives
            output_path.chmod(0o600)
            
            return True
            
        except Exception:
            return False
    
    def import_signing_key(self, key_file_path: Path) -> bool:
        """
        Importe une clé de signature depuis un fichier.
        
        Args:
            key_file_path: Chemin vers le fichier de clé
            
        Returns:
            True si l'import a réussi
        """
        try:
            with open(key_file_path, 'r', encoding='utf-8') as f:
                key_data = json.load(f)
            
            new_key = key_data.get("signing_key")
            if new_key and len(new_key) >= 32:  # Vérification basique
                self._signing_key = new_key
                self._save_signing_key()
                return True
                
        except Exception:
            pass
        
        return False


# Instance globale pour utilisation dans d'autres modules
integrity_manager = LogIntegrityManager()


if __name__ == "__main__":
    # Test du module
    import tempfile
    import shutil
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Créer un log de test
        test_log = {
            "timestamp": "2025-08-17T14:00:00",
            "plugin": "aep",
            "command": "population",
            "parameters": {"debut": 2020, "fin": 2030},
            "results": {"population_2020": 15000}
        }
        
        # Signer le log
        manager = LogIntegrityManager()
        signed_log = manager.sign_log(test_log)
        
        # Sauvegarder le log signé
        log_file = temp_path / "test_log.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(signed_log, f, indent=2, ensure_ascii=False)
        
        # Vérifier l'intégrité
        verification_result = manager.verify_log_integrity(log_file)
        
        print("Test d'intégrité des logs:")
        print(f"Log signé: {log_file}")
        print(f"Vérification: {verification_result}")
        
        # Test de corruption
        with open(log_file, 'r', encoding='utf-8') as f:
            corrupted_log = json.load(f)
        
        corrupted_log["results"]["population_2020"] = 99999
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(corrupted_log, f, indent=2, ensure_ascii=False)
        
        # Vérifier que la corruption est détectée
        corruption_result = manager.verify_log_integrity(log_file)
        print(f"Détection de corruption: {corruption_result}")
