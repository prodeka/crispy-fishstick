# Implémentation de la classe PriceDB

## Vue d'ensemble

La classe `PriceDB` a été implémentée pour fournir une interface unifiée et robuste pour l'accès aux données de prix des diamètres et accessoires dans le projet LCPI. Cette classe remplace l'ancienne approche fragmentée et ajoute des mécanismes de fallback robustes.

## Localisation

- **Fichier source** : `src/lcpi/aep/optimizer/db.py`
- **Base de données principale** : `src/lcpi/db/aep_prices.db`
- **Branche git** : `feature/optimizer-unify`

## Architecture

### Hiérarchie des classes

```
PriceDB (Interface unifiée)
├── Validation de la base
├── Lecture SQLite
├── Lecture YAML
└── Fallback par défaut

DiameterDAO (Compatibilité)
└── Fallback simple

AEPPricesDAO (DAO existant)
└── Accès direct SQLite
```

### Mécanismes de fallback

1. **Niveau 1** : Base de données SQLite principale (`aep_prices.db`)
2. **Niveau 2** : Fichier YAML alternatif (si spécifié)
3. **Niveau 3** : Valeurs de fallback intégrées (9 diamètres standards)

## Fonctionnalités principales

### 1. Initialisation et validation

```python
from lcpi.aep.optimizer.db import PriceDB

# Utilisation du chemin par défaut
db = PriceDB()

# Utilisation d'un chemin personnalisé
db = PriceDB("/path/to/custom/aep_prices.db")

# Utilisation d'un fichier YAML
db = PriceDB("/path/to/diameters.yml")
```

### 2. Informations sur la base

```python
info = db.get_database_info()
print(f"Base: {info['path']}")
print(f"Type: {info['type']}")
print(f"Fallback utilisé: {info['fallback_used']}")
print(f"Checksum: {info['checksum']}")
print(f"Diamètres: {info['diameter_count']}")
```

### 3. Récupération des diamètres

```python
# Tous les diamètres
all_diameters = db.get_candidate_diameters()

# Diamètres d'un matériau spécifique
pvc_diameters = db.get_candidate_diameters("PVC-U")
pehd_diameters = db.get_candidate_diameters("PEHD")
```

### 4. Recherche de prix

```python
# Prix d'un diamètre spécifique
price = db.get_diameter_price(110)  # Prix du DN 110mm

# Diamètre le plus proche
closest = db.get_closest_diameter(115)  # Trouve le plus proche de 115mm
```

## Structure de la base de données

### Table `diameters`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER | Identifiant unique |
| `dn_mm` | INTEGER | Diamètre nominal en mm |
| `material` | TEXT | Matériau (PVC-U, PEHD, Fonte_dutile, etc.) |
| `supply_fcfa_per_m` | REAL | Prix de fourniture en FCFA/m |
| `pose_fcfa_per_m` | REAL | Prix de pose en FCFA/m |
| `total_fcfa_per_m` | REAL | Prix total en FCFA/m |
| `source_method` | TEXT | Méthode de source des données |

### Table `accessories`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER | Identifiant unique |
| `accessory_code` | TEXT | Code de l'accessoire |
| `dn_mm` | INTEGER | Diamètre nominal en mm |
| `material` | TEXT | Matériau |
| `fcfa_per_unit` | REAL | Prix unitaire en FCFA |

## Valeurs de fallback

Si la base de données n'est pas disponible, les valeurs suivantes sont utilisées :

```python
FALLBACK_DIAMETERS = [
    {"d_mm": 50, "cost_per_m": 5.0, "material": "PVC"},
    {"d_mm": 63, "cost_per_m": 7.5, "material": "PVC"},
    {"d_mm": 75, "cost_per_m": 10.0, "material": "PVC"},
    {"d_mm": 90, "cost_per_m": 15.0, "material": "PEHD"},
    {"d_mm": 110, "cost_per_m": 20.0, "material": "PEHD"},
    {"d_mm": 125, "cost_per_m": 25.0, "material": "PEHD"},
    {"d_mm": 140, "cost_per_m": 30.0, "material": "Fonte"},
    {"d_mm": 160, "cost_per_m": 35.0, "material": "Fonte"},
    {"d_mm": 200, "cost_per_m": 50.0, "material": "Fonte"},
]
```

