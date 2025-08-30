
### **Prompt pour Cursor AI / Gemini CLI :**

"Salut. Nous allons maintenant appliquer les **corrections obligatoires** de notre plan d'action sur le projet LCPI.

Ta mission est de modifier le fichier `src/lcpi/aep/optimizer/db.py` pour intégrer toutes les améliorations de robustesse et de cohérence listées ci-dessous.

Ouvre le fichier `src/lcpi/aep/optimizer/db.py` et applique les modifications suivantes :

**1. Unité et Sémantique des Prix (Validation des Données)**

*   Modifie la logique de chargement (depuis SQLite, YAML et le fallback) pour qu'elle normalise les données dans un format interne unifié.
*   Je recommande d'utiliser une classe Pydantic `PipeData` pour valider et structurer chaque entrée. Assure toi d'integrer des messge d'erreur claire une fois que ces contrainte pydantic violé Ajoute ce code au début du fichier :

    ```python
    from pydantic import BaseModel, Field, validator
    from typing import List, Dict, Optional, Any
    import sqlite3
    import yaml
    import logging
    import os
    import hashlib

    class PipeData(BaseModel):
        dn_mm: int = Field(gt=0)
        material: str
        supply_fcfa_per_m: Optional[float] = Field(default=None, ge=0)
        pose_fcfa_per_m: Optional[float] = Field(default=None, ge=0)
        total_fcfa_per_m: float = Field(ge=0)
        source_method: str

        @validator('material')
        def material_must_not_be_empty(cls, v):
            if not v or not v.strip():
                raise ValueError('material must not be empty')
            return v
    ```

**2. Versionnage de la Base de Données**

