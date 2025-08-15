# 📚 Guide Utilisateur - Nouvelles Fonctionnalités AEP

## 🎯 Vue d'ensemble

Ce guide présente les nouvelles fonctionnalités implémentées pour améliorer l'expérience utilisateur et la gestion des projets AEP (Alimentation en Eau Potable).

## 📋 Fonctionnalités Disponibles

### 1. 🗄️ Base de Données Centralisée (Suggestion 1)

**Objectif :** Stockage centralisé et organisé de tous les projets AEP avec historique et traçabilité.

#### Commandes disponibles :

```bash
# Initialiser la base de données
lcpi aep database init

# Ajouter un nouveau projet
lcpi aep database add-project --name "Mon Projet" --desc "Description du projet"

# Lister tous les projets
lcpi aep database list

# Obtenir des informations sur la base
lcpi aep database info --verbose

# Rechercher dans un projet
lcpi aep database search --id 1 --search "forage"

# Exporter un projet
lcpi aep database export --id 1 --format json --output projet_export.json

# Nettoyer un projet
lcpi aep database clean --id 1
```

#### Exemples d'utilisation :

```bash
# Créer un nouveau projet AEP
lcpi aep database add-project \
  --name "Projet Village Mboula" \
  --desc "Alimentation en eau potable du village Mboula" \
  --metadata '{"client": "Commune de Mboula", "region": "Centre"}'

# Lister les projets avec détails
lcpi aep database list --verbose

# Exporter un projet complet
lcpi aep database export --id 1 --format yaml --output mboula_projet.yaml
```

### 2. 📥 Import Automatique Excel/CSV (Suggestion 2)

**Objectif :** Import facile de données depuis Excel ou CSV avec validation automatique.

#### Commandes disponibles :

```bash
# Générer un template Excel
lcpi aep import-data --template --project 1 forages template_forages.xlsx

# Valider un fichier sans importer
lcpi aep import-data --validate --project 1 forages data_forages.csv

# Importer des données
lcpi aep import-data --project 1 forages data_forages.csv

# Import avec rapport détaillé
lcpi aep import-data --project 1 --verbose --output rapport_import.md forages data_forages.csv
```

#### Types d'import supportés :

- **forages** : Données de forages (profondeur, débit, diamètre, etc.)
- **pompes** : Équipements de pompage (type, puissance, rendement, etc.)
- **reservoirs** : Réservoirs de stockage (volume, hauteur, diamètre, etc.)
- **constantes** : Constantes locales (dotations, coefficients, etc.)
- **enquetes** : Enquêtes de consommation (population, dotation, etc.)

#### Exemples d'utilisation :

```bash
# Générer un template pour les forages
lcpi aep import-data --template --project 1 forages template_forages.xlsx

# Importer des données de forages avec validation
lcpi aep import-data --validate --project 1 forages forages_mboula.csv
lcpi aep import-data --project 1 forages forages_mboula.csv --verbose

# Importer des pompes
lcpi aep import-data --project 1 pompes pompes_mboula.csv --output rapport_pompes.md
```

### 3. ✅ Validation des Données (Suggestion 3)

**Objectif :** Validation automatique de la cohérence et de la qualité des données.

#### Commandes disponibles :

```bash
# Valider un projet complet
lcpi aep validate-project 1

# Validation avec rapport détaillé
lcpi aep validate-project 1 --verbose --output rapport_validation.md
```

#### Fonctionnalités de validation :

- **Validation GPS** : Vérification des coordonnées géographiques
- **Validation des valeurs** : Contrôle des plages de valeurs acceptables
- **Cohérence globale** : Vérification de la cohérence entre les données
- **Recommandations** : Suggestions d'amélioration automatiques

#### Exemples d'utilisation :

```bash
# Validation complète d'un projet
lcpi aep validate-project 1 --verbose

# Validation avec rapport
lcpi aep validate-project 1 --output validation_mboula.md
```

### 4. 🔄 Moteur de Recalcul Automatique (Suggestion 6)

**Objectif :** Recalcul automatique des résultats lorsque les données d'entrée changent.

#### Commandes disponibles :

```bash
# Ajouter une tâche de recalcul
lcpi aep recalcul add --type population --project 1 --params '{"population_base": 1000, "taux_croissance": 0.025, "annees": 10}'

# Recalcul en cascade (avec dépendances)
lcpi aep recalcul add --type network --project 1 --cascade --params '{"parametres": "test"}'

# Exécuter les tâches en attente
lcpi aep recalcul execute

# Voir le statut des tâches
lcpi aep recalcul status --verbose

# Nettoyer les tâches terminées
lcpi aep recalcul clean
```

#### Types de recalcul supportés :

- **population** : Projections démographiques
- **hardy_cross** : Calculs de distribution
- **reservoir** : Dimensionnement de réservoirs
- **pumping** : Dimensionnement de pompage
- **demand** : Calculs de demande
- **network** : Calculs de réseau

#### Exemples d'utilisation :

```bash
# Ajouter un recalcul de population
lcpi aep recalcul add \
  --type population \
  --project 1 \
  --params '{"population_base": 1500, "taux_croissance": 0.03, "annees": 15}'

# Recalcul en cascade pour un réseau complet
lcpi aep recalcul add \
  --type network \
  --project 1 \
  --cascade \
  --params '{"longueur_totale": 2500, "diametre_moyen": 150}'

# Exécuter et voir les résultats
lcpi aep recalcul execute --verbose
lcpi aep recalcul status
```

