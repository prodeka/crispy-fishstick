# 📊 Guide Complet - Fonctionnalités CSV LCPI-CLI

## 📋 Vue d'ensemble

LCPI-CLI intègre désormais un système complet de gestion des fichiers CSV pour faciliter le traitement par lot et l'interopérabilité avec d'autres outils. Ce guide détaille toutes les fonctionnalités CSV disponibles.

---

## 🚀 **FONCTIONNALITÉS PRINCIPALES**

### **1. Conversion YAML ↔ CSV**
- **YAML → CSV** : Conversion de fichiers YAML en format CSV
- **CSV → YAML** : Conversion de fichiers CSV en format YAML
- **Détection automatique** du module selon le contenu
- **Validation** des données pendant la conversion

### **2. Traitement par Lot**
- **Traitement en masse** de plusieurs éléments
- **Parallélisation** des calculs
- **Gestion d'erreurs** robuste
- **Rapports détaillés** des résultats

### **3. Validation CSV**
- **Validation automatique** des données
- **Détection d'erreurs** et avertissements
- **Rapports de validation** détaillés
- **Support multi-modules**

### **4. Templates CSV**
- **Templates prédéfinis** pour chaque commande
- **Génération automatique** de fichiers d'exemple
- **Structure standardisée** par module

---

## 🔧 **UTILISATION DES COMMANDES CSV**

### **Commandes Générales**

#### **Conversion YAML ↔ CSV**
```bash
# Conversion YAML vers CSV
lcpi convert yaml-to-csv data.yml data.csv

# Conversion CSV vers YAML
lcpi convert csv-to-yaml data.csv data.yml

# Conversion avec module spécifique
lcpi convert yaml-to-csv data.yml data.csv --module cm
```

#### **Validation CSV**
```bash
# Validation automatique
lcpi convert validate-csv data.csv

# Validation avec module spécifique
lcpi convert validate-csv data.csv --module bois
```

#### **Génération de Templates**
```bash
# Template pour une commande spécifique
lcpi convert template-csv cm check-poteau

# Sauvegarder le template
lcpi convert template-csv cm check-poteau --output template.csv
```

### **Commandes par Module**

#### **Construction Métallique (CM)**
```bash
# Vérification de poteaux
lcpi cm csv check-poteau-csv data.csv --batch

# Vérification de poutres
lcpi cm csv check-deversement-csv data.csv --batch

# Optimisation de sections
lcpi cm csv optimize-section-csv data.csv --batch

# Templates
lcpi cm csv template-csv check-poteau
lcpi cm csv validate-csv data.csv
```

#### **Construction Bois**
```bash
# Vérification de poteaux
lcpi bois csv check-poteau-csv data.csv --batch

# Vérification de poutres
lcpi bois csv check-deversement-csv data.csv --batch

# Vérification d'assemblages
lcpi bois csv check-assemblage-pointe-csv data.csv --batch

# Templates
lcpi bois csv template-csv check-poteau
lcpi bois csv validate-csv data.csv
```

#### **Béton Armé**
```bash
# Calcul de poteaux
lcpi beton csv calc-poteau-csv data.csv --batch

# Calcul de radiers
lcpi beton csv calc-radier-csv data.csv --batch

# Templates
lcpi beton csv template-csv calc-poteau
lcpi beton csv validate-csv data.csv
```

#### **Hydraulique (Hydrodrain)**
```bash
# Dimensionnement d'ouvrages
lcpi hydro csv ouvrage-canal-csv data.csv --batch

# Dimensionnement de réservoirs
lcpi hydro csv reservoir-equilibrage-csv data.csv --batch

# Dimensionnement de collecteurs
lcpi hydro csv collector-dimensionner-troncons-csv data.csv --batch

# Templates
lcpi hydro csv template-csv ouvrage-canal
lcpi hydro csv validate-csv data.csv
```

---

## 📊 **FORMATS CSV PAR MODULE**

### **Construction Métallique (CM)**

#### **Poteaux**
```csv
element_id,type,section,longueur,charge_permanente,charge_exploitation,acier,statut
P1,poteau,HEA200,3.5,15.2,25.8,S235,conforme
P2,poteau,HEA240,4.2,18.5,30.2,S235,conforme
```

#### **Poutres**
```csv
element_id,type,section,longueur,charge_permanente,charge_exploitation,acier,statut
P1,poutre,IPE300,6.0,18.5,30.2,S235,conforme
P2,poutre,IPE400,8.0,25.2,40.5,S235,conforme
```

#### **Assemblages**
```csv
element_id,type,nombre_boulons,diametre_boulon,effort_cisaillement,acier,statut
A1,assemblage,8,M20,85.5,S235,conforme
A2,assemblage,12,M24,120.8,S235,conforme
```

### **Construction Bois**

