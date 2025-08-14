# 🔐 LICENCE ADMIN STANDARD LCPI-CLI

## 📋 **INFORMATIONS DE LA LICENCE**

- **👤 Utilisateur** : admin
- **🏷️ Type** : Standard
- **⏱️ Validité** : 365 jours (1 an)
- **🖥️ Machine** : 0x525a65ffa2a5
- **📅 Date de génération** : Août 2025
- **📅 Expiration** : Août 2026

## 📁 **FICHIERS ASSOCIÉS**

- **Licence principale** : `licence_admin_standard.key` (chiffrée)
- **Guide d'utilisation** : `docs/GUIDE_UTILISATION_LICENCE.md`
- **Générateur** : `tools/generate_license_improved.py`

## 🚀 **INSTALLATION**

1. **Créer le dossier de licence** :
   ```bash
   mkdir %USERPROFILE%\.lcpi
   ```

2. **Installer la licence** :
   ```bash
   copy "licence_admin_standard.key" "%USERPROFILE%\.lcpi\license.key"
   ```

3. **Vérifier l'activation** :
   ```bash
   lcpi --help
   ```

## 🔍 **VÉRIFICATION**

```bash
python -c "
import sys
sys.path.insert(0, 'src')
from lcpi.license_validator import validate_license

is_valid, message = validate_license()
print(f'Licence valide: {is_valid}')
print(f'Message: {message}')
"
```

## 📞 **SUPPORT**

- **Email** : support@lcpi-cli.com
- **Documentation** : docs/GUIDE_UTILISATION_LICENCE.md

---

*Licence générée automatiquement par le système LCPI-CLI*
*Ne pas modifier ce fichier - Utilisation soumise à licence*
