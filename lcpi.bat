@echo off
REM Script batch pour LCPI-CLI avec tous les plugins
REM Placez ce fichier dans un répertoire du PATH ou utilisez-le directement

REM Déterminer le répertoire du script
set "SCRIPT_DIR=%~dp0"

REM Activer l'environnement virtuel s'il existe
if exist "%SCRIPT_DIR%.venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%.venv\Scripts\activate.bat"
)

REM Lancer LCPI-CLI avec tous les plugins
python "%SCRIPT_DIR%src\lcpi\__main__.py" %*

REM Si Python n'est pas trouvé, essayer avec python3
if errorlevel 1 (
    python3 "%SCRIPT_DIR%src\lcpi\__main__.py" %*
) 