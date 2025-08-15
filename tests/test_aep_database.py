#!/usr/bin/env python3
"""
Script de test pour la base de données AEP

Ce script teste la base de données AEP et ses fonctionnalités
de requêtage et d'utilisation par le programme.
"""

import sys
import os
import json
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def test_database_loading():
    """Teste le chargement de la base de données AEP"""
    console.print(Panel(
        "[bold blue]🗄️ TEST DU CHARGEMENT DE LA BASE DE DONNÉES AEP[/bold blue]",
        border_style="blue"
    ))
    
    try:
        # Charger la base de données
        db_path = Path("src/lcpi/db/aep_database.json")
        if not db_path.exists():
            console.print("❌ [red]Base de données AEP non trouvée[/red]")
            return False
        
        with open(db_path, 'r', encoding='utf-8') as f:
            db_data = json.load(f)
        
        console.print("✅ [green]Base de données AEP chargée avec succès[/green]")
        
        # Vérifier la structure
        required_sections = ["metadata", "population", "demande_eau", "reseau", "reservoir", "pompage", "protection", "traitement"]
        for section in required_sections:
            if section in db_data:
                console.print(f"✅ [green]Section '{section}' présente[/green]")
            else:
                console.print(f"❌ [red]Section '{section}' manquante[/red]")
                return False
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Erreur lors du chargement: {e}[/red]")
        return False

def test_database_queries():
    """Teste les requêtes sur la base de données AEP"""
    console.print(Panel(
        "[bold blue]🔍 TEST DES REQUÊTES SUR LA BASE DE DONNÉES[/bold blue]",
        border_style="blue"
    ))
    
    try:
        # Charger la base de données
        db_path = Path("src/lcpi/db/aep_database.json")
        with open(db_path, 'r', encoding='utf-8') as f:
            db_data = json.load(f)
        
        # Test 1: Récupération des données de population
        population_data = db_data.get("population", {})
        if "fidokpui_2024" in population_data:
            console.print(f"✅ [green]Population 2024: {population_data['fidokpui_2024']:,} habitants[/green]")
        
        # Test 2: Récupération des dotations
        demande_data = db_data.get("demande_eau", {})
        if "dotation_bp" in demande_data:
            console.print(f"✅ [green]Dotation BP: {demande_data['dotation_bp']} L/j/hab[/green]")
        
        # Test 3: Récupération des diamètres commerciaux
        reseau_data = db_data.get("reseau", {})
        if "diametres_pvc" in reseau_data:
            diametres = reseau_data["diametres_pvc"]
            console.print(f"✅ [green]Diamètres PVC disponibles: {len(diametres)} tailles[/green]")
        
        # Test 4: Récupération des données de protection
        protection_data = db_data.get("protection", {})
        if "k_pvc" in protection_data:
            console.print(f"✅ [green]Coefficient K PVC: {protection_data['k_pvc']}[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Erreur lors des requêtes: {e}[/red]")
        return False

def test_database_integration():
    """Teste l'intégration de la base de données avec les calculs AEP"""
    console.print(Panel(
        "[bold blue]🔗 TEST DE L'INTÉGRATION AVEC LES CALCULS AEP[/bold blue]",
        border_style="blue"
    ))
    
    try:
        # Charger la base de données
        db_path = Path("src/lcpi/db/aep_database.json")
        with open(db_path, 'r', encoding='utf-8') as f:
            db_data = json.load(f)
        
        # Test avec les données de la base
        population_base = db_data["population"]["fidokpui_2024"]
        taux_croissance = db_data["population"]["taux_croissance"]
        dotation = db_data["demande_eau"]["dotation_bp"]
        coefficient_pointe = db_data["demande_eau"]["coefficient_pointe_j"]
        
        # Import des fonctions AEP
        from lcpi.aep.calculations.population import calculate_population_projection
        from lcpi.aep.calculations.demand import calculate_water_demand
        
        # Test projection démographique
        resultat_pop = calculate_population_projection(
            population_base=population_base,
            taux_croissance=taux_croissance,
            annees=20,
            verbose=False
        )
        
        if resultat_pop["statut"] == "SUCCES":
            population_projetee = resultat_pop["population_projetee"]
            console.print(f"✅ [green]Projection avec données DB: {population_projetee:,.0f} habitants[/green]")
        
        # Test calcul demande
        resultat_demande = calculate_water_demand(
            population=population_projetee,
            dotation_l_j_hab=dotation,
            coefficient_pointe=coefficient_pointe,
            verbose=False
        )
        
        if resultat_demande["statut"] == "SUCCES":
            besoin_brut = resultat_demande["besoins_calcules"]["besoin_brut_m3_jour"]
            console.print(f"✅ [green]Demande avec données DB: {besoin_brut:.1f} m³/jour[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Erreur lors de l'intégration: {e}[/red]")
        return False

