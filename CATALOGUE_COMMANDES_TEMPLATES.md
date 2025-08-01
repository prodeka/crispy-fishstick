# 📋 Catalogue Complet des Commandes LCPI-CLI

## Vue d'ensemble

Ce document recense toutes les commandes disponibles dans LCPI-CLI et identifie les commandes de calcul métier nécessitant des templates adaptés.

## 🔧 Commandes Générales (Non-métier)

### Commandes de Gestion
- `lcpi init` - Initialisation de projets
- `lcpi plugins` - Gestion des plugins
- `lcpi config` - Configuration
- `lcpi doctor` - Diagnostic système
- `lcpi report` - Génération de rapports
- `lcpi tips` - Astuces
- `lcpi guide` - Guides interactifs
- `lcpi examples` - Exemples d'utilisation
- `lcpi welcome` - Message de bienvenue
- `lcpi shell` - Mode interactif

## 🏗️ Commandes de Calcul Métier

### Module Construction Métallique (CM)

#### Commandes Identifiées
1. **check-poteau** - Vérification d'un poteau en compression/flambement
2. **check-deversement** - Vérification au déversement (flexion)
3. **check-tendu** - Vérification d'un élément tendu
4. **check-compose** - Vérification des sollicitations composées
5. **check-fleche** - Vérification de la flèche d'une poutre
6. **check-assemblage-boulon** - Vérification d'un assemblage boulonné
7. **check-assemblage-soude** - Vérification d'un assemblage soudé
8. **optimize-section** - Optimisation de section

#### Templates Nécessaires
- ✅ **poteau_exemple.yml** - Template pour poteau (existe)
- ✅ **poutre_exemple.yml** - Template pour poutre (existe)
- ✅ **assemblage_boulon_exemple.yml** - Template pour assemblage boulonné (existe)
- ❌ **assemblage_soude_exemple.yml** - Template pour assemblage soudé (à créer)
- ❌ **element_tendu_exemple.yml** - Template pour élément tendu (à créer)
- ❌ **optimization_exemple.yml** - Template pour optimisation (à créer)

### Module Construction Bois

#### Commandes Identifiées
1. **check-poteau** - Vérification d'un poteau en bois
2. **check-deversement** - Vérification au déversement
3. **check-cisaillement** - Vérification au cisaillement
4. **check-compression-perp** - Vérification en compression perpendiculaire
5. **check-compose** - Vérification des sollicitations composées
6. **check** - Traitement par lot
7. **check-fleche** - Vérification de la flèche
8. **check-assemblage-pointe** - Vérification d'un assemblage à pointes
9. **check-assemblage-embrevement** - Vérification d'un assemblage par embrevement
10. **interactive** - Mode interactif

#### Templates Nécessaires
- ✅ **poteau_exemple.yml** - Template pour poteau bois (existe)
- ✅ **poutre_exemple.yml** - Template pour poutre bois (existe)
- ✅ **assemblage_pointe_exemple.yml** - Template pour assemblage à pointes (existe)
- ❌ **assemblage_embrevement_exemple.yml** - Template pour assemblage embrevement (à créer)
- ❌ **cisaillement_exemple.yml** - Template pour cisaillement (à créer)
- ❌ **compression_perp_exemple.yml** - Template pour compression perpendiculaire (à créer)

### Module Béton Armé

#### Commandes Identifiées
1. **calc-poteau** - Calcul d'un poteau en béton
2. **calc-radier** - Calcul d'un radier
3. **interactive** - Mode interactif

#### Templates Nécessaires
- ✅ **poteau_exemple.yml** - Template pour poteau béton (existe)
- ✅ **radier_exemple.yml** - Template pour radier (existe)

### Module Hydrologie (Hydro)

#### Sous-module Pluvio
1. **analyser** - Analyse statistique de données de pluie
2. **ajuster-loi** - Ajuste les pluies maximales à la loi de Gumbel
3. **generer-idf** - Génère les courbes IDF

#### Sous-module Ouvrage
1. **canal-dimensionner** - Dimensionne un canal à ciel ouvert
2. **init-canal** - Génère un fichier YAML d'exemple pour un canal
3. **dalot-verifier** - Vérifie les performances hydrauliques d'un dalot
4. **init-dalot** - Génère un fichier YAML d'exemple pour un dalot
5. **deversoir-dimensionner** - Dimensionne la longueur d'un déversoir
6. **init-deversoir** - Génère un fichier YAML d'exemple pour un déversoir

#### Sous-module Reservoir
1. **equilibrage** - Dimensionne un réservoir d'équilibrage
2. **incendie** - Dimensionne un réservoir d'incendie
3. **complet** - Dimensionne un réservoir complet
4. **verifier-pression** - Vérifie la pression disponible

#### Sous-module Util
1. **prevoir-population** - Prévoit l'évolution de la population
2. **estimer-demande-eau** - Estime la demande en eau
3. **diagramme-ombro** - Génère un diagramme ombrothermique

#### Templates Nécessaires
- ✅ **canal_exemple.yml** - Template pour canal (existe)
- ✅ **reservoir_exemple.yml** - Template pour réservoir (existe)
- ✅ **pluviometrie_exemple.yml** - Template pour pluviométrie (existe)
- ❌ **dalot_exemple.yml** - Template pour dalot (à créer)
- ❌ **deversoir_exemple.yml** - Template pour déversoir (à créer)
- ❌ **population_exemple.yml** - Template pour prévision population (à créer)
- ❌ **demande_eau_exemple.yml** - Template pour estimation demande (à créer)
- ❌ **diagramme_ombro_exemple.yml** - Template pour diagramme ombrothermique (à créer)

## 📊 Résumé des Templates

### Templates Existants ✅
- **CM** : 3/6 templates (50%)
- **Bois** : 3/6 templates (50%)
- **Béton** : 2/2 templates (100%)
- **Hydro** : 3/8 templates (37.5%)

### Templates à Créer ❌
- **CM** : 3 templates manquants
- **Bois** : 3 templates manquants
- **Béton** : 0 template manquant
- **Hydro** : 5 templates manquants

**Total** : 11 templates à créer

## 🎯 Plan d'Action

### Phase 1 : Templates CM manquants
1. `assemblage_soude_exemple.yml`
2. `element_tendu_exemple.yml`
3. `optimization_exemple.yml`

### Phase 2 : Templates Bois manquants
1. `assemblage_embrevement_exemple.yml`
2. `cisaillement_exemple.yml`
3. `compression_perp_exemple.yml`

### Phase 3 : Templates Hydro manquants
1. `dalot_exemple.yml`
2. `deversoir_exemple.yml`
3. `population_exemple.yml`
4. `demande_eau_exemple.yml`
5. `diagramme_ombro_exemple.yml`

## 📝 Format des Templates

Tous les templates suivent le format YAML standardisé :

```yaml
# Template pour [nom_commande]
element_id: [ID_UNIQUE]
description: "Description de l'élément"

# Paramètres spécifiques à la commande
parametres:
  # Paramètres selon la commande

# Paramètres de calcul
parametres_calcul:
  # Options de calcul
```

## 🔗 Intégration avec lcpi init

Les templates seront intégrés dans la commande `lcpi init` selon les plugins sélectionnés :

```bash
# Initialisation avec tous les templates
lcpi init projet_complet --template complet

# Initialisation avec templates spécifiques
lcpi init projet_cm --template cm
lcpi init projet_bois --template bois
lcpi init projet_beton --template beton
lcpi init projet_hydro --template hydro
```

---

**Version** : 2.0.0  
**Date** : 2025-08-01  
**Statut** : Analyse complète réalisée 