import math

G = 9.81 # Accélération de la pesanteur

def verifier_dalot(donnees: dict) -> dict:
    """
    Effectue la vérification hydraulique complète d'un dalot ou d'une buse.
    """
    # --- PHASE 1 : Extraction des données d'entrée ---
    q_projet = donnees.get("debit_projet_m3s")
    largeur = donnees.get("largeur_m")
    hauteur = donnees.get("hauteur_m")
    nb_cellules = donnees.get("nombre_cellules", 1)
    longueur_ouvrage = donnees.get("longueur_m")
    n_manning = donnees.get("manning")
    
    if not all([q_projet, largeur, hauteur, longueur_ouvrage, n_manning]):
        return {"statut": "Erreur", "message": "Données d'entrée manquantes."}

    q_cellule = q_projet / nb_cellules
    aire_section = largeur * hauteur

    # --- PHASE 2.2 : Contrôle par l'Amont (Inlet Control) ---
    # Condition dénoyée
    h_amont_denoyee = (q_cellule / (0.53 * largeur))**(2/3)
    # Condition noyée
    h_amont_noyee_part = (q_cellule / (0.6 * aire_section))**2 / (2 * G)
    h_amont_noyee = h_amont_noyee_part + hauteur / 2
    h_controle_amont = max(h_amont_denoyee, h_amont_noyee)

    # --- PHASE 2.3 : Contrôle par l'Aval (Outlet Control) ---
    vitesse = q_cellule / aire_section
    perimetre_mouille = 2 * (largeur + hauteur)
    rayon_hydraulique = aire_section / perimetre_mouille

    # Pertes de charge
    h_entree = 0.5 * (vitesse**2 / (2 * G)) # Ke = 0.5
    h_friction = ((n_manning**2 * longueur_ouvrage) / (rayon_hydraulique**(4/3))) * vitesse**2
    h_sortie = 1.0 * (vitesse**2 / (2 * G)) # Ko = 1.0
    h_pertes_totales = h_entree + h_friction + h_sortie
    
    # Hauteur aval (simplification : on suppose une hauteur critique)
    h_critique = (q_cellule**2 / (G * largeur**2))**(1/3)
    h_aval_effective = max(h_critique, 0) # On suppose h_aval_reelle = 0 pour le pire cas
    h_controle_aval = h_pertes_totales + h_aval_effective

    # --- PHASE 2.4 : Détermination de la hauteur de projet ---
    h_projet_amont = max(h_controle_amont, h_controle_aval)
    
    # --- PHASE 3 : Vérifications finales ---
    vitesse_sortie = vitesse # Simplification, vitesse = constante

    return {
        "statut": "OK",
        "dimensions_testees": f"{nb_cellules}x({largeur}m x {hauteur}m)",
        "debit_par_cellule_m3s": round(q_cellule, 2),
        "hauteur_projet_amont_m": round(h_projet_amont, 2),
        "regime_determinant": "Contrôle Amont" if h_controle_amont > h_controle_aval else "Contrôle Aval",
        "vitesse_sortie_ms": round(vitesse_sortie, 2)
    }