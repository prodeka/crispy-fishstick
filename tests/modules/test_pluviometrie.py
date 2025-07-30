import sys
import os
import json
import tempfile
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from lcpi.hydrodrain.calculs.pluviometrie import analyser_donnees_brutes, ajuster_loi_gumbel

def test_analyser_donnees_brutes():
    # Crée un fichier CSV temporaire
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        f.write('pluie\n100\n120\n90\n110\n130\n')
        f.flush()
        result = analyser_donnees_brutes(f.name)
        print("analyser_donnees_brutes:", json.dumps(result, indent=2, ensure_ascii=False))
    os.unlink(f.name)

def test_ajuster_loi_gumbel():
    series = [100, 120, 90, 110, 130]
    result = ajuster_loi_gumbel(series)
    print("ajuster_loi_gumbel:", json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_analyser_donnees_brutes()
    test_ajuster_loi_gumbel() 