
### Feuille de route pour unifier simple + enhanced dans les commandes `*-unified`

- **Objectif**
  - Faire des `*-unified` des commandes “tout-en-un”: acceptent soit des paramètres inline, soit un fichier (`YAML/CSV`), et exposent un mode “enhanced” (transparence, diagnostics, exports).

### 1) Design commun (spécifications)
- **Options standard à ajouter aux `*-unified`**
  - `--input` (`Path`, optionnel): charge YAML/CSV si fourni.
  - `--mode` (`auto|simple|enhanced`, défaut: `auto`).
  - `--export` (`json|csv|markdown|yaml|html`, défaut: `json`).
  - `--output` (`Path`, optionnel): fichier de sortie si demandé.
  - `--verbose`: détails et transparence mathématique quand applicable.
- **Routage**
  - Si `--input` → charger fichier → `mode=enhanced` par défaut, sinon respecter `--mode`.
  - Si pas `--input` → construire dict depuis options inline → router selon `--mode`.
- **Contrats de sortie**
  - Structures de résultats homogènes: clés minimales communes (`valeurs`, `diagnostics`, `iterations` le cas échéant).
  - Export via une couche utilitaire commune.

### 2) Implémentation par commande (ordre recommandé)
- **`demand_unified`**
  - Ajouter options ci-dessus.
  - Routage:
    - simple: `src/lcpi/aep/calculations/demand_unified.py` (calc “rapide”).
    - enhanced: `PopulationCalculationsEnhanced.calculate_water_demand_enhanced`.
  - Exporteurs et `--output`.
- **`network_unified`**
  - Ajouts identiques.
  - Routage:
    - simple: `calculations/network_unified.dimension_network`.
    - enhanced: `NetworkCalculationsEnhanced.dimensionner_conduite` (+ comparaison si `--mode enhanced` et `--verbose`).
- **`reservoir_unified`**
  - Ajouts identiques.
  - Routage:
    - simple: `calculations/reservoir_unified.dimension_reservoir`.
    - enhanced: `ReservoirCalculationsEnhanced.dimension_reservoir_enhanced`.
- **`pumping_unified`**
  - Ajouts identiques.
  - Routage:
    - simple: `calculations/pumping_unified.dimension_pumping`.
    - enhanced: `PumpingCalculationsEnhanced.dimension_pumping_enhanced`.
- **`population_unified`**
  - Ajouts identiques.
  - Routage:
    - simple: `calculations/population_unified.calculate_population_projection`.
    - enhanced: `PopulationCalculationsEnhanced.calculate_population_projection_enhanced`.
- **Hardy-Cross**
  - Déjà “enhanced” pour `hardy_cross_csv`/`hardy_cross_yaml`. Optionnel: créer `hardy-cross-unified` (inline + `--input` + `--export`) enveloppant `HardyCrossEnhanced`.

### 3) Validation d’entrée (Phase 0)
- Implémenter (si non présents) commandes:
  - `validate-input`, `validate-population`, `validate-network` (schémas + messages lisibles).
- Réutiliser validateurs unifiés `..core.validators` quand disponibles.

### 4) Export et utilitaires
- Créer un module utilitaire d’export commun (JSON/CSV/Markdown/YAML/HTML).
- Garantir encodage UTF-8, gestion erreurs, messages clairs.

### 5) REPL
- Mettre à jour `src/lcpi/shell/main.py`:
  - Aide des commandes `aep` avec nouvelles options.
  - Pass-through des options `--input`, `--mode`, `--export`, `--output`, `--verbose`.
  - Optionnel: surfacer `aep autocomplete` pour l’auto‑complétion.

### 6) Documentation et aide CLI
- Mettre à jour docstrings de `*-unified`:
  - Exemples “inline” et “avec `--input`”.
  - Sections Arguments/Options formatées, exemples d’export.
- Mettre à jour `docs/workflows/aep_workflow.md`:
  - Clarifier que `*-unified` acceptent désormais YAML via `--input`.
  - Ajouter exemples par commande.
- Rappeler la Phase 0 (validation) en préambule.

### 7) Tests
- **Unitaires** pour chaque commande `*-unified`:
  - Inline vs `--input`, `mode=simple|enhanced`, `--export` tous formats.
