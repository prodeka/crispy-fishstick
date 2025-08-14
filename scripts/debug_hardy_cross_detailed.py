#!/usr/bin/env python3
"""Debug détaillé Hardy-Cross - Analyse des calculs"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lcpi.aep.calculations.hardy_cross_enhanced import HardyCrossEnhanced
import sys
sys.path.append('scripts')
from generate_paris_network import ParisNetworkGenerator

def debug_hardy_cross_detailed():
    """Debug détaillé Hardy-Cross"""
    
    print("🔍 Debug détaillé Hardy-Cross")
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
    
    # Créer l'analyseur
    analyzer = HardyCrossEnhanced()
    
    # Identifier les boucles
    boucles = analyzer._identify_loops_robust(hardy_cross_data["troncons"])
    print(f"🔍 Boucles détectées : {len(boucles)}")
    
    # Analyser la première boucle
    if boucles:
        premiere_boucle = boucles[0]
        print(f"\n🔍 Analyse de la première boucle : {premiere_boucle}")
        
        # Vérifier les tronçons de cette boucle
        for i in range(len(premiere_boucle)):
            noeud_actuel = premiere_boucle[i]
            noeud_suivant = premiere_boucle[(i + 1) % len(premiere_boucle)]
            
            # Chercher le tronçon
            troncon_trouve = None
            for troncon in hardy_cross_data["troncons"]:
                if ((troncon.get('noeud_amont') == noeud_actuel and 
                     troncon.get('noeud_aval') == noeud_suivant) or
                    (troncon.get('noeud_amont') == noeud_suivant and 
                     troncon.get('noeud_aval') == noeud_actuel)):
                    troncon_trouve = troncon
                    break
            
            if troncon_trouve:
                print(f"   Tronçon {i+1} : {noeud_actuel} → {noeud_suivant}")
                print(f"     - Débit initial : {troncon_trouve.get('debit_initial', 0)}")
                print(f"     - Longueur : {troncon_trouve.get('longueur', 0)}")
                print(f"     - Diamètre : {troncon_trouve.get('diametre', 0)}")
                print(f"     - Rugosité : {troncon_trouve.get('coefficient_rugosite', 0)}")
            else:
                print(f"   ❌ Tronçon {i+1} : {noeud_actuel} → {noeud_suivant} NON TROUVÉ")
    
    # Simuler une itération Hardy-Cross
    print(f"\n🔧 Simulation d'une itération Hardy-Cross...")
    
    # Initialiser les débits
    debits = {}
    for t in hardy_cross_data["troncons"]:
        key = f"{t['noeud_amont']}-{t['noeud_aval']}"
        debits[key] = t['debit_initial']
    
    # Calculer les coefficients K
    coefficients_K = {}
    for troncon in hardy_cross_data["troncons"]:
        key = f"{troncon['noeud_amont']}-{troncon['noeud_aval']}"
        K = analyzer.calculate_resistance_coefficient(
            troncon['longueur'],
            troncon['diametre'],
            troncon['coefficient_rugosite']
        )
        coefficients_K[key] = K
    
    print(f"   - Débits initialisés : {len(debits)}")
    print(f"   - Coefficients K calculés : {len(coefficients_K)}")
    
    # Analyser la première boucle
    if boucles:
        boucle = boucles[0]
        print(f"\n🔍 Calcul pour la boucle : {boucle}")
        
        somme_KQ = 0
        somme_K = 0
        
        for j in range(len(boucle)):
            noeud_actuel = boucle[j]
            noeud_suivant = boucle[(j + 1) % len(boucle)]
            
            # Trouver le tronçon
            troncon_key = f"{noeud_actuel}-{noeud_suivant}"
            if troncon_key not in debits:
                troncon_key = f"{noeud_suivant}-{noeud_actuel}"
            
            if troncon_key in debits:
                Q = debits[troncon_key]
                K = coefficients_K.get(troncon_key, 0)
                
                # Déterminer le signe
                signe = 1 if troncon_key == f"{noeud_actuel}-{noeud_suivant}" else -1
                
                terme_KQ = signe * K * Q * abs(Q)**0.85
                terme_K = K * abs(Q)**0.85
                
                somme_KQ += terme_KQ
                somme_K += terme_K
                
                print(f"   Tronçon {j+1} : {noeud_actuel} → {noeud_suivant}")
                print(f"     - Q = {Q:.4f}, K = {K:.4f}")
                print(f"     - Signe = {signe}")
                print(f"     - Terme KQ = {terme_KQ:.4f}")
                print(f"     - Terme K = {terme_K:.4f}")
        
        print(f"\n📊 Résultats pour la boucle :")
        print(f"   - Σ(KQ|Q|^0.85) = {somme_KQ:.4f}")
        print(f"   - Σ(K|Q|^0.85) = {somme_K:.4f}")
        
        if somme_K != 0:
            delta_Q = -somme_KQ / (1.85 * somme_K)
            print(f"   - ΔQ = {delta_Q:.6f}")
        else:
            print(f"   - ΔQ = 0 (somme_K = 0)")
    
    return True

if __name__ == "__main__":
    success = debug_hardy_cross_detailed()
    if success:
        print("\n✅ Debug détaillé terminé !")
    else:
        print("\n❌ Debug détaillé : problème détecté")
        sys.exit(1) 