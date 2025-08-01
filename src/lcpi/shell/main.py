# src/lcpi/shell/main.py
import sys
import typer

VERSION = "1.0.0"  # À synchroniser avec la version réelle du projet

WELCOME = f"""
Bienvenue dans l'interpréteur interactif LCPI (v{VERSION})
Tapez 'help' pour la liste des commandes disponibles.
Tapez 'exit' ou Ctrl+C pour quitter.
"""

app = typer.Typer(name="shell", help="Interpréteur de commandes interactif")

@app.command()
def main():
    """Lance le shell interactif."""
    print(WELCOME)
    while True:
        try:
            cmd = input('> ').strip()
            if cmd in ('exit', 'quit'):
                print("Au revoir !")
                break
            elif cmd == 'help':
                print("Commandes disponibles : help, exit, ... (à compléter)")
            elif cmd == 'version':
                print(f"LCPI version {VERSION}")
            elif cmd == '':
                continue
            else:
                print(f"Commande inconnue : {cmd}")
        except (KeyboardInterrupt, EOFError):
            print("Au revoir !")
            break

def register():
    """Enregistre le plugin avec le noyau."""
    return app

if __name__ == '__main__':
    main()
