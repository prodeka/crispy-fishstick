# Fichier: main.py (Version Finale Ultime avec tous les modes)

# -*- coding: utf-8 -*-
import click
import pandas as pd

# --- Importations des modules de calcul ---
from nanostruct.modules.bois.calculs.charges import calculer_sollicitations_completes
from nanostruct.modules.bois.calculs.acier import trouver_profil_acier
from nanostruct.modules.bois.calculs.bois import verifier_section_bois, verifier_traction_bois

# --- FONCTION UTILITAIRE POUR LA SAISIE DES CHARGES (MODE INTERACTIF) ---
def saisir_charges_flexion(verbose_mode):
    """Demande à l'utilisateur toutes les charges pour un cas de flexion."""
    longueur = click.prompt("  -> Longueur de la poutre (en metres)", type=float)
    click.echo(click.style("\nEntrez les charges REPARTIES (en kN/m) :", fg="yellow"))
    charge_g_repartie = click.prompt("  -> Charge permanente G (plancher, etc.)", type=float, default=0.0)
    charge_q_repartie = click.prompt("  -> Charge d'exploitation Q", type=float, default=0.0)
    charge_w = click.prompt("  -> Charge du vent W", type=float, default=0.0)
    charge_s = click.prompt("  -> Charge de neige S", type=float, default=0.0)
    click.echo(click.style("\nEntrez les charges PONCTUELLES au milieu (en kN) :", fg="yellow"))
    charge_g_ponctuelle = click.prompt("  -> Charge permanente G (cloison, poteau...)", type=float, default=0.0)
    charge_q_ponctuelle = click.prompt("  -> Charge d'exploitation Q", type=float, default=0.0)
    
    g_equiv_ponctuelle = (2 * charge_g_ponctuelle) / longueur if longueur > 0 else 0
    q_equiv_ponctuelle = (2 * charge_q_ponctuelle) / longueur if longueur > 0 else 0
    g_total = charge_g_repartie + g_equiv_ponctuelle
    q_total = charge_q_repartie + q_equiv_ponctuelle
    
    if verbose_mode and (g_equiv_ponctuelle > 0 or q_equiv_ponctuelle > 0):
        click.echo(click.style("\nNOTE: Charges ponctuelles converties en charges reparties equivalentes:", fg="blue"))
        click.echo(f"  - G total = {g_total:.2f} kN/m, Q total = {q_total:.2f} kN/m")

    charges_finales = {'G': g_total, 'Q': q_total, 'W': charge_w, 'S': charge_s}
    return charges_finales, longueur

# --- SOUS-PROGRAMMES POUR LE MODE INTERACTIF ---

def run_acier_mode(verbose_mode):
    """Gère le dialogue interactif pour une poutre en acier."""
    click.echo(click.style("\n--- Dimensionnement Acier en FLEXION ---", fg="cyan"))
    charges_entrees, longueur = saisir_charges_flexion(verbose_mode)
    if verbose_mode:
        click.echo(click.style("\nEntrez les parametres du materiau :", fg="yellow"))
    nuance = click.prompt("  -> Nuance de l'acier", default="S235", show_default=verbose_mode)
    fy = click.prompt(f"  -> Limite d'elasticite (fy) de '{nuance}' en MPa", default=235, type=float, show_default=verbose_mode)
    E_module = click.prompt("  -> Module d'Young (E) en MPa", default=210000, type=float, show_default=verbose_mode)
    if verbose_mode:
        click.echo("\n... Lancement des calculs ...")
    sollicitations = calculer_sollicitations_completes(longueur, charges_entrees, 'acier', 'A', verbose=verbose_mode)
    profil_recommande = trouver_profil_acier(
        sollicitations['M_Ed'], sollicitations['V_Ed'], longueur, sollicitations['p_ser'],
        nuance=nuance, fy_MPa=fy, E_MPa=E_module, verbose=verbose_mode
    )
    click.echo("\n----------------------------------------------------")
    click.echo(click.style("✅ RESULTAT DU DIMENSIONNEMENT", fg="green", bold=True))
    click.echo(click.style(f"Le profile IPE recommande est : {profil_recommande}", fg="green"))
    click.echo("----------------------------------------------------")

