"""
Module de diagnostic de connectivité réseau pour LCPI AEP

Ce module fournit des outils pour diagnostiquer les problèmes de connectivité
dans les réseaux hydrauliques, notamment pour résoudre l'erreur EPANET 110.
"""

import networkx as nx
from typing import Dict, List, Any, Set, Tuple
import logging

try:
    from .network_utils import NetworkUtils
except ImportError:
    # Fallback pour les imports dynamiques
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    network_utils_path = os.path.join(current_dir, "network_utils.py")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location("network_utils", network_utils_path)
    network_utils_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(network_utils_module)
    NetworkUtils = network_utils_module.NetworkUtils

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def diagnose_network_connectivity(network_data: Dict[str, Any]) -> bool:
    """
    Diagnostique la connectivité d'un réseau hydraulique.
    
    Cette fonction analyse la structure du réseau pour identifier les problèmes
    de connectivité qui peuvent causer l'erreur EPANET 110 "cannot solve network 
    hydraulic equations".
    
    Args:
        network_data: Données du réseau au format LCPI
            {
                "network": {
                    "nodes": {
                        "node_id": {
                            "type": "reservoir" | "junction" | "tank",
                            "cote": elevation,
                            "demande": demand,
                            ...
                        }
                    },
                    "pipes": {
                        "pipe_id": {
                            "noeud_amont": "from_node_id",
                            "noeud_aval": "to_node_id",
                            ...
                        }
                    }
                }
            }
    
    Returns:
        bool: True si le réseau est entièrement alimenté, False sinon
        
    Raises:
        ValueError: Si les données réseau sont invalides
    """
    
    print("🔍 DIAGNOSTIC DE CONNECTIVITÉ RÉSEAU")
    print("=" * 50)
    
    try:
        # Validation des données d'entrée
        if not network_data or "network" not in network_data:
            raise ValueError("Données réseau invalides: clé 'network' manquante")
        
        network = network_data["network"]
        nodes_data = network.get("nodes", {})
        pipes_data = network.get("pipes", {})
        
        if not nodes_data:
            raise ValueError("Aucun nœud trouvé dans les données réseau")
        
        if not pipes_data:
            raise ValueError("Aucune conduite trouvée dans les données réseau")
        
        print(f"📊 Statistiques du réseau:")
        print(f"   • Nœuds: {len(nodes_data)}")
        print(f"   • Conduites: {len(pipes_data)}")
        
        # 1. Construction du graphe NetworkX
        print("\n🔧 Construction du graphe réseau...")
        G = nx.Graph()
        
        # Ajouter tous les nœuds
        for node_id, node_data in nodes_data.items():
            G.add_node(node_id, **node_data)
        
        # Ajouter toutes les conduites
        for pipe_id, pipe_data in pipes_data.items():
            node1, node2 = NetworkUtils.get_pipe_nodes(pipe_data)
            
            if node1 and node2 and node1 != node2:
                G.add_edge(node1, node2, pipe_id=pipe_id, **pipe_data)
            else:
                print(f"⚠️  Conduite '{pipe_id}' ignorée: nœuds invalides ({node1} -> {node2})")
        
        print(f"   • Nœuds dans le graphe: {G.number_of_nodes()}")
        print(f"   • Conduites dans le graphe: {G.number_of_edges()}")
        
        # 2. Identification des sources d'eau
        print("\n💧 Identification des sources d'eau...")
        water_sources = NetworkUtils.identify_water_sources(network_data)
        
        for node_id in water_sources:
            node_type = NetworkUtils.get_node_type(nodes_data[node_id])
            print(f"   • Source d'eau trouvée: {node_id} (type: {node_type})")
        
        if not water_sources:
            print("❌ ERREUR CRITIQUE: Aucune source d'eau (réservoir/tank) trouvée dans le réseau!")
            print("   EPANET nécessite au moins une source d'eau pour résoudre les équations hydrauliques.")
            return False
        
        print(f"   • Total sources d'eau: {len(water_sources)}")
        
        # 3. Analyse des composantes connexes
        print("\n🔗 Analyse des composantes connexes...")
        connected_components = list(nx.connected_components(G))
        
        print(f"   • Nombre de composantes connexes: {len(connected_components)}")
        
        # 4. Vérification de l'alimentation de chaque composante
        orphaned_components = []
        fed_components = []
        
        for i, component in enumerate(connected_components):
            component_sources = component.intersection(water_sources)
            
            if component_sources:
                fed_components.append({
                    "id": i + 1,
                    "nodes": component,
                    "sources": component_sources,
                    "size": len(component)
                })
                print(f"   ✅ Composante {i+1}: {len(component)} nœuds, alimentée par {len(component_sources)} source(s)")
            else:
                orphaned_components.append({
                    "id": i + 1,
                    "nodes": component,
                    "size": len(component)
                })
                print(f"   ❌ Composante {i+1}: {len(component)} nœuds, AUCUNE SOURCE D'EAU")
        
        # 5. Rapport détaillé des composantes orphelines
        if orphaned_components:
            print(f"\n🚨 PROBLÈME DÉTECTÉ: {len(orphaned_components)} composante(s) orpheline(s)")
            print("=" * 50)
            
            for orphan in orphaned_components:
                print(f"\n📋 Composante orpheline #{orphan['id']}:")
                print(f"   • Taille: {orphan['size']} nœuds")
                print(f"   • Nœuds: {sorted(list(orphan['nodes']))[:10]}{'...' if len(orphan['nodes']) > 10 else ''}")
                
                # Identifier les nœuds les plus proches des sources
                if water_sources:
                    closest_sources = _find_closest_sources(G, orphan['nodes'], water_sources)
                    print(f"   • Sources les plus proches: {closest_sources[:5]}")
        
        # 6. Statistiques finales
        print(f"\n📈 RÉSUMÉ DU DIAGNOSTIC")
        print("=" * 30)
        print(f"   • Composantes alimentées: {len(fed_components)}")
        print(f"   • Composantes orphelines: {len(orphaned_components)}")
        print(f"   • Nœuds alimentés: {sum(c['size'] for c in fed_components)}")
        print(f"   • Nœuds orphelins: {sum(c['size'] for c in orphaned_components)}")
        
        # 7. Recommandations
        if orphaned_components:
            print(f"\n💡 RECOMMANDATIONS:")
            print("   • Ajouter des réservoirs ou tanks dans les composantes orphelines")
            print("   • Vérifier la connectivité des conduites")
            print("   • S'assurer que toutes les parties du réseau sont accessibles depuis une source")
            print("   • Considérer l'ajout de conduites de connexion si nécessaire")
            
            return False
        else:
            print(f"\n✅ RÉSEAU ENTIÈREMENT ALIMENTÉ")
            print("   • Toutes les composantes contiennent au moins une source d'eau")
            print("   • Le réseau devrait être résolvable par EPANET")
            
            return True
            
    except Exception as e:
        print(f"❌ ERREUR LORS DU DIAGNOSTIC: {e}")
        logger.error(f"Erreur dans diagnose_network_connectivity: {e}", exc_info=True)
        raise


