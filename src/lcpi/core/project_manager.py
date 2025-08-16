"""
Gestionnaire de projets LCPI unifié avec support des fichiers lcpi.yml et base de données centralisée.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import hashlib
import logging

logger = logging.getLogger(__name__)

# Import de la base de données unifiée
try:
    from .unified_database import UnifiedDatabase
    UNIFIED_DB_AVAILABLE = True
except ImportError as e:
    UNIFIED_DB_AVAILABLE = False
    logger.warning(f"Base de données unifiée non disponible: {e}")

class ProjectManager:
    """Gestionnaire de projets LCPI avec support des métadonnées."""
    
    def __init__(self, project_dir: Path):
        """
        Initialise le gestionnaire de projet.
        
        Args:
            project_dir: Chemin vers le dossier du projet
        """
        self.project_dir = Path(project_dir)
        self.config_file = self.project_dir / "lcpi.yml"
        self.config = self._load_config()
        
        # Initialiser la base de données unifiée si disponible
        self.database = None
        if UNIFIED_DB_AVAILABLE:
            try:
                db_path = self.project_dir / "database.db"
                self.database = UnifiedDatabase(db_path)
                logger.info(f"Base de données unifiée initialisée pour le projet: {db_path}")
            except Exception as e:
                logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
        else:
            logger.warning("Base de données unifiée non disponible - fonctionnalités limitées")
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration du projet depuis lcpi.yml."""
        if not self.config_file.exists():
            return self._create_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logger.info(f"Configuration chargée depuis {self.config_file}")
                return config or self._create_default_config()
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la configuration: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Crée une configuration par défaut."""
        default_config = {
            "projet_metadata": {
                "nom_projet": self.project_dir.name,
                "version": "1.0.0",
                "date_creation": datetime.now().isoformat(),
                "auteur": "LCPI-CLI",
                "description": "Projet LCPI généré automatiquement",
                "tags": [],
                "client": "Non spécifié",
                "indice_revision": "A"
            },
            "plugins_actifs": ["aep", "cm", "bois", "beton", "hydro"],
            "configurations": {
                "epanet": {
                    "dll_path": "vendor/dlls/epanet2_64.dll",
                    "version": "2.3.1"
                },
                "reporting": {
                    "template_default": "default",
                    "formats_supportes": ["html", "pdf", "docx"]
                }
            },
            "dossiers": {
                "logs": "logs/",
                "outputs": "outputs/",
                "reports": "reports/",
                "data": "data/",
                "temp": "temp/"
            }
        }
        
        # Sauvegarder la configuration par défaut
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Sauvegarde la configuration dans lcpi.yml."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
            logger.info(f"Configuration sauvegardée dans {self.config_file}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la configuration: {e}")
    
    def get_project_info(self) -> Dict[str, Any]:
        """Retourne les informations du projet."""
        return self.config.get("projet_metadata", {})
    
    def update_project_info(self, updates: Dict[str, Any]) -> None:
        """Met à jour les informations du projet."""
        if "projet_metadata" not in self.config:
            self.config["projet_metadata"] = {}
        
        self.config["projet_metadata"].update(updates)
        self._save_config(self.config)
        logger.info("Informations du projet mises à jour")
    
    def get_plugin_config(self, plugin_name: str) -> Dict[str, Any]:
        """Retourne la configuration d'un plugin."""
        return self.config.get("configurations", {}).get(plugin_name, {})
    
    def set_plugin_config(self, plugin_name: str, config: Dict[str, Any]) -> None:
        """Définit la configuration d'un plugin."""
        if "configurations" not in self.config:
            self.config["configurations"] = {}
        
        self.config["configurations"][plugin_name] = config
        self._save_config(self.config)
        logger.info(f"Configuration du plugin {plugin_name} mise à jour")
    
    def get_folder_path(self, folder_name: str) -> Path:
        """Retourne le chemin d'un dossier du projet."""
        folder_path = self.project_dir / self.config.get("dossiers", {}).get(folder_name, folder_name)
        folder_path.mkdir(parents=True, exist_ok=True)
        return folder_path
    
    def create_project_structure(self) -> None:
        """Crée la structure de dossiers du projet."""
        folders = self.config.get("dossiers", {})
        for folder_name, folder_path in folders.items():
            full_path = self.project_dir / folder_path
            full_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Dossier créé: {full_path}")
    
    def get_project_hash(self) -> str:
        """Calcule le hash du projet basé sur la configuration et les fichiers."""
        content = json.dumps(self.config, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:8]
    
    def export_config(self, format: str = "json") -> str:
        """Exporte la configuration dans différents formats."""
        if format.lower() == "json":
            return json.dumps(self.config, indent=2, ensure_ascii=False)
        elif format.lower() == "yaml":
            return yaml.dump(self.config, default_flow_style=False, allow_unicode=True)
        else:
            raise ValueError(f"Format non supporté: {format}")
    
    # === MÉTHODES DE BASE DE DONNÉES ===
    
    def create_project_in_database(self, nom: str = None, description: str = None, 
                                 metadata: Dict[str, Any] = None) -> Optional[int]:
        """
        Crée le projet dans la base de données unifiée.
        
        Args:
            nom: Nom du projet (utilise le nom du dossier si None)
            description: Description du projet
            metadata: Métadonnées supplémentaires
        
        Returns:
            ID du projet créé ou None si échec
        """
        if not self.database:
            logger.warning("Base de données non disponible")
            return None
        
        try:
            nom_projet = nom or self.project_dir.name
            desc_projet = description or self.config.get("projet_metadata", {}).get("description", "")
            
            # Déterminer le module principal
            module_principal = "general"
            if "aep" in self.config.get("plugins_actifs", []):
                module_principal = "aep"
            elif "cm" in self.config.get("plugins_actifs", []):
                module_principal = "cm"
            elif "bois" in self.config.get("plugins_actifs", []):
                module_principal = "bois"
            elif "beton" in self.config.get("plugins_actifs", []):
                module_principal = "beton"
            
            projet_id = self.database.ajouter_projet(
                nom_projet, desc_projet, metadata, module_principal
            )
            
            logger.info(f"Projet créé dans la base de données: {nom_projet} (ID: {projet_id})")
            return projet_id
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du projet dans la base de données: {e}")
            return None
    
    def add_calculation_to_database(self, commande: str, resultats: Dict[str, Any],
                                  hash_donnees: str = None, dependances: List[int] = None,
                                  duree_execution: float = None, version_algorithme: str = None,
                                  metadata: Dict[str, Any] = None, module_source: str = None) -> Optional[int]:
        """
        Ajoute un calcul à la base de données.
        
        Args:
            commande: Commande exécutée
            resultats: Résultats du calcul
            hash_donnees: Hash des données (calculé automatiquement si None)
            dependances: Liste des IDs des calculs dont dépend ce calcul
            duree_execution: Durée d'exécution en secondes
            version_algorithme: Version de l'algorithme utilisé
            metadata: Métadonnées supplémentaires
            module_source: Module source (déterminé automatiquement si None)
        
        Returns:
            ID du calcul créé ou None si échec
        """
        if not self.database:
            logger.warning("Base de données non disponible")
            return None
        
        try:
            # Déterminer le module source
            if module_source is None:
                if "aep" in self.config.get("plugins_actifs", []):
                    module_source = "aep"
                elif "cm" in self.config.get("plugins_actifs", []):
                    module_source = "cm"
                elif "bois" in self.config.get("plugins_actifs", []):
                    module_source = "bois"
                elif "beton" in self.config.get("plugins_actifs", []):
                    module_source = "beton"
                else:
                    module_source = "general"
            
            # Récupérer l'ID du projet depuis la base de données
            projets = self.database.get_projets_par_module(module_source)
            projet_id = None
            for projet in projets:
                if projet["nom"] == self.project_dir.name:
                    projet_id = projet["id"]
                    break
            
            if projet_id is None:
                # Créer le projet s'il n'existe pas
                projet_id = self.create_project_in_database(metadata={"module_source": module_source})
                if projet_id is None:
                    return None
            
            calcul_id = self.database.ajouter_calcul(
                projet_id, commande, resultats, hash_donnees, dependances,
                duree_execution, version_algorithme, metadata, module_source
            )
            
            logger.info(f"Calcul ajouté à la base de données: {commande} (ID: {calcul_id})")
            return calcul_id
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du calcul à la base de données: {e}")
            return None
    
    def add_aep_data_to_database(self, data_type: str, **kwargs) -> Optional[int]:
        """
        Ajoute des données AEP spécifiques à la base de données.
        
        Args:
            data_type: Type de données ('releve', 'resultat', 'reseau', 'noeud', 'troncon')
            **kwargs: Paramètres spécifiques au type de données
        
        Returns:
            ID de l'élément créé ou None si échec
        """
        if not self.database:
            logger.warning("Base de données non disponible")
            return None
        
        try:
            # Récupérer l'ID du projet
            projets = self.database.get_projets_par_module("aep")
            projet_id = None
            for projet in projets:
                if projet["nom"] == self.project_dir.name:
                    projet_id = projet["id"]
                    break
            
            if projet_id is None:
                # Créer le projet s'il n'existe pas
                projet_id = self.create_project_in_database(module_principal="aep")
                if projet_id is None:
                    return None
            
            if data_type == "releve":
                return self.database.ajouter_releve_terrain_aep(projet_id, **kwargs)
            elif data_type == "resultat":
                return self.database.ajouter_resultat_calcul_aep(projet_id, **kwargs)
            elif data_type == "reseau":
                return self.database.ajouter_reseau_aep(projet_id, **kwargs)
            elif data_type == "noeud":
                # Pour les nœuds, on a besoin du reseau_id, pas du projet_id
                reseau_id = kwargs.pop('reseau_id', None)
                if reseau_id is None:
                    logger.error("reseau_id requis pour ajouter un nœud")
                    return None
                return self.database.ajouter_noeud_aep(reseau_id, **kwargs)
            elif data_type == "troncon":
                # Pour les tronçons, on a besoin du reseau_id, pas du projet_id
                reseau_id = kwargs.pop('reseau_id', None)
                if reseau_id is None:
                    logger.error("reseau_id requis pour ajouter un tronçon")
                    return None
                return self.database.ajouter_troncon_aep(reseau_id, **kwargs)
            else:
                logger.error(f"Type de données AEP non supporté: {data_type}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout des données AEP: {e}")
            return None
    
    def get_project_history(self, limite: int = 100) -> List[Dict[str, Any]]:
        """
        Récupère l'historique du projet depuis la base de données.
        
        Args:
            limite: Nombre maximum d'éléments à récupérer
        
        Returns:
            Liste des éléments d'historique
        """
        if not self.database:
            logger.warning("Base de données non disponible")
            return []
        
        try:
            # Récupérer l'ID du projet
            projets = self.database.get_projets_par_module("aep")
            projet_id = None
            for projet in projets:
                if projet["nom"] == self.project_dir.name:
                    projet_id = projet["id"]
                    break
            
            if projet_id is None:
                return []
            
            return self.database.get_historique_projet(projet_id, limite)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'historique: {e}")
            return []
    
    def add_log_to_database(self, niveau: str, message: str, 
                           contexte: Dict[str, Any] = None, module_source: str = None):
        """
        Ajoute un log à la base de données.
        
        Args:
            niveau: Niveau du log (INFO, WARNING, ERROR, DEBUG)
            message: Message du log
            contexte: Contexte supplémentaire
            module_source: Module source (déterminé automatiquement si None)
        """
        if not self.database:
            logger.warning("Base de données non disponible")
            return
        
        try:
            # Déterminer le module source
            if module_source is None:
                if "aep" in self.config.get("plugins_actifs", []):
                    module_source = "aep"
                elif "cm" in self.config.get("plugins_actifs", []):
                    module_source = "cm"
                elif "bois" in self.config.get("plugins_actifs", []):
                    module_source = "bois"
                elif "beton" in self.config.get("plugins_actifs", []):
                    module_source = "beton"
                else:
                    module_source = "general"
            
            # Récupérer l'ID du projet
            projets = self.database.get_projets_par_module(module_source)
            projet_id = None
            for projet in projets:
                if projet["nom"] == self.project_dir.name:
                    projet_id = projet["id"]
                    break
            
            if projet_id is None:
                # Créer le projet s'il n'existe pas
                projet_id = self.create_project_in_database(metadata={"module_source": module_source})
                if projet_id is None:
                    return
            
            self.database.ajouter_log(projet_id, niveau, message, contexte, module_source)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du log: {e}")

def create_project(project_dir: Path, project_name: str = None, 
                  author: str = None, description: str = None) -> ProjectManager:
    """
    Crée un nouveau projet LCPI.
    
    Args:
        project_dir: Chemin vers le dossier du projet
        project_name: Nom du projet
        author: Auteur du projet
        description: Description du projet
    
    Returns:
        Instance du gestionnaire de projet
    """
    project_dir = Path(project_dir)
    project_dir.mkdir(parents=True, exist_ok=True)
    
    manager = ProjectManager(project_dir)
    
    # Mettre à jour les informations du projet
    updates = {}
    if project_name:
        updates["nom_projet"] = project_name
    if author:
        updates["auteur"] = author
    if description:
        updates["description"] = description
    
    if updates:
        manager.update_project_info(updates)
    
    # Créer la structure de dossiers
    manager.create_project_structure()
    
    logger.info(f"Projet créé: {project_dir}")
    return manager
