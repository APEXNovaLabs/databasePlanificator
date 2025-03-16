# Pour la facture
async def create_facture(pool, traitement_id, montant, date_traitement, axe, remarque):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Facture (traitement_id, montant, date_traitement, axe, remarque) VALUES (%s, %s, %s, %s, %s)", (traitement_id, montant, date_traitement, axe, remarque))
            await conn.commit()
            return cur.lastrowid

# Obtention de l'axe mentionnée dans l'ajout du contrat
async def obtenir_axe_contrat(pool, contrat_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT axe FROM Contrat WHERE contrat_id = %s", (contrat_id,))
            resultat = await cursor.fetchone()
            if resultat:
                return resultat[0]
            else:
                return None


async def read_facture(pool, facture_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Facture WHERE facture_id = %s", (facture_id,))
            return await cur.fetchone()

async def update_facture(pool, facture_id, traitement_id, montant, date_traitement, axe, remarque):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Facture SET traitement_id = %s, montant = %s, date_traitement = %s, axe = %s, remarque = %s WHERE facture_id = %s", (traitement_id, montant, date_traitement, axe, remarque, facture_id))
            await conn.commit()

async def delete_facture(pool, facture_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Facture WHERE facture_id = %s", (facture_id,))
            await conn.commit()
