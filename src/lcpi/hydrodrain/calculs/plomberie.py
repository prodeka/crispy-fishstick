import math

def dimensionner_troncon_plomberie(donnees: dict) -> dict:
    # Phase 2 : Débit probable
    nb_appareils = donnees.get("nombre_appareils")
    somme_debits_base = donnees.get("somme_debits_base_ls")
    
    coeff_k = 1 / math.sqrt(nb_appareils - 1) if nb_appareils > 1 else 1
    q_probable_ls = coeff_k * somme_debits_base
    q_probable_m3s = q_probable_ls / 1000
    
    # Phase 3 : Diamètre
    v_max = 2.0 # m/s
    d_theorique_m = math.sqrt((4 * q_probable_m3s) / (math.pi * v_max))
    
    # Choix du diamètre normalisé (simplifié)
    diametres_commerciaux_m = [0.010, 0.012, 0.016, 0.020, 0.025] # DN
    d_normalise = next((d for d in diametres_commerciaux_m if d >= d_theorique_m), diametres_commerciaux_m[-1])
    v_reelle = (4 * q_probable_m3s) / (math.pi * d_normalise**2)
    
    return {
        "statut": "OK",
        "debit_probable_ls": round(q_probable_ls, 3),
        "diametre_theorique_mm": round(d_theorique_m * 1000, 1),
        "diametre_normalise_choisi_mm": d_normalise * 1000,
        "vitesse_reelle_ms": round(v_reelle, 2)
    }
