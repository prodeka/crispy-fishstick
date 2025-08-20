"""
Générateur de rapports PDF pour l'optimisation de réseau.
Utilise le composant PDF existant du projet.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from .utils.pdf_generator import export_to_pdf


class PDFGenerator:
    """Génère des rapports d'optimisation au format PDF."""
    
    def __init__(self):
        """Initialise le générateur PDF."""
        pass
    
    def generate_optimization_report(self, index_data: dict, outputs: dict) -> bytes:
        """
        Génère un rapport d'optimisation complet au format PDF.
        
        Args:
            index_data: Données d'index multi-solveurs
            outputs: Résultats d'optimisation par solveur
            
        Returns:
            Contenu PDF du rapport en bytes
        """
        # Générer d'abord le contenu HTML
        html_content = self._generate_html_content(index_data, outputs)
        
        # Essayer d'abord WeasyPrint
        try:
            return self._generate_with_weasyprint(html_content)
        except Exception as e:
            print(f"WeasyPrint non disponible - export PDF impossible")
            print(f"⚠️  Export PDF non disponible")
            print(f"🔍 Raison: {e}")
            print()
            print("💡 Solutions pour Windows:")
            print("   1. Installer GTK+ Runtime Environment:")
            print("      https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer")
            print("   2. Ou utiliser une alternative comme wkhtmltopdf")
            print("   3. Ou générer en HTML et convertir manuellement")
            print()
            print("📋 Alternatives disponibles : HTML, JSON, YAML, CSV, DOCX")
            
            # Fallback vers le composant PDF existant
            try:
                return self._generate_with_existing_pdf(html_content)
            except Exception:
                # En dernier recours, retourner un PDF d'erreur
                return self._generate_error_pdf()
    
    def _generate_with_weasyprint(self, html_content: str) -> bytes:
        """Génère un PDF avec WeasyPrint."""
        try:
            import weasyprint
            from weasyprint import HTML, CSS
            
            # Créer le PDF
            html_doc = HTML(string=html_content)
            pdf_bytes = html_doc.write_pdf()
            return pdf_bytes
            
        except ImportError:
            raise Exception("WeasyPrint non installé")
        except Exception as e:
            raise Exception(f"Erreur WeasyPrint: {e}")
    
    def _generate_with_existing_pdf(self, html_content: str) -> bytes:
        """Génère un PDF avec le composant existant."""
        try:
            # Convertir en PDF en utilisant le composant existant
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                tmp_path = Path(tmp_file.name)
            
            try:
                # Utiliser le composant PDF existant
                success = export_to_pdf(
                    html_content=html_content,
                    output_path=tmp_path,
                    base_url=Path(__file__).parent / "templates"
                )
                
                if success:
                    # Lire le contenu du fichier PDF temporaire
                    with open(tmp_path, 'rb') as f:
                        pdf_content = f.read()
                    
                    # Nettoyer le fichier temporaire
                    os.unlink(tmp_path)
                    
                    return pdf_content
                else:
                    # En cas d'échec, retourner un PDF d'erreur simple
                    return self._generate_error_pdf()
                    
            except Exception as e:
                # Nettoyer en cas d'erreur
                if tmp_path.exists():
                    os.unlink(tmp_path)
                
                # Retourner un PDF d'erreur
                return self._generate_error_pdf()
                
        except Exception as e:
            raise Exception(f"Erreur composant PDF existant: {e}")
    
    def _generate_html_content(self, index_data: dict, outputs: dict) -> str:
        """Génère le contenu HTML pour la conversion PDF."""
        html_lines = []
        
        # En-tête HTML
        html_lines.extend([
            '<!DOCTYPE html>',
            '<html lang="fr">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '    <title>Rapport d\'Optimisation de Réseau</title>',
            '    <style>',
            '        body { font-family: Arial, sans-serif; margin: 20px; }',
            '        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }',
            '        h2 { color: #34495e; margin-top: 30px; }',
            '        h3 { color: #7f8c8d; }',
            '        .summary { background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }',
            '        .solver-section { margin: 30px 0; padding: 20px; border: 1px solid #bdc3c7; border-radius: 5px; }',
            '        .proposal { margin: 15px 0; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #3498db; }',
            '        .comparison-table { width: 100%; border-collapse: collapse; margin: 20px 0; }',
            '        .comparison-table th, .comparison-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }',
            '        .comparison-table th { background-color: #f2f2f2; }',
            '        .success { color: #27ae60; }',
            '        .error { color: #e74c3c; }',
            '        .info { color: #3498db; }',
            '        .footer { margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #7f8c8d; }',
            '        .diameters-list { font-family: monospace; font-size: 0.9em; }',
            '    </style>',
            '</head>',
            '<body>'
        ])
        
        # En-tête du rapport
        html_lines.extend(self._generate_html_header(index_data))
        
        # Résumé exécutif
        html_lines.extend(self._generate_html_executive_summary(index_data, outputs))
        
        # Métadonnées et configuration
        html_lines.extend(self._generate_html_configuration(index_data))
        
        # Résultats par solveur
        for solver in index_data.get("meta", {}).get("solvers", []):
            if solver in outputs:
                html_lines.extend(self._generate_html_solver_results(solver, outputs[solver]))
        
        # Comparaison des solveurs
        if len(index_data.get("meta", {}).get("solvers", [])) > 1:
            html_lines.extend(self._generate_html_comparison(index_data, outputs))
        
        # Détails techniques
        html_lines.extend(self._generate_html_technical_details(index_data, outputs))
        
        # Pied de page
        html_lines.extend(self._generate_html_footer())
        
        # Fermeture HTML
        html_lines.extend([
            '</body>',
            '</html>'
        ])
        
        return '\n'.join(html_lines)
    
    def _generate_html_header(self, index_data: dict) -> List[str]:
        """Génère l'en-tête HTML du rapport."""
        lines = []
        lines.extend([
            f'<h1>📊 Rapport d\'Optimisation de Réseau</h1>',
            f'<div class="summary">',
            f'    <p><strong>Date de génération:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>',
            f'    <p><strong>Méthode d\'optimisation:</strong> {index_data.get("meta", {}).get("method", "N/A")}</p>',
            f'    <p><strong>Solveurs utilisés:</strong> {", ".join(index_data.get("meta", {}).get("solvers", []))}</p>',
            f'</div>'
        ])
        return lines
    
    def _generate_html_executive_summary(self, index_data: dict, outputs: dict) -> List[str]:
        """Génère le résumé exécutif HTML."""
        lines = []
        lines.append('<h2>🎯 Résumé Exécutif</h2>')
        
        solvers = index_data.get("meta", {}).get("solvers", [])
        if len(solvers) == 1:
            solver = solvers[0]
            if solver in outputs:
                result = outputs[solver]
                best_proposal = result.get("proposals", [{}])[0] if result.get("proposals") else {}
                
                lines.extend([
                    f'<p><strong>Solveur:</strong> {solver.upper()}</p>',
                    f'<p><strong>CAPEX optimal:</strong> {best_proposal.get("CAPEX", "N/A"):,.2f} FCFA</p>',
                    f'<p><strong>Contraintes respectées:</strong> <span class="{"success" if best_proposal.get("constraints_ok") else "error"}">{"✅" if best_proposal.get("constraints_ok") else "❌"}</span></p>',
                    f'<p><strong>Hauteur de réservoir:</strong> {best_proposal.get("H_tank_m", "N/A")} m</p>'
                ])
        else:
            lines.append('<p><strong>Comparaison multi-solveurs:</strong></p>')
            lines.append('<ul>')
            for solver in solvers:
                if solver in outputs:
                    result = outputs[solver]
                    best_proposal = result.get("proposals", [{}])[0] if result.get("proposals") else {}
                    lines.append(f'<li><strong>{solver.upper()}:</strong> CAPEX {best_proposal.get("CAPEX", "N/A"):,.2f} FCFA</li>')
            lines.append('</ul>')
        
        return lines
    
    def _generate_html_configuration(self, index_data: dict) -> List[str]:
        """Génère la section de configuration HTML."""
        lines = []
        lines.append('<h2>⚙️ Configuration</h2>')
        
        meta = index_data.get("meta", {})
        lines.append('<h3>Paramètres d\'optimisation</h3>')
        lines.append(f'<p><strong>Méthode:</strong> {meta.get("method", "N/A")}</p>')
        lines.append(f'<p><strong>Solveurs:</strong> {", ".join(meta.get("solvers", []))}</p>')
        
        # Contraintes si disponibles
        if "constraints" in meta:
            constraints = meta["constraints"]
            lines.append('<h3>Contraintes</h3>')
            if "pressure_min_m" in constraints:
                lines.append(f'<p><strong>Pression minimale:</strong> {constraints["pressure_min_m"]} m</p>')
            if "velocity_min_m_s" in constraints:
                lines.append(f'<p><strong>Vitesse minimale:</strong> {constraints["velocity_min_m_s"]} m/s</p>')
            if "velocity_max_m_s" in constraints:
                lines.append(f'<p><strong>Vitesse maximale:</strong> {constraints["velocity_max_m_s"]} m/s</p>')
        
        return lines
    
    def _generate_html_solver_results(self, solver: str, result: dict) -> List[str]:
        """Génère les résultats HTML pour un solveur spécifique."""
        lines = []
        lines.append(f'<div class="solver-section">')
        lines.append(f'<h2>🔍 Résultats - {solver.upper()}</h2>')
        
        if "error" in result:
            lines.append(f'<p class="error">❌ <strong>Erreur:</strong> {result["error"]}</p>')
            lines.append('</div>')
            return lines
        
        meta = result.get("meta", {})
        proposals = result.get("proposals", [])
        
        lines.append(f'<p><strong>Méthode:</strong> {meta.get("method", "N/A")}</p>')
        lines.append(f'<p><strong>Source:</strong> {meta.get("source", "N/A")}</p>')
        
        if proposals:
            lines.append('<h3>Propositions d\'optimisation</h3>')
            
            for i, proposal in enumerate(proposals[:5]):  # Top 5
                lines.extend([
                    f'<div class="proposal">',
                    f'<h4>Proposition {i+1}</h4>',
                    f'<p><strong>ID:</strong> {proposal.get("id", "N/A")}</p>',
                    f'<p><strong>CAPEX:</strong> {proposal.get("CAPEX", "N/A"):,.2f} FCFA</p>',
                    f'<p><strong>Hauteur réservoir:</strong> {proposal.get("H_tank_m", "N/A")} m</p>',
                    f'<p><strong>Contraintes respectées:</strong> <span class="{"success" if proposal.get("constraints_ok") else "error"}">{"✅" if proposal.get("constraints_ok") else "❌"}</span></p>'
                ])
                
                if proposal.get("constraints_violations"):
                    lines.append(f'<p><strong>Violations:</strong> {", ".join(proposal["constraints_violations"])}</p>')
                
                # Diamètres des conduites
                diameters = proposal.get("diameters_mm", {})
                if diameters:
                    lines.append('<p><strong>Diamètres des conduites:</strong></p>')
                    lines.append('<div class="diameters-list">')
                    for pipe, diameter in list(diameters.items())[:10]:  # Top 10
                        lines.append(f'<div>{pipe}: {diameter} mm</div>')
                    if len(diameters) > 10:
                        lines.append(f'<div>... et {len(diameters) - 10} autres conduites</div>')
                    lines.append('</div>')
                
                lines.append('</div>')
        
        lines.append('</div>')
        return lines
    
    def _generate_html_comparison(self, index_data: dict, outputs: dict) -> List[str]:
        """Génère la section de comparaison HTML."""
        lines = []
        lines.append('<h2>📈 Comparaison des Solveurs</h2>')
        
        lines.append('<table class="comparison-table">')
        lines.append('<thead>')
        lines.append('<tr>')
        lines.append('<th>Solveur</th>')
        lines.append('<th>CAPEX (FCFA)</th>')
        lines.append('<th>Hauteur Réservoir (m)</th>')
        lines.append('<th>Contraintes</th>')
        lines.append('</tr>')
        lines.append('</thead>')
        lines.append('<tbody>')
        
        for solver in index_data.get("meta", {}).get("solvers", []):
            if solver in outputs:
                result = outputs[solver]
                if "error" in result:
                    lines.append(f'<tr><td>{solver.upper()}</td><td class="error">❌ Erreur</td><td>-</td><td>-</td></tr>')
                else:
                    best_proposal = result.get("proposals", [{}])[0] if result.get("proposals") else {}
                    capex = best_proposal.get('CAPEX', 'N/A')
                    if isinstance(capex, (int, float)):
                        capex = f"{capex:,.2f}"
                    height = best_proposal.get('H_tank_m', 'N/A')
                    constraints_ok = '✅' if best_proposal.get('constraints_ok') else '❌'
                    lines.append(f'<tr><td>{solver.upper()}</td><td>{capex}</td><td>{height}</td><td class="{"success" if best_proposal.get("constraints_ok") else "error"}">{constraints_ok}</td></tr>')
        
        lines.append('</tbody>')
        lines.append('</table>')
        
        return lines
    
    def _generate_html_technical_details(self, index_data: dict, outputs: dict) -> List[str]:
        """Génère les détails techniques HTML."""
        lines = []
        lines.append('<h2>🔧 Détails Techniques</h2>')
        
        lines.append('<h3>Métadonnées des fichiers</h3>')
        for solver in index_data.get("meta", {}).get("solvers", []):
            if solver in outputs:
                result = outputs[solver]
                if "integrity" in result:
                    integrity = result["integrity"]
                    lines.extend([
                        f'<p><strong>{solver.upper()}:</strong></p>',
                        f'<ul>',
                        f'<li><strong>Checksum:</strong> {integrity.get("checksum", "N/A")}</li>',
                        f'<li><strong>Signature:</strong> {integrity.get("signature", "N/A")}</li>',
                        f'<li><strong>Validité:</strong> <span class="{"success" if integrity.get("signature_valid") else "error"}">{"✅" if integrity.get("signature_valid") else "❌"}</span></li>',
                        f'</ul>'
                    ])
        
        lines.append('<h3>Informations de performance</h3>')
        for solver in index_data.get("meta", {}).get("solvers", []):
            if solver in outputs:
                result = outputs[solver]
                if "execution_time" in result:
                    lines.append(f'<p><strong>{solver.upper()}:</strong> Temps d\'exécution: {result["execution_time"]:.2f}s</p>')
        
        return lines
    
    def _generate_html_footer(self) -> List[str]:
        """Génère le pied de page HTML."""
        lines = []
        lines.extend([
            '<div class="footer">',
            '<p><em>Rapport généré automatiquement par LCPI-CLI</em></p>',
            f'<p><em>Version: 1.0.0 | Date: {datetime.now().strftime("%Y-%m-%d")}</em></p>',
            '</div>'
        ])
        return lines
    
    def _generate_error_pdf(self) -> bytes:
        """Génère un PDF d'erreur simple."""
        # Retourner un PDF minimal en cas d'erreur
        # Ceci est un PDF simple "Hello World" en base64
        import base64
        
        # PDF minimal "Erreur de génération"
        minimal_pdf = """
JVBERi0xLjQKJcOkw7zDtsO4DQoxIDAgb2JqDQo8PA0KL1R5cGUgL0NhdGFsb2cNCi9QYWdlcyAyIDAg
Ug0KPj4NCmVuZG9iag0KMiAwIG9iag0KPDwNCi9UeXBlIC9QYWdlcw0KL0NvdW50IDENCi9LaWRzIFs
gMyAwIFIgXQ0KPj4NCmVuZG9iag0KMyAwIG9iag0KPDwNCi9UeXBlIC9QYWdlDQovUGFyZW50IDIgMC
BSDQovUmVzb3VyY2VzIDw8DQovRm9udCA8PA0KL0YxIDQgMCBSDQo+Pg0KL1Byb2NTZXQgWy9QREYvV
GV4dF0NCj4+DQovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQ0KL0NvbnRlbnRzIDUgMCBSDQo+Pg0KZW5k
b2JqDQo0IDAgb2JqDQo8PA0KL1R5cGUgL0ZvbnQNCi9TdWJ0eXBlIC9UeXBlMQ0KL0Jhc2VGb250IC
9IZWx2ZXRpY2ENCi9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nDQo+Pg0KZW5kb2JqDQo1IDAgb2Jq
DQo8PA0KL0xlbmd0aCAxNA0KPj4NCnN0cmVhbQ0KQlQNCjAgMCBUZA0KL0YxIDEyIFRmDQooRXJyZXVy
IGRlIGdlbmVyYXRpb24pIFRqDQpFVA0KZW5kc3RyZWFtDQplbmRvYmoNCnhyZWYNCjAgNg0KMDAwMDAw
MDAwMCA2NTUzNSBmDQowMDAwMDAwMDEwIDAwMDAwIG4NCjAwMDAwMDAwNzkgMDAwMDAgbg0KMDAwMDAw
MDE3MyAwMDAwMCBuDQowMDAwMDAwMzA4IDAwMDAwIG4NCjAwMDAwMDAzOTYgMDAwMDAgbg0KdHJhaWxl
cg0KPDwNCi9TaXplIDYNCi9Sb290IDEgMCBSDQo+Pg0Kc3RhcnR4cmVmDQo0OTkNCiUlRU9GDQo=
"""
        
        return base64.b64decode(minimal_pdf.strip())
