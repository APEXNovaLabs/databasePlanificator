USE Planificator;

-- Insertion des clients (5 clients: 2 Particuliers, 2 Organisations, 1 Société)
INSERT INTO Client (nom, prenom, email, telephone, adresse, nif, stat, date_ajout, categorie, axe) VALUES
('Dupont', 'Jean', 'jean.dupont@example.com', '0341234567', '12 Rue des Fleurs, Antananarivo', NULL, NULL, '2023-01-15', 'Particulier', 'Centre (C)'),
('Martin', 'Sophie', 'sophie.martin@example.com', '0327654321', '25 Avenue de la Liberté, Antananarivo', NULL, NULL, '2023-03-20', 'Particulier', 'Est (E)'),
('GlobalCorp', NULL, 'contact@globalcorp.com', '0339876543', '45 Boulevard de l''Indépendance, Antananarivo', NULL, NULL, '2023-05-10', 'Organisation', 'Nord (N)'),
('EcoSolutions', NULL, 'info@ecosolutions.org', '0345678901', '8 Rue des Palmiers, Antananarivo', NULL, NULL, '2024-02-28', 'Organisation', 'Ouest (O)'),
('TechInnov SARL', NULL, 'admin@techinnov.mg', '0321122334', '60 Route Circulaire, Antananarivo', '1234567890', 'A123B456C789', '2024-07-01', 'Société', 'Sud (S)');

