import sys
from pathlib import Path

# Ensure src/ is importable and make this module act like a package proxy for `lcpi.*`
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# Expose package path so that `import lcpi.aep` works even if this file shadows the package
try:
    pkg_dir = SRC / "lcpi"
    if pkg_dir.exists():
        __path__ = [str(pkg_dir)]  # type: ignore[attr-defined]
except Exception:
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "shell":
        # Lancer le mode interactif REPL
        try:
            from src.lcpi.shell.main import main as shell_main
            shell_main()
        except ImportError as e:
            print("[ERREUR] Impossible de lancer le shell interactif :", e)
            sys.exit(1)
    else:
        # Lancer la CLI classique
        try:
            from src.lcpi.main import app
            # Appeler l'application avec un nom de programme explicite pour un usage clair
            app(prog_name="lcpi")
        except ImportError as e:
            print("[ERREUR] Impossible de lancer la CLI classique :", e)
            sys.exit(1)