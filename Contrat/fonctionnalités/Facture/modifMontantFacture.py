import datetime
import asyncio
import aiomysql
from Contrat.fonctionnalités.connexionDB import DBConnection


# --- Fonctions utilitaires (réutilisées de vos scripts précédents) ---

async def obtenirTousClients(pool):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT client_id, CONCAT(nom, ' ', prenom) AS full_name
                    FROM Client
                    ORDER BY full_name;
                    """
            await cursor.execute(query)
            result = await cursor.fetchall()
            return result
    except Exception as e:
        print(f"Erreur lors de la récupération de la liste des clients : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)

async def obtenirIDCLientsParNom(pool, client_name: str):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT client_id
                    FROM Client
                    WHERE CONCAT(nom, ' ', prenom) = %s
                    LIMIT 1;
                    """
            await cursor.execute(query, (client_name,))
            result = await cursor.fetchone()
            return result['client_id'] if result else None
    except Exception as e:
        print(f"Erreur lors de la recherche du client par nom : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)

# --- Nouvelles fonctions spécifiques à la modification de facture ---

async def obtentionRésuméFactureClient(pool, client_id: int):
    """Récupère un résumé des factures pour un client donné."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT f.facture_id,
                           f.date_traitement,
                           f.montant,
                           f.etat AS `Etat paiement`,
                           tt.typeTraitement AS `Type de Traitement`
                    FROM Facture f
                    JOIN PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id
                    JOIN Planning p ON pd.planning_id = p.planning_id
                    JOIN Traitement tr ON p.traitement_id = tr.traitement_id
                    JOIN TypeTraitement tt ON tr.id_type_traitement = tt.id_type_traitement
                    JOIN Contrat co ON tr.contrat_id = co.contrat_id
                    WHERE co.client_id = %s
                    ORDER BY f.date_traitement DESC;
                    """
            await cursor.execute(query, (client_id,))
            return await cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des factures du client : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)

async def obtentionRésuméMontantActuel(pool, facture_id: int):
    """Récupère le montant actuel d'une facture."""
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = "SELECT montant FROM Facture WHERE facture_id = %s;"
            await cursor.execute(query, (facture_id,))
            result = await cursor.fetchone()
            return result['montant'] if result else None
    except Exception as e:
        print(f"Erreur lors de la récupération du montant actuel de la facture {facture_id}: {e}")
        return None
    finally:
        if conn:
            pool.release(conn)

async def majMontantEtHistorique(pool, facture_id: int, old_amount: float, new_amount: float, changed_by: str = 'System'):
    """
    Met à jour le montant d'une facture et enregistre l'ancien/nouveau montant
    dans la table d'historique.
    """
    conn = None
    try:
        conn = await pool.acquire()
        # Assurez-vous que les opérations sont atomiques (tout ou rien)
        async with conn.cursor() as cursor:
            # 1. Mettre à jour le montant dans la table Facture
            update_query = "UPDATE Facture SET montant = %s WHERE facture_id = %s;"
            await cursor.execute(update_query, (new_amount, facture_id))

            # 2. Insérer l'entrée d'historique
            insert_history_query = """
                                   INSERT INTO Historique_prix
                                   (facture_id, old_amount, new_amount, change_date, changed_by)
                                   VALUES (%s, %s, %s, %s, %s);
                                   """
            await cursor.execute(insert_history_query,
                                 (facture_id, old_amount, new_amount, datetime.datetime.now(), changed_by))

            await conn.commit() # Valider la transaction si autocommit n'est pas activé ou pour plus de clarté
            print(f"Montant de la facture {facture_id} mis à jour de {old_amount} à {new_amount}.")
            print("Historique de la modification enregistré.")
            return True
    except Exception as e:
        if conn:
            await conn.rollback() # Annuler la transaction en cas d'erreur
        print(f"Erreur lors de la modification de la facture et de l'enregistrement de l'historique : {e}")
        return False
    finally:
        if conn:
            pool.release(conn)

