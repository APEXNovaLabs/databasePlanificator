# Pour avancement
async def create_signalement(pool, planning_detail_id, motif, type_signalement):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Signalement (planning_detail_id, motif, type) VALUES (%s, %s, %s)", (planning_detail_id, motif, type_signalement))
            await conn.commit()
            return cur.lastrowid

async def read_signalement(pool, signalement_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT s.signalement_id, s.motif, s.type,
                       pd.planning_detail_id, pd.traitement_id, pd.date_debut, pd.date_fin,
                       t.type_traitement
                FROM Signalement s
                JOIN PlanningDetails pd ON s.planning_detail_id = pd.planning_detail_id
                JOIN Traitement t ON pd.traitement_id = t.traitement_id
                WHERE s.signalement_id = %s
            """, (signalement_id,))
            return await cur.fetchone()

async def update_signalement(pool, signalement_id, planning_detail_id, motif, type_signalement):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Signalement SET planning_detail_id = %s, motif = %s, type = %s WHERE signalement_id = %s", (planning_detail_id, motif, type_signalement, signalement_id))
            await conn.commit()

async def delete_signalement(pool, signalement_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Signalement WHERE signalement_id = %s", (signalement_id,))
            await conn.commit()
