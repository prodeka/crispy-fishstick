"""
Formules mathématiques pour les calculs d'Alimentation en Eau Potable (AEP)

Ce fichier contient toutes les formules mathématiques utilisées dans les calculs AEP
selon le document de référence.
"""

import math
from typing import Dict, List, Tuple, Optional
from .constants import *

# =============================================================================
# FORMULES DE PROJECTION DÉMOGRAPHIQUE
# =============================================================================

def formule_malthus(population_base: float, taux_croissance: float, annees: int) -> float:
    """
    Formule de Malthus pour la projection démographique.
    
    Formule: Pn = Po × (1 + a)^n
    
    Args:
        population_base: Population de référence (Po)
        taux_croissance: Taux d'accroissement annuel (a)
        annees: Nombre d'années (n)
    
    Returns:
        Population projetée après n années
    """
    return population_base * ((1 + taux_croissance) ** annees)

def formule_arithmetique(pop_annee1: Tuple[float, int], pop_annee2: Tuple[float, int], annee_future: int) -> float:
    """
    Formule arithmétique pour la projection démographique.
    
    Formule: y = y2 + Ku × (t - t2)
    Où: Ku = (y2 - y1) / (t2 - t1)
    
    Args:
        pop_annee1: (population, année) pour la première année
        pop_annee2: (population, année) pour la deuxième année
        annee_future: Année future pour la projection
    
    Returns:
        Population projetée
    """
    y1, t1 = pop_annee1
    y2, t2 = pop_annee2
    ku = (y2 - y1) / (t2 - t1)
    return y2 + ku * (annee_future - t2)

def formule_geometrique(pop_annee1: Tuple[float, int], pop_annee2: Tuple[float, int], annee_future: int) -> float:
    """
    Formule géométrique pour la projection démographique.
    
    Formule: y = exp(ln(y2) + Kp × (t - t2))
    Où: Kp = (ln(y2) - ln(y1)) / (t2 - t1)
    
    Args:
        pop_annee1: (population, année) pour la première année
        pop_annee2: (population, année) pour la deuxième année
        annee_future: Année future pour la projection
    
    Returns:
        Population projetée
    """
    y1, t1 = pop_annee1
    y2, t2 = pop_annee2
    kp = (math.log(y2) - math.log(y1)) / (t2 - t1)
    log_pop_future = math.log(y2) + kp * (annee_future - t2)
    return math.exp(log_pop_future)

def formule_logistique(pop_annee0: Tuple[float, int], pop_annee1: Tuple[float, int], 
                      pop_annee2: Tuple[float, int], annee_future: int) -> float:
    """
    Formule logistique pour la projection démographique.
    
    Formule: Yc = K / (1 + 10^(a - b×x))
    
    Args:
        pop_annee0: (population, année) pour l'année 0
        pop_annee1: (population, année) pour l'année 1
        pop_annee2: (population, année) pour l'année 2
        annee_future: Année future pour la projection
    
    Returns:
        Population projetée
    """
    y0, t0 = pop_annee0
    y1, t1 = pop_annee1
    y2, t2 = pop_annee2
    
    n = t1 - t0
    if (t2 - t1) != n:
        raise ValueError("L'intervalle de temps 'n' entre les recensements doit être constant.")
    
    x = annee_future - t0
    K_denom = (y0 * y2 - y1**2)
    
    if K_denom == 0:
        raise ValueError("Dénominateur nul (y0*y2 - y1^2 = 0), la méthode logistique ne peut pas s'appliquer.")
    
    K = (2 * y0 * y1 * y2 - y1**2 * (y0 + y2)) / K_denom
    
    if K <= max(y0, y1, y2):
        raise ValueError(f"Le plafond de saturation K={K:.2f} est inférieur ou égal à la population observée.")
    
    a = math.log10((K - y0) / y0)
    b = (1/n) * math.log10((y0 * (K - y1)) / (y1 * (K - y0)))
    
    return K / (1 + 10**(a - b*x))

