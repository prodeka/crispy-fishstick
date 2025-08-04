# 🗄️ Fonctionnalités de Base de Données Métier

## 📋 Vue d'ensemble

Ce système offre des fonctionnalités complètes pour interroger et analyser les bases de données métier comme `cm_bois.json` et d'autres bases de données à venir. Il permet une recherche flexible avec des mots-clés illimités dans toutes les bases de données disponibles.

## 🚀 Fonctionnalités Principales

### 1. **Recherche Globale Intelligente**
- **Parcours automatique** de toutes les bases de données
- **Mots-clés illimités** : recherche avec autant de termes que souhaité
- **Recherche AND/OR** : 
  - `valeur A AND valeur B` : trouve les résultats contenant TOUS les mots
  - `valeur A OR valeur B` : trouve les résultats contenant AU MOINS UN mot
- **Support multi-format** : JSON et SQLite
- **Recherche insensible à la casse**

### 2. **Gestionnaire de Bases de Données**
- **Recherche par classe** : `C24`, `GL24h`, etc.
- **Recherche par propriété** : `fm_k_MPa`, `E0_mean_KN_mm2`, etc.
- **Comparaison de matériaux** : tableau comparatif automatique
- **Informations détaillées** : propriétés complètes d'un matériau
- **Export CSV** : export des données pour analyse externe

### 3. **Conversion et Requêtes SQL**
- **Conversion automatique** JSON → SQLite
- **Requêtes SQL complètes** : SELECT, WHERE, ORDER BY, etc.
- **Gestion des caractères spéciaux** : échappement automatique

### 4. **Interfaces Multiples**
- **Mode REPL interactif** : `python -i repl_db_test.py`
- **Commandes CLI** : `lcpi db search --classe C24`
- **Recherche globale CLI** : `lcpi search global "C24 fm_k"`
- **Mode interactif** : `lcpi search interactive`

## 📁 Structure des Fichiers

```
src/lcpi/
├── db/
│   ├── cm_bois.json              # Base de données bois principale
│   ├── bois_test.json            # Base de test pour démonstration
│   ├── cm_bois_sqlite.db         # Version SQLite (auto-générée)
│   └── bois_test_sqlite.db       # Version SQLite de test
├── db_manager.py                 # Gestionnaire de bases de données
├── db_global_search.py           # Système de recherche globale
├── cli_db.py                     # Commandes CLI pour DB
└── cli_global_search.py          # Commandes CLI pour recherche globale
```

## 🔍 Exemples d'Utilisation

### Recherche Simple
```bash
# Recherche par classe
lcpi db search --classe C24

# Recherche par propriété
lcpi db search --propriete fm_k_MPa --min 20

# Recherche globale
lcpi search global "C24"
```

### Recherche Multiple
```bash
# Recherche AND (tous les mots)
lcpi search global "C24 fm_k" --type AND
lcpi search global "valeur A valeur B"

# Recherche OR (au moins un mot)
lcpi search global "C24 GL24h" --type OR
lcpi search global "bois massif OR lamellé"
```

### Mode Interactif
```bash
# Lancer le mode interactif
lcpi search interactive

# Dans le mode interactif :
# C24 fm_k (recherche AND par défaut)
# C24 OR fm_k (recherche OR)
# valeur A AND valeur B (recherche AND explicite)
# quit (pour quitter)
```

### REPL Python
```python
# Lancer le REPL
python -i repl_db_test.py

# Recherche simple
results = global_search.global_search('C24')
global_search.display_results(results)

# Recherche multiple AND
results = global_search.global_search(['C24', 'fm_k'], 'AND')

# Recherche multiple OR
results = global_search.global_search(['C24', 'GL24h'], 'OR')

# Recherche et affichage en une fois
global_search.search_and_display('C24')
global_search.search_and_display(['valeur A', 'valeur B'], 'AND')
```

## 🛠️ Fonctionnalités Avancées

### 1. **Recherche Contextuelle**
- **Contexte automatique** : affichage du chemin dans la structure
- **Groupement par base** : résultats organisés par source
- **Limitation des résultats** : contrôle du nombre d'affichage

