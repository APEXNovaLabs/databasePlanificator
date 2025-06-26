import asyncio
import aiomysql
from datetime import datetime, timedelta
# Import the relativedelta for robust month/year arithmetic
from dateutil.relativedelta import relativedelta

async def get_db_credentials():
    """
    Demande à l'utilisateur les informations de connexion à la base de données.
    """
    host = input("Entrez l'adresse du serveur MySQL (par exemple, localhost): ").strip()
    if not host: # Default to localhost if empty
        host = "localhost"

    port_str = input("Entrez le port du serveur MySQL (par défaut: 3306): ").strip()
    try:
        port = int(port_str) if port_str else 3306
    except ValueError:
        print("Port invalide, utilisation de la valeur par défaut (3306).")
        port = 3306
    user = input("Entrez le nom d'utilisateur MySQL: ").strip()
    password = input("Entrez le mot de passe MySQL: ").strip()
    database = input("Entrez le nom de la base de données MySQL (par exemple, Planificator): ").strip()
    if not database: # Default to Planificator if empty
        database = "Planificator"
    return host, port, user, password, database

async def get_client_id(pool): # Changed conn to pool as it's better practice for functions that acquire/release
    """
    Demande à l'utilisateur l'ID du client et vérifie son existence dans la base de données.

    Args:
        pool: Le pool de connexions aiomysql.

    Returns:
        L'ID du client si trouvé, None sinon.
    """
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            while True:
                client_id_str = input("Entrez l'ID du client dont vous souhaitez ajuster le planning: ").strip()
                try:
                    client_id = int(client_id_str)
                    # Vérifier si le client existe
                    await cur.execute("SELECT client_id FROM Client WHERE client_id = %s", (client_id,))
                    if await cur.fetchone():
                        return client_id
                    else:
                        print("Client non trouvé. Veuillez entrer un ID de client valide.")
                except ValueError:
                    print("ID de client invalide. Veuillez entrer un nombre entier.")

async def get_client_planning(pool, client_id): # Changed conn to pool
    """
    Récupère le planning du client, les détails du planning et les traitements associés.

    Args:
        pool: Le pool de connexions aiomysql.
        client_id: L'ID du client.

    Returns:
        Un tuple contenant les informations du planning, les détails du planning et les traitements.
        Retourne None si une erreur se produit.
    """
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:

                # Récupérer le planning principal du client
                # ATTENTION: La colonne 'mois_pause' et 'unite_duree' n'existent pas dans votre DDL Planning.
                # Elles ont été retirées des colonnes SELECT.
                sql_planning = """
                    SELECT
                        p.planning_id, p.date_debut_planification, p.mois_debut, p.mois_fin,
                        p.duree_traitement, p.redondance, p.date_fin_planification
                    FROM Planning p
                    JOIN Traitement t ON p.traitement_id = t.traitement_id
                    JOIN Contrat c ON t.contrat_id = c.contrat_id  -- Correction: c.contrat_id est la PK
                    WHERE c.client_id = %s
                """
                await cur.execute(sql_planning, (client_id,))
                planning_data = await cur.fetchone()

                if not planning_data:
                    print("Aucun planning trouvé pour ce client.")
                    return None, None, None

                planning_id = planning_data['planning_id']

                # Récupérer les détails du planning
                # ATTENTION: La colonne 'mois' n'existe pas dans votre DDL PlanningDetails.
                # Elle a été retirée des colonnes SELECT.
                sql_planning_details = """
                    SELECT planning_detail_id, date_planification, statut
                    FROM PlanningDetails
                    WHERE planning_id = %s
                    ORDER BY date_planification
                """
                await cur.execute(sql_planning_details, (planning_id,))
                planning_details = await cur.fetchall()

                # Récupérer les traitements
                sql_traitements = """
                    SELECT t.traitement_id, tt.typeTraitement
                    FROM Traitement t
                    JOIN Contrat c ON t.contrat_id = c.contrat_id -- Correction: c.contrat_id est la PK
                    JOIN TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement
                    WHERE c.client_id = %s
                """
                await cur.execute(sql_traitements, (client_id,))
                traitements = await cur.fetchall()

                return planning_data, planning_details, traitements

    except aiomysql.Error as e:
        print(f"**Erreur lors de la récupération du planning du client :** {e}")
        return None, None, None

