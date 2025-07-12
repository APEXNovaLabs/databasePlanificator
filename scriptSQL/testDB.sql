USE Planificator;

-- ---
-- 1. Table Client (Parent pour Contrat et Remarque)
-- ---
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

---
--- 2. Table TypeTraitement (Parent pour Traitement)
---
INSERT INTO TypeTraitement (categorieTraitement, typeTraitement) VALUES
('AT: Anti termites', 'Anti termites (AT)'),
('PC', 'Dératisation (PC)'),
('PC', 'Désinfection (PC)'),
('PC', 'Désinsectisation (PC)'),
('PC', 'Fumigation (PC)'),
('NI: Nettoyage Industriel', 'Nettoyage industriel (NI)'),
('RO: Ramassage Ordures', 'Ramassage ordure');

---
--- 3. Table Contrat (Enfant de Client, Parent pour Traitement)
---
INSERT INTO Contrat (client_id, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
(1, '2024-01-15', '2024-01-20', '2025-01-19', 'Actif', 12, 'Déterminée', 'Nouveau'),
(2, '2023-11-20', '2023-12-01', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau'),
(3, '2024-02-01', '2024-02-05', '2024-08-04', 'Actif', 6, 'Déterminée', 'Nouveau'),
(4, '2024-03-10', '2024-03-15', '2025-03-14', 'Actif', 12, 'Déterminée', 'Nouveau'),
(5, '2023-10-05', '2023-10-10', NULL, 'Actif', NULL, 'Indeterminée', 'Renouvellement'),
(1, '2025-01-10', '2025-01-20', '2026-01-19', 'Actif', 12, 'Déterminée', 'Renouvellement'),
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

---
--- 4. Table Traitement (Enfant de Contrat et TypeTraitement, Parent pour Planning)
---
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
((SELECT contrat_id FROM Contrat WHERE client_id = 1 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 1 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 2 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 3 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 4 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')),
((SELECT contrat_id FROM Contrat WHERE client_id = 5 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 5 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 1 ORDER BY date_contrat DESC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 6 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 7 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 7 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 8 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 9 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 9 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 10 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 11 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 12 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')),
((SELECT contrat_id FROM Contrat WHERE client_id = 13 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 13 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 14 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 15 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 16 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 16 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 17 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')),
((SELECT contrat_id FROM Contrat WHERE client_id = 18 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')),
((SELECT contrat_id FROM Contrat WHERE client_id = 19 ORDER BY date_contrat ASC LIMIT 1), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)'));

---
--- 5. Table Planning (Enfant de Traitement, Parent pour PlanningDetails)
---
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(1, '2024-01-20', 1, 12, 12, 1, '2025-01-19'),
(2, '2024-01-25', 1, 12, 12, 3, '2025-01-24'),
(3, '2023-12-01', 12, 12, 0, 1, NULL),
(4, '2024-02-05', 2, 8, 6, 1, '2024-08-04'),
(5, '2024-03-15', 3, 12, 12, 2, '2025-03-14'),
(6, '2023-10-10', 10, 12, 0, 6, NULL),
(7, '2023-10-15', 10, 12, 0, 1, NULL),
(8, '2025-01-20', 1, 12, 12, 1, '2026-01-19'),
(9, '2024-05-01', 5, 11, 7, 1, '2024-11-30'),
(10, '2024-05-05', 5, 12, 12, 1, '2025-05-04'),
(11, '2024-05-10', 5, 12, 12, 3, '2025-05-09'),
(12, '2024-06-10', 6, 12, 0, 1, NULL),
(13, '2024-06-15', 6, 12, 12, 1, '2025-06-14'),
(14, '2024-06-20', 6, 12, 12, 3, '2025-06-19'),
(15, '2024-06-20', 6, 12, 0, 1, NULL),
(16, '2024-06-25', 6, 12, 6, 1, '2024-12-24'),
(17, '2024-07-01', 7, 12, 12, 2, '2025-06-30'),
(18, '2024-07-05', 7, 12, 0, 6, NULL),
(19, '2024-07-10', 7, 12, 0, 1, NULL),
(20, '2024-07-15', 7, 12, 12, 1, '2025-07-14');

---
--- 6. Table PlanningDetails (Enfant de Planning, Parent pour Facture, Remarque, Signalement, Historique)
---
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
-- Planning 1 (mensuel) - Client 1
(1, '2024-01-20', 'Effectué'), (1, '2024-02-20', 'Effectué'), (1, '2024-03-20', 'Effectué'), (1, '2024-04-20', 'Effectué'), (1, '2024-05-20', 'Effectué'), (1, '2024-06-20', 'Effectué'), (1, '2024-07-20', 'À venir'), (1, '2024-08-20', 'À venir'), (1, '2024-09-20', 'À venir'), (1, '2024-10-20', 'À venir'), (1, '2024-11-20', 'À venir'), (1, '2024-12-20', 'À venir'),
-- Planning 2 (trimestriel) - Client 1
(2, '2024-01-25', 'Effectué'), (2, '2024-04-25', 'Effectué'), (2, '2024-07-25', 'À venir'), (2, '2024-10-25', 'À venir'),
-- Planning 3 (mensuel, indéterminé) - Client 2
(3, '2023-12-01', 'Effectué'), (3, '2024-01-01', 'Effectué'), (3, '2024-02-01', 'Effectué'), (3, '2024-03-01', 'Effectué'), (3, '2024-04-01', 'Effectué'), (3, '2024-05-01', 'Effectué'), (3, '2024-06-01', 'Effectué'), (3, '2024-07-01', 'À venir'), (3, '2024-08-01', 'À venir'), (3, '2024-09-01', 'À venir'), (3, '2024-10-01', 'À venir'), (3, '2024-11-01', 'À venir'), (3, '2024-12-01', 'À venir'),
-- Planning 4 (mensuel) - Client 3
(4, '2024-02-05', 'Effectué'), (4, '2024-03-05', 'Effectué'), (4, '2024-04-05', 'Effectué'), (4, '2024-05-05', 'Effectué'), (4, '2024-06-05', 'Effectué'), (4, '2024-07-05', 'À venir'),
-- Planning 5 (bimensuel) - Client 4
(5, '2024-03-15', 'Effectué'), (5, '2024-05-15', 'Effectué'), (5, '2024-07-15', 'À venir'), (5, '2024-09-15', 'À venir'), (5, '2024-11-15', 'À venir'), (5, '2025-01-15', 'À venir'), (5, '2025-03-14', 'À venir'),
-- Planning 6 (semestriel, indéterminé) - Client 5
(6, '2023-10-10', 'Effectué'), (6, '2024-04-10', 'Effectué'), (6, '2024-10-10', 'À venir'),
-- Planning 7 (mensuel, indéterminé) - Client 5
(7, '2023-10-15', 'Effectué'), (7, '2023-11-15', 'Effectué'), (7, '2023-12-15', 'Effectué'), (7, '2024-01-15', 'Effectué'), (7, '2024-02-15', 'Effectué'), (7, '2024-03-15', 'Effectué'), (7, '2024-04-15', 'Effectué'), (7, '2024-05-15', 'Effectué'), (7, '2024-06-15', 'Effectué'), (7, '2024-07-15', 'À venir'), (7, '2024-08-15', 'À venir'), (7, '2024-09-15', 'À venir'), (7, '2024-10-15', 'À venir'), (7, '2024-11-15', 'À venir'), (7, '2024-12-15', 'À venir'),
-- Planning 8 (mensuel) - Client 1 (renouvellement)
(8, '2025-01-20', 'À venir'), (8, '2025-02-20', 'À venir'), (8, '2025-03-20', 'À venir'),
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

---
--- 7. Table Facture (Enfant de PlanningDetails, Parent pour Historique_prix, Remarque, Historique)
---
INSERT INTO Facture (planning_detail_id, montant, date_traitement, etat, axe) VALUES
-- Factures 2022
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-01-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-02-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-03-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-04-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-05-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-06-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-07-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-08-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-09-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-10-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-11-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 48000, '2022-12-20', 'Payé', 'Centre (C)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1), 70000, '2022-01-25', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1), 70000, '2022-04-25', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1), 70000, '2022-07-25', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1), 70000, '2022-10-25', 'Payé', 'Centre (C)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-01-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-02-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-03-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-04-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-05-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-06-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-07-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-08-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-09-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-10-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-11-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 145000, '2022-12-01', 'Payé', 'Nord (N)'),

-- Factures 2023-2024
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), 50000, '2024-01-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-02-20' LIMIT 1), 50000, '2024-02-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-03-20' LIMIT 1), 50000, '2024-03-20', 'Non payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-04-20' LIMIT 1), 50000, '2024-04-20', 'Non payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-05-20' LIMIT 1), 50000, '2024-05-20', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-06-20' LIMIT 1), 50000, '2024-06-20', 'Non payé', 'Centre (C)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1), 75000, '2024-01-25', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-04-25' LIMIT 1), 75000, '2024-04-25', 'Non payé', 'Centre (C)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), 150000, '2023-12-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2024-01-01' LIMIT 1), 150000, '2024-01-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2024-02-01' LIMIT 1), 150000, '2024-02-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2024-03-01' LIMIT 1), 150000, '2024-03-01', 'Non payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2024-04-01' LIMIT 1), 150000, '2024-04-01', 'Non payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2024-05-01' LIMIT 1), 150000, '2024-05-01', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2024-06-01' LIMIT 1), 150000, '2024-06-01', 'Non payé', 'Nord (N)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-02-05' LIMIT 1), 60000, '2024-02-05', 'Payé', 'Sud (S)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-03-05' LIMIT 1), 60000, '2024-03-05', 'Non payé', 'Sud (S)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-04-05' LIMIT 1), 60000, '2024-04-05', 'Non payé', 'Sud (S)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-05-05' LIMIT 1), 60000, '2024-05-05', 'Payé', 'Sud (S)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-06-05' LIMIT 1), 60000, '2024-06-05', 'Non payé', 'Sud (S)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 5 AND date_planification = '2024-03-15' LIMIT 1), 100000, '2024-03-15', 'Payé', 'Est (E)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 5 AND date_planification = '2024-05-15' LIMIT 1), 100000, '2024-05-15', 'Non payé', 'Est (E)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 6 AND date_planification = '2023-10-10' LIMIT 1), 200000, '2023-10-10', 'Payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 6 AND date_planification = '2024-04-10' LIMIT 1), 200000, '2024-04-10', 'Non payé', 'Ouest (O)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 7 AND date_planification = '2023-10-15' LIMIT 1), 180000, '2023-10-15', 'Payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 7 AND date_planification = '2023-11-15' LIMIT 1), 180000, '2023-11-15', 'Payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 7 AND date_planification = '2023-12-15' LIMIT 1), 180000, '2023-12-15', 'Payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 7 AND date_planification = '2024-01-15' LIMIT 1), 180000, '2024-01-15', 'Payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 7 AND date_planification = '2024-02-15' LIMIT 1), 180000, '2024-02-15', 'Payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 7 AND date_planification = '2024-03-15' LIMIT 1), 180000, '2024-03-15', 'Non payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 7 AND date_planification = '2024-04-15' LIMIT 1), 180000, '2024-04-15', 'Non payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 7 AND date_planification = '2024-05-15' LIMIT 1), 180000, '2024-05-15', 'Payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 7 AND date_planification = '2024-06-15' LIMIT 1), 180000, '2024-06-15', 'Non payé', 'Ouest (O)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 9 AND date_planification = '2024-05-01' LIMIT 1), 65000, '2024-05-01', 'Payé', 'Sud (S)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 9 AND date_planification = '2024-06-01' LIMIT 1), 65000, '2024-06-01', 'Non payé', 'Sud (S)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 10 AND date_planification = '2024-05-05' LIMIT 1), 55000, '2024-05-05', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 10 AND date_planification = '2024-06-05' LIMIT 1), 55000, '2024-06-05', 'Non payé', 'Nord (N)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 12 AND date_planification = '2024-06-10' LIMIT 1), 160000, '2024-06-10', 'Non payé', 'Sud (S)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 13 AND date_planification = '2024-06-15' LIMIT 1), 50000, '2024-06-15', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 14 AND date_planification = '2024-06-20' LIMIT 1), 75000, '2024-06-20', 'Non payé', 'Nord (N)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 15 AND date_planification = '2024-06-20' LIMIT 1), 150000, '2024-06-20', 'Payé', 'Centre (C)'),

