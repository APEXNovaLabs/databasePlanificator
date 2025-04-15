import asyncio
import aiomysql
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

async def get_db_credentials():
    """
    Demande à l'utilisateur les informations de connexion à la base de données.
    """
    host = input("Entrez l'adresse du serveur MySQL (par exemple, localhost): ")
    port_str = input("Entrez le port du serveur MySQL (par défaut: 3306): ")
    try:
        port = int(port_str) if port_str else 3306
    except ValueError:
        print("Port invalide, utilisation de la valeur par défaut (3306).")
        port = 3306
    user = input("Entrez le nom d'utilisateur MySQL: ")
    password = input("Entrez le mot de passe MySQL: ")
    database = input("Entrez le nom de la base de données MySQL (par exemple, Planificator): ")
    return host, port, user, password, database

async def get_client_id(conn):
    """
    Demande à l'utilisateur l'ID du client et vérifie son existence dans la base de données.

    Args:
        conn: La connexion aiomysql à la base de données.

    Returns:
        L'ID du client si trouvé, None sinon.
    """
    cursor = None
    try:
        cursor = await conn.cursor()
        while True:
            client_id_str = input("Entrez l'ID du client dont vous souhaitez ajuster le planning: ")
            try:
                client_id = int(client_id_str)
                # Vérifier si le client existe
                await cursor.execute("SELECT client_id FROM Client WHERE client_id = %s", (client_id,))
                if await cursor.fetchone():
                    return client_id
                else:
                    print("Client non trouvé. Veuillez entrer un ID de client valide.")
            except ValueError:
                print("ID de client invalide. Veuillez entrer un nombre entier.")
    finally:
        if cursor:
            await cursor.close()

async def get_client_planning(conn, client_id):
    """
    Récupère le planning du client, les détails du planning et les traitements associés.

    Args:
        conn: La connexion aiomysql à la base de données.
        client_id: L'ID du client.

    Returns:
        Un tuple contenant les informations du planning, les détails du planning et les traitements.
        Retourne None si une erreur se produit.
    """
    cursor = None;
    try:
        cursor = await conn.cursor(aiomysql.DictCursor)

        # Récupérer le planning principal du client
        sql_planning = """
            SELECT
                p.planning_id, p.date_debut_planification, p.mois_debut, p.mois_fin,
                p.mois_pause, p.duree_traitement, p.unite_duree, p.redondance, p.date_fin_planification
            FROM Planning p
            JOIN Traitement t ON p.traitement_id = t.traitement_id
            JOIN Contrat c ON t.contrat_id = c.client_id
            WHERE c.client_id = %s
        """
        await cursor.execute(sql_planning, (client_id,))
        planning_data = await cursor.fetchone()

        if not planning_data:
            print("Aucun planning trouvé pour ce client.")
            return None, None, None

        planning_id = planning_data['planning_id']

        # Récupérer les détails du planning
        sql_planning_details = """
            SELECT planning_detail_id, date_planification, mois, statut
            FROM PlanningDetails
            WHERE planning_id = %s
            ORDER BY date_planification
        """
        await cursor.execute(sql_planning_details, (planning_id,))
        planning_details = await cursor.fetchall()

        # Récupérer les traitements
        sql_traitements = """
            SELECT t.traitement_id, tt.typeTraitement
            FROM Traitement t
            JOIN Contrat c ON t.contrat_id = c.client_id
            JOIN TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement
            WHERE c.client_id = %s
        """
        await cursor.execute(sql_traitements, (client_id,))
        traitements = await cursor.fetchall()

        return planning_data, planning_details, traitements

    except aiomysql.Error as e:
        print(f"Erreur lors de la récupération du planning du client : {e}")
        return None, None, None
    finally:
        if cursor:
            await cursor.close()

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

    print("\nInformations sur le planning du client :")
    print(f"  Planning ID: {planning_data['planning_id']}")
    print(f"  Date de début de planification: {planning_data['date_debut_planification']}")
    print(f"  Mois de début: {planning_data['mois_debut']}")
    print(f"  Mois de fin: {planning_data['mois_fin']}")
    print(f"  Mois de pause: {planning_data['mois_pause']}")
    print(f"  Durée du traitement: {planning_data['duree_traitement']} {planning_data['unite_duree']}")
    print(f"  Redondance: {planning_data['redondance']}")
    print(f"  Date de fin de planification: {planning_data['date_fin_planification']}")

    print("\nDétails du planning :")
    if not planning_details:
        print("  Aucun détail de planning trouvé.")
    else:
        for detail in planning_details:
            print(f"    ID: {detail['planning_detail_id']}, Date: {detail['date_planification']}, Mois: {detail['mois']}, Statut: {detail['statut']}")

    print("\nTraitements associés :")
    if not traitements:
        print("  Aucun traitement associé.")
    else:
        for traitement in traitements:
            print(f"    ID: {traitement['traitement_id']}, Type: {traitement['typeTraitement']}")

