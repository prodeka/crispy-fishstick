# Guide d'Utilisation LCPI Platform

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
# Installation depuis le répertoire racine du projet
pip install -r requirements.txt

# Ou installation manuelle des dépendances principales
pip install typer rich pandas pyyaml reportlab numpy matplotlib
```

### Vérification de l'installation

```bash
# Test de l'installation
python -m lcpi_platform.lcpi_core.main --help
```

## Utilisation de base

### 1. Construction Métallique

#### Calcul d'une poutre simple

**Fichier d'entrée :** `elements/poutre_simple.yml`
```yaml
longueur: 6.0
nuance: S235
fy_MPa: 235.0
E_MPa: 210000.0
famille_profil: IPE
charges:
  permanentes_G:
    - type: repartie
      valeur: 5.0
      description: "Poids propre + revêtements"
  exploitation_Q:
    - type: repartie
      valeur: 3.0
      description: "Charge d'exploitation"
```

**Commande :**
```bash
python -m lcpi_platform.lcpi_core.main cm calc elements/poutre_simple.yml
```

**Résultat attendu :**
```
--- Calcul de poutre en acier ---
Longueur: 6.0 m
Charges: [{'type': 'repartie', 'valeur': 5.0, 'categorie': 'G'}, {'type': 'repartie', 'valeur': 3.0, 'categorie': 'Q'}]

Sollicitations calculées:
- M_Ed: 45.2 kN.m
- V_Ed: 24.8 kN
- p_ser: 8.0 kN/m

Profil recommandé: IPE200
Vérifications:
✓ Résistance en flexion: OK
✓ Résistance en cisaillement: OK
✓ Déformation: OK
✓ Déversement: OK
```

#### Traitement par lot

**Fichier CSV d'entrée :** `data/poutres_batch.csv`
```csv
longueur_m,charge_G_kn_m,charge_Q_kn_m,nuance,fy_MPa,E_MPa,famille_profil
6.0,5.0,3.0,S235,235.0,210000.0,IPE
8.0,6.0,4.0,S355,355.0,210000.0,HEA
10.0,7.0,5.0,S235,235.0,210000.0,IPE
```

**Commande :**
```bash
python -m lcpi_platform.lcpi_core.main cm calc --batch-file data/poutres_batch.csv --output-file resultats_poutres.csv
```

#### Mode interactif

```bash
python -m lcpi_platform.lcpi_core.main cm interactive
```

### 2. Construction Bois

#### Vérification d'un élément bois

**Fichier d'entrée :** `elements/panne_toiture.yml`
```yaml
longueur: 4.0
classe_bois: C24
categorie_usage: A
section:
  largeur: 0.08
  hauteur: 0.20
charges:
  permanentes_G:
    - type: repartie
      valeur: 2.0
      description: "Poids propre + couverture"
  exploitation_Q:
    - type: repartie
      valeur: 1.5
      description: "Charge d'exploitation"
```

**Commande :**
```bash
python -m lcpi_platform.lcpi_core.main bois check elements/panne_toiture.yml
```

**Résultat attendu :**
```
--- Vérification d'élément en bois ---
Classe de bois: C24
Catégorie d'usage: A
Section: 80x200 mm

Sollicitations:
- M_Ed: 8.0 kN.m
- V_Ed: 7.0 kN

Vérifications selon Eurocode 5:
✓ Résistance en flexion: OK (σ_m,d = 15.6 MPa ≤ f_m,d = 16.6 MPa)
✓ Résistance en cisaillement: OK (τ_d = 0.66 MPa ≤ f_v,d = 2.5 MPa)
✓ Déformation: OK (δ = 12.3 mm ≤ L/300 = 13.3 mm)
✓ Stabilité au déversement: OK
```

### 3. Béton Armé

#### Calcul d'une poutre en béton armé

**Fichier d'entrée :** `elements/poutre_ba.yml`
```yaml
longueur: 5.0
section:
  largeur: 0.25
  hauteur: 0.50
materiaux:
  beton: C25/30
  acier: B500B
