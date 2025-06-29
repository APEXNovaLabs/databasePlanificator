/*
    Script de suppression des tables
*/

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
DROP TABLE IF EXISTS Historique_prix;
DROP TABLE IF EXISTS Remarque;


-- Supprimer complètement la base de données
DROP DATABASE IF EXISTS Planificator;
