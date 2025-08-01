# projet_templates_final

Projet d'ingénierie utilisant LCPI-CLI (Plateforme de Calcul Polyvalent pour l'Ingénierie).

## Structure du Projet

```
projet_templates_final/
├── data/           # Données d'entrée
├── output/         # Résultats de calculs
├── reports/        # Rapports générés
├── docs/           # Documentation
├── scripts/        # Scripts personnalisés
├── templates/      # Templates de rapports
└── config.yml      # Configuration du projet
```

## Plugins Actifs

- **beton**: Béton Armé - Calculs selon Eurocode 2
- **bois**: Construction Bois - Calculs selon Eurocode 5
- **cm**: Construction Métallique - Calculs selon Eurocode 3
- **db**: Plugin de calcul
- **hydrodrain**: Hydrologie et Assainissement - Dimensionnement d'ouvrages
- **shell**: Plugin de calcul
- **templates**: Plugin de calcul
- **templates_project**: Plugin de calcul

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
   # Exemple pour beton
   lcpi beton --help
   ```

4. **Générer un rapport**:
   ```bash
   lcpi report .
   ```

## Documentation

- [Guide de démarrage rapide](docs/quick_start.md)
- [Exemples d'utilisation](docs/examples.md)
- [Configuration avancée](docs/configuration.md)
