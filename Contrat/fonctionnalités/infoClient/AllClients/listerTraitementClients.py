import asyncio
import aiomysql

async def get_db_credentials():
    """Demande à l'utilisateur les informations de connexion à la base de données."""
    host = input("Entrez l'adresse du serveur MySQL (par exemple, localhost): ")
    port_str = input("Entrez le port du serveur MySQL (par défaut: 3306): ")
    try:
        port = int(port_str) if port_str else 3306
    except ValueError:
        print("Port invalide, utilisation de la valeur par défaut (3306).")
        port = 3306
    user = input("Entrez le nom d'utilisateur MySQL: ")
    password = input("Entrez le mot de passe MySQL: ")
    database = input("Entrez le nom de la base de données MySQL (par exemple, Planificator): ")
    return host, port, user, password, database

async def get_all_clients_with_treatment_count(host: str, port: int, user: str, password: str, database: str):
    """
    Récupère les informations de tous les clients et le nombre de traitements liés à chacun.

    Args:
        host: L'adresse du serveur MySQL.
        port: Le port du serveur MySQL.
        user: Le nom d'utilisateur MySQL.
        password: Le mot de passe MySQL.
        database: Le nom de la base de données MySQL.

    Returns:
        Une liste de dictionnaires, où chaque dictionnaire contient les informations d'un client
        et le nombre de traitements liés. Retourne None en cas d'erreur.
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
        GROUP BY
            cl.client_id, cl.nom, cl.prenom, cl.email, cl.telephone, cl.adresse, cl.date_ajout, cl.categorie, cl.axe
        ORDER BY
            cl.nom, cl.prenom;
        """
        await cursor.execute(sql)
        results = await cursor.fetchall()
        return results

    except aiomysql.Error as e:
        print(f"Erreur MySQL: {e}")
        return None
    finally:
        if cursor:
            await cursor.close()
        if conn:
            conn.close()

async def main():
    host, port, user, password, database = await get_db_credentials()

    all_clients_info = await get_all_clients_with_treatment_count(host, port, user, password, database)

    if all_clients_info:
        print("\nListe de tous les clients et leur nombre de traitements :")
        for client_info in all_clients_info:
            print(f"ID: {client_info['client_id']}, Nom: {client_info['nom_client']}, Prénom: {client_info['prenom_client']}, Traitements: {client_info['nombre_traitements']}")
    else:
        print("\nImpossible de récupérer la liste des clients et leurs traitements.")

if __name__ == "__main__":
    asyncio.run(main())