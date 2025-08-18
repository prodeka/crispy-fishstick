from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


def _sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _stable_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class OptimizationCache:
    """Cache persistant simple (clé = hash(network, H, diameters))."""

    def __init__(self, persist_dir: Optional[Path] = None):
        self.persist_dir = Path(persist_dir) if persist_dir else Path(".cache/opt_v11")
        self.persist_dir.mkdir(parents=True, exist_ok=True)

    def _key(self, network_model: Dict[str, Any], H_tank: float, diameters: Dict[str, int]) -> str:
        payload = {
            "network": network_model,
            "H": float(H_tank),
            "diameters": diameters or {},
        }
        return _sha256_of_text(_stable_json(payload))

    def get(self, network_model: Dict[str, Any], H_tank: float, diameters: Dict[str, int]) -> Optional[Dict[str, Any]]:
        k = self._key(network_model, H_tank, diameters)
        f = self.persist_dir / f"{k}.json"
        if not f.exists():
            return None
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            return None

    def set(self, network_model: Dict[str, Any], H_tank: float, diameters: Dict[str, int], result: Dict[str, Any]) -> None:
        k = self._key(network_model, H_tank, diameters)
        f = self.persist_dir / f"{k}.json"
        try:
            f.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass


