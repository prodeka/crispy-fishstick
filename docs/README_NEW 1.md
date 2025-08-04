# lcpi-core
## Guide d'installation et d'utilisation

`lcpi-core` est une plateforme de calcul polyvalente pour l'ingénierie. Elle fournit un noyau robuste et un système de plugins pour effectuer divers calculs dans des domaines tels que la construction métallique, le bois, le béton armé et l'hydrologie. Ce guide vous aidera à installer, configurer et utiliser `lcpi-core`.

## Prérequis

Avant d'installer `lcpi-core`, assurez-vous que les éléments suivants sont installés sur votre système :

*   **Python** : Version 3.8 ou supérieure.
*   **Pip** : Le gestionnaire de paquets pour Python, généralement inclus avec les installations de Python.
*   **Git** : Recommandé pour la gestion des versions du projet.

Les bibliothèques Python suivantes sont nécessaires et seront installées automatiquement par le script d'installation :
*   `typer[all]`
*   `PyYAML`
*   `pandas`
*   `matplotlib`
*   `reportlab`
*   `scipy`
*   `Jinja2`
*   `python-docx`
*   `rich`
*   `cryptography`

## Procédure d'installation

L'installation de `lcpi-core` est gérée par un script qui simplifie le processus.

1.  **Clonez le dépôt du projet (si ce n'est pas déjà fait) :**
    ```bash
    git clone <url_du_depot>
    cd <nom_du_dossier_du_projet>
    ```

2.  **Exécutez le script d'installation :**
    Le moyen le plus simple de lancer l'installation est d'utiliser le fichier batch `install.bat` qui se charge d'appeler le script Python principal.

    ```bash
    install.bat
    ```

    Alternativement, vous pouvez exécuter le script Python directement :

    ```bash
    python scripts/install_and_run_lcpi_core.py
    ```

3.  **Suivez les instructions à l'écran :**
    *   **Acceptation de la licence :** Vous devrez accepter les termes de la licence et le disclaimer pour continuer.
    *   **Installation des dépendances :** Le script détectera si vous avez une connexion Internet. Il tentera d'installer les dépendances en ligne. En cas d'échec, il vous proposera de les installer en mode hors ligne à partir du dossier `vendor/packages`.
    *   **Installation du noyau :** Le noyau `lcpi-core` sera installé en mode éditable, ce qui signifie que les modifications que vous apportez au code source seront immédiatement disponibles.
    *   **Configuration des plugins :** Les plugins de base (`shell`, `utils`) sont activés par défaut.

## Configuration

### Fichier de configuration du projet
Lorsque vous initialisez un nouveau projet avec `lcpi init`, un fichier `config.yml` est créé. Il vous permet de définir des paramètres spécifiques au projet.

```yaml
# Configuration du projet LCPI
projet:
  nom: "mon_projet"
  version: "1.0.0"
  ...
plugins_actifs:
  - cm
  - bois
parametres_globaux:
  unite_longueur: "m"
  unite_force: "kN"
  ...
```

### Configuration globale
La commande `lcpi config` vous permet de gérer les paramètres de configuration globaux (pour tous les projets) ou locaux (pour le projet courant).

*   **Définir une valeur :**
    ```bash
    lcpi config set ma_cle ma_valeur --global
    ```
*   **Obtenir une valeur :**
    ```bash
    lcpi config get ma_cle
    ```
*   **Lister la configuration :**
    ```bash
    lcpi config list
    ```

## Utilisation

### Initialiser un nouveau projet
La première étape pour utiliser `lcpi-core` est de créer un nouveau projet.

```bash
lcpi init mon_projet_genial --template complet
```
Cette commande crée un nouveau dossier `mon_projet_genial` avec une arborescence de projet complète, incluant des dossiers pour les données (`data`), les résultats (`output`), les rapports (`reports`) et les exemples.

### Vérifier l'installation
Pour vous assurer que tout est correctement configuré, utilisez la commande `doctor`.

```bash
lcpi doctor
```

### Gérer les plugins
Le noyau de `lcpi-core` est léger. Vous devez activer les plugins métier dont vous avez besoin.

*   **Lister les plugins disponibles et leur statut :**
    ```bash
    lcpi plugins list
    ```
*   **Installer (activer) un plugin :**
    ```bash
    lcpi plugins install beton
    ```
*   **Désinstaller (désactiver) un plugin :**
    ```bash
    lcpi plugins uninstall beton
    ```

### Exemple d'utilisation de base
1.  **Créez un projet :**
    ```bash
    lcpi init mon_projet_beton --template beton
    cd mon_projet_beton
    ```
2.  **Activez le plugin `beton` (s'il ne l'est pas déjà) :**
    ```bash
    lcpi plugins install beton
    ```
3.  **Exécutez un calcul :**
    Le dossier `data/beton` contient des exemples de fichiers `.yml`. Vous pouvez lancer un calcul sur l'un d'eux.
    ```bash
    lcpi beton calc-poteau data/beton/poteau_exemple.yml
    ```
4.  **Générez un rapport de synthèse :**
    La commande `report` scanne votre projet, exécute les calculs pertinents et génère un rapport PDF.
    ```bash
    lcpi report .
    ```
    Un fichier `rapport_lcpi.pdf` sera créé dans le dossier `output`.

## Architecture du projet

*   `src/lcpi/`: Contient le code source du noyau de l'application.
    *   `main.py`: Le point d'entrée principal de l'application, utilisant Typer pour la CLI.
    *   `reporter.py`: Le moteur de génération de rapports.
    *   `license_validator.py`: Le système de gestion des licences.
    *   `plugins/`: Chaque sous-dossier correspond à un plugin avec sa propre logique et ses propres commandes.
*   `scripts/`: Contient des scripts utiles, notamment `install_and_run_lcpi_core.py`.
*   `docs/`: Contient la documentation du projet au format Markdown.
*   `data/`: Contient des données d'exemples et de tests pour les différents plugins.
*   `examples/`: Contient des exemples de fichiers de définition `.yml`.

## Contribution

Les contributions sont les bienvenues. Si vous souhaitez contribuer au projet, veuillez suivre les étapes suivantes :

1.  Forkez le dépôt.
2.  Créez une nouvelle branche pour votre fonctionnalité (`git checkout -b feature/ma-nouvelle-fonctionnalite`).
3.  Commitez vos changements (`git commit -am 'Ajout de ma nouvelle fonctionnalité'`).
4.  Poussez vers la branche (`git push origin feature/ma-nouvelle-fonctionnalite`).
5.  Créez une nouvelle Pull Request.
