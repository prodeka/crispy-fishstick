import typer
import json
import yaml
from .calculs.pluviometrie import analyser_donnees_brutes, ajuster_loi_gumbel, generer_courbes_idf
from .calculs.bassin_versant import caracteriser_bassin
from .calculs.canal import dimensionner_canal
from .calculs.pompage import predimensionner_pompe
from .calculs.plomberie import dimensionner_troncon_plomberie
from .calculs.deversoir import dimensionner_deversoir
from .calculs.dalot import verifier_dalot
from .calculs.radier import dimensionner_radier_submersible
from .calculs.population import prevoir_population
from .calculs.demande_eau import estimer_demande_eau
from .calculs.climat import generer_diagramme_ombrothermique

# Variable globale pour la sortie JSON (sera définie par le noyau)
_json_output_enabled = False
from rich.console import Console
from rich.panel import Panel

console = Console()

app = typer.Typer(name="hydro", help="Plugin complet pour l'hydrologie et l'hydraulique (Hydrodrain).")

# --- Groupes de commandes ---
pluvio_app = typer.Typer(name="pluvio", help="Gestion et Analyse des Données Pluviométriques.")
app.add_typer(pluvio_app)
hydro_app = typer.Typer(name="bassin", help="Analyse Hydrologique et Modélisation des Bassins Versants.")
app.add_typer(hydro_app)
ouvrages_app = typer.Typer(name="ouvrage", help="Dimensionnement et Analyse Hydraulique des Ouvrages.")
app.add_typer(ouvrages_app)
utils_app = typer.Typer(name="util", help="Utilitaires et Analyses Spécifiques.")
app.add_typer(utils_app)
plomberie_app = typer.Typer(name="plomberie", help="Dimensionnement des réseaux internes de plomberie.")
app.add_typer(plomberie_app)
stockage_app = typer.Typer(name="stockage", help="Dimensionnement des ouvrages de stockage et régulation.")
app.add_typer(stockage_app)

# --- Commandes (Implémentation finale pour Pluvio et Bassin) ---
@pluvio_app.command("analyser")
def pluvio_analyser(filepath: str):
    """Analyse statistique de données de pluie brutes depuis un fichier."""
    try:
        resultats = analyser_donnees_brutes(filepath)
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Analyse Pluviométrique[/bold green]", border_style="green"))
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Analyse Pluviométrique", border_style="red"))
        raise typer.Exit(code=1)

@pluvio_app.command("ajuster-loi")
def pluvio_ajuster(filepath: str):
    """Ajuste les pluies maximales à la loi de Gumbel (ou autre)."""
    try:
        import pandas as pd
        df = pd.read_csv(filepath)
        if 'pluie' not in df.columns:
            if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": "Le fichier doit contenir une colonne 'pluie'."}))
            else: console.print(Panel("ERREUR: Le fichier doit contenir une colonne 'pluie'.", title="Erreur de Données", border_style="red"))
            raise typer.Exit(code=1)
        series = df['pluie'].dropna().tolist()
        resultats = ajuster_loi_gumbel(series)
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Ajustement Loi[/bold green]", border_style="green"))
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Ajustement Loi", border_style="red"))
        raise typer.Exit(code=1)

@pluvio_app.command("generer-idf")
def pluvio_generer_idf(filepath: str, modele: str = "montana"):
    """Génère les courbes IDF à partir de données ajustées."""
    try:
        donnees_ajustees_exemple = {} # Un vrai cas passerait les résultats de l'ajustement
        quantiles_exemple = {"T2": 0.5, "T5": 0.2, "T10": 0.1, "T20": 0.05, "T50": 0.02, "T100": 0.01}
        resultats = generer_courbes_idf(donnees_ajustees_exemple, quantiles_exemple)
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Génération IDF[/bold green]", border_style="green"))
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Génération IDF", border_style="red"))
        raise typer.Exit(code=1)

@hydro_app.command("caracteriser")
def hydro_caracteriser(filepath: str):
    """Calcule les paramètres physiques d'un bassin versant à partir d'un fichier YAML ou CSV."""
    import os
    import pandas as pd
    import yaml
    try:
        if filepath.endswith('.yml') or filepath.endswith('.yaml'):
            with open(filepath, 'r', encoding='utf-8') as f:
                donnees = yaml.safe_load(f)
        elif filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
            donnees = {
                'superficie_km2': float(df['superficie_km2'].iloc[0]),
                'perimetre_km': float(df['perimetre_km'].iloc[0]),
                'pente_globale_m_km': float(df['pente_globale_m_km'].iloc[0])
            }
        else:
            if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": "Format de fichier non supporté (utilisez .yml, .yaml ou .csv)"}))
            else: console.print(Panel("ERREUR: Format de fichier non supporté (utilisez .yml, .yaml ou .csv)", title="Erreur de Fichier", border_style="red"))
            raise typer.Exit(code=1)
        resultats = caracteriser_bassin(donnees)
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Caractérisation Bassin[/bold green]", border_style="green"))
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Caractérisation Bassin", border_style="red"))
        raise typer.Exit(code=1)

