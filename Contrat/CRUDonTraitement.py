import aiomysql


async def creation_traitement(pool, contrat_id: int, id_type_traitement: int) -> int | None:
    """
    Crée un nouveau traitement lié à un contrat et un type de traitement.

    Args:
        pool: Le pool de connexions aiomysql.
        contrat_id (int): L'ID du contrat associé.
        id_type_traitement (int): L'ID du type de traitement.

    Returns:
        int | None: L'ID du traitement créé, ou None en cas d'échec.
    """
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
        return None
    finally:
        if conn:
            pool.release(conn)

async def read_traitement(pool, traitement_id: int) -> dict | None:
    """
    Lit les informations d'un traitement spécifique par son ID.

    Args:
        pool: Le pool de connexions aiomysql.
        traitement_id (int): L'ID du traitement.

    Returns:
        dict | None: Un dictionnaire contenant les informations du traitement, ou None si non trouvé ou en cas d'erreur.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur:
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
            return await cur.fetchone()
    except Exception as e:
        print(f"Erreur lors de la lecture du traitement (ID: {traitement_id}) : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)

async def update_traitement(pool, traitement_id: int, contrat_id: int, id_type_traitement: int) -> int:
    """
    Modifie un traitement existant.

    Args:
        pool: Le pool de connexions aiomysql.
        traitement_id (int): L'ID du traitement à modifier.
        contrat_id (int): Le nouvel ID du contrat.
        id_type_traitement (int): Le nouvel ID du type de traitement.

    Returns:
        int: Le nombre de lignes affectées (1 si succès, 0 sinon).
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE Traitement SET contrat_id = %s, id_type_traitement = %s WHERE traitement_id = %s",
                (contrat_id, id_type_traitement, traitement_id)
            )
            await conn.commit()
            return cur.rowcount
    except Exception as e:
        print(f"Erreur lors de la modification du traitement (ID: {traitement_id}) : {e}")
        return 0
    finally:
        if conn:
            pool.release(conn)

async def delete_traitement(pool, traitement_id: int) -> int:
    """
    Supprime un traitement existant.

    Args:
        pool: Le pool de connexions aiomysql.
        traitement_id (int): L'ID du traitement à supprimer.

    Returns:
        int: Le nombre de lignes supprimées (1 si succès, 0 sinon).
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Traitement WHERE traitement_id = %s", (traitement_id,))
            await conn.commit()
            return cur.rowcount
    except Exception as e:
        print(f"Erreur lors de la suppression du traitement (ID: {traitement_id}) : {e}")
        return 0
    finally:
        if conn:
            pool.release(conn)

async def obtenir_types_traitement(pool) -> list[dict]:
    """
    Récupère tous les types de traitement disponibles.

    Returns:
        list[dict]: Une liste de dictionnaires, chaque dictionnaire représentant un type de traitement.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT id_type_traitement, typeTraitement FROM TypeTraitement ORDER BY typeTraitement")
            types_data = await cursor.fetchall()
            return types_data
    except Exception as e:
        print(f"Erreur lors de la récupération des types de traitement : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)