"""
Constantes pour les calculs d'Alimentation en Eau Potable (AEP)

Ce fichier contient toutes les constantes utilisées dans les calculs AEP
selon le document de référence et les standards techniques.
"""

import math

# =============================================================================
# CONSTANTES PHYSIQUES
# =============================================================================

# Accélération de la pesanteur (m/s²)
G = 9.81
G_ACCELERATION_GRAVITE = 9.81

# Masse volumique de l'eau (kg/m³)
RHO_EAU = 1000.0

# Viscosité cinématique de l'eau (m²/s) à 20°C
VISCOSITE_CINEMATIQUE_EAU = 1.006e-6

# Module d'élasticité de l'eau (Pa)
EPSILON_EAU = 2.0e9

# Module d'élasticité PVC (Pa) 
E_PVC = 3.0e9

# =============================================================================
# COEFFICIENTS DE RUGOSITÉ (Manning-Strickler)
# =============================================================================

# PVC (selon document AEP)
KS_PVC = 120

# Béton lissé
KS_BETON_LISSE = 80

# Béton brut
KS_BETON_BRUT = 60

# Acier galvanisé
KS_ACIER_GALVANISE = 100

# Fonte
KS_FONTE = 90

# =============================================================================
# COEFFICIENTS DE POINTE
# =============================================================================

# Coefficient de pointe journalière (document AEP)
COEFF_POINTE_JOURNALIERE = 1.5

# Coefficient de pointe horaire (formule génie rural)
# Cph = 1.5 + 2.5/√Qmh
# Où Qmh est le débit moyen horaire en m³/h

# =============================================================================
# RENDEMENTS TECHNIQUES
# =============================================================================

# Rendement technique du réseau (document AEP)
RENDEMENT_TECHNIQUE = 0.95  # 95% = 5% de pertes

# Rendement pompe (typique)
RENDEMENT_POMPE = 0.75

# Rendement moteur (typique)
RENDEMENT_MOTEUR = 0.85

# Facteur de puissance (cos φ)
FACTEUR_PUISSANCE = 0.85

# =============================================================================
# PRESSIONS ET VITESSES
# =============================================================================

# Pression de service minimale (TdE)
PRESSION_SERVICE_MIN = 10.0  # mCE (1 bar)

# Vitesse minimale dans les conduites (m/s)
VITESSE_MIN = 0.3

# Vitesse maximale dans les conduites (m/s)
VITESSE_MAX = 1.5

# Vitesse maximale selon Flamant (m/s)
# V ≤ 0.6 + D_théo

# =============================================================================
# PARAMÈTRES DE DIMENSIONNEMENT RÉSERVOIR
# =============================================================================

# Capacité utile selon type d'adduction (document AEP)
CAPACITE_UTILE = {
    "adduction_nocturne": 0.90,      # 90% du volume journalier
    "adduction_solaire": 0.50,       # 50% du volume journalier (8h/j)
    "adduction_continue": 0.30,      # 30% du volume journalier
    "adduction_jour": 0.20           # 10-30% du volume journalier
}

# Volume de réserve incendie (m³)
VOLUME_INCENDIE = 7.2  # Volume d'incendie standard en m³

# Volume mort (% du volume utile)
VOLUME_MORT_PCT = 0.02  # 2%

# Durée de couverture de sécurité (heures)
DUREE_COUVERTURE_SECURITE = 6.0

# =============================================================================
# PARAMÈTRES DE TRAITEMENT
# =============================================================================

# Dosage chlore (mg/l) - OMS
DOSAGE_CHLORE = 2.0

# Chlore résiduel libre (mg/l) - OMS
CHLORE_RESIDUEL = 0.5

# Temps de contact pour désinfection (heures)
TEMPS_CONTACT_DESINFECTION = 2.0

# Durée d'efficacité du désinfectant (heures)
DUREE_EFFICACITE_DESINFECTANT = 48.0

# =============================================================================
# PARAMÈTRES DE PROTECTION ANTI-BÉLIER
# =============================================================================

# Coefficient k pour PVC (document AEP)
K_PVC = 33

# =============================================================================
# DIAMÈTRES COMMERCIAUX (mm)
# =============================================================================

DIAMETRES_COMMERCIAUX_MM = [
    80, 100, 125, 150, 200, 250, 300, 350, 400, 450, 500,
    600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000
]

# =============================================================================
# DOTATIONS EN EAU (L/jour/habitant)
# =============================================================================

DOTATIONS_EAU = {
    "branchement_prive": 60.0,      # Document AEP
    "borne_fontaine": 20.0,         # Valeur typique
    "milieu_rural": 40.0,           # Valeur typique
    "milieu_urbain": 150.0,         # Valeur typique
    "milieu_industriel": 200.0      # Valeur typique
}

# =============================================================================
# COEFFICIENTS DE DÉBIT (DÉVERSOIRS)
# =============================================================================

