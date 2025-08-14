"""
Utilitaires pour la manipulation des données de réseau

Ce module fournit des méthodes d'assistance pour standardiser l'accès
aux données de réseau, notamment pour gérer les différentes conventions
de nommage des nœuds de conduites.
"""

from typing import Dict, Any, Optional, Tuple, List, Set
import networkx as nx


class NetworkUtils:
    """
    Classe utilitaire pour la manipulation des données de réseau.
    
    Cette classe fournit des méthodes d'assistance pour standardiser
    l'accès aux données de réseau et gérer les différentes conventions
    de nommage utilisées dans les projets hydrauliques.
    """
    
    @staticmethod
    def get_pipe_nodes(pipe_data: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """
        Extrait de manière flexible les nœuds de début et de fin d'une conduite.
        
        Cette méthode essaie plusieurs conventions de nommage communes pour garantir
        la compatibilité avec différents formats de données.
        
        Args:
            pipe_data: Le dictionnaire représentant les données d'une conduite.
            
        Returns:
            Un tuple contenant (noeud_debut, noeud_fin). Chacun peut être None 
            s'il n'est pas trouvé.
        """
        # Essayer différentes conventions de nommage pour le nœud de début
        node1 = (pipe_data.get('noeud_amont') or 
                 pipe_data.get('noeud_debut') or 
                 pipe_data.get('from_node') or
                 pipe_data.get('node1') or
                 pipe_data.get('start_node'))
        
        # Essayer différentes conventions de nommage pour le nœud de fin
        node2 = (pipe_data.get('noeud_aval') or 
                 pipe_data.get('noeud_fin') or 
                 pipe_data.get('to_node') or
                 pipe_data.get('node2') or
                 pipe_data.get('end_node'))
        
        return node1, node2
    
    @staticmethod
    def get_node_elevation(node_data: Dict[str, Any]) -> float:
        """
        Extrait l'élévation d'un nœud de manière flexible.
        
        Args:
            node_data: Le dictionnaire représentant les données d'un nœud.
            
        Returns:
            L'élévation du nœud (0.0 par défaut si non trouvée).
        """
        return (node_data.get('elevation') or 
                node_data.get('cote') or 
                node_data.get('altitude') or 
                node_data.get('z') or 
                0.0)
    
    @staticmethod
    def get_node_demand(node_data: Dict[str, Any]) -> float:
        """
        Extrait la demande d'un nœud de manière flexible.
        
        Args:
            node_data: Le dictionnaire représentant les données d'un nœud.
            
        Returns:
            La demande du nœud (0.0 par défaut si non trouvée).
        """
        return (node_data.get('demand') or 
                node_data.get('demande') or 
                node_data.get('flow') or 
                node_data.get('debit') or 
                0.0)
    
    @staticmethod
    def get_node_type(node_data: Dict[str, Any]) -> str:
        """
        Extrait le type d'un nœud de manière flexible.
        
        Args:
            node_data: Le dictionnaire représentant les données d'un nœud.
            
        Returns:
            Le type du nœud ('junction' par défaut si non trouvé).
        """
        node_type = (node_data.get('type') or 
                    node_data.get('node_type') or 
                    'junction')
        
        # Normaliser le type en minuscules
        return node_type.lower()
    
    @staticmethod
    def get_pipe_length(pipe_data: Dict[str, Any]) -> float:
        """
        Extrait la longueur d'une conduite de manière flexible.
        
        Args:
            pipe_data: Le dictionnaire représentant les données d'une conduite.
            
        Returns:
            La longueur de la conduite (0.0 par défaut si non trouvée).
        """
        return (pipe_data.get('length') or 
                pipe_data.get('longueur') or 
                pipe_data.get('l') or 
                0.0)
    
    @staticmethod
    def get_pipe_diameter(pipe_data: Dict[str, Any]) -> float:
        """
        Extrait le diamètre d'une conduite de manière flexible.
        
        Args:
            pipe_data: Le dictionnaire représentant les données d'une conduite.
            
        Returns:
            Le diamètre de la conduite (0.0 par défaut si non trouvé).
        """
        return (pipe_data.get('diameter') or 
                pipe_data.get('diametre') or 
                pipe_data.get('d') or 
                0.0)
    
    @staticmethod
    def get_pipe_roughness(pipe_data: Dict[str, Any]) -> float:
        """
        Extrait le coefficient de rugosité d'une conduite de manière flexible.
        
        Args:
            pipe_data: Le dictionnaire représentant les données d'une conduite.
            
        Returns:
            Le coefficient de rugosité (120.0 par défaut si non trouvé).
        """
        return (pipe_data.get('roughness') or 
                pipe_data.get('coefficient_rugosite') or 
                pipe_data.get('k') or 
                pipe_data.get('hazen_williams') or 
                120.0)
    
    @staticmethod
    def validate_network_structure(network_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valide la structure des données de réseau.
        
        Args:
            network_data: Les données du réseau à valider.
            
        Returns:
            Un tuple (is_valid, errors) où is_valid est un booléen indiquant
            si la structure est valide et errors est une liste des erreurs trouvées.
        """
        errors = []
        
        # Vérifier la présence de la clé 'network'
        if 'network' not in network_data:
            errors.append("Clé 'network' manquante dans les données")
            return False, errors
        
        network = network_data['network']
        
        # Vérifier la présence des nœuds
        if 'nodes' not in network:
            errors.append("Clé 'nodes' manquante dans network")
        elif not network['nodes']:
            errors.append("Aucun nœud trouvé dans les données")
        
        # Vérifier la présence des conduites
        if 'pipes' not in network:
            errors.append("Clé 'pipes' manquante dans network")
        elif not network['pipes']:
            errors.append("Aucune conduite trouvée dans les données")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def extract_all_node_ids(network_data: Dict[str, Any]) -> Set[str]:
        """
        Extrait tous les IDs de nœuds du réseau, y compris ceux référencés dans les conduites.
        
        Args:
            network_data: Les données du réseau.
            
        Returns:
            Un ensemble contenant tous les IDs de nœuds.
        """
        node_ids = set()
        
        # Ajouter les nœuds définis explicitement
        if 'network' in network_data and 'nodes' in network_data['network']:
            node_ids.update(network_data['network']['nodes'].keys())
        
        # Ajouter les nœuds référencés dans les conduites
        if 'network' in network_data and 'pipes' in network_data['network']:
            for pipe_data in network_data['network']['pipes'].values():
                node1, node2 = NetworkUtils.get_pipe_nodes(pipe_data)
                if node1:
                    node_ids.add(node1)
                if node2:
                    node_ids.add(node2)
        
        return node_ids
    
    @staticmethod
    def build_network_graph(network_data: Dict[str, Any]) -> nx.Graph:
        """
        Construit un graphe NetworkX à partir des données de réseau.
        
        Args:
            network_data: Les données du réseau.
            
        Returns:
            Un graphe NetworkX représentant le réseau.
        """
        G = nx.Graph()
        
        # Ajouter tous les nœuds
        if 'network' in network_data and 'nodes' in network_data['network']:
            for node_id, node_data in network_data['network']['nodes'].items():
                G.add_node(node_id, **node_data)
        
        # Ajouter toutes les conduites
        if 'network' in network_data and 'pipes' in network_data['network']:
            for pipe_id, pipe_data in network_data['network']['pipes'].items():
                node1, node2 = NetworkUtils.get_pipe_nodes(pipe_data)
                
                if node1 and node2 and node1 != node2:
                    G.add_edge(node1, node2, pipe_id=pipe_id, **pipe_data)
                else:
                    print(f"⚠️  Conduite '{pipe_id}' ignorée: nœuds invalides ({node1} -> {node2})")
        
        return G
    
    @staticmethod
    def identify_water_sources(network_data: Dict[str, Any]) -> Set[str]:
        """
        Identifie toutes les sources d'eau dans le réseau.
        
        Args:
            network_data: Les données du réseau.
            
        Returns:
            Un ensemble contenant les IDs des sources d'eau.
        """
        water_sources = set()
        
        if 'network' in network_data and 'nodes' in network_data['network']:
            for node_id, node_data in network_data['network']['nodes'].items():
                node_type = NetworkUtils.get_node_type(node_data)
                if node_type in ['reservoir', 'tank']:
                    water_sources.add(node_id)
        
        return water_sources
    
    @staticmethod
    def format_network_summary(network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère un résumé formaté du réseau.
        
        Args:
            network_data: Les données du réseau.
            
        Returns:
            Un dictionnaire contenant le résumé du réseau.
        """
        summary = {
            'total_nodes': 0,
            'total_pipes': 0,
            'water_sources': 0,
            'junctions': 0,
            'tanks': 0,
            'orphaned_nodes': 0,
            'connected_components': 0
        }
        
        # Compter les nœuds par type
        if 'network' in network_data and 'nodes' in network_data['network']:
            summary['total_nodes'] = len(network_data['network']['nodes'])
            
            for node_data in network_data['network']['nodes'].values():
                node_type = NetworkUtils.get_node_type(node_data)
                if node_type == 'reservoir':
                    summary['water_sources'] += 1
                elif node_type == 'tank':
                    summary['tanks'] += 1
                elif node_type == 'junction':
                    summary['junctions'] += 1
        
        # Compter les conduites
        if 'network' in network_data and 'pipes' in network_data['network']:
            summary['total_pipes'] = len(network_data['network']['pipes'])
        
        # Analyser la connectivité
        try:
            G = NetworkUtils.build_network_graph(network_data)
            summary['connected_components'] = len(list(nx.connected_components(G)))
            
            # Identifier les nœuds orphelins
            all_node_ids = NetworkUtils.extract_all_node_ids(network_data)
            connected_nodes = set()
            for component in nx.connected_components(G):
                connected_nodes.update(component)
            summary['orphaned_nodes'] = len(all_node_ids - connected_nodes)
            
        except Exception as e:
            print(f"⚠️  Erreur lors de l'analyse de connectivité: {e}")
        
        return summary 