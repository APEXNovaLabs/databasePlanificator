import aiomysql
import asyncio
from datetime import datetime

async def ajouter_facture_remarque(pool, remarque_id):
    """Ajoute une facture automatique pour une remarque effectuée et payée."""

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Récupérer les informations de la remarque
            await cur.execute("""
                SELECT r.planning_detail_id, f.facture_id
                FROM Remarque r
                LEFT JOIN Facture f ON r.facture_id = f.facture_id
                JOIN PlanningDetails pd ON r.planning_detail_id = pd.planning_detail_id
                WHERE r.remarque_id = %s AND pd.statut = 'Effectué' AND f.etat = 'Payé'
            """, (remarque_id,))
            remarque_info = await cur.fetchone()

            if not remarque_info:
                print("La remarque n'est pas effectuée ou la facture n'est pas payée.")
                return

            planning_detail_id, facture_id = remarque_info

            # Récupérer les informations nécessaires pour la facture
            await cur.execute("""
                SELECT c.axe, pd.date_planification
                FROM Contrat c
                JOIN Traitement t ON c.contrat_id = t.contrat_id
                JOIN Planning p ON t.traitement_id = p.traitement_id
                JOIN PlanningDetails pd ON p.planning_id = pd.planning_id
                WHERE pd.planning_detail_id = %s
            """, (planning_detail_id,))
            facture_info = await cur.fetchone()

            if not facture_info:
                print("Informations de facture non trouvées.")
                return

            axe, date_traitement = facture_info

            # Calculer le montant de la facture (exemple : 100)
            montant = 100

            # Ajouter la facture
            await cur.execute("""
                INSERT INTO Facture (planning_detail_id, montant, date_traitement, axe, etat)
                VALUES (%s, %s, %s, %s, 'Payé')
            """, (planning_detail_id, montant, date_traitement, axe, 'Payé'))

            print("Facture ajoutée avec succès.")

async def main():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='votre_utilisateur', password='votre_mot_de_passe',
                                      db='Planificator', autocommit=True)

    remarque_id = int(input("ID de la remarque: "))

    await ajouter_facture_remarque(pool, remarque_id)

    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())