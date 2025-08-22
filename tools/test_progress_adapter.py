#!/usr/bin/env python3
"""
Petit script de test pour valider le progress adapter créé dans OptimizationController.
Usage: python tools/test_progress_adapter.py
"""

import time
from pathlib import Path
import json
import sys

# Ajuster le sys.path pour importer depuis src/
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

from src.lcpi.aep.optimizer.controllers import OptimizationController


def ui_callback(evt, data):
    t = time.strftime("%H:%M:%S")
    try:
        payload = json.dumps(data, default=str)
    except Exception:
        payload = str(data)
    print(f"[{t}] UI Callback <- evt='{evt}' data={payload}")


def main():
    ctrl = OptimizationController()
    # On réutilise l'adaptateur défini dans controllers.py si exposé
    adapter = None
    try:
        # Si une méthode d'instance a été ajoutée
        if hasattr(ctrl, "_make_progress_adapter"):
            adapter = ctrl._make_progress_adapter(ui_callback)  # type: ignore
    except Exception:
        adapter = None
    if adapter is None:
        from src.lcpi.aep.optimizer.controllers import _make_progress_adapter as _factory
        adapter = _factory(ui_callback)

    print("Adapter créé. Envoi d'une séquence d'événements simulés...")

    adapter("run_start", {"method": "genetic", "solver": "epanet"})
    time.sleep(0.1)
    adapter("generation_start", {"generation": 0, "total_generations": 3, "population_size": 5})
    time.sleep(0.05)
    adapter("sim_start", {"info": "starting epanet call"})
    time.sleep(0.05)
    adapter("individual_start", {"generation": 0, "index": 1})
    time.sleep(0.05)
    adapter("individual_end", {"generation": 0, "index": 1, "cost": 12345, "fitness": 0.001})
    time.sleep(0.05)
    adapter("sim_done", {"info": "epanet finished"})
    time.sleep(0.05)
    adapter("individual_start", {"generation": 0, "index": 2})
    adapter("individual_end", {"generation": 0, "index": 2, "cost": 12000, "fitness": 0.002})
    time.sleep(0.05)
    adapter("generation_end", {"generation": 0, "best_cost": 12000})
    time.sleep(0.05)
    adapter("generation_start", {"generation": 1, "total_generations": 3, "population_size": 5})
    adapter("sim_start", {})
    adapter("sim_done", {})
    adapter("generation_end", {"generation": 1, "best_cost": 11000})
    adapter("complete", {"result": {"proposals": []}})
    print("Séquence terminée.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test rapide du progress adapter + UI handler.
Exécute une séquence d'événements et affiche les sorties.
"""

import time
import logging
import sys
import os

# Ajouter le répertoire racine au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.lcpi.aep.optimizer.controllers import _make_progress_adapter
    print("✅ Import réussi de _make_progress_adapter")
except Exception as e:
    print(f"❌ Impossible d'importer _make_progress_adapter: {e}")
    print(f"   sys.path: {sys.path[:3]}...")
    _make_progress_adapter = None


def fake_ui_callback(evt, data):
    print(f"[UI CALLBACK] evt={evt} data={data}")


def run_simulation_sequence(adapter):
    print("\n=== DÉBUT SÉQUENCE DE TEST ===")
    adapter("run_start", {"generations": 2, "population_size": 3})
    # Génération 0
    adapter("generation_start", {"generation": 0, "total_generations": 2, "population_size": 3})
    for i in range(1, 4):
        adapter("individual_start", {"generation": 0, "index": i, "population_size": 3})
        adapter("sim_start", {"generation": 0, "index": i})
        time.sleep(0.02)
        adapter("sim_done", {"generation": 0, "index": i, "success": True})
        adapter("individual_end", {"generation": 0, "index": i, "cost": 100000 + i})
    adapter("generation_end", {"generation": 0})
    # Génération 1
    adapter("generation_start", {"generation": 1, "total_generations": 2, "population_size": 3})
    for i in range(1, 4):
        adapter("individual_start", {"generation": 1, "index": i, "population_size": 3})
        adapter("individual_end", {"generation": 1, "index": i, "cost": 100500 + i})
    adapter("generation_end", {"generation": 1})
    adapter("run_end", {"status": "complete"})
    print("=== FIN SÉQUENCE DE TEST ===")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if _make_progress_adapter is None:
        print("❌ Adaptateur non disponible, patch non appliqué.")
        sys.exit(1)
    else:
        adapter = _make_progress_adapter(fake_ui_callback)
        print("✅ Lancement de la séquence de test (adapter -> fake_ui_callback)\n")
        run_simulation_sequence(adapter)


# tools/test_progress_adapter.py
from src.lcpi.aep.optimizer.controllers import _make_progress_adapter


def main():
	log = []
	def user_cb(evt, data):
		log.append((evt, data))
		print("progress adapter received:", evt, data)

	adapter = _make_progress_adapter(user_cb)
	# Sim start/done
	adapter("simulation_start", {})
	adapter("simulation_done", {"generation": 1, "index": 1})
	# Individuals
	adapter("individual_start", {"index": 0})
	adapter("individual_end", {"index": 1, "cost": 123.0})
	# Best updates
	adapter("best_improved", {"new_cost": 100.0})
	adapter("best_updated", {"best_cost": 95.0})
	# Unknown passthrough
	adapter("foo", {"bar": 1})

	assert any(e == "simulation" and d.get("stage") in ("running", "success") for e, d in log)
	assert any(e == "best_updated" for e, _ in log)
	print("OK")


if __name__ == "__main__":
	main()


