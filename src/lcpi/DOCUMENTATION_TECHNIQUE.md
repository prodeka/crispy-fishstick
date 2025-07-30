# Documentation Technique LCPI Platform

## Architecture détaillée

- **main.py** : point d’entrée CLI, gestion du shell interactif, chargement dynamique des plugins
- **Commandes du noyau** : `init`, `plugins`, `config`, `doctor`, `report`, `shell`
- **Plugins** : chaque domaine (cm, bois, beton, hydro) est un sous-module avec un `register()`
- **Standard YAML** : tous les calculs d’ouvrages utilisent des fichiers YAML
- **Tests** : tous les modules disposent de tests unitaires dans `tests/modules/`

---

## Shell interactif

- Lancement : `lcpi shell`
- Affiche l’état de chargement des plugins, l’aide CLI, puis une invite `>`
- Toutes les commandes du noyau et des plugins sont accessibles

---

## Gestion de la configuration

- Fichier `.lcpi_config.json` (local ou global)
- Commande `lcpi config` pour get/set/list

---

## Gestion des plugins

- Commande `lcpi plugins` pour lister, installer, désinstaller, rechercher, mettre à jour

---

## Génération de rapports

- Commande `lcpi report` pour agréger les résultats et générer un PDF/MD/HTML

---

## Tests

- Tous les modules disposent de tests unitaires dans `tests/modules/`
- Lancer tous les tests avec :

```bash
pytest tests/
``` 