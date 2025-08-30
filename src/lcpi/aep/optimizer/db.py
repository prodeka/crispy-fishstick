from __future__ import annotations

import sqlite3
import yaml
import logging
import os
import hashlib
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, validator, ValidationError
from pathlib import Path
from datetime import datetime, timezone

# --- Classe de validation à ajouter ---
class PipeData(BaseModel):
    dn_mm: int = Field(gt=0, description="Diamètre Nominal en mm")
    material: str = Field(min_length=1, description="Matériau de la conduite")
    supply_fcfa_per_m: Optional[float] = Field(default=None, ge=0)
    pose_fcfa_per_m: Optional[float] = Field(default=None, ge=0)
    total_fcfa_per_m: float = Field(ge=0)
    source_method: str

    @validator('material')
    def material_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Le matériau ne peut pas être vide')
        return v

# --- Modèle de tarification réaliste (loi de puissance) ---

# Coefficients à stocker dans un fichier de config à terme, mais OK ici pour commencer.
# Le 'scaling_factor' est à ajuster pour que les prix correspondent à votre monnaie (FCFA).
PRICE_MODELS = {
    "PVC": {"scaling_factor": 25, "exponent_b": 1.30},
    "PEHD": {"scaling_factor": 30, "exponent_b": 1.35},
    "Fonte": {"scaling_factor": 150, "exponent_b": 1.20}
}

def _get_realistic_pipe_price(diameter_mm: int, material: str) -> float:
    """Estime le coût unitaire d'une conduite en utilisant un modèle de loi de puissance."""
    model = PRICE_MODELS.get(material, PRICE_MODELS["PEHD"]) # Fallback sur PEHD si matériau inconnu
    
    # Formule : Coût = a * D^b
    # On arrondit au 100 FCFA le plus proche pour un résultat plus propre.
    cost = model["scaling_factor"] * (diameter_mm ** model["exponent_b"])
    return round(cost / 100) * 100


# --- Liste de base des diamètres de fallback ---

# NOUVELLE LISTE DE BASE - Structure harmonisée avec dn_mm
FALLBACK_DIAMETERS_BASE = [
    # --- PVC-U Pression (généralement pour les petits à moyens diamètres) ---
    {"dn_mm": 25, "material": "PVC"},
    {"dn_mm": 32, "material": "PVC"},
    {"dn_mm": 40, "material": "PVC"},
    {"dn_mm": 50, "material": "PVC"},
    {"dn_mm": 63, "material": "PVC"},
    {"dn_mm": 75, "material": "PVC"},
    {"dn_mm": 90, "material": "PVC"},
    {"dn_mm": 110, "material": "PVC"},
    {"dn_mm": 125, "material": "PVC"},
    {"dn_mm": 140, "material": "PVC"},
    {"dn_mm": 160, "material": "PVC"},
    {"dn_mm": 200, "material": "PVC"},
    {"dn_mm": 225, "material": "PVC"},
    {"dn_mm": 250, "material": "PVC"},

    # --- PEHD (Polyéthylène Haute Densité) - Flexible et très courant ---
    # Note : les diamètres PEHD sont souvent "externes", mais on les utilise comme nominaux ici
    {"dn_mm": 63, "material": "PEHD"},
    {"dn_mm": 75, "material": "PEHD"},
    {"dn_mm": 90, "material": "PEHD"},
    {"dn_mm": 110, "material": "PEHD"},
    {"dn_mm": 125, "material": "PEHD"},
    {"dn_mm": 160, "material": "PEHD"},
    {"dn_mm": 180, "material": "PEHD"},
    {"dn_mm": 200, "material": "PEHD"},
    {"dn_mm": 225, "material": "PEHD"},
    {"dn_mm": 250, "material": "PEHD"},
    {"dn_mm": 315, "material": "PEHD"},

    # --- Fonte Ductile (pour les conduites structurantes et grands diamètres) ---
    {"dn_mm": 100, "material": "Fonte"},
    {"dn_mm": 125, "material": "Fonte"},
    {"dn_mm": 150, "material": "Fonte"},
    {"dn_mm": 200, "material": "Fonte"},
    {"dn_mm": 250, "material": "Fonte"},
    {"dn_mm": 300, "material": "Fonte"},
    {"dn_mm": 350, "material": "Fonte"},
    {"dn_mm": 400, "material": "Fonte"},
    {"dn_mm": 450, "material": "Fonte"},
    {"dn_mm": 500, "material": "Fonte"},
    {"dn_mm": 600, "material": "Fonte"},
]


