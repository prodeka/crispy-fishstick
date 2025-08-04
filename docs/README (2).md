# LCPI - Logiciel de Calcul des Projets d'Ingénierie

## Vue d'ensemble

LCPI est un logiciel de calcul structural pour les constructions métalliques et en bois, basé sur les normes Eurocode et le document FORMATEC. Le logiciel fournit des outils CLI pour la vérification et l'optimisation des éléments structuraux.

## Installation

```bash
# Cloner le repository
git clone <repository-url>
cd PROJET_DIMENTIONEMENT_2

# Installer les dépendances
pip install -r requirements.txt
```

## Structure du projet

```
src/lcpi/
├── cm/                 # Module Construction Métallique
│   ├── main.py        # Commandes CLI pour l'acier
│   ├── test/          # Tests unitaires
│   └── elements/      # Fichiers YAML d'exemples
├── bois/              # Module Structures Bois
│   ├── main.py        # Commandes CLI pour le bois
│   ├── test/          # Tests unitaires
│   └── elements/      # Fichiers YAML d'exemples
└── db/
    └── cm_bois.json   # Base de données des propriétés matériaux
```

## Fonctionnalités implémentées

### Module `cm` (Construction Métallique)

#### 1. Vérification Poteau - `check-poteau`
Vérification au flambement selon FORMATEC.

```bash
lcpi cm check-poteau --filepath elements/poteau.yml
```

**Fichier YAML d'entrée :**
```yaml
description: "Vérification d'un poteau IPE 240"
profil:
  nom: "IPE 240"
materiau:
  nuance: "S235"
longueurs_flambement:
  Lf_y_m: 4.0
  Lf_z_m: 4.0
efforts:
  N_ed_kN: 150.0
```

#### 2. Vérification Déversement - `check-deversement`
Vérification au déversement des poutres selon FORMATEC.

```bash
lcpi cm check-deversement --filepath elements/poutre.yml
```

#### 3. Vérification Tension - `check-tendu`
Vérification des éléments tendus.

```bash
lcpi cm check-tendu --filepath elements/tendu.yml
```

#### 4. Vérification Flexion Composée - `check-compose`
Vérification des éléments en flexion composée.

```bash
lcpi cm check-compose --filepath elements/compose.yml
```

#### 5. Vérification Flèche (ELS) - `check-fleche`
Vérification de la déformation selon page 95 du document FORMATEC.

```bash
lcpi cm check-fleche --filepath elements/fleche.yml
```

**Fichier YAML d'entrée :**
```yaml
description: "Vérification de la flèche d'une poutre IPE 240"
profil:
  nom: "IPE 240"
materiau:
  nuance: "S235"
portee_m: 6.0
charges_service:
  permanente_G:
    type: "uniformement repartie"
    valeur_kN_m: 5.0
  exploitation_Q:
    type: "ponctuelle"
    valeur_kN: 10.0
    position_m: 3.0
```

#### 6. Vérification Assemblages Boulonnés - `check-assemblage-boulon`
Vérification selon les principes de l'Eurocode 3.

```bash
lcpi cm check-assemblage-boulon --filepath elements/assemblage_boulon.yml
```

#### 7. Vérification Assemblages Soudés - `check-assemblage-soude`
Vérification selon les principes de l'Eurocode 3.

```bash
lcpi cm check-assemblage-soude --filepath elements/assemblage_soude.yml
```

#### 8. Optimisation de Section - `optimize-section`
Trouve le profilé le plus léger satisfaisant aux critères.

```bash
lcpi cm optimize-section --check poteau --filepath elements/optimisation.yml
lcpi cm optimize-section --check fleche --filepath elements/optimisation.yml
```

### Module `bois` (Structures Bois)

#### 1. Vérification Poteau Bois - `check-poteau`
Vérification au flambement selon EC5.

```bash
lcpi bois check-poteau --filepath elements/poteau_bois.yml
```

