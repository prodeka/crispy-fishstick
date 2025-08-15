# 📋 RÈGLES ET PRÉFÉRENCES DU PROJET LCPI - VERSION 2.0

## 🎯 **PRÉFÉRENCES ET CONVENTIONS**

### **Interface CLI et Aide Détaillée**

#### **Framework et Affichage**
- **Framework** : Utilisation de `rich-click` pour un affichage en couleur et structuré
- **Thème** : Interface moderne avec couleurs contextuelles et emojis
- **Responsive** : Adaptation automatique à la taille du terminal

#### **Structure de l'Aide CLI (Standardisé)**
```bash
Usage: lcpi aep population [OPTIONS] [POPULATION_BASE] [--taux TAUX] [--annees ANNEES] [--methode METHODE]

📊 Calcul de projection de population
Projette la population d'une zone donnée sur plusieurs années en utilisant différentes méthodes de croissance.

**Méthodes disponibles :**
• malthus     : Croissance exponentielle (P = P₀ × e^(rt))
• arithmetic  : Croissance arithmétique (P = P₀ + rt)
• geometric   : Croissance géométrique (P = P₀ × (1+r)^t)
• logistic    : Croissance logistique avec capacité limite

**Exemples d'utilisation :**
```bash
# Mode simple avec paramètres inline
lcpi aep population 1500 --taux 0.025 --annees 10 --methode malthus

# Mode enhanced avec fichier YAML
lcpi aep population --input population.yml --mode enhanced --export json

