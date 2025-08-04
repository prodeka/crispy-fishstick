#!/usr/bin/env python3
"""
Script de démonstration pour le module AEP (Alimentation en Eau Potable)

Ce script démontre l'utilisation du module AEP avec des exemples concrets
basés sur le document AEP Fidokpui-Dikame.
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text

console = Console()

def demo_population_projection():
    """Démonstration des calculs de projection démographique"""
    console.print(Panel(
        "[bold blue]📊 DÉMONSTRATION - PROJECTION DÉMOGRAPHIQUE[/bold blue]",
        border_style="blue"
    ))
    
    try:
        from lcpi.aep.calculations.population import calculate_population_projection
        
        # Données du document AEP
        population_base = 9967
        taux_croissance = 0.037  # 3.7%
        annees = 20
        
        console.print(f"[cyan]Données d'entrée:[/cyan]")
        console.print(f"• Population de base: {population_base:,} habitants")
        console.print(f"• Taux de croissance: {taux_croissance:.1%}")
        console.print(f"• Horizon de planification: {annees} années")
        
        # Calcul de la projection
        resultat = calculate_population_projection(
            population_base=population_base,
            taux_croissance=taux_croissance,
            annees=annees,
            verbose=True
        )
        
        if resultat.get("statut") == "SUCCES":
            console.print(f"\n[green]✅ Résultats:[/green]")
            console.print(f"• Population projetée: {resultat.get('population_projetee', 'N/A'):,} habitants")
            console.print(f"• Croissance absolue: +{resultat.get('croissance_absolue', 'N/A'):,} habitants")
            console.print(f"• Croissance relative: +{resultat.get('croissance_relative_pct', 'N/A')}%")
            console.print(f"• Méthode utilisée: {resultat.get('methode', 'N/A').title()}")
            
            return resultat.get('population_projetee')
        else:
            console.print(f"[red]❌ Erreur: {resultat.get('message', 'Erreur inconnue')}[/red]")
            return None
            
    except Exception as e:
        console.print(f"[red]❌ Erreur lors de la démonstration: {e}[/red]")
        return None

def demo_water_demand(population_projetee):
    """Démonstration des calculs de demande en eau"""
    console.print(Panel(
        "[bold blue]💧 DÉMONSTRATION - CALCUL DE DEMANDE EN EAU[/bold blue]",
        border_style="blue"
    ))
    
    try:
        from lcpi.aep.calculations.demand import calculate_water_demand
        
        # Données du document AEP
        dotation = 60  # L/j/hab
        coefficient_pointe = 1.5
        
        console.print(f"[cyan]Données d'entrée:[/cyan]")
        console.print(f"• Population: {population_projetee:,} habitants")
        console.print(f"• Dotation: {dotation} L/j/hab")
        console.print(f"• Coefficient de pointe: {coefficient_pointe}")
        
        # Calcul de la demande
        resultat = calculate_water_demand(
            population=population_projetee,
            dotation_l_j_hab=dotation,
            coefficient_pointe=coefficient_pointe,
            verbose=True
        )
        
        if resultat.get("statut") == "SUCCES":
            besoins = resultat.get("besoins_calcules", {})
            debits = resultat.get("debits_calcules", {})
            
            console.print(f"\n[green]✅ Résultats des besoins:[/green]")
            console.print(f"• Besoin domestique: {besoins.get('besoin_domestique_m3_jour', 'N/A'):.1f} m³/jour")
            console.print(f"• Besoin annexe: {besoins.get('besoin_annexe_m3_jour', 'N/A'):.1f} m³/jour")
            console.print(f"• Besoin global: {besoins.get('besoin_global_m3_jour', 'N/A'):.1f} m³/jour")
            console.print(f"• Besoin pointe: {besoins.get('besoin_pointe_m3_jour', 'N/A'):.1f} m³/jour")
            console.print(f"• Besoin brut: {besoins.get('besoin_brut_m3_jour', 'N/A'):.1f} m³/jour")
            
            console.print(f"\n[green]✅ Résultats des débits:[/green]")
            console.print(f"• Débit moyen horaire: {debits.get('debit_moyen_horaire_m3_h', 'N/A'):.1f} m³/h")
            console.print(f"• Coefficient pointe horaire: {debits.get('coefficient_pointe_horaire', 'N/A'):.2f}")
            console.print(f"• Débit pointe horaire: {debits.get('debit_pointe_horaire_m3_h', 'N/A'):.1f} m³/h")
            
            return besoins.get('besoin_brut_m3_jour')
        else:
            console.print(f"[red]❌ Erreur: {resultat.get('message', 'Erreur inconnue')}[/red]")
            return None
            
    except Exception as e:
        console.print(f"[red]❌ Erreur lors de la démonstration: {e}[/red]")
        return None

def demo_formulas():
    """Démonstration des formules mathématiques"""
    console.print(Panel(
        "[bold blue]🧮 DÉMONSTRATION - FORMULES MATHÉMATIQUES[/bold blue]",
        border_style="blue"
    ))
    
    try:
        from lcpi.aep.core.formulas import *
        
        # Test des différentes formules
        table = Table(title="Résultats des Formules AEP")
        table.add_column("Formule", style="cyan")
        table.add_column("Valeur", style="green")
        table.add_column("Unité", style="yellow")
        
        # Formule de Malthus
        pop_malthus = formule_malthus(9967, 0.037, 20)
        table.add_row("Malthus (Population)", f"{pop_malthus:.0f}", "habitants")
        
        # Calculs de besoins
        besoin_dom = calculer_besoin_domestique(20847, 60)
        table.add_row("Besoin domestique", f"{besoin_dom:.1f}", "m³/jour")
        
        besoin_annexe = calculer_besoin_annexe(besoin_dom, 0.10)
        table.add_row("Besoin annexe", f"{besoin_annexe:.1f}", "m³/jour")
        
        besoin_global = calculer_besoin_global(besoin_dom, besoin_annexe)
        table.add_row("Besoin global", f"{besoin_global:.1f}", "m³/jour")
        
        besoin_pointe = calculer_besoin_pointe(besoin_global, 1.5)
        table.add_row("Besoin pointe", f"{besoin_pointe:.1f}", "m³/jour")
        
        besoin_brut = calculer_besoin_brut(besoin_pointe, 0.95)
        table.add_row("Besoin brut", f"{besoin_brut:.1f}", "m³/jour")
        
        # Coefficient de pointe horaire
        debit_moyen_h = besoin_brut / 24
        coeff_pointe_h = calculer_coefficient_pointe_horaire(debit_moyen_h)
        table.add_row("Coeff. pointe horaire", f"{coeff_pointe_h:.2f}", "")
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]❌ Erreur lors de la démonstration: {e}[/red]")

def demo_constants():
    """Démonstration des constantes AEP"""
    console.print(Panel(
        "[bold blue]📏 DÉMONSTRATION - CONSTANTES AEP[/bold blue]",
        border_style="blue"
    ))
    
    try:
        from lcpi.aep.core.constants import *
        
        # Constantes physiques
        console.print("[cyan]Constantes physiques:[/cyan]")
        console.print(f"• Accélération pesanteur: {G} m/s²")
        console.print(f"• Masse volumique eau: {RHO_EAU} kg/m³")
        console.print(f"• Module élasticité eau: {EPSILON_EAU/1e9:.1f} GPa")
        
        # Coefficients de rugosité
        console.print(f"\n[cyan]Coefficients de rugosité (Strickler):[/cyan]")
        console.print(f"• PVC: {KS_PVC}")
        console.print(f"• Béton lissé: {KS_BETON_LISSE}")
        console.print(f"• Béton brut: {KS_BETON_BRUT}")
        console.print(f"• Acier galvanisé: {KS_ACIER_GALVANISE}")
        console.print(f"• Fonte: {KS_FONTE}")
        
        # Coefficients de pointe
        console.print(f"\n[cyan]Coefficients de pointe:[/cyan]")
        console.print(f"• Journalière: {COEFF_POINTE_JOURNALIERE}")
        
        # Rendements
        console.print(f"\n[cyan]Rendements techniques:[/cyan]")
        console.print(f"• Réseau: {RENDEMENT_TECHNIQUE*100:.0f}%")
        console.print(f"• Pompe: {RENDEMENT_POMPE*100:.0f}%")
        console.print(f"• Moteur: {RENDEMENT_MOTEUR*100:.0f}%")
        
        # Vitesses et pressions
        console.print(f"\n[cyan]Vitesses et pressions:[/cyan]")
        console.print(f"• Vitesse min: {VITESSE_MIN} m/s")
        console.print(f"• Vitesse max: {VITESSE_MAX} m/s")
        console.print(f"• Pression service min: {PRESSION_SERVICE_MIN} mCE")
        
        # Dotations
        console.print(f"\n[cyan]Dotations en eau:[/cyan]")
        for type_cons, dotation in DOTATIONS_EAU.items():
            console.print(f"• {type_cons.replace('_', ' ').title()}: {dotation} L/j/hab")
        
    except Exception as e:
        console.print(f"[red]❌ Erreur lors de la démonstration: {e}[/red]")

def demo_cli_usage():
    """Démonstration de l'utilisation CLI"""
    console.print(Panel(
        "[bold blue]🖥️ DÉMONSTRATION - UTILISATION CLI[/bold blue]",
        border_style="blue"
    ))
    
    console.print("[cyan]Commandes CLI disponibles:[/cyan]")
    
    commands = [
        ("lcpi aep help", "Affiche l'aide générale du module AEP"),
        ("lcpi aep population --base 9967 --rate 0.037 --years 20", "Calcul de projection démographique"),
        ("lcpi aep demand --population 20847 --dotation 60 --coeff-pointe 1.5", "Calcul de demande en eau"),
        ("lcpi aep population --file population_exemple.yml", "Calcul avec fichier YAML"),
        ("lcpi aep demand --file demande_exemple.yml", "Calcul avec fichier YAML")
    ]
    
    table = Table(title="Exemples de Commandes CLI")
    table.add_column("Commande", style="cyan")
    table.add_column("Description", style="green")
    
    for cmd, desc in commands:
        table.add_row(cmd, desc)
    
    console.print(table)
    
    console.print(f"\n[cyan]Utilisation dans le REPL:[/cyan]")
    console.print("```python")
    console.print(">>> from lcpi.aep.calculations import population, demand")
    console.print(">>> result = population.calculate_population_projection(9967, 0.037, 20)")
    console.print(">>> result = demand.calculate_water_demand(20847, 60, 1.5)")
    console.print("```")

