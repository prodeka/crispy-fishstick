
import math
import numpy as np
from scipy.optimize import fsolve

G = 9.81  # Accélération de la pesanteur

def calculer_pertes_charge_lineaires(debit_m3s: float, diametre_m: float, longueur_m: float, 
                                   rugosite_mm: float = 0.1, viscosite_m2s: float = 1.004e-6) -> dict:
    """
    Calcule les pertes de charge linéaires selon l'équation de Colebrook-White.
    
    Args:
        debit_m3s: Débit en m³/s
        diametre_m: Diamètre intérieur en m
        longueur_m: Longueur de la conduite en m
        rugosite_mm: Rugosité absolue en mm
        viscosite_m2s: Viscosité cinématique en m²/s
    
    Returns:
        dict: Résultats du calcul
    """
    # Calcul de la vitesse
    aire = math.pi * (diametre_m**2) / 4
    vitesse = debit_m3s / aire
    
    # Nombre de Reynolds
    reynolds = (vitesse * diametre_m) / viscosite_m2s
    
    # Rugosité relative
    rugosite_relative = (rugosite_mm / 1000) / diametre_m
    
    # Coefficient de frottement par itération (équation de Colebrook-White)
    def colebrook(lambda_val):
        return 1/math.sqrt(lambda_val) + 2 * math.log10(rugosite_relative/3.7 + 2.51/(reynolds * math.sqrt(lambda_val)))
    
    # Valeur initiale pour l'itération
    lambda_val = 0.02
    for _ in range(10):
        lambda_val = 1 / (2 * math.log10(rugosite_relative/3.7 + 2.51/(reynolds * math.sqrt(lambda_val))))**2
    
    # Pertes de charge linéaires
    pertes_charge = lambda_val * (longueur_m / diametre_m) * (vitesse**2 / (2 * G))
    
    return {
        "statut": "OK",
        "vitesse_ms": round(vitesse, 2),
        "nombre_reynolds": int(reynolds),
        "coefficient_frottement": round(lambda_val, 4),
        "pertes_charge_m": round(pertes_charge, 3),
        "regime": "Turbulent" if reynolds > 4000 else "Laminaire" if reynolds < 2300 else "Transition"
    }

def calculer_pertes_charge_singulieres(vitesse_ms: float, coefficients_k: dict) -> dict:
    """
    Calcule les pertes de charge singulières.
    
    Args:
        vitesse_ms: Vitesse d'écoulement en m/s
        coefficients_k: Dictionnaire des coefficients K pour chaque singularité
    
    Returns:
        dict: Résultats du calcul
    """
    pertes_totales = 0
    details = {}
    
    for nom, k in coefficients_k.items():
        perte = k * (vitesse_ms**2 / (2 * G))
        pertes_totales += perte
        details[nom] = {"coefficient_k": k, "perte_m": round(perte, 3)}
    
    return {
        "statut": "OK",
        "pertes_totales_m": round(pertes_totales, 3),
        "details_singularites": details
    }

def calculer_courbe_remous(debit_m3s: float, largeur_m: float, pente_m_m: float, 
                          rugosite_manning: float, profondeur_aval_m: float, 
                          longueur_calcul_m: float, pas_m: float = 1.0) -> dict:
    """
    Calcule une courbe de remous par la méthode de la différence finie.
    
    Args:
        debit_m3s: Débit en m³/s
        largeur_m: Largeur du canal en m
        pente_m_m: Pente du fond en m/m
        rugosite_manning: Coefficient de Manning
        profondeur_aval_m: Profondeur d'eau à l'aval en m
        longueur_calcul_m: Longueur sur laquelle calculer la courbe en m
        pas_m: Pas de calcul en m
    
    Returns:
        dict: Résultats du calcul
    """
    # Profondeur critique
    profondeur_critique = ((debit_m3s / largeur_m)**2 / G)**(1/3)
    
    # Profondeur normale (approximation)
    def profondeur_normale(h):
        aire = largeur_m * h
        perimetre = largeur_m + 2 * h
        rayon_hydraulique = aire / perimetre
        debit_calcule = (1/rugosite_manning) * aire * (rayon_hydraulique**(2/3)) * (pente_m_m**0.5)
        return debit_calcule - debit_m3s
    
    profondeur_normale_m = fsolve(profondeur_normale, profondeur_critique)[0]
    
    # Calcul de la courbe de remous
    points = []
    profondeur_courante = profondeur_aval_m
    distance_courante = 0
    
    while distance_courante <= longueur_calcul_m:
        aire = largeur_m * profondeur_courante
        perimetre = largeur_m + 2 * profondeur_courante
        rayon_hydraulique = aire / perimetre
        vitesse = debit_m3s / aire
        
        # Énergie spécifique
        energie_specifique = profondeur_courante + (vitesse**2 / (2 * G))
        
        # Pente de frottement
        pente_frottement = (vitesse * rugosite_manning / (rayon_hydraulique**(2/3)))**2
        
        points.append({
            "distance_m": round(distance_courante, 1),
            "profondeur_m": round(profondeur_courante, 3),
            "vitesse_ms": round(vitesse, 2),
            "energie_specifique_m": round(energie_specifique, 3),
            "nombre_froude": round(vitesse / math.sqrt(G * profondeur_courante), 2)
        })
        
        # Calcul du pas suivant (méthode simplifiée)
        if distance_courante < longueur_calcul_m:
            # Approximation de la dérivée de la profondeur
            dh_dx = (pente_m_m - pente_frottement) / (1 - (debit_m3s**2 * largeur_m) / (G * aire**3))
            profondeur_courante += dh_dx * pas_m
            distance_courante += pas_m
    
    return {
        "statut": "OK",
        "profondeur_critique_m": round(profondeur_critique, 3),
        "profondeur_normale_m": round(profondeur_normale_m, 3),
        "regime": "Fluvial" if profondeur_aval_m > profondeur_critique else "Torrentiel",
        "courbe_remous": points
    }

