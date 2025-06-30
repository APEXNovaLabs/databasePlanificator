import aiomysql
from datetime import date, datetime

from rapportExelFacture import generationFactureClient

async def obtenir_etats_facture(pool):
    """Récupère les valeurs ENUM pour la colonne 'etat' de la table Facture."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                SELECT COLUMN_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Facture' AND COLUMN_NAME = 'etat'
            """
            await cursor.execute(query)
            result = await cursor.fetchone()
            if result and 'COLUMN_TYPE' in result and result['COLUMN_TYPE'].startswith("enum("):
                enum_str = result['COLUMN_TYPE']
                return [val.strip("'") for val in enum_str[len("enum("):-1].split(',')]
            return []
    except Exception as e:
        print(f"Erreur lors de la récupération des états de facture : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)

async def obtenir_axes(pool):
    """Récupère les valeurs ENUM pour la colonne 'axe' de la table Facture."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                SELECT COLUMN_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Facture' AND COLUMN_NAME = 'axe'
            """
            await cursor.execute(query)
            result = await cursor.fetchone()
            if result and 'COLUMN_TYPE' in result and result['COLUMN_TYPE'].startswith("enum("):
                enum_str = result['COLUMN_TYPE']
                return [val.strip("'") for val in enum_str[len("enum("):-1].split(',')]
            return []
    except Exception as e:
        print(f"Erreur lors de la récupération des axes : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)


# --- Vos fonctions CRUD pour Facture (inchangées) ---
async def create_facture(pool, planning_detail_id, montant, date_traitement, etat='Non payé', axe=None):
    """
    Crée une nouvelle facture dans la base de données.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            if axe is None:
                raise ValueError("L'axe ne peut pas être NULL pour la création d'une facture.")

            await cur.execute("""
                INSERT INTO Facture (planning_detail_id, montant, date_traitement, etat, axe)
                VALUES (%s, %s, %s, %s, %s)
            """, (planning_detail_id, montant, date_traitement, etat, axe))
            await conn.commit()
            facture_id = cur.lastrowid

            print(f"Facture {facture_id} créée avec succès pour PlanningDetail ID {planning_detail_id}.")
            return facture_id
    except Exception as e:
        print(f"Erreur lors de la création de la facture : {e}")
        if conn:
            await conn.rollback()
        return None
    finally:
        if conn:
            pool.release(conn)

async def get_facture_details(pool, facture_id):
    """
    Récupère les détails complets d'une facture, y compris les informations de traitement et l'historique des prix.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("""
                SELECT
                    f.facture_id,
                    f.planning_detail_id,
                    f.montant,
                    f.date_traitement,
                    f.etat,
                    f.axe,
                    pd.date_planification,
                    p.traitement_id,
                    tt.typeTraitement AS nom_type_traitement,
                    cl.client_id,
                    cl.nom AS nom_client,
                    cl.prenom AS prenom_client
                FROM Facture f
                JOIN PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id
                JOIN Planning p ON pd.planning_id = p.planning_id
                JOIN Traitement t ON p.traitement_id = t.traitement_id
                JOIN TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement
                JOIN Contrat co ON t.contrat_id = co.contrat_id
                JOIN Client cl ON co.client_id = cl.client_id
                WHERE f.facture_id = %s
            """, (facture_id,))
            facture_details = await cur.fetchone()

            if not facture_details:
                return None

            await cur.execute("""
                SELECT history_id, old_amount, new_amount, change_date, changed_by
                FROM Historique_prix
                WHERE facture_id = %s
                ORDER BY change_date DESC, history_id DESC
            """, (facture_id,))
            historique_prix = await cur.fetchall()

            facture_details['historique_prix'] = historique_prix
            return facture_details
    except Exception as e:
        print(f"Erreur lors de la récupération des détails de la facture {facture_id} : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)

async def update_facture_montant_and_status(pool, facture_id, nouveau_montant=None, nouvel_etat=None, changed_by='System'):
    """
    Met à jour le montant ou l'état d'une facture.
    Si le montant est modifié, un enregistrement est ajouté à Historique_prix.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT montant, etat FROM Facture WHERE facture_id = %s", (facture_id,))
            facture_actuelle = await cur.fetchone()

            if not facture_actuelle:
                print(f"Facture avec l'ID {facture_id} non trouvée.")
                return False

            old_montant = facture_actuelle['montant']
            current_etat = facture_actuelle['etat']

            updates = []
            params = []

            if nouveau_montant is not None and nouveau_montant != old_montant:
                updates.append("montant = %s")
                params.append(nouveau_montant)

                await cur.execute("""
                    INSERT INTO Historique_prix (facture_id, old_amount, new_amount, change_date, changed_by)
                    VALUES (%s, %s, %s, %s, %s)
                """, (facture_id, old_montant, nouveau_montant, datetime.now(), changed_by))
                print(f"Historique de prix enregistré pour la facture {facture_id}: {old_montant} -> {nouveau_montant}.")

            if nouvel_etat is not None and nouvel_etat != current_etat:
                updates.append("etat = %s")
                params.append(nouvel_etat)

            if not updates:
                print("Aucune modification à appliquer (montant et état sont identiques ou non spécifiés).")
                return False

            query_update = f"UPDATE Facture SET {', '.join(updates)} WHERE facture_id = %s"
            params.append(facture_id)

            await cur.execute(query_update, tuple(params))
            await conn.commit()
            print(f"Facture {facture_id} mise à jour avec succès.")
            return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la facture {facture_id} : {e}")
        if conn:
            await conn.rollback()
        return False
    finally:
        if conn:
            pool.release(conn)

async def delete_facture(pool, facture_id):
    """
    Supprime une facture de la base de données.
    Note: Cela déclenchera ON DELETE CASCADE sur Historique_prix et FactureTraitement.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Facture WHERE facture_id = %s", (facture_id,))
            await conn.commit()
            print(f"Facture {facture_id} supprimée avec succès.")
            return cur.rowcount
    except Exception as e:
        print(f"Erreur lors de la suppression de la facture {facture_id} : {e}")
        return 0
    finally:
        if conn:
            pool.release(conn)

async def get_all_factures_for_client(pool, client_id):
    """
    Récupère toutes les factures émises pour un client spécifique.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("""
                SELECT
                    f.facture_id,
                    f.montant,
                    f.date_traitement,
                    f.etat,
                    f.axe,
                    cl.nom AS nom_client,
                    cl.prenom AS prenom_client,
                    tt.typeTraitement AS nom_type_traitement,
                    pd.date_planification
                FROM Facture f
                JOIN PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id
                JOIN Planning p ON pd.planning_id = p.planning_id
                JOIN Traitement tr ON p.traitement_id = tr.traitement_id
                JOIN TypeTraitement tt ON tr.id_type_traitement = tt.id_type_traitement
                JOIN Contrat co ON tr.contrat_id = co.contrat_id
                JOIN Client cl ON co.client_id = cl.client_id
                WHERE cl.client_id = %s
                ORDER BY f.date_traitement DESC
            """, (client_id,))
            return await cur.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des factures pour le client {client_id} : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)
