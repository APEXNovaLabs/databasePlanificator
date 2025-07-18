/*
* Données générées par Gemini
* A noter qu'ils peuvent présenter quelques incohérences
* Date de génération: 18 Juillet 2025
*/
USE Planificator;

-- Réinitialisation des AUTO_INCREMENT pour un environnement de test propre
ALTER TABLE Account AUTO_INCREMENT = 1;
ALTER TABLE Client AUTO_INCREMENT = 1;
ALTER TABLE Contrat AUTO_INCREMENT = 1;
ALTER TABLE TypeTraitement AUTO_INCREMENT = 1;
ALTER TABLE Traitement AUTO_INCREMENT = 1;
ALTER TABLE Planning AUTO_INCREMENT = 1;
ALTER TABLE PlanningDetails AUTO_INCREMENT = 1;
ALTER TABLE Facture AUTO_INCREMENT = 1;
ALTER TABLE Historique_prix AUTO_INCREMENT = 1;
ALTER TABLE Remarque AUTO_INCREMENT = 1;
ALTER TABLE Signalement AUTO_INCREMENT = 1;
ALTER TABLE Historique AUTO_INCREMENT = 1;




-- Insertion des clients (5 clients: 2 Particuliers, 2 Organisations, 1 Société)
INSERT INTO Client (nom, prenom, email, telephone, adresse, nif, stat, date_ajout, categorie, axe) VALUES
('Dupont', 'Jean', 'jean.dupont@example.com', '0341234567', '12 Rue des Fleurs, Antananarivo', NULL, NULL, '2023-01-15', 'Particulier', 'Centre (C)'),
('Martin', 'Sophie', 'sophie.martin@example.com', '0327654321', '25 Avenue de la Liberté, Antananarivo', NULL, NULL, '2023-03-20', 'Particulier', 'Est (E)'),
('GlobalCorp', 'Responsable A', 'contact@globalcorp.com', '0339876543', '45 Boulevard de l''Indépendance, Antananarivo', NULL, NULL, '2023-05-10', 'Organisation', 'Nord (N)'),
('EcoSolutions', 'Directeur B', 'info@ecosolutions.org', '0345678901', '8 Rue des Palmiers, Antananarivo', NULL, NULL, '2024-02-28', 'Organisation', 'Ouest (O)'),
('TechInnov SARL', 'Gérant C', 'admin@techinnov.mg', '0321122334', '60 Route Circulaire, Antananarivo', '1234567890', 'A123B456C789', '2024-07-01', 'Société', 'Sud (S)');

