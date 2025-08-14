#!/usr/bin/env python3
"""
Script de génération d'un grand réseau de type Paris pour tester l'algorithme Hardy-Cross

Ce script génère un réseau complexe similaire à celui de Paris avec :
- Plusieurs boucles interconnectées
- Différents diamètres de conduites
- Demandes réalistes par arrondissement
- Structure logique de distribution
"""

import csv
import yaml
import random
import math
from pathlib import Path
from typing import Dict, List, Tuple

class ParisNetworkGenerator:
    """Générateur de réseau de type Paris"""
    
    def __init__(self):
        self.arrondissements = 20
        self.reservoirs = 3
        self.stations_pompage = 5
        self.diametres_disponibles = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5]
        self.coefficients_rugosite = [120, 130, 140]  # Acier, Fonte, PVC
        
    def generate_nodes(self) -> List[Dict]:
        """Génère les nœuds du réseau"""
        nodes = []
        
        # Réservoirs principaux
        for i in range(self.reservoirs):
            nodes.append({
                "id": f"R{i+1}",
                "type": "reservoir",
                "cote": 100 + i * 10,  # Altitude différente
                "capacite": 50000 + i * 10000,  # m³
                "demande": 0
            })
        
        # Stations de pompage
        for i in range(self.stations_pompage):
            nodes.append({
                "id": f"SP{i+1}",
                "type": "station_pompage",
                "cote": 80 + i * 5,
                "puissance": 100 + i * 50,  # kW
                "demande": 0
            })
        
        # Nœuds de distribution par arrondissement
        for arr in range(1, self.arrondissements + 1):
            # Nœud principal de l'arrondissement
            nodes.append({
                "id": f"A{arr:02d}",
                "type": "arrondissement",
                "cote": 50 + random.randint(-10, 10),
                "demande": 1000 + random.randint(500, 2000),  # m³/jour
                "population": 50000 + random.randint(20000, 80000)
            })
            
            # Nœuds secondaires (2-3 par arrondissement)
            for j in range(random.randint(2, 4)):
                nodes.append({
                    "id": f"A{arr:02d}_{j+1}",
                    "type": "distribution",
                    "cote": 45 + random.randint(-5, 5),
                    "demande": 200 + random.randint(100, 500),
                    "parent": f"A{arr:02d}"
                })
        
        return nodes
    
    def generate_pipes(self, nodes: List[Dict]) -> List[Dict]:
        """Génère les conduites du réseau"""
        pipes = []
        pipe_id = 1
        
        # Extraire les IDs des nœuds
        node_ids = [node["id"] for node in nodes]
        
        # Connexions réservoirs -> stations de pompage
        for i in range(self.reservoirs):
            for j in range(self.stations_pompage):
                if random.random() < 0.7:  # 70% de chance de connexion
                    pipes.append({
                        "id": f"P{pipe_id:04d}",
                        "noeud_amont": f"R{i+1}",
                        "noeud_aval": f"SP{j+1}",
                        "longueur": random.randint(500, 2000),
                        "diametre": random.choice([0.6, 0.8, 1.0, 1.2]),
                        "coefficient_rugosite": random.choice(self.coefficients_rugosite),
                        "debit_initial": random.randint(100, 500)
                    })
                    pipe_id += 1
        
        # Connexions stations de pompage -> arrondissements
        for i in range(self.stations_pompage):
            for arr in range(1, self.arrondissements + 1):
                if random.random() < 0.6:  # 60% de chance de connexion
                    pipes.append({
                        "id": f"P{pipe_id:04d}",
                        "noeud_amont": f"SP{i+1}",
                        "noeud_aval": f"A{arr:02d}",
                        "longueur": random.randint(1000, 3000),
                        "diametre": random.choice([0.4, 0.5, 0.6, 0.8]),
                        "coefficient_rugosite": random.choice(self.coefficients_rugosite),
                        "debit_initial": random.randint(50, 300)
                    })
                    pipe_id += 1
        
        # Connexions entre arrondissements (boucles)
        for arr1 in range(1, self.arrondissements + 1):
            for arr2 in range(arr1 + 1, self.arrondissements + 1):
                if random.random() < 0.3:  # 30% de chance de connexion
                    pipes.append({
                        "id": f"P{pipe_id:04d}",
                        "noeud_amont": f"A{arr1:02d}",
                        "noeud_aval": f"A{arr2:02d}",
                        "longueur": random.randint(800, 2500),
                        "diametre": random.choice([0.3, 0.4, 0.5, 0.6]),
                        "coefficient_rugosite": random.choice(self.coefficients_rugosite),
                        "debit_initial": random.randint(20, 150)
                    })
                    pipe_id += 1
        
        # Connexions internes aux arrondissements
        for arr in range(1, self.arrondissements + 1):
            arr_nodes = [n for n in nodes if n["id"].startswith(f"A{arr:02d}")]
            for i, node1 in enumerate(arr_nodes):
                for node2 in arr_nodes[i+1:]:
                    if random.random() < 0.5:  # 50% de chance de connexion
                        pipes.append({
                            "id": f"P{pipe_id:04d}",
                            "noeud_amont": node1["id"],
                            "noeud_aval": node2["id"],
                            "longueur": random.randint(200, 800),
                            "diametre": random.choice([0.2, 0.25, 0.3, 0.4]),
                            "coefficient_rugosite": random.choice(self.coefficients_rugosite),
                            "debit_initial": random.randint(10, 100)
                        })
                        pipe_id += 1
        
        return pipes
    
    def generate_network_data(self) -> Dict:
        """Génère les données complètes du réseau"""
        nodes = self.generate_nodes()
        pipes = self.generate_pipes(nodes)
        
        return {
            "metadata": {
                "nom": "Réseau Paris Type",
                "description": "Réseau de distribution d'eau similaire à Paris",
                "date_creation": "2025-08-04",
                "generateur": "ParisNetworkGenerator",
                "statistiques": {
                    "nombre_noeuds": len(nodes),
                    "nombre_conduites": len(pipes),
                    "nombre_reservoirs": self.reservoirs,
                    "nombre_stations_pompage": self.stations_pompage,
                    "nombre_arrondissements": self.arrondissements
                }
            },
            "network": {
                "nodes": {node["id"]: node for node in nodes},
                "pipes": {pipe["id"]: pipe for pipe in pipes}
            }
        }
    
    def export_to_csv(self, network_data: Dict, output_path: str):
        """Exporte le réseau au format CSV"""
        pipes = list(network_data["network"]["pipes"].values())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'pipe_id', 'from_node', 'to_node', 'length', 'diameter', 
                'roughness', 'initial_flow'
            ])
            writer.writeheader()
            
            for pipe in pipes:
                writer.writerow({
                    'pipe_id': pipe['id'],
                    'from_node': pipe['noeud_amont'],
                    'to_node': pipe['noeud_aval'],
                    'length': pipe['longueur'],
                    'diameter': pipe['diametre'],
                    'roughness': pipe['coefficient_rugosite'],
                    'initial_flow': pipe['debit_initial']
                })
    
    def export_to_yaml(self, network_data: Dict, output_path: str):
        """Exporte le réseau au format YAML"""
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(network_data, f, default_flow_style=False, allow_unicode=True)