def demo_templates():
    """Démonstration des templates YAML"""
    console.print(Panel(
        "[bold blue]📄 DÉMONSTRATION - TEMPLATES YAML[/bold blue]",
        border_style="blue"
    ))
    
    try:
        import yaml
        
        # Liste des templates disponibles
        templates = [
            ("population_exemple.yml", "Projection démographique"),
            ("demande_exemple.yml", "Calcul de demande en eau"),
            ("projet_complet_exemple.yml", "Projet AEP complet")
        ]
        
        console.print("[cyan]Templates disponibles:[/cyan]")
        for filename, description in templates:
            template_path = Path(f"src/lcpi/templates_project/aep/{filename}")
            if template_path.exists():
                console.print(f"✅ {filename} - {description}")
            else:
                console.print(f"⚠️ {filename} - {description} (non trouvé)")
        
        # Exemple de chargement d'un template
        template_path = Path("src/lcpi/templates_project/aep/population_exemple.yml")
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                donnees = yaml.safe_load(f)
            
            console.print(f"\n[cyan]Exemple de contenu du template population:[/cyan]")
            console.print(f"• Méthode: {donnees.get('methode', 'N/A')}")
            console.print(f"• Année projet: {donnees.get('annee_projet', 'N/A')}")
            console.print(f"• Population de base: {donnees.get('pop_annee_1', ['N/A', 'N/A'])[0]:,} habitants")
            console.print(f"• Projet: {donnees.get('projet', {}).get('nom', 'N/A')}")
        
    except Exception as e:
        console.print(f"[red]❌ Erreur lors de la démonstration: {e}[/red]")

