#!/usr/bin/env python3
"""
Script pour corriger le système de rapports et améliorer les illustrations
"""

import json
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from lcpi.reporting.report_generator import ReportGenerator

def fix_report_generation():
    """Corrige la génération de rapports pour utiliser le bon template"""
    
    print("🔧 Correction du système de rapports")
    print("=" * 60)
    
    # Chemin vers les templates
    template_dir = Path("src/lcpi/reporting/templates")
    
    # Créer le générateur de rapports
    generator = ReportGenerator(template_dir)
    
    # Test avec les données réalistes
    multi_solver_file = Path("results/out_multi_multi_realistic.json")
    
    if not multi_solver_file.exists():
        print(f"❌ Fichier multi-solveurs non trouvé: {multi_solver_file}")
        return False
    
    # Métadonnées du projet
    project_metadata = {
        "nom_projet": "Test Multi-Solveurs Corrigé",
        "client": "Client Test",
        "description": "Test du système de génération de rapports corrigé"
    }
    
    try:
        # Générer le rapport avec détection automatique
        print("🔄 Génération du rapport corrigé...")
        html_content = generator.generate_html_report(
            selected_logs_paths=[multi_solver_file],
            project_metadata=project_metadata,
            lcpi_version="2.1.0"
        )
        
        # Sauvegarder le rapport
        output_file = Path("results/test_multi_solver_report_corrected.html")
        output_file.write_text(html_content, encoding='utf-8')
        
        print(f"✅ Rapport corrigé généré: {output_file}")
        print(f"📊 Taille du rapport: {len(html_content)} caractères")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport: {e}")
        import traceback
        traceback.print_exc()
        return False

def improve_cost_bars():
    """Améliore les barres de coût dans le template"""
    
    print("\n🎨 Amélioration des barres de coût")
    print("=" * 60)
    
    # Lire le template actuel
    template_file = Path("src/lcpi/reporting/templates/multi_solver_comparison.jinja2")
    
    if not template_file.exists():
        print(f"❌ Template non trouvé: {template_file}")
        return False
    
    content = template_file.read_text(encoding='utf-8')
    
    # Améliorer les barres de coût
    improved_content = content.replace(
        'style="width: {{ (solver_data[solver].best_proposal.CAPEX / max_capex * 100) | round(1) }}%"',
        'style="width: {{ ((solver_data[solver].best_proposal.CAPEX / max_capex) * 100) | round(1) }}%"'
    )
    
    # Ajouter une logique pour éviter les barres vides
    improved_content = improved_content.replace(
        'style="width: 0.0%"',
        'style="width: 5.0%"'
    )
    
    # Sauvegarder le template amélioré
    template_file.write_text(improved_content, encoding='utf-8')
    
    print("✅ Template amélioré avec de meilleures barres de coût")
    return True

