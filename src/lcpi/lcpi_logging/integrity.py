"""
Module de vérification d'intégrité des logs pour LCPI.
Gère la détection de corruption et la validation des logs.
"""

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import sqlite3

class IntegrityChecker:
    """Classe pour vérifier l'intégrité des logs LCPI."""
    
    def __init__(self, logs_directory: Optional[Path] = None):
        """
        Initialise le vérificateur d'intégrité.
        
        Args:
            logs_directory: Répertoire des logs à vérifier
        """
        self.logs_directory = logs_directory or Path("logs")
        self.db_path = self.logs_directory / "integrity.db"
        self._init_database()
    
    def _init_database(self):
        """Initialise la base de données d'intégrité."""
        self.logs_directory.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS log_integrity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    log_file TEXT UNIQUE NOT NULL,
                    file_hash TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    last_modified TIMESTAMP NOT NULL,
                    checksum_valid BOOLEAN NOT NULL,
                    signature_valid BOOLEAN,
                    verification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_log_file ON log_integrity(log_file)
            """)
            
            conn.commit()
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """
        Calcule le hash SHA-256 d'un fichier.
        
        Args:
            file_path: Chemin vers le fichier
            
        Returns:
            Hash SHA-256 en hexadécimal
        """
        hash_sha256 = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        
        return hash_sha256.hexdigest()
    
    def verify_log_integrity(self, log_file_path: Path) -> Dict[str, Any]:
        """
        Vérifie l'intégrité d'un fichier de log.
        
        Args:
            log_file_path: Chemin vers le fichier de log
            
        Returns:
            Résultat de la vérification
        """
        if not log_file_path.exists():
            return {
                "valid": False,
                "error": "Fichier non trouvé",
                "file_path": str(log_file_path)
            }
        
        try:
            # Informations de base du fichier
            stat = log_file_path.stat()
            file_size = stat.st_size
            last_modified = datetime.fromtimestamp(stat.st_mtime)
            
            # Calculer le hash du fichier
            file_hash = self.calculate_file_hash(log_file_path)
            
            # Lire et valider le contenu JSON
            with open(log_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                log_data = json.loads(content)
                content_valid = True
                json_error = None
            except json.JSONDecodeError as e:
                content_valid = False
                json_error = str(e)
                log_data = None
            
            # Vérifier la structure du log
            structure_valid = False
            if log_data:
                structure_valid = self._validate_log_structure(log_data)
            
            # Résultat global
            overall_valid = content_valid and structure_valid
            
            # Sauvegarder dans la base de données
            self._save_integrity_check(
                str(log_file_path), file_hash, file_size, last_modified,
                overall_valid, None
            )
            
            return {
                "valid": overall_valid,
                "file_path": str(log_file_path),
                "file_hash": file_hash,
                "file_size": file_size,
                "last_modified": last_modified.isoformat(),
                "content_valid": content_valid,
                "json_error": json_error,
                "structure_valid": structure_valid,
                "checksum_valid": True,
                "verification_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "file_path": str(log_file_path)
            }
    
    def _validate_log_structure(self, log_data: Dict[str, Any]) -> bool:
        """Valide la structure de base d'un log LCPI."""
        required_fields = ["timestamp", "calculation_type", "input_data"]
        
        for field in required_fields:
            if field not in log_data:
                return False
        
        return True
    
    def _save_integrity_check(self, log_file: str, file_hash: str, file_size: int,
                             last_modified: datetime, checksum_valid: bool,
                             signature_valid: Optional[bool]):
        """Sauvegarde le résultat d'une vérification d'intégrité."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO log_integrity 
                (log_file, file_hash, file_size, last_modified, checksum_valid, 
                 signature_valid, verification_date)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (log_file, file_hash, file_size, last_modified.isoformat(),
                  checksum_valid, signature_valid))
            conn.commit()
    
    def verify_all_logs(self) -> Dict[str, Any]:
        """Vérifie l'intégrité de tous les logs du répertoire."""
        if not self.logs_directory.exists():
            return {
                "valid": False,
                "error": "Répertoire des logs non trouvé",
                "logs_directory": str(self.logs_directory)
            }
        
        log_files = list(self.logs_directory.glob("*.json"))
        results = []
        valid_count = 0
        total_count = len(log_files)
        
        for log_file in log_files:
            result = self.verify_log_integrity(log_file)
            results.append(result)
            
            if result.get("valid", False):
                valid_count += 1
        
        return {
            "valid": valid_count == total_count,
            "total_logs": total_count,
            "valid_logs": valid_count,
            "corrupted_logs": total_count - valid_count,
            "logs_directory": str(self.logs_directory),
            "verification_date": datetime.now().isoformat(),
            "results": results
        }
    
    def get_integrity_history(self, log_file: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupère l'historique des vérifications d'intégrité."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            if log_file:
                cursor = conn.execute("""
                    SELECT * FROM log_integrity 
                    WHERE log_file = ? 
                    ORDER BY verification_date DESC
                """, (log_file,))
            else:
                cursor = conn.execute("""
                    SELECT * FROM log_integrity 
                    ORDER BY verification_date DESC
                """)
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def detect_corruption(self) -> List[Dict[str, Any]]:
        """Détecte les logs potentiellement corrompus."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            cursor = conn.execute("""
                SELECT * FROM log_integrity 
                WHERE checksum_valid = 0 OR signature_valid = 0
                ORDER BY verification_date DESC
            """)
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def export_integrity_report(self, output_path: Optional[Path] = None) -> str:
        """Exporte un rapport d'intégrité complet."""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.logs_directory / f"integrity_report_{timestamp}.json"
        
        verification_summary = self.verify_all_logs()
        history = self.get_integrity_history()
        corrupted = self.detect_corruption()
        
        report = {
            "report_info": {
                "generated_at": datetime.now().isoformat(),
                "logs_directory": str(self.logs_directory),
                "total_logs": verification_summary["total_logs"]
            },
            "verification_summary": verification_summary,
            "integrity_history": history,
            "corrupted_logs": corrupted,
            "recommendations": self._generate_recommendations(verification_summary, corrupted)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def _generate_recommendations(self, verification_summary: Dict[str, Any], 
                                 corrupted: List[Dict[str, Any]]) -> List[str]:
        """Génère des recommandations basées sur l'état des logs."""
        recommendations = []
        
        if verification_summary["corrupted_logs"] > 0:
            recommendations.append(
                f"⚠️  {verification_summary['corrupted_logs']} logs corrompus détectés. "
                "Vérifiez l'intégrité du système de fichiers."
            )
        
        if verification_summary["total_logs"] == 0:
            recommendations.append("ℹ️  Aucun log trouvé. Vérifiez la configuration des logs.")
        
        if corrupted:
            recommendations.append(
                "🔧 Certains logs nécessitent une attention. "
                "Vérifiez leur intégrité."
            )
        
        if not recommendations:
            recommendations.append("✅ Tous les logs sont en bon état.")
        
        return recommendations
