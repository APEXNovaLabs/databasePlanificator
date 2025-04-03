import asyncio
import aiomysql

async def get_db_credentials():
    """Demande à l'utilisateur les informations de connexion à la base de données."""
    host = input("Entrez l'adresse du serveur MySQL (Pressez sur entrer si localhost): ") or "localhost"
    port_str = input("Entrez le port du serveur MySQL (par défaut: 3306): ")
    try:
        port = int(port_str) if port_str else 3306
    except ValueError:
        print("Port invalide, utilisation de la valeur par défaut (3306).")
        port = 3306
    user = input("Entrez le nom d'utilisateur MySQL: ")
    password = input("Entrez le mot de passe MySQL: ")
    database = input("Entrez le nom de la base de données MySQL: ") or "Planificator"
    return host, port, user, password, database

async def get_client_id_to_search():
    """Demande à l'utilisateur l'ID du client à rechercher."""
    while True:
        client_id_str = input("Entrez l'ID du client que vous souhaitez rechercher: ")
        try:
            client_id = int(client_id_str)
            return client_id
        except ValueError:
            print("ID de client invalide. Veuillez entrer un nombre entier.")

async def get_client_info_with_treatment_count(host: str, port: int, user: str, password: str, database: str, client_id: int):
    """
    Récupère les informations d'un client et le nombre de traitements liés en utilisant aiomysql.

    Args:
        host: L'adresse du serveur MySQL.
        port: Le port du serveur MySQL.
        user: Le nom d'utilisateur MySQL.
        password: Le mot de passe MySQL.
        database: Le nom de la base de données MySQL.
        client_id: L'ID du client à interroger.

    Returns:
        Un dictionnaire contenant les informations du client et le nombre de traitements,
        ou None si le client n'est pas trouvé.
    """
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=host,
                                       port=port,
                                       user=user,
                                       password=password,
                                       db=database,
                                       autocommit=True)
        cursor = await conn.cursor(aiomysql.DictCursor)

        sql = """
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
            Traitement tr ON ct.contrat_id = tr.contrat_id
        WHERE
            cl.client_id = %s
        GROUP BY
            cl.client_id, cl.nom, cl.prenom, cl.email, cl.telephone, cl.adresse, cl.date_ajout, cl.categorie, cl.axe
        """
        await cursor.execute(sql, (client_id,))
        result = await cursor.fetchone()
        return result

    except aiomysql.Error as e:
        print(f"Erreur MySQL: {e}")
        return None
    finally:
        if cursor:
            await cursor.close()
        if conn:
            await conn.wait_closed()
async def main():
    host, port, user, password, database = await get_db_credentials()
    client_id_a_rechercher = await get_client_id_to_search()

    client_info = await get_client_info_with_treatment_count(host, port, user, password, database, client_id_a_rechercher)

    if client_info:
        print(f"\nInformations du client (ID: {client_info['client_id']}):")
        print(f"  Nom: {client_info['nom_client']}")
        print(f"  Prénom: {client_info['prenom_client']}")
        print(f"  Email: {client_info['email_client']}")
        print(f"  Téléphone: {client_info['telephone_client']}")
        print(f"  Adresse: {client_info['adresse_client']}")
        print(f"  Date d'ajout: {client_info['date_ajout_client']}")
        print(f"  Catégorie: {client_info['categorie_client']}")
        print(f"  Axe: {client_info['axe_client']}")
        print(f"  Nombre de traitements liés: {client_info['nombre_traitements']}")
    else:
        print(f"\nAucun client trouvé avec l'ID: {client_id_a_rechercher}")

if __name__ == "__main__":
    asyncio.run(main())