-- Insertion des contrats (3 par client)
-- Client 1: Dupont Jean (Particulier)
INSERT INTO Contrat (client_id, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
((SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean'), '2023-01-15', '2023-02-01', '2024-01-31', 'Terminé', 12, 'Déterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean'), '2024-01-20', '2024-02-01', '2025-01-31', 'Actif', 12, 'Déterminée', 'Renouvellement'),
((SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean'), '2025-02-05', '2025-03-01', '2026-02-28', 'Actif', 12, 'Déterminée', 'Renouvellement');

-- Client 2: Martin Sophie (Particulier)
INSERT INTO Contrat (client_id, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
((SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie'), '2023-03-20', '2023-04-01', '2024-03-31', 'Terminé', 12, 'Déterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie'), '2024-03-10', '2024-04-01', '2025-03-31', 'Actif', 12, 'Déterminée', 'Renouvellement'),
((SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie'), '2025-04-01', '2025-04-01', '2025-04-01', 'Actif', NULL, 'Indeterminée', 'Renouvellement');

-- Client 3: GlobalCorp (Organisation)
INSERT INTO Contrat (client_id, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
((SELECT client_id FROM Client WHERE nom = 'GlobalCorp'), '2023-05-10', '2023-06-01', '2024-05-31', 'Terminé', 12, 'Déterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'GlobalCorp'), '2024-05-01', '2024-06-01', NULL, 'Actif', NULL, 'Indeterminée', 'Renouvellement'),
((SELECT client_id FROM Client WHERE nom = 'GlobalCorp'), '2025-01-01', '2025-01-01', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau');

-- Client 4: EcoSolutions (Organisation)
INSERT INTO Contrat (client_id, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
((SELECT client_id FROM Client WHERE nom = 'EcoSolutions'), '2024-02-28', '2024-03-10', '2025-03-09', 'Actif', 12, 'Déterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'EcoSolutions'), '2025-03-01', '2025-03-10', NULL, 'Actif', NULL, 'Indeterminée', 'Renouvellement'),
((SELECT client_id FROM Client WHERE nom = 'EcoSolutions'), '2025-06-15', '2025-07-01', '2026-06-30', 'Actif', 12, 'Déterminée', 'Nouveau');

-- Client 5: TechInnov SARL (Société)
INSERT INTO Contrat (client_id, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
((SELECT client_id FROM Client WHERE nom = 'TechInnov SARL'), '2024-07-01', '2024-07-15', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'TechInnov SARL'), '2024-08-01', '2024-08-01', '2025-07-31', 'Actif', 12, 'Déterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'TechInnov SARL'), '2025-01-20', '2025-02-01', NULL, 'Actif', NULL, 'Indeterminée', 'Renouvellement');

-- Insertion des types de traitement (si non déjà présents)
-- Assurez-vous que ces IDs correspondent à votre table TypeTraitement.
-- Voici les insertions pour s'assurer que les types de traitement existent avant de les référencer.
-- Si ces valeurs existent déjà, ces INSERTs échoueront ou n'auront pas d'effet selon votre configuration (e.g. IGNORE, ON DUPLICATE KEY UPDATE)
-- Pour éviter des erreurs si la table est vide ou si des entrées manquent :
INSERT IGNORE INTO TypeTraitement (typeTraitement) VALUES
('Dératisation (PC)'),
('Désinfection (PC)'),
('Désinsectisation (PC)'),
('Fumigation (PC)'),
('Nettoyage industriel (NI)'),
('Anti termites (AT)'),
('Ramassage ordure');

-- Insertion des traitements (3 par client)
-- Client 1: Dupont Jean
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2023-01-15'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2023-01-15'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2024-01-20'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2024-01-20'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2025-02-05'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2025-02-05'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure'));

-- Client 2: Martin Sophie
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2023-03-20'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2023-03-20'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2024-03-10'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2024-03-10'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2025-04-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2025-04-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)'));

-- Client 3: GlobalCorp
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2023-05-10'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2023-05-10'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2024-05-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2024-05-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2025-01-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2025-01-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)'));

-- Client 4: EcoSolutions
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2024-02-28'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2024-02-28'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2025-03-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2025-03-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2025-06-15'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2025-06-15'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)'));

-- Client 5: TechInnov SARL
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2024-07-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2024-07-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2024-08-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2024-08-01'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2025-01-20'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')),
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2025-01-20'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)'));


-- Insertion des plannings et détails de planification
-- Pour simplifier, je vais générer des plannings mensuels pour la plupart des traitements.
-- La date actuelle est le 13 juillet 2025.

-- Client 1: Dupont Jean
-- Contrat 1 (2023-01-15): Dératisation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2023-01-15') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')), '2023-02-01', 2, 1, 12, 1, '2024-01-31');
SET @planning_id_dupont_derat_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_derat_2023, '2023-02-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2023-03-01', 'Effectué'),
(@planning_id_dupont_derat_2023, '2023-04-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2023-05-01', 'Effectué'),
(@planning_id_dupont_derat_2023, '2023-06-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2023-07-01', 'Effectué'),
(@planning_id_dupont_derat_2023, '2023-08-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2023-09-01', 'Effectué'),
(@planning_id_dupont_derat_2023, '2023-10-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2023-11-01', 'Effectué'),
(@planning_id_dupont_derat_2023, '2023-12-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2024-01-01', 'Effectué');

-- Contrat 1 (2023-01-15): Désinfection (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2023-01-15') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')), '2023-02-15', 2, 1, 12, 3, '2024-01-15'); -- Trimestriel
SET @planning_id_dupont_desinf_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_desinf_2023, '2023-02-15', 'Effectué'), (@planning_id_dupont_desinf_2023, '2023-05-15', 'Effectué'),
(@planning_id_dupont_desinf_2023, '2023-08-15', 'Effectué'), (@planning_id_dupont_desinf_2023, '2023-11-15', 'Effectué'),
(@planning_id_dupont_desinf_2023, '2024-02-15', 'Effectué');

-- Contrat 2 (2024-01-20): Désinsectisation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2024-01-20') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')), '2024-02-05', 2, 1, 12, 1, '2025-01-31');
SET @planning_id_dupont_desins_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_desins_2024, '2024-02-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2024-03-05', 'Effectué'),
(@planning_id_dupont_desins_2024, '2024-04-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2024-05-05', 'Effectué'),
(@planning_id_dupont_desins_2024, '2024-06-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2024-07-05', 'Effectué'),
(@planning_id_dupont_desins_2024, '2024-08-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2024-09-05', 'Effectué'),
(@planning_id_dupont_desins_2024, '2024-10-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2024-11-05', 'Effectué'),
(@planning_id_dupont_desins_2024, '2024-12-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2025-01-05', 'Effectué');

-- Contrat 2 (2024-01-20): Nettoyage industriel (NI)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2024-01-20') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')), '2024-02-10', 2, 1, 12, 1, '2025-01-31');
SET @planning_id_dupont_nettoyage_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_nettoyage_2024, '2024-02-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2024-03-10', 'Effectué'),
(@planning_id_dupont_nettoyage_2024, '2024-04-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2024-05-10', 'Effectué'),
(@planning_id_dupont_nettoyage_2024, '2024-06-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2024-07-10', 'Effectué'),
(@planning_id_dupont_nettoyage_2024, '2024-08-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2024-09-10', 'Effectué'),
(@planning_id_dupont_nettoyage_2024, '2024-10-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2024-11-10', 'Effectué'),
(@planning_id_dupont_nettoyage_2024, '2024-12-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2025-01-10', 'Effectué');

-- Contrat 3 (2025-02-05): Anti termites (AT)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2025-02-05') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)')), '2025-03-01', 3, 2, 12, 6, '2026-02-28'); -- Semestriel
SET @planning_id_dupont_termites_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_termites_2025, '2025-03-01', 'Effectué'), (@planning_id_dupont_termites_2025, '2025-09-01', 'À venir'),
(@planning_id_dupont_termites_2025, '2026-03-01', 'À venir');