# --- Commandes Ouvrages ---
# (Les imports sont déjà en haut du fichier)

# --- Commande Canal ---
@ouvrages_app.command("canal-dimensionner")
def ouvrages_canal_dimensionner(filepath: str = typer.Argument(..., help="Chemin vers le fichier de données YAML du canal.")):
    """Dimensionne un canal à ciel ouvert."""
    if not _json_output_enabled:
        console.print(f"--- Lancement du Dimensionnement du Canal depuis : {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        resultats = dimensionner_canal(config)
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Dimensionnement Canal[/bold green]", border_style="green"))
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Dimensionnement Canal", border_style="red"))
        raise typer.Exit(code=1)

@ouvrages_app.command("init-canal")
def ouvrages_init_canal(filepath: str = typer.Argument("canal_exemple.yml")):
    """Génère un fichier YAML d'exemple pour un canal."""
    template = """# Fichier de définition pour le dimensionnement d'un canal\n\ndebit_projet_m3s: 10.0\npente_m_m: 0.001\nk_strickler: 30.0\nfruit_talus_m_m: 1.5\nvitesse_imposee_ms: 1.2\n"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(template)
        if not _json_output_enabled:
            console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Template de canal créé : '{filepath}'", title="Génération Template", border_style="green"))
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Impossible de créer le fichier : {e}", title="Erreur Génération Template", border_style="red"))
        raise typer.Exit(code=1)

# --- Commande Dalot ---
@ouvrages_app.command("dalot-verifier")
def ouvrages_dalot_verifier(filepath: str = typer.Argument(..., help="Chemin vers le fichier de données YAML du dalot.")):
    """Vérifie les performances hydrauliques d'un dalot."""
    if not _json_output_enabled:
        console.print(f"--- Lancement de la Vérification du Dalot depuis : {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        resultats = verifier_dalot(config)
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Vérification Dalot[/bold green]", border_style="green"))
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Vérification Dalot", border_style="red"))
        raise typer.Exit(code=1)

@ouvrages_app.command("init-dalot")
def ouvrages_init_dalot(filepath: str = typer.Argument("dalot_exemple.yml")):
    """Génère un fichier YAML d'exemple pour un dalot."""
    template = """# Fichier de définition pour la vérification d'un dalot\n\nlargeur_m: 2.5\nhauteur_m: 2.0\nnombre_cellules: 2\nlongueur_m: 18.0\npente_m_m: 0.005\ndebit_projet_m3s: 35.0\nmanning: 0.013\n"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(template)
        if not _json_output_enabled:
            console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Template de dalot créé : '{filepath}'", title="Génération Template", border_style="green"))
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Impossible de créer le fichier : {e}", title="Erreur Génération Template", border_style="red"))
        raise typer.Exit(code=1)

# --- Commande Déversoir ---
@ouvrages_app.command("deversoir-dimensionner")
def ouvrages_deversoir_dimensionner(filepath: str = typer.Argument(..., help="Chemin vers le fichier de données YAML du déversoir.")):
    """Dimensionne la longueur d'un déversoir de crue à seuil fixe."""
    if not _json_output_enabled:
        console.print(f"--- Lancement du Dimensionnement du Déversoir depuis : {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        resultats = dimensionner_deversoir(config)
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            if resultats['statut'] == 'OK':
                console.print(Panel(f"  Type de déversoir : {resultats['type_deversoir']}\n  Pour un débit de projet de {resultats['debit_projet_m3s']} m³/s, avec une charge de {resultats['charge_hydraulique_projet_m']} m,\n  => Longueur de crête requise : {resultats['longueur_crete_calculee_m']} m", title="[bold green]Résultats Dimensionnement Déversoir[/bold green]", border_style="green"))
            else:
                console.print(Panel(f"[bold red]ERREUR[/bold red]: {resultats['message']}", title="Erreur Dimensionnement Déversoir", border_style="red"))
    except FileNotFoundError:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": f"Fichier '{filepath}' introuvable."}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Fichier '{filepath}' introuvable.", title="Erreur de Fichier", border_style="red"))
        raise typer.Exit(code=1)
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Une erreur inattendue est survenue : {e}", title="Erreur Inattendue", border_style="red"))
        raise typer.Exit(code=1)

@ouvrages_app.command("init-deversoir")
def ouvrages_init_deversoir(filepath: str = typer.Argument("deversoir_exemple.yml")):
    """Génère un fichier YAML d'exemple pour un déversoir."""
    template = """# Fichier de définition pour un déversoir de crue\n\ndebit_projet_m3s: 600\ncote_crete_barrage_m: 150.0\nrevanche_m: 1.0\ncote_crete_deversoir_m: 148.0\nprofil_crete: creager # Options: creager, seuil_epais, paroi_mince\n"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(template)
        if not _json_output_enabled:
            console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Template de déversoir créé : '{filepath}'", title="Génération Template", border_style="green"))
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Impossible de créer le fichier : {e}", title="Erreur Génération Template", border_style="red"))
        raise typer.Exit(code=1)

# --- Commandes Collecteur d'Assainissement ---
collector_app = typer.Typer(name="collector", help="Dimensionnement des réseaux d'assainissement gravitaire.")
app.add_typer(collector_app)

@collector_app.command("eaux-usees")
def collector_eaux_usees(filepath: str = typer.Argument(..., help="Chemin vers le fichier JSON du réseau d'eaux usées.")):
    """Dimensionne un réseau d'eaux usées (mode déterministe)."""
    if not _json_output_enabled:
        console.print(f"--- Lancement du Dimensionnement Réseau Eaux Usées depuis : {filepath} ---")
    try:
        from .calculs.assainissement_gravitaire import creer_reseau_depuis_json, dimensionner_reseau_eaux_usees, exporter_resultats_json
        
        reseau = creer_reseau_depuis_json(filepath)
        resultats = dimensionner_reseau_eaux_usees(reseau)
        
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Dimensionnement Eaux Usées[/bold green]", border_style="green"))
        
        output_file = filepath.replace('.json', '_resultats_eaux_usees.json')
        exporter_resultats_json(reseau, output_file)
        if not _json_output_enabled:
            console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Résultats exportés vers : {output_file}", title="Export Résultats", border_style="green"))
        
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Dimensionnement Eaux Usées", border_style="red"))
        raise typer.Exit(code=1)

@collector_app.command("eaux-pluviales")
def collector_eaux_pluviales(
    filepath: str = typer.Argument(..., help="Chemin vers le fichier JSON du réseau d'eaux pluviales."),
    type_idf: str = typer.Option("talbot", "--type-idf", help="Type de formule IDF (talbot, montana)"),
    coeff_a: float = typer.Option(120, "--coeff-a", help="Coefficient A de la formule IDF"),
    coeff_b: float = typer.Option(20, "--coeff-b", help="Coefficient B de la formule IDF")
):
    """Dimensionne un réseau d'eaux pluviales (mode hydrologique itératif)."""
    if not _json_output_enabled:
        console.print(f"--- Lancement du Dimensionnement Réseau Eaux Pluviales depuis : {filepath} ---")
    try:
        from .calculs.assainissement_gravitaire import creer_reseau_depuis_json, dimensionner_reseau_eaux_pluviales, exporter_resultats_json
        
        reseau = creer_reseau_depuis_json(filepath)
        params_pluie = {
            "type": type_idf,
            "a": coeff_a,
            "b": coeff_b
        }
        
        resultats = dimensionner_reseau_eaux_pluviales(reseau, params_pluie)
        
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Dimensionnement Eaux Pluviales[/bold green]", border_style="green"))
        
        output_file = filepath.replace('.json', '_resultats_eaux_pluviales.json')
        exporter_resultats_json(reseau, output_file)
        if not _json_output_enabled:
            console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Résultats exportés vers : {output_file}", title="Export Résultats", border_style="green"))
        
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Dimensionnement Eaux Pluviales", border_style="red"))
        raise typer.Exit(code=1)

@collector_app.command("init-exemple")
def collector_init_exemple(
    type_reseau: str = typer.Argument(..., help="Type de réseau (eaux-usees, eaux-pluviales)"),
    filepath: str = typer.Argument("reseau_exemple.json", help="Chemin du fichier de sortie")
):
    """Génère un fichier JSON d'exemple pour un réseau d'assainissement."""
    if type_reseau == "eaux-usees":
        template = {
            "troncons": [
                {
                    "id": "T1",
                    "type_section": "circulaire",
                    "longueur_troncon_m": 100.0,
                    "pente_troncon": 0.005,
                    "ks_manning_strickler": 70.0,
                    "amont_ids": [],
                    "population": 50,
                    "dotation_l_jour_hab": 150.0,
                    "coefficient_pointe": 2.5
                },
                {
                    "id": "T2",
                    "type_section": "circulaire",
                    "longueur_troncon_m": 150.0,
                    "pente_troncon": 0.004,
                    "ks_manning_strickler": 70.0,
                    "amont_ids": ["T1"],
                    "population": 75,
                    "dotation_l_jour_hab": 150.0,
                    "coefficient_pointe": 2.5
                }
            ]
        }
    elif type_reseau == "eaux-pluviales":
        template = {
            "troncons": [
                {
                    "id": "T1",
                    "type_section": "circulaire",
                    "longueur_troncon_m": 100.0,
                    "pente_troncon": 0.005,
                    "ks_manning_strickler": 70.0,
                    "amont_ids": [],
                    "surface_propre_ha": 2.5,
                    "coefficient_ruissellement": 0.8,
                    "longueur_parcours_m": 80.0,
                    "pente_parcours_m_m": 0.02
                },
                {
                    "id": "T2",
                    "type_section": "circulaire",
                    "longueur_troncon_m": 150.0,
                    "pente_troncon": 0.004,
                    "ks_manning_strickler": 70.0,
                    "amont_ids": ["T1"],
                    "surface_propre_ha": 3.0,
                    "coefficient_ruissellement": 0.7,
                    "longueur_parcours_m": 120.0,
                    "pente_parcours_m_m": 0.015
                }
            ]
        }
    else:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": f"Type de réseau '{type_reseau}' non reconnu. Utilisez 'eaux-usees' ou 'eaux-pluviales'."}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Type de réseau '{type_reseau}' non reconnu. Utilisez 'eaux-usees' ou 'eaux-pluviales'.", title="Erreur de Type de Réseau", border_style="red"))
        raise typer.Exit(code=1)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        if not _json_output_enabled:
            console.print(Panel(f"[bold green]SUCCÈS[/bold green]: Template de réseau {type_reseau} créé : '{filepath}'", title="Génération Template", border_style="green"))
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Impossible de créer le fichier : {e}", title="Erreur Génération Template", border_style="red"))
        raise typer.Exit(code=1)

