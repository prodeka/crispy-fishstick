# Template Projet AEP - Village

Ce template fournit une structure complète pour un projet d'Adduction d'Eau Potable (AEP) d'un village.

## 📁 Structure du Projet

```
village-aep/
├── README.md                 # Ce fichier
├── lcpi.yml                 # Configuration principale LCPI
├── data/                    # Données d'entrée
│   ├── population.yml      # Données démographiques
│   ├── demande.yml         # Besoins en eau
│   ├── reseau.yml          # Configuration du réseau
│   ├── reservoir.yml       # Dimensionnement réservoir
│   └── pompage.yml         # Configuration pompage
├── scenarios/               # Scénarios d'analyse
│   ├── base.yml            # Scénario de référence
│   ├── croissance.yml      # Scénario croissance forte
│   └── economique.yml      # Scénario économique
├── outputs/                 # Résultats et rapports
│   ├── logs/               # Journaux de calcul
│   ├── reports/            # Rapports générés
│   └── graphs/             # Graphiques et visualisations
└── docs/                    # Documentation technique
    ├── specifications.md    # Spécifications techniques
    └── plans.md            # Plans et schémas
```

## 🚀 Utilisation

1. **Créer le projet** :
   ```bash
   lcpi project create --template aep-village mon-village
   ```

2. **Analyser les scénarios** :
   ```bash
   lcpi aep network-analyze-scenarios scenarios/base.yml --solver lcpi --verbose
   ```

3. **Générer un rapport** :
   ```bash
   lcpi rapport generate --interactive
   ```

## 📊 Données d'Exemple

Le template inclut des données réalistes pour :
- **Population** : 1000 habitants avec croissance 2.5%/an
- **Demande** : 150 L/hab/j avec coefficient de pointe 1.8
- **Réseau** : 500m de conduites PVC
- **Réservoir** : 150 m³/jour, adduction continue
- **Pompage** : 10 m³/h, HMT 15m

## 🔧 Personnalisation

Modifiez les fichiers YAML dans `data/` pour adapter aux spécificités de votre projet :
- Ajustez la population et la croissance démographique
- Modifiez les dotations et coefficients de pointe
- Adaptez la géométrie du réseau
- Configurez les paramètres du réservoir et du pompage

## 📈 Scénarios Prédéfinis

1. **Base** : Configuration de référence
2. **Croissance** : Forte croissance démographique (3.5%/an)
3. **Économique** : Dotation réduite (120 L/hab/j)
4. **Performance** : Haute performance avec pompage optimisé
5. **Durable** : Approche durable avec énergies renouvelables

## 🎯 Résultats Attendus

- Dimensionnement optimal du réseau
- Capacité de stockage du réservoir
- Puissance et coût du pompage
- Comparaison des scénarios
- Rapports techniques complets

## 📚 Documentation

Consultez la documentation LCPI pour plus de détails sur :
- [Commandes AEP](../docs/aep-commands.md)
- [Format des fichiers YAML](../docs/yaml-format.md)
- [Génération de rapports](../docs/reporting.md)
