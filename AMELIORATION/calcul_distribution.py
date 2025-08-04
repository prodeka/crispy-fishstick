import json
import math
import os

class CalculDistribution:
    """
    Classe pour les calculs du chapitre 5 : Distribution de l'eau.
    - Validation des paramètres de conception (vitesse, pression).
    - Calcul par la formule de Flamant.
    - Calcul des conduites équivalentes (série, parallèle).
    - Implémentation du calcul de correction de débit pour la méthode de Hardy-Cross.
    """
    def __init__(self, fichier_donnees="donnees_distribution.json"):
        if not os.path.exists(fichier_donnees):
            raise FileNotFoundError(f"Erreur : Le fichier de données '{fichier_donnees}' est introuvable.")
        with open(fichier_donnees, 'r', encoding='utf-8') as f:
            self.donnees = json.load(f)
        print("✅ Fichier de données de distribution chargé avec succès.")

    # --- Fonctions de Validation et de Conception ---
    def verifier_vitesse(self, vitesse_ms):
        """Vérifie si la vitesse est dans la plage admissible."""
        vmin = self.donnees['regles_conception']['vitesses_admissibles_ms']['min']
        vmax = self.donnees['regles_conception']['vitesses_admissibles_ms']['max']
        if vmin <= vitesse_ms <= vmax:
            return f"OK ({vitesse_ms:.2f} m/s est dans la plage [{vmin}-{vmax}] m/s)"
        else:
            return f"Hors plage ({vitesse_ms:.2f} m/s n'est pas dans la plage [{vmin}-{vmax}] m/s)"

    def get_pression_requise_m(self, nombre_etages):
        """Retourne la pression requise en mètres pour un nombre d'étages donné."""
        for item in self.donnees['pressions_requises_par_etage_mCE']:
            if item['etages'] == nombre_etages:
                return item['hauteur_m_min'], item['hauteur_m_max']
        return None, None

    # --- Formule de Flamant ---
    def perte_de_charge_unitaire_flamant(self, debit_m3s, diametre_m):
        """Calcule la perte de charge unitaire j (sans dimension) selon Flamant."""
        # j = 0.001404043 * Q^1.75 / D^4.75
        if diametre_m <= 0 or debit_m3s < 0:
            return 0
        return 0.001404043 * (debit_m3s**1.75) / (diametre_m**4.75)
    
    def calcul_diametre_flamant(self, debit_m3s, perte_charge_unitaire_j):
        """Calcule le diamètre D requis pour un débit Q et une perte de charge j."""
        # D = (0.001404043 * Q^1.75 / j)^(1/4.75)
        if perte_charge_unitaire_j <= 0 or debit_m3s < 0:
            return 0
        return (0.001404043 * debit_m3s**1.75 / perte_charge_unitaire_j)**(1/4.75)

    # --- Conduites Équivalentes ---
    def resistance_equivalente_serie(self, liste_resistances_K):
        """Calcule la résistance équivalente K pour des conduites en série."""
        return sum(liste_resistances_K)

    def resistance_equivalente_parallele(self, liste_resistances_K, n):
        """Calcule la résistance équivalente K pour des conduites en parallèle."""
        # T = 1 / K^(1/n)
        # Te = Σ(Ti)
        # Ke = (1 / Te)^n
        if any(k <= 0 for k in liste_resistances_K):
            raise ValueError("Les résistances K doivent être positives.")
        beta = 1.0 / n
        conductances_T = [(1.0 / k**beta) for k in liste_resistances_K]
        conductance_equivalente_Te = sum(conductances_T)
        return (1.0 / conductance_equivalente_Te)**n

    # --- Méthode de Hardy-Cross ---
    def calcul_correction_hardy_cross(self, boucle_maillage, nom_formule="Universelle"):
        """
        Calcule la correction de débit ΔQ pour une boucle de réseau maillé.

        Args:
            boucle_maillage (list): Liste de dictionnaires, chaque dict représentant une conduite
                                    avec {'resistance_K': float, 'debit_Q': float (positif ou négatif)}.
            nom_formule (str): Nom de la formule à utiliser (voir JSON).

        Returns:
            float: La correction de débit ΔQ à appliquer.
        """
        params = self.donnees['parametres_formules_hardy_cross'].get(nom_formule)
        if not params:
            raise ValueError(f"Formule '{nom_formule}' non trouvée dans la base de données.")
        n = params['n']
        
        # Calcul de Σ(K * Q^n)
        somme_K_Qn = sum(pipe['resistance_K'] * (pipe['debit_Q'] * abs(pipe['debit_Q'])**(n-1)) for pipe in boucle_maillage)
        # On utilise une forme qui préserve le signe pour Q^n quand n n'est pas entier

        # Calcul de Σ(n * K * |Q|^(n-1))
        somme_denominateur = sum(n * pipe['resistance_K'] * abs(pipe['debit_Q'])**(n-1) for pipe in boucle_maillage)

        if somme_denominateur == 0:
            return 0 # Pas de correction si les débits sont nuls
        
        delta_Q = -somme_K_Qn / somme_denominateur
        return delta_Q


