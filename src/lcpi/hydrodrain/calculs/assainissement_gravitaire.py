import math
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# Constantes
G = 9.81  # Accélération de la pesanteur
TC_MINIMUM_MIN = 5.0  # Temps de concentration minimum en minutes
MAX_ITERATIONS = 20
TOLERANCE = 0.1  # Tolérance pour la convergence en minutes

@dataclass
class Troncon:
    """Représente un segment de canalisation dans le réseau d'assainissement."""
    id: str
    type_section: str  # "circulaire", "rectangulaire", "trapezoidal"
    longueur_troncon_m: float
    pente_troncon: float
    ks_manning_strickler: float
    amont_ids: List[str]
    
    # Données spécifiques eaux usées
    population: Optional[int] = None
    dotation_l_jour_hab: Optional[float] = None
    coefficient_pointe: Optional[float] = None
    
    # Données spécifiques eaux pluviales
    surface_propre_ha: Optional[float] = None
    coefficient_ruissellement: Optional[float] = None
    longueur_parcours_m: Optional[float] = None
    pente_parcours_m_m: Optional[float] = None
    
    # Résultats calculés
    q_max_m3s: Optional[float] = None
    resultat_dimensionnement: Optional[Dict] = None
    statut: str = "En attente"
    tc_final_min: Optional[float] = None
    surface_cumulee_ha: Optional[float] = None
    coefficient_moyen: Optional[float] = None

class Reseau:
    """Représente l'ensemble du réseau d'assainissement."""
    
    def __init__(self):
        self.troncons: Dict[str, Troncon] = {}
    
    def ajouter_troncon(self, troncon: Troncon):
        """Ajoute un tronçon au réseau."""
        self.troncons[troncon.id] = troncon
    
    def trier_topologiquement(self) -> List[Troncon]:
        """
        Trie les tronçons dans l'ordre de calcul (amont vers aval).
        Utilise un algorithme de tri topologique.
        """
        # Créer un graphe des dépendances
        dependances = {troncon_id: set(troncon.amont_ids) for troncon_id, troncon in self.troncons.items()}
        
        # Algorithme de tri topologique
        resultat = []
        noeuds_disponibles = [troncon_id for troncon_id, deps in dependances.items() if not deps]
        
        while noeuds_disponibles:
            noeud = noeuds_disponibles.pop(0)
            resultat.append(self.troncons[noeud])
            
            # Mettre à jour les dépendances
            for troncon_id, deps in dependances.items():
                if noeud in deps:
                    deps.remove(noeud)
                    if not deps:
                        noeuds_disponibles.append(troncon_id)
        
        if len(resultat) != len(self.troncons):
            raise ValueError("Le réseau contient des cycles ou des tronçons isolés")
        
        return resultat

def dimensionner_reseau_eaux_usees(reseau: Reseau) -> Dict:
    """
    Dimensionne un réseau d'eaux usées (mode déterministe).
    
    Args:
        reseau: Objet Reseau contenant les tronçons
    
    Returns:
        dict: Résultats du dimensionnement
    """
    try:
        troncons_tries = reseau.trier_topologiquement()
        resultats = {"statut": "OK", "troncons": []}
        
        for troncon in troncons_tries:
            # 1. Calcul du débit propre
            debit_propre = calculer_debit_propre_eaux_usees(troncon)
            
            # 2. Calcul du débit amont
            debit_amont = calculer_debit_amont(troncon, reseau)
            
            # 3. Calcul du débit de projet
            troncon.q_max_m3s = debit_propre + debit_amont
            
            # 4. Dimensionnement hydraulique
            troncon.resultat_dimensionnement = dimensionner_section(troncon)
            troncon.statut = "OK"
            
            resultats["troncons"].append(asdict(troncon))
        
        return resultats
        
    except Exception as e:
        return {"statut": "Erreur", "message": str(e)}

