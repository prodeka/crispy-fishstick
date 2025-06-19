# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),                  # Indispensable pour les modèles de pluie
        ('repports/graphics', 'repports/graphics'), # Crée le sous-dossier pour les images
        ('repports/calcul_notes', 'repports/calcul_notes'), # Crée le sous-dossier pour les PDF
        ('IN CSV', 'IN CSV')                   # Inclut les exemples de fichiers CSV
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# La section EXE définit l'exécutable final.
# L'absence d'une section COLLECT indique à PyInstaller de créer un seul fichier.
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='HydroApp', # Le nom de votre exécutable final
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # Important : assure que la console s'ouvre
    runtime_tmpdir=None,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)