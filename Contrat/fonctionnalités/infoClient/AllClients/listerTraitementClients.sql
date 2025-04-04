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
    COUNT(tr.traitement_id) AS nombre_traitements
FROM
    Client cl
LEFT JOIN
    Contrat ct ON cl.client_id = ct.client_id
LEFT JOIN
    Traitement tr ON ct.contrat_id = tr.traitement_id
GROUP BY
    cl.client_id, cl.nom, cl.prenom, cl.email, cl.telephone, cl.adresse, cl.date_ajout, cl.categorie, cl.axe
ORDER BY
    cl.nom, cl.prenom;