COEFFS_DEBIT_DEVERSOIR = {
    "creager": 0.49,
    "seuil_epais": 0.35,
    "paroi_mince": 0.40
}

# =============================================================================
# FORMULES DE DIMENSIONNEMENT DIAMÈTRE THÉORIQUE
# =============================================================================

def formule_bresse(q_m3s: float) -> float:
    """Formule de Bresse: D_théo = 1.5 × √Q (Q en m³/s)"""
    return 1.5 * math.sqrt(q_m3s)

def formule_bresse_modifiee(q_m3s: float) -> float:
    """Formule de Bresse modifiée: D_théo = 0.83 × ∛Q (Q en m³/s)"""
    return 0.83 * (q_m3s ** (1/3))

def formule_munier(q_m3s: float, n_heures: int = 16) -> float:
    """Formule de Munier: D_théo = (1 + 0.02n) × √Q (Q en m³/s)"""
    return (1 + 0.02 * n_heures) * math.sqrt(q_m3s)

def formule_bedjaou(q_m3s: float) -> float:
    """Formule Bedjaou: D_théo = 1.27 × √Q (Q en m³/s)"""
    return 1.27 * math.sqrt(q_m3s)

# =============================================================================
# MESSAGES D'AIDE ET DOCUMENTATION
# =============================================================================

HELP_MESSAGES = {
    "population": """
    Calcul de projection démographique selon la méthode de Malthus.
    
    Formule: Pn = Po × (1 + a)^n
    
    Où:
    - Pn: Population après n années
    - Po: Population de référence
    - a: Taux d'accroissement annuel
    - n: Nombre d'années
    
    CLI Usage:
        lcpi aep population --base <pop> --rate <taux> --years <années>
        
    REPL Usage:
        >>> from lcpi.aep.calculations import population
        >>> result = population.calculate_projection(9967, 0.037, 20)
    """,
    
    "demand": """
    Calcul des besoins en eau potable.
    
    Formules:
    - Besoin domestique: B_dom = Population × Dotation
    - Besoin annexe: B_a = 10% × B_dom
    - Besoin global: B_gbl = B_dom + B_a
    - Besoin pointe: B_npjp = B_gbl × Cpj
    - Besoin brut: B_bpjp = B_npjp / r_technique
    
    CLI Usage:
        lcpi aep demand --population <pop> --dotation <l/j/hab> --coeff-pointe <k>
        
    REPL Usage:
        >>> from lcpi.aep.calculations import demand
        >>> result = demand.calculate_water_demand(20847, 60, 1.5)
    """,
    
    "network": """
    Dimensionnement hydraulique du réseau de distribution.
    
    Formules:
    - Pertes de charge: ΔPt = (L×10.29359×Q²)/(Ks²×D^(16/3)) × (1+0.05)
    - HMT = H_géo + ΔH_asp+ref
    - Vitesse: V = Q/S
    
    CLI Usage:
        lcpi aep network --debit <m³/h> --longueur <m> --material <PVC>
        
    REPL Usage:
        >>> from lcpi.aep.calculations import network
        >>> result = network.dimension_network(215, 5000, "PVC")
    """,
    
    "reservoir": """
    Dimensionnement des réservoirs de stockage.
    
    Formules:
    - Volume utile: Vu = c × B_bpjp
    - Volume incendie: Vi = 120 m³
    - Volume mort: Vm = 0.02 × Vu
    - Volume sécurité: Vr = (B_bpjp/24) × n
    
    CLI Usage:
        lcpi aep reservoir --volume-journalier <m³> --type <adduction>
        
    REPL Usage:
        >>> from lcpi.aep.calculations import reservoir
        >>> result = reservoir.dimension_reservoir(2064, "continue")
    """,
    
    "pumping": """
    Dimensionnement des équipements de pompage.
    
    Formules:
    - Puissance hydraulique: Ph = ρ×g×Q×HMT
    - Puissance électrique: P_élec = Ph/(ηm×ηp)
    - Puissance groupe: P_maxge = 2×(2.725×10^-3×Q×HMT)/(ηm×ηp×cosφ)
    
    CLI Usage:
        lcpi aep pumping --debit <m³/h> --hmt <m> --rendement <%>
        
    REPL Usage:
        >>> from lcpi.aep.calculations import pumping
        >>> result = pumping.dimension_pumping(86, 45.3, 75)
    """,
    
    "protection": """
    Calcul de protection contre les coups de bélier.
    
    Formules:
    - Célérité: C = 9900/√(48.3 + kD/e)
    - Variation pression: ΔP = C × V₀/g
    - Surpression max: H_max = HMT + ΔP - ND_max
    - Dépression min: H_min = HMT - ΔP - ND_max
    
    CLI Usage:
        lcpi aep protection --diametre <mm> --vitesse <m/s> --epaisseur <mm>
        
    REPL Usage:
        >>> from lcpi.aep.calculations import protection
        >>> result = protection.calculate_water_hammer_protection(200, 1.2, 6)
    """
} 