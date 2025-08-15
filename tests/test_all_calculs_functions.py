#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test complet pour toutes les fonctions de calcul métier
Vérifie les imports, crée des tests YAML et teste les transformations CSV
"""

import sys
import os
import yaml
import json
import pandas as pd
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, 'src')

def test_imports():
    """Teste tous les imports des fonctions de calcul métier"""
    print("=== TEST DES IMPORTS ===")
    
    imports_to_test = [
        # Bois
        ("lcpi.bois.calculs", "verifier_section_bois"),
        ("lcpi.bois.calculs", "verifier_traction_bois"),
        
        # CM (Construction Métallique)
        ("lcpi.cm.calculs", "trouver_profil_acier"),
        ("lcpi.cm.calculs", "charger_profils_acier"),
        
        # Calculs généraux
        ("lcpi.calculs", "calculer_sollicitations_completes"),
        ("lcpi.calculs", "charger_psi_coeffs"),
        
        # Hydrodrain
        ("lcpi.hydrodrain.calculs.canal", "dimensionner_canal"),
        ("lcpi.hydrodrain.calculs.bassin_versant", "caracteriser_bassin"),
        ("lcpi.hydrodrain.calculs.pluviometrie", "analyser_donnees_brutes"),
        ("lcpi.hydrodrain.calculs.pompage", "predimensionner_pompe"),
        ("lcpi.hydrodrain.calculs.plomberie", "dimensionner_troncon_plomberie"),
        ("lcpi.hydrodrain.calculs.deversoir", "dimensionner_deversoir"),
        ("lcpi.hydrodrain.calculs.dalot", "verifier_dalot"),
        ("lcpi.hydrodrain.calculs.radier", "dimensionner_radier_submersible"),
        ("lcpi.hydrodrain.calculs.population", "prevoir_population"),
        ("lcpi.hydrodrain.calculs.demande_eau", "estimer_demande_eau"),
        ("lcpi.hydrodrain.calculs.climat", "generer_diagramme_ombrothermique"),
        ("lcpi.hydrodrain.calculs.assainissement_gravitaire", "dimensionner_reseau_eaux_usees"),
        ("lcpi.hydrodrain.calculs.reservoir_aep", "dimensionner_reservoir_equilibrage"),
        
        # Béton
        ("lcpi.beton.core.materials", "Beton"),
        ("lcpi.beton.core.materials", "Acier"),
        ("lcpi.beton.core.sections", "SectionRectangulaire"),
        ("lcpi.beton.core.design.column_design", "design_rectangular_column"),
    ]
    
    failed_imports = []
    
    for module_name, function_name in imports_to_test:
        try:
            module = __import__(module_name, fromlist=[function_name])
            function = getattr(module, function_name)
            print(f"✅ {module_name}.{function_name}")
        except Exception as e:
            print(f"❌ {module_name}.{function_name} - {e}")
            failed_imports.append((module_name, function_name, str(e)))
    
    if failed_imports:
        print(f"\n⚠️  {len(failed_imports)} imports ont échoué")
        return False
    else:
        print("\n✅ Tous les imports sont OK")
        return True

def create_test_yaml_files():
    """Crée des fichiers YAML de test pour chaque module"""
    print("\n=== CRÉATION DES FICHIERS YAML DE TEST ===")
    
    # Test Bois
    bois_test = {
        "type": "poutre_bois",
        "section": {
            "largeur_b_mm": 100,
            "hauteur_h_mm": 200
        },
        "longueur_m": 4.0,
        "sollicitations": {
            "M_Ed_kNm": 15.0,
            "V_Ed_kN": 20.0,
            "p_ser_kN_m": 8.0
        },
        "materiau": {
            "classe_bois": "C24",
            "classe_service": "classe_2",
            "duree_charge": "moyen_terme"
        }
    }
    
    # Test CM
    cm_test = {
        "type": "poutre_acier",
        "sollicitations": {
            "M_Ed_kNm": 50.0,
            "V_Ed_kN": 80.0,
            "p_ser_kN_m": 25.0
        },
        "longueur_m": 6.0,
        "materiau": {
            "famille_profil": "IPE",
            "nuance": "S235",
            "fy_MPa": 235
        }
    }
    
    # Test Hydrodrain - Canal
    hydro_canal_test = {
        "type": "canal",
        "geometrie": {
            "largeur_fond_m": 2.0,
            "hauteur_m": 1.5,
            "pente_longitudinale": 0.002,
            "rugosite_manning": 0.013
        },
        "debit_m3_s": 5.0,
        "type_section": "trapezoidale",
        "pente_talus": 1.5
    }
    
    # Test Hydrodrain - Bassin versant
    hydro_bassin_test = {
        "type": "bassin_versant",
        "surface_km2": 25.0,
        "longueur_cheminement_km": 8.0,
        "pente_moyenne": 0.05,
        "coefficient_de_ruissellement": 0.7,
        "intensite_pluie_mm_h": 50.0
    }
    
    # Test Béton
    beton_test = {
        "type": "poteau_beton",
        "section": {
            "largeur_b_m": 0.3,
            "hauteur_h_m": 0.3
        },
        "longueur_L_m": 3.0,
        "sollicitations": {
            "Nu_MN": 0.8,
            "Mu_MNm": 0.1
        },
        "materiau": {
            "fc28_MPa": 25.0,
            "fe_MPa": 500.0
        },
        "type_calcul": "flexion_composee",
        "k_flambement": 1.0
    }
    
    # Créer le dossier de test
    test_dir = Path("test_yaml_files")
    test_dir.mkdir(exist_ok=True)
    
    test_files = {
        "test_bois.yml": bois_test,
        "test_cm.yml": cm_test,
        "test_hydro_canal.yml": hydro_canal_test,
        "test_hydro_bassin.yml": hydro_bassin_test,
        "test_beton.yml": beton_test
    }
    
    for filename, data in test_files.items():
        filepath = test_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)
        print(f"✅ Créé: {filepath}")
    
    return test_dir

def test_yaml_to_csv_conversion():
    """Teste la conversion YAML vers CSV"""
    print("\n=== TEST CONVERSION YAML VERS CSV ===")
    
    test_dir = Path("test_yaml_files")
    if not test_dir.exists():
        print("❌ Dossier de test YAML non trouvé")
        return False
    
    csv_dir = Path("test_csv_files")
    csv_dir.mkdir(exist_ok=True)
    
    for yaml_file in test_dir.glob("*.yml"):
        try:
            # Lire le YAML
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Convertir en format CSV-friendly
            csv_data = flatten_dict(data)
            
            # Créer le CSV
            csv_file = csv_dir / f"{yaml_file.stem}.csv"
            df = pd.DataFrame([csv_data])
            df.to_csv(csv_file, index=False, encoding='utf-8')
            
            print(f"✅ {yaml_file.name} → {csv_file.name}")
            
        except Exception as e:
            print(f"❌ Erreur conversion {yaml_file.name}: {e}")
    
    return True

def flatten_dict(d, parent_key='', sep='_'):
    """Aplatit un dictionnaire imbriqué pour CSV"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def test_calcul_functions():
    """Teste les fonctions de calcul avec les données de test"""
    print("\n=== TEST DES FONCTIONS DE CALCUL ===")
    
    try:
        # Test Bois
        from lcpi.bois.calculs import verifier_section_bois
        result_bois = verifier_section_bois(
            b=100, h=200, longueur=4.0,
            sollicitations={"M_Ed": 15.0, "p_ser": 8.0},
            classe_bois="C24", classe_service="classe_2", duree_charge="moyen_terme",
            verbose=False
        )
        print(f"✅ Test bois: {type(result_bois)}")
        
        # Test CM
        from lcpi.cm.calculs import trouver_profil_acier
        result_cm = trouver_profil_acier(
            M_Ed_kNm=50.0, V_Ed_kN=80.0, longueur=6.0, p_ser_kN_m=25.0,
            famille_profil="IPE", verbose=False
        )
        print(f"✅ Test CM: {type(result_cm)}")
        
        # Test Hydrodrain
        from lcpi.hydrodrain.calculs.canal import dimensionner_canal
        result_hydro = dimensionner_canal({
            "debit_projet_m3s": 5.0,
            "pente_m_m": 0.002,
            "k_strickler": 80.0,
            "fruit_talus_m_m": 1.5,
            "vitesse_imposee_ms": 1.5
        })
        print(f"✅ Test Hydrodrain: {type(result_hydro)}")
        
        # Test Calculs généraux
        from lcpi.calculs import calculer_sollicitations_completes
        result_calc = calculer_sollicitations_completes(
            longueur=6.0, charges_list=[{"type": "uniforme", "valeur": 10.0}],
            materiau="acier", categorie_usage="bureaux", verbose=False
        )
        print(f"✅ Test calculs généraux: {type(result_calc)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test fonctions: {e}")
        return False

