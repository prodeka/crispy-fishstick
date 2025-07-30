def caracteriser_bassin(donnees_entree: dict):
    # Placeholder pour la délimitation SIG et le calcul des paramètres
    s = donnees_entree.get("superficie_km2", 50.0) # Valeur exemple
    p = 35.0 # Valeur exemple
    kc = 0.282 * p * (s**-0.5)
    # ... autres calculs ...
    print("Caractérisation du bassin versant...")
    return {"statut": "OK", "superficie_km2": s, "perimetre_km": p, "indice_gravelius_kc": round(kc, 2)}
    
def estimer_crue(donnees_bassin: dict, methode: str = "orstom"):
    # Placeholder pour l'estimation de crue (les vraies formules sont dans hydrologie.py)
    # Cet appel pourrait être délégué
    print(f"Estimation de la crue par la méthode {methode}...")
    q10 = 250.0 # m3/s, valeur exemple
    q100 = 2 * q10 # ASEER
    return {"statut": "OK", "debit_decennal_q10_m3s": q10, "debit_projet_q100_m3s": q100}