- **Intégration**:
  - Scénarios complets avec fichiers d’exemple.
  - REPL: exécution `aep` avec options.
- Jeux d’échantillons: `data/` minimal (CSV/YAML) pour CI.

### 8) Compatibilité et migration
- Ne pas casser les commandes “simples”.
- Conserver l’interface actuelle des `*-unified` (options ajoutées = backward‑compatible).
- Versionner le changement dans `CHANGELOG`.


---

# 1) Axe Fonctionnel (expérience utilisateur & logiciel)

**Objectif :** rendre LCPI plus robuste, facile à utiliser, extensible et intégrable.

Principales améliorations

* **Validation d’entrée stricte** : schéma JSON Schema/cerberus pour le YAML, messages d’erreur compréhensibles, contrôle d’unités (L/j, m³/j).
* **Modes d’exécution** : `batch` (fichiers YAML), 
* **Outputs multiples** : CSV/Excel (feuilles séparées), PDF/Word (rapport auto), JSON (machine-readable), graphiques PNG/SVG.
* **Templates de rapport** : modèles LaTeX/Word avec sections préremplies (méthodologie, hypothèses, résultats, annexes) pour tout
* **Profiles / scénarios** : possibilité de stocker plusieurs scénarios (base, pessimiste, optimiste) dans un seul YAML et de comparer automatiquement.
* **Historique & versioning des calculs** : horodatage, hash du jeu d’entrée, numéro de version LCPI dans sortie pour tout les commande
* **Extensibilité / plugin** : architecture plugin pour nouvelles méthodes de dotation, nouveaux coefficients, modules sectoriels (irrigation, industries spécifiques).
Priorité : Validation, Outputs, Scénarios = **Haute**

---

# 2) Axe Métier / Ingénieur

**Objectif :** aligner l’outil sur les pratiques métier et les besoins opérationnels d’un ingénieur AEP.

Fonctionnalités métier

* **Bibliothèque d’unités/dotations** : jeu de dotations standard (OMS, normes nationales) et possibilité d’ajouter références locales.
* **Méthodes de pointe** : implémenter plusieurs méthodes (facteur de pointe journalier, courbe de charge horaire, coefficient K) et permettre comparaison.
* **Gestion pertes & rendement** : séparer pertes physiques (fuites) des pertes commerciales, inclure rendement réseau.
* **Analyse de sensibilité** : calculer variations des besoins selon +/-10% dotation, croissance démographique, fuite.
* **Phasage et planification** : sortie par horizon (2025/2030/2050) + besoins cumulés et capacité à phaser (ex : 1re phase 50%).
* **Compatibilité CAO/EPANET/WaterGEMS** : exporter demandes horaires/points de consommation pour simulation hydraulique.
* +
* **Calage sur mesures** : module d’ajustement/calibration qui compare calcul théorique vs. comptages réels et propose corrections.

Livrables métier

* Feuille Excel préparée pour études d’impact, table de calculs détaillés
* Fichiers d’import pour simulateurs hydrauliques

Priorité : Dotations, Méthodes pointe, Sensibilité, Export EPANET = **Haute**.

---

# 3) Axe Académique / Scientifique

**Objectif :** assurer reproductibilité, traçabilité, rigueur méthodologique et facilité de publication.

Exigences académique

* **Traçabilité** : pour chaque valeur, stocker provenance (source, date, commentaire). Exemple : `dotation.domestique.source: "norme X, 2019"`.
* **Formules explicites & annexes** : afficher pas-à-pas les formules utilisées et les unités en annexe du rapport.
* **Tests et cas d’étude** : jeux de données standards (cas de référence) et résultats attendus documentés.
* **Analyse d’incertitude** : Monte-Carlo ou simple intervalle de confiance sur paramètres clés.
* **Citations & bibliographie** : champ metadata pour insérer références (BibTeX) et les inclure dans le rapport LaTeX.

---

# 4) Proposition concrète : schéma YAML enrichi (exemple)

