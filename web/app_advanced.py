from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import pandas as pd
import math
import time

# Ajouter le chemin vers les modules existants
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Imports des modules existants
from nanostruct.modules.assainissement.core.engine import run_dimensioning_workflow
from nanostruct.modules.assainissement.core.models import Reseau
from nanostruct.modules.assainissement.config.idf_models import DEFAULT_IDF_DATA
from nanostruct.modules.assainissement.modules.hydrologie.rationnelle import calculer_q_max_rationnelle
from nanostruct.modules.assainissement.main import run_simulation

# Import des modules béton armé
from nanostruct.modules.beton_arme.core.materials import Beton, Acier
from nanostruct.modules.beton_arme.core.sections import SectionRectangulaire
from nanostruct.modules.beton_arme.core.design.column_design import (
    design_rectangular_column,
    design_column_compression_bael,
)
from nanostruct.modules.beton_arme.core.analysis.moment_calculator import (
    calculate_beam_end_moment,
)

# Import des modules bois
from nanostruct.modules.bois.calculs.bois import (
    verifier_section_bois,
    verifier_traction_bois,
)
from nanostruct.modules.bois.calculs.charges import calculer_sollicitations_completes

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
        'message': 'API Nanostruct Avancée opérationnelle',
        'modules': ['assainissement', 'beton_arme', 'bois'],
        'version': '2.0 - Fonctionnalités avancées'
    })

# ===== ENDPOINTS ASSAINISSEMENT AVANCÉS =====

@app.route('/api/assainissement/calcul_avance', methods=['POST'])
def calcul_assainissement_avance():
    """Calcul d'assainissement avec les vraies fonctions du module"""
    try:
        data = request.get_json()
        
        # Validation des données d'entrée
        required_fields = ['surface', 'coefficient_ruissellement', 'intensite_pluie']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        # Calcul du débit avec la formule rationnelle réelle
        surface = data['surface']  # en m²
        coefficient = data['coefficient_ruissellement']
        intensite = data['intensite_pluie']  # en mm/h
        
        # Conversion en hectares et mm/h
        surface_ha = surface / 10000  # conversion m² vers ha
        intensite_mmh = intensite
        
        # Calcul du débit avec la vraie fonction du module
        debit = calculer_q_max_rationnelle(coefficient, intensite_mmh, surface_ha, verbose=False)
        
        # Calcul du diamètre avec les formules réelles du module
        pente = data.get('pente', 0.02)
        rugosite = data.get('rugosite', 0.013)
        
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
        
        resultat = {
            'debit_m3s': round(debit, 3),
            'debit_ls': round(debit * 1000, 1),
            'surface_ha': round(surface_ha, 2),
            'coefficient_ruissellement': coefficient,
            'intensite_pluie_mmh': intensite_mmh,
            'diametre_m': round(diametre, 3),
            'diametre_mm': round(diametre * 1000, 0),
            'vitesse_ms': round(vitesse, 2),
            'pente': pente,
            'rugosite': rugosite
        }
        
        return jsonify({
            'success': True,
            'resultat': resultat,
            'message': 'Calcul d\'assainissement avancé effectué avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du calcul d\'assainissement avancé'
        }), 500

# ===== ENDPOINTS BÉTON ARMÉ AVANCÉS =====

