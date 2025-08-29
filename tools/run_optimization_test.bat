@echo off
setlocal enabledelayedexpansion

:: Configuration
set TOTAL_TESTS=8
set CURRENT_TEST=0

:: Caractères pour le spinner
set "SPINNER_CHARS=|/-\"
set SPINNER_POS=0

:: Couleurs ANSI (si supportées)
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RED=[91m"
set "RESET=[0m"

echo.
echo %BLUE%╔══════════════════════════════════════════════════════════════╗%RESET%
echo %BLUE%║                TESTS D'OPTIMISATION LCPI AEP                ║%RESET%
echo %BLUE%║                    Comparaison hmax=100 vs 120              ║%RESET%
echo %BLUE%╚══════════════════════════════════════════════════════════════╝%RESET%
echo.

:: Fonction pour afficher le spinner
:spinner
set /a SPINNER_POS+=1
if !SPINNER_POS! geq 4 set SPINNER_POS=0
set "SPINNER=!SPINNER_CHARS:~%SPINNER_POS%,1!"
goto :eof

:: Fonction pour afficher la barre de progression
:progress_bar
set /a PERCENT=(%CURRENT_TEST% * 100) / %TOTAL_TESTS%
set /a BAR_LENGTH=%PERCENT% / 2
set "PROGRESS_BAR="
for /l %%i in (1,1,%BAR_LENGTH%) do set "PROGRESS_BAR=!PROGRESS_BAR!█"
for /l %%i in (%BAR_LENGTH%,1,50) do set "PROGRESS_BAR=!PROGRESS_BAR!░"
goto :eof

:: Fonction pour afficher le statut
:show_status
call :progress_bar
echo %YELLOW%[%SPINNER%] Test %CURRENT_TEST%/%TOTAL_TESTS% - %PERCENT%%% %RESET%
echo %BLUE%Progression: [%PROGRESS_BAR%]%RESET%
echo.
goto :eof

:: Début des tests
cd test_validation

:: Test 1/8: hmax=100, g=10, p=20
set /a CURRENT_TEST+=1
call :show_status
echo %GREEN%Test 1/8: hmax=100, generations=10, population=20%RESET%
echo %BLUE%Commande: python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 10 --population 20 --solver epanet --verbose --show-stats --output test_h100_g10_p20.json --hmax 100 --no-log%RESET%
echo.
python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 10 --population 20 --solver epanet --verbose --show-stats --output test_h100_g10_p20.json --hmax 100 --no-log
if %ERRORLEVEL% neq 0 (
    echo %RED%Test 1 echoue avec le code d'erreur %ERRORLEVEL%%RESET%
    goto :error_exit
)
echo %GREEN%Test 1 termine avec succes%RESET%
echo.

:: Test 2/8: hmax=120, g=10, p=20
set /a CURRENT_TEST+=1
call :show_status
echo %GREEN%Test 2/8: hmax=120, generations=10, population=20%RESET%
echo %BLUE%Commande: python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 10 --population 20 --solver epanet --verbose --show-stats --output test_h120_g10_p20.json --hmax 120 --no-log%RESET%
echo.
python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 10 --population 20 --solver epanet --verbose --show-stats --output test_h120_g10_p20.json --hmax 120 --no-log
if %ERRORLEVEL% neq 0 (
    echo %RED%Test 2 echoue avec le code d'erreur %ERRORLEVEL%%RESET%
    goto :error_exit
)
echo %GREEN%Test 2 termine avec succes%RESET%
echo.

:: Test 3/8: hmax=100, g=20, p=40
set /a CURRENT_TEST+=1
call :show_status
echo %GREEN%Test 3/8: hmax=100, generations=20, population=40%RESET%
echo %BLUE%Commande: python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 20 --population 40 --solver epanet --verbose --show-stats --output test_h100_g20_p40.json --hmax 100 --no-log%RESET%
echo.
python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 20 --population 40 --solver epanet --verbose --show-stats --output test_h100_g20_p40.json --hmax 100 --no-log
if %ERRORLEVEL% neq 0 (
    echo %RED%Test 3 echoue avec le code d'erreur %ERRORLEVEL%%RESET%
    goto :error_exit
)
echo %GREEN%Test 3 termine avec succes%RESET%
echo.

:: Test 4/8: hmax=120, g=20, p=40
set /a CURRENT_TEST+=1
call :show_status
echo %GREEN%Test 4/8: hmax=120, generations=20, population=40%RESET%
echo %BLUE%Commande: python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 20 --population 40 --solver epanet --verbose --show-stats --output test_h120_g20_p40.json --hmax 120 --no-log%RESET%
echo.
python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 20 --population 40 --solver epanet --verbose --show-stats --output test_h120_g20_p40.json --hmax 120 --no-log
if %ERRORLEVEL% neq 0 (
    echo %RED%Test 4 echoue avec le code d'erreur %ERRORLEVEL%%RESET%
    goto :error_exit
)
echo %GREEN%Test 4 termine avec succes%RESET%
echo.

:: Test 5/8: hmax=100, g=15, p=60
set /a CURRENT_TEST+=1
call :show_status
echo %GREEN%Test 5/8: hmax=100, generations=15, population=60%RESET%
echo %BLUE%Commande: python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 15 --population 60 --solver epanet --verbose --show-stats --output test_h100_g15_p60.json --hmax 100 --no-log%RESET%
echo.
python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 15 --population 60 --solver epanet --verbose --show-stats --output test_h100_g15_p60.json --hmax 100 --no-log
if %ERRORLEVEL% neq 0 (
    echo %RED%Test 5 echoue avec le code d'erreur %ERRORLEVEL%%RESET%
    goto :error_exit
)
echo %GREEN%Test 5 termine avec succes%RESET%
echo.

:: Test 6/8: hmax=120, g=15, p=60
set /a CURRENT_TEST+=1
call :show_status
echo %GREEN%Test 6/8: hmax=120, generations=15, population=60%RESET%
echo %BLUE%Commande: python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 15 --population 60 --solver epanet --verbose --show-stats --output test_h120_g15_p60.json --hmax 120 --no-log%RESET%
echo.
python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 15 --population 60 --solver epanet --verbose --show-stats --output test_h120_g15_p60.json --hmax 120 --no-log
if %ERRORLEVEL% neq 0 (
    echo %RED%Test 6 echoue avec le code d'erreur %ERRORLEVEL%%RESET%
    goto :error_exit
)
echo %GREEN%Test 6 termine avec succes%RESET%
echo.

:: Test 7/8: hmax=100, g=25, p=50
set /a CURRENT_TEST+=1
call :show_status
echo %GREEN%Test 7/8: hmax=100, generations=25, population=50%RESET%
echo %BLUE%Commande: python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 25 --population 50 --solver epanet --verbose --show-stats --output test_h100_g25_p50.json --hmax 100 --no-log%RESET%
echo.
python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 25 --population 50 --solver epanet --verbose --show-stats --output test_h100_g25_p50.json --hmax 100 --no-log
if %ERRORLEVEL% neq 0 (
    echo %RED%Test 7 echoue avec le code d'erreur %ERRORLEVEL%%RESET%
    goto :error_exit
)
echo %GREEN%Test 7 termine avec succes%RESET%
echo.

:: Test 8/8: hmax=120, g=25, p=50
set /a CURRENT_TEST+=1
call :show_status
echo %GREEN%Test 8/8: hmax=120, generations=25, population=50%RESET%
echo %BLUE%Commande: python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 25 --population 50 --solver epanet --verbose --show-stats --output test_h120_g25_p50.json --hmax 120 --no-log%RESET%
echo.
python -m lcpi.aep.cli network-optimize-unified bismark_inp.inp --method genetic --generations 25 --population 50 --solver epanet --verbose --show-stats --output test_h120_g25_p50.json --hmax 120 --no-log
if %ERRORLEVEL% neq 0 (
    echo %RED%Test 8 echoue avec le code d'erreur %ERRORLEVEL%%RESET%
    goto :error_exit
)
echo %GREEN%Test 8 termine avec succes%RESET%
echo.

:: Tous les tests sont terminés avec succès
echo.
echo %GREEN%╔══════════════════════════════════════════════════════════════╗%RESET%
echo %GREEN%║                    SUCCES COMPLET !                         ║%RESET%
echo %GREEN%║                Tous les 8 tests sont termines               ║%RESET%
echo %GREEN%╚══════════════════════════════════════════════════════════════╝%RESET%
echo.
echo %BLUE%Resume des tests executes:%RESET%
echo %YELLOW%• test_h100_g10_p20.json  (hmax=100, g=10, p=20)%RESET%
echo %YELLOW%• test_h120_g10_p20.json  (hmax=120, g=10, p=20)%RESET%
echo %YELLOW%• test_h100_g20_p40.json  (hmax=100, g=20, p=40)%RESET%
echo %YELLOW%• test_h120_g20_p40.json  (hmax=120, g=20, p=40)%RESET%
echo %YELLOW%• test_h100_g15_p60.json  (hmax=100, g=15, p=60)%RESET%
echo %YELLOW%• test_h120_g15_p60.json  (hmax=120, g=15, p=60)%RESET%
echo %YELLOW%• test_h100_g25_p50.json  (hmax=100, g=25, p=50)%RESET%
echo %YELLOW%• test_h120_g25_p50.json  (hmax=120, g=25, p=50)%RESET%
echo.
echo %BLUE%Tous les fichiers sont dans le repertoire: test_validation%RESET%
echo.
goto :success_exit

:error_exit
echo.
echo %RED%╔══════════════════════════════════════════════════════════════╗%RESET%
echo %RED%║                        ERREUR !                              ║%RESET%
echo %RED%║                Un test a echoue. Arret du script.           ║%RESET%
echo %RED%╚══════════════════════════════════════════════════════════════╝%RESET%
echo.
pause
exit /b 1

:success_exit
echo %GREEN%Appuyez sur une touche pour fermer...%RESET%
pause >nul
exit /b 0