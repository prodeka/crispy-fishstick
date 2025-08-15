"""
Interface CLI pour le module AEP (Alimentation en Eau Potable)
"""

import typer
from pathlib import Path
from typing import Optional, Dict, Any
import json

app = typer.Typer(name="aep", help="Module Alimentation en Eau Potable")

# =============================================================================
# OUTILS COMMUNS POUR LES COMMANDES UNIFIÉES
# =============================================================================

def _load_input_file(input_path: Path) -> Dict[str, Any]:
    """Charge un fichier d'entrée YAML/JSON/CSV en dict.

    Retourne un dictionnaire prêt à être passé aux fonctions "enhanced".
    """
    try:
        suffix = input_path.suffix.lower()
        if suffix in {".yml", ".yaml"}:
            import yaml
            with open(input_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        elif suffix == ".json":
            with open(input_path, 'r', encoding='utf-8') as f:
                return json.load(f) or {}
        elif suffix == ".csv":
            import csv
            rows = []
            with open(input_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)
            return {"rows": rows}
        else:
            raise ValueError(f"Extension de fichier non supportée: {suffix}")
    except Exception as e:
        raise ValueError(f"Erreur lors du chargement du fichier d'entrée: {e}")


from .utils.exporters import export_content as _export_generic
from .utils.exporters import _flatten_dict
from .core.validators import (
	check_physical_constraints,
	validate_and_clean_data,
	validate_population_unified_data,
	validate_network_unified_data,
)


def _make_result(valeurs: Dict[str, Any], diagnostics: Optional[Any] = None, iterations: Optional[Any] = None) -> Dict[str, Any]:
	"""Normalise la structure de sortie (valeurs, diagnostics, iterations)."""
	return {
		"valeurs": valeurs or {},
		"diagnostics": diagnostics or [],
		"iterations": iterations,
	}

# =============================================================================
# COMMANDES DE BASE
# =============================================================================

@app.command()
def population(
    fichier_csv: Path = typer.Argument(..., help="Fichier CSV avec les données de population", exists=True, file_okay=True, dir_okay=False, readable=True),
    annee_debut: int = typer.Option(2020, "--debut", "-d", help="Année de début de projection"),
    annee_fin: int = typer.Option(2050, "--fin", "-f", help="Année de fin de projection"),
    taux_croissance: float = typer.Option(0.02, "--taux", "-t", help="Taux de croissance annuel (décimal)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie (par défaut: population_projetee.csv)")
):
    """📊 Calcul de projection de population
    
    Projette la population d'une zone donnée sur plusieurs années en utilisant un taux de croissance constant.
    
    **Structure du fichier CSV d'entrée :**
    ```csv
    annee,population
    2020,15000
    2021,15200
    2022,15400
    ```
    
    **Exemple d'utilisation :**
    ```bash
    lcpi aep population data/population.csv --debut 2020 --fin 2050 --taux 0.025 --output projections.csv
    ```
    
    **Exemple de données d'entrée :**
    ```csv
    annee,population
    2020,15000
    2021,15200
    2022,15400
    ```
    """
    try:
        # Charger les données de population depuis le CSV
        import pandas as pd
        
        df = pd.read_csv(fichier_csv)
        
        # Vérifier la structure du fichier
        if 'annee' not in df.columns or 'population' not in df.columns:
            raise ValueError("Le fichier CSV doit contenir les colonnes 'annee' et 'population'")
        
        # Calculer la projection
        annees = list(range(annee_debut, annee_fin + 1))
        populations = []
        
        # Utiliser la dernière valeur connue comme base
        derniere_population = df['population'].iloc[-1]
        
        for annee in annees:
            if annee <= df['annee'].max():
                # Année dans les données historiques
                pop = df[df['annee'] == annee]['population'].iloc[0] if annee in df['annee'].values else derniere_population
            else:
                # Projection future
                annees_ecoulees = annee - df['annee'].max()
                pop = derniere_population * (1 + taux_croissance) ** annees_ecoulees
            
            populations.append(pop)
        
        # Créer le DataFrame de résultats
        resultats_df = pd.DataFrame({
            'annee': annees,
            'population': [round(p, 0) for p in populations]
        })
        
        # Déterminer le fichier de sortie
        if output is None:
            output = Path("population_projetee.csv")
        
        # Sauvegarder les résultats
        resultats_df.to_csv(output, index=False)
        
        # Afficher un résumé
        print(f"📊 Projection de population terminée!")
        print(f"Période: {annee_debut} - {annee_fin}")
        print(f"Taux de croissance: {taux_croissance:.1%}")
        print(f"Population initiale ({annee_debut}): {int(resultats_df.iloc[0]['population']):,}")
        print(f"Population finale ({annee_fin}): {int(resultats_df.iloc[-1]['population']):,}")
        print(f"Résultats sauvegardés dans: {output}")
        
    except Exception as e:
        typer.echo(f"❌ Erreur lors du calcul de projection: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def demand(
    fichier: Path = typer.Argument(..., help="Fichier YAML/JSON avec les données de demande", exists=True, file_okay=True, dir_okay=False, readable=True),
    type_calcul: str = typer.Option("global", "--type", "-t", help="Type de calcul (global, par_type, avance)"),
    afficher_details: bool = typer.Option(False, "--details", "-d", help="Afficher les détails par type d'usage")
):
    """💧 Calcul de demande en eau pour AEP
    
    Calcule la demande en eau totale et de pointe pour un projet d'alimentation en eau potable.
    
    **Structure du fichier YAML d'entrée :**
    ```yaml
    population:
      actuelle: 15000
      projetee_2030: 18000
      projetee_2050: 22000
    
    consommation:
      domestique: 150  # litres/habitant/jour
      industriel: 50   # litres/habitant/jour
      commercial: 30   # litres/habitant/jour
    
    coefficients:
      pointe_journaliere: 1.3
      pointe_horaire: 1.8
      fuites: 0.15
    ```
    
    **Exemple d'utilisation :**
    ```bash
    lcpi aep demand data/demande.yml --type global --details
    lcpi aep demand data/demande.yml --type par_type
    lcpi aep demand data/demande.yml --type avance --details
    ```
    
    **Types de calcul disponibles :**
    - **global**: Demande totale et de pointe avec coefficients de pointe
    - **par_type**: Détail par type d'usage (domestique, industriel, commercial)
    - **avance**: Calculs avancés avec coefficients saisonniers et analyse temporelle
    """
    try:
        import yaml
        
        # Charger les données YAML
        with open(fichier, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # Calculs simplifiés pour démonstration
        population_actuelle = data.get('population', {}).get('actuelle', 0)
        consommation_domestique = data.get('consommation', {}).get('domestique', 150)
        coefficients = data.get('coefficients', {})
        
        # Calcul de la demande
        demande_moyenne = population_actuelle * consommation_domestique / 1000  # m³/jour
        pointe_journaliere = coefficients.get('pointe_journaliere', 1.3)
        demande_pointe = demande_moyenne * pointe_journaliere
        
        if type_calcul == "par_type" or afficher_details:
            typer.echo("💧 Demande en eau par type d'usage:")
            typer.echo(f"  domestique: {demande_moyenne:.2f} m³/jour")
            typer.echo(f"  industriel: {population_actuelle * data.get('consommation', {}).get('industriel', 50) / 1000:.2f} m³/jour")
            typer.echo(f"  commercial: {population_actuelle * data.get('consommation', {}).get('commercial', 30) / 1000:.2f} m³/jour")
        else:
            typer.echo(f"💧 Demande totale: {demande_moyenne:.2f} m³/jour")
            typer.echo(f"💧 Demande de pointe: {demande_pointe:.2f} m³/jour")
            
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def network(
    fichier: Path = typer.Argument(..., help="Fichier YAML/JSON avec les données du réseau", exists=True, file_okay=True, dir_okay=False, readable=True),
    type_calcul: str = typer.Option("dimensionnement", "--type", "-t", help="Type de calcul (dimensionnement, verification, comparaison)"),
    formule: str = typer.Option("hazen_williams", "--formule", "-f", help="Formule de perte de charge (hazen_williams, manning, darcy_weisbach)")
):
    """🔧 Dimensionnement du réseau de distribution AEP
    
    Calcule le dimensionnement des conduites du réseau d'alimentation en eau potable
    en utilisant différentes formules de perte de charge.
    
    **Structure du fichier YAML d'entrée :**
    ```yaml
    reseau:
      conduites:
        C1:
          longueur: 500      # mètres
          debit: 0.05       # m³/s
          rugosite: 100     # coefficient Hazen-Williams
          type: "acier"
        
        C2:
          longueur: 300
          debit: 0.03
          rugosite: 120
          type: "pvc"
    
    parametres:
      vitesse_max: 2.5      # m/s
      pression_min: 20      # m de colonne d'eau
      tolerance: 0.001      # tolérance de convergence
    ```
    
    **Exemple d'utilisation :**
    ```bash
    lcpi aep network data/reseau.yml --formule hazen_williams
    lcpi aep network data/reseau.yml --type verification --formule manning
    lcpi aep network data/reseau.yml --type comparaison
    ```
    
    **Formules de perte de charge disponibles :**
    - **hazen_williams**: Formule de Hazen-Williams (C) - Standard pour les conduites en service
    - **manning**: Formule de Manning (n) - Adaptée aux canaux et conduites à surface libre
    - **darcy_weisbach**: Formule de Darcy-Weisbach (λ) - Précise mais nécessite le diagramme de Moody
    
    **Types de calcul :**
    - **dimensionnement**: Calcul du diamètre optimal des conduites
    - **verification**: Vérification des vitesses et pressions existantes
    - **comparaison**: Comparaison des résultats avec différentes formules
    """
    try:
        from .calculations.network import dimension_network, compare_network_scenarios
        
        if type_calcul == "comparaison":
            resultats = compare_network_scenarios(str(fichier))
            typer.echo("🔧 Comparaison des scénarios de réseau:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: D={resultat['diametre']:.3f}m, V={resultat['vitesse']:.2f}m/s")
        else:
            resultat = dimension_network(str(fichier), formule)
            typer.echo(f"🔧 Dimensionnement réseau ({formule}):")
            typer.echo(f"  Diamètre: {resultat['diametre']:.3f} m")
            typer.echo(f"  Vitesse: {resultat['vitesse']:.2f} m/s")
            typer.echo(f"  Pertes de charge: {resultat['pertes_charge']:.2f} m")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def reservoir(
    fichier: Path = typer.Argument(..., help="Fichier YAML/JSON avec les données du réservoir", exists=True, file_okay=True, dir_okay=False, readable=True),
    type_calcul: str = typer.Option("dimensionnement", "--type", "-t", help="Type de calcul (dimensionnement, verification, comparaison)"),
    forme: str = typer.Option("cylindrique", "--forme", "-f", help="Forme du réservoir (cylindrique, parallelepipedique)")
):
    """🏗️ Dimensionnement du réservoir de stockage AEP
    
    Calcule le volume et les dimensions optimales du réservoir de stockage
    en fonction de la demande en eau et des contraintes techniques.
    
    **Structure du fichier YAML d'entrée :**
    ```yaml
    reservoir:
      type: "stockage"
      forme: "cylindrique"  # ou "parallelepipedique"
      
      parametres:
        volume_utile: 500    # m³
        reserve_incendie: 100 # m³
        reserve_secours: 50   # m³
        hauteur_max: 8       # mètres
        diametre_max: 15     # mètres (pour cylindrique)
        
      contraintes:
        pression_min: 20     # m de colonne d'eau
        pression_max: 80     # m de colonne d'eau
        niveau_terrain: 150  # mètres NGF
    ```
    
    **Exemple d'utilisation :**
    ```bash
    lcpi aep reservoir data/reservoir.yml --forme cylindrique
    lcpi aep reservoir data/reservoir.yml --type verification --forme parallelepipedique
    lcpi aep reservoir data/reservoir.yml --type comparaison
    ```
    
    **Formes de réservoir disponibles :**
    - **cylindrique**: Réservoir circulaire vertical - Optimale pour la pression
    - **parallelepipedique**: Réservoir rectangulaire - Plus facile à intégrer
    
    **Types de calcul :**
    - **dimensionnement**: Calcul des dimensions optimales
    - **verification**: Vérification des contraintes techniques
    - **comparaison**: Comparaison des deux formes
    """
    try:
        from .calculations.reservoir import dimension_reservoir, compare_reservoir_scenarios
        
        if type_calcul == "comparaison":
            resultats = compare_reservoir_scenarios(str(fichier))
            typer.echo("🏗️ Comparaison des scénarios de réservoir:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: V={resultat['volume']:.0f}m³, H={resultat['hauteur']:.2f}m")
        else:
            resultat = dimension_reservoir(str(fichier), forme)
            typer.echo(f"🏗️ Dimensionnement réservoir ({forme}):")
            typer.echo(f"  Volume: {resultat['volume']:.0f} m³")
            typer.echo(f"  Hauteur: {resultat['hauteur']:.2f} m")
            typer.echo(f"  Surface: {resultat['surface']:.2f} m²")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def pumping(
    fichier: Path = typer.Argument(..., help="Fichier YAML/JSON avec les données de pompage", exists=True, file_okay=True, dir_okay=False, readable=True),
    type_calcul: str = typer.Option("dimensionnement", "--type", "-t", help="Type de calcul (dimensionnement, verification, comparaison)"),
    rendement: float = typer.Option(0.75, "--rendement", "-r", help="Rendement de la pompe (0-1)")
):
    """⚡ Dimensionnement des équipements de pompage AEP
    
    Calcule la puissance et les caractéristiques des pompes nécessaires
    pour l'adduction d'eau en fonction du débit et de la hauteur manométrique.
    
    **Structure du fichier YAML d'entrée :**
    ```yaml
    pompage:
      station: "Station_Principale"
      type: "adduction"
      
      parametres:
        debit_nominal: 0.15    # m³/s
        hauteur_geometrique: 45 # mètres
        longueur_conduite: 2500 # mètres
        diametre_conduite: 0.4  # mètres
        rugosite: 100           # coefficient Hazen-Williams
        
      contraintes:
        vitesse_max: 2.5        # m/s
        pression_max: 100       # bar
        rendement_min: 0.75     # rendement minimum des pompes
        
      pompes:
        P1:
          type: "centrifuge"
          nombre: 2
          fonctionnement: "parallele"
    ```
    
    **Exemple d'utilisation :**
    ```bash
    lcpi aep pumping data/pompage.yml --rendement 0.80
    lcpi aep pumping data/pompage.yml --type verification --rendement 0.75
    lcpi aep pumping data/pompage.yml --type comparaison
    ```
    
    **Types de pompes disponibles :**
    - **centrifuge**: Pompe centrifuge - Standard pour l'adduction d'eau
    - **helice**: Pompe à hélice - Adaptée aux gros débits
    - **piston**: Pompe à piston - Haute pression, faible débit
    
    **Types de calcul :**
    - **dimensionnement**: Calcul de la puissance et des caractéristiques des pompes
    - **verification**: Vérification des performances existantes
    - **comparaison**: Comparaison des résultats avec différents rendements
    """
    try:
        from .calculations.pumping import dimension_pumping, compare_pumping_scenarios
        
        if type_calcul == "comparaison":
            resultats = compare_pumping_scenarios(str(fichier))
            typer.echo("⚡ Comparaison des scénarios de pompage:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: P={resultat['puissance']:.1f}kW, Q={resultat['debit']:.2f}m³/h")
        else:
            resultat = dimension_pumping(str(fichier), rendement)
            typer.echo(f"⚡ Dimensionnement pompage (η={rendement}):")
            typer.echo(f"  Puissance hydraulique: {resultat['puissance_hydraulique']:.1f} kW")
            typer.echo(f"  Puissance électrique: {resultat['puissance_electrique']:.1f} kW")
            typer.echo(f"  Débit: {resultat['debit']:.2f} m³/h")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def protection(
    fichier: Path = typer.Argument(..., help="Fichier YAML/JSON avec les données de protection", exists=True, file_okay=True, dir_okay=False, readable=True),
    type_calcul: str = typer.Option("coup_belier", "--type", "-t", help="Type de calcul (coup_belier, verification, comparaison)")
):
    """🛡️ Calcul de protection contre le coup de bélier AEP
    
    Types de protection:
    - coup_belier: Calcul de la surpression
    - verification: Vérification des protections existantes
    - comparaison: Comparaison de solutions
    
    Exemple: lcpi aep protection protection.yml --type coup_belier
    """
    try:
        from .calculations.protection import calculate_protection, compare_protection_scenarios
        
        if type_calcul == "comparaison":
            resultats = compare_protection_scenarios(str(fichier))
            typer.echo("🛡️ Comparaison des scénarios de protection:")
            for scenario, resultat in resultats.items():
                typer.echo(f"  {scenario}: ΔP={resultat['surpression']:.1f}m, τ={resultat['duree']:.2f}s")
        else:
            resultat = calculate_protection(str(fichier))
            typer.echo(f"🛡️ Protection contre le coup de bélier:")
            typer.echo(f"  Surpression: {resultat['surpression']:.1f} m")
            typer.echo(f"  Durée: {resultat['duree']:.2f} s")
            typer.echo(f"  Énergie: {resultat['energie']:.1f} kJ")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def hardy_cross(
    fichier: Path = typer.Argument(..., help="Fichier JSON/YAML avec les données du réseau maillé", exists=True, file_okay=True, dir_okay=False, readable=True),
    tolerance: float = typer.Option(1e-6, "--tolerance", "-t", help="Tolérance de convergence"),
    max_iterations: int = typer.Option(100, "--iterations", "-i", help="Nombre maximum d'itérations"),
    formule: str = typer.Option("hazen_williams", "--formule", "-f", help="Formule de perte de charge"),
    afficher_iterations: bool = typer.Option(False, "--iterations-detail", "-d", help="Afficher les détails de chaque itération"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Fichier de sortie pour exporter les résultats")
):
    """🔄 Calcul de distribution des débits par méthode Hardy-Cross
    
    Résout le système d'équations hydrauliques d'un réseau maillé en utilisant
    la méthode itérative de Hardy-Cross pour déterminer les débits et pressions.
    
    **Structure du fichier YAML d'entrée :**
    ```yaml
    reseau:
      noeuds:
        N1:
          type: "reservoir"
          cote: 150.0        # mètres NGF
          demande: 0.0       # m³/s
        
        N2:
          type: "consommation"
          cote: 145.0
          demande: 0.02      # m³/s
      
      conduites:
        C1:
          noeud_amont: "N1"
          noeud_aval: "N2"
          longueur: 500      # mètres
          diametre: 0.2      # mètres
          rugosite: 100      # coefficient Hazen-Williams
          type: "acier"
    ```
    
    Exemples:
    - lcpi aep hardy-cross data/reseau.yml --tolerance 1e-6 --iterations 100
    - lcpi aep hardy-cross data/reseau.yml --formule manning --iterations 200
    - lcpi aep hardy-cross data/reseau.yml --export resultats.json
    
    Formules de perte de charge disponibles :
    - **hazen_williams**: Formule de Hazen-Williams (n=1.852) - Standard pour les conduites en service
    - **manning**: Formule de Manning (n=2.0) - Adaptée aux canaux et conduites à surface libre
    - **darcy_weisbach**: Formule de Darcy-Weisbach (n=2.0) - Précise mais nécessite le diagramme de Moody
    
    Paramètres de convergence :
    - **tolerance**: Précision de convergence (défaut: 1e-6)
    - **max_iterations**: Nombre maximum d'itérations (défaut: 100)
    - **afficher_iterations**: Afficher le détail de chaque itération
    
    Sortie standardisée: { valeurs, diagnostics, iterations }
    """
    try:
        from .calculations.hardy_cross import hardy_cross_network
        
        resultat = hardy_cross_network(
            str(fichier), tolerance, max_iterations, formule, afficher_iterations
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
        raise typer.Exit(code=1)

@app.command()
def project(
    fichier: Path = typer.Argument(..., help="Fichier YAML/JSON avec les données du projet complet", exists=True, file_okay=True, dir_okay=False, readable=True),
    type_analyse: str = typer.Option("complet", "--type", "-t", help="Type d'analyse (complet, comparatif, validation)")
):
    """📋 Analyse intégrée d'un projet AEP complet
    
    Effectue une analyse complète d'un projet d'alimentation en eau potable
    en intégrant tous les composants : population, demande, réseau, réservoir, pompage.
    
    **Structure du fichier YAML d'entrée :**
    ```yaml
    projet:
      nom: "Projet AEP Village"
      localisation: "Commune de Example"
      annee_etude: 2024
      
      population:
        actuelle: 15000
        projetee_2030: 18000
        projetee_2050: 22000
      
      reseau:
        type: "ramifie"
        longueur_totale: 25000  # mètres
        diametre_moyen: 0.15    # mètres
        materiau: "pvc"
      
      infrastructure:
        reservoir:
          volume: 500           # m³
          hauteur: 8            # mètres
          type: "cylindrique"
        
        pompage:
          puissance: 45         # kW
          debit: 0.15           # m³/s
          hauteur: 45           # mètres
      
      couts:
        reseau: 450000          # €
        reservoir: 80000        # €
        pompage: 120000         # €
        total: 650000           # €
    ```
    
    **Exemple d'utilisation :**
    ```bash
    lcpi aep project data/projet.yml --type complet
    lcpi aep project data/projet.yml --type comparatif
    lcpi aep project data/projet.yml --type validation
    ```
    
    **Types d'analyse disponibles :**
    - **complet**: Analyse détaillée de tous les composants du projet
    - **comparatif**: Comparaison avec des projets de référence ou des scénarios alternatifs
    - **validation**: Vérification de la cohérence et de la faisabilité technique
    
    **Résultats fournis :**
    - Projection démographique
    - Calcul des besoins en eau
    - Dimensionnement des infrastructures
    - Estimation des coûts
    - Analyse de la rentabilité
    """
    try:
        from .calculations.project import analyze_project
        
        resultat = analyze_project(str(fichier), type_analyse)
        typer.echo(f"📋 Analyse projet ({type_analyse}):")
        typer.echo(f"  Population: {resultat['population']:.0f} habitants")
        typer.echo(f"  Demande: {resultat['demande']:.2f} m³/jour")
        typer.echo(f"  Coût estimé: {resultat['cout']:.0f} €")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

# =============================================================================
# COMMANDES UNIFIÉES
# =============================================================================

@app.command()
def population_unified(
    population_base: Optional[int] = typer.Argument(None, help="Population de base (optionnel si --input fourni)"),
    taux_croissance: float = typer.Option(0.037, "--taux", "-t", help="Taux de croissance annuel"),
    annees: int = typer.Option(20, "--annees", "-a", help="Nombre d'années de projection"),
    methode: str = typer.Option("malthus", "--methode", "-m", help="Méthode de projection"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails"),
    input_file: Optional[Path] = typer.Option(None, "--input", "-i", help="Fichier d'entrée YAML/JSON (active le mode enhanced par défaut)"),
    mode: str = typer.Option("auto", "--mode", "-M", help="Mode de calcul: auto|simple|enhanced"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Export: json|yaml|markdown|csv|html"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour l'export")
):
    """📈 Projection démographique unifiée avec transparence mathématique
    
    Méthodes disponibles:
    - malthus: Croissance exponentielle P(t) = P₀ × e^(rt)
    - arithmetique: Croissance linéaire P(t) = P₀ + rt
    - geometrique: Croissance géométrique P(t) = P₀ × (1+r)^t
    - logistique: Croissance logistique avec saturation
    
    Exemple:
    - lcpi aep population-unified 1000 --taux 0.037 --annees 20
    - lcpi aep population-unified --input data/population.yml --export json
    
    Sortie standardisée: { valeurs, diagnostics, iterations }
    """
    try:
        result: Dict[str, Any]

        use_enhanced = False
        if mode.lower() == "enhanced":
            use_enhanced = True
        elif mode.lower() == "simple":
            use_enhanced = False
        elif mode.lower() == "auto":
            use_enhanced = input_file is not None
        else:
            raise ValueError("--mode doit être parmi: auto|simple|enhanced")

        if use_enhanced:
            if input_file is None:
                raise ValueError("Le mode 'enhanced' pour population_unified requiert --input (YAML/JSON)")
            data = _load_input_file(input_file)
            from .calculations.population_enhanced import calculate_population_projection_enhanced
            result = calculate_population_projection_enhanced(data)
        else:
            if population_base is None:
                raise ValueError("Population de base requise en mode simple (ou utilisez --input pour le mode enhanced)")
            from .calculations.population_unified import calculate_population_projection_unified
            data = {
                "population_base": population_base,
                "taux_croissance": taux_croissance,
                "annees": annees,
                "methode": methode,
                "verbose": verbose
            }
            result = calculate_population_projection_unified(data)

        # Export si demandé
        if export or output:
            fmt = export or "json"
            std = _make_result(result, [], result.get("iterations") or result.get("nombre_iterations"))
            content = _export_generic(std, fmt)
            if output:
                output.write_text(content, encoding="utf-8")
                typer.echo(f"✅ Export sauvegardé: {output}")
            typer.echo(content)
            return

        # Affichage standard (compatibilité)
        if verbose and not use_enhanced:
            typer.echo(f"📈 Projection {methode}:")
            typer.echo(f"  Population initiale: {population_base}")
            typer.echo(f"  Population finale: {result.get('population_finale', 0):.0f}")
            typer.echo(f"  Taux de croissance: {taux_croissance:.3f}")
            typer.echo(f"  Période: {annees} années")
        else:
            # Résumé compact
            final = result.get('population_finale') or result.get('population') or 0
            typer.echo(f"📈 {final:.0f} habitants")

    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def demand_unified(
    population: int = typer.Argument(..., help="Population"),
    dotation_l_hab_j: float = typer.Option(150, "--dotation", "-d", help="Dotation en L/hab/j"),
    coefficient_pointe: float = typer.Option(1.5, "--coeff-pointe", "-c", help="Coefficient de pointe"),
    type_consommation: str = typer.Option("branchement_prive", "--type", "-t", help="Type de consommation"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails"),
    input_file: Optional[Path] = typer.Option(None, "--input", "-i", help="Fichier d'entrée YAML/JSON (active le mode enhanced par défaut)"),
    mode: str = typer.Option("auto", "--mode", "-M", help="Mode de calcul: auto|simple|enhanced"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Export: json|yaml|markdown|csv|html"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour l'export")
):
    """💧 Calcul de demande en eau unifié avec transparence mathématique
    
    Types de consommation:
    - branchement_prive: Branchement privé
    - borne_fontaine: Borne fontaine
    - industriel: Consommation industrielle
    
    Exemple:
    - lcpi aep demand-unified 1000 --dotation 150 --coeff-pointe 1.5
    - lcpi aep demand-unified --input data/demande.yml --export markdown
    
    Sortie standardisée: { valeurs, diagnostics, iterations }
    """
    try:
        use_enhanced = False
        if mode.lower() == "enhanced":
            use_enhanced = True
        elif mode.lower() == "simple":
            use_enhanced = False
        elif mode.lower() == "auto":
            use_enhanced = input_file is not None
        else:
            raise ValueError("--mode doit être parmi: auto|simple|enhanced")

        if use_enhanced:
            data = _load_input_file(input_file) if input_file else {
                "population": population,
                "dotation_l_hab_j": dotation_l_hab_j,
                "coefficient_pointe": coefficient_pointe,
                "type_consommation": type_consommation,
            }
            from .calculations.population_enhanced import calculate_water_demand_enhanced
            result = calculate_water_demand_enhanced(data)
        else:
            from .calculations.demand_unified import calculate_water_demand
            result = calculate_water_demand(
                population, dotation_l_hab_j, coefficient_pointe, type_consommation, verbose
            )

        if export or output:
            fmt = export or "json"
            diag_data = {
                "population": population,
            }
            diags = check_physical_constraints(diag_data)
            std = _make_result(result, diags, result.get("iterations") or result.get("nombre_iterations"))
            content = _export_generic(std, fmt)
            if output:
                output.write_text(content, encoding="utf-8")
                typer.echo(f"✅ Export sauvegardé: {output}")
            typer.echo(content)
            return

        if verbose:
            typer.echo(f"💧 Demande en eau:")
            typer.echo(f"  Population: {population}")
            typer.echo(f"  Dotation: {dotation_l_hab_j} L/hab/j")
            typer.echo(f"  Demande moyenne: {result.get('demande_moyenne', 0):.2f} m³/jour")
            typer.echo(f"  Demande de pointe: {result.get('demande_pointe', 0):.2f} m³/jour")
        else:
            dp = result.get('demande_pointe', 0)
            typer.echo(f"💧 {dp:.2f} m³/jour")

    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def network_unified(
    debit_m3s: float = typer.Argument(..., help="Débit en m³/s"),
    longueur_m: float = typer.Option(1000, "--longueur", "-l", help="Longueur en mètres"),
    materiau: str = typer.Option("fonte", "--materiau", "-m", help="Matériau de la conduite"),
    perte_charge_max_m: float = typer.Option(10.0, "--perte-max", "-p", help="Perte de charge maximale en m"),
    methode: str = typer.Option("darcy", "--methode", "-M", help="Méthode de calcul"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails"),
    input_file: Optional[Path] = typer.Option(None, "--input", "-i", help="Fichier d'entrée YAML/JSON (active le mode enhanced par défaut)"),
    mode: str = typer.Option("auto", "--mode", "-M", help="Mode de calcul: auto|simple|enhanced"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Export: json|yaml|markdown|csv|html"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour l'export")
):
    """🔧 Dimensionnement réseau unifié avec transparence mathématique
    
    Méthodes disponibles:
    - darcy: Formule de Darcy-Weisbach
    - hazen: Formule de Hazen-Williams
    - manning: Formule de Manning
    
    Exemple:
    - lcpi aep network-unified 0.1 --longueur 1000 --materiau fonte
    - lcpi aep network-unified --input data/reseau.yml --export yaml
    
    Sortie standardisée: { valeurs, diagnostics, iterations }
    """
    try:
        use_enhanced = False
        if mode.lower() == "enhanced":
            use_enhanced = True
        elif mode.lower() == "simple":
            use_enhanced = False
        elif mode.lower() == "auto":
            use_enhanced = input_file is not None
        else:
            raise ValueError("--mode doit être parmi: auto|simple|enhanced")

        if use_enhanced:
            data = _load_input_file(input_file) if input_file else {
                "debit_m3s": debit_m3s,
                "longueur_m": longueur_m,
                "materiau": materiau,
                "perte_charge_max_m": perte_charge_max_m,
                "methode": methode,
            }
            from .calculations.network_enhanced import dimension_network_enhanced
            result = dimension_network_enhanced(data)
        else:
            from .calculations.network_unified import dimension_network
            result = dimension_network(
                debit_m3s, longueur_m, materiau, perte_charge_max_m, methode, verbose
            )

        if export or output:
            fmt = export or "json"
            d = result.get('diametre') or result.get('diametre_optimal_m', None)
            diag_data = {
                "debit_m3s": debit_m3s,
                "longueur_m": longueur_m,
                **({"diametre_m": d} if d is not None else {}),
            }
            diags = check_physical_constraints(diag_data)
            std = _make_result(result, diags, result.get("iterations") or result.get("nombre_iterations"))
            content = _export_generic(std, fmt)
            if output:
                output.write_text(content, encoding="utf-8")
                typer.echo(f"✅ Export sauvegardé: {output}")
            typer.echo(content)
            return

        if verbose:
            typer.echo(f"🔧 Dimensionnement réseau:")
            typer.echo(f"  Débit: {debit_m3s} m³/s")
            typer.echo(f"  Diamètre: {result.get('diametre') or result.get('diametre_optimal_m', 0):.3f} m")
            typer.echo(f"  Vitesse: {result.get('vitesse') or result.get('vitesse_ms', 0):.2f} m/s")
            pc = result.get('perte_charge') or result.get('perte_charge_m', 0)
            typer.echo(f"  Perte de charge: {pc:.2f} m")
        else:
            d = result.get('diametre') or result.get('diametre_optimal_m', 0)
            v = result.get('vitesse') or result.get('vitesse_ms', 0)
            typer.echo(f"🔧 D={d:.3f}m, V={v:.2f}m/s")

    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def reservoir_unified(
    volume_journalier_m3: float = typer.Argument(..., help="Volume journalier en m³"),
    type_adduction: str = typer.Option("continue", "--adduction", "-a", help="Type d'adduction"),
    forme_reservoir: str = typer.Option("cylindrique", "--forme", "-f", help="Forme du réservoir"),
    type_zone: str = typer.Option("ville_francaise_peu_importante", "--zone", "-z", help="Type de zone"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails"),
    input_file: Optional[Path] = typer.Option(None, "--input", "-i", help="Fichier d'entrée YAML/JSON (active le mode enhanced par défaut)"),
    mode: str = typer.Option("auto", "--mode", "-M", help="Mode de calcul: auto|simple|enhanced"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Export: json|yaml|markdown|csv|html"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour l'export")
):
    """🏗️ Dimensionnement réservoir unifié avec transparence mathématique
    
    Types d'adduction:
    - continue: Adduction continue
    - discontinue: Adduction discontinue
    
    Formes disponibles:
    - cylindrique: Réservoir cylindrique
    - parallelepipedique: Réservoir parallélépipédique
    
    Exemple:
    - lcpi aep reservoir-unified 1000 --adduction continue --forme cylindrique
    - lcpi aep reservoir-unified --input data/reservoir.yml --export html
    
    Sortie standardisée: { valeurs, diagnostics, iterations }
    """
    try:
        use_enhanced = False
        if mode.lower() == "enhanced":
            use_enhanced = True
        elif mode.lower() == "simple":
            use_enhanced = False
        elif mode.lower() == "auto":
            use_enhanced = input_file is not None
        else:
            raise ValueError("--mode doit être parmi: auto|simple|enhanced")

        if use_enhanced:
            data = _load_input_file(input_file) if input_file else {
                "volume_journalier_m3": volume_journalier_m3,
                "type_zone": type_zone,
                "mode_adduction": "24h" if type_adduction == "continue" else "10h_nuit",
                "forme": forme_reservoir,
            }
            from .calculations.reservoir_enhanced import dimension_reservoir_enhanced
            result = dimension_reservoir_enhanced(data)
        else:
            from .calculations.reservoir_unified import dimension_reservoir
            result = dimension_reservoir(
                volume_journalier_m3, type_adduction, forme_reservoir, type_zone, verbose
            )

        if export or output:
            fmt = export or "json"
            std = _make_result(result, [], result.get("iterations") or result.get("nombre_iterations"))
            content = _export_generic(std, fmt)
            if output:
                output.write_text(content, encoding="utf-8")
                typer.echo(f"✅ Export sauvegardé: {output}")
            typer.echo(content)
            return

        if verbose:
            typer.echo(f"🏗️ Dimensionnement réservoir:")
            vu = result.get('volume_utile') or result.get('volume_utile_m3') or 0
            vt = result.get('volume_total') or result.get('capacite_totale_m3') or 0
            h = result.get('hauteur') or result.get('hauteur_m') or 0
            d = result.get('diametre') or result.get('diametre_m') or 0
            typer.echo(f"  Volume utile: {vu:.0f} m³")
            typer.echo(f"  Volume total: {vt:.0f} m³")
            typer.echo(f"  Hauteur: {h:.2f} m")
            typer.echo(f"  Diamètre: {d:.2f} m")
        else:
            vt = result.get('volume_total') or result.get('capacite_totale_m3') or 0
            h = result.get('hauteur') or result.get('hauteur_m') or 0
            typer.echo(f"🏗️ V={vt:.0f}m³, H={h:.2f}m")

    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def pumping_unified(
    debit_m3h: float = typer.Argument(..., help="Débit en m³/h"),
    hmt_m: float = typer.Option(50, "--hmt", "-h", help="Hauteur manométrique totale en m"),
    type_pompe: str = typer.Option("centrifuge", "--type", "-t", help="Type de pompe"),
    rendement_pompe: float = typer.Option(0.75, "--rendement", "-r", help="Rendement de la pompe"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails"),
    input_file: Optional[Path] = typer.Option(None, "--input", "-i", help="Fichier d'entrée YAML/JSON (active le mode enhanced par défaut)"),
    mode: str = typer.Option("auto", "--mode", "-M", help="Mode de calcul: auto|simple|enhanced"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Export: json|yaml|markdown|csv|html"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour l'export")
):
    """⚡ Dimensionnement pompage unifié avec transparence mathématique
    
    Types de pompes:
    - centrifuge: Pompe centrifuge
    - helice: Pompe à hélice
    - piston: Pompe à piston
    
    Exemple:
    - lcpi aep pumping-unified 100 --hmt 50 --type centrifuge
    - lcpi aep pumping-unified --input data/pompage.yml --export csv
    
    Sortie standardisée: { valeurs, diagnostics, iterations }
    """
    try:
        use_enhanced = False
        if mode.lower() == "enhanced":
            use_enhanced = True
        elif mode.lower() == "simple":
            use_enhanced = False
        elif mode.lower() == "auto":
            use_enhanced = input_file is not None
        else:
            raise ValueError("--mode doit être parmi: auto|simple|enhanced")

        if use_enhanced:
            data = _load_input_file(input_file) if input_file else {
                "debit_m3s": debit_m3h / 3600.0,
                "hauteur_manometrique_m": hmt_m,
                "type_pompe": type_pompe,
                "rendement_pompe": rendement_pompe,
            }
            from .calculations.pumping_enhanced import dimension_pumping_enhanced
            result = dimension_pumping_enhanced(data)
        else:
            from .calculations.pumping_unified import dimension_pumping
            result = dimension_pumping(
                debit_m3h, hmt_m, type_pompe, rendement_pompe, verbose
            )

        if export or output:
            fmt = export or "json"
            diag_data = {
                "debit_m3s": debit_m3h / 3600.0,
                "hmt_m": hmt_m,
            }
            diags = check_physical_constraints(diag_data)
            std = _make_result(result, diags, result.get("iterations") or result.get("nombre_iterations"))
            content = _export_generic(std, fmt)
            if output:
                output.write_text(content, encoding="utf-8")
                typer.echo(f"✅ Export sauvegardé: {output}")
            typer.echo(content)
            return

        if verbose:
            ph = result.get('puissance_hydraulique') or result.get('puissance_hydraulique_kw') or 0
            pe = result.get('puissance_electrique') or result.get('puissance_electrique_kw') or 0
            typer.echo(f"⚡ Dimensionnement pompage:")
            typer.echo(f"  Débit: {debit_m3h} m³/h")
            typer.echo(f"  HMT: {hmt_m} m")
            typer.echo(f"  Puissance hydraulique: {ph:.1f} kW")
            typer.echo(f"  Puissance électrique: {pe:.1f} kW")
        else:
            pe = result.get('puissance_electrique') or result.get('puissance_electrique_kw') or 0
            typer.echo(f"⚡ P={pe:.1f}kW")

    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

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
    
    Exemples:
    - lcpi aep query coefficients --material fonte --format json
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
        raise typer.Exit(code=1)

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
        raise typer.Exit(code=1)

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
        raise typer.Exit(code=1)

# =============================================================================
# COMMANDES HARDY-CROSS
# =============================================================================

@app.command()
def hardy_cross_csv(
    csv_path: Path = typer.Argument(..., help="Chemin vers le fichier CSV", exists=True, file_okay=True, dir_okay=False, readable=True),
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
        hardy_cross.load_network_data(network_data)
        resultat = hardy_cross.hardy_cross_iteration(network_data)
        
        if verbose:
            typer.echo(f"✅ Hardy-Cross terminé:")
            typer.echo(f"  Itérations: {resultat['nombre_iterations']}")
            typer.echo(f"  Tolérance finale: {resultat['tolerance_finale']:.2e}")
            typer.echo(f"  Temps: {resultat.get('temps', 0):.3f} s")
        
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
        raise typer.Exit(code=1)

@app.command()
def hardy_cross_yaml(
    yaml_path: Path = typer.Argument(..., help="Chemin vers le fichier YAML", exists=True, file_okay=True, dir_okay=False, readable=True),
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
        hardy_cross.load_network_data(network_data)
        resultat = hardy_cross.hardy_cross_iteration(network_data)
        
        if verbose:
            typer.echo(f"✅ Hardy-Cross terminé:")
            typer.echo(f"  Itérations: {resultat['nombre_iterations']}")
            typer.echo(f"  Tolérance finale: {resultat['tolerance_finale']:.2e}")
            typer.echo(f"  Temps: {resultat.get('temps', 0):.3f} s")
        
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
        raise typer.Exit(code=1)

# =============================================================================
# HARDY-CROSS UNIFIED
# =============================================================================

@app.command()
def hardy_cross_unified(
    input_file: Optional[Path] = typer.Option(None, "--input", "-i", help="Fichier d'entrée YAML/CSV"),
    tolerance: float = typer.Option(1e-6, "--tolerance", "-t", help="Tolérance de convergence"),
    max_iterations: int = typer.Option(100, "--iterations", "-n", help="Nombre maximum d'itérations"),
    formule: str = typer.Option("hazen_williams", "--formule", "-f", help="Formule de perte de charge"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Export: json|yaml|markdown|csv|html"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour l'export"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """🔄 Hardy-Cross unifié (inline ou via --input YAML/CSV) avec export générique.

    Exemples:
    - lcpi aep hardy-cross-unified --input reseau.yml --tolerance 1e-6 --export json
    - lcpi aep hardy-cross-unified --input reseau.csv --iterations 200 --export markdown
    
    Sortie standardisée: { valeurs, diagnostics, iterations }
    """
    try:
        from .calculations.hardy_cross_enhanced import HardyCrossEnhanced
        import yaml
        import pandas as pd

        if input_file is None:
            raise ValueError("--input est requis pour hardy_cross_unified (YAML ou CSV)")

        if input_file.suffix.lower() in {".yml", ".yaml"}:
            with open(input_file, "r", encoding="utf-8") as f:
                network_data = yaml.safe_load(f)
        elif input_file.suffix.lower() == ".csv":
            df = pd.read_csv(input_file)
            network_data = {
                "network": {
                    "nodes": {},
                    "pipes": {}
                }
            }
            all_nodes = set()
            for _, row in df.iterrows():
                all_nodes.add(row["from_node"])
                all_nodes.add(row["to_node"])
            for node in all_nodes:
                network_data["network"]["nodes"][node] = {"elevation": 0, "demand": 0.0}
            for _, row in df.iterrows():
                pipe_id = row["pipe_id"]
                network_data["network"]["pipes"][pipe_id] = {
                    "from_node": row["from_node"],
                    "to_node": row["to_node"],
                    "length": row["length"],
                    "diameter": row["diameter"],
                    "roughness": row["roughness"],
                    "initial_flow": row.get("initial_flow", 0.0),
                }
        else:
            raise ValueError("Format d'entrée non supporté. Utilisez YAML ou CSV.")

        hardy = HardyCrossEnhanced()
        hardy.load_network_data(network_data)
        results = hardy.hardy_cross_iteration(network_data)

        if verbose:
            typer.echo("🔄 Hardy-Cross unifié terminé")

        if export or output:
            fmt = export or "json"
            std = _make_result(results, [], results.get("iterations") or results.get("nombre_iterations"))
            content = _export_generic(std, fmt)
            if output:
                output.write_text(content, encoding="utf-8")
                typer.echo(f"✅ Export sauvegardé: {output}")
            typer.echo(content)
            return
        typer.echo(_export_generic(_make_result(results, [], results.get("iterations") or results.get("nombre_iterations")), "json"))

    except Exception as e:
        typer.echo(f"❌ Erreur: {e}", err=True)
        raise typer.Exit(code=1)

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
            "original_file": str(inp_file_path)
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

def _export_hardy_cross_markdown(resultat):
    """Exporte les résultats Hardy-Cross en Markdown"""
    typer.echo("# Résultats Hardy-Cross")
    typer.echo(f"\n## Convergence")
    typer.echo(f"- Itérations: {resultat['iterations']}")
    typer.echo(f"- Tolérance finale: {resultat['tolerance']:.2e}")
    typer.echo(f"- Temps: {resultat['temps']:.3f} s")
    
    if 'flows' in resultat:
        typer.echo(f"\n## Débits des conduites")
        for pipe_id, flow in resultat['flows'].items():
            typer.echo(f"- {pipe_id}: {flow:.4f} m³/s")

def _export_hardy_cross_csv(resultat):
    """Exporte les résultats Hardy-Cross en CSV"""
    typer.echo("pipe_id,flow_m3s")
    if 'flows' in resultat:
        for pipe_id, flow in resultat['flows'].items():
            typer.echo(f"{pipe_id},{flow:.4f}")

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

# =============================================================================
# COMMANDES WORKFLOW COMPLET
# =============================================================================

@app.command()
def validate_input(
    input_file: Path = typer.Argument(..., help="Fichier d'entrée YAML/JSON"),
    data_type: str = typer.Option("auto", "--type", "-t", help="Type de données: auto|population|demand|network|reservoir|pumping|protection"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Export: json|yaml|markdown|csv|html"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour l'export")
):
    """🧪 Valide un fichier d'entrée AEP (Phase 0).

    Détecte le type automatiquement si --type=auto.

    Sortie standardisée: { valeurs, diagnostics }
    """
    try:
        import yaml
        with open(input_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) if input_file.suffix.lower() in {'.yml', '.yaml'} else json.load(f)

        detected = data_type
        if data_type == "auto":
            # Détection simple basée sur les clés
            if isinstance(data, dict) and 'network' in data:
                detected = 'network_unified'
            elif isinstance(data, dict) and {'population_base','taux_croissance','annees'} <= set(data.keys()):
                detected = 'population_unified'
            elif isinstance(data, dict) and {'population','dotation_l_hab_j'} <= set(data.keys()):
                detected = 'demand_unified'
            elif isinstance(data, dict) and {'volume_journalier_m3'} <= set(data.keys()):
                detected = 'reservoir_unified'
            elif isinstance(data, dict) and {'debit_m3s','hmt_m'} & set(data.keys()):
                detected = 'pumping_unified'
            else:
                detected = 'population_unified'

        cleaned = validate_and_clean_data(data, detected)
        diagnostics = check_physical_constraints(cleaned)
        std = _make_result(cleaned, diagnostics)

        if export or output:
            fmt = export or 'json'
            content = _export_generic(std, fmt)
            if output:
                output.write_text(content, encoding='utf-8')
                typer.echo(f"✅ Export sauvegardé: {output}")
            typer.echo(content)
            return

        typer.echo(_export_generic(std, 'json'))

    except Exception as e:
        typer.echo(f"❌ Erreur de validation: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def validate_population(
    input_file: Path = typer.Argument(..., help="YAML/JSON de population unifiée (population_base, taux, annees, methode)"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Export: json|yaml|markdown|csv|html"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour l'export")
):
    """🧪 Valide les données de population (unified)."""
    try:
        import yaml
        with open(input_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) if input_file.suffix.lower() in {'.yml', '.yaml'} else json.load(f)
        cleaned = validate_population_unified_data(data)
        diagnostics = check_physical_constraints(cleaned)
        std = _make_result(cleaned, diagnostics)
        if export or output:
            fmt = export or 'json'
            content = _export_generic(std, fmt)
            if output:
                output.write_text(content, encoding='utf-8')
                typer.echo(f"✅ Export sauvegardé: {output}")
            typer.echo(content)
            return
        typer.echo(_export_generic(std, 'json'))
    except Exception as e:
        typer.echo(f"❌ Erreur de validation population: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def validate_network(
    input_file: Path = typer.Argument(..., help="YAML/JSON de réseau unifié (debit_m3s, longueur_m, materiau, ...)"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Export: json|yaml|markdown|csv|html"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier de sortie pour l'export")
):
    """🧪 Valide les données de réseau (unified)."""
    try:
        import yaml
        with open(input_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) if input_file.suffix.lower() in {'.yml', '.yaml'} else json.load(f)
        cleaned = validate_network_unified_data(data)
        diagnostics = check_physical_constraints(cleaned)
        std = _make_result(cleaned, diagnostics)
        if export or output:
            fmt = export or 'json'
            content = _export_generic(std, fmt)
            if output:
                output.write_text(content, encoding='utf-8')
                typer.echo(f"✅ Export sauvegardé: {output}")
            typer.echo(content)
            return
        typer.echo(_export_generic(std, 'json'))
    except Exception as e:
        typer.echo(f"❌ Erreur de validation réseau: {e}", err=True)
        raise typer.Exit(code=1)
def convert_inp(
    inp_file: Path = typer.Argument(..., help="Chemin vers le fichier .inp EPANET", exists=True, file_okay=True, dir_okay=False, readable=True),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Fichier YAML de sortie (optionnel)"),
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
        
        if verbose:
            typer.echo(f"📁 Lecture du fichier .inp: {inp_file}")
        
        # Parser le fichier .inp
        network_data = _parse_inp_file(inp_file)
        if not network_data:
            typer.echo("❌ Échec du parsing du fichier .inp")
            raise typer.Exit(code=1)
        
        # Générer le nom du fichier YAML
        if output_file:
            yaml_path = output_file
        else:
            yaml_path = inp_file.with_suffix('.yml')
        
        # Sauvegarder en YAML
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(network_data, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        typer.echo(f"✅ Fichier YAML créé: {yaml_path}")
        typer.echo(f"📊 Nœuds: {len(network_data['network']['nodes'])}, Conduites: {len(network_data['network']['pipes'])}")
        
        # Simuler si demandé
        if simulate:
            typer.echo("\n🚀 SIMULATION AVEC LCPI AEP")
            try:
                # Import direct pour éviter les problèmes d'import circulaire
                import sys
                import os
                current_dir = os.path.dirname(os.path.abspath(__file__))
                core_dir = os.path.join(current_dir, "core")
                sys.path.insert(0, core_dir)
                
                from epanet_integration import run_epanet_with_diagnostics
                results = run_epanet_with_diagnostics(network_data)
            except ImportError as e:
                typer.echo(f"❌ ERREUR: Module EPANET non trouvé: {e}")
                raise typer.Exit(code=1)
            
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
        raise typer.Exit(code=1)

@app.command()
def diagnose_network(
    network_file: Path = typer.Argument(..., help="Fichier YAML/JSON avec les données du réseau", exists=True, file_okay=True, dir_okay=False, readable=True),
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
        
        # Charger les données
        with open(network_file, 'r', encoding='utf-8') as f:
            network_data = yaml.safe_load(f)
        
        if verbose:
            typer.echo(f"🔍 DIAGNOSTIC RÉSEAU: {network_file}")
        
        # Diagnostic de connectivité
        try:
            # Import dynamique avec importlib
            import importlib.util
            import os
            import sys
            
            # Chemin vers les modules
            current_dir = os.path.dirname(os.path.abspath(__file__))
            core_dir = os.path.join(current_dir, "core")
            
            # Ajouter le répertoire core au path pour les imports relatifs
            if core_dir not in sys.path:
                sys.path.insert(0, core_dir)
            
            # Charger network_utils d'abord
            network_utils_path = os.path.join(core_dir, "network_utils.py")
            spec_utils = importlib.util.spec_from_file_location("network_utils", network_utils_path)
            network_utils = importlib.util.module_from_spec(spec_utils)
            spec_utils.loader.exec_module(network_utils)
            
            # Charger network_diagnostics
            network_diagnostics_path = os.path.join(core_dir, "network_diagnostics.py")
            spec_diagnostics = importlib.util.spec_from_file_location("network_diagnostics", network_diagnostics_path)
            network_diagnostics = importlib.util.module_from_spec(spec_diagnostics)
            spec_diagnostics.loader.exec_module(network_diagnostics)
            
            # Utiliser les fonctions du module
            is_connected = network_diagnostics.diagnose_network_connectivity(network_data)
            validation = network_diagnostics.validate_epanet_compatibility(network_data)
            topology = network_diagnostics.analyze_network_topology(network_data)
            
        except Exception as e:
            typer.echo(f"❌ ERREUR: Module diagnostic non trouvé: {e}")
            raise typer.Exit(code=1)
        
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
        raise typer.Exit(code=1)

@app.command()
def workflow_complete(
    network_file: Path = typer.Argument(..., help="Fichier YAML/JSON avec les données du réseau", exists=True, file_okay=True, dir_okay=False, readable=True),
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Répertoire de sortie"),
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
        
        if verbose:
            typer.echo(f"🚀 WORKFLOW AEP COMPLET: {network_file}")
        
        # Charger les données
        with open(network_file, 'r', encoding='utf-8') as f:
            network_data = yaml.safe_load(f)
        
        # 1. Diagnostic
        typer.echo("🔍 ÉTAPE 1: DIAGNOSTIC")
        try:
            # Import dynamique avec importlib
            import importlib.util
            import os
            
            # Chemin vers le module network_diagnostics
            current_dir = os.path.dirname(os.path.abspath(__file__))
            network_diagnostics_path = os.path.join(current_dir, "core", "network_diagnostics.py")
            
            # Charger le module dynamiquement
            spec = importlib.util.spec_from_file_location("network_diagnostics", network_diagnostics_path)
            network_diagnostics = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(network_diagnostics)
            
            # Utiliser les fonctions du module
            is_connected = network_diagnostics.diagnose_network_connectivity(network_data)
            
            if not is_connected:
                typer.echo("❌ Réseau non connecté - arrêt du workflow")
                raise typer.Exit(code=1)
        except Exception as e:
            typer.echo(f"❌ ERREUR: Module diagnostic non trouvé: {e}")
            raise typer.Exit(code=1)
        
        # 2. Hardy-Cross
        typer.echo("⚡ ÉTAPE 2: HARDY-CROSS")
        try:
            from .calculations.hardy_cross_enhanced import HardyCrossEnhanced
            hardy_cross = HardyCrossEnhanced()
            
            # Convertir le format des données pour Hardy-Cross
            hardy_network_data = _convert_to_hardy_cross_format(network_data)
            
            # Charger les données et exécuter Hardy-Cross
            hardy_cross.load_network_data(hardy_network_data)
            hardy_results = hardy_cross.hardy_cross_iteration(hardy_network_data)
            
            if verbose:
                typer.echo(f"✅ Hardy-Cross: {hardy_results['nombre_iterations']} itérations, tolérance {hardy_results['tolerance_finale']:.2e}")
        except ImportError as e:
            typer.echo(f"❌ ERREUR: Module Hardy-Cross non trouvé: {e}")
            raise typer.Exit(code=1)
        
        # 3. EPANET avec diagnostics
        typer.echo("🌐 ÉTAPE 3: EPANET")
        try:
            # Import dynamique avec importlib
            import importlib.util
            import os
            
            # Chemin vers le module epanet_integration
            current_dir = os.path.dirname(os.path.abspath(__file__))
            epanet_integration_path = os.path.join(current_dir, "core", "epanet_integration.py")
            
            # Charger le module dynamiquement
            spec = importlib.util.spec_from_file_location("epanet_integration", epanet_integration_path)
            epanet_integration = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(epanet_integration)
            
            # Utiliser les fonctions du module
            epanet_results = epanet_integration.run_epanet_with_diagnostics(network_data)
        except Exception as e:
            typer.echo(f"❌ ERREUR: Module EPANET non trouvé: {e}")
            raise typer.Exit(code=1)
        
        if not epanet_results['success']:
            typer.echo("❌ Échec EPANET - arrêt du workflow")
            raise typer.Exit(code=1)
        
        # 4. Comparaison (si demandée)
        if compare_methods:
            typer.echo("🔄 ÉTAPE 4: COMPARAISON")
            comparison = _compare_results(hardy_results, epanet_results)
            
            if verbose:
                typer.echo(f"📊 Écart moyen pressions: {comparison['mean_pressure_diff']:.2f} m")
        
        # 5. Rapports (si demandés)
        if generate_reports:
            typer.echo("📋 ÉTAPE 5: RAPPORTS")
            output_path = output_dir or network_file.parent / "output"
            output_path.mkdir(exist_ok=True)
            
            _generate_workflow_reports(
                network_data, hardy_results, epanet_results, 
                comparison if compare_methods else None,
                output_path
            )
            
            typer.echo(f"✅ Rapports générés dans: {output_path}")
        
        typer.echo("🎉 WORKFLOW AEP COMPLET TERMINÉ AVEC SUCCÈS!")
        
    except Exception as e:
        typer.echo(f"❌ ERREUR: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def simulate_inp(
    inp_file: Path = typer.Argument(..., help="Chemin vers le fichier .inp EPANET", exists=True, file_okay=True, dir_okay=False, readable=True),
    output_format: str = typer.Option("json", "--format", "-f", help="Format de sortie (json, markdown, csv)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Afficher les détails")
):
    """🌐 Simule un fichier .inp EPANET avec LCPI AEP
    
    Exécute une simulation hydraulique complète d'un réseau d'eau potable
    en utilisant le moteur de calcul EPANET à partir d'un fichier .inp existant.
    
    **Structure du fichier .inp EPANET :**
    ```inp
    [TITLE]
    Exemple de réseau AEP
    
    [JUNCTIONS]
    ID              Elev        Demand       Pattern       Comment
    N1              150.0       0.0                         Réservoir
    N2              145.0       0.02                        Consommation
    
    [RESERVOIRS]
    ID              Head        Pattern       Comment
    R1              160.0                                    Source d'eau
    
    [PIPES]
    ID              Node1       Node2        Length        Diameter      Roughness      Status
    P1              R1          N1           500           0.2           100            Open
    P2              N1          N2           300           0.15          100            Open
    
    [PATTERNS]
    ID              Multipliers
    Pattern1        1.0         1.2         1.5         1.8         2.0         1.8
    ```
    
    **Exemple d'utilisation :**
    ```bash
    lcpi aep simulate-inp data/reseau.inp --format json --verbose
    lcpi aep simulate-inp data/reseau.inp --format markdown
    lcpi aep simulate-inp data/reseau.inp --format csv
    ```
    
    **Formats de sortie disponibles :**
    - **json**: Données structurées JSON - Facile à traiter programmatiquement
    - **markdown**: Rapport formaté Markdown - Lisible et bien structuré
    - **csv**: Données tabulaires CSV - Compatible avec Excel et autres outils
    
    **Résultats fournis :**
    - Débits dans chaque conduite
    - Pressions à chaque nœud
    - Vitesses d'écoulement
    - Pertes de charge
    - Statistiques de convergence
    - Analyse de la qualité de l'eau (si configurée)
    """
    try:
        from .epanet_wrapper import EpanetSimulator
        
        if verbose:
            typer.echo(f"🚀 SIMULATION FICHIER .INP: {inp_file}")
        
        # Créer l'instance EPANET
        epanet = EpanetSimulator()
        
        # Ouvrir le fichier .inp
        if not epanet.open_project(str(inp_file)):
            typer.echo("❌ ERREUR: Impossible d'ouvrir le fichier .inp")
            raise typer.Exit(code=1)
        
        if verbose:
            typer.echo("✅ Fichier .inp ouvert avec succès")
        
        # Lancer la simulation hydraulique
        if not epanet.solve_hydraulics():
            typer.echo("❌ ERREUR: Échec de la simulation hydraulique")
            raise typer.Exit(code=1)
        
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
        raise typer.Exit(code=1)

def _convert_to_hardy_cross_format(network_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convertit le format LCPI vers le format Hardy-Cross"""
    hardy_data = {
        "noeuds": [],
        "troncons": [],
        "boucles": []
    }
    
    # Convertir les nœuds
    if "network" in network_data and "nodes" in network_data["network"]:
        for node_id, node_data in network_data["network"]["nodes"].items():
            noeud = {
                "id": node_id,
                "cote": node_data.get("elevation", 0),
                "demande": node_data.get("demand", 0)
            }
            hardy_data["noeuds"].append(noeud)
    
    # Convertir les conduites en tronçons
    if "network" in network_data and "pipes" in network_data["network"]:
        for pipe_id, pipe_data in network_data["network"]["pipes"].items():
            troncon = {
                "id": pipe_id,
                "noeud_debut": pipe_data.get("from_node", ""),
                "noeud_fin": pipe_data.get("to_node", ""),
                "longueur": pipe_data.get("length", 0),
                "diametre": pipe_data.get("diameter", 0),
                "coefficient_rugosite": pipe_data.get("roughness", 120),
                "debit_initial": pipe_data.get("initial_flow", 0)
            }
            hardy_data["troncons"].append(troncon)
    
    return hardy_data

# =============================================================================
# NOUVELLES COMMANDES POUR LES MODULES DES SUGGESTIONS
# =============================================================================

# Import des nouveaux modules
from .core.database import AEPDatabase
from .core.import_automatique import AEPImportAutomatique
from .core.validation_donnees import AEPDataValidator
from .core.recalcul_automatique import AEPRecalculEngine, TypeRecalcul

@app.command()
def database(
    action: str = typer.Argument(..., help="Action à effectuer: init, info, add-project, add-survey, list, search, export, clean"),
    db_path: str = typer.Option("aep_database.db", "--db", "-d", help="Chemin vers la base de données"),
    project_name: str = typer.Option(None, "--name", "-n", help="Nom du projet"),
    description: str = typer.Option(None, "--desc", help="Description du projet"),
    metadata: str = typer.Option(None, "--metadata", help="Métadonnées JSON"),
    search_term: str = typer.Option(None, "--search", help="Terme de recherche"),
    project_id: int = typer.Option(None, "--id", help="ID du projet"),
    export_format: str = typer.Option("json", "--format", help="Format d'export (json/yaml)"),
    output_file: str = typer.Option(None, "--output", "-o", help="Fichier de sortie"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux")
):
    """Gestion de la base de données centralisée AEP"""
    try:
        db = AEPDatabase(db_path)
        
        if action == "init":
            # Initialisation déjà faite dans le constructeur
            typer.echo(f"✅ Base de données initialisée: {db_path}")
            
        elif action == "info":
            info = db.obtenir_info_base()
            if verbose:
                typer.echo(f"📊 Informations de la base de données:")
                typer.echo(f"   Chemin: {info['chemin']}")
                typer.echo(f"   Taille: {info['taille_fichier']} octets")
                typer.echo(f"   Tables: {', '.join(info['tables'])}")
            else:
                typer.echo(f"Base: {info['chemin']} ({info['taille_fichier']} octets)")
                
        elif action == "add-project":
            if not project_name:
                typer.echo("❌ Nom du projet requis")
                raise typer.Exit(1)
                
            metadata_dict = {}
            if metadata:
                try:
                    metadata_dict = json.loads(metadata)
                except json.JSONDecodeError:
                    typer.echo("❌ Métadonnées JSON invalides")
                    raise typer.Exit(1)
            
            projet_id = db.ajouter_projet(project_name, description or "", metadata_dict)
            typer.echo(f"✅ Projet ajouté avec ID: {projet_id}")
            
        elif action == "list":
            projets = db.obtenir_projets()
            if verbose:
                for projet in projets:
                    typer.echo(f"📁 Projet {projet['id']}: {projet['nom']}")
                    typer.echo(f"   Description: {projet['description']}")
                    typer.echo(f"   Créé: {projet['date_creation']}")
                    typer.echo()
            else:
                for projet in projets:
                    typer.echo(f"{projet['id']}: {projet['nom']}")
                    
        elif action == "search":
            if not search_term or not project_id:
                typer.echo("❌ Terme de recherche et ID de projet requis")
                raise typer.Exit(1)
                
            resultats = db.rechercher_donnees(project_id, search_term)
            typer.echo(f"🔍 Résultats pour '{search_term}' dans le projet {project_id}:")
            typer.echo(f"   Relevés: {len(resultats['releves'])}")
            typer.echo(f"   Calculs: {len(resultats['resultats_calculs'])}")
            
        elif action == "export":
            if not project_id:
                typer.echo("❌ ID de projet requis")
                raise typer.Exit(1)
                
            export_data = db.exporter_projet(project_id, export_format)
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(export_data)
                typer.echo(f"✅ Projet exporté vers: {output_file}")
            else:
                typer.echo(export_data)
                
        elif action == "clean":
            if not project_id:
                typer.echo("❌ ID de projet requis")
                raise typer.Exit(1)
                
            stats = db.nettoyer_projet(project_id)
            typer.echo(f"🧹 Nettoyage terminé:")
            typer.echo(f"   Supprimés: {stats['supprimes']}")
            typer.echo(f"   Conservés: {stats['conserves']}")
            
        else:
            typer.echo(f"❌ Action inconnue: {action}")
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"❌ Erreur: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        raise typer.Exit(1)

@app.command()
def import_data(
    file_path: str = typer.Argument(..., help="Chemin vers le fichier à importer"),
    import_type: str = typer.Argument(..., help="Type d'import: forages, pompes, reservoirs, constantes, enquetes"),
    db_path: str = typer.Option("aep_database.db", "--db", "-d", help="Chemin vers la base de données"),
    project_id: int = typer.Option(..., "--project", "-p", help="ID du projet"),
    template: bool = typer.Option(False, "--template", help="Générer un template"),
    validate: bool = typer.Option(False, "--validate", help="Valider le fichier sans importer"),
    output_file: str = typer.Option(None, "--output", "-o", help="Fichier de sortie pour le rapport"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux")
):
    """Import automatique de données depuis Excel/CSV"""
    try:
        db = AEPDatabase(db_path)
        importateur = AEPImportAutomatique(db)
        
        if template:
            if not output_file:
                output_file = f"template_{import_type}.xlsx"
            success = importateur.generer_template(import_type, output_file)
            if success:
                typer.echo(f"✅ Template généré: {output_file}")
            else:
                typer.echo("❌ Erreur lors de la génération du template")
                raise typer.Exit(1)
            return
            
        if validate:
            resultat = importateur.valider_fichier(file_path, import_type)
            if resultat["valide"]:
                typer.echo(f"✅ Fichier valide: {resultat['statistiques']['lignes']} lignes")
                if verbose:
                    typer.echo(f"   Colonnes: {resultat['statistiques']['colonnes']}")
            else:
                typer.echo(f"❌ Fichier invalide: {resultat['erreur']}")
                raise typer.Exit(1)
            return
            
        # Import effectif
        resultat = importateur.importer_fichier(file_path, import_type, project_id)
        
        if output_file:
            rapport = importateur.generer_rapport_import(resultat, import_type)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(rapport)
            typer.echo(f"📄 Rapport d'import sauvegardé: {output_file}")
        
        # Affichage du résumé
        taux_succes = (resultat["importes"] / (resultat["importes"] + resultat["erreurs"])) * 100 if (resultat["importes"] + resultat["erreurs"]) > 0 else 0
        
        if verbose:
            typer.echo(f"📊 Résumé de l'import:")
            typer.echo(f"   Importés: {resultat['importes']}")
            typer.echo(f"   Erreurs: {resultat['erreurs']}")
            typer.echo(f"   Taux de succès: {taux_succes:.1f}%")
            
            for detail in resultat["details"]:
                status = "✅" if detail["type"] == "succes" else "❌"
                typer.echo(f"   {status} Ligne {detail['ligne']}: {detail['message']}")
        else:
            typer.echo(f"✅ Import terminé: {resultat['importes']} importés, {resultat['erreurs']} erreurs ({taux_succes:.1f}%)")
            
    except Exception as e:
        typer.echo(f"❌ Erreur: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        raise typer.Exit(1)

@app.command()
def validate_project(
    project_id: int = typer.Argument(..., help="ID du projet à valider"),
    db_path: str = typer.Option("aep_database.db", "--db", "-d", help="Chemin vers la base de données"),
    output_file: str = typer.Option(None, "--output", "-o", help="Fichier de sortie pour le rapport"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux")
):
    """Validation des données d'un projet"""
    try:
        db = AEPDatabase(db_path)
        validateur = AEPDataValidator(db)
        
        # Validation complète du projet
        resultat = validateur.valider_projet_complet(project_id)
        
        # Génération du rapport
        rapport = validateur.generer_rapport_validation(resultat, project_id)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(rapport)
            typer.echo(f"📄 Rapport de validation sauvegardé: {output_file}")
        else:
            typer.echo(rapport)
        
        # Affichage du résumé
        if resultat.valide:
            typer.echo(f"✅ Projet valide")
        else:
            typer.echo(f"❌ Projet invalide: {len(resultat.erreurs)} erreurs")
            
        if verbose:
            typer.echo(f"   Erreurs: {len(resultat.erreurs)}")
            typer.echo(f"   Avertissements: {len(resultat.avertissements)}")
            
        # Recommandations
        recommandations = validateur.obtenir_recommandations(project_id)
        if recommandations:
            typer.echo(f"💡 Recommandations:")
            for rec in recommandations:
                typer.echo(f"   - {rec}")
                
    except Exception as e:
        typer.echo(f"❌ Erreur: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        raise typer.Exit(1)

@app.command()
def recalcul(
    action: str = typer.Argument(..., help="Action: add, execute, status, clean"),
    recalcul_type: str = typer.Option(None, "--type", help="Type de recalcul: population, hardy_cross, reservoir, pumping, demand, network"),
    project_id: int = typer.Option(None, "--project", "-p", help="ID du projet"),
    parameters: str = typer.Option(None, "--params", help="Paramètres JSON"),
    cascade: bool = typer.Option(False, "--cascade", help="Déclencher un recalcul en cascade"),
    db_path: str = typer.Option("aep_database.db", "--db", "-d", help="Chemin vers la base de données"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux")
):
    """Moteur de recalcul automatique"""
    try:
        db = AEPDatabase(db_path)
        moteur = AEPRecalculEngine(db)
        
        if action == "add":
            if not recalcul_type or not project_id or not parameters:
                typer.echo("❌ Type, projet et paramètres requis")
                raise typer.Exit(1)
                
            try:
                params_dict = json.loads(parameters)
            except json.JSONDecodeError:
                typer.echo("❌ Paramètres JSON invalides")
                raise typer.Exit(1)
                
            # Conversion du type
            type_map = {
                "population": TypeRecalcul.POPULATION,
                "hardy_cross": TypeRecalcul.HARDY_CROSS,
                "reservoir": TypeRecalcul.RESERVOIR,
                "pumping": TypeRecalcul.POMPING,
                "demand": TypeRecalcul.DEMAND,
                "network": TypeRecalcul.NETWORK
            }
            
            if recalcul_type not in type_map:
                typer.echo(f"❌ Type de recalcul inconnu: {recalcul_type}")
                raise typer.Exit(1)
                
            if cascade:
                taches = moteur.declencher_recalcul_cascade(type_map[recalcul_type], project_id, params_dict)
                typer.echo(f"✅ Recalcul en cascade déclenché: {len(taches)} tâches créées")
            else:
                task_id = moteur.ajouter_tache_recalcul(type_map[recalcul_type], project_id, params_dict)
                typer.echo(f"✅ Tâche de recalcul ajoutée: {task_id}")
                
        elif action == "execute":
            import asyncio
            resultats = asyncio.run(moteur.executer_taches_en_attente())
            
            if verbose:
                typer.echo(f"📊 Résultats de l'exécution:")
                typer.echo(f"   Tâches exécutées: {resultats['taches_executees']}")
                typer.echo(f"   Erreurs: {resultats['erreurs']}")
                
                for detail in resultats["details"]:
                    status = "✅" if detail["statut"] == "succes" else "❌"
                    typer.echo(f"   {status} {detail['tache_id']}: {detail['message']}")
            else:
                typer.echo(f"✅ Exécution terminée: {resultats['taches_executees']} tâches, {resultats['erreurs']} erreurs")
                
        elif action == "status":
            statut = moteur.obtenir_statut_taches()
            
            if verbose:
                typer.echo(f"📊 Statut des tâches:")
                typer.echo(f"   En attente: {statut['taches_en_attente']}")
                typer.echo(f"   Par priorité: {statut['taches_par_priorite']}")
                typer.echo(f"   Par type: {statut['taches_par_type']}")
            else:
                typer.echo(f"Tâches en attente: {statut['taches_en_attente']}")
                
        elif action == "clean":
            moteur.nettoyer_taches_terminees()
            typer.echo("✅ Tâches terminées nettoyées")
            
        else:
            typer.echo(f"❌ Action inconnue: {action}")
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"❌ Erreur: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        raise typer.Exit(1)

# =============================================================================
# POINT D'ENTRÉE PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    app()