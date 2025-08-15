# src/lcpi/reporting/table_templates.py

"""
Module centralisé pour la définition et l'initialisation des structures
de tableaux destinées à la journalisation et à la génération de rapports.
"""

# Définition de la bibliothèque de templates de tableaux.
# Chaque clé est un identifiant unique pour un type de tableau.
TABLE_TEMPLATES = {
    "enumeration_troncons": {
        "titre_defaut": "Énumération des tronçons du projet",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["DC_ID", "longueur", "NODE1", "NODE2"],
    },
    "dimensionnement_troncons": {
        "titre_defaut": "Récapitulatif du dimensionnement des tronçons",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["DC_ID", "longueur", "Qd (m^3/s)", "DN (mm)", "V (m/s)", "ΔH (m)"],
    },
    "dimensionnement_noeuds": {
        "titre_defaut": "Récapitulatif du dimensionnement des nœuds du réseau",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["JUNCTIONS", "X", "Y", "Z (m)", "P_réel (m)"],
    },
    "recap_reservoir": {
        "titre_defaut": "Récapitulatif du dimensionnement du réservoir",
        "type_tableau": "liste_parametres",
        "parametres": [
            "Identification du Réservoir", "Longitude", "Latitude", "Altitude au sol",
            "Type de Réservoir", "Demande maximale journalière", "Réserve Incendie",
            "Volume de Conception retenu", "Diamètre intérieur de la cuve (D)",
            "Hauteur Utile de la cuve", "Hauteur Totale de la cuve", "Côte du sommet de la cuve",
            "Côte du radier de la cuve", "Hauteur sous Cuve minimale", "Hauteur sous Cuve choisie"
        ],
    },
    "dimensionnement_adduction": {
        "titre_defaut": "Résultats du dimensionnement de la conduite d'adduction",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["Approche", "Dth (mm)", "DN (mm)", "U (m/s)", "Vérification"],
    },
    "calcul_hmt_params": {
        "titre_defaut": "Paramètres de calcul de la HMT",
        "type_tableau": "liste_parametres",
        "parametres": [
            "Qadd (m³/s)", "L_refoulement (m)", "Z_TN_forage (m)", "ND_max (m)",
            "Z_TN_reservoir (m)", "Z_cuve (m)"
        ],
    },
    "calcul_hmt_resultats": {
        "titre_defaut": "Récapitulatif des résultats du calcul de la HMT",
        "type_tableau": "liste_parametres",
        "parametres": ["H_géo (m)", "Δ Hasp+ref (m)", "Pertes_de_charges_cond(ΔH)", "HMT (m)"],
    },
    "verif_coup_belier": {
        "titre_defaut": "Récapitulatif de la vérification du coup de bélier",
        "type_tableau": "liste_parametres",
        "parametres": [
            "Pression Maximale Admissible (PMA)", "Hauteur Manométrique Total (HMT)",
            "Variation maximale de la pression(ΔP)", "Pression Maximale de la conduite (Hmax)",
            "Pression Minimale de la conduite (Hmin)"
        ],
        "unites": "mCE", # On peut ajouter des métadonnées pour aider au formatage
    },
    "fiche_technique_pompe": {
        "titre_defaut": "Fiche technique de la pompe",
        "type_tableau": "liste_parametres",
        "cle_nom": "Désignation",
        "cle_valeur": "Caractéristique",
        "parametres": [
            "Marque", "Nom du produit", "Débit d’exploitation",
            "Hauteur manométrique totale (HMT)", "Puissance nominale P2",
            "Rendement de la pompe"
        ],
    },
    "dimensionnement_pompe": {
        "titre_defaut": "Récapitulatif du dimensionnement de la pompe",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["Paramètre", "Unité", "Valeur"],
    },
    "fiche_technique_groupe_electrogene": {
        "titre_defaut": "Fiche technique du groupe électrogène",
        "type_tableau": "liste_parametres",
        "parametres": [
            "Modèle", "Marque", "Puissance nominale maximale",
            "Tension nominale", "Facteur de puissance (cos φ)"
        ],
    },
    "comparatif_diametres_debits": {
        "titre_defaut": "Comparatif des diamètres, DN et débits",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["TRONCONS", "D_CALCULE (mm)", "D_EPANET (mm)", "DN_CALCULE (mm)", "DN_EPANET (mm)", "Q_CALCULER (m³/s)", "Q_EPANET (m³/s)"],
    },
    "comparatif_vitesses_pertes": {
        "titre_defaut": "Comparatif des vitesses et pertes de charges",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["TRONCONS", "V_CALCULE (m/s)", "V_EPANET (m/s)", "ΔH_i_CALCULER (m)", "ΔH_i_EPANET (m)"],
    },
    "comparatif_pressions": {
        "titre_defaut": "Comparatif des pressions",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["JUNCTIONS", "P_CALCULE (m)", "P_EPANET (m)"],
    },
    "recap_diametres_conduites": {
        "titre_defaut": "Récapitulatif des diamètres des conduites",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["Diamètre nominal (mm)", "Longueur Distribution", "Longueur refoulement", "Longueurs totales"],
    },
    "dimensionnement_fouilles": {
        "titre_defaut": "Résumé du dimensionnement des fouilles",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["Diamètre Nominal", "Largeur de fouille (m)", "Profondeur de fouille (m)", "Largeurs retenues (m)", "Profondeur retenue (m)"],
    },
    "devis_estimatif": {
        "titre_defaut": "Devis estimatif et quantitatif des travaux",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["N°", "Désignations", "Unité", "Quantité", "Prix Unitaire", "MONTANT"],
    },
    "amortissement_charges": {
        "titre_defaut": "Récapitulatif de l'amortissement et charges de fonctionnement",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["Désignation", "Montant mensuel (FCFA)", "Montant annuel (FCFA)", "Coefficient (%)", "Montant total (FCFA)"],
    },
    "charges_personnel": {
        "titre_defaut": "Récapitulatif des charges de personnel",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["Désignation", "Nombre", "Salaire et prime mensuel (FCFA)", "Montant annuel (FCFA)", "Montant total Unitaire (FCFA)"],
    },
    "milieux_affectes": {
        "titre_defaut": "Liste des milieux affectés par les activités",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["Milieu", "Aspect affecté"],
    },
    "activites_impact": {
        "titre_defaut": "Activités sources d’impact par phase",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["Phase", "Activités"],
    },
    "evaluation_impacts_negatifs": {
        "titre_defaut": "Évaluation des impacts négatifs",
        "type_tableau": "liste_enregistrements",
        "colonnes": ["Impact", "Intensité", "Étendue", "Durée", "Importance Absolue", "Importance Relative"],
    },
}

