"""
Templates spécifiques par plugin pour la génération de rapports

Ce module contient les templates et formules mathématiques
spécifiques à chaque plugin pour la génération de rapports.
"""

from typing import Dict, List, Any
from pathlib import Path

class PluginTemplates:
    """Templates et formules spécifiques par plugin"""
    
    @staticmethod
    def get_aep_templates() -> Dict[str, Any]:
        """Templates et formules pour le plugin AEP"""
        return {
            "title": "Rapport AEP - Alimentation en Eau Potable",
            "description": "Calculs d'alimentation en eau potable avec transparence mathématique",
            "sections": [
                {
                    "name": "projection_population",
                    "title": "Projection Démographique",
                    "formulas": [
                        {
                            "name": "malthus",
                            "latex": "P(t) = P_0 \\times (1 + r)^t",
                            "description": "Formule de Malthus pour la projection démographique",
                            "variables": {
                                "P(t)": "Population à l'année t",
                                "P_0": "Population initiale",
                                "r": "Taux de croissance annuel",
                                "t": "Nombre d'années"
                            }
                        }
                    ]
                },
                {
                    "name": "demande_eau",
                    "title": "Calcul des Besoins en Eau",
                    "formulas": [
                        {
                            "name": "besoin_brut",
                            "latex": "Q_{brut} = \\frac{P \\times D \\times C_p}{\\eta_t}",
                            "description": "Calcul du besoin brut en eau",
                            "variables": {
                                "Q_{brut}": "Besoin brut en m³/j",
                                "P": "Population",
                                "D": "Dotation en L/hab/j",
                                "C_p": "Coefficient de pointe",
                                "\\eta_t": "Rendement technique"
                            }
                        }
                    ]
                },
                {
                    "name": "dimensionnement_reseau",
                    "title": "Dimensionnement Réseau",
                    "formulas": [
                        {
                            "name": "darcy_weisbach",
                            "latex": "h_f = \\frac{f \\times L \\times V^2}{2 \\times g \\times D}",
                            "description": "Formule de Darcy-Weisbach",
                            "variables": {
                                "h_f": "Perte de charge (m)",
                                "f": "Coefficient de frottement",
                                "L": "Longueur de conduite (m)",
                                "V": "Vitesse (m/s)",
                                "g": "Accélération gravitationnelle (m/s²)",
                                "D": "Diamètre (m)"
                            }
                        },
                        {
                            "name": "manning_strickler",
                            "latex": "V = K_s \\times R^{2/3} \\times S^{1/2}",
                            "description": "Formule de Manning-Strickler",
                            "variables": {
                                "V": "Vitesse (m/s)",
                                "K_s": "Coefficient de Strickler",
                                "R": "Rayon hydraulique (m)",
                                "S": "Pente de la conduite"
                            }
                        }
                    ]
                },
                {
                    "name": "dimensionnement_reservoir",
                    "title": "Dimensionnement Réservoir",
                    "formulas": [
                        {
                            "name": "volume_utile",
                            "latex": "V_{utile} = V_{max} - V_{min}",
                            "description": "Volume utile par bilan hydraulique",
                            "variables": {
                                "V_{utile}": "Volume utile (m³)",
                                "V_{max}": "Volume maximum (m³)",
                                "V_{min}": "Volume minimum (m³)"
                            }
                        }
                    ]
                },
                {
                    "name": "dimensionnement_pompage",
                    "title": "Dimensionnement Pompage",
                    "formulas": [
                        {
                            "name": "puissance_hydraulique",
                            "latex": "P_h = \\rho \\times g \\times Q \\times H",
                            "description": "Puissance hydraulique",
                            "variables": {
                                "P_h": "Puissance hydraulique (W)",
                                "\\rho": "Masse volumique de l'eau (kg/m³)",
                                "g": "Accélération gravitationnelle (m/s²)",
                                "Q": "Débit (m³/s)",
                                "H": "Hauteur manométrique (m)"
                            }
                        },
                        {
                            "name": "puissance_electrique",
                            "latex": "P_e = \\frac{P_h}{\\eta}",
                            "description": "Puissance électrique",
                            "variables": {
                                "P_e": "Puissance électrique (W)",
                                "P_h": "Puissance hydraulique (W)",
                                "\\eta": "Rendement de la pompe"
                            }
                        }
                    ]
                }
            ]
        }
    
    @staticmethod
    def get_cm_templates() -> Dict[str, Any]:
        """Templates et formules pour le plugin CM (Construction Métallique)"""
        return {
            "title": "Rapport CM - Construction Métallique",
            "description": "Calculs de construction métallique selon Eurocode 3",
            "sections": [
                {
                    "name": "verification_section",
                    "title": "Vérification des Sections",
                    "formulas": [
                        {
                            "name": "resistance_plastique",
                            "latex": "N_{pl,Rd} = \\frac{A \\times f_y}{\\gamma_{M0}}",
                            "description": "Résistance plastique en compression",
                            "variables": {
                                "N_{pl,Rd}": "Résistance plastique (N)",
                                "A": "Aire de la section (mm²)",
                                "f_y": "Limite d'élasticité (MPa)",
                                "\\gamma_{M0}": "Coefficient de sécurité partiel"
                            }
                        }
                    ]
                },
                {
                    "name": "verification_flambement",
                    "title": "Vérification au Flambement",
                    "formulas": [
                        {
                            "name": "charge_critique_euler",
                            "latex": "N_{cr} = \\frac{\\pi^2 \\times E \\times I}{L_{cr}^2}",
                            "description": "Charge critique d'Euler",
                            "variables": {
                                "N_{cr}": "Charge critique (N)",
                                "E": "Module d'Young (MPa)",
                                "I": "Inertie (mm⁴)",
                                "L_{cr}": "Longueur de flambement (mm)"
                            }
                        }
                    ]
                }
            ]
        }
    
    @staticmethod
    def get_bois_templates() -> Dict[str, Any]:
        """Templates et formules pour le plugin Bois"""
        return {
            "title": "Rapport Bois - Structures en Bois",
            "description": "Calculs de structures en bois selon Eurocode 5",
            "sections": [
                {
                    "name": "verification_flexion",
                    "title": "Vérification en Flexion",
                    "formulas": [
                        {
                            "name": "contrainte_flexion",
                            "latex": "\\sigma_{m,d} = \\frac{M_d}{W_{el}}",
                            "description": "Contrainte de flexion",
                            "variables": {
                                "\\sigma_{m,d}": "Contrainte de flexion (MPa)",
                                "M_d": "Moment de flexion (N.mm)",
                                "W_{el}": "Module de flexion élastique (mm³)"
                            }
                        }
                    ]
                },
                {
                    "name": "verification_cisaillement",
                    "title": "Vérification au Cisaillement",
                    "formulas": [
                        {
                            "name": "contrainte_cisaillement",
                            "latex": "\\tau_d = \\frac{V_d \\times S}{I \\times b}",
                            "description": "Contrainte de cisaillement",
                            "variables": {
                                "\\tau_d": "Contrainte de cisaillement (MPa)",
                                "V_d": "Effort tranchant (N)",
                                "S": "Moment statique (mm³)",
                                "I": "Inertie (mm⁴)",
                                "b": "Largeur (mm)"
                            }
                        }
                    ]
                }
            ]
        }
    
    @staticmethod
    def get_beton_templates() -> Dict[str, Any]:
        """Templates et formules pour le plugin Béton"""
        return {
            "title": "Rapport Béton - Béton Armé",
            "description": "Calculs de béton armé selon Eurocode 2",
            "sections": [
                {
                    "name": "verification_flexion",
                    "title": "Vérification en Flexion",
                    "formulas": [
                        {
                            "name": "moment_resistant",
                            "latex": "M_{Rd} = A_s \\times f_{yd} \\times (d - \\frac{x}{2})",
                            "description": "Moment résistant",
                            "variables": {
                                "M_{Rd}": "Moment résistant (N.mm)",
                                "A_s": "Aire d'armature (mm²)",
                                "f_{yd}": "Limite d'élasticité de l'acier (MPa)",
                                "d": "Hauteur utile (mm)",
                                "x": "Hauteur de la zone comprimée (mm)"
                            }
                        }
                    ]
                },
                {
                    "name": "verification_cisaillement",
                    "title": "Vérification au Cisaillement",
                    "formulas": [
                        {
                            "name": "resistance_cisaillement",
                            "latex": "V_{Rd} = V_{Rd,c} + V_{Rd,s}",
                            "description": "Résistance au cisaillement",
                            "variables": {
                                "V_{Rd}": "Résistance au cisaillement (N)",
                                "V_{Rd,c}": "Résistance du béton (N)",
                                "V_{Rd,s}": "Résistance des armatures (N)"
                            }
                        }
                    ]
                }
            ]
        }
    
    @staticmethod
    def get_hydrodrain_templates() -> Dict[str, Any]:
        """Templates et formules pour le plugin Hydrodrain"""
        return {
            "title": "Rapport Hydrodrain - Hydrologie et Hydraulique",
            "description": "Calculs hydrologiques et hydrauliques",
            "sections": [
                {
                    "name": "bassin_versant",
                    "title": "Calculs de Bassin Versant",
                    "formulas": [
                        {
                            "name": "debit_pluie",
                            "latex": "Q = C \\times i \\times A",
                            "description": "Débit de pointe par méthode rationnelle",
                            "variables": {
                                "Q": "Débit de pointe (m³/s)",
                                "C": "Coefficient de ruissellement",
                                "i": "Intensité de pluie (mm/h)",
                                "A": "Surface du bassin versant (ha)"
                            }
                        }
                    ]
                },
                {
                    "name": "canaux",
                    "title": "Dimensionnement des Canaux",
                    "formulas": [
                        {
                            "name": "debit_manning",
                            "latex": "Q = \\frac{1}{n} \\times A \\times R^{2/3} \\times S^{1/2}",
                            "description": "Formule de Manning pour les canaux",
                            "variables": {
                                "Q": "Débit (m³/s)",
                                "n": "Coefficient de Manning",
                                "A": "Section mouillée (m²)",
                                "R": "Rayon hydraulique (m)",
                                "S": "Pente du canal"
                            }
                        }
                    ]
                }
            ]
        }
    
    @staticmethod
    def get_all_templates() -> Dict[str, Dict[str, Any]]:
        """Retourne tous les templates par plugin"""
        return {
            "aep": PluginTemplates.get_aep_templates(),
            "cm": PluginTemplates.get_cm_templates(),
            "bois": PluginTemplates.get_bois_templates(),
            "beton": PluginTemplates.get_beton_templates(),
            "hydrodrain": PluginTemplates.get_hydrodrain_templates()
        }

