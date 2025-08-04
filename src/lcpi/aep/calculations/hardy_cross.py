"""
Module de calculs pour la méthode Hardy-Cross
Implémentation de la méthode itérative pour le dimensionnement des réseaux maillés
"""

import math
import json
from typing import List, Dict, Tuple, Optional
from pathlib import Path

class HardyCrossError(Exception):
    """Exception personnalisée pour les erreurs Hardy-Cross"""
    pass

def calculate_resistance_coefficient(
    longueur_m: float, 
    diametre_m: float, 
    coefficient_rugosite: float, 
    formule: str = "hazen_williams"
) -> float:
    """
    Calcule le coefficient de résistance K pour une conduite.
    
    Args:
        longueur_m: Longueur de la conduite en mètres
        diametre_m: Diamètre intérieur de la conduite en mètres
        coefficient_rugosite: Coefficient de rugosité (C pour Hazen-Williams, n pour Manning)
        formule: Formule utilisée ("hazen_williams", "manning", "darcy_weisbach")
    
    Returns:
        Coefficient de résistance K
    """
    if longueur_m <= 0 or diametre_m <= 0 or coefficient_rugosite <= 0:
        raise HardyCrossError("Paramètres physiques doivent être positifs")
    
    if formule.lower() == "hazen_williams":
        # K = 10.65 * L / (C^1.852 * D^4.87)
        return 10.65 * longueur_m / (coefficient_rugosite**1.852 * diametre_m**4.87)
    
    elif formule.lower() == "manning":
        # K = 10.29 * n^2 * L / D^(16/3)
        return 10.29 * coefficient_rugosite**2 * longueur_m / (diametre_m**(16/3))
    
    elif formule.lower() == "darcy_weisbach":
        # K = 8 * λ * L / (g * π^2 * D^5)
        # λ est le coefficient de friction de Darcy-Weisbach
        g = 9.81  # m/s²
        return 8 * coefficient_rugosite * longueur_m / (g * math.pi**2 * diametre_m**5)
    
    else:
        raise HardyCrossError(f"Formule '{formule}' non supportée")

def hardy_cross_iteration(
    boucle: List[Dict], 
    formule: str = "hazen_williams"
) -> float:
    """
    Effectue une itération de la méthode Hardy-Cross pour une boucle.
    
    Args:
        boucle: Liste de dictionnaires représentant les conduites de la boucle
               Chaque dict doit contenir: {'resistance_K': float, 'debit_Q': float}
        formule: Formule utilisée pour déterminer l'exposant n
    
    Returns:
        Correction de débit ΔQ à appliquer
    """
    # Déterminer l'exposant n selon la formule
    exposants = {
        "hazen_williams": 1.852,
        "manning": 2.0,
        "darcy_weisbach": 2.0,
        "flamant": 1.75
    }
    
    n = exposants.get(formule.lower(), 2.0)
    
    # Calcul de Σ(K * Q^n)
    somme_numerateur = 0.0
    for conduite in boucle:
        K = conduite['resistance_K']
        Q = conduite['debit_Q']
        # Préserver le signe pour Q^n
        somme_numerateur += K * (Q * abs(Q)**(n-1))
    
    # Calcul de Σ(n * K * |Q|^(n-1))
    somme_denominateur = 0.0
    for conduite in boucle:
        K = conduite['resistance_K']
        Q = conduite['debit_Q']
        somme_denominateur += n * K * abs(Q)**(n-1)
    
    if somme_denominateur == 0:
        return 0.0  # Pas de correction si les débits sont nuls
    
    # Calcul de la correction ΔQ
    delta_Q = -somme_numerateur / somme_denominateur
    return delta_Q