((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 16 AND date_planification = '2024-06-25' LIMIT 1), 60000, '2024-06-25', 'Payé', 'Sud (S)');

---
--- 8. Table Historique_prix (Enfant de Facture)
---
INSERT INTO Historique_prix (facture_id, old_amount, new_amount, change_date, changed_by) VALUES
((SELECT f.facture_id FROM Facture f JOIN PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id WHERE pd.planning_id = 1 AND f.date_traitement = '2024-01-20' LIMIT 1), 45000, 50000, '2024-01-21 10:00:00', 'System'),
((SELECT f.facture_id FROM Facture f JOIN PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id WHERE pd.planning_id = 2 AND f.date_traitement = '2024-01-25' LIMIT 1), 70000, 75000, '2024-01-26 11:30:00', 'System'),
((SELECT f.facture_id FROM Facture f JOIN PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id WHERE pd.planning_id = 3 AND f.date_traitement = '2023-12-01' LIMIT 1), 140000, 150000, '2023-12-02 09:00:00', 'System'),
((SELECT f.facture_id FROM Facture f JOIN PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id WHERE pd.planning_id = 1 AND f.date_traitement = '2022-01-20' LIMIT 1), 47000, 48000, '2022-01-21 10:00:00', 'Admin'),
((SELECT f.facture_id FROM Facture f JOIN PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id WHERE pd.planning_id = 3 AND f.date_traitement = '2022-03-01' LIMIT 1), 140000, 145000, '2022-03-02 09:00:00', 'Admin');