-- Insertion des contrats
-- Client 1: Dupont Jean (Particulier)
INSERT INTO Contrat (client_id, reference_contrat, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
((SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean'), 'REF-DUPONT-001', '2023-01-15', '2023-02-01', '2024-01-31', 'Terminé', 12, 'Déterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean'), 'REF-DUPONT-002', '2024-01-20', '2024-02-01', '2025-01-31', 'Terminé', 12, 'Déterminée', 'Renouvellement'),
((SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean'), 'REF-DUPONT-003', '2025-02-05', '2025-03-01', '2026-02-28', 'Actif', 12, 'Déterminée', 'Renouvellement');

-- Client 2: Martin Sophie (Particulier)
INSERT INTO Contrat (client_id, reference_contrat, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
((SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie'), 'REF-MARTIN-001', '2023-03-20', '2023-04-01', '2024-03-31', 'Terminé', 12, 'Déterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie'), 'REF-MARTIN-002', '2024-03-10', '2024-04-01', '2025-03-31', 'Terminé', 12, 'Déterminée', 'Renouvellement'),
((SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie'), 'REF-MARTIN-003', '2025-04-01', '2025-04-01', NULL, 'Actif', NULL, 'Indeterminée', 'Renouvellement');

-- Client 3: GlobalCorp (Organisation)
INSERT INTO Contrat (client_id, reference_contrat, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
((SELECT client_id FROM Client WHERE nom = 'GlobalCorp'), 'REF-GLOBAL-001', '2023-05-10', '2023-06-01', '2024-05-31', 'Terminé', 12, 'Déterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'GlobalCorp'), 'REF-GLOBAL-002', '2024-05-01', '2024-06-01', NULL, 'Actif', NULL, 'Indeterminée', 'Renouvellement'),
((SELECT client_id FROM Client WHERE nom = 'GlobalCorp'), 'REF-GLOBAL-003', '2025-01-01', '2025-01-01', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau');

-- Client 4: EcoSolutions (Organisation)
INSERT INTO Contrat (client_id, reference_contrat, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
((SELECT client_id FROM Client WHERE nom = 'EcoSolutions'), 'REF-ECO-001', '2024-02-28', '2024-03-10', '2025-03-09', 'Terminé', 12, 'Déterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'EcoSolutions'), 'REF-ECO-002', '2025-03-01', '2025-03-10', NULL, 'Actif', NULL, 'Indeterminée', 'Renouvellement'),
((SELECT client_id FROM Client WHERE nom = 'EcoSolutions'), 'REF-ECO-003', '2025-06-15', '2025-07-01', '2026-06-30', 'Actif', 12, 'Déterminée', 'Nouveau');

-- Client 5: TechInnov SARL (Société)
INSERT INTO Contrat (client_id, reference_contrat, date_contrat, date_debut, date_fin, statut_contrat, duree_contrat, duree, categorie) VALUES
((SELECT client_id FROM Client WHERE nom = 'TechInnov SARL'), 'REF-TECH-001', '2024-07-01', '2024-07-15', NULL, 'Actif', NULL, 'Indeterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'TechInnov SARL'), 'REF-TECH-002', '2024-08-01', '2024-08-01', '2025-07-31', 'Actif', 12, 'Déterminée', 'Nouveau'),
((SELECT client_id FROM Client WHERE nom = 'TechInnov SARL'), 'REF-TECH-003', '2025-01-20', '2025-02-01', NULL, 'Actif', NULL, 'Indeterminée', 'Renouvellement');

-- Insertion des types de traitement (avec catégorieTraitement)
INSERT IGNORE INTO TypeTraitement (categorieTraitement, typeTraitement) VALUES
('PC', 'Dératisation (PC)'),
('PC', 'Désinfection (PC)'),
('PC', 'Désinsectisation (PC)'),
('PC', 'Fumigation (PC)'),
('NI', 'Nettoyage industriel (NI)'),
('AT', 'Anti termites (AT)'),
('RO', 'Ramassage ordure');

-- Insertion des traitements
-- Client 1: Dupont Jean
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND reference_contrat = 'REF-DUPONT-001'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')), -- 1
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND reference_contrat = 'REF-DUPONT-001'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')), -- 2
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND reference_contrat = 'REF-DUPONT-002'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')), -- 3
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND reference_contrat = 'REF-DUPONT-002'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')), -- 4
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND reference_contrat = 'REF-DUPONT-003'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)')), -- 5
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean') AND reference_contrat = 'REF-DUPONT-003'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')); -- 6

-- Client 2: Martin Sophie
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND reference_contrat = 'REF-MARTIN-001'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')), -- 7
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND reference_contrat = 'REF-MARTIN-001'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)')), -- 8
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND reference_contrat = 'REF-MARTIN-002'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')), -- 9
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND reference_contrat = 'REF-MARTIN-002'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')), -- 10
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND reference_contrat = 'REF-MARTIN-003'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')), -- 11
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie') AND reference_contrat = 'REF-MARTIN-003'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')); -- 12

-- Client 3: GlobalCorp
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND reference_contrat = 'REF-GLOBAL-001'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')), -- 13
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND reference_contrat = 'REF-GLOBAL-001'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')), -- 14
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND reference_contrat = 'REF-GLOBAL-002'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')), -- 15
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND reference_contrat = 'REF-GLOBAL-002'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')), -- 16
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND reference_contrat = 'REF-GLOBAL-003'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)')), -- 17
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'GlobalCorp') AND reference_contrat = 'REF-GLOBAL-003'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)')); -- 18

-- Client 4: EcoSolutions
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND reference_contrat = 'REF-ECO-001'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')), -- 19
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND reference_contrat = 'REF-ECO-001'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')), -- 20
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND reference_contrat = 'REF-ECO-002'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')), -- 21
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND reference_contrat = 'REF-ECO-002'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')), -- 22
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND reference_contrat = 'REF-ECO-003'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinsectisation (PC)')), -- 23
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'EcoSolutions') AND reference_contrat = 'REF-ECO-003'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)')); -- 24

-- Client 5: TechInnov SARL
INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND reference_contrat = 'REF-TECH-001'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Anti termites (AT)')), -- 25
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND reference_contrat = 'REF-TECH-001'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Fumigation (PC)')), -- 26
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND reference_contrat = 'REF-TECH-002'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Nettoyage industriel (NI)')), -- 27
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND reference_contrat = 'REF-TECH-002'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Ramassage ordure')), -- 28
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND reference_contrat = 'REF-TECH-003'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Dératisation (PC)')), -- 29
((SELECT contrat_id FROM Contrat WHERE client_id = (SELECT client_id FROM Client WHERE nom = 'TechInnov SARL') AND reference_contrat = 'REF-TECH-003'), (SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = 'Désinfection (PC)')); -- 30


-- Insertion des plannings et détails de planification
-- La date actuelle est le 18 juillet 2025.

-- Client 1: Dupont Jean
-- Contrat REF-DUPONT-001 (Terminé)
-- Traitement Dératisation (PC) (ID 1)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(1, '2023-02-01', 2, 1, 12, 1, '2024-01-31'); -- Mensuel
SET @planning_id_dupont_derat_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_derat_2023, '2023-02-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2023-03-01', 'Effectué'),
(@planning_id_dupont_derat_2023, '2023-04-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2023-05-01', 'Effectué'),
(@planning_id_dupont_derat_2023, '2023-06-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2023-07-01', 'Effectué'),
(@planning_id_dupont_derat_2023, '2023-08-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2023-09-01', 'Effectué'),
(@planning_id_dupont_derat_2023, '2023-10-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2023-11-01', 'Effectué'),
(@planning_id_dupont_derat_2023, '2023-12-01', 'Effectué'), (@planning_id_dupont_derat_2023, '2024-01-01', 'Effectué');

-- Traitement Désinfection (PC) (ID 2)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(2, '2023-02-15', 2, 1, 12, 3, '2024-01-15'); -- Trimestriel
SET @planning_id_dupont_desinf_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_desinf_2023, '2023-02-15', 'Effectué'), (@planning_id_dupont_desinf_2023, '2023-05-15', 'Effectué'),
(@planning_id_dupont_desinf_2023, '2023-08-15', 'Effectué'), (@planning_id_dupont_desinf_2023, '2023-11-15', 'Effectué'),
(@planning_id_dupont_desinf_2023, '2024-02-15', 'Effectué');

-- Contrat REF-DUPONT-002 (Terminé)
-- Traitement Désinsectisation (PC) (ID 3)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(3, '2024-02-05', 2, 1, 12, 1, '2025-01-31'); -- Mensuel
SET @planning_id_dupont_desins_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_desins_2024, '2024-02-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2024-03-05', 'Effectué'),
(@planning_id_dupont_desins_2024, '2024-04-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2024-05-05', 'Effectué'),
(@planning_id_dupont_desins_2024, '2024-06-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2024-07-05', 'Effectué'),
(@planning_id_dupont_desins_2024, '2024-08-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2024-09-05', 'Effectué'),
(@planning_id_dupont_desins_2024, '2024-10-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2024-11-05', 'Effectué'),
(@planning_id_dupont_desins_2024, '2024-12-05', 'Effectué'), (@planning_id_dupont_desins_2024, '2025-01-05', 'Effectué');

-- Traitement Nettoyage industriel (NI) (ID 4)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(4, '2024-02-10', 2, 1, 12, 1, '2025-01-31'); -- Mensuel
SET @planning_id_dupont_nettoyage_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_nettoyage_2024, '2024-02-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2024-03-10', 'Effectué'),
(@planning_id_dupont_nettoyage_2024, '2024-04-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2024-05-10', 'Effectué'),
(@planning_id_dupont_nettoyage_2024, '2024-06-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2024-07-10', 'Effectué'),
(@planning_id_dupont_nettoyage_2024, '2024-08-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2024-09-10', 'Effectué'),
(@planning_id_dupont_nettoyage_2024, '2024-10-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2024-11-10', 'Effectué'),
(@planning_id_dupont_nettoyage_2024, '2024-12-10', 'Effectué'), (@planning_id_dupont_nettoyage_2024, '2025-01-10', 'Effectué');

-- Contrat REF-DUPONT-003 (Actif)
-- Traitement Anti termites (AT) (ID 5)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(5, '2025-03-01', 3, 2, 12, 6, '2026-02-28'); -- Semestriel
SET @planning_id_dupont_termites_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_termites_2025, '2025-03-01', 'Effectué'), (@planning_id_dupont_termites_2025, '2025-09-01', 'À venir'),
(@planning_id_dupont_termites_2025, '2026-03-01', 'À venir');

