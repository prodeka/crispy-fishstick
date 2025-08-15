#!/usr/bin/env python3
"""Test simple pour Hardy-Cross"""

from src.lcpi.aep.calculations.hardy_cross import hardy_cross_network

# Réseau simple
reseau = {
    'mailles': [['C1', 'C2', 'C3']],
    'conduites': {
        'C1': {'resistance_K': 100.0, 'debit_Q': 0.05},
        'C2': {'resistance_K': 150.0, 'debit_Q': 0.03},
        'C3': {'resistance_K': 80.0, 'debit_Q': 0.02}
    }
}

print('🔄 Test Hardy-Cross avec affichage des itérations:')
resultats = hardy_cross_network(reseau, tolerance=1e-6, afficher_iterations=True)

print(f'✅ Convergence: {resultats["convergence"]}')
print(f'📊 Itérations: {resultats["iterations"]}')
print(f'🎯 Erreur finale: {resultats["erreur_finale"]:.2e}')

print('\n💧 Débits finaux:')
for id_conduite, conduite in resultats['conduites_finales'].items():
    debit_ls = conduite['debit_Q'] * 1000
    print(f'  {id_conduite}: {debit_ls:+.2f} l/s') 