## Gestion des erreurs

### Types d'erreurs gérées

1. **FileNotFoundError** : Base de données introuvable
2. **sqlite3.Error** : Erreurs de base SQLite
3. **yaml.YAMLError** : Erreurs de parsing YAML
4. **ValueError** : Structure de données invalide

### Stratégie de récupération

1. **Logging** : Toutes les erreurs sont loggées avec le module `logging`
2. **Fallback automatique** : Passage automatique aux valeurs de fallback
3. **Continuité de service** : L'application continue de fonctionner même en cas d'erreur

## Tests et validation

### Tests unitaires

- **Fichier de test** : `test_price_db_class.py`
- **Couverture** : Création, validation, lecture, fallback
- **Scénarios** : Base existante, base inexistante, erreurs de structure

### Tests d'intégration

- **Fichier de test** : `test_price_db_integration.py`
- **Couverture** : Intégration avec le DAO existant, compatibilité

## Migration depuis l'ancien code

### Ancien code

```python
# Approche fragmentée
from lcpi.aep.optimizer.db_dao import AEPPricesDAO
dao = AEPPricesDAO()
diameters = dao.get_available_diameters()
```

### Nouveau code

```python
# Interface unifiée
from lcpi.aep.optimizer.db import PriceDB
db = PriceDB()
diameters = db.get_candidate_diameters()
```

### Compatibilité

La classe `DiameterDAO` reste disponible pour la compatibilité avec l'ancien code.

## Configuration et déploiement

### Variables d'environnement

```bash
# Matériau par défaut
export AEP_MATERIAL="PVC-U"

# Chemin de la base de données
export AEP_PRICES_DB="/path/to/aep_prices.db"
```

### Fichiers de configuration

```yaml
# config.yml
aep:
  prices:
    db_path: "data/aep_prices.db"
    fallback_enabled: true
    logging_level: "INFO"
```

## Monitoring et observabilité

### Métriques disponibles

- **Taux d'utilisation de fallback** : `fallback_used`
- **Performance de lecture** : Temps de réponse des requêtes
- **Intégrité des données** : Checksum de la base
- **Couverture des diamètres** : Nombre de diamètres disponibles

### Logs

```python
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lcpi.aep.optimizer.db")

# Logs automatiques
# - Validation de la base
# - Utilisation de fallback
# - Erreurs de lecture
# - Recherche de diamètres proches
```

## Roadmap et améliorations

### Court terme (1-2 semaines)

- [ ] Tests de performance et benchmark
- [ ] Documentation des API
- [ ] Intégration avec le système de configuration

### Moyen terme (1-2 mois)

- [ ] Support des bases de données distantes
- [ ] Cache intelligent avec invalidation
- [ ] Synchronisation automatique des prix

### Long terme (3-6 mois)

- [ ] Interface web de gestion des prix
- [ ] Historique des modifications
- [ ] Intégration avec des APIs externes de prix

## Support et maintenance

### Contact

- **Développeur principal** : Équipe LCPI
- **Documentation** : Ce fichier et la documentation du projet
- **Issues** : Système de tickets du projet

### Procédures de maintenance

1. **Sauvegarde** : Sauvegarde automatique de `aep_prices.db`
2. **Validation** : Tests automatiques après modification
3. **Rollback** : Possibilité de revenir à une version précédente
4. **Monitoring** : Surveillance continue de l'intégrité des données

---

*Dernière mise à jour : $(date)*
*Version : 1.0.0*
*Branche : feature/optimizer-unify*
