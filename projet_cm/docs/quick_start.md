# Guide de Démarrage Rapide - projet_cm

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
lcpi examples cm
```

### 3. Premier Calcul

```bash
# Vérifier un poteau
lcpi cm check-poteau data/cm/poteau_exemple.yml

# Vérifier une poutre
lcpi cm check-deversement data/cm/poutre_exemple.yml
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
lcpi cm --help

# Mode interactif
lcpi shell

# Générer un rapport
lcpi report .
```