-- Contrat 3 (2025-02-05): Ramassage ordure (RO)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND date_contrat = '2025-02-05') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')), '2025-03-10', 3, 2, 12, 2, '2026-02-28'); -- Bimensuel
SET @planning_id_dupont_ordure_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_ordure_2025, '2025-03-10', 'Effectué'), (@planning_id_dupont_ordure_2025, '2025-05-10', 'Effectué'),
(@planning_id_dupont_ordure_2025, '2025-07-10', 'Effectué'), -- Date actuelle est le 13/07/2025, donc effectué
(@planning_id_dupont_ordure_2025, '2025-09-10', 'À venir'), (@planning_id_dupont_ordure_2025, '2025-11-10', 'À venir'),
(@planning_id_dupont_ordure_2025, '2026-01-10', 'À venir');

-- Client 2: Martin Sophie
-- Contrat 1 (2023-03-20): Désinsectisation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2023-03-20') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')), '2023-04-01', 4, 3, 12, 1, '2024-03-31');
SET @planning_id_martin_desins_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_desins_2023, '2023-04-01', 'Effectué'), (@planning_id_martin_desins_2023, '2023-05-01', 'Effectué'),
(@planning_id_martin_desins_2023, '2023-06-01', 'Effectué'), (@planning_id_martin_desins_2023, '2023-07-01', 'Effectué'),
(@planning_id_martin_desins_2023, '2023-08-01', 'Effectué'), (@planning_id_martin_desins_2023, '2023-09-01', 'Effectué'),
(@planning_id_martin_desins_2023, '2023-10-01', 'Effectué'), (@planning_id_martin_desins_2023, '2023-11-01', 'Effectué'),
(@planning_id_martin_desins_2023, '2023-12-01', 'Effectué'), (@planning_id_martin_desins_2023, '2024-01-01', 'Effectué'),
(@planning_id_martin_desins_2023, '2024-02-01', 'Effectué'), (@planning_id_martin_desins_2023, '2024-03-01', 'Effectué');

-- Contrat 1 (2023-03-20): Fumigation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2023-03-20') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)')), '2023-04-15', 4, 3, 12, 4, '2024-03-15'); -- Trimestriel
SET @planning_id_martin_fumigation_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_fumigation_2023, '2023-04-15', 'Effectué'), (@planning_id_martin_fumigation_2023, '2023-07-15', 'Effectué'),
(@planning_id_martin_fumigation_2023, '2023-10-15', 'Effectué'), (@planning_id_martin_fumigation_2023, '2024-01-15', 'Effectué');

-- Contrat 2 (2024-03-10): Dératisation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2024-03-10') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')), '2024-04-05', 4, 3, 12, 1, '2025-03-31');
SET @planning_id_martin_derat_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_derat_2024, '2024-04-05', 'Effectué'), (@planning_id_martin_derat_2024, '2024-05-05', 'Effectué'),
(@planning_id_martin_derat_2024, '2024-06-05', 'Effectué'), (@planning_id_martin_derat_2024, '2024-07-05', 'Effectué'),
(@planning_id_martin_derat_2024, '2024-08-05', 'Effectué'), (@planning_id_martin_derat_2024, '2024-09-05', 'Effectué'),
(@planning_id_martin_derat_2024, '2024-10-05', 'Effectué'), (@planning_id_martin_derat_2024, '2024-11-05', 'Effectué'),
(@planning_id_martin_derat_2024, '2024-12-05', 'Effectué'), (@planning_id_martin_derat_2024, '2025-01-05', 'Effectué'),
(@planning_id_martin_derat_2024, '2025-02-05', 'Effectué'), (@planning_id_martin_derat_2024, '2025-03-05', 'Effectué');

-- Contrat 2 (2024-03-10): Nettoyage industriel (NI)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2024-03-10') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')), '2024-04-10', 4, 3, 12, 1, '2025-03-31');
SET @planning_id_martin_nettoyage_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_nettoyage_2024, '2024-04-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2024-05-10', 'Effectué'),
(@planning_id_martin_nettoyage_2024, '2024-06-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2024-07-10', 'Effectué'),
(@planning_id_martin_nettoyage_2024, '2024-08-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2024-09-10', 'Effectué'),
(@planning_id_martin_nettoyage_2024, '2024-10-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2024-11-10', 'Effectué'),
(@planning_id_martin_nettoyage_2024, '2024-12-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2025-01-10', 'Effectué'),
(@planning_id_martin_nettoyage_2024, '2025-02-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2025-03-10', 'Effectué');