```yaml
meta:
  projet: "AEP Agbelouvé"
  auteur: "Nom Ingénieur"
  date: "2025-08-15"
  version_lcpi: "1.2.0"
  references:
    - id: "WHO2017"
      title: "Water supply standards 2017"
      note: "Valeurs recommandées pour zones rurales"

population:
  actuelle: 15000
  projection:
    "2030": 18000
    "2050": 22000
  repartition:   # facultatif
    menages: 3500
    moy_habitants_par_menage: 4.3

consommation:
  domestique:
    dotation_L_j_hab: 150
    source: "WHO2017"
  industriel:
    dotation_L_j_hab: 50
    source: "Enquête entreprise"
  commercial:
    dotation_L_j_hab: 30

coefficients:
  pointe:
    journaliere: 1.3
    horaire: 1.8
  fuites:
    fraction_physique: 0.10
    fraction_commerciale: 0.05

scenarios:
  base:
    population: "actuelle"
    consommation_multiplier: 1.0
  urbain_rapide:
    population: "2030"
    consommation_multiplier: 1.1
```



---

# 7) Monitoring, logs & traçabilité

* Logs structurés (JSON) avec niveau (INFO/WARN/ERROR).
* Archivage des jeux d’entrée + sortie (hash) pour audits.
* Dashboard basique (ou fichier résumé) listant KPI : DEM (m³/j), DEM pointe, fuite %, sensibilité clé.

Parfait — voici des **recommandations nouvelles et concrètes** (fonctionnelles, métier/ingénieur, académiques) pour intégrer **les modules réseau / réservoir / pompage** dans le nouveau **`*-unified`**. Je donne aussi un **schéma YAML enrichi**, les **formules clés**, le **contrat de sortie** et des **tests / validations** recommandés. Direct et prêt à copier-coller.

# 1) Axe Fonctionnel (expérience utilisateur & logiciel)

- **Mode `unified` = single entry point** : accepts inline args OR `--input` (YAML/CSV). Si `--input` présent → `mode=enhanced` par défaut.
    
- **Options communes (obligatoires pour `*-unified`)** :  
    `--input`, `--mode auto|simple|enhanced`, `--export json|yaml|csv|html|xlsx`, `--output`, `--verbose`.
    
- **Diagnostics enhanced** :
    
    - affichage pas-à-pas des formules, itérations et conditions de convergence (`--verbose`).
        
    - rapports d’optimisation: liste des diamètres commerciaux testés et métriques (vitesse, perte, coût estimé si available).
        
- **Profil de calcul** : `--methode hazen_williams|darcy|colebrook` (network); fallback automatique si méthode non match.
    
- **Catalogue de diamètres** : proposer et tester diamètres commerciaux standards (mm) et renvoyer top-3 candidats.
    
- **Exports homogènes** : JSON canonical + Excel sheet par module (Inputs, Calculs, Résultats, Diagnostics).
    
- **Erreurs UX** : messages d’erreur orientés correction (ex: « rugosite invalide — valeur attendue entre 50 et 300 (H-W) »).
    
- **Performances** : calculs itératifs avec max_iter configurable et tolérance `--tolerance`.
    

# 2) Axe Métier / Ingénieur

- **Méthodes disponibles** :
    
    - _Conduites_ : Hazen-Williams (rapide, hydraulique pratique) & Darcy-Weisbach + Colebrook (précis, itératif).
        
    - _Réservoir_ : règles stockage (Journée + incendie + secours + freeboard), phasage par horizon.
        
    - _Pompes_ : calcul HMT complet (Hauteurs géométrique + pertes), puissance hydraulique → électrique (avec rendement).
        
- **Algorithme pré-dimensionnement conduites** (recommandé) :
    
    1. Estimer diamètre par V_target : D0=4QπVtargetD_0 = \sqrt{\dfrac{4Q}{\pi V_{target}}}
        
    2. Tester diamètres commerciaux ≥ D0, pour chaque diamètre calculer perte (H-W ou Darcy) et vitesse.
        
    3. Retenir diamètres qui respectent vitesse_min/max et pression_min, trier par critère (min perte / vitesse cible / coût estimé).
        
    4. Si mode `enhanced` → renvoyer courbe itérative (diam vs perte) + diagnostics.
        
- **Réservoir** :
    
    - stockage utile = demande_journalière × facteur_stockage + reserve_incendie + reserve_secours.
        
    - contraintes géométriques (diamètre_max / hauteur_max) → calculer dimensions géométriques (pour cylindre: V=πD2H/4V = \pi D^2 H /4).
        
    - proposer variantes (plus bas/large ou haut/étroit) et effets sur pressions.
        
