#!/usr/bin/env python3
"""
Script de test simple pour vérifier que la commande CLI fonctionne correctement.
"""

import subprocess
import sys
from pathlib import Path

def test_simple_command():
    """Teste la commande CLI avec des paramètres simples."""
    
    print("🧪 TEST SIMPLE DE LA COMMANDE CLI")
    print("=" * 40)
    
    # Paramètres de test
    input_file = "bismark_inp.inp"
    generations = 15
    population = 25
    tolerance = 1e-5
    max_iterations = 150
    solver = "epanet"
    output = "test_simple_output"
    
    # Commande de test
    cmd = [
        sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
        input_file,
        "--method", "genetic",
        "--generations", str(generations),
        "--population", str(population),
        "--tolerance", str(tolerance),
        "--max-iterations", str(max_iterations),
        "--solver", solver,
        "--output", output,
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
                print(f"📄 Sortie: {result.stdout[:200]}...")
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
    success = test_simple_command()
    sys.exit(0 if success else 1)
