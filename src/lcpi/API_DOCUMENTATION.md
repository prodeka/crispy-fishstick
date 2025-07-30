# Documentation API LCPI Platform

## Vue d'ensemble des API

La plateforme LCPI expose plusieurs interfaces de programmation :

1. **API CLI** : Interface en ligne de commande via Typer
2. **API Python** : Import direct des modules
3. **API Web** : Interface HTTP (ex: Flask/FastAPI)
4. **API JSON** : Échange de données structurées

---

## 1. API CLI

### Lancement

```bash
lcpi [COMMANDES] [OPTIONS]
```

### Exemples

```bash
lcpi hydro util prevoir-population --method arithmetique --annee 2030
lcpi hydro ouvrage canal-dimensionner canal_exemple.yml
lcpi report --output pdf
```

### Commandes du noyau

- `init`, `plugins`, `config`, `report`, `doctor`, `shell`

---

## 2. API Python

### Import des modules

```python
from lcpi.hydrodrain.calculs.population import prevoir_population
result = prevoir_population({...})
```

---

## 3. API Web (exemple)

```python
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    # Appel à la logique LCPI
    from lcpi.hydrodrain.calculs.population import prevoir_population
    result = prevoir_population(data)
    return jsonify(result)
``` 