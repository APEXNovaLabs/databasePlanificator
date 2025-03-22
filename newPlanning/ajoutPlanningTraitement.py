import aiomysql
import asyncio
from datetime import datetime, timedelta

async def ajouter_planning_traitement(pool, traitement_id, redondance, date_debut_planification):
    """Ajoute un planning pour un traitement donné."""

    # Vérifier si le traitement existe
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Traitement WHERE traitement_id = %s", (traitement_id,))
            traitement = await cur.fetchone()

            if not traitement:
                print(f"Traitement avec l'ID {traitement_id} non trouvé.")
                return

            # Calculer la date de fin de la planification (1 an par défaut)
            date_fin_planification = date_debut_planification + timedelta(days=365)

            # Insérer le planning principal
            await cur.execute("""
                INSERT INTO Planning (traitement_id, redondance, date_debut_planification, date_fin_planification)
                VALUES (%s, %s, %s, %s)
            """, (traitement_id, redondance, date_debut_planification, date_fin_planification))

            planning_id = cur.lastrowid

            # Calculer et insérer les détails de la planification
            date_planification = date_debut_planification
            while date_planification <= date_fin_planification:
                await cur.execute("""
                    INSERT INTO PlanningDetails (planning_id, date_planification, statut, element_planification)
                    VALUES (%s, %s, 'À venir', 'Traitement')
                """, (planning_id, date_planification))

                # Calculer la prochaine date de planification
                if redondance == 1:  # Hebdomadaire
                    date_planification += timedelta(weeks=1)
                elif redondance == 1:  # Mensuel
                    date_planification += timedelta(days=30)  # Approximation
                elif redondance == 2:  # 2 mois
                    date_planification += timedelta(days=60)
                elif redondance == 3:  # 3 mois
                    date_planification += timedelta(days=90)
                elif redondance == 4:  # 4 mois
                    date_planification += timedelta(days=120)
                elif redondance == 6:  # 6 mois
                    date_planification += timedelta(days=180)
                elif redondance == 12: # 12 mois
                    date_planification += timedelta(days=365)
                else:
                    print("Redondance non valide.")
                    return

async def main():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='votre_utilisateur', password='votre_mot_de_passe',
                                      db='Planificator', autocommit=True)

    traitement_id = int(input("ID du traitement : "))
    redondance = int(input("Redondance (1: Hebdomadaire, 1: Mensuel, 2: 2 mois, etc.) : "))
    date_debut_planification_str = input("Date de début (YYYY-MM-DD) : ")
    date_debut_planification = datetime.strptime(date_debut_planification_str, '%Y-%m-%d').date()

    await ajouter_planning_traitement(pool, traitement_id, redondance, date_debut_planification)

    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())