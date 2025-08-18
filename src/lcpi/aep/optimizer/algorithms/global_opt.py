from __future__ import annotations

from typing import Any, Dict


def _build_minimal_config(raw: Dict[str, Any]) -> Any:
	"""Construit une configuration minimale compatible avec ConfigurationOptimisation.

	Cette fonction mappe les champs de notre config légère vers les champs requis
	si le modèle exige une structure plus riche.
	"""
	try:
		from ...optimization.models import ConfigurationOptimisation
		# Construire un dict minimal avec champs obligatoires si absents
		base = {
			"criteres": {"principal": "cout", "secondaires": [], "poids": [1.0]},
			"contraintes_budget": {"cout_max_fcfa": 1e12},
			"contraintes_techniques": {
				"pression_min_mce": 10.0,
				"pression_max_mce": 100.0,
				"vitesse_min_m_s": 0.3,
				"vitesse_max_m_s": 2.5,
			},
			"algorithme": {"type": "genetique", "population_size": 50, "generations": 10},
			"diametres_candidats": [{"diametre_mm": 110, "cout_fcfa_m": 0.0}],
		}
		base.update(raw or {})
		return ConfigurationOptimisation(**base)
	except Exception:
		return raw or {}


class GlobalOptimizer:
	"""Wrapper autour de l'algorithme génétique existant (Jalon 2 - squelette)."""

	def __init__(self, config: Any):
		try:
			from ...optimization.genetic_algorithm import GeneticOptimizer
			cfg = _build_minimal_config(config if isinstance(config, dict) else {})
			self.genetic_optimizer = GeneticOptimizer(cfg)
		except Exception:
			self.genetic_optimizer = None

	def optimize_global(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
		if self.genetic_optimizer is None:
			return {"meta": {"method": "global", "status": "skipped"}, "reason": "GeneticOptimizer indisponible"}
		try:
			# Signature à adapter selon l'implémentation réelle
			if hasattr(self.genetic_optimizer, "optimiser"):
				result = self.genetic_optimizer.optimiser(network_data)
			else:
				result = self.genetic_optimizer.optimize(network_data)
			return {"meta": {"method": "global", "status": "ok"}, "result": result}
		except Exception as e:
			return {"meta": {"method": "global", "status": "error"}, "error": str(e)}


