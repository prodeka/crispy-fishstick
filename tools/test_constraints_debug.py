#!/usr/bin/env python3
"""
Script de test pour déboguer les contraintes et l'algorithme génétique.
"""

import sys
import subprocess
from pathlib import Path

def test_constraints_debug():
    """Teste les contraintes avec des valeurs plus permissives."""
    
    print("🧪 TEST DE DÉBOGAGE DES CONTRAINTES")
    print("=" * 50)
    
    # Test avec des contraintes très permissives (respectant les contraintes Pydantic)
    cmd = [
        sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
        "bismark_inp.inp",
        "--method", "genetic",
        "--generations", "10",  # Minimum Pydantic
        "--population", "20",   # Minimum Pydantic
        "--solver", "epanet",
        "--pression-min", "5.0",  # Très permissif
        "--vitesse-max", "5.0",   # Très permissif
        "--vitesse-min", "0.1",   # Très permissif
        "--output", "debug_constraints",
        "--no-log"
    ]
    
    print(f"📋 Commande: {' '.join(cmd)}")
    print(f"📁 Répertoire actuel: {Path.cwd()}")
    
    # Exécuter la commande
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        print(f"\n📊 Résultats:")
        print(f"   • Code de retour: {result.returncode}")
        print(f"   • Sortie standard: {len(result.stdout)} caractères")
        print(f"   • Erreurs: {len(result.stderr)} caractères")
        
        if result.returncode == 0:
            print("✅ Commande exécutée avec succès!")
            if result.stdout:
                print(f"📄 Sortie: {result.stdout[:500]}...")
        else:
            print("❌ Commande échouée!")
            if result.stderr:
                print(f"⚠️ Erreurs: {result.stderr[:500]}...")
                
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏱️ Timeout après 300s")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    success = test_constraints_debug()
    sys.exit(0 if success else 1)
