"""
Tests unitaires pour le gestionnaire CSV
"""

import pytest
import tempfile
import pathlib
import csv
import yaml
from src.lcpi.utils.csv_handler import CSVHandler
from src.lcpi.utils.csv_mappings import CSVMappings

class TestCSVHandler:
    """Tests pour la classe CSVHandler."""
    
    def setup_method(self):
        """Configuration avant chaque test."""
        self.handler = CSVHandler()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Nettoyage après chaque test."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test de l'initialisation."""
        assert self.handler.supported_modules == ['cm', 'bois', 'beton', 'hydrodrain']
        assert hasattr(self.handler, 'csv_templates_dir')
    
    def test_detect_module_from_yaml_cm(self):
        """Test de détection du module CM."""
        yaml_data = {'acier': 'S235', 'section': 'HEA200'}
        module = self.handler._detect_module_from_yaml(yaml_data)
        assert module == 'cm'
    
    def test_detect_module_from_yaml_bois(self):
        """Test de détection du module Bois."""
        yaml_data = {'essence': 'epicea', 'classe': 'C24'}
        module = self.handler._detect_module_from_yaml(yaml_data)
        assert module == 'bois'
    
    def test_detect_module_from_yaml_beton(self):
        """Test de détection du module Béton."""
        yaml_data = {'beton': 'C25', 'acier': 'HA500'}
        module = self.handler._detect_module_from_yaml(yaml_data)
        assert module == 'beton'
    
    def test_detect_module_from_yaml_hydro(self):
        """Test de détection du module Hydro."""
        yaml_data = {'debit': 5.0, 'volume': 1000}
        module = self.handler._detect_module_from_yaml(yaml_data)
        assert module == 'hydrodrain'
    
    def test_detect_module_from_csv_cm(self):
        """Test de détection du module CM depuis CSV."""
        csv_data = [{'acier': 'S235', 'section': 'HEA200'}]
        module = self.handler._detect_module_from_csv(csv_data)
        assert module == 'cm'
    
    def test_detect_module_from_csv_bois(self):
        """Test de détection du module Bois depuis CSV."""
        csv_data = [{'essence': 'epicea', 'classe': 'C24'}]
        module = self.handler._detect_module_from_csv(csv_data)
        assert module == 'bois'
    
    def test_get_csv_template_cm(self):
        """Test de génération de template CSV pour CM."""
        template = self.handler.get_csv_template('cm', 'check-poteau')
        assert 'element_id' in template
        assert 'type' in template
        assert 'section' in template
        assert 'P1' in template
    
    def test_get_csv_template_bois(self):
        """Test de génération de template CSV pour Bois."""
        template = self.handler.get_csv_template('bois', 'check-poteau')
        assert 'element_id' in template
        assert 'essence' in template
        assert 'classe' in template
        assert 'P1' in template
    
    def test_get_csv_template_beton(self):
        """Test de génération de template CSV pour Béton."""
        template = self.handler.get_csv_template('beton', 'calc-poteau')
        assert 'element_id' in template
        assert 'beton' in template
        assert 'acier' in template
        assert 'P1' in template
    
    def test_get_csv_template_hydro(self):
        """Test de génération de template CSV pour Hydro."""
        template = self.handler.get_csv_template('hydrodrain', 'ouvrage-canal')
        assert 'element_id' in template
        assert 'debit' in template
        assert 'matiere' in template
        assert 'C1' in template
    
    def test_get_csv_template_unknown(self):
        """Test de template pour module/commande inconnue."""
        template = self.handler.get_csv_template('unknown', 'unknown')
        assert 'Template non disponible' in template
    
    def test_validate_csv_empty_file(self):
        """Test de validation d'un fichier CSV vide."""
        # Créer un fichier CSV vide
        csv_file = pathlib.Path(self.temp_dir) / "empty.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            f.write("element_id,type,section\n")
        
        validation = self.handler.validate_csv(str(csv_file))
        assert not validation['valid']
        assert 'vide' in validation['errors'][0]
        assert validation['row_count'] == 0
    
    def test_validate_csv_valid_cm(self):
        """Test de validation d'un fichier CSV CM valide."""
        # Créer un fichier CSV valide
        csv_file = pathlib.Path(self.temp_dir) / "valid_cm.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['element_id', 'type', 'section', 'acier'])
            writer.writerow(['P1', 'poteau', 'HEA200', 'S235'])
        
        validation = self.handler.validate_csv(str(csv_file))
        assert validation['valid']
        assert validation['row_count'] == 1
        assert len(validation['errors']) == 0
    
    def test_validate_csv_invalid_missing_element_id(self):
        """Test de validation d'un fichier CSV invalide (element_id manquant)."""
        # Créer un fichier CSV invalide
        csv_file = pathlib.Path(self.temp_dir) / "invalid.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['type', 'section', 'acier'])
            writer.writerow(['poteau', 'HEA200', 'S235'])
        
        validation = self.handler.validate_csv(str(csv_file))
        assert not validation['valid']
        assert any('element_id manquant' in error for error in validation['errors'])
    
    def test_batch_process_csv_empty(self):
        """Test de traitement par lot d'un fichier CSV vide."""
        # Créer un fichier CSV vide
        csv_file = pathlib.Path(self.temp_dir) / "empty.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            f.write("element_id,type,section\n")
        
        results = self.handler.batch_process_csv(str(csv_file), 'cm', 'check-poteau')
        assert len(results) == 0
    
    def test_batch_process_csv_valid(self):
        """Test de traitement par lot d'un fichier CSV valide."""
        # Créer un fichier CSV valide
        csv_file = pathlib.Path(self.temp_dir) / "valid.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['element_id', 'type', 'section'])
            writer.writerow(['P1', 'poteau', 'HEA200'])
            writer.writerow(['P2', 'poteau', 'HEA240'])
        
        results = self.handler.batch_process_csv(str(csv_file), 'cm', 'check-poteau')
        assert len(results) == 2
        assert results[0]['element_id'] == 'P1'
        assert results[1]['element_id'] == 'P2'
        assert results[0]['status'] == 'success'
        assert results[1]['status'] == 'success'
    
    def test_batch_process_csv_with_output(self):
        """Test de traitement par lot avec fichier de sortie."""
        # Créer un fichier CSV d'entrée
        csv_file = pathlib.Path(self.temp_dir) / "input.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['element_id', 'type', 'section'])
            writer.writerow(['P1', 'poteau', 'HEA200'])
        
        output_file = pathlib.Path(self.temp_dir) / "output.csv"
        results = self.handler.batch_process_csv(str(csv_file), 'cm', 'check-poteau', str(output_file))
        
        assert len(results) == 1
        assert output_file.exists()
        
        # Vérifier le contenu du fichier de sortie
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 1
            assert rows[0]['element_id'] == 'P1'

