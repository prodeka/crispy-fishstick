@echo off
ECHO #################################################
ECHO #        INSTALLATEUR LCPI-CLI V1.0             #
ECHO #################################################
ECHO.

ECHO Vérification de la connexion Internet...
ping 8.8.8.8 -n 1 -w 1000 >nul 2>nul

IF %errorlevel% == 0 (
    ECHO Connexion Internet détectée. Installation en mode ONLINE.
    GOTO :online_install
) ELSE (
    ECHO Pas de connexion Internet. Tentative d'installation en mode OFFLINE.
    GOTO :offline_install
)

:online_install
ECHO.
ECHO Installation des dépendances depuis PyPI (Internet)...
pip install -r requirements.txt
IF %errorlevel% NEQ 0 (
    ECHO ERREUR: L'installation des dépendances a échoué.
    pause
    EXIT /B 1
)
GOTO :install_project

:offline_install
ECHO.
ECHO Installation des dépendances depuis le dossier local 'offline_packages'...
pip install --no-index --find-links=offline_packages -r requirements.txt
IF %errorlevel% NEQ 0 (
    ECHO ERREUR: L'installation des dépendances hors ligne a échoué.
    pause
    EXIT /B 1
)
GOTO :install_project

:install_project
ECHO.
ECHO Installation de la plateforme LCPI-CLI...
pip install -e .

ECHO.
ECHO #################################################
ECHO #  Installation terminée avec succès !          #
ECHO #  Vous pouvez maintenant utiliser la commande  #
ECHO #  'lcpi' dans votre terminal.                  #
ECHO #################################################
ECHO.
pause
EXIT /B 0