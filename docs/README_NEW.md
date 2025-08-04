# LCPI-CLI : Guide d'Installation et d'Utilisation

Bienvenue sur LCPI-CLI, une plateforme modulaire de calcul d'ingénierie conçue pour être à la fois puissante et facile à utiliser.

## Table des matières

1.  [Philosophie du projet](#philosophie-du-projet)
2.  [Installation](#installation)
3.  [Premiers Pas](#premiers-pas)
4.  [Gestion des Plugins](#gestion-des-plugins)
5.  [Commandes Principales](#commandes-principales)
6.  [Exemple d'Utilisation](#exemple-dutilisation)
7.  [Contribuer](#contribuer)

## Philosophie du projet

LCPI-CLI est construit sur une architecture modulaire. Le **noyau (`lcpi-core`)** fournit les fonctionnalités de base et une interface de ligne de commande unifiée. Les **plugins** étendent le noyau avec des logiques métier spécifiques à chaque domaine de l'ingénierie (construction métallique, bois, béton, etc.).

Cette approche permet de n'installer et d'activer que les fonctionnalités dont vous avez besoin, gardant l'application légère et pertinente pour votre travail.

## Installation

L'installation est gérée par un script interactif qui vous guide à travers le processus.

**Prérequis :**
*   Python 3.8 ou supérieur
*   Git

**Étapes :**

1.  **Clonez le dépôt :**
    ```bash
    git clone <URL_DU_DEPOT>
    cd lcpi-cli
    ```

2.  **Exécutez le script d'installation :**
    ```bash
    python scripts/install_and_run_lcpi_core.py
    ```

Le script va :
*   Vérifier votre connexion internet.
*   Vous demander d'accepter la licence.
*   Installer les dépendances requises (depuis `requirements.txt`).
*   Installer le noyau `lcpi-core` en mode éditable.
*   Configurer les plugins de base (`shell`, `utils`).

À la fin de l'installation, le noyau LCPI-CLI sera prêt à l'emploi, mais sans aucun plugin métier.

## Premiers Pas

Une fois l'installation terminée, vous pouvez commencer à utiliser `lcpi`.

1.  **Affichez l'aide :**
    ```bash
    lcpi --help
    ```
    Cette commande liste toutes les commandes de base disponibles dans le noyau.

2.  **Vérifiez votre installation :**
    ```bash
    lcpi doctor
    ```
    Cet outil de diagnostic vérifie que toutes les dépendances sont correctement installées.

3.  **Lancez le shell interactif :**
    ```bash
    lcpi shell
    ```
    Le shell interactif offre une expérience plus fluide pour exécuter des commandes sans avoir à taper `lcpi` à chaque fois.

## Gestion des Plugins

Les fonctionnalités métier sont fournies par des plugins que vous devez installer manuellement.

1.  **Listez les plugins disponibles :**
    ```bash
    lcpi plugins list
    ```
    Cette commande affiche tous les plugins disponibles et leur statut (activé ou désactivé).

2.  **Installez un plugin :**
    Par exemple, pour installer le plugin de construction métallique :
    ```bash
    lcpi plugins install cm
    ```
    Une fois installé, les commandes du plugin `cm` seront disponibles (ex: `lcpi cm --help`).

3.  **Désinstallez un plugin :**
    ```bash
    lcpi plugins uninstall cm
    ```

## Commandes Principales

Voici quelques-unes des commandes du noyau les plus utiles :

*   `lcpi init <nom_projet>` : Crée une nouvelle arborescence de projet avec des dossiers pour les données, les sorties et les rapports.
*   `lcpi report <dossier_projet>` : Analyse tous les fichiers `.yml` d'un projet, exécute les calculs correspondants et génère un rapport de synthèse.
*   `lcpi config [get|set] <cle> [valeur]` : Gère les paramètres de configuration locaux ou globaux.

## Exemple d'Utilisation

Voici un flux de travail typique :

1.  **Installez LCPI-CLI** en suivant les instructions ci-dessus.

2.  **Installez les plugins** dont vous avez besoin (par exemple, `beton` et `cm`).
    ```bash
    lcpi plugins install beton
    lcpi plugins install cm
    ```

3.  **Créez un nouveau projet.**
    ```bash
    lcpi init mon_projet_beton
    cd mon_projet_beton
    ```

4.  **Ajoutez vos fichiers de données** dans le dossier `data/beton`. Par exemple, un fichier `poteau.yml` pour un calcul de poteau en béton.

5.  **Exécutez le calcul.**
    ```bash
    lcpi beton calc-poteau --filepath data/beton/poteau.yml
    ```

6.  **Générez un rapport de projet.**
    ```bash
    lcpi report .
    ```
    Un rapport PDF sera généré dans le dossier `reports`.

## Contribuer

Les contributions sont les bienvenues ! Veuillez consulter le fichier `CONTRIBUTING.md` pour plus de détails sur la manière de proposer des améliorations.
