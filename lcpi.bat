@echo off
REM Script batch pour LCPI-CLI
REM Permet d'utiliser la commande 'lcpi' directement

python -X utf8 "%~dp0scripts\lcpi.py" %* 