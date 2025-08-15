# 🚀 Workflow AEP Complet - Alimentation en Eau Potable

## 📋 Vue d'Ensemble

Ce document décrit le workflow complet pour l'étude et le dimensionnement d'un système d'Alimentation en Eau Potable (AEP) en utilisant les commandes LCPI. Le workflow est divisé en **4 phases principales** : Validation des Données, Pré-Calcul, Simulation, et Post-Calcul.

---

## ⚙️ Options communes des commandes `*-unified`

Toutes les commandes unifiées acceptent des paramètres inline OU un fichier via `--input`.

- **--input**: chemin d'un fichier `YAML/CSV/JSON`. Si fourni, `--mode` bascule par défaut sur `enhanced`.
- **--mode**: `auto|simple|enhanced` (défaut: `auto`).
- **--export**: `json|csv|markdown|yaml|html` (défaut: `json`).
- **--output**: chemin de fichier pour sauvegarder l'export.
- **--verbose**: affiche davantage de détails lorsque pertinent.

La sortie est standardisée sous la forme:

```yaml
valeurs: {...}
diagnostics: []   # liste d'avertissements ou messages
iterations: ...   # présent si applicable (ex: Hardy-Cross)
```

---

## 🔍 **PHASE 0 : VALIDATION DES DONNÉES D'ENTRÉE**

### **0.1 Vérification d'Intégrité des Fichiers**

**Objectif :** Valider la cohérence et l'intégrité des données d'entrée avant traitement

**Données d'entrée :**
- Fichiers CSV et YAML du projet
- Critères de validation par type de fichier

**Structure du répertoire de validation :**
```
data/
├── population.csv          # Données démographiques
├── besoins.yml            # Configuration demande
├── reseau.yml             # Configuration réseau
├── reservoir.yml          # Configuration réservoir
├── pompage.yml            # Configuration pompage
├── protection.yml         # Configuration protection
└── projet_final.yml       # Configuration projet complet
```

**Commande LCPI :**
```bash
lcpi aep validate-input data/besoins.yml --type auto --export json
```

**Résultat :**
- Rapport de validation (sortie standardisée: `valeurs`, `diagnostics`)
- Identification des erreurs et incohérences
- Recommandations de correction

---

### **0.2 Validation des Données Démographiques**

**Objectif :** Vérifier la cohérence des données de population

**Données d'entrée :**
- Fichier CSV de population
- Critères de validation démographique

**Commande LCPI :**
```bash
lcpi aep validate-population data/population.yml --export markdown
```

**Résultat :**
- Validation de la progression démographique
- Détection d'anomalies statistiques
- Rapport de qualité des données

---

### **0.3 Validation de la Topologie du Réseau**

**Objectif :** Vérifier la cohérence topologique du réseau

**Données d'entrée :**
- Fichier YAML ou CSV du réseau
- Règles de connectivité

**Commande LCPI :**
```bash
lcpi aep validate-network data/reseau.yml --export json
```

**Résultat :**
- Validation de la connectivité
- Détection des nœuds isolés
- Vérification des boucles

---

## 🔄 **PHASE 1 : PRÉ-CALCUL - ÉTUDE PRÉLIMINAIRE**

### **1.1 Calcul de Projection Démographique**

**Objectif :** Déterminer l'évolution de la population sur la période d'étude

**Données d'entrée :**
- Fichier CSV avec données historiques de population
- Période de projection souhaitée
- Taux de croissance démographique

**Structure du fichier CSV d'entrée :**
```csv
annee,population
2020,15000
2021,15200
2022,15400
2023,15600
```

**Commande LCPI :**
```bash
lcpi aep population data/population.csv --debut 2020 --fin 2050 --taux 0.025 --output projections.csv
```

**Résultat :**
- Projection démographique par année
- Fichier CSV avec population projetée
- Graphiques d'évolution démographique

---

### **1.2 Calcul des Besoins en Eau**

**Objectif :** Évaluer les besoins en eau actuels et futurs

**Données d'entrée :**
- Population actuelle et projetée
- Consommations par type d'usage (domestique, industriel, commercial)
- Coefficients de pointe

**Structure du fichier YAML d'entrée :**
```yaml
population:
  actuelle: 15000
  projetee_2030: 18000
  projetee_2050: 22000

consommation:
  domestique: 150  # litres/habitant/jour
  industriel: 50   # litres/habitant/jour
  commercial: 30   # litres/habitant/jour

coefficients:
  pointe_journaliere: 1.3
  pointe_horaire: 1.8
  fuites: 0.15
```

