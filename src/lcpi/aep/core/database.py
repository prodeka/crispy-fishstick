"""
Base de données centralisée pour les projets AEP

Ce module fournit une interface unifiée pour stocker et récupérer
les données des projets AEP : relevés terrain, plans, résultats de calculs,
historiques, etc.
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import logging

class AEPDatabase:
    """Gestionnaire de base de données centralisée pour les projets AEP"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialise la base de données
        
        Args:
            db_path: Chemin vers la base de données SQLite
        """
        if db_path is None:
            db_path = os.path.join(os.path.expanduser("~"), ".lcpi", "aep", "database.db")
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialiser la base de données
        self._initialiser_base()
        
        # Logger
        self.logger = logging.getLogger(__name__)
    
    def _initialiser_base(self):
        """Initialise les tables de la base de données"""
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
                    statut TEXT DEFAULT 'actif'
                )
            """)
            
            # Table des relevés terrain
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS releves_terrain (
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
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Table des résultats de calculs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resultats_calculs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    type_calcul TEXT NOT NULL,
                    nom_calcul TEXT NOT NULL,
                    parametres_entree TEXT NOT NULL,
                    resultats TEXT NOT NULL,
                    duree_calcul REAL,
                    version_algorithme TEXT,
                    date_calcul TEXT NOT NULL,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Table des plans et documents
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS plans_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    type_document TEXT NOT NULL,
                    nom_fichier TEXT NOT NULL,
                    chemin_fichier TEXT NOT NULL,
                    taille_fichier INTEGER,
                    date_ajout TEXT NOT NULL,
                    description TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Table des historiques de modifications
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historiques_modifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projet_id INTEGER NOT NULL,
                    type_entite TEXT NOT NULL,
                    id_entite INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    utilisateur TEXT NOT NULL,
                    date_modification TEXT NOT NULL,
                    details TEXT,
                    FOREIGN KEY (projet_id) REFERENCES projets (id)
                )
            """)
            
            # Index pour améliorer les performances
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_releves_projet ON releves_terrain (projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_resultats_projet ON resultats_calculs (projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_plans_projet ON plans_documents (projet_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_historiques_projet ON historiques_modifications (projet_id)")
            
            conn.commit()
    
    def obtenir_info_base(self) -> Dict[str, Any]:
        """
        Obtient les informations sur la base de données
        
        Returns:
            Dictionnaire avec les informations de la base
        """
        info = {
            "chemin": str(self.db_path),
            "taille_fichier": self.db_path.stat().st_size if self.db_path.exists() else 0,
            "tables": []
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            info["tables"] = [row[0] for row in cursor.fetchall()]
        
        return info
    
    def ajouter_projet(
        self,
        nom: str,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Ajoute un nouveau projet
        
        Args:
            nom: Nom du projet
            description: Description du projet
            metadata: Métadonnées supplémentaires
            
        Returns:
            ID du projet créé
        """
        date_actuelle = datetime.now().isoformat()
        metadata_json = json.dumps(metadata) if metadata else None
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO projets (nom, description, date_creation, date_modification, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (nom, description, date_actuelle, date_actuelle, metadata_json))
            
            projet_id = cursor.lastrowid
            conn.commit()
            
            # Logger l'action
            self._ajouter_historique(projet_id, "projet", projet_id, "creation", "system", f"Création du projet '{nom}'")
            
            return projet_id
    
    def obtenir_projets(self) -> List[Dict[str, Any]]:
        """
        Obtient tous les projets
        
        Returns:
            Liste des projets
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projets ORDER BY date_creation DESC")
            
            projets = []
            for row in cursor.fetchall():
                projet = dict(row)
                if projet["metadata"]:
                    projet["metadata"] = json.loads(projet["metadata"])
                projets.append(projet)
            
            return projets
    
    def ajouter_releve_terrain(
        self,
        projet_id: int,
        type_releve: str,
        nom_point: str,
        donnees: Dict[str, Any],
        coordonnees_gps: Optional[str] = None,
        altitude: Optional[float] = None,
        operateur: Optional[str] = None,
        notes: Optional[str] = None
    ) -> int:
        """
        Ajoute un relevé terrain
        
        Args:
            projet_id: ID du projet
            type_releve: Type de relevé (forage, pompe, reservoir, etc.)
            nom_point: Nom du point de relevé
            donnees: Données du relevé
            coordonnees_gps: Coordonnées GPS
            altitude: Altitude
            operateur: Nom de l'opérateur
            notes: Notes supplémentaires
            
        Returns:
            ID du relevé créé
        """
        date_actuelle = datetime.now().isoformat()
        donnees_json = json.dumps(donnees)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO releves_terrain 
                (projet_id, type_releve, nom_point, donnees, coordonnees_gps, altitude, operateur, date_releve, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (projet_id, type_releve, nom_point, donnees_json, coordonnees_gps, altitude, operateur, date_actuelle, notes))
            
            releve_id = cursor.lastrowid
            conn.commit()
            
            # Logger l'action
            self._ajouter_historique(projet_id, "releve", releve_id, "creation", operateur or "system", f"Ajout du relevé '{nom_point}'")
            
            return releve_id
    
    def obtenir_releves_projet(
        self,
        projet_id: int,
        type_releve: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtient les relevés d'un projet
        
        Args:
            projet_id: ID du projet
            type_releve: Type de relevé à filtrer (optionnel)
            
        Returns:
            Liste des relevés
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if type_releve:
                cursor.execute("""
                    SELECT * FROM releves_terrain 
                    WHERE projet_id = ? AND type_releve = ?
                    ORDER BY date_releve DESC
                """, (projet_id, type_releve))
            else:
                cursor.execute("""
                    SELECT * FROM releves_terrain 
                    WHERE projet_id = ?
                    ORDER BY date_releve DESC
                """, (projet_id,))
            
            releves = []
            for row in cursor.fetchall():
                releve = dict(row)
                releve["donnees"] = json.loads(releve["donnees"])
                releves.append(releve)
            
            return releves
    
    def sauvegarder_resultat_calcul(
        self,
        projet_id: int,
        type_calcul: str,
        nom_calcul: str,
        parametres_entree: Dict[str, Any],
        resultats: Dict[str, Any],
        duree_calcul: Optional[float] = None,
        version_algorithme: Optional[str] = None
    ) -> int:
        """
        Sauvegarde un résultat de calcul
        
        Args:
            projet_id: ID du projet
            type_calcul: Type de calcul (hardy_cross, population, etc.)
            nom_calcul: Nom du calcul
            parametres_entree: Paramètres d'entrée
            resultats: Résultats du calcul
            duree_calcul: Durée du calcul en secondes
            version_algorithme: Version de l'algorithme
            
        Returns:
            ID du résultat créé
        """
        date_actuelle = datetime.now().isoformat()
        parametres_json = json.dumps(parametres_entree)
        resultats_json = json.dumps(resultats)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO resultats_calculs 
                (projet_id, type_calcul, nom_calcul, parametres_entree, resultats, duree_calcul, version_algorithme, date_calcul)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (projet_id, type_calcul, nom_calcul, parametres_json, resultats_json, duree_calcul, version_algorithme, date_actuelle))
            
            resultat_id = cursor.lastrowid
            conn.commit()
            
            # Logger l'action
            self._ajouter_historique(projet_id, "calcul", resultat_id, "creation", "system", f"Sauvegarde du calcul '{nom_calcul}'")
            
            return resultat_id
    
    def obtenir_resultats_calculs(
        self,
        projet_id: int,
        type_calcul: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtient les résultats de calculs d'un projet
        
        Args:
            projet_id: ID du projet
            type_calcul: Type de calcul à filtrer (optionnel)
            
        Returns:
            Liste des résultats
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if type_calcul:
                cursor.execute("""
                    SELECT * FROM resultats_calculs 
                    WHERE projet_id = ? AND type_calcul = ?
                    ORDER BY date_calcul DESC
                """, (projet_id, type_calcul))
            else:
                cursor.execute("""
                    SELECT * FROM resultats_calculs 
                    WHERE projet_id = ?
                    ORDER BY date_calcul DESC
                """, (projet_id,))
            
            resultats = []
            for row in cursor.fetchall():
                resultat = dict(row)
                resultat["parametres_entree"] = json.loads(resultat["parametres_entree"])
                resultat["resultats"] = json.loads(resultat["resultats"])
                resultats.append(resultat)
            
            return resultats
    
    def ajouter_plan_document(
        self,
        projet_id: int,
        type_document: str,
        nom_fichier: str,
        chemin_fichier: str,
        description: Optional[str] = None
    ) -> int:
        """
        Ajoute un plan ou document
        
        Args:
            projet_id: ID du projet
            type_document: Type de document (plan, photo, rapport, etc.)
            nom_fichier: Nom du fichier
            chemin_fichier: Chemin vers le fichier
            description: Description du document
            
        Returns:
            ID du document créé
        """
        date_actuelle = datetime.now().isoformat()
        taille_fichier = Path(chemin_fichier).stat().st_size if Path(chemin_fichier).exists() else 0
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO plans_documents 
                (projet_id, type_document, nom_fichier, chemin_fichier, taille_fichier, date_ajout, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (projet_id, type_document, nom_fichier, chemin_fichier, taille_fichier, date_actuelle, description))
            
            document_id = cursor.lastrowid
            conn.commit()
            
            # Logger l'action
            self._ajouter_historique(projet_id, "document", document_id, "creation", "system", f"Ajout du document '{nom_fichier}'")
            
            return document_id
    
    def obtenir_statistiques_projet(self, projet_id: int) -> Dict[str, Any]:
        """
        Obtient les statistiques d'un projet
        
        Args:
            projet_id: ID du projet
            
        Returns:
            Statistiques du projet
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Statistiques des relevés par type
            cursor.execute("""
                SELECT type_releve, COUNT(*) as count 
                FROM releves_terrain 
                WHERE projet_id = ?
                GROUP BY type_releve
            """, (projet_id,))
            releves_par_type = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Statistiques des calculs par type
            cursor.execute("""
                SELECT type_calcul, COUNT(*) as count 
                FROM resultats_calculs 
                WHERE projet_id = ?
                GROUP BY type_calcul
            """, (projet_id,))
            calculs_par_type = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Statistiques des documents par type
            cursor.execute("""
                SELECT type_document, COUNT(*) as count 
                FROM plans_documents 
                WHERE projet_id = ?
                GROUP BY type_document
            """, (projet_id,))
            documents_par_type = {row[0]: row[1] for row in cursor.fetchall()}
            
            return {
                "releves_par_type": releves_par_type,
                "calculs_par_type": calculs_par_type,
                "documents_par_type": documents_par_type,
                "total_releves": sum(releves_par_type.values()),
                "total_calculs": sum(calculs_par_type.values()),
                "total_documents": sum(documents_par_type.values())
            }
    
    def rechercher_donnees(
        self,
        projet_id: int,
        terme: str,
        types_entites: Optional[List[str]] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Recherche des données dans un projet
        
        Args:
            projet_id: ID du projet
            terme: Terme de recherche
            types_entites: Types d'entités à rechercher (optionnel)
            
        Returns:
            Résultats de recherche par type
        """
        resultats = {
            "releves": [],
            "calculs": [],
            "documents": []
        }
        
        terme_lower = terme.lower()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Recherche dans les relevés
            if not types_entites or "releves" in types_entites:
                cursor.execute("""
                    SELECT * FROM releves_terrain 
                    WHERE projet_id = ? AND (
                        LOWER(nom_point) LIKE ? OR 
                        LOWER(type_releve) LIKE ? OR 
                        LOWER(notes) LIKE ?
                    )
                """, (projet_id, f"%{terme_lower}%", f"%{terme_lower}%", f"%{terme_lower}%"))
                
                for row in cursor.fetchall():
                    releve = dict(row)
                    releve["donnees"] = json.loads(releve["donnees"])
                    resultats["releves"].append(releve)
            
            # Recherche dans les calculs
            if not types_entites or "calculs" in types_entites:
                cursor.execute("""
                    SELECT * FROM resultats_calculs 
                    WHERE projet_id = ? AND (
                        LOWER(nom_calcul) LIKE ? OR 
                        LOWER(type_calcul) LIKE ?
                    )
                """, (projet_id, f"%{terme_lower}%", f"%{terme_lower}%"))
                
                for row in cursor.fetchall():
                    resultat = dict(row)
                    resultat["parametres_entree"] = json.loads(resultat["parametres_entree"])
                    resultat["resultats"] = json.loads(resultat["resultats"])
                    resultats["calculs"].append(resultat)
            
            # Recherche dans les documents
            if not types_entites or "documents" in types_entites:
                cursor.execute("""
                    SELECT * FROM plans_documents 
                    WHERE projet_id = ? AND (
                        LOWER(nom_fichier) LIKE ? OR 
                        LOWER(type_document) LIKE ? OR 
                        LOWER(description) LIKE ?
                    )
                """, (projet_id, f"%{terme_lower}%", f"%{terme_lower}%", f"%{terme_lower}%"))
                
                for row in cursor.fetchall():
                    resultats["documents"].append(dict(row))
        
        return resultats
    
    def exporter_projet(self, projet_id: int, format_sortie: str = "json") -> str:
        """
        Exporte un projet complet
        
        Args:
            projet_id: ID du projet
            format_sortie: Format de sortie (json, yaml)
            
        Returns:
            Projet exporté
        """
        # Récupérer le projet
        projets = [p for p in self.obtenir_projets() if p["id"] == projet_id]
        if not projets:
            raise ValueError(f"Projet {projet_id} non trouvé")
        
        projet = projets[0]
        
        # Récupérer les données associées
        releves = self.obtenir_releves_projet(projet_id)
        resultats = self.obtenir_resultats_calculs(projet_id)
        
        # Construire l'export
        export_data = {
            "projet": projet,
            "releves_terrain": releves,
            "resultats_calculs": resultats,
            "statistiques": self.obtenir_statistiques_projet(projet_id),
            "date_export": datetime.now().isoformat()
        }
        
        if format_sortie == "json":
            return json.dumps(export_data, indent=2, ensure_ascii=False)
        elif format_sortie == "yaml":
            import yaml
            return yaml.dump(export_data, default_flow_style=False, allow_unicode=True)
        else:
            raise ValueError(f"Format de sortie non supporté: {format_sortie}")
    
    def _ajouter_historique(
        self,
        projet_id: int,
        type_entite: str,
        id_entite: int,
        action: str,
        utilisateur: str,
        details: str
    ):
        """Ajoute une entrée dans l'historique des modifications"""
        date_actuelle = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO historiques_modifications 
                (projet_id, type_entite, id_entite, action, utilisateur, date_modification, details)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (projet_id, type_entite, id_entite, action, utilisateur, date_actuelle, details))
            conn.commit()
    
    def obtenir_historique_projet(self, projet_id: int) -> List[Dict[str, Any]]:
        """
        Obtient l'historique complet d'un projet
        
        Args:
            projet_id: ID du projet
            
        Returns:
            Historique des modifications
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM historiques_modifications 
                WHERE projet_id = ?
                ORDER BY date_modification DESC
            """, (projet_id,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def nettoyer_projet(self, projet_id: int) -> Dict[str, int]:
        """
        Nettoie les données d'un projet (supprime les données obsolètes)
        
        Args:
            projet_id: ID du projet
            
        Returns:
            Statistiques de nettoyage
        """
        stats = {"supprimes": 0}
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Supprimer les relevés sans données
            cursor.execute("""
                DELETE FROM releves_terrain 
                WHERE projet_id = ? AND (donnees = '{}' OR donnees IS NULL)
            """, (projet_id,))
            stats["supprimes"] += cursor.rowcount
            
            # Supprimer les calculs sans résultats
            cursor.execute("""
                DELETE FROM resultats_calculs 
                WHERE projet_id = ? AND (resultats = '{}' OR resultats IS NULL)
            """, (projet_id,))
            stats["supprimes"] += cursor.rowcount
            
            conn.commit()
        
        return stats
