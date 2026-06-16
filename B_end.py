# ================= ENTITÉS =================

class Patient:
    def __init__(self, idp, nom, dn, tel, adresse, sexe, assure=False, nom_ass=""):
        self.idp = idp
        self.nom = nom
        self.dn = dn
        self.tel = tel
        self.adresse = adresse
        self.sexe = sexe
        self.assure = assure
        self.nom_ass = nom_ass

    def __str__(self):
        return (
            f"{self.idp} | "
            f"{self.nom} | "
            f"{self.dn} | "
            f"{self.adresse} | "
            f"{self.sexe} | "
            f"{self.tel}"
        )     


class Produit:
    def __init__(self, idp, nom, type_produit, prix, stock):
        self.idp = idp
        self.nom = nom
        self.type_produit = type_produit
        self.prix = prix
        self.stock = stock

    def __str__(self):
        return (
            f"{self.idp} | "
            f"{self.nom} | "
            f"{self.type_produit} | "
            f"{self.prix} FCFA | "
            f"Stock: {self.stock}"
        )


class Vente:
    def __init__(self, idv, produit, montant, date, heure, qte):
        self.idv = idv
        self.produit = produit
        self.montant = montant
        self.date = date
        self.heure = heure
        self.qte = qte
        self.total = produit.prix * qte

    def __str__(self):
        return (
            f"{self.idv} | "
            f"{self.produit.nom} | "
            f"{self.montant} FCFA | "
            f"{self.date} | "
            f"{self.heure} | "
            f"Qte: {self.qte} | "
            f"Total: {self.total} FCFA"
        )


class Consultation:
    def __init__(self, idc, date, patient):
        self.idc = idc
        self.date = date
        self.patient = patient

    def __str__(self):
        return (
            f"{self.idc} | "
            f"{self.date} | "
            f"{self.patient.nom} | "
        )


class Fournisseur:
    def __init__(self, idf, nom, tel):
        self.idf = idf
        self.nom = nom
        self.tel = tel

    def __str__(self):
        return (
            f"{self.idf} | "
            f"{self.nom} | "
            f"{self.tel}"
        )


class Commande:
    def __init__(self, idc, qte, produit):
        self.idc = idc
        self.qte = qte
        self.produit = produit

    def __str__(self):
        return (
            f"{self.idc} | "
            f"Qte: {self.qte}"
            f"{self.produit.nom} | "
        )


class Livraison:
    def __init__(self, idl, commande):
        self.idl = idl
        self.commande = commande
        self.date = None  # Sera défini lors de la livraison

    def __str__(self):
        return (
            f"{self.idl} | "
            f"Commande: {self.commande.idc} | "
            f"Fournisseur: {self.commande.fournisseur.nom}"
        )


# ================= CENTRE OPTIQUE =================

