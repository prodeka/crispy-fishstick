# Guide Algorithmique Détaillé : Module `cm` (Charpente Métallique)

## 1. Vérification des Poteaux (Compression et Flambement)

**Commande :** `lcpi cm check-poteau --filepath <fichier.yml>`

**Exemple de `fichier.yml` :**
```yaml
description: "Vérification d'un poteau IPE 200 en compression"
profil:
  nom: "IPE 200"
materiau:
  nuance: "S235"  # Pour obtenir σe = 240 MPa
longueurs_flambement:
  Lf_y_m: 3.0  # Longueur de flambement dans le plan fort (autour de l'axe y-y)
  Lf_z_m: 3.0  # Longueur de flambement dans le plan faible (autour de l'axe z-z)
efforts:
  N_ed_kN: 150 # Effort de compression appliqué
```

**Algorithme / Pseudo-code :**

```plaintext
FONCTION check_poteau(donnees_entree):
    // --- ÉTAPE 1 : EXTRACTION DES DONNÉES D'ENTRÉE ---
    N_Ed_N = lire_depuis_yaml(donnees_entree, "efforts.N_ed_kN") * 1000 // en N
    nom_profil = lire_depuis_yaml(donnees_entree, "profil.nom")
    nuance_acier = lire_depuis_yaml(donnees_entree, "materiau.nuance")
    Lf_y_mm = lire_depuis_yaml(donnees_entree, "longueurs_flambement.Lf_y_m") * 1000
    Lf_z_mm = lire_depuis_yaml(donnees_entree, "longueurs_flambement.Lf_z_m") * 1000

    // --- ÉTAPE 2 : CHARGEMENT DES PROPRIÉTÉS (selon les tables du document) ---
    profil_data = charger_profil_depuis_db(nom_profil)
    A_mm2 = profil_data["Section A (cm²)"] * 100
    iy_mm = profil_data["Rayon de giration iy (cm)"] * 10
    iz_mm = profil_data["Rayon de giration iz (cm)"] * 10
    acier_data = charger_nuance_depuis_db(nuance_acier)
    sigma_e_MPa = acier_data["resistance_elastique_σe_MPa"]

    // --- ÉTAPE 3 : CALCUL DE LA CONTRAINTE APPLIQUÉE ---
    sigma_c_appliquee = N_Ed_N / A_mm2 // en MPa (N/mm²)

    // --- ÉTAPE 4 : VÉRIFICATION AU FLAMBEMENT (selon Page 101) ---
    lambda_z = Lf_z_mm / iz_mm
    k_z = calculer_coefficient_k(lambda_z, sigma_e_MPa)
    sigma_adm_z = k_z * sigma_e_MPa
    ratio_flambement_z = sigma_c_appliquee / sigma_adm_z
    lambda_y = Lf_y_mm / iy_mm
    k_y = calculer_coefficient_k(lambda_y, sigma_e_MPa)
    sigma_adm_y = k_y * sigma_e_MPa
    ratio_flambement_y = sigma_c_appliquee / sigma_adm_y

    // --- ÉTAPE 5 : SYNTHÈSE DES RÉSULTATS ---
    RENVOYER {
        "contrainte_appliquee_MPa": sigma_c_appliquee,
        "verification_flambement_plan_faible (axe z)": {
            "elancement_lambda_z": lambda_z,
            "coefficient_k_z": k_z,
            "contrainte_admissible_MPa": sigma_adm_z,
            "ratio": ratio_flambement_z,
            "statut": "OK" si ratio_flambement_z <= 1.0 SINON "NON OK"
        },
        "verification_flambement_plan_fort (axe y)": {
            "elancement_lambda_y": lambda_y,
            "coefficient_k_y": k_y,
            "contrainte_admissible_MPa": sigma_adm_y,
            "ratio": ratio_flambement_y,
            "statut": "OK" si ratio_flambement_y <= 1.0 SINON "NON OK"
        }
    }

FONCTION calculer_coefficient_k(lambda, sigma_e):
    lambda_0 = PI * sqrt(210000 / sigma_e)
    SI lambda <= 20 ALORS:
        k = 1.0
    SINON SI 20 < lambda <= lambda_0:
        k = 1 - ( (1 - 0.6 * (lambda_0/100)) / (lambda_0 - 20) ) * (lambda - 20)
    SINON SI lambda_0 < lambda <= 150:
        k = 0.6 * (lambda_0/100) * (150 - lambda) / (150 - lambda_0)
    SINON:
        k = (9000 / lambda^2)
    RENVOYER k
```

---

## 2. Vérification au Déversement (Poutres Fléchies)

**Commande :** `lcpi cm check-deversement`

**Logique d'implémentation fidèle :**

