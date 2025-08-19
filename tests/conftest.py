import os
import sys
from pathlib import Path

# Ensure src/ is on sys.path for imports like `from lcpi...`
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
	sys.path.insert(0, str(SRC))

# Avoid collision with top-level `lcpi.py` module shadowing the `lcpi` package
if "lcpi" in sys.modules:
	mod = sys.modules.get("lcpi")
	mod_file = getattr(mod, "__file__", "")
	if mod_file and Path(mod_file).name == "lcpi.py":
		del sys.modules["lcpi"]

# Push repository root to the end of sys.path to prefer `src/` package resolution
sys.path = ([str(SRC)] + [p for p in sys.path if Path(p).resolve() != ROOT.resolve()] + [str(ROOT)])

# Also set PYTHONPATH env for subprocesses if any
cur = os.environ.get("PYTHONPATH", "")
os.environ["PYTHONPATH"] = (str(SRC) if not cur else f"{str(SRC)}{os.pathsep}{cur}")
