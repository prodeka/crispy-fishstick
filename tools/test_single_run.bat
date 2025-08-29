@echo off
setlocal enabledelayedexpansion

echo.
echo [94m╔══════════════════════════════════════════════════════════════╗[0m
echo [94m║                TEST UNIQUE D'OPTIMISATION                 ║[0m
echo [94m║                    hmax=100, g=10, p=20                   ║[0m
echo [94m╚══════════════════════════════════════════════════════════════╝[0m
echo.

echo [92m🚀 Test: hmax=100, generations=10, population=20[0m
echo [94mCommande: python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 10 --population 20 --solver epanet --verbose --show-stats --output test_debug.json --hmax 100[0m
echo.

cd test_validation

python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 10 --population 20 --solver epanet --verbose --show-stats --output test_debug.json --hmax 100

if %ERRORLEVEL% neq 0 (
    echo [91m❌ Test échoué avec le code d'erreur %ERRORLEVEL%[0m
) else (
    echo [92m✅ Test terminé avec succès[0m
)

echo.
echo [94mAppuyez sur une touche pour fermer...[0m
pause >nul