-- Traitement Ramassage ordure (RO) (ID 6)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(6, '2025-03-10', 3, 2, 12, 2, '2026-02-28'); -- Bimensuel
SET @planning_id_dupont_ordure_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_dupont_ordure_2025, '2025-03-10', 'Effectué'), (@planning_id_dupont_ordure_2025, '2025-05-10', 'Effectué'),
(@planning_id_dupont_ordure_2025, '2025-07-10', 'Effectué'), -- Date actuelle est le 18/07/2025, donc effectué
(@planning_id_dupont_ordure_2025, '2025-09-10', 'À venir'), (@planning_id_dupont_ordure_2025, '2025-11-10', 'À venir'),
(@planning_id_dupont_ordure_2025, '2026-01-10', 'À venir');

-- Client 2: Martin Sophie
-- Contrat REF-MARTIN-001 (Terminé)
-- Traitement Désinsectisation (PC) (ID 7)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(7, '2023-04-01', 4, 3, 12, 1, '2024-03-31'); -- Mensuel
SET @planning_id_martin_desins_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_desins_2023, '2023-04-01', 'Effectué'), (@planning_id_martin_desins_2023, '2023-05-01', 'Effectué'),
(@planning_id_martin_desins_2023, '2023-06-01', 'Effectué'), (@planning_id_martin_desins_2023, '2023-07-01', 'Effectué'),
(@planning_id_martin_desins_2023, '2023-08-01', 'Effectué'), (@planning_id_martin_desins_2023, '2023-09-01', 'Effectué'),
(@planning_id_martin_desins_2023, '2023-10-01', 'Effectué'), (@planning_id_martin_desins_2023, '2023-11-01', 'Effectué'),
(@planning_id_martin_desins_2023, '2023-12-01', 'Effectué'), (@planning_id_martin_desins_2023, '2024-01-01', 'Effectué'),
(@planning_id_martin_desins_2023, '2024-02-01', 'Effectué'), (@planning_id_martin_desins_2023, '2024-03-01', 'Effectué');

-- Traitement Fumigation (PC) (ID 8)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(8, '2023-04-15', 4, 3, 12, 4, '2024-03-15'); -- Trimestriel
SET @planning_id_martin_fumigation_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_fumigation_2023, '2023-04-15', 'Effectué'), (@planning_id_martin_fumigation_2023, '2023-07-15', 'Effectué'),
(@planning_id_martin_fumigation_2023, '2023-10-15', 'Effectué'), (@planning_id_martin_fumigation_2023, '2024-01-15', 'Effectué');

-- Contrat REF-MARTIN-002 (Terminé)
-- Traitement Dératisation (PC) (ID 9)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(9, '2024-04-05', 4, 3, 12, 1, '2025-03-31'); -- Mensuel
SET @planning_id_martin_derat_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_derat_2024, '2024-04-05', 'Effectué'), (@planning_id_martin_derat_2024, '2024-05-05', 'Effectué'),
(@planning_id_martin_derat_2024, '2024-06-05', 'Effectué'), (@planning_id_martin_derat_2024, '2024-07-05', 'Effectué'),
(@planning_id_martin_derat_2024, '2024-08-05', 'Effectué'), (@planning_id_martin_derat_2024, '2024-09-05', 'Effectué'),
(@planning_id_martin_derat_2024, '2024-10-05', 'Effectué'), (@planning_id_martin_derat_2024, '2024-11-05', 'Effectué'),
(@planning_id_martin_derat_2024, '2024-12-05', 'Effectué'), (@planning_id_martin_derat_2024, '2025-01-05', 'Effectué'),
(@planning_id_martin_derat_2024, '2025-02-05', 'Effectué'), (@planning_id_martin_derat_2024, '2025-03-05', 'Effectué');

-- Traitement Nettoyage industriel (NI) (ID 10)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(10, '2024-04-10', 4, 3, 12, 1, '2025-03-31'); -- Mensuel
SET @planning_id_martin_nettoyage_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_nettoyage_2024, '2024-04-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2024-05-10', 'Effectué'),
(@planning_id_martin_nettoyage_2024, '2024-06-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2024-07-10', 'Effectué'),
(@planning_id_martin_nettoyage_2024, '2024-08-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2024-09-10', 'Effectué'),
(@planning_id_martin_nettoyage_2024, '2024-10-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2024-11-10', 'Effectué'),
(@planning_id_martin_nettoyage_2024, '2024-12-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2025-01-10', 'Effectué'),
(@planning_id_martin_nettoyage_2024, '2025-02-10', 'Effectué'), (@planning_id_martin_nettoyage_2024, '2025-03-10', 'Effectué');

-- Contrat REF-MARTIN-003 (Actif)
-- Traitement Ramassage ordure (RO) (ID 11)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(11, '2025-04-01', 4, 3, 12, 1, '2026-03-31'); -- Mensuel
SET @planning_id_martin_ordure_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_ordure_2025, '2025-04-01', 'Effectué'), (@planning_id_martin_ordure_2025, '2025-05-01', 'Effectué'),
(@planning_id_martin_ordure_2025, '2025-06-01', 'Effectué'), (@planning_id_martin_ordure_2025, '2025-07-01', 'Effectué'),
(@planning_id_martin_ordure_2025, '2025-08-01', 'À venir'), (@planning_id_martin_ordure_2025, '2025-09-01', 'À venir'),
(@planning_id_martin_ordure_2025, '2025-10-01', 'À venir'), (@planning_id_martin_ordure_2025, '2025-11-01', 'À venir'),
(@planning_id_martin_ordure_2025, '2025-12-01', 'À venir'), (@planning_id_martin_ordure_2025, '2026-01-01', 'À venir'),
(@planning_id_martin_ordure_2025, '2026-02-01', 'À venir'), (@planning_id_martin_ordure_2025, '2026-03-01', 'À venir');

-- Traitement Désinfection (PC) (ID 12)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(12, '2025-04-20', 4, 3, 12, 4, '2026-03-20'); -- Trimestriel
SET @planning_id_martin_desinf_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_martin_desinf_2025, '2025-04-20', 'Effectué'), (@planning_id_martin_desinf_2025, '2025-07-20', 'À venir'),
(@planning_id_martin_desinf_2025, '2025-10-20', 'À venir'), (@planning_id_martin_desinf_2025, '2026-01-20', 'À venir');

