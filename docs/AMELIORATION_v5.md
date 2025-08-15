# AMELIORATION_v5 - Feuille de Route d'Implémentation

## 📋 **Contexte**

Ce document constitue la feuille de route pour l'implémentation des fonctionnalités et améliorations techniques définies dans `AMELIORATION_v4`. L'objectif est de transformer la vision stratégique en un plan d'action concret, phasé et réalisable.

Cette feuille de route intègre directement les extraits de code, schémas de données et templates "prêts à l'emploi" de la v4 pour servir de guide de référence unique à l'équipe de développement.

---

## 🚀 **PHASE 1 : Refactoring du Cœur et Consolidation des Fondations**

**Objectif :** Solidifier l'architecture logicielle avant d'ajouter de nouvelles fonctionnalités majeures. Cette phase est interne et vise à améliorer la qualité, la robustesse et la maintenabilité du code.

| Priorité | Tâche | Description | Technologies Clés |
|---|---|---|---|
| **Haute** | **1. Intégration de Pydantic** | Remplacer la validation manuelle des fichiers YAML par des modèles Pydantic. | `Pydantic`, `YAML` |
| **Haute** | **2. Application du "Strategy Pattern"** | Refactorer la sélection des algorithmes (Hazen-Williams vs. Darcy-Weisbach) | POO, Design Patterns |
| **Moyenne**| **3. Amélioration de l'UX CLI avec `Rich`** | Intégrer des composants `Rich` de base pour améliorer l'expérience utilisateur. | `Rich` |
| **Moyenne**| **4. Parallélisation des Calculs** | Utiliser `joblib` ou `multiprocessing` pour paralléliser les évaluations de l'AG et les analyses Monte-Carlo. | `joblib` |
| **Basse** | **5. Optimisation avec `Numba`** | Appliquer le décorateur `@numba.jit` aux fonctions mathématiques intensives. | `Numba` |

### **Implémentation de Référence - Phase 1**

#### **Exemple de Modèle Pydantic pour la validation du YAML (`Tâche 1`)**

```python
from pydantic import BaseModel, Field, Dict, List

class Noeud(BaseModel):
    role: str
    cote_m: float
    demande_m3_s: float = 0.0
    pression_min_mce: int = Field(20, gt=0)
    pression_max_mce: int = Field(80, gt=0)
    profil_consommation: str = "residential"

class Conduite(BaseModel):
    noeud_amont: str
    noeud_aval: str
    longueur_m: float = Field(..., gt=0)
    diametre_m: float = Field(..., gt=0)
    rugosite: float
    materiau: str
    statut: str = "existant"
    coefficient_frottement: str = "hazen_williams"

class ReseauCompletConfig(BaseModel):
    nom: str
    type: str
    noeuds: Dict[str, Noeud]
    conduites: Dict[str, Conduite]
    boucles: Dict[str, List[str]] = None

# Utilisation dans le code:
# import yaml
# config_dict = yaml.safe_load(open("reseau.yml"))
# try:
#     config = ReseauCompletConfig(**config_dict["reseau_complet"])
# except ValidationError as e:
#     print(e)
```

---

## 🎯 **PHASE 2 : Implémentation du Workflow `network-complete-unified`**

**Objectif :** Livrer la première fonctionnalité majeure de l'analyse de réseau de bout en bout, en se concentrant sur la commande `network-complete-unified`.

| Priorité | Tâche | Description | Entrées / Sorties |
|---|---|---|---|
| **Haute** | **1. Calcul Hardy-Cross** | Implémenter l'algorithme de Hardy-Cross. | **Entrée:** `reseau.yml`. **Sortie:** Débits corrigés. |
| **Haute** | **2. Génération de Fichier EPANET** | Créer la logique pour générer un fichier `.inp` valide. | **Entrée:** `reseau.yml`. **Sortie:** `reseau.inp`. |
| **Moyenne**| **3. Post-Traitement et Vérifications** | Ajouter les vérifications automatiques des contraintes. | **Entrée:** Résultats. **Sortie:** Rapport de violations. |
| **Haute** | **4. Contrat de Sortie JSON** | Implémenter la génération du contrat de sortie JSON canonique. | **Sortie:** `results.json`. |
| **Haute** | **5. Tests Unitaires et d'Intégration** | Développer une suite de tests complète pour le workflow. | `pytest` |

### **Implémentation de Référence - Phase 2**

#### **Schéma YAML d'Entrée (`reseau_complet`)**