async def display_planning_info(planning_data, planning_details, traitements):
    """
    Affiche les informations du planning du client.

    Args:
        planning_data: Les données du planning principal.
        planning_details: Les détails du planning.
        traitements: Les traitements associés au client.
    """
    if not planning_data:
        print("Aucun planning à afficher.")
        return

    print("\n--- Informations sur le planning du client ---")
    print(f"  **Planning ID:** {planning_data['planning_id']}")
    print(f"  **Date de début de planification:** {planning_data['date_debut_planification']}")
    print(f"  **Mois de début:** {planning_data['mois_debut']}")
    print(f"  **Mois de fin:** {planning_data['mois_fin']}")
    # 'Mois de pause' et 'Unite_duree' retirés car non présents dans DDL
    print(f"  **Durée du traitement (en mois par défaut):** {planning_data['duree_traitement']}")
    print(f"  **Redondance (en mois par défaut):** {planning_data['redondance']}")
    print(f"  **Date de fin de planification:** {planning_data['date_fin_planification']}")

    print("\n--- Détails du planning ---")
    if not planning_details:
        print("  Aucun détail de planning trouvé.")
    else:
        for detail in planning_details:
            # 'Mois' retiré car non présent dans DDL PlanningDetails
            print(f"    **ID:** {detail['planning_detail_id']}, **Date:** {detail['date_planification']}, **Statut:** {detail['statut']}")

    print("\n--- Traitements associés ---")
    if not traitements:
        print("  Aucun traitement associé.")
    else:
        for traitement in traitements:
            print(f"    **ID:** {traitement['traitement_id']}, **Type:** {traitement['typeTraitement']}")

async def get_option_choix():
    """
    Demande à l'utilisateur de choisir comment gérer le planning.

    Returns:
        Le choix de l'utilisateur (1, 2 ou 3), ou None en cas d'erreur.
    """
    while True:
        print("\nChoisissez comment gérer le planning :")
        print("  1. Garder l'état actuel du planning (ajuster uniquement le statut d'un détail)")
        print("  2. Changer le planning (modifier les dates des traitements futurs)")
        print("  3. Annuler l'opération")
        choix = input("Entrez votre choix (1, 2 ou 3): ").strip()
        if choix in ('1', '2', '3'):
            return int(choix)
        else:
            print("Choix invalide. Veuillez entrer 1, 2 ou 3.")

async def handle_option_1(pool, planning_details): # Changed conn to pool
    """
    Gère l'option de garder l'état actuel du planning (ajuster le statut d'un détail).

    Args:
        pool: Le pool de connexions aiomysql.
        planning_details: Les détails du planning.
    """
    if not planning_details:
        print("Aucun détail de planning à modifier.")
        return

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            while True:
                detail_id_str = input("Entrez l'ID du détail du planning que vous souhaitez modifier (ou '0' pour annuler): ").strip()
                if detail_id_str == '0':
                    print("Opération annulée.")
                    return

                try:
                    detail_id = int(detail_id_str)
                    # Vérifier si detail_id existe parmi les planning_details fournis
                    detail_exists = False
                    for detail in planning_details:
                        if detail['planning_detail_id'] == detail_id:
                            detail_exists = True
                            break
                    if not detail_exists:
                        print(f"ID de détail du planning {detail_id} non trouvé dans la liste pour ce client.")
                        continue
                    break
                except ValueError:
                    print("ID de détail du planning invalide. Veuillez entrer un nombre entier ou 0.")

            # Statuts valides selon votre DDL ENUM ('Effectué', 'À venir', 'Annulé', 'Reporté')
            valid_statuses = ['Effectué', 'À venir', 'Annulé', 'Reporté']
            while True:
                nouveau_statut = input(f"Entrez le nouveau statut ({', '.join(valid_statuses)}): ").strip()
                if nouveau_statut in valid_statuses:
                    break
                else:
                    print(f"Statut invalide. Veuillez choisir parmi {', '.join(valid_statuses)}.")

            try:
                sql_update_statut = "UPDATE PlanningDetails SET statut = %s WHERE planning_detail_id = %s"
                await cur.execute(sql_update_statut, (nouveau_statut, detail_id))
                # autocommit=True sur le pool s'en charge, mais commit explicite n'est pas nuisible
                # await conn.commit()
                print(f"Statut du détail du planning ID {detail_id} mis à jour à '{nouveau_statut}'.")

            except aiomysql.Error as e:
                print(f"**Erreur lors de la mise à jour du statut :** {e}")
                # rollback() n'est pas nécessaire avec autocommit=True, mais peut être utile si autocommit est désactivé.
                # await conn.rollback()


