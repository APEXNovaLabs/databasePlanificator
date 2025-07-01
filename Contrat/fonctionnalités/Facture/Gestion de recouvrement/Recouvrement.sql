/*
    Auteur: Josoa (josoavj sur GitHub)
    Base de données: `Recouvrement`
*/

-- --------------------------------------------------------
-- Suppression
DROP TABLE IF EXISTS Factures;
DROP TABLE IF EXISTS PlanningDetails;
DROP TABLE IF EXISTS Planning;
DROP TABLE IF EXISTS Traitement;
DROP TABLE IF EXISTS Contrat;
DROP TABLE IF EXISTS Clients;

-- --------------------------------------------------------
-- Table `Clients`
-- Stocke les informations des clients
CREATE TABLE Clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255),
    email VARCHAR(255),
    telephone VARCHAR(50),
    adresse TEXT,
    categorie ENUM('Particulier', 'Société', 'Organisation') NOT NULL,
    nif VARCHAR(100), -- Numéro d'Identification Fiscale (pour sociétés/organisations)
    stat VARCHAR(100), -- Numéro Statistique (pour sociétés/organisations)
    axe VARCHAR(255) -- Axe géographique ou commercial
);

-- --------------------------------------------------------
-- Table `Contrats`
-- Stocke les informations sur les contrats, liés aux clients
CREATE TABLE Contrats (
    contrat_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    date_contrat DATE NOT NULL,
    date_debut DATE NOT NULL,
    date_fin_contrat DATE, -- NULL si durée indéterminée
    duree ENUM('Déterminée', 'Indéterminée') NOT NULL,
    categorie VARCHAR(255), -- Ex: "Service", "Produit", etc.
    duree_contrat_mois INT, -- Durée en mois si déterminée
    FOREIGN KEY (client_id) REFERENCES Clients(client_id)
);

-- --------------------------------------------------------
-- Table `TypesTraitement`
-- Stocke les différents types de traitements (ex: "Nettoyage", "Maintenance", "Consulting")
CREATE TABLE TypesTraitement (
    id_type_traitement INT AUTO_INCREMENT PRIMARY KEY,
    typeTraitement VARCHAR(255) NOT NULL UNIQUE,
    description TEXT
);

-- --------------------------------------------------------
-- Table `Traitement`
-- Représente l'association d'un type de traitement à un contrat
CREATE TABLE Traitement (
    traitement_id INT AUTO_INCREMENT PRIMARY KEY,
    contrat_id INT NOT NULL,
    id_type_traitement INT NOT NULL,
    FOREIGN KEY (contrat_id) REFERENCES Contrats(contrat_id),
    FOREIGN KEY (id_type_traitement) REFERENCES TypesTraitement(id_type_traitement),
    UNIQUE (contrat_id, id_type_traitement) -- Un contrat n'aura qu'un seul enregistrement pour un type de traitement donné
);

-- --------------------------------------------------------
-- Table `Planning`
-- Définit la planification générale d'un traitement pour un contrat
CREATE TABLE Planning (
    planning_id INT AUTO_INCREMENT PRIMARY KEY,
    traitement_id INT NOT NULL,
    mois_debut VARCHAR(20),
    mois_fin VARCHAR(20),
    mois_pause TEXT,
    redondance ENUM('Journalier', 'Hebdomadaire', 'Mensuel', 'Trimestriel', 'Annuel') NOT NULL,
    FOREIGN KEY (traitement_id) REFERENCES Traitement(traitement_id)
);

-- --------------------------------------------------------
-- Table `PlanningDetails`
-- Représente une instance spécifique et planifiée d'un traitement (date exacte)
-- Ceci est crucial pour la granularité de la facturation par traitement
CREATE TABLE PlanningDetails (
    planning_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    planning_id INT NOT NULL,
    date_planification DATE NOT NULL,
    statut ENUM('Prévu', 'Effectué', 'Annulé', 'Décalé') NOT NULL DEFAULT 'Prévu',
    remarque TEXT,
    FOREIGN KEY (planning_id) REFERENCES Planning(planning_id),
    UNIQUE (planning_id, date_planification) -- Assure qu'un planning n'a qu'un détail par date
);

-- --------------------------------------------------------
-- Table `Factures`
-- Contient les informations de chaque facture, liée à un détail de planning (un traitement spécifique effectué)
CREATE TABLE Factures (
    facture_id INT AUTO_INCREMENT PRIMARY KEY,
    planning_detail_id INT NOT NULL, -- La facture est liée à une instance spécifique de traitement planifié
    montant DECIMAL(10, 2) NOT NULL,
    date_emission DATE NOT NULL,
    date_echeance DATE,
    etat_facture ENUM('Émise', 'Payée', 'En Retard', 'Annulée') NOT NULL DEFAULT 'Émise',
    remarque TEXT,
    FOREIGN KEY (planning_detail_id) REFERENCES PlanningDetails(planning_detail_id)
);

-- --------------------------------------------------------
-- Table `Signalements`
-- Pour les signalements d'avancement ou de décalage de traitements
CREATE TABLE Signalements (
    signalement_id INT AUTO_INCREMENT PRIMARY KEY,
    planning_detail_id INT NOT NULL, -- Le signalement est lié à un détail de planification
    motif TEXT NOT NULL,
    date_signalement DATETIME DEFAULT CURRENT_TIMESTAMP,
    type_signalement ENUM('Avancement', 'Décalage', 'Problème') NOT NULL,
    FOREIGN KEY (planning_detail_id) REFERENCES PlanningDetails(planning_detail_id)
);