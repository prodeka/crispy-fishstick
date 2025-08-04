"""
Calculs de demande en eau pour l'AEP

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
    from lcpi.hydrodrain.calculs.demande_eau import estimer_demande_eau
    from lcpi.aep.core.constants import HELP_MESSAGES, DOTATIONS_EAU, COEFF_POINTE_JOURNALIERE, RENDEMENT_TECHNIQUE
    from lcpi.aep.core.formulas import *
    from lcpi.aep.core.validators import validate_demand_data, AEPValidationError
except ImportError as e:
    print(f"Erreur d'import: {e}")
    estimer_demande_eau = None

console = Console()

def calculate_water_demand(
    population: Optional[int] = None,
    dotation_l_j_hab: Optional[float] = None,
    coefficient_pointe: Optional[float] = None,
    donnees: Optional[Dict[str, Any]] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Calcule les besoins en eau potable selon le document AEP.
    
    Formules:
    - Besoin domestique: B_dom = Population × Dotation
    - Besoin annexe: B_a = 10% × B_dom
    - Besoin global: B_gbl = B_dom + B_a
    - Besoin pointe: B_npjp = B_gbl × Cpj
    - Besoin brut: B_bpjp = B_npjp / r_technique
    
    Args:
        population: Population desservie
        dotation_l_j_hab: Dotation en litres par jour et par habitant
        coefficient_pointe: Coefficient de pointe journalière (défaut: 1.5)
        donnees: Dictionnaire avec toutes les données (alternative aux paramètres individuels)
        verbose: Afficher les détails de calcul
    
    Returns:
        Dictionnaire contenant tous les besoins calculés
        
    CLI Usage:
        lcpi aep demand --population <pop> --dotation <l/j/hab> --coeff-pointe <k>
        
    REPL Usage:
        >>> from lcpi.aep.calculations import demand
        >>> result = demand.calculate_water_demand(20847, 60, 1.5)
    """
    
    # Afficher l'aide si aucun paramètre n'est fourni
    if all(param is None for param in [population, dotation_l_j_hab]) and donnees is None:
        console.print(Panel(
            HELP_MESSAGES["demand"],
            title="[bold blue]Aide - Calcul de Demande en Eau AEP[/bold blue]",
            border_style="blue"
        ))
        return {"statut": "aide_affichee"}
    
    try:
        # Utiliser les données fournies ou créer un dictionnaire
        if donnees is not None:
            data = donnees.copy()
        else:
            if population is None or dotation_l_j_hab is None:
                raise AEPValidationError("Les paramètres population et dotation sont requis")
            
            data = {
                "population": population,
                "dotation_domestique_l_j_hab": dotation_l_j_hab,
                "rendement_reseau": RENDEMENT_TECHNIQUE,
                "besoins_publics_m3_j": 0
            }
        
        # Valider les données
        data = validate_demand_data(data)
        
        # Utiliser la fonction hydrodrain existante
        if estimer_demande_eau:
            resultat_hydrodrain = estimer_demande_eau(data)
            
            if resultat_hydrodrain.get("statut") == "OK":
                # Enrichir avec les calculs AEP spécifiques
                besoin_journalier = resultat_hydrodrain["besoin_journalier_total_m3_jour"]
                production_requise = resultat_hydrodrain["production_requise_m3_jour"]
                debit_pointe_horaire = resultat_hydrodrain["debit_pointe_horaire_m3_h"]
                
                # Calculs supplémentaires selon le document AEP
                besoin_domestique = calculer_besoin_domestique(data["population"], data["dotation_domestique_l_j_hab"])
                besoin_annexe = calculer_besoin_annexe(besoin_domestique, 0.10)  # 10% selon document AEP
                besoin_global = calculer_besoin_global(besoin_domestique, besoin_annexe)
                
                # Utiliser le coefficient de pointe fourni ou celui par défaut
                coeff_pointe = coefficient_pointe if coefficient_pointe is not None else COEFF_POINTE_JOURNALIERE
                besoin_pointe = calculer_besoin_pointe(besoin_global, coeff_pointe)
                besoin_brut = calculer_besoin_brut(besoin_pointe, data["rendement_reseau"])
                
                # Calcul du coefficient de pointe horaire
                debit_moyen_horaire = besoin_brut / 24  # m³/h
                coeff_pointe_horaire = calculer_coefficient_pointe_horaire(debit_moyen_horaire)
                debit_pointe_horaire_aep = calculer_debit_pointe_horaire(debit_moyen_horaire, coeff_pointe_horaire)
                
                resultat_aep = {
                    "statut": "SUCCES",
                    "parametres_entree": {
                        "population": data["population"],
                        "dotation_l_j_hab": data["dotation_domestique_l_j_hab"],
                        "coefficient_pointe_journaliere": coeff_pointe,
                        "rendement_reseau": data["rendement_reseau"]
                    },
                    "besoins_calcules": {
                        "besoin_domestique_m3_jour": round(besoin_domestique, 2),
                        "besoin_annexe_m3_jour": round(besoin_annexe, 2),
                        "besoin_global_m3_jour": round(besoin_global, 2),
                        "besoin_pointe_m3_jour": round(besoin_pointe, 2),
                        "besoin_brut_m3_jour": round(besoin_brut, 2)
                    },
                    "debits_calcules": {
                        "debit_moyen_horaire_m3_h": round(debit_moyen_horaire, 2),
                        "coefficient_pointe_horaire": round(coeff_pointe_horaire, 2),
                        "debit_pointe_horaire_m3_h": round(debit_pointe_horaire_aep, 2)
                    },
                    "resultats_hydrodrain": resultat_hydrodrain,
                    "formules_utilisees": {
                        "besoin_domestique": "B_dom = Population × Dotation",
                        "besoin_annexe": "B_a = 10% × B_dom",
                        "besoin_global": "B_gbl = B_dom + B_a",
                        "besoin_pointe": "B_npjp = B_gbl × Cpj",
                        "besoin_brut": "B_bpjp = B_npjp / r_technique",
                        "coefficient_pointe_horaire": "Cph = 1.5 + 2.5/√Qmh"
                    }
                }
                
                if verbose:
                    console.print(Panel(
                        f"[bold green]✅ Calcul de demande en eau réussi[/bold green]\n\n"
                        f"Population: {data['population']:,} habitants\n"
                        f"Dotation: {data['dotation_domestique_l_j_hab']} L/j/hab\n\n"
                        f"[bold]Besoins journaliers:[/bold]\n"
                        f"• Domestique: {besoin_domestique:.1f} m³/jour\n"
                        f"• Annexe (10%): {besoin_annexe:.1f} m³/jour\n"
                        f"• Global: {besoin_global:.1f} m³/jour\n"
                        f"• Pointe (×{coeff_pointe}): {besoin_pointe:.1f} m³/jour\n"
                        f"• Brut (rendement {data['rendement_reseau']*100}%): {besoin_brut:.1f} m³/jour\n\n"
                        f"[bold]Débits:[/bold]\n"
                        f"• Moyen horaire: {debit_moyen_horaire:.1f} m³/h\n"
                        f"• Coefficient pointe horaire: {coeff_pointe_horaire:.2f}\n"
                        f"• Pointe horaire: {debit_pointe_horaire_aep:.1f} m³/h",
                        title="[bold blue]Résultats Calcul Demande en Eau[/bold blue]",
                        border_style="green"
                    ))
                
                return resultat_aep
            else:
                return resultat_hydrodrain
        else:
            # Fallback si la fonction hydrodrain n'est pas disponible
            if population is None or dotation_l_j_hab is None:
                raise AEPValidationError("Les paramètres population et dotation sont requis")
            
            # Calculs locaux
            besoin_domestique = calculer_besoin_domestique(population, dotation_l_j_hab)
            besoin_annexe = calculer_besoin_annexe(besoin_domestique, 0.10)
            besoin_global = calculer_besoin_global(besoin_domestique, besoin_annexe)
            
            coeff_pointe = coefficient_pointe if coefficient_pointe is not None else COEFF_POINTE_JOURNALIERE
            besoin_pointe = calculer_besoin_pointe(besoin_global, coeff_pointe)
            besoin_brut = calculer_besoin_brut(besoin_pointe, RENDEMENT_TECHNIQUE)
            
            return {
                "statut": "SUCCES",
                "message": "Calcul effectué avec formules locales (hydrodrain non disponible)",
                "besoins_calcules": {
                    "besoin_domestique_m3_jour": round(besoin_domestique, 2),
                    "besoin_annexe_m3_jour": round(besoin_annexe, 2),
                    "besoin_global_m3_jour": round(besoin_global, 2),
                    "besoin_pointe_m3_jour": round(besoin_pointe, 2),
                    "besoin_brut_m3_jour": round(besoin_brut, 2)
                }
            }
    
    except AEPValidationError as e:
        return {"statut": "ERREUR", "message": f"Erreur de validation: {str(e)}"}
    except Exception as e:
        return {"statut": "ERREUR", "message": f"Erreur de calcul: {str(e)}"}