-- Client 3: GlobalCorp (Organisation)
-- Contrat REF-GLOBAL-001 (Terminé)
-- Traitement Nettoyage industriel (NI) (ID 13)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(13, '2023-06-01', 6, 5, 12, 1, '2024-05-31'); -- Mensuel
SET @planning_id_globalcorp_nettoyage_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_nettoyage_2023, '2023-06-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2023-07-01', 'Effectué'),
(@planning_id_globalcorp_nettoyage_2023, '2023-08-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2023-09-01', 'Effectué'),
(@planning_id_globalcorp_nettoyage_2023, '2023-10-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2023-11-01', 'Effectué'),
(@planning_id_globalcorp_nettoyage_2023, '2023-12-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2024-01-01', 'Effectué'),
(@planning_id_globalcorp_nettoyage_2023, '2024-02-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2024-03-01', 'Effectué'),
(@planning_id_globalcorp_nettoyage_2023, '2024-04-01', 'Effectué'), (@planning_id_globalcorp_nettoyage_2023, '2024-05-01', 'Effectué');

-- Traitement Ramassage ordure (RO) (ID 14)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(14, '2023-06-15', 6, 5, 12, 2, '2024-05-15'); -- Bimensuel
SET @planning_id_globalcorp_ordure_2023 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_ordure_2023, '2023-06-15', 'Effectué'), (@planning_id_globalcorp_ordure_2023, '2023-08-15', 'Effectué'),
(@planning_id_globalcorp_ordure_2023, '2023-10-15', 'Effectué'), (@planning_id_globalcorp_ordure_2023, '2023-12-15', 'Effectué'),
(@planning_id_globalcorp_ordure_2023, '2024-02-15', 'Effectué'), (@planning_id_globalcorp_ordure_2023, '2024-04-15', 'Effectué');

-- Contrat REF-GLOBAL-002 (Actif)
-- Traitement Dératisation (PC) (ID 15)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(15, '2024-06-05', 6, 5, 12, 1, '2025-05-31'); -- Mensuel
SET @planning_id_globalcorp_derat_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_derat_2024, '2024-06-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2024-07-05', 'Effectué'),
(@planning_id_globalcorp_derat_2024, '2024-08-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2024-09-05', 'Effectué'),
(@planning_id_globalcorp_derat_2024, '2024-10-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2024-11-05', 'Effectué'),
(@planning_id_globalcorp_derat_2024, '2024-12-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2025-01-05', 'Effectué'),
(@planning_id_globalcorp_derat_2024, '2025-02-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2025-03-05', 'Effectué'),
(@planning_id_globalcorp_derat_2024, '2025-04-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2025-05-05', 'Effectué'),
(@planning_id_globalcorp_derat_2024, '2025-06-05', 'Effectué'), (@planning_id_globalcorp_derat_2024, '2025-07-05', 'Effectué'); -- Dernier effectué

-- Traitement Désinsectisation (PC) (ID 16)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(16, '2024-06-10', 6, 5, 12, 2, '2025-05-10'); -- Bimensuel
SET @planning_id_globalcorp_desins_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_desins_2024, '2024-06-10', 'Effectué'), (@planning_id_globalcorp_desins_2024, '2024-08-10', 'Effectué'),
(@planning_id_globalcorp_desins_2024, '2024-10-10', 'Effectué'), (@planning_id_globalcorp_desins_2024, '2024-12-10', 'Effectué'),
(@planning_id_globalcorp_desins_2024, '2025-02-10', 'Effectué'), (@planning_id_globalcorp_desins_2024, '2025-04-10', 'Effectué'),
(@planning_id_globalcorp_desins_2024, '2025-06-10', 'Effectué'); -- Dernier effectué

-- Contrat REF-GLOBAL-003 (Actif)
-- Traitement Anti termites (AT) (ID 17)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(17, '2025-01-15', 1, 12, 12, 6, '2025-12-15'); -- Semestriel
SET @planning_id_globalcorp_termites_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_termites_2025, '2025-01-15', 'Effectué'), (@planning_id_globalcorp_termites_2025, '2025-07-15', 'Effectué'), -- Effectué car date actuelle 18/07
(@planning_id_globalcorp_termites_2025, '2026-01-15', 'À venir');

-- Traitement Fumigation (PC) (ID 18)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(18, '2025-01-20', 1, 12, 12, 3, '2025-12-20'); -- Trimestriel
SET @planning_id_globalcorp_fumigation_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_globalcorp_fumigation_2025, '2025-01-20', 'Effectué'), (@planning_id_globalcorp_fumigation_2025, '2025-04-20', 'Effectué'),
(@planning_id_globalcorp_fumigation_2025, '2025-07-20', 'À venir'), (@planning_id_globalcorp_fumigation_2025, '2025-10-20', 'À venir');


-- Client 4: EcoSolutions (Organisation)
-- Contrat REF-ECO-001 (Terminé)
-- Traitement Désinfection (PC) (ID 19)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(19, '2024-03-10', 3, 2, 12, 1, '2025-03-09'); -- Mensuel
SET @planning_id_ecosol_desinf_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosol_desinf_2024, '2024-03-10', 'Effectué'), (@planning_id_ecosol_desinf_2024, '2024-04-10', 'Effectué'),
(@planning_id_ecosol_desinf_2024, '2024-05-10', 'Effectué'), (@planning_id_ecosol_desinf_2024, '2024-06-10', 'Effectué'),
(@planning_id_ecosol_desinf_2024, '2024-07-10', 'Effectué'), (@planning_id_ecosol_desinf_2024, '2024-08-10', 'Effectué'),
(@planning_id_ecosol_desinf_2024, '2024-09-10', 'Effectué'), (@planning_id_ecosol_desinf_2024, '2024-10-10', 'Effectué'),
(@planning_id_ecosol_desinf_2024, '2024-11-10', 'Effectué'), (@planning_id_ecosol_desinf_2024, '2024-12-10', 'Effectué'),
(@planning_id_ecosol_desinf_2024, '2025-01-10', 'Effectué'), (@planning_id_ecosol_desinf_2024, '2025-02-10', 'Effectué');