charges:
  permanentes_G:
    - type: repartie
      valeur: 12.5
  exploitation_Q:
    - type: repartie
      valeur: 8.0
```

**Commande :**
```bash
python -m lcpi_platform.lcpi_core.main beton calc elements/poutre_ba.yml
```

### 4. Hydraulique

#### Dimensionnement d'un réseau d'assainissement

**Fichier d'entrée :** `data/projet_assainissement.yml`
```yaml
reseau:
  type: "assainissement_gravitaire"
  pente_min: 0.5
  pente_max: 5.0
  rugosite: 1.5
  diametres_disponibles: [150, 200, 250, 300, 400]

troncons:
  - nom: "T1"
    longueur: 50.0
    pente: 2.0
    surface_versante: 0.5
    coefficient_ruissellement: 0.8
    periode_retour: 10
```

**Commande :**
```bash
python -m lcpi_platform.lcpi_core.main hydro calc data/projet_assainissement.yml
```

## Formats de sortie

### 1. Sortie standard (console)

```
--- Résultats du calcul ---
Statut: OK
Profil recommandé: IPE200
Moment de calcul: 45.2 kN.m
Effort tranchant: 24.8 kN
Charge de service: 8.0 kN/m
```

### 2. Format JSON

```bash
python -m lcpi_platform.lcpi_core.main cm calc elements/poutre.yml --json
```

**Résultat :**
```json
{
  "statut": "OK",
  "profil_recommande": "IPE200",
  "M_Ed": 45.2,
  "V_Ed": 24.8,
  "p_ser": 8.0,
  "verifications": {
    "flexion": "OK",
    "cisaillement": "OK",
    "deformation": "OK",
    "deversement": "OK"
  },
  "proprietes_profil": {
    "W_el": 194.0,
    "I": 1940.0,
    "A": 28.5
  }
}
```

### 3. Rapport PDF

```bash
python -m lcpi_platform.lcpi_core.main report .
```

Génère un fichier `rapport_lcpi.pdf` contenant tous les résultats.

## Exemples pratiques

### Exemple 1 : Poutre de plancher

**Contexte :** Poutre de plancher en acier pour un bâtiment de bureaux.

**Fichier :** `elements/poutre_plancher.yml`
```yaml
longueur: 7.5
nuance: S355
fy_MPa: 355.0
E_MPa: 210000.0
famille_profil: IPE
charges:
  permanentes_G:
    - type: repartie
      valeur: 8.0
      description: "Poids propre + dalle + revêtements"
  exploitation_Q:
    - type: repartie
      valeur: 5.0
      description: "Charge d'exploitation bureaux"
    - type: ponctuelle
      valeur: 15.0
      position: 3.75
      description: "Équipement lourd"
```

### Exemple 2 : Panne de toiture

**Contexte :** Panne de toiture en bois pour un hangar agricole.

**Fichier :** `elements/panne_hangar.yml`
```yaml
longueur: 5.0
classe_bois: C30
categorie_usage: B
section:
  largeur: 0.10
  hauteur: 0.25
charges:
  permanentes_G:
    - type: repartie
      valeur: 3.5
      description: "Poids propre + couverture"
  exploitation_Q:
    - type: repartie
      valeur: 2.0
      description: "Charge d'exploitation"
  neige_S:
    - type: repartie
      valeur: 4.0
      description: "Charge de neige"
```

### Exemple 3 : Réseau d'assainissement

**Contexte :** Dimensionnement d'un réseau d'assainissement pour un lotissement.

**Fichier :** `data/lotissement_assainissement.yml`
```yaml
projet:
  nom: "Lotissement Les Jardins"
  surface_totale: 2.5
  coefficient_ruissellement: 0.7
  periode_retour: 10

reseau:
  type: "assainissement_gravitaire"
  pente_min: 0.5
  pente_max: 3.0
  rugosite: 1.5
  diametres_disponibles: [200, 250, 300, 400, 500]

troncons:
  - nom: "Collecteur principal"
    longueur: 120.0
    pente: 1.5
    surface_versante: 2.5
  - nom: "Branchement 1"
    longueur: 25.0
    pente: 2.0
    surface_versante: 0.3
  - nom: "Branchement 2"
    longueur: 25.0
    pente: 2.0
    surface_versante: 0.3
