Très bien — voici un plan pratique, priorisé et reproductible pour obtenir un **résultat complet** et avancer rapidement. Je fournis commandes PowerShell, petits scripts Python utiles, et les actions à faire (avec ce que tu dois vérifier / partager ensuite si tu veux que je continue).

---

# Résumé de la situation actuelle (rapide)

- `meta.best_cost` ok et cohérent avec `proposals[0].CAPEX`.
    
- `solver_calls` > 0 et `sim_time_seconds_total` non nul → les simulateurs sont appelés.
    
- **Problèmes à régler / vérifier** :
    
    1. violation de conservation de débit (total ≈ -1.202 m³/s) → **danger hydraulique / parsing**.
        
    2. tous les diamètres identiques (unique=[315]) → PriceDB absent / réparation trop agressive.
        
    3. génération PDF échoue (backends manquants).
        

---

# Objectif immédiat

Obtenir un run « complet & propre » + extraire diagnostics hydrauliques et la provenance des diamètres pour pouvoir :

1. valider masse/équilibre des débits,
    
2. confirmer origine des diamètres (PriceDB vs réparation),
    
3. regénérer PDF/HTML si besoin.
    

---

# Étapes recommandées (exécutables, pas à pas)

## A — Rendre la commande reproductible et capturer tout