-- Traitement Nettoyage industriel (NI) (ID 20)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(20, '2024-03-15', 3, 2, 12, 2, '2025-03-14'); -- Bimensuel
SET @planning_id_ecosol_nettoyage_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosol_nettoyage_2024, '2024-03-15', 'Effectué'), (@planning_id_ecosol_nettoyage_2024, '2024-05-15', 'Effectué'),
(@planning_id_ecosol_nettoyage_2024, '2024-07-15', 'Effectué'), (@planning_id_ecosol_nettoyage_2024, '2024-09-15', 'Effectué'),
(@planning_id_ecosol_nettoyage_2024, '2024-11-15', 'Effectué'), (@planning_id_ecosol_nettoyage_2024, '2025-01-15', 'Effectué'),
(@planning_id_ecosol_nettoyage_2024, '2025-03-15', 'Effectué');

-- Contrat REF-ECO-002 (Actif)
-- Traitement Ramassage ordure (RO) (ID 21)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(21, '2025-03-10', 3, 2, 12, 1, '2026-03-09'); -- Mensuel
SET @planning_id_ecosol_ordure_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosol_ordure_2025, '2025-03-10', 'Effectué'), (@planning_id_ecosol_ordure_2025, '2025-04-10', 'Effectué'),
(@planning_id_ecosol_ordure_2025, '2025-05-10', 'Effectué'), (@planning_id_ecosol_ordure_2025, '2025-06-10', 'Effectué'),
(@planning_id_ecosol_ordure_2025, '2025-07-10', 'Effectué'),
(@planning_id_ecosol_ordure_2025, '2025-08-10', 'À venir'), (@planning_id_ecosol_ordure_2025, '2025-09-10', 'À venir'),
(@planning_id_ecosol_ordure_2025, '2025-10-10', 'À venir'), (@planning_id_ecosol_ordure_2025, '2025-11-10', 'À venir'),
(@planning_id_ecosol_ordure_2025, '2025-12-10', 'À venir'), (@planning_id_ecosol_ordure_2025, '2026-01-10', 'À venir'),
(@planning_id_ecosol_ordure_2025, '2026-02-10', 'À venir');

-- Traitement Dératisation (PC) (ID 22)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(22, '2025-03-15', 3, 2, 12, 3, '2026-02-15'); -- Trimestriel
SET @planning_id_ecosol_derat_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosol_derat_2025, '2025-03-15', 'Effectué'), (@planning_id_ecosol_derat_2025, '2025-06-15', 'Effectué'),
(@planning_id_ecosol_derat_2025, '2025-09-15', 'À venir'), (@planning_id_ecosol_derat_2025, '2025-12-15', 'À venir');

-- Contrat REF-ECO-003 (Actif)
-- Traitement Désinsectisation (PC) (ID 23)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(23, '2025-07-01', 7, 6, 12, 1, '2026-06-30'); -- Mensuel
SET @planning_id_ecosol_desins_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosol_desins_2025, '2025-07-01', 'Effectué'), (@planning_id_ecosol_desins_2025, '2025-08-01', 'À venir'),
(@planning_id_ecosol_desins_2025, '2025-09-01', 'À venir'), (@planning_id_ecosol_desins_2025, '2025-10-01', 'À venir'),
(@planning_id_ecosol_desins_2025, '2025-11-01', 'À venir'), (@planning_id_ecosol_desins_2025, '2025-12-01', 'À venir'),
(@planning_id_ecosol_desins_2025, '2026-01-01', 'À venir'), (@planning_id_ecosol_desins_2025, '2026-02-01', 'À venir'),
(@planning_id_ecosol_desins_2025, '2026-03-01', 'À venir'), (@planning_id_ecosol_desins_2025, '2026-04-01', 'À venir'),
(@planning_id_ecosol_desins_2025, '2026-05-01', 'À venir'), (@planning_id_ecosol_desins_2025, '2026-06-01', 'À venir');

-- Traitement Fumigation (PC) (ID 24)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(24, '2025-07-05', 7, 6, 12, 4, '2026-06-05'); -- Trimestriel
SET @planning_id_ecosol_fumigation_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_ecosol_fumigation_2025, '2025-07-05', 'Effectué'), (@planning_id_ecosol_fumigation_2025, '2025-10-05', 'À venir'),
(@planning_id_ecosol_fumigation_2025, '2026-01-05', 'À venir'), (@planning_id_ecosol_fumigation_2025, '2026-04-05', 'À venir');


-- Client 5: TechInnov SARL (Société)
-- Contrat REF-TECH-001 (Actif)
-- Traitement Anti termites (AT) (ID 25)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(25, '2024-07-15', 7, 6, 12, 6, '2025-06-15'); -- Semestriel
SET @planning_id_tech_termites_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_tech_termites_2024, '2024-07-15', 'Effectué'), (@planning_id_tech_termites_2024, '2025-01-15', 'Effectué'),
(@planning_id_tech_termites_2024, '2025-07-15', 'Effectué'); -- Dernier effectué

-- Traitement Fumigation (PC) (ID 26)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(26, '2024-07-20', 7, 6, 12, 3, '2025-06-20'); -- Trimestriel
SET @planning_id_tech_fumigation_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_tech_fumigation_2024, '2024-07-20', 'Effectué'), (@planning_id_tech_fumigation_2024, '2024-10-20', 'Effectué'),
(@planning_id_tech_fumigation_2024, '2025-01-20', 'Effectué'), (@planning_id_tech_fumigation_2024, '2025-04-20', 'Effectué'),
(@planning_id_tech_fumigation_2024, '2025-07-20', 'À venir'); -- À venir

-- Contrat REF-TECH-002 (Actif)
-- Traitement Nettoyage industriel (NI) (ID 27)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(27, '2024-08-01', 8, 7, 12, 1, '2025-07-31'); -- Mensuel
SET @planning_id_tech_nettoyage_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_tech_nettoyage_2024, '2024-08-01', 'Effectué'), (@planning_id_tech_nettoyage_2024, '2024-09-01', 'Effectué'),
(@planning_id_tech_nettoyage_2024, '2024-10-01', 'Effectué'), (@planning_id_tech_nettoyage_2024, '2024-11-01', 'Effectué'),
(@planning_id_tech_nettoyage_2024, '2024-12-01', 'Effectué'), (@planning_id_tech_nettoyage_2024, '2025-01-01', 'Effectué'),
(@planning_id_tech_nettoyage_2024, '2025-02-01', 'Effectué'), (@planning_id_tech_nettoyage_2024, '2025-03-01', 'Effectué'),
(@planning_id_tech_nettoyage_2024, '2025-04-01', 'Effectué'), (@planning_id_tech_nettoyage_2024, '2025-05-01', 'Effectué'),
(@planning_id_tech_nettoyage_2024, '2025-06-01', 'Effectué'), (@planning_id_tech_nettoyage_2024, '2025-07-01', 'Effectué'); -- Dernier effectué

