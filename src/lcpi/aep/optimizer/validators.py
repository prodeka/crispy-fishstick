from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .io import NetworkModel, sha256_of_file


class NetworkValidator:
    """Validations d'intégrité et de contenu minimal (MVP)."""

    def check_integrity(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {"ok": False, "errors": ["fichier introuvable"], "path": str(path)}
        try:
            checksum = sha256_of_file(path)
        except Exception as e:
            return {"ok": False, "errors": [f"lecture impossible: {e}"], "path": str(path)}
        return {"ok": True, "checksum": checksum, "path": str(path)}

    def validate_model(self, model: NetworkModel) -> Dict[str, Any]:
        errors = []
        if not model.nodes:
            errors.append("aucun noeud trouvé")
        if not model.links:
            errors.append("aucun lien trouvé")
        if not model.tanks:
            errors.append("aucun réservoir/tank défini")
        return {"ok": len(errors) == 0, "errors": errors}


