from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import csv
import io

# Ajouter le chemin vers les modules existants
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from nanostruct.modules.assainissement.web_bridge import handle_sanitation_calculation
from nanostruct.modules.beton_arme.web_bridge import handle_column_calculation, handle_beam_calculation
from nanostruct.modules.bois.web_bridge import handle_wood_beam_calculation, handle_wood_column_calculation

# Import Celery app
from nanostruct.celery_app import celery_app

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin pour le développement

@app.route('/')
def home():
    """Page d'accueil de l'application"""
    return render_template('home.html')

@app.route('/assainissement')
def assainissement_page():
    """Page du module Assainissement"""
    return render_template('assainissement.html')

@app.route('/beton_arme')
def beton_arme_page():
    """Page du module Béton Armé"""
    return render_template('beton_arme.html')

@app.route('/bois')
def bois_page():
    """Page du module Bois"""
    return render_template('bois.html')

@app.route('/api/health')
def health_check():
    """Endpoint de vérification de santé de l'API"""
    return jsonify({
        'status': 'healthy',
        'message': 'API Nanostruct opérationnelle',
        'modules': ['assainissement', 'beton_arme', 'bois']
    })

# ===== ENDPOINTS ASSAINISSEMENT =====

@app.route('/api/assainissement/calcul_complet', methods=['POST'])
def calcul_assainissement():
    """Lance le calcul d'assainissement en tant que tâche Celery.
    Accepte un fichier CSV et d'autres paramètres via FormData.
    """
    if 'csv_file' not in request.files:
        return jsonify({'success': False, 'error': 'Aucun fichier CSV fourni.'}), 400

    csv_file = request.files['csv_file']
    if csv_file.filename == '':
        return jsonify({'success': False, 'error': 'Nom de fichier CSV vide.'}), 400

    if csv_file:
        csv_content = csv_file.read().decode('utf-8')
        delimiter = request.form.get('delimiter', ',')

        # Simple parsing of CSV content into a list of dicts
        csv_data = []
        # Use StringIO to treat the string content as a file
        csv_file_stream = io.StringIO(csv_content)
        reader = csv.reader(csv_file_stream, delimiter=delimiter)
        headers = [h.strip() for h in next(reader)] # Read headers
        for row in reader:
            if not row: # Skip empty rows
                continue
            row_data = {}
            for i, header in enumerate(headers):
                if i < len(row):
                    row_data[header] = row[i].strip()
                else:
                    row_data[header] = '' # Handle missing values
            csv_data.append(row_data)

        # Extract other form data
        methode_calcul = request.form.get('methode_calcul')
        tc_formule_name = request.form.get('tc_formule_name')
        v_min = float(request.form.get('v_min'))
        v_max = float(request.form.get('v_max'))
        idf_a = float(request.form.get('idf_a'))
        idf_b = float(request.form.get('idf_b'))
        periode_retour = int(request.form.get('periode_retour'))
        verbose = request.form.get('verbose') == 'true' # Checkbox value from JS is 'true' or 'false'

        params_pluie = {
            "formula": "montana",
            "periode_retour": periode_retour,
            "nom": f"Manuel T={periode_retour} ans",
            "a": idf_a,
            "b": idf_b
        }

        data_for_calculation = {
            'troncons_data': csv_data,
            'methode_calcul': methode_calcul,
            'tc_formule_name': tc_formule_name,
            'params_pluie': params_pluie,
            'v_min': v_min,
            'v_max': v_max,
            'verbose': verbose
        }

        result = handle_sanitation_calculation(data_for_calculation)

        if not result.get('success'):
            return jsonify(result), result.get('status_code', 500)

        return jsonify(result)

# New endpoint to check task status
@app.route('/api/calcul/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = celery_app.AsyncResult(task_id)
    response = {
        'state': task.state,
        'status': task.status,
    }
    if task.state == 'PENDING':
        response['message'] = 'La tâche est en attente.'
    elif task.state == 'PROGRESS':
        response['message'] = 'La tâche est en cours...'
    elif task.state == 'SUCCESS':
        response['message'] = 'La tâche a été complétée avec succès.'
        response['result'] = task.result
    elif task.state == 'FAILURE':
        response['message'] = 'La tâche a échoué.'
        response['error'] = str(task.info)
    return jsonify(response)


# ===== ENDPOINTS BÉTON ARMÉ =====

@app.route('/api/beton_arme/poteau', methods=['POST'])
def calcul_poteau_ba():
    """Calcul de poteau en béton armé en utilisant la logique CLI."""
    data = request.get_json()
    result = handle_column_calculation(data)

    if not result.get('success'):
        return jsonify(result), result.get('status_code', 500)

    return jsonify(result)

@app.route('/api/beton_arme/poutre', methods=['POST'])
def calcul_poutre_ba():
    """Calcul de poutre en béton armé en utilisant la logique CLI (partielle)."""
    data = request.get_json()
    result = handle_beam_calculation(data)

    if not result.get('success'):
        return jsonify(result), result.get('status_code', 500)

    return jsonify(result)

# ===== ENDPOINTS BOIS =====

@app.route('/api/bois/poteau', methods=['POST'])
def calcul_poteau_bois():
    """Calcul de poteau en bois en utilisant la logique CLI."""
    data = request.get_json()
    result = handle_wood_column_calculation(data)

    if not result.get('success'):
        return jsonify(result), result.get('status_code', 500)

    return jsonify(result)

@app.route('/api/bois/poutre', methods=['POST'])
def calcul_poutre_bois():
    """Calcul de poutre en bois en utilisant la logique CLI."""
    data = request.get_json()
    result = handle_wood_beam_calculation(data)

    if not result.get('success'):
        return jsonify(result), result.get('status_code', 500)

    return jsonify(result)

# ===== ENDPOINTS UTILITAIRES =====

@app.route('/api/assainissement/coefficients', methods=['GET'])
def get_coefficients_assainissement():
    """Récupère les coefficients de ruissellement disponibles"""
    coefficients = {
        'toiture': 0.9,
        'route_asphalte': 0.9,
        'route_graveleuse': 0.4,
        'terrain_herbe': 0.2,
        'terrain_boise': 0.1
    }
    return jsonify(coefficients)

@app.route('/api/beton_arme/classes', methods=['GET'])
def get_classes_beton():
    """Récupère les classes de résistance du béton"""
    classes = ['C20/25', 'C25/30', 'C30/37', 'C35/45', 'C40/50']
    return jsonify(classes)

@app.route('/api/bois/classes', methods=['GET'])
def get_classes_bois():
    """Récupère les classes de bois disponibles"""
    classes = ['C18', 'C24', 'C30', 'C35', 'C40']
    return jsonify(classes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)