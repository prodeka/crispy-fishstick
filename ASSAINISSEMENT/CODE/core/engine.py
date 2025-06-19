# core/engine.py
import pandas as pd
import math
import logging
import sys, os
from io import StringIO

# Ajout du chemin pour permettre les imports depuis la racine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import Reseau
from modules.hydrologie import rationnelle, caquot
from utils.ui import print_colored

def run_dimensioning_workflow(reseau: Reseau, methode_calcul: str, tc_formule_name: str, params_pluie: dict, v_min: float, v_max: float) -> tuple:
    """
    Orchestre le dimensionnement complet du réseau, tronçon par tronçon.
    Capture également un log détaillé du premier tronçon pour le rapport.
    Vérifie les vitesses d'écoulement par rapport aux limites v_min et v_max.
    """
    logging.info(f"\n--- Lancement du dimensionnement ({len(reseau.troncons_tries)} tronçons) ---")
    
    verbose_log_capture = StringIO()
    original_stdout = sys.stdout
    captured_log_for_pdf = "" # Variable pour stocker le log pour le PDF

    for i, troncon in enumerate(reseau.troncons_tries):
        # On rend le premier tronçon "verbeux" pour le rapport
        is_verbose = (i == 0) or (len(reseau.troncons_tries) == 1)
        
        if is_verbose:
            sys.stdout = verbose_log_capture
            print_colored(f"\n({i+1}/{len(reseau.troncons_tries)}) Traitement détaillé du tronçon : {troncon.id}", "bold")

        # Agrégation des données des tronçons en amont
        if troncon.amont_ids != ['NONE']:
            try:
                troncons_amont = [reseau.troncons[am_id] for am_id in troncon.amont_ids]
                troncon.surface_cumulee = troncon.surface_ha + sum(t.surface_cumulee for t in troncons_amont)
                c_pondere_total = (troncon.coeff_ruissellement * troncon.surface_ha) + sum(t.c_moyen_cumule * t.surface_cumulee for t in troncons_amont)
                troncon.c_moyen_cumule = c_pondere_total / troncon.surface_cumulee if troncon.surface_cumulee > 0 else 0
                troncon.tc_amont_max = max(t.tc_final_min for t in troncons_amont) if any(t.tc_final_min for t in troncons_amont) else 0
                main_amont = max(troncons_amont, key=lambda t: t.longueur_cumulee)
                troncon.longueur_cumulee = main_amont.longueur_cumulee + troncon.long_troncon_m
                troncon.pentes_parcours = main_amont.pentes_parcours + [(troncon.long_troncon_m, troncon.pente_troncon)]
            except KeyError as e: raise Exception(f"Erreur de topologie : tronçon amont {e} non trouvé.")

        # Appel du module de calcul spécifique (Rationnelle ou Caquot)
        try:
            if methode_calcul == 'rationnelle':
                rationnelle.run_calcul_rationnelle(troncon, params_pluie, tc_formule_name, is_verbose)
            elif methode_calcul == 'caquot':
                caquot.run_calcul_caquot(troncon, params_pluie, tc_formule_name, is_verbose)
            
            # ***** Vérification de la vitesse si le calcul a réussi *****
            if troncon.statut == 'OK':
                vitesse_calculee = troncon.resultat_dimensionnement.get('vitesse_ms', 0)
                if vitesse_calculee < v_min:
                    troncon.statut = 'OK (Vitesse faible)'
                elif vitesse_calculee > v_max:
                    troncon.statut = 'OK (Vitesse forte)'

        except Exception as e:
            troncon.statut = f"Erreur: {e}"
            logging.error(f"Erreur lors du calcul du tronçon {troncon.id}: {e}")
        
        # Gestion de la capture du log pour l'affichage et le rapport
        if is_verbose:
            sys.stdout = original_stdout # Restaurer la sortie standard
            
            captured_log_for_pdf = verbose_log_capture.getvalue() # Stocker le log pour le PDF
            
            print(captured_log_for_pdf) # Afficher dans la console
            verbose_log_capture.seek(0)
            verbose_log_capture.truncate(0) # Vider le buffer
        else:
            logging.info(f"  - Tronçon {troncon.id}... traité.")

    verbose_log_capture.close()
    
    return reseau, captured_log_for_pdf