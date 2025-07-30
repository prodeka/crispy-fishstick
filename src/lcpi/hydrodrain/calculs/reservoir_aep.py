
def dimensionner_volume_reservoir(donnees: dict) -> dict:
    pop = donnees.get("population")
    dotation_l_j_hab = donnees.get("dotation_l_j_hab")
    cp_j = donnees.get("coeff_pointe_journalier")
    repartition_horaire = donnees.get("repartition_horaire_pourcent")

    q_jour_max_m3 = (pop * dotation_l_j_hab * cp_j) / 1000
    debit_adduction_m3_h = q_jour_max_m3 / 24
    
    v_prod_cumul = [h * debit_adduction_m3_h for h in range(1, 25)]
    v_conso_cumul = []
    conso_cumul = 0
    for i in range(24):
        conso_h = (repartition_horaire[i] / 100) * q_jour_max_m3
        conso_cumul += conso_h
        v_conso_cumul.append(conso_cumul)
        
    v_diff = [prod - conso for prod, conso in zip(v_prod_cumul, v_conso_cumul)]
    v_regulation = max(v_diff) - min(v_diff)
    v_incendie = 120 # m3
    v_secours = (1/3) * q_jour_max_m3 # 8h de conso
    v_utile = v_regulation + v_incendie + v_secours
    
    return {
        "statut": "OK", "volume_regulation_m3": round(v_regulation, 2),
        "volume_incendie_m3": v_incendie, "volume_secours_m3": round(v_secours, 2),
        "volume_utile_total_m3": round(v_utile, 2)
    }
