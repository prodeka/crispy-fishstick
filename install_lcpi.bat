@echo off
echo Installation de LCPI-CLI...
echo.
REM Créer le dossier d'installation
mkdir "C:\Program Files\LCPI-CLI" 2>nul
REM Copier l'exécutable
copy "G:\Mon Drive\Other\PROJET_DIMENTIONEMENT_2\dist_20250818_052010\lcpi_cli\lcpi_cli.exe" "C:\Program Files\LCPI-CLI\lcpi_cli.exe"
REM Ajouter au PATH (nécessite des droits admin)
setx PATH "%PATH%;C:\Program Files\LCPI-CLI"
echo.
echo Installation terminee !
echo LCPI-CLI est maintenant accessible depuis n'importe ou.
pause