-- Contrat 3 (2025-04-01): Ramassage ordure (RO)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2025-04-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')), '2025-04-01', 4, 3, 12, 1, '2026-03-31');
SET @planning_id_martin_ordure_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_ordure_2025, '2025-04-01', 'Effectué'), (@planning_id_martin_ordure_2025, '2025-05-01', 'Effectué'),
(@planning_id_martin_ordure_2025, '2025-06-01', 'Effectué'), (@planning_id_martin_ordure_2025, '2025-07-01', 'Effectué'),
(@planning_id_martin_ordure_2025, '2025-08-01', 'À venir'), (@planning_id_martin_ordure_2025, '2025-09-01', 'À venir'),
(@planning_id_martin_ordure_2025, '2025-10-01', 'À venir'), (@planning_id_martin_ordure_2025, '2025-11-01', 'À venir'),
(@planning_id_martin_ordure_2025, '2025-12-01', 'À venir'), (@planning_id_martin_ordure_2025, '2026-01-01', 'À venir'),
(@planning_id_martin_ordure_2025, '2026-02-01', 'À venir'), (@planning_id_martin_ordure_2025, '2026-03-01', 'À venir');

-- Contrat 3 (2025-04-01): Désinfection (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND date_contrat = '2025-04-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')), '2025-04-20', 4, 3, 12, 4, '2026-03-20'); -- Trimestriel
SET @planning_id_martin_desinf_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_desinf_2025, '2025-04-20', 'Effectué'), (@planning_id_martin_desinf_2025, '2025-07-20', 'À venir'),
(@planning_id_martin_desinf_2025, '2025-10-20', 'À venir'), (@planning_id_martin_desinf_2025, '2026-01-20', 'À venir');

-- Client 3: GlobalCorp (Organisation)
-- Contrat 1 (2023-05-10): Nettoyage industriel (NI)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2023-05-10') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')), '2023-06-01', 6, 5, 12, 1, '2024-05-31');
SET @planning_id_globalcorp_nettoyage_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_nettoyage_2023, '2023-06-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2023-07-01', 'Effectué'),
(@planning_id_globalcorp_nettoyage_2023, '2023-08-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2023-09-01', 'Effectué'),
(@planning_id_globalcorp_nettoyage_2023, '2023-10-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2023-11-01', 'Effectué'),
(@planning_id_globalcorp_nettoyage_2023, '2023-12-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2024-01-01', 'Effectué'),
(@planning_id_globalcorp_nettoyage_2023, '2024-02-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2024-03-01', 'Effectué'),
(@planning_id_globalcorp_nettoyage_2023, '2024-04-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2024-05-01', 'Effectué');

-- Contrat 1 (2023-05-10): Ramassage ordure (RO)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2023-05-10') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')), '2023-06-15', 6, 5, 12, 2, '2024-05-15'); -- Bimensuel
SET @planning_id_globalcorp_ordure_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_ordure_2023, '2023-06-15', 'Effectué'), (@planning_id_globalcorp_ordure_2023, '2023-08-15', 'Effectué'),
(@planning_id_globalcorp_ordure_2023, '2023-10-15', 'Effectué'), (@planning_id_globalcorp_ordure_2023, '2023-12-15', 'Effectué'),
(@planning_id_globalcorp_ordure_2023, '2024-02-15', 'Effectué'), (@planning_id_globalcorp_ordure_2023, '2024-04-15', 'Effectué');

-- Contrat 2 (2024-05-01): Dératisation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2024-05-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')), '2024-06-05', 6, 5, 12, 1, '2025-05-31');
SET @planning_id_globalcorp_derat_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_derat_2024, '2024-06-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2024-07-05', 'Effectué'),
(@planning_id_globalcorp_derat_2024, '2024-08-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2024-09-05', 'Effectué'),
(@planning_id_globalcorp_derat_2024, '2024-10-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2024-11-05', 'Effectué'),
(@planning_id_globalcorp_derat_2024, '2024-12-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2025-01-05', 'Effectué'),
(@planning_id_globalcorp_derat_2024, '2025-02-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2025-03-05', 'Effectué'),
(@planning_id_globalcorp_derat_2024, '2025-04-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2025-05-05', 'Effectué');

-- Contrat 2 (2024-05-01): Désinsectisation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2024-05-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')), '2024-06-10', 6, 5, 12, 1, '2025-05-31');
SET @planning_id_globalcorp_desins_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_desins_2024, '2024-06-10', 'Effectué'), (@planning_id_globalcorp_desins_2024, '2024-07-10', 'Effectué'),
(@planning_id_globalcorp_desins_2024, '2024-08-10', 'Effectué'), (@planning_id_globalcorp_desins_2024, '2024-09-10', 'Effectué'),
(@planning_id_globalcorp_desins_2024, '2024-10-10', 'Effectué'), (@planning_id_globalcorp_desins_2024, '2024-11-10', 'Effectué'),
(@planning_id_globalcorp_desins_2024, '2024-12-10', 'Effectué'), (@planning_id_globalcorp_desins_2024, '2025-01-10', 'Effectué'),
(@planning_id_globalcorp_desins_2024, '2025-02-10', 'Effectué'), (@planning_id_globalcorp_desins_2024, '2025-03-10', 'Effectué'),
(@planning_id_globalcorp_desins_2024, '2025-04-10', 'Effectué'), (@planning_id_globalcorp_desins_2024, '2025-05-10', 'Effectué');

