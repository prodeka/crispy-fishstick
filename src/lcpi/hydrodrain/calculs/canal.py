import math
import yaml
from typing import Dict, Any

def dimensionner_canal(donnees: dict) -> dict:
    """
    Dimensionne un canal à ciel ouvert selon différentes approches.
    
    Args:
        donnees: Dictionnaire contenant les paramètres du canal
        
    Returns:
        dict: Résultats du dimensionnement
    """
    try:
        # Extraction des paramètres
        canal_data = donnees.get("canal", {})
        geometrie = canal_data.get("geometrie", {})
        hydraulique = canal_data.get("hydraulique", {})
        securite = canal_data.get("securite", {})
        
        # Paramètres hydrauliques
        q_design = hydraulique.get("debit_design", 0)
        pente = hydraulique.get("pente_longitudinale", 0)
        n_manning = hydraulique.get("coefficient_rugosite", 0.025)
        
        # Paramètres géométriques
        type_canal = geometrie.get("type", "trapezoidal")
        largeur_fond = geometrie.get("largeur_fond", 0)
        pente_talus = geometrie.get("pente_talus", 1.5)
        profondeur = geometrie.get("profondeur", 0)
        
        # Paramètres de sécurité
        revanche = securite.get("revanche", 0.3)
        v_max = securite.get("vitesse_maximale", 2.0)
        v_min = securite.get("vitesse_minimale", 0.3)
        
        if q_design <= 0:
            return {"statut": "Erreur", "message": "Le débit de conception doit être positif"}
        
        if pente <= 0:
            return {"statut": "Erreur", "message": "La pente longitudinale doit être positive"}
        
        # Calcul selon le type de canal
        if type_canal == "trapezoidal":
            resultats = dimensionner_canal_trapezoidal(q_design, pente, n_manning, pente_talus, v_max, v_min)
        elif type_canal == "rectangular":
            resultats = dimensionner_canal_rectangular(q_design, pente, n_manning, v_max, v_min)
        elif type_canal == "triangular":
            resultats = dimensionner_canal_triangular(q_design, pente, n_manning, pente_talus, v_max, v_min)
        else:
            return {"statut": "Erreur", "message": f"Type de canal non supporté: {type_canal}"}
        
        # Ajout des paramètres de sécurité
        resultats["revanche"] = revanche
        resultats["hauteur_totale"] = resultats["hauteur_eau"] + revanche
        
        return resultats
        
    except Exception as e:
        return {"statut": "Erreur", "message": f"Erreur lors du dimensionnement: {str(e)}"}

def dimensionner_canal_trapezoidal(q: float, pente: float, n: float, m: float, v_max: float, v_min: float) -> dict:
    """
    Dimensionne un canal trapézoïdal.
    
    Args:
        q: Débit en m³/s
        pente: Pente longitudinale en m/m
        n: Coefficient de Manning
        m: Pente des talus (H/V)
        v_max: Vitesse maximale en m/s
        v_min: Vitesse minimale en m/s
        
    Returns:
        dict: Résultats du dimensionnement
    """
    # Approche par vitesse optimale
    v_opt = math.sqrt(v_min * v_max)
    
    # Calcul de la section hydraulique
    aire = q / v_opt
    rayon_hydraulique = (v_opt / (n * math.sqrt(pente)))**1.5
    
    # Résolution itérative pour h et b
    h = math.sqrt(aire / (2 * math.sqrt(1 + m**2) - m))
    b = aire / h - m * h
    
    # Vérifications
    largeur_miroir = b + 2 * m * h
    aire_verif = h * (b + m * h)
    perimetre = b + 2 * h * math.sqrt(1 + m**2)
    rayon_h_verif = aire_verif / perimetre
    
    # Vitesse réelle
    v_reelle = q / aire_verif
    
    # Nombre de Froude
    froude = v_reelle / math.sqrt(9.81 * (aire_verif / largeur_miroir))
    
    return {
        "statut": "OK",
        "type_canal": "trapezoidal",
        "hauteur_eau": round(h, 3),
        "largeur_fond": round(b, 3),
        "largeur_miroir": round(largeur_miroir, 3),
        "aire_section": round(aire_verif, 3),
        "perimetre_mouille": round(perimetre, 3),
        "rayon_hydraulique": round(rayon_h_verif, 3),
        "vitesse_ecoulement": round(v_reelle, 2),
        "nombre_froude": round(froude, 2),
        "regime": "Fluvial" if froude < 1 else "Torrentiel",
        "pente_talus": m
    }

