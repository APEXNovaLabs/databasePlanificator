from datetime import date

async def obtenir_categories(pool, table_name, column_name):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}'")
            resultat = await cursor.fetchone()
            if resultat:
                enum_str = resultat[1].split("'")[1::2]
                return enum_str
            else:
                return []

async def create_client(pool, nom, prenom, email, telephone, adresse, categorie, axe):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Client (nom, prenom, email, telephone, adresse, date_ajout, categorie, axe) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (nom, prenom, email, telephone, adresse, date.today(), categorie, axe))
            await conn.commit()
            return cur.lastrowid  # Retourne l'ID du client créé

async def read_client(pool, client_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Client WHERE client_id = %s", (client_id,))
            return await cur.fetchone()

async def update_client(pool, client_id, nom, prenom, email, telephone, adresse, categorie, axe):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Client SET nom = %s, prenom = %s, email = %s, telephone = %s, adresse = %s, categorie = %s, axe = %s WHERE client_id = %s", (nom, prenom, email, telephone, adresse, categorie, axe, client_id))
            await conn.commit()

async def delete_client(pool, client_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Client WHERE client_id = %s", (client_id,))
            await conn.commit()