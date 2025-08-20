#!/usr/bin/env python3
"""
Script d'analyse des résultats des tests avec --num-prop
Identifie les incohérences dans les données générées
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

def analyze_prop_results():
    """Analyse les résultats des tests avec --num-prop"""
    
    results_dir = Path("results")
    prop_files = []
    
    # Identifier les fichiers de test avec --num-prop
    for file_path in results_dir.glob("test*prop*.json"):
        if file_path.is_file():
            prop_files.append(file_path)
    
    print(f"🔍 Analyse de {len(prop_files)} fichiers de test avec --num-prop")
    print("=" * 80)
    
    for file_path in prop_files:
        print(f"\n📁 Fichier: {file_path.name}")
        print("-" * 60)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Analyser la structure
            analyze_file_structure(data, file_path.name)
            
            # Analyser les propositions
            analyze_proposals(data, file_path.name)
            
            # Analyser les cohérences
            analyze_coherences(data, file_path.name)
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse de {file_path.name}: {e}")
    
    print("\n" + "=" * 80)
    print("🎯 ANALYSE TERMINÉE")

def analyze_file_structure(data: Dict[str, Any], filename: str):
    """Analyse la structure du fichier"""
    
    # Vérifier la présence des sections obligatoires
    required_sections = ["meta", "proposals"]
    missing_sections = [section for section in required_sections if section not in data]
    
    if missing_sections:
        print(f"⚠️  Sections manquantes: {missing_sections}")
    else:
        print("✅ Structure de base correcte")
    
    # Vérifier les métadonnées
    meta = data.get("meta", {})
    print(f"   - Méthode: {meta.get('method', 'N/A')}")
    print(f"   - Solveur: {meta.get('solver', 'N/A')}")
    print(f"   - Contraintes: {meta.get('constraints', {})}")

def analyze_proposals(data: Dict[str, Any], filename: str):
    """Analyse les propositions générées"""
    
    proposals = data.get("proposals", [])
    print(f"📊 Propositions: {len(proposals)} trouvées")
    
    if not proposals:
        print("❌ Aucune proposition trouvée")
        return
    
    # Analyser chaque proposition
    for i, prop in enumerate(proposals):
        print(f"\n   Proposition {i+1}:")
        
        # Vérifier l'ID
        prop_id = prop.get("id", "N/A")
        print(f"     - ID: {prop_id}")
        
        # Vérifier le coût
        capex = prop.get("CAPEX")
        if capex is not None:
            print(f"     - CAPEX: {capex:,.2f} FCFA")
        else:
            print(f"     - CAPEX: ❌ Manquant")
        
        # Vérifier les contraintes
        constraints_ok = prop.get("constraints_ok")
        print(f"     - Contraintes respectées: {'✅' if constraints_ok else '❌'}")
        
        # Vérifier les diamètres
        diameters = prop.get("diameters_mm", {})
        if diameters:
            print(f"     - Diamètres: {len(diameters)} conduites")
            
            # Vérifier la cohérence des diamètres
            invalid_diameters = []
            for pipe_id, diameter in diameters.items():
                if not isinstance(diameter, (int, float)) or diameter <= 0:
                    invalid_diameters.append(f"{pipe_id}: {diameter}")
            
            if invalid_diameters:
                print(f"     - ⚠️  Diamètres invalides: {invalid_diameters[:3]}...")
            else:
                print(f"     - ✅ Diamètres valides")
        else:
            print(f"     - Diamètres: ❌ Manquants")

def analyze_coherences(data: Dict[str, Any], filename: str):
    """Analyse les cohérences dans les données"""
    
    proposals = data.get("proposals", [])
    if len(proposals) < 2:
        return
    
    print(f"\n🔍 Analyse des cohérences:")
    
    # Vérifier la cohérence des IDs
    ids = [prop.get("id", "") for prop in proposals]
    unique_ids = set(ids)
    
    if len(ids) != len(unique_ids):
        print(f"   ⚠️  IDs dupliqués détectés: {[id for id in ids if ids.count(id) > 1]}")
    else:
        print(f"   ✅ IDs uniques")
    
    # Vérifier la cohérence des coûts
    capex_values = [prop.get("CAPEX") for prop in proposals if prop.get("CAPEX") is not None]
    
    if len(capex_values) >= 2:
        # Vérifier que les variations ont des coûts différents
        if len(set(capex_values)) == 1:
            print(f"   ⚠️  Tous les coûts sont identiques: {capex_values[0]:,.2f} FCFA")
        else:
            print(f"   ✅ Coûts différents: {min(capex_values):,.2f} - {max(capex_values):,.2f} FCFA")
    
    # Vérifier la cohérence des diamètres
    if len(proposals) >= 2:
        base_diameters = proposals[0].get("diameters_mm", {})
        variation_diameters = proposals[1].get("diameters_mm", {})
        
        if base_diameters and variation_diameters:
            # Compter les diamètres différents
            different_count = 0
            for pipe_id in base_diameters:
                if pipe_id in variation_diameters:
                    if base_diameters[pipe_id] != variation_diameters[pipe_id]:
                        different_count += 1
            
            if different_count == 0:
                print(f"   ⚠️  Aucune variation de diamètre détectée")
            else:
                print(f"   ✅ {different_count} diamètres variés entre les propositions")
    
    # Vérifier la cohérence des contraintes
    constraints_ok_count = sum(1 for prop in proposals if prop.get("constraints_ok", False))
    print(f"   - Propositions valides: {constraints_ok_count}/{len(proposals)}")

def check_specific_issues():
    """Vérifie des problèmes spécifiques identifiés"""
    
    print("\n🔍 VÉRIFICATION DES PROBLÈMES SPÉCIFIQUES")
    print("=" * 60)
    
    # Vérifier le fichier test_multi_prop.json
    multi_prop_file = Path("results/test_multi_prop.json")
    if multi_prop_file.exists():
        print(f"\n📁 Analyse détaillée de {multi_prop_file.name}")
        
        with open(multi_prop_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        proposals = data.get("proposals", [])
        
        # Vérifier l'ordre des coûts
        print(f"\n💰 Analyse des coûts:")
        for i, prop in enumerate(proposals):
            capex = prop.get("CAPEX", 0)
            constraints_ok = prop.get("constraints_ok", False)
            print(f"   Proposition {i+1}: {capex:,.2f} FCFA - Contraintes: {'✅' if constraints_ok else '❌'}")
        
        # Vérifier les violations de contraintes
        print(f"\n🚨 Violations de contraintes:")
        for i, prop in enumerate(proposals):
            violations = prop.get("constraints_violations", [])
            if violations:
                print(f"   Proposition {i+1}: {violations}")
        
        # Vérifier la cohérence des métriques
        print(f"\n📊 Métriques de performance:")
        for i, prop in enumerate(proposals):
            metrics = prop.get("metrics", {})
            performance = metrics.get("performance_hydraulique", "N/A")
            print(f"   Proposition {i+1}: Performance = {performance}")

if __name__ == "__main__":
    analyze_prop_results()
    check_specific_issues()
