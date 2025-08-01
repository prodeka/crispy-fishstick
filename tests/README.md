# Tests Automatisés LCPI-CLI

Ce répertoire contient les tests automatisés pour vérifier le bon fonctionnement de l'affichage automatique des paramètres d'entrée des commandes CLI.

## 📁 Structure des Tests

```
tests/
├── README.md                    # Ce fichier
├── test_command_helpers.py      # Tests des utilitaires de commandes
├── test_cli_commands.py         # Tests des commandes CLI
└── __init__.py                  # Fichier d'initialisation Python
```

## 🧪 Types de Tests

### 1. Tests Unitaires (`test_command_helpers.py`)

Testent les fonctions utilitaires dans `src/lcpi/utils/command_helpers.py` :

- `create_parameter_dict()` : Création de dictionnaires de paramètres
- `check_required_params()` : Vérification des paramètres requis
- `create_typer_option()` : Création d'options Typer
- `show_input_parameters()` : Affichage des paramètres d'entrée

### 2. Tests d'Intégration CLI (`test_cli_commands.py`)

Testent que toutes les commandes CLI affichent correctement leurs paramètres d'entrée :

- **Module CM** : `check-poteau`, `check-deversement`, `check-tendu`, etc.
- **Module BOIS** : `check-poteau`, `check-deversement`, `check-cisaillement`, etc.
- **Module BETON** : `calc-poteau`, `calc-radier`
- **Module HYDRODRAIN** : `plomberie dimensionner`, `reservoir equilibrage`, etc.

## 🚀 Exécution des Tests

### Option 1 : Script Principal (Recommandé)

```bash
python run_tests.py
```

Ce script exécute :
- Tous les tests unitaires
- Tous les tests d'intégration CLI
- Des tests rapides de validation

### Option 2 : Tests Individuels

```bash
# Tests des utilitaires
pytest tests/test_command_helpers.py -v

# Tests des commandes CLI
pytest tests/test_cli_commands.py -v

# Tests spécifiques
pytest tests/test_cli_commands.py::TestCLICommandsParameterDisplay::test_cm_check_poteau_no_args -v
```

### Option 3 : Tests par Module

```bash
# Tests rapides (sans les tests CLI lents)
pytest tests/ -m "not slow" -v

# Tests CLI uniquement
pytest tests/ -m cli -v

# Tests unitaires uniquement
pytest tests/ -m unit -v
```

## 📊 Validation des Tests

### Tests Réussis ✅

Un test est considéré comme réussi si :

1. **Tests Unitaires** : Toutes les assertions passent
2. **Tests CLI** : 
   - La commande retourne un code de sortie 0
   - La sortie contient "Paramètres d'entrée"
   - La sortie contient les paramètres attendus
   - La sortie contient les exemples d'utilisation

### Exemple de Sortie Attendue

```
╭─────────────────────── Paramètres d'entrée - Vérification Poteau (Construction Métallique) ───────────────────────╮
│ Paramètres d'entrée pour Vérification Poteau (Construction Métallique) :                                          │
│                                                                                                                   │
│ Vérifie un poteau en compression/flambement selon les normes FORMATEC.                                            │
│                                                                                                                   │
│ Paramètres obligatoires :                                                                                         │
│ • --filepath (-f) : Chemin vers le fichier YAML de définition du poteau                                           │
│                                                                                                                   │
│ Exemple d'utilisation :                                                                                           │
│ lcpi cm check-poteau --filepath poteau_exemple.yml                                                                │
│ lcpi cm check-poteau -f poteau_exemple.yml                                                                        │
│                                                                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## 🔧 Dépannage

### Problèmes Courants

1. **ModuleNotFoundError** : Assurez-vous d'être dans le répertoire racine du projet
2. **Timeout** : Certains tests CLI peuvent prendre du temps, augmentez le timeout si nécessaire
3. **Erreurs de licence** : Vérifiez que la licence LCPI est valide

### Debug des Tests

```bash
# Mode verbose avec plus de détails
pytest tests/ -v -s

# Afficher les erreurs complètes
pytest tests/ --tb=long

# Exécuter un test spécifique avec debug
pytest tests/test_cli_commands.py::TestCLICommandsParameterDisplay::test_cm_check_poteau_no_args -v -s
```

## 📝 Ajout de Nouveaux Tests

### Pour une Nouvelle Commande CLI

1. Ajoutez un test dans `test_cli_commands.py` :

```python
def test_nouvelle_commande_no_args(self):
    """Test de la nouvelle commande sans arguments."""
    stdout, stderr, returncode = self.run_lcpi_command(["module", "nouvelle-commande"])
    
    assert returncode == 0
    assert "Paramètres d'entrée - Nom de la Commande" in stdout
    assert "--parametre (-p)" in stdout
    assert "Description du paramètre" in stdout
```

2. Ajoutez le test dans `run_tests.py` si nécessaire

### Pour de Nouvelles Fonctions Utilitaires

1. Ajoutez un test dans `test_command_helpers.py` :

```python
def test_nouvelle_fonction(self):
    """Test de la nouvelle fonction utilitaire."""
    result = nouvelle_fonction(param1, param2)
    assert result == valeur_attendue
```

## 🎯 Objectifs des Tests

- ✅ Vérifier que toutes les commandes affichent leurs paramètres d'entrée
- ✅ S'assurer que les commandes fonctionnent toujours avec des arguments
- ✅ Valider le bon fonctionnement des utilitaires
- ✅ Détecter les régressions lors des modifications
- ✅ Faciliter le développement et la maintenance

## 📈 Métriques

Les tests couvrent actuellement :

- **8 commandes CM** (Construction Métallique)
- **10 commandes BOIS**
- **2 commandes BETON**
- **8 commandes HYDRODRAIN**
- **4 fonctions utilitaires**

**Total : 32 tests d'intégration + tests unitaires** 