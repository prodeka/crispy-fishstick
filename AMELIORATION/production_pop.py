import json
import math
import os

class CalculProductionEau:
    """
    Classe regroupant les calculs du chapitre 2 :
    - Estimation des besoins en eau
    - Prévision de la population
    - Calcul de débit de puits
    """
    def __init__(self, fichier_donnees="donnees_production.json"):
        """Initialise la classe en chargeant les données depuis le fichier JSON."""
        if not os.path.exists(fichier_donnees):
            raise FileNotFoundError(f"Erreur : Le fichier de données '{fichier_donnees}' est introuvable.")
        with open(fichier_donnees, 'r', encoding='utf-8') as f:
            self.donnees = json.load(f)
        print("✅ Fichier de données de production chargé avec succès.")

    # --- PARTIE 1: PRÉVISION DE LA POPULATION ---

    def prevision_population_arithmetique(self, y1, t1, y2, t2, t_futur):
        """
        Prévision de population par progression arithmétique (croissance linéaire).

        Args:
            y1 (int): Population au recensement 1.
            t1 (int): Année du recensement 1.
            y2 (int): Population au recensement 2.
            t2 (int): Année du recensement 2.
            t_futur (int): Année cible pour la prévision.

        Returns:
            float: Population estimée pour l'année future.
        """
        ku = (y2 - y1) / (t2 - t1)  # Taux d'accroissement uniforme
        population_future = y2 + ku * (t_futur - t2)
        return population_future

    def prevision_population_geometrique(self, y1, t1, y2, t2, t_futur):
        """
        Prévision de population par progression géométrique (taux constant en pourcentage).

        Args:
            y1 (int): Population au recensement 1.
            t1 (int): Année du recensement 1.
            y2 (int): Population au recensement 2.
            t2 (int): Année du recensement 2.
            t_futur (int): Année cible pour la prévision.

        Returns:
            float: Population estimée pour l'année future.
        """
        if y1 <= 0 or y2 <= 0:
            raise ValueError("Les populations doivent être positives pour une projection géométrique.")
        kp = (math.log(y2) - math.log(y1)) / (t2 - t1) # Taux d'accroissement
        log_pop_future = math.log(y2) + kp * (t_futur - t2)
        return math.exp(log_pop_future)

    def prevision_population_logistique(self, y0, y1, y2, n, x):
        """
        Prévision de population par méthode logistique (courbe en S).

        Args:
            y0 (int): Population au 1er point (temps 0).
            y1 (int): Population au 2ème point (temps n).
            y2 (int): Population au 3ème point (temps 2n).
            n (int): Intervalle de temps entre les points (ex: 10 pour 10 ans).
            x (int): Intervalle de temps entre le point y0 et l'année cible.

        Returns:
            float: Population estimée.
        """
        # Calcul des constantes K, a, b
        denom_k = y0 * y2 - y1**2
        if denom_k == 0:
            raise ValueError("Division par zéro dans le calcul de K. Les points sont probablement colinéaires.")
        K = (2 * y0 * y1 * y2 - y1**2 * (y0 + y2)) / denom_k
        
        if K <= y0 or K <= y1 or K <= y2:
            raise ValueError("La population de saturation K est inférieure aux données. La méthode logistique n'est pas applicable.")

        a = math.log10((K - y0) / y0)
        
        denom_b = y1 * (K - y0)
        if denom_b == 0:
             raise ValueError("Division par zéro dans le calcul de b.")
        b = (1 / n) * math.log10((y0 * (K - y1)) / denom_b)

        # Calcul de la population future Yc
        Yc = K / (1 + 10**(a + b * x))
        return Yc
        
    # --- PARTIE 2: CALCUL DE DÉBIT DE PUITS ---

    def calcul_debit_puits_nappe_libre(self, K, H, h, R, r):
        """
        Calcule le débit d'un puits en nappe libre (Formule de Thiem).

        Args:
            K (float): Coeff. de perméabilité (m/s).
            H (float): Hauteur initiale de la nappe (m).
            h (float): Hauteur de l'eau dans le puits en pompage (m).
            R (float): Rayon d'influence du pompage (m).
            r (float): Rayon du puits (m).

        Returns:
            float: Débit Q en m³/s.
        """
        if R <= r or r <= 0:
            raise ValueError("Le rayon d'influence R doit être supérieur au rayon du puits r.")
        Q = (K * math.pi * (H**2 - h**2)) / math.log(R / r)
        return Q

    def calcul_debit_puits_nappe_captive(self, K, e, H, h, R, r):
        """
        Calcule le débit d'un puits en nappe captive (Formule de Thiem-Dupuit).

        Args:
            K (float): Coeff. de perméabilité (m/s).
            e (float): Épaisseur de la nappe captive (m).
            H (float): Charge piézométrique initiale (m).
            h (float): Charge dans le puits en pompage (m).
            R (float): Rayon d'influence (m).
            r (float): Rayon du puits (m).

        Returns:
            float: Débit Q en m³/s.
        """
        if R <= r or r <= 0:
            raise ValueError("Le rayon d'influence R doit être supérieur au rayon du puits r.")
        Q = (2 * K * math.pi * e * (H - h)) / math.log(R / r)
        return Q

