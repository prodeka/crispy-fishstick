"""
Module d'intégration EPANET avec diagnostic de connectivité

Ce module intègre la fonction de diagnostic de connectivité réseau
avant l'appel à EPANET pour prévenir l'erreur 110.
"""

import os
import tempfile
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

try:
    from .network_diagnostics import (
        diagnose_network_connectivity,
        analyze_network_topology,
        validate_epanet_compatibility
    )
    from ..epanet_wrapper import EpanetSimulator, create_epanet_inp_file
except ImportError:
    # Fallback pour les imports dynamiques
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Import network_diagnostics
    network_diagnostics_path = os.path.join(current_dir, "network_diagnostics.py")
    import importlib.util
    spec_diagnostics = importlib.util.spec_from_file_location("network_diagnostics", network_diagnostics_path)
    if spec_diagnostics and spec_diagnostics.loader:
        network_diagnostics = importlib.util.module_from_spec(spec_diagnostics)
        spec_diagnostics.loader.exec_module(network_diagnostics)
    else:
        raise ImportError("Impossible de charger network_diagnostics")
    
    # Import epanet_wrapper
    epanet_wrapper_path = os.path.join(os.path.dirname(current_dir), "epanet_wrapper.py")
    spec_wrapper = importlib.util.spec_from_file_location("epanet_wrapper", epanet_wrapper_path)
    if spec_wrapper and spec_wrapper.loader:
        epanet_wrapper = importlib.util.module_from_spec(spec_wrapper)
        spec_wrapper.loader.exec_module(epanet_wrapper)
    else:
        raise ImportError("Impossible de charger epanet_wrapper")
    
    # Assigner les fonctions
    diagnose_network_connectivity = network_diagnostics.diagnose_network_connectivity
    analyze_network_topology = network_diagnostics.analyze_network_topology
    validate_epanet_compatibility = network_diagnostics.validate_epanet_compatibility
    EpanetSimulator = epanet_wrapper.EpanetSimulator
    create_epanet_inp_file = epanet_wrapper.create_epanet_inp_file


