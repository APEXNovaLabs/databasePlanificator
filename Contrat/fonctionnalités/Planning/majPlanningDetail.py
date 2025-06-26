import aiomysql
import asyncio
from datetime import datetime

async def get_db_credentials():
    """Demande à l'utilisateur les identifiants de connexion à la base de données."""
    print("\nVeuillez entrer les informations de connexion à la base de données MySQL:")
    host = input("Entrez l'adresse du serveur MySQL (par défaut, localhost): ").strip()
    if not host:
        host = "localhost"

    port_str = input("Entrez le port du serveur MySQL (par défaut: 3306): ").strip()
    try:
        port = int(port_str) if port_str else 3306
    except ValueError:
        print("Port invalide, utilisation de la valeur par défaut (3306).")
        port = 3306

    user = input("Entrez le nom d'utilisateur MySQL: ").strip()
    password = input("Entrez le mot de passe MySQL: ").strip()
    database = input("Entrez le nom de la base de données MySQL (par défaut, Planificator): ").strip()
    if not database:
        database = "Planificator"
    return host, port, user, password, database

async def mettre_a_jour_planning_detail(pool, planning_detail_id: int, statut: str):
    """
    Met à jour le statut de PlanningDetails et enregistre l'historique si le statut est "Effectué".

    Args:
        pool: Le pool de connexions aiomysql.
        planning_detail_id (int): L'ID du détail de planification à mettre à jour.
        statut (str): Le nouveau statut ('Effectué' ou 'À venir').
    """
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # 1. Vérifier si le planning_detail_id existe
                await cur.execute("SELECT planning_id FROM PlanningDetails WHERE planning_detail_id = %s", (planning_detail_id,))
                detail_exists = await cur.fetchone()
                if not detail_exists:
                    print(f"**Erreur:** Le détail de planification avec l'ID {planning_detail_id} n'existe pas. Aucune mise à jour effectuée.")
                    return

                # 2. Récupérer l'état de la facture associée (si elle existe)
                etat_facture = "Non disponible" # Valeur par défaut
                try:
                    await cur.execute("SELECT etat FROM Facture WHERE planning_detail_id = %s", (planning_detail_id,))
                    resultat_facture = await cur.fetchone()
                    if resultat_facture and 'etat' in resultat_facture:
                        etat_facture = resultat_facture['etat']
                except Exception as e:
                    print(f"**Avertissement:** Erreur lors de la récupération de l'état de la facture pour planning_detail_id {planning_detail_id}: {e}. L'historique utilisera 'Non disponible'.")


                # 3. Mettre à jour le statut de PlanningDetails
                await cur.execute("UPDATE PlanningDetails SET statut = %s WHERE planning_detail_id = %s", (statut, planning_detail_id))
                rows_affected = cur.rowcount

                if rows_affected == 0:
                    print(f"**Avertissement:** Aucune ligne mise à jour pour planning_detail_id {planning_detail_id}. Le statut était peut-être déjà '{statut}'.")
                else:
                    print(f"Statut du détail de planification {planning_detail_id} mis à jour en '{statut}'.")

                # 4. Enregistrer l'historique si le statut est "Effectué"
                if statut == "Effectué":
                    contenu_historique = f"Traitement effectué. État de la facture : {etat_facture}."
                    await cur.execute("""
                        INSERT INTO Historique (planning_detail_id, contenu, date_creation)
                        VALUES (%s, %s, %s)
                    """, (planning_detail_id, contenu_historique, datetime.now()))
                    print(f"Historique enregistré pour planning_detail_id {planning_detail_id}.")

                # conn.commit() est optionnel ici si autocommit=True est défini sur le pool.
                # Mais il n'y a pas de mal à le laisser pour la clarté ou si autocommit=False.
                # await conn.commit()

    except Exception as e:
        print(f"**Erreur lors de la mise à jour du planning_detail {planning_detail_id}:** {e}")

async def main():
    pool = None # Initialiser le pool à None
    try:
        # Récupérer les identifiants de la base de données
        host, port, user, password, database = await get_db_credentials()

        # Créer le pool de connexions avec les identifiants fournis par l'utilisateur
        print(f"\nTentative de connexion à la base de données '{database}' sur {host}:{port} avec l'utilisateur '{user}'...")
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=True, # Auto-commit les opérations
            minsize=1,       # Taille minimale du pool
            maxsize=5        # Taille maximale du pool
        )
        print("Connexion à la base de données établie avec succès.")

        while True:
            print("\n--- Mise à jour du statut d'un détail de planification ---")
            planning_detail_id_input = input("Entrez l'ID du détail de planification à mettre à jour (laissez vide pour quitter) : ").strip()
            if not planning_detail_id_input:
                break # Quitter la boucle si l'utilisateur n'entre rien

            try:
                planning_detail_id = int(planning_detail_id_input)
            except ValueError:
                print("**Erreur :** L'ID du détail de planification doit être un nombre entier. Veuillez réessayer.")
                continue # Recommencer la boucle

            statut_input = input("Entrez le nouveau statut ('Effectué' ou 'À venir') : ").strip()
            if statut_input.lower() not in ['effectué', 'à venir']:
                print("**Erreur :** Statut invalide. Veuillez entrer 'Effectué' ou 'À venir'.")
                continue # Recommencer la boucle

            # Capitaliser la première lettre pour correspondre aux valeurs de l'ENUM si nécessaire
            statut = statut_input.capitalize()

            await mettre_a_jour_planning_detail(pool, planning_detail_id, statut)

            # Demander à l'utilisateur s'il souhaite continuer
            reponse = input("\nVoulez-vous mettre à jour un autre détail de planification ? (oui/non) : ").strip().lower()
            if reponse != 'oui':
                break # Quitter la boucle si la réponse n'est pas 'oui'

    except Exception as e:
        print(f"**Une erreur inattendue est survenue dans le script principal :** {e}")
    finally:
        # S'assurer que le pool est fermé même en cas d'erreur
        if pool:
            print("\nFermeture du pool de connexions à la base de données...")
            pool.close()
            await pool.wait_closed()
            print("Pool de connexions fermé.")

if __name__ == "__main__":
    asyncio.run(main())