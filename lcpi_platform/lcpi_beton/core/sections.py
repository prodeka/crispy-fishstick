# Fichier pour définir les classes de sections (Rectangulaire, T, etc.)


class SectionRectangulaire:
    def __init__(self, b, h, beton=None, acier=None):
        self.b = b  # Largeur (m)
        self.h = h  # Hauteur (m)
        self.beton = beton
        self.acier = acier

    def __repr__(self):
        return f"SectionRectangulaire(b={self.b}m, h={self.h}m)"
