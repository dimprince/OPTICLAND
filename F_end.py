import customtkinter as ctk
from tkinter import messagebox
from customtkinter import CTkInputDialog
from datetime import datetime
from B_end import CentreOptique
from services import ajouter_patient
from services import modifier_patient
from services import supprimer_patient
from services import ajouter_produit
from services import supprimer_produit
from services import rechercher_patient
from services import rechercher_produit
from services import ajouter_vente
from services import supprimer_vente
from services import ajouter_consultation
from services import supprimer_consultation
from services import ajouter_livraison
from services import supprimer_livraison
from services import ajouter_commande
from services import supprimer_commande
from db import get_connection


#+++++++++++++++++++++++++++++++ CONNECTION TO BD +++++++++++++++++++++++++++++++++++++++

conn = get_connection()
cur = conn.cursor()

# ================= UI PALETTE =================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG = "#F0F7FF"
PANEL = "#FFFFFF"
SIDEBAR = "#1A3A5F"

PRIMARY = "#2D9CDB"
SECONDARY = "#56CCF2"
SUCCESS = "#27AE60"
WARNING = "#F2C94C"
DANGER = "#EB5757"
TEXT = "#2C3E50"
TEXT_LIGHT = "#7F8C8D"
GRADIENT_START = "#1A3A5F"
GRADIENT_END = "#2D9CDB"
CARD_BG = "#FFFFFF"
STAT_BG = "#F8F9FA"

