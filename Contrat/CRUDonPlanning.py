import aiomysql
import asyncio
from datetime import datetime, timedelta

async def create_planning(pool, traitement_id, redondance, date_debut_planification, duree_traitement=12, unite_duree='mois'):
    """Crée un planning pour un traitement donné."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Calculer la date de fin de la planification
            if unite_duree == 'mois':
                date_fin_planification = date_debut_planification + timedelta(days=duree_traitement * 30)  # Approximation
            elif unite_duree == 'années':
                date_fin_planification = date_debut_planification + timedelta(days=duree_traitement * 365)
            else:
                raise ValueError("Unité de durée non valide.")

            await cur.execute("""
                INSERT INTO Planning (traitement_id, redondance, date_debut_planification, date_fin_planification, duree_traitement, unite_duree)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (traitement_id, redondance, date_debut_planification, date_fin_planification, duree_traitement, unite_duree))
            await conn.commit()
            return cur.lastrowid


async def obtenir_redondances(pool):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:  # Use DictCursor here!
            # If 'redondance' is an ENUM column in your Planning table:
            query = """
                    SELECT COLUMN_TYPE
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE() \
                      AND TABLE_NAME = 'Planning' \
                      AND COLUMN_NAME = 'redondance' \
                    """
            await cursor.execute(query)
            result = await cursor.fetchone()
            if result and 'COLUMN_TYPE' in result and result['COLUMN_TYPE'].startswith("enum("):
                enum_str = result['COLUMN_TYPE']
                return [val.strip("'") for val in enum_str[len("enum("):-1].split(',')]

            # OR, if redondances come from a separate lookup table (e.g., `RedondanceOptions`):
            # await cursor.execute("SELECT redondance_name FROM RedondanceOptions ORDER BY redondance_name")
            # return [row['redondance_name'] for row in await cursor.fetchall()]

            return []  # Return empty list if no redondances found
    except Exception as e:
        print(f"Erreur lors de la récupération des redondances : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)

async def read_planning(pool, planning_id):
    """Lit un planning à partir de son ID."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Planning WHERE planning_id = %s", (planning_id,))
            return await cur.fetchone()

async def update_planning(pool, planning_id, traitement_id, redondance, date_debut_planification, date_fin_planification, duree_traitement, unite_duree):
    """Modifie un planning existant."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                UPDATE Planning SET traitement_id = %s, redondance = %s, date_debut_planification = %s, date_fin_planification = %s, duree_traitement = %s, unite_duree = %s
                WHERE planning_id = %s
            """, (traitement_id, redondance, date_debut_planification, date_fin_planification, duree_traitement, unite_duree, planning_id))
            await conn.commit()

async def delete_planning(pool, planning_id):
    """Supprime un planning à partir de son ID."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Planning WHERE planning_id = %s", (planning_id,))
            await conn.commit()