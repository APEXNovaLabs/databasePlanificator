# Database for Planificator

- **Description:** Script pour les bases de données du projet Planificator
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
         └── triage/                    # Triage: Triage par ordre alphabetique, Recherche de contrat, Triage des traitements par catégorie, triage des traitements spécifiques à chaque client
     ├── regroupeTraitementCat/         # Scripts de regroupement des traitements par catégories (Script Python et SQL)
     ├── client.py                      # Requête CRUD pour la table Client
     ├── codeObsolète.py                # Requête CRUD pour l'ancienne table Historique
     ├── contrat.py                     # Requête CRUD pour la table Contrat
     ├── crudDatabasePlanificator.py    # Programme principale 
     ├── facture.py                     # Requête CRUD pour la facture Facture
     ├── historique.py                  # Requête CRUD pour la table Historique
     ├── planning.py                    # Requête CRUD pour la table Planning et PlanningDetails
     ├── signalement.py                 # Requête CRUD pour la table Signalement 
     └── traitement.py                  # Requête CRUD pour la table Traitement et typeTraitement
├──  scriptSQL/                         # Script SQL pour la base de données
     └── scriptClean.sql                # Script finale de la base de données
└──  README.md                          # Documentation
```

### 📝 Notice

Certains fichiers peuvent contenir des scripts sur les anciennes versions de la base de données

### 📃 Licence
Ce projet est libre de droits et peut être utilisé pour des projets personnels.
