# Fichier pour définir les classes de matériaux (Béton, Acier)


class Beton:
    def __init__(self, fc28=25.0, gamma_b=1.5):
        self.fc28 = fc28  # Résistance caractéristique à 28 jours (MPa)
        self.gamma_b = gamma_b  # Coefficient de sécurité du béton

    def __repr__(self):
        return f"Béton(fc28={self.fc28} MPa)"


class Acier:
    def __init__(self, fe=500.0, gamma_s=1.15):
        self.fe = fe  # Limite d'élasticité (MPa)
        self.gamma_s = gamma_s  # Coefficient de sécurité de l'acier

    def __repr__(self):
        return f"Acier(fe={self.fe} MPa)"
