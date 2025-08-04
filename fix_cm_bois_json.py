#!/usr/bin/env python3
"""
Script pour corriger le fichier JSON CM-Bois
"""

import json
import os

def fix_cm_bois_json():
    """Corrige le fichier JSON CM-Bois en supprimant le contenu après la ligne 280"""
    
    input_file = "src/lcpi/db/cm_bois.json"
    output_file = "src/lcpi/db/cm_bois_fixed.json"
    
    try:
        # Lire le fichier ligne par ligne
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Prendre seulement les lignes jusqu'à la ligne 280 (index 279)
        fixed_lines = lines[:280]
        
        # S'assurer que le JSON se termine correctement
        # Chercher la dernière accolade fermante
        last_line = fixed_lines[-1].strip()
        if not last_line.endswith('}'):
            # Ajouter l'accolade fermante si nécessaire
            fixed_lines.append('}\n')
        
        # Écrire le fichier corrigé
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        # Vérifier que le JSON est valide
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Fichier corrigé : {output_file}")
        print(f"📊 Nombre d'objets : {len(data)}")
        
        # Remplacer l'ancien fichier
        os.replace(output_file, input_file)
        print(f"✅ Fichier original remplacé : {input_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {e}")
        return False

if __name__ == "__main__":
    success = fix_cm_bois_json()
    if success:
        print("🎉 Correction réussie !")
    else:
        print("❌ Échec de la correction") 