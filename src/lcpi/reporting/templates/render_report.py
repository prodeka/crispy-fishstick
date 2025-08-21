#!/usr/bin/env python3
# scripts/render_report.py
import json, sys
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

TEMPLATES_DIR = Path('templates')

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(['html','xml','md','jinja'])
)

def load_sample():
    # Minimal sample data (remplace par ton JSON complet)
    return {
      "project": {
        "title": "Projet Exemple",
        "tables": {
          "enumeration_troncons": [
            {"DC_ID":"T001","longueur":120.5,"NODE1":"N1","NODE2":"N2"},
            {"DC_ID":"T002","longueur":80,"NODE1":"N2","NODE2":"N3"}
          ],
          "dimensionnement_troncons": [
            {"DC_ID":"T001","longueur":120.5,"Qd (m^3/s)":0.05,"DN (mm)":90,"V (m/s)":0.8,"ΔH (m)":0.5}
          ],
          "dimensionnement_noeuds": [
            {"JUNCTIONS":"N1","X":123.0,"Y":456.0,"Z (m)":10.0,"P_réel (m)":25.0}
          ],
          "recap_reservoir": {
            "ID": "RES1",
            "X": 123.4,
            "Y": 456.7,
            "type": "Aérien",
            "volume_tot_m3": 500.0,
            "hauteur_tot_m": 6.0,
            "h_min_m": 1.0,
            "h_max_m": 6.0,
            "surface_m2": 80.0,
            "niveau_initial_m": 4.5,
            "reserve_utile_m3": 350.0,
            "coord_sys": "WGS84",
            "construction": "béton",
            "remarques": "Exemple"
          },
          "comparatif_diametres_debits": [],
          "comparatif_vitesses_pertes": [],
          "comparatif_pressions": [],
          "recap_diametres_conduites": [],
          "devis_estimatif": [
            {"N°":1,"Désignations":"Tuyau PVC 90mm","Unité":"m","Quantité":200,"Prix Unitaire":1200,"MONTANT":240000}
          ]
        }
      },
      "meta": {"best_cost":"1 234 567 FCFA","method":"genetic","version":"v1","constraints":{},"source_meta":{}},
      "generation_date": "2025-08-20",
      "result": {"proposals":[]},
      "report_payload": {}
    }

def render(out_path='out_report.html', data=None):
    tpl = env.get_template('report_base.html')
    html = tpl.render(**(data or load_sample()), report_payload=(data or {}).get('report_payload', {}))
    Path(out_path).write_text(html, encoding='utf-8')
    print("Wrote", out_path)

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'out_report.html'
    data_path = sys.argv[2] if len(sys.argv) > 2 else None
    if data_path:
        d = json.loads(Path(data_path).read_text(encoding='utf-8'))
    else:
        d = load_sample()
    render(out, d)
