from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import time
from collections import OrderedDict


def _sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _stable_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class OptimizationCache:
    """Cache persistant + LRU mémoire (clé = hash(network, H, diameters, context))."""

    def __init__(self, persist_dir: Optional[Path] = None, max_mem: int = 1024, ttl_s: int = 3600):
        self.persist_dir = Path(persist_dir) if persist_dir else Path(".cache/opt_v11")
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.max_mem = int(max_mem)
        self.ttl_s = int(ttl_s)
        self._mem: OrderedDict[str, Tuple[float, Dict[str, Any]]] = OrderedDict()

    def _key(self, network_model: Dict[str, Any], H_tank: float, diameters: Dict[str, int], context: Optional[Dict[str, Any]] = None) -> str:
        payload = {
            "network": network_model,
            "H": float(H_tank),
            "diameters": diameters or {},
            "context": context or {},
        }
        return _sha256_of_text(_stable_json(payload))

    def get(self, network_model: Dict[str, Any], H_tank: float, diameters: Dict[str, int], context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        k = self._key(network_model, H_tank, diameters, context)
        # Mémoire d'abord
        if k in self._mem:
            ts, val = self._mem.pop(k)
            if (time.time() - ts) <= self.ttl_s:
                # recentrer LRU
                self._mem[k] = (ts, val)
                return val
            # expiré
            # ne pas remettre
        f = self.persist_dir / f"{k}.json"
        if not f.exists():
            return None
        try:
            val = json.loads(f.read_text(encoding="utf-8"))
            # alimenter mémoire
            self._mem[k] = (time.time(), val)
            # evict si besoin
            while len(self._mem) > self.max_mem:
                self._mem.popitem(last=False)
            return val
        except Exception:
            return None

    def set(self, network_model: Dict[str, Any], H_tank: float, diameters: Dict[str, int], result: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> None:
        k = self._key(network_model, H_tank, diameters, context)
        f = self.persist_dir / f"{k}.json"
        try:
            f.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
            # mémoire
            self._mem[k] = (time.time(), result)
            while len(self._mem) > self.max_mem:
                self._mem.popitem(last=False)
        except Exception:
            pass