```

## Dépannage

### Problèmes courants

#### 1. Erreur de module non trouvé

**Symptôme :**
```
ModuleNotFoundError: No module named 'lcpi_platform'
```

**Solution :**
```bash
# Vérifier que vous êtes dans le bon répertoire
cd /chemin/vers/PROJET_DIMENTIONEMENT_2

# Ajouter le répertoire au PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 2. Erreur de dépendance manquante

**Symptôme :**
```
ImportError: No module named 'typer'
```

**Solution :**
```bash
pip install typer rich pandas pyyaml reportlab
```

#### 3. Erreur de fichier YAML invalide

**Symptôme :**
```
yaml.YAMLError: mapping values are not allowed here
```

**Solution :**
- Vérifier la syntaxe YAML
- Utiliser un validateur YAML en ligne
- Vérifier l'indentation (espaces, pas de tabulations)

#### 4. Erreur de calcul

**Symptôme :**
```
ValueError: La longueur doit être positive
```

**Solution :**
- Vérifier les valeurs d'entrée
- S'assurer que toutes les données requises sont présentes
- Vérifier les unités (mètres, kN, etc.)

### Mode debug

```bash
# Activer le mode verbeux
python -m lcpi_platform.lcpi_core.main cm calc elements/poutre.yml --verbose

# Afficher les détails de calcul
python -m lcpi_platform.lcpi_core.main cm calc elements/poutre.yml --debug
```

## Bonnes pratiques

### 1. Organisation des fichiers

```
projet/
├── elements/           # Fichiers YAML des éléments
│   ├── poutres/
│   ├── pannes/
│   └── reseaux/
├── data/              # Données d'entrée CSV
├── resultats/         # Fichiers de sortie
└── rapports/          # Rapports PDF
```

### 2. Nommage des fichiers

- **Éléments :** `type_nom.yml` (ex: `poutre_plancher.yml`)
- **Données :** `source_description.csv` (ex: `poutres_batch.csv`)
- **Résultats :** `calcul_date.csv` (ex: `resultats_20241201.csv`)

### 3. Validation des données

- Vérifier les unités avant calcul
- Valider les plages de valeurs
- Tester avec des cas simples d'abord

### 4. Documentation des calculs

- Commenter les fichiers YAML
- Documenter les hypothèses
- Garder une trace des modifications

## Intégration avec d'autres outils

### 1. Export vers Excel

```python
import pandas as pd

# Lire les résultats CSV
df = pd.read_csv('resultats_poutres.csv')

# Exporter vers Excel
df.to_excel('resultats_poutres.xlsx', index=False)
```

### 2. Intégration avec AutoCAD

```python
# Générer un script AutoLISP
def generate_autocad_script(results):
    script = ""
    for result in results:
        script += f"(command \"_line\" \"0,0\" \"{result['longueur']},0\")\n"
    return script
```

### 3. Interface web

```python
# Utiliser Flask pour créer une API web
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    # Appeler LCPI Platform
    result = subprocess.run([
        'python', '-m', 'lcpi_platform.lcpi_core.main',
        'cm', 'calc', data['filepath'], '--json'
    ], capture_output=True, text=True)
    return jsonify(result.json())
```

## Support et assistance

### 1. Documentation

- **README.md** : Vue d'ensemble
- **DOCUMENTATION_TECHNIQUE.md** : Détails techniques
- **GUIDE_UTILISATION.md** : Ce guide

### 2. Exemples

- **elements/** : Fichiers d'exemples pour chaque module
- **data/** : Données d'exemple
- **tests/** : Tests unitaires et d'intégration

### 3. Logs et debugging

```bash
# Activer les logs détaillés
export LCPI_LOG_LEVEL=DEBUG

# Voir les logs
python -m lcpi_platform.lcpi_core.main cm calc elements/poutre.yml 2>&1 | tee calcul.log
```

Ce guide d'utilisation fournit toutes les informations nécessaires pour utiliser efficacement la plateforme LCPI. 