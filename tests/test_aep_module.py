#!/usr/bin/env python3
"""
Script de test pour le module AEP (Alimentation en Eau Potable)

Ce script teste toutes les fonctionnalités du module AEP en réutilisant
les fonctions existantes d'hydrodrain et en ajoutant les nouvelles
fonctionnalités spécifiques à l'AEP.
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Imports au niveau module pour éviter les erreurs de syntaxe
try:
    from lcpi.aep.core.constants import *
    from lcpi.aep.core.formulas import *
    from lcpi.aep.core.validators import *
    from lcpi.aep.calculations.population import calculate_population_projection
    from lcpi.aep.calculations.demand import calculate_water_demand
    # Import spécifique des fonctions utilisées dans les tests
    from lcpi.aep.core.formulas import (
        formule_malthus, calculer_besoin_domestique, calculer_besoin_annexe,
        calculer_besoin_global, calculer_besoin_pointe, calculer_besoin_brut
    )
    from lcpi.aep.core.validators import validate_population_data, validate_demand_data
    IMPORTS_OK = True
except ImportError as e:
    IMPORTS_OK = False
    IMPORT_ERROR = str(e)

def test_imports():
    """Teste les imports du module AEP"""
    console.print(Panel(
        "[bold blue]🔍 TEST DES IMPORTS DU MODULE AEP[/bold blue]",
        border_style="blue"
    ))
    
    if IMPORTS_OK:
        console.print("✅ [green]Imports core AEP réussis[/green]")
        console.print("✅ [green]Imports formules AEP réussis[/green]")
        console.print("✅ [green]Imports validateurs AEP réussis[/green]")
        console.print("✅ [green]Import population AEP réussi[/green]")
        console.print("✅ [green]Import demande AEP réussi[/green]")
        return True
    else:
        console.print(f"❌ [red]Erreur d'import: {IMPORT_ERROR}[/red]")
        return False

def test_population_calculations():
    """Teste les calculs de projection démographique"""
    console.print(Panel(
        "[bold blue]📊 TEST DES CALCULS DE PROJECTION DÉMOGRAPHIQUE[/bold blue]",
        border_style="blue"
    ))
    
    try:
        from lcpi.aep.calculations.population import calculate_population_projection
        
        # Test avec les données du document AEP
        resultat = calculate_population_projection(
            population_base=9967,
            taux_croissance=0.037,
            annees=20,
            verbose=True
        )
        
        if resultat.get("statut") == "SUCCES":
            console.print("✅ [green]Calcul de projection démographique réussi[/green]")
            console.print(f"   Population projetée: {resultat.get('population_projetee', 'N/A'):,} habitants")
            return True
        else:
            console.print(f"❌ [red]Erreur dans le calcul: {resultat.get('message', 'Erreur inconnue')}[/red]")
            return False
            
    except Exception as e:
        console.print(f"❌ [red]Erreur lors du test: {e}[/red]")
        return False

def test_demand_calculations():
    """Teste les calculs de demande en eau"""
    console.print(Panel(
        "[bold blue]💧 TEST DES CALCULS DE DEMANDE EN EAU[/bold blue]",
        border_style="blue"
    ))
    
    try:
        from lcpi.aep.calculations.demand import calculate_water_demand
        
        # Test avec les données du document AEP
        resultat = calculate_water_demand(
            population=20847,
            dotation_l_j_hab=60,
            coefficient_pointe=1.5,
            verbose=True
        )
        
        if resultat.get("statut") == "SUCCES":
            console.print("✅ [green]Calcul de demande en eau réussi[/green]")
            besoins = resultat.get("besoins_calcules", {})
            console.print(f"   Besoin brut journalier: {besoins.get('besoin_brut_m3_jour', 'N/A'):.1f} m³/jour")
            return True
        else:
            console.print(f"❌ [red]Erreur dans le calcul: {resultat.get('message', 'Erreur inconnue')}[/red]")
            return False
            
    except Exception as e:
        console.print(f"❌ [red]Erreur lors du test: {e}[/red]")
        return False

def test_formulas():
    """Teste les formules mathématiques"""
    console.print(Panel(
        "[bold blue]🧮 TEST DES FORMULES MATHÉMATIQUES[/bold blue]",
        border_style="blue"
    ))
    
    try:
        # Test formule de Malthus
        population_projetee = formule_malthus(9967, 0.037, 20)
        console.print(f"✅ [green]Formule Malthus: {population_projetee:.0f} habitants[/green]")
        
        # Test calcul besoin domestique
        besoin_dom = calculer_besoin_domestique(20847, 60)
        console.print(f"✅ [green]Besoin domestique: {besoin_dom:.1f} m³/jour[/green]")
        
        # Test calcul besoin annexe
        besoin_annexe = calculer_besoin_annexe(besoin_dom, 0.10)
        console.print(f"✅ [green]Besoin annexe: {besoin_annexe:.1f} m³/jour[/green]")
        
        # Test calcul besoin global
        besoin_global = calculer_besoin_global(besoin_dom, besoin_annexe)
        console.print(f"✅ [green]Besoin global: {besoin_global:.1f} m³/jour[/green]")
        
        # Test calcul besoin pointe
        besoin_pointe = calculer_besoin_pointe(besoin_global, 1.5)
        console.print(f"✅ [green]Besoin pointe: {besoin_pointe:.1f} m³/jour[/green]")
        
        # Test calcul besoin brut
        besoin_brut = calculer_besoin_brut(besoin_pointe, 0.95)
        console.print(f"✅ [green]Besoin brut: {besoin_brut:.1f} m³/jour[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Erreur lors du test des formules: {e}[/red]")
        return False

def test_constants():
    """Teste les constantes du module AEP"""
    console.print(Panel(
        "[bold blue]📏 TEST DES CONSTANTES AEP[/bold blue]",
        border_style="blue"
    ))
    
    try:
        # Test des constantes physiques
        console.print(f"✅ [green]Accélération pesanteur: {G} m/s²[/green]")
        console.print(f"✅ [green]Masse volumique eau: {RHO_EAU} kg/m³[/green]")
        
        # Test des coefficients de rugosité
        console.print(f"✅ [green]KS PVC: {KS_PVC}[/green]")
        console.print(f"✅ [green]KS Béton lissé: {KS_BETON_LISSE}[/green]")
        
        # Test des coefficients de pointe
        console.print(f"✅ [green]Coefficient pointe journalière: {COEFF_POINTE_JOURNALIERE}[/green]")
        
        # Test des rendements
        console.print(f"✅ [green]Rendement technique: {RENDEMENT_TECHNIQUE}[/green]")
        console.print(f"✅ [green]Rendement pompe: {RENDEMENT_POMPE}[/green]")
        
        # Test des vitesses
        console.print(f"✅ [green]Vitesse min: {VITESSE_MIN} m/s[/green]")
        console.print(f"✅ [green]Vitesse max: {VITESSE_MAX} m/s[/green]")
        
        # Test des dotations
        console.print(f"✅ [green]Dotation branchement privé: {DOTATIONS_EAU['branchement_prive']} L/j/hab[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Erreur lors du test des constantes: {e}[/red]")
        return False

def test_validation():
    """Teste les fonctions de validation"""
    console.print(Panel(
        "[bold blue]✅ TEST DES FONCTIONS DE VALIDATION[/bold blue]",
        border_style="blue"
    ))
    
    try:
        # Test validation données population
        donnees_pop = {
            "methode": "malthus",
            "annee_projet": 2045,
            "pop_annee_1": [9967, 2025],
            "pop_annee_2": [10340, 2026]
        }
        
        donnees_validees = validate_population_data(donnees_pop)
        console.print("✅ [green]Validation données population réussie[/green]")
        
        # Test validation données demande
        donnees_demande = {
            "population": 20847,
            "dotation_domestique_l_j_hab": 60,
            "rendement_reseau": 0.95
        }
        
        donnees_validees = validate_demand_data(donnees_demande)
        console.print("✅ [green]Validation données demande réussie[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Erreur lors du test de validation: {e}[/red]")
        return False

def test_cli_interface():
    """Teste l'interface CLI"""
    console.print(Panel(
        "[bold blue]🖥️ TEST DE L'INTERFACE CLI[/bold blue]",
        border_style="blue"
    ))
    
    try:
        from lcpi.aep.cli import app
        
        console.print("✅ [green]Interface CLI AEP chargée avec succès[/green]")
        
        # Test de l'aide
        from lcpi.aep.calculations.population import get_population_help
        from lcpi.aep.calculations.demand import get_demand_help
        
        help_pop = get_population_help()
        help_demande = get_demand_help()
        
        console.print("✅ [green]Fonctions d'aide disponibles[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Erreur lors du test CLI: {e}[/red]")
        return False

