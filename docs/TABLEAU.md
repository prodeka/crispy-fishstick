
1.  **Une "Bibliothèque de Templates" (`TABLE_TEMPLATES`) :** Elle contiendra la définition de chaque tableau que vous avez listé.
2.  **Une Fonction d'Initialisation (`initialize_log_data`) :** Cette fonction prendra en entrée le nom d'un tableau et générera un objet Python (dictionnaire) pré-rempli avec des valeurs par défaut (`None` ou des chaînes vides), prêt à être peuplé par vos calculs.

Cela vous fera gagner un temps considérable et garantira que toutes les données de log respectent scrupuleusement le format attendu par vos templates Jinja2.

---

### **Le Module Python : `lcpi/reporting/table_templates.py`**

Créez ce nouveau fichier dans votre projet. Il contiendra la définition centralisée de toutes vos structures de tableaux.

```python
# lcpi/reporting/table_templates.py

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

```

---

### **Comment Utiliser ce Module dans votre Workflow**

Voici le workflow complet, de l'intérieur d'une commande de calcul jusqu'à la journalisation.

**Exemple : Dans votre commande `lcpi aep dimensionnement_reservoir`**

```python
# Importez la fonction d'initialisation au début de votre fichier de commande
from lcpi.reporting.table_templates import initialize_log_data

# ...
# Dans votre fonction de commande, après avoir effectué les calculs...
# ...

# 1. Initialiser la structure de données du log pour le tableau
# On utilise l'identifiant 'recap_reservoir'
log_reservoir = initialize_log_data('recap_reservoir')

# 2. Peuplez les données avec vos résultats de calcul.
# C'est ici que la magie opère : vous remplissez les valeurs 'None'.
# On peut le faire avec une fonction d'aide pour plus de propreté.
def fill_data(log_obj, parametre, valeur):
    for item in log_obj['donnees']:
        if item['Paramètre'] == parametre:
            item['Valeur'] = valeur
            break

fill_data(log_reservoir, "Identification du Réservoir", "R1 (Gapé-Centre)")
fill_data(log_reservoir, "Altitude au sol", f"{altitude_calculee} m")
fill_data(log_reservoir, "Volume de Conception retenu", f"{volume_calcule} m³")
# ... et ainsi de suite pour tous les paramètres

# 3. Créez l'objet de log final complet
log_final_complet = {
    "id": "20250815153000",
    "timestamp": "...",
    "titre_calcul": "Dimensionnement du Réservoir de Stockage",
    "commande_executee": "...",
    "donnees_resultat": {
        "tableau_recapitulatif_reservoir": log_reservoir
        # Vous pouvez ajouter d'autres objets ici, comme des graphiques ou d'autres tableaux
    },
    "transparence_mathematique": [
        f"Volume utile = 0.5 * {demande_jour} + {reserve_incendie}",
        "..."
    ]
}

# 4. Sauvegardez ce `log_final_complet` dans un fichier JSON dans votre dossier `logs/`
# (après avoir demandé à l'utilisateur s'il veut le journaliser, bien sûr).

```

### **Avantages de cette Approche**

1.  **Centralisation :** Toutes vos structures de tableau sont définies en un seul endroit. Si vous voulez changer le nom d'une colonne, vous ne le faites qu'une seule fois.
2.  **Robustesse :** La fonction `initialize_log_data` garantit que chaque log est créé avec la bonne structure et les bonnes clés, éliminant les erreurs de frappe et les oublis.
3.  **Simplicité pour les Développeurs :** Le développeur qui code un calcul métier n'a plus à se soucier de la structure exacte du JSON. Il demande simplement un template par son nom, le remplit, et c'est tout.
4.  **Préparation pour le Futur :** Vous pouvez facilement enrichir les définitions dans `TABLE_TEMPLATES` avec plus de métadonnées (unités par défaut, formatage numérique, descriptions des colonnes) pour rendre vos templates Jinja2 encore plus intelligents.