# 🔐 Guide d'Utilisation du Système de Licence LCPI-CLI

## 📋 **VUE D'ENSEMBLE**

Le système de licence LCPI-CLI est un mécanisme de protection propriétaire robuste qui :
- **Protège** votre logiciel contre l'utilisation non autorisée
- **Contrôle** l'accès aux fonctionnalités selon le type de licence
- **Surveille** l'expiration des licences automatiquement
- **Lie** les licences à des machines spécifiques via empreinte matérielle

---

## 🏷️ **TYPES DE LICENCES DISPONIBLES**

| Type | Fonctionnalités | Usage | Durée |
|------|----------------|-------|-------|
| **Standard** | Fonctionnalités de base + plugins essentiels | Utilisateurs individuels, étudiants | 1 an |
| **Premium** | Toutes les fonctionnalités + support avancé | Professionnels, consultants | 2 ans |
| **Enterprise** | Fonctionnalités complètes + support prioritaire | Entreprises, institutions | 3 ans |

---

## 🔑 **GÉNÉRATION DE LICENCES**

### **Pour les Développeurs/Administrateurs**

#### **Étape 1 : Utiliser le Générateur de Licence**
```bash
cd tools/
python generate_license_improved.py "NomUtilisateur" "standard" 365
```

**Paramètres :**
- `NomUtilisateur` : Nom de l'utilisateur final
- `standard` : Type de licence (standard, premium, enterprise)
- `365` : Durée de validité en jours

#### **Étape 2 : Générer une Licence pour une Machine Spécifique**
```bash
# Obtenir l'empreinte de la machine cible
python -c "import uuid; print(f'Empreinte: {hex(uuid.getnode())}')"

# Générer la licence avec l'empreinte spécifique
python generate_license_improved.py "NomUtilisateur" "standard" 365 --machine-fingerprint 0x123456789abc
```

---

## 👤 **ACTIVATION DE LICENCE POUR L'UTILISATEUR**

### **Étape 1 : Créer le Dossier de Licence**
```bash
# Windows
mkdir %USERPROFILE%\.lcpi

# Linux/macOS
mkdir ~/.lcpi
```

### **Étape 2 : Installer la Licence**
```bash
# Copier le fichier de licence généré
copy "licence_admin_standard.key" "%USERPROFILE%\.lcpi\license.key"
```

### **Étape 3 : Vérifier l'Activation**
```bash
lcpi --help
```

---

## 🔍 **VÉRIFICATION ET DIAGNOSTIC**

### **Vérifier le Statut de la Licence**
```bash
python -c "
import sys
sys.path.insert(0, 'src')
from lcpi.license_validator import validate_license, get_license_info

is_valid, message = validate_license()
print(f'Licence valide: {is_valid}')
print(f'Message: {message}')
"
```

---

## 🛠️ **GESTION AVANCÉE DES LICENCES**

### **Renouveler une Licence**
```bash
# 1. Sauvegarder l'ancienne licence
copy "%USERPROFILE%\.lcpi\license.key" "%USERPROFILE%\.lcpi\license_backup.key"

# 2. Générer une nouvelle licence
python tools/generate_license_improved.py "admin" "premium" 730

# 3. Installer la nouvelle licence
copy "licence_admin_premium.key" "%USERPROFILE%\.lcpi\license.key"
```

---

## 🔒 **SÉCURITÉ ET PROTECTION**

### **Caractéristiques de Sécurité**
- **Empreinte matérielle** : Chaque licence est liée à l'adresse MAC de la machine
- **Chiffrement robuste** : Utilisation de Fernet avec PBKDF2
- **Validation automatique** : Vérification au démarrage de l'application

---

## 📞 **SUPPORT ET DÉPANNAGE**

### **En Cas de Problème**
1. **Vérifier** le statut de la licence avec `lcpi --help`
2. **Consulter** les logs d'erreur
3. **Tester** l'import direct de LCPI
4. **Vérifier** l'empreinte de la machine

### **Informations de Contact**
- **Email** : support@lcpi-cli.com
- **Téléphone** : +33 1 23 45 67 89

---

*Dernière mise à jour : Août 2025*
*Version du guide : 2.0.0*
