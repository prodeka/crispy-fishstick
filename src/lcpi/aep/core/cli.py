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
    """📈 Calcul de projection démographique pour AEP
    
    Méthodes disponibles:
    - malthus: Croissance exponentielle
    - arithmetique: Croissance linéaire
    - geometrique: Croissance géométrique
    - logistique: Croissance logistique avec saturation
    
    Exemple: lcpi aep population population.yml --methode malthus --annee 2050
    """
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
    """💧 Calcul de demande en eau pour AEP
    
    Types de calcul:
    - global: Demande totale et de pointe
    - par_type: Détail par type d'usage (domestique, industriel, etc.)
    - avance: Calculs avancés avec coefficients saisonniers
    
    Exemple: lcpi aep demand demande.yml --type global --details
    """
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
    """🔧 Dimensionnement du réseau de distribution AEP
    
    Formules disponibles:
    - hazen_williams: Formule de Hazen-Williams (C)
    - manning: Formule de Manning (n)
    - darcy_weisbach: Formule de Darcy-Weisbach (λ)
    
    Exemple: lcpi aep network reseau.yml --formule hazen_williams
    """
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
    """🏗️ Dimensionnement du réservoir de stockage AEP
    
    Formes disponibles:
    - cylindrique: Réservoir cylindrique
    - parallelepipedique: Réservoir parallélépipédique
    
    Exemple: lcpi aep reservoir reservoir.yml --forme cylindrique
    """
    from .calculations.reservoir import dimension_reservoir, compare_reservoir_scenarios
    
    try:
        if type_calcul == "comparaison":
            resultats = compare_reservoir_scenarios(fichier)
            typer.echo("🏗️ Comparaison des scénarios de réservoir:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: V={resultat['volume']:.0f}m³, H={resultat['hauteur']:.2f}m")
        else:
            resultat = dimension_reservoir(fichier, forme)
            typer.echo(f"🏗️ Dimensionnement réservoir ({forme}):")
            typer.echo(f"  Volume: {resultat['volume']:.0f} m³")
            typer.echo(f"  Hauteur: {resultat['hauteur']:.2f} m")
            typer.echo(f"  Surface: {resultat['surface']:.2f} m²")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def pumping(
    fichier: str = typer.Argument(..., help="Fichier YAML/JSON avec les données de pompage"),
    type_calcul: str = typer.Option("dimensionnement", "--type", "-t", help="Type de calcul (dimensionnement, verification, comparaison)"),
    rendement: float = typer.Option(0.75, "--rendement", "-r", help="Rendement de la pompe (0-1)")
):
    """⚡ Dimensionnement des équipements de pompage AEP
    
    Types de pompes:
    - centrifuge: Pompe centrifuge
    - helice: Pompe à hélice
    - piston: Pompe à piston
    
    Exemple: lcpi aep pumping pompage.yml --rendement 0.80
    """
    from .calculations.pumping import dimension_pumping, compare_pumping_scenarios
    
    try:
        if type_calcul == "comparaison":
            resultats = compare_pumping_scenarios(fichier)
            typer.echo("⚡ Comparaison des scénarios de pompage:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: P={resultat['puissance']:.1f}kW, Q={resultat['debit']:.2f}m³/h")
        else:
            resultat = dimension_pumping(fichier, rendement)
            typer.echo(f"⚡ Dimensionnement pompage (η={rendement}):")
            typer.echo(f"  Puissance hydraulique: {resultat['puissance_hydraulique']:.1f} kW")
            typer.echo(f"  Puissance électrique: {resultat['puissance_electrique']:.1f} kW")
            typer.echo(f"  Débit: {resultat['debit']:.2f} m³/h")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def protection(
    fichier: str = typer.Argument(..., help="Fichier YAML/JSON avec les données de protection"),
    type_calcul: str = typer.Option("coup_belier", "--type", "-t", help="Type de calcul (coup_belier, verification, comparaison)")
):
    """🛡️ Calcul de protection contre le coup de bélier AEP
    
    Types de protection:
    - coup_belier: Calcul de la surpression
    - verification: Vérification des protections existantes
    - comparaison: Comparaison de solutions
    
    Exemple: lcpi aep protection protection.yml --type coup_belier
    """
    from .calculations.protection import calculate_protection, compare_protection_scenarios
    
    try:
        if type_calcul == "comparaison":
            resultats = compare_protection_scenarios(fichier)
            typer.echo("🛡️ Comparaison des scénarios de protection:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: ΔP={resultat['surpression']:.1f}m, τ={resultat['duree']:.2f}s")
        else:
            resultat = calculate_protection(fichier)
            typer.echo(f"🛡️ Protection contre le coup de bélier:")
            typer.echo(f"  Surpression: {resultat['surpression']:.1f} m")
            typer.echo(f"  Durée: {resultat['duree']:.2f} s")
            typer.echo(f"  Énergie: {resultat['energie']:.1f} kJ")
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
    """🔄 Calcul de distribution des débits par méthode Hardy-Cross
    
    Formules disponibles:
    - hazen_williams: Formule de Hazen-Williams (n=1.852)
    - manning: Formule de Manning (n=2.0)
    - darcy_weisbach: Formule de Darcy-Weisbach (n=2.0)
    
    Exemple: lcpi aep hardy-cross reseau.yml --tolerance 1e-6 --iterations 100
    """
    from .calculations.hardy_cross import hardy_cross_network
    
    try:
        resultat = hardy_cross_network(
            fichier, tolerance, max_iterations, formule, afficher_iterations
        )
        
        typer.echo(f"🔄 Hardy-Cross terminé:")
        typer.echo(f"  Itérations: {resultat['iterations']}")
        typer.echo(f"  Tolérance finale: {resultat['tolerance']:.2e}")
        typer.echo(f"  Temps: {resultat['temps']:.3f} s")
        
        if export:
            from .calculations.hardy_cross import export_hardy_cross_results
            export_hardy_cross_results(resultat, export, "json")
            typer.echo(f"✅ Résultats exportés: {export}")
            
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def project(
    fichier: str = typer.Argument(..., help="Fichier YAML/JSON avec les données du projet complet"),
    type_analyse: str = typer.Option("complet", "--type", "-t", help="Type d'analyse (complet, comparatif, validation)")
):
    """📋 Analyse intégrée d'un projet AEP complet
    
    Types d'analyse:
    - complet: Analyse complète du projet
    - comparatif: Comparaison de scénarios
    - validation: Validation des résultats
    
    Exemple: lcpi aep project projet.yml --type complet
    """
    from .calculations.project import analyze_project
    
    try:
        resultat = analyze_project(fichier, type_analyse)
        typer.echo(f"📋 Analyse projet ({type_analyse}):")
        typer.echo(f"  Population: {resultat['population']:.0f} habitants")
        typer.echo(f"  Demande: {resultat['demande']:.2f} m³/jour")
        typer.echo(f"  Coût estimé: {resultat['cout']:.0f} FCFA")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

