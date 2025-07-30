# Fichier: calculs/acier.py
# Ce module contient les fonctions spécifiques au dimensionnement des poutres en acier.
# Il implémente les vérifications à l'ELU (Flexion, Cisaillement) et à l'ELS (Flèche).
# Les formules sont basées sur les principes de l'Eurocode 3.

# -*- coding: utf-8 -*-
import pandas as pd
import os
import math  # On importe la librairie math ici, une seule fois pour tout le fichier.


# --- FONCTION 1 : CHARGEMENT DES DONNÉES ---
def charger_profils_acier():
    """
    Lit le fichier profils_acier.csv et retourne les données sous forme de DataFrame.
    """
    chemin_db = os.path.join("data", "profils_acier.csv")
    try:
        df = pd.read_csv(chemin_db)
        return df
    except FileNotFoundError:
        return None


# --- FONCTION 2 : VÉRIFICATION COMPLÈTE ---
def trouver_profil_acier(
    M_Ed_kNm,
    V_Ed_kN,
    longueur,
    p_ser_kN_m,
    famille_profil="IPE", # Nouvel argument
    nuance="S235",
    fy_MPa=235,
    E_MPa=210000,
    verbose=True,
):
    """
    Trouve le premier profilé (IPE ou HEA) qui vérifie la flexion, le cisaillement et la flèche.
    """
    if verbose:
        print(
            f"\n--- Recherche du profilé acier ({famille_profil}) pour M_Ed = {M_Ed_kNm:.2f} kN.m, V_Ed = {V_Ed_kN:.2f} kN et L = {longueur} m ---"
        )

    df_all_profils = charger_profils_acier()
    if df_all_profils is None:
        return "Erreur: Impossible de charger les donnees des profilés."

    # Filtrer par famille de profilé
    df_profils = df_all_profils[df_all_profils['famille'] == famille_profil.upper()].copy()
    if df_profils.empty:
        return f"Erreur: Aucune donnée pour la famille de profilé '{famille_profil}'."
        
    fy = fy_MPa
    E = E_MPa
    gamma_M0 = 1.0

    if verbose:
        print(
            f"Materiau: {nuance}, Limite d'elasticite (fy): {fy} MPa, Module d'Young (E): {E} MPa"
        )

    # Conversion des unités pour les calculs
    M_Ed_Nmm = M_Ed_kNm * 1e6
    V_Ed_N = V_Ed_kN * 1000
    charge_ser_N_mm = p_ser_kN_m / 1000  # de kN/m à N/mm

    # --- Boucle de vérification sur chaque profilé ---
    for index, profil in df_profils.iterrows():
        nom_profil_test = profil["Profil"]
        if verbose:
            print(f"\n-- Test du profile: {nom_profil_test} --")

        # --- On pré-calcule toutes les résistances et déformations ---
        Wply_mm3 = profil["Wply_cm3"] * 1000
        M_pl_Rd_Nmm = (Wply_mm3 * fy) / gamma_M0

        h_mm = profil["h_mm"]
        e_ame_mm = profil["e_ame_mm"]
        Av_mm2 = h_mm * e_ame_mm
        V_pl_Rd_N = (Av_mm2 * fy) / (math.sqrt(3) * gamma_M0)

        longueur_mm = longueur * 1000
        fleche_admissible_mm = longueur_mm / 300
        I_mm4 = profil["Iy_cm4"] * 1e4
        fleche_calculee_mm = (
            (5 * charge_ser_N_mm * (longueur_mm**4)) / (384 * E * I_mm4)
            if (E > 0 and I_mm4 > 0)
            else float("inf")
        )

        # --- On définit des booléens pour savoir si les tests passent ---
        resistance_ok = M_pl_Rd_Nmm >= M_Ed_Nmm
        cisaillement_ok = V_pl_Rd_N >= V_Ed_N
        fleche_ok = fleche_calculee_mm <= fleche_admissible_mm

        # --- Maintenant, on fait l'affichage détaillé ---
        if verbose:
            print("  1. Verification de la resistance en flexion (ELU):")
            print(
                f"     Condition: {M_pl_Rd_Nmm / 1e6:.2f} kNm >= {M_Ed_kNm:.2f} kNm ? -> {'OK' if resistance_ok else 'INSUFFISANTE'}"
            )

            print("  2. Verification de l'effort tranchant (ELU):")
            print(
                f"     Condition: {V_pl_Rd_N / 1000:.2f} kN >= {V_Ed_kN:.2f} kN ? -> {'OK' if cisaillement_ok else 'INSUFFISANTE'}"
            )

            print("  3. Verification de la fleche (ELS):")
            print(
                f"     Condition: {fleche_calculee_mm:.2f} mm <= {fleche_admissible_mm:.2f} mm ? -> {'OK' if fleche_ok else 'INACCEPTABLE'}"
            )

        # --- On vérifie si TOUS les tests sont OK ---
        if resistance_ok and cisaillement_ok and fleche_ok:
            if verbose:
                print(f"\n✅ Le Profile {nom_profil_test} est valide !")
            return nom_profil_test
        else:
            if verbose:
                print(f"   -> Le profile {nom_profil_test} est rejete.")
            continue

    return "Aucun profile dans la base de donnees n'est suffisant."



# --- LE BLOC DE TEST EST MAINTENANT VIDE ou COMMENTÉ ---
if __name__ == "__main__":
    pass