**Commande LCPI (YAML) :**
```bash
lcpi aep demand data/besoins.yml --type global --details
```

**Commande LCPI (Unifiée) :**
```bash
lcpi aep demand-unified 15000 --dotation 150 --coeff-pointe 1.5 --type branchement_prive --verbose
```

**Commande LCPI (Unifiée avec --input) :**
```bash
lcpi aep demand-unified --input data/besoins.yml --export markdown
```

**Commande LCPI :**
```bash
lcpi aep demand data/besoins.yml --type global --details
```

**Résultat :**
- Demande moyenne journalière
- Demande de pointe journalière et horaire
- Répartition par type de consommation

---

### **1.3 Pré-dimensionnement des Conduites**

**Objectif :** Déterminer les diamètres préliminaires des conduites

**Données d'entrée :**
- Débits de conception
- Longueurs des tronçons
- Matériaux de conduites
- Vitesses d'écoulement cibles

**Structure du fichier YAML d'entrée :**
```yaml
reseau:
  conduites:
    C1:
      longueur: 500      # mètres
      debit: 0.05       # m³/s
      rugosite: 100     # coefficient Hazen-Williams
      type: "acier"
    
    C2:
      longueur: 300
      debit: 0.03
      rugosite: 120
      type: "pvc"

parametres:
  vitesse_max: 2.5      # m/s
  pression_min: 20      # m de colonne d'eau
  tolerance: 0.001      # tolérance de convergence
```

**Commande LCPI (YAML) :**
```bash
lcpi aep network data/reseau.yml --formule hazen_williams
```

**Commande LCPI (Unifiée) :**
```bash
lcpi aep network-unified 0.1 --longueur 1000 --materiau fonte --perte-max 10.0 --methode darcy --verbose
```

**Commande LCPI (Unifiée avec --input) :**
```bash
lcpi aep network-unified --input data/reseau.yml --export yaml
```

**Résultat :**
- Diamètres préliminaires des conduites
- Vitesses d'écoulement
- Pertes de charge estimées

---

### **1.4 Dimensionnement Préliminaire du Réservoir**

**Objectif :** Évaluer le volume de stockage nécessaire

**Données d'entrée :**
- Demande journalière
- Type d'adduction (continue/discontinue)
- Forme souhaitée (cylindrique/parallélépipédique)

**Structure du fichier YAML d'entrée :**
```yaml
reservoir:
  type: "stockage"
  forme: "cylindrique"  # ou "parallelepipedique"
  
  parametres:
    volume_utile: 500    # m³
    reserve_incendie: 100 # m³
    reserve_secours: 50   # m³
    hauteur_max: 8       # mètres
    diametre_max: 15     # mètres (pour cylindrique)
    
  contraintes:
    pression_min: 20     # m de colonne d'eau
    pression_max: 80     # m de colonne d'eau
    niveau_terrain: 150  # mètres NGF
```

**Commande LCPI (YAML) :**
```bash
lcpi aep reservoir data/reservoir.yml --forme cylindrique
```

**Commande LCPI (Unifiée) :**
```bash
lcpi aep reservoir-unified 1000 --adduction continue --forme cylindrique --zone ville_francaise_peu_importante --verbose
```

**Commande LCPI (Unifiée avec --input) :**
```bash
lcpi aep reservoir-unified --input data/reservoir.yml --export html
```

**Résultat :**
- Volume utile et total du réservoir
- Dimensions géométriques
- Capacité de réserve

---

### **1.5 Dimensionnement Préliminaire des Pompes**

**Objectif :** Évaluer la puissance des équipements de pompage

**Données d'entrée :**
- Débit d'adduction
- Hauteur manométrique totale
- Type de pompe souhaité

**Structure du fichier YAML d'entrée :**
```yaml
pompage:
  station: "Station_Principale"
  type: "adduction"
  
  parametres:
    debit_nominal: 0.15    # m³/s
    hauteur_geometrique: 45 # mètres
    longueur_conduite: 2500 # mètres
    diametre_conduite: 0.4  # mètres
    rugosite: 100           # coefficient Hazen-Williams
    
  contraintes:
    vitesse_max: 2.5        # m/s
    pression_max: 100       # bar
    rendement_min: 0.75     # rendement minimum des pompes
    
  pompes:
    P1:
      type: "centrifuge"
      nombre: 2
      fonctionnement: "parallele"
```

