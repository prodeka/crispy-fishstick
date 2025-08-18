@echo off
REM Script de build pour créer un exécutable portable LCPI-CLI

echo 🚀 Construction de l'executable portable LCPI-CLI...
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

echo 🔨 Construction de l'executable...

REM Construire avec PyInstaller
pyinstaller --clean --onefile --console --name=lcpi --distpath=dist --workpath=build src/lcpi/main.py

if errorlevel 1 (
    echo ❌ Erreur lors de la construction
    pause
    exit /b 1
)

echo.
echo ✅ Construction reussie !
echo.

REM Vérifier que l'exécutable existe
if exist dist\lcpi.exe (
    echo 🎉 Executable cree: dist\lcpi.exe
    
    REM Afficher la taille
    for %%A in (dist\lcpi.exe) do echo 📦 Taille: %%~zA bytes
    
    echo.
    echo 🧪 Test de l'executable...
    dist\lcpi.exe --help
    
    echo.
    echo 🎉 Deploiement reussi !
    echo 📁 L'executable se trouve dans le dossier 'dist'
    echo 🚀 Vous pouvez maintenant distribuer l'executable 'lcpi.exe'
) else (
    echo ❌ L'executable n'a pas ete cree
)

echo.
pause
