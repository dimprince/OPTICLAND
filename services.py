from db import get_connection


#Ajouter un patient
def ajouter_patient(idp, nom, dn, tel, adresse, sexe, assure, nom_ass):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO "PATIENT" ("PA_CO", "PA_NP", "PA_DN", "PA_TE", "PA_AD", "PA_SX", "PA_ST", "PA_AS")
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cur.execute(query, (
        idp,
        nom,
        dn,
        tel,
        adresse,
        sexe,
        assure,
        nom_ass,
    ))

    conn.commit()
    cur.close()
    conn.close()



#Modifier les informations dún client
def modifier_patient(idp, nom, dn, tel, adresse, sexe):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    UPDATE "PATIENT"
    SET "PA_NP" = %s,
        "PA_DN" = %s,
        "PA_TE" = %s,
        "PA_AD" = %s,
        "PA_SX" = %s
    WHERE "PA_CO" = %s
    """

    cur.execute(query, (
        nom,
        dn,
        tel,
        adresse,
        sexe,
        idp
    ))

    conn.commit()
    cur.close()
    conn.close()


#----------------------------------------------------------------------------------------------------------------------------------

def supprimer_patient(idp):
    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
        DELETE FROM "PATIENT"
        WHERE "PA_CO" = %s
        """

        cur.execute(query, (idp,))
        conn.commit()

        if cur.rowcount == 0:
            print("❌ Aucun patient trouvé")
        else:
            print("✅ Patient supprimé")

    except Exception as e:
        print("Erreur :", e)

    finally:
        cur.close()
        conn.close()



#Retrouver un patient----------------------------------------------
def rechercher_patient(idp):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT * FROM "PATIENT" 
    WHERE "PA_CO" = %s
    """
    cur.execute(query, (idp,))

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result


 #Function pour les produits
def ajouter_produit(idp, nom, type_produit, prix, stock):
    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
        INSERT INTO "PRODUITS" ("PR_CO", "PR_LI", "PR_TY", "PR_MON", "PR_ST")
        VALUES (%s, %s, %s, %s, %s)
        """

        cur.execute(query, (idp, nom, type_produit, prix, stock))
        conn.commit()

    finally:
        if conn:
            cur.close()
            conn.close()


def supprimer_produit(idp):
    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
        DELETE FROM "PRODUITS"
        WHERE "PR_CO" = %s
        """

        cur.execute(query, (idp,))
        conn.commit()

        print("✅ Produit supprimé")

    except Exception as e:
        print("Erreur :", e)

    finally:
        cur.close()
        conn.close()



def rechercher_produit(idp):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT * FROM "PRODUITS" 
    WHERE "PR_CO" = %s
    """
    cur.execute(query, (idp,))

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result


def ajouter_vente(idv, idprod, montant, date, heure, qte):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO "VENTE" ("VE_NO", "VE_PR", "VE_MON", "VE_DA", "VE_HE", "VE_QT")
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cur.execute(query, (idv, idprod, montant, date, heure, qte))
    conn.commit()

    
    cur.close()
    conn.close()



def ajouter_consultation(idc, date, idp):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO "CONSULTATIONS" ("CO_NU", "CO_DA", "CO_PA")
    VALUES (%s, %s, %s)
    """

    cur.execute(query, (idc, date, idp))
    conn.commit()

    cur.close()
    conn.close()


def supprimer_consultation(idc):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    DELETE FROM "CONSULTATIONS"
    WHERE "CO_NU" = %s
    """

    cur.execute(query, (idc,))
    conn.commit()

    cur.close()
    conn.close()


def supprimer_vente(idv):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    DELETE FROM "VENTE"
    WHERE "VE_NO" = %s
    """

    cur.execute(query, (idv,))
    conn.commit()


    cur.close()
    conn.close()


def ajouter_livraison(idl, idc):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO "LIVRAISONS" ("LI_ID", "CO_CO")
    VALUES (%s, %s)
    """

    cur.execute(query, (idl, idc))

    conn.commit()
    cur.close()
    conn.close()


def supprimer_livraison(idl):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    DELETE FROM "LIVRAISONS"
    WHERE "LI_ID" = %s
    """

    cur.execute(query, (idl,))
    conn.commit()


    cur.close()
    conn.close()



def ajouter_commande(idc, qte, idp):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO "COMMANDES" ("COM_NO", "COM_QT", "COM_PR")
    VALUES (%s, %s, %s)
    """

    cur.execute(query, (idc, qte, idp))

    conn.commit()
    cur.close()
    conn.close()


def supprimer_commande(idc):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    DELETE FROM "COMMANDES"
    WHERE "COM_NO" = %s
    """

    cur.execute(query, (idc,))
    conn.commit()


    cur.close()
    conn.close()