# =============================================================================
# COMMANDES UNIFIÉES
# =============================================================================

@app.command()
def population_unified(
    population_base: int = typer.Argument(..., help="Population de base"),
    taux_croissance: float = typer.Option(0.037, "--taux", "-t", help="Taux de croissance annuel"),
    annees: int = typer.Option(20, "--annees", "-a", help="Nombre d'années de projection"),
    methode: str = typer.Option("malthus", "--methode", "-m", help="Méthode de projection"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """📈 Projection démographique unifiée avec transparence mathématique
    
    Méthodes disponibles:
    - malthus: Croissance exponentielle P(t) = P₀ × e^(rt)
    - arithmetique: Croissance linéaire P(t) = P₀ + rt
    - geometrique: Croissance géométrique P(t) = P₀ × (1+r)^t
    - logistique: Croissance logistique avec saturation
    
    Exemple: lcpi aep population-unified 1000 --taux 0.037 --annees 20
    """
    from .calculations.population_unified import calculate_population_projection
    
    try:
        resultat = calculate_population_projection(
            population_base, taux_croissance, annees, methode, verbose
        )
        
        if verbose:
            typer.echo(f"📈 Projection {methode}:")
            typer.echo(f"  Population initiale: {population_base}")
            typer.echo(f"  Population finale: {resultat['population_finale']:.0f}")
            typer.echo(f"  Taux de croissance: {taux_croissance:.3f}")
            typer.echo(f"  Période: {annees} années")
        else:
            typer.echo(f"📈 {resultat['population_finale']:.0f} habitants")
            
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
    """💧 Calcul de demande en eau unifié avec transparence mathématique
    
    Types de consommation:
    - branchement_prive: Branchement privé
    - borne_fontaine: Borne fontaine
    - industriel: Consommation industrielle
    
    Exemple: lcpi aep demand-unified 1000 --dotation 150 --coeff-pointe 1.5
    """
    from .calculations.demand_unified import calculate_water_demand
    
    try:
        resultat = calculate_water_demand(
            population, dotation_l_hab_j, coefficient_pointe, type_consommation, verbose
        )
        
        if verbose:
            typer.echo(f"💧 Demande en eau:")
            typer.echo(f"  Population: {population}")
            typer.echo(f"  Dotation: {dotation_l_hab_j} L/hab/j")
            typer.echo(f"  Demande moyenne: {resultat['demande_moyenne']:.2f} m³/jour")
            typer.echo(f"  Demande de pointe: {resultat['demande_pointe']:.2f} m³/jour")
        else:
            typer.echo(f"💧 {resultat['demande_pointe']:.2f} m³/jour")
            
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
    """🔧 Dimensionnement réseau unifié avec transparence mathématique
    
    Méthodes disponibles:
    - darcy: Formule de Darcy-Weisbach
    - hazen: Formule de Hazen-Williams
    - manning: Formule de Manning
    
    Exemple: lcpi aep network-unified 0.1 --longueur 1000 --materiau fonte
    """
    from .calculations.network_unified import dimension_network
    
    try:
        resultat = dimension_network(
            debit_m3s, longueur_m, materiau, perte_charge_max_m, methode, verbose
        )
        
        if verbose:
            typer.echo(f"🔧 Dimensionnement réseau:")
            typer.echo(f"  Débit: {debit_m3s} m³/s")
            typer.echo(f"  Diamètre: {resultat['diametre']:.3f} m")
            typer.echo(f"  Vitesse: {resultat['vitesse']:.2f} m/s")
            typer.echo(f"  Perte de charge: {resultat['perte_charge']:.2f} m")
        else:
            typer.echo(f"🔧 D={resultat['diametre']:.3f}m, V={resultat['vitesse']:.2f}m/s")
            
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
    """🏗️ Dimensionnement réservoir unifié avec transparence mathématique
    
    Types d'adduction:
    - continue: Adduction continue
    - discontinue: Adduction discontinue
    
    Formes disponibles:
    - cylindrique: Réservoir cylindrique
    - parallelepipedique: Réservoir parallélépipédique
    
    Exemple: lcpi aep reservoir-unified 1000 --adduction continue --forme cylindrique
    """
    from .calculations.reservoir_unified import dimension_reservoir
    
    try:
        resultat = dimension_reservoir(
            volume_journalier_m3, type_adduction, forme_reservoir, type_zone, verbose
        )
        
        if verbose:
            typer.echo(f"🏗️ Dimensionnement réservoir:")
            typer.echo(f"  Volume utile: {resultat['volume_utile']:.0f} m³")
            typer.echo(f"  Volume total: {resultat['volume_total']:.0f} m³")
            typer.echo(f"  Hauteur: {resultat['hauteur']:.2f} m")
            typer.echo(f"  Diamètre: {resultat['diametre']:.2f} m")
        else:
            typer.echo(f"🏗️ V={resultat['volume_total']:.0f}m³, H={resultat['hauteur']:.2f}m")
            
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
    """⚡ Dimensionnement pompage unifié avec transparence mathématique
    
    Types de pompes:
    - centrifuge: Pompe centrifuge
    - helice: Pompe à hélice
    - piston: Pompe à piston
    
    Exemple: lcpi aep pumping-unified 100 --hmt 50 --type centrifuge
    """
    from .calculations.pumping_unified import dimension_pumping
    
    try:
        resultat = dimension_pumping(
            debit_m3h, hmt_m, type_pompe, rendement_pompe, verbose
        )
        
        if verbose:
            typer.echo(f"⚡ Dimensionnement pompage:")
            typer.echo(f"  Débit: {debit_m3h} m³/h")
            typer.echo(f"  HMT: {hmt_m} m")
            typer.echo(f"  Puissance hydraulique: {resultat['puissance_hydraulique']:.1f} kW")
            typer.echo(f"  Puissance électrique: {resultat['puissance_electrique']:.1f} kW")
        else:
            typer.echo(f"⚡ P={resultat['puissance_electrique']:.1f}kW")
            
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

# =============================================================================
# COMMANDES BASE DE DONNÉES
# =============================================================================

@app.command()
def query(
    query_type: str = typer.Argument(..., help="Type de requête (coefficients, materials, formulas, constants, search)"),
    search_term: str = typer.Option("", "--search", "-s", help="Terme de recherche"),
    material: str = typer.Option("", "--material", "-m", help="Matériau spécifique"),
    category: str = typer.Option("", "--category", "-c", help="Catégorie spécifique"),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, csv, markdown)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """📊 Interroge la base de données AEP
    
    Types de requête:
    - coefficients: Coefficients de rugosité
    - materials: Matériaux de conduites
    - formulas: Formules de calcul
    - constants: Constantes physiques
    - search: Recherche textuelle
    
    Exemple: lcpi aep query coefficients --material fonte --format json
    """
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
    """🔍 Génère des suggestions d'auto-complétion
    
    Exemple: lcpi aep autocomplete coef --limit 5
    """
    try:
        from ..db.aep_database_manager import AEPDatabaseManager
        
        manager = AEPDatabaseManager()
        suggestions = manager.get_autocomplete_suggestions(query, limit)
        
        if suggestions:
            typer.echo(f"🔍 Suggestions pour '{query}':")
            for suggestion in suggestions:
                typer.echo(f"  • {suggestion}")
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
    """🔍 Recherche textuelle dans la base de données AEP
    
    Exemple: lcpi aep search coefficient --format json --verbose
    """
    try:
        from ..db.aep_database_manager import AEPDatabaseManager
        
        manager = AEPDatabaseManager()
        results = manager.search_database(term)
        
        if verbose:
            typer.echo(f"🔍 Recherche: '{term}'")
            typer.echo(f"📊 Résultats: {len(results)} trouvés")
        
        if results:
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
            typer.echo(f"❌ Aucun résultat trouvé pour '{term}'")
            
    except Exception as e:
        typer.echo(f"❌ Erreur lors de la recherche: {e}", err=True)

# =============================================================================
# COMMANDES HARDY-CROSS
# =============================================================================

@app.command()
def hardy_cross_csv(
    csv_path: str = typer.Argument(..., help="Chemin vers le fichier CSV"),
    max_iterations: int = typer.Option(100, "--max-iterations", "-i", help="Nombre maximum d'itérations"),
    tolerance: float = typer.Option(1e-6, "--tolerance", "-t", help="Tolérance de convergence"),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, markdown, csv)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """🔄 Exécute l'analyse Hardy-Cross depuis un fichier CSV
    
    Format CSV attendu:
    - Colonnes: pipe_id, from_node, to_node, length, diameter, roughness, initial_flow
    
    Exemple: lcpi aep hardy-cross-csv reseau.csv --tolerance 1e-6
    """
    try:
        from .calculations.hardy_cross_enhanced import HardyCrossEnhanced
        
        if verbose:
            typer.echo(f"🔄 Hardy-Cross depuis CSV: {csv_path}")
        
        # Charger les données CSV
        import pandas as pd
        df = pd.read_csv(csv_path)
        
        # Convertir en format réseau
        network_data = {
            "network": {
                "nodes": {},
                "pipes": {}
            }
        }
        
        # Extraire les nœuds uniques
        all_nodes = set()
        for _, row in df.iterrows():
            all_nodes.add(row['from_node'])
            all_nodes.add(row['to_node'])
        
        for node in all_nodes:
            network_data["network"]["nodes"][node] = {
                "elevation": 0,  # Valeur par défaut
                "demand": 0.0
            }
        
        # Extraire les conduites
        for _, row in df.iterrows():
            pipe_id = row['pipe_id']
            network_data["network"]["pipes"][pipe_id] = {
                "from_node": row['from_node'],
                "to_node": row['to_node'],
                "length": row['length'],
                "diameter": row['diameter'],
                "roughness": row['roughness'],
                "initial_flow": row['initial_flow']
            }
        
        # Exécuter Hardy-Cross
        hardy_cross = HardyCrossEnhanced()
        resultat = hardy_cross.solve(network_data)
        
        if verbose:
            typer.echo(f"✅ Hardy-Cross terminé:")
            typer.echo(f"  Itérations: {resultat['iterations']}")
            typer.echo(f"  Tolérance finale: {resultat['tolerance']:.2e}")
            typer.echo(f"  Temps: {resultat['temps']:.3f} s")
        
        # Exporter les résultats
        if output_format == "json":
            typer.echo(json.dumps(resultat, indent=2, ensure_ascii=False))
        elif output_format == "markdown":
            _export_hardy_cross_markdown(resultat)
        elif output_format == "csv":
            _export_hardy_cross_csv(resultat)
        else:
            typer.echo(f"❌ Format non supporté: {output_format}")
            
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def hardy_cross_yaml(
    yaml_path: str = typer.Argument(..., help="Chemin vers le fichier YAML"),
    max_iterations: int = typer.Option(100, "--max-iterations", "-i", help="Nombre maximum d'itérations"),
    tolerance: float = typer.Option(1e-6, "--tolerance", "-t", help="Tolérance de convergence"),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, markdown, csv)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """🔄 Exécute l'analyse Hardy-Cross depuis un fichier YAML
    
    Format YAML attendu:
    ```yaml
    network:
      nodes:
        N1: {elevation: 100, demand: 0.05}
      pipes:
        P1: {from_node: N1, to_node: N2, length: 100, diameter: 0.3, roughness: 130}
    ```
    
    Exemple: lcpi aep hardy-cross-yaml reseau.yml --tolerance 1e-6
    """
    try:
        from .calculations.hardy_cross_enhanced import HardyCrossEnhanced
        import yaml
        
        if verbose:
            typer.echo(f"🔄 Hardy-Cross depuis YAML: {yaml_path}")
        
        # Charger les données YAML
        with open(yaml_path, 'r', encoding='utf-8') as f:
            network_data = yaml.safe_load(f)
        
        # Exécuter Hardy-Cross
        hardy_cross = HardyCrossEnhanced()
        resultat = hardy_cross.solve(network_data)
        
        if verbose:
            typer.echo(f"✅ Hardy-Cross terminé:")
            typer.echo(f"  Itérations: {resultat['iterations']}")
            typer.echo(f"  Tolérance finale: {resultat['tolerance']:.2e}")
            typer.echo(f"  Temps: {resultat['temps']:.3f} s")
        
        # Exporter les résultats
        if output_format == "json":
            typer.echo(json.dumps(resultat, indent=2, ensure_ascii=False))
        elif output_format == "markdown":
            _export_hardy_cross_markdown(resultat)
        elif output_format == "csv":
            _export_hardy_cross_csv(resultat)
        else:
            typer.echo(f"❌ Format non supporté: {output_format}")
            
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)

@app.command()
def hardy_cross_help():
    """📚 Affiche l'aide pour la méthode Hardy-Cross"""
    try:
        from .calculations.hardy_cross_interface import get_hardy_cross_help
        
        help_text = get_hardy_cross_help()
        typer.echo(help_text)
        
    except Exception as e:
        typer.echo(f"❌ Erreur lors de l'affichage de l'aide: {e}", err=True)

# =============================================================================
# COMMANDES WORKFLOW COMPLET
# =============================================================================

@app.command()
def simulate_inp(
    inp_file: str = typer.Argument(..., help="Chemin vers le fichier .inp EPANET"),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, markdown, csv)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """🌐 Simule un fichier .inp EPANET avec LCPI AEP
    
    Formats de sortie:
    - json: Données structurées JSON
    - markdown: Rapport formaté Markdown
    - csv: Données tabulaires CSV
    
    Exemple: lcpi aep simulate-inp reseau.inp --format json --verbose
    """
    try:
        from .epanet_wrapper import EpanetSimulator
        import os
        
        if not os.path.exists(inp_file):
            typer.echo(f"❌ ERREUR: Fichier {inp_file} introuvable")
            return
        
        if verbose:
            typer.echo(f"🚀 SIMULATION FICHIER .INP: {inp_file}")
        
        # Créer l'instance EPANET
        epanet = EpanetSimulator()
        
        # Ouvrir le fichier .inp
        if not epanet.open_project(inp_file):
            typer.echo("❌ ERREUR: Impossible d'ouvrir le fichier .inp")
            return
        
        if verbose:
            typer.echo("✅ Fichier .inp ouvert avec succès")
        
        # Lancer la simulation hydraulique
        if not epanet.solve_hydraulics():
            typer.echo("❌ ERREUR: Échec de la simulation hydraulique")
            return
        
        if verbose:
            typer.echo("✅ Simulation hydraulique réussie")
        
        # Extraire les résultats
        results = _extract_epanet_results(epanet)
        
        # Afficher un résumé
        typer.echo(f"📊 RÉSUMÉ: {results['node_count']} nœuds, {results['pipe_count']} conduites")
        typer.echo(f"📊 RÉSERVOIRS: {results['reservoir_count']}, TANKS: {results['tank_count']}")
        
        if 'statistics' in results:
            stats = results['statistics']
            typer.echo(f"📈 ITÉRATIONS: {stats.get('iterations', 'N/A')}")
            typer.echo(f"📈 ERREUR RELATIVE: {stats.get('relative_error', 'N/A')}")

        # Exporter les résultats
        if output_format == "json":
            typer.echo(json.dumps(results, indent=2, ensure_ascii=False))
        elif output_format == "markdown":
            _export_results_markdown(results)
        elif output_format == "csv":
            _export_results_csv(results)
        
        # Fermer le projet
        epanet.close_project()
        
        if verbose:
            typer.echo("✅ Simulation terminée avec succès")
            
    except Exception as e:
        typer.echo(f"❌ ERREUR: {e}", err=True)

@app.command()
def convert_inp(
    inp_file: str = typer.Argument(..., help="Chemin vers le fichier .inp EPANET"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Fichier YAML de sortie (optionnel)"),
    simulate: bool = typer.Option(True, "--simulate", "-s", help="Simuler après conversion"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """🔄 Convertit un fichier .inp EPANET en YAML LCPI et le simule
    
    Fonctionnalités:
    - Parse le fichier .inp EPANET
    - Convertit en format YAML LCPI
    - Simule avec diagnostics (optionnel)
    
    Exemple: lcpi aep convert-inp reseau.inp --simulate --verbose
    """
    try:
        import yaml
        from pathlib import Path
        
        if verbose:
            typer.echo(f"📁 Lecture du fichier .inp: {inp_file}")
        
        # Parser le fichier .inp
        network_data = _parse_inp_file(inp_file)
        if not network_data:
            typer.echo("❌ Échec du parsing du fichier .inp")
            return
        
        # Générer le nom du fichier YAML
        if output_file:
            yaml_path = output_file
        else:
            inp_path = Path(inp_file)
            yaml_path = str(inp_path.with_suffix('.yml'))
        
        # Sauvegarder en YAML
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(network_data, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        typer.echo(f"✅ Fichier YAML créé: {yaml_path}")
        typer.echo(f"📊 Nœuds: {len(network_data['network']['nodes'])}, Conduites: {len(network_data['network']['pipes'])}")
        
        # Simuler si demandé
        if simulate:
            typer.echo("\n🚀 SIMULATION AVEC LCPI AEP")
            from .epanet_integration import run_epanet_with_diagnostics
            
            results = run_epanet_with_diagnostics(network_data)
            
            if results['success']:
                typer.echo("✅ Simulation LCPI AEP réussie")
                if 'epanet_results' in results:
                    epanet_results = results['epanet_results']
                    typer.echo(f"📊 Nœuds simulés: {len(epanet_results.get('nodes', {}))}")
                    typer.echo(f"📊 Conduites simulées: {len(epanet_results.get('pipes', {}))}")
            else:
                typer.echo("❌ Échec de la simulation LCPI AEP")
                if 'errors' in results:
                    for error in results['errors']:
                        typer.echo(f"   • {error}")
        
    except Exception as e:
        typer.echo(f"❌ ERREUR: {e}", err=True)

@app.command()
def diagnose_network(
    network_file: str = typer.Argument(..., help="Fichier YAML/JSON avec les données du réseau"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails"),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, markdown)")
):
    """🔍 Diagnostique la connectivité d'un réseau hydraulique
    
    Vérifications:
    - Connectivité du réseau
    - Présence de sources d'eau
    - Compatibilité EPANET
    - Analyse topologique
    
    Exemple: lcpi aep diagnose-network reseau.yml --verbose
    """
    try:
        import yaml
        from .network_diagnostics import diagnose_network_connectivity, validate_epanet_compatibility, analyze_network_topology
        
        # Charger les données
        with open(network_file, 'r', encoding='utf-8') as f:
            network_data = yaml.safe_load(f)
        
        if verbose:
            typer.echo(f"🔍 DIAGNOSTIC RÉSEAU: {network_file}")
        
        # Diagnostic de connectivité
        is_connected = diagnose_network_connectivity(network_data)
        
        # Validation EPANET
        validation = validate_epanet_compatibility(network_data)
        
        # Analyse topologique
        topology = analyze_network_topology(network_data)
        
        # Résumé
        typer.echo(f"📊 CONNECTIVITÉ: {'✅ Connecté' if is_connected else '❌ Non connecté'}")
        typer.echo(f"📊 COMPATIBILITÉ EPANET: {'✅ Compatible' if validation['compatible'] else '❌ Incompatible'}")
        typer.echo(f"📊 TOPOLOGIE: {topology.get('nombre_noeuds', 0)} nœuds, {topology.get('nombre_conduites', 0)} conduites")
        
        # Exporter les résultats
        results = {
            "connectivity": is_connected,
            "epanet_compatibility": validation,
            "topology": topology
        }
        
        if output_format == "json":
            typer.echo(json.dumps(results, indent=2, ensure_ascii=False))
        elif output_format == "markdown":
            _export_diagnostic_markdown(results)
            
    except Exception as e:
        typer.echo(f"❌ ERREUR: {e}", err=True)

@app.command()
def workflow_complete(
    network_file: str = typer.Argument(..., help="Fichier YAML/JSON avec les données du réseau"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Répertoire de sortie"),
    compare_methods: bool = typer.Option(True, "--compare", "-c", help="Comparer Hardy-Cross et EPANET"),
    generate_reports: bool = typer.Option(True, "--reports", "-r", help="Générer les rapports"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """🚀 Workflow AEP complet : diagnostic + Hardy-Cross + EPANET + comparaison + rapports
    
    Étapes du workflow:
    1. 🔍 Diagnostic de connectivité du réseau
    2. ⚡ Simulation Hardy-Cross (méthode itérative)
    3. 🌐 Simulation EPANET (standard industriel)
    4. 🔄 Comparaison des résultats (si activée)
    5. 📋 Génération de rapports (si activée)
    
    Exemple: lcpi aep workflow-complete reseau.yml --compare --reports --verbose
    """
    try:
        import yaml
        from pathlib import Path
        from .epanet_integration import run_epanet_with_diagnostics
        
        if verbose:
            typer.echo(f"🚀 WORKFLOW AEP COMPLET: {network_file}")
        
        # Charger les données
        with open(network_file, 'r', encoding='utf-8') as f:
            network_data = yaml.safe_load(f)
        
        # 1. Diagnostic
        typer.echo("🔍 ÉTAPE 1: DIAGNOSTIC")
        from .network_diagnostics import diagnose_network_connectivity
        is_connected = diagnose_network_connectivity(network_data)
        
        if not is_connected:
            typer.echo("❌ Réseau non connecté - arrêt du workflow")
            return
        
        # 2. Hardy-Cross
        typer.echo("⚡ ÉTAPE 2: HARDY-CROSS")
        try:
            from ..calculations.hardy_cross_enhanced import HardyCrossEnhanced
        except ImportError:
            typer.echo("❌ ERREUR: Module Hardy-Cross non trouvé")
            return
        hardy_cross = HardyCrossEnhanced()
        hardy_results = hardy_cross.solve(network_data)
        
        if verbose:
            typer.echo(f"✅ Hardy-Cross: {hardy_results['iterations']} itérations, tolérance {hardy_results['tolerance']:.2e}")
        
        # 3. EPANET avec diagnostics
        typer.echo("🌐 ÉTAPE 3: EPANET")
        epanet_results = run_epanet_with_diagnostics(network_data)
        
        if not epanet_results['success']:
            typer.echo("❌ Échec EPANET - arrêt du workflow")
            return
        
        # 4. Comparaison (si demandée)
        if compare_methods:
            typer.echo("🔄 ÉTAPE 4: COMPARAISON")
            comparison = _compare_results(hardy_results, epanet_results)
            
            if verbose:
                typer.echo(f"📊 Écart moyen pressions: {comparison['mean_pressure_diff']:.2f} m")
        
        # 5. Rapports (si demandés)
        if generate_reports:
            typer.echo("📋 ÉTAPE 5: RAPPORTS")
            output_path = output_dir or Path(network_file).parent / "output"
            Path(output_path).mkdir(exist_ok=True)
            
            _generate_workflow_reports(
                network_data, hardy_results, epanet_results, 
                comparison if compare_methods else None,
                output_path
            )
            
            typer.echo(f"✅ Rapports générés dans: {output_path}")
        
        typer.echo("🎉 WORKFLOW AEP COMPLET TERMINÉ AVEC SUCCÈS!")
        
    except Exception as e:
        typer.echo(f"❌ ERREUR: {e}", err=True)

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def _extract_epanet_results(epanet):
    """Extrait les résultats d'une simulation EPANET"""
    results = {
        "nodes": {},
        "pipes": {},
        "statistics": {}
    }
    
    try:
        # Statistiques de simulation
        results["statistics"] = {
            "iterations": epanet.getstatistic(0),
            "relative_error": epanet.getstatistic(1),
            "max_head_error": epanet.getstatistic(2),
            "max_flow_change": epanet.getstatistic(3),
            "mass_balance": epanet.getstatistic(4)
        }
        
        # Résultats des nœuds
        node_count = epanet.getcount(0)
        results["node_count"] = node_count
        
        for i in range(1, node_count + 1):
            node_id = epanet.getnodeid(i)
            results["nodes"][node_id] = {
                "pressure": epanet.getnodevalue(i, 0),
                "head": epanet.getnodevalue(i, 1),
                "demand": epanet.getnodevalue(i, 2),
                "quality": epanet.getnodevalue(i, 3)
            }
        
        # Résultats des conduites
        pipe_count = epanet.getcount(1)
        results["pipe_count"] = pipe_count
        
        for i in range(1, pipe_count + 1):
            link_id = epanet.getlinkid(i)
            results["pipes"][link_id] = {
                "flow": epanet.getlinkvalue(i, 0),
                "velocity": epanet.getlinkvalue(i, 1),
                "headloss": epanet.getlinkvalue(i, 2),
                "quality": epanet.getlinkvalue(i, 3),
                "status": epanet.getlinkvalue(i, 4)
            }
        
        # Compter les types de nœuds
        reservoir_count = 0
        tank_count = 0
        
        for i in range(1, node_count + 1):
            node_type = epanet.getnodetype(i)
            if node_type == 0:  # EN_RESERVOIR
                reservoir_count += 1
            elif node_type == 1:  # EN_TANK
                tank_count += 1
        
        results["reservoir_count"] = reservoir_count
        results["tank_count"] = tank_count
        
    except Exception as e:
        typer.echo(f"⚠️  Avertissement lors de l'extraction: {e}")
    
    return results

def _parse_inp_file(inp_file_path):
    """Parse un fichier .inp EPANET"""
    network_data = {
        "network": {
            "nodes": {},
            "pipes": {}
        },
        "metadata": {
            "source": "EPANET .inp file",
            "original_file": inp_file_path
        }
    }
    
    try:
        with open(inp_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if not line or line.startswith(';') or line.startswith('['):
                continue
            
            # Détecter les sections
            if line.upper() == '[JUNCTIONS]':
                current_section = 'junctions'
                continue
            elif line.upper() == '[RESERVOIRS]':
                current_section = 'reservoirs'
                continue
            elif line.upper() == '[TANKS]':
                current_section = 'tanks'
                continue
            elif line.upper() == '[PIPES]':
                current_section = 'pipes'
                continue
            elif line.upper() == '[PUMPS]':
                current_section = 'pumps'
                continue
            elif line.upper() == '[VALVES]':
                current_section = 'valves'
                continue
            
            # Parser les données selon la section
            if current_section == 'junctions':
                parts = line.split()
                if len(parts) >= 3:
                    node_id = parts[0]
                    network_data["network"]["nodes"][node_id] = {
                        "type": "junction",
                        "elevation": float(parts[1]),
                        "demand": float(parts[2]) if len(parts) > 2 else 0.0
                    }
            
            elif current_section == 'reservoirs':
                parts = line.split()
                if len(parts) >= 2:
                    node_id = parts[0]
                    network_data["network"]["nodes"][node_id] = {
                        "type": "reservoir",
                        "elevation": float(parts[1]),
                        "demand": 0.0
                    }
            
            elif current_section == 'tanks':
                parts = line.split()
                if len(parts) >= 4:
                    node_id = parts[0]
                    network_data["network"]["nodes"][node_id] = {
                        "type": "tank",
                        "elevation": float(parts[1]),
                        "initial_level": float(parts[2]),
                        "minimum_level": float(parts[3]),
                        "maximum_level": float(parts[4]) if len(parts) > 4 else float(parts[2]) + 10,
                        "demand": 0.0
                    }
            
            elif current_section == 'pipes':
                parts = line.split()
                if len(parts) >= 6:
                    pipe_id = parts[0]
                    network_data["network"]["pipes"][pipe_id] = {
                        "from_node": parts[1],
                        "to_node": parts[2],
                        "length": float(parts[3]),
                        "diameter": float(parts[4]),
                        "roughness": float(parts[5])
                    }
            
            elif current_section == 'pumps':
                parts = line.split()
                if len(parts) >= 3:
                    pump_id = parts[0]
                    network_data["network"]["pipes"][pump_id] = {
                        "from_node": parts[1],
                        "to_node": parts[2],
                        "type": "pump",
                        "pump_curve": parts[3] if len(parts) > 3 else "HEAD"
                    }
            
            elif current_section == 'valves':
                parts = line.split()
                if len(parts) >= 4:
                    valve_id = parts[0]
                    network_data["network"]["pipes"][valve_id] = {
                        "from_node": parts[1],
                        "to_node": parts[2],
                        "type": "valve",
                        "valve_type": parts[3],
                        "setting": float(parts[4]) if len(parts) > 4 else 0.0
                    }
        
        return network_data
        
    except Exception as e:
        typer.echo(f"❌ ERREUR lors du parsing: {e}")
        return None

def _compare_results(hardy_results, epanet_results):
    """Compare les résultats Hardy-Cross et EPANET"""
    comparison = {
        "correlation_flows": 0.0,
        "mean_pressure_diff": 0.0,
        "max_pressure_diff": 0.0,
        "flow_differences": {},
        "pressure_differences": {}
    }
    
    try:
        # Comparaison des débits
        hardy_flows = hardy_results.get('flows', {})
        epanet_flows = epanet_results.get('epanet_results', {}).get('pipes', {})
        
        common_pipes = set(hardy_flows.keys()) & set(epanet_flows.keys())
        
        if common_pipes:
            differences = []
            for pipe_id in common_pipes:
                hardy_flow = hardy_flows[pipe_id]
                epanet_flow = epanet_flows[pipe_id].get('flow', 0)
                diff = abs(hardy_flow - epanet_flow)
                differences.append(diff)
                comparison["flow_differences"][pipe_id] = diff
            
            comparison["mean_flow_diff"] = sum(differences) / len(differences) if differences else 0.0
        
        # Comparaison des pressions
        hardy_pressures = hardy_results.get('pressures', {})
        epanet_pressures = epanet_results.get('epanet_results', {}).get('nodes', {})
        
        common_nodes = set(hardy_pressures.keys()) & set(epanet_pressures.keys())
        
        if common_nodes:
            pressure_diffs = []
            for node_id in common_nodes:
                hardy_pressure = hardy_pressures[node_id]
                epanet_pressure = epanet_pressures[node_id].get('pressure', 0)
                diff = abs(hardy_pressure - epanet_pressure)
                pressure_diffs.append(diff)
                comparison["pressure_differences"][node_id] = diff
            
            comparison["mean_pressure_diff"] = sum(pressure_diffs) / len(pressure_diffs) if pressure_diffs else 0.0
            comparison["max_pressure_diff"] = max(pressure_diffs) if pressure_diffs else 0.0
        
    except Exception as e:
        typer.echo(f"⚠️  Avertissement lors de la comparaison: {e}")
    
    return comparison

def _export_results_markdown(results):
    """Exporte les résultats en Markdown"""
    typer.echo("# Résultats Simulation EPANET")
    typer.echo(f"\n## Statistiques")
    typer.echo(f"- Nœuds: {results['node_count']}")
    typer.echo(f"- Conduites: {results['pipe_count']}")
    typer.echo(f"- Réservoirs: {results['reservoir_count']}")
    typer.echo(f"- Tanks: {results['tank_count']}")
    
    if 'statistics' in results:
        stats = results['statistics']
        typer.echo(f"\n## Convergence")
        typer.echo(f"- Itérations: {stats.get('iterations', 'N/A')}")
        typer.echo(f"- Erreur relative: {stats.get('relative_error', 'N/A')}")

def _export_results_csv(results):
    """Exporte les résultats en CSV"""
    typer.echo("node_id,pressure,head,demand")
    for node_id, node_data in results['nodes'].items():
        typer.echo(f"{node_id},{node_data.get('pressure', 'N/A')},{node_data.get('head', 'N/A')},{node_data.get('demand', 'N/A')}")

def _export_diagnostic_markdown(results):
    """Exporte le diagnostic en Markdown"""
    typer.echo("# Diagnostic Réseau")
    typer.echo(f"\n## Connectivité")
    typer.echo(f"- Statut: {'✅ Connecté' if results['connectivity'] else '❌ Non connecté'}")
    
    typer.echo(f"\n## Compatibilité EPANET")
    typer.echo(f"- Compatible: {'✅ Oui' if results['epanet_compatibility']['compatible'] else '❌ Non'}")
    
    if results['epanet_compatibility']['erreurs']:
        typer.echo(f"\n### Erreurs:")
        for error in results['epanet_compatibility']['erreurs']:
            typer.echo(f"- {error}")

def _generate_workflow_reports(network_data, hardy_results, epanet_results, comparison, output_path):
    """Génère les rapports du workflow complet"""
    try:
        from pathlib import Path
        import json
        
        # Rapport principal
        report_path = Path(output_path) / "rapport_workflow.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Rapport Workflow AEP Complet\n\n")
            f.write(f"## Résumé\n")
            f.write(f"- Réseau: {len(network_data['network']['nodes'])} nœuds, {len(network_data['network']['pipes'])} conduites\n")
            f.write(f"- Hardy-Cross: {hardy_results['iterations']} itérations\n")
            f.write(f"- EPANET: {'✅ Succès' if epanet_results['success'] else '❌ Échec'}\n")
            
            if comparison:
                f.write(f"- Comparaison: Écart moyen pressions {comparison['mean_pressure_diff']:.2f} m\n")
        
        # Données JSON
        data_path = Path(output_path) / "resultats.json"
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump({
                "hardy_cross": hardy_results,
                "epanet": epanet_results,
                "comparison": comparison
            }, f, indent=2, ensure_ascii=False)
        
        typer.echo(f"✅ Rapports générés: {report_path}, {data_path}")
        
    except Exception as e:
        typer.echo(f"⚠️  Avertissement lors de la génération des rapports: {e}")

if __name__ == "__main__":
    app()