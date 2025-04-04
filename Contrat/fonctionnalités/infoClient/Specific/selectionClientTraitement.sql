-- Script SQL pour sélectionner les informations d'un client et le nombre de traitements liés.

SET @client_id_selectionne = VOTRE_ID_CLIENT; -- Veuillez remplacer VOTRE_ID_CLIENT par l'ID réel du client

SELECT
    cl.client_id,
    cl.nom AS nom_client,
    cl.prenom AS prenom_client,
    cl.email AS email_client,
    cl.telephone AS telephone_client,
    cl.adresse AS adresse_client,
    cl.date_ajout AS date_ajout_client,
    cl.categorie AS categorie_client,
    cl.axe AS axe_client,
    COUNT(t.traitement_id) AS nombre_traitements
FROM
    Client cl
LEFT JOIN
    Contrat ct ON cl.client_id = ct.client_id
LEFT JOIN
    Traitement t ON ct.contrat_id = t.contrat_id
WHERE
    cl.client_id = @client_id_selectionne
GROUP BY
    cl.client_id, cl.nom, cl.prenom, cl.email, cl.telephone, cl.adresse, cl.date_ajout, cl.categorie, cl.axe;