"""
Module de recalcul automatique pour les projets AEP

Ce module permet de recalculer automatiquement les résultats
lorsque les données d'entrée changent.
"""

import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import logging
from dataclasses import dataclass
from enum import Enum

from .database import AEPDatabase

class TypeRecalcul(Enum):
    """Types de recalcul"""
    POPULATION = "population"
    HARDY_CROSS = "hardy_cross"
    RESERVOIR = "reservoir"
    POMPING = "pumping"
    DEMAND = "demand"
    NETWORK = "network"

@dataclass
class RecalculTask:
    """Tâche de recalcul"""
    id: str
    type_recalcul: TypeRecalcul
    projet_id: int
    parametres: Dict[str, Any]
    priorite: int = 1
    date_creation: datetime = None
    statut: str = "en_attente"
    
    def __post_init__(self):
        if self.date_creation is None:
            self.date_creation = datetime.now()

class AEPRecalculEngine:
    """Moteur de recalcul automatique"""
    
    def __init__(self, database: AEPDatabase):
        """
        Initialise le moteur de recalcul
        
        Args:
            database: Instance de la base de données AEP
        """
        self.database = database
        self.logger = logging.getLogger(__name__)
        
        # Tâches en attente
        self.taches_en_attente: List[RecalculTask] = []
        
        # Fonctions de calcul
        self.fonctions_calcul = {
            TypeRecalcul.POPULATION: self._calculer_population,
            TypeRecalcul.HARDY_CROSS: self._calculer_hardy_cross,
            TypeRecalcul.RESERVOIR: self._calculer_reservoir,
            TypeRecalcul.POMPING: self._calculer_pumping,
            TypeRecalcul.DEMAND: self._calculer_demand,
            TypeRecalcul.NETWORK: self._calculer_network
        }
        
        # Dépendances entre calculs
        self.dependances = {
            TypeRecalcul.NETWORK: [TypeRecalcul.DEMAND, TypeRecalcul.POPULATION],
            TypeRecalcul.HARDY_CROSS: [TypeRecalcul.NETWORK],
            TypeRecalcul.RESERVOIR: [TypeRecalcul.DEMAND],
            TypeRecalcul.POMPING: [TypeRecalcul.RESERVOIR]
        }
    
    def ajouter_tache_recalcul(self, type_recalcul: TypeRecalcul, projet_id: int, 
                              parametres: Dict[str, Any], priorite: int = 1) -> str:
        """
        Ajoute une tâche de recalcul
        
        Args:
            type_recalcul: Type de recalcul
            projet_id: ID du projet
            parametres: Paramètres du calcul
            priorite: Priorité (1=haute, 5=basse)
            
        Returns:
            ID de la tâche
        """
        task_id = f"{type_recalcul.value}_{projet_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        tache = RecalculTask(
            id=task_id,
            type_recalcul=type_recalcul,
            projet_id=projet_id,
            parametres=parametres,
            priorite=priorite
        )
        
        self.taches_en_attente.append(tache)
        self.logger.info(f"Tâche de recalcul ajoutée: {task_id}")
        
        return task_id
    
    def declencher_recalcul_cascade(self, type_recalcul: TypeRecalcul, projet_id: int, 
                                   parametres: Dict[str, Any]) -> List[str]:
        """
        Déclenche un recalcul en cascade (avec dépendances)
        
        Args:
            type_recalcul: Type de recalcul initial
            projet_id: ID du projet
            parametres: Paramètres du calcul
            
        Returns:
            Liste des IDs de tâches créées
        """
        taches_crees = []
        
        # Ajouter la tâche principale
        task_id = self.ajouter_tache_recalcul(type_recalcul, projet_id, parametres, priorite=1)
        taches_crees.append(task_id)
        
        # Ajouter les tâches dépendantes
        if type_recalcul in self.dependances:
            for dependance in self.dependances[type_recalcul]:
                dep_task_id = self.ajouter_tache_recalcul(dependance, projet_id, parametres, priorite=2)
                taches_crees.append(dep_task_id)
        
        return taches_crees
    
    async def executer_taches_en_attente(self) -> Dict[str, Any]:
        """
        Exécute toutes les tâches en attente
        
        Returns:
            Résultats de l'exécution
        """
        if not self.taches_en_attente:
            return {"taches_executees": 0, "erreurs": 0, "details": []}
        
        # Trier par priorité et date
        self.taches_en_attente.sort(key=lambda x: (x.priorite, x.date_creation))
        
        resultats = {
            "taches_executees": 0,
            "erreurs": 0,
            "details": []
        }
        
        for tache in self.taches_en_attente[:]:  # Copie pour éviter les modifications pendant l'itération
            try:
                self.logger.info(f"Exécution de la tâche: {tache.id}")
                tache.statut = "en_cours"
                
                # Exécuter le calcul
                resultat = await self._executer_calcul(tache)
                
                # Sauvegarder le résultat
                self.database.sauvegarder_resultat_calcul(
                    projet_id=tache.projet_id,
                    type_calcul=tache.type_recalcul.value,
                    nom_calcul=f"recalcul_{tache.id}",
                    parametres_entree=tache.parametres,
                    resultats=resultat,
                    duree_calcul=0.0,  # À améliorer avec un timer
                    version_algorithme="recalcul_automatique"
                )
                
                tache.statut = "terminee"
                resultats["taches_executees"] += 1
                resultats["details"].append({
                    "tache_id": tache.id,
                    "statut": "succes",
                    "message": f"Calcul {tache.type_recalcul.value} exécuté avec succès"
                })
                
                # Retirer la tâche de la liste
                self.taches_en_attente.remove(tache)
                
            except Exception as e:
                tache.statut = "erreur"
                resultats["erreurs"] += 1
                resultats["details"].append({
                    "tache_id": tache.id,
                    "statut": "erreur",
                    "message": f"Erreur lors du calcul {tache.type_recalcul.value}: {str(e)}"
                })
                self.logger.error(f"Erreur lors de l'exécution de {tache.id}: {str(e)}")
        
        return resultats
    
    async def _executer_calcul(self, tache: RecalculTask) -> Dict[str, Any]:
        """
        Exécute un calcul spécifique
        
        Args:
            tache: Tâche à exécuter
            
        Returns:
            Résultat du calcul
        """
        fonction = self.fonctions_calcul.get(tache.type_recalcul)
        if not fonction:
            raise ValueError(f"Fonction de calcul non trouvée pour {tache.type_recalcul}")
        
        # Simuler un calcul asynchrone
        await asyncio.sleep(0.1)
        
        return fonction(tache.parametres)
    
    def _calculer_population(self, parametres: Dict[str, Any]) -> Dict[str, Any]:
        """Calcul de projection de population"""
        population_base = parametres.get("population_base", 1000)
        taux_croissance = parametres.get("taux_croissance", 0.025)
        annees = parametres.get("annees", 10)
        
        resultats = {}
        for annee in range(annees + 1):
            population = population_base * (1 + taux_croissance) ** annee
            resultats[f"annee_{annee}"] = round(population, 2)
        
        return {
            "population_base": population_base,
            "taux_croissance": taux_croissance,
            "projections": resultats
        }
    
    def _calculer_hardy_cross(self, parametres: Dict[str, Any]) -> Dict[str, Any]:
        """Calcul Hardy-Cross"""
        # Simulation d'un calcul Hardy-Cross
        return {
            "debits": {"branche_1": 10.5, "branche_2": 8.3},
            "pertes_charge": {"branche_1": 2.1, "branche_2": 1.8},
            "iterations": 5,
            "convergence": True
        }
    
    def _calculer_reservoir(self, parametres: Dict[str, Any]) -> Dict[str, Any]:
        """Calcul de dimensionnement de réservoir"""
        volume_journalier = parametres.get("volume_journalier", 100)
        coefficient_pointe = parametres.get("coefficient_pointe", 1.5)
        
        volume_reservoir = volume_journalier * coefficient_pointe * 0.3  # 30% de réserve
        
        return {
            "volume_journalier": volume_journalier,
            "coefficient_pointe": coefficient_pointe,
            "volume_reservoir": round(volume_reservoir, 2),
            "hauteur_recommandee": round(volume_reservoir / 10, 2)  # Diamètre de 10m
        }
    
    def _calculer_pumping(self, parametres: Dict[str, Any]) -> Dict[str, Any]:
        """Calcul de pompage"""
        debit = parametres.get("debit", 50)
        hauteur_manometrique = parametres.get("hauteur_manometrique", 30)
        rendement = parametres.get("rendement", 0.7)
        
        puissance_hydraulique = 9.81 * debit * hauteur_manometrique / 3600  # kW
        puissance_moteur = puissance_hydraulique / rendement
        
        return {
            "debit": debit,
            "hauteur_manometrique": hauteur_manometrique,
            "puissance_hydraulique": round(puissance_hydraulique, 2),
            "puissance_moteur": round(puissance_moteur, 2),
            "rendement": rendement
        }
    
    def _calculer_demand(self, parametres: Dict[str, Any]) -> Dict[str, Any]:
        """Calcul des besoins en eau"""
        population = parametres.get("population", 1000)
        dotation = parametres.get("dotation", 60)
        coefficient_pointe = parametres.get("coefficient_pointe", 1.5)
        
        besoin_moyen = population * dotation / 1000  # m³/j
        besoin_pointe = besoin_moyen * coefficient_pointe
        
        return {
            "population": population,
            "dotation": dotation,
            "besoin_moyen": round(besoin_moyen, 2),
            "besoin_pointe": round(besoin_pointe, 2),
            "coefficient_pointe": coefficient_pointe
        }
    
    def _calculer_network(self, parametres: Dict[str, Any]) -> Dict[str, Any]:
        """Calcul de réseau"""
        # Simulation d'un calcul de réseau
        return {
            "longueur_totale": 2500,
            "diametres": {"principal": 200, "secondaire": 150, "tertiaire": 100},
            "debits": {"principal": 50, "secondaire": 25, "tertiaire": 10}
        }
    
    def obtenir_statut_taches(self) -> Dict[str, Any]:
        """
        Obtient le statut des tâches
        
        Returns:
            Statut des tâches
        """
        return {
            "taches_en_attente": len(self.taches_en_attente),
            "taches_par_priorite": {
                1: len([t for t in self.taches_en_attente if t.priorite == 1]),
                2: len([t for t in self.taches_en_attente if t.priorite == 2]),
                3: len([t for t in self.taches_en_attente if t.priorite == 3]),
                4: len([t for t in self.taches_en_attente if t.priorite == 4]),
                5: len([t for t in self.taches_en_attente if t.priorite == 5])
            },
            "taches_par_type": {
                t.value: len([tache for tache in self.taches_en_attente if tache.type_recalcul == t])
                for t in TypeRecalcul
            }
        }
    
    def nettoyer_taches_terminees(self):
        """Nettoie les tâches terminées"""
        self.taches_en_attente = [t for t in self.taches_en_attente if t.statut == "en_attente"]
    
    def generer_rapport_recalcul(self, resultats: Dict[str, Any]) -> str:
        """
        Génère un rapport de recalcul
        
        Args:
            resultats: Résultats de l'exécution
            
        Returns:
            Rapport formaté
        """
        rapport = f"""
# Rapport de Recalcul Automatique

## Résumé
- **Tâches exécutées:** {resultats['taches_executees']}
- **Erreurs:** {resultats['erreurs']}
- **Date d'exécution:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Détails
"""
        
        for detail in resultats["details"]:
            if detail["statut"] == "succes":
                rapport += f"- ✅ {detail['tache_id']}: {detail['message']}\n"
            else:
                rapport += f"- ❌ {detail['tache_id']}: {detail['message']}\n"
        
        return rapport
