"""
Validateur et nettoyeur de fichiers INP pour éviter les warnings wntr.
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple


class INPValidator:
    """Valide et nettoie les fichiers INP pour éviter les warnings wntr."""
    
    def __init__(self, inp_file_path: Path):
        """Initialise le validateur avec un fichier INP."""
        self.inp_file_path = inp_file_path
        self.content = ""
        self.sections = {}
        self.issues = []
        
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
            elif current_section:
                current_lines.append(line)
        
        # Dernière section
        if current_section:
            self.sections[current_section] = current_lines
    
    def validate(self) -> List[str]:
        """Valide le fichier INP et retourne la liste des problèmes."""
        self.issues = []
        
        # Vérifier les courbes orphelines
        self._check_orphan_curves()
        
        # Vérifier les sections vides
        self._check_empty_sections()
        
        # Vérifier la cohérence des unités
        self._check_units_consistency()
        
        return self.issues
    
    def _check_orphan_curves(self):
        """Vérifie s'il y a des courbes définies mais non utilisées."""
        orphan_curves = self._get_orphan_curves()
        
        if orphan_curves:
            self.issues.append(
                f"Courbes orphelines détectées: {', '.join(orphan_curves)}. "
                "Ces courbes seront automatiquement ignorées lors de la simulation."
            )
    
    def _check_empty_sections(self):
        """Vérifie les sections vides qui peuvent causer des problèmes."""
        empty_sections = []
        
        for section_name, lines in self.sections.items():
            # Filtrer les lignes vides et commentaires
            non_empty_lines = [line for line in lines if line and not line.startswith(';')]
            
            if not non_empty_lines:
                empty_sections.append(section_name)
        
        if empty_sections:
            self.issues.append(
                f"Sections vides détectées: {', '.join(empty_sections)}. "
                "Ces sections peuvent causer des warnings wntr."
            )
    
    def _check_units_consistency(self):
        """Vérifie la cohérence des unités."""
        if 'OPTIONS' not in self.sections:
            return
        
        units_line = None
        for line in self.sections['OPTIONS']:
            if line.startswith('Units'):
                units_line = line
                break
        
        if units_line:
            units = units_line.split()[-1] if len(line.split()) > 1 else None
            if units and units not in ['LPS', 'LPM', 'LPS', 'MGD', 'IMGD', 'AFD', 'LPS']:
                self.issues.append(f"Unités non standard détectées: {units}")
    
    def fix_issues(self) -> bool:
        """Corrige automatiquement les problèmes détectés."""
        if not self.issues:
            return True
        
        try:
            # Sauvegarder l'original
            backup_path = self.inp_file_path.with_suffix('.inp.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(self.content)
            
            # Corriger les courbes orphelines
            if any('Courbes orphelines' in issue for issue in self.issues):
                self._fix_orphan_curves()
            
            # Sauvegarder le fichier corrigé
            with open(self.inp_file_path, 'w', encoding='utf-8') as f:
                f.write(self.content)
            
            return True
            
        except Exception as e:
            self.issues.append(f"Erreur lors de la correction: {e}")
            return False
    
    def _fix_orphan_curves(self):
        """Marque les courbes orphelines comme commentées pour les ignorer."""
        if 'CURVES' not in self.sections:
            return
        
        # Identifier les courbes orphelines
        orphan_curves = self._get_orphan_curves()
        
        if not orphan_curves:
            return
        
        # Commenter les courbes orphelines au lieu de les supprimer
        lines = self.content.split('\n')
        new_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # Si c'est une courbe orpheline, la commenter
            if line_stripped and not line_stripped.startswith(';'):
                parts = line_stripped.split()
                if len(parts) >= 1 and parts[0] in orphan_curves:
                    # Commenter la ligne en ajoutant ; au début
                    new_lines.append(f"; {line}  ; COURBE ORPHELINE - IGNORÉE")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        self.content = '\n'.join(new_lines)
        self._parse_sections()  # Re-parse après modification
    
    def _get_orphan_curves(self) -> Set[str]:
        """Retourne l'ensemble des courbes orphelines."""
        if 'CURVES' not in self.sections:
            return set()
        
        # Extraire les IDs de courbes
        curve_ids = set()
        for line in self.sections['CURVES']:
            if line and not line.startswith(';'):
                parts = line.split()
                if len(parts) >= 1:
                    curve_ids.add(parts[0])
        
        if not curve_ids:
            return set()
        
        # Vérifier l'utilisation dans PUMPS
        pumps_using_curves = set()
        if 'PUMPS' in self.sections:
            for line in self.sections['PUMPS']:
                if line and not line.startswith(';'):
                    parts = line.split()
                    if len(parts) >= 4:  # Format: ID Node1 Node2 Curve
                        pumps_using_curves.add(parts[3])
        
        # Vérifier l'utilisation dans VALVES
        valves_using_curves = set()
        if 'VALVES' in self.sections:
            for line in self.sections['VALVES']:
                if line and not line.startswith(';'):
                    parts = line.split()
                    if len(parts) >= 4:  # Format: ID Node1 Node2 Curve
                        valves_using_curves.add(parts[3])
        
        # Courbes orphelines
        return curve_ids - pumps_using_curves - valves_using_curves
    
    def get_summary(self) -> str:
        """Retourne un résumé de la validation."""
        if not self.issues:
            return "✅ Fichier INP valide - Aucun problème détecté"
        
        summary = f"⚠️ {len(self.issues)} problème(s) détecté(s):\n"
        for i, issue in enumerate(self.issues, 1):
            summary += f"  {i}. {issue}\n"
        
        return summary


def validate_inp_file(inp_file_path: Path) -> Tuple[bool, str]:
    """
    Valide un fichier INP et retourne (succès, message).
    
    Args:
        inp_file_path: Chemin vers le fichier INP
        
    Returns:
        Tuple (succès, message)
    """
    validator = INPValidator(inp_file_path)
    
    if not validator.load_and_parse():
        return False, "Impossible de charger le fichier INP"
    
    issues = validator.validate()
    
    if not issues:
        return True, validator.get_summary()
    
    # Essayer de corriger automatiquement
    if validator.fix_issues():
        return True, f"Problèmes corrigés automatiquement:\n{validator.get_summary()}"
    else:
        return False, f"Problèmes détectés mais impossible de les corriger:\n{validator.get_summary()}"