def hardy_cross_network(
    reseau: Dict,
    tolerance: float = 1e-6,
    max_iterations: int = 100,
    formule: str = "hazen_williams",
    afficher_iterations: bool = False
) -> Dict:
    """
    Applique la méthode Hardy-Cross complète à un réseau maillé.
    
    Args:
        reseau: Dictionnaire contenant:
               - 'mailles': Liste des mailles (chaque maille est une liste d'IDs de conduites)
               - 'conduites': Dictionnaire des conduites {id: {'resistance_K': float, 'debit_Q': float}}
        tolerance: Tolérance pour la convergence
        max_iterations: Nombre maximum d'itérations
        formule: Formule de perte de charge utilisée
        afficher_iterations: Afficher les détails de chaque itération
    
    Returns:
        Dictionnaire avec les résultats:
        - 'conduites_finales': Débits finaux par conduite
        - 'iterations': Nombre d'itérations effectuées
        - 'convergence': Booléen indiquant si la convergence a été atteinte
        - 'erreur_finale': Erreur finale (somme des corrections)
        - 'historique_iterations': Détails de chaque itération
    """
    mailles = reseau['mailles']
    conduites = reseau['conduites'].copy()
    
    iteration = 0
    convergence = False
    historique_iterations = []
    
    if afficher_iterations:
        print(f"🔄 Début des calculs Hardy-Cross (tolérance: {tolerance:.2e})")
        print(f"📊 Nombre de mailles: {len(mailles)}")
        print(f"🔧 Formule utilisée: {formule}")
        print("-" * 60)
    
    while iteration < max_iterations:
        corrections_par_maille = []
        debits_iteration = {}
        
        # Sauvegarder les débits actuels
        for id_conduite, conduite in conduites.items():
            debits_iteration[id_conduite] = conduite['debit_Q']
        
        # Calculer les corrections pour chaque maille
        for i, maille in enumerate(mailles):
            boucle = []
            for id_conduite in maille:
                if id_conduite in conduites:
                    boucle.append(conduites[id_conduite])
            
            if boucle:
                delta_Q = hardy_cross_iteration(boucle, formule)
                corrections_par_maille.append(delta_Q)
            else:
                corrections_par_maille.append(0.0)
        
        # Appliquer les corrections aux débits
        for i, maille in enumerate(mailles):
            delta_Q = corrections_par_maille[i]
            for id_conduite in maille:
                if id_conduite in conduites:
                    conduites[id_conduite]['debit_Q'] += delta_Q
        
        # Vérifier la convergence
        max_correction = max(abs(corr) for corr in corrections_par_maille)
        
        # Enregistrer l'historique
        historique_iterations.append({
            'iteration': iteration + 1,
            'corrections_par_maille': corrections_par_maille.copy(),
            'max_correction': max_correction,
            'debits': debits_iteration.copy()
        })
        
        if afficher_iterations:
            print(f"🔄 Itération {iteration + 1:2d}: max_correction = {max_correction:.2e}")
            for i, correction in enumerate(corrections_par_maille):
                print(f"    Maille {i+1}: ΔQ = {correction:+.2e} m³/s")
        
        if max_correction < tolerance:
            convergence = True
            if afficher_iterations:
                print(f"✅ Convergence atteinte après {iteration + 1} itérations")
            break
        
        iteration += 1
    
    if not convergence and afficher_iterations:
        print(f"⚠️  Convergence non atteinte après {max_iterations} itérations")
    
    return {
        'conduites_finales': conduites,
        'iterations': iteration,
        'convergence': convergence,
        'erreur_finale': max_correction if convergence else max_correction,
        'historique_iterations': historique_iterations
    }

def validate_hardy_cross_data(data: Dict) -> bool:
    """
    Valide les données d'entrée pour la méthode Hardy-Cross.
    
    Args:
        data: Données à valider
    
    Returns:
        True si les données sont valides
    
    Raises:
        HardyCrossError: Si les données sont invalides
    """
    required_keys = ['mailles', 'conduites']
    
    for key in required_keys:
        if key not in data:
            raise HardyCrossError(f"Clé requise '{key}' manquante")
    
    if not isinstance(data['mailles'], list):
        raise HardyCrossError("'mailles' doit être une liste")
    
    if not isinstance(data['conduites'], dict):
        raise HardyCrossError("'conduites' doit être un dictionnaire")
    
    # Valider chaque maille
    for i, maille in enumerate(data['mailles']):
        if not isinstance(maille, list):
            raise HardyCrossError(f"Maille {i} doit être une liste")
        
        for id_conduite in maille:
            if id_conduite not in data['conduites']:
                raise HardyCrossError(f"Conduite {id_conduite} de la maille {i} non trouvée")
    
    # Valider chaque conduite
    for id_conduite, conduite in data['conduites'].items():
        if not isinstance(conduite, dict):
            raise HardyCrossError(f"Conduite {id_conduite} doit être un dictionnaire")
        
        required_conduite_keys = ['resistance_K', 'debit_Q']
        for key in required_conduite_keys:
            if key not in conduite:
                raise HardyCrossError(f"Clé '{key}' manquante pour la conduite {id_conduite}")
        
        if not isinstance(conduite['resistance_K'], (int, float)) or conduite['resistance_K'] <= 0:
            raise HardyCrossError(f"resistance_K de la conduite {id_conduite} doit être un nombre positif")
        
        if not isinstance(conduite['debit_Q'], (int, float)):
            raise HardyCrossError(f"debit_Q de la conduite {id_conduite} doit être un nombre")
    
    return True

