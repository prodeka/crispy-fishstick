"""
Utilitaires pour les commandes CLI avec affichage automatique des paramètres d'entrée.
"""

from rich.console import Console
from rich.panel import Panel
from typing import List, Dict, Any, Optional
import typer

console = Console()

def show_input_parameters(
    command_name: str,
    required_params: List[Dict[str, Any]],
    optional_params: Optional[List[Dict[str, Any]]] = None,
    examples: Optional[List[str]] = None,
    description: Optional[str] = None
) -> None:
    """
    Affiche les paramètres d'entrée pour une commande.
    
    Args:
        command_name: Nom de la commande
        required_params: Liste des paramètres obligatoires
        optional_params: Liste des paramètres optionnels
        examples: Exemples d'utilisation
        description: Description de la commande
    """
    content = f"[bold blue]Paramètres d'entrée pour {command_name} :[/bold blue]\n\n"
    
    if description:
        content += f"[italic]{description}[/italic]\n\n"
    
    if required_params:
        content += "[bold]Paramètres obligatoires :[/bold]\n"
        for param in required_params:
            short_opt = f" (-{param['short']})" if 'short' in param else ""
            content += f"• --{param['name']}{short_opt} : {param['help']}\n"
        content += "\n"
    
    if optional_params:
        content += "[bold]Paramètres optionnels :[/bold]\n"
        for param in optional_params:
            short_opt = f" (-{param['short']})" if 'short' in param else ""
            default = f" (défaut: {param['default']})" if 'default' in param else ""
            content += f"• --{param['name']}{short_opt} : {param['help']}{default}\n"
        content += "\n"
    
    if examples:
        content += "[bold]Exemple d'utilisation :[/bold]\n"
        for example in examples:
            content += f"{example}\n"
    
    console.print(Panel(
        content,
        title=f"[bold green]Paramètres d'entrée - {command_name}[/bold green]",
        border_style="blue"
    ))

def check_required_params(*args, **kwargs) -> bool:
    """
    Vérifie si tous les paramètres requis sont fournis.
    
    Args:
        *args: Paramètres positionnels
        **kwargs: Paramètres nommés
        
    Returns:
        True si tous les paramètres requis sont fournis, False sinon
    """
    # Vérifier les paramètres positionnels
    for arg in args:
        if arg is None:
            return False
    
    # Vérifier les paramètres nommés
    for value in kwargs.values():
        if value is None:
            return False
    
    return True

def create_parameter_dict(
    name: str,
    help_text: str,
    short: Optional[str] = None,
    default: Any = None
) -> Dict[str, Any]:
    """
    Crée un dictionnaire de paramètre standardisé.
    
    Args:
        name: Nom du paramètre
        help_text: Texte d'aide
        short: Option courte (ex: 'n' pour --name)
        default: Valeur par défaut
        
    Returns:
        Dictionnaire du paramètre
    """
    param = {
        "name": name,
        "help": help_text
    }
    
    if short:
        param["short"] = short
    if default is not None:
        param["default"] = default
        
    return param

def create_typer_option(
    name: str,
    help_text: str,
    short: Optional[str] = None,
    default: Any = None,
    required: bool = False
) -> Any:
    """
    Crée une option Typer avec gestion automatique des paramètres requis.
    
    Args:
        name: Nom du paramètre
        help_text: Texte d'aide
        short: Option courte
        default: Valeur par défaut
        required: Si True, le paramètre est obligatoire
        
    Returns:
        Option Typer
    """
    if required:
        if short:
            return typer.Option(None, f"--{name}", f"-{short}", help=help_text)
        else:
            return typer.Option(None, f"--{name}", help=help_text)
    else:
        if short:
            return typer.Option(default, f"--{name}", f"-{short}", help=help_text)
        else:
            return typer.Option(default, f"--{name}", help=help_text) 