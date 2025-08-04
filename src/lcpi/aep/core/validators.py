"""
Validateurs pour les données d'Alimentation en Eau Potable (AEP)

Ce fichier contient les fonctions de validation des données d'entrée
pour assurer la cohérence et la validité des calculs AEP.
"""

from typing import Dict, List, Any, Tuple, Optional
from .constants import *

class AEPValidationError(Exception):
    """Exception levée lors d'une erreur de validation des données AEP"""
    pass

def validate_population_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données de projection démographique.
    
    Args:
        data: Dictionnaire contenant les données de population
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    required_fields = ["methode", "annee_projet"]
    
    # Vérifier les champs requis
    for field in required_fields:
        if field not in data:
            raise AEPValidationError(f"Champ requis manquant: {field}")
    
    # Valider la méthode
    methodes_valides = ["arithmetique", "lineaire", "geometrique", "exponentiel", "malthus", "logistique"]
    if data["methode"] not in methodes_valides:
        raise AEPValidationError(f"Méthode invalide: {data['methode']}. Méthodes valides: {methodes_valides}")
    
    # Valider l'année de projet
    if not isinstance(data["annee_projet"], (int, float)) or data["annee_projet"] <= 0:
        raise AEPValidationError("L'année de projet doit être un nombre positif")
    
    # Validation spécifique selon la méthode
    if data["methode"] in ["arithmetique", "lineaire", "geometrique", "exponentiel", "malthus"]:
        if "pop_annee_1" not in data or "pop_annee_2" not in data:
            raise AEPValidationError(f"Pour la méthode {data['methode']}, pop_annee_1 et pop_annee_2 sont requis")
        
        # Valider les données de population
        for field in ["pop_annee_1", "pop_annee_2"]:
            if not isinstance(data[field], (list, tuple)) or len(data[field]) != 2:
                raise AEPValidationError(f"{field} doit être une liste/tuple de 2 éléments [population, année]")
            
            pop, annee = data[field]
            if not isinstance(pop, (int, float)) or pop <= 0:
                raise AEPValidationError(f"Population invalide dans {field}: {pop}")
            if not isinstance(annee, (int, float)) or annee <= 0:
                raise AEPValidationError(f"Année invalide dans {field}: {annee}")
    
    elif data["methode"] == "logistique":
        required_logistic = ["pop_annee_0", "pop_annee_1", "pop_annee_2"]
        for field in required_logistic:
            if field not in data:
                raise AEPValidationError(f"Pour la méthode logistique, {field} est requis")
            
            if not isinstance(data[field], (list, tuple)) or len(data[field]) != 2:
                raise AEPValidationError(f"{field} doit être une liste/tuple de 2 éléments [population, année]")
    
    return data

def validate_population_unified_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données de projection démographique pour les modules unifiés.
    Accepte les paramètres CLI.
    
    Args:
        data: Dictionnaire contenant les données de population
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    # Paramètres requis pour CLI
    if "population_base" not in data:
        raise AEPValidationError("Champ requis manquant: population_base")
    
    # Valider la population de base
    if not isinstance(data["population_base"], (int, float)) or data["population_base"] <= 0:
        raise AEPValidationError("La population de base doit être un nombre positif")
    
    # Paramètres optionnels avec valeurs par défaut
    data.setdefault("taux_croissance", 0.037)
    data.setdefault("annees", 20)
    data.setdefault("methode", "malthus")
    data.setdefault("verbose", False)
    
    # Valider le taux de croissance
    if not isinstance(data["taux_croissance"], (int, float)):
        raise AEPValidationError("Le taux de croissance doit être un nombre")
    
    # Valider le nombre d'années
    if not isinstance(data["annees"], int) or data["annees"] <= 0:
        raise AEPValidationError("Le nombre d'années doit être un entier positif")
    
    # Valider la méthode
    methodes_valides = ["malthus", "arithmetique", "geometrique", "logistique"]
    if data["methode"] not in methodes_valides:
        raise AEPValidationError(f"Méthode invalide: {data['methode']}. Méthodes valides: {methodes_valides}")
    
    return data