def test_templates():
    """Teste les templates YAML"""
    console.print(Panel(
        "[bold blue]📄 TEST DES TEMPLATES YAML[/bold blue]",
        border_style="blue"
    ))
    
    try:
        import yaml
        
        # Test template population
        template_pop_path = Path("src/lcpi/templates_project/aep/population_exemple.yml")
        if template_pop_path.exists():
            with open(template_pop_path, 'r', encoding='utf-8') as f:
                donnees_pop = yaml.safe_load(f)
            console.print("✅ [green]Template population chargé avec succès[/green]")
        else:
            console.print("⚠️ [yellow]Template population non trouvé[/yellow]")
        
        # Test template demande
        template_demande_path = Path("src/lcpi/templates_project/aep/demande_exemple.yml")
        if template_demande_path.exists():
            with open(template_demande_path, 'r', encoding='utf-8') as f:
                donnees_demande = yaml.safe_load(f)
            console.print("✅ [green]Template demande chargé avec succès[/green]")
        else:
            console.print("⚠️ [yellow]Template demande non trouvé[/yellow]")
        
        # Test template projet complet
        template_projet_path = Path("src/lcpi/templates_project/aep/projet_complet_exemple.yml")
        if template_projet_path.exists():
            with open(template_projet_path, 'r', encoding='utf-8') as f:
                donnees_projet = yaml.safe_load(f)
            console.print("✅ [green]Template projet complet chargé avec succès[/green]")
        else:
            console.print("⚠️ [yellow]Template projet complet non trouvé[/yellow]")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Erreur lors du test des templates: {e}[/red]")
        return False

