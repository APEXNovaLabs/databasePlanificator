import aiomysql
import asyncio

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

async def afficher_planning_traitement(pool, client_id: int, traitement_id: int):
    """Affiche les détails de planification d'un traitement pour un client."""
    try:
        # Acquérir une connexion du pool. Le 'async with' assure qu'elle est relâchée.
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur: # Utilisation de DictCursor pour des résultats plus lisibles
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
                    print(f"**Avertissement :** Traitement avec l'ID {traitement_id} non trouvé.")
                    return

                # Accéder aux valeurs par leur nom de colonne
                categorie_traitement = traitement_info['categorieTraitement']
                type_traitement = traitement_info['typeTraitement']
                redondance = traitement_info['redondance']

                # Récupérer les détails de planification
                await cur.execute("""
                    SELECT pd.date_planification, pd.statut
                    FROM PlanningDetails pd
                    JOIN Planning p ON pd.planning_id = p.planning_id
                    JOIN Traitement t ON p.traitement_id = t.traitement_id
                    JOIN Contrat c ON t.contrat_id = c.contrat_id
                    WHERE c.client_id = %s AND t.traitement_id = %s
                    ORDER BY pd.date_planification ASC
                """, (client_id, traitement_id))
                planning_details = await cur.fetchall()

                if not planning_details:
                    print(f"**Avertissement :** Aucun détail de planification trouvé pour le client {client_id} et le traitement {traitement_id}.")
                    return

                # Calculer le nombre de traitements effectués
                traitements_effectues = sum(1 for detail in planning_details if detail['statut'] == 'Effectué')

                # Afficher les informations
                print("\n" + "="*40)
                print(f"--- Détails du Traitement et Planification ---")
                print(f"Traitement ID : {traitement_id}")
                print(f"Catégorie du traitement: {categorie_traitement}")
                print(f"Type de traitement: {type_traitement}")
                print(f"Redondance: {redondance}")
                print(f"**Traitements effectués :** {traitements_effectues}")
                print("\n**Détails de la planification :**")
                for detail in planning_details:
                    # Formatage de la date pour un affichage plus propre
                    date_formatted = detail['date_planification'].strftime('%Y-%m-%d')
                    print(f"  Date: {date_formatted}, Statut: {detail['statut']}")
                print("="*40 + "\n")

    except Exception as e:
        print(f"Une erreur est survenue lors de l'accès à la base de données : {e}")

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
            autocommit=True, # S'assurer que les modifications sont auto-validées
            minsize=1,       # Taille minimale du pool
            maxsize=5        # Taille maximale du pool
        )
        print("Connexion à la base de données établie avec succès.")

        while True:
            client_id_input = input("\nEntrez l'ID du client pour afficher le planning (laissez vide pour quitter): ").strip()
            if not client_id_input:
                break # Quitter la boucle si l'utilisateur n'entre rien

            try:
                client_id = int(client_id_input)
            except ValueError:
                print("Erreur : L'ID du client doit être un nombre entier. Veuillez réessayer.")
                continue # Recommencer la boucle

            traitement_id_input = input("Entrez l'ID du traitement pour afficher le planning (laissez vide pour quitter): ").strip()
            if not traitement_id_input:
                break # Quitter la boucle si l'utilisateur n'entre rien

            try:
                traitement_id = int(traitement_id_input)
            except ValueError:
                print("Erreur : L'ID du traitement doit être un nombre entier. Veuillez réessayer.")
                continue # Recommencer la boucle

            await afficher_planning_traitement(pool, client_id, traitement_id)

            # Demander à l'utilisateur s'il souhaite continuer
            reponse = input("Voulez-vous afficher le planning d'un autre client/traitement ? (oui/non): ").strip().lower()
            if reponse != 'oui':
                break # Quitter la boucle si la réponse n'est pas 'oui'

    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")
    finally:
        # S'assurer que le pool est fermé même en cas d'erreur
        if pool:
            print("\nFermeture du pool de connexions à la base de données...")
            pool.close()
            await pool.wait_closed()
            print("Pool de connexions fermé.")

if __name__ == "__main__":
    asyncio.run(main())