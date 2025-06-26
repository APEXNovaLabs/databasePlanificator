USE Planificator;

-- ---
-- 1. Table Client (Parent pour Contrat et Remarque)
-- ---
-- Les IDs des clients seront auto-incrémentés à partir de 1. Cette table n'a pas de clés étrangères entrantes, donc l'insertion est sûre en premier.
INSERT INTO Client (nom, prenom, email, telephone, adresse, nif, stat, date_ajout, categorie, axe) VALUES
('Dupont', 'Pierre', 'pierre.dupont@email.com', '0321234567', '123 Rue de la Liberté, Antananarivo', NULL, NULL, '2024-01-15', 'Particulier', 'Centre (C)'),
('EcoNet Solutions', NULL, 'contact@econet.com', '0345678901', '45 Av. Indépendance, Antananarivo', '1234567890', '9876543210', '2023-11-20', 'Société', 'Nord (N)'),
('Rasoa', 'Lalao', 'lalao.rasoa@mail.com', '0339876543', '7 Bd. Arcades, Antsirabe', NULL, NULL, '2024-02-01', 'Particulier', 'Sud (S)'),
('GreenClean Services', NULL, 'info@greenclean.org', '0301234567', '8 Rue des Fleurs, Toamasina', NULL, NULL, '2024-03-10', 'Organisation', 'Est (E)'),
('Madagascar Construction SA', NULL, 'contact@madaconstruct.mg', '0329988776', '20 Rte. Université, Antananarivo', '9876543210', '1234567890', '2023-10-05', 'Société', 'Ouest (O)'),
('Randria', 'Jean-Luc', 'jl.randria@mail.com', '0341122334', '30 Av. Platanes, Fianarantsoa', NULL, NULL, '2024-04-22', 'Particulier', 'Sud (S)'),
('Raoelina', 'Fanomezantsoa', 'fano.raoelina@email.com', '0324567890', '50 Rue des Palmiers, Majunga', NULL, NULL, '2024-05-01', 'Particulier', 'Nord (N)'),
('HydroClean Solutions', NULL, 'info@hydroclean.mg', '0331122334', '15 Bd. Port, Toliara', '1122334455', '5544332211', '2024-06-01', 'Société', 'Sud (S)'),
('Andrianina', 'Solo', 'solo.andrianina@email.com', '0320102030', '2 Rue des Baobabs, Mahajanga', NULL, NULL, '2024-06-10', 'Particulier', 'Nord (N)'),
('Horizon Services', NULL, 'contact@horizon.mg', '0340203040', '10 Av. de la Paix, Antananarivo', '2233445566', '6655443322', '2024-06-15', 'Société', 'Centre (C)'),
('Rakoto', 'Voahirana', 'voahirana.r@mail.com', '0331122330', '5 Rue de la Fontaine, Antsiranana', NULL, NULL, '2024-06-20', 'Particulier', 'Nord (N)'),
('Urban Propreté', NULL, 'info@urbanproprete.mg', '0309988770', '25 Route Nationale 7, Antsirabe', NULL, NULL, '2024-06-25', 'Société', 'Sud (S)'),
('Razafy', 'Mamy', 'mamy.razafy@email.com', '0325566770', '40 Bd. Maritime, Toamasina', NULL, NULL, '2024-07-01', 'Particulier', 'Est (E)'),
('Global Hygiene', NULL, 'support@globalhygiene.com', '0346677880', '5 Impasse des Pins, Antananarivo', '3344556677', '7766554433', '2024-07-05', 'Organisation', 'Centre (C)'),
('Fanantenana', 'Haja', 'haja.f@mail.com', '0337788990', '1 Rue des Roses, Morondava', NULL, NULL, '2024-07-10', 'Particulier', 'Ouest (O)'),
('CleanTech Madagascar', NULL, 'contact@cleantech.mg', '0328899000', '12 Avenue des Zébus, Fianarantsoa', '4455667788', '8877665544', '2024-07-15', 'Société', 'Sud (S)'),
('Ranaivo', 'Noromalala', 'noro.r@email.com', '0340011220', '3 Bd. de la Liberté, Ambositra', NULL, NULL, '2024-07-20', 'Particulier', 'Centre (C)'),
('BioProtection SA', NULL, 'info@bioprotection.mg', '0332233440', '7 Place de la Gare, Toliara', '5566778899', '9988776655', '2024-07-25', 'Société', 'Sud (S)'),
('Velona', 'Toky', 'toky.v@mail.com', '0323344550', '22 Rue des Cocotiers, Antsiranana', NULL, NULL, '2024-08-01', 'Particulier', 'Nord (N)'),
('ProNet Services', NULL, 'admin@pronet.mg', '0344455660', '18 Route des Orchidées, Antananarivo', '6677889900', '0099887766', '2024-08-05', 'Société', 'Centre (C)');


