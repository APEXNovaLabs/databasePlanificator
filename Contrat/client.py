from datetime import date

import aiomysql


async def obtenir_categories(pool, table_name, column_name):
    conn = None
    try:
        conn = await pool.acquire()
        # Crucial: Use aiomysql.DictCursor to get results as dictionaries
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            # Query INFORMATION_SCHEMA to get ENUM values for the specified column
            query = """
                SELECT COLUMN_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s
            """
            await cursor.execute(query, (table_name, column_name))
            result = await cursor.fetchone() # This will be a dictionary or None

            if result and 'COLUMN_TYPE' in result and result['COLUMN_TYPE'].startswith("enum("):
                enum_str = result['COLUMN_TYPE']
                # Extract values from the string: "enum('val1','val2')" -> ['val1', 'val2']
                # Remove "enum(" and ")" then split by comma and strip quotes
                enum_values = [val.strip("'") for val in enum_str[5:-1].split(',')]
                return enum_values
            return [] # Return an empty list if column not found or not an ENUM
    except Exception as e:
        print(f"Erreur lors de la récupération des catégories pour la table '{table_name}' et la colonne '{column_name}' : {e}")
        return [] # Return an empty list on error
    finally:
        if conn:
            pool.release(conn)

async def create_client(pool, nom, prenom, email, telephone, adresse, nif, stat, categorie, axe):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Client (nom, prenom, email, telephone, adresse, nif, stat, date_ajout, categorie, axe) VALUES (%s ,%s, %s,%s, %s, %s, %s, %s, %s, %s)", (nom, prenom, email, telephone, adresse, nif, stat,date.today(), categorie, axe))
            await conn.commit()
            return cur.lastrowid  # Retourne l'ID du client créé

async def read_client(pool, client_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Client WHERE client_id = %s", (client_id,))
            return await cur.fetchone()

async def update_client(pool, client_id, nom, prenom, email, telephone, adresse, nif, stat, categorie, axe):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Client SET nom = %s, prenom = %s, email = %s, telephone = %s, adresse = %s, nif = %s, stat = %s, categorie = %s, axe = %s WHERE client_id = %s", (nom, prenom, email, telephone, adresse, nif, stat, categorie, axe, client_id))
            await conn.commit()

async def delete_client(pool, client_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Client WHERE client_id = %s", (client_id,))
            await conn.commit()