import typer
import json
from .core_legacy.assainissement_entry import main as run_legacy_assainissement
from .calculs import hydrologie, hydraulique
from .calculs.dalot import verifier_dalot
from .calculs.deversoir import dimensionner_deversoir
from .calculs.canal import dimensionner_canal
from .calculs.pompage import predimensionner_pompe, verifier_npsh
from .calculs.plomberie import dimensionner_troncon_plomberie
from .calculs.radier import verifier_radier_ancrage

# --- Application Principale du Plugin ---
app = typer.Typer(
    name="hydro", 
    help="Plugin complet pour l'hydrologie et l'hydraulique (Hydrodrain)."
)

# --- I. Groupe de commandes : Données Pluviométriques ---
pluvio_app = typer.Typer(name="pluvio", help="Gestion et Analyse des Données Pluviométriques.")
app.add_typer(pluvio_app)

@pluvio_app.command("analyser")
def pluvio_analyser(filepath: str):
    """Analyse statistique de données de pluie brutes depuis un fichier."""
    print(f"PLACEHOLDER: Analyse statistique du fichier {filepath}...")

@pluvio_app.command("ajuster-loi")
def pluvio_ajuster(filepath: str, loi: str = "gumbel"):
    """Ajuste les pluies maximales à une loi statistique."""
    print(f"PLACEHOLDER: Ajustement des données de {filepath} à la loi {loi}...")

@pluvio_app.command("generer-idf")
def pluvio_generer_idf(filepath: str, modele: str = "montana"):
    """Génère les courbes IDF à partir de données ajustées."""
    print(f"PLACEHOLDER: Génération des courbes IDF ({modele}) pour les données de {filepath}...")

# --- II. Groupe de commandes : Analyse Hydrologique ---
hydro_app = typer.Typer(name="bassin", help="Analyse Hydrologique et Modélisation des Bassins Versants.")
app.add_typer(hydro_app)

@hydro_app.command("caracteriser")
def hydro_caracteriser(filepath: str):
    """Calcule les paramètres physiques d'un bassin versant."""
    print(f"PLACEHOLDER: Caractérisation du bassin versant depuis {filepath}...")

@hydro_app.command("estimer-crue")
def hydro_estimer_crue(filepath: str, methode: str = "rationnelle"):
    """Estime le débit de pointe d'un bassin versant."""
    print(f"PLACEHOLDER: Estimation de crue ({methode}) pour le bassin de {filepath}...")

# --- III. Groupe de commandes : Dimensionnement d'Ouvrages ---
ouvrages_app = typer.Typer(name="ouvrage", help="Dimensionnement et Analyse Hydraulique des Ouvrages.")
app.add_typer(ouvrages_app)

