 
cd /d "%~dp0.."
@echo off
REM Script pour installer les dépendances hors ligne et lancer le programme
echo.
echo ==========================================================
echo    Installation des dependances locales (hors ligne)
echo ==========================================================
echo.

REM Utilise la version de python accessible dans le PATH.
REM --no-index empêche pip de chercher sur internet.
REM --find-links indique à pip de chercher les paquets dans le dossier 'wheels'.
python -m pip install --no-index --find-links=./wheels -r "%~dp0..\requirements.txt"

REM Vérifie si l'installation a réussi
if %errorlevel% neq 0 (
    echo.
    echo ERREUR : L'installation des dependances a echoue.
    echo Veuillez verifier que Python et pip sont correctement installes.
    pause
    exit /b %errorlevel%
)

echo.
echo ==========================================================
echo    Installation terminee. Lancement du programme...
echo ==========================================================
echo.

REM Ajoute le répertoire src au PYTHONPATH pour que Python trouve le module nanostruct
set PYTHONPATH=%CD%\src;%PYTHONPATH%

REM Lance le programme principal
python -m nanostruct.main_app

echo.
echo Le programme s'est termine. Appuyez sur une touche pour fermer.
pause