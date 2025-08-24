"""
Template pour l'utilisation du décorateur de journalisation automatique.

Ce fichier montre comment appliquer le décorateur @logged_command
à n'importe quelle commande LCPI pour ajouter automatiquement la journalisation.
"""

import typer
from pathlib import Path
from typing import Optional

# Import du décorateur de journalisation
from .logging_decorator import logged_command

app = typer.Typer(name="example", help="Exemple d'utilisation du décorateur de journalisation")

# =============================================================================
# EXEMPLE 1: Commande simple avec journalisation automatique
# =============================================================================

@app.command()
@logged_command("example", "simple-calc", log_by_default=True)
def simple_calc(
    value: float = typer.Argument(..., help="Valeur à calculer"),
    multiplier: float = typer.Option(2.0, "--multiplier", "-m", help="Multiplicateur"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Affichage détaillé")
):
    """
    Exemple de commande simple avec journalisation automatique.
    
    Cette commande sera automatiquement journalisée avec:
    - Les paramètres d'entrée (value, multiplier)
    - Le résultat du calcul
    - Le temps d'exécution
    - La commande exécutée
    """
    result = value * multiplier
    
    if verbose:
        typer.echo(f"📊 Calcul: {value} × {multiplier} = {result}")
    else:
        typer.echo(f"Résultat: {result}")
    
    return {"input_value": value, "multiplier": multiplier, "result": result}


# =============================================================================
# EXEMPLE 2: Commande complexe avec gestion d'erreurs
# =============================================================================

@app.command()
@logged_command("example", "complex-calc", log_by_default=False)
def complex_calc(
    input_file: Path = typer.Argument(..., help="Fichier d'entrée"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie"),
    method: str = typer.Option("default", "--method", "-m", help="Méthode de calcul"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Affichage détaillé")
):
    """
    Exemple de commande complexe avec journalisation automatique.
    
    Cette commande montre:
    - Gestion des fichiers d'entrée/sortie
    - Paramètres optionnels
    - Gestion d'erreurs (automatiquement journalisées)
    """
    try:
        # Simulation d'un calcul complexe
        if not input_file.exists():
            raise FileNotFoundError(f"Fichier d'entrée non trouvé: {input_file}")
        
        # Calcul simulé
        result = {
            "input_file": str(input_file),
            "method": method,
            "processed_data": "données traitées",
            "statistics": {"count": 100, "mean": 42.5}
        }
        
        # Sauvegarder le résultat si demandé
        if output_file:
            import json
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            result["output_file"] = str(output_file)
        
        if verbose:
            typer.echo(f"✅ Calcul terminé avec succès")
            typer.echo(f"📁 Fichier traité: {input_file}")
            if output_file:
                typer.echo(f"💾 Résultat sauvegardé: {output_file}")
        
        return result
        
    except Exception as e:
        if verbose:
            typer.echo(f"❌ Erreur lors du calcul: {e}")
        raise


# =============================================================================
# EXEMPLE 3: Commande avec journalisation conditionnelle
# =============================================================================

@app.command()
@logged_command("example", "conditional-calc", log_by_default=False)
def conditional_calc(
    data: str = typer.Argument(..., help="Données à traiter"),
    threshold: float = typer.Option(10.0, "--threshold", "-t", help="Seuil de traitement"),
    save_intermediate: bool = typer.Option(False, "--save-intermediate", help="Sauvegarder les résultats intermédiaires"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Affichage détaillé")
):
    """
    Exemple de commande avec journalisation conditionnelle.
    
    Cette commande montre comment la journalisation capture:
    - Les paramètres de contrôle
    - Les résultats intermédiaires
    - Les décisions conditionnelles
    """
    # Traitement conditionnel
    if len(data) > threshold:
        result = {
            "status": "processed",
            "data_length": len(data),
            "threshold": threshold,
            "intermediate_results": ["étape1", "étape2"] if save_intermediate else None
        }
    else:
        result = {
            "status": "skipped",
            "data_length": len(data),
            "threshold": threshold,
            "reason": "Données trop courtes"
        }
    
    if verbose:
        typer.echo(f"📊 Statut: {result['status']}")
        typer.echo(f"📏 Longueur: {result['data_length']}")
        typer.echo(f"🎯 Seuil: {result['threshold']}")
    
    return result


# =============================================================================
# GUIDE D'UTILISATION
# =============================================================================

"""
GUIDE D'UTILISATION DU DÉCORATEUR @logged_command

1. IMPORTATION:
   from lcpi.core.logging_decorator import logged_command

2. APPLICATION:
   @app.command()
   @logged_command("plugin_name", "command_name", log_by_default=True)
   def your_command(...):
       ...

3. PARAMÈTRES DU DÉCORATEUR:
   - plugin_name: Nom du plugin (aep, cm, bois, etc.)
   - command_name: Nom de la commande (optionnel, déduit automatiquement)
   - log_by_default: Si True, demande confirmation si --log non spécifié

4. OPTIONS AJOUTÉES AUTOMATIQUEMENT:
   --log: Journaliser le calcul (demande confirmation si non spécifié)
   --no-log: Ne pas journaliser le calcul

5. FONCTIONNALITÉS AUTOMATIQUES:
   - Capture des paramètres d'entrée
   - Mesure du temps d'exécution
   - Gestion des erreurs
   - Construction de la commande exécutée
   - Journalisation JSON structurée

6. EXEMPLE COMPLET:
   @app.command()
   @logged_command("aep", "network-unified", log_by_default=True)
   def network_unified(
       input_file: Path = typer.Argument(...),
       solver: str = typer.Option("epanet", "--solver"),
       verbose: bool = typer.Option(False, "--verbose")
   ):
       # Votre logique métier ici
       result = perform_calculation(input_file, solver)
       return result
       
   # Utilisation:
   # lcpi aep network-unified input.inp --solver epanet --log
   # lcpi aep network-unified input.inp --solver epanet --no-log
   # lcpi aep network-unified input.inp --solver epanet  # Demande confirmation
"""
