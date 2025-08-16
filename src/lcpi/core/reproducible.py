"""
Module pour l'export d'environnements reproductibles LCPI.

Ce module permet de créer des exports complets et reproductibles
des projets LCPI, incluant :
- Configuration du projet
- Dépendances exactes
- Logs et résultats
- Environnement de calcul
"""

import os
import json
import hashlib
import tarfile
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .global_config import global_config
from .context import project_context


class ReproducibleExporter:
    """Exportateur d'environnements reproductibles pour LCPI."""
    
    def __init__(self, project_path: Optional[Path] = None):
        self.project_path = project_path or project_context.get_project_path()
        self.export_dir = Path(tempfile.mkdtemp(prefix="lcpi_export_"))
        
    def export_reproducible(self, output_path: str, include_logs: bool = True, 
                           include_results: bool = True, include_env: bool = True) -> Dict[str, Any]:
        """
        Exporte un environnement reproductible complet.
        
        Args:
            output_path: Chemin du fichier d'export (.tar.gz)
            include_logs: Inclure les logs de calcul
            include_results: Inclure les résultats
            include_env: Inclure l'environnement Python
            
        Returns:
            Dict avec les métadonnées de l'export
        """
        try:
            # Créer la structure d'export
            export_info = self._create_export_structure()
            
            # Ajouter les fichiers du projet
            self._add_project_files()
            
            # Ajouter les logs si demandé
            if include_logs:
                self._add_logs()
                
            # Ajouter les résultats si demandé
            if include_results:
                self._add_results()
                
            # Ajouter l'environnement Python si demandé
            if include_env:
                self._add_environment()
                
            # Créer l'archive tar.gz
            self._create_archive(output_path)
            
            # Nettoyer
            self._cleanup()
            
            return export_info
            
        except Exception as e:
            self._cleanup()
            raise RuntimeError(f"Échec de l'export reproductible: {e}")
    
    def _create_export_structure(self) -> Dict[str, Any]:
        """Crée la structure de base de l'export."""
        export_info = {
            'export_date': datetime.now().isoformat(),
            'project_name': self.project_path.name,
            'project_path': str(self.project_path),
            'lcpi_version': '2.1.0',  # TODO: Récupérer depuis le code
            'checksums': {},
            'contents': []
        }
        
        # Créer la structure des dossiers
        (self.export_dir / 'project').mkdir(exist_ok=True)
        (self.export_dir / 'logs').mkdir(exist_ok=True)
        (self.export_dir / 'results').mkdir(exist_ok=True)
        (self.export_dir / 'environment').mkdir(exist_ok=True)
        
        return export_info
    
    def _add_project_files(self):
        """Ajoute les fichiers du projet à l'export."""
        project_export_dir = self.export_dir / 'project'
        
        # Copier les fichiers de configuration
        config_files = ['lcpi.yml', 'config.yml', 'pyproject.toml', 'requirements.txt']
        for config_file in config_files:
            config_path = self.project_path / config_file
            if config_path.exists():
                self._copy_file(config_path, project_export_dir / config_file)
        
        # Copier la structure des données
        data_dir = self.project_path / 'data'
        if data_dir.exists():
            self._copy_directory(data_dir, project_export_dir / 'data')
        
        # Copier les scripts
        scripts_dir = self.project_path / 'scripts'
        if scripts_dir.exists():
            self._copy_directory(scripts_dir, project_export_dir / 'scripts')
    
    def _add_logs(self):
        """Ajoute les logs de calcul à l'export."""
        logs_dir = self.project_path / 'logs'
        if not logs_dir.exists():
            return
            
        logs_export_dir = self.export_dir / 'logs'
        
        # Copier tous les fichiers de logs
        for log_file in logs_dir.glob('*'):
            if log_file.is_file():
                self._copy_file(log_file, logs_export_dir / log_file.name)
        
        # Créer un index des logs avec checksums
        logs_index = self._create_logs_index(logs_dir)
        with open(logs_export_dir / 'logs_index.json', 'w') as f:
            json.dump(logs_index, f, indent=2)
    
    def _add_results(self):
        """Ajoute les résultats de calcul à l'export."""
        output_dir = self.project_path / 'output'
        if not output_dir.exists():
            return
            
        results_export_dir = self.export_dir / 'results'
        
        # Copier les résultats
        self._copy_directory(output_dir, results_export_dir)
        
        # Créer un index des résultats
        results_index = self._create_results_index(output_dir)
        with open(results_export_dir / 'results_index.json', 'w') as f:
            json.dump(results_index, f, indent=2)
    
    def _add_environment(self):
        """Ajoute l'environnement Python à l'export."""
        env_export_dir = self.export_dir / 'environment'
        
        # Générer requirements.txt
        self._generate_requirements_txt(env_export_dir)
        
        # Générer Dockerfile minimal
        self._generate_dockerfile(env_export_dir)
        
        # Générer pyproject.toml
        self._generate_pyproject_toml(env_export_dir)
        
        # Informations sur l'environnement
        env_info = {
            'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            'platform': os.sys.platform,
            'export_date': datetime.now().isoformat()
        }
        
        with open(env_export_dir / 'environment_info.json', 'w') as f:
            json.dump(env_info, f, indent=2)
    
    def _create_logs_index(self, logs_dir: Path) -> Dict[str, Any]:
        """Crée un index des logs avec checksums."""
        logs_index = {
            'total_files': 0,
            'total_size': 0,
            'files': []
        }
        
        for log_file in logs_dir.glob('*'):
            if log_file.is_file():
                file_info = self._get_file_info(log_file)
                logs_index['files'].append(file_info)
                logs_index['total_files'] += 1
                logs_index['total_size'] += file_info['size']
        
        return logs_index
    
    def _create_results_index(self, output_dir: Path) -> Dict[str, Any]:
        """Crée un index des résultats avec checksums."""
        results_index = {
            'total_files': 0,
            'total_size': 0,
            'files': []
        }
        
        for result_file in output_dir.rglob('*'):
            if result_file.is_file():
                file_info = self._get_file_info(result_file)
                results_index['files'].append(file_info)
                results_index['total_files'] += 1
                results_index['total_size'] += file_info['size']
        
        return results_index
    
    def _get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Récupère les informations d'un fichier avec checksum."""
        stat = file_path.stat()
        
        # Calculer le checksum SHA256
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        return {
            'name': str(file_path.relative_to(self.project_path)),
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'checksum_sha256': sha256_hash.hexdigest()
        }
    
    def _generate_requirements_txt(self, env_dir: Path):
        """Génère un requirements.txt avec les dépendances exactes."""
        try:
            import pkg_resources
            requirements = []
            
            for dist in pkg_resources.working_set:
                requirements.append(f"{dist.project_name}=={dist.version}")
            
            with open(env_dir / 'requirements.txt', 'w') as f:
                f.write('\n'.join(sorted(requirements)))
                
        except ImportError:
            # Fallback si pkg_resources n'est pas disponible
            with open(env_dir / 'requirements.txt', 'w') as f:
                f.write("# Impossible de générer les dépendances exactes\n")
                f.write("# Utilisez 'pip freeze' manuellement\n")
    
    def _generate_dockerfile(self, env_dir: Path):
        """Génère un Dockerfile minimal pour reproduire l'environnement."""
        dockerfile_content = f"""# Dockerfile généré automatiquement par LCPI
# Date: {datetime.now().isoformat()}
# Projet: {self.project_path.name}

FROM python:3.11-slim

WORKDIR /app

# Copier les dépendances
COPY environment/requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY project/ .

# Point d'entrée
CMD ["python", "-m", "lcpi", "--help"]
"""
        
        with open(env_dir / 'Dockerfile', 'w') as f:
            f.write(dockerfile_content)
    
    def _generate_pyproject_toml(self, env_dir: Path):
        """Génère un pyproject.toml pour le projet."""
        pyproject_content = f"""[tool.poetry]
name = "{self.project_path.name}-reproducible"
version = "0.1.0"
description = "Export reproductible du projet {self.project_path.name}"
authors = ["LCPI Export <export@lcpi.local>"]

[tool.poetry.dependencies]
python = "^3.11"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

# Généré automatiquement par LCPI le {datetime.now().isoformat()}
"""
        
        with open(env_dir / 'pyproject.toml', 'w') as f:
            f.write(pyproject_content)
    
    def _copy_file(self, src: Path, dst: Path):
        """Copie un fichier avec gestion des erreurs."""
        try:
            import shutil
            shutil.copy2(src, dst)
        except Exception as e:
            print(f"Warning: Impossible de copier {src}: {e}")
    
    def _copy_directory(self, src: Path, dst: Path):
        """Copie un répertoire avec gestion des erreurs."""
        try:
            import shutil
            shutil.copytree(src, dst, dirs_exist_ok=True)
        except Exception as e:
            print(f"Warning: Impossible de copier {src}: {e}")
    
    def _create_archive(self, output_path: str):
        """Crée l'archive tar.gz finale."""
        with tarfile.open(output_path, "w:gz") as tar:
            tar.add(self.export_dir, arcname="lcpi_reproducible")
    
    def _cleanup(self):
        """Nettoie les fichiers temporaires."""
        try:
            import shutil
            shutil.rmtree(self.export_dir)
        except Exception:
            pass


def export_reproducible(project_path: Optional[Path] = None, output_path: str = "repro.tar.gz",
                        include_logs: bool = True, include_results: bool = True, 
                        include_env: bool = True) -> Dict[str, Any]:
    """
    Fonction utilitaire pour exporter un environnement reproductible.
    
    Args:
        project_path: Chemin du projet (optionnel)
        output_path: Chemin du fichier d'export
        include_logs: Inclure les logs
        include_results: Inclure les résultats
        include_env: Inclure l'environnement
        
    Returns:
        Dict avec les métadonnées de l'export
    """
    exporter = ReproducibleExporter(project_path)
    return exporter.export_reproducible(output_path, include_logs, include_results, include_env)
