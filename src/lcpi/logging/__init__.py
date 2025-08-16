"""
Module de journalisation pour LCPI.
Gère la création et la sauvegarde des fichiers de log JSON auditable.
"""

from .logger import log_calculation_result, LogEntryModel

__all__ = ["log_calculation_result", "LogEntryModel"]
