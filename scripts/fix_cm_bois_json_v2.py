#!/usr/bin/env python3
"""
Script pour corriger le fichier JSON CM-Bois - Version 2
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
        
        print(f"📊 Total lignes : {len(lines)}")
        
        # Prendre seulement les lignes jusqu'à la ligne 279 (index 278)
        fixed_lines = lines[:279]
        
        # Chercher la dernière accolade fermante dans les lignes restantes
        for i in range(len(fixed_lines) - 1, -1, -1):
            line = fixed_lines[i].strip()
            if line.endswith('}'):
                # Trouvé la fin du JSON, prendre jusqu'ici
                fixed_lines = fixed_lines[:i+1]
                break
        
        # Écrire le fichier corrigé
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print(f"📊 Lignes corrigées : {len(fixed_lines)}")
        
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