```plaintext
FONCTION check_deversement(donnees_entree):
    AFFICHER "AVERTISSEMENT : La vérification au déversement (flambement latéral-torsionnel) n'est pas décrite dans le document de référence 'Calcul des structures métalliques/Master-FORMATEC'."
    AFFICHER "La vérification se limitera à la résistance de la section en flexion élastique (Chapitre 6, Section 1-1)."
    // ... extraire My_Ed, nom_profil, nuance_acier ...
    // ... charger Wel,y et sigma_e ...
    sigma_flexion = (My_Ed_Nm * 1e6) / (Wel_y_mm3)
    ratio = sigma_flexion / sigma_e
    RENVOYER {
        "type_verification": "Résistance de section en flexion élastique (non déversement)",
        "ratio": ratio,
        "statut": "OK" si ratio <= 1.0 SINON "NON OK"
    }
```

---

## 3. Vérification des Éléments Tendus

**Commande :** `lcpi cm check-tendu --filepath <fichier.yml>`

**Logique d'implémentation fidèle :**

```plaintext
FONCTION check_tendu(donnees_entree):
    N_Ed_N = lire_depuis_yaml(donnees_entree, "efforts.N_ed_kN") * 1000
    nom_profil = lire_depuis_yaml(donnees_entree, "profil.nom")
    nuance_acier = lire_depuis_yaml(donnees_entree, "materiau.nuance")
    profil_data = charger_profil_depuis_db(nom_profil)
    A_brute_mm2 = profil_data["Section A (cm²)"] * 100
    acier_data = charger_nuance_depuis_db(nuance_acier)
    sigma_e_MPa = acier_data["resistance_elastique_σe_MPa"]
    sigma_t_appliquee = N_Ed_N / A_brute_mm2
    sigma_adm = sigma_e_MPa
    ratio_traction = sigma_t_appliquee / sigma_adm
    RENVOYER {
        "note": "La vérification est basée sur la résistance élastique de la section brute (A), conformément à la méthodologie principale du document. La rupture sur section nette (An) n'est pas explicitement formulée.",
        "contrainte_appliquee_MPa": sigma_t_appliquee,
        "contrainte_admissible_MPa": sigma_adm,
        "ratio": ratio_traction,
        "statut": "OK" si ratio_traction <= 1.0 SINON "NON OK"
    }
```

---

## 4. Vérification des Sollicitations Composées (Flexion + Effort Normal)

**Commande :** `lcpi cm check-compose --filepath <fichier.yml>`

**Algorithme / Pseudo-code :**

```plaintext
FONCTION check_flexion_composee(donnees_entree):
    N_Ed_N = lire_depuis_yaml(donnees_entree, "efforts.N_ed_kN") * 1000
    My_Ed_Nmm = lire_depuis_yaml(donnees_entree, "efforts.My_ed_kNm") * 1e6
    Mz_Ed_Nmm = lire_depuis_yaml(donnees_entree, "efforts.Mz_ed_kNm", defaut=0)
    // ... charger A, W_pl,y, W_pl,z, σe, et les dimensions du profil ...
    N_pl_Rd = A_mm2 * sigma_e_MPa
    M_pl_y_Rd = W_pl_y_mm3 * sigma_e_MPa
    M_pl_z_Rd = W_pl_z_mm3 * sigma_e_MPa
    // --- CAS 1: Flexion composée (N + My) ---
    SI Mz_Ed_Nmm == 0:
        n = N_Ed_N / N_pl_Rd
        a = calculer_ratio_aire_ame(profil_data)
        SI n <= a:
            M_Ny_Rd = M_pl_y_Rd
        SINON:
            M_Ny_Rd = M_pl_y_Rd * (1 - n) / (1 - a)
        ratio_interaction_N_My = My_Ed_Nmm / M_Ny_Rd
        RENVOYER { "type_verification": "Flexion composée (N+My)", "ratio": ratio_interaction_N_My, ... }
    // --- CAS 2: Flexion déviée (My + Mz) ---
    SINON SI N_Ed_N == 0:
        alpha = 1.0
        beta = 1.0
        ratio_interaction_My_Mz = (My_Ed_Nmm / M_pl_y_Rd)^alpha + (Mz_Ed_Nmm / M_pl_z_Rd)^beta
        RENVOYER { "type_verification": "Flexion déviée (My+Mz)", "note": "Alpha et Beta pris égaux à 1.0", "ratio": ratio_interaction_My_Mz, ... }
    // --- CAS 3: Sollicitation complète (N + My + Mz) ---
    SINON:
        RENVOYER { "type_verification": "NON SUPPORTÉ", "note": "L'interaction N+My+Mz n'est pas décrite dans le document." }
```