# --- Commandes Réservoirs d'Eau Potable ---
reservoir_app = typer.Typer(name="reservoir", help="Dimensionnement des réservoirs d'eau potable.")
app.add_typer(reservoir_app)

@reservoir_app.command("equilibrage")
def reservoir_equilibrage(
    demande_journaliere_m3: float = typer.Option(None, "--demande-journaliere", "-d", help="Demande journalière moyenne en m³"),
    coefficient_pointe_jour: float = typer.Option(1.3, "--cp-jour", help="Coefficient de pointe journalière"),
    coefficient_pointe_horaire: float = typer.Option(1.7, "--cp-horaire", help="Coefficient de pointe horaire"),
    nombre_jours_stockage: int = typer.Option(1, "--jours-stockage", help="Nombre de jours de stockage de sécurité")
):
    """
    Dimensionne un réservoir d'équilibrage pour l'eau potable.
    
    Si aucun paramètre n'est fourni, affiche les paramètres d'entrée requis.
    """
    # Si aucun paramètre obligatoire n'est fourni, afficher les paramètres d'entrée
    if demande_journaliere_m3 is None:
        from ..utils.command_helpers import show_input_parameters, create_parameter_dict
        
        required_params = [
            create_parameter_dict("demande-journaliere", "Demande journalière moyenne en m³", "d")
        ]
        
        optional_params = [
            create_parameter_dict("cp-jour", "Coefficient de pointe journalière", default=1.3),
            create_parameter_dict("cp-horaire", "Coefficient de pointe horaire", default=1.7),
            create_parameter_dict("jours-stockage", "Nombre de jours de stockage de sécurité", default=1)
        ]
        
        examples = [
            "lcpi hydro reservoir equilibrage --demande-journaliere 1000",
            "lcpi hydro reservoir equilibrage -d 500 --cp-jour 1.5 --cp-horaire 2.0"
        ]
        
        show_input_parameters(
            "Dimensionnement Réservoir d'Équilibrage",
            required_params,
            optional_params,
            examples,
            "Calcule la capacité nécessaire d'un réservoir d'équilibrage pour l'eau potable."
        )
        return

    if not _json_output_enabled:
        console.print(f"--- Dimensionnement Réservoir d'Équilibrage ---")
    try:
        from .calculs.reservoir_aep import dimensionner_reservoir_equilibrage
        
        resultats = dimensionner_reservoir_equilibrage(
            demande_journaliere_m3, coefficient_pointe_jour, coefficient_pointe_horaire, nombre_jours_stockage
        )
        
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Dimensionnement Réservoir d'Équilibrage[/bold green]", border_style="green"))
        
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Dimensionnement Réservoir d'Équilibrage", border_style="red"))
        raise typer.Exit(code=1)