- **Pompes** :
    
    - Puissance hydraulique : Ph=ρgQHP_h = \rho g Q H (W). (ρ=1000 kg/m³, g=9.81 m/s²).
        
    - Puissance électrique : Pe=PhηP_e = \dfrac{P_h}{\eta} (ajouter factor service et réserve).
        
    - Choisir nombre de pompes et fonctionnement (série/parallèle) selon NPSH, variations Q et maintenance.
        
- **Exports pour simulateurs** : générer fichiers d’import EPANET/INP et table de demandes horaires.
    

# 3) Axe Académique / Scientifique

- **Transparence & traçabilité** :
    
    - chaque valeur sortie = valeur + `provenance` (source param / CLI / default) + `timestamp`.
        
- **Notebook reproductible** : fournir un notebook pour chaque module (réseau/réservoir/pompage) qui exécute `lcpi` CLI via subprocess ou appelle les mêmes fonctions python.
    
- **Annexe méthodologique** : inclure formules exactes et limites d’application (ex : H-W fiable pour Re>~3000 et matériaux lisses).
    
- **Analyses** :
    
    - sensibilité (±10% sur Q, rugosité, dotation) et Monte-Carlo (optionnel, `--mc N`).
        
    - documenter hypothèses: densité, g, coefficients, unités.
        
- **Publication-ready outputs** : LaTeX templates avec sections Méthode, Hypothèses, Calculs pas-à-pas, Figures.
    

# 4) Proposition concrète : schéma YAML enrichi (avec unified metadata)

```yaml
meta:
  projet: "AEP Agbelouvé"
  auteur: "Ing. X"
  date: "2025-08-15"
  lcpi_version: "1.3.0"
  mode_unified: "enhanced"   # optionnel, override CLI

network:
  methode: "hazen_williams"    # ou darcy
  conduites:
    C1:
      longueur_m: 500
      debit_m3_s: 0.05
      rugosite: 100          # H-W c, ou friction factor si darcy
      materiau: "acier"
    C2:
      longueur_m: 300
      debit_m3_s: 0.03
      rugosite: 120
      materiau: "pvc"
  parametres:
    vitesse_cible_m_s: 1.2
    vitesse_max_m_s: 2.5
    pression_min_mCE: 20
    tolerance: 0.001
    diametres_commerciaux_mm: [50,63,75,90,110,125,140,160,200,250,300,350,400]

reservoir:
  type: "stockage"
  forme: "cylindrique"
  parametres:
    demande_journaliere_m3: 2850.0
    facteur_stockage_jours: 0.5   # ex: 0.5*demande_jour = demi-journée
    reserve_incendie_m3: 100
    reserve_secours_m3: 50
    hauteur_max_m: 8
    diametre_max_m: 15
  contraintes:
    pression_min_mCE: 20
    pression_max_mCE: 80
    niveau_terrain_mNGF: 150

pumping:
  station: "Station_Principale"
  parametres:
    debit_nominal_m3_s: 0.15
    hauteur_geometrique_m: 45
    longueur_conduite_m: 2500
    diametre_conduite_m: 0.4
    rugosite: 100
    rendement_min: 0.75
  pompes:
    P1:
      type: "centrifuge"
      nombre: 2
      fonctionnement: "parallele"

scenarios:
  base:
    network: "default"
    reservoir: "default"
    pumping: "default"
  urbain_2030:
    population_scale: 1.2
```

# 5) Formules clés (à afficher en `--verbose`)

- **Diamètre estimé par vitesse**:  
    D0=4QπVtargetD_0 = \sqrt{\dfrac{4Q}{\pi V_{\text{target}}}} (m)
    
- **Hazen-Williams (perte par longueur)**:  
    S=10.67 Q1.852C1.852 D4.87S = \dfrac{10.67 \, Q^{1.852}}{C^{1.852} \, D^{4.87}} (m/m)  
    perte (m) = S×LS \times L
    
- **Darcy-Weisbach**:  
    hf=fLDV22gh_f = f \dfrac{L}{D} \dfrac{V^2}{2g} où ff via Colebrook ou formule de Moody.
    
- **Puissance hydraulique**:  
    Ph  [W]=ρ g Q HP_h \;[W] = \rho \, g \, Q \, H (avec ρ=1000 kg/m³, g=9.81 m/s²)  
    Pe  [W]=PhηP_e \;[W] = \dfrac{P_h}{\eta} (η = rendement)
    
