#!/usr/bin/env python3
"""
Script de migration pour appliquer automatiquement le décorateur de journalisation
à toutes les commandes LCPI existantes.

Ce script analyse les fichiers de commandes et propose des modifications
pour intégrer la journalisation automatique.
"""

import re
import ast
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import argparse


class CommandAnalyzer:
    """Analyseur de commandes CLI pour détecter les commandes à migrer."""
    
    def __init__(self, src_dir: Path):
        self.src_dir = src_dir
        self.commands_found = []
    
    def find_cli_files(self) -> List[Path]:
        """Trouve tous les fichiers CLI dans le projet."""
        cli_files = []
        
        # Patterns pour les fichiers CLI
        patterns = [
            "**/cli.py",
            "**/main.py", 
            "**/commands/*.py",
            "**/commands/**/*.py"
        ]
        
        for pattern in patterns:
            cli_files.extend(self.src_dir.glob(pattern))
        
        return sorted(cli_files)
    
    def analyze_file(self, file_path: Path) -> List[Dict]:
        """Analyse un fichier pour détecter les commandes CLI."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Erreur lecture {file_path}: {e}")
            return []
        
        commands = []
        
        # Analyser l'AST pour trouver les décorateurs @app.command()
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Vérifier si la fonction a le décorateur @app.command()
                    has_command_decorator = False
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Attribute):
                                if decorator.func.attr == 'command':
                                    has_command_decorator = True
                                    break
                        elif isinstance(decorator, ast.Attribute):
                            if decorator.attr == 'command':
                                has_command_decorator = True
                                break
                    
                    if has_command_decorator:
                        # Déterminer le plugin et la commande
                        plugin_name = self._extract_plugin_name(file_path)
                        command_name = node.name
                        
                        commands.append({
                            'file': file_path,
                            'function_name': command_name,
                            'plugin_name': plugin_name,
                            'line_number': node.lineno,
                            'has_logging': self._check_existing_logging(content, node.lineno)
                        })
        
        except SyntaxError as e:
            print(f"⚠️  Erreur syntaxe {file_path}: {e}")
        
        return commands
    
    def _extract_plugin_name(self, file_path: Path) -> str:
        """Extrait le nom du plugin à partir du chemin du fichier."""
        # Chercher le nom du plugin dans le chemin
        parts = file_path.parts
        for i, part in enumerate(parts):
            if part == 'src' and i + 1 < len(parts):
                if parts[i + 1] == 'lcpi' and i + 2 < len(parts):
                    return parts[i + 2]  # Nom du plugin
        return "unknown"
    
    def _check_existing_logging(self, content: str, line_number: int) -> bool:
        """Vérifie si la commande a déjà une journalisation."""
        lines = content.split('\n')
        if line_number <= len(lines):
            # Vérifier les lignes autour de la fonction
            start_line = max(0, line_number - 5)
            end_line = min(len(lines), line_number + 10)
            
            for i in range(start_line, end_line):
                line = lines[i].strip()
                if any(keyword in line.lower() for keyword in ['log', 'journal', 'logging']):
                    return True
        
        return False
    
    def analyze_all_files(self) -> List[Dict]:
        """Analyse tous les fichiers CLI du projet."""
        cli_files = self.find_cli_files()
        all_commands = []
        
        print(f"🔍 Analyse de {len(cli_files)} fichiers CLI...")
        
        for file_path in cli_files:
            commands = self.analyze_file(file_path)
            all_commands.extend(commands)
            
            if commands:
                print(f"  📁 {file_path.relative_to(self.src_dir)}: {len(commands)} commandes")
        
        return all_commands


class MigrationGenerator:
    """Générateur de migrations pour appliquer le décorateur de journalisation."""
    
    def __init__(self, commands: List[Dict]):
        self.commands = commands
    
    def generate_migration_plan(self) -> str:
        """Génère un plan de migration détaillé."""
        plan = []
        plan.append("# Plan de Migration - Journalisation Automatique LCPI")
        plan.append("")
        plan.append("## 📊 Résumé")
        plan.append(f"- Total commandes détectées: {len(self.commands)}")
        plan.append(f"- Commandes avec journalisation existante: {sum(1 for c in self.commands if c['has_logging'])}")
        plan.append(f"- Commandes à migrer: {sum(1 for c in self.commands if not c['has_logging'])}")
        plan.append("")
        
        # Grouper par plugin
        plugins = {}
        for cmd in self.commands:
            plugin = cmd['plugin_name']
            if plugin not in plugins:
                plugins[plugin] = []
            plugins[plugin].append(cmd)
        
        plan.append("## 🔧 Commandes par Plugin")
        for plugin, cmds in plugins.items():
            plan.append(f"")
            plan.append(f"### {plugin.upper()}")
            for cmd in cmds:
                status = "✅" if cmd['has_logging'] else "❌"
                plan.append(f"- {status} `{cmd['function_name']}` ({cmd['file'].relative_to(Path('src'))})")
        
        plan.append("")
        plan.append("## 📝 Étapes de Migration")
        plan.append("")
        plan.append("### 1. Ajouter l'import")
        plan.append("```python")
        plan.append("from lcpi.core.logging_decorator import logged_command")
        plan.append("```")
        plan.append("")
        
        plan.append("### 2. Appliquer le décorateur")
        plan.append("Pour chaque commande, ajouter le décorateur:")
        plan.append("```python")
        plan.append("@app.command()")
        plan.append("@logged_command('plugin_name', 'command_name', log_by_default=True)")
        plan.append("def your_command(...):")
        plan.append("    ...")
        plan.append("```")
        plan.append("")
        
        plan.append("### 3. Supprimer la journalisation manuelle")
        plan.append("Retirer le code de journalisation existant si présent.")
        plan.append("")
        
        return "\n".join(plan)
    
    def generate_migration_script(self) -> str:
        """Génère un script Python pour appliquer automatiquement les migrations."""
        script = []
        script.append("#!/usr/bin/env python3")
        script.append('"""')
        script.append("Script généré automatiquement pour appliquer la journalisation automatique.")
        script.append('"""')
        script.append("")
        script.append("import re")
        script.append("from pathlib import Path")
        script.append("")
        
        # Générer les modifications pour chaque commande
        for cmd in self.commands:
            if not cmd['has_logging']:
                script.append(f"# Migration: {cmd['function_name']} dans {cmd['file']}")
                script.append(f"def migrate_{cmd['plugin_name']}_{cmd['function_name']}():")
                script.append(f"    file_path = Path('{cmd['file']}')")
                script.append(f"    # TODO: Appliquer la migration")
                script.append(f"    pass")
                script.append("")
        
        script.append("def main():")
        script.append("    print('🚀 Application des migrations de journalisation...')")
        for cmd in self.commands:
            if not cmd['has_logging']:
                script.append(f"    migrate_{cmd['plugin_name']}_{cmd['function_name']}()")
        script.append("    print('✅ Migrations terminées')")
        script.append("")
        script.append("if __name__ == '__main__':")
        script.append("    main()")
        
        return "\n".join(script)


