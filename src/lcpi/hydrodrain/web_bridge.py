from .tasks import run_sanitation_dimensioning_task

def handle_sanitation_calculation(data):
    """
    Handles a sanitation calculation request from the API by launching a Celery task.
    """
    try:
        # 1. Extract and validate data
        required_fields = [
            'troncons_data', 'methode_calcul', 'tc_formule_name',
            'params_pluie', 'v_min', 'v_max', 'verbose'
        ]
        if not all(field in data for field in required_fields):
            missing_fields = [field for field in required_fields if field not in data]
            return {
                'success': False,
                'error': f'Champs requis manquants: {", ".join(missing_fields)}',
                'status_code': 400
            }

        troncons_data = data['troncons_data']
        methode_calcul = data['methode_calcul']
        tc_formule_name = data['tc_formule_name']
        params_pluie = data['params_pluie']
        v_min = data['v_min']
        v_max = data['v_max']
        verbose = data['verbose']

        # Launch Celery task
        task = run_sanitation_dimensioning_task.delay(
            troncons_data,
            methode_calcul,
            tc_formule_name,
            params_pluie,
            v_min,
            v_max,
            verbose
        )

        return {
            'success': True,
            'message': 'Calcul d\'assainissement lancé avec succès',
            'task_id': task.id,
            'status_code': 202 # Accepted
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Erreur inattendue lors du lancement du calcul d\'assainissement',
            'status_code': 500
        }