- **Volume réservoir cylindrique**:  
    V=πD2H4V = \dfrac{\pi D^2 H}{4} (m³)
    

# 6) Contract de sortie `canonical` (exigé pour `*-unified`)

Chaque commande retourne / écrit un JSON structuré :

```json
{
  "meta": { "projet":"...", "lcpi_version":"1.3.0", "timestamp":"..." },
  "inputs": { /* echo validated YAML or inline args */ },
  "valeurs": {
    "network": {
      "C1": { "diametre_mm": 160, "vitesse_m_s": 1.15, "perte_m": 12.3 },
      ...
    },
    "reservoir": { "volume_utile_m3": 650, "diametre_m": 10, "hauteur_m": 8 },
    "pumping": { "P_h_W": 102345, "P_e_W": 136460, "nombre_pompes": 2 }
  },
  "diagnostics": [ "mode: enhanced", "validation: OK", "warnings: vitesse élevée sur C2" ],
  "iterations": { /* itérations Hazen/Darcy si any */ },
  "hash_input": "sha256:..."
}
```

> Les clés `network`/`reservoir`/`pumping` doivent apparaître même si module non utilisé (null ou absent ok).

# 7) Validation / règles métier (Phase-0)

- `deb[i]` > 0, `longueur` > 0.
    
- `vitesse_cible` 0.3–3.0 m/s (warn en dehors).
    
- `rugosite` (H-W C) 30–160 typiquement ; si darcy -> check friction factor range.
    
- `pression_min` en mCE.
    
- `diametre_commercial` nearest_up(D0).
    
- Warnings: si perte totale > `perte-max` CLI option → advise alternative (augmenter D ou réduire L).
    

# 8) Tests recommandés (CI)

- **Unitaires** : diamètre estimation, conversion unités, Hazen formula correctness, pump power formula.
    
- **Integration** : YAML full pipeline `lcpi aep network-unified --input data/reseau.yml --export json` → compare snapshot JSON.
    
- **Edge cases** : very low Q (laminar warning), Q very high (v>vmax), impossible constraints (diameter > diam_max).
    
- **Regression** : snapshot JSON for canonical keys.
    

# 9) Exemples d’usage `unified` (prêt à coller)

- YAML input enhanced (network):
    

```bash
lcpi aep network-unified --input data/reseau.yml --mode auto --export json --output results/network.json --verbose
```

- Inline quick (simple):
    

```bash
lcpi aep network-unified 0.05 --longueur 500 --rugosite 100 --materiau acier --methode hazen_williams --export yaml
```

- Reservoir unified:
    

```bash
lcpi aep reservoir-unified --input data/reservoir.yml --export xlsx --verbose
```

- Pompage unified:
    

```bash
lcpi aep pumping-unified 0.15 --hmt 45 --diametre 0.4 --rendement 0.75 --export json
```

# 10) Priorités d’implémentation (concrete)

1. **Haute** : `network_unified` (inline + `--input`), exporter JSON/YAML, diagnostics basiques, tests unitaires.
    
2. **Moyenne** : `pumping_unified` & `reservoir_unified`, catalogue diametres, EPANET export.
    
3. **Basse** : Monte-Carlo intégré, coût estimé, optimisation coût-vitesse multi-critère.
    

---

Si tu veux, j’écris **a)** le JSON-Schema enrichi pour `network/reservoir/pumping`, **b)** le handler `router_unified` complet pour ces trois modules, ou **c)** l’implémentation Python de Hazen-Williams + test pytest prêt à coller. Lequel tu veux que je génère maintenant ?

Parfait — je te fournis la même livraison structurée que précédemment, adaptée à **PHASE 2 (Simulation / Analyse hydraulique)** et **PHASE 3 (Post-calcul / Métré & Devis)**. Tout est orienté **CLI `*-unified`**, rétro-compatible, prêt à copier-coller dans le repo. Je reste concis, pratique et technique.

# 1) Axe Fonctionnel (expérience utilisateur & logiciel)

- **Commandes `*-unified` améliorées** : mêmes options communes (`--input`, `--mode auto|simple|enhanced`, `--export json|yaml|csv|xlsx|html`, `--output`, `--verbose`, `--tolerance`, `--iterations`).
    
