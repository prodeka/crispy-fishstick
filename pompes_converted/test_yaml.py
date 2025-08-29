#!/usr/bin/env python3
"""
Test du fichier YAML généré
"""

import yaml

def test_yaml():
    """Teste le fichier YAML généré"""
    try:
        with open('grundfos_pompes_230_modeles_complet_converted.yaml', 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        
        print("📄 TEST DU FICHIER YAML")
        print("=" * 40)
        
        # Métadonnées
        metadata = data.get('metadata', {})
        print(f"📊 Source: {metadata.get('source', 'N/A')}")
        print(f"📅 Date: {metadata.get('conversion_date', 'N/A')}")
        print(f"🔢 Total pompes: {metadata.get('total_pompes', 'N/A')}")
        print(f"📋 Version: {metadata.get('format_version', 'N/A')}")
        
        # Première pompe
        if data.get('pompes'):
            first_pump = data['pompes'][0]
            print(f"\n💧 Première pompe:")
            print(f"  Désignation: {first_pump.get('designation', 'N/A')}")
            print(f"  Marque: {first_pump.get('marque', 'N/A')}")
            print(f"  Débit: {first_pump.get('debit_exploitation_m3h_min', 'N/A')}-{first_pump.get('debit_exploitation_m3h_max', 'N/A')} m³/h")
            print(f"  HMT: {first_pump.get('hmt_min_m', 'N/A')}-{first_pump.get('hmt_max_m', 'N/A')}m")
            print(f"  CAPEX: {first_pump.get('capex_estime_eur', 'N/A')}€")
        
        # Statistiques
        pompes = data.get('pompes', [])
        print(f"\n📈 Statistiques:")
        print(f"  Total pompes: {len(pompes)}")
        
        # Vérifier quelques champs
        marques = set(p.get('marque') for p in pompes if p.get('marque'))
        types_moteur = set(p.get('type_moteur') for p in pompes if p.get('type_moteur'))
        
        print(f"  Marques: {', '.join(marques)}")
        print(f"  Types moteur: {len(types_moteur)} types différents")
        
        print("\n✅ Test YAML réussi!")
        
    except Exception as e:
        print(f"❌ Erreur lors du test YAML: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_yaml()
