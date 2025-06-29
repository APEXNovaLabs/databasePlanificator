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
    """Crée un nouveau traitement lié à un contrat et un type de traitement."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES (%s, %s)",
                (contrat_id, id_type_traitement)
            )
            await conn.commit()
            return cur.lastrowid
    except Exception as e:
        print(f"Erreur lors de la création du traitement : {e}")
        return None  # Retourne None en cas d'échec
    finally:
        if conn:
            pool.release(conn)


async def obtenir_types_traitement(pool):
    """Récupère tous les types de traitement disponibles depuis la table TypeTraitement."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor: # Utilisation de DictCursor, essentielle
            await cursor.execute("SELECT id_type_traitement, typeTraitement FROM TypeTraitement ORDER BY typeTraitement")
            types_data = await cursor.fetchall() # Ceci sera une liste de dictionnaires
            return types_data
    except Exception as e:
        print(f"Erreur lors de la récupération des types de traitement : {e}")
        return [] # Retourne une liste vide en cas d'erreur
    finally:
        if conn:
            pool.release(conn)


async def read_traitement(pool, traitement_id):
    """Lit les informations d'un traitement spécifique par son ID."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur: # Utilisation de DictCursor
            # Il est préférable de joindre avec TypeTraitement pour obtenir le nom du type de traitement
            # plutôt que juste l'id numérique.
            await cur.execute("""
                SELECT
                    t.traitement_id,
                    t.contrat_id,
                    t.id_type_traitement,
                    tt.typeTraitement AS nom_type_traitement
                FROM Traitement t
                JOIN TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement
                WHERE t.traitement_id = %s
            """, (traitement_id,))
            return await cur.fetchone() # Retourne un dictionnaire ou None
    except Exception as e:
        print(f"Erreur lors de la lecture du traitement (ID: {traitement_id}) : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)


async def update_traitement(pool, traitement_id, contrat_id, id_type_traitement): # Renommé type_traitement en id_type_traitement
    """Modifie un traitement existant."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            # Assurez-vous que la colonne dans la DB est bien 'id_type_traitement' et non 'type_traitement'
            await cur.execute(
                "UPDATE Traitement SET contrat_id = %s, id_type_traitement = %s WHERE traitement_id = %s",
                (contrat_id, id_type_traitement, traitement_id)
            )
            await conn.commit()
            return cur.rowcount # Retourne le nombre de lignes affectées (1 si succès, 0 sinon)
    except Exception as e:
        print(f"Erreur lors de la modification du traitement (ID: {traitement_id}) : {e}")
        return 0
    finally:
        if conn:
            pool.release(conn)


async def delete_traitement(pool, traitement_id):
    """Supprime un traitement existant."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Traitement WHERE traitement_id = %s", (traitement_id,))
            await conn.commit()
            return cur.rowcount # Retourne le nombre de lignes supprimées
    except Exception as e:
        print(f"Erreur lors de la suppression du traitement (ID: {traitement_id}) : {e}")
        return 0
    finally:
        if conn:
            pool.release(conn)

