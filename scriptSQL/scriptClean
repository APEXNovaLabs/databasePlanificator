-- Effacer une table dans Planificator
DROP TABLE IF EXISTS Account;
DROP TABLE IF EXISTS Contrat;
DROP TABLE IF EXISTS Traitement;
DROP TABLE IF EXISTS TypeTraitement;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Facture;
DROP TABLE IF EXISTS Historique;
DROP TABLE IF EXISTS Planning;
DROP TABLE IF EXISTS PlanningDetails;
DROP TABLE IF EXISTS Signalement;
DROP TABLE IF EXISTS Remarque;


-- Supprimer complètement la base de données
DROP DATABASE IF EXISTS Planificator;

-- Création de la DB
CREATE DATABASE Planificator;
USE Planificator;

-- Table Compte
CREATE TABLE Account (
                         id_compte INT AUTO_INCREMENT PRIMARY KEY,  -- Identifiant unique pour chaque compte
                         nom VARCHAR(70) NOT NULL,
                         prenom VARCHAR(70) NOT NULL,
                         email VARCHAR(100) NOT NULL UNIQUE,
                         username VARCHAR(50) NOT NULL UNIQUE,
                         password VARCHAR(255) NOT NULL,
                         type_compte ENUM('Administrateur', 'Utilisateur') NOT NULL,  -- Type de compte
                         date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date de création du compte
                         UNIQUE (nom, prenom)                -- Contrainte d'unicité sur le nom et prénom
);

-- Compte administrateur unique
DELIMITER $$

CREATE TRIGGER avant_ajout_compte
    BEFORE INSERT ON Account
    FOR EACH ROW
BEGIN
    IF NEW.type_compte = 'Administrateur' AND (SELECT COUNT(*) FROM Account WHERE type_compte = 'Administrateur') > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un compte Administrateur existe déjà.';
    END IF;
END$$

DELIMITER ;

-- Vérification du mail
DELIMITER $$

CREATE TRIGGER ajout_compte
    BEFORE INSERT ON Account
    FOR EACH ROW
BEGIN
    IF NEW.email NOT LIKE '%@%.%' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'L\'email doit contenir un "@" et un "."';
    END IF;
END$$

CREATE TRIGGER maj_compte
    BEFORE UPDATE ON Account
    FOR EACH ROW
BEGIN
    IF NEW.email NOT LIKE '%@%.%' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'L\'email doit contenir un "@" et un "."';
    END IF;
END$$

DELIMITER ;

-- Modification du type de compte
DELIMITER $$

CREATE TRIGGER avant_maj_compte
    BEFORE UPDATE ON Account
    FOR EACH ROW
BEGIN
    IF OLD.type_compte != NEW.type_compte THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le type de compte ne peut pas être modifié.';
    END IF;
END$$

DELIMITER ;


-- Pour le mot de passe

DELIMITER $$

CREATE TRIGGER avant_ajout_password
    BEFORE INSERT ON Account
    FOR EACH ROW
BEGIN
    IF CHAR_LENGTH(NEW.password) < 8 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le mot de passe doit contenir au moins 8 caractères.';
    END IF;
END$$

CREATE TRIGGER avant_maj_password
    BEFORE UPDATE ON Account
    FOR EACH ROW
BEGIN
    IF CHAR_LENGTH(NEW.password) < 8 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le mot de passe doit contenir au moins 8 caractères.';
    END IF;
END$$

DELIMITER ;

-- Table Client
CREATE TABLE Client (
                        client_id INT PRIMARY KEY AUTO_INCREMENT,
                        nom VARCHAR(255) NOT NULL,
                        prenom VARCHAR(255),
                        email VARCHAR(255) NOT NULL,
                        telephone VARCHAR(20) NOT NULL,
                        adresse VARCHAR(255) NOT NULL,
                        date_ajout DATE NOT NULL,
                        categorie ENUM ('Particulier', 'Organisation', 'Société') NOT NULL,
                        axe ENUM ('Nord (N)', 'Sud (S)', 'Est (E)', 'Ouest (O)') NOT NULL
);

