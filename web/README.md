# Nanostruct Web - Plateforme de Calculs d'Ingénierie

## 🏗️ Architecture

Cette application web moderne utilise une architecture **API REST + Frontend** séparée :

### Backend (API Flask)
- **Framework** : Flask avec CORS
- **Structure** : API REST avec endpoints JSON
- **Modules** : Assainissement, Béton Armé, Bois
- **Validation** : Données d'entrée et gestion d'erreurs

### Frontend (Interface Web)
- **Framework** : HTML5 + CSS3 + JavaScript vanilla
- **UI Framework** : Bootstrap 5
- **Icons** : Font Awesome
- **Responsive** : Design mobile-first

## 📁 Structure du Projet

```
web/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── run.py                # Script de démarrage
├── README.md             # Documentation
├── templates/            # Templates HTML
│   ├── base.html        # Template de base
│   └── index.html       # Page d'accueil
└── static/              # Assets statiques
    ├── css/
    │   └── style.css    # Styles personnalisés
    └── js/
        └── app.js       # JavaScript principal
```

## 🚀 Installation et Démarrage

### Option 1 : Script automatique
```bash
cd web
python run.py
```

### Option 2 : Installation manuelle
```bash
cd web
pip install -r requirements.txt
python app.py
```

L'application sera accessible à l'adresse : **http://localhost:5000**

## 🔌 API Endpoints

### Vérification de santé
- `GET /api/health` - Statut de l'API

### Assainissement
- `POST /api/assainissement/calcul` - Calcul de débit
- `POST /api/assainissement/dimensionnement` - Dimensionnement réseau
- `GET /api/assainissement/coefficients` - Coefficients de ruissellement

### Béton Armé
- `POST /api/beton_arme/poteau` - Calcul de poteau
- `POST /api/beton_arme/poutre` - Calcul de poutre
- `GET /api/beton_arme/classes` - Classes de résistance

### Bois
- `POST /api/bois/poteau` - Calcul de poteau bois
- `POST /api/bois/poutre` - Calcul de poutre bois
- `GET /api/bois/classes` - Classes de bois

## 📊 Format des Données

### Exemple de requête Assainissement
```json
{
  "surface": 1000.0,
  "coefficient_ruissellement": 0.9,
  "intensite_pluie": 50.0
}
```

### Exemple de réponse
```json
{
  "success": true,
  "resultat": {
    "debit": 12.5,
    "diametre": 0.3,
    "vitesse": 1.2
  },
  "message": "Calcul d'assainissement effectué avec succès"
}
```

## 🎨 Fonctionnalités Frontend

### Interface Utilisateur
- **Design moderne** avec gradients et animations
- **Responsive** : adapté mobile, tablette, desktop
- **Validation** : formulaires avec feedback visuel
- **Notifications** : alertes en temps réel

### Interactions
- **Calculs en temps réel** via API
- **Spinners** pendant les calculs
- **Gestion d'erreurs** avec messages explicites
- **Navigation fluide** avec scroll smooth

## 🔧 Configuration

### Variables d'environnement
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### Port personnalisé
Modifiez la ligne dans `app.py` :
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🛠️ Développement

### Ajouter un nouveau module
1. Créer l'endpoint dans `app.py`
2. Ajouter le formulaire dans `templates/index.html`
3. Gérer l'événement dans `static/js/app.js`

### Exemple d'endpoint
```python
@app.route('/api/nouveau_module/calcul', methods=['POST'])
def calcul_nouveau_module():
    try:
        data = request.get_json()
        # Logique de calcul
        resultat = nouveau_module_engine.calculer(data)
        return jsonify({
            'success': True,
            'resultat': resultat,
            'message': 'Calcul effectué avec succès'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

## 🔒 Sécurité

- **Validation** : Toutes les données d'entrée sont validées
- **CORS** : Configuré pour le développement
- **Gestion d'erreurs** : Messages d'erreur appropriés
- **Sanitisation** : Protection contre les injections

## 📈 Avantages de cette Architecture

### Séparation des responsabilités
- **Backend** : Logique métier pure
- **Frontend** : Présentation et interactions
- **API** : Interface standardisée

### Évolutivité
- **Multi-interfaces** : Web, mobile, desktop
- **Microservices** : Chaque module peut être indépendant
- **Scalabilité** : API peut être déployée séparément

### Maintenabilité
- **Code modulaire** : Facile à tester et déboguer
- **Documentation** : API auto-documentée
- **Standards** : REST, JSON, HTTP

## 🚀 Déploiement

### Production
```bash
# Installer gunicorn
pip install gunicorn

# Lancer avec gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 📝 Licence

Ce projet fait partie de la plateforme Nanostruct pour les calculs d'ingénierie.

---

**🎯 Objectif** : Créer une plateforme moderne, robuste et évolutive pour les calculs d'ingénierie, en séparant clairement la logique métier de la présentation. 