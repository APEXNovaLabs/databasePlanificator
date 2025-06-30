import asyncio
from datetime import datetime

import aiomysql
from Contrat.CRUDonClient import (
    create_client,
    read_client,
    update_client,
    delete_client,
    obtenir_categories,
)
from Contrat.CRUDonContrat import (
    create_contrat,
    read_contrat,
    update_contrat,
    delete_contrat,
    obtenir_duree_contrat,
    obtenir_axe_contrat,
)
from Contrat.CRUDonTraitement import (
    creation_traitement,
    obtenir_types_traitement,
    read_traitement,
    update_traitement,
    delete_traitement,
)
from Contrat.CRUDonPlanning import (
    create_planning,
    obtenir_redondances,
    read_planning,
    update_planning,
    delete_planning,
)
# Renaming to avoid conflict with gestionFacture's create_facture
from Contrat.CRUDonFacture import (
    create_facture as crudon_create_facture,
    read_facture as crudon_read_facture,
    delete_facture as crudon_delete_facture,
    update_facture as crudon_update_facture,
)
from Contrat.CRUDonSignalement import (
    create_signalement,
    read_signalement,
    update_signalement,
    delete_signalement,
)

from Contrat.fonctionnalites.Facture.gestionFacture import (
    create_facture, get_facture_details, update_facture_montant_and_status,
    delete_facture, get_all_factures_for_client,
    obtenir_etats_facture, obtenir_axes
)

