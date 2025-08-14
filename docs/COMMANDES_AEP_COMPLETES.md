# 📋 COMMANDES AEP COMPLÈTES - LCPI v2.1.0

## 🎯 **RÉPONSE À VOTRE QUESTION**

**Oui, tout le workflow AEP fonctionne avec la commande `lcpi` !** Voici la liste complète des commandes disponibles.

---

## 🔢 **CALCULS DE BASE**

### **Population**
```bash
# Projection démographique
lcpi aep population <fichier.yml> [options]

# Exemples
lcpi aep population population_data.yml --methode malthus --annee 2050
lcpi aep population population_data.yml --comparaison
```

### **Demande en Eau**
```bash
# Calcul de demande
lcpi aep demand <fichier.yml> [options]

# Exemples
lcpi aep demand demande_data.yml --type global
lcpi aep demand demande_data.yml --type par_type --details
```

### **Réseau de Distribution**
```bash
# Dimensionnement réseau
lcpi aep network <fichier.yml> [options]

# Exemples
lcpi aep network reseau_data.yml --type dimensionnement --formule hazen_williams
lcpi aep network reseau_data.yml --type comparaison
```

### **Réservoir**
```bash
# Dimensionnement réservoir
lcpi aep reservoir <fichier.yml> [options]

# Exemples
lcpi aep reservoir reservoir_data.yml --type dimensionnement --forme cylindrique
lcpi aep reservoir reservoir_data.yml --type verification
```

### **Pompage**
```bash
# Dimensionnement pompage
lcpi aep pumping <fichier.yml> [options]

# Exemples
lcpi aep pumping pompage_data.yml --type dimensionnement --rendement 0.75
lcpi aep pumping pompage_data.yml --type comparaison
```

### **Protection Anti-bélier**
```bash
# Protection
lcpi aep protection <fichier.yml> [options]

# Exemples
lcpi aep protection protection_data.yml --type coup_belier
lcpi aep protection protection_data.yml --type verification
```

### **Hardy-Cross**
```bash
# Calcul Hardy-Cross
lcpi aep hardy-cross <fichier.yml> [options]

# Exemples
lcpi aep hardy-cross reseau_maille.yml --tolerance 1e-6 --iterations 100
lcpi aep hardy-cross reseau_maille.yml --formule hazen_williams --export resultats.json
```

### **Projet Complet**
```bash
# Analyse complète
lcpi aep project <fichier.yml> [options]

# Exemples
lcpi aep project projet_complet.yml --type complet
lcpi aep project projet_complet.yml --type comparatif
```

---

## 🔧 **CALCULS UNIFIÉS**

### **Population Unifiée**
```bash
# Projection démographique unifiée
lcpi aep population-unified <population> [options]

# Exemples
lcpi aep population-unified 1000 --taux 0.037 --annees 20
lcpi aep population-unified 5000 --methode arithmetique --annees 15 --verbose
```

### **Demande Unifiée**
```bash
# Calcul demande unifié
lcpi aep demand-unified <population> [options]

# Exemples
lcpi aep demand-unified 1000 --dotation 150 --coeff-pointe 1.5
lcpi aep demand-unified 2000 --type branchement_prive --verbose
```

### **Réseau Unifié**
```bash
# Dimensionnement réseau unifié
lcpi aep network-unified <debit_m3s> [options]

# Exemples
lcpi aep network-unified 0.1 --longueur 1000 --materiau fonte
lcpi aep network-unified 0.05 --perte-max 5.0 --methode manning --verbose
```

### **Réservoir Unifié**
```bash
# Dimensionnement réservoir unifié
lcpi aep reservoir-unified <volume_journalier_m3> [options]

# Exemples
lcpi aep reservoir-unified 1000 --adduction continue --forme cylindrique
lcpi aep reservoir-unified 500 --zone ville_francaise_peu_importante --verbose
```

### **Pompage Unifié**
```bash
# Dimensionnement pompage unifié
lcpi aep pumping-unified <debit_m3h> [options]

# Exemples
lcpi aep pumping-unified 100 --hmt 50 --type centrifuge
lcpi aep pumping-unified 200 --rendement 0.80 --verbose
```

---

## 🌐 **WORKFLOW COMPLET (NOUVEAU)**

### **Simulation Fichier .inp**
```bash
# Simuler directement un fichier .inp EPANET
lcpi aep simulate-inp <fichier.inp> [options]

# Exemples
lcpi aep simulate-inp mon_reseau.inp --format json
lcpi aep simulate-inp mon_reseau.inp --format markdown --verbose
lcpi aep simulate-inp mon_reseau.inp --format csv
```

### **Conversion .inp → YAML**
```bash
# Convertir .inp en YAML et simuler
lcpi aep convert-inp <fichier.inp> [options]

# Exemples
lcpi aep convert-inp mon_reseau.inp --simulate
lcpi aep convert-inp mon_reseau.inp --output reseau_converted.yml --simulate
lcpi aep convert-inp mon_reseau.inp --verbose
```