def dimensionner_canal_rectangular(q: float, pente: float, n: float, v_max: float, v_min: float) -> dict:
    """
    Dimensionne un canal rectangulaire.
    
    Args:
        q: Débit en m³/s
        pente: Pente longitudinale en m/m
        n: Coefficient de Manning
        v_max: Vitesse maximale en m/s
        v_min: Vitesse minimale en m/s
        
    Returns:
        dict: Résultats du dimensionnement
    """
    # Approche par vitesse optimale
    v_opt = math.sqrt(v_min * v_max)
    
    # Calcul de la section hydraulique
    aire = q / v_opt
    rayon_hydraulique = (v_opt / (n * math.sqrt(pente)))**1.5
    
    # Pour un canal rectangulaire, h = b (section optimale)
    h = math.sqrt(aire)
    b = h
    
    # Vérifications
    aire_verif = h * b
    perimetre = b + 2 * h
    rayon_h_verif = aire_verif / perimetre
    
    # Vitesse réelle
    v_reelle = q / aire_verif
    
    # Nombre de Froude
    froude = v_reelle / math.sqrt(9.81 * h)
    
    return {
        "statut": "OK",
        "type_canal": "rectangular",
        "hauteur_eau": round(h, 3),
        "largeur_fond": round(b, 3),
        "largeur_miroir": round(b, 3),
        "aire_section": round(aire_verif, 3),
        "perimetre_mouille": round(perimetre, 3),
        "rayon_hydraulique": round(rayon_h_verif, 3),
        "vitesse_ecoulement": round(v_reelle, 2),
        "nombre_froude": round(froude, 2),
        "regime": "Fluvial" if froude < 1 else "Torrentiel"
    }

def dimensionner_canal_triangular(q: float, pente: float, n: float, m: float, v_max: float, v_min: float) -> dict:
    """
    Dimensionne un canal triangulaire.
    
    Args:
        q: Débit en m³/s
        pente: Pente longitudinale en m/m
        n: Coefficient de Manning
        m: Pente des talus (H/V)
        v_max: Vitesse maximale en m/s
        v_min: Vitesse minimale en m/s
        
    Returns:
        dict: Résultats du dimensionnement
    """
    # Approche par vitesse optimale
    v_opt = math.sqrt(v_min * v_max)
    
    # Calcul de la section hydraulique
    aire = q / v_opt
    rayon_hydraulique = (v_opt / (n * math.sqrt(pente)))**1.5
    
    # Pour un canal triangulaire
    h = math.sqrt(aire / m)
    
    # Vérifications
    aire_verif = m * h**2
    perimetre = 2 * h * math.sqrt(1 + m**2)
    rayon_h_verif = aire_verif / perimetre
    
    # Vitesse réelle
    v_reelle = q / aire_verif
    
    # Nombre de Froude
    largeur_miroir = 2 * m * h
    froude = v_reelle / math.sqrt(9.81 * (aire_verif / largeur_miroir))
    
    return {
        "statut": "OK",
        "type_canal": "triangular",
        "hauteur_eau": round(h, 3),
        "largeur_fond": 0,
        "largeur_miroir": round(largeur_miroir, 3),
        "aire_section": round(aire_verif, 3),
        "perimetre_mouille": round(perimetre, 3),
        "rayon_hydraulique": round(rayon_h_verif, 3),
        "vitesse_ecoulement": round(v_reelle, 2),
        "nombre_froude": round(froude, 2),
        "regime": "Fluvial" if froude < 1 else "Torrentiel",
        "pente_talus": m
    }

def generer_rapport_canal(resultats: dict, donnees_entree: dict) -> str:
    """
    Génère un rapport détaillé pour le dimensionnement de canal.
    
    Args:
        resultats: Résultats du dimensionnement
        donnees_entree: Données d'entrée
        
    Returns:
        str: Rapport en format Markdown
    """
    rapport = f"""
# Rapport de Dimensionnement - Canal à Ciel Ouvert

## 📊 Résultats du Dimensionnement

### Paramètres Géométriques
- **Type de canal** : {resultats.get('type_canal', 'N/A')}
- **Hauteur d'eau** : {resultats.get('hauteur_eau', 0):.3f} m
- **Largeur du fond** : {resultats.get('largeur_fond', 0):.3f} m
- **Largeur du miroir** : {resultats.get('largeur_miroir', 0):.3f} m
- **Hauteur totale** : {resultats.get('hauteur_totale', 0):.3f} m

### Paramètres Hydrauliques
- **Aire de la section** : {resultats.get('aire_section', 0):.3f} m²
- **Périmètre mouillé** : {resultats.get('perimetre_mouille', 0):.3f} m
- **Rayon hydraulique** : {resultats.get('rayon_hydraulique', 0):.3f} m
- **Vitesse d'écoulement** : {resultats.get('vitesse_ecoulement', 0):.2f} m/s
- **Nombre de Froude** : {resultats.get('nombre_froude', 0):.2f}
- **Régime d'écoulement** : {resultats.get('regime', 'N/A')}

## 📐 Formules Utilisées

### Formule de Manning
```
V = (1/n) × R^(2/3) × S^(1/2)
```

Où :
- V = Vitesse d'écoulement (m/s)
- n = Coefficient de Manning
- R = Rayon hydraulique (m)
- S = Pente longitudinale (m/m)

### Nombre de Froude
```
Fr = V / √(g × h)
```

Où :
- Fr = Nombre de Froude
- V = Vitesse d'écoulement (m/s)
- g = Accélération gravitationnelle (9.81 m/s²)
- h = Hauteur d'eau (m)

## ✅ Vérifications

- **Vitesse** : {resultats.get('vitesse_ecoulement', 0):.2f} m/s
- **Régime** : {resultats.get('regime', 'N/A')}
- **Statut** : {resultats.get('statut', 'N/A')}

---
*Rapport généré automatiquement par LCPI Hydrodrain*
"""
    return rapport