def validate_demand_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données de calcul de demande en eau.
    
    Args:
        data: Dictionnaire contenant les données de demande
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    # Vérifier les champs requis
    if "population" not in data:
        raise AEPValidationError("Champ requis manquant: population")
    
    if "dotation_domestique_l_j_hab" not in data:
        raise AEPValidationError("Champ requis manquant: dotation_domestique_l_j_hab")
    
    # Valider la population
    if not isinstance(data["population"], (int, float)) or data["population"] <= 0:
        raise AEPValidationError("La population doit être un nombre positif")
    
    # Valider la dotation
    if not isinstance(data["dotation_domestique_l_j_hab"], (int, float)) or data["dotation_domestique_l_j_hab"] <= 0:
        raise AEPValidationError("La dotation doit être un nombre positif")
    
    # Valider les champs optionnels
    if "rendement_reseau" in data:
        rendement = data["rendement_reseau"]
        if not isinstance(rendement, (int, float)) or rendement <= 0 or rendement > 1:
            raise AEPValidationError("Le rendement réseau doit être entre 0 et 1")
    
    if "coefficient_pointe" in data:
        coeff = data["coefficient_pointe"]
        if not isinstance(coeff, (int, float)) or coeff <= 0:
            raise AEPValidationError("Le coefficient de pointe doit être un nombre positif")
    
    return data

def validate_demand_unified_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données de demande en eau pour les modules unifiés.
    Accepte les paramètres CLI.
    
    Args:
        data: Dictionnaire contenant les données de demande
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    # Paramètres requis pour CLI
    if "population" not in data:
        raise AEPValidationError("Champ requis manquant: population")
    
    # Valider la population
    if not isinstance(data["population"], int) or data["population"] <= 0:
        raise AEPValidationError("La population doit être un entier positif")
    
    # Paramètres optionnels avec valeurs par défaut
    data.setdefault("dotation_l_j_hab", 150)
    data.setdefault("coefficient_pointe", 1.5)
    data.setdefault("verbose", False)
    
    # Valider la dotation
    if not isinstance(data["dotation_l_j_hab"], (int, float)) or data["dotation_l_j_hab"] <= 0:
        raise AEPValidationError("La dotation doit être un nombre positif")
    
    # Valider le coefficient de pointe
    if not isinstance(data["coefficient_pointe"], (int, float)) or data["coefficient_pointe"] <= 0:
        raise AEPValidationError("Le coefficient de pointe doit être un nombre positif")
    
    return data

def validate_network_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données de dimensionnement réseau.
    
    Args:
        data: Dictionnaire contenant les données du réseau
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    required_fields = ["debit_m3s", "longueur_m", "diametre_m"]
    
    # Vérifier les champs requis
    for field in required_fields:
        if field not in data:
            raise AEPValidationError(f"Champ requis manquant: {field}")
    
    # Valider le débit
    if not isinstance(data["debit_m3s"], (int, float)) or data["debit_m3s"] <= 0:
        raise AEPValidationError("Le débit doit être un nombre positif")
    
    # Valider la longueur
    if not isinstance(data["longueur_m"], (int, float)) or data["longueur_m"] <= 0:
        raise AEPValidationError("La longueur doit être un nombre positif")
    
    # Valider le diamètre
    if not isinstance(data["diametre_m"], (int, float)) or data["diametre_m"] <= 0:
        raise AEPValidationError("Le diamètre doit être un nombre positif")
    
    # Valider le coefficient de rugosité
    if "ks" in data:
        ks = data["ks"]
        if not isinstance(ks, (int, float)) or ks <= 0:
            raise AEPValidationError("Le coefficient de rugosité doit être un nombre positif")
    
    return data

