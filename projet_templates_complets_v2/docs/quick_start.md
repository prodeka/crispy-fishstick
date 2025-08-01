# Guide de Démarrage Rapide - projet_templates_complets_v2

## Premiers Pas

### 1. Vérifier l'Installation
```bash
lcpi doctor
```

### 2. Explorer les Exemples
```bash
# Voir tous les exemples
lcpi examples

# Exemples spécifiques
lcpi examples beton
```

### 3. Premier Calcul

```bash
# Calculer un poteau
lcpi beton calc-poteau data/beton/poteau_exemple.yml

# Calculer un radier
lcpi beton calc-radier data/beton/radier_exemple.yml
```

## Structure des Données

### Format YAML
Tous les fichiers de données utilisent le format YAML. Exemple:

```yaml
# Exemple de fichier de données
description: "Description de l'élément"
parametres:
  valeur1: 10.0
  valeur2: "texte"
```

### Organisation des Fichiers
- `data/` : Données d'entrée
- `output/` : Résultats de calculs
- `reports/` : Rapports générés

## Commandes Utiles

```bash
# Aide générale
lcpi --help

# Aide d'un plugin
lcpi beton --help

# Mode interactif
lcpi shell

# Générer un rapport
lcpi report .
```
