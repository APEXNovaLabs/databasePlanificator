import aiomysql
import asyncio
from datetime import datetime

async def get_db_credentials():
    """Demande à l'utilisateur les identifiants de connexion à la base de données."""
    print("\nVeuillez entrer les informations de connexion à la base de données MySQL:")
    host = input("Entrez l'adresse du serveur MySQL (par défaut, localhost): ").strip()
    if not host:
        host = "localhost"

    port_str = input("Entrez le port du serveur MySQL (par défaut: 3306): ").strip()
    try:
        port = int(port_str) if port_str else 3306
    except ValueError:
        print("Port invalide, utilisation de la valeur par défaut (3306).")
        port = 3306

    user = input("Entrez le nom d'utilisateur MySQL: ").strip()
    password = input("Entrez le mot de passe MySQL: ").strip()
    database = input("Entrez le nom de la base de données MySQL (par défaut, Planificator): ").strip()
    if not database:
        database = "Planificator"
    return host, port, user, password, database

async def ajouter_facture_remarque(pool, remarque_id: int):
    """
    Crée une facture automatique pour une remarque si le traitement associé est "Effectué"
    et si la remarque n'est pas déjà liée à une facture "Payée".
    Permet à l'utilisateur de spécifier le montant, le mode de paiement et les détails associés.
    """
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                print(f"Tentative de création de facture pour la remarque ID: {remarque_id}...")

                # 1. Récupérer les informations de la remarque et vérifier son statut et sa facture associée
                await cur.execute("""
                    SELECT
                        r.remarque_id,
                        r.planning_detail_id,
                        pd.statut AS planning_detail_statut,
                        f.etat AS facture_etat,
                        f.facture_id AS existing_facture_id
                    FROM Remarque r
                    JOIN PlanningDetails pd ON r.planning_detail_id = pd.planning_detail_id
                    LEFT JOIN Facture f ON r.facture_id = f.facture_id
                    WHERE r.remarque_id = %s
                """, (remarque_id,))
                remarque_info = await cur.fetchone()

                if not remarque_info:
                    print(f"**Erreur:** Remarque avec l'ID {remarque_id} non trouvée.")
                    return

                planning_detail_id = remarque_info['planning_detail_id']
                planning_detail_statut = remarque_info['planning_detail_statut']
                facture_etat = remarque_info['facture_etat']
                existing_facture_id = remarque_info['existing_facture_id']

                if planning_detail_statut != 'Effectué':
                    print(f"**Action requise:** Le statut du PlanningDetails ({planning_detail_statut}) pour la remarque {remarque_id} n'est pas 'Effectué'. La facture ne peut pas être créée.")
                    return

                if existing_facture_id and facture_etat == 'Payé':
                    print(f"**Information:** La remarque {remarque_id} est déjà associée à une facture (ID: {existing_facture_id}) qui est 'Payé'. Aucune nouvelle facture ne sera créée.")
                    return
                elif existing_facture_id and facture_etat != 'Payé':
                    print(f"**Information:** La remarque {remarque_id} est déjà associée à une facture (ID: {existing_facture_id}) qui est '{facture_etat}'. Vous pouvez choisir de créer une nouvelle facture ou de laisser l'ancienne en l'état.")
                    # Pour cet exemple, nous allons toujours créer une nouvelle facture si l'ancienne n'est pas payée.
                    # Une logique plus complexe pourrait demander à l'utilisateur de mettre à jour l'ancienne.

                # 2. Récupérer les informations nécessaires pour la facture (axe, date_planification)
                await cur.execute("""
                    SELECT
                        c.axe,
                        pd.date_planification
                    FROM Contrat c
                    JOIN Traitement t ON c.contrat_id = t.contrat_id
                    JOIN Planning p ON t.traitement_id = p.traitement_id
                    JOIN PlanningDetails pd ON p.planning_id = pd.planning_id
                    WHERE pd.planning_detail_id = %s
                """, (planning_detail_id,))
                facture_details_from_planning = await cur.fetchone()

                if not facture_details_from_planning:
                    print(f"**Erreur:** Informations de contrat/planning non trouvées pour planning_detail_id {planning_detail_id}. Impossible de créer la facture.")
                    return

                axe = facture_details_from_planning['axe']
                date_traitement = facture_details_from_planning['date_planification'] # C'est la date de planification, utilisée comme date de traitement/facturation

                # 3. Demander le montant de la facture
                montant = None
                while montant is None:
                    try:
                        montant_input = input("Entrez le montant de la facture (ex: 150000): ").strip()
                        montant = float(montant_input)
                        if montant <= 0:
                            print("Le montant doit être un nombre positif.")
                            montant = None
                    except ValueError:
                        print("Montant invalide. Veuillez entrer un nombre.")

                # 4. Demander le mode de paiement et les détails associés
                mode_paiement = None
                etablissement_payeur = None
                numero_cheque = None
                date_paiement = None
                etat_facture = 'À venir' # Default state

                print("\nChoisissez le mode de paiement:")
                print("1. Espèce")
                print("2. Virement")
                print("3. Chèque")
                print("4. Mobile Money")
                print("5. Non payé / À venir (par défaut)")
                mode_choice = input("Entrez votre choix (1-5): ").strip()

                if mode_choice == '1':
                    mode_paiement = 'Espèce'
                    etat_facture = 'Payé'
                elif mode_choice == '2':
                    mode_paiement = 'Virement'
                    etat_facture = 'Payé'
                elif mode_choice == '3':
                    mode_paiement = 'Chèque'
                    etablissement_payeur = input("Entrez l'établissement payeur (ex: BNI, BOA): ").strip()
                    numero_cheque = input("Entrez le numéro du chèque: ").strip()
                    etat_facture = 'Payé'
                elif mode_choice == '4':
                    mode_paiement = 'Mobile Money'
                    etat_facture = 'Payé'
                else: # Default to 'Non payé' or 'À venir'
                    mode_paiement = None # Explicitly set to None for 'Non payé' enum
                    etat_facture = 'Non payé' # Or 'À venir' depending on your exact ENUM definition for non-paid

                if etat_facture == 'Payé':
                    while True:
                        date_paiement_str = input("Entrez la date de paiement (AAAA-MM-JJ, laissez vide pour la date de traitement): ").strip()
                        if not date_paiement_str:
                            date_paiement = date_traitement # Use planning date as payment date if not provided
                            break
                        try:
                            date_paiement = datetime.strptime(date_paiement_str, '%Y-%m-%d').date()
                            break
                        except ValueError:
                            print("Format de date invalide. Veuillez utiliser AAAA-MM-JJ.")
                else:
                    date_paiement = None # No payment date if not paid

                # 5. Ajouter la nouvelle facture dans la base de données
                await cur.execute("""
                    INSERT INTO Facture (planning_detail_id, reference_facture, montant, mode, etablissemnt_payeur, numero_cheque, date_paiement, date_traitement, etat, axe)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    planning_detail_id,
                    f"F-REM-{remarque_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}", # Générer une référence unique
                    montant,
                    mode_paiement,
                    etablissement_payeur if etablissement_payeur else None,
                    numero_cheque if numero_cheque else None,
                    date_paiement,
                    date_traitement,
                    etat_facture,
                    axe
                ))

                new_facture_id = cur.lastrowid
                if not new_facture_id:
                    print("**Erreur:** Impossible d'obtenir l'ID de la nouvelle facture après insertion.")
                    return

                print(f"Facture ID {new_facture_id} ajoutée avec succès pour PlanningDetails ID {planning_detail_id}.")

                # 6. Mettre à jour la remarque avec le nouveau facture_id
                await cur.execute("""
                    UPDATE Remarque SET facture_id = %s WHERE remarque_id = %s
                """, (new_facture_id, remarque_id))
                print(f"Remarque ID {remarque_id} mise à jour avec facture_id {new_facture_id}.")

                print("Opération terminée.")

    except Exception as e:
        print(f"**Une erreur est survenue lors de l'ajout de la facture/remarque :** {e}")

async def creer_remarque(pool, planning_detail_id: int, contenu: str, issue: str = None, action: str = None):
    """
    Crée une nouvelle remarque pour un PlanningDetail donné.
    Retourne l'ID de la remarque nouvellement créée.
    """
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # Get client_id from planning_detail_id
                await cur.execute("""
                    SELECT cl.client_id
                    FROM PlanningDetails pd
                    JOIN Planning p ON pd.planning_id = p.planning_id
                    JOIN Traitement tr ON p.traitement_id = tr.traitement_id
                    JOIN Contrat co ON tr.contrat_id = co.contrat_id
                    JOIN Client cl ON co.client_id = cl.client_id
                    WHERE pd.planning_detail_id = %s
                """, (planning_detail_id,))
                client_info = await cur.fetchone()

                if not client_info:
                    print(f"**Erreur:** Impossible de trouver le client_id pour planning_detail_id {planning_detail_id}.")
                    return None

                client_id = client_info['client_id']

                await cur.execute("""
                    INSERT INTO Remarque (planning_detail_id, client_id, contenu, issue, action)
                    VALUES (%s, %s, %s, %s, %s)
                """, (planning_detail_id, client_id, contenu, issue, action))
                new_remarque_id = cur.lastrowid
                print(f"Remarque créée avec l'ID: {new_remarque_id} pour PlanningDetail ID: {planning_detail_id}.")
                return new_remarque_id
    except Exception as e:
        print(f"**Erreur lors de la création de la remarque :** {e}")
        return None

async def get_effectue_planning_details(pool):
    """
    Récupère et affiche les détails de planification dont le statut est 'Effectué'.
    Indique si une remarque est déjà associée à cette planification.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT
                        pd.planning_detail_id,
                        pd.date_planification,
                        tt.typeTraitement,
                        CONCAT(cl.nom, ' ', COALESCE(cl.prenom, '')) AS client_nom_complet,
                        co.reference_contrat,
                        r.remarque_id IS NOT NULL AS has_remark,
                        r.remarque_id,
                        r.contenu AS existing_remarque_contenu
                    FROM PlanningDetails pd
                    JOIN Planning p ON pd.planning_id = p.planning_id
                    JOIN Traitement tr ON p.traitement_id = tr.traitement_id
                    JOIN TypeTraitement tt ON tr.id_type_traitement = tt.id_type_traitement
                    JOIN Contrat co ON tr.contrat_id = co.contrat_id
                    JOIN Client cl ON co.client_id = cl.client_id
                    LEFT JOIN Remarque r ON pd.planning_detail_id = r.planning_detail_id
                    WHERE pd.statut = 'Effectué'
                    ORDER BY pd.date_planification DESC;
                    """
            await cursor.execute(query)
            result = await cursor.fetchall()
            return result
    except Exception as e:
        print(f"**Erreur lors de la récupération des planifications effectuées :** {e}")
        return []
    finally:
        if conn:
            pool.release(conn)

async def main():
    pool = None
    try:
        host, port, user, password, database = await get_db_credentials()

        print(f"\nTentative de connexion à la base de données '{database}' sur {host}:{port} avec l'utilisateur '{user}'...")
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=True,
            minsize=1,
            maxsize=5
        )
        print("Connexion à la base de données établie avec succès.")

        while True:
            print("\n--- Menu Principal ---")
            print("1. Gérer les remarques et factures pour les planifications effectuées")
            print("2. Quitter")

            main_choice = input("Entrez votre choix (1-2) : ").strip()

            if main_choice == '1':
                print("\n--- Planifications 'Effectué' disponibles ---")
                planning_details = await get_effectue_planning_details(pool)

                if not planning_details:
                    print("Aucune planification 'Effectué' trouvée pour le moment.")
                    continue

                print(f"{'ID':<5} | {'Date Planif.':<15} | {'Type Traitement':<25} | {'Client':<30} | {'Contrat':<15} | {'Remarque Existante':<20}")
                print("-" * 115)
                for i, pd_info in enumerate(planning_details):
                    remark_status = "Oui" if pd_info['has_remark'] else "Non"
                    print(f"{pd_info['planning_detail_id']:<5} | {pd_info['date_planification'].strftime('%Y-%m-%d'):<15} | {pd_info['typeTraitement']:<25} | {pd_info['client_nom_complet']:<30} | {pd_info['reference_contrat']:<15} | {remark_status:<20}")

                selected_pd_id = input("\nEntrez l'ID de la planification pour laquelle vous souhaitez ajouter/gérer une remarque (laissez vide pour annuler) : ").strip()
                if not selected_pd_id:
                    continue

                try:
                    selected_pd_id = int(selected_pd_id)
                except ValueError:
                    print("**Erreur :** L'ID de la planification doit être un nombre entier.")
                    continue

                selected_planning = next((pd for pd in planning_details if pd['planning_detail_id'] == selected_pd_id), None)

                if not selected_planning:
                    print(f"**Erreur :** Planification avec l'ID {selected_pd_id} non trouvée dans la liste.")
                    continue

                remarque_id_to_use = selected_planning['remarque_id']

                if selected_planning['has_remark']:
                    print(f"\nUne remarque existe déjà pour cette planification (ID: {selected_planning['remarque_id']}).")
                    print(f"Contenu de la remarque existante : {selected_planning['existing_remarque_contenu']}")
                    action_choice = input("Voulez-vous créer une facture pour cette remarque existante ? (oui/non) : ").strip().lower()
                    if action_choice == 'oui':
                        await ajouter_facture_remarque(pool, remarque_id_to_use)
                    else:
                        print("Opération annulée.")
                else:
                    print("\nAucune remarque n'existe pour cette planification. Créons-en une nouvelle.")
                    contenu_remarque = input("Entrez le contenu de la remarque : ").strip()
                    issue_remarque = input("Entrez le problème (laissez vide si aucun) : ").strip() or None
                    action_remarque = input("Entrez l'action prise (laissez vide si aucune) : ").strip() or None

                    new_remarque_id = await creer_remarque(pool, selected_pd_id, contenu_remarque, issue_remarque, action_remarque)

                    if new_remarque_id:
                        facture_choice = input("\nVoulez-vous créer une facture pour cette nouvelle remarque ? (oui/non) : ").strip().lower()
                        if facture_choice == 'oui':
                            await ajouter_facture_remarque(pool, new_remarque_id)
                        else:
                            print("Facture non créée pour cette remarque.")
                    else:
                        print("Impossible de créer la remarque. Opération annulée.")

            elif main_choice == '2':
                print("Quitter le programme.")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

            continuer_main = input("\nVoulez-vous retourner au menu principal ? (oui/non) : ").strip().lower()
            if continuer_main != 'oui':
                break

    except Exception as e:
        print(f"**Une erreur inattendue est survenue dans le script principal :** {e}")
    finally:
        if pool:
            print("\nFermeture du pool de connexions à la base de données...")
            pool.close()
            await pool.wait_closed()
            print("Pool de connexions fermé.")

if __name__ == "__main__":
    asyncio.run(main())