def dimensionner_reseau_eaux_pluviales(reseau: Reseau, params_pluie: Dict) -> Dict:
    """
    Dimensionne un réseau d'eaux pluviales (mode hydrologique itératif).
    
    Args:
        reseau: Objet Reseau contenant les tronçons
        params_pluie: Paramètres de la pluie (type IDF, coefficients)
    
    Returns:
        dict: Résultats du dimensionnement
    """
    try:
        troncons_tries = reseau.trier_topologiquement()
        resultats = {"statut": "OK", "troncons": []}
        
        for troncon in troncons_tries:
            # 1. Agrégation des données amont
            agreger_donnees_amont(troncon, reseau)
            
            # 2. Calcul itératif
            resultat_calcul = run_calcul_rationnelle(troncon, params_pluie)
            
            if resultat_calcul["statut"] == "OK":
                troncon.q_max_m3s = resultat_calcul["debit_projet"]
                troncon.tc_final_min = resultat_calcul["tc_final"]
                troncon.resultat_dimensionnement = dimensionner_section(troncon)
                troncon.statut = "OK"
            else:
                troncon.statut = "Erreur"
                troncon.resultat_dimensionnement = resultat_calcul
            
            resultats["troncons"].append(asdict(troncon))
        
        return resultats
        
    except Exception as e:
        return {"statut": "Erreur", "message": str(e)}

def calculer_debit_propre_eaux_usees(troncon: Troncon) -> float:
    """Calcule le débit propre d'un tronçon pour les eaux usées."""
    if not all([troncon.population, troncon.dotation_l_jour_hab, troncon.coefficient_pointe]):
        return 0.0
    
    # Formule: Q = (Dotation * Coeff_Pointe * Population) / (1000 * 86400)
    debit = (troncon.dotation_l_jour_hab * troncon.coefficient_pointe * troncon.population) / (1000 * 86400)
    return debit

def calculer_debit_amont(troncon: Troncon, reseau: Reseau) -> float:
    """Calcule le débit cumulé des tronçons amont."""
    debit_total = 0.0
    for amont_id in troncon.amont_ids:
        if amont_id in reseau.troncons:
            troncon_amont = reseau.troncons[amont_id]
            if troncon_amont.q_max_m3s is not None:
                debit_total += troncon_amont.q_max_m3s
    return debit_total

def agreger_donnees_amont(troncon: Troncon, reseau: Reseau):
    """Agrège les données des tronçons amont pour les eaux pluviales."""
    # Surface cumulée
    surface_cumulee = troncon.surface_propre_ha or 0.0
    surface_totale_amont = 0.0
    coefficient_total_pondere = 0.0
    tc_amont_max = 0.0
    
    for amont_id in troncon.amont_ids:
        if amont_id in reseau.troncons:
            troncon_amont = reseau.troncons[amont_id]
            if troncon_amont.surface_cumulee_ha:
                surface_totale_amont += troncon_amont.surface_cumulee_ha
                coefficient_total_pondere += troncon_amont.coefficient_moyen * troncon_amont.surface_cumulee_ha
            if troncon_amont.tc_final_min:
                tc_amont_max = max(tc_amont_max, troncon_amont.tc_final_min)
    
    troncon.surface_cumulee_ha = surface_cumulee + surface_totale_amont
    troncon.coefficient_moyen = (troncon.coefficient_ruissellement * surface_cumulee + coefficient_total_pondere) / troncon.surface_cumulee_ha if troncon.surface_cumulee_ha > 0 else 0.0

