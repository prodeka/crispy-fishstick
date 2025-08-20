# 📊 Rapport d'Optimisation de Réseau

**Date de génération:** 2025-08-20 00:12:08
**Méthode d'optimisation:** nested
**Solveurs utilisés:** epanet, lcpi

---

## 🎯 Résumé Exécutif

**Comparaison multi-solveurs:**
- **EPANET:** CAPEX 7,500.00 FCFA
- **LCPI:** CAPEX 7,200.00 FCFA

## ⚙️ Configuration

### Paramètres d'optimisation
- **Méthode:** nested
- **Solveurs:** epanet, lcpi

### Contraintes
- **Pression minimale:** 12.0 m
- **Vitesse maximale:** 2.0 m/s

## 🔍 Résultats - EPANET

**Méthode:** nested
**Source:** test.inp

### Propositions d'optimisation

#### Proposition 1
- **ID:** nested_best
- **CAPEX:** 7,500.00 FCFA
- **Hauteur réservoir:** 17.0 m
- **Contraintes respectées:** ✅
- **Diamètres des conduites:**
  - N1_N2: 156 mm
  - N2_N3: 108 mm

---

## 🔍 Résultats - LCPI

**Méthode:** nested
**Source:** test.inp

### Propositions d'optimisation

#### Proposition 1
- **ID:** nested_best
- **CAPEX:** 7,200.00 FCFA
- **Hauteur réservoir:** 16.5 m
- **Contraintes respectées:** ✅
- **Diamètres des conduites:**
  - N1_N2: 150 mm
  - N2_N3: 100 mm

---

## 📈 Comparaison des Solveurs

| Solveur | CAPEX (FCFA) | Hauteur Réservoir (m) | Contraintes |
|---------|--------------|----------------------|-------------|
| EPANET | 7,500.00 | 17.0 | ✅ |
| LCPI | 7,200.00 | 16.5 | ✅ |

## 🔧 Détails Techniques

### Métadonnées des fichiers
**EPANET:**
- **Checksum:** test123
- **Signature:** sig123
- **Validité:** ✅

**LCPI:**
- **Checksum:** test456
- **Signature:** sig456
- **Validité:** ✅

### Informations de performance
**EPANET:** Temps d'exécution: 1.50s
**LCPI:** Temps d'exécution: 0.80s

---

*Rapport généré automatiquement par LCPI-CLI*
*Version: 1.0.0 | Date: 2025-08-20*