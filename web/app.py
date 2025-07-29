from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os

# Ajouter le chemin vers les modules existants
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Imports des modules existants
from nanostruct.modules.assainissement.core.engine import run_dimensioning_workflow
from nanostruct.modules.assainissement.core.models import Reseau
from nanostruct.modules.assainissement.config.idf_models import DEFAULT_IDF_DATA
from nanostruct.modules.assainissement.modules.hydrologie.rationnelle import calculer_q_max_rationnelle
from nanostruct.modules.assainissement.main import run_simulation

# Import des modules béton armé et bois
from nanostruct.modules.beton_arme.ba_entry import start_ba_module
from nanostruct.modules.bois.main import main as start_bois_module

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin pour le développement

@app.route('/')
def index():
    """Page d'accueil de l'application"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Endpoint de vérification de santé de l'API"""
    return jsonify({
        'status': 'healthy',
        'message': 'API Nanostruct opérationnelle',
        'modules': ['assainissement', 'beton_arme', 'bois']
    })

# ===== ENDPOINTS ASSAINISSEMENT =====

@app.route('/api/assainissement/calcul', methods=['POST'])
def calcul_assainissement():
    """Calcul d'assainissement simple"""
    try:
        data = request.get_json()
        
        # Validation des données d'entrée
        required_fields = ['surface', 'coefficient_ruissellement', 'intensite_pluie']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        # Calcul du débit avec la formule rationnelle
        surface = data['surface']  # en m²
        coefficient = data['coefficient_ruissellement']
        intensite = data['intensite_pluie']  # en mm/h
        
        # Conversion en hectares et mm/h
        surface_ha = surface / 10000  # conversion m² vers ha
        intensite_mmh = intensite
        
        # Calcul du débit avec la formule rationnelle
        debit = calculer_q_max_rationnelle(coefficient, intensite_mmh, surface_ha, verbose=False)
        
        # Calcul du diamètre approximatif (formule simplifiée)
        diametre = (debit / 0.5) ** 0.5  # formule approximative
        
        resultat = {
            'debit_m3s': round(debit, 3),
            'debit_ls': round(debit * 1000, 1),
            'surface_ha': round(surface_ha, 2),
            'coefficient_ruissellement': coefficient,
            'intensite_pluie_mmh': intensite_mmh,
            'diametre_approximatif_m': round(diametre, 2)
        }
        
        return jsonify({
            'success': True,
            'resultat': resultat,
            'message': 'Calcul d\'assainissement effectué avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du calcul d\'assainissement'
        }), 500

@app.route('/api/assainissement/dimensionnement', methods=['POST'])
def dimensionnement_assainissement():
    """Dimensionnement complet des réseaux d'assainissement"""
    try:
        data = request.get_json()
        
        # Validation des données
        if 'debit' not in data:
            return jsonify({'error': 'Débit requis pour le dimensionnement'}), 400
        
        debit = data['debit']
        pente = data.get('pente', 0.02)
        rugosite = data.get('rugosite', 0.013)
        
        # Calcul du diamètre avec la formule de Manning
        # Q = (1/n) * A * R^(2/3) * S^(1/2)
        # Pour un écoulement plein, A = π*D²/4 et R = D/4
        
        # Résolution itérative pour trouver le diamètre
        diametre = 0.1  # diamètre initial en m
        tolerance = 0.001
        max_iterations = 50
        
        for i in range(max_iterations):
            # Calcul de l'aire et du rayon hydraulique
            aire = 3.14159 * diametre**2 / 4
            rayon_hydraulique = diametre / 4
            
            # Calcul du débit avec Manning
            debit_calcule = (1/rugosite) * aire * (rayon_hydraulique**(2/3)) * (pente**0.5)
            
            # Ajustement du diamètre
            if abs(debit_calcule - debit) < tolerance:
                break
            elif debit_calcule < debit:
                diametre *= 1.1
            else:
                diametre *= 0.9
        
        # Calcul de la vitesse
        vitesse = debit / aire
        
        dimensionnement = {
            'diametre_m': round(diametre, 3),
            'diametre_mm': round(diametre * 1000, 0),
            'vitesse_ms': round(vitesse, 2),
            'pente': pente,
            'rugosite': rugosite,
            'debit_m3s': debit
        }
        
        return jsonify({
            'success': True,
            'dimensionnement': dimensionnement,
            'message': 'Dimensionnement effectué avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du dimensionnement'
        }), 500

# ===== ENDPOINTS BÉTON ARMÉ =====

