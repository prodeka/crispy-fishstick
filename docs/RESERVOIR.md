Le problème principal est que le fichier JSON que vous avez fourni est une concaténation de plusieurs objets JSON valides, mais un fichier JSON **doit contenir un seul et unique objet racine** (ou un tableau racine).

Actuellement, votre fichier se présente comme ceci :

```json
{ /* Objet 1 */ },
{ /* Objet 2 */ },
{ /* Objet 3 */ },
{ /* Objet 4 */ }
```

Ceci n'est pas un JSON valide. Pour le rendre valide, vous devez fusionner tous ces objets en un seul grand objet JSON. Chaque objet actuel deviendra une clé/valeur au sein de cet objet global.

Voici comment je vais reformater votre JSON pour le rendre valide :

1.  **Créer un objet racine vide `{}`**.
2.  **Déplacer chaque objet existant** (par exemple, `"specifications_tubes"`, `"hazen_williams_coefficients"`, `"pms_en_fonction_de_pn"`, `"profils_consommation"`, `"parametres_calcul"`, `"criteres_choix_reservoirs"`, `"equipements_reservoirs"`, `"dotations_domestiques"`, etc.) à l'intérieur de cet objet racine.
3.  **Donner une clé unique et descriptive** à chaque objet que vous déplacez (par exemple, `diametres_specifications`, `coeffs_hazen_williams`, `pressions_maximales_services`, etc.).
4.  **Ajouter une virgule `,`** après chaque paire clé-valeur, sauf la dernière dans l'objet racine.

Cela va transformer vos multiples objets en une structure unique et valide.

---