## 🔧 Workflow Typique

### 1. Création et Configuration d'un Projet

```bash
# 1. Initialiser la base de données
lcpi aep database init

# 2. Créer un nouveau projet
lcpi aep database add-project \
  --name "Projet Village Mboula" \
  --desc "AEP Village Mboula - Phase 1" \
  --metadata '{"client": "Commune", "region": "Centre", "phase": "1"}'

# 3. Générer des templates pour l'import
lcpi aep import-data --template --project 1 forages template_forages.xlsx
lcpi aep import-data --template --project 1 pompes template_pompes.xlsx
```

### 2. Import et Validation des Données

```bash
# 1. Remplir les templates Excel avec les données terrain
# (Utiliser Excel ou LibreOffice Calc)

# 2. Valider les fichiers avant import
lcpi aep import-data --validate --project 1 forages forages_mboula.csv
lcpi aep import-data --validate --project 1 pompes pompes_mboula.csv

# 3. Importer les données validées
lcpi aep import-data --project 1 forages forages_mboula.csv --verbose
lcpi aep import-data --project 1 pompes pompes_mboula.csv --verbose

# 4. Valider la cohérence globale du projet
lcpi aep validate-project 1 --verbose --output validation_mboula.md
```

### 3. Calculs et Recalculs Automatiques

```bash
# 1. Ajouter des tâches de recalcul
lcpi aep recalcul add \
  --type population \
  --project 1 \
  --params '{"population_base": 1200, "taux_croissance": 0.025, "annees": 20}'

lcpi aep recalcul add \
  --type network \
  --project 1 \
  --cascade \
  --params '{"longueur_reseau": 3000, "diametre_principal": 200}'

# 2. Exécuter les calculs
lcpi aep recalcul execute --verbose

# 3. Vérifier les résultats
lcpi aep database info --verbose
```

### 4. Export et Rapports

```bash
# 1. Exporter le projet complet
lcpi aep database export --id 1 --format json --output mboula_projet_complet.json

# 2. Générer des rapports de validation
lcpi aep validate-project 1 --output rapport_final.md

# 3. Lister les projets
lcpi aep database list --verbose
```

## 📊 Formats de Données

### Template Forages (CSV/Excel)

```csv
nom_forage,profondeur,debit_test,diametre,niveau_statique,niveau_dynamique,coordonnees_gps
F1,50,10.5,200,15,25,"12.345,67.890"
F2,60,12.0,250,20,30,"12.350,67.895"
```

### Template Pompes (CSV/Excel)

```csv
nom_pompe,type_pompe,debit_nominal,puissance,hauteur_manometrique,rendement
P1,centrifuge,50,10.5,30,0.75
P2,submersible,30,8.0,25,0.80
```

### Template Réservoirs (CSV/Excel)

```csv
nom_reservoir,volume,hauteur,diametre,type_reservoir,coordonnees_gps
R1,1000,8,12,cylindrique,"12.360,67.900"
R2,500,6,10,spherique,"12.365,67.905"
```

## ⚠️ Bonnes Pratiques

### 1. Organisation des Données

- **Nommage cohérent** : Utilisez des noms descriptifs pour les projets et les éléments
- **Métadonnées** : Ajoutez des informations contextuelles (client, région, phase, etc.)
- **Versioning** : Exportez régulièrement les projets pour conserver l'historique

### 2. Validation

- **Validation pré-import** : Validez toujours les fichiers avant import
- **Validation post-import** : Vérifiez la cohérence globale après chaque import
- **Recommandations** : Suivez les recommandations automatiques pour améliorer la qualité

### 3. Recalculs

- **Cascade** : Utilisez le mode cascade pour les calculs interdépendants
- **Priorités** : Organisez les tâches par priorité
- **Monitoring** : Surveillez régulièrement le statut des tâches

### 4. Sauvegarde

- **Exports réguliers** : Exportez les projets à chaque étape importante
- **Formats multiples** : Utilisez JSON et YAML pour la compatibilité
- **Documentation** : Conservez les rapports de validation et d'import

## 🆘 Dépannage

### Problèmes Courants

1. **Erreur "no such table"**
   - Solution : Exécuter `lcpi aep database init`

2. **Fichier CSV invalide**
   - Solution : Utiliser `--validate` avant l'import
   - Vérifier le format avec les templates

3. **Erreur de coordonnées GPS**
   - Format attendu : "latitude,longitude" (ex: "12.345,67.890")
   - Plages : Latitude [-90, 90], Longitude [-180, 180]

4. **Tâches de recalcul bloquées**
   - Vérifier le statut : `lcpi aep recalcul status`
   - Nettoyer : `lcpi aep recalcul clean`

### Commandes de Diagnostic

```bash
# Vérifier l'état de la base de données
lcpi aep database info --verbose

# Lister tous les projets
lcpi aep database list --verbose

# Vérifier le statut des tâches
lcpi aep recalcul status --verbose

# Valider un projet complet
lcpi aep validate-project 1 --verbose
```

## 📞 Support

Pour toute question ou problème :

1. **Documentation** : Consultez ce guide et les autres documents du projet
2. **Tests** : Utilisez les commandes de validation et de diagnostic
3. **Logs** : Activez le mode `--verbose` pour plus de détails
4. **Export** : Exportez les données et rapports pour l'analyse

---

**Version :** 1.0  
**Date :** 2025-08-15  
**Auteur :** Équipe LCPI