**Commande LCPI (YAML) :**
```bash
lcpi aep pumping data/pompage.yml --rendement 0.75
```

**Commande LCPI (Unifiée) :**
```bash
lcpi aep pumping-unified 100 --hmt 50 --type centrifuge --rendement 0.75 --verbose
```

**Commande LCPI (Unifiée avec --input) :**
```bash
lcpi aep pumping-unified --input data/pompage.yml --export csv
```

**Résultat :**
- Puissance hydraulique et électrique
- Caractéristiques des pompes
- Consommation énergétique

---

## ⚡ **PHASE 2 : SIMULATION - ANALYSE HYDRAULIQUE**

### **2.1 Diagnostic de Connectivité du Réseau**

**Objectif :** Vérifier la connectivité et la cohérence du réseau

**Données d'entrée :**
- Fichier YAML du réseau complet
- Topologie des nœuds et conduites

**Structure du fichier YAML d'entrée :**
```yaml
reseau_complet:
  nom: "Réseau Principal"
  type: "maillé"
  
  noeuds:
    N1:
      type: "reservoir"
      cote: 150.0        # mètres NGF
      demande: 0.0       # m³/s
      commentaire: "Réservoir principal"
    
    N2:
      type: "consommation"
      cote: 145.0
      demande: 0.02      # m³/s
      commentaire: "Zone résidentielle"
    
    N3:
      type: "consommation"
      cote: 142.0
      demande: 0.015     # m³/s
      commentaire: "Zone commerciale"
  
  conduites:
    C1:
      noeud_amont: "N1"
      noeud_aval: "N2"
      longueur: 500      # mètres
      diametre: 0.2      # mètres
      rugosite: 100      # coefficient Hazen-Williams
      type: "acier"
      statut: "existant"
    
    C2:
      noeud_amont: "N2"
      noeud_aval: "N3"
      longueur: 300      # mètres
      diametre: 0.15     # mètres
      rugosite: 120      # coefficient Hazen-Williams
      type: "pvc"
      statut: "projet"
```

**Commande LCPI :**
```bash
lcpi aep diagnose-network data/reseau_complet.yml --verbose
```

**Résultat :**
- Statut de connectivité
- Compatibilité EPANET
- Analyse topologique

---

### **2.2 Simulation Hardy-Cross**

**Objectif :** Calculer la distribution des débits par méthode itérative

**Données d'entrée :**
- Réseau maillé avec boucles
- Débits initiaux estimés
- Paramètres de convergence

**Structure du fichier CSV d'entrée (Hardy-Cross) :**
```csv
pipe_id,from_node,to_node,length,diameter,roughness,initial_flow
P1,N1,N2,500,0.2,100,0.05
P2,N2,N3,300,0.15,120,0.03
P3,N3,N4,400,0.18,110,0.04
P4,N4,N1,600,0.25,100,0.06
```

**Structure du fichier YAML d'entrée (alternative) :**
```yaml
reseau:
  noeuds:
    N1:
      type: "reservoir"
      cote: 150.0        # mètres NGF
      demande: 0.0       # m³/s
    
    N2:
      type: "consommation"
      cote: 145.0
      demande: 0.02      # m³/s
  
  conduites:
    C1:
      noeud_amont: "N1"
      noeud_aval: "N2"
      longueur: 500      # mètres
      diametre: 0.2      # mètres
      rugosite: 100      # coefficient Hazen-Williams
      type: "acier"
```

**Commande LCPI :**
```bash
lcpi aep hardy-cross data/reseau_maille.yml --tolerance 1e-6 --iterations 100 --export resultats_hardy.json
```

**Commande LCPI (Unifiée) :**
```bash
lcpi aep hardy-cross-unified --input data/reseau_maille.yml --tolerance 1e-6 --export json
lcpi aep hardy-cross-unified --input data/reseau.csv --iterations 200 --export markdown
```

Sortie standardisée: `{ valeurs, diagnostics, iterations }`.

**Résultat :**
- Débits équilibrés dans chaque conduite
- Pressions aux nœuds
- Convergence de la méthode

---

### **2.3 Simulation EPANET**

**Objectif :** Valider les résultats avec le standard industriel EPANET

**Données d'entrée :**
- Fichier .inp EPANET ou réseau YAML converti

**Commande LCPI :**
```bash
lcpi aep simulate-inp data/reseau.inp --format json --verbose
```