@app.route('/api/beton_arme/poteau', methods=['POST'])
def calcul_poteau_ba():
    """Calcul de poteau en béton armé"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['hauteur', 'section', 'charge_axiale', 'resistance_beton']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        hauteur = data['hauteur']
        section = data['section']
        charge_axiale = data['charge_axiale']
        resistance_beton = data['resistance_beton']
        
        # Calculs simplifiés pour poteau BA
        # Contrainte de compression
        contrainte_compression = charge_axiale / section
        
        # Calcul de l'élancement
        rayon_gyration = (section / 3.14159) ** 0.5
        elancement = hauteur / rayon_gyration
        
        # Vérification de la résistance
        resistance_caracteristique = resistance_beton * 0.85  # coefficient de sécurité
        verification = "OK" if contrainte_compression < resistance_caracteristique else "NOK"
        
        # Calcul de l'armature (simplifié)
        section_armature = max(0.01 * section, 0.0001)  # minimum 1% de la section
        
        resultat = {
            'contrainte_compression_mpa': round(contrainte_compression / 1000000, 2),
            'resistance_caracteristique_mpa': round(resistance_caracteristique / 1000000, 2),
            'elancement': round(elancement, 1),
            'verification': verification,
            'section_armature_m2': round(section_armature, 6),
            'section_armature_cm2': round(section_armature * 10000, 2)
        }
        
        return jsonify({
            'success': True,
            'resultat': resultat,
            'message': 'Calcul de poteau effectué avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du calcul de poteau'
        }), 500

@app.route('/api/beton_arme/poutre', methods=['POST'])
def calcul_poutre_ba():
    """Calcul de poutre en béton armé"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['portee', 'largeur', 'hauteur', 'charge_uniforme']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        portee = data['portee']
        largeur = data['largeur']
        hauteur = data['hauteur']
        charge_uniforme = data['charge_uniforme']
        resistance_beton = data.get('resistance_beton', 25)
        
        # Calculs de poutre BA
        # Moment fléchissant maximal (poutre simple)
        moment_max = charge_uniforme * portee**2 / 8
        
        # Effort tranchant maximal
        effort_tranchant = charge_uniforme * portee / 2
        
        # Section d'armature (simplifié)
        section_armature = moment_max / (0.9 * hauteur * 400)  # fyd = 400 MPa
        
        # Vérification de la contrainte de compression
        contrainte_compression = moment_max / (largeur * hauteur**2 / 6)
        
        resultat = {
            'moment_flechissant_knm': round(moment_max / 1000, 2),
            'effort_tranchant_kn': round(effort_tranchant / 1000, 2),
            'section_armature_m2': round(section_armature, 6),
            'section_armature_cm2': round(section_armature * 10000, 2),
            'contrainte_compression_mpa': round(contrainte_compression / 1000000, 2),
            'resistance_beton_mpa': resistance_beton
        }
        
        return jsonify({
            'success': True,
            'resultat': resultat,
            'message': 'Calcul de poutre effectué avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du calcul de poutre'
        }), 500

# ===== ENDPOINTS BOIS =====

@app.route('/api/bois/poteau', methods=['POST'])
def calcul_poteau_bois():
    """Calcul de poteau en bois"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['hauteur', 'section', 'charge_axiale', 'classe_bois']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        hauteur = data['hauteur']
        section = data['section']
        charge_axiale = data['charge_axiale']
        classe_bois = data['classe_bois']
        
        # Résistances caractéristiques selon la classe de bois
        resistances = {
            'C18': 18, 'C24': 24, 'C30': 30, 'C35': 35, 'C40': 40
        }
        
        resistance_caracteristique = resistances.get(classe_bois, 24)
        
        # Calculs pour poteau bois
        contrainte_compression = charge_axiale / section
        
        # Calcul de l'élancement
        rayon_gyration = (section / 3.14159) ** 0.5
        elancement = hauteur / rayon_gyration
        
        # Vérification de la résistance
        verification = "OK" if contrainte_compression < resistance_caracteristique else "NOK"
        
        resultat = {
            'contrainte_compression_mpa': round(contrainte_compression / 1000000, 2),
            'resistance_caracteristique_mpa': resistance_caracteristique,
            'elancement': round(elancement, 1),
            'verification': verification,
            'classe_bois': classe_bois
        }
        
        return jsonify({
            'success': True,
            'resultat': resultat,
            'message': 'Calcul de poteau bois effectué avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du calcul de poteau bois'
        }), 500

@app.route('/api/bois/poutre', methods=['POST'])
def calcul_poutre_bois():
    """Calcul de poutre en bois"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['portee', 'largeur', 'hauteur', 'charge_uniforme', 'classe_bois']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        portee = data['portee']
        largeur = data['largeur']
        hauteur = data['hauteur']
        charge_uniforme = data['charge_uniforme']
        classe_bois = data['classe_bois']
        
        # Résistances caractéristiques selon la classe de bois
        resistances = {
            'C18': 18, 'C24': 24, 'C30': 30, 'C35': 35, 'C40': 40
        }
        
        resistance_caracteristique = resistances.get(classe_bois, 24)
        
        # Calculs de poutre bois
        moment_max = charge_uniforme * portee**2 / 8
        effort_tranchant = charge_uniforme * portee / 2
        
        # Contrainte de flexion
        contrainte_flexion = moment_max / (largeur * hauteur**2 / 6)
        
        # Vérification
        verification = "OK" if contrainte_flexion < resistance_caracteristique else "NOK"
        
        resultat = {
            'moment_flechissant_knm': round(moment_max / 1000, 2),
            'effort_tranchant_kn': round(effort_tranchant / 1000, 2),
            'contrainte_flexion_mpa': round(contrainte_flexion / 1000000, 2),
            'resistance_caracteristique_mpa': resistance_caracteristique,
            'verification': verification,
            'classe_bois': classe_bois
        }
        
        return jsonify({
            'success': True,
            'resultat': resultat,
            'message': 'Calcul de poutre bois effectué avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du calcul de poutre bois'
        }), 500

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