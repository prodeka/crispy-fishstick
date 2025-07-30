
import math

# --- PHASE 3.1 : MANNING-STRICKLER ---
def calculer_phe_manning_strickler(profil: dict, debit_projet: float, pente: float, k_strickler: float = 30) -> float:
    """
    Détermine la hauteur d'eau (PHE) par itérations avec la formule de Manning-Strickler.
    Le profil est un dictionnaire décrivant une section (ex: trapézoïdale).
    """
    b_lit_mineur = profil.get("largeur_lit_mineur_m", 10)
    m_pente_berges = profil.get("pente_berges_m_m", 2) # Pente de 2:1 (H:V)

    # Fonction interne pour calculer le débit pour une hauteur h donnée
    def _debit_pour_h(h):
        s_mouillee = h * (b_lit_mineur + m_pente_berges * h)
        p_mouille = b_lit_mineur + 2 * h * math.sqrt(1 + m_pente_berges**2)
        if p_mouille == 0: return 0
        r_hydraulique = s_mouillee / p_mouille
        q_calcule = k_strickler * s_mouillee * (r_hydraulique**(2/3)) * (pente**0.5)
        return q_calcule

    # Recherche itérative de la hauteur h
    h_test = 0.01
    q_test = 0
    increment = 0.01 # Précision de 1 cm

    while q_test < debit_projet:
        h_test += increment
        q_test = _debit_pour_h(h_test)
        if h_test > 50: # Sécurité pour éviter les boucles infinies
            return -1 # Code d'erreur

    return h_test

# --- PHASE 3.2 : REMOUS ---
def calculer_remous(vitesse_amont: float, geometrie_pont: dict) -> float:
    """
    Calcule la hauteur de remous.
    (Placeholder avec une formule simplifiée)
    """
    # Formule très simplifiée pour le placeholder
    remous = 0.1 * (vitesse_amont**2 / (2 * 9.81))
    return remous

# --- PHASE 4 : AFFOUILLEMENT ---
def calculer_affouillement(debit_centennal: float, largeur_lit: float, largeur_pile: float) -> dict:
    """
    Estime l'affouillement général (Lacy) et local (Breusers).
    """
    # Affouillement Général (Lacy) - Formule simplifiée
    h_g = 0.47 * (debit_centennal / 1)**(1/3) # 1 = facteur de forme (simplifié)
    
    # Affouillement Local (Breusers)
    h_l = 1.4 * largeur_pile
    
    h_total = h_g + h_l
    
    return {"general": h_g, "local": h_l, "total": h_total}

    
