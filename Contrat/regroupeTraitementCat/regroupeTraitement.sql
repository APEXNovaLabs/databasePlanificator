SELECT
    categorieTraitement,
    GROUP_CONCAT(typeTraitement) AS traitements
FROM
    TypeTraitement
GROUP BY
    categorieTraitement;