import aiomysql
import asyncio

async def trier_traitements_par_categorie(pool):
    """Trie les traitements de tous les clients par catégories."""

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT c.nom, tt.categorieTraitement, tt.typeTraitement
                FROM Client c
                JOIN Contrat co ON c.client_id = co.client_id
                JOIN Traitement t ON co.contrat_id = t.contrat_id
                JOIN TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement
                ORDER BY tt.categorieTraitement, c.nom
            """)
            traitements = await cur.fetchall()

            if traitements:
                print("Traitements des clients par catégories :")
                for nom_client, categorie_traitement, type_traitement in traitements:
                    print(f"Client: {nom_client}, Catégorie: {categorie_traitement}, Type: {type_traitement}")
            else:
                print("Aucun traitement trouvé.")

async def main():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='votre_utilisateur', password='votre_mot_de_passe',
                                      db='Planificator', autocommit=True)

    await trier_traitements_par_categorie(pool)

    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())