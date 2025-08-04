import json
import math
import os

class CalculAdduction:
    """
    Classe pour les calculs hydrauliques du chapitre 4.
    - Calcul des pertes de charge (linéaires et singulières)
    - Implémentation des formules de Darcy-Weisbach, Manning-Strickler et Hazen-Williams.
    """
    def __init__(self, fichier_donnees="donnees_adduction.json"):
        if not os.path.exists(fichier_donnees):
            raise FileNotFoundError(f"Erreur : Le fichier de données '{fichier_donnees}' est introuvable.")
        with open(fichier_donnees, 'r', encoding='utf-8') as f:
            self.donnees = json.load(f)
        self.g = self.donnees['parametres_physiques']['g_acceleration_gravite_ms2']
        self.nu = self.donnees['parametres_physiques']['viscosite_cinematique_eau_m2_s']['valeur']
        print("✅ Fichier de données d'adduction chargé avec succès.")

    # --- Fonctions de recherche dans la base de données ---
    def _get_rugosite_absolue_e(self, materiau):
        for item in self.donnees['coefficients_rugosite']['rugosite_absolue_e_mm']:
            if item['materiau'].lower() == materiau.lower():
                return item['valeur_mm'] / 1000.0 # Conversion en mètres
        raise ValueError(f"Matériau '{materiau}' non trouvé dans la base de données de rugosité.")

    def _get_manning_n(self, materiau, etat):
        for item in self.donnees['coefficients_rugosite']['manning_n']:
            if materiau.lower() in item['nature_parois'].lower():
                return item[etat.lower()]
        raise ValueError(f"Combinaison matériau/état '{materiau}/{etat}' non trouvée pour Manning.")

    def _get_hazen_williams_C(self, materiau, etat):
        for item in self.donnees['coefficients_rugosite']['hazen_williams_C']:
            if item['materiau'].lower() == materiau.lower() and item['etat'].lower() == etat.lower():
                return item['valeur']
        raise ValueError(f"Combinaison matériau/état '{materiau}/{etat}' non trouvée pour Hazen-Williams.")
    
    def _get_singular_K(self, element):
        for item in self.donnees['coefficients_pertes_singulieres_K']:
            if item['element'].lower() == element.lower():
                return item['valeur_K']
        raise ValueError(f"Élément singulier '{element}' non trouvé.")

    # --- Fonctions de calcul de base ---
    def calculer_vitesse(self, debit_m3s, diametre_m):
        aire = math.pi * (diametre_m / 2)**2
        return debit_m3s / aire

    def calculer_reynolds(self, debit_m3s, diametre_m):
        vitesse = self.calculer_vitesse(debit_m3s, diametre_m)
        return (vitesse * diametre_m) / self.nu

    # --- Résolution de Colebrook (la plus complexe) ---
    def calculer_colebrook_lambda(self, reynolds, diametre_m, materiau):
        """
        Résout l'équation implicite de Colebrook-White pour trouver le facteur de friction λ.
        Utilise une méthode itérative simple.
        """
        if reynolds < 2300: # Régime laminaire
            return 64 / reynolds
            
        e = self._get_rugosite_absolue_e(materiau)
        eD = e / diametre_m
        
        # Estimation initiale de λ avec la formule de Haaland
        lambda_i = (1 / (-1.8 * math.log10((eD / 3.7)**1.11 + 6.9 / reynolds)))**2
        
        # Itérations pour affiner la valeur
        for _ in range(10): # 10 itérations suffisent généralement pour la convergence
            terme1 = eD / 3.7
            terme2 = 2.51 / (reynolds * math.sqrt(lambda_i))
            lambda_new = (1 / (-2 * math.log10(terme1 + terme2)))**2
            if abs(lambda_new - lambda_i) < 1e-6:
                return lambda_new
            lambda_i = lambda_new
        return lambda_i

    # --- Fonctions principales de perte de charge linéaire ---
    def perte_de_charge_darcy_weisbach(self, debit_m3s, diametre_m, longueur_m, materiau):
        re = self.calculer_reynolds(debit_m3s, diametre_m)
        lambda_f = self.calculer_colebrook_lambda(re, diametre_m, materiau)
        vitesse = self.calculer_vitesse(debit_m3s, diametre_m)
        
        delta_h = lambda_f * (longueur_m / diametre_m) * (vitesse**2 / (2 * self.g))
        return delta_h

    def perte_de_charge_manning_strickler(self, debit_m3s, diametre_m, longueur_m, materiau, etat='bon'):
        n = self._get_manning_n(materiau, etat)
        ks = 1 / n # Coeff de Strickler
        vitesse = self.calculer_vitesse(debit_m3s, diametre_m)
        rh = diametre_m / 4 # Rayon hydraulique pour conduite circulaire pleine
        
        # Formule réarrangée pour trouver la perte de charge
        # V = ks * Rh^(2/3) * j^(1/2) => j = (V / (ks * Rh^(2/3)))^2
        # j = ΔH/L
        j = (vitesse / (ks * rh**(2/3)))**2
        delta_h = j * longueur_m
        return delta_h

    def perte_de_charge_hazen_williams(self, debit_m3s, diametre_m, longueur_m, materiau, etat='neuve'):
        C = self._get_hazen_williams_C(materiau, etat)
        
        # Formule de débit réarrangée pour ΔH/L (en SI)
        # Q = 0.2785 * C * D^2.63 * j^0.54 => j = (Q / (0.2785 * C * D^2.63))^(1/0.54)
        j = (debit_m3s / (0.2785 * C * diametre_m**2.63))**(1/0.54)
        delta_h = j * longueur_m
        return delta_h
        
    # --- Fonction pour les pertes singulières ---
    def perte_de_charge_singuliere(self, debit_m3s, diametre_m, nom_element):
        K = self._get_singular_K(nom_element)
        vitesse = self.calculer_vitesse(debit_m3s, diametre_m)
        delta_h = K * (vitesse**2) / (2 * self.g)
        return delta_h

    # --- Fonction de synthèse pour un tronçon complet ---
    def calcul_perte_charge_totale_troncon(self, debit_m3s, diametre_m, longueur_m, materiau_conduite, elements_singuliers, methode_lineaire='darcy'):
        """
        Calcule la perte de charge totale sur un tronçon de conduite.
        
        Args:
            elements_singuliers (list): Une liste de noms d'éléments (ex: ["Coude 90° standard", "Vanne à opercule ouverte"])
            methode_lineaire (str): 'darcy', 'manning', ou 'hazen'
        """
        # Calcul de la perte de charge linéaire
        if methode_lineaire == 'darcy':
            pdc_lineaire = self.perte_de_charge_darcy_weisbach(debit_m3s, diametre_m, longueur_m, materiau_conduite)
        elif methode_lineaire == 'manning':
            pdc_lineaire = self.perte_de_charge_manning_strickler(debit_m3s, diametre_m, longueur_m, materiau_conduite)
        elif methode_lineaire == 'hazen':
            pdc_lineaire = self.perte_de_charge_hazen_williams(debit_m3s, diametre_m, longueur_m, materiau_conduite)
        else:
            raise ValueError("Méthode linéaire non reconnue.")
            
        # Calcul des pertes de charge singulières
        pdc_singuliere_totale = 0
        for element in elements_singuliers:
            pdc_singuliere_totale += self.perte_de_charge_singuliere(debit_m3s, diametre_m, element)
            
        pdc_totale = pdc_lineaire + pdc_singuliere_totale
        
        return {
            "Perte de charge linéaire": pdc_lineaire,
            "Perte de charge singulière totale": pdc_singuliere_totale,
            "Perte de charge TOTALE (m)": pdc_totale
        }