# =============================================================================
# FORMULES DE CALCUL DES BESOINS EN EAU
# =============================================================================

def calculer_besoin_domestique(population: int, dotation_l_j_hab: float) -> float:
    """
    Calcul du besoin domestique en eau.
    
    Formule: B_dom = Population × Dotation
    
    Args:
        population: Population desservie
        dotation_l_j_hab: Dotation en litres par jour et par habitant
    
    Returns:
        Besoin domestique en m³/jour
    """
    return (population * dotation_l_j_hab) / 1000

def calculer_besoin_annexe(besoin_domestique: float, pourcentage: float = 0.10) -> float:
    """
    Calcul du besoin annexe en eau.
    
    Formule: B_a = pourcentage × B_dom
    
    Args:
        besoin_domestique: Besoin domestique en m³/jour
        pourcentage: Pourcentage du besoin domestique (défaut: 10%)
    
    Returns:
        Besoin annexe en m³/jour
    """
    return besoin_domestique * pourcentage

def calculer_besoin_global(besoin_domestique: float, besoin_annexe: float) -> float:
    """
    Calcul du besoin global en eau.
    
    Formule: B_gbl = B_dom + B_a
    
    Args:
        besoin_domestique: Besoin domestique en m³/jour
        besoin_annexe: Besoin annexe en m³/jour
    
    Returns:
        Besoin global en m³/jour
    """
    return besoin_domestique + besoin_annexe

def calculer_besoin_pointe(besoin_global: float, coefficient_pointe: float) -> float:
    """
    Calcul du besoin de pointe journalière.
    
    Formule: B_npjp = B_gbl × Cpj
    
    Args:
        besoin_global: Besoin global en m³/jour
        coefficient_pointe: Coefficient de pointe journalière
    
    Returns:
        Besoin de pointe en m³/jour
    """
    return besoin_global * coefficient_pointe

def calculer_besoin_brut(besoin_pointe: float, rendement_technique: float) -> float:
    """
    Calcul du besoin brut de production.
    
    Formule: B_bpjp = B_npjp / r_technique
    
    Args:
        besoin_pointe: Besoin de pointe en m³/jour
        rendement_technique: Rendement technique du réseau
    
    Returns:
        Besoin brut en m³/jour
    """
    return besoin_pointe / rendement_technique

def calculer_coefficient_pointe_horaire(debit_moyen_horaire: float) -> float:
    """
    Calcul du coefficient de pointe horaire selon la formule du génie rural.
    
    Formule: Cph = 1.5 + 2.5/√Qmh
    
    Args:
        debit_moyen_horaire: Débit moyen horaire en m³/h
    
    Returns:
        Coefficient de pointe horaire
    """
    return 1.5 + (2.5 / math.sqrt(debit_moyen_horaire))

def calculer_debit_adduction(besoin_brut: float, temps_distribution: float) -> float:
    """
    Calcul du débit d'adduction.
    
    Formule: Qadd = Bbpjp / Td
    
    Args:
        besoin_brut: Besoin brut en m³/jour
        temps_distribution: Temps de distribution en heures
    
    Returns:
        Débit d'adduction en m³/h
    """
    return besoin_brut / temps_distribution

def calculer_debit_pointe_horaire(debit_adduction: float, coefficient_pointe_horaire: float) -> float:
    """
    Calcul du débit de pointe horaire.
    
    Formule: Qph = Qadd × Cph
    
    Args:
        debit_adduction: Débit d'adduction en m³/h
        coefficient_pointe_horaire: Coefficient de pointe horaire
    
    Returns:
        Débit de pointe horaire en m³/h
    """
    return debit_adduction * coefficient_pointe_horaire

# =============================================================================
# FORMULES DE DIMENSIONNEMENT RÉSEAU
# =============================================================================