def load_hardy_cross_data(file_path: str) -> Dict:
    """
    Charge les données Hardy-Cross depuis un fichier JSON ou YAML.
    
    Args:
        file_path: Chemin vers le fichier de données
    
    Returns:
        Données du réseau
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise HardyCrossError(f"Fichier {file_path} non trouvé")
    
    if file_path.suffix.lower() == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif file_path.suffix.lower() in ['.yml', '.yaml']:
        try:
            import yaml
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except ImportError:
            raise HardyCrossError("PyYAML requis pour les fichiers YAML")
    else:
        raise HardyCrossError("Format de fichier non supporté (JSON ou YAML requis)")
    
    validate_hardy_cross_data(data)
    return data

def export_hardy_cross_results(
    results: Dict, 
    output_file: str, 
    format: str = "json"
) -> None:
    """
    Exporte les résultats Hardy-Cross vers un fichier.
    
    Args:
        results: Résultats de hardy_cross_network
        output_file: Chemin du fichier de sortie
        format: Format de sortie ("json", "csv")
    """
    output_path = Path(output_file)
    
    if format.lower() == "json":
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    elif format.lower() == "csv":
        import csv
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_Conduite', 'Resistance_K', 'Debit_Final_m3s', 'Debit_Final_ls'])
            
            for id_conduite, conduite in results['conduites_finales'].items():
                debit_m3s = conduite['debit_Q']
                debit_ls = debit_m3s * 1000  # Conversion en l/s
                writer.writerow([id_conduite, conduite['resistance_K'], debit_m3s, debit_ls])
    
    else:
        raise HardyCrossError(f"Format de sortie '{format}' non supporté")

def get_hardy_cross_help() -> str:
    """
    Retourne l'aide pour les fonctions Hardy-Cross.
    
    Returns:
        Texte d'aide formaté
    """
    return """
🔧 MÉTHODE HARDY-CROSS - AIDE

La méthode Hardy-Cross est une technique itérative pour calculer la distribution 
des débits dans un réseau maillé d'eau potable.

📋 FONCTIONS DISPONIBLES:

1. calculate_resistance_coefficient(longueur_m, diametre_m, coefficient_rugosite, formule)
   - Calcule le coefficient de résistance K pour une conduite
   - Formules supportées: "hazen_williams", "manning", "darcy_weisbach"

2. hardy_cross_iteration(boucle, formule)
   - Effectue une itération Hardy-Cross pour une boucle
   - Retourne la correction de débit ΔQ

3. hardy_cross_network(reseau, tolerance, max_iterations, formule)
   - Applique la méthode complète à un réseau
   - Retourne les débits finaux et métadonnées

4. validate_hardy_cross_data(data)
   - Valide les données d'entrée
   - Vérifie la structure et les types

5. load_hardy_cross_data(file_path)
   - Charge les données depuis JSON/YAML
   - Valide automatiquement les données

6. export_hardy_cross_results(results, output_file, format)
   - Exporte les résultats en JSON ou CSV

📊 FORMAT DES DONNÉES D'ENTRÉE:
{
  "mailles": [
    ["C1", "C2", "C3"],  # Maille 1
    ["C2", "C4", "C5"]   # Maille 2
  ],
  "conduites": {
    "C1": {"resistance_K": 100.0, "debit_Q": 0.05},
    "C2": {"resistance_K": 150.0, "debit_Q": 0.03},
    ...
  }
}

⚙️ PARAMÈTRES:
- tolerance: Précision de convergence (défaut: 1e-6)
- max_iterations: Nombre max d'itérations (défaut: 100)
- formule: Formule de perte de charge (défaut: "hazen_williams")

📝 EXEMPLE D'UTILISATION:
```python
from lcpi.aep.calculations.hardy_cross import hardy_cross_network, load_hardy_cross_data

# Charger les données
reseau = load_hardy_cross_data("reseau_exemple.json")

# Calculer
resultats = hardy_cross_network(reseau, tolerance=1e-6)

# Afficher les résultats
print(f"Convergence: {resultats['convergence']}")
print(f"Itérations: {resultats['iterations']}")
```
""" 