async def get_option_choix():
    """
    Demande à l'utilisateur de choisir comment gérer le planning.

    Returns:
        Le choix de l'utilisateur (1, 2 ou 3), ou None en cas d'erreur.
    """
    while True:
        print("\nChoisissez comment gérer le planning :")
        print("  1. Garder l'état actuel du planning (ajuster uniquement le statut)")
        print("  2. Changer le planning (modifier les dates des traitements futurs)")
        print("  3. Annuler l'opération")
        choix = input("Entrez votre choix (1, 2 ou 3): ")
        if choix in ('1', '2', '3'):
            return int(choix)
        else:
            print("Choix invalide. Veuillez entrer 1, 2 ou 3.")

async def handle_option_1(conn, planning_details):
    """
    Gère l'option de garder l'état actuel du planning (ajuster le statut).

    Args:
        conn: La connexion aiomysql à la base de données.
        planning_details: Les détails du planning.
    """
    cursor = None
    try:
        cursor = await conn.cursor()
        if not planning_details:
            print("Aucun détail de planning à modifier.")
            return

        while True:
            detail_id_str = input("Entrez l'ID du détail du planning que vous souhaitez modifier (ou '0' pour annuler): ")
            if detail_id_str == '0':
                print("Opération annulée.")
                return

            try:
                detail_id = int(detail_id_str)
                #verifier si detail_id existe
                detail_exists = False
                for detail in planning_details:
                    if detail['planning_detail_id'] == detail_id:
                        detail_exists = True
                        break
                if not detail_exists:
                    print("ID de détail du planning invalide")
                    continue
                break
            except ValueError:
                print("ID de détail du planning invalide. Veuillez entrer un nombre entier ou 0.")

        nouveau_statut = input("Entrez le nouveau statut ('Effectué' ou 'À venir'): ") # Correction du statut
        if nouveau_statut not in ('Effectué', 'À venir'):
            print("Statut invalide. Veuillez entrer 'Effectué' ou 'À venir'.")
            return

        sql_update_statut = "UPDATE PlanningDetails SET statut = %s WHERE planning_detail_id = %s"
        await cursor.execute(sql_update_statut, (nouveau_statut, detail_id))
        await conn.commit()
        print("Statut du détail du planning mis à jour.")

        if nouveau_statut == 'Décalage':
            motif = input("Entrez le motif du décalage: ")
            sql_insert_signalement = "INSERT INTO Signalement (planning_detail_id, motif, type) VALUES (%s, %s, %s)"
            await cursor.execute(sql_insert_signalement, (detail_id, motif, 'Décalage'))
            await conn.commit()
            print("Signalement de décalage enregistré.")

    except aiomysql.Error as e:
        print(f"Erreur lors de la mise à jour du statut : {e}")
        await conn.rollback()
    finally:
        if cursor:
            await cursor.close()

