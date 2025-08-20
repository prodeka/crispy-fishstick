from __future__ import annotations

from typing import List

from src.lcpi.aep.optimization.genetic_algorithm import GeneticOptimizer


class _FakeAlgoCfg:
    def __init__(self) -> None:
        self.population_size = 4
        self.generations = 3
        self.crossover_rate = 0.9
        self.mutation_rate = 0.0


class _FakeCriteres:
    def __init__(self) -> None:
        self.principal = "cout"
        self.poids = [1.0]
        self.secondaires: List[str] = []


class _FakeDiam:
    def __init__(self, d: int, c: float) -> None:
        self.diametre_mm = d
        self.cout_fcfa_m = c


class _FakeConfig:
    def __init__(self) -> None:
        self.algorithme = _FakeAlgoCfg()
        self.criteres = _FakeCriteres()
        self.diametres_candidats = [_FakeDiam(50, 100.0), _FakeDiam(63, 120.0), _FakeDiam(90, 200.0)]


class _FakeConstraintManager:
    def verifier_contraintes(self, individu, reseau_data):
        return True


def test_genetic_optimizer_calls_generation_hook():
    cfg = _FakeConfig()
    cm = _FakeConstraintManager()
    ga = GeneticOptimizer(cfg, cm)  # type: ignore[arg-type]

    calls = {"count": 0}

    def _cb(population, gen):
        calls["count"] += 1

    ga.set_on_generation_callback(_cb)

    reseau_data = {
        "conduites": [
            {"longueur_m": 100.0, "debit_m3_s": 0.05},
            {"longueur_m": 80.0, "debit_m3_s": 0.04},
        ]
    }

    out = ga.optimiser(reseau_data, nb_conduites=2)
    assert isinstance(out, dict)
    assert calls["count"] >= 1


