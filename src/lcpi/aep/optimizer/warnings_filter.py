"""
Filtre et supprime les warnings intrusifs des bibliothèques externes.
"""

import warnings
import logging
from contextlib import contextmanager


class WarningsFilter:
    """Filtre les warnings intrusifs des bibliothèques externes."""
    
    def __init__(self):
        """Initialise le filtre de warnings."""
        self._original_filters = []
        self._suppressed_warnings = [
            # Warnings wntr
            "Not all curves were used",
            "units conversion left to user",
            # Autres warnings courants
            "UserWarning",
            "DeprecationWarning"
        ]
    
    def suppress_warnings(self):
        """Supprime les warnings spécifiés."""
        # Sauvegarde les filtres existants
        self._original_filters = warnings.filters[:]
        
        # Ajoute des filtres pour supprimer les warnings spécifiques
        for warning_msg in self._suppressed_warnings:
            warnings.filterwarnings("ignore", message=warning_msg)
            warnings.filterwarnings("ignore", category=UserWarning)
            warnings.filterwarnings("ignore", category=DeprecationWarning)
        
        # Supprime aussi les warnings de logging
        logging.getLogger("wntr").setLevel(logging.ERROR)
        logging.getLogger("epanet").setLevel(logging.ERROR)
    
    def restore_warnings(self):
        """Restaure les filtres de warnings originaux."""
        warnings.filters[:] = self._original_filters
        
        # Restaure le niveau de logging
        logging.getLogger("wntr").setLevel(logging.WARNING)
        logging.getLogger("epanet").setLevel(logging.WARNING)
    
    @contextmanager
    def suppress_warnings_context(self):
        """Contexte pour supprimer temporairement les warnings."""
        try:
            self.suppress_warnings()
            yield
        finally:
            self.restore_warnings()


# Instance globale
warnings_filter = WarningsFilter()


def suppress_warnings_decorator(func):
    """Décorateur pour supprimer les warnings pendant l'exécution d'une fonction."""
    def wrapper(*args, **kwargs):
        with warnings_filter.suppress_warnings_context():
            return func(*args, **kwargs)
    return wrapper


def suppress_warnings_globally():
    """Supprime globalement les warnings intrusifs."""
    warnings_filter.suppress_warnings()


def restore_warnings_globally():
    """Restaure globalement les warnings."""
    warnings_filter.restore_warnings()