#### **Poteaux**
```csv
element_id,type,section,longueur,essence,classe,charge_permanente,charge_exploitation,statut
P1,poteau,100x100,3.0,epicea,C24,8.5,12.3,conforme
P2,poteau,150x150,4.0,chene,D30,15.2,22.1,conforme
```

#### **Poutres**
```csv
element_id,type,section,longueur,essence,classe,charge_totale,statut
P1,poutre,200x400,6.0,chene,D30,25.2,conforme
P2,poutre,250x500,8.0,epicea,C24,35.8,conforme
```

#### **Assemblages**
```csv
element_id,type,nombre_pointes,diametre_pointe,effort_cisaillement,essence,statut
A1,assemblage,12,4.0,25.5,epicea,conforme
A2,assemblage,16,5.0,35.2,chene,conforme
```

### **Béton Armé**

#### **Poteaux**
```csv
element_id,type,section,hauteur,beton,acier,charge_permanente,charge_exploitation,statut
P1,poteau,30x30,3.0,C25,HA500,45.2,68.5,conforme
P2,poteau,40x40,4.0,C30,HA500,65.8,95.2,conforme
```

#### **Radiers**
```csv
element_id,type,epaisseur,largeur,longueur,beton,acier,charge_totale,statut
R1,radier,0.25,10.0,15.0,C25,HA500,120.5,conforme
R2,radier,0.30,12.0,18.0,C30,HA500,180.2,conforme
```

### **Hydraulique (Hydrodrain)**

#### **Canaux**
```csv
element_id,type,largeur,hauteur,debit,matiere,statut
C1,canal,2.5,1.8,5.0,beton,conforme
C2,canal,3.0,2.2,8.0,beton,conforme
```

#### **Réservoirs**
```csv
element_id,type,volume,hauteur,diametre,matiere,statut
R1,reservoir,1000,8.0,12.0,beton,conforme
R2,reservoir,2000,10.0,16.0,beton,conforme
```

#### **Collecteurs**
```csv
element_id,type,diametre,longueur,debit,pente,matiere,statut
T1,troncon,300,150,25.5,0.02,PVC,conforme
T2,troncon,400,200,35.8,0.025,PVC,conforme
```

---

## 🎯 **EXEMPLES D'UTILISATION**

### **Exemple 1 : Traitement par Lot de Poteaux CM**

1. **Créer le fichier CSV d'entrée** (`poteaux.csv`) :
```csv
element_id,type,section,longueur,charge_permanente,charge_exploitation,acier
P1,poteau,HEA200,3.5,15.2,25.8,S235
P2,poteau,HEA240,4.2,18.5,30.2,S235
P3,poteau,HEA300,5.0,22.8,35.5,S235
```

2. **Exécuter le traitement par lot** :
```bash
lcpi cm csv check-poteau-csv poteaux.csv --batch --output resultats.csv
```

3. **Vérifier les résultats** :
```bash
lcpi cm csv validate-csv resultats.csv
```

### **Exemple 2 : Conversion YAML ↔ CSV**

1. **Convertir un fichier YAML en CSV** :
```bash
lcpi convert yaml-to-csv poteau.yml poteau.csv
```

2. **Modifier le fichier CSV** dans Excel ou LibreOffice

3. **Convertir le CSV modifié en YAML** :
```bash
lcpi convert csv-to-yaml poteau_modifie.csv poteau_nouveau.yml
```

### **Exemple 3 : Génération de Templates**

1. **Générer un template pour poteaux bois** :
```bash
lcpi bois csv template-csv check-poteau --output template_poteaux_bois.csv
```

2. **Remplir le template** avec vos données

3. **Valider le fichier** :
```bash
lcpi bois csv validate-csv template_poteaux_bois.csv
```

---

## 🔍 **VALIDATION ET GESTION D'ERREURS**

### **Types de Validation**

#### **Validation de Base**
- **Présence des colonnes obligatoires**
- **Format des données** (nombres, textes)
- **Valeurs manquantes**

#### **Validation Spécifique par Module**
- **CM** : Types d'acier valides, sections normalisées
- **Bois** : Essences reconnues, classes de résistance
- **Béton** : Classes de béton, types d'acier
- **Hydro** : Débits positifs, pentes valides

### **Messages d'Erreur**

#### **Erreurs Critiques**
```
❌ Erreur: Ligne 3: element_id manquant
❌ Erreur: Ligne 5: section invalide (HEA999)
❌ Erreur: Ligne 7: acier non reconnu (S999)
```

#### **Avertissements**
```
⚠️ Avertissement: Ligne 2: charge_exploitation manquante
⚠️ Avertissement: Ligne 4: longueur très élevée (15.0m)
```

### **Rapports de Validation**

#### **Rapport de Succès**
```
✅ Fichier CSV valide (25 lignes)
  • Module détecté: cm
  • Aucune erreur trouvée
  • 2 avertissements
```

#### **Rapport d'Erreur**
```
❌ Fichier CSV invalide (25 lignes)
  • Module détecté: bois
  • 3 erreurs critiques
  • 1 avertissement
```

