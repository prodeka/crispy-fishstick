

### **Feuille de Route : Implémentation du Gestionnaire de Projets et de Contexte**

**Objectif :** Rendre `lcpi` conscient du "contexte de projet". L'utilisateur ne pourra exécuter des commandes métier que si un projet est actif. L'outil doit gérer une liste de projets connus et permettre à l'utilisateur de basculer facilement entre eux, où qu'il se trouve sur le système de fichiers.

---

#### **Partie 1 : Le Cœur du Système - La Gestion d'État**

Pour que `lcpi` se "souvienne" des projets, il a besoin d'un endroit pour stocker cette information en dehors du projet lui-même.

**Tâche 1.1 : Créer un Fichier de Configuration Global**

*   **Action :** `lcpi` doit gérer un fichier de configuration centralisé, stocké dans le répertoire personnel de l'utilisateur. C'est la pratique standard.
    *   Sur Windows : `C:\Users\<Utilisateur>\.lcpi\config.json`
    *   Sur Linux/macOS : `/home/<Utilisateur>/.lcpi/config.json`
*   **Contenu de `config.json` :**
    ```json
    {
      "projets_connus": {
        "Projet Village Mboula": "G:\\Mon Drive\\Other\\PROJET_DIMENTIONEMENT_2",
        "Etude Pont Riviere Zio": "D:\\Etudes\\Pont_Zio"
      },
      "projet_actif": "Projet Village Mboula",
      "sandbox_path": "C:\\Users\\<Utilisateur>\\.lcpi\\sandbox"
    }
    ```
*   **Implémentation :** Créez un module `lcpi/config/global_manager.py` avec des fonctions pour lire et écrire dans ce fichier.

---

#### **Partie 2 : La Gestion des Projets - Le Nouveau Module `project`**

Vous avez besoin d'un nouveau groupe de commandes pour gérer ce contexte.

**Tâche 2.1 : Créer le groupe de commandes `lcpi project`**

*   **Action :** Créez un nouveau fichier `lcpi/project_cli.py` et ajoutez-le à votre application principale.

