# Fichier de configuration globale

# Par défaut, le mode verbeux est DÉSACTIVÉ.
# Il sera activé si le programme est lancé avec le flag -v.
VERBOSE = False

# Création d'un objet settings pour la compatibilité
class Settings:
    def __init__(self):
        self.VERBOSE = VERBOSE

settings = Settings()