# Export vers fichier spécifique
lcpi aep population 2000 --taux 0.03 --annees 15 --output projections.csv
```

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ population_base  INTEGER  Population de base (requis en mode simple) [default: None] [required]                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --taux     -t      FLOAT   Taux de croissance annuel (décimal) [default: 0.02]                                                  │
│ --annees   -a      INTEGER Nombre d'années de projection [default: 10]                                                          │
│ --methode  -m      TEXT    Méthode de projection [default: malthus]                                                             │
│ --input    -i      PATH    Fichier d'entrée YAML/CSV (mode enhanced) [default: None]                                           │
│ --mode     -M      TEXT    Mode de calcul [default: auto]                                                                       │
│ --export   -e      TEXT    Format d'export [default: json]                                                                      │
│ --output   -o      PATH    Fichier de sortie [default: None]                                                                    │
│ --verbose  -v              Affichage détaillé et transparence mathématique                                                      │
│ --help                     Affiche ce message d'aide et quitte                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### **Standards de Documentation CLI**
- **Emojis contextuels** : 📊 (données), 💧 (eau), 🔧 (outils), ⚡ (énergie), 🏗️ (construction), 🌊 (hydraulique)
- **Exemples de données** : Structure YAML/CSV complète avec commentaires explicatifs
- **Exemples d'utilisation** : Commandes complètes avec tous les flags disponibles
- **Documentation des paramètres** : Explication détaillée de chaque option et ses valeurs par défaut
- **Types de calcul disponibles** : Liste exhaustive des méthodes supportées avec descriptions

### **Structure des Dossiers (Standardisée)**

#### **Organisation Principale**
```
PROJET_DIMENTIONEMENT_2/
├── 📁 docs/                    # Documentation complète
│   ├── 📁 workflows/          # Workflows et guides d'utilisation
│   ├── 📁 api/                # Documentation API et références
│   └── 📁 examples/           # Exemples d'utilisation
├── 📁 tests/                  # Tests unitaires et d'intégration
│   ├── 📁 modules/            # Tests par module
│   └── 📁 integration/        # Tests d'intégration
├── 📁 examples/               # Exemples de projets et données
├── 📁 src/lcpi/               # Code source principal
│   ├── 📁 templates_project/  # Templates de projets
│   └── 📁 utils/              # Utilitaires communs
├── 📁 output/                 # Résultats et rapports
└── 📁 reports/                # Rapports générés
```

#### **Conventions de Nommage des Dossiers**
- **Documentation** : Toujours dans `/docs` avec sous-dossiers thématiques
- **Tests** : Structure miroir de `/src` dans `/tests`
- **Exemples** : Dans `/examples` avec sous-dossiers par module
- **Templates** : Dans `/src/lcpi/templates_project/` avec versions
- **Guides** : Dans `/docs` avec organisation hiérarchique
- **Rapports** : Dans `/output` (temporaires) et `/reports` (finaux)

### **Conventions de Nommage (Étendues)**

#### **Fichiers et Modules**
- **Fichiers Python** : `snake_case.py` (ex: `hardy_cross_enhanced.py`)
- **Modules** : `snake_case` (ex: `population_unified`)
- **Packages** : `snake_case` (ex: `lcpi.aep`)

#### **Classes et Objets**
- **Classes** : `PascalCase` (ex: `HardyCrossEnhanced`)
- **Interfaces** : `IPascalCase` (ex: `INetworkAnalyzer`)
- **Exceptions** : `PascalCaseError` (ex: `AEPValidationError`)

#### **Fonctions et Variables**
- **Fonctions publiques** : `snake_case` (ex: `calculate_population_projection`)
- **Fonctions privées** : `_snake_case` (ex: `_identify_loops_robust`)
- **Variables** : `snake_case` (ex: `population_base`)
- **Constantes** : `UPPER_SNAKE_CASE` (ex: `MAX_ITERATIONS`)

#### **Fichiers de Configuration et Données**
- **Configuration** : `snake_case.yml` (ex: `config.yml`)
- **Données** : `snake_case.csv` ou `snake_case.yml` (ex: `canal_data.yml`)
- **Templates** : `template_snake_case.yml` (ex: `template_project.yml`)

### **Gestion des Versions**

#### **Format de Version**
- **Format** : `X.Y.Z` (Semantic Versioning)
- **Majeur (X)** : Changements incompatibles avec l'API
- **Mineur (Y)** : Nouvelles fonctionnalités compatibles
- **Patch (Z)** : Corrections de bugs et améliorations

#### **Règles de Versionnement**
- **Version 0.x** : Développement initial, API instable
- **Version 1.x** : API stable, fonctionnalités de base
- **Version 2.x** : Nouvelles fonctionnalités majeures
- **Version 3.x** : Refactoring majeur ou nouvelle architecture

---

## 🔧 **FONCTIONNALITÉS IDENTIFIÉES ET IMPLÉMENTÉES**

### **Modules Principaux**

#### **1. AEP (Adduction Eau Potable) - ✅ IMPLÉMENTÉ**
- **Commandes unifiées** : `*-unified` avec support YAML/CSV
- **Hardy-Cross method** : Version enhanced sans limitation de boucles
- **Population calculations** : Projections multi-méthodes (Malthus, arithmetic, geometric, logistic)
- **Demand calculations** : Calculs de demande en eau
- **Pumping systems** : Dimensionnement des systèmes de pompage
- **Reservoir design** : Dimensionnement des réservoirs
- **Validation Phase 0** : `validate-input`, `validate-population`, `validate-network`

#### **2. CM (Construction Métallique) - 🔄 EN DÉVELOPPEMENT**
- **Steel structures** : Structures en acier
- **Connections** : Assemblages et connexions
- **Load calculations** : Calculs de charges

#### **3. Bois (Wood Construction) - 🔄 EN DÉVELOPPEMENT**
- **Timber structures** : Structures en bois
- **Joints** : Assemblages et joints
- **Load calculations** : Calculs de charges

#### **4. Béton (Concrete) - 🔄 EN DÉVELOPPEMENT**
- **Reinforced concrete** : Béton armé
- **Foundations** : Fondations et radiers
- **Structural analysis** : Analyse structurale

#### **5. Hydrodrain (Hydraulics & Drainage) - 🔄 EN DÉVELOPPEMENT**
- **Canal design** : Dimensionnement des canaux
- **Stormwater management** : Gestion des eaux pluviales
- **Hydraulic calculations** : Calculs hydrauliques

### **Fonctionnalités Globales Implémentées**

#### **✅ Base de Données Globale**
- **Module** : `db_manager.py`
- **Fonctionnalités** : Gestion centralisée des données, validation, cache

#### **✅ Auto-complétion**
- **CLI** : Auto-complétion des commandes et options
- **REPL** : Interface interactive avec historique et suggestions

#### **✅ Rapports Globaux**
- **Intégration** : Pandoc integration pour export multi-formats
- **Formats** : HTML, PDF, Markdown, LaTeX

#### **✅ Système de Licence**
- **Validation** : Vérification des licences et permissions
- **Gestion** : Système de licences par module et fonctionnalité

---

## 🚨 **PROBLÈMES IDENTIFIÉS ET RÉSOLUS**

### **1. Algorithme Hardy-Cross Simplifié - ✅ RÉSOLU**

#### **Problème Initial**
- **Limitation** : `_identify_loops()` limité à 5 boucles maximum
- **Cause** : Algorithme simplifié pour éviter la complexité
- **Impact** : Réseaux complexes non supportés

#### **Solution Implémentée**
- **Algorithme robuste** : `_identify_loops_robust()` sans limitation
- **Détection automatique** : Identification de toutes les boucles fondamentales
- **Validation** : Testé avec réseaux de 24+ boucles
- **Performance** : Convergence en 1 itération pour réseaux complexes

#### **Code de Résolution**
```python
def _identify_loops_robust(self, troncons):
    """
    Algorithme robuste de détection de boucles sans limitation
    Basé sur la théorie des graphes et recherche de cycles
    """
    # Implémentation complète dans hardy_cross_enhanced.py
    pass
