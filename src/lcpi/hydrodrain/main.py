import typer
import json
from .calculs.pluviometrie import analyser_donnees_brutes, ajuster_lois_frequentielles, generer_courbes_idf
from .calculs.bassin_versant import caracteriser_bassin, estimer_crue
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
@ouvrages_app.command("canal-dimensionner")
def ouvrages_canal_dimensionner(
    filepath: str = typer.Option(None, "--filepath", help="Fichier YAML de configuration unique."),
    batch_file: str = typer.Option(None, "--batch-file", help="Fichier CSV pour dimensionner plusieurs canaux."),
    output_file: str = typer.Option("resultats_batch_canaux.csv", "--output-file", help="Fichier de résultats CSV.")
):
    """Dimensionne un ou plusieurs canaux à ciel ouvert."""
    if batch_file:
        try:
            import pandas as pd
        except ImportError:
            print("Erreur : La bibliothèque 'pandas' est requise. Installez-la avec 'pip install pandas'.")
            raise typer.Exit(code=1)

        print(f"--- Lancement du Traitement par Lot (Canaux) depuis : {batch_file} ---")
        try:
            df = pd.read_csv(batch_file)
            results_list = []
            for index, row in df.iterrows():
                donnees = row.to_dict()
                resultats = dimensionner_canal(donnees)
                output_row = row.to_dict()
                output_row.update(resultats)
                results_list.append(output_row)
            
            results_df = pd.DataFrame(results_list)
            results_df.to_csv(output_file, index=False)
            print(f"[SUCCES] Traitement par lot terminé. Résultats sauvegardés dans : {output_file}")
        
        except Exception as e:
            print(f"Une erreur est survenue lors du traitement par lot : {e}")
            raise typer.Exit(code=1)

    elif filepath:
        print("Logique YAML pour un seul canal à implémenter si nécessaire.")
    else:
        print("Erreur : Vous devez spécifier soit --filepath, soit --batch-file.")
        raise typer.Exit(code=1)

@ouvrages_app.command("deversoir-dimensionner")
def ouvrages_deversoir_dimensionner(
    debit_projet: float = typer.Option(..., "--debit-projet", help="Débit de projet en m³/s."),
    cote_barrage: float = typer.Option(..., "--cote-barrage", help="Cote de la crête du barrage (m)."),
    cote_deversoir: float = typer.Option(..., "--cote-deversoir", help="Cote de la crête du déversoir (m)."),
    revanche: float = typer.Option(1.0, "--revanche", help="Revanche de sécurité en m.")
):
    """Dimensionne la longueur d'un déversoir à crête épaisse."""
    donnees = {
        "debit_projet_m3s": debit_projet,
        "cote_crete_barrage_m": cote_barrage,
        "cote_crete_deversoir_m": cote_deversoir,
        "revanche_m": revanche
    }
    resultats = dimensionner_deversoir(donnees)
    print(json.dumps(resultats, indent=2))

@ouvrages_app.command("dalot-verifier")
def ouvrages_dalot_verifier(
    largeur: float = typer.Option(..., help="Largeur d'une cellule (m)"),
    hauteur: float = typer.Option(..., help="Hauteur d'une cellule (m)"),
    nombre_cellules: int = typer.Option(1, "--nombre-cellules", help="Nombre de cellules identiques"),
    longueur: float = typer.Option(..., help="Longueur de l'ouvrage (m)"),
    pente: float = typer.Option(..., help="Pente de l'ouvrage (m/m)"),
    debit_projet: float = typer.Option(..., help="Débit de projet à évacuer (m³/s)"),
    manning: float = typer.Option(0.013, help="Coefficient de rugosité de Manning")
):
    # Le reste de la fonction ne change pas...
    donnees_entree = { "largeur_m": largeur, "hauteur_m": hauteur, "nombre_cellules": nombre_cellules, "longueur_m": longueur, "pente_m_m": pente, "debit_projet_m3s": debit_projet, "manning": manning }
    resultats = verifier_dalot(donnees_entree)
    print("\n--- RÉSULTATS DE LA VÉRIFICATION ---")
    print(json.dumps(resultats, indent=2, ensure_ascii=False))

# ... (les commandes pour deversoir, radier, canal, pompe restent ici)

# --- Commandes Utilitaires (Implémentation finale) ---
@utils_app.command("prevoir-population")
def utils_population(
    pop1: int = typer.Option(..., "--pop1", help="Population à l'année de début."),
    annee1: int = typer.Option(..., "--annee1", help="Année de début."),
    pop2: int = typer.Option(..., "--pop2", help="Population à l'année de fin."),
    annee2: int = typer.Option(..., "--annee2", help="Année de fin."),
    annee_projet: int = typer.Option(..., "--annee-projet", help="Année pour laquelle estimer la population.")
):
    """Estime la population future par les méthodes arithmétique et géométrique."""
    donnees = {"pop_annee_1": (pop1, annee1), "pop_annee_2": (pop2, annee2), "annee_projet": annee_projet}
    print("\n--- Prévision Arithmétique ---")
    donnees["methode"] = "arithmetique"
    print(json.dumps(prevoir_population(donnees), indent=2))
    print("\n--- Prévision Géométrique ---")
    donnees["methode"] = "geometrique"
    print(json.dumps(prevoir_population(donnees), indent=2))

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