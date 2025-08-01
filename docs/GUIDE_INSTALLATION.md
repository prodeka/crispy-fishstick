# 🚀 Guide d'Installation LCPI-CLI

## Prérequis

### Système d'exploitation
- **Windows** : 10/11 (64-bit)
- **macOS** : 10.15+ (Catalina)
- **Linux** : Ubuntu 18.04+, CentOS 7+, Debian 9+

### Python
- **Version** : Python 3.8+
- **Recommandé** : Python 3.11 ou 3.12
- **Pip** : Version 21.0+

### Espace disque
- **Minimum** : 500 MB
- **Recommandé** : 1 GB

## Installation

### 1. Installation Automatique (Recommandée)

#### Windows
```bash
# Télécharger et exécuter le script d'installation
python scripts\install_wizard.py

# Ou utiliser le batch file
install.bat
```

#### macOS/Linux
```bash
# Exécuter le script d'installation
python scripts/install_wizard.py

# Ou utiliser le shell script
./install.sh
```

### 2. Installation Manuelle

#### Étape 1 : Cloner le Repository
```bash
git clone https://github.com/lcpi/lcpi-cli.git
cd lcpi-cli
```

#### Étape 2 : Créer un Environnement Virtuel
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### Étape 3 : Installer les Dépendances
```bash
# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt
```

#### Étape 4 : Installer LCPI-CLI
```bash
# Installation en mode développement
pip install -e .

# Ou installation normale
pip install .
```

### 3. Installation via Pip (Version Stable)

```bash
# Installation directe depuis PyPI
pip install lcpi-cli

# Ou avec des options spécifiques
pip install lcpi-cli[all]
```

## Configuration

### 1. Vérification de l'Installation

```bash
# Vérifier que LCPI-CLI est installé
lcpi --version

# Diagnostic complet
lcpi doctor
```

### 2. Configuration Initiale

#### Créer un Fichier de Configuration
```bash
# Créer le dossier de configuration
mkdir ~/.lcpi

# Créer le fichier de configuration
touch ~/.lcpi/config.yml
```

#### Contenu du Fichier de Configuration
```yaml
# ~/.lcpi/config.yml
user:
  name: "Votre Nom"
  email: "votre.email@example.com"
  organization: "Votre Organisation"

system:
  language: "fr"
  units: "metric"
  output_format: "rich"

plugins:
  auto_load: true
  default_plugins: ["cm", "bois", "beton", "hydrodrain"]

paths:
  data: "~/lcpi/data"
  output: "~/lcpi/output"
  templates: "~/lcpi/templates"
```

### 3. Activation des Plugins

```bash
# Voir les plugins disponibles
lcpi plugins list

# Activer un plugin
lcpi plugins install cm
lcpi plugins install bois
lcpi plugins install beton
lcpi plugins install hydrodrain

# Activer tous les plugins
lcpi plugins install all
```

## Licence

### 1. Types de Licence

- **Standard** : Utilisation personnelle et éducative
- **Premium** : Utilisation professionnelle
- **Enterprise** : Utilisation en entreprise

### 2. Activation de la Licence

```bash
# Générer une licence d'essai
lcpi license generate --type trial --days 30

# Activer une licence
lcpi license activate --key YOUR_LICENSE_KEY

# Vérifier le statut
lcpi license status
```

### 3. Gestion des Licences

```bash
# Voir les licences disponibles
lcpi license list

# Renouveler une licence
lcpi license renew --key YOUR_LICENSE_KEY

# Désactiver une licence
lcpi license deactivate
```

## Première Utilisation

### 1. Test de l'Installation

```bash
# Test complet
lcpi doctor

# Voir l'aide
lcpi --help

# Message de bienvenue
lcpi welcome
```

### 2. Créer un Premier Projet

```bash
# Initialiser un projet
lcpi init mon_premier_projet

# Aller dans le projet
cd mon_premier_projet

# Voir la structure
ls -la
```

### 3. Premier Calcul

```bash
# Exemple avec Construction Métallique
lcpi cm check-poteau data/cm/poteau_exemple.yml

# Exemple avec Construction Bois
lcpi bois check-poteau data/bois/poteau_exemple.yml

# Exemple avec Béton Armé
lcpi beton calc-poteau data/beton/poteau_exemple.yml
```

## Dépannage

### Problèmes Courants

#### 1. Erreur "lcpi command not found"
```bash
# Vérifier l'installation
pip list | grep lcpi

# Réinstaller
pip uninstall lcpi-cli
pip install -e .
```

#### 2. Erreur de Module
```bash
# Vérifier les dépendances
pip install -r requirements.txt

# Mettre à jour pip
pip install --upgrade pip
```

#### 3. Erreur de Licence
```bash
# Vérifier le statut
lcpi license status

# Régénérer une licence d'essai
lcpi license generate --type trial
```

#### 4. Erreur d'Encodage
```bash
# Windows : Définir l'encodage
set PYTHONIOENCODING=utf-8

# Linux/macOS
export PYTHONIOENCODING=utf-8
```

### Logs et Diagnostic

```bash
# Mode verbose
lcpi --verbose doctor

# Logs détaillés
lcpi --log-level DEBUG doctor

# Diagnostic complet
lcpi doctor --full
```

## Mise à Jour

### Mise à Jour Automatique

```bash
# Mettre à jour LCPI-CLI
pip install --upgrade lcpi-cli

# Mettre à jour les dépendances
pip install --upgrade -r requirements.txt
```

### Mise à Jour Manuelle

```bash
# Désinstaller l'ancienne version
pip uninstall lcpi-cli

# Installer la nouvelle version
pip install lcpi-cli
```

## Désinstallation

### Désinstallation Complète

```bash
# Désinstaller LCPI-CLI
pip uninstall lcpi-cli

# Supprimer les fichiers de configuration
rm -rf ~/.lcpi

# Supprimer l'environnement virtuel (si utilisé)
rm -rf venv
```

### Nettoyage des Données

```bash
# Supprimer les projets créés
rm -rf ~/lcpi

# Supprimer les caches
rm -rf ~/.cache/lcpi
```

## Support

### Ressources d'Aide

- **Documentation** : [docs/](docs/)
- **Exemples** : [examples/](examples/)
- **Issues** : [GitHub Issues](https://github.com/lcpi/issues)
- **Discussions** : [GitHub Discussions](https://github.com/lcpi/discussions)

### Contact

- **Email** : support@lcpi.com
- **Discord** : [Serveur LCPI](https://discord.gg/lcpi)
- **Forum** : [Forum Communautaire](https://forum.lcpi.com)

---

**Version du guide** : 2.0.0  
**Dernière mise à jour** : 2025-08-01  
**Compatibilité** : LCPI-CLI 2.0.0+ 