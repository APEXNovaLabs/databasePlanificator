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
            print("\n--- Ajout d'une facture automatique pour une remarque ---")
            remarque_id_input = input("Entrez l'ID de la remarque (laissez vide pour quitter) : ").strip()
            if not remarque_id_input:
                break

            try:
                remarque_id = int(remarque_id_input)
            except ValueError:
                print("**Erreur :** L'ID de la remarque doit être un nombre entier.")
                continue

            await ajouter_facture_remarque(pool, remarque_id)

            continuer = input("\nVoulez-vous traiter une autre remarque ? (oui/non) : ").strip().lower()
            if continuer != 'oui':
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
