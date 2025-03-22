import aiomysql
import asyncio
from datetime import datetime

async def mettre_a_jour_planning_detail(pool, planning_detail_id, statut):
    """Met à jour le statut de PlanningDetails et enregistre l'historique."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Récupérer l'état de la facture
            await cur.execute("SELECT etat FROM Facture WHERE planning_detail_id = %s", (planning_detail_id,))
            resultat = await cur.fetchone()
            etat_facture = resultat[0] if resultat else "Non disponible"

            # Mettre à jour le statut de PlanningDetails
            await cur.execute("UPDATE PlanningDetails SET statut = %s WHERE planning_detail_id = %s", (statut, planning_detail_id))

            # Enregistrer l'historique si le statut est "Effectué"
            if statut == "Effectué":
                await cur.execute("""
                    INSERT INTO Historique (planning_detail_id, contenu)
                    VALUES (%s, %s)
                """, (planning_detail_id, f"Traitement effectué. État de la facture : {etat_facture}."))

            await conn.commit()

async def main():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='votre_utilisateur', password='votre_mot_de_passe',
                                      db='Planificator', autocommit=True)

    planning_detail_id = int(input("ID du détail de planification: "))
    statut = input("Nouveau statut (Effectué/À venir): ")

    await mettre_a_jour_planning_detail(pool, planning_detail_id, statut)
    print("Statut mis à jour.")

    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())