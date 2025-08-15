"""
Module de validation des données AEP

Ce module permet de détecter les incohérences et erreurs dans les données
des projets AEP : relevés terrain, calculs, paramètres, etc.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

from .database import AEPDatabase

class ValidationError(Exception):
    """Exception levée lors d'une erreur de validation"""
    pass

class ValidationResult:
    """Résultat d'une validation"""
    
    def __init__(self, valide: bool, erreurs: List[str] = None, avertissements: List[str] = None):
        self.valide = valide
        self.erreurs = erreurs or []
        self.avertissements = avertissements or []
    
    def __bool__(self):
        return self.valide
    
    def ajouter_erreur(self, message: str):
        """Ajoute une erreur"""
        self.erreurs.append(message)
        self.valide = False
    
    def ajouter_avertissement(self, message: str):
        """Ajoute un avertissement"""
        self.avertissements.append(message)

class AEPDataValidator:
    """Validateur de données AEP"""
    
    def __init__(self, database: AEPDatabase):
        """
        Initialise le validateur
        
        Args:
            database: Instance de la base de données AEP
        """
        self.database = database
        self.logger = logging.getLogger(__name__)
        
        # Règles de validation
        self.regles_validation = {
            "forage": {
                "profondeur": {"min": 0, "max": 1000, "type": "float"},
                "debit_test": {"min": 0, "max": 1000, "type": "float"},
                "diametre": {"min": 0.1, "max": 10, "type": "float"},
                "niveau_statique": {"min": 0, "max": 500, "type": "float"},
                "niveau_dynamique": {"min": 0, "max": 500, "type": "float"}
            },
            "pompe": {
                "debit_nominal": {"min": 0, "max": 1000, "type": "float"},
                "puissance": {"min": 0, "max": 1000, "type": "float"},
                "hauteur_manometrique": {"min": 0, "max": 500, "type": "float"},
                "rendement": {"min": 0, "max": 1, "type": "float"}
            },
            "reservoir": {
                "volume": {"min": 0, "max": 100000, "type": "float"},
                "hauteur": {"min": 0, "max": 50, "type": "float"},
                "diametre": {"min": 0, "max": 100, "type": "float"}
            },
            "constante": {
                "valeur": {"type": "any"},
                "unite": {"pattern": r"^[a-zA-Z/²³]+$", "type": "string"}
            },
            "enquete": {
                "population": {"min": 0, "max": 1000000, "type": "int"},
                "dotation": {"min": 0, "max": 1000, "type": "float"},
                "coefficient_pointe": {"min": 0, "max": 10, "type": "float"}
            }
        }
    
    def valider_projet_complet(self, projet_id: int) -> ValidationResult:
        """
        Valide un projet complet
        
        Args:
            projet_id: ID du projet
            
        Returns:
            Résultat de validation
        """
        resultat = ValidationResult(True)
        
        # Valider les relevés terrain
        releves = self.database.obtenir_releves_projet(projet_id)
        for releve in releves:
            validation_releve = self.valider_releve_terrain(releve)
            if not validation_releve.valide:
                resultat.erreurs.extend(validation_releve.erreurs)
                resultat.valide = False
            resultat.avertissements.extend(validation_releve.avertissements)
        
        # Valider les résultats de calculs
        resultats = self.database.obtenir_resultats_calculs(projet_id)
        for resultat_calcul in resultats:
            validation_calcul = self.valider_resultat_calcul(resultat_calcul)
            if not validation_calcul.valide:
                resultat.erreurs.extend(validation_calcul.erreurs)
                resultat.valide = False
            resultat.avertissements.extend(validation_calcul.avertissements)
        
        # Valider la cohérence globale
        validation_coherence = self.valider_coherence_projet(projet_id)
        if not validation_coherence.valide:
            resultat.erreurs.extend(validation_coherence.erreurs)
            resultat.valide = False
        resultat.avertissements.extend(validation_coherence.avertissements)
        
        return resultat
    
    def valider_releve_terrain(self, releve: Dict[str, Any]) -> ValidationResult:
        """
        Valide un relevé terrain
        
        Args:
            releve: Données du relevé
            
        Returns:
            Résultat de validation
        """
        resultat = ValidationResult(True)
        
        # Validation de base
        if not releve.get("nom_point"):
            resultat.ajouter_erreur(f"Nom du point manquant pour le relevé {releve.get('id', 'inconnu')}")
        
        if not releve.get("type_releve"):
            resultat.ajouter_erreur(f"Type de relevé manquant pour {releve.get('nom_point', 'inconnu')}")
        
        # Validation des données selon le type
        type_releve = releve.get("type_releve", "").lower()
        donnees = releve.get("donnees", {})
        
        if type_releve in self.regles_validation:
            validation_donnees = self.valider_donnees_selon_type(donnees, type_releve)
            if not validation_donnees.valide:
                resultat.erreurs.extend(validation_donnees.erreurs)
                resultat.valide = False
            resultat.avertissements.extend(validation_donnees.avertissements)
        
        # Validation des coordonnées GPS
        if releve.get("coordonnees_gps"):
            validation_gps = self.valider_coordonnees_gps(releve["coordonnees_gps"])
            if not validation_gps.valide:
                resultat.erreurs.extend(validation_gps.erreurs)
                resultat.valide = False
        
        return resultat
    
    def valider_resultat_calcul(self, resultat: Dict[str, Any]) -> ValidationResult:
        """
        Valide un résultat de calcul
        
        Args:
            resultat: Données du résultat
            
        Returns:
            Résultat de validation
        """
        validation = ValidationResult(True)
        
        # Validation de base
        if not resultat.get("type_calcul"):
            validation.ajouter_erreur(f"Type de calcul manquant pour le résultat {resultat.get('id', 'inconnu')}")
        
        if not resultat.get("nom_calcul"):
            validation.ajouter_erreur(f"Nom de calcul manquant pour le résultat {resultat.get('id', 'inconnu')}")
        
        # Validation des paramètres d'entrée
        parametres = resultat.get("parametres_entree", {})
        if not parametres:
            validation.ajouter_avertissement(f"Pas de paramètres d'entrée pour le calcul {resultat.get('nom_calcul', 'inconnu')}")
        
        # Validation des résultats
        resultats = resultat.get("resultats", {})
        if not resultats:
            validation.ajouter_erreur(f"Pas de résultats pour le calcul {resultat.get('nom_calcul', 'inconnu')}")
        
        # Validation de la durée de calcul
        duree = resultat.get("duree_calcul")
        if duree is not None and duree < 0:
            validation.ajouter_erreur(f"Durée de calcul négative pour {resultat.get('nom_calcul', 'inconnu')}")
        
        return validation
    
    def valider_donnees_selon_type(self, donnees: Dict[str, Any], type_releve: str) -> ValidationResult:
        """
        Valide les données selon le type de relevé
        
        Args:
            donnees: Données à valider
            type_releve: Type de relevé
            
        Returns:
            Résultat de validation
        """
        validation = ValidationResult(True)
        
        if type_releve not in self.regles_validation:
            return validation
        
        regles = self.regles_validation[type_releve]
        
        for champ, regle in regles.items():
            if champ in donnees:
                valeur = donnees[champ]
                
                # Validation du type
                if regle["type"] == "float":
                    try:
                        valeur = float(valeur)
                    except (ValueError, TypeError):
                        validation.ajouter_erreur(f"Valeur '{valeur}' pour '{champ}' n'est pas un nombre")
                        continue
                
                elif regle["type"] == "int":
                    try:
                        valeur = int(valeur)
                    except (ValueError, TypeError):
                        validation.ajouter_erreur(f"Valeur '{valeur}' pour '{champ}' n'est pas un entier")
                        continue
                
                elif regle["type"] == "string":
                    if not isinstance(valeur, str):
                        validation.ajouter_erreur(f"Valeur '{valeur}' pour '{champ}' n'est pas une chaîne")
                        continue
                
                # Validation des bornes
                if "min" in regle and valeur < regle["min"]:
                    validation.ajouter_erreur(f"Valeur '{valeur}' pour '{champ}' est inférieure au minimum {regle['min']}")
                
                if "max" in regle and valeur > regle["max"]:
                    validation.ajouter_erreur(f"Valeur '{valeur}' pour '{champ}' est supérieure au maximum {regle['max']}")
                
                # Validation par pattern
                if "pattern" in regle and isinstance(valeur, str):
                    if not re.match(regle["pattern"], valeur):
                        validation.ajouter_erreur(f"Valeur '{valeur}' pour '{champ}' ne respecte pas le format attendu")
        
        return validation
    
    def valider_coordonnees_gps(self, coordonnees: str) -> ValidationResult:
        """
        Valide les coordonnées GPS
        
        Args:
            coordonnees: Coordonnées GPS
            
        Returns:
            Résultat de validation
        """
        validation = ValidationResult(True)
        
        # Pattern pour coordonnées GPS (format: lat,lon ou lat;lon)
        pattern_gps = r"^-?\d+\.?\d*[,;]\s*-?\d+\.?\d*$"
        
        if not re.match(pattern_gps, coordonnees):
            validation.ajouter_erreur(f"Format de coordonnées GPS invalide: {coordonnees}")
            return validation
        
        # Extraire lat et lon
        try:
            if "," in coordonnees:
                lat, lon = coordonnees.split(",")
            else:
                lat, lon = coordonnees.split(";")
            
            lat = float(lat.strip())
            lon = float(lon.strip())
            
            # Vérifier les plages
            if lat < -90 or lat > 90:
                validation.ajouter_erreur(f"Latitude {lat} hors limites (-90 à 90)")
            
            if lon < -180 or lon > 180:
                validation.ajouter_erreur(f"Longitude {lon} hors limites (-180 à 180)")
                
        except ValueError:
            validation.ajouter_erreur(f"Impossible de parser les coordonnées: {coordonnees}")
        
        return validation
    
    def valider_coherence_projet(self, projet_id: int) -> ValidationResult:
        """
        Valide la cohérence globale d'un projet
        
        Args:
            projet_id: ID du projet
            
        Returns:
            Résultat de validation
        """
        validation = ValidationResult(True)
        
        # Récupérer tous les relevés
        releves = self.database.obtenir_releves_projet(projet_id)
        
        # Vérifier les doublons de noms
        noms_points = {}
        for releve in releves:
            nom = releve.get("nom_point", "")
            if nom in noms_points:
                validation.ajouter_avertissement(f"Point en double: {nom}")
            else:
                noms_points[nom] = releve.get("id")
        
        # Vérifier la cohérence des types de relevés
        types_releves = {}
        for releve in releves:
            type_releve = releve.get("type_releve", "")
            if type_releve not in types_releves:
                types_releves[type_releve] = 0
            types_releves[type_releve] += 1
        
        # Vérifier les types de relevés attendus
        types_attendus = ["forage", "pompe", "reservoir", "enquete"]
        for type_attendu in types_attendus:
            if type_attendu not in types_releves:
                validation.ajouter_avertissement(f"Aucun relevé de type '{type_attendu}' trouvé")
        
        # Vérifier les incohérences de données
        for releve in releves:
            if releve.get("type_releve") == "forage":
                donnees = releve.get("donnees", {})
                profondeur = donnees.get("profondeur")
                niveau_statique = donnees.get("niveau_statique")
                niveau_dynamique = donnees.get("niveau_dynamique")
                
                if profondeur and niveau_statique and niveau_statique > profondeur:
                    validation.ajouter_erreur(f"Niveau statique ({niveau_statique}) supérieur à la profondeur ({profondeur}) pour {releve.get('nom_point')}")
                
                if niveau_statique and niveau_dynamique and niveau_dynamique < niveau_statique:
                    validation.ajouter_erreur(f"Niveau dynamique ({niveau_dynamique}) inférieur au niveau statique ({niveau_statique}) pour {releve.get('nom_point')}")
        
        return validation
    
    def generer_rapport_validation(self, resultat: ValidationResult, projet_id: int) -> str:
        """
        Génère un rapport de validation
        
        Args:
            resultat: Résultat de validation
            projet_id: ID du projet
            
        Returns:
            Rapport formaté
        """
        # Récupérer les informations du projet
        projets = [p for p in self.database.obtenir_projets() if p["id"] == projet_id]
        nom_projet = projets[0]["nom"] if projets else f"Projet {projet_id}"
        
        rapport = f"""
# Rapport de Validation - {nom_projet}

## Résumé
- **Statut:** {'✅ VALIDE' if resultat.valide else '❌ INVALIDE'}
- **Erreurs:** {len(resultat.erreurs)}
- **Avertissements:** {len(resultat.avertissements)}
- **Date de validation:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        if resultat.erreurs:
            rapport += "## Erreurs\n"
            for i, erreur in enumerate(resultat.erreurs, 1):
                rapport += f"{i}. ❌ {erreur}\n"
            rapport += "\n"
        
        if resultat.avertissements:
            rapport += "## Avertissements\n"
            for i, avertissement in enumerate(resultat.avertissements, 1):
                rapport += f"{i}. ⚠️ {avertissement}\n"
            rapport += "\n"
        
        if not resultat.erreurs and not resultat.avertissements:
            rapport += "## ✅ Aucun problème détecté\n\n"
        
        # Statistiques du projet
        stats = self.database.obtenir_statistiques_projet(projet_id)
        rapport += f"""
