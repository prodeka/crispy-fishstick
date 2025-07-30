# LCPI-CLI - Plateforme Modulaire de Calcul d'Ingénierie

## Description
`lcpi-cli` est une application en ligne de commande (CLI) conçue pour le calcul et le dimensionnement dans divers domaines de l'ingénierie civile. Son architecture modulaire permet d'étendre ses fonctionnalités via des plugins spécialisés (béton, bois, construction métallique, hydraulique).

Le noyau de l'application fournit une interface unifiée et des outils communs, tandis que chaque plugin apporte une logique métier spécifique.

## Installation du Noyau

### Prérequis
- Python 3.8+
- `pip` (gestionnaire de paquets Python)

### Étapes d'installation
1.  **Cloner le dépôt (si ce n'est pas déjà fait) :**
    ```bash
    git clone <URL_DU_DEPOT>
    cd PROJET_DIMENTIONEMENT_2
    ```

2.  **Créer et activer un environnement virtuel (recommandé) :**
    ```bash
    python -m venv venv
    # Sur Windows:
    .\venv\Scripts\activate
    # Sur macOS/Linux:
    source venv/bin/activate
    ```

3.  **Installer le noyau `lcpi-cli` :**
    Le script `install.bat` installe le projet en mode "éditable", ce qui signifie que les modifications que vous faites au code source sont immédiatement disponibles sans avoir à réinstaller.
    ```bash
    # Exécutez le script d'installation
    install.bat
    ```
    Cela installe le paquet `lcpi-cli` et ses dépendances de base.

## Utilisation
Une fois l'installation terminée, la commande `lcpi` est disponible dans votre terminal.
```bash
# Afficher l'aide principale
lcpi --help

# Afficher l'aide d'un plugin (s'il est installé)
lcpi beton --help
```

### Shell Interactif
`lcpi-cli` inclut un shell interactif pour lancer des commandes sans avoir à retaper `lcpi` à chaque fois.
```bash
lcpi shell
```
**Note pour les utilisateurs Windows :** Si la commande ci-dessus se ferme immédiatement sans afficher l'invite `>`, cela est probablement dû à un problème de gestion de la console par la librairie sous-jacente. Dans ce cas, utilisez le script de contournement `run_shell.py` :
```bash
python run_shell.py
```

## Installation des Plugins
Les fonctionnalités de `lcpi-cli` sont étendues via des plugins qui doivent être installés séparément.

Pour installer un plugin, une commande dédiée sera bientôt disponible. Par exemple :
```bash
# Exemple de la future commande d'installation de plugin
lcpi plugins install hydro
```
*Note : L'implémentation de cette commande est en cours. Pour le moment, les plugins sont inclus dans le code source mais ne sont pas activés par défaut.*

## Structure du Projet
Le projet est organisé autour d'un noyau et de plusieurs plugins :
```
src/
└───lcpi/
    ├───main.py         # Point d'entrée de la CLI
    ├───reporter.py     # Moteur de rapport
    ├───utils/          # Utilitaires partagés
    ├───beton/          # Plugin pour le béton armé
    ├───bois/           # Plugin pour le bois
    ├───cm/             # Plugin pour la construction métallique
    └───hydrodrain/     # Plugin pour l'hydraulique/assainissement
```

## Contribution
Les contributions sont les bienvenues. Veuillez suivre les bonnes pratiques de développement (Pull Requests, etc.).