class TestCSVMappings:
    """Tests pour la classe CSVMappings."""
    
    def test_yaml_to_csv_cm_single(self):
        """Test de conversion YAML → CSV pour CM (élément unique)."""
        yaml_data = {
            'element_id': 'P1',
            'type': 'poteau',
            'section': 'HEA200',
            'longueur': 3.5,
            'acier': 'S235'
        }
        
        csv_data = CSVMappings.yaml_to_csv_cm(yaml_data)
        assert len(csv_data) == 1
        assert csv_data[0]['element_id'] == 'P1'
        assert csv_data[0]['type'] == 'poteau'
        assert csv_data[0]['section'] == 'HEA200'
        assert csv_data[0]['longueur'] == 3.5
        assert csv_data[0]['acier'] == 'S235'
    
    def test_yaml_to_csv_cm_list(self):
        """Test de conversion YAML → CSV pour CM (liste d'éléments)."""
        yaml_data = [
            {
                'element_id': 'P1',
                'type': 'poteau',
                'section': 'HEA200',
                'acier': 'S235'
            },
            {
                'element_id': 'P2',
                'type': 'poteau',
                'section': 'HEA240',
                'acier': 'S235'
            }
        ]
        
        csv_data = CSVMappings.yaml_to_csv_cm(yaml_data)
        assert len(csv_data) == 2
        assert csv_data[0]['element_id'] == 'P1'
        assert csv_data[1]['element_id'] == 'P2'
    
    def test_csv_to_yaml_cm_single(self):
        """Test de conversion CSV → YAML pour CM (élément unique)."""
        csv_data = [{
            'element_id': 'P1',
            'type': 'poteau',
            'section': 'HEA200',
            'longueur': '3.5',
            'acier': 'S235'
        }]
        
        yaml_data = CSVMappings.csv_to_yaml_cm(csv_data)
        assert yaml_data['element_id'] == 'P1'
        assert yaml_data['type'] == 'poteau'
        assert yaml_data['section'] == 'HEA200'
        assert yaml_data['longueur'] == 3.5
        assert yaml_data['acier'] == 'S235'
    
    def test_csv_to_yaml_cm_list(self):
        """Test de conversion CSV → YAML pour CM (liste d'éléments)."""
        csv_data = [
            {
                'element_id': 'P1',
                'type': 'poteau',
                'section': 'HEA200',
                'acier': 'S235'
            },
            {
                'element_id': 'P2',
                'type': 'poteau',
                'section': 'HEA240',
                'acier': 'S235'
            }
        ]
        
        yaml_data = CSVMappings.csv_to_yaml_cm(csv_data)
        assert len(yaml_data) == 2
        assert yaml_data[0]['element_id'] == 'P1'
        assert yaml_data[1]['element_id'] == 'P2'
    
    def test_yaml_to_csv_bois(self):
        """Test de conversion YAML → CSV pour Bois."""
        yaml_data = {
            'element_id': 'P1',
            'type': 'poteau',
            'section': '100x100',
            'essence': 'epicea',
            'classe': 'C24'
        }
        
        csv_data = CSVMappings.yaml_to_csv_bois(yaml_data)
        assert len(csv_data) == 1
        assert csv_data[0]['element_id'] == 'P1'
        assert csv_data[0]['essence'] == 'epicea'
        assert csv_data[0]['classe'] == 'C24'
    
    def test_csv_to_yaml_bois(self):
        """Test de conversion CSV → YAML pour Bois."""
        csv_data = [{
            'element_id': 'P1',
            'type': 'poteau',
            'section': '100x100',
            'longueur': '3.0',
            'essence': 'epicea',
            'classe': 'C24'
        }]
        
        yaml_data = CSVMappings.csv_to_yaml_bois(csv_data)
        assert yaml_data['element_id'] == 'P1'
        assert yaml_data['essence'] == 'epicea'
        assert yaml_data['classe'] == 'C24'
        assert yaml_data['longueur'] == 3.0
    
    def test_yaml_to_csv_beton(self):
        """Test de conversion YAML → CSV pour Béton."""
        yaml_data = {
            'element_id': 'P1',
            'type': 'poteau',
            'section': '30x30',
            'beton': 'C25',
            'acier': 'HA500'
        }
        
        csv_data = CSVMappings.yaml_to_csv_beton(yaml_data)
        assert len(csv_data) == 1
        assert csv_data[0]['element_id'] == 'P1'
        assert csv_data[0]['beton'] == 'C25'
        assert csv_data[0]['acier'] == 'HA500'
    
    def test_csv_to_yaml_beton(self):
        """Test de conversion CSV → YAML pour Béton."""
        csv_data = [{
            'element_id': 'P1',
            'type': 'poteau',
            'section': '30x30',
            'hauteur': '3.0',
            'beton': 'C25',
            'acier': 'HA500'
        }]
        
        yaml_data = CSVMappings.csv_to_yaml_beton(csv_data)
        assert yaml_data['element_id'] == 'P1'
        assert yaml_data['beton'] == 'C25'
        assert yaml_data['acier'] == 'HA500'
        assert yaml_data['hauteur'] == 3.0
    
    def test_yaml_to_csv_hydro(self):
        """Test de conversion YAML → CSV pour Hydro."""
        yaml_data = {
            'element_id': 'C1',
            'type': 'canal',
            'debit': 5.0,
            'matiere': 'beton'
        }
        
        csv_data = CSVMappings.yaml_to_csv_hydro(yaml_data)
        assert len(csv_data) == 1
        assert csv_data[0]['element_id'] == 'C1'
        assert csv_data[0]['debit'] == 5.0
        assert csv_data[0]['matiere'] == 'beton'
    
    def test_csv_to_yaml_hydro(self):
        """Test de conversion CSV → YAML pour Hydro."""
        csv_data = [{
            'element_id': 'C1',
            'type': 'canal',
            'debit': '5.0',
            'matiere': 'beton'
        }]
        
        yaml_data = CSVMappings.csv_to_yaml_hydro(csv_data)
        assert yaml_data['element_id'] == 'C1'
        assert yaml_data['debit'] == 5.0
        assert yaml_data['matiere'] == 'beton'

if __name__ == '__main__':
    pytest.main([__file__]) 