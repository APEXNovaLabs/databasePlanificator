USE Planificator;

-- ---
-- 1. Client Table (Parent pour Contrat et Remarque)
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


-- ---
-- 2. TypeTraitement Table (Parent pour Traitement)
-- ---
INSERT INTO TypeTraitement (categorieTraitement, typeTraitement) VALUES
('AT: Anti termites', 'Anti termites (AT)'),
('PC', 'Dératisation (PC)'),
('PC', 'Désinfection (PC)'),
('PC', 'Désinsectisation (PC)'),
('PC', 'Fumigation (PC)'),
('NI: Nettoyage Industriel', 'Nettoyage industriel (NI)'),
('RO: Ramassage Ordures', 'Ramassage ordure');


-- ---
-- 3. Contrat Table (Enfant de Client, Parent pour Traitement)
-- ---
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


-- ---
-- 4. Traitement Table (Enfant de Contrat et TypeTraitement, Parent pour Planning)
-- ---
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
(1, 2), (1, 4), -- Client 1: Dératisation, Désinsectisation
(2, 6), -- Client 2: Nettoyage industriel
(3, 3), -- Client 3: Désinfection
(4, 7), -- Client 4: Ramassage ordure
(5, 1), (5, 6), -- Client 5: Anti termites, Nettoyage industriel
(6, 2), -- Contrat 6 (renouvellement pour Client 1): Dératisation
(7, 4), -- Client 6: Désinsectisation
(8, 2), (8, 3), -- Client 7: Dératisation, Désinfection
(9, 6), -- Client 8: Nettoyage industriel
(10, 2), (10, 4), -- Client 9: Dératisation, Désinsectisation
(11, 6), -- Client 10: Nettoyage industriel
(12, 3), -- Client 11: Désinfection
(13, 7), -- Client 12: Ramassage ordure
(14, 1), (14, 6), -- Client 13: Anti termites, Nettoyage industriel
(15, 2), -- Client 14: Dératisation
(16, 4), -- Client 15: Désinsectisation
(17, 2), (17, 3), -- Client 16: Dératisation, Désinfection
(18, 6), -- Client 17: Nettoyage industriel
(19, 7), -- Client 18: Ramassage ordure
(20, 1); -- Client 19: Anti termites


-- ---
-- 5. Planning Table (Enfant de Traitement, Parent pour PlanningDetails)
-- ---
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


-- ---
-- 6. PlanningDetails Table (Enfant de Planning, Parent pour Facture, Remarque, Signalement, Historique)
-- Note: Considérant que la date actuelle est autour de Juin 2025 pour les statuts "À venir"
-- ---
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
-- Planning 1 (mensuel)
(1, '2024-01-20', 'Effectué'), (1, '2024-02-20', 'Effectué'), (1, '2024-03-20', 'Effectué'), (1, '2024-04-20', 'Effectué'), (1, '2024-05-20', 'Effectué'), (1, '2024-06-20', 'Effectué'), (1, '2024-07-20', 'À venir'), (1, '2024-08-20', 'À venir'),
-- Planning 2 (trimestriel)
(2, '2024-01-25', 'Effectué'), (2, '2024-04-25', 'Effectué'), (2, '2024-07-25', 'À venir'),
-- Planning 3 (mensuel, indéterminé)
(3, '2023-12-01', 'Effectué'), (3, '2024-01-01', 'Effectué'), (3, '2024-02-01', 'Effectué'), (3, '2024-03-01', 'Effectué'), (3, '2024-04-01', 'Effectué'), (3, '2024-05-01', 'Effectué'), (3, '2024-06-01', 'Effectué'), (3, '2024-07-01', 'À venir'),
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
(16, '2024-06-25', 'Effectué'), (16, '2024-07-25', 'À venir'),
-- Planning 17 (bimensuel) - Client 12
(17, '2024-07-01', 'À venir'),
-- Planning 18 (semestriel, indéterminé) - Client 13
(18, '2024-07-05', 'À venir'),
-- Planning 19 (mensuel, indéterminé) - Client 13
(19, '2024-07-10', 'À venir'),
-- Planning 20 (mensuel) - Client 14
(20, '2024-07-15', 'À venir');


