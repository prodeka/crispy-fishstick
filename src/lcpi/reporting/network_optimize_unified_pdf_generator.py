"""
Générateur de rapports PDF spécialisé pour network-optimize-unified.
Réutilise les composants existants et utilise le template Jinja2 spécifique.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import shutil
import subprocess
import tempfile
from io import BytesIO
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .utils.pdf_generator import export_to_pdf
from .table_templates import TABLE_TEMPLATES, initialize_log_data


class NetworkOptimizeUnifiedPDFGenerator:
    """Génère des rapports PDF pour network-optimize-unified."""
    
    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialise le générateur PDF.
        
        Args:
            template_dir: Chemin vers le dossier des templates (optionnel)
        """
        if template_dir is None:
            # Chemin par défaut vers les templates
            template_dir = Path(__file__).parent / "templates"
        
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def generate_pdf_report(
        self, 
        result_data: dict, 
        input_file: str = "N/A",
        version: str = "1.0.0"
    ) -> bytes:
        """
        Génère un rapport PDF pour network-optimize-unified.
        
        Args:
            result_data: Données de résultat de l'optimisation
            input_file: Chemin du fichier d'entrée
            version: Version du logiciel
            
        Returns:
            Contenu PDF du rapport en bytes
        """
        try:
            # Générer le contenu HTML avec le template Jinja2
            html_content = self._generate_html_content(result_data, input_file, version)
            
            # Essayer d'abord WeasyPrint
            try:
                return self._generate_with_weasyprint(html_content)
            except Exception as e:
                print(f"WeasyPrint non disponible: {e}")
                # 1) Fallback via pdfkit (wkhtmltopdf)
                try:
                    return self._generate_with_pdfkit(html_content)
                except Exception as e_pdfkit:
                    print(f"pdfkit/wkhtmltopdf non disponible: {e_pdfkit}")
                # 2) Fallback via CLI wkhtmltopdf si présent dans PATH
                try:
                    return self._generate_with_wkhtmltopdf_cli(html_content)
                except Exception as e_cli:
                    print(f"wkhtmltopdf CLI non disponible: {e_cli}")
                # 3) Fallback vers le composant PDF existant
                try:
                    return self._generate_with_existing_pdf(html_content)
                except Exception as e2:
                    print(f"Composant PDF existant non disponible: {e2}")
                    
                    # En dernier recours, retourner un PDF d'erreur
                    return self._generate_error_pdf()
                    
        except Exception as e:
            print(f"Erreur lors de la génération du rapport PDF: {e}")
            return self._generate_error_pdf()
    
    def _generate_html_content(
        self, 
        result_data: dict, 
        input_file: str, 
        version: str
    ) -> str:
        """Génère le contenu HTML avec le template Jinja2."""
        
        # Préparer le contexte pour le template
        context = self._prepare_template_context(result_data, input_file, version)
        
        try:
            # Utiliser le template spécialisé
            template = self.env.get_template("network_optimize_unified_pdf.jinja2")
            return template.render(**context)
        except Exception as e:
            print(f"Erreur lors du rendu du template: {e}")
            # Fallback vers un HTML simple
            return self._generate_fallback_html(result_data, input_file, version)
    
    def _prepare_template_context(
        self, 
        result_data: dict, 
        input_file: str, 
        version: str
    ) -> dict:
        """Prépare le contexte pour le template Jinja2."""
        
        # Extraire les métadonnées
        meta = result_data.get("meta", {})
        proposals = result_data.get("proposals", [])
        hydraulics = result_data.get("hydraulics", {})
        
        # Préparer les contraintes si disponibles
        constraints = {}
        if "constraints" in result_data:
            constraints = result_data["constraints"]
        elif "pressure_min_m" in meta or "velocity_max_m_s" in meta:
            constraints = {
                "pressure_min_m": meta.get("pressure_min_m"),
                "velocity_min_m_s": meta.get("velocity_min_m_s"),
                "velocity_max_m_s": meta.get("velocity_max_m_s")
            }
        
        # Enrichir les métadonnées avec les informations de l'optimisation
        enriched_meta = {
            "solver": meta.get("solver", "N/A"),
            "method": meta.get("method", "N/A"),
            "generations": meta.get("generations", "N/A"),
            "population": meta.get("population", "N/A"),
            "duration_seconds": meta.get("duration_seconds"),
            "solver_calls": meta.get("solver_calls"),
            **meta  # Inclure toutes les autres métadonnées
        }
        
        context = {
            "meta": enriched_meta,
            "proposals": proposals,
            "hydraulics": hydraulics,
            "constraints": constraints,
            "input_file": input_file,
            "version": version,
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return context
    
    def _generate_fallback_html(
        self, 
        result_data: dict, 
        input_file: str, 
        version: str
    ) -> str:
        """Génère un HTML de fallback si le template échoue."""
        
        html_lines = [
            '<!DOCTYPE html>',
            '<html lang="fr">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <title>Rapport d\'Optimisation Réseau</title>',
            '    <style>',
            '        body { font-family: Arial, sans-serif; margin: 20px; }',
            '        h1 { color: #2c5aa0; }',
            '        .section { margin: 20px 0; }',
            '        .info-item { margin: 10px 0; }',
            '        .info-label { font-weight: bold; color: #2c5aa0; }',
            '    </style>',
            '</head>',
            '<body>',
            '    <h1>📊 Rapport d\'Optimisation Réseau</h1>',
            f'    <p><strong>Fichier source:</strong> {input_file}</p>',
            f'    <p><strong>Version:</strong> {version}</p>',
            f'    <p><strong>Date de génération:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>'
        ]
        
        # Informations générales
        meta = result_data.get("meta", {})
        html_lines.extend([
            '    <div class="section">',
            '        <h2>🎯 Informations Générales</h2>',
            f'        <div class="info-item"><span class="info-label">Méthode:</span> {meta.get("method", "N/A")}</div>',
            f'        <div class="info-item"><span class="info-label">Solveur:</span> {meta.get("solver", "N/A")}</div>',
            '    </div>'
        ])
        
        # Propositions
        proposals = result_data.get("proposals", [])
        if proposals:
            html_lines.extend([
                '    <div class="section">',
                '        <h2>🏆 Résultats de l\'Optimisation</h2>'
            ])
            
            for i, proposal in enumerate(proposals[:5]):  # Top 5
                html_lines.extend([
                    f'        <div class="info-item">',
                    f'            <h3>Proposition {i+1}</h3>',
                    f'            <div><span class="info-label">CAPEX:</span> {proposal.get("CAPEX", "N/A"):,.0f} FCFA</div>',
                    f'            <div><span class="info-label">Contraintes respectées:</span> {"✅ Oui" if proposal.get("constraints_ok") else "❌ Non"}</div>',
                    '        </div>'
                ])
            
            html_lines.append('    </div>')
        
        # Statistiques hydrauliques
        hydraulics = result_data.get("hydraulics", {})
        if hydraulics and "statistics" in hydraulics:
            stats = hydraulics["statistics"]
            html_lines.extend([
                '    <div class="section">',
                '        <h2>📊 Statistiques Hydrauliques</h2>'
            ])
            
            if "pressures" in stats:
                p = stats["pressures"]
                html_lines.extend([
                    '        <h3>📊 Pressions</h3>',
                    f'        <div class="info-item"><span class="info-label">Nœuds:</span> {p.get("count", 0)}</div>',
                    f'        <div class="info-item"><span class="info-label">Min:</span> {p.get("min", 0):.3f} m</div>',
                    f'        <div class="info-item"><span class="info-label">Max:</span> {p.get("max", 0):.3f} m</div>'
                ])
            
            if "flows" in stats:
                f = stats["flows"]
                html_lines.extend([
                    '        <h3>🌊 Débits</h3>',
                    f'        <div class="info-item"><span class="info-label">Conduites:</span> {f.get("count", 0)}</div>',
                    f'        <div class="info-item"><span class="info-label">Sens normal:</span> {f.get("positive_flows", 0)}</div>',
                    f'        <div class="info-item"><span class="info-label">Sens inverse:</span> {f.get("negative_flows", 0)}</div>'
                ])
            
            html_lines.append('    </div>')
        
        html_lines.extend([
            '</body>',
            '</html>'
        ])
        
        return '\n'.join(html_lines)
    
    def _generate_with_weasyprint(self, html_content: str) -> bytes:
        """Génère un PDF avec WeasyPrint."""
        try:
            import weasyprint
            from weasyprint import HTML
            
            # Créer le PDF
            html_doc = HTML(string=html_content)
            pdf_bytes = html_doc.write_pdf()
            return pdf_bytes
            
        except ImportError:
            raise Exception("WeasyPrint non installé")
        except Exception as e:
            raise Exception(f"Erreur WeasyPrint: {e}")

    def _generate_with_pdfkit(self, html_content: str) -> bytes:
        """Génère un PDF avec pdfkit (requiert wkhtmltopdf)."""
        try:
            import pdfkit  # type: ignore
        except Exception as e:
            raise Exception(f"Module pdfkit non installé: {e}")

        wkhtml_path = shutil.which("wkhtmltopdf") or shutil.which("wkhtmltopdf.exe")
        if wkhtml_path is None:
            raise Exception("wkhtmltopdf non trouvé dans le PATH")

        try:
            config = pdfkit.configuration(wkhtmltopdf=wkhtml_path)
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
                tmp_path = Path(tmp_pdf.name)
            try:
                pdfkit.from_string(html_content, str(tmp_path), configuration=config)
                content = tmp_path.read_bytes()
                tmp_path.unlink(missing_ok=True)
                return content
            except Exception:
                if tmp_path.exists():
                    tmp_path.unlink(missing_ok=True)
                raise
        except Exception as e:
            raise Exception(f"Erreur pdfkit: {e}")

    def _generate_with_wkhtmltopdf_cli(self, html_content: str) -> bytes:
        """Génère un PDF en appelant directement wkhtmltopdf en CLI."""
        wkhtml = shutil.which("wkhtmltopdf") or shutil.which("wkhtmltopdf.exe")
        if wkhtml is None:
            raise Exception("wkhtmltopdf non trouvé dans le PATH")

        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as tmp_html:
            tmp_html.write(html_content)
            html_path = Path(tmp_html.name)
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
            pdf_path = Path(tmp_pdf.name)

        try:
            cmd = [wkhtml, str(html_path), str(pdf_path)]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            if proc.returncode != 0:
                stderr = proc.stderr.decode(errors='ignore') if proc.stderr else ''
                raise Exception(f"wkhtmltopdf a échoué (code {proc.returncode}): {stderr[:200]}")
            content = pdf_path.read_bytes()
            return content
        finally:
            try:
                html_path.unlink(missing_ok=True)
            except Exception:
                pass
            try:
                pdf_path.unlink(missing_ok=True)
            except Exception:
                pass
    
    def _generate_with_existing_pdf(self, html_content: str) -> bytes:
        """Génère un PDF avec le composant existant."""
        try:
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                tmp_path = Path(tmp_file.name)
            
            try:
                # Utiliser le composant PDF existant
                success = export_to_pdf(
                    html_content=html_content,
                    output_path=tmp_path,
                    base_url=self.template_dir
                )
                
                if success:
                    # Lire le contenu du fichier PDF temporaire
                    with open(tmp_path, 'rb') as f:
                        pdf_content = f.read()
                    
                    # Nettoyer le fichier temporaire
                    os.unlink(tmp_path)
                    
                    return pdf_content
                else:
                    raise Exception("Échec de la génération PDF avec le composant existant")
                    
            except Exception as e:
                # Nettoyer en cas d'erreur
                if tmp_path.exists():
                    os.unlink(tmp_path)
                raise e
                
        except Exception as e:
            raise Exception(f"Erreur composant PDF existant: {e}")
    
    def _generate_error_pdf(self) -> bytes:
        """Génère un PDF d'erreur simple."""
        # 1) Essayer de générer un PDF minimal avec reportlab si disponible
        try:
            from reportlab.pdfgen import canvas  # type: ignore
            from reportlab.lib.pagesizes import A4  # type: ignore
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            c.setTitle("Erreur de génération PDF")
            width, height = A4
            c.setFont("Helvetica-Bold", 16)
            c.drawString(72, height - 72, "❌ Erreur de génération PDF")
            c.setFont("Helvetica", 11)
            c.drawString(72, height - 100, "Impossible de générer le rapport PDF.")
            c.drawString(72, height - 116, "Utilisez --report html ou installez WeasyPrint / wkhtmltopdf.")
            c.showPage()
            c.save()
            return buffer.getvalue()
        except Exception:
            # 2) Sinon, tenter via WeasyPrint avec un HTML d'erreur
            try:
                error_html = '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Erreur de génération PDF</title>
                    <style>
                        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                        h1 { color: #e74c3c; }
                        .error { background: #fdf2f2; border: 1px solid #fecaca; padding: 20px; border-radius: 5px; }
                    </style>
                </head>
                <body>
                    <h1>❌ Erreur de génération PDF</h1>
                    <div class="error">
                        <p>Impossible de générer le rapport PDF.</p>
                        <p>Veuillez utiliser l'option --report html à la place.</p>
                    </div>
                </body>
                </html>
                '''
                return self._generate_with_weasyprint(error_html)
            except Exception:
                # 3) En dernier recours, lever une erreur
                raise Exception("Impossible de générer un PDF d'erreur")
    
    def generate_multi_solver_pdf_report(
        self, 
        outputs: dict, 
        input_file: str = "N/A",
        version: str = "1.0.0"
    ) -> bytes:
        """
        Génère un rapport PDF multi-solveurs.
        
        Args:
            outputs: Résultats par solveur
            input_file: Chemin du fichier d'entrée
            version: Version du logiciel
            
        Returns:
            Contenu PDF du rapport en bytes
        """
        # Pour l'instant, on génère un rapport pour le premier solveur
        # TODO: Implémenter un template multi-solveurs
        if outputs:
            first_solver = list(outputs.keys())[0]
            return self.generate_pdf_report(outputs[first_solver], input_file, version)
        else:
            return self._generate_error_pdf()
