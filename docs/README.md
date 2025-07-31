# LCPI-CLI - Plateforme Modulaire de Calcul d'Ingénierie

## Description
`lcpi-cli` est une application en ligne de commande (CLI) conçue pour le calcul et le dimensionnement dans divers domaines de l'ingénierie civile. Son architecture modulaire permet d'étendre ses fonctionnalités via des plugins spécialisés (béton, bois, construction métallique, hydraulique).

Le noyau de l'application fournit une interface unifiée et des outils communs, tandis que chaque plugin apporte une logique métier spécifique.

## Nouveautés UX (2025)

- **Assistant d'installation interactif** :
  - `python scripts/install_wizard.py` (interface guidée, choix des plugins, feedback visuel)
- **Messages de licence explicites** :
  - Affichage d'un panneau vert "✅ Licence activée avec succès pour [Nom] (valide jusqu'au ...)" lors de l'installation et au démarrage
- **Commandes UX** :
  - `lcpi tips` : Astuces quotidiennes
  - `lcpi guide` : Guides interactifs (installation, plugins, dépannage...)
  - `lcpi examples` : Exemples d'utilisation contextuels
  - `lcpi welcome` : Message de bienvenue et raccourcis
- **Documentation interactive** :
  - Guide de démarrage rapide : `docs/QUICK_START.md`
  - Exemples et dépannage rapide

## Installation du Noyau

### Prérequis
- Python 3.8+
- `pip` (gestionnaire de paquets Python)

### Installation rapide

```bash
# Assistant interactif (recommandé)
python scripts/install_wizard.py

# Ou installation manuelle
pip install -r requirements.txt
pip install -e .
```

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

## Installation des Plugins

Les fonctionnalités de `lcpi-cli` sont étendues via des plugins qui doivent être activés après installation.

```bash
lcpi plugins list
lcpi plugins install hydro
```

## Commandes UX

- `lcpi tips` : Astuces du jour
- `lcpi guide` : Guides interactifs
- `lcpi examples` : Exemples d'utilisation
- `lcpi welcome` : Message de bienvenue

## Guide de démarrage rapide

Voir `docs/QUICK_START.md` pour un tutoriel pas à pas, des exemples concrets et des solutions de dépannage.

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