-- Traitement Ramassage ordure (RO) (ID 28)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(28, '2024-08-05', 8, 7, 12, 2, '2025-07-05'); -- Bimensuel
SET @planning_id_tech_ordure_2024 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_tech_ordure_2024, '2024-08-05', 'Effectué'), (@planning_id_tech_ordure_2024, '2024-10-05', 'Effectué'),
(@planning_id_tech_ordure_2024, '2024-12-05', 'Effectué'), (@planning_id_tech_ordure_2024, '2025-02-05', 'Effectué'),
(@planning_id_tech_ordure_2024, '2025-04-05', 'Effectué'), (@planning_id_tech_ordure_2024, '2025-06-05', 'Effectué');

-- Contrat REF-TECH-003 (Actif)
-- Traitement Dératisation (PC) (ID 29)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(29, '2025-02-01', 2, 1, 12, 1, '2026-01-31'); -- Mensuel
SET @planning_id_tech_derat_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_tech_derat_2025, '2025-02-01', 'Effectué'), (@planning_id_tech_derat_2025, '2025-03-01', 'Effectué'),
(@planning_id_tech_derat_2025, '2025-04-01', 'Effectué'), (@planning_id_tech_derat_2025, '2025-05-01', 'Effectué'),
(@planning_id_tech_derat_2025, '2025-06-01', 'Effectué'), (@planning_id_tech_derat_2025, '2025-07-01', 'Effectué'),
(@planning_id_tech_derat_2025, '2025-08-01', 'À venir'), (@planning_id_tech_derat_2025, '2025-09-01', 'À venir'),
(@planning_id_tech_derat_2025, '2025-10-01', 'À venir'), (@planning_id_tech_derat_2025, '2025-11-01', 'À venir'),
(@planning_id_tech_derat_2025, '2025-12-01', 'À venir'), (@planning_id_tech_derat_2025, '2026-01-01', 'À venir');

-- Traitement Désinfection (PC) (ID 30)
INSERT INTO Planning (traitement_id, date_debut_planification, mois_debut, mois_fin, duree_traitement, redondance, date_fin_planification) VALUES
(30, '2025-02-10', 2, 1, 12, 4, '2026-01-10'); -- Trimestriel
SET @planning_id_tech_desinf_2025 = LAST_INSERT_ID();
INSERT INTO PlanningDetails (planning_id, date_planification, statut) VALUES
(@planning_id_tech_desinf_2025, '2025-02-10', 'Effectué'), (@planning_id_tech_desinf_2025, '2025-05-10', 'Effectué'),
(@planning_id_tech_desinf_2025, '2025-08-10', 'À venir'), (@planning_id_tech_desinf_2025, '2025-11-10', 'À venir');


-- Insertion des factures (liées aux PlanningDetails 'Effectué')
-- Dupont Jean (Centre (C))
-- Factures pour 2024 (Contrat REF-DUPONT-002)
INSERT INTO Facture (planning_detail_id, reference_facture, montant, mode, etablissemnt_payeur, numero_cheque, date_paiement, date_traitement, etat, axe) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_desins_2024 AND date_planification = '2024-02-05'), 'F-DUP-2024-001', 150000, 'Espèce', NULL, NULL, '2024-02-05', '2024-02-05', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_nettoyage_2024 AND date_planification = '2024-02-10'), 'F-DUP-2024-002', 250000, 'Virement', NULL, NULL, '2024-02-12', '2024-02-10', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_desins_2024 AND date_planification = '2024-03-05'), 'F-DUP-2024-003', 150000, NULL, NULL, NULL, NULL, '2024-03-05', 'Non payé', 'Centre (C)'), -- CORRIGÉ: mode est NULL
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_nettoyage_2024 AND date_planification = '2024-03-10'), 'F-DUP-2024-004', 250000, 'Chèque', 'BNI', 'CHQ-789012', '2024-03-15', '2024-03-10', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_desins_2024 AND date_planification = '2024-07-05'), 'F-DUP-2024-005', 150000, 'Mobile Money', NULL, NULL, '2024-07-05', '2024-07-05', 'Payé', 'Centre (C)');

-- Factures pour 2025 (Contrat REF-DUPONT-003)
INSERT INTO Facture (planning_detail_id, reference_facture, montant, mode, etablissemnt_payeur, numero_cheque, date_paiement, date_traitement, etat, axe) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_termites_2025 AND date_planification = '2025-03-01'), 'F-DUP-2025-001', 500000, 'Espèce', NULL, NULL, '2025-03-01', '2025-03-01', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_ordure_2025 AND date_planification = '2025-03-10'), 'F-DUP-2025-002', 80000, NULL, NULL, NULL, NULL, '2025-03-10', 'Non payé', 'Centre (C)'), -- CORRIGÉ: mode est NULL
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_ordure_2025 AND date_planification = '2025-05-10'), 'F-DUP-2025-003', 80000, 'Mobile Money', NULL, NULL, '2025-05-10', '2025-05-10', 'Payé', 'Centre (C)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_ordure_2025 AND date_planification = '2025-07-10'), 'F-DUP-2025-004', 80000, NULL, NULL, NULL, NULL, '2025-07-10', 'À venir', 'Centre (C)'); -- CORRIGÉ: mode est NULL

-- Martin Sophie (Est (E))
-- Factures pour 2024 (Contrat REF-MARTIN-002)
INSERT INTO Facture (planning_detail_id, reference_facture, montant, mode, etablissemnt_payeur, numero_cheque, date_paiement, date_traitement, etat, axe) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_martin_derat_2024 AND date_planification = '2024-04-05'), 'F-MAR-2024-001', 180000, 'Chèque', 'BOA', 'CHQ-112233', '2024-04-10', '2024-04-05', 'Payé', 'Est (E)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_martin_nettoyage_2024 AND date_planification = '2024-04-10'), 'F-MAR-2024-002', 300000, 'Espèce', NULL, NULL, '2024-04-10', '2024-04-10', 'Payé', 'Est (E)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_martin_derat_2024 AND date_planification = '2024-07-05'), 'F-MAR-2024-003', 180000, NULL, NULL, NULL, NULL, '2024-07-05', 'Non payé', 'Est (E)'), -- CORRIGÉ: mode est NULL
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_martin_nettoyage_2024 AND date_planification = '2024-07-10'), 'F-MAR-2024-004', 300000, 'Virement', NULL, NULL, '2024-07-12', '2024-07-10', 'Payé', 'Est (E)');

