#!/usr/bin/env python3
"""
Script de debug pour identifier le problème Typer et réduire la pollution visuelle
"""

import sys
import os
import typer
from rich.console import Console

# Configuration pour réduire la pollution visuelle
console = Console(quiet=True)

def test_typer_help():
    """Test spécifique du problème d'aide Typer"""
    app = typer.Typer(
        name="test-help",
        help="Test du problème d'aide",
        rich_markup_mode="markdown"
    )
    
    @app.callback()
    def main_callback(verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux")):
        """Callback principal"""
        if verbose:
            console.print("Mode verbeux activé")
    
    @app.command()
    def hello(name: str = typer.Option("World", "--name", "-n", help="Nom à saluer")):
        """Commande de test avec callback"""
        console.print(f"Hello {name}")
    
    return app

def main():
    """Fonction principale de debug"""
    console.print("🔍 Debug du problème Typer - Test d'aide")
    console.print("=" * 50)
    
    # Test spécifique du problème d'aide
    console.print("\n1. Test de l'aide Typer...")
    try:
        app = test_typer_help()
        # Simuler l'appel d'aide
        sys.argv = ["test", "--help"]
        app()
        console.print("✅ Aide Typer fonctionne")
    except Exception as e:
        console.print(f"❌ Erreur aide Typer: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Vérification des versions
    console.print("\n2. Vérification des versions...")
    try:
        import click
        import rich
        console.print(f"Typer: {typer.__version__}")
        console.print(f"Click: {click.__version__}")
        console.print(f"Rich: {rich.__version__}")
    except Exception as e:
        console.print(f"❌ Erreur vérification versions: {e}")
    
    console.print("\n" + "=" * 50)
    console.print("Debug terminé")

if __name__ == "__main__":
    main()
