import typer
import json
import yaml
from .calculs.pluviometrie import analyser_donnees_brutes, ajuster_loi_gumbel, generer_courbes_idf
from .calculs.bassin_versant import caracteriser_bassin
# Imports de tous les modules de calcul du plugin
from .calculs.canal import dimensionner_canal
from .calculs.pompage import predimensionner_pompe
from .calculs.plomberie import dimensionner_troncon_plomberie
from .calculs.deversoir import dimensionner_deversoir
from .calculs.dalot import verifier_dalot
from .calculs.radier import dimensionner_radier_submersible
from .calculs.population import prevoir_population
from .calculs.demande_eau import estimer_demande_eau
from .calculs.climat import generer_diagramme_ombrothermique

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
    resultats = analyser_donnees_brutes(filepath)
    print(json.dumps(resultats, indent=2))

@pluvio_app.command("ajuster-loi")
def pluvio_ajuster(filepath: str):
    """Ajuste les pluies maximales à la loi de Gumbel (ou autre)."""
    # On suppose un CSV avec une colonne 'pluie'
    import pandas as pd
    df = pd.read_csv(filepath)
    if 'pluie' not in df.columns:
        print("ERREUR: Le fichier doit contenir une colonne 'pluie'.")
        return
    series = df['pluie'].dropna().tolist()
    resultats = ajuster_loi_gumbel(series)
    print(json.dumps(resultats, indent=2, ensure_ascii=False))

@pluvio_app.command("generer-idf")
def pluvio_generer_idf(filepath: str, modele: str = "montana"):
    """Génère les courbes IDF à partir de données ajustées."""
    donnees_ajustees_exemple = {} # Un vrai cas passerait les résultats de l'ajustement
    resultats = generer_courbes_idf(donnees_ajustees_exemple)
    print(json.dumps(resultats, indent=2))

@hydro_app.command("caracteriser")
def hydro_caracteriser(filepath: str):
    """Calcule les paramètres physiques d'un bassin versant à partir d'un fichier YAML ou CSV."""
    import os
    import pandas as pd
    import yaml
    if filepath.endswith('.yml') or filepath.endswith('.yaml'):
        with open(filepath, 'r', encoding='utf-8') as f:
            donnees = yaml.safe_load(f)
    elif filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
        # On suppose que le CSV a les colonnes attendues
        donnees = {
            'superficie_km2': float(df['superficie_km2'].iloc[0]),
            'perimetre_km': float(df['perimetre_km'].iloc[0]),
            'pente_globale_m_km': float(df['pente_globale_m_km'].iloc[0])
        }
    else:
        print("ERREUR: Format de fichier non supporté (utilisez .yml, .yaml ou .csv)")
        return
    resultats = caracteriser_bassin(donnees)
    print(json.dumps(resultats, indent=2, ensure_ascii=False))

# --- Commandes Ouvrages ---
import typer
import json
import yaml
from .calculs.canal import dimensionner_canal
from .calculs.deversoir import dimensionner_deversoir
from .calculs.dalot import verifier_dalot

ouvrages_app = typer.Typer(name="ouvrage", help="Dimensionnement et Analyse Hydraulique des Ouvrages.")
app.add_typer(ouvrages_app)

