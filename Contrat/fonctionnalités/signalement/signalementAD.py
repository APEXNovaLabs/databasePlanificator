import asyncio
import aiomysql
from datetime import datetime

# Importez les fonctions nécessaires du fichier principal
from gestionEtatSignalement import get_db_credentials, get_client_id, get_client_planning, display_planning_info, get_option_choix, handle_option_1, handle_option_2

async def enregistrer_signalement(conn, planning_detail_id, motif, type_signalement):
    """
    Enregistre un signalement dans la base de données.

    Args:
        conn: La connexion aiomysql à la base de données.
        planning_detail_id: L'ID du détail de planification concerné par le signalement.
        motif: Le motif du signalement.
        type_signalement: Le type de signalement ('Avancement' ou 'Décalage').

    Returns:
        True si le signalement est enregistré avec succès, False sinon.
    """
    cursor = None
    try:
        cursor = await conn.cursor()
        sql_insert_signalement = "INSERT INTO Signalement (planning_detail_id, motif, type) VALUES (%s, %s, %s)"
        await cursor.execute(sql_insert_signalement, (planning_detail_id, motif, type_signalement))
        await conn.commit()
        print(f"Signalement de {type_signalement} enregistré.")
        return True
    except aiomysql.Error as e:
        print(f"Erreur lors de l'enregistrement du signalement : {e}")
        await conn.rollback()
        return False
    finally:
        if cursor:
            await cursor.close()

async def main():
    conn = None
    try:
        # Établir la connexion à la base de données en utilisant la fonction du fichier principal
        host, port, user, password, database = await get_db_credentials()
        conn = await aiomysql.connect(host=host, port=port, user=user, password=password, db=database)

        # Demander l'ID du client
        client_id = await get_client_id(conn)
        if not client_id:
            print("Opération annulée.")
            return

        # Récupérer les informations du planning du client
        planning_data, planning_details, traitements = await get_client_planning(conn, client_id)
        if not planning_data:
            print("Opération terminée.")
            return

        # Afficher les informations du planning
        await display_planning_info(planning_data, planning_details, traitements)

        # Demander à l'utilisateur de choisir comment gérer le planning
        choix = await get_option_choix()

        if choix == 1:
            await handle_option_1(conn, planning_details)
        elif choix == 2:
            await handle_option_2(conn, planning_data)
        else:
            print("Choix invalide.  Opération annulée.")

    except aiomysql.Error as e:
        print(f"Erreur MySQL : {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    asyncio.run(main())