# --- Programme Principal d'Exemple ---
if __name__ == "__main__":
    calculateur = CalculProductionEau()
    
    print("\n" + "="*50)
    print("EXEMPLE 1 : PRÉVISIONS DÉMOGRAPHIQUES")
    print("="*50)
    # Données de base
    pop_1990, annee_1990 = 90000, 1990
    pop_2000, annee_2000 = 100000, 2000
    pop_2010, annee_2010 = 108000, 2010
    annee_cible = 2025
    
    print(f"Données: P({annee_1990})={pop_1990}, P({annee_2000})={pop_2000}, P({annee_2010})={pop_2010}")
    print(f"Année de prévision : {annee_cible}\n")

    # Calculs
    pop_arith = calculateur.prevision_population_arithmetique(pop_2000, annee_2000, pop_2010, annee_2010, annee_cible)
    pop_geom = calculateur.prevision_population_geometrique(pop_2000, annee_2000, pop_2010, annee_2010, annee_cible)
    # Pour la logistique, on utilise les 3 points : y0=1990, y1=2000, y2=2010. n=10 ans. x = 2025-1990 = 35 ans.
    pop_logist = calculateur.prevision_population_logistique(pop_1990, pop_2000, pop_2010, 10, annee_cible - annee_1990)
    
    print(f"- Prévision Arithmétique : {pop_arith:,.0f} habitants")
    print(f"- Prévision Géométrique  : {pop_geom:,.0f} habitants")
    print(f"- Prévision Logistique   : {pop_logist:,.0f} habitants")

    print("\n" + "="*50)
    print("EXEMPLE 2 : CALCUL DE DÉBIT DE PUITS")
    print("="*50)
    # Paramètres communs
    K_permeabilite = 0.0005 # m/s
    R_influence = 300 # m
    r_puits = 0.25 # m
    H_initial = 50 # m
    h_pompage = 45 # m
    
    print("Scénario 1: Nappe Libre")
    debit_libre = calculateur.calcul_debit_puits_nappe_libre(K_permeabilite, H_initial, h_pompage, R_influence, r_puits)
    print(f"  Débit estimé : {debit_libre:.5f} m³/s  ({debit_libre * 3600:.2f} m³/h)")
    
    print("\nScénario 2: Nappe Captive")
    e_nappe_captive = 15 # m
    debit_captif = calculateur.calcul_debit_puits_nappe_captive(K_permeabilite, e_nappe_captive, H_initial, h_pompage, R_influence, r_puits)
    print(f"  Débit estimé : {debit_captif:.5f} m³/s  ({debit_captif * 3600:.2f} m³/h)")
    print("="*50)