# --- Programme Principal d'Exemple ---
if __name__ == "__main__":
    calc = CalculDistribution()

    print("\n" + "="*50)
    print("EXEMPLE 1 : VALIDATION DES RÈGLES DE CONCEPTION")
    print("="*50)
    # Vérification de vitesse
    vitesse_test = 0.8 # m/s
    print(f"Vérification d'une vitesse de {vitesse_test} m/s : {calc.verifier_vitesse(vitesse_test)}")
    # Pression requise
    etages = 4
    p_min, p_max = calc.get_pression_requise_m(etages)
    print(f"Pression requise pour un immeuble de {etages} étages : entre {p_min} et {p_max} mCE")

    print("\n" + "="*50)
    print("EXEMPLE 2 : CALCUL AVEC LA FORMULE DE FLAMANT")
    print("="*50)
    # Données inspirées de l'exemple du réseau ramifié du livre
    debit_troncon_l_s = 1.95 # l/s (Q1 du tableau 9.1)
    debit_troncon_m3s = debit_troncon_l_s / 1000.0
    diametre_calcule = 0.03748 # m (D de la ligne A du tableau 9.1)
    
    j = calc.perte_de_charge_unitaire_flamant(debit_troncon_m3s, diametre_calcule)
    print(f"Pour Q={debit_troncon_l_s} l/s et D={diametre_calcule*1000:.2f} mm, j = {j:.5f} (proche de 0.15123 dans le texte)")

    diametre_inverse = calc.calcul_diametre_flamant(debit_troncon_m3s, j)
    print(f"Vérification inverse : Pour Q={debit_troncon_l_s} l/s et j={j:.5f}, D = {diametre_inverse*1000:.2f} mm")

    print("\n" + "="*50)
    print("EXEMPLE 3 : CALCUL DE RÉSISTANCE ÉQUIVALENTE")
    print("="*50)
    resistances_serie = [100, 250, 50]
    k_eq_serie = calc.resistance_equivalente_serie(resistances_serie)
    print(f"Résistances en série {resistances_serie} -> K_eq = {k_eq_serie}")
    
    resistances_parallele = [500, 300]
    n_hazen = calc.donnees['parametres_formules_hardy_cross']['Hazen-Williams']['n']
    k_eq_parallele = calc.resistance_equivalente_parallele(resistances_parallele, n_hazen)
    print(f"Résistances en parallèle {resistances_parallele} (formule Hazen, n={n_hazen}) -> K_eq = {k_eq_parallele:.2f}")

    print("\n" + "="*50)
    print("EXEMPLE 4 : CALCUL DE CORRECTION DE DÉBIT (HARDY-CROSS)")
    print("="*50)
    # Scénario : une boucle simple avec 3 conduites et une estimation initiale des débits
    ma_boucle = [
        {'resistance_K': 150, 'debit_Q': 0.05},  # Débit estimé dans le sens horaire (+)
        {'resistance_K': 200, 'debit_Q': 0.03},  # Débit estimé dans le sens horaire (+)
        {'resistance_K': 100, 'debit_Q': -0.08}  # Débit estimé dans le sens anti-horaire (-) pour fermer la boucle
    ]
    
    print("Boucle de test (K, Q) : [(150, 0.05), (200, 0.03), (100, -0.08)]")
    formule_utilisee = "Hazen-Williams"
    delta_q = calc.calcul_correction_hardy_cross(ma_boucle, formule_utilisee)
    print(f"Formule utilisée : {formule_utilisee} (n={n_hazen})")
    print(f"Correction de débit calculée ΔQ = {delta_q:.6f} m³/s")
    print("\nLes nouveaux débits seraient :")
    for pipe in ma_boucle:
        print(f"  Conduite (K={pipe['resistance_K']}) : Q_nouveau = {pipe['debit_Q'] + delta_q:.4f} m³/s")