# Fichier: calculs/charges.py (Version Finale Pédagogique)

# -*- coding: utf-8 -*-
import pandas as pd
import os


def charger_psi_coeffs():
    """Charge les coefficients psi depuis le fichier CSV."""
    chemin_db = os.path.join("data", "psi_coeffs.csv")
    try:
        return pd.read_csv(chemin_db)
    except FileNotFoundError:
        return None


def calculer_sollicitations_completes(
    longueur, charges, materiau, categorie_usage, verbose=True
):
    """
    Calcule toutes les combinaisons d'actions pour l'ELU et l'ELS,
    et retourne les sollicitations maximales.
    """
    if verbose:
        print("\n--- Debut du calcul des sollicitations completes ---")
        print(f"Charges d'entree: {charges}")

    M_Ed_max, V_Ed_max, p_ser_max = 0, 0, 0
    gamma_G, gamma_Q = 1.35, 1.5
    G, Q, W, S = (
        charges.get("G", 0),
        charges.get("Q", 0),
        charges.get("W", 0),
        charges.get("S", 0),
    )

    combinaisons_elu = []

    # --- Logique de combinaisons ---
    if materiau == "acier":
        # Simplifié pour l'exemple, on pourrait lister toutes les combinaisons du cours
        combinaisons_elu = [
            {"desc": "1.35G + 1.5Q", "p_Ed": gamma_G * G + gamma_Q * Q},
            {"desc": "1.35G + 1.5W", "p_Ed": gamma_G * G + gamma_Q * W},
            {"desc": "1.35G + 1.5S", "p_Ed": gamma_G * G + gamma_Q * S},
            {
                "desc": "1.35G + 1.5Q + 1.35*0.75S",
                "p_Ed": gamma_G * G + gamma_Q * Q + gamma_G * 0.75 * S,
            },
            {
                "desc": "1.35G + 1.5Q + 1.35*0.75W",
                "p_Ed": gamma_G * G + gamma_Q * Q + gamma_G * 0.75 * W,
            },
        ]
        p_ser_max = G + Q + W + S

    elif materiau == "bois":
        df_psi = charger_psi_coeffs()
        if df_psi is None:
            raise ValueError("Fichier psi_coeffs.csv introuvable.")

        psi_row = df_psi[df_psi["Categorie"] == categorie_usage]
        if psi_row.empty:
            raise ValueError(f"Categorie d'usage '{categorie_usage}' non trouvee.")

        psi0, psi2 = psi_row.iloc[0]["psi0"], psi_row.iloc[0]["psi2"]

        if verbose:
            print(
                f"Coefficients pour categorie '{categorie_usage}': psi0={psi0}, psi2={psi2}"
            )

        base_G = gamma_G * G

        # Cas 1: Q en base
        p_Ed1 = base_G + gamma_Q * Q + gamma_Q * psi0 * W + gamma_Q * psi0 * S
        formule1 = f"Formule: {gamma_G}*G + {gamma_Q}*Q + {gamma_Q}*{psi0}*W + {gamma_Q}*{psi0}*S"
        remplacement1 = f"Remplacement: {gamma_G}*{G} + {gamma_Q}*{Q} + {gamma_Q}*{psi0}*{W} + {gamma_Q}*{psi0}*{S}"
        combinaisons_elu.append(
            {
                "desc": "ELU: Q en base",
                "p_Ed": p_Ed1,
                "formule": formule1,
                "remplacement": remplacement1,
            }
        )

        # Cas 2: W en base
        p_Ed2 = base_G + gamma_Q * W + gamma_Q * psi0 * Q + gamma_Q * psi0 * S
        formule2 = f"Formule: {gamma_G}*G + {gamma_Q}*W + {gamma_Q}*{psi0}*Q + {gamma_Q}*{psi0}*S"
        remplacement2 = f"Remplacement: {gamma_G}*{G} + {gamma_Q}*{W} + {gamma_Q}*{psi0}*{Q} + {gamma_Q}*{psi0}*{S}"
        combinaisons_elu.append(
            {
                "desc": "ELU: W en base",
                "p_Ed": p_Ed2,
                "formule": formule2,
                "remplacement": remplacement2,
            }
        )

        # Cas 3: S en base
        p_Ed3 = base_G + gamma_Q * S + gamma_Q * psi0 * Q + gamma_Q * psi0 * W
        formule3 = f"Formule: {gamma_G}*G + {gamma_Q}*S + {gamma_Q}*{psi0}*Q + {gamma_Q}*{psi0}*W"
        remplacement3 = f"Remplacement: {gamma_G}*{G} + {gamma_Q}*{S} + {gamma_Q}*{psi0}*{Q} + {gamma_Q}*{psi0}*{W}"
        combinaisons_elu.append(
            {
                "desc": "ELU: S en base",
                "p_Ed": p_Ed3,
                "formule": formule3,
                "remplacement": remplacement3,
            }
        )

        p_ser_max = G + psi2 * Q + psi2 * W + psi2 * S

    if verbose:
        print("\nAnalyse des combinaisons ELU:")

    for combo in combinaisons_elu:
        p_Ed = combo["p_Ed"]
        m_ed = (p_Ed * longueur**2) / 8
        v_ed = (p_Ed * longueur) / 2

        if verbose and "formule" in combo:
            print(f"\n  - Combinaison: {combo['desc']}")
            print(f"    {combo['formule']}")
            print(f"    {combo['remplacement']} = {p_Ed:.2f} kN/m")
            print(
                f"    -> Sollicitations: M_Ed = {m_ed:.2f} kNm, V_Ed = {v_ed:.2f} kNm"
            )
        elif verbose:
            print(
                f"  - Combinaison: {combo['desc']:<25} -> p_Ed = {p_Ed:.2f} kN/m -> M_Ed = {m_ed:.2f} kNm"
            )

        if m_ed > M_Ed_max:
            M_Ed_max, V_Ed_max = m_ed, v_ed

    if verbose:
        print(
            f"\nSollicitation ELU maximale retenue: M_Ed={M_Ed_max:.2f} kNm, V_Ed={V_Ed_max:.2f} kNm"
        )
        print(f"Charge ELS retenue pour la fleche: p_ser={p_ser_max:.2f} kN/m")

    return {"M_Ed": M_Ed_max, "V_Ed": V_Ed_max, "p_ser": p_ser_max}
