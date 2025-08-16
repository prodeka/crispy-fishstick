"""
Module de signature des logs pour LCPI.
Gère la signature et la vérification d'intégrité des logs.
"""

import hashlib
import hmac
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import base64

class LogSigner:
    """Classe pour signer les logs LCPI."""
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialise le signeur de logs.
        
        Args:
            secret_key: Clé secrète pour la signature. Si None, génère une clé aléatoire.
        """
        self.secret_key = secret_key or self._generate_secret_key()
        self.algorithm = "HMAC-SHA256"
    
    def _generate_secret_key(self) -> str:
        """Génère une clé secrète aléatoire."""
        return base64.b64encode(os.urandom(32)).decode('utf-8')
    
    def sign_log(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Signe un log avec HMAC.
        
        Args:
            log_data: Données du log à signer
            
        Returns:
            Log signé avec signature et métadonnées
        """
        # Créer une copie des données pour éviter la modification
        signed_log = log_data.copy()
        
        # Ajouter les métadonnées de signature
        signed_log["_signature"] = {
            "algorithm": self.algorithm,
            "timestamp": datetime.utcnow().isoformat(),
            "key_id": self._get_key_id()
        }
        
        # Calculer la signature
        signature = self._calculate_signature(signed_log)
        signed_log["_signature"]["signature"] = signature
        
        return signed_log
    
    def _calculate_signature(self, log_data: Dict[str, Any]) -> str:
        """
        Calcule la signature HMAC du log.
        
        Args:
            log_data: Données du log
            
        Returns:
            Signature en base64
        """
        # Exclure la signature existante du calcul
        data_to_sign = log_data.copy()
        if "_signature" in data_to_sign:
            del data_to_sign["_signature"]
        
        # Sérialiser les données de manière déterministe
        serialized = json.dumps(data_to_sign, sort_keys=True, separators=(',', ':'))
        
        # Calculer HMAC
        hmac_obj = hmac.new(
            self.secret_key.encode('utf-8'),
            serialized.encode('utf-8'),
            hashlib.sha256
        )
        
        return base64.b64encode(hmac_obj.digest()).decode('utf-8')
    
    def _get_key_id(self) -> str:
        """Génère un identifiant unique pour la clé."""
        key_hash = hashlib.sha256(self.secret_key.encode('utf-8')).hexdigest()
        return key_hash[:16]
    
    def get_public_key_info(self) -> Dict[str, str]:
        """Retourne les informations publiques de la clé."""
        return {
            "key_id": self._get_key_id(),
            "algorithm": self.algorithm,
            "created": datetime.utcnow().isoformat()
        }
    
    def export_key(self, output_path: Optional[Path] = None) -> str:
        """
        Exporte la clé secrète (à utiliser avec précaution).
        
        Args:
            output_path: Chemin de sortie pour la clé
            
        Returns:
            Chemin où la clé a été sauvegardée
        """
        if output_path is None:
            output_path = Path(f"lcpi_key_{self._get_key_id()}.key")
        
        key_data = {
            "secret_key": self.secret_key,
            "key_id": self._get_key_id(),
            "algorithm": self.algorithm,
            "created": datetime.utcnow().isoformat(),
            "warning": "⚠️  CLÉ SECRÈTE - À CONSERVER EN SÉCURITÉ"
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(key_data, f, indent=2, ensure_ascii=False)
        
        return str(output_path)

class LogVerifier:
    """Classe pour vérifier la signature des logs LCPI."""
    
    def __init__(self, secret_key: str):
        """
        Initialise le vérificateur de logs.
        
        Args:
            secret_key: Clé secrète pour la vérification
        """
        self.secret_key = secret_key
        self.algorithm = "HMAC-SHA256"
    
    def verify_log(self, signed_log: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Vérifie la signature d'un log.
        
        Args:
            signed_log: Log signé à vérifier
            
        Returns:
            Tuple (valide, message_d'erreur)
        """
        if "_signature" not in signed_log:
            return False, "Log non signé"
        
        signature_info = signed_log["_signature"]
        
        # Vérifier l'algorithme
        if signature_info.get("algorithm") != self.algorithm:
            return False, f"Algorithme non supporté: {signature_info.get('algorithm')}"
        
        # Vérifier la présence de la signature
        if "signature" not in signature_info:
            return False, "Signature manquante"
        
        # Calculer la signature attendue
        expected_signature = self._calculate_signature(signed_log)
        actual_signature = signature_info["signature"]
        
        # Comparer les signatures
        if not hmac.compare_digest(expected_signature, actual_signature):
            return False, "Signature invalide"
        
        return True, None
    
    def _calculate_signature(self, log_data: Dict[str, Any]) -> str:
        """
        Calcule la signature HMAC du log (même logique que LogSigner).
        
        Args:
            log_data: Données du log
            
        Returns:
            Signature en base64
        """
        # Exclure la signature existante du calcul
        data_to_sign = log_data.copy()
        if "_signature" in data_to_sign:
            del data_to_sign["_signature"]
        
        # Sérialiser les données de manière déterministe
        serialized = json.dumps(data_to_sign, sort_keys=True, separators=(',', ':'))
        
        # Calculer HMAC
        hmac_obj = hmac.new(
            self.secret_key.encode('utf-8'),
            serialized.encode('utf-8'),
            hashlib.sha256
        )
        
        return base64.b64encode(hmac_obj.digest()).decode('utf-8')
    
    def verify_log_file(self, log_file_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Vérifie la signature d'un fichier de log.
        
        Args:
            log_file_path: Chemin vers le fichier de log
            
        Returns:
            Tuple (valide, message_d'erreur)
        """
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            return self.verify_log(log_data)
            
        except FileNotFoundError:
            return False, f"Fichier non trouvé: {log_file_path}"
        except json.JSONDecodeError:
            return False, f"Fichier JSON invalide: {log_file_path}"
        except Exception as e:
            return False, f"Erreur lors de la lecture: {e}"
    
    def get_signature_info(self, signed_log: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrait les informations de signature d'un log.
        
        Args:
            signed_log: Log signé
            
        Returns:
            Informations de signature
        """
        if "_signature" not in signed_log:
            return {}
        
        signature_info = signed_log["_signature"].copy()
        
        # Ajouter des informations calculées
        if "timestamp" in signature_info:
            try:
                timestamp = datetime.fromisoformat(signature_info["timestamp"])
                signature_info["age_hours"] = (datetime.utcnow() - timestamp).total_seconds() / 3600
            except:
                signature_info["age_hours"] = None
        
        return signature_info