def main():
    """Fonction principale de démonstration"""
    console.print(Panel(
        "[bold blue]🚀 DÉMONSTRATION DU MODULE AEP[/bold blue]\n\n"
        "Ce script démontre l'utilisation du module AEP\n"
        "avec des exemples concrets basés sur le document AEP Fidokpui-Dikame.",
        border_style="blue"
    ))
    
    # Démonstrations
    population_projetee = demo_population_projection()
    
    if population_projetee:
        besoin_brut = demo_water_demand(population_projetee)
    
    demo_formulas()
    demo_constants()
    demo_cli_usage()
    demo_templates()
    
    # Résumé
    console.print(Panel(
        "[bold green]🎉 DÉMONSTRATION TERMINÉE[/bold green]\n\n"
        "Le module AEP est maintenant opérationnel avec:\n"
        "• Projections démographiques (Malthus, arithmétique, géométrique, logistique)\n"
        "• Calculs de demande en eau (domestique, annexe, pointe)\n"
        "• Formules mathématiques complètes\n"
        "• Constantes techniques standardisées\n"
        "• Interface CLI intuitive\n"
        "• Templates YAML prêts à l'emploi\n\n"
        "Le module réutilise intelligemment les fonctions d'hydrodrain\n"
        "tout en ajoutant les fonctionnalités spécifiques à l'AEP.",
        border_style="green"
    ))

if __name__ == "__main__":
    main() 