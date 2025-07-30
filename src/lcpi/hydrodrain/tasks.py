from ...celery_app import celery_app
from .core.engine import run_dimensioning_workflow
from .core.models import Reseau
import pandas as pd

@celery_app.task(bind=True)
def run_sanitation_dimensioning_task(self, troncons_data, methode_calcul, tc_formule_name, params_pluie, v_min, v_max, verbose):
    """
    Tâche Celery pour exécuter le dimensionnement d'assainissement.
    """
    try:
        # Convert troncons_data back to pandas DataFrame
        df_input = pd.DataFrame(troncons_data)

        # Define the expected column names based on the Troncon model
        expected_column_names = [
            'id_troncon', 'type_section', 'largeur_fond_m', 'fruit_z', 'surface_ha',
            'coeff_ruissellement', 'longueur_parcours_surface_m', 'pente_parcours_surface',
            'longueur_troncon_m', 'pente_troncon', 'ks_manning_strickler', 'troncon_amont', 'z_start', 'z_end'
        ]

        # Rename columns. This assumes the order of columns in the incoming data matches the expected order.
        if len(df_input.columns) == len(expected_column_names):
            df_input.columns = expected_column_names
        else:
            raise ValueError(f"Le nombre de colonnes dans le fichier CSV ({len(df_input.columns)}) ne correspond pas au nombre attendu ({len(expected_column_names)}).")

        # Ensure 'id_troncon' and 'troncon_amont' are strings
        df_input['id_troncon'] = df_input['id_troncon'].astype(str)
        df_input['troncon_amont'] = df_input['troncon_amont'].astype(str)

        # Create Reseau object
        reseau = Reseau(df_input.copy())

        # Execute calculation
        reseau_calcule, verbose_log = run_dimensioning_workflow(
            reseau,
            methode_calcul,
            tc_formule_name,
            params_pluie,
            v_min,
            v_max,
            verbose,
        )

        # Format and return results
        df_results = pd.DataFrame([t.to_dict() for t in reseau_calcule.troncons.values()])
        results_list = df_results.to_dict(orient='records')

        return {
            'success': True,
            'message': 'Calcul d\'assainissement effectué avec succès',
            'resultat': results_list,
            'verbose_log': verbose_log
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Erreur inattendue dans le module d\'assainissement',
            'status_code': 500
        }