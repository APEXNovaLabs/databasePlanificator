import aiomysql


async def DBConnection():
    # Connexion à la base de données
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

    finally:
        if pool:
            pool.close()
            await pool.wait_closed()
