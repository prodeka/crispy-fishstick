@echo off
echo Installation des dependances locales...
echo.

REM Utilise la version de python associee a la commande 'py' ou 'python'
py -m pip install --no-index --find-links=./wheels -r requirements.txt

echo.
echo Installation terminee. Vous pouvez maintenant lancer le programme.
pause