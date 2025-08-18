"""
Module core LCPI - Fonctionnalités de base et utilitaires.
"""

from .plugin_versioning import plugin_version_manager
from .reproducible import export_reproducible, ReproducibleExporter

__all__ = [
    "plugin_version_manager",
    "export_reproducible",
    "ReproducibleExporter"
]

__version__ = "2.1.0"
