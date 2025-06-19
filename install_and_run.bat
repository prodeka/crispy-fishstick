@echo off
setlocal

set VENV_DIR=venv
set PACKAGES_DIR=vendor\packages

echo "--- Script de lancement et d'installation 100 OFFLINE pour Windows ---"

:: Verifier si Python est disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo "ERREUR: Python n'est pas installe ou n'est pas dans le PATH."
    pause
    exit /b 1
)

:: Creer l'environnement virtuel s'il n'existe pas
if not exist "%VENV_DIR%" (
    echo "Creation de l'environnement virtuel..."
    python -m venv %VENV_DIR%
)

:: Activer l'environnement virtuel
call "%VENV_DIR%\Scripts\activate.bat"

:: Installer les dependances depuis le dossier local
pip install --no-index --find-links="%PACKAGES_DIR%" -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo "ERREUR: L'installation des dependances locales a echoue."
    pause
    exit /b 1
)

echo "Dependances installees avec succes."
echo "Lancement du programme principal..."

:: LA LIGNE CORRIGÉE : %* transmet tous les arguments (comme -v) au script Python
python main.py %*

echo "Programme termine."
endlocal
pause