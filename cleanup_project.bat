@echo off
SETLOCAL

ECHO ###########################################################
ECHO #                                                         #
ECHO #      SCRIPT DE NETTOYAGE FINAL DU PROJET LCPI-CLI       #
ECHO #                                                         #
ECHO #  Ce script va supprimer tous les fichiers et dossiers   #
ECHO #  obsoletes pour ne conserver que le paquet src/lcpi.    #
ECHO #                                                         #
ECHO ###########################################################
ECHO.
ECHO ATTENTION: Cette operation est IRREVERSIBLE.
pause
ECHO.

:: === ETAPE 1: Suppression des Anciens Modules et Codes Sources ===
ECHO [ETAPE 1/4] Suppression des anciens modules et codes sources...

IF EXIST lcpi_platform (
    ECHO  - Suppression de lcpi_platform/...
    rmdir /s /q lcpi_platform
)
IF EXIST BA (
    ECHO  - Suppression de BA/...
    rmdir /s /q BA
)
IF EXIST CM_BOIS (
    ECHO  - Suppression de CM_BOIS/...
    rmdir /s /q CM_BOIS
)
IF EXIST ASSAINISSEMENT (
    ECHO  - Suppression de ASSAINISSEMENT/...
    rmdir /s /q ASSAINISSEMENT
)
IF EXIST web (
    ECHO  - Suppression de web/...
    rmdir /s /q web
)
IF EXIST utils (
    ECHO  - Suppression de utils/...
    rmdir /s /q utils
)
ECHO  -> Termine.
ECHO.

:: === ETAPE 2: Suppression des Fichiers de Notes et de Configuration Obsolètes ===
ECHO [ETAPE 2/4] Suppression des fichiers de notes et de configuration obsoletes...

IF EXIST COPY_PASTE.md del COPY_PASTE.md
IF EXIST PARTAGE.md del PARTAGE.md
IF EXIST "Sans titre.md" del "Sans titre.md"
IF EXIST HYDRODRAIN.md del HYDRODRAIN.md
IF EXIST interface_exemple.py del interface_exemple.py
IF EXIST PROJET_DIMENTIONEMENT.code-workspace del PROJET_DIMENTIONEMENT.code-workspace
IF EXIST climat_test.yml del climat_test.yml
IF EXIST rapport_lcpi.pdf del rapport_lcpi.pdf

ECHO  -> Termine.
ECHO.

:: === ETAPE 3: Nettoyage des Artefacts de Build et des Caches ===
ECHO [ETAPE 3/4] Nettoyage des artefacts de build et des caches...

IF EXIST build ( rmdir /s /q build )
IF EXIST dist ( rmdir /s /q dist )
IF EXIST src\lcpi_cli.egg-info ( rmdir /s /q src\lcpi_cli.egg-info )
IF EXIST .pytest_cache ( rmdir /s /q .pytest_cache )
IF EXIST .ruff_cache ( rmdir /s /q .ruff_cache )
IF EXIST .obsidian ( rmdir /s /q .obsidian )

ECHO  -> Termine.
ECHO.

:: === ETAPE 4: Mise a jour du .gitignore ===
ECHO [ETAPE 4/4] Mise a jour du fichier .gitignore...

(
    echo.
    echo # Caches et artefacts de build
    echo .pytest_cache/
    echo .ruff_cache/
    echo .obsidian/
    echo build/
    echo dist/
    echo *.egg-info/
    echo rapport_lcpi.pdf
    echo climat_test.yml
) >> .gitignore

ECHO  -> Termine.
ECHO.

ECHO ###########################################################
ECHO #                                                         #
ECHO #           NETTOYAGE TERMINE AVEC SUCCES                 #
ECHO #                                                         #
ECHO ###########################################################
ECHO.
ECHO Pour valider que tout fonctionne encore, executez :
ECHO   pip install -e .
ECHO   lcpi --help
ECHO.
ECHO Si tout est OK, n'oubliez pas de commiter ce nettoyage.
ECHO.

pause
EXIT /B 0