**Résultat :**
- Simulation hydraulique complète
- Validation des pressions et débits
- Statistiques de convergence

---

### **2.4 Validation Croisée Hardy-Cross vs EPANET**

**Objectif :** Comparer et valider les deux méthodes de calcul

**Données d'entrée :**
- Résultats Hardy-Cross
- Résultats EPANET

**Commande LCPI :**
```bash
lcpi aep workflow-complete data/reseau_final.yml --compare --reports --verbose
```

**Résultat :**
- Comparaison des débits et pressions
- Analyse des écarts
- Rapport de validation

---

## 📊 **PHASE 3 : POST-CALCUL - DIMENSIONNEMENT FINAL**

### **3.1 Analyse des Résultats de Simulation**

**Objectif :** Analyser les pressions et vitesses obtenues

**Données d'entrée :**
- Résultats de simulation (Hardy-Cross + EPANET)
- Critères de dimensionnement

**Commande LCPI :**
```bash
lcpi aep network data/reseau_final.yml --type verification --formule hazen_williams
```

**Résultat :**
- Vérification des vitesses d'écoulement
- Contrôle des pressions de service
- Identification des points critiques

---

### **3.2 Dimensionnement Final des Pompes d'Adduction**

**Objectif :** Dimensionner précisément les équipements de pompage

**Données d'entrée :**
- Débit d'adduction final
- Hauteur manométrique calculée
- Point de fonctionnement optimal

**Commande LCPI :**
```bash
lcpi aep pumping data/pompage_final.yml --type dimensionnement --rendement 0.80
```

**Résultat :**
- Puissance électrique finale
- Caractéristiques des pompes
- Courbes de fonctionnement

---

### **3.3 Vérification Coup de Bélier**

**Objectif :** Analyser les risques de coup de bélier

**Données d'entrée :**
- Caractéristiques de l'adduction
- Manœuvres de vanne
- Protection anti-coup de bélier

**Structure du fichier YAML d'entrée :**
```yaml
protection:
  type: "coup_belier"
  
  adduction:
    longueur: 2500        # mètres
    diametre: 0.4         # mètres
    vitesse_nominale: 2.0 # m/s
    celerite_onde: 1200   # m/s
    
  manoeuvres:
    type: "fermeture_vanne"
    duree_manoeuvre: 30   # secondes
    coefficient_fermeture: 0.8
    
  protection:
    type: "reservoir_air"
    volume: 50            # m³
    pression_nominale: 6  # bar
```

**Commande LCPI :**
```bash
lcpi aep protection data/protection.yml --type coup_belier
```

**Résultat :**
- Surpression maximale
- Durée de l'onde de choc
- Recommandations de protection

---

### **3.4 Calcul des Besoins en Énergie**

**Objectif :** Dimensionner les groupes électrogènes de secours

**Données d'entrée :**
- Puissance des pompes
- Autonomie souhaitée
- Type de combustible

**Commande LCPI :**
```bash
lcpi aep pumping data/groupe_electrogene.yml --type dimensionnement
```

**Résultat :**
- Puissance du groupe électrogène
- Consommation de combustible
- Autonomie garantie

---

### **3.5 Génération du Métré**

**Objectif :** Établir le métré détaillé du projet

**Données d'entrée :**
- Réseau dimensionné final
- Caractéristiques des matériaux

**Structure du fichier YAML d'entrée :**
```yaml
projet:
  nom: "Projet AEP Village"
  localisation: "Commune de Example"
  annee_etude: 2024
  
  population:
    actuelle: 15000
    projetee_2030: 18000
    projetee_2050: 22000
  
  reseau:
    type: "ramifie"
    longueur_totale: 25000  # mètres
    diametre_moyen: 0.15    # mètres
    materiau: "pvc"
  
  infrastructure:
    reservoir:
      volume: 500           # m³
      hauteur: 8            # mètres
      type: "cylindrique"
    
    pompage:
      puissance: 45         # kW
      debit: 0.15           # m³/s
      hauteur: 45           # mètres
  
  couts:
    reseau: 450000          # €
    reservoir: 80000        # €
    pompage: 120000         # €
    total: 650000           # €
```

**Commande LCPI :**
```bash
lcpi aep project data/projet_final.yml --type complet
```

**Résultat :**
- Longueurs par diamètre de conduite
- Quantités de matériaux
- Métré détaillé

---

### **3.6 Estimation du Devis**

**Objectif :** Évaluer le coût total du projet