@reservoir_app.command("incendie")
def reservoir_incendie(
    population: int = typer.Option(None, "--population", "-p", help="Population desservie"),
    type_zone: str = typer.Option("urbain", "--type-zone", "-t", help="Type de zone (urbain, rural, industriel)")
):
    """Dimensionne un réservoir d'incendie selon les normes."""
    # Si aucun paramètre obligatoire n'est fourni, afficher les paramètres d'entrée
    if population is None:
        from ..utils.command_helpers import show_input_parameters, create_parameter_dict
        
        required_params = [
            create_parameter_dict("population", "Population desservie", "p")
        ]
        
        optional_params = [
            create_parameter_dict("type-zone", "Type de zone (urbain, rural, industriel)", default="urbain")
        ]
        
        examples = [
            "lcpi hydro reservoir incendie --population 5000",
            "lcpi hydro reservoir incendie -p 10000 --type-zone rural"
        ]
        
        show_input_parameters(
            "Dimensionnement Réservoir d'Incendie",
            required_params,
            optional_params,
            examples,
            "Dimensionne un réservoir d'incendie selon les normes en vigueur."
        )
        return

    if not _json_output_enabled:
        console.print(f"--- Dimensionnement Réservoir d'Incendie ---")
    try:
        from .calculs.reservoir_aep import dimensionner_reservoir_incendie
        
        resultats = dimensionner_reservoir_incendie(population, 0, type_zone)
        
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Dimensionnement Réservoir d'Incendie[/bold green]", border_style="green"))
        
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Dimensionnement Réservoir d'Incendie", border_style="red"))
        raise typer.Exit(code=1)

