#!/usr/bin/env python3
"""
Système de rapports globaux avec support Pandoc
"""

import os
import json
import yaml
import subprocess
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class GlobalReportGenerator:
    """Générateur de rapports globaux avec support Pandoc"""
    
    def __init__(self, output_dir: str = "output/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.pandoc_available = self._check_pandoc()
        
    def _check_pandoc(self) -> bool:
        """Vérifie si Pandoc est disponible"""
        try:
            result = subprocess.run(['pandoc', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def generate_markdown_report(self, data: Dict[str, Any], 
                               template: str = "default") -> str:
        """Génère un rapport en Markdown"""
        
        if template == "default":
            return self._generate_default_markdown(data)
        elif template == "enhanced":
            return self._generate_enhanced_markdown(data)
        else:
            return self._generate_custom_markdown(data, template)
    
    def _generate_default_markdown(self, data: Dict[str, Any]) -> str:
        """Génère un rapport Markdown par défaut"""
        
        report = f"""# Rapport LCPI - {data.get('type', 'Calcul')}

## 📊 Informations Générales
- **Date** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Type** : {data.get('type', 'N/A')}
- **Module** : {data.get('module', 'N/A')}

## 📋 Données d'Entrée
"""
        
        # Données d'entrée
        if 'input_data' in data:
            report += "```yaml\n"
            report += yaml.dump(data['input_data'], default_flow_style=False, 
                              allow_unicode=True)
            report += "```\n\n"
        
        # Résultats
        report += "## 🎯 Résultats\n"
        if 'results' in data:
            report += "```json\n"
            report += json.dumps(data['results'], indent=2, ensure_ascii=False)
            report += "```\n\n"
        
        # Formules utilisées
        if 'formulas' in data:
            report += "## 📐 Formules Utilisées\n"
            for formula in data['formulas']:
                report += f"### {formula.get('name', 'Formule')}\n"
                report += f"**Équation** : `{formula.get('equation', 'N/A')}`\n\n"
                if 'variables' in formula:
                    report += "**Variables** :\n"
                    for var, desc in formula['variables'].items():
                        report += f"- `{var}` : {desc}\n"
                report += "\n"
        
        # Vérifications
        if 'verifications' in data:
            report += "## ✅ Vérifications\n"
            for check in data['verifications']:
                status = "✅" if check.get('passed', False) else "❌"
                report += f"{status} **{check.get('name', 'Vérification')}** : {check.get('message', 'N/A')}\n"
            report += "\n"
        
        # Graphiques (si disponibles)
        if 'plots' in data:
            report += "## 📈 Graphiques\n"
            for plot in data['plots']:
                report += f"![{plot.get('title', 'Graphique')}]({plot.get('path', '')})\n\n"
        
        report += "---\n*Rapport généré automatiquement par LCPI*"
        
        return report
    
    def _generate_enhanced_markdown(self, data: Dict[str, Any]) -> str:
        """Génère un rapport Markdown amélioré"""
        
        report = f"""# 🚀 Rapport LCPI Avancé - {data.get('type', 'Calcul')}

<div align="center">

![LCPI Logo](https://img.shields.io/badge/LCPI-Engineering-blue?style=for-the-badge&logo=python)

**Plateforme de Calcul Polyvalent pour l'Ingénierie**

</div>

---

## 📊 Informations Générales

| Propriété | Valeur |
|-----------|--------|
| **Date** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| **Type** | {data.get('type', 'N/A')} |
| **Module** | {data.get('module', 'N/A')} |
| **Version** | {data.get('version', '2.1.0')} |

## 📋 Données d'Entrée

<details>
<summary>🔍 Voir les données d'entrée</summary>

```yaml
{yaml.dump(data.get('input_data', {}), default_flow_style=False, allow_unicode=True)}
```

</details>

## 🎯 Résultats

<details>
<summary>📊 Voir les résultats détaillés</summary>

```json
{json.dumps(data.get('results', {}), indent=2, ensure_ascii=False)}
```

</details>

## 📐 Formules Utilisées

"""
        
        # Formules avec mise en forme améliorée
        if 'formulas' in data:
            for i, formula in enumerate(data['formulas'], 1):
                report += f"### {i}. {formula.get('name', 'Formule')}\n\n"
                report += f"**Équation** :\n```\n{formula.get('equation', 'N/A')}\n```\n\n"
                
                if 'variables' in formula:
                    report += "**Variables** :\n\n"
                    report += "| Variable | Description |\n"
                    report += "|----------|-------------|\n"
                    for var, desc in formula['variables'].items():
                        report += f"| `{var}` | {desc} |\n"
                    report += "\n"
                
                if 'units' in formula:
                    report += "**Unités** :\n"
                    for var, unit in formula['units'].items():
                        report += f"- `{var}` : {unit}\n"
                    report += "\n"
        
        # Vérifications avec badges
        if 'verifications' in data:
            report += "## ✅ Vérifications\n\n"
            for check in data['verifications']:
                status = "🟢" if check.get('passed', False) else "🔴"
                report += f"{status} **{check.get('name', 'Vérification')}**\n"
                report += f"*{check.get('message', 'N/A')}*\n\n"
        
        # Graphiques
        if 'plots' in data:
            report += "## 📈 Graphiques\n\n"
            for plot in data['plots']:
                report += f"### {plot.get('title', 'Graphique')}\n"
                report += f"![{plot.get('title', 'Graphique')}]({plot.get('path', '')})\n\n"
        
        # Métriques de performance
        if 'performance' in data:
            report += "## ⚡ Métriques de Performance\n\n"
            perf = data['performance']
            report += f"- **Temps de calcul** : {perf.get('calculation_time', 'N/A')} s\n"
            report += f"- **Mémoire utilisée** : {perf.get('memory_used', 'N/A')} MB\n"
            report += f"- **Itérations** : {perf.get('iterations', 'N/A')}\n\n"
        
        report += """---

<div align="center">

**📅 Généré le """ + datetime.now().strftime('%Y-%m-%d à %H:%M:%S') + """**

**🔧 LCPI Engineering Platform**

</div>"""
        
        return report
    
    def _generate_custom_markdown(self, data: Dict[str, Any], template: str) -> str:
        """Génère un rapport Markdown personnalisé"""
        # Implémentation pour templates personnalisés
        return self._generate_default_markdown(data)
    
    def convert_to_html(self, markdown_content: str, output_file: str) -> bool:
        """Convertit le Markdown en HTML avec Pandoc"""
        if not self.pandoc_available:
            console.print("⚠️ Pandoc non disponible, conversion HTML impossible")
            return False
        
        try:
            # Créer un fichier temporaire Markdown
            temp_md = self.output_dir / "temp_report.md"
            with open(temp_md, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Convertir avec Pandoc
            cmd = [
                'pandoc',
                str(temp_md),
                '-o', output_file,
                '--standalone',
                '--css', 'style.css',
                '--metadata', 'title=LCPI Report'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Nettoyer le fichier temporaire
            temp_md.unlink()
            
            return result.returncode == 0
            
        except Exception as e:
            console.print(f"❌ Erreur lors de la conversion HTML : {e}")
            return False
    
    def convert_to_pdf(self, markdown_content: str, output_file: str) -> bool:
        """Convertit le Markdown en PDF avec Pandoc"""
        if not self.pandoc_available:
            console.print("⚠️ Pandoc non disponible, conversion PDF impossible")
            return False
        
        try:
            # Créer un fichier temporaire Markdown
            temp_md = self.output_dir / "temp_report.md"
            with open(temp_md, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Convertir avec Pandoc
            cmd = [
                'pandoc',
                str(temp_md),
                '-o', output_file,
                '--pdf-engine=xelatex',
                '--variable', 'geometry:margin=1in',
                '--variable', 'fontsize=11pt'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Nettoyer le fichier temporaire
            temp_md.unlink()
            
            return result.returncode == 0
            
        except Exception as e:
            console.print(f"❌ Erreur lors de la conversion PDF : {e}")
            return False
    
    def generate_complete_report(self, data: Dict[str, Any], 
                               formats: List[str] = ['md', 'html', 'pdf'],
                               template: str = "enhanced") -> Dict[str, str]:
        """Génère un rapport complet dans plusieurs formats"""
        
        results = {}
        
        # Générer le Markdown
        markdown_content = self.generate_markdown_report(data, template)
        
        # Sauvegarder le Markdown
        md_file = self.output_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        results['markdown'] = str(md_file)
        
        # Convertir en autres formats
        if 'html' in formats:
            html_file = md_file.with_suffix('.html')
            if self.convert_to_html(markdown_content, str(html_file)):
                results['html'] = str(html_file)
        
        if 'pdf' in formats:
            pdf_file = md_file.with_suffix('.pdf')
            if self.convert_to_pdf(markdown_content, str(pdf_file)):
                results['pdf'] = str(pdf_file)
        
        return results

# Interface pour CLI
def generate_global_report(data: Dict[str, Any], 
                         output_dir: str = "output/reports",
                         formats: List[str] = ['md', 'html'],
                         template: str = "enhanced") -> Dict[str, str]:
    """Interface pour générer des rapports globaux"""
    
    generator = GlobalReportGenerator(output_dir)
    return generator.generate_complete_report(data, formats, template)

def check_pandoc_availability() -> bool:
    """Vérifie la disponibilité de Pandoc"""
    generator = GlobalReportGenerator()
    return generator.pandoc_available 