#!/usr/bin/env python3
"""
Script pour comparer les rapports multi-solveurs
"""

import webbrowser
from pathlib import Path

def open_reports():
    """Ouvre les deux rapports dans le navigateur"""
    
    old_report = Path("results/out_multi_tabs.html")
    new_report = Path("results/out_multi_tabs_improved.html")
    
    if old_report.exists():
        print(f"🌐 Ouverture de l'ancien rapport: {old_report}")
        webbrowser.open(f"file://{old_report.absolute()}")
    
    if new_report.exists():
        print(f"🌐 Ouverture du nouveau rapport: {new_report}")
        webbrowser.open(f"file://{new_report.absolute()}")
    
    print("📋 Comparaison:")
    print("  - Ancien rapport: out_multi_tabs.html")
    print("  - Nouveau rapport: out_multi_tabs_improved.html")

if __name__ == "__main__":
    open_reports()
