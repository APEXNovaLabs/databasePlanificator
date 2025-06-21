import aiomysql

async def DBConnection():
    """
    Demande les informations de connexion à l'utilisateur et crée un pool de connexions.
    """
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

    # Créer le pool de connexions
    try:
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=True,
            maxsize=10
        )
        print("Pool de connexions à la base de données créé avec succès.")
        return pool
    except Exception as e:
        print(f"Erreur lors de la création du pool de connexions : {e}")
        return None