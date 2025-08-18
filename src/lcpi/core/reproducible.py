"""
Module d'export reproductible pour LCPI - Jalon 2.
Permet d'exporter un projet complet avec son environnement pour la reproductibilité.
"""

import json
import tarfile
import hashlib
import os
import sys
import platform
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml

try:
    import pkg_resources
    PKG_RESOURCES_AVAILABLE = True
except ImportError:
    PKG_RESOURCES_AVAILABLE = False

class ReproducibleExporter:
    """Exporte un projet LCPI de manière reproductible."""
    
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.export_info = {}
        
    def export_reproducible(
        self,
        output_path: str,
        include_logs: bool = True,
        include_results: bool = True,
        include_env: bool = True,
        include_data: bool = True
    ) -> Dict[str, Any]:
        """
        Exporte le projet de manière reproductible.
        
        Args:
            output_path: Chemin de sortie pour l'archive
            include_logs: Inclure les logs de calcul
            include_results: Inclure les résultats exportés
            include_env: Inclure l'environnement Python
            include_data: Inclure les données du projet
            
        Returns:
            Informations sur l'export
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialiser les informations d'export
        self.export_info = {
            "export_date": datetime.now().isoformat(),
            "project_name": self.project_path.name,
            "project_path": str(self.project_path.absolute()),
            "lcpi_version": self._get_lcpi_version(),
            "python_version": sys.version,
            "platform": platform.platform(),
            "export_options": {
                "include_logs": include_logs,
                "include_results": include_results,
                "include_env": include_env,
                "include_data": include_data
            },
            "checksums": {},
            "files_included": []
        }
        
        # Créer l'archive tar.gz
        with tarfile.open(output_path, "w:gz") as tar:
            # Ajouter le projet principal
            self._add_project_to_tar(tar, include_data)
            
            # Ajouter les logs si demandé
            if include_logs:
                self._add_logs_to_tar(tar)
            
            # Ajouter les résultats si demandé
            if include_results:
                self._add_results_to_tar(tar)
            
            # Ajouter l'environnement si demandé
            if include_env:
                self._add_environment_to_tar(tar)
            
            # Ajouter les métadonnées d'export
            self._add_export_metadata_to_tar(tar)
        
        # Calculer le checksum de l'archive finale
        self.export_info["checksums"]["archive"] = self._calculate_file_checksum(output_path)
        self.export_info["files_included"] = list(set(self.export_info["files_included"]))
        
        # Sauvegarder les informations d'export
        metadata_path = output_path.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.export_info, f, indent=2, ensure_ascii=False)
        
        return self.export_info
    
    def _add_project_to_tar(self, tar: tarfile.TarFile, include_data: bool):
        """Ajoute le projet principal à l'archive."""
        project_files = []
        
        # Fichiers de configuration
        config_files = [
            "lcpi.yml", "config.yml", "pyproject.toml", "requirements.txt"
        ]
        
        for config_file in config_files:
            config_path = self.project_path / config_file
            if config_path.exists():
                project_files.append(config_path)
        
        # Répertoires du projet
        project_dirs = ["src", "templates", "docs"]
        if include_data:
            project_dirs.append("data")
        
        for project_dir in project_dirs:
            dir_path = self.project_path / project_dir
            if dir_path.exists():
                project_files.extend(dir_path.rglob("*"))
        
        # Ajouter les fichiers au tar
        for file_path in project_files:
            if file_path.is_file():
                arcname = f"project/{file_path.relative_to(self.project_path)}"
                tar.add(file_path, arcname=arcname)
                self.export_info["files_included"].append(str(file_path))
    
    def _add_logs_to_tar(self, tar: tarfile.TarFile):
        """Ajoute les logs de calcul à l'archive."""
        logs_dir = self.project_path / "logs"
        if not logs_dir.exists():
            return
        
        for log_file in logs_dir.rglob("*.json"):
            arcname = f"logs/{log_file.relative_to(logs_dir)}"
            tar.add(log_file, arcname=arcname)
            self.export_info["files_included"].append(str(log_file))
            
            # Calculer le checksum du log
            checksum = self._calculate_file_checksum(log_file)
            self.export_info["checksums"][f"log_{log_file.name}"] = checksum
    
    def _add_results_to_tar(self, tar: tarfile.TarFile):
        """Ajoute les résultats exportés à l'archive."""
        results_dir = self.project_path / "results"
        if not results_dir.exists():
            return
        
        for result_file in results_dir.rglob("*"):
            if result_file.is_file():
                arcname = f"results/{result_file.relative_to(results_dir)}"
                tar.add(result_file, arcname=arcname)
                self.export_info["files_included"].append(str(result_file))
    
    def _add_environment_to_tar(self, tar: tarfile.TarFile):
        """Ajoute l'environnement Python à l'archive."""
        # Générer requirements.txt
        requirements_content = self._generate_requirements_txt()
        requirements_path = Path("requirements.txt")
        requirements_path.write_text(requirements_content, encoding='utf-8')
        
        # Ajouter requirements.txt
        tar.add(requirements_path, arcname="environment/requirements.txt")
        self.export_info["files_included"].append(str(requirements_path))
        
        # Générer Dockerfile
        dockerfile_content = self._generate_dockerfile()
        dockerfile_path = Path("Dockerfile")
        dockerfile_path.write_text(dockerfile_content, encoding='utf-8')
        
        # Ajouter Dockerfile
        tar.add(dockerfile_path, arcname="environment/Dockerfile")
        self.export_info["files_included"].append(str(dockerfile_path))
        
        # Générer pyproject.toml
        pyproject_content = self._generate_pyproject_toml()
        pyproject_path = Path("pyproject.toml")
        pyproject_path.write_text(pyproject_content, encoding='utf-8')
        
        # Ajouter pyproject.toml
        tar.add(pyproject_path, arcname="environment/pyproject.toml")
        self.export_info["files_included"].append(str(pyproject_path))
        
        # Nettoyer les fichiers temporaires
        requirements_path.unlink()
        dockerfile_path.unlink()
        pyproject_path.unlink()
    
    def _add_export_metadata_to_tar(self, tar: tarfile.TarFile):
        """Ajoute les métadonnées d'export à l'archive."""
        # Créer un fichier temporaire avec les métadonnées
        metadata_content = json.dumps(self.export_info, indent=2, ensure_ascii=False)
        metadata_path = Path("export_metadata.json")
        metadata_path.write_text(metadata_content, encoding='utf-8')
        
        # Ajouter au tar
        tar.add(metadata_path, arcname="export_metadata.json")
        
        # Nettoyer
        metadata_path.unlink()
    
    def _generate_requirements_txt(self) -> str:
        """Génère un requirements.txt basé sur l'environnement actuel."""
        if not PKG_RESOURCES_AVAILABLE:
            return "# Requirements.txt généré automatiquement\n# Module pkg_resources non disponible"
        
        requirements = []
        requirements.append("# Requirements.txt généré automatiquement pour LCPI")
        requirements.append(f"# Généré le: {datetime.now().isoformat()}")
        requirements.append(f"# Python: {sys.version}")
        requirements.append("")
        
        # Obtenir les packages installés
        try:
            installed_packages = [d for d in pkg_resources.working_set]
            for package in sorted(installed_packages, key=lambda x: x.project_name.lower()):
                requirements.append(f"{package.project_name}=={package.version}")
        except Exception as e:
            requirements.append(f"# Erreur lors de la génération: {e}")
        
        return "\n".join(requirements)
    
    def _generate_dockerfile(self) -> str:
        """Génère un Dockerfile pour reproduire l'environnement."""
        return f"""# Dockerfile généré automatiquement pour LCPI
# Généré le: {datetime.now().isoformat()}

FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Installation des dépendances système
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copier les fichiers d'environnement
COPY environment/requirements.txt .
COPY environment/pyproject.toml .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY project/ .

# Commande par défaut
CMD ["python", "-m", "lcpi", "--help"]
"""
    
    def _generate_pyproject_toml(self) -> str:
        """Génère un pyproject.toml basique."""
        return f"""[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "lcpi-reproducible"
version = "0.1.0"
description = "Projet LCPI reproductible exporté le {datetime.now().isoformat()}"
requires-python = ">=3.9"
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "pyyaml>=6.0",
    "packaging>=23.0"
]

[tool.setuptools]
packages = ["lcpi"]
"""
    
    def _get_lcpi_version(self) -> str:
        """Récupère la version de LCPI."""
        try:
            if PKG_RESOURCES_AVAILABLE:
                lcpi_dist = pkg_resources.get_distribution("lcpi-cli")
                return lcpi_dist.version
        except pkg_resources.DistributionNotFound:
            pass
        
        # Fallback: chercher dans le code
        try:
            from .. import __version__
            return __version__
        except ImportError:
            pass
        
        return "2.1.0"  # Version par défaut
    
    def _calculate_file_checksum(self, file_path: Path) -> str:
        """Calcule le checksum SHA-256 d'un fichier."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()


def export_reproducible(
    project_path: str,
    output_path: str,
    include_logs: bool = True,
    include_results: bool = True,
    include_env: bool = True,
    include_data: bool = True
) -> Dict[str, Any]:
    """
    Fonction de convenance pour exporter un projet de manière reproductible.
    
    Args:
        project_path: Chemin vers le projet LCPI
        output_path: Chemin de sortie pour l'archive
        include_logs: Inclure les logs de calcul
        include_results: Inclure les résultats exportés
        include_env: Inclure l'environnement Python
        include_data: Inclure les données du projet
        
    Returns:
        Informations sur l'export
    """
    exporter = ReproducibleExporter(project_path)
    return exporter.export_reproducible(
        output_path=output_path,
        include_logs=include_logs,
        include_results=include_results,
        include_env=include_env,
        include_data=include_data
    )


if __name__ == "__main__":
    # Test de la fonction
    import tempfile
    import shutil
    
    # Créer un projet de test
    with tempfile.TemporaryDirectory() as temp_dir:
        test_project = Path(temp_dir) / "test_project"
        test_project.mkdir()
        
        # Créer quelques fichiers de test
        (test_project / "data").mkdir()
        (test_project / "logs").mkdir()
        (test_project / "results").mkdir()
        
        (test_project / "data" / "test.csv").write_text("test,data")
        (test_project / "logs" / "test.json").write_text('{"test": "log"}')
        (test_project / "results" / "test.txt").write_text("test result")
        
        # Exporter
        output_file = test_project / "export.tar.gz"
        export_info = export_reproducible(
            project_path=str(test_project),
            output_path=str(output_file),
            include_logs=True,
            include_results=True,
            include_env=True,
            include_data=True
        )
        
        print("Export réussi!")
        print(f"Fichier: {output_file}")
        print(f"Taille: {output_file.stat().st_size} bytes")
        print(f"Fichiers inclus: {len(export_info['files_included'])}")
