"""
Module de spinner global pour LCPI.
Fournit des décorateurs pour ajouter automatiquement un spinner à toutes les commandes.
"""

import functools
import time
from typing import Callable, Any, Optional
from rich.console import Console
from rich.status import Status

console = Console()

def with_spinner(
    message: str = "Exécution en cours...",
    spinner_type: str = "dots4"
):
    """
    Décorateur pour ajouter un spinner à une commande LCPI.
    
    Args:
        message: Message à afficher pendant l'exécution
        spinner_type: Type de spinner (dots4, line, etc.)
        transient: Si True, le spinner disparaît après exécution
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Vérifier si on est en mode verbose (pas de spinner)
            verbose = kwargs.get('verbose', False)
            
            if verbose:
                # Mode verbose : afficher le message sans spinner
                console.print(f"[bold blue]🔄 {message}[/bold blue]")
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    console.print(f"[green]✅ Terminé en {end_time - start_time:.2f}s[/green]")
                    return result
                except Exception as e:
                    end_time = time.time()
                    console.print(f"[red]❌ Erreur après {end_time - start_time:.2f}s: {e}[/red]")
                    raise
            else:
                # Mode normal : afficher le spinner
                with console.status(
                    f"[bold cyan]{message}[/bold cyan]",
                    spinner=spinner_type
                ) as status:
                    start_time = time.time()
                    try:
                        result = func(*args, **kwargs)
                        end_time = time.time()
                        
                        return result
                    except Exception as e:
                        end_time = time.time()
                        raise
        
        return wrapper
    return decorator


def with_plugin_spinner(plugin_name: str):
    """
    Décorateur spécialisé pour les commandes de plugins.
    
    Args:
        plugin_name: Nom du plugin (aep, cm, bois, etc.)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            command_name = func.__name__
            message = f"Exécution {plugin_name} {command_name}..."
            
            verbose = kwargs.get('verbose', False)
            
            if verbose:
                console.print(f"[bold blue]🔄 {message}[/bold blue]")
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    console.print(f"[green]✅ {plugin_name} {command_name} terminé en {end_time - start_time:.2f}s[/green]")
                    return result
                except Exception as e:
                    end_time = time.time()
                    console.print(f"[red]❌ {plugin_name} {command_name} - Erreur après {end_time - start_time:.2f}s: {e}[/red]")
                    raise
            else:
                with console.status(
                    f"[bold cyan]{message}[/bold cyan]",
                    spinner="dots4"
                ) as status:
                    start_time = time.time()
                    try:
                        result = func(*args, **kwargs)
                        end_time = time.time()
                        return result
                    except Exception as e:
                        end_time = time.time()
                        raise
        
        return wrapper
    return decorator