def run_calcul_rationnelle(troncon: Troncon, params_pluie: Dict) -> Dict:
    """
    Exécute le calcul rationnel itératif pour un tronçon.
    
    Args:
        troncon: Tronçon à calculer
        params_pluie: Paramètres de la pluie
    
    Returns:
        dict: Résultats du calcul
    """
    try:
        # Initialisation
        tc_surface = calculer_tc_surface(troncon)
        tc_amont_max = max([reseau.troncons[amont_id].tc_final_min or 0 for amont_id in troncon.amont_ids]) if troncon.amont_ids else 0
        tc_iteration = max(tc_surface, tc_amont_max, TC_MINIMUM_MIN)
        
        for iteration in range(MAX_ITERATIONS):
            # 1. Calcul de l'intensité
            intensite = calculer_intensite_pluie(tc_iteration, params_pluie)
            
            # 2. Calcul du débit
            debit_projet = (troncon.coefficient_moyen * intensite * troncon.surface_cumulee_ha) / 360
            
            # 3. Dimensionnement provisoire
            resultat_dim = dimensionner_section_provisoire(debit_projet, troncon)
            if resultat_dim["statut"] != "OK":
                return resultat_dim
            
            vitesse = resultat_dim["vitesse_ms"]
            
            # 4. Calcul du nouveau tc
            temps_parcours = troncon.longueur_parcours_m / (vitesse * 60)  # en minutes
            tc_calcule_nouveau = tc_amont_max + temps_parcours
            
            # 5. Test de convergence
            if abs(tc_calcule_nouveau - tc_iteration) < TOLERANCE:
                return {
                    "statut": "OK",
                    "debit_projet": debit_projet,
                    "tc_final": tc_calcule_nouveau,
                    "iterations": iteration + 1
                }
            
            # 6. Préparation de la prochaine itération
            tc_iteration = max(tc_calcule_nouveau, TC_MINIMUM_MIN)
        
        return {"statut": "Erreur", "message": "Convergence non atteinte"}
        
    except Exception as e:
        return {"statut": "Erreur", "message": str(e)}

def calculer_tc_surface(troncon: Troncon) -> float:
    """Calcule le temps de concentration de surface selon Kirpich."""
    if not all([troncon.longueur_parcours_m, troncon.pente_parcours_m_m]):
        return TC_MINIMUM_MIN
    
    # Formule de Kirpich: tc = 0.01947 * L^0.77 * P^(-0.385)
    longueur_km = troncon.longueur_parcours_m / 1000
    pente_m_km = troncon.pente_parcours_m_m * 1000
    
    tc = 0.01947 * (longueur_km**0.77) * (pente_m_km**(-0.385))
    return tc

def calculer_intensite_pluie(tc_minutes: float, params_pluie: Dict) -> float:
    """Calcule l'intensité de pluie selon le type de formule IDF."""
    type_idf = params_pluie.get("type", "talbot")
    
    if type_idf.lower() == "talbot":
        a = params_pluie.get("a", 120)
        b = params_pluie.get("b", 20)
        return a / (b + tc_minutes)
    
    elif type_idf.lower() == "montana":
        a = params_pluie.get("a", 120)
        b = params_pluie.get("b", 0.5)
        return a * (tc_minutes**(-b))
    
    else:
        raise ValueError(f"Type IDF '{type_idf}' non supporté")

def dimensionner_section(troncon: Troncon) -> Dict:
    """Dimensionne la section d'un tronçon selon son type."""
    if troncon.q_max_m3s is None:
        return {"statut": "Erreur", "message": "Débit non calculé"}
    
    if troncon.type_section == "circulaire":
        return dimensionner_circulaire(troncon.q_max_m3s, troncon.pente_troncon, troncon.ks_manning_strickler)
    elif troncon.type_section == "rectangulaire":
        return dimensionner_rectangulaire(troncon.q_max_m3s, troncon.pente_troncon, troncon.ks_manning_strickler)
    elif troncon.type_section == "trapezoidal":
        return dimensionner_trapezoidal(troncon.q_max_m3s, troncon.pente_troncon, troncon.ks_manning_strickler)
    else:
        return {"statut": "Erreur", "message": f"Type de section '{troncon.type_section}' non supporté"}

def dimensionner_section_provisoire(debit_m3s: float, troncon: Troncon) -> Dict:
    """Dimensionnement provisoire pour le calcul itératif."""
    return dimensionner_section(troncon)

