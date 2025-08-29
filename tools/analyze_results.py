#!/usr/bin/env python3
"""Script simple pour analyser les fichiers de résultats JSON."""

import json
import sys
from pathlib import Path

def analyze_results(filename):
    """Analyse un fichier de résultats JSON."""
    
    if not Path(filename).exists():
        print(f"❌ Fichier non trouvé: {filename}")
        return
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 ANALYSE DU FICHIER: {filename}")
        print("=" * 60)
        
        print(f"🔑 Clés disponibles: {list(data.keys())}")
        
        if "proposals" in data:
            proposals = data["proposals"]
            print(f"📋 Nombre de propositions: {len(proposals)}")
            
            if proposals:
                best = proposals[0]
                print(f"\n🏆 MEILLEURE SOLUTION:")
                print(f"   💰 CAPEX: {best.get('CAPEX', 'N/A'):,.0f} FCFA")
                print(f"   ✅ Faisable: {best.get('constraints_ok', 'N/A')}")
                print(f"   📏 Pression min: {best.get('pression_min', 'N/A')} m")
                print(f"   🏃 Vitesse max: {best.get('vitesse_max', 'N/A')} m/s")
                print(f"   🐌 Vitesse min: {best.get('vitesse_min', 'N/A')} m/s")
                
                # Analyser les contraintes
                if "constraints" in best:
                    constraints = best["constraints"]
                    print(f"\n📋 CONTRAINTES:")
                    for key, value in constraints.items():
                        print(f"   {key}: {value}")
                
                # Analyser les métriques hydrauliques
                if "hydraulic_metrics" in best:
                    metrics = best["hydraulic_metrics"]
                    print(f"\n🌊 MÉTRIQUES HYDRAULIQUES:")
                    for key, value in metrics.items():
                        print(f"   {key}: {value}")
        
        # Analyser les métadonnées
        if "meta" in data:
            meta = data["meta"]
            print(f"\n📝 MÉTADONNÉES:")
            for key, value in meta.items():
                if key != "command":  # Éviter d'afficher la commande complète
                    print(f"   {key}: {value}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")

def main():
    """Fonction principale."""
    
    if len(sys.argv) < 2:
        print("Usage: python tools/analyze_results.py <fichier_resultat>")
        print("Exemple: python tools/analyze_results.py test_amelioration_lcpi")
        return
    
    filename = sys.argv[1]
    analyze_results(filename)

if __name__ == "__main__":
    main()
