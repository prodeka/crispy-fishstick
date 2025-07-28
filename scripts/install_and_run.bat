 
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
python -m pip install --no-index --find-links=./wheels -r requirements.txt

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

REM Lance le programme principal
python main.py

echo.
echo Le programme s'est termine. Appuyez sur une touche pour fermer.
pause