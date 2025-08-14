"""
Méthode Hardy-Cross améliorée pour le dimensionnement de réseaux

Ce module implémente la méthode Hardy-Cross avec :
- Support CSV et YAML pour les données d'entrée
- Transparence mathématique complète
- Affichage des itérations
- Export des résultats
"""

import json
import yaml
import csv
import math
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import pandas as pd
import networkx as nx  # Ajout de NetworkX pour la théorie des graphes

"""
Module Hardy-Cross Enhanced pour LCPI

Ce module implémente la méthode Hardy-Cross améliorée pour l'analyse
des réseaux de distribution d'eau en boucle fermée.
"""

import csv
import yaml
import math
from typing import Dict, List, Any, Optional
from pathlib import Path

def load_hardy_cross_csv(csv_path: str) -> Dict[str, Any]:
    """
    Charge les données de réseau depuis un fichier CSV.
    
    Args:
        csv_path: Chemin vers le fichier CSV
        
    Returns:
        Dict: Données du réseau
    """
    network_data = {
        "troncons": [],
        "noeuds": set(),
        "metadata": {
            "source": "csv",
            "file": csv_path
        }
    }
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            troncon = {
                "id": row.get("pipe_id", f"P{len(network_data['troncons'])+1}"),
                "noeud_amont": row.get("from_node", ""),
                "noeud_aval": row.get("to_node", ""),
                "longueur": float(row.get("length", 0)),
                "diametre": float(row.get("diameter", 0)),
                "coefficient_rugosite": float(row.get("roughness", 120)),
                "debit_initial": float(row.get("initial_flow", 0))
            }
            network_data["troncons"].append(troncon)
            network_data["noeuds"].add(troncon["noeud_amont"])
            network_data["noeuds"].add(troncon["noeud_aval"])
    
    network_data["noeuds"] = list(network_data["noeuds"])
    return network_data

