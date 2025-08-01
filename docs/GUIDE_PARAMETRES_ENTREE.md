# Guide d'Implémentation - Affichage Automatique des Paramètres d'Entrée

## Vue d'ensemble

Ce guide explique comment implémenter l'affichage automatique des paramètres d'entrée pour toutes les commandes de calcul de LCPI-CLI. Cette fonctionnalité permet aux utilisateurs de voir les paramètres requis en tapant simplement la commande sans arguments.

## Fonctionnalité

Quand un utilisateur tape une commande de calcul sans fournir les paramètres obligatoires, le système affiche automatiquement :
- Les paramètres obligatoires avec leurs descriptions
- Les paramètres optionnels avec leurs valeurs par défaut
- Des exemples d'utilisation
- Une description de la commande

## Exemples d'Utilisation

### Commande Plomberie
```bash
# Affiche les paramètres d'entrée
lcpi hydro plomberie dimensionner

# Exécute le calcul
lcpi hydro plomberie dimensionner --nb-appareils 5 --debits-base 2.5
```

### Commande Réservoir
```bash
# Affiche les paramètres d'entrée
lcpi hydro reservoir equilibrage

# Exécute le calcul
lcpi hydro reservoir equilibrage --demande-journaliere 1000
```

## Implémentation

### 1. Utilisation des Utilitaires

Importez les fonctions utilitaires dans votre commande :

```python
from ..utils.command_helpers import show_input_parameters, create_parameter_dict
```

### 2. Définition des Paramètres

Utilisez `typer.Option(None, ...)` pour les paramètres obligatoires :

```python
@app.command("dimensionner")
def ma_commande(
    param1: float = typer.Option(None, "--param1", "-p", help="Description du paramètre 1"),
    param2: str = typer.Option("valeur_defaut", "--param2", help="Description du paramètre 2")
):
```

### 3. Vérification et Affichage

Ajoutez la logique de vérification au début de la fonction :

```python
# Si aucun paramètre obligatoire n'est fourni, afficher les paramètres d'entrée
if param1 is None:
    required_params = [
        create_parameter_dict("param1", "Description du paramètre 1", "p")
    ]
    
    optional_params = [
        create_parameter_dict("param2", "Description du paramètre 2", default="valeur_defaut")
    ]
    
    examples = [
        "lcpi plugin commande --param1 10.5",
        "lcpi plugin commande -p 10.5 --param2 nouvelle_valeur"
    ]
    
    show_input_parameters(
        "Nom de la Commande",
        required_params,
        optional_params,
        examples,
        "Description de ce que fait la commande."
    )
    return
```

### 4. Fonctions Utilitaires Disponibles

#### `show_input_parameters()`
Affiche un panneau avec tous les paramètres d'entrée.

**Paramètres :**
- `command_name`: Nom de la commande
- `required_params`: Liste des paramètres obligatoires
- `optional_params`: Liste des paramètres optionnels (optionnel)
- `examples`: Exemples d'utilisation (optionnel)
- `description`: Description de la commande (optionnel)

#### `create_parameter_dict()`
Crée un dictionnaire de paramètre standardisé.

**Paramètres :**
- `name`: Nom du paramètre
- `help_text`: Texte d'aide
- `short`: Option courte (ex: 'n' pour --name)
- `default`: Valeur par défaut (optionnel)

#### `check_required_params()`
Vérifie si tous les paramètres requis sont fournis.

#### `create_typer_option()`
Crée une option Typer avec gestion automatique des paramètres requis.

## Exemples Complets

### Exemple 1 : Commande Simple

```python
@app.command("calculer")
def calculer_simple(
    valeur: float = typer.Option(None, "--valeur", "-v", help="Valeur à calculer"),
    precision: int = typer.Option(2, "--precision", "-p", help="Précision du résultat")
):
    """
    Effectue un calcul simple.
    
    Si aucun paramètre n'est fourni, affiche les paramètres d'entrée requis.
    """
    if valeur is None:
        from ..utils.command_helpers import show_input_parameters, create_parameter_dict
        
        required_params = [
            create_parameter_dict("valeur", "Valeur à calculer", "v")
        ]
        
        optional_params = [
            create_parameter_dict("precision", "Précision du résultat", default=2)
        ]
        
        examples = [
            "lcpi plugin calculer --valeur 10.5",
            "lcpi plugin calculer -v 10.5 --precision 3"
        ]
        
        show_input_parameters(
            "Calcul Simple",
            required_params,
            optional_params,
            examples,
            "Effectue un calcul simple avec la valeur fournie."
        )
        return
    
    # Logique de calcul...
    resultat = valeur * 2
    print(f"Résultat : {resultat:.{precision}f}")
```

