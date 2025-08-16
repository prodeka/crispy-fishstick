"""
Wrapper AEP qui utilise le ProjectManager centralisé pour la gestion des projets.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

# Import du ProjectManager centralisé
try:
    from ...core.project_manager import ProjectManager
    PROJECT_MANAGER_AVAILABLE = True
except ImportError as e:
    PROJECT_MANAGER_AVAILABLE = False
    logging.warning(f"ProjectManager non disponible: {e}")

logger = logging.getLogger(__name__)

class AEPProjectWrapper:
    """
    Wrapper AEP qui utilise le ProjectManager centralisé.
    
    Ce wrapper fournit une interface unifiée pour gérer les projets AEP
    en utilisant le système de gestion centralisé.
    """
    
    def __init__(self, project_dir: Union[str, Path]):
        """
        Initialise le wrapper AEP.
        
        Args:
            project_dir: Chemin vers le dossier du projet
        """
        self.project_dir = Path(project_dir)
        
        if PROJECT_MANAGER_AVAILABLE:
            try:
                self.project_manager = ProjectManager(self.project_dir)
                logger.info(f"ProjectManager initialisé pour le projet AEP: {self.project_dir}")
            except Exception as e:
                logger.error(f"Erreur lors de l'initialisation du ProjectManager: {e}")
                self.project_manager = None
        else:
            logger.warning("ProjectManager non disponible - fonctionnalités limitées")
            self.project_manager = None
    
    # === GESTION DES PROJETS ===
    
    def create_aep_project(self, nom: str = None, description: str = None,
                          metadata: Dict[str, Any] = None) -> Optional[int]:
        """
        Crée un projet AEP dans la base de données centralisée.
        
        Args:
            nom: Nom du projet
            description: Description du projet
            metadata: Métadonnées supplémentaires
        
        Returns:
            ID du projet créé ou None si échec
        """
        if not self.project_manager:
            logger.warning("ProjectManager non disponible")
            return None
        
        try:
            # Créer le projet dans la base de données
            projet_id = self.project_manager.create_project_in_database(
                nom=nom,
                description=description,
                metadata=metadata
            )
            
            if projet_id:
                logger.info(f"Projet AEP créé avec succès: {projet_id}")
                
                # Ajouter un log de création
                self.project_manager.add_log_to_database(
                    "INFO",
                    f"Projet AEP créé: {nom or self.project_dir.name}",
                    {"action": "create_project", "module": "aep"}
                )
            
            return projet_id
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du projet AEP: {e}")
            return None
    
    def get_project_info(self) -> Dict[str, Any]:
        """Récupère les informations du projet AEP."""
        if not self.project_manager:
            return {}
        
        return self.project_manager.get_project_info()
    
    def update_project_info(self, updates: Dict[str, Any]) -> bool:
        """Met à jour les informations du projet AEP."""
        if not self.project_manager:
            return False
        
        try:
            self.project_manager.update_project_info(updates)
            logger.info("Informations du projet AEP mises à jour")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour: {e}")
            return False
    
    # === GESTION DES CALCULS ===
    
    def add_calculation(self, commande: str, resultats: Dict[str, Any],
                       hash_donnees: str = None, dependances: List[int] = None,
                       duree_execution: float = None, version_algorithme: str = None,
                       metadata: Dict[str, Any] = None) -> Optional[int]:
        """
        Ajoute un calcul AEP à la base de données.
        
        Args:
            commande: Commande exécutée
            resultats: Résultats du calcul
            hash_donnees: Hash des données
            dependances: Liste des IDs des calculs dont dépend ce calcul
            duree_execution: Durée d'exécution en secondes
            version_algorithme: Version de l'algorithme utilisé
            metadata: Métadonnées supplémentaires
        
        Returns:
            ID du calcul créé ou None si échec
        """
        if not self.project_manager:
            logger.warning("ProjectManager non disponible")
            return None
        
        try:
            calcul_id = self.project_manager.add_calculation_to_database(
                commande=commande,
                resultats=resultats,
                hash_donnees=hash_donnees,
                dependances=dependances,
                duree_execution=duree_execution,
                version_algorithme=version_algorithme,
                metadata=metadata,
                module_source="aep"
            )
            
            if calcul_id:
                logger.info(f"Calcul AEP ajouté avec succès: {calcul_id}")
                
                # Ajouter un log de calcul
                self.project_manager.add_log_to_database(
                    "INFO",
                    f"Calcul AEP exécuté: {commande}",
                    {"action": "add_calculation", "calcul_id": calcul_id, "module": "aep"}
                )
            
            return calcul_id
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du calcul AEP: {e}")
            return None
    
    # === GESTION DES DONNÉES AEP SPÉCIFIQUES ===
    
    def add_field_survey(self, type_releve: str, nom_point: str,
                         donnees: Dict[str, Any], coordonnees_gps: str = None,
                         altitude: float = None, operateur: str = None,
                         notes: str = None) -> Optional[int]:
        """
        Ajoute un relevé terrain AEP.
        
        Args:
            type_releve: Type de relevé (ex: "pression", "débit", "altitude")
            nom_point: Nom du point de relevé
            donnees: Données du relevé
            coordonnees_gps: Coordonnées GPS
            altitude: Altitude du point
            operateur: Nom de l'opérateur
            notes: Notes supplémentaires
        
        Returns:
            ID du relevé créé ou None si échec
        """
        if not self.project_manager:
            logger.warning("ProjectManager non disponible")
            return None
        
        try:
            releve_id = self.project_manager.add_aep_data_to_database(
                data_type="releve",
                type_releve=type_releve,
                nom_point=nom_point,
                donnees=donnees,
                coordonnees_gps=coordonnees_gps,
                altitude=altitude,
                operateur=operateur,
                notes=notes
            )
            
            if releve_id:
                logger.info(f"Relevé terrain AEP ajouté avec succès: {releve_id}")
                
                # Ajouter un log
                self.project_manager.add_log_to_database(
                    "INFO",
                    f"Relevé terrain AEP ajouté: {type_releve} - {nom_point}",
                    {"action": "add_field_survey", "releve_id": releve_id, "module": "aep"},
                    "aep"
                )
            
            return releve_id
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du relevé terrain: {e}")
            return None
    
    def add_calculation_result(self, type_calcul: str, nom_calcul: str,
                              parametres_entree: Dict[str, Any], resultats: Dict[str, Any],
                              duree_calcul: float = None, version_algorithme: str = None) -> Optional[int]:
        """
        Ajoute un résultat de calcul AEP.
        
        Args:
            type_calcul: Type de calcul (ex: "hardy_cross", "epanet", "optimisation")
            nom_calcul: Nom du calcul
            parametres_entree: Paramètres d'entrée
            resultats: Résultats du calcul
            duree_calcul: Durée d'exécution
            version_algorithme: Version de l'algorithme
        
        Returns:
            ID du résultat créé ou None si échec
        """
        if not self.project_manager:
            logger.warning("ProjectManager non disponible")
            return None
        
        try:
            resultat_id = self.project_manager.add_aep_data_to_database(
                data_type="resultat",
                type_calcul=type_calcul,
                nom_calcul=nom_calcul,
                parametres_entree=parametres_entree,
                resultats=resultats,
                duree_calcul=duree_calcul,
                version_algorithme=version_algorithme
            )
            
            if resultat_id:
                logger.info(f"Résultat de calcul AEP ajouté avec succès: {resultat_id}")
                
                # Ajouter un log
                self.project_manager.add_log_to_database(
                    "INFO",
                    f"Résultat de calcul AEP ajouté: {type_calcul} - {nom_calcul}",
                    {"action": "add_calculation_result", "resultat_id": resultat_id, "module": "aep"},
                    "aep"
                )
            
            return resultat_id
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du résultat de calcul: {e}")
            return None
    
    def add_network(self, nom_reseau: str, type_reseau: str,
                   caracteristiques: Dict[str, Any], metadata: Dict[str, Any] = None) -> Optional[int]:
        """
        Ajoute un réseau AEP.
        
        Args:
            nom_reseau: Nom du réseau
            type_reseau: Type de réseau (ex: "distribution", "collecte")
            caracteristiques: Caractéristiques du réseau
            metadata: Métadonnées supplémentaires
        
        Returns:
            ID du réseau créé ou None si échec
        """
        if not self.project_manager:
            logger.warning("ProjectManager non disponible")
            return None
        
        try:
            reseau_id = self.project_manager.add_aep_data_to_database(
                data_type="reseau",
                nom_reseau=nom_reseau,
                type_reseau=type_reseau,
                caracteristiques=caracteristiques,
                metadata=metadata
            )
            
            if reseau_id:
                logger.info(f"Réseau AEP ajouté avec succès: {reseau_id}")
                
                # Ajouter un log
                self.project_manager.add_log_to_database(
                    "INFO",
                    f"Réseau AEP ajouté: {nom_reseau} ({type_reseau})",
                    {"action": "add_network", "reseau_id": reseau_id, "module": "aep"},
                    "aep"
                )
            
            return reseau_id
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du réseau: {e}")
            return None
    
    def add_node(self, reseau_id: int, nom_noeud: str, type_noeud: str,
                 coordonnees: str = None, elevation: float = None, demande: float = None,
                 pression_min: float = None, pression_max: float = None,
                 metadata: Dict[str, Any] = None) -> Optional[int]:
        """
        Ajoute un nœud AEP.
        
        Args:
            reseau_id: ID du réseau
            nom_noeud: Nom du nœud
            type_noeud: Type de nœud (ex: "reservoir", "chateau", "pompe", "consommation")
            coordonnees: Coordonnées du nœud
            elevation: Élévation du nœud
            demande: Demande en eau
            pression_min: Pression minimale
            pression_max: Pression maximale
            metadata: Métadonnées supplémentaires
        
        Returns:
            ID du nœud créé ou None si échec
        """
        if not self.project_manager:
            logger.warning("ProjectManager non disponible")
            return None
        
        try:
            noeud_id = self.project_manager.add_aep_data_to_database(
                data_type="noeud",
                reseau_id=reseau_id,
                nom_noeud=nom_noeud,
                type_noeud=type_noeud,
                coordonnees=coordonnees,
                elevation=elevation,
                demande=demande,
                pression_min=pression_min,
                pression_max=pression_max,
                metadata=metadata
            )
            
            if noeud_id:
                logger.info(f"Nœud AEP ajouté avec succès: {noeud_id}")
                
                # Ajouter un log
                self.project_manager.add_log_to_database(
                    "INFO",
                    f"Nœud AEP ajouté: {nom_noeud} ({type_noeud})",
                    {"action": "add_node", "noeud_id": noeud_id, "module": "aep"},
                    "aep"
                )
            
            return noeud_id
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du nœud: {e}")
            return None
    
    def add_pipe(self, reseau_id: int, nom_troncon: str, noeud_debut: str, noeud_fin: str,
                 longueur: float, diametre: float = None, rugosite: float = None,
                 type_materiau: str = None, metadata: Dict[str, Any] = None) -> Optional[int]:
        """
        Ajoute un tronçon AEP.
        
        Args:
            reseau_id: ID du réseau
            nom_troncon: Nom du tronçon
            noeud_debut: Nom du nœud de début
            noeud_fin: Nom du nœud de fin
            longueur: Longueur du tronçon
            diametre: Diamètre du tronçon
            rugosite: Rugosité du tronçon
            type_materiau: Type de matériau
            metadata: Métadonnées supplémentaires
        
        Returns:
            ID du tronçon créé ou None si échec
        """
        if not self.project_manager:
            logger.warning("ProjectManager non disponible")
            return None
        
        try:
            troncon_id = self.project_manager.add_aep_data_to_database(
                data_type="troncon",
                reseau_id=reseau_id,
                nom_troncon=nom_troncon,
                noeud_debut=noeud_debut,
                noeud_fin=noeud_fin,
                longueur=longueur,
                diametre=diametre,
                rugosite=rugosite,
                type_materiau=type_materiau,
                metadata=metadata
            )
            
            if troncon_id:
                logger.info(f"Tronçon AEP ajouté avec succès: {troncon_id}")
                
                # Ajouter un log
                self.project_manager.add_log_to_database(
                    "INFO",
                    f"Tronçon AEP ajouté: {nom_troncon} ({noeud_debut} -> {noeud_fin})",
                    {"action": "add_pipe", "troncon_id": troncon_id, "module": "aep"},
                    "aep"
                )
            
            return troncon_id
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du tronçon: {e}")
            return None
    
    # === RÉCUPÉRATION DES DONNÉES ===
    
    def get_project_history(self, limite: int = 100) -> List[Dict[str, Any]]:
        """
        Récupère l'historique du projet AEP.
        
        Args:
            limite: Nombre maximum d'éléments à récupérer
        
        Returns:
            Liste des éléments d'historique
        """
        if not self.project_manager:
            return []
        
        return self.project_manager.get_project_history(limite)
    
    def get_network_complete(self, reseau_id: int) -> Optional[Dict[str, Any]]:
        """
        Récupère un réseau AEP complet avec ses nœuds et tronçons.
        
        Args:
            reseau_id: ID du réseau
        
        Returns:
            Dictionnaire du réseau complet ou None si non trouvé
        """
        if not self.project_manager or not self.project_manager.database:
            return None
        
        try:
            return self.project_manager.database.get_reseau_aep_complet(reseau_id)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du réseau: {e}")
            return None
    
    # === LOGGING ===
    
    def add_log(self, niveau: str, message: str, contexte: Dict[str, Any] = None):
        """
        Ajoute un log AEP à la base de données.
        
        Args:
            niveau: Niveau du log (INFO, WARNING, ERROR, DEBUG)
            message: Message du log
            contexte: Contexte supplémentaire
        """
        if not self.project_manager:
            return
        
        self.project_manager.add_log_to_database(niveau, message, contexte)
    
    # === UTILITAIRES ===
    
    def is_available(self) -> bool:
        """Vérifie si le wrapper AEP est disponible."""
        return PROJECT_MANAGER_AVAILABLE and self.project_manager is not None
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du wrapper AEP."""
        return {
            "available": self.is_available(),
            "project_manager_available": PROJECT_MANAGER_AVAILABLE,
            "project_dir": str(self.project_dir),
            "project_info": self.get_project_info() if self.is_available() else {}
        }
