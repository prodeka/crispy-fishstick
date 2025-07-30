# core/engine.py
import logging
import sys
import os
from io import StringIO

# Ajout du chemin racine pour permettre les imports inter-modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .models import Reseau
from ..modules.hydrologie import rationnelle, caquot
from ..utils.ui import print_colored


def run_dimensioning_workflow(
    reseau: Reseau,
    methode_calcul: str,
    tc_formule_name: str,
    params_pluie: dict,
    v_min: float,
    v_max: float,
    verbose: bool = False,
) -> tuple:
    """
    Orchestre le dimensionnement complet du réseau, tronçon par tronçon.
    Le paramètre 'verbose' contrôle l'affichage détaillé des calculs.
    """
    if verbose:
        logging.info(
            f"\n--- Lancement du dimensionnement en MODE VERBEUX ({len(reseau.troncons_tries)} tronçons) ---"
        )
    else:
        logging.info(
            f"\n--- Lancement du dimensionnement ({len(reseau.troncons_tries)} tronçons) ---"
        )

    verbose_log_capture = StringIO()
    original_stdout = sys.stdout
    captured_log_for_pdf = ""

    for i, troncon in enumerate(reseau.troncons_tries):
        # En mode verbose, on détaille tout. Sinon, seulement le premier pour le rapport.
        is_verbose_for_troncon = verbose or (i == 0)

        if is_verbose_for_troncon:
            sys.stdout = verbose_log_capture
            print_colored(
                f"\n({i + 1}/{len(reseau.troncons_tries)}) Traitement détaillé du tronçon : {troncon.id}",
                "bold",
            )

        # Agrégation des données des tronçons en amont
        if troncon.amont_ids != ["NONE"]:
            try:
                troncons_amont = [reseau.troncons[am_id] for am_id in troncon.amont_ids]
                troncon.surface_cumulee = troncon.surface_ha + sum(
                    t.surface_cumulee for t in troncons_amont
                )
                c_pondere_total = (
                    troncon.coeff_ruissellement * troncon.surface_ha
                ) + sum(t.c_moyen_cumule * t.surface_cumulee for t in troncons_amont)
                troncon.c_moyen_cumule = (
                    c_pondere_total / troncon.surface_cumulee
                    if troncon.surface_cumulee > 0
                    else 0
                )
                troncon.tc_amont_max = (
                    max(t.tc_final_min for t in troncons_amont)
                    if any(t.tc_final_min for t in troncons_amont)
                    else 0
                )
                main_amont = max(troncons_amont, key=lambda t: t.longueur_cumulee)
                troncon.longueur_cumulee = (
                    main_amont.longueur_cumulee + troncon.long_troncon_m
                )
                troncon.pentes_parcours = main_amont.pentes_parcours + [
                    (troncon.long_troncon_m, troncon.pente_troncon)
                ]
            except KeyError as e:
                raise Exception(
                    f"Erreur de topologie : tronçon amont {e} non trouvé pour le tronçon {troncon.id}."
                )

        # Appel du module de calcul spécifique (Rationnelle ou Caquot)
        try:
            if methode_calcul == "rationnelle":
                rationnelle.run_calcul_rationnelle(
                    troncon, params_pluie, tc_formule_name, is_verbose_for_troncon
                )
            elif methode_calcul == "caquot":
                caquot.run_calcul_caquot(
                    troncon, params_pluie, tc_formule_name, is_verbose_for_troncon
                )

            # Vérification de la vitesse si le calcul a réussi
            if (
                not troncon.statut.startswith("Erreur")
                and troncon.statut != "Non-convergence"
            ):
                vitesse_calculee = troncon.resultat_dimensionnement.get("vitesse_ms", 0)
                if vitesse_calculee < v_min:
                    troncon.statut = "OK (Vitesse faible)"
                elif vitesse_calculee > v_max:
                    troncon.statut = "OK (Vitesse forte)"
                else:
                    troncon.statut = "OK"
        except Exception as e:
            troncon.statut = f"Erreur: {e}"
            logging.error(
                f"Erreur critique lors du calcul du tronçon {troncon.id}: {e}",
                exc_info=True,
            )

        # Gestion de la capture du log pour l'affichage et le rapport PDF
        if is_verbose_for_troncon:
            sys.stdout = original_stdout  # Restaurer la sortie standard pour voir les logs dans la console

            log_content = verbose_log_capture.getvalue()

            # On ne garde que le log du tout premier tronçon pour le rapport PDF
            if i == 0:
                captured_log_for_pdf = log_content

            print(log_content)  # Afficher ce qui a été capturé
            verbose_log_capture.seek(0)
            verbose_log_capture.truncate(
                0
            )  # Vider le buffer pour la prochaine itération verbeuse
        else:
            logging.info(f"  - Tronçon {troncon.id}... traité.")

    verbose_log_capture.close()

    return reseau, captured_log_for_pdf