def _find_closest_sources(G: nx.Graph, orphan_nodes: Set[str], water_sources: Set[str]) -> List[Tuple[str, int]]:
    """
    Trouve les sources d'eau les plus proches d'un ensemble de nœuds orphelins.
    
    Args:
        G: Graphe NetworkX du réseau
        orphan_nodes: Ensemble des nœuds orphelins
        water_sources: Ensemble des sources d'eau
        
    Returns:
        Liste des (source_id, distance_minimale) triée par distance
    """
    closest_sources = []
    
    for source in water_sources:
        if source in G:
            min_distance = float('inf')
            
            for orphan in orphan_nodes:
                if orphan in G:
                    try:
                        distance = nx.shortest_path_length(G, source, orphan)
                        min_distance = min(min_distance, distance)
                    except nx.NetworkXNoPath:
                        continue
            
            if min_distance != float('inf'):
                closest_sources.append((source, min_distance))
    
    # Trier par distance croissante
    closest_sources.sort(key=lambda x: x[1])
    return closest_sources


def analyze_network_topology(network_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyse approfondie de la topologie du réseau.
    
    Args:
        network_data: Données du réseau au format LCPI
        
    Returns:
        Dict contenant les analyses de topologie
    """
    print("\n🔬 ANALYSE TOPOLOGIQUE APPROFONDIE")
    print("=" * 40)
    
    try:
        network = network_data["network"]
        nodes_data = network.get("nodes", {})
        pipes_data = network.get("pipes", {})
        
        # Construction du graphe
        G = nx.Graph()
        
        for node_id, node_data in nodes_data.items():
            G.add_node(node_id, **node_data)
        
        for pipe_id, pipe_data in pipes_data.items():
            node1, node2 = NetworkUtils.get_pipe_nodes(pipe_data)
            if node1 and node2 and node1 != node2:
                G.add_edge(node1, node2, pipe_id=pipe_id, **pipe_data)
            else:
                print(f"⚠️  Conduite '{pipe_id}' ignorée dans analyze_network_topology: nœuds invalides ({node1} -> {node2})")
        
        # Analyses topologiques
        analysis = {
            "nombre_noeuds": G.number_of_nodes(),
            "nombre_conduites": G.number_of_edges(),
            "composantes_connexes": len(list(nx.connected_components(G))),
            "densite": nx.density(G),
            "diametre": nx.diameter(G) if nx.is_connected(G) else "Infini (réseau non connexe)",
            "rayon": nx.radius(G) if nx.is_connected(G) else "Infini (réseau non connexe)",
            "centre": list(nx.center(G)) if nx.is_connected(G) else [],
            "peripherie": list(nx.periphery(G)) if nx.is_connected(G) else [],
            "degre_moyen": sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0,
            "degre_max": max(dict(G.degree()).values()) if G.number_of_nodes() > 0 else 0,
            "degre_min": min(dict(G.degree()).values()) if G.number_of_nodes() > 0 else 0
        }
        
        # Affichage des résultats
        print(f"   • Densité du réseau: {analysis['densite']:.4f}")
        print(f"   • Degré moyen: {analysis['degre_moyen']:.2f}")
        print(f"   • Degré min/max: {analysis['degre_min']}/{analysis['degre_max']}")
        
        if nx.is_connected(G):
            print(f"   • Diamètre: {analysis['diametre']}")
            print(f"   • Rayon: {analysis['rayon']}")
            print(f"   • Centre: {analysis['centre']}")
        else:
            print(f"   • ⚠️  Réseau non connexe: {analysis['composantes_connexes']} composantes")
        
        # Identification des nœuds critiques
        if nx.is_connected(G):
            articulation_points = list(nx.articulation_points(G))
            bridges = list(nx.bridges(G))
            
            analysis["points_articulation"] = articulation_points
            analysis["ponts"] = bridges
            
            print(f"   • Points d'articulation: {len(articulation_points)}")
            print(f"   • Ponts (conduites critiques): {len(bridges)}")
            
            if articulation_points:
                print(f"     - Points critiques: {articulation_points[:5]}{'...' if len(articulation_points) > 5 else ''}")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse topologique: {e}")
        return {}


def validate_epanet_compatibility(network_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide la compatibilité du réseau avec EPANET.
    
    Args:
        network_data: Données du réseau au format LCPI
        
    Returns:
        Dict contenant les validations EPANET
    """
    print("\n🔧 VALIDATION COMPATIBILITÉ EPANET")
    print("=" * 35)
    
    validation = {
        "compatible": True,
        "erreurs": [],
        "avertissements": [],
        "recommandations": []
    }
    
    try:
        network = network_data["network"]
        nodes_data = network.get("nodes", {})
        pipes_data = network.get("pipes", {})
        
        # 1. Vérification des sources d'eau
        water_sources = [nid for nid, ndata in nodes_data.items() 
                        if ndata.get("type", "").lower() in ["reservoir", "tank"]]
        
        if not water_sources:
            validation["compatible"] = False
            validation["erreurs"].append("Aucune source d'eau (réservoir/tank) trouvée")
        else:
            print(f"✅ Sources d'eau: {len(water_sources)} trouvée(s)")
        
        # 2. Vérification de la connectivité
        G = nx.Graph()
        for node_id in nodes_data:
            G.add_node(node_id)
        
        for pipe_id, pipe_data in pipes_data.items():
            node1, node2 = NetworkUtils.get_pipe_nodes(pipe_data)
            if node1 and node2 and node1 != node2:
                G.add_edge(node1, node2)
            else:
                print(f"⚠️  Conduite '{pipe_id}' ignorée dans validate_epanet_compatibility: nœuds invalides ({node1} -> {node2})")
        
        if not nx.is_connected(G):
            validation["compatible"] = False
            validation["erreurs"].append("Réseau non connexe - composantes isolées détectées")
        else:
            print("✅ Réseau connexe")
        
        # 3. Vérification des données de conduites
        invalid_pipes = []
        for pipe_id, pipe_data in pipes_data.items():
            diameter = NetworkUtils.get_pipe_diameter(pipe_data)
            length = NetworkUtils.get_pipe_length(pipe_data)
            if not diameter > 0:
                invalid_pipes.append(pipe_id)
            if not length > 0:
                invalid_pipes.append(pipe_id)
        
        if invalid_pipes:
            validation["avertissements"].append(f"Conduites avec dimensions invalides: {invalid_pipes[:5]}")
        
        # 4. Vérification des demandes
        negative_demands = [nid for nid, ndata in nodes_data.items() 
                           if NetworkUtils.get_node_demand(ndata) < 0]
        
        if negative_demands:
            validation["avertissements"].append(f"Nœuds avec demandes négatives: {negative_demands[:5]}")
        
        # 5. Recommandations générales
        if len(nodes_data) > 1000:
            validation["recommandations"].append("Réseau de grande taille - considérer l'optimisation")
        
        if len(pipes_data) > 2000:
            validation["recommandations"].append("Nombre élevé de conduites - vérifier la convergence")
        
        # Affichage des résultats
        if validation["erreurs"]:
            print("❌ Erreurs critiques:")
            for error in validation["erreurs"]:
                print(f"   • {error}")
        
        if validation["avertissements"]:
            print("⚠️  Avertissements:")
            for warning in validation["avertissements"]:
                print(f"   • {warning}")
        
        if validation["recommandations"]:
            print("💡 Recommandations:")
            for rec in validation["recommandations"]:
                print(f"   • {rec}")
        
        if validation["compatible"]:
            print("✅ Réseau compatible avec EPANET")
        else:
            print("❌ Réseau incompatible avec EPANET")
        
        return validation
        
    except Exception as e:
        validation["compatible"] = False
        validation["erreurs"].append(f"Erreur lors de la validation: {e}")
        print(f"❌ Erreur lors de la validation: {e}")
        return validation 