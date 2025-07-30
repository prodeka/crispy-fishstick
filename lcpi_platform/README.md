# Documentation LCPI Platform

## Vue d'ensemble

LCPI Platform est une plateforme modulaire de calculs d'ingénierie civile qui regroupe plusieurs modules spécialisés pour différents domaines de la construction et de l'hydraulique.

## Architecture générale

La plateforme utilise une architecture modulaire basée sur des plugins, avec un système de commandes CLI unifié via Typer.

### Structure des modules

```
lcpi_platform/
├── lcpi_core/          # Module central et utilitaires
├── lcpi_cm/            # Construction Métallique
├── lcpi_bois/          # Construction Bois
├── lcpi_beton/         # Béton Armé
└── lcpi_hydrodrain/    # Hydraulique et Assainissement
```

## Module Core (`lcpi_core/`)

### Fonctionnalités principales

Le module core fournit les fonctionnalités de base pour tous les autres modules :

#### `main.py`
- **Point d'entrée principal** de l'application CLI
- **Système de plugins** : Charge dynamiquement tous les modules disponibles
- **Commande `report`** : Analyse tous les éléments d'un projet et génère un rapport PDF
- **Gestion des chemins** : Configure automatiquement les chemins pour le développement

**Fonctions principales :**
- `report(project_dir)` : Analyse tous les éléments YAML d'un projet
- Chargement automatique des plugins : `lcpi_cm`, `lcpi_bois`, `lcpi_beton`, `lcpi_hydrodrain`

#### `calculs.py`
- **Calculs de sollicitations** pour différents matériaux (acier, bois)
- **Combinaisons d'actions** selon les normes (ELU, ELS)
- **Coefficients psi** pour le bois selon les catégories d'usage

**Fonctions principales :**
- `calculer_sollicitations_completes()` : Calcule toutes les combinaisons d'actions
- `charger_psi_coeffs()` : Charge les coefficients psi depuis le fichier CSV

#### `reporter.py`
- **Génération de rapports PDF** avec ReportLab
- **Formatage des résultats** pour la présentation

**Fonctions principales :**
- `generate_pdf_report()` : Génère un rapport PDF à partir d'une liste de résultats

#### `utils/`
- **`settings.py`** : Configuration globale (mode verbose, etc.)
- **`ui_helpers.py`** : Utilitaires pour l'interface utilisateur
- **`ui_rich.py`** : Interface utilisateur avec Rich

## Module Construction Métallique (`lcpi_cm/`)

### Fonctionnalités

Calculs de poutres en acier avec dimensionnement automatique des profils.

#### `main.py`
- **Commande `calc`** : Calcul d'une ou plusieurs poutres
- **Mode batch** : Traitement par lot via fichiers CSV
- **Format JSON** : Sortie structurée pour intégration
- **Mode interactif** : Interface utilisateur en ligne de commande

**Fonctions principales :**
- `run_calc_from_file()` : Calcul depuis un fichier YAML ou CSV
- `run_interactive_mode()` : Mode interactif
- `register()` : Enregistrement du plugin dans l'application principale

#### `calculs.py`
- **Dimensionnement des profils** en acier
- **Vérification des contraintes** (flexion, cisaillement, déformation)
- **Sélection automatique** des profils selon les catalogues

## Module Construction Bois (`lcpi_bois/`)

### Fonctionnalités

Calculs de structures en bois avec vérification des contraintes et déformations.

#### `main.py`
- **Commande `check`** : Vérification d'éléments en bois
- **Support des classes** de bois selon les normes
- **Calculs selon l'Eurocode 5**

#### `calculs.py`
- **Vérification des contraintes** de flexion et cisaillement
- **Calcul des déformations** (flèche)
- **Coefficients de modification** pour le bois
- **Classes de résistance** du bois

## Module Béton Armé (`lcpi_beton/`)

### Fonctionnalités

Calculs de structures en béton armé avec dimensionnement des armatures.

#### `main.py`
- **Calculs de poutres** en béton armé
- **Dimensionnement des radiers** de fondation
- **Vérification des états limites**

#### `ba_entry.py`
- **Point d'entrée principal** pour les calculs béton
- **Interface unifiée** pour tous les types de calculs

#### `core/`
- **`analysis/`** : Analyse des structures (poutres continues, etc.)
- **`checks/`** : Vérification des états limites de service
- **`design/`** : Dimensionnement (colonnes, radiers, etc.)
- **`materials.py`** : Propriétés des matériaux
- **`sections.py`** : Définition des sections

#### `web_bridge.py`
- **Interface web** pour les calculs béton
- **API REST** pour l'intégration

## Module Hydraulique (`lcpi_hydrodrain/`)

### Fonctionnalités

Calculs hydrauliques pour l'assainissement, les réseaux d'eau et l'hydrologie.

#### `main.py`
- **Calculs d'assainissement** gravitaire
- **Dimensionnement des canalisations**
- **Études hydrologiques** de bassins versants
- **Calculs de pompage** et réservoirs