def run_bois_flexion(verbose_mode):
    """Gère le dialogue interactif pour une poutre en bois en flexion."""
    click.echo(click.style("\n--- Vérification d'une Poutre en FLEXION ---", fg="cyan"))
    charges_entrees, longueur = saisir_charges_flexion(verbose_mode)
    click.echo(click.style("\nEntrez les parametres du bois (Eurocode 5) :", fg="yellow"))
    classe_bois = click.prompt("  -> Classe du bois (ex: C24, D30, GL24h)", default="C24")
    classe_service = click.prompt("  -> Classe de service", type=click.Choice(['classe_1', 'classe_2', 'classe_3']), default='classe_1')
    duree_charge = click.prompt("  -> Duree de la charge", type=click.Choice(['permanente', 'long_terme', 'moyen_terme', 'court_terme']), default='permanente')
    if verbose_mode:
        click.echo("\n... Lancement du premier calcul de sollicitations ...")
    sollicitations = calculer_sollicitations_completes(longueur, charges_entrees, 'bois', 'A', verbose=verbose_mode)
    while True:
        click.echo(click.style("\nEntrez les dimensions de la section a verifier :", fg="yellow"))
        b = click.prompt("  -> Largeur 'b' de la section (en mm)", type=int)
        h = click.prompt("  -> Hauteur 'h' de la section (en mm)", type=int)
        message, est_valide = verifier_section_bois(
            b, h, longueur, sollicitations, classe_bois, classe_service, duree_charge, verbose=verbose_mode
        )
        click.echo("\n----------------------------------------------------")
        if est_valide:
            click.echo(click.style(f"✅ RESULTAT: {message} La section {b}x{h} est ADEQUATE.", fg="green", bold=True))
            if not click.confirm("Voulez-vous verifier une autre section ?"):
                break
        else:
            click.echo(click.style(f"❌ RESULTAT: {message} La section {b}x{h} n'est PAS adequate.", fg="red", bold=True))
            if not click.confirm("Voulez-vous essayer une autre section ?"):
                break
        click.echo("----------------------------------------------------")

def run_bois_traction(verbose_mode):
    """Gère le dialogue interactif pour une barre en bois en traction."""
    click.echo(click.style("\n--- Vérification d'une Barre en TRACTION ---", fg="cyan"))
    effort_N_daN = click.prompt("  -> Effort de traction N (en daN)", type=float)
    click.echo(click.style("\nEntrez les dimensions de la section a verifier :", fg="yellow"))
    b = click.prompt("  -> Largeur 'b' de la section (en mm)", type=int)
    h = click.prompt("  -> Hauteur 'h' de la section (en mm)", type=int)
    click.echo(click.style("\nEntrez les parametres du bois (Eurocode 5) :", fg="yellow"))
    classe_bois = click.prompt("  -> Classe du bois (ex: D40, C24)", default="D40")
    classe_service = click.prompt("  -> Classe de service", type=click.Choice(['classe_1', 'classe_2', 'classe_3']), default='classe_3')
    duree_charge = click.prompt("  -> Duree de la charge", type=click.Choice(['permanente', 'long_terme', 'moyen_terme', 'court_terme']), default='moyen_terme')
    if verbose_mode:
        click.echo("\n... Lancement de la verification ...")
    message, est_valide = verifier_traction_bois(
        b, h, effort_N_daN, classe_bois, classe_service, duree_charge, verbose=verbose_mode
    )
    click.echo("\n----------------------------------------------------")
    if est_valide:
        click.echo(click.style(f"✅ RESULTAT: {message}", fg="green", bold=True))
    else:
        click.echo(click.style(f"❌ RESULTAT: {message}", fg="red", bold=True))
    click.echo("----------------------------------------------------")

