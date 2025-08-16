"""
Intégration Git pour les projets LCPI.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class GitIntegration:
    """Gestionnaire d'intégration Git pour les projets LCPI."""
    
    def __init__(self, project_dir: Path):
        """
        Initialise l'intégration Git.
        
        Args:
            project_dir: Chemin vers le dossier du projet
        """
        self.project_dir = Path(project_dir)
        self.git_dir = self.project_dir / ".git"
    
    def is_git_repository(self) -> bool:
        """Vérifie si le projet est un dépôt Git."""
        return self.git_dir.exists() and self.git_dir.is_dir()
    
    def init_git_repository(self, initial_commit: bool = True) -> bool:
        """
        Initialise un nouveau dépôt Git.
        
        Args:
            initial_commit: Si True, crée un commit initial
        
        Returns:
            True si l'initialisation a réussi
        """
        try:
            if self.is_git_repository():
                logger.info("Le projet est déjà un dépôt Git")
                return True
            
            # Initialiser le dépôt Git
            result = subprocess.run(
                ["git", "init"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info("Dépôt Git initialisé avec succès")
            
            # Créer le fichier .gitignore
            self._create_gitignore()
            
            # Ajouter tous les fichiers
            subprocess.run(
                ["git", "add", "."],
                cwd=self.project_dir,
                check=True
            )
            
            if initial_commit:
                # Créer le commit initial
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit - Projet LCPI"],
                    cwd=self.project_dir,
                    check=True
                )
                logger.info("Commit initial créé")
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erreur lors de l'initialisation Git: {e}")
            return False
        except Exception as e:
            logger.error(f"Erreur inattendue: {e}")
            return False
    
    def _create_gitignore(self) -> None:
        """Crée un fichier .gitignore approprié pour LCPI."""
        gitignore_content = """# LCPI Project .gitignore

# Fichiers de base de données
*.db
*.sqlite
*.sqlite3

# Fichiers temporaires
temp/
tmp/
*.tmp
*.temp

# Fichiers de sortie
outputs/
reports/
*.pdf
*.docx
*.html

# Logs
logs/
*.log

# Cache Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environnements virtuels
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Fichiers de données sensibles
*.key
*.pem
*.p12
*.pfx
secrets.yml
config.local.yml

# Fichiers de sauvegarde
*.bak
*.backup
*.old
"""
        
        gitignore_path = self.project_dir / ".gitignore"
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        logger.info("Fichier .gitignore créé")
    
    def add_files(self, files: List[str]) -> bool:
        """
        Ajoute des fichiers au staging area.
        
        Args:
            files: Liste des fichiers à ajouter
        
        Returns:
            True si l'ajout a réussi
        """
        try:
            for file_path in files:
                full_path = self.project_dir / file_path
                if full_path.exists():
                    subprocess.run(
                        ["git", "add", str(file_path)],
                        cwd=self.project_dir,
                        check=True
                    )
                    logger.info(f"Fichier ajouté: {file_path}")
                else:
                    logger.warning(f"Fichier non trouvé: {file_path}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erreur lors de l'ajout des fichiers: {e}")
            return False
    
    def commit_changes(self, message: str, author: str = None) -> bool:
        """
        Crée un commit avec les changements.
        
        Args:
            message: Message du commit
            author: Auteur du commit (optionnel)
        
        Returns:
            True si le commit a réussi
        """
        try:
            # Configurer l'auteur si spécifié
            if author:
                subprocess.run(
                    ["git", "config", "user.name", author],
                    cwd=self.project_dir,
                    check=True
                )
            
            # Créer le commit
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.project_dir,
                check=True
            )
            
            logger.info(f"Commit créé: {message}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erreur lors de la création du commit: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Récupère le statut du dépôt Git.
        
        Returns:
            Dictionnaire avec le statut Git
        """
        if not self.is_git_repository():
            return {"is_git": False}
        
        try:
            # Statut des fichiers
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Branche actuelle
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Dernier commit
            last_commit_result = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%H|%an|%ad|%s"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Analyser le statut
            status_lines = status_result.stdout.strip().split('\n') if status_result.stdout.strip() else []
            staged_files = []
            unstaged_files = []
            untracked_files = []
            
            for line in status_lines:
                if line.startswith('M ') or line.startswith('A '):
                    staged_files.append(line[3:])
                elif line.startswith(' M') or line.startswith(' D'):
                    unstaged_files.append(line[3:])
                elif line.startswith('??'):
                    untracked_files.append(line[3:])
            
            # Analyser le dernier commit
            last_commit_info = {}
            if last_commit_result.stdout.strip():
                parts = last_commit_result.stdout.strip().split('|')
                if len(parts) == 4:
                    last_commit_info = {
                        "hash": parts[0],
                        "author": parts[1],
                        "date": parts[2],
                        "message": parts[3]
                    }
            
            return {
                "is_git": True,
                "branch": branch_result.stdout.strip(),
                "staged_files": staged_files,
                "unstaged_files": unstaged_files,
                "untracked_files": untracked_files,
                "last_commit": last_commit_info
            }
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erreur lors de la récupération du statut: {e}")
            return {"is_git": True, "error": str(e)}
    
    def create_branch(self, branch_name: str, checkout: bool = True) -> bool:
        """
        Crée une nouvelle branche.
        
        Args:
            branch_name: Nom de la nouvelle branche
            checkout: Si True, bascule sur la nouvelle branche
        
        Returns:
            True si la création a réussi
        """
        try:
            if checkout:
                subprocess.run(
                    ["git", "checkout", "-b", branch_name],
                    cwd=self.project_dir,
                    check=True
                )
            else:
                subprocess.run(
                    ["git", "branch", branch_name],
                    cwd=self.project_dir,
                    check=True
                )
            
            logger.info(f"Branche créée: {branch_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erreur lors de la création de la branche: {e}")
            return False
    
    def add_remote(self, name: str, url: str) -> bool:
        """
        Ajoute un remote au dépôt.
        
        Args:
            name: Nom du remote (ex: "origin")
            url: URL du remote
        
        Returns:
            True si l'ajout a réussi
        """
        try:
            subprocess.run(
                ["git", "remote", "add", name, url],
                cwd=self.project_dir,
                check=True
            )
            
            logger.info(f"Remote ajouté: {name} -> {url}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erreur lors de l'ajout du remote: {e}")
            return False
    
    def push_to_remote(self, remote: str = "origin", branch: str = None) -> bool:
        """
        Pousse les changements vers le remote.
        
        Args:
            remote: Nom du remote
            branch: Nom de la branche (utilise la branche actuelle si None)
        
        Returns:
            True si le push a réussi
        """
        try:
            if branch is None:
                # Utiliser la branche actuelle
                branch_result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=self.project_dir,
                    capture_output=True,
                    text=True,
                    check=True
                )
                branch = branch_result.stdout.strip()
            
            subprocess.run(
                ["git", "push", remote, branch],
                cwd=self.project_dir,
                check=True
            )
            
            logger.info(f"Changements poussés vers {remote}/{branch}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Erreur lors du push: {e}")
            return False

def setup_git_for_project(project_dir: Path, 
                         initial_commit: bool = True,
                         add_remote: bool = False,
                         remote_url: str = None) -> bool:
    """
    Configure Git pour un projet LCPI.
    
    Args:
        project_dir: Chemin vers le dossier du projet
        initial_commit: Si True, crée un commit initial
        add_remote: Si True, ajoute un remote
        remote_url: URL du remote à ajouter
    
    Returns:
        True si la configuration a réussi
    """
    git_integration = GitIntegration(project_dir)
    
    # Initialiser le dépôt Git
    if not git_integration.init_git_repository(initial_commit):
        return False
    
    # Ajouter un remote si demandé
    if add_remote and remote_url:
        if not git_integration.add_remote("origin", remote_url):
            logger.warning("Impossible d'ajouter le remote, mais le dépôt Git est initialisé")
    
    return True