# --- Commande Canal ---
@ouvrages_app.command("canal-dimensionner")
def ouvrages_canal_dimensionner(filepath: str = typer.Argument(..., help="Chemin vers le fichier de données YAML du canal.")):
    """Dimensionne un canal à ciel ouvert."""
    print(f"--- Lancement du Dimensionnement du Canal depuis : {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        resultats = dimensionner_canal(config)
        print("\n--- RÉSULTATS DU DIMENSIONNEMENT ---")
        print(json.dumps(resultats, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

@ouvrages_app.command("init-canal")
def ouvrages_init_canal(filepath: str = typer.Argument("canal_exemple.yml")):
    """Génère un fichier YAML d'exemple pour un canal."""
    template = """# Fichier de définition pour le dimensionnement d'un canal

debit_projet_m3s: 10.0
pente_m_m: 0.001
k_strickler: 30.0
fruit_talus_m_m: 1.5
vitesse_imposee_ms: 1.2
"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(template)
        print(f"[SUCCES] Template de canal créé : '{filepath}'")
    except Exception as e:
        print(f"[ERREUR] Impossible de créer le fichier : {e}")

# --- Commande Dalot ---
@ouvrages_app.command("dalot-verifier")
def ouvrages_dalot_verifier(filepath: str = typer.Argument(..., help="Chemin vers le fichier de données YAML du dalot.")):
    """Vérifie les performances hydrauliques d'un dalot."""
    print(f"--- Lancement de la Vérification du Dalot depuis : {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        resultats = verifier_dalot(config)
        print("\n--- RÉSULTATS DE LA VÉRIFICATION ---")
        print(json.dumps(resultats, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

@ouvrages_app.command("init-dalot")
def ouvrages_init_dalot(filepath: str = typer.Argument("dalot_exemple.yml")):
    """Génère un fichier YAML d'exemple pour un dalot."""
    template = """# Fichier de définition pour la vérification d'un dalot

largeur_m: 2.5
hauteur_m: 2.0
nombre_cellules: 2
longueur_m: 18.0
pente_m_m: 0.005
debit_projet_m3s: 35.0
manning: 0.013
"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(template)
        print(f"[SUCCES] Template de dalot créé : '{filepath}'")
    except Exception as e:
        print(f"[ERREUR] Impossible de créer le fichier : {e}")

# --- Commande Déversoir ---
@ouvrages_app.command("deversoir-dimensionner")
def ouvrages_deversoir_dimensionner(filepath: str = typer.Argument(..., help="Chemin vers le fichier de données YAML du déversoir.")):
    """Dimensionne la longueur d'un déversoir de crue à seuil fixe."""
    print(f"--- Lancement du Dimensionnement du Déversoir depuis : {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        resultats = dimensionner_deversoir(config)
        print("\n--- RÉSULTATS DU DIMENSIONNEMENT ---")
        if resultats['statut'] == 'OK':
            print(f"  Type de déversoir : {resultats['type_deversoir']}")
            print(f"  Pour un débit de projet de {resultats['debit_projet_m3s']} m³/s, avec une charge de {resultats['charge_hydraulique_projet_m']} m,")
            print(f"  => Longueur de crête requise : {resultats['longueur_crete_calculee_m']} m")
        else:
            print(f"  ERREUR: {resultats['message']}")
    except FileNotFoundError:
        print(f"ERREUR: Fichier '{filepath}' introuvable.")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")

@ouvrages_app.command("init-deversoir")
def ouvrages_init_deversoir(filepath: str = typer.Argument("deversoir_exemple.yml")):
    """Génère un fichier YAML d'exemple pour un déversoir."""
    template = """# Fichier de définition pour un déversoir de crue

debit_projet_m3s: 600
cote_crete_barrage_m: 150.0
revanche_m: 1.0
cote_crete_deversoir_m: 148.0
profil_crete: creager # Options: creager, seuil_epais, paroi_mince
"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(template)
        print(f"[SUCCES] Template de déversoir créé : '{filepath}'")
    except Exception as e:
        print(f"[ERREUR] Impossible de créer le fichier : {e}")

# ... (les commandes pour deversoir, radier, canal, pompe restent ici)

# --- Commandes Utilitaires (Implémentation finale) ---
@utils_app.command("prevoir-population")
def utils_population(
    methode: str = typer.Option("arithmetique", "--method", "-m", help="Méthode de calcul: arithmetique, lineaire, geometrique, exponentiel, malthus, logistique."),
    annee_projet: int = typer.Option(..., "--annee", "-a", help="Année future pour laquelle estimer la population."),
):
    """
    Estime la population future à partir de données de recensement historiques.
    Méthodes disponibles :
    - arithmetique (ou lineaire) : croissance annuelle fixe
    - geometrique (ou exponentiel, malthus) : croissance annuelle en %
    - logistique : croissance en S, nécessite 3 recensements
    """
    donnees = {"methode": methode, "annee_projet": annee_projet}
    print(f"--- Saisie des données pour la méthode '{methode}' ---")
    try:
        if methode in ["arithmetique", "lineaire", "geometrique", "exponentiel", "malthus"]:
            pop1 = typer.prompt("Population du 1er recensement (le plus ancien)", type=int)
            an1 = typer.prompt("Année du 1er recensement", type=int)
            pop2 = typer.prompt("Population du 2nd recensement (le plus récent)", type=int)
            an2 = typer.prompt("Année du 2nd recensement", type=int)
            donnees["pop_annee_1"] = (pop1, an1)
            donnees["pop_annee_2"] = (pop2, an2)
        elif methode == "logistique":
            print("Info : La méthode logistique requiert 3 recensements à intervalle de temps égal.")
            pop0 = typer.prompt("Population du 1er recensement (t0)", type=int)
            an0 = typer.prompt("Année du 1er recensement (t0)", type=int)
            pop1 = typer.prompt("Population du 2ème recensement (t1)", type=int)
            an1 = typer.prompt("Année du 2ème recensement (t1)", type=int)
            pop2 = typer.prompt("Population du 3ème recensement (t2)", type=int)
            an2 = typer.prompt("Année du 3ème recensement (t2)", type=int)
            donnees["pop_annee_0"] = (pop0, an0)
            donnees["pop_annee_1"] = (pop1, an1)
            donnees["pop_annee_2"] = (pop2, an2)
        else:
            print(f"[ERREUR] La méthode '{methode}' n'est pas supportée.")
            return
        resultats = prevoir_population(donnees)
        print(f"\n--- Résultat de la Prévision ({methode}) ---")
        print(json.dumps(resultats, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"\n[ERREUR] Une erreur est survenue durant la saisie ou le calcul : {e}")

@utils_app.command("estimer-demande-eau")
def utils_demande_eau(
    population: int = typer.Option(..., "--pop", help="Population future estimée."),
    dotation: float = typer.Option(..., "--dota", help="Dotation domestique en L/jour/habitant.")
):
    # Le reste de la fonction ne change pas...
    donnees = {"population": population, "dotation_domestique_l_j_hab": dotation}
    resultats = estimer_demande_eau(donnees)
    print(json.dumps(resultats, indent=2))

@utils_app.command("diagramme-ombro")
def utils_diagramme(
    filepath: str = typer.Argument(..., help="Chemin vers le fichier de données climatiques YAML."),
    output_path: str = typer.Option("diagramme_ombro.png", "--output", "-o", help="Chemin du fichier PNG de sortie.")
):
    """Génère un diagramme ombrothermique à partir d'un fichier de données."""
    try:
        import yaml
        with open(filepath, 'r', encoding='utf-8') as f:
            donnees_climat = yaml.safe_load(f)
        
        resultats = generer_diagramme_ombrothermique(donnees_climat, output_path)
        print(json.dumps(resultats, indent=2, ensure_ascii=False))
    except FileNotFoundError:
        print(f"ERREUR: Le fichier de données '{filepath}' est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

# --- Point d'entrée ---
def register():
    return app