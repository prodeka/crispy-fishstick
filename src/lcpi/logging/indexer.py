"""
Module d'indexation des logs pour LCPI.
Gère l'indexation SQLite pour la recherche et le filtrage des logs.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import hashlib

class LogIndexer:
    """Classe pour indexer et rechercher dans les logs LCPI."""
    
    def __init__(self, logs_directory: Optional[Path] = None):
        self.logs_directory = logs_directory or Path("logs")
        self.db_path = self.logs_directory / "logs_index.db"
        self._init_database()
    
    def _init_database(self):
        """Initialise la base de données d'indexation."""
        self.logs_directory.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    log_file TEXT UNIQUE NOT NULL,
                    log_id TEXT,
                    calculation_type TEXT,
                    timestamp TEXT,
                    solver TEXT,
                    input_hash TEXT,
                    output_hash TEXT,
                    duration REAL,
                    status TEXT,
                    tags TEXT,
                    metadata TEXT,
                    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("CREATE INDEX IF NOT EXISTS idx_calculation_type ON logs(calculation_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON logs(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_solver ON logs(solver)")
            conn.commit()
    
    def index_log_file(self, log_file_path: Path) -> Dict[str, Any]:
        """Indexe un fichier de log."""
        if not log_file_path.exists():
            return {"success": False, "error": "Fichier non trouvé"}
        
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            log_info = self._extract_log_info(log_data, log_file_path)
            log_id = self._save_log_to_db(log_info)
            
            return {
                "success": True,
                "log_id": log_id,
                "file_path": str(log_file_path)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _extract_log_info(self, log_data: Dict[str, Any], log_file_path: Path) -> Dict[str, Any]:
        """Extrait les informations d'un log pour l'indexation."""
        return {
            "log_file": str(log_file_path),
            "log_id": log_data.get("id", log_data.get("log_id")),
            "calculation_type": log_data.get("calculation_type"),
            "timestamp": log_data.get("timestamp"),
            "solver": log_data.get("solver"),
            "status": log_data.get("status", "completed"),
            "duration": log_data.get("duration"),
            "tags": json.dumps(log_data.get("tags", [])),
            "metadata": json.dumps(log_data.get("metadata", {}))
        }
    
    def _save_log_to_db(self, log_info: Dict[str, Any]) -> int:
        """Sauvegarde les informations de log dans la base de données."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT OR REPLACE INTO logs 
                (log_file, log_id, calculation_type, timestamp, solver, 
                 duration, status, tags, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                log_info["log_file"], log_info["log_id"], log_info["calculation_type"],
                log_info["timestamp"], log_info["solver"], log_info["duration"],
                log_info["status"], log_info["tags"], log_info["metadata"]
            ))
            
            conn.commit()
            return cursor.lastrowid
    
    def search_logs(self, query: str = None, filters: Dict[str, Any] = None,
                    limit: int = 100) -> List[Dict[str, Any]]:
        """Recherche dans les logs indexés."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            sql = "SELECT * FROM logs"
            params = []
            conditions = []
            
            if query:
                conditions.append("calculation_type LIKE ? OR solver LIKE ?")
                params.extend([f"%{query}%"] * 2)
            
            if filters:
                for key, value in filters.items():
                    if key in ["calculation_type", "solver", "status"]:
                        conditions.append(f"{key} = ?")
                        params.append(value)
            
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            
            sql += f" ORDER BY timestamp DESC LIMIT {limit}"
            
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Récupère des statistiques sur les logs indexés."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM logs")
            total_logs = cursor.fetchone()[0]
            
            cursor = conn.execute("""
                SELECT calculation_type, COUNT(*) as count 
                FROM logs GROUP BY calculation_type
            """)
            by_type = dict(cursor.fetchall())
            
            return {
                "total_logs": total_logs,
                "by_calculation_type": by_type,
                "indexed_at": datetime.now().isoformat()
            }
