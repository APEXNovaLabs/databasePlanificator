-- Vues pour la facturation : "par traitement" et "totale par client/traitement"
-- Ces vues vous permettront d'extraire les données selon vos deux modèles de facture.

-- Vue 1: `VueFacturesParTraitement`
-- Donne un aperçu détaillé de chaque facture individuelle, incluant les infos client, contrat et traitement.
CREATE VIEW VueFacturesParTraitement AS
SELECT
    f.facture_id,
    f.montant,
    f.date_emission,
    f.date_echeance,
    f.etat_facture,
    f.remarque AS facture_remarque,
    pd.date_planification AS date_traitement_effectue,
    pd.statut AS statut_planning,
    tt.typeTraitement,
    c.nom AS client_nom,
    c.prenom AS client_prenom_ou_responsable,
    c.email AS client_email,
    c.telephone AS client_telephone,
    c.adresse AS client_adresse,
    c.categorie AS client_categorie,
    co.contrat_id,
    co.date_contrat,
    co.date_debut AS contrat_date_debut,
    co.date_fin_contrat AS contrat_date_fin,
    co.duree AS contrat_duree
FROM
    Factures f
JOIN
    PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id
JOIN
    Planning p ON pd.planning_id = p.planning_id
JOIN
    Traitement t ON p.traitement_id = t.traitement_id
JOIN
    TypesTraitement tt ON t.id_type_traitement = tt.id_type_traitement
JOIN
    Contrats co ON t.contrat_id = co.contrat_id
JOIN
    Clients c ON co.client_id = c.client_id;


-- Vue 2: `VueFacturesTotalesParClientEtTraitement`
-- Agrège le montant total facturé pour un client pour un type de traitement donné sur une période (mois/année).
-- Utile pour générer des factures récapitulatives.
CREATE VIEW VueFacturesTotalesParClientEtTraitement AS
SELECT
    c.client_id,
    c.nom AS client_nom,
    c.prenom AS client_prenom_ou_responsable,
    tt.typeTraitement,
    YEAR(f.date_emission) AS annee_facture,
    MONTH(f.date_emission) AS mois_facture,
    SUM(f.montant) AS montant_total_facture,
    COUNT(f.facture_id) AS nombre_de_factures_individuelles
FROM
    Factures f
JOIN
    PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id
JOIN
    Planning p ON pd.planning_id = p.planning_id
JOIN
    Traitement t ON p.traitement_id = t.traitement_id
JOIN
    TypesTraitement tt ON t.id_type_traitement = tt.id_type_traitement
JOIN
    Contrats co ON t.contrat_id = co.contrat_id
JOIN
    Clients c ON co.client_id = c.client_id
GROUP BY
    c.client_id,
    tt.typeTraitement,
    YEAR(f.date_emission),
    MONTH(f.date_emission)
ORDER BY
    c.nom, annee_facture DESC, mois_facture DESC, tt.typeTraitement;


-- Vue 3: `VueFacturesTotalesParClient`
-- Agrège le montant total facturé pour un client sur une période donnée (mois/année), tous traitements confondus.
CREATE VIEW VueFacturesTotalesParClient AS
SELECT
    c.client_id,
    c.nom AS client_nom,
    c.prenom AS client_prenom_ou_responsable,
    YEAR(f.date_emission) AS annee_facture,
    MONTH(f.date_emission) AS mois_facture,
    SUM(f.montant) AS montant_total_client_mois
FROM
    Factures f
JOIN
    PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id
JOIN
    Planning p ON pd.planning_id = p.planning_id
JOIN
    Traitement t ON p.traitement_id = t.traitement_id
JOIN
    Contrats co ON t.contrat_id = co.contrat_id
JOIN
    Clients c ON co.client_id = c.client_id
GROUP BY
    c.client_id,
    YEAR(f.date_emission),
    MONTH(f.date_emission)
ORDER BY
    c.nom, annee_facture DESC, mois_facture DESC;

