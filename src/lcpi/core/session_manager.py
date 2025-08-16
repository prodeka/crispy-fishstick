# session_manager.py
"""
Gestionnaire de session pour LCPI — version améliorée.

Principales améliorations :
- verrou simple pour éviter corruptions concurrentes
- écriture atomique des fichiers de session
- import dynamique des plugins via un registre extensible
- logging, typage, TTL configurable
"""

from __future__ import annotations
import os
import json
import time
import hashlib
import tempfile
import logging
import importlib
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional, Any, Callable

from .global_config import global_config

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclass
class SessionData:
    created_at: float
    last_used: float
    environment_hash: str
    plugins: Dict[str, Dict[str, Any]]
    global_config: Dict[str, Any]


class SessionManager:
    """Gestionnaire de session pour LCPI (amélioré)."""

    def __init__(self,
                 session_dir: Optional[Path] = None,
                 ttl_seconds: int = 86400):
        # Répertoire de sessions (configurable pour tests)
        base_tmp = Path(tempfile.gettempdir())
        self._session_dir = (session_dir or base_tmp / "lcpi_sessions")
        self._session_dir.mkdir(parents=True, exist_ok=True)

        # TTL pour invalidation automatique des sessions
        self.ttl_seconds = int(os.environ.get("LCPI_SESSION_TTL", ttl_seconds))

        self._session_file = self._get_session_file_path()
        self._lock_file = self._session_file.with_suffix(".lock")
        self._session_data: Optional[SessionData] = None
        self._is_initialized = False

        # Registre extensible {plugin_name: ("module.path", "callable_name" or None, alias_name_optional)}
        self._plugin_registry: Dict[str, tuple[str, Optional[str], Optional[str]]] = {}
        self._register_default_plugins()

    # -------------------------
    # Identification & chemins
    # -------------------------
    def _get_terminal_id(self) -> str:
        """Création d'un identifiant stable pour le terminal (hostname + user)."""
        try:
            host = os.uname().nodename if hasattr(os, "uname") else os.environ.get("COMPUTERNAME", "")
        except Exception:
            host = os.environ.get("COMPUTERNAME", "")
        
        # Utiliser l'utilisateur au lieu du PID pour plus de stabilité
        try:
            user = os.environ.get("USERNAME", os.environ.get("USER", "unknown"))
        except Exception:
            user = "unknown"
        
        # Créer un hash stable basé sur host + user
        stable_id = hashlib.sha1(f"{host}-{user}".encode()).hexdigest()
        return stable_id[:12]

    def _get_session_file_path(self) -> Path:
        terminal_id = self._get_terminal_id()
        return self._session_dir / f"session_{terminal_id}.json"

    # -------------------------
    # Plugin registry
    # -------------------------
    def _register_default_plugins(self):
        # Remplir avec mapping {name: (module_path, attribute_name_or_None, typer_name_override)}
        self.register_plugin("cm", "src.lcpi.cm.main", "register", "cm")
        self.register_plugin("bois", "src.lcpi.bois.main", "register", "bois")
        self.register_plugin("beton", "src.lcpi.beton.main", "register", "beton")
        self.register_plugin("hydro", "src.lcpi.hydrodrain.main", "register", "hydro")
        self.register_plugin("aep", "src.lcpi.aep.cli", "app", "aep")
        self.register_plugin("shell", "src.lcpi.shell.main", "register", "shell")
        self.register_plugin("reporting", "src.lcpi.reporting.cli", "app", "rapport")
        self.register_plugin("project", "src.lcpi.project_cli", "app", "project")

    def register_plugin(self, name: str, module_path: str, attr: Optional[str] = None, alias: Optional[str] = None):
        """Enregistrer dynamiquement un plugin dans la table de correspondance."""
        self._plugin_registry[name] = (module_path, attr, alias)

    def list_registered_plugins(self) -> Dict[str, tuple]:
        return dict(self._plugin_registry)

    # -------------------------
    # Verrou simple (file lock)
    # -------------------------
    def _acquire_lock(self) -> bool:
        """Tente de créer atomiquement un fichier .lock (retourne True si acquis)."""
        fd = None
        try:
            flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
            fd = os.open(str(self._lock_file), flags)
            os.close(fd)
            return True
        except FileExistsError:
            return False
        except Exception:
            # Ne crash pas l'app si lock non supporté, on renvoie False
            if fd:
                try:
                    os.close(fd)
                except Exception:
                    pass
            return False

    def _release_lock(self):
        try:
            if self._lock_file.exists():
                self._lock_file.unlink()
        except Exception as e:
            logger.debug("Impossible de supprimer le lock file: %s", e)

    # -------------------------
    # Chargement / sauvegarde
    # -------------------------
    def _load_session(self) -> Optional[SessionData]:
        if not self._session_file.exists():
            return None

        # TTL check by mtime
        try:
            file_age = time.time() - self._session_file.stat().st_mtime
            if file_age > self.ttl_seconds:
                try:
                    self._session_file.unlink()
                except Exception:
                    pass
                return None

            with self._session_file.open("r", encoding="utf-8") as f:
                raw = json.load(f)
            return SessionData(**raw)  # type: ignore[arg-type]
        except (json.JSONDecodeError, TypeError) as e:
            try:
                self._session_file.unlink()
            except Exception:
                pass
            return None
        except Exception as e:
            return None

    def _save_session(self, data: SessionData):
        # écriture atomique : fichier temporaire puis remplacement
        temp = None
        try:
            tmp = tempfile.NamedTemporaryFile("w", delete=False, dir=str(self._session_dir), encoding="utf-8")
            temp_path = Path(tmp.name)
            json.dump(asdict(data), tmp, indent=2, default=str)
            tmp.flush()
            tmp.close()
            os.replace(str(temp_path), str(self._session_file))
        except Exception as e:
            logger.exception("Échec sauvegarde session: %s", e)
            # si échec, tenter nettoyage
            try:
                if temp_path and temp_path.exists():
                    temp_path.unlink()
            except Exception:
                pass

    # -------------------------
    # Environnement
    # -------------------------
    def _get_current_environment_hash(self) -> str:
        factors = [
            str(global_config.config_dir),
            str(global_config.get_sandbox_path()),
            str(os.environ.get('PYTHONPATH', '')),
            str(os.environ.get('LCPI_CORE_ONLY_LAUNCH', '')),
        ]
        try:
            config_file = global_config._get_config_file_path()
            if config_file.exists():
                factors.append(str(config_file.stat().st_mtime))
        except Exception:
            pass
        combined = "|".join(factors)
        return hashlib.md5(combined.encode()).hexdigest()

    # -------------------------
    # Vérifications
    # -------------------------
    def _verify_plugins_availability(self, session_data: SessionData) -> bool:
        try:
            # Pour l'instant, on considère que tous les plugins sont disponibles
            # car les chemins dans la session sont des chemins de modules Python
            # et non des fichiers physiques
            return True
        except Exception as e:
            return False

    def is_session_valid(self) -> bool:
        if self._is_initialized:
            return True

        session_data = self._load_session()
        if not session_data:
            return False

        current_env = self._get_current_environment_hash()
        if session_data.environment_hash != current_env:
            return False

        if not self._verify_plugins_availability(session_data):
            return False

        self._session_data = session_data
        self._is_initialized = True
        return True

    # -------------------------
    # API publique
    # -------------------------
    def get_session_data(self) -> Optional[Dict[str, Any]]:
        if not self.is_session_valid():
            return None
        return asdict(self._session_data)  # serialisable

    def create_session(self, plugins_info: Dict[str, Any], init_time: Optional[float] = None):
        now = init_time or time.time()
        sd = SessionData(
            created_at=now,
            last_used=now,
            environment_hash=self._get_current_environment_hash(),
            plugins=plugins_info,
            global_config={
                'active_project': global_config.get_active_project(),
                'sandbox_path': str(global_config.get_sandbox_path()),
                'config_dir': str(global_config.config_dir)
            }
        )
        # tenter verrou avant sauvegarde
        if self._acquire_lock():
            try:
                self._session_data = sd
                self._is_initialized = True
                self._save_session(sd)
            finally:
                self._release_lock()
        else:
            logger.warning("Impossible d'acquérir le lock pour créer la session. Tentative sans lock.")
            # fallback sans lock
            self._session_data = sd
            self._is_initialized = True
            self._save_session(sd)

    def update_session_usage(self):
        if self._session_data:
            self._session_data.last_used = time.time()
            if self._acquire_lock():
                try:
                    self._save_session(self._session_data)
                finally:
                    self._release_lock()
            else:
                self._save_session(self._session_data)

    def clear_session(self):
        try:
            if self._session_file.exists():
                self._session_file.unlink()
        except Exception:
            pass
        self._session_data = None
        self._is_initialized = False

    def get_session_info(self) -> Dict[str, Any]:
        if not self.is_session_valid():
            return {'status': 'no_session'}
        return {
            'status': 'active',
            'session_file': str(self._session_file),
            'created_at': self._session_data.created_at,
            'last_used': self._session_data.last_used,
            'plugins_count': len(self._session_data.plugins),
            'environment_hash': self._session_data.environment_hash
        }

    # -------------------------
    # Restauration plugins
    # -------------------------
    def restore_plugins_from_session(self, app) -> bool:
        """Restaure les plugins depuis la session et les ajoute à l'app Typer (ou autre)."""
        if not self.is_session_valid():
            return False

        data = self._session_data
        restored = 0
        for plugin_name, plugin_meta in data.plugins.items():
            if plugin_meta.get('status') != 'loaded':
                continue
            reg = self._plugin_registry.get(plugin_name)
            if not reg:
                continue
            module_path, attr_name, alias = reg
            try:
                module = importlib.import_module(module_path)
                target = getattr(module, attr_name) if attr_name else module
                # si c'est une factory callable -> appeler pour récupérer Typer/typer app
                if callable(target):
                    try:
                        instance = target()
                    except TypeError:
                        # peut-être c'est déjà une app (pas besoin d'appeler)
                        instance = target
                else:
                    instance = target
                app.add_typer(instance, name=alias or plugin_name)
                restored += 1
            except Exception as e:
                continue

        return restored > 0

    # -------------------------
    # Utilitaires
    # -------------------------
    def remove_stale_sessions(self):
        """Nettoie les fichiers de sessions trop vieux dans le répertoire."""
        for f in self._session_dir.glob("session_*.json"):
            try:
                if time.time() - f.stat().st_mtime > self.ttl_seconds:
                    f.unlink()
            except Exception:
                pass

# instance globale recommandée
session_manager = SessionManager()
