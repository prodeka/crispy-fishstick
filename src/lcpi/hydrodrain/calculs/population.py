import math

def prevoir_population(donnees: dict) -> dict:
    methode = donnees.get("methode")
    t_futur = donnees.get("annee_projet")
    resultats = {"methode": methode, "annee_projet": t_futur}
    
    try:
        if methode == "arithmetique":
            y1, t1 = donnees["pop_annee_1"]
            y2, t2 = donnees["pop_annee_2"]
            ku = (y2 - y1) / (t2 - t1)
            pop_future = y2 + ku * (t_futur - t2)
            resultats["population_estimee"] = int(pop_future)

        elif methode in ["geometrique", "exponentiel", "malthus"]:
            y1, t1 = donnees["pop_annee_1"]
            y2, t2 = donnees["pop_annee_2"]
            kp = (math.log(y2) - math.log(y1)) / (t2 - t1)
            log_pop_future = math.log(y2) + kp * (t_futur - t2)
            resultats["population_estimee"] = int(math.exp(log_pop_future))

        elif methode == "logistique":
            y0, t0 = donnees["pop_annee_0"]
            y1, t1 = donnees["pop_annee_1"]
            y2, t2 = donnees["pop_annee_2"]
            n = t1 - t0
            if (t2 - t1) != n:
                raise ValueError("L'intervalle de temps 'n' entre les recensements doit être constant.")
            x = t_futur - t0

            K_denom = (y0 * y2 - y1**2)
            if K_denom == 0:
                raise ValueError("Dénominateur nul (y0*y2 - y1^2 = 0), la méthode logistique ne peut pas s'appliquer avec ces valeurs.")
            K = (2 * y0 * y1 * y2 - y1**2 * (y0 + y2)) / K_denom

            if K <= max(y0, y1, y2):
                raise ValueError(f"Le plafond de saturation K={K:.2f} est inférieur ou égal à la population observée. La méthode logistique ne peut pas s'appliquer avec ces valeurs.")

            a = math.log10((K - y0) / y0)
            b = (1/n) * math.log10((y0 * (K - y1)) / (y1 * (K - y0)))

            pop_future = K / (1 + 10**(a - b*x))
            resultats["population_estimee"] = int(pop_future)
            resultats["plafond_saturation_K"] = int(K)

        else:
            raise ValueError(f"Méthode '{methode}' non reconnue ou non implémentée.")
        
        resultats["statut"] = "SUCCES"
        return resultats
    except Exception as e:
        return {"statut": "ERREUR", "message": str(e)}
