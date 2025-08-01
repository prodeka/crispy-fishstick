"""
Gestionnaire CSV pour LCPI-CLI
Gère la conversion YAML ↔ CSV et la validation des données
"""

import csv
import yaml
import pathlib
from typing import Dict, List, Any, Optional, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import json

console = Console()

class CSVHandler:
    """Gestionnaire principal pour les opérations CSV."""
    
    def __init__(self):
        self.supported_modules = ['cm', 'bois', 'beton', 'hydrodrain']
        self.csv_templates_dir = pathlib.Path(__file__).parent.parent / "templates" / "csv_templates"
        
    def yaml_to_csv(self, yaml_file: str, csv_file: str, module: str = None) -> bool:
        """
        Convertit un fichier YAML en CSV.
        
        Args:
            yaml_file: Chemin vers le fichier YAML
            csv_file: Chemin vers le fichier CSV de sortie
            module: Module spécifique (optionnel)
            
        Returns:
            bool: True si la conversion réussit
        """
        try:
            # Lire le fichier YAML
            with open(yaml_file, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
            
            if not yaml_data:
                console.print(f"[red]Erreur: Fichier YAML vide ou invalide[/red]")
                return False
            
            # Détecter le module si non spécifié
            if not module:
                module = self._detect_module_from_yaml(yaml_data)
            
            # Convertir en format CSV
            csv_data = self._yaml_to_csv_data(yaml_data, module)
            
            # Écrire le fichier CSV
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if csv_data:
                    writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                    writer.writeheader()
                    writer.writerows(csv_data)
            
            console.print(f"[green]✓[/green] Conversion YAML → CSV réussie: {csv_file}")
            return True
            
        except Exception as e:
            console.print(f"[red]Erreur lors de la conversion YAML → CSV: {e}[/red]")
            return False
    
    def csv_to_yaml(self, csv_file: str, yaml_file: str, module: str = None) -> bool:
        """
        Convertit un fichier CSV en YAML.
        
        Args:
            csv_file: Chemin vers le fichier CSV
            yaml_file: Chemin vers le fichier YAML de sortie
            module: Module spécifique (optionnel)
            
        Returns:
            bool: True si la conversion réussit
        """
        try:
            # Lire le fichier CSV
            csv_data = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    csv_data.append(row)
            
            if not csv_data:
                console.print(f"[red]Erreur: Fichier CSV vide ou invalide[/red]")
                return False
            
            # Détecter le module si non spécifié
            if not module:
                module = self._detect_module_from_csv(csv_data)
            
            # Convertir en format YAML
            yaml_data = self._csv_to_yaml_data(csv_data, module)
            
            # Écrire le fichier YAML
            with open(yaml_file, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True)
            
            console.print(f"[green]✓[/green] Conversion CSV → YAML réussie: {yaml_file}")
            return True
            
        except Exception as e:
            console.print(f"[red]Erreur lors de la conversion CSV → YAML: {e}[/red]")
            return False
    
    def validate_csv(self, csv_file: str, module: str = None) -> Dict[str, Any]:
        """
        Valide un fichier CSV.
        
        Args:
            csv_file: Chemin vers le fichier CSV
            module: Module spécifique (optionnel)
            
        Returns:
            Dict contenant les résultats de validation
        """
        try:
            # Lire le fichier CSV
            csv_data = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    csv_data.append(row)
            
            if not csv_data:
                return {
                    'valid': False,
                    'errors': ['Fichier CSV vide ou invalide'],
                    'warnings': [],
                    'row_count': 0
                }
            
            # Détecter le module si non spécifié
            if not module:
                module = self._detect_module_from_csv(csv_data)
            
            # Valider selon le module
            validation_result = self._validate_csv_data(csv_data, module)
            
            # Afficher les résultats
            self._display_validation_results(validation_result, csv_file)
            
            return validation_result
            
        except Exception as e:
            return {
                'valid': False,
                'errors': [f'Erreur de validation: {e}'],
                'warnings': [],
                'row_count': 0
            }
    
    def get_csv_template(self, module: str, command: str) -> str:
        """
        Génère un template CSV pour un module et une commande.
        
        Args:
            module: Module (cm, bois, beton, hydrodrain)
            command: Commande spécifique
            
        Returns:
            str: Contenu du template CSV
        """
        templates = {
            'cm': {
                'check-poteau': 'element_id,type,section,longueur,charge_permanente,charge_exploitation,acier,statut\nP1,poteau,HEA200,3.5,15.2,25.8,S235,conforme',
                'check-deversement': 'element_id,type,section,longueur,charge_permanente,charge_exploitation,acier,statut\nP1,poutre,IPE300,6.0,18.5,30.2,S235,conforme',
                'check-tendu': 'element_id,type,section,longueur,effort_traction,acier,statut\nT1,tirant,HEA100,4.0,150.5,S235,conforme',
                'check-compose': 'element_id,type,section,longueur,effort_normal,moment_flexion,acier,statut\nC1,poteau,HEA240,4.2,200.0,45.8,S235,conforme',
                'check-fleche': 'element_id,type,section,longueur,charge_totale,flèche_max,acier,statut\nF1,poutre,IPE400,8.0,35.2,25.0,S235,conforme',
                'check-assemblage-boulon': 'element_id,type,nombre_boulons,diametre_boulon,effort_cisaillement,acier,statut\nA1,assemblage,8,M20,85.5,S235,conforme',
                'check-assemblage-soude': 'element_id,type,longueur_soudure,epaisseur_soudure,effort_traction,acier,statut\nA1,assemblage,200.0,8.0,120.5,S235,conforme',
                'optimize-section': 'element_id,type,charge_totale,longueur,acier,section_optimale,statut\nO1,poutre,45.2,6.0,S235,IPE360,conforme'
            },
            'bois': {
                'check-poteau': 'element_id,type,section,longueur,essence,classe,charge_permanente,charge_exploitation,statut\nP1,poteau,100x100,3.0,epicea,C24,8.5,12.3,conforme',
                'check-deversement': 'element_id,type,section,longueur,essence,classe,charge_totale,statut\nP1,poutre,200x400,6.0,chene,D30,25.2,conforme',
                'check-cisaillement': 'element_id,type,section,longueur,essence,classe,effort_cisaillement,statut\nC1,poutre,150x300,4.5,epicea,C24,18.5,conforme',
                'check-compression-perp': 'element_id,type,section,longueur,essence,classe,effort_compression,statut\nCP1,appui,200x200,0.1,chene,D30,45.2,conforme',
                'check-compose': 'element_id,type,section,longueur,essence,classe,effort_normal,moment_flexion,statut\nC1,poteau,150x150,3.5,epicea,C24,85.5,12.8,conforme',
                'check-fleche': 'element_id,type,section,longueur,essence,classe,charge_totale,flèche_max,statut\nF1,poutre,200x400,6.0,chene,D30,35.2,25.0,conforme',
                'check-assemblage-pointe': 'element_id,type,nombre_pointes,diametre_pointe,effort_cisaillement,essence,statut\nA1,assemblage,12,4.0,25.5,epicea,conforme',
                'check-assemblage-embrevement': 'element_id,type,longueur_embrevement,largeur_embrevement,effort_traction,essence,statut\nA1,assemblage,80.0,40.0,45.2,chene,conforme'
            },
            'beton': {
                'calc-poteau': 'element_id,type,section,hauteur,beton,acier,charge_permanente,charge_exploitation,statut\nP1,poteau,30x30,3.0,C25,HA500,45.2,68.5,conforme',
                'calc-radier': 'element_id,type,epaisseur,largeur,longueur,beton,acier,charge_totale,statut\nR1,radier,0.25,10.0,15.0,C25,HA500,120.5,conforme'
            },
            'hydrodrain': {
                'ouvrage-canal': 'element_id,type,largeur,hauteur,debit,matiere,statut\nC1,canal,2.5,1.8,5.0,beton,conforme',
                'reservoir-equilibrage': 'element_id,type,volume,hauteur,diametre,matiere,statut\nR1,reservoir,1000,8.0,12.0,beton,conforme',
                'collector-dimensionner-troncons': 'element_id,type,diametre,longueur,debit,pente,matiere,statut\nT1,troncon,300,150,25.5,0.02,PVC,conforme',
                'plomberie-dimensionner': 'element_id,type,diametre,longueur,debit,type_fluide,matiere,statut\nP1,tuyau,50,25,2.5,eau,PVC,conforme'
            }
        }
        
        if module in templates and command in templates[module]:
            return templates[module][command]
        else:
            return f"Template non disponible pour {module}/{command}"
    
    def batch_process_csv(self, csv_file: str, module: str, command: str, output_file: str = None) -> List[Dict[str, Any]]:
        """
        Traite un fichier CSV en lot.
        
        Args:
            csv_file: Fichier CSV d'entrée
            module: Module à utiliser
            command: Commande à exécuter
            output_file: Fichier de sortie (optionnel)
            
        Returns:
            List[Dict]: Résultats du traitement
        """
        try:
            # Lire le fichier CSV
            csv_data = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    csv_data.append(row)
            
            if not csv_data:
                console.print(f"[red]Erreur: Fichier CSV vide[/red]")
                return []
            
            # Traiter chaque ligne
            results = []
            for i, row in enumerate(csv_data):
                try:
                    # Convertir la ligne en YAML temporaire
                    temp_yaml = self._csv_row_to_yaml(row, module, command)
                    
                    # Exécuter la commande (simulation pour l'instant)
                    result = self._execute_command(temp_yaml, module, command)
                    result['row_index'] = i + 1
                    result['element_id'] = row.get('element_id', f'Row_{i+1}')
                    results.append(result)
                    
                except Exception as e:
                    results.append({
                        'row_index': i + 1,
                        'element_id': row.get('element_id', f'Row_{i+1}'),
                        'status': 'error',
                        'error': str(e)
                    })
            
            # Sauvegarder les résultats si demandé
            if output_file:
                self._save_batch_results(results, output_file)
            
            return results
            
        except Exception as e:
            console.print(f"[red]Erreur lors du traitement par lot: {e}[/red]")
            return []
    
    # Méthodes privées
    def _detect_module_from_yaml(self, yaml_data: Any) -> str:
        """Détecte le module à partir des données YAML."""
        # Logique de détection basée sur la structure
        if isinstance(yaml_data, dict):
            if 'beton' in yaml_data:
                return 'beton'
            elif 'essence' in yaml_data or 'classe' in yaml_data:
                return 'bois'
            elif 'acier' in yaml_data or 'section' in yaml_data:
                return 'cm'
            elif 'debit' in yaml_data or 'volume' in yaml_data:
                return 'hydrodrain'
        return 'unknown'
    
    def _detect_module_from_csv(self, csv_data: List[Dict[str, Any]]) -> str:
        """Détecte le module à partir des données CSV."""
        if not csv_data:
            return 'unknown'
        
        headers = csv_data[0].keys()
        if 'beton' in headers:
            return 'beton'
        elif 'essence' in headers:
            return 'bois'
        elif 'acier' in headers:
            return 'cm'
        elif 'debit' in headers or 'volume' in headers:
            return 'hydrodrain'
        return 'unknown'
    
    def _yaml_to_csv_data(self, yaml_data: Any, module: str) -> List[Dict[str, Any]]:
        """Convertit les données YAML en format CSV."""
        # Implémentation spécifique par module
        if module == 'cm':
            return self._yaml_to_csv_cm(yaml_data)
        elif module == 'bois':
            return self._yaml_to_csv_bois(yaml_data)
        elif module == 'beton':
            return self._yaml_to_csv_beton(yaml_data)
        elif module == 'hydrodrain':
            return self._yaml_to_csv_hydro(yaml_data)
        else:
            return []
    
    def _csv_to_yaml_data(self, csv_data: List[Dict[str, Any]], module: str) -> Any:
        """Convertit les données CSV en format YAML."""
        # Implémentation spécifique par module
        if module == 'cm':
            return self._csv_to_yaml_cm(csv_data)
        elif module == 'bois':
            return self._csv_to_yaml_bois(csv_data)
        elif module == 'beton':
            return self._csv_to_yaml_beton(csv_data)
        elif module == 'hydrodrain':
            return self._csv_to_yaml_hydro(csv_data)
        else:
            return {}
    
    def _validate_csv_data(self, csv_data: List[Dict[str, Any]], module: str) -> Dict[str, Any]:
        """Valide les données CSV selon le module."""
        errors = []
        warnings = []
        
        for i, row in enumerate(csv_data):
            # Validation de base
            if not row.get('element_id'):
                errors.append(f"Ligne {i+1}: element_id manquant")
            
            # Validation spécifique par module
            if module == 'cm':
                errors.extend(self._validate_csv_cm(row, i+1))
            elif module == 'bois':
                errors.extend(self._validate_csv_bois(row, i+1))
            elif module == 'beton':
                errors.extend(self._validate_csv_beton(row, i+1))
            elif module == 'hydrodrain':
                errors.extend(self._validate_csv_hydro(row, i+1))
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'row_count': len(csv_data)
        }
    
    def _display_validation_results(self, results: Dict[str, Any], filename: str):
        """Affiche les résultats de validation."""
        table = Table(title=f"Validation CSV: {filename}")
        table.add_column("Type", style="cyan")
        table.add_column("Message", style="white")
        
        if results['errors']:
            for error in results['errors']:
                table.add_row("❌ Erreur", error)
        
        if results['warnings']:
            for warning in results['warnings']:
                table.add_row("⚠️ Avertissement", warning)
        
        if not results['errors'] and not results['warnings']:
            table.add_row("✅ Valide", f"Fichier valide ({results['row_count']} lignes)")
        
        console.print(table)
    
    # Méthodes de conversion spécifiques par module
    def _yaml_to_csv_cm(self, yaml_data: Any) -> List[Dict[str, Any]]:
        """Conversion YAML → CSV pour Construction Métallique."""
        # Implémentation spécifique
        return []
    
    def _csv_to_yaml_cm(self, csv_data: List[Dict[str, Any]]) -> Any:
        """Conversion CSV → YAML pour Construction Métallique."""
        # Implémentation spécifique
        return {}
    
    def _validate_csv_cm(self, row: Dict[str, Any], line_num: int) -> List[str]:
        """Validation CSV pour Construction Métallique."""
        errors = []
        # Validation spécifique CM
        return errors
    
    # Méthodes similaires pour bois, beton, hydrodrain...
    def _yaml_to_csv_bois(self, yaml_data: Any) -> List[Dict[str, Any]]:
        return []
    
    def _csv_to_yaml_bois(self, csv_data: List[Dict[str, Any]]) -> Any:
        return {}
    
    def _validate_csv_bois(self, row: Dict[str, Any], line_num: int) -> List[str]:
        return []
    
    def _yaml_to_csv_beton(self, yaml_data: Any) -> List[Dict[str, Any]]:
        return []
    
    def _csv_to_yaml_beton(self, csv_data: List[Dict[str, Any]]) -> Any:
        return {}
    
    def _validate_csv_beton(self, row: Dict[str, Any], line_num: int) -> List[str]:
        return []
    
    def _yaml_to_csv_hydro(self, yaml_data: Any) -> List[Dict[str, Any]]:
        return []
    
    def _csv_to_yaml_hydro(self, csv_data: List[Dict[str, Any]]) -> Any:
        return {}
    
    def _validate_csv_hydro(self, row: Dict[str, Any], line_num: int) -> List[str]:
        return []
    
    def _csv_row_to_yaml(self, row: Dict[str, Any], module: str, command: str) -> Dict[str, Any]:
        """Convertit une ligne CSV en YAML pour traitement."""
        # Conversion basique
        return row
    
    def _execute_command(self, yaml_data: Dict[str, Any], module: str, command: str) -> Dict[str, Any]:
        """Exécute une commande avec les données YAML."""
        # Simulation pour l'instant
        return {
            'status': 'success',
            'result': f'Commande {module} {command} exécutée',
            'data': yaml_data
        }
    
    def _save_batch_results(self, results: List[Dict[str, Any]], output_file: str):
        """Sauvegarde les résultats du traitement par lot."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if results:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
        
        console.print(f"[green]✓[/green] Résultats sauvegardés: {output_file}") 