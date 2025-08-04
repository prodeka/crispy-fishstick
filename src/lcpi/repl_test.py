#!/usr/bin/env python3
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

print("\n=== FONCTIONS DISPONIBLES ===")
print("Bois:")
print("  - verifier_section_bois(b, h, longueur, sollicitations, classe_bois, classe_service, duree_charge)")
print("  - verifier_traction_bois(b, h, effort_N_daN, classe_bois, classe_service, duree_charge)")
print("\nCM:")
print("  - trouver_profil_acier(M_Ed_kNm, V_Ed_kN, longueur, p_ser_kN_m, famille_profil='IPE')")
print("  - charger_profils_acier()")
print("\nHydrodrain:")
print("  - dimensionner_canal(largeur_fond_m, hauteur_m, pente_longitudinale, debit_m3_s)")
print("  - caracteriser_bassin(surface_km2, longueur_cheminement_km, pente_moyenne)")
print("  - predimensionner_pompe(debit_m3_h, hauteur_manometrique_m)")
print("\nBéton:")
print("  - design_rectangular_column(Nu_MN, Mu_MNm, section, beton, acier, height, k_factor)")
print("\nCalculs généraux:")
print("  - calculer_sollicitations_completes(longueur, charges_list, materiau, categorie_usage)")

print("\n=== EXEMPLES D'UTILISATION ===")
print("# Test bois:")
print("result = verifier_section_bois(100, 200, 4.0, {'M_Ed': 15.0, 'p_ser': 8.0}, 'C24', 'classe_2', 'moyen_terme')")
print("\n# Test CM:")
print("result = trouver_profil_acier(50.0, 80.0, 6.0, 25.0, 'IPE')")
print("\n# Test Hydrodrain:")
print("result = dimensionner_canal(2.0, 1.5, 0.002, 5.0, 'trapezoidale', 1.5)")

print("\n=== REPL PRÊT ===")
print("Vous pouvez maintenant tester les fonctions de calcul métier!")
