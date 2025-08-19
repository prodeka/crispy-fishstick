# Plan d'Action : AMÉLIORATION V13

Ce document définit le plan de développement pour la V13, qui vise à finaliser les fonctionnalités des plans V10/V11/V12 et à mettre en production une solution d'optimisation robuste, complète et auditable.

---

## Sprint 1 : Fondations Robustes & Économie

**Objectif :** Solidifier les briques de base du système. Rendre le solveur et l'accès aux données robustes, et implémenter les calculs financiers essentiels.

| Tâche | Origine | Statut (début S1) | Description |
|---|---|---|---|
| **1. Solveur EPANET Robuste** | V12-A / Audit V11 | Partiellement implémenté | Finaliser le wrapper `EPANETOptimizer` en utilisant `wntr`. Ajouter la gestion des **retries** en cas d'échec et un **archivage pérenne** des fichiers `.inp` et `.rpt` pour chaque simulation. |
| **2. Modèles de Données Stricts** | Audit V11 | Non implémenté | Créer `optimizer/models.py` et y définir des modèles **Pydantic** pour toutes les structures de configuration (`OptimizationConfig`, etc.). Refactoriser le code pour utiliser ces modèles typés. |
| **3. Couche d'Accès aux Données (DAO)** | Audit V11 | Non implémenté | Créer `optimizer/db.py` et y implémenter une fonction `get_candidate_diameters` qui abstrait l'accès aux données des diamètres (que ce soit un YAML ou une future base de données SQLite). |
| **4. Calcul OPEX Complet** | V12-C / Audit V11 | Partiellement implémenté | Implémenter la logique complète de `compute_opex` dans `scoring.py` pour calculer l'énergie de pompage. Ajouter le calcul de la **Valeur Actuelle Nette (NPV)** et la fonction de **score pondéré** `J = CAPEX + λ·OPEX_NPV`. |
| **5. Cache Multi-Réservoirs** | Audit V11 | Partiellement implémenté | Mettre à jour la clé de hachage du module `cache.py` pour qu'elle supporte un **vecteur (ou dictionnaire) de hauteurs**, la rendant compatible avec les optimisations multi-réservoirs. |

---

## Sprint 2 : Algorithmes d'Optimisation Avancés

**Objectif :** Mettre en production les algorithmes d'optimisation en implémentant les fonctionnalités de performance et de robustesse manquantes.

| Tâche | Origine | Statut (début S2) | Description |
|---|---|---|---|
| **1. `GlobalOptimizer` (NSGA-II)** | V12-B / Audit V11 | Partiellement implémenté | Remplacer le wrapper actuel par un véritable algorithme **NSGA-II** (en utilisant `pymoo`). Implémenter la **parallélisation** avec `ProcessPoolExecutor` et un système de **checkpoints** pour sauvegarder et reprendre les longues optimisations. |
| **2. `MultiTankOptimizer` (Production)** | Audit V11 | Partiellement implémenté | Remplacer l'implémentation simpliste par un véritable algorithme de **descente de coordonnées** (`coordinate descent`) capable de converger vers un optimum fiable pour le cas multi-réservoirs. |
| **3. `SurrogateOptimizer` (Production)** | Audit V11 | Partiellement implémenté | Ajouter la **persistance des modèles** entraînés. Le `SurrogateOptimizer` doit pouvoir sauvegarder ses modèles `RandomForestRegressor` sur disque (`data/model_store/`) et les recharger. |
| **4. `NestedGreedyOptimizer` (Amélioration)** | Audit V11 | Partiellement implémenté | Améliorer l'heuristique de tri des conduites. Remplacer le simple tri par longueur par une métrique de **"criticité"** plus évoluée (ex: combinant longueur, diamètre, impact sur la pression). |

---

## Sprint 3 : CLI, Reporting & Expérience Utilisateur

**Objectif :** Exposer toutes les nouvelles capacités du système via une interface en ligne de commande complète et des rapports d'analyse riches.

| Tâche | Origine | Statut (début S3) | Description |
|---|---|---|---|
| **1. Format de Sortie JSON V11** | Audit V11 | Non implémenté | **Prérequis bloquant.** Refactoriser le format de sortie JSON pour qu'il respecte le standard V11 : une clé `proposals` listant plusieurs solutions, une clé `pareto`, et la gestion des résultats multi-réservoirs. |
| **2. Commandes CLI Manquantes** | Audit V11 | Partiellement implémenté | Implémenter les commandes manquantes dans `lcpi aep tank`: `price-optimize` (optimisation avec score pondéré), `report` (régénération d'un rapport), et `diameters-manage` (gestion de la DB de diamètres). |
| **3. Rapport d'Optimisation V11** | Audit V11 | Non implémenté | Mettre à jour le template `optimisation_tank.jinja2` pour qu'il consomme le nouveau format JSON V11. Le rapport doit pouvoir afficher un **tableau comparatif des solutions** et un **graphique du front de Pareto**. |

---

## Sprint 4 : Auditabilité, Tests et Intégration Continue

**Objectif :** Garantir la qualité, la non-régression et l'auditabilité de chaque résultat produit par le système.

| Tâche | Origine | Statut (début S4) | Description |
|---|---|---|---|
| **1. Auditabilité des Résultats** | V12-D | Non implémenté | Intégrer un système de **signature cryptographique** pour chaque sortie JSON. Mettre en place une base de données SQLite (`results/index.db`) pour **indexer chaque exécution**. Créer une commande `lcpi aep tank verify-log` pour valider une signature. |
| **2. Intégration Continue (CI)** | V12-D | Non implémenté | Mettre en place un workflow **GitHub Actions** qui exécute automatiquement les tests unitaires et d'intégration à chaque `push` et `pull request`. Configurer le cache des dépendances pour accélérer les exécutions. |
| **3. Couverture de Tests Complète** | V11-Audit / V12-D | Partiellement implémenté | Créer les fichiers de tests manquants et ajouter des tests unitaires et d'intégration pour toutes les nouvelles fonctionnalités : `scoring.py` (knee-point), `cache.py` (persistance), `multi_tank.py`, les modèles Pydantic, le DAO, et des tests **end-to-end** pour la CI. |
