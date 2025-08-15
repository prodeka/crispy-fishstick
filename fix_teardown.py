#!/usr/bin/env python3
"""
Script pour corriger automatiquement tous les teardown_method
"""

import re

def fix_teardown_methods():
    """Corrige tous les teardown_method dans le fichier de test"""
    
    with open('tests/test_aep_suggestions_complete.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour trouver les teardown_method simples
    pattern = r'def teardown_method\(self\):\s*\n\s*"""Nettoie après les tests"""\s*\n\s*if os\.path\.exists\(self\.temp_dir\):\s*\n\s*shutil\.rmtree\(self\.temp_dir\)'
    
    # Remplacement avec la version corrigée
    replacement = '''def teardown_method(self):
        """Nettoie après les tests"""
        try:
            if hasattr(self, 'database'):
                del self.database  # Fermer la connexion
            if hasattr(self, 'validateur'):
                del self.validateur
            if hasattr(self, 'moteur'):
                del self.moteur
            if hasattr(self, 'importateur'):
                del self.importateur
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception:
            pass  # Ignorer les erreurs de nettoyage'''
    
    # Appliquer le remplacement
    new_content = re.sub(pattern, replacement, content)
    
    # Écrire le fichier modifié
    with open('tests/test_aep_suggestions_complete.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Tous les teardown_method ont été corrigés")

if __name__ == "__main__":
    fix_teardown_methods()