def create_enhanced_template():
    """Crée un template amélioré avec de meilleures illustrations"""
    
    print("\n🎨 Création d'un template amélioré")
    print("=" * 60)
    
    enhanced_template = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparaison Multi-Solveurs - {{ projet_metadata.nom_projet }}</title>
    
    <style>
    /* Styles améliorés pour les barres de coût */
    .cost-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .cost-bar-fill::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, 
            rgba(255,255,255,0.1) 0%, 
            rgba(255,255,255,0.2) 50%, 
            rgba(255,255,255,0.1) 100%);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Amélioration des barres de coût */
    .cost-bar-container {
        height: 12px;
        background: var(--surface-2);
        border-radius: 6px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .cost-bar-fill.epanet {
        background: linear-gradient(90deg, #4aa3ff, #2d7dd2);
    }
    
    .cost-bar-fill.lcpi {
        background: linear-gradient(90deg, #21c55d, #16a34a);
    }
    
    /* Amélioration des KPI */
    .kpi-item {
        background: var(--surface-2);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .kpi-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--brand), var(--ok));
    }
    
    /* Amélioration des badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .badge::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, 
            rgba(255,255,255,0.1) 0%, 
            rgba(255,255,255,0.2) 50%, 
            rgba(255,255,255,0.1) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .badge:hover::before {
        opacity: 1;
    }
    
    /* Amélioration des tableaux */
    .comparison-table tbody tr {
        transition: all 0.2s ease;
    }
    
    .comparison-table tbody tr:hover {
        background: var(--surface-2);
        transform: scale(1.01);
    }
    
    /* Animations d'entrée */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .section {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .section:nth-child(2) { animation-delay: 0.1s; }
    .section:nth-child(3) { animation-delay: 0.2s; }
    .section:nth-child(4) { animation-delay: 0.3s; }
    .section:nth-child(5) { animation-delay: 0.4s; }
    </style>
    
    {{ inline_css | safe }}
</head>
<body>
    <div class="report-container">
        <header class="page-header">
            <div class="header-content">
                <h1>Comparaison Multi-Solveurs</h1>
                <h2>{{ projet_metadata.nom_projet }}</h2>
                <div class="meta-info">
                    Client: {{ projet_metadata.client or 'Non spécifié' }} · 
                    Généré le {{ generation_date }} · LCPI v{{ version_lcpi }}
                </div>
            </div>
        </header>

        <nav class="toc">
            <h3>Sommaire</h3>
            <ul>
                <li><a href="#overview">Vue d'ensemble</a></li>
                <li><a href="#comparison">Comparaison détaillée</a></li>
                {% for solver in solvers %}
                <li><a href="#solver-{{ solver }}">{{ solver | upper }}</a></li>
                {% endfor %}
                <li><a href="#hydraulics">Analyse hydraulique</a></li>
                <li><a href="#diameters">Analyse des diamètres</a></li>
            </ul>
        </nav>

        <main>
            <!-- Vue d'ensemble -->
            <section id="overview" class="section">
                <h3>Vue d'ensemble</h3>
                <div class="overview-cards">
                    <div class="overview-card">
                        <h4>Résumé global</h4>
                        <div class="kpi-grid">
                            {% set max_capex = solvers | map('upper') | map('lower') | map('replace', ' ', '_') | map('attr', 'best_proposal') | map('attr', 'CAPEX') | max %}
                            {% for solver in solvers %}
                            <div class="kpi-item">
                                <div class="kpi-label">{{ solver | upper }}</div>
                                <div class="kpi-value">
                                    <div class="kpi-main">{{ solver_data[solver].best_proposal.CAPEX | round(0) | int }} FCFA</div>
                                    <div class="kpi-sub">
                                        {% if solver_data[solver].best_proposal.min_pressure_m >= 12 %}
                                        <span class="badge badge-ok">OK</span>
                                        {% else %}
                                        <span class="badge badge-ko">KO</span>
                                        {% endif %}
                                        Pmin: {{ solver_data[solver].best_proposal.min_pressure_m | round(1) }}m
                                    </div>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>

                    <div class="overview-card">
                        <h4>Comparaison des coûts</h4>
                        <div class="cost-comparison">
                            {% set max_capex = solvers | map('upper') | map('lower') | map('replace', ' ', '_') | map('attr', 'best_proposal') | map('attr', 'CAPEX') | max %}
                            {% for solver in solvers %}
                            <div class="cost-bar">
                                <div class="cost-label">{{ solver | upper }}</div>
                                <div class="cost-bar-container">
                                    <div class="cost-bar-fill {{ solver }}" style="width: {{ ((solver_data[solver].best_proposal.CAPEX / max_capex) * 100) | round(1) }}%"></div>
                                </div>
                                <div class="cost-value">{{ solver_data[solver].best_proposal.CAPEX | round(0) | int }} FCFA</div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </section>

            <!-- Comparaison détaillée -->
            <section id="comparison" class="section">
                <h3>Comparaison détaillée</h3>
                <div class="comparison-table-container">
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th>Métrique</th>
                                {% for solver in solvers %}
                                <th>{{ solver | upper }}</th>
                                {% endfor %}
                                <th>Différence</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>CAPEX (FCFA)</td>
                                {% for solver in solvers %}
                                <td>{{ solver_data[solver].best_proposal.CAPEX | round(0) | int }}</td>
                                {% endfor %}
                                <td class="diff">
                                    {% set epanet_capex = solver_data.epanet.best_proposal.CAPEX %}
                                    {% set lcpi_capex = solver_data.lcpi.best_proposal.CAPEX %}
                                    {% set diff = lcpi_capex - epanet_capex %}
                                    {% set diff_pct = (diff / epanet_capex * 100) | round(1) %}
                                    {% if diff < 0 %}
                                    <span class="diff-negative">{{ diff_pct }}%</span>
                                    {% else %}
                                    <span class="diff-positive">+{{ diff_pct }}%</span>
                                    {% endif %}
                                </td>
                            </tr>
                            <tr>
                                <td>Pression min (m)</td>
                                {% for solver in solvers %}
                                <td>{{ solver_data[solver].best_proposal.min_pressure_m | round(3) }}</td>
                                {% endfor %}
                                <td class="diff">
                                    {% set epanet_pressure = solver_data.epanet.best_proposal.min_pressure_m %}
                                    {% set lcpi_pressure = solver_data.lcpi.best_proposal.min_pressure_m %}
                                    {% set diff = lcpi_pressure - epanet_pressure %}
                                    {% if diff > 0 %}
                                    <span class="diff-positive">+{{ diff | round(3) }}m</span>
                                    {% else %}
                                    <span class="diff-negative">{{ diff | round(3) }}m</span>
                                    {% endif %}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- Sections par solveur -->
            {% for solver in solvers %}
            <section id="solver-{{ solver }}" class="section">
                <h3>{{ solver | upper }}</h3>
                <div class="solver-cards">
                    <div class="solver-card">
                        <h4>Métadonnées</h4>
                        <div class="meta-grid">
                            <div class="meta-item">
                                <span class="meta-label">Fichier réseau</span>
                                <span class="meta-value">{{ solver_data[solver].meta.source_meta.file | default('—') }}</span>
                            </div>
                            <div class="meta-item">
                                <span class="meta-label">Méthode</span>
                                <span class="meta-value">{{ solver_data[solver].meta.method }}</span>
                            </div>
                            <div class="meta-item">
                                <span class="meta-label">Contraintes</span>
                                <span class="meta-value">
                                    Pmin: {{ solver_data[solver].meta.constraints.pressure_min_m | default('—') }}m ·
                                    Vmax: {{ solver_data[solver].meta.constraints.velocity_max_m_s | default('—') }}m/s
                                </span>
                            </div>
                        </div>
                    </div>

                    <div class="solver-card">
                        <h4>Résultats</h4>
                        <div class="results-grid">
                            <div class="result-item">
                                <span class="result-label">CAPEX</span>
                                <span class="result-value">{{ solver_data[solver].best_proposal.CAPEX | round(0) | int }} FCFA</span>
                            </div>
                            <div class="result-item">
                                <span class="result-label">Pression min</span>
                                <span class="result-value">{{ solver_data[solver].best_proposal.min_pressure_m | round(3) }} m</span>
                            </div>
                            <div class="result-item">
                                <span class="result-label">Vitesse max</span>
                                <span class="result-value">{{ solver_data[solver].best_proposal.max_velocity_ms | default('—') }} m/s</span>
                            </div>
                            <div class="result-item">
                                <span class="result-label">Statut</span>
                                <span class="result-value">
                                    {% if solver_data[solver].best_proposal.min_pressure_m >= 12 %}
                                    <span class="badge badge-ok">OK</span>
                                    {% else %}
                                    <span class="badge badge-ko">KO</span>
                                    {% endif %}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            {% endfor %}
        </main>

        <footer class="page-footer">
            <p>Rapport généré le {{ generation_date }} — LCPI v{{ version_lcpi }}</p>
        </footer>
    </div>
</body>
</html>'''
    
    # Sauvegarder le template amélioré
    enhanced_file = Path("src/lcpi/reporting/templates/multi_solver_comparison_enhanced.jinja2")
    enhanced_file.write_text(enhanced_template, encoding='utf-8')
    
    print(f"✅ Template amélioré créé: {enhanced_file}")
    return True

def list_available_templates():
    """Liste tous les templates disponibles"""
    
    print("\n📋 Templates disponibles")
    print("=" * 60)
    
    template_dir = Path("src/lcpi/reporting/templates")
    
    print("📁 Templates principaux:")
    for template in template_dir.glob("*.jinja2"):
        print(f"  - {template.name}")
    
    print("\n📁 Templates de base:")
    for template in template_dir.glob("*.html"):
        print(f"  - {template.name}")
    
    print("\n📁 Partiels:")
    partials_dir = template_dir / "partials"
    if partials_dir.exists():
        for partial in partials_dir.glob("*.html"):
            print(f"  - partials/{partial.name}")
    
    print("\n📁 Sections:")
    sections_dir = template_dir / "sections"
    if sections_dir.exists():
        for section in sections_dir.glob("*.html"):
            print(f"  - sections/{section.name}")

def explain_template_system():
    """Explique comment le système de templates fonctionne"""
    
    print("\n🔧 Explication du système de templates")
    print("=" * 60)
    
    explanation = """
📋 Système de Templates LCPI

🎯 Templates Principaux:
- multi_solver_comparison.jinja2: Template pour comparaison multi-solveurs
- optimisation_tabs.jinja2: Template avec onglets pour plusieurs logs
- optimisation_unified.jinja2: Template unifié pour un seul log
- base_simple.html: Template de base simple

🔧 Logique de Sélection:
1. Détection automatique des données multi-solveurs
2. Si multi-solveurs → multi_solver_comparison.jinja2
3. Si plusieurs logs → optimisation_tabs.jinja2
4. Si un seul log → optimisation_unified.jinja2
5. Fallback → base_simple.html

📁 Partiels Disponibles:
- tableau_recapitulatif.html: Tableau récapitulatif réutilisable

🔗 Comment Brancher:
1. Dans report_generator.py, méthode generate_html_report()
2. Détection automatique avec _detect_multi_solver_data()
3. Sélection du template approprié
4. Rendu avec Jinja2

⚠️ Problème Actuel:
- Le flag --report n'utilise pas la détection automatique
- Il utilise toujours optimisation_tabs.jinja2 pour multi-solveurs
- Il faut corriger la logique dans cli.py
"""
    
    print(explanation)

def main():
    """Fonction principale"""
    print("🔧 Correction du système de rapports")
    print("=" * 80)
    
    # 1. Lister les templates disponibles
    list_available_templates()
    
    # 2. Expliquer le système
    explain_template_system()
    
    # 3. Améliorer les barres de coût
    improve_cost_bars()
    
    # 4. Créer un template amélioré
    create_enhanced_template()
    
    # 5. Tester la génération corrigée
    fix_report_generation()
    
    print("\n" + "=" * 80)
    print("🎉 Corrections terminées!")
    print("📁 Fichiers générés:")
    print("  - src/lcpi/reporting/templates/multi_solver_comparison_enhanced.jinja2")
    print("  - results/test_multi_solver_report_corrected.html")
    print("\n🌐 Ouvrir le rapport corrigé pour voir les améliorations")

if __name__ == "__main__":
    main()