@ouvrages_app.command("franchissement")
def ouvrages_franchissement(
    filepath: str = typer.Argument(..., help="Chemin vers le fichier de données du projet (.yml)"),
    periode_retour: int = typer.Option(100, help="Période de retour pour le calcul (ans)"),
    methode_crue: str = typer.Option("orstom", help="Méthode de calcul de crue (orstom ou cieh)"),
    tirant_air: float = typer.Option(1.5, help="Tirant d'air de sécurité (m)"),
    rapport_path: str = typer.Option(None, help="Chemin pour sauvegarder le rapport PDF")
):
    """Dimensionne un ouvrage de franchissement (pont, dalot) à partir d'un fichier de données."""
    print(f"--- Lancement du Dimensionnement Hydraulique du Pont ---")
    print(f"Fichier de données : {filepath}")
    
    # --- PHASE 1 : LECTURE DES DONNÉES (PLACEHOLDER) ---
    # TODO: Implémenter la lecture du fichier YAML
    donnees_projet = {
        "pluies_max_journalieres": [100, 120, 90, 150, 110], # Exemple
        "bassin_versant": {"superficie_km2": 150, "pente_globale": 0.02, "pluvio_annuelle_mm": 1200},
        "cours_eau": {"pente": 0.001, "profil": {}, "largeur_lit": 50},
        "ouvrage": {"largeur_pile": 1.0}
    }
    print("PHASE 1: Données du projet chargées.")

    # --- PHASE 2 : ÉTUDE HYDROLOGIQUE ---
    pluie_decennale = hydrologie.calculer_pluie_decennale_gumbel(donnees_projet["pluies_max_journalieres"])
    
    if methode_crue == "orstom":
        debit_decennal = hydrologie.estimer_crue_decennale_orstom(donnees_projet["bassin_versant"], pluie_decennale)
    elif methode_crue == "cieh":
        debit_decennal = hydrologie.estimer_crue_decennale_cieh(donnees_projet["bassin_versant"])
    else:
        print(f"Erreur : méthode de crue '{methode_crue}' non reconnue.")
        raise typer.Exit(code=1)
        
    debit_projet_q100 = hydrologie.calculer_debit_projet_centennal(debit_decennal, 1.05, 2.0)
    print(f"PHASE 2: Débit de projet (Q100) calculé : {debit_projet_q100:.2f} m³/s")

    # --- PHASE 3 : ÉTUDE HYDRAULIQUE ---
    phe = hydraulique.calculer_phe_manning_strickler(donnees_projet["cours_eau"]["profil"], debit_projet_q100, donnees_projet["cours_eau"]["pente"])
    remous = hydraulique.calculer_remous(1.5, donnees_projet["ouvrage"]) # Vitesse amont = 1.5 m/s en placeholder
    cote_sous_poutre = phe + remous + tirant_air
    print(f"PHASE 3: PHE = {phe:.2f}m | Remous = {remous:.2f}m | Côte sous poutre = {cote_sous_poutre:.2f}m")

    # --- PHASE 4 : ANALYSE DE STABILITÉ ---
    affouillements = hydraulique.calculer_affouillement(debit_projet_q100, donnees_projet["cours_eau"]["largeur_lit"], donnees_projet["ouvrage"]["largeur_pile"])
    print(f"PHASE 4: Affouillement total estimé : {affouillements['total']:.2f}m")
    
    # --- PHASE 5 : SYNTHÈSE ---
    print("\n--- RÉSULTATS FINAUX ---")
    print(f"Débit de projet (Q100): {debit_projet_q100:.2f} m³/s")
    print(f"Hauteur des Plus Hautes Eaux (PHE): {phe:.2f} m")
    print(f"Hauteur sous poutre requise: {cote_sous_poutre:.2f} m")
    print(f"Profondeur d'affouillement maximale: {affouillements['total']:.2f} m")

    if rapport_path:
        # TODO: Appeler une fonction de génération de rapport PDF
        print(f"\nTODO: Générer le rapport dans {rapport_path}")

@ouvrages_app.command("reseau-assainissement")
def ouvrages_reseau(filepath: str, methode: str = "hardy-cross"):
    """Dimensionne et analyse un réseau d'assainissement."""
    run_legacy_assainissement()

@ouvrages_app.command("bassin-retention")
def ouvrages_bassin(filepath: str):
    """Analyse et dimensionne un bassin de rétention."""
    print(f"PLACEHOLDER: Calcul de l'intensité seuil et du volume pour le bassin de {filepath}...")

@ouvrages_app.command("dalot-verifier")
def ouvrages_dalot_verifier(
    largeur: float = typer.Option(..., help="Largeur d'une cellule (m)"),
    hauteur: float = typer.Option(..., help="Hauteur d'une cellule (m)"),
    nombre_cellules: int = typer.Option(1, help="Nombre de cellules identiques"),
    longueur: float = typer.Option(..., help="Longueur de l'ouvrage (m)"),
    pente: float = typer.Option(..., help="Pente de l'ouvrage (m/m)"),
    debit_projet: float = typer.Option(..., help="Débit de projet à évacuer (m³/s)"),
    manning: float = typer.Option(0.013, help="Coefficient de rugosité de Manning")
):
    """Vérifie les performances hydrauliques d'un dalot ou d'une buse."""
    print("--- Lancement de la Vérification Hydraulique du Dalot ---")
    
    donnees_entree = {
        "largeur_m": largeur,
        "hauteur_m": hauteur,
        "nombre_cellules": nombre_cellules,
        "longueur_m": longueur,
        "pente_m_m": pente,
        "debit_projet_m3s": debit_projet,
        "manning": manning
    }
    
    resultats = verifier_dalot(donnees_entree)
    
    print("\n--- RÉSULTATS DE LA VÉRIFICATION ---")
    print(json.dumps(resultats, indent=2, ensure_ascii=False))

