import typer
from src.lcpi.cm.main import app as cm_app

cli = typer.Typer()
cli.add_typer(cm_app, name="cm")

# (Plus tard : cli.add_typer(bois_app, name="bois"))

def main():
    cli()

if __name__ == "__main__":
    main()