### **Diagnostic Réseau**
```bash
# Diagnostic de connectivité
lcpi aep diagnose-network <fichier.yml> [options]

# Exemples
lcpi aep diagnose-network mon_reseau.yml --verbose
lcpi aep diagnose-network mon_reseau.yml --format json
lcpi aep diagnose-network mon_reseau.yml --format markdown
```

### **Workflow Complet AEP**
```bash
# Workflow complet : diagnostic + Hardy-Cross + EPANET + comparaison + rapports
lcpi aep workflow-complete <fichier.yml> [options]

# Exemples
lcpi aep workflow-complete mon_reseau.yml --compare --reports
lcpi aep workflow-complete mon_reseau.yml --output ./resultats --verbose
lcpi aep workflow-complete mon_reseau.yml --no-compare --no-reports
```

---

## 📊 **BASE DE DONNÉES**

### **Requêtes**
```bash
# Interroger la base de données
lcpi aep query <type> [options]

# Exemples
lcpi aep query coefficients --format json
lcpi aep query materials --material fonte --format csv
lcpi aep query formulas --category perte_charge --verbose
```

### **Recherche**
```bash
# Recherche textuelle
lcpi aep search <terme> [options]

# Exemples
lcpi aep search coefficient --format json --verbose
lcpi aep search hazen --format markdown
```

### **Auto-complétion**
```bash
# Auto-complétion
lcpi aep autocomplete <requete> [options]

# Exemples
lcpi aep autocomplete coef --limit 5
lcpi aep autocomplete haz --limit 10
```

---

## ❓ **AIDE ET DOCUMENTATION**

### **Aide Générale**
```bash
# Aide générale AEP
lcpi aep help
```

### **Aide Spécifique**
```bash
# Aide par module
lcpi aep help-population
lcpi aep help-demand
lcpi aep help-network
lcpi aep help-reservoir
lcpi aep help-pumping
lcpi aep help-protection
lcpi aep help-hardy-cross

# Aide modules unifiés
lcpi aep help-population-unified
lcpi aep help-demand-unified
lcpi aep help-network-unified
lcpi aep help-reservoir-unified
lcpi aep help-pumping-unified
```

---

## 🎯 **EXEMPLES DE WORKFLOW COMPLET**

### **1. Simulation Simple d'un Fichier .inp**
```bash
# Simuler directement votre fichier .inp
lcpi aep simulate-inp votre_reseau.inp --verbose
```

### **2. Conversion et Simulation**
```bash
# Convertir .inp en YAML et simuler avec diagnostics
lcpi aep convert-inp votre_reseau.inp --simulate --verbose
```

### **3. Diagnostic d'un Réseau**
```bash
# Diagnostiquer la connectivité
lcpi aep diagnose-network votre_reseau.yml --verbose
```

### **4. Workflow Complet**
```bash
# Exécuter le workflow complet
lcpi aep workflow-complete votre_reseau.yml --compare --reports --verbose
```

---

## 📁 **FORMATS DE FICHIERS SUPPORTÉS**

### **Entrée**
- **YAML** : Format principal LCPI
- **JSON** : Format alternatif
- **CSV** : Pour Hardy-Cross
- **INP** : Fichiers EPANET

### **Sortie**
- **JSON** : Données structurées
- **Markdown** : Documentation
- **CSV** : Données tabulaires
- **HTML** : Rapports (via Pandoc)

---

## 🔧 **OPTIONS COMMUNES**

### **Options Générales**
- `--verbose, -v` : Afficher les détails
- `--format, -f` : Format de sortie (json, markdown, csv)
- `--output, -o` : Fichier/répertoire de sortie
- `--help, -h` : Afficher l'aide

### **Options Spécifiques**
- `--tolerance, -t` : Tolérance de convergence
- `--iterations, -i` : Nombre d'itérations
- `--simulate, -s` : Simuler après conversion
- `--compare, -c` : Comparer les méthodes
- `--reports, -r` : Générer les rapports

---

## ✅ **RÉPONSE FINALE**

**OUI, tout le workflow AEP fonctionne avec la commande `lcpi` !**

### **Commandes Manquantes Ajoutées :**
1. ✅ `lcpi aep simulate-inp` - Simulation directe fichiers .inp
2. ✅ `lcpi aep convert-inp` - Conversion .inp → YAML + simulation
3. ✅ `lcpi aep diagnose-network` - Diagnostic connectivité
4. ✅ `lcpi aep workflow-complete` - Workflow complet AEP

### **Workflow Complet Disponible :**
```bash
# 1. Diagnostic
lcpi aep diagnose-network reseau.yml

# 2. Hardy-Cross
lcpi aep hardy-cross reseau.yml

# 3. EPANET (via workflow)
lcpi aep workflow-complete reseau.yml

# 4. Ou simulation directe .inp
lcpi aep simulate-inp reseau.inp
```

**Toutes les fonctionnalités AEP sont maintenant accessibles via la commande `lcpi` !** 🎉 