-- Contrat 3 (2025-01-01): Anti termites (AT)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2025-01-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)')), '2025-01-20', 1, 12, 12, 6, '2026-01-20'); -- Semestriel
SET @planning_id_globalcorp_termites_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_termites_2025, '2025-01-20', 'Effectué'), (@planning_id_globalcorp_termites_2025, '2025-07-20', 'À venir'),
(@planning_id_globalcorp_termites_2025, '2026-01-20', 'À venir');

-- Contrat 3 (2025-01-01): Fumigation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND date_contrat = '2025-01-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)')), '2025-02-01', 2, 1, 12, 4, '2026-01-31'); -- Trimestriel
SET @planning_id_globalcorp_fumigation_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_fumigation_2025, '2025-02-01', 'Effectué'), (@planning_id_globalcorp_fumigation_2025, '2025-05-01', 'Effectué'),
(@planning_id_globalcorp_fumigation_2025, '2025-08-01', 'À venir'), (@planning_id_globalcorp_fumigation_2025, '2025-11-01', 'À venir'),
(@planning_id_globalcorp_fumigation_2025, '2026-02-01', 'À venir');

-- Client 4: EcoSolutions (Organisation)
-- Contrat 1 (2024-02-28): Désinfection (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2024-02-28') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')), '2024-03-10', 3, 2, 12, 1, '2025-02-28');
SET @planning_id_ecosolutions_desinf_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosolutions_desinf_2024, '2024-03-10', 'Effectué'), (@planning_id_ecosolutions_desinf_2024, '2024-04-10', 'Effectué'),
(@planning_id_ecosolutions_desinf_2024, '2024-05-10', 'Effectué'), (@planning_id_ecosolutions_desinf_2024, '2024-06-10', 'Effectué'),
(@planning_id_ecosolutions_desinf_2024, '2024-07-10', 'Effectué'), (@planning_id_ecosolutions_desinf_2024, '2024-08-10', 'Effectué'),
(@planning_id_ecosolutions_desinf_2024, '2024-09-10', 'Effectué'), (@planning_id_ecosolutions_desinf_2024, '2024-10-10', 'Effectué'),
(@planning_id_ecosolutions_desinf_2024, '2024-11-10', 'Effectué'), (@planning_id_ecosolutions_desinf_2024, '2024-12-10', 'Effectué'),
(@planning_id_ecosolutions_desinf_2024, '2025-01-10', 'Effectué'), (@planning_id_ecosolutions_desinf_2024, '2025-02-10', 'Effectué');

-- Contrat 1 (2024-02-28): Nettoyage industriel (NI)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2024-02-28') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')), '2024-03-20', 3, 2, 12, 1, '2025-02-20');
SET @planning_id_ecosolutions_nettoyage_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosolutions_nettoyage_2024, '2024-03-20', 'Effectué'), (@planning_id_ecosolutions_nettoyage_2024, '2024-04-20', 'Effectué'),
(@planning_id_ecosolutions_nettoyage_2024, '2024-05-20', 'Effectué'), (@planning_id_ecosolutions_nettoyage_2024, '2024-06-20', 'Effectué'),
(@planning_id_ecosolutions_nettoyage_2024, '2024-07-20', 'Effectué'), (@planning_id_ecosolutions_nettoyage_2024, '2024-08-20', 'Effectué'),
(@planning_id_ecosolutions_nettoyage_2024, '2024-09-20', 'Effectué'), (@planning_id_ecosolutions_nettoyage_2024, '2024-10-20', 'Effectué'),
(@planning_id_ecosolutions_nettoyage_2024, '2024-11-20', 'Effectué'), (@planning_id_ecosolutions_nettoyage_2024, '2024-12-20', 'Effectué'),
(@planning_id_ecosolutions_nettoyage_2024, '2025-01-20', 'Effectué'), (@planning_id_ecosolutions_nettoyage_2024, '2025-02-20', 'Effectué');

