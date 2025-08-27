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
from .demand_verifier import verify_demands_in_file, display_verification_results

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
    en se basant sur la section [JUNCTIONS] (3ème colonne).
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
            rprint("[yellow]Section [DEMANDS] manquante. Création automatique depuis [JUNCTIONS]...[/yellow]")
            # Créer la section [DEMANDS] après [JUNCTIONS]
            insert_pos = junctions_idx + 1 if junctions_idx != -1 else 0
            new_lines = lines[:insert_pos] + ["\n[DEMANDS]\n"] + lines[insert_pos:]
            lines = new_lines
            demands_idx = insert_pos

        # Vérifier si la section [DEMANDS] est vide (après création si nécessaire)
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
            rprint("[yellow]Section [DEMANDS] vide détectée. Transfert automatique depuis [JUNCTIONS] (3ème colonne)...[/yellow]")
            
            if junctions_idx == -1:
                rprint("[red]❌ Section [JUNCTIONS] non trouvée.[/red]")
                return input_path

            # Extraire les demandes depuis [JUNCTIONS] (3ème colonne)
            demands_to_add = [
                "; Demandes transférées depuis la section [JUNCTIONS] (3ème colonne)\n",
                ";Node  BaseDemand  Pattern  Category\n"
            ]
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
                        if demand > 0:  # Seulement les nœuds avec demande > 0
                            demands_to_add.append(f"{node_id:<16} {demand:<16.4f}\n")
                            total_demand += demand
                            node_count += 1
                    except (ValueError, IndexError):
                        continue
            
            if len(demands_to_add) > 1:
                # IMPORTANT: Éviter le double comptage EPANET
                # Mettre à zéro la 3ème colonne (demande) dans [JUNCTIONS]
                new_lines = lines.copy()
                zeroed_count = 0
                for i in range(junctions_idx + 1, len(new_lines)):
                    line = new_lines[i].strip()
                    if line.startswith('['):
                        break  # Fin de la section
                    if line and not line.startswith(';'):
                        parts = line.split()
                        if len(parts) >= 3:
                            try:
                                old_demand = float(parts[2])
                                if old_demand > 0:
                                    # Remplacer la demande (3ème colonne) par 0
                                    parts[2] = "0"
                                    new_lines[i] = " ".join(parts) + "\n"
                                    zeroed_count += 1
                            except (ValueError, IndexError):
                                continue
                
                # Insérer les nouvelles demandes après la ligne [DEMANDS]
                new_lines = new_lines[:demands_idx + 1] + demands_to_add + new_lines[demands_idx + 1:]
                temp_path = _write_lines_to_temp_file(new_lines, ".demand_filled.inp")
                
                rprint(f"[green]✅ Section [DEMANDS] remplie automatiquement avec {len(demands_to_add) - 2} entrées[/green]")
                rprint(f"[cyan]📊 Somme totale des demandes : {total_demand:.4f} (moyenne : {total_demand/node_count:.4f} par nœud)[/cyan]")
                rprint(f"[blue]💡 EPANET utilisera ces demandes comme valeurs constantes (pattern = 1.0)[/blue]")
                rprint(f"[yellow]⚠️  IMPORTANT: {zeroed_count} demandes mises à zéro dans [JUNCTIONS] pour éviter le double comptage EPANET[/yellow]")
                rprint(f"[green]✅ Résultat final : demande totale = {total_demand:.4f} (pas de double comptage)[/green]")
                
                # VÉRIFICATION AUTOMATIQUE : S'assurer que le double comptage est évité
                rprint(f"\n🔍 [bold cyan]VÉRIFICATION AUTOMATIQUE DES DEMANDES...[/bold cyan]")
                success, verification_details = verify_demands_in_file(temp_path)
                display_verification_results(temp_path, verification_details)
                
                if not success:
                    rprint(f"\n[red]⚠️  ATTENTION : Problème détecté dans la gestion des demandes ![/red]")
                
                return temp_path
            else:
                rprint("[yellow]⚠️  Aucune demande > 0 trouvée dans [JUNCTIONS].[/yellow]")

    except Exception as e:
        rprint(f"[red]❌ Erreur inattendue dans _ensure_demand_from_junctions: {e}[/red]")
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

        # Vérifier si des demandes existent déjà
        existing_demands = False
        if demands_idx != -1:
            for i in range(demands_idx + 1, len(lines)):
                line = lines[i].strip()
                if line.startswith('['):
                    break  # Nouvelle section
                if line and not line.startswith(';'):
                    # Vérifier si c'est vraiment du contenu (pas juste un en-tête)
                    words = line.split()
                    if not any(word.lower() in ['junction', 'demand', 'pattern', 'category', 'id', 'status', 'setting'] for word in words):
                        existing_demands = True
                        break

        # Si des demandes existent, demander confirmation
        if existing_demands:
            rprint(f"[yellow]⚠️  Des demandes existantes ont été détectées dans la section [DEMANDS].[/yellow]")
            rprint(f"[yellow]Ces demandes peuvent provenir de la section [JUNCTIONS] (3ème colonne) ou d'une configuration précédente.[/yellow]")
            rprint(f"[yellow]Voulez-vous écraser ces demandes avec la valeur {demand_value} ? (y/N)[/yellow]")
            rprint(f"[blue]💡 Répondre 'N' conservera les demandes existantes (recommandé si elles viennent de [JUNCTIONS])[/blue]")
            
            try:
                response = input().strip().lower()
                if response not in ['y', 'yes', 'oui', 'o']:
                    rprint("[blue]✅ Opération annulée. Conservation des demandes existantes.[/blue]")
                    rprint("[blue]📝 Utilisation du fichier original avec les demandes de [JUNCTIONS].[/blue]")
                    return input_path
            except (EOFError, KeyboardInterrupt):
                rprint("[blue]✅ Opération annulée. Conservation des demandes existantes.[/blue]")
                rprint("[blue]📝 Utilisation du fichier original avec les demandes de [JUNCTIONS].[/blue]")
                return input_path

        # Si pas de section [DEMANDS], la créer
        if demands_idx == -1:
            # Insérer la section [DEMANDS] après [JUNCTIONS] ou au début
            insert_pos = junctions_idx + 1 if junctions_idx != -1 else 0
            new_lines = lines[:insert_pos] + ["\n[DEMANDS]\n"] + lines[insert_pos:]
            lines = new_lines
            demands_idx = insert_pos

        # Calculer le nombre de nœuds et la demande par nœud
        node_count = 0
        if junctions_idx != -1:
            for line in lines[junctions_idx + 1:]:
                stripped = line.strip()
                if stripped.startswith('['):
                    break
                if stripped and not stripped.startswith(';'):
                    parts = stripped.split()
                    if len(parts) >= 1:
                        node_count += 1

        if node_count == 0:
            rprint("[red]❌ Aucun nœud trouvé dans la section [JUNCTIONS].[/red]")
            raise typer.Exit(1)

        demand_per_node = demand_value / node_count

        # Remplacer ou ajouter les demandes
        new_demands = [
            f"; Demandes injectées: {demand_value:.4f} réparties sur {node_count} nœuds\n",
            ";Node  BaseDemand  Pattern  Category\n"
        ]
        
        # Parcourir les nœuds et ajouter les demandes
        if junctions_idx != -1:
            for line in lines[junctions_idx + 1:]:
                stripped = line.strip()
                if stripped.startswith('['):
                    break
                if stripped and not stripped.startswith(';'):
                    parts = stripped.split()
                    if len(parts) >= 1:
                        node_id = parts[0]
                        new_demands.append(f"{node_id:<16} {demand_per_node:<16.4f}\n")

        # Remplacer la section [DEMANDS] existante
        # Trouver la fin de la section [DEMANDS]
        demands_end = demands_idx + 1
        for i in range(demands_idx + 1, len(lines)):
            if lines[i].strip().startswith('['):
                demands_end = i
                break
        else:
            demands_end = len(lines)

        # Construire le nouveau fichier
        new_lines = lines[:demands_idx + 1] + new_demands + lines[demands_end:]

        # Écrire le fichier temporaire
        temp_path = _write_lines_to_temp_file(new_lines, ".demand_override.inp")

        if not no_log:
            rprint(f"[green]✅ Demande de {demand_value:.4f} répartie sur {node_count} nœuds ({demand_per_node:.4f} par nœud)[/green]")
            rprint(f"[green]📝 Fichier INP traité: {temp_path}[/green]")
            
            # VÉRIFICATION AUTOMATIQUE : S'assurer que la demande est correctement appliquée
            rprint(f"\n🔍 [bold cyan]VÉRIFICATION AUTOMATIQUE DES DEMANDES...[/bold cyan]")
            success, verification_details = verify_demands_in_file(temp_path)
            display_verification_results(temp_path, verification_details)
            
            if not success:
                rprint(f"\n[red]⚠️  ATTENTION : Problème détecté dans la gestion des demandes ![/red]")

        return temp_path

    except Exception as e:
        rprint(f"[red]❌ Erreur lors de l'application de la demande: {e}[/red]")
        raise typer.Exit(1)