# ================= APP =================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OPTIC LAND - Centre Optique de Excellence")
        self.geometry("1400x800")
        self.configure(fg_color=BG)
        self.minsize(1200, 700)

        # Configuration du grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.centre = CentreOptique()
        
        
        self.sidebar()
        self.main_container()
        
        self.show_home()


    # ================= SIDEBAR =================
    def sidebar(self):
        self.side = ctk.CTkFrame(self, width=280, fg_color=SIDEBAR, corner_radius=0)
        self.side.grid(row=0, column=0, sticky="ns")
        self.side.grid_propagate(False)

        # Logo et titre
        logo_frame = ctk.CTkFrame(self.side, fg_color="transparent")
        logo_frame.pack(pady=30, padx=20)
        
        ctk.CTkLabel(
            logo_frame,
            text="👁️",
            font=("Arial", 48, "bold"),
            text_color=SECONDARY
        ).pack()
        
        ctk.CTkLabel(
            logo_frame,
            text="OPTIC LAND",
            font=("Arial", 26, "bold"),
            text_color="white"
        ).pack()
        
        ctk.CTkLabel(
            logo_frame,
            text="Centre Optique d'Excellence",
            font=("Arial", 11),
            text_color=TEXT_LIGHT
        ).pack()

        # Menu principal
        menu_items = [
            ("🏠 Accueil", self.show_home),
            ("👥 Patients", self.ui_patients),
            ("📦 Produits", self.ui_produits),
            ("💰 Ventes", self.ui_ventes),
            ("🩺 Consultations", self.ui_consultations),
            ("📋 Commandes", self.ui_commandes),
            ("🚚 Livraisons", self.ui_livraisons),
        ]

        for text, command in menu_items:
            btn = ctk.CTkButton(
                self.side, 
                text=text, 
                command=command,
                fg_color="transparent",
                hover_color=PRIMARY,
                anchor="w",
                font=("Arial", 14),
                height=45,
                corner_radius=10
            )
            btn.pack(pady=5, padx=20, fill="x")

        # Statistiques rapides
        stats_frame = ctk.CTkFrame(self.side, fg_color="transparent")
        stats_frame.pack(side="bottom", pady=30, padx=20, fill="x")
        
        ctk.CTkLabel(
            stats_frame,
            text="📊 Aujourd'hui",
            font=("Arial", 12, "bold"),
            text_color=TEXT_LIGHT
        ).pack(anchor="w", pady=(0, 10))
        
        self.today_stats = {
            "ventes": ctk.CTkLabel(stats_frame, text="Ventes: 0", font=("Arial", 11), text_color="white"),
            "consultations": ctk.CTkLabel(stats_frame, text="Consultations: 0", font=("Arial", 11), text_color="white")
        }
        
        for stat in self.today_stats.values():
            stat.pack(anchor="w", pady=2)
        
        self.update_today_stats()

        # Bouton quitter
        ctk.CTkButton(
            self.side, 
            text="🚪 Quitter", 
            fg_color=DANGER, 
            hover_color="#C0392B",
            command=self.destroy,
            height=40,
            corner_radius=10
        ).pack(side="bottom", pady=20, padx=20, fill="x")

    def update_today_stats(self):
        """Met à jour les statistiques du jour"""
        today = datetime.now().strftime("%Y-%m-%d")
        ventes_today = len([v for v in self.centre.ventes if v.date == today])
        consultations_today = len([c for c in self.centre.consultations if hasattr(c, 'date') and c.date == today])
        
        self.today_stats["ventes"].configure(text=f"Ventes: {ventes_today}")
        self.today_stats["consultations"].configure(text=f"Consultations: {consultations_today}")

    # ================= MAIN =================
    def main_container(self):
        self.main = ctk.CTkScrollableFrame(self, fg_color=BG)
        self.main.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main.grid_columnconfigure(0, weight=1)

    def clear(self):
        for w in self.main.winfo_children():
            w.destroy()

    # ================= HOME =================
    def show_home(self):
        self.clear()
        
        # En-tête avec bienvenue
        header_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 30))
        
        current_time = datetime.now().strftime("%A, %d %B %Y | %H:%M")
        
        ctk.CTkLabel(
            header_frame,
            text="Bienvenue chez OPTIC LAND",
            font=("Arial", 36, "bold"),
            text_color=SIDEBAR
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_frame,
            text=f"Votre partenaire de confiance pour une vision parfaite - {current_time}",
            font=("Arial", 14),
            text_color=TEXT_LIGHT
        ).pack(anchor="w", pady=(5, 0))


        # Sections de services
        services_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        services_frame.pack(fill="x", padx=30, pady=30)
        
        ctk.CTkLabel(
            services_frame,
            text="Nos Services",
            font=("Arial", 24, "bold"),
            text_color=SIDEBAR
        ).pack(anchor="w", pady=(0, 20))
        
        services_grid = ctk.CTkFrame(services_frame, fg_color="transparent")
        services_grid.pack(fill="x")
        services_grid.grid_columnconfigure((0,1,2), weight=1)
        
        services = [
            ("👁️", "Consultations Complet", "Examen de vue approfondi\navec équipement moderne"),
            ("👓", "Vente de Lunettes", "Large choix de montures\net verres de qualité"),
            ("🔬", "Lentilles de Contact", "Adaptation et suivi\npersonnalisé"),
            ("🏥", "Dépistage", "Détection précoce\ndes problèmes visuels"),
            ("🚚", "Livraison à Domicile", "Service rapide\net pratique"),
            ("📋", "Suivi Personnalisé", "Accompagnement\ndans le temps")
        ]
        
        for i, (icon, title, desc) in enumerate(services):
            row, col = i // 3, i % 3
            card = ctk.CTkFrame(services_grid, fg_color=CARD_BG, corner_radius=15)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=icon, font=("Arial", 36)).pack(pady=(20, 5))
            ctk.CTkLabel(card, text=title, font=("Arial", 16, "bold")).pack(pady=(5, 5))
            ctk.CTkLabel(card, text=desc, font=("Arial", 11), text_color=TEXT_LIGHT, justify="center").pack(pady=(0, 20))


    def search_patient(self):
        idp = CTkInputDialog(text="ID du patient", title="Rechercher Patient").get_input()
        if idp:
            patient = self.centre.rechercher_patient(idp)
            if patient:
                messagebox.showinfo("Patient Trouvé", str(patient))
            else:
                messagebox.showwarning("Non Trouvé", "Aucun patient avec cet ID")

    def show_sales_report(self):
        report = f"📊 RAPPORT DES VENTES\n\n"
        report += f"Total des ventes: {len(self.centre.ventes)}\n"
        report += f"Revenus totaux: {self.centre.get_chiffre_affaires():,} FCFA\n\n"
        report += "Détail des ventes:\n"
        report += "-" * 50 + "\n"
        
        for vente in self.centre.ventes:
            report += f"{vente.date} - {vente.produit.nom} - {vente.qte} x {vente.produit.prix} = {vente.total} FCFA\n"
        
        messagebox.showinfo("Rapport des Ventes", report)

    # ================= LIST =================
    def show_list(self, data, title="Liste"):
        if not data:
            empty_frame = ctk.CTkFrame(self.main, fg_color=CARD_BG, corner_radius=15)
            empty_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(
                empty_frame,
                text="📭",
                font=("Arial", 48)
            ).pack(expand=True)
            ctk.CTkLabel(
                empty_frame,
                text=f"Aucun {title.lower()} trouvé",
                font=("Arial", 16),
                text_color=TEXT_LIGHT
            ).pack(expand=True)
            return
            
        box = ctk.CTkTextbox(self.main, height=400, font=("Courier", 11))
        box.pack(fill="both", expand=True, padx=20, pady=20)

        for d in data:
            box.insert("end", str(d) + "\n")
            box.insert("end", "-" * 80 + "\n")

    # ================= PATIENTS =================
    def ui_patients(self):
        self.clear()
        
        # En-tête
        header_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header_frame,
            text="Gestion des Patients",
            font=("Arial", 28, "bold"),
            text_color=SIDEBAR
        ).pack(anchor="w")

        # Formulaire
        f = ctk.CTkFrame(self.main, fg_color=CARD_BG, corner_radius=15)
        f.pack(fill="x", padx=20, pady=10)

        # Deux colonnes pour le formulaire
        form_frame = ctk.CTkFrame(f, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=20)
        form_frame.grid_columnconfigure((0,1), weight=1)

        # Colonne gauche
        left_col = ctk.CTkFrame(form_frame, fg_color="transparent")
        left_col.grid(row=0, column=0, padx=10, sticky="nsew")
        
        idp = ctk.CTkEntry(left_col, placeholder_text="ID Patient *", width=250)
        idp.pack(pady=5, fill="x")
        
        nom = ctk.CTkEntry(left_col, placeholder_text="Nom complet *", width=250)
        nom.pack(pady=5, fill="x")
        
        dn = ctk.CTkEntry(left_col, placeholder_text="Date naissance (JJ/MM/AAAA)", width=250)
        dn.pack(pady=5, fill="x")
        
        tel = ctk.CTkEntry(left_col, placeholder_text="Téléphone", width=250)
        tel.pack(pady=5, fill="x")

        # Colonne droite
        right_col = ctk.CTkFrame(form_frame, fg_color="transparent")
        right_col.grid(row=0, column=1, padx=10, sticky="nsew")
        
        adresse = ctk.CTkEntry(right_col, placeholder_text="Adresse", width=250)
        adresse.pack(pady=5, fill="x")

        # Sexe
        ctk.CTkLabel(right_col, text="Sexe", font=("Arial", 12)).pack(anchor="w", pady=(5,0))
        sexe_var = ctk.StringVar(value="M")
        sexe_menu = ctk.CTkOptionMenu(right_col, values=["M", "F"], variable=sexe_var, width=250)
        sexe_menu.pack(pady=5, fill="x")

        # Assurance
        ctk.CTkLabel(right_col, text="Assurance", font=("Arial", 12)).pack(anchor="w", pady=(5,0))
        assure_var = ctk.StringVar(value="Non")
        assure_menu = ctk.CTkOptionMenu(right_col, values=["Non", "Oui"], variable=assure_var, width=250)
        assure_menu.pack(pady=5, fill="x")

        # Champ assurance dynamique
        self.nom_assurance_entry = None
        extra_frame = ctk.CTkFrame(right_col, fg_color="transparent")
        extra_frame.pack(fill="x", pady=5)

        def update_fields(choice):
            for w in extra_frame.winfo_children():
                w.destroy()
            self.nom_assurance_entry = None
            if choice == "Oui":
                self.nom_assurance_entry = ctk.CTkEntry(extra_frame, placeholder_text="Nom de l'assurance", width=250)
                self.nom_assurance_entry.pack(fill="x")

        assure_menu.configure(command=update_fields)

        # Boutons d'actions
        def add():
            try:
                is_assure = assure_var.get() == "Oui"
                nom_ass = self.nom_assurance_entry.get() if is_assure and self.nom_assurance_entry else ""
                
                ajouter_patient(
                    idp.get(), nom.get(), dn.get(), tel.get(),
                    adresse.get(), sexe_var.get(), is_assure, nom_ass
                )
                messagebox.showinfo("Succès", "Patient ajouté avec succès !")
                self.ui_patients()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        def delete():
            idp = CTkInputDialog(text="ID Patient", title="Supprimer").get_input()
            if idp and messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce patient ?"):
                try:
                    supprimer_patient(idp)
                    messagebox.showinfo("Succès", "Patient supprimé !")
                    self.ui_patients()
                except Exception as e:
                    messagebox.showerror("Erreur", str(e))

        def search():
            idp = CTkInputDialog(text="ID Patient", title="Rechercher").get_input()
            if idp:
                patient = rechercher_patient(idp)
                if patient:
                    messagebox.showinfo("Résultat", str(patient))
                else:
                    messagebox.showwarning("Non trouvé", "Patient non trouvé")

        def modify():
            idp = CTkInputDialog(text="ID Patient", title="Modifier").get_input()
            if idp:
                patient = rechercher_patient(idp)
                if not patient:
                    messagebox.showerror("Erreur", "Patient non trouvé")
                    return
                
                # Ouvrir une fenêtre de modification
                mod_window = ctk.CTkToplevel(self)
                mod_window.title("Modifier Patient")
                mod_window.geometry("400x500")
                
                entries = {}
                fields = [
                    ("Nom", patient[1]),
                    ("Date naissance", patient[2]),
                    ("Téléphone", patient[3]),
                    ("Adresse", patient[4]),
                    ("Sexe", patient[5])
                ]
                
                for field_name, default_value in fields:
                    frame = ctk.CTkFrame(mod_window, fg_color="transparent")
                    frame.pack(pady=5, padx=20, fill="x")
                    
                    ctk.CTkLabel(frame, text=field_name, width=120, anchor="w").pack(side="left")
                    entry = ctk.CTkEntry(frame, placeholder_text=field_name)
                    entry.insert(0, str(default_value))
                    entry.pack(side="left", fill="x", expand=True)
                    entries[field_name] = entry
                
                def save_mod():
                    try:
                        modifier_patient(
                            idp,
                            entries["Nom"].get(),
                            entries["Date naissance"].get(),
                            entries["Téléphone"].get(),
                            entries["Adresse"].get(),
                            entries["Sexe"].get()
                        )
                        messagebox.showinfo("Succès", "Patient modifié !")
                        mod_window.destroy()
                        self.ui_patients()
                    except Exception as e:
                        messagebox.showerror("Erreur", str(e))
                
                ctk.CTkButton(mod_window, text="Enregistrer", command=save_mod, fg_color=SUCCESS).pack(pady=20)

        button_frame = ctk.CTkFrame(f, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(button_frame, text="➕ Ajouter", fg_color=SUCCESS, command=add, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🔍 Rechercher", fg_color=WARNING, command=search, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="✏️ Modifier", fg_color=PRIMARY, command=modify, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🗑️ Supprimer", fg_color=DANGER, command=delete, width=120).pack(side="left", padx=5)

        self.show_list(self.centre.patients, "patients")

    # ================= PRODUITS =================
    def ui_produits(self):
        self.clear()
        
        header_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header_frame,
            text="Gestion des Produits",
            font=("Arial", 28, "bold"),
            text_color=SIDEBAR
        ).pack(anchor="w")

        f = ctk.CTkFrame(self.main, fg_color=CARD_BG, corner_radius=15)
        f.pack(fill="x", padx=20, pady=10)

        form_frame = ctk.CTkFrame(f, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=20)
        form_frame.grid_columnconfigure((0,1), weight=1)

        left_col = ctk.CTkFrame(form_frame, fg_color="transparent")
        left_col.grid(row=0, column=0, padx=10, sticky="nsew")
        
        idp = ctk.CTkEntry(left_col, placeholder_text="ID Produit *")
        idp.pack(pady=5, fill="x")
        nom = ctk.CTkEntry(left_col, placeholder_text="Nom du produit *")
        nom.pack(pady=5, fill="x")
        
        right_col = ctk.CTkFrame(form_frame, fg_color="transparent")
        right_col.grid(row=0, column=1, padx=10, sticky="nsew")
        
        prix = ctk.CTkEntry(right_col, placeholder_text="Prix (FCFA) *")
        prix.pack(pady=5, fill="x")
        stock = ctk.CTkEntry(right_col, placeholder_text="Stock *")
        stock.pack(pady=5, fill="x")
        
        ctk.CTkLabel(right_col, text="Type de produit", font=("Arial", 12)).pack(anchor="w", pady=(5,0))
        type_var = ctk.StringVar(value="Lunette")
        type_menu = ctk.CTkOptionMenu(right_col, values=["Lunette", "Lentille", "Produit d'entretien"], variable=type_var)
        type_menu.pack(pady=5, fill="x")

        def add():
            try:
                type_produit = type_var.get()
                
                if type_produit == "Lunette":
                    ajouter_produit(idp.get(), nom.get(), type_var.get(), float(prix.get()), int(stock.get()))
                elif type_produit == "Lentille":
                    ajouter_produit(idp.get(), nom.get(), type_var.get(), float(prix.get()), int(stock.get()))
                else:
                    ajouter_produit(idp.get(), nom.get(), type_var.get(), float(prix.get()), int(stock.get()))
                
                messagebox.showinfo("Succès", "Produit ajouté avec succès")
                self.ui_produits()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
                
        def delete():
            id_produit = CTkInputDialog(text="ID Produit", title="Supprimer").get_input()
            if id_produit and messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce produit ?"):
                try:
                    supprimer_produit(id_produit)
                    messagebox.showinfo("Succès", "Produit supprimé avec succès !")
                    self.ui_produits()
                except Exception as e:
                    messagebox.showerror("Erreur", str(e))
        
        def search():
            id_produit = CTkInputDialog(text="ID Produit", title="Rechercher").get_input()
            if id_produit:
                produit = rechercher_produit(id_produit)
                if produit:
                    messagebox.showinfo("Résultat", str(produit))
                else:
                    messagebox.showwarning("Non trouvé", "Produit non trouvé")

        button_frame = ctk.CTkFrame(f, fg_color="transparent")
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="➕ Ajouter", fg_color=SUCCESS, command=add, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🔍 Rechercher", fg_color=WARNING, command=search, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🗑️ Supprimer", fg_color=DANGER, command=delete, width=120).pack(side="left", padx=5)

        self.show_list(self.centre.produits, "produits")

    # ================= VENTES =================
    def ui_ventes(self):
        self.clear()
        
        header_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header_frame,
            text="Gestion des Ventes",
            font=("Arial", 28, "bold"),
            text_color=SIDEBAR
        ).pack(anchor="w")

        f = ctk.CTkFrame(self.main, fg_color=CARD_BG, corner_radius=15)
        f.pack(fill="x", padx=20, pady=10)

        form_frame = ctk.CTkFrame(f, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=20)
        form_frame.grid_columnconfigure((0,1), weight=1)

        left_col = ctk.CTkFrame(form_frame, fg_color="transparent")
        left_col.grid(row=0, column=0, padx=10, sticky="nsew")
        
        idv = ctk.CTkEntry(left_col, placeholder_text="ID Vente *")
        idv.pack(pady=5, fill="x")
        idprod = ctk.CTkEntry(left_col, placeholder_text="ID Produit *")
        idprod.pack(pady=5, fill="x")
        montant = ctk.CTkEntry(left_col, placeholder_text="Prix *")
        montant.pack(pady=5, fill="x")
        date = ctk.CTkEntry(left_col, placeholder_text="Date *")
        date.pack(pady=5, fill="x")
        heure = ctk.CTkEntry(left_col, placeholder_text="Heure *")
        heure.pack(pady=5, fill="x")
        
        
        right_col = ctk.CTkFrame(form_frame, fg_color="transparent")
        right_col.grid(row=0, column=1, padx=10, sticky="nsew")
        
        qte = ctk.CTkEntry(right_col, placeholder_text="Quantité *")
        qte.pack(pady=5, fill="x")

        def add():
            try:
                date = datetime.now().strftime("%Y-%m-%d")
                heure = datetime.now().strftime("%H:%M:%S")
                
                ajouter_vente(
                    idv.get(), 
                    idprod.get(), 
                    montant.get(),
                    date, 
                    heure, 
                    int(qte.get())
                )
                messagebox.showinfo("Succès", "Vente enregistrée avec succès !")
                self.ui_ventes()
                self.update_today_stats()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        def delete():
            id_vente = CTkInputDialog(text="ID Vente", title="Supprimer").get_input()
            if id_vente and messagebox.askyesno("Confirmation", "Supprimer cette vente ?"):
                try:
                    supprimer_vente(id_vente)
                    messagebox.showinfo("Succès", "Vente supprimée !")
                    self.ui_ventes()
                    self.update_today_stats()
                except Exception as e:
                    messagebox.showerror("Erreur", str(e))

        button_frame = ctk.CTkFrame(f, fg_color="transparent")
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="➕ Ajouter", fg_color=SUCCESS, command=add, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🗑️ Supprimer", fg_color=DANGER, command=delete, width=120).pack(side="left", padx=5)

        self.show_list(self.centre.ventes, "ventes")

    # ================= CONSULTATIONS =================
    def ui_consultations(self):
        self.clear()
        
        header_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header_frame,
            text="Gestion des Consultations",
            font=("Arial", 28, "bold"),
            text_color=SIDEBAR
        ).pack(anchor="w")

        f = ctk.CTkFrame(self.main, fg_color=CARD_BG, corner_radius=15)
        f.pack(fill="x", padx=20, pady=10)

        form_frame = ctk.CTkFrame(f, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=20)
        form_frame.grid_columnconfigure((0,1), weight=1)

        left_col = ctk.CTkFrame(form_frame, fg_color="transparent")
        left_col.grid(row=0, column=0, padx=10, sticky="nsew")
        
        idc = ctk.CTkEntry(left_col, placeholder_text="ID Consultation *")
        idc.pack(pady=5, fill="x")
        date = ctk.CTkEntry(left_col, placeholder_text="Date de consultation *")
        date.pack(pady=5, fill="x")       
        idp = ctk.CTkEntry(left_col, placeholder_text="ID Patient *")
        idp.pack(pady=5, fill="x")
        
        right_col = ctk.CTkFrame(form_frame, fg_color="transparent")
        right_col.grid(row=0, column=1, padx=10, sticky="nsew")
        

        def add():
            try:
                ajouter_consultation(idc.get(), date.get(), idp.get())
                messagebox.showinfo("Succès", "Consultation ajoutée !")
                self.ui_consultations()
                self.update_today_stats()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        def delete():
            id_consult = CTkInputDialog(text="ID Consultation", title="Supprimer").get_input()
            if id_consult and messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette consultation ?"):
                try:
                    supprimer_consultation(id_consult)
                    messagebox.showinfo("Succès", "Consultation supprimée avec succès !")
                    self.ui_consultations()
                    self.update_today_stats()
                except Exception as e:
                    messagebox.showerror("Erreur", str(e))

        button_frame = ctk.CTkFrame(f, fg_color="transparent")
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="➕ Ajouter", fg_color=SUCCESS, command=add, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🗑️ Supprimer", fg_color=DANGER, command=delete, width=120).pack(side="left", padx=5)

        self.show_list(self.centre.consultations, "consultations")

   
    # ================= COMMANDES =================
    def ui_commandes(self):
        self.clear()
        
        header_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header_frame,
            text="Gestion des Commandes",
            font=("Arial", 28, "bold"),
            text_color=SIDEBAR
        ).pack(anchor="w")

        f = ctk.CTkFrame(self.main, fg_color=CARD_BG, corner_radius=15)
        f.pack(fill="x", padx=20, pady=10)

        form_frame = ctk.CTkFrame(f, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=20)
        form_frame.grid_columnconfigure((0,1), weight=1)

        left_col = ctk.CTkFrame(form_frame, fg_color="transparent")
        left_col.grid(row=0, column=0, padx=10, sticky="nsew")
        
        idc = ctk.CTkEntry(left_col, placeholder_text="ID Commande *")
        idc.pack(pady=5, fill="x")
        qte = ctk.CTkEntry(left_col, placeholder_text="Quantité *")
        qte.pack(pady=5, fill="x")       
        
        right_col = ctk.CTkFrame(form_frame, fg_color="transparent")
        right_col.grid(row=0, column=1, padx=10, sticky="nsew")
        
        idp = ctk.CTkEntry(right_col, placeholder_text="ID Produit *")
        idp.pack(pady=5, fill="x")

        def add():
            try:
                ajouter_commande(idc.get(), int(qte.get()), idp.get())
                messagebox.showinfo("Succès", "Commande passée !")
                self.ui_commandes()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        def delete():
            id_commande = CTkInputDialog(text="ID Commande", title="Supprimer").get_input()
            if id_commande and messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette commande ?"):
                try:
                    supprimer_commande(id_commande)
                    messagebox.showinfo("Succès", "Commande supprimée avec succès !")
                    self.ui_commandes()
                except Exception as e:
                    messagebox.showerror("Erreur", str(e))

        button_frame = ctk.CTkFrame(f, fg_color="transparent")
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="➕ Ajouter", fg_color=SUCCESS, command=add, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🗑️ Supprimer", fg_color=DANGER, command=delete, width=120).pack(side="left", padx=5)

        self.show_list(self.centre.commandes, "commandes")

    # ================= LIVRAISONS =================
    def ui_livraisons(self):
        self.clear()
        
        header_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header_frame,
            text="Gestion des Livraisons",
            font=("Arial", 28, "bold"),
            text_color=SIDEBAR
        ).pack(anchor="w")

        f = ctk.CTkFrame(self.main, fg_color=CARD_BG, corner_radius=15)
        f.pack(fill="x", padx=20, pady=10)

        form_frame = ctk.CTkFrame(f, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=20)
        
        idl = ctk.CTkEntry(form_frame, placeholder_text="ID Livraison *")
        idl.pack(pady=5, fill="x")
        idc = ctk.CTkEntry(form_frame, placeholder_text="ID Commande *")
        idc.pack(pady=5, fill="x")

        def add():
            try:
                ajouter_livraison(idl.get(), idc.get())
                messagebox.showinfo("Succès", "Livraison enregistrée !")
                self.ui_livraisons()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        def delete():
            id_livraison = CTkInputDialog(text="ID Livraison", title="Supprimer").get_input()
            if id_livraison and messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette livraison ?"):
                try:
                    supprimer_livraison(id_livraison)
                    messagebox.showinfo("Succès", "Livraison supprimée avec succès !")
                    self.ui_livraisons()
                except Exception as e:
                    messagebox.showerror("Erreur", str(e))

        button_frame = ctk.CTkFrame(f, fg_color="transparent")
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="➕ Ajouter", fg_color=SUCCESS, command=add, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🗑️ Supprimer", fg_color=DANGER, command=delete, width=120).pack(side="left", padx=5)

        self.show_list(self.centre.livraisons, "livraisons")

# ================= RUN =================
if __name__ == "__main__":
    
    app = App()
    app.mainloop()