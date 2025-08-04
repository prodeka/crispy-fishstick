import json
import os

def charger_donnees(fichier_json="donnees_reservoirs.json"):
    """
    Charge les données métier depuis un fichier JSON.
    Retourne un dictionnaire Python.
    """
    if not os.path.exists(fichier_json):
        raise FileNotFoundError(f"Erreur : Le fichier de données '{fichier_json}' est introuvable.")
    with open(fichier_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculer_debit_moyen(volume_journalier_m3):
    """
    Calcule le débit moyen horaire 'a'.

    Args:
        volume_journalier_m3 (float): La consommation totale sur 24 heures.

    Returns:
        float: Le débit moyen horaire 'a' en m³/h.
    """
    return volume_journalier_m3 / 24.0

def calculer_volume_utile(volume_journalier_m3, profil, mode_adduction='24h'):
    """
    Calcule le volume utile du réservoir par la méthode du bilan hydraulique.

    Args:
        volume_journalier_m3 (float): Consommation totale sur 24h.
        profil (dict): Le dictionnaire du profil de consommation à utiliser.
        mode_adduction (str): '24h' pour adduction continue, '10h_nuit' pour adduction de 20h à 6h.

    Returns:
        tuple: (volume_utile_m3, liste_bilan_horaire)
    """
    debit_moyen_a = calculer_debit_moyen(volume_journalier_m3)
    repartition = profil['repartition']
    
    bilan = [0.0] * 25  # Pour stocker le volume accumulé à chaque heure (de h=0 à h=24)
    
    # Créer une liste de coefficients pour chaque heure
    coeffs_horaires = [0.0] * 24
    for tranche in repartition:
        for heure in range(tranche['debut'], tranche['fin']):
            coeffs_horaires[heure] = tranche['coefficient']

    for heure in range(24):
        # Calcul du volume entrant pour l'heure en cours
        if mode_adduction == '24h':
            volume_entrant_heure = debit_moyen_a
        elif mode_adduction == '10h_nuit':
            # Adduction pendant 10h (de 20h à 6h du matin)
            debit_adduction_nuit = volume_journalier_m3 / 10.0
            if heure >= 20 or heure < 6:
                volume_entrant_heure = debit_adduction_nuit
            else:
                volume_entrant_heure = 0.0
        else:
            raise ValueError("Mode d'adduction non supporté. Choisissez '24h' ou '10h_nuit'.")

        # Calcul du volume sortant
        volume_sortant_heure = coeffs_horaires[heure] * debit_moyen_a
        
        # Variation du volume dans le réservoir
        variation = volume_entrant_heure - volume_sortant_heure
        
        # Bilan à la fin de l'heure
        bilan[heure + 1] = bilan[heure] + variation

    volume_utile = max(bilan) - min(bilan)
    return volume_utile, bilan

def calculer_capacite_pratique(volume_utile_m3, volume_journalier_m3, surface_radier_m2, params_calcul):
    """
    Calcule la capacité pratique (totale) du réservoir.

    Args:
        volume_utile_m3 (float): Volume utile calculé.
        volume_journalier_m3 (float): Consommation totale sur 24h.
        surface_radier_m2 (float): Surface au sol du réservoir.
        params_calcul (dict): Dictionnaire des paramètres de calcul (volume mort, réserve incendie).

    Returns:
        dict: Un dictionnaire contenant les détails des volumes.
    """
    # Calcul du volume de réserve incendie
    debit_moyen_a = calculer_debit_moyen(volume_journalier_m3)
    facteur_incendie = params_calcul['facteur_reserve_incendie_par_debit_moyen']
    volume_incendie = facteur_incendie * debit_moyen_a
    
    # Calcul du volume mort
    hauteur_mort = params_calcul['hauteur_volume_mort_m']
    volume_mort = hauteur_mort * surface_radier_m2
    
    # Capacité totale
    capacite_totale = volume_utile_m3 + volume_incendie + volume_mort
    
    return {
        "Volume Utile (Vu)": volume_utile_m3,
        "Volume de Réserve Incendie": volume_incendie,
        "Volume Mort": volume_mort,
        "Capacité Totale du Réservoir": capacite_totale
    }

# --- Programme Principal ---
if __name__ == "__main__":
    try:
        # 1. Charger les données métier
        donnees = charger_donnees()
        print("✅ Fichier de données 'donnees_reservoirs.json' chargé avec succès.")
        
        # 2. Définir les paramètres du projet
        VOLUME_JOURNALIER_PROJET = 5000  # en m³
        SURFACE_RADIER_PROJET = 250     # en m²
        PROFIL_CHOISI = "ville_francaise_peu_importante"
        
        print("\n" + "="*50)
        print("SIMULATION DE DIMENSIONNEMENT D'UN RÉSERVOIR")
        print("="*50)
        print(f"Volume journalier de consommation : {VOLUME_JOURNALIER_PROJET} m³")
        print(f"Surface du radier du réservoir : {SURFACE_RADIER_PROJET} m²")
        print(f"Profil de consommation utilisé : '{PROFIL_CHOISI}'")
        print(f"Description du profil : {donnees['profils_consommation'][PROFIL_CHOISI]['description']}")
        print("="*50 + "\n")

        # 3. Exécuter les calculs pour une adduction continue sur 24h
        print("--- SCÉNARIO 1 : Adduction continue sur 24 heures ---")
        profil = donnees['profils_consommation'][PROFIL_CHOISI]
        vu_24h, bilan_24h = calculer_volume_utile(VOLUME_JOURNALIER_PROJET, profil, mode_adduction='24h')
        
        resultats_24h = calculer_capacite_pratique(
            vu_24h, 
            VOLUME_JOURNALIER_PROJET, 
            SURFACE_RADIER_PROJET,
            donnees['parametres_calcul']
        )
        
        for cle, valeur in resultats_24h.items():
            print(f"- {cle:<35}: {valeur:.2f} m³")
        
        # Le volume utile correspond à 10a (10 * (5000/24)), ce qui correspond au document.
        print(f"  (Note: Le volume utile correspond à {vu_24h / (VOLUME_JOURNALIER_PROJET/24):.2f} fois le débit moyen horaire 'a')")

        print("\n" + "-"*50 + "\n")
        
        # 4. Exécuter les calculs pour une adduction intermittente (10h la nuit)
        print("--- SCÉNARIO 2 : Adduction intermittente sur 10 heures (nuit) ---")
        vu_10h, bilan_10h = calculer_volume_utile(VOLUME_JOURNALIER_PROJET, profil, mode_adduction='10h_nuit')
        
        resultats_10h = calculer_capacite_pratique(
            vu_10h, 
            VOLUME_JOURNALIER_PROJET, 
            SURFACE_RADIER_PROJET,
            donnees['parametres_calcul']
        )
        
        for cle, valeur in resultats_10h.items():
            print(f"- {cle:<35}: {valeur:.2f} m³")
        # Le volume utile correspond à 22a (22 * (5000/24)), ce qui correspond au document.
        print(f"  (Note: Le volume utile correspond à {vu_10h / (VOLUME_JOURNALIER_PROJET/24):.2f} fois le débit moyen horaire 'a')")
        print("="*50 + "\n")

    except Exception as e:
        print(f"Une erreur est survenue : {e}")