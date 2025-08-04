"""
Module pour la transparence mathématique et les explications pédagogiques.
Fournit des fonctions pour afficher les formules, calculs étape par étape,
et explications détaillées pour tous les calculs AEP.
"""

import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class FormulaExplanation:
    """Structure pour expliquer une formule mathématique."""
    name: str
    formula: str
    variables: Dict[str, str]
    units: Dict[str, str]
    description: str
    example: Optional[Dict[str, float]] = None
    steps: Optional[List[str]] = None

class MathematicalTransparency:
    """
    Classe pour gérer la transparence mathématique et les explications pédagogiques.
    """
    
    def __init__(self):
        self.formulas = self._initialize_formulas()
    
    def _initialize_formulas(self) -> Dict[str, FormulaExplanation]:
        """Initialise toutes les formules avec leurs explications."""
        return {
            # Formules de population
            "population_arithmetique": FormulaExplanation(
                name="Progression Arithmétique",
                formula="P(t) = P₂ + k_u × (t - t₂)",
                variables={
                    "P(t)": "Population à l'année t",
                    "P₂": "Population au recensement 2",
                    "k_u": "Taux d'accroissement uniforme",
                    "t": "Année cible",
                    "t₂": "Année du recensement 2"
                },
                units={
                    "P(t)": "habitants",
                    "P₂": "habitants", 
                    "k_u": "habitants/an",
                    "t": "années",
                    "t₂": "années"
                },
                description="Croissance linéaire de la population avec un taux d'accroissement constant.",
                example={
                    "P₂": 100000,
                    "k_u": 800,
                    "t": 2025,
                    "t₂": 2010
                },
                steps=[
                    "Calcul du taux d'accroissement : k_u = (P₂ - P₁) / (t₂ - t₁)",
                    "Application de la formule : P(t) = P₂ + k_u × (t - t₂)",
                    "Résultat : Population estimée pour l'année cible"
                ]
            ),
            
            "population_geometrique": FormulaExplanation(
                name="Progression Géométrique",
                formula="P(t) = P₂ × (P₂/P₁)^((t-t₂)/(t₂-t₁))",
                variables={
                    "P(t)": "Population à l'année t",
                    "P₂": "Population au recensement 2",
                    "P₁": "Population au recensement 1",
                    "t": "Année cible",
                    "t₂": "Année du recensement 2",
                    "t₁": "Année du recensement 1"
                },
                units={
                    "P(t)": "habitants",
                    "P₂": "habitants",
                    "P₁": "habitants",
                    "t": "années",
                    "t₂": "années",
                    "t₁": "années"
                },
                description="Croissance exponentielle avec un taux de croissance constant en pourcentage.",
                example={
                    "P₂": 100000,
                    "P₁": 90000,
                    "t": 2025,
                    "t₂": 2010,
                    "t₁": 2000
                },
                steps=[
                    "Calcul du taux de croissance : r = (P₂/P₁)^(1/(t₂-t₁)) - 1",
                    "Application de la formule : P(t) = P₂ × (1+r)^(t-t₂)",
                    "Résultat : Population estimée pour l'année cible"
                ]
            ),
            
            "population_logistique": FormulaExplanation(
                name="Progression Logistique",
                formula="P(t) = K / (1 + 10^(a + b×t))",
                variables={
                    "P(t)": "Population à l'année t",
                    "K": "Population de saturation",
                    "a": "Paramètre de forme",
                    "b": "Taux de croissance",
                    "t": "Temps"
                },
                units={
                    "P(t)": "habitants",
                    "K": "habitants",
                    "a": "sans dimension",
                    "b": "1/an",
                    "t": "années"
                },
                description="Croissance en S avec une population de saturation.",
                example={
                    "K": 150000,
                    "a": -2.5,
                    "b": 0.1,
                    "t": 2025
                },
                steps=[
                    "Calcul des paramètres a et b à partir de 3 points",
                    "Application de la formule logistique",
                    "Résultat : Population estimée avec saturation"
                ]
            ),
            
            # Formules de demande d'eau
            "besoin_domestique": FormulaExplanation(
                name="Besoin Domestique",
                formula="Q_dom = P × d_dom × C_pointe",
                variables={
                    "Q_dom": "Débit domestique",
                    "P": "Population",
                    "d_dom": "Dotation domestique par habitant",
                    "C_pointe": "Coefficient de pointe"
                },
                units={
                    "Q_dom": "m³/jour",
                    "P": "habitants",
                    "d_dom": "L/habitant/jour",
                    "C_pointe": "sans dimension"
                },
                description="Calcul du débit domestique basé sur la population et la dotation.",
                example={
                    "P": 10000,
                    "d_dom": 150,
                    "C_pointe": 1.5
                },
                steps=[
                    "Conversion de la dotation : d_dom (L/hab/j) → d_dom (m³/hab/j)",
                    "Calcul du débit moyen : Q_moy = P × d_dom",
                    "Application du coefficient de pointe : Q_dom = Q_moy × C_pointe"
                ]
            ),
            
            "besoin_annexe": FormulaExplanation(
                name="Besoin Annexe",
                formula="Q_annexe = P × d_annexe × C_pointe",
                variables={
                    "Q_annexe": "Débit annexe",
                    "P": "Population",
                    "d_annexe": "Dotation annexe par habitant",
                    "C_pointe": "Coefficient de pointe"
                },
                units={
                    "Q_annexe": "m³/jour",
                    "P": "habitants",
                    "d_annexe": "L/habitant/jour",
                    "C_pointe": "sans dimension"
                },
                description="Calcul du débit pour usages annexes (industries, services, etc.).",
                example={
                    "P": 10000,
                    "d_annexe": 50,
                    "C_pointe": 1.2
                },
                steps=[
                    "Conversion de la dotation annexe",
                    "Calcul du débit annexe moyen",
                    "Application du coefficient de pointe"
                ]
            ),
            
            "besoin_global": FormulaExplanation(
                name="Besoin Global",
                formula="Q_global = Q_dom + Q_annexe + Q_incendie",
                variables={
                    "Q_global": "Débit global",
                    "Q_dom": "Débit domestique",
                    "Q_annexe": "Débit annexe",
                    "Q_incendie": "Débit incendie"
                },
                units={
                    "Q_global": "m³/jour",
                    "Q_dom": "m³/jour",
                    "Q_annexe": "m³/jour",
                    "Q_incendie": "m³/jour"
                },
                description="Somme de tous les besoins en eau.",
                example={
                    "Q_dom": 1500,
                    "Q_annexe": 500,
                    "Q_incendie": 200
                },
                steps=[
                    "Calcul des besoins domestiques",
                    "Calcul des besoins annexes",
                    "Ajout du débit d'incendie",
                    "Somme totale des besoins"
                ]
            ),
            
            # Formules hydrauliques
            "darcy_weisbach": FormulaExplanation(
                name="Perte de Charge Darcy-Weisbach",
                formula="Δh = λ × (L/D) × (V²/2g)",
                variables={
                    "Δh": "Perte de charge",
                    "λ": "Coefficient de friction",
                    "L": "Longueur de la conduite",
                    "D": "Diamètre de la conduite",
                    "V": "Vitesse d'écoulement",
                    "g": "Accélération de la pesanteur"
                },
                units={
                    "Δh": "m",
                    "λ": "sans dimension",
                    "L": "m",
                    "D": "m",
                    "V": "m/s",
                    "g": "m/s²"
                },
                description="Formule fondamentale pour calculer les pertes de charge linéaires.",
                example={
                    "λ": 0.02,
                    "L": 1000,
                    "D": 0.5,
                    "V": 2.0,
                    "g": 9.81
                },
                steps=[
                    "Calcul de la vitesse : V = Q / (π × D²/4)",
                    "Calcul du coefficient λ par Colebrook-White",
                    "Application de la formule Darcy-Weisbach",
                    "Résultat : Perte de charge en mètres"
                ]
            ),
            
            "manning_strickler": FormulaExplanation(
                name="Perte de Charge Manning-Strickler",
                formula="V = K_s × R_h^(2/3) × j^(1/2)",
                variables={
                    "V": "Vitesse d'écoulement",
                    "K_s": "Coefficient de Strickler",
                    "R_h": "Rayon hydraulique",
                    "j": "Pente hydraulique"
                },
                units={
                    "V": "m/s",
                    "K_s": "m^(1/3)/s",
                    "R_h": "m",
                    "j": "m/m"
                },
                description="Formule empirique pour calculer les pertes de charge.",
                example={
                    "K_s": 80,
                    "R_h": 0.125,
                    "j": 0.001
                },
                steps=[
                    "Calcul du rayon hydraulique : R_h = A/P",
                    "Calcul de la vitesse : V = K_s × R_h^(2/3) × j^(1/2)",
                    "Calcul de la perte de charge : Δh = j × L"
                ]
            ),
            
            "hazen_williams": FormulaExplanation(
                name="Perte de Charge Hazen-Williams",
                formula="Q = 0.2785 × C × D^2.63 × j^0.54",
                variables={
                    "Q": "Débit",
                    "C": "Coefficient de Hazen-Williams",
                    "D": "Diamètre",
                    "j": "Pente hydraulique"
                },
                units={
                    "Q": "m³/s",
                    "C": "sans dimension",
                    "D": "m",
                    "j": "m/m"
                },
                description="Formule empirique pour les conduites d'eau.",
                example={
                    "C": 100,
                    "D": 0.5,
                    "j": 0.001
                },
                steps=[
                    "Réarrangement pour j : j = (Q/(0.2785×C×D^2.63))^(1/0.54)",
                    "Calcul de la perte de charge : Δh = j × L"
                ]
            ),
            
            # Formules de réservoir
            "volume_utile": FormulaExplanation(
                name="Volume Utile du Réservoir",
                formula="V_u = V_max - V_min",
                variables={
                    "V_u": "Volume utile",
                    "V_max": "Volume maximum dans le réservoir",
                    "V_min": "Volume minimum dans le réservoir"
                },
                units={
                    "V_u": "m³",
                    "V_max": "m³",
                    "V_min": "m³"
                },
                description="Volume nécessaire pour équilibrer les variations de consommation.",
                example={
                    "V_max": 500,
                    "V_min": 100
                },
                steps=[
                    "Calcul du bilan hydraulique heure par heure",
                    "Détermination du volume maximum et minimum",
                    "Calcul du volume utile : V_u = V_max - V_min"
                ]
            ),
            
            "volume_incendie": FormulaExplanation(
                name="Volume d'Incendie",
                formula="V_inc = D × T",
                variables={
                    "V_inc": "Volume d'incendie",
                    "D": "Débit d'eau",
                    "T": "Temps de couverture"
                },
                units={
                    "V_inc": "litres",
                    "D": "litres/minute",
                    "T": "minutes"
                },
                description="Volume d'eau nécessaire pour la protection incendie.",
                example={
                    "D": 500,
                    "T": 30
                },
                steps=[
                    "Détermination du débit d'eau requis",
                    "Détermination du temps de couverture",
                    "Calcul du volume : V_inc = D × T"
                ]
            ),
            
            # Formules de pompage
            "puissance_hydraulique": FormulaExplanation(
                name="Puissance Hydraulique",
                formula="P_h = ρ × g × Q × H",
                variables={
                    "P_h": "Puissance hydraulique",
                    "ρ": "Masse volumique de l'eau",
                    "g": "Accélération de la pesanteur",
                    "Q": "Débit",
                    "H": "Hauteur manométrique totale"
                },
                units={
                    "P_h": "W",
                    "ρ": "kg/m³",
                    "g": "m/s²",
                    "Q": "m³/s",
                    "H": "m"
                },
                description="Puissance nécessaire pour élever l'eau d'une hauteur donnée.",
                example={
                    "ρ": 1000,
                    "g": 9.81,
                    "Q": 0.1,
                    "H": 50
                },
                steps=[
                    "Calcul de la puissance hydraulique : P_h = ρ × g × Q × H",
                    "Conversion en kW : P_h (kW) = P_h (W) / 1000"
                ]
            ),
            
            "puissance_electrique": FormulaExplanation(
                name="Puissance Électrique",
                formula="P_el = P_h / η",
                variables={
                    "P_el": "Puissance électrique",
                    "P_h": "Puissance hydraulique",
                    "η": "Rendement de la pompe"
                },
                units={
                    "P_el": "W",
                    "P_h": "W",
                    "η": "sans dimension"
                },
                description="Puissance électrique nécessaire pour entraîner la pompe.",
                example={
                    "P_h": 49050,
                    "η": 0.75
                },
                steps=[
                    "Calcul de la puissance hydraulique",
                    "Application du rendement : P_el = P_h / η",
                    "Résultat : Puissance électrique en W"
                ]
            ),
            
            # Formules de protection
            "celerite_ondes": FormulaExplanation(
                name="Célérité des Ondes",
                formula="c = √(K/ρ) / √(1 + (K×D)/(E×e))",
                variables={
                    "c": "Célérité des ondes",
                    "K": "Module de compressibilité de l'eau",
                    "ρ": "Masse volumique de l'eau",
                    "D": "Diamètre de la conduite",
                    "E": "Module d'élasticité du matériau",
                    "e": "Épaisseur de la paroi"
                },
                units={
                    "c": "m/s",
                    "K": "Pa",
                    "ρ": "kg/m³",
                    "D": "m",
                    "E": "Pa",
                    "e": "m"
                },
                description="Vitesse de propagation des ondes de pression dans une conduite.",
                example={
                    "K": 2.1e9,
                    "ρ": 1000,
                    "D": 0.5,
                    "E": 2.1e11,
                    "e": 0.01
                },
                steps=[
                    "Calcul du module de compressibilité effectif",
                    "Application de la formule de célérité",
                    "Résultat : Vitesse des ondes en m/s"
                ]
            ),
            
            "variation_pression": FormulaExplanation(
                name="Variation de Pression",
                formula="ΔP = ρ × c × ΔV",
                variables={
                    "ΔP": "Variation de pression",
                    "ρ": "Masse volumique de l'eau",
                    "c": "Célérité des ondes",
                    "ΔV": "Variation de vitesse"
                },
                units={
                    "ΔP": "Pa",
                    "ρ": "kg/m³",
                    "c": "m/s",
                    "ΔV": "m/s"
                },
                description="Variation de pression lors d'un coup de bélier.",
                example={
                    "ρ": 1000,
                    "c": 1200,
                    "ΔV": 2.0
                },
                steps=[
                    "Calcul de la célérité des ondes",
                    "Détermination de la variation de vitesse",
                    "Application de la formule : ΔP = ρ × c × ΔV"
                ]
            ),
            
            # Formules Hardy-Cross
            "hardy_cross_correction": FormulaExplanation(
                name="Correction Hardy-Cross",
                formula="ΔQ = -Σ(K×Q^n) / Σ(n×K×|Q|^(n-1))",
                variables={
                    "ΔQ": "Correction de débit",
                    "K": "Coefficient de résistance",
                    "Q": "Débit estimé",
                    "n": "Exposant de la formule"
                },
                units={
                    "ΔQ": "m³/s",
                    "K": "s²/m⁵",
                    "Q": "m³/s",
                    "n": "sans dimension"
                },
                description="Correction itérative pour équilibrer un réseau maillé.",
                example={
                    "K_values": [100, 150, 80],
                    "Q_values": [0.05, 0.03, -0.08],
                    "n": 1.85
                },
                steps=[
                    "Calcul du numérateur : Σ(K×Q^n)",
                    "Calcul du dénominateur : Σ(n×K×|Q|^(n-1))",
                    "Application de la correction : ΔQ = -numérateur/dénominateur"
                ]
            ),
            
            # Formules Flamant
            "flamant_perte_charge": FormulaExplanation(
                name="Perte de Charge Flamant",
                formula="j = 0.001404043 × Q^1.75 / D^4.75",
                variables={
                    "j": "Perte de charge unitaire",
                    "Q": "Débit",
                    "D": "Diamètre"
                },
                units={
                    "j": "m/m",
                    "Q": "m³/s",
                    "D": "m"
                },
                description="Formule empirique de Flamant pour les pertes de charge.",
                example={
                    "Q": 0.1,
                    "D": 0.5
                },
                steps=[
                    "Application de la formule de Flamant",
                    "Calcul de la perte de charge unitaire",
                    "Multiplication par la longueur pour obtenir la perte totale"
                ]
            ),
            
            "flamant_diametre": FormulaExplanation(
                name="Diamètre Flamant",
                formula="D = (0.001404043 × Q^1.75 / j)^(1/4.75)",
                variables={
                    "D": "Diamètre",
                    "Q": "Débit",
                    "j": "Perte de charge unitaire"
                },
                units={
                    "D": "m",
                    "Q": "m³/s",
                    "j": "m/m"
                },
                description="Calcul du diamètre par la formule de Flamant.",
                example={
                    "Q": 0.1,
                    "j": 0.001
                },
                steps=[
                    "Application de la formule inversée de Flamant",
                    "Calcul du diamètre théorique",
                    "Arrondi au diamètre commercial supérieur"
                ]
            )
        }
    
    def display_formula(self, formula_key: str, values: Optional[Dict[str, float]] = None) -> str:
        """
        Affiche une formule avec ses explications pédagogiques.
        
        Args:
            formula_key: Clé de la formule à afficher
            values: Valeurs numériques pour l'exemple de calcul
            
        Returns:
            str: Explication formatée en Markdown
        """
        if formula_key not in self.formulas:
            return f"❌ Formule '{formula_key}' non trouvée."
        
        formula = self.formulas[formula_key]
        
        # En-tête
        output = f"## {formula.name}\n\n"
        
        # Description
        output += f"**Description :** {formula.description}\n\n"
        
        # Formule mathématique
        output += "### Formule Mathématique\n\n"
        output += f"```\n{formula.formula}\n```\n\n"
        
        # Variables
        output += "### Variables\n\n"
        output += "| Variable | Description | Unité |\n"
        output += "|----------|-------------|-------|\n"
        for var, desc in formula.variables.items():
            unit = formula.units.get(var, "sans unité")
            output += f"| {var} | {desc} | {unit} |\n"
        output += "\n"
        
        # Étapes de calcul
        if formula.steps:
            output += "### Étapes de Calcul\n\n"
            for i, step in enumerate(formula.steps, 1):
                output += f"{i}. {step}\n"
            output += "\n"
        
        # Exemple de calcul
        if values and formula.example:
            output += "### Exemple de Calcul\n\n"
            output += "**Données :**\n"
            for var, val in values.items():
                unit = formula.units.get(var, "")
                output += f"- {var} = {val} {unit}\n"
            output += "\n"
            
            # Calcul étape par étape
            output += "**Calcul :**\n"
            if formula_key == "population_arithmetique":
                p2 = values.get("P₂", 100000)
                ku = values.get("k_u", 800)
                t = values.get("t", 2025)
                t2 = values.get("t₂", 2010)
                result = p2 + ku * (t - t2)
                output += f"P(t) = {p2} + {ku} × ({t} - {t2})\n"
                output += f"P(t) = {p2} + {ku} × {t - t2}\n"
                output += f"P(t) = {p2} + {ku * (t - t2)}\n"
                output += f"P(t) = {result:,.0f} habitants\n\n"
                
            elif formula_key == "population_geometrique":
                p2 = values.get("P₂", 100000)
                p1 = values.get("P₁", 90000)
                t = values.get("t", 2025)
                t2 = values.get("t₂", 2010)
                t1 = values.get("t₁", 2000)
                result = p2 * (p2/p1)**((t-t2)/(t2-t1))
                output += f"P(t) = {p2} × ({p2}/{p1})^(({t}-{t2})/({t2}-{t1}))\n"
                output += f"P(t) = {p2} × ({p2/p1:.3f})^({(t-t2)/(t2-t1):.3f})\n"
                output += f"P(t) = {result:,.0f} habitants\n\n"
                
            elif formula_key == "besoin_domestique":
                p = values.get("P", 10000)
                d_dom = values.get("d_dom", 150)
                c_pointe = values.get("C_pointe", 1.5)
                d_dom_m3 = d_dom / 1000  # Conversion L → m³
                q_moy = p * d_dom_m3
                q_dom = q_moy * c_pointe
                output += f"Q_dom = {p} × {d_dom} L/hab/j × {c_pointe}\n"
                output += f"Q_dom = {p} × {d_dom_m3:.3f} m³/hab/j × {c_pointe}\n"
                output += f"Q_dom = {q_moy:.1f} m³/j × {c_pointe}\n"
                output += f"Q_dom = {q_dom:.1f} m³/j\n\n"
                
            elif formula_key == "darcy_weisbach":
                lambda_val = values.get("λ", 0.02)
                l = values.get("L", 1000)
                d = values.get("D", 0.5)
                v = values.get("V", 2.0)
                g = values.get("g", 9.81)
                delta_h = lambda_val * (l/d) * (v**2 / (2*g))
                output += f"Δh = {lambda_val} × ({l}/{d}) × ({v}²/(2×{g}))\n"
                output += f"Δh = {lambda_val} × {l/d:.1f} × {v**2/(2*g):.3f}\n"
                output += f"Δh = {delta_h:.3f} m\n\n"
                
            elif formula_key == "puissance_hydraulique":
                rho = values.get("ρ", 1000)
                g = values.get("g", 9.81)
                q = values.get("Q", 0.1)
                h = values.get("H", 50)
                p_h = rho * g * q * h
                output += f"P_h = {rho} × {g} × {q} × {h}\n"
                output += f"P_h = {p_h:.1f} W\n"
                output += f"P_h = {p_h/1000:.2f} kW\n\n"
                
            elif formula_key == "volume_incendie":
                d = values.get("D", 500)
                t = values.get("T", 30)
                result = d * t
                output += f"V_inc = {d} × {t}\n"
                output += f"V_inc = {result} litres\n\n"
                
            elif formula_key == "flamant_perte_charge":
                q = values.get("Q", 0.1)
                d = values.get("D", 0.5)
                j = 0.001404043 * (q**1.75) / (d**4.75)
                output += f"j = 0.001404043 × {q}^1.75 / {d}^4.75\n"
                output += f"j = {j:.6f} m/m\n\n"
            
            output += f"**Résultat :** {result if 'result' in locals() else 'Calculé selon la formule'}\n\n"
        
        return output
    
    def display_calculation_steps(self, calculation_name: str, steps: List[Dict[str, Any]]) -> str:
        """
        Affiche les étapes d'un calcul complexe.
        
        Args:
            calculation_name: Nom du calcul
            steps: Liste des étapes avec formules et résultats
            
        Returns:
            str: Affichage formaté des étapes
        """
        output = f"## Calcul : {calculation_name}\n\n"
        
        for i, step in enumerate(steps, 1):
            output += f"### Étape {i}: {step.get('title', f'Étape {i}')}\n\n"
            
            if 'formula' in step:
                output += f"**Formule :** {step['formula']}\n\n"
            
            if 'variables' in step:
                output += "**Variables :**\n"
                for var, val in step['variables'].items():
                    output += f"- {var} = {val}\n"
                output += "\n"
            
            if 'calculation' in step:
                output += f"**Calcul :** {step['calculation']}\n\n"
            
            if 'result' in step:
                output += f"**Résultat :** {step['result']}\n\n"
            
            if 'explanation' in step:
                output += f"**Explication :** {step['explanation']}\n\n"
        
        return output
    
    def create_mathematical_report(self, title: str, calculations: List[Dict[str, Any]]) -> str:
        """
        Crée un rapport mathématique complet avec transparence.
        
        Args:
            title: Titre du rapport
            calculations: Liste des calculs à inclure
            
        Returns:
            str: Rapport complet en Markdown
        """
        output = f"# Rapport de Calcul : {title}\n\n"
        output += "## Introduction\n\n"
        output += "Ce rapport présente les calculs effectués avec transparence mathématique complète.\n"
        output += "Chaque formule est expliquée et illustrée par des exemples numériques.\n\n"
        
        for calc in calculations:
            if calc['type'] == 'formula':
                output += self.display_formula(calc['key'], calc.get('values'))
            elif calc['type'] == 'steps':
                output += self.display_calculation_steps(calc['name'], calc['steps'])
            elif calc['type'] == 'text':
                output += f"## {calc['title']}\n\n{calc['content']}\n\n"
        
        output += "## Conclusion\n\n"
        output += "Tous les calculs ont été effectués selon les formules et méthodes reconnues.\n"
        output += "Les résultats sont présentés avec transparence pour faciliter la vérification.\n\n"
        
        return output

# Instance globale pour utilisation dans les autres modules
math_transparency = MathematicalTransparency() 