# Documentation API LCPI Platform

## Vue d'ensemble des API

La plateforme LCPI expose plusieurs interfaces de programmation pour l'intégration avec d'autres systèmes :

1. **API CLI** : Interface en ligne de commande via Typer
2. **API Python** : Import direct des modules
3. **API Web** : Interface HTTP via Flask/FastAPI
4. **API JSON** : Échange de données structurées

## 1. API CLI

### Structure générale

```bash
python -m lcpi_platform.lcpi_core.main <module> <commande> [options]
```

### Modules disponibles

| Module | Commande | Description |
|--------|----------|-------------|
| `cm` | `calc` | Construction Métallique |
| `bois` | `check` | Construction Bois |
| `beton` | `calc` | Béton Armé |
| `hydro` | `calc` | Hydraulique |

### Options communes

```bash
--filepath <chemin>     # Fichier YAML d'entrée
--batch-file <chemin>   # Fichier CSV pour traitement par lot
--output-file <chemin>  # Fichier de sortie
--json                  # Sortie au format JSON
--verbose               # Mode verbeux
--help                  # Aide
```

### Exemples d'utilisation

```bash
# Calcul d'une poutre métallique
python -m lcpi_platform.lcpi_core.main cm calc elements/poutre.yml

# Vérification d'un élément bois
python -m lcpi_platform.lcpi_core.main bois check elements/panne.yml

# Traitement par lot
python -m lcpi_platform.lcpi_core.main cm calc --batch-file data/poutres.csv --output-file resultats.csv

# Sortie JSON
python -m lcpi_platform.lcpi_core.main cm calc elements/poutre.yml --json
```

## 2. API Python

### Import des modules

```python
# Import du module core
from lcpi_platform.lcpi_core import calculs, reporter

# Import des modules spécialisés
from lcpi_platform.lcpi_cm import calculs as cm_calculs
from lcpi_platform.lcpi_bois import calculs as bois_calculs
from lcpi_platform.lcpi_beton import ba_entry
from lcpi_platform.lcpi_hydrodrain import calculs as hydro_calculs
```

### API Core

#### Calculs de base

```python
from lcpi_platform.lcpi_core.calculs import calculer_sollicitations_completes

# Calcul des sollicitations
charges = [
    {'type': 'repartie', 'valeur': 5.0, 'categorie': 'G'},
    {'type': 'repartie', 'valeur': 3.0, 'categorie': 'Q'}
]

result = calculer_sollicitations_completes(
    longueur=6.0,
    charges_list=charges,
    materiau="acier",
    categorie_usage="A",
    verbose=True
)

print(f"M_Ed: {result['M_Ed']} kN.m")
print(f"V_Ed: {result['V_Ed']} kN")
print(f"p_ser: {result['p_ser']} kN/m")
```

#### Génération de rapports

```python
from lcpi_platform.lcpi_core.reporter import generate_pdf_report

# Liste de résultats
results = [
    {
        'element_id': 'poutre_1',
        'plugin': 'cm',
        'resultats': {
            'profil_recommande': 'IPE200',
            'M_Ed': 45.2,
            'V_Ed': 24.8
        }
    }
]

# Génération du rapport PDF
generate_pdf_report(results, "rapport.pdf")
```

### API Construction Métallique

```python
from lcpi_platform.lcpi_cm.calculs import trouver_profil_acier

# Dimensionnement d'un profil
profil = trouver_profil_acier(
    M_Ed=45.2,
    V_Ed=24.8,
    longueur=6.0,
    p_ser=8.0,
    famille_profil="IPE",
    nuance="S235",
    fy_MPa=235.0,
    E_MPa=210000.0
)

print(f"Profil recommandé: {profil['nom']}")
print(f"Vérifications: {profil['verifications']}")
```

### API Construction Bois

```python
from lcpi_platform.lcpi_bois.calculs import verifier_element_bois

# Vérification d'un élément bois
result = verifier_element_bois(
    longueur=4.0,
    classe_bois="C24",
    categorie_usage="A",
    charges_list=charges
)

print(f"Statut: {result['statut']}")
print(f"Vérifications: {result['verifications']}")
```

### API Béton Armé

```python
from lcpi_platform.lcpi_beton.ba_entry import BetonArmeCalculator

# Initialisation du calculateur
calc = BetonArmeCalculator()

# Calcul d'une poutre
data = {
    'longueur': 5.0,
    'section': {'largeur': 0.25, 'hauteur': 0.50},
    'materiaux': {'beton': 'C25/30', 'acier': 'B500B'},
    'charges': charges
}

result = calc.calculer_poutre(data)
print(f"Armatures: {result['armatures']}")
```

### API Hydraulique

