from __future__ import annotations

import random
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib

try:
    import numpy as np
    from sklearn.ensemble import RandomForestRegressor
    SKLEARN_OK = True
except ImportError:
    SKLEARN_OK = False

from ..cache import OptimizationCache, _stable_json, _sha256_of_text
from ..io import NetworkModel
from .nested import NestedGreedyOptimizer
from ..models import OptimizationResult, Proposal, TankDecision

MODEL_STORE_DIR = Path("data/model_store")
MODEL_STORE_DIR.mkdir(parents=True, exist_ok=True)


def lhs_samples(n: int, bounds: Tuple[float, float]) -> List[float]:
    low, high = float(bounds[0]), float(bounds[1])
    return [low + (i + random.random()) * (high - low) / n for i in range(n)]


class SurrogateOptimizer:
    def __init__(self, network_model: NetworkModel, config: Dict[str, Any]):
        if not SKLEARN_OK:
            raise ImportError("Scikit-learn est requis pour le SurrogateOptimizer.")
        
        self.network = network_model
        self.config = config
        self.solver = config.get("solver", "lcpi")
        self.model: Optional[RandomForestRegressor] = None
        self.dataset: List[Tuple[float, float]] = []  # (H, min_pressure)
        cache_dir = config.get("cache_dir")
        if cache_dir:
            self.cache = OptimizationCache(Path(cache_dir))
        else:
            # Utiliser un cache temporaire si aucun répertoire n'est spécifié
            self.cache = OptimizationCache(Path("temp/cache"))
        self.model_path = self._get_model_path()

        if self.config.get("surrogate_config", {}).get("persist_model", True):
            self._load_model()

    def _get_model_path(self) -> Path:
        """Crée un chemin de fichier unique pour le modèle basé sur le hash du réseau."""
        network_hash = _sha256_of_text(_stable_json(self.network.dict()))
        return MODEL_STORE_DIR / f"surrogate_model_{network_hash}.joblib"

    def _load_model(self):
        if self.model_path.exists():
            try:
                self.model = joblib.load(self.model_path)
                print(f"Modèle de substitution pré-entraîné chargé depuis {self.model_path}")
            except Exception as e:
                print(f"Erreur lors du chargement du modèle : {e}")
                self.model = None

    def _save_model(self):
        """Sauvegarde le modèle et ses métadonnées."""
        if self.model is not None and self.config.get("surrogate_config", {}).get("persist_model", True):
            try:
                # Sauvegarder le modèle
                joblib.dump(self.model, self.model_path)
                
                # Sauvegarder les métadonnées
                metadata = {
                    "name": self.model_path.stem,
                    "type": "RandomForestRegressor",
                    "features": getattr(self.model, 'feature_names_in_', []),
                    "training_date": datetime.now().isoformat(),
                    "performance": self._get_model_performance(),
                    "dataset_size": len(self.dataset),
                    "config": self.config
                }
                
                metadata_path = self.model_path.with_suffix('.json')
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2, default=str)
                
                print(f"✅ Modèle et métadonnées sauvegardés : {self.model_path}")
                
            except Exception as e:
                print(f"⚠️ Erreur lors de la sauvegarde du modèle : {e}")
    
    def _get_model_performance(self) -> Dict[str, Any]:
        """Retourne les métriques de performance du modèle."""
        if self.model is None or not self.dataset:
            return {}
        
        try:
            # Calculer les prédictions sur le dataset d'entraînement
            X = np.array([[h] for h, _ in self.dataset])
            y_true = np.array([p for _, p in self.dataset])
            y_pred = self.model.predict(X)
            
            # Calculer les métriques de performance
            from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
            
            mse = mean_squared_error(y_true, y_pred)
            mae = mean_absolute_error(y_true, y_pred)
            r2 = r2_score(y_true, y_pred)
            
            return {
                "mse": float(mse),
                "mae": float(mae),
                "r2": float(r2),
                "rmse": float(np.sqrt(mse))
            }
        except Exception:
            return {}
    
    def list_available_models(self) -> List[Dict[str, Any]]:
        """Liste tous les modèles disponibles avec leurs métadonnées."""
        available_models = []
        
        if not MODEL_STORE_DIR.exists():
            return available_models
        
        for model_file in MODEL_STORE_DIR.glob("*.joblib"):
            metadata_file = model_file.with_suffix('.json')
            
            model_info = {
                "name": model_file.stem,
                "model_path": str(model_file),
                "size_mb": model_file.stat().st_size / (1024 * 1024),
                "created": model_file.stat().st_ctime
            }
            
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    model_info.update(metadata)
                except Exception:
                    pass
            
            available_models.append(model_info)
        
        return available_models
    
    def delete_model(self, model_name: str) -> bool:
        """Supprime un modèle et ses métadonnées."""
        try:
            model_path = MODEL_STORE_DIR / f"{model_name}.joblib"
            metadata_path = MODEL_STORE_DIR / f"{model_name}.json"
            
            if model_path.exists():
                model_path.unlink()
            
            if metadata_path.exists():
                metadata_path.unlink()
            
            print(f"✅ Modèle {model_name} supprimé")
            return True
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la suppression du modèle {model_name}: {e}")
            return False

    def _simulate_min_pressure(self, H: float, pressure_min_m: float) -> float:
        # On s'assure que H_tanks est un dict pour le cache
        h_tanks = {"tank1": H} # Placeholder pour le nom du tank
        # Utilise le cache si possible
        cached = self.cache.get(self.network.dict(), h_tanks, {})
        if cached and "min_pressure_m" in cached:
            return float(cached["min_pressure_m"])
        
        # Sinon, exécute la simulation (via NestedGreedy pour une évaluation rapide)
        opt = NestedGreedyOptimizer(self.network, solver=self.solver)
        res = opt.optimize_nested((H, H), pressure_min_m=pressure_min_m)
        p_min = 0.0
        if isinstance(res, dict):
            p_min = float(res.get("binary", {}).get("min_pressure_m", 0.0)) if isinstance(res.get("binary"), dict) else 0.0
        
        self.cache.set(self.network.dict(), h_tanks, {}, {"min_pressure_m": p_min})
        return p_min

    def build_and_optimize(self) -> OptimizationResult:
        cfg = self.config.get("surrogate_config", {})
        h_bounds = list(self.config["h_bounds_m"].values())[0]
        pressure_min_m = self.config["pressure_min_m"]
        n_initial = cfg.get("initial_samples", 20)
        rounds = cfg.get("active_learning_rounds", 3)
        top_k = cfg.get("top_k_candidates", 5)
        grid_points = cfg.get("grid_points", 200)

        if self.model is not None:
            n_initial = max(5, n_initial // 4)

        # Étape 1: Dataset initial
        if not self.dataset:
            Hs = lhs_samples(n_initial, h_bounds)
            for H in Hs:
                p_min = self._simulate_min_pressure(H, pressure_min_m)
                self.dataset.append((H, p_min))

        # Étape 2 & 3: Boucle d'apprentissage actif
        for _ in range(max(1, rounds)):
            X = np.array([[h] for h, _ in self.dataset])
            y = np.array([p for _, p in self.dataset])
            self.model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            self.model.fit(X, y)

            grid = np.linspace(h_bounds[0], h_bounds[1], grid_points).reshape(-1, 1)
            pred = self.model.predict(grid)
            order = np.argsort(-pred)
            candidates = [float(grid[i][0]) for i in order[:max(1, top_k)]]

            for hc in candidates:
                p_min_c = self._simulate_min_pressure(hc, pressure_min_m)
                if (hc, p_min_c) not in self.dataset:
                    self.dataset.append((hc, p_min_c))

        self._save_model()

        # Étape 4: Validation finale
        feasible_points = [(h, p) for h, p in self.dataset if p >= pressure_min_m]
        if not feasible_points:
            return OptimizationResult(
                proposals=[],
                pareto_front=None,
                metadata={
                    "method": "surrogate_optimization",
                    "error": "Aucun point faisable trouvé par le surrogate",
                    "dataset_size": len(self.dataset),
                    "feasible": False
                }
            )

        best_h = sorted(feasible_points, key=lambda x: x[0])[0][0] # La plus petite hauteur faisable
        final_result = NestedGreedyOptimizer(self.network, solver=self.solver).optimize_nested(
            (best_h, best_h), pressure_min_m=pressure_min_m
        )

        # Si le résultat final est déjà au format V11, l'utiliser directement
        if isinstance(final_result, OptimizationResult):
            # Mettre à jour les métadonnées avec les informations du surrogate
            final_result.metadata.update({
                "method": "surrogate_optimization",
                "surrogate_dataset_size": len(self.dataset),
                "surrogate_rounds": rounds,
                "surrogate_initial_samples": n_initial,
                "surrogate_top_k": top_k,
                "surrogate_grid_points": grid_points
            })
            return final_result
        else:
            # Créer une proposition au format V11 si le résultat n'est pas au bon format
            tank_decision = TankDecision(
                id="TANK1",  # À adapter selon le réseau
                H_m=best_h
            )

            proposal = Proposal(
                name="surrogate_solution",
                is_feasible=True,
                tanks=[tank_decision],
                diameters_mm=final_result.get("diameters_mm", {}),
                costs=final_result.get("costs", {}),
                metrics={
                    "min_pressure_m": pressure_min_m,
                    "surrogate_dataset_size": len(self.dataset)
                }
            )

            return OptimizationResult(
                proposals=[proposal],
                pareto_front=None,
                metadata={
                    "method": "surrogate_optimization",
                    "network_file": str(getattr(self.network, 'file_path', 'unknown')),
                    "surrogate_dataset_size": len(self.dataset),
                    "surrogate_rounds": rounds,
                    "surrogate_initial_samples": n_initial,
                    "surrogate_top_k": top_k,
                    "surrogate_grid_points": grid_points,
                    "best_h_tank_m": best_h,
                    "final_result": final_result
                }
            )