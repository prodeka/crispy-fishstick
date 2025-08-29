#!/usr/bin/env python3
"""
Outil de conversion CSV → YAML → SQLite pour la base de données des pompes Grundfos

Fonctionnalités:
- Conversion CSV → YAML (pour tests)
- Conversion CSV → SQLite (pour production)
- Conversion des prix d'euros vers FCFA
- Conversion des débits de m³/h vers m³/s pour EPANET
- Estimation précise de l'OPEX basée sur la puissance et le rendement
- Validation et nettoyage des données
- Gestion des erreurs et logging
- Interface CLI flexible
"""

import csv
import yaml
import sqlite3
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
from datetime import datetime


class PumpDataConverter:
    """Convertisseur de données de pompes CSV vers YAML et SQLite"""
    
    def __init__(self, csv_file: str, output_dir: str = "output", 
                 eur_to_fcfa_rate: float = 655.957,  # Taux de change EUR → FCFA
                 energy_cost_fcfa_kwh: float = 98.39):  # Coût électricité en FCFA/kWh
        self.csv_file = Path(csv_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Taux de change et coûts
        self.eur_to_fcfa_rate = eur_to_fcfa_rate
        self.energy_cost_fcfa_kwh = energy_cost_fcfa_kwh
        
        # Configuration du logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / 'conversion.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Schéma de la base de données SQLite amélioré
        self.sqlite_schema = """
        CREATE TABLE IF NOT EXISTS pompes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            designation TEXT UNIQUE NOT NULL,
            marque TEXT,
            nom_produit TEXT,
            type_moteur TEXT,
            poids_net_kg REAL,
            debit_exploitation_m3h_min REAL,
            debit_exploitation_m3h_max REAL,
            debit_exploitation_m3s_min REAL,
            debit_exploitation_m3s_max REAL,
            diametre_moteur TEXT,
            hmt_min_m REAL,
            hmt_max_m REAL,
            frequence_hz INTEGER,
            tension_v TEXT,
            intensite_nominale_a REAL,
            puissance_p2_kw REAL,
            cos_phi REAL,
            rendement_pompe_pct REAL,
            rendement_pompe_moteur_pct REAL,
            materiaux TEXT,
            classe_protection TEXT,
            classe_isolation TEXT,
            temp_max_liquide_c REAL,
            certification_eau_potable TEXT,
            courbe_hq_points TEXT,
            capex_estime_eur REAL,
            capex_estime_fcfa REAL,
            opex_par_kwh_eur REAL,
            opex_par_kwh_fcfa REAL,
            puissance_absorbe_kw REAL,
            opex_estime_fcfa_kwh REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_designation ON pompes(designation);
        CREATE INDEX IF NOT EXISTS idx_marque ON pompes(marque);
        CREATE INDEX IF NOT EXISTS idx_debit_range ON pompes(debit_exploitation_m3s_min, debit_exploitation_m3s_max);
        CREATE INDEX IF NOT EXISTS idx_hmt_range ON pompes(hmt_min_m, hmt_max_m);
        CREATE INDEX IF NOT EXISTS idx_capex_fcfa ON pompes(capex_estime_fcfa);
        CREATE INDEX IF NOT EXISTS idx_opex_fcfa ON pompes(opex_estime_fcfa_kwh);
        """
    
    def parse_csv(self) -> List[Dict[str, Any]]:
        """Parse le fichier CSV et retourne une liste de dictionnaires"""
        self.logger.info(f"Lecture du fichier CSV: {self.csv_file}")
        
        if not self.csv_file.exists():
            raise FileNotFoundError(f"Fichier CSV introuvable: {self.csv_file}")
        
        data = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Nettoyage et validation des données
                        cleaned_row = self._clean_row(row, row_num)
                        if cleaned_row:
                            data.append(cleaned_row)
                    except Exception as e:
                        self.logger.warning(f"Ligne {row_num} ignorée: {e}")
                        continue
                
                self.logger.info(f"✅ {len(data)} lignes parsées avec succès")
                return data
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la lecture du CSV: {e}")
            raise
    
    def _clean_row(self, row: Dict[str, str], row_num: int) -> Optional[Dict[str, Any]]:
        """Nettoie et valide une ligne de données"""
        try:
            # Extraction des plages de débit (ex: "0.3-1.5" → min=0.3, max=1.5)
            debit_range = row.get('Débit exploitation (m³/h)', '')
            debit_min, debit_max = self._parse_range(debit_range)
            
            # Conversion m³/h → m³/s pour EPANET
            debit_min_m3s = debit_min / 3600 if debit_min is not None else None
            debit_max_m3s = debit_max / 3600 if debit_max is not None else None
            
            # Extraction des plages HMT (ex: "10-60" → min=10, max=60)
            hmt_range = row.get('HMT (m)', '')
            hmt_min, hmt_max = self._parse_range(hmt_range)
            
            # Extraction des plages de tension (ex: "1x230/3x400" → ["1x230", "3x400"])
            tension = row.get('Tension (V)', '')
            tensions = self._parse_tension(tension)
            
            # Extraction des plages d'intensité (ex: "1.9/1.1" → [1.9, 1.1])
            intensite = row.get('Intensité nominale (A)', '')
            intensites = self._parse_intensite(intensite)
            
            # Parsing de la courbe H(Q) depuis la chaîne JSON
            courbe_hq = self._parse_courbe_hq(row.get('Courbe H(Q) (points approximatifs)', ''))
            
            # Prix en euros
            capex_eur = self._safe_float(row.get('CAPEX Estimé (€)', ''))
            opex_eur = self._safe_float(row.get('OPEX par kWh Estimé (€/kWh)', ''))
            
            # Conversion vers FCFA
            capex_fcfa = capex_eur * self.eur_to_fcfa_rate if capex_eur is not None else None
            opex_fcfa = opex_eur * self.eur_to_fcfa_rate if opex_eur is not None else None
            
            # Calculs techniques
            puissance_p2 = self._safe_float(row.get('Puissance P2 (kW)', ''))
            rendement_global = self._safe_float(row.get('Rendement pompe+moteur (%)', ''))
            
            # Estimation de la puissance absorbée et OPEX
            puissance_absorbe_kw = None
            opex_estime_fcfa_kwh = None
            
            if puissance_p2 is not None and rendement_global is not None and rendement_global > 0:
                # P_abs_kW = P2_kW / (rendement_global / 100)
                puissance_absorbe_kw = puissance_p2 / (rendement_global / 100)
                
                # OPEX estimé basé sur la puissance absorbée et le coût de l'électricité
                opex_estime_fcfa_kwh = puissance_absorbe_kw * self.energy_cost_fcfa_kwh
            
            cleaned_row = {
                'designation': row.get('Désignation', '').strip(),
                'marque': row.get('Marque', '').strip(),
                'nom_produit': row.get('Nom du produit', '').strip(),
                'type_moteur': row.get('Type de moteur', '').strip(),
                'poids_net_kg': self._safe_float(row.get('Poids net (kg)', '')),
                'debit_exploitation_m3h_min': debit_min,
                'debit_exploitation_m3h_max': debit_max,
                'debit_exploitation_m3s_min': debit_min_m3s,
                'debit_exploitation_m3s_max': debit_max_m3s,
                'diametre_moteur': row.get('Diamètre moteur', '').strip(),
                'hmt_min_m': hmt_min,
                'hmt_max_m': hmt_max,
                'frequence_hz': self._safe_int(row.get('Fréquence (Hz)', '')),
                'tension_v': json.dumps(tensions, ensure_ascii=False),
                'intensite_nominale_a': json.dumps(intensites, ensure_ascii=False),
                'puissance_p2_kw': puissance_p2,
                'cos_phi': self._safe_float(row.get('Cos φ', '')),
                'rendement_pompe_pct': self._safe_float(row.get('Rendement pompe (%)', '')),
                'rendement_pompe_moteur_pct': rendement_global,
                'materiaux': row.get('Matériaux', '').strip(),
                'classe_protection': row.get('Classe protection', '').strip(),
                'classe_isolation': row.get('Classe isolation', '').strip(),
                'temp_max_liquide_c': self._safe_float(row.get('Temp max liquide (°C)', '')),
                'certification_eau_potable': row.get('Certification eau potable', '').strip(),
                'courbe_hq_points': json.dumps(courbe_hq, ensure_ascii=False),
                'capex_estime_eur': capex_eur,
                'capex_estime_fcfa': capex_fcfa,
                'opex_par_kwh_eur': opex_eur,
                'opex_par_kwh_fcfa': opex_fcfa,
                'puissance_absorbe_kw': puissance_absorbe_kw,
                'opex_estime_fcfa_kwh': opex_estime_fcfa_kwh
            }
            
            # Validation des données obligatoires
            if not cleaned_row['designation']:
                self.logger.warning(f"Ligne {row_num}: Désignation manquante, ligne ignorée")
                return None
            
            return cleaned_row
            
        except Exception as e:
            self.logger.warning(f"Ligne {row_num}: Erreur de nettoyage: {e}")
            return None
    
    def _parse_range(self, range_str: str) -> tuple[Optional[float], Optional[float]]:
        """Parse une plage de valeurs (ex: "10-60" → (10.0, 60.0))"""
        if not range_str or range_str.strip() == '':
            return None, None
        
        try:
            parts = range_str.strip().split('-')
            if len(parts) == 2:
                return self._safe_float(parts[0]), self._safe_float(parts[1])
            elif len(parts) == 1:
                value = self._safe_float(parts[0])
                return value, value
            else:
                return None, None
        except:
            return None, None
    
    def _parse_tension(self, tension_str: str) -> List[str]:
        """Parse les tensions (ex: "1x230/3x400" → ["1x230", "3x400"])"""
        if not tension_str or tension_str.strip() == '':
            return []
        
        try:
            return [t.strip() for t in tension_str.split('/') if t.strip()]
        except:
            return [tension_str.strip()]
    
    def _parse_intensite(self, intensite_str: str) -> List[float]:
        """Parse les intensités (ex: "1.9/1.1" → [1.9, 1.1])"""
        if not intensite_str or intensite_str.strip() == '':
            return []
        
        try:
            parts = intensite_str.split('/')
            return [self._safe_float(part.strip()) for part in parts if part.strip()]
        except:
            return []
    
    def _parse_courbe_hq(self, courbe_str: str) -> List[List[float]]:
        """Parse la courbe H(Q) depuis la chaîne JSON"""
        if not courbe_str or courbe_str.strip() == '':
            return []
        
        try:
            # Nettoyage de la chaîne JSON
            courbe_str = courbe_str.strip()
            if courbe_str.startswith('"') and courbe_str.endswith('"'):
                courbe_str = courbe_str[1:-1]
            
            # Parsing JSON
            courbe_data = json.loads(courbe_str)
            if isinstance(courbe_data, list):
                return courbe_data
            else:
                return []
        except Exception as e:
            self.logger.warning(f"Erreur parsing courbe H(Q): {e}")
            return []
    
    def _safe_float(self, value: str) -> Optional[float]:
        """Convertit une valeur en float de manière sécurisée"""
        if not value or value.strip() == '':
            return None
        
        try:
            return float(value.strip().replace(',', '.'))
        except (ValueError, TypeError):
            return None
    
    def _safe_int(self, value: str) -> Optional[int]:
        """Convertit une valeur en int de manière sécurisée"""
        if not value or value.strip() == '':
            return None
        
        try:
            return int(float(value.strip().replace(',', '.')))
        except (ValueError, TypeError):
            return None
    
    def to_yaml(self, data: List[Dict[str, Any]]) -> str:
        """Convertit les données en format YAML"""
        self.logger.info("Conversion vers YAML...")
        
        yaml_data = {
            'metadata': {
                'source': str(self.csv_file),
                'conversion_date': datetime.now().isoformat(),
                'total_pompes': len(data),
                'format_version': '1.0'
            },
            'pompes': data
        }
        
        yaml_file = self.output_dir / f"{self.csv_file.stem}_converted.yaml"
        
        try:
            with open(yaml_file, 'w', encoding='utf-8') as file:
                yaml.dump(yaml_data, file, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False, indent=2)
            
            self.logger.info(f"✅ YAML sauvegardé: {yaml_file}")
            return str(yaml_file)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde YAML: {e}")
            raise
    
    def to_sqlite(self, data: List[Dict[str, Any]]) -> str:
        """Convertit les données en base SQLite"""
        self.logger.info("Conversion vers SQLite...")
        
        db_file = self.output_dir / f"{self.csv_file.stem}_pompes.db"
        
        try:
            # Création de la base de données
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Création des tables
            cursor.executescript(self.sqlite_schema)
            
            # Insertion des données
            insert_sql = """
            INSERT OR REPLACE INTO pompes (
                designation, marque, nom_produit, type_moteur, poids_net_kg,
                debit_exploitation_m3h_min, debit_exploitation_m3h_max, debit_exploitation_m3s_min, debit_exploitation_m3s_max,
                diametre_moteur, hmt_min_m, hmt_max_m, frequence_hz, tension_v, intensite_nominale_a,
                puissance_p2_kw, cos_phi, rendement_pompe_pct, rendement_pompe_moteur_pct,
                materiaux, classe_protection, classe_isolation, temp_max_liquide_c,
                certification_eau_potable, courbe_hq_points, capex_estime_eur, capex_estime_fcfa,
                opex_par_kwh_eur, opex_par_kwh_fcfa, puissance_absorbe_kw, opex_estime_fcfa_kwh
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            for row in data:
                cursor.execute(insert_sql, (
                    row['designation'], row['marque'], row['nom_produit'], row['type_moteur'],
                    row['poids_net_kg'], row['debit_exploitation_m3h_min'], row['debit_exploitation_m3h_max'],
                    row['debit_exploitation_m3s_min'], row['debit_exploitation_m3s_max'],
                    row['diametre_moteur'], row['hmt_min_m'], row['hmt_max_m'], row['frequence_hz'],
                    row['tension_v'], row['intensite_nominale_a'], row['puissance_p2_kw'], row['cos_phi'],
                    row['rendement_pompe_pct'], row['rendement_pompe_moteur_pct'], row['materiaux'],
                    row['classe_protection'], row['classe_isolation'], row['temp_max_liquide_c'],
                    row['certification_eau_potable'], row['courbe_hq_points'], row['capex_estime_eur'],
                    row['capex_estime_fcfa'], row['opex_par_kwh_eur'], row['opex_par_kwh_fcfa'],
                    row['puissance_absorbe_kw'], row['opex_estime_fcfa_kwh']
                ))
            
            # Validation et statistiques
            cursor.execute("SELECT COUNT(*) FROM pompes")
            total_inserted = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT marque) FROM pompes")
            marques_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT designation) FROM pompes")
            designations_count = cursor.fetchone()[0]
            
            # Création d'index pour les performances
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_capex_fcfa ON pompes(capex_estime_fcfa)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_opex_fcfa ON pompes(opex_estime_fcfa_kwh)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_rendement ON pompes(rendement_pompe_moteur_pct)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_debit_m3s ON pompes(debit_exploitation_m3s_min, debit_exploitation_m3s_max)")
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"✅ SQLite sauvegardé: {db_file}")
            self.logger.info(f"📊 Statistiques: {total_inserted} pompes, {marques_count} marques, {designations_count} désignations uniques")
            
            return str(db_file)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création SQLite: {e}")
            raise
    
    def generate_report(self, data: List[Dict[str, Any]], yaml_file: str, sqlite_file: str) -> str:
        """Génère un rapport de conversion"""
        self.logger.info("Génération du rapport...")
        
        report_file = self.output_dir / f"conversion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # Statistiques des données
        marques = set(row['marque'] for row in data if row['marque'])
        types_moteur = set(row['type_moteur'] for row in data if row['type_moteur'])
        materiaux = set(row['materiaux'] for row in data if row['materiaux'])
        
        # Prix en euros
        capex_eur_values = [row['capex_estime_eur'] for row in data if row['capex_estime_eur'] is not None]
        opex_eur_values = [row['opex_par_kwh_eur'] for row in data if row['opex_par_kwh_eur'] is not None]
        
        # Prix en FCFA
        capex_fcfa_values = [row['capex_estime_fcfa'] for row in data if row['capex_estime_fcfa'] is not None]
        opex_fcfa_values = [row['opex_estime_fcfa_kwh'] for row in data if row['opex_estime_fcfa_kwh'] is not None]
        
        # Débits convertis
        debit_m3s_values = [row['debit_exploitation_m3s_min'] for row in data if row['debit_exploitation_m3s_min'] is not None]
        debit_m3s_values.extend([row['debit_exploitation_m3s_max'] for row in data if row['debit_exploitation_m3s_max'] is not None])
        
        try:
            with open(report_file, 'w', encoding='utf-8') as file:
                file.write(f"# Rapport de Conversion CSV → YAML/SQLite\n\n")
                file.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"**Source:** {self.csv_file}\n")
                file.write(f"**Taux de change:** 1 EUR = {self.eur_to_fcfa_rate:.3f} FCFA\n")
                file.write(f"**Coût électricité:** {self.energy_cost_fcfa_kwh:.2f} FCFA/kWh\n\n")
                
                file.write(f"## 📊 Statistiques Générales\n\n")
                file.write(f"- **Total pompes:** {len(data)}\n")
                file.write(f"- **Marques:** {len(marques)}\n")
                file.write(f"- **Types de moteur:** {len(types_moteur)}\n")
                file.write(f"- **Matériaux:** {len(materiaux)}\n\n")
                
                file.write(f"## 💰 Analyse des Coûts (EUR)\n\n")
                if capex_eur_values:
                    file.write(f"- **CAPEX min:** {min(capex_eur_values):.2f} €\n")
                    file.write(f"- **CAPEX max:** {max(capex_eur_values):.2f} €\n")
                    file.write(f"- **CAPEX moyen:** {sum(capex_eur_values)/len(capex_eur_values):.2f} €\n\n")
                
                if opex_eur_values:
                    file.write(f"- **OPEX min:** {min(opex_eur_values):.3f} €/kWh\n")
                    file.write(f"- **OPEX max:** {max(opex_eur_values):.3f} €/kWh\n")
                    file.write(f"- **OPEX moyen:** {sum(opex_eur_values)/len(opex_eur_values):.3f} €/kWh\n\n")
                
                file.write(f"## 💰 Analyse des Coûts (FCFA)\n\n")
                if capex_fcfa_values:
                    file.write(f"- **CAPEX min:** {min(capex_fcfa_values):,.0f} FCFA\n")
                    file.write(f"- **CAPEX max:** {max(capex_fcfa_values):,.0f} FCFA\n")
                    file.write(f"- **CAPEX moyen:** {sum(capex_fcfa_values)/len(capex_fcfa_values):,.0f} FCFA\n\n")
                
                if opex_fcfa_values:
                    file.write(f"- **OPEX min:** {min(opex_fcfa_values):.2f} FCFA/kWh\n")
                    file.write(f"- **OPEX max:** {max(opex_fcfa_values):.2f} FCFA/kWh\n")
                    file.write(f"- **OPEX moyen:** {sum(opex_fcfa_values)/len(opex_fcfa_values):.2f} FCFA/kWh\n\n")
                
                file.write(f"## 🔄 Conversion des Unités\n\n")
                file.write(f"- **Débits convertis:** m³/h → m³/s (divisé par 3600)\n")
                if debit_m3s_values:
                    file.write(f"- **Plage de débits (m³/s):** {min(debit_m3s_values):.6f} - {max(debit_m3s_values):.6f}\n")
                file.write(f"- **Prix convertis:** EUR → FCFA (× {self.eur_to_fcfa_rate:.3f})\n")
                file.write(f"- **OPEX estimé:** Basé sur puissance absorbée et coût électricité local\n\n")
                
                file.write(f"## 📁 Fichiers Générés\n\n")
                file.write(f"- **YAML:** `{yaml_file}`\n")
                file.write(f"- **SQLite:** `{sqlite_file}`\n")
                file.write(f"- **Log:** `conversion.log`\n\n")
                
                file.write(f"## 🔍 Validation des Données\n\n")
                file.write(f"- **Lignes parsées:** {len(data)}\n")
                file.write(f"- **Désignations uniques:** {len(set(row['designation'] for row in data))}\n")
                file.write(f"- **Données complètes:** {len([row for row in data if all(row.values())])}\n\n")
                
                file.write(f"## 📋 Marques Disponibles\n\n")
                for marque in sorted(marques):
                    count = len([row for row in data if row['marque'] == marque])
                    file.write(f"- **{marque}:** {count} pompes\n")
                
                file.write(f"\n## ✅ Conversion Terminée avec Succès\n\n")
                file.write(f"Les données ont été converties et sont prêtes pour:\n")
                file.write(f"- **Tests:** Utilisez le fichier YAML\n")
                file.write(f"- **Production:** Utilisez la base SQLite\n")
                file.write(f"- **EPANET:** Débits en m³/s, coûts en FCFA\n")
                file.write(f"- **Optimisation:** OPEX estimé basé sur la puissance absorbée\n")
            
            self.logger.info(f"✅ Rapport généré: {report_file}")
            return str(report_file)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération du rapport: {e}")
            raise
    
    def convert(self, output_formats: List[str] = None) -> Dict[str, str]:
        """Convertit les données vers les formats spécifiés"""
        if output_formats is None:
            output_formats = ['yaml', 'sqlite']
        
        self.logger.info(f"🚀 Début de la conversion vers: {', '.join(output_formats)}")
        
        # Parsing du CSV
        data = self.parse_csv()
        
        results = {}
        
        # Conversion vers les formats demandés
        if 'yaml' in output_formats:
            yaml_file = self.to_yaml(data)
            results['yaml'] = yaml_file
        
        if 'sqlite' in output_formats:
            sqlite_file = self.to_sqlite(data)
            results['sqlite'] = sqlite_file
        
        # Génération du rapport
        if results:
            report_file = self.generate_report(data, 
                                            results.get('yaml', ''), 
                                            results.get('sqlite', ''))
            results['report'] = report_file
        
        self.logger.info("🎉 Conversion terminée avec succès!")
        return results


def main():
    """Fonction principale du CLI"""
    parser = argparse.ArgumentParser(
        description="Convertisseur CSV → YAML/SQLite pour base de données de pompes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  # Conversion complète (YAML + SQLite) avec paramètres par défaut
  python csv_to_yaml_sqlite_converter.py grundfos_pompes.csv
  
  # Conversion avec taux de change personnalisé
  python csv_to_yaml_sqlite_converter.py grundfos_pompes.csv --eur-fcfa 700
  
  # Conversion avec coût électricité personnalisé
  python csv_to_yaml_sqlite_converter.py grundfos_pompes.csv --energy-cost 100
  
  # Conversion YAML uniquement
  python csv_to_yaml_sqlite_converter.py grundfos_pompes.csv --formats yaml
  
  # Conversion SQLite uniquement
  python csv_to_yaml_sqlite_converter.py grundfos_pompes.csv --formats sqlite
  
  # Dossier de sortie personnalisé
  python csv_to_yaml_sqlite_converter.py grundfos_pompes.csv --output ./ma_sortie
        """
    )
    
    parser.add_argument('csv_file', help='Fichier CSV source à convertir')
    parser.add_argument('--output', '-o', default='output', 
                       help='Dossier de sortie (défaut: output)')
    parser.add_argument('--formats', '-f', nargs='+', 
                       choices=['yaml', 'sqlite'], default=['yaml', 'sqlite'],
                       help='Formats de sortie (défaut: yaml sqlite)')
    parser.add_argument('--eur-fcfa', type=float, default=655.957,
                       help='Taux de change EUR → FCFA (défaut: 655.957)')
    parser.add_argument('--energy-cost', type=float, default=98.39,
                       help='Coût électricité en FCFA/kWh (défaut: 98.39)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Mode verbeux')
    
    args = parser.parse_args()
    
    try:
        # Configuration du logging
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Affichage des paramètres de conversion
        print(f"🔄 Paramètres de conversion:")
        print(f"   - Taux de change: 1 EUR = {args.eur_fcfa:.3f} FCFA")
        print(f"   - Coût électricité: {args.energy_cost:.2f} FCFA/kWh")
        print()
        
        # Création du convertisseur
        converter = PumpDataConverter(
            args.csv_file, 
            args.output,
            eur_to_fcfa_rate=args.eur_fcfa,
            energy_cost_fcfa_kwh=args.energy_cost
        )
        
        # Conversion
        results = converter.convert(args.formats)
        
        # Affichage des résultats
        print("\n" + "="*60)
        print("🎉 CONVERSION TERMINÉE AVEC SUCCÈS!")
        print("="*60)
        
        for format_type, file_path in results.items():
            if format_type == 'report':
                print(f"📋 Rapport: {file_path}")
            else:
                print(f"✅ {format_type.upper()}: {file_path}")
        
        print(f"\n📁 Tous les fichiers sont dans: {args.output}")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Erreur lors de la conversion: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
