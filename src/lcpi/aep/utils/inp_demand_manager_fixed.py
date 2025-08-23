"""
Utilitaire pour la gestion des demandes dans les fichiers EPANET .inp (version corrigée).
"""
import configparser
import io
import os
from pathlib import Path
from typing import Optional
import typer
from rich import print as rprint

import tempfile
import atexit

_temp_files = []

def _cleanup_temp_files():
    for path in _temp_files:
        try:
            if path.exists():
                path.unlink()
                rprint(f"[dim]Fichier temporaire nettoyé : {path}[/dim]")
        except Exception as e:
            rprint(f"[dim red]Erreur lors du nettoyage du fichier temporaire {path}: {e}[/dim]")

atexit.register(_cleanup_temp_files)

def handle_demand_logic(input_path: Path, demand_value: Optional[float], no_log: bool = False) -> Path:
    """
    Gère la logique de la demande pour un fichier .inp.
    """
    if input_path.suffix.lower() != '.inp':
        return input_path

    if demand_value is None:
        # Scénario 1: Pas de --demand, on s'assure que la demande est bien remplie depuis JUNCTIONS si besoin
        return _ensure_demand_from_junctions(input_path)
    else:
        # Scénario 2: --demand est fourni, on gère l'écrasement
        return _apply_demand_override(input_path, demand_value, no_log)