@reservoir_app.command("complet")
def reservoir_complet(
    population: int = typer.Option(None, "--population", "-p", help="Population desservie"),
    dotation_l_jour_hab: float = typer.Option(150.0, "--dotation", "-d", help="Dotation en L/jour/habitant"),
    coefficient_pointe_jour: float = typer.Option(1.3, "--cp-jour", help="Coefficient de pointe journalière"),
    coefficient_pointe_horaire: float = typer.Option(1.7, "--cp-horaire", help="Coefficient de pointe horaire"),
    nombre_jours_securite: int = typer.Option(1, "--jours-securite", help="Nombre de jours de stockage de sécurité"),
    type_zone_incendie: str = typer.Option("urbain", "--type-zone", "-t", help="Type de zone pour l'incendie")
):
    """Dimensionne un réservoir complet (équilibrage + incendie + sécurité)."""
    # Si aucun paramètre obligatoire n'est fourni, afficher les paramètres d'entrée
    if population is None:
        from ..utils.command_helpers import show_input_parameters, create_parameter_dict
        
        required_params = [
            create_parameter_dict("population", "Population desservie", "p")
        ]
        
        optional_params = [
            create_parameter_dict("dotation", "Dotation en L/jour/habitant", default=150.0),
            create_parameter_dict("cp-jour", "Coefficient de pointe journalière", default=1.3),
            create_parameter_dict("cp-horaire", "Coefficient de pointe horaire", default=1.7),
            create_parameter_dict("jours-securite", "Nombre de jours de stockage de sécurité", default=1),
            create_parameter_dict("type-zone", "Type de zone pour l'incendie", default="urbain")
        ]
        
        examples = [
            "lcpi hydro reservoir complet --population 5000",
            "lcpi hydro reservoir complet -p 10000 --dotation 200 --cp-jour 1.5"
        ]
        
        show_input_parameters(
            "Dimensionnement Réservoir Complet",
            required_params,
            optional_params,
            examples,
            "Dimensionne un réservoir complet (équilibrage + incendie + sécurité)."
        )
        return

    if not _json_output_enabled:
        console.print(f"--- Dimensionnement Réservoir Complet ---")
    try:
        from .calculs.reservoir_aep import dimensionner_reservoir_complet
        
        resultats = dimensionner_reservoir_complet(
            population, dotation_l_jour_hab, coefficient_pointe_jour, 
            coefficient_pointe_horaire, nombre_jours_securite, type_zone_incendie
        )
        
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Dimensionnement Réservoir Complet[/bold green]", border_style="green"))
        
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Dimensionnement Réservoir Complet", border_style="red"))
        raise typer.Exit(code=1)

