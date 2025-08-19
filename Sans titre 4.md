## 1) Workflow global — de la feuille de prix au résultat optimisé

1. **Extraire** les tableaux du PDF bordereau → CSV(s).
    
2. **Nettoyer / normaliser** les colonnes (codes, unités, prix, matériel, DN/DNMM, remarques).
    
3. **Importer** les tableaux propres dans une base SQLite centralisée `aep_prices.db`.
    
4. **Exposer** un DAO Python (ex : `optimizer/db.py`) qui retourne `cost_per_m(d_mm, material)` et `unit_price(item_code)` et gère conversions d’unités.
    
5. **Appeler** le DAO depuis `scoring.compute_capex(...)` dans LCPI : CAPEX = Σ length * cost_per_m(d). Pour postes non-linéaires (fourniture + pose) utiliser `unit_price * qty`.
    
6. **Lancer optimisation** (nested/global/surrogate) : chaque candidat -> simulateur (EPANET ou LCPI) -> OPEX calc -> score = CAPEX + λ·OPEX_NPV.
    
7. **Sélectionner** les deux propositions (min CAPEX et knee/compromis).
    
8. **Générer rapport** (JSON + simulation files + template Jinja2 pour `lcpi rapport`).