# Import the Excel generation function
from Rapports.export_excel import generationFactureClient # Assuming export_excel.py is in a 'Rapports' directory

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
        # Ensure 'typeTraitement' and 'id_type_traitement' keys exist before using them
        types_traitement_names = [t['typeTraitement'] for t in types_traitement_data if 'typeTraitement' in t]
        types_traitement_map = {t['typeTraitement']: t['id_type_traitement'] for t in types_traitement_data if 'typeTraitement' in t and 'id_type_traitement' in t}

        redondances = await obtenir_redondances(pool)

        etats_facture = await obtenir_etats_facture(pool)
        axes_facture = await obtenir_axes(pool)

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
                # Mapping Facture operations to gestionFacture functions
                '5': {'create': create_facture, 'read': get_facture_details, 'update': update_facture_montant_and_status,
                      'delete': delete_facture, 'name': "Facture"},
                '6': {'create': create_signalement, 'read': read_signalement, 'update': update_signalement,
                      'delete': delete_signalement, 'name': "Signalement"},
            }

            if choix_table not in table_functions:
                print("Choix de table invalide.")
                continue

            table_name = table_functions[choix_table]['name']

            while True:
                # Special menu for Facture with additional options
                if table_name == "Facture":
                    print(f"\n--- Opérations pour {table_name} ---")
                    print("1. Créer une facture")
                    print("2. Lire les détails d'une facture (par ID)")
                    print("3. Modifier le montant et/ou le statut d'une facture")
                    print("4. Supprimer une facture")
                    print("5. Afficher toutes les factures pour un client")
                    print("6. Générer une facture Excel pour un client") # NEW OPTION
                    print("7. Retour au menu principal")

                    choix_operation = input("Choisissez une opération (1-7) : ").strip()

                    if choix_operation == '7':
                        break # Return to main menu
                    elif choix_operation == '1': # Create Facture
                        contrat_id = int(input("ID du contrat pour lequel facturer les traitements : ").strip())

                        # Fetch treatments associated with the contract
                        async with pool.acquire() as conn:
                            async with conn.cursor(aiomysql.DictCursor) as cursor:
                                await cursor.execute(
                                    "SELECT t.traitement_id, t.id_type_traitement FROM Traitement t WHERE t.contrat_id = %s", (contrat_id,))
                                traitements = await cursor.fetchall()

                        if not traitements:
                            print("Aucun traitement trouvé pour ce contrat. Impossible de créer des factures.")
                            continue

                        print("\nTraitements disponibles pour ce contrat:")
                        for i, t_info in enumerate(traitements):
                            type_name = next((name for name, id_val in types_traitement_map.items() if id_val == t_info['id_type_traitement']), "Inconnu")
                            print(f"{i+1}. Traitement ID: {t_info['traitement_id']} (Type: {type_name})")

                        selected_traitement_id = None
                        while True:
                            try:
                                choice = input("Sélectionnez le numéro du traitement pour la facture : ").strip()
                                if choice.isdigit() and 1 <= int(choice) <= len(traitements):
                                    selected_traitement_id = traitements[int(choice)-1]['traitement_id']
                                    break
                                else:
                                    print("Choix invalide.")
                            except ValueError:
                                print("Entrée invalide. Veuillez entrer un numéro.")

                        if not selected_traitement_id:
                            print("Aucun traitement sélectionné. Annulation de la création de facture.")
                            continue

                        planning_details_for_treatment = []
                        async with pool.acquire() as conn:
                            async with conn.cursor(aiomysql.DictCursor) as cursor:
                                await cursor.execute(
                                    """
                                    SELECT pd.planning_detail_id, pd.date_planification, pd.statut
                                    FROM PlanningDetails pd
                                    JOIN Planning p ON pd.planning_id = p.planning_id
                                    WHERE p.traitement_id = %s
                                    ORDER BY pd.date_planification DESC
                                    """, (selected_traitement_id,))
                                planning_details_for_treatment = await cursor.fetchall()

                        if not planning_details_for_treatment:
                            print(f"Aucun détail de planification trouvé pour le traitement ID {selected_traitement_id}. Impossible de créer une facture.")
                            continue

                        print("\nDétails de planification disponibles pour ce traitement:")
                        for i, pd_info in enumerate(planning_details_for_treatment):
                            print(f"{i+1}. Planning Detail ID: {pd_info['planning_detail_id']} (Date: {pd_info['date_planification']}, Statut: {pd_info['statut']})")

                        selected_planning_detail_id = None
                        selected_date_traitement = None
                        while True:
                            try:
                                choice = input("Sélectionnez le numéro du détail de planification pour la facture : ").strip()
                                if choice.isdigit() and 1 <= int(choice) <= len(planning_details_for_treatment):
                                    selected_planning_detail_id = planning_details_for_treatment[int(choice)-1]['planning_detail_id']
                                    selected_date_traitement = planning_details_for_treatment[int(choice)-1]['date_planification']
                                    break
                                else:
                                    print("Choix invalide.")
                            except ValueError:
                                print("Entrée invalide. Veuillez entrer un numéro.")

                        if not selected_planning_detail_id:
                            print("Aucun détail de planification sélectionné. Annulation de la création de facture.")
                            continue

                        montant = float(input("Montant de la facture : ").strip())
                        remarque = input("Remarque (facultatif) : ").strip() or None

                        # Retrieve 'axe' for the associated contract
                        axe_contrat = await obtenir_axe_contrat(pool, contrat_id)
                        if not axe_contrat:
                            print("Impossible de récupérer l'axe du contrat. La création de la facture pourrait être incomplète.")
                            axe_contrat = "N/A" # Default if not found

                        result_id = await create_facture(pool, selected_planning_detail_id, montant, selected_date_traitement, axe_contrat, remarque)
                        print(f"Facture créée avec l'ID : {result_id}")

                    elif choix_operation == '2': # Read Facture details by ID
                        facture_id = int(input("ID de la facture à lire : ").strip())
                        result = await get_facture_details(pool, facture_id)
                        if result:
                            print("\n--- Détails de la Facture ---")
                            for key, value in result.items():
                                print(f"{key}: {value}")
                        else:
                            print(f"Aucune facture trouvée avec l'ID {facture_id}.")

                    elif choix_operation == '3': # Update Facture montant and status
                        facture_id = int(input("ID de la facture à modifier : ").strip())
                        existing_facture = await get_facture_details(pool, facture_id)
                        if not existing_facture:
                            print(f"Aucune facture trouvée avec l'ID {facture_id}.")
                            continue

                        new_montant_str = input(f"Nouveau montant ({existing_facture.get('montant', 'N/A')}, laissez vide pour garder l'actuel) : ").strip()
                        new_montant = float(new_montant_str) if new_montant_str else existing_facture.get('montant')

                        print("États de facture disponibles:")
                        for i, etat in enumerate(etats_facture):
                            print(f"{i + 1}. {etat}")
                        current_status_name = existing_facture.get('etat_facture')
                        current_status_idx = etats_facture.index(current_status_name) + 1 if current_status_name in etats_facture else -1

                        new_status_name = None
                        while True:
                            status_choice_str = input(f"Nouvel état ({current_status_name}, entrez le numéro ou Entrée pour garder l'actuel) : ").strip()
                            if not status_choice_str:
                                new_status_name = current_status_name
                                break
                            try:
                                choice_idx = int(status_choice_str) - 1
                                if 0 <= choice_idx < len(etats_facture):
                                    new_status_name = etats_facture[choice_idx]
                                    break
                                else:
                                    print("Choix invalide. Veuillez réessayer.")
                            except ValueError:
                                print("Entrée invalide. Veuillez entrer un numéro.")

                        if await update_facture_montant_and_status(pool, facture_id, new_montant, new_status_name):
                            print(f"Facture ID {facture_id} mise à jour avec succès.")
                        else:
                            print(f"Échec de la mise à jour de la facture ID {facture_id}.")

                    elif choix_operation == '4': # Delete Facture
                        facture_id = int(input("ID de la facture à supprimer : ").strip())
                        if await delete_facture(pool, facture_id):
                            print(f"Facture ID {facture_id} supprimée avec succès.")
                        else:
                            print(f"Échec de la suppression de la facture ID {facture_id}.")

                    elif choix_operation == '5': # Get all invoices for a client
                        client_id = int(input("ID du client pour afficher toutes les factures : ").strip())
                        all_factures = await get_all_factures_for_client(pool, client_id)
                        if all_factures:
                            print(f"\n--- Toutes les Factures pour le Client ID {client_id} ---")
                            for facture in all_factures:
                                print("-" * 30)
                                for key, value in facture.items():
                                    print(f"{key}: {value}")
                            print("-" * 30)
                        else:
                            print(f"Aucune facture trouvée pour le client ID {client_id}.")

                    elif choix_operation == '6': # NEW: Generate Excel Invoice
                        client_id = int(input("ID du client pour générer la facture Excel : ").strip())
                        mois_str = input("Mois de la facture (MM, ex: 01 pour Janvier) : ").strip()
                        annee_str = input("Année de la facture (AAAA, ex: 2023) : ").strip()

                        if not mois_str.isdigit() or not annee_str.isdigit() or not (1 <= int(mois_str) <= 12) or len(annee_str) != 4:
                            print("Mois ou année invalide. Veuillez entrer un mois (MM) entre 01 et 12 et une année (AAAA) à quatre chiffres.")
                            continue

                        mois = int(mois_str)
                        annee = int(annee_str)

                        # Call the Excel generation function
                        success = await generationFactureClient(pool, client_id, mois, annee)
                        if success:
                            print(f"Facture Excel générée avec succès pour le client {client_id} pour {mois}/{annee}.")
                        else:
                            print(f"Échec de la génération de la facture Excel pour le client {client_id} pour {mois}/{annee}.")

                    else:
                        print("Choix d'opération invalide pour Facture.")
                    continue # Continue the Facture menu loop

                # Standard operations for other tables
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
                    # --- CREATE Operations (Existing logic, ensure it aligns with any new function signatures) ---
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
                                    if categorie_choisie:
                                        break
                                    else:
                                        print("La catégorie ne peut pas être vide. Veuillez la saisir.")

                            if categorie_choisie == "Particulier":
                                prenom = input("Prénom (facultatif) : ").strip() or None
                            elif categorie_choisie == "Société":
                                prenom = input("Responsable : ").strip() or None
                                nif = input("NIF (Numéro d'Immatriculation Fiscale): ").strip() or None
                                stat = input("Stat: ").strip() or None
                            else:
                                prenom = input("Responsable : ").strip() or None

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
                            duree_contrat_mois = None
                            if duree_contrat_choisie == "Déterminée":
                                date_fin_contrat_str = input("Date de fin (AAAA-MM-JJ) : ").strip()
                                date_fin_contrat = datetime.strptime(date_fin_contrat_str, '%Y-%m-%d').date()
                                duree_contrat_mois = int(input("Durée du contrat en mois : ").strip())

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
                                            types_traitement_choisis_ids = []
                                            break
                                    if valid_choices:
                                        break
                                except ValueError:
                                    print("Entrée invalide. Veuillez entrer des numéros séparés par des virgules.")

                            if not types_traitement_choisis_ids:
                                print("Aucun type de traitement valide sélectionné. Annulation de la création du traitement.")
                                continue

                            for id_type_traitement_chosen in types_traitement_choisis_ids:
                                result_id = await func(pool, contrat_id, id_type_traitement_chosen)
                                print(f"Traitement créé avec l'ID : {result_id} pour le type de traitement ID {id_type_traitement_chosen}")

                        elif table_name == "Planning":
                            contrat_id = int(input("Entrez l'ID du contrat pour lequel planifier les traitements: ").strip())

                            async with pool.acquire() as conn:
                                async with conn.cursor(aiomysql.DictCursor) as cursor:
                                    await cursor.execute(
                                        "SELECT traitement_id, id_type_traitement FROM Traitement WHERE contrat_id = %s",
                                        (contrat_id,))
                                    traitements = await cursor.fetchall()

                            if not traitements:
                                print("Aucun traitement trouvé pour ce contrat. Veuillez d'abord créer des traitements.")
                                continue

                            for traitement_info in traitements:
                                traitement_id = traitement_info['traitement_id']
                                id_type_traitement = traitement_info['id_type_traitement']

                                type_traitement_name = next((name for name, id_val in types_traitement_map.items() if
                                                             id_val == id_type_traitement), "Inconnu")

                                duree_contrat = await obtenir_duree_contrat(pool, contrat_id)

                                print(f"\nPlanification pour le traitement '{type_traitement_name}' (ID: {traitement_id}):")
                                print(f"Durée du contrat : {duree_contrat}")

                                mois_debut = input("Mois de début (ex: 01 pour Janvier, 12 pour Décembre) : ").strip()
                                if not (mois_debut.isdigit() and 1 <= int(mois_debut) <= 12):
                                    print("Mois de début invalide. Veuillez entrer un nombre entre 1 et 12.")
                                    continue

                                mois_fin = None
                                if duree_contrat == "Déterminée":
                                    mois_fin = input("Mois de fin (ex: 01 pour Janvier, 12 pour Décembre) : ").strip()
                                    if not (mois_fin.isdigit() and 1 <= int(mois_fin) <= 12):
                                        print("Mois de fin invalide. Veuillez entrer un nombre entre 1 et 12.")
                                        continue
                                else:
                                    print("Mois de fin : Contrat à durée indéterminée (N/A)")

                                mois_pause = input("Mois de pause (facultatif, ex: 07,08 pour Juillet, Août. Laissez vide si aucun) : ").strip() or None

                                redondance_choisie = None
                                if redondances:
                                    print("Options de redondance disponibles:")
                                    for i, red in enumerate(redondances):
                                        print(f"{i + 1}. {red}")
                                    while True:
                                        try:
                                            choix_red = int(input("Choisissez une option de redondance (entrez le numéro): ").strip()) - 1
                                            if 0 <= choix_red < len(redondances):
                                                redondance_choisie = redondances[choix_red]
                                                break
                                            else:
                                                print("Choix invalide. Veuillez réessayer.")
                                        except ValueError:
                                            print("Entrée invalide. Veuillez entrer un numéro.")
                                else:
                                    print("Aucune option de redondance trouvée. Entrez-la manuellement.")
                                    redondance_choisie = input("Entrez l'option de redondance manuellement (ex: Mensuel, Hebdomadaire) : ").strip()

                                result_id = await func(pool, traitement_id, mois_debut, mois_fin, mois_pause,
                                                       redondance_choisie)
                                print(f"Planning créé avec l'ID : {result_id} pour le traitement ID {traitement_id}")

                        elif table_name == "Signalement":
                            traitement_id = int(input("ID du traitement pour le signalement : ").strip())

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
                                print(f"{i + 1}. Planning ID : {pd['planning_detail_id']} (Date: {pd['date_planification']})")

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


                    # --- READ Operations (Existing logic) ---
                    elif operation_key == 'read':
                        if table_name == "Client":
                            print("\n--- Options de lecture pour Client ---")
                            print("1. Lire un client par ID")
                            print("2. Lire tous les clients")
                            read_option = input("Choisissez une option (1-2) : ").strip()

                            if read_option == '1':
                                client_id_to_read = int(input("ID du client à lire : ").strip())
                                result = await func(pool, client_id_to_read)
                                if result:
                                    print("\n--- Détails du Client ---")
                                    for key, value in result.items():
                                        print(f"{key}: {value}")
                                else:
                                    print(f"Aucun client trouvé avec l'ID {client_id_to_read}.")
                            elif read_option == '2':
                                all_clients = await func(pool, None)
                                if all_clients:
                                    print("\n--- Tous les Clients ---")
                                    for client in all_clients:
                                        print("-" * 20)
                                        for key, value in client.items():
                                            print(f"{key}: {value}")
                                    print("-" * 20)
                                else:
                                    print("Aucun client trouvé dans la base de données.")
                            else:
                                print("Option de lecture invalide.")
                        else:
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

                    # --- UPDATE Operations (Completed logic) ---
                    elif operation_key == 'update':
                        id_a_modifier = int(input(f"ID du {table_name} à modifier : ").strip())
                        # First, read the existing record to pre-fill prompts
                        existing_record = None
                        if table_name == "Client":
                            existing_record = await read_client(pool, id_a_modifier)
                        elif table_name == "Contrat":
                            existing_record = await read_contrat(pool, id_a_modifier)
                        elif table_name == "Traitement":
                            existing_record = await read_traitement(pool, id_a_modifier)
                        elif table_name == "Planning":
                            existing_record = await read_planning(pool, id_a_modifier)
                        elif table_name == "Signalement":
                            existing_record = await read_signalement(pool, id_a_modifier)

                        if not existing_record:
                            print(f"Aucun {table_name} trouvé avec l'ID {id_a_modifier}.")
                            continue

                        if table_name == "Client":
                            nom = input(
                                f"Nouveau nom ({existing_record.get('nom', 'N/A')}) : ").strip() or existing_record.get('nom')

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
                                        break
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
                                print("Aucune catégorie trouvée. Entrez-la manuellement.")
                                new_categorie = input(f"Nouvelle catégorie ({categorie_choisie}) : ").strip()
                                if new_categorie:
                                    categorie_choisie = new_categorie

                            prenom = existing_record.get('prenom')
                            nif = existing_record.get('nif')
                            stat = existing_record.get('stat')

                            if categorie_choisie == "Particulier":
                                prenom = input(f"Nouveau prénom ({existing_record.get('prenom', 'N/A')}) : ").strip() or existing_record.get('prenom')
                                nif = None # NIF and Stat not applicable for Particulier
                                stat = None
                            elif categorie_choisie == "Société":
                                prenom = input(f"Nouveau responsable ({existing_record.get('prenom', 'N/A')}) : ").strip() or existing_record.get('prenom')
                                nif = input(f"Nouveau NIF ({existing_record.get('nif', 'N/A')}) : ").strip() or existing_record.get('nif')
                                stat = input(f"Nouveau Stat ({existing_record.get('stat', 'N/A')}) : ").strip() or existing_record.get('stat')
                            else: # For 'Organisation' or other categories
                                prenom = input(f"Nouveau responsable ({existing_record.get('prenom', 'N/A')}) : ").strip() or existing_record.get('prenom')
                                nif = input(f"Nouveau NIF ({existing_record.get('nif', 'N/A')}) : ").strip() or existing_record.get('nif') # Still ask as it might be relevant
                                stat = input(f"Nouveau Stat ({existing_record.get('stat', 'N/A')}) : ").strip() or existing_record.get('stat')


                            email = input(f"Nouvel email ({existing_record.get('email', 'N/A')}) : ").strip() or existing_record.get('email')
                            telephone = input(f"Nouveau téléphone ({existing_record.get('telephone', 'N/A')}) : ").strip() or existing_record.get('telephone')
                            adresse = input(f"Nouvelle adresse ({existing_record.get('adresse', 'N/A')}) : ").strip() or existing_record.get('adresse')
                            axe = input(f"Nouvel axe ({existing_record.get('axe', 'N/A')}) : ").strip() or existing_record.get('axe')

                            if await func(pool, id_a_modifier, nom, prenom, email, telephone, adresse, categorie_choisie, nif, stat, axe):
                                print(f"{table_name} ID {id_a_modifier} modifié avec succès.")
                            else:
                                print(f"Échec de la modification du {table_name} ID {id_a_modifier}.")

                        elif table_name == "Contrat":
                            client_id = int(input(f"Nouvel ID du client ({existing_record.get('client_id', 'N/A')}) : ").strip() or existing_record.get('client_id'))
                            date_contrat_str = input(f"Nouvelle date du contrat (AAAA-MM-JJ) ({existing_record.get('date_contrat', 'N/A')}) : ").strip() or str(existing_record.get('date_contrat'))
                            date_contrat = datetime.strptime(date_contrat_str, '%Y-%m-%d').date()

                            date_debut_str = input(f"Nouvelle date de début (AAAA-MM-JJ) ({existing_record.get('date_debut', 'N/A')}) : ").strip() or str(existing_record.get('date_debut'))
                            date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()

                            duree_contrat_choisie = existing_record.get('duree_contrat')
                            if categories_contrat_duree:
                                print("Catégories de durée disponibles:")
                                for i, cat in enumerate(categories_contrat_duree):
                                    print(f"{i + 1}. {cat}")
                                current_duree_idx = categories_contrat_duree.index(duree_contrat_choisie) if duree_contrat_choisie in categories_contrat_duree else -1
                                while True:
                                    choix_str = input(f"Choisissez une catégorie de durée ({duree_contrat_choisie}, entrez le numéro ou Entrée pour garder l'actuelle): ").strip()
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
                                new_duree = input(f"Nouvelle catégorie de durée ({duree_contrat_choisie}) : ").strip()
                                if new_duree:
                                    duree_contrat_choisie = new_duree

                            date_fin_contrat = existing_record.get('date_fin_contrat')
                            duree_contrat_mois = existing_record.get('duree_contrat_mois')

                            if duree_contrat_choisie == "Déterminée":
                                date_fin_contrat_str = input(f"Nouvelle date de fin (AAAA-MM-JJ) ({existing_record.get('date_fin_contrat', 'N/A')}) : ").strip() or str(existing_record.get('date_fin_contrat'))
                                date_fin_contrat = datetime.strptime(date_fin_contrat_str, '%Y-%m-%d').date() if date_fin_contrat_str != 'None' else None # Handle 'None' for optional dates
                                duree_contrat_mois_str = input(f"Nouvelle durée du contrat en mois ({existing_record.get('duree_contrat_mois', 'N/A')}) : ").strip() or str(existing_record.get('duree_contrat_mois'))
                                duree_contrat_mois = int(duree_contrat_mois_str) if duree_contrat_mois_str.isdigit() else existing_record.get('duree_contrat_mois')
                            else:
                                date_fin_contrat = None
                                duree_contrat_mois = None

                            categorie_contrat_choisie = existing_record.get('categorie_contrat')
                            if categories_contrat_type:
                                print("Catégories de type disponibles:")
                                for i, cat in enumerate(categories_contrat_type):
                                    print(f"{i + 1}. {cat}")
                                current_type_idx = categories_contrat_type.index(categorie_contrat_choisie) if categorie_contrat_choisie in categories_contrat_type else -1
                                while True:
                                    choix_str = input(f"Choisissez une catégorie de type ({categorie_contrat_choisie}, entrez le numéro ou Entrée pour garder l'actuelle): ").strip()
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
                                new_type = input(f"Nouvelle catégorie de type ({categorie_contrat_choisie}) : ").strip()
                                if new_type:
                                    categorie_contrat_choisie = new_type

                            if await func(pool, id_a_modifier, client_id, date_contrat, date_debut, date_fin_contrat,
                                           duree_contrat_choisie, categorie_contrat_choisie, duree_contrat_mois):
                                print(f"{table_name} ID {id_a_modifier} modifié avec succès.")
                            else:
                                print(f"Échec de la modification du {table_name} ID {id_a_modifier}.")

                        elif table_name == "Traitement":
                            contrat_id = int(input(f"Nouvel ID du contrat ({existing_record.get('contrat_id', 'N/A')}) : ").strip() or existing_record.get('contrat_id'))

                            current_type_traitement_id = existing_record.get('id_type_traitement')
                            current_type_traitement_name = next((name for name, id_val in types_traitement_map.items() if id_val == current_type_traitement_id), "Inconnu")

                            print("Types de traitement disponibles:")
                            for i, tt_name in enumerate(types_traitement_names):
                                print(f"{i + 1}. {tt_name}")

                            new_type_traitement_id = current_type_traitement_id
                            while True:
                                choix_str = input(f"Nouveau type de traitement ({current_type_traitement_name}, entrez le numéro ou Entrée pour garder l'actuel) : ").strip()
                                if not choix_str:
                                    break
                                try:
                                    choix = int(choix_str) - 1
                                    if 0 <= choix < len(types_traitement_names):
                                        selected_type_name = types_traitement_names[choix]
                                        new_type_traitement_id = types_traitement_map[selected_type_name]
                                        break
                                    else:
                                        print("Choix invalide. Veuillez réessayer.")
                                except ValueError:
                                    print("Entrée invalide. Veuillez entrer un numéro.")

                            if await func(pool, id_a_modifier, contrat_id, new_type_traitement_id):
                                print(f"{table_name} ID {id_a_modifier} modifié avec succès.")
                            else:
                                print(f"Échec de la modification du {table_name} ID {id_a_modifier}.")

                        elif table_name == "Planning":
                            traitement_id = int(input(f"Nouvel ID du traitement ({existing_record.get('traitement_id', 'N/A')}) : ").strip() or existing_record.get('traitement_id'))

                            mois_debut = input(f"Nouveau mois de début ({existing_record.get('mois_debut', 'N/A')}) : ").strip() or existing_record.get('mois_debut')
                            mois_fin = input(f"Nouveau mois de fin ({existing_record.get('mois_fin', 'N/A')}) : ").strip() or existing_record.get('mois_fin')
                            mois_pause = input(f"Nouveaux mois de pause (facultatif) ({existing_record.get('mois_pause', 'N/A')}) : ").strip() or existing_record.get('mois_pause') or None

                            redondance_choisie = existing_record.get('redondance')
                            if redondances:
                                print("Options de redondance disponibles:")
                                for i, red in enumerate(redondances):
                                    print(f"{i + 1}. {red}")
                                current_red_idx = redondances.index(redondance_choisie) if redondance_choisie in redondances else -1
                                while True:
                                    choix_str = input(f"Choisissez une option de redondance ({redondance_choisie}, entrez le numéro ou Entrée pour garder l'actuelle): ").strip()
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
                                new_redondance = input(f"Nouvelle option de redondance ({redondance_choisie}) : ").strip()
                                if new_redondance:
                                    redondance_choisie = new_redondance

                            if await func(pool, id_a_modifier, traitement_id, mois_debut, mois_fin, mois_pause, redondance_choisie):
                                print(f"{table_name} ID {id_a_modifier} modifié avec succès.")
                            else:
                                print(f"Échec de la modification du {table_name} ID {id_a_modifier}.")

                        elif table_name == "Signalement":
                            planning_detail_id = int(input(f"Nouvel ID du détail de planification ({existing_record.get('planning_detail_id', 'N/A')}) : ").strip() or existing_record.get('planning_detail_id'))
                            motif = input(f"Nouveau motif ({existing_record.get('motif', 'N/A')}) : ").strip() or existing_record.get('motif')
                            type_signalement = input(f"Nouveau type de signalement (Avancement/Décalage) ({existing_record.get('type_signalement', 'N/A')}) : ").strip() or existing_record.get('type_signalement')

                            if await func(pool, id_a_modifier, planning_detail_id, motif, type_signalement):
                                print(f"Signalement ID {id_a_modifier} modifié avec succès.")
                            else:
                                print(f"Échec de la modification du Signalement ID {id_a_modifier}.")

                        else: # Fallback for tables that don't have custom update logic yet
                            print("Opération de modification non implémentée pour cette table.")

                    # --- DELETE Operations (Existing logic) ---
                    elif operation_key == 'delete':
                        id_a_supprimer = int(input(f"ID du {table_name} à supprimer : ").strip())
                        if await func(pool, id_a_supprimer):
                            print(f"{table_name} ID {id_a_supprimer} supprimé avec succès.")
                        else:
                            print(f"Échec de la suppression du {table_name} ID {id_a_supprimer}.")

                except ValueError:
                    print("Erreur : Veuillez entrer un nombre valide pour l'ID.")
                except Exception as e:
                    print(f"Une erreur inattendue est survenue : {e}")

    except aiomysql.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    finally:
        if pool:
            pool.close()
            await pool.wait_closed()
            print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    asyncio.run(main())