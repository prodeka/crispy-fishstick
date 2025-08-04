"""
Interface CLI pour le module AEP (Alimentation en Eau Potable)
"""

import typer
from pathlib import Path
from typing import Optional
import json

from .calculations.population import get_population_help
from .calculations.demand import get_demand_help
from .calculations.network import get_network_help
from .calculations.reservoir import get_reservoir_help
from .calculations.pumping import get_pumping_help
from .calculations.protection import get_protection_help
from .calculations.hardy_cross import get_hardy_cross_help

# Imports pour les modules unifiés
from .calculations.population_unified import get_population_unified_help
from .calculations.demand_unified import get_demand_unified_help
from .calculations.network_unified import get_network_unified_help
from .calculations.reservoir_unified import get_reservoir_unified_help
from .calculations.pumping_unified import get_pumping_unified_help

app = typer.Typer(name="aep", help="Module Alimentation en Eau Potable")

# =============================================================================
# COMMANDES DE BASE
# =============================================================================

@app.command()
def population(
    fichier: str = typer.Argument(..., help="Fichier YAML/JSON avec les données de population"),
    methode: str = typer.Option("malthus", "--methode", "-m", help="Méthode de projection (malthus, arithmetique, geometrique, logistique)"),
    annee_finale: int = typer.Option(2050, "--annee", "-a", help="Année finale de projection"),
    afficher_comparaison: bool = typer.Option(False, "--comparaison", "-c", help="Afficher la comparaison des méthodes")
):
    """Calcul de projection de population pour AEP"""
    from .calculations.population import calculate_population_projection, compare_population_methods
    
    try:
        if afficher_comparaison:
            resultats = compare_population_methods(fichier, annee_finale)
            typer.echo("📊 Comparaison des méthodes de projection:")
            for methode, projection in resultats.items():
                typer.echo(f"  {methode}: {projection['population_finale']:.0f} habitants")
        else:
            resultat = calculate_population_projection(fichier, methode, annee_finale)
            typer.echo(f"📈 Projection {methode}: {resultat['population_finale']:.0f} habitants en {annee_finale}")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def demand(
    fichier: str = typer.Argument(..., help="Fichier YAML/JSON avec les données de demande"),
    type_calcul: str = typer.Option("global", "--type", "-t", help="Type de calcul (global, par_type, avance)"),
    afficher_details: bool = typer.Option(False, "--details", "-d", help="Afficher les détails par type d'usage")
):
    """Calcul de demande en eau pour AEP"""
    from .calculations.demand import calculate_water_demand, calculate_water_demand_by_type
    
    try:
        if type_calcul == "par_type" or afficher_details:
            resultats = calculate_water_demand_by_type(fichier)
            typer.echo("💧 Demande en eau par type d'usage:")
            for usage, demande in resultats.items():
                typer.echo(f"  {usage}: {demande:.2f} m³/jour")
        else:
            resultat = calculate_water_demand(fichier)
            typer.echo(f"💧 Demande totale: {resultat['demande_totale']:.2f} m³/jour")
            typer.echo(f"💧 Demande de pointe: {resultat['demande_pointe']:.2f} m³/jour")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def network(
    fichier: str = typer.Argument(..., help="Fichier YAML/JSON avec les données du réseau"),
    type_calcul: str = typer.Option("dimensionnement", "--type", "-t", help="Type de calcul (dimensionnement, verification, comparaison)"),
    formule: str = typer.Option("hazen_williams", "--formule", "-f", help="Formule de perte de charge (hazen_williams, manning, darcy_weisbach)")
):
    """Dimensionnement du réseau de distribution AEP"""
    from .calculations.network import dimension_network, compare_network_scenarios
    
    try:
        if type_calcul == "comparaison":
            resultats = compare_network_scenarios(fichier)
            typer.echo("🔧 Comparaison des scénarios de réseau:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: D={resultat['diametre']:.3f}m, V={resultat['vitesse']:.2f}m/s")
        else:
            resultat = dimension_network(fichier, formule)
            typer.echo(f"🔧 Dimensionnement réseau ({formule}):")
            typer.echo(f"  Diamètre: {resultat['diametre']:.3f} m")
            typer.echo(f"  Vitesse: {resultat['vitesse']:.2f} m/s")
            typer.echo(f"  Pertes de charge: {resultat['pertes_charge']:.2f} m")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def reservoir(
    fichier: str = typer.Argument(..., help="Fichier YAML/JSON avec les données du réservoir"),
    type_calcul: str = typer.Option("dimensionnement", "--type", "-t", help="Type de calcul (dimensionnement, verification, comparaison)"),
    forme: str = typer.Option("cylindrique", "--forme", "-f", help="Forme du réservoir (cylindrique, parallelepipedique)")
):
    """Dimensionnement du réservoir de stockage AEP"""
    from .calculations.reservoir import dimension_reservoir, compare_reservoir_scenarios
    
    try:
        if type_calcul == "comparaison":
            resultats = compare_reservoir_scenarios(fichier)
            typer.echo("🏗️ Comparaison des scénarios de réservoir:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: V={resultat['volume_total']:.1f}m³, H={resultat['hauteur']:.2f}m")
        else:
            resultat = dimension_reservoir(fichier, forme)
            typer.echo(f"🏗️ Dimensionnement réservoir ({forme}):")
            typer.echo(f"  Volume total: {resultat['volume_total']:.1f} m³")
            typer.echo(f"  Hauteur: {resultat['hauteur']:.2f} m")
            typer.echo(f"  Diamètre: {resultat.get('diametre', 'N/A')} m")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def pumping(
    fichier: str = typer.Argument(..., help="Fichier YAML/JSON avec les données de pompage"),
    type_calcul: str = typer.Option("dimensionnement", "--type", "-t", help="Type de calcul (dimensionnement, verification, comparaison)"),
    rendement: float = typer.Option(0.75, "--rendement", "-r", help="Rendement de la pompe (0-1)")
):
    """Dimensionnement des équipements de pompage AEP"""
    from .calculations.pumping import dimension_pumping, compare_pumping_scenarios
    
    try:
        if type_calcul == "comparaison":
            resultats = compare_pumping_scenarios(fichier)
            typer.echo("⚡ Comparaison des scénarios de pompage:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: P={resultat['puissance_electrique']:.1f}kW")
        else:
            resultat = dimension_pumping(fichier, rendement)
            typer.echo(f"⚡ Dimensionnement pompage (rendement {rendement*100:.0f}%):")
            typer.echo(f"  Puissance hydraulique: {resultat['puissance_hydraulique']:.1f} kW")
            typer.echo(f"  Puissance électrique: {resultat['puissance_electrique']:.1f} kW")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def protection(
    fichier: str = typer.Argument(..., help="Fichier YAML/JSON avec les données de protection"),
    type_calcul: str = typer.Option("coup_belier", "--type", "-t", help="Type de calcul (coup_belier, verification, comparaison)")
):
    """Calcul de protection contre le coup de bélier AEP"""
    from .calculations.protection import calculate_water_hammer_protection, compare_protection_scenarios
    
    try:
        if type_calcul == "comparaison":
            resultats = compare_protection_scenarios(fichier)
            typer.echo("🛡️ Comparaison des scénarios de protection:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: ΔP={resultat['variation_pression']:.1f}bar")
        else:
            resultat = calculate_water_hammer_protection(fichier)
            typer.echo("🛡️ Protection contre le coup de bélier:")
            typer.echo(f"  Célérité des ondes: {resultat['celerite']:.0f} m/s")
            typer.echo(f"  Variation de pression: {resultat['variation_pression']:.1f} bar")
            typer.echo(f"  Surpression maximale: {resultat['surpression_maximale']:.1f} bar")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def hardy_cross(
    fichier: str = typer.Argument(..., help="Fichier JSON/YAML avec les données du réseau maillé"),
    tolerance: float = typer.Option(1e-6, "--tolerance", "-t", help="Tolérance de convergence"),
    max_iterations: int = typer.Option(100, "--iterations", "-i", help="Nombre maximum d'itérations"),
    formule: str = typer.Option("hazen_williams", "--formule", "-f", help="Formule de perte de charge"),
    afficher_iterations: bool = typer.Option(False, "--iterations-detail", "-d", help="Afficher les détails de chaque itération"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Fichier de sortie pour exporter les résultats")
):
    """Calcul de distribution des débits par méthode Hardy-Cross"""
    from .calculations.hardy_cross import hardy_cross_network, load_hardy_cross_data, export_hardy_cross_results
    
    try:
        # Charger les données
        reseau = load_hardy_cross_data(fichier)
        
        # Effectuer le calcul
        resultats = hardy_cross_network(reseau, tolerance, max_iterations, formule, afficher_iterations)
        
        # Afficher les résultats
        typer.echo("🔄 Résultats Hardy-Cross:")
        typer.echo(f"  Convergence: {'✅' if resultats['convergence'] else '❌'}")
        typer.echo(f"  Itérations: {resultats['iterations']}")
        typer.echo(f"  Erreur finale: {resultats['erreur_finale']:.2e}")
        
        typer.echo("\n📊 Débits finaux par conduite:")
        for id_conduite, conduite in resultats['conduites_finales'].items():
            debit_ls = conduite['debit_Q'] * 1000  # Conversion en l/s
            typer.echo(f"  {id_conduite}: {debit_ls:.2f} l/s")
        
        # Exporter si demandé
        if export:
            export_hardy_cross_results(resultats, export, "json")
            typer.echo(f"\n💾 Résultats exportés vers: {export}")
            
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def project(
    fichier: str = typer.Argument(..., help="Fichier YAML/JSON avec les données du projet complet"),
    type_analyse: str = typer.Option("complet", "--type", "-t", help="Type d'analyse (complet, comparatif, validation)")
):
    """Analyse intégrée d'un projet AEP complet"""
    from .calculations.integration import integrated_aep_design, compare_aep_scenarios
    
    try:
        if type_analyse == "comparatif":
            resultats = compare_aep_scenarios(fichier)
            typer.echo("🏗️ Comparaison des scénarios de projet:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: Coût={resultat.get('cout_estime', 'N/A')}")
        else:
            resultat = integrated_aep_design(fichier)
            typer.echo("🏗️ Analyse intégrée du projet AEP:")
            typer.echo(f"  Population: {resultat['population']['population_finale']:.0f} habitants")
            typer.echo(f"  Demande: {resultat['demande']['demande_totale']:.1f} m³/jour")
            typer.echo(f"  Volume réservoir: {resultat['reservoir']['volume_total']:.1f} m³")
            typer.echo(f"  Puissance pompage: {resultat['pompage']['puissance_electrique']:.1f} kW")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

# =============================================================================
# COMMANDES UNIFIÉES (NOUVELLES)
# =============================================================================

@app.command()
def population_unified(
    population_base: int = typer.Argument(..., help="Population de base"),
    taux_croissance: float = typer.Option(0.037, "--taux", "-t", help="Taux de croissance annuel"),
    annees: int = typer.Option(20, "--annees", "-a", help="Nombre d'années de projection"),
    methode: str = typer.Option("malthus", "--methode", "-m", help="Méthode de projection"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """Projection démographique unifiée avec transparence mathématique"""
    from .calculations.population_unified import calculate_population_projection_unified
    
    try:
        # Créer le dictionnaire de données
        data = {
            "population_base": population_base,
            "taux_croissance": taux_croissance,
            "annees": annees,
            "methode": methode,
            "verbose": verbose
        }
        
        resultat = calculate_population_projection_unified(data)
        
        if resultat['statut'] == 'SUCCES':
            typer.echo(f"📈 Projection {methode}: {resultat['population_finale']:.0f} habitants")
            if verbose:
                typer.echo(f"   Croissance: {resultat.get('croissance_relative_pct', 0):.1f}%")
        else:
            typer.echo(f"❌ Erreur: {resultat['message']}")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def demand_unified(
    population: int = typer.Argument(..., help="Population"),
    dotation_l_hab_j: float = typer.Option(150, "--dotation", "-d", help="Dotation en L/hab/j"),
    coefficient_pointe: float = typer.Option(1.5, "--coeff-pointe", "-c", help="Coefficient de pointe"),
    type_consommation: str = typer.Option("branchement_prive", "--type", "-t", help="Type de consommation"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """Calcul de demande en eau unifié avec transparence mathématique"""
    from .calculations.demand_unified import calculate_water_demand_unified, calculate_water_demand_by_type_unified
    
    try:
        if type_consommation != "branchement_prive":
            data = {
                "population": population,
                "type_consommation": type_consommation
            }
            resultat = calculate_water_demand_by_type_unified(data)
        else:
            # Créer le dictionnaire de données
            data = {
                "population": population,
                "dotation_l_j_hab": dotation_l_hab_j,
                "coefficient_pointe": coefficient_pointe,
                "verbose": verbose
            }
            resultat = calculate_water_demand_unified(data)
        
        if resultat['statut'] == 'SUCCES':
            typer.echo(f"💧 Demande en eau ({type_consommation}):")
            if 'besoin_brut_m3j' in resultat:
                typer.echo(f"   Besoin brut: {resultat['besoin_brut_m3j']:.1f} m³/j")
            if 'debit_pointe_m3s' in resultat:
                typer.echo(f"   Débit pointe: {resultat['debit_pointe_m3s']:.3f} m³/s")
            typer.echo(f"   Méthode: {resultat.get('methode', 'N/A')}")
        else:
            typer.echo(f"❌ Erreur: {resultat['message']}")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def network_unified(
    debit_m3s: float = typer.Argument(..., help="Débit en m³/s"),
    longueur_m: float = typer.Option(1000, "--longueur", "-l", help="Longueur en mètres"),
    materiau: str = typer.Option("fonte", "--materiau", "-m", help="Matériau de la conduite"),
    perte_charge_max_m: float = typer.Option(10.0, "--perte-max", "-p", help="Perte de charge maximale en m"),
    methode: str = typer.Option("darcy", "--methode", "-M", help="Méthode de calcul"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """Dimensionnement réseau unifié avec transparence mathématique"""
    from .calculations.network_unified import dimension_network_unified
    
    try:
        # Créer le dictionnaire de données
        data = {
            "debit_m3s": debit_m3s,
            "longueur_m": longueur_m,
            "materiau": materiau,
            "perte_charge_max_m": perte_charge_max_m,
            "methode": methode
        }
        
        resultat = dimension_network_unified(data, verbose)
        
        if resultat['statut'] == 'SUCCES':
            reseau = resultat['reseau']
            typer.echo(f"🔧 Dimensionnement réseau ({methode}):")
            typer.echo(f"   Diamètre optimal: {reseau['diametre_optimal_mm']} mm")
            typer.echo(f"   Vitesse: {reseau['vitesse_ms']:.2f} m/s")
            typer.echo(f"   Perte de charge: {reseau['perte_charge_m']:.2f} m")
            if verbose:
                typer.echo(f"   Formule utilisée: {reseau.get('formule_utilisee', 'N/A')}")
        else:
            typer.echo(f"❌ Erreur: {resultat['message']}")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def reservoir_unified(
    volume_journalier_m3: float = typer.Argument(..., help="Volume journalier en m³"),
    type_adduction: str = typer.Option("continue", "--adduction", "-a", help="Type d'adduction"),
    forme_reservoir: str = typer.Option("cylindrique", "--forme", "-f", help="Forme du réservoir"),
    type_zone: str = typer.Option("ville_francaise_peu_importante", "--zone", "-z", help="Type de zone"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """Dimensionnement réservoir unifié avec transparence mathématique"""
    from .calculations.reservoir_unified import dimension_reservoir_unified
    
    try:
        # Créer le dictionnaire de données
        data = {
            "volume_journalier_m3": volume_journalier_m3,
            "type_adduction": type_adduction,
            "forme_reservoir": forme_reservoir,
            "type_zone": type_zone
        }
        
        resultat = dimension_reservoir_unified(data, verbose)
        
        if resultat['statut'] == 'SUCCES':
            reservoir = resultat['reservoir']
            typer.echo(f"🏗️ Dimensionnement réservoir ({forme_reservoir}):")
            typer.echo(f"   Volume utile: {reservoir['volume_utile_m3']:.1f} m³")
            typer.echo(f"   Capacité pratique: {reservoir['capacite_pratique_m3']:.1f} m³")
            if 'hauteur_m' in reservoir:
                typer.echo(f"   Hauteur: {reservoir['hauteur_m']:.2f} m")
            if 'diametre_m' in reservoir:
                typer.echo(f"   Diamètre: {reservoir['diametre_m']:.2f} m")
        else:
            typer.echo(f"❌ Erreur: {resultat['message']}")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def pumping_unified(
    debit_m3h: float = typer.Argument(..., help="Débit en m³/h"),
    hmt_m: float = typer.Option(50, "--hmt", "-h", help="Hauteur manométrique totale en m"),
    type_pompe: str = typer.Option("centrifuge", "--type", "-t", help="Type de pompe"),
    rendement_pompe: float = typer.Option(0.75, "--rendement", "-r", help="Rendement de la pompe"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """Dimensionnement pompage unifié avec transparence mathématique"""
    from .calculations.pumping_unified import dimension_pumping_unified
    
    try:
        # Créer le dictionnaire de données
        data = {
            "debit_m3h": debit_m3h,
            "hmt_m": hmt_m,
            "type_pompe": type_pompe,
            "rendement_pompe": rendement_pompe
        }
        
        resultat = dimension_pumping_unified(data, verbose)
        
        if resultat['statut'] == 'SUCCES':
            pompage = resultat['pompage']
            typer.echo(f"⚡ Dimensionnement pompage ({type_pompe}):")
            typer.echo(f"   Puissance hydraulique: {pompage['puissance_hydraulique_kw']:.1f} kW")
            typer.echo(f"   Puissance électrique: {pompage['puissance_electrique_kw']:.1f} kW")
            typer.echo(f"   Puissance groupe: {pompage['puissance_groupe_kva']:.1f} kVA")
            if verbose:
                typer.echo(f"   Énergie journalière: {pompage['energie_kwh']:.1f} kWh")
                typer.echo(f"   Coût journalier: {pompage['cout_euros']:.2f} €")
        else:
            typer.echo(f"❌ Erreur: {resultat['message']}")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def query(
    query_type: str = typer.Argument(..., help="Type de requête (coefficients, materials, formulas, constants, search)"),
    search_term: str = typer.Option("", "--search", "-s", help="Terme de recherche"),
    material: str = typer.Option("", "--material", "-m", help="Matériau spécifique"),
    category: str = typer.Option("", "--category", "-c", help="Catégorie spécifique"),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, csv, markdown)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """Interroge la base de données AEP"""
    try:
        from ..db.aep_database_manager import query_aep_database, AEPDatabaseManager
        
        # Préparer les paramètres
        kwargs = {}
        if search_term:
            kwargs["search_term"] = search_term
        if material:
            kwargs["material"] = material
        if category:
            kwargs["category"] = category
        
        # Exécuter la requête
        results = query_aep_database(query_type, **kwargs)
        
        if verbose:
            typer.echo(f"🔍 Requête: {query_type}")
            typer.echo(f"📊 Résultats: {len(results)} trouvés")
        
        if results:
            # Exporter les résultats
            manager = AEPDatabaseManager()
            if output_format == "json":
                import json
                typer.echo(json.dumps(results, indent=2, ensure_ascii=False))
            elif output_format == "csv":
                csv_content = manager.export_results(results, "csv")
                typer.echo(csv_content)
            elif output_format == "markdown":
                md_content = manager.export_results(results, "markdown")
                typer.echo(md_content)
            else:
                typer.echo(f"❌ Format non supporté: {output_format}")
        else:
            typer.echo(f"❌ Aucun résultat trouvé pour la requête: {query_type}")
            
    except Exception as e:
        typer.echo(f"❌ Erreur lors de la requête: {e}", err=True)

@app.command()
def autocomplete(
    query: str = typer.Argument(..., help="Requête pour l'auto-complétion"),
    limit: int = typer.Option(10, "--limit", "-l", help="Nombre maximum de suggestions")
):
    """Génère des suggestions d'auto-complétion"""
    try:
        from ..db.aep_database_manager import get_aep_autocomplete_options
        
        options = get_aep_autocomplete_options(query)
        
        if options:
            typer.echo(f"💡 Suggestions pour '{query}':")
            for i, option in enumerate(options[:limit], 1):
                typer.echo(f"   {i}. {option}")
        else:
            typer.echo(f"❌ Aucune suggestion trouvée pour '{query}'")
            
    except Exception as e:
        typer.echo(f"❌ Erreur lors de l'auto-complétion: {e}", err=True)

@app.command()
def search(
    term: str = typer.Argument(..., help="Terme de recherche"),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, csv, markdown)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """Recherche textuelle dans la base de données AEP"""
    try:
        from ..db.aep_database_manager import query_aep_database, AEPDatabaseManager
        
        # Recherche textuelle
        results = query_aep_database("search", search_term=term)
        
        if verbose:
            typer.echo(f"🔍 Recherche: {term}")
            typer.echo(f"📊 Résultats: {len(results)} trouvés")
        
        if results:
            # Exporter les résultats
            manager = AEPDatabaseManager()
            if output_format == "json":
                import json
                typer.echo(json.dumps(results, indent=2, ensure_ascii=False))
            elif output_format == "csv":
                csv_content = manager.export_results(results, "csv")
                typer.echo(csv_content)
            elif output_format == "markdown":
                md_content = manager.export_results(results, "markdown")
                typer.echo(md_content)
            else:
                typer.echo(f"❌ Format non supporté: {output_format}")
        else:
            typer.echo(f"❌ Aucun résultat trouvé pour: {term}")
            
    except Exception as e:
        typer.echo(f"❌ Erreur lors de la recherche: {e}", err=True)

@app.command()
def hardy_cross_csv(
    csv_path: str = typer.Argument(..., help="Chemin vers le fichier CSV"),
    max_iterations: int = typer.Option(100, "--max-iterations", "-i", help="Nombre maximum d'itérations"),
    tolerance: float = typer.Option(1e-6, "--tolerance", "-t", help="Tolérance de convergence"),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, markdown, csv)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """Exécute l'analyse Hardy-Cross depuis un fichier CSV"""
    try:
        from .calculations.hardy_cross_interface import hardy_cross_from_csv
        
        results = hardy_cross_from_csv(csv_path, max_iterations, tolerance)
        
        if verbose:
            typer.echo(f"🔍 Analyse Hardy-Cross: {csv_path}")
            typer.echo(f"📊 Itérations max: {max_iterations}")
            typer.echo(f"📊 Tolérance: {tolerance}")
        
        if results["status"] == "success":
            if output_format == "json":
                import json
                typer.echo(json.dumps(results, indent=2, ensure_ascii=False))
            elif output_format == "markdown":
                typer.echo("# Résultats Hardy-Cross")
                typer.echo(f"**Fichier:** {csv_path}")
                typer.echo(f"**Statut:** ✅ Succès")
                if "results" in results:
                    typer.echo(f"**Itérations:** {results['results'].get('iterations', 'N/A')}")
            else:
                typer.echo(f"❌ Format non supporté: {output_format}")
        else:
            typer.echo(f"❌ Erreur: {results.get('error', 'Erreur inconnue')}")
            
    except Exception as e:
        typer.echo(f"❌ Erreur lors de l'analyse Hardy-Cross: {e}", err=True)

@app.command()
def hardy_cross_yaml(
    yaml_path: str = typer.Argument(..., help="Chemin vers le fichier YAML"),
    max_iterations: int = typer.Option(100, "--max-iterations", "-i", help="Nombre maximum d'itérations"),
    tolerance: float = typer.Option(1e-6, "--tolerance", "-t", help="Tolérance de convergence"),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, markdown, csv)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """Exécute l'analyse Hardy-Cross depuis un fichier YAML"""
    try:
        from .calculations.hardy_cross_interface import hardy_cross_from_yaml
        
        results = hardy_cross_from_yaml(yaml_path, max_iterations, tolerance)
        
        if verbose:
            typer.echo(f"🔍 Analyse Hardy-Cross: {yaml_path}")
            typer.echo(f"📊 Itérations max: {max_iterations}")
            typer.echo(f"📊 Tolérance: {tolerance}")
        
        if results["status"] == "success":
            if output_format == "json":
                import json
                typer.echo(json.dumps(results, indent=2, ensure_ascii=False))
            elif output_format == "markdown":
                typer.echo("# Résultats Hardy-Cross")
                typer.echo(f"**Fichier:** {yaml_path}")
                typer.echo(f"**Statut:** ✅ Succès")
                if "results" in results:
                    typer.echo(f"**Itérations:** {results['results'].get('iterations', 'N/A')}")
            else:
                typer.echo(f"❌ Format non supporté: {output_format}")
        else:
            typer.echo(f"❌ Erreur: {results.get('error', 'Erreur inconnue')}")
            
    except Exception as e:
        typer.echo(f"❌ Erreur lors de l'analyse Hardy-Cross: {e}", err=True)

@app.command()
def hardy_cross_help():
    """Affiche l'aide pour la méthode Hardy-Cross"""
    try:
        from .calculations.hardy_cross_interface import get_hardy_cross_help
        
        help_text = get_hardy_cross_help()
        typer.echo(help_text)
        
    except Exception as e:
        typer.echo(f"❌ Erreur lors de l'affichage de l'aide: {e}", err=True)

# =============================================================================
# COMMANDES D'AIDE
# =============================================================================

@app.command()
def help_population():
    """Affiche l'aide pour les calculs de population"""
    typer.echo(get_population_help())

@app.command()
def help_demand():
    """Affiche l'aide pour les calculs de demande"""
    typer.echo(get_demand_help())

@app.command()
def help_network():
    """Affiche l'aide pour les calculs de réseau"""
    typer.echo(get_network_help())

@app.command()
def help_reservoir():
    """Affiche l'aide pour les calculs de réservoir"""
    typer.echo(get_reservoir_help())

@app.command()
def help_pumping():
    """Affiche l'aide pour les calculs de pompage"""
    typer.echo(get_pumping_help())

@app.command()
def help_protection():
    """Affiche l'aide pour les calculs de protection"""
    typer.echo(get_protection_help())

@app.command()
def help_hardy_cross():
    """Affiche l'aide pour les calculs Hardy-Cross"""
    typer.echo(get_hardy_cross_help())

# Commandes d'aide pour les modules unifiés
@app.command()
def help_population_unified():
    """Affiche l'aide pour les calculs de population unifiés"""
    typer.echo(get_population_unified_help())

@app.command()
def help_demand_unified():
    """Affiche l'aide pour les calculs de demande unifiés"""
    typer.echo(get_demand_unified_help())

@app.command()
def help_network_unified():
    """Affiche l'aide pour les calculs de réseau unifiés"""
    typer.echo(get_network_unified_help())

@app.command()
def help_reservoir_unified():
    """Affiche l'aide pour les calculs de réservoir unifiés"""
    typer.echo(get_reservoir_unified_help())

@app.command()
def help_pumping_unified():
    """Affiche l'aide pour les calculs de pompage unifiés"""
    typer.echo(get_pumping_unified_help())

@app.command()
def aep_help():
    """Affiche l'aide générale du module AEP"""
    typer.echo("""
🔵 MODULE AEP (ALIMENTATION EN EAU POTABLE)

📋 COMMANDES DISPONIBLES:

🔢 CALCULS DE BASE:
  population <fichier> - Projection démographique
  demand <fichier> - Calcul de demande en eau
  network <fichier> - Dimensionnement réseau
  reservoir <fichier> - Dimensionnement réservoir
  pumping <fichier> - Dimensionnement pompage
  protection <fichier> - Protection anti-bélier
  hardy-cross <fichier> - Calcul Hardy-Cross
  project <fichier> - Analyse complète de projet

🔧 CALCULS UNIFIÉS (NOUVEAU):
  population-unified <pop> - Projection démographique unifiée
  demand-unified <pop> - Calcul demande unifié
  network-unified <debit> - Dimensionnement réseau unifié
  reservoir-unified <volume> - Dimensionnement réservoir unifié
  pumping-unified <debit> - Dimensionnement pompage unifié

❓ AIDE:
  help-population - Aide population
  help-demand - Aide demande
  help-network - Aide réseau
  help-reservoir - Aide réservoir
  help-pumping - Aide pompage
  help-protection - Aide protection
  help-hardy-cross - Aide Hardy-Cross
  help-population-unified - Aide population unifié
  help-demand-unified - Aide demande unifié
  help-network-unified - Aide réseau unifié
  help-reservoir-unified - Aide réservoir unifié
  help-pumping-unified - Aide pompage unifié

📝 EXEMPLES:
  lcpi aep population-unified 1000 --taux 0.037 --annees 20
  lcpi aep demand-unified 1000 --dotation 150 --coeff-pointe 1.5
  lcpi aep network-unified 0.1 --longueur 1000 --materiau fonte
  lcpi aep reservoir-unified 1000 --adduction continue --forme cylindrique
  lcpi aep pumping-unified 100 --hmt 50 --type centrifuge
""")

if __name__ == "__main__":
    app() 