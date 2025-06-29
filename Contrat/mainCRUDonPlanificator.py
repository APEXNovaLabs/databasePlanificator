import asyncio
from datetime import datetime

import aiomysql
from Contrat.CRUDonClient import create_client, read_client, update_client, delete_client, obtenir_categories
from Contrat.CRUDonContrat import create_contrat, read_contrat, update_contrat, delete_contrat, obtenir_duree_contrat, obtenir_axe_contrat
from Contrat.CRUDonTraitement import creation_traitement, obtenir_types_traitement, read_traitement, update_traitement, delete_traitement
from Contrat.CRUDonPlanning import create_planning, obtenir_redondances, read_planning, update_planning, delete_planning
from Contrat.CRUDonFacture import create_facture, read_facture, delete_facture, update_facture
from Contrat.CRUDonSignalement import create_signalement, read_signalement, update_signalement, delete_signalement

async def main():
    pool = None  # Initialize pool to None
    try:
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

        # Créer le pool de connexions
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=True
        )

        categories_client = await obtenir_categories(pool, "Client", "categorie")
        categories_contrat_duree = await obtenir_categories(pool, "Contrat", "duree")
        categories_contrat_type = await obtenir_categories(pool, "Contrat", "categorie")
        types_traitement_data = await obtenir_types_traitement(pool)
        types_traitement_names = [t['typeTraitement'] for t in types_traitement_data]
        types_traitement_map = {t['typeTraitement']: t['id_type_traitement'] for t in types_traitement_data}

        redondances = await obtenir_redondances(pool)  # Assuming this returns a list of strings

        # Test Loop
        while True:
            print("\n--- Menu Principal ---")
            print("1. Gérer les Clients")
            print("2. Gérer les Contrats")
            print("3. Gérer les Traitements")
            print("4. Gérer les Plannings")
            print("5. Gérer les Factures")
            print("6. Gérer les Signalements")
            print("7. Quitter")

            choix_table = input("Choisissez une table (1-7) : ").strip()

            if choix_table == '7':
                print("Exiting...")
                break

            table_functions = {
                '1': {'create': create_client, 'read': read_client, 'update': update_client, 'delete': delete_client,
                      'name': "Client"},
                '2': {'create': create_contrat, 'read': read_contrat, 'update': update_contrat,
                      'delete': delete_contrat, 'name': "Contrat"},
                '3': {'create': creation_traitement, 'read': read_traitement, 'update': update_traitement,
                      'delete': delete_traitement, 'name': "Traitement"},
                '4': {'create': create_planning, 'read': read_planning, 'update': update_planning,
                      'delete': delete_planning, 'name': "Planning"},
                '5': {'create': create_facture, 'read': read_facture, 'update': update_facture,
                      'delete': delete_facture, 'name': "Facture"},
                '6': {'create': create_signalement, 'read': read_signalement, 'update': update_signalement,
                      'delete': delete_signalement, 'name': "Signalement"},
            }

            if choix_table not in table_functions:
                print("Choix de table invalide.")
                continue

            table_name = table_functions[choix_table]['name']

            while True:
                print(f"\n--- Opérations pour {table_name} ---")
                print("1. Créer")
                print("2. Lire")
                print("3. Modifier")
                print("4. Supprimer")
                print("5. Retour au menu principal")

                choix_operation = input("Choisissez une opération (1-5) : ").strip()
                if choix_operation == '5':
                    break
                if choix_operation not in ('1', '2', '3', '4'):
                    print("Choix d'opération invalide.")
                    continue

                operation_key = ['create', 'read', 'update', 'delete'][int(choix_operation) - 1]
                func = table_functions[choix_table][operation_key]

                try:
                    # --- CREATE Operations ---
                    if operation_key == 'create':
                        if table_name == "Client":
                            nom = input("Nom : ").strip()
                            prenom = None
                            nif = None
                            stat = None
                            axe = input("Axe : ").strip()
                            categorie_choisie = None

                            if categories_client:
                                print("Catégories disponibles:")
                                for i, cat in enumerate(categories_client):
                                    print(f"{i + 1}. {cat}")
                                while True:
                                    try:
                                        choix = int(input("Choisissez une catégorie (entrez le numéro): ").strip()) - 1
                                        if 0 <= choix < len(categories_client):
                                            categorie_choisie = categories_client[choix]
                                            break
                                        else:
                                            print("Choix invalide. Veuillez réessayer.")
                                    except ValueError:
                                        print("Entrée invalide. Veuillez entrer un numéro.")
                            else:
                                print("Aucune catégorie trouvée. Entrez-la manuellement.")
                                while True:
                                    categorie_choisie = input("Entrez la catégorie manuellement : ").strip()
                                    if categorie_choisie:  # Si la saisie n'est pas vide, sortir de la boucle
                                        break
                                    else:
                                        print("La catégorie ne peut pas être vide. Veuillez la saisir.")

                            if categorie_choisie == "Particulier":
                                prenom = input("Prénom (facultatif) : ").strip() or None
                            elif categorie_choisie == "Société":
                                prenom = input("Responsable : ").strip() or None  # Responsible for the company
                                nif = input("NIF (Numéro d'Immatriculation Fiscale): ").strip() or None
                                stat = input("Stat: ").strip() or None
                            else:  # For 'Organisation' or other categories
                                prenom = input("Responsable : ").strip() or None  # Responsible for the organization

                            email = input("Email : ").strip()
                            telephone = input("Téléphone : ").strip()
                            adresse = input("Adresse : ").strip()

                            result_id = await func(pool, nom, prenom, email, telephone, adresse, categorie_choisie, nif,
                                                   stat, axe)
                            print(f"{table_name} créé avec l'ID : {result_id}")
                        elif table_name == "Contrat":
                            client_id = int(input("ID du client : ").strip())
                            date_contrat_str = input("Date du contrat (AAAA-MM-JJ) : ").strip()
                            date_contrat = datetime.strptime(date_contrat_str, '%Y-%m-%d').date()
                            date_debut_str = input("Date de début (AAAA-MM-JJ) : ").strip()
                            date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()

                            duree_contrat_choisie = None
                            if categories_contrat_duree:
                                print("Catégories de durée disponibles:")
                                for i, cat in enumerate(categories_contrat_duree):
                                    print(f"{i + 1}. {cat}")
                                while True:
                                    try:
                                        choix = int(
                                            input("Choisissez une catégorie de durée (entrez le numéro): ").strip()) - 1
                                        if 0 <= choix < len(categories_contrat_duree):
                                            duree_contrat_choisie = categories_contrat_duree[choix]
                                            break
                                        else:
                                            print("Choix invalide. Veuillez réessayer.")
                                    except ValueError:
                                        print("Entrée invalide. Veuillez entrer un numéro.")
                            else:
                                print("Aucune catégorie de durée trouvée. Entrez-la manuellement.")
                                duree_contrat_choisie = input("Entrez la catégorie de durée manuellement : ").strip()

                            date_fin_contrat = None
                            duree_contrat_mois = None  # This is the integer duration, not the category string
                            if duree_contrat_choisie == "Déterminée":
                                date_fin_contrat_str = input("Date de fin (AAAA-MM-JJ) : ").strip()
                                date_fin_contrat = datetime.strptime(date_fin_contrat_str, '%Y-%m-%d').date()
                                duree_contrat_mois = int(input("Durée du contrat en mois : ").strip())
                            # For "Indéterminée", date_fin_contrat remains None and duree_contrat_mois remains None

                            categorie_contrat_choisie = None
                            if categories_contrat_type:
                                print("Catégories de type disponibles:")
                                for i, cat in enumerate(categories_contrat_type):
                                    print(f"{i + 1}. {cat}")
                                while True:
                                    try:
                                        choix = int(
                                            input("Choisissez une catégorie de type (entrez le numéro): ").strip()) - 1
                                        if 0 <= choix < len(categories_contrat_type):
                                            categorie_contrat_choisie = categories_contrat_type[choix]
                                            break
                                        else:
                                            print("Choix invalide. Veuillez réessayer.")
                                    except ValueError:
                                        print("Entrée invalide. Veuillez entrer un numéro.")
                            else:
                                print("Aucune catégorie de type trouvée. Entrez-la manuellement.")
                                categorie_contrat_choisie = input("Entrez la catégorie de type manuellement : ").strip()

                            result_id = await func(pool, client_id, date_contrat, date_debut, date_fin_contrat,
                                                   duree_contrat_choisie, categorie_contrat_choisie, duree_contrat_mois)
                            print(f"{table_name} créé avec l'ID : {result_id}")

                        elif table_name == "Traitement":
                            contrat_id = int(input("ID du contrat : ").strip())

                            if not types_traitement_names:
                                print("Aucun type de traitement trouvé. Impossible de créer un traitement.")
                                continue

                            print("Types de traitement disponibles:")
                            for i, tt_name in enumerate(types_traitement_names):
                                print(f"{i + 1}. {tt_name}")

                            types_traitement_choisis_ids = []
                            while True:
                                choix_str = input(
                                    "Choisissez les types de traitement (numéros séparés par des virgules, ou Entrée pour terminer) : ").strip()
                                if not choix_str:
                                    break

                                try:
                                    choix_list = [int(c.strip()) - 1 for c in choix_str.split(',') if c.strip()]

                                    valid_choices = True
                                    for c_idx in choix_list:
                                        if 0 <= c_idx < len(types_traitement_names):
                                            selected_type_name = types_traitement_names[c_idx]
                                            types_traitement_choisis_ids.append(
                                                types_traitement_map[selected_type_name])
                                        else:
                                            print(f"Choix invalide : {c_idx + 1}. Veuillez réessayer.")
                                            valid_choices = False
                                            types_traitement_choisis_ids = []  # Clear invalid choices
                                            break
                                    if valid_choices:
                                        break
                                except ValueError:
                                    print("Entrée invalide. Veuillez entrer des numéros séparés par des virgules.")

                            if not types_traitement_choisis_ids:
                                print(
                                    "Aucun type de traitement valide sélectionné. Annulation de la création du traitement.")
                                continue

                            for id_type_traitement_chosen in types_traitement_choisis_ids:
                                result_id = await func(pool, contrat_id, id_type_traitement_chosen)
                                print(
                                    f"Traitement créé avec l'ID : {result_id} pour le type de traitement ID {id_type_traitement_chosen}")


                        elif table_name == "Planning":
                            contrat_id = int(
                                input("Entrez l'ID du contrat pour lequel planifier les traitements: ").strip())

                            # Fetch treatments associated with the contract
                            async with pool.acquire() as conn:
                                async with conn.cursor(
                                        aiomysql.DictCursor) as cursor:  # Use DictCursor for easier access by column name
                                    await cursor.execute(
                                        "SELECT traitement_id, id_type_traitement FROM Traitement WHERE contrat_id = %s",
                                        (contrat_id,))
                                    traitements = await cursor.fetchall()

                            if not traitements:
                                print(
                                    "Aucun traitement trouvé pour ce contrat. Veuillez d'abord créer des traitements.")
                                continue

                            for traitement_info in traitements:
                                traitement_id = traitement_info['traitement_id']
                                id_type_traitement = traitement_info['id_type_traitement']

                                # Get type treatment name for display
                                type_traitement_name = next((name for name, id_val in types_traitement_map.items() if
                                                             id_val == id_type_traitement), "Inconnu")

                                # Get contract duration
                                duree_contrat = await obtenir_duree_contrat(pool,
                                                                            contrat_id)  # This should return "Déterminée" or "Indéterminée"

                                print(
                                    f"\nPlanification pour le traitement '{type_traitement_name}' (ID: {traitement_id}):")
                                print(f"Durée du contrat : {duree_contrat}")

                                mois_debut = input("Mois de début (ex: 01 pour Janvier, 12 pour Décembre) : ").strip()
                                # Basic validation for mois_debut (you might want more robust validation)
                                if not (mois_debut.isdigit() and 1 <= int(mois_debut) <= 12):
                                    print("Mois de début invalide. Veuillez entrer un nombre entre 1 et 12.")
                                    continue  # Skip to next treatment or break

                                mois_fin = None
                                if duree_contrat == "Déterminée":
                                    mois_fin = input("Mois de fin (ex: 01 pour Janvier, 12 pour Décembre) : ").strip()
                                    if not (mois_fin.isdigit() and 1 <= int(mois_fin) <= 12):
                                        print("Mois de fin invalide. Veuillez entrer un nombre entre 1 et 12.")
                                        continue  # Skip to next treatment or break
                                else:  # Indeterminée
                                    print("Mois de fin : Contrat à durée indéterminée (N/A)")

                                mois_pause = input(
                                    "Mois de pause (facultatif, ex: 07,08 pour Juillet, Août. Laissez vide si aucun) : ").strip() or None

                                redondance_choisie = None
                                if redondances:
                                    print("Options de redondance disponibles:")
                                    for i, red in enumerate(redondances):
                                        print(f"{i + 1}. {red}")
                                    while True:
                                        try:
                                            choix_red = int(input(
                                                "Choisissez une option de redondance (entrez le numéro): ").strip()) - 1
                                            if 0 <= choix_red < len(redondances):
                                                redondance_choisie = redondances[choix_red]
                                                break
                                            else:
                                                print("Choix invalide. Veuillez réessayer.")
                                        except ValueError:
                                            print("Entrée invalide. Veuillez entrer un numéro.")
                                else:
                                    print("Aucune option de redondance trouvée. Entrez-la manuellement.")
                                    redondance_choisie = input(
                                        "Entrez l'option de redondance manuellement (ex: Mensuel, Hebdomadaire) : ").strip()

                                result_id = await func(pool, traitement_id, mois_debut, mois_fin, mois_pause,
                                                       redondance_choisie)
                                print(f"Planning créé avec l'ID : {result_id} pour le traitement ID {traitement_id}")

                        elif table_name == "Facture":
                            contrat_id = int(input("ID du contrat pour lequel facturer les traitements : ").strip())

                            # Récupérer les traitements associés au contrat
                            async with pool.acquire() as conn:
                                async with conn.cursor(aiomysql.DictCursor) as cursor:
                                    await cursor.execute(
                                        "SELECT t.traitement_id, t.id_type_traitement, co.contrat_id "
                                        "FROM Traitement t JOIN Contrat co ON t.contrat_id = co.contrat_id "
                                        "WHERE co.contrat_id = %s", (contrat_id,))
                                    traitements = await cursor.fetchall()

                            if not traitements:
                                print("Aucun traitement trouvé pour ce contrat. Impossible de créer des factures.")
                                continue

                            # Récupérer l'axe du contrat
                            axe_contrat = await obtenir_axe_contrat(pool,
                                                                    contrat_id)  # Make sure this function exists and works

                            for traitement_info in traitements:
                                traitement_id = traitement_info['traitement_id']
                                id_type_traitement = traitement_info['id_type_traitement']

                                # Get type treatment name for display
                                type_traitement_name = next((name for name, id_val in types_traitement_map.items() if
                                                             id_val == id_type_traitement), "Inconnu")

                                print(f"\nFacture pour le traitement '{type_traitement_name}' (ID: {traitement_id}):")
                                montant = float(input("Montant : ").strip())  # Montant can be float
                                date_traitement_str = input("Date du traitement (AAAA-MM-JJ) : ").strip()
                                date_traitement = datetime.strptime(date_traitement_str, '%Y-%m-%d').date()
                                remarque = input("Remarque (facultatif) : ").strip() or None

                                # Assuming create_facture needs planning_detail_id.
                                # The original code implies linking to `traitement_id` directly, which might be incorrect
                                # if Facture links to PlanningDetails.
                                # For now, I'll pass traitement_id and axe_contrat, assuming `create_facture` handles it.
                                # If `create_facture` requires `planning_detail_id`, you'll need to fetch it here.
                                result_id = await func(pool, traitement_id, montant, date_traitement, axe_contrat,
                                                       remarque)
                                print(f"Facture créée avec l'ID : {result_id} pour le traitement ID {traitement_id}")

                        elif table_name == "Signalement":
                            traitement_id = int(input("ID du traitement pour le signalement : ").strip())

                            # Récupérer les planning_detail_id associés au traitement
                            planning_details = []
                            async with pool.acquire() as conn:
                                async with conn.cursor(aiomysql.DictCursor) as cursor:
                                    await cursor.execute(
                                        "SELECT planning_detail_id, date_planification FROM PlanningDetails WHERE planning_id IN (SELECT planning_id FROM Planning WHERE traitement_id = %s)",
                                        (traitement_id,))
                                    planning_details = await cursor.fetchall()

                            if not planning_details:
                                print("Aucun planning trouvé pour ce traitement. Impossible de créer un signalement.")
                                continue

                            print("Planning disponibles :")
                            for i, pd in enumerate(planning_details):
                                print(
                                    f"{i + 1}. Planning ID : {pd['planning_detail_id']} (Date: {pd['date_planification']})")

                            planning_detail_id = None
                            while True:
                                try:
                                    choix_planning = int(
                                        input("Choisissez un planning (entrez le numéro) : ").strip()) - 1
                                    if 0 <= choix_planning < len(planning_details):
                                        planning_detail_id = planning_details[choix_planning]['planning_detail_id']
                                        break
                                    else:
                                        print("Choix invalide. Veuillez réessayer.")
                                except ValueError:
                                    print("Entrée invalide. Veuillez entrer un numéro.")

                            if planning_detail_id is None:
                                print("Sélection de planning annulée.")
                                continue

                            motif = input("Motif du signalement : ").strip()
                            type_signalement = input("Type de signalement (Avancement/Décalage) : ").strip()

                            result_id = await create_signalement(pool, planning_detail_id, motif, type_signalement)
                            print(f"Signalement créé avec l'ID : {result_id}")


                    # --- READ Operations ---
                    elif operation_key == 'read':
                        if table_name == "Client":
                            print("\n--- Options de lecture pour Client ---")
                            print("1. Lire un client par ID")
                            print("2. Lire tous les clients")
                            read_option = input("Choisissez une option (1-2) : ").strip()

                            if read_option == '1':
                                client_id_to_read = int(input("ID du client à lire : ").strip())
                                # Appel à read_client avec un ID spécifique
                                result = await func(pool, client_id_to_read)  # func est read_client
                                if result:
                                    print("\n--- Détails du Client ---")
                                    # result est un dictionnaire pour un client unique
                                    for key, value in result.items():
                                        print(f"{key}: {value}")
                                else:
                                    print(f"Aucun client trouvé avec l'ID {client_id_to_read}.")
                            elif read_option == '2':
                                # Appel à read_client sans ID pour obtenir tous les clients
                                all_clients = await func(pool, None)  # func est read_client
                                if all_clients:
                                    print("\n--- Tous les Clients ---")
                                    for client in all_clients:
                                        print("-" * 20)  # Séparateur pour chaque client
                                        for key, value in client.items():
                                            print(f"{key}: {value}")
                                    print("-" * 20)
                                else:
                                    print("Aucun client trouvé dans la base de données.")
                            else:
                                print("Option de lecture invalide.")
                        else:
                            # Logique existante pour les autres tables (lecture par ID seulement)
                            id_a_lire = int(input(f"ID du {table_name} à lire : ").strip())
                            result = await func(pool, id_a_lire)
                            if result:
                                print("\n--- Détails ---")
                                if isinstance(result, dict):
                                    for key, value in result.items():
                                        print(f"{key}: {value}")
                                else:
                                    print(result)
                            else:
                                print(f"Aucun {table_name} trouvé avec l'ID {id_a_lire}.")

                    # --- UPDATE Operations ---
                    elif operation_key == 'update':
                        id_a_modifier = int(input(f"ID du {table_name} à modifier : ").strip())
                        # First, read the existing record to pre-fill prompts
                        existing_record = await read_client(pool, id_a_modifier) if table_name == "Client" else \
                            await read_contrat(pool, id_a_modifier) if table_name == "Contrat" else \
                                await read_traitement(pool, id_a_modifier) if table_name == "Traitement" else \
                                    await read_planning(pool, id_a_modifier) if table_name == "Planning" else \
                                        await read_facture(pool, id_a_modifier) if table_name == "Facture" else \
                                            await read_signalement(pool, id_a_modifier)  # Add other read functions

                        if not existing_record:
                            print(f"Aucun {table_name} trouvé avec l'ID {id_a_modifier}.")
                            continue

                        if table_name == "Client":
                            nom = input(
                                f"Nouveau nom ({existing_record.get('nom', 'N/A')}) : ").strip() or existing_record.get(
                                'nom')

                            categorie_choisie = existing_record.get('categorie')
                            if categories_client:
                                print("Catégories disponibles:")
                                for i, cat in enumerate(categories_client):
                                    print(f"{i + 1}. {cat}")
                                current_cat_idx = categories_client.index(
                                    categorie_choisie) if categorie_choisie in categories_client else -1
                                while True:
                                    choix_str = input(
                                        f"Choisissez une catégorie ({categorie_choisie}, entrez le numéro ou Entrée pour garder l'actuelle): ").strip()
                                    if not choix_str:
                                        break  # Keep existing
                                    try:
                                        choix = int(choix_str) - 1
                                        if 0 <= choix < len(categories_client):
                                            categorie_choisie = categories_client[choix]
                                            break
                                        else:
                                            print("Choix invalide. Veuillez réessayer.")
                                    except ValueError:
                                        print("Entrée invalide. Veuillez entrer un numéro.")
                            else:
                                print("Aucune catégorie trouvée.")
                                categorie_choisie = input(
                                    f"Nouvelle catégorie ({categorie_choisie}) : ").strip() or categorie_choisie

                            prenom = existing_record.get('prenom')
                            nif = existing_record.get('nif')
                            stat = existing_record.get('stat')

                            if categorie_choisie == "Particulier":
                                prenom = input(f"Nouveau prénom ({prenom if prenom else 'N/A'}) : ").strip() or prenom
                                nif = None  # Clear NIF/STAT for particuliers if they were set
                                stat = None
                            elif categorie_choisie == "Société":
                                prenom = input(
                                    f"Nouveau responsable ({prenom if prenom else 'N/A'}) : ").strip() or prenom
                                nif = input(f"Nouveau NIF ({nif if nif else 'N/A'}) : ").strip() or nif
                                stat = input(f"Nouveau Stat ({stat if stat else 'N/A'}) : ").strip() or stat
                            else:  # Organisation or others
                                prenom = input(
                                    f"Nouveau responsable ({prenom if prenom else 'N/A'}) : ").strip() or prenom
                                nif = None
                                stat = None

                            email = input(
                                f"Nouvel email ({existing_record.get('email', 'N/A')}) : ").strip() or existing_record.get(
                                'email')
                            telephone = input(
                                f"Nouveau téléphone ({existing_record.get('telephone', 'N/A')}) : ").strip() or existing_record.get(
                                'telephone')
                            adresse = input(
                                f"Nouvelle adresse ({existing_record.get('adresse', 'N/A')}) : ").strip() or existing_record.get(
                                'adresse')
                            axe = input(
                                f"Nouvel axe ({existing_record.get('axe', 'N/A')}) : ").strip() or existing_record.get(
                                'axe')

                            await func(pool, id_a_modifier, nom, prenom, email, telephone, adresse, categorie_choisie,
                                       nif, stat, axe)
                            print(f"{table_name} mis à jour avec succès.")

                        elif table_name == "Contrat":
                            client_id = int(input(
                                f"Nouvel ID du client ({existing_record.get('client_id', 'N/A')}) : ").strip() or existing_record.get(
                                'client_id'))
                            date_contrat_str = input(
                                f"Nouvelle date du contrat (AAAA-MM-JJ) ({existing_record.get('date_contrat', 'N/A')}) : ").strip() or str(
                                existing_record.get('date_contrat'))
                            date_contrat = datetime.strptime(date_contrat_str, '%Y-%m-%d').date()

                            date_debut_str = input(
                                f"Nouvelle date de début (AAAA-MM-JJ) ({existing_record.get('date_debut', 'N/A')}) : ").strip() or str(
                                existing_record.get('date_debut'))
                            date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()

                            duree_contrat_choisie = existing_record.get('duree')  # This is the category string
                            if categories_contrat_duree:
                                print("Catégories de durée disponibles:")
                                for i, cat in enumerate(categories_contrat_duree):
                                    print(f"{i + 1}. {cat}")
                                while True:
                                    choix_str = input(
                                        f"Choisissez une catégorie de durée ({duree_contrat_choisie}, entrez le numéro ou Entrée pour garder l'actuelle): ").strip()
                                    if not choix_str:
                                        break
                                    try:
                                        choix = int(choix_str) - 1
                                        if 0 <= choix < len(categories_contrat_duree):
                                            duree_contrat_choisie = categories_contrat_duree[choix]
                                            break
                                        else:
                                            print("Choix invalide. Veuillez réessayer.")
                                    except ValueError:
                                        print("Entrée invalide. Veuillez entrer un numéro.")
                            else:
                                print("Aucune catégorie de durée trouvée.")
                                duree_contrat_choisie = input(
                                    f"Nouvelle catégorie de durée ({duree_contrat_choisie}) : ").strip() or duree_contrat_choisie

                            date_fin = existing_record.get('date_fin')
                            duree_contrat_mois = existing_record.get(
                                'duree_en_mois')  # Assuming your DB stores this or it's implied

                            if duree_contrat_choisie == "Déterminée":
                                date_fin_str = input(
                                    f"Nouvelle date de fin (AAAA-MM-JJ) ({date_fin if date_fin else 'N/A'}) : ").strip() or str(
                                    date_fin) if date_fin else None
                                date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date() if date_fin_str else None
                                duree_contrat_mois = int(input(
                                    f"Nouvelle durée du contrat en mois ({duree_contrat_mois if duree_contrat_mois else 'N/A'}) : ").strip() or duree_contrat_mois)
                            else:  # Indeterminée
                                date_fin = None
                                duree_contrat_mois = None

                            categorie_contrat_choisie = existing_record.get('categorie_contrat')  # Assuming column name
                            if categories_contrat_type:
                                print("Catégories de type disponibles:")
                                for i, cat in enumerate(categories_contrat_type):
                                    print(f"{i + 1}. {cat}")
                                while True:
                                    choix_str = input(
                                        f"Choisissez une catégorie de type ({categorie_contrat_choisie}, entrez le numéro ou Entrée pour garder l'actuelle): ").strip()
                                    if not choix_str:
                                        break
                                    try:
                                        choix = int(choix_str) - 1
                                        if 0 <= choix < len(categories_contrat_type):
                                            categorie_contrat_choisie = categories_contrat_type[choix]
                                            break
                                        else:
                                            print("Choix invalide. Veuillez réessayer.")
                                    except ValueError:
                                        print("Entrée invalide. Veuillez entrer un numéro.")
                            else:
                                print("Aucune catégorie de type trouvée.")
                                categorie_contrat_choisie = input(
                                    f"Nouvelle catégorie de type ({categorie_contrat_choisie}) : ").strip() or categorie_contrat_choisie

                            await func(pool, id_a_modifier, client_id, date_contrat, date_debut, date_fin,
                                       duree_contrat_choisie, categorie_contrat_choisie, duree_contrat_mois)
                            print(f"{table_name} mis à jour avec succès.")

                        elif table_name == "Traitement":
                            contrat_id = int(input(
                                f"Nouveau ID du contrat ({existing_record.get('contrat_id', 'N/A')}) : ").strip() or existing_record.get(
                                'contrat_id'))

                            type_traitement_id = existing_record.get('id_type_traitement')
                            type_traitement_name = next(
                                (name for name, id_val in types_traitement_map.items() if id_val == type_traitement_id),
                                "Inconnu")

                            if types_traitement_names:
                                print("Types de traitement disponibles:")
                                for i, tt_name in enumerate(types_traitement_names):
                                    print(f"{i + 1}. {tt_name}")
                                while True:
                                    choix_str = input(
                                        f"Nouveau type de traitement ({type_traitement_name}, entrez le numéro ou Entrée pour garder l'actuel): ").strip()
                                    if not choix_str:
                                        break
                                    try:
                                        choix = int(choix_str) - 1
                                        if 0 <= choix < len(types_traitement_names):
                                            type_traitement_id = types_traitement_map[types_traitement_names[choix]]
                                            break
                                        else:
                                            print("Choix invalide. Veuillez réessayer.")
                                    except ValueError:
                                        print("Entrée invalide. Veuillez entrer un numéro.")
                            else:
                                print("Aucun type de traitement trouvé.")
                                # If no types found, perhaps prompt for a raw ID? Depends on how update_traitement handles it.
                                # For now, assume it might fail if type_traitement_id is not found in types_traitement_map.
                                type_traitement_id = int(input(
                                    f"Nouveau ID du type de traitement ({type_traitement_id}) : ").strip() or type_traitement_id)

                            await func(pool, id_a_modifier, contrat_id, type_traitement_id)
                            print(f"{table_name} mis à jour avec succès.")

                        elif table_name == "Planning":
                            traitement_id = int(input(
                                f"Nouveau ID du traitement ({existing_record.get('traitement_id', 'N/A')}) : ").strip() or existing_record.get(
                                'traitement_id'))
                            mois_debut = input(
                                f"Nouveau mois de début ({existing_record.get('mois_debut', 'N/A')}) : ").strip() or existing_record.get(
                                'mois_debut')
                            mois_fin = input(
                                f"Nouveau mois de fin ({existing_record.get('mois_fin', 'N/A')}) : ").strip() or existing_record.get(
                                'mois_fin')
                            mois_pause = input(
                                f"Nouveau mois de pause (facultatif) ({existing_record.get('mois_pause', 'N/A')}) : ").strip() or existing_record.get(
                                'mois_pause') or None

                            redondance_choisie = existing_record.get('redondance')
                            if redondances:
                                print("Options de redondance disponibles:")
                                for i, red in enumerate(redondances):
                                    print(f"{i + 1}. {red}")
                                while True:
                                    choix_str = input(
                                        f"Nouvelle redondance ({redondance_choisie}, entrez le numéro ou Entrée pour garder l'actuelle): ").strip()
                                    if not choix_str:
                                        break
                                    try:
                                        choix = int(choix_str) - 1
                                        if 0 <= choix < len(redondances):
                                            redondance_choisie = redondances[choix]
                                            break
                                        else:
                                            print("Choix invalide. Veuillez réessayer.")
                                    except ValueError:
                                        print("Entrée invalide. Veuillez entrer un numéro.")
                            else:
                                print("Aucune option de redondance trouvée.")
                                redondance_choisie = input(
                                    f"Nouvelle redondance ({redondance_choisie}) : ").strip() or redondance_choisie

                            await func(pool, id_a_modifier, traitement_id, mois_debut, mois_fin, mois_pause,
                                       redondance_choisie)
                            print(f"{table_name} mis à jour avec succès.")

                        elif table_name == "Facture":
                            traitement_id = int(input(
                                f"Nouveau ID du traitement ({existing_record.get('traitement_id', 'N/A')}) : ").strip() or existing_record.get(
                                'traitement_id'))

                            # Vérifier si le traitement existe avant de continuer
                            if not await read_traitement(pool, traitement_id):
                                print("Traitement inexistant. Opération annulée.")
                                continue

                            montant = float(input(
                                f"Nouveau montant ({existing_record.get('montant', 'N/A')}) : ").strip() or existing_record.get(
                                'montant'))
                            date_traitement_str = input(
                                f"Nouvelle date du traitement (AAAA-MM-JJ) ({existing_record.get('date_traitement', 'N/A')}) : ").strip() or str(
                                existing_record.get('date_traitement'))
                            date_traitement = datetime.strptime(date_traitement_str, '%Y-%m-%d').date()

                            # Note: The original `create_facture` section implied `axe_contrat` was passed directly.
                            # For update, we might need to fetch the contract_id from the treatment_id to get the axe.
                            # For simplicity, assuming `update_facture` directly takes `axe`.
                            axe = input(
                                f"Nouvel axe ({existing_record.get('axe', 'N/A')}) : ").strip() or existing_record.get(
                                'axe')  # Assuming 'axe' is directly in Facture or passed
                            remarque = input(
                                f"Nouvelle remarque (facultatif) ({existing_record.get('remarque', 'N/A')}) : ").strip() or existing_record.get(
                                'remarque') or None

                            await func(pool, id_a_modifier, traitement_id, montant, date_traitement, axe, remarque)
                            print(f"{table_name} mis à jour avec succès.")

                        elif table_name == "Signalement":
                            # Assuming read_signalement returns a dict-like object
                            planning_detail_id = int(input(
                                f"Nouveau planning ID ({existing_record.get('planning_detail_id', 'N/A')}) : ").strip() or existing_record.get(
                                'planning_detail_id'))
                            motif = input(
                                f"Nouveau motif ({existing_record.get('motif', 'N/A')}) : ").strip() or existing_record.get(
                                'motif')
                            type_signalement = input(
                                f"Nouveau type de signalement ({existing_record.get('type', 'N/A')}) : ").strip() or existing_record.get(
                                'type')  # 'type' is a common column name, might be 'type_signalement' in your DB

                            await func(pool, id_a_modifier, planning_detail_id, motif, type_signalement)
                            print("Signalement mis à jour.")

                    # --- DELETE Operations ---
                    elif operation_key == 'delete':
                        id_a_supprimer = int(input(f"ID du {table_name} à supprimer : ").strip())
                        confirm = input(
                            f"Êtes-vous sûr de vouloir supprimer le {table_name} avec l'ID {id_a_supprimer}? (oui/non) : ").strip().lower()
                        if confirm == 'oui':
                            await func(pool, id_a_supprimer)
                            print(f"{table_name} avec l'ID {id_a_supprimer} supprimé avec succès.")
                        else:
                            print("Suppression annulée.")

                except ValueError:
                    print(
                        "Entrée invalide. Veuillez vous assurer d'entrer des nombres pour les ID et les montants, et des dates au format AAAA-MM-JJ.")
                except Exception as e:
                    print(f"Une erreur est survenue lors de l'opération : {e}")
                    # You might want more specific error handling based on the type of exception
    except Exception as e:
        print(f"Une erreur critique est survenue lors de l'initialisation : {e}")
    finally:
        if pool:
            print("Fermeture du pool de connexions à la base de données.")
            pool.close()
            await pool.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())