class CentreOptique:
    def __init__(self):
        self.patients = []
        self.produits = []
        self.ventes = []
        self.consultations = []
        self.fournisseurs = []
        self.commandes = []
        self.livraisons = []

    # ================= PATIENTS =================
    
    def ajouter_patient(self, idp, nom, dn, tel, adresse, sexe, assure=False, nom_ass=""):
        if self.rechercher_patient(idp):
            raise ValueError("Patient déjà existant")
        self.patients.append(Patient(idp, nom, dn, tel, adresse, sexe, assure, nom_ass))

    def rechercher_patient(self, idp):
        return next((p for p in self.patients if p.idp == idp), None)

    def supprimer_patient(self, idp):
        p = self.rechercher_patient(idp)
        if not p:
            raise ValueError("Patient introuvable")
        self.patients.remove(p)

    def modifier_patient(self, idp, nom, dn, tel, adresse, sexe):
        p = self.rechercher_patient(idp)
        if not p:
            raise ValueError("Patient introuvable")

        p.nom = nom
        p.dn = dn
        p.tel = tel
        p.adresse = adresse
        p.sexe = sexe

    # ================= PRODUITS =================

    def ajouter_lunette(self, idp, nom, prix, stock):
        self._add_produit(
            idp,
            nom,
            prix,
            stock,
            "Lunette"
        )

    def ajouter_lentille(self, idp, nom, prix, stock):
        self._add_produit(
            idp,
            nom,
            prix,
            stock,
            "Lentille"
        )

    def ajouter_entretien(self, idp, nom, prix, stock):
        self._add_produit(
            idp,
            nom,
            prix,
            stock,
            "Produit d'entretien"
        )

    def _add_produit(self, idp, nom, prix, stock, type_produit):
        if self.rechercher_produit(idp):
            raise ValueError("Produit déjà existant")

        self.produits.append(
            Produit(
                idp,
                nom,
                type_produit,
                prix,
                stock,
            )
        )

    def rechercher_produit(self, idp):
        return next((p for p in self.produits if p.idp == idp), None)

    def supprimer_produit(self, idp):
        p = self.rechercher_produit(idp)

        if not p:
            raise ValueError("Produit introuvable")

        self.produits.remove(p)

    def modifier_produit(self, idp, nom, type_produit, prix, stock):
        p = self.rechercher_produit(idp)

        if not p:
            raise ValueError("Produit introuvable")

        p.nom = nom
        p.prix = prix
        p.stock = stock
        p.type_produit = type_produit

    # ================= VENTES =================
    
    def ajouter_vente(self, idv, idprod, date, heure, qte):
        produit = self.rechercher_produit(idprod)

        if not produit:
            raise ValueError("Produit introuvable")
        if produit.stock < qte:
            raise ValueError(f"Stock insuffisant. Stock disponible: {produit.stock}")

        produit.stock -= qte
        montant = produit.prix * qte
        self.ventes.append(Vente(idv, produit, montant, date, heure, qte))
        
    def supprimer_vente(self, id_vente):
        vente = next((v for v in self.ventes if v.idv == id_vente), None)
        if not vente:
            raise ValueError("Vente introuvable")
        # Restaurer le stock
        vente.produit.stock += vente.qte
        self.ventes.remove(vente)
    
    def rechercher_vente(self, idv):
        return next((v for v in self.ventes if v.idv == idv), None)

    # ================= CONSULTATIONS =================
    
    def ajouter_consultation(self, idc, date, idp):
        patient = self.rechercher_patient(idp)
        if not patient:
            raise ValueError("Patient introuvable")

        self.consultations.append(Consultation(idc, date, idp))
    
    def supprimer_consultation(self, idc):
        consultation = next((c for c in self.consultations if c.idc == idc), None)
        if not consultation:
            raise ValueError("Consultation introuvable")
        self.consultations.remove(consultation)
    
    def rechercher_consultation(self, idc):
        return next((c for c in self.consultations if c.idc == idc), None)

    # ================= FOURNISSEURS =================
    
    def ajouter_fournisseur(self, idf, nom, tel):
        if self.rechercher_fournisseur(idf):
            raise ValueError("Fournisseur déjà existant")
        self.fournisseurs.append(Fournisseur(idf, nom, tel))

    def rechercher_fournisseur(self, idf):
        return next((f for f in self.fournisseurs if f.idf == idf), None)
    
    def supprimer_fournisseur(self, idf):
        fournisseur = self.rechercher_fournisseur(idf)
        if not fournisseur:
            raise ValueError("Fournisseur introuvable")
        self.fournisseurs.remove(fournisseur)
    
    def modifier_fournisseur(self, idf, nom, tel):
        fournisseur = self.rechercher_fournisseur(idf)
        if not fournisseur:
            raise ValueError("Fournisseur introuvable")
        fournisseur.nom = nom
        fournisseur.tel = tel

    # ================= COMMANDES =================
    
    def ajouter_commande(self, idc, qte, idp):
        p = self.rechercher_produit(idp)

        if not p:
            raise ValueError("Produit introuvable")
        
        if self.rechercher_commande(idc):
            raise ValueError("Commande déjà existante")

        self.commandes.append(Commande(idc, qte, idp))
    
    def supprimer_commande(self, idc):
        commande = self.rechercher_commande(idc)
        if not commande:
            raise ValueError("Commande introuvable")
        self.commandes.remove(commande)
    
    def rechercher_commande(self, idc):
        return next((c for c in self.commandes if c.idc == idc), None)

    # ================= LIVRAISONS =================
    
    def ajouter_livraison(self, idl, idc):
        cmd = self.rechercher_commande(idc)
        if not cmd:
            raise ValueError("Commande introuvable")
        
        if self.rechercher_livraison(idl):
            raise ValueError("Livraison déjà existante")

        self.livraisons.append(Livraison(idl, cmd))
    
    def supprimer_livraison(self, idl):
        livraison = self.rechercher_livraison(idl)
        if not livraison:
            raise ValueError("Livraison introuvable")
        self.livraisons.remove(livraison)
    
    def rechercher_livraison(self, idl):
        return next((l for l in self.livraisons if l.idl == idl), None)
    
    # ================= STATISTIQUES =================
    
    def get_stats(self):
        return {
            "patients": len(self.patients),
            "produits": len(self.produits),
            "ventes": len(self.ventes),
            "consultations": len(self.consultations),
            "fournisseurs": len(self.fournisseurs),
            "commandes": len(self.commandes),
            "livraisons": len(self.livraisons)
        }
    
    def get_chiffre_affaires(self):
        return sum(v.total for v in self.ventes)
    
    def get_ventes_aujourdhui(self, date):
        return len([v for v in self.ventes if v.date == date])