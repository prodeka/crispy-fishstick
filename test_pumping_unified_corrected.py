#!/usr/bin/env python3
"""
Test spécifique pour vérifier les calculs de puissance et d'énergie dans pumping_unified
"""

import sys
import os

# Ajouter le chemin pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_pumping_unified_calculs():
    """Test des calculs de puissance et d'énergie dans pumping_unified"""
    print("🔵 TEST CALCULS POMPAGE UNIFIÉ")
    print("=" * 60)
    print("Ce test vérifie que tous les calculs de puissance et d'énergie sont présents.")
    print("=" * 60)
    
    try:
        from lcpi.aep.calculations.pumping_unified import dimension_pumping_unified
        
        # Données de test
        data = {
            "debit_m3h": 100,  # 100 m³/h
            "hmt_m": 50,       # 50 m de HMT
            "type_pompe": "centrifuge",
            "rendement_pompe": 0.75
        }
        
        print(f"📊 DONNÉES DE TEST:")
        print(f"   Débit: {data['debit_m3h']} m³/h")
        print(f"   HMT: {data['hmt_m']} m")
        print(f"   Type de pompe: {data['type_pompe']}")
        print(f"   Rendement: {data['rendement_pompe']}")
        
        # Test du dimensionnement
        resultat = dimension_pumping_unified(data, verbose=True)
        
        if resultat['statut'] == 'SUCCES':
            pompage = resultat['pompage']
            
            print(f"\n✅ RÉSULTATS DU DIMENSIONNEMENT:")
            print(f"   Débit: {pompage['debit_m3h']} m³/h ({pompage['debit_m3s']:.3f} m³/s)")
            print(f"   HMT: {pompage['hmt_m']} m")
            print(f"   Type de pompe: {pompage['type_pompe']}")
            print(f"   Rendement: {pompage['rendement_pompe']}")
            
            # Vérification des calculs de puissance
            print(f"\n⚡ CALCULS DE PUISSANCE:")
            if 'puissance_hydraulique_kw' in pompage:
                print(f"   ✅ Puissance hydraulique: {pompage['puissance_hydraulique_kw']:.2f} kW")
            else:
                print(f"   ❌ Puissance hydraulique: MANQUANTE")
            
            if 'puissance_electrique_kw' in pompage:
                print(f"   ✅ Puissance électrique: {pompage['puissance_electrique_kw']:.2f} kW")
            else:
                print(f"   ❌ Puissance électrique: MANQUANTE")
            
            if 'puissance_groupe_kva' in pompage:
                print(f"   ✅ Puissance groupe: {pompage['puissance_groupe_kva']:.2f} kVA")
            else:
                print(f"   ❌ Puissance groupe: MANQUANTE")
            
            # Vérification des calculs d'énergie
            print(f"\n💡 CALCULS D'ÉNERGIE:")
            if 'energie_kwh' in pompage:
                print(f"   ✅ Énergie consommée: {pompage['energie_kwh']:.1f} kWh")
            else:
                print(f"   ❌ Énergie consommée: MANQUANTE")
            
            if 'cout_euros' in pompage:
                print(f"   ✅ Coût journalier: {pompage['cout_euros']:.2f} €")
            else:
                print(f"   ❌ Coût journalier: MANQUANT")
            
            # Vérification des contraintes
            print(f"\n🔍 VÉRIFICATIONS:")
            contraintes = resultat.get('contraintes', {})
            for contrainte, valeur in contraintes.items():
                status = "✅" if valeur else "❌"
                print(f"   {status} {contrainte}: {valeur}")
            
            # Vérification des recommandations
            print(f"\n💡 RECOMMANDATIONS:")
            recommandations = resultat.get('recommandations', [])
            if recommandations:
                for rec in recommandations:
                    print(f"   • {rec}")
            else:
                print(f"   Aucune recommandation")
            
            # Test de validation
            champs_requis = [
                'puissance_hydraulique_kw',
                'puissance_electrique_kw', 
                'puissance_groupe_kva',
                'energie_kwh',
                'cout_euros'
            ]
            
            champs_manquants = [champ for champ in champs_requis if champ not in pompage]
            
            if champs_manquants:
                print(f"\n❌ CHAMPS MANQUANTS:")
                for champ in champs_manquants:
                    print(f"   • {champ}")
                return False
            else:
                print(f"\n✅ TOUS LES CALCULS SONT PRÉSENTS!")
                return True
                
        else:
            print(f"❌ Erreur: {resultat['message']}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_comparaison_types_pompes():
    """Test de la comparaison des types de pompes"""
    print(f"\n🔵 TEST COMPARAISON TYPES DE POMPES")
    print("-" * 40)
    
    try:
        from lcpi.aep.calculations.pumping_unified import comparer_types_pompes_unified
        
        data = {
            "debit_m3s": 0.05,  # 50 L/s
            "hmt_m": 30         # 30 m de HMT
        }
        
        resultat = comparer_types_pompes_unified(data)
        
        if 'analyse' in resultat:
            analyse = resultat['analyse']
            print(f"✅ Comparaison réussie:")
            print(f"   Type min puissance: {analyse['type_min_puissance']}")
            print(f"   Type max rendement: {analyse['type_max_rendement']}")
            print(f"   Puissance min: {analyse['puissance_min']:.2f} kW")
            print(f"   Puissance max: {analyse['puissance_max']:.2f} kW")
            print(f"   Rendement max: {analyse['rendement_max']:.2f}")
            return True
        else:
            print(f"❌ Erreur: {resultat.get('message', 'Erreur inconnue')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_cout_energie():
    """Test du calcul de coût énergétique"""
    print(f"\n🔵 TEST COÛT ÉNERGÉTIQUE")
    print("-" * 40)
    
    try:
        from lcpi.aep.calculations.pumping_unified import calculer_cout_energie_pompage_unified
        
        data = {
            "puissance_electrique_kw": 15.0,
            "temps_fonctionnement_h": 24.0,
            "prix_kwh": 0.15
        }
        
        resultat = calculer_cout_energie_pompage_unified(data)
        
        if 'energie_kwh' in resultat and 'cout_euros' in resultat:
            print(f"✅ Calcul de coût réussi:")
            print(f"   Énergie consommée: {resultat['energie_kwh']:.1f} kWh")
            print(f"   Coût journalier: {resultat['cout_euros']:.2f} €")
            return True
        else:
            print(f"❌ Erreur: {resultat.get('message', 'Erreur inconnue')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST CALCULS POMPAGE UNIFIÉ")
    print("=" * 60)
    
    # Tests
    test1 = test_pumping_unified_calculs()
    test2 = test_comparaison_types_pompes()
    test3 = test_cout_energie()
    
    # Résumé
    print(f"\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    tests = [
        ("Calculs de puissance et énergie", test1),
        ("Comparaison types de pompes", test2),
        ("Calcul coût énergétique", test3)
    ]
    
    success_count = 0
    for test_name, result in tests:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n📈 Résultat global: {success_count}/{len(tests)} tests réussis")
    
    if success_count == len(tests):
        print("🎉 Tous les calculs de pompage sont corrects !")
        print("✅ Les calculs de puissance et d'énergie sont bien restaurés.")
        return True
    else:
        print("⚠️ Certains calculs de pompage ont échoué.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 