**Fichier YAML d'entrée :**
```yaml
description: "Vérification au flambement d'un poteau en bois C24"
profil:
  type: "rectangulaire"
  dimensions_mm:
    b: 150
    h: 150
materiau:
  classe_resistance: "C24"
  classe_service: 2
  duree_charge: "Moyen terme"
longueur_flambement_m: 4.5
efforts_elu:
  N_c_ed_kN: 80
```

#### 2. Vérification Déversement Bois - `check-deversement`
Vérification au déversement selon EC5.

```bash
lcpi bois check-deversement --filepath elements/poutre_deversement.yml
```

#### 3. Vérification Cisaillement - `check-cisaillement`
Vérification au cisaillement selon EC5.

```bash
lcpi bois check-cisaillement --filepath elements/cisaillement.yml
```

#### 4. Vérification Compression Perpendiculaire - `check-compression-perp`
Vérification en compression perpendiculaire selon EC5.

```bash
lcpi bois check-compression-perp --filepath elements/compression_perp.yml
```

#### 5. Vérification Flexion Composée Bois - `check-compose`
Vérification des éléments en flexion composée selon EC5.

```bash
lcpi bois check-compose --filepath elements/compose_bois.yml
```

#### 6. Vérification Flèche Bois (ELS) - `check-fleche`
Vérification de la déformation selon EC5.

```bash
lcpi bois check-fleche --filepath elements/fleche_bois.yml
```

#### 7. Vérification Assemblages Pointes - `check-assemblage-pointe`
Vérification d'assemblages par pointes selon EC5.

```bash
lcpi bois check-assemblage-pointe --filepath elements/assemblage_pointe.yml
```

#### 8. Vérification Assemblages Embrèvement - `check-assemblage-embrevement`
Vérification d'assemblages traditionnels selon EC5.

```bash
lcpi bois check-assemblage-embrevement --filepath elements/assemblage_embrevement.yml
```

## Base de données

Le logiciel utilise le fichier `src/lcpi/db/cm_bois.json` qui contient :

- **Propriétés des aciers** : Résistances élastiques, caractéristiques mécaniques
- **Propriétés des bois** : Classes de résistance, modules d'élasticité, résistances
- **Profils métalliques** : IPE, HEA, HEB avec caractéristiques géométriques
- **Limites de flèche** : Valeurs réglementaires pour les vérifications ELS
- **Facteurs de modification** : Coefficients pour les bois selon classe de service

## Format de sortie

Toutes les commandes produisent un **JSON structuré** pour faciliter l'automatisation :

```json
{
  "contrainte_appliquee_MPa": 120.5,
  "verification_flambement": {
    "elancement_lambda_z": 85.2,
    "coefficient_k_z": 0.78,
    "contrainte_admissible_MPa": 156.0,
    "ratio": 0.77,
    "statut": "OK"
  }
}
```

## Tests

Exécuter les tests unitaires :

```bash
# Tests module cm
pytest src/lcpi/cm/test/test_cm_commands.py -v

# Tests module bois  
pytest src/lcpi/bois/test/test_bois_commands.py -v

# Tous les tests
pytest src/lcpi/ -v
```

## Exemples d'utilisation

### Vérification d'un poteau métallique
```bash
lcpi cm check-poteau --filepath src/lcpi/cm/elements/poteau_P1.yml
```

### Vérification d'une poutre en bois
```bash
lcpi bois check-poteau --filepath src/lcpi/bois/elements/poteau_bois_test.yml
```

### Optimisation d'une section
```bash
lcpi cm optimize-section --check poteau --filepath src/lcpi/cm/elements/poteau_P1.yml
```

## Normes et références

- **Construction métallique** : Eurocode 3 (EC3) + Document FORMATEC
- **Structures bois** : Eurocode 5 (EC5) + Document FORMATEC
- **États limites** : ELU (Ultime) et ELS (Service)

## Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## Licence

[À définir selon les besoins du projet] 