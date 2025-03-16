async def create_contrat(pool, client_id, date_contrat, date_debut, date_fin, duree, categorie):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Contrat (client_id, date_contrat, date_debut, date_fin, duree, categorie) VALUES (%s, %s, %s, %s, %s, %s)", (client_id, date_contrat, date_debut, date_fin, duree, categorie))
            await conn.commit()
            return cur.lastrowid

async def read_contrat(pool, contrat_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Contrat WHERE contrat_id = %s", (contrat_id,))
            return await cur.fetchone()

async def update_contrat(pool, contrat_id, client_id, date_contrat, date_debut, date_fin, duree, categorie):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Contrat SET client_id = %s, date_contrat = %s, date_debut = %s, date_fin = %s, duree = %s, categorie = %s WHERE contrat_id = %s", (client_id, date_contrat, date_debut, date_fin, categorie, contrat_id))
            await conn.commit()

async def delete_contrat(pool, contrat_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Contrat WHERE contrat_id = %s", (contrat_id,))
            await conn.commit()

async def obtenir_duree_contrat(pool, contrat_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT duree FROM Contrat WHERE contrat_id = %s", (contrat_id,))
            resultat = await cursor.fetchone()
            if resultat:
                return resultat[0]
            else:
                return None

async def obtenir_axe_contrat(pool, contrat_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT axe FROM Contrat WHERE contrat_id = %s", (contrat_id,))
            resultat = await cursor.fetchone()
            if resultat:
                return resultat[0]
            else:
                return None
