import pandas as pd
import datetime
import asyncio
import aiomysql
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from connexionDB import DB_CONFIG  # Importe la configuration de la DB


# --- Fonction de récupération des traitements pour un mois donné ---
async def get_traitements_for_month(year: int, month: int):
    conn = None
    try:
        conn = await aiomysql.connect(**DB_CONFIG)
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """
                    SELECT pd.date_planification        AS `la date du traitement`, \
                           tt.typeTraitement            AS `le traitement concerné`, \
                           tt.categorieTraitement       AS `la catégorie du traitement`, \
                           CONCAT(c.nom, ' ', c.prenom) AS `le client concerné`, \
                           c.categorie                  AS `la catégorie du client`
                    FROM PlanningDetails pd \
                             JOIN \
                         Planning p ON pd.planning_id = p.planning_id \
                             JOIN \
                         Traitement t ON p.traitement_id = t.traitement_id \
                             JOIN \
                         TypeTraitement tt ON t.id_type_traitement = tt.id_type_traitement \
                             JOIN \
                         Contrat co ON t.contrat_id = co.contrat_id \
                             JOIN \
                         Client c ON co.client_id = c.client_id
                    WHERE YEAR(pd.date_planification) = %s \
                      AND MONTH(pd.date_planification) = %s
                    ORDER BY pd.date_planification; \
                    """
            await cursor.execute(query, (year, month))
            result = await cursor.fetchall()
            return result
    except Exception as e:
        print(f"Erreur lors de la récupération des traitements : {e}")
        return []
    finally:
        if conn:
            conn.close()


# --- Fonction pour générer le fichier Excel des traitements ---
def generate_traitements_excel(data: list[dict], year: int, month: int):
    month_name_fr = datetime.date(year, month, 1).strftime('%B').capitalize()
    file_name = f"traitements-{month_name_fr}-{year}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = f"Traitements {month_name_fr} {year}"

    # Styles
    bold_font = Font(bold=True)
    header_font = Font(bold=True, size=14)
    center_align = Alignment(horizontal='center', vertical='center')

    # Titre du rapport
    ws.cell(row=1, column=1, value=f"Rapport des Traitements du mois de {month_name_fr} {year}").font = header_font
    ws.cell(row=1, column=1).alignment = center_align
    # Merge cells for title (assuming max 5 data columns + 1 for count)
    num_cols_for_merge = 5  # Colonnes fixes pour le rapport de traitements
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=num_cols_for_merge)

    # Nombre total de traitements
    total_traitements = len(data)
    ws.cell(row=3, column=1, value=f"Nombre total de traitements ce mois-ci : {total_traitements}").font = bold_font

    # Ligne vide pour la séparation
    ws.cell(row=4, column=1, value="")

    if not data:
        ws.cell(row=5, column=1, value="Aucun traitement trouvé pour ce mois.")
    else:
        df = pd.DataFrame(data)

        # Écrire les en-têtes de colonne
        headers = df.columns.tolist()
        for col_idx, header in enumerate(headers, 1):
            cell = ws.cell(row=5, column=col_idx, value=header)
            cell.font = bold_font

        # Écrire les données
        # Utilisation de dataframe_to_rows pour des données structurées
        for r_idx, row_data in enumerate(df.values.tolist(),
                                         start=6):  # df.values.tolist() pour obtenir les lignes de données
            for c_idx, value in enumerate(row_data, 1):
                ws.cell(row=r_idx, column=c_idx, value=value)

    # Ajuster la largeur des colonnes
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    try:
        output = BytesIO()
        wb.save(output)  # Sauvegarde dans le buffer
        with open(file_name, 'wb') as f:
            f.write(output.getvalue())

        print(f"Fichier '{file_name}' généré avec succès.")
    except Exception as e:
        print(f"Erreur lors de la génération du fichier Excel des traitements : {e}")


# --- Fonction principale pour exécuter le rapport des traitements ---
async def main_traitements_report():
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    print(
        f"\nPréparation du rapport des traitements pour {datetime.date(current_year, current_month, 1).strftime('%B').capitalize()} {current_year}...")
    traitements_data = await get_traitements_for_month(current_year, current_month)
    generate_traitements_excel(traitements_data, current_year, current_month)


if __name__ == "__main__":
    asyncio.run(main_traitements_report())