--- 9. Table Remarque (Enfant de Client, PlanningDetails, Facture)

INSERT INTO Remarque (client_id, planning_detail_id, facture_id, contenu, issue, action) VALUES
(1, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1) AND date_traitement = '2024-01-20' LIMIT 1), 'Traitement effectué avec succès. Client satisfait.', NULL, 'Vérification post-traitement confirmée.'),
(1, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-02-20' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-02-20' LIMIT 1) AND date_traitement = '2024-02-20' LIMIT 1), 'RAS, mission accomplie.', NULL, 'Rapport de fin d''intervention soumis.'),
(2, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1) AND date_traitement = '2023-12-01' LIMIT 1), 'Nettoyage industriel complet. Site propre.', NULL, 'Inspection visuelle et rapport de conformité.'),
(3, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-02-05' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-02-05' LIMIT 1) AND date_traitement = '2024-02-05' LIMIT 1), 'Désinfection effectuée, pas de problème relevé.', NULL, 'Suivi protocolaire de désinfection appliqué.'),
(1, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-03-20' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-03-20' LIMIT 1) AND date_traitement = '2024-03-20' LIMIT 1), 'Client non joignable pour le paiement.', 'Difficulté de communication', 'Relance téléphonique et envoi de mail.'),
(5, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 6 AND date_planification = '2024-04-10' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 6 AND date_planification = '2024-04-10' LIMIT 1) AND date_traitement = '2024-04-10' LIMIT 1), 'Intervention anti-termites complexe, mais efficace.', 'Accès difficile à certaines zones', 'Utilisation d''équipement spécialisé pour l''accès.'),
(7, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 10 AND date_planification = '2024-05-05' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 10 AND date_planification = '2024-05-05' LIMIT 1) AND date_traitement = '2024-05-05' LIMIT 1), 'Premier traitement de dératisation pour ce client, tout s''est bien passé.', NULL, 'Conseils de prévention fournis au client.'),
(9, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 13 AND date_planification = '2024-06-15' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 13 AND date_planification = '2024-06-15' LIMIT 1) AND date_traitement = '2024-06-15' LIMIT 1), 'Nouveau client, premier paiement reçu.', NULL, 'Confirmation de paiement et enregistrement.');