```python
from lcpi_platform.lcpi_hydrodrain.calculs.assainissement_gravitaire import dimensionner_canalisation

# Dimensionnement d'une canalisation
result = dimensionner_canalisation(
    debit=15.0,
    pente=2.0,
    rugosite=1.5,
    diametres_disponibles=[150, 200, 250, 300]
)

print(f"Diamètre recommandé: {result['diametre']} mm")
print(f"Vitesse: {result['vitesse']} m/s")
```

## 3. API Web

### Interface Flask

```python
from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/api/cm/calc', methods=['POST'])
def calculate_steel_beam():
    """API pour le calcul de poutres métalliques."""
    data = request.json
    
    # Validation des données
    required_fields = ['longueur', 'charges', 'nuance']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Champ requis manquant: {field}'}), 400
    
    # Création du fichier YAML temporaire
    yaml_content = create_yaml_from_data(data)
    temp_file = f"/tmp/calc_{id(data)}.yml"
    
    with open(temp_file, 'w') as f:
        f.write(yaml_content)
    
    try:
        # Appel de LCPI Platform
        result = subprocess.run([
            'python', '-m', 'lcpi_platform.lcpi_core.main',
            'cm', 'calc', temp_file, '--json'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Parse du JSON de sortie
            json_start = result.stdout.find('{')
            if json_start != -1:
                output_json = result.stdout[json_start:]
                return jsonify(json.loads(output_json))
            else:
                return jsonify({'error': 'Format de sortie invalide'}), 500
        else:
            return jsonify({'error': result.stderr}), 500
            
    finally:
        # Nettoyage
        import os
        if os.path.exists(temp_file):
            os.remove(temp_file)

@app.route('/api/bois/check', methods=['POST'])
def check_wood_element():
    """API pour la vérification d'éléments bois."""
    # Implémentation similaire
    pass

@app.route('/api/beton/calc', methods=['POST'])
def calculate_concrete_beam():
    """API pour le calcul de poutres béton."""
    # Implémentation similaire
    pass

@app.route('/api/hydro/calc', methods=['POST'])
def calculate_hydraulic_network():
    """API pour les calculs hydrauliques."""
    # Implémentation similaire
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Interface FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import subprocess
import json

app = FastAPI(title="LCPI Platform API", version="1.0.0")

class Charge(BaseModel):
    type: str
    valeur: float
    categorie: str
    description: str = ""

class SteelBeamRequest(BaseModel):
    longueur: float
    nuance: str
    fy_MPa: float = 235.0
    E_MPa: float = 210000.0
    famille_profil: str = "IPE"
    charges: Dict[str, List[Charge]]

class SteelBeamResponse(BaseModel):
    statut: str
    profil_recommande: str
    M_Ed: float
    V_Ed: float
    p_ser: float
    verifications: Dict[str, str]

@app.post("/api/cm/calc", response_model=SteelBeamResponse)
async def calculate_steel_beam(request: SteelBeamRequest):
    """Calcule une poutre métallique."""
    
    # Conversion en YAML
    yaml_content = f"""
longueur: {request.longueur}
nuance: {request.nuance}
fy_MPa: {request.fy_MPa}
E_MPa: {request.E_MPa}
famille_profil: {request.famille_profil}
charges:
  permanentes_G:
"""
    
    for charge in request.charges.get('permanentes_G', []):
        yaml_content += f"    - type: {charge.type}\n"
        yaml_content += f"      valeur: {charge.valeur}\n"
        yaml_content += f"      description: \"{charge.description}\"\n"
    
    yaml_content += "  exploitation_Q:\n"
    for charge in request.charges.get('exploitation_Q', []):
        yaml_content += f"    - type: {charge.type}\n"
        yaml_content += f"      valeur: {charge.valeur}\n"
        yaml_content += f"      description: \"{charge.description}\"\n"
    
    # Écriture du fichier temporaire
    temp_file = f"/tmp/calc_{id(request)}.yml"
    with open(temp_file, 'w') as f:
        f.write(yaml_content)
    
    try:
        # Appel de LCPI Platform
        result = subprocess.run([
            'python', '-m', 'lcpi_platform.lcpi_core.main',
            'cm', 'calc', temp_file, '--json'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            json_start = result.stdout.find('{')
            if json_start != -1:
                output_json = result.stdout[json_start:]
                data = json.loads(output_json)
                return SteelBeamResponse(**data)
            else:
                raise HTTPException(status_code=500, detail="Format de sortie invalide")
        else:
            raise HTTPException(status_code=500, detail=result.stderr)
            
    finally:
        import os
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 4. API JSON

### Format d'entrée

```json
{
  "module": "cm",
  "action": "calc",
  "data": {
    "longueur": 6.0,
    "nuance": "S235",
    "fy_MPa": 235.0,
    "E_MPa": 210000.0,
    "famille_profil": "IPE",
    "charges": {
      "permanentes_G": [
        {
          "type": "repartie",
          "valeur": 5.0,
          "description": "Poids propre + revêtements"
        }
      ],
      "exploitation_Q": [
        {
          "type": "repartie",
          "valeur": 3.0,
          "description": "Charge d'exploitation"
        }
      ]
    }
  }
}
```

### Format de sortie

```json
{
  "statut": "OK",
  "module": "cm",
  "action": "calc",
  "resultats": {
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
  },
  "metadata": {
    "timestamp": "2024-12-01T10:30:00Z",
    "version": "1.0.0",
    "execution_time": 0.125
  }
}
```

## 5. Intégration avec d'autres langages

### JavaScript/Node.js

```javascript
const { spawn } = require('child_process');