- **Mode `diagnose`** pour `diagnose-network` : check topologie, noeuds isolés, cycles orphelins, compatibilité EPANET (génère `.inp` test).
    
- **Wrapper Hardy-Cross unifié** : accepte CSV ou YAML via `--input`, ou inline via pipes spec; `--method` prend `hazen_williams`/`darcy` pour pertes.
    
- **EPANET bridge** : `simulate-inp` lance EPANET (si dispo) ou fallback vers moteur interne (si packaging le permet) ; fournit rapports comparables (pressures, flows, headloss).
    
- **Workflow orchestration** : `workflow-complete` exécute séquentiellement validation → Hardy-Cross → EPANET → comparaison → post-processing → rapport. Retours structurés et codes d’erreur.
    
- **Diagnostics `--verbose`** : matrices d’incidence, graphes topologiques (GraphML/GeoJSON), logs d’itération pour Hardy-Cross (ΔQ, somme erreur boucle).
    
- **Exports harmonisés** : canonical JSON + Excel multi-sheet (Nodes, Pipes, Loops, HardyCrossIterations, EPANETresults, Comparisons).
    
- **Checks rapides** : `lcpi aep validate-network` lance validation topologique + domaine de valeurs (diamètres>0, demandes signées, noeuds référencés).
    

# 2) Axe Métier / Ingénieur

- **Diagnostic de connectivité** :
    
    - vérifier composantes connexes, noeuds sans branchements, arcs dupliqués, sens incohérent (noeud_amont==noeud_aval).
        
    - compatibilité EPANET check: noms, unités, attributs obligatoires.
        
- **Hardy-Cross** :
    
    - acceptance: boucles détectées automatiquement, orientation des boucles, flux initiaux si manquants → estimation heuristique (répartition proportionnelle aux longueurs).
        
    - outputs: Q_final par tuyau, ΔQ itératif, convergence flag, iterations_used.
        
- **EPANET validation** :
    
    - import .inp → exécution → extraire heads, flows, velocities; normaliser unités.
        
- **Comparaison** :
    
    - calculer écarts absolus et relatifs (ΔQ, ΔH) par tuyau/noeud; statistiques agrégées (MAE, RMSE, %>tolerance).
        
    - rules: si >5% sur plus de X% des tuyaux => alerte (configurable).
        
- **Post-calcul** :
    
    - identification des points critiques (vitesse > vmax, P < Pmin), proposer actions (augmenter D, surpression, phasage).
        
- **Coup de bélier** :
    
    - calcul rapide de surpression approximative : ΔP≈ρcΔV\Delta P \approx \rho c \Delta V (méthode simplifiée) ; simulation temporelle optionnelle via méthode des caractéristiques si `--advanced`.
        
- **Métré & Devis** :
    
    - extraire listes matériaux (longueur par diamètre, vannes, regards, fondations), indices de coût par unité, marge & imprévus paramétrables.
        

# 3) Axe Académique / Scientifique

- **Reproductibilité** :
    
    - notebook Jupyter qui exécute les mêmes commandes CLI (ou appelle fonctions libs) et génère figures + tableaux + texte prêt à insérer dans rapport.
        
- **Traçabilité** :
    
    - chaque résultat -> provenance (input CLI/YAML/CSV, méthode, version LCPI), timestamps, hash_inputs.
        
- **Documentation méthodologique** :
    
    - annexes: hypothèses, limites d’applicabilité (Hardy-Cross pour petits réseaux maillés, EPANET pour réseaux complets avec pertes valves).
        
- **Analyses** :
    
    - sensibilité (±param), bootstrap/Monte-Carlo option (`--mc N`) sur Q_init/rugosité/deman­de.
        
- **Tests & cas d’étude** :
    
    - jeux d’essais standard (simple loop, double loop, large maillage) avec résultats attendus pour CI.
        

# 4) Schéma YAML enrichi — Phase 2 & 3 (extrait unifié)

