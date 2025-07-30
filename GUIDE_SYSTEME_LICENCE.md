# 🛡️ Guide du Système de Licence LCPI-CLI

## 📋 **VUE D'ENSEMBLE**

Le système de licence LCPI-CLI est un mécanisme de protection propriétaire robuste qui :
- **Protège** votre logiciel contre l'utilisation non autorisée
- **Contrôle** l'accès aux fonctionnalités selon le type de licence
- **Surveille** l'expiration des licences automatiquement
- **Lie** les licences à des machines spécifiques

---

## 🔐 **POUR LE DÉVELOPPEUR**

### **Installation des Dépendances**

```bash
pip install cryptography
```

### **Génération de Licences**

#### **Étape 1 : Préparation**
1. Envoyez le script `generate_license.py` à votre utilisateur
2. L'utilisateur doit l'exécuter sur **sa propre machine** (important pour l'empreinte matérielle)

#### **Étape 2 : Génération**
```bash
python generate_license.py
```

Le script demandera :
- **Nom de l'utilisateur** : Pour identifier le titulaire de la licence
- **Durée de validité** : Nombre de jours (ex: 365 pour 1 an)
- **Type de licence** : Standard, Premium, ou Enterprise

#### **Étape 3 : Résultat**
Le script génère :
- **Clé de licence chiffrée** : À envoyer à l'utilisateur
- **Fichier de sauvegarde** : Pour vos archives
- **Instructions d'activation** : Pour l'utilisateur

### **Types de Licences**

| Type | Fonctionnalités | Usage |
|------|----------------|-------|
| **Standard** | Fonctionnalités de base | Utilisateurs individuels |
| **Premium** | Fonctionnalités avancées | Professionnels |
| **Enterprise** | Toutes les fonctionnalités | Entreprises |

---

## 👤 **POUR L'UTILISATEUR**

### **Activation de Licence**

#### **Étape 1 : Création du Dossier**
Créez un dossier caché `.lcpi` dans votre répertoire personnel :

**Windows :**
```cmd
mkdir C:\Users\VotreNom\.lcpi
```

**Linux/macOS :**
```bash
mkdir ~/.lcpi
```

#### **Étape 2 : Création du Fichier de Licence**
Dans le dossier `.lcpi`, créez un fichier `license.key` :

**Windows :**
```cmd
notepad C:\Users\VotreNom\.lcpi\license.key
```

**Linux/macOS :**
```bash
nano ~/.lcpi/license.key
```

#### **Étape 3 : Activation**
1. Collez votre clé de licence dans le fichier
2. Sauvegardez le fichier
3. Relancez LCPI-CLI

### **Vérification de l'Activation**

LCPI-CLI vérifie automatiquement la licence au démarrage :
- ✅ **Licence valide** : Le programme démarre normalement
- ❌ **Licence invalide** : Message d'erreur et arrêt du programme

---

## 🔍 **FONCTIONNALITÉS DE SÉCURITÉ**

### **Protection par Empreinte Matérielle**
- Chaque licence est liée à l'adresse MAC de la machine
- Impossible d'utiliser une licence sur une autre machine
- Détection automatique des tentatives de transfert

### **Chiffrement Robuste**
- Utilisation de la bibliothèque `cryptography`
- Chiffrement Fernet avec clé dérivée par PBKDF2
- Protection contre la modification des clés

### **Vérification d'Expiration**
- Contrôle automatique de la date d'expiration
- Messages d'alerte avant expiration
- Arrêt automatique après expiration

### **Validation Intégrée**
- Vérification au démarrage de l'application
- Messages d'erreur clairs et informatifs
- Instructions d'activation automatiques

---

## 🧪 **TESTS ET VÉRIFICATION**

### **Test du Système Complet**

```bash
python test_license_system.py
```

Ce script teste :
- ✅ Génération de licences
- ✅ Validation de licences
- ✅ Activation de licences
- ✅ Vérification d'expiration

### **Test Manuel**

#### **Génération de Test**
```bash
python generate_license.py
```

#### **Validation de Test**
```python
from src.lcpi.license_validator import validate_license
is_valid, message = validate_license()
print(f"Valid: {is_valid}")
print(f"Message: {message}")
```

---

## 🚨 **GESTION DES ERREURS**

### **Erreurs Courantes**

#### **1. Fichier de Licence Introuvable**
```
❌ Fichier de licence introuvable.
Veuillez créer le fichier : ~/.lcpi/license.key
```

**Solution :** Créer le dossier `.lcpi` et le fichier `license.key`

#### **2. Clé de Licence Invalide**
```
❌ La clé de licence est invalide ou corrompue.
```

**Solution :** Vérifier que la clé a été copiée complètement sans espaces

#### **3. Licence pour Autre Machine**
```
❌ La licence n'est pas valide pour cette machine.
```

**Solution :** Générer une nouvelle licence pour cette machine

#### **4. Licence Expirée**
```
❌ La licence a expiré le 2024-12-31.
```

**Solution :** Contacter le support pour renouveler la licence

### **Messages de Succès**

```
✅ Licence valide pour Jean Dupont
📅 Valide jusqu'au : 2025-12-31 23:59:59
⏱️  Jours restants : 365
🏷️  Type : premium
```

---

## 🔧 **CONFIGURATION AVANCÉE**

### **Personnalisation du Mot de Passe Maître**

Dans `generate_license.py` et `license_validator.py`, modifiez :

```python
MASTER_PASSWORD = b"VotrePhraseSecretePersonnalisee!"
```

### **Changement du Sel de Chiffrement**

```python
SALT = b'VotreSelPersonnaliseDe16Bytes'
```

### **Modification du Chemin de Licence**

```python
LICENSE_FILE_PATH = os.path.expanduser("~/.lcpi/license.key")
```

---

## 📞 **SUPPORT ET MAINTENANCE**

### **Contact Support**
- **Email** : support@lcpi-cli.com
- **Téléphone** : +33 1 23 45 67 89
- **Site web** : https://lcpi-cli.com/support

### **Procédures de Support**

#### **Renouvellement de Licence**
1. L'utilisateur contacte le support
2. Fournir l'empreinte de la machine actuelle
3. Génération d'une nouvelle licence
4. Envoi de la nouvelle clé

#### **Transfert de Licence**
1. Désactiver l'ancienne licence
2. Générer une nouvelle licence pour la nouvelle machine
3. Envoyer la nouvelle clé

#### **Récupération d'Urgence**
1. Vérification de l'identité de l'utilisateur
2. Génération d'une licence temporaire
3. Envoi de la clé de récupération

---

## 🛡️ **SÉCURITÉ ET CONFORMITÉ**

### **Bonnes Pratiques**

#### **Pour le Développeur**
- ✅ Gardez le mot de passe maître secret
- ✅ Changez le sel de chiffrement
- ✅ Sauvegardez les licences générées
- ✅ Surveillez les tentatives d'utilisation non autorisée

#### **Pour l'Utilisateur**
- ✅ Ne partagez jamais votre clé de licence
- ✅ Ne modifiez pas le fichier de licence
- ✅ Contactez le support en cas de problème
- ✅ Sauvegardez votre clé de licence

### **Protection Contre le Piratage**

- **Chiffrement robuste** : Impossibilité de déchiffrer sans la clé maître
- **Liaison matérielle** : Empêche l'utilisation sur d'autres machines
- **Vérification d'intégrité** : Détection des modifications
- **Expiration automatique** : Contrôle de la durée d'utilisation

---

## 📊 **STATISTIQUES ET MONITORING**

### **Informations de Licence**

```python
from src.lcpi.license_validator import get_license_info, get_days_remaining

# Informations complètes
license_info = get_license_info()
print(f"Utilisateur: {license_info['user_name']}")
print(f"Type: {license_info['license_type']}")
print(f"Expiration: {license_info['expiration_date']}")

# Jours restants
days_left = get_days_remaining()
print(f"Jours restants: {days_left}")
```

### **Logs de Validation**

Le système peut être étendu pour logger :
- Tentatives de validation
- Erreurs de licence
- Utilisation des fonctionnalités
- Tentatives de contournement

---

## 🎯 **CONCLUSION**

Le système de licence LCPI-CLI offre :

### **✅ Avantages**
- **Protection robuste** contre l'utilisation non autorisée
- **Facilité d'utilisation** pour les utilisateurs finaux
- **Flexibilité** pour différents types de licences
- **Sécurité** avec chiffrement et liaison matérielle
- **Maintenance** simple et automatisée

### **🔧 Fonctionnalités**
- Génération sécurisée de licences
- Validation automatique au démarrage
- Gestion des types de licence
- Contrôle de l'expiration
- Messages d'erreur informatifs

### **🛡️ Sécurité**
- Chiffrement Fernet avec PBKDF2
- Liaison à l'empreinte matérielle
- Protection contre la modification
- Vérification d'intégrité

**Le système de licence LCPI-CLI est maintenant opérationnel et prêt à protéger votre logiciel !** 🚀

---

*Guide généré automatiquement | Système de Licence v1.0 | LCPI-CLI* 