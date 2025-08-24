"""
Décorateur global pour l'intégration automatique de la journalisation dans toutes les commandes LCPI.

Ce module fournit un décorateur qui peut être appliqué à n'importe quelle commande CLI
pour ajouter automatiquement la journalisation sans modifier la logique métier.
"""

import functools
import time
import typer
from typing import Callable, Any, Optional, Dict
from pathlib import Path
import json
from datetime import datetime

from ..lcpi_logging.logger import lcpi_logger


def with_automatic_logging(
    plugin_name: str,
    command_name: Optional[str] = None,
    log_by_default: bool = True
):
    """
    Décorateur pour ajouter automatiquement la journalisation à une commande CLI.
    
    Args:
        plugin_name: Nom du plugin (aep, cm, bois, etc.)
        command_name: Nom de la commande (optionnel, sera déduit automatiquement)
        log_by_default: Si True, journalise par défaut (demande confirmation si --log non spécifié)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extraire les paramètres de journalisation
            should_log = kwargs.get('log', None)
            no_log = kwargs.get('no_log', False)
            
            # Déterminer si on doit journaliser
            if no_log:
                should_log = False
            elif should_log is None and log_by_default:
                # Demander confirmation si pas spécifié
                try:
                    should_log = typer.confirm("📝 Voulez-vous journaliser ce calcul ?")
                except typer.Exit:
                    should_log = False
            
            # Exécuter la fonction originale
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                status = "success"
                error_message = None
            except Exception as e:
                execution_time = time.time() - start_time
                status = "error"
                error_message = str(e)
                raise
            
            # Journaliser si demandé
            if should_log:
                try:
                    # Construire les paramètres d'entrée
                    parameters = _extract_parameters(kwargs)
                    
                    # Construire la commande exécutée
                    command_executed = _build_command_string(
                        plugin_name, 
                        command_name or func.__name__, 
                        kwargs
                    )
                    
                    # Journaliser
                    log_id = lcpi_logger.log_calculation_result(
                        plugin=plugin_name,
                        command=command_name or func.__name__,
                        parameters=parameters,
                        results=result if status == "success" else {"error": error_message},
                        execution_time=execution_time,
                        status=status,
                        error_message=error_message,
                        metadata={
                            "command_executed": command_executed,
                            "function_name": func.__name__,
                            "module": func.__module__
                        }
                    )
                    
                    # Afficher confirmation si verbose
                    if kwargs.get('verbose', False):
                        typer.echo(f"📊 Calcul journalisé avec l'ID: {log_id}")
                        
                except Exception as logging_error:
                    # Ne pas faire échouer la commande si la journalisation échoue
                    if kwargs.get('verbose', False):
                        typer.echo(f"⚠️  Erreur lors de la journalisation: {logging_error}")
            
            return result
        
        return wrapper
    return decorator


def _extract_parameters(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extrait les paramètres pertinents pour la journalisation.
    Exclut les paramètres internes et les options de journalisation.
    """
    # Paramètres à exclure
    exclude_params = {
        'log', 'no_log', 'verbose', 'output', 'export', 
        'help', 'version', 'json', 'quiet', 'silent'
    }
    
    parameters = {}
    for key, value in kwargs.items():
        if key not in exclude_params and value is not None:
            # Convertir les Path en string
            if isinstance(value, Path):
                parameters[key] = str(value)
            else:
                parameters[key] = value
    
    return parameters


def _build_command_string(plugin_name: str, command_name: str, kwargs: Dict[str, Any]) -> str:
    """
    Construit la chaîne de commande exécutée pour la journalisation.
    """
    command_parts = ["lcpi", plugin_name, command_name]
    
    # Ajouter les arguments positionnels (si détectables)
    # Note: Ceci est une approximation, les vrais arguments positionnels
    # sont difficiles à extraire depuis kwargs
    
    # Ajouter les options
    for key, value in kwargs.items():
        if value is not None and key not in ['log', 'no_log', 'verbose']:
            if isinstance(value, bool) and value:
                command_parts.append(f"--{key}")
            elif not isinstance(value, bool):
                command_parts.extend([f"--{key}", str(value)])
    
    return " ".join(command_parts)


def add_logging_options(func: Callable) -> Callable:
    """
    Décorateur pour ajouter automatiquement les options de journalisation
    à une commande Typer.
    
    Usage:
        @app.command()
        @add_logging_options
        @with_automatic_logging("aep", "network-unified")
        def network_unified(...):
            ...
    """
    # Ajouter les paramètres de journalisation
    func.__annotations__['log'] = Optional[bool]
    func.__annotations__['no_log'] = bool
    
    # Ajouter les options Typer
    original_signature = func.__signature__
    
    def wrapper(*args, **kwargs):
        # Les options seront ajoutées automatiquement par Typer
        return func(*args, **kwargs)
    
    # Préserver la signature originale
    wrapper.__signature__ = original_signature
    wrapper.__annotations__ = func.__annotations__
    
    return wrapper


# Décorateur combiné pour faciliter l'usage
def logged_command(
    plugin_name: str,
    command_name: Optional[str] = None,
    log_by_default: bool = True,
    **typer_options
):
    """
    Décorateur combiné qui ajoute automatiquement la journalisation
    et les options de journalisation à une commande.
    
    Usage:
        @logged_command("aep", "network-unified", log_by_default=True)
        def network_unified(
            debit: float = typer.Argument(...),
            verbose: bool = typer.Option(False, "--verbose")
        ):
            ...
    """
    def decorator(func: Callable) -> Callable:
        # Ajouter les options de journalisation
        func = add_logging_options(func)
        
        # Ajouter la journalisation automatique
        func = with_automatic_logging(plugin_name, command_name, log_by_default)(func)
        
        # Retourner la fonction décorée
        return func
    
    return decorator
