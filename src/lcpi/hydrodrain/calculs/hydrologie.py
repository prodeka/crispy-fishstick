
import math
import numpy as np
from scipy import stats
import pandas as pd

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

import math
import numpy as np
from scipy import stats
import pandas as pd

def calculer_debit_crue_methode_rationale(superficie_km2: float, intensite_pluie_mm_h: float, 
                                        coefficient_ruissellement: float) -> dict:
    """
    Calcule le débit de crue par la méthode rationnelle.
    
    Args:
        superficie_km2: Superficie du bassin versant en km²
        intensite_pluie_mm_h: Intensité de pluie en mm/h
        coefficient_ruissellement: Coefficient de ruissellement (0-1)
    
    Returns:
        dict: Résultats du calcul
    """
    # Conversion des unités
    superficie_m2 = superficie_km2 * 1e6
    intensite_ms = intensite_pluie_mm_h / (1000 * 3600)  # mm/h vers m/s
    
    # Débit de crue
    debit_crue = coefficient_ruissellement * intensite_ms * superficie_m2
    
    return {
        "statut": "OK",
        "debit_crue_m3s": round(debit_crue, 2),
        "superficie_km2": superficie_km2,
        "intensite_pluie_mm_h": intensite_pluie_mm_h,
        "coefficient_ruissellement": coefficient_ruissellement,
        "methode": "Rationnelle"
    }

def calculer_debit_crue_methode_snyder(superficie_km2: float, longueur_cours_eau_km: float, 
                                     pente_moyenne_m_km: float, coefficient_regional: float = 0.75) -> dict:
    """
    Calcule le débit de crue par la méthode de Snyder.
    
    Args:
        superficie_km2: Superficie du bassin versant en km²
        longueur_cours_eau_km: Longueur du cours d'eau principal en km
        pente_moyenne_m_km: Pente moyenne du cours d'eau en m/km
        coefficient_regional: Coefficient régional (0.5-1.0)
    
    Returns:
        dict: Résultats du calcul
    """
    # Temps de concentration (formule de Kirpich modifiée)
    temps_concentration_h = 0.0195 * (longueur_cours_eau_km**0.77) * (pente_moyenne_m_km**(-0.385))
    
    # Temps de base
    temps_base_h = 3 * temps_concentration_h
    
    # Débit de pointe (formule simplifiée)
    debit_pointe_m3s = coefficient_regional * (superficie_km2**0.8) * (temps_concentration_h**(-0.5))
    
    return {
        "statut": "OK",
        "debit_pointe_m3s": round(debit_pointe_m3s, 2),
        "temps_concentration_h": round(temps_concentration_h, 2),
        "temps_base_h": round(temps_base_h, 2),
        "superficie_km2": superficie_km2,
        "longueur_cours_eau_km": longueur_cours_eau_km,
        "pente_moyenne_m_km": pente_moyenne_m_km,
        "coefficient_regional": coefficient_regional,
        "methode": "Snyder"
    }

def ajuster_loi_statistique(series_debits: list, loi: str = "gumbel") -> dict:
    """
    Ajuste une série de débits à une loi statistique.
    
    Args:
        series_debits: Liste des débits maximaux annuels
        loi: Type de loi ("gumbel", "log-normal", "pearson3")
    
    Returns:
        dict: Paramètres de la loi ajustée
    """
    if loi.lower() == "gumbel":
        # Ajustement à la loi de Gumbel
        moyenne = np.mean(series_debits)
        ecart_type = np.std(series_debits, ddof=1)
        
        # Paramètres de la loi de Gumbel
        alpha = ecart_type / 1.2825
        u_param = moyenne - 0.5772 * alpha
        
        # Test de qualité d'ajustement (Kolmogorov-Smirnov)
        def gumbel_cdf(x, u, alpha):
            return np.exp(-np.exp(-(x - u) / alpha))
        
        ks_stat, p_value = stats.kstest(series_debits, lambda x: gumbel_cdf(x, u_param, alpha))
        
        return {
            "statut": "OK",
            "loi": "Gumbel",
            "parametres": {
                "alpha": round(alpha, 4),
                "u": round(u_param, 4)
            },
            "qualite_ajustement": {
                "ks_statistique": round(ks_stat, 4),
                "p_value": round(p_value, 4),
                "acceptable": p_value > 0.05
            }
        }
    
    elif loi.lower() == "log-normal":
        # Ajustement à la loi log-normale
        log_debits = np.log(series_debits)
        mu_log = np.mean(log_debits)
        sigma_log = np.std(log_debits, ddof=1)
        
        # Test de qualité d'ajustement
        ks_stat, p_value = stats.kstest(series_debits, lambda x: stats.lognorm.cdf(x, sigma_log, scale=np.exp(mu_log)))
        
        return {
            "statut": "OK",
            "loi": "Log-Normale",
            "parametres": {
                "mu_log": round(mu_log, 4),
                "sigma_log": round(sigma_log, 4)
            },
            "qualite_ajustement": {
                "ks_statistique": round(ks_stat, 4),
                "p_value": round(p_value, 4),
                "acceptable": p_value > 0.05
            }
        }
    
    else:
        return {"statut": "Erreur", "message": f"Loi '{loi}' non supportée"}

