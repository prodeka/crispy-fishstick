# projet_cm

Projet d'ingénierie utilisant LCPI-CLI (Plateforme de Calcul Polyvalent pour l'Ingénierie).

## Structure du Projet

```
projet_cm/
├── data/           # Données d'entrée
├── output/         # Résultats de calculs
├── reports/        # Rapports générés
├── docs/           # Documentation
├── scripts/        # Scripts personnalisés
├── templates/      # Templates de rapports
└── config.yml      # Configuration du projet
```

## Plugins Actifs

- **cm**: Construction Métallique - Calculs selon Eurocode 3

## Utilisation

1. **Vérifier l'installation**:
   ```bash
   lcpi doctor
   ```

2. **Voir les exemples**:
   ```bash
   lcpi examples
   ```

3. **Lancer des calculs**:
   ```bash
   # Exemple pour cm
   lcpi cm --help
   ```

4. **Générer un rapport**:
   ```bash
   lcpi report .
   ```

## Documentation

- [Guide de démarrage rapide](docs/quick_start.md)
- [Exemples d'utilisation](docs/examples.md)
- [Configuration avancée](docs/configuration.md)
