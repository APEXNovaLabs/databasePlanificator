async def create_planning(pool, traitement_id, mois_debut, mois_fin, mois_pause, redondance):
    """Crée un planning pour un traitement donné."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Planning (traitement_id, mois_debut, mois_fin, mois_pause, redondance) VALUES (%s, %s, %s, %s, %s)", (traitement_id, mois_debut, mois_fin, mois_pause, redondance))
            await conn.commit()
            return cur.lastrowid

async def obtenir_redondances(pool):
    """Récupère les options de redondance disponibles."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SHOW COLUMNS FROM Planning LIKE 'redondance'")
            resultat = await cursor.fetchone()
            if resultat:
                enum_str = resultat[1].split("'")[1::2]
                return enum_str
            else:
                return []

async def read_planning(pool, planning_id):
    """Lit un planning à partir de son ID."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Planning WHERE planning_id = %s", (planning_id,))
            return await cur.fetchone()

async def update_planning(pool, planning_id, traitement_id, mois_debut, mois_fin, type_traitement, mois_pause, redondance):
    """Modifie un planning existant."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Planning SET traitement_id = %s, mois_debut = %s, mois_fin = %s, type_traitement = %s, mois_pause = %s, redondance = %s WHERE planning_id = %s", (traitement_id, mois_debut, mois_fin, type_traitement, mois_pause, redondance, planning_id))
            await conn.commit()

async def delete_planning(pool, planning_id):
    """Supprime un planning à partir de son ID."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Planning WHERE planning_id = %s", (planning_id,))
            await conn.commit()