def main():
    """Fonction principale"""
    print("🌊 Génération du réseau Paris Type...")
    
    # Créer le générateur
    generator = ParisNetworkGenerator()
    
    # Générer les données du réseau
    network_data = generator.generate_network_data()
    
    # Créer le dossier de sortie
    output_dir = Path("output/paris_network")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Exporter en CSV
    csv_path = output_dir / "paris_network.csv"
    generator.export_to_csv(network_data, str(csv_path))
    
    # Exporter en YAML
    yaml_path = output_dir / "paris_network.yml"
    generator.export_to_yaml(network_data, str(yaml_path))
    
    # Afficher les statistiques
    stats = network_data["metadata"]["statistiques"]
    print(f"✅ Réseau généré avec succès !")
    print(f"📊 Statistiques:")
    print(f"   - Nœuds: {stats['nombre_noeuds']}")
    print(f"   - Conduites: {stats['nombre_conduites']}")
    print(f"   - Réservoirs: {stats['nombre_reservoirs']}")
    print(f"   - Stations de pompage: {stats['nombre_stations_pompage']}")
    print(f"   - Arrondissements: {stats['nombre_arrondissements']}")
    print(f"📁 Fichiers générés:")
    print(f"   - CSV: {csv_path}")
    print(f"   - YAML: {yaml_path}")
    
    return network_data

if __name__ == "__main__":
    main() 