-- Contrat 2 (2025-03-01): Ramassage ordure (RO)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2025-03-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')), '2025-03-15', 3, 2, 12, 2, '2026-02-15'); -- Bimensuel
SET @planning_id_ecosolutions_ordure_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosolutions_ordure_2025, '2025-03-15', 'Effectué'), (@planning_id_ecosolutions_ordure_2025, '2025-05-15', 'Effectué'),
(@planning_id_ecosolutions_ordure_2025, '2025-07-15', 'À venir'), (@planning_id_ecosolutions_ordure_2025, '2025-09-15', 'À venir'),
(@planning_id_ecosolutions_ordure_2025, '2025-11-15', 'À venir'), (@planning_id_ecosolutions_ordure_2025, '2026-01-15', 'À venir');

-- Contrat 2 (2025-03-01): Dératisation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2025-03-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')), '2025-04-01', 4, 3, 12, 1, '2026-03-31');
SET @planning_id_ecosolutions_derat_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosolutions_derat_2025, '2025-04-01', 'Effectué'), (@planning_id_ecosolutions_derat_2025, '2025-05-01', 'Effectué'),
(@planning_id_ecosolutions_derat_2025, '2025-06-01', 'Effectué'), (@planning_id_ecosolutions_derat_2025, '2025-07-01', 'Effectué'),
(@planning_id_ecosolutions_derat_2025, '2025-08-01', 'À venir'), (@planning_id_ecosolutions_derat_2025, '2025-09-01', 'À venir'),
(@planning_id_ecosolutions_derat_2025, '2025-10-01', 'À venir'), (@planning_id_ecosolutions_derat_2025, '2025-11-01', 'À venir'),
(@planning_id_ecosolutions_derat_2025, '2025-12-01', 'À venir'), (@planning_id_ecosolutions_derat_2025, '2026-01-01', 'À venir'),
(@planning_id_ecosolutions_derat_2025, '2026-02-01', 'À venir'), (@planning_id_ecosolutions_derat_2025, '2026-03-01', 'À venir');

-- Contrat 3 (2025-06-15): Désinsectisation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2025-06-15') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')), '2025-07-01', 7, 6, 12, 1, '2026-06-30');
SET @planning_id_ecosolutions_desins_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosolutions_desins_2025, '2025-07-01', 'Effectué'), (@planning_id_ecosolutions_desins_2025, '2025-08-01', 'À venir'),
(@planning_id_ecosolutions_desins_2025, '2025-09-01', 'À venir'), (@planning_id_ecosolutions_desins_2025, '2025-10-01', 'À venir'),
(@planning_id_ecosolutions_desins_2025, '2025-11-01', 'À venir'), (@planning_id_ecosolutions_desins_2025, '2025-12-01', 'À venir'),
(@planning_id_ecosolutions_desins_2025, '2026-01-01', 'À venir'), (@planning_id_ecosolutions_desins_2025, '2026-02-01', 'À venir'),
(@planning_id_ecosolutions_desins_2025, '2026-03-01', 'À venir'), (@planning_id_ecosolutions_desins_2025, '2026-04-01', 'À venir'),
(@planning_id_ecosolutions_desins_2025, '2026-05-01', 'À venir'), (@planning_id_ecosolutions_desins_2025, '2026-06-01', 'À venir');

-- Contrat 3 (2025-06-15): Fumigation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND date_contrat = '2025-06-15') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)')), '2025-07-10', 7, 6, 12, 4, '2026-06-10'); -- Trimestriel
SET @planning_id_ecosolutions_fumigation_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosolutions_fumigation_2025, '2025-07-10', 'Effectué'), (@planning_id_ecosolutions_fumigation_2025, '2025-10-10', 'À venir'),
(@planning_id_ecosolutions_fumigation_2025, '2026-01-10', 'À venir'), (@planning_id_ecosolutions_fumigation_2025, '2026-04-10', 'À venir');

-- Client 5: TechInnov SARL (Société)
-- Contrat 1 (2024-07-01): Anti termites (AT)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2024-07-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)')), '2024-07-15', 7, 6, 12, 6, '2025-07-15'); -- Semestriel
SET @planning_id_techinnov_termites_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_techinnov_termites_2024, '2024-07-15', 'Effectué'), (@planning_id_techinnov_termites_2024, '2025-01-15', 'Effectué'),
(@planning_id_techinnov_termites_2024, '2025-07-15', 'À venir'); -- Date actuelle est le 13/07/2025, donc à venir

-- Contrat 1 (2024-07-01): Fumigation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2024-07-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)')), '2024-07-20', 7, 6, 12, 4, '2025-07-20'); -- Trimestriel
SET @planning_id_techinnov_fumigation_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_techinnov_fumigation_2024, '2024-07-20', 'Effectué'), (@planning_id_techinnov_fumigation_2024, '2024-10-20', 'Effectué'),
(@planning_id_techinnov_fumigation_2024, '2025-01-20', 'Effectué'), (@planning_id_techinnov_fumigation_2024, '2025-04-20', 'Effectué'),
(@planning_id_techinnov_fumigation_2024, '2025-07-20', 'À venir'); -- Correction ici: utilisation de @planning_id_techinnov_fumigation_2024

