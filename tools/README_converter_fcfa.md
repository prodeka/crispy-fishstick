# Convertisseur CSV → YAML/SQLite avec Support FCFA

## 🎯 Vue d'ensemble

Outil de conversion avancé pour transformer les données de pompes Grundfos depuis un format CSV vers YAML (pour tests) et SQLite (pour production), avec **support complet du franc CFA (FCFA)** et **conversion automatique des unités** pour EPANET.

## ✨ Nouvelles Fonctionnalités FCFA

### 💰 Conversion Monétaire Automatique
- **Conversion EUR → FCFA** avec taux configurable (défaut: 1 EUR = 655.957 FCFA)
- **Coûts en FCFA** pour CAPEX et OPEX
- **Taux de change personnalisable** via ligne de commande

### 🔄 Conversion des Unités
- **Débits m³/h → m³/s** automatique (divisé par 3600)
- **Compatible EPANET** et LCPI (unités standard)
- **Conservation des unités originales** et converties

### ⚡ Estimation OPEX Précise
- **Calcul de la puissance absorbée** : `P_abs = P2 / (η_global / 100)`
- **OPEX basé sur le coût local** de l'électricité (configurable)
- **Métriques d'efficacité énergétique** intégrées

## 🚀 Installation et Utilisation

### Prérequis
```bash
pip install pyyaml
```

### Utilisation Basique
```bash
# Conversion complète avec paramètres par défaut
python csv_to_yaml_sqlite_converter.py grundfos_pompes.csv

# Conversion avec taux de change personnalisé
python csv_to_yaml_sqlite_converter.py grundfos_pompes.csv --eur-fcfa 700

# Conversion avec coût électricité personnalisé
python csv_to_yaml_sqlite_converter.py grundfos_pompes.csv --energy-cost 100

# Conversion YAML uniquement
python csv_to_yaml_sqlite_converter.py grundfos_pompes.csv --formats yaml

# Conversion SQLite uniquement
python csv_to_yaml_sqlite_converter.py grundfos_pompes.csv --formats sqlite
```

### Paramètres de Configuration
- `--eur-fcfa`: Taux de change EUR → FCFA (défaut: 655.957)
- `--energy-cost`: Coût électricité en FCFA/kWh (défaut: 98.39)
- `--output`: Dossier de sortie (défaut: output)
- `--formats`: Formats de sortie (yaml, sqlite)
- `--verbose`: Mode verbeux

## 📊 Structure des Données

### Colonnes Ajoutées (FCFA)
```sql
-- Prix en FCFA
capex_estime_fcfa REAL,           -- CAPEX en FCFA
opex_par_kwh_fcfa REAL,           -- OPEX en FCFA/kWh
opex_estime_fcfa_kwh REAL,        -- OPEX estimé en FCFA/kWh

-- Débits convertis
debit_exploitation_m3s_min REAL,   -- Débit min en m³/s
debit_exploitation_m3s_max REAL,   -- Débit max en m³/s

-- Métriques énergétiques
puissance_absorbe_kw REAL,         -- Puissance absorbée en kW
```

### Exemple de Données
```yaml
designation: "SP 1A-9"
capex_estime_eur: 37.0
capex_estime_fcfa: 24270.41
debit_exploitation_m3h_min: 0.3
debit_exploitation_m3s_min: 0.000083
puissance_absorbe_kw: 0.88
opex_estime_fcfa_kwh: 86.58
```

## 🗄️ Base de Données SQLite

### Structure de la Table
```sql
CREATE TABLE pompes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    designation TEXT UNIQUE NOT NULL,
    marque TEXT,
    nom_produit TEXT,
    -- ... autres champs ...
    capex_estime_fcfa REAL,           -- NOUVEAU
    opex_estime_fcfa_kwh REAL,        -- NOUVEAU
    debit_exploitation_m3s_min REAL,  -- NOUVEAU
    debit_exploitation_m3s_max REAL,  -- NOUVEAU
    puissance_absorbe_kw REAL,        -- NOUVEAU
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Index de Performance
```sql
CREATE INDEX idx_capex_fcfa ON pompes(capex_estime_fcfa);
CREATE INDEX idx_opex_fcfa ON pompes(opex_estime_fcfa_kwh);
CREATE INDEX idx_debit_m3s ON pompes(debit_exploitation_m3s_min, debit_exploitation_m3s_max);
```

## 🔍 Exemples de Requêtes

### Recherche par Coût FCFA
```sql
-- Pompes économiques (< 50,000 FCFA)
SELECT designation, capex_estime_fcfa, rendement_pompe_moteur_pct
FROM pompes 
WHERE capex_estime_fcfa < 50000
ORDER BY capex_estime_fcfa ASC;
```

### Recherche par Plage de Débit
```sql
-- Pompes pour débit 0.5-2.0 m³/h
SELECT designation, debit_exploitation_m3s_min, debit_exploitation_m3s_max
FROM pompes 
WHERE debit_exploitation_m3s_min <= 0.000556  -- 2.0 m³/h / 3600
  AND debit_exploitation_m3s_max >= 0.000139; -- 0.5 m³/h / 3600