---

## 🚀 **SHELL INTERACTIF AVANCÉ**

### **Commandes CSV dans le Shell**

#### **Navigation et Variables**
```bash
# Définir des variables
set csv_file = "data/poteaux.csv"
set output_file = "results/resultats.csv"

# Utiliser les variables
lcpi cm csv check-poteau-csv $csv_file --output $output_file
```

#### **Commandes CSV Intégrées**
```bash
# Import CSV
csv import data.csv

# Export CSV
csv export results.csv

# Validation
csv validate data.csv

# Template
csv template cm check-poteau
```

#### **Calculs avec CSV**
```bash
# Calcul simple
calc cm check-poteau data.csv

# Calcul par lot
calc cm check-poteau data.csv --batch
```

### **Fonctionnalités Avancées du Shell**

#### **Auto-complétion**
- **Tab** pour compléter les commandes
- **Tab** pour compléter les noms de fichiers
- **Historique** des commandes

#### **Variables d'Environnement**
```bash
# Variables système
set PROJECT_DIR = "/path/to/project"
set TEMP_DIR = "/tmp/lcpi"

# Variables de configuration
set DEFAULT_MODULE = "cm"
set BATCH_SIZE = "100"
```

#### **Scripts et Automatisation**
```bash
# Exécuter un script
source script.lcpi

# Boucles et conditions
for file in *.csv; do
    lcpi cm csv validate-csv $file
done
```

---

## 📈 **PERFORMANCES ET OPTIMISATION**

### **Traitement par Lot**

#### **Parallélisation**
- **4 workers** par défaut (configurable)
- **Traitement simultané** des fichiers
- **Cache** des résultats pour éviter les recalculs

#### **Optimisations**
```bash
# Augmenter le nombre de workers
lcpi cm csv check-poteau-csv data.csv --batch --workers 8

# Désactiver le cache
lcpi cm csv check-poteau-csv data.csv --batch --no-cache

# Mode debug pour le profilage
lcpi cm csv check-poteau-csv data.csv --batch --debug
```

### **Gestion de la Mémoire**

#### **Fichiers Larges**
- **Traitement par chunks** pour les gros fichiers
- **Streaming** des données
- **Garbage collection** automatique

#### **Limitations**
- **Fichiers CSV** : jusqu'à 1 million de lignes
- **Mémoire** : 2 GB recommandés pour les gros fichiers
- **Temps** : ~1 seconde par 1000 éléments

---

## 🛠️ **DÉPANNAGE**

### **Problèmes Courants**

#### **Erreur de Conversion**
```
❌ Erreur lors de la conversion YAML → CSV: Module non détecté
```
**Solution** : Spécifier le module manuellement
```bash
lcpi convert yaml-to-csv data.yml data.csv --module cm
```

#### **Erreur de Validation**
```
❌ Erreur: Fichier CSV vide ou invalide
```
**Solution** : Vérifier le format du fichier
```bash
# Vérifier les premières lignes
head -5 data.csv

# Valider avec module spécifique
lcpi convert validate-csv data.csv --module cm
```

#### **Erreur de Traitement par Lot**
```
❌ Erreur lors du traitement par lot: Timeout
```
**Solution** : Réduire la taille du lot
```bash
lcpi cm csv check-poteau-csv data.csv --batch --chunk-size 100
```

### **Logs et Debug**

#### **Mode Debug**
```bash
# Activer le debug
lcpi cm csv check-poteau-csv data.csv --debug

# Logs détaillés
lcpi cm csv check-poteau-csv data.csv --verbose
```

#### **Fichiers de Log**
- **Logs** : `~/.lcpi/logs/csv_operations.log`
- **Cache** : `~/.lcpi/cache/csv_cache.pkl`
- **Templates** : `~/.lcpi/templates/csv/`

---

## 📚 **RESSOURCES ADDITIONNELLES**

### **Documentation**
- **Guide API** : `docs/API_DOCUMENTATION.md`
- **Exemples** : `examples/csv/`
- **Templates** : `src/lcpi/templates/csv/`

### **Outils Complémentaires**
- **Validateur en ligne** : Validation CSV en temps réel
- **Convertisseur web** : Interface web pour YAML ↔ CSV
- **Générateur de templates** : Création de templates personnalisés

### **Support**
- **FAQ** : Questions fréquentes
- **Forum** : Communauté d'utilisateurs
- **Issues** : Signalement de bugs

---

## 🎉 **CONCLUSION**

Les fonctionnalités CSV de LCPI-CLI offrent une solution complète pour :
- **Traitement par lot** efficace
- **Interopérabilité** avec d'autres outils
- **Validation** robuste des données
- **Automatisation** des workflows

Ces fonctionnalités facilitent l'intégration de LCPI-CLI dans des environnements de production et permettent une utilisation plus efficace pour les projets d'envergure. 