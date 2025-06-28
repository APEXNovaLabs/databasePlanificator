# Dans Contrat/signalement.py
import aiomysql
from datetime import date # Si vous utilisez des objets date pour les détails de planification

async def create_signalement(pool, planning_detail_id, motif, type_signalement):
    conn = None # Initialiser la connexion à None
    try:
        conn = await pool.acquire() # Acquérir une connexion du pool
        async with conn.cursor() as cur: # Le curseur par défaut est suffisant pour l'INSERT
            await cur.execute(
                "INSERT INTO Signalement (planning_detail_id, motif, type) VALUES (%s, %s, %s)",
                (planning_detail_id, motif, type_signalement)
            )
            await conn.commit() # Valider explicitement la transaction
            return cur.lastrowid # Retourne l'ID de la dernière ligne insérée
    except Exception as e:
        print(f"Erreur lors de la création du signalement : {e}")
        return None # Retourne None en cas d'échec
    finally:
        if conn:
            pool.release(conn) # S'assurer que la connexion est toujours relâchée

async def read_signalement(pool, signalement_id):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur: # Essentiel : Utiliser DictCursor pour un accès par nom
            await cur.execute("""
                SELECT
                    s.signalement_id,
                    s.motif,
                    s.type,
                    s.date_creation, -- Ajout de la date de création du signalement
                    pd.planning_detail_id,
                    pd.date_planification, -- Date de planification spécifique du détail de planning
                    p.traitement_id, -- L'ID du traitement est généralement dans la table Planning
                    tt.typeTraitement AS nom_type_traitement -- Le nom du type de traitement
                FROM Signalement s
                JOIN PlanningDetails pd ON s.planning_detail_id = pd.planning_detail_id
                JOIN Planning p ON pd.planning_id = p.planning_id -- Jointure de PlanningDetails à Planning
                JOIN TypeTraitement tt ON p.id_type_traitement = tt.id_type_traitement -- Jointure de Planning à TypeTraitement
                WHERE s.signalement_id = %s
            """, (signalement_id,))
            return await cur.fetchone() # Retourne un dictionnaire ou None
    except Exception as e:
        print(f"Erreur lors de la lecture du signalement : {e}")
        return None # Retourne None en cas d'échec
    finally:
        if conn:
            pool.release(conn)

async def update_signalement(pool, signalement_id, planning_detail_id, motif, type_signalement):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE Signalement SET planning_detail_id = %s, motif = %s, type = %s WHERE signalement_id = %s",
                (planning_detail_id, motif, type_signalement, signalement_id)
            )
            await conn.commit() # Validation explicite
    except Exception as e:
        print(f"Erreur lors de la mise à jour du signalement : {e}")
    finally:
        if conn:
            pool.release(conn)

async def delete_signalement(pool, signalement_id):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Signalement WHERE signalement_id = %s", (signalement_id,))
            await conn.commit() # Validation explicite
    except Exception as e:
        print(f"Erreur lors de la suppression du signalement : {e}")
    finally:
        if conn:
            pool.release(conn)