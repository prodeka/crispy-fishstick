#!/usr/bin/env python3
"""
Démonstration d'utilisation de la base SQLite des pompes Grundfos
Montre comment intégrer cette base dans votre projet LCPI
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

class PumpDatabase:
    """Interface pour la base de données des pompes"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connexion à la base de données"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"✅ Connexion à la base: {self.db_path}")
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            raise
    
    def disconnect(self):
        """Déconnexion de la base de données"""
        if self.conn:
            self.conn.close()
            print("🔌 Déconnexion de la base")
    
    def find_pump_by_requirements(self, 
                                target_debit: float, 
                                target_hmt: float,
                                max_capex: Optional[float] = None,
                                min_efficiency: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Trouve les pompes adaptées aux besoins spécifiés
        
        Args:
            target_debit: Débit cible en m³/h
            target_hmt: HMT cible en m
            max_capex: CAPEX maximum en € (optionnel)
            min_efficiency: Rendement minimum en % (optionnel)
        """
        query = """
            SELECT designation, marque, nom_produit,
                   debit_exploitation_m3h_min, debit_exploitation_m3h_max,
                   hmt_min_m, hmt_max_m, capex_estime_eur,
                   rendement_pompe_moteur_pct, opex_par_kwh_eur
            FROM pompes
            WHERE debit_exploitation_m3h_min <= ? 
              AND debit_exploitation_m3h_max >= ?
              AND hmt_min_m <= ? 
              AND hmt_max_m >= ?
        """
        
        params = [target_debit, target_debit, target_hmt, target_hmt]
        
        if max_capex is not None:
            query += " AND capex_estime_eur <= ?"
            params.append(max_capex)
        
        if min_efficiency is not None:
            query += " AND rendement_pompe_moteur_pct >= ?"
            params.append(min_efficiency)
        
        query += " ORDER BY capex_estime_eur, rendement_pompe_moteur_pct DESC"
        
        try:
            self.cursor.execute(query, params)
            results = []
            
            for row in self.cursor.fetchall():
                pump = {
                    'designation': row[0],
                    'marque': row[1],
                    'nom_produit': row[2],
                    'debit_range': f"{row[3]}-{row[4]} m³/h",
                    'hmt_range': f"{row[5]}-{row[6]}m",
                    'capex': row[7],
                    'efficiency': row[8],
                    'opex': row[9]
                }
                results.append(pump)
            
            return results
            
        except Exception as e:
            print(f"❌ Erreur lors de la recherche: {e}")
            return []
    
    def get_pump_curves(self, designation: str) -> Optional[List[List[float]]]:
        """Récupère la courbe H(Q) d'une pompe"""
        try:
            self.cursor.execute(
                "SELECT courbe_hq_points FROM pompes WHERE designation = ?",
                (designation,)
            )
            row = self.cursor.fetchone()
            
            if row and row[0]:
                return json.loads(row[0])
            return None
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de la courbe: {e}")
            return None
    
    def get_cost_analysis(self) -> Dict[str, Any]:
        """Analyse des coûts de toutes les pompes"""
        try:
            # Statistiques générales
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    AVG(capex_estime_eur) as capex_moyen,
                    MIN(capex_estime_eur) as capex_min,
                    MAX(capex_estime_eur) as capex_max,
                    AVG(opex_par_kwh_eur) as opex_moyen
                FROM pompes
                WHERE capex_estime_eur IS NOT NULL
            """)
            
            stats = self.cursor.fetchone()
            
            # Répartition par plage de coût
            self.cursor.execute("""
                SELECT 
                    CASE 
                        WHEN capex_estime_eur <= 500 THEN '0-500€'
                        WHEN capex_estime_eur <= 2000 THEN '500-2000€'
                        WHEN capex_estime_eur <= 5000 THEN '2000-5000€'
                        WHEN capex_estime_eur <= 10000 THEN '5000-10000€'
                        ELSE '10000€+'
                    END as plage_cout,
                    COUNT(*) as nb_pompes
                FROM pompes
                GROUP BY plage_cout
                ORDER BY nb_pompes DESC
            """)
            
            repartition = dict(self.cursor.fetchall())
            
            return {
                'total_pompes': stats[0],
                'capex_moyen': stats[1],
                'capex_min': stats[2],
                'capex_max': stats[3],
                'opex_moyen': stats[4],
                'repartition_cout': repartition
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse des coûts: {e}")
            return {}


def demo_pump_selection():
    """Démonstration de sélection de pompes"""
    print("🚀 DÉMONSTRATION: SÉLECTION DE POMPES")
    print("=" * 50)
    
    db = PumpDatabase("grundfos_pompes_230_modeles_complet_pompes.db")
    
    try:
        db.connect()
        
        # 1. Recherche de pompes pour un besoin spécifique
        print("\n🔍 Recherche de pompes pour:")
        print("   Débit: 15 m³/h")
        print("   HMT: 80m")
        print("   CAPEX max: 5000€")
        print("   Rendement min: 60%")
        
        pompes = db.find_pump_by_requirements(
            target_debit=15.0,
            target_hmt=80.0,
            max_capex=5000.0,
            min_efficiency=60.0
        )
        
        print(f"\n✅ {len(pompes)} pompes trouvées:")
        for i, pompe in enumerate(pompes[:5], 1):  # Afficher les 5 premières
            print(f"  {i}. {pompe['designation']}")
            print(f"     Débit: {pompe['debit_range']}, HMT: {pompe['hmt_range']}")
            print(f"     CAPEX: {pompe['capex']:.0f}€, Rendement: {pompe['efficiency']:.1f}%")
        
        # 2. Analyse des coûts
        print("\n💰 ANALYSE DES COÛTS:")
        cost_analysis = db.get_cost_analysis()
        
        if cost_analysis:
            print(f"  Total pompes: {cost_analysis['total_pompes']}")
            print(f"  CAPEX moyen: {cost_analysis['capex_moyen']:.0f}€")
            print(f"  CAPEX min-max: {cost_analysis['capex_min']:.0f}€ - {cost_analysis['capex_max']:.0f}€")
            print(f"  OPEX moyen: {cost_analysis['opex_moyen']:.3f}€/kWh")
            
            print("\n  Répartition par coût:")
            for plage, nb in cost_analysis['repartition_cout'].items():
                print(f"    {plage}: {nb} pompes")
        
        # 3. Exemple de courbe H(Q)
        if pompes:
            designation = pompes[0]['designation']
            print(f"\n📊 Courbe H(Q) de {designation}:")
            courbe = db.get_pump_curves(designation)
            
            if courbe:
                print("  Points (Q, H):")
                for point in courbe[:5]:  # Afficher les 5 premiers points
                    print(f"    ({point[0]:.1f} m³/h, {point[1]:.1f}m)")
            else:
                print("  Courbe non disponible")
        
        print("\n✅ Démonstration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.disconnect()


if __name__ == "__main__":
    demo_pump_selection()
