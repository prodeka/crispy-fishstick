# src/lcpi/shell/main.py
import typer
import sys

def register(app: typer.Typer):
    """
    Enregistre la commande 'shell' auprès de l'application Typer principale.
    """
    @app.command("shell")
    def shell_logic():
        """
        Lance le shell interactif LCPI-CLI.

        Ce shell permet d'exécuter des commandes LCPI directement sans
        préfixer chaque ligne par 'lcpi'. Tapez 'exit' ou 'quit' pour sortir.
        """
        print("--- Initialisation de LCPI-CLI (depuis le plugin shell) ---")
        # Note: Les plugins sont déjà chargés par le point d'entrée principal.
        print("----------------------------------")
        print("Bienvenue dans le shell interactif LCPI-CLI ! Tapez 'exit' ou 'quit' pour sortir.")
        print("Tapez une commande (ex: 'beton --help') et appuyez sur Entrée.")
        sys.stdout.flush()

        while True:
            try:
                cmd = input('> ').strip()
                if cmd.lower() in ('exit', 'quit'):
                    print('Sortie du shell interactif.')
                    break
                if not cmd:
                    continue

                # Sépare la commande et les arguments
                args = cmd.split()

                # Exécute la commande via l'instance de l'application principale
                # C'est ici que la robustesse est ajoutée.
                app(args, standalone_mode=False)

            except (typer.Exit, SystemExit):
                # Typer/Click lève cette exception pour --help ou en cas d'erreur.
                # On l'intercepte pour ne pas quitter la boucle.
                # L'erreur ou l'aide a déjà été affichée par Typer.
                # On continue simplement à la prochaine invite.
                pass
            except Exception as e:
                # Intercepte toutes les autres erreurs imprévues
                print(f"[ERREUR INATTENDUE] Une erreur est survenue : {e}", file=sys.stderr)
                print("La session interactive continue. Vous pouvez essayer une autre commande.", file=sys.stderr)

        sys.stdout.flush()