def generate_plugin_report_content(plugin_name: str, data: Dict[str, Any]) -> str:
    """
    Génère le contenu Markdown spécifique à un plugin.
    
    Args:
        plugin_name: Nom du plugin (aep, cm, bois, beton, hydrodrain)
        data: Données du plugin
        
    Returns:
        str: Contenu Markdown formaté
    """
    templates = PluginTemplates.get_all_templates()
    
    if plugin_name not in templates:
        return f"## Plugin {plugin_name.upper()}\n\nAucun template disponible pour ce plugin.\n"
    
    template = templates[plugin_name]
    content = []
    
    # En-tête du plugin
    content.append(f"# {template['title']}")
    content.append("")
    content.append(f"**Description:** {template['description']}")
    content.append("")
    
    # Sections avec formules
    for section in template['sections']:
        content.append(f"## {section['title']}")
        content.append("")
        
        for formula in section['formulas']:
            content.append(f"### {formula['name'].replace('_', ' ').title()}")
            content.append("")
            content.append(f"**Formule:**")
            content.append("")
            content.append(f"$${formula['latex']}$$")
            content.append("")
            content.append(f"**Description:** {formula['description']}")
            content.append("")
            content.append("**Variables:**")
            content.append("")
            for var, desc in formula['variables'].items():
                content.append(f"- ${var}$ : {desc}")
            content.append("")
    
    return "\n".join(content) 