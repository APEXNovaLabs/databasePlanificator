import asyncio
import aiomysql
from datetime import date, datetime, timedelta

async def create_historique(pool, traitement_id, contenu, date_traitement=None):
    """Crée un historique pour un traitement donné."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            if date_traitement is None:
                date_traitement = date.today()
            await cur.execute("INSERT INTO Historique (traitement_id, contenu, date_traitement) VALUES (%s, %s, %s)", (traitement_id, contenu, date_traitement))
            await conn.commit()
            return cur.lastrowid

async def read_historique(pool, historique_id):
    """Lit un historique à partir de son ID."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Historique WHERE historique_id = %s", (historique_id,))
            return await cur.fetchone()

async def update_historique(pool, historique_id, contenu, date_traitement):
    """Modifie un historique existant."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Historique SET contenu = %s, date_traitement = %s WHERE historique_id = %s", (contenu, date_traitement, historique_id))
            await conn.commit()

async def delete_historique(pool, historique_id):
    """Supprime un historique à partir de son ID."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Historique WHERE historique_id = %s", (historique_id,))
            await conn.commit()

async def get_historique_for_traitement(pool, traitement_id):
    """Récupère l'historique d'un traitement spécifique."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Historique WHERE traitement_id = %s", (traitement_id,))
            return await cur.fetchall()

async def create_historique_for_planning(pool, planning_id):
    """Crée automatiquement un historique pour chaque traitement avec un planning."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT traitement_id FROM Planning WHERE planning_id = %s", (planning_id,))
            traitement_id = await cur.fetchone()
            if traitement_id:
                traitement_id = traitement_id[0]
                await create_historique(pool, traitement_id, "Historique créé automatiquement lors de la planification.")

async def afficher_historique_client(pool, client_id):
    """Affiche l'historique de tous les traitements d'un client."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT h.* FROM Historique h
                JOIN Traitement t ON h.traitement_id = t.traitement_id
                JOIN Contrat c ON t.contrat_id = c.contrat_id
                WHERE c.client_id = %s
            """, (client_id,))
            historiques = await cur.fetchall()
            for historique in historiques:
                print(f"ID: {historique[0]}, Traitement ID: {historique[1]}, Contenu: {historique[2]}, Date: {historique[3]}")

async def main():
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

    try:
        # Création d'un historique pour un traitement
        historique_id = await create_historique(pool, 1, "Traitement effectué avec succès.", date(2023, 11, 20))
        print(f"Historique créé avec l'ID: {historique_id}")

        # Lecture de l'historique
        historique = await read_historique(pool, historique_id)
        print(f"Historique lu: {historique}")

        # Modification de l'historique
        await update_historique(pool, historique_id, "Traitement modifié.", date(2023, 11, 21))
        print("Historique modifié.")

        # Récupération de l'historique pour un traitement
        historiques_traitement = await get_historique_for_traitement(pool, 1)
        print(f"Historique pour le traitement 1: {historiques_traitement}")

        # Création automatique de l'historique pour un planning
        await create_historique_for_planning(pool, 1)
        print("Historique créé pour le planning.")

        # Affichage de l'historique d'un client
        await afficher_historique_client(pool, 1)

        # Suppression de l'historique
        await delete_historique(pool, historique_id)
        print("Historique supprimé.")

    except aiomysql.OperationalError as e:
        print(f"Erreur de connexion à la base de données: {e}")
    except aiomysql.IntegrityError as e:
        print(f"Violation de contrainte d'intégrité: {e}")
    except ValueError as e:
        print(f"Erreur de valeur: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")

    finally:
        if pool:
            pool.close()
            await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())