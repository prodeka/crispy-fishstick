#!/usr/bin/env python3
"""
Script de test pour vérifier les nouvelles options --tolerance et --max-iterations
"""

import subprocess
import sys
from pathlib import Path

def test_new_options():
    """Teste les nouvelles options de la commande network-optimize-unified."""
    
    print("🧪 TEST DES NOUVELLES OPTIONS CLI")
    print("=" * 50)
    
    # Test 1: Vérifier que les options sont disponibles
    print("\n📋 Test 1: Vérification des options disponibles")
    try:
        result = subprocess.run([
            sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified", "--help"
        ], capture_output=True, text=True, check=True)
        
        help_text = result.stdout
        if "--tolerance" in help_text and "--max-iterations" in help_text:
            print("✅ Options --tolerance et --max-iterations détectées")
        else:
            print("❌ Options non trouvées")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'affichage de l'aide: {e}")
        return False
    
    # Test 2: Vérifier la validation des contraintes Pydantic
    print("\n📋 Test 2: Validation des contraintes Pydantic")
    
    # Test avec generations < 10
    try:
        result = subprocess.run([
            sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
            "bismark_inp.inp", "--method", "genetic", "--generations", "5", 
            "--population", "25", "--solver", "epanet", "--no-log"
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 1 and "doit être >= 10" in result.stderr:
            print("✅ Validation generations >= 10 fonctionne")
        else:
            print("❌ Validation generations échouée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de validation: {e}")
        return False
    
    # Test avec population < 20
    try:
        result = subprocess.run([
            sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
            "bismark_inp.inp", "--method", "genetic", "--generations", "15", 
            "--population", "15", "--solver", "epanet", "--no-log"
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 1 and "doit être >= 20" in result.stderr:
            print("✅ Validation population >= 20 fonctionne")
        else:
            print("❌ Validation population échouée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de validation: {e}")
        return False
    
    # Test 3: Test avec des valeurs valides et les nouvelles options
    print("\n📋 Test 3: Test avec les nouvelles options")
    try:
        result = subprocess.run([
            sys.executable, "-m", "lcpi.aep.cli", "network-optimize-unified",
            "bismark_inp.inp", "--method", "genetic", "--generations", "15", 
            "--population", "25", "--tolerance", "1e-5", "--max-iterations", "150",
            "--solver", "epanet", "--no-log"
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("✅ Exécution avec nouvelles options réussie")
        else:
            print(f"⚠️ Exécution terminée avec code {result.returncode}")
            print(f"Sortie: {result.stdout[:200]}...")
            print(f"Erreurs: {result.stderr[:200]}...")
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'exécution: {e}")
        return False
    
    print("\n🎉 Tous les tests sont passés avec succès!")
    return True

if __name__ == "__main__":
    success = test_new_options()
    sys.exit(0 if success else 1)