### 2. **Gestion des Erreurs**
- **Parsing JSON robuste** : support des fichiers multi-JSON
- **Gestion des caractères spéciaux** : échappement SQL automatique
- **Messages d'erreur informatifs** : diagnostic des problèmes

### 3. **Performance**
- **Cache intelligent** : évite les rechargements inutiles
- **Recherche optimisée** : parcours efficace des structures
- **Limitation des résultats** : évite l'overload d'affichage

## 📊 Formats de Base de Données Supportés

### JSON
- **Structure simple** : objet JSON standard
- **Structure complexe** : fichiers multi-JSON (fusion automatique)
- **Encodage UTF-8** : support des caractères spéciaux

### SQLite
- **Conversion automatique** : JSON → SQLite
- **Requêtes SQL complètes** : toutes les opérations SQL
- **Gestion des types** : conversion automatique des types

## 🔧 Commandes CLI Disponibles

### Gestionnaire de Bases (`lcpi db`)
```bash
lcpi db search --classe C24                    # Recherche par classe
lcpi db search --propriete fm_k_MPa --min 20   # Recherche par propriété
lcpi db compare C24 C30 GL24h                  # Comparaison de matériaux
lcpi db info C24                               # Informations détaillées
lcpi db export bois_classes --output data.csv # Export CSV
lcpi db convert cm_bois                        # Conversion SQLite
lcpi db sql --db cm_bois_sqlite --query "SELECT * FROM table"
lcpi db list                                   # Liste des bases
lcpi db examples                               # Exemples d'utilisation
```

### Recherche Globale (`lcpi search`)
```bash
lcpi search global "C24"                       # Recherche simple
lcpi search global "C24 fm_k" --type AND       # Recherche AND
lcpi search global "C24 GL24h" --type OR       # Recherche OR
lcpi search quick "C24"                        # Recherche rapide
lcpi search interactive                        # Mode interactif
lcpi search databases                          # Liste des bases
lcpi search examples                           # Exemples d'utilisation
```

## 🎯 Cas d'Usage Typiques

### 1. **Recherche de Matériaux**
```bash
# Trouver tous les bois avec fm_k > 20 MPa
lcpi search global "fm_k 20" --type AND

# Comparer C24 et GL24h
lcpi db compare C24 GL24h
```

### 2. **Analyse Comparative**
```bash
# Trouver tous les matériaux avec E0_mean > 10
lcpi search global "E0_mean 10" --type AND

# Exporter les données pour analyse externe
lcpi db export bois_classes --output analyse.csv
```

### 3. **Recherche Complexe**
```bash
# Bois massif avec résistance élevée
lcpi search global "massif fm_k 24" --type AND

# Bois lamellé ou massif avec module d'Young élevé
lcpi search global "lamellé OR massif E0_mean 11" --type AND
```

## 🔮 Extensibilité

### Ajout de Nouvelles Bases
1. **Placer le fichier** dans `src/lcpi/db/`
2. **Format JSON** : structure standard ou multi-JSON
3. **Format SQLite** : tables avec colonnes appropriées
4. **Détection automatique** : le système trouve les nouvelles bases

### Personnalisation
- **Mots-clés personnalisés** : ajout de synonymes
- **Filtres métier** : règles de recherche spécifiques
- **Formats d'export** : CSV, JSON, Excel, etc.

## 📈 Avantages

### Pour l'Utilisateur
- **Simplicité** : une seule commande pour tout rechercher
- **Flexibilité** : mots-clés illimités et recherche AND/OR
- **Efficacité** : résultats instantanés dans toutes les bases
- **Intuitivité** : interface CLI et REPL familière

### Pour le Développeur
- **Extensibilité** : ajout facile de nouvelles bases
- **Maintenabilité** : code modulaire et bien structuré
- **Robustesse** : gestion d'erreurs complète
- **Performance** : recherche optimisée et cache intelligent

## 🎉 Conclusion

Ce système de gestion de bases de données métier offre une solution complète et flexible pour interroger toutes les bases de données du projet. Avec sa recherche globale intelligente, ses interfaces multiples et son extensibilité, il répond parfaitement aux besoins d'analyse et de consultation des données métier.

**Prêt à l'emploi** : toutes les fonctionnalités sont opérationnelles et testées ! 