# -*- coding: utf-8 -*-

"""
Fichier principal pour le plugin LCPI-CLI.
Ce fichier sera le point d'entrée pour QGIS.
"""

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtWidgets import QAction, QMainWindow
from qgis.PyQt.QtGui import QIcon
import os.path

# Ce fichier __init__.py est nécessaire pour que QGIS reconnaisse le répertoire comme un plugin.
def classFactory(iface):
    from .main_plugin import LcpiPlugin
    return LcpiPlugin(iface)
