# Gemini Project Configuration: PROJET_DIMENTIONEMENT

## prompt
Tu es un assistant expert en développement Python pour le projet "nanostruct".
Ton objectif est de maintenir une haute qualité de code.

## tools

# Outil pour lancer l'application principale
run:
  description: "Lance l'application principale en tant que module Python."
  exec:
    command: "python -m nanostruct.main_app {{args}}"

# Outil de linting et de formatage avec Ruff
lint:
  description: "Exécute ruff pour vérifier la qualité du code et le formater."
  exec:
    command: "ruff check . && ruff format ."

# Outil pour lancer la suite de tests avec Pytest
test:
  description: "Exécute tous les tests du projet avec pytest."
  exec:
    command: "pytest"