def calculer_pertes_charge_manning_strickler(debit_m3s: float, longueur_m: float, 
                                           diametre_m: float, ks: float) -> float:
    """
    Calcul des pertes de charge selon Manning-Strickler.
    
    Formule: ΔPt = (L×10.29359×Q²)/(Ks²×D^(16/3)) × (1+0.05)
    
    Args:
        debit_m3s: Débit en m³/s
        longueur_m: Longueur du tronçon en m
        diametre_m: Diamètre intérieur en m
        ks: Coefficient de rugosité de Strickler
    
    Returns:
        Pertes de charge en m
    """
    pertes_lineaires = (longueur_m * 10.29359 * (debit_m3s ** 2)) / ((ks ** 2) * (diametre_m ** (16/3)))
    pertes_singulieres = pertes_lineaires * 0.05  # 5% des pertes linéaires
    return pertes_lineaires + pertes_singulieres

def calculer_hauteur_manometrique_totale(hauteur_geometrique: float, pertes_charge: float) -> float:
    """
    Calcul de la hauteur manométrique totale.
    
    Formule: HMT = H_géo + ΔH_asp+ref
    
    Args:
        hauteur_geometrique: Hauteur géométrique en m
        pertes_charge: Pertes de charge en m
    
    Returns:
        Hauteur manométrique totale en m
    """
    return hauteur_geometrique + pertes_charge

def calculer_vitesse_ecoulement(debit_m3s: float, section_m2: float) -> float:
    """
    Calcul de la vitesse d'écoulement.
    
    Formule: V = Q/S
    
    Args:
        debit_m3s: Débit en m³/s
        section_m2: Section de la conduite en m²
    
    Returns:
        Vitesse en m/s
    """
    return debit_m3s / section_m2

def calculer_section_circulaire(diametre_m: float) -> float:
    """
    Calcul de la section d'une conduite circulaire.
    
    Formule: S = π × D² / 4
    
    Args:
        diametre_m: Diamètre en m
    
    Returns:
        Section en m²
    """
    return math.pi * (diametre_m ** 2) / 4

def calculer_diametre_theorique(debit_m3s: float, vitesse_m_s: float) -> float:
    """
    Calcul du diamètre théorique d'une conduite.
    
    Formule: D_théo = √(4×Q)/(V×π)
    
    Args:
        debit_m3s: Débit en m³/s
        vitesse_m_s: Vitesse en m/s
    
    Returns:
        Diamètre théorique en m
    """
    return math.sqrt((4 * debit_m3s) / (vitesse_m_s * math.pi))

# =============================================================================
# FORMULES DE DIMENSIONNEMENT RÉSERVOIR
# =============================================================================

def calculer_volume_utile(besoin_brut_jour: float, type_adduction: str) -> float:
    """
    Calcul du volume utile du réservoir.
    
    Formule: Vu = c × B_bpjp
    
    Args:
        besoin_brut_jour: Besoin brut journalier en m³
        type_adduction: Type d'adduction (nocturne, solaire, continue, jour)
    
    Returns:
        Volume utile en m³
    """
    coefficient = CAPACITE_UTILE.get(type_adduction, 0.30)
    return besoin_brut_jour * coefficient

def calculer_volume_mort(volume_utile: float) -> float:
    """
    Calcul du volume mort du réservoir.
    
    Formule: Vm = 0.02 × Vu
    
    Args:
        volume_utile: Volume utile en m³
    
    Returns:
        Volume mort en m³
    """
    return volume_utile * VOLUME_MORT_PCT

def calculer_volume_securite(besoin_brut_jour: float, duree_heures: float = 6.0) -> float:
    """
    Calcul du volume de réserve de sécurité.
    
    Formule: Vr = (B_bpjp/24) × n
    
    Args:
        besoin_brut_jour: Besoin brut journalier en m³
        duree_heures: Durée de couverture en heures
    
    Returns:
        Volume de sécurité en m³
    """
    return (besoin_brut_jour / 24) * duree_heures

