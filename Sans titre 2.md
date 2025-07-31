╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ Licence activée avec succès pour Test User (valide jusqu'au 2025-08-30)                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✅ Licence valide pour Test User
📅 Valide jusqu'au : 2025-08-30 07:51:48
⏱️  Jours restants : 29
🏷️  Type : standard
--- Initialisation de LCPI-CLI ---
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\prota\AppData\Roaming\Python\Python313\Scripts\lcpi.exe\__main__.py", line 4, in <module>
    from lcpi.main import app
  File "G:\Mon Drive\Other\PROJET_DIMENTIONEMENT_2\src\lcpi\main.py", line 291, in <module>
    print_plugin_status()
    ~~~~~~~~~~~~~~~~~~~^^
  File "G:\Mon Drive\Other\PROJET_DIMENTIONEMENT_2\src\lcpi\main.py", line 254, in print_plugin_status
    from .cm.main import register as register_cm
  File "G:\Mon Drive\Other\PROJET_DIMENTIONEMENT_2\src\lcpi\cm\main.py", line 120
    db_path = Path(__file__).parent.parent / "db" / "cm_bois.json"
    ^^^^^^^
IndentationError: expected an indented block after 'try' statement on line 119
PS C:\Users\prota>