def validate_network_unified_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données de dimensionnement réseau pour les modules unifiés.
    Accepte les paramètres CLI.
    
    Args:
        data: Dictionnaire contenant les données du réseau
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    # Paramètres requis pour CLI
    if "debit_m3s" not in data:
        raise AEPValidationError("Champ requis manquant: debit_m3s")
    
    # Valider le débit
    if not isinstance(data["debit_m3s"], (int, float)) or data["debit_m3s"] <= 0:
        raise AEPValidationError("Le débit doit être un nombre positif")
    
    # Paramètres optionnels avec valeurs par défaut
    data.setdefault("longueur_m", 1000)
    data.setdefault("materiau", "fonte")
    data.setdefault("perte_charge_max_m", 10.0)
    data.setdefault("methode", "darcy")
    
    # Valider la longueur
    if not isinstance(data["longueur_m"], (int, float)) or data["longueur_m"] <= 0:
        raise AEPValidationError("La longueur doit être un nombre positif")
    
    # Valider la perte de charge maximale
    if not isinstance(data["perte_charge_max_m"], (int, float)) or data["perte_charge_max_m"] <= 0:
        raise AEPValidationError("La perte de charge maximale doit être un nombre positif")
    
    # Valider la méthode
    methodes_valides = ["darcy", "manning", "hazen_williams"]
    if data["methode"] not in methodes_valides:
        raise AEPValidationError(f"Méthode invalide: {data['methode']}. Méthodes valides: {methodes_valides}")
    
    # Valider le matériau
    materiaux_valides = ["fonte", "acier", "pvc", "pe", "beton"]
    if data["materiau"] not in materiaux_valides:
        raise AEPValidationError(f"Matériau invalide: {data['materiau']}. Matériaux valides: {materiaux_valides}")
    
    return data

def validate_reservoir_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données de dimensionnement réservoir.
    
    Args:
        data: Dictionnaire contenant les données du réservoir
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    if "besoin_brut_jour" not in data:
        raise AEPValidationError("Champ requis manquant: besoin_brut_jour")
    
    if "type_adduction" not in data:
        raise AEPValidationError("Champ requis manquant: type_adduction")
    
    # Valider le besoin brut
    if not isinstance(data["besoin_brut_jour"], (int, float)) or data["besoin_brut_jour"] <= 0:
        raise AEPValidationError("Le besoin brut journalier doit être un nombre positif")
    
    # Valider le type d'adduction
    types_valides = list(CAPACITE_UTILE.keys())
    if data["type_adduction"] not in types_valides:
        raise AEPValidationError(f"Type d'adduction invalide: {data['type_adduction']}. Types valides: {types_valides}")
    
    return data

def validate_reservoir_unified_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données de dimensionnement réservoir pour les modules unifiés.
    Accepte les paramètres CLI.
    
    Args:
        data: Dictionnaire contenant les données du réservoir
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    # Paramètres requis pour CLI
    if "volume_journalier_m3" not in data:
        raise AEPValidationError("Champ requis manquant: volume_journalier_m3")
    
    # Valider le volume journalier
    if not isinstance(data["volume_journalier_m3"], (int, float)) or data["volume_journalier_m3"] <= 0:
        raise AEPValidationError("Le volume journalier doit être un nombre positif")
    
    # Paramètres optionnels avec valeurs par défaut
    data.setdefault("type_adduction", "continue")
    data.setdefault("forme_reservoir", "cylindrique")
    data.setdefault("type_zone", "ville_francaise_peu_importante")
    
    # Valider le type d'adduction
    types_adduction_valides = ["continue", "intermittente", "24h", "10h_nuit"]
    if data["type_adduction"] not in types_adduction_valides:
        raise AEPValidationError(f"Type d'adduction invalide: {data['type_adduction']}. Types valides: {types_adduction_valides}")
    
    # Valider la forme du réservoir
    formes_valides = ["cylindrique", "rectangulaire"]
    if data["forme_reservoir"] not in formes_valides:
        raise AEPValidationError(f"Forme de réservoir invalide: {data['forme_reservoir']}. Formes valides: {formes_valides}")
    
    # Valider le type de zone
    types_zone_valides = ["ville_francaise_peu_importante", "ville_francaise_importante", "zone_industrielle"]
    if data["type_zone"] not in types_zone_valides:
        raise AEPValidationError(f"Type de zone invalide: {data['type_zone']}. Types valides: {types_zone_valides}")
    
    return data