*   **Commande `lcpi project init <nom_du_projet>` (Modification de l'existant)**
    *   **Action :** Au lieu de `lcpi <nom>`, on passe à `lcpi project init <nom>`.
    *   **Logique améliorée :**
        1.  Crée l'arborescence du projet dans le répertoire *actuel*.
        2.  Récupère le chemin absolu du projet nouvellement créé.
        3.  **Ajoute une entrée** au fichier `config.json` : ` "nom_du_projet": "/chemin/absolu/vers/le/projet" `.
        4.  Définit automatiquement ce nouveau projet comme le **projet actif**.
        5.  Affiche un message de succès : `✅ Projet 'nom_du_projet' créé et activé.`

*   **Commande `lcpi project list`**
    *   **Action :** Affiche la liste des projets connus.
    *   **Logique :**
        1.  Lit la section `projets_connus` de `config.json`.
        2.  Utilise une table `Rich` pour afficher les projets. Le projet actif doit être mis en évidence.
    *   **Sortie Attendue :**
        ```
        ╭───────── Projets LCPI Connus ──────────╮
        │ NOM DU PROJET                CHEMIN    │
        ├────────────────────────────────────────┤
        │ * Projet Village Mboula      G:\...\...│  <-- L'astérisque indique le projet actif
        │   Etude Pont Riviere Zio     D:\...\...│
        ╰────────────────────────────────────────╯
        ```

*   **Commande `lcpi project switch` (ou `use`)**
    *   **Action :** Permet de changer de projet actif.
    *   **Logique :**
        1.  Si aucun nom n'est fourni, la commande devient **interactive**. Elle affiche la liste des projets avec des numéros et demande à l'utilisateur de choisir.
        2.  Si un nom est fourni (`lcpi project switch "Projet Village Mboula"`), elle le définit comme `projet_actif` dans `config.json`.
        3.  Affiche un message de confirmation : `✅ Projet 'Projet Village Mboula' est maintenant actif.`

---

#### **Partie 3 : L'Intégration du Contexte dans les Commandes Métier**

C'est le point le plus important : forcer l'utilisation d'un contexte.

**Tâche 3.1 : Créer un "Décorateur de Contexte"**

*   **Action :** Pour éviter de répéter le code de vérification dans chaque commande, créez un décorateur Python. C'est une technique avancée et très propre.
*   **Implémentation dans `lcpi/core/context.py` :**
    ```python
    import functools
    from .global_config import get_active_project, set_active_project
    
    def require_project_context(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            active_project = get_active_project()
            if active_project:
                console.print(f" contexte: [bold cyan]{active_project['name']}[/bold cyan] ")
                # On injecte le chemin du projet dans les arguments de la fonction
                kwargs['project_path'] = active_project['path']
                return func(*args, **kwargs)
            else:
                # Logique du Sandbox
                handle_sandbox_logic()
                kwargs['project_path'] = get_sandbox_path()
                return func(*args, **kwargs)
        return wrapper
    ```
*   **Utilisation :** Vous n'aurez qu'à ajouter `@require_project_context` au-dessus de chaque commande métier.

**Tâche 3.2 : Modifier les Commandes Métier**

*   **Action :** Appliquez le décorateur à toutes vos commandes métier.
*   **Exemple dans `lcpi/aep/cli.py` :**
    ```python
    from lcpi.core.context import require_project_context

    @app.command()
    @require_project_context
    def population_unified(project_path: Path, ...): # Le chemin est maintenant injecté
        # Le reste de votre code
        # Il peut maintenant utiliser project_path pour trouver les logs, data, etc.
        log_path = project_path / "logs"
        # ...
    ```

---

#### **Partie 4 : La Gestion du "Sandbox"**

Votre idée de "sandbox" est excellente pour permettre des tests rapides sans polluer un vrai projet.

**Tâche 4.1 : Implémenter la Logique du Sandbox**

*   **Action :** Créez la fonction `handle_sandbox_logic()` utilisée par le décorateur.
*   **Logique :**
    1.  Vérifie une variable de session (ou un petit fichier temporaire) pour voir si le sandbox a déjà été activé dans le terminal actuel.
    2.  Si ce n'est pas le cas :
        *   Affiche un message : `Aucun projet n'est actif.`
        *   Pose la question : `Voulez-vous exécuter cette commande dans l'environnement d'expérimentation (sandbox) ?`
        *   Si l'utilisateur accepte, active le sandbox pour la session.
        *   Si l'utilisateur refuse, `raise typer.Abort()`.
    3.  Si le sandbox est déjà actif dans la session :
        *   Affiche simplement le message de contexte : ` contexte: [bold yellow]sandbox[/bold yellow] `

**Tâche 4.2 : Gérer le Nettoyage du Sandbox**

*   **Action :** L'idée de demander à la fermeture du terminal est techniquement très difficile. Une approche plus simple et plus robuste est de gérer cela avec une commande explicite.
*   **Commande `lcpi project sandbox --clean`**
    *   Pose la question : `Voulez-vous supprimer tout le contenu du sandbox (logs, données) ? Cette action est irréversible.`
    *   Si l'utilisateur confirme, vide le dossier `sandbox/`.
*   **Amélioration :** À la première activation du sandbox dans une session, affichez un message : `💡 Conseil : Le contenu du sandbox est persistant. Utilisez 'lcpi project sandbox --clean' pour le nettoyer.`

---

### **Améliorations Supplémentaires que je vous Propose**

1.  **`lcpi project cd` : La Navigation Intelligente**
    *   Une commande "magique" qui vous téléporte directement dans le dossier du projet actif.
    *   `lcpi project cd` -> change le répertoire courant de PowerShell vers `G:\Mon Drive\Other\PROJET_DIMENTIONEMENT_2`.
    *   C'est une fonctionnalité très appréciée dans les outils comme `conda`.

2.  **`lcpi project archive <nom_du_projet>`**
    *   Crée une archive zip de tout le dossier du projet (données, logs, rapports) avec un nom standardisé (ex: `Projet_Mboula_2025-08-16.zip`).
    *   Très utile pour la livraison finale d'un projet ou l'archivage.

3.  **Alias de Commandes**
    *   Ajoutez des alias courts pour les commandes les plus fréquentes : `lcpi p ls` (pour `project list`), `lcpi p use` (pour `project switch`). Cela rend l'outil encore plus rapide à utiliser.

Cette nouvelle couche de "gestion de projet" va considérablement augmenter la qualité et l'ergonomie de votre outil `lcpi`. C'est une direction de développement très pertinente.