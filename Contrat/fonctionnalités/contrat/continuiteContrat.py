import aiomysql
import asyncio
from datetime import datetime, timedelta

async def verifier_statut_contrat(pool, contrat_id):
    """Vérifie le statut d'un contrat."""

    async with pool.acquire as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT statut_contrat FROM Contrat WHERE contrat_id = %s", (contrat_id,))
            statut = await cur.fetchone()

            if statut:
                print(f"Statut du contrat {contrat_id}: {statut[0]}")
            else:
                print(f"Contrat avec l'ID {contrat_id} non trouvé.")

async def gerer_continuité_contrat(pool, contrat_id):
    """Gère la continuité d'un contrat."""

    async with pool.acquire as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT duree, date_fin, duree_contrat FROM Contrat WHERE contrat_id = %s", (contrat_id,))
            contrat = await cur.fetchone()

            if not contrat:
                print(f"Contrat avec l'ID {contrat_id} non trouvé.")
                return

            duree, date_fin_contrat, duree_contrat = contrat

            if duree == 'Déterminée':
                if date_fin_contrat and date_fin_contrat <= datetime.now().date():
                    choix = input("Souhaitez-vous renouveler le contrat ? (oui/non) : ")
                    if choix.lower() == 'oui':
                        nouvelle_date_fin = date_fin_contrat + timedelta(months=duree_contrat)
                        await cur.execute("UPDATE Contrat SET date_fin = %s WHERE contrat_id = %s", (nouvelle_date_fin, contrat_id))
                        print("Contrat renouvelé.")
                    else:
                        await cur.execute("UPDATE Contrat SET statut_contrat = 'Terminé' WHERE contrat_id = %s", (contrat_id,))
                        print("Contrat terminé.")
            elif duree == 'Indeterminée':
                choix = input("Souhaitez-vous arrêter le contrat ? (oui/non) : ")
                if choix.lower() == 'oui':
                    await cur.execute("UPDATE Contrat SET statut_contrat = 'Terminé' WHERE contrat_id = %s", (contrat_id,))
                    print("Contrat terminé.")

async def main():
    # Connexion à la base de données
    host = input("Hôte de la base de données (par défaut : localhost) : ")
    if not host:
        host = "localhost"

    port_str = input("Port de la base de données (par défaut : 3306) : ")
    if port_str:
        try:
            port = int(port_str)
        except ValueError:
            print("Port invalide. Utilisation du port par défaut 3306.")
            port = 3306
    else:
        port = 3306

    user = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    database = input("Nom de la base de données (Planificator): ")
    if not database:
        database = "Planificator"

    try:
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=True
        )
    finally:
        if pool:
            pool.close()
            await pool.wait_closed()

    contrat_id = int(input("ID du contrat : "))
    choix = input("Vérifier le statut (1) ou gérer la continuité (2) ? ")

    if choix == '1':
        await verifier_statut_contrat(pool, contrat_id)
    elif choix == '2':
        await gerer_continuité_contrat(pool, contrat_id)

    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())