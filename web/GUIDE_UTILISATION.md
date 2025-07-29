# 🚀 Guide d'Utilisation - Nanostruct Web

## Démarrage Rapide

### 1. Installation et Lancement
```bash
cd web
python run.py
```

L'application sera accessible à : **http://localhost:5000**

### 2. Interface Utilisateur

#### 🏠 Page d'Accueil
- **Hero Section** : Présentation de la plateforme
- **Navigation** : Liens vers les modules
- **Design moderne** : Gradients et animations

#### 💧 Module Assainissement
- **Calcul de débit** : Surface, coefficient, intensité de pluie
- **Résultats** : Débit en m³/s et L/s, diamètre approximatif
- **Coefficients** : Toiture, routes, terrains

#### 🏗️ Module Béton Armé
- **Onglets** : Poteau et Poutre
- **Poteau** : Hauteur, section, charge axiale, résistance béton
- **Poutre** : Portée, dimensions, charge uniforme
- **Résultats** : Contraintes, armatures, vérifications

#### 🌳 Module Bois
- **Onglets** : Poteau et Poutre bois
- **Classes** : C18, C24, C30, C35, C40
- **Résultats** : Contraintes, élancement, vérifications

## 🔌 API REST

### Endpoints Principaux

#### Vérification de santé
```bash
GET /api/health
```

#### Assainissement
```bash
POST /api/assainissement/calcul
{
  "surface": 1000.0,
  "coefficient_ruissellement": 0.9,
  "intensite_pluie": 50.0
}
```

#### Béton Armé
```bash
POST /api/beton_arme/poteau
{
  "hauteur": 3.0,
  "section": 0.25,
  "charge_axiale": 500000,
  "resistance_beton": 25
}
```

#### Bois
```bash
POST /api/bois/poteau
{
  "hauteur": 3.0,
  "section": 0.04,
  "charge_axiale": 50000,
  "classe_bois": "C24"
}
```

## 🧪 Tests

### Test Automatique
```bash
python test_api.py
```

### Test Manuel avec curl
```bash
# Test de santé
curl http://localhost:5000/api/health

# Test assainissement
curl -X POST http://localhost:5000/api/assainissement/calcul \
  -H "Content-Type: application/json" \
  -d '{"surface": 1000, "coefficient_ruissellement": 0.9, "intensite_pluie": 50}'
```

## 🎨 Fonctionnalités Frontend

### Interface Responsive
- **Mobile** : Design adaptatif
- **Tablette** : Navigation optimisée
- **Desktop** : Interface complète

### Interactions
- **Validation** : Formulaires avec feedback
- **Calculs temps réel** : Via API REST
- **Notifications** : Alertes en temps réel
- **Spinners** : Indicateurs de chargement

### Design
- **Bootstrap 5** : Framework CSS moderne
- **Font Awesome** : Icônes professionnelles
- **Gradients** : Design contemporain
- **Animations** : Transitions fluides

## 🔧 Configuration

### Variables d'Environnement
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### Port Personnalisé
Modifiez dans `app.py` :
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📊 Exemples d'Utilisation

### Calcul Assainissement
1. Remplir le formulaire
2. Cliquer sur "Calculer"
3. Voir les résultats en temps réel

### Calcul Béton Armé
1. Choisir l'onglet (Poteau/Poutre)
2. Saisir les données
3. Obtenir contraintes et armatures

### Calcul Bois
1. Sélectionner la classe de bois
2. Entrer les dimensions
3. Vérifier la résistance

## 🚨 Dépannage

### Erreur de Connexion
- Vérifier que l'API est démarrée
- Contrôler le port 5000
- Vérifier les logs Flask

### Erreur de Calcul
- Vérifier les données d'entrée
- Contrôler les unités
- Consulter les messages d'erreur

### Problème d'Interface
- Vider le cache navigateur
- Vérifier JavaScript
- Contrôler la console

## 📈 Avantages de cette Architecture

### Séparation des Responsabilités
- **Backend** : Logique métier pure
- **Frontend** : Interface utilisateur
- **API** : Interface standardisée

### Évolutivité
- **Multi-interfaces** : Web, mobile, desktop
- **Microservices** : Modules indépendants
- **Scalabilité** : API déployable séparément

### Maintenabilité
- **Code modulaire** : Facile à tester
- **Standards REST** : API documentée
- **Technologies modernes** : Bootstrap, ES6, CSS3

---

**🎯 Objectif** : Plateforme moderne, robuste et évolutive pour les calculs d'ingénierie. 