# --- Programme Principal d'Exemple ---
if __name__ == "__main__":
    calculateur = CalculAdduction()
    
    # --- Données du projet de calcul ---
    DEBIT = 0.25  # m³/s
    DIAMETRE = 0.5 # m (500 mm)
    LONGUEUR = 1200 # m
    MATERIAU = "Fonte usagée"
    ETAT = "20 ans" # Pour Hazen-Williams
    ETAT_MANNING = "mauvais" # Pour Manning
    
    print("\n" + "="*60)
    print("EXEMPLE 1 : COMPARAISON DES PERTES DE CHARGE LINÉAIRES")
    print("="*60)
    print(f"Paramètres : Q={DEBIT} m³/s, D={DIAMETRE} m, L={LONGUEUR} m, Matériau={MATERIAU}")
    
    pdc_d = calculateur.perte_de_charge_darcy_weisbach(DEBIT, DIAMETRE, LONGUEUR, MATERIAU)
    pdc_m = calculateur.perte_de_charge_manning_strickler(DEBIT, DIAMETRE, LONGUEUR, 'Fonte', ETAT_MANNING)
    pdc_h = calculateur.perte_de_charge_hazen_williams(DEBIT, DIAMETRE, LONGUEUR, 'Fonte', ETAT)
    
    print(f"- Darcy-Weisbach (Colebrook) : {pdc_d:.3f} m")
    print(f"- Manning-Strickler          : {pdc_m:.3f} m")
    print(f"- Hazen-Williams             : {pdc_h:.3f} m")
    
    print("\n" + "="*60)
    print("EXEMPLE 2 : CALCUL COMPLET D'UN TRONÇON")
    print("="*60)
    elements = [
        "Entrée de conduite (bord franc)",
        "Coude 90° standard",
        "Coude 90° standard",
        "Vanne à opercule ouverte",
        "Sortie de conduite"
    ]
    print(f"Le tronçon de {LONGUEUR}m contient les éléments suivants : {', '.join(elements)}")

    resultats_complets = calculateur.calcul_perte_charge_totale_troncon(
        debit_m3s=DEBIT,
        diametre_m=DIAMETRE,
        longueur_m=LONGUEUR,
        materiau_conduite=MATERIAU,
        elements_singuliers=elements,
        methode_lineaire='darcy'
    )
    
    for cle, val in resultats_complets.items():
        print(f"- {cle:<30}: {val:.3f} m")
        