def _read_inp_lines(path: Path) -> list[str]:
    """Lit toutes les lignes d'un fichier .inp."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()

def _write_lines_to_temp_file(lines: list[str], suffix: str) -> Path:
    """Écrit des lignes dans un fichier temporaire en préservant les fins de ligne."""
    fd, temp_path_str = tempfile.mkstemp(suffix=suffix, text=True)
    temp_path = Path(temp_path_str)
    _temp_files.append(temp_path)

    with os.fdopen(fd, 'w', encoding='utf-8', newline='') as f:
        f.writelines(lines)
    
    return temp_path

def _ensure_demand_from_junctions(input_path: Path) -> Path:
    """
    Vérifie si la section [DEMANDS] est vide. Si c'est le cas, la remplit
    en se basant sur la section [JUNCTIONS].
    """
    lines = _read_inp_lines(input_path)
    
    try:
        demands_idx = -1
        junctions_idx = -1
        
        # Trouver les sections
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('[DEMANDS]'):
                demands_idx = i
            elif stripped.startswith('[JUNCTIONS]'):
                junctions_idx = i

        if demands_idx == -1:  # Pas de section [DEMANDS]
            return input_path

        # Vérifier si la section [DEMANDS] est vide
        has_demands_content = False
        for i in range(demands_idx + 1, len(lines)):
            line = lines[i].strip()
            if line.startswith('['):
                break  # Nouvelle section
            if line and not line.startswith(';'):
                # Vérifier si c'est vraiment du contenu (pas juste un en-tête)
                words = line.split()
                if not any(word.lower() in ['junction', 'demand', 'pattern', 'category', 'id', 'status', 'setting'] for word in words):
                    has_demands_content = True
                    break

        if not has_demands_content:
            rprint("[yellow]La section [DEMANDS] est vide. Calcul depuis [JUNCTIONS]...[/yellow]")
            
            if junctions_idx == -1:
                return input_path

            # Extraire les demandes depuis [JUNCTIONS]
            demands_to_add = ["; Demandes reportées depuis la section [JUNCTIONS]\n"]
            total_demand = 0.0
            node_count = 0
            
            for line in lines[junctions_idx + 1:]:
                stripped = line.strip()
                if stripped.startswith('['):
                    break  # Fin de la section
                
                if stripped.startswith(';') or not stripped:
                    continue
                
                parts = stripped.split()
                if len(parts) >= 3:
                    try:
                        node_id = parts[0]
                        demand = float(parts[2])
                        demands_to_add.append(f"{node_id:<16} {demand:<16.4f}\n")
                        total_demand += demand
                        node_count += 1
                    except (ValueError, IndexError):
                        continue
            
            if len(demands_to_add) > 1:
                # Insérer les nouvelles demandes après la ligne [DEMANDS]
                new_lines = lines[:demands_idx + 1] + demands_to_add + lines[demands_idx + 1:]
                temp_path = _write_lines_to_temp_file(new_lines, ".demand_filled.inp")
                rprint(f"[green]La section [DEMANDS] a été remplie avec {len(demands_to_add) - 1} entrées dans {temp_path}[/green]")
                rprint(f"[cyan]Somme totale des demandes calculée : {total_demand:.4f} (moyenne : {total_demand/node_count:.4f} par nœud)[/cyan]")
                return temp_path

    except Exception as e:
        rprint(f"[red]Erreur inattendue dans _ensure_demand_from_junctions: {e}[/red]")
        return input_path

    return input_path

def _apply_demand_override(input_path: Path, demand_value: float, no_log: bool = False) -> Path:
    """
    Applique la demande fournie par l'utilisateur.
    """
    lines = _read_inp_lines(input_path)
    
    try:
        demands_idx = -1
        junctions_idx = -1
        
        # Trouver les sections
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('[DEMANDS]'):
                demands_idx = i
            elif stripped.startswith('[JUNCTIONS]'):
                junctions_idx = i

        if demands_idx == -1:
            rprint("[red]❌ Section [DEMANDS] introuvable dans le fichier .inp.[/red]")
            raise typer.Exit(1)

        # Vérifier si la section [DEMANDS] a du contenu
        has_demands_content = False
        for i in range(demands_idx + 1, len(lines)):
            line = lines[i].strip()
            if line.startswith('['):
                break
            if line and not line.startswith(';'):
                words = line.split()
                if not any(word.lower() in ['junction', 'demand', 'pattern', 'category', 'id', 'status', 'setting'] for word in words):
                    has_demands_content = True
                    break

        if has_demands_content:
            rprint("[bold yellow]⚠️ Une section [DEMANDS] avec du contenu a été détectée.[/bold yellow]")
            if not no_log and not typer.confirm("Voulez-vous écraser les demandes existantes avec la valeur fournie ?"):
                rprint("[red]Opération annulée. Utilisation du fichier original.[/red]")
                return input_path

        if junctions_idx == -1:
            rprint("[red]❌ Impossible d'appliquer la demande : section [JUNCTIONS] introuvable.[/red]")
            raise typer.Exit(1)

        # Collecter tous les nœuds de [JUNCTIONS]
        junction_nodes = []
        for line in lines[junctions_idx + 1:]:
            stripped = line.strip()
            if stripped.startswith('['): 
                break
            if stripped and not stripped.startswith(';'):
                junction_nodes.append(stripped.split()[0])
        
        if not junction_nodes:
            rprint("[red]❌ Impossible d'appliquer la demande : aucun noeud trouvé dans [JUNCTIONS].[/red]")
            raise typer.Exit(1)

        # Répartir la demande uniformément sur tous les nœuds
        demand_per_node = demand_value / len(junction_nodes)
        new_demands_lines = ["; Demande répartie via --demand\n"]
        for node in junction_nodes:
            new_demands_lines.append(f"{node:<16} {demand_per_node:<16.4f}\n")
        
        # Trouver la fin de la section [DEMANDS]
        end_demands_idx = len(lines)
        for i in range(demands_idx + 1, len(lines)):
            if lines[i].strip().startswith('['):
                end_demands_idx = i
                break
        
        # Construire le nouveau fichier
        new_lines = lines[:demands_idx + 1] + new_demands_lines + lines[end_demands_idx:]
        temp_path = _write_lines_to_temp_file(new_lines, ".demand_override.inp")

        rprint(f"[green]Demande de {demand_value:.4f} répartie sur {len(junction_nodes)} nœuds ({demand_per_node:.4f} par nœud) dans {temp_path}[/green]")
        return temp_path

    except Exception as e:
        rprint(f"[red]Erreur inattendue dans _apply_demand_override: {e}[/red]")
        return input_path
