# Documentation LCPI Platform

## Vue d'ensemble

LCPI Platform est une plateforme modulaire de calculs d'ingénierie civile, regroupant plusieurs modules spécialisés pour la construction, l’hydraulique et l’hydrologie. 
**Utilisation moderne via une CLI unifiée (`lcpi`) et un shell interactif (`lcpi shell`).**

---

### Architecture générale

- **Modulaire** : chaque domaine (acier, bois, béton, hydraulique) est un plugin.
- **Extensible** : nouveaux modules/plugins ajoutables sans modifier le noyau.
- **Standard YAML** : tous les calculs d’ouvrages utilisent des fichiers de configuration YAML.

#### Structure des modules

```
src/lcpi/
├── main.py           # Point d'entrée CLI
├── cm/               # Construction Métallique
├── bois/             # Construction Bois
├── beton/            # Béton Armé
├── hydrodrain/       # Hydraulique et Hydrologie
├── utils/            # Utilitaires transverses
```

---

### Utilisation rapide

#### Installation

```bash
pip install -r requirements.txt
```

#### Lancer le shell interactif

```bash
lcpi shell
```

#### Exemples de commandes

```bash
# Générer un template YAML pour un canal
lcpi hydro ouvrage init-canal canal_exemple.yml

# Dimensionner un canal à partir du template
lcpi hydro ouvrage canal-dimensionner canal_exemple.yml

# Estimer une population future
lcpi hydro util prevoir-population --method geometrique --annee 2030
```

#### Commandes du noyau

- `lcpi init [nom-projet] [--template <nom>]`
- `lcpi plugins <list|install|uninstall|search|update> [nom-plugin]`
- `lcpi config [get|set|list] <clé> [valeur] [--global]`
- `lcpi report [--output <pdf|md|html>]`
- `lcpi doctor`

---

### Tests

```bash
pytest tests/
```

---

### Contribution

- Respecter l’architecture modulaire
- Documenter toute nouvelle fonctionnalité
- Ajouter des tests unitaires
- Utiliser le format YAML pour les entrées 

---

## Shell interactif et gestion des erreurs

### Lancer le shell interactif

```bash
lcpi shell
```

- Tapez n'importe quelle commande LCPI à l'invite `>`
- Tapez `exit` ou `quit` pour sortir

### Erreurs courantes

- **Module non trouvé** : vérifiez le PYTHONPATH et l'environnement
- **Dépendance manquante** : installez avec `pip install -r requirements.txt`
- **Fichier YAML invalide** : vérifiez la syntaxe YAML
- **Erreur de calcul** : vérifiez les valeurs d'entrée et les unités 