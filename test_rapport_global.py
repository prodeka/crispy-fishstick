#!/usr/bin/env python3
"""
Test du système de rapports globaux
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.lcpi.reporting.global_reports import generate_global_report, check_pandoc_availability

def test_rapport_canal():
    """Test de génération d'un rapport pour le dimensionnement de canal"""
    
    # Données d'exemple pour un canal
    data = {
        "type": "Dimensionnement Canal",
        "module": "Hydrodrain",
        "version": "2.1.0",
        "input_data": {
            "canal": {
                "nom": "Canal principal d'irrigation",
                "geometrie": {
                    "type": "trapezoidal",
                    "largeur_fond": 2.0,
                    "pente_talus": 1.5,
                    "profondeur": 1.2
                },
                "hydraulique": {
                    "debit_design": 5.0,
                    "pente_longitudinale": 0.001,
                    "coefficient_rugosite": 0.025
                }
            }
        },
        "results": {
            "statut": "OK",
            "type_canal": "trapezoidal",
            "hauteur_eau": 1.751,
            "largeur_fond": 1.06,
            "largeur_miroir": 6.313,
            "aire_section": 6.455,
            "perimetre_mouille": 7.373,
            "rayon_hydraulique": 0.875,
            "vitesse_ecoulement": 0.77,
            "nombre_froude": 0.24,
            "regime": "Fluvial"
        },
        "formulas": [
            {
                "name": "Formule de Manning",
                "equation": "V = (1/n) * R^(2/3) * S^(1/2)",
                "variables": {
                    "V": "Vitesse d'écoulement (m/s)",
                    "n": "Coefficient de Manning",
                    "R": "Rayon hydraulique (m)",
                    "S": "Pente longitudinale (m/m)"
                },
                "units": {
                    "V": "m/s",
                    "n": "sans dimension",
                    "R": "m",
                    "S": "m/m"
                }
            },
            {
                "name": "Nombre de Froude",
                "equation": "Fr = V / √(g * h)",
                "variables": {
                    "Fr": "Nombre de Froude",
                    "V": "Vitesse d'écoulement (m/s)",
                    "g": "Accélération gravitationnelle (m/s²)",
                    "h": "Hauteur d'eau (m)"
                }
            }
        ],
        "verifications": [
            {
                "name": "Vitesse d'écoulement",
                "passed": True,
                "message": "0.77 m/s (dans les limites 0.3 - 2.0 m/s)"
            },
            {
                "name": "Régime d'écoulement",
                "passed": True,
                "message": "Fluvial (Fr = 0.24 < 1)"
            },
            {
                "name": "Stabilité des talus",
                "passed": True,
                "message": "Pente des talus 1.5H:1V acceptable"
            }
        ],
        "performance": {
            "calculation_time": 0.15,
            "memory_used": 2.3,
            "iterations": 3
        }
    }
    
    print("🧪 Test de génération de rapport global...")
    
    # Vérifier Pandoc
    pandoc_available = check_pandoc_availability()
    print(f"📦 Pandoc disponible : {pandoc_available}")
    
    # Formats à tester (sans PDF pour éviter les problèmes)
    formats = ['md', 'html']
    
    # Générer le rapport
    try:
        results = generate_global_report(
            data=data,
            output_dir="output/test_reports",
            formats=formats,
            template="enhanced"
        )
        
        print("✅ Rapport généré avec succès !")
        print("📁 Fichiers créés :")
        for format_type, file_path in results.items():
            print(f"  - {format_type.upper()}: {file_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")
        return False

def test_rapport_aep():
    """Test de génération d'un rapport AEP"""
    
    data = {
        "type": "Calcul AEP - Dimensionnement Réseau",
        "module": "AEP",
        "version": "2.1.0",
        "input_data": {
            "population": 5000,
            "dotation": 150,
            "coefficient_pointe": 1.3,
            "materiau": "PVC",
            "diametre": 0.2
        },
        "results": {
            "debit_global": 9.0,
            "debit_pointe": 11.7,
            "vitesse": 1.2,
            "perte_charge": 2.5,
            "pression": 27.5
        },
        "formulas": [
            {
                "name": "Formule de Hazen-Williams",
                "equation": "J = 10.67 * (Q/C)^1.85 * D^(-4.87)",
                "variables": {
                    "J": "Perte de charge (m/km)",
                    "Q": "Débit (m³/s)",
                    "C": "Coefficient Hazen-Williams",
                    "D": "Diamètre (m)"
                }
            }
        ],
        "verifications": [
            {
                "name": "Pression minimale",
                "passed": True,
                "message": "27.5 m > 15 m (minimum requis)"
            },
            {
                "name": "Vitesse d'écoulement",
                "passed": True,
                "message": "1.2 m/s (dans les limites 0.3 - 3.0 m/s)"
            }
        ]
    }
    
    print("🧪 Test de génération de rapport AEP...")
    
    try:
        results = generate_global_report(
            data=data,
            output_dir="output/test_reports",
            formats=['md', 'html'],
            template="enhanced"
        )
        
        print("✅ Rapport AEP généré avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération AEP : {e}")
        return False

if __name__ == "__main__":
    print("🚀 Tests des rapports globaux LCPI")
    print("=" * 50)
    
    # Test rapport canal
    success1 = test_rapport_canal()
    
    # Test rapport AEP
    success2 = test_rapport_aep()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 Tous les tests de rapports sont passés !")
    else:
        print("❌ Certains tests ont échoué")
    
    print("\n📊 Résumé :")
    print(f"  - Rapport Canal : {'✅' if success1 else '❌'}")
    print(f"  - Rapport AEP : {'✅' if success2 else '❌'}") 