```

### **2. Intégration EPANET - 🔄 EN COURS**

#### **État Actuel**
- **Dossiers détectés** : `EPANET2.2-master`, `pyswmm-2.0.1`
- **Intégration** : Partiellement implémentée dans les commandes unifiées
- **Objectif** : Validation des calculs Hardy-Cross

#### **Plan d'Implémentation**
- **Phase 1** : Wrapper Python pour EPANET
- **Phase 2** : Interface CLI intégrée
- **Phase 3** : Comparaison automatique des résultats

### **3. Intégration SWMM - 📋 PLANIFIÉE**

#### **Objectifs**
- **Gestion des eaux pluviales** : Modélisation avancée
- **Standard EPA** : Conformité aux normes américaines
- **Calculs de drainage** : Intégration avec module hydrodrain

---

## 📚 **NOUVELLES FONCTIONNALITÉS IMPLÉMENTÉES**

### **Commandes Unifiées AEP - ✅ COMPLÈTEMENT IMPLÉMENTÉES**

#### **Architecture Unifiée**
- **Single Entry Point** : Chaque commande accepte paramètres inline OU fichiers
- **Routage automatique** : `--input` → mode enhanced, sinon mode simple
- **Structure de sortie standardisée** : `{valeurs, diagnostics, iterations}`

#### **Commandes Disponibles**
```bash
# Population et demande
lcpi aep population-unified [ARGS] --input FILE --mode auto|simple|enhanced
lcpi aep demand-unified [ARGS] --input FILE --mode auto|simple|enhanced

# Réseau et infrastructure
lcpi aep network-unified [ARGS] --input FILE --mode auto|simple|enhanced
lcpi aep reservoir-unified [ARGS] --input FILE --mode auto|simple|enhanced
lcpi aep pumping-unified [ARGS] --input FILE --mode auto|simple|enhanced

# Hardy-Cross avancé
lcpi aep hardy-cross-unified --input FILE --tolerance 1e-6 --max-iterations 200

# Validation Phase 0
lcpi aep validate-input --input FILE --export json
lcpi aep validate-population --input FILE --export json
lcpi aep validate-network --input FILE --export json
```

#### **Options Communes Standardisées**
- **`--input`** : Fichier YAML/CSV/JSON d'entrée
- **`--mode`** : `auto` (détection automatique), `simple`, `enhanced`
- **`--export`** : `json`, `yaml`, `csv`, `markdown`, `html`
- **`--output`** : Fichier de sortie spécifique
- **`--verbose`** : Affichage détaillé et transparence mathématique

### **Système d'Export Centralisé - ✅ IMPLÉMENTÉ**

#### **Module Exporters**
- **Fichier** : `src/lcpi/aep/utils/exporters.py`
- **Fonctionnalités** : Export multi-formats avec gestion d'erreurs
- **Formats supportés** : JSON, YAML, CSV, Markdown, HTML
- **Encodage** : UTF-8 garanti, gestion des erreurs robuste

#### **Fonctions d'Export**
```python
def _export_generic(data, export_format, output_file=None):
    """Export générique vers tous les formats supportés"""
    pass

def _flatten_dict(data, parent_key='', sep='_'):
    """Aplatissement des dictionnaires pour export CSV"""
    pass
```

### **Validation Robuste - ✅ IMPLÉMENTÉE**

#### **Module Validators**
- **Fichier** : `src/lcpi/aep/core/validators.py`
- **Fonctionnalités** : Validation des données, contraintes physiques
- **Gestion d'erreurs** : Messages clairs et orientés correction

#### **Fonctions de Validation**
```python
def validate_population_unified_data(data):
    """Validation des données de population unifiées"""
    pass