```yaml
reseau_complet:
  nom: "Réseau Principal"
  type: "maillé"
  noeuds:
    N1:
      role: "reservoir"
      cote_m: 150.0
    N2:
      role: "consommation"
      cote_m: 145.0
      demande_m3_s: 0.02
    N3:
      role: "consommation"
      cote_m: 140.0
      demande_m3_s: 0.015
  conduites:
    C1:
      noeud_amont: "N1"
      noeud_aval: "N2"
      longueur_m: 500
      diametre_m: 0.2
      rugosite: 100
      materiau: "acier"
    C2:
      noeud_amont: "N2"
      noeud_aval: "N3"
      longueur_m: 300
      diametre_m: 0.15
      rugosite: 120
      materiau: "pvc"
hardy_cross:
  tolerance: 1e-6
  max_iterations: 200
  methode: "hazen_williams"
epanet:
  run_options:
    duration_h: 24
    timestep_min: 60
post_traitement:
  verifications:
    vitesse_min_m_s: 0.5
    pression_min_mce: 20
```

#### **Contrat de Sortie JSON Canonique (`Tâche 4`)**

```json
{
  "run_info": {
    "lcpi_version": "1.5.0",
    "timestamp_utc": "2025-08-16T10:00:00Z",
    "input_file_hash": "sha256:abcdef..."
  },
  "inputs": {
    "reseau_complet": { /* données d'entrée validées */ }
  },
  "diagnostics": {
    "connectivite_ok": true,
    "boucles_detectees": 3,
    "epanet_compatible": true
  },
  "hardy_cross": {
    "convergence": {
      "converge": true,
      "iterations": 12,
      "temps_calcul_s": 0.15
    },
    "resultats": {
      "debits_finaux": { "C1": 0.05, "C2": 0.03 },
      "pertes_charge": { "C1": 1.2, "C2": 0.8 }
    }
  },
  "epanet": {
    "fichier_generer": "reseau.inp",
    "execution": {
      "succes": true
    },
    "resultats": {
      "pressions": { "N2": 25.5, "N3": 22.1 },
      "vitesses": { "C1": 1.1, "C2": 0.9 }
    }
  },
  "post_traitement": {
    "verifications": {
      "vitesse_ok": true,
      "pression_ok": false,
      "violations": [
        {"noeud": "N3", "parametre": "pression", "valeur": 18.5, "seuil": 20}
      ]
    }
  }
}
```

---

## 🔬 **PHASE 3 : Analyse Avancée et Optimisation**

**Objectif :** Mettre en œuvre les fonctionnalités d'optimisation, d'analyse de sensibilité et de comparaison.

| Priorité | Tâche | Description | Algorithmes / Sorties |
|---|---|---|---|
| **Haute** | **1. Commande `network-optimize-unified`** | Implémenter l'optimisation des diamètres. | Algorithme Génétique |
| **Moyenne**| **2. Commande `network-sensitivity-unified`** | Permettre l'analyse de sensibilité des paramètres clés. | Monte-Carlo, Sobol |
| **Moyenne**| **3. Commande `network-compare-unified`** | Comparer deux ou plusieurs variantes de réseau. | **Sortie:** `comparison.xlsx` |
| **Haute** | **4. Contrat de Sortie JSON (Optimisation)** | Implémenter la génération du contrat de sortie pour l'optimisation. | **Sortie:** `optimization.json` |

### **Implémentation de Référence - Phase 3**

#### **Schéma YAML d'Entrée (`optimisation`)**

```yaml
optimisation:
  criteres:
    principal: "cout"
    secondaires: ["energie", "performance"]
    poids: [0.6, 0.25, 0.15]
  contraintes:
    budget:
      cout_max_euros: 100000
    techniques:
      pression_min_mce: 20
      vitesse_max_m_s: 2.5
  algorithmes:
    type: "genetique"
    parametres:
      population_size: 100
      generations: 50
      mutation_rate: 0.1
  diametres_candidats:
    commerciaux: [90, 110, 125, 140, 160, 200, 250]
    couts_euros_m: [35, 45, 60, 80, 100, 150, 250]
```

#### **Contrat de Sortie JSON pour l'Optimisation (`Tâche 4`)**

```json
{
  "optimisation": {
    "algorithme": "genetique",
    "convergence": {
      "iterations": 45,
      "fitness_finale": 0.92,
      "temps_calcul_s": 125.3
    },
    "meilleure_solution": {
      "diametres": {
        "C1": 200,
        "C2": 160,
        "C3": 125
      },
      "performance": {
        "cout_total_euros": 85000,
        "energie_totale_kwh": 3200,
        "performance_hydraulique": 0.95
      }
    },
    "pareto_front": [
      { "cout": 85000, "energie": 3200, "performance": 0.95 },
      { "cout": 95000, "energie": 2800, "performance": 0.92 }
    ]
  },
  "analyse_sensibilite": {
    "parametres_critiques": [
      { "parametre": "rugosite", "indice_sobol": 0.45, "impact": "eleve" },
      { "parametre": "demande", "indice_sobol": 0.32, "impact": "moyen" }
    ],
    "robustesse": {
      "score_global": 0.78,
      "zones_critiques": ["N3", "C2"]
    }
  }
}
```

