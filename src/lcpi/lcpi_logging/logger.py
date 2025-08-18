"""
Module de logging principal LCPI - Jalon 2.
Gère la création et la sauvegarde des logs de calcul avec intégrité.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from .integrity import integrity_manager

class LCPILogger:
    """Logger principal pour LCPI avec intégrité des logs."""
    
    def __init__(self, log_dir: Union[str, Path] = "logs"):
        """
        Initialise le logger LCPI.
        
        Args:
            log_dir: Répertoire de stockage des logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Créer le répertoire .lcpi s'il n'existe pas
        lcpi_dir = self.log_dir.parent / ".lcpi"
        lcpi_dir.mkdir(exist_ok=True)
    
    def log_calculation_result(
        self,
        plugin: str,
        command: str,
        parameters: Dict[str, Any],
        results: Dict[str, Any],
        execution_time: float,
        status: str = "success",
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Enregistre le résultat d'un calcul avec intégrité.
        
        Args:
            plugin: Nom du plugin utilisé
            command: Commande exécutée
            parameters: Paramètres d'entrée
            results: Résultats du calcul
            execution_time: Temps d'exécution en secondes
            status: Statut de l'exécution
            error_message: Message d'erreur si applicable
            metadata: Métadonnées supplémentaires
            
        Returns:
            ID unique du log créé
        """
        # Générer un ID unique pour le log
        log_id = str(uuid.uuid4())
        
        # Créer le contenu du log
        log_data = {
            "log_id": log_id,
            "timestamp": datetime.now().isoformat(),
            "plugin": plugin,
            "command": command,
            "parameters": parameters,
            "results": results,
            "execution_time": execution_time,
            "status": status,
            "metadata": metadata or {}
        }
        
        # Ajouter le message d'erreur si applicable
        if error_message:
            log_data["error_message"] = error_message
        
        # Signer le log avec intégrité
        signed_log = integrity_manager.sign_log(log_data)
        
        # Générer le nom de fichier
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{plugin}_{command}_{timestamp_str}_{log_id[:8]}.json"
        log_file_path = self.log_dir / filename
        
        # Sauvegarder le log
        with open(log_file_path, 'w', encoding='utf-8') as f:
            json.dump(signed_log, f, indent=2, ensure_ascii=False)
        
        return log_id
    
    def log_plugin_activation(
        self,
        plugin_name: str,
        activation_status: str,
        version: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> str:
        """
        Enregistre l'activation/désactivation d'un plugin.
        
        Args:
            plugin_name: Nom du plugin
            activation_status: Statut d'activation
            version: Version du plugin
            error_message: Message d'erreur si applicable
            
        Returns:
            ID unique du log créé
        """
        log_data = {
            "log_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "event_type": "plugin_activation",
            "plugin_name": plugin_name,
            "activation_status": activation_status,
            "version": version,
            "metadata": {
                "event_category": "plugin_management"
            }
        }
        
        if error_message:
            log_data["error_message"] = error_message
        
        # Signer le log
        signed_log = integrity_manager.sign_log(log_data)
        
        # Sauvegarder
        filename = f"plugin_{plugin_name}_{activation_status}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_file_path = self.log_dir / filename
        
        with open(log_file_path, 'w', encoding='utf-8') as f:
            json.dump(signed_log, f, indent=2, ensure_ascii=False)
        
        return log_data["log_id"]
    
    def log_project_operation(
        self,
        operation: str,
        project_path: str,
        details: Dict[str, Any],
        status: str = "success"
    ) -> str:
        """
        Enregistre une opération sur un projet.
        
        Args:
            operation: Type d'opération (create, lock, unlock, export)
            project_path: Chemin du projet
            details: Détails de l'opération
            status: Statut de l'opération
            
        Returns:
            ID unique du log créé
        """
        log_data = {
            "log_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "event_type": "project_operation",
            "operation": operation,
            "project_path": project_path,
            "details": details,
            "status": status,
            "metadata": {
                "event_category": "project_management"
            }
        }
        
        # Signer le log
        signed_log = integrity_manager.sign_log(log_data)
        
        # Sauvegarder
        filename = f"project_{operation}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_file_path = self.log_dir / filename
        
        with open(log_file_path, 'w', encoding='utf-8') as f:
            json.dump(signed_log, f, indent=2, ensure_ascii=False)
        
        return log_data["log_id"]
    
    def get_log_by_id(self, log_id: str) -> Optional[Dict[str, Any]]:
        """
        Récupère un log par son ID.
        
        Args:
            log_id: ID du log à récupérer
            
        Returns:
            Contenu du log ou None si non trouvé
        """
        for log_file in self.log_dir.glob("*.json"):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = json.load(f)
                
                if log_content.get("log_id") == log_id:
                    return log_content
                    
            except Exception:
                continue
        
        return None
    
    def list_logs(
        self,
        plugin: Optional[str] = None,
        command: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Liste les logs selon des critères de filtrage.
        
        Args:
            plugin: Filtrer par plugin
            command: Filtrer par commande
            status: Filtrer par statut
            limit: Limite du nombre de résultats
            
        Returns:
            Liste des logs correspondants
        """
        logs = []
        
        for log_file in sorted(self.log_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = json.load(f)
                
                # Appliquer les filtres
                if plugin and log_content.get("plugin") != plugin:
                    continue
                if command and log_content.get("command") != command:
                    continue
                if status and log_content.get("status") != status:
                    continue
                
                # Ajouter le chemin du fichier
                log_content["_file_path"] = str(log_file)
                logs.append(log_content)
                
                # Limiter le nombre de résultats
                if limit and len(logs) >= limit:
                    break
                    
            except Exception:
                continue
        
        return logs
    
    def verify_log_integrity(self, log_id: str) -> Dict[str, Any]:
        """
        Vérifie l'intégrité d'un log spécifique.
        
        Args:
            log_id: ID du log à vérifier
            
        Returns:
            Résultat de la vérification
        """
        log_content = self.get_log_by_id(log_id)
        if not log_content:
            return {
                "valid": False,
                "error": f"Log avec ID {log_id} non trouvé"
            }
        
        # Trouver le fichier correspondant
        for log_file in self.log_dir.glob("*.json"):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    if json.load(f).get("log_id") == log_id:
                        return integrity_manager.verify_log_integrity(log_file)
            except Exception:
                continue
        
        return {
            "valid": False,
            "error": "Impossible de localiser le fichier du log"
        }
    
    def verify_all_logs(self) -> Dict[str, Any]:
        """
        Vérifie l'intégrité de tous les logs.
        
        Returns:
            Résumé de la vérification
        """
        return integrity_manager.verify_all_logs(self.log_dir)
    
    def cleanup_old_logs(self, days_to_keep: int = 30) -> int:
        """
        Nettoie les anciens logs.
        
        Args:
            days_to_keep: Nombre de jours à conserver
            
        Returns:
            Nombre de logs supprimés
        """
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted_count = 0
        
        for log_file in self.log_dir.glob("*.json"):
            try:
                # Vérifier la date de modification
                if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
            except Exception:
                continue
        
        return deleted_count


# Instance globale pour utilisation dans d'autres modules
lcpi_logger = LCPILogger()


if __name__ == "__main__":
    # Test du module de logging
    import tempfile
    import shutil
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Créer un logger de test
        test_logger = LCPILogger(temp_path / "logs")
        
        # Tester la création de logs
        log_id1 = test_logger.log_calculation_result(
            plugin="aep",
            command="population",
            parameters={"debut": 2020, "fin": 2030},
            results={"population_2020": 15000},
            execution_time=1.23
        )
        
        log_id2 = test_logger.log_plugin_activation(
            plugin_name="aep",
            activation_status="activated",
            version="2.1.0"
        )
        
        # Lister les logs
        logs = test_logger.list_logs()
        print(f"Logs créés: {len(logs)}")
        
        # Vérifier l'intégrité
        integrity_result = test_logger.verify_all_logs()
        print(f"Vérification d'intégrité: {integrity_result}")
        
        # Récupérer un log spécifique
        log_content = test_logger.get_log_by_id(log_id1)
        if log_content:
            print(f"Log récupéré: {log_content['plugin']} - {log_content['command']}")
