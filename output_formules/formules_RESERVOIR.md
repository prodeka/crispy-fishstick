# Extraction des formules Excel

## Feuille : RESERVOIR

| Ligne | Colonne | Cellule | Formule | Valeur calculée |
|-------|---------|---------|---------|-----------------|
| Ligne 23 | Col 5 | E23 | `='BESOIN SELON ETAT'!$J$42 * 30%` | ='BESOIN SELON ETAT'!$J$42 * 30% |
| Ligne 23 | Col 9 | I23 | `='DEMANDE SELON ETAT'!$M$12` | ='DEMANDE SELON ETAT'!$M$12 |
| Ligne 25 | Col 5 | E25 | `=0.02*E23` | =0.02*E23 |
| Ligne 26 | Col 5 | E26 | `=('BESOIN SELON ETAT'!$J$42)*(2/24)` | =('BESOIN SELON ETAT'!$J$42)*(2/24) |
| Ligne 26 | Col 9 | I26 | `=(PI() * I25^2) / 4` | =(PI() * I25^2) / 4 |
| Ligne 26 | Col 13 | M26 | `=(PI() * M25^2) / 4` | =(PI() * M25^2) / 4 |
| Ligne 27 | Col 5 | E27 | `=E26+E25+E24+E23` | =E26+E25+E24+E23 |
| Ligne 27 | Col 9 | I27 | `=I23/I26` | =I23/I26 |
| Ligne 27 | Col 13 | M27 | `=M23/M26` | =M23/M26 |
| Ligne 28 | Col 9 | I28 | `=I22+I24+I27` | =I22+I24+I27 |
| Ligne 28 | Col 13 | M28 | `=M22+M24+M27` | =M22+M24+M27 |
| Ligne 29 | Col 5 | E29 | `=ROUND(MAX(SUITE_DIM_PIPE!EC38,SUITE_DIM_PIPE!DI53,SUITE_DIM_PIPE!CO46,SUITE_DIM_PIPE!BT57,SUITE_DIM_PIPE!AZ42,SUITE_DIM_PIPE!AG75,SUITE_DIM_PIPE!O75)-E22,0)` | =ROUND(MAX(SUITE_DIM_PIPE!EC38,SUITE_DIM_PIPE!DI53,SUITE_DIM_PIPE!CO46,SUITE_DIM_PIPE!BT57,SUITE_DIM_PIPE!AZ42,SUITE_DIM_PIPE!AG75,SUITE_DIM_PIPE!O75)-E22,0) |
| Ligne 31 | Col 5 | E31 | `=(PI() * E30^2) / 4` | =(PI() * E30^2) / 4 |
| Ligne 32 | Col 5 | E32 | `=E28/E31` | =E28/E31 |
| Ligne 34 | Col 5 | E34 | `=E22+E29+E33` | =E22+E29+E33 |