def with_calculation_spinner(calculation_type: str):
    """
    Décorateur spécialisé pour les calculs.
    
    Args:
        calculation_type: Type de calcul (population, network, etc.)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            message = f"Calcul {calculation_type} en cours..."
            
            verbose = kwargs.get('verbose', False)
            
            if verbose:
                console.print(f"[bold blue]🔄 {message}[/bold blue]")
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    console.print(f"[green]✅ Calcul {calculation_type} terminé en {end_time - start_time:.2f}s[/green]")
                    return result
                except Exception as e:
                    end_time = time.time()
                    console.print(f"[red]❌ Calcul {calculation_type} - Erreur après {end_time - start_time:.2f}s: {e}[/red]")
                    raise
            else:
                with console.status(
                    f"[bold cyan]{message}[/bold cyan]",
                    spinner="dots4"
                ) as status:
                    start_time = time.time()
                    try:
                        result = func(*args, **kwargs)
                        end_time = time.time()
                        return result
                    except Exception as e:
                        end_time = time.time()
                        raise
        
        return wrapper
    return decorator


# Messages prédéfinis pour différents types d'opérations
SPINNER_MESSAGES = {
    # Plugins
    "plugin_activation": "Activation du plugin...",
    "plugin_deactivation": "Désactivation du plugin...",
    "plugin_installation": "Installation du plugin...",
    "plugin_uninstallation": "Désinstallation du plugin...",
    
    # Projets
    "project_creation": "Création du projet...",
    "project_lock": "Verrouillage du projet...",
    "project_unlock": "Déverrouillage du projet...",
    
    # Logs et intégrité
    "log_verification": "Vérification des logs...",
    "integrity_check": "Vérification d'intégrité...",
    "export_reproducible": "Export reproductible...",
    "plugin_version_check": "Vérification des versions...",
    
    # Calculs AEP
    "calculation_population": "Calcul de projection démographique...",
    "calculation_network": "Dimensionnement du réseau...",
    "calculation_reservoir": "Dimensionnement du réservoir...",
    "calculation_pumping": "Dimensionnement du pompage...",
    "hardy_cross": "Calcul Hardy-Cross...",
    "epanet_simulation": "Simulation EPANET...",
    
    # Général
    "optimization": "Optimisation en cours...",
    "validation": "Validation des données...",
    "export_results": "Export des résultats...",
    "import_data": "Import des données...",
    "report_generation": "Génération du rapport...",
    "configuration_load": "Chargement de la configuration...",
    "configuration_save": "Sauvegarde de la configuration...",
    "cache_clear": "Nettoyage du cache...",
    "test_execution": "Exécution des tests...",
    "file_processing": "Traitement des fichiers...",
    "database_query": "Interrogation de la base de données...",
    "backup_creation": "Création de la sauvegarde...",
    "restore_backup": "Restauration de la sauvegarde...",
    "update_check": "Vérification des mises à jour...",
    "dependency_check": "Vérification des dépendances...",
    "build_process": "Processus de compilation...",
    "deployment": "Déploiement en cours...",
    "log_analysis": "Analyse des logs...",
    "performance_test": "Test de performance...",
    "security_scan": "Scan de sécurité...",
    "data_migration": "Migration des données...",
    "system_check": "Vérification du système...",
    "license_validation": "Validation de la licence...",
    "user_authentication": "Authentification utilisateur...",
    "session_creation": "Création de session...",
    "session_cleanup": "Nettoyage de session...",
    "notification_send": "Envoi de notification...",
    "email_send": "Envoi d'email...",
    "file_upload": "Upload de fichier...",
    "file_download": "Téléchargement de fichier...",
    "data_sync": "Synchronisation des données...",
    "index_rebuild": "Reconstruction de l'index...",
    "search_execution": "Exécution de la recherche...",
    "filter_application": "Application des filtres...",
    "sort_execution": "Tri des données...",
    "aggregation_calculation": "Calcul d'agrégation...",
    "statistics_computation": "Calcul des statistiques...",
    "chart_generation": "Génération de graphique...",
    "report_export": "Export du rapport...",
    "data_validation": "Validation des données...",
    "format_conversion": "Conversion de format...",
    "compression_process": "Processus de compression...",
    "decompression_process": "Processus de décompression...",
    "encryption_process": "Processus de chiffrement...",
    "decryption_process": "Processus de déchiffrement...",
    "checksum_calculation": "Calcul du checksum...",
    "signature_verification": "Vérification de signature...",
    "key_generation": "Génération de clé...",
    "certificate_validation": "Validation de certificat...",
    "ssl_handshake": "Poignée de main SSL...",
    "database_connection": "Connexion à la base de données...",
    "query_execution": "Exécution de requête...",
    "transaction_commit": "Validation de transaction...",
    "transaction_rollback": "Annulation de transaction...",
    "backup_restore": "Restauration de sauvegarde...",
    "log_rotation": "Rotation des logs...",
    "cache_warmup": "Préchauffage du cache...",
    "session_refresh": "Actualisation de session...",
    "token_refresh": "Actualisation de token...",
    "rate_limit_check": "Vérification de limite de taux...",
    "quota_check": "Vérification de quota...",
    "resource_allocation": "Allocation de ressources...",
    "resource_cleanup": "Nettoyage de ressources...",
    "memory_optimization": "Optimisation mémoire...",
    "disk_cleanup": "Nettoyage disque...",
    "temp_file_cleanup": "Nettoyage fichiers temporaires...",
    "orphaned_file_cleanup": "Nettoyage fichiers orphelins...",
    "duplicate_removal": "Suppression des doublons...",
    "data_deduplication": "Déduplication des données...",
    "index_optimization": "Optimisation d'index...",
    "query_optimization": "Optimisation de requête...",
    "performance_tuning": "Ajustement de performance...",
    "load_balancing": "Équilibrage de charge...",
    "failover_process": "Processus de basculement...",
    "health_check": "Vérification de santé...",
    "monitoring_setup": "Configuration du monitoring...",
    "alert_processing": "Traitement d'alerte...",
    "metric_collection": "Collecte de métriques...",
    "log_parsing": "Analyse des logs...",
    "pattern_matching": "Correspondance de motifs...",
    "regex_processing": "Traitement d'expressions régulières...",
    "xml_parsing": "Analyse XML...",
    "json_parsing": "Analyse JSON...",
    "yaml_parsing": "Analyse YAML...",
    "csv_parsing": "Analyse CSV...",
    "excel_parsing": "Analyse Excel...",
    "pdf_generation": "Génération PDF...",
    "image_processing": "Traitement d'image...",
    "video_processing": "Traitement vidéo...",
    "audio_processing": "Traitement audio...",
    "archive_creation": "Création d'archive...",
    "archive_extraction": "Extraction d'archive...",
    "checksum_verification": "Vérification de checksum...",
    "virus_scan": "Scan antivirus...",
    "malware_detection": "Détection de malware...",
    "security_audit": "Audit de sécurité...",
    "compliance_check": "Vérification de conformité...",
    "license_check": "Vérification de licence...",
    "update_download": "Téléchargement de mise à jour...",
    "update_installation": "Installation de mise à jour...",
    "dependency_resolution": "Résolution de dépendances...",
    "package_installation": "Installation de package...",
    "package_removal": "Suppression de package...",
    "service_start": "Démarrage de service...",
    "service_stop": "Arrêt de service...",
    "service_restart": "Redémarrage de service...",
    "process_kill": "Arrêt de processus...",
    "thread_creation": "Création de thread...",
    "thread_cleanup": "Nettoyage de thread...",
    "memory_allocation": "Allocation mémoire...",
    "memory_deallocation": "Désallocation mémoire...",
    "garbage_collection": "Collecte de déchets...",
    "object_serialization": "Sérialisation d'objet...",
    "object_deserialization": "Désérialisation d'objet...",
    "data_serialization": "Sérialisation de données...",
    "data_deserialization": "Désérialisation de données...",
    "protocol_handshake": "Poignée de main de protocole...",
    "connection_establishment": "Établissement de connexion...",
    "connection_termination": "Terminaison de connexion...",
    "data_transmission": "Transmission de données...",
    "data_reception": "Réception de données...",
    "packet_processing": "Traitement de paquets...",
    "routing_calculation": "Calcul de routage...",
    "load_calculation": "Calcul de charge...",
    "capacity_planning": "Planification de capacité...",
    "resource_planning": "Planification de ressources...",
    "scheduling_optimization": "Optimisation de planification...",
    "workflow_execution": "Exécution de workflow...",
    "pipeline_processing": "Traitement de pipeline...",
    "batch_processing": "Traitement par lot...",
    "stream_processing": "Traitement de flux...",
    "real_time_processing": "Traitement en temps réel...",
    "asynchronous_processing": "Traitement asynchrone...",
    "synchronous_processing": "Traitement synchrone...",
    "parallel_processing": "Traitement parallèle...",
    "distributed_processing": "Traitement distribué...",
    "cloud_sync": "Synchronisation cloud...",
    "local_sync": "Synchronisation locale...",
    "remote_sync": "Synchronisation distante...",
    "data_mirroring": "Miroir de données...",
    "data_replication": "Réplication de données...",
    "backup_scheduling": "Planification de sauvegarde...",
    "restore_scheduling": "Planification de restauration...",
    "maintenance_scheduling": "Planification de maintenance...",
    "update_scheduling": "Planification de mise à jour...",
    "monitoring_scheduling": "Planification de monitoring...",
    "report_scheduling": "Planification de rapport...",
    "notification_scheduling": "Planification de notification...",
    "alert_scheduling": "Planification d'alerte...",
    "task_scheduling": "Planification de tâche...",
    "job_scheduling": "Planification de job...",
    "cron_setup": "Configuration cron...",
    "daemon_setup": "Configuration daemon...",
    "service_setup": "Configuration de service...",
    "application_setup": "Configuration d'application...",
    "system_setup": "Configuration système...",
    "network_setup": "Configuration réseau...",
    "security_setup": "Configuration sécurité...",
    "user_setup": "Configuration utilisateur...",
    "group_setup": "Configuration de groupe...",
    "permission_setup": "Configuration de permissions...",
    "access_control_setup": "Configuration de contrôle d'accès...",
    "authentication_setup": "Configuration d'authentification...",
    "authorization_setup": "Configuration d'autorisation...",
    "encryption_setup": "Configuration de chiffrement...",
    "certificate_setup": "Configuration de certificat...",
    "ssl_setup": "Configuration SSL...",
    "tls_setup": "Configuration TLS...",
    "vpn_setup": "Configuration VPN...",
    "firewall_setup": "Configuration du firewall...",
    "fin": "Fin..."
}


# Fonction utilitaire pour obtenir un message de spinner
def get_spinner_message(operation_type: str, default_message: str = "Exécution en cours...") -> str:
    """
    Récupère un message de spinner prédéfini ou retourne le message par défaut.
    
    Args:
        operation_type: Type d'opération (clé dans SPINNER_MESSAGES)
        default_message: Message par défaut si l'opération n'est pas trouvée
    
    Returns:
        Message de spinner approprié
    """
    return SPINNER_MESSAGES.get(operation_type, default_message)


# Fonction pour créer un spinner personnalisé
def create_custom_spinner(message: str, spinner_type: str = "dots4"):
    """
    Crée un contexte de spinner personnalisé.
    
    Args:
        message: Message à afficher
        spinner_type: Type de spinner
    
    Returns:
        Contexte de spinner Rich
    """
    return console.status(
        f"[bold cyan]{message}[/bold cyan]",
        spinner=spinner_type
    )


if __name__ == "__main__":
    # Test des décorateurs
    @with_spinner("Test de spinner...")
    def test_function():
        import time
        time.sleep(2)
        return "Test réussi !"
    
    print("Test du décorateur de spinner...")
    result = test_function()
    print(f"Résultat: {result}")