def calculer_volume_total(volume_utile: float, volume_incendie: float = VOLUME_INCENDIE,
                         volume_mort: float = None, volume_securite: float = None) -> float:
    """
    Calcul du volume total du réservoir.
    
    Formule: V_total = Vu + Vi + Vm + Vr
    
    Args:
        volume_utile: Volume utile en m³
        volume_incendie: Volume incendie en m³
        volume_mort: Volume mort en m³ (calculé automatiquement si None)
        volume_securite: Volume sécurité en m³ (calculé automatiquement si None)
    
    Returns:
        Volume total en m³
    """
    if volume_mort is None:
        volume_mort = calculer_volume_mort(volume_utile)
    if volume_securite is None:
        volume_securite = calculer_volume_securite(volume_utile * 24)  # Conversion approximative
    
    return volume_utile + volume_incendie + volume_mort + volume_securite

def calculer_dimensions_reservoir_cylindrique(volume_total: float, hauteur_max: float = 12.0) -> Dict[str, float]:
    """
    Calcul des dimensions d'un réservoir cylindrique.
    
    Formule: D = √(4×V)/(π×H)
    
    Args:
        volume_total: Volume total en m³
        hauteur_max: Hauteur maximale souhaitée en m
    
    Returns:
        Dictionnaire avec diamètre et hauteur en m
    """
    # Calcul du diamètre pour une hauteur donnée
    diametre = math.sqrt((4 * volume_total) / (math.pi * hauteur_max))
    
    # Si le diamètre est trop grand, ajuster la hauteur
    if diametre > 20:  # Diamètre maximum raisonnable
        diametre = 20
        hauteur = (4 * volume_total) / (math.pi * (diametre ** 2))
    else:
        hauteur = hauteur_max
    
    return {
        "diametre_m": diametre,
        "hauteur_m": hauteur,
        "volume_total_m3": volume_total
    }

# =============================================================================
# FORMULES DE DIMENSIONNEMENT POMPAGE
# =============================================================================

def calculer_puissance_hydraulique(debit_m3s: float, hmt_m: float) -> float:
    """
    Calcul de la puissance hydraulique.
    
    Formule: Ph = ρ×g×Q×HMT
    
    Args:
        debit_m3s: Débit en m³/s
        hmt_m: Hauteur manométrique totale en m
    
    Returns:
        Puissance hydraulique en W
    """
    return RHO_EAU * G * debit_m3s * hmt_m

def calculer_puissance_electrique(puissance_hydraulique: float, rendement_pompe: float = RENDEMENT_POMPE,
                                rendement_moteur: float = RENDEMENT_MOTEUR) -> float:
    """
    Calcul de la puissance électrique.
    
    Formule: P_élec = Ph/(ηm×ηp)
    
    Args:
        puissance_hydraulique: Puissance hydraulique en W
        rendement_pompe: Rendement de la pompe
        rendement_moteur: Rendement du moteur
    
    Returns:
        Puissance électrique en W
    """
    return puissance_hydraulique / (rendement_moteur * rendement_pompe)

def calculer_puissance_groupe_electrogene(debit_m3h: float, hmt_m: float, 
                                        rendement_pompe: float = RENDEMENT_POMPE,
                                        rendement_moteur: float = RENDEMENT_MOTEUR,
                                        facteur_puissance: float = FACTEUR_PUISSANCE) -> float:
    """
    Calcul de la puissance du groupe électrogène.
    
    Formule: P_maxge = 2×(2.725×10^-3×Q×HMT)/(ηm×ηp×cosφ)
    
    Args:
        debit_m3h: Débit en m³/h
        hmt_m: Hauteur manométrique totale en m
        rendement_pompe: Rendement de la pompe
        rendement_moteur: Rendement du moteur
        facteur_puissance: Facteur de puissance (cos φ)
    
    Returns:
        Puissance du groupe électrogène en kW
    """
    numerateur = 2 * 2.725e-3 * debit_m3h * hmt_m
    denominateur = rendement_moteur * rendement_pompe * facteur_puissance
    return numerateur / denominateur