def calculer_debit_periode_retour(parametres_loi: dict, periode_retour_ans: float) -> dict:
    """
    Calcule le débit pour une période de retour donnée.
    
    Args:
        parametres_loi: Paramètres de la loi statistique ajustée
        periode_retour_ans: Période de retour en années
    
    Returns:
        dict: Débit calculé
    """
    loi = parametres_loi.get("loi")
    
    if loi == "Gumbel":
        alpha = parametres_loi["parametres"]["alpha"]
        u = parametres_loi["parametres"]["u"]
        
        # Variable réduite de Gumbel
        y_t = -np.log(-np.log(1 - 1/periode_retour_ans))
        
        # Débit pour la période de retour
        debit = u + alpha * y_t
        
        return {
            "statut": "OK",
            "debit_m3s": round(debit, 2),
            "periode_retour_ans": periode_retour_ans,
            "loi": loi
        }
    
    elif loi == "Log-Normale":
        mu_log = parametres_loi["parametres"]["mu_log"]
        sigma_log = parametres_loi["parametres"]["sigma_log"]
        
        # Quantile de la loi normale standard
        proba = 1 - 1/periode_retour_ans
        z = stats.norm.ppf(proba)
        
        # Débit pour la période de retour
        debit = np.exp(mu_log + sigma_log * z)
        
        return {
            "statut": "OK",
            "debit_m3s": round(debit, 2),
            "periode_retour_ans": periode_retour_ans,
            "loi": loi
        }
    
    else:
        return {"statut": "Erreur", "message": f"Loi '{loi}' non supportée"}

def calculer_courbe_tarage(hauteurs_m: list, debits_m3s: list) -> dict:
    """
    Calcule une courbe de tarage à partir de mesures hauteur-débit.
    
    Args:
        hauteurs_m: Liste des hauteurs d'eau en m
        debits_m3s: Liste des débits correspondants en m³/s
    
    Returns:
        dict: Paramètres de la courbe de tarage
    """
    if len(hauteurs_m) != len(debits_m3s) or len(hauteurs_m) < 2:
        return {"statut": "Erreur", "message": "Données insuffisantes"}
    
    # Ajustement par régression non-linéaire (loi puissance)
    # Q = a * H^b
    log_h = np.log(hauteurs_m)
    log_q = np.log(debits_m3s)
    
    # Régression linéaire sur les logarithmes
    coeffs = np.polyfit(log_h, log_q, 1)
    b = coeffs[0]
    a = np.exp(coeffs[1])
    
    # Calcul du coefficient de détermination
    q_calcules = [a * h**b for h in hauteurs_m]
    r2 = 1 - sum((np.array(debits_m3s) - np.array(q_calcules))**2) / sum((np.array(debits_m3s) - np.mean(debits_m3s))**2)
    
    return {
        "statut": "OK",
        "equation": f"Q = {a:.3f} * H^{b:.3f}",
        "parametres": {
            "a": round(a, 4),
            "b": round(b, 4)
        },
        "qualite_ajustement": {
            "r2": round(r2, 4),
            "excellent": r2 > 0.95,
            "bon": r2 > 0.90
        }
    }

def calculer_debit_par_courbe_tarage(hauteur_m: float, parametres_courbe: dict) -> dict:
    """
    Calcule le débit à partir d'une hauteur d'eau et des paramètres de la courbe de tarage.
    
    Args:
        hauteur_m: Hauteur d'eau en m
        parametres_courbe: Paramètres de la courbe de tarage
    
    Returns:
        dict: Débit calculé
    """
    a = parametres_courbe["parametres"]["a"]
    b = parametres_courbe["parametres"]["b"]
    
    debit = a * (hauteur_m**b)
    
    return {
        "statut": "OK",
        "hauteur_m": hauteur_m,
        "debit_m3s": round(debit, 2),
        "equation": parametres_courbe["equation"]
    }

def analyser_serie_temporelle(filepath: str, colonne_debit: str = "debit", colonne_date: str = "date") -> dict:
    """
    Analyse une série temporelle de débits.
    
    Args:
        filepath: Chemin vers le fichier CSV
        colonne_debit: Nom de la colonne contenant les débits
        colonne_date: Nom de la colonne contenant les dates
    
    Returns:
        dict: Résultats de l'analyse
    """
    try:
        df = pd.read_csv(filepath)
        
        if colonne_debit not in df.columns:
            return {"statut": "Erreur", "message": f"Colonne '{colonne_debit}' non trouvée"}
        
        debits = df[colonne_debit].dropna()
        
        # Statistiques descriptives
        stats_desc = {
            "moyenne_m3s": round(debits.mean(), 2),
            "mediane_m3s": round(debits.median(), 2),
            "ecart_type_m3s": round(debits.std(), 2),
            "minimum_m3s": round(debits.min(), 2),
            "maximum_m3s": round(debits.max(), 2),
            "coefficient_variation": round(debits.std() / debits.mean(), 3)
        }
        
        # Débits caractéristiques
        debits_caracteristiques = {
            "debit_moyen_m3s": round(debits.mean(), 2),
            "debit_median_m3s": round(debits.median(), 2),
            "debit_95_percentile_m3s": round(debits.quantile(0.95), 2),
            "debit_5_percentile_m3s": round(debits.quantile(0.05), 2)
        }
        
        return {
            "statut": "OK",
            "nombre_mesures": len(debits),
            "statistiques_descriptives": stats_desc,
            "debits_caracteristiques": debits_caracteristiques
        }
        
    except Exception as e:
        return {"statut": "Erreur", "message": str(e)}

    
