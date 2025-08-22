### Diagramme Algorithme genetique simple

``` mermaid
flowchart TD
  A[Demarrer la commande CLI] --> B[Controleur run optimization]
  B --> C[Charger le reseau et les contraintes]
  C --> D[Instancier optimiseur genetique]
  D --> E[Initialiser la population]
  E --> F[Pour generation de 0 a N moins un]
  F --> G[Evaluer chaque individu]
  G --> H[Realiser simulation hydraulique via EPANET WNTR]
  H --> I[Calculer cout CAPEX et penalites]
  I --> J[Calculer fitness]
  J --> K[Selection croisement mutation]
  K --> L[Construire nouvelle population]
  L --> F
  F --> M[Critere d arret verifie]
  M -- oui --> N[Post traitement et tri des propositions]
  N --> O[Fixer meta best cost et ecrire resultats]
  O --> P[Generer rapports et artefacts html pdf json csv]
  P --> Q[Fin]

```


### Diagramme Hybride genetique plus optimisation locale
``` mermaid
flowchart TD
  A[Demarrer la commande CLI] --> B[Controleur run optimization]
  B --> C[Charger reseau et config]
  C --> D[Instancier optimiseur genetique et refiner]
  D --> E[Initialiser population]
  E --> F[Pour generation de 0 a N moins un]
  F --> G[Evaluer population parallele ou serie]
  G --> H[Simulation EPANET par individu]
  H --> I[Calculer fitness a partir de CAPEX et metrics]
  I --> J[Selection croisement mutation]
  J --> K[Creer nouvelle population]
  K --> L[Si generation modulo periode egal zero]
  L -- oui --> M[Appeler refiner sur top k elites]
  M --> N[Intégrer solutions raffinees dans population]
  N --> F
  L -- non --> F
  F --> O[Apres generation finale
    appeler raffinements globaux]
  O --> P[Valider propositions via simulations rapides]
  P --> Q[Fixer meta best cost et emettre event best updated]
  Q --> R[Exporter artefacts json csv plots et rapports html pdf]
  R --> S[Fin]

```