def load_hardy_cross_yaml(yaml_path: str) -> Dict[str, Any]:
    """
    Charge les données de réseau depuis un fichier YAML.
    
    Args:
        yaml_path: Chemin vers le fichier YAML
        
    Returns:
        Dict: Données du réseau
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    network_data = {
        "troncons": [],
        "noeuds": [],
        "metadata": data.get("metadata", {})
    }
    
    # Extraire les nœuds
    if "network" in data and "nodes" in data["network"]:
        for node_id, node_data in data["network"]["nodes"].items():
            noeud = {
                "id": node_id,
                "cote": node_data.get("elevation", 0),
                "demande": node_data.get("demand", 0)
            }
            network_data["noeuds"].append(noeud)
    
    # Extraire les tronçons
    if "network" in data and "pipes" in data["network"]:
        for pipe_id, pipe_data in data["network"]["pipes"].items():
            troncon = {
                "id": pipe_id,
                "noeud_amont": pipe_data.get("from_node", ""),
                "noeud_aval": pipe_data.get("to_node", ""),
                "longueur": pipe_data.get("length", 0),
                "diametre": pipe_data.get("diameter", 0),
                "coefficient_rugosite": pipe_data.get("roughness", 120),
                "debit_initial": pipe_data.get("initial_flow", 0)
            }
            network_data["troncons"].append(troncon)
    
    return network_data

def hardy_cross_network_enhanced(network_data: Dict[str, Any], max_iterations: int = 100, tolerance: float = 1e-6) -> Dict[str, Any]:
    """
    Exécute l'analyse Hardy-Cross sur un réseau.
    
    Args:
        network_data: Données du réseau
        max_iterations: Nombre maximum d'itérations
        tolerance: Tolérance de convergence
        
    Returns:
        Dict: Résultats de l'analyse
    """
    analyzer = HardyCrossEnhanced()
    analyzer.load_network_data(network_data)
    
    # Identifier les boucles automatiquement
    if "boucles" not in network_data:
        network_data["boucles"] = analyzer._identify_loops_robust(network_data["troncons"])
    
    return analyzer.hardy_cross_iteration(network_data, max_iterations, tolerance)

class HardyCrossEnhanced:
    """
    Implémentation améliorée de la méthode Hardy-Cross.
    
    Fonctionnalités :
    - Support CSV et YAML
    - Transparence mathématique
    - Affichage des itérations
    - Validation des données
    - Export des résultats
    """
    
    def __init__(self):
        """Initialise le calculateur Hardy-Cross."""
        self.iterations = []
        self.network_data = {}
        self.results = {}
    
    def load_network_data(self, network_data: Dict[str, Any]):
        """
        Charge les données de réseau.
        
        Args:
            network_data: Données du réseau
        """
        self.network_data = network_data
        
    def load_network_from_csv(self, csv_path: str) -> Dict[str, Any]:
        """
        Charge les données du réseau depuis un fichier CSV.
        
        Args:
            csv_path: Chemin vers le fichier CSV
            
        Returns:
            Dict: Données du réseau structurées
        """
        try:
            df = pd.read_csv(csv_path)
            
            # Structure attendue du CSV
            # noeud_debut, noeud_fin, longueur, diametre, coefficient_rugosite, debit_initial
            network = {
                "noeuds": [],
                "troncons": [],
                "boucles": []
            }
            
            # Extraire les nœuds uniques
            noeuds_debut = df['noeud_debut'].unique()
            noeuds_fin = df['noeud_fin'].unique()
            network["noeuds"] = list(set(noeuds_debut) | set(noeuds_fin))
            
            # Créer les tronçons
            for _, row in df.iterrows():
                troncon = {
                    "noeud_debut": row['noeud_debut'],
                    "noeud_fin": row['noeud_fin'],
                    "longueur": float(row['longueur']),
                    "diametre": float(row['diametre']),
                    "coefficient_rugosite": float(row['coefficient_rugosite']),
                    "debit_initial": float(row['debit_initial'])
                }
                network["troncons"].append(troncon)
            
            # Identifier les boucles automatiquement
            network["boucles"] = self._identify_loops_robust(network["troncons"])
            
            return network
            
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement du CSV: {e}")
    
    def load_network_from_yaml(self, yaml_path: str) -> Dict[str, Any]:
        """
        Charge les données du réseau depuis un fichier YAML.
        
        Args:
            yaml_path: Chemin vers le fichier YAML
            
        Returns:
            Dict: Données du réseau structurées
        """
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                network = yaml.safe_load(f)
            
            # Validation de la structure
            required_keys = ["noeuds", "troncons", "boucles"]
            for key in required_keys:
                if key not in network:
                    raise ValueError(f"Clé manquante dans le YAML: {key}")
            
            return network
            
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement du YAML: {e}")
    
    def _identify_loops_robust(self, troncons: List[Dict]) -> List[List[str]]:
        """
        Identifie les boucles du réseau via un processus robuste et multi-étapes.

        1.  **Diagnostic :** Calcule le nombre cyclomatique pour vérifier si des boucles peuvent exister.
        2.  **Adaptation :** Gère les réseaux non-connexes en analysant chaque composante séparément.
        3.  **Exécution :** Utilise l'algorithme des cycles fondamentaux de NetworkX pour une
            identification rapide et mathématiquement correcte.
        """
        print("\n--- DÉBUT DE L'ANALYSE TOPOLOGIQUE DU RÉSEAU ---")
        
        # --- ÉTAPE A : Construction du Graphe ---
        try:
            G = nx.Graph()
            for troncon in troncons:
                noeud_amont = troncon.get('noeud_amont') or troncon.get('noeud_debut')
                noeud_aval = troncon.get('noeud_aval') or troncon.get('noeud_fin')
                if noeud_amont and noeud_aval and noeud_amont != noeud_aval:
                    G.add_edge(noeud_amont, noeud_aval)
                else:
                    print(f"⚠️ Tronçon ignoré car invalide : {troncon}")
        except Exception as e:
            print(f"❌ Erreur critique lors de la construction du graphe : {e}")
            return []

        if G.number_of_nodes() == 0:
            print("❌ Le réseau est vide. Aucune boucle ne peut être trouvée.")
            return []

        # --- ÉTAPE B : Diagnostic via le Nombre Cyclomatique ---
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        num_components = nx.number_connected_components(G)
        cyclomatic_number = num_edges - num_nodes + num_components

        print(f"[Diagnostic] Nœuds: {num_nodes}, Conduites: {num_edges}, Parties Connexes: {num_components}")
        print(f"[Diagnostic] Nombre Cyclomatique (μ = E - N + C): {cyclomatic_number}")

        if cyclomatic_number <= 0:
            print("✅ Le réseau est arborescent (non-maillé). Il ne contient aucune boucle. Fin de l'analyse.")
            return []
        
        print("✅ Le réseau est maillé et doit contenir des boucles. Poursuite de l'analyse...")

        # --- ÉTAPES C & D : Adaptation et Exécution ---
        all_loops = []
        
        try:
            if num_components > 1:
                # --- C. Cas d'un réseau non-connexe ---
                print(f"⚠️ Le réseau est composé de {num_components} parties distinctes. Analyse de chaque partie.")
                
                # On récupère les sous-graphes de chaque composante connexe
                connected_subgraphs = (G.subgraph(c).copy() for c in nx.connected_components(G))
                
                for i, subgraph in enumerate(connected_subgraphs):
                    # On applique la méthode des cycles fondamentaux sur chaque morceau
                    loops_in_component = nx.cycle_basis(subgraph)
                    if loops_in_component:
                        print(f"  - Partie {i+1} : Trouvé {len(loops_in_component)} boucle(s).")
                        all_loops.extend(loops_in_component)
                    else:
                        print(f"  - Partie {i+1} : Arborescente, pas de boucle.")

            else:
                # --- D. Cas d'un réseau connexe (idéal) ---
                print("Le réseau est entièrement connexe. Recherche des boucles...")
                # Application directe de la méthode la plus efficace
                all_loops = nx.cycle_basis(G)

            print(f"\n--- RÉSULTAT DE L'ANALYSE ---")
            if all_loops:
                print(f"✅ Succès : {len(all_loops)} boucles fondamentales identifiées au total.")
            else:
                # Ce cas ne devrait pas arriver si le nombre cyclomatique > 0, mais c'est une sécurité
                print("⚠️ Avertissement : Aucune boucle trouvée malgré un nombre cyclomatique positif. Le réseau pourrait avoir une structure inhabituelle.")

            return all_loops

        except Exception as e:
            print(f"❌ Erreur critique lors de la recherche des cycles : {e}")
            return []

    def _identify_loops(self, troncons: List[Dict]) -> List[List[str]]:
        """
        Méthode de compatibilité qui appelle la version robuste.
        """
        return self._identify_loops_robust(troncons)
    
    def calculate_resistance_coefficient(self, longueur: float, diametre: float, 
                                      coefficient_rugosite: float) -> float:
        """
        Calcule le coefficient de résistance K pour un tronçon.
        
        Args:
            longueur: Longueur du tronçon (m)
            diametre: Diamètre du tronçon (m)
            coefficient_rugosite: Coefficient de rugosité (Hazen-Williams)
            
        Returns:
            float: Coefficient de résistance K
        """
        # Formule de Hazen-Williams pour K
        # K = 10.67 * L / (C^1.85 * D^4.87)
        
        K = 10.67 * longueur / (coefficient_rugosite**1.85 * diametre**4.87)
        
        return K
    
    def hardy_cross_iteration(self, network: Dict[str, Any], max_iterations: int = 100, 
                             tolerance: float = 1e-6) -> Dict[str, Any]:
        """
        Exécute la méthode Hardy-Cross avec affichage des itérations.
        
        Args:
            network: Données du réseau
            max_iterations: Nombre maximum d'itérations
            tolerance: Tolérance de convergence
            
        Returns:
            Dict: Résultats avec transparence mathématique
        """
        self.iterations = []
        troncons = network["troncons"]
        boucles = network["boucles"]
        
        # Initialiser les débits
        debits = {}
        for t in troncons:
            # Gérer les deux formats possibles
            if 'noeud_debut' in t and 'noeud_fin' in t:
                key = f"{t['noeud_debut']}-{t['noeud_fin']}"
                debits[key] = t['debit_initial']
            elif 'noeud_amont' in t and 'noeud_aval' in t:
                key = f"{t['noeud_amont']}-{t['noeud_aval']}"
                debits[key] = t['debit_initial']
        
        # Calculer les coefficients de résistance
        coefficients_K = {}
        for troncon in troncons:
            # Gérer les deux formats possibles
            if 'noeud_debut' in troncon and 'noeud_fin' in troncon:
                key = f"{troncon['noeud_debut']}-{troncon['noeud_fin']}"
            elif 'noeud_amont' in troncon and 'noeud_aval' in troncon:
                key = f"{troncon['noeud_amont']}-{troncon['noeud_aval']}"
            else:
                continue
            
            K = self.calculate_resistance_coefficient(
                troncon['longueur'],
                troncon['diametre'],
                troncon['coefficient_rugosite']
            )
            coefficients_K[key] = K
        
        # Itérations Hardy-Cross
        for iteration in range(max_iterations):
            iteration_data = {
                "iteration": iteration + 1,
                "debits": debits.copy(),
                "corrections": {},
                "formules": []
            }
            
            corrections_total = 0
            
            # Pour chaque boucle
            for i, boucle in enumerate(boucles):
                if len(boucle) < 3:  # Boucle trop petite
                    continue
                
                # Calculer Σ(KQ|Q|^0.85) et Σ(K|Q|^0.85)
                somme_KQ = 0
                somme_K = 0
                
                formule_parts = []
                
                # --- AJOUTER UNE VARIABLE DE DÉBOGAGE ---
                unfound_pipes_count = 0
                found_pipes_count = 0
                
                for j in range(len(boucle)):
                    noeud_actuel = boucle[j]
                    noeud_suivant = boucle[(j + 1) % len(boucle)]
                    
                    # Trouver le tronçon correspondant
                    troncon_key_forward = f"{noeud_actuel}-{noeud_suivant}"
                    troncon_key_backward = f"{noeud_suivant}-{noeud_actuel}"
                    
                    # --- MODIFICATION DE LA LOGIQUE DE RECHERCHE ---
                    if troncon_key_forward in debits:
                        troncon_key = troncon_key_forward
                        signe = 1
                        found_pipes_count += 1
                    elif troncon_key_backward in debits:
                        troncon_key = troncon_key_backward
                        signe = -1
                        found_pipes_count += 1
                    else:
                        # LE BUG EST PROBABLEMENT ICI !
                        unfound_pipes_count += 1
                        print(f"    ⚠️ [Debug] Tronçon non trouvé : {noeud_actuel} → {noeud_suivant}")
                        print(f"       - Clés cherchées : '{troncon_key_forward}', '{troncon_key_backward}'")
                        print(f"       - Clés disponibles : {list(debits.keys())[:5]}...")
                        continue # On ne peut rien faire, on passe au tronçon suivant
                    
                    Q = debits[troncon_key]
                    K = coefficients_K.get(troncon_key, 0)
                    
                    terme_KQ = signe * K * Q * abs(Q)**0.85
                    terme_K = K * abs(Q)**0.85
                    
                    somme_KQ += terme_KQ
                    somme_K += terme_K
                    
                    formule_parts.append(f"{signe} × {K:.4f} × {Q:.4f} × |{Q:.4f}|^0.85 = {terme_KQ:.4f}")
                
                # --- AJOUTER UN MESSAGE DE DÉBOGAGE APRÈS CHAQUE BOUCLE ---
                if unfound_pipes_count > 0:
                    print(f"  ⚠️ [Debug Itération {iteration+1}] Boucle {i+1}: Impossible de trouver {unfound_pipes_count} conduites sur {len(boucle)} (trouvées: {found_pipes_count})")
                    print(f"     Boucle : {boucle}")
                elif found_pipes_count > 0:
                    print(f"  ✅ [Debug Itération {iteration+1}] Boucle {i+1}: {found_pipes_count} conduites trouvées sur {len(boucle)}")
                
                # Calculer la correction ΔQ avec facteur de sous-relaxation
                if somme_K != 0:
                    # Vérifier que le dénominateur n'est pas trop petit
                    epsilon = 1e-10
                    if abs(somme_K) < epsilon:
                        delta_Q = 0
                    else:
                        delta_Q = -somme_KQ / (1.85 * somme_K)
                        
                        # Appliquer le facteur de sous-relaxation pour améliorer la convergence
                        relaxation_factor = 0.7
                        delta_Q_relaxed = delta_Q * relaxation_factor
                else:
                    delta_Q = 0
                    delta_Q_relaxed = 0
                
                correction_formule = f"ΔQ = -Σ(KQ|Q|^0.85) / (1.85 × Σ(K|Q|^0.85))"
                correction_calculation = f"ΔQ = -{somme_KQ:.4f} / (1.85 × {somme_K:.4f}) = {delta_Q:.6f}"
                
                iteration_data["corrections"][f"boucle_{i+1}"] = {
                    "delta_Q": delta_Q_relaxed,  # Utiliser la correction relaxée
                    "formule": correction_formule,
                    "calcul": correction_calculation,
                    "termes": formule_parts
                }
                
                # Appliquer la correction relaxée aux débits de la boucle
                for j in range(len(boucle)):
                    noeud_actuel = boucle[j]
                    noeud_suivant = boucle[(j + 1) % len(boucle)]
                    
                    troncon_key = f"{noeud_actuel}-{noeud_suivant}"
                    if troncon_key not in debits:
                        troncon_key = f"{noeud_suivant}-{noeud_actuel}"
                    
                    if troncon_key in debits:
                        # Appliquer la correction relaxée selon le sens
                        signe = 1 if troncon_key == f"{noeud_actuel}-{noeud_suivant}" else -1
                        debits[troncon_key] += signe * delta_Q_relaxed
                
                corrections_total += abs(delta_Q_relaxed)  # Utiliser la correction relaxée pour le total
            
            iteration_data["corrections_total"] = corrections_total
            self.iterations.append(iteration_data)
            
            # Vérifier la convergence
            if corrections_total < tolerance:
                break
        
        # --- DÉBUT DE LA CORRECTION ---
        
        # À la fin de la boucle, après la vérification de convergence, 
        # le dictionnaire 'debits' contient l'état final après la dernière itération.
        
        # Résultats finaux - CETTE SECTION S'EXÉCUTE TOUJOURS
        self.results = {
            "final_results": { # Assurer une structure cohérente
                "flows": debits,
                "pressures": {} # Le calcul des pressions n'est pas encore implémenté
            },
            "debits_finaux": debits, # Pour compatibilité
            "coefficients_K": coefficients_K,
            "iterations": self.iterations,
            "nombre_iterations": len(self.iterations),
            "convergence": corrections_total < tolerance,
            "tolerance_finale": corrections_total
        }
        
        print(f"  [Info] Calcul terminé. Convergence: {self.results['convergence']}. Tolérance finale: {self.results['tolerance_finale']:.6f}")
        
        return self.results
    
    def generate_mathematical_report(self) -> str:
        """
        Génère un rapport avec transparence mathématique.
        
        Returns:
            str: Rapport en Markdown
        """
        if not self.iterations:
            return "Aucune itération disponible."
        
        report = []
        report.append("# Rapport Hardy-Cross - Transparence Mathématique")
        report.append("")
        report.append("## Méthode Hardy-Cross")
        report.append("")
        report.append("La méthode Hardy-Cross est une méthode itérative pour résoudre les réseaux de distribution d'eau.")
        report.append("")
        report.append("### Formules Utilisées")
        report.append("")
        report.append("**1. Coefficient de résistance K (Hazen-Williams):**")
        report.append("")
        report.append("$$K = \\frac{10.67 \\times L}{C^{1.85} \\times D^{4.87}}$$")
        report.append("")
        report.append("Où :")
        report.append("- $L$ = Longueur du tronçon (m)")
        report.append("- $C$ = Coefficient de Hazen-Williams")
        report.append("- $D$ = Diamètre du tronçon (m)")
        report.append("")
        report.append("**2. Correction de débit ΔQ:**")
        report.append("")
        report.append("$$\\Delta Q = -\\frac{\\sum(KQ|Q|^{0.85})}{1.85 \\times \\sum(K|Q|^{0.85})}$$")
        report.append("")
        report.append("### Itérations Détaillées")
        report.append("")
        
        for iteration in self.iterations:
            report.append(f"#### Itération {iteration['iteration']}")
            report.append("")
            
            # Débits actuels
            report.append("**Débits actuels:**")
            report.append("")
            for troncon, debit in iteration['debits'].items():
                report.append(f"- {troncon}: {debit:.6f} m³/s")
            report.append("")
            
            # Corrections par boucle
            for boucle_name, correction in iteration['corrections'].items():
                report.append(f"**{boucle_name.upper()}:**")
                report.append("")
                report.append(f"**Formule:** {correction['formule']}")
                report.append("")
                report.append(f"**Calcul:** {correction['calcul']}")
                report.append("")
                report.append("**Termes détaillés:**")
                for terme in correction['termes']:
                    report.append(f"- {terme}")
                report.append("")
            
            report.append(f"**Correction totale:** {iteration['corrections_total']:.6f}")
            report.append("")
        
        # Résultats finaux
        if self.results:
            report.append("## Résultats Finaux")
            report.append("")
            report.append(f"**Nombre d'itérations:** {self.results['nombre_iterations']}")
            report.append(f"**Convergence:** {'✅ Oui' if self.results['convergence'] else '❌ Non'}")
            report.append(f"**Tolérance finale:** {self.results['tolerance_finale']:.6f}")
            report.append("")
            report.append("**Débits finaux:**")
            report.append("")
            for troncon, debit in self.results['debits_finaux'].items():
                report.append(f"- {troncon}: {debit:.6f} m³/s")
        
        return "\n".join(report)
    
    def export_results(self, format: str = "json") -> str:
        """
        Exporte les résultats dans différents formats.
        
        Args:
            format: Format d'export (json, csv, yaml, markdown)
            
        Returns:
            str: Contenu exporté
        """
        if format == "json":
            return json.dumps(self.results, indent=2, ensure_ascii=False)
        
        elif format == "csv":
            if not self.results.get('debits_finaux'):
                return ""
            
            lines = ["troncon,debit_m3s"]
            for troncon, debit in self.results['debits_finaux'].items():
                lines.append(f"{troncon},{debit:.6f}")
            
            return "\n".join(lines)
        
        elif format == "yaml":
            return yaml.dump(self.results, default_flow_style=False, allow_unicode=True)
        
        elif format == "markdown":
            return self.generate_mathematical_report()
        
        else:
            raise ValueError(f"Format non supporté: {format}")

# Fonctions d'interface pour CLI/REPL

def hardy_cross_from_csv(csv_path: str, max_iterations: int = 100, tolerance: float = 1e-6) -> Dict[str, Any]:
    """
    Exécute Hardy-Cross depuis un fichier CSV.
    
    Args:
        csv_path: Chemin vers le fichier CSV
        max_iterations: Nombre maximum d'itérations
        tolerance: Tolérance de convergence
        
    Returns:
        Dict: Résultats de l'analyse Hardy-Cross
    """
    try:
        # Charger les données CSV
        network_data = load_hardy_cross_csv(csv_path)
        
        # Exécuter l'analyse Hardy-Cross
        results = hardy_cross_network_enhanced(
            network_data, 
            max_iterations=max_iterations, 
            tolerance=tolerance
        )
        
        return {
            "status": "success",
            "input_file": csv_path,
            "results": results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "input_file": csv_path
        }

def hardy_cross_from_yaml(yaml_path: str, max_iterations: int = 100, tolerance: float = 1e-6) -> Dict[str, Any]:
    """
    Exécute Hardy-Cross depuis un fichier YAML.
    
    Args:
        yaml_path: Chemin vers le fichier YAML
        max_iterations: Nombre maximum d'itérations
        tolerance: Tolérance de convergence
        
    Returns:
        Dict: Résultats de l'analyse Hardy-Cross
    """
    try:
        # Charger les données YAML
        network_data = load_hardy_cross_yaml(yaml_path)
        
        # Exécuter l'analyse Hardy-Cross
        results = hardy_cross_network_enhanced(
            network_data, 
            max_iterations=max_iterations, 
            tolerance=tolerance
        )
        
        return {
            "status": "success",
            "input_file": yaml_path,
            "results": results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "input_file": yaml_path
        }

def export_hardy_cross_results(results: Dict[str, Any], output_path: str, format: str = "markdown") -> str:
    """
    Exporte les résultats Hardy-Cross dans différents formats.
    
    Args:
        results: Résultats de l'analyse Hardy-Cross
        output_path: Chemin de sortie
        format: Format d'export (markdown, json, csv, html)
        
    Returns:
        str: Contenu exporté
    """
    if format == "markdown":
        content = generate_hardy_cross_markdown_report(results)
    elif format == "json":
        import json
        content = json.dumps(results, indent=2, ensure_ascii=False)
    elif format == "csv":
        content = generate_hardy_cross_csv_report(results)
    elif format == "html":
        content = generate_hardy_cross_html_report(results)
    else:
        raise ValueError(f"Format non supporté: {format}")
    
    # Écrire le fichier
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return content

def generate_hardy_cross_markdown_report(results: Dict[str, Any]) -> str:
    """
    Génère un rapport Markdown pour l'analyse Hardy-Cross.
    
    Args:
        results: Résultats de l'analyse
        
    Returns:
        str: Rapport Markdown
    """
    lines = []
    
    # En-tête
    lines.append("# Rapport d'Analyse Hardy-Cross")
    lines.append("")
    lines.append(f"**Date:** {results.get('date', 'N/A')}")
    lines.append(f"**Fichier d'entrée:** {results.get('input_file', 'N/A')}")
    lines.append("")
    
    # Résumé
    if 'summary' in results:
        lines.append("## Résumé")
        lines.append("")
        summary = results['summary']
        lines.append(f"- **Nombre de nœuds:** {summary.get('num_nodes', 'N/A')}")
        lines.append(f"- **Nombre de conduites:** {summary.get('num_pipes', 'N/A')}")
        lines.append(f"- **Nombre de boucles:** {summary.get('num_loops', 'N/A')}")
        lines.append(f"- **Itérations:** {summary.get('iterations', 'N/A')}")
        lines.append(f"- **Convergence:** {'✅ Oui' if summary.get('converged', False) else '❌ Non'}")
        lines.append("")
    
    # Itérations détaillées
    if 'iterations' in results:
        lines.append("## Détail des Itérations")
        lines.append("")
        
        for i, iteration in enumerate(results['iterations'], 1):
            lines.append(f"### Itération {i}")
            lines.append("")
            
            if 'loop_corrections' in iteration:
                lines.append("**Corrections de boucle:**")
                lines.append("")
                for loop_id, correction in iteration['loop_corrections'].items():
                    lines.append(f"- Boucle {loop_id}: {correction:.6f} m³/s")
                lines.append("")
            
            if 'pipe_flows' in iteration:
                lines.append("**Débits des conduites:**")
                lines.append("")
                for pipe_id, flow in iteration['pipe_flows'].items():
                    lines.append(f"- Conduite {pipe_id}: {flow:.6f} m³/s")
                lines.append("")
            
            if 'max_correction' in iteration:
                lines.append(f"**Correction maximale:** {iteration['max_correction']:.6f} m³/s")
                lines.append("")
    
    # Résultats finaux
    if 'final_results' in results:
        lines.append("## Résultats Finaux")
        lines.append("")
        
        final = results['final_results']
        
        lines.append("### Débits des Conduites")
        lines.append("")
        for pipe_id, flow in final.get('pipe_flows', {}).items():
            lines.append(f"- **Conduite {pipe_id}:** {flow:.6f} m³/s")
        lines.append("")
        
        lines.append("### Pressions aux Nœuds")
        lines.append("")
        for node_id, pressure in final.get('node_pressures', {}).items():
            lines.append(f"- **Nœud {node_id}:** {pressure:.2f} m")
        lines.append("")
        
        lines.append("### Pertes de Charge")
        lines.append("")
        for pipe_id, head_loss in final.get('head_losses', {}).items():
            lines.append(f"- **Conduite {pipe_id}:** {head_loss:.2f} m")
        lines.append("")
    
    # Formules mathématiques
    lines.append("## Formules Mathématiques")
    lines.append("")
    lines.append("### Méthode Hardy-Cross")
    lines.append("")
    lines.append("La méthode Hardy-Cross utilise les formules suivantes :")
    lines.append("")
    lines.append("**1. Coefficient de résistance :**")
    lines.append("")
    lines.append("$$K = \\frac{8fL}{\\pi^2gD^5}$$")
    lines.append("")
    lines.append("Où :")
    lines.append("- $f$ = coefficient de frottement")
    lines.append("- $L$ = longueur de la conduite (m)")
    lines.append("- $g$ = accélération gravitationnelle (m/s²)")
    lines.append("- $D$ = diamètre de la conduite (m)")
    lines.append("")
    lines.append("**2. Perte de charge :**")
    lines.append("")
    lines.append("$$h_f = KQ^2$$")
    lines.append("")
    lines.append("**3. Correction de débit :**")
    lines.append("")
    lines.append("$$\\Delta Q = -\\frac{\\sum h_f}{2\\sum K|Q|}$$")
    lines.append("")
    
    return "\n".join(lines)

def generate_hardy_cross_csv_report(results: Dict[str, Any]) -> str:
    """
    Génère un rapport CSV pour l'analyse Hardy-Cross.
    
    Args:
        results: Résultats de l'analyse
        
    Returns:
        str: Rapport CSV
    """
    lines = []
    
    # En-tête
    lines.append("Type,ID,Valeur,Unité")
    
    # Résultats finaux
    if 'final_results' in results:
        final = results['final_results']
        
        # Débits des conduites
        for pipe_id, flow in final.get('pipe_flows', {}).items():
            lines.append(f"Pipe_Flow,{pipe_id},{flow:.6f},m³/s")
        
        # Pressions aux nœuds
        for node_id, pressure in final.get('node_pressures', {}).items():
            lines.append(f"Node_Pressure,{node_id},{pressure:.2f},m")
        
        # Pertes de charge
        for pipe_id, head_loss in final.get('head_losses', {}).items():
            lines.append(f"Head_Loss,{pipe_id},{head_loss:.2f},m")
    
    return "\n".join(lines)

def generate_hardy_cross_html_report(results: Dict[str, Any]) -> str:
    """
    Génère un rapport HTML pour l'analyse Hardy-Cross.
    
    Args:
        results: Résultats de l'analyse
        
    Returns:
        str: Rapport HTML
    """
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Rapport Hardy-Cross</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; margin-top: 30px; }
        h3 { color: #7f8c8d; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .success { color: green; }
        .error { color: red; }
        .iteration { background-color: #f9f9f9; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>Rapport d'Analyse Hardy-Cross</h1>
"""
    
    # Résumé
    if 'summary' in results:
        summary = results['summary']
        html += f"""
    <h2>Résumé</h2>
    <table>
        <tr><th>Paramètre</th><th>Valeur</th></tr>
        <tr><td>Nombre de nœuds</td><td>{summary.get('num_nodes', 'N/A')}</td></tr>
        <tr><td>Nombre de conduites</td><td>{summary.get('num_pipes', 'N/A')}</td></tr>
        <tr><td>Nombre de boucles</td><td>{summary.get('num_loops', 'N/A')}</td></tr>
        <tr><td>Itérations</td><td>{summary.get('iterations', 'N/A')}</td></tr>
        <tr><td>Convergence</td><td class="{'success' if summary.get('converged', False) else 'error'}">{'Oui' if summary.get('converged', False) else 'Non'}</td></tr>
    </table>
"""
    
    # Résultats finaux
    if 'final_results' in results:
        final = results['final_results']
        html += """
    <h2>Résultats Finaux</h2>
    <h3>Débits des Conduites</h3>
    <table>
        <tr><th>Conduite</th><th>Débit (m³/s)</th></tr>
"""
        
        for pipe_id, flow in final.get('pipe_flows', {}).items():
            html += f"        <tr><td>{pipe_id}</td><td>{flow:.6f}</td></tr>\n"
        
        html += """
    </table>
    
    <h3>Pressions aux Nœuds</h3>
    <table>
        <tr><th>Nœud</th><th>Pression (m)</th></tr>
"""
        
        for node_id, pressure in final.get('node_pressures', {}).items():
            html += f"        <tr><td>{node_id}</td><td>{pressure:.2f}</td></tr>\n"
        
        html += """
    </table>
"""
    
    html += """
</body>
</html>
"""
    
    return html