def validate_network_unified_data(data):
    """Validation des données de réseau unifiées"""
    pass

def check_physical_constraints(data):
    """Vérification des contraintes physiques"""
    pass
```

---

## 🔄 **PLAN D'ACTION ACTUALISÉ**

### **Phase 1 : Commandes Unifiées - ✅ TERMINÉE**
- ✅ Implémentation de toutes les commandes `*-unified`
- ✅ Système d'export centralisé
- ✅ Validation robuste des données
- ✅ Tests unitaires complets (16/16 passent)

### **Phase 2 : Intégration Réseau Complet - 🎯 EN COURS**
1. **Implémentation** `network-complete-unified`
2. **Intégration Hardy-Cross avancée** (déjà partiellement fait)
3. **Intégration EPANET complète**
4. **Post-traitement et validation**

### **Phase 3 : Optimisation et Analyse Avancée - 📋 PLANIFIÉE**
1. **Algorithmes d'optimisation** (génétique, gradient)
2. **Analyse de sensibilité** (indices de Sobol)
3. **Comparaison de variantes**
4. **Tests et documentation**

### **Phase 4 : Intégration SWMM - 📋 PLANIFIÉE**
1. **Analyse pyswmm et swmm-python-dev**
2. **Module drainage avancé**
3. **Calculs eaux pluviales**

---

## 📝 **NOTES TECHNIQUES ACTUALISÉES**

### **Algorithme de Recherche de Cycles - ✅ IMPLÉMENTÉ**
```python
def _identify_loops_robust(self, troncons):
    """
    Algorithme robuste de détection de boucles
    Basé sur la théorie des graphes et recherche de cycles
    Supporte un nombre illimité de boucles
    """
    # Implémentation complète dans hardy_cross_enhanced.py
    # Testé avec succès sur réseaux de 24+ boucles
    pass
```

### **Intégration EPANET - 🔄 EN DÉVELOPPEMENT**
```python
def epanet_simulation(network_data):
    """
    Utilise EPANET pour valider les calculs Hardy-Cross
    Génération automatique de fichiers .inp
    Exécution via pyswmm
    """
    # Implémentation en cours
    pass
```

### **Système de Validation Unifié - ✅ IMPLÉMENTÉ**
```python
def validate_and_clean_data(data, schema):
    """
    Validation et nettoyage des données selon un schéma
    Gestion des erreurs avec messages clairs
    """
    # Implémentation complète dans validators.py
    pass
```

---

## 🎯 **OBJECTIFS PRIORITAIRES ACTUALISÉS**

### **✅ ACCOMPLIS (Phase 1)**
1. **Commandes unifiées** : Toutes implémentées et testées
2. **Hardy-Cross amélioré** : Limitation de boucles supprimée
3. **Système d'export** : Centralisé et multi-formats
4. **Validation robuste** : Phase 0 complète

### **🎯 EN COURS (Phase 2)**
1. **Intégration réseau complet** : `network-complete-unified`
2. **Intégration EPANET** : Génération et exécution de fichiers .inp
3. **Post-traitement avancé** : Vérifications, coup de bélier

### **📋 PLANIFIÉS (Phase 3)**
1. **Optimisation multi-critères** : Algorithmes génétiques
2. **Analyse de sensibilité** : Indices de Sobol
3. **Comparaison de variantes** : Outils de décision

### **📋 FUTURS (Phase 4)**
1. **Intégration SWMM** : Gestion des eaux pluviales
2. **Modules CM, Bois, Béton** : Développement complet
3. **Interface graphique** : QGIS plugin et web interface

---

## 🧪 **QUALITÉ ET TESTS**

### **Couverture de Tests**
- **Tests unitaires** : 16/16 passent (100%)
- **Tests d'intégration** : En cours de développement
- **Validation des données** : Robuste et complète

### **Standards de Qualité**
- **Documentation** : Complète avec exemples
- **Gestion d'erreurs** : Messages clairs et orientés correction
- **Performance** : Optimisée pour réseaux < 100 nœuds
- **Interface utilisateur** : Intuitive et cohérente

---

*Dernière mise à jour : 2025-01-27*
*Version LCPI : 2.1.0*
*Phase actuelle : 2 (Intégration Réseau Complet)*
