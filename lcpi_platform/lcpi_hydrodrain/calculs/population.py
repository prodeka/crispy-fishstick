import math

def prevoir_population(donnees: dict) -> dict:
    y1, t1 = donnees.get("pop_annee_1")
    y2, t2 = donnees.get("pop_annee_2")
    t_futur = donnees.get("annee_projet")
    methode = donnees.get("methode")
    
    resultats = {"methode": methode, "annee_projet": t_futur}
    
    try:
        if methode == "arithmetique":
            ku = (y2 - y1) / (t2 - t1)
            pop_future = y2 + ku * (t_futur - t2)
            resultats["population_estimee"] = int(pop_future)
        
        elif methode == "geometrique":
            kp = (math.log(y2) - math.log(y1)) / (t2 - t1)
            log_pop_future = math.log(y2) + kp * (t_futur - t2)
            resultats["population_estimee"] = int(math.exp(log_pop_future))
        
        else:
            raise ValueError(f"Méthode '{methode}' non implémentée.")
        
        resultats["statut"] = "OK"
        return resultats
    except Exception as e:
        return {"statut": "Erreur", "message": str(e)}
