"""
Compat couche mince pour anciens tests.

Expose:
- log_calculation_result
- calculate_input_hash
- list_available_logs
- load_log_by_id
- LogEntryModel
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .lcpi_logging.logger import lcpi_logger
from .aep.core.models import LogEntryModel


def calculate_input_hash(data: Dict[str, Any]) -> str:
    normalized = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def log_calculation_result(
    titre_calcul: str,
    commande_executee: str,
    donnees_resultat: Dict[str, Any],
    projet_dir: Path | str,
    parametres_entree: Optional[Dict[str, Any]] = None,
    transparence_mathematique: Optional[List[Any]] = None,
    version_algorithme: Optional[str] = None,
    verbose: bool = False,
) -> str:
    project_dir = Path(projet_dir)
    logs_dir = project_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Utilise lcpi_logger pour écrire un log standardisé
    return lcpi_logger.log_calculation_result(
        plugin="aep",
        command=titre_calcul,
        parameters={
            "commande_executee": commande_executee,
            "parametres_entree": parametres_entree or {},
            "version_algorithme": version_algorithme or "",
            "transparence_mathematique": transparence_mathematique or [],
            "hash_donnees_entree": calculate_input_hash(parametres_entree or {}),
        },
        results=donnees_resultat,
        execution_time=0.0,
        metadata={"projet_dir": str(project_dir)},
    )


def list_available_logs(projet_dir: Path | str) -> List[Dict[str, Any]]:
    logs = lcpi_logger.list_logs()
    return logs


def load_log_by_id(log_id: str, projet_dir: Path | str) -> Optional[Dict[str, Any]]:
    return lcpi_logger.get_log_by_id(log_id)


