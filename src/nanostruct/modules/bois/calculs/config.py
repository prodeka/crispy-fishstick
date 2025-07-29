# -*- coding: utf-8 -*-
# Fichier: calculs/config.py

import sys
import codecs


def configurer_encodage():
    """
    Tente de forcer l'encodage de la console en UTF-8 sur Windows.
    Doit être appelé au tout début d'un script.
    """
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
            # print("--- Encodage reconfigure en UTF-8 ---") # Optionnel
        except Exception:
            # Si ça ne marche pas, on continue sans planter.
            pass