def validate_pumping_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données de dimensionnement pompage.
    
    Args:
        data: Dictionnaire contenant les données de pompage
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    required_fields = ["debit_m3s", "hmt_m"]
    
    # Vérifier les champs requis
    for field in required_fields:
        if field not in data:
            raise AEPValidationError(f"Champ requis manquant: {field}")
    
    # Valider le débit
    if not isinstance(data["debit_m3s"], (int, float)) or data["debit_m3s"] <= 0:
        raise AEPValidationError("Le débit doit être un nombre positif")
    
    # Valider la HMT
    if not isinstance(data["hmt_m"], (int, float)) or data["hmt_m"] <= 0:
        raise AEPValidationError("La HMT doit être un nombre positif")
    
    # Valider les rendements optionnels
    if "rendement_pompe" in data:
        rendement = data["rendement_pompe"]
        if not isinstance(rendement, (int, float)) or rendement <= 0 or rendement > 1:
            raise AEPValidationError("Le rendement de la pompe doit être entre 0 et 1")
    
    if "rendement_moteur" in data:
        rendement = data["rendement_moteur"]
        if not isinstance(rendement, (int, float)) or rendement <= 0 or rendement > 1:
            raise AEPValidationError("Le rendement du moteur doit être entre 0 et 1")
    
    return data

def validate_pumping_unified_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données de dimensionnement pompage pour les modules unifiés.
    Accepte les paramètres CLI.
    
    Args:
        data: Dictionnaire contenant les données de pompage
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    # Paramètres requis pour CLI
    if "debit_m3h" not in data:
        raise AEPValidationError("Champ requis manquant: debit_m3h")
    
    # Valider le débit
    if not isinstance(data["debit_m3h"], (int, float)) or data["debit_m3h"] <= 0:
        raise AEPValidationError("Le débit doit être un nombre positif")
    
    # Paramètres optionnels avec valeurs par défaut
    data.setdefault("hmt_m", 50.0)
    data.setdefault("type_pompe", "centrifuge")
    data.setdefault("rendement_pompe", 0.75)
    
    # Valider la HMT
    if not isinstance(data["hmt_m"], (int, float)) or data["hmt_m"] <= 0:
        raise AEPValidationError("La hauteur manométrique totale doit être un nombre positif")
    
    # Valider le rendement
    if not isinstance(data["rendement_pompe"], (int, float)) or data["rendement_pompe"] <= 0 or data["rendement_pompe"] > 1:
        raise AEPValidationError("Le rendement doit être un nombre entre 0 et 1")
    
    # Valider le type de pompe
    types_pompes_valides = ["centrifuge", "helice", "volumetrique"]
    if data["type_pompe"] not in types_pompes_valides:
        raise AEPValidationError(f"Type de pompe invalide: {data['type_pompe']}. Types valides: {types_pompes_valides}")
    
    return data

def validate_protection_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données de protection anti-bélier.
    
    Args:
        data: Dictionnaire contenant les données de protection
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    required_fields = ["debit_m3s", "diametre_m", "longueur_m", "epaisseur_mm"]
    
    # Vérifier les champs requis
    for field in required_fields:
        if field not in data:
            raise AEPValidationError(f"Champ requis manquant: {field}")
    
    # Valider le débit
    if not isinstance(data["debit_m3s"], (int, float)) or data["debit_m3s"] <= 0:
        raise AEPValidationError("Le débit doit être un nombre positif")
    
    # Valider le diamètre
    if not isinstance(data["diametre_m"], (int, float)) or data["diametre_m"] <= 0:
        raise AEPValidationError("Le diamètre doit être un nombre positif")
    
    # Valider la longueur
    if not isinstance(data["longueur_m"], (int, float)) or data["longueur_m"] <= 0:
        raise AEPValidationError("La longueur doit être un nombre positif")
    
    # Valider l'épaisseur
    if not isinstance(data["epaisseur_mm"], (int, float)) or data["epaisseur_mm"] <= 0:
        raise AEPValidationError("L'épaisseur doit être un nombre positif")
    
    return data

