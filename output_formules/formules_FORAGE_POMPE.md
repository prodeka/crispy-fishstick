# Extraction des formules Excel

## Feuille : FORAGE_POMPE

| Ligne | Colonne | Cellule | Formule | Valeur calculée |
|-------|---------|---------|---------|-----------------|
| Ligne 14 | Col 13 | M14 | `=ADUCTION!C3` | =ADUCTION!C3 |
| Ligne 14 | Col 14 | N14 | `=ADUCTION!I5` | =ADUCTION!I5 |
| Ligne 14 | Col 15 | O14 | `=N14/1000` | =N14/1000 |
| Ligne 14 | Col 16 | P14 | `=ADUCTION!H5` | =ADUCTION!H5 |
| Ligne 14 | Col 17 | Q14 | `=ADUCTION!O5` | =ADUCTION!O5 |
| Ligne 14 | Col 18 | R14 | `=1.05*(4^(10/3)*H17^2*Q14/(PI()^2*H24^2*O14^(16/3)))` | =1.05*(4^(10/3)*H17^2*Q14/(PI()^2*H24^2*O14^(16/3))) |
| Ligne 15 | Col 13 | M15 | `=ADUCTION!C33` | =ADUCTION!C33 |
| Ligne 15 | Col 14 | N15 | `=ADUCTION!I35` | =ADUCTION!I35 |
| Ligne 15 | Col 15 | O15 | `=N15/1000` | =N15/1000 |
| Ligne 15 | Col 16 | P15 | `=ADUCTION!H35` | =ADUCTION!H35 |
| Ligne 15 | Col 17 | Q15 | `=ADUCTION!O35` | =ADUCTION!O35 |
| Ligne 15 | Col 18 | R15 | `=1.05*(4^(10/3)*H17^2*Q15/(PI()^2*H24^2*O15^(16/3)))` | =1.05*(4^(10/3)*H17^2*Q15/(PI()^2*H24^2*O15^(16/3))) |
| Ligne 16 | Col 13 | M16 | `=ADUCTION!C43` | =ADUCTION!C43 |
| Ligne 16 | Col 14 | N16 | `=ADUCTION!I45` | =ADUCTION!I45 |
| Ligne 16 | Col 15 | O16 | `=N16/1000` | =N16/1000 |
| Ligne 16 | Col 16 | P16 | `=ADUCTION!H45` | =ADUCTION!H45 |
| Ligne 16 | Col 17 | Q16 | `=ADUCTION!O45` | =ADUCTION!O45 |
| Ligne 16 | Col 18 | R16 | `=1.05*(4^(10/3)*H17^2*Q16/(PI()^2*H24^2*O16^(16/3)))` | =1.05*(4^(10/3)*H17^2*Q16/(PI()^2*H24^2*O16^(16/3))) |
| Ligne 17 | Col 8 | H17 | `=H16/3600` | =H16/3600 |
| Ligne 17 | Col 9 | I17 | `=I16/3600` | =I16/3600 |
| Ligne 17 | Col 10 | J17 | `=J16/3600` | =J16/3600 |
| Ligne 17 | Col 14 | N17 | `=ADUCTION!I14` | =ADUCTION!I14 |
| Ligne 17 | Col 15 | O17 | `=N17/1000` | =N17/1000 |
| Ligne 17 | Col 16 | P17 | `=ADUCTION!H14` | =ADUCTION!H14 |
| Ligne 17 | Col 17 | Q17 | `=ADUCTION!O14` | =ADUCTION!O14 |
| Ligne 17 | Col 18 | R17 | `=1.05*(4^(10/3)*I17^2*Q17/(PI()^2*I24^2*O17^(16/3)))` | =1.05*(4^(10/3)*I17^2*Q17/(PI()^2*I24^2*O17^(16/3))) |
| Ligne 18 | Col 13 | M18 | `=M15` | =M15 |
| Ligne 19 | Col 13 | M19 | `=M16` | =M16 |
| Ligne 20 | Col 8 | H20 | `=H18*H16` | =H18*H16 |
| Ligne 20 | Col 9 | I20 | `=I18*I16` | =I18*I16 |
| Ligne 20 | Col 10 | J20 | `=J18*J16` | =J18*J16 |
| Ligne 20 | Col 14 | N20 | `=ADUCTION!I24` | =ADUCTION!I24 |
| Ligne 20 | Col 15 | O20 | `=N20/1000` | =N20/1000 |
| Ligne 20 | Col 16 | P20 | `=ADUCTION!H24` | =ADUCTION!H24 |
| Ligne 20 | Col 17 | Q20 | `=ADUCTION!O24` | =ADUCTION!O24 |
| Ligne 20 | Col 18 | R20 | `=1.05*(4^(10/3)*J17^2*Q20/(PI()^2*J24^2*O20^(16/3)))` | =1.05*(4^(10/3)*J17^2*Q20/(PI()^2*J24^2*O20^(16/3))) |
| Ligne 21 | Col 13 | M21 | `=M19` | =M19 |
| Ligne 25 | Col 8 | H25 | `=SUM(R14:R16)` | =SUM(R14:R16) |
| Ligne 25 | Col 9 | I25 | `=SUM(R17:R19)` | =SUM(R17:R19) |
| Ligne 25 | Col 10 | J25 | `=SUM(R20:R21)` | =SUM(R20:R21) |
| Ligne 26 | Col 8 | H26 | `=RESERVOIR!$E$34` | =RESERVOIR!$E$34 |
| Ligne 26 | Col 9 | I26 | `=RESERVOIR!$E$34` | =RESERVOIR!$E$34 |
| Ligne 26 | Col 10 | J26 | `=RESERVOIR!$E$34` | =RESERVOIR!$E$34 |
| Ligne 27 | Col 8 | H27 | `=(H23-H15)+H26` | =(H23-H15)+H26 |
| Ligne 27 | Col 9 | I27 | `=(I23-I15)+I26` | =(I23-I15)+I26 |
| Ligne 27 | Col 10 | J27 | `=(J23-J15)+J26` | =(J23-J15)+J26 |
| Ligne 28 | Col 8 | H28 | `=H27+H25` | =H27+H25 |
| Ligne 28 | Col 9 | I28 | `=I27+I25` | =I27+I25 |
| Ligne 28 | Col 10 | J28 | `=J27+J25` | =J27+J25 |