*   Dans la classe `PriceDB`, ajoute une méthode `_validate_db_schema()` qui vérifie la présence d'une table `metadata` avec une clé `db_version`.
*   Dans la méthode `get_database_info()`, ajoute les clés `db_version` et `schema_version` (elles peuvent être identiques pour l'instant).

**3. Consistance des Noms/Clés**

*   Assure-toi que toutes les données chargées (SQLite, YAML, fallback) sont mappées sur les champs de la classe Pydantic `PipeData`. Utilise `dn_mm` et `total_fcfa_per_m` comme champs canoniques.

**4. Implémentation de `get_closest_diameter`**

*   Ajoute la méthode `get_closest_diameter` à la classe `PriceDB`. Elle doit trouver le diamètre le plus proche dans la liste chargée. En cas d'égalité de distance, elle doit préférer le diamètre supérieur, ce qui est plus sûr pour les calculs hydrauliques.

**5. Cache Mémoire et Gestion de la Connexion**

*   Modifie la classe `PriceDB` pour qu'elle charge les données **une seule fois** lors de l'initialisation et les stocke dans un attribut d'instance (ex: `self._candidate_diameters`).
*   La connexion SQLite doit être ouverte une seule fois dans `__init__` et conservée comme un attribut d'instance pour éviter les ouvertures/fermetures répétées.

**6. Logs & Métriques Clairs**

*   Utilise le module `logging` pour émettre un `logging.WARNING` clair lorsque le fallback est utilisé.
*   Assure-toi que la métrique `fallback_used: bool` est bien présente et correcte dans le retour de `get_database_info()`.

**7. Sécurisation du Chemin d'Entrée**

*   Dans le `__init__` de `PriceDB`, transforme le `db_path` fourni en un chemin absolu et vérifie son existence avant de tenter de le lire.

**Pour t'aider, voici une proposition d'implémentation complète de la classe `PriceDB` que tu peux utiliser pour remplacer l'ancienne version dans le fichier `db.py`. Elle intègre tous les points ci-dessus.**

```python
# --- [DEBUT DU CODE A INSERER DANS db.py] ---

# (Mettre la classe Pydantic PipeData définie au point 1 ici)

class PriceDB:
    """
    Interface unifiée et robuste pour l'accès aux données de prix des diamètres.
    """
    def __init__(self, db_path: Optional[str] = None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_path = self._resolve_db_path(db_path)
        self.db_info = {}
        
        self._conn = None  # Garde la connexion DB ouverte
        self._candidate_diameters: List[PipeData] = self._load_data()
    
    def _resolve_db_path(self, path: Optional[str]) -> Optional[str]:
        # Logique pour trouver le chemin par défaut si path is None
        # ou résoudre le chemin fourni en chemin absolu.
        # Pour l'instant, on suppose que le chemin est correct s'il est fourni.
        if path:
            return os.path.abspath(path)
        # Logique de recherche du chemin par défaut...
        default_path = "src/lcpi/db/aep_prices.db" # A adapter
        return os.path.abspath(default_path) if os.path.exists(default_path) else None

    def _load_data(self) -> List[PipeData]:
        """Orchestre le chargement des données depuis la source la plus pertinente."""
        data = []
        source_type = "none"
        
        if self.db_path and self.db_path.endswith(".db"):
            try:
                data = self._load_from_sqlite()
                source_type = "sqlite"
            except Exception as e:
                self.logger.error(f"Échec du chargement depuis SQLite ({self.db_path}): {e}")
                data = [] # On continue pour tenter le fallback
        
        if not data:
            self.logger.warning("Base de données non disponible ou vide. Utilisation du fallback.")
            data = self._get_fallback_data()
            source_type = "fallback"

        # Validation Pydantic
        validated_data = [PipeData(**row) for row in data]
        
        self._update_db_info(source_type, len(validated_data))
        return validated_data

    def _load_from_sqlite(self) -> List[Dict]:
        if not self.db_path or not os.path.exists(self.db_path):
            raise FileNotFoundError("Chemin de la base de données SQLite non valide.")
        
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        cursor = self._conn.cursor()
        
        # Point 2: Vérification de la version (simplifiée)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metadata';")
        if cursor.fetchone():
            cursor.execute("SELECT key, value FROM metadata WHERE key IN ('db_version', 'schema_version')")
            # Logique pour stocker la version...
        
        cursor.execute("SELECT dn_mm, material, supply_fcfa_per_m, pose_fcfa_per_m, total_fcfa_per_m FROM diameters ORDER BY dn_mm ASC")
        rows = cursor.fetchall()
        
        # Point 3: Consistance des noms
        return [{**row, "source_method": "sqlite"} for row in rows]

    def _get_fallback_data(self) -> List[Dict]:
        # (Copier ici la logique de fallback avec calcul réaliste des prix)
        return [...] # Doit retourner une liste de dictionnaires conformes

    def _update_db_info(self, source_type: str, count: int):
        self.db_info = {
            "path": self.db_path if source_type != 'fallback' else 'N/A',
            "type": source_type,
            "fallback_used": source_type == 'fallback',
            "diameter_count": count,
            "db_version": "1.0.0", # A lire depuis la DB
            "schema_version": "1.0.0" # A lire depuis la DB
        }
        
    def get_database_info(self) -> Dict[str, Any]:
        return self.db_info
        
    def get_candidate_diameters(self, material: Optional[str] = None) -> List[Dict]:
        """Renvoie la liste des diamètres candidats (dictionnaires Pydantic)."""
        if material:
            return [d.dict() for d in self._candidate_diameters if d.material == material]
        return [d.dict() for d in self._candidate_diameters]

    def get_closest_diameter(self, target_d_mm: int, prefer_larger: bool = True) -> Optional[PipeData]:
        """Trouve le diamètre le plus proche dans la liste candidate."""
        if not self._candidate_diameters:
            return None
            
        candidates = self._candidate_diameters
        
        min_diff = float('inf')
        best_match = None
        
        for pipe in candidates:
            diff = abs(pipe.dn_mm - target_d_mm)
            if diff < min_diff:
                min_diff = diff
                best_match = pipe
            elif diff == min_diff:
                if prefer_larger and pipe.dn_mm > best_match.dn_mm:
                    best_match = pipe
                elif not prefer_larger and pipe.dn_mm < best_match.dn_mm:
                    best_match = pipe
                    
        return best_match

    def __del__(self):
        if self._conn:
            self._conn.close()

# --- [FIN DU CODE A INSERER DANS db.py] ---
```

Une fois que tu as appliqué ces modifications, confirme et attends les prochaines instructions."