def main():
    """Fonction principale de test"""
    console.print(Panel(
        "[bold blue]🚀 DÉMARRAGE DES TESTS DU MODULE AEP[/bold blue]\n\n"
        "Ce script teste toutes les fonctionnalités du module AEP\n"
        "en réutilisant les fonctions existantes d'hydrodrain.",
        border_style="blue"
    ))
    
    tests = [
        ("Imports", test_imports),
        ("Constantes", test_constants),
        ("Formules", test_formulas),
        ("Validation", test_validation),
        ("Calculs Population", test_population_calculations),
        ("Calculs Demande", test_demand_calculations),
        ("Interface CLI", test_cli_interface),
        ("Templates YAML", test_templates)
    ]
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        for test_name, test_func in tests:
            task = progress.add_task(f"Test {test_name}...", total=None)
            
            try:
                result = test_func()
                results.append((test_name, result))
                progress.update(task, description=f"✅ {test_name} terminé")
            except Exception as e:
                results.append((test_name, False))
                progress.update(task, description=f"❌ {test_name} échoué")
    
    # Affichage des résultats
    console.print("\n" + "="*60)
    console.print(Panel(
        "[bold blue]📊 RÉSULTATS DES TESTS[/bold blue]",
        border_style="blue"
    ))
    
    table = Table(title="Résultats des Tests AEP")
    table.add_column("Test", style="cyan")
    table.add_column("Statut", style="green")
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        table.add_row(test_name, status)
    
    console.print(table)
    
    # Résumé
    nb_reussis = sum(1 for _, result in results if result)
    nb_total = len(results)
    
    console.print(f"\n[bold]Résumé:[/bold] {nb_reussis}/{nb_total} tests réussis")
    
    if nb_reussis == nb_total:
        console.print(Panel(
            "[bold green]🎉 TOUS LES TESTS SONT RÉUSSIS ![/bold green]\n\n"
            "Le module AEP est prêt à être utilisé.",
            border_style="green"
        ))
    else:
        console.print(Panel(
            f"[bold red]⚠️ {nb_total - nb_reussis} TEST(S) ONT ÉCHOUÉ[/bold red]\n\n"
            "Vérifiez les erreurs ci-dessus.",
            border_style="red"
        ))

if __name__ == "__main__":
    main() 