### 2. Table TypeTraitement (Parent pour Traitement)
-- Les IDs de TypeTraitement seront auto-incrémentés. Cette table n'a pas de clés étrangères entrantes.
INSERT INTO TypeTraitement (categorieTraitement, typeTraitement) VALUES
('AT: Anti termites', 'Anti termites (AT)'),
('PC', 'Dératisation (PC)'),
('PC', 'Désinfection (PC)'),
('PC', 'Désinsectisation (PC)'),
('PC', 'Fumigation (PC)'),
('NI: Nettoyage Industriel', 'Nettoyage industriel (NI)'),
('RO: Ramassage Ordures', 'Ramassage ordure');


### 3. Table Contrat (Enfant de Client, Parent pour Traitement)
-- Les `client_id`s référencent des IDs Client existants. Le `contrat_id` sera auto-incrémenté.
INSERT INTO Contrat (client_id, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
(1, '2024-01-15', '2024-01-20', '2025-01-19', 'Actif', 12, 'Déterminée', 'Nouveau'),
(2, '2023-11-20', '2023-12-01', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau'),
(3, '2024-02-01', '2024-02-05', '2024-08-04', 'Actif', 6, 'Déterminée', 'Nouveau'),
(4, '2024-03-10', '2024-03-15', '2025-03-14', 'Actif', 12, 'Déterminée', 'Nouveau'),
(5, '2023-10-05', '2023-10-10', NULL, 'Actif', NULL, 'Indeterminée', 'Renouvellement'),
(1, '2025-01-10', '2025-01-20', '2026-01-19', 'Actif', 12, 'Déterminée', 'Renouvellement'), -- Contrat de renouvellement pour le client 1
(6, '2024-04-22', '2024-05-01', '2024-11-30', 'Actif', 7, 'Déterminée', 'Nouveau'),
(7, '2024-05-01', '2024-05-05', '2025-05-04', 'Actif', 12, 'Déterminée', 'Nouveau'),
(8, '2024-06-01', '2024-06-10', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau'),
(9, '2024-06-10', '2024-06-15', '2025-06-14', 'Actif', 12, 'Déterminée', 'Nouveau'),
(10, '2024-06-15', '2024-06-20', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau'),
(11, '2024-06-20', '2024-06-25', '2024-12-24', 'Actif', 6, 'Déterminée', 'Nouveau'),
(12, '2024-06-25', '2024-07-01', '2025-06-30', 'Actif', 12, 'Déterminée', 'Nouveau'),
(13, '2024-07-01', '2024-07-05', '2025-07-04', 'Actif', 12, 'Déterminée', 'Nouveau'),
(14, '2024-07-05', '2024-07-10', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau'),
(15, '2024-07-10', '2024-07-15', '2025-07-14', 'Actif', 12, 'Déterminée', 'Nouveau'),
(16, '2024-07-15', '2024-07-20', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau'),
(17, '2024-07-20', '2024-07-25', '2025-07-24', 'Actif', 12, 'Déterminée', 'Nouveau'),
(18, '2024-07-25', '2024-08-01', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau'),
(19, '2024-08-01', '2024-08-05', '2025-08-04', 'Actif', 12, 'Déterminée', 'Nouveau'),
(20, '2024-08-05', '2024-08-10', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau');


### 4. Table Traitement (Enfant de Contrat et TypeTraitement, Parent pour Planning)
-- Les `contrat_id`s doivent faire référence aux IDs auto-générés de la table Contrat.
-- Les `id_type_traitement` font référence aux IDs auto-générés de TypeTraitement.
-- Pour assurer la cohérence, il est préférable d'utiliser des sous-requêtes ou de connaître explicitement les IDs générés.
-- En supposant que les `id_type_traitement` 1-7 correspondent à l'ordre inséré dans TypeTraitement.
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
( (SELECT contrat_id FROM Contrat WHERE client_id = 1 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)') ), -- Client 1, premier contrat
( (SELECT contrat_id FROM Contrat WHERE client_id = 1 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)') ),
( (SELECT contrat_id FROM Contrat WHERE client_id = 2 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)') ), -- Client 2
( (SELECT contrat_id FROM Contrat WHERE client_id = 3 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)') ), -- Client 3
( (SELECT contrat_id FROM Contrat WHERE client_id = 4 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure') ), -- Client 4
( (SELECT contrat_id FROM Contrat WHERE client_id = 5 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)') ), -- Client 5
( (SELECT contrat_id FROM Contrat WHERE client_id = 5 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)') ),
( (SELECT contrat_id FROM Contrat WHERE client_id = 1 ORDER BY date_contrat DESC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)') ), -- Client 1, second contrat (renouvellement)
( (SELECT contrat_id FROM Contrat WHERE client_id = 6 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)') ), -- Client 6
( (SELECT contrat_id FROM Contrat WHERE client_id = 7 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)') ), -- Client 7
( (SELECT contrat_id FROM Contrat WHERE client_id = 7 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)') ),
( (SELECT contrat_id FROM Contrat WHERE client_id = 8 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)') ), -- Client 8
( (SELECT contrat_id FROM Contrat WHERE client_id = 9 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)') ), -- Client 9
( (SELECT contrat_id FROM Contrat WHERE client_id = 9 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)') ),
( (SELECT contrat_id FROM Contrat WHERE client_id = 10 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)') ), -- Client 10
( (SELECT contrat_id FROM Contrat WHERE client_id = 11 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)') ), -- Client 11
( (SELECT contrat_id FROM Contrat WHERE client_id = 12 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure') ), -- Client 12
( (SELECT contrat_id FROM Contrat WHERE client_id = 13 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)') ), -- Client 13
( (SELECT contrat_id FROM Contrat WHERE client_id = 13 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)') ),
( (SELECT contrat_id FROM Contrat WHERE client_id = 14 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)') ), -- Client 14
( (SELECT contrat_id FROM Contrat WHERE client_id = 15 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)') ), -- Client 15
( (SELECT contrat_id FROM Contrat WHERE client_id = 16 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)') ), -- Client 16
( (SELECT contrat_id FROM Contrat WHERE client_id = 16 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)') ),
( (SELECT contrat_id FROM Contrat WHERE client_id = 17 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)') ), -- Client 17
( (SELECT contrat_id FROM Contrat WHERE client_id = 18 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure') ), -- Client 18
( (SELECT contrat_id FROM Contrat WHERE client_id = 19 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)') ); -- Client 19


### 5. Table Planning (Enfant de Traitement, Parent pour PlanningDetails)
-- Les `traitement_id`s doivent faire référence aux IDs Traitement existants.
-- Compte tenu du mappage potentiellement complexe de Contrat à Traitement, il est plus sûr d'utiliser des sous-requêtes ou d'attribuer explicitement des IDs si connus.
-- Les `traitement_id` actuels (1-20) dans l'INSERT correspondent aux IDs auto-incrémentés séquentiellement si l'INSERT Traitement s'est déroulé sans problème.
-- Aucune modification nécessaire ici si la table Traitement a été peuplée séquentiellement comme prévu.
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(1, '2024-01-20', 1, 12, 12, 1, '2025-01-19'), -- C1, Dératisation, mensuel
(2, '2024-01-25', 1, 12, 12, 3, '2025-01-24'), -- C1, Désinsectisation, trimestriel
(3, '2023-12-01', 12, 12, 0, 1, NULL),       -- C2, Nettoyage, indéterminée, mensuel
(4, '2024-02-05', 2, 8, 6, 1, '2024-08-04'), -- C3, Désinfection, mensuel
(5, '2024-03-15', 3, 12, 12, 2, '2025-03-14'), -- C4, Ramassage, bimensuel
(6, '2023-10-10', 10, 12, 0, 6, NULL),      -- C5, Anti termites, indéterminée, semestriel
(7, '2023-10-15', 10, 12, 0, 1, NULL),      -- C5, Nettoyage, indéterminée, mensuel
(8, '2025-01-20', 1, 12, 12, 1, '2026-01-19'), -- C1 Renouvellement, Dératisation, mensuel
(9, '2024-05-01', 5, 11, 7, 1, '2024-11-30'), -- C6, Désinsectisation, mensuel
(10, '2024-05-05', 5, 12, 12, 1, '2025-05-04'), -- C7, Dératisation, mensuel
(11, '2024-05-10', 5, 12, 12, 3, '2025-05-09'), -- C7, Désinfection, trimestriel
(12, '2024-06-10', 6, 12, 0, 1, NULL),       -- C8, Nettoyage, indéterminée, mensuel
(13, '2024-06-15', 6, 12, 12, 1, '2025-06-14'), -- C9, Dératisation, mensuel
(14, '2024-06-20', 6, 12, 12, 3, '2025-06-19'), -- C9, Désinsectisation, trimestriel
(15, '2024-06-20', 6, 12, 0, 1, NULL),       -- C10, Nettoyage, indéterminée, mensuel
(16, '2024-06-25', 6, 12, 6, 1, '2024-12-24'), -- C11, Désinfection, mensuel
(17, '2024-07-01', 7, 12, 12, 2, '2025-06-30'), -- C12, Ramassage, bimensuel
(18, '2024-07-05', 7, 12, 0, 6, NULL),      -- C13, Anti termites, indéterminée, semestriel
(19, '2024-07-10', 7, 12, 0, 1, NULL),      -- C13, Nettoyage, indéterminée, mensuel
(20, '2024-07-15', 7, 12, 12, 1, '2025-07-14'); -- C14, Dératisation, mensuel


### 6. Table PlanningDetails (Enfant de Planning, Parent pour Facture, Remarque, Signalement, Historique)
-- Les `planning_id`s doivent faire référence aux IDs Planning existants.
-- Similaire à `Traitement`, en supposant que les `planning_id`s 1-20 existent comme IDs auto-incrémentés de la table Planning.
-- Les dates et statuts semblent cohérents avec la date actuelle (Juin 2025).
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
-- Planning 1 (mensuel)
(1, '2024-01-20', 'Effectué'), (1, '2024-02-20', 'Effectué'), (1, '2024-03-20', 'Effectué'), (1, '2024-04-20', 'Effectué'), (1, '2024-05-20', 'Effectué'), (1, '2024-06-20', 'Effectué'), (1, '2024-07-20', 'À venir'), (1, '2024-08-20', 'À venir'),
-- Planning 2 (trimestriel)
(2, '2024-01-25', 'Effectué'), (2, '2024-04-25', 'Effectué'), (2, '2024-07-25', 'À venir'),
-- Planning 3 (mensuel, indéterminé)
(3, '2023-12-01', 'Effectué'), (3, '2024-01-01', 'Effectué'), (3, '2024-02-01', 'Effectué'), (3, '2024-03-01', 'Effectué'), (3, '2024-04-01', 'Effectué'), (3, '2024-05-02', 'Effectué'), (3, '2024-06-01', 'Effectué'), (3, '2024-07-01', 'À venir'), (3, '2024-08-01', 'À venir'), (3, '2024-09-01', 'À venir'), (3, '2024-10-01', 'À venir'), (3, '2024-11-03', 'À venir'), (3, '2024-12-02', 'À venir'), (3, '2025-01-08', 'À venir'), (3, '2025-02-02', 'À venir'), (3, '2025-03-01', 'À venir'),
-- Planning 4 (mensuel)
(4, '2024-02-05', 'Effectué'), (4, '2024-03-05', 'Effectué'), (4, '2024-04-05', 'Effectué'), (4, '2024-05-05', 'Effectué'), (4, '2024-06-05', 'Effectué'), (4, '2024-07-05', 'À venir'),
-- Planning 5 (bimensuel)
(5, '2024-03-15', 'Effectué'), (5, '2024-05-15', 'Effectué'), (5, '2024-07-15', 'À venir'),
-- Planning 6 (semestriel, indéterminé)
(6, '2023-10-10', 'Effectué'), (6, '2024-04-10', 'Effectué'), (6, '2024-10-10', 'À venir'),
-- Planning 7 (mensuel, indéterminé)
(7, '2023-10-15', 'Effectué'), (7, '2023-11-15', 'Effectué'), (7, '2023-12-15', 'Effectué'), (7, '2024-01-15', 'Effectué'), (7, '2024-02-15', 'Effectué'), (7, '2024-03-15', 'Effectué'), (7, '2024-04-15', 'Effectué'), (7, '2024-05-15', 'Effectué'), (7, '2024-06-15', 'Effectué'), (7, '2024-07-15', 'À venir'),
-- Planning 9 (mensuel) - Client 6
(9, '2024-05-01', 'Effectué'), (9, '2024-06-01', 'Effectué'), (9, '2024-07-01', 'À venir'),
-- Planning 10 (mensuel) - Client 7
(10, '2024-05-05', 'Effectué'), (10, '2024-06-05', 'Effectué'), (10, '2024-07-05', 'À venir'),
-- Planning 11 (trimestriel) - Client 7
(11, '2024-05-10', 'Effectué'), (11, '2024-08-10', 'À venir'),
-- Planning 12 (mensuel, indéterminé) - Client 8
(12, '2024-06-10', 'Effectué'), (12, '2024-07-10', 'À venir'),
-- Planning 13 (mensuel) - Client 9
(13, '2024-06-15', 'Effectué'), (13, '2024-07-15', 'À venir'),
-- Planning 14 (trimestriel) - Client 9
(14, '2024-06-20', 'Effectué'), (14, '2024-09-20', 'À venir'),
-- Planning 15 (mensuel, indéterminé) - Client 10
(15, '2024-06-20', 'Effectué'), (15, '2024-07-20', 'À venir'),
-- Planning 16 (mensuel) - Client 11
(16, '2024-06-25', 'Effectué'), (16, '2024-07-25', 'À venir'), (16, '2024-08-25', 'À venir'), (16, '2024-09-25', 'À venir'), (16, '2024-10-25', 'À venir'), (16, '2024-11-25', 'À venir'), (16, '2024-12-24', 'À venir'),
-- Planning 17 (bimensuel) - Client 12
(17, '2024-07-01', 'À venir'),
-- Planning 18 (semestriel, indéterminé) - Client 13
(18, '2024-07-05', 'À venir'),
-- Planning 19 (mensuel, indéterminé) - Client 13
(19, '2024-07-10', 'À venir'),
-- Planning 20 (mensuel) - Client 14
(20, '2024-07-15', 'À venir');


### 7. Table Facture (Enfant de PlanningDetails, Parent pour Historique_prix, Remarque, Historique)
-- Les `planning_detail_id`s doivent exister dans PlanningDetails.
-- Le `facture_id` sera auto-incrémenté. C'est là que la plupart des problèmes surviennent avec le référencement explicite des IDs.
-- Ces insertions déterminent les valeurs de `facture_id`.
INSERT INTO Facture (planning_detail_id, montant, date_traitement, etat, axe) VALUES
(1, 50000, '2024-01-20', 'Payé', 'Centre (C)'), (2, 50000, '2024-02-20', 'Payé', 'Centre (C)'), (3, 50000, '2024-03-20', 'Non payé', 'Centre (C)'),
(4, 50000, '2024-04-20', 'Non payé', 'Centre (C)'), (5, 50000, '2024-05-20', 'Payé', 'Centre (C)'), (6, 50000, '2024-06-20', 'Non payé', 'Centre (C)'),
(8, 75000, '2024-01-25', 'Payé', 'Centre (C)'), (9, 75000, '2024-04-25', 'Non payé', 'Centre (C)'),
(11, 150000, '2023-12-01', 'Payé', 'Nord (N)'), (12, 150000, '2024-01-01', 'Payé', 'Nord (N)'), (13, 150000, '2024-02-01', 'Payé', 'Nord (N)'),
(14, 150000, '2024-03-01', 'Non payé', 'Nord (N)'), (15, 150000, '2024-04-01', 'Non payé', 'Nord (N)'), (16, 150000, '2024-05-01', 'Payé', 'Nord (N)'),
(17, 150000, '2024-06-01', 'Non payé', 'Nord (N)'),
(19, 60000, '2024-02-05', 'Payé', 'Sud (S)'), (20, 60000, '2024-03-05', 'Non payé', 'Sud (S)'), (21, 60000, '2024-04-05', 'Non payé', 'Sud (S)'),
(22, 60000, '2024-05-05', 'Payé', 'Sud (S)'), (23, 60000, '2024-06-05', 'Non payé', 'Sud (S)'),
(25, 100000, '2024-03-15', 'Payé', 'Est (E)'), (26, 100000, '2024-05-15', 'Non payé', 'Est (E)'),
(28, 200000, '2023-10-10', 'Payé', 'Ouest (O)'), (29, 200000, '2024-04-10', 'Non payé', 'Ouest (O)'),
(31, 180000, '2023-10-15', 'Payé', 'Ouest (O)'), (32, 180000, '2023-11-15', 'Payé', 'Ouest (O)'), (33, 180000, '2023-12-15', 'Payé', 'Ouest (O)'),
(34, 180000, '2024-01-15', 'Payé', 'Ouest (O)'), (35, 180000, '2024-02-15', 'Payé', 'Ouest (O)'), (36, 180000, '2024-03-15', 'Non payé', 'Ouest (O)'),
(37, 180000, '2024-04-15', 'Non payé', 'Ouest (O)'), (38, 180000, '2024-05-15', 'Payé', 'Ouest (O)'), (39, 180000, '2024-06-15', 'Non payé', 'Ouest (O)'),
(41, 65000, '2024-05-01', 'Payé', 'Sud (S)'), (42, 65000, '2024-06-01', 'Non payé', 'Sud (S)'),
(44, 55000, '2024-05-05', 'Payé', 'Nord (N)'), (45, 55000, '2024-06-05', 'Non payé', 'Nord (N)'),
(49, 160000, '2024-06-10', 'Non payé', 'Sud (S)'),
(51, 50000, '2024-06-15', 'Payé', 'Nord (N)'), (52, 50000, '2024-07-15', 'À venir', 'Nord (N)'), -- Contrat 9, dératisation
(54, 150000, '2024-06-20', 'Payé', 'Centre (C)'), (55, 150000, '2024-07-20', 'À venir', 'Centre (C)'), -- Contrat 10, nettoyage
(57, 60000, '2024-06-25', 'Payé', 'Sud (S)'), (58, 60000, '2024-07-25', 'À venir', 'Sud (S)'); -- Contrat 11, désinfection


### 8. Table Historique_prix (Enfant de Facture)
-- Le `facture_id` doit faire référence aux `facture_id` auto-générés de la table Facture.
-- Nous devons utiliser des sous-requêtes pour nous assurer que le `facture_id` correct est sélectionné en fonction de `planning_detail_id` ou d'autres attributs uniques.
INSERT INTO Historique_prix (facture_id, old_amount, new_amount, change_date, changed_by) VALUES
((SELECT facture_id FROM Facture WHERE planning_detail_id = 1 LIMIT 1), 45000, 50000, '2024-01-21 10:00:00', 'System'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = 8 LIMIT 1), 70000, 75000, '2024-01-26 11:30:00', 'System'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = 11 LIMIT 1), 140000, 150000, '2023-12-02 09:00:00', 'System');


### 9. Table Remarque (Enfant de Client, PlanningDetails, Facture)
-- Les `client_id` et `planning_detail_id` doivent exister.
-- Le `facture_id` doit également exister, et il est préférable de le lier également via `planning_detail_id`.
-- Nous allons lier le `facture_id` dans une instruction `UPDATE` séparée après toutes les insertions.
-- La recommandation précédente d'insérer `NULL` pour `facture_id` dans `Remarque` est bonne si `facture_id` est nullable.
-- Votre DDL pour Remarque avait `facture_id INT NOT NULL`.
-- Si `facture_id` est `NOT NULL` dans `Remarque`, vous **devez** fournir un `facture_id` valide au moment de l'INSERT.
-- Le moyen le plus sûr est d'utiliser des sous-requêtes pour `facture_id` ici aussi, en supposant un mappage 1:1 ou 1:plusieurs clair de `planning_detail_id` à `facture_id`.
-- Si plusieurs `facture_id` peuvent être mappés à un seul `planning_detail_id`, vous auriez besoin d'un critère plus spécifique.
INSERT INTO Remarque (client_id, planning_detail_id, facture_id, contenu, issue, action) VALUES
(1, 1, (SELECT facture_id FROM Facture WHERE planning_detail_id = 1 LIMIT 1), 'Traitement effectué avec succès. Client satisfait.', NULL, 'Vérification post-traitement confirmée.'),
(1, 2, (SELECT facture_id FROM Facture WHERE planning_detail_id = 2 LIMIT 1), 'RAS, mission accomplie.', NULL, 'Rapport de fin d''intervention soumis.'),
(2, 11, (SELECT facture_id FROM Facture WHERE planning_detail_id = 11 LIMIT 1), 'Nettoyage industriel complet. Site propre.', NULL, 'Inspection visuelle et rapport de conformité.'),
(3, 19, (SELECT facture_id FROM Facture WHERE planning_detail_id = 19 LIMIT 1), 'Désinfection effectuée, pas de problème relevé.', NULL, 'Suivi protocolaire de désinfection appliqué.'),
(1, 3, (SELECT facture_id FROM Facture WHERE planning_detail_id = 3 LIMIT 1), 'Client non joignable pour le paiement.', 'Difficulté de communication', 'Relance téléphonique et envoi de mail.'),
(5, 29, (SELECT facture_id FROM Facture WHERE planning_detail_id = 29 LIMIT 1), 'Intervention anti-termites complexe, mais efficace.', 'Accès difficile à certaines zones', 'Utilisation d''équipement spécialisé pour l''accès.'),
(7, 44, (SELECT facture_id FROM Facture WHERE planning_detail_id = 44 LIMIT 1), 'Premier traitement de dératisation pour ce client, tout s''est bien passé.', NULL, 'Conseils de prévention fournis au client.'),
(9, 51, (SELECT facture_id FROM Facture WHERE planning_detail_id = 51 LIMIT 1), 'Nouveau client, premier paiement reçu.', NULL, 'Confirmation de paiement et enregistrement.');

### 10. Table Signalement (Enfant de PlanningDetails, Parent pour Historique)
-- Le `planning_detail_id` doit exister dans PlanningDetails.
-- Le `signalement_id` sera auto-incrémenté.
INSERT INTO Signalement (planning_detail_id, motif, type) VALUES
(4, 'Retard de matériel', 'Décalage'),
(10, 'Urgence client imprévue', 'Avancement'),
(14, 'Accès au site difficile', 'Décalage'),
(23, 'Annulation de dernière minute par le client.', 'Décalage'),
(47, 'Client a demandé un avancement en raison d''un événement.', 'Avancement'),
(52, 'Problème logistique, reporté d''une semaine.', 'Décalage');


### 11. Table Historique (Enfant de Facture, PlanningDetails, Signalement)
-- Toutes les clés étrangères (`facture_id`, `planning_detail_id`, `signalement_id`) doivent exister.
-- Utilisez des sous-requêtes pour `facture_id` et `signalement_id` afin d'assurer un lien correct.
INSERT INTO Historique (facture_id, planning_detail_id, signalement_id, date_historique, contenu, issue, action) VALUES
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 1 LIMIT 1), 1, NULL, '2024-01-20 10:00:00', 'Facture émise et paiement reçu pour Dératisation.', NULL, 'Enregistrement du paiement et fermeture du dossier.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 2 LIMIT 1), 2, NULL, '2024-02-20 10:05:00', 'Facture émise et paiement reçu pour Désinsectisation.', NULL, 'Archivage de la facture et confirmation client.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 3 LIMIT 1), 3, NULL, '2024-03-20 10:10:00', 'Facture émise, en attente de paiement.', 'Paiement en attente', 'Envoi d''une première relance.'),
-- ( (SELECT facture_id FROM Facture WHERE planning_detail_id = 4 LIMIT 1), 4, (SELECT signalement_id FROM Signalement WHERE planning_detail_id = 4 LIMIT 1), 'Facture émise, traitement décalé, en attente de paiement.', 'Décalage traitement', 'Mise à jour du planning et suivi de facture.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 8 LIMIT 1), 8, NULL, '2024-01-25 10:20:00', 'Facture émise et paiement reçu pour Dératisation.', NULL, 'Confirmation de la prestation et clôture.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 9 LIMIT 1), 9, NULL, '2024-04-25 10:25:00', 'Facture émise, en attente de paiement.', 'Paiement en attente', 'Envoi d''une deuxième relance.'),
-- ( (SELECT facture_id FROM Facture WHERE planning_detail_id = 10 LIMIT 1), 10, (SELECT signalement_id FROM Signalement WHERE planning_detail_id = 10 LIMIT 1), 'Planning avancé en raison de l''urgence client.', 'Urgence client', 'Réorganisation de l''emploi du temps de l''équipe.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 11 LIMIT 1), 11, NULL, '2023-12-01 11:00:00', 'Facture émise et paiement reçu pour Nettoyage Industriel.', NULL, 'Validation de la réception du paiement.'),
-- ( (SELECT facture_id FROM Facture WHERE planning_detail_id = 14 LIMIT 1), 14, (SELECT signalement_id FROM Signalement WHERE planning_detail_id = 14 LIMIT 1), 'Facture émise, traitement décalé, en attente de paiement.', 'Report de traitement', 'Ajustement de la date de la prochaine intervention.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 19 LIMIT 1), 19, NULL, '2024-02-05 11:10:00', 'Facture émise et paiement reçu pour Désinfection.', NULL, 'Finalisation de la désinfection et rapport.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 20 LIMIT 1), 20, NULL, '2024-03-05 11:15:00', 'Facture émise, en attente de paiement.', 'Paiement en retard', 'Contact téléphonique avec le client.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 25 LIMIT 1), 25, NULL, '2024-03-15 11:20:00', 'Facture émise et paiement reçu pour Ramassage Ordures.', NULL, 'Confirmation du service effectué.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 29 LIMIT 1), 29, NULL, '2024-04-10 11:25:00', 'Facture émise et paiement reçu pour Anti termites.', NULL, 'Suivi post-traitement programmé.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 34 LIMIT 1), 34, NULL, '2024-01-15 11:30:00', 'Facture émise et paiement reçu pour Nettoyage Industriel.', NULL, 'Révision du protocole de nettoyage.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 44 LIMIT 1), 44, NULL, '2024-03-15 11:35:00', 'Facture émise et paiement reçu pour Dératisation. Nouveau client.', NULL, 'Envoi du pack de bienvenue et informations complémentaires.'),
( (SELECT facture_id FROM Facture WHERE planning_detail_id = 51 LIMIT 1), 51, NULL, '2024-06-15 11:40:00', 'Facture émise et paiement reçu pour Dératisation du nouveau client 9.', NULL, 'Suivi initial de la satisfaction client.');