**Données d'entrée :**
- Métré détaillé
- Prix unitaires des matériaux
- Coûts de main d'œuvre

**Commande LCPI :**
```bash
lcpi aep project data/projet_final.yml --type comparatif
```

**Résultat :**
- Coût total du projet
- Répartition par poste
- Comparaison de scénarios

---

## 📋 **RAPPORT FINAL**

### **Contenu du Rapport**

Le rapport final doit inclure **toutes les étapes de calcul intermédiaires** :

1. **Résumé exécutif** avec les résultats principaux
2. **Données d'entrée** utilisées pour chaque étape
3. **Méthodes de calcul** appliquées
4. **Résultats détaillés** de chaque phase
5. **Comparaisons** Hardy-Cross vs EPANET
6. **Écarts absolus et relatifs** pour chaque élément
7. **Recommandations** de dimensionnement
8. **Métré et devis** détaillés

### **Génération du Rapport**

**Commande LCPI :**
```bash
lcpi aep workflow-complete data/projet_final.yml --reports --output rapport_final/
```

**Résultat :**
- Rapport complet en PDF/HTML
- Données structurées en JSON
- Graphiques et visualisations
- Annexes techniques

---

## 📁 **FORMATS DE FICHIERS D'ENTRÉE**

### **Opérations utilisant des fichiers CSV :**

#### **1. Projection Démographique (`population`)**
- **Format :** CSV
- **Colonnes :** `annee,population`
- **Usage :** Données historiques de population pour projection

#### **2. Hardy-Cross (`hardy_cross_csv`)**
- **Format :** CSV
- **Colonnes :** `pipe_id,from_node,to_node,length,diameter,roughness,initial_flow`
- **Usage :** Réseau maillé pour calcul Hardy-Cross

### **Opérations de Validation :**

#### **1. Validation des Données (`validate-input`)**
- **Format :** Répertoire contenant tous les fichiers du projet
- **Usage :** Validation globale de l'intégrité des données

#### **2. Validation Démographique (`validate-population`)**
- **Format :** CSV (même format que `population`)
- **Usage :** Validation de la cohérence des données démographiques

#### **3. Validation Réseau (`validate-network`)**
- **Format :** YAML ou CSV (même format que `network` ou `hardy_cross`)
- **Usage :** Validation de la topologie et connectivité du réseau

### **Opérations utilisant des fichiers YAML :**

#### **1. Calcul de Demande (`demand`)**
- **Format :** YAML
- **Usage :** Configuration population, consommation, coefficients

#### **2. Dimensionnement Réseau (`network`)**
- **Format :** YAML
- **Usage :** Caractéristiques des conduites et paramètres

#### **3. Dimensionnement Réservoir (`reservoir`)**
- **Format :** YAML
- **Usage :** Paramètres géométriques et contraintes

#### **4. Dimensionnement Pompage (`pumping`)**
- **Format :** YAML
- **Usage :** Caractéristiques des pompes et contraintes

#### **5. Hardy-Cross YAML (`hardy_cross_yaml`)**
- **Format :** YAML
- **Usage :** Alternative au CSV pour réseau maillé

#### **6. Workflow Complet (`workflow_complete`)**
- **Format :** YAML
- **Usage :** Configuration complète du projet

### **Opérations utilisant des fichiers INP :**

#### **1. Simulation EPANET (`simulate_inp`)**
- **Format :** INP (format EPANET)
- **Usage :** Fichiers de simulation hydraulique EPANET

---

## 🎯 **POINTS CLÉS DU WORKFLOW**

### **Séquentialité des Étapes**
- **Phase 0 obligatoire** : Validation des données d'entrée avant tout calcul
- Chaque phase dépend des résultats de la précédente
- Validation croisée obligatoire entre Hardy-Cross et EPANET
- Itération possible sur les phases si nécessaire
- **Retour à la Phase 0** si des erreurs sont détectées

### **Critères de Validation**
- Vitesses d'écoulement : 0.5 à 2.5 m/s
- Pressions de service : 20 à 80 m de colonne d'eau
- Convergence Hardy-Cross : tolérance < 1e-6
- Écarts Hardy-Cross vs EPANET : < 5%

### **Livrables Attendus**
- Rapport technique complet
- Plans de dimensionnement
- Métré détaillé
- Devis estimatif
- Recommandations d'exploitation

---

*Document créé le : 2025-01-27*
*Version LCPI : 2.1.0*
*Workflow AEP Complet - Documentation Métier*