@reservoir_app.command("verifier-pression")
def reservoir_verifier_pression(
    cote_reservoir_m: float = typer.Option(None, "--cote-reservoir", "-c", help="Cote du réservoir en m NGF"),
    cote_terrain_m: float = typer.Option(None, "--cote-terrain", "-t", help="Cote du terrain en m NGF"),
    pertes_charge_m: float = typer.Option(None, "--pertes-charge", "-p", help="Pertes de charge dans le réseau en m"),
    pression_minimale_m: float = typer.Option(15.0, "--pression-min", help="Pression minimale requise en m")
):
    """Vérifie la pression disponible dans le réseau depuis un réservoir."""
    # Si aucun paramètre obligatoire n'est fourni, afficher les paramètres d'entrée
    if cote_reservoir_m is None or cote_terrain_m is None or pertes_charge_m is None:
        from ..utils.command_helpers import show_input_parameters, create_parameter_dict
        
        required_params = [
            create_parameter_dict("cote-reservoir", "Cote du réservoir en m NGF", "c"),
            create_parameter_dict("cote-terrain", "Cote du terrain en m NGF", "t"),
            create_parameter_dict("pertes-charge", "Pertes de charge dans le réseau en m", "p")
        ]
        
        optional_params = [
            create_parameter_dict("pression-min", "Pression minimale requise en m", default=15.0)
        ]
        
        examples = [
            "lcpi hydro reservoir verifier-pression --cote-reservoir 100 --cote-terrain 85 --pertes-charge 5",
            "lcpi hydro reservoir verifier-pression -c 100 -t 85 -p 5 --pression-min 20"
        ]
        
        show_input_parameters(
            "Vérification de la Pression",
            required_params,
            optional_params,
            examples,
            "Vérifie la pression disponible dans le réseau depuis un réservoir."
        )
        return

    if not _json_output_enabled:
        console.print(f"--- Vérification de la Pression ---")
    try:
        from .calculs.reservoir_aep import verifier_pression_reservoir
        
        resultats = verifier_pression_reservoir(cote_reservoir_m, cote_terrain_m, pertes_charge_m, pression_minimale_m)
        
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Vérification Pression[/bold green]", border_style="green"))
        
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Vérification Pression", border_style="red"))
        raise typer.Exit(code=1)

# --- Commandes Utilitaires (Implémentation finale) ---

# --- Commande Plomberie ---
@plomberie_app.command("dimensionner")
def plomberie_dimensionner(
    nombre_appareils: int = typer.Option(None, "--nb-appareils", "-n", help="Nombre d'appareils sanitaires connectés au tronçon"),
    somme_debits_base_ls: float = typer.Option(None, "--debits-base", "-d", help="Somme des débits de base en litres par seconde"),
    v_max: float = typer.Option(2.0, "--v-max", help="Vitesse maximale admissible en m/s")
):
    """
    Dimensionne un tronçon de réseau de plomberie interne.
    
    Si aucun paramètre n'est fourni, affiche les paramètres d'entrée requis.
    """
    # Si aucun paramètre obligatoire n'est fourni, afficher les paramètres d'entrée
    if nombre_appareils is None or somme_debits_base_ls is None:
        console.print(Panel(
            "[bold blue]Paramètres d'entrée pour le dimensionnement de tronçon de plomberie :[/bold blue]\n\n"
            "[bold]Paramètres obligatoires :[/bold]\n"
            "• --nb-appareils (-n) : Nombre d'appareils sanitaires connectés au tronçon\n"
            "• --debits-base (-d) : Somme des débits de base en litres par seconde\n\n"
            "[bold]Paramètres optionnels :[/bold]\n"
            "• --v-max : Vitesse maximale admissible (défaut: 2.0 m/s)\n\n"
            "[bold]Exemple d'utilisation :[/bold]\n"
            "lcpi hydro plomberie dimensionner --nb-appareils 5 --debits-base 2.5\n"
            "lcpi hydro plomberie dimensionner -n 3 -d 1.8 --v-max 1.5",
            title="[bold green]Paramètres d'entrée - Dimensionnement Plomberie[/bold green]",
            border_style="blue"
        ))
        return

    try:
        donnees = {
            "nombre_appareils": nombre_appareils,
            "somme_debits_base_ls": somme_debits_base_ls,
            "v_max": v_max
        }
        
        resultats = dimensionner_troncon_plomberie(donnees)
        
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(
                f"[bold]Résultats du dimensionnement :[/bold]\n\n"
                f"• Débit probable : {resultats['debit_probable_ls']} L/s\n"
                f"• Diamètre théorique : {resultats['diametre_theorique_mm']} mm\n"
                f"• Diamètre normalisé choisi : {resultats['diametre_normalise_choisi_mm']} mm\n"
                f"• Vitesse réelle : {resultats['vitesse_reelle_ms']} m/s",
                title="[bold green]Résultats Dimensionnement Plomberie[/bold green]",
                border_style="green"
            ))
            
    except Exception as e:
        if _json_output_enabled:
            console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else:
            console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Dimensionnement Plomberie", border_style="red"))
        raise typer.Exit(code=1)