class PriceDB:
    """
    Interface unifiée pour l'accès aux prix des diamètres et accessoires.
    
    Cette classe fournit une API cohérente pour accéder aux données de prix
    avec des mécanismes de fallback robustes.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialise la base de données des prix.
        
        Args:
            db_path: Chemin vers la base de données SQLite ou fichier YAML.
                    Si None, utilise le chemin par défaut.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_path = self._resolve_db_path(db_path)
        self.db_info = {}
        self._conn: Optional[sqlite3.Connection] = None
        
        # Le chargement des données se fait UNE SEULE FOIS ici (cache mémoire)
        self._candidate_diameters: List[PipeData] = self._load_data_with_validation()

    def __del__(self):
        """Destructeur pour fermer proprement la connexion à la base de données."""
        if hasattr(self, '_conn') and self._conn:
            self.logger.info("Fermeture de la connexion à la base de données.")
            self._conn.close()

    def _resolve_db_path(self, path: Optional[str]) -> Optional[str]:
        """Résout le chemin de la DB et le valide."""
        if path:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path
            else:
                self.logger.warning(f"Le chemin personnalisé spécifié n'existe pas : {abs_path}")
                return None
        
        # Logique de recherche du chemin par défaut
        try:
            # Chemin relatif au fichier db.py
            default_path = os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'aep_prices.db')
            abs_path = os.path.abspath(default_path)
            if os.path.exists(abs_path):
                return abs_path
        except Exception:
            pass
        
        self.logger.warning("Aucun chemin de base de données valide n'a pu être trouvé.")
        return None

    def _load_data_with_validation(self) -> List[PipeData]:
        """Orchestre le chargement et la validation des données."""
        raw_data = []
        source_type = "none"
        if self.db_path and self.db_path.endswith(".db"):
            try:
                raw_data = self._load_from_sqlite()
                source_type = "sqlite"
            except Exception as e:
                self.logger.error(f"Échec du chargement depuis SQLite ({self.db_path}): {e}")
        
        if not raw_data:
            self.logger.warning("Base de données non disponible ou vide. Utilisation du fallback.")
            raw_data = self._get_fallback_data()
            source_type = "fallback"

        validated_data = []
        for i, row in enumerate(raw_data):
            try:
                # C'est ici que la validation Pydantic a lieu !
                validated_data.append(PipeData(**row))
            except ValidationError as e:
                self.logger.error(f"Donnée invalide (ligne ~{i+1}) de la source '{source_type}' ignorée. Détails : {e}")

        self._update_db_info(source_type, len(validated_data))
        return validated_data

    def _update_db_info(self, source_type: str, data_count: int) -> None:
        """Met à jour les informations de la base de données."""
        self.db_info.update({
            "path": self.db_path if source_type != 'fallback' else 'N/A',
            "type": source_type,
            "fallback_used": source_type == 'fallback',
            "diameter_count": data_count,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
        # La logique de version est déjà gérée ailleurs, on la laisse
        if 'db_version' not in self.db_info:
            self.db_info['db_version'] = "1.0.0" # Valeur par défaut si non lue

    def _get_fallback_data(self) -> List[Dict]:
        """Génère la liste de fallback avec des prix calculés de manière réaliste et structure canonique."""
        self.logger.warning("Utilisation des diamètres de fallback internes avec modèle de tarification réaliste.")
        
        fallback_data = []
        for item in FALLBACK_DIAMETERS_BASE:
            dn_mm = item["dn_mm"]
            item_material = item["material"]
            
            # Calculer le prix dynamiquement avec le modèle réaliste
            price = _get_realistic_pipe_price(dn_mm, item_material)
            
            # Structure canonique complète
            fallback_data.append({
                "dn_mm": dn_mm,
                "supply_fcfa_per_m": price,
                "pose_fcfa_per_m": 0,  # Coût de pose non inclus dans le modèle de base
                "total_fcfa_per_m": price,
                "material": item_material,
                "source_method": "fallback_realistic_model"
            })
        
        return sorted(fallback_data, key=lambda x: x["dn_mm"])
    
    def get_database_info(self) -> Dict[str, Any]:
        """Renvoie les métadonnées sur la source de données actuellement utilisée."""
        # S'assure que les dernières infos sont à jour
        self.db_info['diameter_count'] = len(self._candidate_diameters)
        self.db_info['fallback_used'] = self.db_info.get('type') == 'fallback'
        return self.db_info

    def get_candidate_diameters(self, material: Optional[str] = None) -> List[Dict]:
        """Renvoie la liste des diamètres candidats sous forme de dictionnaires."""
        if material:
            return [d.model_dump() for d in self._candidate_diameters if d.material.upper() == material.upper()]
        return [d.model_dump() for d in self._candidate_diameters]
    
    def _load_from_sqlite(self) -> List[Dict]:
        """Charge les données depuis SQLite et vérifie la version."""
        if not self.db_path: raise FileNotFoundError("Le chemin de la DB est nul.")

        self._conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True) # Connexion en lecture seule
        self._conn.row_factory = sqlite3.Row
        cursor = self._conn.cursor()
        
        # Vérification de la version
        try:
            cursor.execute("SELECT value FROM metadata WHERE key = 'db_version'")
            version_row = cursor.fetchone()
            self.db_info['db_version'] = version_row[0] if version_row else "N/A"
        except sqlite3.Error:
            self.logger.warning("Table 'metadata' non trouvée ou invalide. Version inconnue.")
            self.db_info['db_version'] = "inconnue"

        cursor.execute("SELECT dn_mm, material, supply_fcfa_per_m, pose_fcfa_per_m, total_fcfa_per_m FROM diameters ORDER BY dn_mm ASC")
        rows = cursor.fetchall()
        return [{**row, "source_method": "sqlite"} for row in rows]
    
    def get_diameter_price(self, dn_mm: int, material: Optional[str] = None) -> Optional[float]:
        """
        Obtient le prix d'un diamètre spécifique.
        
        Args:
            dn_mm: Diamètre nominal en mm
            material: Matériau (optionnel)
            
        Returns:
            Prix total en FCFA/m ou None si non trouvé
        """
        candidates = [d for d in self._candidate_diameters if not material or d.material == material]
        
        for diameter in candidates:
            if diameter.dn_mm == dn_mm:
                return diameter.total_fcfa_per_m
        
        return None
    
    def get_closest_diameter(self, target_d_mm: int, material: Optional[str] = None, prefer_larger: bool = True) -> Optional[Dict]:
        """
        Trouve le diamètre commercial le plus proche d'une valeur cible.
        En cas d'égalité de distance, préfère le plus grand.
        """
        candidates = [d for d in self._candidate_diameters if not material or d.material == material]
        if not candidates: return None
        
        # Logique de tri complexe pour gérer les égalités
        # Trie d'abord par la distance absolue, puis par le diamètre (décroissant si prefer_larger)
        best_match = min(candidates, key=lambda p: (
            abs(p.dn_mm - target_d_mm),
            -p.dn_mm if prefer_larger else p.dn_mm 
        ))
        return best_match.model_dump()

    def reload(self) -> None:
        """
        Force le rechargement des données depuis la source de données configurée.
        Invalide le cache mémoire actuel.
        """
        self.logger.info(f"Rechargement des données demandé depuis '{self.db_path or 'fallback'}'...")
        
        # Ferme l'ancienne connexion si elle existe
        if self._conn:
            self._conn.close()
            self._conn = None
            
        # Relance le processus de chargement et de validation
        self._candidate_diameters = self._load_data_with_validation()
        self.logger.info(f"Rechargement terminé. {self.db_info['diameter_count']} diamètres chargés depuis la source '{self.db_info['type']}'.")

    def get_price_for_length(self, dn_mm: int, length_m: float, material: Optional[str] = None) -> Optional[float]:
        """
        Calcule le coût total pour une conduite d'un diamètre et d'une longueur donnés.
        Renvoie le coût total, ou None si le diamètre n'est pas trouvé.
        """
        if length_m < 0:
            return 0.0

        # On utilise le cache interne pour la performance
        candidates = self._candidate_diameters
        
        # Filtre par matériau si spécifié
        if material:
            candidates = [p for p in candidates if p.material.upper() == material.upper()]

        for pipe in candidates:
            if pipe.dn_mm == dn_mm:
                return pipe.total_fcfa_per_m * length_m
                
        self.logger.warning(f"Diamètre {dn_mm} (matériau: {material or 'any'}) non trouvé. Impossible de calculer le prix.")
        return None

    def dump_candidates_to_csv(self, output_path: str) -> None:
        """
        Exporte la liste complète des diamètres candidats chargés en mémoire vers un fichier CSV.
        """
        import csv
        
        if not self._candidate_diameters:
            self.logger.warning("Aucun diamètre candidat à exporter.")
            return

        try:
            # Pydantic .model_dump() nous donne les dictionnaires
            candidates_dicts = [p.model_dump() for p in self._candidate_diameters]
            keys = candidates_dicts[0].keys()
            
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, 'w', newline='', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(candidates_dicts)
            self.logger.info(f"Liste des {len(candidates_dicts)} diamètres candidats exportée avec succès vers {output_path}")
        except Exception as e:
            self.logger.error(f"Échec de l'exportation CSV vers {output_path}: {e}")
            raise

    def run_sanity_checks(self, min_expected_price: float = 100.0, max_expected_price: float = 1000000.0) -> bool:
        """
        Effectue des vérifications statistiques sur les données chargées pour détecter des anomalies.
        Renvoie True si tout est OK, False en cas d'alerte.
        """
        self.logger.info("Lancement des vérifications de cohérence (sanity checks) sur les données de prix...")
        is_sane = True
        if not self._candidate_diameters:
            self.logger.error("Sanity Check ÉCHOUÉ : Aucune donnée de diamètre n'a été chargée.")
            return False

        # 1. Vérification de la plage de prix
        for pipe in self._candidate_diameters:
            if not (min_expected_price <= pipe.total_fcfa_per_m <= max_expected_price):
                self.logger.warning(
                    f"Sanity Check [ALERTE PRIX] : Le prix pour DN {pipe.dn_mm} ({pipe.material}) "
                    f"est de {pipe.total_fcfa_per_m:,.0f} FCFA/m, ce qui est en dehors de la plage attendue "
                    f"[{min_expected_price:,.0f}, {max_expected_price:,.0f}]."
                )
                is_sane = False

        # 2. Vérification de la monotonicité (le prix doit augmenter avec le diamètre par matériau)
        materials = sorted({p.material for p in self._candidate_diameters})
        for material in materials:
            material_pipes = sorted([p for p in self._candidate_diameters if p.material == material], key=lambda p: p.dn_mm)
            for i in range(len(material_pipes) - 1):
                if material_pipes[i].total_fcfa_per_m > material_pipes[i+1].total_fcfa_per_m:
                    self.logger.warning(
                        f"Sanity Check [ALERTE MONOTONICITÉ] ({material}) : Le prix du DN {material_pipes[i].dn_mm} "
                        f"({material_pipes[i].total_fcfa_per_m:,.0f}) est supérieur à celui du DN {material_pipes[i+1].dn_mm} "
                        f"({material_pipes[i+1].total_fcfa_per_m:,.0f})."
                    )
                    is_sane = False
                    
        if is_sane:
            self.logger.info("Sanity checks passés avec succès.")
        return is_sane


# Les classes DiameterDAO et la fonction get_candidate_diameters ne sont plus nécessaires
# avec le nouveau système centralisé dans la classe PriceDB