```

### Optimisation Coût/Rendement
```sql
-- Top 5 pompes optimisées
SELECT designation, 
       capex_estime_fcfa,
       rendement_pompe_moteur_pct,
       (capex_estime_fcfa / rendement_pompe_moteur_pct) as ratio
FROM pompes 
WHERE rendement_pompe_moteur_pct > 30
ORDER BY ratio ASC
LIMIT 5;
```

## 🧪 Tests et Validation

### Script de Test
```bash
python test_converter_fcfa.py
```

### Script de Démonstration
```bash
python demo_converter_fcfa.py
```

## 📈 Intégration avec LCPI

### Utilisation dans l'Optimisation
```python
from lcpi.aep.optimizer import PumpSelector

# Sélection de pompe avec coûts FCFA
selector = PumpSelector(db_path="pompes_converted.db")
pompe = selector.select_pump(
    debit_requis=0.001,  # m³/s
    hmt_requise=50,       # m
    budget_max=100000     # FCFA
)
```

### Métriques d'Optimisation
- **CAPEX en FCFA** pour les contraintes budgétaires
- **OPEX en FCFA/kWh** pour l'analyse des coûts d'exploitation
- **Débits en m³/s** pour la compatibilité EPANET

## 🌍 Contexte Africain

### Taux de Change Recommandés
- **BCEAO officiel**: 1 EUR = 655.957 FCFA
- **Sénégal**: ~655-660 FCFA
- **Côte d'Ivoire**: ~655-660 FCFA
- **Mali**: ~655-660 FCFA
- **Burkina Faso**: ~655-660 FCFA

### Coûts Électriques Typiques
- **Sénégal**: 85-95 FCFA/kWh
- **Côte d'Ivoire**: 90-100 FCFA/kWh
- **Mali**: 95-105 FCFA/kWh
- **Burkina Faso**: 90-100 FCFA/kWh

## 📁 Structure des Fichiers

```
output/
├── grundfos_pompes_230_modeles_complet_converted.yaml    # YAML avec FCFA
├── grundfos_pompes_230_modeles_complet_pompes.db        # SQLite avec FCFA
├── conversion_report_YYYYMMDD_HHMMSS.md                  # Rapport détaillé
└── conversion.log                                        # Logs de conversion
```

## 🔧 Configuration Avancée

### Fichier de Configuration
```yaml
# converter_config.yaml
conversion:
  eur_to_fcfa_rate: 655.957
  energy_cost_fcfa_kwh: 98.39

units:
  debit_conversion_factor: 3600
  debit_output_unit: "m³/s"
  prix_output_unit: "FCFA"
```

### Variables d'Environnement
```bash
export EUR_FCFA_RATE=655.957
export ENERGY_COST_FCFA_KWH=98.39
```

## 🚨 Dépannage

### Problèmes Courants
1. **Erreur de taux de change**: Vérifiez le paramètre `--eur-fcfa`
2. **Erreur de conversion débit**: Vérifiez que les débits sont numériques
3. **Erreur OPEX**: Vérifiez le paramètre `--energy-cost`

### Logs et Debug
```bash
python csv_to_yaml_sqlite_converter.py input.csv --verbose
```

## 📚 Références

- **BCEAO**: [Banque Centrale des États de l'Afrique de l'Ouest](https://www.bceao.int/)
- **EPANET**: [Documentation officielle](https://www.epa.gov/water-research/epanet)
- **LCPI**: Documentation du projet d'ingénierie des réseaux d'eau

## 🤝 Contribution

Pour contribuer ou signaler des problèmes :
1. Vérifiez les logs de conversion
2. Testez avec le script de test
3. Documentez les nouveaux cas d'usage

---

**Version**: 2.0  
**Dernière mise à jour**: 27 août 2025  
**Auteur**: LCPI Team  
**Licence**: Projet LCPI