def calculate_water_demand_advanced(
    donnees: Dict[str, Any],
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Calcul de demande en eau avancé avec toutes les options.
    
    Args:
        donnees: Dictionnaire contenant toutes les données de demande
        verbose: Afficher les détails de calcul
    
    Returns:
        Dictionnaire avec les résultats détaillés
    """
    
    if donnees is None:
        console.print(Panel(
            HELP_MESSAGES["demand"],
            title="[bold blue]Aide - Calcul de Demande Avancée[/bold blue]",
            border_style="blue"
        ))
        return {"statut": "aide_affichee"}
    
    try:
        # Valider les données
        donnees = validate_demand_data(donnees)
        
        # Utiliser la fonction hydrodrain existante
        if estimer_demande_eau:
            resultat = estimer_demande_eau(donnees)
            
            if verbose and resultat.get("statut") == "OK":
                console.print(Panel(
                    f"[bold green]✅ Calcul de demande avancée réussi[/bold green]\n\n"
                    f"Population: {donnees['population']:,} habitants\n"
                    f"Besoin journalier total: {resultat['besoin_journalier_total_m3_jour']:.1f} m³/jour\n"
                    f"Production requise: {resultat['production_requise_m3_jour']:.1f} m³/jour\n"
                    f"Débit de pointe horaire: {resultat['debit_pointe_horaire_m3_h']:.1f} m³/h",
                    title="[bold blue]Résultats Demande Avancée[/bold blue]",
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

def calculate_water_demand_by_type(
    population: int,
    type_consommation: str = "branchement_prive",
    coefficient_pointe: float = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Calcule la demande en eau selon le type de consommation.
    
    Args:
        population: Population desservie
        type_consommation: Type de consommation (branchement_prive, borne_fontaine, etc.)
        coefficient_pointe: Coefficient de pointe journalière
        verbose: Afficher les détails
    
    Returns:
        Dictionnaire avec les résultats
    """
    
    # Récupérer la dotation selon le type
    if type_consommation not in DOTATIONS_EAU:
        return {
            "statut": "ERREUR",
            "message": f"Type de consommation invalide: {type_consommation}. Types valides: {list(DOTATIONS_EAU.keys())}"
        }
    
    dotation = DOTATIONS_EAU[type_consommation]
    
    return calculate_water_demand(
        population=population,
        dotation_l_j_hab=dotation,
        coefficient_pointe=coefficient_pointe,
        verbose=verbose
    )

def compare_water_demand_scenarios(
    population: int,
    scenarios: List[Dict[str, Any]],
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Compare différents scénarios de demande en eau.
    
    Args:
        population: Population de référence
        scenarios: Liste des scénarios à comparer
        verbose: Afficher les détails
    
    Returns:
        Dictionnaire avec la comparaison
    """
    
    resultats = {}
    
    for i, scenario in enumerate(scenarios):
        try:
            nom_scenario = scenario.get("nom", f"Scénario {i+1}")
            dotation = scenario.get("dotation", 60)
            coeff_pointe = scenario.get("coefficient_pointe", 1.5)
            
            resultat = calculate_water_demand(
                population=population,
                dotation_l_j_hab=dotation,
                coefficient_pointe=coeff_pointe,
                verbose=False
            )
            
            resultats[nom_scenario] = resultat
            
        except Exception as e:
            resultats[f"Scénario {i+1}"] = {"statut": "ERREUR", "message": str(e)}
    
    if verbose:
        console.print(Panel(
            f"[bold blue]Comparaison des scénarios de demande[/bold blue]\n\n"
            f"Population: {population:,} habitants\n\n"
            + "\n".join([
                f"{nom}: {resultat.get('besoins_calcules', {}).get('besoin_brut_m3_jour', 'Erreur'):.1f} m³/jour"
                for nom, resultat in resultats.items()
            ]),
            border_style="blue"
        ))
    
    return {
        "statut": "SUCCES",
        "population": population,
        "comparaison": resultats
    }

# Fonction d'aide pour l'interface CLI
def get_demand_help() -> str:
    """Retourne l'aide pour les calculs de demande"""
    return HELP_MESSAGES["demand"] 