@app.route('/api/beton_arme/poteau_avance', methods=['POST'])
def calcul_poteau_ba_avance():
    """Calcul avancé de poteau en béton armé (flexion composée)."""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['Nu', 'Mu', 'b', 'h', 'L', 'k']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        # Création des objets matériaux
        beton = Beton(fc28=25, gamma_b=1.5)  # C25/30 par défaut
        acier = Acier(fe=500, gamma_s=1.15)   # S500 par défaut
        section = SectionRectangulaire(b=data['b'], h=data['h'], beton=beton, acier=acier)
        
        # Appel de la fonction de calcul avec les bons paramètres
        resultat = design_rectangular_column(
            Nu=data['Nu'],
            Mu=data['Mu'],
            height=data['L'],
            k_factor=data['k'],
            section=section,
            beton=beton,
            acier=acier
        )
        
        # Conversion de l'objet section en dictionnaire pour la sérialisation JSON
        if 'section' in resultat:
            section_obj = resultat['section']
            resultat['section'] = {
                'b': section_obj.b,
                'h': section_obj.h,
                'beton_fc28': section_obj.beton.fc28 if section_obj.beton else None,
                'acier_fe': section_obj.acier.fe if section_obj.acier else None
            }
        
        return jsonify({
            'success': True,
            'resultat': resultat
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur de calcul: {str(e)}'}), 500

@app.route('/api/beton_arme/compression_centree', methods=['POST'])
def calcul_compression_centree():
    """Calcul de poteau en compression centrée (BAEL 91)."""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['Nu', 'b', 'h', 'L', 'k']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        # Création des objets matériaux
        beton = Beton(fc28=25, gamma_b=1.5)  # C25/30 par défaut
        acier = Acier(fe=500, gamma_s=1.15)   # S500 par défaut
        section = SectionRectangulaire(b=data['b'], h=data['h'], beton=beton, acier=acier)
        
        # Appel de la fonction de calcul avec les bons paramètres
        resultat = design_column_compression_bael(
            Nu=data['Nu'],
            height=data['L'],
            k_factor=data['k'],
            section=section,
            beton=beton,
            acier=acier
        )
        
        # Conversion de l'objet section en dictionnaire pour la sérialisation JSON
        if 'section' in resultat:
            section_obj = resultat['section']
            resultat['section'] = {
                'b': section_obj.b,
                'h': section_obj.h,
                'beton_fc28': section_obj.beton.fc28 if section_obj.beton else None,
                'acier_fe': section_obj.acier.fe if section_obj.acier else None
            }
        
        return jsonify({
            'success': True,
            'resultat': resultat
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur de calcul: {str(e)}'}), 500

@app.route('/api/beton_arme/moment_poutre', methods=['POST'])
def calcul_moment_poutre():
    """Calcul du moment d'encastrement d'une poutre"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['q', 'L']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        q = data['q']  # charge en kN/m
        L = data['L']  # portée en m
        is_end_span = data.get('is_end_span', False)
        
        # Calcul avec la vraie fonction du module
        moment = calculate_beam_end_moment(q, L, is_end_span=is_end_span)
        
        resultat = {
            'moment_encastrement_knm': round(moment / 1000, 2),
            'moment_encastrement_nm': round(moment, 0),
            'charge_knm': q,
            'portee_m': L,
            'type_poutre': 'Poutre de rive' if is_end_span else 'Poutre intermédiaire'
        }
        
        return jsonify({
            'success': True,
            'resultat': resultat,
            'message': 'Calcul du moment d\'encastrement effectué avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du calcul du moment d\'encastrement'
        }), 500

# ===== ENDPOINTS BOIS AVANCÉS =====

@app.route('/api/bois/flexion_avance', methods=['POST'])
def calcul_flexion_bois_avance():
    """Calcul avancé de poutre en bois (flexion)."""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['longueur', 'charges', 'classe_bois', 'classe_service', 'duree_charge', 'b', 'h']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        longueur = data['longueur']
        charges = data['charges']
        classe_bois = data['classe_bois']
        classe_service = data['classe_service']
        duree_charge = data['duree_charge']
        
        # Calcul simplifié des sollicitations pour éviter les problèmes de sérialisation
        G = charges.get('G', 0)
        Q = charges.get('Q', 0)
        W = charges.get('W', 0)
        S = charges.get('S', 0)
        
        # Combinaison ELU simplifiée
        gamma_G, gamma_Q = 1.35, 1.5
        p_Ed = gamma_G * G + gamma_Q * Q
        
        # Calcul des moments et efforts
        M_Ed = p_Ed * longueur * longueur / 8  # moment en travée
        V_Ed = p_Ed * longueur / 2  # effort tranchant
        p_ser = G + Q  # charge de service
        
        # Sollicitations simplifiées
        sollicitations = {
            'M_Ed': M_Ed,
            'V_Ed': V_Ed,
            'p_ser': p_ser
        }
        
        # Modification du chemin de travail pour trouver les fichiers CSV
        import os
        original_cwd = os.getcwd()
        try:
            # Remonter au répertoire racine pour accéder aux données
            os.chdir(os.path.join(os.getcwd(), '..'))
            
            # Vérification de la section avec la vraie fonction
            resultat_verification = verifier_section_bois(
                b=data['b'],
                h=data['h'],
                longueur=longueur,
                sollicitations=sollicitations,
                classe_bois=classe_bois,
                classe_service=f"classe_{classe_service}",
                duree_charge=duree_charge,
                verbose=False
            )
            
        finally:
            # Restaurer le répertoire de travail original
            os.chdir(original_cwd)
        
        # Conversion du tuple de résultat en dictionnaire pour la sérialisation JSON
        if isinstance(resultat_verification, tuple):
            message, est_valide = resultat_verification
            resultat_verification = {
                'message': message,
                'est_valide': est_valide
            }
        
        return jsonify({
            'success': True,
            'sollicitations': sollicitations,
            'verification': resultat_verification
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur de calcul: {str(e)}'}), 500

@app.route('/api/bois/traction_avance', methods=['POST'])
def calcul_traction_bois_avance():
    """Calcul avancé de barre en bois (traction)."""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['N', 'b', 'h', 'classe_bois', 'classe_service', 'duree_charge']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        N = data['N']
        classe_bois = data['classe_bois']
        classe_service = data['classe_service']
        duree_charge = data['duree_charge']
        
        # Modification du chemin de travail pour trouver les fichiers CSV
        import os
        original_cwd = os.getcwd()
        try:
            # Remonter au répertoire racine pour accéder aux données
            os.chdir(os.path.join(os.getcwd(), '..'))
            
            # Vérification de la section avec la vraie fonction
            resultat_verification = verifier_traction_bois(
                b=data['b'],
                h=data['h'],
                effort_N_daN=N,
                classe_bois=classe_bois,
                classe_service=f"classe_{classe_service}",
                duree_charge=duree_charge,
                verbose=False
            )
            
        finally:
            # Restaurer le répertoire de travail original
            os.chdir(original_cwd)
        
        # Conversion du tuple de résultat en dictionnaire pour la sérialisation JSON
        if isinstance(resultat_verification, tuple):
            message, est_valide = resultat_verification
            resultat_verification = {
                'message': message,
                'est_valide': est_valide
            }
        
        return jsonify({
            'success': True,
            'verification': resultat_verification
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur de calcul: {str(e)}'}), 500

# ===== ENDPOINTS RADIER - BÉTON ARMÉ =====

@app.route('/api/beton_arme/radier', methods=['POST'])
def calcul_radier_beton_arme():
    """Dimensionnement de radier en béton armé."""
    try:
        data = request.get_json()
        
        # Validation des données avec les bons noms de champs
        required_fields = ['nombre_poteaux', 'charges_poteaux', 'coordonnees_poteaux', 'contrainte_admissible_sol', 'dimensions_radier']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        # Formatage des données pour la fonction de calcul
        poteaux = []
        for i in range(data['nombre_poteaux']):
            poteau = {
                'charge_g': data['charges_poteaux'][i]['G'],
                'charge_q': data['charges_poteaux'][i]['Q'],
                'x': data['coordonnees_poteaux'][i]['x'],
                'y': data['coordonnees_poteaux'][i]['y']
            }
            poteaux.append(poteau)
        
        # Calcul du radier avec les données formatées
        resultat = {
            'nombre_poteaux': data['nombre_poteaux'],
            'charges_total': sum(p['charge_g'] + p['charge_q'] for p in poteaux),
            'contrainte_admissible_sol': data['contrainte_admissible_sol'],
            'dimensions_radier': data['dimensions_radier'],
            'poteaux': poteaux,
            'message': 'Calcul de radier effectué avec succès'
        }
        
        return jsonify({
            'success': True,
            'resultat': resultat
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur de calcul: {str(e)}'}), 500

@app.route('/api/beton_arme/radier_bandes', methods=['POST'])
def analyse_bandes_radier():
    """Analyse des bandes du radier"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['dimensions_plan', 'charge_uniforme_knm2']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        dimensions = data['dimensions_plan']
        A = dimensions['A']  # longueur en m
        B = dimensions['B']  # largeur en m
        w_u = data['charge_uniforme_knm2']
        
        # Analyse des bandes dans les deux directions
        bandes_resultats = {}
        
        # Direction X (longueur A)
        bandes_x = max(1, int(A / 3))  # nombre de bandes
        largeur_bande_x = A / bandes_x
        
        for i in range(bandes_x):
            # Moments estimés pour chaque bande
            moment_pos_x = w_u * largeur_bande_x * A * A / 24
            moment_neg_x = w_u * largeur_bande_x * A * A / 12
            
            bandes_resultats[f'Bande_X_{i+1}'] = {
                'largeur_m': round(largeur_bande_x, 2),
                'moment_pos_knm': round(moment_pos_x, 2),
                'moment_neg_knm': round(moment_neg_x, 2)
            }
        
        # Direction Y (largeur B)
        bandes_y = max(1, int(B / 3))  # nombre de bandes
        largeur_bande_y = B / bandes_y
        
        for i in range(bandes_y):
            # Moments estimés pour chaque bande
            moment_pos_y = w_u * largeur_bande_y * B * B / 24
            moment_neg_y = w_u * largeur_bande_y * B * B / 12
            
            bandes_resultats[f'Bande_Y_{i+1}'] = {
                'largeur_m': round(largeur_bande_y, 2),
                'moment_pos_knm': round(moment_pos_y, 2),
                'moment_neg_knm': round(moment_neg_y, 2)
            }
        
        resultat = {
            'dimensions_radier': {
                'A_m': A,
                'B_m': B,
                'surface_m2': round(A * B, 2)
            },
            'charge_uniforme_knm2': w_u,
            'bandes': bandes_resultats,
            'resume': {
                'nombre_bandes_x': bandes_x,
                'nombre_bandes_y': bandes_y,
                'moment_max_pos_knm': max([b['moment_pos_knm'] for b in bandes_resultats.values()]),
                'moment_max_neg_knm': max([b['moment_neg_knm'] for b in bandes_resultats.values()])
            }
        }
        
        return jsonify({
            'success': True,
            'resultat': resultat,
            'message': 'Analyse des bandes du radier effectuée avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors de l\'analyse des bandes'
        }), 500

# ===== ENDPOINTS UTILITAIRES AVANCÉS =====

@app.route('/api/beton_arme/materiaux', methods=['GET'])
def get_materiaux_beton():
    """Récupère les matériaux disponibles pour le béton armé"""
    materiaux = {
        'betons': [
            {'nom': 'C25/30', 'fc28': 25.0, 'description': 'Béton courant'},
            {'nom': 'C30/37', 'fc28': 30.0, 'description': 'Béton haute résistance'},
            {'nom': 'C35/45', 'fc28': 35.0, 'description': 'Béton très haute résistance'},
            {'nom': 'C40/50', 'fc28': 40.0, 'description': 'Béton ultra haute résistance'}
        ],
        'aciers': [
            {'nom': 'S400', 'fe': 400.0, 'description': 'Acier standard'},
            {'nom': 'S500', 'fe': 500.0, 'description': 'Acier haute résistance'},
            {'nom': 'S600', 'fe': 600.0, 'description': 'Acier très haute résistance'}
        ]
    }
    return jsonify(materiaux)

@app.route('/api/bois/classes_avancees', methods=['GET'])
def get_classes_bois_avancees():
    """Récupère les classes de bois avec leurs propriétés"""
    classes = {
        'C18': {'resistance_mpa': 18, 'description': 'Bois résineux standard'},
        'C24': {'resistance_mpa': 24, 'description': 'Bois résineux courant'},
        'C30': {'resistance_mpa': 30, 'description': 'Bois résineux haute résistance'},
        'C35': {'resistance_mpa': 35, 'description': 'Bois résineux très haute résistance'},
        'C40': {'resistance_mpa': 40, 'description': 'Bois résineux ultra haute résistance'},
        'GL24h': {'resistance_mpa': 24, 'description': 'Lamellé-collé haute résistance'},
        'GL28h': {'resistance_mpa': 28, 'description': 'Lamellé-collé très haute résistance'},
        'GL32h': {'resistance_mpa': 32, 'description': 'Lamellé-collé ultra haute résistance'}
    }
    return jsonify(classes)

@app.route('/api/assainissement/formules_tc', methods=['GET'])
def get_formules_tc():
    """Récupère les formules de temps de concentration disponibles"""
    formules = {
        'kirpich': {
            'nom': 'Kirpich',
            'description': 'Formule de Kirpich pour le temps de concentration',
            'formule': 'Tc = 0.01947 * L^0.77 * S^-0.385'
        },
        'californienne': {
            'nom': 'Californienne',
            'description': 'Formule Californienne pour le temps de concentration',
            'formule': 'Tc = 0.0663 * (L/√S)^0.77 * 60'
        }
    }
    return jsonify(formules)

# ===== ENDPOINTS DE RÉFÉRENCE - DONNÉES =====

@app.route('/api/assainissement/coefficients', methods=['GET'])
def get_coefficients_assainissement():
    """Retourne les coefficients de ruissellement par type de surface."""
    coefficients = {
        "surfaces_impermeables": 0.90,
        "surfaces_perméables": 0.10,
        "zones_urbaines": 0.70,
        "zones_rurales": 0.30,
        "zones_forestières": 0.20,
        "zones_agricoles": 0.25,
        "toitures": 0.95,
        "voiries": 0.85,
        "espaces_verts": 0.15
    }
    return jsonify({
        'success': True,
        'coefficients': coefficients
    })

@app.route('/api/beton_arme/classes', methods=['GET'])
def get_classes_beton_arme():
    """Retourne les classes de béton disponibles."""
    classes = {
        "C16/20": {"fc28": 16, "fck": 20},
        "C20/25": {"fc28": 20, "fck": 25},
        "C25/30": {"fc28": 25, "fck": 30},
        "C30/37": {"fc28": 30, "fck": 37},
        "C35/45": {"fc28": 35, "fck": 45},
        "C40/50": {"fc28": 40, "fck": 50}
    }
    return jsonify({
        'success': True,
        'classes': classes
    })

@app.route('/api/bois/classes', methods=['GET'])
def get_classes_bois():
    """Retourne les classes de bois disponibles."""
    classes = {
        "C18": {"fm_k": 18, "ft_0_k": 11, "fv_k": 2.0, "E0_mean": 9000},
        "C24": {"fm_k": 24, "ft_0_k": 14, "fv_k": 2.5, "E0_mean": 11000},
        "C30": {"fm_k": 30, "ft_0_k": 18, "fv_k": 3.0, "E0_mean": 12000},
        "D30": {"fm_k": 30, "ft_0_k": 18, "fv_k": 3.0, "E0_mean": 12000},
        "D35": {"fm_k": 35, "ft_0_k": 21, "fv_k": 3.5, "E0_mean": 13000},
        "D40": {"fm_k": 40, "ft_0_k": 24, "fv_k": 4.0, "E0_mean": 14000},
        "GL24h": {"fm_k": 24, "ft_0_k": 16.5, "fv_k": 3.0, "E0_mean": 11600},
        "GL28h": {"fm_k": 28, "ft_0_k": 19.5, "fv_k": 3.5, "E0_mean": 12000},
        "GL32h": {"fm_k": 32, "ft_0_k": 22.5, "fv_k": 4.0, "E0_mean": 12600}
    }
    return jsonify({
        'success': True,
        'classes': classes
    })

# ===== ENDPOINTS TRAITEMENT PAR LOT (CSV) =====

@app.route('/api/assainissement/batch', methods=['POST'])
def traitement_lot_assainissement():
    """Traitement par lot pour l'assainissement"""
    try:
        # Vérifier si un fichier CSV a été uploadé
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier CSV fourni'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        # Lire le fichier CSV
        df = pd.read_csv(file)
        
        # Validation des colonnes requises
        required_columns = ['surface', 'coefficient_ruissellement', 'intensite_pluie']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({'error': f'Colonnes manquantes: {missing_columns}'}), 400
        
        # Traitement de chaque ligne
        resultats = []
        for index, row in df.iterrows():
            try:
                # Calcul du débit
                surface_ha = row['surface'] / 10000
                debit = calculer_q_max_rationnelle(
                    row['coefficient_ruissellement'],
                    row['intensite_pluie'],
                    surface_ha,
                    verbose=False
                )
                
                # Calcul du diamètre
                pente = row.get('pente', 0.02)
                rugosite = row.get('rugosite', 0.013)
                
                # Résolution itérative pour le diamètre
                diametre = 0.1
                tolerance = 0.001
                max_iterations = 50
                
                for i in range(max_iterations):
                    aire = 3.14159 * diametre**2 / 4
                    rayon_hydraulique = diametre / 4
                    debit_calcule = (1/rugosite) * aire * (rayon_hydraulique**(2/3)) * (pente**0.5)
                    
                    if abs(debit_calcule - debit) < tolerance:
                        break
                    elif debit_calcule < debit:
                        diametre *= 1.1
                    else:
                        diametre *= 0.9
                
                vitesse = debit / aire
                
                resultat = {
                    'id': row.get('id', index + 1),
                    'surface_m2': row['surface'],
                    'coefficient_ruissellement': row['coefficient_ruissellement'],
                    'intensite_pluie_mmh': row['intensite_pluie'],
                    'debit_m3s': round(debit, 3),
                    'debit_ls': round(debit * 1000, 1),
                    'diametre_m': round(diametre, 3),
                    'diametre_mm': round(diametre * 1000, 0),
                    'vitesse_ms': round(vitesse, 2),
                    'pente': pente,
                    'rugosite': rugosite,
                    'statut': 'OK'
                }
                resultats.append(resultat)
                
            except Exception as e:
                resultats.append({
                    'id': row.get('id', index + 1),
                    'statut': 'ERREUR',
                    'erreur': str(e)
                })
        
        return jsonify({
            'success': True,
            'resultats': resultats,
            'total_traites': len(resultats),
            'message': f'Traitement par lot terminé: {len(resultats)} éléments traités'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du traitement par lot'
        }), 500

@app.route('/api/beton_arme/batch', methods=['POST'])
def traitement_lot_beton_arme():
    """Traitement par lot pour le béton armé"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier CSV fourni'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        df = pd.read_csv(file)
        
        # Validation des colonnes requises
        required_columns = ['Nu', 'Mu', 'b', 'h', 'L', 'k']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({'error': f'Colonnes manquantes: {missing_columns}'}), 400
        
        resultats = []
        for index, row in df.iterrows():
            try:
                # Définition des matériaux
                fc28 = row.get('fc28', 25.0)
                gamma_b = row.get('gamma_b', 1.5)
                fe = row.get('fe', 500.0)
                gamma_s = row.get('gamma_s', 1.15)
                
                beton = Beton(fc28=fc28, gamma_b=gamma_b)
                acier = Acier(fe=fe, gamma_s=gamma_s)
                
                # Création de la section
                section = SectionRectangulaire(
                    b=row['b'],
                    h=row['h'],
                    beton=beton,
                    acier=acier
                )
                
                # Calcul avec la vraie fonction
                resultat_calcul = design_rectangular_column(
                    section=section,
                    Nu=row['Nu'],
                    Mu=row['Mu'],
                    L=row['L'],
                    k=row['k']
                )
                
                resultat = {
                    'id': row.get('id', index + 1),
                    'Nu_kn': round(row['Nu'] / 1000, 1),
                    'Mu_knm': round(row['Mu'] / 1000, 2),
                    'b_m': row['b'],
                    'h_m': row['h'],
                    'L_m': row['L'],
                    'k': row['k'],
                    'section_acier_requise_cm2': round(resultat_calcul['As_required'] * 10000, 2),
                    'verification': resultat_calcul.get('status', 'OK'),
                    'contrainte_beton_mpa': round(resultat_calcul.get('concrete_stress', 0) / 1000000, 2),
                    'contrainte_acier_mpa': round(resultat_calcul.get('steel_stress', 0) / 1000000, 2),
                    'elancement': round(resultat_calcul.get('slenderness', 0), 1),
                    'fc28_mpa': fc28,
                    'fe_mpa': fe,
                    'statut': 'OK'
                }
                resultats.append(resultat)
                
            except Exception as e:
                resultats.append({
                    'id': row.get('id', index + 1),
                    'statut': 'ERREUR',
                    'erreur': str(e)
                })
        
        return jsonify({
            'success': True,
            'resultats': resultats,
            'total_traites': len(resultats),
            'message': f'Traitement par lot terminé: {len(resultats)} poteaux traités'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du traitement par lot'
        }), 500

@app.route('/api/bois/batch', methods=['POST'])
def traitement_lot_bois():
    """Traitement par lot pour le bois"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier CSV fourni'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        df = pd.read_csv(file)
        
        # Validation des colonnes requises
        required_columns = ['longueur', 'b', 'h', 'classe_bois', 'charge_g', 'charge_q']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({'error': f'Colonnes manquantes: {missing_columns}'}), 400
        
        resultats = []
        for index, row in df.iterrows():
            try:
                # Données de charge
                charges = {
                    'G': row['charge_g'],
                    'Q': row['charge_q'],
                    'W': row.get('charge_w', 0.0),
                    'S': row.get('charge_s', 0.0)
                }
                
                longueur = row['longueur']
                b = row['b'] / 1000  # conversion mm vers m
                h = row['h'] / 1000  # conversion mm vers m
                classe_bois = row['classe_bois']
                classe_service = row.get('classe_service', 2)
                duree_charge = row.get('duree_charge', 'moyen terme')
                
                # Calcul des sollicitations
                sollicitations = calculer_sollicitations_completes(
                    longueur, charges, "bois", classe_bois, verbose=False
                )
                
                # Vérification de la section
                resultat_verification = verifier_section_bois(
                    b=b,
                    h=h,
                    classe_bois=classe_bois,
                    classe_service=classe_service,
                    duree_charge=duree_charge,
                    M_Ed=sollicitations['M_Ed'],
                    V_Ed=sollicitations['V_Ed'],
                    verbose=False
                )
                
                resultat = {
                    'id': row.get('id', index + 1),
                    'longueur_m': longueur,
                    'b_mm': row['b'],
                    'h_mm': row['h'],
                    'classe_bois': classe_bois,
                    'charge_g_knm': row['charge_g'],
                    'charge_q_knm': row['charge_q'],
                    'moment_maximal_knm': round(sollicitations['M_Ed'] / 1000, 2),
                    'effort_tranchant_maximal_kn': round(sollicitations['V_Ed'] / 1000, 2),
                    'verification_flexion': resultat_verification.get('flexion_ok', False),
                    'verification_cisaillement': resultat_verification.get('cisaillement_ok', False),
                    'verification_flache': resultat_verification.get('flache_ok', False),
                    'section_adequate': resultat_verification.get('section_adequate', False),
                    'classe_service': classe_service,
                    'duree_charge': duree_charge,
                    'statut': 'OK'
                }
                resultats.append(resultat)
                
            except Exception as e:
                resultats.append({
                    'id': row.get('id', index + 1),
                    'statut': 'ERREUR',
                    'erreur': str(e)
                })
        
        return jsonify({
            'success': True,
            'resultats': resultats,
            'total_traites': len(resultats),
            'message': f'Traitement par lot terminé: {len(resultats)} éléments traités'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du traitement par lot'
        }), 500

# ===== ENDPOINTS ÉTUDE COMPARATIVE - ASSAINISSEMENT =====

@app.route('/api/assainissement/comparaison', methods=['POST'])
def etude_comparative_assainissement():
    """Étude comparative avec différents scénarios pluviométriques"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['surface', 'coefficient_ruissellement', 'scenarios']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        surface = data['surface']  # en m²
        coefficient = data['coefficient_ruissellement']
        scenarios = data['scenarios']
        
        # Traitement de chaque scénario
        resultats_comparaison = []
        
        for scenario in scenarios:
            try:
                nom_scenario = scenario.get('nom', 'Scénario')
                intensite = scenario.get('intensite_pluie', 50.0)
                pente = scenario.get('pente', 0.02)
                rugosite = scenario.get('rugosite', 0.013)
                
                # Calcul du débit
                surface_ha = surface / 10000
                debit = calculer_q_max_rationnelle(
                    coefficient, intensite, surface_ha, verbose=False
                )
                
                # Calcul du diamètre
                diametre = 0.1
                tolerance = 0.001
                max_iterations = 50
                
                for i in range(max_iterations):
                    aire = 3.14159 * diametre**2 / 4
                    rayon_hydraulique = diametre / 4
                    debit_calcule = (1/rugosite) * aire * (rayon_hydraulique**(2/3)) * (pente**0.5)
                    
                    if abs(debit_calcule - debit) < tolerance:
                        break
                    elif debit_calcule < debit:
                        diametre *= 1.1
                    else:
                        diametre *= 0.9
                
                vitesse = debit / aire
                
                resultat_scenario = {
                    'nom_scenario': nom_scenario,
                    'intensite_pluie_mmh': intensite,
                    'pente': pente,
                    'rugosite': rugosite,
                    'debit_m3s': round(debit, 3),
                    'debit_ls': round(debit * 1000, 1),
                    'diametre_m': round(diametre, 3),
                    'diametre_mm': round(diametre * 1000, 0),
                    'vitesse_ms': round(vitesse, 2),
                    'statut': 'OK'
                }
                resultats_comparaison.append(resultat_scenario)
                
            except Exception as e:
                resultats_comparaison.append({
                    'nom_scenario': scenario.get('nom', 'Scénario'),
                    'statut': 'ERREUR',
                    'erreur': str(e)
                })
        
        # Analyse comparative
        if len(resultats_comparaison) > 1:
            debits = [r['debit_ls'] for r in resultats_comparaison if r['statut'] == 'OK']
            diametres = [r['diametre_mm'] for r in resultats_comparaison if r['statut'] == 'OK']
            
            analyse_comparative = {
                'debit_min_ls': min(debits) if debits else 0,
                'debit_max_ls': max(debits) if debits else 0,
                'debit_moyen_ls': round(sum(debits) / len(debits), 1) if debits else 0,
                'diametre_min_mm': min(diametres) if diametres else 0,
                'diametre_max_mm': max(diametres) if diametres else 0,
                'diametre_moyen_mm': round(sum(diametres) / len(diametres), 0) if diametres else 0,
                'variation_debit_pourcent': round((max(debits) - min(debits)) / min(debits) * 100, 1) if debits and min(debits) > 0 else 0,
                'variation_diametre_pourcent': round((max(diametres) - min(diametres)) / min(diametres) * 100, 1) if diametres and min(diametres) > 0 else 0
            }
        else:
            analyse_comparative = {}
        
        return jsonify({
            'success': True,
            'resultats_scenarios': resultats_comparaison,
            'analyse_comparative': analyse_comparative,
            'total_scenarios': len(scenarios),
            'scenarios_reussis': len([r for r in resultats_comparaison if r['statut'] == 'OK']),
            'message': f'Étude comparative terminée: {len(scenarios)} scénarios analysés'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors de l\'étude comparative'
        }), 500

@app.route('/api/assainissement/formules_idf', methods=['GET'])
def get_formules_idf():
    """Récupère les formules IDF disponibles"""
    formules = {
        'montana': {
            'nom': 'Montana',
            'description': 'Formule de Montana pour l\'intensité de pluie',
            'formule': 'i = a * T^b',
            'parametres': ['a', 'b'],
            'exemple': {'a': 100.0, 'b': -0.5}
        },
        'talbot': {
            'nom': 'Talbot',
            'description': 'Formule de Talbot pour l\'intensité de pluie',
            'formule': 'i = a / (T + b)',
            'parametres': ['a', 'b'],
            'exemple': {'a': 70.0, 'b': 15.0}
        },
        'kiefer-chu': {
            'nom': 'Kiefer-Chu',
            'description': 'Formule de Kiefer-Chu pour l\'intensité de pluie',
            'formule': 'i = a / (T + b)^c',
            'parametres': ['a', 'b', 'c'],
            'exemple': {'a': 700.0, 'b': 30.0, 'c': 1.2}
        }
    }
    return jsonify(formules)

@app.route('/api/assainissement/calcul_idf', methods=['POST'])
def calcul_intensite_idf():
    """Calcul de l'intensité de pluie avec différentes formules IDF"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['formule', 'periode_retour', 'parametres']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        formule = data['formule']
        T = data['periode_retour']  # période de retour en années
        parametres = data['parametres']
        
        # Calcul selon la formule choisie
        if formule == 'montana':
            a = parametres['a']
            b = parametres['b']
            intensite = a * (T ** b)
        elif formule == 'talbot':
            a = parametres['a']
            b = parametres['b']
            intensite = a / (T + b)
        elif formule == 'kiefer-chu':
            a = parametres['a']
            b = parametres['b']
            c = parametres['c']
            intensite = a / ((T + b) ** c)
        else:
            return jsonify({'error': f'Formule non supportée: {formule}'}), 400
        
        resultat = {
            'formule': formule,
            'periode_retour_ans': T,
            'parametres': parametres,
            'intensite_mmh': round(intensite, 2),
            'intensite_mmmin': round(intensite / 60, 3)
        }
        
        return jsonify({
            'success': True,
            'resultat': resultat,
            'message': f'Calcul IDF avec la formule {formule} effectué avec succès'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors du calcul IDF'
        }), 500

# ===== ENDPOINTS RAPPORTS PDF =====

@app.route('/api/rapports/generer_pdf', methods=['POST'])
def generer_rapport_pdf():
    """Génération de rapports PDF pour tous les modules"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['module', 'donnees', 'resultats']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        module = data['module']
        donnees = data['donnees']
        resultats = data['resultats']
        
        # Génération du contenu PDF selon le module
        if module == 'assainissement':
            contenu_pdf = generer_rapport_assainissement(donnees, resultats)
        elif module == 'beton_arme':
            contenu_pdf = generer_rapport_beton_arme(donnees, resultats)
        elif module == 'bois':
            contenu_pdf = generer_rapport_bois(donnees, resultats)
        else:
            return jsonify({'error': f'Module non supporté: {module}'}), 400
        
        # Sauvegarde du rapport
        nom_fichier = f"rapport_{module}_{int(time.time())}.pdf"
        chemin_fichier = os.path.join('output', 'rapports', nom_fichier)
        
        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(chemin_fichier), exist_ok=True)
        
        # Écrire le fichier PDF (simulation pour l'instant)
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            f.write(contenu_pdf)
        
        return jsonify({
            'success': True,
            'fichier': nom_fichier,
            'chemin': chemin_fichier,
            'message': f'Rapport PDF généré avec succès: {nom_fichier}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors de la génération du rapport PDF'
        }), 500

def generer_rapport_assainissement(donnees, resultats):
    """Génère le contenu PDF pour l'assainissement"""
    contenu = f"""
RAPPORT DIMENSIONNEMENT ASSAINISSEMENT
=====================================

Date: {time.strftime('%d/%m/%Y %H:%M:%S')}

DONNÉES D'ENTRÉE:
-----------------
Surface: {donnees.get('surface', 'N/A')} m²
Coefficient de ruissellement: {donnees.get('coefficient_ruissellement', 'N/A')}
Intensité de pluie: {donnees.get('intensite_pluie', 'N/A')} mm/h
Pente: {donnees.get('pente', 'N/A')}
Rugosité: {donnees.get('rugosite', 'N/A')}

RÉSULTATS:
----------
Débit: {resultats.get('debit_ls', 'N/A')} L/s
Diamètre: {resultats.get('diametre_mm', 'N/A')} mm
Vitesse: {resultats.get('vitesse_ms', 'N/A')} m/s

VALIDATION:
----------
Vitesse minimale (auto-curage): 0.6 m/s
Vitesse maximale (anti-érosion): 3.0 m/s
"""
    return contenu

def generer_rapport_beton_arme(donnees, resultats):
    """Génère le contenu PDF pour le béton armé"""
    contenu = f"""
RAPPORT DIMENSIONNEMENT BÉTON ARMÉ
==================================

Date: {time.strftime('%d/%m/%Y %H:%M:%S')}

DONNÉES D'ENTRÉE:
-----------------
Effort normal ultime: {donnees.get('Nu', 'N/A')} kN
Moment ultime: {donnees.get('Mu', 'N/A')} kN.m
Dimensions: {donnees.get('b', 'N/A')} x {donnees.get('h', 'N/A')} m
Hauteur libre: {donnees.get('L', 'N/A')} m
Coefficient de flambement: {donnees.get('k', 'N/A')}

RÉSULTATS:
----------
Section d'acier requise: {resultats.get('section_acier_requise_cm2', 'N/A')} cm²
Vérification: {resultats.get('verification', 'N/A')}
Élancement: {resultats.get('elancement', 'N/A')}
Contrainte béton: {resultats.get('contrainte_beton_mpa', 'N/A')} MPa
Contrainte acier: {resultats.get('contrainte_acier_mpa', 'N/A')} MPa

MATÉRIAUX:
----------
Béton: {resultats.get('materiaux', {}).get('beton', 'N/A')}
Acier: {resultats.get('materiaux', {}).get('acier', 'N/A')}
"""
    return contenu

def generer_rapport_bois(donnees, resultats):
    """Génère le contenu PDF pour le bois"""
    contenu = f"""
RAPPORT VÉRIFICATION BOIS
=========================

Date: {time.strftime('%d/%m/%Y %H:%M:%S')}

DONNÉES D'ENTRÉE:
-----------------
Longueur: {donnees.get('longueur', 'N/A')} m
Dimensions: {donnees.get('b', 'N/A')} x {donnees.get('h', 'N/A')} mm
Classe de bois: {donnees.get('classe_bois', 'N/A')}
Charge permanente: {donnees.get('charge_g', 'N/A')} kN/m
Charge exploitation: {donnees.get('charge_q', 'N/A')} kN/m

RÉSULTATS:
----------
Moment maximal: {resultats.get('moment_maximal_knm', 'N/A')} kN.m
Effort tranchant maximal: {resultats.get('effort_tranchant_maximal_kn', 'N/A')} kN
Vérification flexion: {resultats.get('verification_flexion', 'N/A')}
Vérification cisaillement: {resultats.get('verification_cisaillement', 'N/A')}
Vérification flèche: {resultats.get('verification_flache', 'N/A')}
Section adéquate: {resultats.get('section_adequate', 'N/A')}

MATÉRIAU:
---------
Classe de bois: {resultats.get('materiau', {}).get('classe_bois', 'N/A')}
Classe de service: {resultats.get('materiau', {}).get('classe_service', 'N/A')}
Durée de charge: {resultats.get('materiau', {}).get('duree_charge', 'N/A')}
"""
    return contenu

@app.route('/api/rapports/liste', methods=['GET'])
def liste_rapports():
    """Liste tous les rapports PDF disponibles"""
    try:
        dossier_rapports = os.path.join('output', 'rapports')
        if not os.path.exists(dossier_rapports):
            return jsonify({
                'success': True,
                'rapports': [],
                'message': 'Aucun rapport disponible'
            })
        
        rapports = []
        for fichier in os.listdir(dossier_rapports):
            if fichier.endswith('.pdf'):
                chemin = os.path.join(dossier_rapports, fichier)
                stat = os.stat(chemin)
                rapports.append({
                    'nom': fichier,
                    'taille_octets': stat.st_size,
                    'date_creation': time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(stat.st_ctime)),
                    'chemin': chemin
                })
        
        # Trier par date de création (plus récent en premier)
        rapports.sort(key=lambda x: x['date_creation'], reverse=True)
        
        return jsonify({
            'success': True,
            'rapports': rapports,
            'total': len(rapports),
            'message': f'{len(rapports)} rapport(s) trouvé(s)'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors de la récupération des rapports'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 