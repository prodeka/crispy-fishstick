# core/formulas.py
import math
from utils.ui import print_colored

# ==============================================================================
# BIBLIOTHÈQUE DE FORMULES PARTAGÉES
# Ce fichier centralise toutes les équations mathématiques utilisées par le programme.
# ==============================================================================


# --- Section 1 : Formules de Temps de Concentration (Tc) ---

def tc_kirpich(longueur_m: float, pente: float) -> float:
    """Calcule le tc de surface avec la formule de Kirpich."""
    if pente <= 0: return 999.0
    return 0.01947 * (longueur_m**0.77) * (pente**-0.385)

def tc_californienne(longueur_m: float, pente: float) -> float:
    """Calcule le tc de surface avec la formule Californienne."""
    longueur_km = longueur_m / 1000
    if pente <= 0: return 999.0
    return 0.0663 * ((longueur_km / math.sqrt(pente))**0.77) * 60


# --- Section 2 : Formules d'Intensité-Durée-Fréquence (IDF) ---

def _calculer_intensite_montana(tc_min, params, verbose=False):
    """Calcule l'intensité avec la formule de Montana : i = a * tc^b."""
    a = params['a']
    b = params['b']
    if verbose:
        print_colored("\n   -> Calcul de l'intensité (i) via Montana :", "yellow")
        print(f"      Formule: i = a * tc^b")
        print(f"      AN     : i = {a} * {tc_min:.2f}^{b}")
    intensite = a * (tc_min ** b)
    if verbose: print(f"      Résultat: i = {intensite:.2f} mm/h")
    return intensite

def _calculer_intensite_talbot(tc_min, params, verbose=False):
    """Calcule l'intensité avec la formule de Talbot : i = a / (b + tc)."""
    a = params['a']
    b = params['b']
    if verbose:
        print_colored("\n   -> Calcul de l'intensité (i) via Talbot :", "yellow")
        print(f"      Formule: i = a / (b + tc)")
        print(f"      AN     : i = {a} / ({b} + {tc_min:.2f})")
    if (b + tc_min) == 0: intensite = float('inf')
    else: intensite = a / (b + tc_min)
    if verbose: print(f"      Résultat: i = {intensite:.2f} mm/h")
    return intensite

def _calculer_intensite_kiefer_chu(tc_min, params, verbose=False):
    """Calcule l'intensité avec la formule de Kiefer-Chu : i = a / ((tc + b)^c)."""
    a = params['a']
    b = params['b']
    c = params['c']
    if verbose:
        print_colored("\n   -> Calcul de l'intensité (i) via Kiefer-Chu :", "yellow")
        print(f"      Formule: i = a / (tc + b)^c")
        print(f"      AN     : i = {a} / ({tc_min:.2f} + {b})^{c}")
    if (tc_min + b) <= 0: intensite = float('inf')
    else: intensite = a / ((tc_min + b) ** c)
    if verbose: print(f"      Résultat: i = {intensite:.2f} mm/h")
    return intensite

def calculer_intensite_pluie(tc_min: float, idf_params: dict, verbose=False) -> float:
    """Dispatcher qui appelle la bonne formule IDF en fonction des paramètres."""
    formula = idf_params.get("formula", "montana").lower()
    
    if formula == "montana":
        return _calculer_intensite_montana(tc_min, idf_params, verbose)
    elif formula == "talbot":
        return _calculer_intensite_talbot(tc_min, idf_params, verbose)
    elif formula == "kiefer-chu":
        return _calculer_intensite_kiefer_chu(tc_min, idf_params, verbose)
    else:
        raise ValueError(f"Formule IDF non reconnue : {formula}")


# --- Section 3 : Formules de Dimensionnement Hydraulique (Manning-Strickler) ---

# Constantes de conception partagées
DIAMETRES_COMMERCIAUX_m = [
    0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 1.20, 1.50, 
    1.80, 2.00, 2.20, 2.50, 2.80, 3.00, 3.50, 4.00, 5.0, 6.0, 8.0
]
HAUTEURS_CANAL_m = [
    0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 
    2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0
]

def dimensionner_section(troncon, q_max_m3s: float, verbose=False) -> dict:
    """Routeur qui appelle la bonne fonction de dimensionnement."""
    type_section = troncon.type_section
    pente = troncon.pente_troncon
    ks = troncon.ks
    
    if type_section == 'circulaire':
        return dimensionner_circulaire(q_max_m3s, pente, ks, verbose)
    elif type_section == 'trapezoidal':
        return dimensionner_trapezoidal(q_max_m3s, pente, ks, troncon.largeur_fond_m, troncon.fruit_z, verbose)
    elif type_section == 'rectangulaire':
        return dimensionner_rectangulaire(q_max_m3s, pente, ks, troncon.largeur_fond_m, verbose)
    else:
        raise ValueError(f"Type de section non reconnu : {type_section}")