def validate_aep_project_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide les données d'un projet AEP complet.
    
    Args:
        data: Dictionnaire contenant les données du projet
    
    Returns:
        Dictionnaire validé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    # Vérifier la présence des sections principales
    sections_requises = ["population", "demande", "reseau", "reservoir", "pompage"]
    
    for section in sections_requises:
        if section not in data:
            raise AEPValidationError(f"Section requise manquante: {section}")
        
        if not isinstance(data[section], dict):
            raise AEPValidationError(f"La section {section} doit être un dictionnaire")
    
    # Valider chaque section
    try:
        data["population"] = validate_population_data(data["population"])
        data["demande"] = validate_demand_data(data["demande"])
        data["reseau"] = validate_network_data(data["reseau"])
        data["reservoir"] = validate_reservoir_data(data["reservoir"])
        data["pompage"] = validate_pumping_data(data["pompage"])
    except AEPValidationError as e:
        raise AEPValidationError(f"Erreur de validation dans une section: {e}")
    
    return data

def check_physical_constraints(data: Dict[str, Any]) -> List[str]:
    """
    Vérifie les contraintes physiques des données AEP.
    
    Args:
        data: Dictionnaire contenant les données à vérifier
    
    Returns:
        Liste des avertissements
    """
    warnings = []
    
    # Vérifications de population
    if "population" in data:
        pop = data["population"]
        if isinstance(pop, (int, float)):
            if pop > 1000000:
                warnings.append("Population très élevée (> 1M), vérifiez les données")
            elif pop < 100:
                warnings.append("Population très faible (< 100), vérifiez les données")
    
    # Vérifications de débit
    if "debit_m3s" in data:
        debit = data["debit_m3s"]
        if isinstance(debit, (int, float)):
            if debit > 100:
                warnings.append("Débit très élevé (> 100 m³/s), vérifiez les données")
            elif debit < 0.001:
                warnings.append("Débit très faible (< 0.001 m³/s), vérifiez les données")
    
    # Vérifications de diamètre
    if "diametre_m" in data:
        diametre = data["diametre_m"]
        if isinstance(diametre, (int, float)):
            if diametre > 5:
                warnings.append("Diamètre très élevé (> 5 m), vérifiez les données")
            elif diametre < 0.01:
                warnings.append("Diamètre très faible (< 0.01 m), vérifiez les données")
    
    # Vérifications de HMT
    if "hmt_m" in data:
        hmt = data["hmt_m"]
        if isinstance(hmt, (int, float)):
            if hmt > 1000:
                warnings.append("HMT très élevée (> 1000 m), vérifiez les données")
            elif hmt < 1:
                warnings.append("HMT très faible (< 1 m), vérifiez les données")
    
    return warnings

def validate_and_clean_data(data: Dict[str, Any], data_type: str) -> Dict[str, Any]:
    """
    Valide et nettoie les données selon leur type.
    
    Args:
        data: Dictionnaire contenant les données
        data_type: Type de données ("population", "demande", "reseau", "reservoir", "pompage", "protection")
    
    Returns:
        Dictionnaire validé et nettoyé
    
    Raises:
        AEPValidationError: Si les données sont invalides
    """
    if not data:
        raise AEPValidationError("Aucune donnée fournie")
    
    # Sélectionner le validateur approprié
    validators = {
        "population": validate_population_data,
        "population_unified": validate_population_unified_data,
        "demande": validate_demand_data,
        "demand_unified": validate_demand_unified_data,
        "reseau": validate_network_data,
        "network_unified": validate_network_unified_data,
        "reservoir": validate_reservoir_data,
        "reservoir_unified": validate_reservoir_unified_data,
        "pompage": validate_pumping_data,
        "pumping_unified": validate_pumping_unified_data,
        "protection": validate_protection_data
    }
    
    if data_type not in validators:
        raise AEPValidationError(f"Type de données invalide: {data_type}")
    
    # Valider les données
    validated_data = validators[data_type](data)
    
    # Vérifier les contraintes physiques
    warnings = check_physical_constraints(validated_data)
    if warnings:
        print("⚠️ Avertissements de validation:")
        for warning in warnings:
            print(f"   - {warning}")
    
    return validated_data 