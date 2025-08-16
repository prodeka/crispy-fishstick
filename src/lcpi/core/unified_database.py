"""
Base de données unifiée LCPI avec support complet pour tous les modules.
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)

class UnifiedDatabase:
    """Base de données LCPI unifiée avec support pour tous les modules."""
    
    def __init__(self, db_path: Optional[Union[str, Path]] = None):
        """
        Initialise la base de données unifiée.
        
        Args:
            db_path: Chemin vers la base de données SQLite
        """
        if db_path is None:
            db_path = Path.home() / ".lcpi" / "unified_database.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialiser la base de données
        self._initialize_database()
        logger.info(f"Base de données unifiée initialisée: {self.db_path}")
    
    def _initialize_database(self):
        """Initialise toutes les tables de la base de données."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # === TABLES GÉNÉRALES ===
            
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
                    version TEXT DEFAULT '1.0.0',
                    module_principal TEXT DEFAULT 'general'
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
                    module_source TEXT DEFAULT 'general',
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
                    module_source TEXT DEFAULT 'general',
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
                    module_source TEXT DEFAULT 'general',
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # === TABLES SPÉCIFIQUES AEP ===
            
            # Table des relevés terrain AEP
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS releves_terrain_aep (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    type_releve TEXT NOT NULL,
                    nom_point TEXT NOT NULL,
                    donnees TEXT NOT NULL,
                    coordonnees_gps TEXT,
                    altitude REAL,
                    operateur TEXT,
                    date_releve TEXT NOT NULL,
                    notes TEXT,
                    hash_donnees TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Table des résultats de calculs AEP
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resultats_calculs_aep (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    type_calcul TEXT NOT NULL,
                    nom_calcul TEXT NOT NULL,
                    parametres_entree TEXT NOT NULL,
                    resultats TEXT NOT NULL,
                    duree_calcul REAL,
                    version_algorithme TEXT,
                    date_calcul TEXT NOT NULL,
                    hash_donnees TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Table des plans et documents AEP
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS plans_documents_aep (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    type_document TEXT NOT NULL,
                    nom_fichier TEXT NOT NULL,
                    chemin_fichier TEXT NOT NULL,
                    taille_fichier INTEGER,
                    date_ajout TEXT NOT NULL,
                    description TEXT,
                    hash_fichier TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Table des réseaux AEP
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reseaux_aep (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    nom_reseau TEXT NOT NULL,
                    type_reseau TEXT NOT NULL,
                    caracteristiques TEXT NOT NULL,
                    date_creation TEXT NOT NULL,
                    date_modification TEXT NOT NULL,
                    metadata TEXT,
                    hash_reseau TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Table des nœuds AEP
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS noeuds_aep (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reseau_id INTEGER NOT NULL,
                    nom_noeud TEXT NOT NULL,
                    type_noeud TEXT NOT NULL,
                    coordonnees TEXT,
                    elevation REAL,
                    demande REAL,
                    pression_min REAL,
                    pression_max REAL,
                    metadata TEXT,
                    FOREIGN KEY (reseau_id) REFERENCES reseaux_aep (id)
                )
            """)
            
            # Table des tronçons AEP
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS troncons_aep (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reseau_id INTEGER NOT NULL,
                    nom_troncon TEXT NOT NULL,
                    noeud_debut TEXT NOT NULL,
                    noeud_fin TEXT NOT NULL,
                    longueur REAL,
                    diametre REAL,
                    rugosite REAL,
                    type_materiau TEXT,
                    metadata TEXT,
                    FOREIGN KEY (reseau_id) REFERENCES reseaux_aep (id)
                )
            """)
            
            # === TABLES SPÉCIFIQUES AUTRES MODULES ===
            
            # Table des structures CM (Construction Métallique)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS structures_cm (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    nom_structure TEXT NOT NULL,
                    type_structure TEXT NOT NULL,
                    caracteristiques TEXT NOT NULL,
                    calculs TEXT,
                    date_creation TEXT NOT NULL,
                    metadata TEXT,
                    hash_structure TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Table des éléments bois
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS elements_bois (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    nom_element TEXT NOT NULL,
                    type_bois TEXT NOT NULL,
                    dimensions TEXT NOT NULL,
                    proprietes TEXT,
                    calculs TEXT,
                    date_creation TEXT NOT NULL,
                    metadata TEXT,
                    hash_element TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Table des éléments béton
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS elements_beton (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    nom_element TEXT NOT NULL,
                    type_beton TEXT NOT NULL,
                    caracteristiques TEXT NOT NULL,
                    armatures TEXT,
                    calculs TEXT,
                    date_creation TEXT NOT NULL,
                    metadata TEXT,
                    hash_element TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # === INDEX POUR PERFORMANCES ===
            
            # Index généraux
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_calculs_projet ON calculs(projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_calculs_hash ON calculs(hash_donnees)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_calculs_module ON calculs(module_source)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_fichiers_projet ON fichiers_donnees(projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_projet ON logs_execution(projet_id)")
            
            # Index AEP
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_releves_projet ON releves_terrain_aep(projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_resultats_projet ON resultats_calculs_aep(projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reseaux_projet ON reseaux_aep(projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_noeuds_reseau ON noeuds_aep(reseau_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_troncons_reseau ON troncons_aep(reseau_id)")
            
            # Index autres modules
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_structures_projet ON structures_cm(projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_elements_bois_projet ON elements_bois(projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_elements_beton_projet ON elements_beton(projet_id)")
            
            conn.commit()
    
    # === MÉTHODES GÉNÉRALES ===
    
    def ajouter_projet(self, nom: str, description: str = None, 
                      metadata: Dict[str, Any] = None, module_principal: str = "general") -> int:
        """Ajoute un nouveau projet."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Calculer le hash du projet
            project_data = {
                "nom": nom,
                "description": description,
                "metadata": metadata or {},
                "module_principal": module_principal,
                "timestamp": datetime.now().isoformat()
            }
            hash_projet = self._calculate_hash(project_data)
            
            cursor.execute("""
                INSERT INTO projets (nom, description, date_creation, date_modification, 
                                   metadata, hash_projet, module_principal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                nom, description, 
                datetime.now().isoformat(), 
                datetime.now().isoformat(),
                json.dumps(metadata or {}),
                hash_projet,
                module_principal
            ))
            
            projet_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Projet créé: {nom} (ID: {projet_id}, Module: {module_principal})")
            return projet_id
    
    def ajouter_calcul(self, projet_id: int, commande: str, resultats: Dict[str, Any],
                      hash_donnees: str = None, dependances: List[int] = None,
                      duree_execution: float = None, version_algorithme: str = None,
                      metadata: Dict[str, Any] = None, module_source: str = "general") -> int:
        """Ajoute un calcul avec traçabilité complète."""
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
                                   version_algorithme, metadata, module_source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                projet_id, commande, json.dumps(resultats), hash_donnees,
                json.dumps(dependances) if dependances else None,
                datetime.now().isoformat(), duree_execution,
                version_algorithme, json.dumps(metadata or {}), module_source
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
            
            logger.info(f"Calcul ajouté: {commande} (ID: {calcul_id}, Module: {module_source})")
            return calcul_id
    
    # === MÉTHODES SPÉCIFIQUES AEP ===
    
    def ajouter_releve_terrain_aep(self, projet_id: int, type_releve: str, nom_point: str,
                                  donnees: Dict[str, Any], coordonnees_gps: str = None,
                                  altitude: float = None, operateur: str = None,
                                  notes: str = None) -> int:
        """Ajoute un relevé terrain AEP."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            hash_donnees = self._calculate_hash(donnees)
            
            cursor.execute("""
                INSERT INTO releves_terrain_aep (projet_id, type_releve, nom_point, donnees,
                                               coordonnees_gps, altitude, operateur, date_releve, notes, hash_donnees)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                projet_id, type_releve, nom_point, json.dumps(donnees),
                coordonnees_gps, altitude, operateur, datetime.now().isoformat(), notes, hash_donnees
            ))
            
            releve_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Relevé terrain AEP ajouté: {type_releve} - {nom_point} (ID: {releve_id})")
            return releve_id
    
    def ajouter_resultat_calcul_aep(self, projet_id: int, type_calcul: str, nom_calcul: str,
                                   parametres_entree: Dict[str, Any], resultats: Dict[str, Any],
                                   duree_calcul: float = None, version_algorithme: str = None) -> int:
        """Ajoute un résultat de calcul AEP."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            hash_donnees = self._calculate_hash(resultats)
            
            cursor.execute("""
                INSERT INTO resultats_calculs_aep (projet_id, type_calcul, nom_calcul,
                                                 parametres_entree, resultats, duree_calcul,
                                                 version_algorithme, date_calcul, hash_donnees)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                projet_id, type_calcul, nom_calcul, json.dumps(parametres_entree),
                json.dumps(resultats), duree_calcul, version_algorithme,
                datetime.now().isoformat(), hash_donnees
            ))
            
            resultat_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Résultat calcul AEP ajouté: {type_calcul} - {nom_calcul} (ID: {resultat_id})")
            return resultat_id
    
    def ajouter_reseau_aep(self, projet_id: int, nom_reseau: str, type_reseau: str,
                          caracteristiques: Dict[str, Any], metadata: Dict[str, Any] = None) -> int:
        """Ajoute un réseau AEP."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            hash_reseau = self._calculate_hash({
                "nom": nom_reseau,
                "type": type_reseau,
                "caracteristiques": caracteristiques,
                "timestamp": datetime.now().isoformat()
            })
            
            cursor.execute("""
                INSERT INTO reseaux_aep (projet_id, nom_reseau, type_reseau, caracteristiques,
                                        date_creation, date_modification, metadata, hash_reseau)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                projet_id, nom_reseau, type_reseau, json.dumps(caracteristiques),
                datetime.now().isoformat(), datetime.now().isoformat(),
                json.dumps(metadata or {}), hash_reseau
            ))
            
            reseau_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Réseau AEP ajouté: {nom_reseau} (ID: {reseau_id})")
            return reseau_id
    
    def ajouter_noeud_aep(self, reseau_id: int, nom_noeud: str, type_noeud: str,
                          coordonnees: str = None, elevation: float = None, demande: float = None,
                          pression_min: float = None, pression_max: float = None,
                          metadata: Dict[str, Any] = None) -> int:
        """Ajoute un nœud AEP."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO noeuds_aep (reseau_id, nom_noeud, type_noeud, coordonnees,
                                       elevation, demande, pression_min, pression_max, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                reseau_id, nom_noeud, type_noeud, coordonnees,
                elevation, demande, pression_min, pression_max,
                json.dumps(metadata or {})
            ))
            
            noeud_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Nœud AEP ajouté: {nom_noeud} (ID: {noeud_id})")
            return noeud_id
    
    def ajouter_troncon_aep(self, reseau_id: int, nom_troncon: str, noeud_debut: str,
                           noeud_fin: str, longueur: float, diametre: float = None,
                           rugosite: float = None, type_materiau: str = None,
                           metadata: Dict[str, Any] = None) -> int:
        """Ajoute un tronçon AEP."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO troncons_aep (reseau_id, nom_troncon, noeud_debut, noeud_fin,
                                         longueur, diametre, rugosite, type_materiau, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                reseau_id, nom_troncon, noeud_debut, noeud_fin,
                longueur, diametre, rugosite, type_materiau,
                json.dumps(metadata or {})
            ))
            
            troncon_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Tronçon AEP ajouté: {nom_troncon} (ID: {troncon_id})")
            return troncon_id
    
    # === MÉTHODES DE RÉCUPÉRATION ===
    
    def get_projet(self, projet_id: int) -> Optional[Dict[str, Any]]:
        """Récupère un projet par son ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projets WHERE id = ?", (projet_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "nom": row[1],
                    "description": row[2],
                    "date_creation": row[3],
                    "date_modification": row[4],
                    "metadata": json.loads(row[5]) if row[5] else {},
                    "statut": row[6],
                    "hash_projet": row[7],
                    "version": row[8],
                    "module_principal": row[9]
                }
            return None
    
    def get_projets_par_module(self, module: str) -> List[Dict[str, Any]]:
        """Récupère tous les projets d'un module spécifique."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM projets WHERE module_principal = ? ORDER BY date_creation DESC
            """, (module,))
            
            projets = []
            for row in cursor.fetchall():
                projets.append({
                    "id": row[0],
                    "nom": row[1],
                    "description": row[2],
                    "date_creation": row[3],
                    "date_modification": row[4],
                    "metadata": json.loads(row[5]) if row[5] else {},
                    "statut": row[6],
                    "hash_projet": row[7],
                    "version": row[8],
                    "module_principal": row[9]
                })
            
            return projets
    
    def get_reseau_aep_complet(self, reseau_id: int) -> Optional[Dict[str, Any]]:
        """Récupère un réseau AEP complet avec ses nœuds et tronçons."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Récupérer le réseau
            cursor.execute("SELECT * FROM reseaux_aep WHERE id = ?", (reseau_id,))
            reseau_row = cursor.fetchone()
            if not reseau_row:
                return None
            
            reseau = {
                "id": reseau_row[0],
                "projet_id": reseau_row[1],
                "nom_reseau": reseau_row[2],
                "type_reseau": reseau_row[3],
                "caracteristiques": json.loads(reseau_row[4]),
                "date_creation": reseau_row[5],
                "date_modification": reseau_row[6],
                "metadata": json.loads(reseau_row[7]) if reseau_row[7] else {},
                "hash_reseau": reseau_row[8],
                "noeuds": [],
                "troncons": []
            }
            
            # Récupérer les nœuds
            cursor.execute("SELECT * FROM noeuds_aep WHERE reseau_id = ?", (reseau_id,))
            for row in cursor.fetchall():
                reseau["noeuds"].append({
                    "id": row[0],
                    "reseau_id": row[1],
                    "nom_noeud": row[2],
                    "type_noeud": row[3],
                    "coordonnees": row[4],
                    "elevation": row[5],
                    "demande": row[6],
                    "pression_min": row[7],
                    "pression_max": row[8],
                    "metadata": json.loads(row[9]) if row[9] else {}
                })
            
            # Récupérer les tronçons
            cursor.execute("SELECT * FROM troncons_aep WHERE reseau_id = ?", (reseau_id,))
            for row in cursor.fetchall():
                reseau["troncons"].append({
                    "id": row[0],
                    "reseau_id": row[1],
                    "nom_troncon": row[2],
                    "noeud_debut": row[3],
                    "noeud_fin": row[4],
                    "longueur": row[5],
                    "diametre": row[6],
                    "rugosite": row[7],
                    "type_materiau": row[8],
                    "metadata": json.loads(row[9]) if row[9] else {}
                })
            
            return reseau
    
    # === MÉTHODES UTILITAIRES ===
    
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
    
    def ajouter_log(self, projet_id: int, niveau: str, message: str, 
                   contexte: Dict[str, Any] = None, module_source: str = "general"):
        """Ajoute un log d'exécution."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO logs_execution (projet_id, niveau, message, timestamp, contexte, module_source)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                projet_id, niveau, message, 
                datetime.now().isoformat(),
                json.dumps(contexte or {}),
                module_source
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
                    "module_source": row[10],
                    "nom_projet": row[11]
                })
            
            return historique
