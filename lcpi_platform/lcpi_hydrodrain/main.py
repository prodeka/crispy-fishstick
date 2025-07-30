import typer
import json
from .calculs.pluviometrie import analyser_donnees_brutes, ajuster_lois_frequentielles, generer_courbes_idf
from .calculs.bassin_versant import caracteriser_bassin, estimer_crue
# Imports de tous les modules de calcul du plugin
from .calculs.canal import dimensionner_canal
from .calculs.pompage import predimensionner_pompe
from .calculs.plomberie import dimensionner_troncon_plomberie
from .calculs.deversoir import dimensionner_deversoir
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
def pluvio_ajuster(filepath: str, loi: str = "gumbel"):
    """Ajuste les pluies maximales à une loi statistique."""
    # Pour un vrai cas, on lirait le fichier pour extraire la série de pluies
    series_pluies_exemple = [85, 110, 95, 130, 78, 115, 125, 90, 105, 140]
    resultats = ajuster_lois_frequentielles(series_pluies_exemple)
    print(json.dumps(resultats, indent=2))

@pluvio_app.command("generer-idf")
def pluvio_generer_idf(filepath: str, modele: str = "montana"):
    """Génère les courbes IDF à partir de données ajustées."""
    donnees_ajustees_exemple = {} # Un vrai cas passerait les résultats de l'ajustement
    resultats = generer_courbes_idf(donnees_ajustees_exemple)
    print(json.dumps(resultats, indent=2))

@hydro_app.command("caracteriser")
def hydro_caracteriser(mnt_filepath: str):
    """Calcule les paramètres physiques d'un bassin versant."""
    donnees_exemple = {"mnt_path": mnt_filepath}
    resultats = caracteriser_bassin(donnees_exemple)
    print(json.dumps(resultats, indent=2))

@hydro_app.command("estimer-crue")
def hydro_estimer_crue(bassin_params_path: str, methode: str = "orstom"):
    """Estime le débit de pointe d'un bassin versant."""
    # Un vrai cas lirait le fichier de paramètres du bassin
    donnees_bassin_exemple = {"superficie_km2": 150}
    resultats = estimer_crue(donnees_bassin_exemple, methode)
    print(json.dumps(resultats, indent=2))

# --- Commandes Ouvrages ---
# ... (les commandes pour deversoir, radier, canal, pompe restent ici)

# --- Commandes Utilitaires (Implémentation finale) ---
@utils_app.command("prevoir-population")
def utils_population(pop1: int, annee1: int, pop2: int, annee2: int, annee_projet: int):
    donnees = {"pop_annee_1": (pop1, annee1), "pop_annee_2": (pop2, annee2), "annee_projet": annee_projet}
    print("\n--- Prévision Arithmétique ---")
    donnees["methode"] = "arithmetique"
    print(json.dumps(prevoir_population(donnees), indent=2))
    print("\n--- Prévision Géométrique ---")
    donnees["methode"] = "geometrique"
    print(json.dumps(prevoir_population(donnees), indent=2))

@utils_app.command("estimer-demande-eau")
def utils_demande_eau(
    population: int = typer.Argument(..., help="Population totale desservie."),
    dotation: float = typer.Argument(..., help="Dotation par habitant (L/jour/hab)."),
    rendement: float = typer.Option(0.8, "--rendement", "-r", help="Rendement du réseau de distribution (ex: 0.8 pour 80%).")
):
    """Estime les besoins en eau potable d'une population."""
    donnees = {
        "population": population,
        "dotation_domestique_l_j_hab": dotation,
        "rendement_reseau": rendement
    }
    print(json.dumps(estimer_demande_eau(donnees), indent=2))

@utils_app.command("diagramme-ombro")
def utils_diagramme(output_path: str = "diagramme_ombro.png"):
    donnees_lomé = { "station": "Lomé, Togo", "donnees_mensuelles": [
            {"mois": "Jan", "temp_C": 27.1, "precip_mm": 19.4}, {"mois": "Fev", "temp_C": 28.2, "precip_mm": 46.1},
            {"mois": "Mar", "temp_C": 28.5, "precip_mm": 91.9}, {"mois": "Avr", "temp_C": 28.4, "precip_mm": 128.6},
            {"mois": "Mai", "temp_C": 27.5, "precip_mm": 197.8}, {"mois": "Juin", "temp_C": 26.1, "precip_mm": 279.1},
            {"mois": "Juil", "temp_C": 25.4, "precip_mm": 105.1}, {"mois": "Aou", "temp_C": 25.2, "precip_mm": 45.9},
            {"mois": "Sep", "temp_C": 25.8, "precip_mm": 159.2}, {"mois": "Oct", "temp_C": 26.8, "precip_mm": 125.4},
            {"mois": "Nov", "temp_C": 27.5, "precip_mm": 35.8}, {"mois": "Dec", "temp_C": 27.2, "precip_mm": 8.5} ]}
    print(json.dumps(generer_diagramme_ombrothermique(donnees_lomé, output_path), indent=2))

# --- Point d'entrée ---
def register():
    return app