from src.lcpi.aep.optimizer.db import PriceDB

db = PriceDB()
print("Exemples de données:")
for i, d in enumerate(db._candidate_diameters[:3]):
    print(f"{i+1}. {d.dict()}")

print(f"\nMatériaux uniques trouvés:")
materials = set(d.material for d in db._candidate_diameters)
for mat in sorted(materials):
    count = len([d for d in db._candidate_diameters if d.material == mat])
    print(f"  {mat}: {count} diamètres")
