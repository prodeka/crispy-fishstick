"""
Module de journalisation pour LCPI.
Gère la création et la sauvegarde des fichiers de log JSON auditable.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import typer


class LogEntryModel(BaseModel):
    """
    Modèle Pydantic pour valider la structure d'un fichier de log.
    Assure la cohérence et la traçabilité des calculs.
    """
    
    id: str = Field(..., description="Identifiant unique du calcul (timestamp)")
    timestamp: str = Field(..., description="Date et heure du calcul (ISO format)")
    titre_calcul: str = Field(..., description="Titre descriptif du calcul")
    commande_executee: str = Field(..., description="Commande CLI complète exécutée")
    donnees_resultat: Dict[str, Any] = Field(..., description="Résultats du calcul")
    transparence_mathematique: Optional[List[str]] = Field(
        default_factory=list, 
        description="Formules et étapes de calcul pour l'audit"
    )
    hash_donnees_entree: Optional[str] = Field(
        None, 
        description="Hash SHA256 des données d'entrée pour la traçabilité"
    )
    dependances: Optional[List[str]] = Field(
        default_factory=list, 
        description="Liste des IDs de calculs dont dépend ce calcul"
    )
    duree_execution: Optional[float] = Field(
        None, 
        description="Durée d'exécution en secondes"
    )
    version_algorithme: Optional[str] = Field(
        None, 
        description="Version de l'algorithme utilisé"
    )
    parametres_entree: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        description="Paramètres d'entrée du calcul"
    )
    diagnostics: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        description="Informations de diagnostic et validation"
    )
    iterations: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        description="Détails des itérations si applicable"
    )


def calculate_input_hash(input_data: Dict[str, Any]) -> str:
    """
    Calcule le hash SHA256 des données d'entrée pour la traçabilité.
    
    Args:
        input_data: Dictionnaire des données d'entrée
        
    Returns:
        Hash SHA256 en format hexadécimal
    """
    # Sérialiser les données en JSON avec tri des clés pour garantir la reproductibilité
    json_str = json.dumps(input_data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(json_str.encode('utf-8')).hexdigest()


def log_calculation_result(
    titre_calcul: str,
    commande_executee: str,
    donnees_resultat: Dict[str, Any],
    projet_dir: Optional[Path] = None,
    transparence_mathematique: Optional[List[str]] = None,
    parametres_entree: Optional[Dict[str, Any]] = None,
    dependances: Optional[List[str]] = None,
    duree_execution: Optional[float] = None,
    version_algorithme: Optional[str] = None,
    diagnostics: Optional[Dict[str, Any]] = None,
    iterations: Optional[Dict[str, Any]] = None,
    verbose: bool = False
) -> str:
    """
    Journalise le résultat d'un calcul dans un fichier JSON auditable.
    
    Args:
        titre_calcul: Titre descriptif du calcul
        commande_executee: Commande CLI complète exécutée
        donnees_resultat: Résultats du calcul
        projet_dir: Répertoire du projet (par défaut: répertoire courant)
        transparence_mathematique: Formules et étapes de calcul
        parametres_entree: Paramètres d'entrée du calcul
        dependances: Liste des IDs de calculs dont dépend ce calcul
        duree_execution: Durée d'exécution en secondes
        version_algorithme: Version de l'algorithme utilisé
        diagnostics: Informations de diagnostic
        iterations: Détails des itérations
        verbose: Mode verbeux pour l'affichage
        
    Returns:
        ID du log créé (timestamp)
    """
    # Déterminer le répertoire du projet
    if projet_dir is None:
        projet_dir = Path.cwd()
    
    # Créer le dossier logs s'il n'existe pas
    logs_dir = projet_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Générer l'ID unique (timestamp)
    timestamp = datetime.now()
    log_id = timestamp.strftime("%Y%m%d_%H%M%S")
    
    # Calculer le hash des données d'entrée si fournies
    hash_donnees_entree = None
    if parametres_entree:
        hash_donnees_entree = calculate_input_hash(parametres_entree)
    
    # Créer l'objet de log
    log_entry = LogEntryModel(
        id=log_id,
        timestamp=timestamp.isoformat(),
        titre_calcul=titre_calcul,
        commande_executee=commande_executee,
        donnees_resultat=donnees_resultat,
        transparence_mathematique=transparence_mathematique or [],
        hash_donnees_entree=hash_donnees_entree,
        dependances=dependances or [],
        duree_execution=duree_execution,
        version_algorithme=version_algorithme,
        parametres_entree=parametres_entree or {},
        diagnostics=diagnostics or {},
        iterations=iterations or {}
    )
    
    # Valider l'objet avec Pydantic
    try:
        validated_log = log_entry.model_dump()
    except Exception as e:
        raise ValueError(f"Erreur de validation du log: {e}")
    
    # Créer le nom du fichier
    filename = f"log_{log_id}.json"
    log_file = logs_dir / filename
    
    # Sauvegarder le fichier JSON
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(validated_log, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise IOError(f"Erreur lors de la sauvegarde du log: {e}")
    
    # Affichage informatif
    if verbose:
        typer.echo(f"✅ Log sauvegardé: {log_file}")
        typer.echo(f"📊 ID: {log_id}")
        typer.echo(f"📝 Titre: {titre_calcul}")
        if hash_donnees_entree:
            typer.echo(f"🔗 Hash: {hash_donnees_entree[:16]}...")
    
    return log_id


def list_available_logs(projet_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Liste tous les logs disponibles dans le répertoire du projet.
    
    Args:
        projet_dir: Répertoire du projet (par défaut: répertoire courant)
        
    Returns:
        Liste des métadonnées des logs disponibles
    """
    if projet_dir is None:
        projet_dir = Path.cwd()
    
    logs_dir = projet_dir / "logs"
    if not logs_dir.exists():
        return []
    
    logs = []
    for log_file in logs_dir.glob("log_*.json"):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
                logs.append({
                    "id": log_data.get("id"),
                    "timestamp": log_data.get("timestamp"),
                    "titre_calcul": log_data.get("titre_calcul"),
                    "commande_executee": log_data.get("commande_executee"),
                    "file_path": log_file
                })
        except Exception as e:
            typer.echo(f"⚠️ Erreur lors de la lecture du log {log_file}: {e}")
    
    # Trier par timestamp (plus récent en premier)
    logs.sort(key=lambda x: x["timestamp"], reverse=True)
    return logs


def load_log_by_id(log_id: str, projet_dir: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """
    Charge un log spécifique par son ID.
    
    Args:
        log_id: ID du log à charger
        projet_dir: Répertoire du projet (par défaut: répertoire courant)
        
    Returns:
        Données du log ou None si non trouvé
    """
    if projet_dir is None:
        projet_dir = Path.cwd()
    
    log_file = projet_dir / "logs" / f"log_{log_id}.json"
    
    if not log_file.exists():
        return None
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        typer.echo(f"⚠️ Erreur lors de la lecture du log {log_id}: {e}")
        return None
