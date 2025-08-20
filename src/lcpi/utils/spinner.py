"""
Module de spinner pour afficher une animation pendant l'exécution des commandes.
"""

import sys
import time
import threading
from typing import Optional, Callable
from contextlib import contextmanager


class Spinner:
    """Classe pour afficher un spinner animé dans le terminal."""
    
    def __init__(self, message: str = "Chargement...", delay: float = 0.1, style: str = "dots"):
        """
        Initialise le spinner.
        
        Args:
            message: Message à afficher avec le spinner
            delay: Délai entre les frames en secondes
            style: Style du spinner ("dots", "line", "arrow", "circle")
        """
        self.message = message
        self.delay = delay
        self.running = False
        self.thread = None
        self.current_frame = 0
        
        # Différents styles de spinner
        self.spinner_styles = {
            "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            "line": ["|", "/", "-", "\\"],
            "arrow": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
            "circle": ["◐", "◓", "◑", "◒"],
            "simple": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            "classic": ["|", "/", "-", "\\"],
            "modern": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        }
        
        self.spinner_chars = self.spinner_styles.get(style, self.spinner_styles["dots"])
    
    def _animate(self):
        """Animation du spinner dans un thread séparé."""
        while self.running:
            frame = self.spinner_chars[self.current_frame]
            sys.stdout.write(f"\r{frame} {self.message}")
            sys.stdout.flush()
            time.sleep(self.delay)
            self.current_frame = (self.current_frame + 1) % len(self.spinner_chars)
    
    def start(self):
        """Démarre l'animation du spinner."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self, final_message: Optional[str] = None):
        """
        Arrête l'animation du spinner.
        
        Args:
            final_message: Message final à afficher (optionnel)
        """
        if not self.running:
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        
        # Effacer la ligne du spinner
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()
        
        # Afficher le message final si fourni
        if final_message:
            print(final_message)


@contextmanager
def spinner(message: str = "Chargement...", final_message: Optional[str] = None, style: str = "line"):
    """
    Contexte manager pour utiliser le spinner facilement.
    
    Args:
        message: Message à afficher pendant l'exécution
        final_message: Message final à afficher (optionnel)
        style: Style du spinner ("dots", "line", "arrow", "circle")
    
    Example:
        with spinner("Optimisation en cours...", style="line"):
            # Code long à exécuter
            time.sleep(5)
    """
    spinner_obj = Spinner(message, style=style)
    try:
        spinner_obj.start()
        yield
    finally:
        spinner_obj.stop(final_message)


class ProgressSpinner:
    """Spinner avec barre de progression."""
    
    def __init__(self, message: str = "Progression...", total: int = 100, style: str = "line"):
        """
        Initialise le spinner de progression.
        
        Args:
            message: Message à afficher
            total: Valeur totale pour 100%
            style: Style du spinner
        """
        self.message = message
        self.total = total
        self.current = 0
        self.running = False
        self.thread = None
        self.current_frame = 0
        
        # Différents styles de spinner
        self.spinner_styles = {
            "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            "line": ["|", "/", "-", "\\"],
            "arrow": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
            "circle": ["◐", "◓", "◑", "◒"],
            "simple": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            "classic": ["|", "/", "-", "\\"],
            "modern": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        }
        
        self.spinner_chars = self.spinner_styles.get(style, self.spinner_styles["line"])
    
    def _animate(self):
        """Animation du spinner avec barre de progression."""
        while self.running:
            frame = self.spinner_chars[self.current_frame]
            percentage = min(100, int((self.current / self.total) * 100))
            bar_length = 20
            filled_length = int(bar_length * percentage // 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            
            sys.stdout.write(f"\r{frame} {self.message} [{bar}] {percentage}%")
            sys.stdout.flush()
            time.sleep(0.1)
            self.current_frame = (self.current_frame + 1) % len(self.spinner_chars)
    
    def start(self):
        """Démarre l'animation."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def update(self, value: int):
        """
        Met à jour la valeur de progression.
        
        Args:
            value: Nouvelle valeur (0 à total)
        """
        self.current = max(0, min(value, self.total))
    
    def stop(self, final_message: Optional[str] = None):
        """
        Arrête l'animation.
        
        Args:
            final_message: Message final à afficher
        """
        if not self.running:
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        
        # Effacer la ligne
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.flush()
        
        if final_message:
            print(final_message)


def show_spinner(message: str = "Chargement...", final_message: Optional[str] = None, style: str = "line"):
    """
    Décorateur pour afficher un spinner pendant l'exécution d'une fonction.
    
    Args:
        message: Message à afficher
        final_message: Message final à afficher
        style: Style du spinner
    
    Returns:
        Décorateur
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            with spinner(message, final_message, style):
                return func(*args, **kwargs)
        return wrapper
    return decorator


# Fonction utilitaire pour tester le spinner
def test_spinner():
    """Teste tous les styles de spinner disponibles."""
    styles = ["dots", "line", "arrow", "circle", "simple", "classic", "modern"]
    
    print("🎯 Test des différents styles de spinner:")
    print("=" * 50)
    
    for style in styles:
        print(f"\nStyle '{style}':")
        with spinner(f"Test du style {style}...", f"✅ Style {style} terminé", style=style):
            time.sleep(2)
    
    print("\n🎉 Test terminé !")


if __name__ == "__main__":
    test_spinner()