-- Contrat 2 (2024-08-01): Nettoyage industriel (NI)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2024-08-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')), '2024-08-05', 8, 7, 12, 1, '2025-07-31');
SET @planning_id_techinnov_nettoyage_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_techinnov_nettoyage_2024, '2024-08-05', 'Effectué'), (@planning_id_techinnov_nettoyage_2024, '2024-09-05', 'Effectué'),
(@planning_id_techinnov_nettoyage_2024, '2024-10-05', 'Effectué'), (@planning_id_techinnov_nettoyage_2024, '2024-11-05', 'Effectué'),
(@planning_id_techinnov_nettoyage_2024, '2024-12-05', 'Effectué'), (@planning_id_techinnov_nettoyage_2024, '2025-01-05', 'Effectué'),
(@planning_id_techinnov_nettoyage_2024, '2025-02-05', 'Effectué'), (@planning_id_techinnov_nettoyage_2024, '2025-03-05', 'Effectué'),
(@planning_id_techinnov_nettoyage_2024, '2025-04-05', 'Effectué'), (@planning_id_techinnov_nettoyage_2024, '2025-05-05', 'Effectué'),
(@planning_id_techinnov_nettoyage_2024, '2025-06-05', 'Effectué'), (@planning_id_techinnov_nettoyage_2024, '2025-07-05', 'Effectué');

-- Contrat 2 (2024-08-01): Ramassage ordure (RO)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2024-08-01') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')), '2024-08-10', 8, 7, 12, 2, '2025-07-31'); -- Bimensuel
SET @planning_id_techinnov_ordure_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_techinnov_ordure_2024, '2024-08-10', 'Effectué'), (@planning_id_techinnov_ordure_2024, '2024-10-10', 'Effectué'),
(@planning_id_techinnov_ordure_2024, '2024-12-10', 'Effectué'), (@planning_id_techinnov_ordure_2024, '2025-02-10', 'Effectué'),
(@planning_id_techinnov_ordure_2024, '2025-04-10', 'Effectué'), (@planning_id_techinnov_ordure_2024, '2025-06-10', 'Effectué');

-- Contrat 3 (2025-01-20): Dératisation (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2025-01-20') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')), '2025-02-01', 2, 1, 12, 1, '2026-01-31');
SET @planning_id_techinnov_derat_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_techinnov_derat_2025, '2025-02-01', 'Effectué'), (@planning_id_techinnov_derat_2025, '2025-03-01', 'Effectué'),
(@planning_id_techinnov_derat_2025, '2025-04-01', 'Effectué'), (@planning_id_techinnov_derat_2025, '2025-05-01', 'Effectué'),
(@planning_id_techinnov_derat_2025, '2025-06-01', 'Effectué'), (@planning_id_techinnov_derat_2025, '2025-07-01', 'Effectué'),
(@planning_id_techinnov_derat_2025, '2025-08-01', 'À venir'), (@planning_id_techinnov_derat_2025, '2025-09-01', 'À venir'),
(@planning_id_techinnov_derat_2025, '2025-10-01', 'À venir'), (@planning_id_techinnov_derat_2025, '2025-11-01', 'À venir'),
(@planning_id_techinnov_derat_2025, '2025-12-01', 'À venir'), (@planning_id_techinnov_derat_2025, '2026-01-01', 'À venir');

