import asyncio
import aiomysql

async def regrouper_traitements():
    """Here xD: Récupère et affiche les traitements regroupés par catégorie."""
    host = input("Hôte de la base de données (par défaut : localhost) : ")
    if not host:
        host = "localhost"

    port_str = input("Port de la base de données (par défaut : 3306) : ")
    if port_str:
        try:
            port = int(port_str)
        except ValueError:
            print("Port invalide. Utilisation du port par défaut 3306.")
            port = 3306
    else:
        port = 3306

    user = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    database = input("Nom de la base de données : ")

    try:
        # Créer le pool de connexions
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=True
        )

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

        await pool.execute(query)

        # Récupération des résultats
        resultats = await pool.fetchall()

        # Affichage des résultats
        for categorie, traitements in resultats:
            print(f"Catégorie: {categorie}, Traitements: {traitements}")


    finally:
        if pool:
            pool.close()
            await pool.wait_closed()


# Exécution de la fonction asynchrone
asyncio.run(regrouper_traitements())