# Valeurs des cellules Excel

## Feuille : RESERVOIR

| Ligne | Colonne | Cellule | Type | Contenu | Valeur calculée |
|-------|---------|---------|------|---------|-----------------|
| Ligne 18 | Col 4 | D18 | Valeur | R3 | R3 |
| Ligne 18 | Col 8 | H18 | Valeur | R2 | R2 |
| Ligne 18 | Col 12 | L18 | Valeur | R1 | R1 |
| Ligne 19 | Col 4 | D19 | Valeur | ID | ID |
| Ligne 19 | Col 5 | E19 | Valeur | R3 | R3 |
| Ligne 19 | Col 8 | H19 | Valeur | ID | ID |
| Ligne 19 | Col 9 | I19 | Valeur | R2 | R2 |
| Ligne 19 | Col 12 | L19 | Valeur | ID | ID |
| Ligne 19 | Col 13 | M19 | Valeur | R2 | R2 |
| Ligne 20 | Col 4 | D20 | Valeur | Longitude | Longitude |
| Ligne 20 | Col 5 | E20 | Valeur | 1.21601051858914 | 1.21601051858914 |
| Ligne 20 | Col 8 | H20 | Valeur | Longitude | Longitude |
| Ligne 20 | Col 9 | I20 | Valeur | 1.2235468 | 1.2235468 |
| Ligne 20 | Col 12 | L20 | Valeur | Longitude | Longitude |
| Ligne 20 | Col 13 | M20 | Valeur | 1.2329531375 | 1.2329531375 |
| Ligne 21 | Col 4 | D21 | Valeur | Latitude | Latitude |
| Ligne 21 | Col 5 | E21 | Valeur | 6.27708976509202 | 6.27708976509202 |
| Ligne 21 | Col 8 | H21 | Valeur | Latitude | Latitude |
| Ligne 21 | Col 9 | I21 | Valeur | 6.261949885 | 6.261949885 |
| Ligne 21 | Col 12 | L21 | Valeur | Latitude | Latitude |
| Ligne 21 | Col 13 | M21 | Valeur | 6.24483232749999 | 6.24483232749999 |
| Ligne 22 | Col 4 | D22 | Valeur | Altitude | Altitude |
| Ligne 22 | Col 5 | E22 | Valeur | 12 | 12 |
| Ligne 22 | Col 8 | H22 | Valeur | Altitude | Altitude |
| Ligne 22 | Col 9 | I22 | Valeur | 17 | 17 |
| Ligne 22 | Col 12 | L22 | Valeur | Altitude | Altitude |
| Ligne 22 | Col 13 | M22 | Valeur | 12 | 12 |
| Ligne 23 | Col 4 | D23 | Valeur | Cu_reel (m^3) | Cu_reel (m^3) |
| Ligne 23 | Col 5 | E23 | Formule | ='BESOIN SELON ETAT'!$J$42 * 30% | ='BESOIN SELON ETAT'!$J$42 * 30% |
| Ligne 23 | Col 8 | H23 | Valeur | C_total (m^3) | C_total (m^3) |
| Ligne 23 | Col 9 | I23 | Formule | ='DEMANDE SELON ETAT'!$M$12 | ='DEMANDE SELON ETAT'!$M$12 |
| Ligne 23 | Col 12 | L23 | Valeur | C_total (m^3) | C_total (m^3) |
| Ligne 23 | Col 13 | M23 | Valeur | 90 | 90 |
| Ligne 24 | Col 4 | D24 | Valeur | Reserve_incendie (m^3) | Reserve_incendie (m^3) |
| Ligne 24 | Col 5 | E24 | Valeur | 120 | 120 |
| Ligne 24 | Col 8 | H24 | Valeur | h_sous_cuve (m) | h_sous_cuve (m) |
| Ligne 24 | Col 9 | I24 | Valeur | 15 | 15 |
| Ligne 24 | Col 12 | L24 | Valeur | h_sous_cuve (m) | h_sous_cuve (m) |
| Ligne 24 | Col 13 | M24 | Valeur | 15 | 15 |
| Ligne 25 | Col 4 | D25 | Valeur | V_mort | V_mort |
| Ligne 25 | Col 5 | E25 | Formule | =0.02*E23 | =0.02*E23 |
| Ligne 25 | Col 8 | H25 | Valeur | Diametre (m) | Diametre (m) |
| Ligne 25 | Col 9 | I25 | Valeur | 7 | 7 |
| Ligne 25 | Col 12 | L25 | Valeur | Diametre (m) | Diametre (m) |
| Ligne 25 | Col 13 | M25 | Valeur | 5 | 5 |
| Ligne 26 | Col 4 | D26 | Valeur | V_reserve_sec | V_reserve_sec |
| Ligne 26 | Col 5 | E26 | Formule | =('BESOIN SELON ETAT'!$J$42)*(2/24) | =('BESOIN SELON ETAT'!$J$42)*(2/24) |
| Ligne 26 | Col 8 | H26 | Valeur | Section (m) | Section (m) |
| Ligne 26 | Col 9 | I26 | Formule | =(PI() * I25^2) / 4 | =(PI() * I25^2) / 4 |
| Ligne 26 | Col 12 | L26 | Valeur | Section (m) | Section (m) |
| Ligne 26 | Col 13 | M26 | Formule | =(PI() * M25^2) / 4 | =(PI() * M25^2) / 4 |
| Ligne 27 | Col 4 | D27 | Valeur | Ct_ajusté (m^3) | Ct_ajusté (m^3) |
| Ligne 27 | Col 5 | E27 | Formule | =E26+E25+E24+E23 | =E26+E25+E24+E23 |
| Ligne 27 | Col 8 | H27 | Valeur | h_total (m) | h_total (m) |
| Ligne 27 | Col 9 | I27 | Formule | =I23/I26 | =I23/I26 |
| Ligne 27 | Col 12 | L27 | Valeur | h_total (m) | h_total (m) |
| Ligne 27 | Col 13 | M27 | Formule | =M23/M26 | =M23/M26 |
| Ligne 28 | Col 4 | D28 | Valeur | Ct_choisie (m^3) | Ct_choisie (m^3) |
| Ligne 28 | Col 5 | E28 | Valeur | 7200 | 7200 |
| Ligne 28 | Col 8 | H28 | Valeur | Z_cuve (m) | Z_cuve (m) |
| Ligne 28 | Col 9 | I28 | Formule | =I22+I24+I27 | =I22+I24+I27 |
| Ligne 28 | Col 12 | L28 | Valeur | Z_cuve (m) | Z_cuve (m) |
| Ligne 28 | Col 13 | M28 | Formule | =M22+M24+M27 | =M22+M24+M27 |
| Ligne 29 | Col 4 | D29 | Valeur | h_sous_cuve_min (m) | h_sous_cuve_min (m) |
| Ligne 29 | Col 5 | E29 | Formule | =ROUND(MAX(SUITE_DIM_PIPE!EC38,SUITE_DIM_PIPE!DI53,SUITE_DIM_PIPE!CO46,SUITE_DIM_PIPE!BT57,SUITE_DIM_PIPE!AZ42,SUITE_DIM_PIPE!AG75,SUITE_DIM_PIPE!O75)-E22,0) | =ROUND(MAX(SUITE_DIM_PIPE!EC38,SUITE_DIM_PIPE!DI53,SUITE_DIM_PIPE!CO46,SUITE_DIM_PIPE!BT57,SUITE_DIM_PIPE!AZ42,SUITE_DIM_PIPE!AG75,SUITE_DIM_PIPE!O75)-E22,0) |
| Ligne 29 | Col 6 | F29 | Valeur | 75 | 75 |
| Ligne 30 | Col 4 | D30 | Valeur | Diametre (m) | Diametre (m) |
| Ligne 30 | Col 5 | E30 | Valeur | 17 | 17 |
| Ligne 31 | Col 4 | D31 | Valeur | Section (m^2) | Section (m^2) |
| Ligne 31 | Col 5 | E31 | Formule | =(PI() * E30^2) / 4 | =(PI() * E30^2) / 4 |
| Ligne 32 | Col 4 | D32 | Valeur | h_utile (m) | h_utile (m) |
| Ligne 32 | Col 5 | E32 | Formule | =E28/E31 | =E28/E31 |
| Ligne 33 | Col 4 | D33 | Valeur | h_total (m) | h_total (m) |
| Ligne 33 | Col 5 | E33 | Valeur | 32 | 32 |
| Ligne 34 | Col 4 | D34 | Valeur | Z_cuve (m) | Z_cuve (m) |
| Ligne 34 | Col 5 | E34 | Formule | =E22+E29+E33 | =E22+E29+E33 |