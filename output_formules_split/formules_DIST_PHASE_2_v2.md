# Extraction des formules Excel

## Feuille : DIST_PHASE_2_v2

| Ligne | Colonne | Cellule | Formule | Valeur calculée |
|-------|---------|---------|---------|-----------------|
| Ligne 16 | Col 4 | D16 | `='DIST _PHASE_1_V1'!D3` | ='DIST _PHASE_1_V1'!D3 |
| Ligne 16 | Col 5 | E16 | `='DIST _PHASE_1_V1'!F3` | ='DIST _PHASE_1_V1'!F3 |
| Ligne 16 | Col 6 | F16 | `='DIST _PHASE_1_V1'!K3` | ='DIST _PHASE_1_V1'!K3 |
| Ligne 16 | Col 7 | G16 | `='DIST _PHASE_1_V1'!L3` | ='DIST _PHASE_1_V1'!L3 |
| Ligne 16 | Col 8 | H16 | `='DIST _PHASE_1_V1'!M3` | ='DIST _PHASE_1_V1'!M3 |
| Ligne 16 | Col 9 | I16 | `= (10.679 * H16) / ((F16/1000)^4.871 * G16^1.852)` | = (10.679 * H16) / ((F16/1000)^4.871 * G16^1.852) |
| Ligne 16 | Col 10 | J16 | `=IF(C16="positif",E16,IF(C16="negatif",-E16,""))` | =IF(C16="positif",E16,IF(C16="negatif",-E16,"")) |
| Ligne 16 | Col 11 | K16 | `=IF(J16>0,I16*E16^1.852,-I16*E16^1.852)` | =IF(J16>0,I16*E16^1.852,-I16*E16^1.852) |
| Ligne 16 | Col 12 | L16 | `=1.852*I16*E16^(1.852-1)` | =1.852*I16*E16^(1.852-1) |
| Ligne 16 | Col 13 | M16 | `=J16+$F$83` | =J16+$F$83 |
| Ligne 16 | Col 36 | AJ16 | `=IFERROR(MATCH(AM16,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM16,$S$22:$S$91,0),0) |
| Ligne 16 | Col 38 | AL16 | `=DIST_PHASE_1_v2!AI5` | =DIST_PHASE_1_v2!AI5 |
| Ligne 16 | Col 39 | AM16 | `=DIST_PHASE_1_v2!AJ5` | =DIST_PHASE_1_v2!AJ5 |
| Ligne 16 | Col 40 | AN16 | `=DIST_PHASE_1_v2!AL5` | =DIST_PHASE_1_v2!AL5 |
| Ligne 16 | Col 41 | AO16 | `=DIST_PHASE_1_v2!AQ5` | =DIST_PHASE_1_v2!AQ5 |
| Ligne 16 | Col 43 | AQ16 | `=DIST_PHASE_1_v2!AS5` | =DIST_PHASE_1_v2!AS5 |
| Ligne 16 | Col 44 | AR16 | `= (10.679 * AQ16) / ((AO16/1000)^4.871 * AP16^1.852)` | = (10.679 * AQ16) / ((AO16/1000)^4.871 * AP16^1.852) |
| Ligne 16 | Col 45 | AS16 | `=IF(AL16="positif",AN16,IF(AL16="negatif",-AN16,""))` | =IF(AL16="positif",AN16,IF(AL16="negatif",-AN16,"")) |
| Ligne 16 | Col 46 | AT16 | `=IF(AS16>0,AR16*AN16^1.852,-AR16*AN16^1.852)` | =IF(AS16>0,AR16*AN16^1.852,-AR16*AN16^1.852) |
| Ligne 16 | Col 47 | AU16 | `=1.852*AR16*AN16^(1.852-1)` | =1.852*AR16*AN16^(1.852-1) |
| Ligne 16 | Col 48 | AV16 | `=AS16+$S$93` | =AS16+$S$93 |
| Ligne 16 | Col 52 | AZ16 | `=IFERROR(MATCH(BC16,$S$22:$S$91,0),0)` | =IFERROR(MATCH(BC16,$S$22:$S$91,0),0) |
| Ligne 16 | Col 54 | BB16 | `=DIST_PHASE_1_v2!BL5` | =DIST_PHASE_1_v2!BL5 |
| Ligne 16 | Col 55 | BC16 | `=DIST_PHASE_1_v2!BM5` | =DIST_PHASE_1_v2!BM5 |
| Ligne 16 | Col 56 | BD16 | `=DIST_PHASE_1_v2!BO5` | =DIST_PHASE_1_v2!BO5 |
| Ligne 16 | Col 57 | BE16 | `=DIST_PHASE_1_v2!BT5` | =DIST_PHASE_1_v2!BT5 |
| Ligne 16 | Col 59 | BG16 | `=DIST_PHASE_1_v2!BV5` | =DIST_PHASE_1_v2!BV5 |
| Ligne 16 | Col 60 | BH16 | `= (10.679 * BG16) / ((BE16/1000)^4.871 * BF16^1.852)` | = (10.679 * BG16) / ((BE16/1000)^4.871 * BF16^1.852) |
| Ligne 16 | Col 61 | BI16 | `=IF(BB16="positif",BD16,IF(BB16="negatif",-BD16,""))` | =IF(BB16="positif",BD16,IF(BB16="negatif",-BD16,"")) |
| Ligne 16 | Col 62 | BJ16 | `=IF(AZ16>0,
        IF(BI16>0, BH16*BI16^1.852,-BH16*ABS(BI16)^1.852),
        IF(BI16>0, BH16*BD16^1.852, -BH16*BD16^1.852))` | =IF(AZ16>0,
        IF(BI16>0, BH16*BI16^1.852,-BH16*ABS(BI16)^1.852),
        IF(BI16>0, BH16*BD16^1.852, -BH16*BD16^1.852)) |
| Ligne 16 | Col 63 | BK16 | `=1.852*BH16*BD16^(1.852-1)` | =1.852*BH16*BD16^(1.852-1) |
| Ligne 16 | Col 64 | BL16 | `=BI16+$S$93` | =BI16+$S$93 |
| Ligne 16 | Col 68 | BP16 | `=IFERROR(MATCH(BS16,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BS16,$AM$22:$AM$57,0),0) |
| Ligne 16 | Col 70 | BR16 | `=DIST_PHASE_1_v2!BG5` | =DIST_PHASE_1_v2!BG5 |
| Ligne 16 | Col 71 | BS16 | `=DIST_PHASE_1_v2!BH5` | =DIST_PHASE_1_v2!BH5 |
| Ligne 16 | Col 72 | BT16 | `=DIST_PHASE_1_v2!BJ5` | =DIST_PHASE_1_v2!BJ5 |
| Ligne 16 | Col 73 | BU16 | `=DIST_PHASE_1_v2!BO5` | =DIST_PHASE_1_v2!BO5 |
| Ligne 16 | Col 74 | BV16 | `=DIST_PHASE_1_v2!BP5` | =DIST_PHASE_1_v2!BP5 |
| Ligne 16 | Col 75 | BW16 | `=DIST_PHASE_1_v2!BQ5` | =DIST_PHASE_1_v2!BQ5 |
| Ligne 16 | Col 76 | BX16 | `= (10.679 * BW16) / ((BU16/1000)^4.871 * BV16^1.852)` | = (10.679 * BW16) / ((BU16/1000)^4.871 * BV16^1.852) |
| Ligne 16 | Col 77 | BY16 | `=IF(BR16="positif",BT16,IF(BR16="negatif",-BT16,""))` | =IF(BR16="positif",BT16,IF(BR16="negatif",-BT16,"")) |
| Ligne 16 | Col 78 | BZ16 | `=IF(BP16>0,
        IF(BY16>0, BX16*BY16^1.852,-BX16*ABS(BY16)^1.852),
        IF(BY16>0, BX16*BT16^1.852, -BX16*BT16^1.852))` | =IF(BP16>0,
        IF(BY16>0, BX16*BY16^1.852,-BX16*ABS(BY16)^1.852),
        IF(BY16>0, BX16*BT16^1.852, -BX16*BT16^1.852)) |
| Ligne 16 | Col 79 | CA16 | `=1.852*BX16*ABS(BY16)^(1.852-1)` | =1.852*BX16*ABS(BY16)^(1.852-1) |
| Ligne 16 | Col 80 | CB16 | `=BY16+$BT$64` | =BY16+$BT$64 |
| Ligne 16 | Col 84 | CF16 | `=IFERROR(MATCH(CI16,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI16,$BS$22:$BS$62,0),0) |
| Ligne 16 | Col 86 | CH16 | `=DIST_PHASE_1_v2!BW5` | =DIST_PHASE_1_v2!BW5 |
| Ligne 16 | Col 87 | CI16 | `=DIST_PHASE_1_v2!BX5` | =DIST_PHASE_1_v2!BX5 |
| Ligne 16 | Col 88 | CJ16 | `=DIST_PHASE_1_v2!BZ5` | =DIST_PHASE_1_v2!BZ5 |
| Ligne 16 | Col 89 | CK16 | `=DIST_PHASE_1_v2!CE5` | =DIST_PHASE_1_v2!CE5 |
| Ligne 16 | Col 90 | CL16 | `=DIST_PHASE_1_v2!CF5` | =DIST_PHASE_1_v2!CF5 |
| Ligne 16 | Col 91 | CM16 | `=DIST_PHASE_1_v2!CG5` | =DIST_PHASE_1_v2!CG5 |
| Ligne 16 | Col 92 | CN16 | `= (10.679 * CM16) / ((CK16/1000)^4.871 * CL16^1.852)` | = (10.679 * CM16) / ((CK16/1000)^4.871 * CL16^1.852) |
| Ligne 16 | Col 93 | CO16 | `=IF(CH16="positif",CJ16,IF(CH16="negatif",-CJ16,""))` | =IF(CH16="positif",CJ16,IF(CH16="negatif",-CJ16,"")) |
| Ligne 16 | Col 94 | CP16 | `=IF(CF16>0,
        IF(CO16>0, CN16*CO16^1.852,-CN16*ABS(CO16)^1.852),
        IF(CO16>0, CN16*CJ16^1.852, -CN16*CJ16^1.852))` | =IF(CF16>0,
        IF(CO16>0, CN16*CO16^1.852,-CN16*ABS(CO16)^1.852),
        IF(CO16>0, CN16*CJ16^1.852, -CN16*CJ16^1.852)) |
| Ligne 16 | Col 95 | CQ16 | `=1.852*CN16*ABS(CO16)^(1.852-1)` | =1.852*CN16*ABS(CO16)^(1.852-1) |
| Ligne 16 | Col 96 | CR16 | `=CO16+$BT$64` | =CO16+$BT$64 |
| Ligne 16 | Col 100 | CV16 | `=IFERROR(MATCH(CY16,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CY16,$BS$22:$BS$62,0),0) |
| Ligne 16 | Col 102 | CX16 | `=DIST_PHASE_1_v2!CM5` | =DIST_PHASE_1_v2!CM5 |
| Ligne 16 | Col 103 | CY16 | `=DIST_PHASE_1_v2!CN5` | =DIST_PHASE_1_v2!CN5 |
| Ligne 16 | Col 104 | CZ16 | `=DIST_PHASE_1_v2!CP5` | =DIST_PHASE_1_v2!CP5 |
| Ligne 16 | Col 105 | DA16 | `=DIST_PHASE_1_v2!CU5` | =DIST_PHASE_1_v2!CU5 |
| Ligne 16 | Col 106 | DB16 | `=DIST_PHASE_1_v2!CV5` | =DIST_PHASE_1_v2!CV5 |
| Ligne 16 | Col 107 | DC16 | `=DIST_PHASE_1_v2!CW5` | =DIST_PHASE_1_v2!CW5 |
| Ligne 16 | Col 108 | DD16 | `= (10.679 * DC16) / ((DA16/1000)^4.871 * DB16^1.852)` | = (10.679 * DC16) / ((DA16/1000)^4.871 * DB16^1.852) |
| Ligne 16 | Col 109 | DE16 | `=IF(CX16="positif",CZ16,IF(CX16="negatif",-CZ16,""))` | =IF(CX16="positif",CZ16,IF(CX16="negatif",-CZ16,"")) |
| Ligne 16 | Col 110 | DF16 | `=IF(CV16>0,
        IF(DE16>0, DD16*DE16^1.852,-DD16*ABS(DE16)^1.852),
        IF(DE16>0, DD16*CZ16^1.852, -DD16*CZ16^1.852))` | =IF(CV16>0,
        IF(DE16>0, DD16*DE16^1.852,-DD16*ABS(DE16)^1.852),
        IF(DE16>0, DD16*CZ16^1.852, -DD16*CZ16^1.852)) |
| Ligne 16 | Col 111 | DG16 | `=1.852*DD16*ABS(DE16)^(1.852-1)` | =1.852*DD16*ABS(DE16)^(1.852-1) |
| Ligne 16 | Col 112 | DH16 | `=DE16+$BT$64` | =DE16+$BT$64 |
| Ligne 22 | Col 5 | E22 | `=DIST_PHASE_1_v2!G11` | =DIST_PHASE_1_v2!G11 |
| Ligne 22 | Col 6 | F22 | `=DIST_PHASE_1_v2!L11` | =DIST_PHASE_1_v2!L11 |
| Ligne 22 | Col 7 | G22 | `=DIST_PHASE_1_v2!M11` | =DIST_PHASE_1_v2!M11 |
| Ligne 22 | Col 8 | H22 | `=DIST_PHASE_1_v2!N11` | =DIST_PHASE_1_v2!N11 |
| Ligne 22 | Col 9 | I22 | `= (10.679 * H22) / ((F22/1000)^4.871 * G22^1.852)` | = (10.679 * H22) / ((F22/1000)^4.871 * G22^1.852) |
| Ligne 22 | Col 10 | J22 | `=IF(C22="positif",E22,IF(C22="negatif",-E22,""))` | =IF(C22="positif",E22,IF(C22="negatif",-E22,"")) |
| Ligne 22 | Col 11 | K22 | `=IF(J22>0,I22*E22^1.852,-I22*E22^1.852)` | =IF(J22>0,I22*E22^1.852,-I22*E22^1.852) |
| Ligne 22 | Col 12 | L22 | `=1.852*I22*ABS(E22)^(1.852-1)` | =1.852*I22*ABS(E22)^(1.852-1) |
| Ligne 22 | Col 13 | M22 | `=J22+$D$93` | =J22+$D$93 |
| Ligne 22 | Col 16 | P22 | `=IFERROR(MATCH(S22,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S22,$D$22:$D$91,0),0) |
| Ligne 22 | Col 18 | R22 | `=DIST_PHASE_1_v2!Q11` | =DIST_PHASE_1_v2!Q11 |
| Ligne 22 | Col 19 | S22 | `=DIST_PHASE_1_v2!R11` | =DIST_PHASE_1_v2!R11 |
| Ligne 22 | Col 20 | T22 | `=DIST_PHASE_1_v2!T11` | =DIST_PHASE_1_v2!T11 |
| Ligne 22 | Col 21 | U22 | `=DIST_PHASE_1_v2!Y11` | =DIST_PHASE_1_v2!Y11 |
| Ligne 22 | Col 23 | W22 | `=DIST_PHASE_1_v2!AA11` | =DIST_PHASE_1_v2!AA11 |
| Ligne 22 | Col 24 | X22 | `= (10.679 * W22) / ((U22/1000)^4.871 * V22^1.852)` | = (10.679 * W22) / ((U22/1000)^4.871 * V22^1.852) |
| Ligne 22 | Col 25 | Y22 | `=IF(R22="positif",T22,IF(R22="negatif",-T22,""))` | =IF(R22="positif",T22,IF(R22="negatif",-T22,"")) |
| Ligne 22 | Col 26 | Z22 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD828DD0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD828DD0> |
| Ligne 22 | Col 27 | AA22 | `=IF(P22>0,
        IF(R22="positif",1,-1),
        0)` | =IF(P22>0,
        IF(R22="positif",1,-1),
        0) |
| Ligne 22 | Col 28 | AB22 | `=X22*SIGN(Y22)*ABS(Y22)^1.852` | =X22*SIGN(Y22)*ABS(Y22)^1.852 |
| Ligne 22 | Col 29 | AC22 | `=1.852*X22*ABS(Y22)^(1.852-1)` | =1.852*X22*ABS(Y22)^(1.852-1) |
| Ligne 22 | Col 30 | AD22 | `=IF(P22>0,
Y22+($D$93*Z22)+(AA22*$S$93),
Y22+$S$93)` | =IF(P22>0,
Y22+($D$93*Z22)+(AA22*$S$93),
Y22+$S$93) |
| Ligne 22 | Col 32 | AF22 | `=ABS(AD22)-ABS(Y22)` | =ABS(AD22)-ABS(Y22) |
| Ligne 22 | Col 36 | AJ22 | `=IFERROR(MATCH(AM22,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM22,$S$22:$S$91,0),0) |
| Ligne 22 | Col 38 | AL22 | `=TRONCONS_V2!AI9` | =TRONCONS_V2!AI9 |
| Ligne 22 | Col 39 | AM22 | `=TRONCONS_V2!AE9` | =TRONCONS_V2!AE9 |
| Ligne 22 | Col 40 | AN22 | `=DIST_PHASE_1_v2!AG11` | =DIST_PHASE_1_v2!AG11 |
| Ligne 22 | Col 41 | AO22 | `=DIST_PHASE_1_v2!AL11` | =DIST_PHASE_1_v2!AL11 |
| Ligne 22 | Col 43 | AQ22 | `=TRONCONS_V2!AG9` | =TRONCONS_V2!AG9 |
| Ligne 22 | Col 44 | AR22 | `= (10.679 * AQ22) / ((AO22/1000)^4.871 * AP22^1.852)` | = (10.679 * AQ22) / ((AO22/1000)^4.871 * AP22^1.852) |
| Ligne 22 | Col 45 | AS22 | `=IF(AL22="positif",AN22,IF(AL22="negatif",-AN22,""))` | =IF(AL22="positif",AN22,IF(AL22="negatif",-AN22,"")) |
| Ligne 22 | Col 46 | AT22 | `=IF(AJ22>0,
        IF(AS22>0, AR22*AS22^1.852,-AR22*ABS(AS22)^1.852),
        IF(AS22>0, AR22*AN22^1.852, -AR22*AN22^1.852))` | =IF(AJ22>0,
        IF(AS22>0, AR22*AS22^1.852,-AR22*ABS(AS22)^1.852),
        IF(AS22>0, AR22*AN22^1.852, -AR22*AN22^1.852)) |
| Ligne 22 | Col 47 | AU22 | `=1.852*AR22*ABS(AS22)^(1.852-1)` | =1.852*AR22*ABS(AS22)^(1.852-1) |
| Ligne 22 | Col 48 | AV22 | `=AS22+$AN$60` | =AS22+$AN$60 |
| Ligne 22 | Col 52 | AZ22 | `=IFERROR(MATCH(BC22,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC22,$AM$22:$AM$57,0),0) |
| Ligne 22 | Col 54 | BB22 | `=DIST_PHASE_1_v2!AQ11` | =DIST_PHASE_1_v2!AQ11 |
| Ligne 22 | Col 55 | BC22 | `=DIST_PHASE_1_v2!AR11` | =DIST_PHASE_1_v2!AR11 |
| Ligne 22 | Col 56 | BD22 | `=DIST_PHASE_1_v2!AT11` | =DIST_PHASE_1_v2!AT11 |
| Ligne 22 | Col 57 | BE22 | `=DIST_PHASE_1_v2!AY11` | =DIST_PHASE_1_v2!AY11 |
| Ligne 22 | Col 58 | BF22 | `=DIST_PHASE_1_v2!AZ11` | =DIST_PHASE_1_v2!AZ11 |
| Ligne 22 | Col 59 | BG22 | `=DIST_PHASE_1_v2!BA11` | =DIST_PHASE_1_v2!BA11 |
| Ligne 22 | Col 60 | BH22 | `= (10.679 * BG22) / ((BE22/1000)^4.871 * BF22^1.852)` | = (10.679 * BG22) / ((BE22/1000)^4.871 * BF22^1.852) |
| Ligne 22 | Col 61 | BI22 | `=IF(BB22="positif",BD22,IF(BB22="negatif",-BD22,""))` | =IF(BB22="positif",BD22,IF(BB22="negatif",-BD22,"")) |
| Ligne 22 | Col 62 | BJ22 | `=IF(AZ22>0,
        IF(BI22>0, BH22*BI22^1.852,-BH22*ABS(BI22)^1.852),
        IF(BI22>0, BH22*BD22^1.852, -BH22*BD22^1.852))` | =IF(AZ22>0,
        IF(BI22>0, BH22*BI22^1.852,-BH22*ABS(BI22)^1.852),
        IF(BI22>0, BH22*BD22^1.852, -BH22*BD22^1.852)) |
| Ligne 22 | Col 63 | BK22 | `=1.852*BH22*ABS(BI22)^(1.852-1)` | =1.852*BH22*ABS(BI22)^(1.852-1) |
| Ligne 22 | Col 64 | BL22 | `=BI22+$BD$75` | =BI22+$BD$75 |
| Ligne 22 | Col 68 | BP22 | `=IFERROR(MATCH(BS22,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS22,$BC$22:$BC$73,0),0) |
| Ligne 22 | Col 70 | BR22 | `=DIST_PHASE_1_v2!BF11` | =DIST_PHASE_1_v2!BF11 |
| Ligne 22 | Col 71 | BS22 | `=DIST_PHASE_1_v2!BG11` | =DIST_PHASE_1_v2!BG11 |
| Ligne 22 | Col 72 | BT22 | `=DIST_PHASE_1_v2!BI11` | =DIST_PHASE_1_v2!BI11 |
| Ligne 22 | Col 73 | BU22 | `=DIST_PHASE_1_v2!BN11` | =DIST_PHASE_1_v2!BN11 |
| Ligne 22 | Col 74 | BV22 | `=DIST_PHASE_1_v2!BO11` | =DIST_PHASE_1_v2!BO11 |
| Ligne 22 | Col 75 | BW22 | `=DIST_PHASE_1_v2!BP11` | =DIST_PHASE_1_v2!BP11 |
| Ligne 22 | Col 76 | BX22 | `= (10.679 * BW22) / ((BU22/1000)^4.871 * BV22^1.852)` | = (10.679 * BW22) / ((BU22/1000)^4.871 * BV22^1.852) |
| Ligne 22 | Col 77 | BY22 | `=IF(BR22="positif",BT22,IF(BR22="negatif",-BT22,""))` | =IF(BR22="positif",BT22,IF(BR22="negatif",-BT22,"")) |
| Ligne 22 | Col 78 | BZ22 | `=IF(BP22>0,
        IF(BY22>0, BX22*BY22^1.852,-BX22*ABS(BY22)^1.852),
        IF(BY22>0, BX22*BT22^1.852, -BX22*BT22^1.852))` | =IF(BP22>0,
        IF(BY22>0, BX22*BY22^1.852,-BX22*ABS(BY22)^1.852),
        IF(BY22>0, BX22*BT22^1.852, -BX22*BT22^1.852)) |
| Ligne 22 | Col 79 | CA22 | `=1.852*BX22*ABS(BY22)^(1.852-1)` | =1.852*BX22*ABS(BY22)^(1.852-1) |
| Ligne 22 | Col 80 | CB22 | `=BY22+$BT$64` | =BY22+$BT$64 |
| Ligne 22 | Col 84 | CF22 | `=IFERROR(MATCH(CI22,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI22,$BS$22:$BS$62,0),0) |
| Ligne 22 | Col 86 | CH22 | `=DIST_PHASE_1_v2!BS11` | =DIST_PHASE_1_v2!BS11 |
| Ligne 22 | Col 87 | CI22 | `=DIST_PHASE_1_v2!BT11` | =DIST_PHASE_1_v2!BT11 |
| Ligne 22 | Col 88 | CJ22 | `=DIST_PHASE_1_v2!BV11` | =DIST_PHASE_1_v2!BV11 |
| Ligne 22 | Col 89 | CK22 | `=DIST_PHASE_1_v2!CA11` | =DIST_PHASE_1_v2!CA11 |
| Ligne 22 | Col 91 | CM22 | `=DIST_PHASE_1_v2!CC11` | =DIST_PHASE_1_v2!CC11 |
| Ligne 22 | Col 92 | CN22 | `= (10.679 * CM22) / ((CK22/1000)^4.871 * CL22^1.852)` | = (10.679 * CM22) / ((CK22/1000)^4.871 * CL22^1.852) |
| Ligne 22 | Col 93 | CO22 | `=IF(CH22="positif",CJ22,IF(CH22="negatif",-CJ22,""))` | =IF(CH22="positif",CJ22,IF(CH22="negatif",-CJ22,"")) |
| Ligne 22 | Col 94 | CP22 | `=IF(CF22>0,
        IF(CO22>0, CN22*CO22^1.852,-CN22*ABS(CO22)^1.852),
        IF(CO22>0, CN22*CJ22^1.852, -CN22*CJ22^1.852))` | =IF(CF22>0,
        IF(CO22>0, CN22*CO22^1.852,-CN22*ABS(CO22)^1.852),
        IF(CO22>0, CN22*CJ22^1.852, -CN22*CJ22^1.852)) |
| Ligne 22 | Col 95 | CQ22 | `=1.852*CN22*ABS(CO22)^(1.852-1)` | =1.852*CN22*ABS(CO22)^(1.852-1) |
| Ligne 22 | Col 96 | CR22 | `=CO22+$CJ$71` | =CO22+$CJ$71 |
| Ligne 22 | Col 100 | CV22 | `=IFERROR(MATCH(CY22,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY22,$CI$22:$CI$69,0),0) |
| Ligne 22 | Col 102 | CX22 | `=DIST_PHASE_1_v2!CF11` | =DIST_PHASE_1_v2!CF11 |
| Ligne 22 | Col 103 | CY22 | `=DIST_PHASE_1_v2!CG11` | =DIST_PHASE_1_v2!CG11 |
| Ligne 22 | Col 104 | CZ22 | `=DIST_PHASE_1_v2!CI11` | =DIST_PHASE_1_v2!CI11 |
| Ligne 22 | Col 105 | DA22 | `=DIST_PHASE_1_v2!CN11` | =DIST_PHASE_1_v2!CN11 |
| Ligne 22 | Col 106 | DB22 | `=DIST_PHASE_1_v2!CO11` | =DIST_PHASE_1_v2!CO11 |
| Ligne 22 | Col 107 | DC22 | `=DIST_PHASE_1_v2!CP11` | =DIST_PHASE_1_v2!CP11 |
| Ligne 22 | Col 108 | DD22 | `= (10.679 * DC22) / ((DA22/1000)^4.871 * DB22^1.852)` | = (10.679 * DC22) / ((DA22/1000)^4.871 * DB22^1.852) |
| Ligne 22 | Col 109 | DE22 | `=IF(CX22="positif",CZ22,IF(CX22="negatif",-CZ22,""))` | =IF(CX22="positif",CZ22,IF(CX22="negatif",-CZ22,"")) |
| Ligne 22 | Col 110 | DF22 | `=IF(CV22>0,
        IF(DE22>0, DD22*DE22^1.852,-DD22*ABS(DE22)^1.852),
        IF(DE22>0, DD22*CZ22^1.852, -DD22*CZ22^1.852))` | =IF(CV22>0,
        IF(DE22>0, DD22*DE22^1.852,-DD22*ABS(DE22)^1.852),
        IF(DE22>0, DD22*CZ22^1.852, -DD22*CZ22^1.852)) |
| Ligne 22 | Col 111 | DG22 | `=1.852*DD22*ABS(DE22)^(1.852-1)` | =1.852*DD22*ABS(DE22)^(1.852-1) |
| Ligne 22 | Col 112 | DH22 | `=DE22+CZ56` | =DE22+CZ56 |
| Ligne 23 | Col 4 | D23 | `=DIST_PHASE_1_v2!E12` | =DIST_PHASE_1_v2!E12 |
| Ligne 23 | Col 5 | E23 | `=DIST_PHASE_1_v2!G12` | =DIST_PHASE_1_v2!G12 |
| Ligne 23 | Col 6 | F23 | `=DIST_PHASE_1_v2!L12` | =DIST_PHASE_1_v2!L12 |
| Ligne 23 | Col 7 | G23 | `=DIST_PHASE_1_v2!M12` | =DIST_PHASE_1_v2!M12 |
| Ligne 23 | Col 8 | H23 | `=DIST_PHASE_1_v2!N12` | =DIST_PHASE_1_v2!N12 |
| Ligne 23 | Col 9 | I23 | `= (10.679 * H23) / ((F23/1000)^4.871 * G23^1.852)` | = (10.679 * H23) / ((F23/1000)^4.871 * G23^1.852) |
| Ligne 23 | Col 10 | J23 | `=IF(C23="positif",E23,IF(C23="negatif",-E23,""))` | =IF(C23="positif",E23,IF(C23="negatif",-E23,"")) |
| Ligne 23 | Col 11 | K23 | `=IF(J23>0,I23*E23^1.852,-I23*E23^1.852)` | =IF(J23>0,I23*E23^1.852,-I23*E23^1.852) |
| Ligne 23 | Col 12 | L23 | `=1.852*I23*ABS(E23)^(1.852-1)` | =1.852*I23*ABS(E23)^(1.852-1) |
| Ligne 23 | Col 13 | M23 | `=J23+$D$93` | =J23+$D$93 |
| Ligne 23 | Col 16 | P23 | `=IFERROR(MATCH(S23,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S23,$D$22:$D$91,0),0) |
| Ligne 23 | Col 18 | R23 | `=DIST_PHASE_1_v2!Q12` | =DIST_PHASE_1_v2!Q12 |
| Ligne 23 | Col 19 | S23 | `=DIST_PHASE_1_v2!R12` | =DIST_PHASE_1_v2!R12 |
| Ligne 23 | Col 20 | T23 | `=DIST_PHASE_1_v2!T12` | =DIST_PHASE_1_v2!T12 |
| Ligne 23 | Col 21 | U23 | `=DIST_PHASE_1_v2!Y12` | =DIST_PHASE_1_v2!Y12 |
| Ligne 23 | Col 23 | W23 | `=DIST_PHASE_1_v2!AA12` | =DIST_PHASE_1_v2!AA12 |
| Ligne 23 | Col 24 | X23 | `= (10.679 * W23) / ((U23/1000)^4.871 * V23^1.852)` | = (10.679 * W23) / ((U23/1000)^4.871 * V23^1.852) |
| Ligne 23 | Col 25 | Y23 | `=IF(R23="positif",T23,IF(R23="negatif",-T23,""))` | =IF(R23="positif",T23,IF(R23="negatif",-T23,"")) |
| Ligne 23 | Col 26 | Z23 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD828BF0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD828BF0> |
| Ligne 23 | Col 27 | AA23 | `=IF(P23>0,
        IF(R23="positif",1,-1),
        0)` | =IF(P23>0,
        IF(R23="positif",1,-1),
        0) |
| Ligne 23 | Col 28 | AB23 | `=X23*SIGN(Y23)*ABS(Y23)^1.852` | =X23*SIGN(Y23)*ABS(Y23)^1.852 |
| Ligne 23 | Col 29 | AC23 | `=1.852*X23*ABS(Y23)^(1.852-1)` | =1.852*X23*ABS(Y23)^(1.852-1) |
| Ligne 23 | Col 30 | AD23 | `=IF(P23>0,
Y23+($D$93*Z23)+(AA23*$S$93),
Y23+$S$93)` | =IF(P23>0,
Y23+($D$93*Z23)+(AA23*$S$93),
Y23+$S$93) |
| Ligne 23 | Col 32 | AF23 | `=ABS(AD23)-ABS(Y23)` | =ABS(AD23)-ABS(Y23) |
| Ligne 23 | Col 36 | AJ23 | `=IFERROR(MATCH(AM23,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM23,$S$22:$S$91,0),0) |
| Ligne 23 | Col 38 | AL23 | `=TRONCONS_V2!AI10` | =TRONCONS_V2!AI10 |
| Ligne 23 | Col 39 | AM23 | `=TRONCONS_V2!AE10` | =TRONCONS_V2!AE10 |
| Ligne 23 | Col 40 | AN23 | `=DIST_PHASE_1_v2!AG12` | =DIST_PHASE_1_v2!AG12 |
| Ligne 23 | Col 41 | AO23 | `=DIST_PHASE_1_v2!AL12` | =DIST_PHASE_1_v2!AL12 |
| Ligne 23 | Col 43 | AQ23 | `=TRONCONS_V2!AG10` | =TRONCONS_V2!AG10 |
| Ligne 23 | Col 44 | AR23 | `= (10.679 * AQ23) / ((AO23/1000)^4.871 * AP23^1.852)` | = (10.679 * AQ23) / ((AO23/1000)^4.871 * AP23^1.852) |
| Ligne 23 | Col 45 | AS23 | `=IF(AL23="positif",AN23,IF(AL23="negatif",-AN23,""))` | =IF(AL23="positif",AN23,IF(AL23="negatif",-AN23,"")) |
| Ligne 23 | Col 46 | AT23 | `=IF(AJ23>0,
        IF(AS23>0, AR23*AS23^1.852,-AR23*ABS(AS23)^1.852),
        IF(AS23>0, AR23*AN23^1.852, -AR23*AN23^1.852))` | =IF(AJ23>0,
        IF(AS23>0, AR23*AS23^1.852,-AR23*ABS(AS23)^1.852),
        IF(AS23>0, AR23*AN23^1.852, -AR23*AN23^1.852)) |
| Ligne 23 | Col 47 | AU23 | `=1.852*AR23*ABS(AS23)^(1.852-1)` | =1.852*AR23*ABS(AS23)^(1.852-1) |
| Ligne 23 | Col 48 | AV23 | `=AS23+$AN$60` | =AS23+$AN$60 |
| Ligne 23 | Col 52 | AZ23 | `=IFERROR(MATCH(BC23,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC23,$AM$22:$AM$57,0),0) |
| Ligne 23 | Col 54 | BB23 | `=DIST_PHASE_1_v2!AQ12` | =DIST_PHASE_1_v2!AQ12 |
| Ligne 23 | Col 55 | BC23 | `=DIST_PHASE_1_v2!AR12` | =DIST_PHASE_1_v2!AR12 |
| Ligne 23 | Col 56 | BD23 | `=DIST_PHASE_1_v2!AT12` | =DIST_PHASE_1_v2!AT12 |
| Ligne 23 | Col 57 | BE23 | `=DIST_PHASE_1_v2!AY12` | =DIST_PHASE_1_v2!AY12 |
| Ligne 23 | Col 58 | BF23 | `=DIST_PHASE_1_v2!AZ12` | =DIST_PHASE_1_v2!AZ12 |
| Ligne 23 | Col 59 | BG23 | `=DIST_PHASE_1_v2!BA12` | =DIST_PHASE_1_v2!BA12 |
| Ligne 23 | Col 60 | BH23 | `= (10.679 * BG23) / ((BE23/1000)^4.871 * BF23^1.852)` | = (10.679 * BG23) / ((BE23/1000)^4.871 * BF23^1.852) |
| Ligne 23 | Col 61 | BI23 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82A6F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82A6F0> |
| Ligne 23 | Col 62 | BJ23 | `=IF(AZ23>0,
        IF(BI23>0, BH23*BI23^1.852,-BH23*ABS(BI23)^1.852),
        IF(BI23>0, BH23*BD23^1.852, -BH23*BD23^1.852))` | =IF(AZ23>0,
        IF(BI23>0, BH23*BI23^1.852,-BH23*ABS(BI23)^1.852),
        IF(BI23>0, BH23*BD23^1.852, -BH23*BD23^1.852)) |
| Ligne 23 | Col 63 | BK23 | `=1.852*BH23*ABS(BI23)^(1.852-1)` | =1.852*BH23*ABS(BI23)^(1.852-1) |
| Ligne 23 | Col 64 | BL23 | `=BI23+$BD$75` | =BI23+$BD$75 |
| Ligne 23 | Col 68 | BP23 | `=IFERROR(MATCH(BS23,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS23,$BC$22:$BC$73,0),0) |
| Ligne 23 | Col 70 | BR23 | `=DIST_PHASE_1_v2!BF12` | =DIST_PHASE_1_v2!BF12 |
| Ligne 23 | Col 71 | BS23 | `=DIST_PHASE_1_v2!BG12` | =DIST_PHASE_1_v2!BG12 |
| Ligne 23 | Col 72 | BT23 | `=DIST_PHASE_1_v2!BI12` | =DIST_PHASE_1_v2!BI12 |
| Ligne 23 | Col 73 | BU23 | `=DIST_PHASE_1_v2!BN12` | =DIST_PHASE_1_v2!BN12 |
| Ligne 23 | Col 74 | BV23 | `=DIST_PHASE_1_v2!BO12` | =DIST_PHASE_1_v2!BO12 |
| Ligne 23 | Col 75 | BW23 | `=DIST_PHASE_1_v2!BP12` | =DIST_PHASE_1_v2!BP12 |
| Ligne 23 | Col 76 | BX23 | `= (10.679 * BW23) / ((BU23/1000)^4.871 * BV23^1.852)` | = (10.679 * BW23) / ((BU23/1000)^4.871 * BV23^1.852) |
| Ligne 23 | Col 77 | BY23 | `=IF(BR23="positif",BT23,IF(BR23="negatif",-BT23,""))` | =IF(BR23="positif",BT23,IF(BR23="negatif",-BT23,"")) |
| Ligne 23 | Col 78 | BZ23 | `=IF(BP23>0,
        IF(BY23>0, BX23*BY23^1.852,-BX23*ABS(BY23)^1.852),
        IF(BY23>0, BX23*BT23^1.852, -BX23*BT23^1.852))` | =IF(BP23>0,
        IF(BY23>0, BX23*BY23^1.852,-BX23*ABS(BY23)^1.852),
        IF(BY23>0, BX23*BT23^1.852, -BX23*BT23^1.852)) |
| Ligne 23 | Col 79 | CA23 | `=1.852*BX23*ABS(BY23)^(1.852-1)` | =1.852*BX23*ABS(BY23)^(1.852-1) |
| Ligne 23 | Col 80 | CB23 | `=BY23+$BT$64` | =BY23+$BT$64 |
| Ligne 23 | Col 84 | CF23 | `=IFERROR(MATCH(CI23,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI23,$BS$22:$BS$62,0),0) |
| Ligne 23 | Col 86 | CH23 | `=DIST_PHASE_1_v2!BS12` | =DIST_PHASE_1_v2!BS12 |
| Ligne 23 | Col 87 | CI23 | `=DIST_PHASE_1_v2!BT12` | =DIST_PHASE_1_v2!BT12 |
| Ligne 23 | Col 88 | CJ23 | `=DIST_PHASE_1_v2!BV12` | =DIST_PHASE_1_v2!BV12 |
| Ligne 23 | Col 89 | CK23 | `=DIST_PHASE_1_v2!CA12` | =DIST_PHASE_1_v2!CA12 |
| Ligne 23 | Col 91 | CM23 | `=DIST_PHASE_1_v2!CC12` | =DIST_PHASE_1_v2!CC12 |
| Ligne 23 | Col 92 | CN23 | `= (10.679 * CM23) / ((CK23/1000)^4.871 * CL23^1.852)` | = (10.679 * CM23) / ((CK23/1000)^4.871 * CL23^1.852) |
| Ligne 23 | Col 93 | CO23 | `=IF(CH23="positif",CJ23,IF(CH23="negatif",-CJ23,""))` | =IF(CH23="positif",CJ23,IF(CH23="negatif",-CJ23,"")) |
| Ligne 23 | Col 94 | CP23 | `=IF(CF23>0,
        IF(CO23>0, CN23*CO23^1.852,-CN23*ABS(CO23)^1.852),
        IF(CO23>0, CN23*CJ23^1.852, -CN23*CJ23^1.852))` | =IF(CF23>0,
        IF(CO23>0, CN23*CO23^1.852,-CN23*ABS(CO23)^1.852),
        IF(CO23>0, CN23*CJ23^1.852, -CN23*CJ23^1.852)) |
| Ligne 23 | Col 95 | CQ23 | `=1.852*CN23*ABS(CO23)^(1.852-1)` | =1.852*CN23*ABS(CO23)^(1.852-1) |
| Ligne 23 | Col 96 | CR23 | `=CO23+$CJ$71` | =CO23+$CJ$71 |
| Ligne 23 | Col 100 | CV23 | `=IFERROR(MATCH(CY23,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY23,$CI$22:$CI$69,0),0) |
| Ligne 23 | Col 102 | CX23 | `=DIST_PHASE_1_v2!CF12` | =DIST_PHASE_1_v2!CF12 |
| Ligne 23 | Col 103 | CY23 | `=DIST_PHASE_1_v2!CG12` | =DIST_PHASE_1_v2!CG12 |
| Ligne 23 | Col 104 | CZ23 | `=DIST_PHASE_1_v2!CI12` | =DIST_PHASE_1_v2!CI12 |
| Ligne 23 | Col 105 | DA23 | `=DIST_PHASE_1_v2!CN12` | =DIST_PHASE_1_v2!CN12 |
| Ligne 23 | Col 106 | DB23 | `=DIST_PHASE_1_v2!CO12` | =DIST_PHASE_1_v2!CO12 |
| Ligne 23 | Col 107 | DC23 | `=DIST_PHASE_1_v2!CP12` | =DIST_PHASE_1_v2!CP12 |
| Ligne 23 | Col 108 | DD23 | `= (10.679 * DC23) / ((DA23/1000)^4.871 * DB23^1.852)` | = (10.679 * DC23) / ((DA23/1000)^4.871 * DB23^1.852) |
| Ligne 23 | Col 109 | DE23 | `=IF(CX23="positif",CZ23,IF(CX23="negatif",-CZ23,""))` | =IF(CX23="positif",CZ23,IF(CX23="negatif",-CZ23,"")) |
| Ligne 23 | Col 110 | DF23 | `=IF(CV23>0,
        IF(DE23>0, DD23*DE23^1.852,-DD23*ABS(DE23)^1.852),
        IF(DE23>0, DD23*CZ23^1.852, -DD23*CZ23^1.852))` | =IF(CV23>0,
        IF(DE23>0, DD23*DE23^1.852,-DD23*ABS(DE23)^1.852),
        IF(DE23>0, DD23*CZ23^1.852, -DD23*CZ23^1.852)) |
| Ligne 23 | Col 111 | DG23 | `=1.852*DD23*ABS(DE23)^(1.852-1)` | =1.852*DD23*ABS(DE23)^(1.852-1) |
| Ligne 23 | Col 112 | DH23 | `=DE23+CZ57` | =DE23+CZ57 |
| Ligne 24 | Col 4 | D24 | `=DIST_PHASE_1_v2!E13` | =DIST_PHASE_1_v2!E13 |
| Ligne 24 | Col 5 | E24 | `=DIST_PHASE_1_v2!G13` | =DIST_PHASE_1_v2!G13 |
| Ligne 24 | Col 6 | F24 | `=DIST_PHASE_1_v2!L13` | =DIST_PHASE_1_v2!L13 |
| Ligne 24 | Col 7 | G24 | `=DIST_PHASE_1_v2!M13` | =DIST_PHASE_1_v2!M13 |
| Ligne 24 | Col 8 | H24 | `=DIST_PHASE_1_v2!N13` | =DIST_PHASE_1_v2!N13 |
| Ligne 24 | Col 9 | I24 | `= (10.679 * H24) / ((F24/1000)^4.871 * G24^1.852)` | = (10.679 * H24) / ((F24/1000)^4.871 * G24^1.852) |
| Ligne 24 | Col 10 | J24 | `=IF(C24="positif",E24,IF(C24="negatif",-E24,""))` | =IF(C24="positif",E24,IF(C24="negatif",-E24,"")) |
| Ligne 24 | Col 11 | K24 | `=IF(J24>0,I24*E24^1.852,-I24*E24^1.852)` | =IF(J24>0,I24*E24^1.852,-I24*E24^1.852) |
| Ligne 24 | Col 12 | L24 | `=1.852*I24*ABS(E24)^(1.852-1)` | =1.852*I24*ABS(E24)^(1.852-1) |
| Ligne 24 | Col 13 | M24 | `=J24+$D$93` | =J24+$D$93 |
| Ligne 24 | Col 16 | P24 | `=IFERROR(MATCH(S24,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S24,$D$22:$D$91,0),0) |
| Ligne 24 | Col 18 | R24 | `=DIST_PHASE_1_v2!Q13` | =DIST_PHASE_1_v2!Q13 |
| Ligne 24 | Col 19 | S24 | `=DIST_PHASE_1_v2!R13` | =DIST_PHASE_1_v2!R13 |
| Ligne 24 | Col 20 | T24 | `=DIST_PHASE_1_v2!T13` | =DIST_PHASE_1_v2!T13 |
| Ligne 24 | Col 21 | U24 | `=DIST_PHASE_1_v2!Y13` | =DIST_PHASE_1_v2!Y13 |
| Ligne 24 | Col 23 | W24 | `=DIST_PHASE_1_v2!AA13` | =DIST_PHASE_1_v2!AA13 |
| Ligne 24 | Col 24 | X24 | `= (10.679 * W24) / ((U24/1000)^4.871 * V24^1.852)` | = (10.679 * W24) / ((U24/1000)^4.871 * V24^1.852) |
| Ligne 24 | Col 25 | Y24 | `=IF(R24="positif",T24,IF(R24="negatif",-T24,""))` | =IF(R24="positif",T24,IF(R24="negatif",-T24,"")) |
| Ligne 24 | Col 26 | Z24 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8299D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8299D0> |
| Ligne 24 | Col 27 | AA24 | `=IF(P24>0,
IF(R24="positif",1,-1),
0)` | =IF(P24>0,
IF(R24="positif",1,-1),
0) |
| Ligne 24 | Col 28 | AB24 | `=X24*SIGN(Y24)*ABS(Y24)^1.852` | =X24*SIGN(Y24)*ABS(Y24)^1.852 |
| Ligne 24 | Col 29 | AC24 | `=1.852*X24*ABS(Y24)^(1.852-1)` | =1.852*X24*ABS(Y24)^(1.852-1) |
| Ligne 24 | Col 30 | AD24 | `=IF(P24>0,
Y24+($D$93*Z24)+(AA24*$S$93),
Y24+$S$93)` | =IF(P24>0,
Y24+($D$93*Z24)+(AA24*$S$93),
Y24+$S$93) |
| Ligne 24 | Col 32 | AF24 | `=ABS(AD24)-ABS(Y24)` | =ABS(AD24)-ABS(Y24) |
| Ligne 24 | Col 36 | AJ24 | `=IFERROR(MATCH(AM24,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM24,$S$22:$S$91,0),0) |
| Ligne 24 | Col 38 | AL24 | `=TRONCONS_V2!AI11` | =TRONCONS_V2!AI11 |
| Ligne 24 | Col 39 | AM24 | `=TRONCONS_V2!AE11` | =TRONCONS_V2!AE11 |
| Ligne 24 | Col 40 | AN24 | `=DIST_PHASE_1_v2!AG13` | =DIST_PHASE_1_v2!AG13 |
| Ligne 24 | Col 41 | AO24 | `=DIST_PHASE_1_v2!AL13` | =DIST_PHASE_1_v2!AL13 |
| Ligne 24 | Col 43 | AQ24 | `=TRONCONS_V2!AG11` | =TRONCONS_V2!AG11 |
| Ligne 24 | Col 44 | AR24 | `= (10.679 * AQ24) / ((AO24/1000)^4.871 * AP24^1.852)` | = (10.679 * AQ24) / ((AO24/1000)^4.871 * AP24^1.852) |
| Ligne 24 | Col 45 | AS24 | `=IF(AL24="positif",AN24,IF(AL24="negatif",-AN24,""))` | =IF(AL24="positif",AN24,IF(AL24="negatif",-AN24,"")) |
| Ligne 24 | Col 46 | AT24 | `=IF(AJ24>0,
        IF(AS24>0, AR24*AS24^1.852,-AR24*ABS(AS24)^1.852),
        IF(AS24>0, AR24*AN24^1.852, -AR24*AN24^1.852))` | =IF(AJ24>0,
        IF(AS24>0, AR24*AS24^1.852,-AR24*ABS(AS24)^1.852),
        IF(AS24>0, AR24*AN24^1.852, -AR24*AN24^1.852)) |
| Ligne 24 | Col 47 | AU24 | `=1.852*AR24*ABS(AS24)^(1.852-1)` | =1.852*AR24*ABS(AS24)^(1.852-1) |
| Ligne 24 | Col 48 | AV24 | `=AS24+$AN$60` | =AS24+$AN$60 |
| Ligne 24 | Col 52 | AZ24 | `=IFERROR(MATCH(BC24,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC24,$AM$22:$AM$57,0),0) |
| Ligne 24 | Col 54 | BB24 | `=DIST_PHASE_1_v2!AQ13` | =DIST_PHASE_1_v2!AQ13 |
| Ligne 24 | Col 55 | BC24 | `=DIST_PHASE_1_v2!AR13` | =DIST_PHASE_1_v2!AR13 |
| Ligne 24 | Col 56 | BD24 | `=DIST_PHASE_1_v2!AT13` | =DIST_PHASE_1_v2!AT13 |
| Ligne 24 | Col 57 | BE24 | `=DIST_PHASE_1_v2!AY13` | =DIST_PHASE_1_v2!AY13 |
| Ligne 24 | Col 58 | BF24 | `=DIST_PHASE_1_v2!AZ13` | =DIST_PHASE_1_v2!AZ13 |
| Ligne 24 | Col 59 | BG24 | `=DIST_PHASE_1_v2!BA13` | =DIST_PHASE_1_v2!BA13 |
| Ligne 24 | Col 60 | BH24 | `= (10.679 * BG24) / ((BE24/1000)^4.871 * BF24^1.852)` | = (10.679 * BG24) / ((BE24/1000)^4.871 * BF24^1.852) |
| Ligne 24 | Col 61 | BI24 | `=IF(BB24="positif",BD24,IF(BB24="negatif",-BD24,""))` | =IF(BB24="positif",BD24,IF(BB24="negatif",-BD24,"")) |
| Ligne 24 | Col 62 | BJ24 | `=IF(AZ24>0,
        IF(BI24>0, BH24*BI24^1.852,-BH24*ABS(BI24)^1.852),
        IF(BI24>0, BH24*BD24^1.852, -BH24*BD24^1.852))` | =IF(AZ24>0,
        IF(BI24>0, BH24*BI24^1.852,-BH24*ABS(BI24)^1.852),
        IF(BI24>0, BH24*BD24^1.852, -BH24*BD24^1.852)) |
| Ligne 24 | Col 63 | BK24 | `=1.852*BH24*ABS(BI24)^(1.852-1)` | =1.852*BH24*ABS(BI24)^(1.852-1) |
| Ligne 24 | Col 64 | BL24 | `=BI24+$BD$75` | =BI24+$BD$75 |
| Ligne 24 | Col 68 | BP24 | `=IFERROR(MATCH(BS24,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS24,$BC$22:$BC$73,0),0) |
| Ligne 24 | Col 70 | BR24 | `=DIST_PHASE_1_v2!BF13` | =DIST_PHASE_1_v2!BF13 |
| Ligne 24 | Col 71 | BS24 | `=DIST_PHASE_1_v2!BG13` | =DIST_PHASE_1_v2!BG13 |
| Ligne 24 | Col 72 | BT24 | `=DIST_PHASE_1_v2!BI13` | =DIST_PHASE_1_v2!BI13 |
| Ligne 24 | Col 73 | BU24 | `=DIST_PHASE_1_v2!BN13` | =DIST_PHASE_1_v2!BN13 |
| Ligne 24 | Col 74 | BV24 | `=DIST_PHASE_1_v2!BO13` | =DIST_PHASE_1_v2!BO13 |
| Ligne 24 | Col 75 | BW24 | `=DIST_PHASE_1_v2!BP13` | =DIST_PHASE_1_v2!BP13 |
| Ligne 24 | Col 76 | BX24 | `= (10.679 * BW24) / ((BU24/1000)^4.871 * BV24^1.852)` | = (10.679 * BW24) / ((BU24/1000)^4.871 * BV24^1.852) |
| Ligne 24 | Col 77 | BY24 | `=IF(BR24="positif",BT24,IF(BR24="negatif",-BT24,""))` | =IF(BR24="positif",BT24,IF(BR24="negatif",-BT24,"")) |
| Ligne 24 | Col 78 | BZ24 | `=IF(BP24>0,
IF(BY24>0, BX24*BY24^1.852,-BX24*ABS(BY24)^1.852),
IF(BY24>0, BX24*BT24^1.852, -BX24*BT24^1.852))` | =IF(BP24>0,
IF(BY24>0, BX24*BY24^1.852,-BX24*ABS(BY24)^1.852),
IF(BY24>0, BX24*BT24^1.852, -BX24*BT24^1.852)) |
| Ligne 24 | Col 79 | CA24 | `=1.852*BX24*ABS(BY24)^(1.852-1)` | =1.852*BX24*ABS(BY24)^(1.852-1) |
| Ligne 24 | Col 80 | CB24 | `=BY24+$BT$64` | =BY24+$BT$64 |
| Ligne 24 | Col 84 | CF24 | `=IFERROR(MATCH(CI24,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI24,$BS$22:$BS$62,0),0) |
| Ligne 24 | Col 86 | CH24 | `=DIST_PHASE_1_v2!BS13` | =DIST_PHASE_1_v2!BS13 |
| Ligne 24 | Col 87 | CI24 | `=DIST_PHASE_1_v2!BT13` | =DIST_PHASE_1_v2!BT13 |
| Ligne 24 | Col 88 | CJ24 | `=DIST_PHASE_1_v2!BV13` | =DIST_PHASE_1_v2!BV13 |
| Ligne 24 | Col 89 | CK24 | `=DIST_PHASE_1_v2!CA13` | =DIST_PHASE_1_v2!CA13 |
| Ligne 24 | Col 91 | CM24 | `=DIST_PHASE_1_v2!CC13` | =DIST_PHASE_1_v2!CC13 |
| Ligne 24 | Col 92 | CN24 | `= (10.679 * CM24) / ((CK24/1000)^4.871 * CL24^1.852)` | = (10.679 * CM24) / ((CK24/1000)^4.871 * CL24^1.852) |
| Ligne 24 | Col 93 | CO24 | `=IF(CH24="positif",CJ24,IF(CH24="negatif",-CJ24,""))` | =IF(CH24="positif",CJ24,IF(CH24="negatif",-CJ24,"")) |
| Ligne 24 | Col 94 | CP24 | `=IF(CF24>0,
IF(CO24>0, CN24*CO24^1.852,-CN24*ABS(CO24)^1.852),
IF(CO24>0, CN24*CJ24^1.852, -CN24*CJ24^1.852))` | =IF(CF24>0,
IF(CO24>0, CN24*CO24^1.852,-CN24*ABS(CO24)^1.852),
IF(CO24>0, CN24*CJ24^1.852, -CN24*CJ24^1.852)) |
| Ligne 24 | Col 95 | CQ24 | `=1.852*CN24*ABS(CO24)^(1.852-1)` | =1.852*CN24*ABS(CO24)^(1.852-1) |
| Ligne 24 | Col 96 | CR24 | `=CO24+$CJ$71` | =CO24+$CJ$71 |
| Ligne 24 | Col 100 | CV24 | `=IFERROR(MATCH(CY24,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY24,$CI$22:$CI$69,0),0) |
| Ligne 24 | Col 102 | CX24 | `=DIST_PHASE_1_v2!CF13` | =DIST_PHASE_1_v2!CF13 |
| Ligne 24 | Col 103 | CY24 | `=DIST_PHASE_1_v2!CG13` | =DIST_PHASE_1_v2!CG13 |
| Ligne 24 | Col 104 | CZ24 | `=DIST_PHASE_1_v2!CI13` | =DIST_PHASE_1_v2!CI13 |
| Ligne 24 | Col 105 | DA24 | `=DIST_PHASE_1_v2!CN13` | =DIST_PHASE_1_v2!CN13 |
| Ligne 24 | Col 106 | DB24 | `=DIST_PHASE_1_v2!CO13` | =DIST_PHASE_1_v2!CO13 |
| Ligne 24 | Col 107 | DC24 | `=DIST_PHASE_1_v2!CP13` | =DIST_PHASE_1_v2!CP13 |
| Ligne 24 | Col 108 | DD24 | `= (10.679 * DC24) / ((DA24/1000)^4.871 * DB24^1.852)` | = (10.679 * DC24) / ((DA24/1000)^4.871 * DB24^1.852) |
| Ligne 24 | Col 109 | DE24 | `=IF(CX24="positif",CZ24,IF(CX24="negatif",-CZ24,""))` | =IF(CX24="positif",CZ24,IF(CX24="negatif",-CZ24,"")) |
| Ligne 24 | Col 110 | DF24 | `=IF(CV24>0,
IF(DE24>0, DD24*DE24^1.852,-DD24*ABS(DE24)^1.852),
IF(DE24>0, DD24*CZ24^1.852, -DD24*CZ24^1.852))` | =IF(CV24>0,
IF(DE24>0, DD24*DE24^1.852,-DD24*ABS(DE24)^1.852),
IF(DE24>0, DD24*CZ24^1.852, -DD24*CZ24^1.852)) |
| Ligne 24 | Col 111 | DG24 | `=1.852*DD24*ABS(DE24)^(1.852-1)` | =1.852*DD24*ABS(DE24)^(1.852-1) |
| Ligne 24 | Col 112 | DH24 | `=DE24+CZ58` | =DE24+CZ58 |
| Ligne 25 | Col 4 | D25 | `=DIST_PHASE_1_v2!E14` | =DIST_PHASE_1_v2!E14 |
| Ligne 25 | Col 5 | E25 | `=DIST_PHASE_1_v2!G14` | =DIST_PHASE_1_v2!G14 |
| Ligne 25 | Col 6 | F25 | `=DIST_PHASE_1_v2!L14` | =DIST_PHASE_1_v2!L14 |
| Ligne 25 | Col 7 | G25 | `=DIST_PHASE_1_v2!M14` | =DIST_PHASE_1_v2!M14 |
| Ligne 25 | Col 8 | H25 | `=DIST_PHASE_1_v2!N14` | =DIST_PHASE_1_v2!N14 |
| Ligne 25 | Col 9 | I25 | `= (10.679 * H25) / ((F25/1000)^4.871 * G25^1.852)` | = (10.679 * H25) / ((F25/1000)^4.871 * G25^1.852) |
| Ligne 25 | Col 10 | J25 | `=IF(C25="positif",E25,IF(C25="negatif",-E25,""))` | =IF(C25="positif",E25,IF(C25="negatif",-E25,"")) |
| Ligne 25 | Col 11 | K25 | `=IF(J25>0,I25*E25^1.852,-I25*E25^1.852)` | =IF(J25>0,I25*E25^1.852,-I25*E25^1.852) |
| Ligne 25 | Col 12 | L25 | `=1.852*I25*ABS(E25)^(1.852-1)` | =1.852*I25*ABS(E25)^(1.852-1) |
| Ligne 25 | Col 13 | M25 | `=J25+$D$93` | =J25+$D$93 |
| Ligne 25 | Col 16 | P25 | `=IFERROR(MATCH(S25,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S25,$D$22:$D$91,0),0) |
| Ligne 25 | Col 18 | R25 | `=DIST_PHASE_1_v2!Q14` | =DIST_PHASE_1_v2!Q14 |
| Ligne 25 | Col 19 | S25 | `=DIST_PHASE_1_v2!R14` | =DIST_PHASE_1_v2!R14 |
| Ligne 25 | Col 20 | T25 | `=DIST_PHASE_1_v2!T14` | =DIST_PHASE_1_v2!T14 |
| Ligne 25 | Col 21 | U25 | `=DIST_PHASE_1_v2!Y14` | =DIST_PHASE_1_v2!Y14 |
| Ligne 25 | Col 23 | W25 | `=DIST_PHASE_1_v2!AA14` | =DIST_PHASE_1_v2!AA14 |
| Ligne 25 | Col 24 | X25 | `= (10.679 * W25) / ((U25/1000)^4.871 * V25^1.852)` | = (10.679 * W25) / ((U25/1000)^4.871 * V25^1.852) |
| Ligne 25 | Col 25 | Y25 | `=IF(R25="positif",T25,IF(R25="negatif",-T25,""))` | =IF(R25="positif",T25,IF(R25="negatif",-T25,"")) |
| Ligne 25 | Col 26 | Z25 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD829910>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD829910> |
| Ligne 25 | Col 27 | AA25 | `=IF(P25>0,
IF(R25="positif",1,-1),
0)` | =IF(P25>0,
IF(R25="positif",1,-1),
0) |
| Ligne 25 | Col 28 | AB25 | `=X25*SIGN(Y25)*ABS(Y25)^1.852` | =X25*SIGN(Y25)*ABS(Y25)^1.852 |
| Ligne 25 | Col 29 | AC25 | `=1.852*X25*ABS(Y25)^(1.852-1)` | =1.852*X25*ABS(Y25)^(1.852-1) |
| Ligne 25 | Col 30 | AD25 | `=IF(P25>0,
Y25+($D$93*Z25)+(AA25*$S$93),
Y25+$S$93)` | =IF(P25>0,
Y25+($D$93*Z25)+(AA25*$S$93),
Y25+$S$93) |
| Ligne 25 | Col 32 | AF25 | `=ABS(AD25)-ABS(Y25)` | =ABS(AD25)-ABS(Y25) |
| Ligne 25 | Col 36 | AJ25 | `=IFERROR(MATCH(AM25,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM25,$S$22:$S$91,0),0) |
| Ligne 25 | Col 38 | AL25 | `=TRONCONS_V2!AI12` | =TRONCONS_V2!AI12 |
| Ligne 25 | Col 39 | AM25 | `=TRONCONS_V2!AE12` | =TRONCONS_V2!AE12 |
| Ligne 25 | Col 40 | AN25 | `=DIST_PHASE_1_v2!AG14` | =DIST_PHASE_1_v2!AG14 |
| Ligne 25 | Col 41 | AO25 | `=DIST_PHASE_1_v2!AL14` | =DIST_PHASE_1_v2!AL14 |
| Ligne 25 | Col 43 | AQ25 | `=TRONCONS_V2!AG12` | =TRONCONS_V2!AG12 |
| Ligne 25 | Col 44 | AR25 | `= (10.679 * AQ25) / ((AO25/1000)^4.871 * AP25^1.852)` | = (10.679 * AQ25) / ((AO25/1000)^4.871 * AP25^1.852) |
| Ligne 25 | Col 45 | AS25 | `=IF(AL25="positif",AN25,IF(AL25="negatif",-AN25,""))` | =IF(AL25="positif",AN25,IF(AL25="negatif",-AN25,"")) |
| Ligne 25 | Col 46 | AT25 | `=IF(AJ25>0,
        IF(AS25>0, AR25*AS25^1.852,-AR25*ABS(AS25)^1.852),
        IF(AS25>0, AR25*AN25^1.852, -AR25*AN25^1.852))` | =IF(AJ25>0,
        IF(AS25>0, AR25*AS25^1.852,-AR25*ABS(AS25)^1.852),
        IF(AS25>0, AR25*AN25^1.852, -AR25*AN25^1.852)) |
| Ligne 25 | Col 47 | AU25 | `=1.852*AR25*ABS(AS25)^(1.852-1)` | =1.852*AR25*ABS(AS25)^(1.852-1) |
| Ligne 25 | Col 48 | AV25 | `=AS25+$AN$60` | =AS25+$AN$60 |
| Ligne 25 | Col 52 | AZ25 | `=IFERROR(MATCH(BC25,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC25,$AM$22:$AM$57,0),0) |
| Ligne 25 | Col 54 | BB25 | `=DIST_PHASE_1_v2!AQ14` | =DIST_PHASE_1_v2!AQ14 |
| Ligne 25 | Col 55 | BC25 | `=DIST_PHASE_1_v2!AR14` | =DIST_PHASE_1_v2!AR14 |
| Ligne 25 | Col 56 | BD25 | `=DIST_PHASE_1_v2!AT14` | =DIST_PHASE_1_v2!AT14 |
| Ligne 25 | Col 57 | BE25 | `=DIST_PHASE_1_v2!AY14` | =DIST_PHASE_1_v2!AY14 |
| Ligne 25 | Col 58 | BF25 | `=DIST_PHASE_1_v2!AZ14` | =DIST_PHASE_1_v2!AZ14 |
| Ligne 25 | Col 59 | BG25 | `=DIST_PHASE_1_v2!BA14` | =DIST_PHASE_1_v2!BA14 |
| Ligne 25 | Col 60 | BH25 | `= (10.679 * BG25) / ((BE25/1000)^4.871 * BF25^1.852)` | = (10.679 * BG25) / ((BE25/1000)^4.871 * BF25^1.852) |
| Ligne 25 | Col 61 | BI25 | `=IF(BB25="positif",BD25,IF(BB25="negatif",-BD25,""))` | =IF(BB25="positif",BD25,IF(BB25="negatif",-BD25,"")) |
| Ligne 25 | Col 62 | BJ25 | `=IF(AZ25>0,
IF(BI25>0, BH25*BI25^1.852,-BH25*ABS(BI25)^1.852),
IF(BI25>0, BH25*BD25^1.852, -BH25*BD25^1.852))` | =IF(AZ25>0,
IF(BI25>0, BH25*BI25^1.852,-BH25*ABS(BI25)^1.852),
IF(BI25>0, BH25*BD25^1.852, -BH25*BD25^1.852)) |
| Ligne 25 | Col 63 | BK25 | `=1.852*BH25*ABS(BI25)^(1.852-1)` | =1.852*BH25*ABS(BI25)^(1.852-1) |
| Ligne 25 | Col 64 | BL25 | `=BI25+$BD$75` | =BI25+$BD$75 |
| Ligne 25 | Col 68 | BP25 | `=IFERROR(MATCH(BS25,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS25,$BC$22:$BC$73,0),0) |
| Ligne 25 | Col 70 | BR25 | `=DIST_PHASE_1_v2!BF14` | =DIST_PHASE_1_v2!BF14 |
| Ligne 25 | Col 71 | BS25 | `=DIST_PHASE_1_v2!BG14` | =DIST_PHASE_1_v2!BG14 |
| Ligne 25 | Col 72 | BT25 | `=DIST_PHASE_1_v2!BI14` | =DIST_PHASE_1_v2!BI14 |
| Ligne 25 | Col 73 | BU25 | `=DIST_PHASE_1_v2!BN14` | =DIST_PHASE_1_v2!BN14 |
| Ligne 25 | Col 74 | BV25 | `=DIST_PHASE_1_v2!BO14` | =DIST_PHASE_1_v2!BO14 |
| Ligne 25 | Col 75 | BW25 | `=DIST_PHASE_1_v2!BP14` | =DIST_PHASE_1_v2!BP14 |
| Ligne 25 | Col 76 | BX25 | `= (10.679 * BW25) / ((BU25/1000)^4.871 * BV25^1.852)` | = (10.679 * BW25) / ((BU25/1000)^4.871 * BV25^1.852) |
| Ligne 25 | Col 77 | BY25 | `=IF(BR25="positif",BT25,IF(BR25="negatif",-BT25,""))` | =IF(BR25="positif",BT25,IF(BR25="negatif",-BT25,"")) |
| Ligne 25 | Col 78 | BZ25 | `=IF(BP25>0,
IF(BY25>0, BX25*BY25^1.852,-BX25*ABS(BY25)^1.852),
IF(BY25>0, BX25*BT25^1.852, -BX25*BT25^1.852))` | =IF(BP25>0,
IF(BY25>0, BX25*BY25^1.852,-BX25*ABS(BY25)^1.852),
IF(BY25>0, BX25*BT25^1.852, -BX25*BT25^1.852)) |
| Ligne 25 | Col 79 | CA25 | `=1.852*BX25*ABS(BY25)^(1.852-1)` | =1.852*BX25*ABS(BY25)^(1.852-1) |
| Ligne 25 | Col 80 | CB25 | `=BY25+$BT$64` | =BY25+$BT$64 |
| Ligne 25 | Col 84 | CF25 | `=IFERROR(MATCH(CI25,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI25,$BS$22:$BS$62,0),0) |
| Ligne 25 | Col 86 | CH25 | `=DIST_PHASE_1_v2!BS14` | =DIST_PHASE_1_v2!BS14 |
| Ligne 25 | Col 87 | CI25 | `=DIST_PHASE_1_v2!BT14` | =DIST_PHASE_1_v2!BT14 |
| Ligne 25 | Col 88 | CJ25 | `=DIST_PHASE_1_v2!BV14` | =DIST_PHASE_1_v2!BV14 |
| Ligne 25 | Col 89 | CK25 | `=DIST_PHASE_1_v2!CA14` | =DIST_PHASE_1_v2!CA14 |
| Ligne 25 | Col 91 | CM25 | `=DIST_PHASE_1_v2!CC14` | =DIST_PHASE_1_v2!CC14 |
| Ligne 25 | Col 92 | CN25 | `= (10.679 * CM25) / ((CK25/1000)^4.871 * CL25^1.852)` | = (10.679 * CM25) / ((CK25/1000)^4.871 * CL25^1.852) |
| Ligne 25 | Col 93 | CO25 | `=IF(CH25="positif",CJ25,IF(CH25="negatif",-CJ25,""))` | =IF(CH25="positif",CJ25,IF(CH25="negatif",-CJ25,"")) |
| Ligne 25 | Col 94 | CP25 | `=IF(CF25>0,
IF(CO25>0, CN25*CO25^1.852,-CN25*ABS(CO25)^1.852),
IF(CO25>0, CN25*CJ25^1.852, -CN25*CJ25^1.852))` | =IF(CF25>0,
IF(CO25>0, CN25*CO25^1.852,-CN25*ABS(CO25)^1.852),
IF(CO25>0, CN25*CJ25^1.852, -CN25*CJ25^1.852)) |
| Ligne 25 | Col 95 | CQ25 | `=1.852*CN25*ABS(CO25)^(1.852-1)` | =1.852*CN25*ABS(CO25)^(1.852-1) |
| Ligne 25 | Col 96 | CR25 | `=CO25+$CJ$71` | =CO25+$CJ$71 |
| Ligne 25 | Col 100 | CV25 | `=IFERROR(MATCH(CY25,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY25,$CI$22:$CI$69,0),0) |
| Ligne 25 | Col 102 | CX25 | `=DIST_PHASE_1_v2!CF14` | =DIST_PHASE_1_v2!CF14 |
| Ligne 25 | Col 103 | CY25 | `=DIST_PHASE_1_v2!CG14` | =DIST_PHASE_1_v2!CG14 |
| Ligne 25 | Col 104 | CZ25 | `=DIST_PHASE_1_v2!CI14` | =DIST_PHASE_1_v2!CI14 |
| Ligne 25 | Col 105 | DA25 | `=DIST_PHASE_1_v2!CN14` | =DIST_PHASE_1_v2!CN14 |
| Ligne 25 | Col 106 | DB25 | `=DIST_PHASE_1_v2!CO14` | =DIST_PHASE_1_v2!CO14 |
| Ligne 25 | Col 107 | DC25 | `=DIST_PHASE_1_v2!CP14` | =DIST_PHASE_1_v2!CP14 |
| Ligne 25 | Col 108 | DD25 | `= (10.679 * DC25) / ((DA25/1000)^4.871 * DB25^1.852)` | = (10.679 * DC25) / ((DA25/1000)^4.871 * DB25^1.852) |
| Ligne 25 | Col 109 | DE25 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82B470>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82B470> |
| Ligne 25 | Col 110 | DF25 | `=IF(CV25>0,
IF(DE25>0, DD25*DE25^1.852,-DD25*ABS(DE25)^1.852),
IF(DE25>0, DD25*CZ25^1.852, -DD25*CZ25^1.852))` | =IF(CV25>0,
IF(DE25>0, DD25*DE25^1.852,-DD25*ABS(DE25)^1.852),
IF(DE25>0, DD25*CZ25^1.852, -DD25*CZ25^1.852)) |
| Ligne 25 | Col 111 | DG25 | `=1.852*DD25*ABS(DE25)^(1.852-1)` | =1.852*DD25*ABS(DE25)^(1.852-1) |
| Ligne 25 | Col 112 | DH25 | `=DE25+CZ59` | =DE25+CZ59 |
| Ligne 26 | Col 4 | D26 | `=DIST_PHASE_1_v2!E15` | =DIST_PHASE_1_v2!E15 |
| Ligne 26 | Col 5 | E26 | `=DIST_PHASE_1_v2!G15` | =DIST_PHASE_1_v2!G15 |
| Ligne 26 | Col 6 | F26 | `=DIST_PHASE_1_v2!L15` | =DIST_PHASE_1_v2!L15 |
| Ligne 26 | Col 7 | G26 | `=DIST_PHASE_1_v2!M15` | =DIST_PHASE_1_v2!M15 |
| Ligne 26 | Col 8 | H26 | `=DIST_PHASE_1_v2!N15` | =DIST_PHASE_1_v2!N15 |
| Ligne 26 | Col 9 | I26 | `= (10.679 * H26) / ((F26/1000)^4.871 * G26^1.852)` | = (10.679 * H26) / ((F26/1000)^4.871 * G26^1.852) |
| Ligne 26 | Col 10 | J26 | `=IF(C26="positif",E26,IF(C26="negatif",-E26,""))` | =IF(C26="positif",E26,IF(C26="negatif",-E26,"")) |
| Ligne 26 | Col 11 | K26 | `=IF(J26>0,I26*E26^1.852,-I26*E26^1.852)` | =IF(J26>0,I26*E26^1.852,-I26*E26^1.852) |
| Ligne 26 | Col 12 | L26 | `=1.852*I26*ABS(E26)^(1.852-1)` | =1.852*I26*ABS(E26)^(1.852-1) |
| Ligne 26 | Col 13 | M26 | `=J26+$D$93` | =J26+$D$93 |
| Ligne 26 | Col 16 | P26 | `=IFERROR(MATCH(S26,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S26,$D$22:$D$91,0),0) |
| Ligne 26 | Col 18 | R26 | `=DIST_PHASE_1_v2!Q15` | =DIST_PHASE_1_v2!Q15 |
| Ligne 26 | Col 19 | S26 | `=DIST_PHASE_1_v2!R15` | =DIST_PHASE_1_v2!R15 |
| Ligne 26 | Col 20 | T26 | `=DIST_PHASE_1_v2!T15` | =DIST_PHASE_1_v2!T15 |
| Ligne 26 | Col 21 | U26 | `=DIST_PHASE_1_v2!Y15` | =DIST_PHASE_1_v2!Y15 |
| Ligne 26 | Col 23 | W26 | `=DIST_PHASE_1_v2!AA15` | =DIST_PHASE_1_v2!AA15 |
| Ligne 26 | Col 24 | X26 | `= (10.679 * W26) / ((U26/1000)^4.871 * V26^1.852)` | = (10.679 * W26) / ((U26/1000)^4.871 * V26^1.852) |
| Ligne 26 | Col 25 | Y26 | `=IF(R26="positif",T26,IF(R26="negatif",-T26,""))` | =IF(R26="positif",T26,IF(R26="negatif",-T26,"")) |
| Ligne 26 | Col 26 | Z26 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8297F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8297F0> |
| Ligne 26 | Col 27 | AA26 | `=IF(P26>0,
IF(R26="positif",1,-1),
0)` | =IF(P26>0,
IF(R26="positif",1,-1),
0) |
| Ligne 26 | Col 28 | AB26 | `=X26*SIGN(Y26)*ABS(Y26)^1.852` | =X26*SIGN(Y26)*ABS(Y26)^1.852 |
| Ligne 26 | Col 29 | AC26 | `=1.852*X26*ABS(Y26)^(1.852-1)` | =1.852*X26*ABS(Y26)^(1.852-1) |
| Ligne 26 | Col 30 | AD26 | `=IF(P26>0,
Y26+($D$93*Z26)+(AA26*$S$93),
Y26+$S$93)` | =IF(P26>0,
Y26+($D$93*Z26)+(AA26*$S$93),
Y26+$S$93) |
| Ligne 26 | Col 32 | AF26 | `=ABS(AD26)-ABS(Y26)` | =ABS(AD26)-ABS(Y26) |
| Ligne 26 | Col 36 | AJ26 | `=IFERROR(MATCH(AM26,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM26,$S$22:$S$91,0),0) |
| Ligne 26 | Col 38 | AL26 | `=TRONCONS_V2!AI13` | =TRONCONS_V2!AI13 |
| Ligne 26 | Col 39 | AM26 | `=TRONCONS_V2!AE13` | =TRONCONS_V2!AE13 |
| Ligne 26 | Col 40 | AN26 | `=DIST_PHASE_1_v2!AG15` | =DIST_PHASE_1_v2!AG15 |
| Ligne 26 | Col 41 | AO26 | `=DIST_PHASE_1_v2!AL15` | =DIST_PHASE_1_v2!AL15 |
| Ligne 26 | Col 43 | AQ26 | `=TRONCONS_V2!AG13` | =TRONCONS_V2!AG13 |
| Ligne 26 | Col 44 | AR26 | `= (10.679 * AQ26) / ((AO26/1000)^4.871 * AP26^1.852)` | = (10.679 * AQ26) / ((AO26/1000)^4.871 * AP26^1.852) |
| Ligne 26 | Col 45 | AS26 | `=IF(AL26="positif",AN26,IF(AL26="negatif",-AN26,""))` | =IF(AL26="positif",AN26,IF(AL26="negatif",-AN26,"")) |
| Ligne 26 | Col 46 | AT26 | `=IF(AJ26>0,
IF(AS26>0, AR26*AS26^1.852,-AR26*ABS(AS26)^1.852),
IF(AS26>0, AR26*AN26^1.852, -AR26*AN26^1.852))` | =IF(AJ26>0,
IF(AS26>0, AR26*AS26^1.852,-AR26*ABS(AS26)^1.852),
IF(AS26>0, AR26*AN26^1.852, -AR26*AN26^1.852)) |
| Ligne 26 | Col 47 | AU26 | `=1.852*AR26*ABS(AS26)^(1.852-1)` | =1.852*AR26*ABS(AS26)^(1.852-1) |
| Ligne 26 | Col 48 | AV26 | `=AS26+$AN$60` | =AS26+$AN$60 |
| Ligne 26 | Col 52 | AZ26 | `=IFERROR(MATCH(BC26,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC26,$AM$22:$AM$57,0),0) |
| Ligne 26 | Col 54 | BB26 | `=DIST_PHASE_1_v2!AQ15` | =DIST_PHASE_1_v2!AQ15 |
| Ligne 26 | Col 55 | BC26 | `=DIST_PHASE_1_v2!AR15` | =DIST_PHASE_1_v2!AR15 |
| Ligne 26 | Col 56 | BD26 | `=DIST_PHASE_1_v2!AT15` | =DIST_PHASE_1_v2!AT15 |
| Ligne 26 | Col 57 | BE26 | `=DIST_PHASE_1_v2!AY15` | =DIST_PHASE_1_v2!AY15 |
| Ligne 26 | Col 58 | BF26 | `=DIST_PHASE_1_v2!AZ15` | =DIST_PHASE_1_v2!AZ15 |
| Ligne 26 | Col 59 | BG26 | `=DIST_PHASE_1_v2!BA15` | =DIST_PHASE_1_v2!BA15 |
| Ligne 26 | Col 60 | BH26 | `= (10.679 * BG26) / ((BE26/1000)^4.871 * BF26^1.852)` | = (10.679 * BG26) / ((BE26/1000)^4.871 * BF26^1.852) |
| Ligne 26 | Col 61 | BI26 | `=IF(BB26="positif",BD26,IF(BB26="negatif",-BD26,""))` | =IF(BB26="positif",BD26,IF(BB26="negatif",-BD26,"")) |
| Ligne 26 | Col 62 | BJ26 | `=IF(AZ26>0,
IF(BI26>0, BH26*BI26^1.852,-BH26*ABS(BI26)^1.852),
IF(BI26>0, BH26*BD26^1.852, -BH26*BD26^1.852))` | =IF(AZ26>0,
IF(BI26>0, BH26*BI26^1.852,-BH26*ABS(BI26)^1.852),
IF(BI26>0, BH26*BD26^1.852, -BH26*BD26^1.852)) |
| Ligne 26 | Col 63 | BK26 | `=1.852*BH26*ABS(BI26)^(1.852-1)` | =1.852*BH26*ABS(BI26)^(1.852-1) |
| Ligne 26 | Col 64 | BL26 | `=BI26+$BD$75` | =BI26+$BD$75 |
| Ligne 26 | Col 68 | BP26 | `=IFERROR(MATCH(BS26,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS26,$BC$22:$BC$73,0),0) |
| Ligne 26 | Col 70 | BR26 | `=DIST_PHASE_1_v2!BF15` | =DIST_PHASE_1_v2!BF15 |
| Ligne 26 | Col 71 | BS26 | `=DIST_PHASE_1_v2!BG15` | =DIST_PHASE_1_v2!BG15 |
| Ligne 26 | Col 72 | BT26 | `=DIST_PHASE_1_v2!BI15` | =DIST_PHASE_1_v2!BI15 |
| Ligne 26 | Col 73 | BU26 | `=DIST_PHASE_1_v2!BN15` | =DIST_PHASE_1_v2!BN15 |
| Ligne 26 | Col 74 | BV26 | `=DIST_PHASE_1_v2!BO15` | =DIST_PHASE_1_v2!BO15 |
| Ligne 26 | Col 75 | BW26 | `=DIST_PHASE_1_v2!BP15` | =DIST_PHASE_1_v2!BP15 |
| Ligne 26 | Col 76 | BX26 | `= (10.679 * BW26) / ((BU26/1000)^4.871 * BV26^1.852)` | = (10.679 * BW26) / ((BU26/1000)^4.871 * BV26^1.852) |
| Ligne 26 | Col 77 | BY26 | `=IF(BR26="positif",BT26,IF(BR26="negatif",-BT26,""))` | =IF(BR26="positif",BT26,IF(BR26="negatif",-BT26,"")) |
| Ligne 26 | Col 78 | BZ26 | `=IF(BP26>0,
IF(BY26>0, BX26*BY26^1.852,-BX26*ABS(BY26)^1.852),
IF(BY26>0, BX26*BT26^1.852, -BX26*BT26^1.852))` | =IF(BP26>0,
IF(BY26>0, BX26*BY26^1.852,-BX26*ABS(BY26)^1.852),
IF(BY26>0, BX26*BT26^1.852, -BX26*BT26^1.852)) |
| Ligne 26 | Col 79 | CA26 | `=1.852*BX26*ABS(BY26)^(1.852-1)` | =1.852*BX26*ABS(BY26)^(1.852-1) |
| Ligne 26 | Col 80 | CB26 | `=BY26+$BT$64` | =BY26+$BT$64 |
| Ligne 26 | Col 84 | CF26 | `=IFERROR(MATCH(CI26,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI26,$BS$22:$BS$62,0),0) |
| Ligne 26 | Col 86 | CH26 | `=DIST_PHASE_1_v2!BS15` | =DIST_PHASE_1_v2!BS15 |
| Ligne 26 | Col 87 | CI26 | `=DIST_PHASE_1_v2!BT15` | =DIST_PHASE_1_v2!BT15 |
| Ligne 26 | Col 88 | CJ26 | `=DIST_PHASE_1_v2!BV15` | =DIST_PHASE_1_v2!BV15 |
| Ligne 26 | Col 89 | CK26 | `=DIST_PHASE_1_v2!CA15` | =DIST_PHASE_1_v2!CA15 |
| Ligne 26 | Col 91 | CM26 | `=DIST_PHASE_1_v2!CC15` | =DIST_PHASE_1_v2!CC15 |
| Ligne 26 | Col 92 | CN26 | `= (10.679 * CM26) / ((CK26/1000)^4.871 * CL26^1.852)` | = (10.679 * CM26) / ((CK26/1000)^4.871 * CL26^1.852) |
| Ligne 26 | Col 93 | CO26 | `=IF(CH26="positif",CJ26,IF(CH26="negatif",-CJ26,""))` | =IF(CH26="positif",CJ26,IF(CH26="negatif",-CJ26,"")) |
| Ligne 26 | Col 94 | CP26 | `=IF(CF26>0,
IF(CO26>0, CN26*CO26^1.852,-CN26*ABS(CO26)^1.852),
IF(CO26>0, CN26*CJ26^1.852, -CN26*CJ26^1.852))` | =IF(CF26>0,
IF(CO26>0, CN26*CO26^1.852,-CN26*ABS(CO26)^1.852),
IF(CO26>0, CN26*CJ26^1.852, -CN26*CJ26^1.852)) |
| Ligne 26 | Col 95 | CQ26 | `=1.852*CN26*ABS(CO26)^(1.852-1)` | =1.852*CN26*ABS(CO26)^(1.852-1) |
| Ligne 26 | Col 96 | CR26 | `=CO26+$CJ$71` | =CO26+$CJ$71 |
| Ligne 26 | Col 100 | CV26 | `=IFERROR(MATCH(CY26,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY26,$CI$22:$CI$69,0),0) |
| Ligne 26 | Col 102 | CX26 | `=DIST_PHASE_1_v2!CF15` | =DIST_PHASE_1_v2!CF15 |
| Ligne 26 | Col 103 | CY26 | `=DIST_PHASE_1_v2!CG15` | =DIST_PHASE_1_v2!CG15 |
| Ligne 26 | Col 104 | CZ26 | `=DIST_PHASE_1_v2!CI15` | =DIST_PHASE_1_v2!CI15 |
| Ligne 26 | Col 105 | DA26 | `=DIST_PHASE_1_v2!CN15` | =DIST_PHASE_1_v2!CN15 |
| Ligne 26 | Col 106 | DB26 | `=DIST_PHASE_1_v2!CO15` | =DIST_PHASE_1_v2!CO15 |
| Ligne 26 | Col 107 | DC26 | `=DIST_PHASE_1_v2!CP15` | =DIST_PHASE_1_v2!CP15 |
| Ligne 26 | Col 108 | DD26 | `= (10.679 * DC26) / ((DA26/1000)^4.871 * DB26^1.852)` | = (10.679 * DC26) / ((DA26/1000)^4.871 * DB26^1.852) |
| Ligne 26 | Col 109 | DE26 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82BA10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82BA10> |
| Ligne 26 | Col 110 | DF26 | `=IF(CV26>0,
IF(DE26>0, DD26*DE26^1.852,-DD26*ABS(DE26)^1.852),
IF(DE26>0, DD26*CZ26^1.852, -DD26*CZ26^1.852))` | =IF(CV26>0,
IF(DE26>0, DD26*DE26^1.852,-DD26*ABS(DE26)^1.852),
IF(DE26>0, DD26*CZ26^1.852, -DD26*CZ26^1.852)) |
| Ligne 26 | Col 111 | DG26 | `=1.852*DD26*ABS(DE26)^(1.852-1)` | =1.852*DD26*ABS(DE26)^(1.852-1) |
| Ligne 26 | Col 112 | DH26 | `=DE26+CZ60` | =DE26+CZ60 |
| Ligne 27 | Col 4 | D27 | `=DIST_PHASE_1_v2!E16` | =DIST_PHASE_1_v2!E16 |
| Ligne 27 | Col 5 | E27 | `=DIST_PHASE_1_v2!G16` | =DIST_PHASE_1_v2!G16 |
| Ligne 27 | Col 6 | F27 | `=DIST_PHASE_1_v2!L16` | =DIST_PHASE_1_v2!L16 |
| Ligne 27 | Col 7 | G27 | `=DIST_PHASE_1_v2!M16` | =DIST_PHASE_1_v2!M16 |
| Ligne 27 | Col 8 | H27 | `=DIST_PHASE_1_v2!N16` | =DIST_PHASE_1_v2!N16 |
| Ligne 27 | Col 9 | I27 | `= (10.679 * H27) / ((F27/1000)^4.871 * G27^1.852)` | = (10.679 * H27) / ((F27/1000)^4.871 * G27^1.852) |
| Ligne 27 | Col 10 | J27 | `=IF(C27="positif",E27,IF(C27="negatif",-E27,""))` | =IF(C27="positif",E27,IF(C27="negatif",-E27,"")) |
| Ligne 27 | Col 11 | K27 | `=IF(J27>0,I27*E27^1.852,-I27*E27^1.852)` | =IF(J27>0,I27*E27^1.852,-I27*E27^1.852) |
| Ligne 27 | Col 12 | L27 | `=1.852*I27*ABS(E27)^(1.852-1)` | =1.852*I27*ABS(E27)^(1.852-1) |
| Ligne 27 | Col 13 | M27 | `=J27+$D$93` | =J27+$D$93 |
| Ligne 27 | Col 16 | P27 | `=IFERROR(MATCH(S27,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S27,$D$22:$D$91,0),0) |
| Ligne 27 | Col 18 | R27 | `=DIST_PHASE_1_v2!Q16` | =DIST_PHASE_1_v2!Q16 |
| Ligne 27 | Col 19 | S27 | `=DIST_PHASE_1_v2!R16` | =DIST_PHASE_1_v2!R16 |
| Ligne 27 | Col 20 | T27 | `=DIST_PHASE_1_v2!T16` | =DIST_PHASE_1_v2!T16 |
| Ligne 27 | Col 21 | U27 | `=DIST_PHASE_1_v2!Y16` | =DIST_PHASE_1_v2!Y16 |
| Ligne 27 | Col 23 | W27 | `=DIST_PHASE_1_v2!AA16` | =DIST_PHASE_1_v2!AA16 |
| Ligne 27 | Col 24 | X27 | `= (10.679 * W27) / ((U27/1000)^4.871 * V27^1.852)` | = (10.679 * W27) / ((U27/1000)^4.871 * V27^1.852) |
| Ligne 27 | Col 25 | Y27 | `=IF(R27="positif",T27,IF(R27="negatif",-T27,""))` | =IF(R27="positif",T27,IF(R27="negatif",-T27,"")) |
| Ligne 27 | Col 26 | Z27 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD829790>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD829790> |
| Ligne 27 | Col 27 | AA27 | `=IF(P27>0,
IF(R27="positif",1,-1),
0)` | =IF(P27>0,
IF(R27="positif",1,-1),
0) |
| Ligne 27 | Col 28 | AB27 | `=X27*SIGN(Y27)*ABS(Y27)^1.852` | =X27*SIGN(Y27)*ABS(Y27)^1.852 |
| Ligne 27 | Col 29 | AC27 | `=1.852*X27*ABS(Y27)^(1.852-1)` | =1.852*X27*ABS(Y27)^(1.852-1) |
| Ligne 27 | Col 30 | AD27 | `=IF(P27>0,
Y27+($D$93*Z27)+(AA27*$S$93),
Y27+$S$93)` | =IF(P27>0,
Y27+($D$93*Z27)+(AA27*$S$93),
Y27+$S$93) |
| Ligne 27 | Col 32 | AF27 | `=ABS(AD27)-ABS(Y27)` | =ABS(AD27)-ABS(Y27) |
| Ligne 27 | Col 36 | AJ27 | `=IFERROR(MATCH(AM27,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM27,$S$22:$S$91,0),0) |
| Ligne 27 | Col 38 | AL27 | `=TRONCONS_V2!AI14` | =TRONCONS_V2!AI14 |
| Ligne 27 | Col 39 | AM27 | `=TRONCONS_V2!AE14` | =TRONCONS_V2!AE14 |
| Ligne 27 | Col 40 | AN27 | `=DIST_PHASE_1_v2!AG16` | =DIST_PHASE_1_v2!AG16 |
| Ligne 27 | Col 41 | AO27 | `=DIST_PHASE_1_v2!AL16` | =DIST_PHASE_1_v2!AL16 |
| Ligne 27 | Col 43 | AQ27 | `=TRONCONS_V2!AG14` | =TRONCONS_V2!AG14 |
| Ligne 27 | Col 44 | AR27 | `= (10.679 * AQ27) / ((AO27/1000)^4.871 * AP27^1.852)` | = (10.679 * AQ27) / ((AO27/1000)^4.871 * AP27^1.852) |
| Ligne 27 | Col 45 | AS27 | `=IF(AL27="positif",AN27,IF(AL27="negatif",-AN27,""))` | =IF(AL27="positif",AN27,IF(AL27="negatif",-AN27,"")) |
| Ligne 27 | Col 46 | AT27 | `=IF(AJ27>0,
IF(AS27>0, AR27*AS27^1.852,-AR27*ABS(AS27)^1.852),
IF(AS27>0, AR27*AN27^1.852, -AR27*AN27^1.852))` | =IF(AJ27>0,
IF(AS27>0, AR27*AS27^1.852,-AR27*ABS(AS27)^1.852),
IF(AS27>0, AR27*AN27^1.852, -AR27*AN27^1.852)) |
| Ligne 27 | Col 47 | AU27 | `=1.852*AR27*ABS(AS27)^(1.852-1)` | =1.852*AR27*ABS(AS27)^(1.852-1) |
| Ligne 27 | Col 48 | AV27 | `=AS27+$AN$60` | =AS27+$AN$60 |
| Ligne 27 | Col 52 | AZ27 | `=IFERROR(MATCH(BC27,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC27,$AM$22:$AM$57,0),0) |
| Ligne 27 | Col 54 | BB27 | `=DIST_PHASE_1_v2!AQ16` | =DIST_PHASE_1_v2!AQ16 |
| Ligne 27 | Col 55 | BC27 | `=DIST_PHASE_1_v2!AR16` | =DIST_PHASE_1_v2!AR16 |
| Ligne 27 | Col 56 | BD27 | `=DIST_PHASE_1_v2!AT16` | =DIST_PHASE_1_v2!AT16 |
| Ligne 27 | Col 57 | BE27 | `=DIST_PHASE_1_v2!AY16` | =DIST_PHASE_1_v2!AY16 |
| Ligne 27 | Col 58 | BF27 | `=DIST_PHASE_1_v2!AZ16` | =DIST_PHASE_1_v2!AZ16 |
| Ligne 27 | Col 59 | BG27 | `=DIST_PHASE_1_v2!BA16` | =DIST_PHASE_1_v2!BA16 |
| Ligne 27 | Col 60 | BH27 | `= (10.679 * BG27) / ((BE27/1000)^4.871 * BF27^1.852)` | = (10.679 * BG27) / ((BE27/1000)^4.871 * BF27^1.852) |
| Ligne 27 | Col 61 | BI27 | `=IF(BB27="positif",BD27,IF(BB27="negatif",-BD27,""))` | =IF(BB27="positif",BD27,IF(BB27="negatif",-BD27,"")) |
| Ligne 27 | Col 62 | BJ27 | `=IF(AZ27>0,
IF(BI27>0, BH27*BI27^1.852,-BH27*ABS(BI27)^1.852),
IF(BI27>0, BH27*BD27^1.852, -BH27*BD27^1.852))` | =IF(AZ27>0,
IF(BI27>0, BH27*BI27^1.852,-BH27*ABS(BI27)^1.852),
IF(BI27>0, BH27*BD27^1.852, -BH27*BD27^1.852)) |
| Ligne 27 | Col 63 | BK27 | `=1.852*BH27*ABS(BI27)^(1.852-1)` | =1.852*BH27*ABS(BI27)^(1.852-1) |
| Ligne 27 | Col 64 | BL27 | `=BI27+$BD$75` | =BI27+$BD$75 |
| Ligne 27 | Col 68 | BP27 | `=IFERROR(MATCH(BS27,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS27,$BC$22:$BC$73,0),0) |
| Ligne 27 | Col 70 | BR27 | `=DIST_PHASE_1_v2!BF16` | =DIST_PHASE_1_v2!BF16 |
| Ligne 27 | Col 71 | BS27 | `=DIST_PHASE_1_v2!BG16` | =DIST_PHASE_1_v2!BG16 |
| Ligne 27 | Col 72 | BT27 | `=DIST_PHASE_1_v2!BI16` | =DIST_PHASE_1_v2!BI16 |
| Ligne 27 | Col 73 | BU27 | `=DIST_PHASE_1_v2!BN16` | =DIST_PHASE_1_v2!BN16 |
| Ligne 27 | Col 74 | BV27 | `=DIST_PHASE_1_v2!BO16` | =DIST_PHASE_1_v2!BO16 |
| Ligne 27 | Col 75 | BW27 | `=DIST_PHASE_1_v2!BP16` | =DIST_PHASE_1_v2!BP16 |
| Ligne 27 | Col 76 | BX27 | `= (10.679 * BW27) / ((BU27/1000)^4.871 * BV27^1.852)` | = (10.679 * BW27) / ((BU27/1000)^4.871 * BV27^1.852) |
| Ligne 27 | Col 77 | BY27 | `=IF(BR27="positif",BT27,IF(BR27="negatif",-BT27,""))` | =IF(BR27="positif",BT27,IF(BR27="negatif",-BT27,"")) |
| Ligne 27 | Col 78 | BZ27 | `=IF(BP27>0,
IF(BY27>0, BX27*BY27^1.852,-BX27*ABS(BY27)^1.852),
IF(BY27>0, BX27*BT27^1.852, -BX27*BT27^1.852))` | =IF(BP27>0,
IF(BY27>0, BX27*BY27^1.852,-BX27*ABS(BY27)^1.852),
IF(BY27>0, BX27*BT27^1.852, -BX27*BT27^1.852)) |
| Ligne 27 | Col 79 | CA27 | `=1.852*BX27*ABS(BY27)^(1.852-1)` | =1.852*BX27*ABS(BY27)^(1.852-1) |
| Ligne 27 | Col 80 | CB27 | `=BY27+$BT$64` | =BY27+$BT$64 |
| Ligne 27 | Col 84 | CF27 | `=IFERROR(MATCH(CI27,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI27,$BS$22:$BS$62,0),0) |
| Ligne 27 | Col 86 | CH27 | `=DIST_PHASE_1_v2!BS16` | =DIST_PHASE_1_v2!BS16 |
| Ligne 27 | Col 87 | CI27 | `=DIST_PHASE_1_v2!BT16` | =DIST_PHASE_1_v2!BT16 |
| Ligne 27 | Col 88 | CJ27 | `=DIST_PHASE_1_v2!BV16` | =DIST_PHASE_1_v2!BV16 |
| Ligne 27 | Col 89 | CK27 | `=DIST_PHASE_1_v2!CA16` | =DIST_PHASE_1_v2!CA16 |
| Ligne 27 | Col 91 | CM27 | `=DIST_PHASE_1_v2!CC16` | =DIST_PHASE_1_v2!CC16 |
| Ligne 27 | Col 92 | CN27 | `= (10.679 * CM27) / ((CK27/1000)^4.871 * CL27^1.852)` | = (10.679 * CM27) / ((CK27/1000)^4.871 * CL27^1.852) |
| Ligne 27 | Col 93 | CO27 | `=IF(CH27="positif",CJ27,IF(CH27="negatif",-CJ27,""))` | =IF(CH27="positif",CJ27,IF(CH27="negatif",-CJ27,"")) |
| Ligne 27 | Col 94 | CP27 | `=IF(CF27>0,
IF(CO27>0, CN27*CO27^1.852,-CN27*ABS(CO27)^1.852),
IF(CO27>0, CN27*CJ27^1.852, -CN27*CJ27^1.852))` | =IF(CF27>0,
IF(CO27>0, CN27*CO27^1.852,-CN27*ABS(CO27)^1.852),
IF(CO27>0, CN27*CJ27^1.852, -CN27*CJ27^1.852)) |
| Ligne 27 | Col 95 | CQ27 | `=1.852*CN27*ABS(CO27)^(1.852-1)` | =1.852*CN27*ABS(CO27)^(1.852-1) |
| Ligne 27 | Col 96 | CR27 | `=CO27+$CJ$71` | =CO27+$CJ$71 |
| Ligne 27 | Col 100 | CV27 | `=IFERROR(MATCH(CY27,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY27,$CI$22:$CI$69,0),0) |
| Ligne 27 | Col 102 | CX27 | `=DIST_PHASE_1_v2!CF16` | =DIST_PHASE_1_v2!CF16 |
| Ligne 27 | Col 103 | CY27 | `=DIST_PHASE_1_v2!CG16` | =DIST_PHASE_1_v2!CG16 |
| Ligne 27 | Col 104 | CZ27 | `=DIST_PHASE_1_v2!CI16` | =DIST_PHASE_1_v2!CI16 |
| Ligne 27 | Col 105 | DA27 | `=DIST_PHASE_1_v2!CN16` | =DIST_PHASE_1_v2!CN16 |
| Ligne 27 | Col 106 | DB27 | `=DIST_PHASE_1_v2!CO16` | =DIST_PHASE_1_v2!CO16 |
| Ligne 27 | Col 107 | DC27 | `=DIST_PHASE_1_v2!CP16` | =DIST_PHASE_1_v2!CP16 |
| Ligne 27 | Col 108 | DD27 | `= (10.679 * DC27) / ((DA27/1000)^4.871 * DB27^1.852)` | = (10.679 * DC27) / ((DA27/1000)^4.871 * DB27^1.852) |
| Ligne 27 | Col 109 | DE27 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E4110>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E4110> |
| Ligne 27 | Col 110 | DF27 | `=IF(CV27>0,
IF(DE27>0, DD27*DE27^1.852,-DD27*ABS(DE27)^1.852),
IF(DE27>0, DD27*CZ27^1.852, -DD27*CZ27^1.852))` | =IF(CV27>0,
IF(DE27>0, DD27*DE27^1.852,-DD27*ABS(DE27)^1.852),
IF(DE27>0, DD27*CZ27^1.852, -DD27*CZ27^1.852)) |
| Ligne 27 | Col 111 | DG27 | `=1.852*DD27*ABS(DE27)^(1.852-1)` | =1.852*DD27*ABS(DE27)^(1.852-1) |
| Ligne 27 | Col 112 | DH27 | `=DE27+CZ61` | =DE27+CZ61 |
| Ligne 28 | Col 4 | D28 | `=DIST_PHASE_1_v2!E17` | =DIST_PHASE_1_v2!E17 |
| Ligne 28 | Col 5 | E28 | `=DIST_PHASE_1_v2!G17` | =DIST_PHASE_1_v2!G17 |
| Ligne 28 | Col 6 | F28 | `=DIST_PHASE_1_v2!L17` | =DIST_PHASE_1_v2!L17 |
| Ligne 28 | Col 7 | G28 | `=DIST_PHASE_1_v2!M17` | =DIST_PHASE_1_v2!M17 |
| Ligne 28 | Col 8 | H28 | `=DIST_PHASE_1_v2!N17` | =DIST_PHASE_1_v2!N17 |
| Ligne 28 | Col 9 | I28 | `= (10.679 * H28) / ((F28/1000)^4.871 * G28^1.852)` | = (10.679 * H28) / ((F28/1000)^4.871 * G28^1.852) |
| Ligne 28 | Col 10 | J28 | `=IF(C28="positif",E28,IF(C28="negatif",-E28,""))` | =IF(C28="positif",E28,IF(C28="negatif",-E28,"")) |
| Ligne 28 | Col 11 | K28 | `=IF(J28>0,I28*E28^1.852,-I28*E28^1.852)` | =IF(J28>0,I28*E28^1.852,-I28*E28^1.852) |
| Ligne 28 | Col 12 | L28 | `=1.852*I28*ABS(E28)^(1.852-1)` | =1.852*I28*ABS(E28)^(1.852-1) |
| Ligne 28 | Col 13 | M28 | `=J28+$D$93` | =J28+$D$93 |
| Ligne 28 | Col 16 | P28 | `=IFERROR(MATCH(S28,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S28,$D$22:$D$91,0),0) |
| Ligne 28 | Col 18 | R28 | `=DIST_PHASE_1_v2!Q17` | =DIST_PHASE_1_v2!Q17 |
| Ligne 28 | Col 19 | S28 | `=DIST_PHASE_1_v2!R17` | =DIST_PHASE_1_v2!R17 |
| Ligne 28 | Col 20 | T28 | `=DIST_PHASE_1_v2!T17` | =DIST_PHASE_1_v2!T17 |
| Ligne 28 | Col 21 | U28 | `=DIST_PHASE_1_v2!Y17` | =DIST_PHASE_1_v2!Y17 |
| Ligne 28 | Col 23 | W28 | `=DIST_PHASE_1_v2!AA17` | =DIST_PHASE_1_v2!AA17 |
| Ligne 28 | Col 24 | X28 | `= (10.679 * W28) / ((U28/1000)^4.871 * V28^1.852)` | = (10.679 * W28) / ((U28/1000)^4.871 * V28^1.852) |
| Ligne 28 | Col 25 | Y28 | `=IF(R28="positif",T28,IF(R28="negatif",-T28,""))` | =IF(R28="positif",T28,IF(R28="negatif",-T28,"")) |
| Ligne 28 | Col 26 | Z28 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82BA70>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82BA70> |
| Ligne 28 | Col 27 | AA28 | `=IF(P28>0,
IF(R28="positif",1,-1),
0)` | =IF(P28>0,
IF(R28="positif",1,-1),
0) |
| Ligne 28 | Col 28 | AB28 | `=X28*SIGN(Y28)*ABS(Y28)^1.852` | =X28*SIGN(Y28)*ABS(Y28)^1.852 |
| Ligne 28 | Col 29 | AC28 | `=1.852*X28*ABS(Y28)^(1.852-1)` | =1.852*X28*ABS(Y28)^(1.852-1) |
| Ligne 28 | Col 30 | AD28 | `=IF(P28>0,
Y28+($D$93*Z28)+(AA28*$S$93),
Y28+$S$93)` | =IF(P28>0,
Y28+($D$93*Z28)+(AA28*$S$93),
Y28+$S$93) |
| Ligne 28 | Col 32 | AF28 | `=ABS(AD28)-ABS(Y28)` | =ABS(AD28)-ABS(Y28) |
| Ligne 28 | Col 36 | AJ28 | `=IFERROR(MATCH(AM28,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM28,$S$22:$S$91,0),0) |
| Ligne 28 | Col 38 | AL28 | `=TRONCONS_V2!AI15` | =TRONCONS_V2!AI15 |
| Ligne 28 | Col 39 | AM28 | `=TRONCONS_V2!AE15` | =TRONCONS_V2!AE15 |
| Ligne 28 | Col 40 | AN28 | `=DIST_PHASE_1_v2!AG17` | =DIST_PHASE_1_v2!AG17 |
| Ligne 28 | Col 41 | AO28 | `=DIST_PHASE_1_v2!AL17` | =DIST_PHASE_1_v2!AL17 |
| Ligne 28 | Col 43 | AQ28 | `=TRONCONS_V2!AG15` | =TRONCONS_V2!AG15 |
| Ligne 28 | Col 44 | AR28 | `= (10.679 * AQ28) / ((AO28/1000)^4.871 * AP28^1.852)` | = (10.679 * AQ28) / ((AO28/1000)^4.871 * AP28^1.852) |
| Ligne 28 | Col 45 | AS28 | `=IF(AL28="positif",AN28,IF(AL28="negatif",-AN28,""))` | =IF(AL28="positif",AN28,IF(AL28="negatif",-AN28,"")) |
| Ligne 28 | Col 46 | AT28 | `=IF(AJ28>0,
IF(AS28>0, AR28*AS28^1.852,-AR28*ABS(AS28)^1.852),
IF(AS28>0, AR28*AN28^1.852, -AR28*AN28^1.852))` | =IF(AJ28>0,
IF(AS28>0, AR28*AS28^1.852,-AR28*ABS(AS28)^1.852),
IF(AS28>0, AR28*AN28^1.852, -AR28*AN28^1.852)) |
| Ligne 28 | Col 47 | AU28 | `=1.852*AR28*ABS(AS28)^(1.852-1)` | =1.852*AR28*ABS(AS28)^(1.852-1) |
| Ligne 28 | Col 48 | AV28 | `=AS28+$AN$60` | =AS28+$AN$60 |
| Ligne 28 | Col 52 | AZ28 | `=IFERROR(MATCH(BC28,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC28,$AM$22:$AM$57,0),0) |
| Ligne 28 | Col 54 | BB28 | `=DIST_PHASE_1_v2!AQ17` | =DIST_PHASE_1_v2!AQ17 |
| Ligne 28 | Col 55 | BC28 | `=DIST_PHASE_1_v2!AR17` | =DIST_PHASE_1_v2!AR17 |
| Ligne 28 | Col 56 | BD28 | `=DIST_PHASE_1_v2!AT17` | =DIST_PHASE_1_v2!AT17 |
| Ligne 28 | Col 57 | BE28 | `=DIST_PHASE_1_v2!AY17` | =DIST_PHASE_1_v2!AY17 |
| Ligne 28 | Col 58 | BF28 | `=DIST_PHASE_1_v2!AZ17` | =DIST_PHASE_1_v2!AZ17 |
| Ligne 28 | Col 59 | BG28 | `=DIST_PHASE_1_v2!BA17` | =DIST_PHASE_1_v2!BA17 |
| Ligne 28 | Col 60 | BH28 | `= (10.679 * BG28) / ((BE28/1000)^4.871 * BF28^1.852)` | = (10.679 * BG28) / ((BE28/1000)^4.871 * BF28^1.852) |
| Ligne 28 | Col 61 | BI28 | `=IF(BB28="positif",BD28,IF(BB28="negatif",-BD28,""))` | =IF(BB28="positif",BD28,IF(BB28="negatif",-BD28,"")) |
| Ligne 28 | Col 62 | BJ28 | `=IF(AZ28>0,
IF(BI28>0, BH28*BI28^1.852,-BH28*ABS(BI28)^1.852),
IF(BI28>0, BH28*BD28^1.852, -BH28*BD28^1.852))` | =IF(AZ28>0,
IF(BI28>0, BH28*BI28^1.852,-BH28*ABS(BI28)^1.852),
IF(BI28>0, BH28*BD28^1.852, -BH28*BD28^1.852)) |
| Ligne 28 | Col 63 | BK28 | `=1.852*BH28*ABS(BI28)^(1.852-1)` | =1.852*BH28*ABS(BI28)^(1.852-1) |
| Ligne 28 | Col 64 | BL28 | `=BI28+$BD$75` | =BI28+$BD$75 |
| Ligne 28 | Col 68 | BP28 | `=IFERROR(MATCH(BS28,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS28,$BC$22:$BC$73,0),0) |
| Ligne 28 | Col 70 | BR28 | `=DIST_PHASE_1_v2!BF17` | =DIST_PHASE_1_v2!BF17 |
| Ligne 28 | Col 71 | BS28 | `=DIST_PHASE_1_v2!BG17` | =DIST_PHASE_1_v2!BG17 |
| Ligne 28 | Col 72 | BT28 | `=DIST_PHASE_1_v2!BI17` | =DIST_PHASE_1_v2!BI17 |
| Ligne 28 | Col 73 | BU28 | `=DIST_PHASE_1_v2!BN17` | =DIST_PHASE_1_v2!BN17 |
| Ligne 28 | Col 74 | BV28 | `=DIST_PHASE_1_v2!BO17` | =DIST_PHASE_1_v2!BO17 |
| Ligne 28 | Col 75 | BW28 | `=DIST_PHASE_1_v2!BP17` | =DIST_PHASE_1_v2!BP17 |
| Ligne 28 | Col 76 | BX28 | `= (10.679 * BW28) / ((BU28/1000)^4.871 * BV28^1.852)` | = (10.679 * BW28) / ((BU28/1000)^4.871 * BV28^1.852) |
| Ligne 28 | Col 77 | BY28 | `=IF(BR28="positif",BT28,IF(BR28="negatif",-BT28,""))` | =IF(BR28="positif",BT28,IF(BR28="negatif",-BT28,"")) |
| Ligne 28 | Col 78 | BZ28 | `=IF(BP28>0,
IF(BY28>0, BX28*BY28^1.852,-BX28*ABS(BY28)^1.852),
IF(BY28>0, BX28*BT28^1.852, -BX28*BT28^1.852))` | =IF(BP28>0,
IF(BY28>0, BX28*BY28^1.852,-BX28*ABS(BY28)^1.852),
IF(BY28>0, BX28*BT28^1.852, -BX28*BT28^1.852)) |
| Ligne 28 | Col 79 | CA28 | `=1.852*BX28*ABS(BY28)^(1.852-1)` | =1.852*BX28*ABS(BY28)^(1.852-1) |
| Ligne 28 | Col 80 | CB28 | `=BY28+$BT$64` | =BY28+$BT$64 |
| Ligne 28 | Col 84 | CF28 | `=IFERROR(MATCH(CI28,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI28,$BS$22:$BS$62,0),0) |
| Ligne 28 | Col 86 | CH28 | `=DIST_PHASE_1_v2!BS17` | =DIST_PHASE_1_v2!BS17 |
| Ligne 28 | Col 87 | CI28 | `=DIST_PHASE_1_v2!BT17` | =DIST_PHASE_1_v2!BT17 |
| Ligne 28 | Col 88 | CJ28 | `=DIST_PHASE_1_v2!BV17` | =DIST_PHASE_1_v2!BV17 |
| Ligne 28 | Col 89 | CK28 | `=DIST_PHASE_1_v2!CA17` | =DIST_PHASE_1_v2!CA17 |
| Ligne 28 | Col 91 | CM28 | `=DIST_PHASE_1_v2!CC17` | =DIST_PHASE_1_v2!CC17 |
| Ligne 28 | Col 92 | CN28 | `= (10.679 * CM28) / ((CK28/1000)^4.871 * CL28^1.852)` | = (10.679 * CM28) / ((CK28/1000)^4.871 * CL28^1.852) |
| Ligne 28 | Col 93 | CO28 | `=IF(CH28="positif",CJ28,IF(CH28="negatif",-CJ28,""))` | =IF(CH28="positif",CJ28,IF(CH28="negatif",-CJ28,"")) |
| Ligne 28 | Col 94 | CP28 | `=IF(CF28>0,
IF(CO28>0, CN28*CO28^1.852,-CN28*ABS(CO28)^1.852),
IF(CO28>0, CN28*CJ28^1.852, -CN28*CJ28^1.852))` | =IF(CF28>0,
IF(CO28>0, CN28*CO28^1.852,-CN28*ABS(CO28)^1.852),
IF(CO28>0, CN28*CJ28^1.852, -CN28*CJ28^1.852)) |
| Ligne 28 | Col 95 | CQ28 | `=1.852*CN28*ABS(CO28)^(1.852-1)` | =1.852*CN28*ABS(CO28)^(1.852-1) |
| Ligne 28 | Col 96 | CR28 | `=CO28+$CJ$71` | =CO28+$CJ$71 |
| Ligne 28 | Col 100 | CV28 | `=IFERROR(MATCH(CY28,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY28,$CI$22:$CI$69,0),0) |
| Ligne 28 | Col 102 | CX28 | `=DIST_PHASE_1_v2!CF17` | =DIST_PHASE_1_v2!CF17 |
| Ligne 28 | Col 103 | CY28 | `=DIST_PHASE_1_v2!CG17` | =DIST_PHASE_1_v2!CG17 |
| Ligne 28 | Col 104 | CZ28 | `=DIST_PHASE_1_v2!CI17` | =DIST_PHASE_1_v2!CI17 |
| Ligne 28 | Col 105 | DA28 | `=DIST_PHASE_1_v2!CN17` | =DIST_PHASE_1_v2!CN17 |
| Ligne 28 | Col 106 | DB28 | `=DIST_PHASE_1_v2!CO17` | =DIST_PHASE_1_v2!CO17 |
| Ligne 28 | Col 107 | DC28 | `=DIST_PHASE_1_v2!CP17` | =DIST_PHASE_1_v2!CP17 |
| Ligne 28 | Col 108 | DD28 | `= (10.679 * DC28) / ((DA28/1000)^4.871 * DB28^1.852)` | = (10.679 * DC28) / ((DA28/1000)^4.871 * DB28^1.852) |
| Ligne 28 | Col 109 | DE28 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E46B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E46B0> |
| Ligne 28 | Col 110 | DF28 | `=IF(CV28>0,
IF(DE28>0, DD28*DE28^1.852,-DD28*ABS(DE28)^1.852),
IF(DE28>0, DD28*CZ28^1.852, -DD28*CZ28^1.852))` | =IF(CV28>0,
IF(DE28>0, DD28*DE28^1.852,-DD28*ABS(DE28)^1.852),
IF(DE28>0, DD28*CZ28^1.852, -DD28*CZ28^1.852)) |
| Ligne 28 | Col 111 | DG28 | `=1.852*DD28*ABS(DE28)^(1.852-1)` | =1.852*DD28*ABS(DE28)^(1.852-1) |
| Ligne 28 | Col 112 | DH28 | `=DE28+CZ62` | =DE28+CZ62 |
| Ligne 29 | Col 4 | D29 | `=DIST_PHASE_1_v2!E18` | =DIST_PHASE_1_v2!E18 |
| Ligne 29 | Col 5 | E29 | `=DIST_PHASE_1_v2!G18` | =DIST_PHASE_1_v2!G18 |
| Ligne 29 | Col 6 | F29 | `=DIST_PHASE_1_v2!L18` | =DIST_PHASE_1_v2!L18 |
| Ligne 29 | Col 7 | G29 | `=DIST_PHASE_1_v2!M18` | =DIST_PHASE_1_v2!M18 |
| Ligne 29 | Col 8 | H29 | `=DIST_PHASE_1_v2!N18` | =DIST_PHASE_1_v2!N18 |
| Ligne 29 | Col 9 | I29 | `= (10.679 * H29) / ((F29/1000)^4.871 * G29^1.852)` | = (10.679 * H29) / ((F29/1000)^4.871 * G29^1.852) |
| Ligne 29 | Col 10 | J29 | `=IF(C29="positif",E29,IF(C29="negatif",-E29,""))` | =IF(C29="positif",E29,IF(C29="negatif",-E29,"")) |
| Ligne 29 | Col 11 | K29 | `=IF(J29>0,I29*E29^1.852,-I29*E29^1.852)` | =IF(J29>0,I29*E29^1.852,-I29*E29^1.852) |
| Ligne 29 | Col 12 | L29 | `=1.852*I29*ABS(E29)^(1.852-1)` | =1.852*I29*ABS(E29)^(1.852-1) |
| Ligne 29 | Col 13 | M29 | `=J29+$D$93` | =J29+$D$93 |
| Ligne 29 | Col 16 | P29 | `=IFERROR(MATCH(S29,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S29,$D$22:$D$91,0),0) |
| Ligne 29 | Col 18 | R29 | `=DIST_PHASE_1_v2!Q18` | =DIST_PHASE_1_v2!Q18 |
| Ligne 29 | Col 19 | S29 | `=DIST_PHASE_1_v2!R18` | =DIST_PHASE_1_v2!R18 |
| Ligne 29 | Col 20 | T29 | `=DIST_PHASE_1_v2!T18` | =DIST_PHASE_1_v2!T18 |
| Ligne 29 | Col 21 | U29 | `=DIST_PHASE_1_v2!Y18` | =DIST_PHASE_1_v2!Y18 |
| Ligne 29 | Col 23 | W29 | `=DIST_PHASE_1_v2!AA18` | =DIST_PHASE_1_v2!AA18 |
| Ligne 29 | Col 24 | X29 | `= (10.679 * W29) / ((U29/1000)^4.871 * V29^1.852)` | = (10.679 * W29) / ((U29/1000)^4.871 * V29^1.852) |
| Ligne 29 | Col 25 | Y29 | `=IF(R29="positif",T29,IF(R29="negatif",-T29,""))` | =IF(R29="positif",T29,IF(R29="negatif",-T29,"")) |
| Ligne 29 | Col 26 | Z29 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82BAD0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82BAD0> |
| Ligne 29 | Col 27 | AA29 | `=IF(P29>0,
IF(R29="positif",1,-1),
0)` | =IF(P29>0,
IF(R29="positif",1,-1),
0) |
| Ligne 29 | Col 28 | AB29 | `=X29*SIGN(Y29)*ABS(Y29)^1.852` | =X29*SIGN(Y29)*ABS(Y29)^1.852 |
| Ligne 29 | Col 29 | AC29 | `=1.852*X29*ABS(Y29)^(1.852-1)` | =1.852*X29*ABS(Y29)^(1.852-1) |
| Ligne 29 | Col 30 | AD29 | `=IF(P29>0,
Y29+($D$93*Z29)+(AA29*$S$93),
Y29+$S$93)` | =IF(P29>0,
Y29+($D$93*Z29)+(AA29*$S$93),
Y29+$S$93) |
| Ligne 29 | Col 32 | AF29 | `=ABS(AD29)-ABS(Y29)` | =ABS(AD29)-ABS(Y29) |
| Ligne 29 | Col 36 | AJ29 | `=IFERROR(MATCH(AM29,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM29,$S$22:$S$91,0),0) |
| Ligne 29 | Col 38 | AL29 | `=TRONCONS_V2!AI16` | =TRONCONS_V2!AI16 |
| Ligne 29 | Col 39 | AM29 | `=TRONCONS_V2!AE16` | =TRONCONS_V2!AE16 |
| Ligne 29 | Col 40 | AN29 | `=DIST_PHASE_1_v2!AG18` | =DIST_PHASE_1_v2!AG18 |
| Ligne 29 | Col 41 | AO29 | `=DIST_PHASE_1_v2!AL18` | =DIST_PHASE_1_v2!AL18 |
| Ligne 29 | Col 43 | AQ29 | `=TRONCONS_V2!AG16` | =TRONCONS_V2!AG16 |
| Ligne 29 | Col 44 | AR29 | `= (10.679 * AQ29) / ((AO29/1000)^4.871 * AP29^1.852)` | = (10.679 * AQ29) / ((AO29/1000)^4.871 * AP29^1.852) |
| Ligne 29 | Col 45 | AS29 | `=IF(AL29="positif",AN29,IF(AL29="negatif",-AN29,""))` | =IF(AL29="positif",AN29,IF(AL29="negatif",-AN29,"")) |
| Ligne 29 | Col 46 | AT29 | `=IF(AJ29>0,
IF(AS29>0, AR29*AS29^1.852,-AR29*ABS(AS29)^1.852),
IF(AS29>0, AR29*AN29^1.852, -AR29*AN29^1.852))` | =IF(AJ29>0,
IF(AS29>0, AR29*AS29^1.852,-AR29*ABS(AS29)^1.852),
IF(AS29>0, AR29*AN29^1.852, -AR29*AN29^1.852)) |
| Ligne 29 | Col 47 | AU29 | `=1.852*AR29*ABS(AS29)^(1.852-1)` | =1.852*AR29*ABS(AS29)^(1.852-1) |
| Ligne 29 | Col 48 | AV29 | `=AS29+$AN$60` | =AS29+$AN$60 |
| Ligne 29 | Col 52 | AZ29 | `=IFERROR(MATCH(BC29,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC29,$AM$22:$AM$57,0),0) |
| Ligne 29 | Col 54 | BB29 | `=DIST_PHASE_1_v2!AQ18` | =DIST_PHASE_1_v2!AQ18 |
| Ligne 29 | Col 55 | BC29 | `=DIST_PHASE_1_v2!AR18` | =DIST_PHASE_1_v2!AR18 |
| Ligne 29 | Col 56 | BD29 | `=DIST_PHASE_1_v2!AT18` | =DIST_PHASE_1_v2!AT18 |
| Ligne 29 | Col 57 | BE29 | `=DIST_PHASE_1_v2!AY18` | =DIST_PHASE_1_v2!AY18 |
| Ligne 29 | Col 58 | BF29 | `=DIST_PHASE_1_v2!AZ18` | =DIST_PHASE_1_v2!AZ18 |
| Ligne 29 | Col 59 | BG29 | `=DIST_PHASE_1_v2!BA18` | =DIST_PHASE_1_v2!BA18 |
| Ligne 29 | Col 60 | BH29 | `= (10.679 * BG29) / ((BE29/1000)^4.871 * BF29^1.852)` | = (10.679 * BG29) / ((BE29/1000)^4.871 * BF29^1.852) |
| Ligne 29 | Col 61 | BI29 | `=IF(BB29="positif",BD29,IF(BB29="negatif",-BD29,""))` | =IF(BB29="positif",BD29,IF(BB29="negatif",-BD29,"")) |
| Ligne 29 | Col 62 | BJ29 | `=IF(AZ29>0,
IF(BI29>0, BH29*BI29^1.852,-BH29*ABS(BI29)^1.852),
IF(BI29>0, BH29*BD29^1.852, -BH29*BD29^1.852))` | =IF(AZ29>0,
IF(BI29>0, BH29*BI29^1.852,-BH29*ABS(BI29)^1.852),
IF(BI29>0, BH29*BD29^1.852, -BH29*BD29^1.852)) |
| Ligne 29 | Col 63 | BK29 | `=1.852*BH29*ABS(BI29)^(1.852-1)` | =1.852*BH29*ABS(BI29)^(1.852-1) |
| Ligne 29 | Col 64 | BL29 | `=BI29+$BD$75` | =BI29+$BD$75 |
| Ligne 29 | Col 68 | BP29 | `=IFERROR(MATCH(BS29,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS29,$BC$22:$BC$73,0),0) |
| Ligne 29 | Col 70 | BR29 | `=DIST_PHASE_1_v2!BF18` | =DIST_PHASE_1_v2!BF18 |
| Ligne 29 | Col 71 | BS29 | `=DIST_PHASE_1_v2!BG18` | =DIST_PHASE_1_v2!BG18 |
| Ligne 29 | Col 72 | BT29 | `=DIST_PHASE_1_v2!BI18` | =DIST_PHASE_1_v2!BI18 |
| Ligne 29 | Col 73 | BU29 | `=DIST_PHASE_1_v2!BN18` | =DIST_PHASE_1_v2!BN18 |
| Ligne 29 | Col 74 | BV29 | `=DIST_PHASE_1_v2!BO18` | =DIST_PHASE_1_v2!BO18 |
| Ligne 29 | Col 75 | BW29 | `=DIST_PHASE_1_v2!BP18` | =DIST_PHASE_1_v2!BP18 |
| Ligne 29 | Col 76 | BX29 | `= (10.679 * BW29) / ((BU29/1000)^4.871 * BV29^1.852)` | = (10.679 * BW29) / ((BU29/1000)^4.871 * BV29^1.852) |
| Ligne 29 | Col 77 | BY29 | `=IF(BR29="positif",BT29,IF(BR29="negatif",-BT29,""))` | =IF(BR29="positif",BT29,IF(BR29="negatif",-BT29,"")) |
| Ligne 29 | Col 78 | BZ29 | `=IF(BP29>0,
IF(BY29>0, BX29*BY29^1.852,-BX29*ABS(BY29)^1.852),
IF(BY29>0, BX29*BT29^1.852, -BX29*BT29^1.852))` | =IF(BP29>0,
IF(BY29>0, BX29*BY29^1.852,-BX29*ABS(BY29)^1.852),
IF(BY29>0, BX29*BT29^1.852, -BX29*BT29^1.852)) |
| Ligne 29 | Col 79 | CA29 | `=1.852*BX29*ABS(BY29)^(1.852-1)` | =1.852*BX29*ABS(BY29)^(1.852-1) |
| Ligne 29 | Col 80 | CB29 | `=BY29+$BT$64` | =BY29+$BT$64 |
| Ligne 29 | Col 84 | CF29 | `=IFERROR(MATCH(CI29,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI29,$BS$22:$BS$62,0),0) |
| Ligne 29 | Col 86 | CH29 | `=DIST_PHASE_1_v2!BS18` | =DIST_PHASE_1_v2!BS18 |
| Ligne 29 | Col 87 | CI29 | `=DIST_PHASE_1_v2!BT18` | =DIST_PHASE_1_v2!BT18 |
| Ligne 29 | Col 88 | CJ29 | `=DIST_PHASE_1_v2!BV18` | =DIST_PHASE_1_v2!BV18 |
| Ligne 29 | Col 89 | CK29 | `=DIST_PHASE_1_v2!CA18` | =DIST_PHASE_1_v2!CA18 |
| Ligne 29 | Col 91 | CM29 | `=DIST_PHASE_1_v2!CC18` | =DIST_PHASE_1_v2!CC18 |
| Ligne 29 | Col 92 | CN29 | `= (10.679 * CM29) / ((CK29/1000)^4.871 * CL29^1.852)` | = (10.679 * CM29) / ((CK29/1000)^4.871 * CL29^1.852) |
| Ligne 29 | Col 93 | CO29 | `=IF(CH29="positif",CJ29,IF(CH29="negatif",-CJ29,""))` | =IF(CH29="positif",CJ29,IF(CH29="negatif",-CJ29,"")) |
| Ligne 29 | Col 94 | CP29 | `=IF(CF29>0,
IF(CO29>0, CN29*CO29^1.852,-CN29*ABS(CO29)^1.852),
IF(CO29>0, CN29*CJ29^1.852, -CN29*CJ29^1.852))` | =IF(CF29>0,
IF(CO29>0, CN29*CO29^1.852,-CN29*ABS(CO29)^1.852),
IF(CO29>0, CN29*CJ29^1.852, -CN29*CJ29^1.852)) |
| Ligne 29 | Col 95 | CQ29 | `=1.852*CN29*ABS(CO29)^(1.852-1)` | =1.852*CN29*ABS(CO29)^(1.852-1) |
| Ligne 29 | Col 96 | CR29 | `=CO29+$CJ$71` | =CO29+$CJ$71 |
| Ligne 29 | Col 100 | CV29 | `=IFERROR(MATCH(CY29,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY29,$CI$22:$CI$69,0),0) |
| Ligne 29 | Col 102 | CX29 | `=DIST_PHASE_1_v2!CF18` | =DIST_PHASE_1_v2!CF18 |
| Ligne 29 | Col 103 | CY29 | `=DIST_PHASE_1_v2!CG18` | =DIST_PHASE_1_v2!CG18 |
| Ligne 29 | Col 104 | CZ29 | `=DIST_PHASE_1_v2!CI18` | =DIST_PHASE_1_v2!CI18 |
| Ligne 29 | Col 105 | DA29 | `=DIST_PHASE_1_v2!CN18` | =DIST_PHASE_1_v2!CN18 |
| Ligne 29 | Col 106 | DB29 | `=DIST_PHASE_1_v2!CO18` | =DIST_PHASE_1_v2!CO18 |
| Ligne 29 | Col 107 | DC29 | `=DIST_PHASE_1_v2!CP18` | =DIST_PHASE_1_v2!CP18 |
| Ligne 29 | Col 108 | DD29 | `= (10.679 * DC29) / ((DA29/1000)^4.871 * DB29^1.852)` | = (10.679 * DC29) / ((DA29/1000)^4.871 * DB29^1.852) |
| Ligne 29 | Col 109 | DE29 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E4C50>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E4C50> |
| Ligne 29 | Col 110 | DF29 | `=IF(CV29>0,
IF(DE29>0, DD29*DE29^1.852,-DD29*ABS(DE29)^1.852),
IF(DE29>0, DD29*CZ29^1.852, -DD29*CZ29^1.852))` | =IF(CV29>0,
IF(DE29>0, DD29*DE29^1.852,-DD29*ABS(DE29)^1.852),
IF(DE29>0, DD29*CZ29^1.852, -DD29*CZ29^1.852)) |
| Ligne 29 | Col 111 | DG29 | `=1.852*DD29*ABS(DE29)^(1.852-1)` | =1.852*DD29*ABS(DE29)^(1.852-1) |
| Ligne 29 | Col 112 | DH29 | `=DE29+CZ63` | =DE29+CZ63 |
| Ligne 30 | Col 4 | D30 | `=DIST_PHASE_1_v2!E19` | =DIST_PHASE_1_v2!E19 |
| Ligne 30 | Col 5 | E30 | `=DIST_PHASE_1_v2!G19` | =DIST_PHASE_1_v2!G19 |
| Ligne 30 | Col 6 | F30 | `=DIST_PHASE_1_v2!L19` | =DIST_PHASE_1_v2!L19 |
| Ligne 30 | Col 7 | G30 | `=DIST_PHASE_1_v2!M19` | =DIST_PHASE_1_v2!M19 |
| Ligne 30 | Col 8 | H30 | `=DIST_PHASE_1_v2!N19` | =DIST_PHASE_1_v2!N19 |
| Ligne 30 | Col 9 | I30 | `= (10.679 * H30) / ((F30/1000)^4.871 * G30^1.852)` | = (10.679 * H30) / ((F30/1000)^4.871 * G30^1.852) |
| Ligne 30 | Col 10 | J30 | `=IF(C30="positif",E30,IF(C30="negatif",-E30,""))` | =IF(C30="positif",E30,IF(C30="negatif",-E30,"")) |
| Ligne 30 | Col 11 | K30 | `=IF(J30>0,I30*E30^1.852,-I30*E30^1.852)` | =IF(J30>0,I30*E30^1.852,-I30*E30^1.852) |
| Ligne 30 | Col 12 | L30 | `=1.852*I30*ABS(E30)^(1.852-1)` | =1.852*I30*ABS(E30)^(1.852-1) |
| Ligne 30 | Col 13 | M30 | `=J30+$D$93` | =J30+$D$93 |
| Ligne 30 | Col 16 | P30 | `=IFERROR(MATCH(S30,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S30,$D$22:$D$91,0),0) |
| Ligne 30 | Col 18 | R30 | `=DIST_PHASE_1_v2!Q19` | =DIST_PHASE_1_v2!Q19 |
| Ligne 30 | Col 19 | S30 | `=DIST_PHASE_1_v2!R19` | =DIST_PHASE_1_v2!R19 |
| Ligne 30 | Col 20 | T30 | `=DIST_PHASE_1_v2!T19` | =DIST_PHASE_1_v2!T19 |
| Ligne 30 | Col 21 | U30 | `=DIST_PHASE_1_v2!Y19` | =DIST_PHASE_1_v2!Y19 |
| Ligne 30 | Col 23 | W30 | `=DIST_PHASE_1_v2!AA19` | =DIST_PHASE_1_v2!AA19 |
| Ligne 30 | Col 24 | X30 | `= (10.679 * W30) / ((U30/1000)^4.871 * V30^1.852)` | = (10.679 * W30) / ((U30/1000)^4.871 * V30^1.852) |
| Ligne 30 | Col 25 | Y30 | `=IF(R30="positif",T30,IF(R30="negatif",-T30,""))` | =IF(R30="positif",T30,IF(R30="negatif",-T30,"")) |
| Ligne 30 | Col 26 | Z30 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82BB30>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD82BB30> |
| Ligne 30 | Col 27 | AA30 | `=IF(P30>0,
IF(R30="positif",1,-1),
0)` | =IF(P30>0,
IF(R30="positif",1,-1),
0) |
| Ligne 30 | Col 28 | AB30 | `=X30*SIGN(Y30)*ABS(Y30)^1.852` | =X30*SIGN(Y30)*ABS(Y30)^1.852 |
| Ligne 30 | Col 29 | AC30 | `=1.852*X30*ABS(Y30)^(1.852-1)` | =1.852*X30*ABS(Y30)^(1.852-1) |
| Ligne 30 | Col 30 | AD30 | `=IF(P30>0,
Y30+($D$93*Z30)+(AA30*$S$93),
Y30+$S$93)` | =IF(P30>0,
Y30+($D$93*Z30)+(AA30*$S$93),
Y30+$S$93) |
| Ligne 30 | Col 32 | AF30 | `=ABS(AD30)-ABS(Y30)` | =ABS(AD30)-ABS(Y30) |
| Ligne 30 | Col 36 | AJ30 | `=IFERROR(MATCH(AM30,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM30,$S$22:$S$91,0),0) |
| Ligne 30 | Col 38 | AL30 | `=TRONCONS_V2!AI17` | =TRONCONS_V2!AI17 |
| Ligne 30 | Col 39 | AM30 | `=TRONCONS_V2!AE17` | =TRONCONS_V2!AE17 |
| Ligne 30 | Col 40 | AN30 | `=DIST_PHASE_1_v2!AG19` | =DIST_PHASE_1_v2!AG19 |
| Ligne 30 | Col 41 | AO30 | `=DIST_PHASE_1_v2!AL19` | =DIST_PHASE_1_v2!AL19 |
| Ligne 30 | Col 43 | AQ30 | `=TRONCONS_V2!AG17` | =TRONCONS_V2!AG17 |
| Ligne 30 | Col 44 | AR30 | `= (10.679 * AQ30) / ((AO30/1000)^4.871 * AP30^1.852)` | = (10.679 * AQ30) / ((AO30/1000)^4.871 * AP30^1.852) |
| Ligne 30 | Col 45 | AS30 | `=IF(AL30="positif",AN30,IF(AL30="negatif",-AN30,""))` | =IF(AL30="positif",AN30,IF(AL30="negatif",-AN30,"")) |
| Ligne 30 | Col 46 | AT30 | `=IF(AJ30>0,
IF(AS30>0, AR30*AS30^1.852,-AR30*ABS(AS30)^1.852),
IF(AS30>0, AR30*AN30^1.852, -AR30*AN30^1.852))` | =IF(AJ30>0,
IF(AS30>0, AR30*AS30^1.852,-AR30*ABS(AS30)^1.852),
IF(AS30>0, AR30*AN30^1.852, -AR30*AN30^1.852)) |
| Ligne 30 | Col 47 | AU30 | `=1.852*AR30*ABS(AS30)^(1.852-1)` | =1.852*AR30*ABS(AS30)^(1.852-1) |
| Ligne 30 | Col 48 | AV30 | `=AS30+$AN$60` | =AS30+$AN$60 |
| Ligne 30 | Col 52 | AZ30 | `=IFERROR(MATCH(BC30,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC30,$AM$22:$AM$57,0),0) |
| Ligne 30 | Col 54 | BB30 | `=DIST_PHASE_1_v2!AQ19` | =DIST_PHASE_1_v2!AQ19 |
| Ligne 30 | Col 55 | BC30 | `=DIST_PHASE_1_v2!AR19` | =DIST_PHASE_1_v2!AR19 |
| Ligne 30 | Col 56 | BD30 | `=DIST_PHASE_1_v2!AT19` | =DIST_PHASE_1_v2!AT19 |
| Ligne 30 | Col 57 | BE30 | `=DIST_PHASE_1_v2!AY19` | =DIST_PHASE_1_v2!AY19 |
| Ligne 30 | Col 58 | BF30 | `=DIST_PHASE_1_v2!AZ19` | =DIST_PHASE_1_v2!AZ19 |
| Ligne 30 | Col 59 | BG30 | `=DIST_PHASE_1_v2!BA19` | =DIST_PHASE_1_v2!BA19 |
| Ligne 30 | Col 60 | BH30 | `= (10.679 * BG30) / ((BE30/1000)^4.871 * BF30^1.852)` | = (10.679 * BG30) / ((BE30/1000)^4.871 * BF30^1.852) |
| Ligne 30 | Col 61 | BI30 | `=IF(BB30="positif",BD30,IF(BB30="negatif",-BD30,""))` | =IF(BB30="positif",BD30,IF(BB30="negatif",-BD30,"")) |
| Ligne 30 | Col 62 | BJ30 | `=IF(AZ30>0,
IF(BI30>0, BH30*BI30^1.852,-BH30*ABS(BI30)^1.852),
IF(BI30>0, BH30*BD30^1.852, -BH30*BD30^1.852))` | =IF(AZ30>0,
IF(BI30>0, BH30*BI30^1.852,-BH30*ABS(BI30)^1.852),
IF(BI30>0, BH30*BD30^1.852, -BH30*BD30^1.852)) |
| Ligne 30 | Col 63 | BK30 | `=1.852*BH30*ABS(BI30)^(1.852-1)` | =1.852*BH30*ABS(BI30)^(1.852-1) |
| Ligne 30 | Col 64 | BL30 | `=BI30+$BD$75` | =BI30+$BD$75 |
| Ligne 30 | Col 68 | BP30 | `=IFERROR(MATCH(BS30,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS30,$BC$22:$BC$73,0),0) |
| Ligne 30 | Col 70 | BR30 | `=DIST_PHASE_1_v2!BF19` | =DIST_PHASE_1_v2!BF19 |
| Ligne 30 | Col 71 | BS30 | `=DIST_PHASE_1_v2!BG19` | =DIST_PHASE_1_v2!BG19 |
| Ligne 30 | Col 72 | BT30 | `=DIST_PHASE_1_v2!BI19` | =DIST_PHASE_1_v2!BI19 |
| Ligne 30 | Col 73 | BU30 | `=DIST_PHASE_1_v2!BN19` | =DIST_PHASE_1_v2!BN19 |
| Ligne 30 | Col 74 | BV30 | `=DIST_PHASE_1_v2!BO19` | =DIST_PHASE_1_v2!BO19 |
| Ligne 30 | Col 75 | BW30 | `=DIST_PHASE_1_v2!BP19` | =DIST_PHASE_1_v2!BP19 |
| Ligne 30 | Col 76 | BX30 | `= (10.679 * BW30) / ((BU30/1000)^4.871 * BV30^1.852)` | = (10.679 * BW30) / ((BU30/1000)^4.871 * BV30^1.852) |
| Ligne 30 | Col 77 | BY30 | `=IF(BR30="positif",BT30,IF(BR30="negatif",-BT30,""))` | =IF(BR30="positif",BT30,IF(BR30="negatif",-BT30,"")) |
| Ligne 30 | Col 78 | BZ30 | `=IF(BP30>0,
IF(BY30>0, BX30*BY30^1.852,-BX30*ABS(BY30)^1.852),
IF(BY30>0, BX30*BT30^1.852, -BX30*BT30^1.852))` | =IF(BP30>0,
IF(BY30>0, BX30*BY30^1.852,-BX30*ABS(BY30)^1.852),
IF(BY30>0, BX30*BT30^1.852, -BX30*BT30^1.852)) |
| Ligne 30 | Col 79 | CA30 | `=1.852*BX30*ABS(BY30)^(1.852-1)` | =1.852*BX30*ABS(BY30)^(1.852-1) |
| Ligne 30 | Col 80 | CB30 | `=BY30+$BT$64` | =BY30+$BT$64 |
| Ligne 30 | Col 84 | CF30 | `=IFERROR(MATCH(CI30,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI30,$BS$22:$BS$62,0),0) |
| Ligne 30 | Col 86 | CH30 | `=DIST_PHASE_1_v2!BS19` | =DIST_PHASE_1_v2!BS19 |
| Ligne 30 | Col 87 | CI30 | `=DIST_PHASE_1_v2!BT19` | =DIST_PHASE_1_v2!BT19 |
| Ligne 30 | Col 88 | CJ30 | `=DIST_PHASE_1_v2!BV19` | =DIST_PHASE_1_v2!BV19 |
| Ligne 30 | Col 89 | CK30 | `=DIST_PHASE_1_v2!CA19` | =DIST_PHASE_1_v2!CA19 |
| Ligne 30 | Col 91 | CM30 | `=DIST_PHASE_1_v2!CC19` | =DIST_PHASE_1_v2!CC19 |
| Ligne 30 | Col 92 | CN30 | `= (10.679 * CM30) / ((CK30/1000)^4.871 * CL30^1.852)` | = (10.679 * CM30) / ((CK30/1000)^4.871 * CL30^1.852) |
| Ligne 30 | Col 93 | CO30 | `=IF(CH30="positif",CJ30,IF(CH30="negatif",-CJ30,""))` | =IF(CH30="positif",CJ30,IF(CH30="negatif",-CJ30,"")) |
| Ligne 30 | Col 94 | CP30 | `=IF(CF30>0,
IF(CO30>0, CN30*CO30^1.852,-CN30*ABS(CO30)^1.852),
IF(CO30>0, CN30*CJ30^1.852, -CN30*CJ30^1.852))` | =IF(CF30>0,
IF(CO30>0, CN30*CO30^1.852,-CN30*ABS(CO30)^1.852),
IF(CO30>0, CN30*CJ30^1.852, -CN30*CJ30^1.852)) |
| Ligne 30 | Col 95 | CQ30 | `=1.852*CN30*ABS(CO30)^(1.852-1)` | =1.852*CN30*ABS(CO30)^(1.852-1) |
| Ligne 30 | Col 96 | CR30 | `=CO30+$CJ$71` | =CO30+$CJ$71 |
| Ligne 30 | Col 100 | CV30 | `=IFERROR(MATCH(CY30,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY30,$CI$22:$CI$69,0),0) |
| Ligne 30 | Col 102 | CX30 | `=DIST_PHASE_1_v2!CF19` | =DIST_PHASE_1_v2!CF19 |
| Ligne 30 | Col 103 | CY30 | `=DIST_PHASE_1_v2!CG19` | =DIST_PHASE_1_v2!CG19 |
| Ligne 30 | Col 104 | CZ30 | `=DIST_PHASE_1_v2!CI19` | =DIST_PHASE_1_v2!CI19 |
| Ligne 30 | Col 105 | DA30 | `=DIST_PHASE_1_v2!CN19` | =DIST_PHASE_1_v2!CN19 |
| Ligne 30 | Col 106 | DB30 | `=DIST_PHASE_1_v2!CO19` | =DIST_PHASE_1_v2!CO19 |
| Ligne 30 | Col 107 | DC30 | `=DIST_PHASE_1_v2!CP19` | =DIST_PHASE_1_v2!CP19 |
| Ligne 30 | Col 108 | DD30 | `= (10.679 * DC30) / ((DA30/1000)^4.871 * DB30^1.852)` | = (10.679 * DC30) / ((DA30/1000)^4.871 * DB30^1.852) |
| Ligne 30 | Col 109 | DE30 | `=IF(CX30="positif",CZ30,IF(CX30="negatif",-CZ30,""))` | =IF(CX30="positif",CZ30,IF(CX30="negatif",-CZ30,"")) |
| Ligne 30 | Col 110 | DF30 | `=IF(CV30>0,
IF(DE30>0, DD30*DE30^1.852,-DD30*ABS(DE30)^1.852),
IF(DE30>0, DD30*CZ30^1.852, -DD30*CZ30^1.852))` | =IF(CV30>0,
IF(DE30>0, DD30*DE30^1.852,-DD30*ABS(DE30)^1.852),
IF(DE30>0, DD30*CZ30^1.852, -DD30*CZ30^1.852)) |
| Ligne 30 | Col 111 | DG30 | `=1.852*DD30*ABS(DE30)^(1.852-1)` | =1.852*DD30*ABS(DE30)^(1.852-1) |
| Ligne 30 | Col 112 | DH30 | `=DE30+CZ64` | =DE30+CZ64 |
| Ligne 31 | Col 4 | D31 | `=DIST_PHASE_1_v2!E20` | =DIST_PHASE_1_v2!E20 |
| Ligne 31 | Col 5 | E31 | `=DIST_PHASE_1_v2!G20` | =DIST_PHASE_1_v2!G20 |
| Ligne 31 | Col 6 | F31 | `=DIST_PHASE_1_v2!L20` | =DIST_PHASE_1_v2!L20 |
| Ligne 31 | Col 7 | G31 | `=DIST_PHASE_1_v2!M20` | =DIST_PHASE_1_v2!M20 |
| Ligne 31 | Col 8 | H31 | `=DIST_PHASE_1_v2!N20` | =DIST_PHASE_1_v2!N20 |
| Ligne 31 | Col 9 | I31 | `= (10.679 * H31) / ((F31/1000)^4.871 * G31^1.852)` | = (10.679 * H31) / ((F31/1000)^4.871 * G31^1.852) |
| Ligne 31 | Col 10 | J31 | `=IF(C31="positif",E31,IF(C31="negatif",-E31,""))` | =IF(C31="positif",E31,IF(C31="negatif",-E31,"")) |
| Ligne 31 | Col 11 | K31 | `=IF(J31>0,I31*E31^1.852,-I31*E31^1.852)` | =IF(J31>0,I31*E31^1.852,-I31*E31^1.852) |
| Ligne 31 | Col 12 | L31 | `=1.852*I31*ABS(E31)^(1.852-1)` | =1.852*I31*ABS(E31)^(1.852-1) |
| Ligne 31 | Col 13 | M31 | `=J31+$D$93` | =J31+$D$93 |
| Ligne 31 | Col 16 | P31 | `=IFERROR(MATCH(S31,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S31,$D$22:$D$91,0),0) |
| Ligne 31 | Col 18 | R31 | `=DIST_PHASE_1_v2!Q20` | =DIST_PHASE_1_v2!Q20 |
| Ligne 31 | Col 19 | S31 | `=DIST_PHASE_1_v2!R20` | =DIST_PHASE_1_v2!R20 |
| Ligne 31 | Col 20 | T31 | `=DIST_PHASE_1_v2!T20` | =DIST_PHASE_1_v2!T20 |
| Ligne 31 | Col 21 | U31 | `=DIST_PHASE_1_v2!Y20` | =DIST_PHASE_1_v2!Y20 |
| Ligne 31 | Col 23 | W31 | `=DIST_PHASE_1_v2!AA20` | =DIST_PHASE_1_v2!AA20 |
| Ligne 31 | Col 24 | X31 | `= (10.679 * W31) / ((U31/1000)^4.871 * V31^1.852)` | = (10.679 * W31) / ((U31/1000)^4.871 * V31^1.852) |
| Ligne 31 | Col 25 | Y31 | `=IF(R31="positif",T31,IF(R31="negatif",-T31,""))` | =IF(R31="positif",T31,IF(R31="negatif",-T31,"")) |
| Ligne 31 | Col 26 | Z31 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E4CB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E4CB0> |
| Ligne 31 | Col 27 | AA31 | `=IF(P31>0,
IF(R31="positif",1,-1),
0)` | =IF(P31>0,
IF(R31="positif",1,-1),
0) |
| Ligne 31 | Col 28 | AB31 | `=X31*SIGN(Y31)*ABS(Y31)^1.852` | =X31*SIGN(Y31)*ABS(Y31)^1.852 |
| Ligne 31 | Col 29 | AC31 | `=1.852*X31*ABS(Y31)^(1.852-1)` | =1.852*X31*ABS(Y31)^(1.852-1) |
| Ligne 31 | Col 30 | AD31 | `=IF(P31>0,
Y31+($D$93*Z31)+(AA31*$S$93),
Y31+$S$93)` | =IF(P31>0,
Y31+($D$93*Z31)+(AA31*$S$93),
Y31+$S$93) |
| Ligne 31 | Col 32 | AF31 | `=ABS(AD31)-ABS(Y31)` | =ABS(AD31)-ABS(Y31) |
| Ligne 31 | Col 36 | AJ31 | `=IFERROR(MATCH(AM31,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM31,$S$22:$S$91,0),0) |
| Ligne 31 | Col 38 | AL31 | `=TRONCONS_V2!AI18` | =TRONCONS_V2!AI18 |
| Ligne 31 | Col 39 | AM31 | `=TRONCONS_V2!AE18` | =TRONCONS_V2!AE18 |
| Ligne 31 | Col 40 | AN31 | `=DIST_PHASE_1_v2!AG20` | =DIST_PHASE_1_v2!AG20 |
| Ligne 31 | Col 41 | AO31 | `=DIST_PHASE_1_v2!AL20` | =DIST_PHASE_1_v2!AL20 |
| Ligne 31 | Col 43 | AQ31 | `=TRONCONS_V2!AG18` | =TRONCONS_V2!AG18 |
| Ligne 31 | Col 44 | AR31 | `= (10.679 * AQ31) / ((AO31/1000)^4.871 * AP31^1.852)` | = (10.679 * AQ31) / ((AO31/1000)^4.871 * AP31^1.852) |
| Ligne 31 | Col 45 | AS31 | `=IF(AL31="positif",AN31,IF(AL31="negatif",-AN31,""))` | =IF(AL31="positif",AN31,IF(AL31="negatif",-AN31,"")) |
| Ligne 31 | Col 46 | AT31 | `=IF(AJ31>0,
IF(AS31>0, AR31*AS31^1.852,-AR31*ABS(AS31)^1.852),
IF(AS31>0, AR31*AN31^1.852, -AR31*AN31^1.852))` | =IF(AJ31>0,
IF(AS31>0, AR31*AS31^1.852,-AR31*ABS(AS31)^1.852),
IF(AS31>0, AR31*AN31^1.852, -AR31*AN31^1.852)) |
| Ligne 31 | Col 47 | AU31 | `=1.852*AR31*ABS(AS31)^(1.852-1)` | =1.852*AR31*ABS(AS31)^(1.852-1) |
| Ligne 31 | Col 48 | AV31 | `=AS31+$AN$60` | =AS31+$AN$60 |
| Ligne 31 | Col 52 | AZ31 | `=IFERROR(MATCH(BC31,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC31,$AM$22:$AM$57,0),0) |
| Ligne 31 | Col 54 | BB31 | `=DIST_PHASE_1_v2!AQ20` | =DIST_PHASE_1_v2!AQ20 |
| Ligne 31 | Col 55 | BC31 | `=DIST_PHASE_1_v2!AR20` | =DIST_PHASE_1_v2!AR20 |
| Ligne 31 | Col 56 | BD31 | `=DIST_PHASE_1_v2!AT20` | =DIST_PHASE_1_v2!AT20 |
| Ligne 31 | Col 57 | BE31 | `=DIST_PHASE_1_v2!AY20` | =DIST_PHASE_1_v2!AY20 |
| Ligne 31 | Col 58 | BF31 | `=DIST_PHASE_1_v2!AZ20` | =DIST_PHASE_1_v2!AZ20 |
| Ligne 31 | Col 59 | BG31 | `=DIST_PHASE_1_v2!BA20` | =DIST_PHASE_1_v2!BA20 |
| Ligne 31 | Col 60 | BH31 | `= (10.679 * BG31) / ((BE31/1000)^4.871 * BF31^1.852)` | = (10.679 * BG31) / ((BE31/1000)^4.871 * BF31^1.852) |
| Ligne 31 | Col 61 | BI31 | `=IF(BB31="positif",BD31,IF(BB31="negatif",-BD31,""))` | =IF(BB31="positif",BD31,IF(BB31="negatif",-BD31,"")) |
| Ligne 31 | Col 62 | BJ31 | `=IF(AZ31>0,
IF(BI31>0, BH31*BI31^1.852,-BH31*ABS(BI31)^1.852),
IF(BI31>0, BH31*BD31^1.852, -BH31*BD31^1.852))` | =IF(AZ31>0,
IF(BI31>0, BH31*BI31^1.852,-BH31*ABS(BI31)^1.852),
IF(BI31>0, BH31*BD31^1.852, -BH31*BD31^1.852)) |
| Ligne 31 | Col 63 | BK31 | `=1.852*BH31*ABS(BI31)^(1.852-1)` | =1.852*BH31*ABS(BI31)^(1.852-1) |
| Ligne 31 | Col 64 | BL31 | `=BI31+$BD$75` | =BI31+$BD$75 |
| Ligne 31 | Col 68 | BP31 | `=IFERROR(MATCH(BS31,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS31,$BC$22:$BC$73,0),0) |
| Ligne 31 | Col 70 | BR31 | `=DIST_PHASE_1_v2!BF20` | =DIST_PHASE_1_v2!BF20 |
| Ligne 31 | Col 71 | BS31 | `=DIST_PHASE_1_v2!BG20` | =DIST_PHASE_1_v2!BG20 |
| Ligne 31 | Col 72 | BT31 | `=DIST_PHASE_1_v2!BI20` | =DIST_PHASE_1_v2!BI20 |
| Ligne 31 | Col 73 | BU31 | `=DIST_PHASE_1_v2!BN20` | =DIST_PHASE_1_v2!BN20 |
| Ligne 31 | Col 74 | BV31 | `=DIST_PHASE_1_v2!BO20` | =DIST_PHASE_1_v2!BO20 |
| Ligne 31 | Col 75 | BW31 | `=DIST_PHASE_1_v2!BP20` | =DIST_PHASE_1_v2!BP20 |
| Ligne 31 | Col 76 | BX31 | `= (10.679 * BW31) / ((BU31/1000)^4.871 * BV31^1.852)` | = (10.679 * BW31) / ((BU31/1000)^4.871 * BV31^1.852) |
| Ligne 31 | Col 77 | BY31 | `=IF(BR31="positif",BT31,IF(BR31="negatif",-BT31,""))` | =IF(BR31="positif",BT31,IF(BR31="negatif",-BT31,"")) |
| Ligne 31 | Col 78 | BZ31 | `=IF(BP31>0,
IF(BY31>0, BX31*BY31^1.852,-BX31*ABS(BY31)^1.852),
IF(BY31>0, BX31*BT31^1.852, -BX31*BT31^1.852))` | =IF(BP31>0,
IF(BY31>0, BX31*BY31^1.852,-BX31*ABS(BY31)^1.852),
IF(BY31>0, BX31*BT31^1.852, -BX31*BT31^1.852)) |
| Ligne 31 | Col 79 | CA31 | `=1.852*BX31*ABS(BY31)^(1.852-1)` | =1.852*BX31*ABS(BY31)^(1.852-1) |
| Ligne 31 | Col 80 | CB31 | `=BY31+$BT$64` | =BY31+$BT$64 |
| Ligne 31 | Col 84 | CF31 | `=IFERROR(MATCH(CI31,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI31,$BS$22:$BS$62,0),0) |
| Ligne 31 | Col 86 | CH31 | `=DIST_PHASE_1_v2!BS20` | =DIST_PHASE_1_v2!BS20 |
| Ligne 31 | Col 87 | CI31 | `=DIST_PHASE_1_v2!BT20` | =DIST_PHASE_1_v2!BT20 |
| Ligne 31 | Col 88 | CJ31 | `=DIST_PHASE_1_v2!BV20` | =DIST_PHASE_1_v2!BV20 |
| Ligne 31 | Col 89 | CK31 | `=DIST_PHASE_1_v2!CA20` | =DIST_PHASE_1_v2!CA20 |
| Ligne 31 | Col 91 | CM31 | `=DIST_PHASE_1_v2!CC20` | =DIST_PHASE_1_v2!CC20 |
| Ligne 31 | Col 92 | CN31 | `= (10.679 * CM31) / ((CK31/1000)^4.871 * CL31^1.852)` | = (10.679 * CM31) / ((CK31/1000)^4.871 * CL31^1.852) |
| Ligne 31 | Col 93 | CO31 | `=IF(CH31="positif",CJ31,IF(CH31="negatif",-CJ31,""))` | =IF(CH31="positif",CJ31,IF(CH31="negatif",-CJ31,"")) |
| Ligne 31 | Col 94 | CP31 | `=IF(CF31>0,
IF(CO31>0, CN31*CO31^1.852,-CN31*ABS(CO31)^1.852),
IF(CO31>0, CN31*CJ31^1.852, -CN31*CJ31^1.852))` | =IF(CF31>0,
IF(CO31>0, CN31*CO31^1.852,-CN31*ABS(CO31)^1.852),
IF(CO31>0, CN31*CJ31^1.852, -CN31*CJ31^1.852)) |
| Ligne 31 | Col 95 | CQ31 | `=1.852*CN31*ABS(CO31)^(1.852-1)` | =1.852*CN31*ABS(CO31)^(1.852-1) |
| Ligne 31 | Col 96 | CR31 | `=CO31+$CJ$71` | =CO31+$CJ$71 |
| Ligne 31 | Col 100 | CV31 | `=IFERROR(MATCH(CY31,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY31,$CI$22:$CI$69,0),0) |
| Ligne 31 | Col 102 | CX31 | `=DIST_PHASE_1_v2!CF20` | =DIST_PHASE_1_v2!CF20 |
| Ligne 31 | Col 103 | CY31 | `=DIST_PHASE_1_v2!CG20` | =DIST_PHASE_1_v2!CG20 |
| Ligne 31 | Col 104 | CZ31 | `=DIST_PHASE_1_v2!CI20` | =DIST_PHASE_1_v2!CI20 |
| Ligne 31 | Col 105 | DA31 | `=DIST_PHASE_1_v2!CN20` | =DIST_PHASE_1_v2!CN20 |
| Ligne 31 | Col 106 | DB31 | `=DIST_PHASE_1_v2!CO20` | =DIST_PHASE_1_v2!CO20 |
| Ligne 31 | Col 107 | DC31 | `=DIST_PHASE_1_v2!CP20` | =DIST_PHASE_1_v2!CP20 |
| Ligne 31 | Col 108 | DD31 | `= (10.679 * DC31) / ((DA31/1000)^4.871 * DB31^1.852)` | = (10.679 * DC31) / ((DA31/1000)^4.871 * DB31^1.852) |
| Ligne 31 | Col 109 | DE31 | `=IF(CX31="positif",CZ31,IF(CX31="negatif",-CZ31,""))` | =IF(CX31="positif",CZ31,IF(CX31="negatif",-CZ31,"")) |
| Ligne 31 | Col 110 | DF31 | `=IF(CV31>0,
IF(DE31>0, DD31*DE31^1.852,-DD31*ABS(DE31)^1.852),
IF(DE31>0, DD31*CZ31^1.852, -DD31*CZ31^1.852))` | =IF(CV31>0,
IF(DE31>0, DD31*DE31^1.852,-DD31*ABS(DE31)^1.852),
IF(DE31>0, DD31*CZ31^1.852, -DD31*CZ31^1.852)) |
| Ligne 31 | Col 111 | DG31 | `=1.852*DD31*ABS(DE31)^(1.852-1)` | =1.852*DD31*ABS(DE31)^(1.852-1) |
| Ligne 31 | Col 112 | DH31 | `=DE31+CZ65` | =DE31+CZ65 |
| Ligne 32 | Col 4 | D32 | `=DIST_PHASE_1_v2!E21` | =DIST_PHASE_1_v2!E21 |
| Ligne 32 | Col 5 | E32 | `=DIST_PHASE_1_v2!G21` | =DIST_PHASE_1_v2!G21 |
| Ligne 32 | Col 6 | F32 | `=DIST_PHASE_1_v2!L21` | =DIST_PHASE_1_v2!L21 |
| Ligne 32 | Col 7 | G32 | `=DIST_PHASE_1_v2!M21` | =DIST_PHASE_1_v2!M21 |
| Ligne 32 | Col 8 | H32 | `=DIST_PHASE_1_v2!N21` | =DIST_PHASE_1_v2!N21 |
| Ligne 32 | Col 9 | I32 | `= (10.679 * H32) / ((F32/1000)^4.871 * G32^1.852)` | = (10.679 * H32) / ((F32/1000)^4.871 * G32^1.852) |
| Ligne 32 | Col 10 | J32 | `=IF(C32="positif",E32,IF(C32="negatif",-E32,""))` | =IF(C32="positif",E32,IF(C32="negatif",-E32,"")) |
| Ligne 32 | Col 11 | K32 | `=IF(J32>0,I32*E32^1.852,-I32*E32^1.852)` | =IF(J32>0,I32*E32^1.852,-I32*E32^1.852) |
| Ligne 32 | Col 12 | L32 | `=1.852*I32*ABS(E32)^(1.852-1)` | =1.852*I32*ABS(E32)^(1.852-1) |
| Ligne 32 | Col 13 | M32 | `=J32+$D$93` | =J32+$D$93 |
| Ligne 32 | Col 16 | P32 | `=IFERROR(MATCH(S32,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S32,$D$22:$D$91,0),0) |
| Ligne 32 | Col 18 | R32 | `=DIST_PHASE_1_v2!Q21` | =DIST_PHASE_1_v2!Q21 |
| Ligne 32 | Col 19 | S32 | `=DIST_PHASE_1_v2!R21` | =DIST_PHASE_1_v2!R21 |
| Ligne 32 | Col 20 | T32 | `=DIST_PHASE_1_v2!T21` | =DIST_PHASE_1_v2!T21 |
| Ligne 32 | Col 21 | U32 | `=DIST_PHASE_1_v2!Y21` | =DIST_PHASE_1_v2!Y21 |
| Ligne 32 | Col 23 | W32 | `=DIST_PHASE_1_v2!AA21` | =DIST_PHASE_1_v2!AA21 |
| Ligne 32 | Col 24 | X32 | `= (10.679 * W32) / ((U32/1000)^4.871 * V32^1.852)` | = (10.679 * W32) / ((U32/1000)^4.871 * V32^1.852) |
| Ligne 32 | Col 25 | Y32 | `=IF(R32="positif",T32,IF(R32="negatif",-T32,""))` | =IF(R32="positif",T32,IF(R32="negatif",-T32,"")) |
| Ligne 32 | Col 26 | Z32 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E4D10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E4D10> |
| Ligne 32 | Col 27 | AA32 | `=IF(P32>0,
IF(R32="positif",1,-1),
0)` | =IF(P32>0,
IF(R32="positif",1,-1),
0) |
| Ligne 32 | Col 28 | AB32 | `=X32*SIGN(Y32)*ABS(Y32)^1.852` | =X32*SIGN(Y32)*ABS(Y32)^1.852 |
| Ligne 32 | Col 29 | AC32 | `=1.852*X32*ABS(Y32)^(1.852-1)` | =1.852*X32*ABS(Y32)^(1.852-1) |
| Ligne 32 | Col 30 | AD32 | `=IF(P32>0,
Y32+($D$93*Z32)+(AA32*$S$93),
Y32+$S$93)` | =IF(P32>0,
Y32+($D$93*Z32)+(AA32*$S$93),
Y32+$S$93) |
| Ligne 32 | Col 32 | AF32 | `=ABS(AD32)-ABS(Y32)` | =ABS(AD32)-ABS(Y32) |
| Ligne 32 | Col 36 | AJ32 | `=IFERROR(MATCH(AM32,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM32,$S$22:$S$91,0),0) |
| Ligne 32 | Col 38 | AL32 | `=TRONCONS_V2!AI19` | =TRONCONS_V2!AI19 |
| Ligne 32 | Col 39 | AM32 | `=TRONCONS_V2!AE19` | =TRONCONS_V2!AE19 |
| Ligne 32 | Col 40 | AN32 | `=DIST_PHASE_1_v2!AG21` | =DIST_PHASE_1_v2!AG21 |
| Ligne 32 | Col 41 | AO32 | `=DIST_PHASE_1_v2!AL21` | =DIST_PHASE_1_v2!AL21 |
| Ligne 32 | Col 43 | AQ32 | `=TRONCONS_V2!AG19` | =TRONCONS_V2!AG19 |
| Ligne 32 | Col 44 | AR32 | `= (10.679 * AQ32) / ((AO32/1000)^4.871 * AP32^1.852)` | = (10.679 * AQ32) / ((AO32/1000)^4.871 * AP32^1.852) |
| Ligne 32 | Col 45 | AS32 | `=IF(AL32="positif",AN32,IF(AL32="negatif",-AN32,""))` | =IF(AL32="positif",AN32,IF(AL32="negatif",-AN32,"")) |
| Ligne 32 | Col 46 | AT32 | `=IF(AJ32>0,
IF(AS32>0, AR32*AS32^1.852,-AR32*ABS(AS32)^1.852),
IF(AS32>0, AR32*AN32^1.852, -AR32*AN32^1.852))` | =IF(AJ32>0,
IF(AS32>0, AR32*AS32^1.852,-AR32*ABS(AS32)^1.852),
IF(AS32>0, AR32*AN32^1.852, -AR32*AN32^1.852)) |
| Ligne 32 | Col 47 | AU32 | `=1.852*AR32*ABS(AS32)^(1.852-1)` | =1.852*AR32*ABS(AS32)^(1.852-1) |
| Ligne 32 | Col 48 | AV32 | `=AS32+$AN$60` | =AS32+$AN$60 |
| Ligne 32 | Col 52 | AZ32 | `=IFERROR(MATCH(BC32,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC32,$AM$22:$AM$57,0),0) |
| Ligne 32 | Col 54 | BB32 | `=DIST_PHASE_1_v2!AQ21` | =DIST_PHASE_1_v2!AQ21 |
| Ligne 32 | Col 55 | BC32 | `=DIST_PHASE_1_v2!AR21` | =DIST_PHASE_1_v2!AR21 |
| Ligne 32 | Col 56 | BD32 | `=DIST_PHASE_1_v2!AT21` | =DIST_PHASE_1_v2!AT21 |
| Ligne 32 | Col 57 | BE32 | `=DIST_PHASE_1_v2!AY21` | =DIST_PHASE_1_v2!AY21 |
| Ligne 32 | Col 58 | BF32 | `=DIST_PHASE_1_v2!AZ21` | =DIST_PHASE_1_v2!AZ21 |
| Ligne 32 | Col 59 | BG32 | `=DIST_PHASE_1_v2!BA21` | =DIST_PHASE_1_v2!BA21 |
| Ligne 32 | Col 60 | BH32 | `= (10.679 * BG32) / ((BE32/1000)^4.871 * BF32^1.852)` | = (10.679 * BG32) / ((BE32/1000)^4.871 * BF32^1.852) |
| Ligne 32 | Col 61 | BI32 | `=IF(BB32="positif",BD32,IF(BB32="negatif",-BD32,""))` | =IF(BB32="positif",BD32,IF(BB32="negatif",-BD32,"")) |
| Ligne 32 | Col 62 | BJ32 | `=IF(AZ32>0,
IF(BI32>0, BH32*BI32^1.852,-BH32*ABS(BI32)^1.852),
IF(BI32>0, BH32*BD32^1.852, -BH32*BD32^1.852))` | =IF(AZ32>0,
IF(BI32>0, BH32*BI32^1.852,-BH32*ABS(BI32)^1.852),
IF(BI32>0, BH32*BD32^1.852, -BH32*BD32^1.852)) |
| Ligne 32 | Col 63 | BK32 | `=1.852*BH32*ABS(BI32)^(1.852-1)` | =1.852*BH32*ABS(BI32)^(1.852-1) |
| Ligne 32 | Col 64 | BL32 | `=BI32+$BD$75` | =BI32+$BD$75 |
| Ligne 32 | Col 68 | BP32 | `=IFERROR(MATCH(BS32,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS32,$BC$22:$BC$73,0),0) |
| Ligne 32 | Col 70 | BR32 | `=DIST_PHASE_1_v2!BF21` | =DIST_PHASE_1_v2!BF21 |
| Ligne 32 | Col 71 | BS32 | `=DIST_PHASE_1_v2!BG21` | =DIST_PHASE_1_v2!BG21 |
| Ligne 32 | Col 72 | BT32 | `=DIST_PHASE_1_v2!BI21` | =DIST_PHASE_1_v2!BI21 |
| Ligne 32 | Col 73 | BU32 | `=DIST_PHASE_1_v2!BN21` | =DIST_PHASE_1_v2!BN21 |
| Ligne 32 | Col 74 | BV32 | `=DIST_PHASE_1_v2!BO21` | =DIST_PHASE_1_v2!BO21 |
| Ligne 32 | Col 75 | BW32 | `=DIST_PHASE_1_v2!BP21` | =DIST_PHASE_1_v2!BP21 |
| Ligne 32 | Col 76 | BX32 | `= (10.679 * BW32) / ((BU32/1000)^4.871 * BV32^1.852)` | = (10.679 * BW32) / ((BU32/1000)^4.871 * BV32^1.852) |
| Ligne 32 | Col 77 | BY32 | `=IF(BR32="positif",BT32,IF(BR32="negatif",-BT32,""))` | =IF(BR32="positif",BT32,IF(BR32="negatif",-BT32,"")) |
| Ligne 32 | Col 78 | BZ32 | `=IF(BP32>0,
IF(BY32>0, BX32*BY32^1.852,-BX32*ABS(BY32)^1.852),
IF(BY32>0, BX32*BT32^1.852, -BX32*BT32^1.852))` | =IF(BP32>0,
IF(BY32>0, BX32*BY32^1.852,-BX32*ABS(BY32)^1.852),
IF(BY32>0, BX32*BT32^1.852, -BX32*BT32^1.852)) |
| Ligne 32 | Col 79 | CA32 | `=1.852*BX32*ABS(BY32)^(1.852-1)` | =1.852*BX32*ABS(BY32)^(1.852-1) |
| Ligne 32 | Col 80 | CB32 | `=BY32+$BT$64` | =BY32+$BT$64 |
| Ligne 32 | Col 84 | CF32 | `=IFERROR(MATCH(CI32,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI32,$BS$22:$BS$62,0),0) |
| Ligne 32 | Col 86 | CH32 | `=DIST_PHASE_1_v2!BS21` | =DIST_PHASE_1_v2!BS21 |
| Ligne 32 | Col 87 | CI32 | `=DIST_PHASE_1_v2!BT21` | =DIST_PHASE_1_v2!BT21 |
| Ligne 32 | Col 88 | CJ32 | `=DIST_PHASE_1_v2!BV21` | =DIST_PHASE_1_v2!BV21 |
| Ligne 32 | Col 89 | CK32 | `=DIST_PHASE_1_v2!CA21` | =DIST_PHASE_1_v2!CA21 |
| Ligne 32 | Col 91 | CM32 | `=DIST_PHASE_1_v2!CC21` | =DIST_PHASE_1_v2!CC21 |
| Ligne 32 | Col 92 | CN32 | `= (10.679 * CM32) / ((CK32/1000)^4.871 * CL32^1.852)` | = (10.679 * CM32) / ((CK32/1000)^4.871 * CL32^1.852) |
| Ligne 32 | Col 93 | CO32 | `=IF(CH32="positif",CJ32,IF(CH32="negatif",-CJ32,""))` | =IF(CH32="positif",CJ32,IF(CH32="negatif",-CJ32,"")) |
| Ligne 32 | Col 94 | CP32 | `=IF(CF32>0,
IF(CO32>0, CN32*CO32^1.852,-CN32*ABS(CO32)^1.852),
IF(CO32>0, CN32*CJ32^1.852, -CN32*CJ32^1.852))` | =IF(CF32>0,
IF(CO32>0, CN32*CO32^1.852,-CN32*ABS(CO32)^1.852),
IF(CO32>0, CN32*CJ32^1.852, -CN32*CJ32^1.852)) |
| Ligne 32 | Col 95 | CQ32 | `=1.852*CN32*ABS(CO32)^(1.852-1)` | =1.852*CN32*ABS(CO32)^(1.852-1) |
| Ligne 32 | Col 96 | CR32 | `=CO32+$CJ$71` | =CO32+$CJ$71 |
| Ligne 32 | Col 100 | CV32 | `=IFERROR(MATCH(CY32,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY32,$CI$22:$CI$69,0),0) |
| Ligne 32 | Col 102 | CX32 | `=DIST_PHASE_1_v2!CF21` | =DIST_PHASE_1_v2!CF21 |
| Ligne 32 | Col 103 | CY32 | `=DIST_PHASE_1_v2!CG21` | =DIST_PHASE_1_v2!CG21 |
| Ligne 32 | Col 104 | CZ32 | `=DIST_PHASE_1_v2!CI21` | =DIST_PHASE_1_v2!CI21 |
| Ligne 32 | Col 105 | DA32 | `=DIST_PHASE_1_v2!CN21` | =DIST_PHASE_1_v2!CN21 |
| Ligne 32 | Col 106 | DB32 | `=DIST_PHASE_1_v2!CO21` | =DIST_PHASE_1_v2!CO21 |
| Ligne 32 | Col 107 | DC32 | `=DIST_PHASE_1_v2!CP21` | =DIST_PHASE_1_v2!CP21 |
| Ligne 32 | Col 108 | DD32 | `= (10.679 * DC32) / ((DA32/1000)^4.871 * DB32^1.852)` | = (10.679 * DC32) / ((DA32/1000)^4.871 * DB32^1.852) |
| Ligne 32 | Col 109 | DE32 | `=IF(CX32="positif",CZ32,IF(CX32="negatif",-CZ32,""))` | =IF(CX32="positif",CZ32,IF(CX32="negatif",-CZ32,"")) |
| Ligne 32 | Col 110 | DF32 | `=IF(CV32>0,
IF(DE32>0, DD32*DE32^1.852,-DD32*ABS(DE32)^1.852),
IF(DE32>0, DD32*CZ32^1.852, -DD32*CZ32^1.852))` | =IF(CV32>0,
IF(DE32>0, DD32*DE32^1.852,-DD32*ABS(DE32)^1.852),
IF(DE32>0, DD32*CZ32^1.852, -DD32*CZ32^1.852)) |
| Ligne 32 | Col 111 | DG32 | `=1.852*DD32*ABS(DE32)^(1.852-1)` | =1.852*DD32*ABS(DE32)^(1.852-1) |
| Ligne 32 | Col 112 | DH32 | `=DE32+CZ66` | =DE32+CZ66 |
| Ligne 33 | Col 4 | D33 | `=DIST_PHASE_1_v2!E22` | =DIST_PHASE_1_v2!E22 |
| Ligne 33 | Col 5 | E33 | `=DIST_PHASE_1_v2!G22` | =DIST_PHASE_1_v2!G22 |
| Ligne 33 | Col 6 | F33 | `=DIST_PHASE_1_v2!L22` | =DIST_PHASE_1_v2!L22 |
| Ligne 33 | Col 7 | G33 | `=DIST_PHASE_1_v2!M22` | =DIST_PHASE_1_v2!M22 |
| Ligne 33 | Col 8 | H33 | `=DIST_PHASE_1_v2!N22` | =DIST_PHASE_1_v2!N22 |
| Ligne 33 | Col 9 | I33 | `= (10.679 * H33) / ((F33/1000)^4.871 * G33^1.852)` | = (10.679 * H33) / ((F33/1000)^4.871 * G33^1.852) |
| Ligne 33 | Col 10 | J33 | `=IF(C33="positif",E33,IF(C33="negatif",-E33,""))` | =IF(C33="positif",E33,IF(C33="negatif",-E33,"")) |
| Ligne 33 | Col 11 | K33 | `=IF(J33>0,I33*E33^1.852,-I33*E33^1.852)` | =IF(J33>0,I33*E33^1.852,-I33*E33^1.852) |
| Ligne 33 | Col 12 | L33 | `=1.852*I33*ABS(E33)^(1.852-1)` | =1.852*I33*ABS(E33)^(1.852-1) |
| Ligne 33 | Col 13 | M33 | `=J33+$D$93` | =J33+$D$93 |
| Ligne 33 | Col 16 | P33 | `=IFERROR(MATCH(S33,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S33,$D$22:$D$91,0),0) |
| Ligne 33 | Col 18 | R33 | `=DIST_PHASE_1_v2!Q22` | =DIST_PHASE_1_v2!Q22 |
| Ligne 33 | Col 19 | S33 | `=DIST_PHASE_1_v2!R22` | =DIST_PHASE_1_v2!R22 |
| Ligne 33 | Col 20 | T33 | `=DIST_PHASE_1_v2!T22` | =DIST_PHASE_1_v2!T22 |
| Ligne 33 | Col 21 | U33 | `=DIST_PHASE_1_v2!Y22` | =DIST_PHASE_1_v2!Y22 |
| Ligne 33 | Col 23 | W33 | `=DIST_PHASE_1_v2!AA22` | =DIST_PHASE_1_v2!AA22 |
| Ligne 33 | Col 24 | X33 | `= (10.679 * W33) / ((U33/1000)^4.871 * V33^1.852)` | = (10.679 * W33) / ((U33/1000)^4.871 * V33^1.852) |
| Ligne 33 | Col 25 | Y33 | `=IF(R33="positif",T33,IF(R33="negatif",-T33,""))` | =IF(R33="positif",T33,IF(R33="negatif",-T33,"")) |
| Ligne 33 | Col 26 | Z33 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E5A30>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E5A30> |
| Ligne 33 | Col 27 | AA33 | `=IF(P33>0,
IF(R33="positif",1,-1),
0)` | =IF(P33>0,
IF(R33="positif",1,-1),
0) |
| Ligne 33 | Col 28 | AB33 | `=X33*SIGN(Y33)*ABS(Y33)^1.852` | =X33*SIGN(Y33)*ABS(Y33)^1.852 |
| Ligne 33 | Col 29 | AC33 | `=1.852*X33*ABS(Y33)^(1.852-1)` | =1.852*X33*ABS(Y33)^(1.852-1) |
| Ligne 33 | Col 30 | AD33 | `=IF(P33>0,
Y33+($D$93*Z33)+(AA33*$S$93),
Y33+$S$93)` | =IF(P33>0,
Y33+($D$93*Z33)+(AA33*$S$93),
Y33+$S$93) |
| Ligne 33 | Col 32 | AF33 | `=ABS(AD33)-ABS(Y33)` | =ABS(AD33)-ABS(Y33) |
| Ligne 33 | Col 36 | AJ33 | `=IFERROR(MATCH(AM33,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM33,$S$22:$S$91,0),0) |
| Ligne 33 | Col 38 | AL33 | `=TRONCONS_V2!AI20` | =TRONCONS_V2!AI20 |
| Ligne 33 | Col 39 | AM33 | `=TRONCONS_V2!AE20` | =TRONCONS_V2!AE20 |
| Ligne 33 | Col 40 | AN33 | `=DIST_PHASE_1_v2!AG22` | =DIST_PHASE_1_v2!AG22 |
| Ligne 33 | Col 41 | AO33 | `=DIST_PHASE_1_v2!AL22` | =DIST_PHASE_1_v2!AL22 |
| Ligne 33 | Col 43 | AQ33 | `=TRONCONS_V2!AG20` | =TRONCONS_V2!AG20 |
| Ligne 33 | Col 44 | AR33 | `= (10.679 * AQ33) / ((AO33/1000)^4.871 * AP33^1.852)` | = (10.679 * AQ33) / ((AO33/1000)^4.871 * AP33^1.852) |
| Ligne 33 | Col 45 | AS33 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E6270>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E6270> |
| Ligne 33 | Col 46 | AT33 | `=IF(AJ33>0,
IF(AS33>0, AR33*AS33^1.852,-AR33*ABS(AS33)^1.852),
IF(AS33>0, AR33*AN33^1.852, -AR33*AN33^1.852))` | =IF(AJ33>0,
IF(AS33>0, AR33*AS33^1.852,-AR33*ABS(AS33)^1.852),
IF(AS33>0, AR33*AN33^1.852, -AR33*AN33^1.852)) |
| Ligne 33 | Col 47 | AU33 | `=1.852*AR33*ABS(AS33)^(1.852-1)` | =1.852*AR33*ABS(AS33)^(1.852-1) |
| Ligne 33 | Col 48 | AV33 | `=AS33+$AN$60` | =AS33+$AN$60 |
| Ligne 33 | Col 52 | AZ33 | `=IFERROR(MATCH(BC33,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC33,$AM$22:$AM$57,0),0) |
| Ligne 33 | Col 54 | BB33 | `=DIST_PHASE_1_v2!AQ22` | =DIST_PHASE_1_v2!AQ22 |
| Ligne 33 | Col 55 | BC33 | `=DIST_PHASE_1_v2!AR22` | =DIST_PHASE_1_v2!AR22 |
| Ligne 33 | Col 56 | BD33 | `=DIST_PHASE_1_v2!AT22` | =DIST_PHASE_1_v2!AT22 |
| Ligne 33 | Col 57 | BE33 | `=DIST_PHASE_1_v2!AY22` | =DIST_PHASE_1_v2!AY22 |
| Ligne 33 | Col 58 | BF33 | `=DIST_PHASE_1_v2!AZ22` | =DIST_PHASE_1_v2!AZ22 |
| Ligne 33 | Col 59 | BG33 | `=DIST_PHASE_1_v2!BA22` | =DIST_PHASE_1_v2!BA22 |
| Ligne 33 | Col 60 | BH33 | `= (10.679 * BG33) / ((BE33/1000)^4.871 * BF33^1.852)` | = (10.679 * BG33) / ((BE33/1000)^4.871 * BF33^1.852) |
| Ligne 33 | Col 61 | BI33 | `=IF(BB33="positif",BD33,IF(BB33="negatif",-BD33,""))` | =IF(BB33="positif",BD33,IF(BB33="negatif",-BD33,"")) |
| Ligne 33 | Col 62 | BJ33 | `=IF(AZ33>0,
IF(BI33>0, BH33*BI33^1.852,-BH33*ABS(BI33)^1.852),
IF(BI33>0, BH33*BD33^1.852, -BH33*BD33^1.852))` | =IF(AZ33>0,
IF(BI33>0, BH33*BI33^1.852,-BH33*ABS(BI33)^1.852),
IF(BI33>0, BH33*BD33^1.852, -BH33*BD33^1.852)) |
| Ligne 33 | Col 63 | BK33 | `=1.852*BH33*ABS(BI33)^(1.852-1)` | =1.852*BH33*ABS(BI33)^(1.852-1) |
| Ligne 33 | Col 64 | BL33 | `=BI33+$BD$75` | =BI33+$BD$75 |
| Ligne 33 | Col 68 | BP33 | `=IFERROR(MATCH(BS33,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS33,$BC$22:$BC$73,0),0) |
| Ligne 33 | Col 70 | BR33 | `=DIST_PHASE_1_v2!BF22` | =DIST_PHASE_1_v2!BF22 |
| Ligne 33 | Col 71 | BS33 | `=DIST_PHASE_1_v2!BG22` | =DIST_PHASE_1_v2!BG22 |
| Ligne 33 | Col 72 | BT33 | `=DIST_PHASE_1_v2!BI22` | =DIST_PHASE_1_v2!BI22 |
| Ligne 33 | Col 73 | BU33 | `=DIST_PHASE_1_v2!BN22` | =DIST_PHASE_1_v2!BN22 |
| Ligne 33 | Col 74 | BV33 | `=DIST_PHASE_1_v2!BO22` | =DIST_PHASE_1_v2!BO22 |
| Ligne 33 | Col 75 | BW33 | `=DIST_PHASE_1_v2!BP22` | =DIST_PHASE_1_v2!BP22 |
| Ligne 33 | Col 76 | BX33 | `= (10.679 * BW33) / ((BU33/1000)^4.871 * BV33^1.852)` | = (10.679 * BW33) / ((BU33/1000)^4.871 * BV33^1.852) |
| Ligne 33 | Col 77 | BY33 | `=IF(BR33="positif",BT33,IF(BR33="negatif",-BT33,""))` | =IF(BR33="positif",BT33,IF(BR33="negatif",-BT33,"")) |
| Ligne 33 | Col 78 | BZ33 | `=IF(BP33>0,
IF(BY33>0, BX33*BY33^1.852,-BX33*ABS(BY33)^1.852),
IF(BY33>0, BX33*BT33^1.852, -BX33*BT33^1.852))` | =IF(BP33>0,
IF(BY33>0, BX33*BY33^1.852,-BX33*ABS(BY33)^1.852),
IF(BY33>0, BX33*BT33^1.852, -BX33*BT33^1.852)) |
| Ligne 33 | Col 79 | CA33 | `=1.852*BX33*ABS(BY33)^(1.852-1)` | =1.852*BX33*ABS(BY33)^(1.852-1) |
| Ligne 33 | Col 80 | CB33 | `=BY33+$BT$64` | =BY33+$BT$64 |
| Ligne 33 | Col 84 | CF33 | `=IFERROR(MATCH(CI33,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI33,$BS$22:$BS$62,0),0) |
| Ligne 33 | Col 86 | CH33 | `=DIST_PHASE_1_v2!BS22` | =DIST_PHASE_1_v2!BS22 |
| Ligne 33 | Col 87 | CI33 | `=DIST_PHASE_1_v2!BT22` | =DIST_PHASE_1_v2!BT22 |
| Ligne 33 | Col 88 | CJ33 | `=DIST_PHASE_1_v2!BV22` | =DIST_PHASE_1_v2!BV22 |
| Ligne 33 | Col 89 | CK33 | `=DIST_PHASE_1_v2!CA22` | =DIST_PHASE_1_v2!CA22 |
| Ligne 33 | Col 91 | CM33 | `=DIST_PHASE_1_v2!CC22` | =DIST_PHASE_1_v2!CC22 |
| Ligne 33 | Col 92 | CN33 | `= (10.679 * CM33) / ((CK33/1000)^4.871 * CL33^1.852)` | = (10.679 * CM33) / ((CK33/1000)^4.871 * CL33^1.852) |
| Ligne 33 | Col 93 | CO33 | `=IF(CH33="positif",CJ33,IF(CH33="negatif",-CJ33,""))` | =IF(CH33="positif",CJ33,IF(CH33="negatif",-CJ33,"")) |
| Ligne 33 | Col 94 | CP33 | `=IF(CF33>0,
IF(CO33>0, CN33*CO33^1.852,-CN33*ABS(CO33)^1.852),
IF(CO33>0, CN33*CJ33^1.852, -CN33*CJ33^1.852))` | =IF(CF33>0,
IF(CO33>0, CN33*CO33^1.852,-CN33*ABS(CO33)^1.852),
IF(CO33>0, CN33*CJ33^1.852, -CN33*CJ33^1.852)) |
| Ligne 33 | Col 95 | CQ33 | `=1.852*CN33*ABS(CO33)^(1.852-1)` | =1.852*CN33*ABS(CO33)^(1.852-1) |
| Ligne 33 | Col 96 | CR33 | `=CO33+$CJ$71` | =CO33+$CJ$71 |
| Ligne 33 | Col 100 | CV33 | `=IFERROR(MATCH(CY33,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY33,$CI$22:$CI$69,0),0) |
| Ligne 33 | Col 102 | CX33 | `=DIST_PHASE_1_v2!CF22` | =DIST_PHASE_1_v2!CF22 |
| Ligne 33 | Col 103 | CY33 | `=DIST_PHASE_1_v2!CG22` | =DIST_PHASE_1_v2!CG22 |
| Ligne 33 | Col 104 | CZ33 | `=DIST_PHASE_1_v2!CI22` | =DIST_PHASE_1_v2!CI22 |
| Ligne 33 | Col 105 | DA33 | `=DIST_PHASE_1_v2!CN22` | =DIST_PHASE_1_v2!CN22 |
| Ligne 33 | Col 106 | DB33 | `=DIST_PHASE_1_v2!CO22` | =DIST_PHASE_1_v2!CO22 |
| Ligne 33 | Col 107 | DC33 | `=DIST_PHASE_1_v2!CP22` | =DIST_PHASE_1_v2!CP22 |
| Ligne 33 | Col 108 | DD33 | `= (10.679 * DC33) / ((DA33/1000)^4.871 * DB33^1.852)` | = (10.679 * DC33) / ((DA33/1000)^4.871 * DB33^1.852) |
| Ligne 33 | Col 109 | DE33 | `=IF(CX33="positif",CZ33,IF(CX33="negatif",-CZ33,""))` | =IF(CX33="positif",CZ33,IF(CX33="negatif",-CZ33,"")) |
| Ligne 33 | Col 110 | DF33 | `=IF(CV33>0,
IF(DE33>0, DD33*DE33^1.852,-DD33*ABS(DE33)^1.852),
IF(DE33>0, DD33*CZ33^1.852, -DD33*CZ33^1.852))` | =IF(CV33>0,
IF(DE33>0, DD33*DE33^1.852,-DD33*ABS(DE33)^1.852),
IF(DE33>0, DD33*CZ33^1.852, -DD33*CZ33^1.852)) |
| Ligne 33 | Col 111 | DG33 | `=1.852*DD33*ABS(DE33)^(1.852-1)` | =1.852*DD33*ABS(DE33)^(1.852-1) |
| Ligne 33 | Col 112 | DH33 | `=DE33+CZ67` | =DE33+CZ67 |
| Ligne 34 | Col 4 | D34 | `=DIST_PHASE_1_v2!E23` | =DIST_PHASE_1_v2!E23 |
| Ligne 34 | Col 5 | E34 | `=DIST_PHASE_1_v2!G23` | =DIST_PHASE_1_v2!G23 |
| Ligne 34 | Col 6 | F34 | `=DIST_PHASE_1_v2!L23` | =DIST_PHASE_1_v2!L23 |
| Ligne 34 | Col 7 | G34 | `=DIST_PHASE_1_v2!M23` | =DIST_PHASE_1_v2!M23 |
| Ligne 34 | Col 8 | H34 | `=DIST_PHASE_1_v2!N23` | =DIST_PHASE_1_v2!N23 |
| Ligne 34 | Col 9 | I34 | `= (10.679 * H34) / ((F34/1000)^4.871 * G34^1.852)` | = (10.679 * H34) / ((F34/1000)^4.871 * G34^1.852) |
| Ligne 34 | Col 10 | J34 | `=IF(C34="positif",E34,IF(C34="negatif",-E34,""))` | =IF(C34="positif",E34,IF(C34="negatif",-E34,"")) |
| Ligne 34 | Col 11 | K34 | `=IF(J34>0,I34*E34^1.852,-I34*E34^1.852)` | =IF(J34>0,I34*E34^1.852,-I34*E34^1.852) |
| Ligne 34 | Col 12 | L34 | `=1.852*I34*ABS(E34)^(1.852-1)` | =1.852*I34*ABS(E34)^(1.852-1) |
| Ligne 34 | Col 13 | M34 | `=J34+$D$93` | =J34+$D$93 |
| Ligne 34 | Col 16 | P34 | `=IFERROR(MATCH(S34,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S34,$D$22:$D$91,0),0) |
| Ligne 34 | Col 18 | R34 | `=DIST_PHASE_1_v2!Q23` | =DIST_PHASE_1_v2!Q23 |
| Ligne 34 | Col 19 | S34 | `=DIST_PHASE_1_v2!R23` | =DIST_PHASE_1_v2!R23 |
| Ligne 34 | Col 20 | T34 | `=DIST_PHASE_1_v2!T23` | =DIST_PHASE_1_v2!T23 |
| Ligne 34 | Col 21 | U34 | `=DIST_PHASE_1_v2!Y23` | =DIST_PHASE_1_v2!Y23 |
| Ligne 34 | Col 23 | W34 | `=DIST_PHASE_1_v2!AA23` | =DIST_PHASE_1_v2!AA23 |
| Ligne 34 | Col 24 | X34 | `= (10.679 * W34) / ((U34/1000)^4.871 * V34^1.852)` | = (10.679 * W34) / ((U34/1000)^4.871 * V34^1.852) |
| Ligne 34 | Col 25 | Y34 | `=IF(R34="positif",T34,IF(R34="negatif",-T34,""))` | =IF(R34="positif",T34,IF(R34="negatif",-T34,"")) |
| Ligne 34 | Col 26 | Z34 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E5EB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E5EB0> |
| Ligne 34 | Col 27 | AA34 | `=IF(P34>0,
IF(R34="positif",1,-1),
0)` | =IF(P34>0,
IF(R34="positif",1,-1),
0) |
| Ligne 34 | Col 28 | AB34 | `=X34*SIGN(Y34)*ABS(Y34)^1.852` | =X34*SIGN(Y34)*ABS(Y34)^1.852 |
| Ligne 34 | Col 29 | AC34 | `=1.852*X34*ABS(Y34)^(1.852-1)` | =1.852*X34*ABS(Y34)^(1.852-1) |
| Ligne 34 | Col 30 | AD34 | `=IF(P34>0,
Y34+($D$93*Z34)+(AA34*$S$93),
Y34+$S$93)` | =IF(P34>0,
Y34+($D$93*Z34)+(AA34*$S$93),
Y34+$S$93) |
| Ligne 34 | Col 32 | AF34 | `=ABS(AD34)-ABS(Y34)` | =ABS(AD34)-ABS(Y34) |
| Ligne 34 | Col 36 | AJ34 | `=IFERROR(MATCH(AM34,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM34,$S$22:$S$91,0),0) |
| Ligne 34 | Col 38 | AL34 | `=TRONCONS_V2!AI21` | =TRONCONS_V2!AI21 |
| Ligne 34 | Col 39 | AM34 | `=TRONCONS_V2!AE21` | =TRONCONS_V2!AE21 |
| Ligne 34 | Col 40 | AN34 | `=DIST_PHASE_1_v2!AG23` | =DIST_PHASE_1_v2!AG23 |
| Ligne 34 | Col 41 | AO34 | `=DIST_PHASE_1_v2!AL23` | =DIST_PHASE_1_v2!AL23 |
| Ligne 34 | Col 43 | AQ34 | `=TRONCONS_V2!AG21` | =TRONCONS_V2!AG21 |
| Ligne 34 | Col 44 | AR34 | `= (10.679 * AQ34) / ((AO34/1000)^4.871 * AP34^1.852)` | = (10.679 * AQ34) / ((AO34/1000)^4.871 * AP34^1.852) |
| Ligne 34 | Col 45 | AS34 | `=IF(AL34="positif",AN34,IF(AL34="negatif",-AN34,""))` | =IF(AL34="positif",AN34,IF(AL34="negatif",-AN34,"")) |
| Ligne 34 | Col 46 | AT34 | `=IF(AJ34>0,
IF(AS34>0, AR34*AS34^1.852,-AR34*ABS(AS34)^1.852),
IF(AS34>0, AR34*AN34^1.852, -AR34*AN34^1.852))` | =IF(AJ34>0,
IF(AS34>0, AR34*AS34^1.852,-AR34*ABS(AS34)^1.852),
IF(AS34>0, AR34*AN34^1.852, -AR34*AN34^1.852)) |
| Ligne 34 | Col 47 | AU34 | `=1.852*AR34*ABS(AS34)^(1.852-1)` | =1.852*AR34*ABS(AS34)^(1.852-1) |
| Ligne 34 | Col 48 | AV34 | `=AS34+$AN$60` | =AS34+$AN$60 |
| Ligne 34 | Col 52 | AZ34 | `=IFERROR(MATCH(BC34,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC34,$AM$22:$AM$57,0),0) |
| Ligne 34 | Col 54 | BB34 | `=DIST_PHASE_1_v2!AQ23` | =DIST_PHASE_1_v2!AQ23 |
| Ligne 34 | Col 55 | BC34 | `=DIST_PHASE_1_v2!AR23` | =DIST_PHASE_1_v2!AR23 |
| Ligne 34 | Col 56 | BD34 | `=DIST_PHASE_1_v2!AT23` | =DIST_PHASE_1_v2!AT23 |
| Ligne 34 | Col 57 | BE34 | `=DIST_PHASE_1_v2!AY23` | =DIST_PHASE_1_v2!AY23 |
| Ligne 34 | Col 58 | BF34 | `=DIST_PHASE_1_v2!AZ23` | =DIST_PHASE_1_v2!AZ23 |
| Ligne 34 | Col 59 | BG34 | `=DIST_PHASE_1_v2!BA23` | =DIST_PHASE_1_v2!BA23 |
| Ligne 34 | Col 60 | BH34 | `= (10.679 * BG34) / ((BE34/1000)^4.871 * BF34^1.852)` | = (10.679 * BG34) / ((BE34/1000)^4.871 * BF34^1.852) |
| Ligne 34 | Col 61 | BI34 | `=IF(BB34="positif",BD34,IF(BB34="negatif",-BD34,""))` | =IF(BB34="positif",BD34,IF(BB34="negatif",-BD34,"")) |
| Ligne 34 | Col 62 | BJ34 | `=IF(AZ34>0,
IF(BI34>0, BH34*BI34^1.852,-BH34*ABS(BI34)^1.852),
IF(BI34>0, BH34*BD34^1.852, -BH34*BD34^1.852))` | =IF(AZ34>0,
IF(BI34>0, BH34*BI34^1.852,-BH34*ABS(BI34)^1.852),
IF(BI34>0, BH34*BD34^1.852, -BH34*BD34^1.852)) |
| Ligne 34 | Col 63 | BK34 | `=1.852*BH34*ABS(BI34)^(1.852-1)` | =1.852*BH34*ABS(BI34)^(1.852-1) |
| Ligne 34 | Col 64 | BL34 | `=BI34+$BD$75` | =BI34+$BD$75 |
| Ligne 34 | Col 68 | BP34 | `=IFERROR(MATCH(BS34,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS34,$BC$22:$BC$73,0),0) |
| Ligne 34 | Col 70 | BR34 | `=DIST_PHASE_1_v2!BF23` | =DIST_PHASE_1_v2!BF23 |
| Ligne 34 | Col 71 | BS34 | `=DIST_PHASE_1_v2!BG23` | =DIST_PHASE_1_v2!BG23 |
| Ligne 34 | Col 72 | BT34 | `=DIST_PHASE_1_v2!BI23` | =DIST_PHASE_1_v2!BI23 |
| Ligne 34 | Col 73 | BU34 | `=DIST_PHASE_1_v2!BN23` | =DIST_PHASE_1_v2!BN23 |
| Ligne 34 | Col 74 | BV34 | `=DIST_PHASE_1_v2!BO23` | =DIST_PHASE_1_v2!BO23 |
| Ligne 34 | Col 75 | BW34 | `=DIST_PHASE_1_v2!BP23` | =DIST_PHASE_1_v2!BP23 |
| Ligne 34 | Col 76 | BX34 | `= (10.679 * BW34) / ((BU34/1000)^4.871 * BV34^1.852)` | = (10.679 * BW34) / ((BU34/1000)^4.871 * BV34^1.852) |
| Ligne 34 | Col 77 | BY34 | `=IF(BR34="positif",BT34,IF(BR34="negatif",-BT34,""))` | =IF(BR34="positif",BT34,IF(BR34="negatif",-BT34,"")) |
| Ligne 34 | Col 78 | BZ34 | `=IF(BP34>0,
IF(BY34>0, BX34*BY34^1.852,-BX34*ABS(BY34)^1.852),
IF(BY34>0, BX34*BT34^1.852, -BX34*BT34^1.852))` | =IF(BP34>0,
IF(BY34>0, BX34*BY34^1.852,-BX34*ABS(BY34)^1.852),
IF(BY34>0, BX34*BT34^1.852, -BX34*BT34^1.852)) |
| Ligne 34 | Col 79 | CA34 | `=1.852*BX34*ABS(BY34)^(1.852-1)` | =1.852*BX34*ABS(BY34)^(1.852-1) |
| Ligne 34 | Col 80 | CB34 | `=BY34+$BT$64` | =BY34+$BT$64 |
| Ligne 34 | Col 84 | CF34 | `=IFERROR(MATCH(CI34,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI34,$BS$22:$BS$62,0),0) |
| Ligne 34 | Col 86 | CH34 | `=DIST_PHASE_1_v2!BS23` | =DIST_PHASE_1_v2!BS23 |
| Ligne 34 | Col 87 | CI34 | `=DIST_PHASE_1_v2!BT23` | =DIST_PHASE_1_v2!BT23 |
| Ligne 34 | Col 88 | CJ34 | `=DIST_PHASE_1_v2!BV23` | =DIST_PHASE_1_v2!BV23 |
| Ligne 34 | Col 89 | CK34 | `=DIST_PHASE_1_v2!CA23` | =DIST_PHASE_1_v2!CA23 |
| Ligne 34 | Col 91 | CM34 | `=DIST_PHASE_1_v2!CC23` | =DIST_PHASE_1_v2!CC23 |
| Ligne 34 | Col 92 | CN34 | `= (10.679 * CM34) / ((CK34/1000)^4.871 * CL34^1.852)` | = (10.679 * CM34) / ((CK34/1000)^4.871 * CL34^1.852) |
| Ligne 34 | Col 93 | CO34 | `=IF(CH34="positif",CJ34,IF(CH34="negatif",-CJ34,""))` | =IF(CH34="positif",CJ34,IF(CH34="negatif",-CJ34,"")) |
| Ligne 34 | Col 94 | CP34 | `=IF(CF34>0,
IF(CO34>0, CN34*CO34^1.852,-CN34*ABS(CO34)^1.852),
IF(CO34>0, CN34*CJ34^1.852, -CN34*CJ34^1.852))` | =IF(CF34>0,
IF(CO34>0, CN34*CO34^1.852,-CN34*ABS(CO34)^1.852),
IF(CO34>0, CN34*CJ34^1.852, -CN34*CJ34^1.852)) |
| Ligne 34 | Col 95 | CQ34 | `=1.852*CN34*ABS(CO34)^(1.852-1)` | =1.852*CN34*ABS(CO34)^(1.852-1) |
| Ligne 34 | Col 96 | CR34 | `=CO34+$CJ$71` | =CO34+$CJ$71 |
| Ligne 34 | Col 100 | CV34 | `=IFERROR(MATCH(CY34,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY34,$CI$22:$CI$69,0),0) |
| Ligne 34 | Col 102 | CX34 | `=DIST_PHASE_1_v2!CF23` | =DIST_PHASE_1_v2!CF23 |
| Ligne 34 | Col 103 | CY34 | `=DIST_PHASE_1_v2!CG23` | =DIST_PHASE_1_v2!CG23 |
| Ligne 34 | Col 104 | CZ34 | `=DIST_PHASE_1_v2!CI23` | =DIST_PHASE_1_v2!CI23 |
| Ligne 34 | Col 105 | DA34 | `=DIST_PHASE_1_v2!CN23` | =DIST_PHASE_1_v2!CN23 |
| Ligne 34 | Col 106 | DB34 | `=DIST_PHASE_1_v2!CO23` | =DIST_PHASE_1_v2!CO23 |
| Ligne 34 | Col 107 | DC34 | `=DIST_PHASE_1_v2!CP23` | =DIST_PHASE_1_v2!CP23 |
| Ligne 34 | Col 108 | DD34 | `= (10.679 * DC34) / ((DA34/1000)^4.871 * DB34^1.852)` | = (10.679 * DC34) / ((DA34/1000)^4.871 * DB34^1.852) |
| Ligne 34 | Col 109 | DE34 | `=IF(CX34="positif",CZ34,IF(CX34="negatif",-CZ34,""))` | =IF(CX34="positif",CZ34,IF(CX34="negatif",-CZ34,"")) |
| Ligne 34 | Col 110 | DF34 | `=IF(CV34>0,
IF(DE34>0, DD34*DE34^1.852,-DD34*ABS(DE34)^1.852),
IF(DE34>0, DD34*CZ34^1.852, -DD34*CZ34^1.852))` | =IF(CV34>0,
IF(DE34>0, DD34*DE34^1.852,-DD34*ABS(DE34)^1.852),
IF(DE34>0, DD34*CZ34^1.852, -DD34*CZ34^1.852)) |
| Ligne 34 | Col 111 | DG34 | `=1.852*DD34*ABS(DE34)^(1.852-1)` | =1.852*DD34*ABS(DE34)^(1.852-1) |
| Ligne 34 | Col 112 | DH34 | `=DE34+CZ68` | =DE34+CZ68 |
| Ligne 35 | Col 4 | D35 | `=DIST_PHASE_1_v2!E24` | =DIST_PHASE_1_v2!E24 |
| Ligne 35 | Col 5 | E35 | `=DIST_PHASE_1_v2!G24` | =DIST_PHASE_1_v2!G24 |
| Ligne 35 | Col 6 | F35 | `=DIST_PHASE_1_v2!L24` | =DIST_PHASE_1_v2!L24 |
| Ligne 35 | Col 7 | G35 | `=DIST_PHASE_1_v2!M24` | =DIST_PHASE_1_v2!M24 |
| Ligne 35 | Col 8 | H35 | `=DIST_PHASE_1_v2!N24` | =DIST_PHASE_1_v2!N24 |
| Ligne 35 | Col 9 | I35 | `= (10.679 * H35) / ((F35/1000)^4.871 * G35^1.852)` | = (10.679 * H35) / ((F35/1000)^4.871 * G35^1.852) |
| Ligne 35 | Col 10 | J35 | `=IF(C35="positif",E35,IF(C35="negatif",-E35,""))` | =IF(C35="positif",E35,IF(C35="negatif",-E35,"")) |
| Ligne 35 | Col 11 | K35 | `=IF(J35>0,I35*E35^1.852,-I35*E35^1.852)` | =IF(J35>0,I35*E35^1.852,-I35*E35^1.852) |
| Ligne 35 | Col 12 | L35 | `=1.852*I35*ABS(E35)^(1.852-1)` | =1.852*I35*ABS(E35)^(1.852-1) |
| Ligne 35 | Col 13 | M35 | `=J35+$D$93` | =J35+$D$93 |
| Ligne 35 | Col 16 | P35 | `=IFERROR(MATCH(S35,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S35,$D$22:$D$91,0),0) |
| Ligne 35 | Col 18 | R35 | `=DIST_PHASE_1_v2!Q24` | =DIST_PHASE_1_v2!Q24 |
| Ligne 35 | Col 19 | S35 | `=DIST_PHASE_1_v2!R24` | =DIST_PHASE_1_v2!R24 |
| Ligne 35 | Col 20 | T35 | `=DIST_PHASE_1_v2!T24` | =DIST_PHASE_1_v2!T24 |
| Ligne 35 | Col 21 | U35 | `=DIST_PHASE_1_v2!Y24` | =DIST_PHASE_1_v2!Y24 |
| Ligne 35 | Col 23 | W35 | `=DIST_PHASE_1_v2!AA24` | =DIST_PHASE_1_v2!AA24 |
| Ligne 35 | Col 24 | X35 | `= (10.679 * W35) / ((U35/1000)^4.871 * V35^1.852)` | = (10.679 * W35) / ((U35/1000)^4.871 * V35^1.852) |
| Ligne 35 | Col 25 | Y35 | `=IF(R35="positif",T35,IF(R35="negatif",-T35,""))` | =IF(R35="positif",T35,IF(R35="negatif",-T35,"")) |
| Ligne 35 | Col 26 | Z35 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E5F10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E5F10> |
| Ligne 35 | Col 27 | AA35 | `=IF(P35>0,
IF(R35="positif",1,-1),
0)` | =IF(P35>0,
IF(R35="positif",1,-1),
0) |
| Ligne 35 | Col 28 | AB35 | `=X35*SIGN(Y35)*ABS(Y35)^1.852` | =X35*SIGN(Y35)*ABS(Y35)^1.852 |
| Ligne 35 | Col 29 | AC35 | `=1.852*X35*ABS(Y35)^(1.852-1)` | =1.852*X35*ABS(Y35)^(1.852-1) |
| Ligne 35 | Col 30 | AD35 | `=IF(P35>0,
Y35+($D$93*Z35)+(AA35*$S$93),
Y35+$S$93)` | =IF(P35>0,
Y35+($D$93*Z35)+(AA35*$S$93),
Y35+$S$93) |
| Ligne 35 | Col 32 | AF35 | `=ABS(AD35)-ABS(Y35)` | =ABS(AD35)-ABS(Y35) |
| Ligne 35 | Col 36 | AJ35 | `=IFERROR(MATCH(AM35,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM35,$S$22:$S$91,0),0) |
| Ligne 35 | Col 38 | AL35 | `=TRONCONS_V2!AI22` | =TRONCONS_V2!AI22 |
| Ligne 35 | Col 39 | AM35 | `=TRONCONS_V2!AE22` | =TRONCONS_V2!AE22 |
| Ligne 35 | Col 40 | AN35 | `=DIST_PHASE_1_v2!AG24` | =DIST_PHASE_1_v2!AG24 |
| Ligne 35 | Col 41 | AO35 | `=DIST_PHASE_1_v2!AL24` | =DIST_PHASE_1_v2!AL24 |
| Ligne 35 | Col 43 | AQ35 | `=TRONCONS_V2!AG22` | =TRONCONS_V2!AG22 |
| Ligne 35 | Col 44 | AR35 | `= (10.679 * AQ35) / ((AO35/1000)^4.871 * AP35^1.852)` | = (10.679 * AQ35) / ((AO35/1000)^4.871 * AP35^1.852) |
| Ligne 35 | Col 45 | AS35 | `=IF(AL35="positif",AN35,IF(AL35="negatif",-AN35,""))` | =IF(AL35="positif",AN35,IF(AL35="negatif",-AN35,"")) |
| Ligne 35 | Col 46 | AT35 | `=IF(AJ35>0,
IF(AS35>0, AR35*AS35^1.852,-AR35*ABS(AS35)^1.852),
IF(AS35>0, AR35*AN35^1.852, -AR35*AN35^1.852))` | =IF(AJ35>0,
IF(AS35>0, AR35*AS35^1.852,-AR35*ABS(AS35)^1.852),
IF(AS35>0, AR35*AN35^1.852, -AR35*AN35^1.852)) |
| Ligne 35 | Col 47 | AU35 | `=1.852*AR35*ABS(AS35)^(1.852-1)` | =1.852*AR35*ABS(AS35)^(1.852-1) |
| Ligne 35 | Col 48 | AV35 | `=AS35+$AN$60` | =AS35+$AN$60 |
| Ligne 35 | Col 52 | AZ35 | `=IFERROR(MATCH(BC35,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC35,$AM$22:$AM$57,0),0) |
| Ligne 35 | Col 54 | BB35 | `=DIST_PHASE_1_v2!AQ24` | =DIST_PHASE_1_v2!AQ24 |
| Ligne 35 | Col 55 | BC35 | `=DIST_PHASE_1_v2!AR24` | =DIST_PHASE_1_v2!AR24 |
| Ligne 35 | Col 56 | BD35 | `=DIST_PHASE_1_v2!AT24` | =DIST_PHASE_1_v2!AT24 |
| Ligne 35 | Col 57 | BE35 | `=DIST_PHASE_1_v2!AY24` | =DIST_PHASE_1_v2!AY24 |
| Ligne 35 | Col 58 | BF35 | `=DIST_PHASE_1_v2!AZ24` | =DIST_PHASE_1_v2!AZ24 |
| Ligne 35 | Col 59 | BG35 | `=DIST_PHASE_1_v2!BA24` | =DIST_PHASE_1_v2!BA24 |
| Ligne 35 | Col 60 | BH35 | `= (10.679 * BG35) / ((BE35/1000)^4.871 * BF35^1.852)` | = (10.679 * BG35) / ((BE35/1000)^4.871 * BF35^1.852) |
| Ligne 35 | Col 61 | BI35 | `=IF(BB35="positif",BD35,IF(BB35="negatif",-BD35,""))` | =IF(BB35="positif",BD35,IF(BB35="negatif",-BD35,"")) |
| Ligne 35 | Col 62 | BJ35 | `=IF(AZ35>0,
IF(BI35>0, BH35*BI35^1.852,-BH35*ABS(BI35)^1.852),
IF(BI35>0, BH35*BD35^1.852, -BH35*BD35^1.852))` | =IF(AZ35>0,
IF(BI35>0, BH35*BI35^1.852,-BH35*ABS(BI35)^1.852),
IF(BI35>0, BH35*BD35^1.852, -BH35*BD35^1.852)) |
| Ligne 35 | Col 63 | BK35 | `=1.852*BH35*ABS(BI35)^(1.852-1)` | =1.852*BH35*ABS(BI35)^(1.852-1) |
| Ligne 35 | Col 64 | BL35 | `=BI35+$BD$75` | =BI35+$BD$75 |
| Ligne 35 | Col 68 | BP35 | `=IFERROR(MATCH(BS35,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS35,$BC$22:$BC$73,0),0) |
| Ligne 35 | Col 70 | BR35 | `=DIST_PHASE_1_v2!BF24` | =DIST_PHASE_1_v2!BF24 |
| Ligne 35 | Col 71 | BS35 | `=DIST_PHASE_1_v2!BG24` | =DIST_PHASE_1_v2!BG24 |
| Ligne 35 | Col 72 | BT35 | `=DIST_PHASE_1_v2!BI24` | =DIST_PHASE_1_v2!BI24 |
| Ligne 35 | Col 73 | BU35 | `=DIST_PHASE_1_v2!BN24` | =DIST_PHASE_1_v2!BN24 |
| Ligne 35 | Col 74 | BV35 | `=DIST_PHASE_1_v2!BO24` | =DIST_PHASE_1_v2!BO24 |
| Ligne 35 | Col 75 | BW35 | `=DIST_PHASE_1_v2!BP24` | =DIST_PHASE_1_v2!BP24 |
| Ligne 35 | Col 76 | BX35 | `= (10.679 * BW35) / ((BU35/1000)^4.871 * BV35^1.852)` | = (10.679 * BW35) / ((BU35/1000)^4.871 * BV35^1.852) |
| Ligne 35 | Col 77 | BY35 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E6FF0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E6FF0> |
| Ligne 35 | Col 78 | BZ35 | `=IF(BP35>0,
IF(BY35>0, BX35*BY35^1.852,-BX35*ABS(BY35)^1.852),
IF(BY35>0, BX35*BT35^1.852, -BX35*BT35^1.852))` | =IF(BP35>0,
IF(BY35>0, BX35*BY35^1.852,-BX35*ABS(BY35)^1.852),
IF(BY35>0, BX35*BT35^1.852, -BX35*BT35^1.852)) |
| Ligne 35 | Col 79 | CA35 | `=1.852*BX35*ABS(BY35)^(1.852-1)` | =1.852*BX35*ABS(BY35)^(1.852-1) |
| Ligne 35 | Col 80 | CB35 | `=BY35+$BT$64` | =BY35+$BT$64 |
| Ligne 35 | Col 84 | CF35 | `=IFERROR(MATCH(CI35,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI35,$BS$22:$BS$62,0),0) |
| Ligne 35 | Col 86 | CH35 | `=DIST_PHASE_1_v2!BS24` | =DIST_PHASE_1_v2!BS24 |
| Ligne 35 | Col 87 | CI35 | `=DIST_PHASE_1_v2!BT24` | =DIST_PHASE_1_v2!BT24 |
| Ligne 35 | Col 88 | CJ35 | `=DIST_PHASE_1_v2!BV24` | =DIST_PHASE_1_v2!BV24 |
| Ligne 35 | Col 89 | CK35 | `=DIST_PHASE_1_v2!CA24` | =DIST_PHASE_1_v2!CA24 |
| Ligne 35 | Col 91 | CM35 | `=DIST_PHASE_1_v2!CC24` | =DIST_PHASE_1_v2!CC24 |
| Ligne 35 | Col 92 | CN35 | `= (10.679 * CM35) / ((CK35/1000)^4.871 * CL35^1.852)` | = (10.679 * CM35) / ((CK35/1000)^4.871 * CL35^1.852) |
| Ligne 35 | Col 93 | CO35 | `=IF(CH35="positif",CJ35,IF(CH35="negatif",-CJ35,""))` | =IF(CH35="positif",CJ35,IF(CH35="negatif",-CJ35,"")) |
| Ligne 35 | Col 94 | CP35 | `=IF(CF35>0,
IF(CO35>0, CN35*CO35^1.852,-CN35*ABS(CO35)^1.852),
IF(CO35>0, CN35*CJ35^1.852, -CN35*CJ35^1.852))` | =IF(CF35>0,
IF(CO35>0, CN35*CO35^1.852,-CN35*ABS(CO35)^1.852),
IF(CO35>0, CN35*CJ35^1.852, -CN35*CJ35^1.852)) |
| Ligne 35 | Col 95 | CQ35 | `=1.852*CN35*ABS(CO35)^(1.852-1)` | =1.852*CN35*ABS(CO35)^(1.852-1) |
| Ligne 35 | Col 96 | CR35 | `=CO35+$CJ$71` | =CO35+$CJ$71 |
| Ligne 35 | Col 100 | CV35 | `=IFERROR(MATCH(CY35,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY35,$CI$22:$CI$69,0),0) |
| Ligne 35 | Col 102 | CX35 | `=DIST_PHASE_1_v2!CF24` | =DIST_PHASE_1_v2!CF24 |
| Ligne 35 | Col 103 | CY35 | `=DIST_PHASE_1_v2!CG24` | =DIST_PHASE_1_v2!CG24 |
| Ligne 35 | Col 104 | CZ35 | `=DIST_PHASE_1_v2!CI24` | =DIST_PHASE_1_v2!CI24 |
| Ligne 35 | Col 105 | DA35 | `=DIST_PHASE_1_v2!CN24` | =DIST_PHASE_1_v2!CN24 |
| Ligne 35 | Col 106 | DB35 | `=DIST_PHASE_1_v2!CO24` | =DIST_PHASE_1_v2!CO24 |
| Ligne 35 | Col 107 | DC35 | `=DIST_PHASE_1_v2!CP24` | =DIST_PHASE_1_v2!CP24 |
| Ligne 35 | Col 108 | DD35 | `= (10.679 * DC35) / ((DA35/1000)^4.871 * DB35^1.852)` | = (10.679 * DC35) / ((DA35/1000)^4.871 * DB35^1.852) |
| Ligne 35 | Col 109 | DE35 | `=IF(CX35="positif",CZ35,IF(CX35="negatif",-CZ35,""))` | =IF(CX35="positif",CZ35,IF(CX35="negatif",-CZ35,"")) |
| Ligne 35 | Col 110 | DF35 | `=IF(CV35>0,
IF(DE35>0, DD35*DE35^1.852,-DD35*ABS(DE35)^1.852),
IF(DE35>0, DD35*CZ35^1.852, -DD35*CZ35^1.852))` | =IF(CV35>0,
IF(DE35>0, DD35*DE35^1.852,-DD35*ABS(DE35)^1.852),
IF(DE35>0, DD35*CZ35^1.852, -DD35*CZ35^1.852)) |
| Ligne 35 | Col 111 | DG35 | `=1.852*DD35*ABS(DE35)^(1.852-1)` | =1.852*DD35*ABS(DE35)^(1.852-1) |
| Ligne 35 | Col 112 | DH35 | `=DE35+CZ69` | =DE35+CZ69 |
| Ligne 36 | Col 4 | D36 | `=DIST_PHASE_1_v2!E25` | =DIST_PHASE_1_v2!E25 |
| Ligne 36 | Col 5 | E36 | `=DIST_PHASE_1_v2!G25` | =DIST_PHASE_1_v2!G25 |
| Ligne 36 | Col 6 | F36 | `=DIST_PHASE_1_v2!L25` | =DIST_PHASE_1_v2!L25 |
| Ligne 36 | Col 7 | G36 | `=DIST_PHASE_1_v2!M25` | =DIST_PHASE_1_v2!M25 |
| Ligne 36 | Col 8 | H36 | `=DIST_PHASE_1_v2!N25` | =DIST_PHASE_1_v2!N25 |
| Ligne 36 | Col 9 | I36 | `= (10.679 * H36) / ((F36/1000)^4.871 * G36^1.852)` | = (10.679 * H36) / ((F36/1000)^4.871 * G36^1.852) |
| Ligne 36 | Col 10 | J36 | `=IF(C36="positif",E36,IF(C36="negatif",-E36,""))` | =IF(C36="positif",E36,IF(C36="negatif",-E36,"")) |
| Ligne 36 | Col 11 | K36 | `=IF(J36>0,I36*E36^1.852,-I36*E36^1.852)` | =IF(J36>0,I36*E36^1.852,-I36*E36^1.852) |
| Ligne 36 | Col 12 | L36 | `=1.852*I36*ABS(E36)^(1.852-1)` | =1.852*I36*ABS(E36)^(1.852-1) |
| Ligne 36 | Col 13 | M36 | `=J36+$D$93` | =J36+$D$93 |
| Ligne 36 | Col 16 | P36 | `=IFERROR(MATCH(S36,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S36,$D$22:$D$91,0),0) |
| Ligne 36 | Col 18 | R36 | `=DIST_PHASE_1_v2!Q25` | =DIST_PHASE_1_v2!Q25 |
| Ligne 36 | Col 19 | S36 | `=DIST_PHASE_1_v2!R25` | =DIST_PHASE_1_v2!R25 |
| Ligne 36 | Col 20 | T36 | `=DIST_PHASE_1_v2!T25` | =DIST_PHASE_1_v2!T25 |
| Ligne 36 | Col 21 | U36 | `=DIST_PHASE_1_v2!Y25` | =DIST_PHASE_1_v2!Y25 |
| Ligne 36 | Col 23 | W36 | `=DIST_PHASE_1_v2!AA25` | =DIST_PHASE_1_v2!AA25 |
| Ligne 36 | Col 24 | X36 | `= (10.679 * W36) / ((U36/1000)^4.871 * V36^1.852)` | = (10.679 * W36) / ((U36/1000)^4.871 * V36^1.852) |
| Ligne 36 | Col 25 | Y36 | `=IF(R36="positif",T36,IF(R36="negatif",-T36,""))` | =IF(R36="positif",T36,IF(R36="negatif",-T36,"")) |
| Ligne 36 | Col 26 | Z36 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E6B10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E6B10> |
| Ligne 36 | Col 27 | AA36 | `=IF(P36>0,
IF(R36="positif",1,-1),
0)` | =IF(P36>0,
IF(R36="positif",1,-1),
0) |
| Ligne 36 | Col 28 | AB36 | `=X36*SIGN(Y36)*ABS(Y36)^1.852` | =X36*SIGN(Y36)*ABS(Y36)^1.852 |
| Ligne 36 | Col 29 | AC36 | `=1.852*X36*ABS(Y36)^(1.852-1)` | =1.852*X36*ABS(Y36)^(1.852-1) |
| Ligne 36 | Col 30 | AD36 | `=IF(P36>0,
Y36+($D$93*Z36)+(AA36*$S$93),
Y36+$S$93)` | =IF(P36>0,
Y36+($D$93*Z36)+(AA36*$S$93),
Y36+$S$93) |
| Ligne 36 | Col 32 | AF36 | `=ABS(AD36)-ABS(Y36)` | =ABS(AD36)-ABS(Y36) |
| Ligne 36 | Col 36 | AJ36 | `=IFERROR(MATCH(AM36,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM36,$S$22:$S$91,0),0) |
| Ligne 36 | Col 38 | AL36 | `=TRONCONS_V2!AI23` | =TRONCONS_V2!AI23 |
| Ligne 36 | Col 39 | AM36 | `=TRONCONS_V2!AE23` | =TRONCONS_V2!AE23 |
| Ligne 36 | Col 40 | AN36 | `=DIST_PHASE_1_v2!AG25` | =DIST_PHASE_1_v2!AG25 |
| Ligne 36 | Col 41 | AO36 | `=DIST_PHASE_1_v2!AL25` | =DIST_PHASE_1_v2!AL25 |
| Ligne 36 | Col 43 | AQ36 | `=TRONCONS_V2!AG23` | =TRONCONS_V2!AG23 |
| Ligne 36 | Col 44 | AR36 | `= (10.679 * AQ36) / ((AO36/1000)^4.871 * AP36^1.852)` | = (10.679 * AQ36) / ((AO36/1000)^4.871 * AP36^1.852) |
| Ligne 36 | Col 45 | AS36 | `=IF(AL36="positif",AN36,IF(AL36="negatif",-AN36,""))` | =IF(AL36="positif",AN36,IF(AL36="negatif",-AN36,"")) |
| Ligne 36 | Col 46 | AT36 | `=IF(AJ36>0,
IF(AS36>0, AR36*AS36^1.852,-AR36*ABS(AS36)^1.852),
IF(AS36>0, AR36*AN36^1.852, -AR36*AN36^1.852))` | =IF(AJ36>0,
IF(AS36>0, AR36*AS36^1.852,-AR36*ABS(AS36)^1.852),
IF(AS36>0, AR36*AN36^1.852, -AR36*AN36^1.852)) |
| Ligne 36 | Col 47 | AU36 | `=1.852*AR36*ABS(AS36)^(1.852-1)` | =1.852*AR36*ABS(AS36)^(1.852-1) |
| Ligne 36 | Col 48 | AV36 | `=AS36+$AN$60` | =AS36+$AN$60 |
| Ligne 36 | Col 52 | AZ36 | `=IFERROR(MATCH(BC36,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC36,$AM$22:$AM$57,0),0) |
| Ligne 36 | Col 54 | BB36 | `=DIST_PHASE_1_v2!AQ25` | =DIST_PHASE_1_v2!AQ25 |
| Ligne 36 | Col 55 | BC36 | `=DIST_PHASE_1_v2!AR25` | =DIST_PHASE_1_v2!AR25 |
| Ligne 36 | Col 56 | BD36 | `=DIST_PHASE_1_v2!AT25` | =DIST_PHASE_1_v2!AT25 |
| Ligne 36 | Col 57 | BE36 | `=DIST_PHASE_1_v2!AY25` | =DIST_PHASE_1_v2!AY25 |
| Ligne 36 | Col 58 | BF36 | `=DIST_PHASE_1_v2!AZ25` | =DIST_PHASE_1_v2!AZ25 |
| Ligne 36 | Col 59 | BG36 | `=DIST_PHASE_1_v2!BA25` | =DIST_PHASE_1_v2!BA25 |
| Ligne 36 | Col 60 | BH36 | `= (10.679 * BG36) / ((BE36/1000)^4.871 * BF36^1.852)` | = (10.679 * BG36) / ((BE36/1000)^4.871 * BF36^1.852) |
| Ligne 36 | Col 61 | BI36 | `=IF(BB36="positif",BD36,IF(BB36="negatif",-BD36,""))` | =IF(BB36="positif",BD36,IF(BB36="negatif",-BD36,"")) |
| Ligne 36 | Col 62 | BJ36 | `=IF(AZ36>0,
IF(BI36>0, BH36*BI36^1.852,-BH36*ABS(BI36)^1.852),
IF(BI36>0, BH36*BD36^1.852, -BH36*BD36^1.852))` | =IF(AZ36>0,
IF(BI36>0, BH36*BI36^1.852,-BH36*ABS(BI36)^1.852),
IF(BI36>0, BH36*BD36^1.852, -BH36*BD36^1.852)) |
| Ligne 36 | Col 63 | BK36 | `=1.852*BH36*ABS(BI36)^(1.852-1)` | =1.852*BH36*ABS(BI36)^(1.852-1) |
| Ligne 36 | Col 64 | BL36 | `=BI36+$BD$75` | =BI36+$BD$75 |
| Ligne 36 | Col 68 | BP36 | `=IFERROR(MATCH(BS36,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS36,$BC$22:$BC$73,0),0) |
| Ligne 36 | Col 70 | BR36 | `=DIST_PHASE_1_v2!BF25` | =DIST_PHASE_1_v2!BF25 |
| Ligne 36 | Col 71 | BS36 | `=DIST_PHASE_1_v2!BG25` | =DIST_PHASE_1_v2!BG25 |
| Ligne 36 | Col 72 | BT36 | `=DIST_PHASE_1_v2!BI25` | =DIST_PHASE_1_v2!BI25 |
| Ligne 36 | Col 73 | BU36 | `=DIST_PHASE_1_v2!BN25` | =DIST_PHASE_1_v2!BN25 |
| Ligne 36 | Col 74 | BV36 | `=DIST_PHASE_1_v2!BO25` | =DIST_PHASE_1_v2!BO25 |
| Ligne 36 | Col 75 | BW36 | `=DIST_PHASE_1_v2!BP25` | =DIST_PHASE_1_v2!BP25 |
| Ligne 36 | Col 76 | BX36 | `= (10.679 * BW36) / ((BU36/1000)^4.871 * BV36^1.852)` | = (10.679 * BW36) / ((BU36/1000)^4.871 * BV36^1.852) |
| Ligne 36 | Col 77 | BY36 | `=IF(BR36="positif",BT36,IF(BR36="negatif",-BT36,""))` | =IF(BR36="positif",BT36,IF(BR36="negatif",-BT36,"")) |
| Ligne 36 | Col 78 | BZ36 | `=IF(BP36>0,
IF(BY36>0, BX36*BY36^1.852,-BX36*ABS(BY36)^1.852),
IF(BY36>0, BX36*BT36^1.852, -BX36*BT36^1.852))` | =IF(BP36>0,
IF(BY36>0, BX36*BY36^1.852,-BX36*ABS(BY36)^1.852),
IF(BY36>0, BX36*BT36^1.852, -BX36*BT36^1.852)) |
| Ligne 36 | Col 79 | CA36 | `=1.852*BX36*ABS(BY36)^(1.852-1)` | =1.852*BX36*ABS(BY36)^(1.852-1) |
| Ligne 36 | Col 80 | CB36 | `=BY36+$BT$64` | =BY36+$BT$64 |
| Ligne 36 | Col 84 | CF36 | `=IFERROR(MATCH(CI36,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI36,$BS$22:$BS$62,0),0) |
| Ligne 36 | Col 86 | CH36 | `=DIST_PHASE_1_v2!BS25` | =DIST_PHASE_1_v2!BS25 |
| Ligne 36 | Col 87 | CI36 | `=DIST_PHASE_1_v2!BT25` | =DIST_PHASE_1_v2!BT25 |
| Ligne 36 | Col 88 | CJ36 | `=DIST_PHASE_1_v2!BV25` | =DIST_PHASE_1_v2!BV25 |
| Ligne 36 | Col 89 | CK36 | `=DIST_PHASE_1_v2!CA25` | =DIST_PHASE_1_v2!CA25 |
| Ligne 36 | Col 91 | CM36 | `=DIST_PHASE_1_v2!CC25` | =DIST_PHASE_1_v2!CC25 |
| Ligne 36 | Col 92 | CN36 | `= (10.679 * CM36) / ((CK36/1000)^4.871 * CL36^1.852)` | = (10.679 * CM36) / ((CK36/1000)^4.871 * CL36^1.852) |
| Ligne 36 | Col 93 | CO36 | `=IF(CH36="positif",CJ36,IF(CH36="negatif",-CJ36,""))` | =IF(CH36="positif",CJ36,IF(CH36="negatif",-CJ36,"")) |
| Ligne 36 | Col 94 | CP36 | `=IF(CF36>0,
IF(CO36>0, CN36*CO36^1.852,-CN36*ABS(CO36)^1.852),
IF(CO36>0, CN36*CJ36^1.852, -CN36*CJ36^1.852))` | =IF(CF36>0,
IF(CO36>0, CN36*CO36^1.852,-CN36*ABS(CO36)^1.852),
IF(CO36>0, CN36*CJ36^1.852, -CN36*CJ36^1.852)) |
| Ligne 36 | Col 95 | CQ36 | `=1.852*CN36*ABS(CO36)^(1.852-1)` | =1.852*CN36*ABS(CO36)^(1.852-1) |
| Ligne 36 | Col 96 | CR36 | `=CO36+$CJ$71` | =CO36+$CJ$71 |
| Ligne 36 | Col 100 | CV36 | `=IFERROR(MATCH(CY36,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY36,$CI$22:$CI$69,0),0) |
| Ligne 36 | Col 102 | CX36 | `=DIST_PHASE_1_v2!CF25` | =DIST_PHASE_1_v2!CF25 |
| Ligne 36 | Col 103 | CY36 | `=DIST_PHASE_1_v2!CG25` | =DIST_PHASE_1_v2!CG25 |
| Ligne 36 | Col 104 | CZ36 | `=DIST_PHASE_1_v2!CI25` | =DIST_PHASE_1_v2!CI25 |
| Ligne 36 | Col 105 | DA36 | `=DIST_PHASE_1_v2!CN25` | =DIST_PHASE_1_v2!CN25 |
| Ligne 36 | Col 106 | DB36 | `=DIST_PHASE_1_v2!CO25` | =DIST_PHASE_1_v2!CO25 |
| Ligne 36 | Col 107 | DC36 | `=DIST_PHASE_1_v2!CP25` | =DIST_PHASE_1_v2!CP25 |
| Ligne 36 | Col 108 | DD36 | `= (10.679 * DC36) / ((DA36/1000)^4.871 * DB36^1.852)` | = (10.679 * DC36) / ((DA36/1000)^4.871 * DB36^1.852) |
| Ligne 36 | Col 109 | DE36 | `=IF(CX36="positif",CZ36,IF(CX36="negatif",-CZ36,""))` | =IF(CX36="positif",CZ36,IF(CX36="negatif",-CZ36,"")) |
| Ligne 36 | Col 110 | DF36 | `=IF(CV36>0,
IF(DE36>0, DD36*DE36^1.852,-DD36*ABS(DE36)^1.852),
IF(DE36>0, DD36*CZ36^1.852, -DD36*CZ36^1.852))` | =IF(CV36>0,
IF(DE36>0, DD36*DE36^1.852,-DD36*ABS(DE36)^1.852),
IF(DE36>0, DD36*CZ36^1.852, -DD36*CZ36^1.852)) |
| Ligne 36 | Col 111 | DG36 | `=1.852*DD36*ABS(DE36)^(1.852-1)` | =1.852*DD36*ABS(DE36)^(1.852-1) |
| Ligne 36 | Col 112 | DH36 | `=DE36+CZ70` | =DE36+CZ70 |
| Ligne 37 | Col 4 | D37 | `=DIST_PHASE_1_v2!E26` | =DIST_PHASE_1_v2!E26 |
| Ligne 37 | Col 5 | E37 | `=DIST_PHASE_1_v2!G26` | =DIST_PHASE_1_v2!G26 |
| Ligne 37 | Col 6 | F37 | `=DIST_PHASE_1_v2!L26` | =DIST_PHASE_1_v2!L26 |
| Ligne 37 | Col 7 | G37 | `=DIST_PHASE_1_v2!M26` | =DIST_PHASE_1_v2!M26 |
| Ligne 37 | Col 8 | H37 | `=DIST_PHASE_1_v2!N26` | =DIST_PHASE_1_v2!N26 |
| Ligne 37 | Col 9 | I37 | `= (10.679 * H37) / ((F37/1000)^4.871 * G37^1.852)` | = (10.679 * H37) / ((F37/1000)^4.871 * G37^1.852) |
| Ligne 37 | Col 10 | J37 | `=IF(C37="positif",E37,IF(C37="negatif",-E37,""))` | =IF(C37="positif",E37,IF(C37="negatif",-E37,"")) |
| Ligne 37 | Col 11 | K37 | `=IF(J37>0,I37*E37^1.852,-I37*E37^1.852)` | =IF(J37>0,I37*E37^1.852,-I37*E37^1.852) |
| Ligne 37 | Col 12 | L37 | `=1.852*I37*ABS(E37)^(1.852-1)` | =1.852*I37*ABS(E37)^(1.852-1) |
| Ligne 37 | Col 13 | M37 | `=J37+$D$93` | =J37+$D$93 |
| Ligne 37 | Col 16 | P37 | `=IFERROR(MATCH(S37,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S37,$D$22:$D$91,0),0) |
| Ligne 37 | Col 18 | R37 | `=DIST_PHASE_1_v2!Q26` | =DIST_PHASE_1_v2!Q26 |
| Ligne 37 | Col 19 | S37 | `=DIST_PHASE_1_v2!R26` | =DIST_PHASE_1_v2!R26 |
| Ligne 37 | Col 20 | T37 | `=DIST_PHASE_1_v2!T26` | =DIST_PHASE_1_v2!T26 |
| Ligne 37 | Col 21 | U37 | `=DIST_PHASE_1_v2!Y26` | =DIST_PHASE_1_v2!Y26 |
| Ligne 37 | Col 23 | W37 | `=DIST_PHASE_1_v2!AA26` | =DIST_PHASE_1_v2!AA26 |
| Ligne 37 | Col 24 | X37 | `= (10.679 * W37) / ((U37/1000)^4.871 * V37^1.852)` | = (10.679 * W37) / ((U37/1000)^4.871 * V37^1.852) |
| Ligne 37 | Col 25 | Y37 | `=IF(R37="positif",T37,IF(R37="negatif",-T37,""))` | =IF(R37="positif",T37,IF(R37="negatif",-T37,"")) |
| Ligne 37 | Col 26 | Z37 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E6B70>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E6B70> |
| Ligne 37 | Col 27 | AA37 | `=IF(P37>0,
IF(R37="positif",1,-1),
0)` | =IF(P37>0,
IF(R37="positif",1,-1),
0) |
| Ligne 37 | Col 28 | AB37 | `=X37*SIGN(Y37)*ABS(Y37)^1.852` | =X37*SIGN(Y37)*ABS(Y37)^1.852 |
| Ligne 37 | Col 29 | AC37 | `=1.852*X37*ABS(Y37)^(1.852-1)` | =1.852*X37*ABS(Y37)^(1.852-1) |
| Ligne 37 | Col 30 | AD37 | `=IF(P37>0,
Y37+($D$93*Z37)+(AA37*$S$93),
Y37+$S$93)` | =IF(P37>0,
Y37+($D$93*Z37)+(AA37*$S$93),
Y37+$S$93) |
| Ligne 37 | Col 32 | AF37 | `=ABS(AD37)-ABS(Y37)` | =ABS(AD37)-ABS(Y37) |
| Ligne 37 | Col 36 | AJ37 | `=IFERROR(MATCH(AM37,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM37,$S$22:$S$91,0),0) |
| Ligne 37 | Col 38 | AL37 | `=TRONCONS_V2!AI24` | =TRONCONS_V2!AI24 |
| Ligne 37 | Col 39 | AM37 | `=TRONCONS_V2!AE24` | =TRONCONS_V2!AE24 |
| Ligne 37 | Col 40 | AN37 | `=DIST_PHASE_1_v2!AG26` | =DIST_PHASE_1_v2!AG26 |
| Ligne 37 | Col 41 | AO37 | `=DIST_PHASE_1_v2!AL26` | =DIST_PHASE_1_v2!AL26 |
| Ligne 37 | Col 43 | AQ37 | `=TRONCONS_V2!AG24` | =TRONCONS_V2!AG24 |
| Ligne 37 | Col 44 | AR37 | `= (10.679 * AQ37) / ((AO37/1000)^4.871 * AP37^1.852)` | = (10.679 * AQ37) / ((AO37/1000)^4.871 * AP37^1.852) |
| Ligne 37 | Col 45 | AS37 | `=IF(AL37="positif",AN37,IF(AL37="negatif",-AN37,""))` | =IF(AL37="positif",AN37,IF(AL37="negatif",-AN37,"")) |
| Ligne 37 | Col 46 | AT37 | `=IF(AJ37>0,
IF(AS37>0, AR37*AS37^1.852,-AR37*ABS(AS37)^1.852),
IF(AS37>0, AR37*AN37^1.852, -AR37*AN37^1.852))` | =IF(AJ37>0,
IF(AS37>0, AR37*AS37^1.852,-AR37*ABS(AS37)^1.852),
IF(AS37>0, AR37*AN37^1.852, -AR37*AN37^1.852)) |
| Ligne 37 | Col 47 | AU37 | `=1.852*AR37*ABS(AS37)^(1.852-1)` | =1.852*AR37*ABS(AS37)^(1.852-1) |
| Ligne 37 | Col 48 | AV37 | `=AS37+$AN$60` | =AS37+$AN$60 |
| Ligne 37 | Col 52 | AZ37 | `=IFERROR(MATCH(BC37,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC37,$AM$22:$AM$57,0),0) |
| Ligne 37 | Col 54 | BB37 | `=DIST_PHASE_1_v2!AQ26` | =DIST_PHASE_1_v2!AQ26 |
| Ligne 37 | Col 55 | BC37 | `=DIST_PHASE_1_v2!AR26` | =DIST_PHASE_1_v2!AR26 |
| Ligne 37 | Col 56 | BD37 | `=DIST_PHASE_1_v2!AT26` | =DIST_PHASE_1_v2!AT26 |
| Ligne 37 | Col 57 | BE37 | `=DIST_PHASE_1_v2!AY26` | =DIST_PHASE_1_v2!AY26 |
| Ligne 37 | Col 58 | BF37 | `=DIST_PHASE_1_v2!AZ26` | =DIST_PHASE_1_v2!AZ26 |
| Ligne 37 | Col 59 | BG37 | `=DIST_PHASE_1_v2!BA26` | =DIST_PHASE_1_v2!BA26 |
| Ligne 37 | Col 60 | BH37 | `= (10.679 * BG37) / ((BE37/1000)^4.871 * BF37^1.852)` | = (10.679 * BG37) / ((BE37/1000)^4.871 * BF37^1.852) |
| Ligne 37 | Col 61 | BI37 | `=IF(BB37="positif",BD37,IF(BB37="negatif",-BD37,""))` | =IF(BB37="positif",BD37,IF(BB37="negatif",-BD37,"")) |
| Ligne 37 | Col 62 | BJ37 | `=IF(AZ37>0,
IF(BI37>0, BH37*BI37^1.852,-BH37*ABS(BI37)^1.852),
IF(BI37>0, BH37*BD37^1.852, -BH37*BD37^1.852))` | =IF(AZ37>0,
IF(BI37>0, BH37*BI37^1.852,-BH37*ABS(BI37)^1.852),
IF(BI37>0, BH37*BD37^1.852, -BH37*BD37^1.852)) |
| Ligne 37 | Col 63 | BK37 | `=1.852*BH37*ABS(BI37)^(1.852-1)` | =1.852*BH37*ABS(BI37)^(1.852-1) |
| Ligne 37 | Col 64 | BL37 | `=BI37+$BD$75` | =BI37+$BD$75 |
| Ligne 37 | Col 68 | BP37 | `=IFERROR(MATCH(BS37,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS37,$BC$22:$BC$73,0),0) |
| Ligne 37 | Col 70 | BR37 | `=DIST_PHASE_1_v2!BF26` | =DIST_PHASE_1_v2!BF26 |
| Ligne 37 | Col 71 | BS37 | `=DIST_PHASE_1_v2!BG26` | =DIST_PHASE_1_v2!BG26 |
| Ligne 37 | Col 72 | BT37 | `=DIST_PHASE_1_v2!BI26` | =DIST_PHASE_1_v2!BI26 |
| Ligne 37 | Col 73 | BU37 | `=DIST_PHASE_1_v2!BN26` | =DIST_PHASE_1_v2!BN26 |
| Ligne 37 | Col 74 | BV37 | `=DIST_PHASE_1_v2!BO26` | =DIST_PHASE_1_v2!BO26 |
| Ligne 37 | Col 75 | BW37 | `=DIST_PHASE_1_v2!BP26` | =DIST_PHASE_1_v2!BP26 |
| Ligne 37 | Col 76 | BX37 | `= (10.679 * BW37) / ((BU37/1000)^4.871 * BV37^1.852)` | = (10.679 * BW37) / ((BU37/1000)^4.871 * BV37^1.852) |
| Ligne 37 | Col 77 | BY37 | `=IF(BR37="positif",BT37,IF(BR37="negatif",-BT37,""))` | =IF(BR37="positif",BT37,IF(BR37="negatif",-BT37,"")) |
| Ligne 37 | Col 78 | BZ37 | `=IF(BP37>0,
IF(BY37>0, BX37*BY37^1.852,-BX37*ABS(BY37)^1.852),
IF(BY37>0, BX37*BT37^1.852, -BX37*BT37^1.852))` | =IF(BP37>0,
IF(BY37>0, BX37*BY37^1.852,-BX37*ABS(BY37)^1.852),
IF(BY37>0, BX37*BT37^1.852, -BX37*BT37^1.852)) |
| Ligne 37 | Col 79 | CA37 | `=1.852*BX37*ABS(BY37)^(1.852-1)` | =1.852*BX37*ABS(BY37)^(1.852-1) |
| Ligne 37 | Col 80 | CB37 | `=BY37+$BT$64` | =BY37+$BT$64 |
| Ligne 37 | Col 84 | CF37 | `=IFERROR(MATCH(CI37,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI37,$BS$22:$BS$62,0),0) |
| Ligne 37 | Col 86 | CH37 | `=DIST_PHASE_1_v2!BS26` | =DIST_PHASE_1_v2!BS26 |
| Ligne 37 | Col 87 | CI37 | `=DIST_PHASE_1_v2!BT26` | =DIST_PHASE_1_v2!BT26 |
| Ligne 37 | Col 88 | CJ37 | `=DIST_PHASE_1_v2!BV26` | =DIST_PHASE_1_v2!BV26 |
| Ligne 37 | Col 89 | CK37 | `=DIST_PHASE_1_v2!CA26` | =DIST_PHASE_1_v2!CA26 |
| Ligne 37 | Col 91 | CM37 | `=DIST_PHASE_1_v2!CC26` | =DIST_PHASE_1_v2!CC26 |
| Ligne 37 | Col 92 | CN37 | `= (10.679 * CM37) / ((CK37/1000)^4.871 * CL37^1.852)` | = (10.679 * CM37) / ((CK37/1000)^4.871 * CL37^1.852) |
| Ligne 37 | Col 93 | CO37 | `=IF(CH37="positif",CJ37,IF(CH37="negatif",-CJ37,""))` | =IF(CH37="positif",CJ37,IF(CH37="negatif",-CJ37,"")) |
| Ligne 37 | Col 94 | CP37 | `=IF(CF37>0,
IF(CO37>0, CN37*CO37^1.852,-CN37*ABS(CO37)^1.852),
IF(CO37>0, CN37*CJ37^1.852, -CN37*CJ37^1.852))` | =IF(CF37>0,
IF(CO37>0, CN37*CO37^1.852,-CN37*ABS(CO37)^1.852),
IF(CO37>0, CN37*CJ37^1.852, -CN37*CJ37^1.852)) |
| Ligne 37 | Col 95 | CQ37 | `=1.852*CN37*ABS(CO37)^(1.852-1)` | =1.852*CN37*ABS(CO37)^(1.852-1) |
| Ligne 37 | Col 96 | CR37 | `=CO37+$CJ$71` | =CO37+$CJ$71 |
| Ligne 37 | Col 100 | CV37 | `=IFERROR(MATCH(CY37,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY37,$CI$22:$CI$69,0),0) |
| Ligne 37 | Col 102 | CX37 | `=DIST_PHASE_1_v2!CF26` | =DIST_PHASE_1_v2!CF26 |
| Ligne 37 | Col 103 | CY37 | `=DIST_PHASE_1_v2!CG26` | =DIST_PHASE_1_v2!CG26 |
| Ligne 37 | Col 104 | CZ37 | `=DIST_PHASE_1_v2!CI26` | =DIST_PHASE_1_v2!CI26 |
| Ligne 37 | Col 105 | DA37 | `=DIST_PHASE_1_v2!CN26` | =DIST_PHASE_1_v2!CN26 |
| Ligne 37 | Col 106 | DB37 | `=DIST_PHASE_1_v2!CO26` | =DIST_PHASE_1_v2!CO26 |
| Ligne 37 | Col 107 | DC37 | `=DIST_PHASE_1_v2!CP26` | =DIST_PHASE_1_v2!CP26 |
| Ligne 37 | Col 108 | DD37 | `= (10.679 * DC37) / ((DA37/1000)^4.871 * DB37^1.852)` | = (10.679 * DC37) / ((DA37/1000)^4.871 * DB37^1.852) |
| Ligne 37 | Col 109 | DE37 | `=IF(CX37="positif",CZ37,IF(CX37="negatif",-CZ37,""))` | =IF(CX37="positif",CZ37,IF(CX37="negatif",-CZ37,"")) |
| Ligne 37 | Col 110 | DF37 | `=IF(CV37>0,
IF(DE37>0, DD37*DE37^1.852,-DD37*ABS(DE37)^1.852),
IF(DE37>0, DD37*CZ37^1.852, -DD37*CZ37^1.852))` | =IF(CV37>0,
IF(DE37>0, DD37*DE37^1.852,-DD37*ABS(DE37)^1.852),
IF(DE37>0, DD37*CZ37^1.852, -DD37*CZ37^1.852)) |
| Ligne 37 | Col 111 | DG37 | `=1.852*DD37*ABS(DE37)^(1.852-1)` | =1.852*DD37*ABS(DE37)^(1.852-1) |
| Ligne 37 | Col 112 | DH37 | `=DE37+CZ71` | =DE37+CZ71 |
| Ligne 38 | Col 4 | D38 | `=DIST_PHASE_1_v2!E27` | =DIST_PHASE_1_v2!E27 |
| Ligne 38 | Col 5 | E38 | `=DIST_PHASE_1_v2!G27` | =DIST_PHASE_1_v2!G27 |
| Ligne 38 | Col 6 | F38 | `=DIST_PHASE_1_v2!L27` | =DIST_PHASE_1_v2!L27 |
| Ligne 38 | Col 7 | G38 | `=DIST_PHASE_1_v2!M27` | =DIST_PHASE_1_v2!M27 |
| Ligne 38 | Col 8 | H38 | `=DIST_PHASE_1_v2!N27` | =DIST_PHASE_1_v2!N27 |
| Ligne 38 | Col 9 | I38 | `= (10.679 * H38) / ((F38/1000)^4.871 * G38^1.852)` | = (10.679 * H38) / ((F38/1000)^4.871 * G38^1.852) |
| Ligne 38 | Col 10 | J38 | `=IF(C38="positif",E38,IF(C38="negatif",-E38,""))` | =IF(C38="positif",E38,IF(C38="negatif",-E38,"")) |
| Ligne 38 | Col 11 | K38 | `=IF(J38>0,I38*E38^1.852,-I38*E38^1.852)` | =IF(J38>0,I38*E38^1.852,-I38*E38^1.852) |
| Ligne 38 | Col 12 | L38 | `=1.852*I38*ABS(E38)^(1.852-1)` | =1.852*I38*ABS(E38)^(1.852-1) |
| Ligne 38 | Col 13 | M38 | `=J38+$D$93` | =J38+$D$93 |
| Ligne 38 | Col 16 | P38 | `=IFERROR(MATCH(S38,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S38,$D$22:$D$91,0),0) |
| Ligne 38 | Col 18 | R38 | `=DIST_PHASE_1_v2!Q27` | =DIST_PHASE_1_v2!Q27 |
| Ligne 38 | Col 19 | S38 | `=DIST_PHASE_1_v2!R27` | =DIST_PHASE_1_v2!R27 |
| Ligne 38 | Col 20 | T38 | `=DIST_PHASE_1_v2!T27` | =DIST_PHASE_1_v2!T27 |
| Ligne 38 | Col 21 | U38 | `=DIST_PHASE_1_v2!Y27` | =DIST_PHASE_1_v2!Y27 |
| Ligne 38 | Col 23 | W38 | `=DIST_PHASE_1_v2!AA27` | =DIST_PHASE_1_v2!AA27 |
| Ligne 38 | Col 24 | X38 | `= (10.679 * W38) / ((U38/1000)^4.871 * V38^1.852)` | = (10.679 * W38) / ((U38/1000)^4.871 * V38^1.852) |
| Ligne 38 | Col 25 | Y38 | `=IF(R38="positif",T38,IF(R38="negatif",-T38,""))` | =IF(R38="positif",T38,IF(R38="negatif",-T38,"")) |
| Ligne 38 | Col 26 | Z38 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E6BD0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E6BD0> |
| Ligne 38 | Col 27 | AA38 | `=IF(P38>0,
IF(R38="positif",1,-1),
0)` | =IF(P38>0,
IF(R38="positif",1,-1),
0) |
| Ligne 38 | Col 28 | AB38 | `=X38*SIGN(Y38)*ABS(Y38)^1.852` | =X38*SIGN(Y38)*ABS(Y38)^1.852 |
| Ligne 38 | Col 29 | AC38 | `=1.852*X38*ABS(Y38)^(1.852-1)` | =1.852*X38*ABS(Y38)^(1.852-1) |
| Ligne 38 | Col 30 | AD38 | `=IF(P38>0,
Y38+($D$93*Z38)+(AA38*$S$93),
Y38+$S$93)` | =IF(P38>0,
Y38+($D$93*Z38)+(AA38*$S$93),
Y38+$S$93) |
| Ligne 38 | Col 32 | AF38 | `=ABS(AD38)-ABS(Y38)` | =ABS(AD38)-ABS(Y38) |
| Ligne 38 | Col 36 | AJ38 | `=IFERROR(MATCH(AM38,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM38,$S$22:$S$91,0),0) |
| Ligne 38 | Col 38 | AL38 | `=TRONCONS_V2!AI25` | =TRONCONS_V2!AI25 |
| Ligne 38 | Col 39 | AM38 | `=TRONCONS_V2!AE25` | =TRONCONS_V2!AE25 |
| Ligne 38 | Col 40 | AN38 | `=DIST_PHASE_1_v2!AG27` | =DIST_PHASE_1_v2!AG27 |
| Ligne 38 | Col 41 | AO38 | `=DIST_PHASE_1_v2!AL27` | =DIST_PHASE_1_v2!AL27 |
| Ligne 38 | Col 43 | AQ38 | `=TRONCONS_V2!AG25` | =TRONCONS_V2!AG25 |
| Ligne 38 | Col 44 | AR38 | `= (10.679 * AQ38) / ((AO38/1000)^4.871 * AP38^1.852)` | = (10.679 * AQ38) / ((AO38/1000)^4.871 * AP38^1.852) |
| Ligne 38 | Col 45 | AS38 | `=IF(AL38="positif",AN38,IF(AL38="negatif",-AN38,""))` | =IF(AL38="positif",AN38,IF(AL38="negatif",-AN38,"")) |
| Ligne 38 | Col 46 | AT38 | `=IF(AJ38>0,
IF(AS38>0, AR38*AS38^1.852,-AR38*ABS(AS38)^1.852),
IF(AS38>0, AR38*AN38^1.852, -AR38*AN38^1.852))` | =IF(AJ38>0,
IF(AS38>0, AR38*AS38^1.852,-AR38*ABS(AS38)^1.852),
IF(AS38>0, AR38*AN38^1.852, -AR38*AN38^1.852)) |
| Ligne 38 | Col 47 | AU38 | `=1.852*AR38*ABS(AS38)^(1.852-1)` | =1.852*AR38*ABS(AS38)^(1.852-1) |
| Ligne 38 | Col 48 | AV38 | `=AS38+$AN$60` | =AS38+$AN$60 |
| Ligne 38 | Col 52 | AZ38 | `=IFERROR(MATCH(BC38,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC38,$AM$22:$AM$57,0),0) |
| Ligne 38 | Col 54 | BB38 | `=DIST_PHASE_1_v2!AQ27` | =DIST_PHASE_1_v2!AQ27 |
| Ligne 38 | Col 55 | BC38 | `=DIST_PHASE_1_v2!AR27` | =DIST_PHASE_1_v2!AR27 |
| Ligne 38 | Col 56 | BD38 | `=DIST_PHASE_1_v2!AT27` | =DIST_PHASE_1_v2!AT27 |
| Ligne 38 | Col 57 | BE38 | `=DIST_PHASE_1_v2!AY27` | =DIST_PHASE_1_v2!AY27 |
| Ligne 38 | Col 58 | BF38 | `=DIST_PHASE_1_v2!AZ27` | =DIST_PHASE_1_v2!AZ27 |
| Ligne 38 | Col 59 | BG38 | `=DIST_PHASE_1_v2!BA27` | =DIST_PHASE_1_v2!BA27 |
| Ligne 38 | Col 60 | BH38 | `= (10.679 * BG38) / ((BE38/1000)^4.871 * BF38^1.852)` | = (10.679 * BG38) / ((BE38/1000)^4.871 * BF38^1.852) |
| Ligne 38 | Col 61 | BI38 | `=IF(BB38="positif",BD38,IF(BB38="negatif",-BD38,""))` | =IF(BB38="positif",BD38,IF(BB38="negatif",-BD38,"")) |
| Ligne 38 | Col 62 | BJ38 | `=IF(AZ38>0,
IF(BI38>0, BH38*BI38^1.852,-BH38*ABS(BI38)^1.852),
IF(BI38>0, BH38*BD38^1.852, -BH38*BD38^1.852))` | =IF(AZ38>0,
IF(BI38>0, BH38*BI38^1.852,-BH38*ABS(BI38)^1.852),
IF(BI38>0, BH38*BD38^1.852, -BH38*BD38^1.852)) |
| Ligne 38 | Col 63 | BK38 | `=1.852*BH38*ABS(BI38)^(1.852-1)` | =1.852*BH38*ABS(BI38)^(1.852-1) |
| Ligne 38 | Col 64 | BL38 | `=BI38+$BD$75` | =BI38+$BD$75 |
| Ligne 38 | Col 68 | BP38 | `=IFERROR(MATCH(BS38,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS38,$BC$22:$BC$73,0),0) |
| Ligne 38 | Col 70 | BR38 | `=DIST_PHASE_1_v2!BF27` | =DIST_PHASE_1_v2!BF27 |
| Ligne 38 | Col 71 | BS38 | `=DIST_PHASE_1_v2!BG27` | =DIST_PHASE_1_v2!BG27 |
| Ligne 38 | Col 72 | BT38 | `=DIST_PHASE_1_v2!BI27` | =DIST_PHASE_1_v2!BI27 |
| Ligne 38 | Col 73 | BU38 | `=DIST_PHASE_1_v2!BN27` | =DIST_PHASE_1_v2!BN27 |
| Ligne 38 | Col 74 | BV38 | `=DIST_PHASE_1_v2!BO27` | =DIST_PHASE_1_v2!BO27 |
| Ligne 38 | Col 75 | BW38 | `=DIST_PHASE_1_v2!BP27` | =DIST_PHASE_1_v2!BP27 |
| Ligne 38 | Col 76 | BX38 | `= (10.679 * BW38) / ((BU38/1000)^4.871 * BV38^1.852)` | = (10.679 * BW38) / ((BU38/1000)^4.871 * BV38^1.852) |
| Ligne 38 | Col 77 | BY38 | `=IF(BR38="positif",BT38,IF(BR38="negatif",-BT38,""))` | =IF(BR38="positif",BT38,IF(BR38="negatif",-BT38,"")) |
| Ligne 38 | Col 78 | BZ38 | `=IF(BP38>0,
IF(BY38>0, BX38*BY38^1.852,-BX38*ABS(BY38)^1.852),
IF(BY38>0, BX38*BT38^1.852, -BX38*BT38^1.852))` | =IF(BP38>0,
IF(BY38>0, BX38*BY38^1.852,-BX38*ABS(BY38)^1.852),
IF(BY38>0, BX38*BT38^1.852, -BX38*BT38^1.852)) |
| Ligne 38 | Col 79 | CA38 | `=1.852*BX38*ABS(BY38)^(1.852-1)` | =1.852*BX38*ABS(BY38)^(1.852-1) |
| Ligne 38 | Col 80 | CB38 | `=BY38+$BT$64` | =BY38+$BT$64 |
| Ligne 38 | Col 84 | CF38 | `=IFERROR(MATCH(CI38,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI38,$BS$22:$BS$62,0),0) |
| Ligne 38 | Col 86 | CH38 | `=DIST_PHASE_1_v2!BS27` | =DIST_PHASE_1_v2!BS27 |
| Ligne 38 | Col 87 | CI38 | `=DIST_PHASE_1_v2!BT27` | =DIST_PHASE_1_v2!BT27 |
| Ligne 38 | Col 88 | CJ38 | `=DIST_PHASE_1_v2!BV27` | =DIST_PHASE_1_v2!BV27 |
| Ligne 38 | Col 89 | CK38 | `=DIST_PHASE_1_v2!CA27` | =DIST_PHASE_1_v2!CA27 |
| Ligne 38 | Col 91 | CM38 | `=DIST_PHASE_1_v2!CC27` | =DIST_PHASE_1_v2!CC27 |
| Ligne 38 | Col 92 | CN38 | `= (10.679 * CM38) / ((CK38/1000)^4.871 * CL38^1.852)` | = (10.679 * CM38) / ((CK38/1000)^4.871 * CL38^1.852) |
| Ligne 38 | Col 93 | CO38 | `=IF(CH38="positif",CJ38,IF(CH38="negatif",-CJ38,""))` | =IF(CH38="positif",CJ38,IF(CH38="negatif",-CJ38,"")) |
| Ligne 38 | Col 94 | CP38 | `=IF(CF38>0,
IF(CO38>0, CN38*CO38^1.852,-CN38*ABS(CO38)^1.852),
IF(CO38>0, CN38*CJ38^1.852, -CN38*CJ38^1.852))` | =IF(CF38>0,
IF(CO38>0, CN38*CO38^1.852,-CN38*ABS(CO38)^1.852),
IF(CO38>0, CN38*CJ38^1.852, -CN38*CJ38^1.852)) |
| Ligne 38 | Col 95 | CQ38 | `=1.852*CN38*ABS(CO38)^(1.852-1)` | =1.852*CN38*ABS(CO38)^(1.852-1) |
| Ligne 38 | Col 96 | CR38 | `=CO38+$CJ$71` | =CO38+$CJ$71 |
| Ligne 38 | Col 100 | CV38 | `=IFERROR(MATCH(CY38,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY38,$CI$22:$CI$69,0),0) |
| Ligne 38 | Col 102 | CX38 | `=DIST_PHASE_1_v2!CF27` | =DIST_PHASE_1_v2!CF27 |
| Ligne 38 | Col 103 | CY38 | `=DIST_PHASE_1_v2!CG27` | =DIST_PHASE_1_v2!CG27 |
| Ligne 38 | Col 104 | CZ38 | `=DIST_PHASE_1_v2!CI27` | =DIST_PHASE_1_v2!CI27 |
| Ligne 38 | Col 105 | DA38 | `=DIST_PHASE_1_v2!CN27` | =DIST_PHASE_1_v2!CN27 |
| Ligne 38 | Col 106 | DB38 | `=DIST_PHASE_1_v2!CO27` | =DIST_PHASE_1_v2!CO27 |
| Ligne 38 | Col 107 | DC38 | `=DIST_PHASE_1_v2!CP27` | =DIST_PHASE_1_v2!CP27 |
| Ligne 38 | Col 108 | DD38 | `= (10.679 * DC38) / ((DA38/1000)^4.871 * DB38^1.852)` | = (10.679 * DC38) / ((DA38/1000)^4.871 * DB38^1.852) |
| Ligne 38 | Col 109 | DE38 | `=IF(CX38="positif",CZ38,IF(CX38="negatif",-CZ38,""))` | =IF(CX38="positif",CZ38,IF(CX38="negatif",-CZ38,"")) |
| Ligne 38 | Col 110 | DF38 | `=IF(CV38>0,
IF(DE38>0, DD38*DE38^1.852,-DD38*ABS(DE38)^1.852),
IF(DE38>0, DD38*CZ38^1.852, -DD38*CZ38^1.852))` | =IF(CV38>0,
IF(DE38>0, DD38*DE38^1.852,-DD38*ABS(DE38)^1.852),
IF(DE38>0, DD38*CZ38^1.852, -DD38*CZ38^1.852)) |
| Ligne 38 | Col 111 | DG38 | `=1.852*DD38*ABS(DE38)^(1.852-1)` | =1.852*DD38*ABS(DE38)^(1.852-1) |
| Ligne 38 | Col 112 | DH38 | `=DE38+CZ72` | =DE38+CZ72 |
| Ligne 39 | Col 4 | D39 | `=DIST_PHASE_1_v2!E28` | =DIST_PHASE_1_v2!E28 |
| Ligne 39 | Col 5 | E39 | `=DIST_PHASE_1_v2!G28` | =DIST_PHASE_1_v2!G28 |
| Ligne 39 | Col 6 | F39 | `=DIST_PHASE_1_v2!L28` | =DIST_PHASE_1_v2!L28 |
| Ligne 39 | Col 7 | G39 | `=DIST_PHASE_1_v2!M28` | =DIST_PHASE_1_v2!M28 |
| Ligne 39 | Col 8 | H39 | `=DIST_PHASE_1_v2!N28` | =DIST_PHASE_1_v2!N28 |
| Ligne 39 | Col 9 | I39 | `= (10.679 * H39) / ((F39/1000)^4.871 * G39^1.852)` | = (10.679 * H39) / ((F39/1000)^4.871 * G39^1.852) |
| Ligne 39 | Col 10 | J39 | `=IF(C39="positif",E39,IF(C39="negatif",-E39,""))` | =IF(C39="positif",E39,IF(C39="negatif",-E39,"")) |
| Ligne 39 | Col 11 | K39 | `=IF(J39>0,I39*E39^1.852,-I39*E39^1.852)` | =IF(J39>0,I39*E39^1.852,-I39*E39^1.852) |
| Ligne 39 | Col 12 | L39 | `=1.852*I39*ABS(E39)^(1.852-1)` | =1.852*I39*ABS(E39)^(1.852-1) |
| Ligne 39 | Col 13 | M39 | `=J39+$D$93` | =J39+$D$93 |
| Ligne 39 | Col 16 | P39 | `=IFERROR(MATCH(S39,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S39,$D$22:$D$91,0),0) |
| Ligne 39 | Col 18 | R39 | `=DIST_PHASE_1_v2!Q28` | =DIST_PHASE_1_v2!Q28 |
| Ligne 39 | Col 19 | S39 | `=DIST_PHASE_1_v2!R28` | =DIST_PHASE_1_v2!R28 |
| Ligne 39 | Col 20 | T39 | `=DIST_PHASE_1_v2!T28` | =DIST_PHASE_1_v2!T28 |
| Ligne 39 | Col 21 | U39 | `=DIST_PHASE_1_v2!Y28` | =DIST_PHASE_1_v2!Y28 |
| Ligne 39 | Col 23 | W39 | `=DIST_PHASE_1_v2!AA28` | =DIST_PHASE_1_v2!AA28 |
| Ligne 39 | Col 24 | X39 | `= (10.679 * W39) / ((U39/1000)^4.871 * V39^1.852)` | = (10.679 * W39) / ((U39/1000)^4.871 * V39^1.852) |
| Ligne 39 | Col 25 | Y39 | `=IF(R39="positif",T39,IF(R39="negatif",-T39,""))` | =IF(R39="positif",T39,IF(R39="negatif",-T39,"")) |
| Ligne 39 | Col 26 | Z39 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E78F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E78F0> |
| Ligne 39 | Col 27 | AA39 | `=IF(P39>0,
IF(R39="positif",1,-1),
0)` | =IF(P39>0,
IF(R39="positif",1,-1),
0) |
| Ligne 39 | Col 28 | AB39 | `=X39*SIGN(Y39)*ABS(Y39)^1.852` | =X39*SIGN(Y39)*ABS(Y39)^1.852 |
| Ligne 39 | Col 29 | AC39 | `=1.852*X39*ABS(Y39)^(1.852-1)` | =1.852*X39*ABS(Y39)^(1.852-1) |
| Ligne 39 | Col 30 | AD39 | `=IF(P39>0,
Y39+($D$93*Z39)+(AA39*$S$93),
Y39+$S$93)` | =IF(P39>0,
Y39+($D$93*Z39)+(AA39*$S$93),
Y39+$S$93) |
| Ligne 39 | Col 32 | AF39 | `=ABS(AD39)-ABS(Y39)` | =ABS(AD39)-ABS(Y39) |
| Ligne 39 | Col 36 | AJ39 | `=IFERROR(MATCH(AM39,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM39,$S$22:$S$91,0),0) |
| Ligne 39 | Col 38 | AL39 | `=TRONCONS_V2!AI26` | =TRONCONS_V2!AI26 |
| Ligne 39 | Col 39 | AM39 | `=TRONCONS_V2!AE26` | =TRONCONS_V2!AE26 |
| Ligne 39 | Col 40 | AN39 | `=DIST_PHASE_1_v2!AG28` | =DIST_PHASE_1_v2!AG28 |
| Ligne 39 | Col 41 | AO39 | `=DIST_PHASE_1_v2!AL28` | =DIST_PHASE_1_v2!AL28 |
| Ligne 39 | Col 43 | AQ39 | `=TRONCONS_V2!AG26` | =TRONCONS_V2!AG26 |
| Ligne 39 | Col 44 | AR39 | `= (10.679 * AQ39) / ((AO39/1000)^4.871 * AP39^1.852)` | = (10.679 * AQ39) / ((AO39/1000)^4.871 * AP39^1.852) |
| Ligne 39 | Col 45 | AS39 | `=IF(AL39="positif",AN39,IF(AL39="negatif",-AN39,""))` | =IF(AL39="positif",AN39,IF(AL39="negatif",-AN39,"")) |
| Ligne 39 | Col 46 | AT39 | `=IF(AJ39>0,
IF(AS39>0, AR39*AS39^1.852,-AR39*ABS(AS39)^1.852),
IF(AS39>0, AR39*AN39^1.852, -AR39*AN39^1.852))` | =IF(AJ39>0,
IF(AS39>0, AR39*AS39^1.852,-AR39*ABS(AS39)^1.852),
IF(AS39>0, AR39*AN39^1.852, -AR39*AN39^1.852)) |
| Ligne 39 | Col 47 | AU39 | `=1.852*AR39*ABS(AS39)^(1.852-1)` | =1.852*AR39*ABS(AS39)^(1.852-1) |
| Ligne 39 | Col 48 | AV39 | `=AS39+$AN$60` | =AS39+$AN$60 |
| Ligne 39 | Col 52 | AZ39 | `=IFERROR(MATCH(BC39,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC39,$AM$22:$AM$57,0),0) |
| Ligne 39 | Col 54 | BB39 | `=DIST_PHASE_1_v2!AQ28` | =DIST_PHASE_1_v2!AQ28 |
| Ligne 39 | Col 55 | BC39 | `=DIST_PHASE_1_v2!AR28` | =DIST_PHASE_1_v2!AR28 |
| Ligne 39 | Col 56 | BD39 | `=DIST_PHASE_1_v2!AT28` | =DIST_PHASE_1_v2!AT28 |
| Ligne 39 | Col 57 | BE39 | `=DIST_PHASE_1_v2!AY28` | =DIST_PHASE_1_v2!AY28 |
| Ligne 39 | Col 58 | BF39 | `=DIST_PHASE_1_v2!AZ28` | =DIST_PHASE_1_v2!AZ28 |
| Ligne 39 | Col 59 | BG39 | `=DIST_PHASE_1_v2!BA28` | =DIST_PHASE_1_v2!BA28 |
| Ligne 39 | Col 60 | BH39 | `= (10.679 * BG39) / ((BE39/1000)^4.871 * BF39^1.852)` | = (10.679 * BG39) / ((BE39/1000)^4.871 * BF39^1.852) |
| Ligne 39 | Col 61 | BI39 | `=IF(BB39="positif",BD39,IF(BB39="negatif",-BD39,""))` | =IF(BB39="positif",BD39,IF(BB39="negatif",-BD39,"")) |
| Ligne 39 | Col 62 | BJ39 | `=IF(AZ39>0,
IF(BI39>0, BH39*BI39^1.852,-BH39*ABS(BI39)^1.852),
IF(BI39>0, BH39*BD39^1.852, -BH39*BD39^1.852))` | =IF(AZ39>0,
IF(BI39>0, BH39*BI39^1.852,-BH39*ABS(BI39)^1.852),
IF(BI39>0, BH39*BD39^1.852, -BH39*BD39^1.852)) |
| Ligne 39 | Col 63 | BK39 | `=1.852*BH39*ABS(BI39)^(1.852-1)` | =1.852*BH39*ABS(BI39)^(1.852-1) |
| Ligne 39 | Col 64 | BL39 | `=BI39+$BD$75` | =BI39+$BD$75 |
| Ligne 39 | Col 68 | BP39 | `=IFERROR(MATCH(BS39,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS39,$BC$22:$BC$73,0),0) |
| Ligne 39 | Col 70 | BR39 | `=DIST_PHASE_1_v2!BF28` | =DIST_PHASE_1_v2!BF28 |
| Ligne 39 | Col 71 | BS39 | `=DIST_PHASE_1_v2!BG28` | =DIST_PHASE_1_v2!BG28 |
| Ligne 39 | Col 72 | BT39 | `=DIST_PHASE_1_v2!BI28` | =DIST_PHASE_1_v2!BI28 |
| Ligne 39 | Col 73 | BU39 | `=DIST_PHASE_1_v2!BN28` | =DIST_PHASE_1_v2!BN28 |
| Ligne 39 | Col 74 | BV39 | `=DIST_PHASE_1_v2!BO28` | =DIST_PHASE_1_v2!BO28 |
| Ligne 39 | Col 75 | BW39 | `=DIST_PHASE_1_v2!BP28` | =DIST_PHASE_1_v2!BP28 |
| Ligne 39 | Col 76 | BX39 | `= (10.679 * BW39) / ((BU39/1000)^4.871 * BV39^1.852)` | = (10.679 * BW39) / ((BU39/1000)^4.871 * BV39^1.852) |
| Ligne 39 | Col 77 | BY39 | `=IF(BR39="positif",BT39,IF(BR39="negatif",-BT39,""))` | =IF(BR39="positif",BT39,IF(BR39="negatif",-BT39,"")) |
| Ligne 39 | Col 78 | BZ39 | `=IF(BP39>0,
IF(BY39>0, BX39*BY39^1.852,-BX39*ABS(BY39)^1.852),
IF(BY39>0, BX39*BT39^1.852, -BX39*BT39^1.852))` | =IF(BP39>0,
IF(BY39>0, BX39*BY39^1.852,-BX39*ABS(BY39)^1.852),
IF(BY39>0, BX39*BT39^1.852, -BX39*BT39^1.852)) |
| Ligne 39 | Col 79 | CA39 | `=1.852*BX39*ABS(BY39)^(1.852-1)` | =1.852*BX39*ABS(BY39)^(1.852-1) |
| Ligne 39 | Col 80 | CB39 | `=BY39+$BT$64` | =BY39+$BT$64 |
| Ligne 39 | Col 84 | CF39 | `=IFERROR(MATCH(CI39,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI39,$BS$22:$BS$62,0),0) |
| Ligne 39 | Col 86 | CH39 | `=DIST_PHASE_1_v2!BS28` | =DIST_PHASE_1_v2!BS28 |
| Ligne 39 | Col 87 | CI39 | `=DIST_PHASE_1_v2!BT28` | =DIST_PHASE_1_v2!BT28 |
| Ligne 39 | Col 88 | CJ39 | `=DIST_PHASE_1_v2!BV28` | =DIST_PHASE_1_v2!BV28 |
| Ligne 39 | Col 89 | CK39 | `=DIST_PHASE_1_v2!CA28` | =DIST_PHASE_1_v2!CA28 |
| Ligne 39 | Col 91 | CM39 | `=DIST_PHASE_1_v2!CC28` | =DIST_PHASE_1_v2!CC28 |
| Ligne 39 | Col 92 | CN39 | `= (10.679 * CM39) / ((CK39/1000)^4.871 * CL39^1.852)` | = (10.679 * CM39) / ((CK39/1000)^4.871 * CL39^1.852) |
| Ligne 39 | Col 93 | CO39 | `=IF(CH39="positif",CJ39,IF(CH39="negatif",-CJ39,""))` | =IF(CH39="positif",CJ39,IF(CH39="negatif",-CJ39,"")) |
| Ligne 39 | Col 94 | CP39 | `=IF(CF39>0,
IF(CO39>0, CN39*CO39^1.852,-CN39*ABS(CO39)^1.852),
IF(CO39>0, CN39*CJ39^1.852, -CN39*CJ39^1.852))` | =IF(CF39>0,
IF(CO39>0, CN39*CO39^1.852,-CN39*ABS(CO39)^1.852),
IF(CO39>0, CN39*CJ39^1.852, -CN39*CJ39^1.852)) |
| Ligne 39 | Col 95 | CQ39 | `=1.852*CN39*ABS(CO39)^(1.852-1)` | =1.852*CN39*ABS(CO39)^(1.852-1) |
| Ligne 39 | Col 96 | CR39 | `=CO39+$CJ$71` | =CO39+$CJ$71 |
| Ligne 39 | Col 100 | CV39 | `=IFERROR(MATCH(CY39,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY39,$CI$22:$CI$69,0),0) |
| Ligne 39 | Col 102 | CX39 | `=DIST_PHASE_1_v2!CF28` | =DIST_PHASE_1_v2!CF28 |
| Ligne 39 | Col 103 | CY39 | `=DIST_PHASE_1_v2!CG28` | =DIST_PHASE_1_v2!CG28 |
| Ligne 39 | Col 104 | CZ39 | `=DIST_PHASE_1_v2!CI28` | =DIST_PHASE_1_v2!CI28 |
| Ligne 39 | Col 105 | DA39 | `=DIST_PHASE_1_v2!CN28` | =DIST_PHASE_1_v2!CN28 |
| Ligne 39 | Col 106 | DB39 | `=DIST_PHASE_1_v2!CO28` | =DIST_PHASE_1_v2!CO28 |
| Ligne 39 | Col 107 | DC39 | `=DIST_PHASE_1_v2!CP28` | =DIST_PHASE_1_v2!CP28 |
| Ligne 39 | Col 108 | DD39 | `= (10.679 * DC39) / ((DA39/1000)^4.871 * DB39^1.852)` | = (10.679 * DC39) / ((DA39/1000)^4.871 * DB39^1.852) |
| Ligne 39 | Col 109 | DE39 | `=IF(CX39="positif",CZ39,IF(CX39="negatif",-CZ39,""))` | =IF(CX39="positif",CZ39,IF(CX39="negatif",-CZ39,"")) |
| Ligne 39 | Col 110 | DF39 | `=IF(CV39>0,
IF(DE39>0, DD39*DE39^1.852,-DD39*ABS(DE39)^1.852),
IF(DE39>0, DD39*CZ39^1.852, -DD39*CZ39^1.852))` | =IF(CV39>0,
IF(DE39>0, DD39*DE39^1.852,-DD39*ABS(DE39)^1.852),
IF(DE39>0, DD39*CZ39^1.852, -DD39*CZ39^1.852)) |
| Ligne 39 | Col 111 | DG39 | `=1.852*DD39*ABS(DE39)^(1.852-1)` | =1.852*DD39*ABS(DE39)^(1.852-1) |
| Ligne 39 | Col 112 | DH39 | `=DE39+CZ73` | =DE39+CZ73 |
| Ligne 40 | Col 4 | D40 | `=DIST_PHASE_1_v2!E29` | =DIST_PHASE_1_v2!E29 |
| Ligne 40 | Col 5 | E40 | `=DIST_PHASE_1_v2!G29` | =DIST_PHASE_1_v2!G29 |
| Ligne 40 | Col 6 | F40 | `=DIST_PHASE_1_v2!L29` | =DIST_PHASE_1_v2!L29 |
| Ligne 40 | Col 7 | G40 | `=DIST_PHASE_1_v2!M29` | =DIST_PHASE_1_v2!M29 |
| Ligne 40 | Col 8 | H40 | `=DIST_PHASE_1_v2!N29` | =DIST_PHASE_1_v2!N29 |
| Ligne 40 | Col 9 | I40 | `= (10.679 * H40) / ((F40/1000)^4.871 * G40^1.852)` | = (10.679 * H40) / ((F40/1000)^4.871 * G40^1.852) |
| Ligne 40 | Col 10 | J40 | `=IF(C40="positif",E40,IF(C40="negatif",-E40,""))` | =IF(C40="positif",E40,IF(C40="negatif",-E40,"")) |
| Ligne 40 | Col 11 | K40 | `=IF(J40>0,I40*E40^1.852,-I40*E40^1.852)` | =IF(J40>0,I40*E40^1.852,-I40*E40^1.852) |
| Ligne 40 | Col 12 | L40 | `=1.852*I40*ABS(E40)^(1.852-1)` | =1.852*I40*ABS(E40)^(1.852-1) |
| Ligne 40 | Col 13 | M40 | `=J40+$D$93` | =J40+$D$93 |
| Ligne 40 | Col 16 | P40 | `=IFERROR(MATCH(S40,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S40,$D$22:$D$91,0),0) |
| Ligne 40 | Col 18 | R40 | `=DIST_PHASE_1_v2!Q29` | =DIST_PHASE_1_v2!Q29 |
| Ligne 40 | Col 19 | S40 | `=DIST_PHASE_1_v2!R29` | =DIST_PHASE_1_v2!R29 |
| Ligne 40 | Col 20 | T40 | `=DIST_PHASE_1_v2!T29` | =DIST_PHASE_1_v2!T29 |
| Ligne 40 | Col 21 | U40 | `=DIST_PHASE_1_v2!Y29` | =DIST_PHASE_1_v2!Y29 |
| Ligne 40 | Col 23 | W40 | `=DIST_PHASE_1_v2!AA29` | =DIST_PHASE_1_v2!AA29 |
| Ligne 40 | Col 24 | X40 | `= (10.679 * W40) / ((U40/1000)^4.871 * V40^1.852)` | = (10.679 * W40) / ((U40/1000)^4.871 * V40^1.852) |
| Ligne 40 | Col 25 | Y40 | `=IF(R40="positif",T40,IF(R40="negatif",-T40,""))` | =IF(R40="positif",T40,IF(R40="negatif",-T40,"")) |
| Ligne 40 | Col 26 | Z40 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E7D70>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E7D70> |
| Ligne 40 | Col 27 | AA40 | `=IF(P40>0,
IF(R40="positif",1,-1),
0)` | =IF(P40>0,
IF(R40="positif",1,-1),
0) |
| Ligne 40 | Col 28 | AB40 | `=X40*SIGN(Y40)*ABS(Y40)^1.852` | =X40*SIGN(Y40)*ABS(Y40)^1.852 |
| Ligne 40 | Col 29 | AC40 | `=1.852*X40*ABS(Y40)^(1.852-1)` | =1.852*X40*ABS(Y40)^(1.852-1) |
| Ligne 40 | Col 30 | AD40 | `=IF(P40>0,
Y40+($D$93*Z40)+(AA40*$S$93),
Y40+$S$93)` | =IF(P40>0,
Y40+($D$93*Z40)+(AA40*$S$93),
Y40+$S$93) |
| Ligne 40 | Col 32 | AF40 | `=ABS(AD40)-ABS(Y40)` | =ABS(AD40)-ABS(Y40) |
| Ligne 40 | Col 36 | AJ40 | `=IFERROR(MATCH(AM40,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM40,$S$22:$S$91,0),0) |
| Ligne 40 | Col 38 | AL40 | `=TRONCONS_V2!AI27` | =TRONCONS_V2!AI27 |
| Ligne 40 | Col 39 | AM40 | `=TRONCONS_V2!AE27` | =TRONCONS_V2!AE27 |
| Ligne 40 | Col 40 | AN40 | `=DIST_PHASE_1_v2!AG29` | =DIST_PHASE_1_v2!AG29 |
| Ligne 40 | Col 41 | AO40 | `=DIST_PHASE_1_v2!AL29` | =DIST_PHASE_1_v2!AL29 |
| Ligne 40 | Col 43 | AQ40 | `=TRONCONS_V2!AG27` | =TRONCONS_V2!AG27 |
| Ligne 40 | Col 44 | AR40 | `= (10.679 * AQ40) / ((AO40/1000)^4.871 * AP40^1.852)` | = (10.679 * AQ40) / ((AO40/1000)^4.871 * AP40^1.852) |
| Ligne 40 | Col 45 | AS40 | `=IF(AL40="positif",AN40,IF(AL40="negatif",-AN40,""))` | =IF(AL40="positif",AN40,IF(AL40="negatif",-AN40,"")) |
| Ligne 40 | Col 46 | AT40 | `=IF(AJ40>0,
IF(AS40>0, AR40*AS40^1.852,-AR40*ABS(AS40)^1.852),
IF(AS40>0, AR40*AN40^1.852, -AR40*AN40^1.852))` | =IF(AJ40>0,
IF(AS40>0, AR40*AS40^1.852,-AR40*ABS(AS40)^1.852),
IF(AS40>0, AR40*AN40^1.852, -AR40*AN40^1.852)) |
| Ligne 40 | Col 47 | AU40 | `=1.852*AR40*ABS(AS40)^(1.852-1)` | =1.852*AR40*ABS(AS40)^(1.852-1) |
| Ligne 40 | Col 48 | AV40 | `=AS40+$AN$60` | =AS40+$AN$60 |
| Ligne 40 | Col 52 | AZ40 | `=IFERROR(MATCH(BC40,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC40,$AM$22:$AM$57,0),0) |
| Ligne 40 | Col 54 | BB40 | `=DIST_PHASE_1_v2!AQ29` | =DIST_PHASE_1_v2!AQ29 |
| Ligne 40 | Col 55 | BC40 | `=DIST_PHASE_1_v2!AR29` | =DIST_PHASE_1_v2!AR29 |
| Ligne 40 | Col 56 | BD40 | `=DIST_PHASE_1_v2!AT29` | =DIST_PHASE_1_v2!AT29 |
| Ligne 40 | Col 57 | BE40 | `=DIST_PHASE_1_v2!AY29` | =DIST_PHASE_1_v2!AY29 |
| Ligne 40 | Col 58 | BF40 | `=DIST_PHASE_1_v2!AZ29` | =DIST_PHASE_1_v2!AZ29 |
| Ligne 40 | Col 59 | BG40 | `=DIST_PHASE_1_v2!BA29` | =DIST_PHASE_1_v2!BA29 |
| Ligne 40 | Col 60 | BH40 | `= (10.679 * BG40) / ((BE40/1000)^4.871 * BF40^1.852)` | = (10.679 * BG40) / ((BE40/1000)^4.871 * BF40^1.852) |
| Ligne 40 | Col 61 | BI40 | `=IF(BB40="positif",BD40,IF(BB40="negatif",-BD40,""))` | =IF(BB40="positif",BD40,IF(BB40="negatif",-BD40,"")) |
| Ligne 40 | Col 62 | BJ40 | `=IF(AZ40>0,
IF(BI40>0, BH40*BI40^1.852,-BH40*ABS(BI40)^1.852),
IF(BI40>0, BH40*BD40^1.852, -BH40*BD40^1.852))` | =IF(AZ40>0,
IF(BI40>0, BH40*BI40^1.852,-BH40*ABS(BI40)^1.852),
IF(BI40>0, BH40*BD40^1.852, -BH40*BD40^1.852)) |
| Ligne 40 | Col 63 | BK40 | `=1.852*BH40*ABS(BI40)^(1.852-1)` | =1.852*BH40*ABS(BI40)^(1.852-1) |
| Ligne 40 | Col 64 | BL40 | `=BI40+$BD$75` | =BI40+$BD$75 |
| Ligne 40 | Col 68 | BP40 | `=IFERROR(MATCH(BS40,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS40,$BC$22:$BC$73,0),0) |
| Ligne 40 | Col 70 | BR40 | `=DIST_PHASE_1_v2!BF29` | =DIST_PHASE_1_v2!BF29 |
| Ligne 40 | Col 71 | BS40 | `=DIST_PHASE_1_v2!BG29` | =DIST_PHASE_1_v2!BG29 |
| Ligne 40 | Col 72 | BT40 | `=DIST_PHASE_1_v2!BI29` | =DIST_PHASE_1_v2!BI29 |
| Ligne 40 | Col 73 | BU40 | `=DIST_PHASE_1_v2!BN29` | =DIST_PHASE_1_v2!BN29 |
| Ligne 40 | Col 74 | BV40 | `=DIST_PHASE_1_v2!BO29` | =DIST_PHASE_1_v2!BO29 |
| Ligne 40 | Col 75 | BW40 | `=DIST_PHASE_1_v2!BP29` | =DIST_PHASE_1_v2!BP29 |
| Ligne 40 | Col 76 | BX40 | `= (10.679 * BW40) / ((BU40/1000)^4.871 * BV40^1.852)` | = (10.679 * BW40) / ((BU40/1000)^4.871 * BV40^1.852) |
| Ligne 40 | Col 77 | BY40 | `=IF(BR40="positif",BT40,IF(BR40="negatif",-BT40,""))` | =IF(BR40="positif",BT40,IF(BR40="negatif",-BT40,"")) |
| Ligne 40 | Col 78 | BZ40 | `=IF(BP40>0,
IF(BY40>0, BX40*BY40^1.852,-BX40*ABS(BY40)^1.852),
IF(BY40>0, BX40*BT40^1.852, -BX40*BT40^1.852))` | =IF(BP40>0,
IF(BY40>0, BX40*BY40^1.852,-BX40*ABS(BY40)^1.852),
IF(BY40>0, BX40*BT40^1.852, -BX40*BT40^1.852)) |
| Ligne 40 | Col 79 | CA40 | `=1.852*BX40*ABS(BY40)^(1.852-1)` | =1.852*BX40*ABS(BY40)^(1.852-1) |
| Ligne 40 | Col 80 | CB40 | `=BY40+$BT$64` | =BY40+$BT$64 |
| Ligne 40 | Col 84 | CF40 | `=IFERROR(MATCH(CI40,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI40,$BS$22:$BS$62,0),0) |
| Ligne 40 | Col 86 | CH40 | `=DIST_PHASE_1_v2!BS29` | =DIST_PHASE_1_v2!BS29 |
| Ligne 40 | Col 87 | CI40 | `=DIST_PHASE_1_v2!BT29` | =DIST_PHASE_1_v2!BT29 |
| Ligne 40 | Col 88 | CJ40 | `=DIST_PHASE_1_v2!BV29` | =DIST_PHASE_1_v2!BV29 |
| Ligne 40 | Col 89 | CK40 | `=DIST_PHASE_1_v2!CA29` | =DIST_PHASE_1_v2!CA29 |
| Ligne 40 | Col 91 | CM40 | `=DIST_PHASE_1_v2!CC29` | =DIST_PHASE_1_v2!CC29 |
| Ligne 40 | Col 92 | CN40 | `= (10.679 * CM40) / ((CK40/1000)^4.871 * CL40^1.852)` | = (10.679 * CM40) / ((CK40/1000)^4.871 * CL40^1.852) |
| Ligne 40 | Col 93 | CO40 | `=IF(CH40="positif",CJ40,IF(CH40="negatif",-CJ40,""))` | =IF(CH40="positif",CJ40,IF(CH40="negatif",-CJ40,"")) |
| Ligne 40 | Col 94 | CP40 | `=IF(CF40>0,
IF(CO40>0, CN40*CO40^1.852,-CN40*ABS(CO40)^1.852),
IF(CO40>0, CN40*CJ40^1.852, -CN40*CJ40^1.852))` | =IF(CF40>0,
IF(CO40>0, CN40*CO40^1.852,-CN40*ABS(CO40)^1.852),
IF(CO40>0, CN40*CJ40^1.852, -CN40*CJ40^1.852)) |
| Ligne 40 | Col 95 | CQ40 | `=1.852*CN40*ABS(CO40)^(1.852-1)` | =1.852*CN40*ABS(CO40)^(1.852-1) |
| Ligne 40 | Col 96 | CR40 | `=CO40+$CJ$71` | =CO40+$CJ$71 |
| Ligne 40 | Col 100 | CV40 | `=IFERROR(MATCH(CY40,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY40,$CI$22:$CI$69,0),0) |
| Ligne 40 | Col 102 | CX40 | `=DIST_PHASE_1_v2!CF29` | =DIST_PHASE_1_v2!CF29 |
| Ligne 40 | Col 103 | CY40 | `=DIST_PHASE_1_v2!CG29` | =DIST_PHASE_1_v2!CG29 |
| Ligne 40 | Col 104 | CZ40 | `=DIST_PHASE_1_v2!CI29` | =DIST_PHASE_1_v2!CI29 |
| Ligne 40 | Col 105 | DA40 | `=DIST_PHASE_1_v2!CN29` | =DIST_PHASE_1_v2!CN29 |
| Ligne 40 | Col 106 | DB40 | `=DIST_PHASE_1_v2!CO29` | =DIST_PHASE_1_v2!CO29 |
| Ligne 40 | Col 107 | DC40 | `=DIST_PHASE_1_v2!CP29` | =DIST_PHASE_1_v2!CP29 |
| Ligne 40 | Col 108 | DD40 | `= (10.679 * DC40) / ((DA40/1000)^4.871 * DB40^1.852)` | = (10.679 * DC40) / ((DA40/1000)^4.871 * DB40^1.852) |
| Ligne 40 | Col 109 | DE40 | `=IF(CX40="positif",CZ40,IF(CX40="negatif",-CZ40,""))` | =IF(CX40="positif",CZ40,IF(CX40="negatif",-CZ40,"")) |
| Ligne 40 | Col 110 | DF40 | `=IF(CV40>0,
IF(DE40>0, DD40*DE40^1.852,-DD40*ABS(DE40)^1.852),
IF(DE40>0, DD40*CZ40^1.852, -DD40*CZ40^1.852))` | =IF(CV40>0,
IF(DE40>0, DD40*DE40^1.852,-DD40*ABS(DE40)^1.852),
IF(DE40>0, DD40*CZ40^1.852, -DD40*CZ40^1.852)) |
| Ligne 40 | Col 111 | DG40 | `=1.852*DD40*ABS(DE40)^(1.852-1)` | =1.852*DD40*ABS(DE40)^(1.852-1) |
| Ligne 40 | Col 112 | DH40 | `=DE40+CZ74` | =DE40+CZ74 |
| Ligne 41 | Col 4 | D41 | `=DIST_PHASE_1_v2!E30` | =DIST_PHASE_1_v2!E30 |
| Ligne 41 | Col 5 | E41 | `=DIST_PHASE_1_v2!G30` | =DIST_PHASE_1_v2!G30 |
| Ligne 41 | Col 6 | F41 | `=DIST_PHASE_1_v2!L30` | =DIST_PHASE_1_v2!L30 |
| Ligne 41 | Col 7 | G41 | `=DIST_PHASE_1_v2!M30` | =DIST_PHASE_1_v2!M30 |
| Ligne 41 | Col 8 | H41 | `=DIST_PHASE_1_v2!N30` | =DIST_PHASE_1_v2!N30 |
| Ligne 41 | Col 9 | I41 | `= (10.679 * H41) / ((F41/1000)^4.871 * G41^1.852)` | = (10.679 * H41) / ((F41/1000)^4.871 * G41^1.852) |
| Ligne 41 | Col 10 | J41 | `=IF(C41="positif",E41,IF(C41="negatif",-E41,""))` | =IF(C41="positif",E41,IF(C41="negatif",-E41,"")) |
| Ligne 41 | Col 11 | K41 | `=IF(J41>0,I41*E41^1.852,-I41*E41^1.852)` | =IF(J41>0,I41*E41^1.852,-I41*E41^1.852) |
| Ligne 41 | Col 12 | L41 | `=1.852*I41*ABS(E41)^(1.852-1)` | =1.852*I41*ABS(E41)^(1.852-1) |
| Ligne 41 | Col 13 | M41 | `=J41+$D$93` | =J41+$D$93 |
| Ligne 41 | Col 16 | P41 | `=IFERROR(MATCH(S41,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S41,$D$22:$D$91,0),0) |
| Ligne 41 | Col 18 | R41 | `=DIST_PHASE_1_v2!Q30` | =DIST_PHASE_1_v2!Q30 |
| Ligne 41 | Col 19 | S41 | `=DIST_PHASE_1_v2!R30` | =DIST_PHASE_1_v2!R30 |
| Ligne 41 | Col 20 | T41 | `=DIST_PHASE_1_v2!T30` | =DIST_PHASE_1_v2!T30 |
| Ligne 41 | Col 21 | U41 | `=DIST_PHASE_1_v2!Y30` | =DIST_PHASE_1_v2!Y30 |
| Ligne 41 | Col 23 | W41 | `=DIST_PHASE_1_v2!AA30` | =DIST_PHASE_1_v2!AA30 |
| Ligne 41 | Col 24 | X41 | `= (10.679 * W41) / ((U41/1000)^4.871 * V41^1.852)` | = (10.679 * W41) / ((U41/1000)^4.871 * V41^1.852) |
| Ligne 41 | Col 25 | Y41 | `=IF(R41="positif",T41,IF(R41="negatif",-T41,""))` | =IF(R41="positif",T41,IF(R41="negatif",-T41,"")) |
| Ligne 41 | Col 26 | Z41 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E7DD0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD8E7DD0> |
| Ligne 41 | Col 27 | AA41 | `=IF(P41>0,
IF(R41="positif",1,-1),
0)` | =IF(P41>0,
IF(R41="positif",1,-1),
0) |
| Ligne 41 | Col 28 | AB41 | `=X41*SIGN(Y41)*ABS(Y41)^1.852` | =X41*SIGN(Y41)*ABS(Y41)^1.852 |
| Ligne 41 | Col 29 | AC41 | `=1.852*X41*ABS(Y41)^(1.852-1)` | =1.852*X41*ABS(Y41)^(1.852-1) |
| Ligne 41 | Col 30 | AD41 | `=IF(P41>0,
Y41+($D$93*Z41)+(AA41*$S$93),
Y41+$S$93)` | =IF(P41>0,
Y41+($D$93*Z41)+(AA41*$S$93),
Y41+$S$93) |
| Ligne 41 | Col 32 | AF41 | `=ABS(AD41)-ABS(Y41)` | =ABS(AD41)-ABS(Y41) |
| Ligne 41 | Col 36 | AJ41 | `=IFERROR(MATCH(AM41,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM41,$S$22:$S$91,0),0) |
| Ligne 41 | Col 38 | AL41 | `=TRONCONS_V2!AI28` | =TRONCONS_V2!AI28 |
| Ligne 41 | Col 39 | AM41 | `=TRONCONS_V2!AE28` | =TRONCONS_V2!AE28 |
| Ligne 41 | Col 40 | AN41 | `=DIST_PHASE_1_v2!AG30` | =DIST_PHASE_1_v2!AG30 |
| Ligne 41 | Col 41 | AO41 | `=DIST_PHASE_1_v2!AL30` | =DIST_PHASE_1_v2!AL30 |
| Ligne 41 | Col 43 | AQ41 | `=TRONCONS_V2!AG28` | =TRONCONS_V2!AG28 |
| Ligne 41 | Col 44 | AR41 | `= (10.679 * AQ41) / ((AO41/1000)^4.871 * AP41^1.852)` | = (10.679 * AQ41) / ((AO41/1000)^4.871 * AP41^1.852) |
| Ligne 41 | Col 45 | AS41 | `=IF(AL41="positif",AN41,IF(AL41="negatif",-AN41,""))` | =IF(AL41="positif",AN41,IF(AL41="negatif",-AN41,"")) |
| Ligne 41 | Col 46 | AT41 | `=IF(AJ41>0,
IF(AS41>0, AR41*AS41^1.852,-AR41*ABS(AS41)^1.852),
IF(AS41>0, AR41*AN41^1.852, -AR41*AN41^1.852))` | =IF(AJ41>0,
IF(AS41>0, AR41*AS41^1.852,-AR41*ABS(AS41)^1.852),
IF(AS41>0, AR41*AN41^1.852, -AR41*AN41^1.852)) |
| Ligne 41 | Col 47 | AU41 | `=1.852*AR41*ABS(AS41)^(1.852-1)` | =1.852*AR41*ABS(AS41)^(1.852-1) |
| Ligne 41 | Col 48 | AV41 | `=AS41+$AN$60` | =AS41+$AN$60 |
| Ligne 41 | Col 52 | AZ41 | `=IFERROR(MATCH(BC41,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC41,$AM$22:$AM$57,0),0) |
| Ligne 41 | Col 54 | BB41 | `=DIST_PHASE_1_v2!AQ30` | =DIST_PHASE_1_v2!AQ30 |
| Ligne 41 | Col 55 | BC41 | `=DIST_PHASE_1_v2!AR30` | =DIST_PHASE_1_v2!AR30 |
| Ligne 41 | Col 56 | BD41 | `=DIST_PHASE_1_v2!AT30` | =DIST_PHASE_1_v2!AT30 |
| Ligne 41 | Col 57 | BE41 | `=DIST_PHASE_1_v2!AY30` | =DIST_PHASE_1_v2!AY30 |
| Ligne 41 | Col 58 | BF41 | `=DIST_PHASE_1_v2!AZ30` | =DIST_PHASE_1_v2!AZ30 |
| Ligne 41 | Col 59 | BG41 | `=DIST_PHASE_1_v2!BA30` | =DIST_PHASE_1_v2!BA30 |
| Ligne 41 | Col 60 | BH41 | `= (10.679 * BG41) / ((BE41/1000)^4.871 * BF41^1.852)` | = (10.679 * BG41) / ((BE41/1000)^4.871 * BF41^1.852) |
| Ligne 41 | Col 61 | BI41 | `=IF(BB41="positif",BD41,IF(BB41="negatif",-BD41,""))` | =IF(BB41="positif",BD41,IF(BB41="negatif",-BD41,"")) |
| Ligne 41 | Col 62 | BJ41 | `=IF(AZ41>0,
IF(BI41>0, BH41*BI41^1.852,-BH41*ABS(BI41)^1.852),
IF(BI41>0, BH41*BD41^1.852, -BH41*BD41^1.852))` | =IF(AZ41>0,
IF(BI41>0, BH41*BI41^1.852,-BH41*ABS(BI41)^1.852),
IF(BI41>0, BH41*BD41^1.852, -BH41*BD41^1.852)) |
| Ligne 41 | Col 63 | BK41 | `=1.852*BH41*ABS(BI41)^(1.852-1)` | =1.852*BH41*ABS(BI41)^(1.852-1) |
| Ligne 41 | Col 64 | BL41 | `=BI41+$BD$75` | =BI41+$BD$75 |
| Ligne 41 | Col 68 | BP41 | `=IFERROR(MATCH(BS41,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS41,$BC$22:$BC$73,0),0) |
| Ligne 41 | Col 70 | BR41 | `=DIST_PHASE_1_v2!BF30` | =DIST_PHASE_1_v2!BF30 |
| Ligne 41 | Col 71 | BS41 | `=DIST_PHASE_1_v2!BG30` | =DIST_PHASE_1_v2!BG30 |
| Ligne 41 | Col 72 | BT41 | `=DIST_PHASE_1_v2!BI30` | =DIST_PHASE_1_v2!BI30 |
| Ligne 41 | Col 73 | BU41 | `=DIST_PHASE_1_v2!BN30` | =DIST_PHASE_1_v2!BN30 |
| Ligne 41 | Col 74 | BV41 | `=DIST_PHASE_1_v2!BO30` | =DIST_PHASE_1_v2!BO30 |
| Ligne 41 | Col 75 | BW41 | `=DIST_PHASE_1_v2!BP30` | =DIST_PHASE_1_v2!BP30 |
| Ligne 41 | Col 76 | BX41 | `= (10.679 * BW41) / ((BU41/1000)^4.871 * BV41^1.852)` | = (10.679 * BW41) / ((BU41/1000)^4.871 * BV41^1.852) |
| Ligne 41 | Col 77 | BY41 | `=IF(BR41="positif",BT41,IF(BR41="negatif",-BT41,""))` | =IF(BR41="positif",BT41,IF(BR41="negatif",-BT41,"")) |
| Ligne 41 | Col 78 | BZ41 | `=IF(BP41>0,
IF(BY41>0, BX41*BY41^1.852,-BX41*ABS(BY41)^1.852),
IF(BY41>0, BX41*BT41^1.852, -BX41*BT41^1.852))` | =IF(BP41>0,
IF(BY41>0, BX41*BY41^1.852,-BX41*ABS(BY41)^1.852),
IF(BY41>0, BX41*BT41^1.852, -BX41*BT41^1.852)) |
| Ligne 41 | Col 79 | CA41 | `=1.852*BX41*ABS(BY41)^(1.852-1)` | =1.852*BX41*ABS(BY41)^(1.852-1) |
| Ligne 41 | Col 80 | CB41 | `=BY41+$BT$64` | =BY41+$BT$64 |
| Ligne 41 | Col 84 | CF41 | `=IFERROR(MATCH(CI41,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI41,$BS$22:$BS$62,0),0) |
| Ligne 41 | Col 86 | CH41 | `=DIST_PHASE_1_v2!BS30` | =DIST_PHASE_1_v2!BS30 |
| Ligne 41 | Col 87 | CI41 | `=DIST_PHASE_1_v2!BT30` | =DIST_PHASE_1_v2!BT30 |
| Ligne 41 | Col 88 | CJ41 | `=DIST_PHASE_1_v2!BV30` | =DIST_PHASE_1_v2!BV30 |
| Ligne 41 | Col 89 | CK41 | `=DIST_PHASE_1_v2!CA30` | =DIST_PHASE_1_v2!CA30 |
| Ligne 41 | Col 91 | CM41 | `=DIST_PHASE_1_v2!CC30` | =DIST_PHASE_1_v2!CC30 |
| Ligne 41 | Col 92 | CN41 | `= (10.679 * CM41) / ((CK41/1000)^4.871 * CL41^1.852)` | = (10.679 * CM41) / ((CK41/1000)^4.871 * CL41^1.852) |
| Ligne 41 | Col 93 | CO41 | `=IF(CH41="positif",CJ41,IF(CH41="negatif",-CJ41,""))` | =IF(CH41="positif",CJ41,IF(CH41="negatif",-CJ41,"")) |
| Ligne 41 | Col 94 | CP41 | `=IF(CF41>0,
IF(CO41>0, CN41*CO41^1.852,-CN41*ABS(CO41)^1.852),
IF(CO41>0, CN41*CJ41^1.852, -CN41*CJ41^1.852))` | =IF(CF41>0,
IF(CO41>0, CN41*CO41^1.852,-CN41*ABS(CO41)^1.852),
IF(CO41>0, CN41*CJ41^1.852, -CN41*CJ41^1.852)) |
| Ligne 41 | Col 95 | CQ41 | `=1.852*CN41*ABS(CO41)^(1.852-1)` | =1.852*CN41*ABS(CO41)^(1.852-1) |
| Ligne 41 | Col 96 | CR41 | `=CO41+$CJ$71` | =CO41+$CJ$71 |
| Ligne 41 | Col 100 | CV41 | `=IFERROR(MATCH(CY41,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY41,$CI$22:$CI$69,0),0) |
| Ligne 41 | Col 102 | CX41 | `=DIST_PHASE_1_v2!CF30` | =DIST_PHASE_1_v2!CF30 |
| Ligne 41 | Col 103 | CY41 | `=DIST_PHASE_1_v2!CG30` | =DIST_PHASE_1_v2!CG30 |
| Ligne 41 | Col 104 | CZ41 | `=DIST_PHASE_1_v2!CI30` | =DIST_PHASE_1_v2!CI30 |
| Ligne 41 | Col 105 | DA41 | `=DIST_PHASE_1_v2!CN30` | =DIST_PHASE_1_v2!CN30 |
| Ligne 41 | Col 106 | DB41 | `=DIST_PHASE_1_v2!CO30` | =DIST_PHASE_1_v2!CO30 |
| Ligne 41 | Col 107 | DC41 | `=DIST_PHASE_1_v2!CP30` | =DIST_PHASE_1_v2!CP30 |
| Ligne 41 | Col 108 | DD41 | `= (10.679 * DC41) / ((DA41/1000)^4.871 * DB41^1.852)` | = (10.679 * DC41) / ((DA41/1000)^4.871 * DB41^1.852) |
| Ligne 41 | Col 109 | DE41 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94D610>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94D610> |
| Ligne 41 | Col 110 | DF41 | `=IF(CV41>0,
IF(DE41>0, DD41*DE41^1.852,-DD41*ABS(DE41)^1.852),
IF(DE41>0, DD41*CZ41^1.852, -DD41*CZ41^1.852))` | =IF(CV41>0,
IF(DE41>0, DD41*DE41^1.852,-DD41*ABS(DE41)^1.852),
IF(DE41>0, DD41*CZ41^1.852, -DD41*CZ41^1.852)) |
| Ligne 41 | Col 111 | DG41 | `=1.852*DD41*ABS(DE41)^(1.852-1)` | =1.852*DD41*ABS(DE41)^(1.852-1) |
| Ligne 41 | Col 112 | DH41 | `=DE41+CZ75` | =DE41+CZ75 |
| Ligne 42 | Col 4 | D42 | `=DIST_PHASE_1_v2!E31` | =DIST_PHASE_1_v2!E31 |
| Ligne 42 | Col 5 | E42 | `=DIST_PHASE_1_v2!G31` | =DIST_PHASE_1_v2!G31 |
| Ligne 42 | Col 6 | F42 | `=DIST_PHASE_1_v2!L31` | =DIST_PHASE_1_v2!L31 |
| Ligne 42 | Col 7 | G42 | `=DIST_PHASE_1_v2!M31` | =DIST_PHASE_1_v2!M31 |
| Ligne 42 | Col 8 | H42 | `=DIST_PHASE_1_v2!N31` | =DIST_PHASE_1_v2!N31 |
| Ligne 42 | Col 9 | I42 | `= (10.679 * H42) / ((F42/1000)^4.871 * G42^1.852)` | = (10.679 * H42) / ((F42/1000)^4.871 * G42^1.852) |
| Ligne 42 | Col 10 | J42 | `=IF(C42="positif",E42,IF(C42="negatif",-E42,""))` | =IF(C42="positif",E42,IF(C42="negatif",-E42,"")) |
| Ligne 42 | Col 11 | K42 | `=IF(J42>0,I42*E42^1.852,-I42*E42^1.852)` | =IF(J42>0,I42*E42^1.852,-I42*E42^1.852) |
| Ligne 42 | Col 12 | L42 | `=1.852*I42*ABS(E42)^(1.852-1)` | =1.852*I42*ABS(E42)^(1.852-1) |
| Ligne 42 | Col 13 | M42 | `=J42+$D$93` | =J42+$D$93 |
| Ligne 42 | Col 16 | P42 | `=IFERROR(MATCH(S42,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S42,$D$22:$D$91,0),0) |
| Ligne 42 | Col 18 | R42 | `=DIST_PHASE_1_v2!Q31` | =DIST_PHASE_1_v2!Q31 |
| Ligne 42 | Col 19 | S42 | `=DIST_PHASE_1_v2!R31` | =DIST_PHASE_1_v2!R31 |
| Ligne 42 | Col 20 | T42 | `=DIST_PHASE_1_v2!T31` | =DIST_PHASE_1_v2!T31 |
| Ligne 42 | Col 21 | U42 | `=DIST_PHASE_1_v2!Y31` | =DIST_PHASE_1_v2!Y31 |
| Ligne 42 | Col 23 | W42 | `=DIST_PHASE_1_v2!AA31` | =DIST_PHASE_1_v2!AA31 |
| Ligne 42 | Col 24 | X42 | `= (10.679 * W42) / ((U42/1000)^4.871 * V42^1.852)` | = (10.679 * W42) / ((U42/1000)^4.871 * V42^1.852) |
| Ligne 42 | Col 25 | Y42 | `=IF(R42="positif",T42,IF(R42="negatif",-T42,""))` | =IF(R42="positif",T42,IF(R42="negatif",-T42,"")) |
| Ligne 42 | Col 26 | Z42 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94CFB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94CFB0> |
| Ligne 42 | Col 27 | AA42 | `=IF(P42>0,
IF(R42="positif",1,-1),
0)` | =IF(P42>0,
IF(R42="positif",1,-1),
0) |
| Ligne 42 | Col 28 | AB42 | `=X42*SIGN(Y42)*ABS(Y42)^1.852` | =X42*SIGN(Y42)*ABS(Y42)^1.852 |
| Ligne 42 | Col 29 | AC42 | `=1.852*X42*ABS(Y42)^(1.852-1)` | =1.852*X42*ABS(Y42)^(1.852-1) |
| Ligne 42 | Col 30 | AD42 | `=IF(P42>0,
Y42+($D$93*Z42)+(AA42*$S$93),
Y42+$S$93)` | =IF(P42>0,
Y42+($D$93*Z42)+(AA42*$S$93),
Y42+$S$93) |
| Ligne 42 | Col 32 | AF42 | `=ABS(AD42)-ABS(Y42)` | =ABS(AD42)-ABS(Y42) |
| Ligne 42 | Col 36 | AJ42 | `=IFERROR(MATCH(AM42,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM42,$S$22:$S$91,0),0) |
| Ligne 42 | Col 38 | AL42 | `=TRONCONS_V2!AI29` | =TRONCONS_V2!AI29 |
| Ligne 42 | Col 39 | AM42 | `=TRONCONS_V2!AE29` | =TRONCONS_V2!AE29 |
| Ligne 42 | Col 40 | AN42 | `=DIST_PHASE_1_v2!AG31` | =DIST_PHASE_1_v2!AG31 |
| Ligne 42 | Col 41 | AO42 | `=DIST_PHASE_1_v2!AL31` | =DIST_PHASE_1_v2!AL31 |
| Ligne 42 | Col 43 | AQ42 | `=TRONCONS_V2!AG29` | =TRONCONS_V2!AG29 |
| Ligne 42 | Col 44 | AR42 | `= (10.679 * AQ42) / ((AO42/1000)^4.871 * AP42^1.852)` | = (10.679 * AQ42) / ((AO42/1000)^4.871 * AP42^1.852) |
| Ligne 42 | Col 45 | AS42 | `=IF(AL42="positif",AN42,IF(AL42="negatif",-AN42,""))` | =IF(AL42="positif",AN42,IF(AL42="negatif",-AN42,"")) |
| Ligne 42 | Col 46 | AT42 | `=IF(AJ42>0,
IF(AS42>0, AR42*AS42^1.852,-AR42*ABS(AS42)^1.852),
IF(AS42>0, AR42*AN42^1.852, -AR42*AN42^1.852))` | =IF(AJ42>0,
IF(AS42>0, AR42*AS42^1.852,-AR42*ABS(AS42)^1.852),
IF(AS42>0, AR42*AN42^1.852, -AR42*AN42^1.852)) |
| Ligne 42 | Col 47 | AU42 | `=1.852*AR42*ABS(AS42)^(1.852-1)` | =1.852*AR42*ABS(AS42)^(1.852-1) |
| Ligne 42 | Col 48 | AV42 | `=AS42+$AN$60` | =AS42+$AN$60 |
| Ligne 42 | Col 52 | AZ42 | `=IFERROR(MATCH(BC42,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC42,$AM$22:$AM$57,0),0) |
| Ligne 42 | Col 54 | BB42 | `=DIST_PHASE_1_v2!AQ31` | =DIST_PHASE_1_v2!AQ31 |
| Ligne 42 | Col 55 | BC42 | `=DIST_PHASE_1_v2!AR31` | =DIST_PHASE_1_v2!AR31 |
| Ligne 42 | Col 56 | BD42 | `=DIST_PHASE_1_v2!AT31` | =DIST_PHASE_1_v2!AT31 |
| Ligne 42 | Col 57 | BE42 | `=DIST_PHASE_1_v2!AY31` | =DIST_PHASE_1_v2!AY31 |
| Ligne 42 | Col 58 | BF42 | `=DIST_PHASE_1_v2!AZ31` | =DIST_PHASE_1_v2!AZ31 |
| Ligne 42 | Col 59 | BG42 | `=DIST_PHASE_1_v2!BA31` | =DIST_PHASE_1_v2!BA31 |
| Ligne 42 | Col 60 | BH42 | `= (10.679 * BG42) / ((BE42/1000)^4.871 * BF42^1.852)` | = (10.679 * BG42) / ((BE42/1000)^4.871 * BF42^1.852) |
| Ligne 42 | Col 61 | BI42 | `=IF(BB42="positif",BD42,IF(BB42="negatif",-BD42,""))` | =IF(BB42="positif",BD42,IF(BB42="negatif",-BD42,"")) |
| Ligne 42 | Col 62 | BJ42 | `=IF(AZ42>0,
IF(BI42>0, BH42*BI42^1.852,-BH42*ABS(BI42)^1.852),
IF(BI42>0, BH42*BD42^1.852, -BH42*BD42^1.852))` | =IF(AZ42>0,
IF(BI42>0, BH42*BI42^1.852,-BH42*ABS(BI42)^1.852),
IF(BI42>0, BH42*BD42^1.852, -BH42*BD42^1.852)) |
| Ligne 42 | Col 63 | BK42 | `=1.852*BH42*ABS(BI42)^(1.852-1)` | =1.852*BH42*ABS(BI42)^(1.852-1) |
| Ligne 42 | Col 64 | BL42 | `=BI42+$BD$75` | =BI42+$BD$75 |
| Ligne 42 | Col 68 | BP42 | `=IFERROR(MATCH(BS42,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS42,$BC$22:$BC$73,0),0) |
| Ligne 42 | Col 70 | BR42 | `=DIST_PHASE_1_v2!BF31` | =DIST_PHASE_1_v2!BF31 |
| Ligne 42 | Col 71 | BS42 | `=DIST_PHASE_1_v2!BG31` | =DIST_PHASE_1_v2!BG31 |
| Ligne 42 | Col 72 | BT42 | `=DIST_PHASE_1_v2!BI31` | =DIST_PHASE_1_v2!BI31 |
| Ligne 42 | Col 73 | BU42 | `=DIST_PHASE_1_v2!BN31` | =DIST_PHASE_1_v2!BN31 |
| Ligne 42 | Col 74 | BV42 | `=DIST_PHASE_1_v2!BO31` | =DIST_PHASE_1_v2!BO31 |
| Ligne 42 | Col 75 | BW42 | `=DIST_PHASE_1_v2!BP31` | =DIST_PHASE_1_v2!BP31 |
| Ligne 42 | Col 76 | BX42 | `= (10.679 * BW42) / ((BU42/1000)^4.871 * BV42^1.852)` | = (10.679 * BW42) / ((BU42/1000)^4.871 * BV42^1.852) |
| Ligne 42 | Col 77 | BY42 | `=IF(BR42="positif",BT42,IF(BR42="negatif",-BT42,""))` | =IF(BR42="positif",BT42,IF(BR42="negatif",-BT42,"")) |
| Ligne 42 | Col 78 | BZ42 | `=IF(BP42>0,
IF(BY42>0, BX42*BY42^1.852,-BX42*ABS(BY42)^1.852),
IF(BY42>0, BX42*BT42^1.852, -BX42*BT42^1.852))` | =IF(BP42>0,
IF(BY42>0, BX42*BY42^1.852,-BX42*ABS(BY42)^1.852),
IF(BY42>0, BX42*BT42^1.852, -BX42*BT42^1.852)) |
| Ligne 42 | Col 79 | CA42 | `=1.852*BX42*ABS(BY42)^(1.852-1)` | =1.852*BX42*ABS(BY42)^(1.852-1) |
| Ligne 42 | Col 80 | CB42 | `=BY42+$BT$64` | =BY42+$BT$64 |
| Ligne 42 | Col 84 | CF42 | `=IFERROR(MATCH(CI42,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI42,$BS$22:$BS$62,0),0) |
| Ligne 42 | Col 86 | CH42 | `=DIST_PHASE_1_v2!BS31` | =DIST_PHASE_1_v2!BS31 |
| Ligne 42 | Col 87 | CI42 | `=DIST_PHASE_1_v2!BT31` | =DIST_PHASE_1_v2!BT31 |
| Ligne 42 | Col 88 | CJ42 | `=DIST_PHASE_1_v2!BV31` | =DIST_PHASE_1_v2!BV31 |
| Ligne 42 | Col 89 | CK42 | `=DIST_PHASE_1_v2!CA31` | =DIST_PHASE_1_v2!CA31 |
| Ligne 42 | Col 91 | CM42 | `=DIST_PHASE_1_v2!CC31` | =DIST_PHASE_1_v2!CC31 |
| Ligne 42 | Col 92 | CN42 | `= (10.679 * CM42) / ((CK42/1000)^4.871 * CL42^1.852)` | = (10.679 * CM42) / ((CK42/1000)^4.871 * CL42^1.852) |
| Ligne 42 | Col 93 | CO42 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94DAF0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94DAF0> |
| Ligne 42 | Col 94 | CP42 | `=IF(CF42>0,
IF(CO42>0, CN42*CO42^1.852,-CN42*ABS(CO42)^1.852),
IF(CO42>0, CN42*CJ42^1.852, -CN42*CJ42^1.852))` | =IF(CF42>0,
IF(CO42>0, CN42*CO42^1.852,-CN42*ABS(CO42)^1.852),
IF(CO42>0, CN42*CJ42^1.852, -CN42*CJ42^1.852)) |
| Ligne 42 | Col 95 | CQ42 | `=1.852*CN42*ABS(CO42)^(1.852-1)` | =1.852*CN42*ABS(CO42)^(1.852-1) |
| Ligne 42 | Col 96 | CR42 | `=CO42+$CJ$71` | =CO42+$CJ$71 |
| Ligne 42 | Col 100 | CV42 | `=IFERROR(MATCH(CY42,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY42,$CI$22:$CI$69,0),0) |
| Ligne 42 | Col 102 | CX42 | `=DIST_PHASE_1_v2!CF31` | =DIST_PHASE_1_v2!CF31 |
| Ligne 42 | Col 103 | CY42 | `=DIST_PHASE_1_v2!CG31` | =DIST_PHASE_1_v2!CG31 |
| Ligne 42 | Col 104 | CZ42 | `=DIST_PHASE_1_v2!CI31` | =DIST_PHASE_1_v2!CI31 |
| Ligne 42 | Col 105 | DA42 | `=DIST_PHASE_1_v2!CN31` | =DIST_PHASE_1_v2!CN31 |
| Ligne 42 | Col 106 | DB42 | `=DIST_PHASE_1_v2!CO31` | =DIST_PHASE_1_v2!CO31 |
| Ligne 42 | Col 107 | DC42 | `=DIST_PHASE_1_v2!CP31` | =DIST_PHASE_1_v2!CP31 |
| Ligne 42 | Col 108 | DD42 | `= (10.679 * DC42) / ((DA42/1000)^4.871 * DB42^1.852)` | = (10.679 * DC42) / ((DA42/1000)^4.871 * DB42^1.852) |
| Ligne 42 | Col 109 | DE42 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94DBB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94DBB0> |
| Ligne 42 | Col 110 | DF42 | `=IF(CV42>0,
IF(DE42>0, DD42*DE42^1.852,-DD42*ABS(DE42)^1.852),
IF(DE42>0, DD42*CZ42^1.852, -DD42*CZ42^1.852))` | =IF(CV42>0,
IF(DE42>0, DD42*DE42^1.852,-DD42*ABS(DE42)^1.852),
IF(DE42>0, DD42*CZ42^1.852, -DD42*CZ42^1.852)) |
| Ligne 42 | Col 111 | DG42 | `=1.852*DD42*ABS(DE42)^(1.852-1)` | =1.852*DD42*ABS(DE42)^(1.852-1) |
| Ligne 42 | Col 112 | DH42 | `=DE42+CZ76` | =DE42+CZ76 |
| Ligne 43 | Col 4 | D43 | `=DIST_PHASE_1_v2!E32` | =DIST_PHASE_1_v2!E32 |
| Ligne 43 | Col 5 | E43 | `=DIST_PHASE_1_v2!G32` | =DIST_PHASE_1_v2!G32 |
| Ligne 43 | Col 6 | F43 | `=DIST_PHASE_1_v2!L32` | =DIST_PHASE_1_v2!L32 |
| Ligne 43 | Col 7 | G43 | `=DIST_PHASE_1_v2!M32` | =DIST_PHASE_1_v2!M32 |
| Ligne 43 | Col 8 | H43 | `=DIST_PHASE_1_v2!N32` | =DIST_PHASE_1_v2!N32 |
| Ligne 43 | Col 9 | I43 | `= (10.679 * H43) / ((F43/1000)^4.871 * G43^1.852)` | = (10.679 * H43) / ((F43/1000)^4.871 * G43^1.852) |
| Ligne 43 | Col 10 | J43 | `=IF(C43="positif",E43,IF(C43="negatif",-E43,""))` | =IF(C43="positif",E43,IF(C43="negatif",-E43,"")) |
| Ligne 43 | Col 11 | K43 | `=IF(J43>0,I43*E43^1.852,-I43*E43^1.852)` | =IF(J43>0,I43*E43^1.852,-I43*E43^1.852) |
| Ligne 43 | Col 12 | L43 | `=1.852*I43*ABS(E43)^(1.852-1)` | =1.852*I43*ABS(E43)^(1.852-1) |
| Ligne 43 | Col 13 | M43 | `=J43+$D$93` | =J43+$D$93 |
| Ligne 43 | Col 16 | P43 | `=IFERROR(MATCH(S43,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S43,$D$22:$D$91,0),0) |
| Ligne 43 | Col 18 | R43 | `=DIST_PHASE_1_v2!Q32` | =DIST_PHASE_1_v2!Q32 |
| Ligne 43 | Col 19 | S43 | `=DIST_PHASE_1_v2!R32` | =DIST_PHASE_1_v2!R32 |
| Ligne 43 | Col 20 | T43 | `=DIST_PHASE_1_v2!T32` | =DIST_PHASE_1_v2!T32 |
| Ligne 43 | Col 21 | U43 | `=DIST_PHASE_1_v2!Y32` | =DIST_PHASE_1_v2!Y32 |
| Ligne 43 | Col 23 | W43 | `=DIST_PHASE_1_v2!AA32` | =DIST_PHASE_1_v2!AA32 |
| Ligne 43 | Col 24 | X43 | `= (10.679 * W43) / ((U43/1000)^4.871 * V43^1.852)` | = (10.679 * W43) / ((U43/1000)^4.871 * V43^1.852) |
| Ligne 43 | Col 25 | Y43 | `=IF(R43="positif",T43,IF(R43="negatif",-T43,""))` | =IF(R43="positif",T43,IF(R43="negatif",-T43,"")) |
| Ligne 43 | Col 26 | Z43 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94D010>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94D010> |
| Ligne 43 | Col 27 | AA43 | `=IF(P43>0,
IF(R43="positif",1,-1),
0)` | =IF(P43>0,
IF(R43="positif",1,-1),
0) |
| Ligne 43 | Col 28 | AB43 | `=X43*SIGN(Y43)*ABS(Y43)^1.852` | =X43*SIGN(Y43)*ABS(Y43)^1.852 |
| Ligne 43 | Col 29 | AC43 | `=1.852*X43*ABS(Y43)^(1.852-1)` | =1.852*X43*ABS(Y43)^(1.852-1) |
| Ligne 43 | Col 30 | AD43 | `=IF(P43>0,
Y43+($D$93*Z43)+(AA43*$S$93),
Y43+$S$93)` | =IF(P43>0,
Y43+($D$93*Z43)+(AA43*$S$93),
Y43+$S$93) |
| Ligne 43 | Col 32 | AF43 | `=ABS(AD43)-ABS(Y43)` | =ABS(AD43)-ABS(Y43) |
| Ligne 43 | Col 36 | AJ43 | `=IFERROR(MATCH(AM43,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM43,$S$22:$S$91,0),0) |
| Ligne 43 | Col 38 | AL43 | `=TRONCONS_V2!AI30` | =TRONCONS_V2!AI30 |
| Ligne 43 | Col 39 | AM43 | `=TRONCONS_V2!AE30` | =TRONCONS_V2!AE30 |
| Ligne 43 | Col 40 | AN43 | `=DIST_PHASE_1_v2!AG32` | =DIST_PHASE_1_v2!AG32 |
| Ligne 43 | Col 41 | AO43 | `=DIST_PHASE_1_v2!AL32` | =DIST_PHASE_1_v2!AL32 |
| Ligne 43 | Col 43 | AQ43 | `=TRONCONS_V2!AG30` | =TRONCONS_V2!AG30 |
| Ligne 43 | Col 44 | AR43 | `= (10.679 * AQ43) / ((AO43/1000)^4.871 * AP43^1.852)` | = (10.679 * AQ43) / ((AO43/1000)^4.871 * AP43^1.852) |
| Ligne 43 | Col 45 | AS43 | `=IF(AL43="positif",AN43,IF(AL43="negatif",-AN43,""))` | =IF(AL43="positif",AN43,IF(AL43="negatif",-AN43,"")) |
| Ligne 43 | Col 46 | AT43 | `=IF(AJ43>0,
IF(AS43>0, AR43*AS43^1.852,-AR43*ABS(AS43)^1.852),
IF(AS43>0, AR43*AN43^1.852, -AR43*AN43^1.852))` | =IF(AJ43>0,
IF(AS43>0, AR43*AS43^1.852,-AR43*ABS(AS43)^1.852),
IF(AS43>0, AR43*AN43^1.852, -AR43*AN43^1.852)) |
| Ligne 43 | Col 47 | AU43 | `=1.852*AR43*ABS(AS43)^(1.852-1)` | =1.852*AR43*ABS(AS43)^(1.852-1) |
| Ligne 43 | Col 48 | AV43 | `=AS43+$AN$60` | =AS43+$AN$60 |
| Ligne 43 | Col 52 | AZ43 | `=IFERROR(MATCH(BC43,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC43,$AM$22:$AM$57,0),0) |
| Ligne 43 | Col 54 | BB43 | `=DIST_PHASE_1_v2!AQ32` | =DIST_PHASE_1_v2!AQ32 |
| Ligne 43 | Col 55 | BC43 | `=DIST_PHASE_1_v2!AR32` | =DIST_PHASE_1_v2!AR32 |
| Ligne 43 | Col 56 | BD43 | `=DIST_PHASE_1_v2!AT32` | =DIST_PHASE_1_v2!AT32 |
| Ligne 43 | Col 57 | BE43 | `=DIST_PHASE_1_v2!AY32` | =DIST_PHASE_1_v2!AY32 |
| Ligne 43 | Col 58 | BF43 | `=DIST_PHASE_1_v2!AZ32` | =DIST_PHASE_1_v2!AZ32 |
| Ligne 43 | Col 59 | BG43 | `=DIST_PHASE_1_v2!BA32` | =DIST_PHASE_1_v2!BA32 |
| Ligne 43 | Col 60 | BH43 | `= (10.679 * BG43) / ((BE43/1000)^4.871 * BF43^1.852)` | = (10.679 * BG43) / ((BE43/1000)^4.871 * BF43^1.852) |
| Ligne 43 | Col 61 | BI43 | `=IF(BB43="positif",BD43,IF(BB43="negatif",-BD43,""))` | =IF(BB43="positif",BD43,IF(BB43="negatif",-BD43,"")) |
| Ligne 43 | Col 62 | BJ43 | `=IF(AZ43>0,
IF(BI43>0, BH43*BI43^1.852,-BH43*ABS(BI43)^1.852),
IF(BI43>0, BH43*BD43^1.852, -BH43*BD43^1.852))` | =IF(AZ43>0,
IF(BI43>0, BH43*BI43^1.852,-BH43*ABS(BI43)^1.852),
IF(BI43>0, BH43*BD43^1.852, -BH43*BD43^1.852)) |
| Ligne 43 | Col 63 | BK43 | `=1.852*BH43*ABS(BI43)^(1.852-1)` | =1.852*BH43*ABS(BI43)^(1.852-1) |
| Ligne 43 | Col 64 | BL43 | `=BI43+$BD$75` | =BI43+$BD$75 |
| Ligne 43 | Col 68 | BP43 | `=IFERROR(MATCH(BS43,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS43,$BC$22:$BC$73,0),0) |
| Ligne 43 | Col 70 | BR43 | `=DIST_PHASE_1_v2!BF32` | =DIST_PHASE_1_v2!BF32 |
| Ligne 43 | Col 71 | BS43 | `=DIST_PHASE_1_v2!BG32` | =DIST_PHASE_1_v2!BG32 |
| Ligne 43 | Col 72 | BT43 | `=DIST_PHASE_1_v2!BI32` | =DIST_PHASE_1_v2!BI32 |
| Ligne 43 | Col 73 | BU43 | `=DIST_PHASE_1_v2!BN32` | =DIST_PHASE_1_v2!BN32 |
| Ligne 43 | Col 74 | BV43 | `=DIST_PHASE_1_v2!BO32` | =DIST_PHASE_1_v2!BO32 |
| Ligne 43 | Col 75 | BW43 | `=DIST_PHASE_1_v2!BP32` | =DIST_PHASE_1_v2!BP32 |
| Ligne 43 | Col 76 | BX43 | `= (10.679 * BW43) / ((BU43/1000)^4.871 * BV43^1.852)` | = (10.679 * BW43) / ((BU43/1000)^4.871 * BV43^1.852) |
| Ligne 43 | Col 77 | BY43 | `=IF(BR43="positif",BT43,IF(BR43="negatif",-BT43,""))` | =IF(BR43="positif",BT43,IF(BR43="negatif",-BT43,"")) |
| Ligne 43 | Col 78 | BZ43 | `=IF(BP43>0,
IF(BY43>0, BX43*BY43^1.852,-BX43*ABS(BY43)^1.852),
IF(BY43>0, BX43*BT43^1.852, -BX43*BT43^1.852))` | =IF(BP43>0,
IF(BY43>0, BX43*BY43^1.852,-BX43*ABS(BY43)^1.852),
IF(BY43>0, BX43*BT43^1.852, -BX43*BT43^1.852)) |
| Ligne 43 | Col 79 | CA43 | `=1.852*BX43*ABS(BY43)^(1.852-1)` | =1.852*BX43*ABS(BY43)^(1.852-1) |
| Ligne 43 | Col 80 | CB43 | `=BY43+$BT$64` | =BY43+$BT$64 |
| Ligne 43 | Col 84 | CF43 | `=IFERROR(MATCH(CI43,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI43,$BS$22:$BS$62,0),0) |
| Ligne 43 | Col 86 | CH43 | `=DIST_PHASE_1_v2!BS32` | =DIST_PHASE_1_v2!BS32 |
| Ligne 43 | Col 87 | CI43 | `=DIST_PHASE_1_v2!BT32` | =DIST_PHASE_1_v2!BT32 |
| Ligne 43 | Col 88 | CJ43 | `=DIST_PHASE_1_v2!BV32` | =DIST_PHASE_1_v2!BV32 |
| Ligne 43 | Col 89 | CK43 | `=DIST_PHASE_1_v2!CA32` | =DIST_PHASE_1_v2!CA32 |
| Ligne 43 | Col 91 | CM43 | `=DIST_PHASE_1_v2!CC32` | =DIST_PHASE_1_v2!CC32 |
| Ligne 43 | Col 92 | CN43 | `= (10.679 * CM43) / ((CK43/1000)^4.871 * CL43^1.852)` | = (10.679 * CM43) / ((CK43/1000)^4.871 * CL43^1.852) |
| Ligne 43 | Col 93 | CO43 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E090>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E090> |
| Ligne 43 | Col 94 | CP43 | `=IF(CF43>0,
IF(CO43>0, CN43*CO43^1.852,-CN43*ABS(CO43)^1.852),
IF(CO43>0, CN43*CJ43^1.852, -CN43*CJ43^1.852))` | =IF(CF43>0,
IF(CO43>0, CN43*CO43^1.852,-CN43*ABS(CO43)^1.852),
IF(CO43>0, CN43*CJ43^1.852, -CN43*CJ43^1.852)) |
| Ligne 43 | Col 95 | CQ43 | `=1.852*CN43*ABS(CO43)^(1.852-1)` | =1.852*CN43*ABS(CO43)^(1.852-1) |
| Ligne 43 | Col 96 | CR43 | `=CO43+$CJ$71` | =CO43+$CJ$71 |
| Ligne 43 | Col 100 | CV43 | `=IFERROR(MATCH(CY43,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY43,$CI$22:$CI$69,0),0) |
| Ligne 43 | Col 102 | CX43 | `=DIST_PHASE_1_v2!CF32` | =DIST_PHASE_1_v2!CF32 |
| Ligne 43 | Col 103 | CY43 | `=DIST_PHASE_1_v2!CG32` | =DIST_PHASE_1_v2!CG32 |
| Ligne 43 | Col 104 | CZ43 | `=DIST_PHASE_1_v2!CI32` | =DIST_PHASE_1_v2!CI32 |
| Ligne 43 | Col 105 | DA43 | `=DIST_PHASE_1_v2!CN32` | =DIST_PHASE_1_v2!CN32 |
| Ligne 43 | Col 106 | DB43 | `=DIST_PHASE_1_v2!CO32` | =DIST_PHASE_1_v2!CO32 |
| Ligne 43 | Col 107 | DC43 | `=DIST_PHASE_1_v2!CP32` | =DIST_PHASE_1_v2!CP32 |
| Ligne 43 | Col 108 | DD43 | `= (10.679 * DC43) / ((DA43/1000)^4.871 * DB43^1.852)` | = (10.679 * DC43) / ((DA43/1000)^4.871 * DB43^1.852) |
| Ligne 43 | Col 109 | DE43 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E150>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E150> |
| Ligne 43 | Col 110 | DF43 | `=IF(CV43>0,
IF(DE43>0, DD43*DE43^1.852,-DD43*ABS(DE43)^1.852),
IF(DE43>0, DD43*CZ43^1.852, -DD43*CZ43^1.852))` | =IF(CV43>0,
IF(DE43>0, DD43*DE43^1.852,-DD43*ABS(DE43)^1.852),
IF(DE43>0, DD43*CZ43^1.852, -DD43*CZ43^1.852)) |
| Ligne 43 | Col 111 | DG43 | `=1.852*DD43*ABS(DE43)^(1.852-1)` | =1.852*DD43*ABS(DE43)^(1.852-1) |
| Ligne 43 | Col 112 | DH43 | `=DE43+CZ77` | =DE43+CZ77 |
| Ligne 44 | Col 4 | D44 | `=DIST_PHASE_1_v2!E33` | =DIST_PHASE_1_v2!E33 |
| Ligne 44 | Col 5 | E44 | `=DIST_PHASE_1_v2!G33` | =DIST_PHASE_1_v2!G33 |
| Ligne 44 | Col 6 | F44 | `=DIST_PHASE_1_v2!L33` | =DIST_PHASE_1_v2!L33 |
| Ligne 44 | Col 7 | G44 | `=DIST_PHASE_1_v2!M33` | =DIST_PHASE_1_v2!M33 |
| Ligne 44 | Col 8 | H44 | `=DIST_PHASE_1_v2!N33` | =DIST_PHASE_1_v2!N33 |
| Ligne 44 | Col 9 | I44 | `= (10.679 * H44) / ((F44/1000)^4.871 * G44^1.852)` | = (10.679 * H44) / ((F44/1000)^4.871 * G44^1.852) |
| Ligne 44 | Col 10 | J44 | `=IF(C44="positif",E44,IF(C44="negatif",-E44,""))` | =IF(C44="positif",E44,IF(C44="negatif",-E44,"")) |
| Ligne 44 | Col 11 | K44 | `=IF(J44>0,I44*E44^1.852,-I44*E44^1.852)` | =IF(J44>0,I44*E44^1.852,-I44*E44^1.852) |
| Ligne 44 | Col 12 | L44 | `=1.852*I44*ABS(E44)^(1.852-1)` | =1.852*I44*ABS(E44)^(1.852-1) |
| Ligne 44 | Col 13 | M44 | `=J44+$D$93` | =J44+$D$93 |
| Ligne 44 | Col 16 | P44 | `=IFERROR(MATCH(S44,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S44,$D$22:$D$91,0),0) |
| Ligne 44 | Col 18 | R44 | `=DIST_PHASE_1_v2!Q33` | =DIST_PHASE_1_v2!Q33 |
| Ligne 44 | Col 19 | S44 | `=DIST_PHASE_1_v2!R33` | =DIST_PHASE_1_v2!R33 |
| Ligne 44 | Col 20 | T44 | `=DIST_PHASE_1_v2!T33` | =DIST_PHASE_1_v2!T33 |
| Ligne 44 | Col 21 | U44 | `=DIST_PHASE_1_v2!Y33` | =DIST_PHASE_1_v2!Y33 |
| Ligne 44 | Col 23 | W44 | `=DIST_PHASE_1_v2!AA33` | =DIST_PHASE_1_v2!AA33 |
| Ligne 44 | Col 24 | X44 | `= (10.679 * W44) / ((U44/1000)^4.871 * V44^1.852)` | = (10.679 * W44) / ((U44/1000)^4.871 * V44^1.852) |
| Ligne 44 | Col 25 | Y44 | `=IF(R44="positif",T44,IF(R44="negatif",-T44,""))` | =IF(R44="positif",T44,IF(R44="negatif",-T44,"")) |
| Ligne 44 | Col 26 | Z44 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94D070>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94D070> |
| Ligne 44 | Col 27 | AA44 | `=IF(P44>0,
IF(R44="positif",1,-1),
0)` | =IF(P44>0,
IF(R44="positif",1,-1),
0) |
| Ligne 44 | Col 28 | AB44 | `=X44*SIGN(Y44)*ABS(Y44)^1.852` | =X44*SIGN(Y44)*ABS(Y44)^1.852 |
| Ligne 44 | Col 29 | AC44 | `=1.852*X44*ABS(Y44)^(1.852-1)` | =1.852*X44*ABS(Y44)^(1.852-1) |
| Ligne 44 | Col 30 | AD44 | `=IF(P44>0,
Y44+($D$93*Z44)+(AA44*$S$93),
Y44+$S$93)` | =IF(P44>0,
Y44+($D$93*Z44)+(AA44*$S$93),
Y44+$S$93) |
| Ligne 44 | Col 32 | AF44 | `=ABS(AD44)-ABS(Y44)` | =ABS(AD44)-ABS(Y44) |
| Ligne 44 | Col 36 | AJ44 | `=IFERROR(MATCH(AM44,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM44,$S$22:$S$91,0),0) |
| Ligne 44 | Col 38 | AL44 | `=TRONCONS_V2!AI31` | =TRONCONS_V2!AI31 |
| Ligne 44 | Col 39 | AM44 | `=TRONCONS_V2!AE31` | =TRONCONS_V2!AE31 |
| Ligne 44 | Col 40 | AN44 | `=DIST_PHASE_1_v2!AG33` | =DIST_PHASE_1_v2!AG33 |
| Ligne 44 | Col 41 | AO44 | `=DIST_PHASE_1_v2!AL33` | =DIST_PHASE_1_v2!AL33 |
| Ligne 44 | Col 43 | AQ44 | `=TRONCONS_V2!AG31` | =TRONCONS_V2!AG31 |
| Ligne 44 | Col 44 | AR44 | `= (10.679 * AQ44) / ((AO44/1000)^4.871 * AP44^1.852)` | = (10.679 * AQ44) / ((AO44/1000)^4.871 * AP44^1.852) |
| Ligne 44 | Col 45 | AS44 | `=IF(AL44="positif",AN44,IF(AL44="negatif",-AN44,""))` | =IF(AL44="positif",AN44,IF(AL44="negatif",-AN44,"")) |
| Ligne 44 | Col 46 | AT44 | `=IF(AJ44>0,
IF(AS44>0, AR44*AS44^1.852,-AR44*ABS(AS44)^1.852),
IF(AS44>0, AR44*AN44^1.852, -AR44*AN44^1.852))` | =IF(AJ44>0,
IF(AS44>0, AR44*AS44^1.852,-AR44*ABS(AS44)^1.852),
IF(AS44>0, AR44*AN44^1.852, -AR44*AN44^1.852)) |
| Ligne 44 | Col 47 | AU44 | `=1.852*AR44*ABS(AS44)^(1.852-1)` | =1.852*AR44*ABS(AS44)^(1.852-1) |
| Ligne 44 | Col 48 | AV44 | `=AS44+$AN$60` | =AS44+$AN$60 |
| Ligne 44 | Col 52 | AZ44 | `=IFERROR(MATCH(BC44,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC44,$AM$22:$AM$57,0),0) |
| Ligne 44 | Col 54 | BB44 | `=DIST_PHASE_1_v2!AQ33` | =DIST_PHASE_1_v2!AQ33 |
| Ligne 44 | Col 55 | BC44 | `=DIST_PHASE_1_v2!AR33` | =DIST_PHASE_1_v2!AR33 |
| Ligne 44 | Col 56 | BD44 | `=DIST_PHASE_1_v2!AT33` | =DIST_PHASE_1_v2!AT33 |
| Ligne 44 | Col 57 | BE44 | `=DIST_PHASE_1_v2!AY33` | =DIST_PHASE_1_v2!AY33 |
| Ligne 44 | Col 58 | BF44 | `=DIST_PHASE_1_v2!AZ33` | =DIST_PHASE_1_v2!AZ33 |
| Ligne 44 | Col 59 | BG44 | `=DIST_PHASE_1_v2!BA33` | =DIST_PHASE_1_v2!BA33 |
| Ligne 44 | Col 60 | BH44 | `= (10.679 * BG44) / ((BE44/1000)^4.871 * BF44^1.852)` | = (10.679 * BG44) / ((BE44/1000)^4.871 * BF44^1.852) |
| Ligne 44 | Col 61 | BI44 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E570>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E570> |
| Ligne 44 | Col 62 | BJ44 | `=IF(AZ44>0,
IF(BI44>0, BH44*BI44^1.852,-BH44*ABS(BI44)^1.852),
IF(BI44>0, BH44*BD44^1.852, -BH44*BD44^1.852))` | =IF(AZ44>0,
IF(BI44>0, BH44*BI44^1.852,-BH44*ABS(BI44)^1.852),
IF(BI44>0, BH44*BD44^1.852, -BH44*BD44^1.852)) |
| Ligne 44 | Col 63 | BK44 | `=1.852*BH44*ABS(BI44)^(1.852-1)` | =1.852*BH44*ABS(BI44)^(1.852-1) |
| Ligne 44 | Col 64 | BL44 | `=BI44+$BD$75` | =BI44+$BD$75 |
| Ligne 44 | Col 68 | BP44 | `=IFERROR(MATCH(BS44,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS44,$BC$22:$BC$73,0),0) |
| Ligne 44 | Col 70 | BR44 | `=DIST_PHASE_1_v2!BF33` | =DIST_PHASE_1_v2!BF33 |
| Ligne 44 | Col 71 | BS44 | `=DIST_PHASE_1_v2!BG33` | =DIST_PHASE_1_v2!BG33 |
| Ligne 44 | Col 72 | BT44 | `=DIST_PHASE_1_v2!BI33` | =DIST_PHASE_1_v2!BI33 |
| Ligne 44 | Col 73 | BU44 | `=DIST_PHASE_1_v2!BN33` | =DIST_PHASE_1_v2!BN33 |
| Ligne 44 | Col 74 | BV44 | `=DIST_PHASE_1_v2!BO33` | =DIST_PHASE_1_v2!BO33 |
| Ligne 44 | Col 75 | BW44 | `=DIST_PHASE_1_v2!BP33` | =DIST_PHASE_1_v2!BP33 |
| Ligne 44 | Col 76 | BX44 | `= (10.679 * BW44) / ((BU44/1000)^4.871 * BV44^1.852)` | = (10.679 * BW44) / ((BU44/1000)^4.871 * BV44^1.852) |
| Ligne 44 | Col 77 | BY44 | `=IF(BR44="positif",BT44,IF(BR44="negatif",-BT44,""))` | =IF(BR44="positif",BT44,IF(BR44="negatif",-BT44,"")) |
| Ligne 44 | Col 78 | BZ44 | `=IF(BP44>0,
IF(BY44>0, BX44*BY44^1.852,-BX44*ABS(BY44)^1.852),
IF(BY44>0, BX44*BT44^1.852, -BX44*BT44^1.852))` | =IF(BP44>0,
IF(BY44>0, BX44*BY44^1.852,-BX44*ABS(BY44)^1.852),
IF(BY44>0, BX44*BT44^1.852, -BX44*BT44^1.852)) |
| Ligne 44 | Col 79 | CA44 | `=1.852*BX44*ABS(BY44)^(1.852-1)` | =1.852*BX44*ABS(BY44)^(1.852-1) |
| Ligne 44 | Col 80 | CB44 | `=BY44+$BT$64` | =BY44+$BT$64 |
| Ligne 44 | Col 84 | CF44 | `=IFERROR(MATCH(CI44,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI44,$BS$22:$BS$62,0),0) |
| Ligne 44 | Col 86 | CH44 | `=DIST_PHASE_1_v2!BS33` | =DIST_PHASE_1_v2!BS33 |
| Ligne 44 | Col 87 | CI44 | `=DIST_PHASE_1_v2!BT33` | =DIST_PHASE_1_v2!BT33 |
| Ligne 44 | Col 88 | CJ44 | `=DIST_PHASE_1_v2!BV33` | =DIST_PHASE_1_v2!BV33 |
| Ligne 44 | Col 89 | CK44 | `=DIST_PHASE_1_v2!CA33` | =DIST_PHASE_1_v2!CA33 |
| Ligne 44 | Col 91 | CM44 | `=DIST_PHASE_1_v2!CC33` | =DIST_PHASE_1_v2!CC33 |
| Ligne 44 | Col 92 | CN44 | `= (10.679 * CM44) / ((CK44/1000)^4.871 * CL44^1.852)` | = (10.679 * CM44) / ((CK44/1000)^4.871 * CL44^1.852) |
| Ligne 44 | Col 93 | CO44 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E6F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E6F0> |
| Ligne 44 | Col 94 | CP44 | `=IF(CF44>0,
IF(CO44>0, CN44*CO44^1.852,-CN44*ABS(CO44)^1.852),
IF(CO44>0, CN44*CJ44^1.852, -CN44*CJ44^1.852))` | =IF(CF44>0,
IF(CO44>0, CN44*CO44^1.852,-CN44*ABS(CO44)^1.852),
IF(CO44>0, CN44*CJ44^1.852, -CN44*CJ44^1.852)) |
| Ligne 44 | Col 95 | CQ44 | `=1.852*CN44*ABS(CO44)^(1.852-1)` | =1.852*CN44*ABS(CO44)^(1.852-1) |
| Ligne 44 | Col 96 | CR44 | `=CO44+$CJ$71` | =CO44+$CJ$71 |
| Ligne 44 | Col 100 | CV44 | `=IFERROR(MATCH(CY44,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY44,$CI$22:$CI$69,0),0) |
| Ligne 44 | Col 102 | CX44 | `=DIST_PHASE_1_v2!CF33` | =DIST_PHASE_1_v2!CF33 |
| Ligne 44 | Col 103 | CY44 | `=DIST_PHASE_1_v2!CG33` | =DIST_PHASE_1_v2!CG33 |
| Ligne 44 | Col 104 | CZ44 | `=DIST_PHASE_1_v2!CI33` | =DIST_PHASE_1_v2!CI33 |
| Ligne 44 | Col 105 | DA44 | `=DIST_PHASE_1_v2!CN33` | =DIST_PHASE_1_v2!CN33 |
| Ligne 44 | Col 106 | DB44 | `=DIST_PHASE_1_v2!CO33` | =DIST_PHASE_1_v2!CO33 |
| Ligne 44 | Col 107 | DC44 | `=DIST_PHASE_1_v2!CP33` | =DIST_PHASE_1_v2!CP33 |
| Ligne 44 | Col 108 | DD44 | `= (10.679 * DC44) / ((DA44/1000)^4.871 * DB44^1.852)` | = (10.679 * DC44) / ((DA44/1000)^4.871 * DB44^1.852) |
| Ligne 44 | Col 109 | DE44 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E7B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E7B0> |
| Ligne 44 | Col 110 | DF44 | `=IF(CV44>0,
IF(DE44>0, DD44*DE44^1.852,-DD44*ABS(DE44)^1.852),
IF(DE44>0, DD44*CZ44^1.852, -DD44*CZ44^1.852))` | =IF(CV44>0,
IF(DE44>0, DD44*DE44^1.852,-DD44*ABS(DE44)^1.852),
IF(DE44>0, DD44*CZ44^1.852, -DD44*CZ44^1.852)) |
| Ligne 44 | Col 111 | DG44 | `=1.852*DD44*ABS(DE44)^(1.852-1)` | =1.852*DD44*ABS(DE44)^(1.852-1) |
| Ligne 44 | Col 112 | DH44 | `=DE44+CZ78` | =DE44+CZ78 |
| Ligne 45 | Col 4 | D45 | `=DIST_PHASE_1_v2!E34` | =DIST_PHASE_1_v2!E34 |
| Ligne 45 | Col 5 | E45 | `=DIST_PHASE_1_v2!G34` | =DIST_PHASE_1_v2!G34 |
| Ligne 45 | Col 6 | F45 | `=DIST_PHASE_1_v2!L34` | =DIST_PHASE_1_v2!L34 |
| Ligne 45 | Col 7 | G45 | `=DIST_PHASE_1_v2!M34` | =DIST_PHASE_1_v2!M34 |
| Ligne 45 | Col 8 | H45 | `=DIST_PHASE_1_v2!N34` | =DIST_PHASE_1_v2!N34 |
| Ligne 45 | Col 9 | I45 | `= (10.679 * H45) / ((F45/1000)^4.871 * G45^1.852)` | = (10.679 * H45) / ((F45/1000)^4.871 * G45^1.852) |
| Ligne 45 | Col 10 | J45 | `=IF(C45="positif",E45,IF(C45="negatif",-E45,""))` | =IF(C45="positif",E45,IF(C45="negatif",-E45,"")) |
| Ligne 45 | Col 11 | K45 | `=IF(J45>0,I45*E45^1.852,-I45*E45^1.852)` | =IF(J45>0,I45*E45^1.852,-I45*E45^1.852) |
| Ligne 45 | Col 12 | L45 | `=1.852*I45*ABS(E45)^(1.852-1)` | =1.852*I45*ABS(E45)^(1.852-1) |
| Ligne 45 | Col 13 | M45 | `=J45+$D$93` | =J45+$D$93 |
| Ligne 45 | Col 16 | P45 | `=IFERROR(MATCH(S45,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S45,$D$22:$D$91,0),0) |
| Ligne 45 | Col 18 | R45 | `=DIST_PHASE_1_v2!Q34` | =DIST_PHASE_1_v2!Q34 |
| Ligne 45 | Col 19 | S45 | `=DIST_PHASE_1_v2!R34` | =DIST_PHASE_1_v2!R34 |
| Ligne 45 | Col 20 | T45 | `=DIST_PHASE_1_v2!T34` | =DIST_PHASE_1_v2!T34 |
| Ligne 45 | Col 21 | U45 | `=DIST_PHASE_1_v2!Y34` | =DIST_PHASE_1_v2!Y34 |
| Ligne 45 | Col 23 | W45 | `=DIST_PHASE_1_v2!AA34` | =DIST_PHASE_1_v2!AA34 |
| Ligne 45 | Col 24 | X45 | `= (10.679 * W45) / ((U45/1000)^4.871 * V45^1.852)` | = (10.679 * W45) / ((U45/1000)^4.871 * V45^1.852) |
| Ligne 45 | Col 25 | Y45 | `=IF(R45="positif",T45,IF(R45="negatif",-T45,""))` | =IF(R45="positif",T45,IF(R45="negatif",-T45,"")) |
| Ligne 45 | Col 26 | Z45 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E1B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E1B0> |
| Ligne 45 | Col 27 | AA45 | `=IF(P45>0,
IF(R45="positif",1,-1),
0)` | =IF(P45>0,
IF(R45="positif",1,-1),
0) |
| Ligne 45 | Col 28 | AB45 | `=X45*SIGN(Y45)*ABS(Y45)^1.852` | =X45*SIGN(Y45)*ABS(Y45)^1.852 |
| Ligne 45 | Col 29 | AC45 | `=1.852*X45*ABS(Y45)^(1.852-1)` | =1.852*X45*ABS(Y45)^(1.852-1) |
| Ligne 45 | Col 30 | AD45 | `=IF(P45>0,
Y45+($D$93*Z45)+(AA45*$S$93),
Y45+$S$93)` | =IF(P45>0,
Y45+($D$93*Z45)+(AA45*$S$93),
Y45+$S$93) |
| Ligne 45 | Col 32 | AF45 | `=ABS(AD45)-ABS(Y45)` | =ABS(AD45)-ABS(Y45) |
| Ligne 45 | Col 36 | AJ45 | `=IFERROR(MATCH(AM45,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM45,$S$22:$S$91,0),0) |
| Ligne 45 | Col 38 | AL45 | `=TRONCONS_V2!AI32` | =TRONCONS_V2!AI32 |
| Ligne 45 | Col 39 | AM45 | `=TRONCONS_V2!AE32` | =TRONCONS_V2!AE32 |
| Ligne 45 | Col 40 | AN45 | `=DIST_PHASE_1_v2!AG34` | =DIST_PHASE_1_v2!AG34 |
| Ligne 45 | Col 41 | AO45 | `=DIST_PHASE_1_v2!AL34` | =DIST_PHASE_1_v2!AL34 |
| Ligne 45 | Col 43 | AQ45 | `=TRONCONS_V2!AG32` | =TRONCONS_V2!AG32 |
| Ligne 45 | Col 44 | AR45 | `= (10.679 * AQ45) / ((AO45/1000)^4.871 * AP45^1.852)` | = (10.679 * AQ45) / ((AO45/1000)^4.871 * AP45^1.852) |
| Ligne 45 | Col 45 | AS45 | `=IF(AL45="positif",AN45,IF(AL45="negatif",-AN45,""))` | =IF(AL45="positif",AN45,IF(AL45="negatif",-AN45,"")) |
| Ligne 45 | Col 46 | AT45 | `=IF(AJ45>0,
IF(AS45>0, AR45*AS45^1.852,-AR45*ABS(AS45)^1.852),
IF(AS45>0, AR45*AN45^1.852, -AR45*AN45^1.852))` | =IF(AJ45>0,
IF(AS45>0, AR45*AS45^1.852,-AR45*ABS(AS45)^1.852),
IF(AS45>0, AR45*AN45^1.852, -AR45*AN45^1.852)) |
| Ligne 45 | Col 47 | AU45 | `=1.852*AR45*ABS(AS45)^(1.852-1)` | =1.852*AR45*ABS(AS45)^(1.852-1) |
| Ligne 45 | Col 48 | AV45 | `=AS45+$AN$60` | =AS45+$AN$60 |
| Ligne 45 | Col 52 | AZ45 | `=IFERROR(MATCH(BC45,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC45,$AM$22:$AM$57,0),0) |
| Ligne 45 | Col 54 | BB45 | `=DIST_PHASE_1_v2!AQ34` | =DIST_PHASE_1_v2!AQ34 |
| Ligne 45 | Col 55 | BC45 | `=DIST_PHASE_1_v2!AR34` | =DIST_PHASE_1_v2!AR34 |
| Ligne 45 | Col 56 | BD45 | `=DIST_PHASE_1_v2!AT34` | =DIST_PHASE_1_v2!AT34 |
| Ligne 45 | Col 57 | BE45 | `=DIST_PHASE_1_v2!AY34` | =DIST_PHASE_1_v2!AY34 |
| Ligne 45 | Col 58 | BF45 | `=DIST_PHASE_1_v2!AZ34` | =DIST_PHASE_1_v2!AZ34 |
| Ligne 45 | Col 59 | BG45 | `=DIST_PHASE_1_v2!BA34` | =DIST_PHASE_1_v2!BA34 |
| Ligne 45 | Col 60 | BH45 | `= (10.679 * BG45) / ((BE45/1000)^4.871 * BF45^1.852)` | = (10.679 * BG45) / ((BE45/1000)^4.871 * BF45^1.852) |
| Ligne 45 | Col 61 | BI45 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94EB10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94EB10> |
| Ligne 45 | Col 62 | BJ45 | `=IF(AZ45>0,
IF(BI45>0, BH45*BI45^1.852,-BH45*ABS(BI45)^1.852),
IF(BI45>0, BH45*BD45^1.852, -BH45*BD45^1.852))` | =IF(AZ45>0,
IF(BI45>0, BH45*BI45^1.852,-BH45*ABS(BI45)^1.852),
IF(BI45>0, BH45*BD45^1.852, -BH45*BD45^1.852)) |
| Ligne 45 | Col 63 | BK45 | `=1.852*BH45*ABS(BI45)^(1.852-1)` | =1.852*BH45*ABS(BI45)^(1.852-1) |
| Ligne 45 | Col 64 | BL45 | `=BI45+$BD$75` | =BI45+$BD$75 |
| Ligne 45 | Col 68 | BP45 | `=IFERROR(MATCH(BS45,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS45,$BC$22:$BC$73,0),0) |
| Ligne 45 | Col 70 | BR45 | `=DIST_PHASE_1_v2!BF34` | =DIST_PHASE_1_v2!BF34 |
| Ligne 45 | Col 71 | BS45 | `=DIST_PHASE_1_v2!BG34` | =DIST_PHASE_1_v2!BG34 |
| Ligne 45 | Col 72 | BT45 | `=DIST_PHASE_1_v2!BI34` | =DIST_PHASE_1_v2!BI34 |
| Ligne 45 | Col 73 | BU45 | `=DIST_PHASE_1_v2!BN34` | =DIST_PHASE_1_v2!BN34 |
| Ligne 45 | Col 74 | BV45 | `=DIST_PHASE_1_v2!BO34` | =DIST_PHASE_1_v2!BO34 |
| Ligne 45 | Col 75 | BW45 | `=DIST_PHASE_1_v2!BP34` | =DIST_PHASE_1_v2!BP34 |
| Ligne 45 | Col 76 | BX45 | `= (10.679 * BW45) / ((BU45/1000)^4.871 * BV45^1.852)` | = (10.679 * BW45) / ((BU45/1000)^4.871 * BV45^1.852) |
| Ligne 45 | Col 77 | BY45 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94EBD0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94EBD0> |
| Ligne 45 | Col 78 | BZ45 | `=IF(BP45>0,
IF(BY45>0, BX45*BY45^1.852,-BX45*ABS(BY45)^1.852),
IF(BY45>0, BX45*BT45^1.852, -BX45*BT45^1.852))` | =IF(BP45>0,
IF(BY45>0, BX45*BY45^1.852,-BX45*ABS(BY45)^1.852),
IF(BY45>0, BX45*BT45^1.852, -BX45*BT45^1.852)) |
| Ligne 45 | Col 79 | CA45 | `=1.852*BX45*ABS(BY45)^(1.852-1)` | =1.852*BX45*ABS(BY45)^(1.852-1) |
| Ligne 45 | Col 80 | CB45 | `=BY45+$BT$64` | =BY45+$BT$64 |
| Ligne 45 | Col 84 | CF45 | `=IFERROR(MATCH(CI45,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI45,$BS$22:$BS$62,0),0) |
| Ligne 45 | Col 86 | CH45 | `=DIST_PHASE_1_v2!BS34` | =DIST_PHASE_1_v2!BS34 |
| Ligne 45 | Col 87 | CI45 | `=DIST_PHASE_1_v2!BT34` | =DIST_PHASE_1_v2!BT34 |
| Ligne 45 | Col 88 | CJ45 | `=DIST_PHASE_1_v2!BV34` | =DIST_PHASE_1_v2!BV34 |
| Ligne 45 | Col 89 | CK45 | `=DIST_PHASE_1_v2!CA34` | =DIST_PHASE_1_v2!CA34 |
| Ligne 45 | Col 91 | CM45 | `=DIST_PHASE_1_v2!CC34` | =DIST_PHASE_1_v2!CC34 |
| Ligne 45 | Col 92 | CN45 | `= (10.679 * CM45) / ((CK45/1000)^4.871 * CL45^1.852)` | = (10.679 * CM45) / ((CK45/1000)^4.871 * CL45^1.852) |
| Ligne 45 | Col 93 | CO45 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94EC90>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94EC90> |
| Ligne 45 | Col 94 | CP45 | `=IF(CF45>0,
IF(CO45>0, CN45*CO45^1.852,-CN45*ABS(CO45)^1.852),
IF(CO45>0, CN45*CJ45^1.852, -CN45*CJ45^1.852))` | =IF(CF45>0,
IF(CO45>0, CN45*CO45^1.852,-CN45*ABS(CO45)^1.852),
IF(CO45>0, CN45*CJ45^1.852, -CN45*CJ45^1.852)) |
| Ligne 45 | Col 95 | CQ45 | `=1.852*CN45*ABS(CO45)^(1.852-1)` | =1.852*CN45*ABS(CO45)^(1.852-1) |
| Ligne 45 | Col 96 | CR45 | `=CO45+$CJ$71` | =CO45+$CJ$71 |
| Ligne 45 | Col 100 | CV45 | `=IFERROR(MATCH(CY45,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY45,$CI$22:$CI$69,0),0) |
| Ligne 45 | Col 102 | CX45 | `=DIST_PHASE_1_v2!CF34` | =DIST_PHASE_1_v2!CF34 |
| Ligne 45 | Col 103 | CY45 | `=DIST_PHASE_1_v2!CG34` | =DIST_PHASE_1_v2!CG34 |
| Ligne 45 | Col 104 | CZ45 | `=DIST_PHASE_1_v2!CI34` | =DIST_PHASE_1_v2!CI34 |
| Ligne 45 | Col 105 | DA45 | `=DIST_PHASE_1_v2!CN34` | =DIST_PHASE_1_v2!CN34 |
| Ligne 45 | Col 106 | DB45 | `=DIST_PHASE_1_v2!CO34` | =DIST_PHASE_1_v2!CO34 |
| Ligne 45 | Col 107 | DC45 | `=DIST_PHASE_1_v2!CP34` | =DIST_PHASE_1_v2!CP34 |
| Ligne 45 | Col 108 | DD45 | `= (10.679 * DC45) / ((DA45/1000)^4.871 * DB45^1.852)` | = (10.679 * DC45) / ((DA45/1000)^4.871 * DB45^1.852) |
| Ligne 45 | Col 109 | DE45 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94ED50>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94ED50> |
| Ligne 45 | Col 110 | DF45 | `=IF(CV45>0,
IF(DE45>0, DD45*DE45^1.852,-DD45*ABS(DE45)^1.852),
IF(DE45>0, DD45*CZ45^1.852, -DD45*CZ45^1.852))` | =IF(CV45>0,
IF(DE45>0, DD45*DE45^1.852,-DD45*ABS(DE45)^1.852),
IF(DE45>0, DD45*CZ45^1.852, -DD45*CZ45^1.852)) |
| Ligne 45 | Col 111 | DG45 | `=1.852*DD45*ABS(DE45)^(1.852-1)` | =1.852*DD45*ABS(DE45)^(1.852-1) |
| Ligne 45 | Col 112 | DH45 | `=DE45+CZ79` | =DE45+CZ79 |
| Ligne 46 | Col 4 | D46 | `=DIST_PHASE_1_v2!E35` | =DIST_PHASE_1_v2!E35 |
| Ligne 46 | Col 5 | E46 | `=DIST_PHASE_1_v2!G35` | =DIST_PHASE_1_v2!G35 |
| Ligne 46 | Col 6 | F46 | `=DIST_PHASE_1_v2!L35` | =DIST_PHASE_1_v2!L35 |
| Ligne 46 | Col 7 | G46 | `=DIST_PHASE_1_v2!M35` | =DIST_PHASE_1_v2!M35 |
| Ligne 46 | Col 8 | H46 | `=DIST_PHASE_1_v2!N35` | =DIST_PHASE_1_v2!N35 |
| Ligne 46 | Col 9 | I46 | `= (10.679 * H46) / ((F46/1000)^4.871 * G46^1.852)` | = (10.679 * H46) / ((F46/1000)^4.871 * G46^1.852) |
| Ligne 46 | Col 10 | J46 | `=IF(C46="positif",E46,IF(C46="negatif",-E46,""))` | =IF(C46="positif",E46,IF(C46="negatif",-E46,"")) |
| Ligne 46 | Col 11 | K46 | `=IF(J46>0,I46*E46^1.852,-I46*E46^1.852)` | =IF(J46>0,I46*E46^1.852,-I46*E46^1.852) |
| Ligne 46 | Col 12 | L46 | `=1.852*I46*ABS(E46)^(1.852-1)` | =1.852*I46*ABS(E46)^(1.852-1) |
| Ligne 46 | Col 13 | M46 | `=J46+$D$93` | =J46+$D$93 |
| Ligne 46 | Col 16 | P46 | `=IFERROR(MATCH(S46,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S46,$D$22:$D$91,0),0) |
| Ligne 46 | Col 18 | R46 | `=DIST_PHASE_1_v2!Q35` | =DIST_PHASE_1_v2!Q35 |
| Ligne 46 | Col 19 | S46 | `=DIST_PHASE_1_v2!R35` | =DIST_PHASE_1_v2!R35 |
| Ligne 46 | Col 20 | T46 | `=DIST_PHASE_1_v2!T35` | =DIST_PHASE_1_v2!T35 |
| Ligne 46 | Col 21 | U46 | `=DIST_PHASE_1_v2!Y35` | =DIST_PHASE_1_v2!Y35 |
| Ligne 46 | Col 23 | W46 | `=DIST_PHASE_1_v2!AA35` | =DIST_PHASE_1_v2!AA35 |
| Ligne 46 | Col 24 | X46 | `= (10.679 * W46) / ((U46/1000)^4.871 * V46^1.852)` | = (10.679 * W46) / ((U46/1000)^4.871 * V46^1.852) |
| Ligne 46 | Col 25 | Y46 | `=IF(R46="positif",T46,IF(R46="negatif",-T46,""))` | =IF(R46="positif",T46,IF(R46="negatif",-T46,"")) |
| Ligne 46 | Col 26 | Z46 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E210>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94E210> |
| Ligne 46 | Col 27 | AA46 | `=IF(P46>0,
IF(R46="positif",1,-1),
0)` | =IF(P46>0,
IF(R46="positif",1,-1),
0) |
| Ligne 46 | Col 28 | AB46 | `=X46*SIGN(Y46)*ABS(Y46)^1.852` | =X46*SIGN(Y46)*ABS(Y46)^1.852 |
| Ligne 46 | Col 29 | AC46 | `=1.852*X46*ABS(Y46)^(1.852-1)` | =1.852*X46*ABS(Y46)^(1.852-1) |
| Ligne 46 | Col 30 | AD46 | `=IF(P46>0,
Y46+($D$93*Z46)+(AA46*$S$93),
Y46+$S$93)` | =IF(P46>0,
Y46+($D$93*Z46)+(AA46*$S$93),
Y46+$S$93) |
| Ligne 46 | Col 32 | AF46 | `=ABS(AD46)-ABS(Y46)` | =ABS(AD46)-ABS(Y46) |
| Ligne 46 | Col 36 | AJ46 | `=IFERROR(MATCH(AM46,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM46,$S$22:$S$91,0),0) |
| Ligne 46 | Col 38 | AL46 | `=TRONCONS_V2!AI33` | =TRONCONS_V2!AI33 |
| Ligne 46 | Col 39 | AM46 | `=TRONCONS_V2!AE33` | =TRONCONS_V2!AE33 |
| Ligne 46 | Col 40 | AN46 | `=DIST_PHASE_1_v2!AG35` | =DIST_PHASE_1_v2!AG35 |
| Ligne 46 | Col 41 | AO46 | `=DIST_PHASE_1_v2!AL35` | =DIST_PHASE_1_v2!AL35 |
| Ligne 46 | Col 43 | AQ46 | `=TRONCONS_V2!AG33` | =TRONCONS_V2!AG33 |
| Ligne 46 | Col 44 | AR46 | `= (10.679 * AQ46) / ((AO46/1000)^4.871 * AP46^1.852)` | = (10.679 * AQ46) / ((AO46/1000)^4.871 * AP46^1.852) |
| Ligne 46 | Col 45 | AS46 | `=IF(AL46="positif",AN46,IF(AL46="negatif",-AN46,""))` | =IF(AL46="positif",AN46,IF(AL46="negatif",-AN46,"")) |
| Ligne 46 | Col 46 | AT46 | `=IF(AJ46>0,
IF(AS46>0, AR46*AS46^1.852,-AR46*ABS(AS46)^1.852),
IF(AS46>0, AR46*AN46^1.852, -AR46*AN46^1.852))` | =IF(AJ46>0,
IF(AS46>0, AR46*AS46^1.852,-AR46*ABS(AS46)^1.852),
IF(AS46>0, AR46*AN46^1.852, -AR46*AN46^1.852)) |
| Ligne 46 | Col 47 | AU46 | `=1.852*AR46*ABS(AS46)^(1.852-1)` | =1.852*AR46*ABS(AS46)^(1.852-1) |
| Ligne 46 | Col 48 | AV46 | `=AS46+$AN$60` | =AS46+$AN$60 |
| Ligne 46 | Col 52 | AZ46 | `=IFERROR(MATCH(BC46,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC46,$AM$22:$AM$57,0),0) |
| Ligne 46 | Col 54 | BB46 | `=DIST_PHASE_1_v2!AQ35` | =DIST_PHASE_1_v2!AQ35 |
| Ligne 46 | Col 55 | BC46 | `=DIST_PHASE_1_v2!AR35` | =DIST_PHASE_1_v2!AR35 |
| Ligne 46 | Col 56 | BD46 | `=DIST_PHASE_1_v2!AT35` | =DIST_PHASE_1_v2!AT35 |
| Ligne 46 | Col 57 | BE46 | `=DIST_PHASE_1_v2!AY35` | =DIST_PHASE_1_v2!AY35 |
| Ligne 46 | Col 58 | BF46 | `=DIST_PHASE_1_v2!AZ35` | =DIST_PHASE_1_v2!AZ35 |
| Ligne 46 | Col 59 | BG46 | `=DIST_PHASE_1_v2!BA35` | =DIST_PHASE_1_v2!BA35 |
| Ligne 46 | Col 60 | BH46 | `= (10.679 * BG46) / ((BE46/1000)^4.871 * BF46^1.852)` | = (10.679 * BG46) / ((BE46/1000)^4.871 * BF46^1.852) |
| Ligne 46 | Col 61 | BI46 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F110>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F110> |
| Ligne 46 | Col 62 | BJ46 | `=IF(AZ46>0,
IF(BI46>0, BH46*BI46^1.852,-BH46*ABS(BI46)^1.852),
IF(BI46>0, BH46*BD46^1.852, -BH46*BD46^1.852))` | =IF(AZ46>0,
IF(BI46>0, BH46*BI46^1.852,-BH46*ABS(BI46)^1.852),
IF(BI46>0, BH46*BD46^1.852, -BH46*BD46^1.852)) |
| Ligne 46 | Col 63 | BK46 | `=1.852*BH46*ABS(BI46)^(1.852-1)` | =1.852*BH46*ABS(BI46)^(1.852-1) |
| Ligne 46 | Col 64 | BL46 | `=BI46+$BD$75` | =BI46+$BD$75 |
| Ligne 46 | Col 68 | BP46 | `=IFERROR(MATCH(BS46,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS46,$BC$22:$BC$73,0),0) |
| Ligne 46 | Col 70 | BR46 | `=DIST_PHASE_1_v2!BF35` | =DIST_PHASE_1_v2!BF35 |
| Ligne 46 | Col 71 | BS46 | `=DIST_PHASE_1_v2!BG35` | =DIST_PHASE_1_v2!BG35 |
| Ligne 46 | Col 72 | BT46 | `=DIST_PHASE_1_v2!BI35` | =DIST_PHASE_1_v2!BI35 |
| Ligne 46 | Col 73 | BU46 | `=DIST_PHASE_1_v2!BN35` | =DIST_PHASE_1_v2!BN35 |
| Ligne 46 | Col 74 | BV46 | `=DIST_PHASE_1_v2!BO35` | =DIST_PHASE_1_v2!BO35 |
| Ligne 46 | Col 75 | BW46 | `=DIST_PHASE_1_v2!BP35` | =DIST_PHASE_1_v2!BP35 |
| Ligne 46 | Col 76 | BX46 | `= (10.679 * BW46) / ((BU46/1000)^4.871 * BV46^1.852)` | = (10.679 * BW46) / ((BU46/1000)^4.871 * BV46^1.852) |
| Ligne 46 | Col 77 | BY46 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F1D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F1D0> |
| Ligne 46 | Col 78 | BZ46 | `=IF(BP46>0,
IF(BY46>0, BX46*BY46^1.852,-BX46*ABS(BY46)^1.852),
IF(BY46>0, BX46*BT46^1.852, -BX46*BT46^1.852))` | =IF(BP46>0,
IF(BY46>0, BX46*BY46^1.852,-BX46*ABS(BY46)^1.852),
IF(BY46>0, BX46*BT46^1.852, -BX46*BT46^1.852)) |
| Ligne 46 | Col 79 | CA46 | `=1.852*BX46*ABS(BY46)^(1.852-1)` | =1.852*BX46*ABS(BY46)^(1.852-1) |
| Ligne 46 | Col 80 | CB46 | `=BY46+$BT$64` | =BY46+$BT$64 |
| Ligne 46 | Col 84 | CF46 | `=IFERROR(MATCH(CI46,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI46,$BS$22:$BS$62,0),0) |
| Ligne 46 | Col 86 | CH46 | `=DIST_PHASE_1_v2!BS35` | =DIST_PHASE_1_v2!BS35 |
| Ligne 46 | Col 87 | CI46 | `=DIST_PHASE_1_v2!BT35` | =DIST_PHASE_1_v2!BT35 |
| Ligne 46 | Col 88 | CJ46 | `=DIST_PHASE_1_v2!BV35` | =DIST_PHASE_1_v2!BV35 |
| Ligne 46 | Col 89 | CK46 | `=DIST_PHASE_1_v2!CA35` | =DIST_PHASE_1_v2!CA35 |
| Ligne 46 | Col 91 | CM46 | `=DIST_PHASE_1_v2!CC35` | =DIST_PHASE_1_v2!CC35 |
| Ligne 46 | Col 92 | CN46 | `= (10.679 * CM46) / ((CK46/1000)^4.871 * CL46^1.852)` | = (10.679 * CM46) / ((CK46/1000)^4.871 * CL46^1.852) |
| Ligne 46 | Col 93 | CO46 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F290>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F290> |
| Ligne 46 | Col 94 | CP46 | `=IF(CF46>0,
IF(CO46>0, CN46*CO46^1.852,-CN46*ABS(CO46)^1.852),
IF(CO46>0, CN46*CJ46^1.852, -CN46*CJ46^1.852))` | =IF(CF46>0,
IF(CO46>0, CN46*CO46^1.852,-CN46*ABS(CO46)^1.852),
IF(CO46>0, CN46*CJ46^1.852, -CN46*CJ46^1.852)) |
| Ligne 46 | Col 95 | CQ46 | `=1.852*CN46*ABS(CO46)^(1.852-1)` | =1.852*CN46*ABS(CO46)^(1.852-1) |
| Ligne 46 | Col 96 | CR46 | `=CO46+$CJ$71` | =CO46+$CJ$71 |
| Ligne 46 | Col 100 | CV46 | `=IFERROR(MATCH(CY46,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY46,$CI$22:$CI$69,0),0) |
| Ligne 46 | Col 102 | CX46 | `=DIST_PHASE_1_v2!CF35` | =DIST_PHASE_1_v2!CF35 |
| Ligne 46 | Col 103 | CY46 | `=DIST_PHASE_1_v2!CG35` | =DIST_PHASE_1_v2!CG35 |
| Ligne 46 | Col 104 | CZ46 | `=DIST_PHASE_1_v2!CI35` | =DIST_PHASE_1_v2!CI35 |
| Ligne 46 | Col 105 | DA46 | `=DIST_PHASE_1_v2!CN35` | =DIST_PHASE_1_v2!CN35 |
| Ligne 46 | Col 106 | DB46 | `=DIST_PHASE_1_v2!CO35` | =DIST_PHASE_1_v2!CO35 |
| Ligne 46 | Col 107 | DC46 | `=DIST_PHASE_1_v2!CP35` | =DIST_PHASE_1_v2!CP35 |
| Ligne 46 | Col 108 | DD46 | `= (10.679 * DC46) / ((DA46/1000)^4.871 * DB46^1.852)` | = (10.679 * DC46) / ((DA46/1000)^4.871 * DB46^1.852) |
| Ligne 46 | Col 109 | DE46 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F350>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F350> |
| Ligne 46 | Col 110 | DF46 | `=IF(CV46>0,
IF(DE46>0, DD46*DE46^1.852,-DD46*ABS(DE46)^1.852),
IF(DE46>0, DD46*CZ46^1.852, -DD46*CZ46^1.852))` | =IF(CV46>0,
IF(DE46>0, DD46*DE46^1.852,-DD46*ABS(DE46)^1.852),
IF(DE46>0, DD46*CZ46^1.852, -DD46*CZ46^1.852)) |
| Ligne 46 | Col 111 | DG46 | `=1.852*DD46*ABS(DE46)^(1.852-1)` | =1.852*DD46*ABS(DE46)^(1.852-1) |
| Ligne 46 | Col 112 | DH46 | `=DE46+CZ80` | =DE46+CZ80 |
| Ligne 47 | Col 4 | D47 | `=DIST_PHASE_1_v2!E36` | =DIST_PHASE_1_v2!E36 |
| Ligne 47 | Col 5 | E47 | `=DIST_PHASE_1_v2!G36` | =DIST_PHASE_1_v2!G36 |
| Ligne 47 | Col 6 | F47 | `=DIST_PHASE_1_v2!L36` | =DIST_PHASE_1_v2!L36 |
| Ligne 47 | Col 7 | G47 | `=DIST_PHASE_1_v2!M36` | =DIST_PHASE_1_v2!M36 |
| Ligne 47 | Col 8 | H47 | `=DIST_PHASE_1_v2!N36` | =DIST_PHASE_1_v2!N36 |
| Ligne 47 | Col 9 | I47 | `= (10.679 * H47) / ((F47/1000)^4.871 * G47^1.852)` | = (10.679 * H47) / ((F47/1000)^4.871 * G47^1.852) |
| Ligne 47 | Col 10 | J47 | `=IF(C47="positif",E47,IF(C47="negatif",-E47,""))` | =IF(C47="positif",E47,IF(C47="negatif",-E47,"")) |
| Ligne 47 | Col 11 | K47 | `=IF(J47>0,I47*E47^1.852,-I47*E47^1.852)` | =IF(J47>0,I47*E47^1.852,-I47*E47^1.852) |
| Ligne 47 | Col 12 | L47 | `=1.852*I47*ABS(E47)^(1.852-1)` | =1.852*I47*ABS(E47)^(1.852-1) |
| Ligne 47 | Col 13 | M47 | `=J47+$D$93` | =J47+$D$93 |
| Ligne 47 | Col 16 | P47 | `=IFERROR(MATCH(S47,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S47,$D$22:$D$91,0),0) |
| Ligne 47 | Col 18 | R47 | `=DIST_PHASE_1_v2!Q36` | =DIST_PHASE_1_v2!Q36 |
| Ligne 47 | Col 19 | S47 | `=DIST_PHASE_1_v2!R36` | =DIST_PHASE_1_v2!R36 |
| Ligne 47 | Col 20 | T47 | `=DIST_PHASE_1_v2!T36` | =DIST_PHASE_1_v2!T36 |
| Ligne 47 | Col 21 | U47 | `=DIST_PHASE_1_v2!Y36` | =DIST_PHASE_1_v2!Y36 |
| Ligne 47 | Col 23 | W47 | `=DIST_PHASE_1_v2!AA36` | =DIST_PHASE_1_v2!AA36 |
| Ligne 47 | Col 24 | X47 | `= (10.679 * W47) / ((U47/1000)^4.871 * V47^1.852)` | = (10.679 * W47) / ((U47/1000)^4.871 * V47^1.852) |
| Ligne 47 | Col 25 | Y47 | `=IF(R47="positif",T47,IF(R47="negatif",-T47,""))` | =IF(R47="positif",T47,IF(R47="negatif",-T47,"")) |
| Ligne 47 | Col 26 | Z47 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94EF30>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94EF30> |
| Ligne 47 | Col 27 | AA47 | `=IF(P47>0,
IF(R47="positif",1,-1),
0)` | =IF(P47>0,
IF(R47="positif",1,-1),
0) |
| Ligne 47 | Col 28 | AB47 | `=X47*SIGN(Y47)*ABS(Y47)^1.852` | =X47*SIGN(Y47)*ABS(Y47)^1.852 |
| Ligne 47 | Col 29 | AC47 | `=1.852*X47*ABS(Y47)^(1.852-1)` | =1.852*X47*ABS(Y47)^(1.852-1) |
| Ligne 47 | Col 30 | AD47 | `=IF(P47>0,
Y47+($D$93*Z47)+(AA47*$S$93),
Y47+$S$93)` | =IF(P47>0,
Y47+($D$93*Z47)+(AA47*$S$93),
Y47+$S$93) |
| Ligne 47 | Col 32 | AF47 | `=ABS(AD47)-ABS(Y47)` | =ABS(AD47)-ABS(Y47) |
| Ligne 47 | Col 36 | AJ47 | `=IFERROR(MATCH(AM47,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM47,$S$22:$S$91,0),0) |
| Ligne 47 | Col 38 | AL47 | `=TRONCONS_V2!AI34` | =TRONCONS_V2!AI34 |
| Ligne 47 | Col 39 | AM47 | `=TRONCONS_V2!AE34` | =TRONCONS_V2!AE34 |
| Ligne 47 | Col 40 | AN47 | `=DIST_PHASE_1_v2!AG36` | =DIST_PHASE_1_v2!AG36 |
| Ligne 47 | Col 41 | AO47 | `=DIST_PHASE_1_v2!AL36` | =DIST_PHASE_1_v2!AL36 |
| Ligne 47 | Col 43 | AQ47 | `=TRONCONS_V2!AG34` | =TRONCONS_V2!AG34 |
| Ligne 47 | Col 44 | AR47 | `= (10.679 * AQ47) / ((AO47/1000)^4.871 * AP47^1.852)` | = (10.679 * AQ47) / ((AO47/1000)^4.871 * AP47^1.852) |
| Ligne 47 | Col 45 | AS47 | `=IF(AL47="positif",AN47,IF(AL47="negatif",-AN47,""))` | =IF(AL47="positif",AN47,IF(AL47="negatif",-AN47,"")) |
| Ligne 47 | Col 46 | AT47 | `=IF(AJ47>0,
IF(AS47>0, AR47*AS47^1.852,-AR47*ABS(AS47)^1.852),
IF(AS47>0, AR47*AN47^1.852, -AR47*AN47^1.852))` | =IF(AJ47>0,
IF(AS47>0, AR47*AS47^1.852,-AR47*ABS(AS47)^1.852),
IF(AS47>0, AR47*AN47^1.852, -AR47*AN47^1.852)) |
| Ligne 47 | Col 47 | AU47 | `=1.852*AR47*ABS(AS47)^(1.852-1)` | =1.852*AR47*ABS(AS47)^(1.852-1) |
| Ligne 47 | Col 48 | AV47 | `=AS47+$AN$60` | =AS47+$AN$60 |
| Ligne 47 | Col 52 | AZ47 | `=IFERROR(MATCH(BC47,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC47,$AM$22:$AM$57,0),0) |
| Ligne 47 | Col 54 | BB47 | `=DIST_PHASE_1_v2!AQ36` | =DIST_PHASE_1_v2!AQ36 |
| Ligne 47 | Col 55 | BC47 | `=DIST_PHASE_1_v2!AR36` | =DIST_PHASE_1_v2!AR36 |
| Ligne 47 | Col 56 | BD47 | `=DIST_PHASE_1_v2!AT36` | =DIST_PHASE_1_v2!AT36 |
| Ligne 47 | Col 57 | BE47 | `=DIST_PHASE_1_v2!AY36` | =DIST_PHASE_1_v2!AY36 |
| Ligne 47 | Col 58 | BF47 | `=DIST_PHASE_1_v2!AZ36` | =DIST_PHASE_1_v2!AZ36 |
| Ligne 47 | Col 59 | BG47 | `=DIST_PHASE_1_v2!BA36` | =DIST_PHASE_1_v2!BA36 |
| Ligne 47 | Col 60 | BH47 | `= (10.679 * BG47) / ((BE47/1000)^4.871 * BF47^1.852)` | = (10.679 * BG47) / ((BE47/1000)^4.871 * BF47^1.852) |
| Ligne 47 | Col 61 | BI47 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F7D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F7D0> |
| Ligne 47 | Col 62 | BJ47 | `=IF(AZ47>0,
IF(BI47>0, BH47*BI47^1.852,-BH47*ABS(BI47)^1.852),
IF(BI47>0, BH47*BD47^1.852, -BH47*BD47^1.852))` | =IF(AZ47>0,
IF(BI47>0, BH47*BI47^1.852,-BH47*ABS(BI47)^1.852),
IF(BI47>0, BH47*BD47^1.852, -BH47*BD47^1.852)) |
| Ligne 47 | Col 63 | BK47 | `=1.852*BH47*ABS(BI47)^(1.852-1)` | =1.852*BH47*ABS(BI47)^(1.852-1) |
| Ligne 47 | Col 64 | BL47 | `=BI47+$BD$75` | =BI47+$BD$75 |
| Ligne 47 | Col 68 | BP47 | `=IFERROR(MATCH(BS47,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS47,$BC$22:$BC$73,0),0) |
| Ligne 47 | Col 70 | BR47 | `=DIST_PHASE_1_v2!BF36` | =DIST_PHASE_1_v2!BF36 |
| Ligne 47 | Col 71 | BS47 | `=DIST_PHASE_1_v2!BG36` | =DIST_PHASE_1_v2!BG36 |
| Ligne 47 | Col 72 | BT47 | `=DIST_PHASE_1_v2!BI36` | =DIST_PHASE_1_v2!BI36 |
| Ligne 47 | Col 73 | BU47 | `=DIST_PHASE_1_v2!BN36` | =DIST_PHASE_1_v2!BN36 |
| Ligne 47 | Col 74 | BV47 | `=DIST_PHASE_1_v2!BO36` | =DIST_PHASE_1_v2!BO36 |
| Ligne 47 | Col 75 | BW47 | `=DIST_PHASE_1_v2!BP36` | =DIST_PHASE_1_v2!BP36 |
| Ligne 47 | Col 76 | BX47 | `= (10.679 * BW47) / ((BU47/1000)^4.871 * BV47^1.852)` | = (10.679 * BW47) / ((BU47/1000)^4.871 * BV47^1.852) |
| Ligne 47 | Col 77 | BY47 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F890>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F890> |
| Ligne 47 | Col 78 | BZ47 | `=IF(BP47>0,
IF(BY47>0, BX47*BY47^1.852,-BX47*ABS(BY47)^1.852),
IF(BY47>0, BX47*BT47^1.852, -BX47*BT47^1.852))` | =IF(BP47>0,
IF(BY47>0, BX47*BY47^1.852,-BX47*ABS(BY47)^1.852),
IF(BY47>0, BX47*BT47^1.852, -BX47*BT47^1.852)) |
| Ligne 47 | Col 79 | CA47 | `=1.852*BX47*ABS(BY47)^(1.852-1)` | =1.852*BX47*ABS(BY47)^(1.852-1) |
| Ligne 47 | Col 80 | CB47 | `=BY47+$BT$64` | =BY47+$BT$64 |
| Ligne 47 | Col 84 | CF47 | `=IFERROR(MATCH(CI47,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI47,$BS$22:$BS$62,0),0) |
| Ligne 47 | Col 86 | CH47 | `=DIST_PHASE_1_v2!BS36` | =DIST_PHASE_1_v2!BS36 |
| Ligne 47 | Col 87 | CI47 | `=DIST_PHASE_1_v2!BT36` | =DIST_PHASE_1_v2!BT36 |
| Ligne 47 | Col 88 | CJ47 | `=DIST_PHASE_1_v2!BV36` | =DIST_PHASE_1_v2!BV36 |
| Ligne 47 | Col 89 | CK47 | `=DIST_PHASE_1_v2!CA36` | =DIST_PHASE_1_v2!CA36 |
| Ligne 47 | Col 91 | CM47 | `=DIST_PHASE_1_v2!CC36` | =DIST_PHASE_1_v2!CC36 |
| Ligne 47 | Col 92 | CN47 | `= (10.679 * CM47) / ((CK47/1000)^4.871 * CL47^1.852)` | = (10.679 * CM47) / ((CK47/1000)^4.871 * CL47^1.852) |
| Ligne 47 | Col 93 | CO47 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F950>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F950> |
| Ligne 47 | Col 94 | CP47 | `=IF(CF47>0,
IF(CO47>0, CN47*CO47^1.852,-CN47*ABS(CO47)^1.852),
IF(CO47>0, CN47*CJ47^1.852, -CN47*CJ47^1.852))` | =IF(CF47>0,
IF(CO47>0, CN47*CO47^1.852,-CN47*ABS(CO47)^1.852),
IF(CO47>0, CN47*CJ47^1.852, -CN47*CJ47^1.852)) |
| Ligne 47 | Col 95 | CQ47 | `=1.852*CN47*ABS(CO47)^(1.852-1)` | =1.852*CN47*ABS(CO47)^(1.852-1) |
| Ligne 47 | Col 96 | CR47 | `=CO47+$CJ$71` | =CO47+$CJ$71 |
| Ligne 47 | Col 100 | CV47 | `=IFERROR(MATCH(CY47,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY47,$CI$22:$CI$69,0),0) |
| Ligne 47 | Col 102 | CX47 | `=DIST_PHASE_1_v2!CF36` | =DIST_PHASE_1_v2!CF36 |
| Ligne 47 | Col 103 | CY47 | `=DIST_PHASE_1_v2!CG36` | =DIST_PHASE_1_v2!CG36 |
| Ligne 47 | Col 104 | CZ47 | `=DIST_PHASE_1_v2!CI36` | =DIST_PHASE_1_v2!CI36 |
| Ligne 47 | Col 105 | DA47 | `=DIST_PHASE_1_v2!CN36` | =DIST_PHASE_1_v2!CN36 |
| Ligne 47 | Col 106 | DB47 | `=DIST_PHASE_1_v2!CO36` | =DIST_PHASE_1_v2!CO36 |
| Ligne 47 | Col 107 | DC47 | `=DIST_PHASE_1_v2!CP36` | =DIST_PHASE_1_v2!CP36 |
| Ligne 47 | Col 108 | DD47 | `= (10.679 * DC47) / ((DA47/1000)^4.871 * DB47^1.852)` | = (10.679 * DC47) / ((DA47/1000)^4.871 * DB47^1.852) |
| Ligne 47 | Col 109 | DE47 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FA10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FA10> |
| Ligne 47 | Col 110 | DF47 | `=IF(CV47>0,
IF(DE47>0, DD47*DE47^1.852,-DD47*ABS(DE47)^1.852),
IF(DE47>0, DD47*CZ47^1.852, -DD47*CZ47^1.852))` | =IF(CV47>0,
IF(DE47>0, DD47*DE47^1.852,-DD47*ABS(DE47)^1.852),
IF(DE47>0, DD47*CZ47^1.852, -DD47*CZ47^1.852)) |
| Ligne 47 | Col 111 | DG47 | `=1.852*DD47*ABS(DE47)^(1.852-1)` | =1.852*DD47*ABS(DE47)^(1.852-1) |
| Ligne 47 | Col 112 | DH47 | `=DE47+CZ81` | =DE47+CZ81 |
| Ligne 48 | Col 4 | D48 | `=DIST_PHASE_1_v2!E37` | =DIST_PHASE_1_v2!E37 |
| Ligne 48 | Col 5 | E48 | `=DIST_PHASE_1_v2!G37` | =DIST_PHASE_1_v2!G37 |
| Ligne 48 | Col 6 | F48 | `=DIST_PHASE_1_v2!L37` | =DIST_PHASE_1_v2!L37 |
| Ligne 48 | Col 7 | G48 | `=DIST_PHASE_1_v2!M37` | =DIST_PHASE_1_v2!M37 |
| Ligne 48 | Col 8 | H48 | `=DIST_PHASE_1_v2!N37` | =DIST_PHASE_1_v2!N37 |
| Ligne 48 | Col 9 | I48 | `= (10.679 * H48) / ((F48/1000)^4.871 * G48^1.852)` | = (10.679 * H48) / ((F48/1000)^4.871 * G48^1.852) |
| Ligne 48 | Col 10 | J48 | `=IF(C48="positif",E48,IF(C48="negatif",-E48,""))` | =IF(C48="positif",E48,IF(C48="negatif",-E48,"")) |
| Ligne 48 | Col 11 | K48 | `=IF(J48>0,I48*E48^1.852,-I48*E48^1.852)` | =IF(J48>0,I48*E48^1.852,-I48*E48^1.852) |
| Ligne 48 | Col 12 | L48 | `=1.852*I48*ABS(E48)^(1.852-1)` | =1.852*I48*ABS(E48)^(1.852-1) |
| Ligne 48 | Col 13 | M48 | `=J48+$D$93` | =J48+$D$93 |
| Ligne 48 | Col 16 | P48 | `=IFERROR(MATCH(S48,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S48,$D$22:$D$91,0),0) |
| Ligne 48 | Col 18 | R48 | `=DIST_PHASE_1_v2!Q37` | =DIST_PHASE_1_v2!Q37 |
| Ligne 48 | Col 19 | S48 | `=DIST_PHASE_1_v2!R37` | =DIST_PHASE_1_v2!R37 |
| Ligne 48 | Col 20 | T48 | `=DIST_PHASE_1_v2!T37` | =DIST_PHASE_1_v2!T37 |
| Ligne 48 | Col 21 | U48 | `=DIST_PHASE_1_v2!Y37` | =DIST_PHASE_1_v2!Y37 |
| Ligne 48 | Col 23 | W48 | `=DIST_PHASE_1_v2!AA37` | =DIST_PHASE_1_v2!AA37 |
| Ligne 48 | Col 24 | X48 | `= (10.679 * W48) / ((U48/1000)^4.871 * V48^1.852)` | = (10.679 * W48) / ((U48/1000)^4.871 * V48^1.852) |
| Ligne 48 | Col 25 | Y48 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FB30>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FB30> |
| Ligne 48 | Col 26 | Z48 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F3B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F3B0> |
| Ligne 48 | Col 27 | AA48 | `=IF(P48>0,
IF(R48="positif",1,-1),
0)` | =IF(P48>0,
IF(R48="positif",1,-1),
0) |
| Ligne 48 | Col 28 | AB48 | `=X48*SIGN(Y48)*ABS(Y48)^1.852` | =X48*SIGN(Y48)*ABS(Y48)^1.852 |
| Ligne 48 | Col 29 | AC48 | `=1.852*X48*ABS(Y48)^(1.852-1)` | =1.852*X48*ABS(Y48)^(1.852-1) |
| Ligne 48 | Col 30 | AD48 | `=IF(P48>0,
Y48+($D$93*Z48)+(AA48*$S$93),
Y48+$S$93)` | =IF(P48>0,
Y48+($D$93*Z48)+(AA48*$S$93),
Y48+$S$93) |
| Ligne 48 | Col 32 | AF48 | `=ABS(AD48)-ABS(Y48)` | =ABS(AD48)-ABS(Y48) |
| Ligne 48 | Col 36 | AJ48 | `=IFERROR(MATCH(AM48,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM48,$S$22:$S$91,0),0) |
| Ligne 48 | Col 38 | AL48 | `=TRONCONS_V2!AI35` | =TRONCONS_V2!AI35 |
| Ligne 48 | Col 39 | AM48 | `=TRONCONS_V2!AE35` | =TRONCONS_V2!AE35 |
| Ligne 48 | Col 40 | AN48 | `=DIST_PHASE_1_v2!AG37` | =DIST_PHASE_1_v2!AG37 |
| Ligne 48 | Col 41 | AO48 | `=DIST_PHASE_1_v2!AL37` | =DIST_PHASE_1_v2!AL37 |
| Ligne 48 | Col 43 | AQ48 | `=TRONCONS_V2!AG35` | =TRONCONS_V2!AG35 |
| Ligne 48 | Col 44 | AR48 | `= (10.679 * AQ48) / ((AO48/1000)^4.871 * AP48^1.852)` | = (10.679 * AQ48) / ((AO48/1000)^4.871 * AP48^1.852) |
| Ligne 48 | Col 45 | AS48 | `=IF(AL48="positif",AN48,IF(AL48="negatif",-AN48,""))` | =IF(AL48="positif",AN48,IF(AL48="negatif",-AN48,"")) |
| Ligne 48 | Col 46 | AT48 | `=IF(AJ48>0,
IF(AS48>0, AR48*AS48^1.852,-AR48*ABS(AS48)^1.852),
IF(AS48>0, AR48*AN48^1.852, -AR48*AN48^1.852))` | =IF(AJ48>0,
IF(AS48>0, AR48*AS48^1.852,-AR48*ABS(AS48)^1.852),
IF(AS48>0, AR48*AN48^1.852, -AR48*AN48^1.852)) |
| Ligne 48 | Col 47 | AU48 | `=1.852*AR48*ABS(AS48)^(1.852-1)` | =1.852*AR48*ABS(AS48)^(1.852-1) |
| Ligne 48 | Col 48 | AV48 | `=AS48+$AN$60` | =AS48+$AN$60 |
| Ligne 48 | Col 52 | AZ48 | `=IFERROR(MATCH(BC48,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC48,$AM$22:$AM$57,0),0) |
| Ligne 48 | Col 54 | BB48 | `=DIST_PHASE_1_v2!AQ37` | =DIST_PHASE_1_v2!AQ37 |
| Ligne 48 | Col 55 | BC48 | `=DIST_PHASE_1_v2!AR37` | =DIST_PHASE_1_v2!AR37 |
| Ligne 48 | Col 56 | BD48 | `=DIST_PHASE_1_v2!AT37` | =DIST_PHASE_1_v2!AT37 |
| Ligne 48 | Col 57 | BE48 | `=DIST_PHASE_1_v2!AY37` | =DIST_PHASE_1_v2!AY37 |
| Ligne 48 | Col 58 | BF48 | `=DIST_PHASE_1_v2!AZ37` | =DIST_PHASE_1_v2!AZ37 |
| Ligne 48 | Col 59 | BG48 | `=DIST_PHASE_1_v2!BA37` | =DIST_PHASE_1_v2!BA37 |
| Ligne 48 | Col 60 | BH48 | `= (10.679 * BG48) / ((BE48/1000)^4.871 * BF48^1.852)` | = (10.679 * BG48) / ((BE48/1000)^4.871 * BF48^1.852) |
| Ligne 48 | Col 61 | BI48 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FDD0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FDD0> |
| Ligne 48 | Col 62 | BJ48 | `=IF(AZ48>0,
IF(BI48>0, BH48*BI48^1.852,-BH48*ABS(BI48)^1.852),
IF(BI48>0, BH48*BD48^1.852, -BH48*BD48^1.852))` | =IF(AZ48>0,
IF(BI48>0, BH48*BI48^1.852,-BH48*ABS(BI48)^1.852),
IF(BI48>0, BH48*BD48^1.852, -BH48*BD48^1.852)) |
| Ligne 48 | Col 63 | BK48 | `=1.852*BH48*ABS(BI48)^(1.852-1)` | =1.852*BH48*ABS(BI48)^(1.852-1) |
| Ligne 48 | Col 64 | BL48 | `=BI48+$BD$75` | =BI48+$BD$75 |
| Ligne 48 | Col 68 | BP48 | `=IFERROR(MATCH(BS48,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS48,$BC$22:$BC$73,0),0) |
| Ligne 48 | Col 70 | BR48 | `=DIST_PHASE_1_v2!BF37` | =DIST_PHASE_1_v2!BF37 |
| Ligne 48 | Col 71 | BS48 | `=DIST_PHASE_1_v2!BG37` | =DIST_PHASE_1_v2!BG37 |
| Ligne 48 | Col 72 | BT48 | `=DIST_PHASE_1_v2!BI37` | =DIST_PHASE_1_v2!BI37 |
| Ligne 48 | Col 73 | BU48 | `=DIST_PHASE_1_v2!BN37` | =DIST_PHASE_1_v2!BN37 |
| Ligne 48 | Col 74 | BV48 | `=DIST_PHASE_1_v2!BO37` | =DIST_PHASE_1_v2!BO37 |
| Ligne 48 | Col 75 | BW48 | `=DIST_PHASE_1_v2!BP37` | =DIST_PHASE_1_v2!BP37 |
| Ligne 48 | Col 76 | BX48 | `= (10.679 * BW48) / ((BU48/1000)^4.871 * BV48^1.852)` | = (10.679 * BW48) / ((BU48/1000)^4.871 * BV48^1.852) |
| Ligne 48 | Col 77 | BY48 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FE90>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FE90> |
| Ligne 48 | Col 78 | BZ48 | `=IF(BP48>0,
IF(BY48>0, BX48*BY48^1.852,-BX48*ABS(BY48)^1.852),
IF(BY48>0, BX48*BT48^1.852, -BX48*BT48^1.852))` | =IF(BP48>0,
IF(BY48>0, BX48*BY48^1.852,-BX48*ABS(BY48)^1.852),
IF(BY48>0, BX48*BT48^1.852, -BX48*BT48^1.852)) |
| Ligne 48 | Col 79 | CA48 | `=1.852*BX48*ABS(BY48)^(1.852-1)` | =1.852*BX48*ABS(BY48)^(1.852-1) |
| Ligne 48 | Col 80 | CB48 | `=BY48+$BT$64` | =BY48+$BT$64 |
| Ligne 48 | Col 84 | CF48 | `=IFERROR(MATCH(CI48,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI48,$BS$22:$BS$62,0),0) |
| Ligne 48 | Col 86 | CH48 | `=DIST_PHASE_1_v2!BS37` | =DIST_PHASE_1_v2!BS37 |
| Ligne 48 | Col 87 | CI48 | `=DIST_PHASE_1_v2!BT37` | =DIST_PHASE_1_v2!BT37 |
| Ligne 48 | Col 88 | CJ48 | `=DIST_PHASE_1_v2!BV37` | =DIST_PHASE_1_v2!BV37 |
| Ligne 48 | Col 89 | CK48 | `=DIST_PHASE_1_v2!CA37` | =DIST_PHASE_1_v2!CA37 |
| Ligne 48 | Col 91 | CM48 | `=DIST_PHASE_1_v2!CC37` | =DIST_PHASE_1_v2!CC37 |
| Ligne 48 | Col 92 | CN48 | `= (10.679 * CM48) / ((CK48/1000)^4.871 * CL48^1.852)` | = (10.679 * CM48) / ((CK48/1000)^4.871 * CL48^1.852) |
| Ligne 48 | Col 93 | CO48 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FF50>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FF50> |
| Ligne 48 | Col 94 | CP48 | `=IF(CF48>0,
IF(CO48>0, CN48*CO48^1.852,-CN48*ABS(CO48)^1.852),
IF(CO48>0, CN48*CJ48^1.852, -CN48*CJ48^1.852))` | =IF(CF48>0,
IF(CO48>0, CN48*CO48^1.852,-CN48*ABS(CO48)^1.852),
IF(CO48>0, CN48*CJ48^1.852, -CN48*CJ48^1.852)) |
| Ligne 48 | Col 95 | CQ48 | `=1.852*CN48*ABS(CO48)^(1.852-1)` | =1.852*CN48*ABS(CO48)^(1.852-1) |
| Ligne 48 | Col 96 | CR48 | `=CO48+$CJ$71` | =CO48+$CJ$71 |
| Ligne 48 | Col 100 | CV48 | `=IFERROR(MATCH(CY48,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY48,$CI$22:$CI$69,0),0) |
| Ligne 48 | Col 102 | CX48 | `=DIST_PHASE_1_v2!CF37` | =DIST_PHASE_1_v2!CF37 |
| Ligne 48 | Col 103 | CY48 | `=DIST_PHASE_1_v2!CG37` | =DIST_PHASE_1_v2!CG37 |
| Ligne 48 | Col 104 | CZ48 | `=DIST_PHASE_1_v2!CI37` | =DIST_PHASE_1_v2!CI37 |
| Ligne 48 | Col 105 | DA48 | `=DIST_PHASE_1_v2!CN37` | =DIST_PHASE_1_v2!CN37 |
| Ligne 48 | Col 106 | DB48 | `=DIST_PHASE_1_v2!CO37` | =DIST_PHASE_1_v2!CO37 |
| Ligne 48 | Col 107 | DC48 | `=DIST_PHASE_1_v2!CP37` | =DIST_PHASE_1_v2!CP37 |
| Ligne 48 | Col 108 | DD48 | `= (10.679 * DC48) / ((DA48/1000)^4.871 * DB48^1.852)` | = (10.679 * DC48) / ((DA48/1000)^4.871 * DB48^1.852) |
| Ligne 48 | Col 109 | DE48 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994050>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994050> |
| Ligne 48 | Col 110 | DF48 | `=IF(CV48>0,
IF(DE48>0, DD48*DE48^1.852,-DD48*ABS(DE48)^1.852),
IF(DE48>0, DD48*CZ48^1.852, -DD48*CZ48^1.852))` | =IF(CV48>0,
IF(DE48>0, DD48*DE48^1.852,-DD48*ABS(DE48)^1.852),
IF(DE48>0, DD48*CZ48^1.852, -DD48*CZ48^1.852)) |
| Ligne 48 | Col 111 | DG48 | `=1.852*DD48*ABS(DE48)^(1.852-1)` | =1.852*DD48*ABS(DE48)^(1.852-1) |
| Ligne 48 | Col 112 | DH48 | `=DE48+CZ82` | =DE48+CZ82 |
| Ligne 49 | Col 4 | D49 | `=DIST_PHASE_1_v2!E38` | =DIST_PHASE_1_v2!E38 |
| Ligne 49 | Col 5 | E49 | `=DIST_PHASE_1_v2!G38` | =DIST_PHASE_1_v2!G38 |
| Ligne 49 | Col 6 | F49 | `=DIST_PHASE_1_v2!L38` | =DIST_PHASE_1_v2!L38 |
| Ligne 49 | Col 7 | G49 | `=DIST_PHASE_1_v2!M38` | =DIST_PHASE_1_v2!M38 |
| Ligne 49 | Col 8 | H49 | `=DIST_PHASE_1_v2!N38` | =DIST_PHASE_1_v2!N38 |
| Ligne 49 | Col 9 | I49 | `= (10.679 * H49) / ((F49/1000)^4.871 * G49^1.852)` | = (10.679 * H49) / ((F49/1000)^4.871 * G49^1.852) |
| Ligne 49 | Col 10 | J49 | `=IF(C49="positif",E49,IF(C49="negatif",-E49,""))` | =IF(C49="positif",E49,IF(C49="negatif",-E49,"")) |
| Ligne 49 | Col 11 | K49 | `=IF(J49>0,I49*E49^1.852,-I49*E49^1.852)` | =IF(J49>0,I49*E49^1.852,-I49*E49^1.852) |
| Ligne 49 | Col 12 | L49 | `=1.852*I49*ABS(E49)^(1.852-1)` | =1.852*I49*ABS(E49)^(1.852-1) |
| Ligne 49 | Col 13 | M49 | `=J49+$D$93` | =J49+$D$93 |
| Ligne 49 | Col 16 | P49 | `=IFERROR(MATCH(S49,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S49,$D$22:$D$91,0),0) |
| Ligne 49 | Col 18 | R49 | `=DIST_PHASE_1_v2!Q38` | =DIST_PHASE_1_v2!Q38 |
| Ligne 49 | Col 19 | S49 | `=DIST_PHASE_1_v2!R38` | =DIST_PHASE_1_v2!R38 |
| Ligne 49 | Col 20 | T49 | `=DIST_PHASE_1_v2!T38` | =DIST_PHASE_1_v2!T38 |
| Ligne 49 | Col 21 | U49 | `=DIST_PHASE_1_v2!Y38` | =DIST_PHASE_1_v2!Y38 |
| Ligne 49 | Col 23 | W49 | `=DIST_PHASE_1_v2!AA38` | =DIST_PHASE_1_v2!AA38 |
| Ligne 49 | Col 24 | X49 | `= (10.679 * W49) / ((U49/1000)^4.871 * V49^1.852)` | = (10.679 * W49) / ((U49/1000)^4.871 * V49^1.852) |
| Ligne 49 | Col 25 | Y49 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9943B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9943B0> |
| Ligne 49 | Col 26 | Z49 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F410>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94F410> |
| Ligne 49 | Col 27 | AA49 | `=IF(P49>0,
IF(R49="positif",1,-1),
0)` | =IF(P49>0,
IF(R49="positif",1,-1),
0) |
| Ligne 49 | Col 28 | AB49 | `=X49*SIGN(Y49)*ABS(Y49)^1.852` | =X49*SIGN(Y49)*ABS(Y49)^1.852 |
| Ligne 49 | Col 29 | AC49 | `=1.852*X49*ABS(Y49)^(1.852-1)` | =1.852*X49*ABS(Y49)^(1.852-1) |
| Ligne 49 | Col 30 | AD49 | `=IF(P49>0,
Y49+($D$93*Z49)+(AA49*$S$93),
Y49+$S$93)` | =IF(P49>0,
Y49+($D$93*Z49)+(AA49*$S$93),
Y49+$S$93) |
| Ligne 49 | Col 32 | AF49 | `=ABS(AD49)-ABS(Y49)` | =ABS(AD49)-ABS(Y49) |
| Ligne 49 | Col 36 | AJ49 | `=IFERROR(MATCH(AM49,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM49,$S$22:$S$91,0),0) |
| Ligne 49 | Col 38 | AL49 | `=TRONCONS_V2!AI36` | =TRONCONS_V2!AI36 |
| Ligne 49 | Col 39 | AM49 | `=TRONCONS_V2!AE36` | =TRONCONS_V2!AE36 |
| Ligne 49 | Col 40 | AN49 | `=DIST_PHASE_1_v2!AG38` | =DIST_PHASE_1_v2!AG38 |
| Ligne 49 | Col 41 | AO49 | `=DIST_PHASE_1_v2!AL38` | =DIST_PHASE_1_v2!AL38 |
| Ligne 49 | Col 43 | AQ49 | `=TRONCONS_V2!AG36` | =TRONCONS_V2!AG36 |
| Ligne 49 | Col 44 | AR49 | `= (10.679 * AQ49) / ((AO49/1000)^4.871 * AP49^1.852)` | = (10.679 * AQ49) / ((AO49/1000)^4.871 * AP49^1.852) |
| Ligne 49 | Col 45 | AS49 | `=IF(AL49="positif",AN49,IF(AL49="negatif",-AN49,""))` | =IF(AL49="positif",AN49,IF(AL49="negatif",-AN49,"")) |
| Ligne 49 | Col 46 | AT49 | `=IF(AJ49>0,
IF(AS49>0, AR49*AS49^1.852,-AR49*ABS(AS49)^1.852),
IF(AS49>0, AR49*AN49^1.852, -AR49*AN49^1.852))` | =IF(AJ49>0,
IF(AS49>0, AR49*AS49^1.852,-AR49*ABS(AS49)^1.852),
IF(AS49>0, AR49*AN49^1.852, -AR49*AN49^1.852)) |
| Ligne 49 | Col 47 | AU49 | `=1.852*AR49*ABS(AS49)^(1.852-1)` | =1.852*AR49*ABS(AS49)^(1.852-1) |
| Ligne 49 | Col 48 | AV49 | `=AS49+$AN$60` | =AS49+$AN$60 |
| Ligne 49 | Col 52 | AZ49 | `=IFERROR(MATCH(BC49,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC49,$AM$22:$AM$57,0),0) |
| Ligne 49 | Col 54 | BB49 | `=DIST_PHASE_1_v2!AQ38` | =DIST_PHASE_1_v2!AQ38 |
| Ligne 49 | Col 55 | BC49 | `=DIST_PHASE_1_v2!AR38` | =DIST_PHASE_1_v2!AR38 |
| Ligne 49 | Col 56 | BD49 | `=DIST_PHASE_1_v2!AT38` | =DIST_PHASE_1_v2!AT38 |
| Ligne 49 | Col 57 | BE49 | `=DIST_PHASE_1_v2!AY38` | =DIST_PHASE_1_v2!AY38 |
| Ligne 49 | Col 58 | BF49 | `=DIST_PHASE_1_v2!AZ38` | =DIST_PHASE_1_v2!AZ38 |
| Ligne 49 | Col 59 | BG49 | `=DIST_PHASE_1_v2!BA38` | =DIST_PHASE_1_v2!BA38 |
| Ligne 49 | Col 60 | BH49 | `= (10.679 * BG49) / ((BE49/1000)^4.871 * BF49^1.852)` | = (10.679 * BG49) / ((BE49/1000)^4.871 * BF49^1.852) |
| Ligne 49 | Col 61 | BI49 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9945F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9945F0> |
| Ligne 49 | Col 62 | BJ49 | `=IF(AZ49>0,
IF(BI49>0, BH49*BI49^1.852,-BH49*ABS(BI49)^1.852),
IF(BI49>0, BH49*BD49^1.852, -BH49*BD49^1.852))` | =IF(AZ49>0,
IF(BI49>0, BH49*BI49^1.852,-BH49*ABS(BI49)^1.852),
IF(BI49>0, BH49*BD49^1.852, -BH49*BD49^1.852)) |
| Ligne 49 | Col 63 | BK49 | `=1.852*BH49*ABS(BI49)^(1.852-1)` | =1.852*BH49*ABS(BI49)^(1.852-1) |
| Ligne 49 | Col 64 | BL49 | `=BI49+$BD$75` | =BI49+$BD$75 |
| Ligne 49 | Col 68 | BP49 | `=IFERROR(MATCH(BS49,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS49,$BC$22:$BC$73,0),0) |
| Ligne 49 | Col 70 | BR49 | `=DIST_PHASE_1_v2!BF38` | =DIST_PHASE_1_v2!BF38 |
| Ligne 49 | Col 71 | BS49 | `=DIST_PHASE_1_v2!BG38` | =DIST_PHASE_1_v2!BG38 |
| Ligne 49 | Col 72 | BT49 | `=DIST_PHASE_1_v2!BI38` | =DIST_PHASE_1_v2!BI38 |
| Ligne 49 | Col 73 | BU49 | `=DIST_PHASE_1_v2!BN38` | =DIST_PHASE_1_v2!BN38 |
| Ligne 49 | Col 74 | BV49 | `=DIST_PHASE_1_v2!BO38` | =DIST_PHASE_1_v2!BO38 |
| Ligne 49 | Col 75 | BW49 | `=DIST_PHASE_1_v2!BP38` | =DIST_PHASE_1_v2!BP38 |
| Ligne 49 | Col 76 | BX49 | `= (10.679 * BW49) / ((BU49/1000)^4.871 * BV49^1.852)` | = (10.679 * BW49) / ((BU49/1000)^4.871 * BV49^1.852) |
| Ligne 49 | Col 77 | BY49 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9946B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9946B0> |
| Ligne 49 | Col 78 | BZ49 | `=IF(BP49>0,
IF(BY49>0, BX49*BY49^1.852,-BX49*ABS(BY49)^1.852),
IF(BY49>0, BX49*BT49^1.852, -BX49*BT49^1.852))` | =IF(BP49>0,
IF(BY49>0, BX49*BY49^1.852,-BX49*ABS(BY49)^1.852),
IF(BY49>0, BX49*BT49^1.852, -BX49*BT49^1.852)) |
| Ligne 49 | Col 79 | CA49 | `=1.852*BX49*ABS(BY49)^(1.852-1)` | =1.852*BX49*ABS(BY49)^(1.852-1) |
| Ligne 49 | Col 80 | CB49 | `=BY49+$BT$64` | =BY49+$BT$64 |
| Ligne 49 | Col 84 | CF49 | `=IFERROR(MATCH(CI49,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI49,$BS$22:$BS$62,0),0) |
| Ligne 49 | Col 86 | CH49 | `=DIST_PHASE_1_v2!BS38` | =DIST_PHASE_1_v2!BS38 |
| Ligne 49 | Col 87 | CI49 | `=DIST_PHASE_1_v2!BT38` | =DIST_PHASE_1_v2!BT38 |
| Ligne 49 | Col 88 | CJ49 | `=DIST_PHASE_1_v2!BV38` | =DIST_PHASE_1_v2!BV38 |
| Ligne 49 | Col 89 | CK49 | `=DIST_PHASE_1_v2!CA38` | =DIST_PHASE_1_v2!CA38 |
| Ligne 49 | Col 91 | CM49 | `=DIST_PHASE_1_v2!CC38` | =DIST_PHASE_1_v2!CC38 |
| Ligne 49 | Col 92 | CN49 | `= (10.679 * CM49) / ((CK49/1000)^4.871 * CL49^1.852)` | = (10.679 * CM49) / ((CK49/1000)^4.871 * CL49^1.852) |
| Ligne 49 | Col 93 | CO49 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994770>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994770> |
| Ligne 49 | Col 94 | CP49 | `=IF(CF49>0,
IF(CO49>0, CN49*CO49^1.852,-CN49*ABS(CO49)^1.852),
IF(CO49>0, CN49*CJ49^1.852, -CN49*CJ49^1.852))` | =IF(CF49>0,
IF(CO49>0, CN49*CO49^1.852,-CN49*ABS(CO49)^1.852),
IF(CO49>0, CN49*CJ49^1.852, -CN49*CJ49^1.852)) |
| Ligne 49 | Col 95 | CQ49 | `=1.852*CN49*ABS(CO49)^(1.852-1)` | =1.852*CN49*ABS(CO49)^(1.852-1) |
| Ligne 49 | Col 96 | CR49 | `=CO49+$CJ$71` | =CO49+$CJ$71 |
| Ligne 49 | Col 100 | CV49 | `=IFERROR(MATCH(CY49,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY49,$CI$22:$CI$69,0),0) |
| Ligne 49 | Col 102 | CX49 | `=DIST_PHASE_1_v2!CF38` | =DIST_PHASE_1_v2!CF38 |
| Ligne 49 | Col 103 | CY49 | `=DIST_PHASE_1_v2!CG38` | =DIST_PHASE_1_v2!CG38 |
| Ligne 49 | Col 104 | CZ49 | `=DIST_PHASE_1_v2!CI38` | =DIST_PHASE_1_v2!CI38 |
| Ligne 49 | Col 105 | DA49 | `=DIST_PHASE_1_v2!CN38` | =DIST_PHASE_1_v2!CN38 |
| Ligne 49 | Col 106 | DB49 | `=DIST_PHASE_1_v2!CO38` | =DIST_PHASE_1_v2!CO38 |
| Ligne 49 | Col 107 | DC49 | `=DIST_PHASE_1_v2!CP38` | =DIST_PHASE_1_v2!CP38 |
| Ligne 49 | Col 108 | DD49 | `= (10.679 * DC49) / ((DA49/1000)^4.871 * DB49^1.852)` | = (10.679 * DC49) / ((DA49/1000)^4.871 * DB49^1.852) |
| Ligne 49 | Col 109 | DE49 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994830>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994830> |
| Ligne 49 | Col 110 | DF49 | `=IF(CV49>0,
IF(DE49>0, DD49*DE49^1.852,-DD49*ABS(DE49)^1.852),
IF(DE49>0, DD49*CZ49^1.852, -DD49*CZ49^1.852))` | =IF(CV49>0,
IF(DE49>0, DD49*DE49^1.852,-DD49*ABS(DE49)^1.852),
IF(DE49>0, DD49*CZ49^1.852, -DD49*CZ49^1.852)) |
| Ligne 49 | Col 111 | DG49 | `=1.852*DD49*ABS(DE49)^(1.852-1)` | =1.852*DD49*ABS(DE49)^(1.852-1) |
| Ligne 49 | Col 112 | DH49 | `=DE49+CZ83` | =DE49+CZ83 |
| Ligne 50 | Col 4 | D50 | `=DIST_PHASE_1_v2!E39` | =DIST_PHASE_1_v2!E39 |
| Ligne 50 | Col 5 | E50 | `=DIST_PHASE_1_v2!G39` | =DIST_PHASE_1_v2!G39 |
| Ligne 50 | Col 6 | F50 | `=DIST_PHASE_1_v2!L39` | =DIST_PHASE_1_v2!L39 |
| Ligne 50 | Col 7 | G50 | `=DIST_PHASE_1_v2!M39` | =DIST_PHASE_1_v2!M39 |
| Ligne 50 | Col 8 | H50 | `=DIST_PHASE_1_v2!N39` | =DIST_PHASE_1_v2!N39 |
| Ligne 50 | Col 9 | I50 | `= (10.679 * H50) / ((F50/1000)^4.871 * G50^1.852)` | = (10.679 * H50) / ((F50/1000)^4.871 * G50^1.852) |
| Ligne 50 | Col 10 | J50 | `=IF(C50="positif",E50,IF(C50="negatif",-E50,""))` | =IF(C50="positif",E50,IF(C50="negatif",-E50,"")) |
| Ligne 50 | Col 11 | K50 | `=IF(J50>0,I50*E50^1.852,-I50*E50^1.852)` | =IF(J50>0,I50*E50^1.852,-I50*E50^1.852) |
| Ligne 50 | Col 12 | L50 | `=1.852*I50*ABS(E50)^(1.852-1)` | =1.852*I50*ABS(E50)^(1.852-1) |
| Ligne 50 | Col 13 | M50 | `=J50+$D$93` | =J50+$D$93 |
| Ligne 50 | Col 16 | P50 | `=IFERROR(MATCH(S50,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S50,$D$22:$D$91,0),0) |
| Ligne 50 | Col 18 | R50 | `=DIST_PHASE_1_v2!Q39` | =DIST_PHASE_1_v2!Q39 |
| Ligne 50 | Col 19 | S50 | `=DIST_PHASE_1_v2!R39` | =DIST_PHASE_1_v2!R39 |
| Ligne 50 | Col 20 | T50 | `=DIST_PHASE_1_v2!T39` | =DIST_PHASE_1_v2!T39 |
| Ligne 50 | Col 21 | U50 | `=DIST_PHASE_1_v2!Y39` | =DIST_PHASE_1_v2!Y39 |
| Ligne 50 | Col 23 | W50 | `=DIST_PHASE_1_v2!AA39` | =DIST_PHASE_1_v2!AA39 |
| Ligne 50 | Col 24 | X50 | `= (10.679 * W50) / ((U50/1000)^4.871 * V50^1.852)` | = (10.679 * W50) / ((U50/1000)^4.871 * V50^1.852) |
| Ligne 50 | Col 25 | Y50 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994950>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994950> |
| Ligne 50 | Col 26 | Z50 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FB90>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD94FB90> |
| Ligne 50 | Col 27 | AA50 | `=IF(P50>0,
IF(R50="positif",1,-1),
0)` | =IF(P50>0,
IF(R50="positif",1,-1),
0) |
| Ligne 50 | Col 28 | AB50 | `=X50*SIGN(Y50)*ABS(Y50)^1.852` | =X50*SIGN(Y50)*ABS(Y50)^1.852 |
| Ligne 50 | Col 29 | AC50 | `=1.852*X50*ABS(Y50)^(1.852-1)` | =1.852*X50*ABS(Y50)^(1.852-1) |
| Ligne 50 | Col 30 | AD50 | `=IF(P50>0,
Y50+($D$93*Z50)+(AA50*$S$93),
Y50+$S$93)` | =IF(P50>0,
Y50+($D$93*Z50)+(AA50*$S$93),
Y50+$S$93) |
| Ligne 50 | Col 32 | AF50 | `=ABS(AD50)-ABS(Y50)` | =ABS(AD50)-ABS(Y50) |
| Ligne 50 | Col 36 | AJ50 | `=IFERROR(MATCH(AM50,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM50,$S$22:$S$91,0),0) |
| Ligne 50 | Col 38 | AL50 | `=TRONCONS_V2!AI37` | =TRONCONS_V2!AI37 |
| Ligne 50 | Col 39 | AM50 | `=TRONCONS_V2!AE37` | =TRONCONS_V2!AE37 |
| Ligne 50 | Col 40 | AN50 | `=DIST_PHASE_1_v2!AG39` | =DIST_PHASE_1_v2!AG39 |
| Ligne 50 | Col 41 | AO50 | `=DIST_PHASE_1_v2!AL39` | =DIST_PHASE_1_v2!AL39 |
| Ligne 50 | Col 43 | AQ50 | `=TRONCONS_V2!AG37` | =TRONCONS_V2!AG37 |
| Ligne 50 | Col 44 | AR50 | `= (10.679 * AQ50) / ((AO50/1000)^4.871 * AP50^1.852)` | = (10.679 * AQ50) / ((AO50/1000)^4.871 * AP50^1.852) |
| Ligne 50 | Col 45 | AS50 | `=IF(AL50="positif",AN50,IF(AL50="negatif",-AN50,""))` | =IF(AL50="positif",AN50,IF(AL50="negatif",-AN50,"")) |
| Ligne 50 | Col 46 | AT50 | `=IF(AJ50>0,
        IF(AS50>0, AR50*AS50^1.852,-AR50*ABS(AS50)^1.852),
        IF(AS50>0, AR50*AN50^1.852, -AR50*AN50^1.852))` | =IF(AJ50>0,
        IF(AS50>0, AR50*AS50^1.852,-AR50*ABS(AS50)^1.852),
        IF(AS50>0, AR50*AN50^1.852, -AR50*AN50^1.852)) |
| Ligne 50 | Col 47 | AU50 | `=1.852*AR50*ABS(AS50)^(1.852-1)` | =1.852*AR50*ABS(AS50)^(1.852-1) |
| Ligne 50 | Col 48 | AV50 | `=AS50+$AN$60` | =AS50+$AN$60 |
| Ligne 50 | Col 52 | AZ50 | `=IFERROR(MATCH(BC50,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC50,$AM$22:$AM$57,0),0) |
| Ligne 50 | Col 54 | BB50 | `=DIST_PHASE_1_v2!AQ39` | =DIST_PHASE_1_v2!AQ39 |
| Ligne 50 | Col 55 | BC50 | `=DIST_PHASE_1_v2!AR39` | =DIST_PHASE_1_v2!AR39 |
| Ligne 50 | Col 56 | BD50 | `=DIST_PHASE_1_v2!AT39` | =DIST_PHASE_1_v2!AT39 |
| Ligne 50 | Col 57 | BE50 | `=DIST_PHASE_1_v2!AY39` | =DIST_PHASE_1_v2!AY39 |
| Ligne 50 | Col 58 | BF50 | `=DIST_PHASE_1_v2!AZ39` | =DIST_PHASE_1_v2!AZ39 |
| Ligne 50 | Col 59 | BG50 | `=DIST_PHASE_1_v2!BA39` | =DIST_PHASE_1_v2!BA39 |
| Ligne 50 | Col 60 | BH50 | `= (10.679 * BG50) / ((BE50/1000)^4.871 * BF50^1.852)` | = (10.679 * BG50) / ((BE50/1000)^4.871 * BF50^1.852) |
| Ligne 50 | Col 61 | BI50 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994B30>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994B30> |
| Ligne 50 | Col 62 | BJ50 | `=IF(AZ50>0,
IF(BI50>0, BH50*BI50^1.852,-BH50*ABS(BI50)^1.852),
IF(BI50>0, BH50*BD50^1.852, -BH50*BD50^1.852))` | =IF(AZ50>0,
IF(BI50>0, BH50*BI50^1.852,-BH50*ABS(BI50)^1.852),
IF(BI50>0, BH50*BD50^1.852, -BH50*BD50^1.852)) |
| Ligne 50 | Col 63 | BK50 | `=1.852*BH50*ABS(BI50)^(1.852-1)` | =1.852*BH50*ABS(BI50)^(1.852-1) |
| Ligne 50 | Col 64 | BL50 | `=BI50+$BD$75` | =BI50+$BD$75 |
| Ligne 50 | Col 68 | BP50 | `=IFERROR(MATCH(BS50,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS50,$BC$22:$BC$73,0),0) |
| Ligne 50 | Col 70 | BR50 | `=DIST_PHASE_1_v2!BF39` | =DIST_PHASE_1_v2!BF39 |
| Ligne 50 | Col 71 | BS50 | `=DIST_PHASE_1_v2!BG39` | =DIST_PHASE_1_v2!BG39 |
| Ligne 50 | Col 72 | BT50 | `=DIST_PHASE_1_v2!BI39` | =DIST_PHASE_1_v2!BI39 |
| Ligne 50 | Col 73 | BU50 | `=DIST_PHASE_1_v2!BN39` | =DIST_PHASE_1_v2!BN39 |
| Ligne 50 | Col 74 | BV50 | `=DIST_PHASE_1_v2!BO39` | =DIST_PHASE_1_v2!BO39 |
| Ligne 50 | Col 75 | BW50 | `=DIST_PHASE_1_v2!BP39` | =DIST_PHASE_1_v2!BP39 |
| Ligne 50 | Col 76 | BX50 | `= (10.679 * BW50) / ((BU50/1000)^4.871 * BV50^1.852)` | = (10.679 * BW50) / ((BU50/1000)^4.871 * BV50^1.852) |
| Ligne 50 | Col 77 | BY50 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994BF0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994BF0> |
| Ligne 50 | Col 78 | BZ50 | `=IF(BP50>0,
IF(BY50>0, BX50*BY50^1.852,-BX50*ABS(BY50)^1.852),
IF(BY50>0, BX50*BT50^1.852, -BX50*BT50^1.852))` | =IF(BP50>0,
IF(BY50>0, BX50*BY50^1.852,-BX50*ABS(BY50)^1.852),
IF(BY50>0, BX50*BT50^1.852, -BX50*BT50^1.852)) |
| Ligne 50 | Col 79 | CA50 | `=1.852*BX50*ABS(BY50)^(1.852-1)` | =1.852*BX50*ABS(BY50)^(1.852-1) |
| Ligne 50 | Col 80 | CB50 | `=BY50+$BT$64` | =BY50+$BT$64 |
| Ligne 50 | Col 84 | CF50 | `=IFERROR(MATCH(CI50,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI50,$BS$22:$BS$62,0),0) |
| Ligne 50 | Col 86 | CH50 | `=DIST_PHASE_1_v2!BS39` | =DIST_PHASE_1_v2!BS39 |
| Ligne 50 | Col 87 | CI50 | `=DIST_PHASE_1_v2!BT39` | =DIST_PHASE_1_v2!BT39 |
| Ligne 50 | Col 88 | CJ50 | `=DIST_PHASE_1_v2!BV39` | =DIST_PHASE_1_v2!BV39 |
| Ligne 50 | Col 89 | CK50 | `=DIST_PHASE_1_v2!CA39` | =DIST_PHASE_1_v2!CA39 |
| Ligne 50 | Col 91 | CM50 | `=DIST_PHASE_1_v2!CC39` | =DIST_PHASE_1_v2!CC39 |
| Ligne 50 | Col 92 | CN50 | `= (10.679 * CM50) / ((CK50/1000)^4.871 * CL50^1.852)` | = (10.679 * CM50) / ((CK50/1000)^4.871 * CL50^1.852) |
| Ligne 50 | Col 93 | CO50 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994CB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994CB0> |
| Ligne 50 | Col 94 | CP50 | `=IF(CF50>0,
IF(CO50>0, CN50*CO50^1.852,-CN50*ABS(CO50)^1.852),
IF(CO50>0, CN50*CJ50^1.852, -CN50*CJ50^1.852))` | =IF(CF50>0,
IF(CO50>0, CN50*CO50^1.852,-CN50*ABS(CO50)^1.852),
IF(CO50>0, CN50*CJ50^1.852, -CN50*CJ50^1.852)) |
| Ligne 50 | Col 95 | CQ50 | `=1.852*CN50*ABS(CO50)^(1.852-1)` | =1.852*CN50*ABS(CO50)^(1.852-1) |
| Ligne 50 | Col 96 | CR50 | `=CO50+$CJ$71` | =CO50+$CJ$71 |
| Ligne 50 | Col 100 | CV50 | `=IFERROR(MATCH(CY50,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY50,$CI$22:$CI$69,0),0) |
| Ligne 50 | Col 102 | CX50 | `=DIST_PHASE_1_v2!CF39` | =DIST_PHASE_1_v2!CF39 |
| Ligne 50 | Col 103 | CY50 | `=DIST_PHASE_1_v2!CG39` | =DIST_PHASE_1_v2!CG39 |
| Ligne 50 | Col 104 | CZ50 | `=DIST_PHASE_1_v2!CI39` | =DIST_PHASE_1_v2!CI39 |
| Ligne 50 | Col 105 | DA50 | `=DIST_PHASE_1_v2!CN39` | =DIST_PHASE_1_v2!CN39 |
| Ligne 50 | Col 106 | DB50 | `=DIST_PHASE_1_v2!CO39` | =DIST_PHASE_1_v2!CO39 |
| Ligne 50 | Col 107 | DC50 | `=DIST_PHASE_1_v2!CP39` | =DIST_PHASE_1_v2!CP39 |
| Ligne 50 | Col 108 | DD50 | `= (10.679 * DC50) / ((DA50/1000)^4.871 * DB50^1.852)` | = (10.679 * DC50) / ((DA50/1000)^4.871 * DB50^1.852) |
| Ligne 50 | Col 109 | DE50 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994D70>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994D70> |
| Ligne 50 | Col 110 | DF50 | `=IF(CV50>0,
IF(DE50>0, DD50*DE50^1.852,-DD50*ABS(DE50)^1.852),
IF(DE50>0, DD50*CZ50^1.852, -DD50*CZ50^1.852))` | =IF(CV50>0,
IF(DE50>0, DD50*DE50^1.852,-DD50*ABS(DE50)^1.852),
IF(DE50>0, DD50*CZ50^1.852, -DD50*CZ50^1.852)) |
| Ligne 50 | Col 111 | DG50 | `=1.852*DD50*ABS(DE50)^(1.852-1)` | =1.852*DD50*ABS(DE50)^(1.852-1) |
| Ligne 50 | Col 112 | DH50 | `=DE50+CZ84` | =DE50+CZ84 |
| Ligne 51 | Col 4 | D51 | `=DIST_PHASE_1_v2!E40` | =DIST_PHASE_1_v2!E40 |
| Ligne 51 | Col 5 | E51 | `=DIST_PHASE_1_v2!G40` | =DIST_PHASE_1_v2!G40 |
| Ligne 51 | Col 6 | F51 | `=DIST_PHASE_1_v2!L40` | =DIST_PHASE_1_v2!L40 |
| Ligne 51 | Col 7 | G51 | `=DIST_PHASE_1_v2!M40` | =DIST_PHASE_1_v2!M40 |
| Ligne 51 | Col 8 | H51 | `=DIST_PHASE_1_v2!N40` | =DIST_PHASE_1_v2!N40 |
| Ligne 51 | Col 9 | I51 | `= (10.679 * H51) / ((F51/1000)^4.871 * G51^1.852)` | = (10.679 * H51) / ((F51/1000)^4.871 * G51^1.852) |
| Ligne 51 | Col 10 | J51 | `=IF(C51="positif",E51,IF(C51="negatif",-E51,""))` | =IF(C51="positif",E51,IF(C51="negatif",-E51,"")) |
| Ligne 51 | Col 11 | K51 | `=IF(J51>0,I51*E51^1.852,-I51*E51^1.852)` | =IF(J51>0,I51*E51^1.852,-I51*E51^1.852) |
| Ligne 51 | Col 12 | L51 | `=1.852*I51*ABS(E51)^(1.852-1)` | =1.852*I51*ABS(E51)^(1.852-1) |
| Ligne 51 | Col 13 | M51 | `=J51+$D$93` | =J51+$D$93 |
| Ligne 51 | Col 16 | P51 | `=IFERROR(MATCH(S51,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S51,$D$22:$D$91,0),0) |
| Ligne 51 | Col 18 | R51 | `=DIST_PHASE_1_v2!Q40` | =DIST_PHASE_1_v2!Q40 |
| Ligne 51 | Col 19 | S51 | `=DIST_PHASE_1_v2!R40` | =DIST_PHASE_1_v2!R40 |
| Ligne 51 | Col 20 | T51 | `=DIST_PHASE_1_v2!T40` | =DIST_PHASE_1_v2!T40 |
| Ligne 51 | Col 21 | U51 | `=DIST_PHASE_1_v2!Y40` | =DIST_PHASE_1_v2!Y40 |
| Ligne 51 | Col 23 | W51 | `=DIST_PHASE_1_v2!AA40` | =DIST_PHASE_1_v2!AA40 |
| Ligne 51 | Col 24 | X51 | `= (10.679 * W51) / ((U51/1000)^4.871 * V51^1.852)` | = (10.679 * W51) / ((U51/1000)^4.871 * V51^1.852) |
| Ligne 51 | Col 25 | Y51 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994E90>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994E90> |
| Ligne 51 | Col 26 | Z51 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994110>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994110> |
| Ligne 51 | Col 27 | AA51 | `=IF(P51>0,
IF(R51="positif",1,-1),
0)` | =IF(P51>0,
IF(R51="positif",1,-1),
0) |
| Ligne 51 | Col 28 | AB51 | `=X51*SIGN(Y51)*ABS(Y51)^1.852` | =X51*SIGN(Y51)*ABS(Y51)^1.852 |
| Ligne 51 | Col 29 | AC51 | `=1.852*X51*ABS(Y51)^(1.852-1)` | =1.852*X51*ABS(Y51)^(1.852-1) |
| Ligne 51 | Col 30 | AD51 | `=IF(P51>0,
Y51+($D$93*Z51)+(AA51*$S$93),
Y51+$S$93)` | =IF(P51>0,
Y51+($D$93*Z51)+(AA51*$S$93),
Y51+$S$93) |
| Ligne 51 | Col 32 | AF51 | `=ABS(AD51)-ABS(Y51)` | =ABS(AD51)-ABS(Y51) |
| Ligne 51 | Col 36 | AJ51 | `=IFERROR(MATCH(AM51,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM51,$S$22:$S$91,0),0) |
| Ligne 51 | Col 38 | AL51 | `=TRONCONS_V2!AI38` | =TRONCONS_V2!AI38 |
| Ligne 51 | Col 39 | AM51 | `=TRONCONS_V2!AE38` | =TRONCONS_V2!AE38 |
| Ligne 51 | Col 40 | AN51 | `=DIST_PHASE_1_v2!AG40` | =DIST_PHASE_1_v2!AG40 |
| Ligne 51 | Col 41 | AO51 | `=DIST_PHASE_1_v2!AL40` | =DIST_PHASE_1_v2!AL40 |
| Ligne 51 | Col 43 | AQ51 | `=TRONCONS_V2!AG38` | =TRONCONS_V2!AG38 |
| Ligne 51 | Col 44 | AR51 | `= (10.679 * AQ51) / ((AO51/1000)^4.871 * AP51^1.852)` | = (10.679 * AQ51) / ((AO51/1000)^4.871 * AP51^1.852) |
| Ligne 51 | Col 45 | AS51 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995070>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995070> |
| Ligne 51 | Col 46 | AT51 | `=IF(AJ51>0,
        IF(AS51>0, AR51*AS51^1.852,-AR51*ABS(AS51)^1.852),
        IF(AS51>0, AR51*AN51^1.852, -AR51*AN51^1.852))` | =IF(AJ51>0,
        IF(AS51>0, AR51*AS51^1.852,-AR51*ABS(AS51)^1.852),
        IF(AS51>0, AR51*AN51^1.852, -AR51*AN51^1.852)) |
| Ligne 51 | Col 47 | AU51 | `=1.852*AR51*ABS(AS51)^(1.852-1)` | =1.852*AR51*ABS(AS51)^(1.852-1) |
| Ligne 51 | Col 48 | AV51 | `=AS51+$AN$60` | =AS51+$AN$60 |
| Ligne 51 | Col 52 | AZ51 | `=IFERROR(MATCH(BC51,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC51,$AM$22:$AM$57,0),0) |
| Ligne 51 | Col 54 | BB51 | `=DIST_PHASE_1_v2!AQ40` | =DIST_PHASE_1_v2!AQ40 |
| Ligne 51 | Col 55 | BC51 | `=DIST_PHASE_1_v2!AR40` | =DIST_PHASE_1_v2!AR40 |
| Ligne 51 | Col 56 | BD51 | `=DIST_PHASE_1_v2!AT40` | =DIST_PHASE_1_v2!AT40 |
| Ligne 51 | Col 57 | BE51 | `=DIST_PHASE_1_v2!AY40` | =DIST_PHASE_1_v2!AY40 |
| Ligne 51 | Col 58 | BF51 | `=DIST_PHASE_1_v2!AZ40` | =DIST_PHASE_1_v2!AZ40 |
| Ligne 51 | Col 59 | BG51 | `=DIST_PHASE_1_v2!BA40` | =DIST_PHASE_1_v2!BA40 |
| Ligne 51 | Col 60 | BH51 | `= (10.679 * BG51) / ((BE51/1000)^4.871 * BF51^1.852)` | = (10.679 * BG51) / ((BE51/1000)^4.871 * BF51^1.852) |
| Ligne 51 | Col 61 | BI51 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9950D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9950D0> |
| Ligne 51 | Col 62 | BJ51 | `=IF(AZ51>0,
IF(BI51>0, BH51*BI51^1.852,-BH51*ABS(BI51)^1.852),
IF(BI51>0, BH51*BD51^1.852, -BH51*BD51^1.852))` | =IF(AZ51>0,
IF(BI51>0, BH51*BI51^1.852,-BH51*ABS(BI51)^1.852),
IF(BI51>0, BH51*BD51^1.852, -BH51*BD51^1.852)) |
| Ligne 51 | Col 63 | BK51 | `=1.852*BH51*ABS(BI51)^(1.852-1)` | =1.852*BH51*ABS(BI51)^(1.852-1) |
| Ligne 51 | Col 64 | BL51 | `=BI51+$BD$75` | =BI51+$BD$75 |
| Ligne 51 | Col 68 | BP51 | `=IFERROR(MATCH(BS51,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS51,$BC$22:$BC$73,0),0) |
| Ligne 51 | Col 70 | BR51 | `=DIST_PHASE_1_v2!BF40` | =DIST_PHASE_1_v2!BF40 |
| Ligne 51 | Col 71 | BS51 | `=DIST_PHASE_1_v2!BG40` | =DIST_PHASE_1_v2!BG40 |
| Ligne 51 | Col 72 | BT51 | `=DIST_PHASE_1_v2!BI40` | =DIST_PHASE_1_v2!BI40 |
| Ligne 51 | Col 73 | BU51 | `=DIST_PHASE_1_v2!BN40` | =DIST_PHASE_1_v2!BN40 |
| Ligne 51 | Col 74 | BV51 | `=DIST_PHASE_1_v2!BO40` | =DIST_PHASE_1_v2!BO40 |
| Ligne 51 | Col 75 | BW51 | `=DIST_PHASE_1_v2!BP40` | =DIST_PHASE_1_v2!BP40 |
| Ligne 51 | Col 76 | BX51 | `= (10.679 * BW51) / ((BU51/1000)^4.871 * BV51^1.852)` | = (10.679 * BW51) / ((BU51/1000)^4.871 * BV51^1.852) |
| Ligne 51 | Col 77 | BY51 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995190>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995190> |
| Ligne 51 | Col 78 | BZ51 | `=IF(BP51>0,
IF(BY51>0, BX51*BY51^1.852,-BX51*ABS(BY51)^1.852),
IF(BY51>0, BX51*BT51^1.852, -BX51*BT51^1.852))` | =IF(BP51>0,
IF(BY51>0, BX51*BY51^1.852,-BX51*ABS(BY51)^1.852),
IF(BY51>0, BX51*BT51^1.852, -BX51*BT51^1.852)) |
| Ligne 51 | Col 79 | CA51 | `=1.852*BX51*ABS(BY51)^(1.852-1)` | =1.852*BX51*ABS(BY51)^(1.852-1) |
| Ligne 51 | Col 80 | CB51 | `=BY51+$BT$64` | =BY51+$BT$64 |
| Ligne 51 | Col 84 | CF51 | `=IFERROR(MATCH(CI51,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI51,$BS$22:$BS$62,0),0) |
| Ligne 51 | Col 86 | CH51 | `=DIST_PHASE_1_v2!BS40` | =DIST_PHASE_1_v2!BS40 |
| Ligne 51 | Col 87 | CI51 | `=DIST_PHASE_1_v2!BT40` | =DIST_PHASE_1_v2!BT40 |
| Ligne 51 | Col 88 | CJ51 | `=DIST_PHASE_1_v2!BV40` | =DIST_PHASE_1_v2!BV40 |
| Ligne 51 | Col 89 | CK51 | `=DIST_PHASE_1_v2!CA40` | =DIST_PHASE_1_v2!CA40 |
| Ligne 51 | Col 91 | CM51 | `=DIST_PHASE_1_v2!CC40` | =DIST_PHASE_1_v2!CC40 |
| Ligne 51 | Col 92 | CN51 | `= (10.679 * CM51) / ((CK51/1000)^4.871 * CL51^1.852)` | = (10.679 * CM51) / ((CK51/1000)^4.871 * CL51^1.852) |
| Ligne 51 | Col 93 | CO51 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995250>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995250> |
| Ligne 51 | Col 94 | CP51 | `=IF(CF51>0,
IF(CO51>0, CN51*CO51^1.852,-CN51*ABS(CO51)^1.852),
IF(CO51>0, CN51*CJ51^1.852, -CN51*CJ51^1.852))` | =IF(CF51>0,
IF(CO51>0, CN51*CO51^1.852,-CN51*ABS(CO51)^1.852),
IF(CO51>0, CN51*CJ51^1.852, -CN51*CJ51^1.852)) |
| Ligne 51 | Col 95 | CQ51 | `=1.852*CN51*ABS(CO51)^(1.852-1)` | =1.852*CN51*ABS(CO51)^(1.852-1) |
| Ligne 51 | Col 96 | CR51 | `=CO51+$CJ$71` | =CO51+$CJ$71 |
| Ligne 51 | Col 100 | CV51 | `=IFERROR(MATCH(CY51,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY51,$CI$22:$CI$69,0),0) |
| Ligne 51 | Col 102 | CX51 | `=DIST_PHASE_1_v2!CF40` | =DIST_PHASE_1_v2!CF40 |
| Ligne 51 | Col 103 | CY51 | `=DIST_PHASE_1_v2!CG40` | =DIST_PHASE_1_v2!CG40 |
| Ligne 51 | Col 104 | CZ51 | `=DIST_PHASE_1_v2!CI40` | =DIST_PHASE_1_v2!CI40 |
| Ligne 51 | Col 105 | DA51 | `=DIST_PHASE_1_v2!CN40` | =DIST_PHASE_1_v2!CN40 |
| Ligne 51 | Col 106 | DB51 | `=DIST_PHASE_1_v2!CO40` | =DIST_PHASE_1_v2!CO40 |
| Ligne 51 | Col 107 | DC51 | `=DIST_PHASE_1_v2!CP40` | =DIST_PHASE_1_v2!CP40 |
| Ligne 51 | Col 108 | DD51 | `= (10.679 * DC51) / ((DA51/1000)^4.871 * DB51^1.852)` | = (10.679 * DC51) / ((DA51/1000)^4.871 * DB51^1.852) |
| Ligne 51 | Col 109 | DE51 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995310>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995310> |
| Ligne 51 | Col 110 | DF51 | `=IF(CV51>0,
IF(DE51>0, DD51*DE51^1.852,-DD51*ABS(DE51)^1.852),
IF(DE51>0, DD51*CZ51^1.852, -DD51*CZ51^1.852))` | =IF(CV51>0,
IF(DE51>0, DD51*DE51^1.852,-DD51*ABS(DE51)^1.852),
IF(DE51>0, DD51*CZ51^1.852, -DD51*CZ51^1.852)) |
| Ligne 51 | Col 111 | DG51 | `=1.852*DD51*ABS(DE51)^(1.852-1)` | =1.852*DD51*ABS(DE51)^(1.852-1) |
| Ligne 51 | Col 112 | DH51 | `=DE51+CZ85` | =DE51+CZ85 |
| Ligne 52 | Col 4 | D52 | `=DIST_PHASE_1_v2!E41` | =DIST_PHASE_1_v2!E41 |
| Ligne 52 | Col 5 | E52 | `=DIST_PHASE_1_v2!G41` | =DIST_PHASE_1_v2!G41 |
| Ligne 52 | Col 6 | F52 | `=DIST_PHASE_1_v2!L41` | =DIST_PHASE_1_v2!L41 |
| Ligne 52 | Col 7 | G52 | `=DIST_PHASE_1_v2!M41` | =DIST_PHASE_1_v2!M41 |
| Ligne 52 | Col 8 | H52 | `=DIST_PHASE_1_v2!N41` | =DIST_PHASE_1_v2!N41 |
| Ligne 52 | Col 9 | I52 | `= (10.679 * H52) / ((F52/1000)^4.871 * G52^1.852)` | = (10.679 * H52) / ((F52/1000)^4.871 * G52^1.852) |
| Ligne 52 | Col 10 | J52 | `=IF(C52="positif",E52,IF(C52="negatif",-E52,""))` | =IF(C52="positif",E52,IF(C52="negatif",-E52,"")) |
| Ligne 52 | Col 11 | K52 | `=IF(J52>0,I52*E52^1.852,-I52*E52^1.852)` | =IF(J52>0,I52*E52^1.852,-I52*E52^1.852) |
| Ligne 52 | Col 12 | L52 | `=1.852*I52*ABS(E52)^(1.852-1)` | =1.852*I52*ABS(E52)^(1.852-1) |
| Ligne 52 | Col 13 | M52 | `=J52+$D$93` | =J52+$D$93 |
| Ligne 52 | Col 16 | P52 | `=IFERROR(MATCH(S52,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S52,$D$22:$D$91,0),0) |
| Ligne 52 | Col 18 | R52 | `=DIST_PHASE_1_v2!Q41` | =DIST_PHASE_1_v2!Q41 |
| Ligne 52 | Col 19 | S52 | `=DIST_PHASE_1_v2!R41` | =DIST_PHASE_1_v2!R41 |
| Ligne 52 | Col 20 | T52 | `=DIST_PHASE_1_v2!T41` | =DIST_PHASE_1_v2!T41 |
| Ligne 52 | Col 21 | U52 | `=DIST_PHASE_1_v2!Y41` | =DIST_PHASE_1_v2!Y41 |
| Ligne 52 | Col 23 | W52 | `=DIST_PHASE_1_v2!AA41` | =DIST_PHASE_1_v2!AA41 |
| Ligne 52 | Col 24 | X52 | `= (10.679 * W52) / ((U52/1000)^4.871 * V52^1.852)` | = (10.679 * W52) / ((U52/1000)^4.871 * V52^1.852) |
| Ligne 52 | Col 25 | Y52 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995610>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995610> |
| Ligne 52 | Col 26 | Z52 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9941D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9941D0> |
| Ligne 52 | Col 27 | AA52 | `=IF(P52>0,
IF(R52="positif",1,-1),
0)` | =IF(P52>0,
IF(R52="positif",1,-1),
0) |
| Ligne 52 | Col 28 | AB52 | `=X52*SIGN(Y52)*ABS(Y52)^1.852` | =X52*SIGN(Y52)*ABS(Y52)^1.852 |
| Ligne 52 | Col 29 | AC52 | `=1.852*X52*ABS(Y52)^(1.852-1)` | =1.852*X52*ABS(Y52)^(1.852-1) |
| Ligne 52 | Col 30 | AD52 | `=IF(P52>0,
Y52+($D$93*Z52)+(AA52*$S$93),
Y52+$S$93)` | =IF(P52>0,
Y52+($D$93*Z52)+(AA52*$S$93),
Y52+$S$93) |
| Ligne 52 | Col 32 | AF52 | `=ABS(AD52)-ABS(Y52)` | =ABS(AD52)-ABS(Y52) |
| Ligne 52 | Col 36 | AJ52 | `=IFERROR(MATCH(AM52,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM52,$S$22:$S$91,0),0) |
| Ligne 52 | Col 38 | AL52 | `=TRONCONS_V2!AI39` | =TRONCONS_V2!AI39 |
| Ligne 52 | Col 39 | AM52 | `=TRONCONS_V2!AE39` | =TRONCONS_V2!AE39 |
| Ligne 52 | Col 40 | AN52 | `=DIST_PHASE_1_v2!AG41` | =DIST_PHASE_1_v2!AG41 |
| Ligne 52 | Col 41 | AO52 | `=DIST_PHASE_1_v2!AL41` | =DIST_PHASE_1_v2!AL41 |
| Ligne 52 | Col 43 | AQ52 | `=TRONCONS_V2!AG39` | =TRONCONS_V2!AG39 |
| Ligne 52 | Col 44 | AR52 | `= (10.679 * AQ52) / ((AO52/1000)^4.871 * AP52^1.852)` | = (10.679 * AQ52) / ((AO52/1000)^4.871 * AP52^1.852) |
| Ligne 52 | Col 45 | AS52 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995730>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995730> |
| Ligne 52 | Col 46 | AT52 | `=IF(AJ52>0,
        IF(AS52>0, AR52*AS52^1.852,-AR52*ABS(AS52)^1.852),
        IF(AS52>0, AR52*AN52^1.852, -AR52*AN52^1.852))` | =IF(AJ52>0,
        IF(AS52>0, AR52*AS52^1.852,-AR52*ABS(AS52)^1.852),
        IF(AS52>0, AR52*AN52^1.852, -AR52*AN52^1.852)) |
| Ligne 52 | Col 47 | AU52 | `=1.852*AR52*ABS(AS52)^(1.852-1)` | =1.852*AR52*ABS(AS52)^(1.852-1) |
| Ligne 52 | Col 48 | AV52 | `=AS52+$AN$60` | =AS52+$AN$60 |
| Ligne 52 | Col 52 | AZ52 | `=IFERROR(MATCH(BC52,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC52,$AM$22:$AM$57,0),0) |
| Ligne 52 | Col 54 | BB52 | `=DIST_PHASE_1_v2!AQ41` | =DIST_PHASE_1_v2!AQ41 |
| Ligne 52 | Col 55 | BC52 | `=DIST_PHASE_1_v2!AR41` | =DIST_PHASE_1_v2!AR41 |
| Ligne 52 | Col 56 | BD52 | `=DIST_PHASE_1_v2!AT41` | =DIST_PHASE_1_v2!AT41 |
| Ligne 52 | Col 57 | BE52 | `=DIST_PHASE_1_v2!AY41` | =DIST_PHASE_1_v2!AY41 |
| Ligne 52 | Col 58 | BF52 | `=DIST_PHASE_1_v2!AZ41` | =DIST_PHASE_1_v2!AZ41 |
| Ligne 52 | Col 59 | BG52 | `=DIST_PHASE_1_v2!BA41` | =DIST_PHASE_1_v2!BA41 |
| Ligne 52 | Col 60 | BH52 | `= (10.679 * BG52) / ((BE52/1000)^4.871 * BF52^1.852)` | = (10.679 * BG52) / ((BE52/1000)^4.871 * BF52^1.852) |
| Ligne 52 | Col 61 | BI52 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995790>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995790> |
| Ligne 52 | Col 62 | BJ52 | `=IF(AZ52>0,
IF(BI52>0, BH52*BI52^1.852,-BH52*ABS(BI52)^1.852),
IF(BI52>0, BH52*BD52^1.852, -BH52*BD52^1.852))` | =IF(AZ52>0,
IF(BI52>0, BH52*BI52^1.852,-BH52*ABS(BI52)^1.852),
IF(BI52>0, BH52*BD52^1.852, -BH52*BD52^1.852)) |
| Ligne 52 | Col 63 | BK52 | `=1.852*BH52*ABS(BI52)^(1.852-1)` | =1.852*BH52*ABS(BI52)^(1.852-1) |
| Ligne 52 | Col 64 | BL52 | `=BI52+$BD$75` | =BI52+$BD$75 |
| Ligne 52 | Col 68 | BP52 | `=IFERROR(MATCH(BS52,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS52,$BC$22:$BC$73,0),0) |
| Ligne 52 | Col 70 | BR52 | `=DIST_PHASE_1_v2!BF41` | =DIST_PHASE_1_v2!BF41 |
| Ligne 52 | Col 71 | BS52 | `=DIST_PHASE_1_v2!BG41` | =DIST_PHASE_1_v2!BG41 |
| Ligne 52 | Col 72 | BT52 | `=DIST_PHASE_1_v2!BI41` | =DIST_PHASE_1_v2!BI41 |
| Ligne 52 | Col 73 | BU52 | `=DIST_PHASE_1_v2!BN41` | =DIST_PHASE_1_v2!BN41 |
| Ligne 52 | Col 74 | BV52 | `=DIST_PHASE_1_v2!BO41` | =DIST_PHASE_1_v2!BO41 |
| Ligne 52 | Col 75 | BW52 | `=DIST_PHASE_1_v2!BP41` | =DIST_PHASE_1_v2!BP41 |
| Ligne 52 | Col 76 | BX52 | `= (10.679 * BW52) / ((BU52/1000)^4.871 * BV52^1.852)` | = (10.679 * BW52) / ((BU52/1000)^4.871 * BV52^1.852) |
| Ligne 52 | Col 77 | BY52 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995850>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995850> |
| Ligne 52 | Col 78 | BZ52 | `=IF(BP52>0,
IF(BY52>0, BX52*BY52^1.852,-BX52*ABS(BY52)^1.852),
IF(BY52>0, BX52*BT52^1.852, -BX52*BT52^1.852))` | =IF(BP52>0,
IF(BY52>0, BX52*BY52^1.852,-BX52*ABS(BY52)^1.852),
IF(BY52>0, BX52*BT52^1.852, -BX52*BT52^1.852)) |
| Ligne 52 | Col 79 | CA52 | `=1.852*BX52*ABS(BY52)^(1.852-1)` | =1.852*BX52*ABS(BY52)^(1.852-1) |
| Ligne 52 | Col 80 | CB52 | `=BY52+$BT$64` | =BY52+$BT$64 |
| Ligne 52 | Col 84 | CF52 | `=IFERROR(MATCH(CI52,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI52,$BS$22:$BS$62,0),0) |
| Ligne 52 | Col 86 | CH52 | `=DIST_PHASE_1_v2!BS41` | =DIST_PHASE_1_v2!BS41 |
| Ligne 52 | Col 87 | CI52 | `=DIST_PHASE_1_v2!BT41` | =DIST_PHASE_1_v2!BT41 |
| Ligne 52 | Col 88 | CJ52 | `=DIST_PHASE_1_v2!BV41` | =DIST_PHASE_1_v2!BV41 |
| Ligne 52 | Col 89 | CK52 | `=DIST_PHASE_1_v2!CA41` | =DIST_PHASE_1_v2!CA41 |
| Ligne 52 | Col 91 | CM52 | `=DIST_PHASE_1_v2!CC41` | =DIST_PHASE_1_v2!CC41 |
| Ligne 52 | Col 92 | CN52 | `= (10.679 * CM52) / ((CK52/1000)^4.871 * CL52^1.852)` | = (10.679 * CM52) / ((CK52/1000)^4.871 * CL52^1.852) |
| Ligne 52 | Col 93 | CO52 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995910>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995910> |
| Ligne 52 | Col 94 | CP52 | `=IF(CF52>0,
IF(CO52>0, CN52*CO52^1.852,-CN52*ABS(CO52)^1.852),
IF(CO52>0, CN52*CJ52^1.852, -CN52*CJ52^1.852))` | =IF(CF52>0,
IF(CO52>0, CN52*CO52^1.852,-CN52*ABS(CO52)^1.852),
IF(CO52>0, CN52*CJ52^1.852, -CN52*CJ52^1.852)) |
| Ligne 52 | Col 95 | CQ52 | `=1.852*CN52*ABS(CO52)^(1.852-1)` | =1.852*CN52*ABS(CO52)^(1.852-1) |
| Ligne 52 | Col 96 | CR52 | `=CO52+$CJ$71` | =CO52+$CJ$71 |
| Ligne 52 | Col 100 | CV52 | `=IFERROR(MATCH(CY52,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY52,$CI$22:$CI$69,0),0) |
| Ligne 52 | Col 102 | CX52 | `=DIST_PHASE_1_v2!CF41` | =DIST_PHASE_1_v2!CF41 |
| Ligne 52 | Col 103 | CY52 | `=DIST_PHASE_1_v2!CG41` | =DIST_PHASE_1_v2!CG41 |
| Ligne 52 | Col 104 | CZ52 | `=DIST_PHASE_1_v2!CI41` | =DIST_PHASE_1_v2!CI41 |
| Ligne 52 | Col 105 | DA52 | `=DIST_PHASE_1_v2!CN41` | =DIST_PHASE_1_v2!CN41 |
| Ligne 52 | Col 106 | DB52 | `=DIST_PHASE_1_v2!CO41` | =DIST_PHASE_1_v2!CO41 |
| Ligne 52 | Col 107 | DC52 | `=DIST_PHASE_1_v2!CP41` | =DIST_PHASE_1_v2!CP41 |
| Ligne 52 | Col 108 | DD52 | `= (10.679 * DC52) / ((DA52/1000)^4.871 * DB52^1.852)` | = (10.679 * DC52) / ((DA52/1000)^4.871 * DB52^1.852) |
| Ligne 52 | Col 109 | DE52 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9959D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9959D0> |
| Ligne 52 | Col 110 | DF52 | `=IF(CV52>0,
IF(DE52>0, DD52*DE52^1.852,-DD52*ABS(DE52)^1.852),
IF(DE52>0, DD52*CZ52^1.852, -DD52*CZ52^1.852))` | =IF(CV52>0,
IF(DE52>0, DD52*DE52^1.852,-DD52*ABS(DE52)^1.852),
IF(DE52>0, DD52*CZ52^1.852, -DD52*CZ52^1.852)) |
| Ligne 52 | Col 111 | DG52 | `=1.852*DD52*ABS(DE52)^(1.852-1)` | =1.852*DD52*ABS(DE52)^(1.852-1) |
| Ligne 52 | Col 112 | DH52 | `=DE52+CZ86` | =DE52+CZ86 |
| Ligne 53 | Col 4 | D53 | `=DIST_PHASE_1_v2!E42` | =DIST_PHASE_1_v2!E42 |
| Ligne 53 | Col 5 | E53 | `=DIST_PHASE_1_v2!G42` | =DIST_PHASE_1_v2!G42 |
| Ligne 53 | Col 6 | F53 | `=DIST_PHASE_1_v2!L42` | =DIST_PHASE_1_v2!L42 |
| Ligne 53 | Col 7 | G53 | `=DIST_PHASE_1_v2!M42` | =DIST_PHASE_1_v2!M42 |
| Ligne 53 | Col 8 | H53 | `=DIST_PHASE_1_v2!N42` | =DIST_PHASE_1_v2!N42 |
| Ligne 53 | Col 9 | I53 | `= (10.679 * H53) / ((F53/1000)^4.871 * G53^1.852)` | = (10.679 * H53) / ((F53/1000)^4.871 * G53^1.852) |
| Ligne 53 | Col 10 | J53 | `=IF(C53="positif",E53,IF(C53="negatif",-E53,""))` | =IF(C53="positif",E53,IF(C53="negatif",-E53,"")) |
| Ligne 53 | Col 11 | K53 | `=IF(J53>0,I53*E53^1.852,-I53*E53^1.852)` | =IF(J53>0,I53*E53^1.852,-I53*E53^1.852) |
| Ligne 53 | Col 12 | L53 | `=1.852*I53*ABS(E53)^(1.852-1)` | =1.852*I53*ABS(E53)^(1.852-1) |
| Ligne 53 | Col 13 | M53 | `=J53+$D$93` | =J53+$D$93 |
| Ligne 53 | Col 16 | P53 | `=IFERROR(MATCH(S53,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S53,$D$22:$D$91,0),0) |
| Ligne 53 | Col 18 | R53 | `=DIST_PHASE_1_v2!Q42` | =DIST_PHASE_1_v2!Q42 |
| Ligne 53 | Col 19 | S53 | `=DIST_PHASE_1_v2!R42` | =DIST_PHASE_1_v2!R42 |
| Ligne 53 | Col 20 | T53 | `=DIST_PHASE_1_v2!T42` | =DIST_PHASE_1_v2!T42 |
| Ligne 53 | Col 21 | U53 | `=DIST_PHASE_1_v2!Y42` | =DIST_PHASE_1_v2!Y42 |
| Ligne 53 | Col 23 | W53 | `=DIST_PHASE_1_v2!AA42` | =DIST_PHASE_1_v2!AA42 |
| Ligne 53 | Col 24 | X53 | `= (10.679 * W53) / ((U53/1000)^4.871 * V53^1.852)` | = (10.679 * W53) / ((U53/1000)^4.871 * V53^1.852) |
| Ligne 53 | Col 25 | Y53 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995B50>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995B50> |
| Ligne 53 | Col 26 | Z53 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994EF0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD994EF0> |
| Ligne 53 | Col 27 | AA53 | `=IF(P53>0,
IF(R53="positif",1,-1),
0)` | =IF(P53>0,
IF(R53="positif",1,-1),
0) |
| Ligne 53 | Col 28 | AB53 | `=X53*SIGN(Y53)*ABS(Y53)^1.852` | =X53*SIGN(Y53)*ABS(Y53)^1.852 |
| Ligne 53 | Col 29 | AC53 | `=1.852*X53*ABS(Y53)^(1.852-1)` | =1.852*X53*ABS(Y53)^(1.852-1) |
| Ligne 53 | Col 30 | AD53 | `=IF(P53>0,
Y53+($D$93*Z53)+(AA53*$S$93),
Y53+$S$93)` | =IF(P53>0,
Y53+($D$93*Z53)+(AA53*$S$93),
Y53+$S$93) |
| Ligne 53 | Col 32 | AF53 | `=ABS(AD53)-ABS(Y53)` | =ABS(AD53)-ABS(Y53) |
| Ligne 53 | Col 36 | AJ53 | `=IFERROR(MATCH(AM53,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM53,$S$22:$S$91,0),0) |
| Ligne 53 | Col 38 | AL53 | `=TRONCONS_V2!AI40` | =TRONCONS_V2!AI40 |
| Ligne 53 | Col 39 | AM53 | `=TRONCONS_V2!AE40` | =TRONCONS_V2!AE40 |
| Ligne 53 | Col 40 | AN53 | `=DIST_PHASE_1_v2!AG42` | =DIST_PHASE_1_v2!AG42 |
| Ligne 53 | Col 41 | AO53 | `=DIST_PHASE_1_v2!AL42` | =DIST_PHASE_1_v2!AL42 |
| Ligne 53 | Col 43 | AQ53 | `=TRONCONS_V2!AG40` | =TRONCONS_V2!AG40 |
| Ligne 53 | Col 44 | AR53 | `= (10.679 * AQ53) / ((AO53/1000)^4.871 * AP53^1.852)` | = (10.679 * AQ53) / ((AO53/1000)^4.871 * AP53^1.852) |
| Ligne 53 | Col 45 | AS53 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995C70>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995C70> |
| Ligne 53 | Col 46 | AT53 | `=IF(AJ53>0,
        IF(AS53>0, AR53*AS53^1.852,-AR53*ABS(AS53)^1.852),
        IF(AS53>0, AR53*AN53^1.852, -AR53*AN53^1.852))` | =IF(AJ53>0,
        IF(AS53>0, AR53*AS53^1.852,-AR53*ABS(AS53)^1.852),
        IF(AS53>0, AR53*AN53^1.852, -AR53*AN53^1.852)) |
| Ligne 53 | Col 47 | AU53 | `=1.852*AR53*ABS(AS53)^(1.852-1)` | =1.852*AR53*ABS(AS53)^(1.852-1) |
| Ligne 53 | Col 48 | AV53 | `=AS53+$AN$60` | =AS53+$AN$60 |
| Ligne 53 | Col 52 | AZ53 | `=IFERROR(MATCH(BC53,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC53,$AM$22:$AM$57,0),0) |
| Ligne 53 | Col 54 | BB53 | `=DIST_PHASE_1_v2!AQ42` | =DIST_PHASE_1_v2!AQ42 |
| Ligne 53 | Col 55 | BC53 | `=DIST_PHASE_1_v2!AR42` | =DIST_PHASE_1_v2!AR42 |
| Ligne 53 | Col 56 | BD53 | `=DIST_PHASE_1_v2!AT42` | =DIST_PHASE_1_v2!AT42 |
| Ligne 53 | Col 57 | BE53 | `=DIST_PHASE_1_v2!AY42` | =DIST_PHASE_1_v2!AY42 |
| Ligne 53 | Col 58 | BF53 | `=DIST_PHASE_1_v2!AZ42` | =DIST_PHASE_1_v2!AZ42 |
| Ligne 53 | Col 59 | BG53 | `=DIST_PHASE_1_v2!BA42` | =DIST_PHASE_1_v2!BA42 |
| Ligne 53 | Col 60 | BH53 | `= (10.679 * BG53) / ((BE53/1000)^4.871 * BF53^1.852)` | = (10.679 * BG53) / ((BE53/1000)^4.871 * BF53^1.852) |
| Ligne 53 | Col 61 | BI53 | `=IF(BB53="positif",BD53,IF(BB53="negatif",-BD53,""))` | =IF(BB53="positif",BD53,IF(BB53="negatif",-BD53,"")) |
| Ligne 53 | Col 62 | BJ53 | `=IF(AZ53>0,
IF(BI53>0, BH53*BI53^1.852,-BH53*ABS(BI53)^1.852),
IF(BI53>0, BH53*BD53^1.852, -BH53*BD53^1.852))` | =IF(AZ53>0,
IF(BI53>0, BH53*BI53^1.852,-BH53*ABS(BI53)^1.852),
IF(BI53>0, BH53*BD53^1.852, -BH53*BD53^1.852)) |
| Ligne 53 | Col 63 | BK53 | `=1.852*BH53*ABS(BI53)^(1.852-1)` | =1.852*BH53*ABS(BI53)^(1.852-1) |
| Ligne 53 | Col 64 | BL53 | `=BI53+$BD$75` | =BI53+$BD$75 |
| Ligne 53 | Col 68 | BP53 | `=IFERROR(MATCH(BS53,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS53,$BC$22:$BC$73,0),0) |
| Ligne 53 | Col 70 | BR53 | `=DIST_PHASE_1_v2!BF42` | =DIST_PHASE_1_v2!BF42 |
| Ligne 53 | Col 71 | BS53 | `=DIST_PHASE_1_v2!BG42` | =DIST_PHASE_1_v2!BG42 |
| Ligne 53 | Col 72 | BT53 | `=DIST_PHASE_1_v2!BI42` | =DIST_PHASE_1_v2!BI42 |
| Ligne 53 | Col 73 | BU53 | `=DIST_PHASE_1_v2!BN42` | =DIST_PHASE_1_v2!BN42 |
| Ligne 53 | Col 74 | BV53 | `=DIST_PHASE_1_v2!BO42` | =DIST_PHASE_1_v2!BO42 |
| Ligne 53 | Col 75 | BW53 | `=DIST_PHASE_1_v2!BP42` | =DIST_PHASE_1_v2!BP42 |
| Ligne 53 | Col 76 | BX53 | `= (10.679 * BW53) / ((BU53/1000)^4.871 * BV53^1.852)` | = (10.679 * BW53) / ((BU53/1000)^4.871 * BV53^1.852) |
| Ligne 53 | Col 77 | BY53 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995D90>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995D90> |
| Ligne 53 | Col 78 | BZ53 | `=IF(BP53>0,
IF(BY53>0, BX53*BY53^1.852,-BX53*ABS(BY53)^1.852),
IF(BY53>0, BX53*BT53^1.852, -BX53*BT53^1.852))` | =IF(BP53>0,
IF(BY53>0, BX53*BY53^1.852,-BX53*ABS(BY53)^1.852),
IF(BY53>0, BX53*BT53^1.852, -BX53*BT53^1.852)) |
| Ligne 53 | Col 79 | CA53 | `=1.852*BX53*ABS(BY53)^(1.852-1)` | =1.852*BX53*ABS(BY53)^(1.852-1) |
| Ligne 53 | Col 80 | CB53 | `=BY53+$BT$64` | =BY53+$BT$64 |
| Ligne 53 | Col 84 | CF53 | `=IFERROR(MATCH(CI53,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI53,$BS$22:$BS$62,0),0) |
| Ligne 53 | Col 86 | CH53 | `=DIST_PHASE_1_v2!BS42` | =DIST_PHASE_1_v2!BS42 |
| Ligne 53 | Col 87 | CI53 | `=DIST_PHASE_1_v2!BT42` | =DIST_PHASE_1_v2!BT42 |
| Ligne 53 | Col 88 | CJ53 | `=DIST_PHASE_1_v2!BV42` | =DIST_PHASE_1_v2!BV42 |
| Ligne 53 | Col 89 | CK53 | `=DIST_PHASE_1_v2!CA42` | =DIST_PHASE_1_v2!CA42 |
| Ligne 53 | Col 91 | CM53 | `=DIST_PHASE_1_v2!CC42` | =DIST_PHASE_1_v2!CC42 |
| Ligne 53 | Col 92 | CN53 | `= (10.679 * CM53) / ((CK53/1000)^4.871 * CL53^1.852)` | = (10.679 * CM53) / ((CK53/1000)^4.871 * CL53^1.852) |
| Ligne 53 | Col 93 | CO53 | `=IF(CH53="positif",CJ53,IF(CH53="negatif",-CJ53,""))` | =IF(CH53="positif",CJ53,IF(CH53="negatif",-CJ53,"")) |
| Ligne 53 | Col 94 | CP53 | `=IF(CF53>0,
IF(CO53>0, CN53*CO53^1.852,-CN53*ABS(CO53)^1.852),
IF(CO53>0, CN53*CJ53^1.852, -CN53*CJ53^1.852))` | =IF(CF53>0,
IF(CO53>0, CN53*CO53^1.852,-CN53*ABS(CO53)^1.852),
IF(CO53>0, CN53*CJ53^1.852, -CN53*CJ53^1.852)) |
| Ligne 53 | Col 95 | CQ53 | `=1.852*CN53*ABS(CO53)^(1.852-1)` | =1.852*CN53*ABS(CO53)^(1.852-1) |
| Ligne 53 | Col 96 | CR53 | `=CO53+$CJ$71` | =CO53+$CJ$71 |
| Ligne 53 | Col 100 | CV53 | `=IFERROR(MATCH(CY53,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY53,$CI$22:$CI$69,0),0) |
| Ligne 53 | Col 102 | CX53 | `=DIST_PHASE_1_v2!CF42` | =DIST_PHASE_1_v2!CF42 |
| Ligne 53 | Col 103 | CY53 | `=DIST_PHASE_1_v2!CG42` | =DIST_PHASE_1_v2!CG42 |
| Ligne 53 | Col 104 | CZ53 | `=DIST_PHASE_1_v2!CI42` | =DIST_PHASE_1_v2!CI42 |
| Ligne 53 | Col 105 | DA53 | `=DIST_PHASE_1_v2!CN42` | =DIST_PHASE_1_v2!CN42 |
| Ligne 53 | Col 106 | DB53 | `=DIST_PHASE_1_v2!CO42` | =DIST_PHASE_1_v2!CO42 |
| Ligne 53 | Col 107 | DC53 | `=DIST_PHASE_1_v2!CP42` | =DIST_PHASE_1_v2!CP42 |
| Ligne 53 | Col 108 | DD53 | `= (10.679 * DC53) / ((DA53/1000)^4.871 * DB53^1.852)` | = (10.679 * DC53) / ((DA53/1000)^4.871 * DB53^1.852) |
| Ligne 53 | Col 109 | DE53 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995F10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD995F10> |
| Ligne 53 | Col 110 | DF53 | `=IF(CV53>0,
IF(DE53>0, DD53*DE53^1.852,-DD53*ABS(DE53)^1.852),
IF(DE53>0, DD53*CZ53^1.852, -DD53*CZ53^1.852))` | =IF(CV53>0,
IF(DE53>0, DD53*DE53^1.852,-DD53*ABS(DE53)^1.852),
IF(DE53>0, DD53*CZ53^1.852, -DD53*CZ53^1.852)) |
| Ligne 53 | Col 111 | DG53 | `=1.852*DD53*ABS(DE53)^(1.852-1)` | =1.852*DD53*ABS(DE53)^(1.852-1) |
| Ligne 53 | Col 112 | DH53 | `=DE53+CZ87` | =DE53+CZ87 |
| Ligne 54 | Col 4 | D54 | `=DIST_PHASE_1_v2!E43` | =DIST_PHASE_1_v2!E43 |
| Ligne 54 | Col 5 | E54 | `=DIST_PHASE_1_v2!G43` | =DIST_PHASE_1_v2!G43 |
| Ligne 54 | Col 6 | F54 | `=DIST_PHASE_1_v2!L43` | =DIST_PHASE_1_v2!L43 |
| Ligne 54 | Col 7 | G54 | `=DIST_PHASE_1_v2!M43` | =DIST_PHASE_1_v2!M43 |
| Ligne 54 | Col 8 | H54 | `=DIST_PHASE_1_v2!N43` | =DIST_PHASE_1_v2!N43 |
| Ligne 54 | Col 9 | I54 | `= (10.679 * H54) / ((F54/1000)^4.871 * G54^1.852)` | = (10.679 * H54) / ((F54/1000)^4.871 * G54^1.852) |
| Ligne 54 | Col 10 | J54 | `=IF(C54="positif",E54,IF(C54="negatif",-E54,""))` | =IF(C54="positif",E54,IF(C54="negatif",-E54,"")) |
| Ligne 54 | Col 11 | K54 | `=IF(J54>0,I54*E54^1.852,-I54*E54^1.852)` | =IF(J54>0,I54*E54^1.852,-I54*E54^1.852) |
| Ligne 54 | Col 12 | L54 | `=1.852*I54*ABS(E54)^(1.852-1)` | =1.852*I54*ABS(E54)^(1.852-1) |
| Ligne 54 | Col 13 | M54 | `=J54+$D$93` | =J54+$D$93 |
| Ligne 54 | Col 16 | P54 | `=IFERROR(MATCH(S54,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S54,$D$22:$D$91,0),0) |
| Ligne 54 | Col 18 | R54 | `=DIST_PHASE_1_v2!Q43` | =DIST_PHASE_1_v2!Q43 |
| Ligne 54 | Col 19 | S54 | `=DIST_PHASE_1_v2!R43` | =DIST_PHASE_1_v2!R43 |
| Ligne 54 | Col 20 | T54 | `=DIST_PHASE_1_v2!T43` | =DIST_PHASE_1_v2!T43 |
| Ligne 54 | Col 21 | U54 | `=DIST_PHASE_1_v2!Y43` | =DIST_PHASE_1_v2!Y43 |
| Ligne 54 | Col 23 | W54 | `=DIST_PHASE_1_v2!AA43` | =DIST_PHASE_1_v2!AA43 |
| Ligne 54 | Col 24 | X54 | `= (10.679 * W54) / ((U54/1000)^4.871 * V54^1.852)` | = (10.679 * W54) / ((U54/1000)^4.871 * V54^1.852) |
| Ligne 54 | Col 25 | Y54 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996090>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996090> |
| Ligne 54 | Col 26 | Z54 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9953D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9953D0> |
| Ligne 54 | Col 27 | AA54 | `=IF(P54>0,
IF(R54="positif",1,-1),
0)` | =IF(P54>0,
IF(R54="positif",1,-1),
0) |
| Ligne 54 | Col 28 | AB54 | `=X54*SIGN(Y54)*ABS(Y54)^1.852` | =X54*SIGN(Y54)*ABS(Y54)^1.852 |
| Ligne 54 | Col 29 | AC54 | `=1.852*X54*ABS(Y54)^(1.852-1)` | =1.852*X54*ABS(Y54)^(1.852-1) |
| Ligne 54 | Col 30 | AD54 | `=IF(P54>0,
Y54+($D$93*Z54)+(AA54*$S$93),
Y54+$S$93)` | =IF(P54>0,
Y54+($D$93*Z54)+(AA54*$S$93),
Y54+$S$93) |
| Ligne 54 | Col 32 | AF54 | `=ABS(AD54)-ABS(Y54)` | =ABS(AD54)-ABS(Y54) |
| Ligne 54 | Col 36 | AJ54 | `=IFERROR(MATCH(AM54,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM54,$S$22:$S$91,0),0) |
| Ligne 54 | Col 38 | AL54 | `=TRONCONS_V2!AI41` | =TRONCONS_V2!AI41 |
| Ligne 54 | Col 39 | AM54 | `=TRONCONS_V2!AE41` | =TRONCONS_V2!AE41 |
| Ligne 54 | Col 40 | AN54 | `=DIST_PHASE_1_v2!AG43` | =DIST_PHASE_1_v2!AG43 |
| Ligne 54 | Col 41 | AO54 | `=DIST_PHASE_1_v2!AL43` | =DIST_PHASE_1_v2!AL43 |
| Ligne 54 | Col 43 | AQ54 | `=TRONCONS_V2!AG41` | =TRONCONS_V2!AG41 |
| Ligne 54 | Col 44 | AR54 | `= (10.679 * AQ54) / ((AO54/1000)^4.871 * AP54^1.852)` | = (10.679 * AQ54) / ((AO54/1000)^4.871 * AP54^1.852) |
| Ligne 54 | Col 45 | AS54 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996270>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996270> |
| Ligne 54 | Col 46 | AT54 | `=IF(AJ54>0,
        IF(AS54>0, AR54*AS54^1.852,-AR54*ABS(AS54)^1.852),
        IF(AS54>0, AR54*AN54^1.852, -AR54*AN54^1.852))` | =IF(AJ54>0,
        IF(AS54>0, AR54*AS54^1.852,-AR54*ABS(AS54)^1.852),
        IF(AS54>0, AR54*AN54^1.852, -AR54*AN54^1.852)) |
| Ligne 54 | Col 47 | AU54 | `=1.852*AR54*ABS(AS54)^(1.852-1)` | =1.852*AR54*ABS(AS54)^(1.852-1) |
| Ligne 54 | Col 48 | AV54 | `=AS54+$AN$60` | =AS54+$AN$60 |
| Ligne 54 | Col 52 | AZ54 | `=IFERROR(MATCH(BC54,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC54,$AM$22:$AM$57,0),0) |
| Ligne 54 | Col 54 | BB54 | `=DIST_PHASE_1_v2!AQ43` | =DIST_PHASE_1_v2!AQ43 |
| Ligne 54 | Col 55 | BC54 | `=DIST_PHASE_1_v2!AR43` | =DIST_PHASE_1_v2!AR43 |
| Ligne 54 | Col 56 | BD54 | `=DIST_PHASE_1_v2!AT43` | =DIST_PHASE_1_v2!AT43 |
| Ligne 54 | Col 57 | BE54 | `=DIST_PHASE_1_v2!AY43` | =DIST_PHASE_1_v2!AY43 |
| Ligne 54 | Col 58 | BF54 | `=DIST_PHASE_1_v2!AZ43` | =DIST_PHASE_1_v2!AZ43 |
| Ligne 54 | Col 59 | BG54 | `=DIST_PHASE_1_v2!BA43` | =DIST_PHASE_1_v2!BA43 |
| Ligne 54 | Col 60 | BH54 | `= (10.679 * BG54) / ((BE54/1000)^4.871 * BF54^1.852)` | = (10.679 * BG54) / ((BE54/1000)^4.871 * BF54^1.852) |
| Ligne 54 | Col 61 | BI54 | `=IF(BB54="positif",BD54,IF(BB54="negatif",-BD54,""))` | =IF(BB54="positif",BD54,IF(BB54="negatif",-BD54,"")) |
| Ligne 54 | Col 62 | BJ54 | `=IF(AZ54>0,
        IF(BI54>0, BH54*BI54^1.852,-BH54*ABS(BI54)^1.852),
        IF(BI54>0, BH54*BD54^1.852, -BH54*BD54^1.852))` | =IF(AZ54>0,
        IF(BI54>0, BH54*BI54^1.852,-BH54*ABS(BI54)^1.852),
        IF(BI54>0, BH54*BD54^1.852, -BH54*BD54^1.852)) |
| Ligne 54 | Col 63 | BK54 | `=1.852*BH54*ABS(BI54)^(1.852-1)` | =1.852*BH54*ABS(BI54)^(1.852-1) |
| Ligne 54 | Col 64 | BL54 | `=BI54+$BD$75` | =BI54+$BD$75 |
| Ligne 54 | Col 68 | BP54 | `=IFERROR(MATCH(BS54,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS54,$BC$22:$BC$73,0),0) |
| Ligne 54 | Col 70 | BR54 | `=DIST_PHASE_1_v2!BF43` | =DIST_PHASE_1_v2!BF43 |
| Ligne 54 | Col 71 | BS54 | `=DIST_PHASE_1_v2!BG43` | =DIST_PHASE_1_v2!BG43 |
| Ligne 54 | Col 72 | BT54 | `=DIST_PHASE_1_v2!BI43` | =DIST_PHASE_1_v2!BI43 |
| Ligne 54 | Col 73 | BU54 | `=DIST_PHASE_1_v2!BN43` | =DIST_PHASE_1_v2!BN43 |
| Ligne 54 | Col 74 | BV54 | `=DIST_PHASE_1_v2!BO43` | =DIST_PHASE_1_v2!BO43 |
| Ligne 54 | Col 75 | BW54 | `=DIST_PHASE_1_v2!BP43` | =DIST_PHASE_1_v2!BP43 |
| Ligne 54 | Col 76 | BX54 | `= (10.679 * BW54) / ((BU54/1000)^4.871 * BV54^1.852)` | = (10.679 * BW54) / ((BU54/1000)^4.871 * BV54^1.852) |
| Ligne 54 | Col 77 | BY54 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9963F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9963F0> |
| Ligne 54 | Col 78 | BZ54 | `=IF(BP54>0,
IF(BY54>0, BX54*BY54^1.852,-BX54*ABS(BY54)^1.852),
IF(BY54>0, BX54*BT54^1.852, -BX54*BT54^1.852))` | =IF(BP54>0,
IF(BY54>0, BX54*BY54^1.852,-BX54*ABS(BY54)^1.852),
IF(BY54>0, BX54*BT54^1.852, -BX54*BT54^1.852)) |
| Ligne 54 | Col 79 | CA54 | `=1.852*BX54*ABS(BY54)^(1.852-1)` | =1.852*BX54*ABS(BY54)^(1.852-1) |
| Ligne 54 | Col 80 | CB54 | `=BY54+$BT$64` | =BY54+$BT$64 |
| Ligne 54 | Col 84 | CF54 | `=IFERROR(MATCH(CI54,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI54,$BS$22:$BS$62,0),0) |
| Ligne 54 | Col 86 | CH54 | `=DIST_PHASE_1_v2!BS43` | =DIST_PHASE_1_v2!BS43 |
| Ligne 54 | Col 87 | CI54 | `=DIST_PHASE_1_v2!BT43` | =DIST_PHASE_1_v2!BT43 |
| Ligne 54 | Col 88 | CJ54 | `=DIST_PHASE_1_v2!BV43` | =DIST_PHASE_1_v2!BV43 |
| Ligne 54 | Col 89 | CK54 | `=DIST_PHASE_1_v2!CA43` | =DIST_PHASE_1_v2!CA43 |
| Ligne 54 | Col 91 | CM54 | `=DIST_PHASE_1_v2!CC43` | =DIST_PHASE_1_v2!CC43 |
| Ligne 54 | Col 92 | CN54 | `= (10.679 * CM54) / ((CK54/1000)^4.871 * CL54^1.852)` | = (10.679 * CM54) / ((CK54/1000)^4.871 * CL54^1.852) |
| Ligne 54 | Col 93 | CO54 | `=IF(CH54="positif",CJ54,IF(CH54="negatif",-CJ54,""))` | =IF(CH54="positif",CJ54,IF(CH54="negatif",-CJ54,"")) |
| Ligne 54 | Col 94 | CP54 | `=IF(CF54>0,
IF(CO54>0, CN54*CO54^1.852,-CN54*ABS(CO54)^1.852),
IF(CO54>0, CN54*CJ54^1.852, -CN54*CJ54^1.852))` | =IF(CF54>0,
IF(CO54>0, CN54*CO54^1.852,-CN54*ABS(CO54)^1.852),
IF(CO54>0, CN54*CJ54^1.852, -CN54*CJ54^1.852)) |
| Ligne 54 | Col 95 | CQ54 | `=1.852*CN54*ABS(CO54)^(1.852-1)` | =1.852*CN54*ABS(CO54)^(1.852-1) |
| Ligne 54 | Col 96 | CR54 | `=CO54+$CJ$71` | =CO54+$CJ$71 |
| Ligne 54 | Col 100 | CV54 | `=IFERROR(MATCH(CY54,$CI$22:$CI$69,0),0)` | =IFERROR(MATCH(CY54,$CI$22:$CI$69,0),0) |
| Ligne 54 | Col 102 | CX54 | `=DIST_PHASE_1_v2!CF43` | =DIST_PHASE_1_v2!CF43 |
| Ligne 54 | Col 103 | CY54 | `=DIST_PHASE_1_v2!CG43` | =DIST_PHASE_1_v2!CG43 |
| Ligne 54 | Col 104 | CZ54 | `=DIST_PHASE_1_v2!CI43` | =DIST_PHASE_1_v2!CI43 |
| Ligne 54 | Col 105 | DA54 | `=DIST_PHASE_1_v2!CN43` | =DIST_PHASE_1_v2!CN43 |
| Ligne 54 | Col 106 | DB54 | `=DIST_PHASE_1_v2!CO43` | =DIST_PHASE_1_v2!CO43 |
| Ligne 54 | Col 107 | DC54 | `=DIST_PHASE_1_v2!CP43` | =DIST_PHASE_1_v2!CP43 |
| Ligne 54 | Col 108 | DD54 | `= (10.679 * DC54) / ((DA54/1000)^4.871 * DB54^1.852)` | = (10.679 * DC54) / ((DA54/1000)^4.871 * DB54^1.852) |
| Ligne 54 | Col 109 | DE54 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996570>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996570> |
| Ligne 54 | Col 110 | DF54 | `=IF(CV54>0,
IF(DE54>0, DD54*DE54^1.852,-DD54*ABS(DE54)^1.852),
IF(DE54>0, DD54*CZ54^1.852, -DD54*CZ54^1.852))` | =IF(CV54>0,
IF(DE54>0, DD54*DE54^1.852,-DD54*ABS(DE54)^1.852),
IF(DE54>0, DD54*CZ54^1.852, -DD54*CZ54^1.852)) |
| Ligne 54 | Col 111 | DG54 | `=1.852*DD54*ABS(DE54)^(1.852-1)` | =1.852*DD54*ABS(DE54)^(1.852-1) |
| Ligne 54 | Col 112 | DH54 | `=DE54+CZ88` | =DE54+CZ88 |
| Ligne 55 | Col 4 | D55 | `=DIST_PHASE_1_v2!E44` | =DIST_PHASE_1_v2!E44 |
| Ligne 55 | Col 5 | E55 | `=DIST_PHASE_1_v2!G44` | =DIST_PHASE_1_v2!G44 |
| Ligne 55 | Col 6 | F55 | `=DIST_PHASE_1_v2!L44` | =DIST_PHASE_1_v2!L44 |
| Ligne 55 | Col 7 | G55 | `=DIST_PHASE_1_v2!M44` | =DIST_PHASE_1_v2!M44 |
| Ligne 55 | Col 8 | H55 | `=DIST_PHASE_1_v2!N44` | =DIST_PHASE_1_v2!N44 |
| Ligne 55 | Col 9 | I55 | `= (10.679 * H55) / ((F55/1000)^4.871 * G55^1.852)` | = (10.679 * H55) / ((F55/1000)^4.871 * G55^1.852) |
| Ligne 55 | Col 10 | J55 | `=IF(C55="positif",E55,IF(C55="negatif",-E55,""))` | =IF(C55="positif",E55,IF(C55="negatif",-E55,"")) |
| Ligne 55 | Col 11 | K55 | `=IF(J55>0,I55*E55^1.852,-I55*E55^1.852)` | =IF(J55>0,I55*E55^1.852,-I55*E55^1.852) |
| Ligne 55 | Col 12 | L55 | `=1.852*I55*ABS(E55)^(1.852-1)` | =1.852*I55*ABS(E55)^(1.852-1) |
| Ligne 55 | Col 13 | M55 | `=J55+$D$93` | =J55+$D$93 |
| Ligne 55 | Col 16 | P55 | `=IFERROR(MATCH(S55,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S55,$D$22:$D$91,0),0) |
| Ligne 55 | Col 18 | R55 | `=DIST_PHASE_1_v2!Q44` | =DIST_PHASE_1_v2!Q44 |
| Ligne 55 | Col 19 | S55 | `=DIST_PHASE_1_v2!R44` | =DIST_PHASE_1_v2!R44 |
| Ligne 55 | Col 20 | T55 | `=DIST_PHASE_1_v2!T44` | =DIST_PHASE_1_v2!T44 |
| Ligne 55 | Col 21 | U55 | `=DIST_PHASE_1_v2!Y44` | =DIST_PHASE_1_v2!Y44 |
| Ligne 55 | Col 23 | W55 | `=DIST_PHASE_1_v2!AA44` | =DIST_PHASE_1_v2!AA44 |
| Ligne 55 | Col 24 | X55 | `= (10.679 * W55) / ((U55/1000)^4.871 * V55^1.852)` | = (10.679 * W55) / ((U55/1000)^4.871 * V55^1.852) |
| Ligne 55 | Col 25 | Y55 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996930>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996930> |
| Ligne 55 | Col 26 | Z55 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9965D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9965D0> |
| Ligne 55 | Col 27 | AA55 | `=IF(P55>0,
IF(R55="positif",1,-1),
0)` | =IF(P55>0,
IF(R55="positif",1,-1),
0) |
| Ligne 55 | Col 28 | AB55 | `=X55*SIGN(Y55)*ABS(Y55)^1.852` | =X55*SIGN(Y55)*ABS(Y55)^1.852 |
| Ligne 55 | Col 29 | AC55 | `=1.852*X55*ABS(Y55)^(1.852-1)` | =1.852*X55*ABS(Y55)^(1.852-1) |
| Ligne 55 | Col 30 | AD55 | `=IF(P55>0,
Y55+($D$93*Z55)+(AA55*$S$93),
Y55+$S$93)` | =IF(P55>0,
Y55+($D$93*Z55)+(AA55*$S$93),
Y55+$S$93) |
| Ligne 55 | Col 32 | AF55 | `=ABS(AD55)-ABS(Y55)` | =ABS(AD55)-ABS(Y55) |
| Ligne 55 | Col 36 | AJ55 | `=IFERROR(MATCH(AM55,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM55,$S$22:$S$91,0),0) |
| Ligne 55 | Col 38 | AL55 | `=TRONCONS_V2!AI42` | =TRONCONS_V2!AI42 |
| Ligne 55 | Col 39 | AM55 | `=TRONCONS_V2!AE42` | =TRONCONS_V2!AE42 |
| Ligne 55 | Col 40 | AN55 | `=DIST_PHASE_1_v2!AG44` | =DIST_PHASE_1_v2!AG44 |
| Ligne 55 | Col 41 | AO55 | `=DIST_PHASE_1_v2!AL44` | =DIST_PHASE_1_v2!AL44 |
| Ligne 55 | Col 43 | AQ55 | `=TRONCONS_V2!AG42` | =TRONCONS_V2!AG42 |
| Ligne 55 | Col 44 | AR55 | `= (10.679 * AQ55) / ((AO55/1000)^4.871 * AP55^1.852)` | = (10.679 * AQ55) / ((AO55/1000)^4.871 * AP55^1.852) |
| Ligne 55 | Col 45 | AS55 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996A50>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996A50> |
| Ligne 55 | Col 46 | AT55 | `=IF(AJ55>0,
        IF(AS55>0, AR55*AS55^1.852,-AR55*ABS(AS55)^1.852),
        IF(AS55>0, AR55*AN55^1.852, -AR55*AN55^1.852))` | =IF(AJ55>0,
        IF(AS55>0, AR55*AS55^1.852,-AR55*ABS(AS55)^1.852),
        IF(AS55>0, AR55*AN55^1.852, -AR55*AN55^1.852)) |
| Ligne 55 | Col 47 | AU55 | `=1.852*AR55*ABS(AS55)^(1.852-1)` | =1.852*AR55*ABS(AS55)^(1.852-1) |
| Ligne 55 | Col 48 | AV55 | `=AS55+$AN$60` | =AS55+$AN$60 |
| Ligne 55 | Col 52 | AZ55 | `=IFERROR(MATCH(BC55,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC55,$AM$22:$AM$57,0),0) |
| Ligne 55 | Col 54 | BB55 | `=DIST_PHASE_1_v2!AQ44` | =DIST_PHASE_1_v2!AQ44 |
| Ligne 55 | Col 55 | BC55 | `=DIST_PHASE_1_v2!AR44` | =DIST_PHASE_1_v2!AR44 |
| Ligne 55 | Col 56 | BD55 | `=DIST_PHASE_1_v2!AT44` | =DIST_PHASE_1_v2!AT44 |
| Ligne 55 | Col 57 | BE55 | `=DIST_PHASE_1_v2!AY44` | =DIST_PHASE_1_v2!AY44 |
| Ligne 55 | Col 58 | BF55 | `=DIST_PHASE_1_v2!AZ44` | =DIST_PHASE_1_v2!AZ44 |
| Ligne 55 | Col 59 | BG55 | `=DIST_PHASE_1_v2!BA44` | =DIST_PHASE_1_v2!BA44 |
| Ligne 55 | Col 60 | BH55 | `= (10.679 * BG55) / ((BE55/1000)^4.871 * BF55^1.852)` | = (10.679 * BG55) / ((BE55/1000)^4.871 * BF55^1.852) |
| Ligne 55 | Col 61 | BI55 | `=IF(BB55="positif",BD55,IF(BB55="negatif",-BD55,""))` | =IF(BB55="positif",BD55,IF(BB55="negatif",-BD55,"")) |
| Ligne 55 | Col 62 | BJ55 | `=IF(AZ55>0,
        IF(BI55>0, BH55*BI55^1.852,-BH55*ABS(BI55)^1.852),
        IF(BI55>0, BH55*BD55^1.852, -BH55*BD55^1.852))` | =IF(AZ55>0,
        IF(BI55>0, BH55*BI55^1.852,-BH55*ABS(BI55)^1.852),
        IF(BI55>0, BH55*BD55^1.852, -BH55*BD55^1.852)) |
| Ligne 55 | Col 63 | BK55 | `=1.852*BH55*ABS(BI55)^(1.852-1)` | =1.852*BH55*ABS(BI55)^(1.852-1) |
| Ligne 55 | Col 64 | BL55 | `=BI55+$BD$75` | =BI55+$BD$75 |
| Ligne 55 | Col 68 | BP55 | `=IFERROR(MATCH(BS55,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS55,$BC$22:$BC$73,0),0) |
| Ligne 55 | Col 70 | BR55 | `=DIST_PHASE_1_v2!BF44` | =DIST_PHASE_1_v2!BF44 |
| Ligne 55 | Col 71 | BS55 | `=DIST_PHASE_1_v2!BG44` | =DIST_PHASE_1_v2!BG44 |
| Ligne 55 | Col 72 | BT55 | `=DIST_PHASE_1_v2!BI44` | =DIST_PHASE_1_v2!BI44 |
| Ligne 55 | Col 73 | BU55 | `=DIST_PHASE_1_v2!BN44` | =DIST_PHASE_1_v2!BN44 |
| Ligne 55 | Col 74 | BV55 | `=DIST_PHASE_1_v2!BO44` | =DIST_PHASE_1_v2!BO44 |
| Ligne 55 | Col 75 | BW55 | `=DIST_PHASE_1_v2!BP44` | =DIST_PHASE_1_v2!BP44 |
| Ligne 55 | Col 76 | BX55 | `= (10.679 * BW55) / ((BU55/1000)^4.871 * BV55^1.852)` | = (10.679 * BW55) / ((BU55/1000)^4.871 * BV55^1.852) |
| Ligne 55 | Col 77 | BY55 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996B70>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996B70> |
| Ligne 55 | Col 78 | BZ55 | `=IF(BP55>0,
IF(BY55>0, BX55*BY55^1.852,-BX55*ABS(BY55)^1.852),
IF(BY55>0, BX55*BT55^1.852, -BX55*BT55^1.852))` | =IF(BP55>0,
IF(BY55>0, BX55*BY55^1.852,-BX55*ABS(BY55)^1.852),
IF(BY55>0, BX55*BT55^1.852, -BX55*BT55^1.852)) |
| Ligne 55 | Col 79 | CA55 | `=1.852*BX55*ABS(BY55)^(1.852-1)` | =1.852*BX55*ABS(BY55)^(1.852-1) |
| Ligne 55 | Col 80 | CB55 | `=BY55+$BT$64` | =BY55+$BT$64 |
| Ligne 55 | Col 84 | CF55 | `=IFERROR(MATCH(CI55,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI55,$BS$22:$BS$62,0),0) |
| Ligne 55 | Col 86 | CH55 | `=DIST_PHASE_1_v2!BS44` | =DIST_PHASE_1_v2!BS44 |
| Ligne 55 | Col 87 | CI55 | `=DIST_PHASE_1_v2!BT44` | =DIST_PHASE_1_v2!BT44 |
| Ligne 55 | Col 88 | CJ55 | `=DIST_PHASE_1_v2!BV44` | =DIST_PHASE_1_v2!BV44 |
| Ligne 55 | Col 89 | CK55 | `=DIST_PHASE_1_v2!CA44` | =DIST_PHASE_1_v2!CA44 |
| Ligne 55 | Col 91 | CM55 | `=DIST_PHASE_1_v2!CC44` | =DIST_PHASE_1_v2!CC44 |
| Ligne 55 | Col 92 | CN55 | `= (10.679 * CM55) / ((CK55/1000)^4.871 * CL55^1.852)` | = (10.679 * CM55) / ((CK55/1000)^4.871 * CL55^1.852) |
| Ligne 55 | Col 93 | CO55 | `=IF(CH55="positif",CJ55,IF(CH55="negatif",-CJ55,""))` | =IF(CH55="positif",CJ55,IF(CH55="negatif",-CJ55,"")) |
| Ligne 55 | Col 94 | CP55 | `=IF(CF55>0,
IF(CO55>0, CN55*CO55^1.852,-CN55*ABS(CO55)^1.852),
IF(CO55>0, CN55*CJ55^1.852, -CN55*CJ55^1.852))` | =IF(CF55>0,
IF(CO55>0, CN55*CO55^1.852,-CN55*ABS(CO55)^1.852),
IF(CO55>0, CN55*CJ55^1.852, -CN55*CJ55^1.852)) |
| Ligne 55 | Col 95 | CQ55 | `=1.852*CN55*ABS(CO55)^(1.852-1)` | =1.852*CN55*ABS(CO55)^(1.852-1) |
| Ligne 55 | Col 96 | CR55 | `=CO55+$CJ$71` | =CO55+$CJ$71 |
| Ligne 55 | Col 110 | DF55 | `=SUM(DF22:DF54)` | =SUM(DF22:DF54) |
| Ligne 55 | Col 111 | DG55 | `=SUM(DG22:DG54)` | =SUM(DG22:DG54) |
| Ligne 56 | Col 4 | D56 | `=DIST_PHASE_1_v2!E45` | =DIST_PHASE_1_v2!E45 |
| Ligne 56 | Col 5 | E56 | `=DIST_PHASE_1_v2!G45` | =DIST_PHASE_1_v2!G45 |
| Ligne 56 | Col 6 | F56 | `=DIST_PHASE_1_v2!L45` | =DIST_PHASE_1_v2!L45 |
| Ligne 56 | Col 7 | G56 | `=DIST_PHASE_1_v2!M45` | =DIST_PHASE_1_v2!M45 |
| Ligne 56 | Col 8 | H56 | `=DIST_PHASE_1_v2!N45` | =DIST_PHASE_1_v2!N45 |
| Ligne 56 | Col 9 | I56 | `= (10.679 * H56) / ((F56/1000)^4.871 * G56^1.852)` | = (10.679 * H56) / ((F56/1000)^4.871 * G56^1.852) |
| Ligne 56 | Col 10 | J56 | `=IF(C56="positif",E56,IF(C56="negatif",-E56,""))` | =IF(C56="positif",E56,IF(C56="negatif",-E56,"")) |
| Ligne 56 | Col 11 | K56 | `=IF(J56>0,I56*E56^1.852,-I56*E56^1.852)` | =IF(J56>0,I56*E56^1.852,-I56*E56^1.852) |
| Ligne 56 | Col 12 | L56 | `=1.852*I56*ABS(E56)^(1.852-1)` | =1.852*I56*ABS(E56)^(1.852-1) |
| Ligne 56 | Col 13 | M56 | `=J56+$D$93` | =J56+$D$93 |
| Ligne 56 | Col 16 | P56 | `=IFERROR(MATCH(S56,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S56,$D$22:$D$91,0),0) |
| Ligne 56 | Col 18 | R56 | `=DIST_PHASE_1_v2!Q45` | =DIST_PHASE_1_v2!Q45 |
| Ligne 56 | Col 19 | S56 | `=DIST_PHASE_1_v2!R45` | =DIST_PHASE_1_v2!R45 |
| Ligne 56 | Col 20 | T56 | `=DIST_PHASE_1_v2!T45` | =DIST_PHASE_1_v2!T45 |
| Ligne 56 | Col 21 | U56 | `=DIST_PHASE_1_v2!Y45` | =DIST_PHASE_1_v2!Y45 |
| Ligne 56 | Col 23 | W56 | `=DIST_PHASE_1_v2!AA45` | =DIST_PHASE_1_v2!AA45 |
| Ligne 56 | Col 24 | X56 | `= (10.679 * W56) / ((U56/1000)^4.871 * V56^1.852)` | = (10.679 * W56) / ((U56/1000)^4.871 * V56^1.852) |
| Ligne 56 | Col 25 | Y56 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996DB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996DB0> |
| Ligne 56 | Col 26 | Z56 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9966F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9966F0> |
| Ligne 56 | Col 27 | AA56 | `=IF(P56>0,
IF(R56="positif",1,-1),
0)` | =IF(P56>0,
IF(R56="positif",1,-1),
0) |
| Ligne 56 | Col 28 | AB56 | `=X56*SIGN(Y56)*ABS(Y56)^1.852` | =X56*SIGN(Y56)*ABS(Y56)^1.852 |
| Ligne 56 | Col 29 | AC56 | `=1.852*X56*ABS(Y56)^(1.852-1)` | =1.852*X56*ABS(Y56)^(1.852-1) |
| Ligne 56 | Col 30 | AD56 | `=IF(P56>0,
Y56+($D$93*Z56)+(AA56*$S$93),
Y56+$S$93)` | =IF(P56>0,
Y56+($D$93*Z56)+(AA56*$S$93),
Y56+$S$93) |
| Ligne 56 | Col 32 | AF56 | `=ABS(AD56)-ABS(Y56)` | =ABS(AD56)-ABS(Y56) |
| Ligne 56 | Col 36 | AJ56 | `=IFERROR(MATCH(AM56,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM56,$S$22:$S$91,0),0) |
| Ligne 56 | Col 38 | AL56 | `=TRONCONS_V2!AI43` | =TRONCONS_V2!AI43 |
| Ligne 56 | Col 39 | AM56 | `=TRONCONS_V2!AE43` | =TRONCONS_V2!AE43 |
| Ligne 56 | Col 40 | AN56 | `=DIST_PHASE_1_v2!AG45` | =DIST_PHASE_1_v2!AG45 |
| Ligne 56 | Col 41 | AO56 | `=DIST_PHASE_1_v2!AL45` | =DIST_PHASE_1_v2!AL45 |
| Ligne 56 | Col 43 | AQ56 | `=TRONCONS_V2!AG43` | =TRONCONS_V2!AG43 |
| Ligne 56 | Col 44 | AR56 | `= (10.679 * AQ56) / ((AO56/1000)^4.871 * AP56^1.852)` | = (10.679 * AQ56) / ((AO56/1000)^4.871 * AP56^1.852) |
| Ligne 56 | Col 45 | AS56 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996ED0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD996ED0> |
| Ligne 56 | Col 46 | AT56 | `=IF(AJ56>0,
IF(AS56>0, AR56*AS56^1.852,-AR56*ABS(AS56)^1.852),
IF(AS56>0, AR56*AN56^1.852, -AR56*AN56^1.852))` | =IF(AJ56>0,
IF(AS56>0, AR56*AS56^1.852,-AR56*ABS(AS56)^1.852),
IF(AS56>0, AR56*AN56^1.852, -AR56*AN56^1.852)) |
| Ligne 56 | Col 47 | AU56 | `=1.852*AR56*ABS(AS56)^(1.852-1)` | =1.852*AR56*ABS(AS56)^(1.852-1) |
| Ligne 56 | Col 48 | AV56 | `=AS56+$AN$60` | =AS56+$AN$60 |
| Ligne 56 | Col 52 | AZ56 | `=IFERROR(MATCH(BC56,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC56,$AM$22:$AM$57,0),0) |
| Ligne 56 | Col 54 | BB56 | `=DIST_PHASE_1_v2!AQ45` | =DIST_PHASE_1_v2!AQ45 |
| Ligne 56 | Col 55 | BC56 | `=DIST_PHASE_1_v2!AR45` | =DIST_PHASE_1_v2!AR45 |
| Ligne 56 | Col 56 | BD56 | `=DIST_PHASE_1_v2!AT45` | =DIST_PHASE_1_v2!AT45 |
| Ligne 56 | Col 57 | BE56 | `=DIST_PHASE_1_v2!AY45` | =DIST_PHASE_1_v2!AY45 |
| Ligne 56 | Col 58 | BF56 | `=DIST_PHASE_1_v2!AZ45` | =DIST_PHASE_1_v2!AZ45 |
| Ligne 56 | Col 59 | BG56 | `=DIST_PHASE_1_v2!BA45` | =DIST_PHASE_1_v2!BA45 |
| Ligne 56 | Col 60 | BH56 | `= (10.679 * BG56) / ((BE56/1000)^4.871 * BF56^1.852)` | = (10.679 * BG56) / ((BE56/1000)^4.871 * BF56^1.852) |
| Ligne 56 | Col 61 | BI56 | `=IF(BB56="positif",BD56,IF(BB56="negatif",-BD56,""))` | =IF(BB56="positif",BD56,IF(BB56="negatif",-BD56,"")) |
| Ligne 56 | Col 62 | BJ56 | `=IF(AZ56>0,
        IF(BI56>0, BH56*BI56^1.852,-BH56*ABS(BI56)^1.852),
        IF(BI56>0, BH56*BD56^1.852, -BH56*BD56^1.852))` | =IF(AZ56>0,
        IF(BI56>0, BH56*BI56^1.852,-BH56*ABS(BI56)^1.852),
        IF(BI56>0, BH56*BD56^1.852, -BH56*BD56^1.852)) |
| Ligne 56 | Col 63 | BK56 | `=1.852*BH56*ABS(BI56)^(1.852-1)` | =1.852*BH56*ABS(BI56)^(1.852-1) |
| Ligne 56 | Col 64 | BL56 | `=BI56+$BD$75` | =BI56+$BD$75 |
| Ligne 56 | Col 68 | BP56 | `=IFERROR(MATCH(BS56,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS56,$BC$22:$BC$73,0),0) |
| Ligne 56 | Col 70 | BR56 | `=DIST_PHASE_1_v2!BF45` | =DIST_PHASE_1_v2!BF45 |
| Ligne 56 | Col 71 | BS56 | `=DIST_PHASE_1_v2!BG45` | =DIST_PHASE_1_v2!BG45 |
| Ligne 56 | Col 72 | BT56 | `=DIST_PHASE_1_v2!BI45` | =DIST_PHASE_1_v2!BI45 |
| Ligne 56 | Col 73 | BU56 | `=DIST_PHASE_1_v2!BN45` | =DIST_PHASE_1_v2!BN45 |
| Ligne 56 | Col 74 | BV56 | `=DIST_PHASE_1_v2!BO45` | =DIST_PHASE_1_v2!BO45 |
| Ligne 56 | Col 75 | BW56 | `=DIST_PHASE_1_v2!BP45` | =DIST_PHASE_1_v2!BP45 |
| Ligne 56 | Col 76 | BX56 | `= (10.679 * BW56) / ((BU56/1000)^4.871 * BV56^1.852)` | = (10.679 * BW56) / ((BU56/1000)^4.871 * BV56^1.852) |
| Ligne 56 | Col 77 | BY56 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997050>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997050> |
| Ligne 56 | Col 78 | BZ56 | `=IF(BP56>0,
IF(BY56>0, BX56*BY56^1.852,-BX56*ABS(BY56)^1.852),
IF(BY56>0, BX56*BT56^1.852, -BX56*BT56^1.852))` | =IF(BP56>0,
IF(BY56>0, BX56*BY56^1.852,-BX56*ABS(BY56)^1.852),
IF(BY56>0, BX56*BT56^1.852, -BX56*BT56^1.852)) |
| Ligne 56 | Col 79 | CA56 | `=1.852*BX56*ABS(BY56)^(1.852-1)` | =1.852*BX56*ABS(BY56)^(1.852-1) |
| Ligne 56 | Col 80 | CB56 | `=BY56+$BT$64` | =BY56+$BT$64 |
| Ligne 56 | Col 84 | CF56 | `=IFERROR(MATCH(CI56,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI56,$BS$22:$BS$62,0),0) |
| Ligne 56 | Col 86 | CH56 | `=DIST_PHASE_1_v2!BS45` | =DIST_PHASE_1_v2!BS45 |
| Ligne 56 | Col 87 | CI56 | `=DIST_PHASE_1_v2!BT45` | =DIST_PHASE_1_v2!BT45 |
| Ligne 56 | Col 88 | CJ56 | `=DIST_PHASE_1_v2!BV45` | =DIST_PHASE_1_v2!BV45 |
| Ligne 56 | Col 89 | CK56 | `=DIST_PHASE_1_v2!CA45` | =DIST_PHASE_1_v2!CA45 |
| Ligne 56 | Col 91 | CM56 | `=DIST_PHASE_1_v2!CC45` | =DIST_PHASE_1_v2!CC45 |
| Ligne 56 | Col 92 | CN56 | `= (10.679 * CM56) / ((CK56/1000)^4.871 * CL56^1.852)` | = (10.679 * CM56) / ((CK56/1000)^4.871 * CL56^1.852) |
| Ligne 56 | Col 93 | CO56 | `=IF(CH56="positif",CJ56,IF(CH56="negatif",-CJ56,""))` | =IF(CH56="positif",CJ56,IF(CH56="negatif",-CJ56,"")) |
| Ligne 56 | Col 94 | CP56 | `=IF(CF56>0,
IF(CO56>0, CN56*CO56^1.852,-CN56*ABS(CO56)^1.852),
IF(CO56>0, CN56*CJ56^1.852, -CN56*CJ56^1.852))` | =IF(CF56>0,
IF(CO56>0, CN56*CO56^1.852,-CN56*ABS(CO56)^1.852),
IF(CO56>0, CN56*CJ56^1.852, -CN56*CJ56^1.852)) |
| Ligne 56 | Col 95 | CQ56 | `=1.852*CN56*ABS(CO56)^(1.852-1)` | =1.852*CN56*ABS(CO56)^(1.852-1) |
| Ligne 56 | Col 96 | CR56 | `=CO56+$CJ$71` | =CO56+$CJ$71 |
| Ligne 56 | Col 104 | CZ56 | `=-(DF55/DG55)` | =-(DF55/DG55) |
| Ligne 57 | Col 4 | D57 | `=DIST_PHASE_1_v2!E46` | =DIST_PHASE_1_v2!E46 |
| Ligne 57 | Col 5 | E57 | `=DIST_PHASE_1_v2!G46` | =DIST_PHASE_1_v2!G46 |
| Ligne 57 | Col 6 | F57 | `=DIST_PHASE_1_v2!L46` | =DIST_PHASE_1_v2!L46 |
| Ligne 57 | Col 7 | G57 | `=DIST_PHASE_1_v2!M46` | =DIST_PHASE_1_v2!M46 |
| Ligne 57 | Col 8 | H57 | `=DIST_PHASE_1_v2!N46` | =DIST_PHASE_1_v2!N46 |
| Ligne 57 | Col 9 | I57 | `= (10.679 * H57) / ((F57/1000)^4.871 * G57^1.852)` | = (10.679 * H57) / ((F57/1000)^4.871 * G57^1.852) |
| Ligne 57 | Col 10 | J57 | `=IF(C57="positif",E57,IF(C57="negatif",-E57,""))` | =IF(C57="positif",E57,IF(C57="negatif",-E57,"")) |
| Ligne 57 | Col 11 | K57 | `=IF(J57>0,I57*E57^1.852,-I57*E57^1.852)` | =IF(J57>0,I57*E57^1.852,-I57*E57^1.852) |
| Ligne 57 | Col 12 | L57 | `=1.852*I57*ABS(E57)^(1.852-1)` | =1.852*I57*ABS(E57)^(1.852-1) |
| Ligne 57 | Col 13 | M57 | `=J57+$D$93` | =J57+$D$93 |
| Ligne 57 | Col 16 | P57 | `=IFERROR(MATCH(S57,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S57,$D$22:$D$91,0),0) |
| Ligne 57 | Col 18 | R57 | `=DIST_PHASE_1_v2!Q46` | =DIST_PHASE_1_v2!Q46 |
| Ligne 57 | Col 19 | S57 | `=DIST_PHASE_1_v2!R46` | =DIST_PHASE_1_v2!R46 |
| Ligne 57 | Col 20 | T57 | `=DIST_PHASE_1_v2!T46` | =DIST_PHASE_1_v2!T46 |
| Ligne 57 | Col 21 | U57 | `=DIST_PHASE_1_v2!Y46` | =DIST_PHASE_1_v2!Y46 |
| Ligne 57 | Col 23 | W57 | `=DIST_PHASE_1_v2!AA46` | =DIST_PHASE_1_v2!AA46 |
| Ligne 57 | Col 24 | X57 | `= (10.679 * W57) / ((U57/1000)^4.871 * V57^1.852)` | = (10.679 * W57) / ((U57/1000)^4.871 * V57^1.852) |
| Ligne 57 | Col 25 | Y57 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997290>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997290> |
| Ligne 57 | Col 26 | Z57 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9967B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9967B0> |
| Ligne 57 | Col 27 | AA57 | `=IF(P57>0,
IF(R57="positif",1,-1),
0)` | =IF(P57>0,
IF(R57="positif",1,-1),
0) |
| Ligne 57 | Col 28 | AB57 | `=X57*SIGN(Y57)*ABS(Y57)^1.852` | =X57*SIGN(Y57)*ABS(Y57)^1.852 |
| Ligne 57 | Col 29 | AC57 | `=1.852*X57*ABS(Y57)^(1.852-1)` | =1.852*X57*ABS(Y57)^(1.852-1) |
| Ligne 57 | Col 30 | AD57 | `=IF(P57>0,
Y57+($D$93*Z57)+(AA57*$S$93),
Y57+$S$93)` | =IF(P57>0,
Y57+($D$93*Z57)+(AA57*$S$93),
Y57+$S$93) |
| Ligne 57 | Col 32 | AF57 | `=ABS(AD57)-ABS(Y57)` | =ABS(AD57)-ABS(Y57) |
| Ligne 57 | Col 36 | AJ57 | `=IFERROR(MATCH(AM57,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM57,$S$22:$S$91,0),0) |
| Ligne 57 | Col 38 | AL57 | `=TRONCONS_V2!AI44` | =TRONCONS_V2!AI44 |
| Ligne 57 | Col 39 | AM57 | `=TRONCONS_V2!AE44` | =TRONCONS_V2!AE44 |
| Ligne 57 | Col 40 | AN57 | `=DIST_PHASE_1_v2!AG46` | =DIST_PHASE_1_v2!AG46 |
| Ligne 57 | Col 41 | AO57 | `=DIST_PHASE_1_v2!AL46` | =DIST_PHASE_1_v2!AL46 |
| Ligne 57 | Col 43 | AQ57 | `=TRONCONS_V2!AG44` | =TRONCONS_V2!AG44 |
| Ligne 57 | Col 44 | AR57 | `= (10.679 * AQ57) / ((AO57/1000)^4.871 * AP57^1.852)` | = (10.679 * AQ57) / ((AO57/1000)^4.871 * AP57^1.852) |
| Ligne 57 | Col 45 | AS57 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9973B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9973B0> |
| Ligne 57 | Col 46 | AT57 | `=IF(AJ57>0,
IF(AS57>0, AR57*AS57^1.852,-AR57*ABS(AS57)^1.852),
IF(AS57>0, AR57*AN57^1.852, -AR57*AN57^1.852))` | =IF(AJ57>0,
IF(AS57>0, AR57*AS57^1.852,-AR57*ABS(AS57)^1.852),
IF(AS57>0, AR57*AN57^1.852, -AR57*AN57^1.852)) |
| Ligne 57 | Col 47 | AU57 | `=1.852*AR57*ABS(AS57)^(1.852-1)` | =1.852*AR57*ABS(AS57)^(1.852-1) |
| Ligne 57 | Col 48 | AV57 | `=AS57+$AN$60` | =AS57+$AN$60 |
| Ligne 57 | Col 52 | AZ57 | `=IFERROR(MATCH(BC57,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC57,$AM$22:$AM$57,0),0) |
| Ligne 57 | Col 54 | BB57 | `=DIST_PHASE_1_v2!AQ46` | =DIST_PHASE_1_v2!AQ46 |
| Ligne 57 | Col 55 | BC57 | `=DIST_PHASE_1_v2!AR46` | =DIST_PHASE_1_v2!AR46 |
| Ligne 57 | Col 56 | BD57 | `=DIST_PHASE_1_v2!AT46` | =DIST_PHASE_1_v2!AT46 |
| Ligne 57 | Col 57 | BE57 | `=DIST_PHASE_1_v2!AY46` | =DIST_PHASE_1_v2!AY46 |
| Ligne 57 | Col 58 | BF57 | `=DIST_PHASE_1_v2!AZ46` | =DIST_PHASE_1_v2!AZ46 |
| Ligne 57 | Col 59 | BG57 | `=DIST_PHASE_1_v2!BA46` | =DIST_PHASE_1_v2!BA46 |
| Ligne 57 | Col 60 | BH57 | `= (10.679 * BG57) / ((BE57/1000)^4.871 * BF57^1.852)` | = (10.679 * BG57) / ((BE57/1000)^4.871 * BF57^1.852) |
| Ligne 57 | Col 61 | BI57 | `=IF(BB57="positif",BD57,IF(BB57="negatif",-BD57,""))` | =IF(BB57="positif",BD57,IF(BB57="negatif",-BD57,"")) |
| Ligne 57 | Col 62 | BJ57 | `=IF(AZ57>0,
IF(BI57>0, BH57*BI57^1.852,-BH57*ABS(BI57)^1.852),
IF(BI57>0, BH57*BD57^1.852, -BH57*BD57^1.852))` | =IF(AZ57>0,
IF(BI57>0, BH57*BI57^1.852,-BH57*ABS(BI57)^1.852),
IF(BI57>0, BH57*BD57^1.852, -BH57*BD57^1.852)) |
| Ligne 57 | Col 63 | BK57 | `=1.852*BH57*ABS(BI57)^(1.852-1)` | =1.852*BH57*ABS(BI57)^(1.852-1) |
| Ligne 57 | Col 64 | BL57 | `=BI57+$BD$75` | =BI57+$BD$75 |
| Ligne 57 | Col 68 | BP57 | `=IFERROR(MATCH(BS57,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS57,$BC$22:$BC$73,0),0) |
| Ligne 57 | Col 70 | BR57 | `=DIST_PHASE_1_v2!BF46` | =DIST_PHASE_1_v2!BF46 |
| Ligne 57 | Col 71 | BS57 | `=DIST_PHASE_1_v2!BG46` | =DIST_PHASE_1_v2!BG46 |
| Ligne 57 | Col 72 | BT57 | `=DIST_PHASE_1_v2!BI46` | =DIST_PHASE_1_v2!BI46 |
| Ligne 57 | Col 73 | BU57 | `=DIST_PHASE_1_v2!BN46` | =DIST_PHASE_1_v2!BN46 |
| Ligne 57 | Col 74 | BV57 | `=DIST_PHASE_1_v2!BO46` | =DIST_PHASE_1_v2!BO46 |
| Ligne 57 | Col 75 | BW57 | `=DIST_PHASE_1_v2!BP46` | =DIST_PHASE_1_v2!BP46 |
| Ligne 57 | Col 76 | BX57 | `= (10.679 * BW57) / ((BU57/1000)^4.871 * BV57^1.852)` | = (10.679 * BW57) / ((BU57/1000)^4.871 * BV57^1.852) |
| Ligne 57 | Col 77 | BY57 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997530>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997530> |
| Ligne 57 | Col 78 | BZ57 | `=IF(BP57>0,
IF(BY57>0, BX57*BY57^1.852,-BX57*ABS(BY57)^1.852),
IF(BY57>0, BX57*BT57^1.852, -BX57*BT57^1.852))` | =IF(BP57>0,
IF(BY57>0, BX57*BY57^1.852,-BX57*ABS(BY57)^1.852),
IF(BY57>0, BX57*BT57^1.852, -BX57*BT57^1.852)) |
| Ligne 57 | Col 79 | CA57 | `=1.852*BX57*ABS(BY57)^(1.852-1)` | =1.852*BX57*ABS(BY57)^(1.852-1) |
| Ligne 57 | Col 80 | CB57 | `=BY57+$BT$64` | =BY57+$BT$64 |
| Ligne 57 | Col 84 | CF57 | `=IFERROR(MATCH(CI57,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI57,$BS$22:$BS$62,0),0) |
| Ligne 57 | Col 86 | CH57 | `=DIST_PHASE_1_v2!BS46` | =DIST_PHASE_1_v2!BS46 |
| Ligne 57 | Col 87 | CI57 | `=DIST_PHASE_1_v2!BT46` | =DIST_PHASE_1_v2!BT46 |
| Ligne 57 | Col 88 | CJ57 | `=DIST_PHASE_1_v2!BV46` | =DIST_PHASE_1_v2!BV46 |
| Ligne 57 | Col 89 | CK57 | `=DIST_PHASE_1_v2!CA46` | =DIST_PHASE_1_v2!CA46 |
| Ligne 57 | Col 91 | CM57 | `=DIST_PHASE_1_v2!CC46` | =DIST_PHASE_1_v2!CC46 |
| Ligne 57 | Col 92 | CN57 | `= (10.679 * CM57) / ((CK57/1000)^4.871 * CL57^1.852)` | = (10.679 * CM57) / ((CK57/1000)^4.871 * CL57^1.852) |
| Ligne 57 | Col 93 | CO57 | `=IF(CH57="positif",CJ57,IF(CH57="negatif",-CJ57,""))` | =IF(CH57="positif",CJ57,IF(CH57="negatif",-CJ57,"")) |
| Ligne 57 | Col 94 | CP57 | `=IF(CF57>0,
IF(CO57>0, CN57*CO57^1.852,-CN57*ABS(CO57)^1.852),
IF(CO57>0, CN57*CJ57^1.852, -CN57*CJ57^1.852))` | =IF(CF57>0,
IF(CO57>0, CN57*CO57^1.852,-CN57*ABS(CO57)^1.852),
IF(CO57>0, CN57*CJ57^1.852, -CN57*CJ57^1.852)) |
| Ligne 57 | Col 95 | CQ57 | `=1.852*CN57*ABS(CO57)^(1.852-1)` | =1.852*CN57*ABS(CO57)^(1.852-1) |
| Ligne 57 | Col 96 | CR57 | `=CO57+$CJ$71` | =CO57+$CJ$71 |
| Ligne 58 | Col 4 | D58 | `=DIST_PHASE_1_v2!E47` | =DIST_PHASE_1_v2!E47 |
| Ligne 58 | Col 5 | E58 | `=DIST_PHASE_1_v2!G47` | =DIST_PHASE_1_v2!G47 |
| Ligne 58 | Col 6 | F58 | `=DIST_PHASE_1_v2!L47` | =DIST_PHASE_1_v2!L47 |
| Ligne 58 | Col 7 | G58 | `=DIST_PHASE_1_v2!M47` | =DIST_PHASE_1_v2!M47 |
| Ligne 58 | Col 8 | H58 | `=DIST_PHASE_1_v2!N47` | =DIST_PHASE_1_v2!N47 |
| Ligne 58 | Col 9 | I58 | `= (10.679 * H58) / ((F58/1000)^4.871 * G58^1.852)` | = (10.679 * H58) / ((F58/1000)^4.871 * G58^1.852) |
| Ligne 58 | Col 10 | J58 | `=IF(C58="positif",E58,IF(C58="negatif",-E58,""))` | =IF(C58="positif",E58,IF(C58="negatif",-E58,"")) |
| Ligne 58 | Col 11 | K58 | `=IF(J58>0,I58*E58^1.852,-I58*E58^1.852)` | =IF(J58>0,I58*E58^1.852,-I58*E58^1.852) |
| Ligne 58 | Col 12 | L58 | `=1.852*I58*ABS(E58)^(1.852-1)` | =1.852*I58*ABS(E58)^(1.852-1) |
| Ligne 58 | Col 13 | M58 | `=J58+$D$93` | =J58+$D$93 |
| Ligne 58 | Col 16 | P58 | `=IFERROR(MATCH(S58,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S58,$D$22:$D$91,0),0) |
| Ligne 58 | Col 18 | R58 | `=DIST_PHASE_1_v2!Q47` | =DIST_PHASE_1_v2!Q47 |
| Ligne 58 | Col 19 | S58 | `=DIST_PHASE_1_v2!R47` | =DIST_PHASE_1_v2!R47 |
| Ligne 58 | Col 20 | T58 | `=DIST_PHASE_1_v2!T47` | =DIST_PHASE_1_v2!T47 |
| Ligne 58 | Col 21 | U58 | `=DIST_PHASE_1_v2!Y47` | =DIST_PHASE_1_v2!Y47 |
| Ligne 58 | Col 23 | W58 | `=DIST_PHASE_1_v2!AA47` | =DIST_PHASE_1_v2!AA47 |
| Ligne 58 | Col 24 | X58 | `= (10.679 * W58) / ((U58/1000)^4.871 * V58^1.852)` | = (10.679 * W58) / ((U58/1000)^4.871 * V58^1.852) |
| Ligne 58 | Col 25 | Y58 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9978F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9978F0> |
| Ligne 58 | Col 26 | Z58 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997650>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997650> |
| Ligne 58 | Col 27 | AA58 | `=IF(P58>0,
IF(R58="positif",1,-1),
0)` | =IF(P58>0,
IF(R58="positif",1,-1),
0) |
| Ligne 58 | Col 28 | AB58 | `=X58*SIGN(Y58)*ABS(Y58)^1.852` | =X58*SIGN(Y58)*ABS(Y58)^1.852 |
| Ligne 58 | Col 29 | AC58 | `=1.852*X58*ABS(Y58)^(1.852-1)` | =1.852*X58*ABS(Y58)^(1.852-1) |
| Ligne 58 | Col 30 | AD58 | `=IF(P58>0,
Y58+($D$93*Z58)+(AA58*$S$93),
Y58+$S$93)` | =IF(P58>0,
Y58+($D$93*Z58)+(AA58*$S$93),
Y58+$S$93) |
| Ligne 58 | Col 32 | AF58 | `=ABS(AD58)-ABS(Y58)` | =ABS(AD58)-ABS(Y58) |
| Ligne 58 | Col 36 | AJ58 | `=IFERROR(MATCH(AM58,$S$22:$S$91,0),0)` | =IFERROR(MATCH(AM58,$S$22:$S$91,0),0) |
| Ligne 58 | Col 38 | AL58 | `=TRONCONS_V2!AI45` | =TRONCONS_V2!AI45 |
| Ligne 58 | Col 39 | AM58 | `=TRONCONS_V2!AE45` | =TRONCONS_V2!AE45 |
| Ligne 58 | Col 40 | AN58 | `=DIST_PHASE_1_v2!AG47` | =DIST_PHASE_1_v2!AG47 |
| Ligne 58 | Col 41 | AO58 | `=DIST_PHASE_1_v2!AL47` | =DIST_PHASE_1_v2!AL47 |
| Ligne 58 | Col 43 | AQ58 | `=TRONCONS_V2!AG45` | =TRONCONS_V2!AG45 |
| Ligne 58 | Col 44 | AR58 | `= (10.679 * AQ58) / ((AO58/1000)^4.871 * AP58^1.852)` | = (10.679 * AQ58) / ((AO58/1000)^4.871 * AP58^1.852) |
| Ligne 58 | Col 45 | AS58 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997A10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997A10> |
| Ligne 58 | Col 46 | AT58 | `=IF(AJ58>0,
IF(AS58>0, AR58*AS58^1.852,-AR58*ABS(AS58)^1.852),
IF(AS58>0, AR58*AN58^1.852, -AR58*AN58^1.852))` | =IF(AJ58>0,
IF(AS58>0, AR58*AS58^1.852,-AR58*ABS(AS58)^1.852),
IF(AS58>0, AR58*AN58^1.852, -AR58*AN58^1.852)) |
| Ligne 58 | Col 47 | AU58 | `=1.852*AR58*ABS(AS58)^(1.852-1)` | =1.852*AR58*ABS(AS58)^(1.852-1) |
| Ligne 58 | Col 48 | AV58 | `=AS58+$AN$60` | =AS58+$AN$60 |
| Ligne 58 | Col 52 | AZ58 | `=IFERROR(MATCH(BC58,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC58,$AM$22:$AM$57,0),0) |
| Ligne 58 | Col 54 | BB58 | `=DIST_PHASE_1_v2!AQ47` | =DIST_PHASE_1_v2!AQ47 |
| Ligne 58 | Col 55 | BC58 | `=DIST_PHASE_1_v2!AR47` | =DIST_PHASE_1_v2!AR47 |
| Ligne 58 | Col 56 | BD58 | `=DIST_PHASE_1_v2!AT47` | =DIST_PHASE_1_v2!AT47 |
| Ligne 58 | Col 57 | BE58 | `=DIST_PHASE_1_v2!AY47` | =DIST_PHASE_1_v2!AY47 |
| Ligne 58 | Col 58 | BF58 | `=DIST_PHASE_1_v2!AZ47` | =DIST_PHASE_1_v2!AZ47 |
| Ligne 58 | Col 59 | BG58 | `=DIST_PHASE_1_v2!BA47` | =DIST_PHASE_1_v2!BA47 |
| Ligne 58 | Col 60 | BH58 | `= (10.679 * BG58) / ((BE58/1000)^4.871 * BF58^1.852)` | = (10.679 * BG58) / ((BE58/1000)^4.871 * BF58^1.852) |
| Ligne 58 | Col 61 | BI58 | `=IF(BB58="positif",BD58,IF(BB58="negatif",-BD58,""))` | =IF(BB58="positif",BD58,IF(BB58="negatif",-BD58,"")) |
| Ligne 58 | Col 62 | BJ58 | `=IF(AZ58>0,
IF(BI58>0, BH58*BI58^1.852,-BH58*ABS(BI58)^1.852),
IF(BI58>0, BH58*BD58^1.852, -BH58*BD58^1.852))` | =IF(AZ58>0,
IF(BI58>0, BH58*BI58^1.852,-BH58*ABS(BI58)^1.852),
IF(BI58>0, BH58*BD58^1.852, -BH58*BD58^1.852)) |
| Ligne 58 | Col 63 | BK58 | `=1.852*BH58*ABS(BI58)^(1.852-1)` | =1.852*BH58*ABS(BI58)^(1.852-1) |
| Ligne 58 | Col 64 | BL58 | `=BI58+$BD$75` | =BI58+$BD$75 |
| Ligne 58 | Col 68 | BP58 | `=IFERROR(MATCH(BS58,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS58,$BC$22:$BC$73,0),0) |
| Ligne 58 | Col 70 | BR58 | `=DIST_PHASE_1_v2!BF47` | =DIST_PHASE_1_v2!BF47 |
| Ligne 58 | Col 71 | BS58 | `=DIST_PHASE_1_v2!BG47` | =DIST_PHASE_1_v2!BG47 |
| Ligne 58 | Col 72 | BT58 | `=DIST_PHASE_1_v2!BI47` | =DIST_PHASE_1_v2!BI47 |
| Ligne 58 | Col 73 | BU58 | `=DIST_PHASE_1_v2!BN47` | =DIST_PHASE_1_v2!BN47 |
| Ligne 58 | Col 74 | BV58 | `=DIST_PHASE_1_v2!BO47` | =DIST_PHASE_1_v2!BO47 |
| Ligne 58 | Col 75 | BW58 | `=DIST_PHASE_1_v2!BP47` | =DIST_PHASE_1_v2!BP47 |
| Ligne 58 | Col 76 | BX58 | `= (10.679 * BW58) / ((BU58/1000)^4.871 * BV58^1.852)` | = (10.679 * BW58) / ((BU58/1000)^4.871 * BV58^1.852) |
| Ligne 58 | Col 77 | BY58 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997B90>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997B90> |
| Ligne 58 | Col 78 | BZ58 | `=IF(BP58>0,
IF(BY58>0, BX58*BY58^1.852,-BX58*ABS(BY58)^1.852),
IF(BY58>0, BX58*BT58^1.852, -BX58*BT58^1.852))` | =IF(BP58>0,
IF(BY58>0, BX58*BY58^1.852,-BX58*ABS(BY58)^1.852),
IF(BY58>0, BX58*BT58^1.852, -BX58*BT58^1.852)) |
| Ligne 58 | Col 79 | CA58 | `=1.852*BX58*ABS(BY58)^(1.852-1)` | =1.852*BX58*ABS(BY58)^(1.852-1) |
| Ligne 58 | Col 80 | CB58 | `=BY58+$BT$64` | =BY58+$BT$64 |
| Ligne 58 | Col 84 | CF58 | `=IFERROR(MATCH(CI58,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI58,$BS$22:$BS$62,0),0) |
| Ligne 58 | Col 86 | CH58 | `=DIST_PHASE_1_v2!BS47` | =DIST_PHASE_1_v2!BS47 |
| Ligne 58 | Col 87 | CI58 | `=DIST_PHASE_1_v2!BT47` | =DIST_PHASE_1_v2!BT47 |
| Ligne 58 | Col 88 | CJ58 | `=DIST_PHASE_1_v2!BV47` | =DIST_PHASE_1_v2!BV47 |
| Ligne 58 | Col 89 | CK58 | `=DIST_PHASE_1_v2!CA47` | =DIST_PHASE_1_v2!CA47 |
| Ligne 58 | Col 91 | CM58 | `=DIST_PHASE_1_v2!CC47` | =DIST_PHASE_1_v2!CC47 |
| Ligne 58 | Col 92 | CN58 | `= (10.679 * CM58) / ((CK58/1000)^4.871 * CL58^1.852)` | = (10.679 * CM58) / ((CK58/1000)^4.871 * CL58^1.852) |
| Ligne 58 | Col 93 | CO58 | `=IF(CH58="positif",CJ58,IF(CH58="negatif",-CJ58,""))` | =IF(CH58="positif",CJ58,IF(CH58="negatif",-CJ58,"")) |
| Ligne 58 | Col 94 | CP58 | `=IF(CF58>0,
IF(CO58>0, CN58*CO58^1.852,-CN58*ABS(CO58)^1.852),
IF(CO58>0, CN58*CJ58^1.852, -CN58*CJ58^1.852))` | =IF(CF58>0,
IF(CO58>0, CN58*CO58^1.852,-CN58*ABS(CO58)^1.852),
IF(CO58>0, CN58*CJ58^1.852, -CN58*CJ58^1.852)) |
| Ligne 58 | Col 95 | CQ58 | `=1.852*CN58*ABS(CO58)^(1.852-1)` | =1.852*CN58*ABS(CO58)^(1.852-1) |
| Ligne 58 | Col 96 | CR58 | `=CO58+$CJ$71` | =CO58+$CJ$71 |
| Ligne 59 | Col 4 | D59 | `=DIST_PHASE_1_v2!E48` | =DIST_PHASE_1_v2!E48 |
| Ligne 59 | Col 5 | E59 | `=DIST_PHASE_1_v2!G48` | =DIST_PHASE_1_v2!G48 |
| Ligne 59 | Col 6 | F59 | `=DIST_PHASE_1_v2!L48` | =DIST_PHASE_1_v2!L48 |
| Ligne 59 | Col 7 | G59 | `=DIST_PHASE_1_v2!M48` | =DIST_PHASE_1_v2!M48 |
| Ligne 59 | Col 8 | H59 | `=DIST_PHASE_1_v2!N48` | =DIST_PHASE_1_v2!N48 |
| Ligne 59 | Col 9 | I59 | `= (10.679 * H59) / ((F59/1000)^4.871 * G59^1.852)` | = (10.679 * H59) / ((F59/1000)^4.871 * G59^1.852) |
| Ligne 59 | Col 10 | J59 | `=IF(C59="positif",E59,IF(C59="negatif",-E59,""))` | =IF(C59="positif",E59,IF(C59="negatif",-E59,"")) |
| Ligne 59 | Col 11 | K59 | `=IF(J59>0,I59*E59^1.852,-I59*E59^1.852)` | =IF(J59>0,I59*E59^1.852,-I59*E59^1.852) |
| Ligne 59 | Col 12 | L59 | `=1.852*I59*ABS(E59)^(1.852-1)` | =1.852*I59*ABS(E59)^(1.852-1) |
| Ligne 59 | Col 13 | M59 | `=J59+$D$93` | =J59+$D$93 |
| Ligne 59 | Col 16 | P59 | `=IFERROR(MATCH(S59,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S59,$D$22:$D$91,0),0) |
| Ligne 59 | Col 18 | R59 | `=DIST_PHASE_1_v2!Q48` | =DIST_PHASE_1_v2!Q48 |
| Ligne 59 | Col 19 | S59 | `=DIST_PHASE_1_v2!R48` | =DIST_PHASE_1_v2!R48 |
| Ligne 59 | Col 20 | T59 | `=DIST_PHASE_1_v2!T48` | =DIST_PHASE_1_v2!T48 |
| Ligne 59 | Col 21 | U59 | `=DIST_PHASE_1_v2!Y48` | =DIST_PHASE_1_v2!Y48 |
| Ligne 59 | Col 23 | W59 | `=DIST_PHASE_1_v2!AA48` | =DIST_PHASE_1_v2!AA48 |
| Ligne 59 | Col 24 | X59 | `= (10.679 * W59) / ((U59/1000)^4.871 * V59^1.852)` | = (10.679 * W59) / ((U59/1000)^4.871 * V59^1.852) |
| Ligne 59 | Col 25 | Y59 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997DD0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997DD0> |
| Ligne 59 | Col 26 | Z59 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9976B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9976B0> |
| Ligne 59 | Col 27 | AA59 | `=IF(P59>0,
IF(R59="positif",1,-1),
0)` | =IF(P59>0,
IF(R59="positif",1,-1),
0) |
| Ligne 59 | Col 28 | AB59 | `=X59*SIGN(Y59)*ABS(Y59)^1.852` | =X59*SIGN(Y59)*ABS(Y59)^1.852 |
| Ligne 59 | Col 29 | AC59 | `=1.852*X59*ABS(Y59)^(1.852-1)` | =1.852*X59*ABS(Y59)^(1.852-1) |
| Ligne 59 | Col 30 | AD59 | `=IF(P59>0,
Y59+($D$93*Z59)+(AA59*$S$93),
Y59+$S$93)` | =IF(P59>0,
Y59+($D$93*Z59)+(AA59*$S$93),
Y59+$S$93) |
| Ligne 59 | Col 32 | AF59 | `=ABS(AD59)-ABS(Y59)` | =ABS(AD59)-ABS(Y59) |
| Ligne 59 | Col 36 | AJ59 | `=COUNTIF(AJ22:AJ58,">0")` | =COUNTIF(AJ22:AJ58,">0") |
| Ligne 59 | Col 46 | AT59 | `=SUM(AT22:AT58)` | =SUM(AT22:AT58) |
| Ligne 59 | Col 47 | AU59 | `=SUM(AU22:AU58)` | =SUM(AU22:AU58) |
| Ligne 59 | Col 52 | AZ59 | `=IFERROR(MATCH(BC59,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC59,$AM$22:$AM$57,0),0) |
| Ligne 59 | Col 54 | BB59 | `=DIST_PHASE_1_v2!AQ48` | =DIST_PHASE_1_v2!AQ48 |
| Ligne 59 | Col 55 | BC59 | `=DIST_PHASE_1_v2!AR48` | =DIST_PHASE_1_v2!AR48 |
| Ligne 59 | Col 56 | BD59 | `=DIST_PHASE_1_v2!AT48` | =DIST_PHASE_1_v2!AT48 |
| Ligne 59 | Col 57 | BE59 | `=DIST_PHASE_1_v2!AY48` | =DIST_PHASE_1_v2!AY48 |
| Ligne 59 | Col 58 | BF59 | `=DIST_PHASE_1_v2!AZ48` | =DIST_PHASE_1_v2!AZ48 |
| Ligne 59 | Col 59 | BG59 | `=DIST_PHASE_1_v2!BA48` | =DIST_PHASE_1_v2!BA48 |
| Ligne 59 | Col 60 | BH59 | `= (10.679 * BG59) / ((BE59/1000)^4.871 * BF59^1.852)` | = (10.679 * BG59) / ((BE59/1000)^4.871 * BF59^1.852) |
| Ligne 59 | Col 61 | BI59 | `=IF(BB59="positif",BD59,IF(BB59="negatif",-BD59,""))` | =IF(BB59="positif",BD59,IF(BB59="negatif",-BD59,"")) |
| Ligne 59 | Col 62 | BJ59 | `=IF(AZ59>0,
IF(BI59>0, BH59*BI59^1.852,-BH59*ABS(BI59)^1.852),
IF(BI59>0, BH59*BD59^1.852, -BH59*BD59^1.852))` | =IF(AZ59>0,
IF(BI59>0, BH59*BI59^1.852,-BH59*ABS(BI59)^1.852),
IF(BI59>0, BH59*BD59^1.852, -BH59*BD59^1.852)) |
| Ligne 59 | Col 63 | BK59 | `=1.852*BH59*ABS(BI59)^(1.852-1)` | =1.852*BH59*ABS(BI59)^(1.852-1) |
| Ligne 59 | Col 64 | BL59 | `=BI59+$BD$75` | =BI59+$BD$75 |
| Ligne 59 | Col 68 | BP59 | `=IFERROR(MATCH(BS59,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS59,$BC$22:$BC$73,0),0) |
| Ligne 59 | Col 70 | BR59 | `=DIST_PHASE_1_v2!BF48` | =DIST_PHASE_1_v2!BF48 |
| Ligne 59 | Col 71 | BS59 | `=DIST_PHASE_1_v2!BG48` | =DIST_PHASE_1_v2!BG48 |
| Ligne 59 | Col 72 | BT59 | `=DIST_PHASE_1_v2!BI48` | =DIST_PHASE_1_v2!BI48 |
| Ligne 59 | Col 73 | BU59 | `=DIST_PHASE_1_v2!BN48` | =DIST_PHASE_1_v2!BN48 |
| Ligne 59 | Col 74 | BV59 | `=DIST_PHASE_1_v2!BO48` | =DIST_PHASE_1_v2!BO48 |
| Ligne 59 | Col 75 | BW59 | `=DIST_PHASE_1_v2!BP48` | =DIST_PHASE_1_v2!BP48 |
| Ligne 59 | Col 76 | BX59 | `= (10.679 * BW59) / ((BU59/1000)^4.871 * BV59^1.852)` | = (10.679 * BW59) / ((BU59/1000)^4.871 * BV59^1.852) |
| Ligne 59 | Col 77 | BY59 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997FB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997FB0> |
| Ligne 59 | Col 78 | BZ59 | `=IF(BP59>0,
IF(BY59>0, BX59*BY59^1.852,-BX59*ABS(BY59)^1.852),
IF(BY59>0, BX59*BT59^1.852, -BX59*BT59^1.852))` | =IF(BP59>0,
IF(BY59>0, BX59*BY59^1.852,-BX59*ABS(BY59)^1.852),
IF(BY59>0, BX59*BT59^1.852, -BX59*BT59^1.852)) |
| Ligne 59 | Col 79 | CA59 | `=1.852*BX59*ABS(BY59)^(1.852-1)` | =1.852*BX59*ABS(BY59)^(1.852-1) |
| Ligne 59 | Col 80 | CB59 | `=BY59+$BT$64` | =BY59+$BT$64 |
| Ligne 59 | Col 84 | CF59 | `=IFERROR(MATCH(CI59,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI59,$BS$22:$BS$62,0),0) |
| Ligne 59 | Col 86 | CH59 | `=DIST_PHASE_1_v2!BS48` | =DIST_PHASE_1_v2!BS48 |
| Ligne 59 | Col 87 | CI59 | `=DIST_PHASE_1_v2!BT48` | =DIST_PHASE_1_v2!BT48 |
| Ligne 59 | Col 88 | CJ59 | `=DIST_PHASE_1_v2!BV48` | =DIST_PHASE_1_v2!BV48 |
| Ligne 59 | Col 89 | CK59 | `=DIST_PHASE_1_v2!CA48` | =DIST_PHASE_1_v2!CA48 |
| Ligne 59 | Col 91 | CM59 | `=DIST_PHASE_1_v2!CC48` | =DIST_PHASE_1_v2!CC48 |
| Ligne 59 | Col 92 | CN59 | `= (10.679 * CM59) / ((CK59/1000)^4.871 * CL59^1.852)` | = (10.679 * CM59) / ((CK59/1000)^4.871 * CL59^1.852) |
| Ligne 59 | Col 93 | CO59 | `=IF(CH59="positif",CJ59,IF(CH59="negatif",-CJ59,""))` | =IF(CH59="positif",CJ59,IF(CH59="negatif",-CJ59,"")) |
| Ligne 59 | Col 94 | CP59 | `=IF(CF59>0,
IF(CO59>0, CN59*CO59^1.852,-CN59*ABS(CO59)^1.852),
IF(CO59>0, CN59*CJ59^1.852, -CN59*CJ59^1.852))` | =IF(CF59>0,
IF(CO59>0, CN59*CO59^1.852,-CN59*ABS(CO59)^1.852),
IF(CO59>0, CN59*CJ59^1.852, -CN59*CJ59^1.852)) |
| Ligne 59 | Col 95 | CQ59 | `=1.852*CN59*ABS(CO59)^(1.852-1)` | =1.852*CN59*ABS(CO59)^(1.852-1) |
| Ligne 59 | Col 96 | CR59 | `=CO59+$CJ$71` | =CO59+$CJ$71 |
| Ligne 60 | Col 4 | D60 | `=DIST_PHASE_1_v2!E49` | =DIST_PHASE_1_v2!E49 |
| Ligne 60 | Col 5 | E60 | `=DIST_PHASE_1_v2!G49` | =DIST_PHASE_1_v2!G49 |
| Ligne 60 | Col 6 | F60 | `=DIST_PHASE_1_v2!L49` | =DIST_PHASE_1_v2!L49 |
| Ligne 60 | Col 7 | G60 | `=DIST_PHASE_1_v2!M49` | =DIST_PHASE_1_v2!M49 |
| Ligne 60 | Col 8 | H60 | `=DIST_PHASE_1_v2!N49` | =DIST_PHASE_1_v2!N49 |
| Ligne 60 | Col 9 | I60 | `= (10.679 * H60) / ((F60/1000)^4.871 * G60^1.852)` | = (10.679 * H60) / ((F60/1000)^4.871 * G60^1.852) |
| Ligne 60 | Col 10 | J60 | `=IF(C60="positif",E60,IF(C60="negatif",-E60,""))` | =IF(C60="positif",E60,IF(C60="negatif",-E60,"")) |
| Ligne 60 | Col 11 | K60 | `=IF(J60>0,I60*E60^1.852,-I60*E60^1.852)` | =IF(J60>0,I60*E60^1.852,-I60*E60^1.852) |
| Ligne 60 | Col 12 | L60 | `=1.852*I60*ABS(E60)^(1.852-1)` | =1.852*I60*ABS(E60)^(1.852-1) |
| Ligne 60 | Col 13 | M60 | `=J60+$D$93` | =J60+$D$93 |
| Ligne 60 | Col 16 | P60 | `=IFERROR(MATCH(S60,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S60,$D$22:$D$91,0),0) |
| Ligne 60 | Col 18 | R60 | `=DIST_PHASE_1_v2!Q49` | =DIST_PHASE_1_v2!Q49 |
| Ligne 60 | Col 19 | S60 | `=DIST_PHASE_1_v2!R49` | =DIST_PHASE_1_v2!R49 |
| Ligne 60 | Col 20 | T60 | `=DIST_PHASE_1_v2!T49` | =DIST_PHASE_1_v2!T49 |
| Ligne 60 | Col 21 | U60 | `=DIST_PHASE_1_v2!Y49` | =DIST_PHASE_1_v2!Y49 |
| Ligne 60 | Col 23 | W60 | `=DIST_PHASE_1_v2!AA49` | =DIST_PHASE_1_v2!AA49 |
| Ligne 60 | Col 24 | X60 | `= (10.679 * W60) / ((U60/1000)^4.871 * V60^1.852)` | = (10.679 * W60) / ((U60/1000)^4.871 * V60^1.852) |
| Ligne 60 | Col 25 | Y60 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8230>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8230> |
| Ligne 60 | Col 26 | Z60 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997710>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997710> |
| Ligne 60 | Col 27 | AA60 | `=IF(P60>0,
IF(R60="positif",1,-1),
0)` | =IF(P60>0,
IF(R60="positif",1,-1),
0) |
| Ligne 60 | Col 28 | AB60 | `=X60*SIGN(Y60)*ABS(Y60)^1.852` | =X60*SIGN(Y60)*ABS(Y60)^1.852 |
| Ligne 60 | Col 29 | AC60 | `=1.852*X60*ABS(Y60)^(1.852-1)` | =1.852*X60*ABS(Y60)^(1.852-1) |
| Ligne 60 | Col 30 | AD60 | `=IF(P60>0,
Y60+($D$93*Z60)+(AA60*$S$93),
Y60+$S$93)` | =IF(P60>0,
Y60+($D$93*Z60)+(AA60*$S$93),
Y60+$S$93) |
| Ligne 60 | Col 32 | AF60 | `=ABS(AD60)-ABS(Y60)` | =ABS(AD60)-ABS(Y60) |
| Ligne 60 | Col 40 | AN60 | `=-AT59/AU59` | =-AT59/AU59 |
| Ligne 60 | Col 52 | AZ60 | `=IFERROR(MATCH(BC60,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC60,$AM$22:$AM$57,0),0) |
| Ligne 60 | Col 54 | BB60 | `=DIST_PHASE_1_v2!AQ49` | =DIST_PHASE_1_v2!AQ49 |
| Ligne 60 | Col 55 | BC60 | `=DIST_PHASE_1_v2!AR49` | =DIST_PHASE_1_v2!AR49 |
| Ligne 60 | Col 56 | BD60 | `=DIST_PHASE_1_v2!AT49` | =DIST_PHASE_1_v2!AT49 |
| Ligne 60 | Col 57 | BE60 | `=DIST_PHASE_1_v2!AY49` | =DIST_PHASE_1_v2!AY49 |
| Ligne 60 | Col 58 | BF60 | `=DIST_PHASE_1_v2!AZ49` | =DIST_PHASE_1_v2!AZ49 |
| Ligne 60 | Col 59 | BG60 | `=DIST_PHASE_1_v2!BA49` | =DIST_PHASE_1_v2!BA49 |
| Ligne 60 | Col 60 | BH60 | `= (10.679 * BG60) / ((BE60/1000)^4.871 * BF60^1.852)` | = (10.679 * BG60) / ((BE60/1000)^4.871 * BF60^1.852) |
| Ligne 60 | Col 61 | BI60 | `=IF(BB60="positif",BD60,IF(BB60="negatif",-BD60,""))` | =IF(BB60="positif",BD60,IF(BB60="negatif",-BD60,"")) |
| Ligne 60 | Col 62 | BJ60 | `=IF(AZ60>0,
IF(BI60>0, BH60*BI60^1.852,-BH60*ABS(BI60)^1.852),
IF(BI60>0, BH60*BD60^1.852, -BH60*BD60^1.852))` | =IF(AZ60>0,
IF(BI60>0, BH60*BI60^1.852,-BH60*ABS(BI60)^1.852),
IF(BI60>0, BH60*BD60^1.852, -BH60*BD60^1.852)) |
| Ligne 60 | Col 63 | BK60 | `=1.852*BH60*ABS(BI60)^(1.852-1)` | =1.852*BH60*ABS(BI60)^(1.852-1) |
| Ligne 60 | Col 64 | BL60 | `=BI60+$BD$75` | =BI60+$BD$75 |
| Ligne 60 | Col 68 | BP60 | `=IFERROR(MATCH(BS60,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS60,$BC$22:$BC$73,0),0) |
| Ligne 60 | Col 70 | BR60 | `=DIST_PHASE_1_v2!BF49` | =DIST_PHASE_1_v2!BF49 |
| Ligne 60 | Col 71 | BS60 | `=DIST_PHASE_1_v2!BG49` | =DIST_PHASE_1_v2!BG49 |
| Ligne 60 | Col 72 | BT60 | `=DIST_PHASE_1_v2!BI49` | =DIST_PHASE_1_v2!BI49 |
| Ligne 60 | Col 73 | BU60 | `=DIST_PHASE_1_v2!BN49` | =DIST_PHASE_1_v2!BN49 |
| Ligne 60 | Col 74 | BV60 | `=DIST_PHASE_1_v2!BO49` | =DIST_PHASE_1_v2!BO49 |
| Ligne 60 | Col 75 | BW60 | `=DIST_PHASE_1_v2!BP49` | =DIST_PHASE_1_v2!BP49 |
| Ligne 60 | Col 76 | BX60 | `= (10.679 * BW60) / ((BU60/1000)^4.871 * BV60^1.852)` | = (10.679 * BW60) / ((BU60/1000)^4.871 * BV60^1.852) |
| Ligne 60 | Col 77 | BY60 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8410>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8410> |
| Ligne 60 | Col 78 | BZ60 | `=IF(BP60>0,
IF(BY60>0, BX60*BY60^1.852,-BX60*ABS(BY60)^1.852),
IF(BY60>0, BX60*BT60^1.852, -BX60*BT60^1.852))` | =IF(BP60>0,
IF(BY60>0, BX60*BY60^1.852,-BX60*ABS(BY60)^1.852),
IF(BY60>0, BX60*BT60^1.852, -BX60*BT60^1.852)) |
| Ligne 60 | Col 79 | CA60 | `=1.852*BX60*ABS(BY60)^(1.852-1)` | =1.852*BX60*ABS(BY60)^(1.852-1) |
| Ligne 60 | Col 80 | CB60 | `=BY60+$BT$64` | =BY60+$BT$64 |
| Ligne 60 | Col 84 | CF60 | `=IFERROR(MATCH(CI60,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI60,$BS$22:$BS$62,0),0) |
| Ligne 60 | Col 86 | CH60 | `=DIST_PHASE_1_v2!BS49` | =DIST_PHASE_1_v2!BS49 |
| Ligne 60 | Col 87 | CI60 | `=DIST_PHASE_1_v2!BT49` | =DIST_PHASE_1_v2!BT49 |
| Ligne 60 | Col 88 | CJ60 | `=DIST_PHASE_1_v2!BV49` | =DIST_PHASE_1_v2!BV49 |
| Ligne 60 | Col 89 | CK60 | `=DIST_PHASE_1_v2!CA49` | =DIST_PHASE_1_v2!CA49 |
| Ligne 60 | Col 91 | CM60 | `=DIST_PHASE_1_v2!CC49` | =DIST_PHASE_1_v2!CC49 |
| Ligne 60 | Col 92 | CN60 | `= (10.679 * CM60) / ((CK60/1000)^4.871 * CL60^1.852)` | = (10.679 * CM60) / ((CK60/1000)^4.871 * CL60^1.852) |
| Ligne 60 | Col 93 | CO60 | `=IF(CH60="positif",CJ60,IF(CH60="negatif",-CJ60,""))` | =IF(CH60="positif",CJ60,IF(CH60="negatif",-CJ60,"")) |
| Ligne 60 | Col 94 | CP60 | `=IF(CF60>0,
IF(CO60>0, CN60*CO60^1.852,-CN60*ABS(CO60)^1.852),
IF(CO60>0, CN60*CJ60^1.852, -CN60*CJ60^1.852))` | =IF(CF60>0,
IF(CO60>0, CN60*CO60^1.852,-CN60*ABS(CO60)^1.852),
IF(CO60>0, CN60*CJ60^1.852, -CN60*CJ60^1.852)) |
| Ligne 60 | Col 95 | CQ60 | `=1.852*CN60*ABS(CO60)^(1.852-1)` | =1.852*CN60*ABS(CO60)^(1.852-1) |
| Ligne 60 | Col 96 | CR60 | `=CO60+$CJ$71` | =CO60+$CJ$71 |
| Ligne 61 | Col 4 | D61 | `=DIST_PHASE_1_v2!E50` | =DIST_PHASE_1_v2!E50 |
| Ligne 61 | Col 5 | E61 | `=DIST_PHASE_1_v2!G50` | =DIST_PHASE_1_v2!G50 |
| Ligne 61 | Col 6 | F61 | `=DIST_PHASE_1_v2!L50` | =DIST_PHASE_1_v2!L50 |
| Ligne 61 | Col 7 | G61 | `=DIST_PHASE_1_v2!M50` | =DIST_PHASE_1_v2!M50 |
| Ligne 61 | Col 8 | H61 | `=DIST_PHASE_1_v2!N50` | =DIST_PHASE_1_v2!N50 |
| Ligne 61 | Col 9 | I61 | `= (10.679 * H61) / ((F61/1000)^4.871 * G61^1.852)` | = (10.679 * H61) / ((F61/1000)^4.871 * G61^1.852) |
| Ligne 61 | Col 10 | J61 | `=IF(C61="positif",E61,IF(C61="negatif",-E61,""))` | =IF(C61="positif",E61,IF(C61="negatif",-E61,"")) |
| Ligne 61 | Col 11 | K61 | `=IF(J61>0,I61*E61^1.852,-I61*E61^1.852)` | =IF(J61>0,I61*E61^1.852,-I61*E61^1.852) |
| Ligne 61 | Col 12 | L61 | `=1.852*I61*ABS(E61)^(1.852-1)` | =1.852*I61*ABS(E61)^(1.852-1) |
| Ligne 61 | Col 13 | M61 | `=J61+$D$93` | =J61+$D$93 |
| Ligne 61 | Col 16 | P61 | `=IFERROR(MATCH(S61,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S61,$D$22:$D$91,0),0) |
| Ligne 61 | Col 18 | R61 | `=DIST_PHASE_1_v2!Q50` | =DIST_PHASE_1_v2!Q50 |
| Ligne 61 | Col 19 | S61 | `=DIST_PHASE_1_v2!R50` | =DIST_PHASE_1_v2!R50 |
| Ligne 61 | Col 20 | T61 | `=DIST_PHASE_1_v2!T50` | =DIST_PHASE_1_v2!T50 |
| Ligne 61 | Col 21 | U61 | `=DIST_PHASE_1_v2!Y50` | =DIST_PHASE_1_v2!Y50 |
| Ligne 61 | Col 23 | W61 | `=DIST_PHASE_1_v2!AA50` | =DIST_PHASE_1_v2!AA50 |
| Ligne 61 | Col 24 | X61 | `= (10.679 * W61) / ((U61/1000)^4.871 * V61^1.852)` | = (10.679 * W61) / ((U61/1000)^4.871 * V61^1.852) |
| Ligne 61 | Col 25 | Y61 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F87D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F87D0> |
| Ligne 61 | Col 26 | Z61 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997770>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD997770> |
| Ligne 61 | Col 27 | AA61 | `=IF(P61>0,
IF(R61="positif",1,-1),
0)` | =IF(P61>0,
IF(R61="positif",1,-1),
0) |
| Ligne 61 | Col 28 | AB61 | `=X61*SIGN(Y61)*ABS(Y61)^1.852` | =X61*SIGN(Y61)*ABS(Y61)^1.852 |
| Ligne 61 | Col 29 | AC61 | `=1.852*X61*ABS(Y61)^(1.852-1)` | =1.852*X61*ABS(Y61)^(1.852-1) |
| Ligne 61 | Col 30 | AD61 | `=IF(P61>0,
Y61+($D$93*Z61)+(AA61*$S$93),
Y61+$S$93)` | =IF(P61>0,
Y61+($D$93*Z61)+(AA61*$S$93),
Y61+$S$93) |
| Ligne 61 | Col 32 | AF61 | `=ABS(AD61)-ABS(Y61)` | =ABS(AD61)-ABS(Y61) |
| Ligne 61 | Col 52 | AZ61 | `=IFERROR(MATCH(BC61,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC61,$AM$22:$AM$57,0),0) |
| Ligne 61 | Col 54 | BB61 | `=DIST_PHASE_1_v2!AQ50` | =DIST_PHASE_1_v2!AQ50 |
| Ligne 61 | Col 55 | BC61 | `=DIST_PHASE_1_v2!AR50` | =DIST_PHASE_1_v2!AR50 |
| Ligne 61 | Col 56 | BD61 | `=DIST_PHASE_1_v2!AT50` | =DIST_PHASE_1_v2!AT50 |
| Ligne 61 | Col 57 | BE61 | `=DIST_PHASE_1_v2!AY50` | =DIST_PHASE_1_v2!AY50 |
| Ligne 61 | Col 58 | BF61 | `=DIST_PHASE_1_v2!AZ50` | =DIST_PHASE_1_v2!AZ50 |
| Ligne 61 | Col 59 | BG61 | `=DIST_PHASE_1_v2!BA50` | =DIST_PHASE_1_v2!BA50 |
| Ligne 61 | Col 60 | BH61 | `= (10.679 * BG61) / ((BE61/1000)^4.871 * BF61^1.852)` | = (10.679 * BG61) / ((BE61/1000)^4.871 * BF61^1.852) |
| Ligne 61 | Col 61 | BI61 | `=IF(BB61="positif",BD61,IF(BB61="negatif",-BD61,""))` | =IF(BB61="positif",BD61,IF(BB61="negatif",-BD61,"")) |
| Ligne 61 | Col 62 | BJ61 | `=IF(AZ61>0,
IF(BI61>0, BH61*BI61^1.852,-BH61*ABS(BI61)^1.852),
IF(BI61>0, BH61*BD61^1.852, -BH61*BD61^1.852))` | =IF(AZ61>0,
IF(BI61>0, BH61*BI61^1.852,-BH61*ABS(BI61)^1.852),
IF(BI61>0, BH61*BD61^1.852, -BH61*BD61^1.852)) |
| Ligne 61 | Col 63 | BK61 | `=1.852*BH61*ABS(BI61)^(1.852-1)` | =1.852*BH61*ABS(BI61)^(1.852-1) |
| Ligne 61 | Col 64 | BL61 | `=BI61+$BD$75` | =BI61+$BD$75 |
| Ligne 61 | Col 68 | BP61 | `=IFERROR(MATCH(BS61,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS61,$BC$22:$BC$73,0),0) |
| Ligne 61 | Col 70 | BR61 | `=DIST_PHASE_1_v2!BF50` | =DIST_PHASE_1_v2!BF50 |
| Ligne 61 | Col 71 | BS61 | `=DIST_PHASE_1_v2!BG50` | =DIST_PHASE_1_v2!BG50 |
| Ligne 61 | Col 72 | BT61 | `=DIST_PHASE_1_v2!BI50` | =DIST_PHASE_1_v2!BI50 |
| Ligne 61 | Col 73 | BU61 | `=DIST_PHASE_1_v2!BN50` | =DIST_PHASE_1_v2!BN50 |
| Ligne 61 | Col 74 | BV61 | `=DIST_PHASE_1_v2!BO50` | =DIST_PHASE_1_v2!BO50 |
| Ligne 61 | Col 75 | BW61 | `=DIST_PHASE_1_v2!BP50` | =DIST_PHASE_1_v2!BP50 |
| Ligne 61 | Col 76 | BX61 | `= (10.679 * BW61) / ((BU61/1000)^4.871 * BV61^1.852)` | = (10.679 * BW61) / ((BU61/1000)^4.871 * BV61^1.852) |
| Ligne 61 | Col 77 | BY61 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F89B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F89B0> |
| Ligne 61 | Col 78 | BZ61 | `=IF(BP61>0,
IF(BY61>0, BX61*BY61^1.852,-BX61*ABS(BY61)^1.852),
IF(BY61>0, BX61*BT61^1.852, -BX61*BT61^1.852))` | =IF(BP61>0,
IF(BY61>0, BX61*BY61^1.852,-BX61*ABS(BY61)^1.852),
IF(BY61>0, BX61*BT61^1.852, -BX61*BT61^1.852)) |
| Ligne 61 | Col 79 | CA61 | `=1.852*BX61*ABS(BY61)^(1.852-1)` | =1.852*BX61*ABS(BY61)^(1.852-1) |
| Ligne 61 | Col 80 | CB61 | `=BY61+$BT$64` | =BY61+$BT$64 |
| Ligne 61 | Col 84 | CF61 | `=IFERROR(MATCH(CI61,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI61,$BS$22:$BS$62,0),0) |
| Ligne 61 | Col 86 | CH61 | `=DIST_PHASE_1_v2!BS50` | =DIST_PHASE_1_v2!BS50 |
| Ligne 61 | Col 87 | CI61 | `=DIST_PHASE_1_v2!BT50` | =DIST_PHASE_1_v2!BT50 |
| Ligne 61 | Col 88 | CJ61 | `=DIST_PHASE_1_v2!BV50` | =DIST_PHASE_1_v2!BV50 |
| Ligne 61 | Col 89 | CK61 | `=DIST_PHASE_1_v2!CA50` | =DIST_PHASE_1_v2!CA50 |
| Ligne 61 | Col 91 | CM61 | `=DIST_PHASE_1_v2!CC50` | =DIST_PHASE_1_v2!CC50 |
| Ligne 61 | Col 92 | CN61 | `= (10.679 * CM61) / ((CK61/1000)^4.871 * CL61^1.852)` | = (10.679 * CM61) / ((CK61/1000)^4.871 * CL61^1.852) |
| Ligne 61 | Col 93 | CO61 | `=IF(CH61="positif",CJ61,IF(CH61="negatif",-CJ61,""))` | =IF(CH61="positif",CJ61,IF(CH61="negatif",-CJ61,"")) |
| Ligne 61 | Col 94 | CP61 | `=IF(CF61>0,
IF(CO61>0, CN61*CO61^1.852,-CN61*ABS(CO61)^1.852),
IF(CO61>0, CN61*CJ61^1.852, -CN61*CJ61^1.852))` | =IF(CF61>0,
IF(CO61>0, CN61*CO61^1.852,-CN61*ABS(CO61)^1.852),
IF(CO61>0, CN61*CJ61^1.852, -CN61*CJ61^1.852)) |
| Ligne 61 | Col 95 | CQ61 | `=1.852*CN61*ABS(CO61)^(1.852-1)` | =1.852*CN61*ABS(CO61)^(1.852-1) |
| Ligne 61 | Col 96 | CR61 | `=CO61+$CJ$71` | =CO61+$CJ$71 |
| Ligne 62 | Col 4 | D62 | `=DIST_PHASE_1_v2!E51` | =DIST_PHASE_1_v2!E51 |
| Ligne 62 | Col 5 | E62 | `=DIST_PHASE_1_v2!G51` | =DIST_PHASE_1_v2!G51 |
| Ligne 62 | Col 6 | F62 | `=DIST_PHASE_1_v2!L51` | =DIST_PHASE_1_v2!L51 |
| Ligne 62 | Col 7 | G62 | `=DIST_PHASE_1_v2!M51` | =DIST_PHASE_1_v2!M51 |
| Ligne 62 | Col 8 | H62 | `=DIST_PHASE_1_v2!N51` | =DIST_PHASE_1_v2!N51 |
| Ligne 62 | Col 9 | I62 | `= (10.679 * H62) / ((F62/1000)^4.871 * G62^1.852)` | = (10.679 * H62) / ((F62/1000)^4.871 * G62^1.852) |
| Ligne 62 | Col 10 | J62 | `=IF(C62="positif",E62,IF(C62="negatif",-E62,""))` | =IF(C62="positif",E62,IF(C62="negatif",-E62,"")) |
| Ligne 62 | Col 11 | K62 | `=IF(J62>0,I62*E62^1.852,-I62*E62^1.852)` | =IF(J62>0,I62*E62^1.852,-I62*E62^1.852) |
| Ligne 62 | Col 12 | L62 | `=1.852*I62*ABS(E62)^(1.852-1)` | =1.852*I62*ABS(E62)^(1.852-1) |
| Ligne 62 | Col 13 | M62 | `=J62+$D$93` | =J62+$D$93 |
| Ligne 62 | Col 16 | P62 | `=IFERROR(MATCH(S62,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S62,$D$22:$D$91,0),0) |
| Ligne 62 | Col 18 | R62 | `=DIST_PHASE_1_v2!Q51` | =DIST_PHASE_1_v2!Q51 |
| Ligne 62 | Col 19 | S62 | `=DIST_PHASE_1_v2!R51` | =DIST_PHASE_1_v2!R51 |
| Ligne 62 | Col 20 | T62 | `=DIST_PHASE_1_v2!T51` | =DIST_PHASE_1_v2!T51 |
| Ligne 62 | Col 21 | U62 | `=DIST_PHASE_1_v2!Y51` | =DIST_PHASE_1_v2!Y51 |
| Ligne 62 | Col 23 | W62 | `=DIST_PHASE_1_v2!AA51` | =DIST_PHASE_1_v2!AA51 |
| Ligne 62 | Col 24 | X62 | `= (10.679 * W62) / ((U62/1000)^4.871 * V62^1.852)` | = (10.679 * W62) / ((U62/1000)^4.871 * V62^1.852) |
| Ligne 62 | Col 25 | Y62 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8BF0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8BF0> |
| Ligne 62 | Col 26 | Z62 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8530>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8530> |
| Ligne 62 | Col 27 | AA62 | `=IF(P62>0,
IF(R62="positif",1,-1),
0)` | =IF(P62>0,
IF(R62="positif",1,-1),
0) |
| Ligne 62 | Col 28 | AB62 | `=X62*SIGN(Y62)*ABS(Y62)^1.852` | =X62*SIGN(Y62)*ABS(Y62)^1.852 |
| Ligne 62 | Col 29 | AC62 | `=1.852*X62*ABS(Y62)^(1.852-1)` | =1.852*X62*ABS(Y62)^(1.852-1) |
| Ligne 62 | Col 30 | AD62 | `=IF(P62>0,
Y62+($D$93*Z62)+(AA62*$S$93),
Y62+$S$93)` | =IF(P62>0,
Y62+($D$93*Z62)+(AA62*$S$93),
Y62+$S$93) |
| Ligne 62 | Col 32 | AF62 | `=ABS(AD62)-ABS(Y62)` | =ABS(AD62)-ABS(Y62) |
| Ligne 62 | Col 52 | AZ62 | `=IFERROR(MATCH(BC62,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC62,$AM$22:$AM$57,0),0) |
| Ligne 62 | Col 54 | BB62 | `=DIST_PHASE_1_v2!AQ51` | =DIST_PHASE_1_v2!AQ51 |
| Ligne 62 | Col 55 | BC62 | `=DIST_PHASE_1_v2!AR51` | =DIST_PHASE_1_v2!AR51 |
| Ligne 62 | Col 56 | BD62 | `=DIST_PHASE_1_v2!AT51` | =DIST_PHASE_1_v2!AT51 |
| Ligne 62 | Col 57 | BE62 | `=DIST_PHASE_1_v2!AY51` | =DIST_PHASE_1_v2!AY51 |
| Ligne 62 | Col 58 | BF62 | `=DIST_PHASE_1_v2!AZ51` | =DIST_PHASE_1_v2!AZ51 |
| Ligne 62 | Col 59 | BG62 | `=DIST_PHASE_1_v2!BA51` | =DIST_PHASE_1_v2!BA51 |
| Ligne 62 | Col 60 | BH62 | `= (10.679 * BG62) / ((BE62/1000)^4.871 * BF62^1.852)` | = (10.679 * BG62) / ((BE62/1000)^4.871 * BF62^1.852) |
| Ligne 62 | Col 61 | BI62 | `=IF(BB62="positif",BD62,IF(BB62="negatif",-BD62,""))` | =IF(BB62="positif",BD62,IF(BB62="negatif",-BD62,"")) |
| Ligne 62 | Col 62 | BJ62 | `=IF(AZ62>0,
IF(BI62>0, BH62*BI62^1.852,-BH62*ABS(BI62)^1.852),
IF(BI62>0, BH62*BD62^1.852, -BH62*BD62^1.852))` | =IF(AZ62>0,
IF(BI62>0, BH62*BI62^1.852,-BH62*ABS(BI62)^1.852),
IF(BI62>0, BH62*BD62^1.852, -BH62*BD62^1.852)) |
| Ligne 62 | Col 63 | BK62 | `=1.852*BH62*ABS(BI62)^(1.852-1)` | =1.852*BH62*ABS(BI62)^(1.852-1) |
| Ligne 62 | Col 64 | BL62 | `=BI62+$BD$75` | =BI62+$BD$75 |
| Ligne 62 | Col 68 | BP62 | `=IFERROR(MATCH(BS62,$BC$22:$BC$73,0),0)` | =IFERROR(MATCH(BS62,$BC$22:$BC$73,0),0) |
| Ligne 62 | Col 70 | BR62 | `=DIST_PHASE_1_v2!BF51` | =DIST_PHASE_1_v2!BF51 |
| Ligne 62 | Col 71 | BS62 | `=DIST_PHASE_1_v2!BG51` | =DIST_PHASE_1_v2!BG51 |
| Ligne 62 | Col 72 | BT62 | `=DIST_PHASE_1_v2!BI51` | =DIST_PHASE_1_v2!BI51 |
| Ligne 62 | Col 73 | BU62 | `=DIST_PHASE_1_v2!BN51` | =DIST_PHASE_1_v2!BN51 |
| Ligne 62 | Col 74 | BV62 | `=DIST_PHASE_1_v2!BO51` | =DIST_PHASE_1_v2!BO51 |
| Ligne 62 | Col 75 | BW62 | `=DIST_PHASE_1_v2!BP51` | =DIST_PHASE_1_v2!BP51 |
| Ligne 62 | Col 76 | BX62 | `= (10.679 * BW62) / ((BU62/1000)^4.871 * BV62^1.852)` | = (10.679 * BW62) / ((BU62/1000)^4.871 * BV62^1.852) |
| Ligne 62 | Col 77 | BY62 | `=IF(BR62="positif",BT62,IF(BR62="negatif",-BT62,""))` | =IF(BR62="positif",BT62,IF(BR62="negatif",-BT62,"")) |
| Ligne 62 | Col 78 | BZ62 | `=IF(BP62>0,
IF(BY62>0, BX62*BY62^1.852,-BX62*ABS(BY62)^1.852),
IF(BY62>0, BX62*BT62^1.852, -BX62*BT62^1.852))` | =IF(BP62>0,
IF(BY62>0, BX62*BY62^1.852,-BX62*ABS(BY62)^1.852),
IF(BY62>0, BX62*BT62^1.852, -BX62*BT62^1.852)) |
| Ligne 62 | Col 79 | CA62 | `=1.852*BX62*ABS(BY62)^(1.852-1)` | =1.852*BX62*ABS(BY62)^(1.852-1) |
| Ligne 62 | Col 80 | CB62 | `=BY62+$BT$64` | =BY62+$BT$64 |
| Ligne 62 | Col 84 | CF62 | `=IFERROR(MATCH(CI62,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI62,$BS$22:$BS$62,0),0) |
| Ligne 62 | Col 86 | CH62 | `=DIST_PHASE_1_v2!BS51` | =DIST_PHASE_1_v2!BS51 |
| Ligne 62 | Col 87 | CI62 | `=DIST_PHASE_1_v2!BT51` | =DIST_PHASE_1_v2!BT51 |
| Ligne 62 | Col 88 | CJ62 | `=DIST_PHASE_1_v2!BV51` | =DIST_PHASE_1_v2!BV51 |
| Ligne 62 | Col 89 | CK62 | `=DIST_PHASE_1_v2!CA51` | =DIST_PHASE_1_v2!CA51 |
| Ligne 62 | Col 91 | CM62 | `=DIST_PHASE_1_v2!CC51` | =DIST_PHASE_1_v2!CC51 |
| Ligne 62 | Col 92 | CN62 | `= (10.679 * CM62) / ((CK62/1000)^4.871 * CL62^1.852)` | = (10.679 * CM62) / ((CK62/1000)^4.871 * CL62^1.852) |
| Ligne 62 | Col 93 | CO62 | `=IF(CH62="positif",CJ62,IF(CH62="negatif",-CJ62,""))` | =IF(CH62="positif",CJ62,IF(CH62="negatif",-CJ62,"")) |
| Ligne 62 | Col 94 | CP62 | `=IF(CF62>0,
IF(CO62>0, CN62*CO62^1.852,-CN62*ABS(CO62)^1.852),
IF(CO62>0, CN62*CJ62^1.852, -CN62*CJ62^1.852))` | =IF(CF62>0,
IF(CO62>0, CN62*CO62^1.852,-CN62*ABS(CO62)^1.852),
IF(CO62>0, CN62*CJ62^1.852, -CN62*CJ62^1.852)) |
| Ligne 62 | Col 95 | CQ62 | `=1.852*CN62*ABS(CO62)^(1.852-1)` | =1.852*CN62*ABS(CO62)^(1.852-1) |
| Ligne 62 | Col 96 | CR62 | `=CO62+$CJ$71` | =CO62+$CJ$71 |
| Ligne 63 | Col 4 | D63 | `=DIST_PHASE_1_v2!E52` | =DIST_PHASE_1_v2!E52 |
| Ligne 63 | Col 5 | E63 | `=DIST_PHASE_1_v2!G52` | =DIST_PHASE_1_v2!G52 |
| Ligne 63 | Col 6 | F63 | `=DIST_PHASE_1_v2!L52` | =DIST_PHASE_1_v2!L52 |
| Ligne 63 | Col 7 | G63 | `=DIST_PHASE_1_v2!M52` | =DIST_PHASE_1_v2!M52 |
| Ligne 63 | Col 8 | H63 | `=DIST_PHASE_1_v2!N52` | =DIST_PHASE_1_v2!N52 |
| Ligne 63 | Col 9 | I63 | `= (10.679 * H63) / ((F63/1000)^4.871 * G63^1.852)` | = (10.679 * H63) / ((F63/1000)^4.871 * G63^1.852) |
| Ligne 63 | Col 10 | J63 | `=IF(C63="positif",E63,IF(C63="negatif",-E63,""))` | =IF(C63="positif",E63,IF(C63="negatif",-E63,"")) |
| Ligne 63 | Col 11 | K63 | `=IF(J63>0,I63*E63^1.852,-I63*E63^1.852)` | =IF(J63>0,I63*E63^1.852,-I63*E63^1.852) |
| Ligne 63 | Col 12 | L63 | `=1.852*I63*ABS(E63)^(1.852-1)` | =1.852*I63*ABS(E63)^(1.852-1) |
| Ligne 63 | Col 13 | M63 | `=J63+$D$93` | =J63+$D$93 |
| Ligne 63 | Col 16 | P63 | `=IFERROR(MATCH(S63,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S63,$D$22:$D$91,0),0) |
| Ligne 63 | Col 18 | R63 | `=DIST_PHASE_1_v2!Q52` | =DIST_PHASE_1_v2!Q52 |
| Ligne 63 | Col 19 | S63 | `=DIST_PHASE_1_v2!R52` | =DIST_PHASE_1_v2!R52 |
| Ligne 63 | Col 20 | T63 | `=DIST_PHASE_1_v2!T52` | =DIST_PHASE_1_v2!T52 |
| Ligne 63 | Col 21 | U63 | `=DIST_PHASE_1_v2!Y52` | =DIST_PHASE_1_v2!Y52 |
| Ligne 63 | Col 23 | W63 | `=DIST_PHASE_1_v2!AA52` | =DIST_PHASE_1_v2!AA52 |
| Ligne 63 | Col 24 | X63 | `= (10.679 * W63) / ((U63/1000)^4.871 * V63^1.852)` | = (10.679 * W63) / ((U63/1000)^4.871 * V63^1.852) |
| Ligne 63 | Col 25 | Y63 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9010>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9010> |
| Ligne 63 | Col 26 | Z63 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8590>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8590> |
| Ligne 63 | Col 27 | AA63 | `=IF(P63>0,
IF(R63="positif",1,-1),
0)` | =IF(P63>0,
IF(R63="positif",1,-1),
0) |
| Ligne 63 | Col 28 | AB63 | `=X63*SIGN(Y63)*ABS(Y63)^1.852` | =X63*SIGN(Y63)*ABS(Y63)^1.852 |
| Ligne 63 | Col 29 | AC63 | `=1.852*X63*ABS(Y63)^(1.852-1)` | =1.852*X63*ABS(Y63)^(1.852-1) |
| Ligne 63 | Col 30 | AD63 | `=IF(P63>0,
Y63+($D$93*Z63)+(AA63*$S$93),
Y63+$S$93)` | =IF(P63>0,
Y63+($D$93*Z63)+(AA63*$S$93),
Y63+$S$93) |
| Ligne 63 | Col 32 | AF63 | `=ABS(AD63)-ABS(Y63)` | =ABS(AD63)-ABS(Y63) |
| Ligne 63 | Col 52 | AZ63 | `=IFERROR(MATCH(BC63,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC63,$AM$22:$AM$57,0),0) |
| Ligne 63 | Col 54 | BB63 | `=DIST_PHASE_1_v2!AQ52` | =DIST_PHASE_1_v2!AQ52 |
| Ligne 63 | Col 55 | BC63 | `=DIST_PHASE_1_v2!AR52` | =DIST_PHASE_1_v2!AR52 |
| Ligne 63 | Col 56 | BD63 | `=DIST_PHASE_1_v2!AT52` | =DIST_PHASE_1_v2!AT52 |
| Ligne 63 | Col 57 | BE63 | `=DIST_PHASE_1_v2!AY52` | =DIST_PHASE_1_v2!AY52 |
| Ligne 63 | Col 58 | BF63 | `=DIST_PHASE_1_v2!AZ52` | =DIST_PHASE_1_v2!AZ52 |
| Ligne 63 | Col 59 | BG63 | `=DIST_PHASE_1_v2!BA52` | =DIST_PHASE_1_v2!BA52 |
| Ligne 63 | Col 60 | BH63 | `= (10.679 * BG63) / ((BE63/1000)^4.871 * BF63^1.852)` | = (10.679 * BG63) / ((BE63/1000)^4.871 * BF63^1.852) |
| Ligne 63 | Col 61 | BI63 | `=IF(BB63="positif",BD63,IF(BB63="negatif",-BD63,""))` | =IF(BB63="positif",BD63,IF(BB63="negatif",-BD63,"")) |
| Ligne 63 | Col 62 | BJ63 | `=IF(AZ63>0,
IF(BI63>0, BH63*BI63^1.852,-BH63*ABS(BI63)^1.852),
IF(BI63>0, BH63*BD63^1.852, -BH63*BD63^1.852))` | =IF(AZ63>0,
IF(BI63>0, BH63*BI63^1.852,-BH63*ABS(BI63)^1.852),
IF(BI63>0, BH63*BD63^1.852, -BH63*BD63^1.852)) |
| Ligne 63 | Col 63 | BK63 | `=1.852*BH63*ABS(BI63)^(1.852-1)` | =1.852*BH63*ABS(BI63)^(1.852-1) |
| Ligne 63 | Col 64 | BL63 | `=BI63+$BD$75` | =BI63+$BD$75 |
| Ligne 63 | Col 78 | BZ63 | `=SUM(BZ22:BZ62)` | =SUM(BZ22:BZ62) |
| Ligne 63 | Col 79 | CA63 | `=SUM(CA22:CA62)` | =SUM(CA22:CA62) |
| Ligne 63 | Col 84 | CF63 | `=IFERROR(MATCH(CI63,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI63,$BS$22:$BS$62,0),0) |
| Ligne 63 | Col 86 | CH63 | `=DIST_PHASE_1_v2!BS52` | =DIST_PHASE_1_v2!BS52 |
| Ligne 63 | Col 87 | CI63 | `=DIST_PHASE_1_v2!BT52` | =DIST_PHASE_1_v2!BT52 |
| Ligne 63 | Col 88 | CJ63 | `=DIST_PHASE_1_v2!BV52` | =DIST_PHASE_1_v2!BV52 |
| Ligne 63 | Col 89 | CK63 | `=DIST_PHASE_1_v2!CA52` | =DIST_PHASE_1_v2!CA52 |
| Ligne 63 | Col 91 | CM63 | `=DIST_PHASE_1_v2!CC52` | =DIST_PHASE_1_v2!CC52 |
| Ligne 63 | Col 92 | CN63 | `= (10.679 * CM63) / ((CK63/1000)^4.871 * CL63^1.852)` | = (10.679 * CM63) / ((CK63/1000)^4.871 * CL63^1.852) |
| Ligne 63 | Col 93 | CO63 | `=IF(CH63="positif",CJ63,IF(CH63="negatif",-CJ63,""))` | =IF(CH63="positif",CJ63,IF(CH63="negatif",-CJ63,"")) |
| Ligne 63 | Col 94 | CP63 | `=IF(CF63>0,
IF(CO63>0, CN63*CO63^1.852,-CN63*ABS(CO63)^1.852),
IF(CO63>0, CN63*CJ63^1.852, -CN63*CJ63^1.852))` | =IF(CF63>0,
IF(CO63>0, CN63*CO63^1.852,-CN63*ABS(CO63)^1.852),
IF(CO63>0, CN63*CJ63^1.852, -CN63*CJ63^1.852)) |
| Ligne 63 | Col 95 | CQ63 | `=1.852*CN63*ABS(CO63)^(1.852-1)` | =1.852*CN63*ABS(CO63)^(1.852-1) |
| Ligne 63 | Col 96 | CR63 | `=CO63+$CJ$71` | =CO63+$CJ$71 |
| Ligne 64 | Col 4 | D64 | `=DIST_PHASE_1_v2!E53` | =DIST_PHASE_1_v2!E53 |
| Ligne 64 | Col 5 | E64 | `=DIST_PHASE_1_v2!G53` | =DIST_PHASE_1_v2!G53 |
| Ligne 64 | Col 6 | F64 | `=DIST_PHASE_1_v2!L53` | =DIST_PHASE_1_v2!L53 |
| Ligne 64 | Col 7 | G64 | `=DIST_PHASE_1_v2!M53` | =DIST_PHASE_1_v2!M53 |
| Ligne 64 | Col 8 | H64 | `=DIST_PHASE_1_v2!N53` | =DIST_PHASE_1_v2!N53 |
| Ligne 64 | Col 9 | I64 | `= (10.679 * H64) / ((F64/1000)^4.871 * G64^1.852)` | = (10.679 * H64) / ((F64/1000)^4.871 * G64^1.852) |
| Ligne 64 | Col 10 | J64 | `=IF(C64="positif",E64,IF(C64="negatif",-E64,""))` | =IF(C64="positif",E64,IF(C64="negatif",-E64,"")) |
| Ligne 64 | Col 11 | K64 | `=IF(J64>0,I64*E64^1.852,-I64*E64^1.852)` | =IF(J64>0,I64*E64^1.852,-I64*E64^1.852) |
| Ligne 64 | Col 12 | L64 | `=1.852*I64*ABS(E64)^(1.852-1)` | =1.852*I64*ABS(E64)^(1.852-1) |
| Ligne 64 | Col 13 | M64 | `=J64+$D$93` | =J64+$D$93 |
| Ligne 64 | Col 16 | P64 | `=IFERROR(MATCH(S64,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S64,$D$22:$D$91,0),0) |
| Ligne 64 | Col 18 | R64 | `=DIST_PHASE_1_v2!Q53` | =DIST_PHASE_1_v2!Q53 |
| Ligne 64 | Col 19 | S64 | `=DIST_PHASE_1_v2!R53` | =DIST_PHASE_1_v2!R53 |
| Ligne 64 | Col 20 | T64 | `=DIST_PHASE_1_v2!T53` | =DIST_PHASE_1_v2!T53 |
| Ligne 64 | Col 21 | U64 | `=DIST_PHASE_1_v2!Y53` | =DIST_PHASE_1_v2!Y53 |
| Ligne 64 | Col 23 | W64 | `=DIST_PHASE_1_v2!AA53` | =DIST_PHASE_1_v2!AA53 |
| Ligne 64 | Col 24 | X64 | `= (10.679 * W64) / ((U64/1000)^4.871 * V64^1.852)` | = (10.679 * W64) / ((U64/1000)^4.871 * V64^1.852) |
| Ligne 64 | Col 25 | Y64 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9370>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9370> |
| Ligne 64 | Col 26 | Z64 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F85F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F85F0> |
| Ligne 64 | Col 27 | AA64 | `=IF(P64>0,
IF(R64="positif",1,-1),
0)` | =IF(P64>0,
IF(R64="positif",1,-1),
0) |
| Ligne 64 | Col 28 | AB64 | `=X64*SIGN(Y64)*ABS(Y64)^1.852` | =X64*SIGN(Y64)*ABS(Y64)^1.852 |
| Ligne 64 | Col 29 | AC64 | `=1.852*X64*ABS(Y64)^(1.852-1)` | =1.852*X64*ABS(Y64)^(1.852-1) |
| Ligne 64 | Col 30 | AD64 | `=IF(P64>0,
Y64+($D$93*Z64)+(AA64*$S$93),
Y64+$S$93)` | =IF(P64>0,
Y64+($D$93*Z64)+(AA64*$S$93),
Y64+$S$93) |
| Ligne 64 | Col 32 | AF64 | `=ABS(AD64)-ABS(Y64)` | =ABS(AD64)-ABS(Y64) |
| Ligne 64 | Col 52 | AZ64 | `=IFERROR(MATCH(BC64,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC64,$AM$22:$AM$57,0),0) |
| Ligne 64 | Col 54 | BB64 | `=DIST_PHASE_1_v2!AQ53` | =DIST_PHASE_1_v2!AQ53 |
| Ligne 64 | Col 55 | BC64 | `=DIST_PHASE_1_v2!AR53` | =DIST_PHASE_1_v2!AR53 |
| Ligne 64 | Col 56 | BD64 | `=DIST_PHASE_1_v2!AT53` | =DIST_PHASE_1_v2!AT53 |
| Ligne 64 | Col 57 | BE64 | `=DIST_PHASE_1_v2!AY53` | =DIST_PHASE_1_v2!AY53 |
| Ligne 64 | Col 58 | BF64 | `=DIST_PHASE_1_v2!AZ53` | =DIST_PHASE_1_v2!AZ53 |
| Ligne 64 | Col 59 | BG64 | `=DIST_PHASE_1_v2!BA53` | =DIST_PHASE_1_v2!BA53 |
| Ligne 64 | Col 60 | BH64 | `= (10.679 * BG64) / ((BE64/1000)^4.871 * BF64^1.852)` | = (10.679 * BG64) / ((BE64/1000)^4.871 * BF64^1.852) |
| Ligne 64 | Col 61 | BI64 | `=IF(BB64="positif",BD64,IF(BB64="negatif",-BD64,""))` | =IF(BB64="positif",BD64,IF(BB64="negatif",-BD64,"")) |
| Ligne 64 | Col 62 | BJ64 | `=IF(AZ64>0,
IF(BI64>0, BH64*BI64^1.852,-BH64*ABS(BI64)^1.852),
IF(BI64>0, BH64*BD64^1.852, -BH64*BD64^1.852))` | =IF(AZ64>0,
IF(BI64>0, BH64*BI64^1.852,-BH64*ABS(BI64)^1.852),
IF(BI64>0, BH64*BD64^1.852, -BH64*BD64^1.852)) |
| Ligne 64 | Col 63 | BK64 | `=1.852*BH64*ABS(BI64)^(1.852-1)` | =1.852*BH64*ABS(BI64)^(1.852-1) |
| Ligne 64 | Col 64 | BL64 | `=BI64+$BD$75` | =BI64+$BD$75 |
| Ligne 64 | Col 72 | BT64 | `=-(BZ63/CA63)` | =-(BZ63/CA63) |
| Ligne 64 | Col 84 | CF64 | `=IFERROR(MATCH(CI64,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI64,$BS$22:$BS$62,0),0) |
| Ligne 64 | Col 86 | CH64 | `=DIST_PHASE_1_v2!BS53` | =DIST_PHASE_1_v2!BS53 |
| Ligne 64 | Col 87 | CI64 | `=DIST_PHASE_1_v2!BT53` | =DIST_PHASE_1_v2!BT53 |
| Ligne 64 | Col 88 | CJ64 | `=DIST_PHASE_1_v2!BV53` | =DIST_PHASE_1_v2!BV53 |
| Ligne 64 | Col 89 | CK64 | `=DIST_PHASE_1_v2!CA53` | =DIST_PHASE_1_v2!CA53 |
| Ligne 64 | Col 91 | CM64 | `=DIST_PHASE_1_v2!CC53` | =DIST_PHASE_1_v2!CC53 |
| Ligne 64 | Col 92 | CN64 | `= (10.679 * CM64) / ((CK64/1000)^4.871 * CL64^1.852)` | = (10.679 * CM64) / ((CK64/1000)^4.871 * CL64^1.852) |
| Ligne 64 | Col 93 | CO64 | `=IF(CH64="positif",CJ64,IF(CH64="negatif",-CJ64,""))` | =IF(CH64="positif",CJ64,IF(CH64="negatif",-CJ64,"")) |
| Ligne 64 | Col 94 | CP64 | `=IF(CF64>0,
IF(CO64>0, CN64*CO64^1.852,-CN64*ABS(CO64)^1.852),
IF(CO64>0, CN64*CJ64^1.852, -CN64*CJ64^1.852))` | =IF(CF64>0,
IF(CO64>0, CN64*CO64^1.852,-CN64*ABS(CO64)^1.852),
IF(CO64>0, CN64*CJ64^1.852, -CN64*CJ64^1.852)) |
| Ligne 64 | Col 95 | CQ64 | `=1.852*CN64*ABS(CO64)^(1.852-1)` | =1.852*CN64*ABS(CO64)^(1.852-1) |
| Ligne 64 | Col 96 | CR64 | `=CO64+$CJ$71` | =CO64+$CJ$71 |
| Ligne 65 | Col 4 | D65 | `=DIST_PHASE_1_v2!E54` | =DIST_PHASE_1_v2!E54 |
| Ligne 65 | Col 5 | E65 | `=DIST_PHASE_1_v2!G54` | =DIST_PHASE_1_v2!G54 |
| Ligne 65 | Col 6 | F65 | `=DIST_PHASE_1_v2!L54` | =DIST_PHASE_1_v2!L54 |
| Ligne 65 | Col 7 | G65 | `=DIST_PHASE_1_v2!M54` | =DIST_PHASE_1_v2!M54 |
| Ligne 65 | Col 8 | H65 | `=DIST_PHASE_1_v2!N54` | =DIST_PHASE_1_v2!N54 |
| Ligne 65 | Col 9 | I65 | `= (10.679 * H65) / ((F65/1000)^4.871 * G65^1.852)` | = (10.679 * H65) / ((F65/1000)^4.871 * G65^1.852) |
| Ligne 65 | Col 10 | J65 | `=IF(C65="positif",E65,IF(C65="negatif",-E65,""))` | =IF(C65="positif",E65,IF(C65="negatif",-E65,"")) |
| Ligne 65 | Col 11 | K65 | `=IF(J65>0,I65*E65^1.852,-I65*E65^1.852)` | =IF(J65>0,I65*E65^1.852,-I65*E65^1.852) |
| Ligne 65 | Col 12 | L65 | `=1.852*I65*ABS(E65)^(1.852-1)` | =1.852*I65*ABS(E65)^(1.852-1) |
| Ligne 65 | Col 13 | M65 | `=J65+$D$93` | =J65+$D$93 |
| Ligne 65 | Col 16 | P65 | `=IFERROR(MATCH(S65,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S65,$D$22:$D$91,0),0) |
| Ligne 65 | Col 18 | R65 | `=DIST_PHASE_1_v2!Q54` | =DIST_PHASE_1_v2!Q54 |
| Ligne 65 | Col 19 | S65 | `=DIST_PHASE_1_v2!R54` | =DIST_PHASE_1_v2!R54 |
| Ligne 65 | Col 20 | T65 | `=DIST_PHASE_1_v2!T54` | =DIST_PHASE_1_v2!T54 |
| Ligne 65 | Col 21 | U65 | `=DIST_PHASE_1_v2!Y54` | =DIST_PHASE_1_v2!Y54 |
| Ligne 65 | Col 23 | W65 | `=DIST_PHASE_1_v2!AA54` | =DIST_PHASE_1_v2!AA54 |
| Ligne 65 | Col 24 | X65 | `= (10.679 * W65) / ((U65/1000)^4.871 * V65^1.852)` | = (10.679 * W65) / ((U65/1000)^4.871 * V65^1.852) |
| Ligne 65 | Col 25 | Y65 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9850>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9850> |
| Ligne 65 | Col 26 | Z65 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8650>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F8650> |
| Ligne 65 | Col 27 | AA65 | `=IF(P65>0,
IF(R65="positif",1,-1),
0)` | =IF(P65>0,
IF(R65="positif",1,-1),
0) |
| Ligne 65 | Col 28 | AB65 | `=X65*SIGN(Y65)*ABS(Y65)^1.852` | =X65*SIGN(Y65)*ABS(Y65)^1.852 |
| Ligne 65 | Col 29 | AC65 | `=1.852*X65*ABS(Y65)^(1.852-1)` | =1.852*X65*ABS(Y65)^(1.852-1) |
| Ligne 65 | Col 30 | AD65 | `=IF(P65>0,
Y65+($D$93*Z65)+(AA65*$S$93),
Y65+$S$93)` | =IF(P65>0,
Y65+($D$93*Z65)+(AA65*$S$93),
Y65+$S$93) |
| Ligne 65 | Col 32 | AF65 | `=ABS(AD65)-ABS(Y65)` | =ABS(AD65)-ABS(Y65) |
| Ligne 65 | Col 52 | AZ65 | `=IFERROR(MATCH(BC65,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC65,$AM$22:$AM$57,0),0) |
| Ligne 65 | Col 54 | BB65 | `=DIST_PHASE_1_v2!AQ54` | =DIST_PHASE_1_v2!AQ54 |
| Ligne 65 | Col 55 | BC65 | `=DIST_PHASE_1_v2!AR54` | =DIST_PHASE_1_v2!AR54 |
| Ligne 65 | Col 56 | BD65 | `=DIST_PHASE_1_v2!AT54` | =DIST_PHASE_1_v2!AT54 |
| Ligne 65 | Col 57 | BE65 | `=DIST_PHASE_1_v2!AY54` | =DIST_PHASE_1_v2!AY54 |
| Ligne 65 | Col 58 | BF65 | `=DIST_PHASE_1_v2!AZ54` | =DIST_PHASE_1_v2!AZ54 |
| Ligne 65 | Col 59 | BG65 | `=DIST_PHASE_1_v2!BA54` | =DIST_PHASE_1_v2!BA54 |
| Ligne 65 | Col 60 | BH65 | `= (10.679 * BG65) / ((BE65/1000)^4.871 * BF65^1.852)` | = (10.679 * BG65) / ((BE65/1000)^4.871 * BF65^1.852) |
| Ligne 65 | Col 61 | BI65 | `=IF(BB65="positif",BD65,IF(BB65="negatif",-BD65,""))` | =IF(BB65="positif",BD65,IF(BB65="negatif",-BD65,"")) |
| Ligne 65 | Col 62 | BJ65 | `=IF(AZ65>0,
IF(BI65>0, BH65*BI65^1.852,-BH65*ABS(BI65)^1.852),
IF(BI65>0, BH65*BD65^1.852, -BH65*BD65^1.852))` | =IF(AZ65>0,
IF(BI65>0, BH65*BI65^1.852,-BH65*ABS(BI65)^1.852),
IF(BI65>0, BH65*BD65^1.852, -BH65*BD65^1.852)) |
| Ligne 65 | Col 63 | BK65 | `=1.852*BH65*ABS(BI65)^(1.852-1)` | =1.852*BH65*ABS(BI65)^(1.852-1) |
| Ligne 65 | Col 64 | BL65 | `=BI65+$BD$75` | =BI65+$BD$75 |
| Ligne 65 | Col 84 | CF65 | `=IFERROR(MATCH(CI65,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI65,$BS$22:$BS$62,0),0) |
| Ligne 65 | Col 86 | CH65 | `=DIST_PHASE_1_v2!BS54` | =DIST_PHASE_1_v2!BS54 |
| Ligne 65 | Col 87 | CI65 | `=DIST_PHASE_1_v2!BT54` | =DIST_PHASE_1_v2!BT54 |
| Ligne 65 | Col 88 | CJ65 | `=DIST_PHASE_1_v2!BV54` | =DIST_PHASE_1_v2!BV54 |
| Ligne 65 | Col 89 | CK65 | `=DIST_PHASE_1_v2!CA54` | =DIST_PHASE_1_v2!CA54 |
| Ligne 65 | Col 91 | CM65 | `=DIST_PHASE_1_v2!CC54` | =DIST_PHASE_1_v2!CC54 |
| Ligne 65 | Col 92 | CN65 | `= (10.679 * CM65) / ((CK65/1000)^4.871 * CL65^1.852)` | = (10.679 * CM65) / ((CK65/1000)^4.871 * CL65^1.852) |
| Ligne 65 | Col 93 | CO65 | `=IF(CH65="positif",CJ65,IF(CH65="negatif",-CJ65,""))` | =IF(CH65="positif",CJ65,IF(CH65="negatif",-CJ65,"")) |
| Ligne 65 | Col 94 | CP65 | `=IF(CF65>0,
IF(CO65>0, CN65*CO65^1.852,-CN65*ABS(CO65)^1.852),
IF(CO65>0, CN65*CJ65^1.852, -CN65*CJ65^1.852))` | =IF(CF65>0,
IF(CO65>0, CN65*CO65^1.852,-CN65*ABS(CO65)^1.852),
IF(CO65>0, CN65*CJ65^1.852, -CN65*CJ65^1.852)) |
| Ligne 65 | Col 95 | CQ65 | `=1.852*CN65*ABS(CO65)^(1.852-1)` | =1.852*CN65*ABS(CO65)^(1.852-1) |
| Ligne 65 | Col 96 | CR65 | `=CO65+$CJ$71` | =CO65+$CJ$71 |
| Ligne 66 | Col 4 | D66 | `=DIST_PHASE_1_v2!E55` | =DIST_PHASE_1_v2!E55 |
| Ligne 66 | Col 5 | E66 | `=DIST_PHASE_1_v2!G55` | =DIST_PHASE_1_v2!G55 |
| Ligne 66 | Col 6 | F66 | `=DIST_PHASE_1_v2!L55` | =DIST_PHASE_1_v2!L55 |
| Ligne 66 | Col 7 | G66 | `=DIST_PHASE_1_v2!M55` | =DIST_PHASE_1_v2!M55 |
| Ligne 66 | Col 8 | H66 | `=DIST_PHASE_1_v2!N55` | =DIST_PHASE_1_v2!N55 |
| Ligne 66 | Col 9 | I66 | `= (10.679 * H66) / ((F66/1000)^4.871 * G66^1.852)` | = (10.679 * H66) / ((F66/1000)^4.871 * G66^1.852) |
| Ligne 66 | Col 10 | J66 | `=IF(C66="positif",E66,IF(C66="negatif",-E66,""))` | =IF(C66="positif",E66,IF(C66="negatif",-E66,"")) |
| Ligne 66 | Col 11 | K66 | `=IF(J66>0,I66*E66^1.852,-I66*E66^1.852)` | =IF(J66>0,I66*E66^1.852,-I66*E66^1.852) |
| Ligne 66 | Col 12 | L66 | `=1.852*I66*ABS(E66)^(1.852-1)` | =1.852*I66*ABS(E66)^(1.852-1) |
| Ligne 66 | Col 13 | M66 | `=J66+$D$93` | =J66+$D$93 |
| Ligne 66 | Col 16 | P66 | `=IFERROR(MATCH(S66,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S66,$D$22:$D$91,0),0) |
| Ligne 66 | Col 18 | R66 | `=DIST_PHASE_1_v2!Q55` | =DIST_PHASE_1_v2!Q55 |
| Ligne 66 | Col 19 | S66 | `=DIST_PHASE_1_v2!R55` | =DIST_PHASE_1_v2!R55 |
| Ligne 66 | Col 20 | T66 | `=DIST_PHASE_1_v2!T55` | =DIST_PHASE_1_v2!T55 |
| Ligne 66 | Col 21 | U66 | `=DIST_PHASE_1_v2!Y55` | =DIST_PHASE_1_v2!Y55 |
| Ligne 66 | Col 23 | W66 | `=DIST_PHASE_1_v2!AA55` | =DIST_PHASE_1_v2!AA55 |
| Ligne 66 | Col 24 | X66 | `= (10.679 * W66) / ((U66/1000)^4.871 * V66^1.852)` | = (10.679 * W66) / ((U66/1000)^4.871 * V66^1.852) |
| Ligne 66 | Col 25 | Y66 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9BB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9BB0> |
| Ligne 66 | Col 26 | Z66 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F93D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F93D0> |
| Ligne 66 | Col 27 | AA66 | `=IF(P66>0,
IF(R66="positif",1,-1),
0)` | =IF(P66>0,
IF(R66="positif",1,-1),
0) |
| Ligne 66 | Col 28 | AB66 | `=X66*SIGN(Y66)*ABS(Y66)^1.852` | =X66*SIGN(Y66)*ABS(Y66)^1.852 |
| Ligne 66 | Col 29 | AC66 | `=1.852*X66*ABS(Y66)^(1.852-1)` | =1.852*X66*ABS(Y66)^(1.852-1) |
| Ligne 66 | Col 30 | AD66 | `=IF(P66>0,
Y66+($D$93*Z66)+(AA66*$S$93),
Y66+$S$93)` | =IF(P66>0,
Y66+($D$93*Z66)+(AA66*$S$93),
Y66+$S$93) |
| Ligne 66 | Col 32 | AF66 | `=ABS(AD66)-ABS(Y66)` | =ABS(AD66)-ABS(Y66) |
| Ligne 66 | Col 52 | AZ66 | `=IFERROR(MATCH(BC66,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC66,$AM$22:$AM$57,0),0) |
| Ligne 66 | Col 54 | BB66 | `=DIST_PHASE_1_v2!AQ55` | =DIST_PHASE_1_v2!AQ55 |
| Ligne 66 | Col 55 | BC66 | `=DIST_PHASE_1_v2!AR55` | =DIST_PHASE_1_v2!AR55 |
| Ligne 66 | Col 56 | BD66 | `=DIST_PHASE_1_v2!AT55` | =DIST_PHASE_1_v2!AT55 |
| Ligne 66 | Col 57 | BE66 | `=DIST_PHASE_1_v2!AY55` | =DIST_PHASE_1_v2!AY55 |
| Ligne 66 | Col 58 | BF66 | `=DIST_PHASE_1_v2!AZ55` | =DIST_PHASE_1_v2!AZ55 |
| Ligne 66 | Col 59 | BG66 | `=DIST_PHASE_1_v2!BA55` | =DIST_PHASE_1_v2!BA55 |
| Ligne 66 | Col 60 | BH66 | `= (10.679 * BG66) / ((BE66/1000)^4.871 * BF66^1.852)` | = (10.679 * BG66) / ((BE66/1000)^4.871 * BF66^1.852) |
| Ligne 66 | Col 61 | BI66 | `=IF(BB66="positif",BD66,IF(BB66="negatif",-BD66,""))` | =IF(BB66="positif",BD66,IF(BB66="negatif",-BD66,"")) |
| Ligne 66 | Col 62 | BJ66 | `=IF(AZ66>0,
IF(BI66>0, BH66*BI66^1.852,-BH66*ABS(BI66)^1.852),
IF(BI66>0, BH66*BD66^1.852, -BH66*BD66^1.852))` | =IF(AZ66>0,
IF(BI66>0, BH66*BI66^1.852,-BH66*ABS(BI66)^1.852),
IF(BI66>0, BH66*BD66^1.852, -BH66*BD66^1.852)) |
| Ligne 66 | Col 63 | BK66 | `=1.852*BH66*ABS(BI66)^(1.852-1)` | =1.852*BH66*ABS(BI66)^(1.852-1) |
| Ligne 66 | Col 64 | BL66 | `=BI66+$BD$75` | =BI66+$BD$75 |
| Ligne 66 | Col 84 | CF66 | `=IFERROR(MATCH(CI66,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI66,$BS$22:$BS$62,0),0) |
| Ligne 66 | Col 86 | CH66 | `=DIST_PHASE_1_v2!BS55` | =DIST_PHASE_1_v2!BS55 |
| Ligne 66 | Col 87 | CI66 | `=DIST_PHASE_1_v2!BT55` | =DIST_PHASE_1_v2!BT55 |
| Ligne 66 | Col 88 | CJ66 | `=DIST_PHASE_1_v2!BV55` | =DIST_PHASE_1_v2!BV55 |
| Ligne 66 | Col 89 | CK66 | `=DIST_PHASE_1_v2!CA55` | =DIST_PHASE_1_v2!CA55 |
| Ligne 66 | Col 91 | CM66 | `=DIST_PHASE_1_v2!CC55` | =DIST_PHASE_1_v2!CC55 |
| Ligne 66 | Col 92 | CN66 | `= (10.679 * CM66) / ((CK66/1000)^4.871 * CL66^1.852)` | = (10.679 * CM66) / ((CK66/1000)^4.871 * CL66^1.852) |
| Ligne 66 | Col 93 | CO66 | `=IF(CH66="positif",CJ66,IF(CH66="negatif",-CJ66,""))` | =IF(CH66="positif",CJ66,IF(CH66="negatif",-CJ66,"")) |
| Ligne 66 | Col 94 | CP66 | `=IF(CF66>0,
IF(CO66>0, CN66*CO66^1.852,-CN66*ABS(CO66)^1.852),
IF(CO66>0, CN66*CJ66^1.852, -CN66*CJ66^1.852))` | =IF(CF66>0,
IF(CO66>0, CN66*CO66^1.852,-CN66*ABS(CO66)^1.852),
IF(CO66>0, CN66*CJ66^1.852, -CN66*CJ66^1.852)) |
| Ligne 66 | Col 95 | CQ66 | `=1.852*CN66*ABS(CO66)^(1.852-1)` | =1.852*CN66*ABS(CO66)^(1.852-1) |
| Ligne 66 | Col 96 | CR66 | `=CO66+$CJ$71` | =CO66+$CJ$71 |
| Ligne 67 | Col 4 | D67 | `=DIST_PHASE_1_v2!E56` | =DIST_PHASE_1_v2!E56 |
| Ligne 67 | Col 5 | E67 | `=DIST_PHASE_1_v2!G56` | =DIST_PHASE_1_v2!G56 |
| Ligne 67 | Col 6 | F67 | `=DIST_PHASE_1_v2!L56` | =DIST_PHASE_1_v2!L56 |
| Ligne 67 | Col 7 | G67 | `=DIST_PHASE_1_v2!M56` | =DIST_PHASE_1_v2!M56 |
| Ligne 67 | Col 8 | H67 | `=DIST_PHASE_1_v2!N56` | =DIST_PHASE_1_v2!N56 |
| Ligne 67 | Col 9 | I67 | `= (10.679 * H67) / ((F67/1000)^4.871 * G67^1.852)` | = (10.679 * H67) / ((F67/1000)^4.871 * G67^1.852) |
| Ligne 67 | Col 10 | J67 | `=IF(C67="positif",E67,IF(C67="negatif",-E67,""))` | =IF(C67="positif",E67,IF(C67="negatif",-E67,"")) |
| Ligne 67 | Col 11 | K67 | `=IF(J67>0,I67*E67^1.852,-I67*E67^1.852)` | =IF(J67>0,I67*E67^1.852,-I67*E67^1.852) |
| Ligne 67 | Col 12 | L67 | `=1.852*I67*ABS(E67)^(1.852-1)` | =1.852*I67*ABS(E67)^(1.852-1) |
| Ligne 67 | Col 13 | M67 | `=J67+$D$93` | =J67+$D$93 |
| Ligne 67 | Col 16 | P67 | `=IFERROR(MATCH(S67,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S67,$D$22:$D$91,0),0) |
| Ligne 67 | Col 18 | R67 | `=DIST_PHASE_1_v2!Q56` | =DIST_PHASE_1_v2!Q56 |
| Ligne 67 | Col 19 | S67 | `=DIST_PHASE_1_v2!R56` | =DIST_PHASE_1_v2!R56 |
| Ligne 67 | Col 20 | T67 | `=DIST_PHASE_1_v2!T56` | =DIST_PHASE_1_v2!T56 |
| Ligne 67 | Col 21 | U67 | `=DIST_PHASE_1_v2!Y56` | =DIST_PHASE_1_v2!Y56 |
| Ligne 67 | Col 23 | W67 | `=DIST_PHASE_1_v2!AA56` | =DIST_PHASE_1_v2!AA56 |
| Ligne 67 | Col 24 | X67 | `= (10.679 * W67) / ((U67/1000)^4.871 * V67^1.852)` | = (10.679 * W67) / ((U67/1000)^4.871 * V67^1.852) |
| Ligne 67 | Col 25 | Y67 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9F10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9F10> |
| Ligne 67 | Col 26 | Z67 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9610>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9610> |
| Ligne 67 | Col 27 | AA67 | `=IF(P67>0,
IF(R67="positif",1,-1),
0)` | =IF(P67>0,
IF(R67="positif",1,-1),
0) |
| Ligne 67 | Col 28 | AB67 | `=X67*SIGN(Y67)*ABS(Y67)^1.852` | =X67*SIGN(Y67)*ABS(Y67)^1.852 |
| Ligne 67 | Col 29 | AC67 | `=1.852*X67*ABS(Y67)^(1.852-1)` | =1.852*X67*ABS(Y67)^(1.852-1) |
| Ligne 67 | Col 30 | AD67 | `=IF(P67>0,
Y67+($D$93*Z67)+(AA67*$S$93),
Y67+$S$93)` | =IF(P67>0,
Y67+($D$93*Z67)+(AA67*$S$93),
Y67+$S$93) |
| Ligne 67 | Col 32 | AF67 | `=ABS(AD67)-ABS(Y67)` | =ABS(AD67)-ABS(Y67) |
| Ligne 67 | Col 52 | AZ67 | `=IFERROR(MATCH(BC67,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC67,$AM$22:$AM$57,0),0) |
| Ligne 67 | Col 54 | BB67 | `=DIST_PHASE_1_v2!AQ56` | =DIST_PHASE_1_v2!AQ56 |
| Ligne 67 | Col 55 | BC67 | `=DIST_PHASE_1_v2!AR56` | =DIST_PHASE_1_v2!AR56 |
| Ligne 67 | Col 56 | BD67 | `=DIST_PHASE_1_v2!AT56` | =DIST_PHASE_1_v2!AT56 |
| Ligne 67 | Col 57 | BE67 | `=DIST_PHASE_1_v2!AY56` | =DIST_PHASE_1_v2!AY56 |
| Ligne 67 | Col 58 | BF67 | `=DIST_PHASE_1_v2!AZ56` | =DIST_PHASE_1_v2!AZ56 |
| Ligne 67 | Col 59 | BG67 | `=DIST_PHASE_1_v2!BA56` | =DIST_PHASE_1_v2!BA56 |
| Ligne 67 | Col 60 | BH67 | `= (10.679 * BG67) / ((BE67/1000)^4.871 * BF67^1.852)` | = (10.679 * BG67) / ((BE67/1000)^4.871 * BF67^1.852) |
| Ligne 67 | Col 61 | BI67 | `=IF(BB67="positif",BD67,IF(BB67="negatif",-BD67,""))` | =IF(BB67="positif",BD67,IF(BB67="negatif",-BD67,"")) |
| Ligne 67 | Col 62 | BJ67 | `=IF(AZ67>0,
IF(BI67>0, BH67*BI67^1.852,-BH67*ABS(BI67)^1.852),
IF(BI67>0, BH67*BD67^1.852, -BH67*BD67^1.852))` | =IF(AZ67>0,
IF(BI67>0, BH67*BI67^1.852,-BH67*ABS(BI67)^1.852),
IF(BI67>0, BH67*BD67^1.852, -BH67*BD67^1.852)) |
| Ligne 67 | Col 63 | BK67 | `=1.852*BH67*ABS(BI67)^(1.852-1)` | =1.852*BH67*ABS(BI67)^(1.852-1) |
| Ligne 67 | Col 64 | BL67 | `=BI67+$BD$75` | =BI67+$BD$75 |
| Ligne 67 | Col 84 | CF67 | `=IFERROR(MATCH(CI67,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI67,$BS$22:$BS$62,0),0) |
| Ligne 67 | Col 86 | CH67 | `=DIST_PHASE_1_v2!BS56` | =DIST_PHASE_1_v2!BS56 |
| Ligne 67 | Col 87 | CI67 | `=DIST_PHASE_1_v2!BT56` | =DIST_PHASE_1_v2!BT56 |
| Ligne 67 | Col 88 | CJ67 | `=DIST_PHASE_1_v2!BV56` | =DIST_PHASE_1_v2!BV56 |
| Ligne 67 | Col 89 | CK67 | `=DIST_PHASE_1_v2!CA56` | =DIST_PHASE_1_v2!CA56 |
| Ligne 67 | Col 91 | CM67 | `=DIST_PHASE_1_v2!CC56` | =DIST_PHASE_1_v2!CC56 |
| Ligne 67 | Col 92 | CN67 | `= (10.679 * CM67) / ((CK67/1000)^4.871 * CL67^1.852)` | = (10.679 * CM67) / ((CK67/1000)^4.871 * CL67^1.852) |
| Ligne 67 | Col 93 | CO67 | `=IF(CH67="positif",CJ67,IF(CH67="negatif",-CJ67,""))` | =IF(CH67="positif",CJ67,IF(CH67="negatif",-CJ67,"")) |
| Ligne 67 | Col 94 | CP67 | `=IF(CF67>0,
IF(CO67>0, CN67*CO67^1.852,-CN67*ABS(CO67)^1.852),
IF(CO67>0, CN67*CJ67^1.852, -CN67*CJ67^1.852))` | =IF(CF67>0,
IF(CO67>0, CN67*CO67^1.852,-CN67*ABS(CO67)^1.852),
IF(CO67>0, CN67*CJ67^1.852, -CN67*CJ67^1.852)) |
| Ligne 67 | Col 95 | CQ67 | `=1.852*CN67*ABS(CO67)^(1.852-1)` | =1.852*CN67*ABS(CO67)^(1.852-1) |
| Ligne 67 | Col 96 | CR67 | `=CO67+$CJ$71` | =CO67+$CJ$71 |
| Ligne 68 | Col 4 | D68 | `=DIST_PHASE_1_v2!E57` | =DIST_PHASE_1_v2!E57 |
| Ligne 68 | Col 5 | E68 | `=DIST_PHASE_1_v2!G57` | =DIST_PHASE_1_v2!G57 |
| Ligne 68 | Col 6 | F68 | `=DIST_PHASE_1_v2!L57` | =DIST_PHASE_1_v2!L57 |
| Ligne 68 | Col 7 | G68 | `=DIST_PHASE_1_v2!M57` | =DIST_PHASE_1_v2!M57 |
| Ligne 68 | Col 8 | H68 | `=DIST_PHASE_1_v2!N57` | =DIST_PHASE_1_v2!N57 |
| Ligne 68 | Col 9 | I68 | `= (10.679 * H68) / ((F68/1000)^4.871 * G68^1.852)` | = (10.679 * H68) / ((F68/1000)^4.871 * G68^1.852) |
| Ligne 68 | Col 10 | J68 | `=IF(C68="positif",E68,IF(C68="negatif",-E68,""))` | =IF(C68="positif",E68,IF(C68="negatif",-E68,"")) |
| Ligne 68 | Col 11 | K68 | `=IF(J68>0,I68*E68^1.852,-I68*E68^1.852)` | =IF(J68>0,I68*E68^1.852,-I68*E68^1.852) |
| Ligne 68 | Col 12 | L68 | `=1.852*I68*ABS(E68)^(1.852-1)` | =1.852*I68*ABS(E68)^(1.852-1) |
| Ligne 68 | Col 13 | M68 | `=J68+$D$93` | =J68+$D$93 |
| Ligne 68 | Col 16 | P68 | `=IFERROR(MATCH(S68,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S68,$D$22:$D$91,0),0) |
| Ligne 68 | Col 18 | R68 | `=DIST_PHASE_1_v2!Q57` | =DIST_PHASE_1_v2!Q57 |
| Ligne 68 | Col 19 | S68 | `=DIST_PHASE_1_v2!R57` | =DIST_PHASE_1_v2!R57 |
| Ligne 68 | Col 20 | T68 | `=DIST_PHASE_1_v2!T57` | =DIST_PHASE_1_v2!T57 |
| Ligne 68 | Col 21 | U68 | `=DIST_PHASE_1_v2!Y57` | =DIST_PHASE_1_v2!Y57 |
| Ligne 68 | Col 23 | W68 | `=DIST_PHASE_1_v2!AA57` | =DIST_PHASE_1_v2!AA57 |
| Ligne 68 | Col 24 | X68 | `= (10.679 * W68) / ((U68/1000)^4.871 * V68^1.852)` | = (10.679 * W68) / ((U68/1000)^4.871 * V68^1.852) |
| Ligne 68 | Col 25 | Y68 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA270>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA270> |
| Ligne 68 | Col 26 | Z68 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9670>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F9670> |
| Ligne 68 | Col 27 | AA68 | `=IF(P68>0,
IF(R68="positif",1,-1),
0)` | =IF(P68>0,
IF(R68="positif",1,-1),
0) |
| Ligne 68 | Col 28 | AB68 | `=X68*SIGN(Y68)*ABS(Y68)^1.852` | =X68*SIGN(Y68)*ABS(Y68)^1.852 |
| Ligne 68 | Col 29 | AC68 | `=1.852*X68*ABS(Y68)^(1.852-1)` | =1.852*X68*ABS(Y68)^(1.852-1) |
| Ligne 68 | Col 30 | AD68 | `=IF(P68>0,
Y68+($D$93*Z68)+(AA68*$S$93),
Y68+$S$93)` | =IF(P68>0,
Y68+($D$93*Z68)+(AA68*$S$93),
Y68+$S$93) |
| Ligne 68 | Col 32 | AF68 | `=ABS(AD68)-ABS(Y68)` | =ABS(AD68)-ABS(Y68) |
| Ligne 68 | Col 52 | AZ68 | `=IFERROR(MATCH(BC68,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC68,$AM$22:$AM$57,0),0) |
| Ligne 68 | Col 54 | BB68 | `=DIST_PHASE_1_v2!AQ57` | =DIST_PHASE_1_v2!AQ57 |
| Ligne 68 | Col 55 | BC68 | `=DIST_PHASE_1_v2!AR57` | =DIST_PHASE_1_v2!AR57 |
| Ligne 68 | Col 56 | BD68 | `=DIST_PHASE_1_v2!AT57` | =DIST_PHASE_1_v2!AT57 |
| Ligne 68 | Col 57 | BE68 | `=DIST_PHASE_1_v2!AY57` | =DIST_PHASE_1_v2!AY57 |
| Ligne 68 | Col 58 | BF68 | `=DIST_PHASE_1_v2!AZ57` | =DIST_PHASE_1_v2!AZ57 |
| Ligne 68 | Col 59 | BG68 | `=DIST_PHASE_1_v2!BA57` | =DIST_PHASE_1_v2!BA57 |
| Ligne 68 | Col 60 | BH68 | `= (10.679 * BG68) / ((BE68/1000)^4.871 * BF68^1.852)` | = (10.679 * BG68) / ((BE68/1000)^4.871 * BF68^1.852) |
| Ligne 68 | Col 61 | BI68 | `=IF(BB68="positif",BD68,IF(BB68="negatif",-BD68,""))` | =IF(BB68="positif",BD68,IF(BB68="negatif",-BD68,"")) |
| Ligne 68 | Col 62 | BJ68 | `=IF(AZ68>0,
IF(BI68>0, BH68*BI68^1.852,-BH68*ABS(BI68)^1.852),
IF(BI68>0, BH68*BD68^1.852, -BH68*BD68^1.852))` | =IF(AZ68>0,
IF(BI68>0, BH68*BI68^1.852,-BH68*ABS(BI68)^1.852),
IF(BI68>0, BH68*BD68^1.852, -BH68*BD68^1.852)) |
| Ligne 68 | Col 63 | BK68 | `=1.852*BH68*ABS(BI68)^(1.852-1)` | =1.852*BH68*ABS(BI68)^(1.852-1) |
| Ligne 68 | Col 64 | BL68 | `=BI68+$BD$75` | =BI68+$BD$75 |
| Ligne 68 | Col 84 | CF68 | `=IFERROR(MATCH(CI68,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI68,$BS$22:$BS$62,0),0) |
| Ligne 68 | Col 86 | CH68 | `=DIST_PHASE_1_v2!BS57` | =DIST_PHASE_1_v2!BS57 |
| Ligne 68 | Col 87 | CI68 | `=DIST_PHASE_1_v2!BT57` | =DIST_PHASE_1_v2!BT57 |
| Ligne 68 | Col 88 | CJ68 | `=DIST_PHASE_1_v2!BV57` | =DIST_PHASE_1_v2!BV57 |
| Ligne 68 | Col 89 | CK68 | `=DIST_PHASE_1_v2!CA57` | =DIST_PHASE_1_v2!CA57 |
| Ligne 68 | Col 91 | CM68 | `=DIST_PHASE_1_v2!CC57` | =DIST_PHASE_1_v2!CC57 |
| Ligne 68 | Col 92 | CN68 | `= (10.679 * CM68) / ((CK68/1000)^4.871 * CL68^1.852)` | = (10.679 * CM68) / ((CK68/1000)^4.871 * CL68^1.852) |
| Ligne 68 | Col 93 | CO68 | `=IF(CH68="positif",CJ68,IF(CH68="negatif",-CJ68,""))` | =IF(CH68="positif",CJ68,IF(CH68="negatif",-CJ68,"")) |
| Ligne 68 | Col 94 | CP68 | `=IF(CF68>0,
IF(CO68>0, CN68*CO68^1.852,-CN68*ABS(CO68)^1.852),
IF(CO68>0, CN68*CJ68^1.852, -CN68*CJ68^1.852))` | =IF(CF68>0,
IF(CO68>0, CN68*CO68^1.852,-CN68*ABS(CO68)^1.852),
IF(CO68>0, CN68*CJ68^1.852, -CN68*CJ68^1.852)) |
| Ligne 68 | Col 95 | CQ68 | `=1.852*CN68*ABS(CO68)^(1.852-1)` | =1.852*CN68*ABS(CO68)^(1.852-1) |
| Ligne 68 | Col 96 | CR68 | `=CO68+$CJ$71` | =CO68+$CJ$71 |
| Ligne 69 | Col 4 | D69 | `=DIST_PHASE_1_v2!E58` | =DIST_PHASE_1_v2!E58 |
| Ligne 69 | Col 5 | E69 | `=DIST_PHASE_1_v2!G58` | =DIST_PHASE_1_v2!G58 |
| Ligne 69 | Col 6 | F69 | `=DIST_PHASE_1_v2!L58` | =DIST_PHASE_1_v2!L58 |
| Ligne 69 | Col 7 | G69 | `=DIST_PHASE_1_v2!M58` | =DIST_PHASE_1_v2!M58 |
| Ligne 69 | Col 8 | H69 | `=DIST_PHASE_1_v2!N58` | =DIST_PHASE_1_v2!N58 |
| Ligne 69 | Col 9 | I69 | `= (10.679 * H69) / ((F69/1000)^4.871 * G69^1.852)` | = (10.679 * H69) / ((F69/1000)^4.871 * G69^1.852) |
| Ligne 69 | Col 10 | J69 | `=IF(C69="positif",E69,IF(C69="negatif",-E69,""))` | =IF(C69="positif",E69,IF(C69="negatif",-E69,"")) |
| Ligne 69 | Col 11 | K69 | `=IF(J69>0,I69*E69^1.852,-I69*E69^1.852)` | =IF(J69>0,I69*E69^1.852,-I69*E69^1.852) |
| Ligne 69 | Col 12 | L69 | `=1.852*I69*ABS(E69)^(1.852-1)` | =1.852*I69*ABS(E69)^(1.852-1) |
| Ligne 69 | Col 13 | M69 | `=J69+$D$93` | =J69+$D$93 |
| Ligne 69 | Col 16 | P69 | `=IFERROR(MATCH(S69,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S69,$D$22:$D$91,0),0) |
| Ligne 69 | Col 18 | R69 | `=DIST_PHASE_1_v2!Q58` | =DIST_PHASE_1_v2!Q58 |
| Ligne 69 | Col 19 | S69 | `=DIST_PHASE_1_v2!R58` | =DIST_PHASE_1_v2!R58 |
| Ligne 69 | Col 20 | T69 | `=DIST_PHASE_1_v2!T58` | =DIST_PHASE_1_v2!T58 |
| Ligne 69 | Col 21 | U69 | `=DIST_PHASE_1_v2!Y58` | =DIST_PHASE_1_v2!Y58 |
| Ligne 69 | Col 23 | W69 | `=DIST_PHASE_1_v2!AA58` | =DIST_PHASE_1_v2!AA58 |
| Ligne 69 | Col 24 | X69 | `= (10.679 * W69) / ((U69/1000)^4.871 * V69^1.852)` | = (10.679 * W69) / ((U69/1000)^4.871 * V69^1.852) |
| Ligne 69 | Col 25 | Y69 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA5D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA5D0> |
| Ligne 69 | Col 26 | Z69 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F96D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9F96D0> |
| Ligne 69 | Col 27 | AA69 | `=IF(P69>0,
IF(R69="positif",1,-1),
0)` | =IF(P69>0,
IF(R69="positif",1,-1),
0) |
| Ligne 69 | Col 28 | AB69 | `=X69*SIGN(Y69)*ABS(Y69)^1.852` | =X69*SIGN(Y69)*ABS(Y69)^1.852 |
| Ligne 69 | Col 29 | AC69 | `=1.852*X69*ABS(Y69)^(1.852-1)` | =1.852*X69*ABS(Y69)^(1.852-1) |
| Ligne 69 | Col 30 | AD69 | `=IF(P69>0,
Y69+($D$93*Z69)+(AA69*$S$93),
Y69+$S$93)` | =IF(P69>0,
Y69+($D$93*Z69)+(AA69*$S$93),
Y69+$S$93) |
| Ligne 69 | Col 32 | AF69 | `=ABS(AD69)-ABS(Y69)` | =ABS(AD69)-ABS(Y69) |
| Ligne 69 | Col 52 | AZ69 | `=IFERROR(MATCH(BC69,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC69,$AM$22:$AM$57,0),0) |
| Ligne 69 | Col 54 | BB69 | `=DIST_PHASE_1_v2!AQ58` | =DIST_PHASE_1_v2!AQ58 |
| Ligne 69 | Col 55 | BC69 | `=DIST_PHASE_1_v2!AR58` | =DIST_PHASE_1_v2!AR58 |
| Ligne 69 | Col 56 | BD69 | `=DIST_PHASE_1_v2!AT58` | =DIST_PHASE_1_v2!AT58 |
| Ligne 69 | Col 57 | BE69 | `=DIST_PHASE_1_v2!AY58` | =DIST_PHASE_1_v2!AY58 |
| Ligne 69 | Col 58 | BF69 | `=DIST_PHASE_1_v2!AZ58` | =DIST_PHASE_1_v2!AZ58 |
| Ligne 69 | Col 59 | BG69 | `=DIST_PHASE_1_v2!BA58` | =DIST_PHASE_1_v2!BA58 |
| Ligne 69 | Col 60 | BH69 | `= (10.679 * BG69) / ((BE69/1000)^4.871 * BF69^1.852)` | = (10.679 * BG69) / ((BE69/1000)^4.871 * BF69^1.852) |
| Ligne 69 | Col 61 | BI69 | `=IF(BB69="positif",BD69,IF(BB69="negatif",-BD69,""))` | =IF(BB69="positif",BD69,IF(BB69="negatif",-BD69,"")) |
| Ligne 69 | Col 62 | BJ69 | `=IF(AZ69>0,
IF(BI69>0, BH69*BI69^1.852,-BH69*ABS(BI69)^1.852),
IF(BI69>0, BH69*BD69^1.852, -BH69*BD69^1.852))` | =IF(AZ69>0,
IF(BI69>0, BH69*BI69^1.852,-BH69*ABS(BI69)^1.852),
IF(BI69>0, BH69*BD69^1.852, -BH69*BD69^1.852)) |
| Ligne 69 | Col 63 | BK69 | `=1.852*BH69*ABS(BI69)^(1.852-1)` | =1.852*BH69*ABS(BI69)^(1.852-1) |
| Ligne 69 | Col 64 | BL69 | `=BI69+$BD$75` | =BI69+$BD$75 |
| Ligne 69 | Col 84 | CF69 | `=IFERROR(MATCH(CI69,$BS$22:$BS$62,0),0)` | =IFERROR(MATCH(CI69,$BS$22:$BS$62,0),0) |
| Ligne 69 | Col 86 | CH69 | `=DIST_PHASE_1_v2!BS58` | =DIST_PHASE_1_v2!BS58 |
| Ligne 69 | Col 87 | CI69 | `=DIST_PHASE_1_v2!BT58` | =DIST_PHASE_1_v2!BT58 |
| Ligne 69 | Col 88 | CJ69 | `=DIST_PHASE_1_v2!BV58` | =DIST_PHASE_1_v2!BV58 |
| Ligne 69 | Col 89 | CK69 | `=DIST_PHASE_1_v2!CA58` | =DIST_PHASE_1_v2!CA58 |
| Ligne 69 | Col 91 | CM69 | `=DIST_PHASE_1_v2!CC58` | =DIST_PHASE_1_v2!CC58 |
| Ligne 69 | Col 92 | CN69 | `= (10.679 * CM69) / ((CK69/1000)^4.871 * CL69^1.852)` | = (10.679 * CM69) / ((CK69/1000)^4.871 * CL69^1.852) |
| Ligne 69 | Col 93 | CO69 | `=IF(CH69="positif",CJ69,IF(CH69="negatif",-CJ69,""))` | =IF(CH69="positif",CJ69,IF(CH69="negatif",-CJ69,"")) |
| Ligne 69 | Col 94 | CP69 | `=IF(CF69>0,
IF(CO69>0, CN69*CO69^1.852,-CN69*ABS(CO69)^1.852),
IF(CO69>0, CN69*CJ69^1.852, -CN69*CJ69^1.852))` | =IF(CF69>0,
IF(CO69>0, CN69*CO69^1.852,-CN69*ABS(CO69)^1.852),
IF(CO69>0, CN69*CJ69^1.852, -CN69*CJ69^1.852)) |
| Ligne 69 | Col 95 | CQ69 | `=1.852*CN69*ABS(CO69)^(1.852-1)` | =1.852*CN69*ABS(CO69)^(1.852-1) |
| Ligne 69 | Col 96 | CR69 | `=CO69+$CJ$71` | =CO69+$CJ$71 |
| Ligne 70 | Col 4 | D70 | `=DIST_PHASE_1_v2!E59` | =DIST_PHASE_1_v2!E59 |
| Ligne 70 | Col 5 | E70 | `=DIST_PHASE_1_v2!G59` | =DIST_PHASE_1_v2!G59 |
| Ligne 70 | Col 6 | F70 | `=DIST_PHASE_1_v2!L59` | =DIST_PHASE_1_v2!L59 |
| Ligne 70 | Col 7 | G70 | `=DIST_PHASE_1_v2!M59` | =DIST_PHASE_1_v2!M59 |
| Ligne 70 | Col 8 | H70 | `=DIST_PHASE_1_v2!N59` | =DIST_PHASE_1_v2!N59 |
| Ligne 70 | Col 9 | I70 | `= (10.679 * H70) / ((F70/1000)^4.871 * G70^1.852)` | = (10.679 * H70) / ((F70/1000)^4.871 * G70^1.852) |
| Ligne 70 | Col 10 | J70 | `=IF(C70="positif",E70,IF(C70="negatif",-E70,""))` | =IF(C70="positif",E70,IF(C70="negatif",-E70,"")) |
| Ligne 70 | Col 11 | K70 | `=IF(J70>0,I70*E70^1.852,-I70*E70^1.852)` | =IF(J70>0,I70*E70^1.852,-I70*E70^1.852) |
| Ligne 70 | Col 12 | L70 | `=1.852*I70*ABS(E70)^(1.852-1)` | =1.852*I70*ABS(E70)^(1.852-1) |
| Ligne 70 | Col 13 | M70 | `=J70+$D$93` | =J70+$D$93 |
| Ligne 70 | Col 16 | P70 | `=IFERROR(MATCH(S70,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S70,$D$22:$D$91,0),0) |
| Ligne 70 | Col 18 | R70 | `=DIST_PHASE_1_v2!Q59` | =DIST_PHASE_1_v2!Q59 |
| Ligne 70 | Col 19 | S70 | `=DIST_PHASE_1_v2!R59` | =DIST_PHASE_1_v2!R59 |
| Ligne 70 | Col 20 | T70 | `=DIST_PHASE_1_v2!T59` | =DIST_PHASE_1_v2!T59 |
| Ligne 70 | Col 21 | U70 | `=DIST_PHASE_1_v2!Y59` | =DIST_PHASE_1_v2!Y59 |
| Ligne 70 | Col 23 | W70 | `=DIST_PHASE_1_v2!AA59` | =DIST_PHASE_1_v2!AA59 |
| Ligne 70 | Col 24 | X70 | `= (10.679 * W70) / ((U70/1000)^4.871 * V70^1.852)` | = (10.679 * W70) / ((U70/1000)^4.871 * V70^1.852) |
| Ligne 70 | Col 25 | Y70 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FAB70>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FAB70> |
| Ligne 70 | Col 26 | Z70 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FABD0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FABD0> |
| Ligne 70 | Col 27 | AA70 | `=IF(P70>0,
IF(R70="positif",1,-1),
0)` | =IF(P70>0,
IF(R70="positif",1,-1),
0) |
| Ligne 70 | Col 28 | AB70 | `=X70*SIGN(Y70)*ABS(Y70)^1.852` | =X70*SIGN(Y70)*ABS(Y70)^1.852 |
| Ligne 70 | Col 29 | AC70 | `=1.852*X70*ABS(Y70)^(1.852-1)` | =1.852*X70*ABS(Y70)^(1.852-1) |
| Ligne 70 | Col 30 | AD70 | `=IF(P70>0,
Y70+($D$93*Z70)+(AA70*$S$93),
Y70+$S$93)` | =IF(P70>0,
Y70+($D$93*Z70)+(AA70*$S$93),
Y70+$S$93) |
| Ligne 70 | Col 32 | AF70 | `=ABS(AD70)-ABS(Y70)` | =ABS(AD70)-ABS(Y70) |
| Ligne 70 | Col 52 | AZ70 | `=IFERROR(MATCH(BC70,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC70,$AM$22:$AM$57,0),0) |
| Ligne 70 | Col 54 | BB70 | `=DIST_PHASE_1_v2!AQ59` | =DIST_PHASE_1_v2!AQ59 |
| Ligne 70 | Col 55 | BC70 | `=DIST_PHASE_1_v2!AR59` | =DIST_PHASE_1_v2!AR59 |
| Ligne 70 | Col 56 | BD70 | `=DIST_PHASE_1_v2!AT59` | =DIST_PHASE_1_v2!AT59 |
| Ligne 70 | Col 57 | BE70 | `=DIST_PHASE_1_v2!AY59` | =DIST_PHASE_1_v2!AY59 |
| Ligne 70 | Col 58 | BF70 | `=DIST_PHASE_1_v2!AZ59` | =DIST_PHASE_1_v2!AZ59 |
| Ligne 70 | Col 59 | BG70 | `=DIST_PHASE_1_v2!BA59` | =DIST_PHASE_1_v2!BA59 |
| Ligne 70 | Col 60 | BH70 | `= (10.679 * BG70) / ((BE70/1000)^4.871 * BF70^1.852)` | = (10.679 * BG70) / ((BE70/1000)^4.871 * BF70^1.852) |
| Ligne 70 | Col 61 | BI70 | `=IF(BB70="positif",BD70,IF(BB70="negatif",-BD70,""))` | =IF(BB70="positif",BD70,IF(BB70="negatif",-BD70,"")) |
| Ligne 70 | Col 62 | BJ70 | `=IF(AZ70>0,
IF(BI70>0, BH70*BI70^1.852,-BH70*ABS(BI70)^1.852),
IF(BI70>0, BH70*BD70^1.852, -BH70*BD70^1.852))` | =IF(AZ70>0,
IF(BI70>0, BH70*BI70^1.852,-BH70*ABS(BI70)^1.852),
IF(BI70>0, BH70*BD70^1.852, -BH70*BD70^1.852)) |
| Ligne 70 | Col 63 | BK70 | `=1.852*BH70*ABS(BI70)^(1.852-1)` | =1.852*BH70*ABS(BI70)^(1.852-1) |
| Ligne 70 | Col 64 | BL70 | `=BI70+$BD$75` | =BI70+$BD$75 |
| Ligne 70 | Col 94 | CP70 | `=SUM(CP22:CP69)` | =SUM(CP22:CP69) |
| Ligne 70 | Col 95 | CQ70 | `=SUM(CQ22:CQ69)` | =SUM(CQ22:CQ69) |
| Ligne 71 | Col 4 | D71 | `=DIST_PHASE_1_v2!E60` | =DIST_PHASE_1_v2!E60 |
| Ligne 71 | Col 5 | E71 | `=DIST_PHASE_1_v2!G60` | =DIST_PHASE_1_v2!G60 |
| Ligne 71 | Col 6 | F71 | `=DIST_PHASE_1_v2!L60` | =DIST_PHASE_1_v2!L60 |
| Ligne 71 | Col 7 | G71 | `=DIST_PHASE_1_v2!M60` | =DIST_PHASE_1_v2!M60 |
| Ligne 71 | Col 8 | H71 | `=DIST_PHASE_1_v2!N60` | =DIST_PHASE_1_v2!N60 |
| Ligne 71 | Col 9 | I71 | `= (10.679 * H71) / ((F71/1000)^4.871 * G71^1.852)` | = (10.679 * H71) / ((F71/1000)^4.871 * G71^1.852) |
| Ligne 71 | Col 10 | J71 | `=IF(C71="positif",E71,IF(C71="negatif",-E71,""))` | =IF(C71="positif",E71,IF(C71="negatif",-E71,"")) |
| Ligne 71 | Col 11 | K71 | `=IF(J71>0,I71*E71^1.852,-I71*E71^1.852)` | =IF(J71>0,I71*E71^1.852,-I71*E71^1.852) |
| Ligne 71 | Col 12 | L71 | `=1.852*I71*ABS(E71)^(1.852-1)` | =1.852*I71*ABS(E71)^(1.852-1) |
| Ligne 71 | Col 13 | M71 | `=J71+$D$93` | =J71+$D$93 |
| Ligne 71 | Col 16 | P71 | `=IFERROR(MATCH(S71,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S71,$D$22:$D$91,0),0) |
| Ligne 71 | Col 18 | R71 | `=DIST_PHASE_1_v2!Q60` | =DIST_PHASE_1_v2!Q60 |
| Ligne 71 | Col 19 | S71 | `=DIST_PHASE_1_v2!R60` | =DIST_PHASE_1_v2!R60 |
| Ligne 71 | Col 20 | T71 | `=DIST_PHASE_1_v2!T60` | =DIST_PHASE_1_v2!T60 |
| Ligne 71 | Col 21 | U71 | `=DIST_PHASE_1_v2!Y60` | =DIST_PHASE_1_v2!Y60 |
| Ligne 71 | Col 23 | W71 | `=DIST_PHASE_1_v2!AA60` | =DIST_PHASE_1_v2!AA60 |
| Ligne 71 | Col 24 | X71 | `= (10.679 * W71) / ((U71/1000)^4.871 * V71^1.852)` | = (10.679 * W71) / ((U71/1000)^4.871 * V71^1.852) |
| Ligne 71 | Col 25 | Y71 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FAE70>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FAE70> |
| Ligne 71 | Col 26 | Z71 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA810>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA810> |
| Ligne 71 | Col 27 | AA71 | `=IF(P71>0,
IF(R71="positif",1,-1),
0)` | =IF(P71>0,
IF(R71="positif",1,-1),
0) |
| Ligne 71 | Col 28 | AB71 | `=X71*SIGN(Y71)*ABS(Y71)^1.852` | =X71*SIGN(Y71)*ABS(Y71)^1.852 |
| Ligne 71 | Col 29 | AC71 | `=1.852*X71*ABS(Y71)^(1.852-1)` | =1.852*X71*ABS(Y71)^(1.852-1) |
| Ligne 71 | Col 30 | AD71 | `=IF(P71>0,
Y71+($D$93*Z71)+(AA71*$S$93),
Y71+$S$93)` | =IF(P71>0,
Y71+($D$93*Z71)+(AA71*$S$93),
Y71+$S$93) |
| Ligne 71 | Col 32 | AF71 | `=ABS(AD71)-ABS(Y71)` | =ABS(AD71)-ABS(Y71) |
| Ligne 71 | Col 52 | AZ71 | `=IFERROR(MATCH(BC71,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC71,$AM$22:$AM$57,0),0) |
| Ligne 71 | Col 54 | BB71 | `=DIST_PHASE_1_v2!AQ60` | =DIST_PHASE_1_v2!AQ60 |
| Ligne 71 | Col 55 | BC71 | `=DIST_PHASE_1_v2!AR60` | =DIST_PHASE_1_v2!AR60 |
| Ligne 71 | Col 56 | BD71 | `=DIST_PHASE_1_v2!AT60` | =DIST_PHASE_1_v2!AT60 |
| Ligne 71 | Col 57 | BE71 | `=DIST_PHASE_1_v2!AY60` | =DIST_PHASE_1_v2!AY60 |
| Ligne 71 | Col 58 | BF71 | `=DIST_PHASE_1_v2!AZ60` | =DIST_PHASE_1_v2!AZ60 |
| Ligne 71 | Col 59 | BG71 | `=DIST_PHASE_1_v2!BA60` | =DIST_PHASE_1_v2!BA60 |
| Ligne 71 | Col 60 | BH71 | `= (10.679 * BG71) / ((BE71/1000)^4.871 * BF71^1.852)` | = (10.679 * BG71) / ((BE71/1000)^4.871 * BF71^1.852) |
| Ligne 71 | Col 61 | BI71 | `=IF(BB71="positif",BD71,IF(BB71="negatif",-BD71,""))` | =IF(BB71="positif",BD71,IF(BB71="negatif",-BD71,"")) |
| Ligne 71 | Col 62 | BJ71 | `=IF(AZ71>0,
IF(BI71>0, BH71*BI71^1.852,-BH71*ABS(BI71)^1.852),
IF(BI71>0, BH71*BD71^1.852, -BH71*BD71^1.852))` | =IF(AZ71>0,
IF(BI71>0, BH71*BI71^1.852,-BH71*ABS(BI71)^1.852),
IF(BI71>0, BH71*BD71^1.852, -BH71*BD71^1.852)) |
| Ligne 71 | Col 63 | BK71 | `=1.852*BH71*ABS(BI71)^(1.852-1)` | =1.852*BH71*ABS(BI71)^(1.852-1) |
| Ligne 71 | Col 64 | BL71 | `=BI71+$BD$75` | =BI71+$BD$75 |
| Ligne 71 | Col 88 | CJ71 | `=-(CP70/CQ70)` | =-(CP70/CQ70) |
| Ligne 72 | Col 4 | D72 | `=DIST_PHASE_1_v2!E61` | =DIST_PHASE_1_v2!E61 |
| Ligne 72 | Col 5 | E72 | `=DIST_PHASE_1_v2!G61` | =DIST_PHASE_1_v2!G61 |
| Ligne 72 | Col 6 | F72 | `=DIST_PHASE_1_v2!L61` | =DIST_PHASE_1_v2!L61 |
| Ligne 72 | Col 7 | G72 | `=DIST_PHASE_1_v2!M61` | =DIST_PHASE_1_v2!M61 |
| Ligne 72 | Col 8 | H72 | `=DIST_PHASE_1_v2!N61` | =DIST_PHASE_1_v2!N61 |
| Ligne 72 | Col 9 | I72 | `= (10.679 * H72) / ((F72/1000)^4.871 * G72^1.852)` | = (10.679 * H72) / ((F72/1000)^4.871 * G72^1.852) |
| Ligne 72 | Col 10 | J72 | `=IF(C72="positif",E72,IF(C72="negatif",-E72,""))` | =IF(C72="positif",E72,IF(C72="negatif",-E72,"")) |
| Ligne 72 | Col 11 | K72 | `=IF(J72>0,I72*E72^1.852,-I72*E72^1.852)` | =IF(J72>0,I72*E72^1.852,-I72*E72^1.852) |
| Ligne 72 | Col 12 | L72 | `=1.852*I72*ABS(E72)^(1.852-1)` | =1.852*I72*ABS(E72)^(1.852-1) |
| Ligne 72 | Col 13 | M72 | `=J72+$D$93` | =J72+$D$93 |
| Ligne 72 | Col 16 | P72 | `=IFERROR(MATCH(S72,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S72,$D$22:$D$91,0),0) |
| Ligne 72 | Col 18 | R72 | `=DIST_PHASE_1_v2!Q61` | =DIST_PHASE_1_v2!Q61 |
| Ligne 72 | Col 19 | S72 | `=DIST_PHASE_1_v2!R61` | =DIST_PHASE_1_v2!R61 |
| Ligne 72 | Col 20 | T72 | `=DIST_PHASE_1_v2!T61` | =DIST_PHASE_1_v2!T61 |
| Ligne 72 | Col 21 | U72 | `=DIST_PHASE_1_v2!Y61` | =DIST_PHASE_1_v2!Y61 |
| Ligne 72 | Col 23 | W72 | `=DIST_PHASE_1_v2!AA61` | =DIST_PHASE_1_v2!AA61 |
| Ligne 72 | Col 24 | X72 | `= (10.679 * W72) / ((U72/1000)^4.871 * V72^1.852)` | = (10.679 * W72) / ((U72/1000)^4.871 * V72^1.852) |
| Ligne 72 | Col 25 | Y72 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FB110>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FB110> |
| Ligne 72 | Col 26 | Z72 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA870>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA870> |
| Ligne 72 | Col 27 | AA72 | `=IF(P72>0,
IF(R72="positif",1,-1),
0)` | =IF(P72>0,
IF(R72="positif",1,-1),
0) |
| Ligne 72 | Col 28 | AB72 | `=X72*SIGN(Y72)*ABS(Y72)^1.852` | =X72*SIGN(Y72)*ABS(Y72)^1.852 |
| Ligne 72 | Col 29 | AC72 | `=1.852*X72*ABS(Y72)^(1.852-1)` | =1.852*X72*ABS(Y72)^(1.852-1) |
| Ligne 72 | Col 30 | AD72 | `=IF(P72>0,
Y72+($D$93*Z72)+(AA72*$S$93),
Y72+$S$93)` | =IF(P72>0,
Y72+($D$93*Z72)+(AA72*$S$93),
Y72+$S$93) |
| Ligne 72 | Col 32 | AF72 | `=ABS(AD72)-ABS(Y72)` | =ABS(AD72)-ABS(Y72) |
| Ligne 72 | Col 52 | AZ72 | `=IFERROR(MATCH(BC72,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC72,$AM$22:$AM$57,0),0) |
| Ligne 72 | Col 54 | BB72 | `=DIST_PHASE_1_v2!AQ61` | =DIST_PHASE_1_v2!AQ61 |
| Ligne 72 | Col 55 | BC72 | `=DIST_PHASE_1_v2!AR61` | =DIST_PHASE_1_v2!AR61 |
| Ligne 72 | Col 56 | BD72 | `=DIST_PHASE_1_v2!AT61` | =DIST_PHASE_1_v2!AT61 |
| Ligne 72 | Col 57 | BE72 | `=DIST_PHASE_1_v2!AY61` | =DIST_PHASE_1_v2!AY61 |
| Ligne 72 | Col 58 | BF72 | `=DIST_PHASE_1_v2!AZ61` | =DIST_PHASE_1_v2!AZ61 |
| Ligne 72 | Col 59 | BG72 | `=DIST_PHASE_1_v2!BA61` | =DIST_PHASE_1_v2!BA61 |
| Ligne 72 | Col 60 | BH72 | `= (10.679 * BG72) / ((BE72/1000)^4.871 * BF72^1.852)` | = (10.679 * BG72) / ((BE72/1000)^4.871 * BF72^1.852) |
| Ligne 72 | Col 61 | BI72 | `=IF(BB72="positif",BD72,IF(BB72="negatif",-BD72,""))` | =IF(BB72="positif",BD72,IF(BB72="negatif",-BD72,"")) |
| Ligne 72 | Col 62 | BJ72 | `=IF(AZ72>0,
IF(BI72>0, BH72*BI72^1.852,-BH72*ABS(BI72)^1.852),
IF(BI72>0, BH72*BD72^1.852, -BH72*BD72^1.852))` | =IF(AZ72>0,
IF(BI72>0, BH72*BI72^1.852,-BH72*ABS(BI72)^1.852),
IF(BI72>0, BH72*BD72^1.852, -BH72*BD72^1.852)) |
| Ligne 72 | Col 63 | BK72 | `=1.852*BH72*ABS(BI72)^(1.852-1)` | =1.852*BH72*ABS(BI72)^(1.852-1) |
| Ligne 72 | Col 64 | BL72 | `=BI72+$BD$75` | =BI72+$BD$75 |
| Ligne 73 | Col 4 | D73 | `=DIST_PHASE_1_v2!E62` | =DIST_PHASE_1_v2!E62 |
| Ligne 73 | Col 5 | E73 | `=DIST_PHASE_1_v2!G62` | =DIST_PHASE_1_v2!G62 |
| Ligne 73 | Col 6 | F73 | `=DIST_PHASE_1_v2!L62` | =DIST_PHASE_1_v2!L62 |
| Ligne 73 | Col 7 | G73 | `=DIST_PHASE_1_v2!M62` | =DIST_PHASE_1_v2!M62 |
| Ligne 73 | Col 8 | H73 | `=DIST_PHASE_1_v2!N62` | =DIST_PHASE_1_v2!N62 |
| Ligne 73 | Col 9 | I73 | `= (10.679 * H73) / ((F73/1000)^4.871 * G73^1.852)` | = (10.679 * H73) / ((F73/1000)^4.871 * G73^1.852) |
| Ligne 73 | Col 10 | J73 | `=IF(C73="positif",E73,IF(C73="negatif",-E73,""))` | =IF(C73="positif",E73,IF(C73="negatif",-E73,"")) |
| Ligne 73 | Col 11 | K73 | `=IF(J73>0,I73*E73^1.852,-I73*E73^1.852)` | =IF(J73>0,I73*E73^1.852,-I73*E73^1.852) |
| Ligne 73 | Col 12 | L73 | `=1.852*I73*ABS(E73)^(1.852-1)` | =1.852*I73*ABS(E73)^(1.852-1) |
| Ligne 73 | Col 13 | M73 | `=J73+$D$93` | =J73+$D$93 |
| Ligne 73 | Col 16 | P73 | `=IFERROR(MATCH(S73,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S73,$D$22:$D$91,0),0) |
| Ligne 73 | Col 18 | R73 | `=DIST_PHASE_1_v2!Q62` | =DIST_PHASE_1_v2!Q62 |
| Ligne 73 | Col 19 | S73 | `=DIST_PHASE_1_v2!R62` | =DIST_PHASE_1_v2!R62 |
| Ligne 73 | Col 20 | T73 | `=DIST_PHASE_1_v2!T62` | =DIST_PHASE_1_v2!T62 |
| Ligne 73 | Col 21 | U73 | `=DIST_PHASE_1_v2!Y62` | =DIST_PHASE_1_v2!Y62 |
| Ligne 73 | Col 23 | W73 | `=DIST_PHASE_1_v2!AA62` | =DIST_PHASE_1_v2!AA62 |
| Ligne 73 | Col 24 | X73 | `= (10.679 * W73) / ((U73/1000)^4.871 * V73^1.852)` | = (10.679 * W73) / ((U73/1000)^4.871 * V73^1.852) |
| Ligne 73 | Col 25 | Y73 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FB3B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FB3B0> |
| Ligne 73 | Col 26 | Z73 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA8D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA8D0> |
| Ligne 73 | Col 27 | AA73 | `=IF(P73>0,
IF(R73="positif",1,-1),
0)` | =IF(P73>0,
IF(R73="positif",1,-1),
0) |
| Ligne 73 | Col 28 | AB73 | `=X73*SIGN(Y73)*ABS(Y73)^1.852` | =X73*SIGN(Y73)*ABS(Y73)^1.852 |
| Ligne 73 | Col 29 | AC73 | `=1.852*X73*ABS(Y73)^(1.852-1)` | =1.852*X73*ABS(Y73)^(1.852-1) |
| Ligne 73 | Col 30 | AD73 | `=IF(P73>0,
Y73+($D$93*Z73)+(AA73*$S$93),
Y73+$S$93)` | =IF(P73>0,
Y73+($D$93*Z73)+(AA73*$S$93),
Y73+$S$93) |
| Ligne 73 | Col 32 | AF73 | `=ABS(AD73)-ABS(Y73)` | =ABS(AD73)-ABS(Y73) |
| Ligne 73 | Col 52 | AZ73 | `=IFERROR(MATCH(BC73,$AM$22:$AM$57,0),0)` | =IFERROR(MATCH(BC73,$AM$22:$AM$57,0),0) |
| Ligne 73 | Col 54 | BB73 | `=DIST_PHASE_1_v2!AQ62` | =DIST_PHASE_1_v2!AQ62 |
| Ligne 73 | Col 55 | BC73 | `=DIST_PHASE_1_v2!AR62` | =DIST_PHASE_1_v2!AR62 |
| Ligne 73 | Col 56 | BD73 | `=DIST_PHASE_1_v2!AT62` | =DIST_PHASE_1_v2!AT62 |
| Ligne 73 | Col 57 | BE73 | `=DIST_PHASE_1_v2!AY62` | =DIST_PHASE_1_v2!AY62 |
| Ligne 73 | Col 58 | BF73 | `=DIST_PHASE_1_v2!AZ62` | =DIST_PHASE_1_v2!AZ62 |
| Ligne 73 | Col 59 | BG73 | `=DIST_PHASE_1_v2!BA62` | =DIST_PHASE_1_v2!BA62 |
| Ligne 73 | Col 60 | BH73 | `= (10.679 * BG73) / ((BE73/1000)^4.871 * BF73^1.852)` | = (10.679 * BG73) / ((BE73/1000)^4.871 * BF73^1.852) |
| Ligne 73 | Col 61 | BI73 | `=IF(BB73="positif",BD73,IF(BB73="negatif",-BD73,""))` | =IF(BB73="positif",BD73,IF(BB73="negatif",-BD73,"")) |
| Ligne 73 | Col 62 | BJ73 | `=IF(AZ73>0,
IF(BI73>0, BH73*BI73^1.852,-BH73*ABS(BI73)^1.852),
IF(BI73>0, BH73*BD73^1.852, -BH73*BD73^1.852))` | =IF(AZ73>0,
IF(BI73>0, BH73*BI73^1.852,-BH73*ABS(BI73)^1.852),
IF(BI73>0, BH73*BD73^1.852, -BH73*BD73^1.852)) |
| Ligne 73 | Col 63 | BK73 | `=1.852*BH73*ABS(BI73)^(1.852-1)` | =1.852*BH73*ABS(BI73)^(1.852-1) |
| Ligne 73 | Col 64 | BL73 | `=BI73+$BD$75` | =BI73+$BD$75 |
| Ligne 74 | Col 4 | D74 | `=DIST_PHASE_1_v2!E63` | =DIST_PHASE_1_v2!E63 |
| Ligne 74 | Col 5 | E74 | `=DIST_PHASE_1_v2!G63` | =DIST_PHASE_1_v2!G63 |
| Ligne 74 | Col 6 | F74 | `=DIST_PHASE_1_v2!L63` | =DIST_PHASE_1_v2!L63 |
| Ligne 74 | Col 7 | G74 | `=DIST_PHASE_1_v2!M63` | =DIST_PHASE_1_v2!M63 |
| Ligne 74 | Col 8 | H74 | `=DIST_PHASE_1_v2!N63` | =DIST_PHASE_1_v2!N63 |
| Ligne 74 | Col 9 | I74 | `= (10.679 * H74) / ((F74/1000)^4.871 * G74^1.852)` | = (10.679 * H74) / ((F74/1000)^4.871 * G74^1.852) |
| Ligne 74 | Col 10 | J74 | `=IF(C74="positif",E74,IF(C74="negatif",-E74,""))` | =IF(C74="positif",E74,IF(C74="negatif",-E74,"")) |
| Ligne 74 | Col 11 | K74 | `=IF(J74>0,I74*E74^1.852,-I74*E74^1.852)` | =IF(J74>0,I74*E74^1.852,-I74*E74^1.852) |
| Ligne 74 | Col 12 | L74 | `=1.852*I74*ABS(E74)^(1.852-1)` | =1.852*I74*ABS(E74)^(1.852-1) |
| Ligne 74 | Col 13 | M74 | `=J74+$D$93` | =J74+$D$93 |
| Ligne 74 | Col 16 | P74 | `=IFERROR(MATCH(S74,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S74,$D$22:$D$91,0),0) |
| Ligne 74 | Col 18 | R74 | `=DIST_PHASE_1_v2!Q63` | =DIST_PHASE_1_v2!Q63 |
| Ligne 74 | Col 19 | S74 | `=DIST_PHASE_1_v2!R63` | =DIST_PHASE_1_v2!R63 |
| Ligne 74 | Col 20 | T74 | `=DIST_PHASE_1_v2!T63` | =DIST_PHASE_1_v2!T63 |
| Ligne 74 | Col 21 | U74 | `=DIST_PHASE_1_v2!Y63` | =DIST_PHASE_1_v2!Y63 |
| Ligne 74 | Col 23 | W74 | `=DIST_PHASE_1_v2!AA63` | =DIST_PHASE_1_v2!AA63 |
| Ligne 74 | Col 24 | X74 | `= (10.679 * W74) / ((U74/1000)^4.871 * V74^1.852)` | = (10.679 * W74) / ((U74/1000)^4.871 * V74^1.852) |
| Ligne 74 | Col 25 | Y74 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FB650>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FB650> |
| Ligne 74 | Col 26 | Z74 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA930>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA930> |
| Ligne 74 | Col 27 | AA74 | `=IF(P74>0,
IF(R74="positif",1,-1),
0)` | =IF(P74>0,
IF(R74="positif",1,-1),
0) |
| Ligne 74 | Col 28 | AB74 | `=X74*SIGN(Y74)*ABS(Y74)^1.852` | =X74*SIGN(Y74)*ABS(Y74)^1.852 |
| Ligne 74 | Col 29 | AC74 | `=1.852*X74*ABS(Y74)^(1.852-1)` | =1.852*X74*ABS(Y74)^(1.852-1) |
| Ligne 74 | Col 30 | AD74 | `=IF(P74>0,
Y74+($D$93*Z74)+(AA74*$S$93),
Y74+$S$93)` | =IF(P74>0,
Y74+($D$93*Z74)+(AA74*$S$93),
Y74+$S$93) |
| Ligne 74 | Col 32 | AF74 | `=ABS(AD74)-ABS(Y74)` | =ABS(AD74)-ABS(Y74) |
| Ligne 74 | Col 52 | AZ74 | `=COUNTIF(AZ22:AZ73,">0")` | =COUNTIF(AZ22:AZ73,">0") |
| Ligne 74 | Col 62 | BJ74 | `=SUM(BJ22:BJ73)` | =SUM(BJ22:BJ73) |
| Ligne 74 | Col 63 | BK74 | `=SUM(BK22:BK73)` | =SUM(BK22:BK73) |
| Ligne 75 | Col 4 | D75 | `=DIST_PHASE_1_v2!E64` | =DIST_PHASE_1_v2!E64 |
| Ligne 75 | Col 5 | E75 | `=DIST_PHASE_1_v2!G64` | =DIST_PHASE_1_v2!G64 |
| Ligne 75 | Col 6 | F75 | `=DIST_PHASE_1_v2!L64` | =DIST_PHASE_1_v2!L64 |
| Ligne 75 | Col 7 | G75 | `=DIST_PHASE_1_v2!M64` | =DIST_PHASE_1_v2!M64 |
| Ligne 75 | Col 8 | H75 | `=DIST_PHASE_1_v2!N64` | =DIST_PHASE_1_v2!N64 |
| Ligne 75 | Col 9 | I75 | `= (10.679 * H75) / ((F75/1000)^4.871 * G75^1.852)` | = (10.679 * H75) / ((F75/1000)^4.871 * G75^1.852) |
| Ligne 75 | Col 10 | J75 | `=IF(C75="positif",E75,IF(C75="negatif",-E75,""))` | =IF(C75="positif",E75,IF(C75="negatif",-E75,"")) |
| Ligne 75 | Col 11 | K75 | `=IF(J75>0,I75*E75^1.852,-I75*E75^1.852)` | =IF(J75>0,I75*E75^1.852,-I75*E75^1.852) |
| Ligne 75 | Col 12 | L75 | `=1.852*I75*ABS(E75)^(1.852-1)` | =1.852*I75*ABS(E75)^(1.852-1) |
| Ligne 75 | Col 13 | M75 | `=J75+$D$93` | =J75+$D$93 |
| Ligne 75 | Col 16 | P75 | `=IFERROR(MATCH(S75,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S75,$D$22:$D$91,0),0) |
| Ligne 75 | Col 18 | R75 | `=DIST_PHASE_1_v2!Q64` | =DIST_PHASE_1_v2!Q64 |
| Ligne 75 | Col 19 | S75 | `=DIST_PHASE_1_v2!R64` | =DIST_PHASE_1_v2!R64 |
| Ligne 75 | Col 20 | T75 | `=DIST_PHASE_1_v2!T64` | =DIST_PHASE_1_v2!T64 |
| Ligne 75 | Col 21 | U75 | `=DIST_PHASE_1_v2!Y64` | =DIST_PHASE_1_v2!Y64 |
| Ligne 75 | Col 23 | W75 | `=DIST_PHASE_1_v2!AA64` | =DIST_PHASE_1_v2!AA64 |
| Ligne 75 | Col 24 | X75 | `= (10.679 * W75) / ((U75/1000)^4.871 * V75^1.852)` | = (10.679 * W75) / ((U75/1000)^4.871 * V75^1.852) |
| Ligne 75 | Col 25 | Y75 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FB830>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FB830> |
| Ligne 75 | Col 26 | Z75 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA990>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA990> |
| Ligne 75 | Col 27 | AA75 | `=IF(P75>0,
IF(R75="positif",1,-1),
0)` | =IF(P75>0,
IF(R75="positif",1,-1),
0) |
| Ligne 75 | Col 28 | AB75 | `=X75*SIGN(Y75)*ABS(Y75)^1.852` | =X75*SIGN(Y75)*ABS(Y75)^1.852 |
| Ligne 75 | Col 29 | AC75 | `=1.852*X75*ABS(Y75)^(1.852-1)` | =1.852*X75*ABS(Y75)^(1.852-1) |
| Ligne 75 | Col 30 | AD75 | `=IF(P75>0,
Y75+($D$93*Z75)+(AA75*$S$93),
Y75+$S$93)` | =IF(P75>0,
Y75+($D$93*Z75)+(AA75*$S$93),
Y75+$S$93) |
| Ligne 75 | Col 32 | AF75 | `=ABS(AD75)-ABS(Y75)` | =ABS(AD75)-ABS(Y75) |
| Ligne 75 | Col 56 | BD75 | `=-(BJ74/BK74)` | =-(BJ74/BK74) |
| Ligne 76 | Col 4 | D76 | `=DIST_PHASE_1_v2!E65` | =DIST_PHASE_1_v2!E65 |
| Ligne 76 | Col 5 | E76 | `=DIST_PHASE_1_v2!G65` | =DIST_PHASE_1_v2!G65 |
| Ligne 76 | Col 6 | F76 | `=DIST_PHASE_1_v2!L65` | =DIST_PHASE_1_v2!L65 |
| Ligne 76 | Col 7 | G76 | `=DIST_PHASE_1_v2!M65` | =DIST_PHASE_1_v2!M65 |
| Ligne 76 | Col 8 | H76 | `=DIST_PHASE_1_v2!N65` | =DIST_PHASE_1_v2!N65 |
| Ligne 76 | Col 9 | I76 | `= (10.679 * H76) / ((F76/1000)^4.871 * G76^1.852)` | = (10.679 * H76) / ((F76/1000)^4.871 * G76^1.852) |
| Ligne 76 | Col 10 | J76 | `=IF(C76="positif",E76,IF(C76="negatif",-E76,""))` | =IF(C76="positif",E76,IF(C76="negatif",-E76,"")) |
| Ligne 76 | Col 11 | K76 | `=IF(J76>0,I76*E76^1.852,-I76*E76^1.852)` | =IF(J76>0,I76*E76^1.852,-I76*E76^1.852) |
| Ligne 76 | Col 12 | L76 | `=1.852*I76*ABS(E76)^(1.852-1)` | =1.852*I76*ABS(E76)^(1.852-1) |
| Ligne 76 | Col 13 | M76 | `=J76+$D$93` | =J76+$D$93 |
| Ligne 76 | Col 16 | P76 | `=IFERROR(MATCH(S76,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S76,$D$22:$D$91,0),0) |
| Ligne 76 | Col 18 | R76 | `=DIST_PHASE_1_v2!Q65` | =DIST_PHASE_1_v2!Q65 |
| Ligne 76 | Col 19 | S76 | `=DIST_PHASE_1_v2!R65` | =DIST_PHASE_1_v2!R65 |
| Ligne 76 | Col 20 | T76 | `=DIST_PHASE_1_v2!T65` | =DIST_PHASE_1_v2!T65 |
| Ligne 76 | Col 21 | U76 | `=DIST_PHASE_1_v2!Y65` | =DIST_PHASE_1_v2!Y65 |
| Ligne 76 | Col 23 | W76 | `=DIST_PHASE_1_v2!AA65` | =DIST_PHASE_1_v2!AA65 |
| Ligne 76 | Col 24 | X76 | `= (10.679 * W76) / ((U76/1000)^4.871 * V76^1.852)` | = (10.679 * W76) / ((U76/1000)^4.871 * V76^1.852) |
| Ligne 76 | Col 25 | Y76 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBA10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBA10> |
| Ligne 76 | Col 26 | Z76 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA9F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FA9F0> |
| Ligne 76 | Col 27 | AA76 | `=IF(P76>0,
IF(R76="positif",1,-1),
0)` | =IF(P76>0,
IF(R76="positif",1,-1),
0) |
| Ligne 76 | Col 28 | AB76 | `=X76*SIGN(Y76)*ABS(Y76)^1.852` | =X76*SIGN(Y76)*ABS(Y76)^1.852 |
| Ligne 76 | Col 29 | AC76 | `=1.852*X76*ABS(Y76)^(1.852-1)` | =1.852*X76*ABS(Y76)^(1.852-1) |
| Ligne 76 | Col 30 | AD76 | `=IF(P76>0,
Y76+($D$93*Z76)+(AA76*$S$93),
Y76+$S$93)` | =IF(P76>0,
Y76+($D$93*Z76)+(AA76*$S$93),
Y76+$S$93) |
| Ligne 76 | Col 32 | AF76 | `=ABS(AD76)-ABS(Y76)` | =ABS(AD76)-ABS(Y76) |
| Ligne 77 | Col 4 | D77 | `=DIST_PHASE_1_v2!E66` | =DIST_PHASE_1_v2!E66 |
| Ligne 77 | Col 5 | E77 | `=DIST_PHASE_1_v2!G66` | =DIST_PHASE_1_v2!G66 |
| Ligne 77 | Col 6 | F77 | `=DIST_PHASE_1_v2!L66` | =DIST_PHASE_1_v2!L66 |
| Ligne 77 | Col 7 | G77 | `=DIST_PHASE_1_v2!M66` | =DIST_PHASE_1_v2!M66 |
| Ligne 77 | Col 8 | H77 | `=DIST_PHASE_1_v2!N66` | =DIST_PHASE_1_v2!N66 |
| Ligne 77 | Col 9 | I77 | `= (10.679 * H77) / ((F77/1000)^4.871 * G77^1.852)` | = (10.679 * H77) / ((F77/1000)^4.871 * G77^1.852) |
| Ligne 77 | Col 10 | J77 | `=IF(C77="positif",E77,IF(C77="negatif",-E77,""))` | =IF(C77="positif",E77,IF(C77="negatif",-E77,"")) |
| Ligne 77 | Col 11 | K77 | `=IF(J77>0,I77*E77^1.852,-I77*E77^1.852)` | =IF(J77>0,I77*E77^1.852,-I77*E77^1.852) |
| Ligne 77 | Col 12 | L77 | `=1.852*I77*ABS(E77)^(1.852-1)` | =1.852*I77*ABS(E77)^(1.852-1) |
| Ligne 77 | Col 13 | M77 | `=J77+$D$93` | =J77+$D$93 |
| Ligne 77 | Col 16 | P77 | `=IFERROR(MATCH(S77,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S77,$D$22:$D$91,0),0) |
| Ligne 77 | Col 18 | R77 | `=DIST_PHASE_1_v2!Q66` | =DIST_PHASE_1_v2!Q66 |
| Ligne 77 | Col 19 | S77 | `=DIST_PHASE_1_v2!R66` | =DIST_PHASE_1_v2!R66 |
| Ligne 77 | Col 20 | T77 | `=DIST_PHASE_1_v2!T66` | =DIST_PHASE_1_v2!T66 |
| Ligne 77 | Col 21 | U77 | `=DIST_PHASE_1_v2!Y66` | =DIST_PHASE_1_v2!Y66 |
| Ligne 77 | Col 23 | W77 | `=DIST_PHASE_1_v2!AA66` | =DIST_PHASE_1_v2!AA66 |
| Ligne 77 | Col 24 | X77 | `= (10.679 * W77) / ((U77/1000)^4.871 * V77^1.852)` | = (10.679 * W77) / ((U77/1000)^4.871 * V77^1.852) |
| Ligne 77 | Col 25 | Y77 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBEF0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBEF0> |
| Ligne 77 | Col 26 | Z77 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBAD0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBAD0> |
| Ligne 77 | Col 27 | AA77 | `=IF(P77>0,
IF(R77="positif",1,-1),
0)` | =IF(P77>0,
IF(R77="positif",1,-1),
0) |
| Ligne 77 | Col 28 | AB77 | `=X77*SIGN(Y77)*ABS(Y77)^1.852` | =X77*SIGN(Y77)*ABS(Y77)^1.852 |
| Ligne 77 | Col 29 | AC77 | `=1.852*X77*ABS(Y77)^(1.852-1)` | =1.852*X77*ABS(Y77)^(1.852-1) |
| Ligne 77 | Col 30 | AD77 | `=IF(P77>0,
Y77+($D$93*Z77)+(AA77*$S$93),
Y77+$S$93)` | =IF(P77>0,
Y77+($D$93*Z77)+(AA77*$S$93),
Y77+$S$93) |
| Ligne 77 | Col 32 | AF77 | `=ABS(AD77)-ABS(Y77)` | =ABS(AD77)-ABS(Y77) |
| Ligne 78 | Col 4 | D78 | `=DIST_PHASE_1_v2!E67` | =DIST_PHASE_1_v2!E67 |
| Ligne 78 | Col 5 | E78 | `=DIST_PHASE_1_v2!G67` | =DIST_PHASE_1_v2!G67 |
| Ligne 78 | Col 6 | F78 | `=DIST_PHASE_1_v2!L67` | =DIST_PHASE_1_v2!L67 |
| Ligne 78 | Col 7 | G78 | `=DIST_PHASE_1_v2!M67` | =DIST_PHASE_1_v2!M67 |
| Ligne 78 | Col 8 | H78 | `=DIST_PHASE_1_v2!N67` | =DIST_PHASE_1_v2!N67 |
| Ligne 78 | Col 9 | I78 | `= (10.679 * H78) / ((F78/1000)^4.871 * G78^1.852)` | = (10.679 * H78) / ((F78/1000)^4.871 * G78^1.852) |
| Ligne 78 | Col 10 | J78 | `=IF(C78="positif",E78,IF(C78="negatif",-E78,""))` | =IF(C78="positif",E78,IF(C78="negatif",-E78,"")) |
| Ligne 78 | Col 11 | K78 | `=IF(J78>0,I78*E78^1.852,-I78*E78^1.852)` | =IF(J78>0,I78*E78^1.852,-I78*E78^1.852) |
| Ligne 78 | Col 12 | L78 | `=1.852*I78*ABS(E78)^(1.852-1)` | =1.852*I78*ABS(E78)^(1.852-1) |
| Ligne 78 | Col 13 | M78 | `=J78+$D$93` | =J78+$D$93 |
| Ligne 78 | Col 16 | P78 | `=IFERROR(MATCH(S78,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S78,$D$22:$D$91,0),0) |
| Ligne 78 | Col 18 | R78 | `=DIST_PHASE_1_v2!Q67` | =DIST_PHASE_1_v2!Q67 |
| Ligne 78 | Col 19 | S78 | `=DIST_PHASE_1_v2!R67` | =DIST_PHASE_1_v2!R67 |
| Ligne 78 | Col 20 | T78 | `=DIST_PHASE_1_v2!T67` | =DIST_PHASE_1_v2!T67 |
| Ligne 78 | Col 21 | U78 | `=DIST_PHASE_1_v2!Y67` | =DIST_PHASE_1_v2!Y67 |
| Ligne 78 | Col 23 | W78 | `=DIST_PHASE_1_v2!AA67` | =DIST_PHASE_1_v2!AA67 |
| Ligne 78 | Col 24 | X78 | `= (10.679 * W78) / ((U78/1000)^4.871 * V78^1.852)` | = (10.679 * W78) / ((U78/1000)^4.871 * V78^1.852) |
| Ligne 78 | Col 25 | Y78 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54110>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54110> |
| Ligne 78 | Col 26 | Z78 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBB30>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBB30> |
| Ligne 78 | Col 27 | AA78 | `=IF(P78>0,
IF(R78="positif",1,-1),
0)` | =IF(P78>0,
IF(R78="positif",1,-1),
0) |
| Ligne 78 | Col 28 | AB78 | `=X78*SIGN(Y78)*ABS(Y78)^1.852` | =X78*SIGN(Y78)*ABS(Y78)^1.852 |
| Ligne 78 | Col 29 | AC78 | `=1.852*X78*ABS(Y78)^(1.852-1)` | =1.852*X78*ABS(Y78)^(1.852-1) |
| Ligne 78 | Col 30 | AD78 | `=IF(P78>0,
Y78+($D$93*Z78)+(AA78*$S$93),
Y78+$S$93)` | =IF(P78>0,
Y78+($D$93*Z78)+(AA78*$S$93),
Y78+$S$93) |
| Ligne 78 | Col 32 | AF78 | `=ABS(AD78)-ABS(Y78)` | =ABS(AD78)-ABS(Y78) |
| Ligne 79 | Col 4 | D79 | `=DIST_PHASE_1_v2!E68` | =DIST_PHASE_1_v2!E68 |
| Ligne 79 | Col 5 | E79 | `=DIST_PHASE_1_v2!G68` | =DIST_PHASE_1_v2!G68 |
| Ligne 79 | Col 6 | F79 | `=DIST_PHASE_1_v2!L68` | =DIST_PHASE_1_v2!L68 |
| Ligne 79 | Col 7 | G79 | `=DIST_PHASE_1_v2!M68` | =DIST_PHASE_1_v2!M68 |
| Ligne 79 | Col 8 | H79 | `=DIST_PHASE_1_v2!N68` | =DIST_PHASE_1_v2!N68 |
| Ligne 79 | Col 9 | I79 | `= (10.679 * H79) / ((F79/1000)^4.871 * G79^1.852)` | = (10.679 * H79) / ((F79/1000)^4.871 * G79^1.852) |
| Ligne 79 | Col 10 | J79 | `=IF(C79="positif",E79,IF(C79="negatif",-E79,""))` | =IF(C79="positif",E79,IF(C79="negatif",-E79,"")) |
| Ligne 79 | Col 11 | K79 | `=IF(J79>0,I79*E79^1.852,-I79*E79^1.852)` | =IF(J79>0,I79*E79^1.852,-I79*E79^1.852) |
| Ligne 79 | Col 12 | L79 | `=1.852*I79*ABS(E79)^(1.852-1)` | =1.852*I79*ABS(E79)^(1.852-1) |
| Ligne 79 | Col 13 | M79 | `=J79+$D$93` | =J79+$D$93 |
| Ligne 79 | Col 16 | P79 | `=IFERROR(MATCH(S79,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S79,$D$22:$D$91,0),0) |
| Ligne 79 | Col 18 | R79 | `=DIST_PHASE_1_v2!Q68` | =DIST_PHASE_1_v2!Q68 |
| Ligne 79 | Col 19 | S79 | `=DIST_PHASE_1_v2!R68` | =DIST_PHASE_1_v2!R68 |
| Ligne 79 | Col 20 | T79 | `=DIST_PHASE_1_v2!T68` | =DIST_PHASE_1_v2!T68 |
| Ligne 79 | Col 21 | U79 | `=DIST_PHASE_1_v2!Y68` | =DIST_PHASE_1_v2!Y68 |
| Ligne 79 | Col 23 | W79 | `=DIST_PHASE_1_v2!AA68` | =DIST_PHASE_1_v2!AA68 |
| Ligne 79 | Col 24 | X79 | `= (10.679 * W79) / ((U79/1000)^4.871 * V79^1.852)` | = (10.679 * W79) / ((U79/1000)^4.871 * V79^1.852) |
| Ligne 79 | Col 25 | Y79 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA542F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA542F0> |
| Ligne 79 | Col 26 | Z79 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBB90>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBB90> |
| Ligne 79 | Col 27 | AA79 | `=IF(P79>0,
IF(R79="positif",1,-1),
0)` | =IF(P79>0,
IF(R79="positif",1,-1),
0) |
| Ligne 79 | Col 28 | AB79 | `=X79*SIGN(Y79)*ABS(Y79)^1.852` | =X79*SIGN(Y79)*ABS(Y79)^1.852 |
| Ligne 79 | Col 29 | AC79 | `=1.852*X79*ABS(Y79)^(1.852-1)` | =1.852*X79*ABS(Y79)^(1.852-1) |
| Ligne 79 | Col 30 | AD79 | `=IF(P79>0,
Y79+($D$93*Z79)+(AA79*$S$93),
Y79+$S$93)` | =IF(P79>0,
Y79+($D$93*Z79)+(AA79*$S$93),
Y79+$S$93) |
| Ligne 79 | Col 32 | AF79 | `=ABS(AD79)-ABS(Y79)` | =ABS(AD79)-ABS(Y79) |
| Ligne 80 | Col 4 | D80 | `=DIST_PHASE_1_v2!E69` | =DIST_PHASE_1_v2!E69 |
| Ligne 80 | Col 5 | E80 | `=DIST_PHASE_1_v2!G69` | =DIST_PHASE_1_v2!G69 |
| Ligne 80 | Col 6 | F80 | `=DIST_PHASE_1_v2!L69` | =DIST_PHASE_1_v2!L69 |
| Ligne 80 | Col 7 | G80 | `=DIST_PHASE_1_v2!M69` | =DIST_PHASE_1_v2!M69 |
| Ligne 80 | Col 8 | H80 | `=DIST_PHASE_1_v2!N69` | =DIST_PHASE_1_v2!N69 |
| Ligne 80 | Col 9 | I80 | `= (10.679 * H80) / ((F80/1000)^4.871 * G80^1.852)` | = (10.679 * H80) / ((F80/1000)^4.871 * G80^1.852) |
| Ligne 80 | Col 10 | J80 | `=IF(C80="positif",E80,IF(C80="negatif",-E80,""))` | =IF(C80="positif",E80,IF(C80="negatif",-E80,"")) |
| Ligne 80 | Col 11 | K80 | `=IF(J80>0,I80*E80^1.852,-I80*E80^1.852)` | =IF(J80>0,I80*E80^1.852,-I80*E80^1.852) |
| Ligne 80 | Col 12 | L80 | `=1.852*I80*ABS(E80)^(1.852-1)` | =1.852*I80*ABS(E80)^(1.852-1) |
| Ligne 80 | Col 13 | M80 | `=J80+$D$93` | =J80+$D$93 |
| Ligne 80 | Col 16 | P80 | `=IFERROR(MATCH(S80,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S80,$D$22:$D$91,0),0) |
| Ligne 80 | Col 18 | R80 | `=DIST_PHASE_1_v2!Q69` | =DIST_PHASE_1_v2!Q69 |
| Ligne 80 | Col 19 | S80 | `=DIST_PHASE_1_v2!R69` | =DIST_PHASE_1_v2!R69 |
| Ligne 80 | Col 20 | T80 | `=DIST_PHASE_1_v2!T69` | =DIST_PHASE_1_v2!T69 |
| Ligne 80 | Col 21 | U80 | `=DIST_PHASE_1_v2!Y69` | =DIST_PHASE_1_v2!Y69 |
| Ligne 80 | Col 23 | W80 | `=DIST_PHASE_1_v2!AA69` | =DIST_PHASE_1_v2!AA69 |
| Ligne 80 | Col 24 | X80 | `= (10.679 * W80) / ((U80/1000)^4.871 * V80^1.852)` | = (10.679 * W80) / ((U80/1000)^4.871 * V80^1.852) |
| Ligne 80 | Col 25 | Y80 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA544D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA544D0> |
| Ligne 80 | Col 26 | Z80 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBBF0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBBF0> |
| Ligne 80 | Col 27 | AA80 | `=IF(P80>0,
IF(R80="positif",1,-1),
0)` | =IF(P80>0,
IF(R80="positif",1,-1),
0) |
| Ligne 80 | Col 28 | AB80 | `=X80*SIGN(Y80)*ABS(Y80)^1.852` | =X80*SIGN(Y80)*ABS(Y80)^1.852 |
| Ligne 80 | Col 29 | AC80 | `=1.852*X80*ABS(Y80)^(1.852-1)` | =1.852*X80*ABS(Y80)^(1.852-1) |
| Ligne 80 | Col 30 | AD80 | `=IF(P80>0,
Y80+($D$93*Z80)+(AA80*$S$93),
Y80+$S$93)` | =IF(P80>0,
Y80+($D$93*Z80)+(AA80*$S$93),
Y80+$S$93) |
| Ligne 80 | Col 32 | AF80 | `=ABS(AD80)-ABS(Y80)` | =ABS(AD80)-ABS(Y80) |
| Ligne 81 | Col 4 | D81 | `=DIST_PHASE_1_v2!E70` | =DIST_PHASE_1_v2!E70 |
| Ligne 81 | Col 5 | E81 | `=DIST_PHASE_1_v2!G70` | =DIST_PHASE_1_v2!G70 |
| Ligne 81 | Col 6 | F81 | `=DIST_PHASE_1_v2!L70` | =DIST_PHASE_1_v2!L70 |
| Ligne 81 | Col 7 | G81 | `=DIST_PHASE_1_v2!M70` | =DIST_PHASE_1_v2!M70 |
| Ligne 81 | Col 8 | H81 | `=DIST_PHASE_1_v2!N70` | =DIST_PHASE_1_v2!N70 |
| Ligne 81 | Col 9 | I81 | `= (10.679 * H81) / ((F81/1000)^4.871 * G81^1.852)` | = (10.679 * H81) / ((F81/1000)^4.871 * G81^1.852) |
| Ligne 81 | Col 10 | J81 | `=IF(C81="positif",E81,IF(C81="negatif",-E81,""))` | =IF(C81="positif",E81,IF(C81="negatif",-E81,"")) |
| Ligne 81 | Col 11 | K81 | `=IF(J81>0,I81*E81^1.852,-I81*E81^1.852)` | =IF(J81>0,I81*E81^1.852,-I81*E81^1.852) |
| Ligne 81 | Col 12 | L81 | `=1.852*I81*ABS(E81)^(1.852-1)` | =1.852*I81*ABS(E81)^(1.852-1) |
| Ligne 81 | Col 13 | M81 | `=J81+$D$93` | =J81+$D$93 |
| Ligne 81 | Col 16 | P81 | `=IFERROR(MATCH(S81,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S81,$D$22:$D$91,0),0) |
| Ligne 81 | Col 18 | R81 | `=DIST_PHASE_1_v2!Q70` | =DIST_PHASE_1_v2!Q70 |
| Ligne 81 | Col 19 | S81 | `=DIST_PHASE_1_v2!R70` | =DIST_PHASE_1_v2!R70 |
| Ligne 81 | Col 20 | T81 | `=DIST_PHASE_1_v2!T70` | =DIST_PHASE_1_v2!T70 |
| Ligne 81 | Col 21 | U81 | `=DIST_PHASE_1_v2!Y70` | =DIST_PHASE_1_v2!Y70 |
| Ligne 81 | Col 23 | W81 | `=DIST_PHASE_1_v2!AA70` | =DIST_PHASE_1_v2!AA70 |
| Ligne 81 | Col 24 | X81 | `= (10.679 * W81) / ((U81/1000)^4.871 * V81^1.852)` | = (10.679 * W81) / ((U81/1000)^4.871 * V81^1.852) |
| Ligne 81 | Col 25 | Y81 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA546B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA546B0> |
| Ligne 81 | Col 26 | Z81 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBC50>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBC50> |
| Ligne 81 | Col 27 | AA81 | `=IF(P81>0,
IF(R81="positif",1,-1),
0)` | =IF(P81>0,
IF(R81="positif",1,-1),
0) |
| Ligne 81 | Col 28 | AB81 | `=X81*SIGN(Y81)*ABS(Y81)^1.852` | =X81*SIGN(Y81)*ABS(Y81)^1.852 |
| Ligne 81 | Col 29 | AC81 | `=1.852*X81*ABS(Y81)^(1.852-1)` | =1.852*X81*ABS(Y81)^(1.852-1) |
| Ligne 81 | Col 30 | AD81 | `=IF(P81>0,
Y81+($D$93*Z81)+(AA81*$S$93),
Y81+$S$93)` | =IF(P81>0,
Y81+($D$93*Z81)+(AA81*$S$93),
Y81+$S$93) |
| Ligne 81 | Col 32 | AF81 | `=ABS(AD81)-ABS(Y81)` | =ABS(AD81)-ABS(Y81) |
| Ligne 82 | Col 4 | D82 | `=DIST_PHASE_1_v2!E71` | =DIST_PHASE_1_v2!E71 |
| Ligne 82 | Col 5 | E82 | `=DIST_PHASE_1_v2!G71` | =DIST_PHASE_1_v2!G71 |
| Ligne 82 | Col 6 | F82 | `=DIST_PHASE_1_v2!L71` | =DIST_PHASE_1_v2!L71 |
| Ligne 82 | Col 7 | G82 | `=DIST_PHASE_1_v2!M71` | =DIST_PHASE_1_v2!M71 |
| Ligne 82 | Col 8 | H82 | `=DIST_PHASE_1_v2!N71` | =DIST_PHASE_1_v2!N71 |
| Ligne 82 | Col 9 | I82 | `= (10.679 * H82) / ((F82/1000)^4.871 * G82^1.852)` | = (10.679 * H82) / ((F82/1000)^4.871 * G82^1.852) |
| Ligne 82 | Col 10 | J82 | `=IF(C82="positif",E82,IF(C82="negatif",-E82,""))` | =IF(C82="positif",E82,IF(C82="negatif",-E82,"")) |
| Ligne 82 | Col 11 | K82 | `=IF(J82>0,I82*E82^1.852,-I82*E82^1.852)` | =IF(J82>0,I82*E82^1.852,-I82*E82^1.852) |
| Ligne 82 | Col 12 | L82 | `=1.852*I82*ABS(E82)^(1.852-1)` | =1.852*I82*ABS(E82)^(1.852-1) |
| Ligne 82 | Col 13 | M82 | `=J82+$D$93` | =J82+$D$93 |
| Ligne 82 | Col 16 | P82 | `=IFERROR(MATCH(S82,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S82,$D$22:$D$91,0),0) |
| Ligne 82 | Col 18 | R82 | `=DIST_PHASE_1_v2!Q71` | =DIST_PHASE_1_v2!Q71 |
| Ligne 82 | Col 19 | S82 | `=DIST_PHASE_1_v2!R71` | =DIST_PHASE_1_v2!R71 |
| Ligne 82 | Col 20 | T82 | `=DIST_PHASE_1_v2!T71` | =DIST_PHASE_1_v2!T71 |
| Ligne 82 | Col 21 | U82 | `=DIST_PHASE_1_v2!Y71` | =DIST_PHASE_1_v2!Y71 |
| Ligne 82 | Col 23 | W82 | `=DIST_PHASE_1_v2!AA71` | =DIST_PHASE_1_v2!AA71 |
| Ligne 82 | Col 24 | X82 | `= (10.679 * W82) / ((U82/1000)^4.871 * V82^1.852)` | = (10.679 * W82) / ((U82/1000)^4.871 * V82^1.852) |
| Ligne 82 | Col 25 | Y82 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54890>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54890> |
| Ligne 82 | Col 26 | Z82 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBCB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBCB0> |
| Ligne 82 | Col 27 | AA82 | `=IF(P82>0,
IF(R82="positif",1,-1),
0)` | =IF(P82>0,
IF(R82="positif",1,-1),
0) |
| Ligne 82 | Col 28 | AB82 | `=X82*SIGN(Y82)*ABS(Y82)^1.852` | =X82*SIGN(Y82)*ABS(Y82)^1.852 |
| Ligne 82 | Col 29 | AC82 | `=1.852*X82*ABS(Y82)^(1.852-1)` | =1.852*X82*ABS(Y82)^(1.852-1) |
| Ligne 82 | Col 30 | AD82 | `=IF(P82>0,
Y82+($D$93*Z82)+(AA82*$S$93),
Y82+$S$93)` | =IF(P82>0,
Y82+($D$93*Z82)+(AA82*$S$93),
Y82+$S$93) |
| Ligne 82 | Col 32 | AF82 | `=ABS(AD82)-ABS(Y82)` | =ABS(AD82)-ABS(Y82) |
| Ligne 83 | Col 4 | D83 | `=DIST_PHASE_1_v2!E72` | =DIST_PHASE_1_v2!E72 |
| Ligne 83 | Col 5 | E83 | `=DIST_PHASE_1_v2!G72` | =DIST_PHASE_1_v2!G72 |
| Ligne 83 | Col 6 | F83 | `=DIST_PHASE_1_v2!L72` | =DIST_PHASE_1_v2!L72 |
| Ligne 83 | Col 7 | G83 | `=DIST_PHASE_1_v2!M72` | =DIST_PHASE_1_v2!M72 |
| Ligne 83 | Col 8 | H83 | `=DIST_PHASE_1_v2!N72` | =DIST_PHASE_1_v2!N72 |
| Ligne 83 | Col 9 | I83 | `= (10.679 * H83) / ((F83/1000)^4.871 * G83^1.852)` | = (10.679 * H83) / ((F83/1000)^4.871 * G83^1.852) |
| Ligne 83 | Col 10 | J83 | `=IF(C83="positif",E83,IF(C83="negatif",-E83,""))` | =IF(C83="positif",E83,IF(C83="negatif",-E83,"")) |
| Ligne 83 | Col 11 | K83 | `=IF(J83>0,I83*E83^1.852,-I83*E83^1.852)` | =IF(J83>0,I83*E83^1.852,-I83*E83^1.852) |
| Ligne 83 | Col 12 | L83 | `=1.852*I83*ABS(E83)^(1.852-1)` | =1.852*I83*ABS(E83)^(1.852-1) |
| Ligne 83 | Col 13 | M83 | `=J83+$D$93` | =J83+$D$93 |
| Ligne 83 | Col 16 | P83 | `=IFERROR(MATCH(S83,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S83,$D$22:$D$91,0),0) |
| Ligne 83 | Col 18 | R83 | `=DIST_PHASE_1_v2!Q72` | =DIST_PHASE_1_v2!Q72 |
| Ligne 83 | Col 19 | S83 | `=DIST_PHASE_1_v2!R72` | =DIST_PHASE_1_v2!R72 |
| Ligne 83 | Col 20 | T83 | `=DIST_PHASE_1_v2!T72` | =DIST_PHASE_1_v2!T72 |
| Ligne 83 | Col 21 | U83 | `=DIST_PHASE_1_v2!Y72` | =DIST_PHASE_1_v2!Y72 |
| Ligne 83 | Col 23 | W83 | `=DIST_PHASE_1_v2!AA72` | =DIST_PHASE_1_v2!AA72 |
| Ligne 83 | Col 24 | X83 | `= (10.679 * W83) / ((U83/1000)^4.871 * V83^1.852)` | = (10.679 * W83) / ((U83/1000)^4.871 * V83^1.852) |
| Ligne 83 | Col 25 | Y83 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54A70>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54A70> |
| Ligne 83 | Col 26 | Z83 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBD10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBD10> |
| Ligne 83 | Col 27 | AA83 | `=IF(P83>0,
IF(R83="positif",1,-1),
0)` | =IF(P83>0,
IF(R83="positif",1,-1),
0) |
| Ligne 83 | Col 28 | AB83 | `=X83*SIGN(Y83)*ABS(Y83)^1.852` | =X83*SIGN(Y83)*ABS(Y83)^1.852 |
| Ligne 83 | Col 29 | AC83 | `=1.852*X83*ABS(Y83)^(1.852-1)` | =1.852*X83*ABS(Y83)^(1.852-1) |
| Ligne 83 | Col 30 | AD83 | `=IF(P83>0,
Y83+($D$93*Z83)+(AA83*$S$93),
Y83+$S$93)` | =IF(P83>0,
Y83+($D$93*Z83)+(AA83*$S$93),
Y83+$S$93) |
| Ligne 83 | Col 32 | AF83 | `=ABS(AD83)-ABS(Y83)` | =ABS(AD83)-ABS(Y83) |
| Ligne 84 | Col 4 | D84 | `=DIST_PHASE_1_v2!E73` | =DIST_PHASE_1_v2!E73 |
| Ligne 84 | Col 5 | E84 | `=DIST_PHASE_1_v2!G73` | =DIST_PHASE_1_v2!G73 |
| Ligne 84 | Col 6 | F84 | `=DIST_PHASE_1_v2!L73` | =DIST_PHASE_1_v2!L73 |
| Ligne 84 | Col 7 | G84 | `=DIST_PHASE_1_v2!M73` | =DIST_PHASE_1_v2!M73 |
| Ligne 84 | Col 8 | H84 | `=DIST_PHASE_1_v2!N73` | =DIST_PHASE_1_v2!N73 |
| Ligne 84 | Col 9 | I84 | `= (10.679 * H84) / ((F84/1000)^4.871 * G84^1.852)` | = (10.679 * H84) / ((F84/1000)^4.871 * G84^1.852) |
| Ligne 84 | Col 10 | J84 | `=IF(C84="positif",E84,IF(C84="negatif",-E84,""))` | =IF(C84="positif",E84,IF(C84="negatif",-E84,"")) |
| Ligne 84 | Col 11 | K84 | `=IF(J84>0,I84*E84^1.852,-I84*E84^1.852)` | =IF(J84>0,I84*E84^1.852,-I84*E84^1.852) |
| Ligne 84 | Col 12 | L84 | `=1.852*I84*ABS(E84)^(1.852-1)` | =1.852*I84*ABS(E84)^(1.852-1) |
| Ligne 84 | Col 13 | M84 | `=J84+$D$93` | =J84+$D$93 |
| Ligne 84 | Col 16 | P84 | `=IFERROR(MATCH(S84,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S84,$D$22:$D$91,0),0) |
| Ligne 84 | Col 18 | R84 | `=DIST_PHASE_1_v2!Q73` | =DIST_PHASE_1_v2!Q73 |
| Ligne 84 | Col 19 | S84 | `=DIST_PHASE_1_v2!R73` | =DIST_PHASE_1_v2!R73 |
| Ligne 84 | Col 20 | T84 | `=DIST_PHASE_1_v2!T73` | =DIST_PHASE_1_v2!T73 |
| Ligne 84 | Col 21 | U84 | `=DIST_PHASE_1_v2!Y73` | =DIST_PHASE_1_v2!Y73 |
| Ligne 84 | Col 23 | W84 | `=DIST_PHASE_1_v2!AA73` | =DIST_PHASE_1_v2!AA73 |
| Ligne 84 | Col 24 | X84 | `= (10.679 * W84) / ((U84/1000)^4.871 * V84^1.852)` | = (10.679 * W84) / ((U84/1000)^4.871 * V84^1.852) |
| Ligne 84 | Col 25 | Y84 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54C50>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54C50> |
| Ligne 84 | Col 26 | Z84 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBD70>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDD9FBD70> |
| Ligne 84 | Col 27 | AA84 | `=IF(P84>0,
IF(R84="positif",1,-1),
0)` | =IF(P84>0,
IF(R84="positif",1,-1),
0) |
| Ligne 84 | Col 28 | AB84 | `=X84*SIGN(Y84)*ABS(Y84)^1.852` | =X84*SIGN(Y84)*ABS(Y84)^1.852 |
| Ligne 84 | Col 29 | AC84 | `=1.852*X84*ABS(Y84)^(1.852-1)` | =1.852*X84*ABS(Y84)^(1.852-1) |
| Ligne 84 | Col 30 | AD84 | `=IF(P84>0,
Y84+($D$93*Z84)+(AA84*$S$93),
Y84+$S$93)` | =IF(P84>0,
Y84+($D$93*Z84)+(AA84*$S$93),
Y84+$S$93) |
| Ligne 84 | Col 32 | AF84 | `=ABS(AD84)-ABS(Y84)` | =ABS(AD84)-ABS(Y84) |
| Ligne 85 | Col 4 | D85 | `=DIST_PHASE_1_v2!E74` | =DIST_PHASE_1_v2!E74 |
| Ligne 85 | Col 5 | E85 | `=DIST_PHASE_1_v2!G74` | =DIST_PHASE_1_v2!G74 |
| Ligne 85 | Col 6 | F85 | `=DIST_PHASE_1_v2!L74` | =DIST_PHASE_1_v2!L74 |
| Ligne 85 | Col 7 | G85 | `=DIST_PHASE_1_v2!M74` | =DIST_PHASE_1_v2!M74 |
| Ligne 85 | Col 8 | H85 | `=DIST_PHASE_1_v2!N74` | =DIST_PHASE_1_v2!N74 |
| Ligne 85 | Col 9 | I85 | `= (10.679 * H85) / ((F85/1000)^4.871 * G85^1.852)` | = (10.679 * H85) / ((F85/1000)^4.871 * G85^1.852) |
| Ligne 85 | Col 10 | J85 | `=IF(C85="positif",E85,IF(C85="negatif",-E85,""))` | =IF(C85="positif",E85,IF(C85="negatif",-E85,"")) |
| Ligne 85 | Col 11 | K85 | `=IF(J85>0,I85*E85^1.852,-I85*E85^1.852)` | =IF(J85>0,I85*E85^1.852,-I85*E85^1.852) |
| Ligne 85 | Col 12 | L85 | `=1.852*I85*ABS(E85)^(1.852-1)` | =1.852*I85*ABS(E85)^(1.852-1) |
| Ligne 85 | Col 13 | M85 | `=J85+$D$93` | =J85+$D$93 |
| Ligne 85 | Col 16 | P85 | `=IFERROR(MATCH(S85,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S85,$D$22:$D$91,0),0) |
| Ligne 85 | Col 18 | R85 | `=DIST_PHASE_1_v2!Q74` | =DIST_PHASE_1_v2!Q74 |
| Ligne 85 | Col 19 | S85 | `=DIST_PHASE_1_v2!R74` | =DIST_PHASE_1_v2!R74 |
| Ligne 85 | Col 20 | T85 | `=DIST_PHASE_1_v2!T74` | =DIST_PHASE_1_v2!T74 |
| Ligne 85 | Col 21 | U85 | `=DIST_PHASE_1_v2!Y74` | =DIST_PHASE_1_v2!Y74 |
| Ligne 85 | Col 23 | W85 | `=DIST_PHASE_1_v2!AA74` | =DIST_PHASE_1_v2!AA74 |
| Ligne 85 | Col 24 | X85 | `= (10.679 * W85) / ((U85/1000)^4.871 * V85^1.852)` | = (10.679 * W85) / ((U85/1000)^4.871 * V85^1.852) |
| Ligne 85 | Col 25 | Y85 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA551F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA551F0> |
| Ligne 85 | Col 26 | Z85 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54D10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54D10> |
| Ligne 85 | Col 27 | AA85 | `=IF(P85>0,
IF(R85="positif",1,-1),
0)` | =IF(P85>0,
IF(R85="positif",1,-1),
0) |
| Ligne 85 | Col 28 | AB85 | `=X85*SIGN(Y85)*ABS(Y85)^1.852` | =X85*SIGN(Y85)*ABS(Y85)^1.852 |
| Ligne 85 | Col 29 | AC85 | `=1.852*X85*ABS(Y85)^(1.852-1)` | =1.852*X85*ABS(Y85)^(1.852-1) |
| Ligne 85 | Col 30 | AD85 | `=IF(P85>0,
Y85+($D$93*Z85)+(AA85*$S$93),
Y85+$S$93)` | =IF(P85>0,
Y85+($D$93*Z85)+(AA85*$S$93),
Y85+$S$93) |
| Ligne 85 | Col 32 | AF85 | `=ABS(AD85)-ABS(Y85)` | =ABS(AD85)-ABS(Y85) |
| Ligne 86 | Col 4 | D86 | `=DIST_PHASE_1_v2!E75` | =DIST_PHASE_1_v2!E75 |
| Ligne 86 | Col 5 | E86 | `=DIST_PHASE_1_v2!G75` | =DIST_PHASE_1_v2!G75 |
| Ligne 86 | Col 6 | F86 | `=DIST_PHASE_1_v2!L75` | =DIST_PHASE_1_v2!L75 |
| Ligne 86 | Col 7 | G86 | `=DIST_PHASE_1_v2!M75` | =DIST_PHASE_1_v2!M75 |
| Ligne 86 | Col 8 | H86 | `=DIST_PHASE_1_v2!N75` | =DIST_PHASE_1_v2!N75 |
| Ligne 86 | Col 9 | I86 | `= (10.679 * H86) / ((F86/1000)^4.871 * G86^1.852)` | = (10.679 * H86) / ((F86/1000)^4.871 * G86^1.852) |
| Ligne 86 | Col 10 | J86 | `=IF(C86="positif",E86,IF(C86="negatif",-E86,""))` | =IF(C86="positif",E86,IF(C86="negatif",-E86,"")) |
| Ligne 86 | Col 11 | K86 | `=IF(J86>0,I86*E86^1.852,-I86*E86^1.852)` | =IF(J86>0,I86*E86^1.852,-I86*E86^1.852) |
| Ligne 86 | Col 12 | L86 | `=1.852*I86*ABS(E86)^(1.852-1)` | =1.852*I86*ABS(E86)^(1.852-1) |
| Ligne 86 | Col 13 | M86 | `=J86+$D$93` | =J86+$D$93 |
| Ligne 86 | Col 16 | P86 | `=IFERROR(MATCH(S86,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S86,$D$22:$D$91,0),0) |
| Ligne 86 | Col 18 | R86 | `=DIST_PHASE_1_v2!Q75` | =DIST_PHASE_1_v2!Q75 |
| Ligne 86 | Col 19 | S86 | `=DIST_PHASE_1_v2!R75` | =DIST_PHASE_1_v2!R75 |
| Ligne 86 | Col 20 | T86 | `=DIST_PHASE_1_v2!T75` | =DIST_PHASE_1_v2!T75 |
| Ligne 86 | Col 21 | U86 | `=DIST_PHASE_1_v2!Y75` | =DIST_PHASE_1_v2!Y75 |
| Ligne 86 | Col 23 | W86 | `=DIST_PHASE_1_v2!AA75` | =DIST_PHASE_1_v2!AA75 |
| Ligne 86 | Col 24 | X86 | `= (10.679 * W86) / ((U86/1000)^4.871 * V86^1.852)` | = (10.679 * W86) / ((U86/1000)^4.871 * V86^1.852) |
| Ligne 86 | Col 25 | Y86 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA553D0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA553D0> |
| Ligne 86 | Col 26 | Z86 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54D70>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54D70> |
| Ligne 86 | Col 27 | AA86 | `=IF(P86>0,
IF(R86="positif",1,-1),
0)` | =IF(P86>0,
IF(R86="positif",1,-1),
0) |
| Ligne 86 | Col 28 | AB86 | `=X86*SIGN(Y86)*ABS(Y86)^1.852` | =X86*SIGN(Y86)*ABS(Y86)^1.852 |
| Ligne 86 | Col 29 | AC86 | `=1.852*X86*ABS(Y86)^(1.852-1)` | =1.852*X86*ABS(Y86)^(1.852-1) |
| Ligne 86 | Col 30 | AD86 | `=IF(P86>0,
Y86+($D$93*Z86)+(AA86*$S$93),
Y86+$S$93)` | =IF(P86>0,
Y86+($D$93*Z86)+(AA86*$S$93),
Y86+$S$93) |
| Ligne 86 | Col 32 | AF86 | `=ABS(AD86)-ABS(Y86)` | =ABS(AD86)-ABS(Y86) |
| Ligne 87 | Col 4 | D87 | `=DIST_PHASE_1_v2!E76` | =DIST_PHASE_1_v2!E76 |
| Ligne 87 | Col 5 | E87 | `=DIST_PHASE_1_v2!G76` | =DIST_PHASE_1_v2!G76 |
| Ligne 87 | Col 6 | F87 | `=DIST_PHASE_1_v2!L76` | =DIST_PHASE_1_v2!L76 |
| Ligne 87 | Col 7 | G87 | `=DIST_PHASE_1_v2!M76` | =DIST_PHASE_1_v2!M76 |
| Ligne 87 | Col 8 | H87 | `=DIST_PHASE_1_v2!N76` | =DIST_PHASE_1_v2!N76 |
| Ligne 87 | Col 9 | I87 | `= (10.679 * H87) / ((F87/1000)^4.871 * G87^1.852)` | = (10.679 * H87) / ((F87/1000)^4.871 * G87^1.852) |
| Ligne 87 | Col 10 | J87 | `=IF(C87="positif",E87,IF(C87="negatif",-E87,""))` | =IF(C87="positif",E87,IF(C87="negatif",-E87,"")) |
| Ligne 87 | Col 11 | K87 | `=IF(J87>0,I87*E87^1.852,-I87*E87^1.852)` | =IF(J87>0,I87*E87^1.852,-I87*E87^1.852) |
| Ligne 87 | Col 12 | L87 | `=1.852*I87*ABS(E87)^(1.852-1)` | =1.852*I87*ABS(E87)^(1.852-1) |
| Ligne 87 | Col 13 | M87 | `=J87+$D$93` | =J87+$D$93 |
| Ligne 87 | Col 16 | P87 | `=IFERROR(MATCH(S87,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S87,$D$22:$D$91,0),0) |
| Ligne 87 | Col 18 | R87 | `=DIST_PHASE_1_v2!Q76` | =DIST_PHASE_1_v2!Q76 |
| Ligne 87 | Col 19 | S87 | `=DIST_PHASE_1_v2!R76` | =DIST_PHASE_1_v2!R76 |
| Ligne 87 | Col 20 | T87 | `=DIST_PHASE_1_v2!T76` | =DIST_PHASE_1_v2!T76 |
| Ligne 87 | Col 21 | U87 | `=DIST_PHASE_1_v2!Y76` | =DIST_PHASE_1_v2!Y76 |
| Ligne 87 | Col 23 | W87 | `=DIST_PHASE_1_v2!AA76` | =DIST_PHASE_1_v2!AA76 |
| Ligne 87 | Col 24 | X87 | `= (10.679 * W87) / ((U87/1000)^4.871 * V87^1.852)` | = (10.679 * W87) / ((U87/1000)^4.871 * V87^1.852) |
| Ligne 87 | Col 25 | Y87 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA558B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA558B0> |
| Ligne 87 | Col 26 | Z87 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54EF0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54EF0> |
| Ligne 87 | Col 27 | AA87 | `=IF(P87>0,
        IF(R87="positif",1,-1),
        0)` | =IF(P87>0,
        IF(R87="positif",1,-1),
        0) |
| Ligne 87 | Col 28 | AB87 | `=X87*SIGN(Y87)*ABS(Y87)^1.852` | =X87*SIGN(Y87)*ABS(Y87)^1.852 |
| Ligne 87 | Col 29 | AC87 | `=1.852*X87*ABS(Y87)^(1.852-1)` | =1.852*X87*ABS(Y87)^(1.852-1) |
| Ligne 87 | Col 30 | AD87 | `=IF(P87>0,
Y87+($D$93*Z87)+(AA87*$S$93),
Y87+$S$93)` | =IF(P87>0,
Y87+($D$93*Z87)+(AA87*$S$93),
Y87+$S$93) |
| Ligne 87 | Col 32 | AF87 | `=ABS(AD87)-ABS(Y87)` | =ABS(AD87)-ABS(Y87) |
| Ligne 88 | Col 4 | D88 | `=DIST_PHASE_1_v2!E77` | =DIST_PHASE_1_v2!E77 |
| Ligne 88 | Col 5 | E88 | `=DIST_PHASE_1_v2!G77` | =DIST_PHASE_1_v2!G77 |
| Ligne 88 | Col 6 | F88 | `=DIST_PHASE_1_v2!L77` | =DIST_PHASE_1_v2!L77 |
| Ligne 88 | Col 7 | G88 | `=DIST_PHASE_1_v2!M77` | =DIST_PHASE_1_v2!M77 |
| Ligne 88 | Col 8 | H88 | `=DIST_PHASE_1_v2!N77` | =DIST_PHASE_1_v2!N77 |
| Ligne 88 | Col 9 | I88 | `= (10.679 * H88) / ((F88/1000)^4.871 * G88^1.852)` | = (10.679 * H88) / ((F88/1000)^4.871 * G88^1.852) |
| Ligne 88 | Col 10 | J88 | `=IF(C88="positif",E88,IF(C88="negatif",-E88,""))` | =IF(C88="positif",E88,IF(C88="negatif",-E88,"")) |
| Ligne 88 | Col 11 | K88 | `=IF(J88>0,I88*E88^1.852,-I88*E88^1.852)` | =IF(J88>0,I88*E88^1.852,-I88*E88^1.852) |
| Ligne 88 | Col 12 | L88 | `=1.852*I88*ABS(E88)^(1.852-1)` | =1.852*I88*ABS(E88)^(1.852-1) |
| Ligne 88 | Col 13 | M88 | `=J88+$D$93` | =J88+$D$93 |
| Ligne 88 | Col 16 | P88 | `=IFERROR(MATCH(S88,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S88,$D$22:$D$91,0),0) |
| Ligne 88 | Col 18 | R88 | `=DIST_PHASE_1_v2!Q77` | =DIST_PHASE_1_v2!Q77 |
| Ligne 88 | Col 19 | S88 | `=DIST_PHASE_1_v2!R77` | =DIST_PHASE_1_v2!R77 |
| Ligne 88 | Col 20 | T88 | `=DIST_PHASE_1_v2!T77` | =DIST_PHASE_1_v2!T77 |
| Ligne 88 | Col 21 | U88 | `=DIST_PHASE_1_v2!Y77` | =DIST_PHASE_1_v2!Y77 |
| Ligne 88 | Col 23 | W88 | `=DIST_PHASE_1_v2!AA77` | =DIST_PHASE_1_v2!AA77 |
| Ligne 88 | Col 24 | X88 | `= (10.679 * W88) / ((U88/1000)^4.871 * V88^1.852)` | = (10.679 * W88) / ((U88/1000)^4.871 * V88^1.852) |
| Ligne 88 | Col 25 | Y88 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA55AF0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA55AF0> |
| Ligne 88 | Col 26 | Z88 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54F50>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54F50> |
| Ligne 88 | Col 27 | AA88 | `=IF(P88>0,
IF(R88="positif",1,-1),
0)` | =IF(P88>0,
IF(R88="positif",1,-1),
0) |
| Ligne 88 | Col 28 | AB88 | `=X88*SIGN(Y88)*ABS(Y88)^1.852` | =X88*SIGN(Y88)*ABS(Y88)^1.852 |
| Ligne 88 | Col 29 | AC88 | `=1.852*X88*ABS(Y88)^(1.852-1)` | =1.852*X88*ABS(Y88)^(1.852-1) |
| Ligne 88 | Col 30 | AD88 | `=IF(P88>0,
Y88+($D$93*Z88)+(AA88*$S$93),
Y88+$S$93)` | =IF(P88>0,
Y88+($D$93*Z88)+(AA88*$S$93),
Y88+$S$93) |
| Ligne 88 | Col 32 | AF88 | `=ABS(AD88)-ABS(Y88)` | =ABS(AD88)-ABS(Y88) |
| Ligne 89 | Col 4 | D89 | `=DIST_PHASE_1_v2!E78` | =DIST_PHASE_1_v2!E78 |
| Ligne 89 | Col 5 | E89 | `=DIST_PHASE_1_v2!G78` | =DIST_PHASE_1_v2!G78 |
| Ligne 89 | Col 6 | F89 | `=DIST_PHASE_1_v2!L78` | =DIST_PHASE_1_v2!L78 |
| Ligne 89 | Col 7 | G89 | `=DIST_PHASE_1_v2!M78` | =DIST_PHASE_1_v2!M78 |
| Ligne 89 | Col 8 | H89 | `=DIST_PHASE_1_v2!N78` | =DIST_PHASE_1_v2!N78 |
| Ligne 89 | Col 9 | I89 | `= (10.679 * H89) / ((F89/1000)^4.871 * G89^1.852)` | = (10.679 * H89) / ((F89/1000)^4.871 * G89^1.852) |
| Ligne 89 | Col 10 | J89 | `=IF(C89="positif",E89,IF(C89="negatif",-E89,""))` | =IF(C89="positif",E89,IF(C89="negatif",-E89,"")) |
| Ligne 89 | Col 11 | K89 | `=IF(J89>0,I89*E89^1.852,-I89*E89^1.852)` | =IF(J89>0,I89*E89^1.852,-I89*E89^1.852) |
| Ligne 89 | Col 12 | L89 | `=1.852*I89*ABS(E89)^(1.852-1)` | =1.852*I89*ABS(E89)^(1.852-1) |
| Ligne 89 | Col 13 | M89 | `=J89+$D$93` | =J89+$D$93 |
| Ligne 89 | Col 16 | P89 | `=IFERROR(MATCH(S89,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S89,$D$22:$D$91,0),0) |
| Ligne 89 | Col 18 | R89 | `=DIST_PHASE_1_v2!Q78` | =DIST_PHASE_1_v2!Q78 |
| Ligne 89 | Col 19 | S89 | `=DIST_PHASE_1_v2!R78` | =DIST_PHASE_1_v2!R78 |
| Ligne 89 | Col 20 | T89 | `=DIST_PHASE_1_v2!T78` | =DIST_PHASE_1_v2!T78 |
| Ligne 89 | Col 21 | U89 | `=DIST_PHASE_1_v2!Y78` | =DIST_PHASE_1_v2!Y78 |
| Ligne 89 | Col 23 | W89 | `=DIST_PHASE_1_v2!AA78` | =DIST_PHASE_1_v2!AA78 |
| Ligne 89 | Col 24 | X89 | `= (10.679 * W89) / ((U89/1000)^4.871 * V89^1.852)` | = (10.679 * W89) / ((U89/1000)^4.871 * V89^1.852) |
| Ligne 89 | Col 25 | Y89 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA55CD0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA55CD0> |
| Ligne 89 | Col 26 | Z89 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54FB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA54FB0> |
| Ligne 89 | Col 27 | AA89 | `=IF(P89>0,
IF(R89="positif",1,-1),
0)` | =IF(P89>0,
IF(R89="positif",1,-1),
0) |
| Ligne 89 | Col 28 | AB89 | `=X89*SIGN(Y89)*ABS(Y89)^1.852` | =X89*SIGN(Y89)*ABS(Y89)^1.852 |
| Ligne 89 | Col 29 | AC89 | `=1.852*X89*ABS(Y89)^(1.852-1)` | =1.852*X89*ABS(Y89)^(1.852-1) |
| Ligne 89 | Col 30 | AD89 | `=IF(P89>0,
Y89+($D$93*Z89)+(AA89*$S$93),
Y89+$S$93)` | =IF(P89>0,
Y89+($D$93*Z89)+(AA89*$S$93),
Y89+$S$93) |
| Ligne 89 | Col 32 | AF89 | `=ABS(AD89)-ABS(Y89)` | =ABS(AD89)-ABS(Y89) |
| Ligne 90 | Col 4 | D90 | `=DIST_PHASE_1_v2!E79` | =DIST_PHASE_1_v2!E79 |
| Ligne 90 | Col 5 | E90 | `=DIST_PHASE_1_v2!G79` | =DIST_PHASE_1_v2!G79 |
| Ligne 90 | Col 6 | F90 | `=DIST_PHASE_1_v2!L79` | =DIST_PHASE_1_v2!L79 |
| Ligne 90 | Col 7 | G90 | `=DIST_PHASE_1_v2!M79` | =DIST_PHASE_1_v2!M79 |
| Ligne 90 | Col 8 | H90 | `=DIST_PHASE_1_v2!N79` | =DIST_PHASE_1_v2!N79 |
| Ligne 90 | Col 9 | I90 | `= (10.679 * H90) / ((F90/1000)^4.871 * G90^1.852)` | = (10.679 * H90) / ((F90/1000)^4.871 * G90^1.852) |
| Ligne 90 | Col 10 | J90 | `=IF(C90="positif",E90,IF(C90="negatif",-E90,""))` | =IF(C90="positif",E90,IF(C90="negatif",-E90,"")) |
| Ligne 90 | Col 11 | K90 | `=IF(J90>0,I90*E90^1.852,-I90*E90^1.852)` | =IF(J90>0,I90*E90^1.852,-I90*E90^1.852) |
| Ligne 90 | Col 12 | L90 | `=1.852*I90*ABS(E90)^(1.852-1)` | =1.852*I90*ABS(E90)^(1.852-1) |
| Ligne 90 | Col 13 | M90 | `=J90+$D$93` | =J90+$D$93 |
| Ligne 90 | Col 16 | P90 | `=IFERROR(MATCH(S90,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S90,$D$22:$D$91,0),0) |
| Ligne 90 | Col 18 | R90 | `=DIST_PHASE_1_v2!Q79` | =DIST_PHASE_1_v2!Q79 |
| Ligne 90 | Col 19 | S90 | `=DIST_PHASE_1_v2!R79` | =DIST_PHASE_1_v2!R79 |
| Ligne 90 | Col 20 | T90 | `=DIST_PHASE_1_v2!T79` | =DIST_PHASE_1_v2!T79 |
| Ligne 90 | Col 21 | U90 | `=DIST_PHASE_1_v2!Y79` | =DIST_PHASE_1_v2!Y79 |
| Ligne 90 | Col 23 | W90 | `=DIST_PHASE_1_v2!AA79` | =DIST_PHASE_1_v2!AA79 |
| Ligne 90 | Col 24 | X90 | `= (10.679 * W90) / ((U90/1000)^4.871 * V90^1.852)` | = (10.679 * W90) / ((U90/1000)^4.871 * V90^1.852) |
| Ligne 90 | Col 25 | Y90 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA55EB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA55EB0> |
| Ligne 90 | Col 26 | Z90 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA55010>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA55010> |
| Ligne 90 | Col 27 | AA90 | `=IF(P90>0,
IF(R90="positif",1,-1),
0)` | =IF(P90>0,
IF(R90="positif",1,-1),
0) |
| Ligne 90 | Col 28 | AB90 | `=X90*SIGN(Y90)*ABS(Y90)^1.852` | =X90*SIGN(Y90)*ABS(Y90)^1.852 |
| Ligne 90 | Col 29 | AC90 | `=1.852*X90*ABS(Y90)^(1.852-1)` | =1.852*X90*ABS(Y90)^(1.852-1) |
| Ligne 90 | Col 30 | AD90 | `=IF(P90>0,
Y90+($D$93*Z90)+(AA90*$S$93),
Y90+$S$93)` | =IF(P90>0,
Y90+($D$93*Z90)+(AA90*$S$93),
Y90+$S$93) |
| Ligne 90 | Col 32 | AF90 | `=ABS(AD90)-ABS(Y90)` | =ABS(AD90)-ABS(Y90) |
| Ligne 91 | Col 4 | D91 | `=DIST_PHASE_1_v2!E80` | =DIST_PHASE_1_v2!E80 |
| Ligne 91 | Col 5 | E91 | `=DIST_PHASE_1_v2!G80` | =DIST_PHASE_1_v2!G80 |
| Ligne 91 | Col 6 | F91 | `=DIST_PHASE_1_v2!L80` | =DIST_PHASE_1_v2!L80 |
| Ligne 91 | Col 7 | G91 | `=DIST_PHASE_1_v2!M80` | =DIST_PHASE_1_v2!M80 |
| Ligne 91 | Col 8 | H91 | `=DIST_PHASE_1_v2!N80` | =DIST_PHASE_1_v2!N80 |
| Ligne 91 | Col 9 | I91 | `= (10.679 * H91) / ((F91/1000)^4.871 * G91^1.852)` | = (10.679 * H91) / ((F91/1000)^4.871 * G91^1.852) |
| Ligne 91 | Col 10 | J91 | `=IF(C91="positif",E91,IF(C91="negatif",-E91,""))` | =IF(C91="positif",E91,IF(C91="negatif",-E91,"")) |
| Ligne 91 | Col 11 | K91 | `=IF(J91>0,I91*E91^1.852,-I91*E91^1.852)` | =IF(J91>0,I91*E91^1.852,-I91*E91^1.852) |
| Ligne 91 | Col 12 | L91 | `=1.852*I91*ABS(E91)^(1.852-1)` | =1.852*I91*ABS(E91)^(1.852-1) |
| Ligne 91 | Col 13 | M91 | `=J91+$D$93` | =J91+$D$93 |
| Ligne 91 | Col 16 | P91 | `=IFERROR(MATCH(S91,$D$22:$D$91,0),0)` | =IFERROR(MATCH(S91,$D$22:$D$91,0),0) |
| Ligne 91 | Col 18 | R91 | `=DIST_PHASE_1_v2!Q80` | =DIST_PHASE_1_v2!Q80 |
| Ligne 91 | Col 19 | S91 | `=DIST_PHASE_1_v2!R80` | =DIST_PHASE_1_v2!R80 |
| Ligne 91 | Col 20 | T91 | `=DIST_PHASE_1_v2!T80` | =DIST_PHASE_1_v2!T80 |
| Ligne 91 | Col 21 | U91 | `=DIST_PHASE_1_v2!Y80` | =DIST_PHASE_1_v2!Y80 |
| Ligne 91 | Col 23 | W91 | `=DIST_PHASE_1_v2!AA80` | =DIST_PHASE_1_v2!AA80 |
| Ligne 91 | Col 24 | X91 | `= (10.679 * W91) / ((U91/1000)^4.871 * V91^1.852)` | = (10.679 * W91) / ((U91/1000)^4.871 * V91^1.852) |
| Ligne 91 | Col 25 | Y91 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA56090>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA56090> |
| Ligne 91 | Col 26 | Z91 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA55070>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA55070> |
| Ligne 91 | Col 27 | AA91 | `=IF(P91>0,
IF(R91="positif",1,-1),
0)` | =IF(P91>0,
IF(R91="positif",1,-1),
0) |
| Ligne 91 | Col 28 | AB91 | `=X91*SIGN(Y91)*ABS(Y91)^1.852` | =X91*SIGN(Y91)*ABS(Y91)^1.852 |
| Ligne 91 | Col 29 | AC91 | `=1.852*X91*ABS(Y91)^(1.852-1)` | =1.852*X91*ABS(Y91)^(1.852-1) |
| Ligne 91 | Col 30 | AD91 | `=IF(P91>0,
Y91+($D$93*Z91)+(AA91*$S$93),
Y91+$S$93)` | =IF(P91>0,
Y91+($D$93*Z91)+(AA91*$S$93),
Y91+$S$93) |
| Ligne 91 | Col 32 | AF91 | `=ABS(AD91)-ABS(Y91)` | =ABS(AD91)-ABS(Y91) |
| Ligne 92 | Col 11 | K92 | `=SUM(K22:K91)` | =SUM(K22:K91) |
| Ligne 92 | Col 12 | L92 | `=SUM(L22:L91)` | =SUM(L22:L91) |
| Ligne 92 | Col 16 | P92 | `=COUNTIF(P22:P91,">0")` | =COUNTIF(P22:P91,">0") |
| Ligne 92 | Col 28 | AB92 | `=SUM(AB22:AB91)` | =SUM(AB22:AB91) |
| Ligne 92 | Col 29 | AC92 | `=SUM(AC22:AC91)` | =SUM(AC22:AC91) |
| Ligne 93 | Col 4 | D93 | `=-(K92/L92)` | =-(K92/L92) |
| Ligne 93 | Col 19 | S93 | `=-(AB92/AC92)` | =-(AB92/AC92) |
| Ligne 107 | Col 21 | U107 | `=P21` | =P21 |
| Ligne 107 | Col 22 | V107 | `=Q21` | =Q21 |
| Ligne 107 | Col 26 | Z107 | `=Z21` | =Z21 |
| Ligne 107 | Col 27 | AA107 | `=AA21` | =AA21 |
| Ligne 108 | Col 8 | H108 | `=D22` | =D22 |
| Ligne 108 | Col 9 | I108 | `=I22` | =I22 |
| Ligne 108 | Col 10 | J108 | `=M22` | =M22 |
| Ligne 108 | Col 11 | K108 | `=I108*SIGN(J108)*ABS(J108)^1.821` | =I108*SIGN(J108)*ABS(J108)^1.821 |
| Ligne 108 | Col 12 | L108 | `=1.852*I108*ABS(J108)^(1.852-1)` | =1.852*I108*ABS(J108)^(1.852-1) |
| Ligne 108 | Col 13 | M108 | `=J108+$I$179` | =J108+$I$179 |
| Ligne 108 | Col 21 | U108 | `=P22` | =P22 |
| Ligne 108 | Col 22 | V108 | `=Q22` | =Q22 |
| Ligne 108 | Col 23 | W108 | `=S22` | =S22 |
| Ligne 108 | Col 24 | X108 | `=X22` | =X22 |
| Ligne 108 | Col 25 | Y108 | `=AD22` | =AD22 |
| Ligne 108 | Col 26 | Z108 | `=Z22` | =Z22 |
| Ligne 108 | Col 27 | AA108 | `=AA22` | =AA22 |
| Ligne 108 | Col 28 | AB108 | `=X108*SIGN(Y108)*ABS(Y108)^1.821` | =X108*SIGN(Y108)*ABS(Y108)^1.821 |
| Ligne 108 | Col 29 | AC108 | `=1.852*X108*ABS(Y108)^(1.852-1)` | =1.852*X108*ABS(Y108)^(1.852-1) |
| Ligne 108 | Col 30 | AD108 | `=IF(U108>0,
Y108+($I$179*Z108)+(AA108*X180),
Y108+$S$93)` | =IF(U108>0,
Y108+($I$179*Z108)+(AA108*X180),
Y108+$S$93) |
| Ligne 108 | Col 32 | AF108 | `=ABS(AD108)-ABS(Y108)` | =ABS(AD108)-ABS(Y108) |
| Ligne 108 | Col 40 | AN108 | `=ABS(AV22)` | =ABS(AV22) |
| Ligne 108 | Col 44 | AR108 | `= (10.679 * AQ108) / ((AO108/1000)^4.871 * AP108^1.852)` | = (10.679 * AQ108) / ((AO108/1000)^4.871 * AP108^1.852) |
| Ligne 108 | Col 45 | AS108 | `=IF(AL108="positif",AN108,IF(AL108="negatif",-AN108,""))` | =IF(AL108="positif",AN108,IF(AL108="negatif",-AN108,"")) |
| Ligne 108 | Col 46 | AT108 | `=IF(AJ108>0,
        IF(AS108>0, AR108*AS108^1.852,-AR108*ABS(AS108)^1.852),
        IF(AS108>0, AR108*AN108^1.852, -AR108*AN108^1.852))` | =IF(AJ108>0,
        IF(AS108>0, AR108*AS108^1.852,-AR108*ABS(AS108)^1.852),
        IF(AS108>0, AR108*AN108^1.852, -AR108*AN108^1.852)) |
| Ligne 108 | Col 47 | AU108 | `=1.852*AR108*ABS(AS108)^(1.852-1)` | =1.852*AR108*ABS(AS108)^(1.852-1) |
| Ligne 108 | Col 48 | AV108 | `=AS108+$AN$146` | =AS108+$AN$146 |
| Ligne 109 | Col 8 | H109 | `=D23` | =D23 |
| Ligne 109 | Col 9 | I109 | `=I23` | =I23 |
| Ligne 109 | Col 10 | J109 | `=M23` | =M23 |
| Ligne 109 | Col 11 | K109 | `=I109*SIGN(J109)*ABS(J109)^1.821` | =I109*SIGN(J109)*ABS(J109)^1.821 |
| Ligne 109 | Col 12 | L109 | `=1.852*I109*ABS(J109)^(1.852-1)` | =1.852*I109*ABS(J109)^(1.852-1) |
| Ligne 109 | Col 13 | M109 | `=J109+$I$179` | =J109+$I$179 |
| Ligne 109 | Col 21 | U109 | `=P23` | =P23 |
| Ligne 109 | Col 22 | V109 | `=Q23` | =Q23 |
| Ligne 109 | Col 23 | W109 | `=S23` | =S23 |
| Ligne 109 | Col 24 | X109 | `=X23` | =X23 |
| Ligne 109 | Col 25 | Y109 | `=AD23` | =AD23 |
| Ligne 109 | Col 26 | Z109 | `=Z23` | =Z23 |
| Ligne 109 | Col 27 | AA109 | `=AA23` | =AA23 |
| Ligne 109 | Col 28 | AB109 | `=X109*SIGN(Y109)*ABS(Y109)^1.821` | =X109*SIGN(Y109)*ABS(Y109)^1.821 |
| Ligne 109 | Col 29 | AC109 | `=1.852*X109*ABS(Y109)^(1.852-1)` | =1.852*X109*ABS(Y109)^(1.852-1) |
| Ligne 109 | Col 30 | AD109 | `=IF(U109>0,
Y109+($I$179*Z109)+(AA109*X181),
Y109+$S$93)` | =IF(U109>0,
Y109+($I$179*Z109)+(AA109*X181),
Y109+$S$93) |
| Ligne 109 | Col 32 | AF109 | `=ABS(AD109)-ABS(Y109)` | =ABS(AD109)-ABS(Y109) |
| Ligne 109 | Col 40 | AN109 | `=ABS(AV23)` | =ABS(AV23) |
| Ligne 109 | Col 44 | AR109 | `= (10.679 * AQ109) / ((AO109/1000)^4.871 * AP109^1.852)` | = (10.679 * AQ109) / ((AO109/1000)^4.871 * AP109^1.852) |
| Ligne 109 | Col 45 | AS109 | `=IF(AL109="positif",AN109,IF(AL109="negatif",-AN109,""))` | =IF(AL109="positif",AN109,IF(AL109="negatif",-AN109,"")) |
| Ligne 109 | Col 46 | AT109 | `=IF(AJ109>0,
        IF(AS109>0, AR109*AS109^1.852,-AR109*ABS(AS109)^1.852),
        IF(AS109>0, AR109*AN109^1.852, -AR109*AN109^1.852))` | =IF(AJ109>0,
        IF(AS109>0, AR109*AS109^1.852,-AR109*ABS(AS109)^1.852),
        IF(AS109>0, AR109*AN109^1.852, -AR109*AN109^1.852)) |
| Ligne 109 | Col 47 | AU109 | `=1.852*AR109*ABS(AS109)^(1.852-1)` | =1.852*AR109*ABS(AS109)^(1.852-1) |
| Ligne 109 | Col 48 | AV109 | `=AS109+$AN$146` | =AS109+$AN$146 |
| Ligne 110 | Col 8 | H110 | `=D24` | =D24 |
| Ligne 110 | Col 9 | I110 | `=I24` | =I24 |
| Ligne 110 | Col 10 | J110 | `=M24` | =M24 |
| Ligne 110 | Col 11 | K110 | `=I110*SIGN(J110)*ABS(J110)^1.821` | =I110*SIGN(J110)*ABS(J110)^1.821 |
| Ligne 110 | Col 12 | L110 | `=1.852*I110*ABS(J110)^(1.852-1)` | =1.852*I110*ABS(J110)^(1.852-1) |
| Ligne 110 | Col 13 | M110 | `=J110+$I$179` | =J110+$I$179 |
| Ligne 110 | Col 21 | U110 | `=P24` | =P24 |
| Ligne 110 | Col 22 | V110 | `=Q24` | =Q24 |
| Ligne 110 | Col 23 | W110 | `=S24` | =S24 |
| Ligne 110 | Col 24 | X110 | `=X24` | =X24 |
| Ligne 110 | Col 25 | Y110 | `=AD24` | =AD24 |
| Ligne 110 | Col 26 | Z110 | `=Z24` | =Z24 |
| Ligne 110 | Col 27 | AA110 | `=AA24` | =AA24 |
| Ligne 110 | Col 28 | AB110 | `=X110*SIGN(Y110)*ABS(Y110)^1.821` | =X110*SIGN(Y110)*ABS(Y110)^1.821 |
| Ligne 110 | Col 29 | AC110 | `=1.852*X110*ABS(Y110)^(1.852-1)` | =1.852*X110*ABS(Y110)^(1.852-1) |
| Ligne 110 | Col 30 | AD110 | `=IF(U110>0,
Y110+($I$179*Z110)+(AA110*X182),
Y110+$S$93)` | =IF(U110>0,
Y110+($I$179*Z110)+(AA110*X182),
Y110+$S$93) |
| Ligne 110 | Col 32 | AF110 | `=ABS(AD110)-ABS(Y110)` | =ABS(AD110)-ABS(Y110) |
| Ligne 110 | Col 40 | AN110 | `=ABS(AV24)` | =ABS(AV24) |
| Ligne 110 | Col 44 | AR110 | `= (10.679 * AQ110) / ((AO110/1000)^4.871 * AP110^1.852)` | = (10.679 * AQ110) / ((AO110/1000)^4.871 * AP110^1.852) |
| Ligne 110 | Col 45 | AS110 | `=IF(AL110="positif",AN110,IF(AL110="negatif",-AN110,""))` | =IF(AL110="positif",AN110,IF(AL110="negatif",-AN110,"")) |
| Ligne 110 | Col 46 | AT110 | `=IF(AJ110>0,
        IF(AS110>0, AR110*AS110^1.852,-AR110*ABS(AS110)^1.852),
        IF(AS110>0, AR110*AN110^1.852, -AR110*AN110^1.852))` | =IF(AJ110>0,
        IF(AS110>0, AR110*AS110^1.852,-AR110*ABS(AS110)^1.852),
        IF(AS110>0, AR110*AN110^1.852, -AR110*AN110^1.852)) |
| Ligne 110 | Col 47 | AU110 | `=1.852*AR110*ABS(AS110)^(1.852-1)` | =1.852*AR110*ABS(AS110)^(1.852-1) |
| Ligne 110 | Col 48 | AV110 | `=AS110+$AN$146` | =AS110+$AN$146 |
| Ligne 111 | Col 8 | H111 | `=D25` | =D25 |
| Ligne 111 | Col 9 | I111 | `=I25` | =I25 |
| Ligne 111 | Col 10 | J111 | `=M25` | =M25 |
| Ligne 111 | Col 11 | K111 | `=I111*SIGN(J111)*ABS(J111)^1.821` | =I111*SIGN(J111)*ABS(J111)^1.821 |
| Ligne 111 | Col 12 | L111 | `=1.852*I111*ABS(J111)^(1.852-1)` | =1.852*I111*ABS(J111)^(1.852-1) |
| Ligne 111 | Col 13 | M111 | `=J111+$I$179` | =J111+$I$179 |
| Ligne 111 | Col 21 | U111 | `=P25` | =P25 |
| Ligne 111 | Col 22 | V111 | `=Q25` | =Q25 |
| Ligne 111 | Col 23 | W111 | `=S25` | =S25 |
| Ligne 111 | Col 24 | X111 | `=X25` | =X25 |
| Ligne 111 | Col 25 | Y111 | `=AD25` | =AD25 |
| Ligne 111 | Col 26 | Z111 | `=Z25` | =Z25 |
| Ligne 111 | Col 27 | AA111 | `=AA25` | =AA25 |
| Ligne 111 | Col 28 | AB111 | `=X111*SIGN(Y111)*ABS(Y111)^1.821` | =X111*SIGN(Y111)*ABS(Y111)^1.821 |
| Ligne 111 | Col 29 | AC111 | `=1.852*X111*ABS(Y111)^(1.852-1)` | =1.852*X111*ABS(Y111)^(1.852-1) |
| Ligne 111 | Col 30 | AD111 | `=IF(U111>0,
Y111+($I$179*Z111)+(AA111*X183),
Y111+$S$93)` | =IF(U111>0,
Y111+($I$179*Z111)+(AA111*X183),
Y111+$S$93) |
| Ligne 111 | Col 32 | AF111 | `=ABS(AD111)-ABS(Y111)` | =ABS(AD111)-ABS(Y111) |
| Ligne 111 | Col 40 | AN111 | `=ABS(AV25)` | =ABS(AV25) |
| Ligne 111 | Col 44 | AR111 | `= (10.679 * AQ111) / ((AO111/1000)^4.871 * AP111^1.852)` | = (10.679 * AQ111) / ((AO111/1000)^4.871 * AP111^1.852) |
| Ligne 111 | Col 45 | AS111 | `=IF(AL111="positif",AN111,IF(AL111="negatif",-AN111,""))` | =IF(AL111="positif",AN111,IF(AL111="negatif",-AN111,"")) |
| Ligne 111 | Col 46 | AT111 | `=IF(AJ111>0,
        IF(AS111>0, AR111*AS111^1.852,-AR111*ABS(AS111)^1.852),
        IF(AS111>0, AR111*AN111^1.852, -AR111*AN111^1.852))` | =IF(AJ111>0,
        IF(AS111>0, AR111*AS111^1.852,-AR111*ABS(AS111)^1.852),
        IF(AS111>0, AR111*AN111^1.852, -AR111*AN111^1.852)) |
| Ligne 111 | Col 47 | AU111 | `=1.852*AR111*ABS(AS111)^(1.852-1)` | =1.852*AR111*ABS(AS111)^(1.852-1) |
| Ligne 111 | Col 48 | AV111 | `=AS111+$AN$146` | =AS111+$AN$146 |
| Ligne 112 | Col 8 | H112 | `=D26` | =D26 |
| Ligne 112 | Col 9 | I112 | `=I26` | =I26 |
| Ligne 112 | Col 10 | J112 | `=M26` | =M26 |
| Ligne 112 | Col 11 | K112 | `=I112*SIGN(J112)*ABS(J112)^1.821` | =I112*SIGN(J112)*ABS(J112)^1.821 |
| Ligne 112 | Col 12 | L112 | `=1.852*I112*ABS(J112)^(1.852-1)` | =1.852*I112*ABS(J112)^(1.852-1) |
| Ligne 112 | Col 13 | M112 | `=J112+$I$179` | =J112+$I$179 |
| Ligne 112 | Col 21 | U112 | `=P26` | =P26 |
| Ligne 112 | Col 22 | V112 | `=Q26` | =Q26 |
| Ligne 112 | Col 23 | W112 | `=S26` | =S26 |
| Ligne 112 | Col 24 | X112 | `=X26` | =X26 |
| Ligne 112 | Col 25 | Y112 | `=AD26` | =AD26 |
| Ligne 112 | Col 26 | Z112 | `=Z26` | =Z26 |
| Ligne 112 | Col 27 | AA112 | `=AA26` | =AA26 |
| Ligne 112 | Col 28 | AB112 | `=X112*SIGN(Y112)*ABS(Y112)^1.821` | =X112*SIGN(Y112)*ABS(Y112)^1.821 |
| Ligne 112 | Col 29 | AC112 | `=1.852*X112*ABS(Y112)^(1.852-1)` | =1.852*X112*ABS(Y112)^(1.852-1) |
| Ligne 112 | Col 30 | AD112 | `=IF(U112>0,
Y112+($I$179*Z112)+(AA112*X184),
Y112+$S$93)` | =IF(U112>0,
Y112+($I$179*Z112)+(AA112*X184),
Y112+$S$93) |
| Ligne 112 | Col 32 | AF112 | `=ABS(AD112)-ABS(Y112)` | =ABS(AD112)-ABS(Y112) |
| Ligne 112 | Col 40 | AN112 | `=ABS(AV26)` | =ABS(AV26) |
| Ligne 112 | Col 44 | AR112 | `= (10.679 * AQ112) / ((AO112/1000)^4.871 * AP112^1.852)` | = (10.679 * AQ112) / ((AO112/1000)^4.871 * AP112^1.852) |
| Ligne 112 | Col 45 | AS112 | `=IF(AL112="positif",AN112,IF(AL112="negatif",-AN112,""))` | =IF(AL112="positif",AN112,IF(AL112="negatif",-AN112,"")) |
| Ligne 112 | Col 46 | AT112 | `=IF(AJ112>0,
IF(AS112>0, AR112*AS112^1.852,-AR112*ABS(AS112)^1.852),
IF(AS112>0, AR112*AN112^1.852, -AR112*AN112^1.852))` | =IF(AJ112>0,
IF(AS112>0, AR112*AS112^1.852,-AR112*ABS(AS112)^1.852),
IF(AS112>0, AR112*AN112^1.852, -AR112*AN112^1.852)) |
| Ligne 112 | Col 47 | AU112 | `=1.852*AR112*ABS(AS112)^(1.852-1)` | =1.852*AR112*ABS(AS112)^(1.852-1) |
| Ligne 112 | Col 48 | AV112 | `=AS112+$AN$146` | =AS112+$AN$146 |
| Ligne 113 | Col 8 | H113 | `=D27` | =D27 |
| Ligne 113 | Col 9 | I113 | `=I27` | =I27 |
| Ligne 113 | Col 10 | J113 | `=M27` | =M27 |
| Ligne 113 | Col 11 | K113 | `=I113*SIGN(J113)*ABS(J113)^1.821` | =I113*SIGN(J113)*ABS(J113)^1.821 |
| Ligne 113 | Col 12 | L113 | `=1.852*I113*ABS(J113)^(1.852-1)` | =1.852*I113*ABS(J113)^(1.852-1) |
| Ligne 113 | Col 13 | M113 | `=J113+$I$179` | =J113+$I$179 |
| Ligne 113 | Col 21 | U113 | `=P27` | =P27 |
| Ligne 113 | Col 22 | V113 | `=Q27` | =Q27 |
| Ligne 113 | Col 23 | W113 | `=S27` | =S27 |
| Ligne 113 | Col 24 | X113 | `=X27` | =X27 |
| Ligne 113 | Col 25 | Y113 | `=AD27` | =AD27 |
| Ligne 113 | Col 26 | Z113 | `=Z27` | =Z27 |
| Ligne 113 | Col 27 | AA113 | `=AA27` | =AA27 |
| Ligne 113 | Col 28 | AB113 | `=X113*SIGN(Y113)*ABS(Y113)^1.821` | =X113*SIGN(Y113)*ABS(Y113)^1.821 |
| Ligne 113 | Col 29 | AC113 | `=1.852*X113*ABS(Y113)^(1.852-1)` | =1.852*X113*ABS(Y113)^(1.852-1) |
| Ligne 113 | Col 30 | AD113 | `=IF(U113>0,
Y113+($I$179*Z113)+(AA113*X185),
Y113+$S$93)` | =IF(U113>0,
Y113+($I$179*Z113)+(AA113*X185),
Y113+$S$93) |
| Ligne 113 | Col 32 | AF113 | `=ABS(AD113)-ABS(Y113)` | =ABS(AD113)-ABS(Y113) |
| Ligne 113 | Col 40 | AN113 | `=ABS(AV27)` | =ABS(AV27) |
| Ligne 113 | Col 44 | AR113 | `= (10.679 * AQ113) / ((AO113/1000)^4.871 * AP113^1.852)` | = (10.679 * AQ113) / ((AO113/1000)^4.871 * AP113^1.852) |
| Ligne 113 | Col 45 | AS113 | `=IF(AL113="positif",AN113,IF(AL113="negatif",-AN113,""))` | =IF(AL113="positif",AN113,IF(AL113="negatif",-AN113,"")) |
| Ligne 113 | Col 46 | AT113 | `=IF(AJ113>0,
IF(AS113>0, AR113*AS113^1.852,-AR113*ABS(AS113)^1.852),
IF(AS113>0, AR113*AN113^1.852, -AR113*AN113^1.852))` | =IF(AJ113>0,
IF(AS113>0, AR113*AS113^1.852,-AR113*ABS(AS113)^1.852),
IF(AS113>0, AR113*AN113^1.852, -AR113*AN113^1.852)) |
| Ligne 113 | Col 47 | AU113 | `=1.852*AR113*ABS(AS113)^(1.852-1)` | =1.852*AR113*ABS(AS113)^(1.852-1) |
| Ligne 113 | Col 48 | AV113 | `=AS113+$AN$146` | =AS113+$AN$146 |
| Ligne 114 | Col 8 | H114 | `=D28` | =D28 |
| Ligne 114 | Col 9 | I114 | `=I28` | =I28 |
| Ligne 114 | Col 10 | J114 | `=M28` | =M28 |
| Ligne 114 | Col 11 | K114 | `=I114*SIGN(J114)*ABS(J114)^1.821` | =I114*SIGN(J114)*ABS(J114)^1.821 |
| Ligne 114 | Col 12 | L114 | `=1.852*I114*ABS(J114)^(1.852-1)` | =1.852*I114*ABS(J114)^(1.852-1) |
| Ligne 114 | Col 13 | M114 | `=J114+$I$179` | =J114+$I$179 |
| Ligne 114 | Col 21 | U114 | `=P28` | =P28 |
| Ligne 114 | Col 22 | V114 | `=Q28` | =Q28 |
| Ligne 114 | Col 23 | W114 | `=S28` | =S28 |
| Ligne 114 | Col 24 | X114 | `=X28` | =X28 |
| Ligne 114 | Col 25 | Y114 | `=AD28` | =AD28 |
| Ligne 114 | Col 26 | Z114 | `=Z28` | =Z28 |
| Ligne 114 | Col 27 | AA114 | `=AA28` | =AA28 |
| Ligne 114 | Col 28 | AB114 | `=X114*SIGN(Y114)*ABS(Y114)^1.821` | =X114*SIGN(Y114)*ABS(Y114)^1.821 |
| Ligne 114 | Col 29 | AC114 | `=1.852*X114*ABS(Y114)^(1.852-1)` | =1.852*X114*ABS(Y114)^(1.852-1) |
| Ligne 114 | Col 30 | AD114 | `=IF(U114>0,
Y114+($I$179*Z114)+(AA114*X186),
Y114+$S$93)` | =IF(U114>0,
Y114+($I$179*Z114)+(AA114*X186),
Y114+$S$93) |
| Ligne 114 | Col 32 | AF114 | `=ABS(AD114)-ABS(Y114)` | =ABS(AD114)-ABS(Y114) |
| Ligne 114 | Col 40 | AN114 | `=ABS(AV28)` | =ABS(AV28) |
| Ligne 114 | Col 44 | AR114 | `= (10.679 * AQ114) / ((AO114/1000)^4.871 * AP114^1.852)` | = (10.679 * AQ114) / ((AO114/1000)^4.871 * AP114^1.852) |
| Ligne 114 | Col 45 | AS114 | `=IF(AL114="positif",AN114,IF(AL114="negatif",-AN114,""))` | =IF(AL114="positif",AN114,IF(AL114="negatif",-AN114,"")) |
| Ligne 114 | Col 46 | AT114 | `=IF(AJ114>0,
IF(AS114>0, AR114*AS114^1.852,-AR114*ABS(AS114)^1.852),
IF(AS114>0, AR114*AN114^1.852, -AR114*AN114^1.852))` | =IF(AJ114>0,
IF(AS114>0, AR114*AS114^1.852,-AR114*ABS(AS114)^1.852),
IF(AS114>0, AR114*AN114^1.852, -AR114*AN114^1.852)) |
| Ligne 114 | Col 47 | AU114 | `=1.852*AR114*ABS(AS114)^(1.852-1)` | =1.852*AR114*ABS(AS114)^(1.852-1) |
| Ligne 114 | Col 48 | AV114 | `=AS114+$AN$146` | =AS114+$AN$146 |
| Ligne 115 | Col 8 | H115 | `=D29` | =D29 |
| Ligne 115 | Col 9 | I115 | `=I29` | =I29 |
| Ligne 115 | Col 10 | J115 | `=M29` | =M29 |
| Ligne 115 | Col 11 | K115 | `=I115*SIGN(J115)*ABS(J115)^1.821` | =I115*SIGN(J115)*ABS(J115)^1.821 |
| Ligne 115 | Col 12 | L115 | `=1.852*I115*ABS(J115)^(1.852-1)` | =1.852*I115*ABS(J115)^(1.852-1) |
| Ligne 115 | Col 13 | M115 | `=J115+$I$179` | =J115+$I$179 |
| Ligne 115 | Col 21 | U115 | `=P29` | =P29 |
| Ligne 115 | Col 22 | V115 | `=Q29` | =Q29 |
| Ligne 115 | Col 23 | W115 | `=S29` | =S29 |
| Ligne 115 | Col 24 | X115 | `=X29` | =X29 |
| Ligne 115 | Col 25 | Y115 | `=AD29` | =AD29 |
| Ligne 115 | Col 26 | Z115 | `=Z29` | =Z29 |
| Ligne 115 | Col 27 | AA115 | `=AA29` | =AA29 |
| Ligne 115 | Col 28 | AB115 | `=X115*SIGN(Y115)*ABS(Y115)^1.821` | =X115*SIGN(Y115)*ABS(Y115)^1.821 |
| Ligne 115 | Col 29 | AC115 | `=1.852*X115*ABS(Y115)^(1.852-1)` | =1.852*X115*ABS(Y115)^(1.852-1) |
| Ligne 115 | Col 30 | AD115 | `=IF(U115>0,
Y115+($I$179*Z115)+(AA115*X187),
Y115+$S$93)` | =IF(U115>0,
Y115+($I$179*Z115)+(AA115*X187),
Y115+$S$93) |
| Ligne 115 | Col 32 | AF115 | `=ABS(AD115)-ABS(Y115)` | =ABS(AD115)-ABS(Y115) |
| Ligne 115 | Col 40 | AN115 | `=ABS(AV29)` | =ABS(AV29) |
| Ligne 115 | Col 44 | AR115 | `= (10.679 * AQ115) / ((AO115/1000)^4.871 * AP115^1.852)` | = (10.679 * AQ115) / ((AO115/1000)^4.871 * AP115^1.852) |
| Ligne 115 | Col 45 | AS115 | `=IF(AL115="positif",AN115,IF(AL115="negatif",-AN115,""))` | =IF(AL115="positif",AN115,IF(AL115="negatif",-AN115,"")) |
| Ligne 115 | Col 46 | AT115 | `=IF(AJ115>0,
IF(AS115>0, AR115*AS115^1.852,-AR115*ABS(AS115)^1.852),
IF(AS115>0, AR115*AN115^1.852, -AR115*AN115^1.852))` | =IF(AJ115>0,
IF(AS115>0, AR115*AS115^1.852,-AR115*ABS(AS115)^1.852),
IF(AS115>0, AR115*AN115^1.852, -AR115*AN115^1.852)) |
| Ligne 115 | Col 47 | AU115 | `=1.852*AR115*ABS(AS115)^(1.852-1)` | =1.852*AR115*ABS(AS115)^(1.852-1) |
| Ligne 115 | Col 48 | AV115 | `=AS115+$AN$146` | =AS115+$AN$146 |
| Ligne 116 | Col 8 | H116 | `=D30` | =D30 |
| Ligne 116 | Col 9 | I116 | `=I30` | =I30 |
| Ligne 116 | Col 10 | J116 | `=M30` | =M30 |
| Ligne 116 | Col 11 | K116 | `=I116*SIGN(J116)*ABS(J116)^1.821` | =I116*SIGN(J116)*ABS(J116)^1.821 |
| Ligne 116 | Col 12 | L116 | `=1.852*I116*ABS(J116)^(1.852-1)` | =1.852*I116*ABS(J116)^(1.852-1) |
| Ligne 116 | Col 13 | M116 | `=J116+$I$179` | =J116+$I$179 |
| Ligne 116 | Col 21 | U116 | `=P30` | =P30 |
| Ligne 116 | Col 22 | V116 | `=Q30` | =Q30 |
| Ligne 116 | Col 23 | W116 | `=S30` | =S30 |
| Ligne 116 | Col 24 | X116 | `=X30` | =X30 |
| Ligne 116 | Col 25 | Y116 | `=AD30` | =AD30 |
| Ligne 116 | Col 26 | Z116 | `=Z30` | =Z30 |
| Ligne 116 | Col 27 | AA116 | `=AA30` | =AA30 |
| Ligne 116 | Col 28 | AB116 | `=X116*SIGN(Y116)*ABS(Y116)^1.821` | =X116*SIGN(Y116)*ABS(Y116)^1.821 |
| Ligne 116 | Col 29 | AC116 | `=1.852*X116*ABS(Y116)^(1.852-1)` | =1.852*X116*ABS(Y116)^(1.852-1) |
| Ligne 116 | Col 30 | AD116 | `=IF(U116>0,
Y116+($I$179*Z116)+(AA116*X188),
Y116+$S$93)` | =IF(U116>0,
Y116+($I$179*Z116)+(AA116*X188),
Y116+$S$93) |
| Ligne 116 | Col 32 | AF116 | `=ABS(AD116)-ABS(Y116)` | =ABS(AD116)-ABS(Y116) |
| Ligne 116 | Col 40 | AN116 | `=ABS(AV30)` | =ABS(AV30) |
| Ligne 116 | Col 44 | AR116 | `= (10.679 * AQ116) / ((AO116/1000)^4.871 * AP116^1.852)` | = (10.679 * AQ116) / ((AO116/1000)^4.871 * AP116^1.852) |
| Ligne 116 | Col 45 | AS116 | `=IF(AL116="positif",AN116,IF(AL116="negatif",-AN116,""))` | =IF(AL116="positif",AN116,IF(AL116="negatif",-AN116,"")) |
| Ligne 116 | Col 46 | AT116 | `=IF(AJ116>0,
IF(AS116>0, AR116*AS116^1.852,-AR116*ABS(AS116)^1.852),
IF(AS116>0, AR116*AN116^1.852, -AR116*AN116^1.852))` | =IF(AJ116>0,
IF(AS116>0, AR116*AS116^1.852,-AR116*ABS(AS116)^1.852),
IF(AS116>0, AR116*AN116^1.852, -AR116*AN116^1.852)) |
| Ligne 116 | Col 47 | AU116 | `=1.852*AR116*ABS(AS116)^(1.852-1)` | =1.852*AR116*ABS(AS116)^(1.852-1) |
| Ligne 116 | Col 48 | AV116 | `=AS116+$AN$146` | =AS116+$AN$146 |
| Ligne 117 | Col 8 | H117 | `=D31` | =D31 |
| Ligne 117 | Col 9 | I117 | `=I31` | =I31 |
| Ligne 117 | Col 10 | J117 | `=M31` | =M31 |
| Ligne 117 | Col 11 | K117 | `=I117*SIGN(J117)*ABS(J117)^1.821` | =I117*SIGN(J117)*ABS(J117)^1.821 |
| Ligne 117 | Col 12 | L117 | `=1.852*I117*ABS(J117)^(1.852-1)` | =1.852*I117*ABS(J117)^(1.852-1) |
| Ligne 117 | Col 13 | M117 | `=J117+$I$179` | =J117+$I$179 |
| Ligne 117 | Col 21 | U117 | `=P31` | =P31 |
| Ligne 117 | Col 22 | V117 | `=Q31` | =Q31 |
| Ligne 117 | Col 23 | W117 | `=S31` | =S31 |
| Ligne 117 | Col 24 | X117 | `=X31` | =X31 |
| Ligne 117 | Col 25 | Y117 | `=AD31` | =AD31 |
| Ligne 117 | Col 26 | Z117 | `=Z31` | =Z31 |
| Ligne 117 | Col 27 | AA117 | `=AA31` | =AA31 |
| Ligne 117 | Col 28 | AB117 | `=X117*SIGN(Y117)*ABS(Y117)^1.821` | =X117*SIGN(Y117)*ABS(Y117)^1.821 |
| Ligne 117 | Col 29 | AC117 | `=1.852*X117*ABS(Y117)^(1.852-1)` | =1.852*X117*ABS(Y117)^(1.852-1) |
| Ligne 117 | Col 30 | AD117 | `=IF(U117>0,
Y117+($I$179*Z117)+(AA117*X189),
Y117+$S$93)` | =IF(U117>0,
Y117+($I$179*Z117)+(AA117*X189),
Y117+$S$93) |
| Ligne 117 | Col 32 | AF117 | `=ABS(AD117)-ABS(Y117)` | =ABS(AD117)-ABS(Y117) |
| Ligne 117 | Col 40 | AN117 | `=ABS(AV31)` | =ABS(AV31) |
| Ligne 117 | Col 44 | AR117 | `= (10.679 * AQ117) / ((AO117/1000)^4.871 * AP117^1.852)` | = (10.679 * AQ117) / ((AO117/1000)^4.871 * AP117^1.852) |
| Ligne 117 | Col 45 | AS117 | `=IF(AL117="positif",AN117,IF(AL117="negatif",-AN117,""))` | =IF(AL117="positif",AN117,IF(AL117="negatif",-AN117,"")) |
| Ligne 117 | Col 46 | AT117 | `=IF(AJ117>0,
IF(AS117>0, AR117*AS117^1.852,-AR117*ABS(AS117)^1.852),
IF(AS117>0, AR117*AN117^1.852, -AR117*AN117^1.852))` | =IF(AJ117>0,
IF(AS117>0, AR117*AS117^1.852,-AR117*ABS(AS117)^1.852),
IF(AS117>0, AR117*AN117^1.852, -AR117*AN117^1.852)) |
| Ligne 117 | Col 47 | AU117 | `=1.852*AR117*ABS(AS117)^(1.852-1)` | =1.852*AR117*ABS(AS117)^(1.852-1) |
| Ligne 117 | Col 48 | AV117 | `=AS117+$AN$146` | =AS117+$AN$146 |
| Ligne 118 | Col 8 | H118 | `=D32` | =D32 |
| Ligne 118 | Col 9 | I118 | `=I32` | =I32 |
| Ligne 118 | Col 10 | J118 | `=M32` | =M32 |
| Ligne 118 | Col 11 | K118 | `=I118*SIGN(J118)*ABS(J118)^1.821` | =I118*SIGN(J118)*ABS(J118)^1.821 |
| Ligne 118 | Col 12 | L118 | `=1.852*I118*ABS(J118)^(1.852-1)` | =1.852*I118*ABS(J118)^(1.852-1) |
| Ligne 118 | Col 13 | M118 | `=J118+$I$179` | =J118+$I$179 |
| Ligne 118 | Col 21 | U118 | `=P32` | =P32 |
| Ligne 118 | Col 22 | V118 | `=Q32` | =Q32 |
| Ligne 118 | Col 23 | W118 | `=S32` | =S32 |
| Ligne 118 | Col 24 | X118 | `=X32` | =X32 |
| Ligne 118 | Col 25 | Y118 | `=AD32` | =AD32 |
| Ligne 118 | Col 26 | Z118 | `=Z32` | =Z32 |
| Ligne 118 | Col 27 | AA118 | `=AA32` | =AA32 |
| Ligne 118 | Col 28 | AB118 | `=X118*SIGN(Y118)*ABS(Y118)^1.821` | =X118*SIGN(Y118)*ABS(Y118)^1.821 |
| Ligne 118 | Col 29 | AC118 | `=1.852*X118*ABS(Y118)^(1.852-1)` | =1.852*X118*ABS(Y118)^(1.852-1) |
| Ligne 118 | Col 30 | AD118 | `=IF(U118>0,
Y118+($I$179*Z118)+(AA118*X190),
Y118+$S$93)` | =IF(U118>0,
Y118+($I$179*Z118)+(AA118*X190),
Y118+$S$93) |
| Ligne 118 | Col 32 | AF118 | `=ABS(AD118)-ABS(Y118)` | =ABS(AD118)-ABS(Y118) |
| Ligne 118 | Col 40 | AN118 | `=ABS(AV32)` | =ABS(AV32) |
| Ligne 118 | Col 44 | AR118 | `= (10.679 * AQ118) / ((AO118/1000)^4.871 * AP118^1.852)` | = (10.679 * AQ118) / ((AO118/1000)^4.871 * AP118^1.852) |
| Ligne 118 | Col 45 | AS118 | `=IF(AL118="positif",AN118,IF(AL118="negatif",-AN118,""))` | =IF(AL118="positif",AN118,IF(AL118="negatif",-AN118,"")) |
| Ligne 118 | Col 46 | AT118 | `=IF(AJ118>0,
IF(AS118>0, AR118*AS118^1.852,-AR118*ABS(AS118)^1.852),
IF(AS118>0, AR118*AN118^1.852, -AR118*AN118^1.852))` | =IF(AJ118>0,
IF(AS118>0, AR118*AS118^1.852,-AR118*ABS(AS118)^1.852),
IF(AS118>0, AR118*AN118^1.852, -AR118*AN118^1.852)) |
| Ligne 118 | Col 47 | AU118 | `=1.852*AR118*ABS(AS118)^(1.852-1)` | =1.852*AR118*ABS(AS118)^(1.852-1) |
| Ligne 118 | Col 48 | AV118 | `=AS118+$AN$146` | =AS118+$AN$146 |
| Ligne 119 | Col 8 | H119 | `=D33` | =D33 |
| Ligne 119 | Col 9 | I119 | `=I33` | =I33 |
| Ligne 119 | Col 10 | J119 | `=M33` | =M33 |
| Ligne 119 | Col 11 | K119 | `=I119*SIGN(J119)*ABS(J119)^1.821` | =I119*SIGN(J119)*ABS(J119)^1.821 |
| Ligne 119 | Col 12 | L119 | `=1.852*I119*ABS(J119)^(1.852-1)` | =1.852*I119*ABS(J119)^(1.852-1) |
| Ligne 119 | Col 13 | M119 | `=J119+$I$179` | =J119+$I$179 |
| Ligne 119 | Col 21 | U119 | `=P33` | =P33 |
| Ligne 119 | Col 22 | V119 | `=Q33` | =Q33 |
| Ligne 119 | Col 23 | W119 | `=S33` | =S33 |
| Ligne 119 | Col 24 | X119 | `=X33` | =X33 |
| Ligne 119 | Col 25 | Y119 | `=AD33` | =AD33 |
| Ligne 119 | Col 26 | Z119 | `=Z33` | =Z33 |
| Ligne 119 | Col 27 | AA119 | `=AA33` | =AA33 |
| Ligne 119 | Col 28 | AB119 | `=X119*SIGN(Y119)*ABS(Y119)^1.821` | =X119*SIGN(Y119)*ABS(Y119)^1.821 |
| Ligne 119 | Col 29 | AC119 | `=1.852*X119*ABS(Y119)^(1.852-1)` | =1.852*X119*ABS(Y119)^(1.852-1) |
| Ligne 119 | Col 30 | AD119 | `=IF(U119>0,
Y119+($I$179*Z119)+(AA119*X191),
Y119+$S$93)` | =IF(U119>0,
Y119+($I$179*Z119)+(AA119*X191),
Y119+$S$93) |
| Ligne 119 | Col 32 | AF119 | `=ABS(AD119)-ABS(Y119)` | =ABS(AD119)-ABS(Y119) |
| Ligne 119 | Col 40 | AN119 | `=ABS(AV33)` | =ABS(AV33) |
| Ligne 119 | Col 44 | AR119 | `= (10.679 * AQ119) / ((AO119/1000)^4.871 * AP119^1.852)` | = (10.679 * AQ119) / ((AO119/1000)^4.871 * AP119^1.852) |
| Ligne 119 | Col 45 | AS119 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA56ED0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA56ED0> |
| Ligne 119 | Col 46 | AT119 | `=IF(AJ119>0,
IF(AS119>0, AR119*AS119^1.852,-AR119*ABS(AS119)^1.852),
IF(AS119>0, AR119*AN119^1.852, -AR119*AN119^1.852))` | =IF(AJ119>0,
IF(AS119>0, AR119*AS119^1.852,-AR119*ABS(AS119)^1.852),
IF(AS119>0, AR119*AN119^1.852, -AR119*AN119^1.852)) |
| Ligne 119 | Col 47 | AU119 | `=1.852*AR119*ABS(AS119)^(1.852-1)` | =1.852*AR119*ABS(AS119)^(1.852-1) |
| Ligne 119 | Col 48 | AV119 | `=AS119+$AN$146` | =AS119+$AN$146 |
| Ligne 120 | Col 8 | H120 | `=D34` | =D34 |
| Ligne 120 | Col 9 | I120 | `=I34` | =I34 |
| Ligne 120 | Col 10 | J120 | `=M34` | =M34 |
| Ligne 120 | Col 11 | K120 | `=I120*SIGN(J120)*ABS(J120)^1.821` | =I120*SIGN(J120)*ABS(J120)^1.821 |
| Ligne 120 | Col 12 | L120 | `=1.852*I120*ABS(J120)^(1.852-1)` | =1.852*I120*ABS(J120)^(1.852-1) |
| Ligne 120 | Col 13 | M120 | `=J120+$I$179` | =J120+$I$179 |
| Ligne 120 | Col 21 | U120 | `=P34` | =P34 |
| Ligne 120 | Col 22 | V120 | `=Q34` | =Q34 |
| Ligne 120 | Col 23 | W120 | `=S34` | =S34 |
| Ligne 120 | Col 24 | X120 | `=X34` | =X34 |
| Ligne 120 | Col 25 | Y120 | `=AD34` | =AD34 |
| Ligne 120 | Col 26 | Z120 | `=Z34` | =Z34 |
| Ligne 120 | Col 27 | AA120 | `=AA34` | =AA34 |
| Ligne 120 | Col 28 | AB120 | `=X120*SIGN(Y120)*ABS(Y120)^1.821` | =X120*SIGN(Y120)*ABS(Y120)^1.821 |
| Ligne 120 | Col 29 | AC120 | `=1.852*X120*ABS(Y120)^(1.852-1)` | =1.852*X120*ABS(Y120)^(1.852-1) |
| Ligne 120 | Col 30 | AD120 | `=IF(U120>0,
Y120+($I$179*Z120)+(AA120*X192),
Y120+$S$93)` | =IF(U120>0,
Y120+($I$179*Z120)+(AA120*X192),
Y120+$S$93) |
| Ligne 120 | Col 32 | AF120 | `=ABS(AD120)-ABS(Y120)` | =ABS(AD120)-ABS(Y120) |
| Ligne 120 | Col 40 | AN120 | `=ABS(AV34)` | =ABS(AV34) |
| Ligne 120 | Col 44 | AR120 | `= (10.679 * AQ120) / ((AO120/1000)^4.871 * AP120^1.852)` | = (10.679 * AQ120) / ((AO120/1000)^4.871 * AP120^1.852) |
| Ligne 120 | Col 45 | AS120 | `=IF(AL120="positif",AN120,IF(AL120="negatif",-AN120,""))` | =IF(AL120="positif",AN120,IF(AL120="negatif",-AN120,"")) |
| Ligne 120 | Col 46 | AT120 | `=IF(AJ120>0,
IF(AS120>0, AR120*AS120^1.852,-AR120*ABS(AS120)^1.852),
IF(AS120>0, AR120*AN120^1.852, -AR120*AN120^1.852))` | =IF(AJ120>0,
IF(AS120>0, AR120*AS120^1.852,-AR120*ABS(AS120)^1.852),
IF(AS120>0, AR120*AN120^1.852, -AR120*AN120^1.852)) |
| Ligne 120 | Col 47 | AU120 | `=1.852*AR120*ABS(AS120)^(1.852-1)` | =1.852*AR120*ABS(AS120)^(1.852-1) |
| Ligne 120 | Col 48 | AV120 | `=AS120+$AN$146` | =AS120+$AN$146 |
| Ligne 121 | Col 8 | H121 | `=D35` | =D35 |
| Ligne 121 | Col 9 | I121 | `=I35` | =I35 |
| Ligne 121 | Col 10 | J121 | `=M35` | =M35 |
| Ligne 121 | Col 11 | K121 | `=I121*SIGN(J121)*ABS(J121)^1.821` | =I121*SIGN(J121)*ABS(J121)^1.821 |
| Ligne 121 | Col 12 | L121 | `=1.852*I121*ABS(J121)^(1.852-1)` | =1.852*I121*ABS(J121)^(1.852-1) |
| Ligne 121 | Col 13 | M121 | `=J121+$I$179` | =J121+$I$179 |
| Ligne 121 | Col 21 | U121 | `=P35` | =P35 |
| Ligne 121 | Col 22 | V121 | `=Q35` | =Q35 |
| Ligne 121 | Col 23 | W121 | `=S35` | =S35 |
| Ligne 121 | Col 24 | X121 | `=X35` | =X35 |
| Ligne 121 | Col 25 | Y121 | `=AD35` | =AD35 |
| Ligne 121 | Col 26 | Z121 | `=Z35` | =Z35 |
| Ligne 121 | Col 27 | AA121 | `=AA35` | =AA35 |
| Ligne 121 | Col 28 | AB121 | `=X121*SIGN(Y121)*ABS(Y121)^1.821` | =X121*SIGN(Y121)*ABS(Y121)^1.821 |
| Ligne 121 | Col 29 | AC121 | `=1.852*X121*ABS(Y121)^(1.852-1)` | =1.852*X121*ABS(Y121)^(1.852-1) |
| Ligne 121 | Col 30 | AD121 | `=IF(U121>0,
Y121+($I$179*Z121)+(AA121*X193),
Y121+$S$93)` | =IF(U121>0,
Y121+($I$179*Z121)+(AA121*X193),
Y121+$S$93) |
| Ligne 121 | Col 32 | AF121 | `=ABS(AD121)-ABS(Y121)` | =ABS(AD121)-ABS(Y121) |
| Ligne 121 | Col 40 | AN121 | `=ABS(AV35)` | =ABS(AV35) |
| Ligne 121 | Col 44 | AR121 | `= (10.679 * AQ121) / ((AO121/1000)^4.871 * AP121^1.852)` | = (10.679 * AQ121) / ((AO121/1000)^4.871 * AP121^1.852) |
| Ligne 121 | Col 45 | AS121 | `=IF(AL121="positif",AN121,IF(AL121="negatif",-AN121,""))` | =IF(AL121="positif",AN121,IF(AL121="negatif",-AN121,"")) |
| Ligne 121 | Col 46 | AT121 | `=IF(AJ121>0,
IF(AS121>0, AR121*AS121^1.852,-AR121*ABS(AS121)^1.852),
IF(AS121>0, AR121*AN121^1.852, -AR121*AN121^1.852))` | =IF(AJ121>0,
IF(AS121>0, AR121*AS121^1.852,-AR121*ABS(AS121)^1.852),
IF(AS121>0, AR121*AN121^1.852, -AR121*AN121^1.852)) |
| Ligne 121 | Col 47 | AU121 | `=1.852*AR121*ABS(AS121)^(1.852-1)` | =1.852*AR121*ABS(AS121)^(1.852-1) |
| Ligne 121 | Col 48 | AV121 | `=AS121+$AN$146` | =AS121+$AN$146 |
| Ligne 122 | Col 8 | H122 | `=D36` | =D36 |
| Ligne 122 | Col 9 | I122 | `=I36` | =I36 |
| Ligne 122 | Col 10 | J122 | `=M36` | =M36 |
| Ligne 122 | Col 11 | K122 | `=I122*SIGN(J122)*ABS(J122)^1.821` | =I122*SIGN(J122)*ABS(J122)^1.821 |
| Ligne 122 | Col 12 | L122 | `=1.852*I122*ABS(J122)^(1.852-1)` | =1.852*I122*ABS(J122)^(1.852-1) |
| Ligne 122 | Col 13 | M122 | `=J122+$I$179` | =J122+$I$179 |
| Ligne 122 | Col 21 | U122 | `=P36` | =P36 |
| Ligne 122 | Col 22 | V122 | `=Q36` | =Q36 |
| Ligne 122 | Col 23 | W122 | `=S36` | =S36 |
| Ligne 122 | Col 24 | X122 | `=X36` | =X36 |
| Ligne 122 | Col 25 | Y122 | `=AD36` | =AD36 |
| Ligne 122 | Col 26 | Z122 | `=Z36` | =Z36 |
| Ligne 122 | Col 27 | AA122 | `=AA36` | =AA36 |
| Ligne 122 | Col 28 | AB122 | `=X122*SIGN(Y122)*ABS(Y122)^1.821` | =X122*SIGN(Y122)*ABS(Y122)^1.821 |
| Ligne 122 | Col 29 | AC122 | `=1.852*X122*ABS(Y122)^(1.852-1)` | =1.852*X122*ABS(Y122)^(1.852-1) |
| Ligne 122 | Col 30 | AD122 | `=IF(U122>0,
Y122+($I$179*Z122)+(AA122*X194),
Y122+$S$93)` | =IF(U122>0,
Y122+($I$179*Z122)+(AA122*X194),
Y122+$S$93) |
| Ligne 122 | Col 32 | AF122 | `=ABS(AD122)-ABS(Y122)` | =ABS(AD122)-ABS(Y122) |
| Ligne 122 | Col 40 | AN122 | `=ABS(AV36)` | =ABS(AV36) |
| Ligne 122 | Col 44 | AR122 | `= (10.679 * AQ122) / ((AO122/1000)^4.871 * AP122^1.852)` | = (10.679 * AQ122) / ((AO122/1000)^4.871 * AP122^1.852) |
| Ligne 122 | Col 45 | AS122 | `=IF(AL122="positif",AN122,IF(AL122="negatif",-AN122,""))` | =IF(AL122="positif",AN122,IF(AL122="negatif",-AN122,"")) |
| Ligne 122 | Col 46 | AT122 | `=IF(AJ122>0,
IF(AS122>0, AR122*AS122^1.852,-AR122*ABS(AS122)^1.852),
IF(AS122>0, AR122*AN122^1.852, -AR122*AN122^1.852))` | =IF(AJ122>0,
IF(AS122>0, AR122*AS122^1.852,-AR122*ABS(AS122)^1.852),
IF(AS122>0, AR122*AN122^1.852, -AR122*AN122^1.852)) |
| Ligne 122 | Col 47 | AU122 | `=1.852*AR122*ABS(AS122)^(1.852-1)` | =1.852*AR122*ABS(AS122)^(1.852-1) |
| Ligne 122 | Col 48 | AV122 | `=AS122+$AN$146` | =AS122+$AN$146 |
| Ligne 123 | Col 8 | H123 | `=D37` | =D37 |
| Ligne 123 | Col 9 | I123 | `=I37` | =I37 |
| Ligne 123 | Col 10 | J123 | `=M37` | =M37 |
| Ligne 123 | Col 11 | K123 | `=I123*SIGN(J123)*ABS(J123)^1.821` | =I123*SIGN(J123)*ABS(J123)^1.821 |
| Ligne 123 | Col 12 | L123 | `=1.852*I123*ABS(J123)^(1.852-1)` | =1.852*I123*ABS(J123)^(1.852-1) |
| Ligne 123 | Col 13 | M123 | `=J123+$I$179` | =J123+$I$179 |
| Ligne 123 | Col 21 | U123 | `=P37` | =P37 |
| Ligne 123 | Col 22 | V123 | `=Q37` | =Q37 |
| Ligne 123 | Col 23 | W123 | `=S37` | =S37 |
| Ligne 123 | Col 24 | X123 | `=X37` | =X37 |
| Ligne 123 | Col 25 | Y123 | `=AD37` | =AD37 |
| Ligne 123 | Col 26 | Z123 | `=Z37` | =Z37 |
| Ligne 123 | Col 27 | AA123 | `=AA37` | =AA37 |
| Ligne 123 | Col 28 | AB123 | `=X123*SIGN(Y123)*ABS(Y123)^1.821` | =X123*SIGN(Y123)*ABS(Y123)^1.821 |
| Ligne 123 | Col 29 | AC123 | `=1.852*X123*ABS(Y123)^(1.852-1)` | =1.852*X123*ABS(Y123)^(1.852-1) |
| Ligne 123 | Col 30 | AD123 | `=IF(U123>0,
Y123+($I$179*Z123)+(AA123*X195),
Y123+$S$93)` | =IF(U123>0,
Y123+($I$179*Z123)+(AA123*X195),
Y123+$S$93) |
| Ligne 123 | Col 32 | AF123 | `=ABS(AD123)-ABS(Y123)` | =ABS(AD123)-ABS(Y123) |
| Ligne 123 | Col 40 | AN123 | `=ABS(AV37)` | =ABS(AV37) |
| Ligne 123 | Col 44 | AR123 | `= (10.679 * AQ123) / ((AO123/1000)^4.871 * AP123^1.852)` | = (10.679 * AQ123) / ((AO123/1000)^4.871 * AP123^1.852) |
| Ligne 123 | Col 45 | AS123 | `=IF(AL123="positif",AN123,IF(AL123="negatif",-AN123,""))` | =IF(AL123="positif",AN123,IF(AL123="negatif",-AN123,"")) |
| Ligne 123 | Col 46 | AT123 | `=IF(AJ123>0,
IF(AS123>0, AR123*AS123^1.852,-AR123*ABS(AS123)^1.852),
IF(AS123>0, AR123*AN123^1.852, -AR123*AN123^1.852))` | =IF(AJ123>0,
IF(AS123>0, AR123*AS123^1.852,-AR123*ABS(AS123)^1.852),
IF(AS123>0, AR123*AN123^1.852, -AR123*AN123^1.852)) |
| Ligne 123 | Col 47 | AU123 | `=1.852*AR123*ABS(AS123)^(1.852-1)` | =1.852*AR123*ABS(AS123)^(1.852-1) |
| Ligne 123 | Col 48 | AV123 | `=AS123+$AN$146` | =AS123+$AN$146 |
| Ligne 124 | Col 8 | H124 | `=D38` | =D38 |
| Ligne 124 | Col 9 | I124 | `=I38` | =I38 |
| Ligne 124 | Col 10 | J124 | `=M38` | =M38 |
| Ligne 124 | Col 11 | K124 | `=I124*SIGN(J124)*ABS(J124)^1.821` | =I124*SIGN(J124)*ABS(J124)^1.821 |
| Ligne 124 | Col 12 | L124 | `=1.852*I124*ABS(J124)^(1.852-1)` | =1.852*I124*ABS(J124)^(1.852-1) |
| Ligne 124 | Col 13 | M124 | `=J124+$I$179` | =J124+$I$179 |
| Ligne 124 | Col 21 | U124 | `=P38` | =P38 |
| Ligne 124 | Col 22 | V124 | `=Q38` | =Q38 |
| Ligne 124 | Col 23 | W124 | `=S38` | =S38 |
| Ligne 124 | Col 24 | X124 | `=X38` | =X38 |
| Ligne 124 | Col 25 | Y124 | `=AD38` | =AD38 |
| Ligne 124 | Col 26 | Z124 | `=Z38` | =Z38 |
| Ligne 124 | Col 27 | AA124 | `=AA38` | =AA38 |
| Ligne 124 | Col 28 | AB124 | `=X124*SIGN(Y124)*ABS(Y124)^1.821` | =X124*SIGN(Y124)*ABS(Y124)^1.821 |
| Ligne 124 | Col 29 | AC124 | `=1.852*X124*ABS(Y124)^(1.852-1)` | =1.852*X124*ABS(Y124)^(1.852-1) |
| Ligne 124 | Col 30 | AD124 | `=IF(U124>0,
Y124+($I$179*Z124)+(AA124*X196),
Y124+$S$93)` | =IF(U124>0,
Y124+($I$179*Z124)+(AA124*X196),
Y124+$S$93) |
| Ligne 124 | Col 32 | AF124 | `=ABS(AD124)-ABS(Y124)` | =ABS(AD124)-ABS(Y124) |
| Ligne 124 | Col 40 | AN124 | `=ABS(AV38)` | =ABS(AV38) |
| Ligne 124 | Col 44 | AR124 | `= (10.679 * AQ124) / ((AO124/1000)^4.871 * AP124^1.852)` | = (10.679 * AQ124) / ((AO124/1000)^4.871 * AP124^1.852) |
| Ligne 124 | Col 45 | AS124 | `=IF(AL124="positif",AN124,IF(AL124="negatif",-AN124,""))` | =IF(AL124="positif",AN124,IF(AL124="negatif",-AN124,"")) |
| Ligne 124 | Col 46 | AT124 | `=IF(AJ124>0,
IF(AS124>0, AR124*AS124^1.852,-AR124*ABS(AS124)^1.852),
IF(AS124>0, AR124*AN124^1.852, -AR124*AN124^1.852))` | =IF(AJ124>0,
IF(AS124>0, AR124*AS124^1.852,-AR124*ABS(AS124)^1.852),
IF(AS124>0, AR124*AN124^1.852, -AR124*AN124^1.852)) |
| Ligne 124 | Col 47 | AU124 | `=1.852*AR124*ABS(AS124)^(1.852-1)` | =1.852*AR124*ABS(AS124)^(1.852-1) |
| Ligne 124 | Col 48 | AV124 | `=AS124+$AN$146` | =AS124+$AN$146 |
| Ligne 125 | Col 8 | H125 | `=D39` | =D39 |
| Ligne 125 | Col 9 | I125 | `=I39` | =I39 |
| Ligne 125 | Col 10 | J125 | `=M39` | =M39 |
| Ligne 125 | Col 11 | K125 | `=I125*SIGN(J125)*ABS(J125)^1.821` | =I125*SIGN(J125)*ABS(J125)^1.821 |
| Ligne 125 | Col 12 | L125 | `=1.852*I125*ABS(J125)^(1.852-1)` | =1.852*I125*ABS(J125)^(1.852-1) |
| Ligne 125 | Col 13 | M125 | `=J125+$I$179` | =J125+$I$179 |
| Ligne 125 | Col 21 | U125 | `=P39` | =P39 |
| Ligne 125 | Col 22 | V125 | `=Q39` | =Q39 |
| Ligne 125 | Col 23 | W125 | `=S39` | =S39 |
| Ligne 125 | Col 24 | X125 | `=X39` | =X39 |
| Ligne 125 | Col 25 | Y125 | `=AD39` | =AD39 |
| Ligne 125 | Col 26 | Z125 | `=Z39` | =Z39 |
| Ligne 125 | Col 27 | AA125 | `=AA39` | =AA39 |
| Ligne 125 | Col 28 | AB125 | `=X125*SIGN(Y125)*ABS(Y125)^1.821` | =X125*SIGN(Y125)*ABS(Y125)^1.821 |
| Ligne 125 | Col 29 | AC125 | `=1.852*X125*ABS(Y125)^(1.852-1)` | =1.852*X125*ABS(Y125)^(1.852-1) |
| Ligne 125 | Col 30 | AD125 | `=IF(U125>0,
Y125+($I$179*Z125)+(AA125*X197),
Y125+$S$93)` | =IF(U125>0,
Y125+($I$179*Z125)+(AA125*X197),
Y125+$S$93) |
| Ligne 125 | Col 32 | AF125 | `=ABS(AD125)-ABS(Y125)` | =ABS(AD125)-ABS(Y125) |
| Ligne 125 | Col 40 | AN125 | `=ABS(AV39)` | =ABS(AV39) |
| Ligne 125 | Col 44 | AR125 | `= (10.679 * AQ125) / ((AO125/1000)^4.871 * AP125^1.852)` | = (10.679 * AQ125) / ((AO125/1000)^4.871 * AP125^1.852) |
| Ligne 125 | Col 45 | AS125 | `=IF(AL125="positif",AN125,IF(AL125="negatif",-AN125,""))` | =IF(AL125="positif",AN125,IF(AL125="negatif",-AN125,"")) |
| Ligne 125 | Col 46 | AT125 | `=IF(AJ125>0,
IF(AS125>0, AR125*AS125^1.852,-AR125*ABS(AS125)^1.852),
IF(AS125>0, AR125*AN125^1.852, -AR125*AN125^1.852))` | =IF(AJ125>0,
IF(AS125>0, AR125*AS125^1.852,-AR125*ABS(AS125)^1.852),
IF(AS125>0, AR125*AN125^1.852, -AR125*AN125^1.852)) |
| Ligne 125 | Col 47 | AU125 | `=1.852*AR125*ABS(AS125)^(1.852-1)` | =1.852*AR125*ABS(AS125)^(1.852-1) |
| Ligne 125 | Col 48 | AV125 | `=AS125+$AN$146` | =AS125+$AN$146 |
| Ligne 126 | Col 8 | H126 | `=D40` | =D40 |
| Ligne 126 | Col 9 | I126 | `=I40` | =I40 |
| Ligne 126 | Col 10 | J126 | `=M40` | =M40 |
| Ligne 126 | Col 11 | K126 | `=I126*SIGN(J126)*ABS(J126)^1.821` | =I126*SIGN(J126)*ABS(J126)^1.821 |
| Ligne 126 | Col 12 | L126 | `=1.852*I126*ABS(J126)^(1.852-1)` | =1.852*I126*ABS(J126)^(1.852-1) |
| Ligne 126 | Col 13 | M126 | `=J126+$I$179` | =J126+$I$179 |
| Ligne 126 | Col 21 | U126 | `=P40` | =P40 |
| Ligne 126 | Col 22 | V126 | `=Q40` | =Q40 |
| Ligne 126 | Col 23 | W126 | `=S40` | =S40 |
| Ligne 126 | Col 24 | X126 | `=X40` | =X40 |
| Ligne 126 | Col 25 | Y126 | `=AD40` | =AD40 |
| Ligne 126 | Col 26 | Z126 | `=Z40` | =Z40 |
| Ligne 126 | Col 27 | AA126 | `=AA40` | =AA40 |
| Ligne 126 | Col 28 | AB126 | `=X126*SIGN(Y126)*ABS(Y126)^1.821` | =X126*SIGN(Y126)*ABS(Y126)^1.821 |
| Ligne 126 | Col 29 | AC126 | `=1.852*X126*ABS(Y126)^(1.852-1)` | =1.852*X126*ABS(Y126)^(1.852-1) |
| Ligne 126 | Col 30 | AD126 | `=IF(U126>0,
Y126+($I$179*Z126)+(AA126*X198),
Y126+$S$93)` | =IF(U126>0,
Y126+($I$179*Z126)+(AA126*X198),
Y126+$S$93) |
| Ligne 126 | Col 32 | AF126 | `=ABS(AD126)-ABS(Y126)` | =ABS(AD126)-ABS(Y126) |
| Ligne 126 | Col 40 | AN126 | `=ABS(AV40)` | =ABS(AV40) |
| Ligne 126 | Col 44 | AR126 | `= (10.679 * AQ126) / ((AO126/1000)^4.871 * AP126^1.852)` | = (10.679 * AQ126) / ((AO126/1000)^4.871 * AP126^1.852) |
| Ligne 126 | Col 45 | AS126 | `=IF(AL126="positif",AN126,IF(AL126="negatif",-AN126,""))` | =IF(AL126="positif",AN126,IF(AL126="negatif",-AN126,"")) |
| Ligne 126 | Col 46 | AT126 | `=IF(AJ126>0,
IF(AS126>0, AR126*AS126^1.852,-AR126*ABS(AS126)^1.852),
IF(AS126>0, AR126*AN126^1.852, -AR126*AN126^1.852))` | =IF(AJ126>0,
IF(AS126>0, AR126*AS126^1.852,-AR126*ABS(AS126)^1.852),
IF(AS126>0, AR126*AN126^1.852, -AR126*AN126^1.852)) |
| Ligne 126 | Col 47 | AU126 | `=1.852*AR126*ABS(AS126)^(1.852-1)` | =1.852*AR126*ABS(AS126)^(1.852-1) |
| Ligne 126 | Col 48 | AV126 | `=AS126+$AN$146` | =AS126+$AN$146 |
| Ligne 127 | Col 8 | H127 | `=D41` | =D41 |
| Ligne 127 | Col 9 | I127 | `=I41` | =I41 |
| Ligne 127 | Col 10 | J127 | `=M41` | =M41 |
| Ligne 127 | Col 11 | K127 | `=I127*SIGN(J127)*ABS(J127)^1.821` | =I127*SIGN(J127)*ABS(J127)^1.821 |
| Ligne 127 | Col 12 | L127 | `=1.852*I127*ABS(J127)^(1.852-1)` | =1.852*I127*ABS(J127)^(1.852-1) |
| Ligne 127 | Col 13 | M127 | `=J127+$I$179` | =J127+$I$179 |
| Ligne 127 | Col 21 | U127 | `=P41` | =P41 |
| Ligne 127 | Col 22 | V127 | `=Q41` | =Q41 |
| Ligne 127 | Col 23 | W127 | `=S41` | =S41 |
| Ligne 127 | Col 24 | X127 | `=X41` | =X41 |
| Ligne 127 | Col 25 | Y127 | `=AD41` | =AD41 |
| Ligne 127 | Col 26 | Z127 | `=Z41` | =Z41 |
| Ligne 127 | Col 27 | AA127 | `=AA41` | =AA41 |
| Ligne 127 | Col 28 | AB127 | `=X127*SIGN(Y127)*ABS(Y127)^1.821` | =X127*SIGN(Y127)*ABS(Y127)^1.821 |
| Ligne 127 | Col 29 | AC127 | `=1.852*X127*ABS(Y127)^(1.852-1)` | =1.852*X127*ABS(Y127)^(1.852-1) |
| Ligne 127 | Col 30 | AD127 | `=IF(U127>0,
Y127+($I$179*Z127)+(AA127*X199),
Y127+$S$93)` | =IF(U127>0,
Y127+($I$179*Z127)+(AA127*X199),
Y127+$S$93) |
| Ligne 127 | Col 32 | AF127 | `=ABS(AD127)-ABS(Y127)` | =ABS(AD127)-ABS(Y127) |
| Ligne 127 | Col 40 | AN127 | `=ABS(AV41)` | =ABS(AV41) |
| Ligne 127 | Col 44 | AR127 | `= (10.679 * AQ127) / ((AO127/1000)^4.871 * AP127^1.852)` | = (10.679 * AQ127) / ((AO127/1000)^4.871 * AP127^1.852) |
| Ligne 127 | Col 45 | AS127 | `=IF(AL127="positif",AN127,IF(AL127="negatif",-AN127,""))` | =IF(AL127="positif",AN127,IF(AL127="negatif",-AN127,"")) |
| Ligne 127 | Col 46 | AT127 | `=IF(AJ127>0,
IF(AS127>0, AR127*AS127^1.852,-AR127*ABS(AS127)^1.852),
IF(AS127>0, AR127*AN127^1.852, -AR127*AN127^1.852))` | =IF(AJ127>0,
IF(AS127>0, AR127*AS127^1.852,-AR127*ABS(AS127)^1.852),
IF(AS127>0, AR127*AN127^1.852, -AR127*AN127^1.852)) |
| Ligne 127 | Col 47 | AU127 | `=1.852*AR127*ABS(AS127)^(1.852-1)` | =1.852*AR127*ABS(AS127)^(1.852-1) |
| Ligne 127 | Col 48 | AV127 | `=AS127+$AN$146` | =AS127+$AN$146 |
| Ligne 128 | Col 8 | H128 | `=D42` | =D42 |
| Ligne 128 | Col 9 | I128 | `=I42` | =I42 |
| Ligne 128 | Col 10 | J128 | `=M42` | =M42 |
| Ligne 128 | Col 11 | K128 | `=I128*SIGN(J128)*ABS(J128)^1.821` | =I128*SIGN(J128)*ABS(J128)^1.821 |
| Ligne 128 | Col 12 | L128 | `=1.852*I128*ABS(J128)^(1.852-1)` | =1.852*I128*ABS(J128)^(1.852-1) |
| Ligne 128 | Col 13 | M128 | `=J128+$I$179` | =J128+$I$179 |
| Ligne 128 | Col 21 | U128 | `=P42` | =P42 |
| Ligne 128 | Col 22 | V128 | `=Q42` | =Q42 |
| Ligne 128 | Col 23 | W128 | `=S42` | =S42 |
| Ligne 128 | Col 24 | X128 | `=X42` | =X42 |
| Ligne 128 | Col 25 | Y128 | `=AD42` | =AD42 |
| Ligne 128 | Col 26 | Z128 | `=Z42` | =Z42 |
| Ligne 128 | Col 27 | AA128 | `=AA42` | =AA42 |
| Ligne 128 | Col 28 | AB128 | `=X128*SIGN(Y128)*ABS(Y128)^1.821` | =X128*SIGN(Y128)*ABS(Y128)^1.821 |
| Ligne 128 | Col 29 | AC128 | `=1.852*X128*ABS(Y128)^(1.852-1)` | =1.852*X128*ABS(Y128)^(1.852-1) |
| Ligne 128 | Col 30 | AD128 | `=IF(U128>0,
Y128+($I$179*Z128)+(AA128*X200),
Y128+$S$93)` | =IF(U128>0,
Y128+($I$179*Z128)+(AA128*X200),
Y128+$S$93) |
| Ligne 128 | Col 32 | AF128 | `=ABS(AD128)-ABS(Y128)` | =ABS(AD128)-ABS(Y128) |
| Ligne 128 | Col 40 | AN128 | `=ABS(AV42)` | =ABS(AV42) |
| Ligne 128 | Col 44 | AR128 | `= (10.679 * AQ128) / ((AO128/1000)^4.871 * AP128^1.852)` | = (10.679 * AQ128) / ((AO128/1000)^4.871 * AP128^1.852) |
| Ligne 128 | Col 45 | AS128 | `=IF(AL128="positif",AN128,IF(AL128="negatif",-AN128,""))` | =IF(AL128="positif",AN128,IF(AL128="negatif",-AN128,"")) |
| Ligne 128 | Col 46 | AT128 | `=IF(AJ128>0,
IF(AS128>0, AR128*AS128^1.852,-AR128*ABS(AS128)^1.852),
IF(AS128>0, AR128*AN128^1.852, -AR128*AN128^1.852))` | =IF(AJ128>0,
IF(AS128>0, AR128*AS128^1.852,-AR128*ABS(AS128)^1.852),
IF(AS128>0, AR128*AN128^1.852, -AR128*AN128^1.852)) |
| Ligne 128 | Col 47 | AU128 | `=1.852*AR128*ABS(AS128)^(1.852-1)` | =1.852*AR128*ABS(AS128)^(1.852-1) |
| Ligne 128 | Col 48 | AV128 | `=AS128+$AN$146` | =AS128+$AN$146 |
| Ligne 129 | Col 8 | H129 | `=D43` | =D43 |
| Ligne 129 | Col 9 | I129 | `=I43` | =I43 |
| Ligne 129 | Col 10 | J129 | `=M43` | =M43 |
| Ligne 129 | Col 11 | K129 | `=I129*SIGN(J129)*ABS(J129)^1.821` | =I129*SIGN(J129)*ABS(J129)^1.821 |
| Ligne 129 | Col 12 | L129 | `=1.852*I129*ABS(J129)^(1.852-1)` | =1.852*I129*ABS(J129)^(1.852-1) |
| Ligne 129 | Col 13 | M129 | `=J129+$I$179` | =J129+$I$179 |
| Ligne 129 | Col 21 | U129 | `=P43` | =P43 |
| Ligne 129 | Col 22 | V129 | `=Q43` | =Q43 |
| Ligne 129 | Col 23 | W129 | `=S43` | =S43 |
| Ligne 129 | Col 24 | X129 | `=X43` | =X43 |
| Ligne 129 | Col 25 | Y129 | `=AD43` | =AD43 |
| Ligne 129 | Col 26 | Z129 | `=Z43` | =Z43 |
| Ligne 129 | Col 27 | AA129 | `=AA43` | =AA43 |
| Ligne 129 | Col 28 | AB129 | `=X129*SIGN(Y129)*ABS(Y129)^1.821` | =X129*SIGN(Y129)*ABS(Y129)^1.821 |
| Ligne 129 | Col 29 | AC129 | `=1.852*X129*ABS(Y129)^(1.852-1)` | =1.852*X129*ABS(Y129)^(1.852-1) |
| Ligne 129 | Col 30 | AD129 | `=IF(U129>0,
Y129+($I$179*Z129)+(AA129*X201),
Y129+$S$93)` | =IF(U129>0,
Y129+($I$179*Z129)+(AA129*X201),
Y129+$S$93) |
| Ligne 129 | Col 32 | AF129 | `=ABS(AD129)-ABS(Y129)` | =ABS(AD129)-ABS(Y129) |
| Ligne 129 | Col 40 | AN129 | `=ABS(AV43)` | =ABS(AV43) |
| Ligne 129 | Col 44 | AR129 | `= (10.679 * AQ129) / ((AO129/1000)^4.871 * AP129^1.852)` | = (10.679 * AQ129) / ((AO129/1000)^4.871 * AP129^1.852) |
| Ligne 129 | Col 45 | AS129 | `=IF(AL129="positif",AN129,IF(AL129="negatif",-AN129,""))` | =IF(AL129="positif",AN129,IF(AL129="negatif",-AN129,"")) |
| Ligne 129 | Col 46 | AT129 | `=IF(AJ129>0,
IF(AS129>0, AR129*AS129^1.852,-AR129*ABS(AS129)^1.852),
IF(AS129>0, AR129*AN129^1.852, -AR129*AN129^1.852))` | =IF(AJ129>0,
IF(AS129>0, AR129*AS129^1.852,-AR129*ABS(AS129)^1.852),
IF(AS129>0, AR129*AN129^1.852, -AR129*AN129^1.852)) |
| Ligne 129 | Col 47 | AU129 | `=1.852*AR129*ABS(AS129)^(1.852-1)` | =1.852*AR129*ABS(AS129)^(1.852-1) |
| Ligne 129 | Col 48 | AV129 | `=AS129+$AN$146` | =AS129+$AN$146 |
| Ligne 130 | Col 8 | H130 | `=D44` | =D44 |
| Ligne 130 | Col 9 | I130 | `=I44` | =I44 |
| Ligne 130 | Col 10 | J130 | `=M44` | =M44 |
| Ligne 130 | Col 11 | K130 | `=I130*SIGN(J130)*ABS(J130)^1.821` | =I130*SIGN(J130)*ABS(J130)^1.821 |
| Ligne 130 | Col 12 | L130 | `=1.852*I130*ABS(J130)^(1.852-1)` | =1.852*I130*ABS(J130)^(1.852-1) |
| Ligne 130 | Col 13 | M130 | `=J130+$I$179` | =J130+$I$179 |
| Ligne 130 | Col 21 | U130 | `=P44` | =P44 |
| Ligne 130 | Col 22 | V130 | `=Q44` | =Q44 |
| Ligne 130 | Col 23 | W130 | `=S44` | =S44 |
| Ligne 130 | Col 24 | X130 | `=X44` | =X44 |
| Ligne 130 | Col 25 | Y130 | `=AD44` | =AD44 |
| Ligne 130 | Col 26 | Z130 | `=Z44` | =Z44 |
| Ligne 130 | Col 27 | AA130 | `=AA44` | =AA44 |
| Ligne 130 | Col 28 | AB130 | `=X130*SIGN(Y130)*ABS(Y130)^1.821` | =X130*SIGN(Y130)*ABS(Y130)^1.821 |
| Ligne 130 | Col 29 | AC130 | `=1.852*X130*ABS(Y130)^(1.852-1)` | =1.852*X130*ABS(Y130)^(1.852-1) |
| Ligne 130 | Col 30 | AD130 | `=IF(U130>0,
Y130+($I$179*Z130)+(AA130*X202),
Y130+$S$93)` | =IF(U130>0,
Y130+($I$179*Z130)+(AA130*X202),
Y130+$S$93) |
| Ligne 130 | Col 32 | AF130 | `=ABS(AD130)-ABS(Y130)` | =ABS(AD130)-ABS(Y130) |
| Ligne 130 | Col 40 | AN130 | `=ABS(AV44)` | =ABS(AV44) |
| Ligne 130 | Col 44 | AR130 | `= (10.679 * AQ130) / ((AO130/1000)^4.871 * AP130^1.852)` | = (10.679 * AQ130) / ((AO130/1000)^4.871 * AP130^1.852) |
| Ligne 130 | Col 45 | AS130 | `=IF(AL130="positif",AN130,IF(AL130="negatif",-AN130,""))` | =IF(AL130="positif",AN130,IF(AL130="negatif",-AN130,"")) |
| Ligne 130 | Col 46 | AT130 | `=IF(AJ130>0,
IF(AS130>0, AR130*AS130^1.852,-AR130*ABS(AS130)^1.852),
IF(AS130>0, AR130*AN130^1.852, -AR130*AN130^1.852))` | =IF(AJ130>0,
IF(AS130>0, AR130*AS130^1.852,-AR130*ABS(AS130)^1.852),
IF(AS130>0, AR130*AN130^1.852, -AR130*AN130^1.852)) |
| Ligne 130 | Col 47 | AU130 | `=1.852*AR130*ABS(AS130)^(1.852-1)` | =1.852*AR130*ABS(AS130)^(1.852-1) |
| Ligne 130 | Col 48 | AV130 | `=AS130+$AN$146` | =AS130+$AN$146 |
| Ligne 131 | Col 8 | H131 | `=D45` | =D45 |
| Ligne 131 | Col 9 | I131 | `=I45` | =I45 |
| Ligne 131 | Col 10 | J131 | `=M45` | =M45 |
| Ligne 131 | Col 11 | K131 | `=I131*SIGN(J131)*ABS(J131)^1.821` | =I131*SIGN(J131)*ABS(J131)^1.821 |
| Ligne 131 | Col 12 | L131 | `=1.852*I131*ABS(J131)^(1.852-1)` | =1.852*I131*ABS(J131)^(1.852-1) |
| Ligne 131 | Col 13 | M131 | `=J131+$I$179` | =J131+$I$179 |
| Ligne 131 | Col 21 | U131 | `=P45` | =P45 |
| Ligne 131 | Col 22 | V131 | `=Q45` | =Q45 |
| Ligne 131 | Col 23 | W131 | `=S45` | =S45 |
| Ligne 131 | Col 24 | X131 | `=X45` | =X45 |
| Ligne 131 | Col 25 | Y131 | `=AD45` | =AD45 |
| Ligne 131 | Col 26 | Z131 | `=Z45` | =Z45 |
| Ligne 131 | Col 27 | AA131 | `=AA45` | =AA45 |
| Ligne 131 | Col 28 | AB131 | `=X131*SIGN(Y131)*ABS(Y131)^1.821` | =X131*SIGN(Y131)*ABS(Y131)^1.821 |
| Ligne 131 | Col 29 | AC131 | `=1.852*X131*ABS(Y131)^(1.852-1)` | =1.852*X131*ABS(Y131)^(1.852-1) |
| Ligne 131 | Col 30 | AD131 | `=IF(U131>0,
Y131+($I$179*Z131)+(AA131*X203),
Y131+$S$93)` | =IF(U131>0,
Y131+($I$179*Z131)+(AA131*X203),
Y131+$S$93) |
| Ligne 131 | Col 32 | AF131 | `=ABS(AD131)-ABS(Y131)` | =ABS(AD131)-ABS(Y131) |
| Ligne 131 | Col 40 | AN131 | `=ABS(AV45)` | =ABS(AV45) |
| Ligne 131 | Col 44 | AR131 | `= (10.679 * AQ131) / ((AO131/1000)^4.871 * AP131^1.852)` | = (10.679 * AQ131) / ((AO131/1000)^4.871 * AP131^1.852) |
| Ligne 131 | Col 45 | AS131 | `=IF(AL131="positif",AN131,IF(AL131="negatif",-AN131,""))` | =IF(AL131="positif",AN131,IF(AL131="negatif",-AN131,"")) |
| Ligne 131 | Col 46 | AT131 | `=IF(AJ131>0,
IF(AS131>0, AR131*AS131^1.852,-AR131*ABS(AS131)^1.852),
IF(AS131>0, AR131*AN131^1.852, -AR131*AN131^1.852))` | =IF(AJ131>0,
IF(AS131>0, AR131*AS131^1.852,-AR131*ABS(AS131)^1.852),
IF(AS131>0, AR131*AN131^1.852, -AR131*AN131^1.852)) |
| Ligne 131 | Col 47 | AU131 | `=1.852*AR131*ABS(AS131)^(1.852-1)` | =1.852*AR131*ABS(AS131)^(1.852-1) |
| Ligne 131 | Col 48 | AV131 | `=AS131+$AN$146` | =AS131+$AN$146 |
| Ligne 132 | Col 8 | H132 | `=D46` | =D46 |
| Ligne 132 | Col 9 | I132 | `=I46` | =I46 |
| Ligne 132 | Col 10 | J132 | `=M46` | =M46 |
| Ligne 132 | Col 11 | K132 | `=I132*SIGN(J132)*ABS(J132)^1.821` | =I132*SIGN(J132)*ABS(J132)^1.821 |
| Ligne 132 | Col 12 | L132 | `=1.852*I132*ABS(J132)^(1.852-1)` | =1.852*I132*ABS(J132)^(1.852-1) |
| Ligne 132 | Col 13 | M132 | `=J132+$I$179` | =J132+$I$179 |
| Ligne 132 | Col 21 | U132 | `=P46` | =P46 |
| Ligne 132 | Col 22 | V132 | `=Q46` | =Q46 |
| Ligne 132 | Col 23 | W132 | `=S46` | =S46 |
| Ligne 132 | Col 24 | X132 | `=X46` | =X46 |
| Ligne 132 | Col 25 | Y132 | `=AD46` | =AD46 |
| Ligne 132 | Col 26 | Z132 | `=Z46` | =Z46 |
| Ligne 132 | Col 27 | AA132 | `=AA46` | =AA46 |
| Ligne 132 | Col 28 | AB132 | `=X132*SIGN(Y132)*ABS(Y132)^1.821` | =X132*SIGN(Y132)*ABS(Y132)^1.821 |
| Ligne 132 | Col 29 | AC132 | `=1.852*X132*ABS(Y132)^(1.852-1)` | =1.852*X132*ABS(Y132)^(1.852-1) |
| Ligne 132 | Col 30 | AD132 | `=IF(U132>0,
Y132+($I$179*Z132)+(AA132*X204),
Y132+$S$93)` | =IF(U132>0,
Y132+($I$179*Z132)+(AA132*X204),
Y132+$S$93) |
| Ligne 132 | Col 32 | AF132 | `=ABS(AD132)-ABS(Y132)` | =ABS(AD132)-ABS(Y132) |
| Ligne 132 | Col 40 | AN132 | `=ABS(AV46)` | =ABS(AV46) |
| Ligne 132 | Col 44 | AR132 | `= (10.679 * AQ132) / ((AO132/1000)^4.871 * AP132^1.852)` | = (10.679 * AQ132) / ((AO132/1000)^4.871 * AP132^1.852) |
| Ligne 132 | Col 45 | AS132 | `=IF(AL132="positif",AN132,IF(AL132="negatif",-AN132,""))` | =IF(AL132="positif",AN132,IF(AL132="negatif",-AN132,"")) |
| Ligne 132 | Col 46 | AT132 | `=IF(AJ132>0,
IF(AS132>0, AR132*AS132^1.852,-AR132*ABS(AS132)^1.852),
IF(AS132>0, AR132*AN132^1.852, -AR132*AN132^1.852))` | =IF(AJ132>0,
IF(AS132>0, AR132*AS132^1.852,-AR132*ABS(AS132)^1.852),
IF(AS132>0, AR132*AN132^1.852, -AR132*AN132^1.852)) |
| Ligne 132 | Col 47 | AU132 | `=1.852*AR132*ABS(AS132)^(1.852-1)` | =1.852*AR132*ABS(AS132)^(1.852-1) |
| Ligne 132 | Col 48 | AV132 | `=AS132+$AN$146` | =AS132+$AN$146 |
| Ligne 133 | Col 8 | H133 | `=D47` | =D47 |
| Ligne 133 | Col 9 | I133 | `=I47` | =I47 |
| Ligne 133 | Col 10 | J133 | `=M47` | =M47 |
| Ligne 133 | Col 11 | K133 | `=I133*SIGN(J133)*ABS(J133)^1.821` | =I133*SIGN(J133)*ABS(J133)^1.821 |
| Ligne 133 | Col 12 | L133 | `=1.852*I133*ABS(J133)^(1.852-1)` | =1.852*I133*ABS(J133)^(1.852-1) |
| Ligne 133 | Col 13 | M133 | `=J133+$I$179` | =J133+$I$179 |
| Ligne 133 | Col 21 | U133 | `=P47` | =P47 |
| Ligne 133 | Col 22 | V133 | `=Q47` | =Q47 |
| Ligne 133 | Col 23 | W133 | `=S47` | =S47 |
| Ligne 133 | Col 24 | X133 | `=X47` | =X47 |
| Ligne 133 | Col 25 | Y133 | `=AD47` | =AD47 |
| Ligne 133 | Col 26 | Z133 | `=Z47` | =Z47 |
| Ligne 133 | Col 27 | AA133 | `=AA47` | =AA47 |
| Ligne 133 | Col 28 | AB133 | `=X133*SIGN(Y133)*ABS(Y133)^1.821` | =X133*SIGN(Y133)*ABS(Y133)^1.821 |
| Ligne 133 | Col 29 | AC133 | `=1.852*X133*ABS(Y133)^(1.852-1)` | =1.852*X133*ABS(Y133)^(1.852-1) |
| Ligne 133 | Col 30 | AD133 | `=IF(U133>0,
Y133+($I$179*Z133)+(AA133*X205),
Y133+$S$93)` | =IF(U133>0,
Y133+($I$179*Z133)+(AA133*X205),
Y133+$S$93) |
| Ligne 133 | Col 32 | AF133 | `=ABS(AD133)-ABS(Y133)` | =ABS(AD133)-ABS(Y133) |
| Ligne 133 | Col 40 | AN133 | `=ABS(AV47)` | =ABS(AV47) |
| Ligne 133 | Col 44 | AR133 | `= (10.679 * AQ133) / ((AO133/1000)^4.871 * AP133^1.852)` | = (10.679 * AQ133) / ((AO133/1000)^4.871 * AP133^1.852) |
| Ligne 133 | Col 45 | AS133 | `=IF(AL133="positif",AN133,IF(AL133="negatif",-AN133,""))` | =IF(AL133="positif",AN133,IF(AL133="negatif",-AN133,"")) |
| Ligne 133 | Col 46 | AT133 | `=IF(AJ133>0,
IF(AS133>0, AR133*AS133^1.852,-AR133*ABS(AS133)^1.852),
IF(AS133>0, AR133*AN133^1.852, -AR133*AN133^1.852))` | =IF(AJ133>0,
IF(AS133>0, AR133*AS133^1.852,-AR133*ABS(AS133)^1.852),
IF(AS133>0, AR133*AN133^1.852, -AR133*AN133^1.852)) |
| Ligne 133 | Col 47 | AU133 | `=1.852*AR133*ABS(AS133)^(1.852-1)` | =1.852*AR133*ABS(AS133)^(1.852-1) |
| Ligne 133 | Col 48 | AV133 | `=AS133+$AN$146` | =AS133+$AN$146 |
| Ligne 134 | Col 8 | H134 | `=D48` | =D48 |
| Ligne 134 | Col 9 | I134 | `=I48` | =I48 |
| Ligne 134 | Col 10 | J134 | `=M48` | =M48 |
| Ligne 134 | Col 11 | K134 | `=I134*SIGN(J134)*ABS(J134)^1.821` | =I134*SIGN(J134)*ABS(J134)^1.821 |
| Ligne 134 | Col 12 | L134 | `=1.852*I134*ABS(J134)^(1.852-1)` | =1.852*I134*ABS(J134)^(1.852-1) |
| Ligne 134 | Col 13 | M134 | `=J134+$I$179` | =J134+$I$179 |
| Ligne 134 | Col 21 | U134 | `=P48` | =P48 |
| Ligne 134 | Col 22 | V134 | `=Q48` | =Q48 |
| Ligne 134 | Col 23 | W134 | `=S48` | =S48 |
| Ligne 134 | Col 24 | X134 | `=X48` | =X48 |
| Ligne 134 | Col 25 | Y134 | `=AD48` | =AD48 |
| Ligne 134 | Col 26 | Z134 | `=Z48` | =Z48 |
| Ligne 134 | Col 27 | AA134 | `=AA48` | =AA48 |
| Ligne 134 | Col 28 | AB134 | `=X134*SIGN(Y134)*ABS(Y134)^1.821` | =X134*SIGN(Y134)*ABS(Y134)^1.821 |
| Ligne 134 | Col 29 | AC134 | `=1.852*X134*ABS(Y134)^(1.852-1)` | =1.852*X134*ABS(Y134)^(1.852-1) |
| Ligne 134 | Col 30 | AD134 | `=IF(U134>0,
Y134+($I$179*Z134)+(AA134*X206),
Y134+$S$93)` | =IF(U134>0,
Y134+($I$179*Z134)+(AA134*X206),
Y134+$S$93) |
| Ligne 134 | Col 32 | AF134 | `=ABS(AD134)-ABS(Y134)` | =ABS(AD134)-ABS(Y134) |
| Ligne 134 | Col 40 | AN134 | `=ABS(AV48)` | =ABS(AV48) |
| Ligne 134 | Col 44 | AR134 | `= (10.679 * AQ134) / ((AO134/1000)^4.871 * AP134^1.852)` | = (10.679 * AQ134) / ((AO134/1000)^4.871 * AP134^1.852) |
| Ligne 134 | Col 45 | AS134 | `=IF(AL134="positif",AN134,IF(AL134="negatif",-AN134,""))` | =IF(AL134="positif",AN134,IF(AL134="negatif",-AN134,"")) |
| Ligne 134 | Col 46 | AT134 | `=IF(AJ134>0,
IF(AS134>0, AR134*AS134^1.852,-AR134*ABS(AS134)^1.852),
IF(AS134>0, AR134*AN134^1.852, -AR134*AN134^1.852))` | =IF(AJ134>0,
IF(AS134>0, AR134*AS134^1.852,-AR134*ABS(AS134)^1.852),
IF(AS134>0, AR134*AN134^1.852, -AR134*AN134^1.852)) |
| Ligne 134 | Col 47 | AU134 | `=1.852*AR134*ABS(AS134)^(1.852-1)` | =1.852*AR134*ABS(AS134)^(1.852-1) |
| Ligne 134 | Col 48 | AV134 | `=AS134+$AN$146` | =AS134+$AN$146 |
| Ligne 135 | Col 8 | H135 | `=D49` | =D49 |
| Ligne 135 | Col 9 | I135 | `=I49` | =I49 |
| Ligne 135 | Col 10 | J135 | `=M49` | =M49 |
| Ligne 135 | Col 11 | K135 | `=I135*SIGN(J135)*ABS(J135)^1.821` | =I135*SIGN(J135)*ABS(J135)^1.821 |
| Ligne 135 | Col 12 | L135 | `=1.852*I135*ABS(J135)^(1.852-1)` | =1.852*I135*ABS(J135)^(1.852-1) |
| Ligne 135 | Col 13 | M135 | `=J135+$I$179` | =J135+$I$179 |
| Ligne 135 | Col 21 | U135 | `=P49` | =P49 |
| Ligne 135 | Col 22 | V135 | `=Q49` | =Q49 |
| Ligne 135 | Col 23 | W135 | `=S49` | =S49 |
| Ligne 135 | Col 24 | X135 | `=X49` | =X49 |
| Ligne 135 | Col 25 | Y135 | `=AD49` | =AD49 |
| Ligne 135 | Col 26 | Z135 | `=Z49` | =Z49 |
| Ligne 135 | Col 27 | AA135 | `=AA49` | =AA49 |
| Ligne 135 | Col 28 | AB135 | `=X135*SIGN(Y135)*ABS(Y135)^1.821` | =X135*SIGN(Y135)*ABS(Y135)^1.821 |
| Ligne 135 | Col 29 | AC135 | `=1.852*X135*ABS(Y135)^(1.852-1)` | =1.852*X135*ABS(Y135)^(1.852-1) |
| Ligne 135 | Col 30 | AD135 | `=IF(U135>0,
Y135+($I$179*Z135)+(AA135*X207),
Y135+$S$93)` | =IF(U135>0,
Y135+($I$179*Z135)+(AA135*X207),
Y135+$S$93) |
| Ligne 135 | Col 32 | AF135 | `=ABS(AD135)-ABS(Y135)` | =ABS(AD135)-ABS(Y135) |
| Ligne 135 | Col 40 | AN135 | `=ABS(AV49)` | =ABS(AV49) |
| Ligne 135 | Col 44 | AR135 | `= (10.679 * AQ135) / ((AO135/1000)^4.871 * AP135^1.852)` | = (10.679 * AQ135) / ((AO135/1000)^4.871 * AP135^1.852) |
| Ligne 135 | Col 45 | AS135 | `=IF(AL135="positif",AN135,IF(AL135="negatif",-AN135,""))` | =IF(AL135="positif",AN135,IF(AL135="negatif",-AN135,"")) |
| Ligne 135 | Col 46 | AT135 | `=IF(AJ135>0,
IF(AS135>0, AR135*AS135^1.852,-AR135*ABS(AS135)^1.852),
IF(AS135>0, AR135*AN135^1.852, -AR135*AN135^1.852))` | =IF(AJ135>0,
IF(AS135>0, AR135*AS135^1.852,-AR135*ABS(AS135)^1.852),
IF(AS135>0, AR135*AN135^1.852, -AR135*AN135^1.852)) |
| Ligne 135 | Col 47 | AU135 | `=1.852*AR135*ABS(AS135)^(1.852-1)` | =1.852*AR135*ABS(AS135)^(1.852-1) |
| Ligne 135 | Col 48 | AV135 | `=AS135+$AN$146` | =AS135+$AN$146 |
| Ligne 136 | Col 8 | H136 | `=D50` | =D50 |
| Ligne 136 | Col 9 | I136 | `=I50` | =I50 |
| Ligne 136 | Col 10 | J136 | `=M50` | =M50 |
| Ligne 136 | Col 11 | K136 | `=I136*SIGN(J136)*ABS(J136)^1.821` | =I136*SIGN(J136)*ABS(J136)^1.821 |
| Ligne 136 | Col 12 | L136 | `=1.852*I136*ABS(J136)^(1.852-1)` | =1.852*I136*ABS(J136)^(1.852-1) |
| Ligne 136 | Col 13 | M136 | `=J136+$I$179` | =J136+$I$179 |
| Ligne 136 | Col 21 | U136 | `=P50` | =P50 |
| Ligne 136 | Col 22 | V136 | `=Q50` | =Q50 |
| Ligne 136 | Col 23 | W136 | `=S50` | =S50 |
| Ligne 136 | Col 24 | X136 | `=X50` | =X50 |
| Ligne 136 | Col 25 | Y136 | `=AD50` | =AD50 |
| Ligne 136 | Col 26 | Z136 | `=Z50` | =Z50 |
| Ligne 136 | Col 27 | AA136 | `=AA50` | =AA50 |
| Ligne 136 | Col 28 | AB136 | `=X136*SIGN(Y136)*ABS(Y136)^1.821` | =X136*SIGN(Y136)*ABS(Y136)^1.821 |
| Ligne 136 | Col 29 | AC136 | `=1.852*X136*ABS(Y136)^(1.852-1)` | =1.852*X136*ABS(Y136)^(1.852-1) |
| Ligne 136 | Col 30 | AD136 | `=IF(U136>0,
Y136+($I$179*Z136)+(AA136*X208),
Y136+$S$93)` | =IF(U136>0,
Y136+($I$179*Z136)+(AA136*X208),
Y136+$S$93) |
| Ligne 136 | Col 32 | AF136 | `=ABS(AD136)-ABS(Y136)` | =ABS(AD136)-ABS(Y136) |
| Ligne 136 | Col 40 | AN136 | `=ABS(AV50)` | =ABS(AV50) |
| Ligne 136 | Col 44 | AR136 | `= (10.679 * AQ136) / ((AO136/1000)^4.871 * AP136^1.852)` | = (10.679 * AQ136) / ((AO136/1000)^4.871 * AP136^1.852) |
| Ligne 136 | Col 45 | AS136 | `=IF(AL136="positif",AN136,IF(AL136="negatif",-AN136,""))` | =IF(AL136="positif",AN136,IF(AL136="negatif",-AN136,"")) |
| Ligne 136 | Col 46 | AT136 | `=IF(AJ136>0,
        IF(AS136>0, AR136*AS136^1.852,-AR136*ABS(AS136)^1.852),
        IF(AS136>0, AR136*AN136^1.852, -AR136*AN136^1.852))` | =IF(AJ136>0,
        IF(AS136>0, AR136*AS136^1.852,-AR136*ABS(AS136)^1.852),
        IF(AS136>0, AR136*AN136^1.852, -AR136*AN136^1.852)) |
| Ligne 136 | Col 47 | AU136 | `=1.852*AR136*ABS(AS136)^(1.852-1)` | =1.852*AR136*ABS(AS136)^(1.852-1) |
| Ligne 136 | Col 48 | AV136 | `=AS136+$AN$146` | =AS136+$AN$146 |
| Ligne 137 | Col 8 | H137 | `=D51` | =D51 |
| Ligne 137 | Col 9 | I137 | `=I51` | =I51 |
| Ligne 137 | Col 10 | J137 | `=M51` | =M51 |
| Ligne 137 | Col 11 | K137 | `=I137*SIGN(J137)*ABS(J137)^1.821` | =I137*SIGN(J137)*ABS(J137)^1.821 |
| Ligne 137 | Col 12 | L137 | `=1.852*I137*ABS(J137)^(1.852-1)` | =1.852*I137*ABS(J137)^(1.852-1) |
| Ligne 137 | Col 13 | M137 | `=J137+$I$179` | =J137+$I$179 |
| Ligne 137 | Col 21 | U137 | `=P51` | =P51 |
| Ligne 137 | Col 22 | V137 | `=Q51` | =Q51 |
| Ligne 137 | Col 23 | W137 | `=S51` | =S51 |
| Ligne 137 | Col 24 | X137 | `=X51` | =X51 |
| Ligne 137 | Col 25 | Y137 | `=AD51` | =AD51 |
| Ligne 137 | Col 26 | Z137 | `=Z51` | =Z51 |
| Ligne 137 | Col 27 | AA137 | `=AA51` | =AA51 |
| Ligne 137 | Col 28 | AB137 | `=X137*SIGN(Y137)*ABS(Y137)^1.821` | =X137*SIGN(Y137)*ABS(Y137)^1.821 |
| Ligne 137 | Col 29 | AC137 | `=1.852*X137*ABS(Y137)^(1.852-1)` | =1.852*X137*ABS(Y137)^(1.852-1) |
| Ligne 137 | Col 30 | AD137 | `=IF(U137>0,
Y137+($I$179*Z137)+(AA137*X209),
Y137+$S$93)` | =IF(U137>0,
Y137+($I$179*Z137)+(AA137*X209),
Y137+$S$93) |
| Ligne 137 | Col 32 | AF137 | `=ABS(AD137)-ABS(Y137)` | =ABS(AD137)-ABS(Y137) |
| Ligne 137 | Col 40 | AN137 | `=ABS(AV51)` | =ABS(AV51) |
| Ligne 137 | Col 44 | AR137 | `= (10.679 * AQ137) / ((AO137/1000)^4.871 * AP137^1.852)` | = (10.679 * AQ137) / ((AO137/1000)^4.871 * AP137^1.852) |
| Ligne 137 | Col 45 | AS137 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57530>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57530> |
| Ligne 137 | Col 46 | AT137 | `=IF(AJ137>0,
        IF(AS137>0, AR137*AS137^1.852,-AR137*ABS(AS137)^1.852),
        IF(AS137>0, AR137*AN137^1.852, -AR137*AN137^1.852))` | =IF(AJ137>0,
        IF(AS137>0, AR137*AS137^1.852,-AR137*ABS(AS137)^1.852),
        IF(AS137>0, AR137*AN137^1.852, -AR137*AN137^1.852)) |
| Ligne 137 | Col 47 | AU137 | `=1.852*AR137*ABS(AS137)^(1.852-1)` | =1.852*AR137*ABS(AS137)^(1.852-1) |
| Ligne 137 | Col 48 | AV137 | `=AS137+$AN$146` | =AS137+$AN$146 |
| Ligne 138 | Col 8 | H138 | `=D52` | =D52 |
| Ligne 138 | Col 9 | I138 | `=I52` | =I52 |
| Ligne 138 | Col 10 | J138 | `=M52` | =M52 |
| Ligne 138 | Col 11 | K138 | `=I138*SIGN(J138)*ABS(J138)^1.821` | =I138*SIGN(J138)*ABS(J138)^1.821 |
| Ligne 138 | Col 12 | L138 | `=1.852*I138*ABS(J138)^(1.852-1)` | =1.852*I138*ABS(J138)^(1.852-1) |
| Ligne 138 | Col 13 | M138 | `=J138+$I$179` | =J138+$I$179 |
| Ligne 138 | Col 21 | U138 | `=P52` | =P52 |
| Ligne 138 | Col 22 | V138 | `=Q52` | =Q52 |
| Ligne 138 | Col 23 | W138 | `=S52` | =S52 |
| Ligne 138 | Col 24 | X138 | `=X52` | =X52 |
| Ligne 138 | Col 25 | Y138 | `=AD52` | =AD52 |
| Ligne 138 | Col 26 | Z138 | `=Z52` | =Z52 |
| Ligne 138 | Col 27 | AA138 | `=AA52` | =AA52 |
| Ligne 138 | Col 28 | AB138 | `=X138*SIGN(Y138)*ABS(Y138)^1.821` | =X138*SIGN(Y138)*ABS(Y138)^1.821 |
| Ligne 138 | Col 29 | AC138 | `=1.852*X138*ABS(Y138)^(1.852-1)` | =1.852*X138*ABS(Y138)^(1.852-1) |
| Ligne 138 | Col 30 | AD138 | `=IF(U138>0,
Y138+($I$179*Z138)+(AA138*X210),
Y138+$S$93)` | =IF(U138>0,
Y138+($I$179*Z138)+(AA138*X210),
Y138+$S$93) |
| Ligne 138 | Col 32 | AF138 | `=ABS(AD138)-ABS(Y138)` | =ABS(AD138)-ABS(Y138) |
| Ligne 138 | Col 40 | AN138 | `=ABS(AV52)` | =ABS(AV52) |
| Ligne 138 | Col 44 | AR138 | `= (10.679 * AQ138) / ((AO138/1000)^4.871 * AP138^1.852)` | = (10.679 * AQ138) / ((AO138/1000)^4.871 * AP138^1.852) |
| Ligne 138 | Col 45 | AS138 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA575F0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA575F0> |
| Ligne 138 | Col 46 | AT138 | `=IF(AJ138>0,
        IF(AS138>0, AR138*AS138^1.852,-AR138*ABS(AS138)^1.852),
        IF(AS138>0, AR138*AN138^1.852, -AR138*AN138^1.852))` | =IF(AJ138>0,
        IF(AS138>0, AR138*AS138^1.852,-AR138*ABS(AS138)^1.852),
        IF(AS138>0, AR138*AN138^1.852, -AR138*AN138^1.852)) |
| Ligne 138 | Col 47 | AU138 | `=1.852*AR138*ABS(AS138)^(1.852-1)` | =1.852*AR138*ABS(AS138)^(1.852-1) |
| Ligne 138 | Col 48 | AV138 | `=AS138+$AN$146` | =AS138+$AN$146 |
| Ligne 139 | Col 8 | H139 | `=D53` | =D53 |
| Ligne 139 | Col 9 | I139 | `=I53` | =I53 |
| Ligne 139 | Col 10 | J139 | `=M53` | =M53 |
| Ligne 139 | Col 11 | K139 | `=I139*SIGN(J139)*ABS(J139)^1.821` | =I139*SIGN(J139)*ABS(J139)^1.821 |
| Ligne 139 | Col 12 | L139 | `=1.852*I139*ABS(J139)^(1.852-1)` | =1.852*I139*ABS(J139)^(1.852-1) |
| Ligne 139 | Col 13 | M139 | `=J139+$I$179` | =J139+$I$179 |
| Ligne 139 | Col 21 | U139 | `=P53` | =P53 |
| Ligne 139 | Col 22 | V139 | `=Q53` | =Q53 |
| Ligne 139 | Col 23 | W139 | `=S53` | =S53 |
| Ligne 139 | Col 24 | X139 | `=X53` | =X53 |
| Ligne 139 | Col 25 | Y139 | `=AD53` | =AD53 |
| Ligne 139 | Col 26 | Z139 | `=Z53` | =Z53 |
| Ligne 139 | Col 27 | AA139 | `=AA53` | =AA53 |
| Ligne 139 | Col 28 | AB139 | `=X139*SIGN(Y139)*ABS(Y139)^1.821` | =X139*SIGN(Y139)*ABS(Y139)^1.821 |
| Ligne 139 | Col 29 | AC139 | `=1.852*X139*ABS(Y139)^(1.852-1)` | =1.852*X139*ABS(Y139)^(1.852-1) |
| Ligne 139 | Col 30 | AD139 | `=IF(U139>0,
Y139+($I$179*Z139)+(AA139*X211),
Y139+$S$93)` | =IF(U139>0,
Y139+($I$179*Z139)+(AA139*X211),
Y139+$S$93) |
| Ligne 139 | Col 32 | AF139 | `=ABS(AD139)-ABS(Y139)` | =ABS(AD139)-ABS(Y139) |
| Ligne 139 | Col 40 | AN139 | `=ABS(AV53)` | =ABS(AV53) |
| Ligne 139 | Col 44 | AR139 | `= (10.679 * AQ139) / ((AO139/1000)^4.871 * AP139^1.852)` | = (10.679 * AQ139) / ((AO139/1000)^4.871 * AP139^1.852) |
| Ligne 139 | Col 45 | AS139 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA576B0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA576B0> |
| Ligne 139 | Col 46 | AT139 | `=IF(AJ139>0,
        IF(AS139>0, AR139*AS139^1.852,-AR139*ABS(AS139)^1.852),
        IF(AS139>0, AR139*AN139^1.852, -AR139*AN139^1.852))` | =IF(AJ139>0,
        IF(AS139>0, AR139*AS139^1.852,-AR139*ABS(AS139)^1.852),
        IF(AS139>0, AR139*AN139^1.852, -AR139*AN139^1.852)) |
| Ligne 139 | Col 47 | AU139 | `=1.852*AR139*ABS(AS139)^(1.852-1)` | =1.852*AR139*ABS(AS139)^(1.852-1) |
| Ligne 139 | Col 48 | AV139 | `=AS139+$AN$146` | =AS139+$AN$146 |
| Ligne 140 | Col 8 | H140 | `=D54` | =D54 |
| Ligne 140 | Col 9 | I140 | `=I54` | =I54 |
| Ligne 140 | Col 10 | J140 | `=M54` | =M54 |
| Ligne 140 | Col 11 | K140 | `=I140*SIGN(J140)*ABS(J140)^1.821` | =I140*SIGN(J140)*ABS(J140)^1.821 |
| Ligne 140 | Col 12 | L140 | `=1.852*I140*ABS(J140)^(1.852-1)` | =1.852*I140*ABS(J140)^(1.852-1) |
| Ligne 140 | Col 13 | M140 | `=J140+$I$179` | =J140+$I$179 |
| Ligne 140 | Col 21 | U140 | `=P54` | =P54 |
| Ligne 140 | Col 22 | V140 | `=Q54` | =Q54 |
| Ligne 140 | Col 23 | W140 | `=S54` | =S54 |
| Ligne 140 | Col 24 | X140 | `=X54` | =X54 |
| Ligne 140 | Col 25 | Y140 | `=AD54` | =AD54 |
| Ligne 140 | Col 26 | Z140 | `=Z54` | =Z54 |
| Ligne 140 | Col 27 | AA140 | `=AA54` | =AA54 |
| Ligne 140 | Col 28 | AB140 | `=X140*SIGN(Y140)*ABS(Y140)^1.821` | =X140*SIGN(Y140)*ABS(Y140)^1.821 |
| Ligne 140 | Col 29 | AC140 | `=1.852*X140*ABS(Y140)^(1.852-1)` | =1.852*X140*ABS(Y140)^(1.852-1) |
| Ligne 140 | Col 30 | AD140 | `=IF(U140>0,
Y140+($I$179*Z140)+(AA140*X212),
Y140+$S$93)` | =IF(U140>0,
Y140+($I$179*Z140)+(AA140*X212),
Y140+$S$93) |
| Ligne 140 | Col 32 | AF140 | `=ABS(AD140)-ABS(Y140)` | =ABS(AD140)-ABS(Y140) |
| Ligne 140 | Col 40 | AN140 | `=ABS(AV54)` | =ABS(AV54) |
| Ligne 140 | Col 44 | AR140 | `= (10.679 * AQ140) / ((AO140/1000)^4.871 * AP140^1.852)` | = (10.679 * AQ140) / ((AO140/1000)^4.871 * AP140^1.852) |
| Ligne 140 | Col 45 | AS140 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57CB0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57CB0> |
| Ligne 140 | Col 46 | AT140 | `=IF(AJ140>0,
        IF(AS140>0, AR140*AS140^1.852,-AR140*ABS(AS140)^1.852),
        IF(AS140>0, AR140*AN140^1.852, -AR140*AN140^1.852))` | =IF(AJ140>0,
        IF(AS140>0, AR140*AS140^1.852,-AR140*ABS(AS140)^1.852),
        IF(AS140>0, AR140*AN140^1.852, -AR140*AN140^1.852)) |
| Ligne 140 | Col 47 | AU140 | `=1.852*AR140*ABS(AS140)^(1.852-1)` | =1.852*AR140*ABS(AS140)^(1.852-1) |
| Ligne 140 | Col 48 | AV140 | `=AS140+$AN$146` | =AS140+$AN$146 |
| Ligne 141 | Col 8 | H141 | `=D55` | =D55 |
| Ligne 141 | Col 9 | I141 | `=I55` | =I55 |
| Ligne 141 | Col 10 | J141 | `=M55` | =M55 |
| Ligne 141 | Col 11 | K141 | `=I141*SIGN(J141)*ABS(J141)^1.821` | =I141*SIGN(J141)*ABS(J141)^1.821 |
| Ligne 141 | Col 12 | L141 | `=1.852*I141*ABS(J141)^(1.852-1)` | =1.852*I141*ABS(J141)^(1.852-1) |
| Ligne 141 | Col 13 | M141 | `=J141+$I$179` | =J141+$I$179 |
| Ligne 141 | Col 21 | U141 | `=P55` | =P55 |
| Ligne 141 | Col 22 | V141 | `=Q55` | =Q55 |
| Ligne 141 | Col 23 | W141 | `=S55` | =S55 |
| Ligne 141 | Col 24 | X141 | `=X55` | =X55 |
| Ligne 141 | Col 25 | Y141 | `=AD55` | =AD55 |
| Ligne 141 | Col 26 | Z141 | `=Z55` | =Z55 |
| Ligne 141 | Col 27 | AA141 | `=AA55` | =AA55 |
| Ligne 141 | Col 28 | AB141 | `=X141*SIGN(Y141)*ABS(Y141)^1.821` | =X141*SIGN(Y141)*ABS(Y141)^1.821 |
| Ligne 141 | Col 29 | AC141 | `=1.852*X141*ABS(Y141)^(1.852-1)` | =1.852*X141*ABS(Y141)^(1.852-1) |
| Ligne 141 | Col 30 | AD141 | `=IF(U141>0,
Y141+($I$179*Z141)+(AA141*X213),
Y141+$S$93)` | =IF(U141>0,
Y141+($I$179*Z141)+(AA141*X213),
Y141+$S$93) |
| Ligne 141 | Col 32 | AF141 | `=ABS(AD141)-ABS(Y141)` | =ABS(AD141)-ABS(Y141) |
| Ligne 141 | Col 40 | AN141 | `=ABS(AV55)` | =ABS(AV55) |
| Ligne 141 | Col 44 | AR141 | `= (10.679 * AQ141) / ((AO141/1000)^4.871 * AP141^1.852)` | = (10.679 * AQ141) / ((AO141/1000)^4.871 * AP141^1.852) |
| Ligne 141 | Col 45 | AS141 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57830>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57830> |
| Ligne 141 | Col 46 | AT141 | `=IF(AJ141>0,
        IF(AS141>0, AR141*AS141^1.852,-AR141*ABS(AS141)^1.852),
        IF(AS141>0, AR141*AN141^1.852, -AR141*AN141^1.852))` | =IF(AJ141>0,
        IF(AS141>0, AR141*AS141^1.852,-AR141*ABS(AS141)^1.852),
        IF(AS141>0, AR141*AN141^1.852, -AR141*AN141^1.852)) |
| Ligne 141 | Col 47 | AU141 | `=1.852*AR141*ABS(AS141)^(1.852-1)` | =1.852*AR141*ABS(AS141)^(1.852-1) |
| Ligne 141 | Col 48 | AV141 | `=AS141+$AN$146` | =AS141+$AN$146 |
| Ligne 142 | Col 8 | H142 | `=D56` | =D56 |
| Ligne 142 | Col 9 | I142 | `=I56` | =I56 |
| Ligne 142 | Col 10 | J142 | `=M56` | =M56 |
| Ligne 142 | Col 11 | K142 | `=I142*SIGN(J142)*ABS(J142)^1.821` | =I142*SIGN(J142)*ABS(J142)^1.821 |
| Ligne 142 | Col 12 | L142 | `=1.852*I142*ABS(J142)^(1.852-1)` | =1.852*I142*ABS(J142)^(1.852-1) |
| Ligne 142 | Col 13 | M142 | `=J142+$I$179` | =J142+$I$179 |
| Ligne 142 | Col 21 | U142 | `=P56` | =P56 |
| Ligne 142 | Col 22 | V142 | `=Q56` | =Q56 |
| Ligne 142 | Col 23 | W142 | `=S56` | =S56 |
| Ligne 142 | Col 24 | X142 | `=X56` | =X56 |
| Ligne 142 | Col 25 | Y142 | `=AD56` | =AD56 |
| Ligne 142 | Col 26 | Z142 | `=Z56` | =Z56 |
| Ligne 142 | Col 27 | AA142 | `=AA56` | =AA56 |
| Ligne 142 | Col 28 | AB142 | `=X142*SIGN(Y142)*ABS(Y142)^1.821` | =X142*SIGN(Y142)*ABS(Y142)^1.821 |
| Ligne 142 | Col 29 | AC142 | `=1.852*X142*ABS(Y142)^(1.852-1)` | =1.852*X142*ABS(Y142)^(1.852-1) |
| Ligne 142 | Col 30 | AD142 | `=IF(U142>0,
Y142+($I$179*Z142)+(AA142*X214),
Y142+$S$93)` | =IF(U142>0,
Y142+($I$179*Z142)+(AA142*X214),
Y142+$S$93) |
| Ligne 142 | Col 32 | AF142 | `=ABS(AD142)-ABS(Y142)` | =ABS(AD142)-ABS(Y142) |
| Ligne 142 | Col 40 | AN142 | `=ABS(AV56)` | =ABS(AV56) |
| Ligne 142 | Col 44 | AR142 | `= (10.679 * AQ142) / ((AO142/1000)^4.871 * AP142^1.852)` | = (10.679 * AQ142) / ((AO142/1000)^4.871 * AP142^1.852) |
| Ligne 142 | Col 45 | AS142 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57D10>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57D10> |
| Ligne 142 | Col 46 | AT142 | `=IF(AJ142>0,
IF(AS142>0, AR142*AS142^1.852,-AR142*ABS(AS142)^1.852),
IF(AS142>0, AR142*AN142^1.852, -AR142*AN142^1.852))` | =IF(AJ142>0,
IF(AS142>0, AR142*AS142^1.852,-AR142*ABS(AS142)^1.852),
IF(AS142>0, AR142*AN142^1.852, -AR142*AN142^1.852)) |
| Ligne 142 | Col 47 | AU142 | `=1.852*AR142*ABS(AS142)^(1.852-1)` | =1.852*AR142*ABS(AS142)^(1.852-1) |
| Ligne 142 | Col 48 | AV142 | `=AS142+$AN$146` | =AS142+$AN$146 |
| Ligne 143 | Col 8 | H143 | `=D57` | =D57 |
| Ligne 143 | Col 9 | I143 | `=I57` | =I57 |
| Ligne 143 | Col 10 | J143 | `=M57` | =M57 |
| Ligne 143 | Col 11 | K143 | `=I143*SIGN(J143)*ABS(J143)^1.821` | =I143*SIGN(J143)*ABS(J143)^1.821 |
| Ligne 143 | Col 12 | L143 | `=1.852*I143*ABS(J143)^(1.852-1)` | =1.852*I143*ABS(J143)^(1.852-1) |
| Ligne 143 | Col 13 | M143 | `=J143+$I$179` | =J143+$I$179 |
| Ligne 143 | Col 21 | U143 | `=P57` | =P57 |
| Ligne 143 | Col 22 | V143 | `=Q57` | =Q57 |
| Ligne 143 | Col 23 | W143 | `=S57` | =S57 |
| Ligne 143 | Col 24 | X143 | `=X57` | =X57 |
| Ligne 143 | Col 25 | Y143 | `=AD57` | =AD57 |
| Ligne 143 | Col 26 | Z143 | `=Z57` | =Z57 |
| Ligne 143 | Col 27 | AA143 | `=AA57` | =AA57 |
| Ligne 143 | Col 28 | AB143 | `=X143*SIGN(Y143)*ABS(Y143)^1.821` | =X143*SIGN(Y143)*ABS(Y143)^1.821 |
| Ligne 143 | Col 29 | AC143 | `=1.852*X143*ABS(Y143)^(1.852-1)` | =1.852*X143*ABS(Y143)^(1.852-1) |
| Ligne 143 | Col 30 | AD143 | `=IF(U143>0,
Y143+($I$179*Z143)+(AA143*X215),
Y143+$S$93)` | =IF(U143>0,
Y143+($I$179*Z143)+(AA143*X215),
Y143+$S$93) |
| Ligne 143 | Col 32 | AF143 | `=ABS(AD143)-ABS(Y143)` | =ABS(AD143)-ABS(Y143) |
| Ligne 143 | Col 40 | AN143 | `=ABS(AV57)` | =ABS(AV57) |
| Ligne 143 | Col 44 | AR143 | `= (10.679 * AQ143) / ((AO143/1000)^4.871 * AP143^1.852)` | = (10.679 * AQ143) / ((AO143/1000)^4.871 * AP143^1.852) |
| Ligne 143 | Col 45 | AS143 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57DD0>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57DD0> |
| Ligne 143 | Col 46 | AT143 | `=IF(AJ143>0,
IF(AS143>0, AR143*AS143^1.852,-AR143*ABS(AS143)^1.852),
IF(AS143>0, AR143*AN143^1.852, -AR143*AN143^1.852))` | =IF(AJ143>0,
IF(AS143>0, AR143*AS143^1.852,-AR143*ABS(AS143)^1.852),
IF(AS143>0, AR143*AN143^1.852, -AR143*AN143^1.852)) |
| Ligne 143 | Col 47 | AU143 | `=1.852*AR143*ABS(AS143)^(1.852-1)` | =1.852*AR143*ABS(AS143)^(1.852-1) |
| Ligne 143 | Col 48 | AV143 | `=AS143+$AN$146` | =AS143+$AN$146 |
| Ligne 144 | Col 8 | H144 | `=D58` | =D58 |
| Ligne 144 | Col 9 | I144 | `=I58` | =I58 |
| Ligne 144 | Col 10 | J144 | `=M58` | =M58 |
| Ligne 144 | Col 11 | K144 | `=I144*SIGN(J144)*ABS(J144)^1.821` | =I144*SIGN(J144)*ABS(J144)^1.821 |
| Ligne 144 | Col 12 | L144 | `=1.852*I144*ABS(J144)^(1.852-1)` | =1.852*I144*ABS(J144)^(1.852-1) |
| Ligne 144 | Col 13 | M144 | `=J144+$I$179` | =J144+$I$179 |
| Ligne 144 | Col 21 | U144 | `=P58` | =P58 |
| Ligne 144 | Col 22 | V144 | `=Q58` | =Q58 |
| Ligne 144 | Col 23 | W144 | `=S58` | =S58 |
| Ligne 144 | Col 24 | X144 | `=X58` | =X58 |
| Ligne 144 | Col 25 | Y144 | `=AD58` | =AD58 |
| Ligne 144 | Col 26 | Z144 | `=Z58` | =Z58 |
| Ligne 144 | Col 27 | AA144 | `=AA58` | =AA58 |
| Ligne 144 | Col 28 | AB144 | `=X144*SIGN(Y144)*ABS(Y144)^1.821` | =X144*SIGN(Y144)*ABS(Y144)^1.821 |
| Ligne 144 | Col 29 | AC144 | `=1.852*X144*ABS(Y144)^(1.852-1)` | =1.852*X144*ABS(Y144)^(1.852-1) |
| Ligne 144 | Col 30 | AD144 | `=IF(U144>0,
Y144+($I$179*Z144)+(AA144*X216),
Y144+$S$93)` | =IF(U144>0,
Y144+($I$179*Z144)+(AA144*X216),
Y144+$S$93) |
| Ligne 144 | Col 32 | AF144 | `=ABS(AD144)-ABS(Y144)` | =ABS(AD144)-ABS(Y144) |
| Ligne 144 | Col 40 | AN144 | `=ABS(AV58)` | =ABS(AV58) |
| Ligne 144 | Col 44 | AR144 | `= (10.679 * AQ144) / ((AO144/1000)^4.871 * AP144^1.852)` | = (10.679 * AQ144) / ((AO144/1000)^4.871 * AP144^1.852) |
| Ligne 144 | Col 45 | AS144 | `<openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57E90>` | <openpyxl.worksheet.formula.ArrayFormula object at 0x000001FFDDA57E90> |
| Ligne 144 | Col 46 | AT144 | `=IF(AJ144>0,
IF(AS144>0, AR144*AS144^1.852,-AR144*ABS(AS144)^1.852),
IF(AS144>0, AR144*AN144^1.852, -AR144*AN144^1.852))` | =IF(AJ144>0,
IF(AS144>0, AR144*AS144^1.852,-AR144*ABS(AS144)^1.852),
IF(AS144>0, AR144*AN144^1.852, -AR144*AN144^1.852)) |
| Ligne 144 | Col 47 | AU144 | `=1.852*AR144*ABS(AS144)^(1.852-1)` | =1.852*AR144*ABS(AS144)^(1.852-1) |
| Ligne 144 | Col 48 | AV144 | `=AS144+$AN$146` | =AS144+$AN$146 |
| Ligne 145 | Col 8 | H145 | `=D59` | =D59 |
| Ligne 145 | Col 9 | I145 | `=I59` | =I59 |
| Ligne 145 | Col 10 | J145 | `=M59` | =M59 |
| Ligne 145 | Col 11 | K145 | `=I145*SIGN(J145)*ABS(J145)^1.821` | =I145*SIGN(J145)*ABS(J145)^1.821 |
| Ligne 145 | Col 12 | L145 | `=1.852*I145*ABS(J145)^(1.852-1)` | =1.852*I145*ABS(J145)^(1.852-1) |
| Ligne 145 | Col 13 | M145 | `=J145+$I$179` | =J145+$I$179 |
| Ligne 145 | Col 21 | U145 | `=P59` | =P59 |
| Ligne 145 | Col 22 | V145 | `=Q59` | =Q59 |
| Ligne 145 | Col 23 | W145 | `=S59` | =S59 |
| Ligne 145 | Col 24 | X145 | `=X59` | =X59 |
| Ligne 145 | Col 25 | Y145 | `=AD59` | =AD59 |
| Ligne 145 | Col 26 | Z145 | `=Z59` | =Z59 |
| Ligne 145 | Col 27 | AA145 | `=AA59` | =AA59 |
| Ligne 145 | Col 28 | AB145 | `=X145*SIGN(Y145)*ABS(Y145)^1.821` | =X145*SIGN(Y145)*ABS(Y145)^1.821 |
| Ligne 145 | Col 29 | AC145 | `=1.852*X145*ABS(Y145)^(1.852-1)` | =1.852*X145*ABS(Y145)^(1.852-1) |
| Ligne 145 | Col 30 | AD145 | `=IF(U145>0,
Y145+($I$179*Z145)+(AA145*X217),
Y145+$S$93)` | =IF(U145>0,
Y145+($I$179*Z145)+(AA145*X217),
Y145+$S$93) |
| Ligne 145 | Col 32 | AF145 | `=ABS(AD145)-ABS(Y145)` | =ABS(AD145)-ABS(Y145) |
| Ligne 145 | Col 36 | AJ145 | `=COUNTIF(AJ108:AJ144,">0")` | =COUNTIF(AJ108:AJ144,">0") |
| Ligne 145 | Col 46 | AT145 | `=SUM(AT108:AT144)` | =SUM(AT108:AT144) |
| Ligne 145 | Col 47 | AU145 | `=SUM(AU108:AU144)` | =SUM(AU108:AU144) |
| Ligne 146 | Col 8 | H146 | `=D60` | =D60 |
| Ligne 146 | Col 9 | I146 | `=I60` | =I60 |
| Ligne 146 | Col 10 | J146 | `=M60` | =M60 |
| Ligne 146 | Col 11 | K146 | `=I146*SIGN(J146)*ABS(J146)^1.821` | =I146*SIGN(J146)*ABS(J146)^1.821 |
| Ligne 146 | Col 12 | L146 | `=1.852*I146*ABS(J146)^(1.852-1)` | =1.852*I146*ABS(J146)^(1.852-1) |
| Ligne 146 | Col 13 | M146 | `=J146+$I$179` | =J146+$I$179 |
| Ligne 146 | Col 21 | U146 | `=P60` | =P60 |
| Ligne 146 | Col 22 | V146 | `=Q60` | =Q60 |
| Ligne 146 | Col 23 | W146 | `=S60` | =S60 |
| Ligne 146 | Col 24 | X146 | `=X60` | =X60 |
| Ligne 146 | Col 25 | Y146 | `=AD60` | =AD60 |
| Ligne 146 | Col 26 | Z146 | `=Z60` | =Z60 |
| Ligne 146 | Col 27 | AA146 | `=AA60` | =AA60 |
| Ligne 146 | Col 28 | AB146 | `=X146*SIGN(Y146)*ABS(Y146)^1.821` | =X146*SIGN(Y146)*ABS(Y146)^1.821 |
| Ligne 146 | Col 29 | AC146 | `=1.852*X146*ABS(Y146)^(1.852-1)` | =1.852*X146*ABS(Y146)^(1.852-1) |
| Ligne 146 | Col 30 | AD146 | `=IF(U146>0,
Y146+($I$179*Z146)+(AA146*X218),
Y146+$S$93)` | =IF(U146>0,
Y146+($I$179*Z146)+(AA146*X218),
Y146+$S$93) |
| Ligne 146 | Col 32 | AF146 | `=ABS(AD146)-ABS(Y146)` | =ABS(AD146)-ABS(Y146) |
| Ligne 146 | Col 40 | AN146 | `=ABS(AT145/(1.852*AU145))` | =ABS(AT145/(1.852*AU145)) |
| Ligne 147 | Col 8 | H147 | `=D61` | =D61 |
| Ligne 147 | Col 9 | I147 | `=I61` | =I61 |
| Ligne 147 | Col 10 | J147 | `=M61` | =M61 |
| Ligne 147 | Col 11 | K147 | `=I147*SIGN(J147)*ABS(J147)^1.821` | =I147*SIGN(J147)*ABS(J147)^1.821 |
| Ligne 147 | Col 12 | L147 | `=1.852*I147*ABS(J147)^(1.852-1)` | =1.852*I147*ABS(J147)^(1.852-1) |
| Ligne 147 | Col 13 | M147 | `=J147+$I$179` | =J147+$I$179 |
| Ligne 147 | Col 21 | U147 | `=P61` | =P61 |
| Ligne 147 | Col 22 | V147 | `=Q61` | =Q61 |
| Ligne 147 | Col 23 | W147 | `=S61` | =S61 |
| Ligne 147 | Col 24 | X147 | `=X61` | =X61 |
| Ligne 147 | Col 25 | Y147 | `=AD61` | =AD61 |
| Ligne 147 | Col 26 | Z147 | `=Z61` | =Z61 |
| Ligne 147 | Col 27 | AA147 | `=AA61` | =AA61 |
| Ligne 147 | Col 28 | AB147 | `=X147*SIGN(Y147)*ABS(Y147)^1.821` | =X147*SIGN(Y147)*ABS(Y147)^1.821 |
| Ligne 147 | Col 29 | AC147 | `=1.852*X147*ABS(Y147)^(1.852-1)` | =1.852*X147*ABS(Y147)^(1.852-1) |
| Ligne 147 | Col 30 | AD147 | `=IF(U147>0,
Y147+($I$179*Z147)+(AA147*X219),
Y147+$S$93)` | =IF(U147>0,
Y147+($I$179*Z147)+(AA147*X219),
Y147+$S$93) |
| Ligne 147 | Col 32 | AF147 | `=ABS(AD147)-ABS(Y147)` | =ABS(AD147)-ABS(Y147) |
| Ligne 147 | Col 40 | AN147 | `=AN60-AN146` | =AN60-AN146 |
| Ligne 148 | Col 8 | H148 | `=D62` | =D62 |
| Ligne 148 | Col 9 | I148 | `=I62` | =I62 |
| Ligne 148 | Col 10 | J148 | `=M62` | =M62 |
| Ligne 148 | Col 11 | K148 | `=I148*SIGN(J148)*ABS(J148)^1.821` | =I148*SIGN(J148)*ABS(J148)^1.821 |
| Ligne 148 | Col 12 | L148 | `=1.852*I148*ABS(J148)^(1.852-1)` | =1.852*I148*ABS(J148)^(1.852-1) |
| Ligne 148 | Col 13 | M148 | `=J148+$I$179` | =J148+$I$179 |
| Ligne 148 | Col 21 | U148 | `=P62` | =P62 |
| Ligne 148 | Col 22 | V148 | `=Q62` | =Q62 |
| Ligne 148 | Col 23 | W148 | `=S62` | =S62 |
| Ligne 148 | Col 24 | X148 | `=X62` | =X62 |
| Ligne 148 | Col 25 | Y148 | `=AD62` | =AD62 |
| Ligne 148 | Col 26 | Z148 | `=Z62` | =Z62 |
| Ligne 148 | Col 27 | AA148 | `=AA62` | =AA62 |
| Ligne 148 | Col 28 | AB148 | `=X148*SIGN(Y148)*ABS(Y148)^1.821` | =X148*SIGN(Y148)*ABS(Y148)^1.821 |
| Ligne 148 | Col 29 | AC148 | `=1.852*X148*ABS(Y148)^(1.852-1)` | =1.852*X148*ABS(Y148)^(1.852-1) |
| Ligne 148 | Col 30 | AD148 | `=IF(U148>0,
Y148+($I$179*Z148)+(AA148*X220),
Y148+$S$93)` | =IF(U148>0,
Y148+($I$179*Z148)+(AA148*X220),
Y148+$S$93) |
| Ligne 148 | Col 32 | AF148 | `=ABS(AD148)-ABS(Y148)` | =ABS(AD148)-ABS(Y148) |
| Ligne 148 | Col 40 | AN148 | `=IF(AN147>0, "L'agorithme est fonctionel","L'algorithme n'est pas fonctionnel; maille à revérifier")` | =IF(AN147>0, "L'agorithme est fonctionel","L'algorithme n'est pas fonctionnel; maille à revérifier") |
| Ligne 149 | Col 8 | H149 | `=D63` | =D63 |
| Ligne 149 | Col 9 | I149 | `=I63` | =I63 |
| Ligne 149 | Col 10 | J149 | `=M63` | =M63 |
| Ligne 149 | Col 11 | K149 | `=I149*SIGN(J149)*ABS(J149)^1.821` | =I149*SIGN(J149)*ABS(J149)^1.821 |
| Ligne 149 | Col 12 | L149 | `=1.852*I149*ABS(J149)^(1.852-1)` | =1.852*I149*ABS(J149)^(1.852-1) |
| Ligne 149 | Col 13 | M149 | `=J149+$I$179` | =J149+$I$179 |
| Ligne 149 | Col 21 | U149 | `=P63` | =P63 |
| Ligne 149 | Col 22 | V149 | `=Q63` | =Q63 |
| Ligne 149 | Col 23 | W149 | `=S63` | =S63 |
| Ligne 149 | Col 24 | X149 | `=X63` | =X63 |
| Ligne 149 | Col 25 | Y149 | `=AD63` | =AD63 |
| Ligne 149 | Col 26 | Z149 | `=Z63` | =Z63 |
| Ligne 149 | Col 27 | AA149 | `=AA63` | =AA63 |
| Ligne 149 | Col 28 | AB149 | `=X149*SIGN(Y149)*ABS(Y149)^1.821` | =X149*SIGN(Y149)*ABS(Y149)^1.821 |
| Ligne 149 | Col 29 | AC149 | `=1.852*X149*ABS(Y149)^(1.852-1)` | =1.852*X149*ABS(Y149)^(1.852-1) |
| Ligne 149 | Col 30 | AD149 | `=IF(U149>0,
Y149+($I$179*Z149)+(AA149*X221),
Y149+$S$93)` | =IF(U149>0,
Y149+($I$179*Z149)+(AA149*X221),
Y149+$S$93) |
| Ligne 149 | Col 32 | AF149 | `=ABS(AD149)-ABS(Y149)` | =ABS(AD149)-ABS(Y149) |
| Ligne 150 | Col 8 | H150 | `=D64` | =D64 |
| Ligne 150 | Col 9 | I150 | `=I64` | =I64 |
| Ligne 150 | Col 10 | J150 | `=M64` | =M64 |
| Ligne 150 | Col 11 | K150 | `=I150*SIGN(J150)*ABS(J150)^1.821` | =I150*SIGN(J150)*ABS(J150)^1.821 |
| Ligne 150 | Col 12 | L150 | `=1.852*I150*ABS(J150)^(1.852-1)` | =1.852*I150*ABS(J150)^(1.852-1) |
| Ligne 150 | Col 13 | M150 | `=J150+$I$179` | =J150+$I$179 |
| Ligne 150 | Col 21 | U150 | `=P64` | =P64 |
| Ligne 150 | Col 22 | V150 | `=Q64` | =Q64 |
| Ligne 150 | Col 23 | W150 | `=S64` | =S64 |
| Ligne 150 | Col 24 | X150 | `=X64` | =X64 |
| Ligne 150 | Col 25 | Y150 | `=AD64` | =AD64 |
| Ligne 150 | Col 26 | Z150 | `=Z64` | =Z64 |
| Ligne 150 | Col 27 | AA150 | `=AA64` | =AA64 |
| Ligne 150 | Col 28 | AB150 | `=X150*SIGN(Y150)*ABS(Y150)^1.821` | =X150*SIGN(Y150)*ABS(Y150)^1.821 |
| Ligne 150 | Col 29 | AC150 | `=1.852*X150*ABS(Y150)^(1.852-1)` | =1.852*X150*ABS(Y150)^(1.852-1) |
| Ligne 150 | Col 30 | AD150 | `=IF(U150>0,
Y150+($I$179*Z150)+(AA150*X222),
Y150+$S$93)` | =IF(U150>0,
Y150+($I$179*Z150)+(AA150*X222),
Y150+$S$93) |
| Ligne 150 | Col 32 | AF150 | `=ABS(AD150)-ABS(Y150)` | =ABS(AD150)-ABS(Y150) |
| Ligne 151 | Col 8 | H151 | `=D65` | =D65 |
| Ligne 151 | Col 9 | I151 | `=I65` | =I65 |
| Ligne 151 | Col 10 | J151 | `=M65` | =M65 |
| Ligne 151 | Col 11 | K151 | `=I151*SIGN(J151)*ABS(J151)^1.821` | =I151*SIGN(J151)*ABS(J151)^1.821 |
| Ligne 151 | Col 12 | L151 | `=1.852*I151*ABS(J151)^(1.852-1)` | =1.852*I151*ABS(J151)^(1.852-1) |
| Ligne 151 | Col 13 | M151 | `=J151+$I$179` | =J151+$I$179 |
| Ligne 151 | Col 21 | U151 | `=P65` | =P65 |
| Ligne 151 | Col 22 | V151 | `=Q65` | =Q65 |
| Ligne 151 | Col 23 | W151 | `=S65` | =S65 |
| Ligne 151 | Col 24 | X151 | `=X65` | =X65 |
| Ligne 151 | Col 25 | Y151 | `=AD65` | =AD65 |
| Ligne 151 | Col 26 | Z151 | `=Z65` | =Z65 |
| Ligne 151 | Col 27 | AA151 | `=AA65` | =AA65 |
| Ligne 151 | Col 28 | AB151 | `=X151*SIGN(Y151)*ABS(Y151)^1.821` | =X151*SIGN(Y151)*ABS(Y151)^1.821 |
| Ligne 151 | Col 29 | AC151 | `=1.852*X151*ABS(Y151)^(1.852-1)` | =1.852*X151*ABS(Y151)^(1.852-1) |
| Ligne 151 | Col 30 | AD151 | `=IF(U151>0,
Y151+($I$179*Z151)+(AA151*X223),
Y151+$S$93)` | =IF(U151>0,
Y151+($I$179*Z151)+(AA151*X223),
Y151+$S$93) |
| Ligne 151 | Col 32 | AF151 | `=ABS(AD151)-ABS(Y151)` | =ABS(AD151)-ABS(Y151) |
| Ligne 152 | Col 8 | H152 | `=D66` | =D66 |
| Ligne 152 | Col 9 | I152 | `=I66` | =I66 |
| Ligne 152 | Col 10 | J152 | `=M66` | =M66 |
| Ligne 152 | Col 11 | K152 | `=I152*SIGN(J152)*ABS(J152)^1.821` | =I152*SIGN(J152)*ABS(J152)^1.821 |
| Ligne 152 | Col 12 | L152 | `=1.852*I152*ABS(J152)^(1.852-1)` | =1.852*I152*ABS(J152)^(1.852-1) |
| Ligne 152 | Col 13 | M152 | `=J152+$I$179` | =J152+$I$179 |
| Ligne 152 | Col 21 | U152 | `=P66` | =P66 |
| Ligne 152 | Col 22 | V152 | `=Q66` | =Q66 |
| Ligne 152 | Col 23 | W152 | `=S66` | =S66 |
| Ligne 152 | Col 24 | X152 | `=X66` | =X66 |
| Ligne 152 | Col 25 | Y152 | `=AD66` | =AD66 |
| Ligne 152 | Col 26 | Z152 | `=Z66` | =Z66 |
| Ligne 152 | Col 27 | AA152 | `=AA66` | =AA66 |
| Ligne 152 | Col 28 | AB152 | `=X152*SIGN(Y152)*ABS(Y152)^1.821` | =X152*SIGN(Y152)*ABS(Y152)^1.821 |
| Ligne 152 | Col 29 | AC152 | `=1.852*X152*ABS(Y152)^(1.852-1)` | =1.852*X152*ABS(Y152)^(1.852-1) |
| Ligne 152 | Col 30 | AD152 | `=IF(U152>0,
Y152+($I$179*Z152)+(AA152*X224),
Y152+$S$93)` | =IF(U152>0,
Y152+($I$179*Z152)+(AA152*X224),
Y152+$S$93) |
| Ligne 152 | Col 32 | AF152 | `=ABS(AD152)-ABS(Y152)` | =ABS(AD152)-ABS(Y152) |
| Ligne 153 | Col 8 | H153 | `=D67` | =D67 |
| Ligne 153 | Col 9 | I153 | `=I67` | =I67 |
| Ligne 153 | Col 10 | J153 | `=M67` | =M67 |
| Ligne 153 | Col 11 | K153 | `=I153*SIGN(J153)*ABS(J153)^1.821` | =I153*SIGN(J153)*ABS(J153)^1.821 |
| Ligne 153 | Col 12 | L153 | `=1.852*I153*ABS(J153)^(1.852-1)` | =1.852*I153*ABS(J153)^(1.852-1) |
| Ligne 153 | Col 13 | M153 | `=J153+$I$179` | =J153+$I$179 |
| Ligne 153 | Col 21 | U153 | `=P67` | =P67 |
| Ligne 153 | Col 22 | V153 | `=Q67` | =Q67 |
| Ligne 153 | Col 23 | W153 | `=S67` | =S67 |
| Ligne 153 | Col 24 | X153 | `=X67` | =X67 |
| Ligne 153 | Col 25 | Y153 | `=AD67` | =AD67 |
| Ligne 153 | Col 26 | Z153 | `=Z67` | =Z67 |
| Ligne 153 | Col 27 | AA153 | `=AA67` | =AA67 |
| Ligne 153 | Col 28 | AB153 | `=X153*SIGN(Y153)*ABS(Y153)^1.821` | =X153*SIGN(Y153)*ABS(Y153)^1.821 |
| Ligne 153 | Col 29 | AC153 | `=1.852*X153*ABS(Y153)^(1.852-1)` | =1.852*X153*ABS(Y153)^(1.852-1) |
| Ligne 153 | Col 30 | AD153 | `=IF(U153>0,
Y153+($I$179*Z153)+(AA153*X225),
Y153+$S$93)` | =IF(U153>0,
Y153+($I$179*Z153)+(AA153*X225),
Y153+$S$93) |
| Ligne 153 | Col 32 | AF153 | `=ABS(AD153)-ABS(Y153)` | =ABS(AD153)-ABS(Y153) |
| Ligne 154 | Col 8 | H154 | `=D68` | =D68 |
| Ligne 154 | Col 9 | I154 | `=I68` | =I68 |
| Ligne 154 | Col 10 | J154 | `=M68` | =M68 |
| Ligne 154 | Col 11 | K154 | `=I154*SIGN(J154)*ABS(J154)^1.821` | =I154*SIGN(J154)*ABS(J154)^1.821 |
| Ligne 154 | Col 12 | L154 | `=1.852*I154*ABS(J154)^(1.852-1)` | =1.852*I154*ABS(J154)^(1.852-1) |
| Ligne 154 | Col 13 | M154 | `=J154+$I$179` | =J154+$I$179 |
| Ligne 154 | Col 21 | U154 | `=P68` | =P68 |
| Ligne 154 | Col 22 | V154 | `=Q68` | =Q68 |
| Ligne 154 | Col 23 | W154 | `=S68` | =S68 |
| Ligne 154 | Col 24 | X154 | `=X68` | =X68 |
| Ligne 154 | Col 25 | Y154 | `=AD68` | =AD68 |
| Ligne 154 | Col 26 | Z154 | `=Z68` | =Z68 |
| Ligne 154 | Col 27 | AA154 | `=AA68` | =AA68 |
| Ligne 154 | Col 28 | AB154 | `=X154*SIGN(Y154)*ABS(Y154)^1.821` | =X154*SIGN(Y154)*ABS(Y154)^1.821 |
| Ligne 154 | Col 29 | AC154 | `=1.852*X154*ABS(Y154)^(1.852-1)` | =1.852*X154*ABS(Y154)^(1.852-1) |
| Ligne 154 | Col 30 | AD154 | `=IF(U154>0,
Y154+($I$179*Z154)+(AA154*X226),
Y154+$S$93)` | =IF(U154>0,
Y154+($I$179*Z154)+(AA154*X226),
Y154+$S$93) |
| Ligne 154 | Col 32 | AF154 | `=ABS(AD154)-ABS(Y154)` | =ABS(AD154)-ABS(Y154) |
| Ligne 155 | Col 8 | H155 | `=D69` | =D69 |
| Ligne 155 | Col 9 | I155 | `=I69` | =I69 |
| Ligne 155 | Col 10 | J155 | `=M69` | =M69 |
| Ligne 155 | Col 11 | K155 | `=I155*SIGN(J155)*ABS(J155)^1.821` | =I155*SIGN(J155)*ABS(J155)^1.821 |
| Ligne 155 | Col 12 | L155 | `=1.852*I155*ABS(J155)^(1.852-1)` | =1.852*I155*ABS(J155)^(1.852-1) |
| Ligne 155 | Col 13 | M155 | `=J155+$I$179` | =J155+$I$179 |
| Ligne 155 | Col 21 | U155 | `=P69` | =P69 |
| Ligne 155 | Col 22 | V155 | `=Q69` | =Q69 |
| Ligne 155 | Col 23 | W155 | `=S69` | =S69 |
| Ligne 155 | Col 24 | X155 | `=X69` | =X69 |
| Ligne 155 | Col 25 | Y155 | `=AD69` | =AD69 |
| Ligne 155 | Col 26 | Z155 | `=Z69` | =Z69 |
| Ligne 155 | Col 27 | AA155 | `=AA69` | =AA69 |
| Ligne 155 | Col 28 | AB155 | `=X155*SIGN(Y155)*ABS(Y155)^1.821` | =X155*SIGN(Y155)*ABS(Y155)^1.821 |
| Ligne 155 | Col 29 | AC155 | `=1.852*X155*ABS(Y155)^(1.852-1)` | =1.852*X155*ABS(Y155)^(1.852-1) |
| Ligne 155 | Col 30 | AD155 | `=IF(U155>0,
Y155+($I$179*Z155)+(AA155*X227),
Y155+$S$93)` | =IF(U155>0,
Y155+($I$179*Z155)+(AA155*X227),
Y155+$S$93) |
| Ligne 155 | Col 32 | AF155 | `=ABS(AD155)-ABS(Y155)` | =ABS(AD155)-ABS(Y155) |
| Ligne 156 | Col 8 | H156 | `=D70` | =D70 |
| Ligne 156 | Col 9 | I156 | `=I70` | =I70 |
| Ligne 156 | Col 10 | J156 | `=M70` | =M70 |
| Ligne 156 | Col 11 | K156 | `=I156*SIGN(J156)*ABS(J156)^1.821` | =I156*SIGN(J156)*ABS(J156)^1.821 |
| Ligne 156 | Col 12 | L156 | `=1.852*I156*ABS(J156)^(1.852-1)` | =1.852*I156*ABS(J156)^(1.852-1) |
| Ligne 156 | Col 13 | M156 | `=J156+$I$179` | =J156+$I$179 |
| Ligne 156 | Col 21 | U156 | `=P70` | =P70 |
| Ligne 156 | Col 22 | V156 | `=Q70` | =Q70 |
| Ligne 156 | Col 23 | W156 | `=S70` | =S70 |
| Ligne 156 | Col 24 | X156 | `=X70` | =X70 |
| Ligne 156 | Col 25 | Y156 | `=AD70` | =AD70 |
| Ligne 156 | Col 26 | Z156 | `=Z70` | =Z70 |
| Ligne 156 | Col 27 | AA156 | `=AA70` | =AA70 |
| Ligne 156 | Col 28 | AB156 | `=X156*SIGN(Y156)*ABS(Y156)^1.821` | =X156*SIGN(Y156)*ABS(Y156)^1.821 |
| Ligne 156 | Col 29 | AC156 | `=1.852*X156*ABS(Y156)^(1.852-1)` | =1.852*X156*ABS(Y156)^(1.852-1) |
| Ligne 156 | Col 30 | AD156 | `=IF(U156>0,
Y156+($I$179*Z156)+(AA156*X228),
Y156+$S$93)` | =IF(U156>0,
Y156+($I$179*Z156)+(AA156*X228),
Y156+$S$93) |
| Ligne 156 | Col 32 | AF156 | `=ABS(AD156)-ABS(Y156)` | =ABS(AD156)-ABS(Y156) |
| Ligne 157 | Col 8 | H157 | `=D71` | =D71 |
| Ligne 157 | Col 9 | I157 | `=I71` | =I71 |
| Ligne 157 | Col 10 | J157 | `=M71` | =M71 |
| Ligne 157 | Col 11 | K157 | `=I157*SIGN(J157)*ABS(J157)^1.821` | =I157*SIGN(J157)*ABS(J157)^1.821 |
| Ligne 157 | Col 12 | L157 | `=1.852*I157*ABS(J157)^(1.852-1)` | =1.852*I157*ABS(J157)^(1.852-1) |
| Ligne 157 | Col 13 | M157 | `=J157+$I$179` | =J157+$I$179 |
| Ligne 157 | Col 21 | U157 | `=P71` | =P71 |
| Ligne 157 | Col 22 | V157 | `=Q71` | =Q71 |
| Ligne 157 | Col 23 | W157 | `=S71` | =S71 |
| Ligne 157 | Col 24 | X157 | `=X71` | =X71 |
| Ligne 157 | Col 25 | Y157 | `=AD71` | =AD71 |
| Ligne 157 | Col 26 | Z157 | `=Z71` | =Z71 |
| Ligne 157 | Col 27 | AA157 | `=AA71` | =AA71 |
| Ligne 157 | Col 28 | AB157 | `=X157*SIGN(Y157)*ABS(Y157)^1.821` | =X157*SIGN(Y157)*ABS(Y157)^1.821 |
| Ligne 157 | Col 29 | AC157 | `=1.852*X157*ABS(Y157)^(1.852-1)` | =1.852*X157*ABS(Y157)^(1.852-1) |
| Ligne 157 | Col 30 | AD157 | `=IF(U157>0,
Y157+($I$179*Z157)+(AA157*X229),
Y157+$S$93)` | =IF(U157>0,
Y157+($I$179*Z157)+(AA157*X229),
Y157+$S$93) |
| Ligne 157 | Col 32 | AF157 | `=ABS(AD157)-ABS(Y157)` | =ABS(AD157)-ABS(Y157) |
| Ligne 158 | Col 8 | H158 | `=D72` | =D72 |
| Ligne 158 | Col 9 | I158 | `=I72` | =I72 |
| Ligne 158 | Col 10 | J158 | `=M72` | =M72 |
| Ligne 158 | Col 11 | K158 | `=I158*SIGN(J158)*ABS(J158)^1.821` | =I158*SIGN(J158)*ABS(J158)^1.821 |
| Ligne 158 | Col 12 | L158 | `=1.852*I158*ABS(J158)^(1.852-1)` | =1.852*I158*ABS(J158)^(1.852-1) |
| Ligne 158 | Col 13 | M158 | `=J158+$I$179` | =J158+$I$179 |
| Ligne 158 | Col 21 | U158 | `=P72` | =P72 |
| Ligne 158 | Col 22 | V158 | `=Q72` | =Q72 |
| Ligne 158 | Col 23 | W158 | `=S72` | =S72 |
| Ligne 158 | Col 24 | X158 | `=X72` | =X72 |
| Ligne 158 | Col 25 | Y158 | `=AD72` | =AD72 |
| Ligne 158 | Col 26 | Z158 | `=Z72` | =Z72 |
| Ligne 158 | Col 27 | AA158 | `=AA72` | =AA72 |
| Ligne 158 | Col 28 | AB158 | `=X158*SIGN(Y158)*ABS(Y158)^1.821` | =X158*SIGN(Y158)*ABS(Y158)^1.821 |
| Ligne 158 | Col 29 | AC158 | `=1.852*X158*ABS(Y158)^(1.852-1)` | =1.852*X158*ABS(Y158)^(1.852-1) |
| Ligne 158 | Col 30 | AD158 | `=IF(U158>0,
Y158+($I$179*Z158)+(AA158*X230),
Y158+$S$93)` | =IF(U158>0,
Y158+($I$179*Z158)+(AA158*X230),
Y158+$S$93) |
| Ligne 158 | Col 32 | AF158 | `=ABS(AD158)-ABS(Y158)` | =ABS(AD158)-ABS(Y158) |
| Ligne 159 | Col 8 | H159 | `=D73` | =D73 |
| Ligne 159 | Col 9 | I159 | `=I73` | =I73 |
| Ligne 159 | Col 10 | J159 | `=M73` | =M73 |
| Ligne 159 | Col 11 | K159 | `=I159*SIGN(J159)*ABS(J159)^1.821` | =I159*SIGN(J159)*ABS(J159)^1.821 |
| Ligne 159 | Col 12 | L159 | `=1.852*I159*ABS(J159)^(1.852-1)` | =1.852*I159*ABS(J159)^(1.852-1) |
| Ligne 159 | Col 13 | M159 | `=J159+$I$179` | =J159+$I$179 |
| Ligne 159 | Col 21 | U159 | `=P73` | =P73 |
| Ligne 159 | Col 22 | V159 | `=Q73` | =Q73 |
| Ligne 159 | Col 23 | W159 | `=S73` | =S73 |
| Ligne 159 | Col 24 | X159 | `=X73` | =X73 |
| Ligne 159 | Col 25 | Y159 | `=AD73` | =AD73 |
| Ligne 159 | Col 26 | Z159 | `=Z73` | =Z73 |
| Ligne 159 | Col 27 | AA159 | `=AA73` | =AA73 |
| Ligne 159 | Col 28 | AB159 | `=X159*SIGN(Y159)*ABS(Y159)^1.821` | =X159*SIGN(Y159)*ABS(Y159)^1.821 |
| Ligne 159 | Col 29 | AC159 | `=1.852*X159*ABS(Y159)^(1.852-1)` | =1.852*X159*ABS(Y159)^(1.852-1) |
| Ligne 159 | Col 30 | AD159 | `=IF(U159>0,
Y159+($I$179*Z159)+(AA159*X231),
Y159+$S$93)` | =IF(U159>0,
Y159+($I$179*Z159)+(AA159*X231),
Y159+$S$93) |
| Ligne 159 | Col 32 | AF159 | `=ABS(AD159)-ABS(Y159)` | =ABS(AD159)-ABS(Y159) |
| Ligne 160 | Col 8 | H160 | `=D74` | =D74 |
| Ligne 160 | Col 9 | I160 | `=I74` | =I74 |
| Ligne 160 | Col 10 | J160 | `=M74` | =M74 |
| Ligne 160 | Col 11 | K160 | `=I160*SIGN(J160)*ABS(J160)^1.821` | =I160*SIGN(J160)*ABS(J160)^1.821 |
| Ligne 160 | Col 12 | L160 | `=1.852*I160*ABS(J160)^(1.852-1)` | =1.852*I160*ABS(J160)^(1.852-1) |
| Ligne 160 | Col 13 | M160 | `=J160+$I$179` | =J160+$I$179 |
| Ligne 160 | Col 21 | U160 | `=P74` | =P74 |
| Ligne 160 | Col 22 | V160 | `=Q74` | =Q74 |
| Ligne 160 | Col 23 | W160 | `=S74` | =S74 |
| Ligne 160 | Col 24 | X160 | `=X74` | =X74 |
| Ligne 160 | Col 25 | Y160 | `=AD74` | =AD74 |
| Ligne 160 | Col 26 | Z160 | `=Z74` | =Z74 |
| Ligne 160 | Col 27 | AA160 | `=AA74` | =AA74 |
| Ligne 160 | Col 28 | AB160 | `=X160*SIGN(Y160)*ABS(Y160)^1.821` | =X160*SIGN(Y160)*ABS(Y160)^1.821 |
| Ligne 160 | Col 29 | AC160 | `=1.852*X160*ABS(Y160)^(1.852-1)` | =1.852*X160*ABS(Y160)^(1.852-1) |
| Ligne 160 | Col 30 | AD160 | `=IF(U160>0,
Y160+($I$179*Z160)+(AA160*X232),
Y160+$S$93)` | =IF(U160>0,
Y160+($I$179*Z160)+(AA160*X232),
Y160+$S$93) |
| Ligne 160 | Col 32 | AF160 | `=ABS(AD160)-ABS(Y160)` | =ABS(AD160)-ABS(Y160) |
| Ligne 161 | Col 8 | H161 | `=D75` | =D75 |
| Ligne 161 | Col 9 | I161 | `=I75` | =I75 |
| Ligne 161 | Col 10 | J161 | `=M75` | =M75 |
| Ligne 161 | Col 11 | K161 | `=I161*SIGN(J161)*ABS(J161)^1.821` | =I161*SIGN(J161)*ABS(J161)^1.821 |
| Ligne 161 | Col 12 | L161 | `=1.852*I161*ABS(J161)^(1.852-1)` | =1.852*I161*ABS(J161)^(1.852-1) |
| Ligne 161 | Col 13 | M161 | `=J161+$I$179` | =J161+$I$179 |
| Ligne 161 | Col 21 | U161 | `=P75` | =P75 |
| Ligne 161 | Col 22 | V161 | `=Q75` | =Q75 |
| Ligne 161 | Col 23 | W161 | `=S75` | =S75 |
| Ligne 161 | Col 24 | X161 | `=X75` | =X75 |
| Ligne 161 | Col 25 | Y161 | `=AD75` | =AD75 |
| Ligne 161 | Col 26 | Z161 | `=Z75` | =Z75 |
| Ligne 161 | Col 27 | AA161 | `=AA75` | =AA75 |
| Ligne 161 | Col 28 | AB161 | `=X161*SIGN(Y161)*ABS(Y161)^1.821` | =X161*SIGN(Y161)*ABS(Y161)^1.821 |
| Ligne 161 | Col 29 | AC161 | `=1.852*X161*ABS(Y161)^(1.852-1)` | =1.852*X161*ABS(Y161)^(1.852-1) |
| Ligne 161 | Col 30 | AD161 | `=IF(U161>0,
Y161+($I$179*Z161)+(AA161*X233),
Y161+$S$93)` | =IF(U161>0,
Y161+($I$179*Z161)+(AA161*X233),
Y161+$S$93) |
| Ligne 161 | Col 32 | AF161 | `=ABS(AD161)-ABS(Y161)` | =ABS(AD161)-ABS(Y161) |
| Ligne 162 | Col 8 | H162 | `=D76` | =D76 |
| Ligne 162 | Col 9 | I162 | `=I76` | =I76 |
| Ligne 162 | Col 10 | J162 | `=M76` | =M76 |
| Ligne 162 | Col 11 | K162 | `=I162*SIGN(J162)*ABS(J162)^1.821` | =I162*SIGN(J162)*ABS(J162)^1.821 |
| Ligne 162 | Col 12 | L162 | `=1.852*I162*ABS(J162)^(1.852-1)` | =1.852*I162*ABS(J162)^(1.852-1) |
| Ligne 162 | Col 13 | M162 | `=J162+$I$179` | =J162+$I$179 |
| Ligne 162 | Col 21 | U162 | `=P76` | =P76 |
| Ligne 162 | Col 22 | V162 | `=Q76` | =Q76 |
| Ligne 162 | Col 23 | W162 | `=S76` | =S76 |
| Ligne 162 | Col 24 | X162 | `=X76` | =X76 |
| Ligne 162 | Col 25 | Y162 | `=AD76` | =AD76 |
| Ligne 162 | Col 26 | Z162 | `=Z76` | =Z76 |
| Ligne 162 | Col 27 | AA162 | `=AA76` | =AA76 |
| Ligne 162 | Col 28 | AB162 | `=X162*SIGN(Y162)*ABS(Y162)^1.821` | =X162*SIGN(Y162)*ABS(Y162)^1.821 |
| Ligne 162 | Col 29 | AC162 | `=1.852*X162*ABS(Y162)^(1.852-1)` | =1.852*X162*ABS(Y162)^(1.852-1) |
| Ligne 162 | Col 30 | AD162 | `=IF(U162>0,
Y162+($I$179*Z162)+(AA162*X234),
Y162+$S$93)` | =IF(U162>0,
Y162+($I$179*Z162)+(AA162*X234),
Y162+$S$93) |
| Ligne 162 | Col 32 | AF162 | `=ABS(AD162)-ABS(Y162)` | =ABS(AD162)-ABS(Y162) |
| Ligne 163 | Col 8 | H163 | `=D77` | =D77 |
| Ligne 163 | Col 9 | I163 | `=I77` | =I77 |
| Ligne 163 | Col 10 | J163 | `=M77` | =M77 |
| Ligne 163 | Col 11 | K163 | `=I163*SIGN(J163)*ABS(J163)^1.821` | =I163*SIGN(J163)*ABS(J163)^1.821 |
| Ligne 163 | Col 12 | L163 | `=1.852*I163*ABS(J163)^(1.852-1)` | =1.852*I163*ABS(J163)^(1.852-1) |
| Ligne 163 | Col 13 | M163 | `=J163+$I$179` | =J163+$I$179 |
| Ligne 163 | Col 21 | U163 | `=P77` | =P77 |
| Ligne 163 | Col 22 | V163 | `=Q77` | =Q77 |
| Ligne 163 | Col 23 | W163 | `=S77` | =S77 |
| Ligne 163 | Col 24 | X163 | `=X77` | =X77 |
| Ligne 163 | Col 25 | Y163 | `=AD77` | =AD77 |
| Ligne 163 | Col 26 | Z163 | `=Z77` | =Z77 |
| Ligne 163 | Col 27 | AA163 | `=AA77` | =AA77 |
| Ligne 163 | Col 28 | AB163 | `=X163*SIGN(Y163)*ABS(Y163)^1.821` | =X163*SIGN(Y163)*ABS(Y163)^1.821 |
| Ligne 163 | Col 29 | AC163 | `=1.852*X163*ABS(Y163)^(1.852-1)` | =1.852*X163*ABS(Y163)^(1.852-1) |
| Ligne 163 | Col 30 | AD163 | `=IF(U163>0,
Y163+($I$179*Z163)+(AA163*X235),
Y163+$S$93)` | =IF(U163>0,
Y163+($I$179*Z163)+(AA163*X235),
Y163+$S$93) |
| Ligne 163 | Col 32 | AF163 | `=ABS(AD163)-ABS(Y163)` | =ABS(AD163)-ABS(Y163) |
| Ligne 164 | Col 8 | H164 | `=D78` | =D78 |
| Ligne 164 | Col 9 | I164 | `=I78` | =I78 |
| Ligne 164 | Col 10 | J164 | `=M78` | =M78 |
| Ligne 164 | Col 11 | K164 | `=I164*SIGN(J164)*ABS(J164)^1.821` | =I164*SIGN(J164)*ABS(J164)^1.821 |
| Ligne 164 | Col 12 | L164 | `=1.852*I164*ABS(J164)^(1.852-1)` | =1.852*I164*ABS(J164)^(1.852-1) |
| Ligne 164 | Col 13 | M164 | `=J164+$I$179` | =J164+$I$179 |
| Ligne 164 | Col 21 | U164 | `=P78` | =P78 |
| Ligne 164 | Col 22 | V164 | `=Q78` | =Q78 |
| Ligne 164 | Col 23 | W164 | `=S78` | =S78 |
| Ligne 164 | Col 24 | X164 | `=X78` | =X78 |
| Ligne 164 | Col 25 | Y164 | `=AD78` | =AD78 |
| Ligne 164 | Col 26 | Z164 | `=Z78` | =Z78 |
| Ligne 164 | Col 27 | AA164 | `=AA78` | =AA78 |
| Ligne 164 | Col 28 | AB164 | `=X164*SIGN(Y164)*ABS(Y164)^1.821` | =X164*SIGN(Y164)*ABS(Y164)^1.821 |
| Ligne 164 | Col 29 | AC164 | `=1.852*X164*ABS(Y164)^(1.852-1)` | =1.852*X164*ABS(Y164)^(1.852-1) |
| Ligne 164 | Col 30 | AD164 | `=IF(U164>0,
Y164+($I$179*Z164)+(AA164*X236),
Y164+$S$93)` | =IF(U164>0,
Y164+($I$179*Z164)+(AA164*X236),
Y164+$S$93) |
| Ligne 164 | Col 32 | AF164 | `=ABS(AD164)-ABS(Y164)` | =ABS(AD164)-ABS(Y164) |
| Ligne 165 | Col 8 | H165 | `=D79` | =D79 |
| Ligne 165 | Col 9 | I165 | `=I79` | =I79 |
| Ligne 165 | Col 10 | J165 | `=M79` | =M79 |
| Ligne 165 | Col 11 | K165 | `=I165*SIGN(J165)*ABS(J165)^1.821` | =I165*SIGN(J165)*ABS(J165)^1.821 |
| Ligne 165 | Col 12 | L165 | `=1.852*I165*ABS(J165)^(1.852-1)` | =1.852*I165*ABS(J165)^(1.852-1) |
| Ligne 165 | Col 13 | M165 | `=J165+$I$179` | =J165+$I$179 |
| Ligne 165 | Col 21 | U165 | `=P79` | =P79 |
| Ligne 165 | Col 22 | V165 | `=Q79` | =Q79 |
| Ligne 165 | Col 23 | W165 | `=S79` | =S79 |
| Ligne 165 | Col 24 | X165 | `=X79` | =X79 |
| Ligne 165 | Col 25 | Y165 | `=AD79` | =AD79 |
| Ligne 165 | Col 26 | Z165 | `=Z79` | =Z79 |
| Ligne 165 | Col 27 | AA165 | `=AA79` | =AA79 |
| Ligne 165 | Col 28 | AB165 | `=X165*SIGN(Y165)*ABS(Y165)^1.821` | =X165*SIGN(Y165)*ABS(Y165)^1.821 |
| Ligne 165 | Col 29 | AC165 | `=1.852*X165*ABS(Y165)^(1.852-1)` | =1.852*X165*ABS(Y165)^(1.852-1) |
| Ligne 165 | Col 30 | AD165 | `=IF(U165>0,
Y165+($I$179*Z165)+(AA165*X237),
Y165+$S$93)` | =IF(U165>0,
Y165+($I$179*Z165)+(AA165*X237),
Y165+$S$93) |
| Ligne 165 | Col 32 | AF165 | `=ABS(AD165)-ABS(Y165)` | =ABS(AD165)-ABS(Y165) |
| Ligne 166 | Col 8 | H166 | `=D80` | =D80 |
| Ligne 166 | Col 9 | I166 | `=I80` | =I80 |
| Ligne 166 | Col 10 | J166 | `=M80` | =M80 |
| Ligne 166 | Col 11 | K166 | `=I166*SIGN(J166)*ABS(J166)^1.821` | =I166*SIGN(J166)*ABS(J166)^1.821 |
| Ligne 166 | Col 12 | L166 | `=1.852*I166*ABS(J166)^(1.852-1)` | =1.852*I166*ABS(J166)^(1.852-1) |
| Ligne 166 | Col 13 | M166 | `=J166+$I$179` | =J166+$I$179 |
| Ligne 166 | Col 21 | U166 | `=P80` | =P80 |
| Ligne 166 | Col 22 | V166 | `=Q80` | =Q80 |
| Ligne 166 | Col 23 | W166 | `=S80` | =S80 |
| Ligne 166 | Col 24 | X166 | `=X80` | =X80 |
| Ligne 166 | Col 25 | Y166 | `=AD80` | =AD80 |
| Ligne 166 | Col 26 | Z166 | `=Z80` | =Z80 |
| Ligne 166 | Col 27 | AA166 | `=AA80` | =AA80 |
| Ligne 166 | Col 28 | AB166 | `=X166*SIGN(Y166)*ABS(Y166)^1.821` | =X166*SIGN(Y166)*ABS(Y166)^1.821 |
| Ligne 166 | Col 29 | AC166 | `=1.852*X166*ABS(Y166)^(1.852-1)` | =1.852*X166*ABS(Y166)^(1.852-1) |
| Ligne 166 | Col 30 | AD166 | `=IF(U166>0,
Y166+($I$179*Z166)+(AA166*X238),
Y166+$S$93)` | =IF(U166>0,
Y166+($I$179*Z166)+(AA166*X238),
Y166+$S$93) |
| Ligne 166 | Col 32 | AF166 | `=ABS(AD166)-ABS(Y166)` | =ABS(AD166)-ABS(Y166) |
| Ligne 167 | Col 8 | H167 | `=D81` | =D81 |
| Ligne 167 | Col 9 | I167 | `=I81` | =I81 |
| Ligne 167 | Col 10 | J167 | `=M81` | =M81 |
| Ligne 167 | Col 11 | K167 | `=I167*SIGN(J167)*ABS(J167)^1.821` | =I167*SIGN(J167)*ABS(J167)^1.821 |
| Ligne 167 | Col 12 | L167 | `=1.852*I167*ABS(J167)^(1.852-1)` | =1.852*I167*ABS(J167)^(1.852-1) |
| Ligne 167 | Col 13 | M167 | `=J167+$I$179` | =J167+$I$179 |
| Ligne 167 | Col 21 | U167 | `=P81` | =P81 |
| Ligne 167 | Col 22 | V167 | `=Q81` | =Q81 |
| Ligne 167 | Col 23 | W167 | `=S81` | =S81 |
| Ligne 167 | Col 24 | X167 | `=X81` | =X81 |
| Ligne 167 | Col 25 | Y167 | `=AD81` | =AD81 |
| Ligne 167 | Col 26 | Z167 | `=Z81` | =Z81 |
| Ligne 167 | Col 27 | AA167 | `=AA81` | =AA81 |
| Ligne 167 | Col 28 | AB167 | `=X167*SIGN(Y167)*ABS(Y167)^1.821` | =X167*SIGN(Y167)*ABS(Y167)^1.821 |
| Ligne 167 | Col 29 | AC167 | `=1.852*X167*ABS(Y167)^(1.852-1)` | =1.852*X167*ABS(Y167)^(1.852-1) |
| Ligne 167 | Col 30 | AD167 | `=IF(U167>0,
Y167+($I$179*Z167)+(AA167*X239),
Y167+$S$93)` | =IF(U167>0,
Y167+($I$179*Z167)+(AA167*X239),
Y167+$S$93) |
| Ligne 167 | Col 32 | AF167 | `=ABS(AD167)-ABS(Y167)` | =ABS(AD167)-ABS(Y167) |
| Ligne 168 | Col 8 | H168 | `=D82` | =D82 |
| Ligne 168 | Col 9 | I168 | `=I82` | =I82 |
| Ligne 168 | Col 10 | J168 | `=M82` | =M82 |
| Ligne 168 | Col 11 | K168 | `=I168*SIGN(J168)*ABS(J168)^1.821` | =I168*SIGN(J168)*ABS(J168)^1.821 |
| Ligne 168 | Col 12 | L168 | `=1.852*I168*ABS(J168)^(1.852-1)` | =1.852*I168*ABS(J168)^(1.852-1) |
| Ligne 168 | Col 13 | M168 | `=J168+$I$179` | =J168+$I$179 |
| Ligne 168 | Col 21 | U168 | `=P82` | =P82 |
| Ligne 168 | Col 22 | V168 | `=Q82` | =Q82 |
| Ligne 168 | Col 23 | W168 | `=S82` | =S82 |
| Ligne 168 | Col 24 | X168 | `=X82` | =X82 |
| Ligne 168 | Col 25 | Y168 | `=AD82` | =AD82 |
| Ligne 168 | Col 26 | Z168 | `=Z82` | =Z82 |
| Ligne 168 | Col 27 | AA168 | `=AA82` | =AA82 |
| Ligne 168 | Col 28 | AB168 | `=X168*SIGN(Y168)*ABS(Y168)^1.821` | =X168*SIGN(Y168)*ABS(Y168)^1.821 |
| Ligne 168 | Col 29 | AC168 | `=1.852*X168*ABS(Y168)^(1.852-1)` | =1.852*X168*ABS(Y168)^(1.852-1) |
| Ligne 168 | Col 30 | AD168 | `=IF(U168>0,
Y168+($I$179*Z168)+(AA168*X240),
Y168+$S$93)` | =IF(U168>0,
Y168+($I$179*Z168)+(AA168*X240),
Y168+$S$93) |
| Ligne 168 | Col 32 | AF168 | `=ABS(AD168)-ABS(Y168)` | =ABS(AD168)-ABS(Y168) |
| Ligne 169 | Col 8 | H169 | `=D83` | =D83 |
| Ligne 169 | Col 9 | I169 | `=I83` | =I83 |
| Ligne 169 | Col 10 | J169 | `=M83` | =M83 |
| Ligne 169 | Col 11 | K169 | `=I169*SIGN(J169)*ABS(J169)^1.821` | =I169*SIGN(J169)*ABS(J169)^1.821 |
| Ligne 169 | Col 12 | L169 | `=1.852*I169*ABS(J169)^(1.852-1)` | =1.852*I169*ABS(J169)^(1.852-1) |
| Ligne 169 | Col 13 | M169 | `=J169+$I$179` | =J169+$I$179 |
| Ligne 169 | Col 21 | U169 | `=P83` | =P83 |
| Ligne 169 | Col 22 | V169 | `=Q83` | =Q83 |
| Ligne 169 | Col 23 | W169 | `=S83` | =S83 |
| Ligne 169 | Col 24 | X169 | `=X83` | =X83 |
| Ligne 169 | Col 25 | Y169 | `=AD83` | =AD83 |
| Ligne 169 | Col 26 | Z169 | `=Z83` | =Z83 |
| Ligne 169 | Col 27 | AA169 | `=AA83` | =AA83 |
| Ligne 169 | Col 28 | AB169 | `=X169*SIGN(Y169)*ABS(Y169)^1.821` | =X169*SIGN(Y169)*ABS(Y169)^1.821 |
| Ligne 169 | Col 29 | AC169 | `=1.852*X169*ABS(Y169)^(1.852-1)` | =1.852*X169*ABS(Y169)^(1.852-1) |
| Ligne 169 | Col 30 | AD169 | `=IF(U169>0,
Y169+($I$179*Z169)+(AA169*X241),
Y169+$S$93)` | =IF(U169>0,
Y169+($I$179*Z169)+(AA169*X241),
Y169+$S$93) |
| Ligne 169 | Col 32 | AF169 | `=ABS(AD169)-ABS(Y169)` | =ABS(AD169)-ABS(Y169) |
| Ligne 170 | Col 8 | H170 | `=D84` | =D84 |
| Ligne 170 | Col 9 | I170 | `=I84` | =I84 |
| Ligne 170 | Col 10 | J170 | `=M84` | =M84 |
| Ligne 170 | Col 11 | K170 | `=I170*SIGN(J170)*ABS(J170)^1.821` | =I170*SIGN(J170)*ABS(J170)^1.821 |
| Ligne 170 | Col 12 | L170 | `=1.852*I170*ABS(J170)^(1.852-1)` | =1.852*I170*ABS(J170)^(1.852-1) |
| Ligne 170 | Col 13 | M170 | `=J170+$I$179` | =J170+$I$179 |
| Ligne 170 | Col 21 | U170 | `=P84` | =P84 |
| Ligne 170 | Col 22 | V170 | `=Q84` | =Q84 |
| Ligne 170 | Col 23 | W170 | `=S84` | =S84 |
| Ligne 170 | Col 24 | X170 | `=X84` | =X84 |
| Ligne 170 | Col 25 | Y170 | `=AD84` | =AD84 |
| Ligne 170 | Col 26 | Z170 | `=Z84` | =Z84 |
| Ligne 170 | Col 27 | AA170 | `=AA84` | =AA84 |
| Ligne 170 | Col 28 | AB170 | `=X170*SIGN(Y170)*ABS(Y170)^1.821` | =X170*SIGN(Y170)*ABS(Y170)^1.821 |
| Ligne 170 | Col 29 | AC170 | `=1.852*X170*ABS(Y170)^(1.852-1)` | =1.852*X170*ABS(Y170)^(1.852-1) |
| Ligne 170 | Col 30 | AD170 | `=IF(U170>0,
Y170+($I$179*Z170)+(AA170*X242),
Y170+$S$93)` | =IF(U170>0,
Y170+($I$179*Z170)+(AA170*X242),
Y170+$S$93) |
| Ligne 170 | Col 32 | AF170 | `=ABS(AD170)-ABS(Y170)` | =ABS(AD170)-ABS(Y170) |
| Ligne 171 | Col 8 | H171 | `=D85` | =D85 |
| Ligne 171 | Col 9 | I171 | `=I85` | =I85 |
| Ligne 171 | Col 10 | J171 | `=M85` | =M85 |
| Ligne 171 | Col 11 | K171 | `=I171*SIGN(J171)*ABS(J171)^1.821` | =I171*SIGN(J171)*ABS(J171)^1.821 |
| Ligne 171 | Col 12 | L171 | `=1.852*I171*ABS(J171)^(1.852-1)` | =1.852*I171*ABS(J171)^(1.852-1) |
| Ligne 171 | Col 13 | M171 | `=J171+$I$179` | =J171+$I$179 |
| Ligne 171 | Col 21 | U171 | `=P85` | =P85 |
| Ligne 171 | Col 22 | V171 | `=Q85` | =Q85 |
| Ligne 171 | Col 23 | W171 | `=S85` | =S85 |
| Ligne 171 | Col 24 | X171 | `=X85` | =X85 |
| Ligne 171 | Col 25 | Y171 | `=AD85` | =AD85 |
| Ligne 171 | Col 26 | Z171 | `=Z85` | =Z85 |
| Ligne 171 | Col 27 | AA171 | `=AA85` | =AA85 |
| Ligne 171 | Col 28 | AB171 | `=X171*SIGN(Y171)*ABS(Y171)^1.821` | =X171*SIGN(Y171)*ABS(Y171)^1.821 |
| Ligne 171 | Col 29 | AC171 | `=1.852*X171*ABS(Y171)^(1.852-1)` | =1.852*X171*ABS(Y171)^(1.852-1) |
| Ligne 171 | Col 30 | AD171 | `=IF(U171>0,
Y171+($I$179*Z171)+(AA171*X243),
Y171+$S$93)` | =IF(U171>0,
Y171+($I$179*Z171)+(AA171*X243),
Y171+$S$93) |
| Ligne 171 | Col 32 | AF171 | `=ABS(AD171)-ABS(Y171)` | =ABS(AD171)-ABS(Y171) |
| Ligne 172 | Col 8 | H172 | `=D86` | =D86 |
| Ligne 172 | Col 9 | I172 | `=I86` | =I86 |
| Ligne 172 | Col 10 | J172 | `=M86` | =M86 |
| Ligne 172 | Col 11 | K172 | `=I172*SIGN(J172)*ABS(J172)^1.821` | =I172*SIGN(J172)*ABS(J172)^1.821 |
| Ligne 172 | Col 12 | L172 | `=1.852*I172*ABS(J172)^(1.852-1)` | =1.852*I172*ABS(J172)^(1.852-1) |
| Ligne 172 | Col 13 | M172 | `=J172+$I$179` | =J172+$I$179 |
| Ligne 172 | Col 21 | U172 | `=P86` | =P86 |
| Ligne 172 | Col 22 | V172 | `=Q86` | =Q86 |
| Ligne 172 | Col 23 | W172 | `=S86` | =S86 |
| Ligne 172 | Col 24 | X172 | `=X86` | =X86 |
| Ligne 172 | Col 25 | Y172 | `=AD86` | =AD86 |
| Ligne 172 | Col 26 | Z172 | `=Z86` | =Z86 |
| Ligne 172 | Col 27 | AA172 | `=AA86` | =AA86 |
| Ligne 172 | Col 28 | AB172 | `=X172*SIGN(Y172)*ABS(Y172)^1.821` | =X172*SIGN(Y172)*ABS(Y172)^1.821 |
| Ligne 172 | Col 29 | AC172 | `=1.852*X172*ABS(Y172)^(1.852-1)` | =1.852*X172*ABS(Y172)^(1.852-1) |
| Ligne 172 | Col 30 | AD172 | `=IF(U172>0,
Y172+($I$179*Z172)+(AA172*X244),
Y172+$S$93)` | =IF(U172>0,
Y172+($I$179*Z172)+(AA172*X244),
Y172+$S$93) |
| Ligne 172 | Col 32 | AF172 | `=ABS(AD172)-ABS(Y172)` | =ABS(AD172)-ABS(Y172) |
| Ligne 173 | Col 8 | H173 | `=D87` | =D87 |
| Ligne 173 | Col 9 | I173 | `=I87` | =I87 |
| Ligne 173 | Col 10 | J173 | `=M87` | =M87 |
| Ligne 173 | Col 11 | K173 | `=I173*SIGN(J173)*ABS(J173)^1.821` | =I173*SIGN(J173)*ABS(J173)^1.821 |
| Ligne 173 | Col 12 | L173 | `=1.852*I173*ABS(J173)^(1.852-1)` | =1.852*I173*ABS(J173)^(1.852-1) |
| Ligne 173 | Col 13 | M173 | `=J173+$I$179` | =J173+$I$179 |
| Ligne 173 | Col 21 | U173 | `=P87` | =P87 |
| Ligne 173 | Col 22 | V173 | `=Q87` | =Q87 |
| Ligne 173 | Col 23 | W173 | `=S87` | =S87 |
| Ligne 173 | Col 24 | X173 | `=X87` | =X87 |
| Ligne 173 | Col 25 | Y173 | `=AD87` | =AD87 |
| Ligne 173 | Col 26 | Z173 | `=Z87` | =Z87 |
| Ligne 173 | Col 27 | AA173 | `=AA87` | =AA87 |
| Ligne 173 | Col 28 | AB173 | `=X173*SIGN(Y173)*ABS(Y173)^1.821` | =X173*SIGN(Y173)*ABS(Y173)^1.821 |
| Ligne 173 | Col 29 | AC173 | `=1.852*X173*ABS(Y173)^(1.852-1)` | =1.852*X173*ABS(Y173)^(1.852-1) |
| Ligne 173 | Col 30 | AD173 | `=IF(U173>0,
Y173+($I$179*Z173)+(AA173*X245),
Y173+$S$93)` | =IF(U173>0,
Y173+($I$179*Z173)+(AA173*X245),
Y173+$S$93) |
| Ligne 173 | Col 32 | AF173 | `=ABS(AD173)-ABS(Y173)` | =ABS(AD173)-ABS(Y173) |
| Ligne 174 | Col 8 | H174 | `=D88` | =D88 |
| Ligne 174 | Col 9 | I174 | `=I88` | =I88 |
| Ligne 174 | Col 10 | J174 | `=M88` | =M88 |
| Ligne 174 | Col 11 | K174 | `=I174*SIGN(J174)*ABS(J174)^1.821` | =I174*SIGN(J174)*ABS(J174)^1.821 |
| Ligne 174 | Col 12 | L174 | `=1.852*I174*ABS(J174)^(1.852-1)` | =1.852*I174*ABS(J174)^(1.852-1) |
| Ligne 174 | Col 13 | M174 | `=J174+$I$179` | =J174+$I$179 |
| Ligne 174 | Col 21 | U174 | `=P88` | =P88 |
| Ligne 174 | Col 22 | V174 | `=Q88` | =Q88 |
| Ligne 174 | Col 23 | W174 | `=S88` | =S88 |
| Ligne 174 | Col 24 | X174 | `=X88` | =X88 |
| Ligne 174 | Col 25 | Y174 | `=AD88` | =AD88 |
| Ligne 174 | Col 26 | Z174 | `=Z88` | =Z88 |
| Ligne 174 | Col 27 | AA174 | `=AA88` | =AA88 |
| Ligne 174 | Col 28 | AB174 | `=X174*SIGN(Y174)*ABS(Y174)^1.821` | =X174*SIGN(Y174)*ABS(Y174)^1.821 |
| Ligne 174 | Col 29 | AC174 | `=1.852*X174*ABS(Y174)^(1.852-1)` | =1.852*X174*ABS(Y174)^(1.852-1) |
| Ligne 174 | Col 30 | AD174 | `=IF(U174>0,
Y174+($I$179*Z174)+(AA174*X246),
Y174+$S$93)` | =IF(U174>0,
Y174+($I$179*Z174)+(AA174*X246),
Y174+$S$93) |
| Ligne 174 | Col 32 | AF174 | `=ABS(AD174)-ABS(Y174)` | =ABS(AD174)-ABS(Y174) |
| Ligne 175 | Col 8 | H175 | `=D89` | =D89 |
| Ligne 175 | Col 9 | I175 | `=I89` | =I89 |
| Ligne 175 | Col 10 | J175 | `=M89` | =M89 |
| Ligne 175 | Col 11 | K175 | `=I175*SIGN(J175)*ABS(J175)^1.821` | =I175*SIGN(J175)*ABS(J175)^1.821 |
| Ligne 175 | Col 12 | L175 | `=1.852*I175*ABS(J175)^(1.852-1)` | =1.852*I175*ABS(J175)^(1.852-1) |
| Ligne 175 | Col 13 | M175 | `=J175+$I$179` | =J175+$I$179 |
| Ligne 175 | Col 21 | U175 | `=P89` | =P89 |
| Ligne 175 | Col 22 | V175 | `=Q89` | =Q89 |
| Ligne 175 | Col 23 | W175 | `=S89` | =S89 |
| Ligne 175 | Col 24 | X175 | `=X89` | =X89 |
| Ligne 175 | Col 25 | Y175 | `=AD89` | =AD89 |
| Ligne 175 | Col 26 | Z175 | `=Z89` | =Z89 |
| Ligne 175 | Col 27 | AA175 | `=AA89` | =AA89 |
| Ligne 175 | Col 28 | AB175 | `=X175*SIGN(Y175)*ABS(Y175)^1.821` | =X175*SIGN(Y175)*ABS(Y175)^1.821 |
| Ligne 175 | Col 29 | AC175 | `=1.852*X175*ABS(Y175)^(1.852-1)` | =1.852*X175*ABS(Y175)^(1.852-1) |
| Ligne 175 | Col 30 | AD175 | `=IF(U175>0,
Y175+($I$179*Z175)+(AA175*X247),
Y175+$S$93)` | =IF(U175>0,
Y175+($I$179*Z175)+(AA175*X247),
Y175+$S$93) |
| Ligne 175 | Col 32 | AF175 | `=ABS(AD175)-ABS(Y175)` | =ABS(AD175)-ABS(Y175) |
| Ligne 176 | Col 8 | H176 | `=D90` | =D90 |
| Ligne 176 | Col 9 | I176 | `=I90` | =I90 |
| Ligne 176 | Col 10 | J176 | `=M90` | =M90 |
| Ligne 176 | Col 11 | K176 | `=I176*SIGN(J176)*ABS(J176)^1.821` | =I176*SIGN(J176)*ABS(J176)^1.821 |
| Ligne 176 | Col 12 | L176 | `=1.852*I176*ABS(J176)^(1.852-1)` | =1.852*I176*ABS(J176)^(1.852-1) |
| Ligne 176 | Col 13 | M176 | `=J176+$I$179` | =J176+$I$179 |
| Ligne 176 | Col 21 | U176 | `=P90` | =P90 |
| Ligne 176 | Col 22 | V176 | `=Q90` | =Q90 |
| Ligne 176 | Col 23 | W176 | `=S90` | =S90 |
| Ligne 176 | Col 24 | X176 | `=X90` | =X90 |
| Ligne 176 | Col 25 | Y176 | `=AD90` | =AD90 |
| Ligne 176 | Col 26 | Z176 | `=Z90` | =Z90 |
| Ligne 176 | Col 27 | AA176 | `=AA90` | =AA90 |
| Ligne 176 | Col 28 | AB176 | `=X176*SIGN(Y176)*ABS(Y176)^1.821` | =X176*SIGN(Y176)*ABS(Y176)^1.821 |
| Ligne 176 | Col 29 | AC176 | `=1.852*X176*ABS(Y176)^(1.852-1)` | =1.852*X176*ABS(Y176)^(1.852-1) |
| Ligne 176 | Col 30 | AD176 | `=IF(U176>0,
Y176+($I$179*Z176)+(AA176*X248),
Y176+$S$93)` | =IF(U176>0,
Y176+($I$179*Z176)+(AA176*X248),
Y176+$S$93) |
| Ligne 176 | Col 32 | AF176 | `=ABS(AD176)-ABS(Y176)` | =ABS(AD176)-ABS(Y176) |
| Ligne 177 | Col 8 | H177 | `=D91` | =D91 |
| Ligne 177 | Col 9 | I177 | `=I91` | =I91 |
| Ligne 177 | Col 10 | J177 | `=M91` | =M91 |
| Ligne 177 | Col 11 | K177 | `=I177*SIGN(J177)*ABS(J177)^1.821` | =I177*SIGN(J177)*ABS(J177)^1.821 |
| Ligne 177 | Col 12 | L177 | `=1.852*I177*ABS(J177)^(1.852-1)` | =1.852*I177*ABS(J177)^(1.852-1) |
| Ligne 177 | Col 13 | M177 | `=J177+$I$179` | =J177+$I$179 |
| Ligne 177 | Col 21 | U177 | `=P91` | =P91 |
| Ligne 177 | Col 22 | V177 | `=Q91` | =Q91 |
| Ligne 177 | Col 23 | W177 | `=S91` | =S91 |
| Ligne 177 | Col 24 | X177 | `=X91` | =X91 |
| Ligne 177 | Col 25 | Y177 | `=AD91` | =AD91 |
| Ligne 177 | Col 26 | Z177 | `=Z91` | =Z91 |
| Ligne 177 | Col 27 | AA177 | `=AA91` | =AA91 |
| Ligne 177 | Col 28 | AB177 | `=X177*SIGN(Y177)*ABS(Y177)^1.821` | =X177*SIGN(Y177)*ABS(Y177)^1.821 |
| Ligne 177 | Col 29 | AC177 | `=1.852*X177*ABS(Y177)^(1.852-1)` | =1.852*X177*ABS(Y177)^(1.852-1) |
| Ligne 177 | Col 30 | AD177 | `=IF(U177>0,
Y177+($I$179*Z177)+(AA177*X249),
Y177+$S$93)` | =IF(U177>0,
Y177+($I$179*Z177)+(AA177*X249),
Y177+$S$93) |
| Ligne 178 | Col 11 | K178 | `=SUM(K108:K177)` | =SUM(K108:K177) |
| Ligne 178 | Col 12 | L178 | `=SUM(L108:L177)` | =SUM(L108:L177) |
| Ligne 178 | Col 27 | AA178 | `=SUM(AB108:AB177)` | =SUM(AB108:AB177) |
| Ligne 178 | Col 28 | AB178 | `=SUM(AC108:AC177)` | =SUM(AC108:AC177) |
| Ligne 179 | Col 9 | I179 | `=-(K178/L178)` | =-(K178/L178) |
| Ligne 179 | Col 24 | X179 | `=ABS(AA178/(1.852*AB178))` | =ABS(AA178/(1.852*AB178)) |
| Ligne 180 | Col 9 | I180 | `=D93-I179` | =D93-I179 |
| Ligne 180 | Col 24 | X180 | `=S93-X179` | =S93-X179 |
| Ligne 181 | Col 9 | I181 | `=IF(I180>0, "L'agorithme est fonctionel","L'algorithme n'est pas fonctionnel; maille à revérifier")` | =IF(I180>0, "L'agorithme est fonctionel","L'algorithme n'est pas fonctionnel; maille à revérifier") |
| Ligne 181 | Col 24 | X181 | `=IF(X180>0, "L'agorithme est fonctionel","L'algorithme n'est pas fonctionnel; maille à revérifier")` | =IF(X180>0, "L'agorithme est fonctionel","L'algorithme n'est pas fonctionnel; maille à revérifier") |
| Ligne 211 | Col 10 | J211 | `=M108` | =M108 |
| Ligne 211 | Col 11 | K211 | `=I211*SIGN(J211)*ABS(J211)^1.821` | =I211*SIGN(J211)*ABS(J211)^1.821 |
| Ligne 211 | Col 12 | L211 | `=1.852*I211*ABS(J211)^(1.852-1)` | =1.852*I211*ABS(J211)^(1.852-1) |
| Ligne 212 | Col 10 | J212 | `=M109` | =M109 |
| Ligne 212 | Col 11 | K212 | `=I212*SIGN(J212)*ABS(J212)^1.821` | =I212*SIGN(J212)*ABS(J212)^1.821 |
| Ligne 212 | Col 12 | L212 | `=1.852*I212*ABS(J212)^(1.852-1)` | =1.852*I212*ABS(J212)^(1.852-1) |
| Ligne 213 | Col 10 | J213 | `=M110` | =M110 |
| Ligne 213 | Col 11 | K213 | `=I213*SIGN(J213)*ABS(J213)^1.821` | =I213*SIGN(J213)*ABS(J213)^1.821 |
| Ligne 213 | Col 12 | L213 | `=1.852*I213*ABS(J213)^(1.852-1)` | =1.852*I213*ABS(J213)^(1.852-1) |
| Ligne 214 | Col 10 | J214 | `=M111` | =M111 |
| Ligne 214 | Col 11 | K214 | `=I214*SIGN(J214)*ABS(J214)^1.821` | =I214*SIGN(J214)*ABS(J214)^1.821 |
| Ligne 214 | Col 12 | L214 | `=1.852*I214*ABS(J214)^(1.852-1)` | =1.852*I214*ABS(J214)^(1.852-1) |
| Ligne 215 | Col 10 | J215 | `=M112` | =M112 |
| Ligne 215 | Col 11 | K215 | `=I215*SIGN(J215)*ABS(J215)^1.821` | =I215*SIGN(J215)*ABS(J215)^1.821 |
| Ligne 215 | Col 12 | L215 | `=1.852*I215*ABS(J215)^(1.852-1)` | =1.852*I215*ABS(J215)^(1.852-1) |
| Ligne 216 | Col 10 | J216 | `=M113` | =M113 |
| Ligne 216 | Col 11 | K216 | `=I216*SIGN(J216)*ABS(J216)^1.821` | =I216*SIGN(J216)*ABS(J216)^1.821 |
| Ligne 216 | Col 12 | L216 | `=1.852*I216*ABS(J216)^(1.852-1)` | =1.852*I216*ABS(J216)^(1.852-1) |
| Ligne 217 | Col 10 | J217 | `=M114` | =M114 |
| Ligne 217 | Col 11 | K217 | `=I217*SIGN(J217)*ABS(J217)^1.821` | =I217*SIGN(J217)*ABS(J217)^1.821 |
| Ligne 217 | Col 12 | L217 | `=1.852*I217*ABS(J217)^(1.852-1)` | =1.852*I217*ABS(J217)^(1.852-1) |
| Ligne 218 | Col 10 | J218 | `=M115` | =M115 |
| Ligne 218 | Col 11 | K218 | `=I218*SIGN(J218)*ABS(J218)^1.821` | =I218*SIGN(J218)*ABS(J218)^1.821 |
| Ligne 218 | Col 12 | L218 | `=1.852*I218*ABS(J218)^(1.852-1)` | =1.852*I218*ABS(J218)^(1.852-1) |
| Ligne 219 | Col 10 | J219 | `=M116` | =M116 |
| Ligne 219 | Col 11 | K219 | `=I219*SIGN(J219)*ABS(J219)^1.821` | =I219*SIGN(J219)*ABS(J219)^1.821 |
| Ligne 219 | Col 12 | L219 | `=1.852*I219*ABS(J219)^(1.852-1)` | =1.852*I219*ABS(J219)^(1.852-1) |
| Ligne 220 | Col 10 | J220 | `=M117` | =M117 |
| Ligne 220 | Col 11 | K220 | `=I220*SIGN(J220)*ABS(J220)^1.821` | =I220*SIGN(J220)*ABS(J220)^1.821 |
| Ligne 220 | Col 12 | L220 | `=1.852*I220*ABS(J220)^(1.852-1)` | =1.852*I220*ABS(J220)^(1.852-1) |
| Ligne 221 | Col 10 | J221 | `=M118` | =M118 |
| Ligne 221 | Col 11 | K221 | `=I221*SIGN(J221)*ABS(J221)^1.821` | =I221*SIGN(J221)*ABS(J221)^1.821 |
| Ligne 221 | Col 12 | L221 | `=1.852*I221*ABS(J221)^(1.852-1)` | =1.852*I221*ABS(J221)^(1.852-1) |
| Ligne 222 | Col 10 | J222 | `=M119` | =M119 |
| Ligne 222 | Col 11 | K222 | `=I222*SIGN(J222)*ABS(J222)^1.821` | =I222*SIGN(J222)*ABS(J222)^1.821 |
| Ligne 222 | Col 12 | L222 | `=1.852*I222*ABS(J222)^(1.852-1)` | =1.852*I222*ABS(J222)^(1.852-1) |
| Ligne 223 | Col 10 | J223 | `=M120` | =M120 |
| Ligne 223 | Col 11 | K223 | `=I223*SIGN(J223)*ABS(J223)^1.821` | =I223*SIGN(J223)*ABS(J223)^1.821 |
| Ligne 223 | Col 12 | L223 | `=1.852*I223*ABS(J223)^(1.852-1)` | =1.852*I223*ABS(J223)^(1.852-1) |
| Ligne 224 | Col 10 | J224 | `=M121` | =M121 |
| Ligne 224 | Col 11 | K224 | `=I224*SIGN(J224)*ABS(J224)^1.821` | =I224*SIGN(J224)*ABS(J224)^1.821 |
| Ligne 224 | Col 12 | L224 | `=1.852*I224*ABS(J224)^(1.852-1)` | =1.852*I224*ABS(J224)^(1.852-1) |
| Ligne 225 | Col 10 | J225 | `=M122` | =M122 |
| Ligne 225 | Col 11 | K225 | `=I225*SIGN(J225)*ABS(J225)^1.821` | =I225*SIGN(J225)*ABS(J225)^1.821 |
| Ligne 225 | Col 12 | L225 | `=1.852*I225*ABS(J225)^(1.852-1)` | =1.852*I225*ABS(J225)^(1.852-1) |
| Ligne 226 | Col 10 | J226 | `=M123` | =M123 |
| Ligne 226 | Col 11 | K226 | `=I226*SIGN(J226)*ABS(J226)^1.821` | =I226*SIGN(J226)*ABS(J226)^1.821 |
| Ligne 226 | Col 12 | L226 | `=1.852*I226*ABS(J226)^(1.852-1)` | =1.852*I226*ABS(J226)^(1.852-1) |
| Ligne 227 | Col 10 | J227 | `=M124` | =M124 |
| Ligne 227 | Col 11 | K227 | `=I227*SIGN(J227)*ABS(J227)^1.821` | =I227*SIGN(J227)*ABS(J227)^1.821 |
| Ligne 227 | Col 12 | L227 | `=1.852*I227*ABS(J227)^(1.852-1)` | =1.852*I227*ABS(J227)^(1.852-1) |
| Ligne 228 | Col 10 | J228 | `=M125` | =M125 |
| Ligne 228 | Col 11 | K228 | `=I228*SIGN(J228)*ABS(J228)^1.821` | =I228*SIGN(J228)*ABS(J228)^1.821 |
| Ligne 228 | Col 12 | L228 | `=1.852*I228*ABS(J228)^(1.852-1)` | =1.852*I228*ABS(J228)^(1.852-1) |
| Ligne 229 | Col 10 | J229 | `=M126` | =M126 |
| Ligne 229 | Col 11 | K229 | `=I229*SIGN(J229)*ABS(J229)^1.821` | =I229*SIGN(J229)*ABS(J229)^1.821 |
| Ligne 229 | Col 12 | L229 | `=1.852*I229*ABS(J229)^(1.852-1)` | =1.852*I229*ABS(J229)^(1.852-1) |
| Ligne 230 | Col 10 | J230 | `=M127` | =M127 |
| Ligne 230 | Col 11 | K230 | `=I230*SIGN(J230)*ABS(J230)^1.821` | =I230*SIGN(J230)*ABS(J230)^1.821 |
| Ligne 230 | Col 12 | L230 | `=1.852*I230*ABS(J230)^(1.852-1)` | =1.852*I230*ABS(J230)^(1.852-1) |
| Ligne 231 | Col 10 | J231 | `=M128` | =M128 |
| Ligne 231 | Col 11 | K231 | `=I231*SIGN(J231)*ABS(J231)^1.821` | =I231*SIGN(J231)*ABS(J231)^1.821 |
| Ligne 231 | Col 12 | L231 | `=1.852*I231*ABS(J231)^(1.852-1)` | =1.852*I231*ABS(J231)^(1.852-1) |
| Ligne 232 | Col 10 | J232 | `=M129` | =M129 |
| Ligne 232 | Col 11 | K232 | `=I232*SIGN(J232)*ABS(J232)^1.821` | =I232*SIGN(J232)*ABS(J232)^1.821 |
| Ligne 232 | Col 12 | L232 | `=1.852*I232*ABS(J232)^(1.852-1)` | =1.852*I232*ABS(J232)^(1.852-1) |
| Ligne 233 | Col 10 | J233 | `=M130` | =M130 |
| Ligne 233 | Col 11 | K233 | `=I233*SIGN(J233)*ABS(J233)^1.821` | =I233*SIGN(J233)*ABS(J233)^1.821 |
| Ligne 233 | Col 12 | L233 | `=1.852*I233*ABS(J233)^(1.852-1)` | =1.852*I233*ABS(J233)^(1.852-1) |
| Ligne 234 | Col 10 | J234 | `=M131` | =M131 |
| Ligne 234 | Col 11 | K234 | `=I234*SIGN(J234)*ABS(J234)^1.821` | =I234*SIGN(J234)*ABS(J234)^1.821 |
| Ligne 234 | Col 12 | L234 | `=1.852*I234*ABS(J234)^(1.852-1)` | =1.852*I234*ABS(J234)^(1.852-1) |
| Ligne 235 | Col 10 | J235 | `=M132` | =M132 |
| Ligne 235 | Col 11 | K235 | `=I235*SIGN(J235)*ABS(J235)^1.821` | =I235*SIGN(J235)*ABS(J235)^1.821 |
| Ligne 235 | Col 12 | L235 | `=1.852*I235*ABS(J235)^(1.852-1)` | =1.852*I235*ABS(J235)^(1.852-1) |
| Ligne 236 | Col 10 | J236 | `=M133` | =M133 |
| Ligne 236 | Col 11 | K236 | `=I236*SIGN(J236)*ABS(J236)^1.821` | =I236*SIGN(J236)*ABS(J236)^1.821 |
| Ligne 236 | Col 12 | L236 | `=1.852*I236*ABS(J236)^(1.852-1)` | =1.852*I236*ABS(J236)^(1.852-1) |
| Ligne 237 | Col 10 | J237 | `=M134` | =M134 |
| Ligne 237 | Col 11 | K237 | `=I237*SIGN(J237)*ABS(J237)^1.821` | =I237*SIGN(J237)*ABS(J237)^1.821 |
| Ligne 237 | Col 12 | L237 | `=1.852*I237*ABS(J237)^(1.852-1)` | =1.852*I237*ABS(J237)^(1.852-1) |
| Ligne 238 | Col 10 | J238 | `=M135` | =M135 |
| Ligne 238 | Col 11 | K238 | `=I238*SIGN(J238)*ABS(J238)^1.821` | =I238*SIGN(J238)*ABS(J238)^1.821 |
| Ligne 238 | Col 12 | L238 | `=1.852*I238*ABS(J238)^(1.852-1)` | =1.852*I238*ABS(J238)^(1.852-1) |
| Ligne 239 | Col 10 | J239 | `=M136` | =M136 |
| Ligne 239 | Col 11 | K239 | `=I239*SIGN(J239)*ABS(J239)^1.821` | =I239*SIGN(J239)*ABS(J239)^1.821 |
| Ligne 239 | Col 12 | L239 | `=1.852*I239*ABS(J239)^(1.852-1)` | =1.852*I239*ABS(J239)^(1.852-1) |
| Ligne 240 | Col 10 | J240 | `=M137` | =M137 |
| Ligne 240 | Col 11 | K240 | `=I240*SIGN(J240)*ABS(J240)^1.821` | =I240*SIGN(J240)*ABS(J240)^1.821 |
| Ligne 240 | Col 12 | L240 | `=1.852*I240*ABS(J240)^(1.852-1)` | =1.852*I240*ABS(J240)^(1.852-1) |
| Ligne 241 | Col 10 | J241 | `=M138` | =M138 |
| Ligne 241 | Col 11 | K241 | `=I241*SIGN(J241)*ABS(J241)^1.821` | =I241*SIGN(J241)*ABS(J241)^1.821 |
| Ligne 241 | Col 12 | L241 | `=1.852*I241*ABS(J241)^(1.852-1)` | =1.852*I241*ABS(J241)^(1.852-1) |
| Ligne 242 | Col 10 | J242 | `=M139` | =M139 |
| Ligne 242 | Col 11 | K242 | `=I242*SIGN(J242)*ABS(J242)^1.821` | =I242*SIGN(J242)*ABS(J242)^1.821 |
| Ligne 242 | Col 12 | L242 | `=1.852*I242*ABS(J242)^(1.852-1)` | =1.852*I242*ABS(J242)^(1.852-1) |
| Ligne 243 | Col 10 | J243 | `=M140` | =M140 |
| Ligne 243 | Col 11 | K243 | `=I243*SIGN(J243)*ABS(J243)^1.821` | =I243*SIGN(J243)*ABS(J243)^1.821 |
| Ligne 243 | Col 12 | L243 | `=1.852*I243*ABS(J243)^(1.852-1)` | =1.852*I243*ABS(J243)^(1.852-1) |
| Ligne 244 | Col 10 | J244 | `=M141` | =M141 |
| Ligne 244 | Col 11 | K244 | `=I244*SIGN(J244)*ABS(J244)^1.821` | =I244*SIGN(J244)*ABS(J244)^1.821 |
| Ligne 244 | Col 12 | L244 | `=1.852*I244*ABS(J244)^(1.852-1)` | =1.852*I244*ABS(J244)^(1.852-1) |
| Ligne 245 | Col 10 | J245 | `=M142` | =M142 |
| Ligne 245 | Col 11 | K245 | `=I245*SIGN(J245)*ABS(J245)^1.821` | =I245*SIGN(J245)*ABS(J245)^1.821 |
| Ligne 245 | Col 12 | L245 | `=1.852*I245*ABS(J245)^(1.852-1)` | =1.852*I245*ABS(J245)^(1.852-1) |
| Ligne 246 | Col 10 | J246 | `=M143` | =M143 |
| Ligne 246 | Col 11 | K246 | `=I246*SIGN(J246)*ABS(J246)^1.821` | =I246*SIGN(J246)*ABS(J246)^1.821 |
| Ligne 246 | Col 12 | L246 | `=1.852*I246*ABS(J246)^(1.852-1)` | =1.852*I246*ABS(J246)^(1.852-1) |
| Ligne 247 | Col 10 | J247 | `=M144` | =M144 |
| Ligne 247 | Col 11 | K247 | `=I247*SIGN(J247)*ABS(J247)^1.821` | =I247*SIGN(J247)*ABS(J247)^1.821 |
| Ligne 247 | Col 12 | L247 | `=1.852*I247*ABS(J247)^(1.852-1)` | =1.852*I247*ABS(J247)^(1.852-1) |
| Ligne 248 | Col 10 | J248 | `=M145` | =M145 |
| Ligne 248 | Col 11 | K248 | `=I248*SIGN(J248)*ABS(J248)^1.821` | =I248*SIGN(J248)*ABS(J248)^1.821 |
| Ligne 248 | Col 12 | L248 | `=1.852*I248*ABS(J248)^(1.852-1)` | =1.852*I248*ABS(J248)^(1.852-1) |
| Ligne 249 | Col 10 | J249 | `=M146` | =M146 |
| Ligne 249 | Col 11 | K249 | `=I249*SIGN(J249)*ABS(J249)^1.821` | =I249*SIGN(J249)*ABS(J249)^1.821 |
| Ligne 249 | Col 12 | L249 | `=1.852*I249*ABS(J249)^(1.852-1)` | =1.852*I249*ABS(J249)^(1.852-1) |
| Ligne 250 | Col 10 | J250 | `=M147` | =M147 |
| Ligne 250 | Col 11 | K250 | `=I250*SIGN(J250)*ABS(J250)^1.821` | =I250*SIGN(J250)*ABS(J250)^1.821 |
| Ligne 250 | Col 12 | L250 | `=1.852*I250*ABS(J250)^(1.852-1)` | =1.852*I250*ABS(J250)^(1.852-1) |
| Ligne 251 | Col 10 | J251 | `=M148` | =M148 |
| Ligne 251 | Col 11 | K251 | `=I251*SIGN(J251)*ABS(J251)^1.821` | =I251*SIGN(J251)*ABS(J251)^1.821 |
| Ligne 251 | Col 12 | L251 | `=1.852*I251*ABS(J251)^(1.852-1)` | =1.852*I251*ABS(J251)^(1.852-1) |
| Ligne 252 | Col 10 | J252 | `=M149` | =M149 |
| Ligne 252 | Col 11 | K252 | `=I252*SIGN(J252)*ABS(J252)^1.821` | =I252*SIGN(J252)*ABS(J252)^1.821 |
| Ligne 252 | Col 12 | L252 | `=1.852*I252*ABS(J252)^(1.852-1)` | =1.852*I252*ABS(J252)^(1.852-1) |
| Ligne 253 | Col 10 | J253 | `=M150` | =M150 |
| Ligne 253 | Col 11 | K253 | `=I253*SIGN(J253)*ABS(J253)^1.821` | =I253*SIGN(J253)*ABS(J253)^1.821 |
| Ligne 253 | Col 12 | L253 | `=1.852*I253*ABS(J253)^(1.852-1)` | =1.852*I253*ABS(J253)^(1.852-1) |
| Ligne 254 | Col 10 | J254 | `=M151` | =M151 |
| Ligne 254 | Col 11 | K254 | `=I254*SIGN(J254)*ABS(J254)^1.821` | =I254*SIGN(J254)*ABS(J254)^1.821 |
| Ligne 254 | Col 12 | L254 | `=1.852*I254*ABS(J254)^(1.852-1)` | =1.852*I254*ABS(J254)^(1.852-1) |
| Ligne 255 | Col 10 | J255 | `=M152` | =M152 |
| Ligne 255 | Col 11 | K255 | `=I255*SIGN(J255)*ABS(J255)^1.821` | =I255*SIGN(J255)*ABS(J255)^1.821 |
| Ligne 255 | Col 12 | L255 | `=1.852*I255*ABS(J255)^(1.852-1)` | =1.852*I255*ABS(J255)^(1.852-1) |
| Ligne 256 | Col 10 | J256 | `=M153` | =M153 |
| Ligne 256 | Col 11 | K256 | `=I256*SIGN(J256)*ABS(J256)^1.821` | =I256*SIGN(J256)*ABS(J256)^1.821 |
| Ligne 256 | Col 12 | L256 | `=1.852*I256*ABS(J256)^(1.852-1)` | =1.852*I256*ABS(J256)^(1.852-1) |
| Ligne 257 | Col 10 | J257 | `=M154` | =M154 |
| Ligne 257 | Col 11 | K257 | `=I257*SIGN(J257)*ABS(J257)^1.821` | =I257*SIGN(J257)*ABS(J257)^1.821 |
| Ligne 257 | Col 12 | L257 | `=1.852*I257*ABS(J257)^(1.852-1)` | =1.852*I257*ABS(J257)^(1.852-1) |
| Ligne 258 | Col 10 | J258 | `=M155` | =M155 |
| Ligne 258 | Col 11 | K258 | `=I258*SIGN(J258)*ABS(J258)^1.821` | =I258*SIGN(J258)*ABS(J258)^1.821 |
| Ligne 258 | Col 12 | L258 | `=1.852*I258*ABS(J258)^(1.852-1)` | =1.852*I258*ABS(J258)^(1.852-1) |
| Ligne 259 | Col 10 | J259 | `=M156` | =M156 |
| Ligne 259 | Col 11 | K259 | `=I259*SIGN(J259)*ABS(J259)^1.821` | =I259*SIGN(J259)*ABS(J259)^1.821 |
| Ligne 259 | Col 12 | L259 | `=1.852*I259*ABS(J259)^(1.852-1)` | =1.852*I259*ABS(J259)^(1.852-1) |
| Ligne 260 | Col 10 | J260 | `=M157` | =M157 |
| Ligne 260 | Col 11 | K260 | `=I260*SIGN(J260)*ABS(J260)^1.821` | =I260*SIGN(J260)*ABS(J260)^1.821 |
| Ligne 260 | Col 12 | L260 | `=1.852*I260*ABS(J260)^(1.852-1)` | =1.852*I260*ABS(J260)^(1.852-1) |
| Ligne 261 | Col 10 | J261 | `=M158` | =M158 |
| Ligne 261 | Col 11 | K261 | `=I261*SIGN(J261)*ABS(J261)^1.821` | =I261*SIGN(J261)*ABS(J261)^1.821 |
| Ligne 261 | Col 12 | L261 | `=1.852*I261*ABS(J261)^(1.852-1)` | =1.852*I261*ABS(J261)^(1.852-1) |
| Ligne 262 | Col 10 | J262 | `=M159` | =M159 |
| Ligne 262 | Col 11 | K262 | `=I262*SIGN(J262)*ABS(J262)^1.821` | =I262*SIGN(J262)*ABS(J262)^1.821 |
| Ligne 262 | Col 12 | L262 | `=1.852*I262*ABS(J262)^(1.852-1)` | =1.852*I262*ABS(J262)^(1.852-1) |
| Ligne 263 | Col 10 | J263 | `=M160` | =M160 |
| Ligne 263 | Col 11 | K263 | `=I263*SIGN(J263)*ABS(J263)^1.821` | =I263*SIGN(J263)*ABS(J263)^1.821 |
| Ligne 263 | Col 12 | L263 | `=1.852*I263*ABS(J263)^(1.852-1)` | =1.852*I263*ABS(J263)^(1.852-1) |
| Ligne 264 | Col 10 | J264 | `=M161` | =M161 |
| Ligne 264 | Col 11 | K264 | `=I264*SIGN(J264)*ABS(J264)^1.821` | =I264*SIGN(J264)*ABS(J264)^1.821 |
| Ligne 264 | Col 12 | L264 | `=1.852*I264*ABS(J264)^(1.852-1)` | =1.852*I264*ABS(J264)^(1.852-1) |
| Ligne 265 | Col 10 | J265 | `=M162` | =M162 |
| Ligne 265 | Col 11 | K265 | `=I265*SIGN(J265)*ABS(J265)^1.821` | =I265*SIGN(J265)*ABS(J265)^1.821 |
| Ligne 265 | Col 12 | L265 | `=1.852*I265*ABS(J265)^(1.852-1)` | =1.852*I265*ABS(J265)^(1.852-1) |
| Ligne 266 | Col 10 | J266 | `=M163` | =M163 |
| Ligne 266 | Col 11 | K266 | `=I266*SIGN(J266)*ABS(J266)^1.821` | =I266*SIGN(J266)*ABS(J266)^1.821 |
| Ligne 266 | Col 12 | L266 | `=1.852*I266*ABS(J266)^(1.852-1)` | =1.852*I266*ABS(J266)^(1.852-1) |
| Ligne 267 | Col 10 | J267 | `=M164` | =M164 |
| Ligne 267 | Col 11 | K267 | `=I267*SIGN(J267)*ABS(J267)^1.821` | =I267*SIGN(J267)*ABS(J267)^1.821 |
| Ligne 267 | Col 12 | L267 | `=1.852*I267*ABS(J267)^(1.852-1)` | =1.852*I267*ABS(J267)^(1.852-1) |
| Ligne 268 | Col 10 | J268 | `=M165` | =M165 |
| Ligne 268 | Col 11 | K268 | `=I268*SIGN(J268)*ABS(J268)^1.821` | =I268*SIGN(J268)*ABS(J268)^1.821 |
| Ligne 268 | Col 12 | L268 | `=1.852*I268*ABS(J268)^(1.852-1)` | =1.852*I268*ABS(J268)^(1.852-1) |
| Ligne 269 | Col 10 | J269 | `=M166` | =M166 |
| Ligne 269 | Col 11 | K269 | `=I269*SIGN(J269)*ABS(J269)^1.821` | =I269*SIGN(J269)*ABS(J269)^1.821 |
| Ligne 269 | Col 12 | L269 | `=1.852*I269*ABS(J269)^(1.852-1)` | =1.852*I269*ABS(J269)^(1.852-1) |
| Ligne 270 | Col 10 | J270 | `=M167` | =M167 |
| Ligne 270 | Col 11 | K270 | `=I270*SIGN(J270)*ABS(J270)^1.821` | =I270*SIGN(J270)*ABS(J270)^1.821 |
| Ligne 270 | Col 12 | L270 | `=1.852*I270*ABS(J270)^(1.852-1)` | =1.852*I270*ABS(J270)^(1.852-1) |
| Ligne 271 | Col 10 | J271 | `=M168` | =M168 |
| Ligne 271 | Col 11 | K271 | `=I271*SIGN(J271)*ABS(J271)^1.821` | =I271*SIGN(J271)*ABS(J271)^1.821 |
| Ligne 271 | Col 12 | L271 | `=1.852*I271*ABS(J271)^(1.852-1)` | =1.852*I271*ABS(J271)^(1.852-1) |
| Ligne 272 | Col 10 | J272 | `=M169` | =M169 |
| Ligne 272 | Col 11 | K272 | `=I272*SIGN(J272)*ABS(J272)^1.821` | =I272*SIGN(J272)*ABS(J272)^1.821 |
| Ligne 272 | Col 12 | L272 | `=1.852*I272*ABS(J272)^(1.852-1)` | =1.852*I272*ABS(J272)^(1.852-1) |
| Ligne 273 | Col 10 | J273 | `=M170` | =M170 |
| Ligne 273 | Col 11 | K273 | `=I273*SIGN(J273)*ABS(J273)^1.821` | =I273*SIGN(J273)*ABS(J273)^1.821 |
| Ligne 273 | Col 12 | L273 | `=1.852*I273*ABS(J273)^(1.852-1)` | =1.852*I273*ABS(J273)^(1.852-1) |
| Ligne 274 | Col 10 | J274 | `=M171` | =M171 |
| Ligne 274 | Col 11 | K274 | `=I274*SIGN(J274)*ABS(J274)^1.821` | =I274*SIGN(J274)*ABS(J274)^1.821 |
| Ligne 274 | Col 12 | L274 | `=1.852*I274*ABS(J274)^(1.852-1)` | =1.852*I274*ABS(J274)^(1.852-1) |
| Ligne 275 | Col 10 | J275 | `=M172` | =M172 |
| Ligne 275 | Col 11 | K275 | `=I275*SIGN(J275)*ABS(J275)^1.821` | =I275*SIGN(J275)*ABS(J275)^1.821 |
| Ligne 275 | Col 12 | L275 | `=1.852*I275*ABS(J275)^(1.852-1)` | =1.852*I275*ABS(J275)^(1.852-1) |
| Ligne 276 | Col 10 | J276 | `=M173` | =M173 |
| Ligne 276 | Col 11 | K276 | `=I276*SIGN(J276)*ABS(J276)^1.821` | =I276*SIGN(J276)*ABS(J276)^1.821 |
| Ligne 276 | Col 12 | L276 | `=1.852*I276*ABS(J276)^(1.852-1)` | =1.852*I276*ABS(J276)^(1.852-1) |
| Ligne 277 | Col 10 | J277 | `=M174` | =M174 |
| Ligne 277 | Col 11 | K277 | `=I277*SIGN(J277)*ABS(J277)^1.821` | =I277*SIGN(J277)*ABS(J277)^1.821 |
| Ligne 277 | Col 12 | L277 | `=1.852*I277*ABS(J277)^(1.852-1)` | =1.852*I277*ABS(J277)^(1.852-1) |
| Ligne 278 | Col 10 | J278 | `=M175` | =M175 |
| Ligne 278 | Col 11 | K278 | `=I278*SIGN(J278)*ABS(J278)^1.821` | =I278*SIGN(J278)*ABS(J278)^1.821 |
| Ligne 278 | Col 12 | L278 | `=1.852*I278*ABS(J278)^(1.852-1)` | =1.852*I278*ABS(J278)^(1.852-1) |
| Ligne 279 | Col 10 | J279 | `=M176` | =M176 |
| Ligne 279 | Col 11 | K279 | `=I279*SIGN(J279)*ABS(J279)^1.821` | =I279*SIGN(J279)*ABS(J279)^1.821 |
| Ligne 279 | Col 12 | L279 | `=1.852*I279*ABS(J279)^(1.852-1)` | =1.852*I279*ABS(J279)^(1.852-1) |
| Ligne 280 | Col 10 | J280 | `=M177` | =M177 |
| Ligne 280 | Col 11 | K280 | `=I280*SIGN(J280)*ABS(J280)^1.821` | =I280*SIGN(J280)*ABS(J280)^1.821 |
| Ligne 280 | Col 12 | L280 | `=1.852*I280*ABS(J280)^(1.852-1)` | =1.852*I280*ABS(J280)^(1.852-1) |
| Ligne 282 | Col 9 | I282 | `=-(K281/L281)` | =-(K281/L281) |
| Ligne 283 | Col 9 | I283 | `=I180-I282` | =I180-I282 |
| Ligne 284 | Col 9 | I284 | `=IF(I283>0, "L'agorithme est fonctionel","L'algorithme n'est pas fonctionnel; maille à revérifier")` | =IF(I283>0, "L'agorithme est fonctionel","L'algorithme n'est pas fonctionnel; maille à revérifier") |