#### `calculs/`
- **`assainissement_gravitaire.py`** : Réseaux d'assainissement
- **`bassin_versant.py`** : Hydrologie de bassins versants
- **`canal.py`** : Dimensionnement de canaux
- **`climat.py`** : Données climatiques
- **`dalot.py`** : Calculs de dalots
- **`demande_eau.py`** : Consommation d'eau
- **`deversoir.py`** : Déversoirs d'orage
- **`hydraulique.py`** : Calculs hydrauliques
- **`hydrologie.py`** : Études hydrologiques
- **`plomberie.py`** : Réseaux d'eau potable
- **`pluviometrie.py`** : Données pluviométriques
- **`pompage.py`** : Stations de pompage
- **`population.py`** : Projections démographiques
- **`radier.py`** : Radiers hydrauliques
- **`reservoir_aep.py`** : Réservoirs d'eau potable

#### `core/`
- **`engine.py`** : Moteur de calcul principal
- **`models.py`** : Modèles de données
- **`shared_formulas.py`** : Formules partagées

#### `config/`
- **`idf_models.py`** : Modèles IDF (Intensité-Durée-Fréquence)
- **`pluviometrie_sources.py`** : Sources de données pluviométriques

#### `modules/`
- **`hydrologie/`** : Modules hydrologiques spécialisés
  - **`caquot.py`** : Méthode de Caquot
  - **`idf_formulas.py`** : Formules IDF
  - **`rationnelle.py`** : Méthode rationnelle

#### `utils/`
- **`logging_config.py`** : Configuration des logs
- **`security.py`** : Sécurité des données
- **`ui.py`** : Interface utilisateur
- **`utils.py`** : Utilitaires généraux

#### `web_bridge.py`
- **Interface web** pour les calculs hydrauliques
- **API REST** pour l'intégration

#### `reporting.py`
- **Génération de rapports** détaillés
- **Graphiques et visualisations**

#### `plotting.py`
- **Visualisation des résultats** hydrauliques
- **Graphiques de dimensionnement**

## Utilisation

### Installation

```bash
# Installation des dépendances
pip install -r requirements.txt

# Ou installation directe
pip install typer rich pandas pyyaml reportlab
```

### Utilisation en ligne de commande

```bash
# Calcul d'une poutre métallique
python -m lcpi_platform.lcpi_core.main cm calc elements/poutre_P1.yml

# Vérification d'un élément bois
python -m lcpi_platform.lcpi_core.main bois check elements/panne_toiture_P1.yml

# Calcul hydraulique
python -m lcpi_platform.lcpi_core.main hydro calc data/projet_pont_manni.yml

# Rapport complet d'un projet
python -m lcpi_platform.lcpi_core.main report .
```

### Format des fichiers d'entrée

#### YAML pour Construction Métallique
```yaml
longueur: 6.0
nuance: S235
fy_MPa: 235.0
E_MPa: 210000.0
famille_profil: IPE
charges:
  permanentes_G:
    - type: repartie
      valeur: 5.0
  exploitation_Q:
    - type: repartie
      valeur: 3.0
```

#### YAML pour Construction Bois
```yaml
longueur: 4.0
classe_bois: C24
categorie_usage: A
charges:
  permanentes_G:
    - type: repartie
      valeur: 2.0
  exploitation_Q:
    - type: repartie
      valeur: 1.5
```

## Architecture technique

### Système de plugins

La plateforme utilise un système de plugins modulaire :

1. **Découverte automatique** : Les plugins sont chargés dynamiquement
2. **Interface unifiée** : Chaque plugin expose une fonction `register()`
3. **Commandes CLI** : Intégration transparente dans l'application principale

### Gestion des données

- **Format YAML** : Configuration des éléments
- **Format CSV** : Données d'entrée et résultats
- **Format JSON** : Sortie structurée pour intégration
- **Format PDF** : Rapports de calcul

### Extensibilité

La plateforme est conçue pour être facilement extensible :

1. **Ajout de nouveaux modules** : Créer un nouveau dossier avec `main.py`
2. **Nouvelles fonctionnalités** : Étendre les modules existants
3. **Nouveaux formats** : Ajouter des parsers pour d'autres formats

## Dépendances principales

- **Typer** : Interface CLI moderne
- **Rich** : Interface utilisateur riche
- **Pandas** : Manipulation de données
- **PyYAML** : Parsing YAML
- **ReportLab** : Génération de rapports PDF
- **NumPy** : Calculs numériques
- **Matplotlib** : Visualisation (module hydraulique)

## Tests

```bash
# Exécution des tests
python -m pytest tests/

# Tests d'intégration
python -m pytest tests/integration/
```

## Contribution

1. **Structure des modules** : Respecter l'architecture existante
2. **Documentation** : Documenter toutes les nouvelles fonctionnalités
3. **Tests** : Ajouter des tests pour les nouvelles fonctionnalités
4. **Formatage** : Respecter les conventions de code existantes

## Licence

Ce projet est destiné à un usage pédagogique et professionnel dans le domaine de l'ingénierie civile. 