import asyncio
import aiomysql
from datetime import date

async def create_client(pool, nom, prenom, email, telephone, adresse, categorie, axe):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Client (nom, prenom, email, telephone, adresse, date_ajout, categorie, axe) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (nom, prenom, email, telephone, adresse, date.today(), categorie, axe))
            await conn.commit()
            return cur.lastrowid  # Retourne l'ID du client créé

async def obtenir_categories(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SHOW COLUMNS FROM Client LIKE 'categorie'")
            resultat = await cursor.fetchone()
            if resultat:
                enum_str = resultat[1].split("'")[1::2]
                return enum_str
            else:
                return []


async def read_client(pool, client_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Client WHERE client_id = %s", (client_id,))
            return await cur.fetchone()

async def update_client(pool, client_id, nom, prenom, email, telephone, adresse, categorie, axe):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Client SET nom = %s, prenom = %s, email = %s, telephone = %s, adresse = %s, categorie = %s, axe = %s WHERE client_id = %s", (nom, prenom, email, telephone, adresse, categorie, axe, client_id))
            await conn.commit()

async def delete_client(pool, client_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Client WHERE client_id = %s", (client_id,))
            await conn.commit()

async def create_contrat(pool, client_id, date_contrat, date_debut, date_fin, categorie):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Contrat (client_id, date_contrat, date_debut, date_fin, categorie) VALUES (%s, %s, %s, %s, %s)", (client_id, date_contrat, date_debut, date_fin, categorie))
            await conn.commit()
            return cur.lastrowid

async def read_contrat(pool, contrat_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Contrat WHERE contrat_id = %s", (contrat_id,))
            return await cur.fetchone()

async def update_contrat(pool, contrat_id, client_id, date_contrat, date_debut, date_fin, categorie):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Contrat SET client_id = %s, date_contrat = %s, date_debut = %s, date_fin = %s, categorie = %s WHERE contrat_id = %s", (client_id, date_contrat, date_debut, date_fin, categorie, contrat_id))
            await conn.commit()

async def delete_contrat(pool, contrat_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Contrat WHERE contrat_id = %s", (contrat_id,))
            await conn.commit()

# Pour la table traitement
types_traitement_valides = ["Dératisation", "Désinfection", "Désinsectisation", "Nettoyage"]

async def creation_traitement(pool, contrat_id, id_type_traitement):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Traitement (contrat_id, id_type_traitement) VALUES (%s, %s)", (contrat_id, id_type_traitement))
            await conn.commit()
            return cur.lastrowid


async def read_traitement(pool, traitement_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Traitement WHERE traitement_id = %s", (traitement_id,))
            return await cur.fetchone()

async def update_traitement(pool, traitement_id, contrat_id, type_traitement):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Traitement SET contrat_id = %s, type_traitement = %s WHERE traitement_id = %s", (contrat_id, type_traitement, traitement_id))
            await conn.commit()

async def delete_traitement(pool, traitement_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Traitement WHERE traitement_id = %s", (traitement_id,))
            await conn.commit()

# Pour le planning
async def create_planning(pool, traitement_id, mois_debut, mois_fin, mois_pause, redondance): # type_traitement supprimé
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Planning (traitement_id, mois_debut, mois_fin, mois_pause, redondance) VALUES (%s, %s, %s, %s, %s)", (traitement_id, mois_debut, mois_fin, mois_pause, redondance)) # type_traitement supprimé
            await conn.commit()
            return cur.lastrowid

async def read_planning(pool, planning_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Planning WHERE planning_id = %s", (planning_id,))
            return await cur.fetchone()

async def update_planning(pool, planning_id, traitement_id, mois_debut, mois_fin, type_traitement, mois_pause, redondance):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Planning SET traitement_id = %s, mois_debut = %s, mois_fin = %s, type_traitement = %s, mois_pause = %s, redondance = %s WHERE planning_id = %s", (traitement_id, mois_debut, mois_fin, type_traitement, mois_pause, redondance, planning_id))
            await conn.commit()

async def delete_planning(pool, planning_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Planning WHERE planning_id = %s", (planning_id,))
            await conn.commit()

# Pour la facture
async def create_facture(pool, traitement_id, montant, date_traitement, axe, remarque):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Facture (traitement_id, montant, date_traitement, axe, remarque) VALUES (%s, %s, %s, %s, %s)", (traitement_id, montant, date_traitement, axe, remarque))
            await conn.commit()
            return cur.lastrowid

async def read_facture(pool, facture_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Facture WHERE facture_id = %s", (facture_id,))
            return await cur.fetchone()

async def update_facture(pool, facture_id, traitement_id, montant, date_traitement, axe, remarque):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Facture SET traitement_id = %s, montant = %s, date_traitement = %s, axe = %s, remarque = %s WHERE facture_id = %s", (traitement_id, montant, date_traitement, axe, remarque, facture_id))
            await conn.commit()

async def delete_facture(pool, facture_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Facture WHERE facture_id = %s", (facture_id,))
            await conn.commit()

# Pour Historique
async def create_historique(pool, facture_id, contenu):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Historique (facture_id, contenu) VALUES (%s, %s)", (facture_id, contenu))
            await conn.commit()
            return cur.lastrowid

async def read_historique(pool, historique_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Historique WHERE historique_id = %s", (historique_id,))
            return await cur.fetchone()

async def update_historique(pool, historique_id, facture_id, contenu):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Historique SET facture_id = %s, contenu = %s WHERE historique_id = %s", (facture_id, contenu, historique_id))
            await conn.commit()

async def delete_historique(pool, historique_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Historique WHERE historique_id = %s", (historique_id,))
            await conn.commit()

# Pour avancement
async def create_avancement(pool, traitement_id, motif, type_avancement):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO Avancement (traitement_id, motif, type) VALUES (%s, %s, %s)", (traitement_id, motif, type_avancement))
            await conn.commit()
            return cur.lastrowid

async def read_avancement(pool, avancement_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Avancement WHERE avancement_id = %s", (avancement_id,))
            return await cur.fetchone()

async def update_avancement(pool, avancement_id, traitement_id, motif, type_avancement):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE Avancement SET traitement_id = %s, motif = %s, type = %s WHERE avancement_id = %s", (traitement_id, motif, type_avancement, avancement_id))
            await conn.commit()

async def delete_avancement(pool, avancement_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM Avancement WHERE avancement_id = %s", (avancement_id,))
            await conn.commit()


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
        categories = await obtenir_categories(pool)
    finally:
        if pool:
            pool.close()
            await pool.wait_closed()

    # Test
    while True:
        print("\nMenu:")
        print("1. Client")
        print("2. Contrat")
        print("3. Traitement")
        print("4. Planning")
        print("5. Facture")
        print("6. Historique")
        print("7. Avancement")
        print("8. Quitter")


        choix_table = input("Choisissez une table (1-8) : ")

        if choix_table == '8':
            break

        table_functions = {
            '1': {'create': create_client, 'read': read_client, 'update': update_client, 'delete': delete_client,
                  'name': "Client"},
            '2': {'create': create_contrat, 'read': read_contrat, 'update': update_contrat, 'delete': delete_contrat,
                  'name': "Contrat"},
            '3': {'create': creation_traitement, 'read': read_traitement, 'update': update_traitement,
                  'delete': delete_traitement, 'name': "Traitement"},
            '4': {'create': create_planning, 'read': read_planning, 'update': update_planning,
                  'delete': delete_planning, 'name': "Planning"},
            '5': {'create': create_facture, 'read': read_facture, 'update': update_facture, 'delete': delete_facture,
                  'name': "Facture"},
            '6': {'create': create_historique, 'read': read_historique, 'update': update_historique,
                  'delete': delete_historique, 'name': "Historique"},
            '7': {'create': create_avancement, 'read': read_avancement, 'update': update_avancement,
                  'delete': delete_avancement, 'name': "Avancement"},
        }

        if choix_table not in table_functions:
            print("Choix de table invalide.")
            continue

        table_name = table_functions[choix_table]['name']
        while True:
            print(f"\nOpérations pour {table_name}:")
            print("1. Créer")
            print("2. Lire")
            print("3. Modifier")
            print("4. Supprimer")
            print("5. Retour au menu principal")

            choix_operation = input("Choisissez une opération (1-5) : ")

            if choix_operation == '5':
                break

            if choix_operation not in ('1', '2', '3', '4'):
                print("Choix d'opération invalide.")
                continue

            operation = ['create', 'read', 'update', 'delete'][int(choix_operation) - 1]
            func = table_functions[choix_table][operation]

            try:
                if operation == 'create':
                    if table_name == "Client":
                        nom = input("Nom : ")
                        prenom = input("Prénom (facultatif) : ")
                        email = input("Email : ")
                        telephone = input("Téléphone : ")
                        adresse = input("Adresse : ")
                        if categories:
                            print("Catégories disponibles:")
                            for i, categorie in enumerate(categories):
                                print(f"{i + 1}. {categorie}")

                            choix = int(input("Choisissez une catégorie (entrez le numéro): ")) - 1
                            categorie_choisie = categories[choix]
                        else:
                            print("Aucune catégorie trouvée.")
                            categorie_choisie = input("Entrez la catégorie manuellement : ")
                        axe = input("Axe : ")
                        result = await func(pool, nom, prenom, email, telephone, adresse, categorie_choisie, axe)

                    elif table_name == "Contrat":
                        client_id = int(input("ID du client : "))  # Assurez-vous que le client existe
                        date_contrat = input("Date du contrat (AAAA-MM-JJ) : ")
                        date_debut = input("Date de début (AAAA-MM-JJ) : ")
                        date_fin = input("Date de fin (AAAA-MM-JJ) : ")
                        categorie = input("Catégorie (Nouveau/Renouvellement) : ")
                        result = await func(pool, client_id, date_contrat, date_debut, date_fin, categorie)

                    elif table_name == "Traitement":
                        contrat_id = int(input("ID du contrat : "))
                        type_traitement = input("Type de traitement : ")
                        result = await func(pool, contrat_id, type_traitement)

                    elif table_name == "Planning":
                        traitement_id = int(input("ID du traitement : "))
                        mois_debut = input("Mois de début : ")
                        mois_fin = input("Mois de fin : ")
                        type_traitement = input("Type de traitement : ")
                        mois_pause = input("Mois de pause (facultatif) : ")
                        redondance = input("Redondance (Mensuel/Hebdo) : ")
                        result = await func(pool, traitement_id, mois_debut, mois_fin, type_traitement, mois_pause,
                                            redondance)

                    elif table_name == "Facture":
                        traitement_id = int(input("ID du traitement : "))
                        montant = int(input("Montant : "))
                        date_traitement = input("Date du traitement (AAAA-MM-JJ) : ")
                        axe = input("Axe : ")
                        remarque = input("Remarque (facultatif) : ")
                        result = await func(pool, traitement_id, montant, date_traitement, axe, remarque)

                    elif table_name == "Historique":
                        facture_id = int(input("ID de la facture : "))
                        contenu = input("Contenu : ")
                        result = await func(pool, facture_id, contenu)

                    print(f"{table_name} créé avec l'ID : {result}")

                elif operation == 'read':
                    id_a_lire = int(input(f"ID du {table_name} à lire : "))
                    result = await func(pool, id_a_lire)
                    print(result)

                elif operation == 'update':
                    id_a_modifier = int(input(f"ID du {table_name} à modifier : "))
                    if table_name == "Client":
                        nom = input("Nouveau nom : ")
                        prenom = input("Nouveau prénom (facultatif) : ")
                        email = input("Nouvel email : ")
                        telephone = input("Nouveau téléphone : ")
                        adresse = input("Nouvelle adresse : ")
                        categorie = input("Nouvelle catégorie (Particulier/Organisation/Société) : ")
                        axe = input("Nouvel axe : ")
                        await func(pool, id_a_modifier, nom, prenom, email, telephone, adresse, categorie, axe)

                    elif table_name == "Contrat":
                        client_id = int(input("Nouvel ID du client : "))
                        date_contrat = input("Nouvelle date du contrat (AAAA-MM-JJ) : ")
                        date_debut = input("Nouvelle date de début (AAAA-MM-JJ) : ")
                        date_fin = input("Nouvelle date de fin (AAAA-MM-JJ) : ")
                        categorie = input("Nouvelle catégorie (Nouveau/Renouvellement) : ")
                        await func(pool, id_a_modifier, client_id, date_contrat, date_debut, date_fin, categorie)

                    elif table_name == "Traitement":
                        contrat_id = int(input("Nouveau ID du contrat : "))
                        type_traitement = input("Nouveau type de traitement : ")
                        await func(pool, id_a_modifier, contrat_id, type_traitement)

                    elif table_name == "Planning":
                        traitement_id = int(input("Nouveau ID du traitement : "))
                        mois_debut = input("Nouveau mois de début : ")
                        mois_fin = input("Nouveau mois de fin : ")
                        mois_pause = input("Nouveau mois de pause (facultatif) : ")
                        redondance = input("Nouvelle redondance (Mensuel/Hebdo) : ")
                        await func(pool, id_a_modifier, traitement_id, mois_debut, mois_fin,
                                   mois_pause, redondance)
                    elif table_name == "Facture":
                            traitement_id = int(input("Nouveau ID du traitement : "))
                            # Vérifier si le traitement existe
                            if not await read_traitement(pool, traitement_id):
                                print("Traitement inexistant.")
                                continue
                            montant = int(input("Nouveau montant : "))
                            date_traitement = input("Nouvelle date du traitement (AAAA-MM-JJ) : ")
                            axe = input("Nouvel axe : ")
                            remarque = input("Nouvelle remarque (facultatif) : ")
                            await func(pool, id_a_modifier, traitement_id, montant, date_traitement, axe, remarque)
                    elif choix_table == '8':  # Si l'utilisateur choisit "Avancement"
                          while True:
                              print(f"\nOpérations pour Avancement:")
                              print("1. Créer")
                              print("2. Lire")
                              print("3. Modifier")
                              print("4. Supprimer")
                              print("5. Retour au menu principal")
                              choix_operation = input("Choisissez une opération (1-5) : ")

                          if choix_operation == '5':
                              break

                          if choix_operation not in ('1', '2', '3', '4'):
                              print("Choix d'opération invalide.")
                              continue
                              operation = ['create', 'read', 'update', 'delete'][int(choix_operation) - 1]
                              func = table_functions[choix_table][operation]
                              try:
                                  if operation == 'create':
                                      traitement_id = int(input("ID du traitement pour l'avancement : "))
                                      motif = input("Motif de l'avancement : ")
                                      type_avancement = input("Type d'avancement (Avancement/Décalage) : ")
                                      result = await func(pool, traitement_id, motif, type_avancement)
                                      print(f"Avancement créé avec l'ID : {result}")
                              except Exception as e:
                                  print(f"Erreur : {e}")

            except aiomysql.OperationalError as e:
                print(f"Erreur de connexion à la base de données : {e}")
            except aiomysql.IntegrityError as e:
                print(f"Violation de contrainte d'intégrité : {e}")
            except ValueError as e:
                print(f"Erreur de valeur : {e}")
            except Exception as e:
                print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    asyncio.run(main())