# =============================================================================
# FORMULES DE PROTECTION ANTI-BÉLIER
# =============================================================================

def calculer_celerite_ondes(diametre_mm: float, epaisseur_mm: float, k_materiau: float = K_PVC) -> float:
    """
    Calcul de la célérité des ondes.
    
    Formule: C = 9900/√(48.3 + kD/e)
    
    Args:
        diametre_mm: Diamètre de la conduite en mm
        epaisseur_mm: Épaisseur de la conduite en mm
        k_materiau: Coefficient k du matériau
    
    Returns:
        Célérité des ondes en m/s
    """
    return 9900 / math.sqrt(48.3 + (k_materiau * diametre_mm / epaisseur_mm))

def calculer_variation_pression(vitesse_initial_ms: float, celerite_ms: float) -> float:
    """
    Calcul de la variation de pression.
    
    Formule: ΔP = C × V₀/g
    
    Args:
        vitesse_initial_ms: Vitesse initiale en m/s
        celerite_ms: Célérité des ondes en m/s
    
    Returns:
        Variation de pression en mCE
    """
    return celerite_ms * vitesse_initial_ms / G

def calculer_surpression_maximale(hmt_m: float, variation_pression_m: float, niveau_dynamique_max_m: float) -> float:
    """
    Calcul de la surpression maximale.
    
    Formule: H_max = HMT + ΔP - ND_max
    
    Args:
        hmt_m: Hauteur manométrique totale en m
        variation_pression_m: Variation de pression en m
        niveau_dynamique_max_m: Niveau dynamique maximal en m
    
    Returns:
        Surpression maximale en mCE
    """
    return hmt_m + variation_pression_m - niveau_dynamique_max_m

def calculer_depression_minimale(hmt_m: float, variation_pression_m: float, niveau_dynamique_max_m: float) -> float:
    """
    Calcul de la dépression minimale.
    
    Formule: H_min = HMT - ΔP - ND_max
    
    Args:
        hmt_m: Hauteur manométrique totale en m
        variation_pression_m: Variation de pression en m
        niveau_dynamique_max_m: Niveau dynamique maximal en m
    
    Returns:
        Dépression minimale en mCE
    """
    return hmt_m - variation_pression_m - niveau_dynamique_max_m

# =============================================================================
# FORMULES DE TRAITEMENT DE L'EAU
# =============================================================================

def calculer_temps_sejour_reservoir(volume_utile_m3: float, debit_horaire_m3h: float) -> float:
    """
    Calcul du temps de séjour dans le réservoir.
    
    Formule: Tsc = Cu/Qs
    
    Args:
        volume_utile_m3: Volume utile en m³
        debit_horaire_m3h: Débit horaire en m³/h
    
    Returns:
        Temps de séjour en heures
    """
    return volume_utile_m3 / debit_horaire_m3h

def verifier_temps_contact_desinfection(temps_sejour_h: float) -> bool:
    """
    Vérification du temps de contact pour la désinfection.
    
    Condition: Tsc ≥ 2 heures
    
    Args:
        temps_sejour_h: Temps de séjour en heures
    
    Returns:
        True si le temps de contact est suffisant
    """
    return temps_sejour_h >= TEMPS_CONTACT_DESINFECTION

def verifier_duree_efficacite_desinfectant(temps_sejour_h: float) -> bool:
    """
    Vérification de la durée d'efficacité du désinfectant.
    
    Condition: Tsm < 48 heures
    
    Args:
        temps_sejour_h: Temps de séjour en heures
    
    Returns:
        True si la durée d'efficacité est respectée
    """
    return temps_sejour_h < DUREE_EFFICACITE_DESINFECTANT 