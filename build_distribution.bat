@echo off
REM Script de lancement principal pour la création de distribution LCPI-CLI
REM Redirige vers le script dans le dossier scripts/

echo 🚀 Lancement du script de distribution LCPI-CLI...
echo 📂 Script : scripts\create_distribution.py
echo.

REM Vérifier que le script existe
if not exist "scripts\create_distribution.py" (
    echo ❌ Script de distribution non trouvé :
    echo    scripts\create_distribution.py
    echo.
    echo 📁 Vérifiez que le fichier existe dans le dossier scripts/
    pause
    exit /b 1
)

REM Lancer le script de distribution
python scripts\create_distribution.py

REM Afficher le résultat
if errorlevel 1 (
    echo.
    echo ❌ Erreur lors de l'exécution du script
    pause
    exit /b 1
) else (
    echo.
    echo ✅ Script de distribution terminé avec succès
    pause
)
