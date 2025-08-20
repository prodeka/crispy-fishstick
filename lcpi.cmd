@echo off
setlocal

rem Déterminer le répertoire du script pour être indépendant du répertoire courant
set "SCRIPT_DIR=%~dp0"

rem Préparer PYTHONPATH pour trouver le package lcpi dans src
set "PYTHONPATH=%SCRIPT_DIR%src"

rem Ajouter les binaires EPANET (si présents) en tête du PATH
if exist "%SCRIPT_DIR%EPANET_2_3_1_WIN_32_64\64bit" (
  set "PATH=%SCRIPT_DIR%EPANET_2_3_1_WIN_32_64\64bit;%PATH%"
)

rem Sélectionner l'interpréteur Python (venv > venv_new > python global)
if exist "%SCRIPT_DIR%venv\Scripts\python.exe" (
  set "PYEXE=%SCRIPT_DIR%venv\Scripts\python.exe"
) else if exist "%SCRIPT_DIR%venv_new\Scripts\python.exe" (
  set "PYEXE=%SCRIPT_DIR%venv_new\Scripts\python.exe"
) else (
  set "PYEXE=python"
)

"%PYEXE%" -m lcpi %*
exit /b %errorlevel%
