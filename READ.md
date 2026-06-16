# OPTIC LAND - Système de Gestion de Centre Optique

## 📖 Présentation

OPTIC LAND est une application de gestion destinée aux centres optiques permettant d'administrer efficacement :

* Les patients
* Les produits optiques
* Les consultations
* Les ventes
* Les commandes
* Les livraisons

L'application dispose d'une interface graphique moderne développée avec **CustomTkinter** et utilise **PostgreSQL** pour la persistance des données.


# 🚀 Fonctionnalités

## 👥 Gestion des Patients

* Ajouter un patient
* Modifier les informations d'un patient
* Rechercher un patient
* Supprimer un patient
* Gestion des assurances médicales

### Informations enregistrées

* Identifiant patient
* Nom complet
* Date de naissance
* Téléphone
* Adresse
* Sexe
* Statut d'assurance
* Nom de l'assurance

---

## 📦 Gestion des Produits

* Ajouter un produit
* Rechercher un produit
* Supprimer un produit
* Gestion du stock

### Types de produits

* Lunettes
* Lentilles
* Produits d'entretien

### Informations enregistrées

* Code produit
* Libellé
* Type
* Prix
* Stock disponible

---

## 💰 Gestion des Ventes

* Enregistrer une vente
* Supprimer une vente
* Historique des ventes
* Suivi du chiffre d'affaires

### Informations enregistrées

* Numéro de vente
* Produit vendu
* Montant
* Date
* Heure
* Quantité

---

## 🩺 Gestion des Consultations

* Ajouter une consultation
* Supprimer une consultation
* Historique des consultations

### Informations enregistrées

* Numéro consultation
* Date consultation
* Patient concerné

---

## 📋 Gestion des Commandes

* Enregistrer une commande
* Supprimer une commande

### Informations enregistrées

* Numéro commande
* Quantité
* Produit commandé

---

## 🚚 Gestion des Livraisons

* Ajouter une livraison
* Supprimer une livraison

### Informations enregistrées

* Numéro livraison
* Commande associée

---

# 🏗️ Architecture du Projet

```text
OPTICLAND/
│
├── main.py                 # Interface graphique principale
├── services.py             # Services CRUD et logique métier
├── db.py                   # Connexion PostgreSQL
├── B_end.py                # Modèle métier (CentreOptique)
│
├── README.md
│
└── database/
    └── script.sql          # Création des tables PostgreSQL
```

---

# 🗄️ Base de Données

Le projet utilise PostgreSQL.

## Paramètres de connexion

```python
host="localhost"
database="CENTRE_OPTICLABS"
user="postgres"
password="mc2007mc"
port="5432"
```


# 📑 Tables Principales

## PATIENT

| Champ | Description      |
| ----- | ---------------- |
| PA_CO | Code patient     |
| PA_NP | Nom patient      |
| PA_DN | Date naissance   |
| PA_TE | Téléphone        |
| PA_AD | Adresse          |
| PA_SX | Sexe             |
| PA_ST | Statut assurance |
| PA_AS | Assurance        |

---

## PRODUITS

| Champ  | Description  |
| ------ | ------------ |
| PR_CO  | Code produit |
| PR_LI  | Libellé      |
| PR_TY  | Type         |
| PR_MON | Prix         |
| PR_ST  | Stock        |

---

## VENTE

| Champ  | Description  |
| ------ | ------------ |
| VE_NO  | Numéro vente |
| VE_PR  | Produit      |
| VE_MON | Montant      |
| VE_DA  | Date         |
| VE_HE  | Heure        |
| VE_QT  | Quantité     |

---

## CONSULTATIONS

| Champ | Description         |
| ----- | ------------------- |
| CO_NU | Numéro consultation |
| CO_DA | Date                |
| CO_PA | Patient             |

---

## COMMANDES

| Champ  | Description     |
| ------ | --------------- |
| COM_NO | Numéro commande |
| COM_QT | Quantité        |
| COM_PR | Produit         |

---

## LIVRAISONS

| Champ | Description      |
| ----- | ---------------- |
| LI_ID | Numéro livraison |
| CO_CO | Commande         |

---


# 🖥️ Interface Utilisateur

L'application propose :

### Menu principal

* Accueil
* Patients
* Produits
* Ventes
* Consultations
* Commandes
* Livraisons

### Tableau de bord

Affiche :

* Nombre de ventes du jour
* Nombre de consultations du jour
* Chiffre d'affaires
* Services proposés

---

# 📊 Statistiques Disponibles

Le système permet de suivre :

* Nombre total de patients
* Nombre total de produits
* Nombre total de ventes
* Nombre total de consultations
* Nombre total de commandes
* Nombre total de livraisons
* Chiffre d'affaires global

---

# 🛠️ Technologies Utilisées

| Technologie   | Usage                 |
| ------------- | --------------------- |
| Python 3      | Langage principal     |
| CustomTkinter | Interface graphique   |
| PostgreSQL    | Base de données       |
| Psycopg2      | Connexion PostgreSQL  |
| Tkinter       | Fenêtres et dialogues |

---

# 👨‍💻 Auteur

Projet réalisé dans le cadre de la gestion d'un centre optique.

**OPTIC LAND - Centre Optique d'Excellence**