---

##  **PHASE 4 : Moteur de Reporting Professionnel**

**Objectif :** Créer le système de génération de rapports, une fonctionnalité à très haute valeur ajoutée pour la production de livrables de qualité.

| Priorité | Tâche | Description | Livrables |
|---|---|---|---|
| **Haute** | **1. Module `table_templates.py`** | Centraliser la définition de toutes les structures de tableaux. | `table_templates.py` |
| **Haute** | **2. Implémentation des Templates Jinja2** | Créer l'arborescence et coder les templates principaux. | Fichiers `.html`, `.css` |
| **Haute** | **3. Logique de la Commande `lcpi rapport`** | Développer la logique de génération de rapport. | Commande `lcpi rapport` |
| **Moyenne**| **4. Export Multi-Format** | Intégrer `WeasyPrint` pour PDF et `python-docx` pour DOCX. | PDF, DOCX |

### **Implémentation de Référence - Phase 4**

#### **Module `lcpi/reporting/table_templates.py` (`Tâche 1`) - Version Complète**

Ce fichier doit être créé avec la liste exhaustive des tableaux pour garantir la standardisation.

```python
# lcpi/reporting/table_templates.py

"""
Module centralisé pour la définition et l'initialisation des structures
de tableaux destinées à la journalisation et à la génération de rapports.
"""

TABLE_TEMPLATES = {
    "enumeration_troncons": { "titre_defaut": "Énumération des tronçons", "type_tableau": "liste_enregistrements", "colonnes": ["DC_ID", "longueur", "NODE1", "NODE2"]},
    "dimensionnement_troncons": { "titre_defaut": "Dimensionnement des tronçons", "type_tableau": "liste_enregistrements", "colonnes": ["DC_ID", "longueur", "Qd (m^3/s)", "DN (mm)", "V (m/s)", "ΔH (m)"]},
    "dimensionnement_noeuds": { "titre_defaut": "Dimensionnement des nœuds", "type_tableau": "liste_enregistrements", "colonnes": ["JUNCTIONS", "X", "Y", "Z (m)", "P_réel (m)"]},
    "recap_reservoir": { "titre_defaut": "Dimensionnement du réservoir", "type_tableau": "liste_parametres", "parametres": ["Identification", "Altitude", "Volume de Conception", "Hauteur sous Cuve"]},
    "dimensionnement_adduction": { "titre_defaut": "Dimensionnement de l'adduction", "type_tableau": "liste_enregistrements", "colonnes": ["Approche", "Dth (mm)", "DN (mm)", "U (m/s)", "Vérification"]},
    "calcul_hmt_resultats": { "titre_defaut": "Calcul de la HMT", "type_tableau": "liste_parametres", "parametres": ["H_géo (m)", "Pertes_de_charges_cond(ΔH)", "HMT (m)"]},
    "verif_coup_belier": { "titre_defaut": "Vérification du coup de bélier", "type_tableau": "liste_parametres", "parametres": ["Pression Maximale Admissible (PMA)", "Pression Maximale (Hmax)", "Pression Minimale (Hmin)"]},
    "fiche_technique_pompe": { "titre_defaut": "Fiche technique de la pompe", "type_tableau": "liste_parametres", "parametres": ["Marque", "Débit d’exploitation", "HMT", "Puissance nominale P2"]},
    "comparatif_diametres_debits": { "titre_defaut": "Comparatif diamètres et débits", "type_tableau": "liste_enregistrements", "colonnes": ["TRONCONS", "D_CALCULE (mm)", "D_EPANET (mm)", "DN_CALCULE (mm)", "DN_EPANET (mm)", "Q_CALCULER (m³/s)", "Q_EPANET (m³/s)"]},
    "comparatif_vitesses_pertes": { "titre_defaut": "Comparatif vitesses et pertes de charges", "type_tableau": "liste_enregistrements", "colonnes": ["TRONCONS", "V_CALCULE (m/s)", "V_EPANET (m/s)", "ΔH_i_CALCULER (m)", "ΔH_i_EPANET (m)"]},
    "comparatif_pressions": { "titre_defaut": "Comparatif des pressions", "type_tableau": "liste_enregistrements", "colonnes": ["JUNCTIONS", "P_CALCULE (m)", "P_EPANET (m)"]},
    "recap_diametres_conduites": { "titre_defaut": "Récapitulatif des diamètres", "type_tableau": "liste_enregistrements", "colonnes": ["Diamètre nominal (mm)", "Longueur Distribution", "Longueur refoulement", "Longueurs totales"]},
    "devis_estimatif": { "titre_defaut": "Devis estimatif et quantitatif", "type_tableau": "liste_enregistrements", "colonnes": ["N°", "Désignations", "Unité", "Quantité", "Prix Unitaire", "MONTANT"]},
    "evaluation_impacts_negatifs": { "titre_defaut": "Évaluation des impacts négatifs", "type_tableau": "liste_enregistrements", "colonnes": ["Impact", "Intensité", "Étendue", "Durée", "Importance Absolue", "Importance Relative"]},
}

def initialize_log_data(template_name: str, titre_personnalise: str = None) -> dict:
    """Initialise la structure de données pour un tableau de log spécifique."""
    if template_name not in TABLE_TEMPLATES: return None
    template = TABLE_TEMPLATES[template_name]
    log_data_object = {
        "type_tableau": template_name,
        "titre": titre_personnalise or template.get("titre_defaut", "Titre non défini"),
    }
    if template["type_tableau"] == "liste_enregistrements":
        log_data_object["donnees"] = []
    elif template["type_tableau"] == "liste_parametres":
        cle_nom = template.get("cle_nom", "Paramètre")
        cle_valeur = template.get("cle_valeur", "Valeur")
        log_data_object["donnees"] = [{cle_nom: param, cle_valeur: None} for param in template.get("parametres", [])]
    return log_data_object
```

