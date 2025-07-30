@echo off
ECHO #################################################
ECHO #       DESINSTALLATEUR LCPI-CLI V1.0           #
ECHO #################################################
ECHO.

ECHO Lancement de la desinstallation de la plateforme LCPI-CLI...
ECHO.

:: Dans la nouvelle structure, nous n'avons qu'un seul paquet à désinstaller.
:: Pip gérera la suppression de tous les modules associés.
pip uninstall lcpi-cli -y

ECHO.
ECHO Desinstallation terminee. Verification...
ECHO.

:: Chemin vers le dossier des scripts.
SET "SCRIPTS_PATH=%APPDATA%\Python\Python313\Scripts\lcpi.exe"

:: Vérifie si le fichier lcpi.exe existe encore
IF EXIST "%SCRIPTS_PATH%" (
    ECHO #########################################################
    ECHO #  ECHEC DE LA DESINSTALLATION COMPLETE                 #
    ECHO #-------------------------------------------------------#
    ECHO # Le fichier 'lcpi.exe' est toujours present.           #
    ECHO # Cela peut arriver si plusieurs versions de Python     #
    ECHO # sont installées. Verifiez manuellement le dossier:    #
    ECHO # %APPDATA%\Python\Python313\Scripts\                   #
    ECHO #########################################################
) ELSE (
    ECHO #########################################################
    ECHO #  DESINSTALLATION REUSSIE                              #
    ECHO #-------------------------------------------------------#
    ECHO # La plateforme LCPI-CLI a ete desinstallee.            #
    ECHO #########################################################
)

ECHO.
pause
EXIT /B 0
