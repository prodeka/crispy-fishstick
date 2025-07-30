
import math
import numpy as np

# --- PHASE 2.1 : LOI DE GUMBEL ---
def calculer_pluie_decennale_gumbel(series_pluies_max_journalieres: list) -> float:
    """
    Calcule la hauteur de pluie décennale (P10) par la loi de GUMBEL.
    Prend en entrée une liste de pluies maximales journalières.
    """
    if not series_pluies_max_journalieres or len(series_pluies_max_journalieres) < 2:
        # Retourne une valeur par défaut ou lève une erreur si la série est trop courte
        return 0.0

    n = len(series_pluies_max_journalieres)
    moyenne = np.mean(series_pluies_max_journalieres)
    ecart_type = np.std(series_pluies_max_journalieres, ddof=1) # ddof=1 pour l'écart-type d'échantillon

    # Paramètres de Gumbel
    alpha = 1 / (0.78 * ecart_type)
    h0 = moyenne - (0.45 * ecart_type)
    
    # Pour T=10 ans, F=0.9
    f = 0.9
    # Variable réduite de Gumbel
    u = -math.log(-math.log(f))
    
    p10 = (u / alpha) + h0
    return p10

# --- PHASE 2.2 : MÉTHODE ORSTOM ---
def estimer_crue_decennale_orstom(donnees_bassin: dict, pluie_decennale: float) -> float:
    """
    Estime le débit de pointe décennal (Q10) par la méthode ORSTOM.
    Version corrigée pour la cohérence des unités.
    """
    s_km2 = donnees_bassin.get("superficie_km2", 0)
    pan_mm = donnees_bassin.get("pluvio_annuelle_mm", 0)
    ig = donnees_bassin.get("pente_globale", 0)

    if s_km2 == 0 or pan_mm == 0:
        return 0.0

    # Coeff d'abattement (alpha)
    coeff_abattement = 1 - ((161 - 0.042 * pan_mm) / 1000) * math.log10(s_km2)
    print(f"DEBUG: coeff_abattement = {coeff_abattement}")

    # Coeff de ruissellement décennal (Kr10) - CORRECTION
    # La formule précédente donnait des résultats irréalistes.
    # On utilise une approche plus simple : un coeff de base ajusté.
    # Un vrai modèle utiliserait des tables ou des formules plus complexes.
    kr10 = 0.3 * (donnees_bassin.get("pente_globale", 0.01) / 0.02)**0.5
    print(f"DEBUG: kr10 (corrigé) = {kr10}")

    # Temps de base décennal (Tb10)
    # Table (abaque) des coefficients a et b en fonction de l'indice de pente Ig
    abaque_tb10 = {
        0.002: (3.2, 5.5),
        0.005: (2.2, 4.5),
        0.01:  (1.5, 3.5),
        0.02:  (1.0, 2.5)
    }
    pentes = sorted(abaque_tb10.keys())

    if ig <= pentes[0]:
        a, b = abaque_tb10[pentes[0]]
    elif ig >= pentes[-1]:
        a, b = abaque_tb10[pentes[-1]]
    else:
        # Interpolation linéaire
        for i in range(len(pentes) - 1):
            p1, p2 = pentes[i], pentes[i+1]
            if p1 <= ig < p2:
                a1, b1 = abaque_tb10[p1]
                a2, b2 = abaque_tb10[p2]
                ratio = (ig - p1) / (p2 - p1)
                a = a1 + ratio * (a2 - a1)
                b = b1 + ratio * (b2 - b1)
                break

    print(f"DEBUG: Pour Ig={ig}, a={a:.2f}, b={b:.2f}")
    tb10_heures = a * (s_km2 ** 0.36) + b
    tb10_secondes = tb10_heures * 3600
    print(f"DEBUG: tb10_heures = {tb10_heures}")

    # Lame d'eau ruisselée (Hr10) en mm
    hr10 = kr10 * coeff_abattement * pluie_decennale
    print(f"DEBUG: hr10 = {hr10}")
    # Volume ruisselé (Vr10) en m3
    vr10_m3 = hr10 * s_km2 * 1000
    print(f"DEBUG: vr10_m3 = {vr10_m3}")
    
    # Coeff de pointe (alpha_10), généralement 2.60
    coeff_pointe = 2.60
    
    # Débit de pointe en m3/s (unités SI cohérentes)
    qr10 = coeff_pointe * (vr10_m3 / tb10_secondes)

    return qr10

# --- PLACEHOLDER POUR LES AUTRES MÉTHODES ---
def estimer_crue_decennale_cieh(donnees_bassin: dict) -> float:
    print("PLACEHOLDER: Logique de calcul C.I.E.H. à implémenter.")
    return 0.0

# --- PHASE 2.3 : EXTRAPOLATION ---
def calculer_debit_projet_centennal(debit_decennal: float, coeff_correction: float = 1.05, coeff_majoration: float = 2.0) -> float:
    """
    Extrapole le débit décennal pour obtenir le débit de projet centennal.
    """
    q10_corrige = coeff_correction * debit_decennal
    q100 = coeff_majoration * q10_corrige
    return q100

    
