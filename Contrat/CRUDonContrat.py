# Dans Contrat/CRUDonContrat.py
import aiomysql
import asyncio
from datetime import datetime

async def create_contrat(pool, client_id, date_contrat, date_debut, date_fin_contrat, duree, categorie, duree_contrat=None):
    """
    Crée un nouveau contrat dans la base de données.

    Args:
        pool: Le pool de connexions aiomysql.
        client_id (int): L'ID du client associé au contrat.
        date_contrat (date): La date de signature du contrat.
        date_debut (date): La date de début du contrat.
        date_fin_contrat (date, optional): La date de fin du contrat (peut être None si durée indéterminée).
        duree (str): La durée du contrat (e.g., 'Déterminée', 'Indéterminée').
        categorie (str): La catégorie du contrat.
        duree_contrat (str, optional): Détail de la durée du contrat (e.g., '1 an', '3 mois').

    Returns:
        int: L'ID du contrat nouvellement créé, ou None en cas d'échec.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute("""
                INSERT INTO Contrat (client_id, date_contrat, date_debut, date_fin, duree, categorie, duree_contrat)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (client_id, date_contrat, date_debut, date_fin_contrat, duree, categorie, duree_contrat))
            await conn.commit()
            return cur.lastrowid
    except Exception as e:
        print(f"Erreur lors de la création du contrat : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)

async def read_contrat(pool, contrat_id):
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
            # Il est souvent utile de récupérer aussi les infos client associées
            await cur.execute("""
                SELECT
                    c.contrat_id,
                    c.client_id,
                    cl.nom AS nom_client,
                    cl.prenom AS prenom_client,
                    cl.email AS email_client,
                    c.date_contrat,
                    c.date_debut,
                    c.date_fin,
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

async def update_contrat(pool, contrat_id, client_id, date_contrat, date_debut, date_fin_contrat, duree, categorie, duree_contrat=None):
    """
    Modifie un contrat existant dans la base de données.

    Args:
        pool: Le pool de connexions aiomysql.
        contrat_id (int): L'ID du contrat à modifier.
        client_id (int): Le nouvel ID du client (peut être le même).
        date_contrat (date): La nouvelle date de signature.
        date_debut (date): La nouvelle date de début.
        date_fin_contrat (date, optional): La nouvelle date de fin (peut être None).
        duree (str): La nouvelle durée.
        categorie (str): La nouvelle catégorie.
        duree_contrat (str, optional): Le nouveau détail de la durée.

    Returns:
        int: Le nombre de lignes affectées (1 en cas de succès, 0 sinon ou en cas d'erreur).
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute("""
                UPDATE Contrat SET client_id = %s, date_contrat = %s, date_debut = %s, date_fin = %s,
                duree = %s, categorie = %s, duree_contrat = %s
                WHERE contrat_id = %s
            """, (client_id, date_contrat, date_debut, date_fin_contrat, duree, categorie, duree_contrat, contrat_id))
            await conn.commit()
            return cur.rowcount # Retourne 1 si mise à jour, 0 si contrat non trouvé
    except Exception as e:
        print(f"Erreur lors de la modification du contrat (ID: {contrat_id}) : {e}")
        return 0
    finally:
        if conn:
            pool.release(conn)

async def delete_contrat(pool, contrat_id):
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

async def obtenir_duree_contrat(pool, contrat_id):
    """
    Récupère la durée principale du contrat (ex: 'Déterminée', 'Indéterminée').

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

async def obtenir_axe_contrat(pool, contrat_id):
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
        print(f"Erreur lors de la récupération de l'axe du contrat (ID: {contrat_id}) : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)