#### **Arborescence et Contenu des Templates (`Tâche 2`)**

La structure du dossier `templates/` reste la même, mais le contenu des fichiers est crucial.

**(Les contenus de `style.css`, `base.html`, `sections/default_calcul.html`, et `tables/recap_reservoir.html` sont identiques à ceux de la v4 et sont supposés être copiés ici.)**

---

## 🧑‍💻 **PHASE 5 : Expérience Utilisateur et Traçabilité**

**Objectif :** Finaliser l'outil avec des fonctionnalités qui améliorent l'ergonomie, la reproductibilité et la traçabilité des calculs.

| Priorité | Tâche | Description |
|---|---|---|
| **Moyenne**| **1. Fichier de Projet `lcpi.yml`** | Utiliser un fichier `lcpi.yml` pour les métadonnées du projet. |
| **Haute** | **2. Journalisation Enrichie** | Ajouter `hash_donnees_entree` et `dependances` aux logs pour une traçabilité complète. |
| **Basse** | **3. Configuration Interactive** | Créer une commande `lcpi aep network-configure --interactive`. |
| **Basse** | **4. Intégration `git`** | Ajouter une option `git init` à `lcpi init`. |

### **Implémentation de Référence - Phase 5**

#### **Exemple de Log Enrichi (`Tâche 2`)**
```json
{
  "id": "20250815153000",
  "titre_calcul": "Dimensionnement des Armatures",
  "commande_executee": "lcpi calcul_armatures --input_calcul 20250815143005.json --log",
  "dependances": ["20250815143005"],
  "hash_donnees_entree": "sha256:abc...",
  "donnees_resultat": { /* ... */ }
}
```

---

## 📦 **PHASE 6 : Scalabilité et Déploiement (Vision à Long Terme)**

**Objectif :** Assurer la pérennité et l'évolutivité du projet en adoptant des pratiques de déploiement modernes.

| Priorité | Tâche | Description |
|---|---|---|
| **Moyenne**| **1. Containerisation avec Docker** | Fournir un `Dockerfile` pour un environnement d'exécution reproductible. |
| **Basse** | **2. Exposition via une API** | Enrober le cœur logique dans une API REST avec `FastAPI` pour de futures interfaces. |
| **Basse** | **3. Backend de Données Performant** | Envisager le support de `Apache Parquet` pour les très grands réseaux. |

---

## ✅ **Résumé de la Feuille de Route V5 (Mise à jour)**

| Phase | Titre | Objectif Principal | Statut |
|---|---|---|---|
| **1** | **Refactoring du Cœur** | Améliorer la qualité et la robustesse du code. | **À faire** |
| **2** | **Workflow Réseau Complet** | Livrer la fonctionnalité d'analyse de réseau de bout en bout. | **À faire** |
| **3** | **Analyse Avancée & Comparaison** | Implémenter les outils d'optimisation, sensibilité et comparaison. | **À faire** |
| **4** | **Moteur de Reporting** | Créer le système de génération de rapports professionnels. | **À faire** |
| **5** | **Expérience Utilisateur & Traçabilité** | Ajouter des fonctionnalités de confort et de gestion de projet. | **À faire** |
| **6** | **Scalabilité & Déploiement** | Préparer l'avenir de l'application. | **À faire** |