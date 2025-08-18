import os
import sys
from pathlib import Path

# Ensure src/ is on sys.path for imports like `from lcpi...`
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
	sys.path.insert(0, str(SRC))

# Also set PYTHONPATH env for subprocesses if any
cur = os.environ.get("PYTHONPATH", "")
os.environ["PYTHONPATH"] = (str(SRC) if not cur else f"{str(SRC)}{os.pathsep}{cur}")
