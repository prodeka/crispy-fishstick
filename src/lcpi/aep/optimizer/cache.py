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
    """Cache persistant + LRU mémoire (clé = hash(network, H_tanks, diameters, context))."""

    def __init__(self, persist_dir: Optional[Path] = None, max_mem: int = 1024, ttl_s: int = 3600):
        self.persist_dir = Path(persist_dir) if persist_dir else Path(".cache/opt_v13")
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.max_mem = int(max_mem)
        self.ttl_s = int(ttl_s)
        self._mem: OrderedDict[str, Tuple[float, Dict[str, Any]]] = OrderedDict()

    def _key(
        self,
        network_model: Dict[str, Any],
        H_tanks: Dict[str, float],  # CHANGED: from float to Dict
        diameters: Dict[str, int],
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        # Trier les clés de H_tanks pour une clé stable
        stable_h_tanks = dict(sorted(H_tanks.items()))

        payload = {
            "network_hash": _sha256_of_text(_stable_json(network_model)),
            "H_tanks": stable_h_tanks,
            "diameters": diameters or {},
            "context": context or {},
        }
        return _sha256_of_text(_stable_json(payload))

    def get(
        self,
        network_model: Dict[str, Any],
        H_tanks: Dict[str, float],
        diameters: Dict[str, int],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        k = self._key(network_model, H_tanks, diameters, context)
        # Mémoire d'abord
        if k in self._mem:
            ts, val = self._mem.pop(k)
            if (time.time() - ts) <= self.ttl_s:
                self._mem[k] = (ts, val)  # recentrer LRU
                return val
        
        f = self.persist_dir / f"{k}.json"
        if not f.exists() or f.stat().st_mtime < time.time() - self.ttl_s:
            if f.exists():
                try:
                    f.unlink() # Supprimer le cache expiré du disque
                except OSError:
                    pass
            return None
        
        try:
            val = json.loads(f.read_text(encoding="utf-8"))
            self._mem[k] = (time.time(), val)
            while len(self._mem) > self.max_mem:
                self._mem.popitem(last=False)
            return val
        except Exception:
            return None

    def set(
        self,
        network_model: Dict[str, Any],
        H_tanks: Dict[str, float],
        diameters: Dict[str, int],
        result: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        k = self._key(network_model, H_tanks, diameters, context)
        f = self.persist_dir / f"{k}.json"
        try:
            f.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
            self._mem[k] = (time.time(), result)
            while len(self._mem) > self.max_mem:
                self._mem.popitem(last=False)
        except Exception:
            pass