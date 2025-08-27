#!/usr/bin/env python3
"""
Utilitaire de vérification des demandes dans les fichiers INP temporaires.
Intégré dans le flux de network-optimize-unified pour vérifier automatiquement
que le double comptage est évité.
"""

from pathlib import Path
from rich import print as rprint
from typing import Tuple, List

def verify_demands_in_file(file_path: Path) -> Tuple[bool, dict]:
    """
    Vérifie le contenu d'un fichier INP pour s'assurer qu'il n'y a pas de double comptage.
    
    Args:
        file_path: Chemin vers le fichier INP à vérifier
        
    Returns:
        Tuple[bool, dict]: (succès, détails de la vérification)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Analyser les sections
        junctions_demands = []
        demands_section = []
        in_junctions = False
        in_demands = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('[JUNCTIONS]'):
                in_junctions = True
                in_demands = False
                continue
            elif line.startswith('[DEMANDS]'):
                in_junctions = False
                in_demands = True
                continue
            elif line.startswith('['):
                in_junctions = False
                in_demands = False
                continue
            
            if in_junctions and line and not line.startswith(';'):
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        demand = float(parts[2])
                        if demand > 0:
                            junctions_demands.append((parts[0], demand))
                    except ValueError:
                        pass
            
            elif in_demands and line and not line.startswith(';'):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        demand = float(parts[1])
                        demands_section.append((parts[0], demand))
                    except ValueError:
                        pass
        
        # Calculer les statistiques
        total_demand = sum(demand for _, demand in demands_section)
        avg_demand = total_demand / len(demands_section) if demands_section else 0
        
        # Vérification du double comptage
        double_counting_avoided = len(junctions_demands) == 0 and len(demands_section) > 0
        
        details = {
            'junctions_with_demand': len(junctions_demands),
            'demands_count': len(demands_section),
            'total_demand': total_demand,
            'avg_demand': avg_demand,
            'double_counting_avoided': double_counting_avoided,
            'problem_nodes': junctions_demands[:5] if junctions_demands else []
        }
        
        return double_counting_avoided, details
        
    except Exception as e:
        rprint(f"[red]❌ Erreur lors de la vérification des demandes : {e}[/red]")
        return False, {'error': str(e)}

def display_verification_results(file_path: Path, details: dict) -> None:
    """
    Affiche les résultats de la vérification des demandes.
    
    Args:
        file_path: Chemin vers le fichier vérifié
        details: Détails de la vérification
    """
    rprint(f"\n🔍 [bold cyan]VÉRIFICATION DES DEMANDES[/bold cyan]")
    rprint(f"📁 Fichier : {file_path.name}")
    
    if 'error' in details:
        rprint(f"[red]❌ Erreur : {details['error']}[/red]")
        return
    
    rprint(f"\n📊 [bold]ANALYSE DES DEMANDES :[/bold]")
    rprint(f"   [JUNCTIONS] avec demande > 0 : {details['junctions_with_demand']}")
    rprint(f"   [DEMANDS] : {details['demands_count']}")
    
    if details['junctions_with_demand'] > 0:
        rprint(f"\n⚠️  [bold yellow]PROBLÈME : Demandes > 0 trouvées dans [JUNCTIONS] :[/bold yellow]")
        for node, demand in details['problem_nodes']:
            rprint(f"      {node}: {demand}")
        if details['junctions_with_demand'] > 5:
            rprint(f"      ... et {details['junctions_with_demand'] - 5} autres")
    else:
        rprint(f"\n✅ [bold green]SUCCÈS : Aucune demande > 0 dans [JUNCTIONS][/bold green]")
    
    if details['demands_count'] > 0:
        rprint(f"\n📈 [bold]Section [DEMANDS] :[/bold]")
        rprint(f"   Total : {details['total_demand']:.4f}")
        rprint(f"   Moyenne : {details['avg_demand']:.4f}")
    
    # Résultat final
    if details['double_counting_avoided']:
        rprint(f"\n🎉 [bold green]CORRECTION RÉUSSIE : Double comptage évité ![/bold green]")
        rprint(f"💡 EPANET utilisera uniquement les demandes de la section [DEMANDS]")
    else:
        rprint(f"\n❌ [bold red]PROBLÈME PERSISTANT : Double comptage possible[/bold red]")
        rprint(f"⚠️  EPANET pourrait additionner les demandes des deux sections")