-- Remarques pour les traitements de 2022
INSERT INTO Remarque (client_id, planning_detail_id, facture_id, contenu, issue, action) VALUES
(1, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1) AND date_traitement = '2022-01-20' LIMIT 1), 'Traitement de routine effectué. Tout est conforme.', NULL, 'Vérification de l''équipement.'),
(1, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1) AND date_traitement = '2022-07-20' LIMIT 1), 'Léger retard dû au trafic, mais intervention terminée dans les délais.', 'Retard logistique mineur', 'Optimisation des itinéraires de déplacement.'),
(2, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1) AND date_traitement = '2022-05-01' LIMIT 1), 'Nettoyage impeccable. Client a fait un retour positif.', NULL, 'Envoi d''une enquête de satisfaction.'),
(2, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1) AND date_traitement = '2022-11-01' LIMIT 1), 'Problème de disponibilité du personnel résolu. Intervention reprogrammée et effectuée.', 'Manque de personnel disponible', 'Planification des ressources améliorée.'),
(1, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1) AND date_traitement = '2022-04-25' LIMIT 1), 'Contrôle qualité effectué. Pas de signes de nuisibles.', NULL, 'Rapport de suivi envoyé.'),
(1, (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1), (SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1) AND date_traitement = '2022-10-25' LIMIT 1), 'Matériel manquant lors de l''intervention.', 'Oubli de matériel', 'Vérification de la checklist avant départ.');


