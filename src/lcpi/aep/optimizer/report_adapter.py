"""
Adaptateur pour la compatibilité entre le format V11 et le système de rapport LCPI.

Ce module permet d'intégrer les résultats d'optimisation V11 
avec la commande 'lcpi rapport' existante.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .models import OptimizationResult
from .output import OutputFormatter


class V11ReportAdapter:
    """Adaptateur pour intégrer le format V11 avec le système de rapport LCPI."""
    
    def __init__(self):
        """Initialise l'adaptateur."""
        self.formatter = OutputFormatter()
    
    def convert_v11_to_log_format(self, v11_result: OptimizationResult, 
                                  execution_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Convertit un résultat V11 en format de log compatible avec 'lcpi rapport'.
        
        Args:
            v11_result: Résultat d'optimisation au format V11
            execution_metadata: Métadonnées d'exécution optionnelles
            
        Returns:
            Dictionnaire au format de log LCPI
        """
        # Formater le résultat en V11 d'abord
        v11_output = self.formatter.format_v11(v11_result, execution_metadata)
        
        # Générer les métadonnées pour le log
        timestamp = datetime.now()
        log_id = f"opt_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        # Calculer des statistiques pour la transparence mathématique
        total_proposals = len(v11_output['proposals'])
        feasible_proposals = len([p for p in v11_output['proposals'] if p.get('is_feasible', False)])
        
        # Créer les étapes de transparence mathématique
        transparence_steps = [
            f"Méthode d'optimisation: {v11_output['metadata'].get('method', 'N/A')}",
            f"Fichier réseau: {v11_output['metadata'].get('network_file', 'N/A')}",
            f"Nombre total de propositions: {total_proposals}",
            f"Solutions faisables: {feasible_proposals}",
        ]
        
        # Ajouter des informations spécifiques selon la méthode
        method = v11_output['metadata'].get('method', '')
        if 'global' in method.lower() or 'nsga' in method.lower():
            transparence_steps.extend([
                f"Algorithme: {v11_output['metadata'].get('algorithm', 'NSGA-II')}",
                f"Population: {v11_output['metadata'].get('population_size', 'N/A')}",
                f"Générations: {v11_output['metadata'].get('generations', 'N/A')}"
            ])
        elif 'nested' in method.lower():
            transparence_steps.extend([
                f"Itérations binaires: {v11_output['metadata'].get('binary_iterations', 'N/A')}",
                f"Pression minimale: {v11_output['metadata'].get('pressure_min_m', 'N/A')} m"
            ])
        elif 'surrogate' in method.lower():
            transparence_steps.extend([
                f"Taille dataset: {v11_output['metadata'].get('surrogate_dataset_size', 'N/A')}",
                f"Rounds d'apprentissage: {v11_output['metadata'].get('surrogate_rounds', 'N/A')}"
            ])
        
        # Ajouter des informations sur les coûts si disponibles
        if v11_output['proposals']:
            first_proposal = v11_output['proposals'][0]
            if 'costs' in first_proposal and first_proposal['costs']:
                costs = first_proposal['costs']
                if 'CAPEX' in costs:
                    transparence_steps.append(f"CAPEX optimal: {costs['CAPEX']:,.0f} FCFA")
                if 'OPEX_npv' in costs:
                    transparence_steps.append(f"OPEX NPV optimal: {costs['OPEX_npv']:,.0f} FCFA")
        
        # Créer le log au format LCPI
        log_format = {
            "id": log_id,
            "titre_calcul": f"Optimisation AEP V11 - {v11_output['metadata'].get('method', 'Méthode inconnue')}",
            "timestamp": timestamp.isoformat(),
            "commande_executee": self._generate_command_executed(v11_output['metadata']),
            "donnees_resultat": v11_output,
            "transparence_mathematique": transparence_steps,
            "hash_donnees_entree": self._generate_input_hash(v11_output['metadata']),
            "parametres_entree": {
                "network_file": v11_output['metadata'].get('network_file'),
                "method": v11_output['metadata'].get('method'),
                "algorithm": v11_output['metadata'].get('algorithm'),
                "iterations": v11_output['metadata'].get('iterations'),
                "pressure_min_m": v11_output['metadata'].get('pressure_min_m'),
                "lambda_opex": execution_metadata.get('lambda_opex') if execution_metadata else None
            },
            "version_algorithme": "V11",
            "plugin": "aep",
            "command": "optimizer",
            "execution_time": execution_metadata.get('execution_time') if execution_metadata else None,
            "status": "success"
        }
        
        return log_format
    
    def _generate_command_executed(self, metadata: Dict[str, Any]) -> str:
        """Génère la commande CLI équivalente."""
        method = metadata.get('method', 'nested')
        network_file = metadata.get('network_file', 'network.inp')
        
        cmd_parts = [
            "lcpi aep optimizer price-optimize",
            network_file,
            f"--method {method}"
        ]
        
        # Ajouter des paramètres spécifiques selon la méthode
        if metadata.get('pressure_min_m'):
            cmd_parts.append(f"--pressure-min {metadata['pressure_min_m']}")
        
        return " ".join(cmd_parts)
    
    def _generate_input_hash(self, metadata: Dict[str, Any]) -> str:
        """Génère un hash simple pour les données d'entrée."""
        import hashlib
        
        # Utiliser les métadonnées principales pour créer un hash
        hash_input = {
            "method": metadata.get('method'),
            "network_file": metadata.get('network_file'),
            "algorithm": metadata.get('algorithm')
        }
        
        hash_str = json.dumps(hash_input, sort_keys=True)
        return hashlib.sha256(hash_str.encode()).hexdigest()[:16]
    
    def save_v11_result_as_log(self, v11_result: OptimizationResult, 
                              output_path: Path,
                              execution_metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Sauvegarde un résultat V11 comme un log compatible avec 'lcpi rapport'.
        
        Args:
            v11_result: Résultat d'optimisation V11
            output_path: Chemin de sauvegarde
            execution_metadata: Métadonnées d'exécution
            
        Returns:
            ID du log créé
        """
        log_format = self.convert_v11_to_log_format(v11_result, execution_metadata)
        
        # Sauvegarder le fichier
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(log_format, f, indent=2, ensure_ascii=False)
        
        return log_format['id']
    
    def create_hybrid_template_context(self, v11_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée un contexte compatible avec les templates existants ET V11.
        
        Args:
            v11_data: Données au format V11
            
        Returns:
            Contexte utilisable par les templates
        """
        # Adapter pour le template existant (base_simple.html)
        log_context = {
            "logs_selectionnes": [self.convert_v11_to_log_format_dict(v11_data)],
            "projet_metadata": {"nom_projet": "Optimisation AEP V11"},
            "generation_date": datetime.now().strftime("%Y-%m-%d"),
            "version_lcpi": "V11"
        }
        
        # Adapter pour le template V11 (optimisation_tank_v11.jinja2)
        v11_context = {
            "proposals": v11_data.get('proposals', []),
            "pareto_front": v11_data.get('pareto_front', []),
            "metadata": v11_data.get('metadata', {}),
            "now": datetime.now()
        }
        
        # Contexte hybride
        return {
            **log_context,
            **v11_context,
            "format_type": "v11",
            "is_v11_format": True
        }
    
    def convert_v11_to_log_format_dict(self, v11_data: Dict[str, Any]) -> Dict[str, Any]:
        """Version simplifiée pour templates existants."""
        return {
            "id": f"v11_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "titre_calcul": f"Optimisation AEP V11 - {v11_data['metadata'].get('method', 'N/A')}",
            "timestamp": datetime.now().isoformat(),
            "commande_executee": f"lcpi aep optimizer --method {v11_data['metadata'].get('method', 'nested')}",
            "donnees_resultat": v11_data,
            "transparence_mathematique": [
                f"Format: V11",
                f"Méthode: {v11_data['metadata'].get('method', 'N/A')}",
                f"Propositions: {len(v11_data.get('proposals', []))}"
            ]
        }


# Instance globale pour utilisation
v11_adapter = V11ReportAdapter()


def create_log_from_v11_result(v11_result: OptimizationResult, 
                              output_path: Path,
                              execution_metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Fonction utilitaire pour créer un log compatible depuis un résultat V11.
    
    Args:
        v11_result: Résultat d'optimisation V11
        output_path: Chemin de sauvegarde
        execution_metadata: Métadonnées d'exécution
        
    Returns:
        ID du log créé
    """
    return v11_adapter.save_v11_result_as_log(v11_result, output_path, execution_metadata)


def convert_v11_for_existing_report(v11_result: OptimizationResult) -> Dict[str, Any]:
    """
    Fonction utilitaire pour convertir un résultat V11 pour les rapports existants.
    
    Args:
        v11_result: Résultat d'optimisation V11
        
    Returns:
        Format compatible avec le système de rapport existant
    """
    return v11_adapter.convert_v11_to_log_format(v11_result)
