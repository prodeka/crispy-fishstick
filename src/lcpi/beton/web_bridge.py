from .core.materials import Beton, Acier
from .core.sections import SectionRectangulaire
from .core.design.column_design import design_rectangular_column, design_column_compression_bael
from .core.analysis.moment_calculator import calculate_beam_end_moment


def handle_column_calculation(data):
    """
    Handles a column calculation request from the API.
    Takes a dictionary of data and returns a dictionary with results.
    """
    try:
        # 1. Extract and validate data
        b = data.get('b')
        h = data.get('h')
        height = data.get('height')
        Nu = data.get('Nu')
        Mu = data.get('Mu', 0.0)
        fc28 = data.get('fc28', 25.0)
        gamma_b = data.get('gamma_b', 1.5)
        fe = data.get('fe', 500.0)
        gamma_s = data.get('gamma_s', 1.15)
        k_factor = data.get('k_factor')

        if None in [b, h, height, Nu, k_factor]:
            return {'success': False, 'error': 'Champs b, h, height, Nu, k_factor sont requis.', 'status_code': 400}

        # 2. Create objects
        beton = Beton(fc28=fc28, gamma_b=gamma_b)
        acier = Acier(fe=fe, gamma_s=gamma_s)
        section = SectionRectangulaire(b, h)

        # 3. Determine design function and args
        if Mu > 0:
            design_function = design_rectangular_column
            design_args = {
                "Nu": Nu, "Mu": Mu, "height": height, "k_factor": k_factor,
                "section": section, "beton": beton, "acier": acier,
            }
        else:
            design_function = design_column_compression_bael
            design_args = {
                "Nu": Nu, "height": height, "k_factor": k_factor,
                "section": section, "beton": beton, "acier": acier,
            }

        # 4. Execute calculation
        results = design_function(**design_args)

        if results.get("status") == "ERREUR":
            return {
                'success': False,
                'error': results.get('message', 'Erreur inconnue lors du calcul.'),
                'message': 'Calcul de poteau échoué',
                'status_code': 400
            }

        # 5. Format and return response
        proposals_formatted = []
        for p in results.get('proposals', []):
            proposals_formatted.append({
                'type': p.get('type'),
                'text': p.get('text'),
                'provided_area_cm2': round(p.get('provided_area', 0), 2),
                'num_bars': p.get('num_bars'),
                'diameter': p.get('diameter'),
                'corner_config': p.get('corner_config'),
                'face_config': p.get('face_config')
            })

        response_data = {
            'success': True,
            'message': 'Calcul de poteau effectué avec succès',
            'resultat': {
                'required_longitudinal_steel_cm2': round(results.get('required_longitudinal_steel_cm2', 0), 2),
                'status': results.get('status'),
                'proposals': proposals_formatted,
                'section_b_m': b,
                'section_h_m': h,
                'height_L_m': height,
                'Nu_MN': Nu,
                'Mu_MNm': Mu,
                'k_factor': k_factor,
                'beton_fc28_mpa': fc28,
                'acier_fe_mpa': fe,
            }
        }
        return response_data
    except Exception as e:
        # In case of unexpected error in the calculation logic
        return {
            'success': False,
            'error': str(e),
            'message': 'Erreur inattendue dans le module de calcul de poteau',
            'status_code': 500
        }

def handle_beam_calculation(data):
    """
    Handles a simplified beam calculation request from the API.
    """
    try:
        # 1. Extract and validate data
        required_fields = ['portee', 'largeur', 'hauteur', 'charge_uniforme']
        if not all(field in data for field in required_fields):
            return {'success': False, 'error': f'Champs requis manquants: {required_fields}', 'status_code': 400}

        portee = data['portee']
        largeur = data['largeur']
        hauteur = data['hauteur']
        charge_uniforme = data['charge_uniforme'] # N/m
        resistance_beton = data.get('resistance_beton', 25) # MPa
        resistance_acier = data.get('resistance_acier', 400) # MPa

        # 2. Perform calculation (simplified logic from web/app.py)
        charge_uniforme_knm = charge_uniforme / 1000
        moment_cli_MNm = calculate_beam_end_moment(charge_uniforme_knm, portee, is_end_span=True)
        moment_max_Nm = moment_cli_MNm * 1e6

        effort_tranchant = charge_uniforme * portee / 2

        fyd = resistance_acier / 1.15
        if hauteur <= 0 or fyd <= 0:
            return {'success': False, 'error': 'Hauteur and fyd must be positive.', 'status_code': 400}
        section_armature = moment_max_Nm / (0.9 * hauteur * fyd)

        if largeur <= 0 or hauteur <= 0:
            return {'success': False, 'error': 'Largeur and hauteur must be positive.', 'status_code': 400}
        contrainte_flexion = moment_max_Nm / (largeur * hauteur**2 / 6)

        resistance_beton_pa = resistance_beton * 1e6
        verification = "OK" if contrainte_flexion < (0.85 * resistance_beton_pa) else "NOK"

        # 3. Format and return response
        resultat = {
            'moment_flechissant_knm': round(moment_max_Nm / 1000, 2),
            'effort_tranchant_kn': round(effort_tranchant / 1000, 2),
            'section_armature_m2': round(section_armature, 6),
            'section_armature_cm2': round(section_armature * 10000, 2),
            'contrainte_flexion_mpa': round(contrainte_flexion / 1000000, 2),
            'resistance_beton_mpa': resistance_beton,
            'verification': verification,
            'note': "Calcul de poutre simplifie. La logique de conception complete du CLI n'est pas encore disponible pour les poutres."
        }

        return {
            'success': True,
            'resultat': resultat,
            'message': 'Calcul de poutre effectué avec succès'
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Erreur inattendue dans le module de calcul de poutre',
            'status_code': 500
        }
