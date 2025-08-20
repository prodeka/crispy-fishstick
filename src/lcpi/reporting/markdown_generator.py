"""
Générateur de rapports Markdown pour l'optimisation de réseau.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class MarkdownGenerator:
    """Génère des rapports d'optimisation au format Markdown."""
    
    def __init__(self):
        """Initialise le générateur Markdown."""
        self._prices_dao = None
        self._init_price_database()
    
    def generate_optimization_report(self, index_data: dict, outputs: dict) -> str:
        """
        Génère un rapport d'optimisation complet au format Markdown.
        
        Args:
            index_data: Données d'index multi-solveurs
            outputs: Résultats d'optimisation par solveur
            
        Returns:
            Contenu Markdown du rapport
        """
        lines = []
        
        # En-tête du rapport
        lines.extend(self._generate_header(index_data))
        
        # Résumé exécutif
        lines.extend(self._generate_executive_summary(index_data, outputs))
        
        # Métadonnées et configuration
        lines.extend(self._generate_configuration_section(index_data))
        
        # Résultats par solveur
        for solver in index_data.get("meta", {}).get("solvers", []):
            if solver in outputs:
                lines.extend(self._generate_solver_results(solver, outputs[solver]))
        
        # Comparaison des solveurs
        if len(index_data.get("meta", {}).get("solvers", [])) > 1:
            lines.extend(self._generate_comparison_section(index_data, outputs))
        
        # Détails techniques
        lines.extend(self._generate_technical_details(index_data, outputs))
        
        # Pied de page
        lines.extend(self._generate_footer())
        
        return "\n".join(lines)
    
    def _generate_header(self, index_data: dict) -> List[str]:
        """Génère l'en-tête du rapport."""
        lines = []
        lines.append("# 📊 Rapport d'Optimisation de Réseau")
        lines.append("")
        lines.append(f"**Date de génération:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Méthode d'optimisation:** {index_data.get('meta', {}).get('method', 'N/A')}")
        lines.append(f"**Solveurs utilisés:** {', '.join(index_data.get('meta', {}).get('solvers', []))}")
        lines.append("")
        lines.append("---")
        lines.append("")
        return lines
    
    def _generate_executive_summary(self, index_data: dict, outputs: dict) -> List[str]:
        """Génère le résumé exécutif."""
        lines = []
        lines.append("## 🎯 Résumé Exécutif")
        lines.append("")
        
        solvers = index_data.get("meta", {}).get("solvers", [])
        if len(solvers) == 1:
            solver = solvers[0]
            if solver in outputs:
                result = outputs[solver]
                best_proposal = result.get("proposals", [{}])[0] if result.get("proposals") else {}
                
                lines.append(f"**Solveur:** {solver.upper()}")
                lines.append(f"**CAPEX optimal:** {best_proposal.get('CAPEX', 'N/A'):,.2f} FCFA")
                lines.append(f"**Contraintes respectées:** {'✅' if best_proposal.get('constraints_ok') else '❌'}")
                lines.append(f"**Hauteur de réservoir:** {best_proposal.get('H_tank_m', 'N/A')} m")
                
                # Ajouter les violations de contraintes si présentes
                if best_proposal.get('constraints_violations'):
                    lines.append(f"**Violations:** {', '.join(best_proposal['constraints_violations'])}")
        else:
            lines.append("**Comparaison multi-solveurs:**")
            for solver in solvers:
                if solver in outputs:
                    result = outputs[solver]
                    best_proposal = result.get("proposals", [{}])[0] if result.get("proposals") else {}
                    lines.append(f"- **{solver.upper()}:** CAPEX {best_proposal.get('CAPEX', 'N/A'):,.2f} FCFA")
        
        lines.append("")
        return lines
    
    def _generate_configuration_section(self, index_data: dict) -> List[str]:
        """Génère la section de configuration."""
        lines = []
        lines.append("## ⚙️ Configuration")
        lines.append("")
        
        meta = index_data.get("meta", {})
        lines.append("### Paramètres d'optimisation")
        lines.append(f"- **Méthode:** {meta.get('method', 'N/A')}")
        lines.append(f"- **Solveurs:** {', '.join(meta.get('solvers', []))}")
        
        # Contraintes si disponibles
        if "constraints" in meta:
            constraints = meta["constraints"]
            lines.append("")
            lines.append("### Contraintes")
            if "pressure_min_m" in constraints:
                lines.append(f"- **Pression minimale:** {constraints['pressure_min_m']} m")
            if "velocity_min_m_s" in constraints:
                lines.append(f"- **Vitesse minimale:** {constraints['velocity_min_m_s']} m/s")
            if "velocity_max_m_s" in constraints:
                lines.append(f"- **Vitesse maximale:** {constraints['velocity_max_m_s']} m/s")
        
        lines.append("")
        return lines
    
    def _generate_solver_results(self, solver: str, result: dict) -> List[str]:
        """Génère les résultats pour un solveur spécifique."""
        lines = []
        lines.append(f"## 🔍 Résultats - {solver.upper()}")
        lines.append("")
        
        if "error" in result:
            lines.append(f"❌ **Erreur:** {result['error']}")
            lines.append("")
            return lines
        
        meta = result.get("meta", {})
        proposals = result.get("proposals", [])
        
        lines.append(f"**Méthode:** {meta.get('method', 'N/A')}")
        lines.append(f"**Source:** {meta.get('source', 'N/A')}")
        lines.append("")
        
        if proposals:
            lines.append("### Propositions d'optimisation")
            lines.append("")
            
            for i, proposal in enumerate(proposals[:5]):  # Top 5
                lines.append(f"#### Proposition {i+1}")
                lines.append(f"- **ID:** {proposal.get('id', 'N/A')}")
                lines.append(f"- **CAPEX:** {proposal.get('CAPEX', 'N/A'):,.2f} FCFA")
                lines.append(f"- **Hauteur réservoir:** {proposal.get('H_tank_m', 'N/A')} m")
                lines.append(f"- **Contraintes respectées:** {'✅' if proposal.get('constraints_ok') else '❌'}")
                
                if proposal.get('constraints_violations'):
                    lines.append(f"- **Violations:** {', '.join(proposal['constraints_violations'])}")
                
                # Diamètres des conduites
                diameters = proposal.get('diameters_mm', {})
                if diameters:
                    lines.append("- **Diamètres des conduites:**")
                    for pipe, diameter in list(diameters.items())[:10]:  # Top 10
                        lines.append(f"  - {pipe}: {diameter} mm")
                    if len(diameters) > 10:
                        lines.append(f"  - ... et {len(diameters) - 10} autres conduites")
                lines.append("")
        
        # Ajouter les détails hydrauliques complets
        lines.extend(self._generate_hydraulic_details(result))
        
        lines.append("---")
        lines.append("")
        return lines
    
    def _generate_hydraulic_details(self, result: dict) -> List[str]:
        """Génère les détails hydrauliques complets."""
        lines = []
        
        # Vérifier si nous avons des données hydrauliques
        hydraulics = result.get("hydraulics", {})
        if not hydraulics or "error" in hydraulics:
            lines.append("### ⚠️ Données hydrauliques non disponibles")
            if "error" in hydraulics:
                lines.append(f"**Erreur:** {hydraulics['error']}")
            lines.append("")
            return lines
        
        lines.append("### 🌊 Détails Hydrauliques Complets")
        lines.append("")
        
        # Pressions des nœuds
        pressures = hydraulics.get("pressures", {})
        if pressures:
            lines.append("#### 📍 Pressions des Nœuds")
            lines.append("")
            lines.append("| Nœud | Pression (m) |")
            lines.append("|------|-------------|")
            for node, pressure in sorted(pressures.items()):
                lines.append(f"| {node} | {pressure:.2f} |")
            lines.append("")
        
        # Vitesses des conduites
        velocities = hydraulics.get("velocities_m_s", {})
        if velocities:
            lines.append("#### 🚀 Vitesses des Conduites")
            lines.append("")
            lines.append("| Conduite | Vitesse (m/s) |")
            lines.append("|----------|---------------|")
            for pipe, velocity in sorted(velocities.items()):
                lines.append(f"| {pipe} | {velocity:.3f} |")
            lines.append("")
        
        # Pertes de charge
        headloss = hydraulics.get("headloss", {})
        if headloss:
            lines.append("#### 📉 Pertes de Charge")
            lines.append("")
            lines.append("| Conduite | Perte de charge (m) |")
            lines.append("|----------|---------------------|")
            for pipe, loss in sorted(headloss.items()):
                lines.append(f"| {pipe} | {loss:.3f} |")
            lines.append("")
        
        # Débits des conduites
        flows = hydraulics.get("flows_m3_s", {})
        if flows:
            lines.append("#### 💧 Débits des Conduites")
            lines.append("")
            lines.append("| Conduite | Débit (m³/s) |")
            lines.append("|----------|--------------|")
            for pipe, flow in sorted(flows.items()):
                lines.append(f"| {pipe} | {flow:.4f} |")
            lines.append("")
        
        # Détails des conduites avec prix
        lines.extend(self._generate_pipe_details_with_prices(result))
        
        return lines
    
    def _generate_pipe_details_with_prices(self, result: dict) -> List[str]:
        """Génère les détails des conduites avec diamètres et prix."""
        lines = []
        
        # Récupérer la meilleure proposition
        proposals = result.get("proposals", [])
        if not proposals:
            return lines
        
        best_proposal = proposals[0]
        diameters = best_proposal.get("diameters_mm", {})
        
        if not diameters:
            return lines
        
        lines.append("#### 🔧 Détails des Conduites avec Prix")
        lines.append("")
        lines.append("| Conduite | Diamètre théorique (mm) | DN choisi (mm) | Matériau | Fourniture (FCFA/m) | Pose (FCFA/m) | Total (FCFA/m) | Longueur (m) | Prix total (FCFA) | Source |")
        lines.append("|----------|-------------------------|----------------|----------|-------------------|---------------|----------------|-------------|------------------|--------|")
        
        # Matériau par défaut
        default_material = os.getenv("AEP_MATERIAL", "PVC-U")
        
        for pipe, diameter in sorted(diameters.items()):
            # Trouver le DN standard le plus proche
            dn_chosen = self._find_closest_dn(diameter)
            
            # Récupérer les informations de prix depuis la base de données
            price_info = self._get_pipe_price_info(dn_chosen, default_material)
            
            # Longueur (approximative - à récupérer depuis le fichier INP si disponible)
            length = self._get_pipe_length(pipe, result)
            
            # Prix total
            total_price = price_info["total_price"] * length
            
            lines.append(f"| {pipe} | {diameter} | {dn_chosen} | {price_info['material']} | {price_info['supply_price']:,.0f} | {price_info['pose_price']:,.0f} | {price_info['total_price']:,.0f} | {length:.1f} | {total_price:,.0f} | {price_info['source']} |")
        
        lines.append("")
        
        # Résumé des coûts avec détails
        total_capex = best_proposal.get("CAPEX", 0)
        lines.append(f"**CAPEX total:** {total_capex:,.2f} FCFA")
        
        # Informations sur la base de données de prix
        if self._prices_dao:
            lines.append(f"**Base de prix:** Connectée (aep_prices.db)")
            lines.append(f"**Matériau par défaut:** {default_material}")
        else:
            lines.append(f"**Base de prix:** Non connectée (prix estimés)")
        
        lines.append("")
        
        return lines
    
    def _find_closest_dn(self, theoretical_diameter: float) -> int:
        """Trouve le diamètre DN standard le plus proche."""
        # Diamètres DN standards (mm)
        dn_standards = [50, 63, 75, 90, 110, 125, 140, 160, 180, 200, 225, 250, 280, 315, 355, 400, 450, 500, 560, 630, 710, 800, 900, 1000]
        
        closest = min(dn_standards, key=lambda x: abs(x - theoretical_diameter))
        return closest
    
    def _init_price_database(self) -> None:
        """Initialise la connexion à la base de données de prix."""
        try:
            # Import local pour éviter les dépendances circulaires
            from pathlib import Path as P
            import sys
            import os
            
            # Ajouter le chemin vers le module AEP
            current_dir = Path(__file__).resolve().parent
            aep_dir = current_dir.parent / "aep"
            if str(aep_dir) not in sys.path:
                sys.path.insert(0, str(aep_dir))
            
            # Importer le DAO de prix
            from optimizer.db_dao import AEPPricesDAO
            
            # Chemin vers la base de données
            db_path = current_dir.parent / "db" / "aep_prices.db"
            
            if db_path.exists():
                self._prices_dao = AEPPricesDAO(db_path)
            else:
                print(f"⚠️  Base de données de prix non trouvée: {db_path}")
                self._prices_dao = None
                
        except Exception as e:
            print(f"⚠️  Erreur lors de l'initialisation de la base de prix: {e}")
            self._prices_dao = None

    def _get_diameter_price_from_db(self, dn_mm: int, material: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Récupère les informations de prix d'un diamètre depuis la base de données.
        
        Args:
            dn_mm: Diamètre nominal en mm
            material: Matériau (PVC-U par défaut)
            
        Returns:
            Dictionnaire avec les prix ou None si non trouvé
        """
        if not self._prices_dao:
            return None
            
        try:
            material = material or os.getenv("AEP_MATERIAL", "PVC-U")
            info = self._prices_dao.get_diameter_info(dn_mm, material)
            return info
        except Exception as e:
            print(f"⚠️  Erreur lors de la récupération du prix pour DN {dn_mm}: {e}")
            return None

    def _get_pipe_price_info(self, dn_mm: int, material: Optional[str] = None) -> Dict[str, Any]:
        """
        Récupère les informations de prix complètes depuis la base de données.
        
        Args:
            dn_mm: Diamètre nominal en mm
            material: Matériau
            
        Returns:
            Dictionnaire avec les informations de prix
        """
        info = self._get_diameter_price_from_db(dn_mm, material)
        
        if info:
            return {
                "dn_mm": info["dn_mm"],
                "material": info["material"],
                "supply_price": info["supply_fcfa_per_m"],
                "pose_price": info["pose_fcfa_per_m"],
                "total_price": info["total_fcfa_per_m"],
                "source": "aep_prices.db"
            }
        else:
            # Fallback avec estimation
            estimated_price = self._estimate_pipe_price_fallback(dn_mm)
            return {
                "dn_mm": dn_mm,
                "material": material or "PVC-U",
                "supply_price": estimated_price * 0.7,  # 70% fourniture
                "pose_price": estimated_price * 0.3,    # 30% pose
                "total_price": estimated_price,
                "source": "estimation"
            }

    def _estimate_pipe_price_fallback(self, dn: int) -> float:
        """Estimation de prix de fallback si la DB n'est pas disponible."""
        # Prix approximatifs en FCFA/m basés sur les données historiques
        price_table = {
            20: 1750, 25: 2100, 32: 2500, 40: 3000, 50: 3500,
            63: 4200, 75: 4800, 90: 5500, 110: 6500, 125: 7500,
            140: 8500, 160: 9500, 180: 11000, 200: 12500, 225: 14000,
            250: 16000, 280: 18000, 315: 21000, 355: 25000, 400: 30000,
            450: 35000, 500: 42000, 560: 50000, 630: 60000, 710: 72000,
            800: 85000, 900: 100000, 1000: 120000
        }
        
        return price_table.get(dn, dn * 100)  # Estimation linéaire par défaut

    def _get_pipe_length(self, pipe_id: str, result: dict) -> float:
        """
        Récupère la longueur d'une conduite depuis les données du réseau.
        
        Args:
            pipe_id: Identifiant de la conduite
            result: Résultats d'optimisation
            
        Returns:
            Longueur en mètres (approximée si non trouvée)
        """
        # Essayer de récupérer depuis les métadonnées du réseau
        meta = result.get("meta", {})
        
        # Chercher dans les données de source
        if "source_meta" in meta:
            # Si on a des informations sur le fichier INP source
            # On pourrait parser le fichier pour récupérer les longueurs réelles
            pass
        
        # Pour l'instant, retourner une longueur approximative basée sur le type de conduite
        # Les conduites principales ont généralement plus de longueur
        if any(keyword in pipe_id.lower() for keyword in ["main", "trunk", "primary"]):
            return 500.0  # Conduites principales plus longues
        elif any(keyword in pipe_id.lower() for keyword in ["secondary", "branch"]):
            return 200.0  # Conduites secondaires
        elif any(keyword in pipe_id.lower() for keyword in ["service", "connection"]):
            return 50.0   # Branchements courts
        else:
            return 100.0  # Longueur par défaut
    
    def _generate_comparison_section(self, index_data: dict, outputs: dict) -> List[str]:
        """Génère la section de comparaison des solveurs."""
        lines = []
        lines.append("## 📈 Comparaison des Solveurs")
        lines.append("")
        
        lines.append("| Solveur | CAPEX (FCFA) | Hauteur Réservoir (m) | Contraintes |")
        lines.append("|---------|--------------|----------------------|-------------|")
        
        for solver in index_data.get("meta", {}).get("solvers", []):
            if solver in outputs:
                result = outputs[solver]
                if "error" in result:
                    lines.append(f"| {solver.upper()} | ❌ Erreur | - | - |")
                else:
                    best_proposal = result.get("proposals", [{}])[0] if result.get("proposals") else {}
                    capex = best_proposal.get('CAPEX', 'N/A')
                    if isinstance(capex, (int, float)):
                        capex = f"{capex:,.2f}"
                    height = best_proposal.get('H_tank_m', 'N/A')
                    constraints_ok = '✅' if best_proposal.get('constraints_ok') else '❌'
                    lines.append(f"| {solver.upper()} | {capex} | {height} | {constraints_ok} |")
        
        lines.append("")
        return lines
    
    def _generate_technical_details(self, index_data: dict, outputs: dict) -> List[str]:
        """Génère les détails techniques."""
        lines = []
        lines.append("## 🔧 Détails Techniques")
        lines.append("")
        
        lines.append("### Métadonnées des fichiers")
        for solver in index_data.get("meta", {}).get("solvers", []):
            if solver in outputs:
                result = outputs[solver]
                if "integrity" in result:
                    integrity = result["integrity"]
                    lines.append(f"**{solver.upper()}:**")
                    lines.append(f"- **Checksum:** {integrity.get('checksum', 'N/A')}")
                    lines.append(f"- **Signature:** {integrity.get('signature', 'N/A')}")
                    lines.append(f"- **Validité:** {'✅' if integrity.get('signature_valid') else '❌'}")
                    lines.append("")
        
        lines.append("### Informations de performance")
        for solver in index_data.get("meta", {}).get("solvers", []):
            if solver in outputs:
                result = outputs[solver]
                if "execution_time" in result:
                    lines.append(f"**{solver.upper()}:** Temps d'exécution: {result['execution_time']:.2f}s")
        
        lines.append("")
        return lines
    
    def _generate_footer(self) -> List[str]:
        """Génère le pied de page."""
        lines = []
        lines.append("---")
        lines.append("")
        lines.append("*Rapport généré automatiquement par LCPI-CLI*")
        lines.append(f"*Version: 1.0.0 | Date: {datetime.now().strftime('%Y-%m-%d')}*")
        return lines
