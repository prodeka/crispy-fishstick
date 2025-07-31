import json

def rechercher_recursivement(objet_a_chercher, mot_cle):
    """
    Fonction récursive pour chercher un mot-clé dans un objet Python
    (dictionnaire, liste, chaîne, etc.) de manière insensible à la casse.
    """
    mot_cle = mot_cle.lower()

    if isinstance(objet_a_chercher, dict):
        # Si c'est un dictionnaire, on cherche dans les clés et les valeurs
        for cle, valeur in objet_a_chercher.items():
            if mot_cle in str(cle).lower() or rechercher_recursivement(valeur, mot_cle):
                return True
    
    elif isinstance(objet_a_chercher, list):
        # Si c'est une liste, on cherche dans chaque élément
        for element in objet_a_chercher:
            if rechercher_recursivement(element, mot_cle):
                return True
                
    elif isinstance(objet_a_chercher, str):
        # Si c'est une chaîne, on regarde si le mot-clé est dedans
        if mot_cle in objet_a_chercher.lower():
            return True
            
    return False


def rechercher_tableaux_par_mot_cle(chemin_fichier_json, mot_cle):
    """
    Fonction principale qui charge le fichier JSON et recherche les tableaux
    contenant un mot-clé spécifique dans leur titre ou leur contenu.
    """
    try:
        with open(chemin_fichier_json, 'r', encoding='utf-8') as f:
            content = f.read()
            # Les objets JSON dans le fichier sont séparés par des sauts de ligne.
            # Nous allons les séparer en utilisant un délimiteur unique.
            json_strings = content.replace("}\r\n\r\n{", "}|--|{").split("|--|")
            
            donnees_completes_list = []
            for js in json_strings:
                try:
                    # S'assurer que les objets commencent et finissent bien par des accolades
                    if not js.startswith('{'):
                        js = '{' + js
                    if not js.endswith('}'):
                        js = js + '}'
                    donnees_completes_list.append(json.loads(js))
                except json.JSONDecodeError:
                    # Ignorer les parties qui ne sont pas du JSON valide
                    pass

    except FileNotFoundError:
        print(f"ERREUR : Le fichier '{chemin_fichier_json}' n'a pas été trouvé.")
        return

    resultats_trouves = []
    
    # Itérer à travers chaque objet JSON du fichier
    for donnees_completes in donnees_completes_list:
        # Chaque objet est un dictionnaire où chaque clé est un titre de tableau
        for titre_tableau, contenu_tableau in donnees_completes.items():
            # Chercher le mot-clé dans le titre OU dans le contenu du tableau
            if mot_cle.lower() in titre_tableau.lower() or rechercher_recursivement(contenu_tableau, mot_cle):
                resultats_trouves.append({titre_tableau: contenu_tableau})

    # Affichage des résultats
    if resultats_trouves:
        print(f"\n--- {len(resultats_trouves)} résultat(s) trouvé(s) pour '{mot_cle}' ---")
        for resultat in resultats_trouves:
            print(json.dumps(resultat, indent=2, ensure_ascii=False))
            print("-" * 50)


# --- POINT D'ENTRÉE DU SCRIPT ---
if __name__ == "__main__":
    nom_du_fichier_json = 'donnees_completes.json' 
    
    # Mots-clés pertinents pour la recherche de l'utilisateur
    mots_a_rechercher = ["pointes", "vis", "embrèvement", "assemblage"]
    
    print(f"Lancement de la recherche dans le fichier '{nom_du_fichier_json}'...")
    
    tous_les_resultats = 0
    for mot in mots_a_rechercher:
        rechercher_tableaux_par_mot_cle(nom_du_fichier_json, mot)

    print("\nRecherche terminée.")