class EpanetWithDiagnostics:
    """
    Classe wrapper pour EPANET avec diagnostic automatique de connectivité.
    
    Cette classe intègre les diagnostics de connectivité réseau avant
    l'exécution d'EPANET pour prévenir l'erreur 110.
    """
    
    def __init__(self, epanet_path: Optional[str] = None):
        """
        Initialise le wrapper EPANET avec diagnostics.
        
        Args:
            epanet_path: Chemin vers la DLL EPANET (optionnel)
        """
        self.epanet_simulator = EpanetSimulator(epanet_path)
        self.diagnostic_results = {}
        self.validation_results = {}
        
    def run_with_diagnostics(self, network_data: Dict[str, Any], 
                           inp_file_path: Optional[str] = None,
                           skip_diagnostics: bool = False) -> Dict[str, Any]:
        """
        Exécute EPANET avec diagnostic automatique de connectivité.
        
        Args:
            network_data: Données du réseau au format LCPI
            inp_file_path: Chemin du fichier .inp (optionnel, généré automatiquement si None)
            skip_diagnostics: Si True, ignore les diagnostics (non recommandé)
            
        Returns:
            Dict contenant les résultats de simulation et diagnostics
            
        Raises:
            ValueError: Si le réseau présente des problèmes de connectivité critiques
            RuntimeError: Si EPANET échoue après validation
        """
        
        results = {
            "success": False,
            "diagnostics": {},
            "validation": {},
            "epanet_results": {},
            "errors": [],
            "warnings": []
        }
        
        try:
            print("🚀 DÉMARRAGE SIMULATION EPANET AVEC DIAGNOSTICS")
            print("=" * 60)
            
            # ÉTAPE 1: Diagnostic de connectivité
            if not skip_diagnostics:
                print("\n🔍 ÉTAPE 1: DIAGNOSTIC DE CONNECTIVITÉ")
                print("-" * 40)
                
                try:
                    is_connected = diagnose_network_connectivity(network_data)
                    results["diagnostics"]["connectivity"] = is_connected
                    
                    if not is_connected:
                        error_msg = "❌ RÉSEAU NON CONNECTÉ - Simulation EPANET annulée"
                        results["errors"].append(error_msg)
                        print(error_msg)
                        print("💡 Corrigez les problèmes de connectivité avant de relancer EPANET")
                        return results
                    
                    print("✅ Réseau connecté - Diagnostic réussi")
                    
                except Exception as e:
                    error_msg = f"❌ Erreur lors du diagnostic: {e}"
                    results["errors"].append(error_msg)
                    print(error_msg)
                    return results
            
            # ÉTAPE 2: Validation EPANET
            print("\n🔧 ÉTAPE 2: VALIDATION COMPATIBILITÉ EPANET")
            print("-" * 40)
            
            try:
                validation = validate_epanet_compatibility(network_data)
                results["validation"] = validation
                
                if not validation["compatible"]:
                    error_msg = "❌ RÉSEAU INCOMPATIBLE AVEC EPANET - Simulation annulée"
                    results["errors"].append(error_msg)
                    print(error_msg)
                    
                    if validation["erreurs"]:
                        print("📋 Erreurs détectées:")
                        for error in validation["erreurs"]:
                            print(f"   • {error}")
                    
                    return results
                
                print("✅ Réseau compatible avec EPANET")
                
            except Exception as e:
                error_msg = f"❌ Erreur lors de la validation: {e}"
                results["errors"].append(error_msg)
                print(error_msg)
                return results
            
            # ÉTAPE 3: Analyse topologique (optionnelle)
            print("\n🔬 ÉTAPE 3: ANALYSE TOPOLOGIQUE")
            print("-" * 40)
            
            try:
                topology = analyze_network_topology(network_data)
                results["diagnostics"]["topology"] = topology
                print("✅ Analyse topologique terminée")
                
            except Exception as e:
                warning_msg = f"⚠️  Erreur lors de l'analyse topologique: {e}"
                results["warnings"].append(warning_msg)
                print(warning_msg)
            
            # ÉTAPE 4: Génération du fichier .inp
            print("\n📝 ÉTAPE 4: GÉNÉRATION FICHIER .INP")
            print("-" * 40)
            
            if inp_file_path is None:
                # Créer un fichier temporaire
                temp_dir = tempfile.gettempdir()
                inp_file_path = os.path.join(temp_dir, "lcpi_epanet_temp.inp")
            
            try:
                success = create_epanet_inp_file(network_data, inp_file_path)
                if not success:
                    error_msg = "❌ Échec de la génération du fichier .inp"
                    results["errors"].append(error_msg)
                    print(error_msg)
                    return results
                
                print(f"✅ Fichier .inp généré: {inp_file_path}")
                
            except Exception as e:
                error_msg = f"❌ Erreur lors de la génération du fichier .inp: {e}"
                results["errors"].append(error_msg)
                print(error_msg)
                return results
            
            # ÉTAPE 5: Simulation EPANET
            print("\n⚡ ÉTAPE 5: SIMULATION EPANET")
            print("-" * 40)
            
            try:
                # Ouvrir le fichier .inp
                if not self.epanet_simulator.open_project(inp_file_path):
                    raise Exception("Impossible d'ouvrir le projet EPANET")
                
                # Lancer la simulation hydraulique
                print("   • Lancement de la simulation hydraulique...")
                if not self.epanet_simulator.solve_hydraulics():
                    raise Exception("Échec de la simulation hydraulique")
                
                # Sauvegarder les résultats
                if not self.epanet_simulator.save_results():
                    raise Exception("Impossible de sauvegarder les résultats")
                
                # Récupérer les résultats
                print("   • Récupération des résultats...")
                epanet_results = self._extract_epanet_results()
                results["epanet_results"] = epanet_results
                
                # Fermer le fichier
                self.epanet_simulator.close_project()
                
                print("✅ Simulation EPANET réussie")
                results["success"] = True
                
            except Exception as e:
                error_msg = f"❌ Erreur EPANET: {e}"
                results["errors"].append(error_msg)
                print(error_msg)
                
                # Nettoyer
                try:
                    self.epanet_simulator.close_project()
                except:
                    pass
                
                return results
            
            # ÉTAPE 6: Nettoyage
            if inp_file_path and "temp" in inp_file_path and os.path.exists(inp_file_path):
                try:
                    os.remove(inp_file_path)
                    print(f"🧹 Fichier temporaire supprimé: {inp_file_path}")
                except:
                    pass
            
            print(f"\n{'='*60}")
            print("✅ SIMULATION TERMINÉE AVEC SUCCÈS")
            print(f"{'='*60}")
            
            return results
            
        except Exception as e:
            error_msg = f"❌ Erreur générale: {e}"
            results["errors"].append(error_msg)
            print(error_msg)
            return results
    
    def _extract_epanet_results(self) -> Dict[str, Any]:
        """
        Extrait les résultats de simulation EPANET.
        
        Returns:
            Dict contenant les résultats de simulation
        """
        results = {
            "nodes": {},
            "pipes": {},
            "statistics": {}
        }
        
        try:
            # Statistiques de simulation (simplifiées pour l'instant)
            results["statistics"] = {
                "status": "completed",
                "message": "Simulation EPANET terminée avec succès"
            }
            
            # Résultats des nœuds
            node_ids = self.epanet_simulator.get_node_ids()
            for node_id in node_ids:
                # Pour l'instant, on récupère juste les IDs
                # Les valeurs détaillées nécessiteraient des méthodes supplémentaires
                results["nodes"][node_id] = {
                    "status": "calculated",
                    "id": node_id
                }
            
            # Résultats des conduites (simplifiés)
            summary = self.epanet_simulator.get_network_summary()
            results["pipes"] = {
                "total_count": summary.get('links', 0),
                "status": "calculated"
            }
                
        except Exception as e:
            print(f"⚠️  Erreur lors de l'extraction des résultats: {e}")
        
        return results


