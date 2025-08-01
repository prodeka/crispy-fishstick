@echo off
echo Installation des dependances locales...
echo.

REM Naviguer vers le repertoire du script, puis vers la racine du projet
pushd "%~dp0"
cd ..

REM Utilise la version de python associee a la commande 'py' ou 'python'
py -m pip install --no-index --find-links=./wheels -r requirements.txt

echo.
echo Installation terminee. Vous pouvez maintenant lancer le programme.
pause
popd