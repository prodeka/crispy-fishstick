from typing import Dict, List, Tuple, Optional
import random
import logging

logger = logging.getLogger(__name__)

def soft_repair_solution(
    diameters_map: Dict[str, int],
    simulation_metrics: Dict,
    candidate_diameters: List[int],
    max_changes_fraction: float = 0.10,
    constraints: Optional[Dict] = None
) -> Tuple[Dict[str, int], Dict]:
    """
    Tente une réparation "douce" d'une solution infaisable.

    Identifie les N conduites les plus problématiques (basé sur la perte de charge)
    et augmente leur diamètre d'un seul cran dans la liste des candidats.

    Retourne le nouveau dictionnaire de diamètres et un dictionnaire de diagnostic.
    """
    changes_made = {"repaired_pipes": [], "total_changes": 0}
    
    # On a besoin des pertes de charge par conduite pour une réparation intelligente
    headlosses = simulation_metrics.get("headlosses_m")
    if not headlosses or not isinstance(headlosses, dict):
        logger.debug("Réparation impossible : métriques de perte de charge par conduite non disponibles.")
        return diameters_map, changes_made
        
    # Trier les conduites par perte de charge, de la plus élevée à la plus basse
    problematic_pipes_sorted = sorted(headlosses.items(), key=lambda item: item[1], reverse=True)
    
    # Calculer le nombre de conduites à modifier (au moins 1)
    num_pipes_to_change = max(1, int(len(diameters_map) * max_changes_fraction))
    
    # Sélectionner les N conduites les plus problématiques
    pipes_to_repair = [pipe_id for pipe_id, _ in problematic_pipes_sorted[:num_pipes_to_change]]
    
    new_diameters_map = dict(diameters_map)
    sorted_candidates = sorted(candidate_diameters)

    for pipe_id in pipes_to_repair:
        current_diameter = new_diameters_map.get(pipe_id)
        if current_diameter is None:
            continue
            
        try:
            current_index = sorted_candidates.index(current_diameter)
            # Augmenter d'un seul cran, sans dépasser la fin de la liste
            new_index = min(current_index + 1, len(sorted_candidates) - 1)
            
            new_diameter = sorted_candidates[new_index]

            if new_diameter != current_diameter:
                new_diameters_map[pipe_id] = new_diameter
                changes_made["repaired_pipes"].append({
                    "pipe_id": pipe_id,
                    "from_dn_mm": current_diameter,
                    "to_dn_mm": new_diameter
                })
        except ValueError:
            # Le diamètre actuel n'est pas dans la liste des candidats, on ne peut rien faire
            logger.warning(f"Impossible de réparer la conduite {pipe_id}: son diamètre {current_diameter} n'est pas dans la liste des candidats.")
            continue
            
    changes_made["total_changes"] = len(changes_made["repaired_pipes"])
    return new_diameters_map, changes_made
