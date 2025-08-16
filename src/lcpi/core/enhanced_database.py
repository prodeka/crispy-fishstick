"""
Base de données améliorée LCPI avec traçabilité complète.
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)

class EnhancedDatabase:
    """Base de données LCPI avec traçabilité complète."""
    
    def __init__(self, db_path: Optional[Union[str, Path]] = None):
        """
        Initialise la base de données améliorée.
        
        Args:
            db_path: Chemin vers la base de données SQLite
        """
        if db_path is None:
            db_path = Path.home() / ".lcpi" / "database.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialiser la base de données
        self._initialize_database()
        logger.info(f"Base de données initialisée: {self.db_path}")
    
    def _initialize_database(self):
        """Initialise les tables de la base de données."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table des projets
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    description TEXT,
                    date_creation TEXT NOT NULL,
                    date_modification TEXT NOT NULL,
                    metadata TEXT,
                    statut TEXT DEFAULT 'actif',
                    hash_projet TEXT UNIQUE,
                    version TEXT DEFAULT '1.0.0'
                )
            """)
            
            # Table des calculs avec traçabilité
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS calculs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    commande TEXT NOT NULL,
                    resultats TEXT NOT NULL,
                    hash_donnees TEXT NOT NULL,
                    dependances TEXT,
                    date_creation TEXT NOT NULL,
                    duree_execution REAL,
                    version_algorithme TEXT,
                    metadata TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Table des dépendances entre calculs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dependances_calculs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    calcul_id INTEGER NOT NULL,
                    calcul_dependance_id INTEGER NOT NULL,
                    type_dependance TEXT DEFAULT 'input',
                    FOREIGN KEY (calcul_id) REFERENCES calculs (id),
                    FOREIGN KEY (calcul_dependance_id) REFERENCES calculs (id)
                )
            """)
            
            # Table des fichiers de données
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fichiers_donnees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    nom_fichier TEXT NOT NULL,
                    chemin_fichier TEXT NOT NULL,
                    type_fichier TEXT NOT NULL,
                    hash_fichier TEXT NOT NULL,
                    taille_fichier INTEGER,
                    date_ajout TEXT NOT NULL,
                    metadata TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Table des logs d'exécution
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs_execution (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    niveau TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    contexte TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Index pour améliorer les performances
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_calculs_projet ON calculs(projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_calculs_hash ON calculs(hash_donnees)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_fichiers_projet ON fichiers_donnees(projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_projet ON logs_execution(projet_id)")
            
            conn.commit()
    
    def ajouter_projet(self, nom: str, description: str = None, 
                      metadata: Dict[str, Any] = None) -> int:
        """
        Ajoute un nouveau projet.
        
        Args:
            nom: Nom du projet
            description: Description du projet
            metadata: Métadonnées supplémentaires
        
        Returns:
            ID du projet créé
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Calculer le hash du projet
            project_data = {
                "nom": nom,
                "description": description,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat()
            }
            hash_projet = self._calculate_hash(project_data)
            
            cursor.execute("""
                INSERT INTO projets (nom, description, date_creation, date_modification, 
                                   metadata, hash_projet)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nom, description, 
                datetime.now().isoformat(), 
                datetime.now().isoformat(),
                json.dumps(metadata or {}),
                hash_projet
            ))
            
            projet_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Projet créé: {nom} (ID: {projet_id})")
            return projet_id
    
    def ajouter_calcul(self, projet_id: int, commande: str, resultats: Dict[str, Any],
                      hash_donnees: str = None, dependances: List[int] = None,
                      duree_execution: float = None, version_algorithme: str = None,
                      metadata: Dict[str, Any] = None) -> int:
        """
        Ajoute un calcul avec traçabilité complète.
        
        Args:
            projet_id: ID du projet
            commande: Commande exécutée
            resultats: Résultats du calcul
            hash_donnees: Hash des données d'entrée (calculé automatiquement si None)
            dependances: Liste des IDs des calculs dont dépend ce calcul
            duree_execution: Durée d'exécution en secondes
            version_algorithme: Version de l'algorithme utilisé
            metadata: Métadonnées supplémentaires
        
        Returns:
            ID du calcul créé
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Calculer le hash des données d'entrée si non fourni
            if hash_donnees is None:
                hash_donnees = self._calculate_hash(resultats)
            
            # Vérifier les dépendances
            if dependances:
                for dep_id in dependances:
                    if not self._calcul_existe(dep_id):
                        raise ValueError(f"Dépendance {dep_id} non trouvée")
            
            # Insérer le calcul
            cursor.execute("""
                INSERT INTO calculs (projet_id, commande, resultats, hash_donnees, 
                                   dependances, date_creation, duree_execution, 
                                   version_algorithme, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                projet_id, commande, json.dumps(resultats), hash_donnees,
                json.dumps(dependances) if dependances else None,
                datetime.now().isoformat(), duree_execution,
                version_algorithme, json.dumps(metadata or {})
            ))
            
            calcul_id = cursor.lastrowid
            
            # Ajouter les dépendances
            if dependances:
                for dep_id in dependances:
                    cursor.execute("""
                        INSERT INTO dependances_calculs (calcul_id, calcul_dependance_id, type_dependance)
                        VALUES (?, ?, ?)
                    """, (calcul_id, dep_id, 'input'))
            
            conn.commit()
            
            logger.info(f"Calcul ajouté: {commande} (ID: {calcul_id})")
            return calcul_id
    
    def _calcul_existe(self, calcul_id: int) -> bool:
        """Vérifie si un calcul existe."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM calculs WHERE id = ?", (calcul_id,))
            return cursor.fetchone()[0] > 0
    
    def _calculate_hash(self, data: Any) -> str:
        """Calcule le hash SHA-256 des données."""
        if isinstance(data, dict):
            # Trier les clés pour un hash cohérent
            sorted_data = json.dumps(data, sort_keys=True, ensure_ascii=False)
        else:
            sorted_data = str(data)
        
        return hashlib.sha256(sorted_data.encode('utf-8')).hexdigest()
    
    def get_calcul(self, calcul_id: int) -> Optional[Dict[str, Any]]:
        """Récupère un calcul par son ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM calculs WHERE id = ?
            """, (calcul_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "projet_id": row[1],
                    "commande": row[2],
                    "resultats": json.loads(row[3]),
                    "hash_donnees": row[4],
                    "dependances": json.loads(row[5]) if row[5] else [],
                    "date_creation": row[6],
                    "duree_execution": row[7],
                    "version_algorithme": row[8],
                    "metadata": json.loads(row[9]) if row[9] else {}
                }
            return None
    
    def get_calculs_projet(self, projet_id: int) -> List[Dict[str, Any]]:
        """Récupère tous les calculs d'un projet."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM calculs WHERE projet_id = ? ORDER BY date_creation DESC
            """, (projet_id,))
            
            calculs = []
            for row in cursor.fetchall():
                calculs.append({
                    "id": row[0],
                    "projet_id": row[1],
                    "commande": row[2],
                    "resultats": json.loads(row[3]),
                    "hash_donnees": row[4],
                    "dependances": json.loads(row[5]) if row[5] else [],
                    "date_creation": row[6],
                    "duree_execution": row[7],
                    "version_algorithme": row[8],
                    "metadata": json.loads(row[9]) if row[9] else {}
                })
            
            return calculs
    
    def ajouter_log(self, projet_id: int, niveau: str, message: str, 
                   contexte: Dict[str, Any] = None):
        """Ajoute un log d'exécution."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO logs_execution (projet_id, niveau, message, timestamp, contexte)
                VALUES (?, ?, ?, ?, ?)
            """, (
                projet_id, niveau, message, 
                datetime.now().isoformat(),
                json.dumps(contexte or {})
            ))
            conn.commit()
    
    def get_historique_projet(self, projet_id: int, limite: int = 100) -> List[Dict[str, Any]]:
        """Récupère l'historique complet d'un projet."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, p.nom as nom_projet
                FROM calculs c
                JOIN projets p ON c.projet_id = p.id
                WHERE c.projet_id = ?
                ORDER BY c.date_creation DESC
                LIMIT ?
            """, (projet_id, limite))
            
            historique = []
            for row in cursor.fetchall():
                historique.append({
                    "id": row[0],
                    "projet_id": row[1],
                    "commande": row[2],
                    "resultats": json.loads(row[3]),
                    "hash_donnees": row[4],
                    "dependances": json.loads(row[5]) if row[5] else [],
                    "date_creation": row[6],
                    "duree_execution": row[7],
                    "version_algorithme": row[8],
                    "metadata": json.loads(row[9]) if row[9] else {},
                    "nom_projet": row[10]
                })
            
            return historique