def main():
    parser = argparse.ArgumentParser(description="Migration vers la journalisation automatique LCPI")
    parser.add_argument("--src-dir", default="src", help="Répertoire source (défaut: src)")
    parser.add_argument("--output-plan", help="Fichier de sortie pour le plan de migration")
    parser.add_argument("--output-script", help="Fichier de sortie pour le script de migration")
    parser.add_argument("--dry-run", action="store_true", help="Mode simulation (pas de modification)")
    
    args = parser.parse_args()
    
    src_dir = Path(args.src_dir)
    if not src_dir.exists():
        print(f"❌ Répertoire source non trouvé: {src_dir}")
        return 1
    
    print("🔍 Analyse du projet LCPI pour la migration vers la journalisation automatique...")
    print(f"📁 Répertoire source: {src_dir}")
    print()
    
    # Analyser les commandes
    analyzer = CommandAnalyzer(src_dir)
    commands = analyzer.analyze_all_files()
    
    if not commands:
        print("❌ Aucune commande CLI détectée")
        return 1
    
    print(f"\n📊 Résultats de l'analyse:")
    print(f"  - Commandes détectées: {len(commands)}")
    print(f"  - Avec journalisation existante: {sum(1 for c in commands if c['has_logging'])}")
    print(f"  - À migrer: {sum(1 for c in commands if not c['has_logging'])}")
    
    # Générer le plan de migration
    generator = MigrationGenerator(commands)
    plan = generator.generate_migration_plan()
    
    if args.output_plan:
        with open(args.output_plan, 'w', encoding='utf-8') as f:
            f.write(plan)
        print(f"\n📝 Plan de migration sauvegardé: {args.output_plan}")
    else:
        print("\n" + "="*60)
        print(plan)
        print("="*60)
    
    # Générer le script de migration
    if args.output_script:
        script = generator.generate_migration_script()
        with open(args.output_script, 'w', encoding='utf-8') as f:
            f.write(script)
        print(f"🔧 Script de migration généré: {args.output_script}")
    
    print("\n💡 Prochaines étapes:")
    print("1. Examiner le plan de migration")
    print("2. Appliquer les modifications fichier par fichier")
    print("3. Tester chaque commande migrée")
    print("4. Vérifier la journalisation avec 'lcpi logs list'")
    
    return 0


if __name__ == "__main__":
    exit(main())
