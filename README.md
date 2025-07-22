<h1 align="center">Planificator (DB)</h1>

<p align="center">
  <strong>Script pour la base de données du projet Planificator.</strong>
</p>

<p align="center">
  <!-- Badges -->
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/github/last-commit/josoavj/dbPlanificator" alt="Last Commit">
  <img src="https://img.shields.io/github/stars/josoavj/dbPlanificator?style=social" alt="GitHub Stars">
</p>
 

# Database for Planificator

- **DB:** mysql
- **Langage pour les scripts:** Python
- **Extension utilisés:** aiomysql, mysqlconnector, bycript, re

## Autres

- Projet **[Planificator](https://github.com/AinaMaminirina18/Planificator)**
- Contributeur du projet:
  - Pour la base de données: [josoavj](https://github.com/josoavj)
  - Pour l'interface: [Aina Maminirina](https://github.com/AinaMaminirina18)
- Final Version: [Planificator 1.0]()

### 📂 Structuration des dossiers

```
Database/
├──  Acccount/                          # Pour les scripts des comptes dans le logiciel (Requête CRUD)
     ├── accountAvecHash.py             # Script avec hashage du mot de passe pour chaque compte
     └── accountSansHash.py             # Script sans hashage du mot de passe pour chaque compte
├──  Contrat/                           # Pour les scripts sur l'ensemble de la table Planificator (Sans Account)
     ├── fonctionnalités/               # Les principaux fonctionnalités dans chaque instance
         ├── Planning/                  # Fonctionnalités sur planning (Affichage, Ajout du détails pour chaque planning, Mise à jour des détails de planification)
         ├── contrat/                   # Fonctionnalités sur le contrat (Choix sur la continuité du contrat)
         ├── infoClient                 # Option de sélection des clients et affichage des traitements assignés
         ├── remarque/                  # Fonctionnalités sur les remarques (Ajout d'une facture à chaque enregistrement de remarque)
         ├── Excel/                     # Géneration de planning par Excel
         ├── Facture/                   # Gestion de facture (Maintenance)
         ├── signalement/               # Gestion des signalements
         └── triage/                    # Triage: Triage par ordre alphabetique, Recherche de contrat, Triage des traitements par catégorie, triage des traitements spécifiques à chaque client
     ├── regroupeTraitementCat/         # Scripts de regroupement des traitements par catégories (Script Python et SQL)
     ├── CRUDonClient.py                # Requête CRUD pour la table Client
     ├── CRUDonContrat.py               # Requête CRUD pour la table Contrat
     ├── mainCRUDonPlanificator.py      # Programme principale 
     ├── CRUDonFacture.py               # Requête CRUD pour la facture Facture
     ├── CRUDonHistorique.py            # Requête CRUD pour la table Historique
     ├── CRUDonPlanning.py              # Requête CRUD pour la table Planning et PlanningDetails
     ├── CRUDonSignalement.py           # Requête CRUD pour la table Signalement 
     └── CRUDonTraitement.py            # Requête CRUD pour la table Traitement et typeTraitement
├──  scriptSQL/                         # Script SQL pour la base de données
     ├── testDB.sql                     # Script pour une série d'insertion de données pour tester la base de données
     ├── SuppressionDB.sql              # Script de suppression de l'entièreté de la base de données
     └── Planificator.sql               # Script principal de la base de données

└──  README.md                          # Documentation
```

### 📝 Notice

Veuillez créer un nouveau utilisateur pour la DB si vous voulez la tester.

### 📃 Licence

Ce projet est libre de droits et peut être utilisé pour des projets personnels. Que ce soit pour les scripts python et aussi ceux de la DB