# --- SOUS-PROGRAMME POUR LE MODE BATCH ---
def run_batch_mode(filepath, verbose_mode):
    """Lance le programme en lisant un fichier CSV (pour l'acier)."""
    click.echo(click.style(f"\nLancement du Traitement par Lots sur le fichier: {filepath}", fg="cyan", bold=True))
    try:
        df_entree = pd.read_csv(filepath)
        click.echo("Fichier d'entree lu avec succes.")
    except FileNotFoundError:
        click.echo(click.style(f"Erreur: Le fichier '{filepath}' n'a pas ete trouve.", fg="red"))
        return
    liste_resultats = []
    for index, poutre in df_entree.iterrows():
        click.echo(f"\n--- Calcul pour la poutre: {poutre['id_poutre']} ---")
        est_en_mode_detail = (index == 0) and verbose_mode
        charges = {'G': poutre.get('charge_G', 0), 'Q': poutre.get('charge_Q', 0), 'W': poutre.get('charge_W', 0), 'S': poutre.get('charge_S', 0)}
        sollicitations = calculer_sollicitations_completes(
            poutre['longueur'], charges, 'acier', 'A', verbose=est_en_mode_detail
        )
        profil_recommande = trouver_profil_acier(
            sollicitations['M_Ed'], sollicitations['V_Ed'], poutre['longueur'], sollicitations['p_ser'],
            nuance=poutre['nuance_acier'], fy_MPa=poutre['fy_MPa'], E_MPa=poutre['E_MPa'],
            verbose=est_en_mode_detail
        )
        resultat_ligne = poutre.to_dict()
        resultat_ligne['profil_recommande'] = profil_recommande
        liste_resultats.append(resultat_ligne)
    df_resultats = pd.DataFrame(liste_resultats)
    click.echo("\n\n" + "="*50)
    click.echo(click.style("✅ TRAITEMENT PAR LOTS TERMINE", fg="green", bold=True))
    click.echo("="*50 + "\nTableau recapitulatif des resultats :")
    click.echo(df_resultats.to_string(index=False))
    fichier_sortie = "resultats_batch.csv"
    df_resultats.to_csv(fichier_sortie, index=False, sep=';')
    click.echo(click.style(f"\nLes resultats ont ete enregistres dans le fichier: {fichier_sortie}", fg="yellow"))

# --- Le Chef d'Orchestre (Point d'entrée principal) ---
@click.command()
@click.option('--fichier', '-f', default=None, help="Chemin vers le fichier CSV pour le traitement par lots.")
@click.option('--silencieux', is_flag=True, help="N'affiche pas les etapes de calcul detaillees.")
def main(fichier, silencieux):
    """Outil de dimensionnement de poutres en Acier et Bois."""
    verbose_mode = not silencieux
    if fichier:
        run_batch_mode(fichier, verbose_mode)
    else:
        click.echo(click.style("\nBienvenue dans PyStruct, l'assistant de dimensionnement.", fg="blue", bold=True))
        texte_menu_mat = "\nVeuillez choisir le materiau:\n  [1] Bois\n  [2] Acier\n"
        choix_mat = click.prompt(texte_menu_mat, type=int)
        if choix_mat == 1:
            texte_menu_bois = "\nQuel type de sollicitation pour le bois ?\n  [1] Flexion (poutre)\n  [2] Traction (barre de treillis)\n"
            choix_sol = click.prompt(texte_menu_bois, type=int)
            if choix_sol == 1:
                run_bois_flexion(verbose_mode)
            elif choix_sol == 2:
                run_bois_traction(verbose_mode)
            else:
                click.echo("Choix invalide.")
        elif choix_mat == 2:
            run_acier_mode(verbose_mode)
        else:
            click.echo("Choix invalide.")

if __name__ == '__main__':
    main()