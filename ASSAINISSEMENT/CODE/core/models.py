# core/models.py
import math
from formulas import tc_kirpich, tc_californienne, dimensionner_section

class Troncon:
    """Représente un tronçon unique du réseau avec ses données et résultats."""
    def __init__(self, **kwargs):
        # Attributs d'entrée
        self.id = str(kwargs.get('id_troncon'))
        self.type_section = kwargs.get('type_section')
        self.largeur_fond_m = float(kwargs.get('largeur_fond_m', 0))
        self.fruit_z = float(kwargs.get('fruit_z', 0))
        self.surface_ha = float(kwargs.get('surface_ha'))
        self.coeff_ruissellement = float(kwargs.get('coeff_ruissellement'))
        self.long_parcours_surface_m = float(kwargs.get('longueur_parcours_surface_m'))
        self.pente_parcours_surface = float(kwargs.get('pente_parcours_surface'))
        self.long_troncon_m = float(kwargs.get('longueur_troncon_m'))
        self.pente_troncon = float(kwargs.get('pente_troncon'))
        self.ks = float(kwargs.get('ks_manning_strickler'))
        self.amont_ids = [s.strip() for s in str(kwargs.get('troncon_amont', 'NONE')).split(';')] if str(kwargs.get('troncon_amont', 'NONE')) != 'NONE' else ['NONE']

        # Attributs calculés
        self.surface_cumulee = self.surface_ha
        self.c_moyen_cumule = self.coeff_ruissellement
        self.tc_amont_max = 0
        self.tc_final_min = 0
        self.q_max_m3s = 0
        self.longueur_cumulee = 0
        self.pentes_parcours = []
        self.resultat_dimensionnement = {}
        self.statut = 'Non traité'

    def calculer_tc_surface(self, methode='kirpich'):
        if methode == 'kirpich':
            return tc_kirpich(self.long_parcours_surface_m, self.pente_parcours_surface)
        else:
            return tc_californienne(self.long_parcours_surface_m, self.pente_parcours_surface)

    def to_dict(self):
        """Convertit les résultats de l'objet en dictionnaire pour le DataFrame final."""
        return {
            'id_troncon': self.id,
            'type_section': self.type_section,
            'surface_cumulee': round(self.surface_cumulee, 2),
            'c_moyen_cumule': round(self.c_moyen_cumule, 2),
            'tc_final_min': round(self.tc_final_min, 2),
            'q_max_m3s': round(self.q_max_m3s, 3),
            'diametre_retenu_mm': self.resultat_dimensionnement.get('diametre_mm', 0),
            'hauteur_retenue_m': self.resultat_dimensionnement.get('hauteur_m', 0),
            'largeur_m': self.resultat_dimensionnement.get('largeur_m', 0),
            'vitesse_ms': round(self.resultat_dimensionnement.get('vitesse_ms', 0), 2),
            'statut': self.statut
        }

class Reseau:
    """Représente l'ensemble du réseau, gère la topologie et l'ordre de calcul."""
    def __init__(self, df_input):
        self.troncons = {str(row['id_troncon']): Troncon(**row) for _, row in df_input.iterrows()}
        self.troncons_tries = self.trier_topologiquement()

    def trier_topologiquement(self):
        sorted_list = []
        processed_ids = set()
        
        while len(sorted_list) < len(self.troncons):
            found_new = False
            for troncon_id, troncon in self.troncons.items():
                if troncon_id in processed_ids: continue
                if troncon.amont_ids == ['NONE'] or all(am_id in processed_ids for am_id in troncon.amont_ids):
                    sorted_list.append(troncon)
                    processed_ids.add(troncon_id)
                    found_new = True
            
            if not found_new:
                unprocessed = set(self.troncons.keys()) - processed_ids
                raise Exception(f"Erreur de topologie. Boucle ou dépendance manquante. Tronçons non traités: {unprocessed}")
        
        return sorted_list