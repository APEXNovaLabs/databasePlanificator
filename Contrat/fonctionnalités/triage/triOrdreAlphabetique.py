import aiomysql
import asyncio

async def tri_alphabetique_clients(pool):
    """Trie les noms des clients par ordre alphabétique."""

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT nom FROM Client ORDER BY nom ASC")
            clients = await cur.fetchall()

            if clients:
                print("Liste des clients par ordre alphabétique :")
                for nom in clients:
                    print(nom[0])
            else:
                print("Aucun client trouvé.")

async def main():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='votre_utilisateur', password='votre_mot_de_passe',
                                      db='Planificator', autocommit=True)

    await tri_alphabetique_clients(pool)

    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())