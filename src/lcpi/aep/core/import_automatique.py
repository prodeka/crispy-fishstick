"""
Module d'import automatique pour les données AEP

Ce module permet d'importer automatiquement des données depuis Excel ou CSV
pour les relevés terrain, résultats de forages, caractéristiques des pompes, etc.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime

from .database import AEPDatabase

class AEPImportAutomatique:
    """Gestionnaire d'import automatique pour les données AEP"""
    
    def __init__(self, database: AEPDatabase):
        """
        Initialise l'importateur automatique
        
        Args:
            database: Instance de la base de données AEP
        """
        self.database = database
        self.logger = logging.getLogger(__name__)
        
        # Définir les types d'import supportés
        self.types_import = {
            "releves_terrain": {
                "description": "Relevés terrain génériques",
                "colonnes_requises": ["type_releve", "nom_point", "donnees"],
                "colonnes_optionnelles": ["coordonnees_gps", "altitude", "operateur", "notes"]
            },
            "forages": {
                "description": "Données de forages",
                "colonnes_requises": ["nom_forage", "profondeur", "debit_test"],
                "colonnes_optionnelles": ["diametre", "niveau_statique", "niveau_dynamique", "qualite_eau", "coordonnees_gps"]
            },
            "pompes": {
                "description": "Caractéristiques des pompes",
                "colonnes_requises": ["nom_pompe", "type_pompe", "debit_nominal"],
                "colonnes_optionnelles": ["puissance", "hauteur_manometrique", "rendement", "fabricant", "modele"]
            },
            "reservoirs": {
                "description": "Données de réservoirs",
                "colonnes_requises": ["nom_reservoir", "volume", "hauteur"],
                "colonnes_optionnelles": ["diametre", "type_reservoir", "materiau", "coordonnees_gps"]
            },
            "constantes": {
                "description": "Constantes et paramètres",
                "colonnes_requises": ["nom_constante", "valeur", "unite"],
                "colonnes_optionnelles": ["type_constante", "source", "description", "validateur"]
            },
            "enquetes": {
                "description": "Données d'enquêtes",
                "colonnes_requises": ["nom_enquete", "date_enquete", "population"],
                "colonnes_optionnelles": ["dotation", "coefficient_pointe", "observations", "enqueteur"]
            }
        }
    
    def obtenir_types_import_supportes(self) -> List[str]:
        """
        Obtient la liste des types d'import supportés
        
        Returns:
            Liste des types d'import
        """
        return list(self.types_import.keys())
    
    def generer_template(self, type_import: str, chemin_sortie: str) -> bool:
        """
        Génère un template Excel pour un type d'import
        
        Args:
            type_import: Type d'import
            chemin_sortie: Chemin de sortie du template
            
        Returns:
            True si le template a été généré avec succès
        """
        if type_import not in self.types_import:
            raise ValueError(f"Type d'import non supporté: {type_import}")
        
        config = self.types_import[type_import]
        
        # Créer un DataFrame avec les colonnes requises et optionnelles
        colonnes = config["colonnes_requises"] + config["colonnes_optionnelles"]
        
        # Créer des données d'exemple
        donnees_exemple = []
        for i in range(3):  # 3 lignes d'exemple
            ligne = {}
            for col in colonnes:
                if col in config["colonnes_requises"]:
                    ligne[col] = f"Exemple_{col}_{i+1}"
                else:
                    ligne[col] = f"Optionnel_{col}_{i+1}"
            donnees_exemple.append(ligne)
        
        df = pd.DataFrame(donnees_exemple)
        
        # Créer le fichier Excel
        with pd.ExcelWriter(chemin_sortie, engine='openpyxl') as writer:
            # Feuille Template
            df.to_excel(writer, sheet_name="Template", index=False)
            
            # Feuille Instructions
            instructions = pd.DataFrame([
                ["Type d'import", type_import],
                ["Description", config["description"]],
                ["", ""],
                ["Colonnes requises", ", ".join(config["colonnes_requises"])],
                ["Colonnes optionnelles", ", ".join(config["colonnes_optionnelles"])],
                ["", ""],
                ["Instructions", "Remplissez les données dans la feuille 'Template'"],
                ["", "Supprimez les lignes d'exemple avant l'import"],
                ["", "Conservez les en-têtes de colonnes"]
            ])
            instructions.to_excel(writer, sheet_name="Instructions", index=False, header=False)
        
        return True
    
    def valider_fichier(self, chemin_fichier: str, type_import: str) -> Dict[str, Any]:
        """
        Valide un fichier d'import
        
        Args:
            chemin_fichier: Chemin vers le fichier
            type_import: Type d'import attendu
            
        Returns:
            Résultat de validation
        """
        if type_import not in self.types_import:
            return {
                "valide": False,
                "erreur": f"Type d'import non supporté: {type_import}"
            }
        
        config = self.types_import[type_import]
        
        try:
            # Lire le fichier
            if chemin_fichier.endswith('.csv'):
                df = pd.read_csv(chemin_fichier)
            elif chemin_fichier.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(chemin_fichier, sheet_name="Template")
            else:
                return {
                    "valide": False,
                    "erreur": "Format de fichier non supporté. Utilisez CSV ou Excel."
                }
            
            # Vérifier les colonnes requises
            colonnes_manquantes = []
            for col in config["colonnes_requises"]:
                if col not in df.columns:
                    colonnes_manquantes.append(col)
            
            if colonnes_manquantes:
                return {
                    "valide": False,
                    "erreur": f"Colonnes requises manquantes: {', '.join(colonnes_manquantes)}"
                }
            
            # Statistiques
            stats = {
                "lignes": len(df),
                "colonnes": len(df.columns),
                "colonnes_requises": len([col for col in df.columns if col in config["colonnes_requises"]]),
                "colonnes_optionnelles": len([col for col in df.columns if col in config["colonnes_optionnelles"]])
            }
            
            return {
                "valide": True,
                "statistiques": stats,
                "colonnes_trouvees": list(df.columns)
            }
            
        except Exception as e:
            return {
                "valide": False,
                "erreur": f"Erreur lors de la lecture du fichier: {str(e)}"
            }
    
    def importer_fichier(self, chemin_fichier: str, type_import: str, projet_id: int) -> Dict[str, Any]:
        """
        Importe un fichier dans la base de données
        
        Args:
            chemin_fichier: Chemin vers le fichier
            type_import: Type d'import
            projet_id: ID du projet
            
        Returns:
            Résultat de l'import
        """
        if type_import not in self.types_import:
            return {
                "importes": 0,
                "erreurs": 1,
                "details": [{"ligne": 0, "type": "erreur", "message": f"Type d'import non supporté: {type_import}"}]
            }
        
        try:
            # Lire le fichier
            if chemin_fichier.endswith('.csv'):
                df = pd.read_csv(chemin_fichier)
            elif chemin_fichier.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(chemin_fichier, sheet_name="Template")
            else:
                return {
                    "importes": 0,
                    "erreurs": 1,
                    "details": [{"ligne": 0, "type": "erreur", "message": "Format de fichier non supporté"}]
                }
            
            # Valider le fichier
            validation = self.valider_fichier(chemin_fichier, type_import)
            if not validation["valide"]:
                return {
                    "importes": 0,
                    "erreurs": 1,
                    "details": [{"ligne": 0, "type": "erreur", "message": validation["erreur"]}]
                }
            
            # Importer selon le type
            if type_import == "forages":
                return self._importer_forages(df, projet_id)
            elif type_import == "pompes":
                return self._importer_pompes(df, projet_id)
            elif type_import == "reservoirs":
                return self._importer_reservoirs(df, projet_id)
            elif type_import == "constantes":
                return self._importer_constantes(df, projet_id)
            elif type_import == "enquetes":
                return self._importer_enquetes(df, projet_id)
            else:
                return self._importer_releves_generiques(df, projet_id, type_import)
                
        except Exception as e:
            return {
                "importes": 0,
                "erreurs": 1,
                "details": [{"ligne": 0, "type": "erreur", "message": f"Erreur lors de l'import: {str(e)}"}]
            }
    
    def _importer_forages(self, df: pd.DataFrame, projet_id: int) -> Dict[str, Any]:
        """Importe des données de forages"""
        importes = 0
        erreurs = 0
        details = []
        
        for index, row in df.iterrows():
            try:
                # Préparer les données
                donnees = {
                    "profondeur": float(row.get("profondeur", 0)),
                    "debit_test": float(row.get("debit_test", 0)),
                    "diametre": float(row.get("diametre", 0)) if pd.notna(row.get("diametre")) else None,
                    "niveau_statique": float(row.get("niveau_statique", 0)) if pd.notna(row.get("niveau_statique")) else None,
                    "niveau_dynamique": float(row.get("niveau_dynamique", 0)) if pd.notna(row.get("niveau_dynamique")) else None,
                    "qualite_eau": str(row.get("qualite_eau", "")) if pd.notna(row.get("qualite_eau")) else None
                }
                
                # Ajouter à la base
                self.database.ajouter_releve_terrain(
                    projet_id=projet_id,
                    type_releve="forage",
                    nom_point=str(row["nom_forage"]),
                    donnees=donnees,
                    coordonnees_gps=str(row.get("coordonnees_gps", "")) if pd.notna(row.get("coordonnees_gps")) else None,
                    operateur="import_automatique",
                    notes=f"Importé automatiquement le {datetime.now().strftime('%Y-%m-%d')}"
                )
                
                importes += 1
                details.append({
                    "ligne": index + 2,  # +2 car index commence à 0 et il y a l'en-tête
                    "type": "succes",
                    "message": f"Forage '{row['nom_forage']}' importé avec succès",
                    "id": importes
                })
                
            except Exception as e:
                erreurs += 1
                details.append({
                    "ligne": index + 2,
                    "type": "erreur",
                    "message": f"Erreur lors de l'import du forage '{row.get('nom_forage', 'inconnu')}': {str(e)}"
                })
        
        return {
            "importes": importes,
            "erreurs": erreurs,
            "details": details
        }
    
    def _importer_pompes(self, df: pd.DataFrame, projet_id: int) -> Dict[str, Any]:
        """Importe des données de pompes"""
        importes = 0
        erreurs = 0
        details = []
        
        for index, row in df.iterrows():
            try:
                # Préparer les données
                donnees = {
                    "type_pompe": str(row["type_pompe"]),
                    "debit_nominal": float(row["debit_nominal"]),
                    "puissance": float(row.get("puissance", 0)) if pd.notna(row.get("puissance")) else None,
                    "hauteur_manometrique": float(row.get("hauteur_manometrique", 0)) if pd.notna(row.get("hauteur_manometrique")) else None,
                    "rendement": float(row.get("rendement", 0)) if pd.notna(row.get("rendement")) else None,
                    "fabricant": str(row.get("fabricant", "")) if pd.notna(row.get("fabricant")) else None,
                    "modele": str(row.get("modele", "")) if pd.notna(row.get("modele")) else None
                }
                
                # Ajouter à la base
                self.database.ajouter_releve_terrain(
                    projet_id=projet_id,
                    type_releve="pompe",
                    nom_point=str(row["nom_pompe"]),
                    donnees=donnees,
                    operateur="import_automatique",
                    notes=f"Importé automatiquement le {datetime.now().strftime('%Y-%m-%d')}"
                )
                
                importes += 1
                details.append({
                    "ligne": index + 2,
                    "type": "succes",
                    "message": f"Pompe '{row['nom_pompe']}' importée avec succès",
                    "id": importes
                })
                
            except Exception as e:
                erreurs += 1
                details.append({
                    "ligne": index + 2,
                    "type": "erreur",
                    "message": f"Erreur lors de l'import de la pompe '{row.get('nom_pompe', 'inconnue')}': {str(e)}"
                })
        
        return {
            "importes": importes,
            "erreurs": erreurs,
            "details": details
        }
    
    def _importer_reservoirs(self, df: pd.DataFrame, projet_id: int) -> Dict[str, Any]:
        """Importe des données de réservoirs"""
        importes = 0
        erreurs = 0
        details = []
        
        for index, row in df.iterrows():
            try:
                # Préparer les données
                donnees = {
                    "volume": float(row["volume"]),
                    "hauteur": float(row["hauteur"]),
                    "diametre": float(row.get("diametre", 0)) if pd.notna(row.get("diametre")) else None,
                    "type_reservoir": str(row.get("type_reservoir", "")) if pd.notna(row.get("type_reservoir")) else None,
                    "materiau": str(row.get("materiau", "")) if pd.notna(row.get("materiau")) else None
                }
                
                # Ajouter à la base
                self.database.ajouter_releve_terrain(
                    projet_id=projet_id,
                    type_releve="reservoir",
                    nom_point=str(row["nom_reservoir"]),
                    donnees=donnees,
                    coordonnees_gps=str(row.get("coordonnees_gps", "")) if pd.notna(row.get("coordonnees_gps")) else None,
                    operateur="import_automatique",
                    notes=f"Importé automatiquement le {datetime.now().strftime('%Y-%m-%d')}"
                )
                
                importes += 1
                details.append({
                    "ligne": index + 2,
                    "type": "succes",
                    "message": f"Réservoir '{row['nom_reservoir']}' importé avec succès",
                    "id": importes
                })
                
            except Exception as e:
                erreurs += 1
                details.append({
                    "ligne": index + 2,
                    "type": "erreur",
                    "message": f"Erreur lors de l'import du réservoir '{row.get('nom_reservoir', 'inconnu')}': {str(e)}"
                })
        
        return {
            "importes": importes,
            "erreurs": erreurs,
            "details": details
        }
    
    def _importer_constantes(self, df: pd.DataFrame, projet_id: int) -> Dict[str, Any]:
        """Importe des constantes"""
        importes = 0
        erreurs = 0
        details = []
        
        for index, row in df.iterrows():
            try:
                # Préparer les données
                donnees = {
                    "valeur": row["valeur"],
                    "unite": str(row["unite"]),
                    "type_constante": str(row.get("type_constante", "")) if pd.notna(row.get("type_constante")) else None,
                    "source": str(row.get("source", "")) if pd.notna(row.get("source")) else None,
                    "description": str(row.get("description", "")) if pd.notna(row.get("description")) else None
                }
                
                # Ajouter à la base
                self.database.ajouter_releve_terrain(
                    projet_id=projet_id,
                    type_releve="constante",
                    nom_point=str(row["nom_constante"]),
                    donnees=donnees,
                    operateur=str(row.get("validateur", "import_automatique")),
                    notes=f"Importé automatiquement le {datetime.now().strftime('%Y-%m-%d')}"
                )
                
                importes += 1
                details.append({
                    "ligne": index + 2,
                    "type": "succes",
                    "message": f"Constante '{row['nom_constante']}' importée avec succès",
                    "id": importes
                })
                
            except Exception as e:
                erreurs += 1
                details.append({
                    "ligne": index + 2,
                    "type": "erreur",
                    "message": f"Erreur lors de l'import de la constante '{row.get('nom_constante', 'inconnue')}': {str(e)}"
                })
        
        return {
            "importes": importes,
            "erreurs": erreurs,
            "details": details
        }
    
    def _importer_enquetes(self, df: pd.DataFrame, projet_id: int) -> Dict[str, Any]:
        """Importe des données d'enquêtes"""
        importes = 0
        erreurs = 0
        details = []
        
        for index, row in df.iterrows():
            try:
                # Préparer les données
                donnees = {
                    "date_enquete": str(row["date_enquete"]),
                    "population": int(row["population"]),
                    "dotation": float(row.get("dotation", 0)) if pd.notna(row.get("dotation")) else None,
                    "coefficient_pointe": float(row.get("coefficient_pointe", 0)) if pd.notna(row.get("coefficient_pointe")) else None,
                    "observations": str(row.get("observations", "")) if pd.notna(row.get("observations")) else None
                }
                
                # Ajouter à la base
                self.database.ajouter_releve_terrain(
                    projet_id=projet_id,
                    type_releve="enquete",
                    nom_point=str(row["nom_enquete"]),
                    donnees=donnees,
                    operateur=str(row.get("enqueteur", "import_automatique")),
                    notes=f"Importé automatiquement le {datetime.now().strftime('%Y-%m-%d')}"
                )
                
                importes += 1
                details.append({
                    "ligne": index + 2,
                    "type": "succes",
                    "message": f"Enquête '{row['nom_enquete']}' importée avec succès",
                    "id": importes
                })
                
            except Exception as e:
                erreurs += 1
                details.append({
                    "ligne": index + 2,
                    "type": "erreur",
                    "message": f"Erreur lors de l'import de l'enquête '{row.get('nom_enquete', 'inconnue')}': {str(e)}"
                })
        
        return {
            "importes": importes,
            "erreurs": erreurs,
            "details": details
        }
    
    def _importer_releves_generiques(self, df: pd.DataFrame, projet_id: int, type_releve: str) -> Dict[str, Any]:
        """Importe des relevés génériques"""
        importes = 0
        erreurs = 0
        details = []
        
        for index, row in df.iterrows():
            try:
                # Convertir la ligne en dictionnaire de données
                donnees = {}
                for col in df.columns:
                    if col not in ["type_releve", "nom_point", "coordonnees_gps", "altitude", "operateur", "notes"]:
                        if pd.notna(row[col]):
                            donnees[col] = row[col]
                
                # Ajouter à la base
                self.database.ajouter_releve_terrain(
                    projet_id=projet_id,
                    type_releve=str(row.get("type_releve", type_releve)),
                    nom_point=str(row["nom_point"]),
                    donnees=donnees,
                    coordonnees_gps=str(row.get("coordonnees_gps", "")) if pd.notna(row.get("coordonnees_gps")) else None,
                    altitude=float(row.get("altitude", 0)) if pd.notna(row.get("altitude")) else None,
                    operateur=str(row.get("operateur", "import_automatique")),
                    notes=str(row.get("notes", f"Importé automatiquement le {datetime.now().strftime('%Y-%m-%d')}"))
                )
                
                importes += 1
                details.append({
                    "ligne": index + 2,
                    "type": "succes",
                    "message": f"Relevé '{row['nom_point']}' importé avec succès",
                    "id": importes
                })
                
            except Exception as e:
                erreurs += 1
                details.append({
                    "ligne": index + 2,
                    "type": "erreur",
                    "message": f"Erreur lors de l'import du relevé '{row.get('nom_point', 'inconnu')}': {str(e)}"
                })
        
        return {
            "importes": importes,
            "erreurs": erreurs,
            "details": details
        }
    
    def generer_rapport_import(self, resultat: Dict[str, Any], type_import: str) -> str:
        """
        Génère un rapport d'import
        
        Args:
            resultat: Résultat de l'import
            type_import: Type d'import
            
        Returns:
            Rapport formaté
        """
        total = resultat["importes"] + resultat["erreurs"]
        taux_succes = (resultat["importes"] / total * 100) if total > 0 else 0
        
        rapport = f"""
# Rapport d'Import - {type_import.upper()}

## Résumé
- **Importés avec succès:** {resultat["importes"]}
- **Erreurs:** {resultat["erreurs"]}
- **Total traité:** {total}
- **Taux de succès:** {taux_succes:.1f}%

## Détails
"""
        
        for detail in resultat["details"]:
            if detail["type"] == "succes":
                rapport += f"- ✅ Ligne {detail['ligne']}: {detail['message']}\n"
            else:
                rapport += f"- ❌ Ligne {detail['ligne']}: {detail['message']}\n"
        
        return rapport
