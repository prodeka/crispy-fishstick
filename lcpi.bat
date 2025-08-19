@echo off
setlocal
set SCRIPT_DIR=%~dp0
if exist "%SCRIPT_DIR%venv\Scripts\python.exe" (
  set PYEXE="%SCRIPT_DIR%venv\Scripts\python.exe"
) else if exist "%SCRIPT_DIR%venv_new\Scripts\python.exe" (
  set PYEXE="%SCRIPT_DIR%venv_new\Scripts\python.exe"
) else (
  set PYEXE=python
)
%PYEXE% -m lcpi %*
exit /b %errorlevel%