def dimensionner_circulaire(q_max_m3s, pente, ks, verbose=False):
    """Trouve le plus petit diamètre commercial pouvant évacuer le débit."""
    if verbose: print_colored("\n   -> Dimensionnement hydraulique (Section Circulaire) :", "yellow")
    for diametre in DIAMETRES_COMMERCIAUX_m:
        if verbose: print(f"\n      Test D={int(diametre*1000)}mm...")
        section_pleine = math.pi * (diametre / 2) ** 2
        rayon_hydraulique_plein = diametre / 4
        if verbose:
            print(f"         1. Section (S) = {section_pleine:.4f} m²")
            print(f"         2. Rayon Hyd. (Rh) = {rayon_hydraulique_plein:.3f} m")
        q_capacite = ks * section_pleine * (rayon_hydraulique_plein ** (2/3)) * (pente ** 0.5)
        if verbose: print(f"         3. Q_capacité calculé = {q_capacite:.3f} m³/s")
        if q_capacite >= q_max_m3s:
            if verbose: print_colored("            -> Diamètre retenu.", "green")
            vitesse = q_max_m3s / section_pleine if section_pleine > 0 else 0
            return {'diametre_mm': int(diametre * 1000), 'hauteur_m': 0, 'largeur_m': 0, 'vitesse_ms': vitesse, 'section_m2': section_pleine, 'q_capacite_m3s': q_capacite}
    raise ValueError(f"Débit trop élevé ({q_max_m3s:.3f} m³/s)")

def dimensionner_trapezoidal(q_max_m3s, pente, ks, largeur_fond, fruit_z, verbose=False):
    """Trouve la plus petite hauteur de canal trapézoïdal pouvant évacuer le débit."""
    if verbose: print_colored("\n   -> Dimensionnement hydraulique (Section Trapézoïdale) :", "yellow")
    for hauteur in HAUTEURS_CANAL_m:
        if verbose: print(f"\n      Test H={hauteur:.2f}m...")
        section_mouillee = hauteur * (largeur_fond + fruit_z * hauteur)
        perimetre_mouille = largeur_fond + 2 * hauteur * math.sqrt(1 + fruit_z**2)
        rayon_hydraulique = section_mouillee / perimetre_mouille if perimetre_mouille > 0 else 0
        if verbose:
            print(f"         1. Section (S) = {section_mouillee:.4f} m²")
            print(f"         2. Rayon Hyd. (Rh) = {rayon_hydraulique:.3f} m")
        q_capacite = ks * section_mouillee * (rayon_hydraulique ** (2/3)) * (pente ** 0.5)
        if verbose: print(f"         3. Q_capacité calculé = {q_capacite:.3f} m³/s")
        if q_capacite >= q_max_m3s:
            if verbose: print_colored("            -> Hauteur retenue.", "green")
            vitesse = q_max_m3s / section_mouillee if section_mouillee > 0 else 0
            return {'diametre_mm': 0, 'hauteur_m': hauteur, 'largeur_m': largeur_fond, 'vitesse_ms': vitesse, 'section_m2': section_mouillee, 'q_capacite_m3s': q_capacite}
    raise ValueError(f"Débit trop élevé ({q_max_m3s:.3f} m³/s)")

def dimensionner_rectangulaire(q_max_m3s, pente, ks, largeur, verbose=False):
    """Trouve la plus petite hauteur de canal rectangulaire pouvant évacuer le débit."""
    if verbose: print_colored("\n   -> Dimensionnement hydraulique (Section Rectangulaire) :", "yellow")
    for hauteur in HAUTEURS_CANAL_m:
        if verbose: print(f"\n      Test H={hauteur:.2f}m...")
        section_mouillee = largeur * hauteur
        perimetre_mouille = largeur + 2 * hauteur
        rayon_hydraulique = section_mouillee / perimetre_mouille if perimetre_mouille > 0 else 0
        if verbose:
            print(f"         1. Section (S) = {section_mouillee:.4f} m²")
            print(f"         2. Rayon Hyd. (Rh) = {rayon_hydraulique:.3f} m")
        q_capacite = ks * section_mouillee * (rayon_hydraulique ** (2/3)) * (pente ** 0.5)
        if verbose: print(f"         3. Q_capacité calculé = {q_capacite:.3f} m³/s")
        if q_capacite >= q_max_m3s:
            if verbose: print_colored("            -> Hauteur retenue.", "green")
            vitesse = q_max_m3s / section_mouillee if section_mouillee > 0 else 0
            return {'diametre_mm': 0, 'hauteur_m': hauteur, 'largeur_m': largeur, 'vitesse_ms': vitesse, 'section_m2': section_mouillee, 'q_capacite_m3s': q_capacite}
    raise ValueError(f"Débit trop élevé ({q_max_m3s:.3f} m³/s)")