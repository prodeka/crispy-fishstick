#!/usr/bin/env python3
"""
Script pour corriger le support Unicode dans le terminal Windows
"""
import os
import sys
import subprocess
from pathlib import Path

def setup_unicode_support():
    """Configure le support Unicode pour le terminal Windows"""
    print("🔧 Configuration du support Unicode pour Windows...")
    
    # Définir les variables d'environnement pour Unicode
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
    
    # Forcer l'encodage UTF-8 pour stdout/stderr
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    
    print("✅ Support Unicode configuré")

def run_command_with_unicode_fix(cmd):
    """Exécute une commande avec support Unicode"""
    setup_unicode_support()
    
    # Préparer l'environnement
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
    
    print(f"🚀 Exécution: {cmd}")
    
    try:
        # Exécuter avec capture d'erreurs Unicode
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            errors='replace',  # Remplacer les caractères problématiques
            env=env
        )
        
        print("📤 Sortie standard:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Erreurs:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        return False

def test_unicode_commands():
    """Teste les commandes avec support Unicode"""
    print("🧪 TEST DES COMMANDES AVEC SUPPORT UNICODE")
    print("=" * 50)
    
    # Test 1: Commande simple
    print("\n1️⃣ Test commande simple:")
    success = run_command_with_unicode_fix("python -c \"print('Test Unicode: éàçù')\"")
    print(f"✅ Succès: {success}")
    
    # Test 2: Commande LCPI
    print("\n2️⃣ Test commande LCPI:")
    success = run_command_with_unicode_fix("python -m lcpi.aep.cli --help")
    print(f"✅ Succès: {success}")
    
    # Test 3: Commande d'optimisation courte
    print("\n3️⃣ Test optimisation courte:")
    success = run_command_with_unicode_fix(
        'python -m lcpi.aep.cli network-optimize-unified "bismark_inp.inp" '
        '--method genetic --generations 2 --population 5 --demand 500.0 '
        '--no-confirm --no-cache --no-surrogate --verbose --output "temp/test_unicode.json"'
    )
    print(f"✅ Succès: {success}")

def create_unicode_wrapper_script():
    """Crée un script wrapper pour exécuter les commandes avec support Unicode"""
    wrapper_content = '''#!/usr/bin/env python3
"""
Wrapper pour exécuter les commandes LCPI avec support Unicode
Usage: python tools/unicode_wrapper.py "commande"
"""
import os
import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/unicode_wrapper.py \"commande\"")
        sys.exit(1)
    
    # Configuration Unicode
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
    
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    
    # Exécuter la commande
    cmd = sys.argv[1]
    print(f"🚀 Exécution avec support Unicode: {cmd}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            errors='replace',
            env=os.environ
        )
        
        print("📤 Sortie:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Erreurs:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    main()
'''
    
    # Écrire le wrapper
    wrapper_path = Path("tools/unicode_wrapper.py")
    with open(wrapper_path, 'w', encoding='utf-8') as f:
        f.write(wrapper_content)
    
    print(f"✅ Wrapper créé: {wrapper_path}")
    print("Usage: python tools/unicode_wrapper.py \"commande\"")

def main():
    print("🔧 CONFIGURATION DU SUPPORT UNICODE")
    print("=" * 50)
    
    # 1. Configurer l'environnement
    setup_unicode_support()
    
    # 2. Tester les commandes
    test_unicode_commands()
    
    # 3. Créer le wrapper
    create_unicode_wrapper_script()
    
    print("\n" + "=" * 50)
    print("✅ CONFIGURATION TERMINÉE")
    print("=" * 50)
    print("💡 Pour exécuter des commandes avec support Unicode:")
    print("   python tools/unicode_wrapper.py \"votre_commande\"")

if __name__ == "__main__":
    main()