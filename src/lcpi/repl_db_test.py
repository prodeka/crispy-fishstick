#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test REPL pour toutes les fonctions de calcul métier ET les bases de données
Usage: python -i repl_db_test.py
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

# Base de données
from lcpi.db_manager import db_manager, search_bois_cli, compare_materials_cli, export_data_cli, sql_query_cli
print("✅ Base de données: db_manager, search_bois_cli, compare_materials_cli, export_data_cli, sql_query_cli")

print("\n=== FONCTIONS DE CALCUL DISPONIBLES ===")
print("Bois:")
print("  - verifier_section_bois(b, h, longueur, sollicitations, classe_bois, classe_service, duree_charge)")
print("  - verifier_traction_bois(b, h, effort_N_daN, classe_bois, classe_service, duree_charge)")
print("\nCM:")
print("  - trouver_profil_acier(M_Ed_kNm, V_Ed_kN, longueur, p_ser_kN_m, famille_profil='IPE')")
print("  - charger_profils_acier()")
print("\nHydrodrain:")
print("  - dimensionner_canal(donnees_dict)")
print("  - caracteriser_bassin(donnees_dict)")
print("  - predimensionner_pompe(donnees_dict)")
print("\nBéton:")
print("  - design_rectangular_column(Nu_MN, Mu_MNm, section, beton, acier, height, k_factor)")
print("\nCalculs généraux:")
print("  - calculer_sollicitations_completes(longueur, charges_list, materiau, categorie_usage)")

print("\n=== FONCTIONS BASE DE DONNÉES DISPONIBLES ===")
print("Recherche:")
print("  - db_manager.search_bois_by_class('C24')")
print("  - db_manager.search_bois_by_property('fm_k_MPa', min_value=20)")
print("  - search_bois_cli(classe='C24')")
print("  - search_bois_cli(propriete='fm_k_MPa', min_val=20)")
print("\nComparaison:")
print("  - db_manager.compare_materials(['C24', 'C30'])")
print("  - compare_materials_cli(['C24', 'C30'])")
print("\nInformations:")
print("  - db_manager.get_material_info('C24')")
print("\nExport:")
print("  - db_manager.export_to_csv(data, 'export.csv')")
print("  - export_data_cli('bois_classes', 'bois_data.csv')")
print("\nSQL:")
print("  - db_manager.create_sqlite_db('cm_bois', 'cm_bois_sqlite')")
print("  - db_manager.query_sql('cm_bois_sqlite', 'SELECT * FROM table')")
print("  - sql_query_cli('cm_bois_sqlite', 'SELECT Classe, fm_k_MPa FROM table')")

print("\n=== EXEMPLES D'UTILISATION ===")
print("# Test calcul bois:")
print("result = verifier_section_bois(100, 200, 4.0, {'M_Ed': 15.0, 'p_ser': 8.0}, 'C24', 'classe_2', 'moyen_terme')")
print("\n# Test calcul CM:")
print("result = trouver_profil_acier(50.0, 80.0, 6.0, 25.0, 'IPE')")
print("\n# Test calcul Hydrodrain:")
print("result = dimensionner_canal({'debit_projet_m3s': 5.0, 'pente_m_m': 0.002, 'k_strickler': 80.0, 'fruit_talus_m_m': 1.5, 'vitesse_imposee_ms': 1.5})")
print("\n# Test base de données:")
print("result = db_manager.search_bois_by_class('C24')")
print("result = db_manager.get_material_info('C24')")
print("result = db_manager.compare_materials(['C24', 'C30'])")

print("\n=== REPL PRÊT ===")
print("Vous pouvez maintenant tester les fonctions de calcul métier ET interroger les bases de données!")
print("\n💡 Conseils:")
print("  - Utilisez db_manager pour accéder aux bases de données")
print("  - Utilisez les fonctions CLI pour des affichages formatés")
print("  - Convertissez en SQLite pour des requêtes SQL complexes")
print("  - Exportez en CSV pour l'analyse externe") 