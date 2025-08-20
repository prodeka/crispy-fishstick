"""
Package d'optimisation pour les réseaux AEP.
"""

from .warnings_filter import suppress_warnings_globally

# Supprime automatiquement les warnings intrusifs au chargement du package
suppress_warnings_globally()

__all__ = [
    "suppress_warnings_globally",
]


