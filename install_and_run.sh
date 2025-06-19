#!/bin/bash

VENV_DIR="venv"
PACKAGES_DIR="vendor/packages"

echo "--- Script de lancement et d'installation 100% OFFLINE pour Linux/macOS ---"

if ! command -v python3 &> /dev/null
then
    echo "ERREUR: Python 3 n'est pas installe."
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv $VENV_DIR
fi

source "$VENV_DIR/bin/activate"

pip install --no-index --find-links="$PACKAGES_DIR" -r requirements.txt >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERREUR: L'installation des dépendances locales a échoué."
    deactivate
    exit 1
fi

echo "Dépendances installées avec succès."
echo "Lancement du programme principal..."

# LA LIGNE CORRIGÉE : "$@" transmet tous les arguments (comme -v) au script Python
python3 main.py "$@"

echo "Programme terminé."
deactivate