-- Factures pour 2025 (Contrat REF-MARTIN-003)
INSERT INTO Facture (planning_detail_id, reference_facture, montant, mode, etablissemnt_payeur, numero_cheque, date_paiement, date_traitement, etat, axe) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_martin_ordure_2025 AND date_planification = '2025-04-01'), 'F-MAR-2025-001', 90000, 'Espèce', NULL, NULL, '2025-04-01', '2025-04-01', 'Payé', 'Est (E)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_martin_desinf_2025 AND date_planification = '2025-04-20'), 'F-MAR-2025-002', 200000, NULL, NULL, NULL, NULL, '2025-04-20', 'Non payé', 'Est (E)'), -- CORRIGÉ: mode est NULL
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_martin_ordure_2025 AND date_planification = '2025-07-01'), 'F-MAR-2025-003', 90000, 'Mobile Money', NULL, NULL, '2025-07-01', '2025-07-01', 'Payé', 'Est (E)');

-- GlobalCorp (Nord (N))
-- Factures pour 2024 (Contrat REF-GLOBAL-002)
INSERT INTO Facture (planning_detail_id, reference_facture, montant, mode, etablissemnt_payeur, numero_cheque, date_paiement, date_traitement, etat, axe) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_derat_2024 AND date_planification = '2024-06-05'), 'F-GLOB-2024-001', 200000, 'Virement', NULL, NULL, '2024-06-07', '2024-06-05', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_desins_2024 AND date_planification = '2024-06-10'), 'F-GLOB-2024-002', 220000, 'Chèque', 'BFV', 'CHQ-445566', '2024-06-15', '2024-06-10', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_derat_2024 AND date_planification = '2024-09-05'), 'F-GLOB-2024-003', 200000, NULL, NULL, NULL, NULL, '2024-09-05', 'Non payé', 'Nord (N)'), -- CORRIGÉ: mode est NULL
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_desins_2024 AND date_planification = '2024-10-10'), 'F-GLOB-2024-004', 220000, 'Espèce', NULL, NULL, '2024-10-10', '2024-10-10', 'Payé', 'Nord (N)');

-- Factures pour 2025 (Contrat REF-GLOBAL-003)
INSERT INTO Facture (planning_detail_id, reference_facture, montant, mode, etablissemnt_payeur, numero_cheque, date_paiement, date_traitement, etat, axe) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_termites_2025 AND date_planification = '2025-01-15'), 'F-GLOB-2025-001', 600000, 'Virement', NULL, NULL, '2025-01-17', '2025-01-15', 'Payé', 'Nord (N)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_fumigation_2025 AND date_planification = '2025-01-20'), 'F-GLOB-2025-002', 250000, NULL, NULL, NULL, NULL, '2025-01-20', 'Non payé', 'Nord (N)'), -- CORRIGÉ: mode est NULL
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_termites_2025 AND date_planification = '2025-07-15'), 'F-GLOB-2025-003', 600000, 'Mobile Money', NULL, NULL, '2025-07-15', '2025-07-15', 'Payé', 'Nord (N)');

-- EcoSolutions (Ouest (O))
-- Factures pour 2024 (Contrat REF-ECO-001)
INSERT INTO Facture (planning_detail_id, reference_facture, montant, mode, etablissemnt_payeur, numero_cheque, date_paiement, date_traitement, etat, axe) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_ecosol_desinf_2024 AND date_planification = '2024-03-10'), 'F-ECO-2024-001', 190000, 'Espèce', NULL, NULL, '2024-03-10', '2024-03-10', 'Payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_ecosol_nettoyage_2024 AND date_planification = '2024-03-15'), 'F-ECO-2024-002', 320000, 'Chèque', 'BMOI', 'CHQ-778899', '2024-03-20', '2024-03-15', 'Payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_ecosol_desinf_2024 AND date_planification = '2024-08-10'), 'F-ECO-2024-003', 190000, NULL, NULL, NULL, NULL, '2024-08-10', 'Non payé', 'Ouest (O)'), -- CORRIGÉ: mode est NULL
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_ecosol_nettoyage_2024 AND date_planification = '2024-09-15'), 'F-ECO-2024-004', 320000, 'Virement', NULL, NULL, '2024-09-18', '2024-09-15', 'Payé', 'Ouest (O)');

-- Factures pour 2025 (Contrat REF-ECO-002)
INSERT INTO Facture (planning_detail_id, reference_facture, montant, mode, etablissemnt_payeur, numero_cheque, date_paiement, date_traitement, etat, axe) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_ecosol_ordure_2025 AND date_planification = '2025-03-10'), 'F-ECO-2025-001', 95000, 'Mobile Money', NULL, NULL, '2025-03-10', '2025-03-10', 'Payé', 'Ouest (O)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_ecosol_derat_2025 AND date_planification = '2025-03-15'), 'F-ECO-2025-002', 210000, NULL, NULL, NULL, NULL, '2025-03-15', 'Non payé', 'Ouest (O)'), -- CORRIGÉ: mode est NULL
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_ecosol_ordure_2025 AND date_planification = '2025-07-10'), 'F-ECO-2025-003', 95000, 'Espèce', NULL, NULL, '2025-07-10', '2025-07-10', 'Payé', 'Ouest (O)');

-- TechInnov SARL (Sud (S))
-- Factures pour 2024 (Contrat REF-TECH-001 & REF-TECH-002)
INSERT INTO Facture (planning_detail_id, reference_facture, montant, mode, etablissemnt_payeur, numero_cheque, date_paiement, date_traitement, etat, axe) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_tech_termites_2024 AND date_planification = '2024-07-15'), 'F-TECH-2024-001', 550000, 'Virement', NULL, NULL, '2024-07-18', '2024-07-15', 'Payé', 'Sud (S)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_tech_fumigation_2024 AND date_planification = '2024-07-20'), 'F-TECH-2024-002', 280000, 'Espèce', NULL, NULL, '2024-07-20', '2024-07-20', 'Payé', 'Sud (S)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_tech_nettoyage_2024 AND date_planification = '2024-08-01'), 'F-TECH-2024-003', 350000, NULL, NULL, NULL, NULL, '2024-08-01', 'Non payé', 'Sud (S)'), -- CORRIGÉ: mode est NULL
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_tech_ordure_2024 AND date_planification = '2024-08-05'), 'F-TECH-2024-004', 100000, 'Chèque', 'MCB', 'CHQ-001122', '2024-08-10', '2024-08-05', 'Payé', 'Sud (S)');

