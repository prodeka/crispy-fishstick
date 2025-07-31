# Plan d'action : Implémentation des 7 fonctionnalités CLI pour lcpi cm et lcpi bois  
  
  
  
## Objectif  
  
Mettre en place 7 fonctionnalités CLI exploitant le fichier JSON de données techniques, accessibles via les commandes `lcpi cm` et `lcpi bois`.  
  
  
  
---  
  
  
  
## 1. Recherche de propriétés d’un matériau  
  
- **Commande** : `lcpi cm mat --type "Aciers doux"` ou `lcpi bois mat --essence "Chêne"`  
  
- **Étapes** :  
  
  - Lire le JSON  
  
  - Filtrer la catégorie matériaux/aciers/bois selon le type ou l’essence  
  
  - Afficher les propriétés (résistance, module, etc.)  
  
- **Test** : Vérifier l’affichage pour plusieurs types/essences  
  
  
  
## 2. Liste des poutrelles disponibles  
  
- **Commande** : `lcpi cm poutrelles --type IPE` ou `lcpi cm poutrelles --all`  
  
- **Étapes** :  
  
  - Lire la catégorie "Types de poutrelles"  
  
  - Filtrer ou lister toutes les désignations  
  
  - Afficher la plage de dimensions  
  
- **Test** : Vérifier la liste pour chaque type  
  
  
  
## 3. Recherche de charges permanentes ou d’exploitation  
  
- **Commande** : `lcpi cm charges --type "plancher"` ou `lcpi cm charges --usage "habitation"`  
  
- **Étapes** :  
  
  - Lire les catégories "Valeurs de quelques charges permanentes" et "Valeurs des charges d'exploitation"  
  
  - Filtrer selon le type ou l’usage  
  
  - Afficher la charge correspondante  
  
- **Test** : Vérifier pour plusieurs usages  
  
  
  
## 4. Génération d’un tableau récapitulatif  
  
- **Commande** : `lcpi cm tableau --categorie "Caractéristiques fondamentales des aciers E"`  
  
- **Étapes** :  
  
  - Lire la catégorie demandée  
  
  - Générer un tableau Markdown ou CSV  
  
  - Afficher ou sauvegarder le tableau  
  
- **Test** : Vérifier le format et le contenu  
  
  
  
## 5. Vérification de conformité  
  
- **Commande** : `lcpi cm verif --acier "E240" --sollicitation 200`  
  
- **Étapes** :  
  
  - Lire les propriétés de la nuance  
  
  - Comparer la sollicitation à la résistance  
  
  - Afficher conforme/non conforme  
  
- **Test** : Cas conforme et non conforme  
  
  
  
## 6. Ajout ou mise à jour d’une donnée  
  
- **Commande** : `lcpi cm add --categorie "charges" --designation "Nouveau plancher" --valeur 123`  
  
- **Étapes** :  
  
  - Ajouter ou modifier une entrée dans le JSON  
  
  - Sauvegarder le fichier  
  
  - Afficher confirmation  
  
- **Test** : Vérifier l’ajout et la persistance  
  
  
  
## 7. Export de données  
  
- **Commande** : `lcpi cm export --categorie "poutrelles" --format csv`  
  
- **Étapes** :  
  
  - Lire la catégorie  
  
  - Exporter au format demandé (CSV, JSON, etc.)  
  
  - Sauvegarder le fichier  
  
- **Test** : Vérifier le fichier exporté

