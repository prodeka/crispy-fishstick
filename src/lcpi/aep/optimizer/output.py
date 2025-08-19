"""
Module de formatage de sortie pour l'optimisation AEP (V11).

Ce module s'intègre avec les modèles Pydantic existants pour générer
des sorties JSON standardisées et compatibles avec l'architecture LCPI.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import OptimizationResult, Proposal, TankDecision


class OutputFormatter:
    """Formateur de sortie pour les résultats d'optimisation AEP (V11)."""
    
    def __init__(self):
        """Initialise le formateur de sortie."""
        pass
    
    def format_v11(self, result: OptimizationResult, execution_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Formate un résultat d'optimisation au format JSON V11.
        
        Args:
            result: Résultat d'optimisation avec les propositions et le front de Pareto
            execution_metadata: Métadonnées d'exécution (temps, itérations, etc.)
            
        Returns:
            Dictionnaire au format JSON V11 standard
        """
        # Métadonnées par défaut
        default_metadata = {
            "version": "V11",
            "generation_date": datetime.now().isoformat(),
            "format": "lcpi_aep_optimization"
        }
        
        # Fusionner avec les métadonnées d'exécution
        if execution_metadata:
            default_metadata.update(execution_metadata)
        
        # Formater les propositions
        formatted_proposals = []
        for proposal in result.proposals:
            formatted_proposal = self._format_proposal(proposal)
            formatted_proposals.append(formatted_proposal)
        
        # Formater le front de Pareto
        pareto_front = None
        if result.pareto_front:
            pareto_front = [self._format_proposal(p) for p in result.pareto_front]
        
        # Structure V11 finale
        v11_output = {
            "proposals": formatted_proposals,
            "pareto_front": pareto_front,
            "metadata": {
                **default_metadata,
                **result.metadata
            }
        }
        
        return v11_output
    
    def _format_proposal(self, proposal: Proposal) -> Dict[str, Any]:
        """
        Formate une proposition individuelle au format V11.
        
        Args:
            proposal: Proposition d'optimisation
            
        Returns:
            Dictionnaire formaté de la proposition
        """
        # Formater les réservoirs
        tanks = []
        for tank in proposal.tanks:
            tanks.append({
                "id": tank.id,
                "H_m": tank.H_m
            })
        
        # Formater les coûts (assurer la compatibilité avec les clés existantes)
        costs = {}
        if hasattr(proposal.costs, 'get'):
            # Si c'est un dict
            costs = {
                "CAPEX": proposal.costs.get("CAPEX", proposal.costs.get("capex", 0.0)),
                "OPEX_annual": proposal.costs.get("OPEX_annual", proposal.costs.get("opex_annual", 0.0)),
                "OPEX_npv": proposal.costs.get("OPEX_npv", proposal.costs.get("opex_npv", 0.0))
            }
        else:
            # Si c'est un objet avec attributs
            costs = {
                "CAPEX": getattr(proposal.costs, "CAPEX", getattr(proposal.costs, "capex", 0.0)),
                "OPEX_annual": getattr(proposal.costs, "OPEX_annual", getattr(proposal.costs, "opex_annual", 0.0)),
                "OPEX_npv": getattr(proposal.costs, "OPEX_npv", getattr(proposal.costs, "opex_npv", 0.0))
            }
        
        # Formater les métriques
        metrics = {}
        if hasattr(proposal.metrics, 'get'):
            # Si c'est un dict
            metrics = {
                "min_pressure_m": proposal.metrics.get("min_pressure_m", 0.0),
                "max_velocity_m_s": proposal.metrics.get("max_velocity_m_s", 0.0)
            }
        else:
            # Si c'est un objet avec attributs
            metrics = {
                "min_pressure_m": getattr(proposal.metrics, "min_pressure_m", 0.0),
                "max_velocity_m_s": getattr(proposal.metrics, "max_velocity_m_s", 0.0)
            }
        
        return {
            "name": proposal.name,
            "is_feasible": proposal.is_feasible,
            "tanks": tanks,
            "diameters_mm": proposal.diameters_mm,
            "costs": costs,
            "metrics": metrics
        }
    
    def save_v11_json(self, result: OptimizationResult, output_path: Path, 
                      execution_metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Sauvegarde un résultat au format JSON V11.
        
        Args:
            result: Résultat d'optimisation
            output_path: Chemin de sortie pour le fichier JSON
            execution_metadata: Métadonnées d'exécution
        """
        v11_data = self.format_v11(result, execution_metadata)
        
        # Créer le dossier parent si nécessaire
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder en JSON avec indentation
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(v11_data, f, indent=2, ensure_ascii=False, default=str)
    
    def load_v11_json(self, input_path: Path) -> Dict[str, Any]:
        """
        Charge un fichier JSON V11.
        
        Args:
            input_path: Chemin vers le fichier JSON V11
            
        Returns:
            Données chargées au format V11
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def validate_v11_format(self, data: Dict[str, Any]) -> bool:
        """
        Valide qu'un dictionnaire respecte le format V11.
        
        Args:
            data: Données à valider
            
        Returns:
            True si le format est valide, False sinon
        """
        try:
            # Vérifier les clés obligatoires
            required_keys = ["proposals", "metadata"]
            if not all(key in data for key in required_keys):
                return False
            
            # Vérifier que proposals est une liste
            if not isinstance(data["proposals"], list):
                return False
            
            # Vérifier chaque proposition
            for proposal in data["proposals"]:
                if not self._validate_proposal_format(proposal):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _validate_proposal_format(self, proposal: Dict[str, Any]) -> bool:
        """
        Valide le format d'une proposition individuelle.
        
        Args:
            proposal: Proposition à valider
            
        Returns:
            True si le format est valide, False sinon
        """
        try:
            required_keys = ["name", "is_feasible", "tanks", "diameters_mm", "costs", "metrics"]
            if not all(key in proposal for key in required_keys):
                return False
            
            # Vérifier les types
            if not isinstance(proposal["name"], str):
                return False
            
            if not isinstance(proposal["is_feasible"], bool):
                return False
            
            if not isinstance(proposal["tanks"], list):
                return False
            
            if not isinstance(proposal["diameters_mm"], dict):
                return False
            
            if not isinstance(proposal["costs"], dict):
                return False
            
            if not isinstance(proposal["metrics"], dict):
                return False
            
            return True
            
        except Exception:
            return False


# Instance globale pour utilisation directe
formatter = OutputFormatter()


def format_optimization_result_v11(result: OptimizationResult, 
                                 execution_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Fonction utilitaire pour formater un résultat d'optimisation au format V11.
    
    Args:
        result: Résultat d'optimisation
        execution_metadata: Métadonnées d'exécution
        
    Returns:
        Dictionnaire au format JSON V11
    """
    return formatter.format_v11(result, execution_metadata)


def save_optimization_result_v11(result: OptimizationResult, 
                               output_path: Path,
                               execution_metadata: Optional[Dict[str, Any]] = None) -> None:
    """
    Fonction utilitaire pour sauvegarder un résultat au format V11.
    
    Args:
        result: Résultat d'optimisation
        output_path: Chemin de sortie
        execution_metadata: Métadonnées d'exécution
    """
    formatter.save_v11_json(result, output_path, execution_metadata)
