# 🚀 Convertisseur CSV → YAML/SQLite pour Base de Données de Pompes

Outil de conversion automatique pour transformer votre base de données de pompes Grundfos depuis le format CSV vers YAML (pour les tests) et SQLite (pour la production).

## 📋 Fonctionnalités

- **🔄 Conversion automatique** CSV → YAML + SQLite
- **🧹 Nettoyage et validation** des données
- **📊 Parsing intelligent** des plages de valeurs (ex: "10-60" → min=10, max=60)
- **🗄️ Base SQLite optimisée** avec index et contraintes
- **📄 Format YAML structuré** avec métadonnées
- **📋 Rapports automatiques** en Markdown
- **🔍 Logging détaillé** pour le débogage
- **⚙️ Configuration flexible** via YAML

## 🛠️ Installation

### Prérequis
```bash
pip install pyyaml
```

### Fichiers inclus
- `csv_to_yaml_sqlite_converter.py` - Convertisseur principal
- `converter_config.yaml` - Configuration par défaut
- `test_converter.py` - Script de test
- `README_converter.md` - Cette documentation

## 🚀 Utilisation

### 1. Conversion complète (YAML + SQLite)
```bash
python csv_to_yaml_sqlite_converter.py grundfos_pompes_230_modeles_complet.csv
```

### 2. Conversion YAML uniquement
```bash
python csv_to_yaml_sqlite_converter.py grundfos_pompes_230_modeles_complet.csv --formats yaml
```

### 3. Conversion SQLite uniquement
```bash
python csv_to_yaml_sqlite_converter.py grundfos_pompes_230_modeles_complet.csv --formats sqlite
```

### 4. Dossier de sortie personnalisé
```bash
python csv_to_yaml_sqlite_converter.py grundfos_pompes_230_modeles_complet.csv --output ./ma_sortie
```

### 5. Mode verbeux
```bash
python csv_to_yaml_sqlite_converter.py grundfos_pompes_230_modeles_complet.csv --verbose
```

## 📁 Structure des fichiers de sortie

```
output/
├── grundfos_pompes_230_modeles_complet_converted.yaml  # Données YAML
├── grundfos_pompes_230_modeles_complet_pompes.db      # Base SQLite
├── conversion_report_20250827_235149.md                # Rapport de conversion
└── conversion.log                                      # Logs détaillés
```

## 🗄️ Structure de la base SQLite

### Table `pompes`
```sql
CREATE TABLE pompes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    designation TEXT UNIQUE NOT NULL,           -- Désignation unique
    marque TEXT,                               -- Marque (Grundfos)
    nom_produit TEXT,                          -- Nom du produit
    type_moteur TEXT,                          -- Type de moteur
    poids_net_kg REAL,                         -- Poids en kg
    debit_exploitation_m3h_min REAL,           -- Débit min (m³/h)
    debit_exploitation_m3h_max REAL,           -- Débit max (m³/h)
    diametre_moteur TEXT,                      -- Diamètre moteur
    hmt_min_m REAL,                            -- HMT min (m)
    hmt_max_m REAL,                            -- HMT max (m)
    frequence_hz INTEGER,                      -- Fréquence (Hz)
    tension_v TEXT,                            -- Tensions (JSON)
    intensite_nominale_a REAL,                 -- Intensités (JSON)
    puissance_p2_kw REAL,                      -- Puissance (kW)
    cos_phi REAL,                              -- Cos φ
    rendement_pompe_pct REAL,                  -- Rendement pompe (%)
    rendement_pompe_moteur_pct REAL,           -- Rendement total (%)
    materiaux TEXT,                            -- Matériaux
    classe_protection TEXT,                    -- Classe protection
    classe_isolation TEXT,                     -- Classe isolation
    temp_max_liquide_c REAL,                   -- Température max (°C)
    certification_eau_potable TEXT,            -- Certification
    courbe_hq_points TEXT,                     -- Courbe H(Q) (JSON)
    capex_estime_eur REAL,                     -- CAPEX estimé (€)
    opex_par_kwh_eur REAL,                     -- OPEX (€/kWh)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Index créés automatiquement
- `idx_designation` - Recherche par désignation
- `idx_marque` - Recherche par marque
- `idx_debit_range` - Recherche par plage de débit
- `idx_hmt_range` - Recherche par plage HMT
- `idx_capex` - Recherche par coût
- `idx_rendement` - Recherche par rendement

## 🔍 Exemples de requêtes SQLite

### 1. Trouver toutes les pompes Grundfos
```sql
SELECT designation, nom_produit, debit_exploitation_m3h_min, debit_exploitation_m3h_max
FROM pompes 
WHERE marque = 'Grundfos';
```

### 2. Pompes par plage de débit
```sql
SELECT designation, hmt_min_m, hmt_max_m, capex_estime_eur
FROM pompes 
WHERE debit_exploitation_m3h_min <= 5.0 
  AND debit_exploitation_m3h_max >= 5.0;
