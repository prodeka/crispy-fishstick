#!/usr/bin/env python3
"""
Script de test pour vérifier que la commande lcpi fonctionne depuis la racine du projet.
"""

import subprocess
import sys
from pathlib import Path

def test_lcpi_from_root():
    """Teste la commande lcpi depuis la racine du projet."""
    
    print("🧪 TEST DE LA COMMANDE LCPI DEPUIS LA RACINE")
    print("=" * 60)
    
    # Test de la commande lcpi --help
    print("📋 Test 1: lcpi --help")
    try:
        result = subprocess.run(["lcpi", "--help"], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Commande lcpi --help fonctionne")
            print(f"   • Sortie: {len(result.stdout)} caractères")
        else:
            print("❌ Commande lcpi --help échouée")
            print(f"   • Erreur: {result.stderr}")
    except FileNotFoundError:
        print("❌ Commande lcpi non trouvée - vérifier l'installation")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False
    
    # Test de la commande lcpi aep --help
    print("\n📋 Test 2: lcpi aep --help")
    try:
        result = subprocess.run(["lcpi", "aep", "--help"], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Commande lcpi aep --help fonctionne")
            print(f"   • Sortie: {len(result.stdout)} caractères")
        else:
            print("❌ Commande lcpi aep --help échouée")
            print(f"   • Erreur: {result.stderr}")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False
    
    # Test de la commande lcpi aep network-optimize-unified --help
    print("\n📋 Test 3: lcpi aep network-optimize-unified --help")
    try:
        result = subprocess.run(["lcpi", "aep", "network-optimize-unified", "--help"], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Commande lcpi aep network-optimize-unified --help fonctionne")
            print(f"   • Sortie: {len(result.stdout)} caractères")
        else:
            print("❌ Commande lcpi aep network-optimize-unified --help échouée")
            print(f"   • Erreur: {result.stderr}")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False
    
    print("\n🎉 Tests terminés avec succès!")
    return True

if __name__ == "__main__":
    success = test_lcpi_from_root()
    sys.exit(0 if success else 1)
