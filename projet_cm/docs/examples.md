# Exemples d'Utilisation - projet_cm

## Plugins Disponibles

### CM
- Vérification de poteaux en compression/flambement
- Vérification de poutres en flexion
- Vérification d'assemblages boulonnés/soudés
- Optimisation de sections

## Exemples de Fichiers de Données

### Construction Métallique (CM)
```yaml
# data/cm/poutre_exemple.yml
element_id: P1
description: "Poutre principale"
materiau:
  nuance: S235
  fy_MPa: 235.0
geometrie:
  type_profil: IPE
  longueur_m: 8.0
charges:
  permanentes_G:
    - type: repartie
      valeur: 5.0
```

### Construction Bois
```yaml
# data/bois/poteau_exemple.yml
description: "Poteau en bois C24"
profil:
  type: "rectangulaire"
  dimensions_mm:
    b: 150
    h: 150
materiau:
  classe_resistance: "C24"
  classe_service: 2
longueur_flambement_m: 4.5
efforts_elu:
  N_c_ed_kN: 80
```

### Béton Armé
```yaml
# data/beton/poteau_exemple.yml
element_id: P1
description: "Poteau béton armé"
materiaux:
  fc28_MPa: 25.0
  fe_MPa: 500.0
geometrie:
  section_mm:
    b: 300
    h: 300
  longueur_m: 3.0
efforts:
  N_ed_kN: 500
  M_ed_kNm: 50
```

### Hydrologie
```yaml
# data/hydro/canal_exemple.yml
debit_projet_m3s: 10.0
k_strickler: 30.0
vitesse_max_admissible_ms: 1.5
pente_m_m: 0.001
fruit_talus_z: 1.5
```