```yaml
meta:
  projet: "Projet AEP Exemple"
  auteur: "Ing. X"
  date: "2025-08-15"
  lcpi_version: "1.3.0"
  mode_unified: "enhanced"

reseau_complet:
  nom: "Réseau Principal"
  type: "maillé"
  noeuds:
    N1:
      role: "reservoir"
      cote_m: 150.0
      demande_m3_s: 0.0
    N2:
      role: "consommation"
      cote_m: 145.0
      demande_m3_s: 0.02
  conduites:
    C1:
      noeud_amont: "N1"
      noeud_aval: "N2"
      longueur_m: 500
      diametre_m: 0.2
      rugosite: 100
      materiau: "acier"
      statut: "existant"
  loops:   # optionnel, utile pour Hardy-Cross
    L1: [C1, C2, C3, C4]

hardy_cross:
  input_format: "csv"   # or yaml
  tolerance: 1e-6
  max_iterations: 200
  pipes_csv: "data/hardy_pipes.csv"  # alternative to inline

epanet:
  inp_file: "data/reseau.inp"
  run_options:
    duration_h: 24
    timestep_min: 60

post:
  checks:
    vitesse_min_m_s: 0.5
    vitesse_max_m_s: 2.5
    pression_min_mce: 20
    pression_max_mce: 80
  coup_belier:
    celerite_m_s: 1200
    analyse: true

project:
  metrage:
    longueur_totale_m: 25000
    breakdown_by_diameter: true
  devis:
    prix_unitaires: "data/prix_unitaires.yml"
    marge_pct: 10
```

# 5) Formules clés à exposer (`--verbose`)

