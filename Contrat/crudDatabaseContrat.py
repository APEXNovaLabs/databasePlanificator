import asyncio
import aiomysql
from client import create_client, read_client, update_client, delete_client, obtenir_categories
from contrat import create_contrat, read_contrat, update_contrat, delete_contrat, obtenir_duree_contrat, obtenir_axe_contrat
from traitement import typestraitement, creation_traitement, obtenir_types_traitement, read_traitement, update_traitement, delete_traitement
from planning import create_planning, obtenir_redondances, read_planning, update_planning, delete_planning
from facture import create_facture, read_facture, obtenir_axe_contrat, delete_facture, update_facture
from signalement import create_signalement, read_signalement, update_signalement, delete_signalement
"""
  **** Remarque: l'historique présent dans ce fichier est obsolète
  Veuillez vous reférer au fichier historique.py pour le code fonctionnel
"""

# Accès aux catégories
async def obtenir_categories(pool, table_name, column_name):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}'")
            resultat = await cursor.fetchone()
            if resultat:
                enum_str = resultat[1].split("'")[1::2]
                return enum_str
            else:
                return []

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
        # Pour les catégories
        categories_client = await obtenir_categories(pool, "Client", "categorie")
        categories_contrat_duree = await obtenir_categories(pool, "Contrat", "duree")
        categories_contrat_type = await obtenir_categories(pool, "Contrat", "categorie")
        types_traitement = await obtenir_types_traitement(pool)
        redondances = await obtenir_redondances(pool)

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
        print("6. Signalement")
        print("7. Quitter")


        choix_table = input("Choisissez une table (1-7) : ")

        if choix_table == '7':
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
            '6': {'create': create_signalement, 'read': read_signalement, 'update': update_signalement,
                  'delete': delete_signalement, 'name': "Signalement"},
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
                        if categorie:
                            print("Catégories disponibles:")
                            for i, categories_client in enumerate(categorie):
                                print(f"{i + 1}. {categorie}")

                            while True:
                                try:
                                    choix = int(input("Choisissez une catégorie (entrez le numéro): ")) - 1
                                    if 0 <= choix < len(categorie):
                                        categorie_choisie = categories_client[choix]
                                        break  # Sortir de la boucle si le choix est valide
                                    else:
                                        print("Choix invalide. Veuillez réessayer.")
                                except ValueError:
                                    print("Entrée invalide. Veuillez entrer un numéro.")
                        else:
                            print("Aucune catégorie trouvée.")
                            categorie_choisie = input("Entrez la catégorie manuellement : ")

                        if categorie_choisie == "Particulier":
                            prenom = input("Prénom (facultatif) : ")
                        else:
                            prenom = input("Responsable : ")

                        email = input("Email : ")
                        telephone = input("Téléphone : ")
                        adresse = input("Adresse : ")
                        axe = input("Axe : ")
                        result = await func(pool, nom, prenom, email, telephone, adresse, categorie_choisie, axe)

                    elif table_name == "Contrat":
                        client_id = int(input("ID du client : "))
                        date_contrat = input("Date du contrat (AAAA-MM-JJ) : ")
                        date_debut = input("Date de début (AAAA-MM-JJ) : ")
                        # Sélection de la catégorie de durée du contrat
                        if categories_contrat_duree:
                            print("Catégories de durée disponibles:")
                            for i, categorie_contrat in enumerate(categories_contrat_duree):
                                print(f"{i + 1}. {categorie_contrat}")
                            while True:
                                try:
                                    choix = int(input("Choisissez une catégorie de durée (entrez le numéro): ")) - 1
                                    if 0 <= choix < len(categories_contrat_duree):
                                        duree_contrat_choisie = categories_contrat_duree[choix]
                                        break
                                    else:
                                        print("Choix invalide. Veuillez réessayer.")
                                except ValueError:
                                    print("Entrée invalide. Veuillez entrer un numéro.")
                        else:
                            print("Aucune catégorie de durée trouvée.")
                            duree_contrat_choisie = input("Entrez la catégorie de durée manuellement : ")
                        if duree_contrat_choisie != "Indeterminée":
                            date_fin = input("Date de fin (AAAA-MM-JJ) : ")
                        else:
                            date_fin = None  # ou une valeur par défaut, par exemple '0000-00-00'
                        if categories_contrat_type:
                            print("Catégories de type disponibles:")
                            for i, categorie_type_contrat in enumerate(categories_contrat_type):
                                print(f"{i + 1}. {categorie_type_contrat}")
                            while True:
                                try:
                                    choix = int(input("Choisissez une catégorie de type (entrez le numéro): ")) - 1
                                    if 0 <= choix < len(categories_contrat_type):
                                        categorie_contrat_choisie = categories_contrat_type[choix]
                                        break
                                    else:
                                        print("Choix invalide. Veuillez réessayer.")
                                except ValueError:
                                    print("Entrée invalide. Veuillez entrer un numéro.")
                        else:
                            print("Aucune catégorie de type trouvée.")
                            categorie_contrat_choisie = input("Entrez la catégorie de type manuellement : ")
                        result = await func(pool, client_id, date_contrat, date_debut, date_fin, duree_contrat_choisie,
                                            categorie_contrat_choisie)

                    elif table_name == "Traitement":
                        contrat_id = int(input("ID du contrat : "))
                        # Sélection des types de traitement
                        if types_traitement:
                            print("Types de traitement disponibles:")
                            for i, type_traitement in enumerate(types_traitement):
                                print(f"{i + 1}. {type_traitement}")
                            types_traitement_choisis = []
                            while True:
                                try:
                                    choix = input(
                                        "Choisissez un type de traitement (entrez les numéros séparés par des virgules, ou appuyez sur Entrée pour terminer): ")
                                    if not choix:
                                        break
                                    choix_list = [int(c) - 1 for c in choix.split(",")]
                                    for c in choix_list:
                                        if 0 <= c < len(types_traitement):
                                            types_traitement_choisis.append(types_traitement[c])
                                        else:
                                            print(f"Choix invalide : {c + 1}. Veuillez réessayer.")
                                except ValueError:
                                    print("Entrée invalide. Veuillez entrer des numéros séparés par des virgules.")
                        else:
                            print("Aucun type de traitement trouvé.")
                        # Insertion des traitements sélectionnés
                        for type_traitement_choisi in types_traitement_choisis:
                            # Récupérer l'id du type de traitement
                            async with pool.acquire() as conn:
                                async with conn.cursor() as cursor:
                                    await cursor.execute(
                                        "SELECT id_type_traitement FROM TypeTraitement WHERE typeTraitement = %s",
                                        (type_traitement_choisi,))
                                    resultat = await cursor.fetchone()
                                    if resultat:
                                        id_type_traitement = resultat[0]
                                        await func(pool, contrat_id,
                                                   id_type_traitement)
                                    else:
                                        print(f"Type de traitement non trouvé : {type_traitement_choisi}")
                        result = await func(pool, contrat_id, type_traitement)

                    elif table_name == "Planning":
                        # Récupérer les traitements associés au contrat
                        async with pool.acquire() as conn:
                            async with conn.cursor() as cursor:
                                await cursor.execute(
                                    "SELECT traitement_id, id_type_traitement, contrat_id FROM Traitement WHERE contrat_id = %s",
                                    (contrat_id,))
                                traitements = await cursor.fetchall()
                        if traitements:
                            for traitement_id, id_type_traitement, contrat_id in traitements:
                                # Récupérer le nom du type de traitement
                                type_traitement = next(
                                    key for key, val in types_traitement.items() if val == id_type_traitement)
                                # Récupérer la durée du contrat
                                duree_contrat = await obtenir_duree_contrat(pool, contrat_id)
                                print(f"\nPlanification pour le traitement {type_traitement} (ID: {traitement_id}):")
                                print(f"Durée du contrat : {duree_contrat}")
                                mois_debut = input("Mois de début : ")
                                if duree_contrat == "Déterminée":
                                    mois_fin = input("Mois de fin : ")
                                else:
                                    mois_fin = "Contrat à durée indéterminée"
                                mois_pause = input("Mois de pause (facultatif) : ")
                                # Sélection de la redondance
                                if redondances:
                                    print("Options de redondance disponibles:")
                                    for i, redondance in enumerate(redondances):
                                        print(f"{i + 1}. {redondance}")
                                    while True:
                                        try:
                                            choix = int(
                                                input("Choisissez une option de redondance (entrez le numéro): ")) - 1
                                            if 0 <= choix < len(redondances):
                                                redondance_choisie = redondances[choix]
                                                break
                                            else:
                                                print("Choix invalide. Veuillez réessayer.")
                                        except ValueError:
                                            print("Entrée invalide. Veuillez entrer un numéro.")
                                else:
                                    print("Aucune option de redondance trouvée.")
                                    redondance_choisie = input("Entrez l'option de redondance manuellement : ")
                                result = await func(pool, traitement_id, mois_debut, mois_fin, mois_pause,
                                                    redondance_choisie)
                        else:
                            print("Aucun traitement trouvé pour ce contrat.")

                    elif table_name == "Facture":
                        # Récupérer les traitements associés au contrat
                        async with pool.acquire() as conn:
                            async with conn.cursor() as cursor:
                                await cursor.execute(
                                    "SELECT traitement_id, id_type_traitement, contrat_id FROM Traitement WHERE contrat_id = %s",
                                    (contrat_id,))
                                traitements = await cursor.fetchall()
                        if traitements:
                            # Récupérer l'axe du contrat
                            axe_contrat = await obtenir_axe_contrat(pool, contrat_id)
                            for traitement_id, id_type_traitement, contrat_id in traitements:
                                # Récupérer le nom du type de traitement
                                type_traitement = next(
                                    key for key, val in types_traitement.items() if val == id_type_traitement)
                                print(f"\nFacture pour le traitement {type_traitement} (ID: {traitement_id}):")
                                montant = int(input("Montant : "))
                                date_traitement = input("Date du traitement (AAAA-MM-JJ) : ")
                                remarque = input("Remarque (facultatif) : ")
                                result = await func(pool, traitement_id, montant, date_traitement, axe_contrat,
                                                    remarque)
                        else:
                            print("Aucun traitement trouvé pour ce contrat.")


                    elif table_name == "Historique":
                        facture_id = int(input("ID de la facture : "))
                        contenu = input("Contenu : ")
                        result = await func(pool, facture_id, contenu)

                        print(f"{table_name} créé avec l'ID : {result}")
                        
                elif operation == 'read':
                    id_a_lire = int(input(f"ID du {table_name} à lire : "))
                    result = await func(pool, id_a_lire)
                    print(result)
                elif operation == 'update' :
                    id_a_modifier = int(input(f"ID du {table_name} à modifier : "))
                    if table_name == "Client":
                        nom = input("Nouveau nom : ")
                        prenom = input("Nouveau prénom (facultatif) : ")
                        email = input("Nouvel email : ")
                        telephone = input("Nouveau téléphone : ")
                        adresse = input("Nouvelle adresse : ")
                        # Sélection de la catégorie du client
                        if categories_client:
                            print("Catégories disponibles:")
                            for i, categorie in enumerate(categories_client):
                                print(f"{i + 1}. {categorie}")
                                while True:
                                    try:
                                        choix = int(input("Choisissez une catégorie (entrez le numéro): ")) - 1
                                        if 0 <= choix < len(categories_client):
                                            categorie_choisie = categories_client[choix]
                                            break
                                        else:
                                            print("Choix invalide. Veuillez réessayer.")
                                    except ValueError:
                                        print("Entrée invalide. Veuillez entrer un numéro.")
                        else:
                            print("Aucune catégorie trouvée.")
                            categorie_choisie = input("Entrez la catégorie manuellement : ")
                            axe = input("Nouvel axe : ")
                    await func(pool, id_a_modifier, nom, prenom, email, telephone, adresse, categorie_choisie, axe)

                elif table_name == "Contrat":
                    client_id = int(input("Nouvel ID du client : "))
                    date_contrat = input("Nouvelle date du contrat (AAAA-MM-JJ) : ")
                    date_debut = input("Nouvelle date de début (AAAA-MM-JJ) : ")
                    # Sélection de la durée du contrat
                    if categories_contrat_duree:
                        print("Catégories de durée disponibles:")
                        for i, categorie_contrat in enumerate(categories_contrat_duree):
                            print(f"{i + 1}. {categorie_contrat}")
                        while True:
                            try:
                                choix = int(input("Choisissez une catégorie de durée (entrez le numéro): ")) - 1
                                if 0 <= choix < len(categories_contrat_duree):
                                    duree_contrat_choisie = categories_contrat_duree[choix]
                                    break
                                else:
                                    print("Choix invalide. Veuillez réessayer.")
                            except ValueError:
                                print("Entrée invalide. Veuillez entrer un numéro.")
                    else:
                        print("Aucune catégorie de durée trouvée.")
                    duree_contrat_choisie = input("Entrez la catégorie de durée manuellement : ")
                    if duree_contrat_choisie != "Indeterminée":
                        date_fin = input("Nouvelle date de fin (AAAA-MM-JJ) : ")
                    else:
                        date_fin = None  # ou une valeur par défaut, par exemple '0000-00-00'
                    # Sélection de la catégorie du contrat
                    if categories_contrat_type:
                        print("Catégories de type disponibles:")
                        for i, categorie_type_contrat in enumerate(categories_contrat_type):
                            print(f"{i + 1}. {categorie_type_contrat}")
                            while True:
                                try:
                                    choix = int(input("Choisissez une catégorie de type (entrez le numéro): ")) - 1
                                    if 0 <= choix < len(categories_contrat_type):
                                        categorie_contrat_choisie = categories_contrat_type[choix]
                                        break
                                    else:
                                        print("Choix invalide. Veuillez réessayer.")
                                except ValueError:
                                    print("Entrée invalide. Veuillez entrer un numéro.")
                    else:
                        print("Aucune catégorie de type trouvée.")
                        categorie_contrat_choisie = input("Entrez la catégorie de type manuellement : ")
                        await func(pool, id_a_modifier, client_id, date_contrat, date_debut, date_fin, duree_contrat_choisie,
                           categorie_contrat_choisie)

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
                elif choix_table == '6':
                          while True:
                              print(f"\n Effectuer un signalement: ")
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
                                      traitement_id = int(input("ID du traitement pour le signalement : "))

                                      # Récupérer les planning_detail_id associés au traitement
                                      async with pool.acquire() as conn:
                                          async with conn.cursor() as cursor:
                                              await cursor.execute(
                                                  "SELECT planning_detail_id FROM PlanningDetails WHERE traitement_id = %s",
                                                  (traitement_id,))
                                              planning_details = await cursor.fetchall()

                                      if not planning_details:
                                          print("Aucun planning trouvé pour ce traitement.")
                                          continue

                                      print("Planning disponibles :")
                                      for i, planning_detail in enumerate(planning_details):
                                          print(f"{i + 1}. Planning ID : {planning_detail[0]}")

                                      while True:
                                          try:
                                              choix_planning = int(
                                                  input("Choisissez un planning (entrez le numéro) : ")) - 1
                                              if 0 <= choix_planning < len(planning_details):
                                                  planning_detail_id = planning_details[choix_planning][0]
                                                  break
                                              else:
                                                  print("Choix invalide. Veuillez réessayer.")
                                          except ValueError:
                                              print("Entrée invalide. Veuillez entrer un numéro.")

                                      motif = input("Motif du signalement : ")
                                      type_signalement = input("Type de signalement (Avancement/Décalage) : ")

                                      result = await create_signalement(pool, planning_detail_id, motif,
                                                                        type_signalement)
                                      print(f"Signalement créé avec l'ID : {result}")

                                  elif operation == 'update':
                                      signalement_id = int(input("ID du signalement à modifier : "))

                                      # Récupérer le signalement existant
                                      async with pool.acquire() as conn:
                                          async with conn.cursor() as cursor:
                                              await cursor.execute(
                                                  "SELECT planning_detail_id, motif, type FROM Signalement WHERE signalement_id = %s",
                                                  (signalement_id,))
                                              signalement_existant = await cursor.fetchone()

                                      if not signalement_existant:
                                          print("Signalement non trouvé.")
                                          continue

                                      planning_detail_id_existant, motif_existant, type_existant = signalement_existant

                                      # Demander à l'utilisateur de modifier les champs
                                      planning_detail_id = int(input(
                                          f"Nouveau planning ID ({planning_detail_id_existant}) : ") or planning_detail_id_existant)
                                      motif = input(f"Nouveau motif ({motif_existant}) : ") or motif_existant
                                      type_signalement = input(
                                          f"Nouveau type de signalement ({type_existant}) : ") or type_existant

                                      await update_signalement(pool, signalement_id, planning_detail_id, motif,
                                                               type_signalement)
                                      print("Signalement mis à jour.")


                                  elif operation == 'read':
                                      if table_name == "Signalement":
                                          signalement_id = int(input("ID du signalement à lire : "))
                                          signalement = await read_signalement(pool, signalement_id)
                                          if signalement:
                                              signalement_id, motif, type_signalement, planning_detail_id, traitement_id, date_debut, date_fin, type_traitement = signalement
                                              print(f"Signalement ID: {signalement_id}")
                                              print(f"Motif: {motif}")
                                              print(f"Type: {type_signalement}")
                                              print(f"Planning ID: {planning_detail_id}")
                                              print(f"Traitement ID: {traitement_id}")
                                              print(f"Type de traitement: {type_traitement}")
                                              print(f"Date de début: {date_debut}")
                                              print(f"Date de fin: {date_fin}")
                                          else:
                                              print("Signalement non trouvé.")
                                  elif operation == 'delete':
                                      signalement_id = int(input("ID du signalement à supprimer : "))
                                      await delete_signalement(pool, signalement_id)
                                      print("Signalement supprimé.")
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