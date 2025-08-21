# tools/simulate_progress_events.py
import time
from pathlib import Path

# Import ton module progress_ui (adapter name selon ton projet)
try:
    from lcpi.core.progress_ui import RichProgressManager  # adapte si nom différent
except Exception as e:
    print("Impossible d'importer progress_ui:", e)
    raise SystemExit(2)

def fake_run():
    with RichProgressManager() as ui:
        ui.setup_tasks(total_generations=5, population_size=10)
        # run_start
        ui.update("run_start", {"generations": 5, "population": 10})
        for g in range(5):
            ui.update("generation_start", {"generation": g, "total_generations": 5, "population_size": 10})
            for i in range(1, 11):
                ui.update("individual_start", {"generation": g, "index": i, "population_size": 10})
                time.sleep(0.02)
                ui.update("individual_end", {"generation": g, "index": i, "cost": 1e6/(g+1+i)})
            ui.update("generation_end", {"generation": g, "best_cost": float(1000000/(g+1))})
        ui.update("best_updated", {"best_cost": 123456.0})
        ui.update("complete", {"result": {}})
        time.sleep(0.3)

if __name__ == "__main__":
    fake_run()
    print("Simulation events done.")