def create_repl_test_script():
    """Crée un script pour tester dans le REPL"""
    print("\n=== CRÉATION DU SCRIPT REPL ===")
    
    repl_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test REPL pour toutes les fonctions de calcul métier
Usage: python -i repl_test.py
"""

import sys
import os
import yaml
import json
import pandas as pd
from pathlib import Path

# Configuration du path
sys.path.insert(0, 'src')

# Imports des fonctions de calcul
print("Chargement des fonctions de calcul...")

# Bois
from lcpi.bois.calculs import verifier_section_bois, verifier_traction_bois
print("✅ Bois: verifier_section_bois, verifier_traction_bois")

# CM
from lcpi.cm.calculs import trouver_profil_acier, charger_profils_acier
print("✅ CM: trouver_profil_acier, charger_profils_acier")

# Calculs généraux
from lcpi.calculs import calculer_sollicitations_completes, charger_psi_coeffs
print("✅ Calculs: calculer_sollicitations_completes, charger_psi_coeffs")

# Hydrodrain
from lcpi.hydrodrain.calculs.canal import dimensionner_canal
from lcpi.hydrodrain.calculs.bassin_versant import caracteriser_bassin
from lcpi.hydrodrain.calculs.pluviometrie import analyser_donnees_brutes
from lcpi.hydrodrain.calculs.pompage import predimensionner_pompe
from lcpi.hydrodrain.calculs.plomberie import dimensionner_troncon_plomberie
from lcpi.hydrodrain.calculs.deversoir import dimensionner_deversoir
from lcpi.hydrodrain.calculs.dalot import verifier_dalot
from lcpi.hydrodrain.calculs.radier import dimensionner_radier_submersible
from lcpi.hydrodrain.calculs.population import prevoir_population
from lcpi.hydrodrain.calculs.demande_eau import estimer_demande_eau
from lcpi.hydrodrain.calculs.climat import generer_diagramme_ombrothermique
print("✅ Hydrodrain: toutes les fonctions")

# Béton
from lcpi.beton.core.materials import Beton, Acier
from lcpi.beton.core.sections import SectionRectangulaire
from lcpi.beton.core.design.column_design import design_rectangular_column
print("✅ Béton: Beton, Acier, SectionRectangulaire, design_rectangular_column")

print("\\n=== FONCTIONS DISPONIBLES ===")
print("Bois:")
print("  - verifier_section_bois(b, h, longueur, sollicitations, classe_bois, classe_service, duree_charge)")
print("  - verifier_traction_bois(b, h, effort_N_daN, classe_bois, classe_service, duree_charge)")
print("\\nCM:")
print("  - trouver_profil_acier(M_Ed_kNm, V_Ed_kN, longueur, p_ser_kN_m, famille_profil='IPE')")
print("  - charger_profils_acier()")
print("\\nHydrodrain:")
print("  - dimensionner_canal(largeur_fond_m, hauteur_m, pente_longitudinale, debit_m3_s)")
print("  - caracteriser_bassin(surface_km2, longueur_cheminement_km, pente_moyenne)")
print("  - predimensionner_pompe(debit_m3_h, hauteur_manometrique_m)")
print("\\nBéton:")
print("  - design_rectangular_column(Nu_MN, Mu_MNm, section, beton, acier, height, k_factor)")
print("\\nCalculs généraux:")
print("  - calculer_sollicitations_completes(longueur, charges_list, materiau, categorie_usage)")

print("\\n=== EXEMPLES D'UTILISATION ===")
print("# Test bois:")
print("result = verifier_section_bois(100, 200, 4.0, {'M_Ed': 15.0, 'p_ser': 8.0}, 'C24', 'classe_2', 'moyen_terme')")
print("\\n# Test CM:")
print("result = trouver_profil_acier(50.0, 80.0, 6.0, 25.0, 'IPE')")
print("\\n# Test Hydrodrain:")
print("result = dimensionner_canal(2.0, 1.5, 0.002, 5.0, 'trapezoidale', 1.5)")

print("\\n=== REPL PRÊT ===")
print("Vous pouvez maintenant tester les fonctions de calcul métier!")
'''
    
    with open("repl_test.py", 'w', encoding='utf-8') as f:
        f.write(repl_script)
    
    print("✅ Script REPL créé: repl_test.py")
    return True

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DES TESTS COMPLETS")
    print("=" * 50)
    
    # Test 1: Imports
    imports_ok = test_imports()
    
    # Test 2: Création YAML
    yaml_ok = create_test_yaml_files()
    
    # Test 3: Conversion CSV
    csv_ok = test_yaml_to_csv_conversion()
    
    # Test 4: Fonctions de calcul
    calc_ok = test_calcul_functions()
    
    # Test 5: Script REPL
    repl_ok = create_repl_test_script()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    print(f"Imports: {'✅' if imports_ok else '❌'}")
    print(f"YAML: {'✅' if yaml_ok else '❌'}")
    print(f"CSV: {'✅' if csv_ok else '❌'}")
    print(f"Calculs: {'✅' if calc_ok else '❌'}")
    print(f"REPL: {'✅' if repl_ok else '❌'}")
    
    if all([imports_ok, yaml_ok, csv_ok, calc_ok, repl_ok]):
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("Vous pouvez maintenant utiliser: python -i repl_test.py")
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")

if __name__ == "__main__":
    main() 