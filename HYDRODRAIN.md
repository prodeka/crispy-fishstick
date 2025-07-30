Absolument. Voici une liste exhaustive et structurée de toutes les fonctionnalités de calcul et d'analyse qui peuvent être extraites de l'ensemble des documents fournis.

Cette liste est organisée par grand domaine d'application, en se concentrant sur les actions concrètes qu'un programme en ligne de commande pourrait exécuter.

---

### **Fonctionnalités du Programme `HydroDesign-CLI`**

#### **I. Gestion et Analyse des Données Pluviométriques**

1.  **Traitement des Données Brutes :**
    *   Importation de données pluviométriques depuis des fichiers (`.csv`, `.xlsx`).
    *   Analyse statistique descriptive des données de pluie pour une durée donnée (calcul du max, min, moyenne, médiane, écart-type, coefficient de variation).
    *   Génération d'histogrammes de précipitations mensuelles moyennes sur plusieurs années.

2.  **Analyse Fréquentielle des Pluies :**
    *   Ajustement des séries de pluies maximales à différentes lois de distribution statistique :
        *   Loi de Gumbel
        *   Loi Log-normale
        *   Loi GEV (Generalized Extreme Value)
    *   Calcul des paramètres spécifiques à chaque loi (ex: `u` et `α` pour Gumbel).
    *   Tests de validation de l'ajustement des lois :
        *   Test du Chi-deux (χ²) de Karl Pearson.
        *   Test d'Anderson-Darling.
    *   Comparaison et sélection de la meilleure loi d'ajustement via les critères :
        *   Critère d'information d'Akaike (AIC).
        *   Critère d'information bayésien (BIC).

3.  **Génération des Courbes Intensité-Durée-Fréquence (IDF) :**
    *   Calcul des quantiles de pluie pour différentes périodes de retour (2, 5, 10, 15, 20, 25, 30, 50, 100 ans).
    *   Modélisation et traçage des courbes IDF en utilisant les formules suivantes :
        *   Formule de **Montana** (`I = a * t^-b`)
        *   Formule de **Talbot** (`I = a / (b + t)`)
        *   Formule de **Keifer-Chu** (`I = a / (b + t)^c`)
        *   Formule de **Wanieslita** (formule générale à 4 paramètres)
    *   Calcul des coefficients (a, b, c) de chaque modèle pour différentes périodes de retour.
    *   Évaluation de la performance des modèles IDF via :
        *   Erreur Quadratique Moyenne (MSE).
        *   Coefficient de Corrélation (R).
    *   Comparaison graphique entre les courbes IDF de différentes études ou périodes.

#### **II. Analyse Hydrologique et Modélisation des Bassins Versants**

1.  **Délimitation et Caractérisation de Bassin Versant :**
    *   Délimitation automatique d'un bassin versant à partir d'un exutoire donné (nécessite un modèle numérique de terrain en entrée).
    *   Calcul des paramètres physiques d'un bassin versant :
        *   Superficie (S)
        *   Périmètre (P)
        *   Indice de compacité de Gravelius (Kc)
        *   Longueur et largeur du rectangle équivalent
        *   Indice global de pente (Ig)
        *   Dénivelée spécifique (Ds)

2.  **Estimation des Crues et Débits de Projet :**
    *   Calcul du temps de base (Tb) d'un ruissellement.
    *   Calcul de la lame d'eau ruisselée (Hr) et du volume d'eau ruisselé (Vr).
    *   Détermination du débit de pointe décennal et centennal en utilisant les méthodes suivantes :
        *   **Méthode Rationnelle** (pour les petits bassins).
        *   **Méthode ORSTOM** (incluant le calcul des coefficients d'abattement, de ruissellement et de pointe).
        *   **Méthode du C.I.E.H.** (utilisant des régressions multiples basées sur les paramètres du bassin).
        *   **Méthode du Gradex** pour l'extrapolation des crues.
    *   Application des coefficients de majoration pour passer du débit décennal au débit centennal.

#### **III. Dimensionnement et Analyse Hydraulique des Ouvrages**

1.  **Ouvrages de Franchissement (Ponts, Dalots) :**
    *   **Calcul du Niveau des Plus Hautes Eaux (PHE) :**
        *   Application de la formule de Manning-Strickler sur une section de cours d'eau.
        *   Détermination de la hauteur d'eau normale (hn) par itérations.
    *   **Estimation des Remous :**
        *   Calcul du remous à l'amont d'un ouvrage basé sur la méthode du Bureau of Public Roads (USA).
        *   Détermination des coefficients de contraction (M), d'obstruction (J) et des coefficients de base (Kb, Kp, Ke).
    *   **Calcul de l'Affouillement :**
        *   Estimation de l'affouillement général (formule de Lacy).
        *   Estimation de l'affouillement local autour des piles (formule de Breusers).
        *   Calcul de la profondeur totale d'affouillement.
    *   **Calage et Dimensionnement Final :**
        *   Détermination de la hauteur sous poutre (en incluant PHE, remous et tirant d'air).
        *   Détermination du débouché linéaire de l'ouvrage.
        *   Dimensionnement des protections contre l'affouillement (largeur et hauteur du tapis d'enrochement).

2.  **Réseaux d'Assainissement et de Plomberie :**
    *   **Calcul des Pertes de Charge :**
        *   Calcul des pertes de charge linéaires en utilisant les formules de Darcy-Weisbach, Manning-Strickler, et Hazen-Williams.
        *   Calcul des pertes de charge singulières.
    *   **Dimensionnement des Caniveaux et Conduites :**
        *   Calcul du débit de projet à évacuer par la méthode rationnelle.
        *   Dimensionnement de la section (rectangulaire, trapézoïdale) d'un caniveau ou d'une conduite.
        *   Vérification des vitesses d'écoulement et du régime (fluvial/torrentiel via le nombre de Froude).
    *   **Analyse de Réseaux :**
        *   Calcul des réseaux ramifiés.
        *   Résolution des réseaux maillés par la méthode de Hardy Cross.

3.  **Bassins de Rétention et Réservoirs :**
    *   **Analyse de la Réponse Hydrologique :**
        *   Calcul de l'intensité de pluie seuil (Is) qui remplit un bassin de rétention (pour un bassin vide ou à moitié plein).
        *   Comparaison de l'intensité seuil avec les courbes IDF pour déterminer la période de retour pour laquelle le bassin est efficace.
    *   **Dimensionnement de la Capacité :**
        *   Calcul du volume théorique d'un réservoir en fonction de la modulation de la demande journalière.

#### **IV. Utilitaires et Analyses Spécifiques**

1.  **Prévision de Population :**
    *   Estimation de l'évolution d'une population à court et long terme en utilisant :
        *   La méthode de progression arithmétique.
        *   La méthode de progression géométrique.
        *   La méthode du taux décroissant.
        *   La méthode logistique.

2.  **Estimation de la Demande en Eau :**
    *   Calcul des besoins en eau pour différents usages (domestique, public, commercial, industriel) sur la base de ratios.
    *   Estimation de la demande totale d'une agglomération.

3.  **Analyses Climatiques :**
    *   Génération de diagrammes ombrothermiques à partir de données de précipitation et de température.
    *   Calcul de l'amplitude thermique et détermination des mois "secs".