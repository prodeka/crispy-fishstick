# config/pluviometrie_sources.py

"""
Ce fichier centralise les paramètres pluviométriques (coefficients de Montana 'a' et 'b')
issus de diverses sources scientifiques pour différentes localités.

Le programme utilise la formule I = a * tc^b. Pour que l'intensité (I) diminue
lorsque le temps de concentration (tc) augmente, l'exposant 'b' doit être négatif.
Toutes les valeurs de 'b' listées ici ont été standardisées en conséquence.
"""

# --- DICTIONNAIRE PRINCIPAL DES DONNÉES SCIENTIFIQUES PAR DÉFAUT ---
# Cette structure unique contient toutes les données, rendant le fichier
# plus clair et plus facile à maintenir.
DEFAULT_PLUVIO_DATA = {

    # --- Source: DOUTI N. (2021) ---
    "Lomé-Aéroport, Togo (DOUTI 2021)": {
        '5': {'nom': 'Pluie T=5 ans', 'a': 66.234, 'b': -0.470},
        '10': {'nom': 'Pluie T=10 ans', 'a': 75.763, 'b': -0.471},
        '15': {'nom': 'Pluie T=15 ans', 'a': 140.384, 'b': -0.472},
        '20': {'nom': 'Pluie T=20 ans', 'a': 178.236, 'b': -0.473},
    },
    "Atakpamé, Togo (DOUTI 2021)": {
        '5': {'nom': 'Pluie T=5 ans', 'a': 87.700, 'b': -0.480},
        '10': {'nom': 'Pluie T=10 ans', 'a': 106.915, 'b': -0.482},
        '20': {'nom': 'Pluie T=20 ans', 'a': 156.717, 'b': -0.485},
    },
    "Kara, Togo (DOUTI 2021)": {
        '5': {'nom': 'Pluie T=5 ans', 'a': 115.648, 'b': -0.500},
        '10': {'nom': 'Pluie T=10 ans', 'a': 136.649, 'b': -0.501},
        '20': {'nom': 'Pluie T=20 ans', 'a': 157.650, 'b': -0.503},
    },
    "Mango, Togo (DOUTI 2021)": {
        '5': {'nom': 'Pluie T=5 ans', 'a': 96.917, 'b': -0.510},
        '10': {'nom': 'Pluie T=10 ans', 'a': 118.130, 'b': -0.511},
        '20': {'nom': 'Pluie T=20 ans', 'a': 139.344, 'b': -0.513},
    },

    # --- Source: Gbafa et al. (2017b) ---
    # Les auteurs donnent b > 0 pour I = a / d^b. Nous prenons donc -b.
    "Lomé, Togo (Gbafa et al. 2017b)": {
        '10': {'nom': 'Pluie T=10 ans', 'a': 9.4130, 'b': -0.5525},
        '20': {'nom': 'Pluie T=20 ans', 'a': 10.7400, 'b': -0.5667},
        '50': {'nom': 'Pluie T=50 ans', 'a': 12.5800, 'b': -0.5862},
        '100': {'nom': 'Pluie T=100 ans', 'a': 14.0400, 'b': -0.6008},
    },

    # --- Source: WOUEDJE.M.A.L (Mémoire) ---
    # L'auteur donne b = -1 pour toutes les périodes.
    "Abidjan, CIV (WOUEDJE)": {
        '2': {'nom': 'Pluie T=2 ans', 'a': 5.1588, 'b': -1.0},
        '5': {'nom': 'Pluie T=5 ans', 'a': 7.2100, 'b': -1.0},
        '10': {'nom': 'Pluie T=10 ans', 'a': 8.5000, 'b': -1.0},
        '20': {'nom': 'Pluie T=20 ans', 'a': 9.2000, 'b': -1.0},
        '30': {'nom': 'Pluie T=30 ans', 'a': 9.5569, 'b': -1.0},
    },
    "Adiaké, CIV (WOUEDJE)": {
        '2': {'nom': 'Pluie T=2 ans', 'a': 4.4434, 'b': -1.0},
        '30': {'nom': 'Pluie T=30 ans', 'a': 7.0543, 'b': -1.0},
    },
    "Yamoussoukro, CIV (WOUEDJE)": {
        '2': {'nom': 'Pluie T=2 ans', 'a': 2.9478, 'b': -1.0},
        '30': {'nom': 'Pluie T=30 ans', 'a': 5.2817, 'b': -1.0},
    },

    # --- Source: MODONGOU B. S. (2023) ---
    "Cinkassé, Togo (MODONGOU 2023)": {
        '2': {'nom': 'Pluie T=2 ans', 'a': 29.289, 'b': -1.0},
        '30': {'nom': 'Pluie T=30 ans', 'a': 139.79, 'b': -1.0},
    },
    "Mandouri, Togo (MODONGOU 2023)": {
        '2': {'nom': 'Pluie T=2 ans', 'a': 32.141, 'b': -1.0},
        '30': {'nom': 'Pluie T=30 ans', 'a': 142.45, 'b': -1.0},
    },

    # --- Source: BENZAID B. (2015) ---
    "Guelma, Algérie (BENZAID 2015)": {
        '2': {'nom': 'Pluie T=2 ans', 'a': 21.206, 'b': -0.748},
        '5': {'nom': 'Pluie T=5 ans', 'a': 28.839, 'b': -0.749},
        '10': {'nom': 'Pluie T=10 ans', 'a': 33.893, 'b': -0.750},
        '20': {'nom': 'Pluie T=20 ans', 'a': 38.741, 'b': -0.751},
        '25': {'nom': 'Pluie T=25 ans', 'a': 40.279, 'b': -0.754},
        '50': {'nom': 'Pluie T=50 ans', 'a': 45.016, 'b': -0.757},
        '100': {'nom': 'Pluie T=100 ans', 'a': 49.718, 'b': -0.759},
    },
}