def test_database_search():
    """Teste la recherche dans la base de données AEP"""
    console.print(Panel(
        "[bold blue]🔎 TEST DE LA RECHERCHE DANS LA BASE DE DONNÉES[/bold blue]",
        border_style="blue"
    ))
    
    try:
        # Charger la base de données
        db_path = Path("src/lcpi/db/aep_database.json")
        with open(db_path, 'r', encoding='utf-8') as f:
            db_data = json.load(f)
        
        def search_in_data(data, keywords):
            """Recherche récursive dans les données"""
            results = []
            
            def search_recursive(obj, path=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        current_path = f"{path}.{key}" if path else key
                        search_recursive(value, current_path)
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        current_path = f"{path}[{i}]"
                        search_recursive(item, current_path)
                else:
                    # Recherche dans les valeurs
                    if any(keyword.lower() in str(obj).lower() for keyword in keywords):
                        results.append({
                            "path": path,
                            "value": obj
                        })
            
            search_recursive(data)
            return results
        
        # Test de recherche
        keywords = ["population", "60"]
        results = search_in_data(db_data, keywords)
        
        console.print(f"✅ [green]Recherche trouvée: {len(results)} résultats[/green]")
        for result in results[:3]:  # Afficher les 3 premiers résultats
            console.print(f"   • {result['path']}: {result['value']}")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Erreur lors de la recherche: {e}[/red]")
        return False

def test_database_export():
    """Teste l'export de données de la base AEP"""
    console.print(Panel(
        "[bold blue]📤 TEST DE L'EXPORT DE DONNÉES[/bold blue]",
        border_style="blue"
    ))
    
    try:
        # Charger la base de données
        db_path = Path("src/lcpi/db/aep_database.json")
        with open(db_path, 'r', encoding='utf-8') as f:
            db_data = json.load(f)
        
        # Export en CSV (simulation)
        import csv
        
        # Créer un fichier CSV temporaire avec les données de population
        csv_path = "temp_population_aep.csv"
        population_data = db_data["population"]["projections"]
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Année", "Population"])
            for annee, population in population_data.items():
                writer.writerow([annee, population])
        
        console.print(f"✅ [green]Export CSV créé: {csv_path}[/green]")
        
        # Nettoyer le fichier temporaire
        os.remove(csv_path)
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Erreur lors de l'export: {e}[/red]")
        return False

def main():
    """Fonction principale de test"""
    console.print(Panel(
        "[bold blue]🚀 DÉMARRAGE DES TESTS DE LA BASE DE DONNÉES AEP[/bold blue]\n\n"
        "Ce script teste la base de données AEP et ses fonctionnalités\n"
        "de requêtage, intégration et export.",
        border_style="blue"
    ))
    
    tests = [
        ("Chargement DB", test_database_loading),
        ("Requêtes DB", test_database_queries),
        ("Intégration DB", test_database_integration),
        ("Recherche DB", test_database_search),
        ("Export DB", test_database_export)
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
        "[bold blue]📊 RÉSULTATS DES TESTS BASE DE DONNÉES AEP[/bold blue]",
        border_style="blue"
    ))
    
    table = Table(title="Résultats des Tests Base de Données AEP")
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
            "La base de données AEP est prête à être utilisée.",
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