def verifier_stabilite_talus(hauteur_m: float, pente_talus: float, angle_frottement_deg: float, 
                           cohesion_kpa: float, poids_volumique_kn_m3: float = 20.0) -> dict:
    """
    Vérifie la stabilité d'un talus selon la méthode de Bishop simplifiée.
    
    Args:
        hauteur_m: Hauteur du talus en m
        pente_talus: Pente du talus (H/V)
        angle_frottement_deg: Angle de frottement interne en degrés
        cohesion_kpa: Cohésion en kPa
        poids_volumique_kn_m3: Poids volumique en kN/m³
    
    Returns:
        dict: Résultats de la vérification
    """
    angle_frottement_rad = math.radians(angle_frottement_deg)
    angle_talus_rad = math.atan(1 / pente_talus)
    
    # Calcul du coefficient de sécurité selon Bishop simplifié
    # Formule simplifiée pour un talus homogène
    if angle_talus_rad <= angle_frottement_rad:
        # Talus stable par frottement seul
        fs_frottement = math.tan(angle_frottement_rad) / math.tan(angle_talus_rad)
        fs_cohesion = (4 * cohesion_kpa) / (poids_volumique_kn_m3 * hauteur_m * math.sin(2 * angle_talus_rad))
        coefficient_securite = fs_frottement + fs_cohesion
    else:
        coefficient_securite = 0  # Instable
    
    return {
        "statut": "OK",
        "coefficient_securite": round(coefficient_securite, 2),
        "stabilite": "Stable" if coefficient_securite > 1.3 else "Instable" if coefficient_securite < 1.0 else "Limite",
        "angle_talus_deg": round(math.degrees(angle_talus_rad), 1),
        "hauteur_critique_m": round((4 * cohesion_kpa) / (poids_volumique_kn_m3 * math.sin(2 * angle_talus_rad)), 2) if angle_talus_rad <= angle_frottement_rad else None
    }

def calculer_debit_critique(largeur_m: float, profondeur_m: float, pente_m_m: float, 
                           rugosite_manning: float) -> dict:
    """
    Calcule le débit critique pour un canal rectangulaire.
    
    Args:
        largeur_m: Largeur du canal en m
        profondeur_m: Profondeur d'eau en m
        pente_m_m: Pente du fond en m/m
        rugosite_manning: Coefficient de Manning
    
    Returns:
        dict: Résultats du calcul
    """
    # Débit critique selon la théorie
    aire = largeur_m * profondeur_m
    perimetre = largeur_m + 2 * profondeur_m
    rayon_hydraulique = aire / perimetre
    
    # Débit selon Manning
    debit_manning = (1/rugosite_manning) * aire * (rayon_hydraulique**(2/3)) * (pente_m_m**0.5)
    
    # Vitesse critique
    vitesse_critique = math.sqrt(G * profondeur_m)
    
    # Débit critique théorique
    debit_critique = largeur_m * profondeur_m * vitesse_critique
    
    return {
        "statut": "OK",
        "debit_manning_m3s": round(debit_manning, 2),
        "debit_critique_m3s": round(debit_critique, 2),
        "vitesse_critique_ms": round(vitesse_critique, 2),
        "nombre_froude": round(debit_manning / (largeur_m * profondeur_m * vitesse_critique), 2),
        "regime": "Fluvial" if debit_manning < debit_critique else "Torrentiel"
    }

    
