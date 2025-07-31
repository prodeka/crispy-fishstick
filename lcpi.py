import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "shell":
        # Lancer le mode interactif REPL
        try:
            from src.lcpi.shell.main import main as shell_main
            shell_main()
        except ImportError as e:
            print("[ERREUR] Impossible de lancer le shell interactif :", e)
            sys.exit(1)
    else:
        # Lancer la CLI classique
        try:
            from src.lcpi.cli import main as cli_main
            cli_main()
        except ImportError as e:
            print("[ERREUR] Impossible de lancer la CLI classique :", e)
            sys.exit(1)