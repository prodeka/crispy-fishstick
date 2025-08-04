import json
import os

class GestionDonneesTechniques:
    """
    Charge et fournit des méthodes pour interroger les données techniques
    de maintenance (Annexe 3) et de diamètres (Tableau 7.4).
    """
    def __init__(self, fichier_donnees="donnees_techniques_complementaires.json"):
        if not os.path.exists(fichier_donnees):
            raise FileNotFoundError(f"Erreur : Le fichier de données '{fichier_donnees}' est introuvable.")
        with open(fichier_donnees, 'r', encoding='utf-8') as f:
            self.donnees = json.load(f)
        
        self.plan_entretien_ouvrages = self.donnees['annexe_3_entretien']['entretien_ouvrages']
        self.plan_entretien_electro = self.donnees['annexe_3_entretien']['entretien_electromecanique']
        self.catalogue_diametres = self.donnees['tableau_7_4_diametres']['donnees']
        print("✅ Fichier de données techniques (Entretien & Diamètres) chargé.")

    def get_plan_entretien_par_ouvrage(self, nom_ouvrage):
        """
        Recherche toutes les tâches de maintenance pour un ouvrage donné.
        La recherche est insensible à la casse.
        """
        taches = []
        # Recherche dans les deux listes de maintenance
        for tache in self.plan_entretien_ouvrages + self.plan_entretien_electro:
            if nom_ouvrage.lower() in tache['ouvrage'].lower():
                taches.append(tache)
        return taches

    def get_infos_diametre(self, diametre_mm, tolerance=0.1):
        """
        Recherche les informations pour un diamètre intérieur spécifique.
        """
        for item in self.catalogue_diametres:
            if abs(item['diametre_interieur_mm'] - diametre_mm) <= tolerance:
                return item
        return None
    
    def find_diametres_par_materiau(self, materiau_str):
        """
        Trouve tous les diamètres disponibles pour un type de matériau donné.
        """
        resultats = []
        for item in self.catalogue_diametres:
            for nature in item['nature_tuyaux']:
                if materiau_str.lower() in nature.lower():
                    resultats.append(item)
                    break # Pour ne pas ajouter le même diamètre plusieurs fois
        return resultats

# --- Programme Principal d'Exemple ---
if __name__ == "__main__":
    gestionnaire = GestionDonneesTechniques()

    print("\n" + "="*50)
    print("EXEMPLE 1 : RECHERCHE DE PLAN DE MAINTENANCE")
    print("="*50)
    
    ouvrage_recherche = "Pompes"
    taches_pompes = gestionnaire.get_plan_entretien_par_ouvrage(ouvrage_recherche)
    
    if taches_pompes:
        print(f"Tâches de maintenance trouvées pour '{ouvrage_recherche}':")
        for i, tache in enumerate(taches_pompes, 1):
            print(f"\n--- Tâche {i} ---")
            print(f"  Ouvrage complet: {tache['ouvrage']}")
            print(f"  Type d'entretien: {tache['type_entretien']}")
            print(f"  Fréquence: {tache['frequence']}")
            print(f"  Durée: {tache['duree']}")
            print(f"  Effectif: {tache['effectif']}")
            print(f"  Observations: {tache['observations']}")
    else:
        print(f"Aucune tâche trouvée pour '{ouvrage_recherche}'.")
        
    print("\n" + "="*50)
    print("EXEMPLE 2 : RECHERCHE D'INFORMATIONS SUR UN DIAMÈTRE")
    print("="*50)
    
    diametre_recherche = 21.6
    infos_diametre = gestionnaire.get_infos_diametre(diametre_recherche)
    
    if infos_diametre:
        print(f"Informations pour le diamètre intérieur ~{diametre_recherche} mm:")
        print(f"  - Section intérieure : {infos_diametre['section_interieure_mm2']} mm²")
        print(f"  - Nature des tuyaux :")
        for nature in infos_diametre['nature_tuyaux']:
            print(f"    - {nature}")
    else:
        print(f"Aucune information trouvée pour le diamètre {diametre_recherche} mm.")

    print("\n" + "="*50)
    print("EXEMPLE 3 : TROUVER LES DIAMÈTRES POUR UN MATÉRIAU")
    print("="*50)
    
    materiau_recherche = "P.c.v."
    diametres_pvc = gestionnaire.find_diametres_par_materiau(materiau_recherche)
    
    if diametres_pvc:
        print(f"Diamètres disponibles pour le matériau '{materiau_recherche}':")
        for item in diametres_pvc:
            print(f"  - Diamètre: {item['diametre_interieur_mm']} mm (Section: {item['section_interieure_mm2']} mm²)")
    else:
        print(f"Aucun diamètre trouvé pour le matériau '{materiau_recherche}'.")