CREATE TABLE Contrat (
                         contrat_id INT PRIMARY KEY AUTO_INCREMENT,
                         client_id INT NOT NULL,
                         date_contrat DATE NOT NULL,
                         date_debut DATE NOT NULL,
                         date_fin VARCHAR(50),
                         duree ENUM ('Indeterminée', 'Déterminée') NOT NULL,
                         categorie ENUM ('Nouveau', 'Renouvellement') NOT NULL,
                         FOREIGN KEY (client_id) REFERENCES Client(client_id)
);


-- Dans le code, lors de l'ajout du contrat:
SELECT *, DATEDIFF(date_fin, date_debut) AS duree FROM Contrat;

-- Type de traitement utilisant enum
CREATE TABLE TypeTraitement (
                                id_type_traitement INT PRIMARY KEY AUTO_INCREMENT,
                                typeTraitement ENUM('Dératisation', 'Désinfection', 'Désinsectisation', 'Fumigation', 'Nettoyage industriel') NOT NULL
);


-- Table Traitement
CREATE TABLE Traitement (
                            traitement_id INT PRIMARY KEY AUTO_INCREMENT,
                            contrat_id INT NOT NULL,
                            id_type_traitement INT NOT NULL,  -- Clé étrangère vers TypeTraitement
                            FOREIGN KEY (contrat_id) REFERENCES Contrat(contrat_id) ON DELETE CASCADE,
                            FOREIGN KEY (id_type_traitement) REFERENCES TypeTraitement(id_type_traitement) ON DELETE CASCADE -- Ajout de la contrainte pour la clé étrangère
);


-- Table Planning
CREATE TABLE Planning (
                          planning_id INT PRIMARY KEY AUTO_INCREMENT,
                          traitement_id INT NOT NULL,
                          mois_debut VARCHAR(20) NOT NULL,
                          mois_fin VARCHAR(20) NOT NULL,
                          mois_pause VARCHAR(20),
                          redondance ENUM ('Mensuel', 'Hebdomadaire', '2 mois', '3 mois', '4 mois', '6 mois') NOT NULL,
                          date_fin_planification DATE,
                          FOREIGN KEY (traitement_id) REFERENCES Traitement(traitement_id) ON DELETE CASCADE
);

-- Table PlanningDetails
CREATE TABLE PlanningDetails (
                                 planning_detail_id INT PRIMARY KEY AUTO_INCREMENT,
                                 planning_id INT NOT NULL,
                                 date_planification DATE NOT NULL,
                                 statut ENUM ('Effectué', 'À venir') NOT NULL,
                                 element_planification VARCHAR(20) NOT NULL,
                                 FOREIGN KEY (planning_id) REFERENCES Planning(planning_id) ON DELETE CASCADE
);

-- Table Facture
CREATE TABLE Facture (
                         facture_id INT PRIMARY KEY AUTO_INCREMENT,
                         planning_detail_id INT NOT NULL,
                         montant INT NOT NULL,
                         date_traitement DATE NOT NULL,
                         axe VARCHAR(255) NOT NULL,
                         remarque TEXT,
                         FOREIGN KEY (planning_detail_id) REFERENCES PlanningDetails(planning_detail_id) ON DELETE CASCADE
);

-- Table Remarque
CREATE TABLE Remarque (
                          remarque_id INT PRIMARY KEY AUTO_INCREMENT,
                          client_id INT NOT NULL,
                          planning_detail_id INT NOT NULL,
                          contenu TEXT NOT NULL,
                          date_remarque TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                          FOREIGN KEY (client_id) REFERENCES Client(client_id) ON DELETE CASCADE,
                          FOREIGN KEY (planning_detail_id) REFERENCES PlanningDetails(planning_detail_id) ON DELETE CASCADE
);


-- Table Historique
CREATE TABLE Historique (
                            historique_id INT PRIMARY KEY AUTO_INCREMENT,
                            facture_id INT NOT NULL,
                            date_historique TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            contenu TEXT NOT NULL,
                            FOREIGN KEY (facture_id) REFERENCES Facture(facture_id) ON DELETE CASCADE
);

-- Table Avancement
CREATE TABLE Signalement (
                             signalement_id INT PRIMARY KEY AUTO_INCREMENT,
                             planning_detail_id INT NOT NULL,
                             motif TEXT NOT NULL,
                             type ENUM ('Avancement', 'Décalage') NOT NULL,
                             FOREIGN KEY (planning_detail_id) REFERENCES PlanningDetails(planning_detail_id) ON DELETE CASCADE
);