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
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT typeTraitement FROM TypeTraitement")
            resultats = await cursor.fetchall()
            return [resultat[0] for resultat in resultats]

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