import pandas as pd
import datetime
import asyncio
import aiomysql
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from Contrat.fonctionnalités.connexionDB import DBConnection


# --- Fonction de récupération des données de facture pour un client spécifique (pour rapport mensuel) ---
async def obtenirDataFactureClient(pool, client_id: int, year: int, month: int):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT cl.nom                  AS client_nom,
                           COALESCE(cl.prenom, '') AS client_prenom,
                           cl.adresse              AS client_adresse,
                           cl.telephone            AS client_telephone,
                           cl.categorie            AS client_categorie,
                           cl.axe                  AS client_axe,
                           f.date_traitement       AS `Date de traitement`,
                           tt.typeTraitement       AS `Traitement (Type)`,
                           pd.statut               AS `Etat traitement`,
                           f.etat                  AS `Etat paiement (Payée ou non)`,
                           f.mode                  AS `Mode de Paiement`,
                           COALESCE(
                                   (SELECT hp.new_amount
                                    FROM Historique_prix hp
                                    WHERE hp.facture_id = f.facture_id
                                    ORDER BY hp.change_date DESC, hp.history_id DESC
                                    LIMIT 1),
                                   f.montant
                           )                       AS montant_facture
                    FROM Facture f
                             JOIN PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id
                             JOIN Planning p ON pd.planning_id = p.planning_id
                             JOIN Traitement tr ON p.traitement_id = tr.traitement_id
                             JOIN TypeTraitement tt ON tr.id_type_traitement = tt.id_type_traitement
                             JOIN Contrat co ON tr.contrat_id = co.contrat_id
                             JOIN Client cl ON co.client_id = cl.client_id
                    WHERE cl.client_id = %s
                      AND YEAR(f.date_traitement) = %s
                      AND MONTH(f.date_traitement) = %s
                    ORDER BY f.date_traitement;
                    """
            await cursor.execute(query, (client_id, year, month))
            result = await cursor.fetchall()
            return result
    except Exception as e:
        print(f"Erreur lors de la récupération des données de facture : {e}")
        return []
    finally:
        if conn:
            pool.release(conn)


# --- Fonction de récupération des données de facture complètes pour un client (pour rapport annuel/complet) ---
async def get_factures_data_for_client_comprehensive(pool, client_id: int, start_date: datetime.date = None,
                                                     end_date: datetime.date = None):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT cl.nom                  AS client_nom,
                           COALESCE(cl.prenom, '') AS client_prenom,
                           cl.adresse              AS client_adresse,
                           cl.telephone            AS client_telephone,
                           cl.categorie            AS client_categorie,
                           cl.axe                  AS client_axe,
                           co.contrat_id,
                           co.date_contrat,
                           co.date_debut           AS contrat_date_debut,
                           co.date_fin             AS contrat_date_fin,
                           co.statut_contrat,
                           co.duree                AS contrat_duree_type,
                           tt.typeTraitement       AS `Type de Traitement`,
                           pd.date_planification   AS `Date de Planification`,
                           pd.statut               AS `Etat du Planning`,
                           p.redondance            AS `Redondance (Mois)`,
                           f.date_traitement       AS `Date de Facturation`,
                           f.etat                  AS `Etat de Paiement`,
                           f.mode                  AS `Mode de Paiement`,
                           COALESCE(
                                   (SELECT hp.new_amount
                                    FROM Historique_prix hp
                                    WHERE hp.facture_id = f.facture_id
                                    ORDER BY hp.change_date DESC, hp.history_id DESC
                                    LIMIT 1),
                                   f.montant
                           )                       AS `Montant Facturé`
                    FROM Client cl
                             JOIN Contrat co ON cl.client_id = co.client_id
                             JOIN Traitement tr ON co.contrat_id = tr.contrat_id
                             JOIN TypeTraitement tt ON tr.id_type_traitement = tt.id_type_traitement
                             JOIN Planning p ON tr.traitement_id = p.traitement_id
                             INNER JOIN PlanningDetails pd ON p.planning_id = pd.planning_id
                             INNER JOIN Facture f ON pd.planning_detail_id = f.planning_detail_id
                    WHERE cl.client_id = %s
                    """
            params = [client_id]

            if start_date and end_date:
                query += " AND f.date_traitement BETWEEN %s AND %s"
                params.append(start_date)
                params.append(end_date)
            elif start_date:
                query += " AND f.date_traitement >= %s"
                params.append(start_date)
            elif end_date:
                query += " AND f.date_traitement <= %s"
                params.append(end_date)

            query += " ORDER BY `Date de Planification` ASC, `Date de Facturation` ASC;"

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
async def obtenirTousClient(pool):
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
async def obtenirIDClientAvecNom(pool, client_name: str):
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