Exécute la commande avec logs complets (PowerShell) — utilise `--no-cache --no-surrogate --verbose` (tu l'as déjà fait). Exemple (adapté) :

```powershell
$env:PYTHONIOENCODING='utf-8'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
.\venv_new\Scripts\python.exe -m lcpi.aep.cli network-optimize-unified `
  .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp `
  --method genetic --solver epanet --generations 10 --population 20 `
  --pression-min 0 --vitesse-max 5 --hmax 50 --no-cache --no-surrogate `
  --verbose --show-stats --output .\results\test_integrated_stats.json `
  --report pdf --report-output .\results
```

Vérifie que `test_integrated_stats.json` et le log (chemin indiqué) sont présents.

---

## B — Activer PDF de façon simple (wkhtmltopdf portable)

WeasyPrint sous Windows requiert GTK (lourd). + simple : installer `wkhtmltopdf` portable et l'ajouter temporairement au PATH.

1. Télécharger wkhtmltopdf portable (ex. x64 Windows) depuis [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html) → extraire `bin\wkhtmltopdf.exe`.
    
2. Dans PowerShell (le dossier où tu as `wkhtmltopdf.exe`), lancer la commande d’exécution en préfixant le PATH :
    

```powershell
$wk = "C:\chemin\vers\wkhtmltopdf\bin"
$env:Path = "$wk;$env:Path"
# relancer la commande d'optimisation (ex. la commande ci-dessus)
```

Si tu préfères, je peux te donner un script PowerShell pour télécharger et placer le binaire dans `.\vendor\wkhtmltopdf` et ajouter au PATH.

---

## C — Vérifications rapides sur le JSON (scripts utilitaires)

Exécute ces petites vérifications Python (creuse infos utiles) :

1. Somme des flux, diamètres uniques, best cost, stats simulateur :
    

```python
# tools/quick_inspect.py
import json, sys
p = sys.argv[1]
d = json.load(open(p, encoding='utf-8'))
meta = d.get("meta", {})
props = d.get("proposals", [])
print("meta.best_cost:", meta.get("best_cost"))
print("simulator:", meta.get("simulator_used") or meta.get("simulator"))
print("solver_calls:", meta.get("solver_calls"))
print("sim_time_s_total:", meta.get("sim_time_seconds_total"))
# hydraulics
hyd = d.get("hydraulics", {})
flows = hyd.get("flows_m3_s") or {}
total = sum(float(v or 0.0) for v in flows.values()) if isinstance(flows, dict) else None
print("total_flow:", total)
# diameters
ds = []
for p in props:
    dd = p.get("diameters_mm") or {}
    ds.extend(list(dd.values()))
print("Diameters count:", len(ds), "unique:", sorted(set(ds)))
```

Commande :

```powershell
.\venv_new\Scripts\python.exe tools\quick_inspect.py results\test_integrated_stats.json
```

→ Post les résultats si tu veux que j’analyse.

---

## D — Diagnostiquer la conservation de masse (flow breach)

Souvent causes : sens défini arbitraire, conduites orientées, exports WNTR mal agrégés, unité signée, ou modification d'orientations par la réparation.

1. **Simuler un run unique** sur l’INP avec le simulateur EPANET (CLI déjà fourni) :
    

```powershell
.\venv_new\Scripts\python.exe -m lcpi.aep.cli simulate-inp .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --format json --output .\results\sim_one.json --verbose
```

2. Ouvrir `results\sim_one.json` et exécuter un script qui somme les `flows_m3_s` (comme ci-dessus). Compare `total_flow` entre `simulate-inp` et `optimisation` (hydraulics).
    
3. Si `simulate-inp` montre somme ≈ 0 mais l’optimisation non, alors la **modification des diamètres** faite par l’optimiseur/reparation produit l’erreur. Sinon, le parsing initial de l’INP (ordre/orientation) est suspect.
    
4. Pour isoler, choisis un petit sous-ensemble de conduites (10 premières) et simule uniquement en construisant un .inp temporaire (ou utiliser WNTR API) pour vérifier sens/valeurs.
    

Je peux te fournir un script WNTR rapide pour lire l’INP et calculer `sum(flows)` si tu veux.

---

## E — Contrôler d’où viennent les diamètres (PriceDB vs réparation automatique)

- Vérifie `meta.price_db_info` dans le JSON ; s’il pointe vers un fichier inexistant ou `version: unknown`, alors PriceDB n’a pas été utilisé.
    
- Si `meta.price_db_info` ok mais diamètres = constant (315), la logique `_ensure_at_least_one_feasible` a probablement remplacé toutes les tailles par un cran unique.
    

Commandes / snippet à exécuter :

```python
import json
d=json.load(open('results/test_integrated_stats.json',encoding='utf-8'))
print(d.get('meta',{}).get('price_db_info'))
for p in d.get('proposals',[]):
    print("proposal id", p.get('id'), "diam_count", len(p.get('diameters_mm',{})))
```

Si réparation appliquée, cherche le log `REPAIR_DIAMETERS_APPLIED` dans le fichier log JSON (chemin indiqué par la CLI). Ouvre le log et recherche cette clé.

---

## F — Re-run minimal et contrôlé (debug)

Pour tester comportement GA sans réparations agressives :

- Désactiver réparation automatique (si flag dispo) ou forcer no_repair via algo_params. Si tu n'as pas de flag, exécute en ajoutant `--generations 10 --population 20` et `algo_params`? (ex: `--algo-penalty-weight 0`? selon CLI). Si pas dispo, modifie temporairement `controllers._ensure_at_least_one_feasible` pour logger mais ne rien changer (je peux t'aider).
    

Commande test avec forcing backend DLL (si disponible) :

```powershell
.\venv_new\Scripts\python.exe -m lcpi.aep.cli network-optimize-unified .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --method genetic --solver epanet --generations 10 --population 20 --pression-min 0 --vitesse-max 5 --hmax 50 --no-cache --no-surrogate --verbose --epanet-backend dll --output .\results\test_epanet_dll.json
```

Comparer `test_epanet_dll.json` vs `test_integrated_stats.json` :

- change de `simulator_used`
    
- `total_flow`
    
- diamètres.
    

---

## G — Si tu veux que j’applique un correctif rapide

Je peux :

1. Ajouter un log détaillé avant/ après `_ensure_at_least_one_feasible` (dump diam map best avant/après).
    
2. Réduire l’agressivité de la réparation (ne pas appliquer un cran global à toutes les conduites — privilégier augmentation par secteur).
    
3. Produire un CSV `best_diameters.csv` pour examen.
    

Dis-moi si tu veux que je génère le patch (je te fournis le diff / script).

---

## H — Checklist pour toi (très pratique)

1.  Lancer la commande complète et capturer `results/test_integrated_stats.json` + `logs/...log.json`.
    
2.  Exécuter `tools/quick_inspect.py results/test_integrated_stats.json` et poster la sortie si tu veux que j’analyse.
    
3.  Lancer `simulate-inp` et comparer flux.
    
4.  Vérifier `meta.price_db_info` et le log `REPAIR_DIAMETERS_APPLIED`.
    
5.  Installer wkhtmltopdf (ou fournir binaire) si tu veux PDF ; relancer commande avec PATH mis à jour.
    
6.  Si diamètres uniformes, me dire si tu veux que je :
    
    - a) limite réparation (patch), ou
        
    - b) trace davantage (logs) pour voir quelles arêtes changées.
        

---

# Commandes utilitaires que je te recommande de lancer maintenant

### 1) Quick inspect JSON

```powershell
.\venv_new\Scripts\python.exe tools\quick_inspect.py results\test_integrated_stats.json
```

### 2) Simuler INP seul

```powershell
.\venv_new\Scripts\python.exe -m lcpi.aep.cli simulate-inp .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --format json --verbose --output .\results\sim_one.json
.\venv_new\Scripts\python.exe tools\quick_inspect.py .\results\sim_one.json
```

### 3) Re-run optimisation avec backend DLL (pour comparer)

```powershell
.\venv_new\Scripts\python.exe -m lcpi.aep.cli network-optimize-unified .\src\lcpi\aep\PROTOTYPE\INP\bismark-Administrator.inp --method genetic --solver epanet --generations 10 --population 20 --pression-min 0 --vitesse-max 5 --hmax 50 --no-cache --no-surrogate --verbose --epanet-backend dll --output .\results\test_epanet_dll.json
```

### 4) Lister logs pour trouver `REPAIR_DIAMETERS_APPLIED`

```powershell
Select-String -Path .\test_validation\logs\*.log.json -Pattern "REPAIR_DIAMETERS_APPLIED" -SimpleMatch
```

---

# Que j’attends de toi pour continuer (si tu veux que je bosse dessus)

1. Résultats du `tools/quick_inspect.py` (ou copie console).
    
2. Le fichier `simulate-inp` JSON (`results/sim_one.json`) si tu l’as.
    
3. Extrait des logs (le log JSON complet ou les lignes `REPAIR_DIAMETERS_APPLIED` et `FLOW_CONSERVATION_BREACH`).
    
4. Dis-moi si tu veux que je te génère le patch qui :
    
    - réduit agressivité de réparation,
        
    - ajoute dump avant/après réparation,
        
    - exporte `best_diameters.csv`.
        

Avec ces éléments je :

- propose un patch précis (diff) pour limiter la réparation et corriger l’origine des diamètres ;
    
- ou je t'explique exactement ce qu'il faut modifier côté PriceDB / fallback.
    

---

Tu veux que je :

- Génère le diff qui ajoute le dump `pre_repair` + `post_repair` et limite la réparation (patch small) ?
    
- Ou je te guide pour installer wkhtmltopdf automatiquement et relancer la génération PDF ?