async def handle_option_2(conn, planning_data):
    """
    Gère l'option de changer le planning (modifier les dates des traitements futurs).

    Args:
        conn: La connexion aiomysql à la base de données.
        planning_data: Les données du planning principal.
    """
    cursor = None
    try:
        cursor = await conn.cursor()
        ajustement_type = input("S'agit-il d'un 'Avancement' ou d'un 'Décalage' ? ")
        if ajustement_type not in ('Avancement', 'Décalage'):
            print("Type d'ajustement invalide. Veuillez entrer 'Avancement' ou 'Décalage'.")
            return

        date_str = input(f"Entrez la nouvelle date du prochain traitement (AAAA-MM-JJ): ")
        try:
            nouvelle_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Format de date invalide. Veuillez utiliser le format AAAA-MM-JJ.")
            return

        # Trouver la date de la prochaine planification
        sql_next_planification = """
            SELECT MIN(date_planification)
            FROM PlanningDetails
            WHERE planning_id = %s AND date_planification >= CURDATE()
        """
        await cursor.execute(sql_next_planification, (planning_data['planning_id'],))
        result = await cursor.fetchone()
        prochaine_date_planification = result['MIN(date_planification)']

        if not prochaine_date_planification:
            print("Aucune planification future trouvée.")
            return

        # Calculer la différence en jours
        delta_jours = (nouvelle_date - prochaine_date_planification).days
        unite_duree = planning_data['unite_duree'] # Récupérer l'unité de durée

        if unite_duree == 'mois':
            delta_mois = (nouvelle_date.year - prochaine_date_planification.year) * 12 + (nouvelle_date.month - prochaine_date_planification.month)
            sql_update_dates = """
                UPDATE PlanningDetails
                SET date_planification = DATE_ADD(date_planification, INTERVAL %s MONTH)
                WHERE planning_id = %s AND date_planification >= CURDATE()
            """
            await cursor.execute(sql_update_dates, (delta_mois, planning_data['planning_id']))
        elif unite_duree == 'années':
            delta_ans = nouvelle_date.year - prochaine_date_planification.year
            sql_update_dates = """
                UPDATE PlanningDetails
                SET date_planification = DATE_ADD(date_planification, INTERVAL %s YEAR)
                WHERE planning_id = %s AND date_planification >= CURDATE()
            """
            await cursor.execute(sql_update_dates, (delta_ans, planning_data['planning_id']))
        else:
            sql_update_dates = """
                UPDATE PlanningDetails
                SET date_planification = DATE_ADD(date_planification, INTERVAL %s DAY)
                WHERE planning_id = %s AND date_planification >= CURDATE()
            """
            await cursor.execute(sql_update_dates, (delta_jours, planning_data['planning_id']))

        await conn.commit()
        print("Dates de planification futures mises à jour.")

        # Enregistrer le signalement
        motif = input(f"Entrez le motif de l'{ajustement_type.lower()}: ")
        sql_insert_signalement = "INSERT INTO Signalement (planning_detail_id, motif, type) VALUES (NULL, %s, %s)"
        await cursor.execute(sql_insert_signalement, (motif, ajustement_type))
        await conn.commit()
        print(f"Signalement d'{ajustement_type.lower()} enregistré.")

    except aiomysql.Error as e:
        print(f"Erreur lors de la modification du planning : {e}")
        await conn.rollback()
    finally:
        if cursor:
            await cursor.close()

async def main():
    conn = None
    try:
        host, port, user, password, database = await get_db_credentials()
        conn = await aiomysql.connect(host=host, port=port, user=user, password=password, db=database)

        client_id = await get_client_id(conn)
        if not client_id:
            print("Opération annulée.")
            return

        planning_data, planning_details, traitements = await get_client_planning(conn, client_id)
        if not planning_data:
            print("Opération terminée.")
            return

        await display_planning_info(planning_data, planning_details, traitements)

        choix = await get_option_choix()
        if choix == 1:
            await handle_option_1(conn, planning_details)
        elif choix == 2:
            await handle_option_2(conn, planning_data)
        elif choix == 3:
            print("Opération annulée.")
        else:
            print("Choix invalide. Opération annulée.")

        print("Opération terminée.")

    except aiomysql.Error as e:
        print(f"Erreur MySQL: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    asyncio.run(main())
