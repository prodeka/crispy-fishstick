"""
Interface graphique pour la gestion des constantes dynamiques AEP

Interface Tkinter simple pour ajouter, valider et rechercher
les constantes locales sans connaissances techniques.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional
import json
import os
from pathlib import Path

from .dynamic_constants import (
    AEPDynamicConstantsManager, 
    StatutElement, 
    ModeImport,
    ReferenceLocale,
    DotationLocale,
    CoefficientLocal
)

class ConstantsGUI:
    """Interface graphique pour la gestion des constantes"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.manager = AEPDynamicConstantsManager(config_dir)
        
        # Créer la fenêtre principale
        self.root = tk.Tk()
        self.root.title("Gestionnaire de Constantes AEP")
        self.root.geometry("800x600")
        
        # Variables pour les champs
        self.nom_var = tk.StringVar()
        self.valeur_var = tk.StringVar()
        self.unite_var = tk.StringVar()
        self.source_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.type_element_var = tk.StringVar(value="reference")
        self.utilisateur_var = tk.StringVar(value="utilisateur")
        
        self._creer_interface()
        self._charger_donnees()
    
    def _creer_interface(self):
        """Crée l'interface utilisateur"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Titre
        titre = ttk.Label(main_frame, text="Gestionnaire de Constantes AEP", 
                         font=("Arial", 16, "bold"))
        titre.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame pour l'ajout d'éléments
        self._creer_frame_ajout(main_frame)
        
        # Frame pour la recherche
        self._creer_frame_recherche(main_frame)
        
        # Frame pour l'affichage
        self._creer_frame_affichage(main_frame)
        
        # Frame pour les actions
        self._creer_frame_actions(main_frame)
    
    def _creer_frame_ajout(self, parent):
        """Crée le frame pour l'ajout d'éléments"""
        frame_ajout = ttk.LabelFrame(parent, text="Ajouter un élément", padding="10")
        frame_ajout.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Type d'élément
        ttk.Label(frame_ajout, text="Type:").grid(row=0, column=0, sticky=tk.W)
        type_combo = ttk.Combobox(frame_ajout, textvariable=self.type_element_var, 
                                 values=["reference", "dotation", "coefficient"], 
                                 state="readonly", width=15)
        type_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Nom
        ttk.Label(frame_ajout, text="Nom:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        ttk.Entry(frame_ajout, textvariable=self.nom_var, width=30).grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 0))
        
        # Valeur
        ttk.Label(frame_ajout, text="Valeur:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        ttk.Entry(frame_ajout, textvariable=self.valeur_var, width=30).grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 0))
        
        # Unité
        ttk.Label(frame_ajout, text="Unité:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        unite_combo = ttk.Combobox(frame_ajout, textvariable=self.unite_var, 
                                  values=["m", "m³", "L", "m³/h", "L/s", "bar", "Pa", "kW", "W", ""], 
                                  width=15)
        unite_combo.grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 0))
        
        # Source
        ttk.Label(frame_ajout, text="Source:").grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
        ttk.Entry(frame_ajout, textvariable=self.source_var, width=30).grid(row=4, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 0))
        
        # Description
        ttk.Label(frame_ajout, text="Description:").grid(row=5, column=0, sticky=tk.W, pady=(10, 0))
        description_text = tk.Text(frame_ajout, height=3, width=40)
        description_text.grid(row=5, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 0))
        self.description_text = description_text
        
        # Utilisateur
        ttk.Label(frame_ajout, text="Utilisateur:").grid(row=6, column=0, sticky=tk.W, pady=(10, 0))
        ttk.Entry(frame_ajout, textvariable=self.utilisateur_var, width=20).grid(row=6, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 0))
        
        # Bouton d'ajout
        btn_ajouter = ttk.Button(frame_ajout, text="Ajouter", command=self._ajouter_element)
        btn_ajouter.grid(row=7, column=1, sticky=tk.W, pady=(10, 0))
    
    def _creer_frame_recherche(self, parent):
        """Crée le frame pour la recherche"""
        frame_recherche = ttk.LabelFrame(parent, text="Rechercher", padding="10")
        frame_recherche.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Terme de recherche
        self.terme_recherche_var = tk.StringVar()
        ttk.Label(frame_recherche, text="Terme:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame_recherche, textvariable=self.terme_recherche_var, width=30).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Bouton de recherche
        btn_rechercher = ttk.Button(frame_recherche, text="Rechercher", command=self._rechercher)
        btn_rechercher.grid(row=0, column=2, padx=(10, 0))
        
        # Bouton tout afficher
        btn_tout = ttk.Button(frame_recherche, text="Tout afficher", command=self._afficher_tout)
        btn_tout.grid(row=0, column=3, padx=(10, 0))
    
    def _creer_frame_affichage(self, parent):
        """Crée le frame pour l'affichage des résultats"""
        frame_affichage = ttk.LabelFrame(parent, text="Résultats", padding="10")
        frame_affichage.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        frame_affichage.columnconfigure(0, weight=1)
        frame_affichage.rowconfigure(0, weight=1)
        
        # Treeview pour afficher les résultats
        columns = ("Nom", "Valeur", "Unité", "Source", "Statut", "Utilisateur")
        self.tree = ttk.Treeview(frame_affichage, columns=columns, show="headings", height=15)
        
        # Configurer les colonnes
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_affichage, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Placement
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Binding pour double-clic
        self.tree.bind("<Double-1>", self._afficher_details)
    
    def _creer_frame_actions(self, parent):
        """Crée le frame pour les actions"""
        frame_actions = ttk.Frame(parent)
        frame_actions.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        # Boutons d'action
        btn_valider = ttk.Button(frame_actions, text="Valider sélectionné", command=self._valider_selectionne)
        btn_valider.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_deprecie = ttk.Button(frame_actions, text="Déprécier sélectionné", command=self._deprecie_selectionne)
        btn_deprecie.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_export = ttk.Button(frame_actions, text="Exporter", command=self._exporter)
        btn_export.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_import = ttk.Button(frame_actions, text="Importer", command=self._importer)
        btn_import.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_stats = ttk.Button(frame_actions, text="Statistiques", command=self._afficher_stats)
        btn_stats.pack(side=tk.LEFT, padx=(0, 10))
    
    def _ajouter_element(self):
        """Ajoute un nouvel élément"""
        try:
            nom = self.nom_var.get().strip()
            valeur_str = self.valeur_var.get().strip()
            unite = self.unite_var.get().strip()
            source = self.source_var.get().strip()
            description = self.description_text.get("1.0", tk.END).strip()
            type_element = self.type_element_var.get()
            utilisateur = self.utilisateur_var.get().strip()
            
            # Validation
            if not nom or not valeur_str or not source:
                messagebox.showerror("Erreur", "Nom, valeur et source sont obligatoires")
                return
            
            # Conversion de la valeur
            try:
                if "." in valeur_str:
                    valeur = float(valeur_str)
                else:
                    valeur = int(valeur_str)
            except ValueError:
                messagebox.showerror("Erreur", "La valeur doit être un nombre")
                return
            
            # Ajout selon le type
            if type_element == "reference":
                success = self.manager.ajouter_reference_locale(
                    nom, valeur, unite, source, description, utilisateur
                )
            elif type_element == "dotation":
                success = self.manager.ajouter_dotation_locale(
                    nom, valeur, unite, "zone_standard", source, description
                )
            elif type_element == "coefficient":
                success = self.manager.ajouter_coefficient_local(
                    nom, valeur, unite, "calcul_standard", source, description
                )
            
            if success:
                messagebox.showinfo("Succès", f"{type_element.capitalize()} ajouté avec succès")
                self._vider_champs()
                self._charger_donnees()
            else:
                messagebox.showerror("Erreur", f"Impossible d'ajouter le {type_element}")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")
    
    def _vider_champs(self):
        """Vide les champs de saisie"""
        self.nom_var.set("")
        self.valeur_var.set("")
        self.unite_var.set("")
        self.source_var.set("")
        self.description_text.delete("1.0", tk.END)
    
    def _charger_donnees(self):
        """Charge les données dans le treeview"""
        # Vider le treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Charger les références
        for nom, ref in self.manager.references_locales.items():
            self.tree.insert("", tk.END, values=(
                nom, ref.valeur, ref.unite, ref.source, ref.statut, ref.validateur
            ), tags=("reference",))
        
        # Charger les dotations
        for nom, dot in self.manager.dotations_locales.items():
            self.tree.insert("", tk.END, values=(
                nom, dot.valeur, dot.unite, dot.source, dot.statut, "N/A"
            ), tags=("dotation",))
        
        # Charger les coefficients
        for nom, coeff in self.manager.coefficients_locaux.items():
            self.tree.insert("", tk.END, values=(
                nom, coeff.valeur, coeff.unite, coeff.source, coeff.statut, "N/A"
            ), tags=("coefficient",))
    
    def _rechercher(self):
        """Effectue une recherche"""
        terme = self.terme_recherche_var.get().strip()
        if not terme:
            self._charger_donnees()
            return
        
        # Vider le treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Rechercher dans les références
        resultats_ref = self.manager.rechercher_references(terme)
        for ref in resultats_ref:
            self.tree.insert("", tk.END, values=(
                ref.nom, ref.valeur, ref.unite, ref.source, ref.statut, ref.validateur
            ), tags=("reference",))
        
        # Rechercher dans les dotations
        resultats_dot = self.manager.rechercher_dotations(terme)
        for dot in resultats_dot:
            self.tree.insert("", tk.END, values=(
                dot.nom, dot.valeur, dot.unite, dot.source, dot.statut, "N/A"
            ), tags=("dotation",))
        
        # Rechercher dans les coefficients
        resultats_coeff = self.manager.rechercher_coefficients(terme)
        for coeff in resultats_coeff:
            self.tree.insert("", tk.END, values=(
                coeff.nom, coeff.valeur, coeff.unite, coeff.source, coeff.statut, "N/A"
            ), tags=("coefficient",))
    
    def _afficher_tout(self):
        """Affiche tous les éléments"""
        self._charger_donnees()
    
    def _afficher_details(self, event):
        """Affiche les détails d'un élément sélectionné"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        nom = item['values'][0]
        
        # Trouver l'élément
        if nom in self.manager.references_locales:
            element = self.manager.references_locales[nom]
            self._afficher_fenetre_details(element, "Référence")
        elif nom in self.manager.dotations_locales:
            element = self.manager.dotations_locales[nom]
            self._afficher_fenetre_details(element, "Dotation")
        elif nom in self.manager.coefficients_locaux:
            element = self.manager.coefficients_locaux[nom]
            self._afficher_fenetre_details(element, "Coefficient")
    
    def _afficher_fenetre_details(self, element, type_element):
        """Affiche une fenêtre de détails"""
        fenetre = tk.Toplevel(self.root)
        fenetre.title(f"Détails - {type_element}: {element.nom}")
        fenetre.geometry("500x400")
        
        # Frame principal
        frame = ttk.Frame(fenetre, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Informations de base
        ttk.Label(frame, text=f"Nom: {element.nom}", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        ttk.Label(frame, text=f"Valeur: {element.valeur} {element.unite}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"Source: {element.source}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"Statut: {element.statut}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"Version: {element.version}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"Date création: {element.date_creation}").pack(anchor=tk.W)
        
        # Description
        ttk.Label(frame, text="Description:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        desc_text = tk.Text(frame, height=4, width=50, wrap=tk.WORD)
        desc_text.insert("1.0", element.description)
        desc_text.pack(anchor=tk.W, pady=(5, 0))
        
        # Historique
        ttk.Label(frame, text="Historique:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        hist_text = tk.Text(frame, height=8, width=50, wrap=tk.WORD)
        for entree in element.historique:
            hist_text.insert(tk.END, f"{entree['date']} - {entree['action']} par {entree['utilisateur']}\n")
            if entree['details']:
                hist_text.insert(tk.END, f"  {entree['details']}\n")
            hist_text.insert(tk.END, "\n")
        hist_text.pack(anchor=tk.W, pady=(5, 0))
    
    def _valider_selectionne(self):
        """Valide l'élément sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Aucun élément sélectionné")
            return
        
        item = self.tree.item(selection[0])
        nom = item['values'][0]
        utilisateur = self.utilisateur_var.get().strip()
        
        if nom in self.manager.references_locales:
            success = self.manager.valider_reference(nom, utilisateur)
        elif nom in self.manager.dotations_locales:
            success = self.manager.valider_dotation(nom)
        elif nom in self.manager.coefficients_locaux:
            success = self.manager.valider_coefficient(nom)
        else:
            success = False
        
        if success:
            messagebox.showinfo("Succès", "Élément validé avec succès")
            self._charger_donnees()
        else:
            messagebox.showerror("Erreur", "Impossible de valider l'élément")
    
    def _deprecie_selectionne(self):
        """Déprécie l'élément sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Aucun élément sélectionné")
            return
        
        item = self.tree.item(selection[0])
        nom = item['values'][0]
        
        if nom in self.manager.references_locales:
            success = self.manager.deprecie_reference(nom)
        elif nom in self.manager.dotations_locales:
            success = self.manager.deprecie_dotation(nom)
        elif nom in self.manager.coefficients_locaux:
            success = self.manager.deprecie_coefficient(nom)
        else:
            success = False
        
        if success:
            messagebox.showinfo("Succès", "Élément déprécié avec succès")
            self._charger_donnees()
        else:
            messagebox.showerror("Erreur", "Impossible de déprécier l'élément")
    
    def _exporter(self):
        """Exporte la configuration"""
        fichier = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        
        if fichier:
            try:
                if fichier.endswith('.yaml'):
                    config = self.manager.exporter_configuration("yaml")
                else:
                    config = self.manager.exporter_configuration("json")
                
                with open(fichier, 'w', encoding='utf-8') as f:
                    f.write(config)
                
                messagebox.showinfo("Succès", "Configuration exportée avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")
    
    def _importer(self):
        """Importe une configuration"""
        fichier = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        
        if fichier:
            try:
                # Demander le mode d'import
                mode = tk.StringVar(value="remplacer")
                dialog = tk.Toplevel(self.root)
                dialog.title("Mode d'import")
                dialog.geometry("300x150")
                
                ttk.Label(dialog, text="Choisir le mode d'import:").pack(pady=10)
                ttk.Radiobutton(dialog, text="Remplacer tout", variable=mode, value="remplacer").pack()
                ttk.Radiobutton(dialog, text="Fusion", variable=mode, value="fusion").pack()
                ttk.Radiobutton(dialog, text="Mettre à jour", variable=mode, value="mettre_a_jour").pack()
                
                def confirmer():
                    dialog.destroy()
                    mode_import = ModeImport(mode.get())
                    success = self.manager.importer_configuration(fichier, mode_import)
                    
                    if success:
                        messagebox.showinfo("Succès", "Configuration importée avec succès")
                        self._charger_donnees()
                    else:
                        messagebox.showerror("Erreur", "Erreur lors de l'import")
                
                ttk.Button(dialog, text="Confirmer", command=confirmer).pack(pady=10)
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'import: {str(e)}")
    
    def _afficher_stats(self):
        """Affiche les statistiques"""
        stats = self.manager.generer_rapport_statut()
        
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Statistiques")
        fenetre.geometry("400x300")
        
        frame = ttk.Frame(fenetre, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Statistiques des constantes", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Références
        ttk.Label(frame, text="Références locales:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        ttk.Label(frame, text=f"  Total: {stats['references_locales']['total']}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"  Validées: {stats['references_locales']['validees']}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"  Proposées: {stats['references_locales']['proposees']}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"  Dépréciées: {stats['references_locales']['depreciees']}").pack(anchor=tk.W)
        
        # Dotations
        ttk.Label(frame, text="Dotations locales:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(frame, text=f"  Total: {stats['dotations_locales']['total']}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"  Validées: {stats['dotations_locales']['validees']}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"  Proposées: {stats['dotations_locales']['proposees']}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"  Dépréciées: {stats['dotations_locales']['depreciees']}").pack(anchor=tk.W)
        
        # Coefficients
        ttk.Label(frame, text="Coefficients locaux:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(frame, text=f"  Total: {stats['coefficients_locaux']['total']}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"  Validés: {stats['coefficients_locaux']['valides']}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"  Proposés: {stats['coefficients_locaux']['proposes']}").pack(anchor=tk.W)
        ttk.Label(frame, text=f"  Dépréciés: {stats['coefficients_locaux']['deprecies']}").pack(anchor=tk.W)
    
    def demarrer(self):
        """Démarre l'interface graphique"""
        self.root.mainloop()

def lancer_gui(config_dir: Optional[str] = None):
    """Fonction utilitaire pour lancer l'interface graphique"""
    app = ConstantsGUI(config_dir)
    app.demarrer()

if __name__ == "__main__":
    lancer_gui()