async def handle_option_2(pool, planning_data): # Changed conn to pool
    """
    Gère l'option de changer le planning (modifier les dates des traitements futurs).
    La redondance est basée sur 'redondance' de la table Planning (assumée en mois).

    Args:
        pool: Le pool de connexions aiomysql.
        planning_data: Les données du planning principal.
    """
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            ajustement_type = input("S'agit-il d'un 'Avancement' ou d'un 'Décalage' ? ").strip()
            if ajustement_type not in ('Avancement', 'Décalage'):
                print("Type d'ajustement invalide. Veuillez entrer 'Avancement' ou 'Décalage'.")
                return

            date_str = input(f"Entrez la date du prochain traitement que vous souhaitez modifier (AAAA-MM-JJ): ").strip()
            try:
                date_a_modifier = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                print("Format de date invalide. Veuillez utiliser le format AAAA-MM-JJ.")
                return

            nouvelle_date_str = input(f"Entrez la nouvelle date pour ce traitement (AAAA-MM-JJ): ").strip()
            try:
                nouvelle_date = datetime.strptime(nouvelle_date_str, '%Y-%m-%d').date()
            except ValueError:
                print("Format de date invalide. Veuillez utiliser le format AAAA-MM-JJ.")
                return

            # Trouver tous les planning details à partir de la date spécifiée
            sql_details_to_update = """
                SELECT planning_detail_id, date_planification
                FROM PlanningDetails
                WHERE planning_id = %s AND date_planification >= %s
                ORDER BY date_planification ASC
            """
            await cur.execute(sql_details_to_update, (planning_data['planning_id'], date_a_modifier))
            details_to_update = await cur.fetchall()

            if not details_to_update:
                print(f"Aucune planification trouvée à partir du {date_a_modifier} pour ce planning.")
                return

            # Calculer le décalage pour la première date trouvée (celle que l'utilisateur veut modifier)
            first_detail_original_date = None
            first_detail_id_to_signal = None
            for detail in details_to_update:
                if detail['date_planification'] == date_a_modifier:
                    first_detail_original_date = detail['date_planification']
                    first_detail_id_to_signal = detail['planning_detail_id']
                    break

            if not first_detail_original_date:
                print(f"La date {date_a_modifier} n'est pas une date de planification future valide pour ce planning.")
                return

            delta_days = (nouvelle_date - first_detail_original_date).days
            print(f"Décalage calculé de {delta_days} jours pour la première date affectée.")

            # Mettre à jour toutes les dates futures à partir de la date spécifiée
            # On applique le même delta_days à toutes les dates suivantes.
            # On utilise un CURDATE() dans la requête pour ne pas affecter les passées
            sql_update_dates = """
                UPDATE PlanningDetails
                SET date_planification = DATE_ADD(date_planification, INTERVAL %s DAY)
                WHERE planning_id = %s AND date_planification >= %s
            """
            await cur.execute(sql_update_dates, (delta_days, planning_data['planning_id'], date_a_modifier))
            print(f"{cur.rowcount} dates de planification futures mises à jour à partir du {date_a_modifier}.")

            # Enregistrer le signalement pour la première planification décalée/avancée
            if first_detail_id_to_signal:
                motif = input(f"Entrez le motif de l'{ajustement_type.lower()} pour la planification du {date_a_modifier}: ").strip()
                sql_insert_signalement = "INSERT INTO Signalement (planning_detail_id, motif, type) VALUES (%s, %s, %s)"
                await cur.execute(sql_insert_signalement, (first_detail_id_to_signal, motif, ajustement_type))
                signalement_id = cur.lastrowid
                print(f"Signalement d'{ajustement_type.lower()} enregistré avec ID: {signalement_id}.")

                # Enregistrer également dans Historique
                # ATTENTION: La FK composite dans Historique (contenu, issue, action) vers Remarque est très inhabituelle.
                # Ici, nous insérons des données directes, non liées à Remarque par cette FK composite.
                # 'issue' et 'action' sont définies comme vides si l'utilisateur ne les fournit pas.
                issue_hist = input("Entrez un problème (issue) lié à ce signalement (laissez vide si aucun): ").strip()
                action_hist = input("Entrez une action entreprise pour ce signalement: ").strip()

                sql_insert_historique = """
                    INSERT INTO Historique (
                        facture_id, planning_detail_id, signalement_id,
                        date_historique, contenu, issue, action
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                # facture_id est NULL ici car ce n'est pas directement lié à une facture existante.
                # contenu est le motif du signalement.
                await cur.execute(sql_insert_historique, (
                    None, # facture_id est NULL pour un signalement pur
                    first_detail_id_to_signal,
                    signalement_id,
                    datetime.now(),
                    motif,
                    issue_hist if issue_hist else "", # Empty string if no issue
                    action_hist if action_hist else "Non spécifié" # Empty string if no action
                ))
                print("Entrée d'historique enregistrée pour le signalement.")

    except aiomysql.Error as e:
        print(f"**Erreur lors de la modification du planning :** {e}")
        # La ligne suivante n'est pas nécessaire si autocommit=True sur le pool.
        # await conn.rollback()
    except Exception as e:
        print(f"**Une erreur inattendue est survenue :** {e}")


async def main():
    pool = None
    try:
        host, port, user, password, database = await get_db_credentials()
        # Use create_pool instead of connect directly for better resource management
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=True, # Ensure transactions are committed
            minsize=1,
            maxsize=5
        )
        print("Connexion à la base de données établie avec succès.")

        client_id = await get_client_id(pool)
        if not client_id:
            print("Opération annulée.")
            return

        planning_data, planning_details, traitements = await get_client_planning(pool, client_id)
        if not planning_data:
            print("Aucun planning trouvé pour ce client. Opération terminée.")
            return

        await display_planning_info(planning_data, planning_details, traitements)

        choix = await get_option_choix()
        if choix == 1:
            await handle_option_1(pool, planning_details)
        elif choix == 2:
            await handle_option_2(pool, planning_data)
        elif choix == 3:
            print("Opération annulée.")
        else:
            print("Choix invalide. Opération annulée.") # This branch should theoretically be unreachable

        print("--- Opération terminée ---")

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