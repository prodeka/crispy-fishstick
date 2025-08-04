import json
import os

class CalculEntretien:
    """
    Classe pour les calculs du chapitre 6 : Entretien et Maintenance.
    - Calcul des indicateurs de performance du réseau (rendement, indices linéaires).
    """
    def __init__(self, fichier_donnees="donnees_entretien.json"):
        if not os.path.exists(fichier_donnees):
            raise FileNotFoundError(f"Erreur : Le fichier de données '{fichier_donnees}' est introuvable.")
        with open(fichier_donnees, 'r', encoding='utf-8') as f:
            self.donnees = json.load(f)
        print("✅ Fichier de données d'entretien chargé avec succès.")

    def calculer_rendement_primaire(self, volume_comptabilise, volume_mis_en_distribution):
        """Calcule le rendement primaire du réseau en pourcentage."""
        if volume_mis_en_distribution == 0:
            return 0
        rendement = (volume_comptabilise / volume_mis_en_distribution) * 100
        
        # Analyse par rapport aux seuils
        seuil_bon = self.donnees['seuils_performance_reseau']['rendement_primaire']['objectif_bon_pourcent']
        seuil_excellent = self.donnees['seuils_performance_reseau']['rendement_primaire']['objectif_excellent_pourcent']
        if rendement >= seuil_excellent:
            performance = "Excellent"
        elif rendement >= seuil_bon:
            performance = "Bon"
        else:
            performance = "Faible (à améliorer)"
            
        return rendement, performance

    def calculer_indice_lineaire_pertes(self, volume_mis_en_distribution, volume_comptabilise, longueur_reseau_km):
        """Calcule l'Indice Linéaire de Pertes (ILP) en m³/jour/km."""
        if longueur_reseau_km == 0:
            return 0
        volume_pertes = volume_mis_en_distribution - volume_comptabilise
        # On suppose que les volumes sont annuels, donc on divise par 365
        ilp = (volume_pertes / 365) / longueur_reseau_km
        return ilp

    def calculer_indice_lineaire_reparations(self, nombre_reparations_annuelles, longueur_reseau_km):
        """Calcule l'Indice Linéaire de Réparations (ILR) en réparations/an/km."""
        if longueur_reseau_km == 0:
            return 0
        return nombre_reparations_annuelles / longueur_reseau_km
        
    def calculer_indice_lineaire_consommation_net(self, volume_comptabilise, volume_service, longueur_reseau_km):
        """Calcule l'Indice Linéaire de Consommation Net (ILCN) en m³/j/km."""
        if longueur_reseau_km == 0:
            return 0
        # Volume total utilisé = comptabilisé + service (non facturé mais autorisé)
        # Supposant des volumes annuels, on divise par 365
        ilcn = ((volume_comptabilise + volume_service) / 365) / longueur_reseau_km
        return ilcn

# --- Programme Principal d'Exemple ---
if __name__ == "__main__":
    calc = CalculEntretien()

    # --- Données d'un réseau de taille moyenne pour l'exemple ---
    VOL_PRODUIT_AN_M3 = 3_500_000  # Volume mis en distribution
    VOL_COMPTABILISE_AN_M3 = 2_800_000 # Volume facturé aux abonnés
    VOL_SERVICE_AN_M3 = 150_000 # Volume pour nettoyage, services municipaux...
    LONGUEUR_RESEAU_KM = 250
    NOMBRE_REPARATIONS_AN = 150

    print("\n" + "="*50)
    print("EXEMPLE : CALCUL DES INDICATEURS DE PERFORMANCE D'UN RÉSEAU")
    print("="*50)
    print(f"Données du réseau :")
    print(f" - Volume produit/an : {VOL_PRODUIT_AN_M3:,.0f} m³")
    print(f" - Volume comptabilisé/an : {VOL_COMPTABILISE_AN_M3:,.0f} m³")
    print(f" - Volume de service/an : {VOL_SERVICE_AN_M3:,.0f} m³")
    print(f" - Longueur du réseau : {LONGUEUR_RESEAU_KM} km")
    print(f" - Nombre de réparations/an : {NOMBRE_REPARATIONS_AN}")
    print("="*50 + "\n")

    # Calculs
    rendement, perf_rendement = calc.calculer_rendement_primaire(VOL_COMPTABILISE_AN_M3, VOL_PRODUIT_AN_M3)
    ilp = calc.calculer_indice_lineaire_pertes(VOL_PRODUIT_AN_M3, VOL_COMPTABILISE_AN_M3, LONGUEUR_RESEAU_KM)
    ilr = calc.calculer_indice_lineaire_reparations(NOMBRE_REPARATIONS_AN, LONGUEUR_RESEAU_KM)
    ilcn = calc.calculer_indice_lineaire_consommation_net(VOL_COMPTABILISE_AN_M3, VOL_SERVICE_AN_M3, LONGUEUR_RESEAU_KM)

    print(f"1. Rendement primaire du réseau : {rendement:.2f}% (Performance : {perf_rendement})")
    print(f"2. Indice Linéaire de Pertes (ILP) : {ilp:.2f} m³/jour/km")
    print(f"3. Indice Linéaire de Réparations (ILR) : {ilr:.2f} réparations/an/km")
    print(f"4. Indice Linéaire de Consommation Net (ILCN) : {ilcn:.2f} m³/jour/km")
    print("="*50)