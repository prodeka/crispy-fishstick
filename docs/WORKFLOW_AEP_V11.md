## Workflow AEP V11 (INP → Optimisation → Rapport)

### 0) Pré-requis
- Python/venv activé et dépendances installées
- Base de prix SQLite: `src/lcpi/db/aep_prices.db`
- Fichier réseau EPANET `.inp` valide (ex.: `src/lcpi/aep/PROTOTYPE/INP/bismark-Administrator.inp`)
- Optionnel: matériau par défaut via variable d’environnement
```
# Windows PowerShell
$env:AEP_MATERIAL = "PVC-U"
```

### 1) Aide CLI (vérification rapide)
```
python -m lcpi.aep.cli optimizer --help
```

Vous devez voir les sous-commandes: `price-optimize`, `report`, `diameters-manage`.

### 2) Optimisation (nested) depuis un fichier INP
- Le parseur interne lit minimalement la section `[PIPES]` (ID, noeuds, longueur)
- Les coûts (tuyaux + accessoires) sont pris depuis `aep_prices.db`

Commande:
```
python -m lcpi.aep.cli optimizer price-optimize \
  C:\PROJET_DIMENTIONEMENT_2\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp \
  --method nested \
  --lambda-opex 0.5 \
  --output C:\PROJET_DIMENTIONEMENT_2\results\opt_v11.json
```

Sorties produites:
- JSON V11: `results/opt_v11.json`
- Log compatible `lcpi rapport`: `results/opt_v11.log.json`

### 3) Rapport HTML (template V11)
```
python -m lcpi.aep.cli optimizer report \
  C:\PROJET_DIMENTIONEMENT_2\results\opt_v11.json \
  --template optimisation_tank_v11.jinja2 \
  --output C:\PROJET_DIMENTIONEMENT_2\results\rapport_aep.html
```

Sortie:
- HTML: `results/rapport_aep.html`

### 4) Variantes (au besoin)
- Changer le matériau global: `AEP_MATERIAL` (défaut `PVC-U`)
- Autres méthodes (si disponibles/configurées): `--method global`, `--method surrogate`

### 5) Diagnostics rapides
- Vérifier la DB prix:
```
python - <<PY
import sqlite3, pathlib
p = pathlib.Path('src/lcpi/db/aep_prices.db')
con = sqlite3.connect(p)
cur = con.cursor(); cur.execute('select count(*) from diameters'); print('diameters=', cur.fetchone()[0])
cur.execute('select count(*) from accessories'); print('accessories=', cur.fetchone()[0])
con.close()
PY
```

### 6) Notes d’implémentation utiles
- `AEP_MATERIAL` pilote la lecture des prix (diamètres/accessoires) via le DAO
- Le scoring CAPEX interroge la DB si aucun mapping n’est injecté
- Les accessoires par conduite peuvent être fournis via `links[link_id]['accessories']` (code, dn_mm, qty)


### 7) Workflow A → Z (vérification → calcul → rapport)

1. Vérifier l’environnement
   - Activer le venv, installer les deps, définir le matériau si besoin:
   ```
   # PowerShell
   $env:AEP_MATERIAL = "PVC-U"
   ```
   - Contrôler la DB prix:
   ```
   python - <<PY
   import sqlite3, pathlib
   p = pathlib.Path('src/lcpi/db/aep_prices.db')
   con = sqlite3.connect(p)
   cur = con.cursor()
   print('diameters=', cur.execute('select count(*) from diameters').fetchone()[0])
   print('accessories=', cur.execute('select count(*) from accessories').fetchone()[0])
   con.close()
   PY
   ```

2. Vérifier la CLI
   ```
   python -m lcpi.aep.cli optimizer --help
   ```

3. (Optionnel) Audit rapide intégré
   ```
   python tools/run_audit_v13.py
   # Produit docs/AUDIT_V13_REPORT.md et un JSON de statut en stdout
   ```

4. Lancer l’optimisation (nested)
   - Lit minimalement `[PIPES]` du fichier `.inp` (ID, noeuds, longueur)
   - Utilise les prix de `aep_prices.db` (tuyaux + accessoires)
   ```
   python -m lcpi.aep.cli optimizer price-optimize \
     C:\PROJET_DIMENTIONEMENT_2\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp \
     --method nested \
     --lambda-opex 0.5 \
     --output C:\PROJET_DIMENTIONEMENT_2\results\opt_v11.json
   ```

5. Générer le rapport HTML AEP V11
   ```
   python -m lcpi.aep.cli optimizer report \
     C:\PROJET_DIMENTIONEMENT_2\results\opt_v11.json \
     --template optimisation_tank_v11.jinja2 \
     --output C:\PROJET_DIMENTIONEMENT_2\results\rapport_aep.html
   ```

6. (Optionnel) Rapport via `lcpi rapport`
   - Un log compatible est déjà produit: `results/opt_v11.log.json`
   - Utiliser ensuite la commande `lcpi rapport generate ...` (si disponible) pour documents globaux.

7. Post-vérifications
   - Ouvrir `results/rapport_aep.html`
   - Vérifier `results/opt_v11.json` (structure V11) et `results/opt_v11.log.json`


### 8) Options avancées

- Matériau: `AEP_MATERIAL` (ex.: `PVC-U`, `PEHD`)
- Global Optimizer (si `pymoo` installé):
  ```
  python -m lcpi.aep.cli optimizer price-optimize \
    C:\path\to\network.inp \
    --method global \
    --lambda-opex 1.0 \
    --output C:\path\to\results\opt_global_v11.json
  ```
  - Supporte la parallélisation et checkpoints (voir `GlobalOptimizer`)

- Gestion des diamètres:
  ```
  python -m lcpi.aep.cli optimizer diameters-manage --help
  # Exemple (lecture)
  python -m lcpi.aep.cli optimizer diameters-manage --db src/lcpi/db/aep_prices.db --action list
  ```


### 9) Dépannage (troubleshooting)

- EPANET/wntr
  - Le wrapper sélectionne automatiquement `EpanetSimulator`/`WNTRSimulator` disponibles.
  - En cas d’échec API, fallback contrôlé + messages d’erreurs robustes.

- Fichier INP
  - Le parseur minimal lit `[PIPES]`. Assurez-vous que la section existe et est correctement formatée.

- Affichage CLI Windows
  - Les libellés utilisent "lambda" au lieu du caractère spécial "λ" pour compatibilité consoles Windows.


