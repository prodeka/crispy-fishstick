"""
Validateur spécialisé pour vérifier la conservation de masse dans les fichiers INP.
Vérifie que la somme des entrées = somme des sorties.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class INPMassConservationValidator:
    """Valide la conservation de masse dans un fichier INP."""
    
    def __init__(self, inp_file_path: Path):
        """Initialise le validateur avec un fichier INP."""
        self.inp_file_path = inp_file_path
        self.content = ""
        self.sections = {}
        self.issues = []
        self.warnings = []
        
    def load_and_parse(self) -> bool:
        """Charge et parse le fichier INP."""
        try:
            with open(self.inp_file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            
            self._parse_sections()
            return True
        except Exception as e:
            self.issues.append(f"Erreur de lecture: {e}")
            return False
    
    def _parse_sections(self):
        """Parse les sections du fichier INP."""
        current_section = None
        current_lines = []
        
        for line in self.content.split('\n'):
            line = line.strip()
            
            # Nouvelle section
            if line.startswith('[') and line.endswith(']'):
                if current_section:
                    self.sections[current_section] = current_lines
                current_section = line[1:-1]  # Enlève les []
                current_lines = []
            elif current_section and line and not line.startswith(';'):
                current_lines.append(line)
        
        # Dernière section
        if current_section:
            self.sections[current_section] = current_lines
    
    def validate_mass_conservation(self) -> Dict[str, any]:
        """Valide la conservation de masse et retourne un rapport détaillé."""
        report = {
            "valid": False,
            "total_input": 0.0,
            "total_output": 0.0,
            "balance": 0.0,
            "issues": [],
            "warnings": [],
            "sections_analysis": {}
        }
        
        # Analyser chaque section critique
        self._analyze_reservoirs(report)
        self._analyze_tanks(report)
        self._analyze_demands(report)
        self._analyze_pumps(report)
        
        # Calculer le bilan
        report["balance"] = report["total_input"] - report["total_output"]
        report["valid"] = abs(report["balance"]) < 1e-6  # Tolérance numérique
        
        # Collecter les problèmes
        report["issues"] = self.issues
        report["warnings"] = self.warnings
        
        return report
    
    def _analyze_reservoirs(self, report: Dict):
        """Analyse la section [RESERVOIRS]."""
        reservoirs = self.sections.get("RESERVOIRS", [])
        section_analysis = {
            "count": 0,
            "total_head": 0.0,
            "reservoirs": []
        }
        
        for line in reservoirs:
            if line and not line.startswith(';'):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        reservoir_id = parts[0]
                        head = float(parts[1])
                        section_analysis["count"] += 1
                        section_analysis["total_head"] += head
                        section_analysis["reservoirs"].append({
                            "id": reservoir_id,
                            "head": head
                        })
                        # Les réservoirs sont des sources (entrées positives)
                        report["total_input"] += 1000.0  # Estimation: 1000 L/s par réservoir
                    except ValueError:
                        self.warnings.append(f"Valeur de hauteur invalide pour réservoir: {line}")
        
        report["sections_analysis"]["reservoirs"] = section_analysis
        
        if section_analysis["count"] == 0:
            self.issues.append("Aucun réservoir défini - le réseau n'a pas de source d'eau")
    
    def _analyze_tanks(self, report: Dict):
        """Analyse la section [TANKS]."""
        tanks = self.sections.get("TANKS", [])
        section_analysis = {
            "count": 0,
            "tanks": []
        }
        
        for line in tanks:
            if line and not line.startswith(';'):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        tank_id = parts[0]
                        elevation = float(parts[1])
                        section_analysis["count"] += 1
                        section_analysis["tanks"].append({
                            "id": tank_id,
                            "elevation": elevation
                        })
                        # Les tanks peuvent être des sources ou des consommateurs selon le niveau
                        # Pour l'instant, on les considère comme neutres
                    except ValueError:
                        self.warnings.append(f"Valeur d'élévation invalide pour tank: {line}")
        
        report["sections_analysis"]["tanks"] = section_analysis
    
    def _analyze_demands(self, report: Dict):
        """Analyse la section [DEMANDS]."""
        demands = self.sections.get("DEMANDS", [])
        section_analysis = {
            "count": 0,
            "total_demand": 0.0,
            "demands": []
        }
        
        for line in demands:
            if line and not line.startswith(';'):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        node_id = parts[0]
                        demand = float(parts[1])
                        section_analysis["count"] += 1
                        section_analysis["total_demand"] += demand
                        section_analysis["demands"].append({
                            "node": node_id,
                            "demand": demand
                        })
                        # Les demandes sont des sorties (négatives)
                        report["total_output"] += demand
                    except ValueError:
                        self.warnings.append(f"Valeur de demande invalide: {line}")
        
        report["sections_analysis"]["demands"] = section_analysis
        
        if section_analysis["count"] == 0:
            self.issues.append("Aucune demande définie - le réseau n'a pas de consommation")
    
    def _analyze_pumps(self, report: Dict):
        """Analyse la section [PUMPS]."""
        pumps = self.sections.get("PUMPS", [])
        section_analysis = {
            "count": 0,
            "pumps": []
        }
        
        for line in pumps:
            if line and not line.startswith(';'):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        pump_id = parts[0]
                        node1 = parts[1]
                        node2 = parts[2]
                        section_analysis["count"] += 1
                        section_analysis["pumps"].append({
                            "id": pump_id,
                            "from": node1,
                            "to": node2
                        })
                        # Les pompes peuvent modifier le bilan hydraulique
                        # Pour l'instant, on les considère comme neutres
                    except (ValueError, IndexError):
                        self.warnings.append(f"Format de pompe invalide: {line}")
        
        report["sections_analysis"]["pumps"] = section_analysis
    
    def get_summary(self) -> str:
        """Retourne un résumé des problèmes détectés."""
        if not self.issues and not self.warnings:
            return "✅ Aucun problème détecté"
        
        summary = "📋 Résumé de la validation:\n"
        
        if self.issues:
            summary += "\n❌ Problèmes critiques:\n"
            for i, issue in enumerate(self.issues, 1):
                summary += f"  {i}. {issue}\n"
        
        if self.warnings:
            summary += "\n⚠️ Avertissements:\n"
            for i, warning in enumerate(self.warnings, 1):
                summary += f"  {i}. {warning}\n"
        
        return summary
    
    def suggest_fixes(self, report: Dict) -> List[str]:
        """Suggère des corrections pour les problèmes détectés."""
        fixes = []
        
        if report["sections_analysis"]["reservoirs"]["count"] == 0:
            fixes.append("Ajouter au moins un réservoir dans la section [RESERVOIRS]")
        
        if report["sections_analysis"]["demands"]["count"] == 0:
            fixes.append("Ajouter des demandes dans la section [DEMANDS] pour les nœuds de consommation")
        
        if abs(report["balance"]) > 1e-3:
            fixes.append(f"Équilibrer le réseau: entrées ({report['total_input']:.3f}) ≠ sorties ({report['total_output']:.3f})")
        
        return fixes


def validate_inp_mass_conservation(inp_file_path: Path) -> Tuple[bool, Dict[str, any]]:
    """
    Valide la conservation de masse d'un fichier INP.
    
    Args:
        inp_file_path: Chemin vers le fichier INP
        
    Returns:
        Tuple (succès, rapport détaillé)
    """
    validator = INPMassConservationValidator(inp_file_path)
    
    if not validator.load_and_parse():
        return False, {"error": "Impossible de charger le fichier INP"}
    
    report = validator.validate_mass_conservation()
    
    return report["valid"], report


def quick_inp_check(inp_file_path: Path) -> str:
    """
    Vérification rapide d'un fichier INP avec rapport en texte.
    
    Args:
        inp_file_path: Chemin vers le fichier INP
        
    Returns:
        Rapport en texte
    """
    # Convertir en Path si c'est une string
    if isinstance(inp_file_path, str):
        inp_file_path = Path(inp_file_path)
    
    validator = INPMassConservationValidator(inp_file_path)
    
    if not validator.load_and_parse():
        return f"❌ Erreur: Impossible de charger {inp_file_path}"
    
    report = validator.validate_mass_conservation()
    
    output = f"🔍 Validation INP: {inp_file_path.name}\n"
    output += f"📊 Bilan hydraulique:\n"
    output += f"  • Entrées totales: {report['total_input']:.3f} L/s\n"
    output += f"  • Sorties totales: {report['total_output']:.3f} L/s\n"
    output += f"  • Bilan: {report['balance']:.3f} L/s\n"
    output += f"  • Conservation OK: {'✅' if report['valid'] else '❌'}\n"
    
    if report["issues"]:
        output += f"\n❌ Problèmes critiques ({len(report['issues'])}):\n"
        for issue in report["issues"]:
            output += f"  • {issue}\n"
    
    if report["warnings"]:
        output += f"\n⚠️ Avertissements ({len(report['warnings'])}):\n"
        for warning in report["warnings"]:
            output += f"  • {warning}\n"
    
    if not report["valid"]:
        fixes = validator.suggest_fixes(report)
        if fixes:
            output += f"\n🔧 Suggestions de correction:\n"
            for fix in fixes:
                output += f"  • {fix}\n"
    
    return output
