import asyncio
import aiomysql

async def regrouper_traitements():
    """Récupère et affiche les traitements regroupés par catégorie."""

    # Configuration de la connexion à la base de données
    conn = await aiomysql.connect(
        host="votre_hôte",
        user="votre_utilisateur",
        password="votre_mot_de_passe",
        db="Planificator",
        autocommit=True,  # Important pour les requêtes qui modifient les données
    )

    try:
        cur = await conn.cursor()

        # Requête SQL pour regrouper les traitements par catégorie
        query = """
        SELECT 
            categorieTraitement,
            GROUP_CONCAT(typeTraitement) AS traitements
        FROM 
            TypeTraitement
        GROUP BY 
            categorieTraitement;
        """

        await cur.execute(query)

        # Récupération des résultats
        resultats = await cur.fetchall()

        # Affichage des résultats
        for categorie, traitements in resultats:
            print(f"Catégorie: {categorie}, Traitements: {traitements}")

    finally:
        # Fermeture du curseur et de la connexion
        await cur.close()
        conn.close()

# Exécution de la fonction asynchrone
asyncio.run(regrouper_traitements())