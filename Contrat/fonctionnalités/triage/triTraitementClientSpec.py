import aiomysql
import asyncio

async def trier_traitements_client_par_categorie(pool, client_id):
    """Trie les traitements d'un client spécifique par catégories."""

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT tt.categorieTraitement, tt.typeTraitement
                FROM Client c
                JOIN Contrat co ON c.client_id = co.client_id
                JOIN Traitement t ON co.contrat_id = t.contrat_id
                JOIN TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement
                WHERE c.client_id = %s
                ORDER BY tt.categorieTraitement
            """, (client_id,))
            traitements = await cur.fetchall()

            if traitements:
                print(f"Traitements du client (ID: {client_id}) par catégories :")
                for categorie_traitement, type_traitement in traitements:
                    print(f"Catégorie: {categorie_traitement}, Type: {type_traitement}")
            else:
                print("Aucun traitement trouvé pour ce client.")

async def main():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='votre_utilisateur', password='votre_mot_de_passe',
                                      db='Planificator', autocommit=True)

    client_id = int(input("ID du client: "))

    await trier_traitements_client_par_categorie(pool, client_id)

    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())