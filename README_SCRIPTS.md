# 📁 Organisation des Scripts et Tests LCPI-CLI

## 🗂️ Structure des dossiers

```
PROJET_DIMENTIONEMENT_2/
├── 📁 scripts/                    # Tous les scripts utilitaires
│   ├── build_portable.py         # Construction exécutable portable
│   ├── build_lcpi.bat           # Version batch du build
│   ├── create_distribution.py    # Création packages de distribution
│   ├── install_portable.py       # Installation avec choix
│   ├── lcpi.bat                 # Script de lancement LCPI
│   ├── setup_lcpi_*.ps1         # Scripts PowerShell d'installation
│   └── ...                      # Autres scripts utilitaires
├── 📁 tests/                     # Tous les tests et démos
│   ├── test_*.py                # Tests unitaires et d'intégration
│   ├── demo_*.py                # Scripts de démonstration
│   ├── debug_*.py               # Scripts de débogage
│   └── ...                      # Autres fichiers de test
├── 🚀 build_distribution.py      # Lanceur principal (racine)
├── 🚀 build_distribution.bat     # Lanceur batch (racine)
└── ...                          # Autres fichiers du projet
```

## 🚀 Utilisation des scripts

### **Scripts de distribution (racine)**
```bash
# Version Python
python build_distribution.py

# Version Batch (Windows)
build_distribution.bat
```

### **Scripts directs dans le dossier scripts/**
```bash
# Construction portable
python scripts/build_portable.py
scripts/build_lcpi.bat

# Création de distribution
python scripts/create_distribution.py

# Installation
python scripts/install_portable.py
```

### **Tests dans le dossier tests/**
```bash
# Lancer tous les tests
python -m pytest tests/

# Lancer un test spécifique
python tests/test_cli.py
```

## 📋 Scripts principaux

### **1. build_distribution.py** (Racine)
- **Fonction** : Lanceur principal pour la création de distribution
- **Utilisation** : `python build_distribution.py`
- **Résultat** : Lance le script de distribution avec interface utilisateur

### **2. scripts/create_distribution.py**
- **Fonction** : Création de packages de distribution
- **Options** :
  - Package pip (installation système)
  - Archive portable (exécutable autonome)
  - Distribution complète (les deux)
- **Résultat** : Fichiers prêts à distribuer

### **3. scripts/build_portable.py**
- **Fonction** : Construction d'exécutable portable avec PyInstaller
- **Mode** : `--onedir` pour démarrage rapide
- **Résultat** : Dossier `dist/lcpi/` avec exécutable

### **4. scripts/install_portable.py**
- **Fonction** : Installation avec choix entre portable et système
- **Options** : Installation système ou version portable
- **Résultat** : LCPI installé selon le choix

## 🔧 Scripts utilitaires

### **Scripts PowerShell**
- `setup_lcpi_final.ps1` : Configuration finale avec alias permanent
- `setup_lcpi_absolute.ps1` : Configuration avec chemins absolus
- `install_lcpi.ps1` : Installation simple
- `setup_lcpi_path.ps1` : Configuration du PATH

### **Scripts Batch**
- `build_lcpi.bat` : Construction portable (version batch)
- `lcpi.bat` : Lanceur LCPI pour Windows

## 🧪 Tests et démonstrations

### **Tests principaux**
- `test_cli.py` : Tests de l'interface CLI
- `test_logging_system.py` : Tests du système de logs
- `test_validation_system.py` : Tests de validation
- `test_new_project_system.py` : Tests de création de projets

### **Démonstrations**
- `demo_phase4.py` : Démonstration des fonctionnalités Phase 4
- `debug_session.py` : Débogage des sessions

## 📝 Notes importantes

1. **Chemins relatifs** : Tous les scripts utilisent des chemins relatifs au projet
2. **Dépendances** : Les scripts nécessitent Python et les dépendances installées
3. **Permissions** : Les scripts PowerShell peuvent nécessiter des permissions d'exécution
4. **Environnement** : Assurez-vous d'être dans l'environnement virtuel approprié

## 🚨 Dépannage

### **Script non trouvé**
```bash
# Vérifier que le script existe
ls scripts/create_distribution.py

# Vérifier les permissions
chmod +x scripts/*.py
```

### **Erreur de chemin**
```bash
# Vérifier la structure
tree scripts/
tree tests/
```

### **Erreur PyInstaller**
```bash
# Installer PyInstaller
pip install pyinstaller

# Vérifier la version
pyinstaller --version
```
