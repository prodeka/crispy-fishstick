"""
Module de comparaison des variantes de réseaux AEP.

Ce module implémente les méthodes de comparaison, les métriques
d'évaluation et la génération de rapports comparatifs.
"""

from .metrics import ComparisonMetrics
from .visualizer import NetworkVisualizer
from .reporter import ComparisonReporter

__all__ = [
    'ComparisonMetrics',
    'NetworkVisualizer',
    'ComparisonReporter'
]
