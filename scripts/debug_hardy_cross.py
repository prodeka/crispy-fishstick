#!/usr/bin/env python3
"""Debug Hardy-Cross - Analyse des boucles détectées"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.calculations.hardy_cross_enhanced import hardy_cross_network_enhanced
import sys
sys.path.append('scripts')
from generate_paris_network import ParisNetworkGenerator

def debug_hardy_cross():
    """Debug Hardy-Cross pour analyser les boucles"""
    
    print("🔍 Debug Hardy-Cross - Analyse des boucles")
    print("=" * 50)
    
    # Générer réseau
    generator = ParisNetworkGenerator()
    network_data = generator.generate_network_data()
    
    # Convertir structure
    hardy_cross_data = {
        "metadata": network_data["metadata"],
        "troncons": list(network_data["network"]["pipes"].values()),
        "noeuds": list(network_data["network"]["nodes"].values())
    }
    
    print(f"📊 Réseau : {len(hardy_cross_data['troncons'])} tronçons")
    
    # Analyser les boucles détectées
    from lcpi.aep.calculations.hardy_cross_enhanced import HardyCrossEnhanced
    analyzer = HardyCrossEnhanced()
    
    boucles = analyzer._identify_loops_robust(hardy_cross_data["troncons"])
    print(f"🔍 Boucles détectées : {len(boucles)}")
    
    # Analyser la taille des boucles
    tailles = [len(b) for b in boucles]
    print(f"📏 Taille des boucles :")
    print(f"   - Min : {min(tailles) if tailles else 0}")
    print(f"   - Max : {max(tailles) if tailles else 0}")
    print(f"   - Moyenne : {sum(tailles)/len(tailles) if tailles else 0:.1f}")
    
    # Compter les boucles par taille
    from collections import Counter
    taille_counts = Counter(tailles)
    print(f"📊 Distribution des tailles :")
    for taille, count in sorted(taille_counts.items()):
        print(f"   - Taille {taille} : {count} boucles")
    
    # Afficher quelques boucles
    print(f"\n🔍 Exemples de boucles :")
    for i, boucle in enumerate(boucles[:5]):
        print(f"   Boucle {i+1} ({len(boucle)} nœuds) : {boucle}")
    
    # Vérifier les débits initiaux
    print(f"\n💧 Analyse des débits initiaux :")
    debits_avec_valeurs = 0
    debits_nuls = 0
    
    for troncon in hardy_cross_data["troncons"]:
        debit = troncon.get('debit_initial', 0)
        if debit > 0:
            debits_avec_valeurs += 1
        else:
            debits_nuls += 1
    
    print(f"   - Tronçons avec débit > 0 : {debits_avec_valeurs}")
    print(f"   - Tronçons avec débit = 0 : {debits_nuls}")
    
    # Vérifier les boucles avec débits
    boucles_avec_debits = 0
    for boucle in boucles:
        if len(boucle) >= 3:  # Taille minimale
            # Vérifier si la boucle a des débits
            a_des_debits = False
            for i in range(len(boucle)):
                noeud_actuel = boucle[i]
                noeud_suivant = boucle[(i + 1) % len(boucle)]
                
                # Chercher le tronçon
                for troncon in hardy_cross_data["troncons"]:
                    if ((troncon.get('noeud_amont') == noeud_actuel and 
                         troncon.get('noeud_aval') == noeud_suivant) or
                        (troncon.get('noeud_amont') == noeud_suivant and 
                         troncon.get('noeud_aval') == noeud_actuel)):
                        if troncon.get('debit_initial', 0) > 0:
                            a_des_debits = True
                            break
                if a_des_debits:
                    break
            
            if a_des_debits:
                boucles_avec_debits += 1
    
    print(f"   - Boucles avec débits > 0 : {boucles_avec_debits}")
    print(f"   - Boucles sans débits : {len(boucles) - boucles_avec_debits}")
    
    # Test Hardy-Cross
    print(f"\n🔧 Test Hardy-Cross...")
    try:
        results = hardy_cross_network_enhanced(
            hardy_cross_data, max_iterations=10, tolerance=1e-6
        )
        
        iterations = results.get('iterations', [])
        print(f"✅ Hardy-Cross terminé : {len(iterations)} itérations")
        print(f"   - Convergence : {results.get('convergence', False)}")
        
        if iterations:
            print(f"   - Première itération : {iterations[0]}")
        
    except Exception as e:
        print(f"❌ Erreur Hardy-Cross : {e}")
    
    return len(boucles) > 0

if __name__ == "__main__":
    success = debug_hardy_cross()
    if success:
        print("\n✅ Debug terminé avec succès !")
    else:
        print("\n❌ Debug : problème détecté")
        sys.exit(1) 