- Hardy-Cross loop correction:  
    ΔQ=−∑(hi/ri)∑((2Qihi′)/ri)\Delta Q = - \dfrac{\sum (h_i / r_i)}{\sum ( (2 Q_i h'_i) / r_i )} (forme générique — afficher les formules exactes du code).
    
- Hazen-Williams (pour pertes dans Hardy-Cross si utilisé):  
    S=10.67 Q1.852C1.852 D4.87S = \dfrac{10.67\, Q^{1.852}}{C^{1.852}\,D^{4.87}}, perte = S×LS \times L.
    
- Darcy-Weisbach:  
    hf=fLDV22gh_f = f \dfrac{L}{D}\dfrac{V^2}{2g} ; ff via Colebrook/Manning approximations.
    
- Puissance pompage:  
    Ph=ρgQHP_h = \rho g Q H; Pe=PhηP_e = \dfrac{P_h}{\eta}.
    
- Coup de bélier (approx):  
    ΔPmax≈ρcΔV\Delta P_{max} \approx \rho c \Delta V (valeur indicative — préciser limites).
    

# 6) Contrat de sortie canonical (Phase 2 & 3)

Chaque exécution écrit un JSON canonical contenant:

```json
{
  "meta": { "projet":"...", "lcpi_version":"1.3.0", "timestamp":"..." },
  "inputs": { /* echo validated inputs */ },
  "diagnostics": {
    "connectivity_ok": true,
    "components_isolated": [],
    "epanet_compatible": true
  },
  "hardy_cross": {
    "converged": true,
    "iterations": 12,
    "pipes": { "P1": {"Q_m3_s":0.05, "deltaQ":1e-7}, ... },
    "loops": { "L1": {"residual":1e-9} }
  },
  "epanet": {
    "nodes": { "N1": {"head_m":150.0, "pressure_mCE":...}, ... },
    "pipes": { "C1": {"flow_m3_s":0.049, "velocity_m_s":1.2} }
  },
  "comparison": {
    "Q_mae": 0.0003,
    "H_mae": 0.12,
    "flags": ["Q_diff_large_on_C4"]
  },
  "post": {
    "critical_points":[ {"node":"N7","issue":"low_pressure","value":12.3} ]
  },
  "metrage": { /* lengths per diameter, materials */ },
  "devis": { "total": 650000, "breakdown": {"reseau":450000} },
  "hash_input": "sha256:..."
}
```

> Toujours fournir `meta`, `inputs`, `diagnostics`, `hardy_cross`, `epanet`, `comparison`, `post`, `metrage`, `devis`.

# 7) Validation et règles métier (Phase-0 & Phase-2 checks)

- Topologie: tous `noeud_amont`/`noeud_aval` doivent exister.
    
- Conservation des débits sur boucle: sum(inflows - outflows) ≈ 0 (avec tolérance).
    
- Diamètres > 0, longueur > 0, rugosité dans plage raisonnable.
    
- Hardy-Cross convergence tolérance par défaut `1e-6` (configurable).
    
- Comparaison: tolérance absolue/relative configurable (default 5%).
    
- Coup de bélier: if vitesse_nominale > 2.5 m/s → warn for transient risk.
    

# 8) Tests recommandés (CI)

- **Unitaires** :
    
    - test_corrige_hardy_cross_simple (2-loop toy case with known solution).
        
    - test_epanet_parser_roundtrip (YAML → INP → parse back minimal).
        
    - test_connectivity_detects_islands.
        
- **Intégration** :
    
    - full workflow: `validate` → `hardy-cross` → `simulate-inp` → `workflow-complete --compare` → assert `comparison.Q_mae < 0.05` (configurable).
        
- **Edge cases** :
    
    - disconnected network, negative demands, zero-length pipes, extreme rugosity → proper errors/warnings.
        
- **Snapshots** :
    
    - baseline JSON outputs for regression.
        

# 9) CLI signatures & exemples prêts à coller

```bash
# Diagnostic connectivité
lcpi aep diagnose-network --input data/reseau_complet.yml --export json --output results/diag.json --verbose

# Hardy-Cross unified (CSV input)
lcpi aep hardy-cross-unified --input data/hardy.csv --mode auto --tolerance 1e-6 --iterations 200 --export json --output results/hc.json

# EPANET simulate
lcpi aep simulate-inp --input data/reseau.inp --export json --output results/epanet.json --verbose

# Workflow complet + comparaison
lcpi aep workflow-complete --input data/reseau_final.yml --compare --reports --output results/workflow/ --verbose

# Post / metrage / devis
lcpi aep project-unified --input data/projet_final.yml --type complet --export xlsx --output results/metrage.xlsx
```

# 10) Priorités d’implémentation (concret)

1. **Haute**
    
    - `diagnose-network` (connectivity + EPANET compatibility)
        
    - `hardy-cross-unified` core algorithm + CSV/YAML input + JSON export
        
    - `simulate-inp` wrapper minimal (parse INP, run engine if available, otherwise parse results)
        
2. **Moyenne**
    
    - `workflow-complete` orchestration + comparison module (hardy vs epanet)
        
    - canonical exporter multi-sheet Excel et reports LaTeX
        
3. **Basse**
    
    - transient coup_de_belier avancé (méthode caractéristiques)
        
    - Monte-Carlo intégré `--mc` pour incertitude
        
    - coût estimé détaillé et optimisation coût/vitesse
        

# 11) Snippets utiles (validator & test stub)

**JSON Schema (mini) pour réseau_complet** (à étendre)

```json
{
  "$id":"https://lcpi/schemas/reseau.schema.json",
  "type":"object",
  "required":["reseau_complet"],
  "properties":{
    "reseau_complet": {
      "type":"object",
      "required":["noeuds","conduites"],
      "properties":{
        "noeuds":{"type":"object"},
        "conduites":{"type":"object"}
      }
    }
  }
}
```

**Pytest stub**

```python
def test_hardy_cross_converges(sample_hardy_csv, runner, tmp_path):
    out = tmp_path/"hc.json"
    res = runner.invoke(cli.app, ["hardy-cross-unified","--input",str(sample_hardy_csv),"--export","json","--output",str(out)])
    assert res.exit_code==0
    data = json.loads(out.read_text())
    assert data["hardy_cross"]["converged"] is True
```

# 12) Critères d’acceptation (exemples mesurables)

- `lcpi aep diagnose-network sample.yml` → exit 0 si réseau connecté, otherwise non-zero + diagnostics clairs.
    
- `lcpi aep hardy-cross-unified sample.csv --tolerance 1e-6` → `hardy_cross.converged == true` et `iterations < max_iterations`.
    
- `workflow-complete sample.yml --compare` → génère `comparison.json` et `rapport.pdf`; `comparison.Q_mae` < tol ou signalement si non respecté.
    
- Reports: PDF contient Méthode, Hypothèses, Tableaux HC et EPANET, Comparaisons (écarts absolus & relatifs).
    

---

Si tu veux que je génère **a)** le JSON-Schema complet (reseau+hardy+epanet+post), **b)** l’implémentation Python du noyau Hardy-Cross (avec tests pytest), ou **c)** le handler `workflow-complete` (orchestrator) prêt à coller — je peux le coder maintenant. Lequel tu veux que je produise tout de suite ?