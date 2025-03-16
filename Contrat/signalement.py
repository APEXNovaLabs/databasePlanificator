# Pour avancement
async def create_avancement(pool, traitement_id, motif, type_avancement):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Avancement (traitement_id, motif, type) VALUES (%s, %s, %s)", (traitement_id, motif, type_avancement))
            await conn.commit()
            return cur.lastrowid

async def read_avancement(pool, avancement_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Avancement WHERE avancement_id = %s", (avancement_id,))
            return await cur.fetchone()

async def update_avancement(pool, avancement_id, traitement_id, motif, type_avancement):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Avancement SET traitement_id = %s, motif = %s, type = %s WHERE avancement_id = %s", (traitement_id, motif, type_avancement, avancement_id))
            await conn.commit()

async def delete_avancement(pool, avancement_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Avancement WHERE avancement_id = %s", (avancement_id,))
            await conn.commit()