def dimensionner_circulaire(debit_m3s: float, pente: float, ks: float) -> Dict:
    """Dimensionne une section circulaire selon Manning-Strickler."""
    diametres_commerciaux_m = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0]
    
    for diametre in diametres_commerciaux_m:
        # Paramètres géométriques
        section = math.pi * (diametre/2)**2
        perimetre = math.pi * diametre
        rayon_hydraulique = section / perimetre  # = diametre/4
        
        # Capacité selon Manning-Strickler
        debit_capacite = ks * section * (rayon_hydraulique**(2/3)) * (pente**0.5)
        
        if debit_capacite >= debit_m3s:
            vitesse = debit_m3s / section
            return {
                "statut": "OK",
                "type_section": "circulaire",
                "diametre_mm": round(diametre * 1000, 0),
                "vitesse_ms": round(vitesse, 2),
                "debit_capacite_m3s": round(debit_capacite, 2),
                "remplissage_pourcent": round((debit_m3s / debit_capacite) * 100, 1)
            }
    
    return {"statut": "Erreur", "message": "Débit trop élevé pour les diamètres disponibles"}

def dimensionner_rectangulaire(debit_m3s: float, pente: float, ks: float) -> Dict:
    """Dimensionne une section rectangulaire selon Manning-Strickler."""
    # Approche simplifiée: on fixe la largeur et on calcule la hauteur
    largeur_m = 0.5  # Largeur fixe pour l'exemple
    
    # Calcul de la hauteur nécessaire
    # Q = ks * (b*h) * ((b*h)/(b+2h))^(2/3) * I^0.5
    # Résolution itérative simplifiée
    hauteur_m = 0.1
    for _ in range(20):
        section = largeur_m * hauteur_m
        perimetre = largeur_m + 2 * hauteur_m
        rayon_hydraulique = section / perimetre
        debit_calcule = ks * section * (rayon_hydraulique**(2/3)) * (pente**0.5)
        
        if debit_calcule >= debit_m3s:
            vitesse = debit_m3s / section
            return {
                "statut": "OK",
                "type_section": "rectangulaire",
                "largeur_m": largeur_m,
                "hauteur_m": round(hauteur_m, 3),
                "vitesse_ms": round(vitesse, 2),
                "debit_capacite_m3s": round(debit_calcule, 2)
            }
        
        hauteur_m += 0.05
    
    return {"statut": "Erreur", "message": "Section rectangulaire insuffisante"}

def dimensionner_trapezoidal(debit_m3s: float, pente: float, ks: float) -> Dict:
    """Dimensionne une section trapézoïdale selon Manning-Strickler."""
    # Approche simplifiée: on fixe la largeur de base et le fruit
    largeur_base_m = 0.5
    fruit = 1.5  # Fruit des talus
    
    hauteur_m = 0.1
    for _ in range(20):
        section = hauteur_m * (largeur_base_m + fruit * hauteur_m)
        perimetre = largeur_base_m + 2 * hauteur_m * math.sqrt(1 + fruit**2)
        rayon_hydraulique = section / perimetre
        debit_calcule = ks * section * (rayon_hydraulique**(2/3)) * (pente**0.5)
        
        if debit_calcule >= debit_m3s:
            vitesse = debit_m3s / section
            return {
                "statut": "OK",
                "type_section": "trapezoidal",
                "largeur_base_m": largeur_base_m,
                "hauteur_m": round(hauteur_m, 3),
                "fruit": fruit,
                "vitesse_ms": round(vitesse, 2),
                "debit_capacite_m3s": round(debit_calcule, 2)
            }
        
        hauteur_m += 0.05
    
    return {"statut": "Erreur", "message": "Section trapézoïdale insuffisante"}

def creer_reseau_depuis_json(filepath: str) -> Reseau:
    """Crée un réseau à partir d'un fichier JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        reseau = Reseau()
        for troncon_data in data.get("troncons", []):
            troncon = Troncon(**troncon_data)
            reseau.ajouter_troncon(troncon)
        
        return reseau
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture du fichier: {e}")

def exporter_resultats_json(reseau: Reseau, filepath: str):
    """Exporte les résultats du réseau au format JSON."""
    resultats = {"troncons": []}
    for troncon in reseau.troncons.values():
        resultats["troncons"].append(asdict(troncon))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(resultats, f, indent=2, ensure_ascii=False)