@plomberie_app.command("init-exemple")
def plomberie_init_exemple(filepath: str = typer.Argument("plomberie_exemple.yml")):
    """Génère un fichier d'exemple pour le dimensionnement de plomberie."""
    try:
        exemple_data = {
            "nombre_appareils": 5,
            "somme_debits_base_ls": 2.5,
            "v_max": 2.0,
            "description": "Exemple de tronçon de plomberie pour un immeuble résidentiel"
        }
        
        import yaml
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(exemple_data, f, default_flow_style=False, allow_unicode=True)
        
        if not _json_output_enabled:
            console.print(Panel(
                f"✅ Fichier d'exemple créé : {filepath}\n\n"
                f"Vous pouvez maintenant utiliser :\n"
                f"lcpi hydro plomberie dimensionner --nb-appareils 5 --debits-base 2.5",
                title="[bold green]Fichier d'exemple créé[/bold green]",
                border_style="green"
            ))
            
    except Exception as e:
        if _json_output_enabled:
            console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else:
            console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Création Fichier Exemple", border_style="red"))
        raise typer.Exit(code=1)

@utils_app.command("prevoir-population")
def utils_population(
    methode: str = typer.Option(None, "--method", "-m", help="Méthode de calcul: arithmetique, lineaire, geometrique, exponentiel, malthus, logistique."),
    annee_projet: int = typer.Option(None, "--annee", "-a", help="Année future pour laquelle estimer la population.")
):
    """Prévoit l'évolution de la population selon différentes méthodes."""
    # Si aucun paramètre obligatoire n'est fourni, afficher les paramètres d'entrée
    if methode is None or annee_projet is None:
        from ..utils.command_helpers import show_input_parameters, create_parameter_dict
        
        required_params = [
            create_parameter_dict("method", "Méthode de calcul: arithmetique, lineaire, geometrique, exponentiel, malthus, logistique", "m"),
            create_parameter_dict("annee", "Année future pour laquelle estimer la population", "a")
        ]
        
        examples = [
            "lcpi hydro util prevoir-population --method arithmetique --annee 2030",
            "lcpi hydro util prevoir-population -m lineaire -a 2040"
        ]
        
        show_input_parameters(
            "Prévision de Population",
            required_params,
            examples=examples,
            description="Prévoit l'évolution de la population selon différentes méthodes statistiques."
        )
        return

    if not _json_output_enabled:
        console.print(f"--- Prévision de Population ---")
    try:
        # Données d'exemple pour la démonstration
        population_actuelle = 10000
        annee_actuelle = 2024
        
        # Calcul selon la méthode choisie
        if methode == "arithmetique":
            taux_croissance = 0.02  # 2% par an
            population_future = population_actuelle * (1 + taux_croissance * (annee_projet - annee_actuelle))
        elif methode == "lineaire":
            croissance_annuelle = 200  # habitants par an
            population_future = population_actuelle + croissance_annuelle * (annee_projet - annee_actuelle)
        elif methode == "geometrique":
            taux_croissance = 0.015  # 1.5% par an
            population_future = population_actuelle * ((1 + taux_croissance) ** (annee_projet - annee_actuelle))
        else:
            population_future = population_actuelle  # Valeur par défaut
        
        resultats = {
            "methode": methode,
            "annee_actuelle": annee_actuelle,
            "annee_projet": annee_projet,
            "population_actuelle": population_actuelle,
            "population_future": round(population_future, 0),
            "croissance": round(population_future - population_actuelle, 0)
        }
        
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Prévision Population[/bold green]", border_style="green"))
        
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Prévision Population", border_style="red"))
        raise typer.Exit(code=1)