-- ---
-- 7. Facture Table (Enfant de PlanningDetails, Parent pour Historique_prix, Remarque, Historique)
-- ---
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


-- ---
-- 8. Historique_prix Table (Enfant de Facture)
-- ---
INSERT INTO Historique_prix (facture_id, old_amount, new_amount, change_date, changed_by) VALUES
(1, 45000, 50000, '2024-01-21 10:00:00', 'System'),
(7, 70000, 75000, '2024-01-26 11:30:00', 'System'),
(9, 140000, 150000, '2023-12-02 09:00:00', 'System');


-- ---
-- 9. Remarque Table (Enfant de Client, PlanningDetails, Facture)
-- ---
INSERT INTO Remarque (client_id, planning_detail_id, facture_id, contenu) VALUES
(1, 1, 1, 'Traitement effectué avec succès. Client satisfait.'),
(1, 2, 2, 'RAS, mission accomplie.'),
(2, 11, 9, 'Nettoyage industriel complet. Site propre.'),
(3, 19, 16, 'Désinfection effectuée, pas de problème relevé.'),
(1, 3, 3, 'Client non joignable pour le paiement.'),
(5, 29, 24, 'Intervention anti-termites complexe, mais efficace.'),
(7, 44, 36, 'Premier traitement de dératisation pour ce client, tout s''est bien passé.'),
(9, 51, 51, 'Nouveau client, premier paiement reçu.');


-- ---
-- 10. Signalement Table (Enfant de PlanningDetails, Parent pour Historique)
-- ---
INSERT INTO Signalement (planning_detail_id, motif, type) VALUES
(4, 'Retard de matériel', 'Décalage'),
(10, 'Urgence client imprévue', 'Avancement'),
(14, 'Accès au site difficile', 'Décalage'),
(23, 'Annulation de dernière minute par le client.', 'Décalage'),
(47, 'Client a demandé un avancement en raison d''un événement.', 'Avancement'),
(52, 'Problème logistique, reporté d''une semaine.', 'Décalage');


-- ---
-- 11. Historique Table (Enfant de Facture, PlanningDetails, Signalement)
-- ---
INSERT INTO Historique (facture_id, planning_detail_id, signalement_id, contenu) VALUES
(1, 1, NULL, 'Facture émise et paiement reçu pour Dératisation.'),
(2, 2, NULL, 'Facture émise et paiement reçu pour Désinsectisation.'),
(3, 3, NULL, 'Facture émise, en attente de paiement.'),
(4, 4, 1, 'Facture émise, traitement décalé, en attente de paiement.'),
(7, 8, NULL, 'Facture émise et paiement reçu pour Dératisation.'),
(8, 9, NULL, 'Facture émise, en attente de paiement.'),
(NULL, 10, 2, 'Planning avancé en raison de l''urgence client.'),
(9, 11, NULL, 'Facture émise et paiement reçu pour Nettoyage Industriel.'),
(12, 14, 3, 'Facture émise, traitement décalé, en attente de paiement.'),
(16, 19, NULL, 'Facture émise et paiement reçu pour Désinfection.'),
(17, 20, NULL, 'Facture émise, en attente de paiement.'),
(21, 25, NULL, 'Facture émise et paiement reçu pour Ramassage Ordures.'),
(24, 29, NULL, 'Facture émise et paiement reçu pour Anti termites.'),
(28, 34, NULL, 'Facture émise et paiement reçu pour Nettoyage Industriel.'),
(36, 44, NULL, 'Facture émise et paiement reçu pour Dératisation. Nouveau client.'),
(51, 51, NULL, 'Facture émise et paiement reçu pour Dératisation du nouveau client 9.');