```

### 3. Pompes par plage HMT
```sql
SELECT designation, debit_exploitation_m3h_min, debit_exploitation_m3h_max
FROM pompes 
WHERE hmt_min_m <= 100 
  AND hmt_max_m >= 100;
```

### 4. Analyse des coûts
```sql
SELECT 
    marque,
    COUNT(*) as total_pompes,
    AVG(capex_estime_eur) as capex_moyen,
    AVG(opex_par_kwh_eur) as opex_moyen
FROM pompes 
GROUP BY marque;
```

### 5. Pompes les plus performantes
```sql
SELECT designation, rendement_pompe_moteur_pct, capex_estime_eur
FROM pompes 
WHERE rendement_pompe_moteur_pct > 70
ORDER BY rendement_pompe_moteur_pct DESC;
```

## 📊 Format YAML

### Structure
```yaml
metadata:
  source: "grundfos_pompes_230_modeles_complet.csv"
  conversion_date: "2025-08-27T23:51:49"
  total_pompes: 230
  format_version: "1.0"

pompes:
  - designation: "SP 1A-9"
    marque: "Grundfos"
    nom_produit: "SP 1A-9"
    type_moteur: "MS 402"
    poids_net_kg: 10.0
    debit_exploitation_m3h_min: 0.3
    debit_exploitation_m3h_max: 1.5
    hmt_min_m: 10.0
    hmt_max_m: 60.0
    # ... autres champs
```

## 🧪 Tests

### Test automatique
```bash
python test_converter.py
```

### Test manuel
```bash
# Créer un petit fichier de test
echo "Désignation,Marque" > test.csv
echo "TEST1,Grundfos" >> test.csv

# Tester la conversion
python csv_to_yaml_sqlite_converter.py test.csv --formats yaml
```

## ⚙️ Configuration

Modifiez `converter_config.yaml` pour personnaliser :
- Formats de sortie
- Validation des données
- Structure de la base SQLite
- Niveau de logging
- Génération des rapports

## 🔧 Personnalisation

### Ajouter de nouveaux champs
1. Modifiez `_clean_row()` dans `PumpDataConverter`
2. Ajoutez le champ au schéma SQLite
3. Mettez à jour la requête d'insertion

### Modifier la validation
1. Ajustez `_safe_float()` et `_safe_int()`
2. Modifiez les plages de valeurs dans la config
3. Ajoutez des contraintes personnalisées

## 📝 Logs et débogage

### Niveaux de log
- `DEBUG` - Détails complets
- `INFO` - Informations générales (défaut)
- `WARNING` - Avertissements
- `ERROR` - Erreurs

### Fichiers de log
- `conversion.log` - Logs détaillés
- Console - Affichage en temps réel

## 🚨 Gestion des erreurs

### Erreurs courantes
1. **Fichier CSV introuvable** - Vérifiez le chemin
2. **Encodage incorrect** - Utilisez UTF-8
3. **Données malformées** - Vérifiez le format CSV
4. **Permissions** - Vérifiez les droits d'écriture

### Solutions
- Utilisez `--verbose` pour plus de détails
- Consultez `conversion.log`
- Vérifiez le rapport de conversion

## 📈 Performance

### Optimisations incluses
- Index automatiques sur les champs de recherche
- Parsing par lot des données
- Gestion mémoire optimisée
- Transactions SQLite

### Temps de conversion estimé
- **230 pompes** : ~2-5 secondes
- **1000 pompes** : ~10-20 secondes
- **10000 pompes** : ~1-2 minutes

## 🤝 Contribution

### Améliorations possibles
- Support d'autres formats (JSON, XML)
- Validation avancée des données
- Interface graphique
- Intégration avec d'autres bases de données
- Tests unitaires complets

### Structure du code
- `PumpDataConverter` - Classe principale
- Méthodes de parsing spécialisées
- Gestion d'erreurs robuste
- Interface CLI flexible

## 📞 Support

### En cas de problème
1. Vérifiez les logs (`conversion.log`)
2. Consultez le rapport de conversion
3. Utilisez `--verbose` pour plus de détails
4. Testez avec `test_converter.py`

### Dépendances
- `csv` - Parsing CSV (standard)
- `yaml` - Génération YAML
- `sqlite3` - Base de données (standard)
- `pathlib` - Gestion des chemins (standard)

---

**🎯 Objectif** : Transformer votre base de données de pompes en formats optimisés pour les tests (YAML) et la production (SQLite) avec une validation automatique et des rapports détaillés.
