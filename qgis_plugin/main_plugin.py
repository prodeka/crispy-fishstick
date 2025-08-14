# -*- coding: utf-8 -*-

"""
Fichier principal pour le plugin LCPI-CLI.
Ce fichier sera le point d'entrée pour QGIS.
"""

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtWidgets import QAction, QMainWindow
from qgis.PyQt.QtGui import QIcon
import os.path

class LcpiPlugin:
    """Classe principale du Plugin QGIS."""

    def __init__(self, iface):
        """Constructeur.

        :param iface: Une instance de QgisInterface.
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = u'&LCPI-CLI'
        self.toolbar = self.iface.addToolBar(u'LCPI-CLI')
        self.toolbar.setObjectName(u'LcpiToolbar')

    def initGui(self):
        """Crée les actions du menu et les boutons de la barre d'outils."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png') # Prévoir une icone
        icon = QIcon(icon_path)
        
        self.add_action(
            icon,
            text=u'Lancer Calcul LCPI',
            callback=self.run_dialog,
            parent=self.iface.mainWindow(),
            add_to_menu=True,
            add_to_toolbar=True
        )

    def add_action(self, icon, text, callback, enabled_flag=True, add_to_menu=True, add_to_toolbar=True, status_tip=None, whats_this=None, parent=None):
        """Crée une action et la connecte."""
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)
        return action

    def unload(self):
        """Supprime les éléments de l'interface lors du déchargement."""
        for action in self.actions:
            self.iface.removePluginMenu(u'&LCPI-CLI', action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run_dialog(self):
        """Exécute la boîte de dialogue principale."""
        # C'est ici que nous allons créer et afficher notre dialogue.
        # from .main_dialog import LcpiDialog
        # dlg = LcpiDialog()
        # dlg.exec_()
        self.iface.messageBar().pushMessage("Succès", "Le plugin LCPI est en cours de développement.", level=0, duration=3)
        print("La boîte de dialogue LCPI devrait s'ouvrir ici.")
