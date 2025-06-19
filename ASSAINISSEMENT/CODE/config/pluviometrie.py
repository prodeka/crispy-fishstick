# config/pluviometrie.py
# --- Dictionnaire des coefficients de pluie pour différentes périodes de retour (Lomé, Togo) ---
# Unités : i(mm/h), t(min)
REGIONAL_PARAMS_TOGO = {
    '10': {'nom': 'Pluie décennale (T=10 ans)', 'a': 1755, 'b': -0.84},
    '20': {'nom': 'Pluie vingtennale (T=20 ans)', 'a': 2010, 'b': -0.85},
    '50': {'nom': 'Pluie cinquantennale (T=50 ans)', 'a': 2385, 'b': -0.86},
    '100': {'nom': 'Pluie centennale (T=100 ans)', 'a': 2697, 'b': -0.86}
}