function calculateSteelBeam(data) {
    return new Promise((resolve, reject) => {
        const process = spawn('python', [
            '-m', 'lcpi_platform.lcpi_core.main',
            'cm', 'calc', data.filepath, '--json'
        ]);
        
        let stdout = '';
        let stderr = '';
        
        process.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        process.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        process.on('close', (code) => {
            if (code === 0) {
                const jsonStart = stdout.indexOf('{');
                if (jsonStart !== -1) {
                    const jsonOutput = stdout.substring(jsonStart);
                    resolve(JSON.parse(jsonOutput));
                } else {
                    reject(new Error('Format de sortie invalide'));
                }
            } else {
                reject(new Error(stderr));
            }
        });
    });
}

// Utilisation
calculateSteelBeam({ filepath: 'elements/poutre.yml' })
    .then(result => console.log(result))
    .catch(error => console.error(error));
```

### Python avec requests

```python
import requests
import json

def call_lcpi_api(module, action, data):
    """Appelle l'API LCPI via HTTP."""
    url = f"http://localhost:8000/api/{module}/{action}"
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erreur API: {response.text}")

# Exemple d'utilisation
data = {
    "longueur": 6.0,
    "nuance": "S235",
    "charges": {
        "permanentes_G": [
            {"type": "repartie", "valeur": 5.0}
        ],
        "exploitation_Q": [
            {"type": "repartie", "valeur": 3.0}
        ]
    }
}

try:
    result = call_lcpi_api("cm", "calc", data)
    print(f"Profil recommandé: {result['profil_recommande']}")
except Exception as e:
    print(f"Erreur: {e}")
```

## 6. Gestion des erreurs

### Codes d'erreur

| Code | Description |
|------|-------------|
| 400 | Données d'entrée invalides |
| 404 | Module ou action non trouvé |
| 500 | Erreur interne du serveur |
| 503 | Service temporairement indisponible |

### Format d'erreur

```json
{
  "error": {
    "code": 400,
    "message": "Champ requis manquant: longueur",
    "details": {
      "missing_fields": ["longueur"],
      "provided_fields": ["nuance", "charges"]
    },
    "timestamp": "2024-12-01T10:30:00Z"
  }
}
```

## 7. Authentification et sécurité

### API Key

```python
from functools import wraps
from flask import request, jsonify

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != 'your-secret-key':
            return jsonify({'error': 'API key invalide'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/cm/calc', methods=['POST'])
@require_api_key
def calculate_steel_beam():
    # Logique de calcul
    pass
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/cm/calc', methods=['POST'])
@limiter.limit("10 per minute")
def calculate_steel_beam():
    # Logique de calcul
    pass
```

## 8. Tests des API

### Tests unitaires

```python
import pytest
from lcpi_platform.lcpi_core.calculs import calculer_sollicitations_completes

def test_calculer_sollicitations_completes():
    """Test du calcul des sollicitations."""
    charges = [{'type': 'repartie', 'valeur': 5.0, 'categorie': 'G'}]
    
    result = calculer_sollicitations_completes(
        longueur=6.0,
        charges_list=charges,
        materiau="acier",
        categorie_usage="A"
    )
    
    assert result["M_Ed"] == pytest.approx(22.5, rel=1e-2)
    assert result["V_Ed"] == pytest.approx(15.0, rel=1e-2)
    assert result["p_ser"] == pytest.approx(5.0, rel=1e-2)
```

### Tests d'intégration

```python
import requests
import json

def test_api_cm_calc():
    """Test de l'API Construction Métallique."""
    data = {
        "longueur": 6.0,
        "nuance": "S235",
        "charges": {
            "permanentes_G": [
                {"type": "repartie", "valeur": 5.0}
            ],
            "exploitation_Q": [
                {"type": "repartie", "valeur": 3.0}
            ]
        }
    }
    
    response = requests.post(
        "http://localhost:8000/api/cm/calc",
        json=data,
        headers={"X-API-Key": "test-key"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["statut"] == "OK"
    assert "profil_recommande" in result
```

Cette documentation API fournit toutes les informations nécessaires pour intégrer LCPI Platform dans d'autres systèmes. 