```json
{
  "diametres_specifications": {
    "specifications_tubes": [
      {
        "D_theo_min_mm": 2,
        "Diametre_Nominal_DN": 6,
        "Pouce": "1/8\"",
        "Diametre_Exterieur_Moyen_mm": 6.00,
        "Diametre_Interieur_Approximatif_mm": 5,
        "epaisseur_mm": 1.00
      },
      {
        "D_theo_min_mm": 6,
        "Diametre_Nominal_DN": 8,
        "Pouce": "1/4\"",
        "Diametre_Exterieur_Moyen_mm": 8,
        "Diametre_Interieur_Approximatif_mm": 8,
        "epaisseur_mm": 0.00
      },
      {
        "D_theo_min_mm": 8,
        "Diametre_Nominal_DN": 10,
        "Pouce": "3/8\"",
        "Diametre_Exterieur_Moyen_mm": 10,
        "Diametre_Interieur_Approximatif_mm": 9,
        "epaisseur_mm": 1.00
      },
      {
        "D_theo_min_mm": 10,
        "Diametre_Nominal_DN": 15,
        "Pouce": "1/2\"",
        "Diametre_Exterieur_Moyen_mm": 21,
        "Diametre_Interieur_Approximatif_mm": 15,
        "epaisseur_mm": 6.00
      },
      {
        "D_theo_min_mm": 15,
        "Diametre_Nominal_DN": 20,
        "Pouce": "3/4\"",
        "Diametre_Exterieur_Moyen_mm": 27,
        "Diametre_Interieur_Approximatif_mm": 20,
        "epaisseur_mm": 7.00
      },
      {
        "D_theo_min_mm": 20,
        "Diametre_Nominal_DN": 25,
        "Pouce": "1\"",
        "Diametre_Exterieur_Moyen_mm": 34,
        "Diametre_Interieur_Approximatif_mm": 25,
        "epaisseur_mm": 9.00
      },
      {
        "D_theo_min_mm": 25,
        "Diametre_Nominal_DN": 32,
        "Pouce": "1 1/4\"",
        "Diametre_Exterieur_Moyen_mm": 42,
        "Diametre_Interieur_Approximatif_mm": 33,
        "epaisseur_mm": 9.00
      },
      {
        "D_theo_min_mm": 32,
        "Diametre_Nominal_DN": 40,
        "Pouce": "1 1/2\"",
        "Diametre_Exterieur_Moyen_mm": 50,
        "Diametre_Interieur_Approximatif_mm": 40,
        "epaisseur_mm": 10.00
      },
      {
        "D_theo_min_mm": 40,
        "Diametre_Nominal_DN": 50,
        "Pouce": "2\"",
        "Diametre_Exterieur_Moyen_mm": 63,
        "Diametre_Interieur_Approximatif_mm": 51,
        "epaisseur_mm": 12.00
      },
      {
        "D_theo_min_mm": 50,
        "Diametre_Nominal_DN": 65,
        "Pouce": "2 1/2\"",
        "Diametre_Exterieur_Moyen_mm": 76,
        "Diametre_Interieur_Approximatif_mm": 67,
        "epaisseur_mm": 9.00
      },
      {
        "D_theo_min_mm": 65,
        "Diametre_Nominal_DN": 80,
        "Pouce": "3\"",
        "Diametre_Exterieur_Moyen_mm": 89,
        "Diametre_Interieur_Approximatif_mm": 77,
        "epaisseur_mm": 12.00
      },
      {
        "D_theo_min_mm": 80,
        "Diametre_Nominal_DN": 100,
        "Pouce": "4\"",
        "Diametre_Exterieur_Moyen_mm": 114,
        "Diametre_Interieur_Approximatif_mm": 100,
        "epaisseur_mm": 14.00
      },
      {
        "D_theo_min_mm": 100,
        "Diametre_Nominal_DN": 125,
        "Pouce": "5\"",
        "Diametre_Exterieur_Moyen_mm": 140,
        "Diametre_Interieur_Approximatif_mm": 125,
        "epaisseur_mm": 15.00
      },
      {
        "D_theo_min_mm": 125,
        "Diametre_Nominal_DN": 150,
        "Pouce": "6\"",
        "Diametre_Exterieur_Moyen_mm": 168,
        "Diametre_Interieur_Approximatif_mm": 150,
        "epaisseur_mm": 18.00
      },
      {
        "D_theo_min_mm": 150,
        "Diametre_Nominal_DN": 200,
        "Pouce": "8\"",
        "Diametre_Exterieur_Moyen_mm": 219,
        "Diametre_Interieur_Approximatif_mm": 200,
        "epaisseur_mm": 19.00
      },
      {
        "D_theo_min_mm": 200,
        "Diametre_Nominal_DN": 250,
        "Pouce": "10\"",
        "Diametre_Exterieur_Moyen_mm": 273,
        "Diametre_Interieur_Approximatif_mm": 250,
        "epaisseur_mm": 23.00
      },
      {
        "D_theo_min_mm": 250,
        "Diametre_Nominal_DN": 300,
        "Pouce": "12\"",
        "Diametre_Exterieur_Moyen_mm": 325,
        "Diametre_Interieur_Approximatif_mm": 300,
        "epaisseur_mm": 25.00
      },
      {
        "D_theo_min_mm": 300,
        "Diametre_Nominal_DN": 350,
        "Pouce": "14\"",
        "Diametre_Exterieur_Moyen_mm": 377,
        "Diametre_Interieur_Approximatif_mm": 350,
        "epaisseur_mm": 27.00
      },
      {
        "D_theo_min_mm": 350,
        "Diametre_Nominal_DN": 400,
        "Pouce": "16\"",
        "Diametre_Exterieur_Moyen_mm": 426,
        "Diametre_Interieur_Approximatif_mm": 400,
        "epaisseur_mm": 26.00
      },
      {
        "D_theo_min_mm": 400,
        "Diametre_Nominal_DN": 450,
        "Pouce": "18\"",
        "Diametre_Exterieur_Moyen_mm": 470,
        "Diametre_Interieur_Approximatif_mm": 421,
        "epaisseur_mm": 49.00
      },
      {
        "D_theo_min_mm": 450,
        "Diametre_Nominal_DN": 500,
        "Pouce": "20\"",
        "Diametre_Exterieur_Moyen_mm": 520,
        "Diametre_Interieur_Approximatif_mm": 466,
        "epaisseur_mm": 54.00
      },
      {
        "D_theo_min_mm": 500,
        "Diametre_Nominal_DN": 600,
        "Pouce": "24\"",
        "Diametre_Exterieur_Moyen_mm": 630,
        "Diametre_Interieur_Approximatif_mm": 565,
        "epaisseur_mm": 65.00
      },
      {
        "D_theo_min_mm": 600,
        "Diametre_Nominal_DN": 700,
        "Pouce": "24\"",
        "Diametre_Exterieur_Moyen_mm": 610,
        "Diametre_Interieur_Approximatif_mm": 600,
        "epaisseur_mm": 10.00
      },
      {
        "D_theo_min_mm": 700,
        "Diametre_Nominal_DN": 800,
        "Pouce": "28\"",
        "Diametre_Exterieur_Moyen_mm": 711,
        "Diametre_Interieur_Approximatif_mm": 700,
        "epaisseur_mm": 11.00
      },
      {
        "D_theo_min_mm": 800,
        "Diametre_Nominal_DN": 900,
        "Pouce": "32\"",
        "Diametre_Exterieur_Moyen_mm": 813,
        "Diametre_Interieur_Approximatif_mm": 800,
        "epaisseur_mm": 13.00
      },
      {
        "D_theo_min_mm": 900,
        "Diametre_Nominal_DN": 1000,
        "Pouce": "36\"",
        "Diametre_Exterieur_Moyen_mm": 914,
        "Diametre_Interieur_Approximatif_mm": 900,
        "epaisseur_mm": 14.00
      },
      {
        "D_theo_min_mm": 9,
        "Diametre_Nominal_DN": 13,
        "Pouce": "3/8\"",
        "Diametre_Exterieur_Moyen_mm": 18,
        "Diametre_Interieur_Approximatif_mm": 13,
        "epaisseur_mm": 1.5
      },
      {
        "D_theo_min_mm": 13,
        "Diametre_Nominal_DN": 16,
        "Pouce": "1/2\"",
        "Diametre_Exterieur_Moyen_mm": 22,
        "Diametre_Interieur_Approximatif_mm": 16,
        "epaisseur_mm": 1.5
      },
      {
        "D_theo_min_mm": 16,
        "Diametre_Nominal_DN": 20,
        "Pouce": "3/4\"",
        "Diametre_Exterieur_Moyen_mm": 26,
        "Diametre_Interieur_Approximatif_mm": 20,
        "epaisseur_mm": 1.5
      },
      {
        "D_theo_min_mm": 20,
        "Diametre_Nominal_DN": 25,
        "Pouce": "1\"",
        "Diametre_Exterieur_Moyen_mm": 32,
        "Diametre_Interieur_Approximatif_mm": 25,
        "epaisseur_mm": 1.9
      },
      {
        "D_theo_min_mm": 25,
        "Diametre_Nominal_DN": 30,
        "Pouce": "1 1/4\"",
        "Diametre_Exterieur_Moyen_mm": 38,
        "Diametre_Interieur_Approximatif_mm": 31,
        "epaisseur_mm": 1.9
      },
      {
        "D_theo_min_mm": 30,
        "Diametre_Nominal_DN": 40,
        "Pouce": "1 1/2\"",
        "Diametre_Exterieur_Moyen_mm": 48,
        "Diametre_Interieur_Approximatif_mm": 40,
        "epaisseur_mm": 1.9
      },
      {
        "D_theo_min_mm": 40,
        "Diametre_Nominal_DN": 42,
        "Pouce": null,
        "Diametre_Exterieur_Moyen_mm": 48,
        "Diametre_Interieur_Approximatif_mm": 42,
        "epaisseur_mm": 2
      },
      {
        "D_theo_min_mm": 42,
        "Diametre_Nominal_DN": 50,
        "Pouce": "2\"",
        "Diametre_Exterieur_Moyen_mm": 60,
        "Diametre_Interieur_Approximatif_mm": 51,
        "epaisseur_mm": 2.4
      },
      {
        "D_theo_min_mm": 50,
        "Diametre_Nominal_DN": 63,
        "Pouce": null,
        "Diametre_Exterieur_Moyen_mm": 76,
        "Diametre_Interieur_Approximatif_mm": 59.2,
        "epaisseur_mm": 3
      },
      {
        "D_theo_min_mm": 63,
        "Diametre_Nominal_DN": 65,
        "Pouce": "2 1/2\"",
        "Diametre_Exterieur_Moyen_mm": 76,
        "Diametre_Interieur_Approximatif_mm": 67,
        "epaisseur_mm": 3
      },
      {
        "D_theo_min_mm": 65,
        "Diametre_Nominal_DN": 75,
        "Pouce": null,
        "Diametre_Exterieur_Moyen_mm": 89,
        "Diametre_Interieur_Approximatif_mm": 70.6,
        "epaisseur_mm": 3.6
      },
      {
        "D_theo_min_mm": 75,
        "Diametre_Nominal_DN": 80,
        "Pouce": "3\"",
        "Diametre_Exterieur_Moyen_mm": 89,
        "Diametre_Interieur_Approximatif_mm": 77,
        "epaisseur_mm": 3.8
      },
      {
        "D_theo_min_mm": 80,
        "Diametre_Nominal_DN": 90,
        "Pouce": null,
        "Diametre_Exterieur_Moyen_mm": 114,
        "Diametre_Interieur_Approximatif_mm": 84.6,
        "epaisseur_mm": 4.3
      },
      {
        "D_theo_min_mm": 90,
        "Diametre_Nominal_DN": 100,
        "Pouce": "4\"",
        "Diametre_Exterieur_Moyen_mm": 114,
        "Diametre_Interieur_Approximatif_mm": 100,
        "epaisseur_mm": 4.3
      },
      {
        "D_theo_min_mm": 100,
        "Diametre_Nominal_DN": 110,
        "Pouce": null,
        "Diametre_Exterieur_Moyen_mm": 129,
        "Diametre_Interieur_Approximatif_mm": 103.6,
        "epaisseur_mm": 4.8
      },
      {
        "D_theo_min_mm": 110,
        "Diametre_Nominal_DN": 125,
        "Pouce": "5\"",
        "Diametre_Exterieur_Moyen_mm": 140,
        "Diametre_Interieur_Approximatif_mm": 125,
        "epaisseur_mm": 5.4
      },
      {
        "D_theo_min_mm": 125,
        "Diametre_Nominal_DN": 130,
        "Pouce": null,
        "Diametre_Exterieur_Moyen_mm": 168,
        "Diametre_Interieur_Approximatif_mm": 131.8,
        "epaisseur_mm": 5.4
      },
      {
        "D_theo_min_mm": 130,
        "Diametre_Nominal_DN": 140,
        "Pouce": null,
        "Diametre_Exterieur_Moyen_mm": 168,
        "Diametre_Interieur_Approximatif_mm": 137.8,
        "epaisseur_mm": 6.2
      },
      {
        "D_theo_min_mm": 140,
        "Diametre_Nominal_DN": 150,
        "Pouce": "6\"",
        "Diametre_Exterieur_Moyen_mm": 165,
        "Diametre_Interieur_Approximatif_mm": 146,
        "epaisseur_mm": 6.2
      },
      {
        "D_theo_min_mm": 150,
        "Diametre_Nominal_DN": 160,
        "Pouce": null,
        "Diametre_Exterieur_Moyen_mm": 182,
        "Diametre_Interieur_Approximatif_mm": 150.6,
        "epaisseur_mm": 6.2
      },
      {
        "D_theo_min_mm": 160,
        "Diametre_Nominal_DN": 200,
        "Pouce": "8\"",
        "Diametre_Exterieur_Moyen_mm": 216,
        "Diametre_Interieur_Approximatif_mm": 194,
        "epaisseur_mm": 7.7
      },
      {
        "D_theo_min_mm": 200,
        "Diametre_Nominal_DN": 250,
        "Pouce": "10\"",
        "Diametre_Exterieur_Moyen_mm": 267,
        "Diametre_Interieur_Approximatif_mm": 239,
        "epaisseur_mm": 9.6
      },
      {
        "D_theo_min_mm": 250,
        "Diametre_Nominal_DN": 300,
        "Pouce": "12\"",
        "Diametre_Exterieur_Moyen_mm": 318,
        "Diametre_Interieur_Approximatif_mm": 284,
        "epaisseur_mm": 11.5
      },
      {
        "D_theo_min_mm": 300,
        "Diametre_Nominal_DN": 350,
        "Pouce": "14\"",
        "Diametre_Exterieur_Moyen_mm": 370,
        "Diametre_Interieur_Approximatif_mm": 332,
        "epaisseur_mm": 13.4
      },
      {
        "D_theo_min_mm": 350,
        "Diametre_Nominal_DN": 400,
        "Pouce": "16\"",
        "Diametre_Exterieur_Moyen_mm": 420,
        "Diametre_Interieur_Approximatif_mm": 376,
        "epaisseur_mm": 15.3
      },
      {
        "D_theo_min_mm": 400,
        "Diametre_Nominal_DN": 450,
        "Pouce": "18\"",
        "Diametre_Exterieur_Moyen_mm": 470,
        "Diametre_Interieur_Approximatif_mm": 421,
        "epaisseur_mm": 17.2
      },
      {
        "D_theo_min_mm": 450,
        "Diametre_Nominal_DN": 500,
        "Pouce": "20\"",
        "Diametre_Exterieur_Moyen_mm": 520,
        "Diametre_Interieur_Approximatif_mm": 466,
        "epaisseur_mm": 19.2
      },
      {
        "D_theo_min_mm": 500,
        "Diametre_Nominal_DN": 600,
        "Pouce": "24\"",
        "Diametre_Exterieur_Moyen_mm": 630,
        "Diametre_Interieur_Approximatif_mm": 565,
        "epaisseur_mm": 22.7
      }
    ]
  },
  "coeffs_hazen_williams": {
    "hazen_williams_coefficients": [
      {
        "Materiau": "PVC / Matière plastique",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": 150,
        "Remarques": "Neuf, valeur standard élevée"
      },
      {
        "Materiau": "Polyéthylène (PEHD)",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": 150,
        "Remarques": "Neuf"
      },
      {
        "Materiau": "Cuivre",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": "140 - 150",
        "Remarques": "Selon source"
      },
      {
        "Materiau": "Verre",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": 140,
        "Remarques": ""
      },
      {
        "Materiau": "Acier inoxydable",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": 140,
        "Remarques": "Neuf"
      },
      {
        "Materiau": "Béton (centrifugé)",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": 140,
        "Remarques": "Neuf"
      },
      {
        "Materiau": "Béton, brique",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": "100 - 110",
        "Remarques": "Selon état"
      },
      {
        "Materiau": "Fonte non revêtue",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": "100 - 130",
        "Remarques": "130 neuf, 100 vieux (20 ans+)"
      },
      {
        "Materiau": "Fonte asphaltée",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": 130,
        "Remarques": ""
      },
      {
        "Materiau": "Acier riveté",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": 120,
        "Remarques": ""
      },
      {
        "Materiau": "Acier",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": 120,
        "Remarques": ""
      },
      {
        "Materiau": "Bois",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": 120,
        "Remarques": ""
      },
      {
        "Materiau": "Plomb",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": 130,
        "Remarques": ""
      },
      {
        "Materiau": "Étain",
        "Coefficient_de_rugosite_Hazen_Williams_C_ou_Ch": 130,
        "Remarques": ""
      }
    ]
  },
  "hazen_williams_vieillissement": {
    "hazen_williams_vieillissement": [
      {
        "Materiau": "PVC ou PEHD",
        "Neuf_Ch": 150,
        "Vieux_20_ans_ou_plus_Ch": 135
      },
      {
        "Materiau": "Béton centrifugé",
        "Neuf_Ch": 140,
        "Vieux_20_ans_ou_plus_Ch": 130
      },
      {
        "Materiau": "Fonte non revêtue",
        "Neuf_Ch": 130,
        "Vieux_20_ans_ou_plus_Ch": 100
      },
      {
        "Materiau": "Acier inoxydable",
        "Neuf_Ch": 140,
        "Vieux_20_ans_ou_plus_Ch": 130
      }
    ]
  },
  "manning_roughness_coefficients": {
    "manning_roughness_coef": [
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Ciment lissé",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,010 à 0,013"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Mortier de ciment",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,011 à 0,015"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Aqueducs en bois raboté",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,010 à 0,014"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Aqueducs en bois non raboté",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,011 à 0,015"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Canaux revêtus de béton",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,012 à 0,018"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Moëllons bruts",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,017 à 0,030"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Pierres sèches",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,025 à 0,035"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Moëllons dressés",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,013 à 0,017"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Aqueducs métalliques (section demi-circulaire lisse)",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,011 à 0,015"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Aqueducs métalliques (section demi-circulaire plissée)",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,0225 à 0,030"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Canaux en terre droits et uniformes",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,017 à 0,025"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Canaux avec pierres lisses et uniformes",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,025 à 0,035"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Canaux avec pierres rugueux et irréguliers",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,035 à 0,045"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Canaux en terre à larges méandres",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,0225 à 0,030"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Canaux en terre dragués",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,025 à 0,033"
      },
      {
        "Categorie": "Canaux artificiels",
        "Nature_de_la_surface_Type_de_canal": "Canaux à fond en terre, côtés avec pierres",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,028 à 0,035"
      },
      {
        "Categorie": "Cours d'eau naturels",
        "Nature_de_la_surface_Type_de_canal": "Propres, rives en ligne droite",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,025 à 0,033"
      },
      {
        "Categorie": "Cours d'eau naturels",
        "Nature_de_la_surface_Type_de_canal": "Avec quelques herbes et pierres",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,030 à 0,040"
      },
      {
        "Categorie": "Cours d'eau naturels",
        "Nature_de_la_surface_Type_de_canal": "Avec méandres, étangs, endroits peu profonds, propres",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,035 à 0,050"
      },
      {
        "Categorie": "Cours d'eau naturels",
        "Nature_de_la_surface_Type_de_canal": "Même conditions que ci-dessus, eau à l’étiage, pente faible",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,040 à 0,055"
      },
      {
        "Categorie": "Cours d'eau naturels",
        "Nature_de_la_surface_Type_de_canal": "Avec quelques herbes et pierres",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,033 à 0,045"
      },
      {
        "Categorie": "Cours d'eau naturels",
        "Nature_de_la_surface_Type_de_canal": "Avec pierres",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,045 à 0,060"
      },
      {
        "Categorie": "Cours d'eau naturels",
        "Nature_de_la_surface_Type_de_canal": "Zones à eau coulant lentement avec herbes ou fosses profondes",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,050 à 0,080"
      },
      {
        "Categorie": "Cours d'eau naturels",
        "Nature_de_la_surface_Type_de_canal": "Zones avec beaucoup de mauvaises herbes",
        "Etat_Rugosite": "Parfait à Mauvais",
        "Coefficient_n_de_Manning_valeurs_typiques": "0,075 à 0,150"
      }
    ]
  },
  "manning_roughness_coef_materiaux": {
    "manning_roughness_coef_materiaux": [
      {
        "Materiau_de_la_conduite_canal": "PVC (Polychlorure de Vinyle)",
        "Etat_Revetement": "Neuf, lisse",
        "Valeur_typique_de_n": "0,009 – 0,011",
        "Plage_courante_approximative": "0,009 – 0,013"
      },
      {
        "Materiau_de_la_conduite_canal": "PEHD (Polyéthylène Haute Densité)",
        "Etat_Revetement": "Neuf, lisse",
        "Valeur_typique_de_n": "0,009 – 0,011",
        "Plage_courante_approximative": "0,009 – 0,013"
      },
      {
        "Materiau_de_la_conduite_canal": "Fonte ductile",
        "Etat_Revetement": "Revêtement ciment neuf",
        "Valeur_typique_de_n": "0,011 – 0,013",
        "Plage_courante_approximative": "0,010 – 0,014"
      },
      {
        "Materiau_de_la_conduite_canal": "Fonte ductile",
        "Etat_Revetement": "Sans revêtement / ancien",
        "Valeur_typique_de_n": "0,014 – 0,018+",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Acier",
        "Etat_Revetement": "Neuf, lisse / revêtu",
        "Valeur_typique_de_n": "0,010 – 0,012",
        "Plage_courante_approximative": "0,009 – 0,014"
      },
      {
        "Materiau_de_la_conduite_canal": "Acier",
        "Etat_Revetement": "Sans revêtement / ancien",
        "Valeur_typique_de_n": "0,013 – 0,017+",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Béton",
        "Etat_Revetement": "Lisse, bien fini",
        "Valeur_typique_de_n": "0,011 – 0,013",
        "Plage_courante_approximative": "0,010 – 0,015"
      },
      {
        "Materiau_de_la_conduite_canal": "Béton",
        "Etat_Revetement": "Brut, usé",
        "Valeur_typique_de_n": "0,014 – 0,017",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Amiante-Ciment",
        "Etat_Revetement": "Neuf",
        "Valeur_typique_de_n": "0,010 – 0,011",
        "Plage_courante_approximative": "0,010 – 0,012"
      },
      {
        "Materiau_de_la_conduite_canal": "Amiante-Ciment",
        "Etat_Revetement": "Ancien",
        "Valeur_typique_de_n": "0,011 – 0,015",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Grès (canalisations gravitaires)",
        "Etat_Revetement": "Vitrifié, bons joints",
        "Valeur_typique_de_n": "0,011 – 0,013",
        "Plage_courante_approximative": "0,011 – 0,015"
      },
      {
        "Materiau_de_la_conduite_canal": "Grès (canalisations gravitaires)",
        "Etat_Revetement": "Joints dégradés",
        "Valeur_typique_de_n": "0,014 – 0,017",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Caniveaux / Chenaux en béton",
        "Etat_Revetement": "Lisse",
        "Valeur_typique_de_n": "0,012 – 0,014",
        "Plage_courante_approximative": "0,011 – 0,016"
      },
      {
        "Materiau_de_la_conduite_canal": "Caniveaux / Chenaux en béton",
        "Etat_Revetement": "Avec débris, rugueux",
        "Valeur_typique_de_n": "0,015 – 0,020+",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Canaux en terre",
        "Etat_Revetement": "Propres, droits",
        "Valeur_typique_de_n": "0,018 – 0,025",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Canaux en terre",
        "Etat_Revetement": "Végétation, sinueux",
        "Valeur_typique_de_n": "0,025 – 0,040+",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Canaux revêtus béton (général)",
        "Etat_Revetement": "Parfait à mauvais état",
        "Valeur_typique_de_n": "0,012 – 0,018",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Moëllons bruts",
        "Etat_Revetement": "Parfait à mauvais état",
        "Valeur_typique_de_n": "0,017 – 0,030",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Pierres sèches",
        "Etat_Revetement": "Parfait à mauvais état",
        "Valeur_typique_de_n": "0,025 – 0,035",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Aqueducs métalliques lisses",
        "Etat_Revetement": "Parfait à mauvais état",
        "Valeur_typique_de_n": "0,011 – 0,015",
        "Plage_courante_approximative": ""
      },
      {
        "Materiau_de_la_conduite_canal": "Aqueducs métalliques plissés",
        "Etat_Revetement": "Parfait à mauvais état",
        "Valeur_typique_de_n": "0,0225 – 0,030",
        "Plage_courante_approximative": ""
      }
    ]
  },
  "pn10_sdr21_dimensions": {
    "pn10_sdr21_dimensions": [
      {
        "DN_mm": 20,
        "Diametre_Exterieur_DE_Typique_mm": 20,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 1,
        "Diametre_Interieur_DI_Estime_mm": 18
      },
      {
        "DN_mm": 25,
        "Diametre_Exterieur_DE_Typique_mm": 25,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 1.2,
        "Diametre_Interieur_DI_Estime_mm": 22.6
      },
      {
        "DN_mm": 32,
        "Diametre_Exterieur_DE_Typique_mm": 32,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 1.6,
        "Diametre_Interieur_DI_Estime_mm": 28.8
      },
      {
        "DN_mm": 40,
        "Diametre_Exterieur_DE_Typique_mm": 40,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 1.9,
        "Diametre_Interieur_DI_Estime_mm": 36.2
      },
      {
        "DN_mm": 50,
        "Diametre_Exterieur_DE_Typique_mm": 50,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 2.4,
        "Diametre_Interieur_DI_Estime_mm": 45.2
      },
      {
        "DN_mm": 63,
        "Diametre_Exterieur_DE_Typique_mm": 63,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 3,
        "Diametre_Interieur_DI_Estime_mm": 57
      },
      {
        "DN_mm": 75,
        "Diametre_Exterieur_DE_Typique_mm": 75,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 3.6,
        "Diametre_Interieur_DI_Estime_mm": 67.8
      },
      {
        "DN_mm": 90,
        "Diametre_Exterieur_DE_Typique_mm": 90,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 4.3,
        "Diametre_Interieur_DI_Estime_mm": 81.4
      },
      {
        "DN_mm": 110,
        "Diametre_Exterieur_DE_Typique_mm": 110,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 5.3,
        "Diametre_Interieur_DI_Estime_mm": 99.4
      },
      {
        "DN_mm": 125,
        "Diametre_Exterieur_DE_Typique_mm": 125,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 6,
        "Diametre_Interieur_DI_Estime_mm": 113
      },
      {
        "DN_mm": 140,
        "Diametre_Exterieur_DE_Typique_mm": 140,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 6.7,
        "Diametre_Interieur_DI_Estime_mm": 126.6
      },
      {
        "DN_mm": 160,
        "Diametre_Exterieur_DE_Typique_mm": 160,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 7.7,
        "Diametre_Interieur_DI_Estime_mm": 144.6
      },
      {
        "DN_mm": 180,
        "Diametre_Exterieur_DE_Typique_mm": 180,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 8.6,
        "Diametre_Interieur_DI_Estime_mm": 162.8
      },
      {
        "DN_mm": 200,
        "Diametre_Exterieur_DE_Typique_mm": 200,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 9.6,
        "Diametre_Interieur_DI_Estime_mm": 180.8
      },
      {
        "DN_mm": 225,
        "Diametre_Exterieur_DE_Typique_mm": 225,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 10.8,
        "Diametre_Interieur_DI_Estime_mm": 203.4
      },
      {
        "DN_mm": 250,
        "Diametre_Exterieur_DE_Typique_mm": 250,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 11.9,
        "Diametre_Interieur_DI_Estime_mm": 226.2
      },
      {
        "DN_mm": 280,
        "Diametre_Exterieur_DE_Typique_mm": 280,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 13.4,
        "Diametre_Interieur_DI_Estime_mm": 253.2
      },
      {
        "DN_mm": 315,
        "Diametre_Exterieur_DE_Typique_mm": 315,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 15,
        "Diametre_Interieur_DI_Estime_mm": 285
      },
      {
        "DN_mm": 355,
        "Diametre_Exterieur_DE_Typique_mm": 355,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 16.9,
        "Diametre_Interieur_DI_Estime_mm": 321.2
      },
      {
        "DN_mm": 400,
        "Diametre_Exterieur_DE_Typique_mm": 400,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 19.1,
        "Diametre_Interieur_DI_Estime_mm": 361.8
      },
      {
        "DN_mm": 450,
        "Diametre_Exterieur_DE_Typique_mm": 450,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 21.5,
        "Diametre_Interieur_DI_Estime_mm": 407
      },
      {
        "DN_mm": 500,
        "Diametre_Exterieur_DE_Typique_mm": 500,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 23.9,
        "Diametre_Interieur_DI_Estime_mm": 452.2
      },
      {
        "DN_mm": 560,
        "Diametre_Exterieur_DE_Typique_mm": 560,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 26.7,
        "Diametre_Interieur_DI_Estime_mm": 506.6
      },
      {
        "DN_mm": 630,
        "Diametre_Exterieur_DE_Typique_mm": 630,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 30,
        "Diametre_Interieur_DI_Estime_mm": 570
      },
      {
        "DN_mm": 710,
        "Diametre_Exterieur_DE_Typique_mm": 710,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 33.9,
        "Diametre_Interieur_DI_Estime_mm": 642.2
      },
      {
        "DN_mm": 800,
        "Diametre_Exterieur_DE_Typique_mm": 800,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 38.1,
        "Diametre_Interieur_DI_Estime_mm": 723.8
      },
      {
        "DN_mm": 900,
        "Diametre_Exterieur_DE_Typique_mm": 900,
        "Epaisseur_Estimee_e_pour_PN10_SDR21_mm": 42.9,
        "Diametre_Interieur_DI_Estime_mm": 814.2
      }
    ]
  },
  "pms_en_fonction_de_pn": {
    "pms_en_fonction_de_pn": [
      {
        "Application": "Conduite de l'eau destinée à l'alimentation humaine",
        "Details": [
          {
            "Type": "Adduction gravitaire",
            "Type_d_assemblage": "Collage ou bague d'étanchéité",
            "Action_corrosive_fluide_vehicule": "S",
            "Conditions": [
              {
                "TMS": "≤ 25°C",
                "PN_25": 25,
                "PN_16": 16,
                "PN_10": 10,
                "PN_6": 6
              },
              {
                "TMS": "≤ 40°C",
                "PN_25": 16,
                "PN_16": 10,
                "PN_10": 6,
                "PN_6": 4
              }
            ]
          },
          {
            "Type": "Adduction par refoulement",
            "Type_d_assemblage": "Bague d'étanchéité",
            "Action_corrosive_fluide_vehicule": "S",
            "Conditions": [
              {
                "TMS": "≤ 25°C",
                "PN_25": 25,
                "PN_16": 16,
                "PN_10": 10,
                "PN_6": 6
              },
              {
                "TMS": "≤ 40°C",
                "PN_25": 16,
                "PN_16": 10,
                "PN_10": 6,
                "PN_6": 4
              }
            ]
          },
          {
            "Type": "Branchement",
            "Type_d_assemblage": "Collage",
            "Action_corrosive_fluide_vehicule": "S",
            "Conditions": [
              {
                "TMS": "≤ 25°C",
                "PN_25": 16,
                "PN_16": 10,
                "PN_10": 6,
                "PN_6": 4
              },
              {
                "TMS": "≤ 40°C",
                "PN_25": 10,
                "PN_16": 6,
                "PN_10": 4,
                "PN_6": 2.5
              }
            ]
          },
          {
            "Type": "Distribution à l'intérieur des bâtiments",
            "Type_d_assemblage": "Collage ou bague d'étanchéité",
            "Action_corrosive_fluide_vehicule": "S",
            "Conditions": [
              {
                "TMS": "≤ 25°C",
                "PN_25": 16,
                "PN_16": 10,
                "PN_10": 6,
                "PN_6": 4
              },
              {
                "TMS": "≤ 40°C",
                "PN_25": 10,
                "PN_16": 6,
                "PN_10": 4,
                "PN_6": 2.5
              }
            ]
          }
        ]
      },
      {
        "Application": "Evacuation sous pression des eaux usées",
        "Details": [
          {
            "Type": "refoulement",
            "Type_d_assemblage": "Collage ou bague d'étanchéité",
            "Action_corrosive_fluide_vehicule": "S",
            "Conditions": [
              {
                "TMS": "≤ 25°C",
                "PN_25": 25,
                "PN_16": 16,
                "PN_10": 10,
                "PN_6": 6
              },
              {
                "TMS": "≤ 40°C",
                "PN_25": 16,
                "PN_16": 10,
                "PN_10": 6,
                "PN_6": 4
              }
            ]
          }
        ]
      },
      {
        "Application": "Conduite de liquides alimentaires, eaux thermales et liquides industriels",
        "Details": [
          {
            "Type": "Refoulement",
            "Type_d_assemblage": "Bague d'étanchéité",
            "Conditions": [
              {
                "Action_corrosive_fluide_vehicule": "S",
                "TMS": "≤ 25°C",
                "PN_25": 16,
                "PN_16": 10,
                "PN_10": 6,
                "PN_6": 4
              },
              {
                "Action_corrosive_fluide_vehicule": "S",
                "TMS": "≤ 40°C",
                "PN_25": 10,
                "PN_16": 6,
                "PN_10": 4,
                "PN_6": 2.5
              },
              {
                "Action_corrosive_fluide_vehicule": "S",
                "TMS": "≤ 60°C",
                "PN_25": 6,
                "PN_16": 4,
                "PN_10": 2.5,
                "PN_6": "-"
              },
              {
                "Action_corrosive_fluide_vehicule": "L",
                "TMS": "≤ 25°C",
                "PN_25": 10,
                "PN_16": 6,
                "PN_10": 4,
                "PN_6": 2.5
              },
              {
                "Action_corrosive_fluide_vehicule": "L",
                "TMS": "≤ 40°C",
                "PN_25": 6,
                "PN_16": 4,
                "PN_10": 2.5,
                "PN_6": "-"
              }
            ]
          },
          {
            "Type": "Refoulement",
            "Type_d_assemblage": "collage",
            "Conditions": [
              {
                "Action_corrosive_fluide_vehicule": "S",
                "TMS": "≤ 25°C",
                "PN_25": 10,
                "PN_16": 6,
                "PN_10": 4,
                "PN_6": 2.5
              },
              {
                "Action_corrosive_fluide_vehicule": "S",
                "TMS": "≤ 40°C",
                "PN_25": 6,
                "PN_16": 4,
                "PN_10": 2.5,
                "PN_6": "-"
              },
              {
                "Action_corrosive_fluide_vehicule": "S",
                "TMS": "≤ 60°C",
                "PN_25": 4,
                "PN_16": 2.5,
                "PN_10": "-",
                "PN_6": "-"
              },
              {
                "Action_corrosive_fluide_vehicule": "L",
                "TMS": "≤ 25°C",
                "PN_25": 6,
                "PN_16": 4,
                "PN_10": 2.5,
                "PN_6": "-"
              },
              {
                "Action_corrosive_fluide_vehicule": "L",
                "TMS": "≤ 40°C",
                "PN_25": 4,
                "PN_16": 2.5,
                "PN_10": "-",
                "PN_6": "-"
              }
            ]
          }
        ]
      }
    ]
  },
  "profils_consommation": {
    "ville_francaise_peu_importante": {
      "description": "Profil de consommation typique pour une petite ville française.",
      "repartition": [
        { "debut": 0, "fin": 6, "coefficient": 0.125 },
        { "debut": 6, "fin": 7, "coefficient": 1.0 },
        { "debut": 7, "fin": 11, "coefficient": 3.5 },
        { "debut": 11, "fin": 16, "coefficient": 0.4 },
        { "debut": 16, "fin": 18, "coefficient": 2.0 },
        { "debut": 18, "fin": 22, "coefficient": 0.5 },
        { "debut": 22, "fin": 24, "coefficient": 0.125 }
      ]
    },
    "standard_urbain_lisse": {
      "description": "Un profil urbain plus générique et lissé pour la modélisation.",
      "repartition": [
        { "debut": 0, "fin": 5, "coefficient": 0.4 },
        { "debut": 5, "fin": 9, "coefficient": 1.5 },
        { "debut": 9, "fin": 11, "coefficient": 1.2 },
        { "debut": 11, "fin": 14, "coefficient": 1.4 },
        { "debut": 14, "fin": 18, "coefficient": 1.1 },
        { "debut": 18, "fin": 22, "coefficient": 1.6 },
        { "debut": 22, "fin": 24, "coefficient": 0.8 }
      ]
    }
  },
  "parametres_calcul": {
    "hauteur_volume_mort_m": 0.20,
    "facteur_reserve_incendie_par_debit_moyen": 12,
    "description_reserve_incendie": "La réserve incendie est fixée à 12 fois le débit moyen horaire 'a', soit l'équivalent de 2 heures de consommation à un débit de 6a."
  },
  "criteres_choix_reservoirs": [
    {
      "critere": "Économie - Investissement",
      "Reservoir_au_sol": 3,
      "Reservoir_sureleve": 1,
      "Reservoir_avec_contre-pression_d_air": 2,
      "Reservoir_au_sol_avec_station_de_surpression": 1
    },
    {
      "critere": "Économie - Fonctionnement",
      "Reservoir_au_sol": 3,
      "Reservoir_sureleve": 3,
      "Reservoir_avec_contre-pression_d_air": 2,
      "Reservoir_au_sol_avec_station_de_surpression": 1
    },
    {
      "critere": "Sécurité d'approvisionnement",
      "Reservoir_au_sol": 3,
      "Reservoir_sureleve": 3,
      "Reservoir_avec_contre-pression_d_air": 1,
      "Reservoir_au_sol_avec_station_de_surpression": 2
    },
    {
      "critere": "Facilité d'exploitation",
      "Reservoir_au_sol": 3,
      "Reservoir_sureleve": 2,
      "Reservoir_avec_contre-pression_d_air": 2,
      "Reservoir_au_sol_avec_station_de_surpression": 2
    },
    {
      "critere": "Possibilité d'adaptation au réseau",
      "Reservoir_au_sol": 1,
      "Reservoir_sureleve": 1,
      "Reservoir_avec_contre-pression_d_air": 3,
      "Reservoir_au_sol_avec_station_de_surpression": 3
    },
    {
      "critere": "Inscription dans le site",
      "Reservoir_au_sol": 3,
      "Reservoir_sureleve": 1,
      "Reservoir_avec_contre-pression_d_air": 3,
      "Reservoir_au_sol_avec_station_de_surpression": 3
    }
  ],
  "equipements_reservoirs": {
    "Hydraulique": [
      "Vannes diverses",
      "Clapet",
      "Equipement de trop plein",
      "Vidange",
      "Siphon pour réserve incendie",
      "Canalisation de liaison",
      "Compteur",
      "Clapet à rentrée d'air",
      "Purgeur d'air"
    ],
    "Exploitation": [
      "Niveau",
      "Débit",
      "Equipement de télétransmission",
      "Télécommande",
      "Poste de livraison électrique"
    ],
    "Entretien": [
      "Appareil de manutention",
      "Appareil de montage",
      "Eclairage",
      "Trappes de visite pour le personnel et le matériel"
    ],
    "Nettoyage": [
      "Trappes de visite pour le personnel et le matériel",
      "Equipements spéciaux pour le nettoyage",
      "Pompe d'alimentation en eau"
    ],
    "Qualite_de_l_eau": [
      "Equipements ou dispositions pour le renouvellement de l'eau",
      "Equipements ou dispositions pour le renouvellement de l'air",
      "Robinet de prélèvement",
      "Equipements de désinfection, analyseurs",
      "Dispositifs de protection contre les actes de malveillance et les intrusions"
    ],
    "Securite_lors_des_interventions": [
      "Passerelle",
      "Echelle à crinoline",
      "Garde-corps",
      "Ancrages pour harnais de sécurité",
      "Eclairage"
    ],
    "Divers": [
      "Suivant les réservoirs : compresseur d'air",
      "Protection thermique des équipements",
      "Alarmes diverses"
    ]
  },
  "dotations_et_consommations": {
    "dotations_domestiques": {
      "par_pays_litre_jour_habitant": [
        {
          "pays": "G.B",
          "boisson_cuisine": 4.6,
          "lavage_vaisselle": 13.7,
          "lavage_linge": 13.7,
          "hygiene": 45.5,
          "wc": 49.9,
          "divers": 4.6,
          "total": 132
        },
        {
          "pays": "Belgique",
          "boisson_cuisine": 4,
          "lavage_vaisselle": 11,
          "lavage_linge": {"min": 11, "max": 20},
          "hygiene": 38,
          "wc": 42,
          "divers": 22,
          "total": {"min": 128, "max": 146}
        },
        {
          "pays": "R.F.A",
          "boisson_cuisine": {"min": 3, "max": 6},
          "lavage_vaisselle": 4,
          "lavage_linge": {"min": 20, "max": 40},
          "hygiene": {"min": 30, "max": 55},
          "wc": {"min": 20, "max": 40},
          "divers": {"min": 26, "max": 30},
          "total": {"min": 100, "max": 170}
        },
        {
          "pays": "Suède",
          "boisson_cuisine": 10,
          "lavage_vaisselle": 20,
          "lavage_linge": 20,
          "hygiene": 55,
          "wc": 50,
          "divers": 9,
          "total": 164
        },
        {
          "pays": "U.S.A",
          "boisson_cuisine": 11,
          "lavage_vaisselle": 14,
          "lavage_linge": 33,
          "hygiene": 170,
          "wc": null,
          "divers": 11,
          "total": 240
        }
      ],
      "france_par_usage": {
        "chasse_wc": {"valeur": {"min": 8, "max": 10}, "unite": "litres/usage"},
        "lavabo": {"valeur": 10, "unite": "litres/usage"},
        "douche": {"valeur": 100, "unite": "litres/usage"},
        "bain": {"valeur": {"min": 150, "max": 200}, "unite": "litres/usage"},
        "lave_vaisselle_10_couverts": {"valeur": 50, "unite": "litres/cycle"},
        "lave_vaisselle_12_couverts": {"valeur": 80, "unite": "litres/cycle"},
        "lave_linge_4kg": {"valeur": {"min": 80, "max": 100}, "unite": "litres/cycle"},
        "lave_linge_5kg": {"valeur": {"min": 120, "max": 220}, "unite": "litres/cycle"}
      }
    },
    "dotations_services_publics": {
      "ecoles_sans_douche": {"valeur": 100, "unite": "l/jour/eleve"},
      "hopitaux": {"valeur": {"min": 100, "max": 400}, "unite": "l/jour/lit"},
      "batiments_publics": {"valeur": {"min": 40, "max": 60}, "unite": "l/jour/employe"},
      "arrosage_chaussee": {"valeur": 1, "unite": "l/jour/m2"},
      "arrosage_jardin": {"valeur": {"min": 5, "max": 10}, "unite": "l/jour/m2"},
      "abattoirs_gros_betail": {"valeur": {"min": 300, "max": 500}, "unite": "l/tete"},
      "abattoirs_petit_betail": {"valeur": {"min": 250, "max": 300}, "unite": "l/tete"},
      "piscines": {"valeur": {"min": 100, "max": 200}, "unite": "m3/jour"},
      "bains_publics": {"valeur": {"min": 160, "max": 180}, "unite": "l/visiteur"},
      "lutte_incendie": {"debit": 60, "duree_heure": 2, "unite_debit": "m3/h", "description": "Besoin ponctuel, non inclus dans le calcul journalier mais essentiel pour le dimensionnement de la réserve."}
    },
    "dotations_commerces_bureaux": {
      "maisons_de_commerce_sans_clim": {"valeur": 100, "unite": "l/j/employe"},
      "maisons_de_commerce_avec_clim": {"valeur": 400, "unite": "l/j/employe"},
      "maisons_de_commerce_sans_clim_avec_resto": {"valeur": 150, "unite": "l/j/employe"},
      "maisons_de_commerce_avec_clim_avec_resto": {"valeur": 250, "unite": "l/j/employe"},
      "boulangerie": {"valeur": 200, "unite": "l/j/employe"},
      "coiffeur": {"valeur": 15, "unite": "l/j/visiteur"},
      "restaurant": {"valeur": 200, "unite": "l/j/visiteur"},
      "hotel": {"valeur": {"min": 200, "max": 600}, "unite": "l/j/lit"},
      "bureaux_sans_clim_sans_cantine": {"valeur": {"min":10, "max": 30}, "unite": "l/j/employe"},
      "bureaux_sans_clim_avec_cantine": {"valeur": {"min":30, "max": 100}, "unite": "l/j/employe"},
      "bureaux_avec_clim_generale": {"valeur": {"min":100, "max": 225}, "unite": "l/j/employe"},
      "boucherie": {"valeur": {"min":250, "max": 400}, "unite": "l/j/employe"}
    },
    "dotations_industries_m3_par_tonne": {
      "acier": {"min": 6, "max": 300},
      "rayonne": {"min": 400, "max": 11000},
      "savon": {"min": 1, "max": 35},
      "plastique": {"min": 1, "max": 2},
      "papier": {"min": 80, "max": 1000},
      "carton": {"min": 60, "max": 400},
      "essence": {"min": 0.1, "max": 40},
      "coton_teinturerie": {"min": 7, "max": 35},
      "biere": {"min": 8, "max": 25},
      "sucre": {"min": 3, "max": 400}
    },
    "dotations_centrales_thermiques": {
        "tranche_1000_MW_circuit_ouvert_thermique": {"debit": 35, "unite": "m3/s", "rechauffement": 7, "unite_temp": "°C"},
        "tranche_1000_MW_circuit_ouvert_nucleaire": {"debit": 40, "unite": "m3/s", "rechauffement": 10, "unite_temp": "°C"},
        "tranche_1000_MW_circuit_ferme": {"debit_appoint": {"min": 20, "max": 30}, "unite": "fois moins", "rechauffement": 0.2, "unite_temp": "°C"}
    }
  },
  "parametres_adduction": {
    "parametres_physiques": {
      "g_acceleration_gravite_ms2": 9.81,
      "viscosite_cinematique_eau_m2_s": {
        "valeur": 1.004e-6,
        "temperature_C": 20,
        "source": "Valeur standard pour l'eau à 20°C"
      }
    },
    "coefficients_rugosite": {
      "hazen_williams_C": [
        { "materiau": "Fonte", "etat": "neuve", "valeur": 130 },
        { "materiau": "Fonte", "etat": "5 ans", "valeur": 120 },
        { "materiau": "Fonte", "etat": "20 ans", "valeur": 100 },
        { "materiau": "Béton", "etat": "neuf", "valeur": 130 },
        { "materiau": "Acier", "etat": "neuf", "valeur": 140 },
        { "materiau": "Amiante-Ciment", "etat": "neuf", "valeur": 140 },
        { "materiau": "PVC", "etat": "neuf", "valeur": 150 },
        { "materiau": "PEHD", "etat": "neuf", "valeur": 150 }
      ],
      "manning_n": [
        { "nature_parois": "Ciment lissé", "tres_bon": 0.010, "bon": 0.011, "assez_bon": 0.012, "mauvais": 0.013 },
        { "nature_parois": "Mortier de ciment", "tres_bon": 0.011, "bon": 0.012, "assez_bon": 0.013, "mauvais": 0.015 },
        { "nature_parois": "Béton", "tres_bon": 0.012, "bon": 0.014, "assez_bon": 0.016, "mauvais": 0.018 },
        { "nature_parois": "Fonte", "tres_bon": 0.012, "bon": 0.013, "assez_bon": 0.014, "mauvais": 0.015 },
        { "nature_parois": "Acier riveté", "tres_bon": 0.013, "bon": 0.015, "assez_bon": 0.016, "mauvais": 0.017 },
        { "nature_parois": "PVC", "tres_bon": 0.009, "bon": 0.010, "assez_bon": 0.011, "mauvais": 0.012 },
        { "nature_parois": "PEHD", "tres_bon": 0.009, "bon": 0.010, "assez_bon": 0.011, "mauvais": 0.012 }
      ],
      "rugosite_absolue_e_mm": [
        { "materiau": "PVC", "valeur_mm": 0.0015 },
        { "materiau": "PEHD", "valeur_mm": 0.0015 },
        { "materiau": "Acier neuf", "valeur_mm": 0.045 },
        { "materiau": "Acier usagé", "valeur_mm": 0.2 },
        { "materiau": "Fonte neuve", "valeur_mm": 0.25 },
        { "materiau": "Fonte usagée", "valeur_mm": 1.0 },
        { "materiau": "Béton lisse", "valeur_mm": 0.3 },
        { "materiau": "Béton brut", "valeur_mm": 2.0 }
      ]
    },
    "coefficients_pertes_singulieres_K": [
      { "element": "Coude 90° standard", "valeur_K": 0.9 },
      { "element": "Coude 45° standard", "valeur_K": 0.4 },
      { "element": "Vanne à opercule ouverte", "valeur_K": 0.2 },
      { "element": "Vanne à opercule mi-fermée", "valeur_K": 5.6 },
      { "element": "Clapet anti-retour", "valeur_K": 2.5 },
      { "element": "Té (écoulement direct)", "valeur_K": 0.2 },
      { "element": "Té (branche)", "valeur_K": 1.8 },
      { "element": "Entrée de conduite (bord franc)", "valeur_K": 0.5 },
      { "element": "Sortie de conduite", "valeur_K": 1.0 }
    ]
  },
  "parametres_distribution": {
    "regles_conception": {
      "vitesses_admissibles_ms": {
        "min": 0.5,
        "max": 1.25,
        "description": "Plage de vitesse de l'eau recommandée dans les conduites pour éviter la sédimentation et les coups de bélier."
      },
      "coefficient_pointe_alpha": {
        "min": 1.4,
        "max": 3.5,
        "description": "Coefficient multiplicateur du débit moyen journalier pour obtenir le débit de pointe. Varie des grandes agglomérations (1.4) aux petites (3.5)."
      },
      "diametres_minimum_incendie_mm": {
        "troncons_avec_bouches_incendie": 80,
        "general": 60,
        "recommande_si_possible": 100
      }
    },
    "pressions_requises_par_etage_mCE": [
      { "etages": 1, "hauteur_m_min": 12, "hauteur_m_max": 15 },
      { "etages": 2, "hauteur_m_min": 16, "hauteur_m_max": 19 },
      { "etages": 3, "hauteur_m_min": 20, "hauteur_m_max": 23 },
      { "etages": 4, "hauteur_m_min": 24, "hauteur_m_max": 27 },
      { "etages": 5, "hauteur_m_min": 29, "hauteur_m_max": 32 },
      { "etages": 6, "hauteur_m_min": 33, "hauteur_m_max": 36 },
      { "etages": 7, "hauteur_m_min": 37, "hauteur_m_max": 40 }
    ],
    "parametres_formules_hardy_cross": {
      "description": "Paramètres pour la formule de perte de charge ΔH = K * Q^n",
      "Universelle": {
        "n": 2,
        "K_expression": "(1 + α) * 8 * λ * L / (g * π^2 * D^5)",
        "commentaire": "λ est le coeff. de Darcy-Weisbach. α est la fraction des pertes singulières."
      },
      "Manning-Strickler": {
        "n": 2,
        "K_expression": "(1 + α) * 10.29 * n^2 * L / D^(16/3)",
        "commentaire": "n est le coeff. de Manning."
      },
      "Hazen-Williams": {
        "n": 1.852,
        "K_expression": "(1 + α) * 10.65 * L / (C^1.852 * D^4.87)",
        "commentaire": "C est le coeff. de Hazen-Williams."
      },
      "Flamant": {
        "n": 1.75,
        "K_expression": "(1 + α) * 0.001404 * L / D^4.75",
        "commentaire": "Q en m³/s. Formule spécifique mentionnée dans le chapitre."
      }
    }
  },
  "normes_qualite_eau_annexe1": {
    "references_sources": {
      "a": {
        "source": "USA",
        "documents": ["Drinking water regulation -USA-EPA-Avril 1992"],
        "valeurs": {
          "MCL": "Maximum Contaminant Level",
          "AL": "Action Level",
          "TT": "Treatment Technique"
        }
      },
      "b": {
        "source": "OMS (WHO)",
        "documents": ["Guidelines for drinking water quality -1993"],
        "valeurs": {
          "GV": "Guideline value"
        }
      },
      "c": {
        "source": "CEE (UE)",
        "documents": ["Directive Européenne du 15.07.80 – 80/778/CEE – Qualité des eaux destinées à la consommation humaine"],
        "valeurs": {
          "NG": "Niveau guide",
          "CMA": "Concentration maximale admissible"
        }
      },
      "d": {
        "source": "France",
        "documents": ["Décret 03.01.89 modifié le 10.04.90 et le 07.03.91 – Eaux destinées à la consommation humaine"]
      },
      "notes_generales": {
        "1": "Pour les grandes installations (plus de 40 échantillons par mois) tolérance fixée à 5% d'échantillons positifs. Pour les petites installations (moins de 39 échantillons par mois) tolérance fixée à 1 échantillon positif.",
        "2": "A la production /en distribution."
      }
    },
    "parametres": [
      { "groupe": "Paramètres organoleptiques", "parametre": "Couleur", "unite": "mg/l Pt/Co", "valeurs": { "USA": {"MCL": 15}, "OMS": {"GV": 15}, "CEE": {"NG": 1, "CMA": 20}, "France": {"Reference": null, "Limite": 15} } },
      { "groupe": "Paramètres organoleptiques", "parametre": "Turbidité", "unite": "NTU-JTU", "valeurs": { "USA": {"MCL": "0,5 à 1"}, "OMS": {"GV": 5}, "CEE": {"NG": 0.4, "CMA": 4}, "France": {"Reference": null, "Limite": 2} } },
      { "groupe": "Paramètres organoleptiques", "parametre": "Odeur", "unite": "dilution (12°C) dilutions (25°C)", "valeurs": { "USA": {"MCL": 3}, "OMS": null, "CEE": {"NG": 0, "CMA": 2}, "France": {"Reference": 0, "Limite": 3} } },
      { "groupe": "Paramètres organoleptiques", "parametre": "Saveur", "unite": "dilution (12°C) dilution (25°C)", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 0, "CMA": 3}, "France": {"Reference": null, "Limite": 3} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Température", "unite": "degré Celsius", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 12, "CMA": 25}, "France": {"Reference": null, "Limite": 25} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "pH", "unite": null, "valeurs": { "USA": {"MCL": {"min": 6.5, "max": 8.5}}, "OMS": null, "CEE": {"NG": {"min": 6.5, "max": 8.5}}, "France": {"Reference": {"min": 6.5, "max": 8.5}, "Limite": {"min": 6.5, "max": 9}} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Conductivité", "unite": "μS/cm (20°C)", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 400}, "France": {"Reference": 400} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Résidu sec", "unite": "mg/l", "valeurs": { "USA": {"MCL": 500}, "OMS": {"GV": 1000}, "CEE": {"CMA": 1500}, "France": {"Limite": 1500} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Chlorures", "unite": "mg/l (Cl)", "valeurs": { "USA": {"MCL": 250}, "OMS": {"GV": 250}, "CEE": {"NG": 200, "CMA": 200}, "France": {"Limite": 200} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Sulfates", "unite": "mg/l (SO4)", "valeurs": { "USA": {"MCL": 250}, "OMS": {"GV": 250}, "CEE": {"NG": 25, "CMA": 250}, "France": {"Limite": 250} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Calcium", "unite": "mg/l (Ca)", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 100}, "France": {"Limite": 100} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Magnésium", "unite": "mg/l (Mg)", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 30, "CMA": 50}, "France": {"Limite": 50} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Sodium", "unite": "mg/l (Na)", "valeurs": { "USA": null, "OMS": {"GV": 200}, "CEE": {"NG": 20, "CMA": 150}, "France": {"Limite": 150} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Potassium", "unite": "mg/l (K)", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 10, "CMA": 12}, "France": {"Limite": 12} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Aluminium", "unite": "mg/l (Al)", "valeurs": { "USA": {"MCL": {"min": 0.05, "max": 0.2}}, "OMS": {"GV": 0.2}, "CEE": {"NG": -0.05, "CMA": 0.2}, "France": {"Limite": 0.2} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Oxygène dissous", "unite": "% de satur.", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": ">75"}, "France": null } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Nitrates", "unite": "Mg/l (NO3)", "valeurs": { "USA": {"MCL": 10}, "OMS": {"GV": 50}, "CEE": {"NG": 25, "CMA": 50}, "France": {"Limite": 50} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Nitrites", "unite": "Mg/l (NO2)", "valeurs": { "USA": {"MCL": 1}, "OMS": {"GV": 3}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Nitrates + nitrites", "unite": "mg/l (N)", "valeurs": { "USA": {"MCL": 10}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Ammonium", "unite": "mg/l (NH4)", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 0.05, "CMA": 0.5}, "France": {"Limite": 0.5} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Azote kjedahl", "unite": "mg/l (N)", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 0.1, "CMA": 1}, "France": {"Limite": 1} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Oxydabilité au KMnO4", "unite": "mg/l (O2)", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 2, "CMA": 5}, "France": {"Limite": 5} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Sulfure d'hydrogène", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": "0,05"}, "CEE": null, "France": {"Reference": "Sans od.", "Limite": "Sans od."} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "SEC chloroforme", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 0.1, "CMA": 10}, "France": {"Limite": 10} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Hydrocarbures dissous", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"CMA": 0.5}, "France": {"Limite": 0.5} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Indice phénol", "unite": "µg/l (C6H5OH)", "valeurs": { "USA": null, "OMS": null, "CEE": {"CMA": 0.5}, "France": {"Limite": 0.5} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Bore", "unite": "µg/l (B)", "valeurs": { "USA": null, "OMS": {"GV": 300}, "CEE": {"CMA": 1000}, "France": {"Limite": 1000} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Agents de surface", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 200, "CMA": 200}, "France": {"Limite": 200} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Organochlorés", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"CMA": 1}, "France": {"Limite": 1} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Fer", "unite": "µg/l (Fe)", "valeurs": { "USA": {"MCL": 300}, "OMS": {"GV": 300}, "CEE": {"NG": 50, "CMA": 200}, "France": {"Limite": 200} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Manganèse", "unite": "µg/l (Mn)", "valeurs": { "USA": {"MCL": 50}, "OMS": {"GV": 500}, "CEE": {"NG": 20, "CMA": 50}, "France": {"Limite": 50} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Cuivre", "unite": "µg/l (Cu)", "valeurs": { "USA": {"MCL": "Al 1 300"}, "OMS": {"GV": 1000}, "CEE": null, "France": null } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Zinc", "unite": "µg/l (Zn)", "valeurs": { "USA": {"MCL": "5 000"}, "OMS": {"GV": "3 000"}, "CEE": {"NG": 100, "CMA": "5 000"}, "France": {"Limite": "5 000"} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Phosphore", "unite": "µg/l (P2O5)", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 400, "CMA": "5 000"}, "France": {"Limite": "5 000"} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Fluorure", "unite": "µg/l (F)(8/12°C)", "valeurs": { "USA": {"MCL": "4 000"}, "OMS": {"GV": 1500}, "CEE": {"CMA": 1500}, "France": {"Limite": 1500} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Fluorure", "unite": "µg/l (F)(25/30°C)", "valeurs": { "USA": null, "OMS": null, "CEE": {"CMA": 700}, "France": {"Limite": 700} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Matières en suspension", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"Absence": true}, "France": {"Absence": true} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Baryum", "unite": "µg/l (Ba)", "valeurs": { "USA": {"MCL": 2000}, "OMS": {"GV": 700}, "CEE": {"NG": 100}, "France": {"Limite": 100} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Argent", "unite": "µg/l (Ag)", "valeurs": { "USA": {"MCL": "AL 15"}, "OMS": null, "CEE": {"NG": 10}, "France": {"Limite": 10} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Arsenic", "unite": "µg/l (As)", "valeurs": { "USA": {"MCL": 50}, "OMS": {"GV": 10}, "CEE": {"CMA": 50}, "France": {"Limite": 50} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Beryllium", "unite": "µg/l (Be)", "valeurs": { "USA": {"MCL": 1}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Cadmium", "unite": "µg/l (Cd)", "valeurs": { "USA": {"MCL": 5}, "OMS": {"GV": 3}, "CEE": {"CMA": 5}, "France": {"Limite": 5} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Cyanures", "unite": "µg/l (Cn)", "valeurs": { "USA": {"MCL": 200}, "OMS": {"GV": 70}, "CEE": {"CMA": 50}, "France": {"Limite": 50} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Chrome total", "unite": "µg/l (Cr)", "valeurs": { "USA": {"MCL": 100}, "OMS": null, "CEE": {"CMA": 50}, "France": {"Limite": 50} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Mercure", "unite": "µg/l (Hg)", "valeurs": { "USA": {"MCL": 2, "note": "inodér"}, "OMS": {"GV": 2}, "CEE": {"CMA": 50}, "France": {"Limite": 50} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Nickel", "unite": "µg/l (Ni)", "valeurs": { "USA": {"MCL": 100}, "OMS": {"GV": 20}, "CEE": {"CMA": 50}, "France": {"Limite": 50} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Plomb", "unite": "µg/l (Pb)", "valeurs": { "USA": {"MCL": "AL 15"}, "OMS": {"GV": 10}, "CEE": {"CMA": 50}, "France": {"Limite": 50} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Antimoine", "unite": "µg/l (Sb)", "valeurs": { "USA": {"MCL": "5-10"}, "OMS": {"GV": 10}, "CEE": {"CMA": 10}, "France": {"Limite": 10} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Sélénium", "unite": "µg/l (Se)", "valeurs": { "USA": {"MCL": 50}, "OMS": {"GV": 10}, "CEE": {"CMA": 10}, "France": {"Limite": 10} } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Thallium", "unite": "µg/l (Tl)", "valeurs": { "USA": {"MCL": 2}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Molybdène", "unite": "µg/l (Mo)", "valeurs": { "USA": null, "OMS": {"GV": 70}, "CEE": null, "France": null } },
      { "groupe": "Paramètres physico-chimiques", "parametre": "Amiante", "unite": "million fibres/l", "valeurs": { "USA": {"MCL": 7}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Pesticides par subs.", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Pesticides au total", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"CMA": 0.5}, "France": {"Limite": 0.5} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "PCB et PCT", "unite": "µg/l", "valeurs": { "USA": {"MCL": 0.5}, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Aldrin et Dieldrine", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 0.03}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Chlordane", "unite": "µg/l", "valeurs": { "USA": {"MCL": 2}, "OMS": {"GV": 0.2}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "2,4-D", "unite": "µg/l", "valeurs": { "USA": {"MCL": 70}, "OMS": {"GV": 30}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "DDT", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 2}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Heptachlor-époxyde", "unite": "µg/l", "valeurs": { "USA": {"MCL": "0,4 et 0,2"}, "OMS": {"GV": 0.03}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Hexachlorobenzène", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 1}, "CEE": {"CMA": 0.01}, "France": {"Limite": 0.01} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Lindane", "unite": "µg/l", "valeurs": { "USA": {"MCL": 0.2}, "OMS": {"GV": 2}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Méthoxychlore", "unite": "µg/l", "valeurs": { "USA": {"MCL": 40}, "OMS": {"GV": 20}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Pentachlorophénol", "unite": "µg/l", "valeurs": { "USA": {"MCL": 1}, "OMS": {"GV": 9}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "2,4,5-T ou Silvex", "unite": "µg/l", "valeurs": { "USA": {"MCL": 50}, "OMS": {"GV": 9}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "1,2 dichloropropane", "unite": "µg/l", "valeurs": { "USA": {"MCL": 5}, "OMS": {"GV": 20}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Alachlore", "unite": "µg/l", "valeurs": { "USA": {"MCL": 2}, "OMS": {"GV": 20}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Aldicarbe", "unite": "µg/l", "valeurs": { "USA": {"MCL": 3}, "OMS": {"GV": 10}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Atrazine", "unite": "µg/l", "valeurs": { "USA": {"MCL": 3}, "OMS": {"GV": 2}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Simazine", "unite": "µg/l", "valeurs": { "USA": {"MCL": 40}, "OMS": {"GV": 2}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Carbofuran", "unite": "µg/l", "valeurs": { "USA": {"MCL": 40}, "OMS": {"GV": 7}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Dibromochloropropane", "unite": "µg/l", "valeurs": { "USA": {"MCL": 0.2}, "OMS": {"GV": 1}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Aldicarb sulfoxyde", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Dicamba sulfone", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Ethylene dibromure", "unite": "µg/l", "valeurs": { "USA": {"MCL": 0.05}, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Endrin", "unite": "µg/l", "valeurs": { "USA": {"MCL": 2}, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Dalapon", "unite": "µg/l", "valeurs": { "USA": {"MCL": 200}, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Dinoseb", "unite": "µg/l", "valeurs": { "USA": {"MCL": 7}, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Diquat", "unite": "µg/l", "valeurs": { "USA": {"MCL": 20}, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Endothall", "unite": "µg/l", "valeurs": { "USA": {"MCL": 100}, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Glyphosate", "unite": "µg/l", "valeurs": { "USA": {"MCL": 700}, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Oxamyl", "unite": "µg/l", "valeurs": { "USA": {"MCL": 200}, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Piclorem", "unite": "µg/l", "valeurs": { "USA": {"MCL": 500}, "OMS": null, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Benthazone", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 30}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "1,2 dichloropropane", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 20}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Isoproturon", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 9}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "MCPA", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 2}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Mecoprop", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 10}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Molinate", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 6}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Pendimethaline", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 20}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Propanil", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 20}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Pyridate", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 100}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Trifluraline", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 20}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Dichlorprop", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 100}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "2,4-DB", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 90}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "2,4,5-T", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 9}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Pesticides et produits apparentés", "parametre": "Mécoprop", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 10}, "CEE": {"CMA": 0.1}, "France": {"Limite": 0.1} } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Monochloramine", "unite": "mg/l", "valeurs": { "USA": null, "OMS": {"GV": 3}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Chlore", "unite": "mg/l", "valeurs": { "USA": null, "OMS": {"GV": 5}, "CEE": null, "France": {"Limite": 0.1} } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Bromate", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 25}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "2,4,6 trichlorophenol", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 200}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Formaldéhyde", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 900}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "THM (total)", "unite": "µg/l", "valeurs": { "USA": {"MCL": 100}, "OMS": null, "CEE": {"NG": 1}, "France": {"Limite": 1} } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Bromoforme", "unite": "µg/l", "valeurs": { "USA": {"MCL": 100}, "OMS": {"GV": 100}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Dibromochloromethane", "unite": "µg/l", "valeurs": { "USA": {"MCL": 100}, "OMS": {"GV": 60}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Chlorodibromomethane", "unite": "µg/l", "valeurs": { "USA": {"MCL": 100}, "OMS": {"GV": 100}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Acide trichloroacétique", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 200}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Acide dichloroacétique", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 50}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Trichloroacétaldéide", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 10}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Trichloroacétonitrile", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 1}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Dibromoacétonitrile", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 100}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Trichloroacétonitrile", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 1}, "CEE": null, "France": null } },
      { "groupe": "Sous-produits d'oxydation", "parametre": "Chlorure de Cyanogène", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 70}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Monochlorobenzène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 100}, "OMS": {"GV": 300}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "1,2 dichlorobenzène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 600}, "OMS": {"GV": 1000}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "1,4 dichlorobenzène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 300}, "OMS": {"GV": 75}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "trichlorobenzène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 70}, "OMS": {"GV": 20}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "chlorure de vinyle", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 5}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "trichlorure de carbone", "unite": "µg/l", "valeurs": { "USA": {"MCL": 5}, "OMS": {"GV": 2}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "1,2 dichloréthane", "unite": "µg/l", "valeurs": { "USA": {"MCL": 5}, "OMS": {"GV": 30}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "1,1,1 trichloréthane", "unite": "µg/l", "valeurs": { "USA": {"MCL": 200}, "OMS": {"GV": 2000}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "1,1,2 trichloréthane", "unite": "µg/l", "valeurs": { "USA": {"MCL": 5}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "1,1 dichloréthylène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 7}, "OMS": {"GV": 30}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Cis-dichloréthylène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 70}, "OMS": {"GV": 50}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Trans 1,2 dichloréthyl.", "unite": "µg/l", "valeurs": { "USA": {"MCL": 100}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Trichloréthylène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 5}, "OMS": {"GV": 70}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Tetrachloréthylène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 5}, "OMS": {"GV": 40}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "chlorure de vinyle", "unite": "µg/l", "valeurs": { "USA": {"MCL": 2}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Hexachlorobutadiene", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 0.6}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Hexachlorocyclopentad", "unite": "µg/l", "valeurs": { "USA": {"MCL": 50}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Toxaphène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 3}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "EDTA", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 200}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Acide nitrilotriacetique", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 200}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Benzène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 5}, "OMS": {"GV": 10}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Ethylbenzène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 700}, "OMS": {"GV": 300}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Styrène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 100}, "OMS": {"GV": 20}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Toluène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 1000}, "OMS": {"GV": 700}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Xylène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 10000}, "OMS": {"GV": 500}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "diethylhexyladipate", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 80}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Di(éthylhexyl)phtalate", "unite": "µg/l", "valeurs": { "USA": null, "OMS": {"GV": 8}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "3,4,7,8 TCDD (dioxine)", "unite": "µg/l", "valeurs": { "USA": {"MCL": "5*10-3"}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Epichlorhydrine", "unite": "µg/l", "valeurs": { "USA": {"MCL": "TT"}, "OMS": {"GV": 400}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Acrylamide", "unite": "µg/l", "valeurs": { "USA": {"MCL": "TT"}, "OMS": {"GV": 0.5}, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Vydate (oxamyl)", "unite": "µg/l", "valeurs": { "USA": {"MCL": 200}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "HPA (total)", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 2.0, "CMA": 2.0}, "France": {"Limite": 2.0} } },
      { "groupe": "Autres composés organiques", "parametre": "Fluoranthène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 0.2}, "OMS": null, "CEE": {"NG": 2.0, "CMA": 2.0}, "France": {"Limite": 2.0} } },
      { "groupe": "Autres composés organiques", "parametre": "Benzo 3,4 fluoranthène", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 0.2, "CMA": 0.2}, "France": {"Limite": 0.2} } },
      { "groupe": "Autres composés organiques", "parametre": "Benzo 11,12 fluor", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 0.2, "CMA": 0.2}, "France": {"Limite": 0.2} } },
      { "groupe": "Autres composés organiques", "parametre": "Benzo 1,12 pérylène", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 0.2, "CMA": 0.2}, "France": {"Limite": 0.2} } },
      { "groupe": "Autres composés organiques", "parametre": "Benzo 3,4 pyrène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 0.2}, "OMS": {"GV": 0.7}, "CEE": {"NG": 0.2, "CMA": 0.2}, "France": {"Limite": 0.01} } },
      { "groupe": "Autres composés organiques", "parametre": "Indeno 1,2,3-cd pyrène", "unite": "µg/l", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 0.2, "CMA": 0.2}, "France": {"Limite": 0.2} } },
      { "groupe": "Autres composés organiques", "parametre": "Benzoanthracène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 0.1}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Autres composés organiques", "parametre": "Dibenzo 1,4 anthracène", "unite": "µg/l", "valeurs": { "USA": {"MCL": 0.3}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Paramètres microbiologiques", "parametre": "Coliformes totaux", "unite": "N/100 ml", "valeurs": { "USA": {"MCL": "Q.Inst.(1) P, inst.(1)"}, "OMS": {"GV": "0 (95%)"}, "CEE": {"NG": "0 (95%)"}, "France": {"Limite": "0 (95%)"} } },
      { "groupe": "Paramètres microbiologiques", "parametre": "Coliformes thermotol.", "unite": "N/100 ml", "valeurs": { "USA": null, "OMS": {"GV": 0}, "CEE": {"NG": 0}, "France": {"Limite": 0} } },
      { "groupe": "Paramètres microbiologiques", "parametre": "Streptocoques fécaux", "unite": "N/100 ml", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 0}, "France": {"Limite": 0} } },
      { "groupe": "Paramètres microbiologiques", "parametre": "Clostridium", "unite": "N/20 ml", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 1}, "France": {"Limite": 1} } },
      { "groupe": "Paramètres microbiologiques", "parametre": "Germes totaux", "unite": "N/1 ml (37°C) N/1 ml (22°C)", "valeurs": { "USA": {"MCL": "π"}, "OMS": {"GV": "π"}, "CEE": {"NG": 10, "CMA": 100}, "France": {"Limite": "2/10(2) 20/100(2)"} } },
      { "groupe": "Paramètres microbiologiques", "parametre": "Salmonelles", "unite": "N/5 l", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 0}, "France": {"Limite": 0} } },
      { "groupe": "Paramètres microbiologiques", "parametre": "Staphylocoques patho.", "unite": "N/100 ml", "valeurs": { "USA": null, "OMS": null, "CEE": {"NG": 0}, "France": {"Limite": 0} } },
      { "groupe": "Paramètres microbiologiques", "parametre": "Bactériophages fécaux", "unite": "N/50 ml", "valeurs": { "USA": null, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Paramètres microbiologiques", "parametre": "Legionella", "unite": null, "valeurs": { "USA": {"MCL": "π"}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Paramètres microbiologiques", "parametre": "Giardia", "unite": null, "valeurs": { "USA": {"MCL": "π"}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Paramètres microbiologiques", "parametre": "Virus", "unite": "N/10 l", "valeurs": { "USA": {"MCL": "π"}, "OMS": null, "CEE": {"NG": 0}, "France": {"Limite": 0} } },
      { "groupe": "Radioactivité", "parametre": "Alpha globale", "unite": "Becquerel/l", "valeurs": { "USA": {"MCL": "15 (picC/l)"}, "OMS": {"GV": 0.1}, "CEE": null, "France": null } },
      { "groupe": "Radioactivité", "parametre": "Beta globale", "unite": "pico curie/l", "valeurs": { "USA": null, "OMS": {"GV": 1}, "CEE": null, "France": null } },
      { "groupe": "Radioactivité", "parametre": "Beta", "unite": "millirein/an", "valeurs": { "USA": {"MCL": 4}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Radioactivité", "parametre": "Radium 226/228", "unite": "pico curie/l", "valeurs": { "USA": {"MCL": 20}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Radioactivité", "parametre": "Uranium", "unite": "µg/l", "valeurs": { "USA": {"MCL": 20}, "OMS": null, "CEE": null, "France": null } },
      { "groupe": "Radioactivité", "parametre": "Radon", "unite": "pico curie/l", "valeurs": { "USA": {"MCL": 300}, "OMS": null, "CEE": null, "France": null } }
    ]
  },
  "entretien_et_maintenance": {
    "causes_pollution": {
      "description": "Classification des causes de pollution des réseaux d'eau (Tableau 6.1)",
      "accidentelle_occasionnelle": {
        "localisees": [
          "Accident de transport",
          "Rupture de conduite",
          "Rupture de stockage de produits chimiques et pétroliers",
          "Accident industriel, guerre, sabotage"
        ],
        "lineaires": [
          "Pollution accidentelle de cours d'eau"
        ],
        "diffuses": [
          "Pollution atmosphérique, accidentelle massive",
          "Pollution des sols",
          "Inondation",
          "Rupture de digue"
        ]
      },
      "chronique": {
        "localisees": [
          "Ouvrage de captage défectueux",
          "Puisards, puits perdus",
          "Lagunage des bassins non étanches",
          "Décharges, terrils, dépôts mal conçus",
          "Rejets souterrains"
        ],
        "lineaires": [
          "Réalimentation de nappe par des cours d'eau pollués",
          "Infiltration des eaux de ruissellement du réseau routier",
          "Fuite de réseau d'assainissement",
          "Fuite de conduites de produits industriels",
          "Intrusion d'eau marine",
          "Décharge chimique"
        ],
        "diffuses": [
          "Epandage agricole mal conduit",
          "Mauvaises pratiques culturales",
          "Rejet souterrain d'eau de drainage agricole",
          "Pollution atmosphérique chronique",
          "Assainissement domestique autonome mal conçu et mal exploité",
          "Crues individuelles de fuel domestique"
        ]
      }
    },
    "elements_cout_entretien": {
      "description": "Principaux postes de coût de l'entretien d'un réseau (Tableau 6.2)",
      "Detection": [
        "Coût de la surveillance « détection »",
        "Coût des campagnes de recherche de fuite",
        "Coût du fonctionnement des postes de protection cathodiques"
      ],
      "Entretien_Courant": [
        "Coût d'entretien des compteurs",
        "Coût d'entretien de la fontainerie",
        "Coût d'entretien des branchements"
      ],
      "Reparation": [
        "Coût de réparations de conduites",
        "Coût de remise à niveau des bouches à clé"
      ]
    },
    "relation_chlore_temps_desinfection": {
      "description": "Relation entre la dose de chlore et le temps de contact pour la désinfection de canalisations (Tableau 6.4)",
      "donnees": [
        { "temps_contact_minimum_heures": 24, "dose_chlore_actif_mg_l": 10 },
        { "temps_contact_minimum_heures": 12, "dose_chlore_actif_mg_l": 25 },
        { "temps_contact_minimum_heures": 6, "dose_chlore_actif_mg_l": 50 },
        { "temps_contact_minimum_heures": 3, "dose_chlore_actif_mg_l": 100 },
        { "temps_contact_minimum_heures": 1, "dose_chlore_actif_mg_l": 150 },
        { "temps_contact_minimum_heures": 0, "dose_chlore_actif_mg_l": 10000, "note": "Contact instantané" }
      ]
    },
    "seuils_performance_reseau": {
      "description": "Valeurs de référence pour les indicateurs de performance du réseau.",
      "rendement_primaire": {
        "objectif_bon_pourcent": 65,
        "objectif_excellent_pourcent": 90
      },
      "indice_lineaire_reparations": {
        "plage_courante_an_km": { "min": 0.4, "max": 1.0 }
      },
      "indice_lineaire_pertes": {
        "plage_typique_m3_jour_km": { "min": 1, "max": 15 }
      }
    }
  },
  "annexe_3_entretien_detaillee": {
    "annexe_3_entretien": {
      "description": "Transcription de l'Annexe 3 - Fichier sommaire des opérations d'entretien et de maintenance préventive.",
      "entretien_ouvrages": [
        { "ouvrage": "Prise en rivière Canal d'amenée", "type_entretien": "Dévasage", "frequence": "5 ans", "duree": "5 jours", "effectif": "3 pers.", "observations": "Plongeurs" },
        { "ouvrage": "Dégrilleur", "type_entretien": "Nettoyage de la fosse", "frequence": "1 an", "duree": "4 heures", "effectif": "2 pers.", "observations": "A la lance" },
        { "ouvrage": "Macrotamisage", "type_entretien": "Nettoyage prise niveau", "frequence": "1 an", "duree": "8 heures", "effectif": "1 pers.", "observations": "Lance et si besoin injection de chlore" },
        { "ouvrage": "Bâche d'exhaure", "type_entretien": "Nettoyage", "frequence": "1 an", "duree": "8 heures", "effectif": "2 à 3 pers.", "observations": "Lance + désinfection" },
        { "ouvrage": "Bâche reprise", "type_entretien": "Nettoyage", "frequence": "1 an", "duree": "8 heures", "effectif": "2 à 3 pers.", "observations": "Lance + désinfection" },
        { "ouvrage": "Bâche de refoulement", "type_entretien": "Nettoyage", "frequence": "1 an", "duree": "8 heures", "effectif": "2 à 3 pers.", "observations": "Lance + désinfection" },
        { "ouvrage": "Décanteurs", "type_entretien": "Nettoyage total", "frequence": "1 an", "duree": "8 heures", "effectif": "4 pers.", "observations": "Lance, raclette, balais" },
        { "ouvrage": "Décanteurs", "type_entretien": "Nettoyage partiel (nettoyage clarinettes et concentrateurs)", "frequence": "4 mois", "duree": "4 heures", "effectif": "2 pers.", "observations": null },
        { "ouvrage": "Vannes, ventilateurs", "type_entretien": "Dépoussiérage, roulement moteurs, vérification des vannes", "frequence": "2 ans", "duree": "8 heures", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Filtres Parois des filtres", "type_entretien": "Nettoyage", "frequence": "15 jours", "duree": "1 heure", "effectif": "1 pers.", "observations": "Lance, acide, brosses" },
        { "ouvrage": "Vérification des niveaux, matériaux filtrants", "type_entretien": null, "frequence": "1 an", "duree": "1/2 heure", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Entretien des vannes et vérins", "type_entretien": "démontage, remplacement des joints etc.", "frequence": "1 an", "duree": "4 heures", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Tour d'Ozone Parois de tours", "type_entretien": "Nettoyage", "frequence": "2 ans", "duree": "8 heures", "effectif": "2 pers.", "observations": "Lance" },
        { "ouvrage": "Tour d'Ozone Nettoyage des poreux, remplac. des joints", "type_entretien": "Nettoyage à l'acide", "frequence": "2 ans", "duree": "5 jours", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Cuves de recyclage des eaux de lavage", "type_entretien": "Vidange et nettoyage", "frequence": "6 mois", "duree": "8 heures", "effectif": "2 pers.", "observations": "Lance, pompe de vidange" },
        { "ouvrage": "Citerne de stockage de réactifs", "type_entretien": "Nettoyage, vérification des parois, révision des vannes", "frequence": "3 ans", "duree": "8 heures", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Cuves métalliques de réactifs (acides etc.)", "type_entretien": "Vérification des épaisseurs", "frequence": "2 ans", "duree": "1/2 heure", "effectif": "1 pers.", "observations": "Ultrasons" },
        { "ouvrage": "Ballons antibéliers", "type_entretien": "Nettoyage et contrôle des épaisseurs de parois", "frequence": "5 ans", "duree": "Variable suivant la taille", "effectif": "1 à 2 pers.", "observations": "Organisme de contrôle" },
        { "ouvrage": "Groupe sécheur", "type_entretien": "Contrôle alumine (décuvage)", "frequence": "3 ans", "duree": "8 à 16 h suivant taille", "effectif": "2 pers.", "observations": "Changement partiel d'alumine" },
        { "ouvrage": "Transformateurs Self", "type_entretien": "Nettoyage contrôle de serrage. Vérification niveaux d'huile", "frequence": "1 an", "duree": "2 heures", "effectif": "2 pers.", "observations": null },
        { "ouvrage": "Capteurs Physicocimiques (Chlore résiduel, Ozone résiduel, pH mètre, oxygène dissous, Turbidimètre)", "type_entretien": "Etalonnage et nettoyage des électrodes et cuves", "frequence": "8 jours", "duree": "1 heure", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Capteurs Physicocimiques (Chlore résiduel, Ozone résiduel, pH mètre, oxygène dissous, Turbidimètre)", "type_entretien": "révision complète", "frequence": "1 an", "duree": "8 heures", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Capteurs Chimiques (Colorimètres - Ammonium - chlore résiduel)", "type_entretien": "Etalonnage et renouvellement des actifs", "frequence": "8 jours", "duree": "1 heure", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Capteurs Physiques (Régulation filtre - Mesure niveau - Mesure perte de charge)", "type_entretien": "Etalonnage et nettoyage", "frequence": "3 mois", "duree": "1 heure", "effectif": "2 pers.", "observations": "Pièce de recharge" },
        { "ouvrage": "Capteurs Débitmètres", "type_entretien": "Etalonnage et nettoyage", "frequence": "3 mois", "duree": "4 heures", "effectif": "1 pers.", "observations": "Matériel spécifique" },
        { "ouvrage": "Capteurs (Pression différentielle, Electromagnétique, Capteurs niveaux UV, etc.)", "type_entretien": "Etalonnage du zéro", "frequence": "3 mois", "duree": "15 mn", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Capteurs (Pression différentielle, Electromagnétique, Capteurs niveaux UV, etc.)", "type_entretien": "Etalonnage", "frequence": "3 mois", "duree": "1 heure", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Pesons", "type_entretien": "Etalonnage", "frequence": "3 mois", "duree": "1 heure", "effectif": "1 pers.", "observations": null }
      ],
      "entretien_electromecanique": [
        { "ouvrage": "Groupe électropompe Moteurs - jusqu'à 250 kW", "type_entretien": "Révision complète. Démontage, nettoyage. Remplacement roulements", "frequence": "Suivant heures de marche 25 000h ou tous les 5 ans", "duree": "2 jours", "effectif": "1 pers.", "observations": "Appareillage spécifique" },
        { "ouvrage": "Groupe électropompe Moteurs - 250 à 2 000 kW", "type_entretien": "Révision complète. Démontage, nettoyage. Remplacement roulements", "frequence": "Suivant heures de marche 25 000h ou tous les 5 ans", "duree": "3 à 4 jours", "effectif": "2 pers.", "observations": null },
        { "ouvrage": "Groupe électropompe - tous moteurs", "type_entretien": "Contrôle et vibrations de l'usure des roulements si besoin équilibrage et alignement", "frequence": "2 mois", "duree": "1h ou plus suiv. état", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Groupe électropompe - moteurs à rotor charbons", "type_entretien": "Contrôle usure charbons", "frequence": "3 mois", "duree": "1h ou 8h suiv. puis 1/2 h", "effectif": "1 à 2 pers.", "observations": "Produits nettoyants" },
        { "ouvrage": "Bobine", "type_entretien": "nettoyage collecteurs ou bagues. Contrôle isolement", "frequence": "3 mois", "duree": "1/2 h", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Pompes", "type_entretien": "Révision complète (démontage et vérification des organes vitaux)", "frequence": "Suiv. heures de marche 25 000 h ou tous les 5 ans", "duree": "5 jours", "effectif": "2 pers.", "observations": "Suivant la puissance des pompes, la révision sera sous-traitée au constructeur" },
        { "ouvrage": "Pompes", "type_entretien": "Remplacement des presses étoupes", "frequence": "1 à 2 ans", "duree": "2 à 3 h", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Equipements MT - Transformateurs", "type_entretien": "Dégraissage des isolateurs (poupées). Contrôle dessicateur. Niveau d'huile - organe sécurité contrôle huile diélectrique", "frequence": "1 an", "duree": "2 heures", "effectif": "2 pers.", "observations": "Suivant la puissance" },
        { "ouvrage": "cellules Interrupteurs Secteurs Disjoncteurs -jeux de barres", "type_entretien": "Contrôle du fonctionnement mécanique", "frequence": "2 ans", "duree": "Quelques h/cellules", "effectif": "2 pers.", "observations": "Sous-traité au constructeur" },
        { "ouvrage": "cellules Interrupteurs Secteurs Disjoncteurs -jeux de barres", "type_entretien": "Contrôle de dépoussiérage", "frequence": "2 ans", "duree": "1 journée", "effectif": "2 pers.", "observations": null },
        { "ouvrage": "Surpresseur", "type_entretien": "Révision (étanchéité roulement...)", "frequence": "Suivant heures de marche 15 à 20 000 h ou 2 ans", "duree": "1 journée", "effectif": "1 pers.", "observations": "Sous-traité au constructeur" },
        { "ouvrage": "Compresseurs (air de service)", "type_entretien": "Révision (clapets, roulement)", "frequence": "5 ans", "duree": "1/2 journée", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Vannes", "type_entretien": "Contrôle des surcouples essai de manœuvre, entretien du motoréducteur", "frequence": "1 an", "duree": "1 heure", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Pneumatiques", "type_entretien": "Entretien du pilote et vérin", "frequence": "1 an", "duree": "2 heures", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Pneumatiques", "type_entretien": "Essai de manœuvre", "frequence": "3 mois", "duree": "quelq. mn", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Manuelles", "type_entretien": "Essai de manœuvre", "frequence": "3 mois", "duree": "quelq. mn", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Manuelles", "type_entretien": "Entretien réducteur", "frequence": "5 ans", "duree": "8 heures", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Système de préparation d'air sec - Groupe froid", "type_entretien": "Contrôle et nettoyage des échangeurs, vérification change de pièces", "frequence": "1 an", "duree": "8 heures", "effectif": "2 pers.", "observations": "Frigoriste" },
        { "ouvrage": "Système de préparation d'air sec - Groupe froid", "type_entretien": "Contrôle et nettoyage des échangeurs, vérification change de pièces", "frequence": "1 an", "duree": "2 heures", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Système de préparation d'air sec - Sécheur", "type_entretien": "Contrôle système de régénération (ventilateur, vannes, résistances chauffantes...)", "frequence": "1 an", "duree": "8 heures", "effectif": "1 pers.", "observations": null },
        { "ouvrage": "Alumine", "type_entretien": null, "frequence": null, "duree": null, "effectif": null, "observations": null }
      ]
    }
  },
  "tableau_7_4_diametres_internes": {
    "tableau_7_4_diametres": {
      "description": "Diamètre d'emploi courant dans les installations intérieures d'eau (Tableau 7.4).",
      "notes": {
        "Acier s/soud": "tube d'acier sans soudure",
        "P.c.v": "tuyau en polychlorure de vinyle rigide, série 10 kg/cm²",
        "Fonte C": "fonte Centriflex",
        "fonte L": "fonte Lavril",
        "diametres_retenus": "pour la fonte, les diamètres intérieurs nominaux; pour les autres matériaux, les diamètres intérieurs réels (aux tolérances de fabrication près)."
      },
      "donnees": [
        { "diametre_interieur_mm": 8, "nature_tuyaux": ["Cuivre 8/10, plomb", "P.c.v.", "Acier s/soud 8/13"], "section_interieure_mm2": 50.3 },
        { "diametre_interieur_mm": 9.8, "nature_tuyaux": ["Acier «Standard 41» de 10"], "section_interieure_mm2": 70.9 },
        { "diametre_interieur_mm": 10, "nature_tuyaux": ["Cuivre 10/12, plomb", "P.c.v."], "section_interieure_mm2": 78.5 },
        { "diametre_interieur_mm": 11.5, "nature_tuyaux": ["Acier «Standard 41» de 12"], "section_interieure_mm2": 104 },
        { "diametre_interieur_mm": 11.6, "nature_tuyaux": ["P.c.v."], "section_interieure_mm2": 106 },
        { "diametre_interieur_mm": 12, "nature_tuyaux": ["Cuivre 12/14"], "section_interieure_mm2": 113 },
        { "diametre_interieur_mm": 12.5, "nature_tuyaux": ["Acier s/soud 12/17"], "section_interieure_mm2": 123 },
        { "diametre_interieur_mm": 13, "nature_tuyaux": ["Plomb"], "section_interieure_mm2": 133 },
        { "diametre_interieur_mm": 13.2, "nature_tuyaux": ["Acier s/soud 12/17", "P.c.v."], "section_interieure_mm2": 137 },
        { "diametre_interieur_mm": 14, "nature_tuyaux": ["Cuivre 14/16"], "section_interieure_mm2": 154 },
        { "diametre_interieur_mm": 15, "nature_tuyaux": ["Acier «Standard 41» de 15"], "section_interieure_mm2": 189 },
        { "diametre_interieur_mm": 16, "nature_tuyaux": ["Acier s/soud 15/21", "cuivre 16/18", "plomb"], "section_interieure_mm2": 201 },
        { "diametre_interieur_mm": 16.6, "nature_tuyaux": ["Acier s/soud 15/21"], "section_interieure_mm2": 216 },
        { "diametre_interieur_mm": 18, "nature_tuyaux": ["P.c.v."], "section_interieure_mm2": 222 },
        { "diametre_interieur_mm": 18.8, "nature_tuyaux": ["Cuivre 18/20"], "section_interieure_mm2": 278 },
        { "diametre_interieur_mm": 19.5, "nature_tuyaux": ["Acier «Standard 41» de 20"], "section_interieure_mm2": 299 },
        { "diametre_interieur_mm": 20, "nature_tuyaux": ["Cuivre 20/22", "plomb"], "section_interieure_mm2": 314 },
        { "diametre_interieur_mm": 21, "nature_tuyaux": ["P.c.v."], "section_interieure_mm2": 346 },
        { "diametre_interieur_mm": 21.6, "nature_tuyaux": ["Acier s/soud 21/27"], "section_interieure_mm2": 366 },
        { "diametre_interieur_mm": 21.8, "nature_tuyaux": ["Acier s/soud 21/27"], "section_interieure_mm2": 373 },
        { "diametre_interieur_mm": 22.2, "nature_tuyaux": ["Cuivre 24.8/28"], "section_interieure_mm2": 387 },
        { "diametre_interieur_mm": 25, "nature_tuyaux": ["Acier «Standard 41» de 26", "fonte C."], "section_interieure_mm2": 491 },
        { "diametre_interieur_mm": 26.8, "nature_tuyaux": ["P.c.v."], "section_interieure_mm2": 564 },
        { "diametre_interieur_mm": 27, "nature_tuyaux": ["Plomb", "amiante-ciment"], "section_interieure_mm2": 573 },
        { "diametre_interieur_mm": 27.2, "nature_tuyaux": ["Acier s/soud 26/34"], "section_interieure_mm2": 581 },
        { "diametre_interieur_mm": 27.9, "nature_tuyaux": ["Acier s/soud 26/34"], "section_interieure_mm2": 611 },
        { "diametre_interieur_mm": 28.8, "nature_tuyaux": ["Cuivre 28/32"], "section_interieure_mm2": 651 },
        { "diametre_interieur_mm": 30, "nature_tuyaux": ["Acier s/soud 30/34", "plomb", "fonte L"], "section_interieure_mm2": 707 },
        { "diametre_interieur_mm": 32, "nature_tuyaux": ["Cuivre 32/36", "fonte C"], "section_interieure_mm2": 804 },
        { "diametre_interieur_mm": 33.6, "nature_tuyaux": ["P.c.v."], "section_interieure_mm2": 887 },
        { "diametre_interieur_mm": 34, "nature_tuyaux": ["Cuivre 34/36"], "section_interieure_mm2": 908 },
        { "diametre_interieur_mm": 35, "nature_tuyaux": ["Acier «Standard 41» de 33"], "section_interieure_mm2": 962 },
        { "diametre_interieur_mm": 35.9, "nature_tuyaux": ["Plomb", "amiante-ciment"], "section_interieure_mm2": 1012 },
        { "diametre_interieur_mm": 36.6, "nature_tuyaux": ["Acier s/soud 33/42"], "section_interieure_mm2": 1052 },
        { "diametre_interieur_mm": 38, "nature_tuyaux": ["Cuivre 38/40", "P.c.v."], "section_interieure_mm2": 1134 },
        { "diametre_interieur_mm": 40, "nature_tuyaux": ["Plomb", "fonte", "amiante-ciment"], "section_interieure_mm2": 1257 },
        { "diametre_interieur_mm": 40.5, "nature_tuyaux": ["Acier «Standard 41» de 40"], "section_interieure_mm2": 1288 },
        { "diametre_interieur_mm": 41.8, "nature_tuyaux": ["Acier s/soud 40/49"], "section_interieure_mm2": 1372 },
        { "diametre_interieur_mm": 42.8, "nature_tuyaux": ["P.c.v."], "section_interieure_mm2": 1385 },
        { "diametre_interieur_mm": 45, "nature_tuyaux": ["Acier s/soud 40/49", "plomb"], "section_interieure_mm2": 1590 },
        { "diametre_interieur_mm": 46.8, "nature_tuyaux": ["Cuivre 46.8/50"], "section_interieure_mm2": 1720 },
        { "diametre_interieur_mm": 50, "nature_tuyaux": ["Acier «Standard 41» de 50", "plomb", "fonte", "amiante-ciment"], "section_interieure_mm2": 1963 },
        { "diametre_interieur_mm": 53, "nature_tuyaux": ["Acier s/soud 50/60", "P.c.v."], "section_interieure_mm2": 2206 },
        { "diametre_interieur_mm": 53.8, "nature_tuyaux": ["Acier s/soud 50/60"], "section_interieure_mm2": 2273 },
        { "diametre_interieur_mm": 58, "nature_tuyaux": ["Acier «Standard 41» de 60"], "section_interieure_mm2": 2642 },
        { "diametre_interieur_mm": 60, "nature_tuyaux": ["Plomb", "fonte", "amiante-ciment"], "section_interieure_mm2": 2827 }
      ]
    }
  }
}
```