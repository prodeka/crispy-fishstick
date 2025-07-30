"""
Module pour les fonctionnalités avancées de rapports LCPI-CLI
Inclut : cache, parallélisation, synthèse intelligente, comparaison
"""

import hashlib
import pickle
import time
import json
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
from rich.console import Console

console = Console()

class ReportCache:
    """Système de cache pour les résultats de calculs."""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = pathlib.Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "report_cache.pkl"
        self.cache_data = self._load_cache()
    
    def _load_cache(self) -> Dict[str, Any]:
        """Charge le cache depuis le fichier."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                console.print(f"[yellow]Impossible de charger le cache: {e}[/yellow]")
        return {}
    
    def _save_cache(self):
        """Sauvegarde le cache dans le fichier."""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache_data, f)
        except Exception as e:
            console.print(f"[yellow]Impossible de sauvegarder le cache: {e}[/yellow]")
    
    def _calculate_file_hash(self, file_path: pathlib.Path) -> str:
        """Calcule le hash d'un fichier."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
    
    def get_cached_result(self, file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
        """Récupère un résultat en cache si disponible."""
        file_hash = self._calculate_file_hash(file_path)
        cache_key = f"{file_path}_{file_hash}"
        
        if cache_key in self.cache_data:
            cached_data = self.cache_data[cache_key]
            # Vérifier que le cache n'est pas trop ancien (7 jours)
            if time.time() - cached_data.get('timestamp', 0) < 7 * 24 * 3600:
                return cached_data.get('result')
        return None
    
    def cache_result(self, file_path: pathlib.Path, result: Dict[str, Any]):
        """Met en cache un résultat."""
        file_hash = self._calculate_file_hash(file_path)
        cache_key = f"{file_path}_{file_hash}"
        
        self.cache_data[cache_key] = {
            'result': result,
            'timestamp': time.time(),
            'file_path': str(file_path)
        }
        self._save_cache()
    
    def clear_cache(self):
        """Vide le cache."""
        self.cache_data = {}
        if self.cache_file.exists():
            self.cache_file.unlink()
        console.print("[green]Cache vidé avec succès[/green]")

class ReportAnalyzer:
    """Analyseur intelligent pour les rapports de synthèse."""
    
    @staticmethod
    def generate_synthesis(results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Génère une synthèse intelligente des résultats."""
        synthesis = {
            'total_elements': len(results),
            'plugins_used': list(set(r.get('plugin', 'Inconnu') for r in results)),
            'status_summary': {},
            'critical_ratios': [],
            'warnings': [],
            'errors': [],
            'success_rate': 0.0
        }
        
        # Analyse des statuts
        for result in results:
            status = result.get('statut', 'Inconnu')
            synthesis['status_summary'][status] = synthesis['status_summary'].get(status, 0) + 1
        
        # Calcul du taux de succès
        success_count = synthesis['status_summary'].get('OK', 0)
        synthesis['success_rate'] = (success_count / len(results)) * 100 if results else 0
        
        # Analyse des ratios critiques
        for result in results:
            resultats = result.get('resultats', {})
            for key, value in resultats.items():
                if any(crit_key in key.lower() for crit_key in ['ratio', 'coefficient', 'securite', 'verification']):
                    try:
                        if isinstance(value, str):
                            # Extraire la valeur numérique si possible
                            import re
                            num_match = re.search(r'(\d+\.?\d*)', value)
                            if num_match:
                                num_value = float(num_match.group(1))
                            else:
                                continue
                        else:
                            num_value = float(value)
                        
                        synthesis['critical_ratios'].append({
                            'element': result.get('element_id', 'Inconnu'),
                            'parameter': key,
                            'value': num_value,
                            'status': result.get('statut', 'Inconnu')
                        })
                    except (ValueError, TypeError):
                        continue
        
        # Tri des ratios critiques par valeur
        synthesis['critical_ratios'].sort(key=lambda x: x['value'])
        
        # Collecte des avertissements et erreurs
        for result in results:
            if result.get('statut') == 'Avertissement':
                synthesis['warnings'].append({
                    'element': result.get('element_id', 'Inconnu'),
                    'plugin': result.get('plugin', 'Inconnu'),
                    'details': result.get('resultats', {})
                })
            elif result.get('statut') == 'Erreur':
                synthesis['errors'].append({
                    'element': result.get('element_id', 'Inconnu'),
                    'plugin': result.get('plugin', 'Inconnu'),
                    'details': result.get('resultats', {})
                })
        
        return synthesis
    
    @staticmethod
    def compare_reports(current_results: List[Dict[str, Any]], previous_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare deux rapports et identifie les différences."""
        comparison = {
            'added_elements': [],
            'removed_elements': [],
            'modified_elements': [],
            'summary_changes': {}
        }
        
        # Créer des dictionnaires pour faciliter la comparaison
        current_dict = {r.get('element_id'): r for r in current_results}
        previous_dict = {r.get('element_id'): r for r in previous_results}
        
        # Éléments ajoutés
        for element_id in current_dict:
            if element_id not in previous_dict:
                comparison['added_elements'].append(element_id)
        
        # Éléments supprimés
        for element_id in previous_dict:
            if element_id not in current_dict:
                comparison['removed_elements'].append(element_id)
        
        # Éléments modifiés
        for element_id in current_dict:
            if element_id in previous_dict:
                current = current_dict[element_id]
                previous = previous_dict[element_id]
                
                changes = []
                
                # Comparer les statuts
                if current.get('statut') != previous.get('statut'):
                    changes.append({
                        'type': 'status',
                        'field': 'statut',
                        'old': previous.get('statut'),
                        'new': current.get('statut')
                    })
                
                # Comparer les résultats numériques
                current_resultats = current.get('resultats', {})
                previous_resultats = previous.get('resultats', {})
                
                for key in set(current_resultats.keys()) | set(previous_resultats.keys()):
                    current_val = current_resultats.get(key)
                    previous_val = previous_resultats.get(key)
                    
                    if current_val != previous_val:
                        # Essayer de calculer la différence pour les valeurs numériques
                        try:
                            if isinstance(current_val, str) and isinstance(previous_val, str):
                                import re
                                curr_num = re.search(r'(\d+\.?\d*)', current_val)
                                prev_num = re.search(r'(\d+\.?\d*)', previous_val)
                                
                                if curr_num and prev_num:
                                    curr_float = float(curr_num.group(1))
                                    prev_float = float(prev_num.group(1))
                                    if prev_float != 0:
                                        percentage_change = ((curr_float - prev_float) / prev_float) * 100
                                        changes.append({
                                            'type': 'numeric',
                                            'field': key,
                                            'old': previous_val,
                                            'new': current_val,
                                            'change_percent': percentage_change
                                        })
                                    else:
                                        changes.append({
                                            'type': 'value',
                                            'field': key,
                                            'old': previous_val,
                                            'new': current_val
                                        })
                                else:
                                    changes.append({
                                        'type': 'value',
                                        'field': key,
                                        'old': previous_val,
                                        'new': current_val
                                    })
                            else:
                                changes.append({
                                    'type': 'value',
                                    'field': key,
                                    'old': previous_val,
                                    'new': current_val
                                })
                        except (ValueError, TypeError):
                            changes.append({
                                'type': 'value',
                                'field': key,
                                'old': previous_val,
                                'new': current_val
                            })
                
                if changes:
                    comparison['modified_elements'].append({
                        'element_id': element_id,
                        'changes': changes
                    })
        
        # Résumé des changements
        comparison['summary_changes'] = {
            'total_elements_current': len(current_results),
            'total_elements_previous': len(previous_results),
            'elements_added': len(comparison['added_elements']),
            'elements_removed': len(comparison['removed_elements']),
            'elements_modified': len(comparison['modified_elements'])
        }
        
        return comparison

class ParallelAnalyzer:
    """Analyseur parallèle pour les projets."""
    
    def __init__(self, cache: Optional[ReportCache] = None, max_workers: int = 4):
        self.cache = cache
        self.max_workers = max_workers
    
    def _process_single_file(self, yml_file: pathlib.Path, plugin_name: str, command: str) -> Optional[Dict[str, Any]]:
        """Traite un seul fichier YML et retourne le résultat."""
        try:
            # Vérifier le cache si activé
            if self.cache:
                cached_result = self.cache.get_cached_result(yml_file)
                if cached_result:
                    return cached_result
            
            script_path = pathlib.Path(__file__).parent.parent.parent / "main.py"
            cmd = [sys.executable, str(script_path), plugin_name, command, str(yml_file), "--json"]
            
            process = subprocess.run(
                cmd, capture_output=True, text=True, check=False, encoding='utf-8', errors='ignore'
            )
            
            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    returncode=process.returncode,
                    cmd=cmd,
                    stderr=process.stderr
                )

            output = process.stdout
            start = output.find('{')
            end = output.rfind('}') + 1
            if start != -1 and end != 0:
                json_output = output[start:end]
                data = json.loads(json_output)
                
                # Mettre en cache le résultat
                if self.cache:
                    self.cache.cache_result(yml_file, data)
                
                return data
            else:
                console.log(f"[yellow]Avertissement[/yellow]: Pas de sortie JSON pour {yml_file.name}.")
                return None

        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Erreur lors de l'analyse de {yml_file.name}[/bold red]")
            console.print(f"[red]  Code de sortie: {e.returncode}[/red]")
            error_output = e.stderr or e.stdout or ""
            console.print(f"[red]  Erreur: {error_output.strip()}[/red]")
            return None
        except json.JSONDecodeError:
            console.print(f"[bold red]Erreur de décodage JSON pour {yml_file.name}[/bold red]")
            return None
        except Exception as e:
            console.print(f"[bold red]Une erreur inattendue est survenue avec {yml_file.name}: {e}[/bold red]")
            return None
    
    def analyze_project_parallel(self, project_dir: pathlib.Path, plugin_commands: Dict[str, str]) -> List[Dict[str, Any]]:
        """Analyse le projet en parallèle avec cache."""
        results = []
        files_to_process = []
        
        # Collecter tous les fichiers à traiter
        for plugin in plugin_commands.keys():
            plugin_dir = pathlib.Path(__file__).parent.parent.parent / plugin
            if plugin_dir.is_dir():
                for yml_file in plugin_dir.glob("**/*.yml"):
                    try:
                        plugin_name = yml_file.relative_to(pathlib.Path(__file__).parent.parent.parent).parts[0]
                        command = plugin_commands.get(plugin_name)
                        if command:
                            files_to_process.append((yml_file, plugin_name, command))
                    except ValueError:
                        continue
        
        if not files_to_process:
            console.print("[yellow]Aucun fichier .yml à analyser n'a été trouvé dans les plugins.[/yellow]")
            return results
        
        # Traitement parallèle
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Soumettre toutes les tâches
            future_to_file = {
                executor.submit(self._process_single_file, yml_file, plugin_name, command): yml_file
                for yml_file, plugin_name, command in files_to_process
            }
            
            # Traiter les résultats au fur et à mesure
            for future in as_completed(future_to_file):
                yml_file = future_to_file[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    console.print(f"[red]Erreur avec {yml_file.name}: {e}[/red]")
        
        return results 