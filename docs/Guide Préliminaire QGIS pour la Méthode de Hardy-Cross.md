# Guide Préliminaire QGIS pour la Méthode de Hardy-Cross

> [!abstract] Objectif
> Préparer les données géométriques et attributaires d'un réseau hydraulique dans QGIS, y compris l'estimation initiale des débits et des sens d'écoulement, avant d'effectuer les calculs manuels de la méthode de Hardy-Cross (par exemple, dans un tableur).

---

## Phase 1 : Création et Structuration du Réseau dans QGIS

*   **Étape 1 : Tracer le Réseau**
    *   Créez deux couches vectorielles dans QGIS : une couche de points pour les **Nœuds** et une couche de lignes pour les **Conduites**.
    *   Digitalisez précisément le tracé des conduites, en connectant correctement aux nœuds (utiliser l'accrochage).
    *   Incluez les **Réservoirs** comme des nœuds spécifiques.
> [!tip] Outils QGIS
> Outils de numérisation, gestion des couches, options d'accrochage.

*   **Étape 2 : Identifier les Boucles**
    *   Repérez visuellement (ou via des outils d'analyse) les boucles fermées.
    *   Attribuez un identifiant unique à chaque boucle (ex: B1, B2...). Essentiel pour l'organisation des calculs.
> [!note] Peut être fait sur papier ou via une couche polygone de référence.

*   **Étape 3 : Définir les Zones d'Influence et le Sens d'Écoulement Initial (Hypothèse)**
    *   Identifiez les réservoirs (sources) et leurs niveaux piézométriques ($Z$). Distinguez les hauts et les bas.
    *   Esquissez mentalement des "zones d'influence".
    *   Hypothésez un sens d'écoulement logique pour **chaque conduite** :
        *   Globalement : Des réservoirs hauts vers les zones de demande et les réservoirs bas.
        *   Indiquez ce sens *supposé* (flèches sur carte de travail ou champ attributaire temporaire).

*   **Étape 4 : Placer et Identifier les Nœuds**
    *   Chaque jonction, extrémité, connexion réservoir doit être un point dans la couche Nœuds.
    *   Attribuez un **identifiant unique** à chaque nœud (ex: N1, N2..., champ numérique `id` ou `node_id`).
> [!tip] Auto-Incrémentation Optionnelle
> Pour faciliter l'attribution d'ID uniques aux nœuds, configurez une valeur par défaut auto-incrémentée.
> *   Voir guide : [[QGIS Configurer un ID AutoIncrémenté dans le Formulaire d'Attributs]]

---

## Phase 2 : Estimation Initiale des Débits et Données Conduites

*   **Étape 5 : Répartir les Débits Initiaux ($Q_{initial}$)**
    *   **Prérequis :** Avoir la demande d'eau ($Demande_{Noeud\_i}$) à chaque nœud.
    *   **Attribuez une valeur de débit initial ($Q_{initial}$)** à chaque conduite, selon le sens d'écoulement de l'Étape 3.
> [!important] Règle Impérative : Loi de Continuité
> Assurez-vous que la Loi de Continuité est respectée à **chaque nœud** :
> $$
 > \Sigma Q_{entrants\_au\_nœud} = \Sigma Q_{sortants\_du\_nœud} + Demande_{Noeud\_i}
 > $$
> *   C'est une étape d'estimation et d'équilibrage manuel rigoureuse.
*   Ajoutez un champ numérique (`q_initial`) à la table attributaire des Conduites et saisissez ces valeurs.
*   Voir principe : [[Guide détailler sur la méthode de Hardy-Cross]]

*   **Étape 5b : Choisir les Diamètres Initiaux ($D_{initial}$)**
    *   Pour chaque conduite, en fonction de $Q_{initial}$ et d'un critère de vitesse (ex: 1-1.5 m/s), choisissez un diamètre commercial standard.
    *   Ajoutez un champ (`diametre`) à la table attributaire des Conduites et saisissez ces valeurs.

*   **Étape 5c : Définir la Rugosité et la Longueur**
    *   Ajoutez un champ pour le coefficient de rugosité (ex: `C_HW`, `n_Manning`, ou `epsilon_DW`).
    *   Remplissez ce champ selon le matériau choisi.
    *   Assurez-vous d'avoir un champ pour la Longueur (`longueur`) de chaque conduite.

---

## Phase 3 : Préparation des Données pour Hardy-Cross

*   **Étape 6 : Identifier Nœuds Amont/Aval par Conduite**
    *   Pour chaque conduite, identifiez le nœud de départ (amont) et d'arrivée (aval) *selon le sens défini à l'Étape 3*.
> [!warning] Action Manuelle ou Spatiale
> Utilisez une jointure spatiale ou une analyse manuelle pour déterminer les ID de nœuds. Créez deux nouveaux champs dans la couche Conduites : `id_amont` et `id_aval`. Remplissez-les.
> *   Guide utile : [[Algorithme QGIS Joindre les attributs par localisation]] (peut nécessiter adaptation).

*   **Étape 7 : Nettoyer la Table Attributaire des Conduites**
    *   Supprimez les champs superflus.
    *   Vérifiez la cohérence et l'absence de valeurs nulles dans les champs essentiels (`id_amont`, `id_aval`, `q_initial`, `longueur`, `diametre`, `rugosite`).
> [!tip] Guide Détaillé
> Voir [[Étapes de Nettoyage de la Table Attributaire de la couche des conduites]] pour une méthode structurée.

*   **Étape 8 & 9 : Créer un Nom de Conduite Unique (Optionnel mais Recommandé)**
    *   **Objectif :** Faciliter le suivi dans les calculs manuels.
    *   Créez un nouveau champ texte (ex: `Nom_Conduite`).
    *   Utilisez la calculatrice de champs pour concaténer les ID amont et aval :

```qgis
-- Concatène 'N', l'ID amont, '_', 'N', et l'ID aval
'N' || "id_amont" || '_' || 'N' || "id_aval"
```

*   **Étape 10 : Exporter les Données par Boucle pour Calcul**
    *   Pour **chaque boucle** identifiée à l'Étape 2 :
        *   Sélectionnez les conduites de la boucle.
        *   Ouvrez la table attributaire des entités sélectionnées.
        *   Copiez/collez les données essentielles dans une feuille de calcul (Excel, Sheets...) dédiée à la boucle.
> [!important] Champs Essentiels à Exporter par Conduite :
> *   `Nom_Conduite` (ou ID unique)
> *   `q_initial` (Débit initial supposé)
> *   `longueur`
> *   `diametre`
> *   Coefficient de `rugosite` (selon formule choisie)
> *   (Optionnel: `id_amont`, `id_aval` pour référence)


---

## Suite : Calculs Hardy-Cross

> [!success] Prêt pour le Calcul
> Vous disposez maintenant, pour chaque boucle, des données organisées dans un tableur, prêtes pour l'application des calculs itératifs de la méthode de Hardy-Cross afin de déterminer les débits corrigés.

[[Guide détailler sur la méthode de Hardy-Cross]]
[[Guide Détaillé pour le Dimensionnement Manuel d'un Réseau de Distribution d'Eau Maillé avec Trois Réservoirs]]

|     |     |     |
| --- | --- | --- |

