# Guide d'Utilisation LCPI Platform

## Installation

```bash
pip install -r requirements.txt
```

## Lancement du shell interactif

```bash
lcpi shell
```

## Commandes principales

- **Initialiser un projet** :  
  `lcpi init mon_projet [--template hangar-mixte-bois-acier]`
- **Gérer les plugins** :  
  `lcpi plugins list`  
  `lcpi plugins install hydrodrain`
- **Configurer LCPI** :  
  `lcpi config set user.name "Mon Nom"`
- **Générer un rapport** :  
  `lcpi report --output pdf`
- **Vérifier l’installation** :  
  `lcpi doctor`

## Utilisation des modules

### 1. Ouvrages hydrauliques (workflow YAML)

```bash
lcpi hydro ouvrage init-canal canal_exemple.yml
lcpi hydro ouvrage canal-dimensionner canal_exemple.yml
```

### 2. Population

```bash
lcpi hydro util prevoir-population --method logistique --annee 2050
```
- Méthodes disponibles : arithmetique, lineaire, geometrique, exponentiel, malthus, logistique

### 3. Pluviométrie

```bash
lcpi hydro pluvio analyser data/pluies.csv
lcpi hydro pluvio ajuster-loi data/pluies.csv
```

---

## Shell interactif

- Lancer `lcpi shell`
- Saisir n’importe quelle commande LCPI à l’invite `>`
- Sortir avec `exit` ou `quit`

---

## Bonnes pratiques

- Organiser les fichiers YAML dans `elements/`, les données dans `data/`
- Valider les fichiers YAML avant calcul
- Utiliser les commandes `init-canal`, `init-dalot`, etc. pour générer des templates

---

## Dépannage

- **Erreur de module non trouvé** : vérifier le PYTHONPATH et l’environnement
- **Erreur de dépendance manquante** : installer avec `pip install -r requirements.txt`
- **Erreur de fichier YAML invalide** : vérifier la syntaxe YAML
- **Erreur de calcul** : vérifier les valeurs d’entrée et les unités

---

## Tests

```bash
pytest tests/
```

---

## Support

- Voir la documentation technique et les exemples dans le dossier `src/lcpi/`
- Utiliser les tests unitaires pour valider les modules 

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