## Statistiques du Projet
- **Relevés terrain:** {stats['total_releves']}
- **Calculs effectués:** {stats['total_calculs']}
- **Documents:** {stats['total_documents']}

### Répartition par type
"""
        
        for type_releve, count in stats['releves_par_type'].items():
            rapport += f"- **{type_releve}:** {count}\n"
        
        return rapport
    
    def valider_fichier_import(self, chemin_fichier: str, type_import: str) -> ValidationResult:
        """
        Valide un fichier d'import avant traitement
        
        Args:
            chemin_fichier: Chemin vers le fichier
            type_import: Type d'import
            
        Returns:
            Résultat de validation
        """
        validation = ValidationResult(True)
        
        # Vérifier l'existence du fichier
        try:
            with open(chemin_fichier, 'r') as f:
                pass
        except FileNotFoundError:
            validation.ajouter_erreur(f"Fichier non trouvé: {chemin_fichier}")
            return validation
        
        # Vérifier l'extension
        if not chemin_fichier.endswith(('.csv', '.xlsx', '.xls')):
            validation.ajouter_erreur(f"Format de fichier non supporté: {chemin_fichier}")
        
        # Vérifier le type d'import
        if type_import not in ["forages", "pompes", "reservoirs", "constantes", "enquetes", "releves_terrain"]:
            validation.ajouter_erreur(f"Type d'import non supporté: {type_import}")
        
        return validation
    
    def obtenir_recommandations(self, projet_id: int) -> List[str]:
        """
        Obtient des recommandations pour améliorer la qualité des données
        
        Args:
            projet_id: ID du projet
            
        Returns:
            Liste des recommandations
        """
        recommandations = []
        
        # Analyser les relevés
        releves = self.database.obtenir_releves_projet(projet_id)
        
        # Vérifier les coordonnées GPS manquantes
        releves_sans_gps = [r for r in releves if not r.get("coordonnees_gps")]
        if releves_sans_gps:
            recommandations.append(f"Ajouter des coordonnées GPS pour {len(releves_sans_gps)} relevés")
        
        # Vérifier les notes manquantes
        releves_sans_notes = [r for r in releves if not r.get("notes")]
        if releves_sans_notes:
            recommandations.append(f"Ajouter des notes pour {len(releves_sans_notes)} relevés")
        
        # Vérifier les types de relevés manquants
        types_presents = set(r.get("type_releve", "") for r in releves)
        types_attendus = {"forage", "pompe", "reservoir", "enquete"}
        types_manquants = types_attendus - types_presents
        
        if types_manquants:
            recommandations.append(f"Ajouter des relevés pour les types: {', '.join(types_manquants)}")
        
        # Vérifier la cohérence des données
        for releve in releves:
            if releve.get("type_releve") == "forage":
                donnees = releve.get("donnees", {})
                if not donnees.get("debit_test"):
                    recommandations.append(f"Mesurer le débit de test pour le forage {releve.get('nom_point')}")
        
        return recommandations