# --- Fonction principale ---
async def mainModificationMontant():
    pool = None
    try:
        pool = await DBConnection()
        if not pool:
            print("Échec de la connexion à la base de données. Impossible de modifier la facture.")
            return

        print("\n--- Modification du montant de la facture ---")

        # 1. Sélectionner le client
        clients = await obtenirTousClients(pool)
        if not clients:
            print("Aucun client trouvé dans la base de données.")
            return

        print("\nClients disponibles :")
        client_map = {}
        for i, client in enumerate(clients):
            print(f"{i + 1}. {client['full_name']}")
            client_map[str(i + 1)] = client

        idClientChoisi = None
        nomCLientChoisi = None
        while idClientChoisi is None:
            choix = input(
                "\nVeuillez entrer le numéro du client dans la liste, ou son nom complet (Nom Prénom) : ").strip()
            if choix.isdigit():
                if choix in client_map:
                    selected_client = client_map[choix]
                    idClientChoisi = selected_client['client_id']
                    nomCLientChoisi = selected_client['full_name']
                    print(f"Client sélectionné : {nomCLientChoisi}")
                else:
                    print("Numéro invalide. Veuillez réessayer.")
            else:
                nomCLientChoisi = choix
                idClientChoisi = await obtenirIDCLientsParNom(pool, nomCLientChoisi)
                if idClientChoisi is None:
                    print(f"Client '{nomCLientChoisi}' non trouvé. Veuillez vérifier le nom et réessayer.")
                else:
                    print(f"Client trouvé : {nomCLientChoisi}")

        # 2. Récupérer et afficher les factures du client
        invoices = await obtentionRésuméFactureClient(pool, idClientChoisi)
        if not invoices:
            print(f"Aucune facture trouvée pour le client '{nomCLientChoisi}'.")
            return

        print(f"\nFactures de {nomCLientChoisi} :")
        invoice_map = {}
        for i, inv in enumerate(invoices):
            print(f"{i + 1}. ID Facture: {inv['facture_id']}, Date: {inv['date_traitement'].strftime('%Y-%m-%d')}, "
                  f"Type: {inv['Type de Traitement']}, Montant Actuel: {inv['montant']:.2f} {inv['Etat paiement']}")
            invoice_map[str(i + 1)] = inv['facture_id']

        # 3. Sélectionner la facture à modifier
        selected_facture_id = None
        while selected_facture_id is None:
            invoice_choice = input("\nVeuillez entrer le numéro de la facture à modifier : ").strip()
            if invoice_choice.isdigit() and invoice_choice in invoice_map:
                selected_facture_id = invoice_map[invoice_choice]
            else:
                print("Numéro de facture invalide. Veuillez réessayer.")

        # 4. Récupérer le montant actuel de la facture sélectionnée
        old_amount = await obtentionRésuméMontantActuel(pool, selected_facture_id)
        if old_amount is None:
            print(f"Impossible de récupérer le montant actuel pour la facture ID {selected_facture_id}.")
            return

        print(f"\nMontant actuel de la facture ID {selected_facture_id}: {old_amount:.2f}")

        # 5. Demander le nouveau montant
        new_amount = None
        while new_amount is None:
            try:
                new_amount_input = input(f"Entrez le nouveau montant pour la facture ID {selected_facture_id} : ").strip()
                new_amount = float(new_amount_input)
                if new_amount < 0:
                    print("Le montant ne peut pas être négatif.")
                    new_amount = None # Reset to re-enter loop
            except ValueError:
                print("Montant invalide. Veuillez entrer un nombre.")

        if new_amount == old_amount:
            print("Le nouveau montant est identique à l'ancien. Aucune modification nécessaire.")
            return

        # 6. Confirmation
        confirm = input(
            f"Confirmez-vous la modification du montant de la facture {selected_facture_id} de {old_amount:.2f} à {new_amount:.2f} ? (oui/non) : ").lower().strip()

        if confirm == 'oui':
            success = await majMontantEtHistorique(pool, selected_facture_id, old_amount, new_amount)
            if success:
                print("Modification effectuée avec succès.")
            else:
                print("La modification a échoué.")
        else:
            print("Modification annulée.")

    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
    finally:
        if pool:
            await pool.close()

if __name__ == "__main__":
    asyncio.run(mainModificationMontant())