# Pour Historique
async def create_historique(pool, facture_id, contenu):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Historique (facture_id, contenu) VALUES (%s, %s)", (facture_id, contenu))
            await conn.commit()
            return cur.lastrowid

async def read_historique(pool, historique_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Historique WHERE historique_id = %s", (historique_id,))
            return await cur.fetchone()

async def update_historique(pool, historique_id, facture_id, contenu):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Historique SET facture_id = %s, contenu = %s WHERE historique_id = %s", (facture_id, contenu, historique_id))
            await conn.commit()

async def delete_historique(pool, historique_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Historique WHERE historique_id = %s", (historique_id,))
            await conn.commit()
