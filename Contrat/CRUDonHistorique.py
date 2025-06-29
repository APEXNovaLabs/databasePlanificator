import asyncio
import aiomysql
from datetime import date, datetime, timedelta


async def create_historique(pool, traitement_id, contenu, date_traitement=None):
    """Crée un historique pour un traitement donné."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            if date_traitement is None:
                date_traitement = date.today()
            await cur.execute(
                "INSERT INTO Historique (traitement_id, contenu, date_traitement) VALUES (%s, %s, %s)",
                (traitement_id, contenu, date_traitement)
            )
            await conn.commit()
            return cur.lastrowid
    except Exception as e:
        print(f"Erreur lors de la création de l'historique : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)


async def read_historique(pool, historique_id):
    """Lit un historique à partir de son ID."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur:  # Utilisation de DictCursor
            await cur.execute("SELECT * FROM Historique WHERE historique_id = %s", (historique_id,))
            return await cur.fetchone()  # Retourne un dictionnaire ou None
    except Exception as e:
        print(f"Erreur lors de la lecture de l'historique (ID: {historique_id}) : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)


async def update_historique(pool, historique_id, contenu, date_traitement):
    """Modifie un historique existant."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE Historique SET contenu = %s, date_traitement = %s WHERE historique_id = %s",
                (contenu, date_traitement, historique_id)
            )
            await conn.commit()
            return cur.rowcount  # Retourne le nombre de lignes affectées (1 si succès, 0 sinon)
    except Exception as e:
        print(f"Erreur lors de la modification de l'historique (ID: {historique_id}) : {e}")
        return 0
    finally:
        if conn:
            pool.release(conn)


async def delete_historique(pool, historique_id):
    """Supprime un historique à partir de son ID."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Historique WHERE historique_id = %s", (historique_id,))
            await conn.commit()
            return cur.rowcount  # Retourne le nombre de lignes supprimées
    except Exception as e:
        print(f"Erreur lors de la suppression de l'historique (ID: {historique_id}) : {e}")
        return 0
    finally:
        if conn:
            pool.release(conn)


async def get_historique_for_traitement(pool, traitement_id):
    """Récupère l'historique d'un traitement spécifique."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur:  # Utilisation de DictCursor
            await cur.execute("SELECT * FROM Historique WHERE traitement_id = %s ORDER BY date_traitement DESC",
                              (traitement_id,))
            return await cur.fetchall()  # Retourne une liste de dictionnaires
    except Exception as e:
        print(f"Erreur lors de la récupération de l'historique pour le traitement ID {traitement_id} : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)


async def create_historique_for_planning(pool, planning_id, contenu_specifique=None):
    """
    Crée automatiquement un historique pour le traitement associé à un planning donné.
    Le contenu peut être spécifié ou généré par défaut.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur:  # Utilisation de DictCursor
            # Récupérer l'ID du traitement associé à ce planning
            await cur.execute("SELECT traitement_id FROM Planning WHERE planning_id = %s", (planning_id,))
            result = await cur.fetchone()
            if result:
                traitement_id = result['traitement_id']

                # Définir le contenu par défaut si non spécifié
                if contenu_specifique is None:
                    contenu = f"Historique généré automatiquement pour la planification du traitement {traitement_id}."
                else:
                    contenu = contenu_specifique

                await create_historique(pool, traitement_id, contenu)
                print(f"Historique créé pour le traitement {traitement_id} lié au planning {planning_id}.")
                return True
            else:
                print(f"Aucun traitement trouvé pour le planning ID {planning_id}.")
                return False
    except Exception as e:
        print(f"Erreur lors de la création automatique de l'historique pour le planning {planning_id} : {e}")
        return False
    finally:
        if conn:
            pool.release(conn)


async def afficher_historique_client(pool, client_id):
    """Affiche l'historique de tous les traitements d'un client."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur:  # Utilisation de DictCursor
            await cur.execute("""
                              SELECT h.historique_id,
                                     h.traitement_id,
                                     h.contenu,
                                     h.date_traitement,
                                     t.id_type_traitement,                     -- ID du type de traitement pour plus de détails
                                     tt.typeTraitement AS nom_type_traitement, -- Nom du type de traitement
                                     c.contrat_id,
                                     cl.nom            AS nom_client,
                                     cl.prenom         AS prenom_client
                              FROM Historique h
                                       JOIN Traitement t ON h.traitement_id = t.traitement_id
                                       JOIN Contrat c ON t.contrat_id = c.contrat_id
                                       JOIN Client cl ON c.client_id = cl.client_id
                                       JOIN TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement -- Jointure pour le nom du type de traitement
                              WHERE c.client_id = %s
                              ORDER BY h.date_traitement DESC
                              """, (client_id,))
            historiques = await cur.fetchall()

            if not historiques:
                print(f"Aucun historique trouvé pour le client ID {client_id}.")
                return

            print(
                f"\n--- Historique des traitements pour le client ID {client_id} ({historiques[0]['nom_client']} {historiques[0]['prenom_client']}) ---")
            for historique in historiques:
                print("-" * 30)
                print(f"ID Historique: {historique['historique_id']}")
                print(f"ID Traitement: {historique['traitement_id']} (Type: {historique['nom_type_traitement']})")
                print(f"Contenu: {historique['contenu']}")
                print(f"Date Traitement: {historique['date_traitement']}")
                print(f"ID Contrat: {historique['contrat_id']}")
            print("-" * 30)

    except Exception as e:
        print(f"Erreur lors de l'affichage de l'historique du client ID {client_id} : {e}")
    finally:
        if conn:
            pool.release(conn)