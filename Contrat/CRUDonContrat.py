import aiomysql
from datetime import date

async def create_contrat(pool, client_id: int, date_contrat: date, date_debut: date, date_fin_contrat: str | None, duree: str, categorie: str, duree_contrat: int | None = None):
    """
    Crée un nouveau contrat dans la base de données.

    Args:
        pool: Le pool de connexions aiomysql.
        client_id (int): L'ID du client associé au contrat.
        date_contrat (date): La date de signature du contrat.
        date_debut (date): La date de début du contrat.
        date_fin_contrat (str | None): La date de fin du contrat sous forme de chaîne (peut être None si durée indéterminée).
                                        Doit être au format 'YYYY-MM-DD' ou une description textuelle.
        duree (str): La durée du contrat ('Indeterminee' ou 'Déterminée').
        categorie (str): La catégorie du contrat ('Nouveau' ou 'Renouvellement').
        duree_contrat (int | None): La durée du contrat en mois/années (INT dans la DB), ou None.

    Returns:
        int: L'ID du contrat nouvellement créé, ou None en cas d'échec.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            # Vérifier si duree est 'Indeterminée' et ajuster date_fin_contrat et duree_contrat
            if duree == 'Indeterminée':
                date_fin_contrat_db = None
                duree_contrat_db = None
            else:
                date_fin_contrat_db = date_fin_contrat
                duree_contrat_db = duree_contrat

            await cur.execute("""
                INSERT INTO Contrat (client_id, date_contrat, date_debut, date_fin, duree, categorie, duree_contrat)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (client_id, date_contrat, date_debut, date_fin_contrat_db, duree, categorie, duree_contrat_db))
            await conn.commit()
            return cur.lastrowid
    except Exception as e:
        print(f"Erreur lors de la création du contrat pour client {client_id}: {e}")
        return None
    finally:
        if conn:
            pool.release(conn)

async def read_contrat(pool, contrat_id: int):
    """
    Lit les détails d'un contrat spécifique à partir de son ID.

    Args:
        pool: Le pool de connexions aiomysql.
        contrat_id (int): L'ID du contrat à lire.

    Returns:
        dict: Un dictionnaire contenant les détails du contrat, ou None si non trouvé ou en cas d'erreur.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur: # Utilisation de DictCursor
            await cur.execute("""
                SELECT
                    c.contrat_id,
                    c.client_id,
                    cl.nom AS nom_client,
                    cl.prenom AS prenom_client,
                    cl.email AS email_client,
                    c.reference_contrat,
                    c.date_contrat,
                    c.date_debut,
                    c.date_fin,
                    c.statut_contrat,
                    c.duree,
                    c.categorie,
                    c.duree_contrat
                FROM Contrat c
                JOIN Client cl ON c.client_id = cl.client_id
                WHERE c.contrat_id = %s
            """, (contrat_id,))
            return await cur.fetchone() # Retourne un dictionnaire ou None
    except Exception as e:
        print(f"Erreur lors de la lecture du contrat (ID: {contrat_id}) : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)

async def update_contrat(pool, contrat_id: int, client_id: int, date_contrat: date, date_debut: date, date_fin_contrat: str | None, duree: str, categorie: str, duree_contrat: int | None = None):
    """
    Modifie un contrat existant dans la base de données.

    Args:
        pool: Le pool de connexions aiomysql.
        contrat_id (int): L'ID du contrat à modifier.
        client_id (int): Le nouvel ID du client.
        date_contrat (date): La nouvelle date de signature.
        date_debut (date): La nouvelle date de début.
        date_fin_contrat (str | None): La nouvelle date de fin sous forme de chaîne (peut être None).
                                        Doit être au format 'YYYY-MM-DD' ou une description textuelle.
        duree (str): La nouvelle durée ('Indeterminée' ou 'Déterminée').
        categorie (str): La nouvelle catégorie ('Nouveau' ou 'Renouvellement').
        duree_contrat (int | None): La nouvelle durée du contrat en mois/années (INT dans la DB), ou None.

    Returns:
        int: Le nombre de lignes affectées (1 en cas de succès, 0 sinon ou en cas d'erreur).
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            # Ajuster date_fin_contrat et duree_contrat en fonction de la valeur de 'duree'
            if duree == 'Indeterminée':
                date_fin_contrat_db = None
                duree_contrat_db = None
            else:
                date_fin_contrat_db = date_fin_contrat
                duree_contrat_db = duree_contrat

            await cur.execute("""
                UPDATE Contrat SET client_id = %s, date_contrat = %s, date_debut = %s, date_fin = %s,
                duree = %s, categorie = %s, duree_contrat = %s
                WHERE contrat_id = %s
            """, (client_id, date_contrat, date_debut, date_fin_contrat_db, duree, categorie, duree_contrat_db, contrat_id))
            await conn.commit()
            return cur.rowcount # Retourne 1 si mise à jour, 0 si contrat non trouvé
    except Exception as e:
        print(f"Erreur lors de la modification du contrat (ID: {contrat_id}) : {e}")
        return 0
    finally:
        if conn:
            pool.release(conn)

async def delete_contrat(pool, contrat_id: int):
    """
    Supprime un contrat de la base de données.

    Args:
        pool: Le pool de connexions aiomysql.
        contrat_id (int): L'ID du contrat à supprimer.

    Returns:
        int: Le nombre de lignes supprimées (1 en cas de succès, 0 sinon ou en cas d'erreur).
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Contrat WHERE contrat_id = %s", (contrat_id,))
            await conn.commit()
            return cur.rowcount # Retourne 1 si supprimé, 0 si contrat non trouvé
    except Exception as e:
        print(f"Erreur lors de la suppression du contrat (ID: {contrat_id}) : {e}")
        return 0
    finally:
        if conn:
            pool.release(conn)

async def obtenir_duree_contrat(pool, contrat_id: int):
    """
    Récupère la durée principale du contrat ('Indeterminee', 'Déterminée').

    Args:
        pool: Le pool de connexions aiomysql.
        contrat_id (int): L'ID du contrat.

    Returns:
        str: La valeur de la colonne 'duree' du contrat, ou None si non trouvé ou en cas d'erreur.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor: # Utilisation de DictCursor
            await cursor.execute("SELECT duree FROM Contrat WHERE contrat_id = %s", (contrat_id,))
            resultat = await cursor.fetchone()
            if resultat:
                return resultat['duree'] # Accès par clé de dictionnaire
            else:
                return None
    except Exception as e:
        print(f"Erreur lors de la récupération de la durée du contrat (ID: {contrat_id}) : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)

async def obtenir_axe_client_par_contrat(pool, contrat_id: int):
    """
    Récupère l'axe géographique associé au client d'un contrat donné.

    Args:
        pool: Le pool de connexions aiomysql.
        contrat_id (int): L'ID du contrat.

    Returns:
        str: La valeur de l'axe du client, ou None si non trouvé ou en cas d'erreur.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor: # Utilisation de DictCursor
            await cursor.execute("""
                SELECT cl.axe
                FROM Contrat c
                JOIN Client cl ON c.client_id = cl.client_id
                WHERE c.contrat_id = %s
            """, (contrat_id,))
            resultat = await cursor.fetchone()
            if resultat:
                return resultat['axe'] # Accès par clé de dictionnaire
            else:
                return None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'axe du client pour contrat (ID: {contrat_id}) : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)