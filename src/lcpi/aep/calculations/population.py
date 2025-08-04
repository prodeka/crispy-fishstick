"""
Calculs de projection démographique pour l'AEP

Ce module réutilise les fonctions d'hydrodrain et ajoute des fonctionnalités
spécifiques à l'AEP selon le document de référence.
"""

import sys
import os
from typing import Dict, List, Tuple, Optional, Any
from rich.console import Console
from rich.panel import Panel

# Ajouter le chemin pour importer les modules hydrodrain
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from lcpi.hydrodrain.calculs.population import prevoir_population
    from lcpi.aep.core.constants import HELP_MESSAGES
    from lcpi.aep.core.formulas import *
    from lcpi.aep.core.validators import validate_population_data, AEPValidationError
except ImportError as e:
    print(f"Erreur d'import: {e}")
    prevoir_population = None

console = Console()

def calculate_population_projection(
    population_base: Optional[float] = None,
    taux_croissance: Optional[float] = None,
    annees: Optional[int] = None,
    donnees: Optional[Dict[str, Any]] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Calcule la projection démographique selon la méthode de Malthus.
    
    Formule: Pn = Po × (1 + a)^n
    
    Args:
        population_base: Population de référence (Po)
        taux_croissance: Taux d'accroissement annuel (a)
        annees: Nombre d'années (n)
        donnees: Dictionnaire avec toutes les données (alternative aux paramètres individuels)
        verbose: Afficher les détails de calcul
    
    Returns:
        Dictionnaire contenant la population projetée et les détails de calcul
        
    CLI Usage:
        lcpi aep population --base <pop> --rate <taux> --years <années>
        
    REPL Usage:
        >>> from lcpi.aep.calculations import population
        >>> result = population.calculate_projection(9967, 0.037, 20)
    """
    
    # Afficher l'aide si aucun paramètre n'est fourni
    if all(param is None for param in [population_base, taux_croissance, annees]) and donnees is None:
        console.print(Panel(
            HELP_MESSAGES["population"],
            title="[bold blue]Aide - Projection Démographique AEP[/bold blue]",
            border_style="blue"
        ))
        return {"statut": "aide_affichee"}
    
    try:
        # Utiliser les données fournies ou créer un dictionnaire
        if donnees is not None:
            data = donnees.copy()
        else:
            if population_base is None or taux_croissance is None or annees is None:
                raise AEPValidationError("Tous les paramètres (population_base, taux_croissance, annees) sont requis")
            
            data = {
                "methode": "malthus",
                "annee_projet": annees,
                "pop_annee_1": [population_base, 2025],  # Année de référence
                "pop_annee_2": [population_base * (1 + taux_croissance), 2026]  # Année suivante
            }
        
        # Valider les données
        data = validate_population_data(data)
        
        # Utiliser la fonction hydrodrain existante
        if prevoir_population:
            resultat_hydrodrain = prevoir_population(data)
            
            if resultat_hydrodrain.get("statut") == "SUCCES":
                # Enrichir avec les calculs AEP spécifiques
                population_projetee = resultat_hydrodrain["population_estimee"]
                
                # Calculs supplémentaires pour l'AEP
                croissance_absolue = population_projetee - data["pop_annee_1"][0]
                croissance_relative = (croissance_absolue / data["pop_annee_1"][0]) * 100
                
                resultat_aep = {
                    "statut": "SUCCES",
                    "methode": data["methode"],
                    "annee_projet": data["annee_projet"],
                    "population_base": data["pop_annee_1"][0],
                    "population_projetee": population_projetee,
                    "croissance_absolue": int(croissance_absolue),
                    "croissance_relative_pct": round(croissance_relative, 2),
                    "annee_base": data["pop_annee_1"][1],
                    "annee_finale": data["pop_annee_1"][1] + data["annee_projet"],
                    "details_calcul": resultat_hydrodrain,
                    "formule_utilisee": resultat_hydrodrain.get("formule", "Non spécifiée")
                }
                
                if verbose:
                    console.print(Panel(
                        f"[bold green]✅ Projection démographique réussie[/bold green]\n\n"
                        f"Population de base ({data['pop_annee_1'][1]}): {data['pop_annee_1'][0]:,} habitants\n"
                        f"Population projetée ({resultat_aep['annee_finale']}): {population_projetee:,} habitants\n"
                        f"Croissance: +{croissance_absolue:,} habitants (+{croissance_relative:.1f}%)\n"
                        f"Méthode: {data['methode'].title()}\n"
                        f"Formule: {resultat_hydrodrain.get('formule', 'Non spécifiée')}",
                        title="[bold blue]Résultats Projection Démographique[/bold blue]",
                        border_style="green"
                    ))
                
                return resultat_aep
            else:
                return resultat_hydrodrain
        else:
            # Fallback si la fonction hydrodrain n'est pas disponible
            if data["methode"] == "malthus":
                from lcpi.aep.core.formulas import formule_malthus
                population_projetee = formule_malthus(
                    data["pop_annee_1"][0], 
                    (data["pop_annee_2"][0] - data["pop_annee_1"][0]) / data["pop_annee_1"][0],
                    data["annee_projet"]
                )
                
                return {
                    "statut": "SUCCES",
                    "methode": "malthus",
                    "population_projetee": int(population_projetee),
                    "formule_utilisee": "Pn = Po × (1 + a)^n",
                    "message": "Calcul effectué avec formule locale (hydrodrain non disponible)"
                }
            else:
                return {
                    "statut": "ERREUR",
                    "message": "Méthode non implémentée en local. Module hydrodrain requis."
                }
    
    except AEPValidationError as e:
        return {"statut": "ERREUR", "message": f"Erreur de validation: {str(e)}"}
    except Exception as e:
        return {"statut": "ERREUR", "message": f"Erreur de calcul: {str(e)}"}

def calculate_population_projection_advanced(
    donnees: Dict[str, Any],
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Calcul de projection démographique avancé avec toutes les méthodes.
    
    Args:
        donnees: Dictionnaire contenant toutes les données de projection
        verbose: Afficher les détails de calcul
    
    Returns:
        Dictionnaire avec les résultats de toutes les méthodes
    """
    
    if donnees is None:
        console.print(Panel(
            HELP_MESSAGES["population"],
            title="[bold blue]Aide - Projection Démographique Avancée[/bold blue]",
            border_style="blue"
        ))
        return {"statut": "aide_affichee"}
    
    try:
        # Valider les données
        donnees = validate_population_data(donnees)
        
        # Utiliser la fonction hydrodrain existante
        if prevoir_population:
            resultat = prevoir_population(donnees)
            
            if verbose and resultat.get("statut") == "SUCCES":
                console.print(Panel(
                    f"[bold green]✅ Projection démographique avancée réussie[/bold green]\n\n"
                    f"Méthode: {donnees['methode'].title()}\n"
                    f"Population projetée: {resultat['population_estimee']:,} habitants\n"
                    f"Formule: {resultat.get('formule', 'Non spécifiée')}",
                    title="[bold blue]Résultats Projection Avancée[/bold blue]",
                    border_style="green"
                ))
            
            return resultat
        else:
            return {
                "statut": "ERREUR",
                "message": "Module hydrodrain non disponible pour les calculs avancés"
            }
    
    except AEPValidationError as e:
        return {"statut": "ERREUR", "message": f"Erreur de validation: {str(e)}"}
    except Exception as e:
        return {"statut": "ERREUR", "message": f"Erreur de calcul: {str(e)}"}

def compare_population_methods(
    population_base: float,
    taux_croissance: float,
    annees: int,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Compare différentes méthodes de projection démographique.
    
    Args:
        population_base: Population de référence
        taux_croissance: Taux d'accroissement annuel
        annees: Nombre d'années
        verbose: Afficher les détails
    
    Returns:
        Dictionnaire avec les résultats de toutes les méthodes
    """
    
    methodes = ["arithmetique", "geometrique", "malthus"]
    resultats = {}
    
    for methode in methodes:
        try:
            # Créer les données pour chaque méthode
            if methode == "arithmetique":
                pop_annee1 = [population_base, 2025]
                pop_annee2 = [population_base + (population_base * taux_croissance), 2026]
            else:  # geometrique et malthus
                pop_annee1 = [population_base, 2025]
                pop_annee2 = [population_base * (1 + taux_croissance), 2026]
            
            donnees = {
                "methode": methode,
                "annee_projet": annees,
                "pop_annee_1": pop_annee1,
                "pop_annee_2": pop_annee2
            }
            
            resultat = calculate_population_projection(donnees=donnees, verbose=False)
            resultats[methode] = resultat
            
        except Exception as e:
            resultats[methode] = {"statut": "ERREUR", "message": str(e)}
    
    if verbose:
        console.print(Panel(
            f"[bold blue]Comparaison des méthodes de projection[/bold blue]\n\n"
            f"Population de base: {population_base:,} habitants\n"
            f"Taux de croissance: {taux_croissance:.1%}\n"
            f"Horizon: {annees} années\n\n"
            + "\n".join([
                f"{methode.title()}: {resultats[methode].get('population_projetee', 'Erreur'):,} habitants"
                for methode in methodes
            ]),
            border_style="blue"
        ))
    
    return {
        "statut": "SUCCES",
        "population_base": population_base,
        "taux_croissance": taux_croissance,
        "annees": annees,
        "comparaison": resultats
    }

# Fonction d'aide pour l'interface CLI
def get_population_help() -> str:
    """Retourne l'aide pour les calculs de population"""
    return HELP_MESSAGES["population"] 