--- 10. Table Signalement (Enfant de PlanningDetails, Parent pour Historique)

INSERT INTO Signalement (planning_detail_id, motif, type) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-04-05' LIMIT 1), 'Retard de matériel', 'Décalage'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 10 AND date_planification = '2024-06-05' LIMIT 1), 'Urgence client imprévue', 'Avancement'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 14 AND date_planification = '2024-06-20' LIMIT 1), 'Accès au site difficile', 'Décalage'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-06-05' LIMIT 1), 'Annulation de dernière minute par le client.', 'Décalage'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 11 AND date_planification = '2024-05-10' LIMIT 1), 'Client a demandé un avancement en raison d''un événement.', 'Avancement'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 13 AND date_planification = '2024-07-15' LIMIT 1), 'Problème logistique, reporté d''une semaine.', 'Décalage');


--- 11. Table Historique (Enfant de Facture, PlanningDetails, Signalement)

INSERT INTO Historique (facture_id, planning_detail_id, signalement_id, date_historique, contenu, issue, action) VALUES
-- Historique 2024
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1) AND date_traitement = '2024-01-20' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), NULL, '2024-01-20 10:00:00', 'Facture émise et paiement reçu pour Dératisation.', NULL, 'Enregistrement du paiement et fermeture du dossier.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-02-20' LIMIT 1) AND date_traitement = '2024-02-20' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-02-20' LIMIT 1), NULL, '2024-02-20 10:05:00', 'Facture émise et paiement reçu pour Désinsectisation.', NULL, 'Archivage de la facture et confirmation client.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-03-20' LIMIT 1) AND date_traitement = '2024-03-20' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-03-20' LIMIT 1), NULL, '2024-03-20 10:10:00', 'Facture émise, en attente de paiement.', 'Paiement en attente', 'Envoi d''une première relance.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-04-20' LIMIT 1) AND date_traitement = '2024-04-20' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-04-20' LIMIT 1), (SELECT signalement_id FROM Signalement WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-04-05' LIMIT 1) LIMIT 1), 'Facture émise, traitement décalé, en attente de paiement.', 'Décalage traitement', 'Mise à jour du planning et suivi de facture.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1) AND date_traitement = '2024-01-25' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1), NULL, '2024-01-25 10:20:00', 'Facture émise et paiement reçu pour Dératisation.', NULL, 'Confirmation de la prestation et clôture.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-04-25' LIMIT 1) AND date_traitement = '2024-04-25' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-04-25' LIMIT 1), NULL, '2024-04-25 10:25:00', 'Facture émise, en attente de paiement.', 'Paiement en attente', 'Envoi d''une deuxième relance.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 10 AND date_planification = '2024-06-05' LIMIT 1) AND date_traitement = '2024-06-05' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 10 AND date_planification = '2024-06-05' LIMIT 1), (SELECT signalement_id FROM Signalement WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 10 AND date_planification = '2024-06-05' LIMIT 1) LIMIT 1), 'Planning avancé en raison de l''urgence client.', 'Urgence client', 'Réorganisation de l''emploi du temps de l''équipe.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1) AND date_traitement = '2023-12-01' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), NULL, '2023-12-01 11:00:00', 'Facture émise et paiement reçu pour Nettoyage Industriel.', NULL, 'Validation de la réception du paiement.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 14 AND date_planification = '2024-06-20' LIMIT 1) AND date_traitement = '2024-06-20' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 14 AND date_planification = '2024-06-20' LIMIT 1), (SELECT signalement_id FROM Signalement WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 14 AND date_planification = '2024-06-20' LIMIT 1) LIMIT 1), 'Facture émise, traitement décalé, en attente de paiement.', 'Report de traitement', 'Ajustement de la date de la prochaine intervention.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-02-05' LIMIT 1) AND date_traitement = '2024-02-05' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-02-05' LIMIT 1), NULL, '2024-02-05 11:10:00', 'Facture émise et paiement reçu pour Désinfection.', NULL, 'Finalisation de la désinfection et rapport.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-03-05' LIMIT 1) AND date_traitement = '2024-03-05' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 4 AND date_planification = '2024-03-05' LIMIT 1), NULL, '2024-03-05 11:15:00', 'Facture émise, en attente de paiement.', 'Paiement en retard', 'Contact téléphonique avec le client.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 5 AND date_planification = '2024-03-15' LIMIT 1) AND date_traitement = '2024-03-15' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 5 AND date_planification = '2024-03-15' LIMIT 1), NULL, '2024-03-15 11:20:00', 'Facture émise et paiement reçu pour Ramassage Ordures.', NULL, 'Confirmation du service effectué.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 6 AND date_planification = '2024-04-10' LIMIT 1) AND date_traitement = '2024-04-10' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 6 AND date_planification = '2024-04-10' LIMIT 1), NULL, '2024-04-10 11:25:00', 'Facture émise et paiement reçu pour Anti termites.', NULL, 'Suivi post-traitement programmé.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 7 AND date_planification = '2024-01-15' LIMIT 1) AND date_traitement = '2024-01-15' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 7 AND date_planification = '2024-01-15' LIMIT 1), NULL, '2024-01-15 11:30:00', 'Facture émise et paiement reçu pour Nettoyage Industriel.', NULL, 'Révision du protocole de nettoyage.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 10 AND date_planification = '2024-05-05' LIMIT 1) AND date_traitement = '2024-05-05' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 10 AND date_planification = '2024-05-05' LIMIT 1), NULL, '2024-03-15 11:35:00', 'Facture émise et paiement reçu pour Dératisation. Nouveau client.', NULL, 'Envoi du pack de bienvenue et informations complémentaires.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 13 AND date_planification = '2024-06-15' LIMIT 1) AND date_traitement = '2024-06-15' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 13 AND date_planification = '2024-06-15' LIMIT 1), NULL, '2024-06-15 11:40:00', 'Facture émise et paiement reçu pour Dératisation du nouveau client 9.', NULL, 'Suivi initial de la satisfaction client.');

