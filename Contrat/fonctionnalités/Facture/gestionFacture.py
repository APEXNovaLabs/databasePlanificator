import aiomysql
from datetime import date

# Assurez-vous d'importer votre script d'exportation Excel ici
# Par exemple, si votre script s'appelle 'export_excel.py'
# from export_excel import generate_invoice_excel

# Fonction factice pour simuler l'exportation Excel (gardée comme avant, à remplacer)
async def generate_invoice_excel_mock(facture_details, output_path="facture.xlsx"):
    """
    Simule la génération d'un fichier Excel.
    Remplacez cette fonction par l'importation et l'appel de votre fonction réelle.
    """
    print(f"\n--- Génération de la facture Excel ---")
    print(f"Détails de la facture à exporter : {facture_details.get('facture_id')}")
    print(f"Chemin de sortie : {output_path}")
    print("Fichier Excel généré (simulation).")
    return True

async def create_facture(pool, client_id, date_facture, montant_total, traitements_ids):
    """
    Crée une nouvelle facture et l'associe à un ou plusieurs traitements.
    Les montants initiaux (payé, restant) sont gérés ici.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cur:
            # Insérer la facture principale
            # Les montants sont traités comme des entiers
            await cur.execute("""
                INSERT INTO Facture (client_id, date_facture, montant_total, montant_paye, montant_restant)
                VALUES (%s, %s, %s, %s, %s)
            """, (client_id, date_facture, montant_total, 0, montant_total)) # 0 au lieu de Decimal('0.00')
            await conn.commit()
            facture_id = cur.lastrowid

            if not facture_id:
                raise Exception("Erreur: Impossible de récupérer l'ID de la facture créée.")

            # Associer les traitements à la facture
            if traitements_ids:
                for traitement_id in traitements_ids:
                    await cur.execute(
                        "INSERT INTO FactureTraitement (facture_id, traitement_id) VALUES (%s, %s)",
                        (facture_id, traitement_id)
                    )
                await conn.commit()

            print(f"Facture {facture_id} créée avec succès pour le client {client_id}.")
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
    Récupère les détails complets d'une facture, y compris les traitements associés.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # Détails de la facture
            await cur.execute("SELECT * FROM Facture WHERE facture_id = %s", (facture_id,))
            facture_details = await cur.fetchone()

            if not facture_details:
                return None

            # Traitements associés à la facture
            await cur.execute("""
                SELECT
                    ft.traitement_id,
                    tt.typeTraitement AS nom_type_traitement,
                    t.contrat_id
                FROM FactureTraitement ft
                JOIN Traitement t ON ft.traitement_id = t.traitement_id
                JOIN TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement
                WHERE ft.facture_id = %s
            """, (facture_id,))
            traitements_associes = await cur.fetchall()

            facture_details['traitements_associes'] = traitements_associes
            return facture_details
    except Exception as e:
        print(f"Erreur lors de la récupération des détails de la facture {facture_id} : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)

async def update_montant_facture(pool, facture_id, nouveau_montant_total=None, montant_paye_ajoute=None):
    """
    Met à jour le montant total ou ajoute un montant au 'montant_paye' d'une facture.
    Recalcule le montant restant en conséquence.
    Les montants sont traités comme des entiers.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # 1. Récupérer l'état actuel de la facture
            await cur.execute("SELECT montant_total, montant_paye, montant_restant FROM Facture WHERE facture_id = %s", (facture_id,))
            facture_actuelle = await cur.fetchone()

            if not facture_actuelle:
                print(f"Facture avec l'ID {facture_id} non trouvée.")
                return False

            current_total = facture_actuelle['montant_total']
            current_paid = facture_actuelle['montant_paye']

            # 2. Calculer les nouveaux montants
            updated_total = current_total
            updated_paid = current_paid

            if nouveau_montant_total is not None:
                updated_total = nouveau_montant_total
                updated_remaining = updated_total - updated_paid
            elif montant_paye_ajoute is not None:
                updated_paid += montant_paye_ajoute
                updated_remaining = updated_total - updated_paid
            else:
                print("Aucun montant à modifier ou à ajouter spécifié.")
                return False

            # Empêcher le montant restant d'être négatif
            # Utiliser max(0, ...) pour les entiers
            updated_remaining = max(0, updated_remaining)

            # 3. Mettre à jour la base de données
            await cur.execute("""
                UPDATE Facture
                SET montant_total = %s, montant_paye = %s, montant_restant = %s
                WHERE facture_id = %s
            """, (updated_total, updated_paid, updated_remaining, facture_id))
            await conn.commit()
            print(f"Facture {facture_id} mise à jour. Total: {updated_total}, Payé: {updated_paid}, Restant: {updated_remaining}")
            return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour des montants de la facture {facture_id} : {e}")
        if conn:
            await conn.rollback()
        return False
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
                    f.date_facture,
                    f.montant_total,
                    f.montant_paye,
                    f.montant_restant,
                    cl.nom AS nom_client,
                    cl.prenom AS prenom_client
                FROM Facture f
                JOIN Client cl ON f.client_id = cl.client_id
                WHERE f.client_id = %s
                ORDER BY f.date_facture DESC
            """, (client_id,))
            return await cur.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des factures pour le client {client_id} : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)