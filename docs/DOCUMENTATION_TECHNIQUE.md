# Documentation Technique de LCPI-CLI

## 1. Introduction

LCPI-CLI est une plateforme de calcul polyvalente pour l'ingénierie, conçue pour être modulaire et extensible. Elle fournit un noyau de base qui gère les fonctionnalités communes telles que la gestion des plugins, la configuration, la génération de rapports, et un système de licence. Des plugins spécifiques à chaque domaine de l'ingénierie (béton, bois, construction métallique, hydrologie) peuvent être activés pour étendre les fonctionnalités de l'application.

## 2. Architecture

L'application est basée sur une architecture modulaire composée d'un noyau (core) et de plugins. Le noyau fournit les fonctionnalités de base et les plugins ajoutent des commandes et des logiques de calcul spécifiques à un domaine.

### 2.1. Noyau (Core)

Le noyau est responsable des fonctionnalités suivantes :

*   **Gestion des plugins** : Le noyau découvre et charge les plugins disponibles. Il permet à l'utilisateur d'activer ou de désactiver les plugins.
*   **Gestion de la configuration** : Le noyau fournit un système de configuration pour gérer les paramètres de l'application.
*   **Génération de rapports** : Le noyau peut générer des rapports de synthèse à partir des résultats des calculs des plugins.
*   **Système de licence** : Le noyau intègre un système de licence pour contrôler l'accès aux fonctionnalités.

### 2.2. Plugins

Les plugins sont des modules autonomes qui ajoutent des fonctionnalités spécifiques à l'application. Chaque plugin est un sous-répertoire dans le dossier `src/lcpi` et doit contenir un fichier `main.py` qui définit les commandes du plugin et une fonction `register()` qui renvoie l'application `typer` du plugin.

## 3. Noyau (Core)

Le noyau est implémenté dans le fichier `src/lcpi/main.py`. Il utilise la bibliothèque `typer` pour créer l'interface en ligne de commande.

### 3.1. Gestion des Plugins

La gestion des plugins est assurée par les fonctions `get_plugin_config`, `save_plugin_config`, et `get_available_plugins`. La commande `lcpi plugins` permet à l'utilisateur de lister, d'installer (activer) et de désinstaller (désactiver) les plugins.

### 3.2. Génération de Rapports

La génération de rapports est gérée par le module `src/lcpi/reporter.py`. La commande `lcpi report` analyse un projet, collecte les résultats des calculs des plugins et génère un rapport de synthèse au format PDF, JSON, HTML, DOCX ou CSV.

## 4. Plugins

### 4.1. Plugin `beton`

Le plugin `beton` fournit des fonctionnalités pour le calcul des structures en béton armé. Il contient les commandes suivantes :

*   `calc-poteau` : Calcule un poteau en béton armé en flexion composée ou en compression centrée.
*   `calc-radier` : Calcule un radier en béton armé.
*   `interactive` : Lance un mode interactif pour le calcul des éléments en béton.

### 4.2. Plugin `bois`

Le plugin `bois` fournit des fonctionnalités pour le calcul des structures en bois. Il contient les commandes suivantes :

*   `check-poteau` : Vérifie un poteau en bois en compression avec flambement.
*   `check-deversement` : Vérifie le déversement d'une poutre en bois.
*   `check-cisaillement` : Vérifie le cisaillement d'une poutre en bois.
*   `check-compression-perp` : Vérifie la compression perpendiculaire au fil du bois.
*   `check-compose` : Vérifie les sollicitations composées.
*   `check-fleche` : Vérifie la flèche d'une poutre en bois.
*   `check-assemblage-pointe` : Vérifie un assemblage par pointes.
*   `check-assemblage-embrevement` : Vérifie un assemblage par embrèvement.

### 4.3. Plugin `cm`

Le plugin `cm` (Construction Métallique) fournit des fonctionnalités pour le calcul des structures métalliques. Il contient les commandes suivantes :

*   `check-poteau` : Vérifie un poteau en compression/flambement.
*   `check-deversement` : Vérifie le déversement d'une poutre.
*   `check-tendu` : Vérifie un élément tendu.
*   `check-compose` : Vérifie les sollicitations composées.
*   `check-fleche` : Vérifie la flèche d'une poutre.
*   `check-assemblage-boulon` : Vérifie un assemblage boulonné.
*   `check-assemblage-soude` : Vérifie un assemblage soudé.
*   `optimize-section` : Optimise la section d'un profilé.

### 4.4. Plugin `hydro`

Le plugin `hydro` (Hydrologie) fournit des fonctionnalités pour les calculs hydrologiques et hydrauliques. Il est divisé en plusieurs sous-plugins :

*   `pluvio` : Gestion et analyse des données pluviométriques.
*   `bassin` : Analyse hydrologique et modélisation des bassins versants.
*   `ouvrage` : Dimensionnement et analyse hydraulique des ouvrages.
*   `util` : Utilitaires et analyses spécifiques.
*   `plomberie` : Dimensionnement des réseaux internes de plomberie.
*   `stockage` : Dimensionnement des ouvrages de stockage et régulation.

### 4.5. Plugin `shell`

Le plugin `shell` fournit un interpréteur de commandes interactif pour LCPI-CLI.

## 5. Système de Licence

Le système de licence est implémenté dans le module `src/lcpi/license_validator.py`. Il utilise la cryptographie pour générer et valider les clés de licence. La validation est basée sur une empreinte machine unique et une date d'expiration.

## 6. Guide du Développeur

Pour créer un nouveau plugin, il suffit de créer un nouveau sous-répertoire dans `src/lcpi` et d'y ajouter un fichier `main.py`. Ce fichier doit contenir une application `typer` et une fonction `register()` qui la renvoie. Le noyau de l'application se chargera de découvrir et de charger automatiquement le nouveau plugin.