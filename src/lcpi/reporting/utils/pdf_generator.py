"""
Générateur de PDF utilisant WeasyPrint avec gestion d'erreurs robuste.
"""

import logging
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

# Flag pour indiquer si WeasyPrint est disponible
WEASYPRINT_AVAILABLE = False
WEASYPRINT_ERROR = None

# Tentative de chargement de WeasyPrint avec gestion d'erreurs complète
def _try_load_weasyprint():
    """Tente de charger WeasyPrint avec gestion d'erreurs complète."""
    global WEASYPRINT_AVAILABLE, WEASYPRINT_ERROR
    
    try:
        # Vérifier les dépendances système sur Windows
        if sys.platform.startswith('win'):
            # Vérifier si les DLLs GTK sont disponibles
            try:
                import ctypes
                gtk_dlls = [
                    'libgobject-2.0-0.dll',
                    'libcairo-2.dll',
                    'libpango-1.0-0.dll',
                    'libpangoft2-1.0-0.dll',
                    'libpangocairo-1.0-0.dll',
                    'libgdk_pixbuf-2.0-0.dll',
                    'libgdk-3-0.dll',
                    'libgtk-3-0.dll'
                ]
                
                missing_dlls = []
                for dll in gtk_dlls:
                    try:
                        ctypes.CDLL(dll)
                    except OSError:
                        missing_dlls.append(dll)
                
                if missing_dlls:
                    WEASYPRINT_ERROR = f"DLLs GTK manquantes: {', '.join(missing_dlls)}"
                    logger.debug(f"WeasyPrint non disponible: {WEASYPRINT_ERROR}")
                    return False
                    
            except Exception as e:
                logger.debug(f"Impossible de vérifier les DLLs GTK: {e}")
        
        # Tentative d'import de WeasyPrint
        from weasyprint import HTML
        WEASYPRINT_AVAILABLE = True
        WEASYPRINT_ERROR = None
        logger.info("WeasyPrint chargé avec succès")
        return True
        
    except ImportError as e:
        WEASYPRINT_ERROR = f"Module WeasyPrint non installé: {e}"
        logger.debug(f"WeasyPrint non disponible: {WEASYPRINT_ERROR}")
        return False
        
    except OSError as e:
        WEASYPRINT_ERROR = f"Dépendances système manquantes: {e}"
        logger.debug(f"WeasyPrint non disponible: {WEASYPRINT_ERROR}")
        return False
        
    except Exception as e:
        WEASYPRINT_ERROR = f"Erreur inattendue lors du chargement: {e}"
        logger.debug(f"WeasyPrint non disponible: {WEASYPRINT_ERROR}")
        return False

# Charger WeasyPrint au démarrage
_try_load_weasyprint()

def export_to_pdf(html_content: str, output_path: Path, base_url: Path) -> bool:
    """
    Exporte une chaîne de caractères HTML en fichier PDF.

    Args:
        html_content: Le contenu HTML à convertir.
        output_path: Le chemin du fichier PDF de sortie.
        base_url: Le chemin de base pour résoudre les URLs relatives (ex: pour le CSS).
        
    Returns:
        bool: True si l'export a réussi, False sinon
    """
    if not WEASYPRINT_AVAILABLE:
        logger.warning("WeasyPrint non disponible - export PDF impossible")
        
        # Afficher des informations détaillées sur l'erreur
        print("⚠️  Export PDF non disponible")
        if WEASYPRINT_ERROR:
            print(f"🔍 Raison: {WEASYPRINT_ERROR}")
        
        # Suggestions selon le type d'erreur
        if WEASYPRINT_ERROR and "DLLs GTK" in WEASYPRINT_ERROR:
            print("\n💡 Solutions pour Windows:")
            print("   1. Installer GTK+ Runtime Environment:")
            print("      https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer")
            print("   2. Ou utiliser une alternative comme wkhtmltopdf")
            print("   3. Ou générer en HTML et convertir manuellement")
        elif WEASYPRINT_ERROR and "Module WeasyPrint" in WEASYPRINT_ERROR:
            print("\n💡 Solution:")
            print("   pip install weasyprint")
        else:
            print("\n💡 Solutions générales:")
            print("   1. Vérifier les dépendances système")
            print("   2. Redémarrer l'application")
            print("   3. Utiliser une alternative (HTML, DOCX)")
        
        print("\n📋 Alternatives disponibles : HTML, JSON, YAML, CSV, DOCX")
        return False

    try:
        # WeasyPrint a besoin d'une URL de base pour trouver les fichiers liés comme le CSS
        html = HTML(string=html_content, base_url=str(base_url))
        html.write_pdf(output_path)
        print(f"✅ Rapport PDF généré avec succès : {output_path}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la génération du PDF : {e}")
        print(f"❌ Erreur lors de la génération du PDF : {e}")
        
        # Suggestions d'erreurs courantes
        if "Permission denied" in str(e):
            print("💡 Vérifiez les permissions du dossier de sortie")
        elif "No such file or directory" in str(e):
            print("💡 Vérifiez que le dossier de sortie existe")
        elif "cairo" in str(e).lower() or "pango" in str(e).lower():
            print("💡 Problème avec les dépendances graphiques GTK")
            print("   Essayez de redémarrer l'application")
        
        return False

def get_weasyprint_status() -> Dict[str, Any]:
    """
    Retourne le statut détaillé de WeasyPrint.
    
    Returns:
        Dictionnaire avec le statut et les détails
    """
    return {
        "available": WEASYPRINT_AVAILABLE,
        "error": WEASYPRINT_ERROR,
        "platform": sys.platform,
        "python_version": sys.version,
        "suggestions": _get_suggestions()
    }

def _get_suggestions() -> List[str]:
    """Retourne des suggestions selon le type d'erreur."""
    if not WEASYPRINT_ERROR:
        return []
    
    suggestions = []
    
    if "DLLs GTK" in WEASYPRINT_ERROR:
        suggestions.extend([
            "Installer GTK+ Runtime Environment pour Windows",
            "Utiliser wkhtmltopdf comme alternative",
            "Générer en HTML et convertir manuellement"
        ])
    elif "Module WeasyPrint" in WEASYPRINT_ERROR:
        suggestions.append("Installer WeasyPrint: pip install weasyprint")
    elif "dépendances système" in WEASYPRINT_ERROR:
        suggestions.extend([
            "Vérifier les dépendances système",
            "Redémarrer l'application",
            "Utiliser une alternative (HTML, DOCX)"
        ])
    
    return suggestions

def retry_weasyprint_load():
    """
    Tente de recharger WeasyPrint.
    
    Returns:
        True si le rechargement a réussi
    """
    global WEASYPRINT_AVAILABLE, WEASYPRINT_ERROR
    return _try_load_weasyprint()
