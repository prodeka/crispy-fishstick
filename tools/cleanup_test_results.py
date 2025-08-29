#!/usr/bin/env python3
"""
Script de nettoyage et organisation des fichiers de test et résultats.
Objectif : Organiser proprement tous les fichiers générés pendant les tests.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def create_results_directory():
    """Crée le dossier de résultats organisé."""
    results_dir = Path("test_results_organized")
    results_dir.mkdir(exist_ok=True)
    
    # Sous-dossiers
    (results_dir / "lcpi_results").mkdir(exist_ok=True)
    (results_dir / "epanet_results").mkdir(exist_ok=True)
    (results_dir / "reports").mkdir(exist_ok=True)
    (results_dir / "scripts").mkdir(exist_ok=True)
    
    return results_dir

def organize_test_files(results_dir):
    """Organise les fichiers de test dans les bons dossiers."""
    
    print("🗂️  ORGANISATION DES FICHIERS DE TEST")
    print("=" * 50)
    
    # Fichiers LCPI
    lcpi_files = [
        "test_amelioration_lcpi",
        "test_amelioration_lcpi_optimise"
    ]
    
    # Fichiers EPANET
    epanet_files = [
        "test_amelioration_epanet",
        "test_epanet_optimise"
    ]
    
    # Rapports
    report_files = [
        "rapport_ameliorations_final_20250829_175803.md",
        "rapport_ameliorations_complet_final.md"
    ]
    
    # Scripts d'outils
    script_files = [
        "tools/analyze_fitness_function.py",
        "tools/harmonize_hydraulic_constraints.py",
        "tools/test_cli_basic.py",
        "tools/analyze_results.py",
        "tools/validation_finale_ameliorations.py",
        "tools/monitor_epanet_optimization.py",
        "tools/cleanup_test_results.py"
    ]
    
    # Déplacer les fichiers LCPI
    print("📁 Déplacement des résultats LCPI...")
    for file in lcpi_files:
        if Path(file).exists():
            shutil.move(file, results_dir / "lcpi_results" / file)
            print(f"   ✅ {file} → lcpi_results/")
    
    # Déplacer les fichiers EPANET
    print("📁 Déplacement des résultats EPANET...")
    for file in epanet_files:
        if Path(file).exists():
            shutil.move(file, results_dir / "epanet_results" / file)
            print(f"   ✅ {file} → epanet_results/")
    
    # Déplacer les rapports
    print("📁 Déplacement des rapports...")
    for file in report_files:
        if Path(file).exists():
            shutil.move(file, results_dir / "reports" / file)
            print(f"   ✅ {file} → reports/")
    
    # Copier les scripts d'outils
    print("📁 Copie des scripts d'outils...")
    for script in script_files:
        if Path(script).exists():
            shutil.copy2(script, results_dir / "scripts" / Path(script).name)
            print(f"   ✅ {script} → scripts/")

def generate_summary_report(results_dir):
    """Génère un rapport de résumé de l'organisation."""
    
    summary_file = results_dir / "README_organisation.md"
    
    summary = f"""# 📁 ORGANISATION DES FICHIERS DE TEST

📅 **Organisé le** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔧 **Script utilisé** : `tools/cleanup_test_results.py`

## 📂 Structure des Dossiers

```
{results_dir.name}/
├── 📁 lcpi_results/          # Résultats des optimisations LCPI
├── 📁 epanet_results/         # Résultats des optimisations EPANET
├── 📁 reports/                # Rapports d'analyse et d'amélioration
├── 📁 scripts/                # Scripts d'outils créés
└── 📄 README_organisation.md  # Ce fichier
```

## 🎯 Résultats Principaux

### 🏆 LCPI (Champion)
- **LCPI Standard** : 5,620,757 FCFA (faisable)
- **LCPI Optimisé** : 5,294,968 FCFA (faisable, -5.8%)

### 🥈 EPANET (Problématique)
- **EPANET Standard** : 19,497,733 FCFA (non faisable)
- **EPANET Optimisé** : 28,719,768 FCFA (non faisable)

## 🚀 Recommandations

1. **Utiliser LCPI Optimisé** pour les optimisations futures
2. **Paramètres optimaux** : 40 générations, 75 population
3. **Contraintes** : Pression min 15m, Vitesse 0.5-2.0 m/s

## 🔧 Scripts Disponibles

Tous les scripts d'outils sont disponibles dans le dossier `scripts/` pour réutilisation future.

---
**🎯 Organisation terminée avec succès ! 🎉**
"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"📄 Rapport de résumé généré: {summary_file}")

def main():
    """Fonction principale."""
    print("🧹 NETTOYAGE ET ORGANISATION DES FICHIERS DE TEST")
    print("=" * 60)
    
    try:
        # Créer la structure de dossiers
        results_dir = create_results_directory()
        print(f"✅ Dossier créé: {results_dir}")
        
        # Organiser les fichiers
        organize_test_files(results_dir)
        
        # Générer le rapport de résumé
        generate_summary_report(results_dir)
        
        print("\n" + "=" * 60)
        print("🎉 ORGANISATION TERMINÉE AVEC SUCCÈS !")
        print("=" * 60)
        print(f"📁 Tous les fichiers sont organisés dans: {results_dir}")
        print("📄 Consultez le README_organisation.md pour plus de détails")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'organisation: {e}")

if __name__ == "__main__":
    main()
