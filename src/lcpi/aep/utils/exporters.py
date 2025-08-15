"""
Utilitaires d'export pour les commandes AEP.

Fournit une API homogène pour exporter des résultats en:
- json
- yaml
- markdown
- csv
- html
"""

from typing import Any, Dict
import json


def _flatten_dict(nested: Any, parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Aplati un dictionnaire pour export CSV/Markdown basique."""
    flattened: Dict[str, Any] = {}
    if isinstance(nested, dict):
        for key, value in nested.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else str(key)
            flattened.update(_flatten_dict(value, new_key, sep))
    elif isinstance(nested, list):
        for idx, item in enumerate(nested):
            new_key = f"{parent_key}{sep}{idx}" if parent_key else str(idx)
            flattened.update(_flatten_dict(item, new_key, sep))
    else:
        flattened[parent_key or "value"] = nested
    return flattened


def export_content(result: Any, export_format: str) -> str:
    """Exporte un résultat dans un format texte.

    Args:
        result: Objet Python sérialisable (dict/list/...)
        export_format: json|yaml|markdown|csv|html

    Returns:
        str: contenu exporté prêt à écrire/afficher
    """
    export_format = (export_format or "json").lower()
    if export_format == "json":
        return json.dumps(result, indent=2, ensure_ascii=False)
    if export_format == "yaml":
        import yaml
        return yaml.safe_dump(result, sort_keys=False, allow_unicode=True)
    if export_format == "markdown":
        flat = _flatten_dict(result)
        lines = ["# Résultats", ""]
        for k, v in flat.items():
            lines.append(f"- **{k}**: {v}")
        return "\n".join(lines)
    if export_format == "csv":
        flat = _flatten_dict(result)
        lines = ["key,value"]
        for k, v in flat.items():
            v_str = str(v).replace("\n", " ").replace(",", ";")
            lines.append(f"{k},{v_str}")
        return "\n".join(lines)
    if export_format == "html":
        body = json.dumps(result, indent=2, ensure_ascii=False)
        return f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>Résultats</title></head><body><pre>{body}</pre></body></html>"""
    raise ValueError(f"Format d'export non supporté: {export_format}")


__all__ = [
    "export_content",
    "_flatten_dict",
]


