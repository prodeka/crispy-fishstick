# Plan d'intégration des commandes métier dans le REPL LCPI

## Objectif
Permettre d'exécuter toutes les vraies commandes métier (cm, bois, etc.) dans le REPL LCPI, avec la même expérience qu'en CLI classique.

---

## 1. Centraliser la logique de parsing
- Utiliser la même logique de parsing (typer/click/argparse) pour la CLI et le REPL.
- Le REPL doit pouvoir parser une ligne de commande comme si elle venait du terminal.

## 2. Appeler dynamiquement la CLI depuis le REPL
- Quand l’utilisateur tape une commande dans le REPL, découper la ligne (`shlex.split`).
- Passer la liste d’arguments à la fonction principale de la CLI (typer/click/argparse) en simulant sys.argv.

## 3. Gestion des erreurs et de l’aide
- Afficher les erreurs et l’aide dans le REPL comme en CLI.
- Intercepter SystemExit pour ne pas quitter le REPL sur une erreur ou un --help.

---

## Exemple d’intégration (pseudo-code Python)

```python
import sys
import shlex

def main():
    print(WELCOME)
    import src.lcpi.cli.main as cli_main  # Import dynamique pour éviter les cycles
    while True:
        try:
            cmd = input('> ').strip()
            if cmd in ('exit', 'quit'):
                print("Au revoir !")
                break
            elif cmd == '':
                continue
            # Découper la commande comme dans un shell
            args = shlex.split(cmd)
            # Appeler la CLI principale avec ces arguments
            try:
                cli_main.main(args=args, standalone_mode=False)
            except SystemExit:
                pass
        except (KeyboardInterrupt, EOFError):
            print("\nAu revoir !")
            break
```

---

## Étapes concrètes à suivre
1. Vérifier le type de CLI utilisé (typer/click/argparse)
2. Adapter le REPL pour parser et transmettre les commandes à la CLI
3. Tester avec des commandes réelles :
   - `cm mat --type "Aciers doux"`
   - `cm poutrelles --type IPE`
   - `bois mat --essence "Chêne"`
4. Gérer les erreurs et l’aide dans le REPL

---

## Avantages
- Aucune duplication de code métier
- Les deux modes (CLI classique et REPL) coexistent
- Facile à maintenir et à enrichir

---

## À faire lors de l’implémentation
- Lire la structure de `src/lcpi/cli/` pour voir comment la CLI principale est organisée
- Adapter le REPL pour exécuter dynamiquement les vraies commandes métier
- Gérer les cas d’erreur et l’aide
- Tester l’intégration sur plusieurs commandes