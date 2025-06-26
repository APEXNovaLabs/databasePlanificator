import pandas as pd
import datetime
import asyncio
import aiomysql
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from Contrat.fonctionnalités.connexionDB import DBConnection


# --- Fonction de récupération des données de facture complètes pour un client ---
async def get_factures_data_for_client_comprehensive(pool, client_id: int, start_date: datetime.date = None,
                                                     end_date: datetime.date = None):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT cl.nom                AS client_nom, \
                           cl.prenom             AS client_prenom, \
                           cl.adresse            AS client_adresse,
                           cl.telephone          AS client_telephone, \
                           cl.categorie          AS client_categorie,
                           co.contrat_id, \
                           co.date_contrat, \
                           co.date_debut         AS contrat_date_debut,
                           co.date_fin           AS contrat_date_fin, \
                           co.statut_contrat, \
                           co.duree              AS contrat_duree_type,
                           tt.typeTraitement     AS `Type de Traitement`,
                           pd.date_planification AS `Date de Planification`,
                           pd.statut             AS `Etat du Planning`,
                           p.redondance          AS `Redondance (Mois)`,
                           f.date_traitement     AS `Date de Facturation`,
                           f.etat                AS `Etat de Paiement`,
                           COALESCE(
                                   (SELECT hp.new_amount
                                    FROM Historique_prix hp
                                    WHERE hp.facture_id = f.facture_id
                                    ORDER BY hp.change_date DESC, hp.history_id DESC
                                    LIMIT 1),
                                   f.montant
                           )                     AS `Montant Facturé`
                    FROM Client cl
                             JOIN Contrat co ON cl.client_id = co.client_id
                             JOIN Traitement tr ON co.contrat_id = tr.contrat_id
                             JOIN TypeTraitement tt ON tr.id_type_traitement = tt.id_type_traitement
                             JOIN Planning p ON tr.traitement_id = p.traitement_id
                             LEFT JOIN PlanningDetails pd ON p.planning_id = pd.planning_id
                             LEFT JOIN Facture f ON pd.planning_detail_id = f.planning_detail_id
                    WHERE cl.client_id = %s
                    """
            params = [client_id]

            if start_date and end_date:
                query += " AND f.date_traitement BETWEEN %s AND %s"
                params.append(start_date)
                params.append(end_date)
            elif start_date:  # Only start_date provided, assume from start_date onwards
                query += " AND f.date_traitement >= %s"
                params.append(start_date)
            elif end_date:  # Only end_date provided, assume up to end_date
                query += " AND f.date_traitement <= %s"
                params.append(end_date)

            query += " ORDER BY co.date_contrat ASC, `Date de Planification` ASC, `Date de Facturation` ASC;"

            await cursor.execute(query, tuple(params))
            result = await cursor.fetchall()
            return result
    except Exception as e:
        print(f"Erreur lors de la récupération des données de facture complètes : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)


# --- Fonction utilitaire pour obtenir le client_id et nom complet de tous les clients ---
async def get_all_clients(pool):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT client_id, CONCAT(nom, ' ', COALESCE(prenom, '')) AS full_name
                    FROM Client
                    ORDER BY full_name;
                    """
            await cursor.execute(query)
            result = await cursor.fetchall()
            return result
    except Exception as e:
        print(f"Erreur lors de la récupération de la liste des clients : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)


# --- Fonction utilitaire pour obtenir le client_id à partir du nom/prénom ---
async def get_client_id_by_name(pool, client_name: str):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT client_id
                    FROM Client
                    WHERE CONCAT(nom, ' ', COALESCE(prenom, '')) = %s
                    LIMIT 1;
                    """
            await cursor.execute(query, (client_name,))
            result = await cursor.fetchone()
            return result['client_id'] if result else None
    except Exception as e:
        print(f"Erreur lors de la recherche du client par nom : {e}")
        return None
    finally:
        if conn:
            pool.release(conn)


# --- Fonction pour récupérer la liste des clients et les mois/années de factures disponibles (pour le menu) ---
async def get_client_invoice_counts_and_months(pool):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT c.client_id,
                           CONCAT(c.nom, ' ', COALESCE(c.prenom, '')) AS full_name,
                           COUNT(f.facture_id)                        AS total_factures,
                           GROUP_CONCAT(DISTINCT
                                        CONCAT(YEAR(f.date_traitement), '-', LPAD(MONTH(f.date_traitement), 2, '0'))
                                        ORDER BY YEAR(f.date_traitement) DESC, MONTH(f.date_traitement) DESC SEPARATOR \
                                        ', ')                         AS facture_months
                    FROM Client c
                             LEFT JOIN Contrat co ON c.client_id = co.client_id
                             LEFT JOIN Traitement tr ON co.contrat_id = tr.contrat_id
                             LEFT JOIN Planning p ON tr.traitement_id = p.traitement_id
                             LEFT JOIN PlanningDetails pd ON p.planning_id = pd.planning_id
                             LEFT JOIN Facture f ON pd.planning_detail_id = f.planning_detail_id
                    GROUP BY c.client_id, full_name
                    ORDER BY full_name;
                    """
            await cursor.execute(query)
            result = await cursor.fetchall()
            return result
    except Exception as e:
        print(f"Erreur lors de la récupération du nombre de factures par client et des mois : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)


# --- Fonction pour générer le fichier Excel de la facture client complète ---
def generate_comprehensive_facture_excel(data: list[dict], client_full_name: str, report_period: str):
    safe_client_name = "".join(c for c in client_full_name if c.isalnum() or c in (' ', '-', '_')).replace(' ',
                                                                                                           '_').rstrip(
        '_')
    file_name = f"Rapport_Factures_{safe_client_name}_{report_period.replace(' ', '_')}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = f"Factures {client_full_name} {report_period}"

    # Styles
    bold_font = Font(bold=True)
    header_font = Font(bold=True, size=14)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'),
                         bottom=Side(style='thin'))

    # Définition des couleurs de remplissage
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")  # Vert clair
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")  # Rouge clair

    current_row = 1

    # Informations du client (en-tête)
    if data:
        client_info = data[0]  # Prendre les infos du premier enregistrement pour le client
        client_display_name = f"{client_info['client_nom']} {client_info['client_prenom']}"
        if client_info['client_categorie'] != 'Particulier':
            client_display_name = f"{client_info['client_nom']} (Responsable: {client_info['client_prenom'] if client_info['client_prenom'] else 'N/A'})"

        ws.cell(row=current_row, column=1, value="Client :").font = bold_font
        ws.cell(row=current_row, column=2, value=client_display_name)
        current_row += 1

        ws.cell(row=current_row, column=1, value="Adresse :").font = bold_font
        ws.cell(row=current_row, column=2, value=client_info['client_adresse'])
        current_row += 1

        ws.cell(row=current_row, column=1, value="Téléphone :").font = bold_font
        ws.cell(row=current_row, column=2, value=client_info['client_telephone'])
        current_row += 1

        ws.cell(row=current_row, column=1, value="Catégorie Client :").font = bold_font
        ws.cell(row=current_row, column=2, value=client_info['client_categorie'])
        current_row += 1

    current_row += 1  # Ligne vide

    # Ligne de titre du rapport
    ws.cell(row=current_row, column=1,
            value=f"Rapport de Facturation pour la période : {report_period}").font = header_font
    # Fusionner les cellules pour le titre, en fonction du nombre maximum de colonnes du tableau
    max_cols_for_merge = 13  # This should match the number of columns in table_headers
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=max_cols_for_merge)
    ws.cell(row=current_row, column=1).alignment = Alignment(horizontal='center')
    current_row += 2  # Deux lignes vides après pour la séparation avec le tableau

    # Tableau des détails de la facture
    table_headers = [
        'ID Contrat', 'Date Contrat', 'Début Contrat', 'Fin Contrat', 'Statut Contrat', 'Durée Contrat',
        'Type de Traitement', 'Redondance (Mois)', 'Date de Planification', 'Etat du Planning',
        'Date de Facturation', 'Etat de Paiement', 'Montant Facturé'
    ]

    # Écrire les en-têtes du tableau
    for col_idx, header in enumerate(table_headers, 1):
        cell = ws.cell(row=current_row, column=col_idx, value=header)
        cell.font = bold_font
        cell.border = thin_border
    current_row += 1

    if not data:
        ws.cell(row=current_row, column=1,
                value=f"Aucune facture trouvée pour le client '{client_full_name}' pour la période sélectionnée.").border = thin_border
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=len(table_headers))
        current_row += 1
    else:
        # Préparer les données pour le tableau
        df_invoice_data = pd.DataFrame(data)

        # S'assurer que les dates sont au format 'YYYY-MM-DD' pour l'affichage
        # Appliquer une fonction de formatage pour les dates/datetimes
        def format_date_if_datetime(val):
            if isinstance(val, (datetime.date, datetime.datetime)):
                return val.strftime('%Y-%m-%d')
            return val

        # Appliquer le formatage aux colonnes de date spécifiques
        date_cols = ['Date Contrat', 'Début Contrat', 'Fin Contrat', 'Date de Planification', 'Date de Facturation']
        for col in date_cols:
            # Vérifier si la colonne existe dans le DataFrame avant d'essayer de la formater
            if col in df_invoice_data.columns:
                df_invoice_data[col] = df_invoice_data[col].apply(format_date_if_datetime)

        # Réordonner les colonnes pour l'affichage selon table_headers
        # Utiliser .reindex pour s'assurer que l'ordre est correct et que les colonnes manquantes sont gérées (bien que non attendu ici)
        df_display = df_invoice_data.reindex(columns=table_headers)

        # Écrire les données du tableau et appliquer la couleur
        for r_idx, row_data in enumerate(df_display.values.tolist(), start=current_row):
            # Déterminer la couleur de remplissage basée sur l'état de paiement
            # 'Etat de Paiement' est la 12ème colonne dans table_headers (index 11)
            payment_status = row_data[11]
            fill_to_apply = None
            if payment_status == 'Payé':
                fill_to_apply = green_fill
            elif payment_status == 'Non payé':
                fill_to_apply = red_fill

            for c_idx, value in enumerate(row_data, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                cell.border = thin_border
                if fill_to_apply:
                    cell.fill = fill_to_apply
            current_row += 1

    current_row += 1  # Ligne vide avant les totaux

    # Calcul et affichage des totaux
    if data:
        df_calc = pd.DataFrame(data)  # Utilise le DataFrame complet

        # Total général
        grand_total = df_calc['Montant Facturé'].sum()
        ws.cell(row=current_row, column=1, value="Montant Total Facturé sur la période :").font = bold_font
        ws.cell(row=current_row, column=len(table_headers), value=grand_total).font = bold_font
        current_row += 1

        # Total payé
        total_paid = df_calc[df_calc['Etat de Paiement'] == 'Payé']['Montant Facturé'].sum()
        ws.cell(row=current_row, column=1, value="Montant Total Payé sur la période :").font = bold_font
        ws.cell(row=current_row, column=len(table_headers), value=total_paid).font = bold_font
        ws.cell(row=current_row, column=len(table_headers)).fill = green_fill
        current_row += 1

        # Total impayé
        total_unpaid = df_calc[df_calc['Etat de Paiement'] == 'Non payé']['Montant Facturé'].sum()
        ws.cell(row=current_row, column=1, value="Montant Total Impayé sur la période :").font = bold_font
        ws.cell(row=current_row, column=len(table_headers), value=total_unpaid).font = bold_font
        ws.cell(row=current_row, column=len(table_headers)).fill = red_fill
        current_row += 1

        current_row += 1  # Ligne vide

        # Totaux par type de traitement (tous statuts)
        ws.cell(row=current_row, column=1, value="Synthèse par Type de Traitement :").font = bold_font
        current_row += 1

        # S'assurer que 'Type de Traitement' est une colonne pour le groupby
        if 'Type de Traitement' in df_calc.columns:
            total_by_type = df_calc.groupby('Type de Traitement')['Montant Facturé'].sum().reset_index()
            for _, row in total_by_type.iterrows():
                ws.cell(row=current_row, column=2, value=row['Type de Traitement']).font = bold_font
                ws.cell(row=current_row, column=3, value=row['Montant Facturé']).font = bold_font
                current_row += 1
        else:
            ws.cell(row=current_row, column=1,
                    value="Impossible de synthétiser par type de traitement (colonne manquante).")
            current_row += 1

    # Ajuster la largeur des colonnes
    for i in range(1, len(table_headers) + 1):
        column_letter = get_column_letter(i)
        length = 0
        for row_idx in range(1, ws.max_row + 1):
            cell = ws.cell(row=row_idx, column=i)
            if cell.value is not None:
                # Gérer les dates et autres types pour la longueur
                if isinstance(cell.value, (datetime.date, datetime.datetime)):
                    cell_length = len(cell.value.strftime('%Y-%m-%d'))  # Format standard de date
                else:
                    cell_length = len(str(cell.value))
                length = max(length, cell_length)
        ws.column_dimensions[column_letter].width = length + 2

    try:
        output = BytesIO()
        wb.save(output)
        with open(file_name, 'wb') as f:
            f.write(output.getvalue())

        print(f"Fichier '{file_name}' généré avec succès.")
    except Exception as e:
        print(f"Erreur lors de la génération du fichier Excel de la facture : {e}")


# --- Fonction principale pour exécuter la génération de rapport de facture ---
async def main_client_invoice_report():
    pool = None
    try:
        pool = await DBConnection()
        if not pool:
            print("Échec de la connexion à la base de données. Annulation de l'opération.")
            return

        print("\n--- Aperçu des clients et de leurs factures ---")
        client_counts_and_months = await get_client_invoice_counts_and_months(pool)

        if client_counts_and_months:
            df_counts = pd.DataFrame(client_counts_and_months)
            df_counts.rename(columns={'full_name': 'Nom du Client', 'total_factures': 'Nb. Factures',
                                      'facture_months': 'Mois des Factures'}, inplace=True)
            df_counts.index = df_counts.index + 1
            print(df_counts[['Nom du Client', 'Nb. Factures', 'Mois des Factures']].to_string())
            print("\n")
        else:
            print("Aucun client trouvé ou aucune facture enregistrée.")

        clients_for_selection = await get_all_clients(pool)

        client_map = {}
        for i, client in enumerate(clients_for_selection):
            client_map[str(i + 1)] = client

        client_id_for_report = None
        client_full_name_for_report = None

        while client_id_for_report is None:
            choice = input(
                "Veuillez entrer le numéro du client dans la liste ci-dessus, ou son nom complet (Nom Prénom) : ").strip()

            if choice.isdigit():
                if choice in client_map:
                    selected_client = client_map[choice]
                    client_id_for_report = selected_client['client_id']
                    client_full_name_for_report = selected_client['full_name']
                    print(f"Client sélectionné : {client_full_name_for_report}")
                else:
                    print("Numéro invalide. Veuillez réessayer.")
            else:
                client_full_name_for_report = choice
                client_id_for_report = await get_client_id_by_name(pool, client_full_name_for_report)
                if client_id_for_report is None:
                    print(f"Client '{client_full_name_for_report}' non trouvé. Veuillez vérifier le nom et réessayer.")
                else:
                    print(f"Client trouvé : {client_full_name_for_report}")

        # --- Sélection de la période du rapport ---
        start_date = None
        end_date = None
        report_period_str = ""

        while True:
            period_choice = input(
                "\nSouhaitez-vous générer le rapport pour :\n"
                "  1. Une année spécifique ?\n"
                "  2. Toute la durée des contrats actifs du client ?\n"
                "Votre choix (1 ou 2) : "
            ).strip()

            if period_choice == '1':
                while True:
                    try:
                        year_input = input("Veuillez entrer l'année pour le rapport (ex: 2024) : ").strip()
                        selected_year = int(year_input)
                        if not (2000 <= selected_year <= datetime.datetime.now().year + 5):
                            print(
                                f"Année invalide. Veuillez entrer une année entre 2000 et {datetime.datetime.now().year + 5}.")
                            continue
                        start_date = datetime.date(selected_year, 1, 1)
                        end_date = datetime.date(selected_year, 12, 31)
                        report_period_str = f"Année_{selected_year}"
                        break
                    except ValueError:
                        print("Entrée invalide. Veuillez entrer un nombre pour l'année.")
                break
            elif period_choice == '2':
                conn_contracts = None
                try:
                    conn_contracts = await pool.acquire()
                    async with conn_contracts.cursor(aiomysql.DictCursor) as cursor:
                        query_contract_dates = """
                                               SELECT MIN(date_debut)                    AS min_date_debut,
                                                      MAX(COALESCE(date_fin, CURDATE())) AS max_date_fin
                                               FROM Contrat
                                               WHERE client_id = %s \
                                                 AND statut_contrat = 'Actif';
                                               """
                        await cursor.execute(query_contract_dates, (client_id_for_report,))
                        contract_dates = await cursor.fetchone()

                        if contract_dates and contract_dates['min_date_debut']:
                            start_date_db = contract_dates['min_date_debut']
                            end_date_db = contract_dates['max_date_fin']

                            # Ensure these are date objects, not datetime or strings
                            start_date = start_date_db.date() if isinstance(start_date_db,
                                                                            datetime.datetime) else start_date_db
                            end_date = end_date_db.date() if isinstance(end_date_db, datetime.datetime) else end_date_db

                            report_period_str = f"Durée_Contrats_{start_date.year}-{end_date.year}"
                        else:
                            print(
                                "Aucun contrat actif trouvé pour ce client. Veuillez choisir une année spécifique ou revoir les contrats.")
                            continue  # Loop again for period_choice
                except Exception as e:
                    print(f"Erreur lors de la récupération des dates de contrat : {e}")
                    print("Impossible de déterminer la durée du contrat. Veuillez choisir une année spécifique.")
                    continue  # Loop again for period_choice
                finally:
                    if conn_contracts:
                        pool.release(conn_contracts)
                break
            else:
                print("Choix invalide. Veuillez entrer '1' ou '2'.")

        if start_date is None:  # Si aucun contrat actif n'a été trouvé et l'utilisateur a choisi l'option 2.
            print("Impossible de générer le rapport. Aucune période valide sélectionnée.")
            return

        print(
            f"\nPréparation du rapport de facture pour '{client_full_name_for_report}' pour la période : {report_period_str}...")

        factures_data = await get_factures_data_for_client_comprehensive(pool, client_id_for_report, start_date,
                                                                         end_date)

        # S'assurer que le nom complet du client est utilisé pour le rapport final
        if not client_full_name_for_report and factures_data:
            client_full_name_for_report = f"{factures_data[0]['client_nom']} {factures_data[0]['client_prenom']}"

        generate_comprehensive_facture_excel(factures_data, client_full_name_for_report, report_period_str)

    except Exception as e:
        print(f"Une erreur inattendue est survenue dans le script principal : {e}")
    finally:
        if pool:
            pool.close()


if __name__ == "__main__":
    asyncio.run(main_client_invoice_report())