-- Contrat 3 (2025-01-20): Désinfection (PC)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
((SELECT traitement_id FROM Traitement WHERE contrat_id = (SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND date_contrat = '2025-01-20') AND id_type_traitement = (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')), '2025-02-10', 2, 1, 12, 1, '2026-01-31');
SET @planning_id_techinnov_desinf_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_techinnov_desinf_2025, '2025-02-10', 'Effectué'), (@planning_id_techinnov_desinf_2025, '2025-03-10', 'Effectué'),
(@planning_id_techinnov_desinf_2025, '2025-04-10', 'Effectué'), (@planning_id_techinnov_desinf_2025, '2025-05-10', 'Effectué'),
(@planning_id_techinnov_desinf_2025, '2025-06-10', 'Effectué'), (@planning_id_techinnov_desinf_2025, '2025-07-10', 'Effectué'),
(@planning_id_techinnov_desinf_2025, '2025-08-10', 'À venir'), (@planning_id_techinnov_desinf_2025, '2025-09-10', 'À venir'),
(@planning_id_techinnov_desinf_2025, '2025-10-10', 'À venir'), (@planning_id_techinnov_desinf_2025, '2025-11-10', 'À venir'),
(@planning_id_techinnov_desinf_2025, '2025-12-10', 'À venir'), (@planning_id_techinnov_desinf_2025, '2026-01-10', 'À venir');


-- Insertion des factures (pour les traitements de 2023 à 2025)
-- Je vais insérer des factures pour tous les planning_details qui sont 'Effectué' et dont la date de planification est <= 2025-12-31.
INSERT INTO Facture (planning_detail_id, montant, mode, date_traitement, etat, axe)
SELECT
    pd.planning_detail_id,
    FLOOR(100000 + RAND() * 900000) AS montant, -- Montant aléatoire entre 100,000 et 1,000,000
    CASE FLOOR(RAND() * 2) WHEN 0 THEN 'Chèque' ELSE 'Espèce' END AS mode,
    pd.date_planification AS date_traitement,
    CASE FLOOR(RAND() * 2) WHEN 0 THEN 'Payé' ELSE 'Non payé' END AS etat,
    cl.axe
FROM PlanningDetails pd
JOIN Planning pl ON pd.planning_id = pl.planning_id
JOIN Traitement tr ON pl.traitement_id = tr.traitement_id
JOIN Contrat co ON tr.contrat_id = co.contrat_id
JOIN Client cl ON co.client_id = cl.client_id
WHERE pd.statut = 'Effectué' AND pd.date_planification <= '2025-12-31';


-- Insertion des remarques et signalements
-- Je vais insérer une remarque pour chaque planning_detail 'Effectué'
INSERT INTO Remarque (client_id, planning_detail_id, facture_id, contenu, issue, action, date_remarque)
SELECT
    cl.client_id,
    pd.planning_detail_id,
    f.facture_id,
    CONCAT('Traitement effectué le ', pd.date_planification, '. RAS.'),
    NULL,
    'Vérification et application du traitement standard.',
    NOW()
FROM PlanningDetails pd
JOIN Planning pl ON pd.planning_id = pl.planning_id
JOIN Traitement tr ON pl.traitement_id = tr.traitement_id
JOIN Contrat co ON tr.contrat_id = co.contrat_id
JOIN Client cl ON co.client_id = cl.client_id
LEFT JOIN Facture f ON pd.planning_detail_id = f.planning_detail_id
WHERE pd.statut = 'Effectué';

-- Quelques signalements spécifiques (pour les planning_details 'Effectué' ou 'À venir' pour simuler des problèmes ou des ajustements)
-- Client 1, Dupont Jean, Dératisation 2023: Problème persistant
INSERT INTO Signalement (planning_detail_id, motif, type) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_derat_2023 AND date_planification = '2023-05-01'), 'Présence de rongeurs persistante après le traitement.', 'Décalage');

-- Client 2, Martin Sophie, Nettoyage 2024: Demande d'avancement
INSERT INTO Signalement (planning_detail_id, motif, type) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_martin_nettoyage_2024 AND date_planification = '2024-07-10'), 'Client a demandé un nettoyage supplémentaire urgent.', 'Avancement');

-- Client 3, GlobalCorp, Dératisation 2024: Problème de matériel
INSERT INTO Signalement (planning_detail_id, motif, type) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_derat_2024 AND date_planification = '2024-11-05'), 'Matériel défectueux, traitement incomplet.', 'Décalage');

-- Client 5, TechInnov SARL, Anti termites 2025: Nouveau foyer détecté
INSERT INTO Signalement (planning_detail_id, motif, type) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_techinnov_termites_2024 AND date_planification = '2025-07-15'), 'Nouveau foyer de termites détecté avant la prochaine intervention.', 'Décalage');


-- Insertion de l'historique
-- Je vais insérer un historique pour chaque planning_detail 'Effectué'.
-- S'il y a un signalement pour ce planning_detail, je le lierai.
INSERT INTO Historique (facture_id, planning_detail_id, signalement_id, date_historique, contenu, issue, action)
SELECT
    f.facture_id,
    pd.planning_detail_id,
    s.signalement_id,
    NOW(),
    CONCAT('Traitement effectué le ', pd.date_planification, '.'),
    CASE WHEN s.signalement_id IS NOT NULL THEN s.motif ELSE 'Aucun problème signalé.' END,
    'Vérification et application du traitement standard.'
FROM PlanningDetails pd
JOIN Planning pl ON pd.planning_id = pl.planning_id
JOIN Traitement tr ON pl.traitement_id = tr.traitement_id
JOIN Contrat co ON tr.contrat_id = co.contrat_id
JOIN Client cl ON co.client_id = cl.client_id
LEFT JOIN Facture f ON pd.planning_detail_id = f.planning_detail_id
LEFT JOIN Signalement s ON pd.planning_detail_id = s.planning_detail_id
WHERE pd.statut = 'Effectué';
