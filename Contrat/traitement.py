import aiomysql


async def typestraitement(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SHOW COLUMNS FROM TypeTraitement LIKE 'typeTraitement'")
            resultat = await cursor.fetchone()
            if resultat:
                enum_str = resultat[1].split("'")[1::2]
                return enum_str
            else:
                return []

async def creation_traitement(pool, contrat_id, id_type_traitement):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES (%s, %s)", (contrat_id, id_type_traitement))
            await conn.commit()
            return cur.lastrowid

async def obtenir_types_traitement(pool):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor: # Use DictCursor here!
            await cursor.execute("SELECT id_type_traitement, typeTraitement FROM TypeTraitement ORDER BY typeTraitement")
            types_data = await cursor.fetchall() # This will be a list of dictionaries like [{'id_type_traitement': 1, 'typeTraitement': 'Désinfection'}]
            return types_data
    except Exception as e:
        print(f"Erreur lors de la récupération des types de traitement : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)
async def read_traitement(pool, traitement_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Traitement WHERE traitement_id = %s", (traitement_id,))
            return await cur.fetchone()

async def update_traitement(pool, traitement_id, contrat_id, type_traitement):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Traitement SET contrat_id = %s, type_traitement = %s WHERE traitement_id = %s", (contrat_id, type_traitement, traitement_id))
            await conn.commit()

async def delete_traitement(pool, traitement_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Traitement WHERE traitement_id = %s", (traitement_id,))
            await conn.commit()