-- Factures pour 2025 (Contrat REF-TECH-003)
INSERT INTO Facture (planning_detail_id, reference_facture, montant, mode, etablissemnt_payeur, numero_cheque, date_paiement, date_traitement, etat, axe) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_tech_termites_2024 AND date_planification = '2025-01-15'), 'F-TECH-2025-001', 550000, 'Virement', NULL, NULL, '2025-01-15', '2025-01-15', 'Payé', 'Sud (S)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_tech_fumigation_2024 AND date_planification = '2025-01-20'), 'F-TECH-2025-002', 280000, NULL, NULL, NULL, NULL, '2025-01-20', 'Non payé', 'Sud (S)'), -- CORRIGÉ: mode est NULL
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_tech_derat_2025 AND date_planification = '2025-02-01'), 'F-TECH-2025-003', 160000, 'Mobile Money', NULL, NULL, '2025-02-01', '2025-02-01', 'Payé', 'Sud (S)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_tech_desinf_2025 AND date_planification = '2025-02-10'), 'F-TECH-2025-004', 230000, 'Espèce', NULL, NULL, '2025-02-10', '2025-02-10', 'Payé', 'Sud (S)'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_tech_termites_2024 AND date_planification = '2025-07-15'), 'F-TECH-2025-005', 550000, NULL, NULL, NULL, NULL, '2025-07-15', 'À venir', 'Sud (S)'); -- CORRIGÉ: mode est NULL

-- Insertion des historiques de prix (pour tester la fonctionnalité de COALESCE)
-- Changement de prix pour F-DUP-2024-003 (de 150000 à 160000)
INSERT INTO Historique_prix (facture_id, old_amount, new_amount, change_date, changed_by) VALUES
((SELECT facture_id FROM Facture WHERE reference_facture = 'F-DUP-2024-003'), 150000, 160000, '2024-04-01 10:00:00', 'System');

-- Changement de prix pour F-MAR-2024-003 (de 180000 à 190000)
INSERT INTO Historique_prix (facture_id, old_amount, new_amount, change_date, changed_by) VALUES
((SELECT facture_id FROM Facture WHERE reference_facture = 'F-MAR-2024-003'), 180000, 190000, '2024-08-01 14:30:00', 'Admin_Plan');

-- Changement de prix pour F-GLOB-2025-002 (de 250000 à 260000)
INSERT INTO Historique_prix (facture_id, old_amount, new_amount, change_date, changed_by) VALUES
((SELECT facture_id FROM Facture WHERE reference_facture = 'F-GLOB-2025-002'), 250000, 260000, '2025-02-01 09:00:00', 'System');


-- Insertion des remarques
INSERT INTO Remarque (client_id, planning_detail_id, facture_id, contenu, issue, action) VALUES
((SELECT client_id FROM Client WHERE nom = 'Dupont' AND prenom = 'Jean'),
 (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_derat_2023 AND date_planification = '2023-07-01'),
 (SELECT facture_id FROM Facture WHERE reference_facture = 'F-DUP-2024-005'), -- NOTE: ceci est une incohérence délibérée pour montrer le lien, mais le planning est de 2023
 'Traitement dératisation effectué, client satisfait.', NULL, 'Vérification des appâts, aucun signe de rongeurs.'),
((SELECT client_id FROM Client WHERE nom = 'Martin' AND prenom = 'Sophie'),
 (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_martin_derat_2024 AND date_planification = '2024-07-05'),
 (SELECT facture_id FROM Facture WHERE reference_facture = 'F-MAR-2024-003'),
 'Problème d''accès à une zone, traitement partiel.', 'Accès bloqué par des meubles lourds.', 'Planification d''une nouvelle intervention pour la zone non traitée.'),
((SELECT client_id FROM Client WHERE nom = 'GlobalCorp'),
 (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_termites_2025 AND date_planification = '2025-07-15'),
 (SELECT facture_id FROM Facture WHERE reference_facture = 'F-GLOB-2025-003'),
 'Traitement anti-termites semestriel effectué.', NULL, 'Application du produit sur les fondations et zones à risque.'),
((SELECT client_id FROM Client WHERE nom = 'TechInnov SARL'),
 (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_tech_fumigation_2024 AND date_planification = '2024-07-20'),
 (SELECT facture_id FROM Facture WHERE reference_facture = 'F-TECH-2024-002'),
 'Fumigation effectuée avec succès, site sécurisé.', NULL, 'Utilisation de fumigènes spécifiques, aération post-traitement.');


-- Insertion des signalements
INSERT INTO Signalement (planning_detail_id, motif, type) VALUES
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_ordure_2025 AND date_planification = '2025-09-10'), 'Intempéries, forte pluie.', 'Décalage'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_martin_desinf_2025 AND date_planification = '2025-10-20'), 'Client a demandé un report.', 'Décalage'),
((SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_fumigation_2025 AND date_planification = '2025-07-20'), 'Équipe disponible plus tôt que prévu.', 'Avancement');


-- Insertion de l'historique (pour les traitements, factures et signalements)
-- Historique pour un traitement effectué et facturé
INSERT INTO Historique (facture_id, planning_detail_id, signalement_id, date_historique, contenu, issue, action) VALUES
((SELECT facture_id FROM Facture WHERE reference_facture = 'F-DUP-2024-001'),
 (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_dupont_desins_2024 AND date_planification = '2024-02-05'),
 NULL,
 '2024-02-05 17:00:00',
 'Traitement de désinsectisation effectué et facture émise.',
 NULL,
 'Intervention standard.'),
((SELECT facture_id FROM Facture WHERE reference_facture = 'F-MAR-2025-002'), -- Facture non payée
 (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_martin_desinf_2025 AND date_planification = '2025-04-20'),
 NULL,
 '2025-04-20 11:30:00',
 'Traitement de désinfection effectué, facture émise mais impayée.',
 NULL,
 'Rappel de paiement à envoyer.'),
((SELECT facture_id FROM Facture WHERE reference_facture = 'F-GLOB-2025-003'),
 (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_termites_2025 AND date_planification = '2025-07-15'),
 (SELECT signalement_id FROM Signalement WHERE planning_detail_id = (SELECT planning_detail_id FROM PlanningDetails WHERE planning_id = @planning_id_globalcorp_fumigation_2025 AND date_planification = '2025-07-20')), -- Signalement d'avancement
 '2025-07-15 10:00:00',
 'Traitement anti-termites effectué, facture payée. Avancement du planning noté.',
 NULL,
 'Intervention anticipée suite à la disponibilité de l''équipe.');