def initialize_log_data(template_name: str, titre_personnalise: str = None) -> dict:
    """
    Initialise la structure de données pour un tableau de log spécifique.
    
    Args:
        template_name (str): Le nom du template de tableau (ex: 'recap_reservoir').
        titre_personnalise (str, optional): Un titre pour surcharger le titre par défaut.
    
    Returns:
        dict: Un dictionnaire pré-rempli avec des valeurs nulles, prêt à être utilisé.
              Retourne None si le template_name est inconnu.
    """
    if template_name not in TABLE_TEMPLATES:
        print(f"Erreur : Le template de tableau '{template_name}' est inconnu.")
        return None

    template = TABLE_TEMPLATES[template_name]
    
    log_data_object = {
        "type_tableau": template_name,
        "titre": titre_personnalise or template.get("titre_defaut", "Titre non défini"),
    }

    if template["type_tableau"] == "liste_enregistrements":
        # Pour ce type, les données sont une liste de dictionnaires.
        # On initialise avec une liste vide. C'est à la fonction de calcul
        # de remplir cette liste avec des dictionnaires ayant les bonnes clés.
        log_data_object["donnees"] = []
        
    elif template["type_tableau"] == "liste_parametres":
        # Pour ce type, les données sont une liste de paires clé/valeur.
        # On peut pré-remplir la structure avec des valeurs nulles.
        cle_nom = template.get("cle_nom", "Paramètre")
        cle_valeur = template.get("cle_valeur", "Valeur")
        
        donnees_initiales = []
        for param in template.get("parametres", []):
            donnees_initiales.append({cle_nom: param, cle_valeur: None})
        
        log_data_object["donnees"] = donnees_initiales

    return log_data_object
