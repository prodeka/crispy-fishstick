# Plugin QGIS pour LCPI-CLI

Ce répertoire contient le code source pour un plugin QGIS destiné à intégrer l'outil de calcul `lcpi-cli`.

## Objectif

L'objectif de ce plugin est de fournir une interface graphique conviviale dans QGIS pour :
1.  Sélectionner des données géospatiales (points, lignes, polygones).
2.  Configurer les paramètres de calcul pour les différents modules de `lcpi` (`aep`, `beton`, `cm`, `bois`).
3.  Générer automatiquement les fichiers d'entrée (`.yml`) pour `lcpi`.
4.  Exécuter les commandes de calcul `lcpi` en arrière-plan.
5.  Récupérer les résultats et les afficher directement dans QGIS (mise à jour d'attributs, création de nouvelles couches, stylisation).

## Prochaines Étapes

1.  **Installer l'environnement de développement QGIS** :
    *   Installer `pb_tool` (Plugin Builder tool) et `Qt Designer`.
    *   Configurer le répertoire du plugin dans les options de QGIS.
2.  **Créer l'interface utilisateur** :
    *   Utiliser Qt Designer pour créer une boîte de dialogue (`.ui` file) dans le dossier `ui/`.
    *   L'interface devra permettre de choisir le module `lcpi` à utiliser et de mapper les champs des couches QGIS aux paramètres `lcpi`.
3.  **Développer la logique du plugin** (dans `main_plugin.py` et d'autres fichiers Python) :
    *   Charger l'interface utilisateur.
    *   Implémenter la logique pour lire les données des couches QGIS.
    *   Générer le fichier de configuration `.yml`.
    *   Appeler `lcpi.bat` ou `lcpi.py` avec `subprocess`.
    *   Parser la sortie JSON et mettre à jour le projet QGIS.
4.  **Compiler les ressources** :
    *   Utiliser `pyrcc5 -o resources.py resources.qrc` pour compiler le fichier de ressources.

## Modules à Intégrer

L'architecture du plugin doit être modulaire pour permettre d'intégrer facilement :
-   [ ] **AEP** : Calcul de réseaux d'adduction d'eau potable.
-   [ ] **Béton** : Calcul d'éléments en béton armé (poteaux, poutres, radiers).
-   [ ] **CM** : Calcul d'éléments en construction métallique.
-   [ ] **Bois** : Calcul d'éléments en bois.