-- Historique pour les traitements de 2022
INSERT INTO Historique (facture_id, planning_detail_id, signalement_id, date_historique, contenu, issue, action) VALUES
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1) AND date_traitement = '2022-01-20' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), NULL, '2022-01-20 10:00:00', 'Traitement mensuel effectué et facturé.', NULL, 'Vérification de routine.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1) AND date_traitement = '2022-07-20' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 1 AND date_planification = '2024-01-20' LIMIT 1), NULL, '2022-07-20 09:30:00', 'Traitement réalisé malgré un léger retard.', 'Retard sur le planning', 'Alerte logistique envoyée.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1) AND date_traitement = '2022-05-01' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), NULL, '2022-05-01 14:00:00', 'Nettoyage industriel terminé. Client satisfait.', NULL, 'Rapport de fin de chantier.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1) AND date_traitement = '2022-11-01' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 3 AND date_planification = '2023-12-01' LIMIT 1), NULL, '2022-11-01 10:45:00', 'Intervention de nettoyage reprogrammée effectuée.', 'Problème de disponibilité équipe', 'Planification ajustée.'),
((SELECT facture_id FROM Facture WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1) AND date_traitement = '2022-04-25' LIMIT 1), (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = 2 AND date_planification = '2024-01-25' LIMIT 1), NULL, '2022-04-25 11:00:00', 'Contrôle trimestriel de dératisation. RAS.', NULL, 'Rapport de conformité.');