@ouvrages_app.command("deversoir-dimensionner")
def ouvrages_deversoir_dimensionner(
    debit_projet: float = typer.Option(..., help="Débit de la crue de projet (m³/s)"),
    cote_barrage: float = typer.Option(..., help="Côte de la crête du barrage principal (m NGF)"),
    cote_deversoir: float = typer.Option(..., help="Côte de la crête du déversoir (m NGF)"),
    revanche: float = typer.Option(1.0, help="Revanche de sécurité sur le barrage (m)"),
    profil: str = typer.Option("creager", help="Profil de la crête (creager, seuil_epais, paroi_mince)")
):
    """Dimensionne la longueur d'un déversoir de crue à seuil fixe."""
    print("--- Lancement du Dimensionnement du Déversoir de Crue ---")
    
    donnees_entree = {
        "debit_projet_m3s": debit_projet,
        "cote_crete_barrage_m": cote_barrage,
        "revanche_m": revanche,
        "cote_crete_deversoir_m": cote_deversoir,
        "profil_crete": profil
    }
    
    resultats = dimensionner_deversoir(donnees_entree)
    
    print("\n--- RÉSULTATS DU DIMENSIONNEMENT ---")
    print(json.dumps(resultats, indent=2, ensure_ascii=False))

@ouvrages_app.command("canal-dimensionner")
def ouvrages_canal_dimensionner(
    debit_projet: float = typer.Option(..., help="Débit de projet (m³/s)"),
    pente: float = typer.Option(..., help="Pente du canal (m/m)"),
    k_strickler: float = typer.Option(..., help="Coefficient de Strickler"),
    fruit_talus: float = typer.Option(..., help="Fruit des talus (m/m)"),
    vitesse_imposee: float = typer.Option(..., help="Vitesse d'écoulement imposée (m/s)")
):
    """Dimensionne un canal à ciel ouvert."""
    print("--- Lancement du Dimensionnement du Canal ---")
    donnees = {
        "debit_projet_m3s": debit_projet,
        "pente_m_m": pente,
        "k_strickler": k_strickler,
        "fruit_talus_m_m": fruit_talus,
        "vitesse_imposee_ms": vitesse_imposee
    }
    resultats = dimensionner_canal(donnees)
    print(json.dumps(resultats, indent=2))

@ouvrages_app.command("pompe-predimensionner")
def ouvrages_pompe_predimensionner(
    debit_pompage: float = typer.Option(..., help="Débit de pompage (m³/s)"),
    cote_refoulement: float = typer.Option(..., help="Cote de refoulement (m NGF)"),
    cote_aspiration: float = typer.Option(..., help="Cote d'aspiration minimale (m NGF)"),
    longueur_conduite: float = typer.Option(..., help="Longueur de la conduite (m)"),
    diametre_conduite: float = typer.Option(..., help="Diamètre de la conduite (m)"),
    pertes_k: str = typer.Option("0.0", help="Coefficients de pertes singulières (virgules)")
):
    """Prédimensionne une station de pompage."""
    print("--- Lancement du Prédimensionnement de la Pompe ---")
    donnees = {
        "debit_pompage_m3s": debit_pompage,
        "cote_refoulement_m": cote_refoulement,
        "cote_aspiration_min_m": cote_aspiration,
        "longueur_conduite_m": longueur_conduite,
        "diametre_conduite_m": diametre_conduite,
        "pertes_singulieres_k": [float(k) for k in pertes_k.split(',')]
    }
    resultats = predimensionner_pompe(donnees)
    print(json.dumps(resultats, indent=2))