# --- Fonction pour récupérer la liste des clients, le nombre de factures et les mois des factures ---
async def obtenirInformationsClients(pool):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT c.client_id,
                           CONCAT(c.nom, ' ', COALESCE(c.prenom, '')) AS nomComplet,
                           COUNT(f.facture_id)                        AS total_factures,
                           GROUP_CONCAT(DISTINCT
                                        CONCAT(YEAR(f.date_traitement), '-', LPAD(MONTH(f.date_traitement), 2, '0'))
                                        ORDER BY YEAR(f.date_traitement) DESC, MONTH(f.date_traitement) DESC SEPARATOR
                                        ', ')                         AS facture_months
                    FROM Client c
                             LEFT JOIN Contrat co ON c.client_id = co.client_id
                             LEFT JOIN Traitement tr ON co.contrat_id = tr.contrat_id
                             LEFT JOIN Planning p ON tr.traitement_id = p.traitement_id
                             LEFT JOIN PlanningDetails pd ON p.planning_id = pd.planning_id
                             LEFT JOIN Facture f ON pd.planning_detail_id = f.planning_detail_id
                    GROUP BY c.client_id, nomComplet
                    ORDER BY nomComplet;
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


# --- Fonction pour obtenir la date de la première et de la dernière facture pour un client ---
async def get_client_earliest_latest_invoice_dates(pool, client_id: int):
    conn = None
    try:
        conn = await pool.acquire()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT MIN(f.date_traitement) AS min_date,
                           MAX(f.date_traitement) AS max_date
                    FROM Facture f
                             JOIN PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id
                             JOIN Planning p ON pd.planning_id = p.planning_id
                             JOIN Traitement tr ON p.traitement_id = tr.traitement_id
                             JOIN Contrat co ON tr.contrat_id = co.contrat_id
                    WHERE co.client_id = %s;
                    """
            await cursor.execute(query, (client_id,))
            result = await cursor.fetchone()
            return result['min_date'], result['max_date']
    except Exception as e:
        print(f"Erreur lors de la récupération des dates de facture min/max : {e}")
        return None, None
    finally:
        if conn:
            pool.release(conn)


# --- Fonction pour générer le fichier Excel de la facture client (mensuel) ---
def genererFactureExcel(data: list[dict], client_full_name: str, year: int, month: int):
    month_name_fr = datetime.date(year, month, 1).strftime('%B').capitalize()

    safe_client_name = "".join(c for c in client_full_name if c.isalnum() or c in (' ', '-', '_')).replace(' ',
                                                                                                           '_').rstrip(
        '_')
    file_name = f"{safe_client_name}-{month_name_fr}-{year}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = f"Facture {client_full_name} {month_name_fr}"

    # Styles
    bold_font = Font(bold=True)
    header_font = Font(bold=True, size=14)
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    # Définition des couleurs de remplissage
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")  # Vert clair
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")  # Rouge clair

    ligneActuelle = 1

    # Informations du client (en-tête)
    if data:
        infoClient = data[0]
        affichageNomClient = f"{infoClient['client_nom']} {infoClient['client_prenom']}"
        if infoClient['client_categorie'] != 'Particulier':
            affichageNomClient = f"{infoClient['client_nom']} (Responsable: {infoClient['client_prenom'] if infoClient['client_prenom'] else 'N/A'})"

        ws.cell(row=ligneActuelle, column=1, value="Client :").font = bold_font
        ws.cell(row=ligneActuelle, column=2, value=affichageNomClient)
        ligneActuelle += 1

        ws.cell(row=ligneActuelle, column=1, value="Adresse :").font = bold_font
        ws.cell(row=ligneActuelle, column=2, value=infoClient['client_adresse'])
        ligneActuelle += 1

        ws.cell(row=ligneActuelle, column=1, value="Téléphone :").font = bold_font
        ws.cell(row=ligneActuelle, column=2, value=infoClient['client_telephone'])
        ligneActuelle += 1

        ws.cell(row=ligneActuelle, column=1, value="Catégorie Client :").font = bold_font
        ws.cell(row=ligneActuelle, column=2, value=infoClient['client_categorie'])
        ligneActuelle += 1

        ws.cell(row=ligneActuelle, column=1, value="Axe Client :").font = bold_font
        ws.cell(row=ligneActuelle, column=2, value=infoClient['client_axe'])
        ligneActuelle += 1

    ligneActuelle += 1

    # Tableau des traitements
    table_headers = ['Date de Planification', 'Date de Facturation', 'Traitement concerné', 'Redondance (Mois)',
                     'Etat du Planning', 'Mode de Paiement', 'Etat de Paiement', 'Montant']
    num_table_cols = len(table_headers)

    # Ligne "Facture du mois de:"
    ws.cell(row=ligneActuelle, column=1, value=f"Facture du mois de : {month_name_fr} {year}").font = header_font
    ws.merge_cells(start_row=ligneActuelle, start_column=1, end_row=ligneActuelle, end_column=num_table_cols)
    ws.cell(row=ligneActuelle, column=1).alignment = Alignment(horizontal='center')
    ligneActuelle += 2

    # Écrire les en-têtes du tableau
    for col_idx, header in enumerate(table_headers, 1):
        cell = ws.cell(row=ligneActuelle, column=col_idx, value=header)
        cell.font = bold_font
        cell.border = thin_border
    ligneActuelle += 1

    if not data:
        ws.cell(row=ligneActuelle, column=1,
                value=f"Aucune facture trouvée pour le client '{client_full_name}' pour ce mois.").border = thin_border
        ws.merge_cells(start_row=ligneActuelle, start_column=1, end_row=ligneActuelle, end_column=len(table_headers))
        ligneActuelle += 1
    else:
        df_invoice_data = pd.DataFrame(data)
        df_display = df_invoice_data.reindex(columns=[
            'Date de Planification', 'Date de Facturation', 'Traitement (Type)', 'Redondance (Mois)',
            'Etat traitement', 'Mode de Paiement', 'Etat paiement (Payée ou non)', 'montant_facture'
        ])
        df_display.rename(columns={
            'Traitement (Type)': 'Traitement concerné',
            'Etat traitement': 'Etat du Planning',
            'Etat paiement (Payée ou non)': 'Etat de Paiement',
            'montant_facture': 'Montant'
        }, inplace=True)

        for r_idx, row_data in enumerate(df_display.values.tolist(), start=ligneActuelle):
            payment_status = row_data[6]
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
            ligneActuelle += 1

    ligneActuelle += 1

    # Calcul et affichage des totaux
    if data:
        df_calc = pd.DataFrame(data)

        total_by_type_paid = df_calc[df_calc['Etat paiement (Payée ou non)'] == 'Payé'].groupby('Traitement (Type)')[
            'montant_facture'].sum()

        if not total_by_type_paid.empty:
            ws.cell(row=ligneActuelle, column=1, value="Facture total pour :").font = bold_font
            ligneActuelle += 1
            for service_type, total_amount in total_by_type_paid.items():
                ws.cell(row=ligneActuelle, column=2, value=f"{service_type} (Payé)").font = bold_font
                ws.cell(row=ligneActuelle, column=3, value=total_amount).font = bold_font
                ligneActuelle += 1
        else:
            ws.cell(row=ligneActuelle, column=1,
                    value="Aucun montant payé pour les types de traitement ce mois.").font = bold_font
            ligneActuelle += 1

        ligneActuelle += 1

        # Total de paiement par mode de paiement
        ws.cell(row=ligneActuelle, column=1, value="Total de paiement par mode de paiement :").font = bold_font
        ligneActuelle += 1
        payment_mode_counts = df_calc.groupby('Mode de Paiement').size().reset_index(name='Nombre de Paiements')
        for _, row in payment_mode_counts.iterrows():
            ws.cell(row=ligneActuelle, column=2, value=f"{row['Mode de Paiement']} :").font = bold_font
            ws.cell(row=ligneActuelle, column=3, value=row['Nombre de Paiements']).font = bold_font
            ligneActuelle += 1
        ligneActuelle += 1

        grand_total = df_calc['montant_facture'].sum()
        ws.cell(row=ligneActuelle, column=1, value="Montant total des traitements effectués ce mois :").font = bold_font
        ws.cell(row=ligneActuelle, column=3, value=grand_total).font = bold_font
        ligneActuelle += 1

    max_col_for_width = len(table_headers)

    for i in range(1, max_col_for_width + 1):
        column_letter = get_column_letter(i)
        length = 0
        for row_idx in range(1, ws.max_row + 1):
            cell = ws.cell(row=row_idx, column=i)
            if cell.value is not None:
                length = max(length, len(str(cell.value)))
        ws.column_dimensions[column_letter].width = length + 2

    try:
        output = BytesIO()
        wb.save(output)
        with open(file_name, 'wb') as f:
            f.write(output.getvalue())

        print(f"Fichier '{file_name}' généré avec succès.")
    except Exception as e:
        print(f"Erreur lors de la génération du fichier Excel de la facture : {e}")


# --- Fonction pour générer le fichier Excel de la facture client complète (annuel/complet) ---
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
        client_info = data[0]
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

        ws.cell(row=current_row, column=1, value="Axe Client :").font = bold_font
        ws.cell(row=current_row, column=2, value=client_info['client_axe'])
        current_row += 1

    current_row += 1

    # Ligne de titre du rapport
    ws.cell(row=current_row, column=1,
            value=f"Rapport de Facturation pour la période : {report_period}").font = header_font
    table_headers = [
        'Date de Planification', 'Date de Facturation', 'Traitement concerné', 'Redondance (Mois)',
        'Etat du Planning', 'Mode de Paiement', 'Etat de Paiement', 'Montant Facturé'
    ]
    max_cols_for_merge = len(table_headers)
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=max_cols_for_merge)
    ws.cell(row=current_row, column=1).alignment = Alignment(horizontal='center')
    current_row += 2

    # Tableau des détails de la facture
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
        df_invoice_data = pd.DataFrame(data)
        df_display = df_invoice_data.reindex(columns=table_headers)

        for r_idx, row_data in enumerate(df_display.values.tolist(), start=current_row):
            payment_status = row_data[6]
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

    current_row += 1

    # Calcul et affichage des totaux
    if data:
        df_calc = pd.DataFrame(data)

        grand_total = df_calc['Montant Facturé'].sum()
        ws.cell(row=current_row, column=1, value="Montant Total Facturé sur la période :").font = bold_font
        ws.cell(row=current_row, column=len(table_headers), value=grand_total).font = bold_font
        current_row += 1

        total_paid = df_calc[df_calc['Etat de Paiement'] == 'Payé']['Montant Facturé'].sum()
        ws.cell(row=current_row, column=1, value="Montant Total Payé sur la période :").font = bold_font
        ws.cell(row=current_row, column=len(table_headers), value=total_paid).font = bold_font
        ws.cell(row=current_row, column=len(table_headers)).fill = green_fill
        current_row += 1

        total_unpaid = df_calc[df_calc['Etat de Paiement'] == 'Non payé']['Montant Facturé'].sum()
        ws.cell(row=current_row, column=1, value="Montant Total Impayé sur la période :").font = bold_font
        ws.cell(row=current_row, column=len(table_headers), value=total_unpaid).font = bold_font
        ws.cell(row=current_row, column=len(table_headers)).fill = red_fill
        current_row += 1

        current_row += 1

        # Total de paiement par mode de paiement
        ws.cell(row=current_row, column=1, value="Total de paiement par mode de paiement :").font = bold_font
        current_row += 1
        payment_mode_counts = df_calc.groupby('Mode de Paiement').size().reset_index(name='Nombre de Paiements')
        for _, row in payment_mode_counts.iterrows():
            ws.cell(row=current_row, column=2, value=f"{row['Mode de Paiement']} :").font = bold_font
            ws.cell(row=current_row, column=3, value=row['Nombre de Paiements']).font = bold_font
            current_row += 1
        current_row += 1

        ws.cell(row=current_row, column=1, value="Synthèse par Type de Traitement :").font = bold_font
        current_row += 1

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

    for i in range(1, len(table_headers) + 1):
        column_letter = get_column_letter(i)
        length = 0
        for row_idx in range(1, ws.max_row + 1):
            cell = ws.cell(row=row_idx, column=i)
            if cell.value is not None:
                if isinstance(cell.value, (datetime.date, datetime.datetime)):
                    cell_length = len(cell.value.strftime('%Y-%m-%d'))
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
async def main_invoice_report_menu():
    pool = None
    try:
        pool = await DBConnection()
        if pool is None:
            print("Échec de la connexion à la base de données. Annulation de l'opération.")
            return

        continue_generating_reports = True
        while continue_generating_reports:
            print("\n--- Aperçu des clients et de leurs factures ---")
            informationsClient = await obtenirInformationsClients(pool)

            if informationsClient:
                df_counts = pd.DataFrame(informationsClient)
                df_counts.rename(columns={'nomComplet': 'Nom du Client', 'total_factures': 'Nb. Factures',
                                          'facture_months': 'Mois des Factures'}, inplace=True)
                df_counts.index = df_counts.index + 1
                print(df_counts[['Nom du Client', 'Nb. Factures', 'Mois des Factures']].to_string())
                print("\n")
            else:
                print("Aucun client trouvé ou aucune facture enregistrée.")

            clients_for_selection = await obtenirTousClient(pool)

            client_map = {}
            for i, client in enumerate(clients_for_selection):
                client_map[str(i + 1)] = client

            client_id_selected = None
            client_full_name_selected = None

            while client_id_selected is None:
                choice = input(
                    "Veuillez entrer le numéro du client dans la liste ci-dessus, ou son nom complet (Nom Prénom) : ").strip()

                if choice.isdigit():
                    if choice in client_map:
                        selected_client = client_map[choice]
                        client_id_selected = selected_client['client_id']
                        client_full_name_selected = selected_client['full_name']
                        print(f"Client sélectionné : {client_full_name_selected}")
                    else:
                        print("Numéro invalide. Veuillez réessayer.")
                else:
                    client_full_name_selected = choice
                    client_id_selected = await obtenirIDClientAvecNom(pool, client_full_name_selected)
                    if client_id_selected is None:
                        print(
                            f"Client '{client_full_name_selected}' non trouvé. Veuillez vérifier le nom et réessayer.")
                    else:
                        print(f"Client trouvé : {client_full_name_selected}")

            report_generated_successfully = False
            while not report_generated_successfully:
                report_type_choice = input(
                    "\nQuel type de rapport souhaitez-vous générer pour ce client ?\n"
                    "  1. Facture pour un mois spécifique\n"
                    "  2. Toutes les factures pour une année spécifique\n"
                    "  3. Toutes les factures depuis le début jusqu'au dernier traitement planifié\n"
                    "Votre choix (1, 2 ou 3) : "
                ).strip()

                if report_type_choice == '1':
                    try:
                        async with pool.acquire() as conn_for_months:
                            async with conn_for_months.cursor(aiomysql.DictCursor) as cursor:
                                query_client_months = """
                                                      SELECT DISTINCT YEAR(f.date_traitement)  AS annee,
                                                                      MONTH(f.date_traitement) AS mois
                                                      FROM Facture f
                                                               JOIN PlanningDetails pd ON f.planning_detail_id = pd.planning_detail_id
                                                               JOIN Planning p ON pd.planning_id = p.planning_id
                                                               JOIN Traitement tr ON p.traitement_id = tr.traitement_id
                                                               JOIN Contrat co ON tr.contrat_id = co.contrat_id
                                                      WHERE co.client_id = %s
                                                      ORDER BY annee DESC, mois DESC;
                                                      """
                                await cursor.execute(query_client_months, (client_id_selected,))
                                client_available_months = await cursor.fetchall()
                    except Exception as e:
                        print(f"Erreur lors de la récupération des mois disponibles pour le client : {e}")
                        client_available_months = []

                    annéeChoisi = None
                    moisChoisi = None

                    if client_available_months:
                        print(f"\nMois de factures disponibles pour {client_full_name_selected} :")
                        for i, entry in enumerate(client_available_months):
                            month_name = datetime.date(entry['annee'], entry['mois'], 1).strftime('%B').capitalize()
                            print(f"  {i + 1}. {month_name} {entry['annee']}")
                        print("  0. Entrer un autre mois/année manuellement (pour un mois non listé)")

                        while True:
                            try:
                                choice = int(
                                    input(
                                        "Choisissez un numéro de mois dans la liste ou '0' pour entrer manuellement : ").strip())
                                if 0 < choice <= len(client_available_months):
                                    annéeChoisi = client_available_months[choice - 1]['annee']
                                    moisChoisi = client_available_months[choice - 1]['mois']
                                    break
                                elif choice == 0:
                                    while True:
                                        try:
                                            year_input = input(
                                                "Veuillez entrer l'année de la facture (ex: 2023) : ").strip()
                                            month_input = input(
                                                "Veuillez entrer le numéro du mois (1-12) de la facture (ex: 6 pour Juin) : ").strip()

                                            annéeChoisi = int(year_input)
                                            moisChoisi = int(month_input)

                                            if not (1 <= moisChoisi <= 12):
                                                print(
                                                    "Numéro de mois invalide. Veuillez entrer un nombre entre 1 et 12.")
                                                continue
                                            if not (2000 <= annéeChoisi <= datetime.datetime.now().year + 5):
                                                print(
                                                    f"Année invalide. Veuillez entrer une année entre 2000 et {datetime.datetime.now().year + 5}.")
                                                continue
                                            break
                                        except ValueError:
                                            print("Entrée invalide. Veuillez entrer un nombre pour l'année et le mois.")
                                    break
                                else:
                                    print("Choix invalide. Veuillez réessayer.")
                            except ValueError:
                                print("Entrée invalide. Veuillez entrer un numéro.")
                    else:
                        print(
                            f"\nAucune facture trouvée pour {client_full_name_selected}. Veuillez entrer le mois et l'année manuellement.")
                        while True:
                            try:
                                year_input = input("Veuillez entrer l'année de la facture (ex: 2023) : ").strip()
                                month_input = input(
                                    "Veuillez entrer le numéro du mois (1-12) de la facture (ex: 6 pour Juin) : ").strip()

                                annéeChoisi = int(year_input)
                                moisChoisi = int(month_input)

                                if not (1 <= moisChoisi <= 12):
                                    print("Numéro de mois invalide. Veuillez entrer un nombre entre 1 et 12.")
                                    continue
                                if not (2000 <= annéeChoisi <= datetime.datetime.now().year + 5):
                                    print(
                                        f"Année invalide. Veuillez entrer une année entre 2000 et {datetime.datetime.now().year + 5}.")
                                    continue
                                break
                            except ValueError:
                                print("Entrée invalide. Veuillez entrer un nombre pour l'année et le mois.")

                    if annéeChoisi is None or moisChoisi is None:
                        print("Sélection de l'année ou du mois annulée. Retour au menu principal.")
                    else:
                        print(
                            f"\nPréparation de la facture pour '{client_full_name_selected}' pour {datetime.date(annéeChoisi, moisChoisi, 1).strftime('%B').capitalize()} {annéeChoisi}...")

                        factures_data = await obtenirDataFactureClient(pool, client_id_selected, annéeChoisi,
                                                                       moisChoisi)
                        genererFactureExcel(factures_data, client_full_name_selected, annéeChoisi, moisChoisi)
                        report_generated_successfully = True

                elif report_type_choice == '2':
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

                    print(
                        f"\nPréparation du rapport de facture pour '{client_full_name_selected}' pour la période : {report_period_str}...")

                    factures_data = await get_factures_data_for_client_comprehensive(pool, client_id_selected,
                                                                                     start_date,
                                                                                     end_date)
                    generate_comprehensive_facture_excel(factures_data, client_full_name_selected, report_period_str)
                    report_generated_successfully = True

                elif report_type_choice == '3':
                    min_date, max_date = await get_client_earliest_latest_invoice_dates(pool, client_id_selected)

                    if min_date and max_date:
                        start_date = min_date.date() if isinstance(min_date, datetime.datetime) else min_date
                        end_date = max_date.date() if isinstance(max_date, datetime.datetime) else max_date
                        report_period_str = f"Complet_{start_date.year}_à_{end_date.year}"

                        print(
                            f"\nPréparation du rapport de facture pour '{client_full_name_selected}' pour la période : {report_period_str}...")

                        factures_data = await get_factures_data_for_client_comprehensive(pool, client_id_selected,
                                                                                         start_date,
                                                                                         end_date)
                        generate_comprehensive_facture_excel(factures_data, client_full_name_selected,
                                                             report_period_str)
                        report_generated_successfully = True
                    else:
                        print("Aucune donnée de facture trouvée pour ce client pour générer un rapport complet.")
                else:
                    print("Choix invalide. Veuillez entrer '1', '2' ou '3'.")

            while True:
                continue_choice = input("\nVoulez-vous générer un autre rapport ? (oui/non) : ").strip().lower()
                if continue_choice in ['oui', 'o']:
                    break
                elif continue_choice in ['non', 'n']:
                    continue_generating_reports = False
                    print("Quitting application.")
                    break
                else:
                    print("Choix invalide. Veuillez répondre 'oui' ou 'non'.")

    except Exception as e:
        print(f"Une erreur inattendue est survenue dans le script principal : {e}")
    finally:
        if pool:
            pool.close()


if __name__ == "__main__":
    asyncio.run(main_invoice_report_menu())