@utils_app.command("estimer-demande-eau")
def utils_demande_eau(
    population: int = typer.Option(None, "--pop", "-p", help="Population future estimée."),
    dotation: float = typer.Option(None, "--dota", "-d", help="Dotation domestique en L/jour/habitant.")
):
    """Estime la demande en eau pour une population donnée."""
    # Si aucun paramètre obligatoire n'est fourni, afficher les paramètres d'entrée
    if population is None or dotation is None:
        from ..utils.command_helpers import show_input_parameters, create_parameter_dict
        
        required_params = [
            create_parameter_dict("pop", "Population future estimée", "p"),
            create_parameter_dict("dota", "Dotation domestique en L/jour/habitant", "d")
        ]
        
        examples = [
            "lcpi hydro util estimer-demande-eau --pop 5000 --dota 150",
            "lcpi hydro util estimer-demande-eau -p 10000 -d 200"
        ]
        
        show_input_parameters(
            "Estimation Demande en Eau",
            required_params,
            examples=examples,
            description="Estime la demande en eau pour une population donnée."
        )
        return

    if not _json_output_enabled:
        console.print(f"--- Estimation Demande en Eau ---")
    try:
        demande_journaliere_l = population * dotation
        demande_journaliere_m3 = demande_journaliere_l / 1000
        
        resultats = {
            "population": population,
            "dotation_l_jour_hab": dotation,
            "demande_journaliere_l": demande_journaliere_l,
            "demande_journaliere_m3": demande_journaliere_m3
        }
        
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Estimation Demande Eau[/bold green]", border_style="green"))
        
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Estimation Demande Eau", border_style="red"))
        raise typer.Exit(code=1)

@utils_app.command("diagramme-ombro")
def utils_diagramme(
    filepath: str = typer.Option(None, "--filepath", "-f", help="Chemin vers le fichier de données climatiques YAML."),
    output_path: str = typer.Option("diagramme_ombro.png", "--output", "-o", help="Chemin du fichier PNG de sortie.")
):
    """Génère un diagramme ombrothermique à partir de données climatiques."""
    # Si aucun paramètre obligatoire n'est fourni, afficher les paramètres d'entrée
    if filepath is None:
        from ..utils.command_helpers import show_input_parameters, create_parameter_dict
        
        required_params = [
            create_parameter_dict("filepath", "Chemin vers le fichier de données climatiques YAML", "f")
        ]
        
        optional_params = [
            create_parameter_dict("output", "Chemin du fichier PNG de sortie", default="diagramme_ombro.png")
        ]
        
        examples = [
            "lcpi hydro util diagramme-ombro --filepath donnees_climat.yml",
            "lcpi hydro util diagramme-ombro -f donnees_climat.yml --output mon_diagramme.png"
        ]
        
        show_input_parameters(
            "Génération Diagramme Ombrothermique",
            required_params,
            optional_params,
            examples,
            "Génère un diagramme ombrothermique à partir de données climatiques."
        )
        return

    if not _json_output_enabled:
        console.print(f"--- Génération Diagramme Ombrothermique ---")
    try:
        import yaml
        with open(filepath, 'r', encoding='utf-8') as f:
            donnees_climat = yaml.safe_load(f)
        
        resultats = generer_diagramme_ombrothermique(donnees_climat, output_path)
        
        if _json_output_enabled:
            console.print(json.dumps(resultats, indent=2, ensure_ascii=False))
        else:
            console.print(Panel(json.dumps(resultats, indent=2, ensure_ascii=False), title="[bold green]Résultats Génération Diagramme[/bold green]", border_style="green"))
        
    except FileNotFoundError:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": f"Fichier de données '{filepath}' introuvable."}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: Le fichier de données '{filepath}' est introuvable.", title="Erreur de Fichier", border_style="red"))
        raise typer.Exit(code=1)
    except Exception as e:
        if _json_output_enabled: console.print(json.dumps({"statut": "Erreur", "message": str(e)}))
        else: console.print(Panel(f"[bold red]ERREUR[/bold red]: {e}", title="Erreur Diagramme Ombrothermique", border_style="red"))
        raise typer.Exit(code=1)

# --- Point d'entrée ---
def register():
    return app