### Exemple 2 : Commande Complexe

```python
@app.command("dimensionner")
def dimensionner_complexe(
    largeur: float = typer.Option(None, "--largeur", "-l", help="Largeur en mètres"),
    hauteur: float = typer.Option(None, "--hauteur", "-h", help="Hauteur en mètres"),
    materiau: str = typer.Option("beton", "--materiau", "-m", help="Type de matériau"),
    securite: float = typer.Option(1.5, "--securite", "-s", help="Coefficient de sécurité")
):
    """
    Dimensionne un élément structurel.
    
    Si aucun paramètre obligatoire n'est fourni, affiche les paramètres d'entrée requis.
    """
    if largeur is None or hauteur is None:
        from ..utils.command_helpers import show_input_parameters, create_parameter_dict
        
        required_params = [
            create_parameter_dict("largeur", "Largeur en mètres", "l"),
            create_parameter_dict("hauteur", "Hauteur en mètres", "h")
        ]
        
        optional_params = [
            create_parameter_dict("materiau", "Type de matériau", default="beton"),
            create_parameter_dict("securite", "Coefficient de sécurité", default=1.5)
        ]
        
        examples = [
            "lcpi plugin dimensionner --largeur 5.0 --hauteur 3.0",
            "lcpi plugin dimensionner -l 5.0 -h 3.0 --materiau acier --securite 2.0"
        ]
        
        show_input_parameters(
            "Dimensionnement Structurel",
            required_params,
            optional_params,
            examples,
            "Calcule les dimensions optimales d'un élément structurel."
        )
        return
    
    # Logique de dimensionnement...
    surface = largeur * hauteur
    charge = surface * securite
    print(f"Surface : {surface} m², Charge : {charge} kN")
```

## Bonnes Pratiques

### 1. Paramètres Obligatoires
- Utilisez `typer.Option(None, ...)` au lieu de `typer.Argument(..., ...)`
- Vérifiez si les paramètres sont `None` au début de la fonction
- Affichez les paramètres d'entrée si au moins un paramètre obligatoire est manquant

### 2. Documentation
- Incluez une description claire de la commande
- Fournissez des exemples d'utilisation réalistes
- Expliquez les unités et les valeurs typiques

### 3. Paramètres Optionnels
- Définissez des valeurs par défaut appropriées
- Documentez clairement l'impact des paramètres optionnels
- Utilisez des noms de paramètres explicites

### 4. Exemples
- Fournissez au moins 2 exemples d'utilisation
- Incluez des exemples avec et sans paramètres optionnels
- Utilisez des valeurs réalistes dans les exemples

## Migration des Commandes Existantes

Pour migrer une commande existante :

1. **Changer les Arguments en Options :**
   ```python
   # Avant
   def commande(filepath: str = typer.Argument(..., help="..."))
   
   # Après
   def commande(filepath: str = typer.Option(None, "--filepath", help="..."))
   ```

2. **Ajouter la Vérification :**
   ```python
   if filepath is None:
       # Afficher les paramètres d'entrée
       return
   ```

3. **Tester la Commande :**
   ```bash
   lcpi plugin commande  # Doit afficher les paramètres
   lcpi plugin commande --filepath fichier.yml  # Doit fonctionner normalement
   ```

## Avantages

- **UX Améliorée :** Les utilisateurs voient immédiatement les paramètres requis
- **Documentation Intégrée :** Les paramètres sont documentés dans la commande
- **Réduction des Erreurs :** Moins d'erreurs dues à des paramètres manquants
- **Cohérence :** Interface uniforme pour toutes les commandes

## Support

Pour toute question ou problème d'implémentation, consultez :
- Les exemples dans `src/lcpi/hydrodrain/main.py`
- Les utilitaires dans `src/lcpi/utils/command_helpers.py`
- Ce guide de documentation 