def get_hardy_cross_help() -> str:
    """
    Retourne l'aide pour la méthode Hardy-Cross.
    
    Returns:
        str: Texte d'aide
    """
    return """
# Méthode Hardy-Cross

## Description
La méthode Hardy-Cross est une méthode itérative pour résoudre les réseaux de distribution d'eau en boucle fermée.

## Principe
1. **Estimation initiale** : Attribution de débits initiaux aux conduites
2. **Calcul des pertes de charge** : Pour chaque conduite
3. **Vérification des boucles** : Calcul de la somme des pertes de charge
4. **Correction des débits** : Application des corrections de débit
5. **Itération** : Répétition jusqu'à convergence

## Formules
- **Coefficient de résistance :** K = 8fL/(π²gD⁵)
- **Perte de charge :** hf = KQ²
- **Correction de débit :** ΔQ = -Σhf/(2ΣK|Q|)

## Formats d'entrée
- **CSV** : Fichier avec colonnes (pipe_id, from_node, to_node, length, diameter, roughness)
- **YAML** : Structure hiérarchique avec nœuds et conduites

## Exemples d'utilisation
```bash
# Depuis un fichier CSV
lcpi aep hardy-cross-csv network.csv

# Depuis un fichier YAML
lcpi aep hardy-cross-yaml network.yml

# Avec options
lcpi aep hardy-cross-csv network.csv --max-iterations 50 --tolerance 1e-5
```
"""

# Fonctions utilitaires pour la conversion des fichiers Markdown
def convert_markdown_to_yaml(markdown_content: str) -> Dict[str, Any]:
    """
    Convertit le contenu d'un fichier Markdown Hardy-Cross en structure YAML.
    
    Args:
        markdown_content: Contenu du fichier Markdown
        
    Returns:
        Dict: Structure YAML
    """
    # Cette fonction peut être étendue pour parser les fichiers Markdown
    # et extraire les données de réseau
    return {
        "network": {
            "nodes": [],
            "pipes": []
        },
        "metadata": {
            "source": "markdown_conversion",
            "date": "2024-01-01"
        }
    }

def convert_markdown_to_csv(markdown_content: str) -> str:
    """
    Convertit le contenu d'un fichier Markdown Hardy-Cross en format CSV.
    
    Args:
        markdown_content: Contenu du fichier Markdown
        
    Returns:
        str: Contenu CSV
    """
    # En-tête CSV
    lines = ["pipe_id,from_node,to_node,length,diameter,roughness"]
    
    # Cette fonction peut être étendue pour parser les fichiers Markdown
    # et extraire les données de réseau
    
    return "\n".join(lines)