# Rapport de Conversion CSV → YAML/SQLite

**Date:** 2025-08-28 00:10:51
**Source:** ..\src\lcpi\db\grundfos_pompes_230_modeles_complet.csv
**Taux de change:** 1 EUR = 655.957 FCFA
**Coût électricité:** 98.39 FCFA/kWh

## 📊 Statistiques Générales

- **Total pompes:** 203
- **Marques:** 1
- **Types de moteur:** 12
- **Matériaux:** 2

## 💰 Analyse des Coûts (EUR)

- **CAPEX min:** 29.00 €
- **CAPEX max:** 19200.00 €
- **CAPEX moyen:** 2203.45 €

- **OPEX min:** 0.181 €/kWh
- **OPEX max:** 0.600 €/kWh
- **OPEX moyen:** 0.253 €/kWh

## 💰 Analyse des Coûts (FCFA)

- **CAPEX min:** 19,023 FCFA
- **CAPEX max:** 12,594,374 FCFA
- **CAPEX moyen:** 1,445,371 FCFA

- **OPEX min:** 86.68 FCFA/kWh
- **OPEX max:** 18966.75 FCFA/kWh
- **OPEX moyen:** 3033.14 FCFA/kWh

## 🔄 Conversion des Unités

- **Débits convertis:** m³/h → m³/s (divisé par 3600)
- **Plage de débits (m³/s):** 0.000056 - 0.111111
- **Prix convertis:** EUR → FCFA (× 655.957)
- **OPEX estimé:** Basé sur puissance absorbée et coût électricité local

## 📁 Fichiers Générés

- **YAML:** `..\pompes_converted_fcfa\grundfos_pompes_230_modeles_complet_converted.yaml`
- **SQLite:** `..\pompes_converted_fcfa\grundfos_pompes_230_modeles_complet_pompes.db`
- **Log:** `conversion.log`

## 🔍 Validation des Données

- **Lignes parsées:** 203
- **Désignations uniques:** 203
- **Données complètes:** 203

## 📋 Marques Disponibles

- **Grundfos:** 203 pompes

## ✅ Conversion Terminée avec Succès

Les données ont été converties et sont prêtes pour:
- **Tests:** Utilisez le fichier YAML
- **Production:** Utilisez la base SQLite
- **EPANET:** Débits en m³/s, coûts en FCFA
- **Optimisation:** OPEX estimé basé sur la puissance absorbée