@ouvrages_app.command("pompe-verifier-npsh")
def ouvrages_pompe_verifier_npsh(
    debit_pompage: float = typer.Option(..., help="Débit de pompage (m³/s)"),
    cote_aspiration: float = typer.Option(..., help="Cote d'aspiration minimale (m NGF)"),
    diametre_conduite: float = typer.Option(..., help="Diamètre de la conduite d'aspiration (m)"),
    longueur_aspiration: float = typer.Option(..., help="Longueur de la conduite d'aspiration (m)"),
    npsh_requis: float = typer.Option(..., help="NPSH requis par la pompe (m)"),
    temp_eau: float = typer.Option(20.0, help="Température de l'eau (°C)")
):
    """Vérifie le NPSH disponible pour une pompe."""
    print("--- Lancement de la Vérification du NPSH ---")
    donnees = {
        "debit_pompage_m3s": debit_pompage,
        "cote_aspiration_min_m": cote_aspiration,
        "diametre_conduite_aspiration_m": diametre_conduite,
        "longueur_conduite_aspiration_m": longueur_aspiration,
        "npsh_requis_m": npsh_requis,
        "temperature_eau_c": temp_eau
    }
    resultats = verifier_npsh(donnees)
    print(json.dumps(resultats, indent=2))

@ouvrages_app.command("radier-verifier-ancrage")
def ouvrages_radier_verifier_ancrage(
    surface_radier: float = typer.Option(..., help="Surface du radier (m²)"),
    poids_radier: float = typer.Option(..., help="Poids propre du radier (kN)"),
    poids_remblai: float = typer.Option(..., help="Poids du remblai sur le radier (kN)"),
    niveau_nappe: float = typer.Option(..., help="Niveau de la nappe phréatique (m NGF)"),
    niveau_fond_radier: float = typer.Option(..., help="Niveau du fond du radier (m NGF)"),
    coeff_securite: float = typer.Option(1.1, help="Coefficient de sécurité requis")
):
    """Vérifie la stabilité à l'ancrage d'un radier sous l'effet de la sous-pression."""
    print("--- Lancement de la Vérification d'Ancrage du Radier ---")
    donnees = {
        "surface_radier_m2": surface_radier,
        "poids_radier_kn": poids_radier,
        "poids_remblai_kn": poids_remblai,
        "niveau_nappe_ngf": niveau_nappe,
        "niveau_fond_radier_ngf": niveau_fond_radier,
        "coeff_securite_requis": coeff_securite
    }
    resultats = verifier_radier_ancrage(donnees)
    print(json.dumps(resultats, indent=2))

# --- IV. Groupe de commandes : Plomberie ---
plomberie_app = typer.Typer(name="plomberie", help="Dimensionnement des réseaux internes de plomberie.")
app.add_typer(plomberie_app)

@plomberie_app.command("troncon-dimensionner")
def plomberie_troncon_dimensionner(
    nb_appareils: int = typer.Option(..., help="Nombre d'appareils sur le tronçon"),
    somme_debits_base: float = typer.Option(..., help="Somme des débits de base (L/s)")
):
    """Dimensionne un tronçon de tuyauterie de plomberie."""
    print("--- Lancement du Dimensionnement du Tronçon ---")
    donnees = {
        "nombre_appareils": nb_appareils,
        "somme_debits_base_ls": somme_debits_base
    }
    resultats = dimensionner_troncon_plomberie(donnees)
    print(json.dumps(resultats, indent=2))

# --- V. Groupe de commandes : Utilitaires ---
utils_app = typer.Typer(name="util", help="Utilitaires et Analyses Spécifiques.")
app.add_typer(utils_app)

@utils_app.command("prevoir-population")
def utils_population(filepath: str):
    """Estime l'évolution d'une population."""
    print(f"PLACEHOLDER: Prévision de population à partir des données de {filepath}...")

@utils_app.command("estimer-demande-eau")
def utils_demande_eau(filepath: str):
    """Estime la demande en eau d'une agglomération."""
    print(f"PLACEHOLDER: Estimation de la demande en eau depuis {filepath}...")

@utils_app.command("diagramme-ombro")
def utils_diagramme(filepath: str):
    """Génère un diagramme ombrothermique."""
    print(f"PLACEHOLDER: Création du diagramme ombrothermique depuis {filepath}...")

# --- Point d'entrée pour l'enregistrement du plugin ---
def register():
    return app