def run_epanet_with_diagnostics(network_data: Dict[str, Any], 
                               epanet_path: Optional[str] = None,
                               inp_file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Fonction utilitaire pour exécuter EPANET avec diagnostics.
    
    Args:
        network_data: Données du réseau au format LCPI
        epanet_path: Chemin vers la DLL EPANET (optionnel)
        inp_file_path: Chemin du fichier .inp (optionnel)
        
    Returns:
        Dict contenant les résultats de simulation et diagnostics
    """
    epanet_wrapper = EpanetWithDiagnostics(epanet_path)
    return epanet_wrapper.run_with_diagnostics(network_data, inp_file_path)


def quick_diagnostic(network_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Diagnostic rapide du réseau sans simulation EPANET.
    
    Args:
        network_data: Données du réseau au format LCPI
        
    Returns:
        Dict contenant les résultats de diagnostic
    """
    results = {
        "connectivity": False,
        "epanet_compatible": False,
        "topology": {},
        "errors": [],
        "warnings": []
    }
    
    try:
        # Test de connectivité
        results["connectivity"] = diagnose_network_connectivity(network_data)
        
        # Validation EPANET
        validation = validate_epanet_compatibility(network_data)
        results["epanet_compatible"] = validation["compatible"]
        results["errors"].extend(validation["erreurs"])
        results["warnings"].extend(validation["avertissements"])
        
        # Analyse topologique
        try:
            results["topology"] = analyze_network_topology(network_data)
        except Exception as e:
            results["warnings"].append(f"Erreur analyse topologique: {e}")
        
    except Exception as e:
        results["errors"].append(f"Erreur diagnostic: {e}")
    
    return results 