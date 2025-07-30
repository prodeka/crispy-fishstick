import math

G = 9.81 # Accélération de la pesanteur

def dimensionner_deversoir(donnees: dict) -> dict:
    """
    Détermine la longueur de crête (L) d'un déversoir de surface.
    """
    # --- PHASE 1 : Extraction des données d'entrée ---
    q_projet = donnees.get("debit_projet_m3s")
    cote_crete_barrage = donnees.get("cote_crete_barrage_m")
    revanche = donnees.get("revanche_m")
    cote_crete_deversoir = donnees.get("cote_crete_deversoir_m")
    profil_crete = donnees.get("profil_crete", "creager")

    if not all([q_projet, cote_crete_barrage, revanche, cote_crete_deversoir]):
        return {"statut": "Erreur", "message": "Données d'entrée manquantes."}

    phe_max = cote_crete_barrage - revanche
    
    # --- PHASE 2 : Dimensionnement Hydraulique ---
    # 2.2 : Choix du coefficient de débit (m)
    coeffs_debit = {"creager": 0.49, "seuil_epais": 0.35, "paroi_mince": 0.40}
    m = coeffs_debit.get(profil_crete.lower(), 0.49)

    # 2.3.1 : Détermination de la charge hydraulique disponible (h)
    h = phe_max - cote_crete_deversoir
    if h <= 0:
        return {"statut": "Erreur", "message": "La cote de la crête du déversoir doit être inférieure à la PHE maximale."}

    # 2.3.2 : Calcul de la longueur de crête (L)
    denominateur = m * math.sqrt(2 * G) * (h**1.5)
    if denominateur == 0:
        return {"statut": "Erreur", "message": "Calcul impossible (dénominateur nul)."}
        
    longueur_crete = q_projet / denominateur
    
    # NOTE: L'itération avec la vitesse d'approche n'est pas implémentée dans cette version.
    
    # --- PHASE 4 : SYNTHÈSE ---
    return {
        "statut": "OK",
        "type_deversoir": profil_crete,
        "debit_projet_m3s": q_projet,
        "cote_crete_deversoir_m_ngf": round(cote_crete_deversoir, 2),
        "longueur_crete_calculee_m": round(longueur_crete, 2),
        "charge_hydraulique_projet_m": round(h, 2)
    }
