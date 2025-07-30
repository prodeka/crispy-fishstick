### **Comment Partager votre Programme LCPI-CLI**

#### **Étape 1 : Préparer Chaque Paquet pour la Publication**

Chaque dossier de votre plateforme (`lcpi-core`, `lcpi-cm`, `lcpi-bois`, etc.) est un **paquet Python indépendant**. Vous devez préparer chacun d'eux pour la publication.

**Action : Compléter le fichier `pyproject.toml` de chaque paquet.**

Le fichier `pyproject.toml` est le fichier de configuration moderne pour les paquets Python. Vous devez le remplir avec les métadonnées de votre projet.

**Exemple pour le `lcpi-core` :**

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "lcpi-core"
version = "0.1.0" # La version de votre noyau
authors = [
  { name="Votre Nom", email="votre.email@example.com" },
]
description = "Noyau de la plateforme de calcul polyvalent pour l'ingénierie LCPI-CLI."
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License", # Choisissez votre licence
    "Operating System :: OS Independent",
]
dependencies = [
    "typer",
    "rich", # Si vous utilisez la bibliothèque Rich pour de beaux affichages
    "PyYAML", # Pour lire les fichiers .yml
]

# C'est la ligne la plus importante pour une application CLI
[project.scripts]
lcpi = "lcpi_core.main:app" # Crée la commande "lcpi" qui pointe vers l'objet "app" dans "main.py"
```

**Exemple pour un plugin comme `lcpi-cm` :**

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "lcpi-cm"
version = "0.1.0" # La version de votre plugin
authors = [
  { name="Votre Nom", email="votre.email@example.com" },
]
description = "Plugin de Construction Métallique pour la plateforme LCPI-CLI."
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    # ...
]
dependencies = [
    "lcpi-core", # Le plugin dépend du noyau !
    "pandas",   # Si vous utilisez pandas pour les calculs
]

# C'est la ligne qui le déclare comme un plugin pour lcpi-core
[project.entry-points."lcpi.plugins"]
cm = "lcpi_cm.main:register"
```

#### **Étape 2 : Publier les Paquets sur PyPI**

PyPI (Python Package Index) est le dépôt public officiel où sont stockés tous les paquets installables avec `pip`. C'est l'équivalent du "Google Play Store" pour les développeurs Python.

1.  **Créez un Compte sur PyPI :** Allez sur [pypi.org](https://pypi.org/) et créez un compte.
2.  **Générez une Clé API PyPI :** Dans les paramètres de votre compte, générez un "API token". C'est ce qui vous permettra de pousser votre code.
3.  **Construisez vos Paquets :**
    *   Installez les outils de build : `pip install build twine`.
    *   Pour chaque paquet (en commençant par `lcpi-core`), allez dans son répertoire et lancez la commande `python -m build`.
    *   Cela va créer un dossier `dist/` contenant les fichiers de votre paquet (`.whl` et `.tar.gz`).
4.  **Uploadez vos Paquets :**
    *   Depuis le répertoire de chaque paquet, lancez la commande : `twine upload dist/*`.
    *   On vous demandera votre nom d'utilisateur (pour PyPI, c'est `__token__`) et votre mot de passe (c'est le token que vous avez généré).

**Ordre de publication :** Vous devez publier `lcpi-core` **en premier**, car les plugins en dépendent.

#### **Étape 3 : L'Utilisateur Final Installe votre Programme**

Une fois vos paquets publiés, le partage devient incroyablement simple. Vous pouvez dire à n'importe qui dans le monde :

"Pour installer ma plateforme, ouvre un terminal et tape :"

```bash
# Installe le noyau et le plugin de construction métallique
pip install lcpi-core lcpi-cm

# Si l'utilisateur veut aussi le béton
pip install lcpi-beton
```

Et c'est tout ! `pip` va automatiquement télécharger vos paquets depuis PyPI, gérer les dépendances, et la commande `lcpi` sera immédiatement disponible dans leur terminal.

---

### **Alternative : Partage Privé (sans PyPI)**

Si vous ne voulez pas rendre votre projet public, vous pouvez le partager de manière privée :

1.  **Partage via Git :** Donnez accès à votre dépôt Git (sur GitHub, GitLab...). L'utilisateur clone le projet et peut l'installer en "mode éditable" :
    ```bash
    git clone https://votre_depot/lcpi.git
    cd lcpi
    pip install -e ./lcpi_platform/lcpi-core
    pip install -e ./lcpi_platform/lcpi-cm
    ```
2.  **Partage via des Fichiers de Paquet :** Vous pouvez construire les paquets (`.whl`) comme décrit à l'étape 2, mais au lieu de les uploader sur PyPI, vous les envoyez directement à votre utilisateur (par email, clé USB...). Il pourra alors les installer depuis son disque local :
    ```bash
    pip install lcpi-core-0.1.0-py3-none-any.whl
    pip install lcpi-cm-0.1.0-py3-none-any.whl
    ```

**En résumé :** La préparation des fichiers `pyproject.toml` est l'étape clé qui transforme votre code source en un produit logiciel professionnel et distribuable.