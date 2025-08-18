@echo off
REM Script de build pour créer un exécutable portable LCPI-CLI
REM Version optimisée avec --onedir pour un démarrage rapide

echo 🚀 Construction de l'executable portable LCPI-CLI (mode rapide)...
echo 📁 Mode --onedir pour un demarrage ultra-rapide
echo.

REM Vérifier que PyInstaller est installé
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ❌ PyInstaller n'est pas installe. Installation...
    pip install pyinstaller
)

REM Nettoyer les anciens builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

echo 🧹 Nettoyage des anciens builds termine
echo.

echo 🔨 Construction de l'executable (mode --onedir)...

REM Construire avec PyInstaller en mode --onedir
echo 🔧 Commande PyInstaller executee :
echo pyinstaller --clean --onedir --console --name=lcpi --distpath=dist --workpath=build --log-level=DEBUG ..\src\lcpi\__main__.py
echo.
echo 📋 Sortie en temps reel :
echo ----------------------------------------
pyinstaller --clean --onedir --console --name=lcpi --distpath=dist --workpath=build --log-level=DEBUG ..\src\lcpi\__main__.py
echo ----------------------------------------

if errorlevel 1 (
    echo ❌ Erreur lors de la construction
    pause
    exit /b 1
)

echo.
echo ✅ Construction reussie !
echo.

REM Vérifier que l'exécutable existe
if exist dist\lcpi\lcpi.exe (
    echo 🎉 Executable cree: dist\lcpi\lcpi.exe
    
    REM Afficher la taille du dossier
    echo 📦 Taille du dossier dist\lcpi:
    dir dist\lcpi /s | find "File(s)"
    
    echo.
    echo ⚡ Demarrage ultra-rapide (2-5 secondes)
    echo 📁 Dossier complet: dist\lcpi
    echo.
    
    REM Créer un script de lancement rapide
    echo @echo off > lcpi_launcher.bat
    echo REM Lanceur rapide pour LCPI-CLI >> lcpi_launcher.bat
    echo REM Demarrage ultra-rapide en mode --onedir >> lcpi_launcher.bat
    echo "dist\lcpi\lcpi.exe" %%* >> lcpi_launcher.bat
    
    echo 🚀 Script de lancement cree: lcpi_launcher.bat
    echo.
    
    echo 🧪 Test de l'executable...
    dist\lcpi\lcpi.exe --help
    
    echo.
    echo 🎉 Deploiement reussi !
    echo 📁 L'executable se trouve dans le dossier 'dist\lcpi'
    echo ⚡ Demarrage ultra-rapide (2-5 secondes)
    echo 🚀 Utilisez 'lcpi_launcher.bat' pour lancer rapidement
    echo 📋 Ou naviguez dans 'dist\lcpi' et double-cliquez sur 'lcpi.exe'
) else (
    echo ❌ L'executable n'a pas ete cree
)

echo.
pause
