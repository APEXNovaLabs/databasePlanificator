import asyncio
import aiomysql

async def rechercher_client(pool, search_term):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT c.*, tt.nom_type_traitement, p.mois_debut, ct.date_ajout 
                FROM Client c
                LEFT JOIN Contrat ct ON c.client_id = ct.client_id
                LEFT JOIN Traitement t ON ct.contrat_id = t.contrat_id
                LEFT JOIN TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement
                LEFT JOIN Planning p ON t.traitement_id = p.traitement_id
                WHERE c.nom LIKE %s OR c.prenom LIKE %s
            """, (f"%{search_term}%", f"%{search_term}%"))
            return await cur.fetchall()

async def afficher_clients(clients):
    if clients:
        print("\nClients trouvés :")
        for client in clients:
            print(f"ID: {client[0]}, Nom: {client[1]}, Prénom: {client[2]}, Email: {client[3]}, "
                  f"Type de traitement: {client[8] or 'Aucun'}, Mois de début planning: {client[9] or 'Aucun'}, Date d'ajout contrat: {client[10] or 'Aucune'}")
    else:
        print("\nAucun client trouvé.")

async def tri_client(clients, sort_by):
    if sort_by == 'traitement':
        return sorted(clients, key=lambda x: x[8] or '')  # Tri par type de traitement
    elif sort_by == 'mois':
        return sorted(clients, key=lambda x: x[9] or '')  # Tri par mois de début planning
    elif sort_by == 'date':
        return sorted(clients, key=lambda x: x[10] or '')  # Tri par date d'ajout contrat
    else:
        return clients

async def actualiser_data(pool, search_term=None): # Paramètre search_term optionnel
    print("\nDonnées mises à jour.")
    if search_term:
        return await rechercher_client(pool, search_term)
    return None

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
    database = input("Nom de la base de données : ")

    try:
        # Créer le pool de connexions
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=True
        )
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return

    try:
        while True:
            print("\nMenu principal:")
            print("1. Rechercher un client")
            print("2. Trier les résultats")
            print("3. Actualiser les données")
            print("4. Quitter")

            choice = input("Choisissez une option : ")

            if choice == '4':
                break

            elif choice == '1':
                search_term = input("Entrez le terme de recherche (nom ou prénom) : ")
                clients = await rechercher_client(pool, search_term)
                afficher_clients(clients)
            elif choice == '2':
                if 'clients' in locals() and clients:  # Vérifier si une recherche a été effectuée
                    sort_by = input("Trier par (traitement/mois) : ").lower()
                    clients = tri_client(clients, sort_by)
                    afficher_clients(clients)
                else:
                    print("Veuillez d'abord effectuer une recherche.")
            elif choice == '3':
                await actualiser_data(pool)
                if 'search_term' in locals() and search_term: # Vérifier si une recherche a été effectuée
                    clients = await rechercher_client(pool, search_term)
                    afficher_clients(clients)
            else:
                print("Option invalide. Veuillez réessayer.")

    finally:
        if pool:
            pool.close()
            await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())