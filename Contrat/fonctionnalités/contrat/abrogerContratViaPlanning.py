import datetime
import asyncio
import aiomysql
from ..Excel.connexionDB import DBConnection


async def get_planning_detail_info(pool, planning_detail_id: int):
    """
    Récupère les informations détaillées d'un planning_detail spécifique,
    incluant les IDs du planning, traitement et contrat associés.
    Prend le pool de connexions en argument.
    """
    conn = None
    try:
        conn = await pool.acquire()  # Obtenir une connexion du pool
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT pd.planning_detail_id, \
                           pd.planning_id, \
                           pd.date_planification, \
                           pd.statut, \
                           p.traitement_id, \
                           t.contrat_id
                    FROM PlanningDetails pd \
                             JOIN \
                         Planning p ON pd.planning_id = p.planning_id \
                             JOIN \
                         Traitement t ON p.traitement_id = t.traitement_id
                    WHERE pd.planning_detail_id = %s; \
                    """
            await cursor.execute(query, (planning_detail_id,))
            result = await cursor.fetchone()
            return result
    except Exception as e:
        print(f"Erreur lors de la récupération des informations du planning_detail {planning_detail_id}: {e}")
        return None
    finally:
        if conn:
            pool.release(conn)  # Relâcher la connexion dans le pool


async def mark_treatment_as_performed(pool, planning_detail_id: int):
    """
    Marque un traitement (planning_detail) comme 'Effectué'.
    Prend le pool de connexions en argument.
    """
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor() as cursor:
            query = """
                    UPDATE PlanningDetails
                    SET statut = 'Effectué'
                    WHERE planning_detail_id = %s; \
                    """
            await cursor.execute(query, (planning_detail_id,))
            print(
                f"Le traitement (planning_detail_id: {planning_detail_id}) a été marqué comme 'Effectué' avec succès.")
            return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour du statut du traitement {planning_detail_id}: {e}")
        return False
    finally:
        if conn:
            pool.release(conn)


async def abrogate_contract(pool, planning_detail_id: int, resignation_date: datetime.date):
    """
    Abroge un contrat à partir d'une date de résiliation.
    Supprime les traitements futurs et marque le contrat comme 'Terminé'.
    Prend le pool de connexions en argument.
    """
    conn = None
    try:
        conn = await pool.acquire()
        # 1. Récupérer les informations initiales pour obtenir planning_id et contrat_id
        # Passez le pool à get_planning_detail_info
        detail_info = await get_planning_detail_info(pool, planning_detail_id)
        if not detail_info:
            print(f"Impossible de trouver les informations pour planning_detail_id {planning_detail_id}.")
            return False

        current_planning_id = detail_info['planning_id']
        current_contrat_id = detail_info['contrat_id']

        async with conn.cursor() as cursor:
            # 2. Supprimer les traitements (PlanningDetails) futurs pour ce planning
            delete_query = """
                           DELETE \
                           FROM PlanningDetails
                           WHERE planning_id = %s \
                             AND date_planification > %s; \
                           """
            await cursor.execute(delete_query, (current_planning_id, resignation_date))
            deleted_count = cursor.rowcount
            print(
                f"{deleted_count} traitements futurs (PlanningDetails) associés au planning {current_planning_id} ont été supprimés après le {resignation_date}.")

            # 3. Mettre à jour le statut du contrat
            update_contract_query = """
                                    UPDATE Contrat
                                    SET statut_contrat = 'Terminé', \
                                        date_fin       = %s, \
                                        duree          = 'Déterminée'
                                    WHERE contrat_id = %s; \
                                    """
            await cursor.execute(update_contract_query, (resignation_date, current_contrat_id))

            print(
                f"Le contrat {current_contrat_id} a été marqué comme 'Terminé' avec date de fin {resignation_date} avec succès.")
            return True

    except Exception as e:
        print(f"Erreur lors de l'abrogation du contrat ou de la suppression des traitements: {e}")
        return False
    finally:
        if conn:
            pool.release(conn)


async def main_contract_management():
    pool = None  # Initialiser le pool à None
    try:
        pool = await DBConnection()  # Appel de la fonction asynchrone pour obtenir le pool
        if not pool:  # Si la création du pool a échoué
            print("Échec de la connexion à la base de données. Annulation de l'opération.")
            return

        print("\n--- Gestion des Contrats et Traitements ---")

        while True:
            try:
                planning_detail_id_input = input(
                    "Veuillez entrer l'ID du détail de planification (planning_detail_id) concerné : ")
                planning_detail_id = int(planning_detail_id_input)

                # Passer le pool aux fonctions
                detail_info = await get_planning_detail_info(pool, planning_detail_id)
                if not detail_info:
                    print(
                        "L'ID du détail de planification spécifié n'existe pas ou une erreur est survenue. Veuillez réessayer.")
                    continue

                print(f"\nInformations pour planning_detail_id {planning_detail_id}:")
                print(f"  Date de planification: {detail_info['date_planification']}")
                print(f"  Statut actuel: {detail_info['statut']}")
                print(f"  Associé au planning_id: {detail_info['planning_id']}")
                print(f"  Associé au contrat_id: {detail_info['contrat_id']}")

                print("\nOptions disponibles:")
                print("1. Abroger le contrat (supprime les traitements futurs et termine le contrat)")
                print("2. Marquer ce traitement comme 'Effectué'")
                print("3. Annuler")

                choice = input("Votre choix (1, 2 ou 3) : ")

                if choice == '1':
                    while True:
                        resignation_date_str = input("Veuillez entrer la date de résiliation (AAAA-MM-JJ) : ")
                        try:
                            resignation_date = datetime.datetime.strptime(resignation_date_str, "%Y-%m-%d").date()
                            break
                        except ValueError:
                            print("Format de date invalide. Veuillez utiliser AAAA-MM-JJ.")

                    print(
                        f"\nTentative d'abrogation du contrat lié à planning_detail_id {planning_detail_id} à partir du {resignation_date}...")
                    success = await abrogate_contract(pool, planning_detail_id, resignation_date)  # Passer le pool
                    if success:
                        print("Opération d'abrogation terminée avec succès.")
                    else:
                        print("L'opération d'abrogation a échoué.")
                    break

                elif choice == '2':
                    print(f"\nTentative de marquer planning_detail_id {planning_detail_id} comme 'Effectué'...")
                    success = await mark_treatment_as_performed(pool, planning_detail_id)  # Passer le pool
                    if success:
                        print("Le traitement a été marqué comme 'Effectué' avec succès.")
                    else:
                        print("L'opération de marquage a échoué.")
                    break

                elif choice == '3':
                    print("Opération annulée.")
                    break

                else:
                    print("Choix invalide. Veuillez entrer 1, 2 ou 3.")

            except ValueError:
                print("Entrée invalide. Veuillez entrer un nombre pour l'ID du détail de planification.")
            except Exception as e:
                print(f"Une erreur inattendue est survenue: {e}")
    finally:
        if pool:
            pool.close()  # Fermer le pool à la fin de l'exécution du script


if __name__ == "__main__":
    asyncio.run(main_contract_management())