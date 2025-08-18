@echo off
REM Script de lancement LCPI-CLI pour Windows
REM Utilise: lcpi [command] [options]

REM Déterminer le répertoire du script (chemin absolu)
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Ajouter le répertoire src au PYTHONPATH
set PYTHONPATH=%SCRIPT_DIR%\src;%PYTHONPATH%

REM Changer vers le répertoire du script
cd /d "%SCRIPT_DIR%"

REM Lancer LCPI
python -m src.lcpi %* 