# test_canal

Projet créé avec le template LCPI **canal-simple**.

## Description

Dimensionnement de canal simple

## Structure du Projet

```
test_canal/
├── lcpi.yml          # Configuration du projet
├── data/             # Données d'entrée
├── output/           # Résultats et rapports
└── docs/             # Documentation
```

## Utilisation

1. **Activer le projet :**
   ```bash
   lcpi project switch test_canal
   ```

2. **Exécuter les calculs :**
   ```bash
   lcpi aep run data/network.yml
   ```

3. **Générer les rapports :**
   ```bash
   lcpi report generate
   ```

## Support

Pour plus d'informations, consultez la documentation LCPI.
