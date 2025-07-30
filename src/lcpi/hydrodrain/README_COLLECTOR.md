# Module Collecteur d'Assainissement - Plugin Hydro

Ce module implémente un moteur de calcul complet pour le dimensionnement des réseaux d'assainissement gravitaire, couvrant à la fois les **eaux usées** (calcul déterministe) et les **eaux pluviales** (calcul hydrologique itératif).

## Architecture

### Objets Principaux

1. **`Troncon`** : Représente un segment de canalisation
   - Attributs d'entrée : géométrie, pente, rugosité, données hydrologiques
   - Attributs calculés : débit, dimensions, statut

2. **`Reseau`** : Représente l'ensemble du réseau
   - Gestion de la topologie
   - Tri topologique pour l'ordre de calcul

## Algorithmes Implémentés

### 1. Réseau d'Eaux Usées (Mode Déterministe)

**Principe** : Calcul direct basé sur la population et les ratios de production.

**Formules** :
- Débit de pointe : `Q = (Dotation × Coeff_Pointe × Population) / (1000 × 86400)`
- Dimensionnement : Formule de Manning-Strickler

**Utilisation** :
```bash
lcpi hydro collector eaux-usees reseau_eaux_usees.json
```

### 2. Réseau d'Eaux Pluviales (Mode Hydrologique Itératif)

**Principe** : Calcul itératif basé sur la méthode rationnelle avec convergence du temps de concentration.

**Formules** :
- Temps de concentration (Kirpich) : `tc = 0.01947 × L^0.77 × P^(-0.385)`
- Intensité de pluie (Talbot) : `i = a / (b + tc)`
- Débit de projet : `Q = (C × i × A) / 360`

**Utilisation** :
```bash
lcpi hydro collector eaux-pluviales reseau_eaux_pluviales.json --type-idf talbot --coeff-a 120 --coeff-b 20
```

## Types de Sections Supportés

### 1. Section Circulaire
- Diamètres commerciaux : 100mm à 2000mm
- Calcul automatique du taux de remplissage
- Vérification des vitesses (0.6 à 4.0 m/s)

### 2. Section Rectangulaire
- Largeur fixe, hauteur calculée
- Optimisation pour le débit de projet

### 3. Section Trapézoïdale
- Largeur de base et fruit des talus
- Calcul itératif de la hauteur

## Format des Fichiers JSON

### Réseau d'Eaux Usées
```json
{
  "troncons": [
    {
      "id": "T1",
      "type_section": "circulaire",
      "longueur_troncon_m": 100.0,
      "pente_troncon": 0.005,
      "ks_manning_strickler": 70.0,
      "amont_ids": [],
      "population": 50,
      "dotation_l_jour_hab": 150.0,
      "coefficient_pointe": 2.5
    }
  ]
}
```

### Réseau d'Eaux Pluviales
```json
{
  "troncons": [
    {
      "id": "T1",
      "type_section": "circulaire",
      "longueur_troncon_m": 100.0,
      "pente_troncon": 0.005,
      "ks_manning_strickler": 70.0,
      "amont_ids": [],
      "surface_propre_ha": 2.5,
      "coefficient_ruissellement": 0.8,
      "longueur_parcours_m": 80.0,
      "pente_parcours_m_m": 0.02
    }
  ]
}
```

## Commandes Disponibles

### Génération d'Exemples
```bash
# Créer un exemple de réseau d'eaux usées
lcpi hydro collector init-exemple eaux-usees reseau_eaux_usees.json

# Créer un exemple de réseau d'eaux pluviales
lcpi hydro collector init-exemple eaux-pluviales reseau_eaux_pluviales.json
```

### Dimensionnement
```bash
# Dimensionner un réseau d'eaux usées
lcpi hydro collector eaux-usees reseau_eaux_usees.json

# Dimensionner un réseau d'eaux pluviales
lcpi hydro collector eaux-pluviales reseau_eaux_pluviales.json --type-idf talbot
```

## Résultats de Sortie

### Structure des Résultats
```json
{
  "statut": "OK",
  "troncons": [
    {
      "id": "T1",
      "q_max_m3s": 0.0023,
      "resultat_dimensionnement": {
        "statut": "OK",
        "type_section": "circulaire",
        "diametre_mm": 200,
        "vitesse_ms": 1.2,
        "remplissage_pourcent": 65.4
      },
      "statut": "OK"
    }
  ]
}
```

### Export Automatique
Les résultats sont automatiquement exportés vers :
- `reseau_eaux_usees_resultats_eaux_usees.json`
- `reseau_eaux_pluviales_resultats_eaux_pluviales.json`

## Algorithmes Techniques

### Tri Topologique
- Détection automatique de l'ordre de calcul
- Gestion des dépendances entre tronçons
- Prévention des cycles dans le réseau

### Convergence Itérative (Eaux Pluviales)
- Critère de convergence : `|tc_nouveau - tc_ancien| < 0.1 min`
- Maximum 20 itérations
- Temps de concentration minimum : 5 minutes

### Dimensionnement Hydraulique
- Formule de Manning-Strickler : `Q = Ks × S × Rh^(2/3) × I^0.5`
- Vérification des contraintes de vitesse
- Choix automatique des diamètres commerciaux

## Exemples d'Utilisation

### Exemple 1 : Réseau Simple d'Eaux Usées
```bash
# Créer l'exemple
lcpi hydro collector init-exemple eaux-usees exemple.json

# Dimensionner
lcpi hydro collector eaux-usees exemple.json
```

### Exemple 2 : Réseau d'Eaux Pluviales avec Talbot
```bash
# Créer l'exemple
lcpi hydro collector init-exemple eaux-pluviales exemple_pluviales.json

# Dimensionner avec formule Talbot
lcpi hydro collector eaux-pluviales exemple_pluviales.json --type-idf talbot --coeff-a 120 --coeff-b 20
```

## Validation et Contrôles

### Contrôles Automatiques
- Vérification de la cohérence des données d'entrée
- Détection des cycles dans le réseau
- Validation des contraintes hydrauliques
- Contrôle de la convergence des calculs

### Messages d'Erreur
- Données manquantes ou incohérentes
- Débits trop élevés pour les diamètres disponibles
- Non-convergence des calculs itératifs
- Cycles détectés dans la topologie

## Extensions Futures

### Fonctionnalités Prévues
- Support des sections ovoïdes
- Calcul des courbes de remous
- Intégration des pompes de relevage
- Modélisation des déversoirs d'orage
- Export vers formats CAD

### Améliorations Techniques
- Optimisation des performances
- Support des réseaux complexes
- Interface graphique
- Intégration avec SIG 