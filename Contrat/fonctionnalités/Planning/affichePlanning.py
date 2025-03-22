import aiomysql
import asyncio

async def afficher_planning_traitement(pool, client_id, traitement_id):
    """Affiche les détails de planification d'un traitement pour un client."""

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Récupérer les informations du traitement
            await cur.execute("""
                SELECT tt.categorieTraitement, tt.typeTraitement, p.redondance
                FROM Traitement t
                JOIN TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement
                JOIN Planning p ON t.traitement_id = p.traitement_id
                WHERE t.traitement_id = %s
            """, (traitement_id,))
            traitement_info = await cur.fetchone()

            if not traitement_info:
                print("Traitement non trouvé.")
                return

            categorie_traitement, type_traitement, redondance = traitement_info

            # Récupérer les détails de planification
            await cur.execute("""
                SELECT pd.date_planification, pd.statut
                FROM PlanningDetails pd
                JOIN Planning p ON pd.planning_id = p.planning_id
                JOIN Traitement t ON p.traitement_id = t.traitement_id
                JOIN Contrat c ON t.contrat_id = c.contrat_id
                WHERE c.client_id = %s AND t.traitement_id = %s
            """, (client_id, traitement_id))
            planning_details = await cur.fetchall()

            # Calculer le nombre de traitements effectués
            traitements_effectues = sum(1 for _, statut in planning_details if statut == 'Effectué')

            # Afficher les informations
            print(f"Catégorie du traitement: {categorie_traitement}")
            print(f"Type de traitement: {type_traitement}")
            print(f"Redondance: {redondance}")
            print(f"Traitements effectués: {traitements_effectues}")
            print("\nDétails de la planification:")
            for date_planification, statut in planning_details:
                print(f"  Date: {date_planification}, Statut: {statut}")

async def main():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='votre_utilisateur', password='votre_mot_de_passe',
                                      db='Planificator', autocommit=True)

    client_id = int(input("ID du client: "))
    traitement_id = int(input("ID du traitement: "))

    await afficher_planning_traitement(pool, client_id, traitement_id)

    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())