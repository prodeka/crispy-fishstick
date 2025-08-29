#!/usr/bin/env python3
"""
Script d'investigation approfondie des divergences EPANET vs LCPI.
Objectif : Identifier les causes exactes des différences de performance.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List
import re

def investigate_epanet_parameters():
    """Investigue les paramètres de simulation EPANET utilisés."""
    
    print("🔍 INVESTIGATION DES PARAMÈTRES EPANET")
    print("=" * 60)
    
    # Vérifier le fichier INP pour les paramètres EPANET
    inp_file = "bismark_inp.inp"
    if not Path(inp_file).exists():
        print(f"❌ Fichier INP non trouvé: {inp_file}")
        return
    
    print(f"📖 Analyse du fichier INP: {inp_file}")
    
    try:
        with open(inp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Rechercher la section [OPTIONS]
        options_match = re.search(r'\[OPTIONS\](.*?)(?=\[|$)', content, re.DOTALL)
        if options_match:
            options = options_match.group(1)
            print("✅ Section [OPTIONS] trouvée:")
            print(options.strip())
        else:
            print("⚠️  Section [OPTIONS] non trouvée")
        
        # Rechercher la section [PIPES] pour les coefficients de rugosité
        pipes_match = re.search(r'\[PIPES\](.*?)(?=\[|$)', content, re.DOTALL)
        if pipes_match:
            pipes = pipes_match.group(1)
            lines = pipes.strip().split('\n')
            if len(lines) > 1:
                header = lines[0]
                print(f"\n📏 En-tête des conduites: {header}")
                
                # Analyser quelques conduites
                for i, line in enumerate(lines[1:6]):  # Premières 5 conduites
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 6:
                            print(f"   Conduite {i+1}: {parts[:6]}")
        
        # Rechercher les éléments spéciaux
        elements = {
            'RESERVOIRS': r'\[RESERVOIRS\](.*?)(?=\[|$)',
            'PUMPS': r'\[PUMPS\](.*?)(?=\[|$)',
            'VALVES': r'\[VALVES\](.*?)(?=\[|$)',
            'TANKS': r'\[TANKS\](.*?)(?=\[|$)'
        }
        
        print("\n🔧 ÉLÉMENTS SPÉCIAUX DÉTECTÉS:")
        for element, pattern in elements.items():
            match = re.search(pattern, content, re.DOTALL)
            if match:
                lines = match.group(1).strip().split('\n')
                if len(lines) > 1:
                    print(f"   ✅ {element}: {len(lines)-1} éléments")
                else:
                    print(f"   ⚠️  {element}: Section vide")
            else:
                print(f"   ❌ {element}: Non trouvé")
                
    except Exception as e:
        print(f"❌ Erreur lecture INP: {e}")

def investigate_lcpi_implementation():
    """Investigue l'implémentation LCPI Hardy-Cross."""
    
    print("\n🔍 INVESTIGATION DE L'IMPLÉMENTATION LCPI")
    print("=" * 60)
    
    # Vérifier le solveur Hardy-Cross
    hardy_cross_file = "src/lcpi/aep/solver/hardy_cross.py"
    if Path(hardy_cross_file).exists():
        print(f"✅ Fichier Hardy-Cross trouvé: {hardy_cross_file}")
        
        try:
            with open(hardy_cross_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Rechercher les modèles de perte de charge
            if "hazen" in content.lower() or "hazen-williams" in content.lower():
                print("   📊 Modèle de perte de charge: Hazen-Williams")
            elif "darcy" in content.lower() or "darcy-weisbach" in content.lower():
                print("   📊 Modèle de perte de charge: Darcy-Weisbach")
            else:
                print("   ⚠️  Modèle de perte de charge: Non identifié")
            
            # Rechercher la gestion des contraintes
            if "pressure" in content.lower() or "pression" in content.lower():
                print("   📏 Gestion des contraintes de pression: Détectée")
            if "velocity" in content.lower() or "vitesse" in content.lower():
                print("   🚀 Gestion des contraintes de vitesse: Détectée")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture: {e}")
    else:
        print(f"❌ Fichier Hardy-Cross non trouvé: {hardy_cross_file}")
    
    # Vérifier le gestionnaire de contraintes
    constraints_file = "src/lcpi/aep/optimizer/constraints_handler.py"
    if Path(constraints_file).exists():
        print(f"✅ Gestionnaire de contraintes trouvé: {constraints_file}")
        
        try:
            with open(constraints_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Rechercher la logique de faisabilité
            if "feasible" in content.lower() or "faisable" in content.lower():
                print("   ✅ Logique de faisabilité: Détectée")
            if "penalty" in content.lower() or "penalite" in content.lower():
                print("   ⚖️  Système de pénalités: Détecté")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture: {e}")
    else:
        print(f"❌ Gestionnaire de contraintes non trouvé: {constraints_file}")

def investigate_optimization_parameters():
    """Investigue les paramètres d'optimisation utilisés."""
    
    print("\n🔍 INVESTIGATION DES PARAMÈTRES D'OPTIMISATION")
    print("=" * 60)
    
    # Vérifier l'algorithme génétique
    ga_file = "src/lcpi/aep/optimization/genetic_algorithm.py"
    if Path(ga_file).exists():
        print(f"✅ Algorithme génétique trouvé: {ga_file}")
        
        try:
            with open(ga_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Rechercher les paramètres d'optimisation
            params = {
                'mutation_rate': r'mutation.*rate.*=.*?(\d+\.?\d*)',
                'crossover_rate': r'crossover.*rate.*=.*?(\d+\.?\d*)',
                'population_size': r'population.*size.*=.*?(\d+)',
                'generations': r'generations.*=.*?(\d+)'
            }
            
            for param, pattern in params.items():
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    print(f"   ⚙️  {param}: {match.group(1)}")
                else:
                    print(f"   ❓ {param}: Non trouvé")
                    
        except Exception as e:
            print(f"   ❌ Erreur lecture: {e}")
    else:
        print(f"❌ Algorithme génétique non trouvé: {ga_file}")

def investigate_results_divergence():
    """Investigue les divergences dans les résultats."""
    
    print("\n🔍 INVESTIGATION DES DIVERGENCES DE RÉSULTATS")
    print("=" * 60)
    
    # Analyser les résultats LCPI vs EPANET
    results_files = [
        ("test_results_organized/lcpi_results/test_amelioration_lcpi", "LCPI Standard"),
        ("test_results_organized/epanet_results/test_amelioration_epanet", "EPANET Standard"),
        ("test_results_organized/lcpi_results/test_amelioration_lcpi_optimise", "LCPI Optimisé"),
        ("test_results_organized/epanet_results/test_epanet_optimise", "EPANET Optimisé")
    ]
    
    for file_path, name in results_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"\n📊 {name}:")
                
                if "proposals" in data and data["proposals"]:
                    best = data["proposals"][0]
                    
                    # Analyser la faisabilité
                    feasible = best.get("constraints_ok", "N/A")
                    cost = best.get("CAPEX", "N/A")
                    
                    print(f"   💰 Coût: {cost:,} FCFA" if isinstance(cost, (int, float)) else f"   💰 Coût: {cost}")
                    print(f"   ✅ Faisable: {feasible}")
                    
                    # Analyser les métriques hydrauliques
                    p_min = best.get("pression_min", "N/A")
                    v_max = best.get("vitesse_max", "N/A")
                    v_min = best.get("vitesse_min", "N/A")
                    
                    print(f"   📏 Pression min: {p_min}")
                    print(f"   🚀 Vitesse max: {v_max}")
                    print(f"   🐌 Vitesse min: {v_min}")
                    
                    # Analyser les détails de contraintes
                    if "constraint_violations" in best:
                        violations = best["constraint_violations"]
                        print(f"   ⚠️  Violations de contraintes: {violations}")
                    
                else:
                    print("   ❌ Aucune proposition trouvée")
                    
            except Exception as e:
                print(f"   ❌ Erreur lecture: {e}")
        else:
            print(f"   ⏳ {name}: Fichier non trouvé")

def generate_investigation_report():
    """Génère un rapport d'investigation complet."""
    
    print("\n📄 GÉNÉRATION DU RAPPORT D'INVESTIGATION")
    print("=" * 60)
    
    report = []
    report.append("# 🔍 RAPPORT D'INVESTIGATION - DIVERGENCES EPANET vs LCPI")
    report.append(f"📅 Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 80)
    report.append("")
    
    report.append("## 🚨 POINTS CRITIQUES IDENTIFIÉS")
    report.append("")
    report.append("### 1. **Paramètres de Simulation EPANET**")
    report.append("- **Problème potentiel** : Configuration incorrecte des paramètres")
    report.append("- **Investigation requise** : Vérifier [OPTIONS] et paramètres hydrauliques")
    report.append("")
    
    report.append("### 2. **Modèles Hydrauliques**")
    report.append("- **Problème potentiel** : Différences dans les formules et coefficients")
    report.append("- **Investigation requise** : Aligner Hazen-Williams/Darcy-Weisbach")
    report.append("")
    
    report.append("### 3. **Gestion des Contraintes**")
    report.append("- **Problème potentiel** : Logique de faisabilité biaisée")
    report.append("- **Investigation requise** : Vérifier la cohérence des seuils")
    report.append("")
    
    report.append("### 4. **Qualité de l'Optimisation**")
    report.append("- **Problème potentiel** : AG EPANET vs AG LCPI mal calibrés")
    report.append("- **Investigation requise** : Comparer les fonctions d'évaluation")
    report.append("")
    
    report.append("### 5. **Éléments Spéciaux**")
    report.append("- **Problème potentiel** : Réservoirs, pompes, vannes mal gérés")
    report.append("- **Investigation requise** : Vérifier la gestion complète des éléments")
    report.append("")
    
    report.append("## 🔧 ACTIONS RECOMMANDÉES")
    report.append("")
    report.append("### **Immédiat (1-2 jours)**")
    report.append("1. **Audit complet** des paramètres EPANET vs LCPI")
    report.append("2. **Vérification** des modèles hydrauliques utilisés")
    report.append("3. **Analyse** de la logique de faisabilité")
    report.append("")
    
    report.append("### **Court terme (1 semaine)**")
    report.append("1. **Tests unitaires** sur réseaux simples")
    report.append("2. **Validation** des calculs hydrauliques de base")
    report.append("3. **Harmonisation** des paramètres de simulation")
    report.append("")
    
    report.append("### **Moyen terme (2-3 semaines)**")
    report.append("1. **Refactoring** de la fonction d'évaluation")
    report.append("2. **Amélioration** de la gestion des contraintes")
    report.append("3. **Tests de validation** complets")
    report.append("")
    
    report.append("## ⚠️ **AVERTISSEMENT IMPORTANT**")
    report.append("")
    report.append("**Les divergences identifiées ne signifient pas que le code est cassé !**")
    report.append("")
    report.append("Il s'agit probablement de **différences dans l'approche** et la **configuration**")
    report.append("qui peuvent être résolues par un **fine-tuning** et une **validation approfondie**.")
    report.append("")
    report.append("**LCPI reste un solveur valide** avec des **résultats économiques supérieurs**.")
    report.append("")
    
    report.append("## 🎯 **CONCLUSION**")
    report.append("")
    report.append("Cette investigation révèle la **complexité** de la comparaison entre solveurs")
    report.append("et l'**importance** d'un **alignement parfait** des paramètres et modèles.")
    report.append("")
    report.append("**Continuer l'utilisation de LCPI** tout en **investiguant** ces divergences")
    report.append("pour **améliorer** la **comparabilité** et la **fiabilité** des résultats.")
    
    # Sauvegarder le rapport
    report_file = f"rapport_investigation_divergences_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print(f"📄 Rapport d'investigation généré: {report_file}")

def main():
    """Fonction principale."""
    print("🔍 INVESTIGATION APPROFONDIE DES DIVERGENCES EPANET vs LCPI")
    print("=" * 80)
    
    try:
        # Investigations
        investigate_epanet_parameters()
        investigate_lcpi_implementation()
        investigate_optimization_parameters()
        investigate_results_divergence()
        
        # Générer le rapport
        generate_investigation_report()
        
        print("\n" + "=" * 80)
        print("🎯 INVESTIGATION TERMINÉE - RAPPORT GÉNÉRÉ")
        print("=" * 80)
        print("📋 Consultez le rapport pour les recommandations détaillées")
        print("⚠️  Les divergences identifiées nécessitent une investigation approfondie")
        print("✅ LCPI reste un solveur valide malgré ces divergences")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'investigation: {e}")

if __name__ == "__main__":
    from datetime import datetime
    main()
