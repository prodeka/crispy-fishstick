#!/bin/bash
echo "Installation des dépendances locales..."
echo ""

# Utilise la version de python associee a la commande 'python3'
python3 -m pip install --no-index --find-links=./wheels -r requirements.txt

echo ""
echo "Installation terminée. Vous pouvez maintenant lancer le programme."